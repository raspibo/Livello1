#!/usr/bin/env python3

# Questo file modifica chiavi "sets" redis
# Predisposto per gruppi di I (input)

# Serve per la parte di gestione html in python
import cgi
import cgitb
import html

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis

# Parametri generali
TestoPagina="Modifica chiave \"sets\" Redis"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
ExecFile="/cgi-bin/writesetsredis.py"
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
print ("Non e` possibile modificare il nome della chiave (ovviamente).<br/>")

print ("<hr/>") # La linea orizzontale


form=cgi.FieldStorage()
try:
	RedisKey = html.escape(form[FormName].value)	# Assegno alla chiave prima di ...
except:
	print ("Errore: Non hai passato nessun valore")
	exit()

# Controllo se la chiave esiste e se e` del tipo giusto
if (flt.Decode(MyDB.type(RedisKey)) == "set" and MyDB.exists(RedisKey)):
	# Inizio del form
	print (mhl.MyActionForm(ExecFile,"POST"))
	
	print ("<table>")   # 2 colonne
	
	# La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
	print ("<tr>")
	print ("<td>")
	print ("Key: ")
	print ("</td>")
	print ("<td>")
	print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
	print ("</td>")
	print ("</tr>")
	
	# A dire la verita`, per come ho sistemato ora .. questa parte e` inutile.
	print ("<tr>")
	print ("<td>")
	print ("Contenuto:")
	print ("</td>")
	print ("<td>")
	#print (str(flt.DecodeList(MyDB.smembers(RedisKey))))	# Meglio se lo visualizzo tutto, col form sarei limitato.
	LISTA = flt.DecodeList(MyDB.smembers(RedisKey))		# Appoggio a variabile l'elenco/lista
	print ("<fieldset>")								# Ho usato il "fieldset" come separatore/raggruppatore
	#print ("<legend>Contenuto</legend>")
	for i in range (len(LISTA)):
		print (LISTA[i], "<br/>")
	print ("</fieldset>")
	print ("</td>")
	print ("</tr>")
	
	print ("<br/>")	# Aggiungo uno spazio (una riga)
	
	print ("<tr>")
	print ("<td>")
	print ("Elimina:")
	print ("</td>")
	print ("<td>")
	LISTA = flt.DecodeList(MyDB.smembers(RedisKey))		# Appoggio a variabile l'elenco/lista
	print ("<fieldset>")								# Ho usato il "fieldset" come separatore/raggruppatore
	print ("<legend>Seleziona le chiavi da eliminare</legend>")
	for i in range (len(LISTA)):
		print (mhl.MyCheckboxForm("del",LISTA[i]), LISTA[i], "<br/>")
	print ("</fieldset>")
	#print ("<hr/>")	# Mi sa che serve un separatore, senno` ci si confonde
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("Aggiungi:")
	print ("</td>")
	print ("<td>")
	# Non riesco a filtrare con una normale 'regex', mi son stufato e allora prendo tutti
	# quelli che hanno ":Valori" e poi eliminero` il finale ":Valori"
	LISTA = flt.DecodeList(MyDB.keys("?:*:*:*:*:Valori"))
	print ("<fieldset>")
	print ("<legend>Seleziona le chiavi da aggiungere</legend>")
	for i in range (len(LISTA)):
		# La lista e` (uguale alla lista puntata da i [i]),
		# presa per tutta la sua lunghezza di caratteri [:L-7],
		# tolto 7, che e` la lunghezza di ":Valori"
		LISTAi=LISTA[i][:len(LISTA[i])-7]
		print (mhl.MyCheckboxForm("add",LISTAi), LISTAi, "<br/>")
	print ("</fieldset>")
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td colspan=\"2\">")
	print ("<hr/>") # La linea orizzontale
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("")  # Testo nella 1a colonna
	print ("</td>")
	print ("<td>")
	print (mhl.MyButtonForm("submit","Modifica"))
	print ("</td>")
	print ("</tr>")
	
	print ("</table>")
	
	
	# End form
	print (mhl.MyEndForm())
else:
	print ("Manca la chiave: <b>",html.escape(form[FormName].value),"</b><br/>oppure hai selezionato una chiave non modificabile.")


# End web page
print (mhl.MyHtmlBottom())
