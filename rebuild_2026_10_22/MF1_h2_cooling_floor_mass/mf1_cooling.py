#!/usr/bin/env python3
"""MF1_h2_cooling_floor_mass: M_f from H2 cooling in route E floor halos, then X49's regrade with M200 = max(EM1, M_f).

Frozen criteria: FROZEN_CRITERIA.md (b612d856a4). Reads X1's CSV, CFG257's binary table, EM1's relation, F3's background (read-only).
One thread, seconds.

    python3 mf1_cooling.py            -> mf1_cooling.out, mf1_results.json
    python3 mf1_cooling.py --mutate   -> Lambda / 1000, separate outputs; exit 1 if the shift does not bite
"""
import csv, json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""; OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
KB, MP = 1.380649e-23, 1.67262192e-27
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
SIG = {f: A0[f] / (2 * math.pi * G) for f in FEET}; SIGPC = {f: SIG[f] * PC ** 2 / MSUN for f in FEET}
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")
GPK, XPK, MU = 0.254484, 0.9634, 1.22
ZS = (10.0, 15.0, 25.0); WIN = (6.25, 7.00)
P(f"MF1_h2_cooling_floor_mass  {'MUTATE (Lambda / 1000)' if MUTATE else 'normal run'}  frozen b612d856a4")
P("kappa = 1/2 FITTED; route E, floor Burkert halos; NOT blind (window known); not theory closed")

EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3P = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]["A_c2b_refit"]["params"]
a_, b_ = EM1J["rows"]["A_c2b_refit"]["R1"]["a"], EM1J["rows"]["A_c2b_refit"]["R1"]["b"]
h = F3P["h"]; OB = F3P["omega_b"] / h ** 2; OM = OB + F3P["omega_cdm"] / h ** 2
H0 = 100 * h * 1e3 / MPC; RHOC = 3 * H0 ** 2 / (8 * math.pi * G)
def Hz(z): return H0 * math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
X0 = 1.2e-5 * math.sqrt(OM) / (OB * h)
P(f"Native background: h {h:.4f}, Om {OM:.4f}, Ob {OB:.4f}, x0 {X0:.3e}")

def lam(T):       # Galli & Palla 1998, low density, erg cm^3 / s
    t = math.log10(T); v = 10 ** (-103.0 + 97.59 * t - 48.05 * t ** 2 + 10.80 * t ** 3 - 0.9032 * t ** 4)
    return v / 1000 if MUTATE else v
def krec(T): return 1.88e-10 * T ** -0.64
def kmol(T): return 1.83e-18 * T ** 0.88
def xh2(T, n, t): return kmol(T) / krec(T) * math.log1p(X0 * n * krec(T) * t)
def tcool(T, n, t): return 1.5 * (KB * 1e7) * T / (xh2(T, n, t) * n * lam(T))
def n_vir(z): return 0.76 * 178 * OB * RHOC * (1 + z) ** 3 / MP * 1e-6      # cm^-3
def Tcrit(z, n=None):
    n = n_vir(z) if n is None else n; t = 1 / Hz(z)
    Ts = np.logspace(2, 4, 2001)
    for T in Ts:
        if tcool(float(T), n, t) <= t: return float(T)
    return 1e4 if MUTATE else float("nan")       # MUTATE: no H2 solution below 1e4 K, so the threshold caps at atomic

def B(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def R200_of(M): return (3 * M * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot): return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
def M200_of_r0(r0_m, Sig):
    return math.exp(brentq(lambda lm: math.pi * Sig * r0_m ** 2 * float(B(R200_of(math.exp(lm)) / r0_m)) / MSUN - math.exp(lm), math.log(1e2), math.log(1e15)))
def r0_of_T(T, a0): return (2 * KB * T / (MU * MP)) / (GPK * a0 * XPK)
def Mf_of_T(T, a0, Sig): return M200_of_r0(r0_of_T(T, a0), Sig)
def T_core_density(z, f):
    n = n_vir(z)
    for _ in range(60):
        T = Tcrit(z, n); r0 = r0_of_T(T, A0[f]); rho0 = SIG[f] / r0       # kg/m^3
        new = 0.76 * (OB / OM) * rho0 / MP * 1e-6
        if abs(new / n - 1) < 1e-4: break
        n = math.sqrt(n * new)
    return T, n

ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
def base(f):
    out = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC; Mb = 10 ** float(r["logMstar"])
        out.append(dict(name=r["name"], cls=r["cls"], lm=float(r["logMstar"]), gobs=3 * (sc * 1e3) ** 2 / r12, gN=G * (Mb / 2) * MSUN / r12 ** 2, r12=r12,
                        M200=10 ** (a_ + b_ * (math.log10(Mb) - 10)), s=float(r["sdMC[Newton]"])))
    return out
def boot(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float); ry = np.argsort(np.argsort(y)).astype(float); rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / math.sqrt((rx ** 2).sum() * (ry ** 2).sum()))
def regrade(f, Mf):
    Rw = base(f); rng = np.random.default_rng(20261026); res = {}; allE = []
    for x in Rw:
        M = max(x["M200"], Mf); R2 = R200_of(M); r0 = solve_r0(M * MSUN, R2, SIG[f])
        x["E"] = math.log10(x["gobs"] / (x["gN"] + G * math.pi * SIG[f] * r0 ** 2 * float(B(min(x["r12"], R2) / r0)) / x["r12"] ** 2))
    for c in CLS:
        q = [x for x in Rw if x["cls"] == c]; m, sd = boot(np.array([x["E"] for x in q]), np.array([x["s"] for x in q]), rng)
        res[c] = dict(N=len(q), E=m, sd=sd, Z=m / sd, ok=abs(m / sd) < 2)
    res["_rho"] = spearman(np.array([x["lm"] for x in Rw]), np.array([x["E"] for x in Rw]))
    res["_above"] = [x["name"] for x in Rw if x["E"] > 2 * x["s"]]; res["_below"] = [x["name"] for x in Rw if x["E"] < -2 * x["s"]]
    res["_draco"] = next(x["E"] for x in Rw if x["name"] == "Draco")
    return res

RES = dict(frozen="b612d856a4", mutate=MUTATE, footings={}, Tcrit={})
P("\n=== Chemistry: T_crit(z), virial-density gas")
for z in ZS:
    T = Tcrit(z); n = n_vir(z); t = 1 / Hz(z); RES["Tcrit"][str(int(z))] = T
    P(f"  z {z:4.0f}: n {n:7.3f} cm^-3, t {t / 3.156e13:6.1f} Myr, T_crit {T:7.1f} K, x_H2 {xh2(T, n, t):.2e}, V {math.sqrt(2 * KB * T / (MU * MP)) / 1e3:.2f} km/s")

checks = []
L1 = -103.0 + 97.59 * 3 - 48.05 * 9 + 10.80 * 27 - 0.9032 * 81
checks.append(("K1 Lambda(1000)", abs(L1 + 24.24) < 0.01))
checks.append(("K2 x0", 1.5e-4 <= X0 <= 3e-4))
Tk, nk, tk = 1000.0, 1.0, 3e15
sol = solve_ivp(lambda s, y: [-krec(Tk) * nk * y[0] ** 2, kmol(Tk) * nk * y[0]], (0, tk), [X0, 0.0], rtol=1e-9, atol=1e-16, method="LSODA")
checks.append(("K3 x_H2 ODE", abs(sol.y[1, -1] / xh2(Tk, nk, tk) - 1) < 0.05))
K4R = {"canonical": 0.51, "alt": 0.02}
for f in FEET:
    checks.append((f"K4[{f}]", abs(regrade(f, 10 ** 6.5)["MW ultra-faint"]["Z"] - K4R[f]) < 0.15))
    r = solve_r0(1e8 * MSUN, R200_of(1e8), SIG[f]); checks.append((f"K5[{f}]", abs(M200_of_r0(r, SIG[f]) / 1e8 - 1) < 1e-3))

verd = {}
for f in FEET:
    FR = RES["footings"][f] = {}
    P(f"\n=== [{f}] Sigma {SIGPC[f]:.1f} Msun/pc^2")
    Mf = {}
    for z in ZS:
        T = RES["Tcrit"][str(int(z))]; r0 = r0_of_T(T, A0[f]); Mf[z] = Mf_of_T(T, A0[f], SIG[f])
        R2z = (3 * Mf[z] * MSUN / (4 * math.pi * 200 * RHOC * (Hz(z) / H0) ** 2)) ** (1 / 3); V2z = math.sqrt(G * Mf[z] * MSUN / R2z)
        T200 = MU * MP * V2z ** 2 / (2 * KB)
        P(f"  z {z:4.0f}: T_crit {T:7.1f} K -> r0 {r0 / PC:6.1f} pc -> lg M_f {math.log10(Mf[z]):.3f}  in window {WIN[0] <= math.log10(Mf[z]) <= WIN[1]};  V200(z) there {V2z / 1e3:.2f} km/s = T {T200:.0f} K (reported)")
    FR["lgMf"] = {str(int(z)): math.log10(Mf[z]) for z in ZS}
    P("  Regrade at M_f(z = 15):")
    rg = regrade(f, Mf[15.0]); FR["regrade"] = rg
    for c in CLS: P(f"    {c:15s} N {rg[c]['N']:2d}: E {rg[c]['E']:+.3f} +- {rg[c]['sd']:.3f} (Z {rg[c]['Z']:+.2f}) {'REPRODUCED' if rg[c]['ok'] else 'FAIL'}")
    P(f"    Spearman(E, lg M*) {rg['_rho']:+.2f} (X49 -0.64); above by >2s: {len(rg['_above'])}, below by >2s: {len(rg['_below'])}; Draco E {rg['_draco']:+.3f}")
    Ta = 1e4; Ma = Mf_of_T(Ta, A0[f], SIG[f]); ra = regrade(f, Ma); FR["atomic"] = dict(lgMf=math.log10(Ma), regrade=ra)
    aok = all(ra[c]["ok"] for c in CLS)
    P(f"  Tooth, atomic 1e4 K: lg M_f {math.log10(Ma):.3f}; " + ", ".join(f"{c[:9]} {ra[c]['Z']:+.2f}" for c in CLS) + f"; all five {aok}")
    all5 = all(rg[c]["ok"] for c in CLS); band = all(WIN[0] <= math.log10(Mf[z]) <= WIN[1] for z in ZS)
    verd[f] = "NOT DIAGNOSTIC" if aok else ("CONSISTENT, BAND-STABLE" if all5 and band else ("CONSISTENT, z-DEPENDENT" if all5 else "MISS"))
    P(f"  VERDICT [{f}]: {verd[f]}")
    # Reported only
    Tc, nc = T_core_density(15.0, f); Mc = Mf_of_T(Tc, A0[f], SIG[f]); FR["core_density"] = dict(T=Tc, n=nc, lgMf=math.log10(Mc))
    P(f"  Reported: core-density gas (z 15) n {nc:.1f} cm^-3, T {Tc:.0f} K, lg M_f {math.log10(Mc):.3f}")
    Ml = Mf_of_T(RES["Tcrit"]["15"], A0[f] * 0.93, SIG[f] * 0.93); P(f"  Reported: a0 x 0.93: lg M_f {math.log10(Ml):.3f}")
    for T in (1000., 2000.): P(f"  Reported: T {T:.0f} K fixed: lg M_f {math.log10(Mf_of_T(T, A0[f], SIG[f])):.3f}")
    for lm_ in WIN:
        lo, hi = 50., 5e4
        Tw = brentq(lambda T: math.log10(Mf_of_T(T, A0[f], SIG[f])) - lm_, lo, hi)
        P(f"  Reported: window edge lg {lm_} corresponds to T {Tw:.0f} K")
RES["verdict"] = verd

P("\nChecks: " + ", ".join(f"{n} {'PASS' if v else 'FAIL'}" for n, v in checks))
RES["checks"] = {n: bool(v) for n, v in checks}
code = 0 if all(v for _, v in checks) else 1
if MUTATE:
    base_res = json.load(open(os.path.join(HERE, "mf1_results.json")))
    bite = all(abs(RES["footings"][f]["lgMf"]["15"] - base_res["footings"][f]["lgMf"]["15"]) > 0.25 for f in FEET) and RES["Tcrit"]["15"] > base_res["Tcrit"]["15"]
    P(f"MUTATE bite (T_crit up, lg M_f moved > 0.25, both footings): {bite}"); RES["mutate_bite"] = bite; code = 0 if bite else 1
json.dump(RES, open(os.path.join(HERE, f"mf1_results{TAG}.json"), "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else str(o))
open(os.path.join(HERE, f"mf1_cooling{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(code)
