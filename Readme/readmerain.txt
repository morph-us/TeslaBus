Interface of Rain Drop Sensor with Servo Motor

Library used :
   import time
   import RPi.GPIO as io
   
Functions :
	
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(c2w_tsl_rainmotor, GPIO.OUT)
	wiper = GPIO.PWM(c2w_tsl_rainmotor, 50)   # GPIO c2w_tsl_rainmotor for PWM with 50Hz
	wiper.start(2.5)                          # Set the initial motor angle to zero
     

	c2w_tsl_t4 = threading.Thread(target=c2w_tsl_rainthread)
	
	c2w_tsl_t4.start()

	c2w_tsl_t4.join()	

	# defination of rainservo
	
	def c2w_tsl_rainservo():
            c2w_tsl_output = c2w_tsl_analogInput(0) # Reading from CH0
            print(c2w_tsl_output)
            if(c2w_tsl_output>400):
                print("Not Raining")
                time.sleep(0.7)

            else:
                print("Heavy Rain")
                wiper.ChangeDutyCycle(2.5)
                wiper.ChangeDutyCycle(5)
                wiper.ChangeDutyCycle(7.5)
                time.sleep(0.7)
                wiper.ChangeDutyCycle(5)
                wiper.ChangeDutyCycle(2.5)
                time.sleep(0.7)


	
     

Components used -
  1. Rasberry  pi 3
  2. Rain Drop Sensor
  3. Bread Board
  4. Jumping Wire

Pins -
   A0 - CH0 (ADC )
   GND - GND
   Vcc - 3.3v

 Rain Drop with Raspberry :
       1. Vcc - 3.3 V (short on breadboard )
       2. GND - ground ( pin 20 )
       3. A0 - CH0 ( Rain Drop Sensor )

Protocol used :
	SPI ( Serial Peripheral Interface ) Protocol

Key Pins of SPI Protocol :
          MISO
          MOSI
          SCLK

Working :
    Description - 
	The Rain Drop Sensor is an easy module for rain detection.
It has three pins which are connected to raspberry pi. We have used 
analog pin hence ADC ( Analog to Digital Converter ) MCP3008
is used for connection with raspberry pi 3.
	In our project,we have mounted Rain Drop Sensor at
the top of the smart bus .Whenever it detectes rainwater on its 
surface,it gives output and the Servo Motor gets started .
Rain Drop Sensor uses SPI protocol.
