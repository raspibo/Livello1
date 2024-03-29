#!/usr/bin/env python3

# Questo file legge il file di configurazione,
# trova e modifica il parametro eseguendo il rispettivo "write*.py"

# Serve per la parte di gestione html in python
import cgi
import cgitb
import html

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie Json, Html, flt (Thermo(Redis))
import mjl, mhl, flt

import redis,os,glob,shutil


# Parametri generali
TestoPagina="Elimina file "
#ConfigFile=""
ViewFile="/cgi-bin/viewpagegraph.py"
SaveFile="/cgi-bin/savepagegraph.py"
DeleteFile="/cgi-bin/deletepagegraph.py"
# Redis "key"
#RedisKey = ""
# Directory's (lista)
Dirs = ["../", "../archive/"]
# Forms
FormName = "file"
FileName = ""
#NewFormName = "newfile"
#NewFileName = ""

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

#form=cgi.FieldStorage()

#if FormName not in form:
#	print ("<h3>Manca il valore: </h3>",FormName)
#else:
#	FileName = html.escape(form[FormName].value)

TestoPagina = TestoPagina + FileName


# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("...............<br/><br/>")

#if FileName == "":
#	pass
#else:
#	print("Eliminazione del file in corso ...<br/>")
#	os.remove(FileName)
#	print("<br/>... completato.<br/><hr/>")

form=cgi.FieldStorage()

for i in form.keys():
	if i not in form:							# Non ci sara` mai
		print ("<h3>Manca il valore: </h3>",i)
	elif i == FormName:
		for j in form.getlist(FormName):
			print ("Error:")
			print (os.remove(j))
			print (", <b>file eliminato:</b> ",j,"<br/>")
	else:
		print ("<h3>Cosa e` successo ? Questo e` il valore in form: </h3>",i)


"""
print ("<h2>Report:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
print ("<tr>")
print ("<td>")
print (FileName)
print ("</td>")
print ("<td>")
print ("")
print ("</td>")
print ("</tr>")
print ("</table>")
"""


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
print ("<button type=\"button\" onclick='location.href=\"/cgi-bin/selectpagegraph.py\"'>Indietro</button>")
print ("</td>")
print ("<td>")
print ("")  # Testo nella 3a colonna
print ("</td>")
print ("</tr>")

print ("</table>")



# End web page
print (mhl.MyHtmlBottom())