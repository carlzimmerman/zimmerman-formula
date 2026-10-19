"""CFG828 -- uniform dwarf excess: LAW-SHAPE or DISPERSION-SPECIFIC?  Criteria: FROZEN_CRITERIA.md (dbbfeedff).
SPARC (Lelli+16, Lelli+17 cuts) vs CFG827 pressure-supported dwarfs at matched g_bar.  Run: python3 cfg828.py (CFG828_MUTATE=1).
kappa = 1/2 FITTED; not theory closed."""
import os, glob, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG828_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
nu_s = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-12)))
# ---- SPARC
Q = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q[v[0]] = (float(v[5]), int(v[17]))
        except ValueError: pass
gb, go = [], []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", ""); inc, q = Q.get(name, (0, 3))
    if q > 2 or inc < 30: continue
    for l in open(fn):
        if l.startswith("#") or not l.strip(): continue
        R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
        if V <= 0 or R <= 0 or eV / V >= 0.10: continue
        g_b = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
        if g_b <= 0: continue
        gb.append(g_b); go.append(V * V * 1e6 / (R * KPC))
gb, go = np.array(gb), np.array(go)
# ---- dwarfs (CFG827 rows, Ups_SFH at [M/H] -1.31)
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
import csv
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))):
        def fn_(x):
            try: return float(x)
            except: return None
        LVD[r["name"]] = (fn_(r.get("M_V")), fn_(r.get("rhalf_sph_physical")) or fn_(r.get("rhalf_physical")))
EXCL = {"WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
DW = []
for nm, r in R27.items():
    if nm in EXCL: continue
    MV, rh = LVD[nm]; s = R24[nm]["so"] / (1.45 if MUT else 1.0); r12 = (4 / 3) * rh * PC
    Ms = r["ups"] * 10 ** (0.4 * (4.83 - MV))
    DW.append(dict(name=nm, gbar=G * (Ms / 2) * Msun / r12 ** 2, gobs=3 * (s * 1e3) ** 2 / r12, train=r["train"]))
P(f"CFG828  dwarf excess: rotation (SPARC) vs dispersion at matched g_bar" + ("  [MUTATE sigma/1.45]" if MUT else ""))
P(f"  SPARC points after Lelli+17 cuts: {len(gb)} (g_bar {gb.min():.1e} .. {gb.max():.1e});  dwarfs: {len(DW)} (excluded {sorted(EXCL)})")
RES = dict(lane="CFG828", mutate=MUT, n_sparc=int(len(gb)))
rng = np.random.default_rng(828)
for foot in ("canonical", "alt"):
    for kn, nu in (("nu_e", nu_e), ("nu_simple", nu_s)):
        if foot == "alt" and kn == "nu_simple": continue
        a0 = A0[foot]; dS = np.log10(go / (gb * nu(gb / a0))); lg = np.log10(gb)
        rows = []
        for d in DW:
            dd = math.log10(d["gobs"] / (d["gbar"] * float(nu(d["gbar"] / a0)))); w = np.abs(lg - math.log10(d["gbar"])) <= 0.15
            rows.append(dict(name=d["name"], lgbar=math.log10(d["gbar"]), delta=dd, n_sparc=int(w.sum()), dS=float(np.median(dS[w])) if w.sum() >= 20 else None))
        inr = [r for r in rows if r["dS"] is not None]; D = np.array([r["delta"] - r["dS"] for r in inr])
        boot = [rng.choice(D, len(D)).mean() for _ in range(2000)] if len(D) else [0]
        mD, sD = (float(D.mean()), float(np.std(boot))) if len(D) else (float("nan"), float("nan")); z = mD / sD if len(D) else float("nan")
        dS_in = float(np.median([r["dS"] for r in inr])) if inr else float("nan")
        cls = "NOT DIAGNOSTIC" if len(inr) < 8 else ("DISPERSION-SPECIFIC" if (mD > 0 and z >= 3) else ("LAW-SHAPE" if (abs(z) < 2 and dS_in >= 0.10) else "MIXED"))
        out_ = [r for r in rows if r["dS"] is None]
        RES[f"{foot}|{kn}"] = dict(N_in=len(inr), mean_D=mD, se_D=sD, z=z, sparc_median_in=dS_in, sparc_median_all=float(np.median(dS)), cls=cls, rows=rows,
                                   out_of_range_mean_delta=float(np.mean([r["delta"] for r in out_])) if out_ else None)
        P(f"\n  [{foot} | {kn}] SPARC overall median Delta {np.median(dS):+.3f} dex")
        bins = np.arange(-12.75, -8.74, 0.25)
        P("    SPARC Delta by log g_bar bin: " + "  ".join(f"{b:.2f}:{np.median(dS[(lg >= b) & (lg < b + 0.25)]):+.2f}({((lg >= b) & (lg < b + 0.25)).sum()})" for b in bins if ((lg >= b) & (lg < b + 0.25)).sum() >= 10))
        P(f"    dwarfs in SPARC range: {len(inr)}  mean dwarf Delta {np.mean([r['delta'] for r in inr]):+.3f}  SPARC Delta at their g_bar (median) {dS_in:+.3f}")
        P(f"    mean D = Delta_dwarf - Delta_SPARC = {mD:+.3f} +- {sD:.3f} dex  (z {z:+.1f})  -> {cls}")
        if out_: P(f"    out of SPARC range ({len(out_)}): mean Delta {np.mean([r['delta'] for r in out_]):+.3f}  ({', '.join(r['name'] for r in out_)})")
if not MUT:
    P("\n  per dwarf (canonical, nu_e): name  log g_bar  Delta  SPARC-window Delta (n)")
    for r in sorted(RES["canonical|nu_e"]["rows"], key=lambda r: r["lgbar"]):
        P(f"    {r['name']:18s} {r['lgbar']:6.2f} {r['delta']:+6.2f}  {('%+.2f' % r['dS']) if r['dS'] is not None else '  -  '} ({r['n_sparc']})")
    k1 = RES["canonical|nu_e"]["sparc_median_all"]; P(f"\n  K1 SPARC overall median {k1:+.3f} dex -> {'PASS' if abs(k1) <= 0.05 else 'FAIL'}")
RES["cls"] = RES["canonical|nu_e"]["cls"]; P(f"\n  CLASS (canonical, primary nu): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg828_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg828{sfx}.out"), "w").write("\n".join(OUT) + "\n")
