#!/usr/bin/env python3

# Questo file manipola chiavi "sets" redis

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
TestoPagina="Aggiunge un gruppo di allarmi (chiave Redis)"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
ExecFile="/cgi-bin/writesetsredis.py"
# Redis "key"
RedisKey = "sets:*"  # chiavi, ma in realta` e` settata piu` avanti
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
print ("Non ho rinominato i campi e non sono stato a riordinare le voci.<br/>")


form=cgi.FieldStorage()

# In realta` questo script non viene eseguito da un'altro che passa parametri,
# quindi le 4 righe seguenti potrei eliminarle.
if FormName not in form:
	pass
else:
	RedisKey = html.escape(form[FormName].value)

print ("<h2>","<center>","Filtra chiave Redis","</center>","</h2>")
print ("Puoi usare i caratteri \"*\" e \"?\", esempi:<br/>")
print ("*stringa*, *stringafinale, *stringacon3caratterifinali???<br/><br/>")

# Inizio del form
print (mhl.MyActionForm("/cgi-bin/readsetsredis.py","POST"))

print ("<table>")   # 2 colonne

print ("<tr>")
print ("<td>")
print ("Inserisci il filtro:")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm(FormName,RedisKey,"40","required",""))   #	Ho messo 40, ma un chiave puo` arrivare a 125 caratteri (se non ricordo male)
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td colspan=\"2\">")
#print ("<hr/>") # La linea orizzontale
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("")  # Testo nella 1a colonna
print ("</td>")
print ("<td>")
print (mhl.MyButtonForm("submit","Attiva filtro"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())

print ("<hr/><br/>")

# Tabella visualizzazione chiavi:valore
print ("<table>")

# La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
print ("<tr>")
print ("<td>")
print ("<b>Key/s: ",RedisKey,"</b>")
print ("</td>")
print ("<td>")
print ("<b>Type : Value</b>")
print ("</td>")
print ("</tr>")

# Per ogni campo ... stampo il campo ed il suo valore. (la funzione "Decode()" serve per trasformare "bin->str")
for i in MyDB.keys(RedisKey):
    print ("<tr>")
    print ("<td>")
    #print (flt.Decode(i),": ",sep="")
    print (flt.Decode(i))
    print ("</td>")
    print ("<td>")
    # Ho dovudo decodificare due volte per leggere la stringa del tipo di chiave e controllarne l'uguaglianza
    if flt.Decode(MyDB.type(flt.Decode(i))) == "hash":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.hgetall(flt.Decode(i)))
    elif flt.Decode(MyDB.type(flt.Decode(i))) == "string":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.get(flt.Decode(i)))
    elif flt.Decode(MyDB.type(flt.Decode(i))) == "list":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.llen(flt.Decode(i)),"valori, il primo e`: ",MyDB.lindex(flt.Decode(i),"0"))
    elif flt.Decode(MyDB.type(flt.Decode(i))) == "sets":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.smembers(flt.Decode(i)))
    else:
        print (MyDB.type(flt.Decode(i)),": ","Non ancora contemplata")
    print ("</td>")
    print ("</tr>")

print ("</table>")
# Fine


print ("<hr/><br/>")


print ("<h2>","<center>","Modifica chiave Redis","</center>","</h2>")

# Inizio del form
print (mhl.MyActionForm("/cgi-bin/changesetredis.py","POST"))

print ("<table>")   # 2 colonne

print ("<tr>")
print ("<td>")
print ("Seleziona la chiave da modificare:")
print ("</td>")
print ("<td>")
print (mhl.MyDropDown(FormName,flt.DecodeList(MyDB.keys(RedisKey)),""))   #
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td colspan=\"2\">")
#print ("<hr/>") # La linea orizzontale
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


print ("<hr/><br/>")


print ("<h2>","<center>","Eliminazione chiave Redis","</center>","</h2>")
print ("<strong><center>ATTENZIONE: Non ci sara` una richiesta di conferma</center></strong><br/>")

# Inizio del form
print (mhl.MyActionForm("/cgi-bin/deletekeyredis.py","POST"))

print ("<table>")   # 2 colonne

print ("<tr>")
print ("<td>")
print ("Seleziona la chiave da eliminare:")
print ("</td>")
print ("<td>")
print (mhl.MyDropDown(FormName,flt.DecodeList(MyDB.keys(RedisKey)),""))   #
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td colspan=\"2\">")
#print ("<hr/>") # La linea orizzontale
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("")  # Testo nella 1a colonna
print ("</td>")
print ("<td>")
print (mhl.MyButtonForm("submit","ELIMINA"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())


# End web page
print (mhl.MyHtmlBottom())
