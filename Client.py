from gpiozero import Motor
import socket
import time

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = Servo(14, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

frmotor = Motor(forward=16, backward=17)
flmotor = Motor(forward=18, backward=13)
blmotor = Motor(forward=11, backward=12)
brmotor = Motor(forward=10, backward=9)

speed = 0.5

def left():
    global speed
    flmotor.backward(speed)
    frmotor.forward(speed)
    blmotor.backward(speed)
    brmotor.forward(speed)

def right():
    global speed
    flmotor.forward(speed)
    frmotor.backward(speed)
    blmotor.forward(speed)
    brmotor.backward(speed)

def forward():
    global speed
    flmotor.forward(speed)
    frmotor.forward(speed)
    blmotor.forward(speed)
    brmotor.forward(speed)

def reverse():
    global speed
    flmotor.backward(speed)
    frmotor.backward(speed)
    blmotor.backward(speed)
    brmotor.backward(speed)

def stop():
    flmotor.stop()
    frmotor.stop()
    blmotor.stop()
    brmotor.stop()

CAM = 0.07
servo.value = 0.0
velCam = 0.0
isStop = True

def camLeft():
    global isStop, velCam, CAM
    isStop = False
    velCam = CAM

def camRight():
    global isStop, velCam, CAM
    isStop = False
    velCam = -CAM

def camStop():
    global isStop, velCam, CAM
    isStop = True
    if servo.value <= -2*CAM:
        velCam = 2*CAM
    elif servo.value < 0:
        velCam = -servo.value
    elif servo.value >= 2*CAM:
        velCam = -2*CAM
    elif servo.value > 0:
        velCam = -servo.value
    else:
        velCam = 0

s = socket.socket()
host = '192.168.0.100'
port = 12345

while True:
    try:
        s.connect((host, port))
        break
    except:
        print("Failed, trying again")
        time.sleep(2)
        continue

s.settimeout(0.1)
while True:
    try:
        pp = s.recv(1024)
        data = pp.decode()
    except socket.timeout:
        data = 'pp'
    
    if data == 'forward':
        print('shamne ja')
        forward()
    if data == 'reverse':
        print('piche ja')
        reverse()
    if data == 'left':
        print('baame ja')
        left()
    if data == 'right':
        print('daane ja')
        right()
    if data == 'camlef':
        print('baam e dekh')
        camLeft()
    if data == 'camrig':
        print('daan e dekh')
        camRight()
    if data == 'stop':
        print('tham re baap')
        stop()
        camStop()
    if data == 'sup':
        if speed < 1:
            speed += 0.05
        print('jore chol - speed ' + str(speed))
    if data == 'sdown':
        if speed > 0:
            speed -= 0.05
        print('areh aste - speed ' + str(speed))
    
    if isStop:
        camStop()
        if velCam != 0:
            servo.value += velCam 
    else:
        if velCam > 0 and servo.value < 0.92:
            servo.value += velCam
        elif velCam < 0 and servo.value > -0.92:
            servo.value += velCam
    
s.close()

