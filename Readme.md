Herzlich Willkommen zu meinem Rechner für die Analytische Geometrie.

Es gibt zwei Möglichkeiten den Rechner zu benutzen:
Entweder Rechner.exe ausführen oder Main.py.


Die Rechner.exe sollte direkt ohne Probleme ausführbar sein. 

Du kannst also schon alle Funktionen ausführen. Du wirst aber vielleicht merken, dass es einige � Boxen gibt. Das liegt an der standard Windows Schriftart. Diese unterstützt viele der verwendeten Schriftzeichen nicht. Dafür gibt es allerdings eine Lösung: Eine eigene Schriftart zu verwenden. Dies ist auch nicht allzu kompliziert.

-> Es gibt eine Schriftart "DejaVu Sans Mono Unifont.ttf" im Ordner "Fonts".
-> Die Schriftart installieren
-> Jetzt Rechner.exe öffnen
-> Rechtsclick auf den oberen Rand des Fensters (Wo auch das X ist)
-> Eigenschaften
-> Schriftart
-> Bei Schriftart "DejaVu Sans Mono Unifont" auswählen
-> OK

Jetzt sollten alle Zeichen richtig angezeigt werden und du kannst den Rechner vollständig nutzen.


Alternativ kannst du auch den Python Source-Code ausführen. Dafür benötigst du aber eine Installation von Python. Diese findest du auf https://www.python.org/downloads/. Nachdem du dies installiert hast kannst du auch den Rechner nutzen. Hier musst du den gleichen Prozess wie oben beschrieben machen um die Schriftart zu ändern. 


Der Rechner sollte nach Möglichkeit auf einem PC ausgeführt werden, die Zeilenumbrüche bei kleinen Screens nicht gut aussehen. 


Nützliche / Veränderbare Einstellungen

Du kannst entweder in der config.json Datei alle Einstellungen anpassen oder über den Rechner. Das kannst du über die 0-te Einstellung tun. Hier findest du Farben, Nachkommastellen, Variablen, diverse Einstellungen und Rechne- bzw. Lösungswege. Diese können mit den vorhandenen Einstellungen angepasst werden.

Außerdem kann man bei der Eingabe für z.B. einen Punkt "r" eingeben. Dadurch wird ein zufälliger Punkt mit Koordinaten zwischen -15 und 15 erzeugt (Kann im Code in StandardLib.py Zeile 10-11 random_lower, random_upper angepasst werden).
Für größere Eingaben erzeugt "r" immernur eine Spalte. Um z.B. eine Gerade vollständig zu füllen kannst du "rr" eingeben. Funktioniert auch für Ebene, Matrix, etc.


Dieser Rechner kann auch in einer Python Konsole für Android / IPhone ausgeführt werden, würde ich aber nicht empfehlen, da es zum einen umständlicher ist, man meist die Schriftart nicht ändern kann und der Platz meist nicht ausreicht.