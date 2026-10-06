"""p50: re-measure the Upsilon-robust gas-point a0 with Cosmicflows-4 (Tully+2023, VizieR J/ApJ/944/94) ROTATION-FREE distances (TRGB > Cepheid > SBF > SN Ia > SN II;
Tully-Fisher, Fundamental Plane and the combined DM are EXCLUDED: TF is built from rotation and would be circular for a0). Data outside the repo in
../_external_data/cosmicflows4/ (table2, Sesame positions for the SPARC names; approved by the owner 2026-10-05). Position match within 60 arcsec.
Control: for SPARC galaxies whose own distance is TRGB/Cepheid (f_D 2, 3), CF4's rotation-free distance must agree (median ratio within 5%).
Test: gas-point a0 (p41b selection, framework kernel, Upsilon 0.5, sigma_int 0.11) for (i) SPARC's original TRGB/Cepheid set, (ii) galaxies UPGRADED from Hubble flow to a CF4
rotation-free distance, (iii) all gas-point galaxies with a rotation-free distance (union), each with a galaxy bootstrap.
Run: python3 p50_cf4_distances.py [NBOOT]  |  MUTATE=1: CF4 distances scaled x1.2 (control C must fail)
"""
import csv, math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 300
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DD = os.path.join(os.path.dirname(REPO), "_external_data", "cosmicflows4")
def fw(l, a, b):
    s = l[a - 1:b].strip()
    return float(s) if s else float("nan")
CF = []
for l in open(os.path.join(DD, "table2.dat")):
    meth = [("TRGB", fw(l, 103, 107)), ("Cepheid", fw(l, 114, 119)), ("SBF", fw(l, 78, 83)), ("SNIa", fw(l, 42, 47)), ("SNII", fw(l, 91, 96))]
    pick = next(((m, dm) for m, dm in meth if math.isfinite(dm)), None)
    if pick: CF.append((fw(l, 138, 145), fw(l, 147, 154), pick[0], 10**(pick[1] / 5 + 1) / 1e6 * (1.2 if MUTATE else 1.0), int(l[0:7])))
CF = np.array([(r[0], r[1], r[3]) for r in CF]), [r[2] for r in CF], [r[4] for r in CF]
POS = {r["sparc_name"]: (float(r["ra_deg"]), float(r["dec_deg"])) for r in csv.DictReader(open(os.path.join(DD, "sesame_sparc.csv"))) if r["ra_deg"]}
def match(ra, de):
    d = 3600 * np.hypot((CF[0][:, 0] - ra) * math.cos(math.radians(de)), CF[0][:, 1] - de)
    i = int(np.argmin(d))
    return (CF[0][i, 2], CF[1][i], d[i]) if d[i] < 60 else None
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
for g in gals:
    m = match(*POS[g["name"]]) if g["name"] in POS else None
    g["cf4"] = m
# control
ctl = [(g["name"], g["D"], g["cf4"][0], g["cf4"][1]) for g in gals if g["fD"] in (2, 3) and g["cf4"]]
rat = np.array([c[2] / c[1] for c in ctl])
print(f"   control: {len(ctl)} SPARC TRGB/Cepheid galaxies matched in CF4 (rotation-free); D_CF4/D_SPARC median {np.median(rat):.3f}, 16-84% {np.percentile(rat,16):.3f}-{np.percentile(rat,84):.3f}")
check(f"C CF4 rotation-free distances agree with SPARC's own TRGB/Cepheid distances (median ratio {np.median(rat):.3f} within 5%)", abs(np.median(rat) - 1) < 0.05)
def sub(g, m):
    h = dict(g)
    for k in ("Rm", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"): h[k] = g[k][m]
    return h
def gaspts(sel):
    out = []
    for g in sel:
        vb2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2
        fg = np.where(vb2 > 0, np.sign(g["Vgas"]) * g["Vgas"]**2 / np.where(vb2 > 0, vb2, 1), 0)
        mm = fg > 0.8
        if mm.sum() >= 2: out.append(sub(g, mm))
    return out
A = np.exp(np.linspace(math.log(0.3e-10), math.log(3.0e-10), 121))
fit = lambda S: V.parabola_min(A, V.Profile(S, V.IF_alpha1, ufixed=0.5).scan(A, 0.11), k=6)[0]
def boot(S, nb):
    rng = np.random.default_rng(50); B = np.array([fit([S[i] for i in rng.integers(0, len(S), len(S))]) for _ in range(nb)])
    lo, hi = np.percentile(B, [16, 84]); return (hi - lo) / 2
orig = gaspts([g for g in gals if g["fD"] in (2, 3)])
upg_raw = [g for g in gals if g["fD"] not in (2, 3) and g["cf4"]]
upg = [V.transform(g, dist_scale=g["cf4"][0] / g["D"]) for g in upg_raw]
for g0, g1 in zip(upg_raw, upg): g1["name"] = g0["name"]
upgP = gaspts(upg)
print("   upgraded (Hubble flow -> CF4 rotation-free) galaxies with gas points: " +
      ", ".join(f"{g['name']} ({next(x['cf4'][1] for x in upg_raw if x['name']==g['name'])}, D {next(x['D'] for x in upg_raw if x['name']==g['name']):.1f}->{next(x['cf4'][0] for x in upg_raw if x['name']==g['name']):.1f})" for g in upgP))
out = {}
for lab, S in (("SPARC TRGB/Cepheid (original)", orig), ("upgraded via CF4", upgP), ("union: all rotation-free", orig + upgP)):
    if len(S) < 2: print(f"   {lab}: {len(S)} galaxies -- too few"); out[lab] = None; continue
    a = fit(S); e = boot(S, NB) / a
    out[lab] = (a, e, len(S))
    print(f"   {lab:32s}: {len(S):2d} galaxies, a0 = {a:.3e} +- {100*e:.1f}%   vs 0.936 {100*(a/9.3603e-11-1):+.1f}% | vs 1.131 {100*(a/1.1312e-10-1):+.1f}%")
u = out["union: all rotation-free"]
check(f"G the rotation-free set grows beyond SPARC's 8 (now {u[2] if u else 0})", u is not None and u[2] > 8)
# ---- POST-HOC sensitivity (added after the strict 0.8 cut found 0 upgrades): gas cut 0.7 (p41b: 17% Upsilon spread at 0.7, less clean)
def gaspts07(sel):
    out_ = []
    for g in sel:
        vb2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2
        fg = np.where(vb2 > 0, np.sign(g["Vgas"]) * g["Vgas"]**2 / np.where(vb2 > 0, vb2, 1), 0)
        mm = fg > 0.7
        if mm.sum() >= 2: out_.append(sub(g, mm))
    return out_
o7, u7 = gaspts07([g for g in gals if g["fD"] in (2, 3)]), gaspts07(upg)
print(f"   POST-HOC gas cut 0.7: original TRGB/Ceph {len(o7)} gal, upgraded {len(u7)} gal ({', '.join(g['name'] for g in u7)})")
for lab, S in (("cut 0.7, original TRGB/Ceph", o7), ("cut 0.7, upgraded via CF4", u7), ("cut 0.7, union", o7 + u7)):
    if len(S) >= 2:
        a = fit(S); e = boot(S, max(NB // 3, 30)) / a
        print(f"      {lab:30s}: {len(S):2d} gal, a0 = {a:.3e} +- {100*e:.1f}%   vs 0.936 {100*(a/9.3603e-11-1):+.1f}% | vs 1.131 {100*(a/1.1312e-10-1):+.1f}%")
# ---- POST-HOC: WALLABY gas points with CF4 rotation-free distances (p43 pipeline, distance overridden where CF4 has one)
import importlib.util, types
spec = importlib.util.spec_from_file_location("p43", os.path.join(os.path.dirname(os.path.abspath(__file__)), "p43_wallaby_gas_points.py"))
src43 = open(spec.origin).read().split("gals = build()")[0].replace("MUTATE = os.environ.get(\"MUTATE\") == \"1\"", "MUTATE = False")
ns = {"__file__": spec.origin, "__name__": "p43mod"}; sys.argv = [sys.argv[0], "10"]; exec(src43, ns)
wkin = {}
for r in ns["best"].values():
    m = match(float(r["RA_model"] or r["ra"]), float(r["DEC_model"] or r["dec"]))
    if m: wkin[r["name"]] = m
for nm, m in wkin.items():
    ns["src"][nm] = dict(ns["src"][nm], dist_h=str(m[0] * 73.0 / 70.0))      # build() multiplies dist_h by 70/H0 (H0 = 73)
Wall = ns["build"](); WP = ns["gas_points"](Wall)
WPu = [p for p in WP if p[0] in wkin]
print(f"   POST-HOC WALLABY: {len(wkin)} kinematic galaxies have a CF4 rotation-free distance; {len(WPu)} of them have gas points: {[p[0] for p in WPu]}")
if len(WPu) >= 2:
    aw = ns["fit"](WPu); print(f"      WALLABY upgraded subset a0 = {aw:.3e} (n = {len(WPu)}; too few for a bootstrap error)")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
