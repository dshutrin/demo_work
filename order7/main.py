import json, vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import tok
import datetime, time


def read_bd():
	with open('data.json', 'r', encoding = 'utf-8') as file:
		data = json.load(file)
	return data


def write(data):
	data = json.dumps(data)
	data = json.loads(str(data))
	with open('data.json', 'w', encoding = 'utf-8') as file:
		json.dump(data, file, indent = 4)


def generate_data(names, message, last_clear_logs, bans, lock_words, history):
	return {'message' : message, 'admin_id' : ADMIN_ID, 'group_id' : GROUP_ID, 'last_clear_logs' : last_clear_logs, 'users' : names, 'banned' : bans, 'lock_words' : lock_words, 'history' : history}


def sender(id, text):
	vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'random_id' : 0})


def check_moder(id, names):
	for user in names:
		if user['id'] == id:
			if (user['moder'] == 1) or (id == ADMIN_ID):
				return 1
	return 0


def get_info(id):
	ans = vk_session.method('users.get', {'user_id' : id, 'name_case' : 'Nom'})[0]
	ans = f"{ans['first_name']} {ans['last_name']}"
	return ans


def check_link(id, msg):
	flag = 0
	if (id != ADMIN_ID) and (check_moder(id, names) == 0):
		if ('http://vk.com' in msg.lower()) or ('https://vk.com' in msg.lower()):
			flag = 1
		if ('[' in msg) and ('|@' in msg) and (']' in msg) and (not('[club189277936|@awpservermrd]' in msg.lower())):
			flag = 1
	return flag


def search_man(id):
	flag = 0
	for user in names:
		if user['id'] == id:
			flag = 1
			break
	return flag


def logging(id, msg):
	with open('logs.txt', 'a', encoding='utf-8') as file:
		file.write(f'Пользователь {get_info(id)} воспользовался командой <{msg}> | {datetime.datetime.now()}\n')


def get_logs():
	with open('logs.txt', 'r', encoding='utf-8') as file:
		data = file.read()
	return data


def clear_logs():
	with open('logs.txt', 'w', encoding='utf-8') as file:
		pass


class MyLongPoll(VkBotLongPoll):
	def listen(self):
		while True:
			try:
				for event in self.check():
					yield event
			except Exception as e:
				pass


data = read_bd()

last_clear_logs = data['last_clear_logs']
names = data['users']
info_message = data['message']
bans = data['banned']
lock_words = data['lock_words']
ADMIN_ID = data['admin_id']
GROUP_ID = data['group_id']
history = data['history']


vk_session = vk_api.VkApi(token = tok)
longpoll = MyLongPoll(vk_session, GROUP_ID)


def check_in_chat(id, chat_id):
	return (id in [x['member_id'] for x in vk_session.method('messages.getConversationMembers', {'peer_id' : 2000000000+chat_id})['items']])


var1 = """
🌐Информирование всех общих команд бота от сервера [club189277936|@awpservermrd]

📃Команда №1:
/mutedelmessage — данная команда выдает блокировку чата пользователю, нарушающего правила беседы, и бот удаляет автоматически его новые сообщения.

📄Команда №2:
/unmutedelmessage — данной командой администратор или модератор беседы может снять блокировку с пользователя, который нарушил правила беседы.

📑Команда №3:
/block — (ссылка на профиль). Администраторы и модераторы — могут банить игроков навсегда за нарушения правил беседы с помощи команды /block и ссылка на страницу vk - нарушителя.

📰Команда №4:
/bindingmoderor — данной командой администратор может добавить модератора, которому будет доступен весь функционал бота. Также, назначенный модератор беседы — может добавлять данной командой других модераторов для руководства.

📃Команда №5:
/delmoderor — данной командой администратор может снять с должности любого модератора.Также, модераторы могут снимать друг друга лишив права пользования высоким функционалом бота.

📄Команда №6:
/insertforbiddenword — данной командой администратор или модератор могут занести в фильтр слова, которые будут блокироваться у обычных пользователей беседы. Бот автоматически удаляет запрещенные слова и выдает предупреждение.

📑Команда №7:
/listwordslocks — данной командой все пользователи могут посмотреть заблокированные слова в беседе.

📰Команда №8:
/dellistout — данная команда удаляет запрещенные слова из фильтра запрещенных слов. /dellistout text.

📄Команда №9:
/inlistmoderor — данной командой можно посмотреть список всех действующих модераторов в беседе.

📑Команда №10:
Ник — данной командой можно установить свой персональный NickName в беседе. Чтобы установить, напишите слово Ник, нажмите пробел и напишите ник. Пример: Ник EAVC.

📃Команда №11:
Ники — данная команда информирует всех игроков в беседе о том, кто зарегистрирован в системе ников.

📄Команда №12:
Правила — данная команда информирует о общем положении правил в беседе всех пользователей. Ссылка на пункты.

📰Команда №13:
Команду set_info <text> — могут писать администраторы и модераторы, чтобы задать любую информацию на отдельную и доступную для всех команду info. Информация может редактироваться в любое время.

📑Команда №14:
ip — данная команда показывает ip и port сервера на который можно зайти. Достаточно в игре консоли написать connect и ip+port

📃Команда №15:
руководители — данной командой выводится всё руководство сервера @awpservermrd

📄Команда №16:
/teamformanagerslist — данная команда предназначена для администраторов и модераторов данной беседы. Это подробная статья их инструментов для работы/команд.

📰Команда №17:
/teamsforuserbot — данная команда боту предназначена для всей структуры общества людей, которая находится в беседе. Это подробная статься, с помощи которой — можно посмотреть команды обычным пользователям.

📑Команда №18:
/generalteaminfobot — данной командой можно посмотреть всю информацию по командам. Справка подробной информации с описанием.

📑Команда №19:
/sourcebans - данные Банов/мутов игроков с сервера [club189277936|@awpservermrd]
Ссылка: http://web.parlahost.ru/sb/kirichbsk/index.php?p=banlist

🧾Команда №20:
/delviolation — данная команда предназначена администраторам и модераторам. С помощи данного инструмента, администрация сервера может удалить сообщения пользователя, который нарушил правила обще-пользовательской беседы. Примечание: Выделить сообщение нарушителя и прописать команду.

📄Команда №21:
/botteamlogging — данная команда выводит полное логирование действий в обще-пользовательской беседе. Log - бызы удаляется каждые 3 дня автоматически.

📄Команда №22:
/rankandlogchat — данная команда делает вывод ранговых внутриигровых показателей с сервера на каждого игрока. Так же, команда выводит логирование чата из игры. Показывается вся отчетность в Web - панели по ссылке.

📄Команда №23:
/demo — данная команда предназначена для того, чтобы Вы могли скачать записи демо с сервера @awpservermrd Запись игрового процесса (геймплея) компьютерной игры средствами самой игры!
"""

var2 = '''
✔Инструменты для работы - команды боту для администраторов и модераторов [club189277936|@awpservermrd]:
1) команды "/block", "/mutedelmessage", "/unmutedelmessage" - используется при ответе на сообщение
2) команда "/insertforbiddenword <фраза/слово>" - запретить использование фразы/слова
3) команда "set_info <text>" - утановить информацию для команды info
4) команды "/bindingmoderor" и "/delmoderor" - даёт и снимает статус модератора
5) команда "/sourcebans" - данные Банов/мутов игроков с сервера [club189277936|@awpservermrd]\nСсылка: http://web.parlahost.ru/sb/kirichbsk/index.php?p=banlist
6) команда "/delviolation" - С помощи данного инструмента, администрация сервера может удалить сообщения пользователя, который нарушил правила обще-пользовательской беседы. Примечание: Выделить сообщение нарушителя и прописать команду.
'''

var3 = '''
Создатель проекта: https://vk.com/basisspace (ник в игре: EAVC)
Тех/разработчик проекта: https://vk.com/daniil.agarkov (ник в игре: danil253467)
Гл.руководитель проекта: https://vk.com/id620449697 (Ник в игре: MaxBronz)
Комментатор турниров проекта [club189277936|@awpservermrd]:
https://vk.com/katayamas (Ник в игре: wiski aka sarven)

Администраторы сервера:
1) https://vk.com/wasbka (Ник в игре: Waso)
2) https://vk.com/troyanov_1999 (Ник в игре Sasha)
3) https://vk.com/leon.shuez (Ник в игре: LEON ®)
4) https://vk.com/maks_petlqra1996 (Ник в игре: АУЕ)
5) https://vk.com/spirempti03 (Ник в игре: Spirempti)
6) https://vk.com/lizzzochkaaa_fujoirxl (Ник в игре: elsie)
7) https://vk.com/id636322697 (Ник в игре: ПОТЕРЯЙСЯ)
'''
var4 = '''_'''


var5 = '''

📌Список команд боту от пользователей:

1) Команда "Ник" — данной командой можно установить свой персональный NickName в беседе. Чтобы установить, напишите, пожалуйста, слово Ник, нажмите пробел и напишите ник. Пример: Ник EAVC.

2) Команда "Ники" — данная команда информирует всех игроков в беседе о том, кто зарегистрирован в системе ников.

3) Командой "руководители" — выводится всё руководство сервера @awpservermrd

4) Команда "info" - показывает для пользователей информацию, установленную администратором или модератором.

5) Команда "ip" - показать ip игрового сервера.

6) Команда "/listwordslocks" - посмотреть список запрещённых слов/фраз в фильтре.

7) команда "правила" - показать правила сообщества

8) команда "/sourcebans" - данные Банов/мутов игроков с сервера [club189277936|@awpservermrd]\nСсылка: http://web.parlahost.ru/sb/kirichbsk/index.php?p=banlist
'''


while True:
	try:
		for event in longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if (event.from_chat):

					if (time.time() - last_clear_logs) >= (60*60*24*3):
						clear_logs()
						last_clear_logs = time.time()

					id = event.object.message['from_id']
					msg = event.object.message['text']


					if (search_man(id) == 0) and (id > 0):
						names.append({'name' : '', 'id' : id, 'moder' : 0})


					if check_link(id, msg) == 1:
						try:
							vk_session.method('messages.delete', {'delete_for_all' : 1, 'peer_id' : event.object.message['peer_id'], 'conversation_message_ids' : [event.object.message['conversation_message_id']]})
						except Exception as e:
							pass
						sender(event.chat_id, f'❌[id{id}|{get_info(id)}], Вам выдана блокировка чата за спам! Максимально-возможное количество отправленных сообщений "10" — подряд. Ваши сообщения будут удаляться автоматически ботом сервера @awpservermrd , пока кто-то из других пользователей не напишет в данную беседу после ваших сообщений. [club189277936|@awpservermrd]')


					dey = None
					invite_id = None
					try:
						dey = event.message.action['type']
						invite_id = event.message.action['member_id']
					except Exception as e:
						dey = None
						invite_id = None


					if dey in ('chat_invite_user', 'chat_invite_user_by_link'):
						sender(event.chat_id, f'''🔰Здравствуйте, [id{invite_id}|{get_info(invite_id)}]
— Мы рады Вас приветствовать в беседе сервера!
📩С уважением,
[club189277936|@awpservermrd]

❗Ознакомьтесь, пожалуйста, с правилами беседы для общего пользования: https://vk.com/topic-189277936_40429053

☑ Архив записи демо с сервера: awpmrd.cssold.ru

📌Материал для общего пользования:

👁‍🗨Данной командой /teamsforuserbot — вы можете вызвать в любое время подробную информацию о доступных для всех пользователей команд Бота.

Примечание для модераторов:
📝Данной командой /generalteaminfobot — можно посмотреть всю информацию по командам. Справка подробной информации с описанием.
Модераторам и администраторам — доступны все команды для работы без ограничений.

— Для подключения к серверу: connect 109.237.109.80:27021 — в консоль cs:source''')



					else:
						if len(history) > 9:
							flag = 1
							for i in history:
								if (i != id):
									flag = 0
						else:
							flag = 0


						if (flag == 1):
							if (id != ADMIN_ID) and (check_moder(id, names) == 0):
								try:
									vk_session.method('messages.delete', {'delete_for_all' : 1, 'peer_id' : event.object.message['peer_id'], 'conversation_message_ids' : [event.object.message['conversation_message_id']]})
									sender(event.chat_id, f'❌[id{id}|{get_info(id)}], Вам выдана блокировка чата за спам! Максимально-возможное количество отправленных сообщений "10" — подряд. Ваши сообщения будут удаляться автоматически ботом сервера [club189277936|@awpservermrd] , пока кто-то из других пользователей не напишет в данную беседу после ваших сообщений.')
								except Exception as e:
									pass
								flag = 0

						history.append(id)
						if (len(history) > 10):
							history = history[len(history)-10:len(history)]



						# для админов
						if flag == 0:
							if (id == ADMIN_ID) or (check_moder(id, names) == 1):
								if ('reply_message' in event.object.message) and (event.object.message['reply_message']['from_id'] != ADMIN_ID):


									if msg.lower() == '/mutedelmessage':
										logging(id, msg)
										if not(event.object.message['reply_message']['from_id'] in bans):
											bans.append(event.object.message['reply_message']['from_id'])
											sender(event.chat_id, f"Пользователь @id{event.object.message['reply_message']['from_id']} заблокирован!")
										else:
											sender(event.chat_id, f"Пользователь @id{event.object.message['reply_message']['from_id']} уже заблокирован!")


									elif msg.lower() == '/delviolation':
										logging(id, msg)
										if (check_moder(event.object.message['reply_message']['from_id'], names) == 0):
											try:
												vk_session.method('messages.delete', {'delete_for_all' : 1, 'peer_id' : event.object.message['peer_id'], 'conversation_message_ids' : [event.object.message['reply_message']['conversation_message_id']]})
												sender(event.chat_id, f"⛔ [id{event.object.message['reply_message']['from_id']}|{get_info(event.object.message['reply_message']['from_id'])}], ваше сообщение удалено администрацией [club189277936|@awpservermrd] — за нарушение правил данной обще-пользовательской беседы.")
											except Exception as e:
												pass

									elif (msg.lower().split()[0] in ['ник', 'nick']) and ('reply_message' in event.object.message):
										logging(id, msg)
										name = msg.replace(msg.split()[0], '').strip()
										print(name)
										if (1 <= len(name) <= 15):
											for user in names:
												if user['id'] == event.object.message['reply_message']['from_id']:
													user['name'] = name
													sender(event.chat_id, f"⚙Ник [id{event.object.message['reply_message']['from_id']}|{get_info(event.object.message['reply_message']['from_id'])}] установлен ({user['name']})!")
										else:
											sender(event.chat_id, '📝Ник должен содержать от 1 до 15 символов!')


									elif msg.lower() == '/unmutedelmessage':
										logging(id, msg)
										if event.object.message['reply_message']['from_id'] in bans:
											del bans[bans.index(event.object.message['reply_message']['from_id'])]
											sender(event.chat_id, f"Пользователь @id{event.object.message['reply_message']['from_id']} разблокирован!")
										else:
											sender(event.chat_id, 'Пользователь сейчас не в муте!')


									elif msg.lower() == '/block':
										logging(id, msg)
										print('1')
										vk_session.method('messages.removeChatUser', {'chat_id' : event.chat_id, 'user_id' : event.object.message['reply_message']['from_id']})
										sender(event.chat_id, f"⛔Пользователь [id{event.object.message['reply_message']['from_id']}|{get_info(event.object.message['reply_message']['from_id'])}] — был заблокирован администрацией сервера.\nЕсли есть вопросы ,пожалуйста, создайте обращение в личные сообщения сообщества: [club189277936|@awpservermrd]")


									elif msg.lower() == '/bindingmoderor':
										logging(id, msg)
										flag = 0
										for user in names:
											if user['id'] == event.object.message['reply_message']['from_id']:
												flag = 1
												if user['moder'] == 0:
													user['moder'] = 1
													sender(event.chat_id, f"♻[id{event.object.message['reply_message']['from_id']}|{get_info(event.object.message['reply_message']['from_id'])}] -- теперь модератор!")
												else:
													sender(event.chat_id, f"♻[id{event.object.message['reply_message']['from_id']}|{get_info(event.object.message['reply_message']['from_id'])}] уже является модератором!")
												break
										if flag == 0:
											sender(id, f"♻[id{event.object.message['reply_message']['from_id']}|{get_info(event.object.message['reply_message']['from_id'])}] еще не установил ник!")


									elif msg.lower() == '/delmoderor':
										logging(id, msg)
										flag = 0
										for user in names:
											if user['id'] == event.object.message['reply_message']['from_id']:
												flag = 1
												if user['moder'] == 1:
													user['moder'] = 0
													sender(event.chat_id, f"⛔[id{event.object.message['reply_message']['from_id']}|{get_info(event.object.message['reply_message']['from_id'])}] -- больше не модератор!")
												else:
													sender(event.chat_id, 'Пользователь ещё не является модератором!')
												break
										if flag == 0:
											sender(id, 'Пользователь еще не установил ник!')


								elif msg.lower().startswith('/dellistout '):
									logging(id, msg)
									val = msg.replace('/dellistout ', '', 1).strip()
									if val:
										if val in lock_words:
											del lock_words[lock_words.index(val)]
											sender(event.chat_id, 'Слово удалено из списка запрещённых!')
									else:
										sender(event.chat_id, 'Для использования данной команды необходимо включить в сообщение слово из списка исключений!')


								elif msg.lower().startswith('/insertforbiddenword '):
									logging(id, msg)
									msg = msg.replace('/insertforbiddenword ', '', 1).strip()
									lock_words.append(msg)
									sender(event.chat_id, f'Слово {msg.lower()} внесено в список запрещённых!')


								elif msg.lower() == '/teamformanagerslist':
									logging(id, msg)
									if (id == ADMIN_ID) or (check_moder(id, names)):
										sender(event.chat_id, var2)


								if msg.lower().startswith('set_info'):
									logging(id, msg)
									msg = msg.replace(msg.split()[0], '', 1).strip()
									info_message = msg
									sender(event.chat_id, f'💡⚙Новая информация в беседе: {info_message}')


								elif msg.lower().startswith('/block'):
									logging(id, msg)
									print('2')
									if msg.replace(msg.split()[0], '', 1) != '':
										link = msg.replace(msg.split()[0], '', 1).strip()
										s_id = ''
										start = -1; end = -1
										for i in range(len(link)):
											if link[i] == '[':
												start = i
											if link[i] == '|':
												end = i
												break
										s_id = int(link[start+3:end])
										if (check_moder(id, names) == 1):
											vk_session.method('messages.removeChatUser', {'chat_id' : event.chat_id, 'user_id' : s_id})
											sender(event.chat_id, f"Пользователь [@id{s_id}|{get_info(s_id)}] — был заблокирован администрацией сервера.\nЕсли есть вопросы ,пожалуйста, создайте обращение в личные сообщения сообщества: [club189277936|@awpservermrd]")


								elif msg.lower().startswith('/mutedelmessage'):
									logging(id, msg)
									if msg.replace(msg.split()[0], '', 1) != '':
										link = msg.replace(msg.split()[0], '', 1).strip()
										s_id = ''
										start = -1; end = -1
										for i in range(len(link)):
											if link[i] == '[':
												start = i
											if link[i] == '|':
												end = i
												break
										s_id = None
										try:
											s_id = int(link[start+3:end])
										except Exception as e:
											s_id = None
										if (s_id):
											if not(s_id in bans):
												bans.append(s_id)
												sender(event.chat_id, f"Пользователь @id{s_id} заблокирован!")
											else:
												sender(event.chat_id, f"Пользователь @id{s_id} уже заблокирован!")
										else:
											sender(event.chat_id, 'Нужно указать пользователя!')


								elif msg.lower().startswith('/unmutedelmessage'):
									logging(id, msg)
									if msg.replace(msg.split()[0], '', 1) != '':
										link = msg.replace(msg.split(' ')[0], '', 1).strip()
										s_id = ''
										start = -1; end = -1
										for i in range(len(link)):
											if link[i] == '[':
												start = i
											if link[i] == '|':
												end = i
												break
										s_id = int(link[start+3:end])
										if s_id in bans:
											del bans[bans.index(s_id)]
											sender(event.chat_id, f"Пользователь @id{s_id} разблокирован!")
										else:
											sender(event.chat_id, 'Пользователь сейчас не в муте!')


							if (id != ADMIN_ID) and (check_moder(id, names) == 0):
								for word in lock_words:
									if (word.lower() in msg.lower()) and (not(event.object.message['text'].startswith('/insertforbiddenword '))) and (event.object.message['text'].lower() != ('/listwordslocks')):
										vk_session.method('messages.delete', {'delete_for_all' : 1, 'peer_id' : event.object.message['peer_id'], 'conversation_message_ids' : [event.object.message['conversation_message_id']]})
										sender(event.chat_id, f'⛔Пользователь @id{id} получает предупреждение за использование запрещённых слов!')


							if not(id in bans):#для всех

								if check_moder(id, names) == 0:
									if '@all' in msg:
										sender(event.chat_id, f'''[id{id}|{get_info(id)}]🔒Вы не можете в данной беседе через команду (@all) уведомление — отправлять информацию всем пользователям!
																	Примечание: 🔓Доступно только администраторам и модераторам [club189277936|@awpservermrd]''')
										vk_session.method('messages.delete', {'delete_for_all' : 1, 'peer_id' : event.object.message['peer_id'], 'conversation_message_ids' : [event.object.message['conversation_message_id']]})

								if msg.lower() == '/generalteaminfobot':
									try:
										logging(id, msg)
										sender(event.chat_id, var1)
									except Exception as e:
										print(e)

								elif msg.lower() == '/inlistmoderor':
									logging(id, msg)
									ans = '📃Список модераторов:'
									for user in names:
										if user['moder'] == 1:
											ans = f'{ans}\n[@id{user["id"]}|{get_info(user["id"])}]'
									sender(event.chat_id, ans)

								elif (msg.strip() != '') and (msg.split()[0] in ['ник', 'Ник', 'nick', 'Nick']) and not(('reply_message' in event.object.message)) and (msg.replace(msg.split()[0], '', 1).strip() != '') and (msg.lower().strip() != 'ник'):
									logging(id, msg)
									if (1 <= len(msg.replace(msg.split()[0], '', 1).strip()) <= 15):
										flag = 0
										for user in names:
											if user['id'] == id:
												user['name'] = msg.replace(msg.split()[0], '', 1).strip()
												sender(event.chat_id, f'✅@id{id}, вы успешно сменили ник!')
												flag = 1
										if (flag == 0) and (id > 0):
											names.append({'name' : msg.replace(msg.split()[0], '', 1).strip(), 'id' : id, 'moder' : 0})
											sender(event.chat_id, '✅Вы зарегистрировали новый ник!')
									else:
										sender(event.chat_id, '📝Ник должен содержать от 1 до 15 символов!')

								elif (msg.lower().strip() == 'ник') and ('reply_message' in event.object.message):
									logging(id, msg)
									for user in names:
										if (user['id'] == event.object.message['reply_message']['from_id']):
											if user['name']:
												sender(event.chat_id, f'📝Ник данного пользователя: {user["name"]}')
											else:
												sender(event.chat_id, f'📝У данного пользователя нет ника!')

								elif msg.lower() == 'правила':
									logging(id, msg)
									sender(event.chat_id, 'Правила беседы: https://vk.com/topic-189277936_40429053\nСообщество: https://vk.com/awpservermrd')

								elif msg.lower() == 'ники':
									logging(id, msg)
									names = [x for x in names if check_in_chat(x['id'], event.chat_id)]
									ans = '📒Текущие ники игроков с сервера [club189277936|@awpservermrd]:'
									for user in names:
										if (user['name']) and (check_in_chat(event.object.message['from_id'], event.chat_id)):
											ans = f'{ans}\n{get_info(user["id"])} - {user["name"]}'
									sender(event.chat_id, ans)

								elif msg.lower() in ['/sourcebans', '/source bans']:
									logging(id, msg)
									sender(event.chat_id, 'Данные Банов/мутов игроков с сервера [club189277936|@awpservermrd]\nСсылка: http://web.parlahost.ru/sb/kirichbsk/index.php?p=banlist')

								elif msg in ["/ip", "!ip", 'ip']:
									logging(id, msg)
									sender(event.chat_id, "Для подключения к серверу: connect 109.237.109.80:27021 — в консоль cs:source")

								elif msg.lower() == '/listwordslocks':
									logging(id, msg)
									sender(event.chat_id, '💬Запрещённые слова:\n' + '\n'.join(lock_words))

								elif msg.lower() == 'info':
									logging(id, msg)
									sender(event.chat_id, f'📂[club189277936|@awpservermrd]\nИнформация от администрации:\n{info_message}')

								elif msg.lower() == 'руководители':
									logging(id, msg)
									sender(event.chat_id, var3)

								elif msg.lower() == 'администраторы':
									logging(id, msg)
									sender(event.chat_id, var4)

								elif msg.lower() == '/teamsforuserbot':
									logging(id, msg)
									sender(event.chat_id, var5)

								elif msg.lower() == '/botteamlogging':
									logging(id, msg)
									sender(event.chat_id, get_logs())

								elif msg.lower() == '/rankandlogchat':
									logging(id, msg)
									sender(event.chat_id, '📉Ранговые внутриигровые показатели и логирование чата с сервера: awpmrd.cssold.ru/rankandlogchat')

								elif msg.lower() in ('/demo', 'демо'):
									logging(id, msg)
									sender(event.chat_id, '‼Скачайте Демо-записи с сервера: awpmrd.cssold.ru')


							else:
								try:
									vk_session.method('messages.delete', {'delete_for_all' : 1, 'peer_id' : event.object.message['peer_id'], 'conversation_message_ids' : [event.object.message['conversation_message_id']]})
									sender(event.chat_id, f'[ @id{id} | {get_info(id)} ] - Пользователь заблокирован системой мут!')
								except Exception as e:
									pass

					write(generate_data(names, info_message, last_clear_logs, bans, lock_words, history))
	except Exception as e:
		print(e)