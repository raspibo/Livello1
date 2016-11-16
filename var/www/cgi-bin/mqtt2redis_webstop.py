#!/usr/bin/env python3

# Questo file visualizza i programmi attivi (daemons ?)

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis,subprocess,os

# Parametri generali
TestoPagina="Stop mqtt2redis"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
ExecFile="/cgi-bin/daemons_init.d.py"
# Redis "key"
RedisKey = "*"  # Tutte le chiavi, ma in realta` e` settata piu` avanti
# Form name/s
FormName = "daemons"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Genero chiave/valori se non esiste
# Assegno dei valori piu` o meno standard
#if not MyDB.exists(RedisKey):
#    MyDB.hmset(RedisKey,{"hostname":"nessuno","port":6379,"database":0,"password":""})

# Start web page - Sono blocchi di html presenti nella libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("<br/><hr/>")


print (subprocess.call(['/var/www/cgi-bin/mqtt2redis_init.d.py','stop']))
print ("<h3>mqtt2redis_d.py stopped!</h3>")


# End web page
print (mhl.MyHtmlBottom())
