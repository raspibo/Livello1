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

import redis

# Parametri generali
TestoPagina="Taglia valori da chiave \"lists\" Redis"
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
elif "VStart" not in form:
	print ("<h3>Manca il valore: Start</h3>")
elif "VStop" not in form:
	print ("<h3>Manca il valore: Stop</h3>")
else:
	RedisKey = html.escape(form[FormName].value)
	print ("<b>Prima:</b>")
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
	
	print ("<tr>")
	print ("<td>")
	print ("Primo valore:")
	print ("</td>")
	print ("<td>")
	print (str(MyDB.lindex(RedisKey,"0")))
	print ("</td>")
	print ("</tr>")
	
	print ("<br/>")	# Aggiungo uno spazio (una riga)
	
	print ("<tr>")
	print ("<td>")
	print ("Valori:")
	print ("</td>")
	print ("<td>")
	print (str(MyDB.llen(RedisKey)))
	print ("</td>")
	print ("</tr>")
	
	print ("<br/>")	# Aggiungo uno spazio (una riga)
	
	print ("<tr>")
	print ("<td>")
	print ("Ultimo valore:")
	print ("</td>")
	print ("<td>")
	print (str(MyDB.lindex(RedisKey,"-1")))
	print ("</td>")
	print ("</tr>")
	
	print ("</table>")
	
	RedisKeyStart = html.escape(form["VStart"].value)
	RedisKeyStop = html.escape(form["VStop"].value)
	print ("</br></br> <b>Command</b>: ltrim {0:s} {1:s} {2:s} </br></br></br>".format(RedisKey,RedisKeyStart,RedisKeyStop))
	if MyDB.ltrim(RedisKey,RedisKeyStart,RedisKeyStop):
		print ("<b>Dopo:</b>")
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
		
		print ("<tr>")
		print ("<td>")
		print ("Primo valore:")
		print ("</td>")
		print ("<td>")
		print (str(MyDB.lindex(RedisKey,"0")))
		print ("</td>")
		print ("</tr>")
		
		print ("<br/>")	# Aggiungo uno spazio (una riga)
		
		print ("<tr>")
		print ("<td>")
		print ("Valori:")
		print ("</td>")
		print ("<td>")
		print (str(MyDB.llen(RedisKey)))
		print ("</td>")
		print ("</tr>")
		
		print ("<br/>")	# Aggiungo uno spazio (una riga)
		
		print ("<tr>")
		print ("<td>")
		print ("Ultimo valore:")
		print ("</td>")
		print ("<td>")
		print (str(MyDB.lindex(RedisKey,"-1")))
		print ("</td>")
		print ("</tr>")
		
		print ("</table>")


# End web page
print (mhl.MyHtmlBottom())
