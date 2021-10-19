import amino
import random
import multiprocessing as mp
import time
import requests
from urllib.request import urlopen
import json
from colorama import Fore, Back, Style
from colorama import init
init()

accounts = {
				'email1': 'password1',
				'email2': 'password2',
				'...': '...',
				'emailn': 'passwordn'
			} #Аккаунты для команды whf

def sub(client: amino.Client):
	subclients = []
	subnames = []
	i = 1
	for subname, subid in zip(client.sub_clients(size=100).name, client.sub_clients(size=100).comId):
		print(f'{i}. {subname}: {subid}')
		i += 1
		subclients.append(subid)
		subnames.append(subname)

	print('\n')
	choice = int(input('Your choice: '))
	community = subclients[choice-1]
	communityname = subnames[choice-1]
	print(f'You choosed {community}, {communityname}\n')

	return amino.SubClient(comId = community, profile = client.profile)

def whf(comId: str, chatId: str, email: str, password: str):
	client = amino.Client()
	client.login(email = email, password = password)

	subclient = amino.SubClient(comId = comId, profile = client.profile)

	try:
		client.join_video_chat_as_viewer(comId = comId, chatId = chatId)
		client.send_action(comId = comId, chatId = chatId, actions = ["Chatting"])
		print(1)
		subclient.activity_status('on')
	except Exception as e:
		print(f'{email}: {e}')
	print(f'{email}: готово')


def main():
	antiraid = False

	email = input('Email >> ')
	password = input('Password >> ')
	client = amino.Client()
	client.login(email = email, password = password)

	subclient = sub(client)
	print(f"{Fore.YELLOW}{Style.BRIGHT}Emerald Dream\n{Fore.CYAN}Введите help для списка команд.")

	@client.event("on_text_message")
	def on_text_message(data):
		if antiraid:
			if data.message.type not in [0, None]:
				try:
					print(f'{data.message.chatId}: {data.message.author.nickname}: {data.message.type}')
					subclient.kick(chatId = data.message.chatId, userId = data.message.author.userId, allowRejoin = False)
					subclient.delete_message(chatId = data.message.chatId, messageId = data.message.messageId)
				except Exception as e:
					print(e)

	while True:
		print(f'{Fore.WHITE}')
		command = input(f'>> ')
		command = command.split(' ')

		if command[0] == 'help':
			print(f"""{Fore.YELLOW} Строение команд. [Обязательный ввод] (Необязательный ввод)\n
	При вводе не ставить скобки.\n
	\n
> {Fore.GREEN}help - Информация о командах.\n 
> {Fore.GREEN}getchat [количество] - Получение айди чатов.\n 
> {Fore.GREEN}getinfo user [айди пользователя] [получение данных(см. lib.util.objects.py)] - Информация о пользователе.\n 
> {Fore.GREEN}getinfo chat [айди чата] [получение данных(см objects.py)] - Информация о чате.\n 
> {Fore.GREEN}getmsg [айди чата] [количество сообщений] [получение данных(см objects.py)] - Информация о сообщении.\n 
> {Fore.GREEN}deletemsg [айди чата] [айди сообщений] - Удаление сообщения(требуется роль помощника/ведущего).\n 
> {Fore.GREEN}kick [айди чата] [айди сообщений] (с галкой(true),без(false)) - Удаление участника(требуется роль помощника/ведущего).\n 
> {Fore.GREEN}antiraid [on/off] - Включает/выключает антирейд.\n
> {Fore.GREEN}sendmessage [чат] [тип сообщения] [сообщений] - Отправка сообщения в чат.\n 
> {Fore.GREEN}changecom - сменить сообщество.\n 
> {Fore.GREEN}tag user [чат] [пользователь] [сообщение]- Отметка участника в чате.\n 
> {Fore.GREEN}tag all [чат] [сообщение] - Отметка всех участников в чате.\n 
> {Fore.GREEN}copybubble [чат] [айди сообщения] - Копирование пузыря чата.\n 
> {Fore.GREEN}whf [чат] - Запуск ботов в голосовой чат/кинозал в режиме зрителя.\n 
> {Fore.GREEN}startvc [чат] - Запуск голосового чата.\n 
> {Fore.GREEN}endvc [чат] - Закрытие голосового чата.\n 
> {Fore.GREEN}vcjointype [чат] [тип разрешения(0,1,2)] - Разрешение захода в гч/кз.\n 	
> {Fore.GREEN}reputation get [чат] - Данные о накопившейся репутации(только для вашего кз).\n
> {Fore.GREEN}reputation claim [чат] - Получить репутации без закрытия кз.
			""")

		if command[0] == 'getchat':
			try: 
				chats = subclient.get_chat_threads(size = int(command[1]))
				for chatName, chatId in zip(chats.title, chats.chatId):
					print(f"{Fore.YELLOW}{chatName}  \n  {Fore.GREEN}{chatId}\n")
			except: 
				print('Ошибка.')	

		if command[0] == 'getinfo':
			if command[1] == 'user':
				try:
					print(getattr(subclient.get_user_info(userId = command[2]), command[3]))
				except Exception as e:
					print(e)
			if command[1] == 'chat':
				try: 
					thread = subclient.get_chat_thread(chatId = command[2])
					print(getattr(thread, command[3]))
				except Exception as e:
					print(e)

		if command[0] == 'getmsg':

			try:
				msgList = subclient.get_chat_messages(chatId = command[1], size = int(command[2]))
				if '.' in command[3]:
					command[3] = command[3].split('.')
					for author, attr in zip(msgList.author.nickname, getattr(getattr(msgList, command[3][0]), command[3][1])):
						print(f'{Fore.YELLOW}{author}: {Fore.GREEN}{attr}')
				else:
					for author, attr in zip(msgList.author.nickname, getattr(msgList, command[3])):
						print(f'{Fore.YELLOW}{author}: {Fore.GREEN}{attr}')

			except Exception as e:
				print(f'Ошибка\n{e}')

		if command[0] == 'deletemsg':
			try:
				subclient.delete_message(chatId = command[1], messageId = command[2])
			except Exception as e:
				print(e)			

		if command[0] == 'kick':
			try:
				if command[3]:
					subclient.kick(chatId = command[1], userId = command[2], allowRejoin = not command[3].lower() in ['1', 'true'])
				else:
					subclient.kick(chatId = command[1], userId = command[2])
			except Exception as e:
				print(e)

		if command[0] == 'antiraid':
			if command[1] == 'on':
				antiraid = True
				print(f'{Fore.RED}Антирейд включен.')
			elif command[1] == 'off':
				antiraid = False
				print(f'{Fore.RED}Антирейд выключен.')

		if command[0] == 'sendmessage':
			try: 
				msg = ' '.join(map(str, command[3:]))
				subclient.send_message(chatId = command[1], message = msg, messageType = int(command[2]))
				print(f'{command[3:]}: отправлено.')
			except Exception as e: 
				msg = ' '.join(map(str, command[3:]))
				print(f'{msg}: не отправлено. \n ошибка: {e}')

		if command[0] == 'changecom':
			try:
				subclient = sub(client)
			except Exception as e:
				print(e)

		if command[0] == 'tag':
			if command[1] == 'user':
				try:
					message = ' '.join(map(str, command[4:]))
					subclient.send_message(chatId = command[2], message = f'<${message}$>', mentionUserIds = [command[3]])
				except Exception as e:
					print(e)

			elif command[1] == 'all':
				try:
					message = ' '.join(map(str, command[3:]))
					subclient.send_message(chatId = command[2], message = f'<${message}$>', mentionUserIds = subclient.get_chat_users(chatId = command[2], size = 1000).userId)
				except Exception as e:
					print(e)

		if command[0] == 'copybubble':
			try:
				bubbleUrl = subclient.get_message_info(chatId = command[1], messageId = command[2]).json['chatBubble']['resourceUrl']

				with urlopen(bubbleUrl) as file:
					data = file.read()

				bubble = requests.post(f"https://service.narvii.com/api/v1/x{subclient.comId}/s/chat/chat-bubble/templates/107147e9-05c5-405f-8553-af65d2823457/generate", data = data, headers = client.parse_headers())
				bubbleId = json.loads(bubble.text)['chatBubble']['bubbleId']
				print(f"Установление пузыря с айди {bubbleId}")
				bubblePost = requests.post(f"https://service.narvii.com/api/v1/x{subclient.comId}/s/chat/chat-bubble/{bubbleId}", data = data, headers = client.parse_headers())

				if bubblePost.status_code == 200:
					print('Копирование пузыря прошло успешно!')
				else:
					print('Произошла ошибка.')

			except Exception as e:
				print(e)

		if command[0] == 'whf':

			variables = {}
			try:
				for i, j in zip(range(len(accounts)), accounts):
					variables[i] = mp.Process(target = whf, args = (subclient.comId, command[1], j, accounts[j]))
				for i in range(len(variables)):
					variables[i].start()
				time.sleep(10)
			except Exception as e:
				print(e)

		if command[0] == 'startvc':
			try: client.start_vc(comId = community, chatId = command[1], joinType = int(command[2]))
			except Exception as e: print(e) 

		if command[0] == 'endvc':
			try: client.end_vc(comId = community, chatId = command[1])
			except Exception as e: print(e) 

		if command[0] == 'vcjointype':
			try: subclient.vc_permission(chatId = command[1], permission = int(command[2]))
			except Exception as e: print(e) 

		if command[0] == 'reputation':
			if command[1] == 'get':
				try:
					print(f'{Fore.CYAN}Репутаций: {subclient.get_vc_reputation_info(chatId = command[2]).availableReputation}')
				except Exception as e:
					print(e)
			elif command[1] == 'claim':
				try:
					reputations = subclient.get_vc_reputation_info(chatId = command[2]).availableReputation
					subclient.claim_vc_reputation(chatId = command[2])
					print(f'{Fore.CYAN}Вы собрали {reputations} репутаций!')
				except Exception as e:
					print(e)

if __name__ == '__main__':
	main()