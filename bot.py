#encoding: utf8
import json, requests, pprint, telepot, urllib2, sys, re
from time import strftime
from youtube import BuscadorYoutube

# Configurando a codificação de todo o programa para UTF-8
reload(sys)
sys.setdefaultencoding('utf8')

LINK_API = "http://www.youtubeinmp3.com/fetch/?format=JSON&video=http://www.youtube.com/watch?v={}"

# Forçando request e urllib2 a não usarem proxy
proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
session = requests.Session()
session.trust_env = False

class TelegramBot(telepot.Bot):

    def __init__(self, token):
        super(TelegramBot, self).__init__(token)
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
        link = self.obterLinkFormatado(msg['text'])

        if link:
            print LINK_API.format(link)
            r = session.get(LINK_API.format(link))

            if r.status_code == 200:
                dados = json.loads(r.text)
                self.sendMessage(msg['chat']['id'], "Requisição recebida\nNome: {}\nProcessando, isso pode levar alguns minutos...".format(dados['title']))
                musica = urllib2.urlopen(dados['link'])

                #TO BEMMMMMMM??????????
                print musica.code
                print musica.headers['content-length']

                #Combate a bugs
                if not musica.code == 200 or musica.headers['content-length'] < 22300:
                    musica = urllib2.urlopen(dados['link'])
                #if

                self.sendAudio(msg['chat']['id'], (dados['title'] + ".mp3", musica))
                self.sendMessage(msg['chat']['id'], "Tudo feito!\nObrigado por ter utilizado! \nDesenvolvido por J.Ricardo")
                return
            #if
        #if
        self.sendMessage(msg['chat']['id'], "Algo deu errado, verifique se o link está correto :/")
	#handle_link()

    def handle_musica(self, msg):
        nomeMusica = msg['text'].split("/musica")[1].strip()
        buscador = BuscadorYoutube()
        res = buscador.buscar(nomeMusica)

        msg['text'] = 'http://www.youtube.com/watch?v=' + res['id']
        
        return self.handle_link(msg) 
    #handle_musica()

    def obterLinkFormatado(self, url):
        youtube_regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_match = re.match(youtube_regex, url)

        if youtube_regex_match:
            return youtube_regex_match.group(6)
        #if

        return youtube_regex_match
    #obterLinkFormatado()

    def handle_start(self, msg):
        self.sendMessage(msg['chat']['id'], "Esse bot deveria servir pra baixar músicas...")
    #handle_start()

    def handle_time(self, msg):
        self.sendMessage(msg['chat']['id'], strftime("Data: %d/%m/%Y\nHora: %H:%M:%S"))
    #handle_time()

    def handle_command(self, msg):
        comando = msg['text'].strip().split(" ")[0].split("/")[1]
        method = 'handle_' + comando

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
#TelegramBot

if __name__ == "__main__":
	bot = TelegramBot('222171717:AAE12Wc1KoTcGPdGAAnekmJwXc902JPgEv0')
	bot.runBot()
#if
