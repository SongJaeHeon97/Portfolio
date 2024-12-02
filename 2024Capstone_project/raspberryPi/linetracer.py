import RPi.GPIO as GPIO
import time
import YB_Pcb_Car   

car = YB_Pcb_Car.YB_Pcb_Car()

Tracking_Right1 = 11   
Tracking_Right2 = 7    
Tracking_Left1 = 13    
Tracking_Left2 = 15    

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(Tracking_Left1, GPIO.IN)
GPIO.setup(Tracking_Left2, GPIO.IN)
GPIO.setup(Tracking_Right1, GPIO.IN)
GPIO.setup(Tracking_Right2, GPIO.IN)

tracking_active = True

def stop_car():
    global tracking_active
    tracking_active = False
    print("Car stopped by stop_car()")

def resume_tracking():
    global tracking_active
    tracking_active = True 
    print("Resuming car tracking by resume_tracking()")

def tracking_function():
    while True:
        if not tracking_active:
            car.Car_Stop()
            time.sleep(0.3)
            continue

        Tracking_Left1Value = GPIO.input(Tracking_Left1)
        Tracking_Left2Value = GPIO.input(Tracking_Left2)
        Tracking_Right1Value = GPIO.input(Tracking_Right1)
        Tracking_Right2Value = GPIO.input(Tracking_Right2)

        
        # 1 0 0 0
        if Tracking_Left1Value == True and Tracking_Left2Value == False and Tracking_Right1Value == False and Tracking_Right2Value == False:
            car.Car_Spin_Right(95, 100)
            time.sleep(0.05) 
        #1 0 1 0
        elif Tracking_Left1Value == True and Tracking_Left2Value == False and Tracking_Right1Value == True and Tracking_Right2Value == False:
            car.Car_Spin_Right(95, 100)
            time.sleep(0.05)
        #1 1 0 1
        elif Tracking_Left1Value == True and Tracking_Left2Value == True and Tracking_Right1Value == False and Tracking_Right2Value == True:
            car.Car_Spin_Right(95, 100)
            time.sleep(0.05)
        #1 1 0 0
        elif Tracking_Left1Value == True and Tracking_Left2Value == True and Tracking_Right1Value == False and Tracking_Right2Value == False:
            car.Car_Spin_Right(95, 100)
            time.sleep(0.05)
        #1 1 1 0
        elif Tracking_Left1Value == True and Tracking_Left2Value == True and Tracking_Right1Value == True and Tracking_Right2Value == False:
            car.Car_Spin_Right(95, 100)
            time.sleep(0.05)
        #0 0 0 1
        elif Tracking_Left1Value == False and Tracking_Left2Value == False and Tracking_Right1Value == False and Tracking_Right2Value == True:
            car.Car_Spin_Left(100, 95) 
            time.sleep(0.05)
        #0 1 0 1
        elif Tracking_Left1Value == False and Tracking_Left2Value == True and Tracking_Right1Value == False and Tracking_Right2Value == True:
            car.Car_Spin_Left(100, 95) 
            time.sleep(0.05)
        #1 0 1 1
        elif Tracking_Left1Value == True and Tracking_Left2Value == False and Tracking_Right1Value == True and Tracking_Right2Value == True:
            car.Car_Spin_Left(100, 95) 
            time.sleep(0.05)
        #0 0 1 1
        elif Tracking_Left1Value == False and Tracking_Left2Value == False and Tracking_Right1Value == True and Tracking_Right2Value == True:
            car.Car_Spin_Left(100, 95) 
            time.sleep(0.05)
        #0 1 1 1
        elif Tracking_Left1Value == False and Tracking_Left2Value == True and Tracking_Right1Value == True and Tracking_Right2Value == True:
            car.Car_Spin_Left(100, 95) 
            time.sleep(0.05)
        #1 0 0 1
        elif Tracking_Left2Value == False and Tracking_Right1Value == False:
            car.Car_Run(60, 60) 


def run_car():
    try:
        tracking_function() 
    except KeyboardInterrupt:
        pass
    finally:
        car.Car_Stop()
        GPIO.cleanup()

if __name__ == "__main__":
    run_car()
