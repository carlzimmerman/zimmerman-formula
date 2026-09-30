# -*- coding: utf-8 -*-
"""CFG253 -- dark energy converted into the cold mass (an owner's idea): an interacting vacuum, readings (A) continuous,
(B) early/completed, (C) clusters.  Background cosmology only.  Frozen criteria: ../CFG253_FROZEN_CRITERIA.md (sha256 printed
at the top of the .out and checked against CFG253_FROZEN_CRITERIA_SHA256.txt).

Units: H0 = 1, densities in units of today's critical density (H^2 = sum rho), x = ln a.
Exchange: rho_DE' = -Q/H, rho_c' = -3 rho_c + Q/H  (' = d/dx).  Tie: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)); kappa = 1/2 FITTED.

MUTATE=1: Q == 0 in every reading (must: rho_DE constant, a0 flat; load-bearing claims H-A1 and H-B1 FAIL -> exit 1).
MUTATE=2: the tie replaced by a0 proportional to H(z) (load-bearing claim H-A2 'FLAT-LIKE at the G1 tolerance' must FAIL -> exit 1).
Self-contained: reads only the frozen criteria and its hash file.  No network, no downloads, writes only inside this directory.
"""
import os, sys, math, json, hashlib
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
CRIT = os.path.join(HERE, "..", "CFG253_FROZEN_CRITERIA.md")
MUTATE = int(os.environ.get("MUTATE", "0"))
TAG = "" if MUTATE == 0 else "_MUTATE%d" % MUTATE
OUT = os.path.join(HERE, "CFG253_background%s.out" % TAG)
JS = os.path.join(HERE, "CFG253_background%s_results.json" % TAG)
QFAC = 0.0 if MUTATE == 1 else 1.0

_f = open(OUT, "w", encoding="utf-8")
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _f.write(s + "\n"); _f.flush()

CHECKS = []
def check(tag, stmt, measured, ok, lb=True):
    ok = bool(ok)
    CHECKS.append(dict(tag=tag, ok=ok, load_bearing=lb, statement=stmt, measured=str(measured)))
    P("  [%s] %s %s" % ("PASS" if ok else ("FAIL" if lb else "FAIL(reported)"), tag, stmt))
    P("         measured: %s" % measured)

def banner(t):
    P(""); P("=" * 118); P(t); P("=" * 118)

h = hashlib.sha256(open(CRIT, "rb").read()).hexdigest()
rec = open(os.path.join(HERE, "CFG253_FROZEN_CRITERIA_SHA256.txt")).read()
P("CFG253 background (MUTATE=%d)" % MUTATE)
P("CFG253_FROZEN_CRITERIA.md sha256 = %s ; matches the recorded hash: %s" % (h, h in rec))
P("kappa = 1/2 FITTED (never derived).  The mass is still required.  Nothing here says the theory is closed or that data favour it.")

# ---------------------------------------------------------------------------------------------------------- declared inputs
OC, OB, OL, OR = 0.265, 0.050, 0.685, 9.1e-5          # CFG131 Dcommon / CFG43 declared inputs
OM = OC + OB
H0KMS = 67.4
ZREC, ZEQ = 1090.0, 3423.0                             # L121 as parsed by CFG251
Z_K02 = None                                           # horizon entry of k = 0.2/Mpc, computed below
ZBBN = 4.3e8                                           # T ~ 0.1 MeV (from memory, UNVERIFIED)
XEND = -math.log(1 + ZBBN)
C_KMS = 299792.458

def E_lcdm(z):
    return math.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)

# ========================================================================================================== sympy
banner("S  sympy: closed forms and identities")
a, xi, OLs, OCs, at, K = sp.symbols('a xi Omega_L Omega_c a_t K', positive=True)
x = sp.Symbol('x', real=True)
# A1: Q/H = xi rho_DE
rDE1 = OLs * a ** (-xi)
u1 = OCs - xi * OLs * (1 - a ** (3 - xi)) / (3 - xi)          # rho_c a^3
# check the ODEs in x = ln a:  d rho_DE/dx = -xi rho_DE ;  d(rho_c a^3)/dx = xi rho_DE a^3
s1a = sp.simplify(sp.diff(rDE1.subs(a, sp.exp(x)), x) + xi * rDE1.subs(a, sp.exp(x)))
s1b = sp.simplify(sp.diff(u1.subs(a, sp.exp(x)), x) - xi * (rDE1 * a ** 3).subs(a, sp.exp(x)))
s1c = sp.simplify(u1.subs(a, 1) - OCs)
check("S1", "A1 (Q = xi H rho_DE): rho_DE = Omega_L a^-xi and rho_c a^3 = Omega_c - xi Omega_L (1 - a^(3-xi))/(3-xi) solve the exchange equations",
      "residuals %s, %s, %s" % (s1a, s1b, s1c), s1a == 0 and s1b == 0 and s1c == 0)
# A2: Q/H = xi rho_c
rc2 = OCs * a ** (xi - 3)
rDE2 = OLs + xi * OCs * (a ** (xi - 3) - 1) / (3 - xi)
s2a = sp.simplify(sp.diff(rc2.subs(a, sp.exp(x)), x) + 3 * rc2.subs(a, sp.exp(x)) - xi * rc2.subs(a, sp.exp(x)))
s2b = sp.simplify(sp.diff(rDE2.subs(a, sp.exp(x)), x) + xi * rc2.subs(a, sp.exp(x)))
check("S2", "A2 (Q = xi H rho_c): rho_c = Omega_c a^(xi-3), rho_DE = Omega_L + xi Omega_c (a^(xi-3) - 1)/(3 - xi); at early times rho_DE/rho_c -> xi/(3 - xi)",
      "residuals %s, %s; limit %s" % (s2a, s2b, sp.limit((rDE2 / rc2).subs(xi, sp.Rational(1, 10)), a, 0)),
      s2a == 0 and s2b == 0 and sp.limit((rDE2 / rc2).subs(xi, sp.Rational(1, 10)), a, 0) == sp.Rational(1, 29))
# A3: d rho/dt = -xi rho^(3/2)  ->  d(rho^(-1/2))/dt = xi/2
t = sp.Symbol('t'); r = sp.Function('r')
s3 = sp.simplify(sp.diff(r(t) ** sp.Rational(-1, 2), t).subs(sp.Derivative(r(t), t), -xi * r(t) ** sp.Rational(3, 2)) - xi / 2)
check("S3", "A3 (Q = xi H_L rho_DE, H_L = sqrt(rho_DE) in H0 units): d(rho_DE^-1/2)/dt = xi/2, so a0(z)/a0(0) = 1/(1 + xi sqrt(Omega_L)(t_z - t0)/2) (CFG131's closed form)",
      "residual %s" % s3, s3 == 0)
# G1 identity: rho_c a^3 constant  <=>  Q = 0   (d(rho_c a^3)/dx = (Q/H) a^3)
Qs = sp.Function('Q'); Hs = sp.Function('H'); rcf = sp.Function('rc')
expr = sp.diff(rcf(x) * sp.exp(3 * x), x).subs(sp.Derivative(rcf(x), x), -3 * rcf(x) + Qs(x) / Hs(x))
s4 = sp.simplify(expr - Qs(x) / Hs(x) * sp.exp(3 * x))
check("S4", "G1 identity: d(rho_c a^3)/dln a = (Q/H) a^3, so rho_c a^3 constant on an interval <=> Q = 0 there (a transfer that keeps LCDM's a^-3 history exactly makes nothing)",
      "residual %s" % s4, s4 == 0)
# B-pow: single vacuum, Q = xi H rho_DE for a < a_t, rho_DE(a_t) = Omega_L  -> created rho_c(a_t) = xi Omega_L/(3 - xi)
ai = sp.Symbol('a_i', positive=True)
created = sp.integrate(xi * OLs * (a / at) ** (-xi) * a ** 3 / a, (a, ai, at), conds='none')
s5 = sp.simplify(sp.limit((created / at ** 3).subs(xi, sp.Rational(1, 2)), ai, 0) - sp.Rational(1, 2) * OLs / (3 - sp.Rational(1, 2)))
check("S5", "B-pow: with rho_DE continuous (= Omega_L at z_t) and Q = xi H rho_DE (xi < 3) before z_t, the cold density created by z_t is xi Omega_L/(3 - xi) (a_i -> 0)",
      "residual (xi = 1/2) %s" % s5, s5 == 0)
# B-step: ρ_X constant, then Q/H = K rho_X for x > x_t: created comoving = rho_X a_t^3 K/(K - 3)
created_step = sp.integrate(K * sp.exp(-K * x) * sp.exp(3 * x), (x, 0, sp.oo), conds='none')
s6 = sp.simplify(created_step - K / (K - 3))
check("S6", "B-step (sharp transfer at z_t with rate K H): created rho_c a^3 = rho_X a_t^3 K/(K - 3), i.e. the instantaneous bound rho_X(before) >= rho_c(z_t) is reached as K -> oo",
      "residual %s (K > 3)" % s6, s6 == 0 or sp.simplify(s6.subs(K, 2000)) == 0)

# ========================================================================================================== reading A
banner("A  continuous transfer, ongoing to today (today's Omega_c, Omega_L fixed; backward integration to z_BBN)")

def qh(form, xi_, rde, rc, H):
    if form == "A1":
        q = xi_ * rde
    elif form == "A2":
        q = xi_ * rc
    else:
        q = xi_ * math.sqrt(max(rde, 0.0)) * rde / H
    return QFAC * q

def solveA(form, xi_, xend=XEND):
    def rhs(xx, y):
        rde, rc = y
        aa = math.exp(xx)
        H = math.sqrt(max(rde + rc + OB / aa ** 3 + OR / aa ** 4, 1e-300))
        q = qh(form, xi_, rde, rc, H)
        return [-q, -3 * rc + q]
    sol = solve_ivp(rhs, [0.0, xend], [OL, OC], method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True)
    return sol

def st(sol, z):
    rde, rc = sol.sol(-math.log(1 + z))
    aa = 1 / (1 + z)
    H = math.sqrt(rde + rc + OB / aa ** 3 + OR / aa ** 4)
    return rde, rc, H

def Fmade(sol):
    rde, rc, H = st(sol, ZREC)
    return 1 - rc / (1 + ZREC) ** 3 / OC

def a0ratio(sol, z):
    if MUTATE == 2:
        return st(sol, z)[2] / st(sol, 0.0)[2]
    return math.sqrt(st(sol, z)[0] / OL)

ZS = [0.5, 1.0, 1.4, 2.5, 4.5, 5.0, 5.5]
ZG = np.concatenate([np.linspace(0.0, 5.0, 101)])

def curve_stats(sol):
    rat = {z: a0ratio(sol, z) for z in ZS}
    dev = max(abs(a0ratio(sol, z) - 1) for z in ZG)
    dex = max(abs(math.log10(a0ratio(sol, z))) for z in ZG)
    phi = {z: (math.log(a0ratio(sol, z)) / math.log(E_lcdm(z))) for z in (1.0, 2.5, 5.0, 10.0, 100.0, ZREC)}
    return rat, dev, dex, phi

def g2_label(dev, dex, phi):
    a_ = "PASS(<1%)" if dev < 0.01 else "FAIL(>=1%)"
    if dex <= 0.05:
        b_ = "FLAT-LIKE"
    elif phi[2.5] >= 0.8 and phi[5.0] >= 0.8:
        b_ = "RIVAL-LIKE"
    else:
        b_ = "BETWEEN (NON-DIAGNOSTIC)"
    return a_, b_

def extras(sol, form, xi_):
    rde0, rc0, H0_ = st(sol, 0.0)
    def weff(z):
        rde, rc, H = st(sol, z)
        return -1 + qh(form, xi_, rde, rc, H) / H / (3 * rde)
    w0 = weff(0.0); wa = (weff(1.0) - w0) / 0.5
    dH = {z: st(sol, z)[2] / E_lcdm(z) - 1 for z in (1.0, 2.5, ZREC)}
    DM = quad(lambda z: 1 / st(sol, z)[2], 0, ZREC, limit=400, epsrel=1e-10)[0]
    DM0 = quad(lambda z: 1 / E_lcdm(z), 0, ZREC, limit=400, epsrel=1e-10)[0]
    zz = np.logspace(3, 5, 81)
    fwin = max(st(sol, z)[0] / st(sol, z)[2] ** 2 for z in zz)
    frec = st(sol, ZREC)[0] / st(sol, ZREC)[2] ** 2
    rde_b, rc_b, H_b = st(sol, ZBBN)
    fbbn = rde_b / (OR * (1 + ZBBN) ** 4)
    rcmin = min(st(sol, z)[1] for z in np.concatenate([np.logspace(-2, math.log10(ZBBN), 400), [0.0]]))
    rdemin = min(st(sol, z)[0] for z in np.concatenate([np.logspace(-2, math.log10(ZBBN), 400), [0.0]]))
    return dict(w0=w0, wa=wa, dH=dH, DM_shift=DM / DM0 - 1, fDE_rec=frec, fDE_max_1e3_1e5=fwin, DE_over_rad_BBN=fbbn,
                rho_c_min=rcmin, rho_DE_min=rdemin)

# ---- controls
P("")
P("Controls")
if MUTATE != 1:
    s = solveA("A1", 0.1)
    e1 = max(abs(st(s, z)[0] / (OL * (1 + z) ** 0.1) - 1) for z in (1, 5, ZREC, 1e5))
    u1n = lambda z: OC - 0.1 * OL * (1 - (1 + z) ** (-(3 - 0.1))) / (3 - 0.1)
    e1b = max(abs(st(s, z)[1] / (1 + z) ** 3 / u1n(z) - 1) for z in (1, 5, ZREC))
    s2 = solveA("A2", 0.05)
    e2 = max(abs(st(s2, z)[1] / (OC * (1 + z) ** (3 - 0.05)) - 1) for z in (1, 5, ZREC, 1e5))
    e2b = max(abs(st(s2, z)[0] / (OL + 0.05 * OC * ((1 + z) ** (3 - 0.05) - 1) / (3 - 0.05)) - 1) for z in (1, 5, ZREC))
    check("K1", "numerics reproduce the A1 and A2 closed forms to <= 1e-7", "A1 %.1e / %.1e ; A2 %.1e / %.1e" % (e1, e1b, e2, e2b), max(e1, e1b, e2, e2b) < 1e-7)
    s3 = solveA("A3", 0.1)
    tz = quad(lambda z: 1 / ((1 + z) * st(s3, z)[2]), 0, 2.5, epsrel=1e-12)[0]      # t0 - t_z
    pred = 1 / (1 + 0.1 * math.sqrt(OL) * (-tz) / 2)
    e3 = abs(a0ratio(s3, 2.5) / pred - 1) if MUTATE == 0 else 0.0
    check("K2", "numerics reproduce A3's closed form a0(z)/a0(0) = 1/(1 + xi sqrt(Omega_L)(t_z - t0)/2) at xi = 0.1, z = 2.5 to <= 1e-7", "rel. diff %.1e" % e3, e3 < 1e-7)
sq = solveA("A1", 0.0)
e0 = max(max(abs(st(sq, z)[0] / OL - 1), abs(st(sq, z)[1] / (OC * (1 + z) ** 3) - 1)) for z in (1, 5, ZREC, 1e5))
check("K3", "Q = 0 reproduces LCDM (rho_DE constant, rho_c a^3 constant) to <= 1e-10", "max rel. diff %.1e" % e0, e0 < 1e-10)

def dev_cfg131(xi_):
    s = solveA("A3", xi_, xend=-math.log(6.0))
    return max(abs(math.sqrt(st(s, z)[0] / OL) - 1) for z in (0.5, 1.0, 2.5, 5.0))
if MUTATE != 1:
    xi131 = brentq(lambda v: dev_cfg131(v) - 0.01, 1e-4, 0.5, xtol=1e-7)
    check("K4", "A3's 1% flat-a0 line reproduces CFG131's |xi| < 0.0275 within 5% (CFG131 anchors rho_c a^3 at z = 999, this lane today)",
          "xi(1%%) = %.4f vs 0.0275 (%.1f%%)" % (xi131, 100 * (xi131 / 0.0275 - 1)), abs(xi131 / 0.0275 - 1) < 0.05)
else:
    xi131 = float("nan")

# ---- xi at the targets
FORMS = ["A1", "A2", "A3"]
TARGETS = [0.03, 0.10, 0.5, 0.9]
resA = {}
def F_of(form, v):
    return Fmade(solveA(form, v))
def xi_for(form, F):
    hi = {"A1": 0.8368, "A2": 5.0, "A3": 1.1}[form]   # A3: backward finite-time blow-up of rho_DE for xi >~ 1.12
    fhi = F_of(form, hi)
    if not (fhi > F):
        return None
    return brentq(lambda v: F_of(form, v) - F, 1e-7, hi, xtol=1e-9)
def xi_all_made(form):
    """largest xi with rho_c >= 0 over the integrated history (rho_c a^3 -> 0 at z_BBN): the whole cold mass made by the transfer"""
    if form == "A2":
        return None
    g = lambda v: st(solveA(form, v), ZBBN)[1]
    if QFAC == 0.0:
        return None
    lo, hi = (0.5, 1.0) if form == "A1" else (1.0, 1.1)
    return brentq(g, lo, hi, xtol=1e-10)

P("")
P("Reading A: xi at each G1 target F_made (fraction of today's cold mass created after z_rec = 1090) and the a0 curve it implies")
P("  %-4s %-7s %-10s %s | %-9s %-7s | %-6s %-6s %-6s %-6s | %s" % ("form", "F_made", "xi", "a0(z)/a0(0) at z = " + ", ".join("%g" % z for z in ZS), "maxdev<=5", "maxdex", "phi1", "phi2.5", "phi5", "phi1090", "G2a / G2b"))
for form in FORMS:
    resA[form] = {}
    cases = [(F, xi_for(form, F)) for F in TARGETS]
    if form == "A2":
        cases += [(0.99, xi_for(form, 0.99))]
    else:
        v = xi_all_made(form)
        cases += [("all", v)]
    for F, v in cases:
        if v is None:
            P("  %-4s %-7s no xi reaches this F_made (Q = 0 in MUTATE=1, or beyond the form)" % (form, F))
            resA[form][str(F)] = None
            continue
        s = solveA(form, v)
        Fm = Fmade(s)
        rat, dev, dex, phi = curve_stats(s)
        g2a, g2b = g2_label(dev, dex, phi)
        ex = extras(s, form, v)
        g1 = "PASS" if Fm <= 0.03 + 1e-6 else ("PASS(0.10 sens.)" if Fm <= 0.10 + 1e-6 else "FAIL")   # 1e-6: root-finder tolerance at the targets
        g3 = "PASS" if (ex["rho_c_min"] >= -1e-12 and ex["rho_DE_min"] >= 0) else "FAIL"
        g5 = "PASS" if (ex["fDE_max_1e3_1e5"] <= 0.10 and ex["DE_over_rad_BBN"] <= 0.040) else "FAIL"
        resA[form][str(F)] = dict(xi=v, F_made=Fm, a0ratio=rat, maxdev_z5=dev, maxdex_z5=dex, phi=phi, G1=g1, G2a=g2a, G2b=g2b, G3=g3, G5=g5, **ex)
        P("  %-4s %-7s %-10.5g %s | %-9.4f %-7.4f | %-6.3f %-6.3f %-6.3f %-6.3f | %s / %s" % (
            form, ("%.3f" % Fm) if F == "all" else F, v, "  ".join("%.4f" % rat[z] for z in ZS), dev, dex, phi[1.0], phi[2.5], phi[5.0], phi[ZREC], g2a, g2b))
        P("       G1 %s  G3 %s (min rho_c %.2e)  G5 %s  | w0 %.4f wa %+.4f | H/H_LCDM-1 at z=1: %+.4f, 2.5: %+.4f, 1090: %+.4f | D_M(1090) %+.2e | f_DE rec %.2e, max[1e3,1e5] %.2e, DE/rad at BBN %.2e" % (
            g1, g3, ex["rho_c_min"], g5, ex["w0"], ex["wa"], ex["dH"][1.0], ex["dH"][2.5], ex["dH"][ZREC], ex["DM_shift"], ex["fDE_rec"], ex["fDE_max_1e3_1e5"], ex["DE_over_rad_BBN"]))

P("")
P("  CFG131's 1%% flat-a0 line in each form (xi and the F_made it allows):")
line1 = {}
for form in FORMS:
    if QFAC == 0.0:
        line1[form] = None; continue
    def dv(v, form=form):
        s = solveA(form, v, xend=-math.log(1 + ZREC + 1))
        return max(abs(math.sqrt(st(s, z)[0] / OL) - 1) for z in ZG) - 0.01
    v = brentq(dv, 1e-6, 0.5, xtol=1e-9)
    Fm = Fmade(solveA(form, v))
    line1[form] = dict(xi=v, F_made=Fm)
    P("   %s: xi = %.5f -> F_made = %.5f (%.2f%% of today's cold mass made after recombination)" % (form, v, Fm, 100 * Fm))

# ---- load-bearing claims for A
banner("A-claims")
g1tol = {f: resA[f].get("0.03") for f in FORMS}
if MUTATE == 1:
    ok = all(g1tol[f] is not None and g1tol[f]["maxdev_z5"] > 1e-4 for f in FORMS)
    check("H-A1", "at the G1 tolerance (F_made = 0.03) every form's transfer leaves a nonzero a0 rise (> 1e-4) at z <= 5",
          "MUTATED (Q = 0): no xi reaches F_made = 0.03", ok)
else:
    check("H-A1", "at the G1 tolerance (F_made = 0.03) every form's transfer leaves a nonzero a0 rise (> 1e-4) at z <= 5",
          "; ".join("%s maxdev %.4f" % (f, g1tol[f]["maxdev_z5"]) for f in FORMS), all(g1tol[f]["maxdev_z5"] > 1e-4 for f in FORMS))
if MUTATE != 1:
    check("H-A2", "at the G1 tolerance (F_made = 0.03) every form is FLAT-LIKE (max |log10 a0 ratio| <= 0.05 dex at z <= 5)" + (" [MUTATE=2: tie a0 ~ H(z)]" if MUTATE == 2 else ""),
          "; ".join("%s %.4f dex (%s)" % (f, g1tol[f]["maxdex_z5"], g1tol[f]["G2b"]) for f in FORMS), all(g1tol[f]["G2b"] == "FLAT-LIKE" for f in FORMS))
    check("H-A3", "at the G1 tolerance every form FAILS CFG131's 1% line (the transfer is visible in a0 at the 1% level before it is visible in G1 at 3%)",
          "; ".join("%s %.4f" % (f, g1tol[f]["maxdev_z5"]) for f in FORMS), all(g1tol[f]["maxdev_z5"] >= 0.01 for f in FORMS), lb=False)

# ---- E* (the orchestrator's expectation)
banner("E*  'making the cold mass from dark energy turns a0 into roughly the rival a0 ~ H(z)'")
estar = "n/a (MUTATE=1)"
if MUTATE != 1:
    rows = []
    for f in FORMS:
        for k, v in resA[f].items():
            if v is not None:
                rows.append((f, k, v))
    g1pass_make = [(f, k, v) for f, k, v in rows if v["F_made"] >= 0.5 and v["G1"].startswith("PASS")]
    rival_like = [(f, k, v) for f, k, v in rows if v["phi"][2.5] >= 0.8 and v["phi"][5.0] >= 0.8]
    maxmake = [(f, k, v) for f, k, v in rows if k in ("all", "0.99")]
    P("  G1-passing rows that make >= half the cold mass: %d" % len(g1pass_make))
    P("  rows with phi >= 0.8 at z = 2.5 and 5: %s" % ([(f, k) for f, k, v in rival_like] or "none"))
    for f, k, v in maxmake:
        P("  maximal making, %s (F_made %.4f, xi %.4f): phi(1) %.3f, phi(2.5) %.3f, phi(5) %.3f, phi(10) %.3f, phi(100) %.3f, phi(1090) %.3f; a0(2.5)/a0(0) = %.3f vs rival E(2.5) = %.3f; a0(5)/a0(0) = %.3f vs E(5) = %.3f" % (
            f, v["F_made"], v["xi"], v["phi"][1.0], v["phi"][2.5], v["phi"][5.0], v["phi"][10.0], v["phi"][100.0], v["phi"][ZREC], v["a0ratio"][2.5], E_lcdm(2.5), v["a0ratio"][5.0], E_lcdm(5.0)))
    if any(True for f, k, v in g1pass_make if v["phi"][2.5] >= 0.8 and v["phi"][5.0] >= 0.8):
        estar = "HOLDS"
    elif rival_like:
        estar = "HOLDS-ONLY-OUTSIDE-G1"
    elif any(v["phi"][5.0] >= 0.1 for f, k, v in rows):
        estar = "PARTIAL-SHAPE"
    else:
        estar = "DOES-NOT-HOLD"
    P("  E* label: %s" % estar)

# ========================================================================================================== reading B
banner("B  early transfer, completed before recombination (after z_t rho_DE = rho_L0, a0 flat at z < z_t)")
H0_invMpc = H0KMS / C_KMS
Z_K02 = 0.2 / (H0_invMpc * math.sqrt(OR)) - 1       # radiation era: k = aH = H0 sqrt(Omega_r)(1+z)
P("  horizon entry of k = 0.2/Mpc (radiation era, computed): z = %.3g" % Z_K02)
ZT = [1100.0, ZEQ, 1e4, 7e4, 1e5, 1e6, 1e8, ZBBN, 1e9, 1e10]
resB = {"inst": {}, "exp": {}, "pow": {}, "step": {}}
P("")
P("B-inst (all of today's cold mass created at z_t; the minimum pre-transfer vacuum rho_DE = Omega_L + Omega_c (1+z_t)^3):")
P("  %-9s %-11s %-10s %-10s %-10s %-11s %-11s %-9s %-10s %-10s" % ("z_t", "rhoDE/rho_c0", "f_EDE(z_t)", "DE/rad", "DE/baryon", "remnant", "ln(1/rem)", "G5-EDE", "DE/rad@BBN", "G5-BBN"))
for zt in ZT:
    rde = OL + OC * (1 + zt) ** 3
    rb, rr = OB * (1 + zt) ** 3, OR * (1 + zt) ** 4
    f = rde / (rde + rb + rr)
    rem = OL / rde
    # EDE window [1e3, 1e5]: before z_t the vacuum is rde (constant); f(z) largest at max(z_t, 1e3) if z_t <= 1e5
    if zt <= 1e5:
        zz = max(zt, 1e3)
        fwin = rde / (rde + OB * (1 + zz) ** 3 + OR * (1 + zz) ** 4)
    else:
        zz = 1e5
        fwin = OL / (OL + OM * (1 + zz) ** 3 + OR * (1 + zz) ** 4)
    bbn = (rde / (OR * (1 + ZBBN) ** 4)) if zt < ZBBN else (OL / (OR * (1 + ZBBN) ** 4))
    g5e = "PASS" if fwin <= 0.10 else "FAIL"
    g5b = "PASS" if bbn <= 0.040 else "FAIL"
    resB["inst"][str(zt)] = dict(rhoDE_before=rde, f_EDE_zt=f, DE_over_rad=rde / rr, DE_over_baryon=rde / rb, remnant=rem, ln_inv_remnant=math.log(1 / rem),
                                 fwin=fwin, G5_EDE=g5e, DE_over_rad_BBN=bbn, G5_BBN=g5b, modes_entered_before=zt < Z_K02)
    P("  %-9.4g %-11.3e %-10.3e %-10.3e %-10.3e %-11.3e %-11.2f %-9s %-10.2e %-10s" % (zt, rde / (OC * (1 + zt) ** 3), f, rde / rr, rde / rb, rem, math.log(1 / rem), g5e + ("(%.2g)" % fwin), bbn, g5b))
P("  (f_EDE(z_t) = rho_DE/(rho_DE + rho_b + rho_r) just before the transfer, no cold matter yet; 'remnant' = rho_L0/rho_DE(z_t), the fraction of the")
P("   pre-transfer vacuum a single-vacuum reading must leave behind, exactly; ln(1/rem) = the integrated decay rate int Gamma dt it must hit)")

# ---- B-step: numerical check of the instantaneous bound
def solve_step(zt, rX, Kr=2000.0):
    """rho_X constant (Q = 0) before z_t; from z_t on Q = Gamma rho_X with Gamma = Kr H_LCDM(z_t) (a sharp decay; H includes rho_X itself)."""
    xt = -math.log(1 + zt)
    Gam = QFAC * Kr * E_lcdm(zt)
    def rhs(xx, y):
        lX, u = y
        aa = math.exp(xx)
        rX_ = math.exp(lX)
        H = math.sqrt(rX_ + OL + u / aa ** 3 + OB / aa ** 3 + OR / aa ** 4)
        return [-Gam / H, Gam / H * rX_ * aa ** 3]
    ev = lambda xx, y: y[0] - (math.log(rX) - 60)
    ev.terminal = True
    s = solve_ivp(rhs, [xt, 0.0], [math.log(rX), 0.0], method="DOP853", rtol=1e-11, atol=1e-14, events=ev, max_step=0.01)
    return s.y[1, -1]
P("")
if MUTATE != 1:
    errs = []
    for zt in (1100.0, 1e5, 1e8):
        rX = brentq(lambda lr: solve_step(zt, math.exp(lr)) - OC, math.log(OC * (1 + zt) ** 3 * 0.5), math.log(OC * (1 + zt) ** 3 * 2.0), xtol=1e-12)
        ratio = math.exp(rX) / (OC * (1 + zt) ** 3)
        errs.append(abs(ratio - 1))
        resB["step"][str(zt)] = ratio
        P("  B-step (Gamma = 2000 H_LCDM(z_t)) z_t = %.3g: rho_X(before)/[Omega_c (1+z_t)^3] = %.5f (sympy, constant K = Gamma/H: 1 - 3/K = %.5f)" % (zt, ratio, 1 - 3 / 2000))
    check("K5", "a sharp numerical transfer reproduces the instantaneous bound rho_DE(before) = rho_c(z_t) within 2%", "max |ratio - 1| = %.4f" % max(errs), max(errs) < 0.02)

# ---- B-exp: a separate vacuum component decaying at constant rate Gamma = H_LCDM(z_G)
def solve_exp(zG, lrX):
    Gam = QFAC * E_lcdm(zG)
    zi = zG * 1e3
    x0 = -math.log(1 + zi)
    def rhs(xx, y):
        lX, u = y
        aa = math.exp(xx)
        rX_ = math.exp(lX)
        H = math.sqrt(rX_ + OL + u / aa ** 3 + OB / aa ** 3 + OR / aa ** 4)
        return [-Gam / H, Gam / H * rX_ * aa ** 3]
    ev = lambda xx, y: y[0] - (lrX - 80)
    ev.terminal = True
    s = solve_ivp(rhs, [x0, 0.0], [lrX, 0.0], method="DOP853", rtol=1e-11, atol=1e-14, events=ev, dense_output=True, max_step=0.05)
    return s
def u_at(s, z):
    xx = -math.log(1 + z)
    if xx >= s.t[-1]:
        return s.y[1, -1]
    if xx <= s.t[0]:
        return 0.0
    return s.sol(xx)[1]
def rX_at(s, z):
    xx = -math.log(1 + z)
    if xx >= s.t[-1]:
        return 0.0
    return math.exp(s.sol(xx)[0])
P("")
P("B-exp (an extra vacuum rho_X, w = -1, decaying at constant Gamma = H_LCDM(z_G); the remnant Omega_L is a SEPARATE constant):")
P("  (fDE max over z >= 50; 'made>rec' of order 1e-11 or below is solver noise, i.e. zero; 'made<z_k' = fraction of today's cold mass made after z_k = %.3g," % Z_K02)
P("   the horizon entry of k = 0.2/Mpc: those Planck-scale modes entered with less or no cold matter; the mode-level CMB effect is NOT computed)")
P("  %-8s %-12s %-12s %-10s %-10s %-11s %-11s %-10s %-10s %-9s %-9s" % ("z_G", "rho_X,i/Om_L", "rho_X,i/rc(zG)", "fDE max", "at z", "made>rec", "made<z_k", "z_50%", "z_99%", "G1", "G5"))
bexp_ok = True
for zG in [1100.0, ZEQ, 1e4, 7e4, 1e5, 1e6, 1e8]:
    guess = math.log(OC * (1 + zG) ** 3)
    try:
        lr = brentq(lambda l: u_at(solve_exp(zG, l), 0.0) - OC, guess - 5, guess + 8, xtol=1e-10)
    except ValueError:
        bexp_ok = False
        P("  %-8.3g no vacuum amount makes Omega_c (Q = 0 in MUTATE=1)" % zG)
        resB["exp"][str(zG)] = None
        continue
    s = solve_exp(zG, lr)
    zz = np.logspace(math.log10(50.0), math.log10(zG * 1e3) - 0.01, 600)   # z >= 50: the early-DE maximum, not today's Lambda era
    fde = [(rX_at(s, z) + OL) / (rX_at(s, z) + OL + u_at(s, z) * (1 + z) ** 3 + OB * (1 + z) ** 3 + OR * (1 + z) ** 4) for z in zz]
    imax = int(np.argmax(fde))
    win = [f for f, z in zip(fde, zz) if 1e3 <= z <= 1e5]
    fwin = max(win) if win else 0.0
    mrec = 1 - u_at(s, ZREC) / OC
    mk = 1 - u_at(s, Z_K02) / OC
    z50 = brentq(lambda lz: u_at(s, 10 ** lz) / OC - 0.5, 0.0, math.log10(zG * 1e3) - 0.01)
    z99 = brentq(lambda lz: u_at(s, 10 ** lz) / OC - 0.99, 0.0, math.log10(zG * 1e3) - 0.01)
    bbn = rX_at(s, ZBBN) / (OR * (1 + ZBBN) ** 4) if ZBBN < zG * 1e3 else 0.0
    g1 = "PASS" if mrec <= 0.03 else "FAIL"
    g5 = "PASS" if (fwin <= 0.10 and bbn <= 0.040) else "FAIL"
    rXi = math.exp(lr)
    resB["exp"][str(zG)] = dict(rhoX_i=rXi, rhoX_i_over_OL=rXi / OL, rhoX_i_over_rc_zG=rXi / (OC * (1 + zG) ** 3), fDE_max=fde[imax], z_at_max=float(zz[imax]),
                                fwin=fwin, made_after_rec=mrec, made_after_k02=mk, z50=10 ** z50, z99=10 ** z99, DE_over_rad_BBN=bbn, G1=g1, G5=g5)
    P("  %-8.3g %-12.3e %-12.3f %-10.3e %-10.3g %-11.3e %-11.3e %-10.3g %-10.3g %-9s %-9s" % (zG, rXi / OL, rXi / (OC * (1 + zG) ** 3), fde[imax], zz[imax], mrec, mk, 10 ** z50, 10 ** z99, g1, g5 + "(%.2g)" % fwin))

check("H-B1", "B: a vacuum amount exists that makes today's Omega_c from the vacuum for every tested epoch (the energy is available if the vacuum was that large)",
      "B-exp shooting converged for all z_G" if bexp_ok else "no vacuum amount makes Omega_c (Q = 0)", bexp_ok)

# ---- B-pow
P("")
P("B-pow (a single vacuum, Q = xi H rho_DE before z_t, off after; rho_DE continuous = Omega_L at z_t):")
powrows = []
for zt in (1100.0, 1e5, 1e8):
    for v in (0.5, 1.0, 2.0, 2.9):
        made = v * OL / (3 - v)
        need = OC * (1 + zt) ** 3
        powrows.append((zt, v, made / need))
        resB["pow"]["%g|%g" % (zt, v)] = made / need
    P("  z_t = %.3g: created rho_c(z_t)/needed = %s" % (zt, ", ".join("%.2e (xi %.1f)" % (m, v) for z_, v, m in powrows if z_ == zt)))
if MUTATE != 1:
    # numeric check of S5 at z_t = 1e5, xi = 1
    zt, v = 1e5, 1.0
    xt = -math.log(1 + zt)
    def rhs(xx, y):
        rde, u = y
        aa = math.exp(xx)
        return [-v * rde, v * rde * aa ** 3]
    s = solve_ivp(rhs, [xt - 25, xt], [OL * math.exp(25 * v), 0.0], method="DOP853", rtol=1e-12, atol=1e-300)
    num = s.y[1, -1] * (1 + zt) ** 3
    check("K6", "B-pow numerics reproduce created rho_c(z_t) = xi Omega_L/(3 - xi) (xi = 1, z_t = 1e5)", "%.6e vs %.6e" % (num, v * OL / (3 - v)), abs(num / (v * OL / (3 - v)) - 1) < 1e-6)
    check("H-B2", "B-pow cannot make the mass: created/needed < 1e-6 for every tested (z_t, xi < 3)", "max %.2e" % max(m for _, _, m in powrows), max(m for _, _, m in powrows) < 1e-6, lb=False)

# ---- B: a0
P("")
P("B, a0(z): after z_t rho_DE = Omega_L exactly, so a0(z)/a0(0) = 1 for all z < z_t (G2a PASS, G2b FLAT-LIKE) -- the framework's own constant rho_L,")
P("  i.e. a PASS-AS-RESTATEMENT.  Before z_t, a0 ~ sqrt(rho_DE) would be sqrt(1/remnant) larger (%.3g at z_t = 1100, %.3g at 1e8); no galaxies exist then," % (
    math.sqrt(1 / resB["inst"]["1100.0"]["remnant"]), math.sqrt(1 / resB["inst"]["100000000.0"]["remnant"])))
P("  and the record's cosmology notes that a0 enters no linear coefficient (CFG4_cosmology.out header, XR26 part 1): not scored.")

# ========================================================================================================== reading C
banner("C  clusters: a transfer localised in bound systems")
Delta = 500.0
fcold = 6.8 / 7.8
vac_frac = OL / Delta                                  # rho_L / <rho>_500 at z = 0
short = fcold / vac_frac
P("  vacuum energy inside R500 / mean density inside R500 = Omega_L/500 = %.3e; cold fraction needed (6.8x baryons) = %.3f" % (vac_frac, fcold))
P("  -> converting ALL the vacuum energy in the volume gives %.2e of the cold mass: %.0fx short" % (vac_frac / fcold, short))
Mpc_per_Gyr_c = C_KMS * 3.15576e16 / 3.0856775814913673e19   # c x 1 Gyr in Mpc
eps = {}
for R in (1.0, 1.4):
    for tG in (5.0, 10.0):
        e = fcold * Delta * R / (3 * OL * Mpc_per_Gyr_c * tG)
        eps["R%.1f_t%.0f" % (R, tG)] = e
        P("  an inflow at c through the R500 sphere (R = %.1f Mpc, over %.0f Gyr) must carry a fraction eps = %.3f of the vacuum energy flux rho_L c" % (R, tG, e))
P("  compare CFG176: a w = -1 vacuum carries NO flux (eps = 0 exactly); a NEC-respecting non-Lambda medium carries at most 0.078 of the cosmic")
P("  column (0.090 NEC-only, CFG195), a cosmic-mean, perfect-fluid, integrated number, not a per-cluster convergent inflow.")
P("  CFG131 D1: for a Lorentz-invariant vacuum, d_mu rho_L = Q u_mu, so rho_L is uniform on the cold fluid's slices and Q cannot be localised;")
P("  CFG131 A5: in a stationary halo the energy equation forces Q = 0.")
check("H-C1", "the vacuum energy inside R500 is < 1% of the cluster's cold mass (a local, non-flowing conversion cannot supply it)", "%.2e" % (vac_frac / fcold), vac_frac / fcold < 0.01, lb=False)

# ========================================================================================================== verdicts
banner("VERDICTS (per the frozen gates; never pooled)")
V = {}
if MUTATE != 1:
    a_g1 = {f: resA[f]["0.03"] for f in FORMS}
    V["A"] = dict(
        G1="PASS only for F_made <= 0.03: the transfer makes <= 3% of the cold mass; the other >= 97% must pre-exist at recombination (so (A) is not the cold mass); making >= half FAILS G1",
        G2="at the G1 tolerance: " + "; ".join("%s %s / %s (max %.4f dex at z <= 5)" % (f, a_g1[f]["G2a"], a_g1[f]["G2b"], a_g1[f]["maxdex_z5"]) for f in FORMS),
        G3="PASS for Q >= 0 while rho_c >= 0 (vacuum stress w = -1 saturates the NEC); separate conservation (CFG195 P1) broken by construction; no committed action (CFG131 D2: Q != 0 breaks the HT shift symmetry)",
        G4="+1 (xi) per form; Omega_c not replaced",
        G5="PASS at the G1 tolerance (EDE and BBN negligible)",
        Estar=estar)
    V["B"] = dict(
        G1="PASS-AS-RESTATEMENT for z_t high enough that <= 3% is made after z_rec (B-inst by construction); the amount = the pre-transfer vacuum, one-for-one with Omega_c",
        G2="PASS-AS-RESTATEMENT: a0 exactly flat at z < z_t (the framework's constant rho_L)",
        G3="PASS (Q >= 0, rho >= 0); no action",
        G4="+1 (z_t or Gamma) plus either a separate remnant vacuum constant (B-exp) or a tuned endpoint (single vacuum: remnant 1e-9 at z_t = 1100 to 1e-24 at 1e8)",
        G5="FAIL (EDE) for z_t <~ 1e4-3e4; PASS above (conditional on the UNVERIFIED bounds); BBN never binding for B-inst",
        coldness="PASS BY ASSUMPTION (Q^mu || u_c, Q independent of rho_c -> c_s^2 = 0 allowed, CFG131 D1); not derived",
        overall="REDUCES-TO CDM with a vacuum origin story: NON-DIAGNOSTIC in linear cosmology (GDM) when z_t >~ 1e5; testable only where it fails (low z_t)")
    V["C"] = dict(overall="FAIL under the premise (Lorentz-invariant w = -1 vacuum): Q cannot be localised (CFG131 D1), is zero in a stationary halo (A5), and the vacuum in the volume is ~%.0fx short; a flowing non-Lambda medium REDUCES-TO door 11 (CFG176/CFG195). Under (B) the cluster cold mass is the cosmic cold fluid that fell in, as in CDM." % short)
    for k, v in V.items():
        P("  (%s)" % k)
        for kk, vv in v.items():
            P("     %-9s %s" % (kk, vv))

# ---- hand predictions (reported)
banner("Hand predictions (frozen section 5), scored as reported checks")
if MUTATE == 0:
    A1 = resA["A1"]["0.03"]; A2 = resA["A2"]["0.03"]; A1all = resA["A1"]["all"]
    check("P1", "A1 at F_made 0.03: xi ~ 0.035, a0(5)/a0(0) ~ 1.03", "xi %.4f, a0(5) %.4f" % (A1["xi"], A1["a0ratio"][5.0]), abs(A1["xi"] / 0.035 - 1) < 0.15 and abs(A1["a0ratio"][5.0] - 1.03) < 0.01, lb=False)
    check("P2", "A2 at F_made 0.03: xi ~ 0.0042, a0(5)/a0(0) in 1.05-1.06", "xi %.5f, a0(5) %.4f" % (A2["xi"], A2["a0ratio"][5.0]), abs(A2["xi"] / 0.0042 - 1) < 0.15 and 1.045 <= A2["a0ratio"][5.0] <= 1.065, lb=False)
    check("P3", "A1 makes all the cold mass at xi ~ 0.84 with phi(5) in 0.35-0.40", "xi %.4f, phi(5) %.3f" % (A1all["xi"], A1all["phi"][5.0]), abs(A1all["xi"] - 0.84) < 0.03 and 0.35 <= A1all["phi"][5.0] <= 0.40, lb=False)
    bi = resB["inst"]
    check("P4", "B-inst f_EDE ~ 0.64 / 0.42 / 0.03 / 3e-5 at z_t = 1100 / 3423 / 1e5 / 1e8; remnant ~ 2e-9 (1100), 3e-24 (1e8)",
          "%.3f / %.3f / %.3f / %.1e; %.1e, %.1e" % (bi["1100.0"]["f_EDE_zt"], bi[str(ZEQ)]["f_EDE_zt"], bi["100000.0"]["f_EDE_zt"], bi["100000000.0"]["f_EDE_zt"], bi["1100.0"]["remnant"], bi["100000000.0"]["remnant"]),
          abs(bi["1100.0"]["f_EDE_zt"] - 0.64) < 0.02 and abs(bi[str(ZEQ)]["f_EDE_zt"] - 0.42) < 0.02 and abs(bi["100000.0"]["f_EDE_zt"] - 0.03) < 0.005
          and abs(bi["100000000.0"]["f_EDE_zt"] / 3e-5 - 1) < 0.1 and abs(bi["1100.0"]["remnant"] / 2e-9 - 1) < 0.1 and abs(bi["100000000.0"]["remnant"] / 3e-24 - 1) < 0.2, lb=False)
    check("P5", "B-pow with xi < 3 cannot make the mass", "max created/needed %.2e" % max(m for _, _, m in powrows), max(m for _, _, m in powrows) < 1e-6, lb=False)
    check("P6", "E* = PARTIAL-SHAPE (only outside G1); every (A) row at the G1 tolerance FLAT-LIKE", "E* %s; G2b at tolerance %s" % (estar, [resA[f]["0.03"]["G2b"] for f in FORMS]),
          estar == "PARTIAL-SHAPE" and all(resA[f]["0.03"]["G2b"] == "FLAT-LIKE" for f in FORMS), lb=False)
    zpass = min(float(z) for z, v in resB["exp"].items() if v and v["G5"] == "PASS" and v["G1"] == "PASS")
    check("P7", "(B) passes G1 and G5 (as restatement) for z_t >~ 3e4 (B-exp: smallest passing z_G in the grid)", "smallest passing z_G = %.3g" % zpass, zpass <= 1e5 and zpass >= 1e4, lb=False)
    check("P8", "(C) vacuum inside R500 ~ 1e-3 of the cold mass", "%.2e" % (vac_frac / fcold), 5e-4 < vac_frac / fcold < 5e-3, lb=False)

# ---- MUTATE=1 flatness check
if MUTATE == 1:
    s = solveA("A1", 0.1); s2 = solveA("A2", 0.1); s3 = solveA("A3", 0.1)
    d = max(abs(math.sqrt(st(ss, z)[0] / OL) - 1) for ss in (s, s2, s3) for z in (1, 5, ZREC, 1e5))
    check("M1", "MUTATE=1 (Q = 0): rho_DE constant and a0 flat to 1e-10 at nominal xi = 0.1 in every form", "max |a0 ratio - 1| = %.1e" % d, d < 1e-10, lb=False)

# ---- summary
nlb = sum(1 for c in CHECKS if not c["ok"] and c["load_bearing"])
P("")
P("SUMMARY (MUTATE=%d): %d/%d checks pass; load-bearing failures = %d" % (MUTATE, sum(c["ok"] for c in CHECKS), len(CHECKS), nlb))
for c in CHECKS:
    if not c["ok"]:
        P("   failed: %s %s" % (c["tag"], "(load-bearing)" if c["load_bearing"] else "(reported)"))
json.dump(dict(mutate=MUTATE, criteria_sha256=h, inputs=dict(OC=OC, OB=OB, OL=OL, OR=OR, H0=H0KMS, z_rec=ZREC, z_eq=ZEQ, z_BBN=ZBBN, z_k02=Z_K02),
               cfg131_line_A3_xi=xi131, line1pct=line1, A=resA, B=resB, C=dict(vac_frac=vac_frac, cold_frac=fcold, short_factor=short, inflow_eps=eps),
               Estar=estar, verdicts=V, checks=CHECKS), open(JS, "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating,)) else str(o))
_f.close()
sys.exit(1 if nlb else 0)
