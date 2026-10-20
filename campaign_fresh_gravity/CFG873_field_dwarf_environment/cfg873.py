"""CFG873 -- is the dwarf excess a SATELLITE property or a SMALL-SYSTEM property?  Criteria: FROZEN_CRITERIA.md (30dd0b297).
Five isolated field dwarfs vs MW/M31 satellites at matched g_bar, gas included via HI size-mass discs (Wang+16).
Run: python3 cfg873.py   (CFG873_MUTATE=up|down).  kappa = 1/2 FITTED; not theory closed."""
import os, json, math, csv, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG873_MUTATE", ""); assert MUT in ("", "up", "down")
SUF = f"_MUTATE_{MUT}" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
EXCL = {"WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}       # CFG828, unchanged
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
R28 = {r["name"]: r for r in json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"]}
def fl(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError): return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))):
        LVD[r["name"]] = dict(MV=fl(r.get("M_V")), rh=fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical")),
                              lHI=fl(r.get("mass_HI")), host=(r.get("host") or "").strip() or "field", s26=fl(r.get("vlos_sigma")))

def gas_in(lHI, r12_pc, rscale=1.0, root="large"):
    """Helium-corrected HI mass inside r12 (M_sun) for an exponential disc with Wang+16 R_HI (x rscale)."""
    if lHI is None: return 0.0, None
    MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3 * rscale            # pc
    lo, hi, Rs = 1e-3 * RHI, 10 * RHI, None                                             # solve Sigma(R_HI) = 1 Msun/pc^2
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(lo, hi, 4000); vals = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
    Rs = (max(roots) if root == "large" else min(roots)) if roots else RHI / 2      # script default: larger (extended) root; "small" = post-hoc compact-disc sensitivity
    x = r12_pc / Rs
    return 1.33 * MHI * (1 - (1 + x) * math.exp(-x)), dict(RHI=RHI, Rs=Rs, fallback=not roots, MHI=MHI)

def build(rscale=1.0, gas_mode="model", sig_leoT=None, root="large"):
    rows = []
    for nm, r in R27.items():
        if nm in EXCL: continue
        L = LVD[nm]; s = R24[nm]["so"]
        if nm == "Leo T" and sig_leoT: s = sig_leoT
        host = "field" if L["host"] == "field" else ("mw" if L["host"] == "mw" else "m31")
        if host == "field" and MUT: s = s * 1.45 if MUT == "up" else s / 1.45
        r12_pc = (4 / 3) * L["rh"]; r12 = r12_pc * PC
        Ms = r["ups"] * 10 ** (0.4 * (4.83 - L["MV"]))
        Mg_full = 1.33 * 10 ** L["lHI"] if L["lHI"] is not None else 0.0
        if gas_mode == "zero": Mg, info = 0.0, None
        elif gas_mode == "full": Mg, info = Mg_full, None
        else: Mg, info = gas_in(L["lHI"], r12_pc, rscale, root)
        rows.append(dict(name=nm, host=host, Ms=Ms, Mg_in=Mg, Mg_full=Mg_full, gas=info, r12_pc=r12_pc, sigma=s,
                         gbar=G * (Ms / 2 + Mg) * Msun / r12 ** 2, gobs=3 * (s * 1e3) ** 2 / r12))
    return rows

def stats(rows, a0, seed=873, nb=4000):
    for d in rows:
        d["lg"] = math.log10(d["gbar"]); d["D"] = math.log10(d["gobs"] / (d["gbar"] * float(nu_e(d["gbar"] / a0))))
    F = [d for d in rows if d["host"] == "field"]; S = [d for d in rows if d["host"] != "field"]
    def ref(f, Ss):
        for w in (0.4, 0.6):
            m = [s["D"] for s in Ss if abs(s["lg"] - f["lg"]) <= w]
            if len(m) >= 5: return float(np.mean(m)), w, len(m)
        return float("nan"), None, 0
    Ed = np.array([f["D"] for f in F]); refs = [ref(f, S) for f in F]; Di = Ed - np.array([x[0] for x in refs])
    rng = np.random.default_rng(seed); bE, bD = [], []
    for _ in range(nb):
        Fi = rng.integers(0, len(F), len(F)); Si = rng.integers(0, len(S), len(S)); Sb = [S[j] for j in Si]
        bE.append(Ed[Fi].mean())
        rr = [ref(F[j], Sb)[0] for j in Fi]
        if not any(math.isnan(x) for x in rr): bD.append(float(np.mean(Ed[Fi] - np.array(rr))))
    E, sE, D, sD = float(Ed.mean()), float(np.std(bE)), float(np.nanmean(Di)), float(np.std(bD))
    if sD > 0.20: cls = "NOT DIAGNOSTIC"
    elif E / sE >= 3 and abs(D) / sD < 2: cls = "SMALL-SYSTEM"
    elif E / sE < 2 and D / sD <= -3: cls = "SATELLITE-ONLY"
    elif E / sE >= 2 and D / sD <= -2: cls = "PARTIAL"
    else: cls = "UNDECIDED"
    sub = {}
    for tag, names in (("gas_free", ("Tucana", "Cetus")), ("HI_bearing", ("Leo T", "Phoenix", "Aquarius"))):
        idx = [i for i, f in enumerate(F) if f["name"] in names]
        sub[tag] = dict(E=float(Ed[idx].mean()), D=float(np.nanmean(Di[idx])))
    return dict(E=E, se_E=sE, D=D, se_D=sD, cls=cls, N_F=len(F), N_S=len(S), sub=sub,
                field=[dict(name=f["name"], lgbar=f["lg"], Delta=f["D"], ref=refs[i][0], win=refs[i][1], n_ref=refs[i][2],
                            Ms=f["Ms"], Mg_in=f["Mg_in"], Mg_full=f["Mg_full"], r12_pc=f["r12_pc"], sigma=f["sigma"]) for i, f in enumerate(F)],
                all_rows=[dict(name=d["name"], host=d["host"], lgbar=d["lg"], Delta=d["D"]) for d in rows],
                sat_mean_lowg=float(np.mean([s["D"] for s in S if s["lg"] < -12])))

P("CFG873  field dwarfs vs satellites at matched g_bar (gas included)" + (f"  [MUTATE {MUT}: field sigma {'x' if MUT == 'up' else '/'}1.45]" if MUT else ""))
RES = dict(lane="CFG873", mutate=MUT or None)
# ---- K1: zero gas reproduces CFG828 rows
z = build(gas_mode="zero"); stats(z, A0["canonical"], nb=10)
dev = max(abs(d["D"] - R28[d["name"]]["delta"]) for d in z if d["name"] in R28)
k1 = dev < 1e-9 if not MUT else (dev < 1e-9 or None)
P(f"  K1 zero-gas vs CFG828 per-dwarf Delta: max |dDelta| = {dev:.2e} over {sum(d['name'] in R28 for d in z)} dwarfs -> {'PASS' if dev < 1e-9 else ('n/a under MUTATE (field sigma changed)' if MUT else 'FAIL')}")
RES["K1_maxdev"] = dev
# ---- gas model per field dwarf
P("\n  gas model (field dwarfs): name  log M_HI  R_HI[pc]  R_s[pc]  r12[pc]  M*/2  M_gas,in  (M_gas total)")
for d in build():
    if d["host"] == "field":
        gi = d["gas"]
        P(f"    {d['name']:9s} " + (f"{math.log10(gi['MHI']):5.2f}  {gi['RHI']:7.0f}  {gi['Rs']:6.0f}{' (fallback)' if gi['fallback'] else ''}" if gi else "  gas-free (upper limit)       ")
          + f"  {d['r12_pc']:6.0f}  {d['Ms']/2:9.3e}  {d['Mg_in']:9.3e}  ({d['Mg_full']:.3e})")
# ---- primary + bracket, both footings
for foot in ("canonical", "alt"):
    a0 = A0[foot]; RES[foot] = {}
    for tag, kw in (("primary", dict()), ("RHIx2", dict(rscale=2.0)), ("RHI/2", dict(rscale=0.5)),
                    ("env_zero", dict(gas_mode="zero")), ("env_full", dict(gas_mode="full")), ("LeoT_sigma_LVD", dict(sig_leoT=LVD["Leo T"]["s26"])),
                    ("posthoc_compact_root", dict(root="small"))):
        r = stats(build(**kw), a0); RES[foot][tag] = r
        P(f"\n  [{foot} | {tag}]  N_F {r['N_F']}  N_S {r['N_S']}  E_F = {r['E']:+.3f} +- {r['se_E']:.3f} ({r['E']/r['se_E']:+.1f} se)   "
          f"D = {r['D']:+.3f} +- {r['se_D']:.3f} ({r['D']/r['se_D']:+.1f} se)   -> {r['cls']}" + ("" if tag in ("primary", "RHIx2", "RHI/2") else "   (info only)"))
        P(f"      subsets: gas-free E {r['sub']['gas_free']['E']:+.3f} D {r['sub']['gas_free']['D']:+.3f} | HI-bearing E {r['sub']['HI_bearing']['E']:+.3f} D {r['sub']['HI_bearing']['D']:+.3f}"
          f"   | satellites at g_bar<1e-12: mean Delta {r['sat_mean_lowg']:+.3f}")
        if tag == "primary":
            for f in r["field"]:
                P(f"      {f['name']:9s} log g_bar {f['lgbar']:+.2f}  Delta {f['Delta']:+.3f}  satellite ref {f['ref']:+.3f} (+-{f['win']} dex, n {f['n_ref']})  D_i {f['Delta']-f['ref']:+.3f}")
c_can, c_alt = RES["canonical"]["primary"]["cls"], RES["alt"]["primary"]["cls"]
overall = c_can if c_can == c_alt else "UNDECIDED"
brk = {RES[f][t]["cls"] for f in ("canonical", "alt") for t in ("primary", "RHIx2", "RHI/2")}
flag = " (GAS-SENSITIVE)" if len(brk) > 1 else ""
P(f"\n  CLASS (canonical {c_can}; alt {c_alt}): {overall}{flag}")
if MUT:
    ok = (overall != "SMALL-SYSTEM") if MUT == "down" else (overall != "SATELLITE-ONLY")
    P(f"  MUTATE-{MUT} check: {'statistic responds (allowed class)' if ok else 'TOOTHLESS (forbidden class)'}")
    RES["mutate_ok"] = ok
RES.update(cls=overall, flag=flag.strip(" ()") or None)
json.dump(RES, open(os.path.join(HERE, f"cfg873_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg873{SUF}.out"), "w").write("\n".join(OUT) + "\n")
