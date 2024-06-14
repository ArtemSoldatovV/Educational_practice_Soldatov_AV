import sqlite3
import os
import re

db = sqlite3.connect('Artyom_Soldatov_v.sqlite')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS recording_logs(
	ip TEXT,
	text_block TEXT,
	username TEXT,
	data_time TEXT,
	file_route TEXT,
	code_and_number_of_bytes TEXT
)""")

def function_1(text):
	try:
		return list(map(lambda x: [x.group(1),x.group(2),x.group(3),x.group(4),x.group(5),x.group(6)], text))
	except BaseException:
		print("не тот формат данных")
def parsing():
	try:
		choice = input("1.парсинг готового файла 2.парсинг своего файла")
		separation = re.compile(r'(\d*[.]\d*[.]\d*[.]\d*) (.*) (.*) [[](.*)[]] "(.*)" (\d* \d*)')
		if choice=='1':
			f = open(os.path.dirname(os.path.abspath(__file__))+"\\test.log", 'r')
			mas =function_1(separation.finditer(f.read()))
			for i in range(len(mas)):
				sql.execute(f"INSERT INTO recording_logs VALUES ('{mas[i][0]}', '{mas[i][1]}', '{mas[i][2]}', '{mas[i][3]}','{mas[i][4]}','{mas[i][5]}')")
			print("парсинг успешно сделон")
		elif choice=='2':
			way = input("введите путь до файла")
			file_name = input("введите имя файла без расширения")
			f = open(way+"\\"+file_name+".log", 'r')
			mas =function_1(separation.finditer(f.read()))
			for i in range(len(mas)):
				sql.execute(f"INSERT INTO recording_logs VALUES ('{mas[i][0]}', '{mas[i][1]}', '{mas[i][2]}', '{mas[i][3]}','{mas[i][4]}','{mas[i][5]}')")
			print("парсинг успешно сделон")
	except BaseException:
		print("не тот формат данных в файле")
#=======================================
def function_2(text):
	try:
		return list(map(lambda x: [x.group(1),x.group(2),x.group(3)], text))
	except BaseException:
		print("не тот формат данных")
def substitution(abc):
	if abc == "ip":
		return 0
	if abc == "text_block":
		return 1
	if abc == "username":
		return 2
	if abc == "data_time":
		return 3
	if abc == "file_route":
		return 4
	if abc == "code_and_number_of_bytes":
		return 5
def filter_selection(abc,entering_filters):
	command_determinant=re.compile(r'(\w*) ?(>=|<=|-=|>|<|=) ?(\S*)')
	mas =function_2(command_determinant.finditer(entering_filters))
	yes_no = True
	for i in mas:
		if i[1]==">":
			if (abc[substitution(i[0])] > i[2])!=True:
				yes_no = False
		elif i[1]=="<":
			if (abc[substitution(i[0])] < i[2])!=True:
				yes_no = False
		elif i[1]=="=":
			if (abc[substitution(i[0])] == i[2])!=True:
				yes_no = False
		if i[1]==">=":
			if (abc[substitution(i[0])] >= i[2])!=True:
				yes_no = False
		elif i[1]=="<=":
			if (abc[substitution(i[0])] <= i[2])!=True:
				yes_no = False
		elif i[1]=="-=":
			if (abc[substitution(i[0])] != i[2])!=True:
				yes_no = False
	if (yes_no==True):
		return abc
	else:
		return ""

def viewing():
	try:
		choice = input("1.просмотр всей базы данных 2.просмотр с фильтрацией данных")
		if choice=='1':
			for i in sql.execute("SELECT * FROM recording_logs"):
				print(i)
		elif choice=='2':
			print("сортировать можно по нескольким фильтрам и между ними надо ставить пробел")
			print("пример: ip<127.0.0.0 code_and_number_of_bytes>404 7218")
			print("данные по которым можно сортировать: ip text_block  username  data_time file_route code_and_number_of_bytes")
			print("< меньше, > больше, = равно, <= меньше или равно, >= больше или равно, -= не равен")
			entering_filters = input()
			check = True
			for i in sql.execute("SELECT * FROM recording_logs"):
				if (filter_selection(i,entering_filters) ==""):
					print("",end="")
				else:
					print(filter_selection(i,entering_filters))
					check=False
			if (check == True):
				print("нет совподений")
	except BaseException:
		print("базы данных нет или она повреждена")
#=======================================
start_end = True
while(start_end):
	main_menu=input("1.парсинг 2.просмотр 3.закончить программу")
	if main_menu=='1':
		parsing()
	elif main_menu=='2':
		viewing()
	elif main_menu=='3':
		start_end=False
	else:
		print(f"варианта {main_menu} нет")
db.commit()
