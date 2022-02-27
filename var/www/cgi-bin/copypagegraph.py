#!/usr/bin/env python3

# Copia file

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
TestoPagina="Copia file "
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
NewFormName = "newfile"
NewFileName = ""

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

form=cgi.FieldStorage()

if FormName not in form:
	print ("<h3>Manca il valore: </h3>",FormName)
else:
	FileName = html.escape(form[FormName].value)

TestoPagina = TestoPagina + FileName


# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("...............<br/><br/>")

if NewFormName not in form:
	print ("<h3>Manca il valore: </h3>",NewFormName)
else:
	NewFileName = html.escape(form[NewFormName].value)
	print("Copia del file in corso ...<br/>")
	try:
		shutil.copy(FileName,Dirs[1]+NewFileName)
		print("<br/>... completato.<br/><hr/>")
	except:
		print("""
<br/>
<b>Operazione non riuscita!!!</b>
<br/>
<b>Hai messo una directory e/o hai specificato un nome di file non valido ?
</b>
<br/><hr/>
""")

print ("<h2>Report:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
print ("<tr>")
print ("<td>")
print (FileName)
print ("</td>")
print ("<td>")
print (Dirs[1]+NewFileName)
print ("</td>")
print ("</tr>")
print ("</table>")


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