#encoding: utf8
import json, requests, pprint, telepot, urllib2, urllib, sys, re, youtube_dl, io, os
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

#Opcoes para download dos audios
options = {
    'format': 'bestaudio/best', # qualidade
    #'extractaudio' : True,      # manter so audio
    'outtmpl': '/musicas/%(id)s.%(ext)s',     # nome de saida
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist' : True,        # baixar somente 1 musica, nao uma playlist inteira
}

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
		video_id = self.obterLinkFormatado(msg['text'])

		if video_id:
			with youtube_dl.YoutubeDL(options) as ydl:
				#Obtém metainformações do vídeo
				meta = ydl.extract_info(video_id, download=False) 
				self.sendMessage(msg['chat']['id'], "Requisição recebida\nNome: {}\nProcessando, isso pode levar alguns minutos...".format(meta['title']))

				#Nome do arquivo
				arquivo = 'musicas/' + video_id + '.mp3'

				#Verifica se já foi baixado. Se não foi, baixa
				if os.path.isfile(arquivo) != True:
					ydl.download([video_id])
				#if

				self.sendAudio(msg['chat']['id'], (meta['title'] + ".mp3", urllib2.urlopen('file:' + urllib.pathname2url(arquivo))))
				self.sendMessage(msg['chat']['id'], "Tudo feito!\nObrigado por ter utilizado! \nDesenvolvido por J.Ricardo")
            #with
			return  
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
