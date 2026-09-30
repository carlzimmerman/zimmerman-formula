"""Numerical (mpmath, 50 digits) helpers for the dS C-metric in the Dias-Lemos form used in PREDECLARED.md.
   G(x) = 1 - x^2 - 2 s x^3,  F(y) = -(1 + h^2) + y^2 - 2 s y^3,  s = m A, h = H/A = 1/(ell A).
   q = a0/(cH) with a0 := A is 1/h."""
import mpmath as mp

mp.mp.dps = 50
SQRT27_INV = 1 / mp.sqrt(27)


def G_roots(s):
    """real roots of G(x) = 0, returned as (x_minus, x_s, x_n) with x_minus < x_s < 0 < x_n  (0 < s < 1/sqrt 27)"""
    s = mp.mpf(s)
    r = mp.polyroots([2 * s, 1, 0, -1], maxsteps=400, extraprec=200)
    r = sorted([mp.re(z) for z in r])
    return r[0], r[1], r[2]


def Gp(x, s):
    return -2 * x - 6 * s * x**2


def kappa_reg_north(s):
    xm, xs, xn = G_roots(s)
    return 2 / abs(Gp(xn, s))


def mu_string_south(s):
    """tension of the string on the south axis when the north pole is regular (family R1)"""
    xm, xs, xn = G_roots(s)
    return (1 - abs(Gp(xs, s)) / abs(Gp(xn, s))) / 4


def mu_at(s, pole, kappa):
    xm, xs, xn = G_roots(s)
    x = xn if pole == "n" else xs
    return (1 - (kappa / 2) * abs(Gp(x, s))) / 4


def F_roots(s, h):
    """roots of F(y) = -(1+h^2) + y^2 - 2 s y^3, sorted; all real iff 27 s^2 (1+h^2) <= 1"""
    s = mp.mpf(s); h = mp.mpf(h)
    r = mp.polyroots([-2 * s, 1, 0, -(1 + h**2)], maxsteps=400, extraprec=200)
    return sorted(r, key=lambda z: (mp.re(z)))


def Fp(y, s, h):
    return 2 * y - 6 * s * y**2


def horizon_area_over_4piL2(s, h, kappa=None):
    """a := H^2 Area / (4 pi) of the acceleration/cosmological horizon y = y2 (in the R1 family, north regular)"""
    xm, xs, xn = G_roots(s)
    if kappa is None:
        kappa = kappa_reg_north(s)
    y = F_roots(s, h)
    y2 = mp.re(y[1])
    return (mp.mpf(h) ** 2 * kappa / 2) * (1 / (xs + y2) - 1 / (xn + y2))


def h_extremal(s):
    return mp.sqrt(1 / (27 * mp.mpf(s) ** 2) - 1)
