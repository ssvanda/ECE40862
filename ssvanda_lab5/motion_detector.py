import esp32
import socket
import network
import struct
import math
from machine import I2C, ADC, Pin, Timer, RTC, PWM
import urequests
import ujson
import time
#https://maker.ifttt.com/trigger/{Motion_Detected}/with/key/HAZT0dj6QHh9xi_1i8Mg
#https://api.thingspeak.com/update?api_key=W4F7573ZIBKWJ1UL&field1=0



def createI2Cbus():
    #For the feather board
    #pin 18 is SCL
    #pin 17 is SDA

    i2c = I2C(scl = Pin(22), sda = Pin(23), freq = 400000)
    #data registers
    #0x00  0= device ID // ADXL343 id code of 0xE5, 345 octal
    devIDaddress = 0x00
    DEVIDreg = 0xe5
    #address for PIN12 high = 0x3a, 0x3b
    #address for PIN12 gnd  = 0xa6, 0xa7
    #                             W/R
    #write = 0x3a
    #read = 0x3b
    print(i2c.scan())
    address = i2c.scan()[1]
    write = address << 1
    read = write | 1
   
    #SECTION3.3
    XaxisAddress = 0x1e
    YaxisAddress = 0x1f
    ZaxisAddress = 0x20
   
    dataFormat = 0x31
    #readfrom_mem reads out like b'\x()\'
    #last digit is for number of bytes to read
    if ((write != 0xa6) or (read != 0xa7)):
        print("Error regarding device address")
        exit()
    else:
    #0x1E 30= X-axis offset
    #0x1F 31= Y-axis offset
    #0x20 32= Z-axis offset
    #When full res bit set to 0, device is in 10 bit mode //pg24 of ADXL343
        #in register 0x31 data format
       
        #write to register
        #take a bunch of measurements, write to offset register
        #write -255 in x axis offset address register bc x axis is 255
        #OFSX
        i2c.writeto_mem(address, 0x1e, b'\x02')
        #OFSY
        i2c.writeto_mem(address, 0x1f, b'\x00')
        #OFSZ
        i2c.writeto_mem(address, 0x20, b'\x7f')
        
        i2c.writeto_mem(address, 0x31, b'\x00')
        #print('Set to 10-bit full-resolution mode for output data')
        # When the FULL_RES bit is set to 0, the device is in 10-bit mode
        i2c.writeto_mem(address, 0x2c, b'\x0c')
        #print('Set data rate and power mode control')
        i2c.writeto_mem(address, 0x2d, b'\x08')
        #print('Set measure bit in power ctl register')
        # an 8 will turn on measurement
        print('Accelerometer Calibrated')
    return i2c, address
def twosComp(number):
    if number > 32767:
        number = number - 65535 
    return number
    
    
    
def I2Cread(i2c, address):
    #x axis data 0 and 1
   
    measurements = i2c.readfrom_mem(address, 0x32, 6)
    print(measurements)
    zVec = int(bin(measurements[4]) or bin(measurements[5] << 8))
    #y axis data 0 and 1
    yVec = int(bin(measurements[2]) or bin(measurements[3] << 8))
    #z axis data 0 and 1
    xVec = int(bin(measurements[0]) or bin(measurements[1] << 8))
    #16th bit is the sign bit, 32767, if greater than 2^16, sub it by 65536
    # x = x - 65536
    #convert it to int, then see what value,
    
    X = round((twosComp(xVec) / 256),2)
    Y = round((twosComp(yVec) / 256),2)
    Z = round((twosComp(zVec) / 256),3)
    
    acc = math.sqrt(X**2 + Y**2 + (Z - 1)**2)
    print(f"X accel = {X}")
    print(f"Y accel = {Y}")
    print(f"Z accel = {Z}")
    print(f"Acc = {acc}")
    return X, Y, Z, acc
   

def IFMotion_DetectedTHENnotification(X, Y, Z):
    #https://maker.ifttt.com/trigger/{Motion_Detected}/with/key/HAZT0dj6QHh9xi_1i8Mg
    request_url = 'https://maker.ifttt.com/trigger/Motion_Detected/with/key/HAZT0dj6QHh9xi_1i8Mg'
    #request_url = 'https://maker.ifttt.com/trigger/Motion_Detected/with/key/HAZT0dj6QHh9xi_1i8Mg?value1=X&value2=Y&value3=Z'
    #configure output into
    #dumps will grab object and give us a string
    #post_data = ujson.dumps({ 'value1:'+ str(X) + '\n' + 'value2:' + str(accY) + '\n' + 'value3:' + str(accZ)})
    post_data = ujson.dumps({'value1':X, 'value2':Y, 'value3':Z})
    res = urequests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data)
    
    #https://maker.ifttt.com/trigger/{event}/with/key/{HAZT0dj6QHh9xi_1i8Mg}?value1=value1&value2=value2&value3=value3
    
    res.close()
   
def IFSayPhraseTHENthingSpeak(green):
    #https://api.thingspeak.com/update?api_key=W4F7573ZIBKWJ1UL&field1=0
    #url = 'https://api.thingspeak.com/update?api_key=W4F7573ZIBKWJ1UL&field1=' + str(ACTIVATE)
    #this is the GET url
    #header result=2 means that we just want 2 data
    url = 'https://api.thingspeak.com/channels/1582157/feeds.json?api_key=HWRZ04A5RVDLX8RR&results=2'
    #request for data, put into json format
    thingSpeakData = urequests.get(url).json()
    
       
    status1 = thingSpeakData['feeds'][0]['field1'].strip()
    status2 = thingSpeakData['feeds'][1]['field1'].strip()
    
    # first activate/deactivate takes place in status2
    status = status2
    

    if (status == 'activate'):
        print('I am active')
        green.on()
        #make a local variable, check its somewhere else
        #take value of LED
        #keep a while loop for measurement part
        
        
    elif (status == 'deactivate'):
        print('I am deactivated')
        green.off()
    else:
        print('Unrecognized, assumed deactivated')
        green.off()
    return status
    # how do i track changes on the thingspeak??
def wifiConnect():
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


def readMotion(i2c, address, red, green):
    if green.value():
        X, Y, Z, acc = I2Cread(i2c, address)
        if acc > 0.5:
            red.on()
        else:
            red.off()
        IFMotion_DetectedTHENnotification(X, Y, Z)
        
    
    
    
    
def main():
    red = Pin(14, Pin.OUT, Pin.PULL_DOWN)
    green = Pin(32, Pin.OUT, Pin.PULL_DOWN)
    
    wifiConnect()
    i2c, address = createI2Cbus()
    #X, Y, Z, acc = I2Cread(i2c, address)
    
    
    sayPhraseTimer = Timer(0)
    sayPhraseTimer.init(mode = Timer.PERIODIC, period = 30000, callback = lambda x: IFSayPhraseTHENthingSpeak(green))
    
    checkMeTimer = Timer(1)
    checkMeTimer.init(mode = Timer.PERIODIC, period = 10000, callback = lambda x:readMotion(i2c, address, red, green))
    
       
if __name__ == "__main__":
    main()
