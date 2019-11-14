IR Sensor Interface with Servo Motor


Functions :
	
	c2w_tsl_entryIR = 16
	c2w_tsl_exitIR = 18
	
	GPIO.setup(c2w_tsl_entryIR,GPIO.IN)
        
	GPIO.setup(c2w_tsl_exitIR,GPIO.IN)

	#Function to detect person using IR sensor at entry gate and increase total count variable 
    
	 c2w_tsl_sensor_entry(c2w_tsl_entryIR):
   
	
	#Function to detect person using IR sensor at exit gate and decrease total count variable 

	 c2w_tsl_sensor_exit(c2w_tsl_exitIR):

	#Function for entrygate thread 

	 c2w_tsl_entrygate():
	
	#Function for working of exitgate thread 
	
	 c2w_tsl_exitgate():
		
     

Components used :
  	1. Raspberry Pi 3
  	2. IR sensor
  	3. Servo motor
  	4. Breadboard
  	5. Jumper wires
  
Pins :
    	 IR Sensor -
		
		Vcc - 3.3 V
		GND - ground
		Data -  data pin
     
	 Servo Motor -
		
		Vcc (red wire)- 5 V
		GND (brown wire ) - ground
		PWM (orange wire )- data pin

Connections :

	   IR  Raspberrry pi :
		Vcc ( pin 1) - 3.3 V
		GND ( pin 6 ) - ground 
		Data (pin 16)- GPIO 23 ( GEN4 )
   
Servo Raspberry pi :
		
		Vcc ( pin 2 ) - 5 V
		GND (pin 9 ) - ground
		PWM (pin 3) - GPIO 2 ( I2C ) 

Protocol used :
	
	I2C ( Inter Integrated Circuit ) Protocol

Key Pins of I2C Protocol :

	1. SDA - Serial Data  ( line for master and slave to send and receive data ) 
    	2. SCL - Serial Clock ( line that carries the clock signal )

Working :
	
	Description :
	
		IR Sensors (Infrared Sensors ) are modules which detect the presence of objects before them. If object is present it
		give 3.3 V as output and if it is not present it gives 0 volt.
		An IR Sensor Module consists of three parts- an IR Transmitter , an IR Detector and a control circuit. Usually, an IR LED
		is used as an IR Transmitter and Photo Diode or Photo Transistor is used as an IR Detector. The control circuit consists of a Comparator
		IC with necessary components. Based on application and requirements, IR sensors can be implemented in two ways.  
	
		In this smart bus ,we have interfaced IR with Servo motor. As soon as person is detected by IR sensor, the door gets open 
		for a certain period of time with the help of Servo motor for a certain time. Here we have used two IR sensors and  two Servo motors.
		One module mounted at the Entry gate and the  other module mounted at Exit gate. IR Sensor used I2C protocol. Servo motor requires 5V supply. 
	
	

