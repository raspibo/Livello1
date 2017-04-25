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

""" Prende i dati ricevuti da MQTT broker, li elabora ed inserisce in Redis
    Questo programma dovra` sempre "girare".

    Thu 22 Dec 2016 01:53:32 PM CET
    Introdotto blocchi di codice per generazione file di log per ricerca
    problema di blocco
"""

import os,time,json,redis
import paho.mqtt.client as mqtt
import mjl, mhl, flt	# Non servono tutte, ormai le metto d'abitudine ;)

DirBase="/var/www/"
ConfigFile=DirBase+"conf/config.json"

# File di log
#FileName=DirBase+"file_di.log"
FileName="/tmp/file_di.log"
# Lo cancello se esiste (ogni volta che avvio il programma)
if os.path.isfile(FileName):
    #print (".. deleting logfile ..")
    os.remove(FileName)								# Elimino il file se esiste

# Scrive un file
def WriteFileData(Filename,Dato):
    if not os.path.exists(Filename):
        FileTemp = open(Filename,"w")
        FileTemp.write(Dato)
        FileTemp.close()
    else:
        # Funzionano entrambe
        print ("Errore, il file \"{}\" esiste gia`!".format(Filename))
        #print ("Errore, il file \"%s\" esiste gia`!" % Filename)
        exit()

# Aggiunge dati ad un file, aprendolo e richiudendolo
def AddFileData(Filename,Dato):
    if os.path.exists(Filename):
        FileTemp = open(Filename,"a")
        FileTemp.write(Dato)
        FileTemp.close()
    else:
        print ("Errore, manca il file", Filename)
        exit()

# Genero file di log (ogni volta che avvio il programma)
if not os.path.isfile(FileName):
    WriteFileData(FileName,"File di log"+"\n")								# New log file


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    #print("Connected with result code "+str(rc))
    AddFileData(FileName,"Connected with result code "+str(rc)+"\n")    # Scrivo nel file di log
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("I/+/+/+/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Data in formato CSV (dgraph.js)
    # (Spostata qua perche` la uso anche per i messaggi nel file di log)
    DataCSV=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    # File di log
    #AddFileData(FileName,msg.topic+" "+str(msg.payload)+"\n")				# Aggiungo messaggi in elaborazione nel file log
    #print(msg.topic+" "+str(msg.payload))	# MyDebug
    # Preparazione delle variabili per generazione chiave Redis
    var = msg.topic
    #print ("*** Topic:",var)
    #AddFileData(FileName,"*** Topic:"+str(var)+"\n")    # Scrivo nel file di log
    Tipo = os.path.basename(var)
    var = os.path.split(var)[0]
    PosizioneS = os.path.basename(var)
    var = os.path.split(var)[0]
    PosizioneP = os.path.basename(var)
    var = os.path.split(var)[0]
    PosizioneC = os.path.basename(var)
    var = os.path.split(var)[0]
    TipoIO = os.path.basename(var)
    #print (TipoIO, PosizioneC, PosizioneP, PosizioneS, Tipo)	# MyDebug
    # Devo "parsare" il formato per trasformarlo in dizionario python ..
    # Ho dovuto usare una try/except perche` un esp8266 a volte sembra inviare
    # due stringhe assieme.
    # Modificata try/except perche` capitano errori sulle stringhe (sempre dove c'e` il modulo ESP8266)
    try:
        var = json.loads(flt.Decode(msg.payload))
    except:
        AddFileData(FileName,DataCSV+":\t"+msg.topic+" "+str(msg.payload)+"\n")				# Scrivo l'errore nel file di log
        var = ""
    print ("var =", var)
    #AddFileData(FileName,"var ="+str(var)+"\n")    # Scrivo nel file di log
    # Cambio il controllo causa "KeyError: var"
    if "ID" in var and "Valore" in var:
        #print(var)
        MyDB = flt.OpenDBFile(ConfigFile)	# Apro il database Redis
        # Scrivo il record ("chiave redis") ed il valore
        IDHASH=TipoIO+":"+PosizioneC+":"+PosizioneP+":"+PosizioneS+":"+Tipo+":"+var["ID"]	# Uso una variabile di appoggio per l'identificatore della chiave "primaria"
        MyDB.hset(IDHASH, "Valori", IDHASH+":Valori" )										# La seconda chiave e` uguale alla prima con ":Valori" alla fine
        #print("IDHASH:",IDHASH)
        #AddFileData(FileName,"IDHASH:"+str(IDHASH)+"\n")    # Scrivo nel file di log
        #print("Data:",DataCSV)
        #AddFileData(FileName,"Data:"+str(DataCSV)+"\n")    # Scrivo nel file di log
        # Lista dei valori, contiene "Data,Valore" e si chiama (quasi) come sopra
        # Inserisco il valore solo se esiste # Questo dovrebbe eliminare alcuni errori che capitano
        MyDB.rpush(IDHASH+":Valori",DataCSV+","+var["Valore"])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
