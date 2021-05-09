from tetris import Tetris
import pygame
import random
from threading import Thread
from time import time
import random
from os.path import join
VOLUME = 1  # %
ROWS = 20
HEIGHT = 800  # высота игрового окна
WIDTH = int((HEIGHT/(ROWS))*10)  # ширина игрового окна
TIME_FOR_FALL = 2  # s
FPS = 60  # частота кадров в секунду
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

LEFT_BTN = 4
RIGHT_BTN = 3
BOTTOM_BTN = 2
ROTATE_LEFT_BTN = -1
ROTATE_RIGHT_BTN = 1
HOLD_BTN = 5
SCALE = int(WIDTH/10)

HEIGHT = SCALE * ROWS

X_OFFSET_BRICKS = 0
Y_OFFSET_BRICKS = 40

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
pygame.font.init()


sprites = {
	0: pygame.image.load(join("resources", "blocks", "0.png")),
	1: pygame.image.load(join("resources", "blocks", "1.png")),
	2: pygame.image.load(join("resources", "blocks", "2.png")),
	3: pygame.image.load(join("resources", "blocks", "3.png")),
	4: pygame.image.load(join("resources", "blocks", "4.png")),
	5: pygame.image.load(join("resources", "blocks", "5.png")),
	6: pygame.image.load(join("resources", "blocks", "6.png")),
	7: pygame.image.load(join("resources", "blocks", "7.png")),

	-1: pygame.image.load(join("resources", "blocks", "-1.png")),
	-2: pygame.image.load(join("resources", "blocks", "-2.png")),
	-3: pygame.image.load(join("resources", "blocks", "-3.png")),
	-4: pygame.image.load(join("resources", "blocks", "-4.png")),
	-5: pygame.image.load(join("resources", "blocks", "-5.png")),
	-6: pygame.image.load(join("resources", "blocks", "-6.png")),
	-7: pygame.image.load(join("resources", "blocks", "-7.png"))

}


preview = {
	0: pygame.image.load(join("resources", "none.png")),
	1: pygame.image.load(join("resources", "preview", "1.png")),
	2: pygame.image.load(join("resources", "preview", "2.png")),
	3: pygame.image.load(join("resources", "preview", "3.png")),
	4: pygame.image.load(join("resources", "preview", "4.png")),
	5: pygame.image.load(join("resources", "preview", "5.png")),
	6: pygame.image.load(join("resources", "preview", "6.png")),
	7: pygame.image.load(join("resources", "preview", "7.png"))
}


sounds = {
	1: pygame.mixer.Sound(join("resources", "spin.wav"))

}
for i in sounds.keys():
	sounds[i].set_volume(VOLUME/100)


class Window:
	def __init__(self, tetris):
		self.tetris = tetris

		self.screen = pygame.display.set_mode(
			(WIDTH, HEIGHT), pygame.RESIZABLE)

		pygame.display.set_caption("Tetris")
		self.clock = pygame.time.Clock()
		self.running = True
		self.resize()

	def draw(self):
		if self.tetris.die:
			self.tetris = self.tetris.__init__(ROWS, FPS,TIME_FOR_FALL)
		
		#print("\033[92m FPS \033[0m")
		self.screen.fill(WHITE)

		self.clock.tick(FPS)  # держим фпс
		self.tetris.FPS = self.clock.get_fps() if self.clock.get_fps()!=0 else FPS
		self.tetris.run()  # run

		# event running
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_q:
					self.tetris.button = ROTATE_LEFT_BTN
				if event.key == pygame.K_e:
					self.tetris.button = ROTATE_RIGHT_BTN
				if event.key == pygame.K_a:
					self.tetris.button = LEFT_BTN
				if event.key == pygame.K_s:
					self.tetris.button = BOTTOM_BTN
				if event.key == pygame.K_d:
					self.tetris.button = RIGHT_BTN
				if event.key == pygame.K_c:
					self.tetris.button = HOLD_BTN

			if event.type == pygame.VIDEORESIZE:
				self.resize()

		# музыкы

		sound = []
		i = True
		while i:
			i = self.tetris.sound
			sound.append(i)

		sound = sound[:-1:]

		for i in sound:
			if i in sounds.keys():
				sounds[i].play()

		# отрисовка

		main_array = self.tetris.main_array
		# print(main_array)

		for x in range(len(main_array)):
			for y in range(len(main_array[x])):
				self.drawRect(x, y, main_array[x][y])

		# текст
		font = pygame.font.SysFont(None, int(SCALE/2))

		self.lines_breaked_text = font.render(
			f"LINES:{self.tetris.lines_breaked}", True, BLUE)
		self.score_text = font.render(f"SCORE:{self.tetris.score}", True, BLUE)

		self.screen.blit(self.score_text, (SCALE*5, 0))
		self.screen.blit(self.lines_breaked_text, (SCALE*5, SCALE*0.4))

		# превью следуйщего блока
		for idx in range(len(self.tetris.next_pieces)):
			#print (self.tetris.next_pieces)
			spr = pygame.transform.scale(preview[self.tetris.next_pieces[idx]],
										 (
				{0: 0, 1: SCALE*1, 2: SCALE*2, 3: SCALE*2, 4: SCALE*2, 5: SCALE *
					2, 6: SCALE*2, 7: SCALE*2}[self.tetris.next_pieces[idx]],
				{0: 0, 1: SCALE*4, 2: SCALE*3, 3: SCALE*3, 4: SCALE*3, 5: SCALE *
					3, 6: SCALE*3, 7: SCALE*2}[self.tetris.next_pieces[idx]]
			))
			self.screen.blit(spr, (
				spr.get_rect(topleft=(
					SCALE * 10+X_OFFSET_BRICKS, Y_OFFSET_BRICKS + 4*SCALE*idx
				))
			))

		# превью взятого блока
		spr = pygame.transform.scale(preview[self.tetris.holded_piece],
									 (
			{0: 0, 1: SCALE*1, 2: SCALE*2, 3: SCALE*2, 4: SCALE*2, 5: SCALE *
				2, 6: SCALE*2, 7: SCALE*2}[self.tetris.holded_piece],
			{0: 0, 1: SCALE*4, 2: SCALE*3, 3: SCALE*3, 4: SCALE*3,
					5: SCALE*3, 6: SCALE*3, 7: SCALE*2}[self.tetris.holded_piece]
		))
		self.screen.blit(spr, (
			spr.get_rect(topleft=(
				SCALE * -2 + X_OFFSET_BRICKS, Y_OFFSET_BRICKS
			))
		))

		pygame.display.flip()

	def drawRect(self, x, y, type):

		x = int(x*(SCALE) + X_OFFSET_BRICKS)
		y = int((ROWS-(y+1))*(SCALE) + Y_OFFSET_BRICKS)

		spr = pygame.transform.scale(sprites[type], (SCALE, SCALE))

		self.screen.blit(spr, (
			spr.get_rect(
				topleft=(x, y)
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
		global X_OFFSET_BRICKS
		global Y_OFFSET_BRICKS
		HEIGHT_ = self.screen.get_height()
		WIDTH_ = self.screen.get_width()

		HEIGHT = HEIGHT_ * 0.95
		WIDTH = int((HEIGHT/(ROWS))*10)  # ширина игрового окна
		SCALE = int(WIDTH/10)
		HEIGHT = int(SCALE * ROWS)

		X_OFFSET_BRICKS = 2*SCALE
		Y_OFFSET_BRICKS = int(HEIGHT_ * 0.05)

		self.screen = pygame.display.set_mode(
			(WIDTH+X_OFFSET_BRICKS+2*SCALE, HEIGHT+Y_OFFSET_BRICKS), pygame.RESIZABLE)


def run():
	tetris = Tetris(ROWS,FPS, TIME_FOR_FALL)
	app = Window(tetris)
	app.run()


if __name__ == "__main__":
	run()
