#!/usr/bin/env python3

# Questo file visualizza la chiave "lists" redis
#
# Prima verifica che ci sia la chiave nel form

# Serve per la parte di gestione html in python
import cgi
import cgitb
import html

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis, subprocess

# Parametri generali
TestoPagina="Genera file \".csv\" dei valori di chiave \"lists\" Redis"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
#ExecFile="/cgi-bin/<exefile>"
# Redis "key"
RedisKey = "*"  # Tutte le chiavi
# Form name/s
FormName = "rkey"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Start web page - Sono blocchi di html presenti nella libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("Non ho rinominato i campi e non sono stato a riordinare le voci.<br/>")


form=cgi.FieldStorage()

if FormName not in form:
	print ("<h2>ERRORE: Non e` stata passata la chiave Redis</h2>")
else:
	RedisKey = html.escape(form[FormName].value)
	RedisKeyStart = html.escape(form["VStart"].value)
	RedisKeyStop = html.escape(form["VStop"].value)
	print ("La chiave viene passata come argomento ad un'altro programma, quindi l'unico feedback possibile e` 0 se e` andato a buon fine, o 1 se c'e` stato un'errore.</br></br>")
	print ("Comando eseguito:</br>/var/www/cgi-bin/setsVals2csv.py {0:s} {1:s} {2:s}</br></br>".format(RedisKey, RedisKeyStart, RedisKeyStop))
	print (subprocess.call(['/var/www/cgi-bin/setsVals2csv.py', RedisKey, RedisKeyStart, RedisKeyStop]))

# End web page
print (mhl.MyHtmlBottom())
