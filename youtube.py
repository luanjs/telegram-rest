#coding: utf-8

from apiclient.discovery import build
from apiclient.errors import HttpError

DEVELOPER_KEY = "AIzaSyCOCnj2CFR3wdYBHzi2paDyR7bZkj9gsLY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class BuscadorYoutube():

  def youtube_search(self, termo):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
      q=termo,
      part="id,snippet",
      maxResults=1
    ).execute()

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        #videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
        return {"id": search_result["id"]["videoId"], "nome": search_result["snippet"]["title"]}
      #if
    #for

    return {"erro": "algum erro"}
  #youtube_search()

  def buscar(self, termo):
    try:
      return self.youtube_search(termo)
    except HttpError, e:
      return False
    #except
  #buscar()

#BuscadorYoutube()