/*
 11-14-2013
 SparkFun Electronics 2013
 Shawn Hymel

 This code is public domain but you buy me a beer if you use this 
 and we meet someday (Beerware license).

 Description:

 This sketch shows how to use the SparkFun INA169 Breakout
 Board. As current passes through the shunt resistor (Rs), a
 voltage is generated at the Vout pin. Use an analog read and
 some math to determine the current. The current value is
 displayed through the Serial Monitor.

 Hardware connections:

 Uno Pin    INA169 Board    Function

 +5V        VCC             Power supply
 GND        GND             Ground
 A0         VOUT            Analog voltage measurement

 VIN+ and VIN- need to be connected inline with the positive
 DC power rail of a load (e.g. an Arduino, an LED, etc.).

 */

// Constants
const int SENSOR_PIN = A0;  // Input pin for measuring Vout
const int SENSOR_PIN1 = A1;  // Input pin for measuring divided voltage
const float RS = 0.1;          // Shunt resistor value (in ohms)
const int VOLTAGE_REF = 5;  // Reference voltage for analog read

// Global Variables
float sensorValue;   // Variable to store value from analog read
float halvedVoltage;
float voltage;
float current;       // Calculated current value
float mCurrent;
float power;
float energy = 0;

void setup() {

  // Initialize serial monitor
  Serial.begin(9600);

}

void loop() {

  // Read a value from the INA169 board
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
  
  power = mCurrent * VOLTAGE_REF;

  energy = energy + (power / 1000);

  // Output value (in amps) to the serial monitor to 3 decimal
  // places
  
  Serial.print("Voltage = ");
  Serial.print(voltage, 3);
  Serial.println(" V");
  Serial.print("Current = ");
  Serial.print(mCurrent, 3);
  Serial.println(" mA");
  Serial.print("Power = ");
  Serial.print(power, 3);
  Serial.println(" mW");
  Serial.print("Energy = ");
  Serial.print(energy, 3);
  Serial.println(" J");
  Serial.println("");
  
  // Delay program for a few milliseconds
  delay(1000);

}
