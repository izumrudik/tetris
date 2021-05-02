from tetris import Tetris
from threading import Thread
from time import time
from colored import fg, bg, attr
import sys
import os

from pynput import keyboard

FPS = 24
ROWS = 15
TIME_FOR_LOOP = 1/FPS

TIME_FOR_FALL = 2#s

sprites = {
	0:"#000000",
	1:"#0000FF",
	2:"#00FF00",
	3:"#FF0000",
	4:"#00FFFF",
	5:"#FF00FF",
	6:"#FFFF00",
	7:"#64FF32",
 
	-1:"#000064",
	-2:"#006400",
	-3:"#640000",
	-4:"#006464",
	-5:"#640064",
	-6:"#646400",
	-7:"#326419"
 
 
}


tetris = Tetris(ROWS,TIME_FOR_FALL*FPS)


def loop():

	global tetris
	main_array = tetris.main_array
	arr = [[ "" for x in range(10) ] for y in range(ROWS)]
	for x in range(len(main_array)):
		for y in range(len(main_array[x])):
			arr[ROWS-y-1][x] = fg(sprites.get(main_array[x][y],"#000000"))+"▢ "
	buff = ""
	for y in arr:
		for x in y:
			buff+=x + attr("reset")
		buff+="\n"

	os.system('cls' ) #clear if bash or something
	
	sys.stdout.write(buff)

	#sys.stdout.flush()

STOP = False

def loop_start():
	start = 0
	
	while True:
		
		if start + TIME_FOR_LOOP <= time():
			start = time()
			#print(int(time()))
			Thread(target=loop).start()
		if STOP: return



loop_thread= Thread(target=loop_start)
loop_thread.start()
#button annotation:
# -1-rotate-left
# 1-rotate-right
# 2-bottom
# 3-right
# 4-left

try:
	def press(key):
		global tetris
		#print(key)
		key = str(key)
		#print(key)
		#print("n" in key)

		if 	 r"a" in key: tetris.button = 4
		if 	 r"s" in key: tetris.button = 2
		if 	 r"d" in key: tetris.button = 3
		if 	 r"q" in key: tetris.button = -1
		if 	 r"e" in key: tetris.button = 1

		if r'\x03' in key:
			# Stop listener
			return False


	with keyboard.Listener(
	
		on_release=press) as listener:
		listener.join()

except:
	import traceback
	traceback.print_exc()
	STOP = True
	sys.exit()

