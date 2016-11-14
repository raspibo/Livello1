#!/usr/bin/env python3

# Questo file visualizza un grafico da file "csv"

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

""" Stavolta e` tutta un'altra cosa
    
    Modificato perche` accetti un file in input
    Esempio: viewpagegraph.py?file=graph.csv
	Ha il percorso sulla "root": ../filename
	Dovrebbe funzionare anche per gli archivi
"""

# Parametri generali // Non li uso tutti, li lascio per "abitudine"
TestoPagina="Visualizza grafico da file: "
ConfigFile="../conf/config.json"
ExecFile="none"
# Redis "key"
RedisKey = "none"
# Form name/s
FormName = "file"
FileName = ""

form=cgi.FieldStorage()

if FormName not in form:
	pass
else:
	FileName = cgi.escape(form[FormName].value)

TestoPagina = TestoPagina + FileName

print("""<!DOCTYPE html>
<html>

<head>
  <title>Livello 1</title>
  <meta name="GENERATOR" content="Midnight Commander (mcedit)">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Keywords" content="centralina, livello1, grafico, python">
  <meta name="Author" content="Davide">
  <!-- <meta http-equiv="refresh" content="300">
  L`ho chiamato da un GET, quindi il timer funziona, ma non serve per come ho pensato di fare/usare .. !!!
  -->
  <meta http-equiv="refresh" content="300">

<script type="text/javascript"
  src="../dygraph-combined.js"></script>
</head>


<body>
<title>Graphic</title>
""")

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("Non ho rinominato i campi e non sono stato a riordinare le voci.<br/>")

print("""
<p>
Questa "chart" e` interattiva.
Muovi il mouse per evidenziare i singoli valori.
Clicca e trascina per selezionare ed effettuare uno zoom sull'area selezionata.
Doppio click del mouse per ritornare alla visualizzazione globale.
Con il tasto "Shift" premuto, usa il click del mouse per trascinare l'area di visualizzazione.
</p>

<div id="graphdiv" style="position:absolute; left:20px; right:20px; top:200px; bottom:20px;"></div>
<script type="text/javascript">
  g = new Dygraph(

    // containing div
    document.getElementById("graphdiv"),

    // CSV or path to a CSV file.
""")

print("    \""+FileName+"\",")

print("""
    {
    showRoller: false,
    connectSeparatedPoints: true,
    //title: 'Grafico',
    ylabel: 'Value',
    xlabel: 'Time',
    //legend: 'always',
    labelDivStyles: {'textalign':'right'}
    }
  );
</script>

</body>
</html>""")