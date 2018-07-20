import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

def setup_sensor():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    print "Distance Measurement In Progress"

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print "Waiting for sensor to settle"
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

def get_location():

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print "Distance: ", distance, "cm"



if __name__ == '__main__':
    setup_sensor()
    try:
        while True:
            get_location()
    # Stop on Cmd+C and clean up
    except KeyboardInterrupt:
        GPIO.cleanup()
