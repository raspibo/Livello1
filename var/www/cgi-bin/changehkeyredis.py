#!/usr/bin/env python3

# Questo file modifica chiavi "hash" redis
# Predisposto per segnali di I/O

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
TestoPagina="Modifica chiave \"hash\" Redis"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
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
print ("Non e` possibile modificare il nome della chiave (ovviamente), il valore e la data.<br/>")
print ("Tutti gli altri, non sono parametri obbligatori (ad oggi).<br/>")
print ("""
<ul>

<li>Descrizione</li>
  <ul>
	<li>Inserire una breve descrizione dell'oggetto, utile per ricordarselo meglio</li>
  </ul>

<li>UM (unita` di misura)</li>
  <ul>
	<li>Non che sia importante, e` usata nei messaggi di allarme</li>
  </ul>

<li>TempoRitardo</li>
  <ul>
	<li>Usare se il segnale e` utile sia da considerarsi attendibile dopo n.nnn secondi</li>
  </ul>

<li>RangeValori</li>
  <ul>
	<li>Dipende che cos'e`, se un digitale, puo` essere solamente "0" o "1", quindi indicare "0,1", altrimenti ...</li>
	<li>Vengono emessi avvisi se il valore e` impostato</li>
  </ul>

<li>ValoreMin</li>
  <ul>
	<li>Dipende che cos'e`, se un digitale, puo` essere solamente "0", altrimenti ...</li>
	<li>Vengono emessi avvisi se il valore e` impostato</li>
  </ul>

<li>ValoreMax</li>
  <ul>
	<li>Dipende che cos'e`, se un digitale, puo` essere solamente "1", altrimenti ...</li>
	<li>Vengono emessi avvisi se il valore e` impostato</li>
  </ul>

<li>ValoreOn</li>
  <ul>
	<li>Solitamente "1", ma potrebbe trattarsi di un sensore negato, in qual caso "0"</li>
	<li>Vengono emessi avvisi se il valore e` impostato</li>
  </ul>

<li>Allarme</li>
  <ul>
	<li>Definre qui i valori che sono presi come allarme, per esempio: ValoreOn,ValoreMin</li>
	<li>Se sono impostati, ma non indicati negli allarmi, sono emessi dei semplici avvisi</li>
  </ul>

<li>TempoErrore</li>
  <ul>
	<li>E` espresso in secondi (es.: 1 ora = 3600, 2 ore = 7200)</li>
	<li>Usare per controllare che il dato arrivi</li>
	<li>Utile per verificare corretto funzionamento del "remote" (potrebbe essersi bloccato, per esempio per mancanza di alimentazione)</li>
  </ul>


</ul>
""")
print ("<hr/>") # La linea orizzontale


form=cgi.FieldStorage()

try:
	RedisKey = html.escape(form[FormName].value)	# Assegno alla chiave prima di ...
except:
	print ("Errore: Non hai passato nessun valore")
	exit()


# Controllo se la chiave esiste e se esiste il parametro essenziale: valori (che sono di una chiave modificabile da questa routine).
if (flt.Decode(MyDB.type(RedisKey)) == "hash" and MyDB.exists(RedisKey) and MyDB.hexists(RedisKey,"Valori")):
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
	print ("Valori:")
	print ("</td>")
	print ("<td>")
	print (mhl.MyTextForm("Valori",flt.Decode(MyDB.hget(RedisKey,"Valori")),"40","","readonly"))   # DEVE ESISTERE, altrimenti qualcosa non va ?
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("UM (Unita` di misura):")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"UM"):
		print (mhl.MyTextForm("UM",flt.Decode(MyDB.hget(RedisKey,"UM")),"5","",""))   # Non richiesto
	else:
		print (mhl.MyTextForm("UM","","5","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("TempoRitardo:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"TempoRitardo"):
		print (mhl.MyNumberForm("TempoRitardo",flt.Decode(MyDB.hget(RedisKey,"TempoRitardo")),"6","6","0","99","0.001","",""))   # Non richiesto
	else:
		print (mhl.MyNumberForm("TempoRitardo","","6","6","0","99","0.001","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("RangeValori:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"RangeValori"):
		print (mhl.MyTextForm("RangeValori",flt.Decode(MyDB.hget(RedisKey,"RangeValori")),"10","",""))   # Non richiesto
	else:
		print (mhl.MyTextForm("RangeValori","","10","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("ValoreMin:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"ValoreMin"):
		#                        Name,      Value,                             Size,Maxlenght,Min,Max,Step,Required,Readonly
		print (mhl.MyNumberForm("ValoreMin",flt.Decode(MyDB.hget(RedisKey,"ValoreMin")),"10","10","-1023","1023","0.001","",""))   # Non richiesto
	else:
		print (mhl.MyNumberForm("ValoreMin","","10","10","-1023","1023","0.001","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("ValoreMax:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"ValoreMax"):
		print (mhl.MyNumberForm("ValoreMax",flt.Decode(MyDB.hget(RedisKey,"ValoreMax")),"10","10","-1023","1023","0.001","",""))   # Non richiesto
	else:
		print (mhl.MyNumberForm("ValoreMax","","10","10","-1023","1023","0.001","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("ValoreOn:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"ValoreOn"):
		print (mhl.MyNumberForm("ValoreOn",flt.Decode(MyDB.hget(RedisKey,"ValoreOn")),"2","2","0","1","1","",""))   # Non richiesto
	else:
		print (mhl.MyNumberForm("ValoreOn","","2","2","0","1","1","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("Allarme:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"Allarme"):
		print (mhl.MyTextForm("Allarme",flt.Decode(MyDB.hget(RedisKey,"Allarme")),"20","",""))   # Non richiesto
	else:
		print (mhl.MyTextForm("Allarme","","20","",""))   # Non richiesto
	print ("</td>")
	print ("</tr>")
	
	print ("<tr>")
	print ("<td>")
	print ("TempoErrore:")
	print ("</td>")
	print ("<td>")
	if MyDB.hexists(RedisKey,"TempoErrore"):
		# def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
		print (mhl.MyNumberForm("TempoErrore",flt.Decode(MyDB.hget(RedisKey,"TempoErrore")),"5","5","0","28800","60","",""))   # Non richiesto
	else:
		print (mhl.MyNumberForm("TempoErrore","","5","5","0","28800","60","",""))   # Non richiesto
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
