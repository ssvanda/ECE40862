https://youtu.be/vAOHjH-lIqQ

In this lab, I set the red LED to pin 14 and the green LED to pin 32

In order to do this lab, I have two timers.
One timer checks the thingspeak channel for the google assistant keyword 'activate' or 'deactivate' every 30 seconds
If it sees activate, it then throws the green LED into an ON state

The other timer checks to see if the green LED is in an ON state. If the LED is not on, then the timer does nothing every 10 seconds
If the LED is on, it reads the I2C channel
If the acceleration of the device is greater than .5, then the red LED turns on, inferring that motion has occured.
Data from the I2C channel is then sent to the IFTTT such that notifications are sent through to my phone.