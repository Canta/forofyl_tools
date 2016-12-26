#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import getpass
import math
from bs4 import BeautifulSoup
import json
import time
import os

def debug(texto):
  print "[" + str(time.strftime("%H:%M:%S")) + "] - " + str(texto)

def yes_no(texto):
    reply = str(raw_input(texto+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
      return yes_no(texto)

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

if not os.path.isdir("./posts_backup"):
  os.makedirs("./posts_backup")

files  = [f for f in os.listdir("./posts_backup") if os.path.isfile(os.path.join("./posts_backup", f))]
files.sort()

if len(files) > 0 :
  ultimo = files[ len(files) - 1 ].split(".")[1]
  if yes_no("Continuar desde " + ultimo + "" ):
    while str( links[actual]["post_id"] ) != ultimo :
      actual = actual + 1


while actual < total:
  debug("Procesando #" + str(links[actual]["post_id"]) + " (" + str(actual+1) + "/" + str(total) + "): " + links[actual]["url"] )

  try:
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
    tries = 0
    actual = actual + 1
  except Exception, e:
    debug("Error: " + str(e))
    if tries < 3 :
      tries = tries + 1
    else:
      debug("Salteándoselo por repetición de errores.")
      errs   = open("errores.txt", "a")
      errs.write( str(links[actual]["post_id"]).encode("utf-8") + " : " + unicode(e) + "\n")
      errs.close()
      tries  = 0
      actual = actual + 1

response  = session.get( forum + "/ucp.php?mode=logout")

debug("Proceso finalizado.")
