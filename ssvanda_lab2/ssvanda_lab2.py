from machine import Pin, PWM, ADC, Timer, RTC
from time import sleep

#Initialize and start a PWM signal on the external LED using a frequency of 10 Hz and
#a duty cycle of 256. The LED should start blinking at the defined frequency.
count = 0
pbPress1 = True
pbPress2 = False
#change freq or DC based on button press
def freqDutyChange(pin):
    if pbPress1:
        led.freq(int(pot.read()/100))
    elif (not pbPress1):
        led.duty(int(pot.read()/10))
#no idea why i need a second pb but thats how it worked out
def pbIRQ(pin):
    global pbPress1
    global pbPress2
    
    pbPress2 = False
    pbPress1 = not pbPress1
#    pbPress2 = not pbPress2
pb = Pin(32, Pin.IN, Pin.PULL_DOWN)
led = PWM(Pin(14), 10, 256)

pot = ADC(Pin(33))
pot.width(ADC.WIDTH_9BIT)
pot.atten(ADC.ATTN_11DB)

potTimer = Timer(-1)
potTimer.init(period=100, mode=Timer.PERIODIC, callback=freqDutyChange)

pb.irq(handler = pbIRQ, trigger = Pin.IRQ_RISING)

#calling all needed variables
year = int(input("Year? "))
month = int(input("Month? "))
day = int(input("Day? "))
weekday = int(input("Weekday? "))
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
microsecond = int(input("Microsecond? "))




#Use the real-time clock (RTC) and a hardware timer to display the
#current date and time every 30 seconds. Do not use time.sleep().
#Use the RTC and a timer interrupt/callback instead.
#See this URL for more information on callbacks & interrupts
#in MicroPython. 

#create an RTC object
clock = RTC()
#Get or set the date and time of the RTC with an 8-tuple with input date and time
clock.datetime((year, month, day, weekday, hour, minute, second, microsecond))
# Create a timer object using timer 0
hardwareTimer = Timer(0)
#initialize it in periodic mode
#set to read every 30 seconds
#print every 30 seconds
hardwareTimer.init(mode = Timer.PERIODIC, period = 30000, callback = lambda t: print(clock.datetime()))




while True:
    pass