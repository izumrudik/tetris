#%% 
from tetris import Tetris
import pygame
import random
from threading import Thread
from time import time
import random
from os.path import join
VOLUME = 1#%
ROWS = 15
HEIGHT =800  # высота игрового окна
WIDTH = int((HEIGHT/(ROWS))*10)# ширина игрового окна
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

X_OFFSET_BRICKS = 0
Y_OFFSET_BRICKS = 40

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
pygame.font.init()



sprites = {
	0:pygame.image.load(join("resources","blocks","0.png")),
	1:pygame.image.load(join("resources","blocks","1.png")),
	2:pygame.image.load(join("resources","blocks","2.png")),
	3:pygame.image.load(join("resources","blocks","3.png")),
	4:pygame.image.load(join("resources","blocks","4.png")),
	5:pygame.image.load(join("resources","blocks","5.png")),
	6:pygame.image.load(join("resources","blocks","6.png")),
	7:pygame.image.load(join("resources","blocks","7.png")),

	-1:pygame.image.load(join("resources","blocks","-1.png")),
	-2:pygame.image.load(join("resources","blocks","-2.png")),
	-3:pygame.image.load(join("resources","blocks","-3.png")),
	-4:pygame.image.load(join("resources","blocks","-4.png")),
	-5:pygame.image.load(join("resources","blocks","-5.png")),
	-6:pygame.image.load(join("resources","blocks","-6.png")),
	-7:pygame.image.load(join("resources","blocks","-7.png"))
 
}


sounds = {
	1:pygame.mixer.Sound(join("resources","spin.wav"))

}
for i in sounds.keys():
	sounds[i].set_volume(VOLUME/100)


class Window:
	def __init__(self,tetris):
		self.tetris = tetris

		self.screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

		self.basic_font = pygame.font.SysFont(None, 24)

		pygame.display.set_caption("Tetris")
		self.clock = pygame.time.Clock()
		self.running = True
		self.resize()


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
				if event.key == pygame.K_s: self.tetris.button = BOTTOM_BTN
				if event.key == pygame.K_d: self.tetris.button = RIGHT_BTN



			if event.type == pygame.VIDEORESIZE:
				self.resize()


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
		self.lines_breaked_text = self.basic_font.render(f"LINES:{self.tetris.lines_breaked}", True, BLUE)
		self.score_text = self.basic_font.render(f"SCORE:{self.tetris.score}", True, BLUE)
		self.screen.blit(self.score_text, (20, 5))
		self.screen.blit(self.lines_breaked_text, (20, 25))
		
		pygame.display.flip()

	def drawRect(self,x,y,type):

		x = int(x*(SCALE) + X_OFFSET_BRICKS)
		y = int((ROWS-(y+1))*(SCALE) + Y_OFFSET_BRICKS)


		spr = pygame.transform.scale(sprites[type],(SCALE,SCALE))

		self.screen.blit(spr, (
			spr.get_rect(
				topleft=(x,y)
			)

		))


	def run(self):
		while self.running:
			self.draw()
		pygame.quit()

	def resize(self):
		global HEIGHT
		global WIDTH
		global SCALE

		HEIGHT_ = self.screen.get_height()
		WIDTH_  = self.screen.get_width()
		
		HEIGHT = HEIGHT_
		WIDTH= int((HEIGHT/(ROWS))*10)  # ширина игрового окна
		SCALE = int(WIDTH/10)
		HEIGHT = int(SCALE * ROWS)


		self.screen = pygame.display.set_mode((WIDTH+X_OFFSET_BRICKS, HEIGHT+Y_OFFSET_BRICKS),pygame.RESIZABLE)
			

		

tetris = Tetris(ROWS,TIME_FOR_FALL*FPS)
app = Window(tetris)


app.run()

# %%
