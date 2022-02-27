#!/usr/bin/env python3

# Questo file legge/visualizza le chiavi redis (e se richiesto ...)

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
TestoPagina="Visualizzazione delle chiavi memorizzate in Redis"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
ExecFile="/cgi-bin/selectkeysredis.py"
# Redis "key"
RedisKey = "*"  # Tutte le chiavi, ma in realta` e` settata piu` avanti
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
In questa pagina puoi visualizzare le 'chiavi' del database ed il contenuto.
</p>
<p>
Vista la possibilita` di filtrare, ho previsto qua la sezione per alcune
manipolazioni.
</p>
<p>
Non sono stato a riordinare le voci.
</p>
<p>
I filtri di programma sono impostati al tipo di chiave, ma potrebbero esserci delle
incongruenze, per esempio, non e` detto che tutte le chiavi di tipo 'hash' siano
da modificare con la richiesta di questa pagina. Daltronde, e` ancora una versione
provvisoria ;) .
</p>
<hr/>
""")

form=cgi.FieldStorage()

if FormName not in form:
	pass
else:
	RedisKey = html.escape(form[FormName].value)

print ("<h2>","<center>","Filtra chiave Redis","</center>","</h2>")
print ("Puoi usare i caratteri \"*\" e \"?\", esempi: ")
print ("*stringa*, *stringafinale, *stringacon3caratterifinali???<br/>")

# Preselezioni
print ("<p>Preselezioni</p>")

# Questi pulsanti richiamano questo file con "valori" preimpostati
print (mhl.MyActionForm("","POST"))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"*:Temperatura:*\">".format(FormName))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"*:Umidita:*\">".format(FormName))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"*:Pioggia:*\">".format(FormName))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"*:MotionDect:*\">".format(FormName))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"*Valori\">".format(FormName))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"sets:*\">".format(FormName))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"*:graph:*\">".format(FormName))
print ("<input type=\"submit\" name=\"{0:s}\" value=\"*:alarms:*\">".format(FormName))
print ("</form>")

# Filtro
print (mhl.MyActionForm("","POST"))
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
# Creo le opportune variabili per le selezioni/modifiche delle forms seguenti
RedisKeyString=[]
RedisKeyHash=[]
RedisKeyList=[]
RedisKeySet=[]
for i in MyDB.keys(RedisKey):
    print ("<tr>")
    print ("<td>")
    print (flt.Decode(i))
    print ("</td>")
    print ("<td>")
    # Ho dovudo decodificare due volte per leggere la stringa del tipo di chiave e controllarne l'uguaglianza
    if flt.Decode(MyDB.type(flt.Decode(i))) == "hash":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.hgetall(flt.Decode(i)))
        RedisKeyHash.append(flt.Decode(i))
    elif flt.Decode(MyDB.type(flt.Decode(i))) == "string":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.get(flt.Decode(i)))
        RedisKeyString.append(flt.Decode(i))
    elif flt.Decode(MyDB.type(flt.Decode(i))) == "list":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.llen(flt.Decode(i)),"valori, l'ultimo e`: ",MyDB.lindex(flt.Decode(i),"-1"))
        RedisKeyList.append(flt.Decode(i))
    elif flt.Decode(MyDB.type(flt.Decode(i))) == "set":
        print (MyDB.type(flt.Decode(i)),": ",MyDB.smembers(flt.Decode(i)))
        RedisKeySet.append(flt.Decode(i))
    else:
        print (MyDB.type(flt.Decode(i)),": ","Non ancora contemplata")
    print ("</td>")
    print ("</tr>")

print ("</table>")
# Fine tabella visualizzazione

#print ("<hr/><br/>")
print ("<hr/>")


print ("<h2>","<center>","Modifica chiave Redis","</center>","</h2>")


# Inizio del form
# Modifica HASH
print (mhl.MyActionForm("/cgi-bin/changehkeyredis.py","POST"))
print ("""
<p>
In questa sezione puoi selezionare per modificare le chiavi "hash",
sono quelle delle utenze collegate (per esempio: sensori di presenza,
sonde di temperatura, ...
</p>
""")

print ("<table>")   # 2 colonne

print ("<tr>")
print ("<td>")
print ("Seleziona la chiave \"hash\" da modificare:")
print ("</td>")
print ("<td>")
# In effetti, questo puo` modificare si gli "hash", ma solamente le chiavi I/O, quindi si dovrebbe cambiare il filtro.
#print (mhl.MyDropDown(FormName,flt.DecodeList(MyDB.keys(RedisKey)),""))
print (mhl.MyDropDown(FormName,RedisKeyHash,""))
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


#print ("<hr/><br/>")
print ("<br/>")


# Inizio del form
# Modifica HASH
print (mhl.MyActionForm("/cgi-bin/changehkeyconfig.py","POST"))
print ("""
<p>
In questa sezione puoi selezionare per modificare le chiavi "hash",
sono quelle realtive ai gruppi di allarme (sets:alarms:*:Config)
</p>
""")

print ("<table>")   # 2 colonne

print ("<tr>")
print ("<td>")
print ("Seleziona la chiave \"hash\" da modificare:")
print ("</td>")
print ("<td>")
# In effetti, questo puo` modificare si gli "hash", ma solamente le chiavi I/O, quindi si dovrebbe cambiare il filtro.
#print (mhl.MyDropDown(FormName,flt.DecodeList(MyDB.keys(RedisKey)),""))
print (mhl.MyDropDown(FormName,RedisKeyHash,""))
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


#print ("<hr/><br/>")
print ("<br/>")


# Inizio del form
# Modifica SETS
print (mhl.MyActionForm("/cgi-bin/changesetsredis.py","POST"))
print ("""
<p>
In questa sezione puoi selezionare per modificare le chiavi "sets",
sono i gruppi di utenze che hai creato, un gruppo di sensori allarme,
uno di temperature, .. ("sets:[alarms,graph]:*")
</p>
""")

print ("<table>")   # 2 colonne

print ("<tr>")
print ("<td>")
print ("Seleziona la chiave \"sets\" da modificare:")
print ("</td>")
print ("<td>")
# In effetti, questo puo` modificare si i "sets", ma solamente i gruppi alarms/graph, quindi si dovrebbe cambiare il filtro.
#print (mhl.MyDropDown(FormName,flt.DecodeList(MyDB.keys(RedisKey)),""))
print (mhl.MyDropDown(FormName,RedisKeySet,""))
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


#print ("<hr/><br/>")
print ("<br/>")


# Inizio del form
# Analisi e Modifica LISTS
print (mhl.MyActionForm("/cgi-bin/analistsredis.py","POST"))
print ("""
<p>
In questa sezione puoi selezionare per analizzare e modificare le chiavi "lists",
sono praticamente le chiavi "Valori" delle utenze.
</p>
""")

print ("<table>")   # 2 colonne

print ("<tr>")
print ("<td>")
print ("Seleziona la chiave \"lists\" da modificare:")
print ("</td>")
print ("<td>")
#print (mhl.MyDropDown(FormName,flt.DecodeList(MyDB.keys(RedisKey)),""))
print (mhl.MyDropDown(FormName,RedisKeyList,""))
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
print (mhl.MyButtonForm("submit","Analizza e Modifica"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())


#print ("<hr/><br/>")
print ("<hr/>")


print ("<h2>","<center>","Eliminazione chiave Redis","</center>","</h2>")
print ("<strong><center>ATTENZIONE: Non ci sara` una richiesta di conferma</center></strong>")

# Inizio del form
print (mhl.MyActionForm("/cgi-bin/deletekeyredis.py","POST"))
print ("""
<p>
In questa sezione puoi selezionare per eliminare, qualsiasi chiave.
</p>
<p>
La selezione e` dipendente dal filtro in uso.
</p>
""")

print ("<table>")   # 2 colonne

# Sono ideciso, questa versione, dove comanda il filtro:
#print ("<tr>")
#print ("<td>")
#print ("<b>Chiavi selezionate per l'eliminazione:</b>")
#print ("</td>")
#print ("<td>")
#for i in range (len(flt.DecodeList(MyDB.keys(RedisKey)))):
#	print (mhl.MyTextForm(FormName,flt.DecodeList(MyDB.keys(RedisKey))[i],"50","required","readonly"))
#print ("</td>")
#print ("</tr>")

# .. o questa versione, dove, oltre al filtro, si devono anche selezionare una per una:
print ("<tr>")
print ("<td>")
print ("<b>Seleziona le chiavi da eliminare:</b>")
print ("</td>")
print ("<td>")
for i in range (len(flt.DecodeList(MyDB.keys(RedisKey)))):
	print (mhl.MyCheckboxForm(FormName,flt.DecodeList(MyDB.keys(RedisKey))[i]),flt.DecodeList(MyDB.keys(RedisKey))[i],"<br/>")
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
