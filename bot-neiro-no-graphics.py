# %%
import pickle

import neat
import sys
import tetris
from tetris import Tetris
from threading import Thread
from time import time
from os.path import join
from time import time
import argparse
tetris.GO_DOWN_SCORE = 0.1
tetris.SET_BRICK_SCORE = 1

CLEAR_LINE = "\x1b[2K"
parser = argparse.ArgumentParser()
parser.add_argument('-s','--state',action='store_true',help='generate/load checkpoints')

STATE = not parser.parse_args().state   # True- generate
# False - load neat


class Game:
	def __init__(self, p ):
		self.die = False
		self.tetris = Tetris(20, 2, 20)
		self.bot = Bot(self.tetris, p)


	def draw(self):
		if not self.die:
			self.bot.run()
		self.tetris.run()
		if self.tetris.die:
			self.die = True


























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
			if outputs[i] > 0.7:
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

FPS = 10


width = 350
height = 2 * width
MaxScore = 0


# %%


def run(genomes, config):
	
	global generation
	global MaxScore

	nets = []
	

	games = []
	for __idx__, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		g.fitness = 0
		games.append(Game(net))



	MaxGenScore = 0
	length = len(genomes)

	previus = time()
	fps = 0
	while 1:
		now = time()
		fps = 1/(now-previus)

		died = 0
		for idx, i in enumerate(games):
			genomes[idx][1].fitness = i.tetris.score
			if MaxScore < i.tetris.score:
				MaxScore = i.tetris.score
			if MaxGenScore < i.tetris.score:
				MaxGenScore = i.tetris.score
			if i.die:
				died += 1

			i.draw()

		if died == length:
			generation += 1
			break

		print(end=f"{CLEAR_LINE}\rgeneration:{generation} alive:{length-died} FPS:{int(fps)} max:{MaxScore} current max:{MaxGenScore}")


		previus = now
	
	print(CLEAR_LINE)
		



# %%
winner = p.run(run, 5000)
win = p.best_genome
pickle.dump(winner, open(join('neiro','winner.pkl'), 'wb'))
pickle.dump(win, open(join('neiro','real_winner.pkl'), 'wb'))







