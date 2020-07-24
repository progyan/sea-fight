from random import *
from copy import deepcopy
import getpass


def gce(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

blue  = gce(57, 189, 255, True)
lblue = gce(87, 209, 255, True)
green = gce(192, 255, 43, True)
red   = gce(255, 57,  0,  True)

termblue    = gce(57, 189, 255)
termgreen   = gce(192, 255, 43)

def turn_shape(shape, times=1):
	shp = []
	for sh in shape:
		shp.append((sh[1], sh[0]))
	if times == 1:
		return shp
	elif times == 0:
		return shape

def gen_pentamino():
	pentaminoes = [
		[(0,0), (0,1), (0,2), (1,1), (2,1)],
		[(0,0), (1,0), (1,1), (1,2), (2,1)],
		[(0,0), (1,0), (1,1), (1,2), (2,2)],
		[(0,0), (1,0), (2,0), (3,0), (3,1)],
		[(0,0), (1,0), (2,0), (2,1), (2,2)],
		[(0,0), (1,0), (1,1), (2,1), (2,2)],
		[(0,0), (1,0), (2,0), (2,1), (3,1)],
		[(0,0), (1,0), (2,0), (2,1), (1,1)],
		[(0,0), (1,0), (2,0), (2,1), (3,0)],
		[(0,0), (1,0), (0,1), (2,0), (2,1)],
		[(0,0), (1,0), (2,0), (3,0), (4,0)],
		[(0,1), (1,0), (1,1), (1,2), (2,1)]
	]
	return turn_shape(pentaminoes[randint(0, 11)], randint(0, 1))

def place_pentamino(grid, pentamino, place):
	new_grid = deepcopy(grid)
	for s in pentamino:
		x = s[0] + place[0]
		y = s[1] + place[1]
		if x > 9 or y > 9 or x < 0 or y < 0:
			return False
		new_grid[y][x] = 100

	grid = deepcopy(new_grid)
	return grid

def count_katana(nums):
	nums.append(0)
	ans = []
	tmp = 0
	for n in nums:
		if n == 100 or n == 10:
			tmp += 1
		else:
			if tmp != 0:
				ans.append(tmp)
				tmp = 0
	return ans

def print_grid(grid, gridmask, kat1mask, kat2mask):
	kat1 = []
	kat2 = []
	for j in range(10):
		kat1.append(count_katana(grid[j]))
		kat2.append(count_katana([grid[x][j] for x in range(10)]))

	print('   \033[1mА Б В Г Д Е Ж З И К')
	for j in range(10):
		if j < 9:
			print('\033[1m ' + str(j + 1), end='\033[0m ')
		else:
			print('\033[1m10\033[0m ', end='')
		for i in range(10):
			if (j + i) % 2 == 0:
				col = lblue
			else:
				col = blue

			k = grid[i][j]
			if not gridmask[i][j]:
				print(col + '  ' + '\033[0m', end='')
			elif k == 100:
				print('██', end='')
			elif k == -1:
				print(green + '  ' + '\033[0m', end='')
			elif k == 10:
				print(red + '  ' + '\033[0m', end='')
			else:
				print(col + str(k) + ' ' + '\033[0m', end='')
		if kat2mask[j]:
			print('\033[1m' + ' '.join(map(str, kat2[j])) + '\033[0m')
		else:
			print()

	for i in range(5):
		print('  ', end=' ')
		for j in range(10):
			if len(kat1[j]) > i and kat1mask[j]:
				print('\033[1m' + str(kat1[j][i]) + '\033[0m', end=' ')
			else:
				print(' ', end=' ')
		print()

def fill_grid(grid):
	for i in range(10):
		for j in range(10):
			if grid[j][i] == 100:
				continue
			tile = 0
			neighbors = [(j-1, i-1), (j, i-1), (j+1, i-1), (j-1, i), (j+1, i), (j-1, i+1), (j, i+1), (j+1, i+1)]
			for nb in neighbors:
				if nb[0] <= 9 and nb[1] <= 9 and nb[0] >= 0 and nb[1] >= 0 and grid[nb[0]][nb[1]] == 100:
					tile += 1
			grid[j][i] = tile

def command(strs, patrons):
	if strs[0] == 'С':
		gridmask[ord(strs[1]) - 1040][int(strs[2]) - 1] = True
		kat1mask[ord(strs[1]) - 1040] = True
		kat2mask[int(strs[2]) - 1] = True
		patrons -= 1
	elif strs[0] == 'М':
		if grid[ord(strs[1]) - 1040][int(strs[2]) - 1] < 10:
			grid[ord(strs[1]) - 1040][int(strs[2]) - 1] = -1
			gridmask[ord(strs[1]) - 1040][int(strs[2]) - 1] = True
		else:
			gridmask[ord(strs[1]) - 1040][int(strs[2]) - 1] = True
			patrons -= 2
	elif strs[0] == 'К':
		if grid[ord(strs[1]) - 1040][int(strs[2]) - 1] == 100:
			grid[ord(strs[1]) - 1040][int(strs[2]) - 1] = 10
			gridmask[ord(strs[1]) - 1040][int(strs[2]) - 1] = True
		else:
			gridmask[ord(strs[1]) - 1040][int(strs[2]) - 1] = True
			patrons -= 2
	else:
		print('\033[31mERROR 657: "НЕВЕРНАЯ КОМАНДА. Пожалуйста просмотрите правила в начале вывода программы и попробуйте ещё раз."')
	return patrons

def ruleshow():
	print_grid([
		[1,1,0,1,100,100,100,100,1,0],
		[100,2,0,1,3,100,5,4,3,1],
		[100,4,1,1,1,1,2,100,100,2],
		[100,5,100,3,1,0,2,5,100,3],
		[100,5,100,100,3,1,1,100,100,2],
		[100,3,3,100,100,1,1,3,4,3],
		[1,2,2,3,2,1,1,3,100,100],
		[0,2,100,2,0,0,1,100,100,4],
		[1,4,100,4,1,0,1,3,100,2],
		[1,100,100,100,1,0,0,1,1,1]
	], [[True for i in range(10)] for i in range(10)], [True for i in range(10)], [True for i in range(10)])


grid = [[-1 for i in range(10)] for i in range(10)]
seacode = chr(randint(33, 122)) + chr(randint(33, 122)) + chr(randint(33, 122))
patrons = 10
rules = '''Правила игры "ГОЛОВОЛОМНЫЙ МОРСКОЙ БОЙ":
На поле 10х10 расположены 5 кораблей в форме пентамино (фигурки из 5 клеток). Формы кораблей известны. Корабли не касаются друг друга даже углами. Цель игры - потопить все корабли. 

В начале у Вас 10 патронов и Вам неизвестно, где находятся корабли.

За один ход можно сначала “бесплатно” (без использования патронов) открыть какие-то участки поля. После этого нужно сделать выстрел. 

Если выстрел попал в море, то рыба-шпион сообщает, сколько клеток из 8, окружающих эту, занято кораблями. 
Если выстрел попал в корабль, крыса-шпион сообщает информацию о расположении кораблей в этой строке и столбце (см. пример). Крыса-шпион перечисляет по порядку длины блоков подряд идущих клеток, занятых кораблями. Между этими блоками может быть любое количество клеток моря (>0). (Похоже на японские кроссворды.)

“Бесплатно” можно открыть любую клетку поля, если Вы можете доказать, почему Вы точно знаете, что в этой клетке море или кусок корабля, исходя из полученной ранее информации.
Сначала открывайте все, что можно, "бесплатно", потом делайте 1 выстрел.

Можно играть с друзьями, делая ходы (описание строкой выше) по очереди!

Интерфейс игры \"ГОЛОВОЛОМНЫЙ МОРСКОЙ БОЙ\"

'''+blue+'''Голубые\033[0m клетки обозначают море.
'''+green+'''Зелёные\033[0m клетки обозначают правильно угаданную клетку с морем.
'''+red+'''Красные\033[0m клетки - правильно угаданные корабли.
Чёрные (белые) клетки - простреленные корабли.

Выстрел можно легко сделать с помощью команды

\033[34mС Б 4\033[0m

, если хочется стрельнуть в клетку Б-4 на игровом поле.

Если Вы уверены в том, что на клетке, например, И-6, расположен корабль, напишите:

\033[34mК И 6\033[0m

А если море, то:

\033[34mМ И 6\033[0m

Пример поля, на котором открыта вся возможная информация, ниже.

'''

rules2 = '''

ВНИМАНИЕ! Программа должна запускаться в цветной среде Python. Если внизу правильно
окрашены слова, можно играть!

'''+blue+'''голубой фон\033[0m
'''+lblue+'''фон чуть светлее\033[0m
'''+green+'''светло зелёный фон\033[0m
'''+red+'''красный фон\033[0m
\033[34mсиний текст\033[0m
'''

gridmask = [[False for i in range(10)] for i in range(10)]
kat1mask = [False for i in range(10)]
kat2mask = [False for i in range(10)]

for i in range(5):
	ok = False
	while not ok:
		g = place_pentamino(grid, turn_shape(gen_pentamino()), (randint(0, 9), randint(0, 9)))
		if not g == False:
			grid = g
			ok = True
fill_grid(grid)

if input("Если вы играете первый раз, введите слово \"да\" и нажмите Enter. Если нет, просто нажмите Enter. ").lower() == "да":
	print(rules)
	ruleshow()
	print(rules2)

print()
input()

while True:
	print_grid(grid, gridmask, kat1mask, kat2mask)
	print('Вычисляем... Количество оставшихся патронов: ' + str(patrons))
	if patrons == 0:
		print('Увы, но Ваши патроны закончились. Удачи в следующей игре!')
	patrons = command(input('\033[34m~/ROBOGUN[sea:' + seacode + ']$\033[0m Введите команду для робо-пушки: \033[34m').split(), patrons)
	print('\033[0m')
