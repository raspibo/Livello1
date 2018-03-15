#!/usr/bin/env python3

"""
The MIT License (MIT)

Copyright (c) 2016 davide

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

""" Prende i dati dalla chiave Redis passata come argomento all'avvio,
    ri-elabora e ?

    Questo programma, una volta eseguito, si deve interrompere solo se si
    effettuano modifiche alla chiave (gruppo) e/o alla sua configurazione,
    altrimenti dovra` sempre "girare".
"""

import os,time,json,redis,sys,datetime
import paho.mqtt.client as mqtt
import mjl, mhl, flt    # Non servono tutte, ormai le metto d'abitudine ;)

DirBase="/var/www"                    # Meglio specificare il percorso assoluto
ConfigFile=DirBase+"/conf/config.json"


# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Controllo se piu` di un argomento o se richiesto l'help
if len(sys.argv) != 2 or sys.argv[1] == "-h":
#    print ("\n\tUso: %s <RedisKey>" % sys.argv[0])
    print ("\n\tUso: {0:s} <RedisKey>".format(sys.argv[0]))
    print ("""
Questo programma prende una chiave Redis di gruppo (sets),
normalmente "sets:alarm:<nome>", la elabora, invia gli
allarmi e/o avvisi all'utente tramite il centralino
(centred).
Altro ?
""")


if len(sys.argv) == 2 and MyDB.exists(sys.argv[1]):
    # Setto le variabili per comodita` e chiarezza di programma
    Key=sys.argv[1]            # La chiave e` nel formato sets:alarms:ID
    KeySort=flt.DecodeList(MyDB.sort(Key,alpha=1))    # Devo mantenerla sempre ordinata, altrimenti i dati non coincidono, e` una stringa, quindi "alpha=1"
    # Contorllo e set del funzionamento, se la chaive non siste, rimane OFF
    KeyFunction="Off"
    if MyDB.hexists(Key+":Config","Funzionamento"):
        KeyFunction=flt.Decode(MyDB.hget(Key+":Config","Funzionamento"))
    """ Timers
        Timer, preso dalla configurazione, al momento e` finito inutilizzato
        ExpireTimer, l'ho aggiunto perche` se l'allarme non cessa, viene rispedito ad ogni eliminazione della chiave
        sleep -- questo e` da vedere, forse servira` un ritardo temporizzato nel caso di attivazioni manuali
                 al momento non necessita perche` non ci sono manuali.
    """
    Timer=int(flt.Decode(MyDB.hget(Key+":Config","Timer")))        # Mi serve in secondi e lo manterrei per memoria allarme avevo messo *60, ma e` gia` in secondi
    #######################################################        # Non e` utilizzato.
    ExpireTimer=14400    # Fisso a N ora/e (e` in secondi), meglio averlo nelle impostazioni ?
    time.sleep(3)    # Ritardo attivazione, forse sarebbe meglio parametrizzare anche questo ?
    
    # Metto a 0 se non sono indicati "dalle" "alle" in configurazione
    if MyDB.hexists(Key+":Config","dalleH"):
        KeyHd=flt.Decode(MyDB.hget(Key+":Config","dalleH"))
    else:
        KeyHd=0
    if MyDB.hexists(Key+":Config","dalleM"):
        KeyMd=flt.Decode(MyDB.hget(Key+":Config","dalleM"))
    else:
        KeyMd=0
    if MyDB.hexists(Key+":Config","alleH"):
        KeyHa=flt.Decode(MyDB.hget(Key+":Config","alleH"))
    else:
        KeyHa=0
    if MyDB.hexists(Key+":Config","alleM"):
        KeyMa=flt.Decode(MyDB.hget(Key+":Config","alleM"))
    else:
        KeyMa=0
    # Calcolo/trasformo in minuti totali
    KeySumDalle=int(KeyHd)*60+int(KeyMd)
    KeySumAlle=int(KeyHa)*60+int(KeyMa)
    
    # Finche` esistono le "chiavi" (sensore e valori)
    while MyDB.exists(Key) and MyDB.exists(Key+":Config"):
        NowInMinute=int(time.strftime("%H",time.localtime()))*60+int(time.strftime("%M",time.localtime()))
        #print ("Dalle:", KeySumDalle, "Now:", NowInMinute, "Alle:", KeySumAlle)    # myDebug
        #time.sleep(3)    # MyDebug
        
        for i in range (len(KeySort)):
            # Devo prendere l'ultimo ":Valori" dalla chiave (nella chiave, e` un gruppo "sets")
            # ma solo dopo la virgola         .split(",")[1]
            # perche` prima c'e` la data        .split(",")[0]
            Valore=flt.Decode(MyDB.lindex(KeySort[i]+":Valori",-1)).split(",")[1]
            
            # Preparo i "default" nel caso non siano stati configurati
            Descrizione="Manca descrizione"
            if MyDB.hexists(KeySort[i],"Descrizione"):
                Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
            UM=""
            if MyDB.hexists(KeySort[i],"UM"):
                UM=flt.Decode(MyDB.hget(KeySort[i],"UM"))
            
            """ RANGEVALORI
                Dev'essere nel formato [+/-]numero,[+/-]numero
                Questa e` fuori dal controllo di allarmi, perche` e` un'errore del sensore/sonda
                e se c'e` un problema e` meglio saperlo.
            """
            # Se esiste RangeValori, e il valore non rientra nel range, e non esiste allarme attivo da tempoX .. parte un nuovo allarme.
            if MyDB.hexists(KeySort[i],"RangeValori"):
                # Ho dovuto leggere il range e metterlo in una stringa ..
                STRING = flt.Decode(MyDB.hget(KeySort[i],"RangeValori"))
                # splitto alla virgola e uso il primo (0) ed il secondo (1) come numeri interi separatamente
                #if int(Valore) not in range (int(STRING.split(",")[0]),int(STRING.split(",")[1]+"1")):    # NON FUNZIONA
                if float(Valore) < float(STRING.split(",")[0]) or float(Valore) > float(STRING.split(",")[1]):
                    if not MyDB.hexists(KeySort[i]+":Allarmi","RangeValori"):
                        print (STRING.split(",")[0],Valore,STRING.split(",")[1])
                        print (type(STRING.split(",")[0]))
                        print (type(Valore))
                        # InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
                        flt.InviaAvviso(MyDB,"msg:level1:RangeValori:"+flt.AlertsID()[0],"alert","Errore range valori "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"RangeValori")),UM,flt.AlertsID()[1])
                        MyDB.hset(KeySort[i]+":Allarmi","RangeValori","Alarm")
                        MyDB.expire(KeySort[i]+":Allarmi",ExpireTimer)
            
            """ CONTROLLO LETTURA SENSORE
                Verifica che arrivi una nuove lettura del sensore, nel caso, potrebbe essere
                bloccato per qualche motivo, mancanza alimentazione, blocco della scheda,
                guasto alla rete, o altro ...
            """
            # Se e` attivo
            if MyDB.hexists(KeySort[i],"TempoErrore"):
                time.sleep(10)
                if not MyDB.hexists(KeySort[i]+":Allarmi","TempoErrore"):    # se non c'e` gia` allarme
                    # mi serve la data
                    DataValore=flt.Decode(MyDB.lindex(KeySort[i]+":Valori",-1)).split(",")[0]
                    #print(DataValore)
                    # Converto in tipo 'datetime' per il calcolo (sottrazione)
                    ValoreData=datetime.datetime(time.strptime(DataValore, "%Y/%m/%d %H:%M:%S").tm_year,time.strptime(DataValore, "%Y/%m/%d %H:%M:%S").tm_mon,time.strptime(DataValore, "%Y/%m/%d %H:%M:%S").tm_mday,time.strptime(DataValore, "%Y/%m/%d %H:%M:%S").tm_hour,time.strptime(DataValore, "%Y/%m/%d %H:%M:%S").tm_min,time.strptime(DataValore, "%Y/%m/%d %H:%M:%S").tm_sec)
                    #print (ValoreData)
                    # Se da piu` di "TempoErrore" non viene aggiornato il valore, c'e` un problema e mando un messaggio
                    # Se adesso - 'ora del valore' e` maggiore di "TempoErrore":
                    TempoErroreSec= int(flt.Decode(MyDB.hget(KeySort[i],"TempoErrore")))
                    if (datetime.datetime.now() - ValoreData) > datetime.timedelta(seconds=TempoErroreSec):
                        #print (ValoreData)
                        #print (datetime.datetime.now())
                        #print (MyDB,"msg:level1:TempoErrore:"+flt.AlertsID()[0],"alert",Descrizione+", in ritardo lettura/aggiornamento valore (vedi data)",Valore,UM,DataValore)
                        # InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
                        flt.InviaAvviso(MyDB,"msg:level1:TempoErrore:"+flt.AlertsID()[0],"alert",Descrizione+", in ritardo lettura/aggiornamento valore, probabile guasto elettrico",Valore,UM,DataValore)
                        MyDB.hset(KeySort[i]+":Allarmi","TempoErrore","Ritardo")
                        MyDB.expire(KeySort[i]+":Allarmi",TempoErroreSec)    # Si auto-elimina con lo stesso tempo di controllo errore
            
            # Inizio automatici
            """ La linea e` lunga, vado a capo """
            if KeyFunction == "On" or ( KeyFunction == "Auto" and \
                    (( KeySumDalle < KeySumAlle ) and ( KeySumDalle <= NowInMinute <= KeySumAlle )) or \
                    (( KeySumDalle > KeySumAlle ) and (( KeySumDalle <= NowInMinute ) or (NowInMinute <= KeySumAlle ))) ) :
                """ Gestione degli avvisi/allarmi
                    Decido se deve essere inviato come allarme o come avviso
                    Vale per le variabili Valore On,Min,Max
                
                    Lo .split(",") finale, genera una lista
                """
                TypeValoreOn="alert"
                TypeValoreMin="alert"
                TypeValoreMax="alert"
                if MyDB.hexists(KeySort[i],"Allarme"):
                    Allarmi=flt.Decode(MyDB.hget(KeySort[i],"Allarme")).split(",")
                    for j in range (len(Allarmi)):
                        if Allarmi[j] == "ValoreOn":
                            TypeValoreOn="alarm"
                        if Allarmi[j] == "ValoreMin":
                            TypeValoreMin="alarm"
                        if Allarmi[j] == "ValoreMax":
                            TypeValoreMax="alarm"
                
                if MyDB.hexists(KeySort[i],"ValoreMin"):
                    if float(Valore) < float(flt.Decode(MyDB.hget(KeySort[i],"ValoreMin"))):
                        if not MyDB.hexists(KeySort[i]+":Allarmi","ValoreMin"):
                            # InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
                            flt.InviaAvviso(MyDB,"msg:level1:ValoreMin:"+flt.AlertsID()[0],TypeValoreMin,"Errore valore minimo "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"ValoreMin")),UM,flt.AlertsID()[1])
                            MyDB.hset(KeySort[i]+":Allarmi","ValoreMin","Alarm")
                            MyDB.expire(KeySort[i]+":Allarmi",ExpireTimer)
                if MyDB.hexists(KeySort[i],"ValoreMax"):
                    if float(Valore) > float(flt.Decode(MyDB.hget(KeySort[i],"ValoreMax"))):
                        if not MyDB.hexists(KeySort[i]+":Allarmi","ValoreMax"):
                            # InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
                            flt.InviaAvviso(MyDB,"msg:level1:ValoreMax:"+flt.AlertsID()[0],TypeValoreMax,"Errore valore massimo "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"ValoreMax")),UM,flt.AlertsID()[1])
                            MyDB.hset(KeySort[i]+":Allarmi","ValoreMax","Alarm")
                            MyDB.expire(KeySort[i]+":Allarmi",ExpireTimer)
                if MyDB.hexists(KeySort[i],"ValoreOn"):
                    if Valore == flt.Decode(MyDB.hget(KeySort[i],"ValoreOn")):
                        if not MyDB.hexists(KeySort[i]+":Allarmi","ValoreOn"):
                            # InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
                            flt.InviaAvviso(MyDB,"msg:level1:ValoreOn:"+flt.AlertsID()[0],TypeValoreOn,"Allarme "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"ValoreOn")),UM,flt.AlertsID()[1])
                            MyDB.hset(KeySort[i]+":Allarmi","ValoreOn","Alarm")
                            MyDB.expire(KeySort[i]+":Allarmi",ExpireTimer)
            #elif KeyFunction == "Off" and not MyDB.hexists(KeySort[i],"RangeValori"): # Non ha senso quando ci sono piu` sensori
            elif KeyFunction == "Off":
                print ("Funzionamento : Off")
                exit()
else:
    print ("""       Mancano dei parametri, oppure la chiave specificata non esiste         """)
