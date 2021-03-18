import copy
from numbers import Number

import AnalytischeGeometrie.Berechnungen as ber
import AnalytischeGeometrie.Display as dis
import AnalytischeGeometrie.StandardLib as std
from AnalytischeGeometrie.Colored import colored
from AnalytischeGeometrie.Colored import cprint


# Errors
class Error(Exception):
    """Base Class für Ausnahmen."""
    pass


class InputError(Error):
    """Es gab einen Error beim Input."""

    pass


class InputError2(Error):
    """Es gab einen Error beim Input."""


class Input:
    """Class für Input."""

    def __init__(self):
        self.error = True


class Farbe:
    """Class für Farben."""

    def __init__(self, wert, sprache):
        """

        Parameters
        ----------
        wert        Was für eine Farbe
        sprache     In welcher Sprache die Farbe angegeben ist
        """
        err_far = "red"
        if sprache not in ["Deutsch", "Englisch", "Zahl"]:
            raise InputError(colored(f"Sprache ist nicht richtig: {sprache}", err_far))

        if wert not in ["Grau", "Rot", "Grün", "Gelb", "Blau", "Violett", "Cyan", "Weiß",
                        "grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"] + list(range(1, 8)):
            raise InputError(colored(f"Wert ist nicht richtig: {wert, type(wert)}", err_far))

        self.de = None
        self.en = None
        self.za = None

        if sprache == "Deutsch":
            if wert == "Rot":
                self.färben("red")

            elif wert == "Grün":
                self.färben("green")

            elif wert == "Gelb":
                self.färben("yellow")

            elif wert == "Blau":
                self.färben("blue")

            elif wert == "Violett":
                self.färben("magenta")

            elif wert == "Cyan":
                self.färben("cyan")

            elif wert == "Weiß":
                self.färben("white")

        elif sprache == "Englisch":
            if wert == "red":
                self.färben("red")

            elif wert == "green":
                self.färben("green")

            elif wert == "yellow":
                self.färben("yellow")

            elif wert == "blue":
                self.färben("blue")

            elif wert == "magenta":
                self.färben("magenta")

            elif wert == "cyan":
                self.färben("cyan")

            elif wert == "white":
                self.färben("white")

        elif sprache == "Zahl":
            if wert == 1:
                self.färben("red")

            elif wert == 2:
                self.färben("green")

            elif wert == 3:
                self.färben("yellow")

            elif wert == 4:
                self.färben("blue")

            elif wert == 5:
                self.färben("magenta")

            elif wert == 6:
                self.färben("cyan")

            elif wert == 7:
                self.färben("white")

    def färben(self, farbe):
        """farbe in farbe_en."""
        err_far = "red"
        if not isinstance(farbe, str):
            raise InputError(colored(f"farbe ist kein str: {farbe}", err_far))

        if farbe not in ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]:
            raise InputError(colored(f"farbe ist nicht in farbe_en: {farbe}", err_far))

        elif farbe == "red":
            self.de = "Rot"
            self.en = "red"
            self.za = 1

        elif farbe == "green":
            self.de = "Grün"
            self.en = "green"
            self.za = 2

        elif farbe == "yellow":
            self.de = "Gelb"
            self.en = "yellow"
            self.za = 3

        elif farbe == "blue":
            self.de = "Blau"
            self.en = "blue"
            self.za = 4

        elif farbe == "magenta":
            self.de = "Violett"
            self.en = "magenta"
            self.za = 5

        elif farbe == "cyan":
            self.de = "Cyan"
            self.en = "cyan"
            self.za = 6

        elif farbe == "white":
            self.de = "Weiß"
            self.en = "white"
            self.za = 7

import time

class Matrix:
    """
    Class für Matritzen.
    """

    def __init__(self, A, b=None, zeilen=True, A_buchst="A", b_buchst="b"):
        """
        Parameters
        ----------
        A           Matrix in [[...], [...], ...] form - Falls nur eine Zahl / nur eine Liste gegeben ist wird sie aufgefüllt
        b           Für die EKM - als normale list
        zeilen      Soll der Input als Zeile in den [] interpretiert werden (True) oder nicht (False)
        A_buchst    Der Buchstabe von der Matrix
        b_buchst    Der Buchstabe von b
        """
        std.verify_input(A, A_buchst, "matrix")
        self.A_buchst = A_buchst
        if isinstance(A, (Number, str)):
            self.A = [[A]]

        elif isinstance(A, list):
            if all(isinstance(item, (Number, str)) for item in A):
                self.A = [A]

            else:
                std.verify_input(A, A_buchst, "list matrix")

                self.A = A

        if b is None:
            self.has_b = False

        else:
            if isinstance(b, (Number, str)):
                self.b = [b]

            else:
                all(std.verify_input(item, b_buchst, (str, Number)) for item in b)
                self.b = b
                self.b_buchst = b_buchst
                if isinstance(b[0], Number):
                    self.dim_b = 1
                else:
                    self.dim_b = len(b)
                self.has_b = True

        self.dim_m = len(self.A)
        self.dim_n = len(self.A[0])

        if zeilen is False:
            self.transp()
            self.dim_n, self.dim_m = self.dim_m, self.dim_n

    def swap(self, zeile_1, zeile_2):
        self.A[zeile_1], self.A[zeile_2] = self.A[zeile_2], self.A[zeile_1]
        if self.has_b:
            self.b[zeile_1], self.b[zeile_2] = self.b[zeile_2], self.b[zeile_1]

    def transp(self):
        """
        Transponiert die Matrix
        Parameters
        ----------
        ändern  Soll der zeilen Wert auch geändert werden

        Returns
        -------
        None
        """
        self.A = [[self.A[j][i] for j in range(self.dim_m)] for i in range(self.dim_n)]

    def find_non_0(self, zeile=False, sarr_start=False, sarr_end=False, b=False):
        """
        Findet den Eintrag in der Matrix / Zeile der als erstes nicht Null ist
        Parameters
        ----------
        zeile       Soll eine bestimmte Zeile untersucht werden
        sarr_start  Wenn eine Zahl dann sucht nur in dem Subarray ab sarr_start
        sarr_end    Wenn eine Zahl dann sucht nur in dem Subarray bis sarr_end
        b           Ob das b der Matrix auch mitbetrachtet werden soll

        Returns
        -------
        Number (Zeile) oder False
        """

        if std.gauss_fast:
            err_far = "red"
            prec_int = 10
        else:
            err_far = std.get_color("err")
            prec_int = std.get_prec("int")
            all(std.verify_input(item, str(item), (bool, Number)) for item in [zeile, sarr_start, sarr_end])
            std.verify_input(b, "b", bool)
            if zeile is True:
                raise InputError(colored(f"zeile ist True: {zeile}", err_far))

            if sarr_start is True:
                raise InputError(colored(f"Subarray start ist True: {sarr_start}", err_far))

            if sarr_end is True:
                raise InputError(colored(f"Subarray end ist True: {sarr_end}", err_far))

            if zeile and (sarr_start or sarr_end):
                raise InputError(colored(f"zeile und subarray sind True: zeile: {zeile}, subarray start: {sarr_start}, subarray end: {sarr_end}", err_far))

            if b is True and self.has_b is False:
                raise InputError(colored(f"Die Matrix {self.A_buchst} hat kein b", err_far))

        bis = self.dim_m
        if sarr_end is not False and sarr_end < self.dim_m:
            bis = sarr_end

        if zeile is False:
            for j in range(self.dim_n):
                for i in range(sarr_start, bis):
                    if (b and self.has_b and round(self.b[i], prec_int)) or round(self.A[i][j], prec_int):
                        return i

            return False

        else:
            for i, item in enumerate(self.A[zeile] + [self.b[zeile] if b else 0]):
                if round(item, prec_int):
                    return i

            return False


    def pos_KV(self):
        """
        Findet die Spalten der vorhandenen Kopfvariablen in der Matrix
        Returns
        -------
        Positionen der Kopfvariablen - list.
        """
        pos_KV = []

        for i in range(self.dim_m):
            n = self.find_non_0(zeile=i)

            if n is not False and n not in pos_KV:
                pos_KV.append(n)

        return pos_KV

    def pos_NKV(self):
        """
        Findet die Spalten der vorhanden Nichtkopfvariablen in der Matrix
        Returns
        -------
        Positionen der Nichtkopfvariablen - list
        """
        pos_KV = self.pos_KV()
        pos_NKV = [i for i in range(self.dim_n) if i not in pos_KV]
        return pos_NKV

    def __matmul__(self, A):
        return ber.matmul(self, A)

    def display(self, prec=3, color=None, print_=True, pfeil=False, overset=None, nur_pfeil=False, min_len_pfeil=None):
        """

        Parameters
        ----------
        prec            Anzahl der Nachkommastellen - int
        color           In welcher Farbe die Matrix dargestellt werden soll
        print_          Soll geprinted werden
        pfeil           Soll ein Pfeil am Anfang angezeigt werden - gebalanced auf overset / min 3
        overset         Was über dem Pfeil stehen soll
        nur_pfeil       Soll nur der Pfeil returned werden
        min_len_pfeil   Soll der Pfeil eine minimale Länge haben

        Returns
        -------
        Liste von geprinteter Matrix
        """
        klam = std.get_klam(self.dim_m)
        out = []
        mitte = int(self.dim_m / 2)

        if pfeil is False:
            buchst_darst = ["" for _ in range(self.dim_m)]
            if self.has_b:
                buchst_darst[mitte] += "["

            if isinstance(self.A_buchst, list):
                if self.has_b:
                    buchst_darst[mitte - 1] += " "
                buchst_darst[mitte - 1] += self.A_buchst[0]
                buchst_darst[mitte] += self.A_buchst[1]
            else:
                buchst_darst[mitte] += self.A_buchst

            buchst_darst = std.format_prec(buchst_darst, string=True, ausrichtung="links", min_length=5)

            if self.has_b:
                if isinstance(self.b_buchst, list):
                    buchst_darst[mitte - 1] += f" {self.b_buchst[0]}"
                    buchst_darst[mitte] += f"|{self.b_buchst[1]}"
                else:
                    buchst_darst[mitte] += f"|{self.b_buchst}]"

            buchst_darst[mitte] += " = "
            buchst_darst = std.format_prec(buchst_darst, string=True, ausrichtung="links")

        else:
            if overset is None:
                pfeil = std.get_pfeil(3 if min_len_pfeil is None else min_len_pfeil)
                buchst_darst = ["" if i != mitte else pfeil for i in range(self.dim_m)]
                buchst_darst = std.format_prec(buchst_darst, string=True, ausrichtung="links")

            else:
                if isinstance(overset, (list, tuple)):
                    leng = len(overset[0])
                else:
                    leng = len(overset)
                if min_len_pfeil:
                    len_pfeil = max(min_len_pfeil, leng + 2)
                else:
                    len_pfeil = leng + 2

                pfeil = std.get_pfeil(len_pfeil)

                if isinstance(overset, list):
                    overset.append(pfeil)
                    for _ in range(mitte - len(overset) + 1):
                        overset.insert(0, "")
                    buchst_darst = std.format_prec(overset, string=True, ausrichtung="mitte")

                else:
                    buchst_darst = std.format_prec([overset, pfeil], string=True, ausrichtung="mitte")

            buchst_darst = [f"{item}  " for item in buchst_darst]

        if self.has_b:
            b_darst = std.format_prec(self.b, prec, string=True)

        A_darst = [std.format_prec([self.A[j][i] for j in range(len(self.A))], prec, ausrichtung="rechts", string=True, string_ausrichtung="mitte") for i in range(len(self.A[0]))]

        if isinstance(buchst_darst, (list, tuple)) and len(buchst_darst) > self.dim_m:
            for i in range(len(buchst_darst) - self.dim_m):
                out.append(f"{buchst_darst[i]}")

            buchst_darst = buchst_darst[len(buchst_darst) - self.dim_m:]

        if isinstance(buchst_darst, (list, tuple)) and len(buchst_darst) < self.dim_m:
            for i in range(self.dim_m - len(buchst_darst)):
                buchst_darst.append(" " * len(buchst_darst[0]))

        for i in range(self.dim_m):
            out_string = ""
            out_string += f"{buchst_darst[i]}{klam[0][i]}{A_darst[0][i]}"
            for j in range(1, self.dim_n):
                out_string += f"  {A_darst[j][i]}"

            if self.has_b:
                out_string += f" │ {b_darst[i]}"

            out_string += f"{klam[1][i]}"

            out.append(out_string)

        if print_:
            for item in out:
                cprint(item, color)

        if nur_pfeil and pfeil:
            return pfeil

        return out

if __name__ == '__main__':
    A = Matrix([[0.36840362789339853], [0.5106520737259224]], b=[0.6774765732353941, 0.31861152315818386])
    A.find_non_0()

class Ebene:
    """Class für eine Ebene."""

    def __init__(self, inp, param=None, buchst="E", pfeil=False):
        """

        Parameters
        ----------
        inp     Der Input - entweder parameterform: [[_, _, _,], [_, _, _,], [_, _, _,]] / normalenform: [[_, _, _,], [_, _, _,]] / koordinatenform: [_, _, _, _]
        param   Die Parameter für die Ebene
        buchst  Der Buchstabe für die Ebene
        pfeil   Ob der Buchstabe ein Pfeil haben soll
        """
        if param is None:
            param = ["s", "t"]
        std.verify_input(inp, buchst, "ebene"), all(std.verify_input(item, "Parameter", str) for item in param)
        std.verify_input(buchst, "Buchstabe", str), std.verify_input(pfeil, "Pfeil", bool)

        self.param = param
        self.buchst = buchst
        self.has_pfeil = pfeil
        self.dim = 3
        if pfeil:
            self.pfeil = std.format_prec(buchst, string=True, pfeil=True, nur_pfeil=True)
        else:
            self.pfeil = " " * len(buchst)

        if isinstance(inp[0], list):
            if len(inp) == 2:
                self.darst = "norm"
                self.sv = inp[0]
                self.nv = inp[1]

                if not any(isinstance(item, str) for row in inp for item in row):
                    self.umrechnen("norm", "koor")
                    self.umrechnen("norm", "para")

            else:
                self.darst = "para"
                self.sv = inp[0]
                self.rv_1 = inp[1]
                self.rv_2 = inp[2]

                if not any(isinstance(item, str) for row in inp for item in row):
                    self.umrechnen("para", "norm")
                    self.umrechnen("para", "koor")

        else:
            self.darst = "koor"
            self.kv = inp
            if not any(isinstance(item, str) for item in inp):
                self.umrechnen("koor", "para", sv_berechnen=True)
                self.umrechnen("koor", "norm")

    def umrechnen(self, von, nach, rechenweg=False, intro=False, end=False, ende=False, sv_berechnen=False):
        """
        Umrechnen der Ebene von einer bestimmten Form in die andere
        Parameters
        ----------
        von             Darstellungsform von der Umgerechnet werden soll
        nach            Darstellungsform nach der Umgerechnet werden soll
        rechenweg       Soll ein Rechenweg angezeigt werden
        intro           Soll ein Intro angezeigt werden
        end             Soll ein Ende angezeigt werden
        ende            Soll das Ende als Ende von allem behandelt werden
        sv_berechnen    Soll für norm -> para der Stützvektor neu berechnet werden

        Returns
        -------
        None
        """
        err_far = std.get_color("err")
        std.verify_input(von, "von", "ebene darst"), std.verify_input(nach, "nach", "ebene darst")
        prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)
        prec_int = std.get_prec("int")
        if rechenweg != "force" and rechenweg is not False:
            rechenweg = std.get_lsg("rweg umrechnung")

        if von == nach:
            raise InputError(colored(f"Von und Nach sind gleich: {von}, {nach}", err_far))

        if von == "para":
            if nach == "norm":
                self.nv = ber.conv_norm(self.rv_1, self.rv_2, return_list=True)

            elif nach == "koor":
                self.umrechnen("para", "norm")
                self.umrechnen("norm", "koor")

        elif von == "norm":
            if nach == "para":
                self.umrechnen("norm", "koor")
                self.umrechnen("koor", "para")

            elif nach == "koor":
                self.kv = self.nv + [sum(self.nv[i] * self.sv[i] for i in range(3))]

        elif von == "koor":
            if nach == "para":
                if round(self.kv[2], prec_int) != 0:
                    self.rv_1 = [1, 0, -self.kv[0] / self.kv[2]]
                    self.rv_2 = [0, 1, -self.kv[1] / self.kv[2]]
                    if sv_berechnen:
                        self.sv = [0, 0, self.kv[3] / self.kv[2]]

                elif round(self.kv[1], prec_int) != 0:
                    self.rv_1 = [1, -self.kv[0] / self.kv[1], 0]
                    self.rv_2 = [0, 0, 1]
                    if sv_berechnen:
                        self.sv = [0, self.kv[3] / self.kv[1], 0]

                elif round(self.kv[0], prec_int) != 0:
                    self.rv_1 = [0, 1, 0]
                    self.rv_2 = [0, 0, 1]
                    if sv_berechnen:
                        self.sv = [self.kv[3] / self.kv[0], 0, 0]

                else:
                    raise InputError(colored("Der Koordinatenvektor ist [0, 0, 0]", err_far))

            elif nach == "norm":
                self.nv = self.kv[:3]
                if round(self.kv[2], prec_int) != 0:
                    self.sv = [0, 0, self.kv[3] / self.kv[2]]

                elif round(self.kv[1], prec_int) != 0:
                    self.sv = [0, self.kv[3] / self.kv[1], 0]

                elif round(self.kv[0], prec_int) != 0:
                    self.sv = [self.kv[3] / self.kv[0], 0, 0]

        if rechenweg:
            abs_far = std.get_color("abs")
            if von == "para":
                if nach == "para":
                    pass

                if nach == "norm":
                    if intro:
                        cprint("Umrechnung einer Ebenengleichung von Parameterform zu Normalenform:\n", abs_far)
                    print("Zunächst den Normelenvektor bestimmen:\n")
                    ber.conv_norm(self.rv_1, self.rv_2, True, end=True)
                    if end:
                        print("\n")
                        cprint("Jetzt den Stützvektor mit dem Normalenvektor zu einer Normalenform führen:\n", abs_far)

                if nach == "koor":
                    if intro:
                        cprint("Umrechnung einer Ebenengleichung von Parameterform zu Koordinatenform:\n", abs_far)
                    self.umrechnen("para", "norm", "force", end=True)
                    print("\n")
                    self.umrechnen("norm", "koor", "force", end=True, ende=True)
                    end = False

            if von == "norm":
                if nach == "para":
                    if intro:
                        cprint("Umrechnung einer Ebenengleichung von Normalenform zu Parameterform:\n", abs_far)
                    self.umrechnen("norm", "koor", "force", end=True)
                    print("\n")
                    self.umrechnen("koor", "para", "force", end=True, ende=True)
                    end = False

                if nach == "koor":
                    if intro:
                        cprint("Umrechnung einer Ebenengleichung von Normalenform zu Koordinatenform:\n", abs_far)

                    print("Das Skalarprodukt aus Normalenvektor und Stützvektor bestimmen:\n")
                    ber.skalarprodukt(self.sv, self.nv, True, end=False)
                    if end:
                        print("\n")
                        cprint("Damit lautet die Koordinatenform:\n", abs_far)

            if von == "koor":
                if nach == "para":
                    if intro:
                        cprint("Umrechnung einer Ebenengleichung von Koordintenform zu der Parameterform:\n", abs_far)
                    if round(self.kv[2], prec_int) != 0:
                        print("Die Koordinatenform nach z umstellen:\n")
                        umst = "z"

                        lgs_list = [["", 1, "", "x"], ["", "", 1, "y"], [self.kv[3] / self.kv[2], -self.kv[0] / self.kv[2],
                                                                         -self.kv[1] / self.kv[2], "z"]]

                    else:
                        print("Normalerweise formt man die Koordintenform nach z um, allerdings ist z Null.\n")
                        if round(self.kv[1], prec_int) != 0:
                            cprint("Deswegen nach y umstellen:\n", abs_far)
                            umst = "y"
                            lgs_list = [["", 1, "", "x"], [self.kv[3] / self.kv[1], -self.kv[0] / self.kv[1],
                                                           -self.kv[2] / self.kv[1], "y"], ["", "", 1, "z"]]
                        else:
                            cprint("Deswegen nach x umstellen:\n", abs_far)
                            umst = "x"
                            lgs_list = [[self.kv[3] / self.kv[0], -self.kv[1] / self.kv[0], -self.kv[2] / self.kv[0], "x"],
                                        ["", 1, "", "y"], ["", "", 1, "z"]]

                    self.display(prec, darst="koor", umstellen=umst, rev=True)
                    print("\n")
                    cprint("Jetzt normieren:\n", abs_far)

                    if len(self.display(prec, darst="koor", umstellen=umst, rev=True, norm=True)) == 3:
                        print("\n")
                        print("Auswerten:\n")
                        std.config_["Bruch"] = False
                        self.display(prec, darst="koor", umstellen=umst, rev=True, norm=True)
                        std.config_["Bruch"] = True

                    p_list = [item for item in ["x", "y", "z"] if umst != item]
                    print("\n")
                    cprint(f"Jetzt eine Substitution vornehmen: {p_list[0]} = {self.param[0]}", abs_far)
                    cprint(f"                                   {p_list[1]} = {self.param[1]}", abs_far)
                    print("\n")
                    dis.lgs([[item if item else 0 for item in row] for row in lgs_list], prec, zeilen=True, param_list=["", self.param[0], self.param[1]], rev=True, print_param_str=False)
                    print("\n")
                    cprint("Daraus lässt sich eine Parametergleichung bilden, indem man die Parameter ausklammert.", abs_far)
                    if not sv_berechnen:
                        print("\n")
                        cprint("Es wird der ursprünglich gegebene Punkt für den Stützvektor genommen:\n")

                if nach == "norm":
                    if intro:
                        cprint("Umrechnung einer Ebenengleichung von Koordinatenform zu Normalenform:\n", abs_far)

                    if round(self.kv[2], prec_int) != 0:
                        print("Die Koordinatenform nach z umstellen und nur die Zahl betrachen:\n")
                        umst = "z"

                    else:
                        print("Normalerweise formt man die Koordintenform nach z um, allerdings ist z Null.\n")
                        if round(self.kv[1], prec_int) != 0:
                            print("Deswegen nach y umstellen und nur die Zahl betrachen:\n")
                            umst = "y"
                        else:
                            print("Deswegen nach x umstellen und nur die Zahl betrachen:\n")
                            umst = "x"

                    if len(self.display(prec, darst="koor", umstellen=umst, rev=True, norm=True, nur_zahl=True)) == 3:
                        print("\n")
                        print("Auswerten:\n")
                        std.config_["Bruch"] = False
                        self.display(prec, darst="koor", umstellen=umst, rev=True, norm=True, nur_zahl=True)
                        std.config_["Bruch"] = True

                    print("\n")
                    cprint(f"Dies ist der Spurpunkt bezüglich {umst}:\n")
                    P = Punkt(self.sv)
                    P.display(prec, zwi_far)
                    print("\n")
                    cprint("Der Normalenvektor ist bereits durch die Koordinatenform bekannt:\n")

        if end:
            self.display(prec, end_far, darst=nach, print_buchst=True)

    def einsetzen(self, objekt, typ=None, rechenweg=False, intro=False, end=False, ende=False, return_list=False):
        """
        Einsetzen von einem Objekt (Punkt, Gerade, Ebene) in die Ebene
        Parameters
        ----------
        objekt      Objekt das eingesetzt wird
        typ         Typ vom Objekt das eingesetzt wird - nur bei parameter nötig
        rechenweg   Soll ein Rechenweg angezeigt werden
        intro       Soll ein Intro angezeigt werden
        end         Soll ein Ende angezeigt werden
        ende        Soll das Ende als Ende von allem behandelt werden
        buchst      Keine Funktion, nur damit sowohl gerade / ebene den gleichen keyword accepted
        return_list Soll das Objekt als Liste zurückgegeben werden oder als instanziiertes Objekt

        Returns
        -------
        Das eingesetzte Objekt
        """
        std.verify_input(objekt, "Objekt", ("punkt", "gerade", "ebene"))
        std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
        std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

        prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

        if not isinstance(objekt, (Gerade, Punkt, Ebene)) and typ != "parameter" and typ != "zwei parameter" and typ != "hnf":
            err_far = std.get_color("err")
            raise InputError(colored(f"Das Objekt ist nicht instanziiert: {objekt}", err_far))

        if isinstance(objekt, Punkt):
            wert = [self.kv[i] * objekt.P[i] for i in range(3)]
            if rechenweg:
                if intro:
                    cprint(f"Einsetzen eines Punktes in die Koordinatenform der Ebene {self.buchst}:\n", abs_far)
                print(f"Die Werte von {objekt.buchst} jeweils in x, y und z von der Koordinatenform einsetzen:\n")

                self.display(3, darst="koor", einsetzen=objekt, schritt=0, print_buchst=False)
                print("\n")
                print("Vereinfachen:\n")
                self.display(3, darst="koor", einsetzen=objekt, schritt=1, print_buchst=False)
                print("\n")
                print("Zusammenfassen:\n")

            if end:
                self.display(3, end_far, darst="koor", einsetzen=objekt, schritt=2, print_buchst=False)

                return sum(wert) == self.kv[3]

        elif isinstance(objekt, Gerade):
            ohne_param = round(sum(self.kv[i] * objekt.sv[i] for i in range(3)), prec_int)
            mit_param = round(sum(self.kv[i] * objekt.rv[i] for i in range(3)), prec_int)
            if rechenweg:
                if intro:
                    cprint(f"Einsetzen einer Gerade in die Koordinatenform der Ebene {self.buchst}")
                print(f"Die Werte von {objekt.buchst} jeweils in x, y und z von der Koordinatenform einsetzen:\n")
                self.display(3, darst="koor", einsetzen=objekt, schritt=0, print_buchst=False)
                print("\n")
                print("Ausmultiplizieren:\n")
                self.display(3, darst="koor", einsetzen=objekt, schritt=1, print_buchst=False)
                print("\n")
                print("Vereinfachen:\n")
                self.display(3, darst="koor", einsetzen=objekt, schritt=2, print_buchst=False)
                if round(mit_param, prec_int) != 0:
                    print("\n")
                    print("Umstellen:\n")
                    if round(mit_param, prec_int) not in [0, 1]:
                        self.display(3, darst="koor", einsetzen=objekt, schritt=3, print_buchst=False)

                if round(mit_param, prec_int) not in [0, 1]:
                    print("\n")
                    print("Normieren:\n")

            if end:
                if round(mit_param, prec_int) != 0:
                    self.display(3, end_far, darst="koor", einsetzen=objekt, schritt=4, print_buchst=False)

            if round(mit_param, prec_int) == 0:
                if round(self.kv[3], prec_int) == round(ohne_param, prec_int):
                    return True
                else:
                    return False

            return (self.kv[3] - ohne_param) / mit_param

        elif isinstance(objekt, Ebene):
            ohne_param = round(sum(self.kv[i] * objekt.sv[i] for i in range(3)), prec_int)
            mit_param_1 = round(sum(self.kv[i] * objekt.rv_1[i] for i in range(3)), prec_int)
            mit_param_2 = round(sum(self.kv[i] * objekt.rv_2[i] for i in range(3)), prec_int)

            if rechenweg:
                if intro:
                    cprint(f"Einsetzen einer Ebene in die Koordinatenform der Ebene {self.buchst}")
                print(f"Die Werte von {objekt.buchst} jeweils in x, y und z von der Koordinatenform einsetzen:\n")
                self.display(3, darst="koor", einsetzen=objekt, schritt=0, print_buchst=False)
                print("\n")
                print("Ausmultiplizieren:\n")
                self.display(3, darst="koor", einsetzen=objekt, schritt=1, print_buchst=False)
                print("\n")
                print("Vereinfachen:\n")
                self.display(3, darst="koor", einsetzen=objekt, schritt=2, print_buchst=False)
                if round(mit_param_1, prec_int) != 0 or round(mit_param_2, prec_int) != 0:
                    print("\n")
                    print("Umstellen:\n")
                    if (round(mit_param_1, prec_int) != 0 and round(mit_param_1, prec_int) != 1) or (round(mit_param_2, prec_int) != 0 and round(mit_param_2, prec_int) != 1):
                        self.display(3, darst="koor", einsetzen=objekt, schritt=3, print_buchst=False)

                if (round(mit_param_1, prec_int) != 0 and round(mit_param_1, prec_int) != 1) or (round(mit_param_2, prec_int) != 0 and round(mit_param_2, prec_int) != 1):
                    print("\n")
                    print("Normieren:\n")

            if end:
                if round(mit_param_1, prec_int) != 0 or round(mit_param_2, prec_int) != 0:
                    self.display(3, end_far, darst="koor", einsetzen=objekt, schritt=4, print_buchst=False)

            if round(mit_param_1, prec_int) == 0 and round(mit_param_2, prec_int) == 0:
                if round(ohne_param, prec_int) != round(self.kv[3], prec_int):
                    return False
                else:
                    return True

            return [mit_param_1, mit_param_2, self.kv[3] - ohne_param]

        if typ is not None and "parameter" in typ:
            objekt = copy.deepcopy(objekt)
            if typ == "zwei parameter":
                # objekt in Form: [[Para für Stütz 1, Para für RV 1], [Para für Stütz 2, Para für RV 2]]
                g = Gerade([[a + objekt[0][0] * b + objekt[1][0] * c for a, b, c in zip(self.sv, self.rv_1, self.rv_2)], [objekt[0][1] * a + objekt[1][1] * b for a, b in zip(self.rv_1, self.rv_2)]], param=self.param[1])
                for item in objekt:
                    item.reverse()
                    item.insert(0, 1)
                param = "r"
            else:
                if round(objekt[0], prec_int):
                    objekt[1] /= -objekt[0]
                    objekt[2] /= objekt[0]
                    param = self.param[1]
                    parameter = 1
                else:
                    objekt[0], objekt[1] = objekt[1], objekt[0]
                    objekt[2] /= objekt[0]
                    param = self.param[0]
                    parameter = 2

                if round(objekt[0], prec_int):
                    g = Gerade([[a + objekt[2] * b for a, b in zip(self.sv, self.rv_1)], [a + objekt[1] * b for a, b in zip(self.rv_2, self.rv_1)]], param=param)

                else:
                    g = Gerade([[a + objekt[2] * b for a, b in zip(self.sv, self.rv_2)], copy.deepcopy(self.rv_1)], param=param)

            if rechenweg:
                self.display(prec)
                old_buchst = self.buchst
                self.buchst = "g"
                buchst, sv, rv_1, rv_2 = self.display(prec, nur="buchst", print_=False), self.display(prec, nur="sv", print_=False), self.display(prec, nur="rv_1", print_=False), self.display(prec, nur="rv_2", print_=False)
                para_1, para_2 = self.display(prec, nur="para_1", print_=False), self.display(prec, nur="para_2", print_=False)
                print("\n")
                print("Einsetzen:\n")

                klammer = False
                if typ == "zwei parameter":
                    objekt_ = objekt
                else:
                    objekt_ = [objekt]

                para = []
                for item in objekt_:
                    if round(item[1], prec_int) != 0 and round(item[2], prec_int) != 0:
                        para.append(f" + ({std.format_prec(item[2], prec)} {std.negcheck(item[1])[0]} {std.format_prec(item[1], prec, absval=True)}{param}) ∙ ")
                        klammer = True
                    else:
                        if round(item[1], prec_int) == 0:
                            para.append(f" {std.negcheck(item[2])[0]} {std.format_prec(item[2], prec, absval=True)} ∙ ")
                        else:
                            para.append(f" {std.negcheck(item[1])[0]} {std.format_prec(item[1], prec, absval=True)}{param} ∙ ")

                if typ == "zwei parameter" or parameter == 1:
                    para_1 = std.format_prec(["", para[0], ""], string=True)
                    if typ == "zwei parameter":
                        para_2 = std.format_prec(["", para[1], ""], string=True)
                else:
                    para_2 = std.format_prec(["", para[0], ""], string=True)

                for _ in zip(buchst, sv, para_1, rv_1, para_2, rv_2):
                    print("".join(_))

                print("\n")
                if klammer:
                    print("Ausmultiplizieren:\n")

                    if typ == "zwei parameter":
                        para_l = [[], []]
                        rv_l = [[], []]
                        for i, item in enumerate(objekt):
                            for j, _ in enumerate(reversed(item[1:])):
                                if round(_, prec_int) != 0:
                                    para_l[i].append(f" {std.negcheck(_, prec)[0]} {std.format_prec(_, prec, absval=True)}{param if j == 1 else ''} ∙ ")
                                    if i == 0:
                                        rv_l[i].append(rv_1)
                                    else:
                                        rv_l[i].append(rv_2)
                                else:
                                    para_l[i].append("")
                                    rv_l[i].append(["", "", ""])

                        para_1, para_2 = para_l
                        para_1, para_2 = [std.format_prec(["", item, ""], string=True) for item in para_1], [std.format_prec(["", item, ""], string=True) for item in para_2]
                        rv_1, rv_2 = rv_l

                    else:
                        para = [f" {std.negcheck(objekt[2], prec)[0]} {std.format_prec(objekt[2], prec, absval=True)} ∙ " if round(objekt[2], prec_int) != 0 else '',
                                f" {std.negcheck(objekt[1], prec)[0]} {std.format_prec(objekt[1], prec, absval=True)}{param} ∙ " if round(objekt[2], prec_int) != 0 else '']

                        if parameter == 1:
                            rv_1 = [rv_1, rv_1]
                            rv_2 = [rv_2, ["", "", ""]]
                            para_1 = [std.format_prec(["", item, ""], string=True) for item in para]
                            para_2 = [para_2, ["", "", ""]]
                        else:
                            rv_1 = [rv_1, ["", "", ""]]
                            rv_2 = [rv_2, rv_2]
                            para_1 = [para_1, ["", "", ""]]
                            para_2 = [std.format_prec(["", item, ""], string=True) for item in para]

                    for _ in zip(buchst, sv, para_1[0], rv_1[0], para_1[1], rv_1[1], para_2[0], rv_2[0], para_2[1], rv_2[1]):
                        print("".join(_))

                    print("\n")

                print("Zusammenfassen:\n")
                self.buchst = old_buchst

            if end:
                g.display(prec)

            if return_list:
                return [g.sv, g.rv]
            return g

        elif typ is not None and typ == "hnf":
            if not isinstance(objekt, Vektor):
                objekt = Vektor(objekt)

            diff = [a - b for a, b in zip(objekt.v, self.sv)]
            d = ber.skalarprodukt(diff, self.nv)

            if rechenweg:
                print("Einsetzen:\n")
                self.display(prec, einsetzen=objekt, n0=True, schritt=0)
                print("\n")
                print("Subtrahieren:\n")
                self.display(prec, einsetzen=Vektor(diff), n0=True, schritt=1)
                print("\n")
                print("Skalarprodukt bilden:\n")
                ber.skalarprodukt(diff, self.nv, True, end=True)

            return d

    def display(self, prec, color=None, darst=None, print_buchst=True, print_=True, umstellen=False, rev=False, norm=False,
                nur_zahl=False, einsetzen=False, schritt=False, nur=None, n0=False):
        """

        Parameters
        ----------
        prec            Anzahl der Nachkommastellen
        color           Die Farbe die angezeigt wird
        darst           Die Darstellung der Ebene
        print_buchst    Soll der Buchstabe der Ebene geprinted werden
        print_          Soll die Ebene geprinted werden
        umstellen       Nur bei darst == koor: Soll nach x / y / z / zahl umgestellt werden
        rev             Soll die Umstellung reversed werden
        norm            Soll bei der Umstellung normiert werden
        nur_zahl        Keine Ahnung
        einsetzen       Soll ein Objekt in die Ebene eingesetzt werden - Von .einsetzen() kontrolliert
        schritt         Welcher Schritt der Einsetzung gewählt wird
        nur             Soll nur ein bestimmter Vektor (sv, rv_1, rv_2) angezeigt werden
        n0              Soll bei darst == norm der Normaleneinheitsvektor angezeigt werden

        Returns
        -------
        Liste die geprinted wurde
        """
        std.verify_input(darst, "darst", ("ebene darst", None))
        std.verify_input(color, "Farbe", "farben_en"), std.verify_input(print_, "print_ebene", bool)

        if darst is None:
            darst = self.darst

        if isinstance(prec, list):
            all(std.verify_input(item, "prec", Number) for item in prec)
        else:
            std.verify_input(prec, "prec", Number)

        out = []
        klam = std.get_klam(self.dim)
        mitte = int(self.dim / 2)

        if print_buchst:
            if darst != "koor":

                if darst == "para":
                    buchst = std.format_prec(["", self.buchst], string=True, pfeil=self.has_pfeil)
                    x = std.format_prec("x", string=True, pfeil=True)
                    buchst[0] += f"  {x[0]}   "
                    buchst[1] += f": {x[1]} = "
                else:
                    if n0:
                        buchst = std.format_prec(["", "d = "], string=True)
                    else:
                        buchst = std.format_prec([self.pfeil, f"{self.buchst}: "], string=True, ausrichtung="links")
                i = 2
                while i < self.dim:
                    buchst.append("")
                    i += 1

                buchst = std.format_prec(buchst, string=True, ausrichtung="links")

            else:
                buchst = f"{self.buchst}: "

        else:
            if darst != "koor":
                buchst = ["" for _ in range(self.dim)]
            else:
                buchst = ""

        if darst == "para":
            prec = std.prec_auffüllen(prec, 3)

            param = [std.format_prec([f" + {item} ∙ " if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links") for item in self.param]
            E_darst = [std.format_prec(item, prec[i], string=True, string_ausrichtung="mitte") for i, item in enumerate([self.sv, self.rv_1, self.rv_2])]

            for i in range(self.dim):
                if nur == "buchst":
                    out.append(buchst[i])

                elif nur == "para_1":
                    out.append(param[0][i])
                elif nur == "para_2":
                    out.append(param[1][i])
                elif nur == "sv":
                    out.append(f"{klam[0][i]}{E_darst[0][i]}{klam[1][i]}")

                elif nur == "rv_1":
                    out.append(f"{klam[0][i]}{E_darst[1][i]}{klam[1][i]}")

                elif nur == "rv_2":
                    out.append(f"{klam[0][i]}{E_darst[2][i]}{klam[1][i]}")

                else:
                    out.append(f"{buchst[i]}{klam[0][i]}{E_darst[0][i]}{klam[1][i]}")

                    for j in range(1, 3):
                        out[i] += f"{param[j - 1][i]}{klam[0][i]}{E_darst[j][i]}{klam[1][i]}"

        elif darst == "norm":
            prec = std.prec_auffüllen(prec, 2)
            if n0:
                prec[1] = std.get_prec(3)

            E_darst = [std.format_prec(item, prec[i], string=True, string_ausrichtung="mitte") for i, item in enumerate([self.sv, self.nv])]
            minus = std.format_prec(["-" if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links")

            circ = std.format_prec(["∘" if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links")
            if einsetzen:
                x = einsetzen.display(prec, print_=False, print_buchst=False)
            else:
                x = std.format_prec(["x" if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links", pfeil=True)
            if n0 is False:
                null = std.format_prec([" = 0" if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links")
            else:
                null = [""] * 3

            check = not einsetzen or schritt not in [1]

            for i in range(self.dim):
                if nur == "sv":
                    out.append(f"{klam[0][i]}{E_darst[0][i]}{klam[1][i]}")

                elif nur == "nv":
                    out.append(f"{klam[0][i]}{E_darst[1][i]}{klam[1][i]}")

                else:
                    out.append(f"{buchst[i]}{klam[0][i] if check else ''} {x[i]}{f' {minus[i]} {klam[0][i]}{E_darst[0][i]}{klam[1][i]}' if check else ''}")
                    out[i] += f" {klam[1][i] + ' ' if check else ''}{circ[i]} {klam[0][i]}{E_darst[1][i]}{klam[1][i]}{null[i]}"

        elif darst == "koor":
            # Hier siehst du wie man etwas overengineeren kann. Eigentlich hätte die Funktion so schön simpel sein können, aber ich wollte immer mehr in die Funktion reinbauen.
            # Ist nicht immer empfehlenswert
            prec_int = std.get_prec("int")
            bruch = std.get_divers("bruch")
            eval_nchk = True

            if umstellen is False:
                umstellen = "zahl"

            prec = std.prec_auffüllen(prec, 4)

            if umstellen != "zahl":
                if umstellen == "x":
                    umst = 0
                    davor_list = [[],
                                  [-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3]],
                                  [-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3],
                                   -self.kv[1] if isinstance(self.kv[1], Number) else self.kv[1]], []]

                    davor_links = [-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3],
                                   -self.kv[1] if isinstance(self.kv[1], Number) else self.kv[1],
                                   -self.kv[2] if isinstance(self.kv[2], Number) else self.kv[2]]

                elif umstellen == "y":
                    umst = 1
                    davor_list = [[-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3]], [],
                                  [-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3],
                                   -self.kv[0] if isinstance(self.kv[0], Number) else self.kv[0]], []]

                    davor_links = [-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3],
                                   -self.kv[0] if isinstance(self.kv[0], Number) else self.kv[0],
                                   -self.kv[2] if isinstance(self.kv[2], Number) else self.kv[2]]

                elif umstellen == "z":
                    umst = 2
                    davor_list = [[-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3]],
                                  [-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3],
                                   -self.kv[0] if isinstance(self.kv[0], Number) else self.kv[0]], [], []]

                    davor_links = [-self.kv[3] if isinstance(self.kv[3], Number) else self.kv[3],
                                   -self.kv[0] if isinstance(self.kv[0], Number) else self.kv[0],
                                   -self.kv[1] if isinstance(self.kv[1], Number) else self.kv[1]]

                koor = [-item if i != umst and not isinstance(item, str) and i != 3 else item for i, item in enumerate(self.kv)]

            else:
                koor = self.kv.copy()

                davor_list = [[], [self.kv[0]], [self.kv[0], self.kv[1]], []]
                davor_links = [self.kv[0], self.kv[1], self.kv[2]]

                umst = 3

            zeichen = "="
            if einsetzen:
                if isinstance(einsetzen, Punkt):
                    if schritt == 0:
                        iter_list = [std.format_prec(item, prec, mehrere=False, klammer=True) for item, prec in zip(einsetzen.P, prec)]
                        iter_list = ["" if i == 3 else f" ∙ {iter_list[i]}" for i in range(4)]

                    elif schritt == 1:
                        for i in range(len(koor) - 1):
                            if isinstance(koor[i], Number):
                                koor[i] *= einsetzen.P[i]

                        if koor[umst] == 0:
                            bruch_check = False
                        else:
                            bruch_check = any(int((item * P) / koor[umst] * einsetzen.P[0]) != round((item * P) / koor[umst] * einsetzen.P[0], prec_int) if (isinstance(item, Number) and isinstance(koor[umst], Number)) else 1 for item, P in zip(koor, einsetzen.P))

                        iter_list = [""] * 4

                    elif schritt == 2:
                        koor = [sum(item * P for item, P in zip(koor, einsetzen.P))] + [""] * 2 + [self.kv[3]]

                        iter_list = ["", "", "", ""]
                        if round(koor[0], prec_int) != round(koor[3], prec_int):
                            zeichen = "≠"

                if isinstance(einsetzen, Gerade):
                    ohne_param = sum(koor[i] * einsetzen.sv[i] for i in range(3))
                    mit_param = sum(koor[i] * einsetzen.rv[i] for i in range(3))
                    if schritt == 0:
                        iter_list = [[std.format_prec(item, prec, mehrere=False) for item, prec in zip(einsetzen.sv, prec)], [std.format_prec(item, prec, mehrere=False, klammer=True) for item, prec in zip(einsetzen.rv, prec)]]
                        iter_list = ["" if i == 3 else f" ∙ ({iter_list[0][i]} + {einsetzen.param} ∙ {iter_list[1][i]})" for i in range(4)]

                    elif schritt == 1:
                        ohne_param = [koor[i] * einsetzen.sv[i] for i in range(3) if isinstance(koor[i], Number)]
                        mit_param = [koor[i] * einsetzen.rv[i] for i in range(3) if isinstance(koor[i], Number)]

                        iter_list = [""] * 4
                        bruch_check = False
                        nchk_mit = std.negcheck(mit_param)

                        koor = [f"{'' if round(a, prec_int) == 0 else std.format_prec(a, prec_) if i == 0 else std.format_prec(a, prec_, absval=True)}"
                                f"{std.format_prec(0, prec[0]) if round(a, prec_int) == 0 and round(b, prec_int) == 0 else ''}{f' {nchk_mit[i]} ' if round(a, prec_int) != 0 and round(b, prec_int) != 0 else ''}"
                                f"{std.format_prec(b, prec_, klammer=True, absval=True) if round(b, prec_int) not in [0, 1, -1] else ''}{f'{einsetzen.param}' if round(b, prec_int) != 0 else ''}" for i, (a, b, prec_) in enumerate(zip(ohne_param, mit_param, prec))] + [koor[-1]]
                        eval_nchk = False
                        nchk = [a if round(a, prec_int) != 0 else b for a, b in zip(ohne_param, mit_param)]
                        nchk = std.negcheck(nchk)

                    elif schritt == 2:
                        iter_list = [""] * 4
                        koor = [f"{std.format_prec(ohne_param, prec[0]) if round(ohne_param, prec_int) != 0 else ''}{f' {std.negcheck(mit_param)[0]} ' if round(mit_param, prec_int) != 0 else ''}"
                                f"{std.format_prec(mit_param, prec[0], absval=True) if round(mit_param, prec_int) not in [0, 1, -1] else ''}{einsetzen.param if round(mit_param, prec_int) != 0 else ''}", "", ""] + [koor[-1]]
                        if round(mit_param, prec_int) == 0 and round(ohne_param, prec_int) != round(self.kv[3], prec_int):
                            zeichen = "≠"

                    elif schritt == 3:
                        iter_list = [""] * 4
                        koor = [f"{std.format_prec(mit_param, prec[0]) if round(mit_param, prec_int) != 1 else ''}{einsetzen.param if round(mit_param, prec_int) != 0 else ''}", "", ""] + [std.format_prec(self.kv[3] - ohne_param, prec[0])]

                    elif schritt == 4:
                        iter_list = [""] * 4
                        koor = [einsetzen.param, "", "", std.format_prec((self.kv[3] - ohne_param) / mit_param, prec[0])]

                elif isinstance(einsetzen, Ebene):
                    ohne_param = sum(self.kv[i] * einsetzen.sv[i] for i in range(3))
                    mit_param_1 = sum(self.kv[i] * einsetzen.rv_1[i] for i in range(3))
                    mit_param_2 = sum(self.kv[i] * einsetzen.rv_2[i] for i in range(3))
                    diff = self.kv[3] - ohne_param
                    if schritt == 0:
                        iter_list = [[std.format_prec(item, prec, mehrere=False) for item, prec in zip(einsetzen.sv, prec)], [std.format_prec(item, prec, mehrere=False, klammer=True) for item, prec in zip(einsetzen.rv_1, prec)], [std.format_prec(item, prec, mehrere=False, klammer=True) for item, prec in zip(einsetzen.rv_2, prec)]]
                        iter_list = ["" if i == 3 else f" ∙ ({iter_list[0][i]} + {einsetzen.param[0]} ∙ {iter_list[1][i]} + {einsetzen.param[1]} ∙ {iter_list[2][i]})" for i in range(4)]

                    elif schritt in [1, 2]:
                        if schritt == 2:
                            ohne_param = [ohne_param]
                            mit_param_1 = [mit_param_1]
                            mit_param_2 = [mit_param_2]
                        else:
                            ohne_param = [self.kv[i] * einsetzen.sv[i] for i in range(3)]
                            mit_param_1 = [self.kv[i] * einsetzen.rv_1[i] for i in range(3)]
                            mit_param_2 = [self.kv[i] * einsetzen.rv_2[i] for i in range(3)]
                        last = copy.deepcopy(koor[-1])
                        iter_list = [""] * 4
                        koor = []
                        nchk_lst = []
                        for i, (a, b, c) in enumerate(zip(ohne_param, mit_param_1, mit_param_2)):
                            koor.append("")
                            print_before = False
                            if round(a, prec_int) != 0:
                                if i == 0:
                                    koor[i] += std.format_prec(a, prec[i])
                                else:
                                    koor[i] += std.format_prec(a, prec[i], absval=True)
                                print_before = True
                                nchk_lst.append(a)

                            if round(b, prec_int) != 0:
                                nchk = std.negcheck(b)
                                if print_before:
                                    koor[i] += f" {nchk[0]} {std.format_prec(b, prec[i], absval=True) if round(b, prec_int) != 1 else ''}{einsetzen.param[0]}"
                                else:
                                    koor[i] += f"{std.format_prec(b, prec[i], absval=True) if round(b, prec_int) != 1 else ''}{einsetzen.param[0]}"
                                    nchk_lst.append(b)
                                print_before = True

                            if round(c, prec_int) != 0:
                                nchk = std.negcheck(c)
                                if print_before:
                                    koor[i] += f" {nchk[0]} {std.format_prec(c, prec[i], absval=True) if round(c, prec_int) != 1 else ''}{einsetzen.param[1]}"
                                else:
                                    koor[i] += f"{std.format_prec(c, prec[i], absval=True) if round(c, prec_int) != 1 else ''}{einsetzen.param[1]}"
                                    nchk_lst.append(c)
                                print_before = True

                            if print_before is False:
                                koor[i] += std.format_prec(0, prec[i])
                                nchk_lst.append(0)

                        if schritt == 2:
                            koor.extend(("", ""))

                        nchk_lst.append(0)

                        koor.append(last)
                        eval_nchk = False
                        nchk = std.negcheck(nchk_lst)

                    elif schritt in [3, 4]:
                        iter_list = [""] * 4

                        if round(mit_param_1, prec_int):
                            mit_param_2 = -mit_param_2
                            if schritt == 4:
                                mit_param_2 /= mit_param_1
                                diff /= mit_param_1
                                mit_param_1 /= mit_param_1

                            nchk = std.negcheck(mit_param_2)
                            koor = [f"{std.format_prec(mit_param_1, prec[0]) if round(mit_param_1, prec_int) != 1 else ''}{einsetzen.param[0]}", "", "", f"{std.format_prec(diff, prec[3])}{f' {nchk[0]} ' if round(mit_param_2, prec_int) != 0 else ''}"
                                                                                                                                                         f"{std.format_prec(mit_param_2, prec[1], absval=True) if round(mit_param_2, prec_int) not in [0, 1, -1] else ''}{einsetzen.param[1] if round(mit_param_2, prec_int) != 0 else ''}"]
                        else:
                            if schritt == 4:
                                diff /= mit_param_2
                                mit_param_2 /= mit_param_2

                            nchk = std.negcheck(mit_param_2)
                            koor = [f"{std.format_prec(mit_param_2, prec[0]) if round(mit_param_2, prec_int) != 1 else ''}{einsetzen.param[1]}", "", "", f"{std.format_prec(diff, prec[3])}"]

            else:
                if koor[umst] == 0:
                    bruch_check = False
                else:
                    bruch_check = any(int(abs(item / koor[umst])) != round(abs(item / koor[umst]), prec_int) if (isinstance(item, Number) and isinstance(koor[umst], Number)) else 1 for item in koor)
                iter_list = [" x", " y", " z", ""]

            if norm and bruch and bruch_check:
                nchk = [std.negcheck(["", item / koor[umst] if (isinstance(item, Number) and isinstance(koor[umst], Number)) else item, ""], string=False) for item in koor]

                bruch = True
                mitte = 1
                E_darst, E_darst_abs = [], []

                for i, item in enumerate(koor):
                    if (isinstance(item, Number) and isinstance(koor[umst], Number)) and int(item / koor[umst]) == round(item / koor[umst], prec_int):
                        E_darst.append(std.format_prec(["", item / koor[umst], ""], prec[i], string=True))
                        E_darst_abs.append(std.format_prec(["", item / koor[umst], ""], prec[i], string=True, absval=True))

                    else:
                        E_darst.append(std.format_prec([item, koor[umst]], prec[i], mehrere=False, bruch=True, absval=True))
                        E_darst_abs.append(std.format_prec([item, koor[umst]], prec[i], mehrere=False, bruch=True, absval=True))

            else:
                bruch = False
                mitte = 0
                if norm:
                    if eval_nchk:
                        nchk = std.negcheck([item/koor[umst] for item in koor])
                    E_darst = [std.format_prec(item / koor[umst] if isinstance(item, Number) else item, prec[i], string=True) for i, item in enumerate(koor)]
                    E_darst_abs = [std.format_prec(item / koor[umst] if isinstance(item, Number) else item, prec[i], absval=True, string=True) for i, item in enumerate(koor)]

                else:
                    if eval_nchk:
                        nchk = std.negcheck(koor)
                    E_darst = [std.format_prec(item, prec[i], string=True) for i, item in enumerate(koor)]
                    E_darst_abs = [std.format_prec(item, prec[i], absval=True, string=True) for i, item in enumerate(koor)]

            darst = []

            for j, item in enumerate(iter_list):
                if E_darst[j]:
                    if umstellen == item.strip():
                        if bruch:
                            darst.append([f"{E_darst[j][i]}{item}" if i == mitte else f"{E_darst[j][i]}{'  ' if item else ''}" for i in range(3)])
                        else:
                            darst.append(f"{E_darst[j]}{item}")

                    else:
                        if isinstance(self.kv[j], str) or round(self.kv[j], prec_int) != 0:
                            if any(round(item, prec_int) if isinstance(item, Number) else 1 for item in davor_list[j]) or (isinstance(einsetzen, Ebene) and schritt == 1 and j != 0):  # Kack Lösung aber keine Ahnung wie ichs sonst lösen soll
                                if bruch:
                                    darst.append([f" {nchk[j][i]} {E_darst_abs[j][i]}{item}" if i == mitte else f"   {E_darst_abs[j][i]}{'  ' if item else ''}" for i in range(3)])
                                else:
                                    darst.append(f" {nchk[j]} {E_darst_abs[j]}{item}")
                            else:
                                if bruch:
                                    if nchk[j][mitte] == "-" and E_darst[j][0].strip():
                                        darst.append([f"{nchk[j][i]} {E_darst_abs[j][i]}{item}" if i == mitte else f"  {E_darst_abs[j][i]}{'  ' if item else ''}" for i in range(3)])
                                    else:
                                        darst.append([f"{E_darst[j][i]}{item}" if i == mitte else f"{E_darst[j][i]}{'  ' if item else ''}" for i in range(3)])

                                else:
                                    if nchk[mitte] == "-":
                                        darst.append(f"{E_darst[j]}{item}")
                                    else:
                                        darst.append(f"{E_darst[j]}{item}")
                        else:
                            if j == 3 and (umstellen == "zahl" and j == 3 or not any(round(item, prec_int) if isinstance(item, Number) else 1 for item in davor_links)):
                                if bruch:
                                    darst.append([f"{E_darst[j][i]}{item}" if i == mitte else f"{E_darst[j][i]}{'  ' if item else ''}" for i in range(3)])
                                else:
                                    darst.append(f"{E_darst[j]}{item}")
                            else:
                                if bruch:
                                    darst.append(["" for _ in range(3)])
                                else:
                                    darst.append("")
                else:
                    darst.append("")

            # Wert der auf der allein auf einer Seite von = stehen soll - index [3]
            if nur_zahl:
                if umstellen == "zahl":
                    pass
                else:
                    if bruch:
                        darst = [[item if i == umst or i == 3 else "" for item in row] for i, row in enumerate(darst)]
                    else:
                        darst = [item if i == umst or i == 3 else "" for i, item in enumerate(darst)]

            if umstellen == "x":
                darst[0], darst[1], darst[2], darst[3] = darst[3], darst[1], darst[2], darst[0]

            elif umstellen == "y":
                darst[0], darst[1], darst[2], darst[3] = darst[3], darst[0], darst[2], darst[1]

            elif umstellen == "z":
                darst[0], darst[1], darst[2], darst[3] = darst[3], darst[0], darst[1], darst[2]

            elif umstellen == "zahl":
                darst[0], darst[1], darst[2], darst[3] = darst[0], darst[1], darst[2], darst[3]

            if rev:
                darst.insert(0, darst[-1])
                darst.pop()
                if bruch:
                    darst[0] = [f"{darst[0][i]} {zeichen} " if i == mitte else f"{darst[0][i]}   " for i in range(3)]
                else:
                    darst[0] += f" {zeichen} "

            else:
                if bruch:
                    darst[-1] = [f" {zeichen} {darst[-1][i]}" if i == mitte else f"   {darst[-1][i]}" for i in range(3)]
                else:
                    darst[-1] = f" {zeichen} {darst[-1]}"

            if bruch:
                buchst = [buchst if i == mitte else " " * len(buchst) for i in range(3)]
                for i in range(3):
                    out.append(buchst[i])
                    for j in range(4):
                        out[i] += f"{darst[j][i]}"
            else:

                out = [buchst]
                for j in range(4):
                    out[0] += f"{darst[j]}"

        if print_:
            for item in out:
                cprint(item, color)

        return out


class Gerade:
    """Class für eine Gerade."""

    def __init__(self, inp, param="r", buchst="g", pfeil=False):
        """

        Parameters
        ----------
        inp     Input für die Gerade - in Form: [[_, _, _], [_, _, _]]
        param   Parameter für die Gerade
        buchst  Buchstabe für die Gerade
        pfeil   Ob der Buchstabe ein Pfeil haben soll
        """
        std.verify_input(inp, buchst, "gerade"), std.verify_input(param, "Parameter", str)
        std.verify_input(buchst, "Buchstabe", str), std.verify_input(pfeil, "Pfeil", bool)

        self.param = param
        self.buchst = buchst
        self.has_pfeil = pfeil
        if pfeil:
            self.pfeil = std.format_prec(buchst, string=True, pfeil=True, nur_pfeil=True)
        else:
            self.pfeil = " " * len(buchst)

        self.dim = len(inp[0])

        self.sv = inp[0]
        self.rv = inp[1]

    def einsetzen(self, objekt, typ=None, rechenweg=False, intro=False, end=False, ende=False, return_list=False, buchst="S"):
        std.verify_input(objekt, "Objekt", ("punkt", "gerade", Number))
        std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
        std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

        prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

        if typ == "parameter":
            S = Vektor([self.sv[i] + objekt * self.rv[i] for i in range(self.dim)], buchst=buchst)
            if rechenweg:
                if intro:
                    cprint("Einsetzen eines Parameters in eine Gerade:\n", abs_far)
                print("Den Parameter multiplizieren und zeilenweise addieren:\n")
                self.display(prec, einsetzen=objekt, typ=typ, schritt=0, print_buchst=True, buchst=buchst)
                print("\n")
                self.display(prec, einsetzen=objekt, typ=typ, schritt=1, print_buchst=True, buchst=buchst)

            if end:
                if rechenweg:
                    print("\n")
                    print("Damit kommt man auf den Vektor:\n")
                S.display(prec, end_far)

            if return_list:
                return S.v
            return S

    def display(self, prec, color=None, print_buchst=True, print_=True, nur=None, einsetzen=None, typ=None, schritt=False, buchst=None):
        std.verify_input(color, "Farbe", "farben_en"), std.verify_input(print_, "print gerade", bool)

        if isinstance(prec, list):
            all(std.verify_input(item, "prec", Number) for item in prec)
        else:
            std.verify_input(prec, "prec", Number)

        out = []
        klam = std.get_klam(self.dim)
        mitte = int(self.dim / 2)

        if print_buchst:
            if einsetzen is None:
                x = std.format_prec("x", string=True, pfeil=True)
                buchst = std.format_prec(["", self.buchst], string=True, pfeil=self.has_pfeil)
                buchst[0] += f"  {x[0]}"
                buchst[1] += f": {x[1]}"
                i = 2
                while i < self.dim:
                    buchst.append("")
                    i += 1

            else:
                buchst = ["", buchst, ""]
            buchst = std.format_prec(buchst, string=True, ausrichtung="links")

            for i in range(self.dim):
                if i == mitte:
                    buchst[i] += " = "
                else:
                    buchst[i] += "   "
        else:
            buchst = ["" for _ in range(self.dim)]

        prec = std.prec_auffüllen(prec, 2)

        if einsetzen is not None:
            if typ == "parameter":
                if schritt == 0:
                    nchk = std.negcheck(einsetzen)
                    param = std.format_prec([f" {nchk[0]} {std.format_prec(einsetzen, prec[0], absval=True)} ∙ " if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links")
                elif schritt == 1:
                    param = std.format_prec([f" + " if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links")
        else:
            param = std.format_prec([f" + {self.param} ∙ " if i == mitte else "" for i in range(self.dim)], string=True, ausrichtung="links")

        if einsetzen is not None and typ == "parameter" and schritt == 1:
            rv = copy.deepcopy(self.rv)
            rv = [item * einsetzen for item in rv]
            g_darst = [std.format_prec(item, prec[i], string=True, string_ausrichtung="mitte") for i, item in enumerate([self.sv, rv])]

        else:
            g_darst = [std.format_prec(item, prec[i], string=True, string_ausrichtung="mitte") for i, item in enumerate([self.sv, self.rv])]

        for i in range(self.dim):
            if nur == "sv":
                out.append(f"{klam[0][i]}{g_darst[0][i]}{klam[1][i]}")

            elif nur == "rv":
                out.append(f"{klam[0][i]}{g_darst[1][i]}{klam[1][i]}")

            else:
                if einsetzen is not None and typ == "parameter":
                    out.append(f"{buchst[i]}{klam[0][i]}{g_darst[0][i]}{klam[1][i]}{param[i]}{klam[0][i]}{g_darst[1][i]}{klam[1][i]}")
                else:
                    out.append(f"{buchst[i]}{klam[0][i]}{g_darst[0][i]}{klam[1][i]}{param[i]}{klam[0][i]}{g_darst[1][i]}{klam[1][i]}")

        if print_:
            for item in out:
                cprint(item, color)

        return out


class Punkt:
    """Class für einen Punkt."""

    def __init__(self, inp, buchst="P", pfeil=False):
        std.verify_input(inp, buchst, "punkt")
        std.verify_input(buchst, "Buchstabe", str), std.verify_input(pfeil, "Pfeil", bool)

        self.buchst = buchst
        self.has_pfeil = pfeil
        if pfeil:
            self.pfeil = std.format_prec(buchst, string=True, pfeil=True, nur_pfeil=True)
        else:
            self.pfeil = " " * len(buchst)

        self.dim = len(inp)

        self.P = inp

    def display(self, prec, color=None, print_buchst=True, print_=True):
        std.verify_input(color, "Farbe", "farben_en"), std.verify_input(print_, "print gerade", bool)

        if isinstance(prec, list):
            all(std.verify_input(item, "prec", Number) for item in prec)
        else:
            std.verify_input(prec, "prec", Number)

        out = []

        prec = std.prec_auffüllen(prec, 3)

        P_darst = [std.format_prec(item, prec[i], string=True, string_ausrichtung="mitte") for i, item in enumerate(self.P)]

        if print_buchst:
            buchst = std.format_prec(self.buchst, string=True, pfeil=self.has_pfeil)
        else:
            buchst = ""

        buchst = std.format_prec(buchst, string=True)

        n = 0
        if self.has_pfeil:
            out.append(f"{self.pfeil}")
            n = 1

        out.append(f"{buchst}({P_darst[0]}")

        for j in range(1, self.dim):
            out[n] += f"|{P_darst[j]}"

        out[n] += ")"

        if print_:
            for item in out:
                cprint(item, color)

        return out


class Vektor:
    """Class für einen Punkt."""

    def __init__(self, inp, buchst="v", pfeil=True):
        std.verify_input(inp, buchst, "vektor")
        std.verify_input(buchst, "Buchstabe", str)

        self.buchst = buchst
        self.has_pfeil = pfeil
        if pfeil:
            self.pfeil = std.format_prec(buchst, string=True, pfeil=True, nur_pfeil=True)
        else:
            self.pfeil = " " * len(buchst)

        self.dim = len(inp)

        self.v = inp

    def display(self, prec, color=None, print_buchst=True, print_=True):
        std.verify_input(color, "Farbe", "farben_en"), std.verify_input(print_, "print gerade", bool)

        if isinstance(prec, list):
            all(std.verify_input(item, "prec", Number) for item in prec)
        else:
            std.verify_input(prec, "prec", Number)

        out = []
        klam = std.get_klam(self.dim)
        mitte = int(self.dim / 2)

        if print_buchst:
            buchst = std.format_prec(["", self.buchst], string=True, pfeil=self.has_pfeil)
            i = 2
            while i < self.dim:
                buchst.append("")
                i += 1

            buchst = std.format_prec(buchst, string=True, ausrichtung="links")

            for i in range(self.dim):
                if i == mitte:
                    buchst[i] += " = "
                else:
                    buchst[i] += "   "
        else:
            buchst = ["" for _ in range(self.dim)]

        prec = std.prec_auffüllen(prec, 1)

        v_darst = [std.format_prec(item, prec[i], string=True, string_ausrichtung="mitte") for i, item in enumerate([self.v])]

        for i in range(self.dim):
            out.append(f"{buchst[i]}{klam[0][i]}{v_darst[0][i]}{klam[1][i]}")

        if print_:
            for item in out:
                cprint(item, color)

        return out
