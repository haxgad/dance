#include <Arduino.h>

// Global Variables
float sensorValue = 0;   // Variable to store value from analog read
float halvedVoltage = 0;
float voltage = 0;
float current = 0;       // Calculated current value
float mCurrent = 0;
float power = 0;
float cumuPower = 0;
//float energy = 0;
unsigned long lasttime = 0;
unsigned long currenttime = 0;

// Static Variables
int baudRate = 19200;
const int SENSOR_PIN = A0;  // Input pin for measuring Vout
const int SENSOR_PIN1 = A1;  // Input pin for measuring divided voltage
const float RS = 0.1;          // Shunt resistor value (in ohms)
const int VOLTAGE_REF = 5;  // Reference voltage for analog read

#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

//MPU6050 mpu;
MPU6050 mpu[5];

#define SENSOR0_AD0 13
#define SENSOR1_AD0 11
#define SENSOR2_AD0 10
#define SENSOR3_AD0 9
#define SENSOR4_AD0 8

int activeSensor = 0;

double sensorReadings[15]; 

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
//uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t packetSizes[5];    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector

const int offset0[6] = {-3273, -1300, 1387, -17, -41, 81};
const int offset1[6] = {-2734, 2518, 1139, 41, -35, 52};
const int offset2[6] = {1960, -204, 1074, 203, -144, 25};
const int offset3[6] = {-3742, 746, 1984, 80, -25, 83};
const int offset4[6] = {983, -2752, 1027, 273, -40, -159};

void SetOffsets(int mpuNum, int TheOffsets[6])
  { mpu[mpuNum].setXAccelOffset(TheOffsets [0]);
    mpu[mpuNum].setYAccelOffset(TheOffsets [1]);
    mpu[mpuNum].setZAccelOffset(TheOffsets [2]);
    mpu[mpuNum].setXGyroOffset (TheOffsets [3]);
    mpu[mpuNum].setYGyroOffset (TheOffsets [4]);
    mpu[mpuNum].setZGyroOffset (TheOffsets [5]);
  } // SetOffsets


// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high

#include "Arduino.h"
#include <SoftwareSerial.h>
#include "Arduino_FreeRTOS.h"
#include "semphr.h"  // add the FreeRTOS functions for Semaphores (or Flags).

// Declare a mutex Semaphore Handle which we will use to manage the Serial Port.
// It will be used to ensure only only one Task is accessing this resource at any time.
SemaphoreHandle_t xSerialSemaphore;

// void HandShake( void *pvParameters __attribute__((unused)) ) //http://www.robopapa.com/Projects/RaspberryPiArduinoCommunication
// {
//   for (;;)
//   {
//     if ( xSemaphoreTake( xSerialSemaphore, ( TickType_t ) 5 ) == pdTRUE )
//     {
    
//     xSemaphoreGive( xSerialSemaphore );
//     }
//   vTaskDelay(100);
//   }  
// }

// Definition of packet structure
typedef struct DataPacket{
//  int16_t sensorID0;
  int16_t readings0[3];
//  int16_t sensorID1;
  int16_t readings1[3];
//  int16_t sensorID2;
  int16_t readings2[3];
//  int16_t sensorID3;
  int16_t readings3[3];
//  int16_t sensorID4;
  int16_t readings4[3];
  int16_t powerID;
  int16_t voltageV;
  int16_t currentV;
  int16_t powerV;
} DataPacket;

// Serialize method, adapted from lecture notes
unsigned int serialize(char *buf, void *p, size_t size)
{
  int16_t checksum = 0;
  buf[0]=size;
  memcpy(buf+1, p, size);
  for(int i=1; i<=(int)size; i++)
  {
     checksum ^= buf[i];
  }
  //Serial.print("Checksum is ");
  //Serial.println((int)checksum);
  buf[size+1]=checksum;
  return size+2;
}

unsigned int deserialize(void *p, char *buf)
{
  size_t size = buf[0];
  char checksum = 0;

  for (int i=1; i<=size; i++)
  checksum ^= buf[i];

  if (checksum == buf[size+1])
  {
    memcpy(p, buf+1, size);
    //Serial.print("checksum correct: ");
    //Serial.println(checksum);
    return 1;

  } 
  else
  {
    Serial.println("checksum Wrong");
    return 0;
  }
}  

unsigned sendConfig(char * buffer, unsigned char deviceCode[],double readings[])
{
  DataPacket pkt;
//  pkt.sensorID0 = 0;
  pkt.readings0[0] = readings[0] * 1000;
  pkt.readings0[1] = readings[1] * 1000;
  pkt.readings0[2] = readings[2] * 1000;
//  pkt.sensorID1 = 1;
  pkt.readings1[0] = readings[3] * 1000;
  pkt.readings1[1] = readings[4] * 1000;
  pkt.readings1[2] = readings[5] * 1000;
//  pkt.sensorID2 = 2;
  pkt.readings2[0] = readings[6] * 1000;
  pkt.readings2[1] = readings[7] * 1000;
  pkt.readings2[2] = readings[8] * 1000;
//  pkt.sensorID3 = 3;
  pkt.readings3[0] = readings[9] * 1000;
  pkt.readings3[1] = readings[10] * 1000;
  pkt.readings3[2] = readings[11] * 1000;
//  pkt.sensorID4 = 4;
  pkt.readings4[0] = readings[12] * 1000;
  pkt.readings4[1] = readings[13] * 1000;
  pkt.readings4[2] = readings[14] * 1000;
  pkt.powerID = 9;
  pkt.voltageV = voltage * 1000;
  pkt.currentV = current * 1000;
  pkt.powerV = cumuPower;
  unsigned len = serialize(buffer, &pkt, sizeof(pkt));
  return len;
}


// Adapted from lecture notes
void sendSerialData(char *buffer, int len)
{
  //Serial.println(len);
  char startByte = 'A';
  Serial2.write(startByte);
  for(int i=0; i<len; i++)
  {
  // Serial.print("a");
  Serial2.write(buffer[i]);
  }
}

/*--------------------------------------------------*/
/*---------------------- Tasks ---------------------*/
/*--------------------------------------------------*/
void Task1( void *pvParameters __attribute__((unused)) )  // This is a Task.
{
  for (;;)
  {
    // read the input pin:
    // int buttonState = digitalRead(pushButton);

    // See if we can obtain or "Take" the Serial Semaphore.
    // If the semaphore is not available, wait 5 ticks of the Scheduler to see if it becomes free.
    if ( xSemaphoreTake( xSerialSemaphore, ( TickType_t ) 5 ) == pdTRUE )
    {
      //Serial.println("Obtaining readings from sensors");
      //mpuInterrupt = true;
      
      // if programming failed, don't try to do anything
      if (!dmpReady) return;
    /*
      // wait for MPU interrupt or extra packet(s) available
      while (!mpuInterrupt && fifoCount < packetSize) {
          if (mpuInterrupt && fifoCount < packetSize) {
            // try to get out of the infinite loop 
            fifoCount = mpu[activeSensor].getFIFOCount();
          }  
          // other program behavior stuff here
          // .
          // .
          // .
          // if you are really paranoid you can frequently test in between other
          // stuff to see if mpuInterrupt is true, and if so, "break;" from the
          // while() loop to immediately process the MPU data
          // .
          // .
          // .
      }
    
      // reset interrupt flag and get INT_STATUS byte
      mpuInterrupt = false;*/
      for(activeSensor=1; activeSensor<2; activeSensor++) {
      switch (activeSensor) {
        case 0:
          digitalWrite(SENSOR0_AD0, LOW);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          break;
        case 1:
          digitalWrite(SENSOR1_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          break;
        case 2:
          digitalWrite(SENSOR2_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          break;
        case 3:
          digitalWrite(SENSOR3_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          break;
        case 4:
          digitalWrite(SENSOR4_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          break;
      }
    
      mpuIntStatus = mpu[activeSensor].getIntStatus();

      // get current FIFO count
      fifoCount = mpu[activeSensor].getFIFOCount();
    
      // check for overflow (this should never happen unless our code is too inefficient)
      if ((mpuIntStatus & _BV(MPU6050_INTERRUPT_FIFO_OFLOW_BIT)) || fifoCount >= 1024) {
          // reset so we can continue cleanly
          mpu[activeSensor].resetFIFO();
          fifoCount = mpu[activeSensor].getFIFOCount();
          Serial.println(F("FIFO overflow!"));
    
      // otherwise, check for DMP data ready interrupt (this should happen frequently)
      } else if (mpuIntStatus & _BV(MPU6050_INTERRUPT_DMP_INT_BIT)) {
        //if (mpuIntStatus & _BV(MPU6050_INTERRUPT_DMP_INT_BIT)) {
            // wait for correct available data length, should be a VERY short wait
            while (fifoCount < packetSizes[activeSensor]) fifoCount = mpu[activeSensor].getFIFOCount();
      
            // read a packet from FIFO
            mpu[activeSensor].getFIFOBytes(fifoBuffer, packetSizes[activeSensor]);
            
            // track FIFO count here in case there is > 1 packet available
            // (this lets us immediately read more without waiting for an interrupt)
            fifoCount -= packetSizes[activeSensor];
      
            // display initial world-frame acceleration, adjusted to remove gravity
            // and rotated based on known orientation from quaternion
            mpu[activeSensor].dmpGetQuaternion(&q, fifoBuffer);
            mpu[activeSensor].dmpGetAccel(&aa, fifoBuffer);
            mpu[activeSensor].dmpGetGravity(&gravity, &q);
            mpu[activeSensor].dmpGetLinearAccel(&aaReal, &aa, &gravity);
            mpu[activeSensor].dmpGetLinearAccelInWorld(&aaWorld, &aaReal, &q);
            //Serial.print("aworld\t");
            double x = (double) aaWorld.x / 8192.0;
            //Serial.print(x, 5);
            //Serial.print("\t");
            double y = (double) aaWorld.y / 8192.0;
            //Serial.print(y, 5);
            //Serial.print("\t");
            double z = (double) aaWorld.z / 8192.0;
            //Serial.println(z, 5);
            int arrayCursor = activeSensor * 3;
            sensorReadings[arrayCursor] = x;
            sensorReadings[arrayCursor + 1] = y;
            sensorReadings[arrayCursor + 2] = z;
        }
      }
      xSemaphoreGive( xSerialSemaphore ); // Now free or "Give" the Serial Port for others.
    }

    vTaskDelay(1);  // one tick delay (15ms) in between reads for stability
  }
}
void Task2( void *pvParameters __attribute__((unused)) )  // This is a Task.
{
  for (;;)
  {  
    // read the input pin:
    // int buttonState = digitalRead(pushButton);

    // See if we can obtain or "Take" the Serial Semaphore.
    // If the semaphore is not available, wait 5 ticks of the Scheduler to see if it becomes free.
    if ( xSemaphoreTake( xSerialSemaphore, ( TickType_t ) 5 ) == pdTRUE )
    {
      
      if (Serial2.available() > 0)
      {
        char message = Serial2.read();
        if (message == '1')
        {
          Serial2.println("ACK");
          while (Serial2.read() >=0);
        }
      }
      //Serial.println("Sending Data to RPi");
      // Serial2.println("Data reading");
      unsigned char deviceCode[1];
      //double readings[1];
      char buffer[64];
      Serial.print("Sensor readings are: ");
      for(int i=0; i<14; i++) {
              Serial.print(sensorReadings[i], 5);
              Serial.print("\t");
          }
          Serial.println(sensorReadings[14], 5);
      unsigned len = sendConfig(buffer,deviceCode,sensorReadings);
      DataPacket results; 
      deserialize(&results, buffer);
      sendSerialData(buffer,len);
//      Serial.print("Deserialized Voltage is :");
//      Serial.print(results.voltageV);
//      Serial.println();
//      
//      Serial.print("Deserialized Current is :");
//      Serial.print(results.currentV);
//      Serial.println();
//      
//      Serial.print("Deserialized Power is :");
//      Serial.print(results.powerV);
//      Serial.println();
      //Serial.println("Done");
      
      xSemaphoreGive( xSerialSemaphore ); // Now free or "Give" the Serial Port for others.
    }

    vTaskDelay(1);  // one tick delay (15ms) in between reads for stability
  }
}
void Task3( void *pvParameters __attribute__((unused)) )  // This is a Task.
{
  for (;;)
  {

    // See if we can obtain or "Take" the Serial Semaphore.
    // If the semaphore is not available, wait 5 ticks of the Scheduler to see if it becomes free.
    if ( xSemaphoreTake( xSerialSemaphore, ( TickType_t ) 5 ) == pdTRUE )
    {
    sensorValue = analogRead(SENSOR_PIN);
    halvedVoltage = analogRead(SENSOR_PIN1);

    voltage = halvedVoltage * (5/1023.0) * 2;

    // Remap the ADC value into a voltage number (5V reference)
    sensorValue = (sensorValue * VOLTAGE_REF) / 1023;

    // Follow the equation given by the INA169 datasheet to
    // determine the current flowing through RS. Assume RL = 10k
    // Is = (Vout x 1k) / (RS x RL)
    current = sensorValue / (10 * RS);
    mCurrent = current * 1000; 
    
    power = mCurrent * VOLTAGE_REF; // unit = milli watt
    //Serial.print("Instant power = ");
    //Serial.println(power);
    unsigned int timediff = millis() - lasttime;
    //Serial.println(timediff);
    //Serial.println(double(timediff/(1000.0 *60.0*60.0 )));
    //cumuPower = cumuPower + (power * (millis() - lasttime)/ ( 1000.0 * 60.0 * 60.0)); 
    cumuPower = cumuPower + (power * (millis() - lasttime)/  1000000.0); // unit is joules
    //Serial.println("Cumulative Power is equals to: ");
    //Serial.println(cumuPower);
    lasttime = millis();

    //energy = energy + (power / 1000);
      xSemaphoreGive( xSerialSemaphore ); // Now free or "Give" the Serial Port for others.
    }



    vTaskDelay(100);  // one tick delay (15ms) in between reads for stability
  }
}


// ================================================================
// ===                      INITIAL SETUP                       ===
// ================================================================

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    Serial.begin(baudRate);
    while (!Serial); // wait for Leonardo enumeration, others continue immediately
    Serial.println("I'M ALIVE!");
    pinMode(SENSOR0_AD0, OUTPUT);
    pinMode(SENSOR1_AD0, OUTPUT);
    pinMode(SENSOR2_AD0, OUTPUT);
    pinMode(SENSOR3_AD0, OUTPUT);
    pinMode(SENSOR4_AD0, OUTPUT);

for(activeSensor=0; activeSensor<4; activeSensor++) {
    Serial.print("BEFORE SWITCH");
      switch (activeSensor) {
        case 0:
          digitalWrite(SENSOR0_AD0, LOW);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          //SetOffsets(activeSensor, offset0);
          break;
        case 1:
          digitalWrite(SENSOR1_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          //SetOffsets(activeSensor, offset1);
          break;
        case 2:
          digitalWrite(SENSOR2_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          //SetOffsets(activeSensor, offset2);
          break;
        case 3:
          digitalWrite(SENSOR3_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR4_AD0, HIGH);
          //SetOffsets(activeSensor, offset3);
          break;
        case 4:
          digitalWrite(SENSOR4_AD0, LOW);
          digitalWrite(SENSOR0_AD0, HIGH);
          digitalWrite(SENSOR1_AD0, HIGH);
          digitalWrite(SENSOR2_AD0, HIGH);
          digitalWrite(SENSOR3_AD0, HIGH);
          //SetOffsets(activeSensor, offset4);
          break;
      }

    // initialize device
    Serial.print(F("Initializing I2C devices... Sensor "));
    Serial.println(activeSensor);
    mpu[activeSensor].initialize();
    
    // verify connection
    Serial.println(F("Testing device connections..."));
    Serial.println(mpu[activeSensor].testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

    // wait for ready
    //Serial.println(F("\nSend any character to begin DMP programming and demo: "));
    //while (Serial.available() && Serial.read()); // empty buffer
    //while (!Serial.available());                 // wait for data
    //while (Serial.available() && Serial.read()); // empty buffer again

    // load and configure the DMP
    Serial.println(F("Initializing DMP..."));
    devStatus = mpu[activeSensor].dmpInitialize();
    
    // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        // turn on the DMP, now that it's ready
        Serial.println(F("Enabling DMP..."));
        mpu[activeSensor].setDMPEnabled(true);

        // enable Arduino interrupt detection
        Serial.println(F("Enabling interrupt detection ..."));
        //Timer1.initialize(100000);         // initialize timer1, and set a 0.1 second period
        //Timer1.attachInterrupt(dmpDataReady);  // attaches dmpDataReady() as a timer overflow interrupt
        mpuIntStatus = mpu[activeSensor].getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSizes[activeSensor] = mpu[activeSensor].dmpGetFIFOPacketSize();

        switch (activeSensor) {
          case 0:
            SetOffsets(activeSensor, offset0);
            break;
          case 1:
            SetOffsets(activeSensor, offset1);
            break;
          case 2:
            SetOffsets(activeSensor, offset2);
            break;
          case 3:
            SetOffsets(activeSensor, offset3);
            break;
          case 4:
            SetOffsets(activeSensor, offset4);
            break;
      }
        
    } else {
        // ERROR!
        // 1 = initial memory load failed
        // 2 = DMP configuration updates failed
        // (if it's going to break, usually the code will be 1)
        Serial.print(F("DMP Initialization failed (code "));
        Serial.print(devStatus);
        Serial.println(F(")"));
        if(activeSensor == 4) {for(;;);}
    }
    
      }

    Serial2.begin(baudRate);


  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB, on LEONARDO, MICRO, YUN, and other 32u4 based boards.
  }

  // Semaphores are useful to stop a Task proceeding, where it should be paused to wait,
  // because it is sharing a resource, such as the Serial port.
  // Semaphores should only be used whilst the scheduler is running, but we can set it up here.
  if ( xSerialSemaphore == NULL )  // Check to confirm that the Serial Semaphore has not already been created.
  {
    xSerialSemaphore = xSemaphoreCreateMutex();  // Create a mutex semaphore we will use to manage the Serial Port
    if ( ( xSerialSemaphore ) != NULL )
      xSemaphoreGive( ( xSerialSemaphore ) );  // Make the Serial Port available for use, by "Giving" the Semaphore.
  }

  // Handshake
  int isReady = 0;

  while (isReady == 0)
  {
    while (Serial2.available() == 0)
    {
      // do nothing if there is no input, wait for input in serial.
      Serial.println("Waiting for RPi...");
    }

    // if there is an incoming message, read the message
    while (Serial2.available() > 0)
    {
      char message = Serial2.read();
      if (message == '1')
      {
        Serial.print("Message Received: ");
        Serial.println(message);
        isReady = 1;
        Serial2.println("ACK");
        Serial.println("Sent ACK");
      }
      else
      {
      Serial.println("Invalid Message");
      Serial.println(message);
      }
    }
  }

  // Now set up two Tasks to run independently.
  xTaskCreate(
    Task1
    ,  (const portCHAR *)"ReadSensor"  // A name just for humans
    ,  1024  // This stack size can be checked & adjusted by reading the Stack Highwater
    ,  NULL
    ,  2  // Priority, with 3 (configMAX_PRIORITIES - 1) being the highest, and 0 being the lowest.
    ,  NULL );

  xTaskCreate(
    Task2
    ,  (const portCHAR *) "Send"
    ,  1024  // Stack size
    ,  NULL
    ,  1  // Priority
    ,  NULL );

    xTaskCreate(
    Task3
    ,  (const portCHAR *) "ReadPower"
    ,  256  // Stack size
    ,  NULL
    ,  0  // Priority
    ,  NULL );

  // Now the Task scheduler, which takes over control of scheduling individual Tasks, is automatically started.
}


// ================================================================
// ===                    MAIN PROGRAM LOOP                     ===
// ================================================================

void loop() {
}
