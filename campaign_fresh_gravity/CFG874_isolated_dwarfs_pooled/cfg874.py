"""CFG874 -- all 11 isolated Local Group dwarfs (stellar sigma, >=300 kpc from MW and M31), pooled, gas counted, vs satellites.
Criteria: FROZEN_CRITERIA.md (ac12da6c0).  Run: python3 cfg874.py  (CFG874_MUTATE=up|down).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG874_MUTATE", ""); assert MUT in ("", "up", "down"); SUF = f"_MUTATE_{MUT}" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu_e = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))
def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}   # CFG852 / CFG860
DIRR = ("Leo A", "Sagittarius dIrr")                                                                         # variant only
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R860 = json.load(open(os.path.join(LANES, "CFG860_stripping_vs_isolated_dwarfs", "cfg860_results.json")))["members"]

def gas_in(lHI, r12_pc, mode):
    if lHI is None or mode == "zero": return 0.0
    Mg = 1.33 * 10 ** lHI
    if mode == "full": return Mg
    if mode == "half": return Mg / 2                                                   # CFG860 convention
    MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3                     # pc
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = (max(roots) if mode == "disc" else min(roots)) if roots else RHI / 2          # disc = extended (primary); compact = bracket
    x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))

SAMPLE = []
for nm, r in LVD.items():
    if nm in EXCL and nm not in DIRR: continue
    s = fnum(r.get("vlos_sigma"))
    if s is None or fnum(r.get("vlos_sigma_ul")) is not None: continue
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")); MV = fnum(r.get("M_V"))
    if rh is None or MV is None: continue
    dmw, dm31 = fnum(r.get("distance_gc")), fnum(r.get("distance_m31"))
    if dmw is None or dm31 is None: continue
    det = fnum(r.get("mass_HI")); dmin = min(dmw, dm31)
    grp = ("I" if dmin >= 300 else ("S" if det is None else "SG"))
    if nm in DIRR: grp = "DIRR" if dmin >= 300 else "x"
    SAMPLE.append(dict(name=nm, grp=grp, s=s, rh=rh, MV=MV, lHI=det, dmin=dmin, host=r.get("host") or "-"))

def build(foot, gas="disc", ups="2", sig_mut=True):
    a0 = A0[foot]; rows = []
    for d in SAMPLE:
        s = d["s"]
        if sig_mut and MUT and d["grp"] in ("I", "DIRR"): s = s * 1.45 if MUT == "up" else s / 1.45
        r12_pc = (4 / 3) * d["rh"]; r12 = r12_pc * PC
        U = R27[d["name"]]["ups"] if (ups == "SFH" and d["name"] in R27) else 2.0
        Ms = U * 10 ** (0.4 * (4.83 - d["MV"])); Mg = gas_in(d["lHI"], r12_pc, gas)
        gb = G * (Ms / 2 + Mg) * Msun / r12 ** 2
        rows.append(dict(d, Mg=Mg, Ms=Ms, lg=math.log10(gb), D=math.log10(3 * (s * 1e3) ** 2 / r12 / (gb * nu_e(gb / a0)))))
    return rows

def analyse(rows, iso=("I",), restrict=True, drop=(), smv=None, mindist=300.0, seed=874, nb=4000):
    I = [r for r in rows if r["grp"] in iso and r["name"] not in drop and r["dmin"] >= mindist]
    S = [r for r in rows if r["grp"] == "S" and (smv is None or r["MV"] <= smv)]
    if restrict:
        lo, hi = min(r["lg"] for r in I) - 0.5, max(r["lg"] for r in I) + 0.5
        S = [r for r in S if lo <= r["lg"] <= hi]
    def fit(Ii, Si):
        X = np.array([[1.0, r["lg"] + 12.5, 1.0] for r in Ii] + [[1.0, r["lg"] + 12.5, 0.0] for r in Si]); y = np.array([r["D"] for r in Ii + Si])
        return np.linalg.lstsq(X, y, rcond=None)[0]
    a, b, c = fit(I, S); E = float(np.mean([r["D"] for r in I]))
    rng = np.random.default_rng(seed); bc, bE = [], []
    for _ in range(nb):
        Ii = [I[j] for j in rng.integers(0, len(I), len(I))]; Si = [S[j] for j in rng.integers(0, len(S), len(S))]
        bc.append(fit(Ii, Si)[2]); bE.append(np.mean([r["D"] for r in Ii]))
    sc, sE = float(np.std(bc)), float(np.std(bE))
    if sc > 0.20: cls = "NOT DIAGNOSTIC"
    elif E / sE >= 3 and abs(c) / sc < 2: cls = "SMALL-SYSTEM"
    elif E / sE < 2 and c / sc <= -3: cls = "SATELLITE-ONLY"
    elif E / sE >= 2 and c / sc <= -2: cls = "PARTIAL"
    else: cls = "UNDECIDED"
    return dict(N_I=len(I), N_S=len(S), b=float(b), c=float(c), se_c=sc, E=E, se_E=sE, cls=cls,
                iso=[dict(name=r["name"], lg=r["lg"], D=r["D"], Mg=r["Mg"], Ms2=r["Ms"] / 2, dmin=r["dmin"]) for r in I])

P("CFG874  all isolated LG dwarfs pooled, gas counted, vs satellites at matched g_bar" + (f"  [MUTATE {MUT}: isolated sigma {'x' if MUT == 'up' else '/'}1.45]" if MUT else ""))
RES = dict(lane="CFG874", mutate=MUT or None)
# ---- K1: gas zero, Ups 2 -> CFG860 d values for I0 + IG
z = {r["name"]: r for r in build("canonical", gas="zero", sig_mut=False)}
ref = {m["name"]: m["d"] for k in ("I0", "IG") for m in R860[k]}
dev = max(abs(z[n]["D"] - v) for n, v in ref.items()); RES["K1_maxdev"] = dev; RES["K1"] = dev < 1e-9
P(f"  K1 zero gas, Ups 2 vs CFG860 d (N {len(ref)}): max |dDelta| = {dev:.2e} -> {'PASS' if dev < 1e-9 else 'FAIL'}")
iso_names = sorted(r["name"] for r in z.values() if r["grp"] == "I")
P(f"  isolated (N {len(iso_names)}): {', '.join(iso_names)}")
P(f"  satellites S (all): {sum(r['grp'] == 'S' for r in z.values())}   SG (HI satellites, unused): {', '.join(r['name'] for r in z.values() if r['grp'] == 'SG')}")
for foot in ("canonical", "alt"):
    RES[foot] = {}
    runs = [("primary", dict(gas="disc"), {}), ("compact", dict(gas="compact"), {}), ("half (CFG860)", dict(gas="half"), {}),
            ("no gas", dict(gas="zero"), {}), ("all gas", dict(gas="full"), {}),
            ("Ups_SFH", dict(gas="disc", ups="SFH"), {}), ("strict >=500 kpc", dict(gas="disc"), dict(mindist=500.0)),
            ("Antlia B dropped", dict(gas="disc"), dict(drop=("Antlia B",))), ("sat M_V<=-6", dict(gas="disc"), dict(smv=-6.0)),
            ("full-range fit", dict(gas="disc"), dict(restrict=False)), ("+Leo A, SagDIG", dict(gas="disc"), dict(iso=("I", "DIRR")))]
    for tag, bk, ak in runs:
        r = analyse(build(foot, **bk), **ak); RES[foot][tag] = r
        graded = tag in ("primary", "compact", "half (CFG860)")
        P(f"\n  [{foot} | {tag}]  N_I {r['N_I']}  N_S {r['N_S']}  slope {r['b']:+.3f}  c = {r['c']:+.3f} +- {r['se_c']:.3f} ({r['c']/r['se_c']:+.1f} se)   "
          f"E = {r['E']:+.3f} +- {r['se_E']:.3f} ({r['E']/r['se_E']:+.1f} se)  -> {r['cls']}" + ("" if graded else "  (variant)"))
        if tag == "primary":
            for x in sorted(r["iso"], key=lambda q: q["lg"]):
                P(f"      {x['name']:17s} {x['dmin']:5.0f} kpc  log g_bar {x['lg']:+.2f}  Delta {x['D']:+.3f}  gas/stars in r12 {x['Mg']/x['Ms2']:.2f}")
cc, ca = RES["canonical"]["primary"]["cls"], RES["alt"]["primary"]["cls"]
overall = cc if cc == ca else "UNDECIDED"
brk = {RES[f][t]["cls"] for f in ("canonical", "alt") for t in ("primary", "compact", "half (CFG860)")}
flag = "GAS-SENSITIVE" if len(brk) > 1 else None
P(f"\n  CLASS (canonical {cc}; alt {ca}): {overall}" + (f" ({flag})" if flag else ""))
if MUT:
    ok = overall != ("SMALL-SYSTEM" if MUT == "down" else "SATELLITE-ONLY"); RES["mutate_ok"] = ok
    P(f"  MUTATE-{MUT}: {'statistic responds (allowed class)' if ok else 'TOOTHLESS (forbidden class)'}")
RES.update(cls=overall, flag=flag)
json.dump(RES, open(os.path.join(HERE, f"cfg874_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg874{SUF}.out"), "w").write("\n".join(OUT) + "\n")
