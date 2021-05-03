#%% 
from tetris import Tetris
import pygame
import random
from threading import Thread
from time import time
import random

VOLUME = 1#%
ROWS = 15
HEIGHT =900  # высота игрового окна
WIDTH = int((HEIGHT/(ROWS))*10)  # ширина игрового окна
TIME_FOR_FALL= 2#s
FPS = 60 # частота кадров в секунду
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

LEFT_BTN = 4
RIGHT_BTN = 3
BOTTOM_BTN = 2
ROATE_LEFT_BTN     = -1
ROATE_RIGHT_BTN     = 1
SCALE = int(WIDTH/10)

HEIGHT = SCALE * ROWS
sprites = {
	0:BLACK,
	1:(0,0,255),
	2:(0,255,0),
	3:(255,0,0),
	4:(0,255,255),
	5:(255,0,255),
	6:(255,255,0),
	7:(100,255,50),
 
	-1:(0,0,100),
	-2:(0,100,0),
	-3:(100,0,0),
	-4:(0,100,100),
	-5:(100,0,100),
	-6:(100,100,0),
	-7:(50,100,25)
 
 
}

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука

sounds = {
	1:pygame.mixer.Sound("spin.wav")

}
for i in sounds.keys():
	sounds[i].set_volume(VOLUME/100)


class Window:
	def __init__(self,tetris):
		self.tetris = tetris

		self.screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

		

		pygame.display.set_caption("Tetris")
		self.clock = pygame.time.Clock()
		self.running = True
		


	def draw(self):
		#print("\033[92m FPS \033[0m")
		self.screen.fill(WHITE)

		self.clock.tick(FPS) #держим фпс




		#event running
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_q: self.tetris.button = ROATE_LEFT_BTN
				if event.key == pygame.K_e: self.tetris.button = ROATE_RIGHT_BTN
				if event.key == pygame.K_a: self.tetris.button = LEFT_BTN
				if event.key in (pygame.K_s,pygame.K_j): self.tetris.button = BOTTOM_BTN
				if event.key == pygame.K_d: self.tetris.button = RIGHT_BTN



			if event.type == pygame.VIDEORESIZE:
				global HEIGHT
				global WIDTH
				global SCALE

				HEIGHT_ = self.screen.get_height()
				WIDTH_  = self.screen.get_width()
		
				HEIGHT = HEIGHT_
				WIDTH= int((HEIGHT/(ROWS))*10)  # ширина игрового окна
				SCALE = int(WIDTH/10)
				HEIGHT = SCALE* ROWS


				self.screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
			

		

		#музыкы

		sound = []
		i = True
		while i:
			i = self.tetris.sound
			sound.append(i)

		sound = sound[:-1:]


		for i in sound:
			if i in sounds.keys():
				sounds[i].play()
			
		#отрисовка

		main_array = self.tetris.main_array
		#print(main_array)

		for x in range(len(main_array)):
			for y in range(len(main_array[x])):
				self.drawRect(x,y, main_array[x][y])
				
		#убрать ненужные части
		
		pygame.display.flip()

	def drawRect(self,x,y,type):

		x = int(x*(SCALE))
		y = int((ROWS-(y+1))*(SCALE))

		#if type>0: type = random.randint(0,7)
		pygame.draw.rect(self.screen,sprites.get(type,BLACK),(
			x,
			y,

			SCALE,
			SCALE
		
			))


	def run(self):
		while self.running:
			self.draw()
		pygame.quit()

tetris = Tetris(ROWS,TIME_FOR_FALL*FPS)
app = Window(tetris)


app.run()

# %%
