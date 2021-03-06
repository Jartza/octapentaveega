import serial
import time
import random
import sys

# Give port name of your UART as first argument. No error checking
# here, sorry.
#
ser = serial.Serial(sys.argv[1], 9600,  timeout = 1)

serwrite = lambda x: ser.write(bytearray(map(ord, x)))
move_to = lambda x, y: serwrite("\x1B[{0};{1}H".format(y, x))

serwrite("xxxxx") # dismiss if we're left in ANSI mode...
serwrite("\x1Bc") # Reset
time.sleep(2)
serwrite("\x1B[16]") # Graphics mode
serwrite("\x1B[?7l") # disable wrap
serwrite("\x1BG") # Tricoder mode

image=[
#red
[
"......    ...     ..   ..      .. .  ....   ....    ...     ....",
".......    ...    ..         ... ..   ....  ....    ...    .... ",
"   .....    ..    ..    .      . .  . .   . ...    ...    ....  ",
"     ....   ...   ..    .      . ..  ..   .....    ...    ...   ",
"...   ....   ..   ...   .  ..    .............    ...    ...    ",
".....  ....  ...   ..   ......   ..... .......   ....   ...     ",
"......  ...   ..   ..   ......   .   .     ...   ...    ...   . ",
"      .  ...  ..   ..   .....          .   ..    ...   ...  ....",
"       .  ...  ..  ..   ......  ..  .  .   ..   ...   ...  ..   ",
"          ...  ..  ..   .....          .  ...   ...   ..   .    ",
"           ...  .   ..  .......        .  ..   ...   ..         ",
".......     ..  ..  ..  ... .   .     ......   ...   ..  .      ",
"........    ... ..  ......      .     ....... ...   ..  .       ",
".........    ..  ..........    ..     ...........   .. .  ......",
" .. ......   ....................    ............. ..  .  ......",
"             ....................   . ...............   ....    ",
"             ........  ...........    ............... .  .      ",
"             .........................................          ",
"             .........................................          ",
"............  .....      .............        ...............   ",
".............  ...   ..     ........    ....   .................",
"...........    .. .........   .....  .  ....... ..... ....      ",
"               . .................. .  ......... ....           ",
"               ................. ... .  ......... ...   .       ",
"           ..   .................................. .......      ",
".............. .....      ...........       ...... ...... ......",
"..................  .    . .........       . ............ ......",
".......... ....     .    .   .......  .   ..    ......... ..... ",
"          ..... ...         .......         ...... .. ...       ",
"          ... ........    ............................ ...      ",
"           ............................................ ..      ",
"           .....................................................",
"................................................................",
".......... ..............................................       ",
"            ............................................        ",
"            ... ..................................... ..        ",
"            . ................. ........................        ",
"...............................  .................. .... ...  . ",
"............... ............   ..   .............. . .. .....   ",
"             .   ............... .................              ",
"                 ............... .................              ",
"                 .................................              ",
"                 ..................................             ",
"..............    ...........   ...........................   . ",
"............       ..........    ................ ..........    ",
"                   .......... . ................                ",
"                    .......................... .                ",
"                   ............    ........... .                ",
"                    ............  ............ .                ",
"                     ...........  ...........  ............  .  ",
" ..........           .........   ........... ..............  . ",
"  ..  ....             ............................             ",
"                        ......................                  ",
"                       .  ......   ...........                  ",
"                       ....         ..........                  ",
"                       .......................                  ",
".................      ......      . .........  ......... ...   ",
"      .............    .....           .......  ..... . .. ..   ",
"                     . .....  .    ..  .......  .               ",
"                     . .....        .  ..........               ",
"...................... .....        .  ............. ...   .    ",
" ..................  . .....           ...................      ",
"                     .  ....        .  ..........               ",
"                     .  ....        .. ...... ...               "
],
#green
[
"......     ..     .     .      .      ...      .      .      .  ",
" ......    ...    .                   .               .     .   ",
"    ....    ..    .     .                     .      .     .    ",
"      ...   ..    ..    .                   .       ..    ..    ",
"       ...   ..    .    .               . ....    ...    ..     ",
" ..     ..    .    ..   .  ..              . .    ..     ..     ",
"        ...   ..   ..   .. ..              .     ...    ..      ",
"         ...   .   ..   ..  .                    ...   ...      ",
"          ..   .    .    . ..                   ...    .        ",
"           ..  ..   .    . .                    ..    ..        ",
"           ..   .   .    .. .                   ..    .         ",
"  . ..      ..  .   ..                ..  ..   ..    ..         ",
" ......     ..   .  ..  .             .......  ..    .          ",
"  .......    ..  . .......            ...........   .      ..  .",
"       .     .............     ..     ...........   .       .   ",
"             ........                     ........ ..    ..     ",
"              ......     .    ...      .   . .......            ",
"              ......     ..  .......................            ",
"             ........   .................... .........          ",
"..     ....     ...        ...........        .... ... .        ",
"          ..    ..           .......           ...  . ......  . ",
"               .   . ...      ....       ......  .. . .         ",
"               . .........  .   ..      .......  ....           ",
"                 .... ..... ..   ...      ......  ..    .       ",
"           ..   ..... ... .  .. ..     .. .....    .... ..      ",
"    .  .. ....  ....      .. .....          ....   ...    .     ",
" ......... ... ...           .... .           ....  . ... ..... ",
" ........  ....     .    .   ......        .     .  .....       ",
"           .. . ...          ...  .          ....  .. ...       ",
"           .  ........    . ....  ....   ............  ..       ",
"           .  .......      ....... ...    ............          ",
"           . ...........   ... ...      . ............ ......   ",
".......... .............   ... ....  .    ...........   ....... ",
"           .. ........... ....... ..     ..............         ",
"            ... ......... ...... .... . .......... ..  .        ",
"            ... .................................  .. ..        ",
"            . . ..............  ................. . . ..        ",
"    ....... ... .......... ..      ..............   ...         ",
"........... ..  ..........          .............  . .          ",
"                 ..........  ..  .......... .... .              ",
"                 .........  ...  ......... ..... .              ",
"                 ......... ............... ....                 ",
"                  ............ .......... ....                  ",
"    ......        ..........      ....... .... ..               ",
"      ....         .........      ....... ...  ..               ",
"                    ....  .      .....   ...   .                ",
"                    ... .....    ....... ..    .                ",
"                    ..........     ........                     ",
"                     .......         ... .  .                   ",
"                      .......       ....  ...  ....     ..      ",
"   .                   .......     .....  ..  ...      ..       ",
"                       ........   ...... ..  .                  ",
"                        .... ..    .... ..  ..                  ",
"                          ..         .........                  ",
"                                      .. .....                  ",
"                         .  .      .....  ....                  ",
" ..............        . ..           . ..  .                   ",
"                       ....             .. ..   ..              ",
"                        ...         .  .... ..                  ",
"                         ..         .   .   .                   ",
" ................  ..  ....         .   .  .. ...               ",
"                         ..            .. ...  ... ...          ",
"                         ..         .  ..  ..  ..               ",
"                         ..         .. ..   .  .                "
],
#blue
[
"                          .                                     ",
"                          .                                     ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                 .                 .            ",
"                                 .                              ",
"                                 .                              ",
"                                                                ",
"                                                                ",
"                                                 .              ",
"         .                                       .              ",
"                              .    .            ..      ..      ",
"                              .......         .       .         ",
"                              ....             .                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                           ....                 ",
"                                           ..                   ",
"                                      ......                    ",
"                                      .....                     ",
"                                       ...                      ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                                                                ",
"                             .     .  .                         ",
"                              ..   ....                         ",
"                                   ...                          ",
"                               .  .....                         ",
"                            ..    .....                         ",
"                                  .....                         ",
"                                  .....                         "
]
]

nums = [ "  ", " .", ". ", ".." ]

for row in range(16):
	for char in range(32):
		red = 0
		green = 0
		blue = 0
		for index in range (row * 4, row * 4 + 4):
			red <<= 2
			green <<= 2
			blue <<= 2
			red |= nums.index(image[0][index][(char * 2):(char * 2) + 2][:2])
			green |= nums.index(image[1][index][(char * 2):(char * 2) + 2][:2])
			blue |= nums.index(image[2][index][(char * 2):(char * 2) + 2][:2])
		if red in [8,10,13,27,127]:
			serwrite(chr(27) + chr(red))
		else:
			serwrite(chr(red))
		if green in [8,10,13,27,127]:
			serwrite(chr(27) + chr(green))
		else:
			serwrite(chr(green))
		if blue in [8,10,13,27,127]:
			serwrite(chr(27) + chr(blue))
		else:
			serwrite(chr(blue))
	if row < 15:
		serwrite(chr(13))

ser.flush()
# time.sleep(2)

# delay = 0.6
# delay2 = 0.03

# for i in range(8):
# 	for x in range(17):
# 		serwrite("\x1B[{0}]".format(x))
# 		ser.flush()
# 		time.sleep(delay2)
# 	time.sleep(delay)
# 	for x in range(16,-1,-1):
# 		serwrite("\x1B[{0}]".format(x))
# 		ser.flush()
# 		time.sleep(delay2)
# 	time.sleep(delay)
# 	delay -= .07
# 	delay2 -= .003

# for x in range(17):
# 	serwrite("\x1B[{0}]".format(x))
# 	ser.flush()
# 	time.sleep(delay2)


ser.close()
