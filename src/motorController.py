import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class MotorController:
    def __init__(self) -> None:
        self.isOpen = False
        self.PIN = 11
        GPIO.setup(self.PIN, GPIO.OUT)
        self.servo = GPIO.PWM(self.PIN, 50)
        self.servo.start(0)
        self.servo.ChangeDutyCycle(6.5)  # initial locked position
        time.sleep(0.5)
        self.servo.ChangeDutyCycle(0)  # stop PWM to reduce jitter
        self.flush = lambda: GPIO.cleanup()

    def open(self):
        self.isOpen = True
        self.servo.ChangeDutyCycle(2)  # open position
        time.sleep(0.5)
        self.servo.ChangeDutyCycle(0)  # stop PWM

    def close(self):
        self.isOpen = False
        self.servo.ChangeDutyCycle(6.5)  # locked position
        time.sleep(0.5)
        self.servo.ChangeDutyCycle(0)  # stop PWM
