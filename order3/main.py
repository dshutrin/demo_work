from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from os.path import abspath as tdir
from threading import Thread
import vk_api, os, json, random


vk_session = vk_api.VkApi(token="b9b988999919f0091601461c5c85c0c3a3202e7350bf65ddc5b239597485e034edfe886db9d4d71364007")


def send_chat(id, text): # отправка сообщения в беседу
	vk_session.method("messages.send", {"chat_id": id, "message": text, "random_id": 0})


def ls_sender(id, text, key): # отправка сообщения в чат (всегда с клавиатурой)
	vk_session.method("messages.send", {"user_id": id, "message": text, "random_id": 0, "keyboard" : key})


class User():
	def __init__(self, id, cash):
		self.id = id
		self.cash = cash


def save_chat_bd(users): # сохранение бд беседы
	lines = []
	for user in users:
		lines.append(f'"id" : {user.id}, "cash" : {user.cash}')
	lines = '\n'.join(lines)
	with open(f'chat_data.txt'.replace('\\', '/').replace('main.py/', ''), 'w', encoding = 'utf-8') as file:
		file.write(lines)
		file.close()


def read_bd(): # считывание бд беседы
	users = []
	with open(f'chat_data.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'utf-8') as file:
		lines = [x.replace('\n', '') for x in file.readlines()]
		file.close()
	for line in lines:
		line = eval('{' + line + '}')
		if line != '{}':
			users.append(User(id = int(line["id"]), cash = int(line["cash"])))
	return users


def read_adm(): # получение админов беседы
	users = []
	with open(f'admins.txt'.replace('\\', '/').replace('main.py/', ''), 'r', encoding = 'utf-8') as file:
		lines = [int(x.replace('\n', '')) for x in file.readlines()]
		file.close()
	return lines


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
	first_keyboard = {'one_time': False, 'buttons': nb, 'inline' : False}
	first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard



clear_key = get_keyboard([])# пустая клавиатура

keyboard1 = get_keyboard([
	[('Привет', 'зеленый'), ('Пока', 'красный')]
])



# добавить команды и кнопки
def ls(): # если сообщение в лс боту
	while True:
		longpoll = VkLongPoll(vk_session)
		try:
			for event in longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW:
					if event.to_me:
						id = event.user_id
						msg = event.text.lower()

						if msg == 'привет':
							ls_sender(id, 'Пиривет!', keyboard1)

						elif msg == 'пока':
							ls_sender(id, 'Ну и пока!', keyboard1)

						else:
							ls_sender(id, msg.upper(), clear_key)

		except Exception:
			longpoll = VkLongPoll(vk_session)




def chats(): # если сообщение в чате
	bot_longpoll = VkBotLongPoll(vk_session, 202598138)
	adm_commands = ['расширить', 'ban']
	us_commands = ['перевод', 'info', 'очко', 'удача']
	admins = read_adm()
	users = read_bd()
	while True:
		try:
			for event in bot_longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.from_chat:
						id = event.chat_id # id чата
						msg = event.object.message['text'].lower()
						us_id = event.object.message['from_id'] # id отправителя
						us_name = vk_session.method("users.get", {"user_ids" : [us_id]})[0]["first_name"] # имя отправителя
						us_sur = vk_session.method("users.get", {"user_ids" : [us_id]})[0]["last_name"] # фамилия отправителя


						#Добавить автоматический парсинг участников
						flag = False
						for user in users:
							if user.id == us_id:
								flag = True
								break
						if flag == False:
							users.append(User(id = us_id, cash = 0))
							send_chat(id, 'added')

						to = ''

						if msg.startswith('/'): # если вызвали команду
							command = msg.split()[0].replace('/', '').strip()
							if (command in us_commands) or (command in adm_commands): # если есть такая команда в списке команд
								print(len(msg.split()))

								for com in us_commands:
									if msg == f'/{com}':
										msg = f'{msg} {us_id}'

								for com in adm_commands:
									if msg == f'/{com}':
										msg = f'{msg} {us_id}'

								print(f'command : {command}')


								if len(msg.split()) == 2:#если команда состоит из 2х частей
									if msg.replace(f'/{command}', '').strip() == '':
										adresant = event.object.message['from_id']
									else:
										adresant = int(msg.replace('/', '').replace('[', '').replace(']', '').replace('|', '').split()[1].split('@')[0].replace('id', '').strip())
									try:
										adr_name = vk_session.method("users.get", {"user_ids" : [adresant]})[0]["first_name"]
										adr_sur = vk_session.method("users.get", {"user_ids" : [adresant]})[0]["last_name"]
									except:
										adr_name = ''
										adr_sur = ''

									# реализация команд

									print(f'y command : "{command}"')

									if command == 'ban': #Доработать
										if us_id in admins: # если написал админ
											if adresant == us_id:
												send_chat(id, f'так нельзя')
												break
											send_chat(id, f'забанили {adresant}')
										else: # если команду вызвал не админ
											name = vk_session.method("users.get", {"user_ids" : [us_id]})[0]["first_name"] # получаем имя того, кто вызвал команду
											send_chat(id, f'[id{us_id}|{name}], у вас нет прав доступа к этой команде!')

									elif command == 'info':
										print(adresant)
										for user in users:
											if user.id == adresant:
												adr_name = vk_session.method("users.get", {"user_ids": [adresant]})[0]["first_name"]
												send_chat(id, f'{adr_name}, размер твоего очка составляет: {user.cash} см.')

									elif command == 'очко':
										print(adresant)
										for user in users:
											if user.id == adresant:
												a = random.randint(5, 15)
												b = random.randint(0, 1)
												c = random.randint(0, 5)
												per = random.randint(0, 10)
												if b == 0:
													if user.cash <= 0:
														user.cash += a
													else:
														if per <= 6:
															a = c
															user.cash -= a
														else:
															user.cash -= a
														send_chat(id, f'{adr_name}, размер твоего очка уменьшился на {a} см.\nТеперь ширина твоего очка составляет {user.cash} см.')
												else:
													if per <= 6:
														a = c
														user.cash += c
													else:
														user.cash += a
													send_chat(id, f'{adr_name}, размер очка увеличился на {a} см.\nТеперь ширина твоего очка составляет {user.cash} см.')
												#send_chat(id, f'Счёт: {user.cash}')


									elif command == 'удача':
										print('вошли! ' + str(msg.split()))
										try:
											var = int(msg.replace(f'/{command}', '').strip())
										except Exception as e:
											print(e)
										send_chat(id, var)
										print(var)
										if (var > user.cash) or (var == 0) or (var < 0):
											send_chat(id, f'А можно руки из жопы вытащить, и написать нормально?')
										else:
											chance = random.randint(1, 100)
											if chance == 51: #Супер приз
												send_chat(id, f'Вы выиграли СУПЕРПРИЗ!')
												winprc = 10
												user.cash = user.cash * (1+winprc)
											else:
												if adresant == user.cash or adresant >= 0.92: #если больше 92% или равно
													if chance <= 10:
														winprc = 2
														user.cash = user.cash * (1+winprc)
														send_chat(id, f'Ты выиграл джекпот!\nТеперь размер твоего очка составляет {user.cash} см!')
													else:
														user.cash = user.cash - adresant
														send_chat(id, f'Ты проиграл.\n Твое очко уменьшилось на {adresant} см, и теперь составляет {user.cash} см.')

												elif adresant / user.cash >= 0.5: #если больше 50%
													if chance <= 25:
														winprc = 1
														user.cash = user.cash * (1 + winprc)
														send_chat(id, f'Ты выиграл!\nТеперь размер твоего очка составляет {user.cash} см!')
													else:
														user.cash = user.cash - adresant
														send_chat(id, f'Ты проиграл.\n Твое очко уменьшилось на {adresant} см, и теперь составляет {user.cash} см.')

												elif adresant / user.cash < 0.5: #если меньше 50%
													if chance <= 40:
														winprc = 0.6
														user.cash = user.cash * (1 + winprc)
														send_chat(id, f'Ты выиграл джекпот!\nТеперь размер твоего очка составляет {user.cash} см!')
													else:
														user.cash = user.cash - adresant
														send_chat(id, f'Ты проиграл.\n Твое очко уменьшилось на {adresant} см, и теперь составляет {user.cash} см.')

									elif (msg.startswith('/расширить')) or (msg.startswith('/перевод')):
										send_chat(id, 'Не корректная команда!')

									else:
										send_chat(id, 'Такой команды не существует!')



								elif len(msg.split()) == 3:#если команда состоит из 3х частей
									ch3 = msg.split()[2]
									if msg.replace(f'/{command}', '').replace(ch3, '').strip() == '':
										adresant = event.object.message['from_id']
									else:
										adresant = int(msg.replace('/', '').replace('[', '').replace(']', '').replace('|', '').split()[1].split('@')[0].replace('id', '').strip())
									adr_name = vk_session.method("users.get", {"user_ids" : [adresant]})[0]["first_name"]
									adr_sur = vk_session.method("users.get", {"user_ids": [adresant]})[0]["last_name"]


									# реализация команд
									if command == 'расширить':
										if us_id in admins:# если написал админ
											ch3 = int(eval(ch3))# int(ch3) т.к. ch3 это сумма бонуса, поэтому нужно преобразовать в int
											if ch3:
												if ch3 > 0:
													for user in users:
														if user.id == adresant:
															user.cash += ch3 
															send_chat(id, f'Очко пользователя {adr_name} {adr_sur} магическим образом расширилось на {ch3} см.\nТеперь ширина его очка составляет {user.cash} см.')
												elif ch3 < 0:
													for user in users:
														if user.id == adresant:
															user.cash -= ch3*-1
															send_chat(id, f'Очко пользователя {adr_name} {adr_sur} сжалось само по себе на {ch3*-1} см.\nТеперь ширина его очка составляет {user.cash} см.')
												else:
													send_chat(id, 'Некорректный бонус!')
											else:
												send_chat(id, 'Некорректный бонус!')
										else:# если команду вызвал не админ
											name = vk_session.method("users.get", {"user_ids" : [us_id]})[0]["first_name"] # получаем имя того, кто вызвал команду
											send_chat(id, f'[id{us_id}|{name}], у вас нет прав доступа к этой команде!')

							else:
								send_chat(id, 'Такой команды не существует!')

						else:# если не команда
							nameparse = vk_session.method("users.get", {"user_ids": [us_id]})[0]["first_name"]
							idchat = event.chat_id
							print([us_id][0],idchat,':',nameparse,' >>> ',msg)
							if msg == 'привет':
								send_chat(id, 'Пиривет!')
						
						save_chat_bd(users)

		except Exception as e:
			bot_longpoll = VkBotLongPoll(vk_session, 202598138)

Thread(target = chats).start()
Thread(target = ls).start()