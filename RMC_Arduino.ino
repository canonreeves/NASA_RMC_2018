/* -----------------------------------------------------------------------------
 * Example .ino file for arduino, compiled with CmdMessenger.h and
 * CmdMessenger.cpp in the sketch directory. 
 *----------------------------------------------------------------------------*/
//Changed on 5/5/2018

#include "CmdMessenger.h"
#include <Servo.h>
//#include "Math.h"

//Global Vars
#define SHOULDER_PIN 5
#define ELBOW_PIN 6
#define LEFT_F_PIN 7
#define LEFT_B_PIN 8
#define RIGHT_F_PIN 9
#define RIGHT_B_PIN 10
#define DRUM_PIN 11
#define MAX_DRUM 45
#define MAX_DELTA 10

double prev_drum = 90;

/*SoftwareSerial LEFT(NOT_A_PIN, LEFT_PIN); // RX on no pin (unused), TX on pin 11 (to S1).
SyRenSimplified Left(LEFT); // Use SWSerial as the serial port.

SoftwareSerial RIGHT(NOT_A_PIN, RIGHT_PIN); // RX on no pin (unused), TX on pin 11 (to S1).
SyRenSimplified Right(RIGHT); // Use SWSerial as the serial port.

SoftwareSerial DRUM(NOT_A_PIN, DRUM_PIN); // RX on no pin (unused), TX on pin 11 (to S1).
SyRenSimplified Drum(DRUM); // Use SWSerial as the serial port.
*/

Servo Shoulder;
Servo Elbow;
Servo Left_F;
Servo Left_B;
Servo Right_F;
Servo Right_B;
Servo Drum;

/* Define available CmdMessenger commands */
enum {
    shoulder,
    elbow,
    left_F,
    left_B,
    right_F,
    right_B,
    drum,
};

/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');

/* Create callback functions to deal with incoming messages */

/* callback */
void on_shoulder(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Shoulder.write(value);
    /* Send result back */ 
    //c.sendBinCmd(shoulder,value);
}

void on_elbow(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Elbow.write(value);
    /* Send result back */ 
    //c.sendBinCmd(elbow,value);
}

void on_left_F(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Left_F.write(value);
    /* Send result back */ 
    //c.sendBinCmd(left_F,value);
}

void on_left_B(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Left_B.write(value);
    /* Send result back */ 
    //c.sendBinCmd(left_B,value);
}

void on_right_F(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Right_F.write(value);
    /* Send result back */ 
    //c.sendBinCmd(right_F,value);
}

void on_right_B(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Right_B.write(value);
    /* Send result back */ 
    c.sendBinCmd(right_B,value);
    
}

void on_drum(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    /*int error = value - prev_drum;
    
    if(abs(error) > MAX_DELTA){
      if(value > 90) 
        value = prev_drum + MAX_DELTA;
      else if(value < 90)
        value = prev_drum - MAX_DELTA;
    }
    if(value > 90 + MAX_DRUM)
      value = 90 + MAX_DRUM;
    else if( value < (90 - MAX_DRUM))
      value = 90 - MAX_DRUM;
    Drum.write(value);
    prev_drum = value;*/
    /* Send result back */ 
    //c.sendBinCmd(drum,value);

    Drum.write(value);

}

/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) { 
    c.attach(shoulder,on_shoulder);
    c.attach(elbow,on_elbow);
    c.attach(left_F,on_left_F);
    c.attach(left_B,on_left_B);
    c.attach(right_F,on_right_F);
    c.attach(right_B,on_right_B);
    c.attach(drum,on_drum);
}

void setup() {
    Shoulder.attach(SHOULDER_PIN,1000,2000);
    Elbow.attach(ELBOW_PIN,1000,2000);
    Left_F.attach(LEFT_F_PIN,1000,2000);
    Left_B.attach(LEFT_B_PIN,1000,2000);
    Right_F.attach(RIGHT_F_PIN,1000,2000);
    Right_B.attach(RIGHT_B_PIN,1000,2000);
    Drum.attach(DRUM_PIN,1000,2000);
    Serial.begin(BAUD_RATE);
    attach_callbacks();     
}

void loop() {
    c.feedinSerialData();
    delay(10);
}
