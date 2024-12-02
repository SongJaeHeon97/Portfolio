import threading
import socket
import time
import CV
import linetracer
import servo_buzzer

buzzer_active = False
last_detected_time = time.time()

def socket_listener():
    global buzzer_active, last_detected_time

    host = "192.168.168.146"
    port = 8001
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("Main server started and waiting for messages...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode("utf-8")

        if message == "FL_detected":
            last_detected_time = time.time()
            if not buzzer_active:
                buzzer_active = True
                servo_buzzer.activate_buzzer()
                linetracer.stop_car()
                print("FL_detected: Buzzer ON and Car STOP")

def check_for_resume():
    global buzzer_active
    while True:
        if buzzer_active and (time.time() - last_detected_time > 3):
            buzzer_active = False
            servo_buzzer.deactivate_buzzer()
            linetracer.resume_tracking()
            print("No FL_detected signal: Buzzer OFF and Car RESUME")
        time.sleep(1)

def main():
    cv_thread = threading.Thread(target=CV.run_CV)
    cv_thread.start()

    linetracer_thread = threading.Thread(target=linetracer.run_car)
    linetracer_thread.start()

    socket_thread = threading.Thread(target=socket_listener)
    resume_thread = threading.Thread(target=check_for_resume)

    socket_thread.start()
    resume_thread.start()

    try:
        cv_thread.join()
        linetracer_thread.join()
        socket_thread.join()
        resume_thread.join()
    except KeyboardInterrupt:
        print("Ctrl+C detected. Stopping all threads.")
    finally:
        print("All threads stopped.")

if __name__ == "__main__":
    main()
