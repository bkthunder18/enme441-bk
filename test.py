import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # try current code's assumption
while True:
    print("S1=", GPIO.input(5))
    time.sleep(0.3)
