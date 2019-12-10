import json
import datetime
import pandas as pd

def getData(fileName):
	file = open(fileName, 'r')
	data = json.load(file)
	file.close()
	return data

def writeFile(fileName, data):
	file = open(fileName, 'w')
	json.dump(data, file, indent=4)
	file.close()

def inputPresence(stud):
	while True:
		result = str(input(str(stud) + '? '))
		if result == '+' or result == '-':
			return result == '+'

print(datetime.date.today())

data = getData('group.json')

for i in range(len(data)):
	data[i]['visiting'].append({
		"date": str(datetime.date.today()),
		"presence": inputPresence( str(data[i]['name']) )
		})

writeFile('group.json', data)

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

print(df)