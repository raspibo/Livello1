#!/usr/bin/env python3

# Questo file modifica chiavi "hash" redis
# Predisposto per segnali di I/O

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie mjl (Json, Files), mhl (Html), flt (T w/ Redis)
import mjl, mhl, flt

import redis

# Parametri generali
TestoPagina="Aggiungi chiave \"sets\" Redis"
ConfigFile="../conf/config.json"
ExecFile="/cgi-bin/writesetsredis.py"
# Redis "key"
RedisKey = "sets:*"
# Form name/s
FormName = "rkey"		# Alla fine ho usato una "manuale" perche` l'EXE e` usato 'parametrizzato' anche da altri scripts

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
Questa form e` da utilizzarsi SOLO per il primo inserimento di un gruppo.<br/>

Nel campo "Key", devi digitare una nuova chiave, assegnandogli un'identificativo a piacere
(per es.: sets:allarmi:piano2), poi selezionare dalla voce "Aggiungi", una chiave fra quelle
proposte (ho messo un filtro, ma attenzione, controllare sempre), che sara` parte del gruppo
(a cui verranno poi aggiunte/eliminate altre tramite altra form).<br/>

Non ho dato la possibilita` di inserimenti multipli.<br/>

Ho previsto una notazione standard d'inserimento.<br/>
Per ogni tipologia di gruppo:<br/>
<ul>

<li>Allarmi</li>
  <ul>
  <li>Servira` per identificare un gruppo di periferiche che faranno capo ad un solo gruppo per quel che riguarda l'attivazione e disattivazione</li>
  <li>Sintassi "sets:alarms:identificativo"</li>
	<ul>
	<li>Identificativo</li>
	  <ul>
		<li>Puoi utilizzare quello che vuoi (per ora)</li>
	  </ul>
	</ul>
  </ul>

<li>Grafico</li>
  <ul>
  <li>Servira` per identificare un gruppo di sensori/utenze che saranno raggruppati nella creazione e visualizzazione di un grafico tempo/valori</li>
  <li>Sintassi "sets:graph:identificativo"</li>
	<ul>
	<li>Identificativo</li>
	  <ul>
		<li>Puoi utilizzare quello che vuoi (per ora)</li>
	  </ul>
	</ul>
  </ul>

</ul>
""")

print ("<hr/>") # La linea orizzontale

# Inizio del form
print (mhl.MyActionForm(ExecFile,"POST"))

print ("<table>")   # 2 colonne

# La prima voce (in questo raro caso ?) e` modificabile ed e` la chiave Redis
print ("<tr>")
print ("<td>")
print ("Key: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm(FormName,RedisKey,"40","required",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Aggiungi:")
print ("</td>")
print ("<td>")
#print (mhl.MyDropDown("add",flt.DecodeList(MyDB.keys("?:*:*:*:*:*[^:Valori]")),""))   # Sto` provando a filtrare le chiavi, questa e` la meglio che ho trovato.
# Non riesco a filtrare con una normale 'regex', mi son stufato e allora prendo tutti
# quelli che hanno ":Valori" e poi eliminero` il finale ":Valori"
LISTA = flt.DecodeList(MyDB.keys("?:*:*:*:*:Valori"))
for i in range (len(LISTA)):
	# La lista e` (uguale alla lista puntata da i [i]),
	# presa per tutta la sua lunghezza di caratteri [:L-7],
	# tolto 7, che e` la lunghezza di ":Valori"
	LISTAi=LISTA[i][:len(LISTA[i])-7]
	print (mhl.MyCheckboxForm("add",LISTAi), LISTAi, "<br/>")
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
print (mhl.MyButtonForm("submit","Aggiungi"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())


# End web page
print (mhl.MyHtmlBottom())
