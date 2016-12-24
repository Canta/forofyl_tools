#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import getpass

print "Nombre de usuario: "
username  = raw_input()
password  = getpass.getpass()

forum     = "http://forofyl.com.ar/"

headers   = {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"'}
payload   = {'username': username, 'password': password, 'redirect':'index.php', 'sid':'', 'login':'Login'}
session   = requests.Session()

session.headers = headers

response  = session.post(forum + "ucp.php?mode=login", data=payload)

flogin.write( response.text.encode("utf-8") )

response  = session.get( forum + "/viewforum.php?f=9")

response  = session.get( forum + "/ucp.php?mode=logout")

