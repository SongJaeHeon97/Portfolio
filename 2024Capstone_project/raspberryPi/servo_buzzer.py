import RPi.GPIO as GPIO
import time
import YB_Pcb_Car

car = YB_Pcb_Car.YB_Pcb_Car()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
p = GPIO.PWM(32, 1000)

def activate_buzzer():
    p.start(50) 
    print("Buzzer activated.")
    car.Ctrl_Servo(3, 0)
    print("Servo motor moved.")

def deactivate_buzzer():
    p.ChangeDutyCycle(0) 
    car.Ctrl_Servo(3, 90)
    print("Buzzer deactivated.")

def cleanup():
    p.stop()
    GPIO.cleanup()
