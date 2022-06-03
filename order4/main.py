import vk_api, json
from random import randint as rand
from vk_api.longpoll import VkEventType, VkLongPoll
from config import tok
from threading import Thread


try:
	vk_session = vk_api.VkApi(token = tok)
	longpoll = VkLongPoll(vk_session)
	print('Connected')
except Exception as e:
	input('Произошла ошибка подключения к вк, программа завершилась!')
	exit()


class User():
	def __init__(self, id, cash, mode, number, access_key):
		self.id = id
		self.number = number
		self.cash = cash
		self.mode = mode
		self.access_key = access_key


def get_access_key():
	st = 'qwertyuiopasdfghjklzxcvbnm1234567890'
	code = ''
	for i in range(8):
		code = f'{code}{st[rand(0, len(st))]}'
	return code


def get_carousel(el):
	carousel = {"type" : "carousel", "elements" : []}
	for element in el:
		carousel["elements"].append({"photo_id": element[0], "action": { "type": "open_photo" },
		"buttons": [{ "action": { "type": "text", "label": element[1], "payload": "{}" }}]})
	carousel = json.dumps(carousel, ensure_ascii = False).encode('utf-8')
	carousel = str(carousel.decode('utf-8'))
	return carousel


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


carous = get_carousel([
	["296431501_457273770", "Кейс 1 уровня (10руб)"],
	["296431501_457273771", "Кейс 2 уровня (20руб)"],
	["296431501_457273772", "Кейс 3 уровня (30руб)"]
])

clear_key = get_keyboard([])

bal_key = get_keyboard([
	[('Пополнить', 'синий'), ('Снять', 'синий')],
	[('Мой баланс', 'зеленый')],
	[('Назад', 'красный')]
])

back_key = get_keyboard([
	[('Назад', 'синий')]
])

menu_key = get_keyboard([
	[('Играть', 'зеленый'), ('Баланс', 'синий')]
])


def sender(id, text, key):
	vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'message' : text, 'random_id' : 0, 'keyboard' : key})


def send_car(id, text, car):
	vk_session.method('messages.send', {
			'user_id' : id,
			'message' : text,
			'random_id' : 0,
			'attachment' : [],
			'template' : car
		})


users = []


def pay(number, score):# выплата
	print(f'Выплачено {score}руб по номеру {number}')
	# выплата score рублей на номер number


def get_transactions():
	global users
	last = 0
	while True:
		pass # проверка последнего платежа по токену пользователя


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
							if id == user.id:
								sender(id, 'Выберите действие:', menu_key)
								user.mode = 'menu'
								flag = 1
						if flag == 0:
							sender(id, 'Выберите действие:', menu_key)
							users.append(User(id = id, cash = 30, mode = 'menu', number = 0, access_key = 'None'))

					else:
						for user in users:
							if id == user.id:


								if user.mode == 'menu':

									if msg  == 'играть':
										sender(id, 'Выберите действие:', back_key)
										send_car(id, 'Выберите кейс:', carous)
										user.mode = 'game'

									elif msg == 'баланс':
										sender(id, 'Выберите действие:', bal_key)
										user.mode = 'balance'


								elif user.mode == 'game':

									if msg == 'кейс 1 уровня (10руб)':
										if user.cash >= 10:
											user.cash -= 10
											bonus = rand(5, 16)
											user.cash += bonus
											send_car(id, f'Вы выиграли {bonus} рублей!\nВыберите кейс:', carous)
											print('1')
										else:
											sender(id, f'У вас недостаточно средств!\nВаш баланс: {user.cash}\nВы можете пополнить баланс через QIWI.', menu_key)
											user.mode = 'menu'

									elif msg == 'кейс 2 уровня (20руб)':
										if user.cash >= 20:
											user.cash -= 20
											bonus = rand(15, 26)
											user.cash += bonus
											send_car(id, f'Вы выиграли {bonus} рублей!\nВыберите кейс:', carous)
											print('2')
										else:
											sender(id, f'У вас недостаточно средств!\nВаш баланс: {user.cash}\nВы можете пополнить баланс через QIWI.', menu_key)
											user.mode = 'menu'

									elif msg == 'кейс 3 уровня (30руб)':
										if user.cash >= 30:
											user.cash -= 30
											bonus = rand(25, 36)
											user.cash += bonus
											send_car(id, f'Вы выиграли {bonus} рублей!\nВыберите кейс:', carous)
											print('3')
										else:
											sender(id, f'У вас недостаточно средств!\nВаш баланс: {user.cash}\nВы можете пополнить баланс через QIWI.', menu_key)
											user.mode = 'menu'

									elif msg == 'назад':
										sender(id, 'Выберите действие:', menu_key)
										user.mode = 'menu'


								elif user.mode == 'balance':

									if msg == 'назад':
										sender(id, 'Выберите действие:', menu_key)
										user.mode = 'menu'

									elif msg == 'пополнить':
										sender(id, 'Для пополнения баланса переведите сумму на QIWI на номер: 89294046340\nПосле перевода средств, ваш баланс в боте пополнится в течении 5 минут.\nВведите номер телефона, с которого придет оплата(по QIWI):', clear_key)
										user.mode = 'upload1'

									elif msg == 'снять':
										if user.cash >= 100:
											sender(id, 'Введите телефонный номер своего qiwi, на который выведется баланс:', clear_key)
											user.mode = 'upload2'
										else:
											sender(id, f'Минимальная сумма вывода: 100руб\nВаш баланс: {user.cash}руб', bal_key)

									elif msg == 'мой баланс':
										sender(id, f'Ваш баланс: {user.cash}', bal_key)


								elif user.mode == 'upload1': # пополнение
									if (msg.startswith('8')) or (msg.startswith('7')):
										if (len(msg) == 11)&(msg.isdigit()):
											user.number = msg
											user.access_key = get_access_key()
											sender(id, f'Номер введён верно!\n!!!Внимание!!!\nДля корректной проверки платежа вы должны отправить код "{user.access_key}" в комментарии при переводе!', bal_key)
											user.mode = 'balance'

									elif msg.startswith('+'):
										if (len(msg) == 12)&(msg[1::].isdigit()):
											user.number = msg
											user.access_key = get_access_key()
											sender(id, f'Номер введён верно!\n!!!Внимание!!!\nДля корректной проверки платежа вы должны отправить код "{user.access_key}" в комментарии при переводе!', bal_key)
											user.mode = 'balance'

									else:
										sender(id, 'Неверный номер!', bal_key)
										user.mode = 'balance'


								elif user.mode == 'upload2': # вывод
									if (msg.startswith('8')) or (msg.startswith('7')):
										if (len(msg) == 11)&(msg.isdigit()):
											user.number = msg
											score = (user.cash-50)
											try:
												pay(user.number, score)
												user.cash -= score
												sender(id, f'Номер введён верно!\nОжидайте выплаты на QIWI на номер {msg}\nСумма выплаты: {score}', bal_key)
											except Exception as e:
												sender(id, 'Не удалось вывести средства!\nПроизошла ошибка при переводе!\nВозможные причины:\n1) Сбой в работе бота\n2) Вы не подтвердили паспортные данные своего кошелька QIWI\nПроверьте свой QIWI кошелёк или попробуйте позже!', bal_key)
											user.mode = 'balance'

									elif msg.startswith('+'):
										if (len(msg) == 12)&(msg[1::].isdigit()):
											user.number = msg
											score = (user.cash-50)
											try:
												pay(user.number, score)
												user.cash -= score
												sender(id, f'Номер введён верно!\nОжидайте выплаты на QIWI на номер {msg}\nСумма выплаты: {score}', bal_key)
											except Exception as e:
												sender(id, 'Не удалось вывести средства!\nПроизошла ошибка при переводе!\nВозможные причины:\n1) Сбой в работе бота\n2) Вы не подтвердили паспортные данные своего кошелька QIWI\nПроверьте свой QIWI кошелёк или попробуйте позже!', bal_key)
											user.mode = 'balance'

									else:
										sender(id, 'Неверный номер!', bal_key)
										user.mode = 'balance'


	except Exception as e:
		print('Произошла ошибка, идёт переподключение к серверу вк...')
		vk_session = vk_api.VkApi(token = tok)
		longpoll = VkLongPoll(vk_session)