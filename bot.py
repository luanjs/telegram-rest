#encoding: utf8
import json, requests, pprint, telepot, urllib2, sys
from time import strftime

# Configurando a codificação de todo o programa para UTF-8
reload(sys)
sys.setdefaultencoding('utf8')

LINK_API = "http://www.youtubeinmp3.com/fetch/?format=JSON&video="
LINK_BASE_YOUTUBE = "https://www.youtube.com/"

# Forçando request e urllib2 a não usarem proxy
proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
session = requests.Session()
session.trust_env = False

class TelegramTutorial(telepot.Bot):

    def __init__(self, token):
        super(TelegramTutorial, self).__init__(token)
    #__init__()

    def handle_message(self, msg):
        if 'text' not in msg:
            return
        #if

        if msg['text'].startswith('/'):
            self.handle_command(msg)
        else:
			self.handle_link(msg)
        #else
    #handle_message()

    def handle_link(self, msg):
		
		r = session.get(LINK_API + msg['text'])
		
		if r.status_code == 200:
			dados = json.loads(r.text)
			self.sendMessage(msg['chat']['id'], "Requisição recebida\nNome: {}\nProcessando, isso pode levar alguns minutos...".format(dados['title']))
			self.sendAudio(msg['chat']['id'], (dados['title'] + ".mp3", urllib2.urlopen(dados['link'])))
			self.sendMessage(msg['chat']['id'], "Tudo feito!\nObrigado por ter utilizado! \nDesenvolvido por J.Ricardo")
		else:
			self.sendMessage(msg['chat']['id'], "Algo deu errado, verifique se o link está correto :/")
		#else
	#handle_link()

    def handle_start(self, msg):
        self.sendMessage(msg['chat']['id'], "Esse bot deveria servir pra baixar músicas...")
    #handle_start()

    def handle_time(self, msg):
        self.sendMessage(msg['chat']['id'], strftime("Data: %d/%m/%Y\nHora: %H:%M:%S"))
    #handle_time()

    def handle_command(self, msg):
        method = 'handle_' + msg['text'][1:]
        if hasattr(self, method):
            getattr(self, method)(msg)
        #if
    #handle_command()

    def runBot(self):
        last_offset = 0
        print('Ouvindo...')

        while True:
            updates = self.getUpdates(timeout=60, offset=last_offset)

            if updates:
                for aux in updates:
                    self.handle_message(aux['message'])
                #for
                last_offset = updates[-1]['update_id'] + 1
            #if
        #while
    #runBot()
#TelegramTutorial

if __name__ == "__main__":
	bot = TelegramTutorial('222171717:AAE12Wc1KoTcGPdGAAnekmJwXc902JPgEv0')
	bot.runBot()
#if
