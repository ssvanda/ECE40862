import machine
from machine import TouchPad, Pin
from time import sleep
import esp32
import network
import ntptime
from machine import RTC, Timer, deepsleep, wake_reason
#Automatically connects to wifi network
def wifiModule():
    #used to configure WiFi connection
    #https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ssid = "Shapoopy"
    password = "12345678"
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    
    print('Connected to:', ssid)
    print('IP Address:', wlan.ifconfig()[0])
     
    
def NTPdatetime():
    ntptime.settime()
    rtc = RTC()
    y, mon, d, w, h, m, sec, microsec = rtc.datetime()
    rtc.datetime((y, mon, d, w, h, m, sec, microsec))
    month = rtc.datetime()[1]
    day = rtc.datetime()[2]
    year = rtc.datetime()[0]
    hour = rtc.datetime()[4] - 4
    minute = rtc.datetime()[5]
    second = rtc.datetime()[6]
    
    myDateTimeTimer = Timer(0)
    myDateTimeTimer.init(mode=Timer.PERIODIC, period=15000, callback=lambda x:print("Date: ", month, "/", day, "/", year, "\nTime: ", hour, ":", minute, ":", second))
    
def touchMe(wire, green):
    if wire.read() > 400:
        green.value(0)
    else:
        green.value(1)
def greenLED():
    wire = TouchPad(Pin(33))
    wire.config(500)
    green = Pin(32, Pin.OUT)
    greenTimer = Timer(2)
    greenTimer.init(mode = Timer.PERIODIC, period = 50, callback = lambda x:touchMe(wire, green))
def sleepCmd(red, pb):
    red.value(0)
    print('I am going to sleep for 1 minute.')
    machine.deepsleep(60000) #1 min of deepsleep
    
    #deepsleep for 1 min
    # no need for timer
    


def redLED():
    red = Pin(14, Pin.OUT)
    pb = Pin(15, Pin.IN, Pin.PULL_DOWN)
    red.value(1)
    esp32.wake_on_ext0(pb, esp32.WAKEUP_ANY_HIGH)
    #tells machine to wake when pb is pressed high
    redTimer = Timer(3)
    redTimer.init(mode = Timer.ONE_SHOT, period = 30000, callback = lambda x: sleepCmd(red,pb))
    #timer.ONESHOT
    #for going to sleep than waking up
    if (machine.wake_reason() == 4):
        red.value(1)
        print("Timer Wake Up")
    elif (machine.wake_reason() == 2):
        red.value(1)
        print("Woke up due to EXT0 wakeup")
def main():
    wifiModule()
    NTPdatetime()
    greenLED()
    
    redLED()
if __name__ == "__main__":
    main()
