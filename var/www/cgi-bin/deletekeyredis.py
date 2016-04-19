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

if MyDB.exists(cgi.escape(form[FormName].value)):
    print ("<h2>Chiave eliminata:</h2>")
    #print ("<br>")
    print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")  # 1 colonna
    print ("<tr>")
    print ("<td>")
    print (cgi.escape(form[FormName].value))
    print ("</td>")
    print ("</tr>")
    print ("</table>")
    MyDB.delete(cgi.escape(form[FormName].value))
else:
    print ("<h3>Manca la chiave: </h3>",cgi.escape(form[FormName].value))


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
print ("<button type=\"button\" onclick=\"/cgi-bin/selectkeysredis.py\">Indietro</button>")
print ("</td>")
print ("<td>")
print ("")  # Testo nella 3a colonna
print ("</td>")
print ("</tr>")

print ("</table>")


# End web page
print (mhl.MyHtmlBottom())
