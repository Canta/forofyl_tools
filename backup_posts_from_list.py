#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import getpass
import math
from bs4 import BeautifulSoup
import json
import time

def debug(texto):
  print "[" + str(time.strftime("%H:%M:%S")) + "] - " + str(texto)

print "Nombre de usuario: "
username  = raw_input()
password  = getpass.getpass()

debug("Cargando lista de posts.")

forum     = "http://forofyl.com.ar/"

headers   = {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"'}
payload   = {'username': username, 'password': password, 'redirect':'index.php', 'sid':'', 'login':'Login'}
session   = requests.Session()


session.headers = headers

response  = session.post(forum + "ucp.php?mode=login", data=payload)

response  = session.get( forum + "/ucp.php")

author_id = response.text.split("href=\"./search.php?author_id=")[1].split("&")[0]

linksfile = open(author_id + ".posts.txt", "r")
links     = json.loads( linksfile.read() )
linksfile.close()

links.sort(key=lambda x: int(x["post_id"]), reverse=False)

actual = 0
total  = len(links)

while actual < total:
  debug("Procesando #" + str(links[actual]["post_id"]) + " (" + str(actual+1) + "/" + str(total) + "): " + links[actual]["url"] )

  response          = session.get( forum + links[actual]["url"].replace("./","/") )
  tmp               = {}
  soup              = BeautifulSoup( response.text.encode("utf-8") , "lxml")
  tmp["post"]       = soup.select("#p" + str(links[actual]["post_id"]) )[0]
  content           = tmp["post"].select("#postdiv" + str(links[actual]["post_id"]))[0]
  tmp["text"]       = content.text
  tmp["html"]       = unicode( content )
  tmp["post"]       = unicode( tmp["post"] )
  # voy a buscar el bbcode
  if "quick-edit-icon" in tmp["post"]:
    payload           = {'post_id': str(links[actual]["post_id"]) }
    response          = session.post(forum + "quickedit.php", data=payload)
    response.encoding = "utf-8"
    soup2             = BeautifulSoup("<html><body>" + response.text.encode("utf-8") + "</body></html>", "lxml")
    tmp["bbcode"]     = soup2.select("#quickedit-textarea")[0].contents
  
  output  = json.dumps(tmp, indent = 4, ensure_ascii=False , sort_keys = True)
  outfile = open( "./posts_backup/" + str(author_id) + "." + str(links[actual]["post_id"]) + ".txt", 'w')
  outfile.write(output.encode("utf-8"))
  outfile.close()
  actual = actual + 1

response  = session.get( forum + "/ucp.php?mode=logout")

debug("Proceso finalizado.")
