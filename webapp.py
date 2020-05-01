

from __future__ import division
from magicblue import MagicBlue
from flask import Flask, render_template, request, json
#from ipadress import IPAddress
import time
#import smtplib
import socket
import RPi.GPIO as GPIO
import os
import sys
import serial
import struct
#time.sleep(10)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
buttonState = GPIO.input(17)
#try:
#    ser = serial.Serial('/dev/ttyACM0', 9600)
#    print(" * Successfully connected to Arduino on /dev/ttyACM0")
#except:
#    ser = serial.Serial('/dev/ttyACM1', 9600)
#    print(" * Successfully connected to Arduino on /dev/ttyACM")
#print("Trying to connect.....")
app = Flask(__name__)

bulb_mac_address = 'C8:DF:84:22:01:4C'
bulb = MagicBlue(bulb_mac_address, 9) # Replace 9 by whatever your version is ($
bulb.connect()
print(" * Successfully connected to the bulb")


#ip=socket.gethostbyname(socket.gethostname())
#ipadress=IPAddress()
#ip=ipadress.get_ipaddress()

ip= [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]


print(" * IP Adress is " + ip)







gmailUser="felixraspi@gmail.com"
gmailPass="scac2018raspiguy"
sentFrom=gmailUser
to=['harisdb12@gmail.com']
subject= "IP Adress"
body="The IP Adress to connect to is " + ip
email_text= """\
From: %s
To: %s
Subject: %s

%s
""" % (sentFrom, to, subject, body)


#server=smtplib.SMTP_SSL('smtp.gmail.com')
#server.ehlo()
#server.login(gmailUser, gmailPass)
#server.sendmail("Felix' Lamp", to, email_text)
#server.close()

print(" * Email Sent")

f = open("color.txt", "w+")
f.write("255\n")
f.write("0\n")
f.write("0\n")
f.write("0\n")
f.close()



r = 0
g = 0
b = 0
bright = 255
bulb.set_color([int(r * bright), int(g * bright), int(b * bright)])
#ser.write("+0/0/0")
#ser.write("!255")
@app.route("/")
def index():
    checkButton()
    return render_template('/main.html')

@app.route("/red", methods=["POST", "GET"])
def red():
    f = open("color.txt", "w+")
    f.write("255\n")
    f.write("255\n")
    f.write("0\n")
    f.write("0\n")
    f.close()
    r = 1
    g = 0
    b = 0
    bulb.set_color([int(r * bright), int(g * bright), int(b * bright)])
    #ser.write("+255/0/0")
    # Send instructions to arduino
    checkButton()
    return json.dumps({'Status': 'OK'});
    
@app.route("/green", methods=["POST", "GET"])
def green():
    f = open("color.txt", "w+")
    f.write("255\n")
    f.write("0\n")
    f.write("255\n")
    f.write("0\n")
    f.close()
    r = 0
    g = 1
    b = 0
    bulb.set_color([int(r * bright), int(g * bright), int(b * bright)])    # Send instructions to arduino
    #ser.write("+0/255/0")
    checkButton()
    return json.dumps({'Status': 'OK'});
    
@app.route("/blue", methods=["POST", "GET"])
def blue():
    f = open("color.txt", "w+")
    f.write("255\n")
    f.write("0\n")
    f.write("0\n")
    f.write("255\n")
    f.close()
    r = 0
    g = 0
    b = 1
    bulb.set_color([int(r * bright), int(g * bright), int(b * bright)])
    #ser.write("+0/0/255")
    #Send instructions to arduino
    checkButton()
    return json.dumps({'Status': 'OK'});

@app.route("/white", methods=["POST", "GET"])
def white():
    f = open("color.txt", "w+")
    f.write("255\n")
    f.write("255\n")
    f.write("255\n")
    f.write("255\n")
    f.close()
    r = 1
    g = 1
    b = 1
    bulb.set_color([int(r * bright), int(g * bright), int(b * bright)])
    #ser.write("+255/255/255")
    #send instructions to arduino
    checkButton()
    return json.dumps({'Status': 'OK'});

@app.route("/warmWhite", methods=["POST", "GET"])
def warmWhite():
    f = open("color.txt", "w+")
    f.write("255\n")
    f.write("255\n")
    f.write("255\n")
    f.write("255\n")
    f.close()
    bulb.set_warm_light((bright/255))
    #ser.write("+255/255/80")
    #Send instructions to arduino
    checkButton()
    return json.dumps({'Status': 'OK'});
    
@app.route("/off", methods=["POST", "GET"])
def off():
    bulb.turn_off()
    #ser.write("!0")
    #Send instrductions to arduino
    checkButton()
    return json.dumps({'Status': 'OK'});

@app.route("/on", methods=["POST", "GET"])
def on():
    bulb.turn_on()
    #ser.write("!")
    #ser.write(bright)
    #Send instructions to arduino
    checkButton()
    return json.dumps({'Status': 'OK'});

@app.route("/setColors", methods=['POST'])
def setColors():
    brightinp = request.form['brightnessSlide'];
    rinp = request.form['redSlide'];
    ginp = request.form['greenSlide'];
    binp = request.form['blueSlide'];
    bright = int(brightinp)
    r = int(rinp)
    g = int(ginp)
    b = int(binp)
    print(bright)
    print(r)
    print(g)
    print(b)
    
    f = open("color.txt", "w+")
    f.write(str(bright)+ "\n")
    f.write(str(r) + "\n")
    f.write(str(g) + "\n")
    f.write(str(b) + "\n")
    f.close()
    checkButton()
    bulb.set_color([int((r/255)*bright),int((g/255)*bright),int((b/255)*bright)])
    return json.dumps({'status':'OK', 'brightness': bright, 'red':r,'green':g,'blue':b});

@app.route("/savefile", methods=['GET'])
def savefile():
    savedata = request.args['send']
    print("data")
    print(savedata)
    f = open("/home/pi/lamp/savefile.txt", "w+")
    f.write(str(savedata))
    f.close
    checkButton()
    return json.dumps({'status':'OK'});

@app.route("/getfile", methods=["GET", "POST"])
def getfile():
    f = open("./savefile.txt", "r")
    f1 = f.readlines()
    return f1[0]

@app.route("/getcurrentcolor", methods=["GET", "POST"])
def getcurrentcolor():
    f = open("color.txt", "r")
    f1 = f.readlines()
    #message = f1[0] + "/" + f1[1] + "/" + f1[2] + "/" + f1[3]
    message = f1[0] + f1[1] + f1[2] + f1[3]
    print("Message: " + message)
    checkButton()
    return message

@app.route("/currentcolor", methods=["GET", "POST"])
def currentcolor():
    f = open("color.txt", "r")
    f1 = f.readlines()
    #message = f1[0] + "/" + f1[1] + "/" + f1[2] + "/" + f1[3]
    message = "rgb(" + f1[1] + "," + f1[2] + "," + f1[3] + ")"
    print("Message: " + message)
    checkButton()
    return message


@app.route("/getCurrentBright", methods=["GET", "POST"])
def getCurrentBright():
    f = open("color.txt", "r")
    f1 = f.readlines()
    message = f1[0]
    checkButton()
    return message

@app.route("/getCurrentRed", methods=["GET", "POST"])
def getCurrentRed():
    f = open("color.txt", "r")
    f1 = f.readlines()
    message = f1[1]
    checkButton()
    return message

@app.route("/getCurrentGreen", methods=["GET", "POST"])
def getCurrentGreen():
    f = open("color.txt", "r")
    f1 = f.readlines()
    message = f1[2]
    checkButton()
    return message

@app.route("/getCurrentBlue", methods=["GET", "POST"])
def getCurrentBlue():
    f = open("color.txt", "r")
    f1 = f.readlines()
    message = f1[3]
    checkButton()
    checkButton()
    return message

@app.route("/setSavedColor", methods=["GET"])
def setSavedColor():
    messageString = request.args['value']
    print(messageString);
    cutoff = messageString.index("(")
    messageString = messageString[cutoff+1:]
    print(messageString)
    cutoff = messageString.index(",")
    r = messageString[:cutoff]
    print("RED " + r)
    messageString = messageString[cutoff+1:]
    print(messageString)
    cutoff = messageString.index(",")
    g = messageString[1:cutoff]
    print("GREEN " + g)
    messageString = messageString[cutoff+1:]
    print(messageString)
    cutoff = messageString.index(")")
    b = messageString[1:cutoff]
    print("BLUE " + b)
    print(r, g, b)
    
    f = open("color.txt", "w+")
    f.write(str(bright) + "\n")
    f.write(str(r) + "\n")
    f.write(str(g) + "\n")
    f.write(str(b) + "\n")
    f.close()
    
    checkButton()
    bulb.set_color([int(r), int(g), int(b)])
    return json.dumps({'status':"OK"});
#    fdrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrddddddddddddddddddddddddddddddddddddddddddddddddddrddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd';///////////////\\\\\\\\\\\\\\\\\'gjkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkj222222222222222222222222222111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111m1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111nj

@app.route("/end")
def end():
    sys.exit()

def checkButton():
    count = 0
    for x in range(0,5000):
        count += GPIO.input(17)
    if count > 0:
       	shutdown_server()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()






    
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
