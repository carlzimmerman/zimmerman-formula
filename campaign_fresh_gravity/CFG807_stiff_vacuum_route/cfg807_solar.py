"""CFG807 script 1: solar-system objections to the PAPER42 vacuum route, inside the stiffened action (S2).

Criteria: FROZEN_CRITERIA.md (committed alone first). Checks S1 (Cassini Q2 with a k = 2 phantom turn-off in the
Galactic background response), S2 (extreme-TNO apsidal precession from the stiff action's anomaly vs the giant planets),
S3 reported (turn-off radius, the Sun's response amplitude).

The Q2 / anomaly machinery is COPIED from campaign_fresh_gravity/CFG770_cassini_stiff_action/cfg770.py (functions mfun,
defic, J, Q2, a_anom; same quadratures), not imported (that script writes its own outputs on import). Only the background
response (A_par, A_perp) is changed: it is computed from the law with the turn-off.

Run:  nice python3 cfg807_solar.py           (seconds)
      CFG807_MUTATE=M1 nice python3 cfg807_solar.py   (stiffness off: unscreened phantom; S2 must FAIL)
"""
import json
import math
import os
import sys

import numpy as np
from scipy import integrate, optimize

MODE = os.environ.get("CFG807_MUTATE", "")
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = f"_MUTATE_{MODE}" if MODE else ""
OUTF = open(os.path.join(HERE, f"cfg807_solar{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUTF.write(s + "\n")


G = 6.67430e-11
GM = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
YR = 3.15576e7
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GE = [2.00e-10, 2.32e-10, 2.64e-10]
Q2_CEIL = 5.2e-27
LSTAR = 5.75 * PC
LAM = LSTAR / math.sqrt(2)          # CFG770 K1: L*^2 = 2 Lambda^2
YTS = [None, 32.0, 64.0, 128.915, 1000.0]
RES = {"lane": "CFG807", "script": "solar", "mutate": MODE, "checks": {}, "numbers": {}}
FAILS = []


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- the law with a turn-off (phantom u vs g_N)
def u_law(gN, a0):
    y = gN / a0
    return a0 * 0.5 * (-y + math.sqrt(y * y + 4 * y))     # simple mu: u^2 = g_N (a0 - u)


def u_t(gN, a0, yt):
    u = u_law(gN, a0)
    return u if yt is None else u / (1 + (gN / (yt * a0)) ** 2)


def background(ge, a0, yt):
    gN = optimize.brentq(lambda x: x + u_t(x, a0, yt) - ge, 1e-6 * ge, ge, xtol=1e-30, rtol=1e-15)
    u = u_t(gN, a0, yt)
    h = 1e-6 * gN
    dudg = (u_t(gN + h, a0, yt) - u_t(gN - h, a0, yt)) / (2 * h)
    return dict(gNe=gN, ue=u, Apar=1.0 / dudg, Aperp=gN / u)


# ---------------------------------------------------------------- copied from CFG770 (unchanged)
XC, WC = np.polynomial.legendre.leggauss(96)
P2C = 0.5 * (3 * XC ** 2 - 1)


def defic(kap, Apar, Aperp):
    return XC ** 2 / (Apar + 1 + kap ** 2) + (1 - XC ** 2) / (Aperp + 1 + kap ** 2)


def J(kap, Apar, Aperp):
    d = defic(kap, Apar, Aperp)
    d0 = 1.0 / (Aperp + 1 + kap ** 2)
    return float(np.sum(WC * P2C * (d / (1 - d) - d0 / (1 - d0))))


def Q2(Lam, Apar, Aperp):
    f = lambda t: (math.exp(t) ** 3) * J(math.exp(t), Apar, Aperp)
    val = 0.0
    for lo, hi in [(-12, -4), (-4, 0), (0, 4), (4, 12)]:
        val += integrate.quad(f, lo, hi, limit=400, epsabs=0, epsrel=1e-11)[0]
    return GM / (math.pi * Lam ** 3) * val


def a_anom(r, Lam, Apar, Aperp):
    lead = -GM / (2 * Lam ** 2)
    x0 = r / Lam

    def j1(x):
        return (math.sin(x) / x - math.cos(x)) / x if x > 1e-4 else x / 3 - x ** 3 / 30

    def g(t):
        kap = math.exp(t)
        d = defic(kap, Apar, Aperp)
        rem = float(0.5 * np.sum(WC * (d / (1 - d) - 1 / kap ** 2)))
        return kap * kap * j1(kap * x0) * rem

    val = 0.0
    for lo, hi in [(-14, -6), (-6, -2), (-2, 2), (2, 6), (6, 9)]:
        val += integrate.quad(g, lo, hi, limit=600, epsabs=1e-30, epsrel=1e-10)[0]
    return lead - (2 * GM / math.pi) * val / Lam ** 2


# ================================================================ S1 Cassini with the turn-off
P("CFG807 script 1: solar-system objections to the vacuum route in the stiffened action" + (f"  [MUTATE {MODE}]" if MODE else ""))
P(f"\nS1  Cassini Q2 at L* = 5.75 pc, background response from the law with a k = 2 phantom turn-off (ceiling {Q2_CEIL:.1e})")
s1 = {}
for yt in YTS:
    for f, a0 in A0.items():
        for ge in GE:
            b = background(ge, a0, yt)
            q = Q2(LAM, b["Apar"], b["Aperp"])
            s1[f"yt={yt}|{f}|{ge:.2e}"] = dict(Q2=q, ratio=abs(q) / Q2_CEIL, **b)
    worst = max(v["ratio"] for k, v in s1.items() if k.startswith(f"yt={yt}|"))
    P(f"  y_t = {str(yt):8s}: worst |Q2|/ceiling = {worst:.3e}")
base = s1[f"yt=None|canonical|{GE[1]:.2e}"]
P(f"  (no turn-off, canonical, g_e 2.32e-10: Q2 = {base['Q2']:+.3e}; CFG770 reported -1.1 to -1.8e-32)")
w1 = max(v["ratio"] for v in s1.values())
check("S1 Cassini Q2 < ceiling for every y_t", w1 < 1, f"worst |Q2|/ceiling {w1:.3e}")
dmax = max(abs(s1[f"yt={yt}|{f}|{ge:.2e}"]["Q2"] / s1[f"yt=None|{f}|{ge:.2e}"]["Q2"] - 1)
           for yt in YTS[1:] for f in A0 for ge in GE)
P(f"  largest fractional change of Q2 from any turn-off: {dmax:.3e}")
RES["numbers"]["S1"] = s1
RES["numbers"]["S1_max_frac_change_from_turnoff"] = dmax

# ================================================================ S2 extreme TNOs
P("\nS2  extreme-TNO apsidal precession from the stiff action's anomaly (canonical, g_e 2.32e-10)")
a0c = A0["canonical"]
b = background(GE[1], a0c, None)
rgrid = np.logspace(math.log10(10 * AU), math.log10(2e5 * AU), 45)
if MODE == "M1":
    # stiffness off: the Sun's unscreened phantom (EFE neglected, as p56's exact-law control); sunward = negative
    agrid = np.array([-u_law(GM / r ** 2, a0c) for r in rgrid])
else:
    agrid = np.array([a_anom(r, LAM, b["Apar"], b["Aperp"]) for r in rgrid])
lr = np.log(rgrid)
A = lambda r: float(np.interp(math.log(r), lr, agrid))
for rr in [30, 100, 300, 1000, 3000, 10000]:
    P(f"  anomaly at {rr:6d} AU: {A(rr * AU):+.4e} m/s^2")
RES["numbers"]["S2_anomaly_grid"] = dict(r_AU=(rgrid / AU).tolist(), a=agrid.tolist())

path = os.path.join(HERE, "../../../_external_data/etno_sbdb/etno_a150_q30.json")
d = json.load(open(path))
rows = [dict(zip(d["fields"], r)) for r in d["data"]]
P(f"  data: {len(rows)} objects (SBDB a > 150 AU, q > 30 AU; data_assembly/etno_sbdb/FETCH_LOG.md)")


def rates(o):
    a, e, inc = float(o["a"]) * AU, float(o["e"]), math.radians(float(o["i"]))
    n = math.sqrt(GM / a ** 3)
    Ms = np.linspace(0, 2 * np.pi, 2001)[:-1]
    E = Ms.copy()
    for _ in range(60):
        E = E - (E - e * np.sin(E) - Ms) / (1 - e * np.cos(E))
    f = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    r = a * (1 - e * np.cos(E))
    acc = np.mean([A(ri) for ri in r] * np.cos(f))
    wdot = math.sqrt(1 - e ** 2) / (n * a * e) * acc
    planets = [(1 / 1047.35, 5.2), (1 / 3497.9, 9.54), (1 / 22902.9, 19.19), (1 / 19412.2, 30.07)]
    J2R2 = 0.5 * sum(m * (aa * AU) ** 2 for m, aa in planets)
    wpl = 0.75 * n * J2R2 / (a ** 2 * (1 - e ** 2) ** 2) * (5 * math.cos(inc) ** 2 - 1)
    return wdot, wpl


tab = []
for o in rows:
    w, wp = rates(o)
    tab.append(dict(name=o["full_name"].strip(), a=float(o["a"]), ratio=abs(w / wp),
                    T_anom_Gyr=2 * math.pi / abs(w) / YR / 1e9 if w else float("inf")))
tab.sort(key=lambda t: -t["ratio"])
nfast = sum(t["ratio"] > 1 for t in tab)
nslow = sum(t["T_anom_Gyr"] > 4.5 for t in tab)
P(f"  objects where the anomaly precesses faster than the planets: {nfast}/90 (p56 turn-off y_t = 128.9: 43/90)")
P(f"  objects with anomaly apsidal period > 4.5 Gyr: {nslow}/90")
for t in tab[:5]:
    P(f"    {t['name']:34s} a = {t['a']:8.1f} AU: |w_anom/w_pl| = {t['ratio']:.3e}, anomaly period {t['T_anom_Gyr']:.3g} Gyr")
sed = [t for t in tab if "Sedna" in t["name"]][0]
P(f"    Sedna: |w_anom/w_pl| = {sed['ratio']:.3e}, anomaly period {sed['T_anom_Gyr']:.3g} Gyr (p56 turn-off: 0.02 Gyr)")
check("S2 TNO: |w_anom/w_pl| < 0.1 for all 90 and anomaly period > 4.5 Gyr for >= 80/90",
      max(t["ratio"] for t in tab) < 0.1 and nslow >= 80,
      f"max ratio {max(t['ratio'] for t in tab):.3e}; {nslow}/90 slower than 4.5 Gyr")
RES["numbers"]["S2"] = dict(nfast=nfast, nslow=nslow, top=tab[:10], sedna=sed)
# POST-HOC (declared after the first run; does NOT change S2's frozen verdict): at a ~ 1e4 AU the giant-planet
# quadrupole is itself negligible, so the frozen ratio-to-planets test is mis-specified there. Report the anomaly
# against the Galactic vertical tide, the dominant secular driver at large a (timescale ~ n / (4 pi G rho_0),
# rho_0 = 0.1 Msun/pc^3).
rho0 = 0.1 * 1.98847e30 / PC ** 3
P("  POST-HOC (after the first run; S2 verdict unchanged): anomaly vs Galactic vertical tide, rho_0 = 0.1 Msun/pc^3")
worst_tide = 0.0
for o in rows:
    a = float(o["a"]) * AU
    n = math.sqrt(GM / a ** 3)
    w_tide = 2 * math.pi / (n / (4 * math.pi * G * rho0))          # 1/s, order of magnitude
    w, wp = rates(o)
    rt = abs(w) / max(abs(wp), w_tide)
    if rt > worst_tide:
        worst_tide, wn = rt, o["full_name"].strip()
P(f"    largest |w_anom| / max(|w_planets|, w_tide) over 90 objects = {worst_tide:.3e} ({wn})")
mq = [t for t in tab if "2020 MQ53" in t["name"]][0]
aM = mq["a"] * AU
P(f"    2020 MQ53: tide timescale {math.sqrt(GM / aM ** 3) / (4 * math.pi * G * rho0) / YR / 1e9:.3g} Gyr vs anomaly period {mq['T_anom_Gyr']:.3g} Gyr")
RES["numbers"]["S2_posthoc_tide"] = dict(worst_ratio=worst_tide, name=wn)

# ================================================================ S3 reported
P("\nS3  (reported) turn-off radius vs stiffness; the Sun's response amplitude")
for yt in YTS[1:]:
    rt = math.sqrt(GM / (yt * a0c))
    P(f"  y_t = {yt:8.1f}: r_t = {rt / AU:7.0f} AU = {rt / PC:.4f} pc = {rt / LSTAR:.2e} L*")
usun = abs(A(1000 * AU))
P(f"  the Sun's stiff response |u| at 1000 AU = {usun:.3e} m/s^2 = {usun / a0c:.2e} a0 (GM/L*^2 = {GM / LSTAR ** 2:.3e})")
P("  The turn-off acts on the phantom at y ~ y_t >> 1; the Sun's own P response is the linear critical (stiff) one,")
P("  u << a0 everywhere inside L*, so the turn-off cannot change it (only the Galactic background's A_par/A_perp, S1).")
RES["numbers"]["S3"] = dict(usun_1000AU=usun, ratio_a0=usun / a0c)

if MODE == "M1":
    bite = any(n.startswith("S2") for n in FAILS)
    P(f"\nM1 tooth (stiffness off -> S2 must FAIL): {'bites' if bite else 'DID NOT BITE'}")
    if not bite:
        FAILS.append("M1 tooth did not bite")
RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"cfg807_solar_results{SUF}.json"), "w"), indent=1, default=str)
P("\nFAILS:", FAILS if FAILS else "none")
OUTF.close()
sys.exit(1 if FAILS else 0)
