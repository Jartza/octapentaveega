#
#   Quick'n'Dirty Font Creator & Reorganizer for Attiny85 VGA.
# 
#   Copyright 2015-2016 Jari Tulilahti
#   
#   All right and deserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import sys
import functools

try:
	f = open("vgafont.dat", "r")
	data = f.readlines()
	f.close()

	fontdata = []
	font = [0] * 256 * 10

	for line in data:
		line = str().join(map(lambda x: x if x in "0123456789=.x" else "", line))
		if len(line) > 2:
			fontdata.append(line)

	index = 32 * 10

	for line in fontdata:
		if line.endswith("="):
			try:
				index = int(line.strip("=")) * 10
			except:
				index = 0
		elif len(line) == 6:
			value = functools.reduce(lambda k, x: (k << 1) + x, [x != '.' for x in line], 0)
			font[index] = value << 2
			index += 1

	for i in range(32, 160):
		for h in range(10):
			x = (i * 10) + h
			z = (((i + 128) & 255) * 10) + h
			font[z] = font[x] ^ 252


	f = open("font.inc", "w")

	f.write( ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;   32 x 16 character VGA output with UART for Attiny85.                      ;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;   Copyright 2015-2016 Jari Tulilahti                                        ;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;   All right and deserved                                                    ;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;   Licensed under the Apache License, Version 2.0 (the \"License\");           ;;\n")
	f.write( ";;   you may not use this file except in compliance with the License.          ;;\n")
	f.write( ";;   You may obtain a copy of the License at                                   ;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;       http://www.apache.org/licenses/LICENSE-2.0                            ;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;   Unless required by applicable law or agreed to in writing, software       ;;\n")
	f.write( ";;   distributed under the License is distributed on an \"AS IS\" BASIS,         ;;\n")
	f.write( ";;   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  ;;\n")
	f.write( ";;   See the License for the specific language governing permissions and       ;;\n")
	f.write( ";;   limitations under the License.                                            ;;\n")
	f.write( ";;                                                                             ;;\n")
	f.write( ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n")
	f.write("\n")
	f.write( "; Automatically generated file. DO NOT EDIT!\n")
	f.write("\n")
	f.write( ".cseg\n")
	f.write( ".org 0xB00\n")
	f.write("\n")
	f.write( "font:\n")
	f.write( "\t.db ")

	cnt = 0

	for i in range(10):
		for h in range(256):
			fontline = font[(h * 10) + i]
			f.write("0x{0:02x}".format(fontline))
			cnt += 1
			if cnt == 8:
				if [h, i] == [255, 9]:
					f.write("\n")
				else:
					f.write("\n\t.db ")
					cnt = 0
			else:
				f.write(", ")

	f.write("\n")
	f.close()

except:
	print("Cannot create font. Exiting.")
	sys.exit(1)
