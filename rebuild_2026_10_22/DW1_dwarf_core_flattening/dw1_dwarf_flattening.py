"""DW1_dwarf_core_flattening -- frozen criteria FROZEN_CRITERIA.md (279b4aa47c).

M1 (short-mean-free-path saturation) and M2 (gravothermal collapse) are analytic screens; M3 (the law's sigma = the
halo's own V_max/sqrt2, solved self-consistently) is graded on X1's dwarfs at OS1's q_f.  MUTATE=1: sigma_h = sigma_ref.
"""
import os, sys, csv, json, math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUTATE = os.environ.get("MUTATE") == "1"; TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

G, MSUN, PC, YR = 6.674e-11, 1.989e30, 3.0857e16, 3.156e7
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
SREF = 70.50e3; T_AGE = 13.8e9 * YR; CAP0 = 0.254484
OS1 = json.load(open(os.path.join(REB, "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")))
QF = {f: OS1["footings"][f]["q_f"] for f in A0}
def Bk(x): return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)

P(f"DW1_dwarf_core_flattening{TAG}  (frozen 279b4aa47c)  kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"q_f from OS1: canonical {QF['canonical']:.3f}, alt {QF['alt']:.3f}; sigma_ref {SREF/1e3:.2f} km/s")
# K1
xs = np.logspace(-3, 3, 400001); m1g = float((Bk(xs) / xs).max())
dfun = lambda x: (4 * x * x / ((1 + x) * (1 + x * x))) / x - Bk(x) / x ** 2
xr = brentq(dfun, 1.0, 10.0, xtol=1e-14); M1 = float(Bk(xr) / xr)
k1 = abs(m1g - M1) < 1e-6
P(f"K1 m1 = max Bk(x)/x: grid {m1g:.7f}, root {M1:.7f} at x {xr:.4f}: {'PASS' if k1 else 'FAIL'}")
checks = [("K1", k1)]

# ---- M1 / M2 screens
RES = dict(frozen="279b4aa47c", mutate=MUTATE, q_f=QF, footings={})
for f, a0 in A0.items():
    q = QF[f]; knr = 4 / (3 * math.sqrt(math.pi)) * 2 * a0 * T_AGE / SREF
    kn = {s: knr * (s * 1e3 / SREF) ** (q - 1) for s in (5, 10, 20, 70.5, 1000)}
    P(f"M1 [{f}] Kn_ref {knr:.1f}; Kn at sigma 5/10/20/70.5/1000 km/s: " + " / ".join(f"{v:.0f}" for v in kn.values())
      + f" -> {'RULED OUT (Kn >> 1 everywhere)' if min(kn.values()) > 1 else 'Kn < 1 somewhere'}")
    RES["footings"][f] = dict(M1_Kn=kn, M1="RULED OUT" if min(kn.values()) > 1 else "OPEN")
P("M2 gravothermal collapse: the core law sets Gamma t = 1 at every core, so the collapse parameter is system-independent: RULED OUT within this law (structural)")

# ---- M3
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
R0G = np.logspace(math.log10(PC), math.log10(1e6 * PC), 4001)

def sigma_h(r0, f):
    q = QF[f]; SA = A0[f] / (2 * math.pi * G)
    return (math.pi * G * SA * SREF ** (-q) * r0 * M1 / 2) ** (1 / (2 - q))

def cap_halo(r12, f):
    q = QF[f]; SA = A0[f] / (2 * math.pi * G)
    def g(lr0):
        r0 = math.exp(lr0); sh = SREF if MUTATE else sigma_h(r0, f)
        return math.pi * G * SA * (sh / SREF) ** q * float(Bk(r12 / r0)) * (r0 / r12) ** 2
    vals = np.array([g(math.log(r)) for r in R0G]); i = int(vals.argmax())
    lo, hi = math.log(R0G[max(i - 1, 0)]), math.log(R0G[min(i + 1, len(R0G) - 1)])
    res = minimize_scalar(lambda l: -g(l), bounds=(lo, hi), method="bounded", options={"xatol": 1e-10})
    r0 = math.exp(res.x); return -res.fun, r0, (SREF if MUTATE else sigma_h(r0, f))

def grade(f, mode):
    a0 = A0[f]; q = QF[f]; out = []
    for r in [r for r in X1 if r["footing"] == f]:
        r12 = 4 / 3 * float(r["rh_pc"]) * PC; gN = G * (10 ** float(r["logMstar"]) * MSUN / 2) / r12 ** 2
        D, sd = float(r["Delta[Newton]"]), float(r["sdMC[Newton]"]); gobs = gN * 10 ** D
        sst = math.sqrt(gobs * r12 / 3)
        if mode == "stellar": cap, r0, sh = CAP0 * a0 * (sst / SREF) ** q, float("nan"), sst
        else: cap, r0, sh = cap_halo(r12, f)
        if D <= 0: out.append(dict(name=r["name"], cls=r["cls"], S=0.0, z=-np.inf, graded=True)); continue
        ratio = 10 ** D - 1
        if ratio < 0.1: out.append(dict(name=r["name"], cls=r["cls"], graded=False)); continue
        gh = gobs - gN; sdh = sd * 10 ** D / ratio
        Mh = float("nan")
        if np.isfinite(r0):
            SA = a0 / (2 * math.pi * G); Mh = math.pi * SA * (sh / SREF) ** q * r0 ** 2 * float(Bk(10.0)) / MSUN
        out.append(dict(name=r["name"], cls=r["cls"], S=gh / cap, z=(math.log10(gh) - math.log10(cap)) / sdh, graded=True,
                        sig_star=sst / 1e3, sig_h=sh / 1e3, r0_pc=r0 / PC if np.isfinite(r0) else None, M10r0=Mh,
                        plausible=bool(np.isfinite(r0) and r0 >= r12 / 3 and Mh <= 1e11)))
    g = [o for o in out if o["graded"]]
    fex = float(np.mean([o["z"] >= 2 for o in g])); medS = float(np.median([o["S"] for o in g]))
    return fex, medS, out

classes = {}
for f in A0:
    fs, ms, _ = grade(f, "stellar")
    k0 = abs(fs - OS1["footings"][f]["dwarfs"]["frac"]) < 0.001
    P(f"\n=== [{f}] K0 stellar-sigma rule reproduces OS1: frac {fs:.3f} (OS1 {OS1['footings'][f]['dwarfs']['frac']:.3f}), median S {ms:.2f}: {'PASS' if k0 else 'FAIL'}")
    checks.append((f"K0[{f}]", k0))
    fex, medS, rows = grade(f, "halo")
    if MUTATE:
        cd1 = {"canonical": 0.53, "alt": 0.44}[f]
        okm = abs(fex - 0.011) < 0.002 and abs(medS - cd1) < 0.006
        P(f"   MUTATE sigma_h = sigma_ref: frac {fex:.3f}, median S {medS:.3f} vs CD1 (0.011, {cd1}): {'REPRODUCES' if okm else 'DIFFERS'}")
        checks.append((f"MUT[{f}]", okm)); continue
    # K2: sigma_h solve self-consistency at one r0
    r0t = 300 * PC; sh = sigma_h(r0t, f); SA = A0[f] / (2 * math.pi * G)
    vmax = math.sqrt(math.pi * G * SA * (sh / SREF) ** QF[f] * r0t * M1)
    k2 = abs(vmax / math.sqrt(2) / sh - 1) < 1e-8; checks.append((f"K2[{f}]", k2))
    cls = "M3 RESCUES DWARFS" if (fex < 0.05 and medS <= 1) else ("M3 PARTIAL" if fex < 0.25 else "M3 FAILS")
    classes[f] = cls
    g = [o for o in rows if o["graded"] and "sig_h" in o]          # A1: reporting only (Delta <= 0 rows carry no halo)
    P(f"   K2 sigma_h solve self-consistent: {'PASS' if k2 else 'FAIL'}")
    P(f"   M3 halo-dispersion cap: frac z>=2 {fex:.3f}, median S {medS:.2f}  -> {cls}")
    P(f"   sigma_h/sigma_* median {np.median([o['sig_h'] / o['sig_star'] for o in g]):.2f}; median sigma_h {np.median([o['sig_h'] for o in g]):.1f} km/s; "
      f"median r0 {np.median([o['r0_pc'] for o in g]):.0f} pc; plausible (r0 >= r12/3, M(<10 r0) <= 1e11) {sum(o['plausible'] for o in g)}/{len(g)}")
    by = {}
    for o in [o for o in rows if o["graded"]]: by.setdefault(o["cls"], []).append(o)
    for k, v in sorted(by.items()):
        P(f"     {k:24s} n {len(v):3d} frac z>=2 {np.mean([o['z'] >= 2 for o in v]):.2f} median S {np.median([o['S'] for o in v]):.2f} "
          f"median sigma_h {np.median([o['sig_h'] for o in v if 'sig_h' in o]):.1f}")
    RES["footings"][f].update(M3=dict(cls=cls, frac=fex, medS=medS, rows=rows))

if not MUTATE:
    RES["verdict"] = classes["canonical"] if classes["canonical"] == classes["alt"] else f"UNDECIDED (footings disagree: {classes})"
    P(f"\n=== VERDICT (M3): {RES['verdict']}; M1 and M2 ruled out as stated")
n = sum(v for _, v in checks); P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks))
RES["checks"] = {k: bool(v) for k, v in checks}
open(os.path.join(HERE, f"dw1_dwarf_flattening{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"dw1_dwarf_flattening_results{TAG}.json"), "w"), indent=1, default=float)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
