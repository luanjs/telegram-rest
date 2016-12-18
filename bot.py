#encoding: utf8
import json, requests, pprint, telepot, urllib2, urllib, sys, re, youtube_dl, io, os, threading
from time import strftime
from youtube import BuscadorYoutube
from cinebot import Cine
from letrasbot import Api

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
    'format': 'bestaudio/best',              # qualidade
    'outtmpl': '/musicas/%(id)s.%(ext)s',    # nome de saida
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

		vazio = True
		for aux in nomeMusica:
			if aux != "":
				vazio = False
			#if
		#for

		if vazio == True:
			self.sendMessage(msg['chat']['id'], "Verifique se enviou os dados no formato certo!")
			return
		#if

		buscador = BuscadorYoutube()
		res = buscador.buscar(nomeMusica)

		msg['text'] = 'http://www.youtube.com/watch?v=' + res['id']
        
		return self.handle_link(msg) 
	#handle_musica()

	def handle_info(self, msg):
		nomeFilme = msg['text'].split("/info")[1].strip()

		vazio = True
		for aux in nomeFilme:
			if aux != "":
				vazio = False
			#if
		#for

		if vazio == True:
			self.sendMessage(msg['chat']['id'], "Verifique se enviou os dados no formato certo!")
			return
		#if

		api = Api()
		info = json.loads(json.loads(api.infoFilme(nomeFilme)))

		if info['Response'] == "True":
			res = '''Nome: {}\nAno: {}\nTamanho: {}\nMetascore: {}\nIMDB: {}\n
			'''.format(info['Title'], info['Year'], info['Runtime'], info['Metascore'], info['imdbRating'])

			self.sendMessage(msg['chat']['id'], res)
		else:
			self.sendMessage(msg['chat']['id'], "Esse filme provavelmente não existe!")
		#else
	#handle_info()

	def handle_letra(self, msg):
		try:
			aux = msg['text'].split("/letra")[1].strip().split("-")
			api = Api()
			letra = api.letraMusica(aux[0].strip(), aux[1].strip())

			if letra == "":
				self.sendMessage(msg['chat']['id'], "Algo deu errado, verifique se os dados estão corretos :(")
			else:
				self.sendMessage(msg['chat']['id'], letra)
			#else
		except:
			self.sendMessage(msg['chat']['id'], "Verifique se enviou os dados no formato certo, que é: \n\n/letra <nome_musica> - <nome_artista>")
		#except
	#handle_letra()

	def obterLinkFormatado(self, url):
		youtube_regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
		youtube_regex_match = re.match(youtube_regex, url)

		if youtube_regex_match:
			return youtube_regex_match.group(6)
		#if

		return youtube_regex_match
	#obterLinkFormatado()

	def handle_start(self, msg):
		aux = '''
			Bem vindo ao LJBot! Este bot tem o objetivo de fornecer diversos serviços utilitários relacionados a multimídia.

			Comandos disponíveis:\n
			/start - Exibe texto inicial de ajuda\n
			/time - Exibe a hora e data do servidor\n
			/musica <nome_musica> - Baixa uma música através de seu nome\n
			/musica <nome_musica - nome_artista> - Baixa uma música através de seu nome e do nome do artista\n
			<link_youtube> - Baixa uma música através de seu link do Youtube\n
			/letra <nome_musica - nome_artista> - Exibe a letra de uma música a partir de seu nome e do nome do artista\n
			/info <nome_filme> - Exibe as informações de um filme

		'''
		self.sendMessage(msg['chat']['id'], aux)
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
