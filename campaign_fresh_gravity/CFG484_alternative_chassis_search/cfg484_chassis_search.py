#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg484_chassis_search.py -- CFG484: search for a relativistic chassis for candidate B that passes every chassis gate.

Frozen criteria: FROZEN_CRITERIA.md (committed alone before this script). Theory survey + checks, offline, no
downloads, read-only on every other lane. kappa = 1/2 is FITTED. Both a0 footings are run wherever a0 enters.
No dark-matter particle species is added; the cold fluid's mass is still required. Untested is not passed.

What it does
  1. Controls K1-K8 (reproduce committed numbers; unit tests of the harness).
  2. NC1 first gate pass (GR + Lambda chassis, MOND only in the cold-fluid sector, target keyed to the fluid's own
     4-acceleration): N1a-N1g.
  3. NC2 first gate pass (alpha_c screened in strong fields): N2. NC3 / NC5 argument rows.
  4. Scores every row (record table in cfg484_record.py + new classes) with the frozen rule, ranks them, names the
     top candidate and the lane verdict.
  5. MUTATE (CFG484_MUTATE=1): the harness is applied to known-failing completions fed as the candidate under test;
     each must FAIL at its recorded gate; the final "candidate WORKS" check fails, so rc = 1 as required.

Run:   python3 cfg484_chassis_search.py            (main; ~30 s)
       CFG484_MUTATE=1 python3 cfg484_chassis_search.py
"""
import os
import sys
import json
import time
import math
import re

sys.dont_write_bytecode = True

import numpy as np
from scipy.integrate import quad
from scipy.special import ellipk, ellipe, i0, i1, k0, k1, j0, j1
import sympy as sp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))


def repo_root():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "campaign_fresh_gravity")):
        return os.path.abspath(env)
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("repo root not found; set ZF_REPO")


ROOT = repo_root()
CFG = os.path.join(ROOT, "campaign_fresh_gravity")
sys.path.insert(0, HERE)
import cfg484_record as REC  # noqa: E402
sys.path.insert(0, os.path.join(CFG, "CFG44_fluid_target"))
import Bcommon as BC  # noqa: E402  (read-only: kernels nu_p2, nu_mono)

MUT = os.environ.get("CFG484_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


def rel(path):
    return "<repo>/" + os.path.relpath(path, ROOT)


CHECKS = {}


def check(name, ok, detail, load_bearing=True):
    ok = bool(ok)
    CHECKS[name] = dict(ok=ok, detail=str(detail), load_bearing=load_bearing)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}: {detail}")
    return ok


# ---------------------------------------------------------------------------------------------------- constants (SI)
G = 6.67430e-11
C_LIGHT = 299792458.0
MSUN = 1.98892e30
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ["canonical", "alt"]
R_MARS, R_SAT = 1.523679 * AU, 9.5826 * AU
EPH = {"Mars": 1.4e-15, "Saturn": 7.0e-15}          # MI_FIELD_THEORY_RESULTS section 5.1 (LIT, provisional)
Q2C, Q2SIG = 3e-27, 3e-27                           # CFG357 (Hees+ via the record)
GAMMA_BOUND = 2.3e-5                                # Cassini (LIT)
ALPHA2_STRICT = 1.6e-9
NU = {"P2": BC.nu_p2, "nu_mono": BC.nu_mono}
_trap = getattr(np, "trapezoid", None) or np.trapz   # numpy 1.x / 2.x


def nu_prime(name, y):
    y = np.asarray(y, float)
    if name == "P2":
        return -1.0 / (2.0 * y * y * np.sqrt(1.0 + 1.0 / y))
    h = 1e-3 * math.log(10.0)
    return (BC.nu_mono(y * math.exp(h)) - BC.nu_mono(y * math.exp(-h))) / (y * (math.exp(h) - math.exp(-h)))


OUT = dict(lane="CFG484", mutate=MUT, frozen_criteria="FROZEN_CRITERIA.md (committed alone before any script)",
           inputs=dict(a0=A0, ephemeris_bounds=EPH, Q2=[Q2C, Q2SIG], gamma_bound=GAMMA_BOUND,
                       alpha2_strict=ALPHA2_STRICT))

P("=" * 110)
P("CFG484: search for a relativistic chassis for candidate B" + ("   [MUTATE]" if MUT else ""))
P("kappa = 1/2 FITTED; both footings; theory + checks, no downloads; untested is not passed")
P(f"repo: <repo>   record module: {rel(os.path.join(HERE, 'cfg484_record.py'))}")
P("=" * 110)


# ------------------------------------------------------------------------------------------------ interval engine
def _num(t):
    t = t.strip()
    if t in ("inf", "+inf"):
        return math.inf
    if t == "-inf":
        return -math.inf
    return float(t)


def parse_set(s):
    """CFG467 set strings: 'EMPTY', '{0}', '(0, 0.5) U (0.5, 2)', '[9.6e-14, inf)'. -> list of (lo, hi, lc, hc)."""
    s = s.strip()
    if s == "EMPTY":
        return []
    out = []
    for part in s.split(" U "):
        part = part.strip()
        if part.startswith("{"):
            for v in part.strip("{}").split(","):
                x = _num(v)
                out.append((x, x, True, True))
            continue
        lc, hc = part[0] == "[", part[-1] == "]"
        lo, hi = part[1:-1].split(",")
        out.append((_num(lo), _num(hi), lc, hc))
    return out


def _icap(a, b):
    lo, lc = (a[0], a[2]) if a[0] > b[0] else ((b[0], b[2]) if b[0] > a[0] else (a[0], a[2] and b[2]))
    hi, hc = (a[1], a[3]) if a[1] < b[1] else ((b[1], b[3]) if b[1] < a[1] else (a[1], a[3] and b[3]))
    if lo < hi or (lo == hi and lc and hc):
        return (lo, hi, lc, hc)
    return None


def intersect(A, B):
    out = []
    for a in A:
        for b in B:
            c = _icap(a, b)
            if c is not None:
                out.append(c)
    return out


def fmt_set(A):
    if not A:
        return "EMPTY"
    parts = []
    for lo, hi, lc, hc in A:
        if lo == hi:
            parts.append("{%g}" % lo)
        else:
            parts.append(("[" if lc else "(") + "%g, %g" % (lo, hi) + ("]" if hc else ")"))
    return " U ".join(parts)


# ------------------------------------------------------------------------------------------------ classification
GG, HH = REC.GATES_G, REC.GATES_H
PASSLIKE = ("PASS", "NA")


def classify(row):
    g = [row["G"][k][0] for k in GG]
    h = [row["H"][k][0] for k in HH]
    if "FAIL" in g:
        return "FAILS"
    if all(x in PASSLIKE for x in g):
        return "WORKS" if all(x in PASSLIKE for x in h) else "CHASSIS-CLEAN"
    if "LEN" in g:
        return "TENSION"
    return "INCOMPLETE"


def rank_key(row):
    g = [row["G"][k][0] for k in GG]
    h = [row["H"][k][0] for k in HH]
    n = row["constants"]["n"]
    return (g.count("FAIL"), g.count("LEN"), g.count("UNT") + g.count("COND"),
            h.count("FAIL"), h.count("LEN"), h.count("UNT") + h.count("COND"),
            n if n is not None else 99)


def gates_with(row, code, which=None):
    keys = (GG + HH) if which is None else which
    return [k for k in keys if (row["G"].get(k) or row["H"].get(k))[0] == code]


# ==================================================================================================== CONTROLS
P("\n[controls]")
# K1 ---------------------------------------------------------------------------------------------------------
cfg467_json = os.path.join(CFG, "CFG467_alpha_c_sign_tension", "cfg467_results.json")
J467 = json.load(open(cfg467_json))
u = J467["union"]
check("K1 CFG467 committed JSON: union I_strict EMPTY, I_len [9.6240e-14, 3.2000e-09], verdict TENSION",
      u["I_strict"] == "EMPTY" and u["I_len"] == "[9.6240e-14, 3.2000e-09]" and J467["verdict"] == "TENSION",
      f"read {rel(cfg467_json)}: I_strict {u['I_strict']}, I_len {u['I_len']}, verdict {J467['verdict']}")

# K2 ---------------------------------------------------------------------------------------------------------
gN_s, a0_s = sp.symbols("g_N a_0", positive=True)
g_s = sp.sqrt(gN_s ** 2 + a0_s * gN_s)
k2 = sp.expand(g_s ** 2 + (a0_s / 2) ** 2 - (gN_s + a0_s / 2) ** 2)
check("K2 CFG373 perfect square g^2 + a_L^2 = (g_N + a_L)^2 for P2 with a_L = a0/2",
      k2 == 0, f"expand(...) = {k2}")

# K3 ---------------------------------------------------------------------------------------------------------
x = np.logspace(-3, 3, 2001)
gN_x = 1.0 / x ** 2                       # units a0, r_M; y = g_N/a0 = 1/x^2
nu_x = BC.nu_p2(gN_x)
# r^2 (g - g_N)/G in units of M, written cancellation-free: for P2, nu^2 - 1 = 1/y, so nu - 1 = 1/(y (nu + 1)).
# (Run 1 used x^2 (nu - 1) g_N and M(sqrt(1+x^2) - 1) directly: float cancellation at x = 1e-3, where nu - 1 ~ 5e-7,
#  gave 1.16e-10 > 1e-10 and K3 FAILED; kept as cfg484_chassis_search_run1.out. Same identity, same tolerance.)
Mc_identity = x ** 2 * gN_x / (gN_x * (nu_x + 1.0))
Mc_cfg44 = x ** 2 / (np.sqrt(1 + x ** 2) + 1)     # = sqrt(1 + x^2) - 1, exactly
k3 = np.max(np.abs(Mc_identity / Mc_cfg44 - 1))
check("K3 P2 point-mass cold mass M(sqrt(1+x^2) - 1) (CFG44 B1) from the spherical identity", k3 <= 1e-10,
      f"max rel diff {k3:.2e} over x in [1e-3, 1e3]")

# K4 ---------------------------------------------------------------------------------------------------------
fac_sat = (A0["canonical"] / 2) / EPH["Saturn"]
fac_mars = (A0["canonical"] / 2) / EPH["Mars"]
check("K4 a0/2 anomaly reproduces MI_FIELD_THEORY_RESULTS 5.1 exclusions (Saturn 6686x, Mars 33429x, canonical)",
      abs(fac_sat / 6686 - 1) <= 0.01 and abs(fac_mars / 33429 - 1) <= 0.01,
      f"Saturn {fac_sat:.0f}x, Mars {fac_mars:.0f}x")

# K5 ---------------------------------------------------------------------------------------------------------
cfg357_py = os.path.join(CFG, "CFG357_heat_filter_cassini_q2", "cfg357_heat_filter_q2.py")
txt357 = open(cfg357_py).read()
m357 = re.search(r"Q2C,\s*SIG\s*=\s*([0-9.eE+-]+),\s*([0-9.eE+-]+)", txt357)
check("K5 CFG357 holds Q2C = SIG = 3e-27", m357 is not None and float(m357.group(1)) == Q2C
      and float(m357.group(2)) == Q2SIG, f"{rel(cfg357_py)}: {m357.group(0) if m357 else 'not found'}")

# K6 ---------------------------------------------------------------------------------------------------------
yk = np.array([0.1, 1.0, 2.0])
nu_rar = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))
k6a = np.max(np.abs(BC.nu_mono(yk) / nu_rar(yk) - 1))
yy = 10 ** np.linspace(-3, 3, 60001)
dev = np.abs(np.log10(BC.nu_mono(yy) / nu_rar(yy)))
imax = int(np.argmax(dev))
check("K6 nu_mono = nu_RAR at y = 0.1, 1, 2; max deviation 0.0104 +- 0.0005 dex at y = 14.35 +- 1",
      k6a <= 1e-6 and abs(dev[imax] - 0.0104) <= 5e-4 and abs(yy[imax] - 14.35) <= 1.0,
      f"rel diff {k6a:.1e}; max {dev[imax]:.5f} dex at y = {yy[imax]:.2f}")

# K7 ---------------------------------------------------------------------------------------------------------
t1 = fmt_set(intersect(parse_set("(0, 0.5) U (0.5, 2)"), parse_set("{0}")))
t2 = fmt_set(intersect(parse_set("[1, 2]"), parse_set("(1.5, 3)")))
t3 = fmt_set(intersect(parse_set("[9.6240e-14, inf)"), parse_set("(-inf, 2)")))
_allp = {k: ("PASS", "") for k in GG}
_allh = {k: ("PASS", "") for k in HH}
toy = {
    "works": dict(G=_allp, H=_allh, constants=dict(n=0)),
    "clean": dict(G=_allp, H=dict(_allh, H3=("UNT", "")), constants=dict(n=0)),
    "fails": dict(G=dict(_allp, G12=("FAIL", "")), H=_allh, constants=dict(n=0)),
    "tension": dict(G=dict(_allp, G12=("LEN", "")), H=_allh, constants=dict(n=0)),
    "incomplete": dict(G=dict(_allp, G12=("UNT", "")), H=_allh, constants=dict(n=0)),
}
cls_ok = all(classify(v) == {"works": "WORKS", "clean": "CHASSIS-CLEAN", "fails": "FAILS", "tension": "TENSION",
                             "incomplete": "INCOMPLETE"}[k] for k, v in toy.items())
order = [k for k, _ in sorted(toy.items(), key=lambda kv: rank_key(kv[1]))]
check("K7 interval engine and classification/ranking on toy rows",
      t1 == "EMPTY" and t2 == "(1.5, 2]" and t3 == "[9.624e-14, 2)" and cls_ok
      and order[:2] == ["works", "clean"] and order[-1] == "fails",
      f"{t1}; {t2}; {t3}; classes ok {cls_ok}; rank order {order}")

# K8 ---------------------------------------------------------------------------------------------------------
t_, r_, th_, ph_ = sp.symbols("t r theta phi")
Gs, Ms, cs = sp.symbols("G M c", positive=True)
rs = 2 * Gs * Ms / cs ** 2
X = [t_, r_, th_, ph_]
gmet = sp.diag(-(1 - rs / r_), 1 / (1 - rs / r_), r_ ** 2, r_ ** 2 * sp.sin(th_) ** 2)
ginv = gmet.inv()


def christoffel(gm, gi, X):
    n = len(X)
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(gm[d, b], X[c]) + sp.diff(gm[d, c], X[b]) - sp.diff(gm[b, c], X[d]))
                              for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]


Gam = christoffel(gmet, ginv, X)


def riemann_up(a, b, c, d):  # R^a_{bcd}
    expr = sp.diff(Gam[a][b][d], X[c]) - sp.diff(Gam[a][b][c], X[d])
    expr += sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(4))
    return sp.simplify(expr)


Rup = [[[[riemann_up(a, b, c, d) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
Rdn = [[[[sp.simplify(sum(gmet[a, e] * Rup[e][b][c][d] for e in range(4))) for d in range(4)] for c in range(4)]
        for b in range(4)] for a in range(4)]
Kret = 0
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                if Rdn[a][b][c][d] != 0:
                    Kret += Rdn[a][b][c][d] * sum(ginv[a, a2] * ginv[b, b2] * ginv[c, c2] * ginv[d, d2] *
                                                  Rdn[a2][b2][c2][d2]
                                                  for a2 in [a] for b2 in [b] for c2 in [c] for d2 in [d])
Kret = sp.simplify(Kret)
k8 = sp.simplify(Kret - 48 * Gs ** 2 * Ms ** 2 / (cs ** 4 * r_ ** 6))
check("K8 Schwarzschild Kretschmann = 48 G^2 M^2/(c^4 r^6), finite for r > 0", k8 == 0, f"K = {Kret}")

# ==================================================================================================== NC1
P("\n" + "=" * 110)
P("NC1: GR + Lambda chassis, MOND only in the cold-fluid sector (target keyed to the fluid's own 4-acceleration)")
P("=" * 110)
NC1 = {}

# N1a --------------------------------------------------------------------------------------------------------
P("\n[N1a] black holes (G12)")
check("N1a G12 for the GR chassis: Schwarzschild/Kerr regular outside r = 0 (LIT-GR; K8 the computed instance); "
      "the cold fluid is test matter near holes", CHECKS["K8 Schwarzschild Kretschmann = 48 G^2 M^2/(c^4 r^6), finite "
                                                         "for r > 0"]["ok"], "K8 reused")

# N1b --------------------------------------------------------------------------------------------------------
P("\n[N1b] messenger (H2): the static fluid's own 4-acceleration is the total field; the target is local in it")
eps = sp.symbols("epsilon")
xs, ys, zs = sp.symbols("x y z")
Phi = sp.Function("Phi")(xs, ys, zs)
Xc = [t_, xs, ys, zs]
gw = sp.diag(-(1 + 2 * eps * Phi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
gwi = gw.inv()
acc = []
for i in range(1, 4):
    Gam_i_tt = sum(gwi[i, d] * (2 * sp.diff(gw[d, 0], Xc[0]) - sp.diff(gw[0, 0], Xc[d])) for d in range(4)) / 2
    a_i = Gam_i_tt / (1 + 2 * eps * Phi)            # a^i = Gamma^i_tt (u^t)^2 for a static observer
    acc.append(sp.simplify(sp.series(a_i, eps, 0, 2).removeO()))
n1b_i = all(sp.simplify(acc[i - 1] - eps * sp.diff(Phi, Xc[i])) == 0 for i in range(1, 4))
check("N1b(i) static congruence in ds^2 = -(1+2Phi)dt^2 + (1-2Phi)dx^2: a^i = d_i Phi + O(Phi^2) (sympy)", n1b_i,
      f"a^x = {acc[0]}")
yg = np.logspace(-8, 8, 20001)
mono = {k: bool(np.all(np.diff(yg * NU[k](yg)) > 0)) for k in NU}
# round trip of the inversion g_tot -> g_N for nu_mono
from scipy.optimize import brentq  # noqa: E402
rt = 0.0
for gt in [1e-3, 0.1, 1.0, 10.0, 1e3]:
    yN = brentq(lambda yv: yv * float(BC.nu_mono(np.array(yv))) - gt, 1e-12, 1e12, xtol=1e-14, rtol=1e-14)
    rt = max(rt, abs(yN * float(BC.nu_mono(np.array(yN))) / gt - 1))
check("N1b(ii) y nu(y) strictly increasing on [1e-8, 1e8] for nu_mono and P2 (inversion exists, target local in |A|)",
      all(mono.values()) and rt < 1e-9, f"monotone {mono}; nu_mono round trip {rt:.1e}")
NC1["N1b"] = dict(monotone=mono, roundtrip=rt, static_acc=str(acc[0]))

# N1c --------------------------------------------------------------------------------------------------------
P("\n[N1c] EP blindness (reported): NC1's target in a uniform external field is unchanged (ratio 1 exactly);")
P("      for comparison, the algebraic law's internal field at r = r_M (g_N = a0), aligned 1-D estimate:")
efe = {}
for k in NU:
    efe[k] = {}
    for ge in [0.01, 0.1, 1.0]:
        gi = NU[k](np.array(1.0 + ge)) * (1.0 + ge) - NU[k](np.array(ge)) * ge
        ratio = float(gi / (NU[k](np.array(1.0)) * 1.0))
        efe[k][str(ge)] = ratio
        P(f"      {k:8s} g_e = {ge:5.2f} a0: law internal field / isolated = {ratio:.4f}   NC1: 1 (EP)")
NC1["N1c_efe_law_ratio"] = efe

# N1d --------------------------------------------------------------------------------------------------------
P("\n[N1d] Solar System (G14): R1 embedded Sun (Liouville cap), R2/R3 Sun owns its own settled target")
MW_MB = 6e10 * MSUN
R0 = 8.2 * KPC
n1d = {}
R1_ok_all = True
for f in FOOTS:
    a0 = A0[f]
    rM = math.sqrt(G * MW_MB / a0)
    xx = R0 / rM
    rho_c = MW_MB * xx / (4 * math.pi * R0 ** 2 * rM * math.sqrt(1 + xx ** 2))      # P2 point-mass phantom density
    Mc = MW_MB * (math.sqrt(1 + xx ** 2) - 1)
    gN = G * MW_MB / R0 ** 2
    gt = math.sqrt(gN ** 2 + a0 * gN)
    Vc = math.sqrt(R0 * gt)
    sig = Vc / math.sqrt(2)
    row = dict(rM_kpc=rM / KPC, x=xx, rho_c_kg_m3=rho_c, rho_c_Msun_pc3=rho_c * PC ** 3 / MSUN, Vc_kms=Vc / 1e3)
    for boost in [1.0, 3.0]:
        rho = rho_c * boost
        fmax = rho / ((2 * math.pi) ** 1.5 * sig ** 3)
        res = {}
        for pl, rr in [("Mars", R_MARS), ("Saturn", R_SAT)]:
            Mcap = 4 * math.pi * fmax * (4 * math.pi / 3) * (2 * GM_SUN) ** 1.5 * (2.0 / 3.0) * rr ** 1.5
            dg_cap = G * Mcap / rr ** 2
            # the Sun's own nu_mono target density at rr, for the shortfall factor
            yv = GM_SUN / (rr ** 2 * a0)
            hh = 1e-3
            ff = lambda rq: rq ** 2 * (float(BC.nu_mono(np.array(GM_SUN / (rq ** 2 * a0)))) - 1) * GM_SUN / rq ** 2
            rho_tgt = (ff(rr * (1 + hh)) - ff(rr * (1 - hh))) / (2 * rr * hh) / (4 * math.pi * G * rr ** 2)
            rho_capr = fmax * (4 * math.pi / 3) * (2 * GM_SUN / rr) ** 1.5
            res[pl] = dict(dg_cap=dg_cap, ratio_to_bound=dg_cap / EPH[pl], rho_target_sun_numono=rho_tgt,
                           rho_cap=rho_capr, liouville_shortfall=rho_tgt / rho_capr)
        tide = abs(4 * math.pi * G * rho - 3 * G * Mc * boost / R0 ** 3)
        mono_sat = (4 * math.pi / 3) * G * rho * R_SAT
        mono_mars = (4 * math.pi / 3) * G * rho * R_MARS
        eps_g = rho * (4 * math.pi / 3) * AU ** 3 / MSUN
        q2_sig = abs(tide - Q2C) / Q2SIG
        ok = (res["Mars"]["ratio_to_bound"] <= 0.1 and res["Saturn"]["ratio_to_bound"] <= 0.1
              and tide <= Q2C + 2 * Q2SIG and q2_sig <= 2 and mono_sat <= 0.1 * EPH["Saturn"]
              and mono_mars <= 0.1 * EPH["Mars"] and eps_g <= GAMMA_BOUND)
        if boost == 1.0:
            R1_ok_all &= ok
        row[f"R1_boost{boost:g}"] = dict(fmax=fmax, sigma_kms=sig / 1e3, planets=res, MW_fluid_tide=tide,
                                         Q2_sigma=q2_sig, monopole_Saturn=mono_sat, monopole_Mars=mono_mars,
                                         gamma_contamination=eps_g, ok=ok)
        P(f"  {f:9s} R1 rho_host x{boost:g} = {rho * PC ** 3 / MSUN:.4f} Msun/pc^3, sigma {sig / 1e3:.0f} km/s: "
          f"Liouville-cap anomaly Mars {res['Mars']['dg_cap']:.2e} ({res['Mars']['ratio_to_bound']:.1e} of bound), "
          f"Saturn {res['Saturn']['dg_cap']:.2e} ({res['Saturn']['ratio_to_bound']:.1e}); "
          f"Sun-target/cap at Saturn {res['Saturn']['liouville_shortfall']:.1e}; MW-fluid tide {tide:.2e} s^-2 "
          f"({q2_sig:.2f} sigma from Q2 = 3e-27); monopole Saturn {mono_sat:.1e}; gamma contamination {eps_g:.1e}")
    # R2 / R3: the Sun owns its own settled target
    for pl, rr in [("Mars", R_MARS), ("Saturn", R_SAT)]:
        gNs = GM_SUN / rr ** 2
        for k in NU:
            dg = (float(NU[k](np.array(gNs / a0))) - 1) * gNs
            row[f"R{'2' if k == 'nu_mono' else '3'}_{k}_{pl}"] = dict(dg=dg, ratio=dg / EPH[pl])
    P(f"  {f:9s} R2 (nu_mono, Sun owns target): Mars {row['R2_nu_mono_Mars']['dg']:.2e} m/s^2 = "
      f"{row['R2_nu_mono_Mars']['ratio']:.0f}x bound, Saturn {row['R2_nu_mono_Saturn']['dg']:.2e} = "
      f"{row['R2_nu_mono_Saturn']['ratio']:.0f}x;  R3 (P2): Mars {row['R3_P2_Mars']['ratio']:.0f}x, Saturn "
      f"{row['R3_P2_Saturn']['ratio']:.0f}x")
    # Bondi radius for a collisional fluid streaming past the Sun at 230 km/s (reported)
    vrel = 230e3
    rB = 2 * GM_SUN / (vrel ** 2 + sig ** 2)
    row["bondi_radius_AU"] = rB / AU
    n1d[f] = row
P(f"  reported: Bondi-Hoyle capture radius of a collisional host fluid (v_rel 230 km/s): "
  f"{n1d['canonical']['bondi_radius_AU']:.3f} AU (inside 5.2 solar radii: captured fluid falls into the Sun)")
check("N1d R1 (embedded Sun): Liouville-capped anomaly <= 0.1 x bound at Mars and Saturn; MW-fluid tide within 2 sigma "
      "of Q2; MW-fluid monopole <= 0.1 x bound; gamma contamination <= 2.3e-5 (both footings, host x1)",
      R1_ok_all, "see rows above")
R2_fail = all(n1d[f]["R2_nu_mono_Saturn"]["ratio"] > 1 and n1d[f]["R2_nu_mono_Mars"]["ratio"] > 1 for f in FOOTS)
R3_fail = all(n1d[f]["R3_P2_Saturn"]["ratio"] > 1 and n1d[f]["R3_P2_Mars"]["ratio"] > 1 for f in FOOTS)
check("N1d R2/R3 (Sun owns a settled target) exceed the ephemeris bounds (pre-declared expectation: FAIL by >= 1e3)",
      R2_fail and R3_fail and min(n1d[f]["R2_nu_mono_Saturn"]["ratio"] for f in FOOTS) >= 1e3,
      f"min ratio nu_mono {min(min(n1d[f]['R2_nu_mono_Saturn']['ratio'], n1d[f]['R2_nu_mono_Mars']['ratio']) for f in FOOTS):.0f}, "
      f"P2 {min(min(n1d[f]['R3_P2_Saturn']['ratio'], n1d[f]['R3_P2_Mars']['ratio']) for f in FOOTS):.0f}",
      load_bearing=False)
NC1["N1d"] = n1d
G14_NC1 = "COND" if R1_ok_all else "FAIL"
P(f"  -> G14 for NC1 = {G14_NC1} (frozen rule: PASS needs phase-space-conserving settling shown for embedded systems; "
  f"NC1's settling is dissipative, so not shown)")

# N1e --------------------------------------------------------------------------------------------------------
P("\n[N1e] preferred-frame contamination by the fluid's mass (G6/G7)")
eps_ppn = max(n1d[f]["R1_boost1"]["gamma_contamination"] for f in FOOTS)
check("N1e fluid mass inside 1 AU / M_sun <= 1e-3 x the strict alpha2 bound (1.6e-12)", eps_ppn <= 1e-3 * ALPHA2_STRICT,
      f"{eps_ppn:.2e}")
NC1["N1e_eps"] = eps_ppn

# N1f --------------------------------------------------------------------------------------------------------
P("\n[N1f] realisability of the target with real mass (fluid-sector analog of G5; reported F-gate)")
SIG0 = 1.0 / (2.0 * math.pi)        # units: G = 1, M = 1, R_d = 1


def ring_g(a, R, z):
    s = (a + R) ** 2 + z * z
    m = 4.0 * a * R / s
    if m < 1e-4:
        K = 0.5 * math.pi * (1 + m / 4 + 9 * m * m / 64)
        dK = 0.5 * math.pi * (0.25 + 9 * m / 32)
    else:
        K = float(ellipk(m))
        E = float(ellipe(m))
        dK = (E - (1 - m) * K) / (2 * m * (1 - m))
    dmdR = (4 * a / s) * (1 - 2 * R * (a + R) / s)
    dmdz = -2 * z * m / s
    pre = -2.0 / math.pi
    dPdR = pre * (dK * dmdR / math.sqrt(s) - K * (a + R) * s ** -1.5)
    dPdz = pre * (dK * dmdz / math.sqrt(s) - K * z * s ** -1.5)
    return -dPdR, -dPdz


def disc_g(R, z, amax=40.0):
    w = lambda a: 2 * math.pi * a * SIG0 * math.exp(-a)
    pts = [R] if R < amax else None
    gR = quad(lambda a: w(a) * ring_g(a, R, z)[0], 0, amax, points=pts, limit=400, epsabs=1e-13, epsrel=1e-10)[0]
    gz = quad(lambda a: w(a) * ring_g(a, R, z)[1], 0, amax, points=pts, limit=400, epsabs=1e-13, epsrel=1e-10)[0]
    return gR, gz


def hankel_g(R, z):
    fR = lambda k: k * j1(k * R) * math.exp(-k * z) * (1 + k * k) ** -1.5
    fz = lambda k: k * j0(k * R) * math.exp(-k * z) * (1 + k * k) ** -1.5
    Kx = 60.0 / z
    return (-2 * math.pi * SIG0 * quad(fR, 0, Kx, limit=5000, epsabs=1e-13, epsrel=1e-10)[0],
            -2 * math.pi * SIG0 * quad(fz, 0, Kx, limit=5000, epsabs=1e-13, epsrel=1e-10)[0])


val = 0.0
for (Rv, zv) in [(1.0, 0.5), (3.0, 1.0), (0.5, 0.1), (5.0, 0.02)]:
    a_ = disc_g(Rv, zv)
    b_ = hankel_g(Rv, zv)
    val = max(val, abs(a_[0] - b_[0]) / abs(b_[0]), abs(a_[1] - b_[1]) / abs(b_[1]))
far = disc_g(0.0, 30.0)[1] / (-1.0 / 900.0)
check("N1f-v ring-integral disc field = Hankel form (4 points) and point-mass far field on the axis (z = 30 R_d)",
      val <= 1e-6 and abs(far - 1) <= 0.02, f"max rel diff {val:.1e}; far field / point mass {far:.4f}")


def freeman_gR(R):
    yv = R / 2.0
    V2 = 2.0 * yv * yv * (i0(yv) * k0(yv) - i1(yv) * k1(yv))      # 4 pi G Sigma0 R_d y^2 [...] with 4 pi Sigma0 = 2
    return -V2 / R


def build_grid(nR, nz):
    Rg = np.logspace(math.log10(0.05), math.log10(20.0), nR)
    zg = np.logspace(math.log10(0.02), math.log10(20.0), nz)
    gR = np.zeros((nR, nz))
    gz = np.zeros((nR, nz))
    for i, Rv in enumerate(Rg):
        for j, zv in enumerate(zg):
            gR[i, j], gz[i, j] = disc_g(Rv, zv)
    return Rg, zg, gR, gz


def eta_disc(Rg, zg, gR, gz, kernel, a0_dimless):
    gm = np.hypot(gR, gz)
    yv = gm / a0_dimless
    dy_dR, dy_dz = np.gradient(yv, Rg, zg, edge_order=2)
    rho = -(1.0 / (4 * math.pi)) * nu_prime(kernel, yv) * (dy_dR * gR + dy_dz * gz)
    RR = Rg[:, None]
    integrand_pos = 2 * math.pi * RR * np.where(rho > 0, rho, 0.0)
    integrand_neg = 2 * math.pi * RR * np.where(rho < 0, -rho, 0.0)
    Mpos = 2 * _trap(_trap(integrand_pos, zg, axis=1), Rg)
    Mneg = 2 * _trap(_trap(integrand_neg, zg, axis=1), Rg)
    Rs = np.logspace(math.log10(1e-3), math.log10(20.0), 4000)
    Sig = SIG0 * np.exp(-Rs)
    ypl = np.hypot([freeman_gR(r) for r in Rs], 2 * math.pi * Sig) / a0_dimless
    Msurf = _trap(2 * math.pi * Rs * (NU[kernel](ypl) - 1) * Sig, Rs)
    neg_cells = np.argwhere(rho < 0)
    region = None
    if len(neg_cells):
        region = dict(R_min=float(Rg[neg_cells[:, 0].min()]), R_max=float(Rg[neg_cells[:, 0].max()]),
                      z_min=float(zg[neg_cells[:, 1].min()]), z_max=float(zg[neg_cells[:, 1].max()]),
                      n_cells=int(len(neg_cells)), n_total=int(rho.size))
    return float(Mneg / (Mpos + Msurf)), float(Mpos), float(Mneg), float(Msurf), region


t_grid = time.time()
GRIDS = {"base": build_grid(64, 56), "dense": build_grid(96, 84)}
P(f"  disc fields built on 64x56 and 96x84 grids in {time.time() - t_grid:.1f} s (R in [0.05, 20], z in [0.02, 20] R_d; "
  f"slab z < 0.02 R_d excluded)")
DISCS = [(1e9, 1.0), (1e10, 2.0), (1e11, 3.5)]
n1f = {}
eta_max = 0.0
conv_ok = True
for f in FOOTS:
    for (Mb, Rd) in DISCS:
        a0_dimless = A0[f] * (Rd * KPC) ** 2 / (G * Mb * MSUN)
        for k in NU:
            e_b, Mp, Mn, Ms_, reg = eta_disc(*GRIDS["base"], k, a0_dimless)
            e_d = eta_disc(*GRIDS["dense"], k, a0_dimless)[0]
            conv = abs(e_d - e_b) <= 0.2 * max(e_b, e_d) + 1e-4
            key = f"{f}|{Mb:.0e}|{k}"
            n1f[key] = dict(eta=e_b, eta_dense=e_d, converged=conv, M_pos=Mp, M_neg=Mn, M_surface=Ms_,
                            neg_region=reg, a0_dimless=a0_dimless)
            if f == "canonical":
                eta_max = max(eta_max, e_b, e_d)
                conv_ok &= conv
            P(f"  {f:9s} M_b {Mb:.0e} R_d {Rd} kpc {k:8s}: eta = {e_b:.2e} (dense {e_d:.2e}, "
              f"{'converged' if conv else 'NOT CONVERGED'}); negative cells "
              f"{(reg['n_cells'] if reg else 0)}/{GRIDS['base'][2].size}"
              + (f" in R [{reg['R_min']:.2f}, {reg['R_max']:.2f}], z [{reg['z_min']:.3f}, {reg['z_max']:.3f}] R_d"
                 if reg else ""))
check("N1f realisability: eta = |M_neg|/(M_pos + M_surface) <= 0.01 (canonical, both kernels, three discs)",
      eta_max <= 0.01, f"max eta {eta_max:.2e}; converged {conv_ok}", load_bearing=False)
NC1["N1f"] = n1f
# POSITIVE CONTROL (added after run 1; reported, not frozen): the same detector on a configuration whose QUMOND phantom
# is known to go negative -- a point mass in a uniform external field (the saddle where the Newtonian field vanishes).
# Units G M = a0 = 1 (r_M = 1); g_e = 0.1 a0 along -z, saddle at z = -1/sqrt(g_e) on the axis.
pc = {}
for k in NU:
    ge = 0.1
    Rl = np.linspace(0.01, 8.0, 400)
    zl = np.linspace(-9.0, 5.0, 700)
    RRg, ZZg = np.meshgrid(Rl, zl, indexing="ij")
    rr3 = (RRg ** 2 + ZZg ** 2) ** 1.5
    gRp = -RRg / rr3
    gzp = -ZZg / rr3 - ge
    yp = np.hypot(gRp, gzp)
    dyR, dyz = np.gradient(yp, Rl, zl, edge_order=2)
    rhop = -(1.0 / (4 * math.pi)) * nu_prime(k, yp) * (dyR * gRp + dyz * gzp)
    mask = np.sqrt(RRg ** 2 + ZZg ** 2) > 0.3
    Mp_ = _trap(_trap(2 * math.pi * RRg * np.where((rhop > 0) & mask, rhop, 0.0), zl, axis=1), Rl)
    Mn_ = _trap(_trap(2 * math.pi * RRg * np.where((rhop < 0) & mask, -rhop, 0.0), zl, axis=1), Rl)
    negc = np.argwhere((rhop < 0) & mask)
    pc[k] = dict(eta=float(Mn_ / Mp_), n_neg=int(len(negc)),
                 z_range=[float(zl[negc[:, 1].min()]), float(zl[negc[:, 1].max()])] if len(negc) else None)
    P(f"  positive control ({k}): point mass + uniform field 0.1 a0: eta = {pc[k]['eta']:.3e}, negative cells "
      f"{pc[k]['n_neg']}" + (f" at z in [{pc[k]['z_range'][0]:.2f}, {pc[k]['z_range'][1]:.2f}] r_M (saddle at "
                             f"{-1 / math.sqrt(ge):.2f})" if pc[k]['z_range'] else ""))
check("N1f-pc (added after run 1) the detector finds the known negative phantom lobe near an external-field saddle",
      all(v["n_neg"] > 0 for v in pc.values()), f"eta P2 {pc['P2']['eta']:.2e}, nu_mono {pc['nu_mono']['eta']:.2e}",
      load_bearing=False)
NC1["N1f_positive_control"] = pc

# N1g --------------------------------------------------------------------------------------------------------
P("\n[N1g] Lagrangian forms of the own-acceleration rule (reading, argument only):")
P("  - foliation-invariant f(rho_c, A) of an irrotational fluid = a khronon dust: the BS24 class; N8 (BSX3 I1) closes it")
P("    by KiDS for ANY K (mu_eff^2 = k_J^2 (1 + c_ad^2)), and BSK1's inner instability applies.")
P("  - shift-symmetric f(X, box theta) of a superfluid phase: second derivatives of the phase, Ostrogradsky unless")
P("    degenerate; the FRIED_CHICKEN banner's dark_sector_honesty no-go (fourth order, ghost) is the record's instance;")
P("    a degenerate (DHOST-type) form is untested; doors 3/4/10 (CFG121/122/124) are the related record no-gos.")
P("  - so NC1 is scored only in its non-Lagrangian relaxation (dissipative) form; covariant relaxation-time")
P("    hydrodynamics/kinetics exists (LIT: Anderson-Witting; Israel-Stewart/BDNK causality), but a relaxation target")
P("    that contains grad A changes the principal part, so G1 for the full NC1 system is UNTESTED.")

# ==================================================================================================== NC2
P("\n" + "=" * 110)
P("NC2: khronon with alpha_c screened to 0 in strong fields (alpha_c a field-dependent function)")
P("=" * 110)
n2 = {}
for c2k in J467["table"]["G1"]["by_c2"]:
    A1 = parse_set(J467["table"]["G1"]["by_c2"][c2k]["A_str"])
    A12 = parse_set(J467["table"]["G12"]["by_c2"][c2k]["A_str"])
    A12L = parse_set(J467["table"]["G12"]["by_c2"][c2k]["A_len"])
    cap = intersect(A1, A12)
    capL = intersect(A1, A12L)
    n2[c2k] = dict(G1_str=fmt_set(A1), G12_str=fmt_set(A12), cap_strict=fmt_set(cap), cap_lenient=fmt_set(capL))
    P(f"  c2 = {c2k}: at the universal horizon alpha_c must lie in G1_str {fmt_set(A1)} AND G12_str {fmt_set(A12)}: "
      f"{fmt_set(cap)};  with G12 lenient: {fmt_set(capL)}")
NC2_strict_empty = all(v["cap_strict"] == "EMPTY" for v in n2.values())
check("N2 pointwise G1 (frozen-coefficient symbol) x G12 (UH) is EMPTY at every CFG467 c2 key (NC2 fails strictly)",
      NC2_strict_empty, "screening alpha_c -> 0 at the UH makes the khronon non-hyperbolic there; keeping alpha_c > 0 "
      "there fails reading S", load_bearing=False)
P("  -> NC2 FAILS at G12 under the strict reading; with reading W it reduces to row R03 plus >= 1 screening constant "
  "(dominated). If the screening zero is placed strictly behind the UH, the G1 failure is hidden: that is reading W's "
  "censorship argument again (LEN).")
OUT["NC2"] = n2

# ==================================================================================================== rows
P("\n" + "=" * 110)
P("SCORING (frozen rule): record rows R01-R25 + new classes NC1, NC2, NC3, NC5")
P("=" * 110)
S = REC.S
GR_G = {
    "G1": S("UNT", "gravity sector PASS (LIT-GR: Einstein + perfect fluid with 0 <= c_s^2 <= 1 strongly hyperbolic in "
                   "harmonic gauge; globally hyperbolic spacetimes have a time function, so criterion B holds with the "
                   "light cone); the fluid sector's relaxation rule reads grad A, which changes the principal part: not "
                   "computed"),
    "G2": S("PASS", "LIT-GR: constraints solvable by the CMC conformal method; maximal-slicing lapse equation elliptic "
                    "with nonnegative potential under the WEC; NC1's target needs no elliptic solve (local in A)"),
    "G3": S("NA", "F2a is the khronon scheme's lapse operator; there is no khronon"),
    "G4": S("PASS", "LIT-GR: no khronon vertex; the gravity EFT cutoff is M_P >> 1e3 x LHC; fluid microphysics is H3"),
    "G5": S("NA", "the lobe-health condition is the khronon's inertia in negative phantom lobes; no khronon. The fluid "
                  "analog (realisability) is N1f, reported separately"),
    "G6": S("PASS", f"LIT-GR alpha2 = 0; fluid contamination {eps_ppn:.1e} (N1e)"),
    "G7": S("PASS", f"LIT-GR alpha1 = 0; fluid contamination {eps_ppn:.1e} (N1e)"),
    "G8": S("PASS", "LIT-GR: no scalar charge, no dipole radiation; quadrupole formula"),
    "G9": S("PASS", "LIT-GR: G_cos = G_N; the fluid is CDM in FRW where the switch is OFF"),
    "G10": S("PASS", "LIT-GR: G_N = G"),
    "G11": S("PASS", "no small chassis coupling beyond Lambda (the cosmological-constant problem is shared by every row and "
                     "by LCDM; not a discriminating gate)"),
    "G12": S("PASS", "LIT-GR Kerr; K8 computed instance; fluid is test matter (N1a)"),
    "G13": S("PASS", "LIT-GR: gravitons and photons share one metric"),
    "G14": S(G14_NC1, "N1d: R1 (embedded Sun) passes on both footings (Liouville cap, MW-fluid tide and monopole, gamma); "
                      "R2/R3 (Sun owns a target) fail by >= 1e3; PASS would need the settling shown phase-space "
                      "conserving for embedded systems (NC1's is dissipative). Reported: the fluid's own A sees the Sun "
                      "only if the fluid is already at rest around it (EP); Bondi radius 0.02 AU"),
}
NC1_ROW = dict(
    id="NC1", name="NEW: GR + Lambda chassis, MOND only in the cold fluid (own-4-acceleration target, relaxation form)",
    sources="CFG484 N1a-N1g; CFG373 G1 (local target in the total field); CFG43 (fluid tie); CFG44 (closure); CFG478",
    G=GR_G,
    H={
        "H1": S("PASS", "fixed point = the law with the declared kernel (spherical exact, K3/N1b; non-spherical: the AQUAL "
                        "form of the same kernel, not QUMOND; the difference is untested)"),
        "H2": S("PASS", "N1b: the static fluid's own 4-acceleration is the total field; CFG373's inversion makes the target "
                        "local in it, zero constants, both kernels; no khronon needed"),
        "H3": S("UNT", "the decisive next test: a dissipative fluid microphysics that makes the rule an attractor, supplies "
                       "the support/temperature non-adiabatically from settling energy, and is well-posed (CFG44's "
                       "closure, CFG472 support, FRIED_CHICKEN row 10)"),
        "H4": S("COND", "fluid-sector first-order switch: CFG478 legal (LMP/van der Waals double tangent), CFG482 two-valued "
                        "SED PASS in PM runs; non-relativistic, ownership mapping open"),
        "H5": S("PASS", "the rule reads the fluid's own 4-acceleration, never the baryons: no reciprocity reaction, no "
                        "direct coupling; the fluid is the record's cold fluid, no species"),
        "H6": S("PASS", "CFG43 existence result (tie written into the fluid sector, Lambda global, a0 flat) and the XR20 T1 "
                        "form; kappa chosen"),
    },
    constants=dict(n=0, names="0 in the chassis; fluid sector: settling rate (CFG464: the zero-constant t_dyn rate is "
                              "not excluded), switch constants open", counted_on_record=False))

NC2_ROW = dict(
    id="NC2", name="NEW: khronon with alpha_c screened to 0 in strong fields",
    sources="CFG484 N2 on CFG467's committed sets",
    G=dict(REC._CHK_G, G12=S("FAIL", "N2: alpha_c at the UH must be in G1_str (0, 0.5) U (0.5, 2) and in G12_str {0}: "
                                     "EMPTY at every c2")),
    H=REC._CHK_H,
    constants=dict(n=4, names="alpha_c, c_2, xi + >= 1 screening scale", counted_on_record=False))

NC3_ROW = dict(
    id="NC3", name="NEW (argument): invertible disformal / two-time-scale redefinition of the khronon chassis",
    sources="argument: physical gate outcomes are invariant under invertible field redefinitions applied to the whole "
            "action including the matter coupling (Foster-type; LIT, memory-level); a non-invertible map is mimetic "
            "(CFG124)",
    G=dict(REC._CHK_G, G12=S("FAIL", "inherits R01 by redefinition invariance (ARG)")),
    H=REC._CHK_H,
    constants=dict(n=None, names="disformal coefficients", counted_on_record=False))

NC5_ROW = dict(
    id="NC5", name="NEW (argument): Einstein-aether, aether not hypersurface-orthogonal",
    sources="argument against the 09-26 user decision (criterion B)",
    G=dict({g: S("UNT", "not computed") for g in GG},
           G1=S("FAIL", "criterion B requires a global preferred time; a twisting aether defines no foliation (ARG); "
                        "in spherical symmetry it reduces to the khronon (R01)")),
    H={h: S("UNT", "not computed") for h in HH},
    constants=dict(n=None, names="c_1..c_4", counted_on_record=False))

ROWS = []
for r in REC.ROWS:
    r = dict(r)
    if r["G"] == "GR_CHASSIS":
        r["G"] = dict(GR_G, G1=S("UNT", "gravity sector PASS (LIT-GR); no fluid dynamics specified on the record"),
                      G14=S(G14_NC1, "same GR chassis as NC1: N1d R1 (embedded Sun) passes, R2/R3 (Sun owns a target) "
                                     "fail; which applies depends on fluid dynamics the record does not specify"))
    ROWS.append(r)
ROWS += [NC1_ROW, NC2_ROW, NC3_ROW, NC5_ROW]

for r in ROWS:
    r["class"] = classify(r)
    r["rank_key"] = rank_key(r)

ranked = sorted(ROWS, key=lambda r: r["rank_key"])
P(f"\n{'row':4s} {'class':14s} {'G: FAIL LEN UNT/COND':22s} {'H: FAIL LEN UNT/COND':22s} {'const':6s}  name")
for r in ranked:
    kk = r["rank_key"]
    P(f"{r['id']:4s} {r['class']:14s} {kk[0]:4d} {kk[1]:3d} {kk[2]:4d}            {kk[3]:4d} {kk[4]:3d} {kk[5]:4d}"
      f"            {('-' if r['constants']['n'] is None else r['constants']['n'])!s:6s} {r['name']}")

P("\nper-row gate detail (FAIL / LEN / COND / UNT listed; PASS and NA omitted; identical notes grouped):")
for r in ROWS:
    bad = [(k, (r["G"].get(k) or r["H"].get(k))) for k in GG + HH if (r["G"].get(k) or r["H"].get(k))[0]
           not in PASSLIKE]
    P(f"  {r['id']} {r['name']}  [{r['class']}]")
    groups = {}
    for k, (code, note) in bad:
        groups.setdefault((code, note), []).append(k)
    for (code, note), ks in groups.items():
        P(f"      {','.join(ks):12s} {code:4s} {note}")

top = ranked[0]
second = ranked[1]
tie_on_gates = top["rank_key"][:6] == second["rank_key"][:6]
works = [r["id"] for r in ROWS if r["class"] == "WORKS"]
clean = [r["id"] for r in ROWS if r["class"] == "CHASSIS-CLEAN"]
verdict = "FOUND" if works else ("CHASSIS ONLY" if clean else "NONE")
P("\n" + "=" * 110)
P(f"TOP CANDIDATE (frozen ranking): {top['id']} -- {top['name']}  [{top['class']}]")
P(f"  runner-up: {second['id']} -- {second['name']}  [{second['class']}]"
  + ("   (tied with the top on every gate count; separated only by the constant count)" if tie_on_gates else ""))
P(f"  open items of the top candidate: " + ", ".join(
    f"{k} {(top['G'].get(k) or top['H'].get(k))[0]}" for k in GG + HH
    if (top['G'].get(k) or top['H'].get(k))[0] not in PASSLIKE))
P(f"LANE VERDICT: {verdict}  (WORKS: {works or 'none'}; CHASSIS-CLEAN: {clean or 'none'})")
P("=" * 110)

# ==================================================================================================== MUTATE
mutate_rows = {}
if MUT:
    P("\n[MUTATE] harness on known-failing completions fed as the candidate under test")
    byid = {r["id"]: r for r in ROWS}
    NC1_R2 = dict(NC1_ROW, id="NC1-R2", name="NC1 with G14 scored by reading R2 (Sun owns its target)",
                  G=dict(GR_G, G14=S("FAIL", "N1d R2: nu_mono anomaly at Mars/Saturn exceeds the ephemeris bounds by "
                                            f"{min(n1d[f]['R2_nu_mono_Saturn']['ratio'] for f in FOOTS):.0f}x or more")))
    NC1_R2["class"] = classify(NC1_R2)
    cases = [("M1", byid["R01"], "G12"), ("M2", byid["R08"], "G7"), ("M3", byid["R18"], "G14"), ("M4", NC1_R2, "G14")]
    bites = True
    for mid, row, gate in cases:
        cl = classify(row)
        fails = gates_with(row, "FAIL", GG)
        ok = cl == "FAILS" and gate in fails
        bites &= ok
        mutate_rows[mid] = dict(row=row["id"], cls=cl, fail_gates=fails, recorded_gate=gate, ok=ok)
        check(f"{mid} {row['id']} fails at its recorded gate {gate}", ok, f"class {cl}; FAIL gates {fails}")
    cand = cases[0][1]
    check("MUTATE final: the candidate under test WORKS", classify(cand) == "WORKS",
          f"{cand['id']} class {classify(cand)} (must fail: the harness bites)")
    OUT["mutate_response"] = dict(cases=mutate_rows, harness_bites=bites)

# ==================================================================================================== output
OUT["checks"] = CHECKS
OUT["NC1"] = NC1
OUT["rows"] = [dict(id=r["id"], name=r["name"], sources=r["sources"], cls=r["class"], rank_key=list(r["rank_key"]),
                    constants=r["constants"], G={k: list(v) for k, v in r["G"].items()},
                    H={k: list(v) for k, v in r["H"].items()}) for r in ROWS]
OUT["ranking"] = [r["id"] for r in ranked]
OUT["top_candidate"] = dict(id=top["id"], name=top["name"], cls=top["class"], tie_with_runner_up_on_gates=tie_on_gates,
                            runner_up=second["id"])
OUT["verdict"] = verdict
lb_fail = [k for k, v in CHECKS.items() if v["load_bearing"] and not v["ok"]]
OUT["n_checks"] = len(CHECKS)
OUT["n_pass"] = sum(v["ok"] for v in CHECKS.values())
OUT["load_bearing_failures"] = lb_fail
OUT["runtime_s"] = round(time.time() - T0, 1)
P(f"\nchecks: {OUT['n_pass']}/{OUT['n_checks']} pass; load-bearing failures: {lb_fail or 'none'}; "
  f"runtime {OUT['runtime_s']} s")
rc = 1 if lb_fail else 0
P(f"exit code {rc}" + ("  (MUTATE: rc 1 is the required response)" if MUT else ""))


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, float) and (math.isinf(o) or math.isnan(o)):
        return str(o)
    return o


json.dump(_clean(OUT), open(os.path.join(HERE, f"cfg484_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg484_chassis_search{TAG}.out"), "w").write("\n".join(LINES) + "\n")
sys.exit(rc)
