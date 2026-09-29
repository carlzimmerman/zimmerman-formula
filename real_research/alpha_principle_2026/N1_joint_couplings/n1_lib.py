"""n1_lib -- shared machinery of lane N1: SM running (one- and two-loop), the running variants, and the joint ratio scorer.
No __main__: exercised by n1_3_running_scorer.py and n1_4_score_maps.py (both take --mutate).
Conventions: t = ln(mu); alpha_i^-1 with i = (Y, 2, 3); alpha_Y = alpha_em/cos^2, alpha_2 = alpha_em/sin^2, alpha_1 = (5/3) alpha_Y (GUT normalisation) so alpha_Y^-1 = (5/3) alpha_1^-1.
d alpha_i^-1/dt = -(1/2 pi) [ b_i + (1/16 pi^2)(sum_j B_ij g_j^2 - C_i y_t^2) ],  b = (b_1, b_2, b_3) in GUT normalisation, b_Y = (5/3) b_1.
"""
import sys
sys.dont_write_bytecode = True
import math
from fractions import Fraction
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MZ = 91.1876
MT = 172.57
MPL = 1.220890e19            # un-reduced Planck mass, l_P^2 = G_4 = 1/M_P^2 (as in lanes F, AH6)
ALPHA_INV0 = 137.035999177
SET_A = dict(alpha_inv=127.930, s2w=0.23122, alpha_s=0.1180)     # lane B rg_common inputs
SET_B = dict(alpha_inv=127.955, s2w=0.23122, alpha_s=0.1179)     # lane G g4 inputs
YT_MT = 0.9334               # MSbar y_t(m_t) = sqrt2 * 162.5/246.22 (declared external input, +-5% tested in n1_3)
B2L = np.array([[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26.0]])   # RECALLED (Machacek-Vaughn / Arason et al.)
C2L = np.array([17 / 10, 3 / 2, 2.0])                                                            # RECALLED (top Yukawa only)


def sm_coefficients(mutate=False):
    """One-loop b's from the SM field content (Weyl fermions + one Higgs doublet): returns (b_Y, b_2, b_3) as Fractions, and the GUT-normalised b_1."""
    gens = 3
    # (dim_SU3, dim_SU2, Y)
    weyl = [(3, 2, Fraction(1, 6)), (3, 1, Fraction(-2, 3)), (3, 1, Fraction(1, 3)), (1, 2, Fraction(-1, 2)), (1, 1, Fraction(1))]
    higgs = [(1, 2, Fraction(1, 2))]
    bY = sum(Fraction(2, 3) * d3 * d2 * y * y for d3, d2, y in weyl) * gens + sum(Fraction(1, 3) * d3 * d2 * y * y for d3, d2, y in higgs)
    T2 = lambda d: Fraction(1, 2) if d == 2 else Fraction(0)
    T3 = lambda d: Fraction(1, 2) if d == 3 else Fraction(0)
    b2 = Fraction(-22, 3) + sum(Fraction(2, 3) * T2(d2) * d3 * (1 if d2 == 2 else 0) for d3, d2, y in weyl) * gens + sum(Fraction(1, 3) * T2(d2) * d3 for d3, d2, y in higgs)
    b3 = Fraction(-11) + sum(Fraction(2, 3) * T3(d3) * d2 for d3, d2, y in weyl) * gens
    b1 = bY * Fraction(3, 5)
    if mutate:      # lane A's bug: b_Y = (3/5) b_1 instead of (5/3) b_1
        bY = Fraction(3, 5) * b1
    return bY, b2, b3, b1


def boundaries(inp):
    aY = inp["alpha_inv"] * (1 - inp["s2w"])
    a2 = inp["alpha_inv"] * inp["s2w"]
    a3 = 1.0 / inp["alpha_s"]
    return np.array([aY, a2, a3])


class Runner:
    """Runs (alpha_Y^-1, alpha_2^-1, alpha_3^-1) from m_Z.  variants: '1L-A', '2L-A', '1L-B', '2L-B', '1L-A-topdec'."""

    def __init__(self, mutate=False):
        bY, b2, b3, b1 = sm_coefficients(mutate)
        self.b = np.array([float(bY), float(b2), float(b3)])
        self.b1 = float(b1)
        self.mutate = mutate
        self._yt0 = None

    # ---- one loop (closed form)
    def oneloop(self, mu, inp=SET_A, topdec=False):
        a0 = boundaries(inp)
        L = math.log(mu / MZ)
        out = a0 - self.b / (2 * math.pi) * L
        if topdec and mu > MZ:
            # top decoupled between m_Z and m_t: remove the top's contribution to b over that window (crude; Delta b_top = (17/18, 1/2, 2/3))
            Lt = math.log(min(mu, MT) / MZ)
            db = np.array([17 / 18, 1 / 2, 2 / 3])
            out = out + db / (2 * math.pi) * Lt
        return out

    # ---- two loop
    def _rhs(self, t, y, yt_scale=1.0):
        ainv = y[:3]
        yt = y[3]
        g2 = 4 * math.pi / ainv                       # g_Y^2, g_2^2, g_3^2
        g1sq = g2[0] * 3 / 5 * 1.0                    # GUT normalised g_1^2 = (5/3) g_Y^2 ... see below
        g1sq = g2[0] * 5 / 3
        gs = np.array([g1sq, g2[1], g2[2]])
        b = np.array([self.b1, self.b[1], self.b[2]])
        two = (B2L @ gs - C2L * yt ** 2) / (16 * math.pi ** 2)
        da_gut = -(1 / (2 * math.pi)) * (b + two)     # d alpha_i^-1/dt in GUT normalisation for i = 1, 2, 3
        # convert alpha_1^-1 -> alpha_Y^-1 = (5/3) alpha_1^-1
        dY = da_gut[0] * 5 / 3
        dyt = yt / (16 * math.pi ** 2) * (4.5 * yt ** 2 - 8 * gs[2] - 2.25 * gs[1] - 0.85 * gs[0])
        return [dY, da_gut[1], da_gut[2], dyt]

    def yt_at_mz(self, inp=SET_A, scale=1.0):
        # shooting: y_t(m_t) = YT_MT * scale using one-loop gauge inputs for the short window m_Z..m_t
        def f(y0):
            sol = solve_ivp(lambda t, y: self._rhs(t, y), [math.log(MZ), math.log(MT)], list(boundaries(inp)) + [y0], rtol=1e-10, atol=1e-12)
            return sol.y[3, -1] - YT_MT * scale
        return brentq(f, 0.7, 1.3)

    def twoloop(self, mu, inp=SET_A, yt_scale=1.0):
        y0 = self.yt_at_mz(inp, yt_scale)
        if mu <= MZ:
            return boundaries(inp)
        sol = solve_ivp(lambda t, y: self._rhs(t, y), [math.log(MZ), math.log(mu)], list(boundaries(inp)) + [y0], rtol=1e-10, atol=1e-12)
        return sol.y[:3, -1]

    VARIANTS = ["2L-A", "1L-A", "1L-B", "2L-B", "1L-A-topdec"]

    def run(self, mu, variant="2L-A"):
        if variant == "1L-A":
            return self.oneloop(mu, SET_A)
        if variant == "1L-B":
            return self.oneloop(mu, SET_B)
        if variant == "1L-A-topdec":
            return self.oneloop(mu, SET_A, topdec=True)
        if variant == "2L-A":
            return self.twoloop(mu, SET_A)
        if variant == "2L-B":
            return self.twoloop(mu, SET_B)
        raise ValueError(variant)

    # ---- ratios
    @staticmethod
    def ratios(a):
        aY, a2, a3 = a
        return dict(rY2=a2 / aY,        # alpha_Y/alpha_2
                    r23=a3 / a2,        # alpha_2/alpha_3
                    rY3=a3 / aY)        # alpha_Y/alpha_3

    def variants_at(self, mu):
        return {v: self.run(mu, v) for v in self.VARIANTS}

    def delta_run(self, mu):
        """relative spread of each ratio among the 5 variants, with respect to the central 2L-A."""
        vs = self.variants_at(mu)
        cen = self.ratios(vs["2L-A"])
        out = {}
        for k in cen:
            out[k] = max(abs(self.ratios(a)[k] / cen[k] - 1) for a in vs.values())
        return out, vs, cen

    def alpha2_selfconsistent_mu(self, factor=1.0, variant="2L-A"):
        """mu_c solving  mu_c = factor * M_P * sqrt(alpha_2(mu_c)/3)   [Map A: alpha_2 = 3 l_P^2/R^2, mu_c = 1/R]."""
        f = lambda lm: math.exp(lm) - factor * MPL * math.sqrt(1.0 / (3 * self.run(math.exp(lm), variant)[1]))
        lm = brentq(f, math.log(1e12), math.log(MPL))
        return math.exp(lm)


def scale_ambiguity(runner, mu_c, factor=3.5):
    """max relative shift of each ratio when the identification mu_c = 1/R is uncertain by `factor` (lightest KK mass of the internal space vs 1/R)."""
    base = runner.ratios(runner.run(mu_c))
    out = {}
    for k in base:
        out[k] = max(abs(runner.ratios(runner.run(mu_c * f))[k] / base[k] - 1) for f in (1 / factor, factor))
    return out


# ---------------------------------------------------------------- the joint scorer
LN_SPAN = math.log(100.0)      # log-uniform prior on each ratio over [0.1, 10] (declared convention)


def tol_of(delta_run):
    return max(2 * delta_run, 0.01)


def look_elsewhere(n_trials, tols):
    lam = n_trials * float(np.prod([min(1.0, 2 * t / LN_SPAN) for t in tols]))
    return lam, 1 - math.exp(-lam)


def joint_score(pred, meas, delta_run, n_trials):
    """pred, meas, delta_run: dicts ratio-name -> value.  Returns dict with per-ratio miss and tol, J1 pass, lambda, P (family of n_trials)."""
    names = list(pred)
    rows = {}
    ok = True
    tols = []
    for k in names:
        miss = pred[k] / meas[k] - 1
        tol = tol_of(delta_run[k])
        rows[k] = dict(pred=pred[k], meas=meas[k], miss=miss, tol=tol, sigma_run=miss / max(delta_run[k], 1e-12), ok=abs(miss) <= tol)
        ok = ok and rows[k]["ok"]
        tols.append(tol)
    lam, P = look_elsewhere(n_trials, tols)
    return dict(rows=rows, J1=ok, lam=lam, P=P, J2=P < 1e-3)
