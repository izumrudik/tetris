#%%
import numpy as np, neat,sys
from tetris import Tetris
import pygame,random
from threading import Thread
from time import time
from os.path import join



class Game:
	def __init__(self,p,x,y,width,height,screen):
		self.die = False

		self.tetris = Tetris(20,2,20)
		self.bot = Bot(self.tetris,p) 
		self.x = x
		self.y = y
		self.width = width
		self.height = height * 0.95
		self.screen = screen
		self.self = self



		self.SCALE = int(self.height/23)
		self.X_OFFSET_BRICKS = 2*self.SCALE
		self.Y_OFFSET_BRICKS = int(height * 0.05)


	
	def draw(self):

		#self.tetris.FPS = 20 #FPS if 0!=FPS else 60 	#little fix

		if not self.die:self.bot.run()
		self.tetris.run()
		if self.tetris.die:
			self.die = True



		#rip sound		


		main_array = self.tetris.main_array
		# print(main_array)

		for x in range(len(main_array)):
			for y in range(len(main_array[x])):
				self.drawRect(x, y, main_array[x][y])

		# текст
		font = pygame.font.SysFont(None, int(self.SCALE))

		self.lines_breaked_text = font.render(
			f"LINES:{self.tetris.lines_breaked}", True, TEXT_COLOR)
		self.score_text = font.render(f"SCORE:{self.tetris.score}", True, TEXT_COLOR)

		self.screen.blit(self.score_text, (self.x+self.SCALE*2, self.y))
		self.screen.blit(self.lines_breaked_text, (self.x+self.SCALE*8, self.y))

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
					self.x+self.SCALE * 10+self.X_OFFSET_BRICKS, self.y+self.Y_OFFSET_BRICKS + 4*self.SCALE*idx
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
				self.x+self.SCALE * 5 + self.X_OFFSET_BRICKS, self.y+self.Y_OFFSET_BRICKS+self.SCALE*20
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

















class Bot:
	def __init__(self,tetris,net):
		self.net = net
		self.generation = 0
		self.__tetris = tetris




	def run(self):


		inputs = []
		for i in self.main:inputs.extend(i)
		inputs.extend([*self.next,self.holded])


		
		for i in range(len(inputs)):
			#-7 to 7 to -1 to 1
			inputs[i] = inputs[i]/7 #7 = 1, 0 = 0, -7 = -1
			# -7 to 7 to 0 to 1
			#inputs[i] = (inputs[i]+7) /14# -7 = 0, 0 = 0.5, 7 = 1


		inputs = np.array(inputs,dtype=np.float)#numpy



		outputs = self.net.activate(inputs)




		self.net.fitness = self.score
		# should be 206 inputs


		#outputs = 0,0,0,0,0,0
		#outputs = self.workout(inputs)
		# should be 6 outputs




		for i in range(len(outputs)):
			if outputs[i] > 0:
				self.button = -1 if i == 0 else i




	





	#all bot allowed to look
	@property 
	def button(self):return
	@button.setter
	def button(self,value):	self.__tetris.button = value
	@property
	def next(self):return self.__tetris.next_pieces#to preview next piece
	@property
	def holded(self):return self.__tetris.holded_piece#to get holded piece
	@property
	def main(self):return self.__tetris.main_array#to get main_array
	@property
	def score(self):return self.__tetris.score#score





config_path = join("neiro","config-feedforward.txt")
config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
p = neat.Population(config)


p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)





generation = 0
#%%

pygame.init()
pygame.mixer.init()  # для звука
pygame.font.init()

FPS = 20
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
screen = pygame.display.set_mode((int(5.2*width),int(height*1.1)),pygame.RESIZABLE)
clock = pygame.time.Clock()
MaxScore = 0
#%%
def run(genomes,config):
	global generation
	global MaxScore

	nets = []

	games = []
	index = 0
	for idx, g in genomes:
		
		net = neat.nn.FeedForwardNetwork.create(g,config)
		nets.append(net)
		g.fitness = 0
		games.append(Game(net,index*width,0,width,height,screen) )
		index += 1







	running = True

	font = pygame.font.SysFont(None, 40)



	
	MaxGenScore = 0

	while 1:
		screen.fill((255, 255, 255))
		
		clock.tick(FPS) 



		for i in pygame.event.get():
			if i.type == pygame.QUIT:
				pygame.display.quit()

		died = 0
		for idx,i in enumerate(games):
			if MaxScore < i.tetris.score: MaxScore = i.tetris.score
			if MaxGenScore < i.tetris.score: MaxGenScore = i.tetris.score
			died+=1 if i.die else 0
			i.draw()


		if died==5:
			generation+=1
			break



		text = font.render(f"generation:{generation} alive:{5-died} FPS:{int(clock.get_fps())} max:{MaxScore} current max:{MaxGenScore}",True, (10,0,255))

		screen.blit(text,(width*1.5,height*1.05))

		pygame.display.flip()

	
#%%
p.run(run,n=1000000)

# %%
pygame.display.quit()
# %%
