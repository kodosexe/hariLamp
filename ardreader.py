#from __future__ import division
from magicblue import MagicBlue
import time
import serial
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)
buttonState = GPIO.input(17)
count = 0
for x in range(0,5000):
	count += GPIO.input(17)
if count > 0:
	buttonState = 0
else:
	buttonState = 1



try:
	ser = serial.Serial('/dev/ttyACM0', 9600)
	print(" * Successfully connected to Arduino on /dev/ttyACM0")
except:
	ser = serial.Serial('/dev/ttyACM1', 9600)
	print(" * Successfully connected to Arduino on /dev/ttyACM1")
print(" * Trying to connect....")
r = 1.0
g = 1.0
b = 1.0
bright = 255

bulb_mac_address = 'C8:DF:84:22:01:4C'
bulb = MagicBlue(bulb_mac_address, 9)
bulb.connect()
print(" * Connected")
bulb.turn_on()
time.sleep(2)
#bulb.set_color([255, 0, 0])
while True:
	recieved = ''
	recievedByte = b''
	while ser.in_waiting > 0:
        	recievedByte = ser.readline()
	recieved = str(recievedByte, 'utf-8')
	##recieved = recievedByte
	#print(recieved)
	if len(recieved) > 0 and recieved[0:1] == "+":
		indexSlash = int(recieved.index('/'))
		rstr = recieved[1:indexSlash]
		recieved = recieved[indexSlash + 1:]

		indexSlash = recieved.index('/')
		gstr = recieved[0:indexSlash]
		recieved = recieved[indexSlash + 1:]
		bstr = recieved[0:]

		r = float(rstr) / 255
		g = float(gstr) / 255
		b = float(bstr) / 255
		rint = int(r * bright)
		gint = int(g * bright)
		bint = int(b * bright)
		#print(rint, gint, bint)
		bulb.set_color([rint, gint, bint])
	if len(recieved) > 0 and recieved[0:1] == "!":
		bright = int(recieved[1:])
		rint = int(r * bright)
		gint = int(g * bright)
		bint = int(b * bright)
		bulb.set_color([rint, gint, bint])
	count = 0
	for x in range(0,5000):
        	count += GPIO.input(17)
	if count > 0:
		newstate = 0
	else:
		newstate = 1


	if (newstate != buttonState):
		sys.exit()
