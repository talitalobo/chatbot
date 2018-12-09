
import random
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Button
from persist import insert

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEJZBM7qpfcBAOyZC4OZCHAqLCdn0av4FbDlKTywy4sgiqwH6O0pASb8Lhyfmwy8yhtsMhPOZB3E4HZCXrS2RUexmCbpW3peT6VDYd8VMVV3pazZAy5cZBNZC7G7OplfaPVnM9IRVfcZBhXKccXrNEcOhA8BmjDz0d0ZA2IUGZBdqkeRgjZCkzFUqZB0'
VERIFY_TOKEN = 'mcjJsvg6S4'
bot = Bot(ACCESS_TOKEN)
teste = 1
resposta = ''
placa_carro = ''
url_imagem = ''
nome_orgao = ''


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    global teste
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        if teste == 1: 
            first_int()
        elif teste == 2:
            second_int()
        elif teste == 3:
            ter_int()
        elif teste == 4:
            quar_int()
        elif teste == 5:
            quin_int()
        if  teste > 5:
            teste = 1
        

        

    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def first_int():
    global teste
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            recipient_id = message['sender']['id']                
            button_message(recipient_id)
            teste += 1

def second_int():
    global teste
    global resposta
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('postback'):
            recipient_id = message['sender']['id']
            resposta = message['postback']['payload']
            if resposta == "Sim":
               send_message(recipient_id, 'Muito bem, informe a placa do veículo.')
               teste += 1
            elif resposta == "Não":
                send_message(recipient_id,'Infelizmente só estamos trabalhando com informação de veículos oficiais no momento!')            
                teste = 1

def ter_int():
    global teste
    global placa_carro
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            recipient_id = message['sender']['id']  
            placa_carro = message['message']['text']
            print(placa_carro)
            send_message(recipient_id,'Ok! Informe a qual órgão público pertence este veículo! ')
            teste += 1


def quar_int():
    global teste
    global nome_orgao
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            recipient_id = message['sender']['id']  
            nome_orgao = message['message']['text']
            send_message(recipient_id,'Ok! Anexe a imagem da ocorrência! ')
            teste += 1

def quin_int():
    global teste
    global url_imagem
    global placa_carro
    global nome_orgao
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            if message['message'].get('attachments'):
                attachments = message['message']['attachments']
                recipient_id = message['sender']['id']
                url_imagem = attachments[0]['payload']['url']
                insert(placa_carro,nome_orgao,url_imagem)
                send_message(recipient_id,'Obrigado pelo seu apoio!!')
                teste += 1



def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

def button_message(recipient_id):
    buttons = []
    button = Button(title='Sim', type='postback', payload='Sim')
    buttons.append(button)
    button = Button(title='Não', type='postback', payload='Não')
    buttons.append(button)
    text = 'Olá, você gostaria de reportar o uso indevido de um veículo público? Para isto você precisará informar a placa do veículo e ter uma foto do flagrante. '
    bot.send_button_message(recipient_id, text, buttons)    
    
if __name__ == "__main__":
    app.run()