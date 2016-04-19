#!/usr/bin/env python3

# Questo file elimina chiavi redis

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis

# Parametri generali
TestoPagina="Eliminazione chiave Redis"
ConfigFile="../conf/config.json"
#ExecFile="/cgi-bin/readkeysredis.py"
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

for i in form.keys():
	if i not in form:							# Non ci sara` mai
		print ("<h3>Manca il valore: </h3>",i)
	elif i == FormName:
		for j in form.getlist(FormName):
			print ("Deleted:")
			print (MyDB.delete(j))
			print (", ID:",j,"<br/>")
	else:
		print ("<h3>Cosa e` successo ? Questo e` il valore in form: </h3>",i)


# Prova INDIETRO

print ("<table>")   # 3 colonne

print ("<tr>")
print ("<td>")
#print ("")
print ("</td>")
print ("<td>")
#print ("")
print ("</td>")
print ("<td>")
#print ("")
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td colspan=\"3\">")
#print ("<hr/>") # La linea orizzontale
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("")  # Testo nella 1a colonna
print ("</td>")
print ("<td>")
print ("<button type=\"button\" onclick='location.href=\"/cgi-bin/selectkeysredis.py\"'>Indietro</button>")
print ("</td>")
print ("<td>")
print ("")  # Testo nella 3a colonna
print ("</td>")
print ("</tr>")

print ("</table>")


# End web page
print (mhl.MyHtmlBottom())
