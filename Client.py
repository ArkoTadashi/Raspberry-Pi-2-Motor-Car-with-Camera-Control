from gpiozero import Motor
import socket
import time

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = Servo(14, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

flmotor = Motor(forward=16, backward=17)
frmotor = Motor(forward=18, backward=13)
blmotor = Motor(forward=11, backward=12)
brmotor = Motor(forward=10, backward=9)

def left():
    flmotor.backward()
    frmotor.forward()
    blmotor.backward()
    brmotor.forward()

def right():
    flmotor.forward()
    frmotor.backward()
    blmotor.forward()
    brmotor.backward()


def forward():
    flmotor.forward()
    frmotor.forward()
    blmotor.forward()
    brmotor.forward()

def reverse():
    flmotor.backward()
    frmotor.backward()
    blmotor.backward()
    brmotor.backward()

def stop():
    flmotor.stop()
    frmotor.stop()
    blmotor.stop()
    brmotor.stop()

servo.value = 0.0
velCam = 0.0
isStop = True

def camLeft():
    if servo.value > -0.94:
        servo.value -= 0.05
        time.sleep(0.05)

def camRight():
    if servo.value < 0.94:
        servo.value += 0.05
        time.sleep(0.05)

def camStop():
    servo.value = 0

s = socket.socket()
host = '192.168.0.107'
port = 12345

while True:
    try:
        s.connect((host, port))
        break
    except:
        print("Failed, trying again")
        time.sleep(2)
        continue

while True:
    
    pp = s.recv(1024)
    data = pp.decode()
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
s.close()

