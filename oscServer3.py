"""
	This scripts receives OSC messages via the pyOSC library 
	and controls APA102 LEDs with the Adafruit DotStar library.
	It is used for displaying video or test data on LED stripes.
"""

import os
import OSC
import time
from subprocess import call
from dotstar import Adafruit_DotStar

""" Setup DotStar strip for use in manual mode"""
strip = Adafruit_DotStar()
strip.begin()
strip.setBrightness(0)
	
""" 
Load three different txt files that contain the video data.
It is saved as hex arrays, one line per frame.
"""
with open("/home/pi/frames/frames1.txt", "rb") as fp:
	fone = fp.readlines()
	
foneNumFrames = sum(1 for _ in fone) - 1
foneIndex = -1

with open("/home/pi/frames/frames2.txt", "rb") as fp:
	ftwo = fp.readlines()
	
ftwoNumFrames = sum(1 for _ in ftwo) - 1
ftwoIndex = -1

with open("/home/pi/frames/frames3.txt", "rb") as fp:
	fthree	= fp.readlines()
	
fthreeNumFrames = sum(1 for _ in fthree) - 1
fthreeIndex = -1


""" Load the videos for test mode and blinking """
with open("/home/pi/frames/rgbColors.txt", "rb") as fp:
	testFrames = fp.readlines()
	
with open("/home/pi/frames/testmode.txt", "rb") as fp:
	testmode = fp.readlines()
	
	activeTest = -1

	
""" 
	These functions are executed, when a 'timecode' is received.
	The range is remapped from 0-1 to 0-number of frames.
	When the frame number wasn't received before, the corresponding line is read from the file.
	This line is then handed to the show function of the DotStar library as a byte array.
"""
def recFoneIndex(addr, tags, data, client_address):
	global foneIndex
	global fone	
	global foneNumFrames
	
	index = int(data[0] * foneNumFrames)

	if index != foneIndex:	
		foneIndex = index
		f = fone[index].rstrip()
		strip.show(bytearray.fromhex(f))
	return
	
def recFtwoIndex(addr, tags, data, client_address):
	global ftwoIndex
	global ftwo	
	global ftwoNumFrames
	
	index = int(data[0] * ftwoNumFrames)

	if index != ftwoIndex:	
		ftwoIndex = index
		f = ftwo[index].rstrip()
		strip.show(bytearray.fromhex(f))
	return
	
def recFthreeIndex(addr, tags, data, client_address):
	global fthreeIndex
	global fthree
	global fthreeNumFrames
	
	index = int(data[0] * fthreeNumFrames)

	if index != fthreeIndex:	
		fthreeIndex = index
		f = fthree[index].rstrip()
		strip.show(bytearray.fromhex(f))
	return
	
def recTestmode(addr, tags, data, client_address):
	global activeTest
	global testmode
	
	indexIn = int(data[0] * 499)
	
	if indexIn != activeTest:
		activeTest = indexIn
		fr = testmode[indexIn].rstrip()
		strip.show(bytearray.fromhex(fr))	
	return

"""
	This function makes the LED blink any number of times.
	Colors are: 0=Black, 1=100% Red, 2=100% Green, 3=100% Blue
				4=50% Red, 5=50% Green, 6=50% Blue
"""
def Blink(color, count):	
	global testFrames
	for i in range(count):
		f = testFrames[color].rstrip()
		strip.show(bytearray.fromhex(f))
		time.sleep(0.2)
		f = testFrames[0].rstrip()
		strip.show(bytearray.fromhex(f))
		time.sleep(0.2)
	return
	
		
"""
	This test functions cycles through all LEDs 
	to make sure the mapping is right.
"""
def recStripTest(addr, tags, data, client_address):
	with open("/home/pi/frames/rgbTest.txt", "rb") as fp:
		pixs = fp.readlines()
		
	for i in range(1500):
		f = pixs[i].rstrip()
		strip.show(bytearray.fromhex(f))
		time.sleep(0.02)
		
	Blink(0,1)
	return
				
def recConnectTest(addr, tags, data, client_address):
	Blink(7,3)
	return
	
def recBlack(addr, tags, data, client_address):
	Blink(0,1)
	return
	
def recExit(addr, tags, data, client_address):
	Blink(0,1)
	s.close()
	return
	
def recShutdown(addr, tags, data, client_address):
	Blink(5,3)
	s.close()
	call("sudo shutdown -h now", shell=True)
	return
		
def recReboot(addr, tags, data, client_address):
	Blink(0,1)
	call("sudo reboot", shell=True)
	return
	
def recCpu(addr, tags, data, client_address):
	print(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
	return 
	
def recRam(addr, tags, data, client_address):
	call("free -h", shell=True)
	return

def recSampleRate(addr, tags, stuff, source):
    pass
		

s = OSC.OSCServer(("",7000))

s.addDefaultHandlers()
s.addMsgHandler('default', recSampleRate) #handels all not handled OSC messages
s.addMsgHandler('/_samplerate', recSampleRate)
s.addMsgHandler('/leds/fone', recFoneIndex)
s.addMsgHandler('/leds/ftwo', recFtwoIndex)
s.addMsgHandler('/leds/fthree', recFthreeIndex)
s.addMsgHandler('leds/striptest', recStripTest)
s.addMsgHandler('/leds/connecttest', recConnectTest)
s.addMsgHandler('/leds/black', recBlack)
s.addMsgHandler('/leds/exit', recExit)
s.addMsgHandler('/leds/reboot', recReboot)
s.addMsgHandler('/leds/shutdown', recShutdown)
s.addMsgHandler('/leds/ram', recRam)
s.addMsgHandler('/leds/cpu', recCpu)
s.addMsgHandler('/leds/testmode',recTestmode)

Blink(6,3)

s.serve_forever()	