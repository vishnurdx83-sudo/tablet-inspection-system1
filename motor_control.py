import RPi.GPIO as GPIO
import time

# -------- SENSORS (ACTIVE LOW) --------
SENSOR1 = 18   # start sensor (once)
SENSOR2 = 23   # stop 5 sec
SENSOR3 = 24   # stop 5 sec
SENSOR4 = 25   # RESET sensor (full stop)

# -------- L298N --------
IN1 = 17
IN2 = 27
ENA = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(SENSOR1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# -------- INITIAL STATE --------
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(ENA, GPIO.HIGH)   # ENABLE DRIVER

motor_on = False

def motor_start():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

try:
    while True:

        # 🔹 SENSOR 4 → FULL STOP + RESET
        if GPIO.input(SENSOR4) == GPIO.LOW:
            motor_stop()
            motor_on = False
            print("Sensor4 → MOTOR STOP & RESET")

            # debounce
            time.sleep(0.5)
            continue   # skip remaining logic

        # 🔹 SENSOR 1 → START MOTOR (ONCE, AFTER RESET ALSO)
        if GPIO.input(SENSOR1) == GPIO.LOW and not motor_on:
            motor_start()
            motor_on = True
            print("Sensor1 → Motor continuous RUN")

        # 🔹 SENSOR 2 OR SENSOR 3 → STOP 5 SEC
        if motor_on and (GPIO.input(SENSOR2) == GPIO.LOW or GPIO.input(SENSOR3) == GPIO.LOW):
            print("Sensor2 / Sensor3 → Motor STOP 5 sec")

            motor_stop()
            time.sleep(5)

            motor_start()
            print("5 sec over → Motor RUN again")

            time.sleep(0.5)  # debounce

        # 🔒 FORCE LATCH
        if motor_on:
            motor_start()

        time.sleep(0.1)

except KeyboardInterrupt:
    motor_stop()
    GPIO.cleanup()
