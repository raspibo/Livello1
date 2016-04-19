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
"""

import os,time,json,redis
import paho.mqtt.client as mqtt
import mjl, mhl, flt	# Non servono tutte, ormai le metto d'abitudine ;)

DirBase="/var/www"
ConfigFile=DirBase+"/conf/config.json"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("I/+/+/+/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	#print(msg.topic+" "+str(msg.payload))	# MyDebug
	# Preparazione delle variabili per generazione chiave Redis
	var = msg.topic
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
	try:
		var = json.loads(flt.Decode(msg.payload))
		#print (var["ID"])
		MyDB = flt.OpenDBFile(ConfigFile)	# Apro il database Redis
		# Scrivo il record ("chiave redis") ed il valore
		IDHASH=TipoIO+":"+PosizioneC+":"+PosizioneP+":"+PosizioneS+":"+Tipo+":"+var["ID"]	# Uso una variabile di appoggio per l'identificatore della chiave "primaria"
		MyDB.hset(IDHASH, "Valori", IDHASH+":Valori" )										# La seconda chiave e` uguale alla prima con ":Valori" alla fine
		# Data in formato CSV (dgraph.js)
		DataCSV=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
		# Lista dei valori, contiene "Data,Valore" e si chiama (quasi) come sopra
		MyDB.rpush(IDHASH+":Valori",DataCSV+","+var["Valore"])
	except:
		print ("Error:",msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
