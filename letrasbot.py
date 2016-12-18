#coding: utf-8
import requests
import json

class Api:
    def _init_(self):
        pass
    def infoFilme(self, nome):
        url_base = 'http://www.imdb.com/'
        nomeFilmeDigitado = nome
        nomeFilme = "+".join(nomeFilmeDigitado.split(" "))
        pesquisa = 'http://www.omdbapi.com/?t={}&y=&plot=short&r=json'

        r = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q='+nomeFilme+'&s=all')
        link_filme =  r.text.split('class="result_text">')[1].split('" >')[0].split('<a href="')[1].strip()

        r = requests.get(url_base+link_filme)

        try:
            nomeFilme = r.text.split('class="originalTitle">')[1].split('<span')[0]
        except:
            nomeFilme = nomeFilmeDigitado


        nomeFilme = "+".join(nomeFilme.split(" "))

        r = requests.get(pesquisa.format(nomeFilme))
        return json.dumps(r.text)
    #infoFilme

    def letraMusica(self, nomeMusica, artista):
        key = '738473284fdbda1298e337a45bb40f3b'
        url = "https://api.vagalume.com.br/search.php"+"?art="+ artista+ "&mus=" + nomeMusica + "&apikey="+key
        r = requests.get(url)
        try:
            return json.loads(r.text)['mus'][0]['text']
        except:
            url = "https://api.vagalume.com.br/search.php"+"?art="+ nomeMusica+ "&mus=" + artista + "&apikey="+key
            r = requests.get(url)
            try:
                return json.loads(r.text)['mus'][0]['text']
            except:
                return ""
    #letraMusica
