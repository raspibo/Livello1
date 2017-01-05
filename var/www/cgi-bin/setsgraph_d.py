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
	ri-elabora e reinserisce in Redis

	Questo programma, una volta eseguito, si deve interrompere solo se si
	effettuano modifiche alla chiave (gruppo) e al suo timer, altrimenti
	dovra` sempre "girare".
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
#	print ("\n\tUso: %s <RedisKey>" % sys.argv[0])
	print ("\n\tUso: {0:s} <RedisKey>".format(sys.argv[0]))
	print ("""
Questo programma prende una chiave Redis di gruppo (sets),
la elabora, reinserendo i valori in una nuova lista
e crea il rispettivo file .csv
""")


if len(sys.argv) == 2 and MyDB.exists(sys.argv[1]):
	# Setto le variabili per comodita` e chiarezza di programma
	Key=sys.argv[1]
	KeyVal=Key+":Valori"
	KeySort=flt.DecodeList(MyDB.sort(Key,alpha=1))	# Devo mantenerla sempre ordinata, altrimenti i dati non coincidono, e` una stringa, quindi "alpha=1"
	Timer=int(flt.Decode(MyDB.hget(Key+":Config","Timer")))
	TimerInizioCiclo=int(time.time())-Timer				# Tempo attuale meno Timer, cosi` il ciclo inizia subito
	# Ho usato il secondo e terzo valore (sets:NOME:ID), perche potrebbero esserci dei duplicati fra allarmi e grafici e .. altro (se ci sara`)
	FileName=DirBase+"/"+Key.split(":")[1]+Key.split(":")[2]+".csv"
	if os.path.isfile(FileName):
		print ("Delete")
		os.remove(FileName)								# Elimino il file se esiste
	
	while True:
		
		if int(time.time()) - TimerInizioCiclo > Timer:
			# Questo blocco scrive l'intestazione nel file .csv (se non esiste il file)
			# Ho fatto questo perche` se viene eliminato il file, magari dopo che lo si e`
			# salvato, se il programma stava girando, si blocca.
			if not os.path.isfile(FileName):
				IntestazioneCSV="Data"
				for i in range (len(KeySort)):
					Descrizione="none"	# Metto qualcosa nel caso mancasse la descrizione
					if MyDB.hexists(KeySort[i],"Descrizione"):
						Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
					IntestazioneCSV=IntestazioneCSV+","+Descrizione
				flt.WriteFileData(FileName,IntestazioneCSV+"\n")								# New
			ValoriCSV=""
			for i in range (len(KeySort)):
				# Devo prendere l'ultimo ":Valori" dalla chiave (nella chiave, e` un gruppo "sets")
				# ma solo dopo la virgola 		.split(",")[1]
				# perche` prima c'e` la data		.split(",")[0]
				ValoriCSV=ValoriCSV+","+flt.Decode(MyDB.lindex(KeySort[i]+":Valori",-1)).split(",")[1]
			DataCSV=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())	# La data
			MyDB.rpush(KeyVal,DataCSV+ValoriCSV)							# Inserisco i dati in una chiave :Valori dello stesso nome del gruppo
			flt.AddFileData(FileName,DataCSV+ValoriCSV+"\n")				# E li aggiungo anche nel file
			TimerInizioCiclo=int(time.time())								# Tempo attuale
