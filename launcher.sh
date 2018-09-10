#!/bin/sh
"""
	This scripts is executed automatically after the Raspberry Pi has booted. 
	It changes the mac address of the Pi, turns off the power saving features of the wifi chip
	and starts the right Python scripts.
"""

sudo ifconfig wlan0 down
sudo ifconfig wlan0 hw ether 00:11:22:33:44:13
sudo ifconfig wlan0 up
sudo iwconfig wlan0 power off
cd /
cd home/pi/scripts
sudo python oscServer3.py &
#If this is the bluetooth receiver, uncomment next line
#sudo python controller.py &
cd /

