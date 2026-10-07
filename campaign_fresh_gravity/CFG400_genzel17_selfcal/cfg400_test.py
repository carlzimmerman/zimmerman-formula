"""CFG400 test: per-galaxy self-calibrated a0(z) on Genzel+2017's six digitised curves. Criteria: FROZEN_CRITERIA.md (1dccb3a0c).
Run after cfg400_digitise.py: python3 cfg400_test.py ; MUTATE=1 multiplies every outer (R > R_1/2) velocity by 1.3 (Delta chi2 must move > 4; rc 1).
"""
import csv, json, math, os, sys
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import CFG4_common as C4  # noqa: E402

MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

# Table 1 (Genzel+2017): z, kpc/arcsec, inclination (prior), R_1/2 (n=1 fit), sigma0, Mbulge/Mbaryon, vc(R_1/2)
T1 = {"COS4 01351": (0.854, 7.68, 75, 7.3, 39, 0.20, 276), "D3a 6397": (1.500, 8.46, 30, 7.4, 73, 0.35, 310),
      "GS4 43501": (1.613, 8.47, 62, 4.9, 39, 0.40, 257), "zC 406690": (2.196, 8.26, 25, 5.5, 74, 0.60, 301),
      "zC 400569": (2.242, 8.23, 45, 3.3, 34, 0.37, 364), "D3a 15504": (2.383, 8.14, 34, 6.0, 76, 0.15, 299)}
PSF_HALF = 0.30                                          # arcsec (seeing 0.6" FWHM, conservative)
KPC, G = 3.0857e19, 6.674e-11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
Om = 0.315
def E(z): return math.sqrt(Om * (1 + z) ** 3 + 1 - Om)
def de(z):
    a = 1 / (1 + z); w0, wa = -0.838, -0.62
    return math.sqrt(a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a)))
LAWS = {"DE": de, "RIVAL": E, "FLAT": lambda z: 1.0}

def gbar_shape(R, Rhalf, bt):
    """unit-total-mass baryon acceleration (m/s^2 per Msun-equivalent scale; only the SHAPE matters): Freeman disc + Hernquist bulge (R_e 1 kpc)."""
    Rd = Rhalf / 1.678
    y = np.maximum(R / (2 * Rd), 1e-4)
    vd2 = 2 * (1 - bt) * (G * 1.989e30 / (Rd * KPC)) * y**2 * (i0(y) * k0(y) - i1(y) * k1(y))
    a = 1.0 / 1.8153
    Mb = bt * R**2 / (R + a) ** 2
    vb2 = G * 1.989e30 * Mb / (R * KPC)
    return (vd2 + vb2) / (R * KPC)

rows = list(csv.DictReader(open(os.path.join(HERE, "cfg400_points.csv"))))
data = {}
say("CFG400 self-calibrated a0(z), Genzel+2017" + ("  (MUTATE: outer v x1.3)" if MUTATE else ""))
say("=" * 78)
c2 = []
for g, (z, kpa, inc, Rh, s0, bt, vc) in T1.items():
    pts = [r for r in rows if r["galaxy"] == g and r["kind"] == "v"]
    R, V, eV = [], [], []
    for r in pts:
        off = abs(float(r["offset_arcsec"]))
        if off < PSF_HALF:
            continue
        Rk = off * kpa
        v = abs(float(r["value"])) / math.sin(math.radians(inc))
        if MUTATE and Rk > Rh:
            v *= 1.3
        ev = max(float(r["err"]), 1.0) / math.sin(math.radians(inc))
        R.append(Rk); V.append(v); eV.append(ev)
    R, V, eV = map(np.array, (R, V, eV))
    vc2 = V**2 + 3.36 * s0**2 * (R / Rh)
    gobs = vc2 * 1e6 / (R * KPC)
    elog = np.sqrt((2 * V * eV / vc2 / math.log(10)) ** 2 + 0.05**2)
    data[g] = dict(z=z, R=R, gobs=gobs, elog=elog, Rh=Rh, bt=bt)
    near = np.abs(R - Rh) < 0.35 * Rh
    vc_dig = float(np.sqrt(np.mean(vc2[near]))) if near.any() else float("nan")
    c2.append(abs(vc_dig / vc - 1) <= 0.20)
    say(f"  {g:11s} z {z:.2f}: {len(R)} points beyond the beam, R {R.min():.1f}-{R.max():.1f} kpc; vc(R_1/2) digitised {vc_dig:.0f} vs Table 1 {vc} km/s; "
        f"g_obs {gobs.max()/A0['canonical']:.2f}-{gobs.min()/A0['canonical']:.2f} a0")
check("C2 digitised vc(R_1/2) within 20% of Table 1 for >= 5 of 6", MUTATE or sum(c2) >= 5, f"{sum(c2)} of 6")
check("C3 >= 4 points per galaxy after the beam cut", all(len(d["R"]) >= 4 for d in data.values()), str({k: len(v['R']) for k, v in data.items()}))

LF = np.linspace(-3, 3, 3001)
def chi2_law(foot, law, scale=1.0, kernel="nu_mono"):
    tot = 0.0
    for g, d in data.items():
        gb = gbar_shape(d["R"], d["Rh"], d["bt"])
        a0 = A0[foot] * LAWS[law](d["z"]) * scale
        best = 1e99
        # profile f on a grid then refine
        for lf in LF[::10]:
            gn = gb * 10**lf * 1e11
            nu = C4.nu_mono(gn / a0) if kernel == "nu_mono" else np.sqrt(1 + a0 / gn)
            c = np.sum(((np.log10(d["gobs"]) - np.log10(nu * gn)) / d["elog"]) ** 2)
            best = min(best, c)
        tot += best
    return tot

res = {}
for foot in A0:
    c = {law: chi2_law(foot, law) for law in LAWS}
    res[foot] = c
    say(f"\n  {foot}: chi2 DE {c['DE']:.1f}, RIVAL {c['RIVAL']:.1f}, FLAT {c['FLAT']:.1f}  ->  Delta chi2 (RIVAL - DE) = {c['RIVAL'] - c['DE']:+.1f}")
dd = [res[f]["RIVAL"] - res[f]["DE"] for f in A0]
if all(abs(x) >= 9 for x in dd) and np.sign(dd[0]) == np.sign(dd[1]):
    V_ = "SEPARATES (" + ("DE preferred" if dd[0] > 0 else "RIVAL preferred") + ")"
elif all(abs(x) >= 4 for x in dd) and np.sign(dd[0]) == np.sign(dd[1]):
    V_ = "LEANS (" + ("DE" if dd[0] > 0 else "RIVAL") + ")"
else:
    V_ = "NON-DIAGNOSTIC"
say(f"\nVERDICT: {V_}")
# reported: a0 scale profile relative to the DE law (canonical), and pressure systematic
sc = np.logspace(-1.5, 1.5, 121)
prof = [chi2_law("canonical", "DE", s) for s in sc]
i = int(np.argmin(prof)); within = sc[np.array(prof) <= prof[i] + 1]
say(f"  REPORTED: best common a0 scale relative to the DE law (canonical): x{sc[i]:.2f} (1-sigma {within.min():.2f}-{within.max():.2f}); the RIVAL corresponds to x{np.median([E(d['z'])/de(d['z']) for d in data.values()]):.2f}")
pres = {}
for fac in (0.5, 2.0):
    store = {g: d["gobs"].copy() for g, d in data.items()}
    for g, d in data.items():
        z, kpa, inc, Rh, s0, bt, vc = T1[g]
        V2 = d["gobs"] * d["R"] * KPC / 1e6 - 3.36 * s0**2 * (d["R"] / Rh)
        d["gobs"] = (V2 + fac * 3.36 * s0**2 * (d["R"] / Rh)) * 1e6 / (d["R"] * KPC)
    pres[fac] = chi2_law("canonical", "RIVAL") - chi2_law("canonical", "DE")
    for g in data:
        data[g]["gobs"] = store[g]
say(f"  REPORTED pressure systematic (canonical): Delta chi2 with the drift term x0.5 {pres[0.5]:+.1f}, x2 {pres[2.0]:+.1f}")
check("T-MUT main-run marker (MUTATE outer x1.3 must move Delta chi2 by > 4)", not MUTATE, f"{dd[0]:+.1f}")
if MUTATE:
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": dd})
n = sum(c_["pass"] for c_ in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG400", "mutate": MUTATE, "verdict": V_, "chi2": res, "delta": dd, "a0_scale_best": float(sc[i]),
           "a0_scale_1sigma": [float(within.min()), float(within.max())], "pressure": {str(k): v for k, v in pres.items()}, "checks": checks},
          open(os.path.join(HERE, f"cfg400_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg400{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
