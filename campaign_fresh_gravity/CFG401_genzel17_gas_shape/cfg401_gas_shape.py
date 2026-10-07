"""CFG401: CFG400 with stars + an extended gas disc (2 x R_d, record convention), gas fractions from Genzel+2017 Table 1 priors,
beam cut at FWHM. Gate: per-galaxy a0 consistency before any law comparison. Criteria: FROZEN_CRITERIA.md.
Run: python3 cfg401_gas_shape.py ; MUTATE=1 sets the gas scale to 1 x R_d (spread must change by > 0.2 dex; rc 1).
"""
import csv, json, math, os, sys
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import CFG4_common as C4  # noqa: E402

MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
GAS_SCALE = 1.0 if MUTATE else 2.0
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

# Table 1: z, kpc/", inc, R_1/2, sigma0, B/T, vc(R_1/2), M* prior, Mbaryon prior (1e11)
T1 = {"COS4 01351": (0.854, 7.68, 75, 7.3, 39, 0.20, 276, 0.54, 0.9), "D3a 6397": (1.500, 8.46, 30, 7.4, 73, 0.35, 310, 1.2, 2.3),
      "GS4 43501": (1.613, 8.47, 62, 4.9, 39, 0.40, 257, 0.41, 0.75), "zC 406690": (2.196, 8.26, 25, 5.5, 74, 0.60, 301, 0.42, 1.4),
      "zC 400569": (2.242, 8.23, 45, 3.3, 34, 0.37, 364, 1.2, 2.5), "D3a 15504": (2.383, 8.14, 34, 6.0, 76, 0.15, 299, 1.1, 2.0)}
FWHM = 0.6
KPC, G, MS = 3.0857e19, 6.674e-11, 1.989e30
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
Om = 0.315
E = lambda z: math.sqrt(Om * (1 + z) ** 3 + 1 - Om)
def de(z):
    a = 1 / (1 + z); w0, wa = -0.838, -0.62
    return math.sqrt(a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a)))
LAWS = {"DE": de, "RIVAL": E, "FLAT": lambda z: 1.0}

def disc(R, Rd, M):
    y = np.maximum(R / (2 * Rd), 1e-4)
    return 2 * M * (G * MS / (Rd * KPC)) * y**2 * (i0(y) * k0(y) - i1(y) * k1(y)) / (R * KPC)
def gshape(R, Rh, bt, fgas):
    Rd = Rh / 1.678
    a = 1.0 / 1.8153
    stars = (1 - fgas)
    g_st = disc(R, Rd, stars * (1 - bt)) + G * MS * stars * bt * R**2 / (R + a) ** 2 / (R * KPC) ** 2
    g_gas = disc(R, GAS_SCALE * Rd, fgas) if fgas > 0 else 0 * R
    return g_st + g_gas

say("CFG401 two-component shape" + ("  (MUTATE: gas at 1 x R_d)" if MUTATE else ""))
say("=" * 78)
Rt = np.linspace(2, 20, 50)
c1 = np.max(np.abs(gshape(Rt, 5.0, 0.3, 0.0) / (disc(Rt, 5.0 / 1.678, 0.7) + G * MS * 0.3 * Rt**2 / (Rt + 1 / 1.8153) ** 2 / (Rt * KPC) ** 2) - 1))
check("C1 two-component shape reduces to the stars-only shape at f_gas = 0", c1 < 1e-12, f"{c1:.1e}")

rows = list(csv.DictReader(open(os.path.join(HERE, "..", "CFG400_genzel17_selfcal", "cfg400_points.csv"))))
data = {}
for g, (z, kpa, inc, Rh, s0, bt, vc, ms, mb) in T1.items():
    R, V, eV = [], [], []
    for r in rows:
        if r["galaxy"] != g or r["kind"] != "v":
            continue
        off = abs(float(r["offset_arcsec"]))
        if off < FWHM:
            continue
        R.append(off * kpa); V.append(abs(float(r["value"])) / math.sin(math.radians(inc))); eV.append(max(float(r["err"]), 1.0) / math.sin(math.radians(inc)))
    if len(R) < 4:
        say(f"  {g}: {len(R)} points beyond FWHM -> DROPPED"); continue
    R, V, eV = map(np.array, (R, V, eV))
    vc2 = V**2 + 3.36 * s0**2 * (R / Rh)
    data[g] = dict(z=z, R=R, gobs=vc2 * 1e6 / (R * KPC), elog=np.sqrt((2 * V * eV / vc2 / math.log(10)) ** 2 + 0.05**2),
                   Rh=Rh, bt=bt, fgas=1 - ms / mb)

LF = np.linspace(-3, 3, 601); SC = np.logspace(-2, 2, 161)
def fit(d, a0):
    gb = gshape(d["R"], d["Rh"], d["bt"], d["fgas"]); best = 1e99
    for lf in LF:
        gn = gb * 10**lf * 1e11
        best = min(best, float(np.sum(((np.log10(d["gobs"]) - np.log10(C4.nu_mono(gn / a0) * gn)) / d["elog"]) ** 2)))
    return best
say("\nG-CONSISTENCY: per-galaxy best a0 (canonical, f and a0 free; grid x0.01-x100)")
per = {}
for g, d in data.items():
    prof = [fit(d, A0["canonical"] * s) for s in SC]
    i = int(np.argmin(prof)); per[g] = math.log10(SC[i])
    edge = i in (0, len(SC) - 1)
    say(f"  {g:11s} z {d['z']:.2f} f_gas {d['fgas']:.2f}, {len(d['R'])} pts: best a0 x{SC[i]:.2f}{'  (GRID EDGE)' if edge else ''}; chi2/N {prof[i]/len(d['R']):.2f}")
vals = np.array(list(per.values()))
spread = float(np.percentile(vals, 84) - np.percentile(vals, 16))
edges = sum(1 for v in vals if abs(v) >= 1.999)
gate = (edges == 0) and spread <= 0.5
say(f"  spread (16-84%) {spread:.2f} dex; grid-edge galaxies {edges} -> G-CONSISTENCY {'PASS' if gate else 'FAIL'}")
res = {}
if gate:
    for foot in A0:
        c = {law: sum(fit(d, A0[foot] * LAWS[law](d["z"])) for d in data.values()) for law in LAWS}
        res[foot] = c
        say(f"  {foot}: chi2 DE {c['DE']:.1f} RIVAL {c['RIVAL']:.1f} FLAT {c['FLAT']:.1f}; Delta (RIVAL-DE) {c['RIVAL']-c['DE']:+.1f}")
    dd = [res[f]["RIVAL"] - res[f]["DE"] for f in A0]
    V_ = ("SEPARATES" if all(abs(x) >= 9 for x in dd) else "LEANS" if all(abs(x) >= 4 for x in dd) else "NON-DIAGNOSTIC") if np.sign(dd[0]) == np.sign(dd[1]) else "NON-DIAGNOSTIC"
    if V_ != "NON-DIAGNOSTIC":
        V_ += " (" + ("DE" if dd[0] > 0 else "RIVAL") + ")"
else:
    V_ = "INVALID AGAIN: no law comparison (Genzel+2017 needs resolved gas maps for this test)"
say(f"\nVERDICT: {V_}")
check("T-MUT main-run marker (MUTATE gas 1xR_d must move the spread by > 0.2 dex)", not MUTATE, f"spread {spread:.2f}")
if MUTATE:
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": spread})
n = sum(c_["pass"] for c_ in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG401", "mutate": MUTATE, "per_galaxy_log_a0": per, "spread": spread, "gate": gate, "verdict": V_, "chi2": res, "checks": checks},
          open(os.path.join(HERE, f"cfg401_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg401{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
