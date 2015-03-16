#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

import urllib2
import json
import pprint

temp_f = ''
humidity = ''
 
API_KEY='ENTER YOUR KEY HERE' # Obtain a free API key from weatherunderground.com

pp = pprint.PrettyPrinter(indent=4)

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


lcd = Adafruit_CharLCD()

cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

lcd.begin(16, 1)


def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

while 1:
	lcd.home();
	get_weather()
	ipaddr = run_cmd(cmd)
	lcd.message(datetime.now().strftime('%b %d  %I:%M %p\n'))
#	lcd.message("IP: %s" % ipaddr.strip())
	temp = str(temp_f) + unichr(223) + "F"
	lcd.message("%s Hum: %s" % (temp, humidity))
	sleep(15)
