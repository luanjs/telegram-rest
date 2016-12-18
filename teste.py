import re
import json
from youtube import BuscadorYoutube
import youtube_dl
import urllib2, urllib
from cinebot import Cine
from letrasbot import Api

def youtube_url_validation(url):
	youtube_regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

	youtube_regex_match = re.match(youtube_regex, url)
	if youtube_regex_match:
		return youtube_regex_match.group(6)
	#if

	return youtube_regex_match
#youtube_url_validation()


api = Api()
print api.infoFilme("troia")



