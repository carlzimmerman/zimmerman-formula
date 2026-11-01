#!/usr/bin/env python3
"""TD1_threshold_derivation: three a0-free attempts on the switch threshold T. FROZEN_CRITERIA.md committed alone first (7f011a08bc).

kappa = 1/2 FITTED, unused; cold dark energy = gravitating field component, never a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I td1_threshold.py      (TD1_MUTATE=1 twin)
"""
import os, sys, io, json, math, contextlib, resource
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import brentq
from scipy.special import erfc
from scipy.integrate import quad

MUT = os.environ.get("TD1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
OUT = open(os.path.join(HERE, f"td1_threshold{TAG}.out"), "w")
RES = {"lane": "TD1_threshold_derivation", "criteria": "7f011a08bc", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED, unused; cold dark energy = gravitating field component, never a particle; not theory closed"}
W = (12.19, 12.39)
GYR_PER_MPC_C = 3.2615637769e-3          # Mpc / c in Gyr
G, MSUN, MPC, C = 6.67430e-11, 1.98847e30, 3.0856775814913673e22, 299792458.0


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


P("TD1_threshold_derivation" + (" [MUTATE: turnaround at eta = pi/2 - control output]" if MUT else "") +
  ": criteria 7f011a08bc; kappa = 1/2 FITTED, unused; not theory closed")

# ---------------- exact EdS spherical collapse: R = A (1 - cos eta), t = B (eta - sin eta) ----------------
def dlin(eta):
    return 0.6 * (0.75 * (eta - math.sin(eta))) ** (2 / 3)


ETA_TA = math.pi / 2 if MUT else math.pi
D_TA, D_C = dlin(ETA_TA), dlin(2 * math.pi)
check("K3", abs(D_TA - 1.0624) <= 0.001 and abs(D_C - 1.6865) <= 0.001, f"delta_ta {D_TA:.5f}, delta_c {D_C:.5f}", "1.0624, 1.6865 within 0.001")

# ---------------- record backgrounds (EM1's CLASS, as DT1) ----------------
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- halo profiles")], EM1SRC, "exec"), NE)
sys.argv = argv0
DC_REC, OMEGA = 1.686, 0.974
BG = {}
for tag, bg in NE["BGS"].items():
    cc = bg["c"]; h = bg["h"]; Om = float(cc.Omega_m())
    zg = np.linspace(0, 30, 3001); Dg = np.array([cc.scale_independent_growth_factor(z) for z in zg]); Dg /= Dg[0]
    lMg = np.linspace(7.0, 16.5, 191); sigf = bg["cB"].__defaults__[1]
    sg = np.array([float(sigf(10 ** l)[0]) for l in lMg])
    zt = np.linspace(0, 12, 2401); Ht = np.array([cc.Hubble(z) for z in zt])      # 1/Mpc
    lb = np.concatenate([[0.0], np.cumsum(0.5 * (1 / ((1 + zt[1:]) * Ht[1:]) + 1 / ((1 + zt[:-1]) * Ht[:-1])) * np.diff(zt))]) * GYR_PER_MPC_C
    age = float(cc.age())
    BG[tag] = dict(h=h, Om=Om, zg=zg, Dg=Dg, lMg=lMg, sg=sg, s2=sg ** 2, zt=zt, lb=lb, age=age, s8=bg["s8"], sigf=sigf, rhom=Om * 2.775e11 * h ** 2,
                   OL=float(1 - Om))


def sig(tag, l):
    e = BG[tag]; return float(np.interp(l, e["lMg"], e["sg"]))


def z_of_D(tag, D):
    e = BG[tag]; return float(np.interp(-D, -e["Dg"], e["zg"]))


def lookback(tag, z):
    e = BG[tag]; return float(np.interp(z, e["zt"], e["lb"]))


def root(fun, lo=7.5, hi=16.0):
    xs = np.linspace(lo, hi, 400); v = [fun(x) for x in xs]
    for i in range(len(xs) - 1):
        if np.isfinite(v[i]) and np.isfinite(v[i + 1]) and np.sign(v[i]) != np.sign(v[i + 1]):
            return float(brentq(fun, xs[i], xs[i + 1], xtol=1e-6))
    return None


def zform(tag, M):
    e = BG[tag]; s2i = lambda l: float(np.interp(l, e["lMg"], e["s2"]))
    S = math.sqrt(max(s2i(math.log10(M / 2)) - s2i(math.log10(M)), 0.0)); Df = DC_REC / (DC_REC + OMEGA * S)
    return float(np.interp(-Df, -e["Dg"], e["zg"])) if Df < 1 else 0.0


A = "A_c2b_refit"; B = "B_cfg886_bg"
k1 = abs(zform(A, 1e12) - 0.944) <= 0.005 and abs(zform(A, 10 ** 12.3) - 0.886) <= 0.005
check("K1", k1, f"z_f(1e12) {zform(A, 1e12):.3f}, z_f(1e12.3) {zform(A, 10 ** 12.3):.3f}", "DT1 0.944, 0.886 within 0.005")
M8 = {t: 4 / 3 * math.pi * (8 / BG[t]["h"]) ** 3 * BG[t]["rhom"] for t in BG}
s8r = {t: sig(t, math.log10(M8[t])) for t in BG}
check("K2", all(abs(s8r[t] - BG[t]["s8"]) <= 0.01 for t in BG), "; ".join(f"{t} {s8r[t]:.4f} vs {BG[t]['s8']:.4f}" for t in BG), "within 0.01")


def grade_primary(lt, spread):
    if spread > 0.20: return "CHOICE-DEPENDENT"
    return "LANDS" if (lt is not None and W[0] <= lt <= W[1]) else "MISS"


# ---------------- A1: turned-around mass ----------------
P("\n== A1 turned-around mass: sigma(M, z=0) = delta")
A1 = {}
for t in (A, B):
    mta = root(lambda l: sig(t, l) - D_TA)
    mst = root(lambda l: sig(t, l) - D_C)
    mta_low = root(lambda l: sig(t, l) - D_TA * 0.993)
    S = lambda l: sig(t, l) ** 2
    fcoll = float(erfc((D_C - D_TA) / math.sqrt(2 * (S(9.0) - S(mta)))))
    A1[t] = dict(M_ta=mta, M_star=mst, M_ta_low_Om=mta_low, f_coll=fcoll, M_ta_fcoll=mta + math.log10(fcoll))
    P(f"  {t}: A1 M_ta {mta:.3f}; A1b M* {mst:.3f}; A1c M_ta f_coll {A1[t]['M_ta_fcoll']:.3f} (f_coll {fcoll:.3f}); delta_ta x 0.993 {mta_low:.3f}")
sp1 = max(abs(A1[A]["M_ta"] - A1[B]["M_ta"]), abs(A1[A]["M_ta"] - A1[A]["M_ta_low_Om"]))
lab1 = grade_primary(A1[A]["M_ta"], sp1)
P(f"  primary {A1[A]['M_ta']:.3f}, miss from W {A1[A]['M_ta'] - W[1]:+.3f} above upper edge; input spread {sp1:.3f}; label {lab1}")
P(f"  reported, never deciding: A1b in W? {W[0] <= A1[A]['M_star'] <= W[1]}; A1c in W? {W[0] <= A1[A]['M_ta_fcoll'] <= W[1]}")
RES["A1"] = dict(rows=A1, spread=sp1, label=lab1)

# ---------------- A2: Astra's clock on basins ----------------
P("\n== A2 CFG763's clock: turned around at least tau ago, D(z_ta) = delta_ta / sigma(M), lookback(z_ta) = tau")
TAUS = (0.72, 1.20, 3.47)
A2 = {}
for t in (A, B):
    A2[t] = {}
    for tau in TAUS:
        def fun(l):
            D = D_TA / sig(t, l)
            if D >= 1: return -tau
            return lookback(t, z_of_D(t, D)) - tau
        A2[t][str(tau)] = root(fun)
    P(f"  {t}: " + ", ".join(f"tau {x} Gyr -> {A2[t][str(x)]:.3f}" for x in TAUS))
vals = [A2[t][str(x)] for t in (A, B) for x in TAUS]
sp2 = max(vals) - min(vals)
pr2 = A2[A]["1.2"]
lab2 = grade_primary(pr2, sp2)
P(f"  primary (1.20 Gyr) {pr2:.3f}; input spread {sp2:.3f}; label {lab2}")
RES["A2"] = dict(rows=A2, spread=sp2, primary=pr2, label=lab2)

# ---------------- A3: the action with its posits removed ----------------
P("\n== A3 L = -1/2 (grad chi)^2 - 1/2 xi theta chi^2 - 1/4 lambda chi^4, exact EdS top hat")
# theta = 3 Rdot / R = 3 sin(eta) / (B (1 - cos eta)^2), dt = B (1 - cos eta) d eta, t_coll = 2 pi B, so
# N = int sqrt(xi |theta|) dt = sqrt(3 xi B) I = sqrt(3 xi t_coll / 2 pi) I, I = int_pi^2pi sqrt(|sin eta|) d eta
I1 = quad(lambda e: math.sqrt(abs(math.sin(e))), math.pi, 2 * math.pi, limit=400)[0]
gr = np.linspace(math.pi, 2 * math.pi, 400001)
I2 = float(np.trapz(np.sqrt(np.abs(np.sin(gr))), gr))
check("K4", abs(I1 - I2) <= 1e-4, f"I quad {I1:.6f}, grid {I2:.6f}", "within 1e-4")
P(f"  (a) N = sqrt(3 xi t_coll / 2 pi) I, I = {I1:.5f}. No M in the integral: M enters only through t_coll.")
e = BG[A]
HL = math.sqrt(e["OL"]) * 100 * e["h"] * 1e3 / MPC * 3.15576e16        # 1/Gyr, sqrt(8 pi G rho_DE / 3)
rows = {}
for l in (11.0, 11.5, 12.0, 12.19, 12.3, 12.39, 12.5, 12.8):
    s = sig(A, l); Dc = D_C / s
    if Dc >= 1:
        rows[str(l)] = dict(sigma=s, t_coll=None, N=None); continue
    tc = e["age"] - lookback(A, z_of_D(A, Dc))
    rows[str(l)] = dict(sigma=s, t_coll=tc, N=math.sqrt(3 * HL * tc / (2 * math.pi)) * I1)
    P(f"  lg M {l:5.2f}: sigma {s:.3f}, t_coll {tc:6.2f} Gyr, N at xi = H_Lambda {rows[str(l)]['N']:.3f}")
Ns = [rows[k]["N"] for k in ("12.19", "12.39") if rows[k]["N"] is not None]
P(f"  sign: later-collapsing, more massive systems have larger N, so a threshold N0 selects HIGH mass: right direction.")
P(f"  (b) numbers: xi, seed chi_0/chi_c (N0 = ln of it), lambda. rho_DE can fix xi's scale at most (H_Lambda = {HL:.4f} /Gyr). Seed stays free.")
P(f"      W needs N0 in {min(Ns):.3f} to {max(Ns):.3f} at xi = H_Lambda: growth of about e^{np.mean(Ns):.2f} = x{math.exp(np.mean(Ns)):.2f}, width {max(Ns) - min(Ns):.3f}. A seed tuned to within {100 * (math.exp(max(Ns) - min(Ns)) - 1):.1f} %.")
P("  (c) after virialisation <theta> = 0, so the tachyonic mass goes to zero; with lambda chi^4 alone the field redshifts as w = 1/3 until it dilutes. Not w = 0, so requirement R5 isn't met without a separate mass term, itself a new number.")
HM = C ** 3 / (G * math.sqrt(e["OL"]) * 100 * e["h"] * 1e3 / MPC) / MSUN
P(f"  (d) Newtonian pressureless collapse carries no c, and G with H(t) makes no mass, so the only scale is P(k)'s, through sigma(M, z) = number. With c: Hubble mass c^3/(G H_Lambda), lg {math.log10(HM):.2f}, about {math.log10(HM) - 12.3:.1f} dex away. With hbar, baryon rates or a0 other scales exist; those are outside this attempt.")
lk = "NO LINK"
P(f"  label {lk}. Missing piece: a seed number, and a term that holds the condensate cold once theta averages to zero.")
RES["A3"] = dict(I=I1, HL_per_Gyr=HL, rows=rows, N0_window=[min(Ns), max(Ns)], log_Hubble_mass=math.log10(HM), label=lk, sign_selects_high_mass=True)

# ---------------- verdict ----------------
land = [x for x, y in (("A1", lab1), ("A2", lab2)) if y == "LANDS"]
if land and lk == "LINK": verdict = "T DERIVED"
elif land: verdict = "T LANDS WITHOUT A MECHANISM"
else: verdict = "T LOCATED, NOT DERIVED"
RES["verdict"] = verdict
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 3     # darwin: bytes
check("K5", rss < 1.0, f"peak RSS {rss:.2f} GB", "< 1 GB")
P(f"\nVERDICT (frozen rule): {verdict}; A1 {lab1}, A2 {lab2}, A3 {lk}")
P("kappa = 1/2 FITTED, unused; T LOCATED; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.")
json.dump({k: v for k, v in RES.items()}, open(os.path.join(HERE, f"td1_threshold{TAG}_results.json"), "w"), indent=1, sort_keys=True, default=float)
fails = [k for k, v in RES["checks"].items() if not v["pass"]]
if fails: P("FAILED CHECKS:", fails)
sys.exit(1 if fails else 0)
