import re
import json
from youtube import BuscadorYoutube
import youtube_dl
import urllib2, urllib

def youtube_url_validation(url):
	youtube_regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

	youtube_regex_match = re.match(youtube_regex, url)
	if youtube_regex_match:
		return youtube_regex_match.group(6)
	#if

	return youtube_regex_match
#youtube_url_validation()

'''b = BuscadorYoutube()
print b.buscar("rito pls")['nome']'''


a = urllib2.urlopen('file:' + urllib.pathname2url('musicas/Metallica - Ronnie Rising Medley (A Tribute To Dio) HQ.mp3'))
print a

