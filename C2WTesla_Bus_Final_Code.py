import RPi.GPIO as GPIO
import time


###########################################Libraries for rainservo module ###########################################
import sys
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values


###########################################Libraries for LED module ###########################################
import re
import argparse
import threading
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


GPIO.setmode(GPIO.BOARD)                                 #pin mode for Ras pi
###########################################Global variabels declarations ###########################################
c2w_tsl_total_count=0


c2w_tsl_entrymotor=3
c2w_tsl_exitmotor=11



###########################################entry motor setup  ###########################################
c2w_tsl_entrymotor=3
GPIO.setup(c2w_tsl_entrymotor, GPIO.OUT)
c2w_tsl_entrydoor = GPIO.PWM(c2w_tsl_entrymotor,50)                                 #GPIO c2w_tsl_entrymotor for PWM with 50Hz
c2w_tsl_entrydoor.start(2.5)                                                #Set the initial motor angle to zero

###########################################exit motor setup  ###########################################
c2w_tsl_exitmotor=11
GPIO.setup(c2w_tsl_exitmotor, GPIO.OUT)
c2w_tsl_exitdoor = GPIO.PWM(c2w_tsl_exitmotor ,50)# GPIO c2w_tsl_exitmotor for PWM with 50Hz
c2w_tsl_exitdoor.start(2.5)# Set the initial motor angle to zero


###########################################IR sensor setup  ###########################################
c2w_tsl_entryIR = 16
c2w_tsl_exitIR = 18
GPIO.setup(c2w_tsl_entryIR,GPIO.IN)
GPIO.setup(c2w_tsl_exitIR,GPIO.IN)


 
###########################################rain motor setup  ###########################################
c2w_tsl_rainmotor = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(c2w_tsl_rainmotor, GPIO.OUT)
wiper = GPIO.PWM(c2w_tsl_rainmotor, 50) # GPIO c2w_tsl_rainmotor for PWM with 50Hz
wiper.start(2.5) # Set the initial motor angle to zero


###########################################rain sensor setup  ###########################################
c2w_tsl_wiper_spi = spidev.SpiDev() # Created an object for wiper spi
c2w_tsl_wiper_spi.open(0,0) #bus and chip select set to zero
channel=0

###########################################LED setup  ###########################################
serial = spi(port=0, device=1, gpio=noop())
device = max7219(serial, cascaded=3 or 1, rotate=0)


###########################################Function to open entry gate###########################################
def c2w_tsl_openentrygate():
    print("entry gate open")
    c2w_tsl_entrydoor.ChangeDutyCycle(5)# 37 degre
    time.sleep(0.5)
    c2w_tsl_entrydoor.ChangeDutyCycle(7.5)# 90 degree
    time.sleep(0.5)


###########################################Function to open exit gate###########################################
def c2w_tsl_openexitgate():
    print("exit gate open")
    c2w_tsl_exitdoor.ChangeDutyCycle(5)# 37 degre
    time.sleep(0.5)
    c2w_tsl_exitdoor.ChangeDutyCycle(7.5)# 90 degree
    time.sleep(0.5)



###########################################Function to display message on LED###########################################
def c2w_tsl_startled(c2w_tsl_msg):
    show_message(device, c2w_tsl_msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)



###########################################Function to detect person using IR sensor at entry gate and increase total count variable ###########################################
def c2w_tsl_sensor_entry(c2w_tsl_entryIR):
    global c2w_tsl_total_count
    if GPIO.input(c2w_tsl_entryIR):
          time.sleep(0.2)
          return 0
    else :
          print("person entered")
          c2w_tsl_total_count+=1
          while(GPIO.input(c2w_tsl_entryIR)==0):
                      time.sleep(0.2)
          return 1;



###########################################Function to detect person using IR sensor at exit gate and decrease total count variable ###########################################

def c2w_tsl_sensor_exit(c2w_tsl_exitIR):
    global c2w_tsl_total_count
    if GPIO.input(c2w_tsl_exitIR):
          time.sleep(0.2)
          return 0

    else :
          print("person exited")
          while(GPIO.input(c2w_tsl_exitIR)==0):
                      time.sleep(0.2)
          c2w_tsl_total_count-=1
          return 1


###########################################Function for entrygate thread ###########################################

def c2w_tsl_entrygate():
    global c2w_tsl_total_count
    if(c2w_tsl_total_count<5 ) :
              flag1 = c2w_tsl_sensor_entry(c2w_tsl_entryIR)
              if(flag1 == 1):
                  c2w_tsl_openentrygate()
                  print("Total Count Entry: " + str(c2w_tsl_total_count))
                  t=time.time()
                  while(time.time()-t < 5 and c2w_tsl_total_count<5):
                      c2w_tsl_entrydoor.ChangeDutyCycle(7.5)
                      c2w_tsl_sensor_entry(c2w_tsl_entryIR)
                  
                  c2w_tsl_entrydoor.ChangeDutyCycle(2.5)
                  print("Total Count Entry: " + str(c2w_tsl_total_count))


###########################################Function for working of exitgate thread ###########################################
def c2w_tsl_exitgate():
    global c2w_tsl_total_count
    if(c2w_tsl_total_count >0) :
              flag1 = c2w_tsl_sensor_exit(c2w_tsl_exitIR)
              if(flag1 == 1):
                  c2w_tsl_openexitgate()
                  print("Total Count Exit : " + str(c2w_tsl_total_count))    
                  t=time.time()
                  while(time.time()-t < 5 and c2w_tsl_total_count>0):
                      c2w_tsl_exitdoor.ChangeDutyCycle(7.5)
                      c2w_tsl_sensor_exit(c2w_tsl_exitIR)
                  c2w_tsl_exitdoor.ChangeDutyCycle(2.5)
                  print("Total Count Exit : " + str(c2w_tsl_total_count))



###########################################Function to calculate analog input for rain sensor ###########################################
def c2w_tsl_analogInput(channel):
  c2w_tsl_wiper_spi.max_speed_hz = 1350000
  adc = c2w_tsl_wiper_spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data


###########################################Function for rain sensor and  motor integration ###########################################
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



###########################################Function for entry thread ###########################################
def c2w_tsl_entrythread():
    while True:
            c2w_tsl_entrygate()


###########################################Function for exit thread ###########################################
def c2w_tsl_exitthread():
    while True:
            c2w_tsl_exitgate()

###########################################Function for LED thread ###########################################
def c2w_tsl_ledthread():
    global c2w_tsl_total_count
    c2w_tsl_msg = "NARHE TO SINHGAD"
    c2w_tsl_startled(c2w_tsl_msg)
    while True:
            if(c2w_tsl_total_count==5):
                c2w_tsl_msg="BUS FULL "
            else:
                c2w_tsl_msg = str(c2w_tsl_total_count)
            c2w_tsl_startled(c2w_tsl_msg)

###########################################Function for rain thread ###########################################
def c2w_tsl_rainthread():
    while True:
        c2w_tsl_rainservo()

    

if __name__ == "__main__":
    try:
        c2w_tsl_t1=threading.Thread(target=c2w_tsl_entrythread)
        c2w_tsl_t2 = threading.Thread(target=c2w_tsl_exitthread)
        c2w_tsl_t3 = threading.Thread(target=c2w_tsl_ledthread)
        c2w_tsl_t4 = threading.Thread(target=c2w_tsl_rainthread)
        
        c2w_tsl_t1.start()
        c2w_tsl_t2.start()
        c2w_tsl_t3.start()
        c2w_tsl_t4.start()

        
        c2w_tsl_t1.join()
        c2w_tsl_t2.join()
        c2w_tsl_t3.join()
        c2w_tsl_t4.join()
            

    except KeyboardInterrupt:
        GPIO.cleanup()
