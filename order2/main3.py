import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from time import sleep, time
from datetime import datetime as date
from threading import Thread
from os.path import abspath as tdir

tok = '916c86592d4ae25db789f4534d8dd2cbf90a4ace673cb4fac1a05825dfcae098496a5215f42bc657745ec'
vk_session = vk_api.VkApi(token = tok)
longpoll = VkLongPoll(vk_session)

class User():
	def __init__(self, minion_level, id, mode, is_work, money, pol, energy, level, count5, count10, count15, coal, pers_name, last_minion_work, to_sleep, minion_evo, axe_level, oak, oak_limit, sklad_level, pick_level):
		self.last_minion_work = last_minion_work
		self.minion_level = minion_level
		self.sklad_level = sklad_level
		self.minion_evo = minion_evo
		self.pick_level = pick_level
		self.pers_name = pers_name
		self.axe_level = axe_level
		self.oak_limit = oak_limit
		self.to_sleep = to_sleep
		self.count10 = count10
		self.count15 = count15
		self.is_work = is_work
		self.energy = energy
		self.count5 = count5
		self.level = level
		self.money = money
		self.mode = mode
		self.coal = coal
		self.pol = pol
		self.oak = oak
		self.id = id

def check_registration(id):
	members = vk_session.method('groups.getMembers', {'group_id' : 188446752})['items']
	return (id in members)

def save_bd(users):
	lines = []
	for user in users:
		lines.append(f'"minion_level" : {user.minion_level}, "to_sleep" : {user.to_sleep}, "is_work" : {user.is_work}, "pick_level" : {user.pick_level}, "axe_level" : {user.axe_level}, "sklad_level" : {user.sklad_level}, "oak_limit" : {user.oak_limit}, "oak" : {user.oak}, "minion_evo" : {user.minion_evo}, "last_minion_work" : {user.last_minion_work}, "id" : {user.id}, "mode" : "{user.mode}", "money" : {user.money},  "pol" : "{user.pol}",  "energy" : {user.energy},  "level" : {user.level},"count5" : {user.count5},  "count10" : {user.count10},  "count15" : {user.count15}, "coal" : {user.coal}, "pers_name" : "{user.pers_name}"')
	lines = '\n'.join(lines)
	with open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main3.py/', ''), 'w', encoding = 'utf-8') as file:
		file.write(lines)
		file.close()

def read_bd():
	users = []
	with open(f'{tdir(__file__)}/data.txt'.replace('\\', '/').replace('main3.py/', ''), 'r', encoding = 'utf-8') as file:
		lines = [x.replace('\n', '') for x in file.readlines()]
		file.close()
	for line in lines:
		line = eval('{' + line + '}')
		if line != '{}':
			users.append(User(minion_level = line['minion_level'], to_sleep = line['to_sleep'], is_work = line['is_work'], axe_level = line['axe_level'], pick_level = line['pick_level'], sklad_level = line['sklad_level'], oak_limit = line['oak_limit'], oak = line['oak'], minion_evo = line['minion_evo'], last_minion_work = line['last_minion_work'], id = line['id'], mode = line['mode'], money = line['money'], pol = line['pol'], energy = line['energy'], level = line['level'], count5 = line['count5'], count10 = line['count10'], count15 = line['count15'], coal = line['coal'], pers_name = line['pers_name']))
	return users

def get_keyboard(buts): # функция создания клавиатур
	nb = []
	color = ''
	for i in range(len(buts)):
		nb.append([])
		for k in range(len(buts[i])):
			nb[i].append(None)
	for i in range(len(buts)):
		for k in range(len(buts[i])):
			text = buts[i][k][0]
			color = {'зеленый' : 'positive', 'красный' : 'negative', 'синий' : 'primary', 'белый' : 'secondary'}[buts[i][k][1]]
			nb[i][k] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
	first_keyboard = {'one_time': False, 'buttons': nb}
	first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard

def sender(id, text, key):
	vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : key, 'dont_parse_links' : 1})

reg_key = get_keyboard([
	[('Мужской', 'белый'), ('Женский', 'белый')]
])

lv1_menu_key = get_keyboard([
	[('Работа', 'белый'), ('Персонаж', 'белый')]
])

lv2_menu_key = get_keyboard([
	[('Работа', 'белый'), ('Персонаж', 'белый'), ('Миньон', 'белый')]
])

pers_key = get_keyboard([
	[('Статистика', 'белый'), ('Назад', 'красный')]
])

time_key_lv1 = get_keyboard([
	[('5сек', 'белый'), ('10сек', 'белый'), ('15сек', 'белый')],
	[('Назад', 'красный')]
])

time_key_lv2 = get_keyboard([
	[('10сек', 'белый'), ('15сек', 'белый'), ('20сек', 'белый')],
	[('Назад', 'красный')]
])

time_key_lv3 = get_keyboard([
	[('15сек', 'белый'), ('20сек', 'белый'), ('25сек', 'белый')],
	[('Назад', 'красный')]
])

to2lvl_key = get_keyboard([
	[('Перейти на 2й уровень', 'зеленый')]
])

to3lvl_key = get_keyboard([
	[('Перейти на 3й уровень', 'зеленый')]
])

minion_menu = get_keyboard([
	[('Улучшить', 'белый'), ('Статистика', 'белый')],
	[('Назад', 'красный')]
])

buy_minion_key = get_keyboard([
	[('Купить миньона', 'зеленый'), ('Назад', 'красный')]
])

ask_key = get_keyboard([
	[('Улучшить', 'зеленый'), ('Отмена', 'красный')]
])

evo_minion_key = get_keyboard([
	[('Эволюция', 'зеленый'), ('Назад', 'красный')]
])

lv3_menu_key = get_keyboard([
	[('Работа', 'белый'), ('Персонаж', 'белый'), ('Миньон', 'белый')],
	[('Лес', 'белый')]
])

forest_menu_key = get_keyboard([
	[('Рубить дуб', 'белый'), ('Назад', 'красный')]
])

buy_axe_key = get_keyboard([
	[('Купить топор', 'белый'), ('Назад', 'красный')]
])

to4lvl_key = get_keyboard([
	[('Перейти на 4й уровень', 'зеленый')]
])

lv4_menu_key = get_keyboard([
	[('Шахта', 'белый'), ('Персонаж', 'белый'), ('Миньон', 'белый')],
	[('Лес', 'белый'), ('Дом', 'белый')]
])

buy_pick_key = get_keyboard([
	[('Купить кирку', 'зеленый'), ('Назад', 'красный')]
])

mine_menu_key = get_keyboard([
	[('Добывать уголь', 'белый'), ('Назад', 'красный')]
])

house_menu_key = get_keyboard([
	[('Спать', 'белый'), ('Хранилище', 'белый')],
	[('Назад', 'красный')]
])

sklad_menu_key = get_keyboard([
	[('Улучшить', 'зеленый'), ('Назад', 'красный')]
])

buy_sklad_key = get_keyboard([
	[('Построить хранилище', 'зеленый'), ('Назад', 'красный')]
])

stand_up_key = get_keyboard([
	[('Проснуться', 'зеленый')]
])

clear_key = get_keyboard([])

menus = {1 : lv1_menu_key, 2 : lv2_menu_key, 3 : lv3_menu_key, 4 : lv4_menu_key}
minion_level_cash = 			{0 : {0 : 70, 1 : 90, 2 : 120}, 1 : {1 : 90, 2 : 120}}
minion_cash_from_evo_level = 	{0 : {0 : 0, 1 : 0, 2 : 0, 3 : 0}, 1 : {1 : 0, 2 : 1, 3 : 2}}
minion_energy_from_evo_level = 	{0 : {0 : 0, 1 : 3, 2 : 6, 3 : 9}, 1 : {1 : 6, 2 : 9, 3 : 12}}
users = read_bd()

predel = 1

def get_coal(id): # добыча угля (поток) для каждого запускается отдельно
	global users
	for user in users:
		if user.id == id:
			sleep(30)
			user.coal += 1
			sender(id, 'Добыча угля завершена, вы получили 1 уголь!\nВыберите действие:', mine_menu_key)
			save_bd(users)

def forest_render(id): # добыча дуба (поток) для каждого запускается отдельно
	global users
	for user in users:
		if user.id == id:
			sleep(5)
			user.oak += 1
			if user.oak == user.oak_limit:
				sender(id, 'Ваше хрнилище дуба заполнено!', clear_key)
			user.energy -= 5
			sender(id, 'Рубка леса окончена, вам начислена 1 единица дуба!\nВыберите действие:', forest_menu_key)
			save_bd(users)

def minions_render():
	global users
	while True:
		for user in users:
			if user.level > 1:
				if user.coal > 0:
					if time() - user.last_minion_work > (60*60):
						user.money += minion_cash_from_evo_level[user.minion_evo][user.minion_level]
						user.energy += minion_energy_from_evo_level[user.minion_evo][user.minion_level]
						user.last_minion_work = time()
						user.coal -= 1
						save_bd(users)
Thread(target = minions_render).start()

def timer(id, level, time):
	global users
	for user in users:
		if user.id == id:
			if (user.is_work == False):
				user.is_work = True
				if time == 5:
					if user.level == 1:
						sleep(5)
						user.money += 1
						user.energy -= 1
						sender(id, 'Работа выполнена, вам начислена 1 монета', time_key_lv1)

					elif user.level == 2:
						sleep(10)
						user.money += 1
						user.energy -= 1
						sender(id, 'Работа выполнена, вам начислена 1 монета', time_key_lv2)

					elif user.level == 3:
						sleep(15)
						user.money += 2
						user.energy -= 2
						sender(id, 'Работа выполнена, вам начислено 2 монеты', time_key_lv3)

					user.count5 += 1
					user.is_work = False

				elif time == 10:
					if user.level == 1:
						sleep(10)
						user.money += 2
						user.energy -= 2
						sender(id, 'Работа выполнена, вам начислено 2 монеты', time_key_lv1)

					elif user.level == 2:
						sleep(15)
						user.money += 2
						user.energy -= 2
						sender(id, 'Работа выполнена, вам начислено 2 монеты', time_key_lv2)

					elif user.level == 3:
						sleep(20)
						user.money += 3
						user.energy -= 3
						sender(id, 'Работа выполнена, вам начислено 3 монеты', time_key_lv3)

					user.count10 += 1
					user.is_work = False

				elif time == 15:
					if user.level == 1:
						sleep(15)
						user.money += 3
						user.energy -= 3
						sender(id, 'Работа выполнена, вам начислено 3 монеты', time_key_lv1)

					elif user.level == 2:
						sleep(20)
						user.money += 3
						user.energy -= 3
						sender(id, 'Работа выполнена, вам начислено 3 монеты', time_key_lv2)

					elif user.level == 3:
						sleep(25)
						user.money += 4
						user.energy -= 4
						sender(id, 'Работа выполнена, вам начислено 4 монеты', time_key_lv3)

					user.count15 += 1
					user.is_work = False

				print(user.count5, user.count10, user.count15)

				for user in users:
					if user.id == id:
						if ((user.count5 == predel) & (user.count10 == predel) & (user.count15 == predel)):
							if user.level == 1:
								sender(id, 'Вы выполнили все задания на 1м уровне, перейдите на 2й уровень!', to2lvl_key)
								user.mode = 'level_up'

							elif user.level == 2:
								sender(id, 'Вы выполнили все задания на 2м уровне, перейдите на 3й уровень!', to3lvl_key)
								user.mode = 'level_up'

							elif user.level == 3:
								sender(id, 'Вы выполнили все задания на 3м уровне, перейдите на 4й уровень!', to4lvl_key)
								user.mode = 'level_up'
			else:
				sender(id, 'Вы уже выполняете работу!', clear_key)

	save_bd(users)

print('Bot started!')
while True:
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				if event.to_me:

					id = event.user_id
					msg = event.text.lower()

					if msg == 'начать':

						if check_registration(id):
							flag = 0
							for user in users:
								if user.id == id:
									flag = 1
									break
							if not(flag): # если новый пользователь, то переходим в меню регистрации
								users.append( User(id = id, coal = 24, last_minion_work = 0, sklad_level = 0, to_sleep = 0, is_work = False, pick_level = 0, oak_limit = 0, minion_evo = 0, oak = 0, axe_level = 0, pers_name = None, minion_level = 0, mode = 'registration1', money = 0, pol = None, energy = 100, level = 1, count5 = 0, count10 = 0, count15 = 0) )
								sender(id, f'Правила:\nДля того, чтобы пройти уровень, вам нужно выполнить каждый тип работы, по {predel} раз.', clear_key)
								sender(id, 'Выберите пол вашего персонажа:', reg_key)
							elif flag: # если пользователь старый, то выходим в главное меню
								for user in users:
									if user.id == id:
										if not(user.mode in ['registration1', 'registration2']):
											sender(id, 'Выберите действие:', menus[user.level])
											user.mode = 'start'
						else:
							sender(id, 'Вы не подписаны на группу!\nДля того, чтобы пользоваться ботом, необходимо подписаться на сообщество!', clear_key)

					else:
						for user in users:
							if user.id == id:

								if user.mode == 'registration1':
									flag = 0
									if msg == 'мужской':
										user.pol = 'Мужской'
										flag = 1
									elif msg == 'женский':
										user.pol = 'Женский'
										flag = 1
									if flag:
										sender(id, 'Введите имя персонажа:', clear_key)
										user.mode = 'registration2'

								elif user.mode == 'registration2':
									user.pers_name = event.text
									sender(id, 'Выберите действие:', lv1_menu_key)
									user.mode = 'start'

								elif user.level == 1:
									if user.mode == 'start':
										
										if msg == 'работа':
											sender(id, 'Выберите, сколько вы хотите работать:', time_key_lv1)
											user.mode = 'work'
										
										elif msg == 'персонаж':
											sender(id, f'Пол: {user.pol}\nИмя: {user.pers_name}\nМонеты: {user.money}', lv1_menu_key)

									elif user.mode == 'work':
										if msg == '5сек':
											if user.count5 < predel:
												sender(id, 'Работа началась и продлится 5 секунд...', clear_key)
												Thread(target = timer(id, user.level, 5)).start()
											else:
												sender(id, 'Вы выполнили всю 5-ти секундную работу, приступайте к другой!', time_key_lv1)

										elif msg == '10сек':
											if user.count10 < predel:
												sender(id, 'Работа началась и продлится 10 секунд...', clear_key)
												Thread(target = timer(id, user.level, 10)).start()
											else:
												sender(id, 'Вы выполнили всю 10-ти секундную работу, приступайте к другой!', time_key_lv1)

										elif msg == '15сек':
											if user.count15 < predel:
												sender(id, 'Работа началась и продлится 15 секунд...', clear_key)
												Thread(target = timer(id, user.level, 15)).start()
											else:
												sender(id, 'Вы выполнили всю 15-ти секундную работу, приступайте к другой!', time_key_lv1)

										elif msg == 'назад':
											sender(id, 'Выберите действие:', lv1_menu_key)
											user.mode = 'start'

									elif user.mode == 'level_up':
										if msg == 'перейти на 2й уровень':
											user.count5 = 0
											user.count10 = 0
											user.count15 = 0
											user.coal = 24
											sender(id, 'Поздравляем, вы перешли на 2й уровень!\nВыберите действие:', lv2_menu_key)
											user.level = 2
											user.mode = 'start'

								elif user.level == 2:
									if user.mode == 'start':
										if msg == 'работа':
											sender(id, 'Выберите, сколько вы хотите работать:', time_key_lv2)
											user.mode = 'work'

										elif msg == 'персонаж':
											sender(id, f'Пол персонажа: {user.pol}\nИмя: {user.pers_name}\nМонеты: {user.money}', lv2_menu_key)

										elif msg == 'миньон':
											if user.minion_level == 0:
												sender(id, 'Для начала работы с миньёном, купите его за 70 монет:', buy_minion_key)
											else:
												sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

									elif user.mode == 'work':
										if msg == '10сек':
											if user.count5 < predel:
												sender(id, 'Работа началась и продлится 10 секунд...', clear_key)
												Thread(target = timer(id, user.level, 5)).start()
											else:
												sender(id, 'Вы выполнили всю 10-ти секундную работу, приступайте к другой!', time_key_lv2)

										if msg == '15сек':
											if user.count10 < predel:
												sender(id, 'Работа началась и продлится 15 секунд...', clear_key)
												Thread(target = timer(id, user.level, 10)).start()
											else:
												sender(id, 'Вы выполнили всю 30-ти секундную работу, приступайте к другой!', time_key_lv2)

										if msg == '20сек':
											if user.count15 < predel:
												sender(id, 'Работа началась и продлится 20 секунд...', clear_key)
												Thread(target = timer(id, user.level, 15)).start()
											else:
												sender(id, 'Вы выполнили всю 45-ти секундную работу, приступайте к другой!', time_key_lv2)

										if msg == 'назад':
											sender(id, 'Выберите действие:', lv2_menu_key)
											user.mode = 'start'

									elif user.mode == 'minion':
										if user.minion_level == 0:
											if msg == 'купить миньона':
												if user.money >= minion_level_cash[user.minion_evo][user.minion_level]:
													user.money -= minion_level_cash[user.minion_evo][user.minion_level]
													user.minion_level = 1
													sender(id, 'Поздравляем, вы купили миньона, теперь он будет приносить вам доход!\nВыберите действие:', minion_menu)
												else:
													sender(id, 'У вас не достаточно монет!', buy_minion_key)
											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv2_menu_key)
												user.mode = 'start'

										else:
											if msg == 'улучшить':
												if user.minion_evo == 0:
													if user.minion_level < 3:
														sender(id, f'Улучшение стоит: {minion_level_cash[user.minion_evo][user.minion_level]}\nВаши монеты: {user.money}', ask_key)
														user.mode = 'ask_menu'
													elif user.minion_level == 3:
														if user.minion_evo < 1:
															sender(id, 'Ваш миньон достиг максимального уровня, эволюционируйте его!', evo_minion_key)
															user.mode = 'evo_1_minion_mode'
														else:
															sender(id, 'Ваш миньон уже эволюционирован!', minion_menu)

												elif user.minion_evo == 1:
													if user.minion_level < 3:
														sender(id, f'Улучшение стоит: {minion_level_cash[user.minion_evo][user.minion_level]}\nВаши монеты: {user.money}', ask_key)
														user.mode = 'ask_menu'
													elif user.minion_level == 3:
														sender(id, 'Ваш миньон достиг максимального уровня!', minion_menu)

											elif msg == 'статистика':
												if user.minion_evo == 0:
													sender(id, f'Уровень миньона: {user.minion_level}\nПрибыль: {minion_energy_from_evo_level[user.minion_evo][user.minion_level]} энергии в час', minion_menu)
												elif user.minion_evo == 1:
													sender(id, f'Уровень миньона: {user.minion_level}\nПрибыль:\n{minion_energy_from_evo_level[user.minion_evo][user.minion_level]} энергии в час\n{minion_cash_from_evo_level[user.minion_evo][user.minion_level]} монет в час', minion_menu)

											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv2_menu_key)
												user.mode = 'start'

									elif user.mode == 'ask_menu':
										if msg == 'улучшить':
											if user.money >= minion_level_cash[user.minion_evo][user.minion_level]:
												user.money -= minion_level_cash[user.minion_evo][user.minion_level]
												user.minion_level += 1
												sender(id, f'Вы успешно улучшили своего миньона на {user.minion_level} уровень', minion_menu)
												user.mode = 'minion'
											else:
												sender(id, 'У вас не достаточно монет для улучшения!', ask_key)

										elif msg == 'отмена':
											sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

									elif user.mode == 'evo_1_minion_mode':
										if msg == 'эволюция':
											if user.minion_evo < 1:
												user.minion_level = 1
												user.minion_evo += 1
												sender(id, 'Вы успешно эволюционировали своего миньона!\nВыберите действие:', minion_menu)
												user.mode = 'minion'
											else:
												sender(id, 'Ваш миньон уже эволюционирован!', minion_menu)
												user.mode = 'minion'

										elif msg == 'назад':
											sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

									elif user.mode == 'level_up':
										if msg == 'перейти на 3й уровень':
											user.count5 = 0
											user.count10 = 0
											user.count15 = 0
											sender(id, 'Поздравляем, вы перешли на 3й уровень!\nВыберите действие:', lv3_menu_key)
											user.level = 3
											user.mode = 'start'

								elif user.level == 3:
									if user.mode == 'start':
										if msg == 'работа':
											sender(id, 'Выберите, сколько вы хотите работать:', time_key_lv3)
											user.mode = 'work'

										elif msg == 'персонаж':
											sender(id, f'Пол персонажа: {user.pol}\nИмя: {user.pers_name}\nМонеты: {user.money}\nДуб: {user.oak}', lv3_menu_key)

										elif msg == 'миньон':
											if user.minion_level == 0:
												sender(id, 'Для начала работы с миньёном, купите его за 70 монет:', buy_minion_key)
											else:
												sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

										elif msg == 'лес':
											if user.axe_level == 0:
												sender(id, 'Для начала работы с лесом, купите топор за 60 монет!', buy_axe_key)
											else:
												sender(id, 'Выберите действие:', forest_menu_key)
											user.mode = 'forest'

									elif user.mode == 'work':
										if msg == '15сек':
											if user.count5 < predel:
												sender(id, 'Работа началась и продлится 15 секунд...', clear_key)
												Thread(target = timer(id, user.level, 5))
											else:
												sender(id, 'Вы выполнили всю 15-ти секундную работу, приступайте к другой!', time_key_lv3)

										elif msg == '20сек':
											if user.count10 < predel:
												sender(id, 'Работа началась и продлится 20 секунд...', clear_key)
												Thread(target = timer(id, user.level, 10))
											else:
												sender(id, 'Вы выполнили всю 20-ти секундную работу, приступайте к другой!', time_key_lv3)

										elif msg == '25сек':
											if user.count15 < predel:
												sender(id, 'Работа началась и продлится 25 секунд...', clear_key)
												Thread(target = timer(id, user.level, 15))
											else:
												sender(id, 'Вы выполнили всю 25-ти секундную работу, приступайте к другой!', time_key_lv3)

										elif msg == 'назад':
											sender(id, 'Выберите действие:', lv3_menu_key)
											user.mode = 'start'

									elif user.mode == 'minion':

										if user.minion_level == 0:
											if msg == 'купить миньона':
												if user.money >= minion_level_cash[user.minion_evo][user.minion_level]:
													user.money -= minion_level_cash[user.minion_evo][user.minion_level]
													user.minion_level = 1
													sender(id, 'Поздравляем, вы купили миньона, теперь он будет приносить вам доход!\nВыберите действие:', minion_menu)
												else:
													sender(id, 'У вас не достаточно монет!', buy_minion_key)
											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv3_menu_key)
												user.mode = 'start'

										else:
											if msg == 'улучшить':
												if user.minion_evo == 0:
													if user.minion_level < 3:
														sender(id, f'Улучшение стоит: {minion_level_cash[user.minion_evo][user.minion_level]}\nВаши монеты: {user.money}', ask_key)
														user.mode = 'ask_menu'
													elif user.minion_level == 3:
														if user.minion_evo < 1:
															sender(id, 'Ваш миньон достиг максимального уровня, эволюционируйте его!', evo_minion_key)
															user.mode = 'evo_1_minion_mode'
														else:
															sender(id, 'Ваш миньон уже эволюционирован!', minion_menu)

												elif user.minion_evo == 1:
													if user.minion_level < 3:
														sender(id, f'Улучшение стоит: {minion_level_cash[user.minion_evo][user.minion_level]}\nВаши монеты: {user.money}', ask_key)
														user.mode = 'ask_menu'
													elif user.minion_level == 3:
														sender(id, 'Ваш миньон достиг максимального уровня!', minion_menu)

											elif msg == 'статистика':
												if user.minion_evo == 0:
													sender(id, f'Уровень миньона: {user.minion_level}\nПрибыль: {minion_energy_from_evo_level[user.minion_evo][user.minion_level]} энергии в час', minion_menu)
												elif user.minion_evo == 1:
													sender(id, f'Уровень миньона: {user.minion_level}\nПрибыль:\n{minion_energy_from_evo_level[user.minion_evo][user.minion_level]} энергии в час\n{minion_cash_from_evo_level[user.minion_evo][user.minion_level]} монет в час', minion_menu)

											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv3_menu_key)
												user.mode = 'start'

									elif user.mode == 'ask_menu':
										if msg == 'улучшить':
											if user.money >= minion_level_cash[user.minion_evo][user.minion_level]:
												user.money -= minion_level_cash[user.minion_evo][user.minion_level]
												user.minion_level += 1
												sender(id, f'Вы успешно улучшили своего миньона на {user.minion_level} уровень', minion_menu)
												user.mode = 'minion'
											else:
												sender(id, 'У вас не достаточно монет для улучшения!', ask_key)

										elif msg == 'отмена':
											sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

									elif user.mode == 'evo_1_minion_mode':
										if msg == 'эволюция':
											if user.minion_evo < 1:
												user.minion_level = 1
												user.minion_evo += 1
												sender(id, 'Вы успешно эволюционировали своего миньона!\nВыберите действие:', minion_menu)
												user.mode = 'minion'
											else:
												sender(id, 'Ваш миньон уже эволюционирован!', minion_menu)
												user.mode = 'minion'

										elif msg == 'назад':
											sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

									elif user.mode == 'forest':

										if user.axe_level == 0:
											if msg == 'купить топор':
												if user.money >= 60:
													user.money -= 60
													user.axe_level += 1
													user.oak_limit = 32
													sender(id, 'Поздравляем, вы успешно приобрели топор!\nВыберите действие:', forest_menu_key)
												else:
													sender(id, 'У вас не достаточно монет!', buy_axe_key)
											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv3_menu_key)
												user.mode = 'start'

										else:
											if msg == 'рубить дуб':
												sender(id, f'Рубить дуб можно начиная с 4го уровня!\nЧтобы перейти на 4й уровень, выполните всю рботу 3го уровня!\nВыберите действие:', forest_menu_key)

											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv3_menu_key)
												user.mode = 'start'

									elif user.mode == 'level_up':
										if msg == 'перейти на 4й уровень':
											user.count5 = 0
											user.count10 = 0
											user.count15 = 0
											sender(id, 'Поздравляем, вы перешли на 4й уровень!\nВыберите действие:', lv4_menu_key)
											user.level = 4
											user.mode = 'start'

								if user.level == 4:

									if user.mode == 'start':
										if msg == 'шахта':
											if user.pick_level == 0:
												sender(id, 'Для начала работы с шахтой, купите кирку за 96 единиц дуба!', buy_pick_key)
											else:
												sender(id, 'Выберите действие:', mine_menu_key)
											user.mode = 'mine'

										elif msg == 'персонаж':
											sender(id, f'Пол: {user.pol}\nИмя: {user.pers_name}\nМонеты: {user.money}\nУголь: {user.coal}\nДуб: {user.oak}/{user.oak_limit}\nУровень миньёна: {user.minion_level}', lv4_menu_key)

										elif msg == 'миньон':
											if user.minion_level == 0:
												sender(id, 'Для начала работы с миньёном, купите его за 70 монет:', buy_minion_key)
											else:
												sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

										elif msg == 'лес':
											if user.axe_level == 0:
												sender(id, 'Для начала работы с лесом, купите топор за 60 монет!', buy_axe_key)
											else:
												sender(id, 'Выберите действие:', forest_menu_key)
											user.mode = 'forest'

										elif msg == 'дом':
											sender(id, 'Выберите действие:', house_menu_key)
											user.mode = 'house'

									elif user.mode == 'minion':
										if user.minion_level == 0:
											if msg == 'купить миньона':
												if user.money >= minion_level_cash[user.minion_evo][user.minion_level]:
													user.money -= minion_level_cash[user.minion_evo][user.minion_level]
													user.minion_level = 1
													sender(id, 'Поздравляем, вы купили миньона, теперь он будет приносить вам доход!\nВыберите действие:', minion_menu)
												else:
													sender(id, 'У вас не достаточно монет!', buy_minion_key)
											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv4_menu_key)
												user.mode = 'start'

										else:
											if msg == 'улучшить':
												if user.minion_evo == 0:
													if user.minion_level < 3:
														sender(id, f'Улучшение стоит: {minion_level_cash[user.minion_evo][user.minion_level]}\nВаши монеты: {user.money}', ask_key)
														user.mode = 'ask_menu'
													elif user.minion_level == 3:
														if user.minion_evo < 1:
															sender(id, 'Ваш миньон достиг максимального уровня, эволюционируйте его!', evo_minion_key)
															user.mode = 'evo_1_minion_mode'
														else:
															sender(id, 'Ваш миньон уже эволюционирован!', minion_menu)

												elif user.minion_evo == 1:
													if user.minion_level < 3:
														sender(id, f'Улучшение стоит: {minion_level_cash[user.minion_evo][user.minion_level]}\nВаши монеты: {user.money}', ask_key)
														user.mode = 'ask_menu'
													elif user.minion_level == 3:
														sender(id, 'Ваш миньон достиг максимального уровня!', minion_menu)

											elif msg == 'статистика':
												if user.minion_evo == 0:
													sender(id, f'Уровень миньона: {user.minion_level}\nПрибыль: {minion_energy_from_evo_level[user.minion_evo][user.minion_level]} энергии в час', minion_menu)
												elif user.minion_evo == 1:
													sender(id, f'Уровень миньона: {user.minion_level}\nПрибыль:\n{minion_energy_from_evo_level[user.minion_evo][user.minion_level]} энергии в час\n{minion_cash_from_evo_level[user.minion_evo][user.minion_level]} монет в час', minion_menu)

											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv4_menu_key)
												user.mode = 'start'

									elif user.mode == 'ask_menu':
										if msg == 'улучшить':
											if user.money >= minion_level_cash[user.minion_evo][user.minion_level]:
												user.money -= minion_level_cash[user.minion_evo][user.minion_level]
												user.minion_level += 1
												sender(id, f'Вы успешно улучшили своего миньона на {user.minion_level} уровень', minion_menu)
												user.mode = 'minion'
											else:
												sender(id, 'У вас не достаточно монет для улучшения!', ask_key)

										elif msg == 'отмена':
											sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

									elif user.mode == 'evo_1_minion_mode':
										if msg == 'эволюция':
											if user.minion_evo < 1:
												user.minion_level = 1
												user.minion_evo += 1
												sender(id, 'Вы успешно эволюционировали своего миньона!\nВыберите действие:', minion_menu)
												user.mode = 'minion'
											else:
												sender(id, 'Ваш миньон уже эволюционирован!', minion_menu)
												user.mode = 'minion'

										elif msg == 'назад':
											sender(id, 'Выберите действие:', minion_menu)
											user.mode = 'minion'

									elif user.mode == 'forest':
										if user.axe_level == 0:
											if msg == 'купить топор':
												if user.money >= 60:
													user.money -= 60
													#user.axe_level += 1
													#user.oak_limit = 64
													sender(id, 'Поздравляем, вы успешно приобрели топор!\nВыберите действие:', forest_menu_key)
												else:
													sender(id, 'У вас не достаточно монет!', buy_axe_key)
											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv4_menu_key)
												user.mode = 'start'

										else:
											if msg == 'рубить дуб':
												if user.oak < user.oak_limit:#                                          \
													sender(id, 'Работа продолжится в течении 5ти секунд...', clear_key)# \
													Thread(target = forest_render(id)).start()#							  | если будет нельзя рубить дуб на 3м уровне, то заменить это на sender(id, f'Рубить дуб можно начиная с 4го уровня!\nЧтобы перейти на 4й уровень, выполните всю рботу 3го уровня!\nВыберите действие:', forest_menu_key)
												else:#																	 /
													sender(id, 'Ваше хранилище дуба заполнено!', forest_menu_key)#       /

											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv4_menu_key)
												user.mode = 'start'

									elif user.mode == 'mine':
										if user.pick_level == 0:
											if msg == 'купить кирку':
												if user.oak >= 96:
													user.pick_level += 1
													user.oak -= 96
													sender(id, 'Вы успешно купили кирку!\nВыберите действие:', mine_menu_key)
												else:
													sender(id, 'У вас не достаточно дуба для покупки кирки!', mine_menu_key)
											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv4_menu_key)
												user.mode = 'start'

										else:
											if msg == 'добывать уголь':
												sender(id, 'Началась добыча угля, она продлится 30 секунд!', clear_key)
												Thread(target = get_coal(id)).start()

											elif msg == 'назад':
												sender(id, 'Выберите действие:', lv4_menu_key)
												user.mode = 'start'

									elif user.mode == 'house':
										if msg == 'спать':
											sender(id, 'Чтобы проснуться нажмите на "Проснуться"', stand_up_key)
											user.to_sleep = time()
											user.mode = 'sleep'

										elif msg == 'хранилище':
											if user.sklad_level == 0:
												sender(id, f'Для того, чтобы пользоваться хранилищем, постройте его!', buy_sklad_key)
											else:
												sender(id, f'Уровень хранилища: {user.sklad_level}\nВместимость хранилища: {user.oak_limit}\nВыберите действие:', sklad_menu_key)
											user.mode = 'sklad'

										elif msg == 'назад':
											sender(id, 'Выберите действие:', lv4_menu_key)
											user.mode = 'start'

									elif user.mode == 'sleep':
										if msg == 'проснуться':
											count = (time() - user.to_sleep) // 3
											user.energy += count
											sender(id, f'За время сна вам начислено: {count} энергии!\nВыберите действие:', house_menu_key)
											user.mode = 'house'

									elif user.mode == 'sklad':
										if user.sklad_level == 0:
											if msg == 'построить хранилище':
												user.sklad_level = 1
												user.oak_limit = 32
												sender(id, f'Вы успешно построили хранилище!\nУровень хранилища: {user.sklad_level}\nВместимость хранилища: {user.oak_limit}\nВыберите действие:', sklad_menu_key)
											elif msg == 'назад':
												sender(id, 'Выберите действие:', house_menu_key)
												user.mode = 'house'
										else:
											if msg == 'улучшить':
												if user.sklad_level < 10:
													sender(id, f'Улучшение хранилища стоит: {(user.sklad_level)*32} единиц дуба\nУ вас: {user.oak} дуба\nУлучшение хранилища даст +32 к лимиту хранения дуба', ask_key)
													user.mode = 'ask_2_menu'
												else:
													sender(id, 'Ваш хранилище достиг максимального уровня!', sklad_menu_key)

											elif msg == 'назад':
												sender(id, 'Выберите действие:', house_menu_key)
												user.mode = 'house'

									elif user.mode == 'ask_2_menu':
										if msg == 'улучшить':
											if user.oak < ((user.sklad_level)*32):
												sender(id, 'У вас не достаточно дуба!', ask_key)
											else:
												user.oak -= ((user.sklad_level)*32)
												user.sklad_level += 1
												user.oak_limit = user.sklad_level*32
												sender(id, f'Вы успешно улучшили хранилище!\nУровень хранилища: {user.sklad_level}\nВместимость хранилища: {user.oak_limit}', sklad_menu_key)
												user.mode = 'sklad'
										elif msg == 'отмена':
											sender(id, 'Выберите действие:', house_menu_key)
											user.mode = 'house'

				save_bd(users)

	except Exception as error:
		print('Error detected!')
		longpoll = VkLongPoll(vk_session)