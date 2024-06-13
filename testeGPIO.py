import time
import RPi.GPIO as GPIO

pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)

time.sleep(3)

GPIO.output(pin, GPIO.LOW)

time.sleep(3)

GPIO.output(pin, GPIO.HIGH)

time.sleep(3)

GPIO.output(pin, GPIO.LOW)
