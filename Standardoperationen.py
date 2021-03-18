import AnalytischeGeometrie.Berechnungen as ber


def standardoperationen(inp, operation, rechenweg, darst=None):
    print()
    if operation == 1:
        # Vektor aus zwei Punkten berechnen
        P, Q = inp
        ber.vektor_zwei_punkte(P, Q, rechenweg, intro=True, end=True, ende=True)

    elif operation == 2:
        # Gerade aus zwei Punkten berechnen
        P, Q = inp
        ber.gerade_zwei_punkte(P, Q, rechenweg, intro=True, end=True, ende=True)

    elif operation == 3:
        # Ebene aus drei Punkten berechnen
        P, Q, T = inp
        ber.ebene_drei_punkte(P, Q, T, rechenweg, intro=True, end=True, ende=True)

    elif operation == 4:
        # Betrag eines Vektors berechnen
        u = inp[0]
        ber.absvec(u, rechenweg, intro=True, end=True, ende=True)

    elif operation == 5:
        # Normalenvektor berechnen
        u, v = inp
        n = ber.conv_norm(u, v, rechenweg, intro=True, end=True, ende=True)

    elif operation == 6:
        # Normaleneinheitsvektor berechnen
        u, v = inp
        ber.conv_norm0(u, v, rechenweg, intro=True, end=True, ende=True)

    elif operation == 7:
        # Skalarprodukt berechnen
        u, v = inp
        ber.skalarprodukt(u, v, rechenweg, intro=True, end=True, ende=True)

    elif operation == 8:
        # Lineare Abhängigkeit testen
        u, v = inp
        ber.linear_abhangig(u, v, rechenweg, intro=True, end=True, ende=True)

    elif operation == 9:
        # Punktprobe von Punkt und Gerade
        P, g = inp
        ber.punktprobe_pg(P, g, rechenweg, intro=True, end=True, ende=True)

    elif operation == 10:
        # Punktprobe von Punkt Ebene
        P, E = inp
        ber.punktprobe_pE(P, E, rechenweg, intro=True, end=True, ende=True)

    elif operation == 11:
        # Schnittpunkt zweier Geraden berechnen
        g, h = inp
        ber.schnitt(g, h, typ=["gerade", "gerade"], rechenweg=rechenweg, intro=True, end=True, ende=True)

    elif operation == 12:
        # Schnittpunkt von Gerade und Ebene berechnen
        g, E = inp
        ber.schnitt(g, E, typ=["gerade", "ebene"], rechenweg=rechenweg, intro=True, end=True, ende=True)


    elif operation == 13:
        # Schnittpunkt zweier Ebenen berechnen
        E, F = inp
        ber.schnitt(E, F, typ=["ebene", "ebene"], rechenweg=rechenweg, intro=True, end=True, ende=True)



    elif operation == 14:
        # Schnittwinkel zweier Geraden berechnen
        g, h = inp
        ber.schnittwinkel(g, h, rechenweg, typ=["gerade", "gerade"], intro=True, end=True, ende=True)

    elif operation == 15:
        # Schnittwinkel von Gerade und Ebene berechnen
        g, E = inp
        ber.schnittwinkel(g, E, rechenweg, typ=["gerade", "ebene"], intro=True, end=True, ende=True)

    elif operation == 16:
        # Schnittwinkel zweier Ebenen berechnen
        E, F = inp
        ber.schnittwinkel(E, F, rechenweg, typ=["ebene", "ebene"], intro=True, end=True, ende=True)

    elif operation == 17:
        # Umrechnung zwischen Ebenengleichungen
        E = inp[0]
        E.umrechnen(darst[0], darst[1], rechenweg, intro=True, end=True, ende=True)

    elif operation == 18:
        # Sind die eingebenen Ebenen gleich?
        ber.ebenen_gleich(inp[0], inp[1], rechenweg, intro=True, end=True, ende=True)

    elif operation == 19:
        # Abstand zwischen Punkt und Gerade
        P, g = inp
        ber.dist(P, g, typ=["punkt", "gerade"], rechenweg=rechenweg, intro=True, end=True, ende=True)

    elif operation == 20:
        # Abstand von zwei Geraden berechnen
        g, h = inp
        ber.dist(g, h, typ=["punkt", "gerade"], rechenweg=rechenweg, intro=True, end=True, ende=True)

    elif operation == 21:
        # Abstand von Punkt und Ebene
        P, E = inp
        ber.dist(P, E, typ=["punkt", "ebene"], rechenweg=rechenweg, intro=True, end=True, ende=True)

    elif operation == 22:
        # Abstand von Gerade und Ebene
        g, E = inp
        ber.dist(g, E, typ=["gerade", "ebene"], rechenweg=rechenweg, intro=True, end=True, ende=True)

    elif operation == 23:
        # Abstand von Ebene und Ebene
        E, F = inp
        ber.dist(E, F, typ=["ebene", "ebene"], rechenweg=rechenweg, intro=True, end=True, ende=True)


def standardoperationen_lagl(inp, operation, rechenweg, darst=False):
    """Standardoperationen für Lineare Algebra"""
    print()

    if operation == 1:
        # Matrix Multiplikation
        A, B = inp
        x = ber.matmul(A, B, zeilen=True, rechenweg=rechenweg, intro=True, end=True, ende=True)
    elif operation == 2:
        # Gauss Algorithmus einer nxm Matrix
        A = inp[0]
        x = ber.gauss(A, zeilen=True, rechenweg=rechenweg, intro=True, end=True, ende=True, debugzeiten=True)
        # print(x)
