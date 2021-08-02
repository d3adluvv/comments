APP_VERSION = 0.1
import vk_api
from requests import post, get
import time
import json
import sys
from random import choice

def installUpdate():
    r = get('https://raw.githubusercontent.com/insan1tyyy/comments/main/comments.py').text
    with open('comments.py', 'w') as f:
        f.write(r)
    print("Обновление успешно установлено! Запусти скрипт заново.")
    return

def checkUpdates():
    r:str = get('https://raw.githubusercontent.com/insan1tyyy/comments/main/comments.py').text
    r = r.split('\r\n', maxsplit=1)[0]
    app_ver = float(r.replace('APP_VERSION = ', ''))
    if APP_VERSION < app_ver:
        confirm = input("Доступно обновление. Чтобы установить - нажми ENTER, Чтобы пропустить - напиши любой символ")
        if not confirm:
            installUpdate()
        else:
            return

checkUpdates()


with open('config.json', 'r') as f:
    config = json.load(f)

def login() -> str:
    while True:
        token = input("Введи токен: ")
        try:
            user = vk_api.VkApi(token=token).get_api().users.get()[0]
            name = '{} {}'.format(user['first_name'], user['last_name'])
            print(f'Успешная авторизация как {name} !')
            return token

        except vk_api.exceptions.VkApiError:
            print('Неверный токен.')
            continue

if not config['token']:
    config['token'] = login()
    with open('config.json', 'w') as f: 
        json.dump(config, f, indent = 4)

vk = vk_api.VkApi(token=config['token']).get_api()


def newComments() -> list:
    comments = input("Введи новый текст для комментов. Чтобы разделить текст, поставь ; (Пример: Hello world; Bye world; i want some candies)\n\n>>> ").split(';')
    return comments

def answerComments():
    a = input("Если хочешь вставить новый текст для комментариев, введи любой символ, иначе нажми ENTER, оставив поле пустым.\n\n>>> ")
    if a:
        config['comments'] = newComments()
        with open('config.json', 'w') as f:
            json.dump(config, f, indent = 4)
        return
    else:
        return

if not config['comments']:
    config['comments'] = newComments()
    with open('config.json', 'w') as f:
        json.dump(config, f, indent = 4)
else:
    answerComments()

post_id = vk.wall.get()['items'][0]['id']

start = time.time()
commentList = config['comments']
print('\n\nНачинаю накрутку...')
while True:
    msg = choice(commentList)
    try:
        vk.wall.createComment(post_id = post_id, message = msg)
        print(f'[' + str(round(time.time() - start, 3)) + f'] Comment added: "{msg}" comment count: ' + str(vk.wall.get()['items'][0]['comments']['count']))
    except vk_api.exceptions.Captcha as e:
        print(f'[' + str(round(time.time() - start, 3)) + f'] Comment error: CAPTCHA. trying to sleep 300s...')
        time.sleep(300)
    


