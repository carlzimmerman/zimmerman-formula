"""CFG860 -- is the dwarf excess tied to gas lost by STRIPPING?  Satellites (S) vs isolated gas-free (I0) vs isolated
gas-bearing (IG) dwarfs at matched g_bar.  Criteria: FROZEN_CRITERIA.md (219d4d5dc).  Part A (graded), Part R (reported), K1.
Delta as CFG852's delta_ups2 (Ups_V 2, Wolf, nu_e); fit Delta = a + b (lg g_bar + 12.5) + c0[I0] + cG[IG]; stratified bootstrap.
Run: python3 cfg860.py (CFG860_MUTATE=1 -> _MUTATE outputs).  Part E (Earth bound): cfg860_earth_bound.py.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, csv, json, math, ast, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG860_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # CFG828 / CFG852 values
nu_e = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))
def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}   # CFG852's set
R28J = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
R28 = {ft: {r["name"]: r for r in R28J[f"{ft}|nu_e"]["rows"]} for ft in ("canonical", "alt")}
NB, SEED, SAT = 2000, 860, 300.0

def delta(r, a0, gas=0.0):
    """CFG852 delta_ups2 with a0 as an argument; gas (Msun) is added to M* for the IG gas bracket only."""
    MV, s, rh = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    r12 = (4 / 3) * rh * PC; Ms = 2.0 * 10 ** (0.4 * (4.83 - MV)); gb = G * ((Ms + gas) / 2) * Msun / r12 ** 2
    return math.log10(3 * (s * 1e3) ** 2 / r12 / (gb * nu_e(gb / a0))), math.log10(gb)

# ---- sample (frozen): measured sigma (no upper limit), r_h, M_V; CFG852's rotating / gas-rich set excluded
SAMPLE, n_sig_ul = [], 0
for nm, r in LVD.items():
    if nm in EXCL: continue
    if fnum(r.get("vlos_sigma")) is None:
        n_sig_ul += fnum(r.get("vlos_sigma_ul")) is not None; continue
    if fnum(r.get("vlos_sigma_ul")) is not None: continue
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if rh is None or fnum(r.get("M_V")) is None: continue
    det, ul = fnum(r.get("mass_HI")), fnum(r.get("mass_HI_ul"))
    SAMPLE.append(dict(name=nm, host=r.get("host") or "-", dmw=fnum(r.get("distance_gc")), dm31=fnum(r.get("distance_m31")),
                       hi="det" if det is not None else ("ul" if ul is not None else "none"), lHI=det if det is not None else ul, row=r))

def group(s, cut):
    if s["dmw"] is None or s["dm31"] is None: return "no-distance"
    dmin = min(s["dmw"], s["dm31"])
    if dmin < SAT: return "SG" if s["hi"] == "det" else "S"
    if dmin < cut: return "gap"                       # between the 300 kpc satellite radius and a wider isolation cut: left out
    return {"det": "IG", "ul": "I0", "none": "I?"}[s["hi"]]

def build(foot, cut=300.0, ups="2", gas=False, drop=(), lgmax=None):
    rows = []
    for s in SAMPLE:
        grp = "dropped" if s["name"] in drop else group(s, cut)
        if ups == "SFH" and s["name"] in R28[foot]: d, lg, src = R28[foot][s["name"]]["delta"], R28[foot][s["name"]]["lgbar"], "SFH"
        else:
            gm = 1.33 * 10 ** s["lHI"] if (gas and grp == "IG") else 0.0
            (d, lg), src = delta(s["row"], A0[foot], gm), "2"
        if lgmax is not None and lg >= lgmax and grp in ("S", "I0", "IG"): grp = "lg-cut"
        rows.append(dict(name=s["name"], grp=grp, d=d, lg=lg, src=src))
    return rows

def fit(x, y, g):
    A = np.vstack([np.ones_like(x), x, (g == "I0") * 1.0, (g == "IG") * 1.0]).T
    return np.linalg.lstsq(A, y, rcond=None)[0]

def classify(N0, NG, c0, s0, cG, sG, ac0, sac0, acG, sacG):
    if N0 < 4 or NG < 4 or s0 > 0.20 or sG > 0.20: return "NOT DIAGNOSTIC"
    if c0 >= 2 * s0 or cG >= 2 * sG: return "OPPOSITE"
    if c0 <= -2 * s0 and cG <= -2 * sG: return "STRIPPING"
    if abs(c0) < 2 * s0 and cG <= -2 * sG: return "GAS LOSS, ANY ROUTE"
    if abs(c0) < 2 * s0 and abs(cG) < 2 * sG and ac0 >= 2 * sac0 and acG >= 2 * sacG: return "NOT GAS"
    return "INCONCLUSIVE"

def analyse(rows, sh0=0.0, shG=0.0):
    U = [r for r in rows if r["grp"] in ("S", "I0", "IG")]
    g = np.array([r["grp"] for r in U]); x = np.array([r["lg"] + 12.5 for r in U])
    y = np.array([r["d"] + (sh0 if r["grp"] == "I0" else 0.0) + (shG if r["grp"] == "IG" else 0.0) for r in U])
    N = {k: int((g == k).sum()) for k in ("S", "I0", "IG")}
    if min(N.values()) == 0: return dict(N=N, cls="NOT DIAGNOSTIC", note="empty group")
    a, b, c0, cG = fit(x, y, g); idx = {k: np.where(g == k)[0] for k in ("S", "I0", "IG")}
    rng = np.random.default_rng(SEED); B = []
    for _ in range(NB):
        ii = np.concatenate([idx[k][rng.integers(0, len(idx[k]), len(idx[k]))] for k in ("S", "I0", "IG")])
        B.append(fit(x[ii], y[ii], g[ii]))
    B = np.array(B); sd = B.std(axis=0); sac0, sacG = float((B[:, 0] + B[:, 2]).std()), float((B[:, 0] + B[:, 3]).std())
    mean = {k: float(y[g == k].mean()) for k in N}; mlg = {k: float(x[g == k].mean() - 12.5) for k in N}
    cls = classify(N["I0"], N["IG"], c0, sd[2], cG, sd[3], a + c0, sac0, a + cG, sacG)
    return dict(N=N, a=float(a), b=float(b), c0=float(c0), cG=float(cG), sa=float(sd[0]), sb=float(sd[1]), s0=float(sd[2]), sG=float(sd[3]),
                ac0=float(a + c0), sac0=sac0, acG=float(a + cG), sacG=sacG, mean=mean, mean_lg=mlg, cls=cls)

def line(lab, R):
    if "a" not in R: return f"  [{lab}] N {R['N']} -> {R['cls']} ({R.get('note', '')})"
    return (f"  [{lab}] N S/I0/IG {R['N']['S']}/{R['N']['I0']}/{R['N']['IG']}  b {R['b']:+.3f}  c0 {R['c0']:+.3f}+-{R['s0']:.3f}  "
            f"cG {R['cG']:+.3f}+-{R['sG']:.3f}  a+c0 {R['ac0']:+.3f}+-{R['sac0']:.3f}  a+cG {R['acG']:+.3f}+-{R['sacG']:.3f}  -> {R['cls']}")

P("CFG860  dwarf excess: stripped satellites vs isolated gas-free vs isolated gas-bearing at matched g_bar"
  + ("  [MUTATE]" if MUT else ""))
RES = dict(lane="CFG860", criteria_commit="219d4d5dc", mutate=MUT)
base = {ft: build(ft) for ft in ("canonical", "alt")}
BASE = {ft: analyse(base[ft]) for ft in ("canonical", "alt")}
real = BASE["canonical"]["cls"]

if MUT:
    P(line('real run, canonical', BASE['canonical']))
    M = {}
    for lab, s0, sG, want in (("(a) -0.4 dex on every I0 and IG Delta", -0.4, -0.4, "STRIPPING"), ("(b) -0.4 dex on IG only", 0.0, -0.4, "GAS LOSS, ANY ROUTE")):
        R = analyse(base["canonical"], s0, sG); bite = "did not bite by rule" if real == "NOT DIAGNOSTIC" else ("BITES" if R["cls"] == want else "DOES NOT BITE")
        R.update(want=want, outcome=bite); M[lab] = R
        P(line(lab, R)); P(f"      must class {want}: {bite}" + ("  (real run NOT DIAGNOSTIC: c values printed only)" if real == "NOT DIAGNOSTIC" else ""))
    RES.update(real=BASE["canonical"], mutate_runs=M, cls=real)
else:
    P(f"  sample: {len(SAMPLE)} LVD dwarfs with measured sigma, r_h, M_V (excluded {sorted(EXCL)}; {n_sig_ul} sigma upper limits not used)")
    P(f"  groups at the {SAT:.0f} kpc cut (distance_gc to MW, distance_m31 to M31; HI: det = mass_HI, ul = mass_HI_ul, log Msun)")
    cn, al = {r["name"]: r for r in base["canonical"]}, {r["name"]: r for r in base["alt"]}
    members = {}
    for k in ("S", "I0", "IG", "SG", "I?", "no-distance"):
        L = sorted([s for s in SAMPLE if cn[s["name"]]["grp"] == k], key=lambda s: cn[s["name"]]["lg"])
        members[k] = [dict(name=s["name"], host=s["host"], dmw=s["dmw"], dm31=s["dm31"], hi=s["hi"], lHI=s["lHI"], lg=cn[s["name"]]["lg"],
                           d=cn[s["name"]]["d"], d_alt=al[s["name"]]["d"]) for s in L]
        P(f"\n  {k} (N {len(L)})" + {"S": " stripped satellites", "I0": " isolated gas-free", "IG": " isolated gas-bearing",
                                      "SG": " satellites with HI (reported, not graded)", "I?": " isolated, no HI entry (left out)",
                                      "no-distance": " (left out)"}[k])
        if L: P("    name                host       d_MW   d_M31  HI      log g_bar  Delta(can)  Delta(alt)")
        for m in members[k]:
            P(f"    {m['name']:19s} {m['host']:8s} {m['dmw']:7.1f} {m['dm31']:7.1f}  {m['hi']:4s}{(m['lHI'] if m['lHI'] is not None else float('nan')):5.2f}"
              f"   {m['lg']:7.3f}    {m['d']:+.3f}      {m['d_alt']:+.3f}")
    RES["members"] = members
    P("\n  GRADED FIT (canonical a0 9.3603e-11, nu_e, Ups_V 2, 2000 stratified draws, seed 860)")
    R = BASE["canonical"]
    P(line("canonical", R))
    P("    group means: " + "  ".join(f"{k} Delta {R['mean'][k]:+.3f} at lg {R['mean_lg'][k]:.2f}" for k in ("S", "I0", "IG")) + f"   a {R['a']:+.3f}+-{R['sa']:.3f}")
    P(f"\n  CLASS: {real}")
    P("\n  REPORTED VARIANTS (not graded)")
    VAR = {}
    for ft in ("canonical", "alt"):
        for lab, kw in (("base", {}), ("cut 350 kpc", dict(cut=350.0)), ("cut 400 kpc", dict(cut=400.0)), ("Ups_SFH (CFG828 rows)", dict(ups="SFH")),
                        ("IG gas bracket (M*+1.33 M_HI)", dict(gas=True)), ("Antlia B dropped", dict(drop=("Antlia B",))),
                        ("log g_bar < -11.9", dict(lgmax=-11.9))):
            if ft == "canonical" and lab == "base": continue
            rows = build(ft, **kw); V = analyse(rows); key = f"{ft}|{lab}"; VAR[key] = V
            P(line(key, V))
            if "cut" in lab: P(f"      left out between 300 kpc and the cut: {', '.join(r['name'] for r in rows if r['grp'] == 'gap') or 'none'}")
            if lab.startswith("Ups_SFH"): P(f"      Ups_SFH rows used: {', '.join(r['name'] for r in rows if r['src'] == 'SFH' and r['grp'] in ('S', 'I0', 'IG'))}")
            if lab == "log g_bar < -11.9": P(f"      I0 kept: {', '.join(r['name'] for r in rows if r['grp'] == 'I0')};  IG kept: {', '.join(r['name'] for r in rows if r['grp'] == 'IG') or 'none'}")
    RES["variants"] = VAR
    # SG offset from the graded line
    a, b = R["a"], R["b"]; sg = [(m["name"], m["d"] - (a + b * (m["lg"] + 12.5))) for m in members["SG"]]
    P(f"\n  SG offset from the graded S line (canonical): " + ", ".join(f"{n} {o:+.3f}" for n, o in sg) + (f";  mean {np.mean([o for _, o in sg]):+.3f}" if sg else ""))
    RES["SG_offset"] = dict(rows={n: float(o) for n, o in sg}, mean=float(np.mean([o for _, o in sg])) if sg else None)
    # Cetus / Tucana cross-check vs CFG838's field values (CFG838 used CFG828's Ups_SFH rows)
    f838 = json.load(open(os.path.join(LANES, "CFG838_satellite_tides", "cfg838_results.json")))["field"]; sfh = {r["name"]: r for r in build("canonical", ups="SFH")}
    CT = {}
    for nm in ("Cetus", "Tucana"):
        CT[nm] = dict(ups2=cn[nm]["d"], ups_sfh=sfh[nm]["d"], cfg838=f838[nm], sfh_minus_838=sfh[nm]["d"] - f838[nm])
        P(f"  {nm}: Delta Ups 2 {cn[nm]['d']:+.3f} | Ups_SFH {sfh[nm]['d']:+.3f} vs CFG838 field {f838[nm]:+.3f} (diff {sfh[nm]['d'] - f838[nm]:+.1e}) "
          f"-> {'MATCH' if abs(sfh[nm]['d'] - f838[nm]) < 1e-9 else 'DIFFERS'}; Ups 2 - CFG838 {cn[nm]['d'] - f838[nm]:+.3f} dex (Ups and sigma source)")
    RES["cetus_tucana"] = CT
    # ---- K1
    src = ast.parse(open(os.path.join(LANES, "CFG852_gas_loss_metallicity", "cfg852.py")).read()); keep = []
    for n in src.body:
        if isinstance(n, ast.FunctionDef) and n.name in ("fnum", "delta_ups2"): keep.append(n)
        elif isinstance(n, ast.Assign):
            ids = {t.id for t in n.targets if isinstance(t, ast.Name)} | {e.id for t in n.targets if isinstance(t, ast.Tuple) for e in t.elts if isinstance(e, ast.Name)}
            if ids & {"G", "Msun", "PC", "a0", "nu", "law"}: keep.append(n)
    ns = {"math": math}; exec(compile(ast.Module(body=keep, type_ignores=[]), "cfg852_subset", "exec"), ns)
    d852, lg852 = ns["delta_ups2"](LVD["Draco"]); k1a = abs(d852 - cn["Draco"]["d"]) <= 1e-9 and abs(lg852 - cn["Draco"]["lg"]) <= 1e-9
    U = [r for r in base["canonical"] if r["grp"] in ("S", "I0", "IG")]; x = np.array([r["lg"] + 12.5 for r in U]); y = np.array([r["d"] for r in U])
    ls = np.linalg.lstsq(np.vstack([np.ones_like(x), x]).T, y, rcond=None)[0]; pf = np.polyfit(x, y, 1); k1b = abs(ls[1] - pf[0]) < 1e-9
    P(f"\n  K1 Draco Delta {cn['Draco']['d']:+.12f} vs CFG852 delta_ups2 {d852:+.12f} (diff {abs(d852 - cn['Draco']['d']):.1e}) -> {'PASS' if k1a else 'FAIL'};"
      f"  pooled slope (c0 = cG = 0) lstsq {ls[1]:.9f} vs polyfit {pf[0]:.9f} -> {'PASS' if k1b else 'FAIL'}")
    RES["K1"] = dict(draco=cn["Draco"]["d"], draco_cfg852=d852, draco_pass=bool(k1a), slope_lstsq=float(ls[1]), slope_polyfit=float(pf[0]), slope_pass=bool(k1b))
    # ---- Part R
    R50 = json.load(open(os.path.join(LANES, "CFG850_red_split_mstar_systematic", "cfg850_results.json")))["rows"]; PR = {}
    P("\n  PART R  isolated (B21) KiDS lenses, CFG850 rows with the +0.123 dex red M* correction (reported, no new statistic)")
    for ft in ("canonical", "alt"):
        q = R50[f"{ft}|0.123|0.0"]; PR[ft] = dict(A_red=q["A_red"], A_blue=q["A_blue"], z_colour=q["z_colour"])
        P(f"    [{ft}] A_red {q['A_red']:.3f} ({math.log10(q['A_red']):+.3f} dex)  A_blue {q['A_blue']:.3f} ({math.log10(q['A_blue']):+.3f} dex)  split {q['z_colour']:.1f} sigma")
    P("    scale caveat: lensing probes 30-300 kpc, the dwarf dispersions r_1/2 ~ 0.1-1 kpc; CFG851 found no single law across the two.")
    RES["partR"] = PR; RES["cls"] = real

sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg860_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg860{sfx}.out"), "w").write("\n".join(OUT) + "\n")
