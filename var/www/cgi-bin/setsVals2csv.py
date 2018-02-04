#!/usr/bin/env python3

"""
The MIT License (MIT)

Copyright (c) 2018 davide

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

""" setsVals2csv.py
    Prende i dati dalla chiave Redis (sets:*:Valori) passata come argomento all'avvio,
    elabora e ricrea il file .csv
"""

import os,time,json,redis,sys
import mjl, mhl, flt    # Non servono tutte, ormai le metto d'abitudine ;)

DirBase="/var/www"                                      # Meglio specificare il percorso assoluto
ConfigFile=DirBase+"/conf/config.json"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Controllo se piu` di un argomento o se richiesto l'help
if len(sys.argv) != 4 or sys.argv[1] == "-h":
    print ("\n\tUso: %s <RedisKey> <Start> <Stop>" % sys.argv[0])
    print ("""
Questo programma prende una chiave Redis di gruppo (sets:*), elabora,
e crea il rispettivo file .csv
""")
    exit()

if len(sys.argv) == 4 and MyDB.exists(sys.argv[1]):
    # Setto le variabili per comodita` e chiarezza di programma
    KeyVal=sys.argv[1]
    Key=KeyVal[:-7]         # Toglie ":Valori"
    KeySort=flt.DecodeList(MyDB.sort(Key,alpha=1))  # Devo mantenerla sempre ordinata, altrimenti i dati non coincidono, e` una stringa, quindi "alpha=1"
    print ("Input sets: \t\t", KeyVal)
    print ("Key: \t\t\t", Key)
    print ("Key contents: \t\t", KeySort)
    # Ho usato il secondo e terzo valore (sets:NOME:ID), perche potrebbero esserci dei duplicati fra allarmi e grafici e .. altro (se ci sara`)
    #FileName=DirBase+"/"+Key.split(":")[1]+Key.split(":")[2]+".csv"
    FileName=DirBase+"/"+Key.split(":")[1]+Key.split(":")[2]+".csv"
    if os.path.isfile(FileName):
        print ("Deleting: \t\t\"%s\"" % FileName)
        os.remove(FileName)                                                             # Elimino il file se esiste
    # Creazione dell'intestazione: DATA, Descrizione1, Descrizione2, .., DescrizioneN
    IntestazioneCSV="Data"
    for i in range (len(KeySort)):
        Descrizione="none"      # Metto qualcosa nel caso mancasse la descrizione
        if MyDB.hexists(KeySort[i],"Descrizione"):
            Descrizione=flt.Decode(MyDB.hget(KeySort[i],"Descrizione"))
        IntestazioneCSV=IntestazioneCSV+","+Descrizione
    FileTemp = open(FileName,"w")
    FileTemp.write(IntestazioneCSV+"\n")  # Scrittura intestazione
    # Per tutta la lunghezza della lista "Valori", li leggo e li scrivo nel file
    #for i in range(MyDB.llen(KeyVal)):
    for i in range(int(sys.argv[2]), int(sys.argv[3])):
        #print (flt.Decode(MyDB.lindex(KeyVal,i)))
        ValoriCSV=flt.Decode(MyDB.lindex(KeyVal,i))
        FileTemp.write(ValoriCSV+"\n")
    FileTemp.close()
    print ("[re]Generated file: \t\"{}\"".format(FileName))
elif not MyDB.exists(sys.argv[1]):
    print ("Chiave inesistente", sys.argv[1])
