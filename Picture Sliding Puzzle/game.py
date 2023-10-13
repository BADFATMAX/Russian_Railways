import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from tkinter import messagebox
from datetime import datetime

import os
import glob

from logic import isSolvable, isSolved
from game_over_screen import GameWon

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.gridCells = []
		self.imgType = tk.StringVar()
		self.imgType.set('rail')
		self.numMoves = 0
		self.firstMove = True
		self.timer_id = None

		self.imgDict = {}
		self.solDict = {}

		for directory in os.listdir('images'):
			if directory.startswith('rail_map_'):
				img_files = glob.glob(f'images/{directory}/img*.png')
				img_files.sort()
				self.imgDict[directory] = [PhotoImage(file=img_file) for img_file in img_files]
				self.solDict[directory] = PhotoImage(file=f'images/rail_map_{directory.split("_")[2]}_resized.png')


		self.draw_header()
		self.draw_body()
		
		self.master.bind('<Up>', self.up)
		self.master.bind('<Down>', self.down)
		self.master.bind('<Left>', self.left)
		self.master.bind('<Right>', self.right)

		self.imgType.trace_add('write', self.new_game)

	def draw_header(self):
		self.header = tk.LabelFrame(self, width=600, height=100, bg='red', relief=tk.SUNKEN)
		self.header.grid()
		self.header.grid_propagate(False)

		self.reset_btn = tk.Button(self.header, image=refresh_icon,
				relief=tk.FLAT, command=self.new_game, bg='red')
		self.reset_btn.grid(row=0, column=0, padx=(30,10), pady=0)

		style = ttk.Style()
		style.configure('Red.TMenubutton', background='red')
		# self.options = ttk.OptionMenu(self.header, self.imgType, 'rail_map_1', *self.imgDict.keys())
		# self.options.config(width=10)
		# self.options.grid(row=0, column=1, padx=(30,10), pady=10)

		directories = [directory for directory in os.listdir('images') if os.path.isdir(os.path.join('images', directory))]
		#options_menu_values = [directory for directory in os.listdir('images') if directory.startswith('rail_map_')]
		#excluded_strings = [f'rail_map_{directory.split("_")[0]}_resized' for directory in os.listdir('images') if directory.startswith('rail_map_')]
		#result = [x for x in options_menu_values if x not in excluded_strings]
		self.options = ttk.OptionMenu(self.header, self.imgType, 'rail_map_1', *directories, style='Red.TMenubutton')
		self.options.config(width=10)
		self.options.grid(row=0, column=1, padx=(30,10), pady=10)
		
		# self.options.bind("<Configure>", self.new_game)

		self.hint_btn = tk.Button(self.header, image=hint_icon,
				relief=tk.FLAT, command=self.show_solution, bg='red')
		self.hint_btn.grid(row=0, column=2, padx=(30,10), pady=0)

		self.timer_label = tk.Label(self.header, font=('verdana', 14), fg='black',
						text='00:00:00', width=10, bg='red')
		self.timer_label.grid(row=1, column=0, columnspan=3)

		self.movesFrame = tk.LabelFrame(self.header, width=150, height=150, bg='red', borderwidth=0)
		self.movesFrame.grid(row=0, column=3, rowspan=2)
		#self.movesFrame.pack(side='right')
		self.movesFrame.grid_propagate(True)

		self.movesLabel = tk.Label(self.movesFrame, bg='red', fg='white', text=self.numMoves,
						font='verdana 24', width=5, height=2, borderwidth=0)
		self.movesLabel.grid(row=0, column=0)

		self.imageLabel = tk.Label(self.movesFrame, image=logo_image, bg='red', borderwidth=0)
		self.imageLabel.grid(row=0, column=1)

		self.sbody = tk.Frame(self, width=600, height=400)
		self.slabel = tk.Label(self.sbody, image=self.solDict[self.imgType.get()])
		self.slabel.grid(row=0, column=0)

	def draw_body(self):
		self.body = tk.Frame(self, width=600, height=400)
		self.body.grid()
		self.body.grid_propagate(False)

		self.create_board(self.imgType.get())

	def create_board(self, im_type):
		self.array = [i for i in range(1,16)] + [0]
		random.shuffle(self.array)
		while not isSolvable(self.array):
			random.shuffle(self.array)

		self.emptyCell = self.array.index(0)
		img_list = self.imgDict[im_type]
		self.imgMatrix = [img_list[index-1] if index else None for index in self.array]

		for index, img in enumerate(self.imgMatrix):
				frame = tk.Frame(self.body, width=150, height=100)
				frame.grid(row=index//4, column=index%4)
				frame.grid_propagate(False)

				if img:
					lbl = tk.Label(frame, image=img)
				else:
					img = white_bg
					lbl = tk.Label(frame, image=img)

				lbl.grid()
				lbl.bind('<Button-1>', lambda event, pos=index: self.move(pos))
				self.gridCells.append(lbl)

	def new_game(self, *args):
		self.body.destroy()

		self.numMoves = 0
		self.movesLabel['text'] = self.numMoves
		self.firstMove = True
		self.gridCells = []

		if self.timer_id:
			self.after_cancel(self.timer_id)
			self.timer_label['text'] = '00:00:00'
		# self.start_time = datetime.now()

		self.draw_body()

	def move(self, pos):
		# print(pos)
		
		if self.imgMatrix[pos]:
			for num in (-1, 1, -4, 4):
				index = num + pos
				if index == self.emptyCell and (pos % 4 - (index % 4) in (-1,0,1)):
					self.swap_cell(pos, index)
					self.emptyCell = pos
					self.update_state()

	def up(self, event=None):
		if self.emptyCell - 4 >= 0:
			self.swap_cell(self.emptyCell, self.emptyCell - 4)
			self.emptyCell -= 4
			self.update_state()

	def down(self, event=None):
		if self.emptyCell + 4 <= 15:
			self.swap_cell(self.emptyCell, self.emptyCell + 4)
			self.emptyCell += 4
			self.update_state()

	def left(self, event=None):
		row_changed = self.emptyCell // 4 == (self.emptyCell - 1) // 4
		if 0 <= (self.emptyCell - 1) % 4 < 4 and row_changed:
			self.swap_cell(self.emptyCell, self.emptyCell - 1)
			self.emptyCell -= 1
			self.update_state()

	def right(self, event=None):
		row_changed = self.emptyCell // 4 == (self.emptyCell + 1) // 4
		if 0 <= (self.emptyCell + 1) % 4 < 4 and row_changed:
			self.swap_cell(self.emptyCell, self.emptyCell + 1)
			self.emptyCell += 1
			self.update_state()

	def swap_cell(self, p1, p2):
		if self.firstMove:
			self.start_time = datetime.now()
			self.firstMove = False
			self.timer_id = self.after(1000, self.update_timer)

		self.imgMatrix[p1], self.imgMatrix[p2] = self.imgMatrix[p2], self.imgMatrix[p1]
		self.array[p1], self.array[p2] = self.array[p2], self.array[p1]
		self.update_moves()

		if isSolved(self.array):
			GameWon(self.master, self.numMoves, self.new_game)

	def update_state(self):
		for index, img in enumerate(self.imgMatrix):
			if img:
				self.gridCells[index]['image'] = img
			else:
				self.gridCells[index]['image'] = white_bg
		self.update_idletasks()

	def update_moves(self):
		self.numMoves += 1
		self.movesLabel['text'] = self.numMoves

	def update_timer(self):
		now =  datetime.now()
		minutes, seconds = divmod((now - self.start_time).total_seconds(),60)
		string = f"00:{int(minutes):02}:{round(seconds):02}"
		self.timer_label['text'] = string
		self.timer_id = self.after(1000, self.update_timer)

	def show_solution(self):
		self.body.grid_forget()
		self.sbody.grid()
		self.slabel['image'] = self.solDict[self.imgType.get()]
		self.reset_btn.config(state=tk.DISABLED)
		self.hint_btn.config(state=tk.DISABLED)
		self.after(1000, self.hide_solution)

	def hide_solution(self):
		self.sbody.grid_forget()
		self.body.grid()
		self.reset_btn.config(state=tk.NORMAL)
		self.hint_btn.config(state=tk.NORMAL)


if __name__ == '__main__':
	root = tk.Tk()
	root.title('Picture Puzzle')
	root.configure(bg='red')
	root.geometry('600x500+450+130')

	white_bg = PhotoImage(file='icons/white_bg.png') 
	refresh_icon = PhotoImage(file='icons/refresh.png')
	hint_icon = PhotoImage(file='icons/hint.png')
	solved_icon = PhotoImage(file='icons/solved.png')
	logo_image = PhotoImage(file='icons/white_bg_1.png')
	#gif = tk.PhotoImage(file='icons/cga_train2.gif')

	#rail_map_1_list = [PhotoImage(file=f'images/rail_map_1/img{index}.png') for index in range(1,17)]

	#rail_map_1_sol = PhotoImage(file='images/rail_map_1_resized.png')

	app = Application(master=root)
	app.mainloop()