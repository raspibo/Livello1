#!/usr/bin/env python3

# Questo file legge il file di configurazione,
# trova e modifica il parametro eseguendo il rispettivo "write*.py"

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie Json, Html, flt (Thermo(Redis))
import mjl, mhl, flt

import redis,os,time #

import glob	# Prima volta che lo uso

# Parametri generali
TestoPagina="Manipolazione files .csv"
# ConfigFile
#DirBase="/var/www"
#ConfigFile=DirBase+"/conf/config.json"
ViewFile="/cgi-bin/viewpagegraph.py"
CopyFile="/cgi-bin/copypagegraph.py"
DeleteFile="/cgi-bin/deletepagegraph.py"
# Redis "key"
#RedisKey = ""
# Directory's (lista)
Dirs = ["../", "../archive/"]
# Forms
FormName = "file"
FileName = ""
NewFormName = "newfile"
NewFileName = ""+time.strftime("%y%m%d%H%M%S")+".csv"

# Apro il database Redis con l'istruzione della mia libreria
#MyDB = flt.OpenDBFile(ConfigFile)

# Cerco
# Prima quelli della "archive", poi aggiungo in testa quella della www
FileList = glob.glob(Dirs[1]+"*.csv")
FileList[0:0] = glob.glob(Dirs[0]+"*.csv")

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("""
Seleziona il file del grafico che vuoi visualizzare.
<br/>
<br/>
""")

# Inizio del form
print (mhl.MyActionForm(ViewFile,"GET"))	# Ho usato il GET invece del POST per utilizzare il refresh nel "view" (ma serve ?)

print ("<table>")

print ("<tr>")
print ("<td>")
print (mhl.MyDropDown(FormName,FileList,""))
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
#print ("<hr/>")
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
print (mhl.MyButtonForm("submit","Visualizza"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())


print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("""
Seleziona il file del grafico che vuoi salvare e scrivi il nome del file di destinazione.
<br/>
<em>La directory di destinazione e` prefissata/preimpostata ad "archive".</em>
<br/>
<br/>
""")

FilesList = glob.glob(Dirs[0]+"*.csv")	# Rifaccio la lista per i soli files nella root

# Inizio del form
print (mhl.MyActionForm(CopyFile,"POST"))

print ("<table>")

print ("<tr>")
print ("<td>")
print (mhl.MyDropDown(FormName,FilesList,""))
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
print (mhl.MyTextForm(NewFormName,NewFileName,"40","",""))	# Ho messo un nome diverso alla form, vedi copypagegraph.py
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
#print ("<hr/>")
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
print (mhl.MyButtonForm("submit","Copia"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())


print ("<hr/>","<br/>")


# Eventuale help/annotazione
print ("""
<b>Seleziona files "grafici" da eliminare</b>
<br/>
""")

# Inizio del form
print (mhl.MyActionForm(DeleteFile,"POST"))

print ("<table>")

print ("<tr>")
print ("<td>")
#print (mhl.MyDropDown(FormName,FileList,""))
for i in range (len(FileList)):
	print (mhl.MyCheckboxForm(FormName,FileList[i]),FileList[i],"<br/>")
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
#print ("<hr/>")
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
print (mhl.MyButtonForm("submit","ELIMINA"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())


# End web page
print (mhl.MyHtmlBottom())