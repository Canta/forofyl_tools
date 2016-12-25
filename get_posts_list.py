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

debug("Iniciando la lectura de la lista de posts del usuario.")

forum     = "http://forofyl.com.ar/"

headers   = {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"'}
payload   = {'username': username, 'password': password, 'redirect':'index.php', 'sid':'', 'login':'Login'}
session   = requests.Session()


session.headers = headers

response  = session.post(forum + "ucp.php?mode=login", data=payload)

response  = session.get( forum + "/ucp.php")

author_id = response.text.split("href=\"./search.php?author_id=")[1].split("&")[0]

response  = session.get( forum + "/search.php?st=0&sk=t&sd=d&sr=posts&author_id=" + author_id + "&start=0")

per_page  = int(response.text.split("per_page = '")[1].split("';")[0])
total     = int(response.text.split("<h2>Se encontraron ")[1].split(" coincidencias</h2>")[0])
paginas   = str( math.ceil( float(total) / float(per_page) ) ) 

print "Items por página: " + str( per_page )
print "Items totales:    " + str( total    )
print "Páginas:          " + str( paginas  ) 

soup      = BeautifulSoup( response.text.encode("utf-8") , "lxml")
links     = []

actual    = 0 
while actual < total:
  actual  = actual + per_page

  debug("Procesando items " + str(actual - per_page) + " a " + str(actual) + ".")
  for item in soup.find_all("h3"):
    tmp = {}
    a   = item.find("a")
    
    tmp["url"]      = a["href"]
    tmp["titulo"]   = a.text
    tmp["post_id"]  = a["href"].split("#p")[1]
    links.append(tmp)

  # Siguiente página
  response  = session.get( forum + "/search.php?st=0&sk=t&sd=d&sr=posts&author_id=" + author_id + "&start=" + str(actual) )
  soup      = BeautifulSoup( response.text.encode("utf-8") , "lxml")

output  = json.dumps(links, indent = 4, ensure_ascii=False , sort_keys = True)
outfile = open( str(author_id) + '.posts.txt', 'w')
outfile.write(output.encode("utf-8"))
outfile.close()

response  = session.get( forum + "/ucp.php?mode=logout")

debug("Proceso finalizado.")
