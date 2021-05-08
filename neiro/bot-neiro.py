import numpy as np, neat
from tetris import Tetris
import pygame,random
from threading import Thread
from time import time
from os.path import join



VOLUME=1
ROWS=20
HEIGHT=800
WIDTH=int(HEIGHT/ROWS*10)
TIME_FOR_FALL=2
FPS=60
BLACK=0,0,0
WHITE=255,255,255
RED=255,0,0
GREEN=0,255,0
BLUE=0,0,255
LEFT_BTN=4
RIGHT_BTN=3
BOTTOM_BTN=2
ROTATE_LEFT_BTN=-1
ROTATE_RIGHT_BTN=1
HOLD_BTN=5
SCALE=int(WIDTH/10)
HEIGHT=SCALE*ROWS
X_OFFSET_BRICKS=0
Y_OFFSET_BRICKS=40

pygame.init()
pygame.mixer.init()
pygame.font.init()

#this is minifyed VVVVVVVVVVVV
_K='7.png';_J='6.png';_I='5.png';_H='4.png';_G='3.png';_F='2.png';_E='1.png';_D=True;_C='preview';_B='blocks';_A='resources'
sprites={0:pygame.image.load(join(_A,_B,'0.png')),1:pygame.image.load(join(_A,_B,_E)),2:pygame.image.load(join(_A,_B,_F)),3:pygame.image.load(join(_A,_B,_G)),4:pygame.image.load(join(_A,_B,_H)),5:pygame.image.load(join(_A,_B,_I)),6:pygame.image.load(join(_A,_B,_J)),7:pygame.image.load(join(_A,_B,_K)),-1:pygame.image.load(join(_A,_B,'-1.png')),-2:pygame.image.load(join(_A,_B,'-2.png')),-3:pygame.image.load(join(_A,_B,'-3.png')),-4:pygame.image.load(join(_A,_B,'-4.png')),-5:pygame.image.load(join(_A,_B,'-5.png')),-6:pygame.image.load(join(_A,_B,'-6.png')),-7:pygame.image.load(join(_A,_B,'-7.png'))}
preview={0:pygame.image.load(join(_A,'none.png')),1:pygame.image.load(join(_A,_C,_E)),2:pygame.image.load(join(_A,_C,_F)),3:pygame.image.load(join(_A,_C,_G)),4:pygame.image.load(join(_A,_C,_H)),5:pygame.image.load(join(_A,_C,_I)),6:pygame.image.load(join(_A,_C,_J)),7:pygame.image.load(join(_A,_C,_K))}
sounds={1:pygame.mixer.Sound(join(_A,'spin.wav'))}
for i in sounds.keys():sounds[i].set_volume(VOLUME/100)
class Window:
	def __init__(A,tetris,bot):A.bt = bot;A.tetris=tetris;A.screen=pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE);pygame.display.set_caption('Tetris');A.clock=pygame.time.Clock();A.running=_D;A.resize()
	def draw(A):
		A.tetris.run()
		if A.tetris.die:A.tetris = A.tetris.__init__(ROWS,TIME_FOR_FALL*FPS)
		A.screen.fill(WHITE);A.clock.tick(FPS)
		for B in pygame.event.get():
			if B.type==pygame.QUIT:A.running=False
			if B.type==pygame.VIDEORESIZE:A.resize()
		E=[];C=_D
		while C:C=A.tetris.sound;E.append(C)
		E=E[:-1]
		for C in E:
			if C in sounds.keys():sounds[C].play()
		G=A.tetris.main_array
		for H in range(len(G)):
			for I in range(len(G[H])):A.drawRect(H,I,G[H][I])
		J=pygame.font.SysFont(None,int(SCALE/2));A.lines_breaked_text=J.render(f"LINES:{A.tetris.lines_breaked}",_D,BLUE);A.score_text=J.render(f"SCORE:{A.tetris.score}",_D,BLUE);A.screen.blit(A.score_text,(SCALE*5,0));A.screen.blit(A.lines_breaked_text,(SCALE*5,SCALE*0.4))
		for F in range(len(A.tetris.next_pieces)):D=pygame.transform.scale(preview[A.tetris.next_pieces[F]],({0:0,1:SCALE*1,2:SCALE*2,3:SCALE*2,4:SCALE*2,5:SCALE*2,6:SCALE*2,7:SCALE*2}[A.tetris.next_pieces[F]],{0:0,1:SCALE*4,2:SCALE*3,3:SCALE*3,4:SCALE*3,5:SCALE*3,6:SCALE*3,7:SCALE*2}[A.tetris.next_pieces[F]]));A.screen.blit(D,D.get_rect(topleft=(SCALE*10+X_OFFSET_BRICKS,Y_OFFSET_BRICKS+4*SCALE*F)))
		D=pygame.transform.scale(preview[A.tetris.holded_piece],({0:0,1:SCALE*1,2:SCALE*2,3:SCALE*2,4:SCALE*2,5:SCALE*2,6:SCALE*2,7:SCALE*2}[A.tetris.holded_piece],{0:0,1:SCALE*4,2:SCALE*3,3:SCALE*3,4:SCALE*3,5:SCALE*3,6:SCALE*3,7:SCALE*2}[A.tetris.holded_piece]));A.screen.blit(D,D.get_rect(topleft=(SCALE*-2+X_OFFSET_BRICKS,Y_OFFSET_BRICKS)));pygame.display.flip()
	def drawRect(B,x,y,type):x=int(x*SCALE+X_OFFSET_BRICKS);y=int((ROWS-(y+1))*SCALE+Y_OFFSET_BRICKS);A=pygame.transform.scale(sprites[type],(SCALE,SCALE));B.screen.blit(A,A.get_rect(topleft=(x,y)))
	def run(A):
		while A.running:A.bt.run();A.draw()
		pygame.quit()
	def resize(A):global HEIGHT;global WIDTH;global SCALE;global X_OFFSET_BRICKS;global Y_OFFSET_BRICKS;B=A.screen.get_height();C=A.screen.get_width();HEIGHT=B*0.95;WIDTH=int(HEIGHT/ROWS*10);SCALE=int(WIDTH/10);HEIGHT=int(SCALE*ROWS);X_OFFSET_BRICKS=2*SCALE;Y_OFFSET_BRICKS=int(B*0.05);A.screen=pygame.display.set_mode((WIDTH+X_OFFSET_BRICKS+2*SCALE,HEIGHT+Y_OFFSET_BRICKS),pygame.RESIZABLE)

#class window is minifyed ^^^^^^^




















class Bot:
	def __init__(self,tetris):
		self.__tetris = tetris




	def run(self):
		array = []
		for i in self.main:
			for j in i:
				array.append(j)
		array.extend([*self.next,self.holded])

		#print(array)
		
		inputs = np.array(array,dtype=np.int)

	





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






tetris=Tetris(ROWS,TIME_FOR_FALL*FPS)
bot = Bot(tetris)
app=Window(tetris,bot)




app.run()
