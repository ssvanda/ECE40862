from machine import Pin
from time import sleep
'''
led_board = Pin(13, Pin.OUT)

for i in range(10):
    led_board.value(not led_board.value())
    sleep(0.5)
print("Led blinked 5 times")
'''
count1 = 0
count2 = 0

redLED = Pin(12, Pin.OUT)
greenLED = Pin(33, Pin.OUT)
pb1 = Pin(32, Pin.IN, Pin.PULL_DOWN)
pb2 = Pin(14,Pin.IN, Pin.PULL_DOWN)

while True:
    if (count1 == 10):
        while True:
            redLED.off()
            greenLED.on()
            sleep(.1)
            redLED.on()
            greenLED.off()
            sleep(.1)
            
            if (pb2.value()):
                redLED.off()
                greenLED.off()
                print("You have successfully implemented LAB1 DEMO!!!")
                break
        break
    elif (count2 == 10):
        while True:
            redLED.off()
            greenLED.on()
            sleep(.1)
            redLED.on()
            greenLED.off()
            sleep(.1)

            if pb1.value():
                redLED.off()
                greenLED.off()
                print("You have successfully implemented LAB1 DEMO!!!")
                break
        break
    elif ((not pb1.value()) and (not pb2.value())):
        redLED.off()
        greenLED.off()
        sleep(.2)
    elif ((not pb1.value()) and (pb2.value())):
        redLED.off()
        greenLED.on()
        sleep(.2)
        count2 +=1
    elif (pb1.value() and (not pb2.value())):
        redLED.on()
        greenLED.off()
        sleep(.2)
        count1 +=1
    elif (pb1.value() and pb2.value()):
        redLED.off()
        greenLED.off() 
        sleep(.2)
        count1 +=1
        count2 +=1
        
        
        
        
        