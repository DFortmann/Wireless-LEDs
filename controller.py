"""
	This Python script listens to key presses on a bluetooth remote with the evdev library.
	It retries to connect, if the remote is not found or got lost.
	When it receives a certain keypress, it sends an OSC message with the pyOSC library.
"""

from evdev import InputDevice, categorize, ecodes
from OSC import OSCClient, OSCMessage
import time
import sys
import os

client = OSCClient()
controller = None

def connectOSC():
	connected = False

	while not connected:
		try:
			client.connect( ("192.168.0.2", 7003) )
			connected = True
		except:
			time.sleep(0.5)
		
		
def connectController():
	global controller
	connected = False
	
	while not connected:
		try:
			#the bluetooth remote has to be the only input device connected, otherwise 'event0' could be wrong
			controller = InputDevice('/dev/input/event0')
			#Prevent the controller from writing to the command line
			controller.grab()
			connected = True 
		except:
			time.sleep(0.5)

def readController():
	try:
		for event in controller.read_loop():
			if event.type == ecodes.EV_KEY:
				if event.value == 0 or event.value == 1:
					if event.code == 105 or event.code == 165:
						client.send( OSCMessage("/controller/left", [float(event.value)] ) )
					elif event.code == 106 or event.code == 163:
						client.send( OSCMessage("/controller/right", [float(event.value)] ) )
					elif event.code == 103 or event.code == 115:
						client.send( OSCMessage("/controller/up", [float(event.value)] ) )
					elif event.code == 108 or event.code == 114:
						client.send( OSCMessage("/controller/down", [float(event.value)] ) )
					elif event.code == 28 or event.code == 164:
						client.send( OSCMessage("/controller/play", [float(event.value)] ) )
					elif event.code == 1 or event.code == 113:
						client.send( OSCMessage("/controller/mute", [float(event.value)] ) )
					elif event.code == 172:
						client.send( OSCMessage("/controller/record", [float(event.value)] ) )
				
	except KeyboardInterrupt: return
	except IOError: 
		connectController()
		readController()
	except: 
		print(sys.exc_info()[0])
		connectOSC()
		readController()
				
connectOSC()
connectController()
readController()