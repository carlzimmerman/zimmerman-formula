"""p47: a0 from LITTLE THINGS (Oh+2015, VizieR J/AJ/149/180; ../_external_data/little_things_oh2015/, approved by the owner 2026-10-05).
Per galaxy: total curve (rotdmbar 'Data', asymmetric-drift corrected) and DM-only curve (rotdm 'Data'), each de-scaled with its OWN R0.3, V0.3; DM interpolated onto the
total radii; baryons V_bar^2 = V_tot^2 - V_DM^2 (gas + stars with the AUTHORS' stellar M/L: NOT Upsilon-free, unlike p41b). Distances: table1 (Hunter+2012; mostly TRGB --
not re-verified per galaxy here). Framework kernel, log-g chi2 with e_V and sigma_int 0.11, a0 profiled, galaxy bootstrap. Samples: all points; outer half of each curve.
Cross-check: the galaxies also in SPARC (names matched by number) -- compare a0 from the two pipelines per galaxy.
Run: python3 p47_little_things_a0.py [NBOOT]  |  MUTATE=1: DM curve not subtracted (V_bar = V_tot: g_bar = g_obs, a0 -> ~0; check A must fail)
"""
import os, sys, math, re
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 300
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DD = os.path.join(os.path.dirname(REPO), "_external_data", "little_things_oh2015")
KPC = 3.0857e19
def load(fn):
    out = {}
    for l in open(os.path.join(DD, fn)):
        p = l.split()
        if len(p) < 7 or p[1] != "Data": continue
        R0, V0, Rs, Vs, eVs = map(float, p[2:7])
        out.setdefault(p[0], []).append((Rs * R0, Vs * V0, eVs * V0))
    return {k: np.array(sorted(v)) for k, v in out.items()}
TOT, DM = load("rotdmbar.dat"), load("rotdm.dat")
DIST = {}
for l in open(os.path.join(DD, "table1.dat")):
    p = l.split("|"); DIST[p[0].strip()] = float(p[2])
gals = []
for nm, t in TOT.items():
    if nm not in DM or nm not in DIST: continue
    d = DM[nm]
    R, Vt, eV = t[:, 0], t[:, 1], np.maximum(t[:, 2], 1.0)
    Vd = np.interp(R, d[:, 0], d[:, 1], left=np.nan, right=np.nan)
    vb2 = Vt**2 - (0 if MUTATE else 1) * Vd**2
    m = np.isfinite(vb2) & (vb2 > 0) & (R > 0)
    if m.sum() < 3: continue
    gals.append(dict(name=nm, R=R[m], gobs=(Vt[m] * 1e3)**2 / (R[m] * KPC), gbar=vb2[m] * 1e6 / (R[m] * KPC), sig=(2 * eV[m] / Vt[m]) / math.log(10)))
A = np.exp(np.linspace(math.log(0.2e-10), math.log(4e-10), 141))
def fit(G, outer=False):
    ch = np.zeros_like(A)
    for g in G:
        sl = slice(len(g["R"]) // 2, None) if outer else slice(None)
        gb, go, sg = g["gbar"][sl], g["gobs"][sl], g["sig"][sl]
        for i, a in enumerate(A):
            ch[i] += np.sum((np.log10(go) - np.log10(gb * np.sqrt(1 + a / gb)))**2 / (sg**2 + 0.11**2))
    return V.parabola_min(A, ch, k=6)[0]
a_all, a_out = fit(gals), fit(gals, outer=True)
rng = np.random.default_rng(47); B = np.array([fit([gals[i] for i in rng.integers(0, len(gals), len(gals))]) for _ in range(NB)])
lo, hi = np.percentile(B, [16, 84]); e = (hi - lo) / 2 / a_all
ys = np.concatenate([g["gbar"] for g in gals]) / 9.36e-11
print(f"   LITTLE THINGS: {len(gals)} galaxies with total + DM curves and a distance; {sum(len(g['R']) for g in gals)} points; y median {np.median(ys):.3f}")
print(f"   a0 (all points) = {a_all:.3e} +- {100*e:.1f}% (stat, galaxy bootstrap);  outer half: {a_out:.3e}")
for lab, v in (("kappa=1/2 rho_L", 9.3603e-11), ("alt rho_tot (original formula)", 1.1312e-10), ("SPARC TRGB gas points (p46)", 1.158e-10), ("SPARC all gas points", 9.00e-11)):
    print(f"      vs {lab:32s} {v:.3e}: {100*(a_all/v-1):+6.1f}%  ({math.log(a_all/v)/e:+.2f} sigma)")
# cross-check with SPARC for overlapping galaxies (per-galaxy a0 in both pipelines)
sp = {g["name"]: g for g in V.load_sparc()}
def key(n): return re.sub(r"[^A-Z0-9]", "", n.upper().split("|")[0])
spk = {key(k): k for k in sp}
pairs = []
for g in gals:
    k = key(g["name"])
    if k in spk:
        aL = fit([g]); aS = V.parabola_min(A, V.Profile([sp[spk[k]]], V.IF_alpha1, ufixed=0.5).scan(A, 0.11), k=6)[0]
        pairs.append((g["name"], spk[k], aL, aS))
        print(f"      overlap {g['name']:10s} = SPARC {spk[k]:10s}: a0 LT {aL:.3e}  SPARC {aS:.3e}  ratio {aL/aS:.2f}")
if pairs:
    r = np.array([p[2] / p[3] for p in pairs]); print(f"      overlap median ratio LT/SPARC = {np.median(r):.2f} (n = {len(r)})")
check(f"A LITTLE THINGS gives a finite a0 within a factor 2 of SPARC's gas-point value ({a_all:.3e})", 0.5 < a_all / 9.0e-11 < 2.0)
check("X the pipelines agree on the overlapping galaxies (median LT/SPARC ratio within 0.67-1.5)", bool(pairs) and 0.67 < np.median(r) < 1.5)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
