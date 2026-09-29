"""Shared helpers for lane U1 (invented horizon principles).  Not a script; imported by u1_0 ... u1_9.

Units hbar = c = 1, Heaviside-Lorentz, alpha = e^2/(4 pi).  lambda = eE/H^2, M = m/H.  All reused formulas are gated in u1_0_gates.py against committed outputs
of lanes AH1, AH4, N5 and Q1.  No absolute paths: the bar checker is located relative to this file.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import json
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi
ALPHA_INPUT = 1.0 / 137.035999177
INV_ALPHA = 137.035999177
GAMMA_E = float(mp.euler)

# ---------------------------------------------------------------- constants (declared in U1_PREREGISTRATION.md)
HBAR_EV_S = 6.582119569e-16
MPC_M = 3.0856775814913673e22
H0_S = 67.4e3 / MPC_M                       # 1/s
OMEGA_L = 0.685
H0_EV = H0_S * HBAR_EV_S
H_EV = H0_EV * math.sqrt(OMEGA_L)           # H_Lambda in eV (hbar = 1)
MP_EV = 1.220890e19 * 1e9                   # Planck mass (not reduced), eV
E_HL = math.sqrt(4 * PI * ALPHA_INPUT)      # e in HL units


def species_fermions():
    """(name, mass_MeV, Q^2 N_c). PDG-rounded inputs."""
    return [("electron", 0.51099895, 1.0), ("muon", 105.6583755, 1.0), ("tau", 1776.86, 1.0),
            ("up", 2.16, 4.0 / 3.0), ("down", 4.67, 1.0 / 3.0), ("strange", 93.4, 1.0 / 3.0),
            ("charm", 1270.0, 4.0 / 3.0), ("bottom", 4180.0, 1.0 / 3.0), ("top", 172570.0, 4.0 / 3.0)]


M_PION_MEV = 139.57039
M_W_MEV = 80377.0


def Mof(m_mev):
    """M = m/H for a mass in MeV (float)."""
    return m_mev * 1e6 / H_EV


# ---------------------------------------------------------------- dS_4 Dirac fermion (Q1, S2, T1)
def Gf(M, dps=250):
    """G_f(M) = (4/(3 pi)) [ln M - Re psi(iM) - pi M (4M^2+1)/(3 sinh 2 pi M)], sigma/H = alpha G_f (Q1). Returns an mpf."""
    with mp.workdps(dps):
        M = mp.mpf(M)
        x = 2 * mp.pi * M
        sh = mp.pi * M * (4 * M ** 2 + 1) / (3 * mp.sinh(x)) if x < 700 else mp.mpf(0)
        return (4 / (3 * mp.pi)) * (mp.log(M) - mp.re(mp.digamma(1j * M)) - sh)


def Gf_small_lnM(target):
    """ln M for G_f(M) = target in the small-M form G_f = (4/(3 pi))(ln M + gamma_E - 1/6): ln M = (3 pi/4) target - gamma_E + 1/6."""
    return 0.75 * PI * float(target) - GAMMA_E + 1.0 / 6.0


# ---------------------------------------------------------------- dS_4 complex scalar (AH4 closed form, transcribed there from a PDF; re-gated in u1_0)
def scalar_f_closed(lam, mu_phys):
    """f = 4 pi^2 J/(e H^3) for the dS_4 complex scalar, Kobayashi-Afshordi eq. (2.58) as transcribed in AH4 (closed_form_f)."""
    with mp.workdps(30):
        lam = mp.mpf(lam)
        m = mp.mpf(mu_phys)
        mw = mp.sqrt(mp.mpf(9) / 4 - lam ** 2 - m ** 2)
        s2 = mp.sin(2 * mp.pi * mw)
        pi = mp.pi
        T1 = (45 + 4 * pi ** 2 * (-2 + 3 * lam ** 2 + 2 * mw ** 2)) * mw * mp.cosh(2 * pi * lam) / (12 * pi ** 3 * lam * s2)
        T2 = (45 + 8 * pi ** 2 * (-1 + 9 * lam ** 2 + mw ** 2)) * mw * mp.sinh(2 * pi * lam) / (24 * pi ** 4 * lam ** 2 * s2)

        def integrand(rr):
            poly = -1 + 4 * mw ** 2 + (7 + 12 * lam ** 2 - 12 * mw ** 2) * rr ** 2 - 20 * lam ** 2 * rr ** 4
            e1 = (mp.e ** (2 * pi * rr * lam) + mp.e ** (2j * pi * mw)) * mp.psi(0, mp.mpf(1) / 2 + mw + 1j * rr * lam)
            e2 = (mp.e ** (2 * pi * rr * lam) + mp.e ** (-2j * pi * mw)) * mp.psi(0, mp.mpf(1) / 2 - mw + 1j * rr * lam)
            return mp.re(1j * lam / (16 * s2) * poly * (e1 - e2))

        integ = mp.quad(integrand, [-1, -0.5, 0, 0.5, 1])
        return float(-2 * lam ** 3 / 15 + (lam / 3) * mp.log(m) + mp.re(T1) - mp.re(T2) + integ)


def Gs(M):
    """G_s(M) = f/(pi lambda) at lambda = 1e-3 (AH4 V4 convention: sigma/H = alpha G_s).  For M > 200 the heavy form 7/(18 pi M^2) (gated at M = 40)."""
    M = float(M)
    if M > 200.0:
        return 7.0 / (18.0 * PI * M * M)
    lam = 1e-3
    return scalar_f_closed(lam, M) / lam / PI


def solve_Gs(target, lo=3e-3, hi=3.0):
    """M with G_s(M) = target (>0) by bisection in ln M; returns (M, note). G_s is decreasing on (0.003, 3)."""
    if target <= 0:
        return None, "no solution: G_s > 0 at every M (wrong sign)"
    glo, ghi = Gs(lo), Gs(hi)
    if not (ghi < target < glo):
        if target >= glo:
            # small-M asymptote G_s ~ 0.955/M^2 (gated numerically at M = 0.01 : 9546.9)
            return math.sqrt(0.9547 / target), "below the bisection window: from G_s ~ 0.9547/M^2"
        return None, "target smaller than G_s(hi)"
    a, b = math.log(lo), math.log(hi)
    for _ in range(42):
        c = 0.5 * (a + b)
        if Gs(math.exp(c)) > target:
            a = c
        else:
            b = c
    return math.exp(0.5 * (a + b)), "bisection"


# ---------------------------------------------------------------- dS_2 (AH1, N5)
def rho_s(lam, mu):
    v = mu * mu + lam * lam - 0.25
    return math.sqrt(v) if v > 0 else float("nan")


def lncosh(x):
    ax = abs(x)
    return ax + math.log1p(math.exp(-2.0 * ax)) - math.log(2.0)


def ln_r_s(lam, mu):
    rh = rho_s(lam, mu)
    return -2.0 * PI * rh + lncosh(PI * (lam + rh)) - lncosh(PI * (lam - rh))


def r_s(lam, mu):
    return math.exp(ln_r_s(lam, mu))


def J_f2(lam, mu):
    """N5: J/(eH) = (1/pi) rho_f sinh(2 pi lambda)/sinh(2 pi rho_f), rho_f = sqrt(mu^2 + lambda^2)."""
    with mp.workdps(50):
        lam = mp.mpf(lam)
        mu = mp.mpf(mu)
        rf = mp.sqrt(mu ** 2 + lam ** 2)
        return float(rf * mp.sinh(2 * mp.pi * lam) / (mp.pi * mp.sinh(2 * mp.pi * rf)))


def g_f2(mu):
    mu = float(mu)
    return 1.0 / PI if mu == 0 else 2 * mu / math.sinh(2 * PI * mu)


# ---------------------------------------------------------------- back-reaction ceiling (T-BACK)
def lam_max():
    """lambda_max: E^2/2 = rho_Lambda = 3 H^2 M_P^2/(8 pi)  =>  E = H M_P sqrt(3/(4 pi)),  lambda = e E/H^2."""
    return E_HL * MP_EV * math.sqrt(3.0 / (4.0 * PI)) / H_EV


def energy_ratio(lam):
    """rho_E / rho_Lambda = (4 pi/3) lambda^2 H^2 / (e^2 M_P^2)."""
    return (4.0 * PI / 3.0) * lam * lam * (H_EV / MP_EV) ** 2 / (E_HL ** 2)


# ---------------------------------------------------------------- lane D bar
def bar_assess(delta, log2size, **kw):
    """Lane D's look-elsewhere bar (alpha_bar_checker.assess), quiet.  Returns its result dict."""
    d = os.path.join(HERE, "..", "D_calibration_bar")
    if d not in sys.path:
        sys.path.insert(0, d)
    import alpha_bar_checker as ABC
    return ABC.assess(delta=delta, log2size=log2size, verbose=False, **kw)


# ---------------------------------------------------------------- bookkeeping
class Checks:
    def __init__(self):
        self.items = []

    def __call__(self, tag, ok, detail=""):
        self.items.append((tag, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)
        return bool(ok)

    def all_ok(self):
        return all(o for _, o in self.items)

    def failed(self):
        return [t for t, o in self.items if not o]


def finish(chk, mutate, targeted_tags=None):
    """Campaign standard: real run exits 0 iff every check passed; mutate run exits 1 iff the targeted check(s) FAIL as required (3 if the control has no power)."""
    ok = chk.all_ok()
    if not mutate:
        sys.exit(0 if ok else 1)
    tags = set(targeted_tags or [])
    failed = {t.split()[0] for t in chk.failed()}
    hit = bool(tags) and tags <= failed
    print("\nMUTATE CONTROL: " + ("targeted check(s) " + ", ".join(sorted(tags)) + (" FAILED as required -- the control works (exit 1, the campaign standard)" if hit else " DID NOT ALL FAIL -- the control has no power (exit 3)")))
    sys.exit(1 if hit else 3)


def write_json(name, mutate, obj):
    fn = os.path.join(HERE, name.replace(".json", "_MUTATE.json") if mutate else name)
    with open(fn, "w") as f:
        json.dump(obj, f, indent=1, default=float)
    return fn
