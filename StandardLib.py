import json
import os
import random
from numbers import Number

import StandardLib as std
import classes as cla
from Colored import colored
from Colored import cprint

random_lower = -15
random_upper = 15

forma_counter = 0

config_ = None


def übersetzung_zahl_string_sub(zahl):
    """Gibt die Zahl in subscript an."""
    if zahl == 0:
        zahl = "₀"
    elif zahl == 1:
        zahl = "₁"
    elif zahl == 2:
        zahl = "₂"
    elif zahl == 3:
        zahl = "₃"
    elif zahl == 4:
        zahl = "₄"
    elif zahl == 5:
        zahl = "₅"
    elif zahl == 6:
        zahl = "₆"
    elif zahl == 7:
        zahl = "₇"
    elif zahl == 8:
        zahl = "₈"
    elif zahl == 9:
        zahl = "₉"
    return zahl


def übersetzung_zahl_string_sup(zahl):
    """Gibt die Zahl in superscript an."""
    if zahl == 0:
        zahl = "⁰"
    elif zahl == 1:
        zahl = "¹"
    elif zahl == 2:
        zahl = "²"
    elif zahl == 3:
        zahl = "³"
    elif zahl == 4:
        zahl = "⁴"
    elif zahl == 5:
        zahl = "⁵"
    elif zahl == 6:
        zahl = "⁶"
    elif zahl == 7:
        zahl = "⁷"
    elif zahl == 8:
        zahl = "⁸"
    elif zahl == 9:
        zahl = "⁹"
    return zahl


def übersetzung_zahl_param(zahl):
    """Gib x_zahl wieder."""
    if type(zahl) != str:
        zahl = str(zahl)
    res = "x"

    for char in zahl:
        zahl_sub = übersetzung_zahl_string_sub(int(char))
        res += zahl_sub

    return res


def display_farben():
    """Stellt die zur verfügung stehenden Farben dar."""
    print(colored("1: Rot", "red"))
    print(colored("2: Grün", "green"))
    print(colored("3: Gelb", "yellow"))
    print(colored("4: Blau", "blue"))
    print(colored("5: Violett", "magenta"))
    print(colored("6: Cyan", "cyan"))
    print(colored("7: Weiß", "white"))
    return


def cls():
    """Cleart den screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def hr():
    """Fügt einen vertikalen strich ein."""
    cprint("──────────────────────────────────────────────────────────────────────", get_color("abs"))
    return


def save_config(name, wert):
    """Speichert eine gegebene Konfiguration."""
    with open("config.json", "r") as conf:
        std_config = json.load(conf)

    std_config[name] = wert
    with open('config.json', 'w') as conf:
        json.dump(std_config, conf, indent=2)

    global config_
    config_ = std_config


def load_config():
    """Lädt die Konfiguration."""
    global config_
    if config_ is None:
        try:
            with open("config.json", "r") as conf:
                config_ = json.load(conf)
        except FileNotFoundError:
            save_config_standard()
            with open("config.json", "r") as conf:
                config_ = json.load(conf)

    err_far = cla.Farbe(config_["Error Farbe"], "Deutsch")

    config_iter_1 = get_iter("config")

    farben_de = ["Rot", "Grün", "Gelb", "Blau", "Violett", "Cyan", "Weiß"]
    farben_en = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]

    changed = False

    try:
        for i, liste in enumerate(config_iter_1):
            for item in liste:
                if i == 0:
                    if isinstance(config_[item], float):
                        save_config(item, int(round(config_[item], 0)))
                        changed = True

                    elif not isinstance(config_[item], int):
                        raise cla.InputError(colored(f"{item} ist keine Zahl: {config_[item]}", err_far.en))

                elif i == 1:
                    if config_[item] not in farben_de:
                        try:
                            wert = int(config_[item])
                            if wert in list(range(8)):
                                x = cla.Farbe(wert, "Zahl").de
                                save_config(item, x)
                                changed = True

                        except ValueError:
                            if config_[item] in farben_en:
                                save_config(config_[item], cla.Farbe(config_[item], "Englisch").de)
                                changed = True

                        else:
                            raise cla.InputError(colored(f"{item} ist keine Farbe: {config_[item]}", err_far.en))

                elif i == 2:
                    if isinstance(config_[item], str):
                        pass

                    elif isinstance(config_[item], list):
                        if len(config_[item]) != 2:
                            raise cla.InputError(colored(f"{item} ist keine Liste mit 2 Elementen: {config_[item]}", err_far.en))

                        if not isinstance(config_[item][0], str):
                            raise cla.InputError(colored(f"{item}[0] ist kein str: {config_[item]}", err_far.en))

                        if not isinstance(config_[item][1], str):
                            raise cla.InputError(colored(f"{item}[1] ist kein str: {config_[item]}", err_far.en))

                elif i == 3:
                    if not isinstance(config_[item], bool):
                        raise cla.InputError(colored(f"{item} ist kein bool: {config_[item]}", err_far.en))

                elif i == 4:
                    if isinstance(config_[item], float):
                        save_config(item, int(round(config_[item], 0)))
                        changed = True

                    elif not isinstance(config_[item], int):
                        raise cla.InputError(colored(f"{item} ist keine Zahl: {config_[item]}", err_far.en))

        if changed:
            config_ = load_config()

    except cla.InputError:
        cprint("Die Einstellungen wurden nicht erkannt. Sie werden nun auf den Standard zurückgesetzt\n\n", err_far.en)
        config_ = save_config_standard()

    return config_


def save_config_standard():
    """Stellt Eigenschaften wieder auf Standard her."""
    std_config = {
        "Nachkommastellen 1": 2,
        "Nachkommastellen 2": 3,
        "Nachkommastellen 3": 4,
        "Nachkommastellen Parser": 2,
        "Nachkommastellen Intern": 12,

        "Zwischenergebnis Farbe": "Violett",
        "Zwischenergebnis Zwischen Farbe": "Cyan",
        "Endergebnis Farbe": "Grün",
        "Abschnitt Farbe": "Gelb",
        "Menü Farbe": "Weiß",
        "Error Farbe": "Rot",
        "Eingabe Farbe": "Cyan",

        "Punkt 1 Buchstabe": "P",
        "Punkt 2 Buchstabe": "Q",
        "Punkt 3 Buchstabe": "R",

        "Vektor 1 Buchstabe": ["→", "v"],

        "Vektor 2 Buchstabe": ["→", "u"],

        "Gerade 1 Buchstabe": "g",
        "Gerade 1 Parameter": "r",

        "Gerade 2 Buchstabe": "h",
        "Gerade 2 Parameter": "s",

        "Ebene 1 Buchstabe": "E",
        "Ebene 1 Parameter 1": "s",
        "Ebene 1 Parameter 2": "t",

        "Ebene 2 Buchstabe": "F",
        "Ebene 2 Parameter 1": "u",
        "Ebene 2 Parameter 2": "v",

        "Matrix Buchstabe": "A",
        "Matrix Lösungsvektor Buchstabe": ["→", "x"],
        "Matrix LGS Vektor": "b",

        "Bruch": True,
        "Komma": False,

        "Gauss Pretty": False,

        "Rechenweg Absvec": False,
        "Rechenweg Vektor zwei Punkte": False,
        "Rechenweg Normalenvektor": False,
        "Rechenweg Normaleneinheitsvektor": True,
        "Rechenweg Skalarprodukt": True,
        "Rechenweg Lineare Abhängigkeit": True,
        "Rechenweg Umrechnung zwischen Ebenengleichungen": False,
        "Rechenweg Abstand zwischen Punkt und Gerade": True,
        "Rechenweg Abstand zwischen zwei Geraden": True,
        "Rechenweg Abstand zwischen Gerade und Ebene": True,
        "Rechenweg Abstand zwischen zwei Ebenen": True,
        "Rechenweg Gauss": False,

        "Lösungsweg Punktprobe Punkt Ebene": "lgs",  # lgs, koor
        "Lösungsweg Schnitt Gerade Ebene": "passend",  # lgs, koor, passend
        "Lösungsweg Schnitt Ebene Ebene": "passend",  # lgs, koor, passend
        "Lösungsweg Abstand Punkt Gerade": "hilf",  # hilf, geo
        "Lösungsweg Abstand Punkt Ebene": "lfp",  # hnf, lfp
        "Lösungsweg Abstand Gerade Gerade parallel": "hilf",  # hilf, geo
        "Lösungsweg Abstand Gerade Gerade windschief": "hnf",  # hnf, lfp
        "Lösungsweg Abstand Gerade Ebene": "hnf",  # hnf, lfp
        "Lösungsweg Abstand Ebene Ebene": "hnf",  # hnf, lfp
    }

    with open('config.json', 'w') as output:
        json.dump(std_config, output, indent=2)

    global config_
    config_ = std_config

    return std_config


def get_color(farbe=None, value=True, sprache="Englisch"):
    """Lädt die Farben."""
    config = load_config()
    zwi_far = cla.Farbe(config["Zwischenergebnis Farbe"], "Deutsch")
    zwi_zwi_far = cla.Farbe(config["Zwischenergebnis Zwischen Farbe"], "Deutsch")
    end_far = cla.Farbe(config["Endergebnis Farbe"], "Deutsch")
    abs_far = cla.Farbe(config["Abschnitt Farbe"], "Deutsch")
    men_far = cla.Farbe(config["Menü Farbe"], "Deutsch")
    err_far = cla.Farbe(config["Error Farbe"], "Deutsch")
    ein_far = cla.Farbe(config["Eingabe Farbe"], "Deutsch")

    if value:
        if sprache == "Deutsch":
            zwi_far = zwi_far.de
            zwi_zwi_far = zwi_zwi_far.de
            end_far = end_far.de
            abs_far = abs_far.de
            men_far = men_far.de
            err_far = err_far.de
            ein_far = ein_far.de

        elif sprache == "Englisch":
            zwi_far = zwi_far.en
            zwi_zwi_far = zwi_zwi_far.en
            end_far = end_far.en
            abs_far = abs_far.en
            men_far = men_far.en
            err_far = err_far.en
            ein_far = ein_far.en

        elif sprache == "Zahl":
            zwi_far = zwi_far.za
            zwi_zwi_far = zwi_zwi_far.za
            end_far = end_far.za
            abs_far = abs_far.za
            men_far = men_far.za
            err_far = err_far.za
            ein_far = ein_far.za

        elif sprache == "Alle":
            zwi_far = zwi_far.de, zwi_far.en, zwi_far.za
            zwi_zwi_far = zwi_zwi_far.de, zwi_zwi_far.en, zwi_zwi_far.za
            end_far = end_far.de, end_far.en, end_far.za
            abs_far = abs_far.de, abs_far.en, abs_far.za
            men_far = men_far.de, men_far.en, men_far.za
            err_far = err_far.de, err_far.en, err_far.za
            ein_far = ein_far.de, ein_far.en, ein_far.za

    if farbe is None:
        return zwi_far, zwi_zwi_far, end_far, abs_far, men_far, err_far, ein_far

    check = False
    if not isinstance(farbe, (list, tuple)):
        farbe = [farbe]
        check = True

    for item in farbe:
        if not isinstance(item, str):
            raise cla.InputError(colored(f"\nFarbe ist kein str, gescheitert an: str, \n{item}", err_far))

    out = []
    for item in farbe:
        if item == "zwi":
            out.append(zwi_far)

        elif item == "end":
            out.append(end_far)

        elif item == "zwi_end":
            out.append(zwi_zwi_far)

        elif item == "abs":
            out.append(abs_far)

        elif item == "men":
            out.append(men_far)

        elif item == "err":
            out.append(err_far)

        elif item == "ein":
            out.append(ein_far)

    if check:
        return out[0]
    return out


def get_prec(zahl=None):
    """Lädt die Nachkommastellen."""
    config = load_config()

    prec_1 = config["Nachkommastellen 1"]
    prec_2 = config["Nachkommastellen 2"]
    prec_3 = config["Nachkommastellen 3"]
    prec_parser = config["Nachkommastellen Parser"]
    prec_int = config["Nachkommastellen Intern"]

    if zahl is None:
        return prec_1, prec_2, prec_3, prec_parser, prec_int

    check = False
    if not isinstance(zahl, (list, tuple)):
        zahl = [zahl]
        check = True

    out = []
    for item in zahl:
        if item == 1:
            out.append(prec_1)

        elif item == 2:
            out.append(prec_2)

        elif item == 3:
            out.append(prec_3)

        elif str(item).lower() == "parser":
            out.append(prec_parser)

        elif str(item).lower() in ["intern", "int"]:
            out.append(prec_int)

    if check:
        return out[0]
    return out


def get_divers(wert):
    """Lädt, ob die diversen Einstellungen."""
    config = load_config()

    check = False
    if not isinstance(wert, (list, tuple)):
        wert = [wert]
        check = True

    out = []
    for item in wert:
        if item.lower() == "bruch":
            out.append(config["Bruch"])
        elif item.lower() == "komma":
            out.append(config["Komma"])
        elif item.lower() == "gauss pretty":
            out.append(config["Gauss Pretty"])

    if check:
        return out[0]
    return out


def get_lsg(wert):
    """Lädt die Einstellungen für Lösungs- und Rechenweg"""
    config = load_config()

    check = False
    if not isinstance(wert, (list, tuple)):
        wert = [wert]
        check = True

    out = []
    for item in wert:
        item = item.lower().replace("rweg", "rechenweg").replace("lsg", "lösungsweg").replace("lsgweg", "lösungsweg")
        if item == "rechenweg absvec":
            out.append(config["Rechenweg Absvec"])
        if item == "rechenweg vektor":
            out.append(config["Rechenweg Vektor zwei Punkte"])
        elif item == "rechenweg norm":
            out.append(config["Rechenweg Normalenvektor"])
        elif item == "rechenweg norm0":
            out.append(config["Rechenweg Normaleneinheitsvektor"])
        elif item == "rechenweg skalar":
            out.append(config["Rechenweg Skalarprodukt"])
        elif item == "rechenweg lin un":
            out.append(config["Rechenweg Lineare Abhängigkeit"])
        elif item == "rechenweg umrechnung":
            out.append(config["Rechenweg Umrechnung zwischen Ebenengleichungen"])
        elif item == "rechenweg dist p g":
            out.append(config["Rechenweg Abstand zwischen Punkt und Gerade"])
        elif item == "rechenweg dist g g":
            out.append(config["Rechenweg Abstand zwischen zwei Geraden"])
        elif item == "rechenweg dist g e":
            out.append(config["Rechenweg Abstand zwischen Gerade und Ebene"])
        elif item == "rechenweg dist e e":
            out.append(config["Rechenweg Abstand zwischen zwei Ebenen"])
        elif item == "rechenweg gauss":
            out.append(config["Rechenweg Gauss"])

        elif item == "lösungsweg punktprobe p e":
            out.append(config["Lösungsweg Punktprobe Punkt Ebene"])
        elif item == "lösungsweg schnitt g e":
            out.append(config["Lösungsweg Schnitt Gerade Ebene"])
        elif item == "lösungsweg schnitt e e":
            out.append(config["Lösungsweg Schnitt Ebene Ebene"])
        elif item == "lösungsweg dist p g":
            out.append(config["Lösungsweg Abstand Punkt Gerade"])
        elif item == "lösungsweg dist p e":
            out.append(config["Lösungsweg Abstand Punkt Ebene"])
        elif item == "lösungsweg dist g g parallel":
            out.append(config["Lösungsweg Abstand Gerade Gerade parallel"])
        elif item == "lösungsweg dist g g windschief":
            out.append(config["Lösungsweg Abstand Gerade Gerade windschief"])
        elif item == "lösungsweg dist g e":
            out.append(config["Lösungsweg Abstand Gerade Ebene"])
        elif item == "lösungsweg dist e e":
            out.append(config["Lösungsweg Abstand Ebene Ebene"])

    if check:
        try:
            return out[0]
        except IndexError:
            err_far = std.get_color("err")
            raise cla.InputError(colored(f"Irgendwas war mit dem Input Falsch:\n{wert}", err_far))
    return out


def get_iter(wert):
    """Gibt Iterables für diverse Operationen."""
    if wert == "config":
        iter_list = [["Nachkommastellen 1", "Nachkommastellen 2", "Nachkommastellen 3", "Nachkommastellen Parser",
                      "Nachkommastellen Intern"],
                     ["Zwischenergebnis Farbe", "Zwischenergebnis Zwischen Farbe", "Endergebnis Farbe", "Abschnitt Farbe",
                      "Menü Farbe", "Error Farbe", "Eingabe Farbe"],
                     ["Punkt 1 Buchstabe", "Punkt 2 Buchstabe", "Punkt 3 Buchstabe",
                      "Vektor 1 Buchstabe", "Vektor 2 Buchstabe",
                      "Gerade 1 Buchstabe", "Gerade 1 Parameter", "Gerade 2 Buchstabe", "Gerade 2 Parameter",
                      "Ebene 1 Buchstabe", "Ebene 1 Parameter 1", "Ebene 1 Parameter 2",
                      "Ebene 2 Buchstabe", "Ebene 2 Parameter 1", "Ebene 2 Parameter 2",
                      "Matrix Buchstabe", "Matrix Lösungsvektor Buchstabe", "Matrix LGS Vektor"],
                     ["Bruch", "Komma", "Gauss Pretty"]]

    elif wert == "config_buchst":
        iter_list = ["Punkt 1 Buchstabe", "Punkt 2 Buchstabe", "Punkt 3 Buchstabe",
                     "Vektor 1 Buchstabe", "Vektor 2 Buchstabe",
                     "Gerade 1 Buchstabe", "Gerade 1 Parameter", "Gerade 2 Buchstabe", "Gerade 2 Parameter",
                     "Ebene 1 Buchstabe", "Ebene 1 Parameter 1", "Ebene 1 Parameter 2",
                     "Ebene 2 Buchstabe", "Ebene 2 Parameter 1", "Ebene 2 Parameter 2",
                     "Matrix Buchstabe", "Matrix Lösungsvektor Buchstabe", "Matrix LGS Vektor"]

    elif wert == "config_buchst_darst":
        iter_list = ["Buchstabe des ersten Punktes", "Buchstabe des zweiten Punktes", "Buchstabe des dritten Punktes",
                     "Buchstabe des ersten Vektors", "Buchstabe des zweiten Vektors",
                     "Buchstabe der ersten Gerade", "Parameter der ersten Gerade",
                     "Buchstabe der zweiten Gerade", "Parameter der zweiten Gerade",
                     "Buchstabe der ersten Ebene", "Richtungsvektor 1 der ersten Ebene", "Richtungsvektor 2 der ersten Ebene",
                     "Buchstabe der zweiten Ebene", "Richtungsvektor 1 der zweiten Ebene", "Richtungsvektor 2 der zweiten Ebene",
                     "Buchstabe der Matrix", "Buchstabe des Lösungsvektors einer Matrix",
                     "Buchstabe des Vektors, der die Lösung eines LGS enthält"]

    elif wert == "config_divers":
        iter_list = ["Bruch", "Komma"]

    elif wert == "config_divers_darst":
        iter_list = ["Soll nach möglichkeit ein Bruch angezeigt werden?",
                     "Soll ein Komma für Dezimalstellen angezeigt werden?"]

    elif wert == "config_prec":
        iter_list = ["Nachkommastellen 1", "Nachkommastellen 2", "Nachkommastellen 3", "Nachkommastellen Parser",
                     "Nachkommastellen Intern"]

    elif wert == "config_prec_darst":
        iter_list = ["Anzahl der Nachkommazellen für normale Zahlen:", "Anzahl der Nachkommazellen für genauere Zahlen:",
                     "Anzahl der Nachkommazellen für sehr genaue Zahlen:", "Anzahl der Nachkommazellen für den Parser:",
                     "Anzahl der Nachkommazellen für interne Vergleiche:"]

    elif wert == "config_farben":
        iter_list = ["Zwischenergebnis Farbe", "Zwischenergebnis Zwischen Farbe", "Endergebnis Farbe", "Abschnitt Farbe",
                     "Menü Farbe", "Error Farbe", "Eingabe Farbe"]

    elif wert == "config_farben_darst":
        iter_list = ["Farbe der Zwischenergebnisse:", "Farbe der geschachtelten Zwischenergebnisse:",
                     "Farbe der Endergebnisse:", "Farbe eines neuen Abschnittes im Rechenweg:", "Farbe des Menüs:",
                     "Farbe der Fehlermeldungen:", "Farbe von der Zusammenfassung der Eingabe:"]

    elif wert == "config_lösung":
        iter_list = ["Rechenweg Absvec", "Rechenweg Vektor zwei Punkte", "Rechenweg Normalenvektor", "Rechenweg Normaleneinheitsvektor", "Rechenweg Skalarprodukt", "Rechenweg Lineare Abhängigkeit",
                     "Rechenweg Umrechnung zwischen Ebenengleichungen", "Rechenweg Abstand zwischen Punkt und Gerade", "Rechenweg Abstand zwischen zwei Geraden",
                     "Rechenweg Abstand zwischen Gerade und Ebene", "Rechenweg Abstand zwischen zwei Ebenen", "Rechenweg Gauss", "Lösungsweg Punktprobe Punkt Ebene",
                     "Lösungsweg Schnitt Gerade Ebene", "Lösungsweg Schnitt Ebene Ebene", "Lösungsweg Abstand Punkt Gerade", "Lösungsweg Abstand Punkt Ebene",
                     "Lösungsweg Abstand Gerade Gerade parallel", "Lösungsweg Abstand Gerade Gerade windschief", "Lösungsweg Abstand Gerade Ebene", "Lösungsweg Abstand Ebene Ebene"]

    elif wert == "config_lösung_darst":
        iter_list = ["Rechenweg für den Betrag eines Vektors", "Rechenweg für den Vektor aus zwei Punkten", "Rechenweg für den Normalenvektor", "Rechenweg für den Normaleneinheitsvektor", "Rechenweg für das Skalarprodukt",
                     "Rechenweg für Lineare Abhängigkeit", "Rechenweg für das Umrechnen der Ebenengleichungen", "Rechenweg für den Abstand zwischen Punkt und Gerade",
                     "Rechenweg für den Abstand zwischen zwei Geraden", "Rechenweg für den Abstand zwischen Gerade und Ebene", "Rechenweg für den Abstand zwischen zwei Ebenen",
                     "Rechenweg für den Gauss Algorithmus", "Lösungsweg für die Punktprobe von Punkt und Ebene", "Lösungsweg für den Schnitt aus Gerade und Ebene",
                     "Lösungsweg für den Schnitt zweier Ebenen", "Lösungsweg für den Abstand zwischen Punkt und Gerade", "Lösungsweg für den Abstand zwischen Punkt und Ebene",
                     "Lösungsweg für den Abstand zwischen zwei parallelen Geraden", "Lösungsweg für den Abstand zwischen zwei windschiefen Geraden",
                     "Lösungsweg für den Abstand zwischen Gerade und Ebene", "Lösungsweg für den Abstand zwischen zwei Ebenen"]

    elif wert == "farben_de":
        iter_list = ["Rot", "Grün", "Gelb", "Blau", "Violett", "Cyan", "Weiß", None]

    elif wert == "farben_en":
        iter_list = ["red", "green", "yellow", "blue", "magenta", "cyan", "white", None]

    elif wert == "farben_alle":
        iter_list = [["Rot", "Grün", "Gelb", "Blau", "Violett", "Cyan", "Weiß"], ["red", "green", "yellow", "blue", "magenta"],
                     list(range(8))]

    elif wert == "operation_lagl_darst":
        iter_list = ["Multiplikation zweier Matrizen", "Gauss Algorithmus einer n x m Matrix"]

    elif wert == "inputs":
        iter_list = [int, float, bool, str, None, list, Number, "list matrix", "matrix", "ebene", "ebene darst", "gerade",
                     "punkt", "vektor", "dimension", "buchstabe", "farben_de", "farben_en"]

    return iter_list


def get_parameter():
    """Gibt Parameter zurück."""
    return [["r", "s", "t", "u", "v", "w"],
            ["α", "β", "γ", "δ", "ε", "ζ", "θ", "ϑ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "ρ", "σ", "τ", "υ", "φ", "χ", "ψ", "ω"]]


def verify_input(inp, name, erlaubte_werte, streng=False):
    """Checkt ob der gegebene Input valide ist."""
    err_far = get_color("err")
    prec_int = get_prec("int")

    if not isinstance(erlaubte_werte, (list, tuple)):
        erlaubte_werte = [erlaubte_werte]

    inputs = get_iter("inputs")

    if not all(item in inputs for item in erlaubte_werte):
        raise cla.InputError(colored(f"\nNicht alle Elemente in erlaubte_werte sind erlaubt! \n{list(item for item in erlaubte_werte if item not in inputs)}", err_far))

    def verify_matrix(inp, streng=False):
        if streng:
            if not isinstance(inp, cla.Matrix):
                raise cla.InputError(colored(f"\n{name} ist keine Matrix, gescheitert an: Matrix, \n{inp}", err_far))

        if isinstance(inp, cla.Matrix):
            return True

        if not isinstance(inp, (list, tuple)):
            raise cla.InputError(colored(f"{name} ist keine list matrix, gescheitert an: list, \n{inp}", err_far))

        if not all(isinstance(item, (list, tuple)) for item in inp):
            raise cla.InputError(colored(f"\n{name} ist keine list matrix, gescheitert an: innerer list, \n{inp}", err_far))

        leng = len(inp[0])
        if not all(len(item) == leng for item in inp):
            raise cla.InputError(colored(f"\n{name} ist keine list matrix, gescheitert an: länge, \n{inp}", err_far))

        if not all(isinstance(item, (Number, str)) for row in inp for item in row):
            raise cla.InputError(colored(f"\n{name} ist keine list matrix, gescheitert an: Number in innerer list, \n{inp}", err_far))

        return True

    def verify_ebene(inp, streng=False):
        if streng:
            if not isinstance(inp, cla.Ebene):
                raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: streng - Ebene, \n{inp}", err_far))

        if isinstance(inp, cla.Ebene):
            return True

        elif not isinstance(inp, (list, tuple)):
            raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: list, \n{inp}", err_far))

        elif all(isinstance(item, (list, tuple)) for item in inp):
            # Norm oder Para
            if len(inp) not in [2, 3]:
                raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: len({name}) != 2 / 3, \n{inp}", err_far))

            if len(inp) == 2:
                # Norm
                if not all(isinstance(item, (Number, str)) for row in inp for item in row):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Norm - Number for..., \n{inp}", err_far))

                if not all(len(item) in [2, 3] for item in inp):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Norm - len(item) != 2 for..., \n{inp}", err_far))

                if not len(inp[0]) == len(inp[1]):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Norm - len({name}[0]) != len({name}[1]), \n{inp}", err_far))


            elif len(inp) == 3:
                # Para
                if not all(isinstance(item, (Number, str)) for row in inp for item in row):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Para - Number for..., \n{inp}", err_far))

                if not all(len(item) in [2, 3] for item in inp):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Para - len(item) != 2 for..., \n{inp}", err_far))

                if not len(inp[0]) == len(inp[1]) == len(inp[2]):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Para - len({name}[0]) != len({name}[1]), \n{inp}", err_far))

                if all(round(a, prec_int) == round(b, prec_int) if isinstance(a, Number) and isinstance(b, Number) else 0 for a, b in zip(inp[1], inp[2])):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Richtungsvektoren sind gleich, \n{inp}", err_far))

                if not all(any(round(item, prec_int) if isinstance(item, Number) else 1 for item in row) for row in inp[1:]):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Ein Richtungsvektor ist [0, 0, 0], \n{inp}", err_far))

                param = []
                for i in range(len(inp[0])):
                    if isinstance(inp[1][i], str) or isinstance(inp[2][i], str):
                        param.append("F")

                    elif inp[1][i] == 0 and inp[2][i] == 0:
                        param.append("*")

                    elif round(inp[1][i], prec_int) == 0 or round(inp[2][i], prec_int) == 0:
                        param.append(0)

                    else:
                        param.append(inp[2][i] / inp[1][i])

                for item in param:
                    if isinstance(item, Number):
                        wert = item
                        break
                else:
                    wert = 1

                if all(round(item, prec_int) == round(wert, prec_int) if isinstance(item, Number) else 0 for item in param) and (round(wert, prec_int) != 0):
                    raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Die Richtungsvektoren sind linear abhängig, \n{inp}", err_far))

        else:
            # Koor
            if not all(isinstance(item, (Number, str)) for item in inp):
                raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Koor - Number for..., \n{inp}", err_far))

            if len(inp) != 4:
                raise cla.InputError(colored(f"\n{name} ist keine Ebene, gescheitert an: Koor - len != 4, \n{inp}", err_far))

        return True

    def verify_ebene_darst(inp):
        if not isinstance(inp, str):
            raise cla.InputError(colored(f"\n{name} ist keine Ebene darst, gescheitert an: str, \n{inp}", err_far))

        if inp not in ["para", "norm", "koor"]:
            raise cla.InputError(colored(f'\n{name} ist keine Ebene darst, gescheitert an: inp in ["para", "norm", "koor"], \n{inp}', err_far))

        return True

    def verify_gerade(inp, streng=False):
        if streng:
            if not isinstance(inp, cla.Gerade):
                raise cla.InputError(colored(f"\n{name} ist keine Gerade, gescheitert an: streng - Gerade, \n{inp}", err_far))

        if isinstance(inp, cla.Gerade):
            return True

        elif not isinstance(inp, (list, tuple)):
            raise cla.InputError(colored(f"\n{name} ist keine Gerade, gescheitert an: list, \n{inp}", err_far))

        elif not all(isinstance(item, (list, tuple)) for item in inp):
            raise cla.InputError(colored(f"\n{name} ist keine Gerade, gescheitert an: list for..., \n{inp}", err_far))

        if not all(isinstance(item, (Number, str)) for row in inp for item in row):
            raise cla.InputError(colored(f"\n{name} ist keine Gerade, gescheitert an: Number for..., \n{inp}", err_far))

        elif len(inp) != 2:
            raise cla.InputError(colored(f"\n{name} ist keine Gerade, gescheitert an: len({name}) != 2, \n{inp}", err_far))

        if not all(len(item) in [2, 3] for item in inp):
            raise cla.InputError(colored(f"\n{name} ist keine Gerade, gescheitert an: len(item) != 2/3 for..., \n{inp}", err_far))

        elif not len(inp[0]) == len(inp[1]):
            raise cla.InputError(colored(f"\n{name} ist keine Gerade, gescheitert an: len({name}[0]) == len({name}[1]), \n{inp}", err_far))

        return True

    def verify_punkt(inp, streng=False):
        if streng:
            if not isinstance(inp, cla.Punkt):
                raise cla.InputError(colored(f"\n{name} ist kein Punkt, gescheitert an: streng - Punkt, \n{inp}", err_far))

        if isinstance(inp, cla.Punkt):
            return True

        elif not isinstance(inp, (list, tuple)):
            raise cla.InputError(colored(f"\n{name} ist kein Punkt, gescheitert an: list, \n{inp}", err_far))

        elif len(inp) not in [2, 3]:
            raise cla.InputError(colored(f"\n{name} ist kein Punkt, gescheitert an: len({name}) != 2/3, \n{inp}", err_far))

        elif not all(isinstance(item, (Number, str)) for item in inp):
            raise cla.InputError(colored(f"\n{name} ist kein Punkt, gescheitert an: Number for..., \n{inp}", err_far))

        return True

    def verify_vektor(inp, streng=False):
        if streng:
            if not isinstance(inp, cla.Vektor):
                raise cla.InputError(colored(f"\n{name} ist kein Vektor, gescheitert an: streng - Punkt, \n{inp}", err_far))

        if isinstance(inp, cla.Vektor):
            return True

        elif not isinstance(inp, (list, tuple)):
            raise cla.InputError(colored(f"\n{name} ist kein Vektor, gescheitert an: list, \n{inp}", err_far))

        elif len(inp) not in [2, 3]:
            raise cla.InputError(colored(f"\n{name} ist kein Vektor, gescheitert an: len({name}) != 2/3, \n{inp}", err_far))

        elif not all(isinstance(item, (Number, str)) for item in inp):
            raise cla.InputError(colored(f"\n{name} ist kein Vektor, gescheitert an: Number for..., \n{inp}", err_far))

        return True

    def verify_dimension(inp):
        if not isinstance(inp, (list, tuple)):
            raise cla.InputError(colored(f"\n{name} ist keine Dimension, gescheitert an: list, \n{inp}", err_far))

        if len(inp) != 2:
            raise cla.InputError(colored(f"\n{name} ist keine Dimension, gescheitert an: len != 2, \n{inp}", err_far))

        if not all(isinstance(item, Number) for item in inp):
            raise cla.InputError(colored(f"\n{name} ist keine Dimension, gescheitert an: Number, \n{inp}", err_far))

        return True

    def verify_buchstabe(inp):
        if isinstance(inp, (list, tuple)):
            if len(inp) != 2:
                cla.InputError(colored(f"\n{name} ist kein Buchstabe, gescheitert an: list len != 2, \n{inp}", err_far))

            if not all(isinstance(item, str) for item in inp):
                raise cla.InputError(colored(f"\n{name} ist kein Buchstabe, gescheitert an: str in list, \n{inp}", err_far))


        elif not isinstance(inp, str):
            raise cla.InputError(colored(f"\n{name} ist kein Buchstabe, gescheitert an: str, \n{inp}", err_far))

        return True

    def verify_farben_de(inp):
        if inp not in get_iter("farben_de"):
            raise cla.InputError(colored(f"\n{name} ist keine Farbe, gescheitert an: color, \n{inp}", err_far))

        return True

    def verify_farben_en(inp):
        if inp not in get_iter("farben_en"):
            raise cla.InputError(colored(f"\n{name} ist keine Farbe, gescheitert an: color, \n{inp}", err_far))

        return True

    def verify_int(inp):
        if not isinstance(inp, int):
            raise cla.InputError(colored(f"\n{name} ist kein int, gescheitert an: int, \n{inp}", err_far))

        return True

    def verify_float(inp):
        if not isinstance(inp, float):
            raise cla.InputError(colored(f"\n{name} ist kein float, gescheitert an: float, \n{inp}", err_far))

        return True

    def verify_bool(inp):
        if not isinstance(inp, bool) and inp != "force" and inp is not None:
            raise cla.InputError(colored(f"\n{name} ist kein bool, gescheitert an: bool, \n{inp}", err_far))

        return True

    def verify_str(inp):
        if not isinstance(inp, str):
            raise cla.InputError(colored(f"\n{name} ist kein str, gescheitert an: str, \n{inp}", err_far))

        return True

    def verify_None(inp):
        if inp is not None:
            raise cla.InputError(colored(f"\n{name} ist kein None, gescheitert an: None, \n{inp}", err_far))

        return True

    def verify_list(inp):
        if not isinstance(inp, (list, tuple)):
            raise cla.InputError(colored(f"\n{name} ist keine Liste, gescheitert an: list, \n{inp}", err_far))

        leng = len(inp[0])
        if not all(len(item) == leng for item in inp):
            raise cla.InputError(colored(f"\n{name} ist keine Liste, gescheitert an: länge, \n{inp}", err_far))

        if not all(isinstance(item, Number) for item in inp):
            raise cla.InputError(colored(f"\n{name} ist keine Liste, gescheitert an: Number, \n{inp}", err_far))

    def verify_number(inp):
        if not isinstance(inp, Number):
            raise cla.InputError(colored(f"\n{name} ist keine Zahl, gescheitert an: Number, \n{inp}", err_far))

        return True

    def checker(check, item):
        if item == "matrix":
            check = verify_matrix(inp, streng)

        elif item == "ebene":
            check = verify_ebene(inp, streng)

        elif item == "ebene darst":
            check = verify_ebene_darst(inp)

        elif item == "gerade":
            check = verify_gerade(inp, streng)

        elif item == "punkt":
            check = verify_punkt(inp, streng)

        elif item == "vektor":
            check = verify_vektor(inp, streng)

        elif item == "dimension":
            check = verify_dimension(inp)

        elif item == "buchstabe":
            check = verify_buchstabe(inp)

        elif item == "farben_de":
            check = verify_farben_de(inp)

        elif item == "farben_en":
            check = verify_farben_en(inp)

        elif item == int:
            check = verify_int(inp)

        elif item == float:
            check = verify_float(inp)

        elif item == bool:
            check = verify_bool(inp)

        elif item == str:
            check = verify_str(inp)

        elif item is None:
            check = verify_None(inp)

        elif item == Number:
            check = verify_number(inp)

        if check:
            return check

    check = False
    for item in erlaubte_werte:
        try:
            check = checker(check, item)
            if check:
                return True

        except cla.InputError:
            pass

    if check is False:
        for item in erlaubte_werte:
            checker(check, item)

    else:
        return True


def dynamic_type(objekt, available_types, typ=None, instantiate=False, previous=None):
    transl = {"punkt": cla.Punkt, "gerade": cla.Gerade, "ebene": cla.Ebene}

    if not isinstance(available_types, (list, tuple)):
        available_types = [available_types]

    err_far = std.get_color("err")

    for key, value in transl.items():
        if key in available_types and isinstance(objekt, value):
            typ = key
            isinst = True
            return typ, objekt
    else:
        if not isinstance(objekt, (list, tuple)):
            raise cla.InputError(colored(f"Das Objekt ist instanziiert, aber nicht in den verfügbaren Typen:\n{objekt}", err_far))

        if typ is not None:
            pass

        elif isinstance(objekt[0], (list, tuple)):
            if len(objekt) == 2 and typ is None:
                raise cla.InputError(colored(f"Der Typ von dem Objekt konnte nicht dynamisch herausgefunden werden. Die länge war 2 - uneindeutig ob Gerade oder Normalform:\n{objekt}", err_far))
            if len(objekt) == 3:
                typ = "ebene"
            else:
                typ = None
        else:
            if len(objekt) == 3:
                typ = "punkt"
            elif len(objekt) == 4:
                typ = "ebene"
            else:
                typ = None

    if typ is None:
        raise cla.InputError(colored(f"Es gab einen Fehler bei der Typ bestimmung: Typ is None:\n {typ}", err_far))

    if not instantiate:
        return typ

    if previous is not None and not isinstance(previous, (cla.Punkt, cla.Gerade, cla.Ebene)):
        raise cla.InputError(colored(f"Das vorherige Objekt ist nicht instanziiert:\n{previous}", err_far))
    if typ == "punkt":
        buchst = ["P", "Q"]
        if isinstance(previous, cla.Punkt):
            buchst.remove(previous.buchst)

        objekt = cla.Punkt(objekt, buchst=buchst[0])
    elif typ == "gerade":
        buchst = ["g", "h"]
        param = ["r", "s"]
        if isinstance(previous, cla.Gerade):
            buchst.remove(previous.buchst)
            param.remove(previous.param)

        objekt = cla.Gerade(objekt, buchst=buchst[0], param=param[0])

    elif typ == "ebene":
        buchst = ["E", "F"]
        param = ["s", "t", "u", "v"]
        if isinstance(previous, cla.Ebene):
            buchst.remove(previous.buchst)
            param.remove(previous.param[0])
            param.remove(previous.param[1])

        objekt = cla.Ebene(objekt, buchst=buchst[0], param=param[0:2])

    return typ, objekt


def parser(objekt, dim=3, darst=None, buchst=None, param=None, weitere=None, weitere_color=None):
    """

    Parameters
    ----------
    objekt          Welches Objekt geparsed werden soll: matrix, ebene, gerade, punkt, vektor, linear abhängig.
    dim             Welche Dimension wird geparsed (2/3) - für Matrix [n, m]
    darst           Darstellung für die Ebene oder zeilen für Matrix
    buchst          Welcher Buchstabe soll angezeigt werden
    param           Welcher Parameter soll angezeigt werden
    weitere         Liste von weiteren Objekten, die oben drüber angezeigt werden sollen
    weitere_color   Die Farben für die Objekte

    Returns
    -------
    Das geparsde Objekt - ggf. auch list wenn linear abhängig.
    """
    verify_input(weitere_color, "Farben", "farben_en"), verify_input(buchst, "Buchstabe", ("buchstabe", None))

    cls()
    prec_parser = get_prec("parser")
    ein_far = get_color("ein")
    err_far = get_color("err")
    err = cla.Input()

    if objekt == "matrix":
        verify_input(dim, "Dimension", "dimension")
        if buchst is None:
            buchst = "A"
        if darst in [None, True]:
            zeilen = True

        elif darst is False:
            zeilen = False

        else:
            raise cla.InputError(colored(f"darst (Matrix) is nicht None, True oder False: {darst}", err_far))

        if param is True:
            ekm = True
        else:
            ekm = False

        parsed = cla.Matrix([["" for i in range(dim[1])] for j in range(dim[0])], zeilen=zeilen, A_buchst=buchst, b=[""] * dim[0] if ekm else None)
        if isinstance(dim, list):
            old_dim = dim.copy()
        else:
            old_dim = dim

        if zeilen:
            dim = dim[1]
        else:
            dim = dim[0]

        if ekm is False:
            iter_list = parsed.A
        else:
            iter_list = parsed.A
            _ = ["" for i in range(len(iter_list))]
            for i in range(len(iter_list)):
                iter_list[i].append(_[i])

            b = ["" for i in range(old_dim[0])]
            dim += 1



    elif objekt == "ebene":
        if buchst is None:
            buchst = "E"
        if param is None:
            param = ["s", "t"]

        if dim != 3:
            raise cla.InputError(colored(f"Für dim != 3 ergeben Ebenen keinen Sinn! {dim}", err_far))
        if darst == "para":
            parsed = cla.Ebene([[" " * 3 for i in range(dim)] for i in range(3)], buchst=buchst, param=param)
            iter_list = [parsed.sv, parsed.rv_1, parsed.rv_2]

        elif darst == "norm":
            parsed = cla.Ebene([[" " * 3 for i in range(dim)] for i in range(2)], buchst=buchst, param=param)
            iter_list = [parsed.sv, parsed.nv]

        elif darst == "koor":
            parsed = cla.Ebene([" " * 1 for i in range(4)], buchst=buchst, param=param)
            iter_list = [parsed.kv]
            dim = 4

    elif objekt == "gerade":
        if buchst is None:
            buchst = "g"
        if param is None:
            param = "r"

        parsed = cla.Gerade([[" " * 3 for i in range(dim)] for i in range(2)], buchst=buchst, param=param)
        iter_list = [parsed.sv, parsed.rv]

    elif objekt == "punkt":
        if buchst is None:
            buchst = "P"
        parsed = cla.Punkt([" " for i in range(dim)], buchst=buchst)
        iter_list = [parsed.P]

    elif objekt == "vektor":
        if buchst is None:
            buchst = "v"
        parsed = cla.Vektor([" " * 3 for i in range(dim)], buchst=buchst)
        iter_list = [parsed.v]

    elif objekt == "linear abhängig":
        if buchst is None:
            buchst = "μ"
        parsed = [cla.Vektor([" " * 3 for i in range(dim)], buchst="u"), cla.Vektor([" " * 3 for i in range(dim)], buchst="v")]
        mitte = int(dim / 2)
        iter_list = [parsed[0].v, parsed[1].v]

    if weitere is not None:
        if not isinstance(weitere, (list, tuple)):
            weitere = [weitere]

        if weitere_color is None:
            weitere_color = [ein_far for i in range(len(weitere))]

        else:
            if isinstance(weitere_color, str):
                weitere_color = [weitere_color]

            if len(weitere) != len(weitere_color):
                i = len(weitere_color)
                if len(weitere_color) < len(weitere):
                    while i < len(weitere):
                        weitere_color.append(ein_far)
                        i += 1

                elif len(weitere_color) > len(weitere):
                    weitere_color = weitere_color[:len(weitere)]

            all(verify_input(item, "Weitere Farbe", "farben_en") for item in weitere_color)

    check = False
    check1 = True
    n = 0
    while n < len(iter_list):
        if check1:
            i = 0
        check1 = True
        pars = iter_list[n]

        while i < dim:
            if objekt == "punkt" or (objekt == "ebene" and darst == "koor"):
                pars[i] = "•"
            elif objekt == "matrix" and i == dim - 1:
                parsed.b[n] = "• "
            else:
                pars[i] = " • "
            err.error = True
            while err.error:
                if weitere is not None:
                    for item, color in zip(weitere, weitere_color):
                        item.display(prec_parser, color)
                        print("\n\n")

                if objekt == "linear abhängig":
                    u_darst = parsed[0].display(prec_parser, print_buchst=False, print_=False)
                    v_darst = parsed[1].display(prec_parser, print_buchst=False, print_=False)
                    mu = format_prec([f" = {buchst} ∙ " if i == mitte else "" for i in range(dim)], string=True)
                    for j in range(dim):
                        print(f"{u_darst[j]}{mu[j]}{v_darst[j]}")

                else:
                    parsed.display(prec_parser)

                zahl = user_input(err, min_amount=False, random=True, erlaubte_werte=["b", "br"])

            if zahl == "b":
                pars[i] = ""
                if objekt == "matrix" and i == dim - 1:
                    parsed.b[n] = ""
                if i == 0:
                    n -= 2
                    i = dim - 1
                    check1 = False
                    break
                else:
                    i -= 1
                    continue

            elif zahl == "br" and objekt == "matrix":
                if i == 0:
                    pars[0] = ""
                    n -= 1

                iter_list[n] = ["" for _ in range(dim)]
                parsed.b[n] = ""
                pars = iter_list[n]
                n -= 1
                check1 = True
                break

            if zahl == "r":
                random_auffüllen(pars)
                if objekt == "matrix" and param is True:
                    parsed.b[n] = pars[-1]
                    b[n] = pars[-1]

                break

            elif zahl == "rr":
                for item in iter_list[n:]:
                    random_auffüllen(item)
                    if objekt == "matrix" and param is True:
                        parsed.b[n] = item[-1]
                        b[n] = item[-1]
                        n += 1

                check = True
                break

            else:
                pars[i] = zahl

            if i == len(pars) - 1 and objekt == "matrix" and param is True:
                parsed.b[n] = pars[i]
                b[n] = pars[i]

            i += 1

        if check:
            break
        n += 1

    if len(iter_list) == 1:
        iter_list = iter_list[0]

    if objekt == "matrix":
        if param is True:
            for i in range(len(iter_list)):
                iter_list[i].pop()
            parsed = cla.Matrix(iter_list, b=b, zeilen=zeilen, A_buchst=buchst)
        else:
            parsed = cla.Matrix(iter_list, zeilen=zeilen, A_buchst=buchst)

    elif objekt == "ebene":
        if darst == "para":
            parsed = cla.Ebene(iter_list, buchst=buchst, param=param)

        elif darst == "norm":
            parsed = cla.Ebene(iter_list, buchst=buchst, param=param)

        elif darst == "koor":
            parsed = cla.Ebene(iter_list, buchst=buchst, param=param)

    elif objekt == "gerade":
        parsed = cla.Gerade(iter_list, buchst=buchst, param=param)

    elif objekt == "punkt":
        parsed = cla.Punkt(iter_list, buchst=buchst)

    elif objekt == "vektor":
        parsed = cla.Vektor(iter_list, buchst=buchst)

    elif objekt == "linear abhängig":
        parsed = [cla.Vektor(iter_list[0], buchst="u"), cla.Vektor(iter_list[1], buchst="v")]

    if weitere is not None:
        for item, color in zip(weitere, weitere_color):
            item.display(prec_parser, color)
            print("\n\n")

    if objekt == "linear abhängig":
        u_darst = parsed[0].display(prec_parser, print_buchst=False, print_=False)
        v_darst = parsed[1].display(prec_parser, print_buchst=False, print_=False)
        mu = format_prec([f" = {buchst} ∙ " if i == mitte else "" for i in range(dim)], string=True)
        for j in range(dim):
            cprint(u_darst[j], ein_far, end=""), cprint(mu[j], ein_far, end=""), cprint(v_darst[j], ein_far)

    else:
        parsed.display(prec_parser, ein_far)

    return parsed


def input_darst_ebene(erste=False, zweite=False):
    """Prompt für Ebene."""
    err = cla.Input()
    if erste:
        erste_darst = " ersten"
    else:
        erste_darst = ""

    if zweite:
        if erste:
            zweite_darst = ""
            dritte_darst = " zweiten"
        else:
            zweite_darst = " zweiten"
    else:
        zweite_darst = ""

    while err.error:
        print(f"Welche Darstellungsform der{erste_darst}{zweite_darst} Ebene möchtest du benutzen?\n")
        print("1: Parameterform")
        print("2: Normalenform")
        print("3: Koordinatenform")
        darst_1 = user_input(err, string=True, ebene_darst=True)

    if darst_1 == 1:
        darst_1 = "para"
    elif darst_1 == 2:
        darst_1 = "norm"
    elif darst_1 == 3:
        darst_1 = "koor"

    if erste and zweite:
        err.error = True
        while err.error:
            print(f"Welche Darstellungsform der{dritte_darst} Ebene möchtest du benutzen?\n")
            print("1: Parameterform")
            print("2: Normalenform")
            print("3: Koordinatenform")
            darst_2 = user_input(err, string=True, ebene_darst=True)

        if darst_2 == 1:
            darst_2 = "para"
        elif darst_2 == 2:
            darst_2 = "norm"
        elif darst_2 == 3:
            darst_2 = "koor"

        return darst_1, darst_2

    return darst_1


def input_lösungsansatz(lösungen, beides=True):
    """Prompt für Lösungsansatz"""
    men_far = get_color("men")
    err = cla.Input()
    leng = len(lösungen)
    if beides:
        leng += 1

    while err.error:
        cprint("Über welchen Lösungsansatz möchtest du rechnen?\n", men_far)
        for i, item in enumerate(lösungen, start=1):
            if item == "lgs":
                cprint(f"{i}: LGS aufstellen", men_far)

            elif item == "koor":
                cprint(f"{i}: Einsetzen in die Koordinatenform", men_far)

            elif item == "lfp":
                cprint(f"{i}: Lotfußpunkt bestimmen", men_far)

            elif item == "geo":
                cprint(f"{i}: Geometrischer Ansatz", men_far)

            elif item == "hnf":
                cprint(f"{i}: HNF", men_far)

        if beides:
            cprint(f"{i + 1}: Beides", men_far)

        lsgweg = user_input(err, max_amount=leng)

        for i in range(1, leng + 1):
            if lsgweg == i:
                if i == leng and beides:
                    return "beides"

                return lösungen[i - 1]


def input_umrechnen(von=False, nach=False, streng=True):
    """Prompt für Umrechnen"""
    men_far, err_far = get_color("men"), get_color("err")
    err = cla.Input()

    if von:
        while err.error:
            cprint("Umrechnen von:\n", men_far)
            cprint("1: Parameterform", men_far)
            cprint("2: Normalenform", men_far)
            cprint("3: Koordinatenform", men_far)
            darst_1 = user_input(err, string=True, ebene_darst=True)

    if nach:
        err.error = True
        while err.error:
            cprint("Umrechnen nach:\n", men_far)
            if streng is False or darst_1 != "para":
                cprint("1: Parameterform", men_far)
            else:
                print()
            if streng is False or darst_1 != "norm":
                cprint("2: Normalenform", men_far)
            else:
                print()
            if streng is False or darst_1 != "koor":
                cprint("3: Koordinatenform", men_far)
            else:
                print()

            darst_2 = user_input(err, string=True, ebene_darst=True)

    if von != nach:
        if von:
            return darst_1
        else:
            return darst_2

    else:
        return darst_1, darst_2


def input_nxm_mat(n=None, m=None, num=""):
    """Prompt für nxm Matrix"""
    err = cla.Input()
    while True:
        if n is None:
            n_for = "•"
        else:
            n_for = str(n)

        if m is None:
            m_for = "•"
        else:
            m_for = str(m)

        while err.error:
            print(f"Die {num} Matrix hat eine {n_for} × {m_for} Dimension")

            darst = std.user_input(err, random=True, matrix_nxm=True)

        if darst in ["r", "rr"]:
            n, m = random_auffüllen(["", ""], down_lim=1)
            return n, m

        if n is None:
            n = darst
            err.error = True

        elif m is None:
            m = darst
            return n, m

        else:
            return n, m


def user_input(err, string=False, ja=False, nein=False, max_amount=False, min_amount=1, erlaubte_werte=None, random=False,
               farben=False, matrix_nxm=False, ebene_darst=False):
    """Gibt dem User die Möglichkeit bestimmte Eingaben zu nutzen"""
    err_far = get_color("err")
    err.error = True

    if not isinstance(erlaubte_werte, (list, tuple)):
        erlaube_werte = [erlaubte_werte]

    try:
        inp = input("\n")
        out = inp.lower()
        cls()
        if erlaubte_werte is not None and inp in erlaubte_werte:
            err.error = False
            return inp

        if inp == "":
            if "" not in erlaubte_werte:
                err.error = True
                out = [True, "none"]
                error(out)
                return out
            else:
                err.error = False
                return inp

        if random:
            if out in ["random", "r"]:
                err.error = False
                out = "r"

            elif out in ["rr"]:
                err.error = False
                out = "rr"

        if err.error:
            if string:
                if ja or nein:
                    err.error = True
                    if ja:
                        if out in ["ja", "j"]:
                            out = True
                            err.error = False

                    if nein:
                        if out in ["nein", "n"]:
                            out = False
                            err.error = False

                    if err.error:
                        out = [True, ""]

                        if ja:
                            out[1] += "j"

                        if nein:
                            out[1] += "n"

                        error(out)

                elif farben:
                    err.error = True
                    colors = get_iter("farben_alle")
                    try:
                        inp = int(inp)
                        if inp in colors[2]:
                            err.error = False
                            out = inp, "Zahl"

                    except ValueError:
                        if inp.lower().capitalize() in colors[0]:
                            err.error = False
                            out = inp.lower().capitalize(), "Deutsch"

                        elif inp.lower() in colors[1]:
                            err.error = False
                            out = inp.lower(), "Englisch"

                elif ebene_darst:
                    err.error = True
                    try:
                        inp = int(inp)
                        if inp == 1:
                            err.error = False
                            out = "para"
                        elif inp == 2:
                            err.error = False
                            out = "norm"
                        elif inp == 3:
                            err.error = False
                            out = "koor"
                        else:
                            error([True, "ebene darst"])

                    except ValueError:
                        if inp.lower() in ["parameterform", "para", "p"]:
                            err.error = False
                            out = "para"

                        elif inp.lower() in ["normalenform", "norm", "n"]:
                            err.error = False
                            out = "norm"

                        elif inp.lower() in ["koordinatenform", "koor", "k"]:
                            err.error = False
                            out = "koor"

                        else:
                            error([True, "ebene darst"])


                else:
                    err.error = False
                    out = inp

            else:
                inp = inp.replace(",", ".")
                out = eval(inp)

                if max_amount is False and min_amount is False:
                    if isinstance(out, Number):
                        err.error = False
                        pass

                    else:
                        out = [True, "eval"]
                        err.error = True
                        error(out)

                else:
                    if isinstance(out, (int, float)):
                        if isinstance(out, float):
                            out = int(round(out, 0))

                        if erlaubte_werte is not None:
                            if out in erlaubte_werte:
                                err.error = False
                                pass

                        if err.error:
                            if min_amount is False:
                                if out <= max_amount:
                                    err.error = False

                                else:
                                    out = [True, "größer"]
                                    err.error = True
                                    error(out)

                            elif max_amount is False:
                                if min_amount <= out:
                                    err.error = False

                                else:
                                    if matrix_nxm:
                                        out = [True, "matrix kleiner"]
                                    else:
                                        out = [True, "kleiner"]

                                    err.error = True
                                    error(out)

                            elif isinstance(min_amount, int) and isinstance(max_amount, int):
                                if min_amount <= out <= max_amount:
                                    err.error = False
                                    pass

                                elif out > max_amount:
                                    out = [True, "größer"]
                                    err.error = True
                                    error(out)

                                elif out < min_amount:
                                    if matrix_nxm:
                                        out = [True, "matrix kleiner"]
                                    else:
                                        out = [True, "kleiner"]
                                    err.error = True
                                    error(out)

                    else:
                        out = [True, "eval"]
                        err.error = True
                        error(out)

    except ZeroDivisionError:
        out = [True, "null"]
        err.error = True
        error(out)

    except Exception:
        out = [True, "zahl"]
        err.error = True
        error(out)

    return out


def random_auffüllen(inp, up_lim=None, down_lim=None):
    """Füllt eine Liste inp mit zufälligen Werten auf"""
    i = 0
    if up_lim is None:
        global random_upper
    else:
        random_upper = up_lim

    if down_lim is None:
        global random_lower
    else:
        random_lower = down_lim

    for item in inp:
        if not isinstance(item, Number):
            inp[i] = random.randint(random_lower, random_upper)
        else:
            pass
        i += 1
    return inp


def buchstabe_auffüllen(inp, auff):
    if inp is None:
        inp = auff

    if not isinstance(inp, list):
        if isinstance(inp, str):
            inp = [inp]
        else:
            inp = list(inp)

    if not isinstance(auff, list):
        if isinstance(auff, str):
            auff = [auff]
        else:
            auff = list(auff)

    i = len(inp)
    while i < len(auff):
        inp.append(auff[i])
        i += 1

    return inp


def ber_setup(rechenweg, end, ende):
    prec_int = get_prec("int")
    if rechenweg or end:
        prec = std.get_prec(1)
        abs_far, zwi_far = get_color(["abs", "zwi"])
        if ende:
            end_far = get_color("end")
        else:
            end_far = get_color("zwi_end")

    else:
        prec, abs_far, zwi_far, end_far = None, None, None, None

    return prec, prec_int, abs_far, zwi_far, end_far


def error(inp):
    """Gibt einen Fehler wieder, je nachdem, was durch user_input*() für einen Wert gibt"""
    err_far = get_color("err")

    if inp[0]:
        print()
        if inp[1] == "none":
            cprint("Bitte überhaupt etwas eingeben!", err_far)

        elif inp[1] == "zahl":
            cprint("Bitte eine Zahl eingeben!", err_far)

        elif inp[1] == "null":
            cprint("Nicht durch 0 teilen!", err_far)

        elif inp[1] == "größer":
            cprint("Eine Zahl eingeben, die nicht größer ist als die maximale Anzahl!", err_far)

        elif inp[1] == "kleiner":
            cprint("Eine Zahl eingeben, die nicht kleiner ist als die minimale Anzahl!", err_far)

        elif inp[1] == "matrix kleiner":
            cprint("Eine Matrix kann keine kleinere Dimension als 1 haben!", err_far)

        elif inp[1] == "float":
            cprint("Keine Kommazahlen eingeben!", err_far)

        elif inp[1] == "j":
            cprint('Bitte nur "Ja" eingeben!', err_far)

        elif inp[1] == "n":
            cprint('Bitte nur "Nein" eingeben!', err_far)

        elif inp[1] == "jn":
            cprint('Bitte nur "Ja" oder "Nein" eingeben!', err_far)

        elif inp[1] == "eval":
            cprint("Keine anderen Datentypen / Ausdrücke angeben!", err_far)

        elif inp[1] == "ebene darst":
            cprint('Entweder eine Zahl von 1 bis 3 eingeben oder "Parameterform", "Normalenform" oder "Koordinatenform"')

        print()


def roman(n):
    roman_nums = [[1000, 'M'], [900, "CM"], [500, 'D'], [400, "CD"], [100, 'C'], [90, "XC"],
                  [50, 'L'], [40, "XL"], [10, 'X'], [9, "IX"], [5, 'V'], [4, "IV"], [1, 'I']]

    num = ""
    while n > 0:
        for i, [arabic, roman] in enumerate(roman_nums):
            if n - roman_nums[i][0] >= 0:
                n -= arabic
                num += roman
                break
    return num


def get_klam(dim_n=3, klammertyp="rund"):
    """Gibt die Bausteine einer runden Klammer zurück."""
    if klammertyp in ["r", "rund"]:
        klam = ["⎛", "⎜", "⎝"], ["⎞", "⎟", "⎠"]
    elif klammertyp in ["e", "eckig"]:
        klam = [["⎡", "⎢", "⎣"], ["⎤", "⎥", "⎦	"]]
    elif klammertyp in ["g", "geschwungen"]:
        klam = [["⎧", "⎨", "⎩", "⎪"], ["⎫", "⎬", "⎭", "⎪"]]

    out = [[], []]
    if klammertyp in ["r", "rund", "e", "eckig"]:
        if dim_n == 1:
            out = [["("], [")"]]

        else:
            for i in range(dim_n):
                for j in range(2):
                    if i == 0:
                        out[j].append(klam[j][0])

                    elif i == dim_n - 1:
                        out[j].append(klam[j][2])

                    else:
                        out[j].append(klam[j][1])
    else:
        if dim_n == 1:
            out = [["{"], ["}"]]

        elif dim_n == 2:
            out = [["⎰", "⎱"], ["⎱", "⎰"]]

        else:
            mitte = int(dim_n / 2)
            for i in range(dim_n):
                for j in range(2):
                    if i == 0:
                        out[j].append(klam[j][0])

                    elif i == dim_n - 1:
                        out[j].append(klam[j][2])

                    elif i == mitte:
                        out[j].append(klam[j][1])

                    else:
                        out[j].append(klam[j][3])
    return out


def get_pfeil(max_len):
    """Gibt einen Pfeil mit der Länge max_len zurück"""
    if max_len == 0:
        pfeil = ""

    elif max_len == 1:
        pfeil = "→"

    else:
        forma = f"─<{max_len - 1}"
        pfeil = f"{'':{forma}}" + "➤"

    return pfeil


def get_ausrichtung(ausrichtung):
    if ausrichtung == "links":
        ar = "<"
    elif ausrichtung == "mitte":
        ar = "^"
    elif ausrichtung == "rechts":
        ar = ">"
    return ar


def prec_auffüllen(prec, leng):
    prec_1 = get_prec(1)
    if type(prec) == int:
        prec = [prec for i in range(leng)]

    elif len(prec) <= leng:
        i = len(prec)
        while i < leng:
            prec.append(prec_1)
            i += 1

    if len(prec) > leng:
        i = len(prec)
        while i > leng:
            prec.pop()
            i -= 1
    return prec


def negcheck(neglist, string=False):
    """Gibt + oder - wieder, je nach Wert von neglist[i]"""
    if not isinstance(neglist, list):
        neglist = [neglist]
    negcheck = []
    i = 0
    while i < len(neglist):
        if type(neglist[i]) == str:
            if string:
                negcheck.append(" ")
            else:
                negcheck.append("+")
        elif neglist[i] < 0:
            negcheck.append("-")
        else:
            negcheck.append("+")
        i += 1

    return negcheck


def parser_maxlen(phlist, prec, mehrere, string=False, absval=False, klammer=False):
    """Parsed die maximale Länge der Werte von phlist."""
    if isinstance(phlist, Number):
        phlist = [phlist]

    elif isinstance(phlist, str):
        phlist = ["", phlist]

    max_len = 0
    for item in phlist:
        if type(item) == str:
            if string:
                if len(item) > max_len:
                    max_len = len(item)

        else:
            forma = f".{prec}f"
            if absval:
                b = f"{abs(item):{forma}}"

            else:
                if klammer and mehrere:
                    if item < 0:
                        b = f"({item:{forma}})"
                    else:
                        if all(item >= 0 if isinstance(item, Number) else 1 for item in phlist):
                            b = f"{item:{forma}}"
                        else:
                            b = f"{' ' * (3 - len(str(int(item))))}{item:{forma}} "

                else:
                    b = f"{item:{forma}}"

            if len(b) > max_len:
                max_len = len(b)

    return max_len


def format_prec(phlist, prec=2, mehrere=True, min_length=0, ausrichtung="rechts", string=False, klammer=False,
                klammertyp="rund", pfeil=False, pfeil_under=False, vorne=False, absval=False, gross_klam=False,
                string_ausrichtung=None, bruch=False, nur_pfeil=False, liste=False, dotted=False, dotted_len=False):
    """format_prec - Die Spacing Funktion. Diese Funktion gibt formattierten Input zurück.
    Dependencies:
        parser_maxlen
        get_ausrichtung
        get_klam
        get_divers
        get_pfeil

    """
    global forma_counter
    forma_counter += 1

    err_far = get_color("err")
    check = False

    if isinstance(phlist, Number):
        phlist = [phlist]
        check = True

    elif isinstance(phlist, str):
        if pfeil:
            phlist = ["", phlist]
        else:
            phlist = [phlist]
        check = True

    elif isinstance(phlist, dict):
        phlist = list(phlist.values())

    elif isinstance(phlist, (list, tuple)):
        pass

    elif isinstance(phlist[0], (list, tuple)):
        pass

    else:
        raise cla.InputError(colored(f"phlist ist nicht richtig: {phlist}", err_far))

    if check:
        if pfeil and not nur_pfeil:
            check = False

    if absval:
        phlist = [abs(item) if isinstance(item, Number) else item for item in phlist]
    if liste:
        check = False

    max_len = parser_maxlen(phlist, prec, mehrere, string, absval, klammer)

    if dotted_len is not False and isinstance(dotted_len, Number):
        max_len += dotted_len

    ar = get_ausrichtung(ausrichtung)
    if string_ausrichtung is None:
        str_ar = ar
    else:
        str_ar = get_ausrichtung(string_ausrichtung)

    anf_klam, end_klam = [""], [""]
    if klammer:
        if gross_klam:
            anf_klam, end_klam = get_klam(len(phlist), klammertyp)

    check_2 = False
    if vorne and ausrichtung == "links":
        for item in phlist:
            if item < 0:
                check_2 = True

    if check_2:
        vorne_space = " "
    else:
        vorne_space = ""

    ph = []
    i = 0
    n = 0

    if bruch:
        check_3 = True
        if mehrere:
            if len(phlist) % 2 == 0:
                while i < len(phlist):
                    max_len = parser_maxlen(phlist[i:i + 2], prec, mehrere, string, absval, klammer)
                    if dotted_len is not False and isinstance(dotted_len, Number):
                        max_len += dotted_len

                    if isinstance(phlist[i], str):
                        if string:
                            x_1 = f" {anf_klam[n]}{phlist[i]:{str_ar}{max_len}}{end_klam[n]} "

                        else:
                            x_1 = f" {anf_klam[n]}{phlist[i].strip():{str_ar}{max_len}}{end_klam[n]} "

                    else:
                        forma = f".{prec}f"
                        if round(phlist[i], 12) == 0:
                            phlist[i] = abs(phlist[i])

                        if phlist[i] < 0:
                            temp_space = ""
                        else:
                            temp_space = vorne_space

                        b = f"{phlist[i]:{forma}}"
                        x_1 = f" {anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]} "

                    if isinstance(phlist[i + 1], str):
                        if string:
                            x_2 = f" {anf_klam[n]}{phlist[i + 1]:{str_ar}{max_len}}{end_klam[n]} "

                        else:
                            x_2 = f" {anf_klam[n]}{phlist[i + 1].strip():{str_ar}{max_len}}{end_klam[n]} "

                    else:
                        forma = f".{prec}f"
                        if round(phlist[i + 1], 12) == 0:
                            phlist[i] = abs(phlist[i + 1])

                        if phlist[i + 1] < 0:
                            temp_space = ""
                        else:
                            temp_space = vorne_space

                        b = f"{phlist[i + 1]:{forma}}"
                        x_2 = f" {anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]} "

                    forma = f"─<{max(len(x_1) - 2, len(x_2) - 2)}"
                    x_3 = f"╶{'':{forma}}╴"

                    if nur_pfeil:
                        ph.append(x_3)

                    else:
                        ph.append(x_1)
                        ph.append(x_3)
                        ph.append(x_2)

                    i += 2

        else:
            mitte = int(len(phlist) / 2)

            while i < len(phlist):
                if i == mitte and check_3:
                    forma = f"─<{max_len}"
                    x = f"╶{'':{forma}}╴"
                    check_3 = False

                else:
                    if isinstance(phlist[i], str):
                        if string:
                            x = f" {anf_klam[n]}{phlist[i]:{str_ar}{max_len}}{end_klam[n]} "

                        else:
                            x = f" {anf_klam[n]}{phlist[i].strip():{str_ar}{max_len}}{end_klam[n]} "

                    else:
                        forma = f".{prec}f"
                        if phlist[i] < 0:
                            temp_space = ""
                        else:
                            temp_space = vorne_space

                        b = f"{phlist[i]:{forma}}"
                        x = f" {anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]} "

                    i += 1

                ph.append(x)

        if get_divers("komma"):
            for i in range(len(ph)):
                ph[i] = ph[i].replace(".", ",")

        return ph

    while i < len(phlist):
        if not mehrere:
            max_len = parser_maxlen(phlist[i], prec, mehrere, string, absval, klammer)

        if type(phlist[i]) == str:
            if pfeil and phlist[i].strip():
                pfeil = get_pfeil(max_len)

                if nur_pfeil:
                    if liste:
                        pfeil = [pfeil]
                    return pfeil

                elif pfeil_under:
                    try:
                        ph[i] = phlist[i]
                    except IndexError:
                        ph.append(phlist[i])
                    try:
                        ph[i + 1] = pfeil
                    except IndexError:
                        ph.append(pfeil)
                    i += 1
                    continue

                else:
                    if i == 0:
                        ph.insert(0, pfeil)
                    else:
                        ph[i - 1] = pfeil

            if dotted:
                x = f"{anf_klam[n]}{phlist[i]:{str_ar}}{end_klam[n]}"
                j = len(x)
                if j % 2 == 0:
                    x += " "
                else:
                    x += "  "

                j = len(x)

                while j < max_len:
                    if j == max_len - 1:
                        x += " "
                    elif j % 2 == 0:
                        x += " "

                    else:
                        x += "."

                    j += 1

            elif string:
                x = f"{anf_klam[n]}{phlist[i]:{str_ar}{max_len}}{end_klam[n]}"

            else:
                x = f"{anf_klam[n]}{phlist[i].strip():{str_ar}{max_len}}{end_klam[n]}"

        else:
            if round(phlist[i], 12) == 0:
                phlist[i] = abs(phlist[i])

            forma = f".{prec}f"
            b = f"{phlist[i]:{forma}}"

            if klammer and not gross_klam:
                if phlist[i] < 0:
                    b = f"({phlist[i]:{forma}})"

                elif mehrere:
                    if all(item >= 0 if isinstance(item, Number) else 1 for item in phlist):
                        b = f"{phlist[i]:{forma}}"
                    else:
                        b = f"{' ' * (3 - len(str(int(phlist[i]))))}{phlist[i]:{forma}} "

                else:
                    b = f"{phlist[i]:{forma}}"

            if phlist[i] < 0:
                temp_space = ""

            else:
                temp_space = vorne_space
            x = f"{anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]}"

        ph.append(x)
        i += 1
        if klammer and gross_klam:
            n += 1

    if get_divers("komma") and not dotted:
        for i in range(len(ph)):
            ph[i] = ph[i].replace(".", ",")

    if check:
        return ph[0]

    return ph
