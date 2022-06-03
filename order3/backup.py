from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from os.path import abspath as tdir
from threading import Thread
import vk_api, os, json

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
			users.append(User(id = line["id"], cash = line["cash"]))
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
							if us_id in admins: # если написал админ
								command = msg.replace('/', '').split()[0].strip()
								if msg.replace(f'/{command}', '').strip() == '':
									to = event.object.message['from_id']
								else:
									to = int(msg.replace('/', '').replace('[', '').replace(']', '').replace('|', '').split()[1].split('@')[0].replace('id', '').strip())



								if command == 'del':
									vk_session.method('messages.removeChatUser', {'user_id' : to, 'chat_id' : id})
									send_chat(id, f'Пользователь {to} удален!')

								elif command == 'hi':
									send_chat(id, f'Hello, {vk_session.method("users.get", {"user_ids" : [to]})[0]["first_name"]}!')

								elif command == 'info':
									name = vk_session.method("users.get", {"user_ids" : [us_id]})[0]["first_name"]
									sur_name = vk_session.method("users.get", {"user_ids" : [us_id]})[0]["last_name"]
									for user in users:
										if to == user.id:
											send_chat(id, f'Информация о {name} {sur_name}\ncash: {user.cash}')
											break

								elif command == 'bonus':
									try:
										sum = int(msg.split()[-1])
										if sum:
											for user in users:
												if user.id == to:
													user.cash += sum
													if (sum > 0):
														send_chat(id, f'Добавлено {sum}')
													elif (sum < 0):
														send_chat(id, f'снято {-sum}')
													break
									except Exception:
										send_chat(id, 'Bonus error!')

								elif (command): # если вызвали несуществующую команду
									send_chat(id, f'{vk_session.method("users.get", {"user_ids" : [us_id]})[0]["first_name"]}, такой команды не существует!')



							else: # если команду вызвал не админ
								name = vk_session.method("users.get", {"user_ids" : [us_id]})[0]["first_name"] # получаем имя того, кто вызвал команду
								send_chat(id, f'[id{us_id}|{name}], у вас нет прав доступа к этой команде!')

						else: # если не команда
							if msg == 'привет':
								send_chat(id, 'Пиривет!')
						
						save_chat_bd(users)

		except Exception as e:
			bot_longpoll = VkBotLongPoll(vk_session, 202598138)

Thread(target = chats).start()
Thread(target = ls).start()