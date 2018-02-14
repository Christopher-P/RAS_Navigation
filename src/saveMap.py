#!/usr/bin/env python

import os
import time

path = "/home/ras/catkin_ws/src/ras_navigation/Data/map.pbstream"

while True:
	time.sleep(30)
	print("Saving map to: " + path)
	os.system('rosservice call /write_state ' + path)
