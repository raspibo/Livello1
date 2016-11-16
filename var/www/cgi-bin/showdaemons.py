#!/usr/bin/env python3

# Questo file visualizza i programmi attivi (daemons ?)

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis,subprocess

# Parametri generali
TestoPagina="Daemons"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
ExecFile="/cgi-bin/startstopdaemons.py"
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
print ("<p><b>Ricordati di salvare i dati che non vuoi perdere.</b></p>")
print ("""
<p>
Ogni volta che avvii un programma automatico, alcuni files sono prima eliminati
e poi sovrascritti dai nuovi dati.
</p>
<p>
Questo perche` potrebbe essere cambiato il numero di utenze controllate,
e per la parte "grafica", si tradurrebbe in una incongruenza dei dati.
</p>
<p>
<b>ATTENZIONE</b>: Ho scelto (per ora) di non eliminare la chiave "*:Valori", quindi,
se e` cambiato il numero delle utenze collegate, questa lista conterra`
dei valori incongruenti (puoi eliminarla utilizzando l'apposita pagina di
manipolazione).
</p>
""")
print ("""
<p><b>Ricordati di salvare i dati che non vuoi perdere</b>
(Mi riferisco in particolare ai .csv, perche` saranno sovrascritti).</p>
""")
print ("<br/>")	# Riga vuota / no linea orizzonatale


form=cgi.FieldStorage()

if FormName not in form:
	pass
else:
	RedisKey = cgi.escape(form[FormName].value)

# Demone principale
# Deve sempre girare, quindi non e` previsto che si possa avviare/fermare (per ora)
print ("<fieldset>")
print ("<legend>mqtt2redis</legend>")
print (flt.Decode(subprocess.check_output(['/var/www/cgi-bin/mqtt2redis_init.d.sh','status'])))
#print ("<hr>")
print ("</fieldset>")

# NON FUNZIONA, credo per un'istruzione del programma, quel cilent.loop_forever()
#print (mhl.MyActionForm("/cgi-bin/mqtt2redis_webstart.py","POST"))
#print (mhl.MyButtonForm("submit","Start"))
#print (mhl.MyActionForm("/cgi-bin/mqtt2redis_webstop.py","POST"))
#print (mhl.MyButtonForm("submit","Stop"))

print ("<br/>")	# Riga vuota / no linea orizzonatale
print ("<br/>")	# Riga vuota / no linea orizzonatale

# Gruppi Redis
# Non riesco a filtrare con una normale 'regex', mi son stufato e allora prendo tutti
# quelli che hanno "sets:*:Config" e poi eliminero` il finale ":Config"
SetsRedis = flt.DecodeList(MyDB.keys("sets:*:Config"))
for i in range (len(SetsRedis)):
	# La lista e` (uguale alla lista puntata da i [i]),
	# presa per tutta la sua lunghezza di caratteri [:L-7],
	# tolto 7, che e` la lunghezza di ":Config"
	SetsRedis[i] = SetsRedis[i][:len(SetsRedis[i])-7]
SetsRedisOn=[]
SetsRedisOff=[]
print ("<fieldset>")
print ("<legend>Gruppi GRAPH</legend>")
for i in range (len(SetsRedis)):
	Appoggio=flt.Decode(subprocess.check_output(['/var/www/cgi-bin/setsgraph_init.d.sh','status',SetsRedis[i]]))
	print ("<b>", SetsRedis[i], "</b>", Appoggio, "<br/><hr/>")
	# .split()	Divido le parole
	# [-1]	Prendo l'ultima
	# try int()	Intero ? 
	try:
		int(Appoggio.split()[-1])
		SetsRedisOn.append(SetsRedis[i])
	except ValueError as e:
		SetsRedisOff.append(SetsRedis[i])
print ("</fieldset>")

# Inizio del form
print (mhl.MyActionForm(ExecFile,"POST"))

print ("<table>")   # 2 colonne

# La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
print ("<tr>")
print ("<td>")
print ("Start:")
print ("</td>")
print ("<td>")
print ("<fieldset>")								# Ho usato il "fieldset" come separatore/raggruppatore
print ("<legend>Seleziona i demoni da avviare</legend>")
for i in range (len(SetsRedisOff)):
	print (mhl.MyCheckboxForm("start",SetsRedisOff[i]), SetsRedisOff[i], "<br/>")
print ("</fieldset>")
#print ("<hr/>")	# Mi sa che serve un separatore, senno` ci si confonde
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Stop:")
print ("</td>")
print ("<td>")
print ("<fieldset>")
print ("<legend>Seleziona i demoni da fermare</legend>")
for i in range (len(SetsRedisOn)):
	print (mhl.MyCheckboxForm("stop",SetsRedisOn[i]), SetsRedisOn[i], "<br/>")
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
print (mhl.MyButtonForm("submit","Esegui"))
print ("</td>")
print ("</tr>")

print ("</table>")

# End form
print (mhl.MyEndForm())


# Gruppi Redis
# Non riesco a filtrare con una normale 'regex', mi son stufato e allora prendo tutti
# quelli che hanno "sets:*:Config" e poi eliminero` il finale ":Config"
SetsRedis = flt.DecodeList(MyDB.keys("sets:*:Config"))
for i in range (len(SetsRedis)):
	# La lista e` (uguale alla lista puntata da i [i]),
	# presa per tutta la sua lunghezza di caratteri [:L-7],
	# tolto 7, che e` la lunghezza di ":Config"
	SetsRedis[i] = SetsRedis[i][:len(SetsRedis[i])-7]
SetsRedisOn=[]
SetsRedisOff=[]
print ("<fieldset>")
print ("<legend>Gruppi ALARMS</legend>")
for i in range (len(SetsRedis)):
	Appoggio=flt.Decode(subprocess.check_output(['/var/www/cgi-bin/setsalarms_init.d.sh','status',SetsRedis[i]]))
	print ("<b>", SetsRedis[i], "</b>", Appoggio, "<br/><hr/>")
	# .split()	Divido le parole
	# [-1]	Prendo l'ultima
	# try int()	Intero ? 
	try:
		int(Appoggio.split()[-1])
		SetsRedisOn.append(SetsRedis[i])
	except ValueError as e:
		SetsRedisOff.append(SetsRedis[i])
print ("</fieldset>")

# Inizio del form
print (mhl.MyActionForm("/cgi-bin/startstopdaemonsalarms.py","POST"))

print ("<table>")   # 2 colonne

# La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
print ("<tr>")
print ("<td>")
print ("Start:")
print ("</td>")
print ("<td>")
print ("<fieldset>")								# Ho usato il "fieldset" come separatore/raggruppatore
print ("<legend>Seleziona i demoni da avviare</legend>")
for i in range (len(SetsRedisOff)):
	print (mhl.MyCheckboxForm("start",SetsRedisOff[i]), SetsRedisOff[i], "<br/>")
print ("</fieldset>")
#print ("<hr/>")	# Mi sa che serve un separatore, senno` ci si confonde
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Stop:")
print ("</td>")
print ("<td>")
print ("<fieldset>")
print ("<legend>Seleziona i demoni da fermare</legend>")
for i in range (len(SetsRedisOn)):
	print (mhl.MyCheckboxForm("stop",SetsRedisOn[i]), SetsRedisOn[i], "<br/>")
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
print (mhl.MyButtonForm("submit","Esegui"))
print ("</td>")
print ("</tr>")

print ("</table>")

# End form
print (mhl.MyEndForm())


# End web page
print (mhl.MyHtmlBottom())
