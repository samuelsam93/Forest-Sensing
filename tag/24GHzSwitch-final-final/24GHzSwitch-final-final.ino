#include "Arduino.h"
#include "util/delay.h"


void setup() {
  
  Serial.begin(9600);
  digitalWrite(A3, LOW);
  delay(500);
  digitalWrite(A2, LOW);
  delay(500);
  digitalWrite(A1, LOW);
  delay(500);
  digitalWrite(A0, LOW);
  digitalWrite(2, LOW);
  Serial.println("running");

  pinMode(A0, OUTPUT); //VDD
  pinMode(A1, OUTPUT); //set VSS to output and LOW
  pinMode(A2, OUTPUT); //set CTRL to output and LOW
  pinMode(A3, OUTPUT); // set EN to output and LOW
  pinMode(2, OUTPUT); //safeReset
}

int delayVal=1500;
int ISOdelayVal=2000;
char rx_byte = 0;
double rate =  1e5;//1e5 = 100ms; 1e6 = 1s;// in microseconds
//625;// => 1500 1.5;//1000;//625 => 800 Hz; //Rates of 500, 625, 800 > modF -> modF of 1000, 800, 625
int code1[14] = {1,1,1,1,0,0,0,0,1,1,0,0,1,0};
int code2[10] = {1,0,0,0,1,1,1,0,0,1};
int loopTime = 10000;
int starttime;
int endtime;
int idleCurrentTime;
int idleStarttime;
unsigned long idleTime = 120000;
int isSafeMode=1;

void loop() {
  
  if (Serial.available() > 0) {    // is a character available?
    isSafeMode=0;
    Serial.println("safe mode 0");
    Serial.println(rate);

    rx_byte = Serial.read();       // get the character
    if ((rx_byte >= '0') && (rx_byte <= '9') || digitalRead(4)==HIGH) {
      Serial.print("Number received: ");
      Serial.println(rx_byte);
      if (rx_byte=='6') //turn off the whole board
      {  
        Serial.println("shut down");
        digitalWrite(A3, LOW);
        delay(delayVal);
        digitalWrite(A2, LOW); 
        delay(delayVal);
        digitalWrite(A1, LOW);
        delay(delayVal);
        digitalWrite(A0, LOW);
      }
      else if (rx_byte=='0') //turn off the switch
      {
        Serial.println("isolation mode");
        digitalWrite(A0, HIGH);
        delay(delayVal);
        digitalWrite(A1, HIGH);
        delay(delayVal);
        digitalWrite(A3, HIGH);
        
      }
      else if (rx_byte=='1') //switch to RF1
      {
        digitalWrite(A0, HIGH);
        delay(delayVal);
        digitalWrite(A1, HIGH);
        delay(delayVal);
        
        //Serial.println("Isolation Mode");
        //digitalWrite(A3, HIGH);
        //delay(ISOdelayVal);
        
        Serial.println("switch to RF1 always");
        digitalWrite(A2, HIGH);
        delay(delayVal);
        digitalWrite(A3, LOW);
      }
      else if (rx_byte=='2') //switch to RF2
      {
        Serial.println("switch to RF2 always");
        digitalWrite(A0, HIGH);
        delay(delayVal);
        digitalWrite(A1, HIGH);
        delay(delayVal);
        
        //Serial.println("Isolation Mode");
        //digitalWrite(A3, HIGH);
        //delay(ISOdelayVal);
        
        digitalWrite(A2, LOW);
        delay(delayVal);
        digitalWrite(A3, LOW);
      }
      else if (rx_byte=='3' || digitalRead(4)==HIGH) //switch constantly
      {
        digitalWrite(A0, HIGH);
        delay(delayVal);
        digitalWrite(A1, HIGH);
        delay(delayVal);

        Serial.println("Isolation Mode");
        digitalWrite(A3, HIGH);
        delay(ISOdelayVal);

        Serial.println("constant switching RF1-RF2");
        starttime = millis();
        endtime = starttime;

        // Switch tag on/off.
        // 1) Use millis(), not delayMicros(), to keep account of
        // the time needed of switching pins. millis() in Arduino
        // Uno is always a multiple of 4us. Overflow of millis()
        // does not matter since the subtraction always provide
        // the correct result.
        // 2) Use direct pin access instead of digitalWrite/Read,
        // since the former takes ~5us and the latter <1us.
        // 3) Tried figuring out a better solution of turning off
        // the tag, but proto-threading (pseudo-multithreading) does
        // not work with Serial input... probably add a button while
        // designing the new 3D tag?
        unsigned long curr;
        while ((PIND & _BV(2)) == 0) // digitalRead(2) == LOW
        {
          curr = micros();
          PORTC |= _BV(2); // digitalWrite(A2, HIGH);
          PORTC &= ~_BV(3); // digitalWrite(A3, LOW);
          while (micros() - curr < rate);
          curr = micros();
          PORTC &= ~_BV(2); // digitalWrite(A2, LOW);
          PORTC &= ~_BV(3); // digitalWrite(A3, LOW);
          while (micros() - curr < rate);
        }

        Serial.println("reset button pressed");
      }
      else if (rx_byte=='4') //swich by sending a code
      {
          Serial.println("Sending chirp code");
          digitalWrite(A0, HIGH);
          delay(delayVal);
          digitalWrite(A1, HIGH);
          delay(delayVal);

          Serial.println("Isolation Mode");
          digitalWrite(A3, HIGH);
          delay(ISOdelayVal);
        
          int ind=0;
          starttime = millis();
          endtime = starttime;
          while ((endtime - starttime) <=loopTime) //while (true){
          {
              if (ind>13)
                ind=0;
              if (code1[ind]==1){
                digitalWrite(A2, HIGH);
                digitalWrite(A3, LOW);
                delayMicroseconds(rate);
              }
              else
              {
                digitalWrite(A2, LOW);
                digitalWrite(A3, LOW);
                delayMicroseconds(rate);
              }
              ind=ind+1;
              endtime = millis();
          }
      }
      else if (rx_byte=='5') //swich by sending a code
      {
          Serial.println("Sending gold code");
          digitalWrite(A0, HIGH);
          delay(delayVal);
          digitalWrite(A1, HIGH);
          delay(delayVal);
          Serial.println("Isolation Mode");
          digitalWrite(A3, HIGH);
          delay(ISOdelayVal);
        
          int ind=0;
          starttime = millis();
          endtime = starttime;
          while ((endtime - starttime) <=loopTime) //while (true){
          {              if (ind>9)
                ind=0;
              if (code2[ind]==1){
                digitalWrite(A2, HIGH);
                digitalWrite(A3, LOW);
                delayMicroseconds(rate);
              }
              else
              {
                digitalWrite(A2, LOW);
                digitalWrite(A3, LOW);
                delayMicroseconds(rate);
              }
              ind=ind+1;
              endtime = millis();
          }
      }  
    }   
  }
  else if(digitalRead(4)==HIGH) 
    {
        digitalWrite(A0, HIGH);
        delay(delayVal);
        digitalWrite(A1, HIGH);
        delay(delayVal);
        Serial.println("Isolation Mode");
        digitalWrite(A3, HIGH);
        delay(ISOdelayVal);
        Serial.println("constant switching RF1-RF2");
        starttime = millis();
        endtime = starttime;
        while (digitalRead(2)==LOW)//while ((endtime - starttime) <=loopTime) //
        {
          digitalWrite(A2, HIGH);
          digitalWrite(A3, LOW);
          delayMicroseconds(rate);
          digitalWrite(A2, LOW);
          digitalWrite(A3, LOW);
          delayMicroseconds(rate);
          
          //endtime = millis();
        }
        Serial.println("reset button pressed");
    }
  else
  {
    idleCurrentTime=millis();
    //Serial.println("in idle mode");​
    if((idleCurrentTime - idleStarttime) >=idleTime  && isSafeMode==0)
    {
      isSafeMode=1;
      safeMode();
    }
  }
}
void safeMode()
{
  Serial.println("Safe Switch ShutDown");
  digitalWrite(A3, LOW);
  delay(delayVal);
  digitalWrite(A2, LOW); 
  delay(delayVal);
  digitalWrite(A1, LOW);
  delay(delayVal);
  digitalWrite(A0, LOW);
}
