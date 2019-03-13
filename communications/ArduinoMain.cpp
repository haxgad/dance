char foo;

#include "Arduino.h"
#include <SoftwareSerial.h>
#include <Arduino_FreeRTOS.h>
#include <semphr.h>  // add the FreeRTOS functions for Semaphores (or Flags).

// Declare a mutex Semaphore Handle which we will use to manage the Serial Port.
// It will be used to ensure only only one Task is accessing this resource at any time.
SemaphoreHandle_t xSerialSemaphore;

void TaskDigitalRead( void *pvParameters __attribute__((unused)) )  // This is a Task.
{
  /*
    DigitalReadSerial
    Reads a digital input on pin 2, prints the result to the serial monitor

    This example code is in the public domain.
  */

  // digital pin 2 has a pushbutton attached to it. Give it a name:
  uint8_t pushButton = 2;

  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);

  for (;;) // A Task shall never return or exit.
  {
    // read the input pin:
    int buttonState = digitalRead(pushButton);

    // See if we can obtain or "Take" the Serial Semaphore.
    // If the semaphore is not available, wait 5 ticks of the Scheduler to see if it becomes free.
    if ( xSemaphoreTake( xSerialSemaphore, ( TickType_t ) 5 ) == pdTRUE )
    {
      // We were able to obtain or "Take" the semaphore and can now access the shared resource.
      // We want to have the Serial Port for us alone, as it takes some time to print,
      // so we don't want it getting stolen during the middle of a conversion.
      // print out the state of the button:
      Serial.println(buttonState);

      xSemaphoreGive( xSerialSemaphore ); // Now free or "Give" the Serial Port for others.
    }

    vTaskDelay(100);  // one tick delay (15ms) in between reads for stability
  }
}

void TaskAnalogRead( void *pvParameters __attribute__((unused)) )  // This is a Task.
{

  for (;;)
  {
    // read the input on analog pin 0:
    int sensorValue = analogRead(A0);

    // See if we can obtain or "Take" the Serial Semaphore.
    // If the semaphore is not available, wait 5 ticks of the Scheduler to see if it becomes free.
    if ( xSemaphoreTake( xSerialSemaphore, ( TickType_t ) 5 ) == pdTRUE )
    {
      // We were able to obtain or "Take" the semaphore and can now access the shared resource.
      // We want to have the Serial Port for us alone, as it takes some time to print,
      // so we don't want it getting stolen during the middle of a conversion.
      // print out the value you read:
      Serial.println(sensorValue);

      xSemaphoreGive( xSerialSemaphore ); // Now free or "Give" the Serial Port for others.
    }

    vTaskDelay(100);  // one tick delay (15ms) in between reads for stability
  }
}
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

int number = 1;
int i;

// Definition of packet structure
typedef struct DataPacket{
  int16_t sensorID0;
  int16_t readings0[3];
  int16_t sensorID1;
  int16_t readings1[3];
  int16_t sensorID2;
  int16_t readings2[3];
  int16_t sensorID3;
  int16_t readings3[3];
  int16_t sensorID4;
  int16_t readings4[3];
  int16_t powerID;
  int16_t voltage;
  int16_t current;
  int16_t power;
} DataPacket;

// Serialize method, adapted from lecture notes
unsigned int serialize(char *buf, void *p, size_t size)
{
  char checksum = 0;
  buf[0]=size;
  memcpy(buf+1, p, size);
  for(int i=1; i<=(int)size; i++)
  {
     checksum ^= buf[i];
  }
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
  pkt.sensorID0 = 0;
  pkt.readings0[0] = 0;
  pkt.readings0[1] = 100;
  pkt.readings0[2] = 200;
  pkt.sensorID1 = 1;
  pkt.readings1[0] = 1000;
  pkt.readings1[1] = 2000;
  pkt.readings1[2] = 3000;
  pkt.sensorID2 = 2;
  pkt.readings2[0] = 1234;
  pkt.readings2[1] = 3214;
  pkt.readings2[2] = 1211;
  pkt.sensorID3 = 3;
  pkt.readings3[0] = 3000;
  pkt.readings3[1] = 1414;
  pkt.readings3[2] = 2222;
  pkt.sensorID1 = 1;
  pkt.powerID = 9;
  pkt.voltage = 10;
  pkt.current = 5;
  pkt.power = 3;
  unsigned len = serialize(buffer, &pkt, sizeof(pkt));
  return len;
}


// Adapted from lecture notes
void sendSerialData(char *buffer, int len)
{
  Serial.println(len);
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
      Serial.println("Obtaining readings from sensors");
      delay(10);
      Serial.println("Obtained readings");

      xSemaphoreGive( xSerialSemaphore ); // Now free or "Give" the Serial Port for others.
    }

    vTaskDelay(200);  // one tick delay (15ms) in between reads for stability
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
      Serial.println("Sending Data to RPi");
      // Serial2.println("Data reading");
      unsigned char deviceCode[1];
      double readings[1];
      char buffer[64];
      unsigned len = sendConfig(buffer,deviceCode,readings);
      sendSerialData(buffer,len);
      Serial.println("Done");

      xSemaphoreGive( xSerialSemaphore ); // Now free or "Give" the Serial Port for others.
    }

    vTaskDelay(200);  // one tick delay (15ms) in between reads for stability
  }
}

// Static Variables
int baudRate = 9600;

SoftwareSerial mySerial(10, 11); // RX, TX

/*--------------------------------------------------*/
/*------------------- Main Code --------------------*/
/*--------------------------------------------------*/

// the setup function runs once when you press reset or power the board
void setup() {

  // initialize serial communication at 9600 bits per second FOR COM(USB):
  Serial.begin(baudRate); 
  // initialize serial coms for UART:
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
  int isReady = 1;

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
    ,  (const portCHAR *)"DigitalRead"  // A name just for humans
    ,  256  // This stack size can be checked & adjusted by reading the Stack Highwater
    ,  NULL
    ,  2  // Priority, with 3 (configMAX_PRIORITIES - 1) being the highest, and 0 being the lowest.
    ,  NULL );

  xTaskCreate(
    Task2
    ,  (const portCHAR *) "AnalogRead"
    ,  256  // Stack size
    ,  NULL
    ,  1  // Priority
    ,  NULL );


  // Now the Task scheduler, which takes over control of scheduling individual Tasks, is automatically started.
}

void loop()
{
  // Empty. Things are done in Tasks.
}


/*--------------------------------------------------*/
/*---------------------- Notes ---------------------*/
/*--------------------------------------------------*/
// to do:
