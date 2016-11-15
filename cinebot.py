#conding: iso-8859-2
import requests
import html
import HTMLParser
import urllib2
import sys

class Cine:
    def cleanupString(self,string):
        string = urllib2.unquote(string).decode('utf8')
        return HTMLParser.HTMLParser().unescape(string).encode(sys.getfilesystemencoding())
    #cleanupString

    @property
    def filmes(self):
        r = requests.get('http://www.cineplaza.com.br/')
        h = r.text.split('}]">')
        filmes = []

        for i, item in enumerate(h):
            if i != 0:
                filmes.append(item.split("- </span>")[0].strip().decode('iso-8859-1').encode('utf8'))

        return [self.cleanupString(i) for i in filmes]
    #getFilmes
#Cine

