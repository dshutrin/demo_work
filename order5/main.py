import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from config import tok
from os.path import abspath as tdir


vk_session = vk_api.VkApi(token = tok)
longpoll = VkLongPoll(vk_session)


class User():
	def __init__(self, id, mode, year, need_percent, need_money, access_banks):
		self.id = id
		self.mode = mode
		self.year = year
		self.need_percent = need_percent
		self.need_money = need_money
		self.access_banks = access_banks


class Bank():
	def __init__(self, link, name, age, percent, max):
		self.max = max
		self.link = link
		self.name = name
		self.age = age
		self.percent = percent


def sender(id, text, key):
	vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : key})


def get_keyboard(buts): # функция создания клавиатур
	nb = []
	for i in range(len(buts)):
		nb.append([])
		for k in range(len(buts[i])):
			nb[i].append(None)
	for i in range(len(buts)):
		for k in range(len(buts[i])):
			text = buts[i][k][0]
			color = {'зеленый' : 'positive', 'красный' : 'negative', 'синий' : 'primary'}[buts[i][k][1]]
			nb[i][k] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
	first_keyboard = {'one_time': False, 'buttons': nb, 'inline' : True}
	first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard


def get_down_keyboard(buts): # функция создания клавиатур
	nb = []
	for i in range(len(buts)):
		nb.append([])
		for k in range(len(buts[i])):
			nb[i].append(None)
	for i in range(len(buts)):
		for k in range(len(buts[i])):
			text = buts[i][k][0]
			color = {'зеленый' : 'positive', 'красный' : 'negative', 'синий' : 'primary'}[buts[i][k][1]]
			nb[i][k] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
	first_keyboard = {'one_time': False, 'buttons': nb, 'inline' : False}
	first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard


def get_links(lines):
	nb = []
	for line in lines:
		print(line)
		nb.append([])
		nb[-1].append(
			{
                "action":{
                    "type" : "open_link",
                    "link" : line[1],
                    "label" : line[0]
                },
            }
		)
	nb.append([
		{
            "action":{
               "type":"text",
               "payload":"{\"button\": \"2\"}",
               "label":"Главное меню"
            },
            "color":"primary"
        }
	])
	first_keyboard = {'one_time': False, 'buttons': nb, 'inline' : True}
	first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard


banks = [
	Bank(link = 'https://vk.cc/bYImkX', name = 'Деньги Сразу', 	age = 18, 	percent = 1, 		max = 30000),
	Bank(link = 'https://vk.cc/bZqN1F', name = 'Срочноденьги', 	age = 22, 	percent = 1,		max = 100000),
	Bank(link = 'https://vk.cc/bZqNrS', name = 'Online-Zaim', 	age = 21, 	percent = 1,		max = 30000),
	Bank(link = 'https://vk.cc/bZqNLJ', name = 'Pay P.S.', 		age = 21, 	percent = 1,		max = 50000),
	Bank(link = 'https://vk.cc/bZqNbC', name = 'Доброзайм', 		age = 19, 	percent = [0, 1],	max = 100000),
	Bank(link = 'https://vk.cc/bZqLIN', name = 'Комета Займ', 	age = 18, 	percent = 0,		max = 50000),
	Bank(link = 'https://vk.cc/bYLKmD', name = 'Cashtoyou', 		age = 20, 	percent = 1,		max = 30000),
	Bank(link = 'https://vk.cc/bYBYHB', name = 'Быстроденьги', 	age = 21, 	percent = [0, 1],	max = 30000)
]


def save_bd(users):
	lines = []
	for user in users:
		lines.append(f'"id" : {user.id}, "mode" : "{user.mode}", "year" : {user.year}, "need_percent" : {user.need_percent}, "need_money" : {user.need_money}, "access_banks" : {[]}')
	lines = '\n'.join(lines)
	with open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'w', encoding = 'utf-8') as file:
		file.write(lines)
		file.close()


def read_bd():
	users = []
	with open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'utf-8') as file:
		lines = [x.replace('\n', '') for x in file.readlines()]
		file.close()
	for line in lines:
		line = eval('{' + line + '}')
		if line != '{}':
			users.append(User(id = line["id"], mode = line["mode"], year = line["year"], need_percent = line["need_percent"], need_money = line["need_money"], access_banks = []))
	return users


users = read_bd()

clear_key = get_down_keyboard([
])

menu_key = get_keyboard([
	[('Подобрать займ', 'зеленый')],
	[('Займ под 0%', 'красный')]
])

money_key = get_keyboard([
	[('До 30.000', 'зеленый')],
	[('До 50.000', 'зеленый')],
	[('До 100.000', 'зеленый')],
	[('Главное меню', 'синий')]
])


while True:
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				if event.to_me:

					id = event.user_id
					msg = event.text.lower()

					if msg == 'начать':
						flag = 0
						for user in users:
							if user.id == id:
								flag = 1
								user.mode = 'start'
								break
						if flag == 0:
							users.append(User( id = id, mode = 'start', year = -1, need_percent = None, need_money = None, access_banks = []))
						sender(id, "Выберите действие:", menu_key)

					elif msg == 'главное меню':
						for user in users:
							if user.id == id:
								user.year = -1
								user.need_percent = None
								user.need_money = None
								sender(id, "Выберите действие:", menu_key)
								user.mode = 'start'

					else:
						for user in users:
							if user.id == id:

								if user.mode == 'start':
									if msg == 'подобрать займ':
										user.mode = 'start'
										user.year = -1
										user.need_percent = 100
										user.need_money = None
										sender(id, 'Сколько денег вы хотите получить?', money_key)
										user.mode = 'check1'

									elif msg == 'займ под 0%':
										user.mode = 'start'
										user.year = -1
										user.need_money = None
										user.need_percent = 0
										sender(id, 'Сколько денег вы хотите получить?', money_key)
										user.mode = 'check1'

								elif user.mode == 'check1':
									if msg == 'до 30.000':
										user.need_money = 30000
										sender(id, 'Сколько вам полных лет?\nВедите число:', clear_key)
										user.mode = 'check_age'

									elif msg == 'до 50.000':
										user.need_money = 50000
										sender(id, 'Сколько вам полных лет?\nВедите число:', clear_key)
										user.mode = 'check_age'

									elif msg == 'до 100.000':
										user.need_money = 100000
										sender(id, 'Сколько вам полных лет?\nВедите число:', clear_key)
										user.mode = 'check_age'

									else:
										sender(id, 'Нет таких режимов!\nСколько денег вы хотите получить?', money_key)

								elif user.mode == 'check_age':
									try:
										user.year = int(msg)
										if (user.year < 18):
											sender(id, 'Не найдено сервисов, предоставляющик деньги в займы несовершеннолетним.', menu_key)
											user.mode = 'start'
										else:
											
											user.access_banks = [x for x in banks if (x.age<=user.year)]
											m1 = [x for x in user.access_banks if (str(type(x.percent)) == "<class 'list'>")]
											m1 = [x for x in  m1 if (x.percent[0] <= user.need_percent)]

											m2 = [x for x in user.access_banks if (str(type(x.percent)) == "<class 'int'>")]
											m2 = [x for x in  m2 if (x.percent <= user.need_percent)&(not(x in m1))]

											user.access_banks = m1+m2
											user.access_banks = [x for x in user.access_banks if x.max >= user.need_money]

										if user.access_banks == []:
											sender(id, 'Не удалось подобрать сервис для займа по вашим параметрам.', menu_key)
											user.mode = 'start'

										elif str(type(user.access_banks[0])) == "<class '__main__.Bank'>":
											buts = []
											for x in user.access_banks:
												buts.append([x.name, x.link])
											
											sender(id, 'Вы можете воспользоваться следующими сервисами:', get_links(buts))
											user.mode = 'start'

									except Exception as e:
										print('error')
										sender(id, 'Произошла ошибка, пожалуйста, заполните форму заново.', menu_key)
										user.mode = 'start'
			save_bd(users)

	except Exception as e:
		vk_session = vk_api.VkApi(token = tok)
		longpoll = VkLongPoll(vk_session)