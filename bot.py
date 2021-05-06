_L=False;_K='7.png';_J='6.png';_I='5.png';_H='4.png';_G='3.png';_F='2.png';_E='1.png';_D=True;_C='preview';_B='blocks';_A='resources';from tetris import Tetris;import pygame,random;from threading import Thread;from time import time;from os.path import join;VOLUME=1;ROWS=15;HEIGHT=800;WIDTH=int(HEIGHT/ROWS*10);TIME_FOR_FALL=2;FPS=60;BLACK=0,0,0;WHITE=255,255,255;RED=255,0,0;GREEN=0,255,0;BLUE=0,0,255;LEFT_BTN=4;RIGHT_BTN=3;BOTTOM_BTN=2;ROATE_LEFT_BTN=-1;ROATE_RIGHT_BTN=1;HOLD_BTN=5;SCALE=int(WIDTH/10);HEIGHT=SCALE*ROWS;X_OFFSET_BRICKS=0;Y_OFFSET_BRICKS=40;pygame.init();pygame.mixer.init();pygame.font.init();sprites={0:pygame.image.load(join(_A,_B,'0.png')),1:pygame.image.load(join(_A,_B,_E)),2:pygame.image.load(join(_A,_B,_F)),3:pygame.image.load(join(_A,_B,_G)),4:pygame.image.load(join(_A,_B,_H)),5:pygame.image.load(join(_A,_B,_I)),6:pygame.image.load(join(_A,_B,_J)),7:pygame.image.load(join(_A,_B,_K)),-1:pygame.image.load(join(_A,_B,'-1.png')),-2:pygame.image.load(join(_A,_B,'-2.png')),-3:pygame.image.load(join(_A,_B,'-3.png')),-4:pygame.image.load(join(_A,_B,'-4.png')),-5:pygame.image.load(join(_A,_B,'-5.png')),-6:pygame.image.load(join(_A,_B,'-6.png')),-7:pygame.image.load(join(_A,_B,'-7.png'))};preview={0:pygame.image.load(join(_A,'none.png')),1:pygame.image.load(join(_A,_C,_E)),2:pygame.image.load(join(_A,_C,_F)),3:pygame.image.load(join(_A,_C,_G)),4:pygame.image.load(join(_A,_C,_H)),5:pygame.image.load(join(_A,_C,_I)),6:pygame.image.load(join(_A,_C,_J)),7:pygame.image.load(join(_A,_C,_K))};sounds={1:pygame.mixer.Sound(join(_A,'spin.wav'))}
for i in sounds.keys():sounds[i].set_volume(VOLUME/100)
#minified
class Window:#minified
	def __init__(self,tetris,bot):self.bot=bot;self.tetris=tetris;self.screen=pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE);pygame.display.set_caption('Tetris');self.clock=pygame.time.Clock();self.running=_D;self.resize()
	def draw(self):#minified
		self.screen.fill(WHITE);self.clock.tick(FPS);self.bot.run()#minified
		for event in pygame.event.get():#minified
			if event.type==pygame.QUIT:self.running=_L#minified
			if event.type==pygame.VIDEORESIZE:self.resize()#minified
		sound=[];i=_D#minified
		while i:i=self.tetris.sound;sound.append(i)#minified
		sound=sound[:-1]#minified
		for i in sound:#minified
			if i in sounds.keys():sounds[i].play()#minified
		main_array=self.tetris.main_array#minified
		for x in range(len(main_array)):#minified
			for y in range(len(main_array[x])):self.drawRect(x,y,main_array[x][y])#minified
		font=pygame.font.SysFont(None,int(SCALE/2));self.lines_breaked_text=font.render(f"LINES:{self.tetris.lines_breaked}",_D,BLUE);self.score_text=font.render(f"SCORE:{self.tetris.score}",_D,BLUE);self.screen.blit(self.score_text,(SCALE*5,0));self.screen.blit(self.lines_breaked_text,(SCALE*5,SCALE*0.4));spr=pygame.transform.scale(preview[self.tetris.next_piece],({1:SCALE*1,2:SCALE*2,3:SCALE*2,4:SCALE*2,5:SCALE*2,6:SCALE*2,7:SCALE*2}[self.tetris.next_piece],{1:SCALE*4,2:SCALE*3,3:SCALE*3,4:SCALE*3,5:SCALE*3,6:SCALE*3,7:SCALE*2}[self.tetris.next_piece]));self.screen.blit(spr,spr.get_rect(topleft=(SCALE*10+X_OFFSET_BRICKS,Y_OFFSET_BRICKS)));spr=pygame.transform.scale(preview[self.tetris.holded_piece],({0:0,1:SCALE*1,2:SCALE*2,3:SCALE*2,4:SCALE*2,5:SCALE*2,6:SCALE*2,7:SCALE*2}[self.tetris.holded_piece],{0:0,1:SCALE*4,2:SCALE*3,3:SCALE*3,4:SCALE*3,5:SCALE*3,6:SCALE*3,7:SCALE*2}[self.tetris.holded_piece]));self.screen.blit(spr,spr.get_rect(topleft=(SCALE*10+X_OFFSET_BRICKS,Y_OFFSET_BRICKS+SCALE*5)));pygame.display.flip()
	def drawRect(self,x,y,type):x=int(x*SCALE+X_OFFSET_BRICKS);y=int((ROWS-(y+1))*SCALE+Y_OFFSET_BRICKS);spr=pygame.transform.scale(sprites[type],(SCALE,SCALE));self.screen.blit(spr,spr.get_rect(topleft=(x,y)))
	def run(self):#minified
		while self.running:self.draw()#minified
		pygame.quit()#minified
	def resize(self):global HEIGHT;global WIDTH;global SCALE;global X_OFFSET_BRICKS;global Y_OFFSET_BRICKS;HEIGHT_=self.screen.get_height();WIDTH_=self.screen.get_width()*1;HEIGHT=HEIGHT_*0.95;WIDTH=int(HEIGHT/ROWS*10);SCALE=int(WIDTH/10);HEIGHT=int(SCALE*ROWS);X_OFFSET_BRICKS=0*SCALE;Y_OFFSET_BRICKS=int(HEIGHT_*0.05);self.screen=pygame.display.set_mode((WIDTH+X_OFFSET_BRICKS+2*SCALE,HEIGHT+Y_OFFSET_BRICKS),pygame.RESIZABLE)
#minified




class Bot:
	def __init__(self,tetris):
		self.__tetris = tetris
	
	def run(self):
		
		self.button = BOTTOM_BTN
		self.button = RIGHT_BTN
		self.button = ROATE_LEFT_BTN



	#all bot allowed to look
	@property 
	def button(self):return
	@button.setter
	def button(self,value):	self.__tetris.button = value
	@property
	def next(self):return self.tetris.next_piece#to preview next piece
	@property
	def holded(self):return self.tetris.holded_piece#to get holded piece
	@property
	def main(self):return self.tetris.main_array#to get main_array






tetris=Tetris(ROWS,TIME_FOR_FALL*FPS)
bot = Bot(tetris)
app=Window(tetris,bot)





def run():app.run()
if __name__=='__main__':run()