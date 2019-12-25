from tkinter import *
import json
import datetime
import pandas as pd

class WindowApplication():

	def __init__(self):
		obj = self.get_config('math.json')

		self.labels = [''] * (len(obj) + 1)
		for i in range(len(self.labels)):
			self.labels[i] = Label(root,
				font = ('Verdana', 15),
				justify = LEFT
				)
		now = datetime.datetime.now()
		now = str(now.day) + '.' + str(now.month) + '.' + str(now.year)
		self.labels[0]['text'] = now
		self.labels[0].place(x = 110, y = 40)

		for i in range(len(obj)):
			self.labels[i + 1]['text'] = obj[i]['name']
			self.labels[i + 1].place(x = 20, y = 50 * (i + 2))

		self.entry = [''] * len(obj)
		for i in range(len(self.entry)):
			self.entry[i] = Entry(
				font = ('Verdana', 20),
				justify = CENTER,
				relief = SOLID,
				width = 2
				)
		
		for i in range(len(obj)):
			self.entry[i].place(x = 300, y = 50 * (i + 2))

		self.buttons = [''] * 2
		for i in range(len(self.buttons)):
			self.buttons[i] = Button(root,
				font = ('Verdana', 10)
			)

		self.buttons[0]['text'] = 'Применить'
		self.buttons[1]['text'] = 'Отобразить журнал'

		self.buttons[0].place(x = 0, y = 0)
		self.buttons[1].place(x = 270, y = 0)

		self.buttons[0].bind('<ButtonRelease-1>', self.main)
		self.buttons[1].bind('<ButtonRelease-1>', self.show)

	def get_config(self, file_name):
		file = open(file_name, 'r', encoding='utf-8')
		result = json.load(file)
		file.close()
		return result

	def write_file(self, file_name, content):
		file = open(file_name, 'w')
		json.dump(content, file, indent=4, ensure_ascii=False)
		file.close()

	def get_valid_visit(self, number):
		return str(self.entry[number].get()) == '+'
		

	def main(self, event):
		config = self.get_config('math.json')


		now = datetime.datetime.now()
		now = str(now.day) + '.' + str(now.month) + '.' + str(now.year)
		#print(now)
		for i in range(len(config)):
			config[i]['visit'].append({
				'date': now,
				'presence': self.get_valid_visit(i)
			})

		self.write_file('math.json', config)

	def show(self, event):
		config = self.get_config('math.json')
		index = []
		column = []
		df = []
		for i in range(len(config)):
			index.append(config[i]['name'])
			_df = []
			for j in range(len(config[i]['visit'])):
				_df.append(config[i]['visit'][j]['presence'])
			df.append(_df)

		for i in range(len(config[0]['visit'])):
			column.append(config[0]['visit'][i]['date'])

		df = pd.DataFrame(df, index = index, columns = column)

		child = Tk()
		child.title('Просмотр журнала')
		child.wm_geometry('1000x500')
		child.resizable(width=False, height=False)

		label = Label(child,
			font = ('Verdana', 15),
			justify = RIGHT
			)
		label['text'] = df
		label.place(x = 0, y = 50)
		
		child.mainloop()

root = Tk()
root.title('Журнал посещения занятий')
root.wm_geometry('415x500')
root.resizable(width=False, height=True)
application = WindowApplication()	
root.mainloop()
