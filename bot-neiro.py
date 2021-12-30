# %%
import pickle
import neat
import sys
import tetris
from tetris import Tetris
import pygame
import random
from threading import Thread
from time import time
from os.path import join
from threading import Thread
import argparse

tetris.GO_DOWN_SCORE = 0.1
tetris.SET_BRICK_SCORE = 1

parser = argparse.ArgumentParser()
parser.add_argument('-s','--state',action='store_true',help='generate/load checkpoints')

STATE = not parser.parse_args().state   # True- generate
# False - load neat


class Game:
	def __init__(self, idx, p, x, y, width, height, screen, display=True):
		self.moved = False
		self.die = False
		self.display = display
		self.tetris = Tetris(20, 2, 20)
		self.bot = Bot(self.tetris, p)
		self.x = x
		self.y = y
		self.width = width
		self.height = height * 0.95
		self.screen = screen
		self.self = self

		self.idx = idx

		self.SCALE = int(self.height/23)
		self.X_OFFSET_BRICKS = 2*self.SCALE
		self.Y_OFFSET_BRICKS = int(height * 0.05)
		self.font = pygame.font.SysFont(None, int(self.SCALE))
		

	def draw(self):

		# self.tetris.FPS = 20 #FPS if 0!=FPS else 60 	#little fix

		if not self.die:
			self.bot.run()
		self.tetris.run()
		if self.tetris.die:
			self.die = True

		if not self.display:
			return  # optimization

		# rip sound

		main_array = self.tetris.main_array
		# print(main_array)

		for x in range(len(main_array)):
			for y in range(len(main_array[x])):
				self.drawRect(x, y, main_array[x][y])

		# текст

		self.lines_breaked_text = self.font.render(
			f"IDX:{self.idx} LINES:{self.tetris.lines_breaked}", True, TEXT_COLOR)
		self.score_text = self.font.render(
			f"SCORE:{self.tetris.score}", True, TEXT_COLOR)

		self.screen.blit(self.score_text, (self.x+self.SCALE*2, self.y))
		self.screen.blit(self.lines_breaked_text,
						 (self.x+self.SCALE*7, self.y))

		# превью следуйщего блока
		for idx in range(len(self.tetris.next_pieces)):
			#print (self.tetris.next_pieces)
			spr = pygame.transform.scale(preview[self.tetris.next_pieces[idx]],
										 (
				{0: 0, 1: self.SCALE*1, 2: self.SCALE*2, 3: self.SCALE*2, 4: self.SCALE*2, 5: self.SCALE *
				 2, 6: self.SCALE*2, 7: self.SCALE*2}[self.tetris.next_pieces[idx]],
				{0: 0, 1: self.SCALE*4, 2: self.SCALE*3, 3: self.SCALE*3, 4: self.SCALE*3, 5: self.SCALE *
					 3, 6: self.SCALE*3, 7: self.SCALE*2}[self.tetris.next_pieces[idx]]
			))
			self.screen.blit(spr, (
				spr.get_rect(topleft=(
					self.x+self.SCALE * 10+self.X_OFFSET_BRICKS, self.y +
					self.Y_OFFSET_BRICKS + 4*self.SCALE*idx
				))
			))

		# превью взятого блока
		spr = pygame.transform.scale(preview[self.tetris.holded_piece],
									 (
			{0: 0, 1: self.SCALE*1, 2: self.SCALE*2, 3: self.SCALE*2, 4: self.SCALE*2, 5: self.SCALE *
			 2, 6: self.SCALE*2, 7: self.SCALE*2}[self.tetris.holded_piece],
			{0: 0, 1: self.SCALE*4, 2: self.SCALE*3, 3: self.SCALE*3, 4: self.SCALE*3,
				 5: self.SCALE*3, 6: self.SCALE*3, 7: self.SCALE*2}[self.tetris.holded_piece]
		))
		self.screen.blit(spr, (
			spr.get_rect(topleft=(
				self.x+self.SCALE * 5 + self.X_OFFSET_BRICKS, self.y +
				self.Y_OFFSET_BRICKS+self.SCALE*20
			))
		))

	def drawRect(self, x, y, type):

		x = int(x*(self.SCALE) + self.X_OFFSET_BRICKS) + self.x
		y = int((20-(y+1))*(self.SCALE) + self.Y_OFFSET_BRICKS) + self.y

		spr = pygame.transform.scale(sprites[type], (self.SCALE, self.SCALE))

		self.screen.blit(spr, (
			spr.get_rect(
				topleft=(x, y)
			)

		))

	def run(self):
		running = True
		while running:
			pygame.display.fill((255, 255, 255))
			for i in pygame.event.get():
				if i.type == pygame.QUIT:
					running = False
			self.draw()
			pygame.display.flip()



























class Bot:
	def __init__(self, tetris, net):
		self.net = net
		self.generation = 0
		self.__tetris = tetris

	def run(self):

		inputs = []
		for i in self.main:
			inputs.extend(i)
		inputs.extend([*self.next, self.holded,1])

		for i in range(len(inputs)):
			# -7 to 7 to -1 to 1
			inputs[i] = inputs[i]/7  # 7 = 1, 0 = 0, -7 = -1
			# -7 to 7 to 0 to 1
			# inputs[i] = (inputs[i]+7) /14# -7 = 0, 0 = 0.5, 7 = 1

		#inputs = np.array(inputs, dtype=np.float)  # numpy

		outputs = self.net.activate(inputs)
		
		
		# should be 206 inputs

		#outputs = 0,0,0,0,0,0
		#outputs = self.workout(inputs)
		# should be 6 outputs

		for i in range(len(outputs)):
			if outputs[i] > 0.5:
				self.button = -1 if i == 0 else i

	# all bot allowed to look

	@property
	def button(self): return
	@button.setter
	def button(self, value):	self.__tetris.button = value
	@property
	def next(self): return self.__tetris.next_pieces  # to preview next piece
	@property
	def holded(self): return self.__tetris.holded_piece  # to get holded piece
	@property
	def main(self): return self.__tetris.main_array  # to get main_array
	@property
	def score(self): return self.__tetris.score  # score


config_path = join("neiro", "config-feedforward.txt")
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
							neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
p = neat.Population(config)

checkpoints = neat.Checkpointer(1,60,join('.',"neiro", "checkpoints","checkpoint "))


if not STATE:
	p = neat.Checkpointer.restore_checkpoint(
		join("neiro", "checkpoints",input("Enter filename of checkpoint (neiro folder):\n")))


p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(checkpoints)

generation = 0
# %%

pygame.init()
pygame.mixer.init()  # для звука
pygame.font.init()

FPS = 10
TEXT_COLOR = (0, 0, 0)

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


width = 350
height = 2 * width
screen = pygame.display.set_mode(
	(int(5.2*width), int(height*1.1)), pygame.RESIZABLE)
clock = pygame.time.Clock()
MaxScore = 0

font = pygame.font.SysFont(None, int(40))

# %%


def run(genomes, config):
	global generation
	global MaxScore

	nets = []
	

	games = []
	index = 0
	for __idx__, g in genomes:

		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		g.fitness = 0
		games.append(Game(index, net, index*width, 40,
					 width, height, screen, index < 5))
		index += 1

	running = True


	MaxGenScore = 0
	length = len(genomes)
	screen_width = screen.get_width()
	screen_height = screen.get_height()

	while 1:
		screen.fill((255, 255, 255))

		clock.tick(FPS)
		for i in pygame.event.get():
			if i.type == pygame.QUIT:
				checkpoints.save_checkpoint(config, p, neat.DefaultSpeciesSet(config,stats), p.generation)

			if i.type == pygame.VIDEORESIZE:
				screen_width = screen.get_width()
				screen_height = screen.get_height()

		died = 0
		move_by = 0
		threds = []
		for idx, i in enumerate(games):


			genomes[idx][1].fitness = i.tetris.score
			if MaxScore < i.tetris.score:
				MaxScore = i.tetris.score
			if MaxGenScore < i.tetris.score:
				MaxGenScore = i.tetris.score
			i.x -= move_by * width
			i.display = not(i.x + 100 > screen_width or i.moved or i.y + 100 >screen_height)
			if i.die:
				died += 1
				if not i.moved:
					i.display = False
					i.moved = True
					move_by += 1

			threds.append(Thread(target=i.draw))
			threds[-1].start()


		if died == length:
			generation += 1
			break

		text = f"generation:{generation} alive:{length-died} FPS:{int(clock.get_fps())} max:{MaxScore} current max:{MaxGenScore}"
		pygame.display.set_caption(text)

		screen.blit(
			font.render(text, True, (10,0,255)),
			(10,0)

		)


		for i in threds:
			i.join()
			#0
		pygame.display.flip()

	


# %%
winner = p.run(run, 5000)
# %%
checkpoints.save_checkpoint(config, p,None, generation)	

win = p.best_genome
pickle.dump(winner, open(join('neiro','winner.pkl'), 'wb'))
pickle.dump(win, open(join('neiro','real_winner.pkl'), 'wb'))
pickle.dump(p, open(join('neiro','population.pkl'), 'wb'))

#%%

Game(win, 100, 0, width, height, screen).run()




# %%
pygame.display.quit()
# %%
