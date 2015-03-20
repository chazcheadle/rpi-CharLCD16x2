#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

import urllib2
import json

lcd = Adafruit_CharLCD()
lcd.begin(16, 2)

cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

humidity = ''
temp_f = ''
API_KEY='' # Obtain a free API key from weatherunderground.com

def get_weather():
	global data
	global temp_f
	global humidity
	f = urllib2.urlopen('http://api.wunderground.com/api/' + API_KEY + '/geolookup/conditions/q/NY/Garrison.json')
	json_string = f.read()
	parsed_json = json.loads(json_string)
	result = parsed_json['current_observation']
	temp_f = int(result['temp_f'])
	humidity = result['relative_humidity']
	f.close()
	return

def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

while 1:
#	lcd.home()
	if datetime.now().second % 2:
		lcd.setCursor(0,0)
		lcd.message(datetime.now().strftime('%b %d %I %M %p\n'))
	else:
		lcd.setCursor(0,0)
		lcd.message(datetime.now().strftime('%b %d %I:%M %p\n'))
	if (datetime.now().minute % 5 == 0) and (datetime.now().second == 0):
		lcd.setCursor(0,1)
		get_weather()
		temp = str(temp_f) + unichr(223) + "F"
		lcd.message("%s Hum: %s" % (temp, humidity))
	sleep(1)
