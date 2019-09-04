import RPi.GPIO as GPIO
import time
import os
import psutil
GPIO.setmode(GPIO.BCM)
procnameServer = "webapp.py"
procnamePoti   = "ardreader.py"
#Button Pin: 17
GPIO.setup(17,GPIO.IN)
serverRun = True
potiRun   = False

prev_input = 00
while True:
	count = 0
        for x in range(0,5000):
                count += GPIO.input(17)
        if count > 0:
                input = 0
        else:
                input = 1

	if ((not prev_input) and input):
		if (potiRun):
			print("Stopping Poti Control")
			for proc in psutil.process_iter():
				if proc.name == procnamePoti:
					proc.kill()
					potiRun = False
					print("Stopped")
		print("Starting Server Control")
		os.system("python3 /home/pi/lamp/webapp.py")
		serverRun = True
	prev_input = input
	if ((not input) and serverRun):
		print("Stopping Server Control")
		for proc in psutil.process_iter():
			if proc.name() == procnameServer:
				proc.kill()
				serverRun = False
		print("Starting Poti Control")
		os.system("python3 /home/pi/lamp/ardreader.py")
		potiRun=True
	if input:
		print("Pressed")
	else:
		print("Not Pressed")
