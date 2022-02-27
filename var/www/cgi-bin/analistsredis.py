#!/usr/bin/env python3

# Questo file modifica chiavi "sets" redis
# Predisposto per gruppi di I (input)

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
TestoPagina="Analizza e modifica chiave \"lists\" Redis"
DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"
ExecFile="/cgi-bin/writelistsredis.py"
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
print ("Non e` possibile modificare il nome della chiave (ovviamente).<br/>")

print ("<hr/>") # La linea orizzontale


form=cgi.FieldStorage()
try:
    RedisKey = html.escape(form[FormName].value)     # Assegno alla chiave prima di ...
except:
    print ("Errore: Non hai passato nessun valore")
    exit()

# Controllo se la chiave esiste e se e` del tipo giusto
if (flt.Decode(MyDB.type(RedisKey)) == "list" and MyDB.exists(RedisKey)):
    # Inizio del form
    #print (mhl.MyActionForm(ExecFile,"POST"))  # Soppresso perche` questa volta ci sono piu` "POST"
    
    print ("<table>")   # 2 colonne
    
    # La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
    print ("<tr>")
    print ("<td>")
    print ("Key: ")
    print ("</td>")
    print ("<td>")
    print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
    print ("</td>")
    print ("</tr>")
    
    print ("<tr>")
    print ("<td>")
    print ("Primo valore:")
    print ("</td>")
    print ("<td>")
    print (str(MyDB.lindex(RedisKey,"0")))
    print ("</td>")
    print ("</tr>")
    
    print ("<br/>") # Aggiungo uno spazio (una riga)
    
    print ("<tr>")
    print ("<td>")
    print ("Valori:")
    print ("</td>")
    print ("<td>")
    print (str(MyDB.llen(RedisKey)))
    print ("</td>")
    print ("</tr>")
    
    print ("<br/>") # Aggiungo uno spazio (una riga)
    
    print ("<tr>")
    print ("<td>")
    print ("Ultimo valore:")
    print ("</td>")
    print ("<td>")
    print (str(MyDB.lindex(RedisKey,"-1")))
    print ("</td>")
    print ("</tr>")
    
    print ("<br/>") # Aggiungo uno spazio (una riga)
    
    print ("<tr>")
    print ("<td colspan=\"2\">")
    print ("<hr/>") # La linea orizzontale
    print ("</td>")
    print ("</tr>")
    
    # Visualizza
    print (mhl.MyActionForm("/cgi-bin/viewlistredis.py","POST"))
    print ("<tr>")
    print ("<td>")
    print ("Key: ")  # Testo nella 1a colonna
    print ("</td>")
    print ("<td>")
    print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
    print ("</td>")
    print ("</tr>")
    
    print ("<tr>")
    print ("<td>")
    print ("")  # Testo nella 1a colonna
    print ("</td>")
    print ("<td>")
    print (mhl.MyButtonForm("submit","Visualizza tutti i valori"))
    print ("</td>")
    print ("</tr>")
    # End form
    print (mhl.MyEndForm())
    
    print ("<tr>")
    print ("<td colspan=\"2\">")
    print ("<hr/>") # La linea orizzontale
    print ("</td>")
    print ("</tr>")
    
    # Controllo che tipo di chiave si tratta e la do` in pasto al csv con singolo valore, oppure a quello con piu` valori (sets)
    # il [:4] prende le prime 4 lettere (che vengono confrontate con sets)
    print ("<tr>")
    print ("<td colspan=\"2\">")
    print ("<h3>Crea .CSV</h3>")  # ho tolto il ritorno a capo <br/>
    print ("<b>Attenzione:</b> se la quantita` dei valori e` eccessiva, compare un'errore del web server, che non funzionera` fino al termine della creazione del file, il tempo di attesa puo` essere notevole, anche piu` di un'ora, dipende dalla mole dei dati.</br>")
    print ("Per dare un'idea, un'estrazione di 10000 valori ha impiegato circa 2 ore.</br>")
    print ("</td>")
    print ("</tr>")
    
    if RedisKey[:4] != "sets":
        # Crea CSV
        print (mhl.MyActionForm("/cgi-bin/writecsvlistredis.py","POST"))
        
        print ("<tr>")
        print ("<td>")
        print ("Key: ")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Start:")
        print ("</td>")
        print ("<td>")
        if MyDB.llen(RedisKey) >= 10000 :
                start=MyDB.llen(RedisKey)-10000
        else:
                start=0
        # def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
        print (mhl.MyNumberForm("VStart",str(start),"","","0",str(MyDB.llen(RedisKey)-1),"1","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Stop:")
        print ("</td>")
        print ("<td>")
        # def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
        print (mhl.MyNumberForm("VStop",str(MyDB.llen(RedisKey)),"","","",str(MyDB.llen(RedisKey)),"1","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyButtonForm("submit","Crea .csv (single)"))
        print ("</td>")
        print ("</tr>")
        # End form
        print (mhl.MyEndForm())
        
    else:
        # Crea CSV
        print (mhl.MyActionForm("/cgi-bin/writecsvlistsetsredis.py","POST"))
        
        print ("<tr>")
        print ("<td>")
        print ("Key: ")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Start:")
        print ("</td>")
        print ("<td>")
        if MyDB.llen(RedisKey) >= 10000 :
                start=MyDB.llen(RedisKey)-10000
        else:
                start=0
        # def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
        print (mhl.MyNumberForm("VStart",str(start),"","","0",str(MyDB.llen(RedisKey)-1),"1","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Stop:")
        print ("</td>")
        print ("<td>")
        # def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
        print (mhl.MyNumberForm("VStop",str(MyDB.llen(RedisKey)),"","","",str(MyDB.llen(RedisKey)),"1","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyButtonForm("submit","Crea .csv (sets)"))
        print ("</td>")
        print ("</tr>")
        # End form
        print (mhl.MyEndForm())
    
    print ("<tr>")
    print ("<td colspan=\"2\">")
    print ("<hr/>") # La linea orizzontale
    print ("</td>")
    print ("</tr>")
    
    # Search Date
    # Controllo che tipo di chiave si tratta e la do` in pasto al csv con singolo valore, oppure a quello con piu` valori (sets)
    # il [:4] prende le prime 4 lettere (che vengono confrontate con sets)
    print ("<tr>")
    print ("<td colspan=\"2\">")
    print ("<h3>Crea .CSV per selezione data</h3>")  # ho tolto il ritorno a capo <br/>
    print ("La selezione e` \"da\" \"a\", dove la seconda e` esclusa, per esempio selezionando dal giorno 3 al giorno 4, verranno selezionati solo i valori del giorno 3, quelli del 4 sono esclusi.</br>")
    print ("Non c'e` controllo sull'immissione, se errata potrebbe non produrre risultati.</br>")
    print ("Si possono inserire date nel formato YYYY/MM/GG (anno/mese/giorno), ma e` possibile inserire anche solo YYYY/MM (anno/mese), o addiritttura l'anno YYYY.</br>")
    print ("(L'estrazione dati e` fatta se maggiore di ... e minore di ...)</br>")
    print ("<b>Attenzione:</b> se la quantita` dei valori e` eccessiva, compare un'errore del web server, che non funzionera` fino al termine della creazione del file, il tempo di attesa puo` essere notevole, anche piu` di un'ora, dipende dalla mole dei dati.</br>")
    print ("Per dare un'idea, su un totale di 500000 valori il tempo impiegato e` stato di circa 2 ore.</br>")
    print ("</td>")
    print ("</tr>")
    if RedisKey[:4] != "sets":
        # Crea CSV
        print (mhl.MyActionForm("/cgi-bin/write_vals2csv_w_search_date.py","POST"))
        
        print ("<tr>")
        print ("<td>")
        print ("Key: ")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Start (da):")
        print ("</td>")
        print ("<td>")
        # def MyTextForm(Name,Value,Size,Required,Readonly):
        print (mhl.MyTextForm("VStart","2018/01/01","10","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Stop (a):")
        print ("</td>")
        print ("<td>")
        # def MyTextForm(Name,Value,Size,Required,Readonly):
        print (mhl.MyTextForm("VStop","2018/12/31","10","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyButtonForm("submit","Crea .csv (single)"))
        print ("</td>")
        print ("</tr>")
        # End form
        print (mhl.MyEndForm())
        
    else:
        # Crea CSV
        print (mhl.MyActionForm("/cgi-bin/write_setsVals2csv_w_search_date.py","POST"))
        
        print ("<tr>")
        print ("<td>")
        print ("Key: ")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Start:")
        print ("</td>")
        print ("<td>")
        # def MyTextForm(Name,Value,Size,Required,Readonly):
        print (mhl.MyTextForm("VStart","2018/01/01","10","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("Stop:")
        print ("</td>")
        print ("<td>")
        # def MyTextForm(Name,Value,Size,Required,Readonly):
        print (mhl.MyTextForm("VStop","2018/12/31","10","required",""))
        print ("</td>")
        print ("</tr>")
        
        print ("<tr>")
        print ("<td>")
        print ("")  # Testo nella 1a colonna
        print ("</td>")
        print ("<td>")
        print (mhl.MyButtonForm("submit","Crea .csv (sets)"))
        print ("</td>")
        print ("</tr>")
        # End form
        print (mhl.MyEndForm())
    
    print ("<tr>")
    print ("<td colspan=\"2\">")
    print ("<hr/>") # La linea orizzontale
    print ("</td>")
    print ("</tr>")
    
    # Reset
    print (mhl.MyActionForm("/cgi-bin/trimlistredis.py","POST"))
    print ("<tr>")
    print ("<td colspan=\"2\">")
    print ("<b>Ripulisce la lista dai valori indesiderati/obsoleti</b></br>")
    print ("""
L'eliminazione funziona contrariamente al solito, se viene indicato da -100 a -1 [default] vengono eliminati tutti i valori tranne gli ultimi 100.</br>
Il valore End=-1 sta` a significare l'ultimo elemento, il valore Start=-100 sta` a significare che intendiamo iniziare dal centesimo valore piu` vecchio.
""")
    print ("</td>")
    print ("</tr>")
    
    print ("<tr>")
    print ("<td>")
    print ("Key: ")
    print ("</td>")
    print ("<td>")
    print (mhl.MyTextForm(FormName,RedisKey,"40","required","readonly"))
    print ("</td>")
    print ("</tr>")
    
    print ("<tr>")
    print ("<td>")
    print ("Start:")
    print ("</td>")
    print ("<td>")
    # def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
    print (mhl.MyNumberForm("VStart","-100","6","6","","","1","required",""))
    print ("</td>")
    print ("</tr>")
    
    print ("<tr>")
    print ("<td>")
    print ("Stop:")
    print ("</td>")
    print ("<td>")
    # def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
    print (mhl.MyNumberForm("VStop","-1","6","6","","","1","required",""))
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
    print (mhl.MyButtonForm("submit","Ripulisci lista"))
    print ("</td>")
    print ("</tr>")
    
    print ("</table>")
    
    
    # End form
    print (mhl.MyEndForm())
else:
    print ("Manca la chiave: <b>",html.escape(form[FormName].value),"</b><br/>oppure hai selezionato una chiave non modificabile.")


# End web page
print (mhl.MyHtmlBottom())
