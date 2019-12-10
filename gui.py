from tkinter import *
import json
import datetime
import pandas as pd

class WindowApplication():

	def __init__(self):
		obj = self.getData('group.json')

		self.labels = [''] * (len(obj) + 1)
		for i in range(len(self.labels)):
			self.labels[i] = Label(root,
				font = ('Verdana', 20),
				justify = LEFT
				)

		self.labels[0]['text'] = str(datetime.date.today())
		self.labels[0].place(x = 110, y = 40)

		for i in range(len(obj)):
			self.labels[i + 1]['text'] = obj[i]['name']
			self.labels[i + 1].place(x = 20, y = 60 * (i + 2))

		self.entry = [''] * len(obj)
		for i in range(len(self.entry)):
			self.entry[i] = Entry(
				font = ('Verdana', 20),
				justify = CENTER,
				relief = SOLID,
				width = 2
				)
		
		for i in range(len(obj)):
			self.entry[i].place(x = 300, y = 60 * (i + 2))

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

	def getData(self, fileName):
		file = open(fileName, 'r')
		data = json.load(file)
		file.close()
		return data

	def writeFile(self, fileName, data):
		file = open(fileName, 'w')
		json.dump(data, file, indent=4)
		file.close()

	def inputPresence(self, stud):
		if stud != '-' or stud != '':
			return True
		else:
			return False

	def main(self, event):
		data = self.getData('group.json')
		
		for i in range(len(data)):
			data[i]['visiting'].append({
				"date": str(datetime.date.today()),
				"presence": self.inputPresence( str(self.entry[i]) )
				})

		self.writeFile('group.json', data)

	def show(self, event):
		data = self.getData('group.json')

		date = list()
		for i in range(len(data[0]['visiting'])):
			date.append(data[0]['visiting'][i]['date'])

		mtx = dict()
		for i in range(len(data)):
			presence = list()
			for j in range(len(data[i]['visiting'])):
				presence.append(data[i]['visiting'][j]['presence']) 
			mtx[str(data[i]['name'])] = presence

		df = pd.DataFrame(mtx, index=date)
		df = df.T
		df = df[sorted(list(df.columns.values))]

		child = Tk()
		child.title('Просмотр журнала')
		child.wm_geometry('1000x500')
		child.resizable(width=False, height=False)

		label = Label(child,
			font = ('Verdana', 10)
			)
		label['text'] = df
		label.place(x = 0, y = 50)
		
		child.mainloop()

root = Tk()
root.title('Журнал посещения занятий')
root.wm_geometry('415x500')
root.resizable(width=False, height=False)
application = WindowApplication()	
root.mainloop()
