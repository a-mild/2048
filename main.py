from tkinter import *
import numpy as np
from random import randint

CELL_SIZE = 40
GRID_SIZE = 4

COLORS = {2**x: '#{0:06x}'.format(randint(0, 16**6-1)) 
			for x in range(1, GRID_SIZE**2)}
COLORS = {0: "#808080", **COLORS}

print(COLORS)

class Grid(object):
	def __init__(self):
		self.matrix = np.zeros((GRID_SIZE, GRID_SIZE), np.int32)

		# create two starting cells
		for i in range(2):
			while True:
				x, y = randint(0, GRID_SIZE-1), randint(0, GRID_SIZE-1)
				if self.matrix[x, y] == 0:
					self.matrix[x, y] = 2*randint(1, 2)
					break

	def move(self, matrix):
		for y in range(GRID_SIZE):
			# remove 0s
			tmp = [matrix[x, y] for x in range(GRID_SIZE) if matrix[x, y] != 0]
			print(tmp)
			# merge equal values
			for i in range(len(tmp)-1):
				if tmp[i] == tmp[i+1]:
					tmp[i] *= 2
					print(tmp[i])
					self.score.set(self.score.get() + tmp[i])
					tmp[i+1] = 0
			# remove 0s again
			tmp = [tmp[i] for i in range(len(tmp)) if tmp[i] != 0]
			print(tmp)
			# write to matrix
			matrix[:, y] = tmp + [0 for x in range(GRID_SIZE - len(tmp))]
			print(matrix[:, y])
		return matrix

	def new_cell(self):
		while True:
			x, y = randint(0, GRID_SIZE-1), randint(0, GRID_SIZE-1)
			if self.matrix[x, y] == 0:
				self.matrix[x, y] = 2*randint(1,2)
				break

class Game(Grid):
	celloptions = {"width": 6, "height": 3,
					"padx": 3, "pady": 3,
					"relief": "sunken"}

	def __init__(self):
		self.app = Tk()
		self.app.title("2048 - oder auch mehr :)")
		self.app.bind("<Key>", self.handle_input)

		self.matrix = Grid().matrix
		self.score = IntVar(self.app)
		self.score.set(0)

		self.colors = {}

		self.f_score = Frame(self.app)
		score_label = Label(self.f_score, text="Score")
		score_label.pack(side=LEFT)
		score = Label(self.f_score, textvariable=self.score)
		score.pack(side=LEFT)
		self.f_score.pack()


		self.f_grid = Frame(self.app)
		self.f_grid.pack()

		self.draw_grid()

		self.app.mainloop()

	def draw_grid(self):
		for i in range(GRID_SIZE):
			for j in range(GRID_SIZE):
				val = self.matrix[i, j]
				color = COLORS[val]
				l = Label(self.f_grid, text=val,
					background=color,
					**Game.celloptions)
				l.grid(row=i, column=j, sticky=NSEW)
		print(self.matrix)

	def handle_input(self, event):
		old = np.copy(self.matrix)

		if event.keysym == "Up":
			self.up()
		elif event.keysym == "Down":
			self.down()
		elif event.keysym == "Left":
			self.left()
		elif event.keysym == "Right":
			self.right()

		if not np.array_equal(old, self.matrix):
			self.new_cell()
		# else:
		# 	print("kann keine neue zelle machen")

		self.draw_grid()

	def up(self):
		self.matrix = self.move(self.matrix)

	def down(self):
		tmp = np.flipud(self.matrix)
		tmp = self.move(tmp)
		tmp = np.flipud(tmp)
		self.matrix = tmp

	def left(self):
		tmp = np.transpose(self.matrix)
		tmp = np.fliplr(tmp)
		tmp = self.move(tmp)
		tmp = np.fliplr(tmp)
		self.matrix = np.transpose(tmp)

	def right(self):
		tmp = np.fliplr(self.matrix)
		tmp = np.transpose(tmp)
		tmp = self.move(tmp)
		tmp = np.transpose(tmp)
		self.matrix = np.fliplr(tmp)

game = Game()
