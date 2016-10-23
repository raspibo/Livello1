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

""" Prende i dati dalla chiave Redis (sets:*:Valori) passata come argomento all'avvio,
	elabora e ricrea il file .csv

"""

import os,time,json,redis,sys
import mjl, mhl, flt	# Non servono tutte, ormai le metto d'abitudine ;)

DirBase="/var/www"					# Meglio specificare il percorso assoluto
ConfigFile=DirBase+"/conf/config.json"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Controllo se piu` di un argomento o se richiesto l'help
if len(sys.argv) != 2 or sys.argv[1] == "-h":
	print ("\n\tUso: %s <RedisKey>" % sys.argv[0])
	print ("""
Questo programma prende una chiave Redis di gruppo (sets:*), elabora,
e crea il rispettivo file .csv
""")
	exit()

if len(sys.argv) == 2 and MyDB.exists(sys.argv[1]):
	# Setto le variabili per comodita` e chiarezza di programma
	KeyVal=sys.argv[1]
	Key=KeyVal[:-7]		# Toglie ":Valori"
	KeySort=flt.DecodeList(MyDB.sort(Key,alpha=1))	# Devo mantenerla sempre ordinata, altrimenti i dati non coincidono, e` una stringa, quindi "alpha=1"
	# Ho usato il secondo e terzo valore (sets:NOME:ID), perche potrebbero esserci dei duplicati fra allarmi e grafici e .. altro (se ci sara`)
	FileName=DirBase+"/"+Key.split(":")[1]+Key.split(":")[2]+".csv"
	if os.path.isfile(FileName):
		print ("Delete")
		os.remove(FileName)								# Elimino il file se esiste
	
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
	
	for i in range (MyDB.llen(KeyVal)):
		ValoriCSV=flt.Decode(MyDB.lindex(KeyVal,i))
		flt.AddFileData(FileName,ValoriCSV+"\n")
elif not MyDB.exists(sys.argv[1]):
	print ("Chiave inesistente", sys.argv[1])

""" Debug
print (Key)
print (KeyVal)
print (KeySort)
print (FileName)
print (IntestazioneCSV)
#print (ValoriCSV)
print (FileName)
"""