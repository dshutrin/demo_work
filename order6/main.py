import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from config import tok


class MyLongPoll(VkLongPoll):
	def listen(self):
		while True:
			try:
				for event in self.check():
					yield event
			except Exception as e:
				print('error', e)


class User:
	def __init__(self, id, mode, money, nickname, clan_name, password, is_log, inv):
		self.id = id
		self.mode = mode
		self.clan_name = clan_name
		self.money = money
		self.nickname = nickname
		self.password = password
		self.is_log = is_log
		self.inv = inv


class Clan:
	def __init__(self, name, users, counts):
		self.name = name
		self.counts = counts
		self.users = users
		self.lider = users[0].id

	def add_user(self, user):
		self.users.append(user)


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


vk_session = vk_api.VkApi(token = tok)
longpoll = MyLongPoll(vk_session)

clear_key = get_keyboard([])

start_key = get_keyboard([
	[('Войти', 'зеленый'), ('Зарегистрироваться', 'синий')]
])

back_key = get_keyboard([
	[('Назад', 'красный')]
])

menu_key = get_keyboard([
	[('Профиль', 'синий'), ('Донат', 'зеленый')],
	[('Выйти', 'красный'), ('Кланы', 'синий')]
])

lid_clan_menu = get_keyboard([
	[('Пригласить в клан', 'синий')],
	[('Список кланов', 'синий'), ('Мой клан', 'синий')],
	[('Удалить клан', 'красный'), ('Исключить участника', 'красный')],
	[('Назад', 'красный'), ('Выйти из клана', 'зеленый')]
])

cl_del_key = get_keyboard([
	[('Подтвердить', 'красный')],
	[('Назад', 'зеленый')]
])

prof_key = get_keyboard([
	[('Мой профиль', 'зеленый')],
	[('Сменить пароль', 'синий'), ('Сменить никнэйм', 'синий')],
	[('Назад', 'красный')]
])

clan_menu = get_keyboard([
	[('Список кланов', 'синий'), ('Мой клан', 'синий')],
	[('Назад', 'красный'), ('Выйти из клана', 'зеленый')]
])

clan_menu1 = get_keyboard([
	[('Вступить в клан', 'синий'), ('Создать клан', 'зеленый')],
	[('Назад', 'красный'), ('Список кланов', 'синий')]
])

donate_menu = get_keyboard([
	[('Тарифы', 'синий'), ('Сделать покупку', 'зеленый')],
	[('Назад', 'красный')]
])


def top_clans(clans):
	for i in range(len(clans)):
		for k in range(i, len(clans)):
			if clans[i].counts < clans[k].counts:
				clans[i], clans[k] = clans[k], clans[i]
	if len(clans) >= 10:
		return clans[:10]
	else:
		return clans


users = []
clans = []
ADMIN_ID = 296431501
online = 0


def sender(id, text, key):
	vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : key})


def admin_info(e_id):
	flag = 0
	for s_user in users:
		if s_user.id == ADMIN_ID:
			sender(ADMIN_ID, f'Пользователь @id{e_id} ввёл не верный пароль!')
			s_user.mode = 'main'
			flag = 1
			break


def search_clan(id):
	for clan in clans:
		for user in clan.users:
			if user.id == id:
				return clan


while True:
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				if (event.to_me) and not(event.from_chat):
		
					id = event.user_id
					msg = event.text.lower()
		
					flag = 0
					for user in users:
						if user.id == id:
							flag = 1
							break
		
					if flag == 0:
						users.append(User(id, 'start', 3000, '', '', '', 0, []))
						sender(id, 'Для регистрации введите "/reg" или "/register"\nДля авторизации в боте введите "/log" или "/login"', start_key)
	
					for user in users:
						if user.id == id:
							
							if user.mode == 'start':
	
								if msg in ['/reg', '/register', 'зарегистрироваться']:
									flag = 0
									for s_user in users:
										if (s_user.id == id) and (s_user.nickname == user.nickname) and (user.nickname != ''):
											flag = 1
											break
									if flag == 0:
										sender(id, 'Для регистрации введите желаемый никнэйм в следующем сообщении\nНикнэйм нельзя изменить, он устанавливается 1 раз!', clear_key)
										user.mode = 'reg1'
									else:
										sender(id, 'Вы уже зарегистрированы в боте!', start_key)
	
								elif msg in ['/log', '/login', 'войти']:
									flag = 0
									for s_user in users:
										if (s_user.id == id) and (s_user.password != ''):
											flag = 1
											break
									if flag:
										sender(id, 'Введите свой пароль:', clear_key)
										user.mode = 'log'
									else:
										sender(id, "Вы еще не зарегистрированы в боте!", start_key)
	
							else:
								if user.mode == 'reg1':
									flag = 0
									for s_user in users:
										if s_user.nickname == event.text:
											flag = 1
											break
									if flag:
										sender(id, 'Такой никнэйм уже занят!\nВведите другой!', clear_key)
									else:
										user.nickname = event.text
										sender(id, 'Для завершения регистрации придумайте надёжный пароль:', clear_key)
										user.mode = 'reg2'
	
								elif user.mode == 'reg2':
									user.password = event.text
									sender(id, 'Поздравляем с успешной регистрацией!\nДля авторизации в боте введите "/log" или "/login"', start_key)
									user.mode = 'start'
	
								elif user.mode == 'log':
									if event.text == user.password:
										sender(id, 'Выберите действие:', menu_key)
										user.is_log = True
										online += 1
										user.mode = 'main'
	
									else:
										sender(id, 'Пароль неверный!\nДля регистрации введите "/reg" или "/register"\nДля авторизации в боте введите "/log" или "/login"', start_key)
										admin_info(id)
										user.mode = 'start'
	
	
	
								elif user.mode == 'main':
									if msg == 'выйти':
										user.is_log = False
										online -= 1
										sender(id, 'Для регистрации введите "/reg" или "/register"\nДля авторизации в боте введите "/log" или "/login"', start_key)
										user.mode = 'start'
	
									elif msg == 'профиль':
										sender(id, f'Выберите действие:', prof_key)
										user.mode = 'profil'
	
									elif msg == 'кланы':
										if user.clan_name:
											if search_clan(id).lider == id:
												sender(id, 'Выберите действие:', lid_clan_menu)
											else:
												sender(id, 'Выберите действие:', clan_menu)
										else:
											sender(id, 'Выберите действие:', clan_menu1)
										user.mode = 'clans'
	
									elif msg == 'донат':
										sender(id, 'Выберите действие:', donate_menu)
										user.mode = 'donate'



								elif user.mode == 'profil':
									if msg == 'назад':
										sender(id, 'Выберите действие:', menu_key)
										user.mode = 'main'

									elif msg == 'мой профиль':
										if user.clan_name:
											clan_info = user.clan_name
										else:
											clan_info = 'Вы не состоите в клане на данный момент'
										ans = f'Ваш никнэйм: {user.nickname}\nВаш пароль: {user.password}\nВаши монеты: {user.money}\nВаш клан: {clan_info}\nПользователей онлайн: {online}'
										sender(id, ans, prof_key)

									elif msg == 'сменить пароль':
										sender(id, 'Придумайте новый надёжный пароль:', back_key)
										user.mode = 'change_pass'

									elif msg == 'сменить никнэйм':
										if user.money >= 100:
											sender(id, 'Смена никнэйма стоит 100 монет\nВведите новый никнэйм:', back_key)
											user.mode = 'change_name'
										else:
											sender(id, 'Смена никнэйма стоит 100 монет\nУ вас недостаточно средств!', prof_key)



								elif user.mode == 'change_pass':
									if msg == 'назад':
										sender(id, 'Выберите действие:', prof_key)
										user.mode = 'profil'

									else:
										if user.password == event.text:
											sender(id, 'Нельзя сменить пароль на текущий\nПридумайте новый!', prof_key)
											user.mode = 'profil'
										else:
											user.password = event.text
											sender(id, f'Вы успешно сменили пароль на {user.password}\nВыберите действие:', prof_key)
											user.mode = 'profil'



								elif user.mode == 'change_name':
									if msg == 'назад':
										sender(id, 'Выберите действие:', prof_key)
										user.mode = 'profil'

									else:
										if user.nickname == event.text:
											sender(id, 'Нельзя сменить никнэйм на текущий!\nВыберите действие:', prof_key)
											user.mode = 'profil'
										else:
											flag = 0
											for s_user in users:
												if event.text == s_user.nickname:
													flah = 1
													break
											if flag == 0:
												user.nickname = event.text
												sender(id, f'Вы успешно сменили никнэйм на {user.nickname}\nВыберите действие:', prof_key)
												user.mode = 'profil'
											else:
												sender(id, 'Такой никнэйм уже занят!\nВыберите действие:', prof_key)
												user.mode = 'profil'



								elif user.mode == 'clans':
									if msg == 'назад':
										sender(id, 'Выберите действие:', menu_key)
										user.mode = 'main'

									else:
										if user.clan_name:
											
											if msg == 'мой клан':
												my_clan = search_clan(id)
												ans = 'Ваши соклановцы:\n'
												for s_user in my_clan.users:
													ans = f'{ans}{s_user.nickname}\n'
												if search_clan(id).lider == id:
													sender(id, ans, lid_clan_menu)
												else:
													sender(id, ans, clan_menu)

											elif msg == 'список кланов':
												ans = ''
												if len(clans) > 0:
													ans = 'Топ кланов:\n'
													for clan in top_clans(clans):
														ans = f'{ans}{clan.name}\n'
												else:
													ans = 'На данный момент не существует ни одного клана'
												if search_clan(id).lider == id:
													sender(id, ans, lid_clan_menu)
												else:
													sender(id, ans, clan_menu)

											elif msg == 'выйти из клана':
												for clan in clans:
													if user.clan_name == clan.name:
														del clan.users[clan.users.index(user)]
														break
												user.clan_name = ''
												sender(id, 'Вы успешно вышли из клана', menu_key)
												user.mode = 'main'

											elif msg == 'пригласить в клан':
												sender(id, 'Введите игровой ник игрока, которого хотите пригласить:', clear_key)
												user.mode = 'invite'

											elif (msg == 'удалить клан') and (search_clan(id).lider == id):
												sender(id, 'Подтвердите удаление клана', cl_del_key)
												user.mode = 'del_clan'

											elif msg == ('исключить участника') and (search_clan(id).lider == id):
												s_clan = search_clan(id)
												ans = 'Введите игровой ник участника, которого хотите исключить:\n'
												for s_user in s_clan.users:
													ans = f'{ans}{s_user.nickname}\n'
												sender(id, ans, back_key)
												user.mode = 'kick_user'

										else:
											if msg == 'создать клан':
												if user.money >= 300:
													sender(id, 'Введите название для нового клана', back_key)
													user.mode = 'create_clan'
												else:
													sender(id, 'У вас недостаточно монет (необходимо 300 монет)', clan_menu1)

											elif msg == 'список кланов':
												ans = ''
												if len(clans) > 0:
													ans = 'Топ кланов:\n'
													for clan in clans:
														ans = f'{ans}{clan.name}\n'
												else:
													ans = 'На данный момент не существует ни одного клана'
												sender(id, ans, clan_menu1)

											elif msg == 'вступить в клан':
												if len(user.inv) > 0:
													ans = 'Ваши приглашения:\n'
													for i in range(len(user.inv)):
														ans = f'{ans}{i+1}) {user.inv[i][0]}\n'
													ans = f'{ans}\nВведите номер приглашения:'
													sender(id, ans, back_key)
													user.mode = 'get_invite'
												else:
													ans = 'У вас нет приглашений'
													sender(id, ans, clan_menu1)



								elif user.mode == 'kick_user':
									if msg == 'назад':
										sender(id, 'Выберите действие:', lid_clan_menu)
										user.mode = 'clans'

									else:
										if event.text == user.nickname:
											sender(id, 'Нельзя исключить самого себя!', lid_clan_menu)
											user.mode = 'clans'
										else:
											flag = 0
											s_i = -1
											for s_user in [x for x in search_clan(id).users]:
												s_i += 1
												if (s_user.nickname == event.text) and (event.text != user.nickname):
													s_user.clan_name = ''
													sender(s_user.id, 'Вы были исключены из клана!', clan_menu1)
													s_user.mode = 'clans'
													flag = 1
													break
											if flag:
												sender(id, 'Пользователь был исключён!', lid_clan_menu)
												user.mode = 'clans'
											else:
												sender(id, 'Пользователя с таким ником нет в вашем клане!', lid_clan_menu)
												user.mode = 'clans'



								elif user.mode == 'del_clan':
									print(clans)
									if msg == 'подтвердить':
										s_clan = search_clan(id)
										for s_user in s_clan.users:
											if s_user.id != id:
												s_user.clan_name = ''
												sender(s_user.id, 'Ваш клан распался. Теперь вы не являетесь его участником!', clan_menu1)
												s_user.mode = 'clans'

										for i in range(len(clans)):
											if clans[i].name == user.clan_name:
												clans = [clan for clan in clans if clan.name != user.clan_name]
												print(clans)
												break
										user.clan_name = ''
										user.money =+ 150
										sender(id, 'Вы разформировали свой клан!', clan_menu1)
										user.mode = 'clans'

									elif msg == 'назад':
										sender(id, 'Выберите действие:', lid_clan_menu)
										user.mode = 'clans'



								elif user.mode == 'get_invite':
									if msg == 'назад':
										sender(id, 'Выберите действие:', clan_menu1)
										user.mode = 'clans'
									else:
										try:
											num = int(msg)
											user.inv[num-1][1].add_user(user)
											user.clan_name = user.inv[num-1][0]
											del user.inv[num-1]
											sender(id, 'Поздравляем, вы успешно присоединились к клану!', clan_menu)
											user.mode = 'clans'
										except:
											sender(id, 'Введите номер приглашения:', back_key)



								elif user.mode == 'invite':
									flag = 0
									for s_user in users:
										if s_user.nickname == event.text:
											if s_user.clan_name == '':
												flag = 1
												s_user.inv.append([user.clan_name, search_clan(user.id)])
											else:
												flag = 2
									if flag == 1:
										sender(id, 'Приглашение отправлено!', lid_clan_menu)
									elif flag == 0:
										sender(id, 'Пользователя  таким ником не существует!', lid_clan_menu)
									elif flag == 2:
										sender(id, 'Пользователь уже состоит в клане!', lid_clan_menu)
									user.mode = 'clans'



								elif user.mode == 'create_clan':
									if msg == 'назад':
										sender(id, 'Выберите действие:', clan_menu1)
										user.mode = 'clans'
	
									else:
										flag = 0
										for clan in clans:
											if clan.name == event.text:
												flag = 1
												break
										if flag == 1:
											sender(id, 'Клан с таким названием уже существует!', back_key)
										else:
											clans.append(Clan(event.text, [user], 0))
											user.clan_name = event.text
											user.money -= 300
											sender(id, 'Выберите действие:', menu_key)
											user.mode = 'main'



								elif user.mode == 'donate':
									if msg == 'назад':
										sender(id, 'Выберите действие:', menu_key)
										user.mode = 'main'

							clans = [x for x in clans if len(x.users) > 0]
							print(f'Пользователь: {id}\nСообщение: {msg}\nРежим: {user.mode}\n\n')
	
	except Exception as e:
		vk_session = vk_api.VkApi(token = tok)
		longpoll = MyLongPoll(vk_session)
		print(e)