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
TestoPagina="Start/Stop Daemons"
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


form=cgi.FieldStorage()

for i in form.keys():
	if i not in form:							# Non ci sara` mai
		print ("<h3>Manca il valore: </h3>",i)
	elif i == "start":
		for j in form.getlist("start"):
			print ("Start",j,":")
			print (subprocess.call(['/sbin/start-stop-daemon','--start','--verbose', '--background', '--pidfile', '/var/run/setsgraph_d.pid', '--make-pidfile', '--startas', '/var/www/cgi-bin/setsgraph_d.py','--',j]))
	elif i == "stop":
		for j in form.getlist("stop"):
			print ("Stop",j,":")
			print (subprocess.call(['/var/www/cgi-bin/setsgraph_init.d.sh', 'stop', j]))
	else:
		print ("<h3>Cosa e` successo ? Questo e` il valore in form: </h3>",i)

# Genero il file con i "daemons" in esecuzione, come promemoria
os.system("ps -e -o cmd | grep sets:grap[h] > /var/www/daemons_graphs_running.list")


# INDIETRO

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
print ("<button type=\"button\" onclick='location.href=\"/cgi-bin/showdaemons.py\"'>Indietro</button>")
print ("</td>")
print ("<td>")
print ("")  # Testo nella 3a colonna
print ("</td>")
print ("</tr>")

print ("</table>")



# End web page
print (mhl.MyHtmlBottom())
