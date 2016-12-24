#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import getpass
import math
from bs4 import BeautifulSoup

print "Nombre de usuario: "
username  = raw_input()
password  = getpass.getpass()

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

print "Items por página: " + str(per_page)
print "Items totales:    " + str(total)
print "Páginas:          " + str( math.ceil( float(total) / float(per_page) ) ) 

soup      = BeautifulSoup( response.text.encode("utf-8") , "lxml")
links     = []

for item in soup.find_all("h3"):
  tmp = {}
  a   = item.find("a")
  tmp["url"]      = a["href"]
  tmp["titulo"]   = a.text
  links.append(tmp)

print links

response  = session.get( forum + "/ucp.php?mode=logout")
