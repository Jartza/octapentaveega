#################################################################################
##                                                                             ##
##   Very simple ANSI-tester Python application for Attiny85 VGA               ##
##                                                                             ##
##                                                                             ##
##   Copyright 2015 Jari Tulilahti                                             ##
##                                                                             ##
##   Licensed under the Apache License, Version 2.0 (the "License")#           ##
##   you may not use this file except in compliance with the License.          ##
##   You may obtain a copy of the License at                                   ##
##                                                                             ##
##       http://www.apache.org/licenses/LICENSE-2.0                            ##
##                                                                             ##
##   Unless required by applicable law or agreed to in writing, software       ##
##   distributed under the License is distributed on an "AS IS" BASIS,         ##
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  ##
##   See the License for the specific language governing permissions and       ##
##   limitations under the License.                                            ##
##                                                                             ##
#################################################################################

import serial
import time
import random

# Change port name to correspond with your UART
#
ser = serial.Serial('/dev/cu.usbserial', 9600)

serwrite = lambda x: ser.write(bytearray(map(ord, x)))
move_to = lambda x, y: serwrite("\x1B[{0};{1}H".format(y, x))
set_color = lambda fg, bg = 0: serwrite("\x1B[3{0};4{1}m".format(fg, bg))

def rndclear(c = 32):
	serwrite("\x1B[m") # Reset colors
	for loc in random.sample(xrange(448), 448):
		move_to(int(loc / 14), loc % 14)
		serwrite(chr(c))
	serwrite("\x1B[H") # Move cursor to 0,0

directions = [
	# Worm travelling North
	{ "x" :  0, "y" : -1, "dirs" : 
		[
			{ "char" : 138, "nextdir" : 0 }, # Straight
			{ "char" : 151, "nextdir" : 1 }, # Left
			{ "char" : 137, "nextdir" : 3 }  # Right
		] 
	},
	# Worm travelling West
	{ "x" : -1, "y" :  0, "dirs" : 
		[
			{ "char" : 133, "nextdir" : 1 }, # Straight
			{ "char" : 137, "nextdir" : 2 }, # Left
			{ "char" : 136, "nextdir" : 0 }  # Right
		]
	},
	# Worm travelling South
	{ "x" :  0, "y" :  1, "dirs" : 
		[
			{ "char" : 138, "nextdir" : 2 }, # Straight
			{ "char" : 136, "nextdir" : 3 }, # Left
			{ "char" : 135, "nextdir" : 1 }  # Right
		] 
	},
	# Worm travelling East
	{ "x" :  1, "y" :  0, "dirs" : 
		[
			{ "char" : 133, "nextdir" : 3 }, # Straight
			{ "char" : 135, "nextdir" : 0 }, # Left
			{ "char" : 151, "nextdir" : 2 }  # Right
		]
	},
]

worms = [
	{ "x" : 16, "y" :  0, "dir" : 2, "color" : 1},
	{ "x" : 16, "y" : 13, "dir" : 0, "color" : 2},
	{ "x" : 12, "y" : 10, "dir" : 2, "color" : 3},
	{ "x" : 16, "y" :  7, "dir" : 1, "color" : 4},
	{ "x" : 31, "y" :  7, "dir" : 1, "color" : 5},
	{ "x" : 22, "y" :  4, "dir" : 3, "color" : 6},
	{ "x" :  0, "y" :  7, "dir" : 3, "color" : 7},
]

serwrite("x\x08") # dismiss if we're left in ANSI mode...
serwrite("\x1B[2J") # Clear screen
serwrite("\x1B[=7l") # Disable wrap

# Draw color bars
x = 0
d = 1
c = 0
for zz in range(800):
	set_color(int(c), int(c - 0.5))
	move_to(x, 13)
	serwrite("\x96\x96\x96\x96\x96\x96\x96\x96\n")
	x += d
	c += .25
	if int(c) == 8:
		c = 1
	if x in [0, 24]:
		d = -d

rndclear()

# Draw some worms in the screen
for z in xrange(300):
	for worm in worms:
		move = directions[worm["dir"]]
		worm["x"] = (worm["x"] + move["x"]) % 32
		worm["y"] = (worm["y"] + move["y"]) % 14
		turn = [0, 0, 0, 1, 2][random.randint(0, 4)]
		move_to(worm["x"], worm["y"])
		set_color(worm["color"])
		serwrite(chr(move["dirs"][turn]["char"]))
		worm["dir"] = move["dirs"][turn]["nextdir"]

rndclear(160)
rndclear(32)

# Rakettitiede go-around
for i in [150, 149, 146, 149, 150, 160]:
	a = chr(i)
	x = random.randint(3, 16)
	y = random.randint(3, 10)
	serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
	move_to(x,y)
	serwrite("Rakettitiede")

	for i in range(32):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(i, 0)
		serwrite(a)

	for i in range(0,14):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(31, i)
		serwrite(a)

	for i in range(31,-1,-1):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(i, 13)
		serwrite(a)

	for i in range(13,-1,-1):
		serwrite("\x1B[3{0}m".format(random.randint(1, 7)))
		move_to(0, i)
		serwrite(a)

	move_to(x,y)
	serwrite("            ")

rndclear(160)

# Random color characters
for zz in range(20):
	for i in range(65,91):
		move_to(random.randint(0, 31), random.randint(0, 13))
		(f, b) = random.sample(range(8), 2)
		set_color(f, b)
		serwrite(chr(i))

rndclear()
# Show color map
serwrite("Attiny85 VGA, displaying 32x14\n")
serwrite("characters on screen with 6x8 px\n")
serwrite("font. Single attiny for B&W text\n")
serwrite("or three attinys for 8 colors!\n")
serwrite("      (C) 2015 // Jartza\n")

move_to(0, 5)
set_color(0, 7)

serwrite("  bg :   0  1  2  3  4  5  6  7 \n")

for x in range(8):
	move_to(2, x + 6)
	set_color(7, 0)
	serwrite("fg {0}".format(x))
	for i in range(8):
		move_to(8 + (i * 3), x + 6)
		set_color(x, i)	
		serwrite("xY")	

ser.flush()
ser.close()