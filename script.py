import RPi.GPIO as GPIO
import time
import signal
import sys
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 23
pinEcho = 24
occupied = True

def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, close)

def setup_sensor():
    # set GPIO input and output channels
    GPIO.setup(pinTrigger, GPIO.OUT)
    GPIO.setup(pinEcho, GPIO.IN)

def get_distance():
	# set Trigger to HIGH
	GPIO.output(pinTrigger, True)
	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(pinTrigger, False)

	startTime = time.time()
	stopTime = time.time()

	# save start time
	while 0 == GPIO.input(pinEcho):
		startTime = time.time()

	# save time of arrival
	while 1 == GPIO.input(pinEcho):
		stopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = stopTime - startTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2

	return distance

if __name__ == '__main__':
    pnconfig = PNConfiguration()
    pnconfig.publish_key = 'pub-c-559f5d98-9a8a-42e0-8a38-dfe760065056'
    pubnub = PubNub(pnconfig)

    setup_sensor()
    while True:
        if (occupied and (get_distance() >= 5)) or (not occupied and (get_distance() < 5)):
			print('ENTERS IF')
			try:
				occupied = not occupied
            	pubnub.publish().channel("parking_spot").message({
                    'occupied': occupied
                }).sync()
				print("Success publishing")
			except PubNubException as e:
				print("Error publishing")
        time.sleep(5)
