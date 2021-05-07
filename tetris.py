#main array anotation:
# 0 : nothing           color
# - something: whited   color
# 1 :bar                color
# 2 :L                  color
# 3 :J                  color
# 4 :T                  color
# 5 :Z                  color
# 6 :inverted Z         color
# 7 :brick              color

#sound annotation:
#0 - nothing
#1 - rotate
#2 - clear line
#3 - can't swap

#button annotation:
# -1-rotate-left
# 1-rotate-right
# 2-bottom
# 3-right
# 4-left
# 5 -hlod

from random import choice


class Tetris:
	def __init__(self,height=15,speed_frames=60):
		self.__main_array = [
			[ 0 for j in range(height) ] for i in range(10)
		]
		self.__lines_breaked = 0
		self.__felled_array = [
			[ 0 for j in range(height) ] for i in range(10)
		]
		self.height = height
		self.__sound = []
		self.__sample_pack = [1,2,3,4,5,6,7]
		self.__pack = self.__sample_pack.copy()
		self.__next_piece = choice(self.__pack)
		self.__pack.remove(self.__next_piece)
		
		
		self.__next_piece_2 = choice(self.__pack)
		self.__pack.remove(self.__next_piece_2)
		
		
		
		self.__next_piece_3 = choice(self.__pack)
		self.__pack.remove(self.__next_piece_3)
		
		self.__next_piece_4 = choice(self.__pack)
		self.__pack.remove(self.__next_piece_4)
				

		self.__next_piece_5 = choice(self.__pack)
		self.__pack.remove(self.__next_piece_5)
																		
		
		
		self.__buttons = []

		self.__speed_frames = speed_frames
		self.__frames_passed = 0


		self.__current_brick_type = choice(self.__pack)
		self.__pack.remove(self.__current_brick_type)
		
		self.__make_pos()
		self.__score = 0
		self.__delete_lines = []
		self.__current_rotation = 0
		self.__holded = 0
		self.__hold_allowed = True
		


# 1 :bar                color
# 2 :L                  color
# 3 :J                  color
# 4 :T                  color
# 5 :Z                  color
# 6 :inverted Z         color
# 7 :brick              color




	def __die(self):
		self.__current_brick_pos = []
		self.die = True
		#print("died")

		self = self.__init__(self.height,(self.__speed_frames-1))#restart but harder


	def __move_brick_by(self,offset):
		try:
			copy = [[ 0,0 ] for i in range(4)]

			for i in range(len(self.__current_brick_pos)):
				copy[i] = self.__current_brick_pos[i].copy()



			for i in copy: #move
				i[0] -=offset
				assert i[0] >=0 and i[0] <=9, "Hit borders"
				assert not self.__felled_array[i[0]][i[1]], "Hit something"
				
				
			self.__current_brick_pos = copy
		

		except AssertionError:#hit ground
			pass

	def __move_brick(self):



		try:
			copy = [[ 0,0 ] for i in range(4)]

			for i in range(len(self.__current_brick_pos)):
				copy[i] = self.__current_brick_pos[i].copy()



			for i in copy: #move
				i[1] -=1
				assert not self.__felled_array[i[0]][i[1]], "Hit something"
				assert i[0]>=0 and i[1]>=0, "hit ground"
				
			self.__current_brick_pos = copy
		

		except AssertionError:#hit ground
			for i in self.__current_brick_pos:
				self.__felled_array[i[0]][i[1]] = self.__current_brick_type # add brick
			self.__swap_current_brick()

	def __delete_if_possible(self):
		if not self.__delete_lines:
			return 0
		self.__sound.append(2)
		self.__delete_lines.sort(reverse=True)
		for line_to_delete in self.__delete_lines:
			self.__lines_breaked +=1
			for line_to_move in range(line_to_delete,self.height-1):
				for x in range(len(self.__felled_array)):
					self.__felled_array[x][line_to_move] = self.__felled_array[x][line_to_move+1]
				for x in range(len(self.__felled_array)):
					self.__felled_array[x][self.height-1] = 0
		self.__delete_lines = []




	def __check_for_lines(self):
		y_shaped_array =[[ 0 for i in range(10)]  for j in range(self.height)]

		for x in range(len(self.__felled_array)):
			for y in range(len(self.__felled_array[x])):
				y_shaped_array[y][x] = self.__felled_array[x][y]


		delete_lines = []
		for y in range(len(y_shaped_array)):
			i = True
			for x in y_shaped_array[y]:
				i = i and x
			if i:
				delete_lines.append(y)

		for x in range(len(self.__felled_array)):
			for y in range(len(self.__felled_array[x])):
				if y in delete_lines:
					self.__felled_array[x][y] = -abs(self.__felled_array[x][y])

		self.__delete_lines = delete_lines
		#print(delete_lines)


	def __swap_current_brick(self):
		
		self.__check_for_lines()
		(self.__current_brick_type,
		self.__next_piece,
		self.__next_piece_2,
		self.__next_piece_3,
		self.__next_piece_4) = (self.__next_piece,
		self.__next_piece_2,
		self.__next_piece_3,
		self.__next_piece_4,
		self.__next_piece_5)
		
		if len(self.__pack) ==0: self.__pack = self.__sample_pack.copy()
		self.__next_piece_5 = choice(self.__pack)
		self.__pack.remove(self.__next_piece_5)
	
		self.__make_pos()

		self.__hold_allowed = True

		try:
			for i in self.__current_brick_pos: #move
				assert not self.__felled_array[i[0]][i[1]], "Hit something"

		except AssertionError:
			self.__die()



	def __next(self,buttons=()):
		if 1 in buttons:#rotate right
			self.__current_rotation = (self.__current_rotation+1) % 4;copy = self.__rotate(self.__current_brick_pos)
			try:
				for i in copy:assert i[0]>=0 and i[1]>=0 and i[1]<self.height and i[0]<10, "borders";assert not self.__felled_array[i[0]][i[1]], "Hit something";
				self.__current_brick_pos = copy.copy();self.__sound.append(1)
			except AssertionError:self.__current_rotation = (self.__current_rotation-1) % 4 

		if -1 in buttons:#rotate left
			self.__current_rotation = (self.__current_rotation+1) % 4;copy = self.__rotate(self.__current_brick_pos);self.__current_rotation = (self.__current_rotation+1) % 4;copy = self.__rotate(copy);self.__current_rotation = (self.__current_rotation+1) % 4;copy = self.__rotate(copy);self.__sound.append(1)
			try:
				for i in copy: assert i[0]>=0 and i[1]>=0 and i[1]<self.height and i[0]<10, "borders"; assert not self.__felled_array[i[0]][i[1]], "Hit something"
				self.__current_brick_pos = copy.copy()
			except AssertionError:self.__current_rotation = (self.__current_rotation-3) % 4 

		if 5 in buttons:#hold
			self.__hold()




		self.__frames_passed +=1
		if self.__frames_passed >= self.__speed_frames:
			self.__delete_if_possible()
			self.__move_brick()
			self.__frames_passed = 0
		if 2 in buttons: 
			self.__delete_if_possible()
			self.__move_brick()
			self.__score+=1
			self.__frames_passed = 0
		if 3 in buttons: self.__move_brick_by(-1)
		if 4 in buttons: self.__move_brick_by(1)
		

		#adding bricks

		copy = [[ 0 for j in range(self.height) ] for i in range(10)]
		for i in range(len(self.__felled_array)):
			copy[i] = self.__felled_array[i].copy()
		
		for i in self.__current_brick_pos:
			copy[i[0]][i[1]] = self.__current_brick_type



		self.__main_array = copy


	def __make_pos(self):

		self.__current_rotation = 0
		height = self.height-1
		if self.__current_brick_type == 1:
			self.__current_brick_pos = [ [3,height] ,  [4,height], [5,height], [6,height]]
			return 0
		if self.__current_brick_type == 2:
			self.__current_brick_pos = [[3,height-1], [4,height-1],[5,height-1],[5,height]] 
			return 0
		if self.__current_brick_type == 3:
			self.__current_brick_pos = [ [3,height],[3,height-1], [4,height-1] , [5,height-1]] 
			return 
		if self.__current_brick_type == 4:
			self.__current_brick_pos = [[3,height-1],[4,height-1],[4,height],[5,height-1]] 
			return 0
		if self.__current_brick_type == 5:
			self.__current_brick_pos = [ [3,height-1], [4,height-1],[4,height],[5,height] ] 
			return 0
		if self.__current_brick_type == 6:
			self.__current_brick_pos = [[3,height],[4,height], [4,height-1], [5,height-1] ] 
			return 0
		if self.__current_brick_type == 7:
			self.__current_brick_pos = [[4,height],[4,height-1], [5,height-1],  [5,height]] 
			return 0

		return 1

	def __rotate(self,brick_pos):
		
		pos = brick_pos
		copy = [i.copy() for i in brick_pos]


		if self.__current_brick_type == 1:#bar #works
			if self.__current_rotation==0: copy = [ [pos[0][0]-2,pos[0][1]-1] ,[pos[1][0]-1,pos[1][1]], [pos[2][0],pos[2][1]+1],[pos[3][0]+1,pos[3][1]+2] ]
			if self.__current_rotation==1: copy = [ [pos[0][0]+1,pos[0][1]+1] ,[pos[1][0],pos[1][1]], [pos[2][0]-1,pos[2][1]-1],[pos[3][0]-2,pos[3][1]-2] ]
			if self.__current_rotation==2: copy = [ [pos[0][0]-1,pos[0][1]-2] ,[pos[1][0],pos[1][1]-1], [pos[2][0]+1,pos[2][1]],[pos[3][0]+2,pos[3][1]+1] ]
			if self.__current_rotation==3: copy = [ [pos[0][0]+2,pos[0][1]+2] ,[pos[1][0]+1,pos[1][1]+1], [pos[2][0],pos[2][1]],[pos[3][0]-1,pos[3][1]-1] ]
			
		if self.__current_brick_type == 2:#L  #WORKS
			if self.__current_rotation==0: copy = [ [pos[0][0],pos[0][1]-2] ,[pos[1][0]+1,pos[1][1]-1], [pos[2][0]+2,pos[2][1]],[pos[3][0]+1,pos[3][1]+1] ]
			if self.__current_rotation==1: copy = [ [pos[0][0]+2,pos[0][1]] ,[pos[1][0]+1,pos[1][1]+1], [pos[2][0],pos[2][1]+2],[pos[3][0]-1,pos[3][1]+1] ]
			if self.__current_rotation==2: copy = [ [pos[0][0],pos[0][1]+2] ,[pos[1][0]-1,pos[1][1]+1], [pos[2][0]-2,pos[2][1]],[pos[3][0]-1,pos[3][1]-1] ]
			if self.__current_rotation==3: copy = [ [pos[0][0]-2,pos[0][1]] ,[pos[1][0]-1,pos[1][1]-1], [pos[2][0],pos[2][1]-2],[pos[3][0]+1,pos[3][1]-1] ]

		if self.__current_brick_type == 3:#J #works
			if self.__current_rotation==0: copy = [ [pos[0][0]-1,pos[0][1]-1] ,[pos[1][0],pos[1][1]-2], [pos[2][0]+1,pos[2][1]-1],[pos[3][0]+2,pos[3][1]] ]
			if self.__current_rotation==1: copy = [ [pos[0][0]+1,pos[0][1]-1] ,[pos[1][0]+2,pos[1][1]], [pos[2][0]+1,pos[2][1]+1],[pos[3][0],pos[3][1]+2] ]
			if self.__current_rotation==2: copy = [ [pos[0][0]+1,pos[0][1]+1] ,[pos[1][0],pos[1][1]+2], [pos[2][0]-1,pos[2][1]+1],[pos[3][0]-2,pos[3][1]] ]
			if self.__current_rotation==3: copy = [ [pos[0][0]-1,pos[0][1]+1] ,[pos[1][0]-2,pos[1][1]], [pos[2][0]-1,pos[2][1]-1],[pos[3][0],pos[3][1]-2] ]
			
		if self.__current_brick_type == 4:#T #works
			if self.__current_rotation==0: copy = [ [pos[0][0],pos[0][1]-2] ,[pos[1][0]+1,pos[1][1]-1], [pos[2][0],pos[2][1]],[pos[3][0]+2,pos[3][1]] ]
			if self.__current_rotation==1: copy = [ [pos[0][0]+2,pos[0][1]] ,[pos[1][0]+1,pos[1][1]+1], [pos[2][0],pos[2][1]],[pos[3][0],pos[3][1]+2] ]
			if self.__current_rotation==2: copy = [ [pos[0][0],pos[0][1]+2] ,[pos[1][0]-1,pos[1][1]+1], [pos[2][0],pos[2][1]],[pos[3][0]-2,pos[3][1]] ]
			if self.__current_rotation==3: copy = [ [pos[0][0]-2,pos[0][1]] ,[pos[1][0]-1,pos[1][1]-1], [pos[2][0],pos[2][1]],[pos[3][0],pos[3][1]-2] ]
			
		if self.__current_brick_type == 5:#Z # works
			if self.__current_rotation==0: copy = [ [pos[0][0],pos[0][1]-2] ,[pos[1][0]+1,pos[1][1]-1], [pos[2][0],pos[2][1]],[pos[3][0]+1,pos[3][1]+1] ]
			if self.__current_rotation==1: copy = [ [pos[0][0]+1,pos[0][1]+2] ,[pos[1][0],pos[1][1]+1], [pos[2][0]+1,pos[2][1]],[pos[3][0],pos[3][1]-1] ]
			if self.__current_rotation==2: copy = [ [pos[0][0]-1,pos[0][1]-1] ,[pos[1][0],pos[1][1]], [pos[2][0]-1,pos[2][1]+1],[pos[3][0],pos[3][1]+2] ]
			if self.__current_rotation==3: copy = [ [pos[0][0],pos[0][1]+1] ,[pos[1][0]-1,pos[1][1]], [pos[2][0],pos[2][1]-1],[pos[3][0]-1,pos[3][1]-2] ]
			


		if self.__current_brick_type == 6:#Z inverted
			if self.__current_rotation==0: copy = [ [pos[0][0],pos[0][1]+1] ,[pos[1][0]+1,pos[1][1]], [pos[2][0],pos[2][1]-1],[pos[3][0]+1,pos[3][1]-2] ]
			if self.__current_rotation==1: copy = [ [pos[0][0]+1,pos[0][1]-1] ,[pos[1][0],pos[1][1]], [pos[2][0]+1,pos[2][1]+1],[pos[3][0],pos[3][1]+2] ]
			if self.__current_rotation==2: copy = [ [pos[0][0]-1,pos[0][1]+2] ,[pos[1][0],pos[1][1]+1], [pos[2][0]-1,pos[2][1]],[pos[3][0],pos[3][1]-1] ]
			if self.__current_rotation==3: copy = [ [pos[0][0],pos[0][1]-2] ,[pos[1][0]-1,pos[1][1]-1], [pos[2][0],pos[2][1]],[pos[3][0]-1,pos[3][1]+1] ]
			





		if self.__current_brick_type == 7:#brick # works #SIMETRIC
			copy = [ [pos[0][0],pos[0][1]] ,[pos[1][0],pos[1][1]], [pos[2][0],pos[2][1]],[pos[3][0],pos[3][1]] ]





		return copy







	def __hold(self):
		if not self.__hold_allowed:
			self.__sound.append(3)
			return

		if not self.__holded:
			self.__holded = self.__current_brick_type 
			self.__swap_current_brick()
			self.__hold_allowed = False
			return 

		

		self.__holded,self.__current_brick_type = self.__current_brick_type, self.__holded
		self.__make_pos()
		
		self.__hold_allowed = False

		







# acceseble


	@property #for setter
	def button(self):#for setter
		return self.__buttons#for setter
	
	@button.setter#to push buttons
	def button(self,value):
		self.__buttons.append(value)




	@property
	def score(self):#to get score
		return self.__score + 1000 * self.__lines_breaked

	@property
	def sound(self):#to get sound
		if len(self.__sound) >=1:
			return self.__sound.pop(0)	
		return 0






	@property
	def lines_breaked(self):#to get lines breaked number
		return self.__lines_breaked

	@property
	def next_pieces(self):#to preview next pieces
		return (
		self.__next_piece,
		self.__next_piece_2,
		self.__next_piece_3,	
		self.__next_piece_4,
		self.__next_piece_5	
		
		)

	@property
	def holded_piece(self):#to get holded piece
		return self.__holded



	@property
	def main_array(self):#to get main_array
		self.__next(self.__buttons)
		self.__buttons = []

		return self.__main_array


	