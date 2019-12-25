import json
import datetime
import pandas as pd

def get_config(file_name):
	file = open(file_name, 'r', encoding='utf-8')
	result = json.load(file)
	file.close()
	return result

def get_valid_visit(name):
	while True:
		result = str(input(name + ': '))
		if result == '+' or result == '-':
			return result == '+'

def write_file(file_name, content):
	file = open(file_name, 'w')
	json.dump(content, file, indent=4, ensure_ascii=False)
	file.close()

config = get_config('math.json')


now = datetime.datetime.now()
now = str(now.day) + '.' + str(now.month) + '.' + str(now.year)
print(now)


index = []
column = []
df = []
for i in range(len(config)):
	index.append(config[i]['name'])
	config[i]['visit'].append({
		'date': now,
		'presence': get_valid_visit(config[i]['name'])
	})
	_df = []
	for j in range(len(config[i]['visit'])):
		_df.append(config[i]['visit'][j]['presence'])
	df.append(_df)

for i in range(len(config[0]['visit'])):
	column.append(config[0]['visit'][i]['date'])



df = pd.DataFrame(df, index = index, columns = column)

print(df)

write_file('math.json', config)
# print(json.dumps(config, indent=4, ensure_ascii=False))


