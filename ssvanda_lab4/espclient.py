import machine
from machine import Pin
import dht
import sys
try:
  import usocket as socket
except:
  import socket
import ussl as ssl
from machine import RTC, Timer
import esp32
import network
import time
#a socket is basically the endpoint that recieves data
#endpoint sits at an IP in a port


def thingSpeak():
    
    
    hall = esp32.hall_sensor()     # read the internal hall sensor
    temp = esp32.raw_temperature() # read the internal temperature of the MCU, in Fahrenheit
    print("Internal Hall Sensor: " + str(hall))
    print("Temperature: " + str(temp))

    #HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    port = 80        # default port for socket
    # Creates a socket instance and passes in two parameters
    # AF_INET refers to the address-family IPV4
    # SOCK_STREAM means connection-oriented TCP Protocol\
    url = ('https://api.thingspeak.com/update?api_key=GJFLYW0XUYPJ1FQG&field1='+ str(temp) + "&field2=" + str(hall))

    https, nada, host, path = url.split('/', 3)
    
    #print(host)
    #print(path)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = socket.getaddrinfo(host, port)
    #print(address)
    #s.connect(address[0], port)
    #print(address[0][4])
    connectToMe = address[0][4]
    s.connect(connectToMe)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
            
        else:
            break
    s.close()
   
def stopMe():
    exit()
    
def section2():
    #used to configure WiFi connection
    #https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
    start = time.time()
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
    
    
    
    thingSpeakTimer = Timer(3)
    thingSpeakTimer.init(mode = Timer.PERIODIC, period = 16000, callback = lambda x: thingSpeak())
    breakTimer = Timer(2)
    breakTimer.init(mode = Timer.ONE_SHOT, period = 300000, callback = lambda x:stopMe())
    
    
    
    
    
def main():
    red = Pin(14, Pin.OUT)
    pb = Pin(15, Pin.IN)
    green = Pin(32, Pin.OUT)
    section2()
        
if __name__ == "__main__":
    main()
