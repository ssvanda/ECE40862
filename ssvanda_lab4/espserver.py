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


# Global variables
temp = 0# measure temperature sensor data
hall = 0# measure hall sensor data
red_led_state = 'ON'# string, check state of red led, ON or OFF
green_led_state = 'ON'# string, check state of red led, ON or OFF
push_button_state = 'PRESSED'
def connectToWifi():
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
    pass
def web_page():
    global temp
    global hall
    global red_led_state
    global green_led_state
    global push_button_state
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state, green_led_state
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    
    PUSH BUTTON Current State: <strong>""" + push_button_state + """</strong>
    </p>
    
    <p>
    </body>
    </html>"""
    
    print("hall from webpage" + str(hall))
    print("temp from webpage" + str(temp))
    #print(f"The current state of the PB is {push}")

    return html_webpage
change = True
state = False
def button_callback(x):
    global change
    global state
    if change:
        push_button_state = 'PRESSED'
    else:
        push_button_state = 'NOT PRESSED'
    state = True
    state = not state
def main():
    
    global temp
    global hall
    global red_led_state
    global green_led_state
    global push_button_state
    global pb
    connectToWifi()
    red = Pin(14, Pin.OUT)
    pb = Pin(15, Pin.IN,Pin.PULL_DOWN)
    green = Pin(32, Pin.OUT)
    hall = esp32.hall_sensor()     # read the internal hall sensor
    temp = esp32.raw_temperature() # read the internal temperature of the MCU, in Fahrenheit
    host = '' #
    port = 80
    '''
    
    address = socket.getaddrinfo(host, port)
    
    connectToMe = address[0][4]
    '''  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port)) #uses own IP
    #leaves a queue of 5's if data gets strung up
    s.listen(5)
    while True:
        # If anyone connects, we are happy to see you and it should connect
        # store client socket and IP address where it comes from
        # this socket will recieve things
        clientsocket, address = s.accept()
        # debugging f stream
        print(f"Connection from {address} has been established!")
        #gets the request recieved on the newly created socket and saves it to msg
        msg = clientsocket.recv(1024)
        msg = str(msg)
        #convert msg to a string
        # need to find it within the string
        print(f"Content = {msg}")
        hall = esp32.hall_sensor()     # read the internal hall sensor
        temp = esp32.raw_temperature() # read the internal temperature of the MCU, in Fahrenheit
        print(hall)
        print(temp)
        '''
        if 'http://172.20.10.5/?red_led=on' in response:
            red.value(1)
            red_led_state = 'ON'
            
        if 'http://172.20.10.5/?red_led=off' in response:
            red.value(0)
            red_led_state = 'OFF'
        if 'http://172.20.10.5/?green_led=on' in response:
            green.value(1)
            green_led_state = 'ON'
        if 'http://172.20.10.5/?green_led=off' in response:
            green.value(0)
            green_led_state = 'OFF'
        '''
        if msg.find('/?red_led=on') == 6:
            red.value(1)
            red_led_state = 'ON'
        if msg.find('/?red_led=off') == 6:
            red.value(0)
            red_led_state = 'OFF'
        if msg.find('/?green_led=on') == 6:
            green.value(1)
            green_led_state = 'ON'
        if msg.find('/?green_led=off') == 6:
            green.value(0)
            green_led_state = 'OFF'
        '''
        if msg.find('/?push_button=on') == 6:
            push_button_state = 'ON'
        if msg.find('/?push_button=off') == 6:
            push_button_state = 'OFF'
        '''
        '''
        print(f"The current state of the PB is {pb.value()}")
        if pb.value() == 1:
            push_button_state = 'PRESSED'
        if pb.value() == 0:
            push_button_state = 'NOT PRESSED'
        '''
        pb.irq(trigger = Pin.IRQ_RISING, handler = button_callback(pb.value()))
        #needs to be right before these sends
        response = web_page()
        #print(response)
        clientsocket.send(bytes('HTTP/1.1 200 OK\n', 'utf8'))
        clientsocket.send(bytes('Content-Type: text/html\n', 'utf8'))
        clientsocket.send(bytes('Connection: close\n\n', 'utf8'))
        clientsocket.sendall(bytes(response, 'utf8'))
        clientsocket.close()
if __name__ == "__main__":
    main()

