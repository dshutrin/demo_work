import telebot, time
from config import token, admin_id
from random import randint
from os.path import abspath as tdir

bot = telebot.TeleBot(token)

# клавиатуры

clear_key = telebot.types.ReplyKeyboardMarkup(True)

key_for_start = telebot.types.ReplyKeyboardMarkup(True)
key_for_start.row('Задания', 'Баланс')

key_for_balans = telebot.types.ReplyKeyboardMarkup(True)
key_for_balans.row('Снять', 'Назад')

key_in_balans = telebot.types.ReplyKeyboardMarkup(True)
key_in_balans.row('Сбер', 'Яндекс', 'Назад')
	
key_for_main1 = telebot.types.ReplyKeyboardMarkup(True)
key_for_main1.row('Получить задание', 'Назад')
	
key_for_main2 = telebot.types.ReplyKeyboardMarkup(True)
key_for_main2.row('Готово', 'Пропустить', 'Назад')
	
key_for_main3 = telebot.types.ReplyKeyboardMarkup(True)
key_for_main3.row('Получить новое задание', 'Назад')
	
# клавиатуры


class User():
	def __init__(self, id, task, balans, mode):
		self.id = id # id пользователя
		self.task = task # текущее задание
		self.mode = mode # текущий режим
		self.balans = balans # текущий баланс
		self.yandex = ''
		self.sber = ''
		self.last_ok = 0


file = open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'utf-8')
lines = file.readlines()
file.close()

users = []
try:
	for line in lines:
		line = line.replace('\n', '')
		user = eval(line)
		users.append(User(user['id'], user['task'], user['balans'], user['mode']))
	
except Exception:
	pass

in_users = False
# mods: start / main / balans / select / get_account

def update_bd(user):
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


def check_new(user):
	file = open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'a', encoding = 'UTF-8')
	file.write(f'"id" : {user.id}, "task" : "{user.task}", "balans" : {user.balans}, "mode" : "{user.mode}"')
	file.close()


def get_task():
	try:
		file = open(f'{tdir(__file__)}/vars.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'UTF-8')
		body = file.readlines()
		file.close()
		l1 = len(body)

		body = [x.replace('\n', '') for x in body]
		number = randint(0, l1)
		task = body[number]
		del body[number]

		file = open(f'{tdir(__file__)}/vars.txt'.replace('\\', '/').replace('main.py/', ''), 'w', encoding = 'UTF-8')
		file.write('\n'.join(body).strip())
		file.close()
		return task
	except:
		return 'Задания закончились!'


def sender(id, msg, key):
	bot.send_message(id, msg, reply_markup = key)


@bot.message_handler(content_types=['text'])
def main(message):
	global in_users, users

	id = message.chat.id
	msg = message.text.lower()
	name = message.from_user.first_name

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
								sender(id, 'Вы получили 1 монету!', clear_key)
								update_bd(user)
								sender(id, 'Выберите действие:', key_for_main3)
							else:
								sender(id, '5 секунд ещё не прошло!', clear_key)
						else:
							sender(id, 'Сначала нужно выполнить задание!', clear_key)

					if msg == 'получить задание':
						user.task = get_task()
						update_bd(user)
						sender(id, f'Ваше новое задание:\n{user.task}', key_for_main2)

					if msg == 'пропустить':
						user.task = ''
						user.mode = 'start'
						update_bd(user)
						sender(id, 'Выберите действие:', key_for_start)

					if msg == 'получить новое задание':
						user.task = get_task()
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
	update_bd(user)

bot.polling(none_stop = True)