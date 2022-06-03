from config import token, admin_id
import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
import time
from os.path import abspath as tdir

# библиотеки: os, vk_api, random, json
# афйлы: config.py (заполненый)

session = vk_api.VkApi(token = token)
vk = session.get_api()
longpoll = VkLongPoll(session)


class User():
	def __init__(self, id, task, balans, mode):
		self.id = id # id пользователя
		self.task = task # текущее задание
		self.mode = mode # текущий режим
		self.balans = balans # текущий баланс
		self.yandex = ''
		self.sber = ''
		self.last_ok = 0


def get_keyboard(buts):
	global get_but
	nb = []
	color = ''
	for i in range(len(buts)):
		nb.append([])
		for k in range(len(buts[i])):
			nb[i].append(None)
	for i in range(len(buts)):
		for k in range(len(buts[i])):
			text = buts[i][k][0]
			if buts[i][k][1] == 'зеленый':
				color = 'positive'
			elif buts[i][k][1] == 'красный':
				color = 'negative'
			elif buts[i][k][1] == 'синий':
				color = 'primary'
			nb[i][k] = {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + "1" + "\"}",
                    "label": f"{text}"
                },
                "color": f"{color}"
            }
	first_keyboard = {
	    'one_time': False,
	    'buttons': nb
	    }
	first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard


file = open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'utf-8')
lines = file.readlines()
file.close()

users = []
try:
	for line in lines:
		line = line.replace('\n', '')
		user = eval(line)
		users.append(User(id = user['id'], task = user['task'], balans = user['balans'], mode = user['mode']))
except Exception:
	pass

in_users = False


# клавиатуры

clear_key = get_keyboard(
	[]
)

key_for_start = get_keyboard(
	[[('Задания','зеленый'),('Баланс','синий')]]
)

key_for_balans = get_keyboard(
	[[('Снять','синий'),('Назад','красный')]]
)

key_in_balans = get_keyboard(
	[[('Сбер','синий'),('Яндекс','синий'), ('Назад','красный')]]
)

key_for_main1 = get_keyboard(
	[[('Получить задание','синий'), ('Назад','красный')]]
)

key_for_main2 = get_keyboard(
	[[('Готово','зеленый'), ('Пропустить','красный'), ('Назад','красный')]]
)

key_for_main3 = get_keyboard(
	[[('Получить новое задание','зеленый'), ('Назад','красный')]]
)

# клавиатуры


def sender(id, text, key):
	session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : key})


def clear_sender(id, text):
	session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0})


def update_bd(user):
	try:
		id = user.id
		balans = user.balans
		task = user.task
		mode = user.mode
		data = f'"id" : {id}, "task" : "{task}", "balans" : {balans}, "mode" : "{mode}"'
		data = eval('{' + data + '}') # актуальная инфа
		data = str(data) # актуальная инфа строкой
		file = open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'UTF-8')
		body = file.read()
		file.close()
		lines = body.split('\n')
		old_info = '_'
		for line in lines:
			line = line.replace('\n', '')
			if (str(id) in str(line)):
				old_info = str(line)
		if data != old_info:
			file = open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'w', encoding = 'UTF-8')
			file.write((body.replace(old_info, data)).strip()+'\n')
			file.close()
	except Exception:
		pass


def check_new(user):
	file = open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'a', encoding = 'UTF-8')
	file.write(f'"id" : {user.id}, "task" : "{user.task}", "balans" : {user.balans}, "mode" : "{user.mode}"')
	file.close()


def get_task(user):
	try:
		file = open(f'{tdir(__file__)}/vars.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'UTF-8')
		body = file.readlines()
		file.close()
		
		body = [x.replace('\n', '') for x in body]
		l1 = len(body)
		
		task = body[randint(0, l1)-1]
		return task

	except Exception as e:
		print(e)
		return 'Задания закончились!'


while True:
	for event in longpoll.listen():

		if event.type == VkEventType.MESSAGE_NEW:
			if event.to_me:

				msg = event.text.lower()
				id = event.user_id
				name = session.method('users.get', {'user_ids': id})[0]['first_name']

				# логика
				if msg == 'начать':

					for user in users: # проверка, новый пользователь или старый
						if user.id == id:
							in_users = True

					if in_users: # если пользователь не новый, то мы просто определяем его id и ставим ему mode = 'start'
						user.mode = 'start'
						sender(id, f'Привет, {name}!\nВыберите действие:', key_for_start)

					else:				# если пользователь новый, то мы создаем объект класса, соответсвующий его параметрам(id, mode)
						users.append(User(id = id, task = '', balans = 0, mode = 'start'))
						check_new(users[len(users)-1])
						sender(id, f'Привет, {name}!\nВыберите действие:', key_for_start)

				for user in users:
					update_bd(user)

				else:
					for user in users:
						if id == user.id:

							update_bd(user)


							if user.mode == 'start': # готово
								if msg == 'задания':
									update_bd(user)
									if user.task == '':
										sender(id, f'Получите новое задание!', key_for_main1)
									else:
										sender(id, f'Ваше текущее задание:\n{user.task}', key_for_main2)
									user.mode = 'main'

								if msg == 'баланс':
									sender(id, f'Ваш текущий баланс: {user.balans}', key_for_balans)
									user.mode = 'balans'


							if user.mode == 'main': # готово
								if msg == 'назад':
									sender(id, 'Выберите действие:', key_for_start)
									user.mode = 'start'

								if msg == 'готово':
									update_bd(user)
									if (user.task != '')&(user.task != 'Задания закончились!'):
										if (time.time() - user.last_ok) >= 5:
											user.last_ok = time.time() 
											user.balans += 1
											user.task = ''
											clear_sender(id, 'Вы получили 1 монету!')
											update_bd(user)
											sender(id, 'Выберите действие:', key_for_main3)
										else:
											clear_sender(id, '5 секунд ещё не прошло!')
									else:
										clear_sender(id, 'Сначала нужно выполнить задание!')

								if msg == 'получить задание':
									user.task = get_task(user)
									update_bd(user)
									sender(id, f'Ваше новое задание:\n{user.task}', key_for_main2)

								if msg == 'пропустить':
									user.task = ''
									update_bd(user)
									user.mode = 'start'
									sender(id, 'Выберите действие:', key_for_start)

								if msg == 'получить новое задание':
									user.task = get_task(user)
									update_bd(user)
									sender(id, f'Ваше новое задание:\n{user.task}', key_for_main2)


							if user.mode == 'balans': # готово
								if msg == 'снять':
									sender(id, 'Выберите счёт:', key_in_balans)
									user.mode = 'select'

								if msg == 'назад':
									sender(id, 'Выберите действие:', key_for_start)
									user.mode = 'start'


							if user.mode == 'select': # готово
								if msg == 'сбер':
									user.sber = True
									sender(id, 'Введите номер счета без пробелов:', clear_key)
									user.mode = 'get_account'

								if msg == 'яндекс':
									user.yandex = True
									sender(id, 'Введите номер счета без пробелов:', clear_key)
									user.mode = 'get_account'

								if msg == 'назад':
									sender(id, 'выберите действие:', key_for_start)
									user.mode = 'start'


							if user.mode == 'get_account': # готово
								if not msg in ['яндекс', 'сбер', 'назад', 'задания', 'снять']:
									file = open(f'{tdir(__file__)}/exit.txt'.replace('\\', '/').replace('main.py/', ''), 'a', encoding = 'UTF-8')
									if user.sber:
										file.write(f'Sberbank {msg} : {user.balans}\n')
										sender(admin_id, f'Sberbank {msg} : {user.balans}', clear_key)
									elif user.yandex:
										file.write(f'Yandex {msg} : {user.balans}\n')
										sender(admin_id, f'Sberbank {msg} : {user.balans}', clear_key)
									file.close()
									user.balans = 0
									update_bd(user)
									sender(id, 'Готово, вы добавлены в список выплат!\nВыберите действие:', key_for_start)
									user.mode = 'start'