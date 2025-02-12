//apparently this goes first
#define USE_ARDUINO_INTERRUPTS true       // Set-up low-level interrupts for most accurate BPM math.

//library used in project
#include <LiquidCrystal.h>                // Set-up for using LCD monitors
#include <PulseSensorPlayground.h>        // Includes the PulseSensorPlayground Library.

// Variables                              //
// initialize the library with for the    //
// numbers of the interface pins          //
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);   //
const int PulseWire = 0;                  // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
const int LED = LED_BUILTIN;              // The on-board Arduino LED< close to PIN 13
int Threshold = 550;                      // Determine which Signal to count as a beat" and which to ignore
                                          // Use the "Getting STarted Project" to fine-tune Threshold Value beyond default
                                          // Otherwise leave the default "550" value.
PulseSensorPlayground pulseSensor;        // Creates an instance of the PulseSensorPlayground object called "pulseSensor"

void setup()                              
{                                         
  //LCD SETUP                             //
  //setting up the LCD's number...        //
  //...of columns and rows                //
  lcd.begin(16, 2);                       //

  //PulseSensorPlayground SETUP           //
  Serial.begin(9600);                     //

  //Configure the PulseSensor object by assign our variables to it.
  pulseSensor.analogInput(PulseWire);
  pulseSensor.blinkOnPulse(LED);
  pulseSensor.setThreshold(Threshold);

  if(pulseSensor.begin())
  {
     
  }
}


void loop()
{
  //PulseSensorPlayground LOOP
  if(pulseSensor.sawStartOfBeat())                // Constatly test to see if "a beat happened"
  {                                               //
    int myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int"
    Serial.println(myBPM);                        // "myBPM" hold this BPM value now.

    //LCD LOOP
    //set the cursor to column 0, line 1
    //(note: line 1 is the second row, since counting begins at 0)  
    lcd.setCursor(0,0);
    if((myBPM / 100) < 1)
    {
      
      //print the number of seconds since reset:
      lcd.print("   ");
      lcd.setCursor(0,0);
      lcd.print(myBPM);
    }
    else
    {
      lcd.print("  ");
      lcd.setCursor(0,0);
      lcd.print(myBPM);   
    }
     
  }
  
  delay(20);                                      // considered best practice in a simple sketch
}
