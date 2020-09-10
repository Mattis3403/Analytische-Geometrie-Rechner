import copy
import math
from numbers import Number

import Berechnungen as ber
import StandardLib as std
import classes as cla
from Colored import colored
from Colored import cprint


def skalarprodukt_ohne(g_2, h_2):
    """Berechnet das Standardskalarprodukt von g_2 und h_2 in der Dimension - config"""
    summe = 0
    for i in range(len(g_2)):
        summe += g_2[i] * h_2[i]
    return summe
    # Einzeiler: return sum([g_2[i] * h_2[i] for i in range(dimension())])


def absvec_ohne(vec):
    """Berechnet den Betrag eines gegebenen Vektores in der Dimension - config"""
    return math.sqrt(sum(item ** 2 for item in vec))


def transp_ohne(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def ohne_b_ohne(A, zeilen=True):
    return [transp_ohne(transp_ohne(A)[:-1]) if zeilen else A[:-1]]


def find_non_0_ohne(A):
    prec = std.get_prec("int")
    if type(A[0]) == list:
        A = transp_ohne(A)
        for row in A:
            n = 0
            for item in row:
                if round(item, prec) != 0:
                    return n
                n += 1
        return False

    elif isinstance(A[0], Number):
        n = 0
        for item in A:
            if item != 0:
                return n
            n += 1
        return False
    else:
        err_far = std.get_color("err")
        raise cla.InputError(colored(f"Ich hab ehrlich keine Ahnung was falsch ist. Die Funktion sollte sowieso nicht benutzt werden und keine Ahnung. Hier noch das A:\n{A}", err_far))


def find_NKV_ohne(A, zeilen=True, EKM=False):
    if EKM:
        A_neu = ohne_b_ohne(copy.deepcopy(A))
    else:
        A_neu = A
    if isinstance(A_neu[0], list):
        # Matrix
        if zeilen is False:
            A_neu = transp_ohne(A_neu)
        pos_NKV = list(range(len(A_neu[0])))
        for i in range(len(A_neu)):
            # i = Counter über Zeilen
            n = find_non_0_ohne(A_neu[i])
            if n in pos_NKV:
                pos_NKV.remove(n)

    elif isinstance(A_neu[0], Number):
        n = find_non_0_ohne(A_neu)

        pos_NKV = list(range(len(A_neu)))
        pos_NKV.remove(n)
    return pos_NKV


def skalarprodukt_formel(u, v, prec, dim=3, color=None):
    cprint(f"→   →    ", color)
    cprint(f"u ∘ v = u₁ ∙ v₁ + u₂ ∙ v₂ + u₃ ∙ v₃ ", color)
    return


def absvec(v, prec, color=None):
    summe = sum(item ** 2 for item in v.v)
    wert = math.sqrt(summe)
    v_darst = std.format_prec(v.v, prec, mehrere=False, klammer=True)
    summe_darst = std.format_prec(summe, prec)
    wert_darst = std.format_prec(wert, prec)
    sqrt_1, sqrt_2 = f"√{v_darst[0]}² + {v_darst[1]}²", f"√{summe_darst}"
    if v.dim == 3:
        sqrt_1 += f" + {v_darst[2]}²"

    forma_1 = f"_<{len(sqrt_1)}"
    forma_2 = f"_<{len(sqrt_2)}"

    cprint(f"{' ':{forma_1}}   {' ':{forma_2}}", color)
    cprint(f"{sqrt_1} = {sqrt_2} = {wert_darst}", color)

    return


def lgs(inp, prec, b_len=1, operation="+", zeilen=False, b_berechnen=False, rev=False, print_param_str=True, color=None,
        param_list=None, print_param=True,
        nach_KV_umstellen=False, print_=True, string_ausrichtung=None):
    """

    Parameters
    ----------
    inp                 Darzustellende Werte. Der letzte (b_len) wert wird als b interpretiert
    prec                Anzahl der Nachkommastellen
    b_len               Die länge von b
    operation           Welche Operation angezeigt (und ggf. per b_berechnen berchnet) wird
    zeilen              Soll inp als zeilen interpretiert werden?
    b_berechnen         Soll b berechnet werden
    rev                 Soll b auf der linken Seite stehen?
    print_param_str     Soll bei leeren Strings die Parameter geprinted werden?
    color               In welcher Farbe soll alles angezeigt werden?
    param_list          Welche Parameter sollen angezeigt werden
    print_param         Sollen dei Parameter angezeigt werden
    nach_KV_umstellen   Soll nach den Kopfvariablen (einer Matrix) umgestellt werden?
    print_              Soll der Output angezeigt werden?
    string_ausrichtung  Mit welcher Ausrichtung sollen die str angezeigt werden?

    Returns
    -------
    list von Strings die geprinted werden
    """
    inp = copy.deepcopy(inp)
    if not isinstance(inp[0], list):
        inp = [inp]

    if zeilen is True:
        inp = transp_ohne(inp)
    else:
        pass
    # inp wird in Spaltenform bearbeitet
    if b_berechnen:
        inp.append([])

    prec_1, prec_int = std.get_prec([1, "int"])

    dim_n = len(inp[0])  # dim_n = Anzahl der Zeilen
    dim_m = len(inp)  # dim_m = Anzahl der Spalten

    prec = std.prec_auffüllen(prec, dim_m)

    if print_param:
        if param_list is None:
            param_list = []
            for i in range(1, dim_m):
                param_list.append(f" {std.übersetzung_zahl_param(i)}")

        else:
            for i, item in enumerate(param_list):
                if item == "":
                    continue
                if item[0] != " ":
                    param_list[i] = f" {item}"

        if len(param_list) + 1 < dim_m:
            i = len(param_list) + 1
            while i < dim_m:
                param_list.append(f" {std.übersetzung_zahl_param(i)}")
                i += 1
        param_list.append("")

    else:
        param_list = ["" for _ in range(dim_m)]

    if b_berechnen:
        neu_b = [inp[0][i] if operation in ["+", "-", "/"] else 1 for i in range(dim_n)]

        start = 1 if operation in ["+", "-", "/"] else 0
        for i in range(dim_n):
            for j in range(start, dim_m - 1):
                if operation == "+":
                    neu_b[i] += inp[j][i]

                elif operation == "-":
                    neu_b[i] -= inp[j][i]

                elif operation == "*":
                    neu_b[i] *= inp[j][i]

                elif operation == "/":
                    if round(inp[j][i], prec_int) == 0:
                        if neu_b[i] == 0:
                            neu_b[i] = "*"
                        else:
                            neu_b[i] = 0
                    else:
                        neu_b[i] /= inp[j][i]

        inp[-1] = neu_b

    if nach_KV_umstellen:
        n = find_NKV_ohne(ohne_b_ohne(inp, False), False)

        neu_inp = [inp[i] for i in range(len(inp)) if i not in n]
        neu_param = [param_list[i] for i in range(len(inp)) if i not in n]
        for i in range(len(inp)):
            if i in n:
                neu_inp.append([-inp[i][j] for j in range(dim_n)])
                neu_param.append(param_list[i])

        inp = neu_inp
        param_list = neu_param

        b_len += len(n)

    inp_darst, inp_darst_abs, inp_darst_vorne, inp_darst_klam = [], [], [], []
    if string_ausrichtung is None:
        string_ausrichtung = "rechts"
    for i in range(dim_m):
        inp_darst.append(std.format_prec(inp[i], prec[i], True, string_ausrichtung=string_ausrichtung))
        inp_darst_abs.append(std.format_prec(inp[i], prec[i], absval=True, string_ausrichtung=string_ausrichtung))
        inp_darst_vorne.append(std.format_prec(inp[i], prec[i], vorne=True, string_ausrichtung=string_ausrichtung))
        inp_darst_klam.append(std.format_prec(inp[i], prec[i], klammer=True, string=True, string_ausrichtung=string_ausrichtung))

    if operation == "*":
        nchk = ["∙" for _ in range(dim_n)]
    elif operation == "/":
        nchk = ["/" for _ in range(dim_n)]

    if operation == "-":
        for i in range(dim_n):
            for j in range(1, dim_m - 1):
                inp[j][i] *= -1

    out = []
    for i in range(dim_n):
        # i = Counter über Zeilen
        out.append("")
        if rev:
            out[i] += colored(f"{inp_darst_vorne[-1][i]} = ", color)

        out[i] += colored(f"{inp_darst_vorne[0][i]}{param_list[0] if print_param_str or inp_darst_vorne[0][i].strip() else ''}",
                          color)
        for j in range(1, len(inp)):
            # j = Counter über die Spalten
            if operation in ["+", "-"]:
                nchk = std.negcheck(inp[j][i])

            if j >= dim_m - b_len:
                if j == dim_m - b_len:
                    if not rev:
                        out[i] += colored(f" = {inp_darst_vorne[j][i]}", color)
                else:
                    if nach_KV_umstellen:
                        if operation in ["+", "/"]:
                            out[i] += colored(
                                f" {nchk[0]} {inp_darst_abs[j][i]}{param_list[j] if print_param_str or inp_darst_abs[j][i].strip() else ''}",
                                color)
                        else:
                            out[i] += colored(
                                f" {nchk[0]} {inp_darst_abs[j][i]}{param_list[j] if print_param_str or inp_darst_abs[j][i].strip() else ''}",
                                color)

                    else:
                        if operation in ["+", "/"]:
                            out[i] += colored(
                                f" {nchk[0]} {inp_darst_klam[j][i]}{param_list[j] if print_param_str or inp_darst_klam[j][i].strip() else ''}",
                                color)
                        else:
                            out[i] += colored(
                                f" {nchk[0]} {inp_darst_abs[j][i]}{param_list[j] if print_param_str or inp_darst_abs[j][i].strip() else ''}",
                                color)

            else:
                if operation in ["*", "/"]:
                    out[i] += colored(
                        f" {nchk[0]} {inp_darst_klam[j][i]}{param_list[j] if print_param_str or inp_darst_klam[j][i].strip() else ''}",
                        color)
                else:
                    out[i] += colored(
                        f" {nchk[0]} {inp_darst_abs[j][i]}{param_list[j] if print_param_str or inp_darst_abs[j][i].strip() else ''}",
                        color)

    if print_:
        for item in out:
            print(item)

    return out


def conv_norm_formel(u, v, color=None, print_=True):
    out = [f"{u.pfeil}   {v.pfeil}   ⎛{u.buchst}₂ ∙ {v.buchst}₃ - {u.buchst}₃ ∙ {v.buchst}₂⎞",
           f"{u.buchst} × {v.buchst} = ⎜{u.buchst}₃ ∙ {v.buchst}₁ - {u.buchst}₁ ∙ {v.buchst}₃⎟",
           f"{' ' * (len(u.buchst) + len(v.buchst))}      ⎝{u.buchst}₁ ∙ {v.buchst}₂ - {u.buchst}₂ ∙ {v.buchst}₁⎠"]

    if print_:
        for item in out:
            cprint(item, color)

    return out


def conv_norm0_formel(n, prec, color=None, print_=True):
    bruch = std.format_prec(["1", f"|{n.buchst}|"], mehrere=False, bruch=True, string=True, ausrichtung="mitte")
    out = ["Die allgemeine Formel für den Normaleneinheitsvektor lautet:\n",
           f"{' ' * len(f'{n.buchst}₀ = ')}{n.pfeil}   {bruch[0]}",
           f"{n.buchst}₀ = {n.buchst} ∙ {bruch[1]}"]
    if n.has_pfeil:
        out.append(f"{' ' * len(f'{n.buchst}₀ = ')}{' ' * len(n.buchst)}     {n.pfeil}")
    out.append(f"{' ' * len(f'{n.buchst}₀ = ')}{' ' * len(n.buchst)}   {bruch[2]}")

    if print_:
        for item in out:
            cprint(item, color)

    return out


def gauss_overset(zeile_1, zeile_2, operation, div=None, bruch_zahl_1=None, bruch_zahl_2=None):
    """Gibt den Pfeil vor dem Gauss Algorithmus wieder"""
    bruch = std.get_divers("bruch")
    prec = std.get_prec(1)

    if operation in ["+", "-"]:
        operation = "+" if round(eval(f"{operation}{div}"), ) >= 0 else "-"
        div = std.format_prec(div, prec, absval=True)

        if bruch_zahl_1 is None or bruch_zahl_2 is None:
            out = f"{std.roman(zeile_1)}. {operation} {div} ∙ {std.roman(zeile_2)}."

        else:
            pfeil = std.format_prec(["", f"{std.roman(zeile_1)}. {operation} ", ""], 1, string=True)
            bruch_darst = std.format_prec([bruch_zahl_1, bruch_zahl_2], bruch=True, absval=True)

            out = []

            for a, b in zip(pfeil, bruch_darst):
                out.append(a + b)

            out = [f"{item} ∙ {std.roman(zeile_2)}." if i == 1 else f"{item}{' ' * (len(std.roman(zeile_2)) + 4)}" for i, item in enumerate(out)]

    elif operation == "*":
        if bruch_zahl_1 is None or bruch_zahl_2 is None:
            div = std.format_prec(div, prec, klammer=True)
            out = f"{std.roman(zeile_2)}. ∙ {div}"

        else:
            pfeil = std.format_prec(["", f"{std.roman(zeile_1)}. ∙ ", ""], 1, string=True)

            bruch_zahl_1 = (-1 if div < 0 else 1) * abs(bruch_zahl_1)
            bruch_darst = std.format_prec([bruch_zahl_1, abs(bruch_zahl_2)], bruch=True, mehrere=True)

            out = []
            for a, b in zip(pfeil, bruch_darst):
                out.append(a + b)

            out = [f"{item} ∙ {std.roman(zeile_2)}." if i == 1 else f"{item}{' ' * (len(std.roman(zeile_2)) + 4)}" for i, item in
                   enumerate(out)]

    elif operation == "tausch":
        out = [f"{std.roman(zeile_1)}. <─> {std.roman(zeile_2)}."]

    return out


def lgs_lösung(inp, prec, zeilen=True, color=None, param_list=None, print_=True):

    if isinstance(inp, (list, tuple)):
        if inp[0] == "eind":
            spez_lsg = True
            inp = inp[1:]

        elif inp[0] == "unend":
            if any(row[0] == "spez" for row in inp[1]):
                spez_lsg = True
            else:
                spez_lsg = False

            if any(isinstance(row[0], str) for row in inp[1]):
                param_list = []

            for row in inp[1]:
                if isinstance(row[0], str) and row[0] != "spez":
                    param_list.append(row[0])

            inp = [item[1:] for item in inp[1]]

        elif inp[0] == "keine":
            cprint("L = ∅", color)
            return

    if not isinstance(inp[0], (list, tuple)):
        inp = [inp]

    if zeilen is True:
        inp = transp_ohne(inp)

    # inp wird in Spaltenform bearbeitet

    prec_1, prec_int = std.get_prec([1, "int"])

    dim_n = len(inp[0])  # dim_n = Anzahl der Zeilen
    dim_m = len(inp)  # dim_m = Anzahl der Spalten

    mitte = int(dim_n / 2)

    prec = std.prec_auffüllen(prec, dim_m)

    if param_list is None:
        param_list = []
        for i in range(1, dim_m):
            param_list.append(f" {std.übersetzung_zahl_param(i)}")

    else:
        for i, item in enumerate(param_list):
            if item == "":
                continue
            if item[0] != " ":
                param_list[i] = f" {item}"

    if len(param_list) + 1 < dim_m:
        i = len(param_list) + 1
        while i < dim_m:
            param_list.append(f" {std.übersetzung_zahl_param(i)}")
            i += 1

    if spez_lsg:
        param_list.append("")

    klam_r, klam_g = std.get_klam(dim_n, "r"), std.get_klam(dim_n, "g")

    inp_darst = [std.format_prec(inp[i], prec_1) for i in range(dim_m)]

    # Strings für Darstellung:
    L_str = std.format_prec(["L = " if i == mitte else "" for i in range(dim_n)], prec_1, string=True)
    param_list_str_1 = [std.format_prec([f"{param_list[i]} ∙ " if j == mitte else "" for j in range(dim_n)], prec_1, string=True)
                        for i in range(len(param_list))]
    param_str = ""
    for i, item in enumerate(param_list):
        if i == 0:
            param_str = item.strip()
        elif item:
            param_str += f", {item.strip()}"

    if param_list:
        param_str += f" ∈ ℝ"

    param_list_str_2 = std.format_prec([param_str if _ == mitte else "" for _ in range(dim_n)], string=True)

    plus_str = std.format_prec([f" +" if j == mitte else "" for j in range(dim_n)], string=True)
    strich = [" │ " for i in range(dim_n)]

    out = []
    if spez_lsg:
        anfang = 1
    else:
        anfang = 0

    for i in range(dim_n):
        out.append(f"{L_str[i]}{klam_g[0][i]}")
        if spez_lsg:
            out[i] += f" {klam_r[0][i]}{inp_darst[0][i]}{klam_r[1][i]}"

        for j in range(anfang, dim_m):
            out[i] += f"{plus_str[i] if spez_lsg or j != anfang else ''}{param_list_str_1[j - 1 if spez_lsg else j][i]}{klam_r[0][i]}{inp_darst[j][i]}{klam_r[1][i]}"

        if any(param_list):
            out[i] += f"{strich[i]}{param_list_str_2[i]}"

        out[i] += f" {klam_g[1][i]}"

    if print_:
        for item in out:
            cprint(item, color)

    return out


def schnittwinkel_formel(inp_1, inp_2, typ=None, print_=True, ausrechnen=False, umstellen=False, winkel="α", color=None):
    buchst = [None, None]
    if typ is None:
        typ = [None, None]

    if ausrechnen is True:
        ausrechnen = "F"

    # Buchstaben Parsen
    if isinstance(inp_1, cla.Gerade):
        buchst[0] = inp_1.param
        typ[0] = "gerade"

    elif isinstance(inp_1, cla.Ebene):
        if typ[1] == "ebene" or isinstance(inp_2, cla.Ebene):
            buchst[0] = "n₁"
        else:
            buchst[0] = "n"

    else:
        if typ[0] == "gerade":
            buchst[0] = "r"
        elif typ[0] == "ebene":
            if typ[1] == "ebene" or isinstance(inp_2, cla.Ebene):
                buchst[0] = "n₁"
            else:
                buchst[0] = "n"

    if isinstance(inp_2, cla.Gerade):
        buchst[1] = inp_2.param
        typ[1] = "gerade"

    elif isinstance(inp_2, cla.Ebene):
        if typ[0] == "ebene":
            buchst[1] = "n₂"
        else:
            buchst[1] = "n"

    else:
        if typ[1] == "gerade":
            buchst[1] = "r"
        elif typ[1] == "ebene":
            if typ[0] == "ebene":
                buchst[1] = "n₁"
            else:
                buchst[1] = "n"

    if ausrechnen:
        prec, prec_2 = std.get_prec([1, 2])

        if typ[0] == "gerade":
            v1 = inp_1.rv.copy()
            inp_1_darst = inp_1.display(prec=prec, nur="rv", print_=False)
        else:
            v1 = inp_1.nv.copy()
            inp_1_darst = inp_1.display(prec=prec, nur="nv", darst="norm", print_=False)

        if typ[1] == "gerade":
            v2 = inp_2.rv.copy()
            inp_2_darst = inp_2.display(prec=prec, nur="rv", print_=False)
        else:
            v2 = inp_2.nv.copy()
            inp_2_darst = inp_2.display(prec=prec, nur="nv", darst="norm", print_=False)

        if "bruch" in ausrechnen:
            bruch_darst = std.format_prec(abs(ber.skalarprodukt(v1, v2)) / (ber.absvec(v1) * ber.absvec(v2)), prec_2, liste=True)

        else:
            if "oben" in ausrechnen:
                forma_list = [f"|{ber.skalarprodukt(v1, v2)}|"]
                if "unten" not in ausrechnen:
                    forma_list.insert(0, "")

                bruch_oben = std.format_prec(forma_list, prec, liste=True)

            else:
                bruch_oben = []
                offen_kringel = ["∘" if i == int(inp_1.dim / 2) else " " for i in range(inp_1.dim)]

                for i in range(inp_1.dim):
                    bruch_oben.append(f"┃ {inp_1_darst[i]} {offen_kringel[i]} {inp_2_darst[i]} ┃")

            if "unten" in ausrechnen:
                forma_list = [ber.absvec(v1) * ber.absvec(v2)]
                if "oben" not in ausrechnen:
                    forma_list.append("")
                    forma_list.append("")

                bruch_unten = std.format_prec(forma_list, prec, liste=True)

            else:
                bruch_unten = []
                zu_kringel = ["∙" if i == int(inp_1.dim / 2) else " " for i in range(inp_1.dim)]

                for i in range(inp_1.dim):
                    bruch_unten.append(f"┃{inp_1_darst[i]}┃ {zu_kringel[i]} ┃{inp_2_darst[i]}┃")

            bruch_darst = std.format_prec(bruch_oben + bruch_unten, bruch=True, mehrere=False, string=True, ausrichtung="mitte")

    else:
        pfeile = [std.get_pfeil(len(_)) for _ in buchst]
        bruch = [f" {pfeile[0]}   {pfeile[1]}", f"|{buchst[0]} ∘ {buchst[1]}|",
                 f" {pfeile[0]}     {pfeile[1]}", f"|{buchst[0]}| ∙ |{buchst[1]}|"]
        bruch_darst = std.format_prec(bruch, bruch=True, mehrere=False, string=True, ausrichtung="mitte")

    formel = "sin" if typ.count("gerade") == 1 and typ.count("ebene") == 1 else "cos"

    formel_darst = []
    mitte = int(len(bruch_darst) / 2)
    for i in range(len(bruch_darst)):
        if umstellen:
            st = f"{winkel} = {formel}⁻¹ "
            if i == mitte:
                formel_darst.append(st)
            else:
                formel_darst.append(f" "*len(st))

        else:
            st = f"{formel}({winkel}) = "
            if i == mitte:
                formel_darst.append(st)
            else:
                formel_darst.append(" "*len(st))

    out = []
    if umstellen:
        klam = std.get_klam(inp_1.dim if "bruch" not in ausrechnen else 1)
        for fo, kl0, da, kl1 in zip(formel_darst, klam[0], bruch_darst, klam[1]):
            out.append(fo + kl0 + da + kl1)
    else:
        for a, b in zip(formel_darst, bruch_darst):
            out.append(a + b)

    if print_:
        for _ in out:
            cprint(_, color)

    return out


def lgs_probe(A_1, A_2, x, b, prec, nummer=2, color=None, print_=True):
    prec_int = std.get_prec("int")
    A_1_darst = std.format_prec(A_1[nummer], prec, mehrere=False)
    A_2_darst = std.format_prec(A_2[nummer], prec, mehrere=False, absval=True)
    x_darst = std.format_prec(x, prec, mehrere=False, klammer=True)
    b_darst = std.format_prec(b[nummer], prec, mehrere=False)
    nchk = std.negcheck(A_2[nummer])

    out = [f"Einsetzen in {std.roman(nummer + 1)}:\n", f"{std.roman(nummer + 1)}.  {A_1_darst} ∙ {x_darst[0]} {nchk[0]} {A_2_darst} ∙ {x_darst[1]} = {b_darst}"]

    A_1_darst = std.format_prec(A_1[nummer] * x[0], prec, mehrere=False)
    A_2_darst = std.format_prec(A_2[nummer] * x[1], prec, mehrere=False, absval=True)
    b_darst = std.format_prec(b[nummer], prec, mehrere=False)
    nchk = std.negcheck(A_2[nummer] * x[1])
    out.append("\n")
    out.append("Vereinfachen:\n")
    out.append(f"{std.roman(nummer + 1)}.  {A_1_darst} {nchk[0]} {A_2_darst} = {b_darst}")

    wert = A_1[nummer] * x[0] + A_2[nummer] * x[1]
    wert_darst = std.format_prec(wert, prec)

    if round(wert, prec_int) == round(b[nummer], prec_int):
        zeichen = "="
    else:
        zeichen = "≠"
    out.append("\n")
    out.append("Zusammenfassen:\n")
    out.append(colored(f"{std.roman(nummer + 1)}.  {wert_darst} {zeichen} {b_darst}", color))

    if print_:
        for item in out:
            print(item)

    return out
