import random
import time

import StandardLib as std
import Standardoperationen as stdop
import classes as cla
from Colored import cprint




def main():
    config = std.load_config()
    prec_1 = config["Nachkommastellen 1"]
    prec_2 = config["Nachkommastellen 2"]
    prec_3 = config["Nachkommastellen 3"]
    prec_parser = config["Nachkommastellen Parser"]
    prec_int = config["Nachkommastellen Intern"]

    zwi_far, zwi_zwi_far, end_far, abs_far, men_far, err_far, ein_far = std.get_color(value=False)
    err = cla.Input()

    while err.error:
        cprint("Willkommen bei dem Analytischen Geometrie-Rechner von Mattis Seebeck.\n", men_far.en)
        cprint("Welche Funktionalität möchtest du benutzen?", men_far.en)
        cprint("Zur Auswahl steht:\n", men_far.en)
        cprint("0: Standardeinsetellungen ändern", men_far.en)
        cprint("1: Standard Operationen ohne Rechenweg", men_far.en)
        cprint("2: Standard Operationen mit  Rechenweg", men_far.en)
        cprint("3: Lineare Algebra ohne Rechenweg", men_far.en)
        cprint("4: Lineare Algebra mit  Rechenweg", men_far.en)

        func = std.user_input(err, max_amount=4, min_amount=0)

    err.error = True
    darst = None
    if func == 0:
        while True:
            err.error = True
            while err.error:
                cprint("Veränderbare Einstellungen:\n", men_far.en)
                cprint("0: Standards wiederherstellen", men_far.en)
                cprint("1: Farben verändern", men_far.en)
                cprint("2: Anzahl der Nachkommastellen verändern", men_far.en)
                cprint("3: Variablen verändern", men_far.en)
                cprint("4: Diverses", men_far.en)
                cprint("5: Rechen- und Lösungswege", men_far.en)

                einst = std.user_input(err, max_amount=5, min_amount=0)

            err.error = True
            standards = False

            if einst == 0:
                standards = True
                std.save_config_standard()

            elif einst == 1:
                while err.error:
                    for i, (color, item) in enumerate(zip(std.get_color(value=False), std.format_prec(std.get_iter("config_farben_darst"), string=True, ausrichtung="links", dotted=True, dotted_len=2)), start=1):
                        cprint(f"{i}: {item}", men_far.en, end="")
                        cprint(color.de, color.en)
                        print()

                    einst = std.user_input(err, max_amount=7)

                err.error = True
                while err.error:
                    cprint("Welche Farbe möchtest du wählen?\n")
                    std.display_farben()

                    far, darst = std.user_input(err, string=True, farben=True)

                neu_far = cla.Farbe(far, darst)

                for i, item in enumerate(std.get_iter("config_farben"), start=1):
                    if einst == i:
                        std.save_config(item, neu_far.de)
                        break

            elif einst == 2:
                while err.error:
                    for i, (prec, item) in enumerate(zip(std.get_prec(), std.format_prec(std.get_iter("config_prec_darst"), string=True, ausrichtung="links", dotted=True, dotted_len=4)), start=1):
                        cprint(f"{i}: {item}{prec}", men_far.en)
                        print()

                    einst = std.user_input(err, max_amount=5)

                err.error = True
                while err.error:
                    if einst == 5:
                        cprint("Mit wie vielen Nachkommastellen soll gerechnet werden?", men_far.en)

                    else:
                        cprint("Wie viele Nachkommastellen sollen angezeigt werden? Maximal 15", men_far.en)

                    prec = std.user_input(err, max_amount=15)

                for i, item in enumerate(std.get_iter("config_prec")):
                    if einst == i:
                        std.save_config(item, prec)
                        break

            elif einst == 3:
                while err.error:
                    for i, (conf, item) in enumerate(zip(std.get_iter("config_buchst"), std.format_prec(std.get_iter("config_buchst_darst"), string=True, ausrichtung="links", dotted=True, dotted_len=4)), start=1):
                        pass
                    for i, (conf, item) in enumerate(zip(std.get_iter("config_buchst"), std.format_prec(std.get_iter("config_buchst_darst"), string=True, ausrichtung="links", dotted=True, dotted_len=4)), start=1):
                        if isinstance(config[conf], list):
                            cprint(f"    {' ' * len(item)}{config[conf][0]}", men_far.en)
                            cprint(f"{i:<2}: {item}{config[conf][1]}", men_far.en)
                            print()

                        else:
                            cprint(f"{i:<2}: {item}{config[conf]}", men_far.en)
                            print()

                    einst = std.user_input(err, max_amount=19)

                err.error = True
                pfeil = False
                while err.error:
                    cprint('Tipp: Wenn du "pfeil" in die Eingabe schreibst, wird der Buchstabe mit pfeil angezeigt\n', men_far.en)
                    cprint("Was für ein Buchstabe soll zugewiesen werden?")

                    buchst = std.user_input(err, string=True)
                    if buchst == "pfeil":
                        pfeil = True
                        err.error = True

                buchst = std.format_prec(buchst, ausrichtung="links", string=True, pfeil=pfeil)

                for i, item in enumerate(std.get_iter("config_buchst"), start=1):
                    if einst == i:
                        std.save_config(item, buchst)
                        break

            elif einst == 4:
                while err.error:
                    for i, (conf, item) in enumerate(zip(std.get_iter("config_divers"), std.format_prec(std.get_iter("config_divers_darst"), string=True, ausrichtung="links", dotted=True, dotted_len=4)), start=1):
                        if isinstance(config[conf], bool):
                            if config[conf]:
                                conf = "Ja"
                            else:
                                conf = "Nein"
                        else:
                            conf = config[conf]
                        cprint(f"{i}: {item}{conf}", men_far.en)
                        print()

                    einst = std.user_input(err, max_amount=i)

                err.error = True
                while err.error:
                    cprint("Ja oder Nein?", men_far.en)

                    wert = std.user_input(err, string=True, ja=True, nein=True)

                if einst == 1:
                    std.save_config("Bruch", wert)

                elif einst == 2:
                    std.save_config("Komma", wert)

                elif einst == 3:
                    std.save_config("Gauss Pretty", wert)

                elif einst == 4:
                    std.save_config("Gauss Fast", wert)

            elif einst == 5:
                while err.error:
                    for i, (conf, item) in enumerate(zip(std.get_iter("config_lösung"), std.format_prec(std.get_iter("config_lösung_darst"), string=True, ausrichtung="links", dotted=True, dotted_len=4)), start=1):
                        if isinstance(config[conf], bool):
                            if config[conf]:
                                conf = "Ja"
                            else:
                                conf = "Nein"
                        else:
                            conf = config[conf]
                        cprint(f"{f' {i}' if i < 10 else i}: {item}{conf}", men_far.en)
                        print()

                    einst = std.user_input(err, max_amount=i)

                err.error = True

                if 1 <= einst <= 10:
                    while err.error:
                        cprint(f"Soll ein {std.get_iter('config_lösung_darst')[einst - 1]} angezeigt werden?", men_far.en)

                        wert = std.user_input(err, ja=True, nein=True, string=True)

                elif 11 <= einst <= 13:
                    while err.error:
                        cprint(f"Welcher {std.get_iter('config_lösung_darst')[einst - 1]} soll gewählt werden?\n", men_far.en)
                        cprint("1: Lineares Gleichungsystem", men_far.en)
                        cprint("2: Einsetzen in die Koordinatenform", men_far.en)
                        if einst > 11:
                            cprint("3: Passend")

                        wert = std.user_input(err, max_amount=3 if einst > 11 else 2, erlaubte_werte=["lgs", "koor", "passend"])

                    if wert == 1:
                        wert = "lgs"
                    elif wert == 2:
                        wert = "koor"
                    elif wert == 3:
                        wert = "passend"

                elif 14 <= einst <= 19:
                    lsg = []
                    if einst in [14, 16]:
                        lsg = ["hilf", "geo"]
                    else:
                        lsg = ["hnf", "lfp"]
                    while err.error:
                        cprint(f"Welcher {std.get_iter('config_lösung_darst')[einst - 1]} soll gewählt werden?\n", men_far.en)
                        for i, item in enumerate(lsg, start=1):
                            if item == "lfp":
                                cprint(f"{i}: Lotfußpunkt", men_far.en)
                            elif item == "hnf":
                                cprint(f"{i}: Hessesche Normalenform", men_far.en)
                            elif item == "hilf":
                                cprint(f"{i}: Hilfsebene", men_far.en)
                            elif item == "geo":
                                cprint(f"{i}: Geometrischer Ansatz", men_far.en)

                        wert = std.user_input(err, max_amount=i, erlaubte_werte=lsg)

                    wert = lsg[wert - 1]

                for i, item in enumerate(std.get_iter("config_lösung"), start=1):
                    if einst == i:
                        std.save_config(item, wert)
                        break

            config = std.load_config()
            prec_1 = config["Nachkommastellen 1"]
            prec_2 = config["Nachkommastellen 2"]
            prec_3 = config["Nachkommastellen 3"]
            prec_parser = config["Nachkommastellen Parser"]
            prec_int = config["Nachkommastellen Intern"]

            zwi_far, zwi_zwi_far, end_far, abs_far, men_far, err_far, ein_far = std.get_color(value=False)
            std.cls()

            if standards:
                cprint("Standards erfolgreich wiederhergestellt!", men_far.en)
            else:
                cprint("Einstellung erfolgreich verändert!", men_far.en)

            cprint("\nMöchtest du noch etwas verändern?", men_far.en)
            err.error = True
            back = std.user_input(err, string=True, ja=True, nein=True, random=True, erlaubte_werte="")
            if back == "r":
                if random.randint(0, 1):
                    return

            elif not back:
                return

    elif func in [1, 2]:
        if func == 1:
            rweg = "Ohne"
            rechenweg = False
        else:
            rweg = "Mit"
            rechenweg = "force"

        while err.error:
            cprint(f"Welche Operation möchtest du benutzen ({rweg} Rechenweg)?\n", men_far.en)
            cprint("1:  Vektor aus zwei Punkten berechnen", men_far.en)
            cprint("2:  Gerade aus zwei Punkten berechnen", men_far.en)
            cprint("3:  Ebene aus drei Punkten berechnen", men_far.en)
            cprint("4:  Betrag eines Vektors berechnen", men_far.en)
            cprint("5:  Normalenvektor berechnen", men_far.en)
            cprint("6:  Normaleneinheitsvektor berechnen", men_far.en)
            cprint("7:  Skalarprodukt berechnen", men_far.en)
            cprint("8:  Lineare Abhängigkeit testen", men_far.en)
            cprint("9:  Punktprobe von Punkt und Gerade", men_far.en)
            cprint("10: Punktprobe von Punkt Ebene", men_far.en)
            cprint("11: Schnittpunkt zweier Geraden berechnen", men_far.en)
            cprint("12: Schnittpunkt von Gerade und Ebene berechnen", men_far.en)
            cprint("13: Schnittgerade zweier Ebenen berechnen", men_far.en)
            cprint("14: Schnittwinkel zweier Geraden berechnen", men_far.en)
            cprint("15: Schnittwinkel von Gerade und Ebene berechnen", men_far.en)
            cprint("16: Schnittwinkel zweier Ebenen berechnen", men_far.en)
            cprint("17: Umrechnung zwischen Ebenengleichungen", men_far.en)
            cprint("18: Sind die eingegebenen Ebenen gleich?", men_far.en)
            cprint("19: Abstand zwischen Punkt und Gerade berechnen", men_far.en)
            cprint("20: Abstand zwischen zwei Geraden berechnen", men_far.en)
            cprint("21: Abstand zwischen Punkt und Ebene berechnen", men_far.en)
            cprint("22: Abstand zwischen Gerade und Ebene berechnen", men_far.en)
            cprint("23: Abstand zwischen Ebene und Ebene berechnen", men_far.en)
            operation = std.user_input(err, max_amount=23)

        if operation in [1, 2]:
            P = std.parser("punkt")
            Q = std.parser("punkt", buchst="Q", weitere=P)
            parsed = [P, Q]

        elif operation == 3:
            P = std.parser("punkt")
            Q = std.parser("punkt", buchst="Q", weitere=P)
            T = std.parser("punkt", buchst="T", weitere=(P, Q))
            parsed = [P, Q, T]

        elif operation == 4:
            parsed = [std.parser("vektor")]

        elif operation in [5, 6, 7]:
            u = std.parser("vektor", buchst="u")
            v = std.parser("vektor", weitere=u)
            parsed = [u, v]

        elif operation == 8:
            parsed = std.parser("linear abhängig")

        elif operation in [9, 19]:
            P = std.parser("punkt")
            g = std.parser("gerade", weitere=P)
            parsed = [P, g]

        elif operation in [10, 21]:
            darst = std.input_darst_ebene()
            P = std.parser("punkt")
            E = std.parser("ebene", darst=darst, weitere=P)
            parsed = [P, E]

        elif operation in [11, 14, 20]:
            g = std.parser("gerade")
            h = std.parser("gerade", buchst="h", weitere=g, param="s")
            parsed = [g, h]

        elif operation in [12, 15, 22]:
            darst = std.input_darst_ebene()
            g = std.parser("gerade")
            E = std.parser("ebene", darst=darst, weitere=g)
            parsed = [g, E]

        elif operation in [13, 16, 18, 23]:
            darst = std.input_darst_ebene(erste=True, zweite=True)
            E = std.parser("ebene", darst=darst[0])
            F = std.parser("ebene", darst=darst[1], buchst="F", weitere=E, param=["u", "v"])
            parsed = [E, F]

        elif operation == 17:
            darst = std.input_umrechnen(von=True, nach=True)
            E = std.parser("ebene", darst=darst[0])
            parsed = [E]

        stdop.standardoperationen(parsed, operation, rechenweg, darst)

    elif func in [3, 4]:
        if func == 3:
            Rweg = "Ohne"
            rechenweg = False

        else:
            Rweg = "Mit"
            rechenweg = "force"

        while err.error:
            cprint(f"Welche Operation möchtest du benutzen ({Rweg} Rechenweg)?\n", men_far.en)
            for i, item in enumerate(std.get_iter("operation_lagl_darst"), start=1):
                cprint(f"{i}: {item}", men_far.en)

            operation = std.user_input(err, max_amount=i)

        A, B = None, None
        if operation == 1:
            darst = std.input_nxm_mat(num="erste"), std.input_nxm_mat(num="zweite")
            A = std.parser("matrix", darst[0], True)
            std.cls()
            B = std.parser("matrix", darst[1], True, buchst="B", weitere=A)

        elif operation == 2:
            darst = std.input_nxm_mat()
            cprint(f"Die Matrix hat eine {darst[0]} × {darst[1]} Dimension", men_far.en)
            A = std.parser("matrix", darst, True, param=True)

        s = time.time()
        stdop.standardoperationen_lagl([A, B], operation, rechenweg, darst)

    return True


if __name__ == "__main__":
    std.cls()
    menu_far = std.get_color("men")

    y = True

    error = cla.Input()
    while y:
        x = main()
        if x:
            cprint("\n", menu_far)
            cprint("Nochmal?", menu_far)
            error.error = True
            y = std.user_input(error, string=True, ja=True, nein=True, erlaubte_werte="")
            if y is "":
                y = True
        std.cls()
