#!/usr/bin/env python3

# Questo file modifica chiavi "hash" redis
# Predisposto per configurazione dei gruppi di allarme

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis

# Parametri generali
TestoPagina="Modifica chiave \"hash\" Redis"
ConfigFile="../conf/config.json"
ExecFile="/cgi-bin/writehkeyredis.py"
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
print ("""
<p>
Non e` possibile modificare il nome della chiave (ovviamente).
</p>
<p>Nessun parametro e` obbligatorio, tranne Timer.
</p>

<ul>

<li>Descrizione</li>
  <ul>
	<li>Inserire una breve descrizione, utile per ricordarselo meglio</li>
  </ul>

<li>Timer</li>
  <ul>
	<li>Tempo di campionamento per i grafici</li>
  </ul>
  <ul>
	<li>Tempo di memoria del medesimo allarme, prima di un successivo riconoscimento ed invio</li>
  </ul>

<li>Funzionamento</li>
  <ul>
	<li>Fisso a On/Off/Auto, serve per gli allarmi, in automatico si accendono/spengono alle ore designate.</li>
  </ul>

<li>Dalle</li>
  <ul>
	<li>Per gli allarmi automatici, a che ora entrano in funzione.</li>
  </ul>

<li>Alle</li>
  <ul>
	<li>Per gli allarmi automatici, a che ora si devono disattivare.</li>
  </ul>

</ul>
""")
print ("<hr/>") # La linea orizzontale


form=cgi.FieldStorage()

try:
	RedisKey = cgi.escape(form[FormName].value)	# Assegno alla chiave prima di ...
except:
	print ("Errore: Non hai passato nessun valore")
	exit()

# Controllo se la chiave esiste e se esiste il parametro essenziale: Timer (che sono di una chiave modificabile da questa routine).
if (flt.Decode(MyDB.type(RedisKey)) == "hash" and MyDB.exists(RedisKey) and MyDB.hexists(RedisKey,"Timer")):
	# Inizio del form
	print (mhl.MyActionForm(ExecFile,"POST"))
	
	print ("<table>")   # 2 colonne
	
	# La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
	print ("<tr>")
	print ("<td>")
	print ("Key: ")
	print ("</td>")
	print ("<td>")
	print (mhl.MyTextForm("key",RedisKey,"40","required","readonly"))
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("Descrizione:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"Descrizione"):
		print (mhl.MyTextForm("Descrizione",flt.Decode(MyDB.hget(RedisKey,"Descrizione")),"40","",""))   # Non richiesto
	else:
		print (mhl.MyTextForm("Descrizione","","40","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("Timer:")
	print ("</td>")
	print ("<td>")
	print (mhl.MyNumberForm("Timer",flt.Decode(MyDB.hget(RedisKey,"Timer")),"2","2","1","60","1","required",""))
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("Funzionamento:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"Funzionamento"):
		print (mhl.MyDropDown("Funzionamento",["On","Off","Auto"],flt.Decode(MyDB.hget(RedisKey,"Funzionamento"))))
	else:
		print (mhl.MyDropDown("Funzionamento",["On","Off","Auto"],"Off"))	# Non richiesto
	print ("</td>")
	print ("</tr>")
	
	# MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
	print ("<tr>")
	print ("<td>")
	print ("(Auto) dalle")
	print ("</td>")
	print ("<td>")
	print ("ore:")
	if MyDB.hexists(RedisKey,"dalleH"):
		print (mhl.MyNumberForm("dalleH",flt.Decode(MyDB.hget(RedisKey,"dalleH")),"2","2","0","23","1","",""))
	else:
		print (mhl.MyNumberForm("dalleH","","2","2","0","23","1","",""))   # Non richiesto
	print ("minuti:")
	if MyDB.hexists(RedisKey,"dalleM"):
		print (mhl.MyNumberForm("dalleM",flt.Decode(MyDB.hget(RedisKey,"dalleM")),"2","2","0","59","1","",""))
	else:
		print (mhl.MyNumberForm("dalleM","","2","2","0","59","1","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("(Auto) alle")
	print ("</td>")
	print ("<td>")
	print ("ore:")
	if MyDB.hexists(RedisKey,"alleH"):
		print (mhl.MyNumberForm("alleH",flt.Decode(MyDB.hget(RedisKey,"alleH")),"2","2","0","23","1","",""))
	else:
		print (mhl.MyNumberForm("alleH","","2","2","0","23","1","",""))   # Non richiesto
	print ("minuti:")
	if MyDB.hexists(RedisKey,"dalleM"):
		print (mhl.MyNumberForm("alleM",flt.Decode(MyDB.hget(RedisKey,"alleM")),"2","2","0","59","1","",""))
	else:
		print (mhl.MyNumberForm("alleM","","2","2","0","59","1","",""))   # Non richiesto
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
	print ("Manca la chiave: <b>",cgi.escape(form[FormName].value),"</b><br/>oppure hai selezionato una chiave non modificabile.")


# End web page
print (mhl.MyHtmlBottom())
