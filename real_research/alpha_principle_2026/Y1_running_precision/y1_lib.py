"""y1_lib -- shared machinery of lane Y1 (declared in Y1_PREREGISTRATION.md).  Not a script; imported by y1_1 ... y1_5.

WHAT IS HERE AND WHERE EACH COEFFICIENT COMES FROM  (every number is a printed coefficient of the named source, a PDG number, or an integer / pi / zeta_3):
* Gauge beta functions, four forms typed independently (they are compared in y1_1):
    form D : Davies-Herren-Poole-Steinhauser-Thomsen arXiv:1912.07624, one- to FOUR-loop, alpha_b = alpha_tau = 0, in alpha_i/pi variables.
    form M : Mihaila-Salomon-Steinhauser arXiv:1208.3357 (long paper), one- to three-loop with the traces tr T, tr B, tr L, n_G and lambda-hat.
    form S : Mihaila-Salomon-Steinhauser arXiv:1201.5868 (letter), one- to three-loop, alpha_b = alpha_tau = 0, n_G, n_t.
    form B : Buttazzo et al. arXiv:1307.3536 Appendix B, one- to three-loop in g_i^2 variables (y_b, y_tau at one and two loops).
  The running uses M for loops 1-3 (it contains alpha_b, alpha_tau) and D for the four-loop term (alpha_b = alpha_tau = 0 there).
* y_t^2, y_b^2, y_tau^2, lambda beta functions: Buttazzo Appendix B (y_t, lambda to three loops with the printed DECIMAL coefficients -- the paper's own numerical transcription of the
  Chetyrkin-Zoller / Bednyakov et al. results, which were NOT read here; y_b, y_tau to two loops).  The two-loop y_t, y_b, y_tau betas are cross-checked against the Mihaila long paper (y1_1).
* Matching at mu = M_t: Buttazzo's interpolation formulas of their Sec. 3 (NNLO electroweak + three-loop QCD, which they state) and the analytic one-loop weak-coupling thresholds of their Appendix A.
* QCD: RunDec hep-ph/0004189 beta_0..beta_3 (eq. 2) and the three-loop decoupling (eqs. 19-25).
Conventions: state u = (g1^2, g2^2, g3^2, yt^2, yb^2, ytau^2, lambda) with g1^2 = (5/3) gY^2 (GUT normalised), V = lambda |H|^4; rhs is d u / d ln mu^2.
a_Y = 4 pi / gY^2 = (5/3)(4 pi / g1^2), a_2 = 4 pi / g2^2, a_3 = 4 pi / g3^2.
"""
import sys
sys.dont_write_bytecode = True
import math
from fractions import Fraction as Fr
import numpy as np
from scipy.integrate import solve_ivp, quad

PI = math.pi
ZETA2 = PI ** 2 / 6
ZETA3 = 1.2020569031595942
FOURPI = 4 * PI

# ------------------------------------------------------------------------------------------------ polynomial machinery
# variables: index 0..6 = alpha_1, alpha_2, alpha_3, alpha_t, alpha_b, alpha_tau, lambda-hat (= lambda / 4 pi)
TOK = {"1": 0, "2": 1, "3": 2, "t": 3, "b": 4, "T": 5, "l": 6}


def mono(s):
    e = [0] * 7
    for ch in s:
        e[TOK[ch]] += 1
    return tuple(e)


def F(x):
    return float(x)


def fr(a, b=1):
    return Fr(a, b)


# ---------------- form D  (arXiv:1912.07624): entries (rational, zeta3 coefficient, monomial); bracket_ell multiplies alpha_i^2/(4 pi)^(ell+1)
D_BR = {
    1: {
        1: [(fr(82, 5), 0, "")],
        2: [(fr(398, 25), 0, "1"), (fr(54, 5), 0, "2"), (fr(176, 5), 0, "3"), (fr(-34, 5), 0, "t")],
        3: [(fr(-388613, 6000), 0, "11"), (fr(123, 40), 0, "12"), (fr(-548, 75), 0, "13"), (fr(789, 16), 0, "22"), (fr(-12, 5), 0, "23"), (fr(1188, 5), 0, "33"),
            (fr(-2827, 200), 0, "1t"), (fr(-471, 8), 0, "2t"), (fr(-116, 5), 0, "3t"), (fr(189, 4), 0, "tt"), (fr(54, 25), 0, "1l"), (fr(18, 5), 0, "2l"), (fr(-36, 5), 0, "ll")],
        4: [(fr(-143035709, 1080000), fr(-1638851, 5625), "111"), (fr(-3819731, 24000), fr(16529, 125), "112"), (fr(-3629273, 6750), fr(720304, 1125), "113"),
            (fr(572059, 14400), fr(-6751, 75), "122"), (fr(-69, 25), 0, "123"), (fr(333556, 675), fr(-274624, 225), "133"), (fr(-117923, 2880), fr(-3109, 5), "222"),
            (fr(-41971, 90), fr(7472, 15), "223"), (fr(-1748, 3), fr(2944, 5), "233"), (fr(6116, 15), fr(-18560, 9), "333"),
            (fr(8978897, 72000), fr(2598, 125), "11t"), (fr(-42841, 800), fr(-1122, 25), "12t"), (fr(-2012, 75), fr(408, 25), "13t"), (fr(-439841, 960), fr(616, 5), "22t"),
            (fr(1468, 5), fr(-1896, 5), "23t"), (fr(-11462, 45), fr(3184, 5), "33t"), (fr(29059, 160), fr(-357, 25), "1tt"), (fr(71463, 160), fr(639, 5), "2tt"),
            (fr(1429, 5), fr(-240), "3tt"), (fr(-13653, 40), fr(-102, 5), "ttt"),
            (fr(3627, 500), 0, "11l"), (fr(1917, 50), 0, "12l"), (fr(889, 20), 0, "22l"), (fr(-1926, 25), 0, "1tl"), (fr(-162, 5), 0, "2tl"), (fr(-474, 5), 0, "ttl"),
            (fr(-1269, 25), 0, "1ll"), (fr(-981, 5), 0, "2ll"), (fr(1188, 5), 0, "tll"), (fr(624, 5), 0, "lll")],
    },
    2: {
        1: [(fr(-38, 3), 0, "")],
        2: [(fr(18, 5), 0, "1"), (fr(70, 3), 0, "2"), (fr(48), 0, "3"), (fr(-6), 0, "t")],
        3: [(fr(-5597, 400), 0, "11"), (fr(873, 40), 0, "12"), (fr(-4, 5), 0, "13"), (fr(324953, 432), 0, "22"), (fr(156), 0, "23"), (fr(324), 0, "33"),
            (fr(-593, 40), 0, "1t"), (fr(-729, 8), 0, "2t"), (fr(-28), 0, "3t"), (fr(147, 4), 0, "tt"), (fr(6, 5), 0, "1l"), (fr(6), 0, "2l"), (fr(-12), 0, "ll")],
        4: [(fr(-6418229, 72000), fr(21173, 375), "111"), (fr(-787709, 4800), fr(659, 25), "112"), (fr(-52297, 450), fr(2032, 15), "113"), (fr(161, 5), 0, "123"),
            (fr(-375767, 2880), fr(4631, 15), "122"), (fr(-1748, 9), fr(2944, 15), "133"), (fr(124660945, 15552), fr(-78803, 9), "222"), (fr(-72881, 18), fr(16432, 3), "223"),
            (fr(10348, 3), fr(-2560), "233"), (fr(1028, 3), fr(-7040, 3), "333"),
            (fr(465089, 4800), fr(-498, 25), "11t"), (fr(-102497, 480), fr(-28), "12t"), (fr(796, 15), fr(-376, 5), "13t"), (fr(-500665, 576), fr(478, 3), "22t"),
            (fr(-1444, 3), fr(-56), "23t"), (fr(-614, 3), fr(336), "33t"), (fr(3161, 32), fr(153, 5), "1tt"), (fr(30213, 32), fr(-63), "2tt"), (fr(239), fr(-144), "3tt"),
            (fr(-2143, 8), fr(-18), "ttt"),
            (fr(457, 100), 0, "11l"), (fr(69, 2), 0, "12l"), (fr(2905, 12), 0, "22l"), (fr(-54, 5), 0, "1tl"), (fr(-150), 0, "2tl"), (fr(-78), 0, "ttl"),
            (fr(-327, 5), 0, "1ll"), (fr(-363), 0, "2ll"), (fr(300), 0, "tll"), (fr(208), 0, "lll")],
    },
    3: {
        1: [(fr(-28), 0, "")],
        2: [(fr(22, 5), 0, "1"), (fr(18), 0, "2"), (fr(-104), 0, "3"), (fr(-8), 0, "t")],
        3: [(fr(-523, 30), 0, "11"), (fr(-3, 10), 0, "12"), (fr(109, 2), 0, "22"), (fr(308, 15), 0, "13"), (fr(84), 0, "23"), (fr(130), 0, "33"),
            (fr(-101, 10), 0, "1t"), (fr(-93, 2), 0, "2t"), (fr(-160), 0, "3t"), (fr(60), 0, "tt")],
        4: [(fr(-6085099, 54000), fr(17473, 225), "111"), (fr(-46951, 1200), fr(973, 25), "112"), (fr(-35542, 135), fr(902, 9), "113"), (fr(69, 5), 0, "123"),
            (fr(-37597, 720), fr(691, 15), "122"), (fr(-57739, 135), fr(32476, 45), "133"), (fr(-176815, 432), fr(-935), "222"), (fr(3812, 9), fr(-950, 3), "223"),
            (fr(-5969, 3), fr(3476), "233"), (fr(127118, 9), fr(-179792, 9), "333"),
            (fr(362287, 3600), fr(-19, 25), "11t"), (fr(77, 40), fr(-54), "12t"), (fr(-1283, 15), fr(-32, 5), "13t"), (fr(-12887, 48), fr(117), "22t"),
            (fr(-473), fr(-288), "23t"), (fr(-26836, 9), fr(1088), "33t"), (fr(3641, 40), fr(42, 5), "1tt"), (fr(3201, 8), fr(90), "2tt"), (fr(1708), fr(-384), "3tt"),
            (fr(-423), fr(-24), "ttt"), (fr(-120), 0, "ttl"), (fr(144), 0, "tll")],
    },
}


def _poly_from_D(i, ell):
    return [(F(c) + F(z) * ZETA3, mono(m)) for (c, z, m) in D_BR[i][ell]]


# ---------------- form M  (arXiv:1208.3357): coefficients as (c0, c1, c2) multiplying 1, n_G, n_G^2 ; tr B^2 and (tr B)^2 etc. are both alpha_b^2 for the diagonal third generation
def _c(a=0, b=0, c=0):
    return (Fr(a), Fr(b), Fr(c))


M_BR = {
    1: {
        1: {"": _c(fr(2, 5), fr(16, 3))},
        2: {"1": _c(fr(18, 25), fr(76, 15)), "2": _c(fr(18, 5), fr(12, 5)), "3": _c(0, fr(176, 15)), "t": _c(fr(-34, 5)), "b": _c(-2), "T": _c(-6)},
        3: {"11": _c(fr(489, 2000), fr(-232, 75), fr(-836, 135)), "12": _c(fr(783, 200), fr(-7, 25)), "22": _c(fr(3401, 80), fr(166, 15), fr(-44, 15)),
            "1l": _c(fr(54, 25)), "2l": _c(fr(18, 5)), "ll": _c(fr(-36, 5)),
            "1t": _c(fr(-2827, 200)), "2t": _c(fr(-471, 8)), "3t": _c(fr(-116, 5)),
            "1b": _c(fr(-1267, 200)), "2b": _c(fr(-1311, 40)), "3b": _c(fr(-68, 5)),
            "1T": _c(fr(-2529, 200)), "2T": _c(fr(-1629, 40)),
            "bb": _c(fr(183, 20) + fr(51, 10)), "bT": _c(fr(157, 5)), "TT": _c(fr(261, 20) + fr(99, 10)),
            "tb": _c(fr(3, 2) + fr(177, 5)), "tt": _c(fr(339, 20) + fr(303, 10)), "tT": _c(fr(199, 5)),
            "13": _c(0, fr(-548, 225)), "23": _c(0, fr(-4, 5)), "33": _c(0, fr(1100, 9), fr(-1936, 135))},
    },
    2: {
        1: {"": _c(fr(-86, 3), fr(16, 3))},
        2: {"1": _c(fr(6, 5), fr(4, 5)), "2": _c(fr(-518, 3), fr(196, 3)), "3": _c(0, 16), "t": _c(-6), "b": _c(-6), "T": _c(-2)},
        3: {"11": _c(fr(163, 400), fr(-28, 15), fr(-44, 45)), "12": _c(fr(561, 40), fr(13, 5)), "22": _c(fr(-667111, 432), fr(25648, 27), fr(-1660, 27)),
            "1l": _c(fr(6, 5)), "2l": _c(6), "ll": _c(-12),
            "1t": _c(fr(-593, 40)), "2t": _c(fr(-729, 8)), "3t": _c(-28),
            "1b": _c(fr(-533, 40)), "2b": _c(fr(-729, 8)), "3b": _c(-28),
            "1T": _c(fr(-51, 8)), "2T": _c(fr(-243, 8)),
            "bb": _c(fr(57, 4) + fr(45, 2)), "bT": _c(15), "TT": _c(fr(19, 4) + fr(5, 2)),
            "tb": _c(fr(27, 2) + 45), "tt": _c(fr(57, 4) + fr(45, 2)), "tT": _c(15),
            "13": _c(0, fr(-4, 15)), "23": _c(0, 52), "33": _c(0, fr(500, 3), fr(-176, 9))},
    },
    3: {
        1: {"": _c(-44, fr(16, 3))},
        2: {"3": _c(-408, fr(304, 3)), "1": _c(0, fr(22, 15)), "2": _c(0, 6), "t": _c(-8), "b": _c(-8)},
        3: {"33": _c(-5714, fr(20132, 9), fr(-2600, 27)), "11": _c(0, fr(-13, 30), fr(-242, 135)), "12": _c(0, fr(-1, 10)), "22": _c(0, fr(241, 6), fr(-22, 3)),
            "13": _c(0, fr(308, 45)), "23": _c(0, 28),
            "1t": _c(fr(-101, 10)), "2t": _c(fr(-93, 2)), "3t": _c(-160),
            "1b": _c(fr(-89, 10)), "2b": _c(fr(-93, 2)), "3b": _c(-160),
            "bb": _c(18 + 42), "bT": _c(14), "tb": _c(-12 + 84), "tt": _c(18 + 42), "tT": _c(14)},
    },
}


def _poly_from_M(i, ell, nG=3):
    out = []
    for m, (c0, c1, c2) in M_BR[i][ell].items():
        out.append((F(c0 + c1 * nG + c2 * nG * nG), mono(m)))
    return out


_POLY_CACHE = {}


def gauge_poly(i, ell, source):
    key = (i, ell, source)
    if key not in _POLY_CACHE:
        pl = _poly_from_D(i, ell) if source == "D" else _poly_from_M(i, ell)
        coef = np.array([c for c, _ in pl])
        ex = np.array([e for _, e in pl], dtype=float)
        _POLY_CACHE[key] = (coef, ex)
    return _POLY_CACHE[key]


def beta_alpha_pi(alpha, loops, bt=True, mutate=False, drop3=()):
    """(beta_1, beta_2, beta_3) = mu^2 d/dmu^2 (alpha_i / pi) for alpha = (a1, a2, a3, at, ab, atau, alam) (alam = lambda/4pi).
    loops 1-3: form M (includes alpha_b, alpha_tau unless bt=False); loop 4 adds form D's four-loop bracket (alpha_b = alpha_tau = 0 there)."""
    al = np.array(alpha, dtype=float)
    if not bt:
        al = al.copy()
        al[4] = 0.0
        al[5] = 0.0
    out = []
    for i in (1, 2, 3):
        tot = 0.0
        for ell in range(1, min(loops, 3) + 1):
            coef, ex = gauge_poly(i, ell, "M")
            if mutate and i == 1 and ell == 3:
                coef = coef.copy()
                coef[np.argmax(np.abs(coef))] *= -1.0          # MUTATE: flip the sign of the largest three-loop coefficient
            a_use = al
            if ell == 3 and drop3:
                a_use = al.copy()
                for j in drop3:
                    a_use[j] = 0.0                             # diagnostic: switch off selected couplings in the three-loop bracket only
            tot += (np.prod(a_use[None, :] ** ex, axis=1) @ coef) / (4 * PI) ** (ell + 1)
        if loops >= 4:
            coef, ex = gauge_poly(i, 4, "D")
            a4 = al.copy()
            a4[4] = 0.0
            a4[5] = 0.0
            tot += (np.prod(a4[None, :] ** ex, axis=1) @ coef) / (4 * PI) ** 5
        out.append(al[i - 1] ** 2 * tot)
    return np.array(out)


def beta_D_alpha_pi(alpha, loops):
    """form D only (alpha_b = alpha_tau = 0): loops 1..4, for the cross-checks."""
    al = np.array(alpha, dtype=float)
    out = []
    for i in (1, 2, 3):
        tot = 0.0
        for ell in range(1, loops + 1):
            coef, ex = gauge_poly(i, ell, "D")
            tot += (np.prod(al[None, :] ** ex, axis=1) @ coef) / (4 * PI) ** (ell + 1)
        out.append(al[i - 1] ** 2 * tot)
    return np.array(out)


def beta_M_alpha_pi(alpha, loops, nG=3):
    al = np.array(alpha, dtype=float)
    out = []
    for i in (1, 2, 3):
        tot = 0.0
        for ell in range(1, loops + 1):
            pl = _poly_from_M(i, ell, nG)
            coef = np.array([c for c, _ in pl])
            ex = np.array([e for _, e in pl], dtype=float)
            tot += (np.prod(al[None, :] ** ex, axis=1) @ coef) / (4 * PI) ** (ell + 1)
        out.append(al[i - 1] ** 2 * tot)
    return np.array(out)


# ---------------- form S  (arXiv:1201.5868 letter; alpha_b = alpha_tau = 0; nG, nt).  x_i = alpha_i/pi ; xl = lambda/(4 pi^2)
def beta_S_alpha_pi(alpha, nG=3, nt=1):
    a1, a2, a3, at, _ab, _atau, al = [float(v) for v in alpha]
    x1, x2, x3, xt = a1 / PI, a2 / PI, a3 / PI, at / PI
    xl = al / PI           # lambda/(4 pi^2) = alpha_lambda / pi
    b1 = x1 ** 2 * (1 / 40 + nG / 3 + x1 * (9 / 800 + 19 * nG / 240) + x2 * (9 / 160 + 3 * nG / 80) + x3 * (11 * nG / 60)
                    + x1 ** 2 * (489 / 512000 - 29 * nG / 2400 - 209 * nG ** 2 / 8640) + x1 * x2 * (783 / 51200 - 7 * nG / 6400) - x1 * x3 * (137 * nG / 14400)
                    + x2 ** 2 * (3401 / 20480 + 83 * nG / 1920 - 11 * nG ** 2 / 960) - x2 * x3 * (nG / 320) + x3 ** 2 * (275 * nG / 576 - 121 * nG ** 2 / 2160)
                    + nt * xt * (-17 / 160 - x1 * 2827 / 51200 - x2 * 471 / 2048 - x3 * 29 / 320 + xt * (339 / 5120 + 303 * nt / 2560))
                    + xl * (x1 * 27 / 3200 + x2 * 9 / 640 - xl * 9 / 320))
    b2 = x2 ** 2 * (-43 / 24 + nG / 3 + x1 * (3 / 160 + nG / 80) + x2 * (-259 / 96 + 49 * nG / 48) + x3 * nG / 4
                    + x1 ** 2 * (163 / 102400 - 7 * nG / 960 - 11 * nG ** 2 / 2880) + x1 * x2 * (561 / 10240 + 13 * nG / 1280) - x1 * x3 * nG / 960
                    + x2 ** 2 * (-667111 / 110592 + 1603 * nG / 432 - 415 * nG ** 2 / 1728) + x2 * x3 * 13 * nG / 64
                    + x3 ** 2 * (125 * nG / 192 - 11 * nG ** 2 / 144)
                    + nt * xt * (-3 / 32 - x1 * 593 / 10240 - x2 * 729 / 2048 - x3 * 7 / 64 + xt * (57 / 1024 + 45 * nt / 512))
                    + xl * (x1 * 3 / 640 + x2 * 3 / 128 - xl * 3 / 64))
    b3 = x3 ** 2 * (-11 / 4 + nG / 3 + x1 * 11 * nG / 480 + x2 * 3 * nG / 32 + x3 * (-51 / 8 + 19 * nG / 12)
                    + x1 ** 2 * (-13 * nG / 7680 - 121 * nG ** 2 / 17280) - x1 * x2 * nG / 2560 + x1 * x3 * 77 * nG / 2880
                    + x2 ** 2 * (241 * nG / 1536 - 11 * nG ** 2 / 384) + x2 * x3 * 7 * nG / 64
                    + x3 ** 2 * (-2857 / 128 + 5033 * nG / 576 - 325 * nG ** 2 / 864)
                    + nt * xt * (-1 / 8 - x1 * 101 / 2560 - x2 * 93 / 512 - x3 * 5 / 8 + xt * (9 / 128 + 21 * nt / 128)))
    return np.array([b1, b2, b3])


# ---------------- form B  (Buttazzo Appendix B): d g_i^2 / d ln mu^2 in g^2 variables
def gauge_B(u, loops):
    g1, g2, g3, yt, yb, ytau, lam = [float(v) for v in u]
    k = 1 / (4 * PI) ** 2
    d1 = g1 ** 2 * k * (41 / 10)
    d2 = g2 ** 2 * k * (-19 / 6)
    d3 = g3 ** 2 * k * (-7.0)
    if loops >= 2:
        d1 += g1 ** 2 * k ** 2 * (44 * g3 / 5 + 27 * g2 / 10 + 199 * g1 / 50 - 17 * yt / 10 - yb / 2 - 3 * ytau / 2)
        d2 += g2 ** 2 * k ** 2 * (12 * g3 + 35 * g2 / 6 + 9 * g1 / 10 - 3 * yt / 2 - 3 * yb / 2 - ytau / 2)
        d3 += g3 ** 2 * k ** 2 * (-26 * g3 + 9 * g2 / 2 + 11 * g1 / 10 - 2 * yt - 2 * yb)
    if loops >= 3:
        d1 += g1 ** 2 * k ** 3 * (yt * (189 * yt / 16 - 29 * g3 / 5 - 471 * g2 / 32 - 2827 * g1 / 800) + lam * (-9 * lam / 5 + 9 * g2 / 10 + 27 * g1 / 50)
                                  + 297 * g3 ** 2 / 5 + 789 * g2 ** 2 / 64 - 388613 * g1 ** 2 / 24000 - 3 * g3 * g2 / 5 - 137 * g3 * g1 / 75 + 123 * g2 * g1 / 160)
        d2 += g2 ** 2 * k ** 3 * (yt * (147 * yt / 16 - 7 * g3 - 729 * g2 / 32 - 593 * g1 / 160) + lam * (-3 * lam + 3 * g2 / 2 + 3 * g1 / 10)
                                  + 81 * g3 ** 2 + 324953 * g2 ** 2 / 1728 - 5597 * g1 ** 2 / 1600 + 39 * g3 * g2 - g3 * g1 / 5 + 873 * g2 * g1 / 160)
        d3 += g3 ** 2 * k ** 3 * (yt * (15 * yt - 40 * g3 - 93 * g2 / 8 - 101 * g1 / 40) + 65 * g3 ** 2 / 2 + 109 * g2 ** 2 / 8 - 523 * g1 ** 2 / 120
                                  + 21 * g3 * g2 + 77 * g3 * g1 / 15 - 3 * g2 * g1 / 40)
    return np.array([d1, d2, d3])


# ------------------------------------------------------------------------------------------------ Yukawa and lambda betas (Buttazzo Appendix B)
def yuk_lam_B(u, loops):
    g1, g2, g3, yt, yb, ytau, lam = [float(v) for v in u]
    k = 1 / (4 * PI) ** 2
    # ---- y_t^2
    t1 = yt * k * (9 * yt / 2 + 3 * yb / 2 + ytau - 8 * g3 - 9 * g2 / 4 - 17 * g1 / 20)
    t2 = t3 = 0.0
    if loops >= 2:
        t2 = yt * k ** 2 * (yt * (-12 * yt - 11 * yb / 4 - 9 * ytau / 4 - 12 * lam + 36 * g3 + 225 * g2 / 16 + 393 * g1 / 80)
                            + yb * (-yb / 4 + 5 * ytau / 4 + 4 * g3 + 99 * g2 / 16 + 7 * g1 / 80)
                            + ytau * (-9 * ytau / 4 + 15 * g2 / 8 + 15 * g1 / 8)
                            + 6 * lam ** 2 - 108 * g3 ** 2 - 23 * g2 ** 2 / 4 + 1187 * g1 ** 2 / 600 + 9 * g3 * g2 + 19 * g3 * g1 / 15 - 9 * g2 * g1 / 20)
    if loops >= 3:
        t3 = yt * k ** 3 * (yt ** 2 * (58.6028 * yt + 198 * lam - 157 * g3 - 1593 * g2 / 16 - 2437 * g1 / 80)
                            + lam * yt * (15 * lam / 4 + 16 * g3 - 135 * g2 / 2 - 127 * g1 / 10)
                            + yt * (363.764 * g3 ** 2 + 16.990 * g2 ** 2 - 24.422 * g1 ** 2 + 48.370 * g3 * g2 + 18.074 * g3 * g1 + 34.829 * g2 * g1)
                            + lam ** 2 * (-36 * lam + 45 * g2 + 9 * g1)
                            + lam * (-171 * g2 ** 2 / 16 - 1089 * g1 ** 2 / 400 + 117 * g2 * g1 / 40)
                            - 619.35 * g3 ** 3 + 169.829 * g2 ** 3 + 16.099 * g1 ** 3 + 73.654 * g3 ** 2 * g2 - 15.096 * g3 ** 2 * g1 - 21.072 * g3 * g2 ** 2
                            - 22.319 * g3 * g1 ** 2 - 321 / 20 * g3 * g2 * g1 - 4.743 * g2 ** 2 * g1 - 4.442 * g2 * g1 ** 2)
    dyt = t1 + t2 + t3
    # ---- y_b^2 (two loops)
    dyb = yb * k * (3 * yt / 2 + 9 * yb / 2 + ytau - 8 * g3 - 9 * g2 / 4 - g1 / 4)
    if loops >= 2:
        dyb += yb * k ** 2 * (yt * (-yt / 4 - 11 * yb / 4 + 5 * ytau / 4 + 4 * g3 + 99 * g2 / 16 + 91 * g1 / 80)
                              + yb * (-12 * yb - 9 * ytau / 4 - 12 * lam + 36 * g3 + 225 * g2 / 16 + 237 * g1 / 80)
                              + ytau * (-9 * ytau / 4 + 15 * g2 / 8 + 15 * g1 / 8)
                              + 6 * lam ** 2 - 108 * g3 ** 2 - 23 * g2 ** 2 / 4 - 127 * g1 ** 2 / 600 + 9 * g3 * g2 + 31 * g3 * g1 / 15 - 27 * g2 * g1 / 20)
    # ---- y_tau^2 (two loops)
    dytau = ytau * k * (3 * yt + 3 * yb + 5 * ytau / 2 - 9 * g2 / 4 - 9 * g1 / 4)
    if loops >= 2:
        dytau += ytau * k ** 2 * (6 * lam ** 2 - 23 * g2 ** 2 / 4 + 1371 * g1 ** 2 / 200 + 27 * g2 * g1 / 20
                                  + yt * (-27 * yt / 4 + 3 * yb / 2 - 27 * ytau / 4 + 20 * g3 + 45 * g2 / 8 + 17 * g1 / 8)
                                  + yb * (-27 * yb / 4 - 27 * ytau / 4 + 20 * g3 + 45 * g2 / 8 + 5 * g1 / 8)
                                  + ytau * (-3 * ytau - 12 * lam + 165 * g2 / 16 + 537 * g1 / 80))
    # ---- lambda
    l1 = k * (lam * (12 * lam + 6 * yt + 6 * yb + 2 * ytau - 9 * g2 / 2 - 9 * g1 / 10) - 3 * yt ** 2 - 3 * yb ** 2 - ytau ** 2
              + 9 * g2 ** 2 / 16 + 27 * g1 ** 2 / 400 + 9 * g2 * g1 / 40)
    l2 = l3 = 0.0
    if loops >= 2:
        l2 = k ** 2 * (lam ** 2 * (-156 * lam - 72 * yt - 72 * yb - 24 * ytau + 54 * g2 + 54 * g1 / 5)
                       + lam * yt * (-3 * yt / 2 - 21 * yb + 40 * g3 + 45 * g2 / 4 + 17 * g1 / 4)
                       + lam * yb * (-3 * yb / 2 + 40 * g3 + 45 * g2 / 4 + 5 * g1 / 4)
                       + lam * ytau * (-ytau / 2 + 15 * g2 / 4 + 15 * g1 / 4)
                       + lam * (-73 * g2 ** 2 / 16 + 1887 * g1 ** 2 / 400 + 117 * g2 * g1 / 40)
                       + yt ** 2 * (15 * yt - 3 * yb - 16 * g3 - 4 * g1 / 5)
                       + yt * (-9 * g2 ** 2 / 8 - 171 * g1 ** 2 / 200 + 63 * g2 * g1 / 20)
                       + yb ** 2 * (-3 * yt + 15 * yb - 16 * g3 + 2 * g1 / 5)
                       + yb * (-9 * g2 ** 2 / 8 + 9 * g1 ** 2 / 40 + 27 * g2 * g1 / 20)
                       + ytau ** 2 * (5 * ytau - 6 * g1 / 5)
                       + ytau * (-3 * g2 ** 2 / 8 - 9 * g1 ** 2 / 8 + 33 * g2 * g1 / 20)
                       + 305 * g2 ** 3 / 32 - 3411 * g1 ** 3 / 4000 - 289 * g2 ** 2 * g1 / 160 - 1677 * g2 * g1 ** 2 / 800)
    if loops >= 3:
        l3 = k ** 3 * (lam ** 3 * (6011.35 * lam + 873 * yt - 387.452 * g2 - 77.490 * g1)
                       + lam ** 2 * yt * (1768.26 * yt + 160.77 * g3 - 359.539 * g2 - 63.869 * g1)
                       + lam ** 2 * (-790.28 * g2 ** 2 - 185.532 * g1 ** 2 - 316.64 * g2 * g1)
                       + lam * yt ** 2 * (-223.382 * yt - 662.866 * g3 - 5.470 * g2 - 21.015 * g1)
                       + lam * yt * (356.968 * g3 ** 2 - 319.664 * g2 ** 2 - 74.8599 * g1 ** 2 + 15.1443 * g3 * g2 + 17.454 * g3 * g1 + 5.615 * g2 * g1)
                       + lam * g2 ** 2 * (-57.144 * g3 + 865.483 * g2 + 79.638 * g1)
                       + lam * g1 ** 2 * (-8.381 * g3 + 61.753 * g2 + 28.168 * g1)
                       + yt ** 3 * (-243.149 * yt + 250.494 * g3 + 74.138 * g2 + 33.930 * g1)
                       + yt ** 2 * (-50.201 * g3 ** 2 + 15.884 * g2 ** 2 + 15.948 * g1 ** 2 + 13.349 * g3 * g2 + 17.570 * g3 * g1 - 70.356 * g2 * g1)
                       + yt * g3 * (16.464 * g2 ** 2 + 1.016 * g1 ** 2 + 11.386 * g2 * g1)
                       + yt * g2 ** 2 * (62.500 * g2 + 13.041 * g1)
                       + yt * g1 ** 2 * (10.627 * g2 + 11.117 * g1)
                       + g3 * (7.536 * g2 ** 3 + 0.663 * g1 ** 3 + 1.507 * g2 ** 2 * g1 + 1.105 * g2 * g1 ** 2)
                       - 114.091 * g2 ** 4 - 1.508 * g1 ** 4 - 37.889 * g2 ** 3 * g1 + 6.500 * g2 ** 2 * g1 ** 2 - 1.543 * g2 * g1 ** 3)
    return dyt, dyb, dytau, l1 + l2 + l3


# ------------------------------------------------------------------------------------------------ the full rhs and the runner
QCD4_K = -2472.28          # Buttazzo Appendix B: dg_3^2/d ln mu^2 contains -2472.28 g_3^10/(4 pi)^8 (n_f = 6, checked against RunDec in y1_1)


class Opts:
    def __init__(self, gauge_loops=4, yuk_loops=3, bt=True, mutate=False, drop3=(), qcd4=False):
        self.qcd4 = qcd4                  # add only the pure-QCD four-loop term (Buttazzo's -2472.28 g3^10/(4 pi)^8) to a three-loop gauge run
        self.gauge_loops = gauge_loops
        self.yuk_loops = yuk_loops
        self.bt = bt
        self.mutate = mutate
        self.drop3 = tuple(drop3)


def rhs_lnmu2(u, o):
    g1, g2, g3, yt, yb, ytau, lam = [float(v) for v in u]
    alpha = (g1 / FOURPI, g2 / FOURPI, g3 / FOURPI, yt / FOURPI, yb / FOURPI, ytau / FOURPI, lam / FOURPI)
    b = beta_alpha_pi(alpha, o.gauge_loops, bt=o.bt, mutate=o.mutate, drop3=o.drop3)
    dg = 4 * PI ** 2 * b
    if o.qcd4 and o.gauge_loops == 3:
        dg[2] += QCD4_K * g3 ** 5 / (4 * PI) ** 8
    dyt, dyb, dytau, dlam = yuk_lam_B(u, o.yuk_loops)
    return np.array([dg[0], dg[1], dg[2], dyt, dyb, dytau, dlam])


def u_from_gY_g2_g3(gY, g2, g3, yt, yb, ytau, lam):
    return np.array([5.0 / 3.0 * gY ** 2, g2 ** 2, g3 ** 2, yt ** 2, yb ** 2, ytau ** 2, lam])


def a_from_u(u):
    return np.array([FOURPI / (3.0 / 5.0 * u[0]), FOURPI / u[1], FOURPI / u[2]])


class Traj:
    """Dense trajectory u(mu) for mu in [mu0, mu_max]; A(mu) = (a_Y, a_2, a_3)."""

    def __init__(self, u0, mu0, o, mu_max=1e21, rtol=1e-11, atol=1e-14):
        self.o = o
        self.mu0 = mu0
        f = lambda t, y: 2.0 * rhs_lnmu2(y, o)          # t = ln mu
        self.sol = solve_ivp(f, [math.log(mu0), math.log(mu_max)], list(u0), method="DOP853", rtol=rtol, atol=atol, dense_output=True)
        if self.sol.status != 0:
            raise RuntimeError("ODE failed: " + self.sol.message)
        self.lnmax = math.log(mu_max)

    def u(self, mu):
        return np.array(self.sol.sol(math.log(mu)))

    def A(self, mu):
        return a_from_u(self.u(mu))


# ------------------------------------------------------------------------------------------------ Buttazzo boundary at mu = M_t  (interpolation formulas, Sec. 3 of arXiv:1307.3536)
VEV = 246.21971            # (sqrt2 G_mu)^(-1/2), Buttazzo Table 1
MZ_BUT = 91.1876
YB_MT_SMDR = 0.015480097   # SMDR reference point, Q0 = 173.1 (arXiv:1907.02500 eq 1.11)
YTAU_MT_SMDR = 0.0099944422


def buttazzo_boundary(Mt=173.34, Mh=125.15, MW=80.384, als=0.1184, g3_override=None, dg2=0.0, dgY=0.0, dyt=0.0, dlam=0.0, yb=YB_MT_SMDR, ytau=YTAU_MT_SMDR):
    """Returns (u0 at mu = Mt, dict of the five printed couplings).  The d* arguments are additive shifts for the error budget."""
    sW = 0.014
    sa = 0.0007
    lam = 0.12604 + 0.00206 * (Mh - 125.15) - 0.00004 * (Mt - 173.34) + dlam
    yt = 0.93690 + 0.00556 * (Mt - 173.34) - 0.00042 * (als - 0.1184) / sa + dyt
    g2 = 0.64779 + 0.00004 * (Mt - 173.34) + 0.00011 * (MW - 80.384) / sW + dg2
    gY = 0.35830 + 0.00011 * (Mt - 173.34) - 0.00020 * (MW - 80.384) / sW + dgY
    g3 = 1.1666 + 0.00314 * (als - 0.1184) / sa - 0.00046 * (Mt - 173.34) if g3_override is None else g3_override
    u0 = u_from_gY_g2_g3(gY, g2, g3, yt, yb, ytau, lam)
    return u0, dict(gY=gY, g2=g2, g3=g3, yt=yt, lam=lam)


# ------------------------------------------------------------------------------------------------ one-loop weak-scale thresholds (Buttazzo Appendix A), real parts
def A0(M, mu):
    return M ** 2 * (1 - math.log(M ** 2 / mu ** 2))


def B0(p, M1, M2, mu):
    def f(x):
        arg = x * M1 ** 2 + (1 - x) * M2 ** 2 - x * (1 - x) * p ** 2
        arg = max(abs(arg), 1e-300)
        return -math.log(arg / mu ** 2)
    # integrable log singularities at most: split the interval finely
    pts = np.linspace(0, 1, 9)[1:-1]
    v, _ = quad(f, 0, 1, points=list(pts), limit=400, epsabs=1e-13, epsrel=1e-13)
    return v


def tree_couplings(MW, MZ, V=VEV):
    return 2 * MW / V, 2 * math.sqrt(MZ ** 2 - MW ** 2) / V


def threshold1_g2(mu, Mt, Mh, MW, MZ, V=VEV):
    k = 2 * MW / ((4 * PI) ** 2 * V ** 3)
    a0 = lambda M: A0(M, mu)
    b0 = lambda p, m1, m2: B0(p, m1, m2, mu)
    s = ((Mh ** 4 / (6 * MW ** 2) - 2 * Mh ** 2 / 3 + 2 * MW ** 2) * b0(MW, Mh, MW)
         + (-Mt ** 4 / MW ** 2 - Mt ** 2 + 2 * MW ** 2) * b0(MW, 0.0, Mt)
         + (1 / 6) * (-48 * MW ** 4 / MZ ** 2 + MZ ** 4 / MW ** 2 - 68 * MW ** 2 + 16 * MZ ** 2) * b0(MW, MW, MZ)
         + (1 / 6) * (Mh ** 2 * (9 / (Mh ** 2 - MW ** 2) + 1 / MW ** 2) + MZ ** 2 / MW ** 2 + MW ** 2 * (9 / (MW ** 2 - MZ ** 2) + 48 / MZ ** 2) - 27) * a0(MW)
         + (2 - Mh ** 2 * (Mh ** 2 + 8 * MW ** 2) / (6 * MW ** 2 * (Mh ** 2 - MW ** 2))) * a0(Mh)
         + (Mt ** 2 / MW ** 2 + 1) * a0(Mt)
         + (1 / 6) * (24 * MW ** 2 / MZ ** 2 - MZ ** 2 / MW ** 2 + 9 * MW ** 2 / (MZ ** 2 - MW ** 2) - 17) * a0(MZ)
         + (1 / 36) * (-3 * Mh ** 2 + 18 * Mt ** 2 + 288 * MW ** 4 / MZ ** 2 - 374 * MW ** 2 - 3 * MZ ** 2))
    return k * s


def threshold1_gY(mu, Mt, Mh, MW, MZ, V=VEV):
    k = 2 * math.sqrt(MZ ** 2 - MW ** 2) / ((4 * PI) ** 2 * V ** 3)
    a0 = lambda M: A0(M, mu)
    b0 = lambda p, m1, m2: B0(p, m1, m2, mu)
    D = MZ ** 2 - MW ** 2
    P6 = MZ ** 6 - 48 * MW ** 6 - 68 * MZ ** 2 * MW ** 4 + 16 * MZ ** 4 * MW ** 2
    s = ((88 / 9 - 124 * MW ** 2 / (9 * MZ ** 2) + (Mh ** 2 + 34 * MW ** 2) / (6 * D)) * a0(MZ)
         + (Mh ** 2 - 4 * MW ** 2) / (2 * (Mh ** 2 - MW ** 2)) * a0(Mh)
         + (-7 / 9 - Mt ** 2 / D + 64 * MW ** 2 / (9 * MZ ** 2)) * a0(Mt)
         + (Mh ** 4 + 2 * MW ** 2 * (MW ** 2 - 15 * MZ ** 2) + 3 * Mh ** 2 * (2 * MW ** 2 + 7 * MZ ** 2)) / (6 * (Mh ** 2 - MW ** 2) * (MW ** 2 - MZ ** 2)) * a0(MW)
         - (Mt ** 4 + MW ** 2 * Mt ** 2 - 2 * MW ** 4) / (MW ** 2 - MZ ** 2) * b0(MW, 0.0, Mt)
         - (Mh ** 4 - 4 * MZ ** 2 * Mh ** 2 + 12 * MZ ** 4) / (6 * (MW ** 2 - MZ ** 2)) * b0(MZ, Mh, MZ)
         + (Mh ** 4 - 4 * MW ** 2 * Mh ** 2 + 12 * MW ** 4) / (6 * (MW ** 2 - MZ ** 2)) * b0(MW, Mh, MW)
         + P6 / (6 * MZ ** 2 * (MW ** 2 - MZ ** 2)) * b0(MW, MW, MZ)
         + (1 / 9) * (-23 * MW ** 2 + 7 * Mt ** 2 + 17 * MZ ** 2 - 64 * Mt ** 2 * MW ** 2 / MZ ** 2 - 9 * MW ** 2 * (Mt ** 2 - MW ** 2) / D) * b0(MZ, Mt, Mt)
         + P6 / (6 * MZ ** 2 * D) * b0(MZ, MW, MW)
         + (1 / 36) * (576 * MW ** 4 / MZ ** 2 - 242 * MW ** 2 - 3 * Mh ** 2 + 257 * MZ ** 2 + 36 * MW ** 2 / D + Mt ** 2 * (82 - 256 * MW ** 2 / MZ ** 2)))
    return k * s


# ------------------------------------------------------------------------------------------------ QCD (RunDec hep-ph/0004189)
def qcd_beta(nf):
    b0 = (11 - 2 / 3 * nf) / 4
    b1 = (102 - 38 / 3 * nf) / 16
    b2 = (2857 / 2 - 5033 / 18 * nf + 325 / 54 * nf ** 2) / 64
    b3 = (149753 / 6 + 3564 * ZETA3 + (-1078361 / 162 - 6508 / 27 * ZETA3) * nf + (50065 / 162 + 6472 / 81 * ZETA3) * nf ** 2 + 1093 / 729 * nf ** 3) / 256
    return b0, b1, b2, b3


def qcd_run(als0, mu0, mu1, nf, loops=4, rtol=1e-12):
    b = qcd_beta(nf)[:loops]
    f = lambda t, y: [-2.0 * sum(b[i] * (y[0] / PI) ** (i + 2) * PI for i in range(loops))]   # d alpha_s / d ln mu ; a = alpha_s/pi, mu^2 da/dmu^2 = -sum b_i a^(i+2)
    sol = solve_ivp(f, [math.log(mu0), math.log(mu1)], [als0], method="DOP853", rtol=rtol, atol=1e-15)
    return float(sol.y[0, -1])


def inv_zeta_g2_OS(als_nl, L, nl=5):
    """1 / zeta_g^2 = alpha_s^(nf) / alpha_s^(nl) at the pole-mass heavy quark, in terms of alpha_s^(nl); L = ln(mu^2 / M_h^2)  (RunDec eq. 25)."""
    a = als_nl / PI
    c1 = L / 6
    c2 = 7 / 24 + 19 / 24 * L + L ** 2 / 36
    c3 = (58933 / 124416 + ZETA2 * 2 / 3 * (1 + math.log(2) / 3) + 80507 / 27648 * ZETA3 + 8941 / 1728 * L + 511 / 576 * L ** 2 + L ** 3 / 216
          + nl * (-2479 / 31104 - ZETA2 / 9 - 409 / 1728 * L))
    return 1 + a * c1 + a ** 2 * c2 + a ** 3 * c3


def zeta_g2_OS(als_nf, L, nl=5):
    """zeta_g^2 = alpha_s^(nl)/alpha_s^(nf) in terms of alpha_s^(nf) (RunDec eq. 22)."""
    a = als_nf / PI
    c1 = -L / 6
    c2 = -7 / 24 - 19 / 24 * L + L ** 2 / 36
    c3 = (-58933 / 124416 - ZETA2 * 2 / 3 * (1 + math.log(2) / 3) - 80507 / 27648 * ZETA3 - 8521 / 1728 * L - 131 / 576 * L ** 2 - L ** 3 / 216
          + nl * (2479 / 31104 + ZETA2 / 9 + 409 / 1728 * L))
    return 1 + a * c1 + a ** 2 * c2 + a ** 3 * c3


def inv_zeta_g2_SI(als_nl, L, nl=5):
    """1 / zeta_g^2 for the scale-invariant heavy mass mu_h = m_h(mu_h); L = ln(mu^2/mu_h^2)  (RunDec eq. 24)."""
    a = als_nl / PI
    c1 = L / 6
    c2 = -11 / 72 + 19 / 24 * L + L ** 2 / 36
    c3 = (564731 / 124416 - 82043 / 27648 * ZETA3 + 2191 / 576 * L + 511 / 576 * L ** 2 + L ** 3 / 216 + nl * (-2633 / 31104 + 281 / 1728 * L))
    return 1 + a * c1 + a ** 2 * c2 + a ** 3 * c3


def g3_from_als5(als5_mz, Mt, mu_dec=None, MZ=91.1876, loops_run=4, form="OS", mut_run=None):
    """g_3^(6)(mu = M_t) from alpha_s^(5)(m_Z): four-loop running with n_f = 5 up to mu_dec, three-loop decoupling (pole-mass form), four-loop running with n_f = 6 to M_t."""
    mu_dec = Mt if mu_dec is None else mu_dec
    a5 = qcd_run(als5_mz, MZ, mu_dec, 5, loops_run)
    L = math.log(mu_dec ** 2 / Mt ** 2)
    a6 = a5 * inv_zeta_g2_OS(a5, L, 5)
    a6 = qcd_run(a6, mu_dec, Mt, 6, loops_run)
    return math.sqrt(FOURPI * a6), a6


# ------------------------------------------------------------------------------------------------ the Y1 central run (PDG 2024 inputs; matching per Buttazzo interpolation for g_2, g_Y, y_t, lambda; QCD-only g_3 calibrated to SMDR, see amendment A6)
PDG = dict(Mt=172.57, sMt_exp=0.29, sMt_th=0.30, MW=80.3692, sMW=0.0133, als=0.1180, sals=0.0009, Mh=125.10, sMh=0.09, MZ=91.1876, sMZ=0.0021,
           aem_inv=127.930, saem_inv=0.008, s2w_hat=0.23129, ss2w_hat=0.00004, MW_with_CDF=80.3946, MW_CDF_only=80.4335)
SMDR_G3 = (0.1181, 173.1, 1.1636241)        # (alpha_s^(5)(m_Z), M_t, g_3(Q0 = M_t)) of the SMDR reference model


def g3_cal():
    return SMDR_G3[2] / g3_from_als5(SMDR_G3[0], SMDR_G3[1])[0]


_G3CAL = None


def g3_base(als, Mt, mu_dec=None):
    global _G3CAL
    if _G3CAL is None:
        _G3CAL = g3_cal()
    return g3_from_als5(als, Mt, mu_dec=mu_dec)[0] * _G3CAL


def central_u0(Mt=None, Mh=None, MW=None, als=None, rel_g3=0.0, dg2=0.0, dgY=0.0, dyt=0.0, dlam=0.0, yb_scale=1.0, ytau_scale=1.0, mu_dec=None, g3_mode="base"):
    Mt = PDG["Mt"] if Mt is None else Mt
    Mh = PDG["Mh"] if Mh is None else Mh
    MW = PDG["MW"] if MW is None else MW
    als = PDG["als"] if als is None else als
    if g3_mode == "base":
        g3 = g3_base(als, Mt, mu_dec) * (1 + rel_g3)
    elif g3_mode == "buttazzo":
        g3 = None
    else:
        raise ValueError(g3_mode)
    u0, c = buttazzo_boundary(Mt, Mh, MW, als, g3_override=g3, dg2=dg2, dgY=dgY, dyt=dyt, dlam=dlam, yb=YB_MT_SMDR * yb_scale, ytau=YTAU_MT_SMDR * ytau_scale)
    return u0


def run_central(mu_max=1e21, o=None, **kw):
    o = L_default_opts() if o is None else o
    Mt = PDG["Mt"] if kw.get("Mt") is None else kw["Mt"]
    return Traj(central_u0(**kw), Mt, o, mu_max=mu_max)


def L_default_opts():
    return Opts(gauge_loops=4, yuk_loops=3)


def crossing(traj, k1, k2, lo=None, hi=1e21):
    """First mu where coupling k1 = coupling k2 (keys 'aY','a1','a2','a3').  a_1 = (3/5) a_Y."""
    from scipy.optimize import brentq
    lo = traj.mu0 * 1.001 if lo is None else lo
    def val(k, A):
        return {"aY": A[0], "a1": 0.6 * A[0], "a2": A[1], "a3": A[2]}[k]
    f = lambda lm: val(k1, traj.A(math.exp(lm))) - val(k2, traj.A(math.exp(lm)))
    xs = np.linspace(math.log(lo), math.log(min(hi, math.exp(traj.lnmax) * 0.999)), 400)
    prev = f(xs[0])
    for i in range(1, len(xs)):
        cur = f(xs[i])
        if prev * cur < 0:
            return math.exp(brentq(f, xs[i - 1], xs[i], xtol=1e-13))
        prev = cur
    return None


def mc_draws(n, seed=20260929):
    """The Gaussian draws of the budget items E1-E5 used by y1_4, y1_5 and y1_6 (same order of random numbers): list of kwargs for central_u0."""
    rng = np.random.default_rng(seed)
    sMt = math.hypot(PDG["sMt_exp"], PDG["sMt_th"])
    sg2 = abs(0.64779 - 0.64754) * max(abs(0.64779 - 0.64754) / abs(0.64754 - 0.65294), 0.108 / PI)
    sgY = abs(0.35830 - 0.35940) * max(abs(0.35830 - 0.35940) / abs(0.35940 - 0.34972), 0.108 / PI)
    sMZ_gY = 0.35830 * PDG["MZ"] * PDG["sMZ"] / (PDG["MZ"] ** 2 - PDG["MW"] ** 2)
    sg3 = math.hypot(2.62e-5, 6.72e-5 / 2)
    out = []
    for _ in range(n):
        z = rng.standard_normal(9)
        out.append(dict(als=PDG["als"] + z[0] * PDG["sals"], MW=PDG["MW"] + z[1] * PDG["sMW"], Mt=PDG["Mt"] + z[2] * sMt, Mh=PDG["Mh"] + z[3] * PDG["sMh"],
                        dgY=z[4] * sMZ_gY + z[5] * sgY, dg2=z[6] * sg2, rel_g3=z[7] * sg3, dyt=z[8] * 0.0005))
    return out
