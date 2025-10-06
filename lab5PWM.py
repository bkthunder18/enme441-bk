'''
Bryan Kennedy
ENME441
Lab 5 - PWM & Threaded Callbacks

'''

import RPi.GPIO as gpio
import time
import numpy as np

def brightness(t, f, phase):
    return (np.sin(2 * np.pi * f * t - phase)) ** 2

gpio.setmode(gpio.BCM)

leds = [17, 27, 22, 23, 24, 25, 5, 6, 12, 13]

pwms = []
for i in leds:
    gpio.setup(i, gpio.OUT)
    pwm = gpio.PWM(i, 500)
    pwm.start(0)
    pwms.append(pwm)

button_pin = 26
gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_DOWN)

f = 0.2
phaseShift = np.pi/9 #changed from 11 to 9 since we have a 10 led bar, not a 12 led bar
sign = 1 # (+) or (-) depending on desired direction, flips on button press

def changeSign(channel):
    global sign 
    sign *= -1
    
gpio.add_event_detect(button_pin, gpio.RISING, callback=changeSign, bouncetime=300)

try:
    while True:
        t = time.time()
        for i, pwm in enumerate(pwms):
            phase = sign * phaseShift * i
            B = brightness(t, f, phase)
            pwm.ChangeDutyCycle(B * 100)
        
except KeyboardInterrupt:
    pass
finally:
    try:
        gpio.remove_event_detect(button_pin)
    except Exception:
        pass
    for p in pwms:
        p.stop()
    gpio.cleanup()
