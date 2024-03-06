
import signal
import sys
import RPi.GPIO as GPIO
import board
import neopixel

from datetime import datetime

#libraries to find IP address
#import socket
import netifaces as ni

FIRST_BTN_GPIO  = 14
FIRST_LED_GPIO  = 15
SECOND_BTN_GPIO = 23
SECOND_LED_GPIO = 24
THIRD_BTN_GPIO  = 25
THIRD_LED_GPIO  = 8

NEOPIX_GPIO = board.D18


WEBPAGE = '/var/www/html/index.html'

FIRST_RELEASED = "<!-- first released -->"
FIRST_NOTRELEASED = "<!-- first not released -->"
SECOND_RELEASED = "<!-- second released -->"
SECOND_NOTRELEASED = "<!-- second not released -->"
THIRD_RELEASED = "<!-- third released -->"
THIRD_NOTRELEASED = "<!-- third not released -->"

FIRST_RELEASED_TXT    = '<p><font size="20" face="arial" color="green"><em>Aircraft released</em></font></p>'
FIRST_NOTRELEASED_TXT = '<p><font size="3" face="arial" color="black"><em>No aircraft released</em></font></p>'
SECOND_RELEASED_TXT = "second released"
SECOND_NOTRELEASED_TXT = "no second released"
THIRD_RELEASED_TXT = "third released"
THIRD_NOTRELEASED_TXT = "no third released"

LOG_FILE = 'serverlog.txt'

def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)

def line_replace(key_txt, replace_txt):
	webpage = open(WEBPAGE,'r')
	webpage_text = webpage.readlines()
	webpage.close()
	webpage = open(WEBPAGE,'w')

	for line in webpage_text:
		if key_txt in line:
			line = replace_txt + "\n"
		webpage.writelines(line)
	webpage.close()


def first_button_pressed_callback(channel):
#	print("first button pressed!")
	webpage = open(WEBPAGE,'r')
	webpage_text = webpage.read()
	webpage.close()

	logfile = open(LOG_FILE, "a")

	ct = datetime.now().strftime("%m-%d %H:%M:%S.%f")
	if GPIO.input(FIRST_LED_GPIO): #if the aircraft has not yet been release, this action is releasing
		GPIO.output(FIRST_LED_GPIO, GPIO.LOW)
		logfile.write(ct + " - " + FIRST_NOTRELEASED + "\n")
		line_replace(FIRST_RELEASED,FIRST_NOTRELEASED + FIRST_NOTRELEASED_TXT)
	else:
		GPIO.output(FIRST_LED_GPIO, GPIO.HIGH)
		logfile.write(ct + " - " + FIRST_RELEASED + "\n")
		line_replace(FIRST_NOTRELEASED,FIRST_RELEASED + FIRST_RELEASED_TXT)

	logfile.close()

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(FIRST_BTN_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(FIRST_LED_GPIO, GPIO.OUT)

	GPIO.add_event_detect(FIRST_BTN_GPIO, GPIO.FALLING,
		callback=first_button_pressed_callback, bouncetime=500)

	#initialize the button low and the webpage
	GPIO.output(FIRST_LED_GPIO, GPIO.LOW)
	print("Init as", FIRST_NOTRELEASED)
	line_replace(FIRST_RELEASED,FIRST_NOTRELEASED + FIRST_NOTRELEASED_TXT)

# removed, wasn't working with crontab
#	ni.ifaddresses('wlan0')
#	ip = ni.ifaddresses('wlan0')[2][0]['addr']
#	print(ip)
#	line_replace("<!-- ip address -->","<!-- ip address --><p>" + ip + "</p>")

	signal.signal(signal.SIGINT, signal_handler)
	signal.pause()
