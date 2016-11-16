#!/usr/bin/env python3

# Questo file modifica le chiavi "hash" redis
#
# Prima verifica che ci sia la chiave nel form
# Si 'parsa' tutte le "name" in "form" per verificare ed inserirle se presenti
# Teoricamente dovrebbe funzionare ogni volta che sia chiamato per la scrittura
# di una chiave di tipo "hash".

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis

# Parametri generali
TestoPagina="Aggiorna chiave Redis"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
#ExecFile="/cgi-bin/deletekeyredis.py"
# Redis "key"
RedisKey = "*"  # Tutte le chiavi
# Form name/s
FormName = "rkey"

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
#print ("Non ho rinominato i campi e non sono stato a riordinare le voci.<br/>")


form=cgi.FieldStorage()


if "key" not in form:
	print ("<h2>ERRORE: Non e` stata passata la chiave Redis</h2>")
else:
	RedisKey = cgi.escape(form["key"].value)
	# Se sono stati eliminati dei parametri, e` piu` facile eliminare la chiave e poi reinserire i dati.
	MyDB.delete(RedisKey)
	for i in form.keys():
		if i not in form:							# Non ci sara` mai
			print ("<h3>Manca il valore: </h3>",i)
		elif cgi.escape(form[i].value) == "":		# Non sara` mai verificata
			print ("<h3>Non e` stato inserito un valore per </h3>",i)
		elif i == "key":
			pass	# e` la chiave, l'ho manipolata inizialmente
		else:
			MyDB.hset(RedisKey,i,cgi.escape(form[i].value))
	
	print ("<h2>Dati inseriti/modificati:</h2>")
	print ("<br>")
	print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
	print ("<tr>")
	print ("<td>")
	print (RedisKey)
	print ("</td>")
	print ("<td>")
	print (MyDB.hgetall(RedisKey))
	print ("</td>")
	print ("</tr>")
	print ("</table>")


# End web page
print (mhl.MyHtmlBottom())
