import RPi.GPIO as GPIO
import time
import signal
import sys


# SMS related
lastSms = time.time()	# initialise with current time

from SMS import SMS
sms = SMS("<domain_api_key>", "<domain_secret>", "<user_id>")

def send_SMS(distance):
	if ((time.time() - lastSms) > 300):
		sent = sms.send("<source_phone_number>", "<destination_phone_number>", "Distance: %.1f cm" % distance)
		if (sent == True):
			print ("SMS sent")
		else:
			print ("SMS not sent")
		lastSms = time.time()


# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 18
pinEcho = 24

def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

while True:
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

	print ("Distance: %.1f cm" % distance)

	send_SMS(distance)

time.sleep(1)
