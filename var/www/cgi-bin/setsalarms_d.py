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
	effettuano modifiche alla chiave (gruppo) e/o alla suo aconfigurazione,
	altrimenti dovra` sempre "girare".
"""

import os,time,json,redis,sys
import paho.mqtt.client as mqtt
import mjl, mhl, flt	# Non servono tutte, ormai le metto d'abitudine ;)

DirBase="/var/www"					# Meglio specificare il percorso assoluto
ConfigFile=DirBase+"/conf/config.json"


# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Controllo se piu` di un argomento o se richiesto l'help
if len(sys.argv) != 2 or sys.argv[1] == "-h":
	print ("\n\tUso: %s <RedisKey>" % sys.argv[0])
	print ("""
Questo programma prende una chiave Redis di gruppo (sets), la elabora,
e ?
""")


if len(sys.argv) == 2 and MyDB.exists(sys.argv[1]):
	# Setto le variabili per comodita` e chiarezza di programma
	Key=sys.argv[1]			# La chiave e` nel formato sets:alarms:ID
	KeySort=flt.DecodeList(MyDB.sort(Key,alpha=1))	# Devo mantenerla sempre ordinata, altrimenti i dati non coincidono, e` una stringa, quindi "alpha=1"
	KeyFunction=flt.Decode(MyDB.hget(Key+":Config","Funzionamento"))
	Timer=int(flt.Decode(MyDB.hget(Key+":Config","Timer")))*60			# Mi serve in secondi e lo manterrei per memoria allarme
	#TimerInizio=int(time.time())				# Tempo attuale meno Timer, cosi` il ciclo inizia subito
	time.sleep(3)	# Ritardo attivazione, forse sarebbe meglio parametrizzare anche questo ?
	
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
	KeySumDalle=int(KeyHd)*60+int(KeyMd)
	KeySumAlle=int(KeyHa)*60+int(KeyMa)
	
	while True:
		NowInMinute=int(time.strftime("%H",time.localtime()))*60+int(time.strftime("%M",time.localtime()))
		#print ("Dalle:", KeySumDalle, "Now:", NowInMinute, "Alle:", KeySumAlle)	# myDebug
		time.sleep(3)	# MyDebug
		if KeyFunction == "On" or ( KeyFunction == "Auto" and ( KeySumDalle <= NowInMinute <= KeySumAlle ) ) :
			for i in range (len(KeySort)):
				# Devo prendere l'ultimo ":Valori" dalla chiave (nella chiave, e` un gruppo "sets")
				# ma solo dopo la virgola 		.split(",")[1]
				# perche` prima c'e` la data		.split(",")[0]
				Valore=flt.Decode(MyDB.lindex(KeySort[i]+":Valori",-1)).split(",")[1]
				
				# CI STO` PENSANDO .. mettere qui i default, ma se li metto qui,
				# vengono ricalcolati ogni volta, se faccio una funzione,
				# non riesco a generalizzarla perche` i testi sono differenti.
				# Boh !?!? #####################################################
				"""
				# Preparo i "default" nel caso non siano stati configurati
				Descrizione="Manca descrizione"
				if MyDB.hexists(KeySort[i],"Descrizione"):
					Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
				UM=""
				if MyDB.hexists(KeySort[i],"UM"):
					UM=flt.Decode(MyDB.hget(KeySort[i],"UM"))
				"""
				
				# Se esiste RangeValori, e il valore non rientra nel range, e non esiste allarme attivo da tempoX .. parte un nuovo allarme.
				if MyDB.hexists(KeySort[i],"RangeValori"):
					# Ho dovuto leggere il range e metterlo in una stringa ..
					STRING = (flt.Decode(MyDB.hget(KeySort[i],"RangeValori")))
					# splitto alla virgola e uso il primo (0) ed il secondo (1) come numeri interi separatamente
					#if int(Valore) not in range (int(STRING.split(",")[0]),int(STRING.split(",")[1]+"1")):	# NON FUNZIONA
					if float(Valore) < float(STRING.split(",")[0]) or float(Valore) > float(STRING.split(",")[1]):
						if not MyDB.hexists(KeySort[i]+":Allarmi","RangeValori"):
							print (STRING.split(",")[0],Valore,STRING.split(",")[1])
							print(type(STRING.split(",")[0]))
							print(type(Valore))
							# Preparo i "default" nel caso non siano stati configurati
							Descrizione="Manca descrizione"
							if MyDB.hexists(KeySort[i],"Descrizione"):
								Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
							UM=""
							if MyDB.hexists(KeySort[i],"UM"):
								UM=flt.Decode(MyDB.hget(KeySort[i],"UM"))
							# InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
							flt.InviaAvviso(MyDB,"msg:level1:RangeValori:"+flt.AlertsID()[0],"alert","Errore range valori "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"RangeValori")),UM,flt.AlertsID()[1])
							MyDB.hset(KeySort[i]+":Allarmi","RangeValori","Alarm")
							MyDB.expire(KeySort[i]+":Allarmi",Timer)
				if MyDB.hexists(KeySort[i],"ValoreMin"):
					if float(Valore) < float(flt.Decode(MyDB.hget(KeySort[i],"ValoreMin"))):
						if not MyDB.hexists(KeySort[i]+":Allarmi","ValoreMin"):
							# Preparo i "default" nel caso non siano stati configurati
							Descrizione="Manca descrizione"
							if MyDB.hexists(KeySort[i],"Descrizione"):
								Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
							UM=""
							if MyDB.hexists(KeySort[i],"UM"):
								UM=flt.Decode(MyDB.hget(KeySort[i],"UM"))
							# InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
							flt.InviaAvviso(MyDB,"msg:level1:ValoreMin:"+flt.AlertsID()[0],"alert","Errore valore minimo "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"ValoreMin")),UM,flt.AlertsID()[1])
							MyDB.hset(KeySort[i]+":Allarmi","ValoreMin","Alarm")
							MyDB.expire(KeySort[i]+":Allarmi",Timer)
				if MyDB.hexists(KeySort[i],"ValoreMax"):
					if float(Valore) > float(flt.Decode(MyDB.hget(KeySort[i],"ValoreMax"))):
						if not MyDB.hexists(KeySort[i]+":Allarmi","ValoreMax"):
							# Preparo i "default" nel caso non siano stati configurati
							Descrizione="Manca descrizione"
							if MyDB.hexists(KeySort[i],"Descrizione"):
								Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
							UM=""
							if MyDB.hexists(KeySort[i],"UM"):
								UM=flt.Decode(MyDB.hget(KeySort[i],"UM"))
							# InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
							flt.InviaAvviso(MyDB,"msg:level1:ValoreMax:"+flt.AlertsID()[0],"alert","Errore valore massimo "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"ValoreMax")),UM,flt.AlertsID()[1])
							MyDB.hset(KeySort[i]+":Allarmi","ValoreMax","Alarm")
							MyDB.expire(KeySort[i]+":Allarmi",Timer)
				if MyDB.hexists(KeySort[i],"ValoreOn"):
					if Valore == flt.Decode(MyDB.hget(KeySort[i],"ValoreOn")):
						if not MyDB.hexists(KeySort[i]+":Allarmi","ValoreOn"):
							# Preparo i "default" nel caso non siano stati configurati
							Descrizione="Manca descrizione"
							if MyDB.hexists(KeySort[i],"Descrizione"):
								Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
							UM=""
							if MyDB.hexists(KeySort[i],"UM"):
								UM=flt.Decode(MyDB.hget(KeySort[i],"UM"))
							# InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
							flt.InviaAvviso(MyDB,"msg:level1:ValoreOn:"+flt.AlertsID()[0],"alert","Allarme "+Descrizione,Valore+"/"+flt.Decode(MyDB.hget(KeySort[i],"ValoreOn")),UM,flt.AlertsID()[1])
							MyDB.hset(KeySort[i]+":Allarmi","ValoreOn","Alarm")
							MyDB.expire(KeySort[i]+":Allarmi",Timer)
				else:
					# Qua potrei avere dei problemi con le sonde di temperatura che misurano "1"
					# A meno che: alle sonde di temperatura non venga messo un "ValoreOn" a "-40" per esempio.
					if Valore == "1":
						if not MyDB.hexists(KeySort[i]+":Allarmi","Valore"):
							# Preparo i "default" nel caso non siano stati configurati
							Descrizione="Manca descrizione"
							if MyDB.hexists(KeySort[i],"Descrizione"):
								Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
							UM=""
							if MyDB.hexists(KeySort[i],"UM"):
								UM=flt.Decode(MyDB.hget(KeySort[i],"UM"))
							# InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
							flt.InviaAvviso(MyDB,"msg:level1:Valore:"+flt.AlertsID()[0],"alert","Allarme "+Descrizione,Valore,UM,flt.AlertsID()[1])
							MyDB.hset(KeySort[i]+":Allarmi","Valore","Alarm")
							MyDB.expire(KeySort[i]+":Allarmi",Timer)
