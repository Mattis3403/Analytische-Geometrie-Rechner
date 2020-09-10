import copy
import math
import time
from collections import deque
from numbers import Number

import Display as dis
import StandardLib as std
import classes as cla
from Colored import colored
from Colored import cprint


def skalarprodukt(u, v, rechenweg=False, intro=False, end=False, ende=False, buchst=None):
    """

    Parameters
    ----------
    u           Entweder cla.Vektor oder Liste
    v           Entweder cla.Vektor oder Liste - Vektoren aus denen das Skalarprodukt gebildet wird
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für u und v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Skalarprodukt aus u und v - Number
    """

    std.verify_input(u, "u", "vektor"), std.verify_input(v, "v", "vektor")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst = std.buchstabe_auffüllen(buchst, ["u", "v"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)
    if rechenweg != "force" and rechenweg is not False:
        rechenweg = std.get_lsg("rweg skalar")

    if not isinstance(u, cla.Vektor):
        u = cla.Vektor(u, buchst=buchst[0])
    if not isinstance(v, cla.Vektor):
        v = cla.Vektor(v, buchst=buchst[1])

    skp = sum([u.v[i] * v.v[i] for i in range(u.dim)])

    if rechenweg:
        if intro:
            cprint(f"Skalarprodukt von {u.buchst} und {v.buchst} berechnen:\n", abs_far)
        print("Die allgemeine Formel für das Skalarprodukt lautet:\n")
        dis.skalarprodukt_formel(u, v, prec)
        print("\n")
        print("Das heißt in diesem Fall:\n")
        dis.lgs([u.v, v.v], prec, operation="*", b_berechnen=True, print_param=False)
        print("\n")
        dis.lgs([u.v[i] * v.v[i] for i in range(u.dim)], prec, operation="+", zeilen=True, b_berechnen=True, print_param=False)
        if end:
            print("\n")

    if end:
        skp_darst = std.format_prec(skp, prec)
        print(colored(f"Das Skalarprodukt beträgt {skp_darst}", end_far))

    return skp


def absvec(v, rechenweg=False, intro=False, end=False, ende=False, buchst=None):
    """

    Parameters
    ----------
    v           Der Vektor von dem der Betrag berechnet wird. Entweder als cla.Vektor oder Liste
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Betrag von dem Vektor - Number
    """
    std.verify_input(v, "v", "vektor")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    if rechenweg != "force" and rechenweg is not False:
        rechenweg = std.get_lsg("rweg absvec")

    buchst = std.buchstabe_auffüllen(buchst, "v")
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)
    prec_2 = std.get_prec(2)

    if not isinstance(v, cla.Vektor):
        v = cla.Vektor(v, buchst=buchst[0])

    wert = math.sqrt(sum(item ** 2 for item in v.v))

    if end:
        wert_darst = std.format_prec(wert, prec_2)
    if rechenweg:
        if intro:
            if v.has_pfeil:
                cprint(" " * len("Betrag des Vektors " + v.pfeil))
            cprint(f"Betrag des Vektors {v.buchst} berechnen:", abs_far)

        dis.absvec(v, prec_2)

    if end:
        if rechenweg:
            if v.has_pfeil:
                print()
            else:
                print("\n")
        if v.has_pfeil:
            cprint(" " * len("Der Betrag von ") + v.pfeil, end_far)
        cprint(f"Der Betrag von {v.buchst} beträgt {wert_darst}LE", end_far)

    return wert


def vektor_zwei_punkte(P, Q, rechenweg=False, intro=False, end=False, ende=False, buchst=None, return_list=False):
    """

    Parameters
    ----------
    P           Erster Punkt enweder cla.Punkt oder Liste
    Q           Zweiter Punkt entweder cla.Punkt oder Liste
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)
    return_list returned den Vektor als Listenform falls True

    Returns
    -------
    Vektor aus P und Q - list / cla.Vektor
    """
    std.verify_input(P, "P", "punkt"), std.verify_input(Q, "Q", "punkt")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst = std.buchstabe_auffüllen(buchst, ["P", "Q"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if rechenweg != "force" and rechenweg is not False:
        rechenweg = std.get_lsg("rweg vektor")

    if not isinstance(P, cla.Punkt):
        P = cla.Punkt(P, buchst=buchst[0])
    if not isinstance(Q, cla.Punkt):
        Q = cla.Punkt(Q, buchst=buchst[1])

    vektor = cla.Vektor([Q.P[i] - P.P[i] for i in range(3)], buchst=P.buchst + Q.buchst)

    if rechenweg:
        if intro:
            cprint(f"Vektor aus zwei Punkten {P.buchst} und {Q.buchst} berechnen:\n", abs_far)
        pfeil = std.format_prec([P.buchst + Q.buchst], string=True, pfeil=True, nur_pfeil=True)
        print(f"{pfeil}                  {Q.pfeil}   {P.pfeil}")
        print(f"{P.buchst + Q.buchst} berechnen, dafür {Q.buchst} - {P.buchst} komponentenweise subtrahieren:\n")
        dis.lgs([Q.P, P.P], prec, operation="-", b_berechnen=True, print_param=False)
        if end:
            print("\n")
            cprint("Daraus ergibt sich der Vektor:\n", end_far)

    if end:
        vektor.display(prec, end_far)

    if return_list:
        vektor = vektor.v

    return vektor


def gerade_zwei_punkte(P, Q, rechenweg=False, intro=False, end=False, ende=False, buchst=None, param=None, return_list=False):
    """

    Parameters
    ----------
    P           Erster Punkt enweder cla.Punkt oder Liste
    Q           Zweiter Punkt entweder cla.Punkt oder Liste
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)
    return_list returned die Gerade als Listenform falls True

    Returns
    -------
    Gerade aus P und Q - list / cla.Gerade
    """
    std.verify_input(P, "P", "punkt"), std.verify_input(Q, "Q", "punkt")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst, param = std.buchstabe_auffüllen(buchst, "g"), std.buchstabe_auffüllen(param, "r")
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if not isinstance(P, cla.Punkt):
        P = cla.Punkt(P)
    if not isinstance(Q, cla.Punkt):
        Q = cla.Punkt(Q, buchst="Q")

    gerade = cla.Gerade([P.P, [Q.P[i] - P.P[i] for i in range(P.dim)]], buchst=buchst[0], param=param[0])

    if rechenweg:
        pfeil = std.format_prec(P.buchst + Q.buchst, string=True, pfeil=True, nur_pfeil=True)
        if intro:
            cprint("Gerade aus zwei Punkten berechnen:\n", abs_far)
        print(f"{P.pfeil}                  {pfeil}")
        print(f"{P.buchst} als Stützvektor, {P.buchst + Q.buchst} als Richtungsvektor:\n")
        vektor_zwei_punkte(P, Q, True, end=True)
        if end:
            print("\n")
            print("Daraus ergibt sich:\n")

    if end:
        gerade.display(prec, end_far)

    if return_list:
        gerade = [gerade.sv, gerade.rv]

    return gerade


def ebene_drei_punkte(P, Q, T, rechenweg=False, intro=False, end=False, ende=False, buchst=None, param=None, return_list=False):
    """

    Parameters
    ----------
    P           Erster Punkt enweder cla.Punkt oder Liste
    Q           Zweiter Punkt entweder cla.Punkt oder Liste
    T           Dritter Punkt entweder cla.Punkt oder Liste
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)
    return_list returned die Ebene als Listenform falls True

    Returns
    -------
    Ebene aus P, Q und T - list / cla.Ebene

    """
    std.verify_input(P, "P", "punkt"), std.verify_input(Q, "Q", "punkt"), std.verify_input(T, "T", "punkt")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst, param = std.buchstabe_auffüllen(buchst, "E"), std.buchstabe_auffüllen(param, ["s", "t"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if not isinstance(P, cla.Punkt):
        P = cla.Punkt(P)
    if not isinstance(Q, cla.Punkt):
        Q = cla.Punkt(Q, buchst="Q")
    if not isinstance(T, cla.Punkt):
        T = cla.Punkt(T, buchst="T")

    pq = cla.Vektor([Q.P[i] - P.P[i] for i in range(P.dim)], buchst=P.buchst + Q.buchst)
    pt = cla.Vektor([T.P[i] - P.P[i] for i in range(P.dim)], buchst=P.buchst + T.buchst)

    ebene = cla.Ebene([P.P, pq.v, pt.v], buchst=buchst[0], param=param)

    if rechenweg:
        if intro:
            cprint("Ebene aus drei Punkten berechnen:\n", abs_far)
        print(f"{P.pfeil}                  {pq.pfeil}                                {pt.pfeil}")
        print(f"{P.buchst} als Stützvektor, {pq.buchst} als erster Richtungsvektor und {pt.buchst} als zweiter Richtungsvektor:\n")
        vektor_zwei_punkte(P, Q, True, end=True)
        print("\n")
        vektor_zwei_punkte(P, T, True, end=True)
        if end:
            print("\n")
            print("Daraus ergibt sich:\n")

    if end:
        ebene.display(prec, end_far)

    if return_list:
        ebene = [ebene.sv, ebene.rv_1, ebene.rv_2]

    return ebene


def conv_norm(u, v, rechenweg=False, intro=False, end=False, ende=False, buchst=None, return_list=False):
    """

    Parameters
    ----------
    u           Erster Vektor - entweder als Liste oder cla.Vektor
    v           Zweiter Vektor - entweder als Liste oder cla.Vektor
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)
    return_list returned den Vektor als Listenform falls True

    Returns
    -------
    Normalenvektor aus u und v - list / cla.Vektor
    """
    std.verify_input(u, "u", "vektor"), std.verify_input(v, "v", "vektor")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst = std.buchstabe_auffüllen(buchst, ["u", "v", "n"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)
    if rechenweg != "force" and rechenweg is not False:
        rechenweg = std.get_lsg("rweg norm")

    if not isinstance(u, cla.Vektor):
        u = cla.Vektor(u, buchst=buchst[0])
    if not isinstance(v, cla.Vektor):
        v = cla.Vektor(v, buchst=buchst[1])

    n = cla.Vektor([u.v[(i + 1) % 3] * v.v[(i + 2) % 3] - u.v[(i + 2) % 3] * v.v[(i + 1) % 3] for i in range(3)], buchst=buchst[2])

    if rechenweg:
        if intro:
            cprint(f"Normalenvektor aus {u.buchst} und {v.buchst} berechnen:\n", abs_far)
        print("Die allgemeine Formel für den Normalenvektor lautet:\n")
        dis.conv_norm_formel(u, v)
        print("\n")
        print("In diesem Fall heißt das:\n")
        u_hilf_1, u_hilf_2 = deque(u.v), deque([-item for item in u.v])
        v_hilf_1, v_hilf_2 = deque(v.v), deque(v.v)
        u_hilf_1.rotate(-1), u_hilf_2.rotate(-2)
        v_hilf_1.rotate(1), v_hilf_2.rotate(2)

        u_hilf_1, u_hilf_2 = list(u_hilf_1), list(u_hilf_2)
        v_hilf_1, v_hilf_2 = list(v_hilf_1), list(v_hilf_2)

        dis_1 = dis.lgs([u_hilf_1, v_hilf_1], prec, b_len=0, print_param=False, operation="*", print_=False)
        dis_2 = dis.lgs([[abs(item) for item in u_hilf_2], v_hilf_2], prec, b_len=0, print_param=False, operation="*",
                        print_=False)

        nchk = std.negcheck(u_hilf_2)
        klam = std.get_klam(u.dim)
        mitte = int(u.dim / 2)
        buchst_darst = std.format_prec([buchst[2] if i == mitte else "" for i in range(u.dim)], string=True, pfeil=True)
        for i in range(u.dim):
            if i == mitte:
                buchst_darst[i] += " = "
            else:
                buchst_darst[i] += "   "
        for i, (a, b) in enumerate(zip(dis_1, dis_2)):
            print(f"{buchst_darst[i]}{klam[0][i]}{a} {nchk[i]} {b}{klam[1][i]}")

        if end:
            print("\n")
            print("Vereinfachen:\n")

    if end:
        n.display(prec, end_far)

    if return_list:
        n = n.v

    return n


def conv_norm0(u, v, rechenweg=False, u_as_nv=False, intro=False, end=False, ende=False, buchst=None, return_list=False):
    """

    Parameters
    ----------
    u           Erster Vektor - entweder als Liste oder cla.Vektor
    v           Zweiter Vektor - entweder als Liste oder cla.Vektor
    rechenweg   Soll ein Rechenweg angezeigt werden
    u_as_nv     Soll u als Normalenvektor behandelt werden? - Ohne conv_norm sondern nur normieren
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)
    return_list returned den Vektor als Listenform falls True

    Returns
    -------
    Normaleneinheitsvektor aus u und v - list / cla.Vektor
    """
    std.verify_input(u, "u", "vektor"), std.verify_input(v, "v", "vektor")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst = std.buchstabe_auffüllen(buchst, ["u", "v", "n", "n₀"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)
    if rechenweg != "force" and rechenweg is not False:
        rechenweg = std.get_lsg("rweg norm0")
    prec_3 = std.get_prec(3)

    if not isinstance(u, cla.Vektor):
        u = cla.Vektor(u, buchst=buchst[0])
    if not isinstance(v, cla.Vektor):
        v = cla.Vektor(v, buchst=buchst[1])

    if u_as_nv:
        n = copy.deepcopy(u)
        n.buchst = "n"
    else:
        n = conv_norm(u, v, end=False, buchst=buchst[2])
    absval = absvec(n, False, end=False)
    n0 = cla.Vektor([item * 1 / absval for item in n.v], buchst=buchst[3])
    if rechenweg:
        if intro:
            cprint("Normaleneinheitsvektor berechnen:\n", abs_far)
        dis.conv_norm0_formel(n, prec)
        print("\n")
        if not u_as_nv:
            cprint("Dafür wird der Normalenvektor benötigt:\n", abs_far)
            conv_norm(u, v, True, end=True, buchst=buchst)
            print("\n")
        print("Betrag berechnen:\n")
        absvec(n, True, end=True, buchst=buchst)
        print("\n")
        print("Einsetzen:\n")

        n_darst, n0_darst = n.display(prec, print_buchst=False, print_=False), n0.display(prec_3, print_buchst=False, print_=False)
        mal, gleich = std.format_prec(["", "∙", ""], string=True), std.format_prec(["", "=", ""], string=True)
        bruch = std.format_prec(["1", absval], prec, ausrichtung="mitte", string=True, mehrere=False, bruch=True)
        for i in range(n0.dim):
            print(f"{n_darst[i]} {mal[i]} {bruch[i]} {gleich[i]} {n0_darst[i]}")

        if end:
            print("\n")
            print("Daraus ergibt sich:\n")

    if end:
        n0.display(prec_3, end_far)

    if return_list:
        n0 = n0.v

    return n0


def linear_abhangig(u, v, rechenweg=False, null=False, intro=False, end=False, ende=False, buchst=None):
    """

    Parameters
    ----------
    u           Erster Vektor - list / cla.Vektor
    v           Zweiter Vektor - list / cla.Vektor
    rechenweg   Soll ein Rechenweg angezeigt werden
    null        Soll ein volles Nullergebnis als Linear unabhängig (True) oder abhängig (False) gewertet werden?
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Ob die Vektoren u und v linear abhängig sind - bool
    """
    std.verify_input(u, "u", "vektor"), std.verify_input(v, "v", "vektor")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst = std.buchstabe_auffüllen(buchst, ["u", "v", "μ"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)
    if rechenweg != "force" and rechenweg is not False:
        rechenweg = std.get_lsg("rweg lin un")

    if not isinstance(u, cla.Vektor):
        u = cla.Vektor(u, buchst=buchst[0])
    if not isinstance(v, cla.Vektor):
        v = cla.Vektor(v, buchst=buchst[1])

    param = []
    for i in range(u.dim):
        if u.v[i] == 0 and v.v[i] == 0:
            param.append("*")

        elif round(u.v[i], prec_int) == 0 or round(v.v[i], prec_int) == 0:
            param.append(0)

        else:
            param.append(v.v[i] / u.v[i])

    for item in param:
        if isinstance(item, Number):
            wert = item
            break
    else:
        param = []
        wert = 1

    check = all(round(item, prec_int) == round(wert, prec_int) for item in param if isinstance(item, Number)) and (round(wert, prec_int) != 0 or null)
    if rechenweg:
        if intro:
            cprint("Festellen der Linearen abhängigkeit zweier Vektoren:\n", abs_far)
        print(f"Um den Paramemter {buchst[2]} herauszufinden muss man zeilenweise den zweiten Vektor durch den ersten teilen:\n")
        dis.lgs([v.v, u.v], prec, operation="/", b_berechnen=True, print_param=False, string_ausrichtung="mitte")
        if param.count("*") > 0 or param == []:
            print()
            print('Der Parameter "*" bedeutet, dass es jeder beliebige Parameter sein kann')

    if end:
        print("\n")
        if all(round(item, prec_int) == 0 for item in param if isinstance(item, Number)):
            if null:
                cprint("Die Parameter sind alle Null. In diesem Fall wird dies als Wahr gewertet und die ", end_far, end="")
                cprint("Vektoren linear abhängig", end_far)
            else:
                cprint("Die Parameter sind alle Null. In diesem Fall wird dies als Falsch gewertet und die ", end_far, end="")
                cprint("Vektoren linear abhängig", end_far)

        elif check:
            cprint("Die Parameterwerte sind gleich. Damit sind die Vektoren linear abhängig", end_far)
        else:
            cprint("Die Parameterwerte sind nicht gleich. Damit sind die Vektoren nicht linear abhängig", end_far)

    return check


def punktprobe_pg(P, g, rechenweg=False, intro=False, end=False, ende=False, buchst=None):
    """

    Parameters
    ----------
    P           Der Punkt - list / cla.Punkt
    g           Die Gerade - list / cla.Gerade
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Ob der Punkt auf der Geraden liegt - bool
    """
    std.verify_input(P, "P", ("vektor", "punkt")), std.verify_input(g, "g", "gerade")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst = std.buchstabe_auffüllen(buchst, ["P", "g", "r"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if isinstance(P, cla.Punkt):
        P = cla.Vektor(P.P, buchst=P.buchst, pfeil=P.pfeil)

    if not isinstance(P, cla.Vektor):
        P = cla.Vektor(P, buchst=buchst[0], pfeil=False)
    if not isinstance(g, cla.Gerade):
        g = cla.Gerade(g, buchst=buchst[1])

    dim = P.dim

    rv = cla.Vektor(g.rv)
    diff = cla.Vektor([P.v[i] - g.sv[i] for i in range(dim)])

    check = linear_abhangig(g.rv, diff, null=True)

    if rechenweg:
        if intro:
            cprint(f"Punktprobe von einer Geraden {g.buchst} und einem Punkt {P.buchst}:\n", abs_far)
        print("Als erstes Punkt und Gerade gleichstellen:\n")
        P_darst = P.display(prec, print_=False, print_buchst=False)
        g_darst = g.display(prec, print_=False, print_buchst=False)
        rv_darst = rv.display(prec, print_=False, print_buchst=False)
        diff_darst = diff.display(prec, print_=False, print_buchst=False)

        param = std.format_prec([f"{buchst[2]} ∙" if i == 1 else "" for i in range(dim)], string=True)
        gleich = std.format_prec(["=" if i == 1 else "" for i in range(dim)], string=True)

        for i in range(dim):
            print(f"{g_darst[i]} {gleich[i]} {P_darst[i]}")

        print("\n")
        print("Jetzt den Stützvektor von der Geraden von dem Punkt abziehen:\n")
        for i in range(dim):
            cprint(f"{param[i]} {rv_darst[i]} {gleich[i]} {diff_darst[i]}", zwi_far)

        print("\n")
        cprint("Jetzt auf lineare Abhängigkeit überprüfen:\n", abs_far)
        linear_abhangig(g.rv, diff, True, null=True, end=True, buchst=buchst)

    if end:
        print("\n")
        if check:
            cprint("Da eine lineare Abhängigkeit vorliegt, liegt der Punkt auf der Geraden", end_far)
        else:
            cprint("Da keine lineare Abhängigkeit vorliegt, liegt der Punkt nicht auf der Geraden", end_far)

    return check


def punktprobe_pE(P, E, rechenweg=False, lsgweg="koor", intro=False, end=False, ende=False, buchst=None):
    """

    Parameters
    ----------
    P           Der Punkt - list / cla.Punkt
    E           Die Ebene - list / cla.Ebene
    rechenweg   Soll ein Rechenweg angezeigt werden
    lsgweg      Welcher Lösungsweg soll genommen werden - gdw "force ..." - "lgs" / "koor"
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Ob der Puntk in der Ebene liegt - bool
    """
    std.verify_input(P, "P", ("punkt", "vektor")), std.verify_input(E, "E", "ebene")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    buchst = std.buchstabe_auffüllen(buchst, ["P", "E", "s", "t"])
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if "force" in lsgweg:
        lsgweg = lsgweg.replace("force", "").strip()
    else:
        lsgweg = std.get_lsg("lsg punktprobe p e")
        if lsgweg not in ["lgs", "koor", "passend"]:
            err_far = std.get_color("err")
            raise cla.InputError(colored(f'Der Lösungsweg war nicht in den Vorgegebenen Typen. Das kann auf einen Fehler in der Konfiguration hindeuten ["lgs", "koor", "passend"]:\n{lsgweg}', err_far))
        if lsgweg == "passend":
            if E.darst == "para":
                lsgweg = "lgs"
            else:
                lsgweg = "koor"

    if isinstance(P, cla.Punkt):
        P = cla.Vektor(P.P, buchst=P.buchst, pfeil=bool(P.pfeil))

    if not isinstance(P, cla.Vektor):
        P = cla.Vektor(P, buchst=buchst[0], pfeil=False)
    if not isinstance(E, cla.Ebene):
        E = cla.Ebene(E, buchst=buchst[1], param=buchst[2:])

    if lsgweg == "lgs":
        A = [E.rv_1, E.rv_2]
        B = [a - b for a, b in zip(P.v, E.sv)]

        x = gauss(A, B, zeilen=False)
        x_org = copy.deepcopy(x)
        if x[0] == "keine":
            check = False
        else:
            check = True

        if rechenweg:
            if intro:
                cprint("Punktprobe von einer Ebene und einem Punkt über das LGS:\n", abs_far)

            if E.darst != "para":
                print("Als erstes die Ebene in Parameterform umformen:\n")
                E.umrechnen(E.darst, "para", True, end=True)
                print("\n")
                cprint("Jetzt Punkt und Ebene gleichstellen:\n", abs_far)

            else:
                print("Als erstes Punkt und Ebene gleichstellen:\n")

            P_darst = P.display(prec, print_=False, print_buchst=False)
            E_darst = E.display(prec, darst="para", print_=False, print_buchst=False)
            diff = cla.Vektor([P.v[i] - E.sv[i] for i in range(3)])
            diff_darst = diff.display(prec, print_=False, print_buchst=False)

            rv_1_darst = cla.Vektor(E.rv_1).display(prec, print_=False, print_buchst=False)
            rv_2_darst = cla.Vektor(E.rv_2).display(prec, print_=False, print_buchst=False)

            param = [std.format_prec([f"{item} ∙" if i == 1 else "" for i in range(3)], string=True) for item in buchst[2:]]
            gleich = std.format_prec(["=" if i == 1 else "" for i in range(3)], string=True)
            plus = std.format_prec(["+" if i == 1 else "" for i in range(3)], string=True)

            for i in range(3):
                print(f"{E_darst[i]} {gleich[i]} {P_darst[i]}")

            print("\n")
            print("Jetzt den Stützvektor von der Ebene von dem Punkt abziehen:\n")
            for i in range(3):
                cprint(f"{param[0][i]} {rv_1_darst[i]} {plus[i]} {param[1][i]} {rv_2_darst[i]} {gleich[i]} {diff_darst[i]}", zwi_far)

            print("\n")
            print("Jetzt ein LGS bilden:\n")
            dis.lgs([E.rv_1, E.rv_2, diff.v], prec, param_list=buchst[2:])

            print("\n")
            cprint("Jetzt das LGS lösen. Dies geschieht über den Gauss Algorithmus", abs_far)
            print("\n")
            gauss(A, B, zeilen=False, rechenweg=True, end=True, print_lsg=True, param=["r"])
            if x_org[0] != "keine":
                print("\n")

            if x_org[0] == "eind":
                cprint("Da eine eindeutige Lösung existiert, liegt der Punkt in der Ebene", end_far)

            elif x_org[0] == "keine":
                cprint("Es gibt keine Lösung des Gleichungssystems, der Punkt ist nicht Teil der Ebene", end_far)

            elif x_org[0] == "unend":
                cprint("Es gibt unendlich viele Lösungen des Gleichungssystems, der Punkt ist Teil der Ebene", end_far)

        return check

    elif lsgweg == "koor":
        wert = [E.kv[i] * P.v[i] for i in range(3)]
        check = sum(wert) == E.kv[3]
        if rechenweg:
            if intro:
                cprint("Punktprobe von einer Ebene in Parameterform und einem Punkt über das Einsetzen in die Koordinatenform:\n", abs_far)

            if E.darst != "koor":
                cprint("Als erstes die Ebene in Koordinatenform umformen:\n")
                E.umrechnen(E.darst, "koor", True, end=True)
                print("\n")
                cprint(f"Jetzt kann der Punkt {P.buchst} in die Koordinatenform eingesetzt werden:\n", abs_far)

            E.einsetzen(cla.Punkt(P.v), rechenweg=True, end=True)
            print("\n")
            cprint(f"Dies ist {'' if check else 'k'}eine Wahre Aussage, der Punkt ist{'' if check else ' nicht'} Teil der Ebene", end_far)

        return check

    elif lsgweg == "beides":
        check_1 = punktprobe_pE(P, E, rechenweg=rechenweg, lsgweg="lgs", intro=True, end=True, ende=True, buchst=buchst)
        print("\n\n\n")
        check_2 = punktprobe_pE(P, E, rechenweg=rechenweg, lsgweg="koor", intro=True, end=True, ende=True, buchst=buchst)

        if check_1 == check_2:
            return check_1
        else:
            err_far = std.get_color("err")
            raise cla.Error(colored(f"Die Checks sind nicht gleich:\n{check_1}, {check_2}", err_far))


def schnittwinkel(inp1, inp2, rechenweg=False, intro=False, end=False, ende=False, typ=None, buchst=None):
    """

    Parameters
    ----------
    inp1        Der erste Input - list / cla.Gerade / cla.Ebene
    inp2        Der zweite Input - list / cla.Gerade / cla.Ebene
    rechenweg   Soll ein Rechenweg angezeigt werden
    lsgweg      Welcher Lösungsweg soll genommen werden - gdw "force ..." - "lgs" / "koor"
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    typ         Von welchem Typ die beiden Inputs sind - gerade oder Ebene
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Den Schnittwinkel aus inp1 und inp2 - Number in Deg
    """
    std.verify_input(inp1, "Objekt 1", ("gerade", "ebene")), std.verify_input(inp2, "Objekt 2", ("gerade", "ebene"))
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)
    prec_2 = std.get_prec(2)

    if typ is None:
        typ = []
    if buchst is None:
        buchst = [None, None, None]

    std.buchstabe_auffüllen(typ, ["", ""])

    for i, item in enumerate([inp1, inp2]):
        try:
            std.verify_input(item, f"Objekt {i + 1}", "gerade")
            std.verify_input(item, f"Objekt {i + 1}", "ebene")

            err_far = std.get_color("err")

            if not isinstance(typ, (list, tuple)):
                raise cla.InputError2(colored(f"\nDer Typ von Objekt 1 konnte nicht dynamisch herausgefunden werden und type != list", err_far))
            else:
                if len(typ) != 2:
                    raise cla.InputError2(colored(f"Die Länge von typ != 2", err_far))

                if typ[i] not in ["gerade", "ebene"]:
                    raise cla.InputError2(colored(f"\nDie Elemente von typ[{i}] sind nicht nur gerade und ebene: {typ}", err_far))

        except cla.InputError:
            try:
                std.verify_input(item, "Objekt 1", "gerade")
                typ[i] = "gerade"

            except cla.InputError:
                std.verify_input(item, "Objekt 1", "ebene")
                typ[i] = "ebene"

    if typ[0] == "gerade":
        if buchst[0] is None:
            buchst[0] = ["r", "g"]

        if not isinstance(inp1, cla.Gerade):
            inp1 = cla.Gerade(inp1, param=buchst[0][0], buchst=buchst[0][1])

    elif typ[0] == "ebene":
        if buchst[0] is None:
            buchst[0] = ["s", "t", "E"]

        if not isinstance(inp1, cla.Ebene):
            inp1 = cla.Ebene(inp1, param=buchst[0][:2], buchst=buchst[0][2])

    if typ[1] == "gerade":
        if buchst[1] is None:
            if typ[0] == "gerade":
                buchst[1] = ["s", "h"]
            else:
                buchst[1] = ["r", "g"]

        if not isinstance(inp2, cla.Gerade):
            inp2 = cla.Gerade(inp2, param=buchst[1][0], buchst=buchst[1][1])

    elif typ[1] == "ebene":
        if buchst[1] is None:
            if typ[0] == "gerade":
                buchst[1] = ["s", "t", "E"]
            else:
                buchst[1] = ["u", "v", "F"]

        if not isinstance(inp2, cla.Ebene):
            inp2 = cla.Ebene(inp2, param=buchst[1][:2], buchst=buchst[1][2])

    if typ[0] == "gerade":
        v_1 = cla.Vektor(copy.deepcopy(inp1.rv), buchst=inp1.param)
    else:
        if typ[1] == "ebene":
            v_1 = cla.Vektor(copy.deepcopy(inp1.nv), buchst="n₁")
        else:
            v_1 = cla.Vektor(copy.deepcopy(inp1.nv), buchst="n")

    if typ[1] == "gerade":
        v_2 = cla.Vektor(copy.deepcopy(inp2.rv), buchst=inp2.param)
    else:
        if typ[0] == "ebene":
            v_2 = cla.Vektor(copy.deepcopy(inp2.nv), buchst="n₂")
        else:
            v_2 = cla.Vektor(copy.deepcopy(inp2.nv), buchst="n")

    if buchst[2] is None:
        buchst[2] = "α"

    if all(item == "gerade" for item in typ):
        # Schnittwinkel Gerade - Gerade
        algo = math.acos
        if intro:
            intro_text = "des Schnittwikels zweier Geraden"

    elif typ.count("gerade") == typ.count("ebene") == 1:
        # Schnittwinkel Gerade - Ebene
        algo = math.asin
        if intro:
            intro_text = f"des Schnittwikels von {typ[0].capitalize()} und {typ[1].capitalize()}"

    else:
        # Schnittwinkel Ebene - Ebene
        algo = math.acos
        if intro:
            intro_text = "des Schnittwikels zweier Ebenen"

    skp = skalarprodukt(v_1, v_2)
    abs_v1 = absvec(v_1)
    abs_v2 = absvec(v_2)
    mul = abs_v1 * abs_v2

    div = 0 if round(mul, prec_int) == 0 else abs(skp) / mul

    alpha = math.degrees((algo(div)))

    if rechenweg:
        alpha_darst = std.format_prec(alpha, prec)
        if intro:
            cprint(f"Berechnung {intro_text}:\n", abs_far)

        print("Die allgemeine Formel des Schnittwinkels lautet:\n")
        dis.schnittwinkel_formel(inp1, inp2, typ=typ, winkel=buchst[2])
        print("\n")

        if typ[0] == typ[1] == "ebene" and all(_.darst == "para" for _ in (inp1, inp2)):
            print(f"Davor müssen allerdings noch die Normalenvektoren von {inp1.buchst} und {inp2.buchst} berechnet werden:\n")
            conv_norm(inp1.rv_1, inp1.rv_2, True, end=True, buchst=[inp1.param[0], inp1.param[1], "n₁"])
            print("\n")
            conv_norm(inp2.rv_1, inp2.rv_2, True, end=True, buchst=[inp2.param[0], inp2.param[1], "n₂"])
            print("\n")

        elif typ[0] == "ebene" and inp1.darst == "para":
            print(f"Davor muss allerdings noch der Normalenvektor von {inp1.buchst} berechnet werden:\n")
            conv_norm(inp1.rv_1, inp1.rv_2, True, end=True)
            print("\n")

        elif typ[1] == "ebene" and inp2.darst == "para":
            print(f"Davor muss allerdings noch der Normalenvektor von {inp2.buchst} berechnet werden:\n")
            conv_norm(inp2.rv_1, inp2.rv_2, True, end=True)
            print("\n")

        print("Einsetzen:\n")
        dis.schnittwinkel_formel(inp1, inp2, typ=typ, ausrechnen=True, winkel=buchst[2], color=zwi_far)

        print("\n")
        cprint("Das Skalarprodukt ausrechnen:\n", abs_far)
        skalarprodukt(v_1, v_2, True, end=True)

        print("\n")
        print("Einsetzen:")
        dis.schnittwinkel_formel(inp1, inp2, typ=typ, ausrechnen="oben", winkel=buchst[2], color=zwi_far)

        print("\n")
        cprint("Die Beträge ausrechnen:\n", abs_far)
        absvec(v_1, True, end=True)
        print()
        absvec(v_2, True, end=True)
        print("\n")
        cprint("Multiplizieren:\n", abs_far)
        dis.lgs([abs_v1, abs_v2], prec_2, b_len=1, operation="*", b_berechnen=True, zeilen=True, print_param=False)

        print("\n")
        print("Einsetzen:\n")
        dis.schnittwinkel_formel(inp1, inp2, typ=typ, ausrechnen="oben, unten", winkel=buchst[2], color=zwi_far)

        print("\n")
        cprint("Ausrechnen:\n", abs_far)
        dis.lgs([abs(skp), mul], prec_2, b_len=1, operation="/", b_berechnen=True, zeilen=True, print_param=False)

        print("\n")
        print("Umkehren:\n")
        dis.schnittwinkel_formel(inp1, inp2, typ=typ, ausrechnen="oben, unten bruch", umstellen=True, winkel=buchst[2])

        print("\n")
        print("Berechnen:\n")
        cprint(f"{buchst[2]} = {alpha_darst}°", end_far)
    return alpha


def ebenen_gleich(E, F, rechenweg=False, intro=False, end=False, ende=False, buchst=None):
    """

    Parameters
    ----------
    E           Die erste Ebene - list / cla.Ebene
    F           Die zweite Ebeen - list / cla.Ebene
    rechenweg   Soll ein Rechenweg angezeigt werden
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Ob die Ebenen gleich sind - bool
    """
    std.verify_input(E, "Objekt 1", "ebene"), std.verify_input(F, "Objekt 2", "ebene")
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "intro", bool)
    std.verify_input(end, "end", bool), std.verify_input(ende, "ende", bool)

    if buchst is None:
        buchst = [None, None]

    buchst = [std.buchstabe_auffüllen(buch, item) for buch, item in zip(buchst, [["E", "s", "t"], ["F", "u", "v"]])]
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if not isinstance(E, cla.Ebene):
        E = cla.Ebene(E, buchst=buchst[0][0], param=buchst[0][1:])
    if not isinstance(F, cla.Ebene):
        F = cla.Ebene(F, buchst=buchst[1][0], param=buchst[1][1:])

    n1 = E.nv.copy()
    n2 = F.nv.copy()

    check1 = linear_abhangig(n1, n2)

    if F.darst != "koor":
        P = cla.Punkt(F.sv)
        eb = E

    elif E.darst != "koor":
        P = cla.Punkt(E.sv)
        eb = F

    else:
        P = cla.Punkt(F.sv)
        eb = E

    if eb.darst != "para":
        lsgweg = "koor"
    else:
        lsgweg = "lgs"

    check2 = punktprobe_pE(P, eb, False, lsgweg=lsgweg)

    if rechenweg:
        if intro:
            cprint(f"Feststellen, ob die Ebenen {E.buchst} und {F.buchst} gleich sind:\n", abs_far)

        print("Zunächst werden die Normalenvektoren auf lineare abhängigkeit untersucht:\n")

        if E.darst == F.darst == "para":
            print(f"Davor müssen aber noch beide Normalenvektoren gebildet werden:\n")
            conv_norm(E.rv_1, E.rv_2, True, end=True, buchst=[E.param[0], E.param[1], "n₁"])
            print("\n")
            conv_norm(F.rv_1, F.rv_2, True, end=True, buchst=[F.param[0], F.param[1], "n₂"])
            print("\n")

        elif E.darst == "para":
            print(f"Dafür muss aber noch der Normalenvektor der Ebene {E.buchst} gebildet werden:\n")
            conv_norm(E.rv_1, E.rv_2, True, end=True, buchst=[E.param[0], E.param[1], "n₁"])
            print("\n")

        elif F.darst == "para":
            print(f"Dafür muss aber noch der Normalenvektor der Ebene {F.buchst} gebildet werden:\n")
            conv_norm(F.rv_1, E.rv_2, True, end=True, buchst=[F.param[0], F.param[1], "n₁"])
            print("\n")

        print("Es gibt also folgende Normalenvektoren die auf lineare Abhängigkeit untersucht werden müssen:\n")
        n1_darst = E.display(prec, nur="nv", darst="norm", print_=False)
        n2_darst = F.display(prec, nur="nv", darst="norm", print_=False)

        mitte = int(E.dim / 2)

        n1_buchst = std.format_prec(["n₁ = " if i == mitte else "" for i in range(E.dim)], string=True)
        n2_buchst = std.format_prec(["  n₂ = " if i == mitte else "" for i in range(E.dim)], string=True)
        komma = std.format_prec(["," if i == mitte else "" for i in range(E.dim)], string=True)

        for a, b, c, d, e in zip(n1_buchst, n1_darst, komma, n2_buchst, n2_darst):
            print(a + b + c + d + e)
        print("\n")

        linear_abhangig(E.nv, F.nv, True, buchst=["n₁", "n₂"])
        print("\n")

        if check1:
            cprint("Die Parameterwerte sind gleich. Damit sind die Ebenen entweder parallel oder identisch.", abs_far)
            cprint("Also muss noch eine Punktprobe zwischen den beiden Ebenen durchgeführt werden:\n", abs_far)
            if F.darst != "koor":
                print(f"Als Punkt zum einsetzen wird der Stützvektor von {F.buchst} verwendet.")

            elif E.darst != "koor":
                print(f"Als Punkt zum einsetzen wird der Stützvektor von {E.buchst} verwendet.")

            else:
                print(f"Der Stützvektor ist noch nicht gebildet. Er wird aus der Koordinatenform von {F.buchst} gebildet:\n")
                F.umrechnen("koor", "para", True, sv_berechnen=True, end=True)
                print("\n")

            if F.darst != "koor":
                if E.darst == "para":
                    cprint(f"Der Stützvektor wird in die Parameterform von {E.buchst} eingesetzt und über das LGS gelöst.")
                else:
                    cprint(f"Der Stützvektor wird in die Koordinatenform von {E.buchst} eingesetzt.")

            elif E.darst != "koor":
                if F.darst == "para":
                    cprint(f"Der Stützvektor wird in die Parameterform von {F.buchst} eingesetzt und über das LGS gelöst.")
                else:
                    cprint(f"Der Stützvektor wird in die Koordinatenform von {F.buchst} eingesetzt.")

            else:
                cprint(f"Der Stützvektor von {F.buchst} wird in die Koordinatenform von {E.buchst} eingesetzt.")

            print("\n")
            punktprobe_pE(P, eb, True, lsgweg=lsgweg, end=True)
            print("\n")

            if check2:
                cprint("Da der Punkt Teil der Ebene ist, sind die Ebenen identisch.", end_far)
            else:
                cprint("Da der Punkt nicht Teil der Ebene ist, sind die Ebenen nicht identsich.", end_far)

        else:
            cprint("Die Parameterwerte sind nicht gleich. Damit können die Ebenen nicht gleich sein", end_far)


def schnitt(obj1, obj2, typ=None, rechenweg=False, lsgweg="lgs", intro=False, end=False, ende=False, buchst=None):
    """

    Parameters
    ----------
    obj1        Objekt 1 - list / cla.Gerade / cla.Ebene
    obj2        Objekt 2 - list / cla.Gerade / cla.Ebene
    typ         Typ von Objekt 1 / 2 - wird nur gebraucht, wenn [[...], [...]] weil uneindeutig bzgl. Gerade / Normalenform
    rechenweg   Soll ein Rechenweg angezeigt werden
    lsgweg      Welcher Lösungsweg soll gewählt werden - nur wenn "force ..." - lgs / koor / passend
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden
    buchst      Welcher Buchstabe soll für v gewählt werden (falls kein cla.Vektor)

    Returns
    -------
    Den Schnitt aus Objekt 1 und 2 - bool falls ident / windschief / cla.Punkt / cla.Gerade
    """
    if typ is None:
        typ = [None, None]
    typ0, obj1 = std.dynamic_type(obj1, ["gerade", "ebene"], typ=typ[0], instantiate=True)
    typ1, obj2 = std.dynamic_type(obj2, ["gerade", "ebene"], typ=typ[1], instantiate=True, previous=obj1)
    typ = [typ0, typ1]
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if typ == ["ebene", "gerade"]:
        obj1, obj2 = obj2, obj1
        typ = ["gerade", "ebene"]

    if "force" in lsgweg:
        lsgweg = lsgweg.replace("force", "").strip()
    else:
        if typ[0] == "gerade":
            if buchst is None:
                buchst = "S"
        else:
            if buchst is None:
                buchst = "g"

        if typ == ["gerade", "gerade"]:
            lsgweg = "lgs"
        elif typ == ["gerade", "ebene"]:
            lsgweg = std.get_lsg("lsg schnitt g e")
        else:
            lsgweg = std.get_lsg("lsg schnitt e e")

        if lsgweg not in ["lgs", "koor", "passend"]:
            err_far = std.get_color("err")
            raise cla.InputError(colored(f'Der Lösungsweg war nicht in den Vorgegebenen Typen. Das kann auf einen Fehler in der Konfiguration hindeuten ["lgs", "koor", "passend"]:\n{lsgweg}', err_far))

        if lsgweg == "passend":
            if typ == ["gerade", "ebene"]:
                if obj2.darst == "para":
                    lsgweg = "lgs"
                else:
                    lsgweg = "koor"
            else:
                if obj1.darst == "para" and obj2.darst == "para":
                    lsgweg = "lgs"
                else:
                    lsgweg = "koor"

    if lsgweg == "lgs":
        diff = [a - b for a, b in zip(obj2.sv, obj1.sv)]
        if typ == ["gerade", "gerade"]:
            A = [obj1.rv, [-_ for _ in obj2.rv]]

        elif typ == ["gerade", "ebene"]:
            A = [obj1.rv, [-_ for _ in obj2.rv_1], [-_ for _ in obj2.rv_2]]

        elif typ == ["ebene", "ebene"]:
            A = [obj1.rv_1, obj1.rv_2, [-_ for _ in obj2.rv_1], [-_ for _ in obj2.rv_2]]

        lsg = gauss(A, diff, zeilen=False, rechenweg=False, end=True, param=["r"])
        if lsg[0] == "eind" and (typ == ["gerade", "gerade"] or typ == ["gerade", "ebene"]):
            final_lsg = cla.Punkt(obj1.einsetzen(lsg[1][0], "parameter", return_list=True), buchst=buchst)

        elif lsg[0] == "unend":
            if typ == ["gerade", "gerade"]:
                final_lsg = True
            elif typ == ["ebene", "ebene"]:
                altlsg = [item for item in lsg[1] if item[0] != "spez"]
                einzusetzen = [[lsg[1][0][1], lsg[1][1][1]], [lsg[1][0][2], lsg[1][1][2]]]
                if len(altlsg) == 1:
                    final_lsg = cla.Gerade(obj1.einsetzen(einzusetzen, typ="zwei parameter", return_list=True), buchst=buchst)
                elif len(altlsg) == 2:
                    final_lsg = True
                else:
                    print("Die Lösung hat mehr als 2 freie Dimensionen... Intressant.")
                    final_lsg = None

        elif lsg[0] == "keine":
            final_lsg = False

        if rechenweg:
            if intro:
                cprint(f"Schnittpunktbestimmung zwischen {typ[0].capitalize()} und {typ[1].capitalize()} über das LGS:\n", abs_far)

            if typ[0] == "ebene" and obj1.darst != "para":
                print(f"Damit ein LGS aufgestellt werden kann muss zunächst die Ebene {obj1.buchst} in Parameterform umgerechnet werden:\n")
                obj1.umrechnen(obj1.darst, "para", True, end=True, sv_berechnen=True)
                obj1.darst = "para"
                print("\n")

            if typ[1] == "ebene" and obj2.darst != "para":
                print(f"Damit ein LGS aufgestellt werden kann muss die Ebene {obj2.buchst} in Parameterform umgerechnet werden:\n")
                obj2.umrechnen(obj2.darst, "para", True, end=True, sv_berechnen=True)
                obj2.darst = "para"
                print("\n")

            print(f"{obj1.buchst} und {obj2.buchst} gleichstellen:\n")
            obj1_darst = obj1.display(prec, print_buchst=False, print_=False)
            obj2_darst = obj2.display(prec, print_buchst=False, print_=False)

            mitte = int(len(obj1_darst) / 2)

            gleich = ["   "] * len(obj1_darst)
            gleich[mitte] = " = "
            for _ in zip(obj1_darst, gleich, obj2_darst):
                print("".join(_))

            print("\n")
            print("Die Parameter auf eine Seite bringen:\n")

            dummy = [""] * len(obj1_darst)

            param_list = []
            if typ[0] == "gerade":
                obj1_darst_1 = obj1.display(prec, print_buchst=False, print_=False, nur="rv")
                obj1_darst_2 = dummy
                param1_darst = [[" " * len(f"{obj1.param} ∙ ")] * len(obj1_darst_1), dummy]
                param1_darst[0][mitte] = f"{obj1.param} ∙ "
                param_list.append(obj1.param)

            elif typ[0] == "ebene":
                obj1_darst_1 = obj1.display(prec, print_buchst=False, print_=False, nur="rv_1")
                obj1_darst_2 = obj1.display(prec, print_buchst=False, print_=False, nur="rv_2")
                param1_darst = [[" " * len(f"{obj1.param[0]} ∙ ")] * len(obj1_darst_1), [" " * len(f" + {obj1.param[1]} ∙ ")] * len(obj1_darst_1)]
                param1_darst[0][mitte] = f"{obj1.param[0]} ∙ "
                param1_darst[1][mitte] = f" + {obj1.param[1]} ∙ "
                param_list.append(obj1.param[0])
                param_list.append(obj1.param[1])

            if typ[1] == "gerade":
                obj2_darst_1 = obj2.display(prec, print_buchst=False, print_=False, nur="rv")
                obj2_darst_2 = dummy
                param2_darst = [[" " * len(f" - {obj2.param} ∙ ")] * len(obj2_darst_1), dummy]
                param2_darst[0][mitte] = f" - {obj2.param} ∙ "
                param_list.append(obj2.param)

            elif typ[1] == "ebene":
                obj2_darst_1 = obj2.display(prec, print_buchst=False, print_=False, nur="rv_1")
                obj2_darst_2 = obj2.display(prec, print_buchst=False, print_=False, nur="rv_2")
                param2_darst = [[" " * len(f" - {obj2.param[i]} ∙ ")] * len(obj2_darst_1) for i in range(2)]
                for i in range(2):
                    param2_darst[i][int(len(obj2_darst_1) / 2)] = f" - {obj2.param[i]} ∙ "
                param_list.append(obj2.param[0])
                param_list.append(obj2.param[1])

            diff = cla.Vektor(diff)
            diff_darst = diff.display(prec, print_buchst=False, print_=False)

            for _ in zip(param1_darst[0], obj1_darst_1, param1_darst[1], obj1_darst_2, param2_darst[0], obj2_darst_1, param2_darst[1], obj2_darst_2, gleich, diff_darst):
                print("".join(_))

            print("\n")
            print("Hieraus ein LGS bilden um es mit dem Gauss Algorithmus zu lösen:\n")
            dis.lgs(A + [diff.v], prec, param_list=param_list)
            print("\n")
            cprint("Nun das LGS lösen:\n", abs_far)
            gauss(A, diff.v, zeilen=False, rechenweg=True, end=True, print_lsg=True, param=["r"])
            print("\n")

            if lsg[0] == "eind":
                if typ == ["gerade", "gerade"] or typ == ["gerade", "ebene"]:
                    if round(lsg[1][0], prec_int) and round(lsg[1][1]):
                        cprint(f"Um auf den Schnittpunkt zu kommen wird der Parameter {obj1.param} = {std.format_prec(lsg[1][0], prec)} in die Gerade {obj1.buchst} eingesetzt:\n")
                        obj1.einsetzen(lsg[1][0], "parameter", True, buchst=buchst)
                        print("\n")
                        print(f"Damit kommt man auf den Schnittpunkt {final_lsg.buchst}:\n")
                    else:
                        if round(lsg[1][0], prec_int) == 0:
                            obj = obj1
                        else:
                            obj = obj2
                        print(f"Da der Parameter {obj.param} = 0 ist, ist der Schnittpunkt {final_lsg.buchst} der Stützvektor von {obj.buchst}:\n")

                    final_lsg.display(prec, end_far)

            elif lsg[0] == "unend":
                if typ == ["gerade", "gerade"]:
                    cprint("Es gibt unendlich viele Lösungen.\nDas heißt die Geraden sind identisch und es existiert eine Schnittgerade:\n", end_far)
                    obj1.display(prec, end_far)

                elif typ == ["gerade", "ebene"]:
                    cprint("Es gibt unendlich viele Lösungen.\nDas heißt die ist Teil der Ebene und es existiert eine Schnittgerade:\n", end_far)
                    obj1.display(prec, end_far)

                elif typ == ["ebene", "ebene"]:

                    if len(altlsg) == 1:
                        cprint("Es gibt unendlich viele Lösungen, aber mit nur einer freien Dimension. Es existiert also eine Schnittgerade.", zwi_far)
                        print("\n")
                        print(f"Diese kann nun in die Ebenengleichung von {obj1.buchst} eingesetzt werden um auf eine Schnittgerade zu schließen.")
                        print(f"Dabei werden die ersten beiden Zeilen der Lösung eingesetzt, weil diese der Lösung für {obj1.param[0]} und {obj1.param[1]} entsprechen:\n")

                        obj1.einsetzen(einzusetzen, typ="zwei parameter", rechenweg=True, buchst=buchst)
                        print()
                        final_lsg.display(prec, end_far)
                    elif len(altlsg) == 2:
                        cprint("Es gibt unendlich viele Lösungen, aber mit zwei freien Dimensionen. Die ebenen sind also identisch.", end_far)

            elif lsg[0] == "keine":
                if typ == ["gerade", "gerade"]:
                    cprint("Für dieses Gleichungsystem existiert keine Lösung. Das heißt die Geraden sind windschief oder parallel und es gibt keinen Schnittpunkt.", end_far)

                elif typ == ["gerade", "ebene"]:
                    cprint("Für dieses Gleichungsystem existiert keine Lösung. Das heißt die Gerade und die Ebene sind parallel.", end_far)

                elif typ == ["ebene", "ebene"]:
                    cprint("Für dieses Gleichungsystem existiert keine Lösung. Die Ebenen sind parallel.", end_far)

            else:
                cprint("Dieser Fall sollte nicht eingetreten sein... Ich bin wohl einfach schlecht in dem was ich tue :(", end_far)

    elif lsgweg == "koor":
        if typ[0] == "ebene" and typ[1] == "ebene" and ((obj1.darst == "koor" and obj2.darst != "koor") or (obj1.darst == "norm" and obj2.darst == "para")):
            obj1, obj2 = obj2, obj1
        para = obj2.einsetzen(obj1, typ=typ[0])

        if typ[0] == "gerade":
            if not isinstance(para, bool):
                final_lsg = cla.Punkt(obj1.einsetzen(para, typ="parameter", return_list=True), buchst=buchst)
            else:
                final_lsg = para
        else:
            if not isinstance(para, bool):
                final_lsg = cla.Gerade(obj1.einsetzen(para, typ="parameter", return_list=True), buchst=buchst, param=obj1.param[1] if round(para[0], prec_int) != 0 else obj1.param[0])
            else:
                print(para)
                final_lsg = para

        if rechenweg:
            if intro:
                cprint(f"Schnittpunktbestimmung zwischen {typ[0].capitalize()} und {typ[1].capitalize()} über einsetzen in die Koordinatenform:\n", abs_far)

            if typ[0] == "gerade":
                if obj2.darst != "koor":
                    print(f"Damit die Gerade {obj1.buchst} in die Ebene {obj2.buchst} eingesetzt werden kann, muss zunächst die Koordinatenform der Ebene gebildet werden:\n")
                    obj2.umrechnen(obj2.darst, "koor", True, end=True)
                    obj2.darst = "koor"
                    print("\n")

                cprint("Die Gerade koordinatenweise in die Ebenengleichung einsetzen:\n", abs_far)
                obj2.einsetzen(obj1, rechenweg=True, typ=typ[0], end=True)
                print("\n")
                if para is True:
                    cprint(f"Dies ist eine wahre Aussage. Damit sind {typ[0].capitalize()} und {typ[1].capitalize()} identisch.", end_far)
                elif para is False:
                    cprint(f"Dies ist eine falsche Aussage. Damit sind {typ[0].capitalize()} und {typ[1].capitalize()} parallel.", end_far)
                else:
                    cprint("Dies ist der Parameter zum finden des Schnittpunktes. Dieser wird in die Gerade eingesetzt:\n", abs_far)
                    obj1.einsetzen(para, typ="parameter", rechenweg=True)
                    print("\n")
                    cprint(f"Damit kommt man auf den Schnittpunkt {final_lsg.buchst}:\n", end_far)
                    final_lsg.display(prec, end_far)

            else:
                if obj2.darst == "koor" or obj1.darst != "koor":
                    print(f"Es wird die Ebene {obj1.buchst} in die Ebene {obj2.buchst} eingesetzt:\n")
                else:
                    print(f"Es wird die Ebene {obj2.buchst} in die Ebene {obj1.buchst} eingesetzt:\n")
                    obj1, obj2 = obj2, obj1

                schon_geschrieben = False

                if obj2.darst != "koor":
                    print(f"Damit die Ebene {obj1.buchst} in die Ebene {obj2.buchst} eingesetzt werden kann, muss zunächst die Koordinatenform der Ebene {obj2.buchst} gebildet werden:\n")
                    obj2.umrechnen(obj2.darst, "koor", True, end=True)
                    print("\n")
                    obj2.darst = "koor"
                    schon_geschrieben = True

                if obj1.darst != "para" and not schon_geschrieben:
                    print(f"Damit die Ebene {obj1.buchst} in die Ebene {obj2.buchst} eingesetzt werden kann, muss zunächst die Parameterform der Ebene {obj1.buchst} gebildet werden:\n")
                    obj1.umrechnen(obj1.darst, "para", True, end=True)
                    obj1.darst = "para"
                    print("\n")
                    schon_geschrieben = True

                elif obj1.darst != "para" and schon_geschrieben:
                    print(f"Außerdem muss noch die Parameterform der Ebene {obj1.buchst} gebildet werden:\n")
                    obj1.umrechnen(obj1.darst, "para", True, end=True)
                    obj1.darst = "para"
                    print("\n")
                    schon_geschrieben = True

                if schon_geschrieben:
                    cprint(f"Nun kann die Ebene {obj1.buchst} in die Ebene {obj2.buchst} eingesetzt werden:\n", abs_far)

                obj2.einsetzen(obj1, typ="ebene", rechenweg=True, end=True)
                print("\n")
                if para is True:
                    cprint(f"Dies ist eine Wahre Aussage. Die Ebenen {obj1.buchst} und {obj2.buchst} sind also identisch.", end_far)
                elif para is False:
                    cprint(f"Dies ist eine Falsche Aussage. Die Ebenen {obj1.buchst} und {obj2.buchst} sind also parallel.", end_far)
                elif round(para[0], prec_int) != 0:
                    p = obj1.param[0]
                else:
                    p = obj1.param[1]

                if not isinstance(para, bool):
                    cprint(f"Dies wird nun für den Parameter {p} in der Ebene {obj1.buchst} eingesetzt:\n", abs_far)
                    obj1.einsetzen(para, typ="parameter", rechenweg=True)
                    final_lsg.display(prec, end_far)

    return final_lsg


def dist(obj1, obj2, typ=None, rechenweg=False, lsgweg="passend", intro=False, end=False, ende=False):
    """

    Parameters
    ----------
    obj1        Objekt 1 - list / cla.Punkt / cla.Gerade / cla.Ebene
    obj2        Objekt 2 - list / cla.Punkt / cla.Gerade / cla.Ebene
    typ         Typ von Objekt 1 / 2 - wird nur gebraucht, wenn [[...], [...]] weil uneindeutig bzgl. Gerade / Normalenform
    rechenweg   Soll ein Rechenweg angezeigt werden
    lsgweg      Welcher Lösungsweg soll gewählt werden - nur wenn "force ..." - hilf / geo / lfp / hnf / passend
    intro       Soll ein Intro angezeigt werden
    end         Soll das Ende angezeigt werden
    ende        Soll das Ende als Ende (True) oder als Zwischenergebnis (False) behandelt werden

    Returns
    -------
    Den Abstand von Objekt 1 zu 2 - Number
    """
    if typ is None:
        typ = [None, None]
    typ0, obj1 = std.dynamic_type(obj1, ["gerade", "punkt", "ebene"], typ=typ[0], instantiate=True)
    typ1, obj2 = std.dynamic_type(obj2, ["gerade", "punkt", "ebene"], typ=typ[1], instantiate=True, previous=obj1)
    typ = [typ0, typ1]
    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if typ == ["gerade", "punkt"] or typ == ["ebene", "gerade"]:
        obj1, obj2 = obj2, obj1
        typ.reverse()

    if "force" in lsgweg:
        lsgweg = lsgweg.replace("force", "").strip()
    else:
        _ = ""
        if typ == ["gerade", "gerade"]:
            # feststellen ob parallel oder windschief
            if linear_abhangig(obj1.rv, obj2.rv) and not punktprobe_pg(obj1.sv, obj2):
                _ = " parallel"
            else:
                _ = " windschief"
        lsgweg = std.get_lsg(f"lsg dist {typ[0][0]} {typ[1][0]}{_}")
        if lsgweg not in ["hilf", "geo", "lfp", "hnf"]:
            err_far = std.get_color("err")
            raise cla.InputError(colored(f'Der Lösungsweg war nicht in den Vorgegebenen Typen. Das kann auf einen Fehler in der Konfiguration hindeuten ["hilf", "geo", "lfp", "hnf"]:\n{lsgweg}', err_far))

    obj1_buchst = obj1.buchst
    obj2_buchst = obj2.buchst

    if lsgweg == "hilf":
        # Punkt Gerade ∨ Gerade Gerade
        backup_buchst = obj1.buchst
        if typ[0] == "gerade":
            obj1 = cla.Punkt(obj1.sv, buchst="P")

        E = cla.Ebene([obj1.P, obj2.rv])
        S = schnitt(obj2, E, typ=["gerade", "ebene"], buchst="Fₗ")
        dist_v = vektor_zwei_punkte(obj1, S)
        d = absvec(dist_v)

        if rechenweg:
            if intro:
                cprint(f"Abstandsbestimmung zwischen {typ[0].capitalize()} und {typ[1].capitalize()}:\n", abs_far)
            if typ[0] == "gerade":
                print(f"Die Abstandsbestimmung von zwei Geraden ist sehr ähnlich zu der von Punkt und Gerade. Man nehme den Stützvektor von {backup_buchst} als Punkt P:\n")
                obj1.display(prec)
                print()
                print("Nun", end="")

            else:
                print("Zunächst", end="")
            if typ[0] == "punkt":
                _ = "Ortsvektor"
            else:
                _ = "Stützvektor"
            print(f" wird die Hilfsebene E in Normalenform mit dem Normalenvektor von {obj2.buchst} und dem {_} von {obj1.buchst} gebildet:\n")
            E.display(prec, zwi_far)
            print("\n")
            print(f"Nun muss der Schnittpunkt von {E.buchst} und {obj2.buchst}, der Lotfußpunkt Fₗ, gebildet werden:\n")
            schnitt(obj2, E, typ=["gerade", "ebene"], rechenweg=True, buchst="Fₗ")
            print("\n")
            print(f"Nun den Abstand von {obj1.buchst} zu dem Stützvektor von {obj2.buchst} finden. Dafür einen Vektor zwischen {obj1.buchst} und {S.buchst} bilden und dessen Betrag berechnen:\n")
            vektor_zwei_punkte(obj1, S, True, end=True)
            if dist_v.has_pfeil:
                print()
                cprint(" " * len("Nun den Betrag von ") + dist_v.pfeil, abs_far)
            else:
                print("\n")
            cprint(f"Nun den Betrag von {dist_v.buchst} berechnen:\n", abs_far)
            absvec(dist_v, True, end=True)

    elif lsgweg == "geo":
        # Punkt Gerade ∨ Gerade Gerade
        backup_buchst = obj1.buchst
        if typ[0] == "gerade":
            obj1 = cla.Punkt(obj1.sv, buchst="P")

        ab = vektor_zwei_punkte(obj1, obj2.sv)

        alpha = schnittwinkel(obj2, cla.Gerade([[0, 0, 0], ab.v]))
        betrag = absvec(ab)
        d = abs(math.sin(math.radians(alpha)) * betrag)

        if rechenweg:
            if intro:
                cprint(f"Abstandsbestimmung zwischen {typ[0].capitalize()} und {typ[1].capitalize()} mithilfe des geometrischen Ansatzes:\n", abs_far)
            if typ[0] == "gerade":
                print(f"Die Abstandsbestimmung von zwei Geraden ist sehr ähnlich zu der von Punkt und Gerade. Man nehme den Stützvektor von {backup_buchst} als Punkt P:\n")
                obj1.display(prec)
                print()
                print("Nun", end="")
            else:
                print("Zunächst", end="")
            print(f" den Vektor von {backup_buchst} zum Stützvektor von {obj2.buchst}, Q, bilden:\n")
            vektor_zwei_punkte(obj1, obj2.sv, True, end=True)
            if ab.has_pfeil:
                print(" " * len("Nun muss noch der Schnittwinkel zwischen ") + ab.pfeil)
            print(f"Nun muss noch der Schnittwinkel zwischen {ab.buchst} und {obj2.buchst} berechnet werden:\n")
            alpha = schnittwinkel(obj2, cla.Gerade([[0, 0, 0], ab.v]), True)
            print("\n")
            if ab.has_pfeil:
                print(" " * len("Jetzt fehlt nur noch der Betrag von ") + ab.pfeil)
            print(f"Jetzt fehlt nur noch der Betrag von {ab.buchst}:\n")
            absvec(ab, True, end=True)
            print("\n")
            print("Damit kann nun der Abstand berechnet werden:\n")
            if ab.has_pfeil:
                print(" " * len("d = |sin(α) ∙ |") + ab.pfeil)
            print(f"d = |sin(α) ∙ |{ab.buchst}||")
            print("\n")
            alpha_darst, betrag_darst = std.format_prec(alpha, prec), std.format_prec(betrag, prec)
            print(f"d = │sin({alpha_darst}°) ∙ {betrag_darst}│")
            print("\n")
            d_darst = std.format_prec(d, prec)
            print(f"d = {d_darst}")

    elif lsgweg == "lfp":
        if typ[0] == "ebene" and obj2.darst == "para" and obj1.darst != "para":
            obj1, obj2 = obj2, obj1

        backup_buchst = obj2.buchst
        if typ == ["gerade", "gerade"]:
            obj2 = cla.Ebene([obj2.sv, obj1.rv, obj2.rv])

        if typ[0] == "punkt":
            sv = obj1.P
        else:
            sv = obj1.sv

        g = cla.Gerade([sv, obj2.nv])
        S = schnitt(g, obj2, buchst="Fₗ")
        dist_v = vektor_zwei_punkte(sv, S)
        d = absvec(dist_v)

        if rechenweg:
            if intro:
                cprint(f"Abstandsbestimmung zwischen {typ[0].capitalize()} und {typ[1].capitalize()} mithilfe des Lotfußpunktes:\n", abs_far)
            if typ == ["gerade", "gerade"]:
                print(f"Die Geraden {obj1.buchst} und {backup_buchst} sind windschief.\nEs muss eine Hilfsebene mit beiden Richtungsvektoren der Geraden und Stützvektor der Geraden {backup_buchst} gebildet werden:\n")
                obj2.display(prec, zwi_far)
                print("\n")
                print("Nun", end="")
            else:
                print("Zunächst", end="")
            if typ[0] == "punkt":
                _ = "Ortsvektor"
            else:
                _ = "Stützvektor"
            print(f" wird die Lotgerade gebildet. Diese hat den Normalenvektor von {obj2.buchst} und den {_} von {obj1.buchst}:\n")
            if obj2.darst == "para" and (typ[0] != "ebene" or obj1.darst == "para"):
                print(f"Dafür muss allerdings noch der Normalenvektor von {obj2.buchst} gebildet werden:\n")
                conv_norm(obj2.rv_1, obj2.rv_2, True, end=True)
                print("\n")
                print("Daraus ergibt sich:\n")

            g.display(prec, zwi_far)
            print("\n")
            cprint(f"Nun muss der Schnittpunkt von {g.buchst} und {obj2.buchst} gefunden werden:\n", abs_far)
            schnitt(g, obj2, rechenweg=True, end=True, buchst="Fₗ")
            print("\n")
            print(f"Nun den Abstand von {obj1.buchst} zu dem Stützvektor von {obj2.buchst} finden. Dafür einen Vektor zwischen {obj1.buchst} und {S.buchst} bilden und dessen Betrag berechnen:\n")
            vektor_zwei_punkte(sv, S, True, end=True)
            if dist_v.has_pfeil:
                print()
                cprint(" " * len("Nun den Betrag von ") + dist_v.pfeil, abs_far)
            else:
                print("\n")
            cprint(f"Nun den Betrag von {dist_v.buchst} berechnen:\n", abs_far)
            absvec(dist_v, True, end=True)

    elif lsgweg == "hnf":
        if typ[0] == "ebene" and obj2.darst == "para" and obj1.darst != "para":
            obj1, obj2 = obj2, obj1

        backup_buchst = obj2.buchst
        if typ == ["gerade", "gerade"]:
            obj2 = cla.Ebene([obj2.sv, obj1.rv, obj2.rv])

        if typ[0] == "punkt":
            sv = obj1.P
        else:
            sv = obj1.sv

        if obj2.darst == "para":
            n0 = conv_norm0(obj2.rv_1, obj2.rv_2, return_list=True)
        else:
            n0 = conv_norm0(obj2.nv, cla.Vektor([1, 1, 1]), u_as_nv=True, return_list=True)

        E_hnf = cla.Ebene([obj2.sv, n0])
        d = abs(E_hnf.einsetzen(sv, typ="hnf"))

        if rechenweg:
            if intro:
                cprint(f"Abstandsbestimmung zwischen {typ[0].capitalize()} und {typ[1].capitalize()} mithilfe der Hessischen Normalenform:\n", abs_far)
            if typ == ["gerade", "gerade"]:
                print(f"Die Geraden {obj1.buchst} und {backup_buchst} sind windschief.\nEs muss eine Hilfsebene mit beiden Richtungsvektoren der Geraden und Stützvektor der Geraden {backup_buchst} gebildet werden:\n")
                obj2.display(prec, zwi_far)
                print("\n")
                print("Nun", end="")
            else:
                print("Zunächst", end="")
            print(f" wird die Hessische Normalenform der Ebene {obj2.buchst} gebildet. Dafür muss der Normaleneinheitsvektor gefunden werden:\n")
            if obj2.darst == "para":
                conv_norm0(obj2.rv_1, obj2.rv_2, True)
            else:
                conv_norm0(obj2.nv, cla.Vektor([1, 1, 1]), True, u_as_nv=True)
            print("\n")
            print(f"Diesen als Normalenvektor der Ebene {obj2.buchst} verwenden um eine Abstandsfunktion zu bekommen:\n")
            E_hnf.display(prec, zwi_far, n0=True)
            print("\n")
            if typ[0] == "punkt":
                _ = "Ortsvektors"
            else:
                _ = "Stützvektors"
            print(f"Einsetzen des {_} von {obj1.buchst} in die HNF um den Abstand bestimmen zu können:\n")
            E_hnf.einsetzen(sv, typ="hnf", rechenweg=True)

    if end:
        if rechenweg:
            print("\n")
            cprint(f"Damit beträgt der Abstand von {obj1_buchst} und {obj2_buchst}", end_far, end="")
        else:
            cprint(f"Der Abstand von {obj1_buchst} und {obj2_buchst} beträgt", end_far, end="")
        cprint(f" {std.format_prec(d, prec)}LE", end_far)

    return d


def matmul(A, B, zeilen=True, rechenweg=False, intro=False, end=False, ende=False, buchst=None):
    std.verify_input(A, "Matrix A", "matrix"), std.verify_input(B, "Matrix B", "matrix")

    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    buchst = std.buchstabe_auffüllen(buchst, ["A", "B"])
    if isinstance(zeilen, bool):
        zeilen = [zeilen, zeilen]

    if not isinstance(A, cla.Matrix):
        A = cla.Matrix(A, zeilen=zeilen, A_buchst=buchst[0])
    if not isinstance(B, cla.Matrix):
        B = cla.Matrix(B, zeilen=zeilen, A_buchst=buchst[1])

    if A.dim_m != B.dim_n:
        err_far = std.get_color("err")
        raise cla.InputError(colored(f"Die Matritzen haben nicht kompatibele Dimensionen: A: {colored(f'{A.dim_m}', 'yellow')} × {A.dim_n}, B: {B.dim_m} × {colored(f'{B.dim_n}', 'yellow')}", err_far))

    C = cla.Matrix([[0 for _ in range(A.dim_m)] for _ in range(B.dim_n)])

    for i in range(A.dim_m):
        for j in range(B.dim_n):
            C.A[j][i] = sum(A.A[i][k] * B.A[k][j] for k in range(A.dim_n))

    if rechenweg:
        if intro:
            cprint(f"Matrixmultiplikation von {A.A_buchst} und {B.A_buchst}:\n", abs_far)

        cprint("Summen berechnen:\n")

        hilf_str0 = []
        hilf_str1 = []
        for i in range(B.dim_n):
            hilf_str0.append([])
            hilf_str1.append([])
            for j in range(A.dim_m):
                hilf_st0 = ""
                hilf_st1 = ""
                for k in range(A.dim_n):
                    A_st = std.format_prec(A.A[i][k], prec)
                    A_st_abs = std.format_prec(A.A[i][k], prec, absval=True)
                    AB_st = std.format_prec(A.A[i][k] * B.A[k][j], prec)

                    nchk = std.negcheck(A.A[i][k])[0]
                    B_st = std.format_prec(B.A[k][j], prec, klammer=True, mehrere=False)
                    if k == 0:
                        hilf_st0 += f"{A_st} ∙ {B_st}"
                        if round(A.A[i][k] * B.A[k][j], prec_int) != 0:
                            hilf_st1 += AB_st
                    else:
                        hilf_st0 += f" {nchk} {A_st_abs} ∙ {B_st}"
                        if round(A.A[i][k] * B.A[k][j], prec_int) != 0:
                            hilf_st1 += f" {nchk} {AB_st}"
                hilf_str0[i].append(hilf_st0)
                hilf_str1[i].append(hilf_st1)

        hilf0 = cla.Matrix(hilf_str0)
        hilf0.display()
        print("\n")
        cprint("Zusammenfassen:\n", abs_far)
        hilf1 = cla.Matrix(hilf_str1)
        hilf1.display()
        print("\n")
        cprint("Ausrechnen:\n", abs_far)
        C.display()

    return C


def gauss(A, b=None, zeilen=True, rechenweg=False, debugzeiten=False, intro=False, end=False, ende=False, print_lsg=False, param=None):
    start = time.time()
    std.verify_input(A, "Matrix A", "matrix"), std.verify_input(b, "Matrix b", (list, None)),
    std.verify_input(rechenweg, "Rechenweg", bool), std.verify_input(intro, "Intro", bool),
    std.verify_input(end, "Ende", bool)
    if rechenweg != "force" and rechenweg is not False:
        rechenweg = std.get_lsg("rweg gauss")

    pretty = std.get_divers("gauss pretty")
    err_far = std.get_color("err")

    if isinstance(A, list):
        if b is None:
            A = cla.Matrix(A[:-1], b=A[-1], zeilen=zeilen, A_buchst="A", b_buchst="b")
        else:
            A = cla.Matrix(A, b, zeilen=zeilen, A_buchst="A", b_buchst="b")

    elif isinstance(A, cla.Matrix) and b is not None:
        if isinstance(b, list):
            pass

        elif isinstance(b, cla.Matrix):
            # b = [[1], [2], [3], ...]
            b = [item[0] for item in b.A]

        A = cla.Matrix(A.A, b, zeilen=A.zeilen, A_buchst=A.A_buchst, b_buchst=A.b_buchst if A.has_b else "b")

    elif isinstance(A, cla.Matrix) and b is None:
        if A.has_b is False:
            raise cla.InputError(colored("Es ist kein b gegeben", err_far))

    if A.dim_n <= 15 and A.dim_m <= 15:
        pretty = True

    prec, prec_int, abs_far, zwi_far, end_far = std.ber_setup(rechenweg, end, ende)

    if A.find_non_0() is False:
        print("\n\n\n")
        A.display(3, color=err_far)
        print()
        raise cla.Error(colored(f"A ist eine Nullmatrix: {A.A}", err_far))

    A = copy.deepcopy(A)

    # sichern von A und b für den Rechenweg
    if rechenweg:
        A_old = copy.deepcopy(A)


    if A.zeilen is False:
        A.transp()

    n = A.find_non_0()
    if n != 0:
        A.swap(0, n)

    max_len = [0, 0, 0]

    # ZSF ------
    for i in range(A.dim_n - 1):
        for j in range(i + 1, A.dim_n):
            n = A.find_non_0(i)
            if round(A.A[j][n], prec_int) == 0:
                continue

            div = A.A[j][n] / A.A[i][n]

            zahl_1 = A.A[j][n]
            zahl_2 = A.A[i][n]

            for k in range(A.dim_m):
                A.A[j][k] -= div * A.A[i][k]

            A.b[j] -= div * A.b[i]

            if pretty and rechenweg:
                check = round(div, prec_int) != int(div)

                _ = len(A.display(3, pfeil=True, overset=dis.gauss_overset(j + 1, i + 1, "-", div, zahl_1 if check else None, zahl_2 if check else None), print_=False, nur_pfeil=True).strip())

                if _ > max_len[0]:
                    max_len[0] = _

        n = A.find_non_0(sarr_start=i + 1)

        if n != i + 1 and n is not False:
            A.swap(i + 1, n)

    # ZSF erreicht ------
    zsf = time.time()

    # Eleminieren über den Köpfen ------
    for i in reversed(range(1, A.dim_n)):
        for j in reversed(range(i)):
            n = A.find_non_0(i)

            if n is False or round(A.A[j][n], prec_int) == 0:
                continue

            zahl_1 = A.A[j][n]
            zahl_2 = A.A[i][n]

            div = A.A[j][n] / A.A[i][n]

            for k in range(A.dim_m):
                A.A[j][k] -= div * A.A[i][k]

            A.b[j] -= div * A.b[i]

            if pretty and rechenweg:
                check = round(div, prec_int) != int(div)
                _ = len(A.display(prec, pfeil=True, overset=dis.gauss_overset(j + 1, i + 1, "-", div, zahl_1 if check else None, zahl_2 if check else None), print_=False, nur_pfeil=True).strip())

                if _ > max_len[1]:
                    max_len[1] = _
    # Eleminieren über den Köpfen erreicht ------

    elem = time.time()

    # Normieren ------
    for i in range(A.dim_n):
        n = A.find_non_0(i)

        div = 1 / A.A[i][n] if A.A[i][n] else 0
        zahl_2 = A.A[i][n]

        if n is False or round(div, prec_int) == 1:
            continue

        for j in range(A.dim_m):
            A.A[i][j] *= div

        A.b[i] *= div

        if pretty and rechenweg:
            check = round(div, prec_int) != int(div)
            _ = len(A.display(prec, pfeil=True, overset=dis.gauss_overset(j + 1, i + 1, "*", div, 1 if check else None, zahl_2 if check else None), print_=False, min_len_pfeil=max_len[2], nur_pfeil=True).strip())

            if _ > max_len[2]:
                max_len[2] = _
    # Normieren erreicht ------

    norm = time.time()

    for i in range(A.dim_n):
        if A.find_non_0(i) is False and round(A.b[i], prec_int) != 0:
            lsg = ["keine"]
            break

    else:
        if not A.pos_NKV():
            lsg = ["eind", A.b]

        else:
            pos_KV = A.pos_KV()
            pos_NKV = A.pos_NKV()

            x = [[0 for j in range(A.dim_m)] for _ in range(len(pos_NKV))]

            for i, item in enumerate(pos_NKV):
                x[i][item] = 1

            for i, NKV in enumerate(pos_NKV):
                for j, KV in enumerate(pos_KV):
                    x[i][j] -= A.A[j][NKV]

            chk = param and len(param) >= len(pos_NKV)
            if chk:
                param.reverse()
                if param[0] == "":
                    param.pop(0)

            for i, item in enumerate(pos_NKV):
                if chk:
                    x[i].insert(0, param[i])
                else:
                    x[i].insert(0, std.übersetzung_zahl_param(item + 1))

            if A.find_non_0(b=True) is not False:
                # Spezielle Lösung existiert
                spez_lsg = []
                n = 0

                for j in range(A.dim_m):
                    if j in pos_KV:
                        spez_lsg.append(A.b[n])
                        n += 1
                    else:
                        spez_lsg.append(0)

                spez_lsg.insert(0, "spez")
                x.insert(0, spez_lsg)

            lsg = ["unend", x]

    if rechenweg:
        A = copy.deepcopy(A_old)

        if intro:
            cprint(f"Gauss Algorithmus für eine {A.dim_n} × {A.dim_m} Matrix:\n", abs_far)

        print("Als erstes die Zeilenstufenform erreichen:\n")

        n = A.find_non_0()
        if n != 0:
            A.swap(0, n)
            A.display(prec, pfeil=True, overset=dis.gauss_overset(1, n + 1, "tausch"), min_len_pfeil=max_len[0])
            print()

        # ZSF ------
        for i in range(A.dim_n - 1):
            for j in range(i + 1, A.dim_n):
                n = A.find_non_0(i)
                if round(A.A[j][n], prec_int) == 0:
                    continue

                div = A.A[j][n] / A.A[i][n]

                zahl_1 = A.A[j][n]
                zahl_2 = A.A[i][n]

                for k in range(A.dim_m):
                    A.A[j][k] -= div * A.A[i][k]

                A.b[j] -= div * A.b[i]

                check = round(div, prec_int) != int(div)
                _ = len(A.display(prec, pfeil=True, overset=dis.gauss_overset(j + 1, i + 1, "-", div, zahl_1 if check else None, zahl_2 if check else None), min_len_pfeil=max_len[0], nur_pfeil=True).strip())

                if pretty is False and _ > max_len[0]:
                    max_len[0] = _

                print()

            n = A.find_non_0(sarr_start=i + 1)

            if n != i + 1 and n is not False:
                A.swap(i + 1, n)
                _ = len(A.display(prec, pfeil=True, overset=dis.gauss_overset(i + 2, n + 1, "tausch"), min_len_pfeil=max_len[0], nur_pfeil=True).strip())

                if pretty is False and _ > max_len[0]:
                    max_len[0] = _

                print()

        # ZSF erreicht ------

        # ZSF Fertig
        cprint("Damit haben wir die Zeilenstufenform erreicht:\n", abs_far)
        A.display(prec, color=zwi_far)

        print("\n")
        print(colored("Jetzt die Köpfe über den Zeilen eliminieren:\n", abs_far))

        # Eleminieren über den Köpfen ------
        for i in reversed(range(1, A.dim_n)):
            for j in reversed(range(i)):
                n = A.find_non_0(i)

                if n is False or round(A.A[j][n], prec_int) == 0:
                    continue

                div = A.A[j][n] / A.A[i][n]

                zahl_1 = A.A[j][n]
                zahl_2 = A.A[i][n]

                for k in range(A.dim_m):
                    A.A[j][k] -= div * A.A[i][k]

                A.b[j] -= div * A.b[i]

                check = round(div, prec_int) != int(div)

                _ = len(A.display(prec, pfeil=True, overset=dis.gauss_overset(j + 1, i + 1, "-", div, zahl_1 if check else None, zahl_2 if check else None), min_len_pfeil=max_len[1], nur_pfeil=True).strip())

                if pretty is False and _ > max_len[1]:
                    max_len[1] = _

                print()
        # Eleminieren über den Köpfen erreicht ------

        # Fast NZSF Fertig, jetzt normieren
        print(colored("Jetzt die Köpfe Normieren:\n", abs_far))

        # Normieren ------
        for i in range(A.dim_n):
            n = A.find_non_0(i)

            div = 1 / A.A[i][n] if A.A[i][n] else 0

            if n is False or round(div, prec_int) == 1:
                continue

            zahl_2 = A.A[i][n]

            for j in range(A.dim_m):
                A.A[i][j] *= div

            A.b[i] *= div

            check = round(div, prec_int) != int(div)
            _ = len(A.display(prec, pfeil=True, overset=dis.gauss_overset(j + 1, i + 1, "*", div, 1 if check else None, zahl_2 if check else None), min_len_pfeil=max_len[2], nur_pfeil=True).strip())

            if pretty is False and _ > max_len[2]:
                max_len[2] = _

            print()
        # Normieren erreicht ------

        print(colored("Damit ist die NZSF erreicht:\n", abs_far))
        A.display(prec, color=zwi_far)

        lgs_list = copy.deepcopy(A.A)
        for i in range(A.dim_n):
            lgs_list[i].append(A.b[i])

        if lsg[0] != "keine":
            print("\n")
            cprint(f"Jetzt das LGS aufstellen um die Spezielle Lösung{' und Kern' if lsg[0] == 'unend' else ''} ablesen zu können:\n")

            dis.lgs(lgs_list, prec, operation="+", zeilen=True)

        if lsg[0] == "unend":
            print("\n")
            print(colored("Damit kommt man auf das LGS:\n", abs_far))
            dis.lgs(lgs_list, prec, operation="+", zeilen=True, nach_KV_umstellen=True)

        if lsg[0] != "keine":
            print("\n")
            cprint(f"Jetzt kann man die spezielle Lösung{' und den Kern' if lsg[0] == 'unend' else ''} ablesen:")

        print()

    if print_lsg or rechenweg:
        dis.lgs_lösung(lsg, 3, color=end_far, zeilen=False)

    if debugzeiten:
        print("\n\nDebugzeiten:")
        print(f"Done ZSF  in {zsf - start:.5f}s")
        print(f"Done Elem in {elem - zsf:.5f}s")
        print(f"Done Norm in {norm - elem:.5f}s")

        print("\n")
        print(f"Gesamt: {time.time() - start:.5f}s")
        print(lsg)

    return lsg


# /Gauss-----------------------------------


if __name__ == '__main__':
    X = cla.Ebene([[1, 2, 3], [4, 5, 6], [7, 8, 9]], pfeil=True)
    X.display(3, darst="norm")
