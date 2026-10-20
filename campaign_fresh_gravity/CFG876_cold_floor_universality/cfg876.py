"""CFG876 -- is the dwarfs' cold component (CFG870) universal?  Out-of-sample large dwarfs, no refit.
Criteria: FROZEN_CRITERIA.md (21fab6d76).  Run: python3 cfg876.py  (CFG876_MUTATE=halve).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG876_MUTATE", ""); assert MUT in ("", "halve"); SUF = "_MUTATE_halve" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; RC = 104.0
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
def fnum(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError): return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
R870 = json.load(open(os.path.join(LANES, "CFG870_cored_component_joint", "cfg870_results.json")))
R28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
R59 = json.load(open(os.path.join(LANES, "CFG859_extra_speed_vs_ufds", "cfg859_results.json")))
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
VX = {f: R870[f]["Vx"] for f in ("canonical", "alt")}

def gas_in(lHI, r12_pc):                                   # CFG874 primary (extended root)
    if lHI is None: return 0.0
    Mg = 1.33 * 10 ** lHI; MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = max(roots) if roots else RHI / 2; x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))

def pred(nm, a0, ups, Vx, gas=True, cap=False):
    L = LVD[nm]; rh_pc = fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical")); r12_pc = (4 / 3) * rh_pc; r12 = r12_pc * PC
    Ms = ups * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); Mg = gas_in(fnum(L.get("mass_HI")), r12_pc) if gas else 0.0
    gN = G * (Ms / 2 + Mg) * Msun / r12 ** 2; sl2 = float(gN * nu(gN / a0)) * r12 / 3 / 1e6        # (km/s)^2
    fc = r12_pc ** 2 / (r12_pc ** 2 + RC ** 2); sx2 = Vx ** 2 * fc / 3
    if cap:
        Mcap = 53.64 * (Ms + 1.33 * 10 ** fnum(L["mass_HI"]) if fnum(L.get("mass_HI")) is not None else Ms)
        sx2 = min(sx2, G * Mcap * Msun / (3 * r12) / 1e6)
    return math.sqrt(sl2 + sx2), math.sqrt(sl2), r12_pc

P("CFG876  universality of the cored cold component (CFG870, no refit) on large out-of-sample dwarfs" + ("  [MUTATE: sigma_obs x 0.5]" if MUT else ""))
RES = dict(lane="CFG876", mutate=MUT or None, Vx=VX, rc=RC)
# ---- K1: reproduce CFG870 T2
for foot in ("canonical", "alt"):
    rows = R28[f"{foot}|nu_e"]["rows"]; host = lambda nm: LVD[nm].get("host") or "field"
    oth = [(r["name"], R24[r["name"]]["so"], R27[r["name"]]["ups"]) for r in rows if host(r["name"]) in ("m_031", "field")]
    e2 = float(np.mean([math.log(so / pred(nm, A0[foot], ups, VX[foot], gas=False)[0]) for nm, so, ups in oth]))
    dev = abs(e2 - R870[foot]["m31_field_E"]); RES[f"K1_{foot}"] = dev
    P(f"  K1 [{foot}] CFG870 T2 E reproduced: {e2:+.12f} vs {R870[foot]['m31_field_E']:+.12f}  |diff| {dev:.1e} -> {'PASS' if dev < 1e-9 else 'FAIL'}")
used = {r["name"] for r in R28["canonical|nu_e"]["rows"]} | set(R59["canonical|secondary (literature sigma)"]["names"])
SAMP = []
for nm, r in LVD.items():
    if nm in used or nm in EXCL: continue
    s = fnum(r.get("vlos_sigma"))
    if s is None or fnum(r.get("vlos_sigma_ul")) is not None: continue
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if rh is None or fnum(r.get("M_V")) is None: continue
    SAMP.append(dict(name=nm, host=r.get("host") or "field", s=s * (0.5 if MUT else 1.0), em=fnum(r.get("vlos_sigma_em")) or 0.2 * s,
                     ep=fnum(r.get("vlos_sigma_ep")) or 0.2 * s, r12=(4 / 3) * rh))
B = [d for d in SAMP if d["r12"] >= 312]; SM = [d for d in SAMP if d["r12"] < 312]
P(f"  out-of-sample dwarfs: {len(SAMP)}; primary B (r12 >= 312 pc): {len(B)}; small: {len(SM)}")

def score(group, foot, Vx, ups=2.0, cap=False, nb=4000):
    a0 = A0[foot]; eps, rows = [], []
    for d in group:
        sp, sl, r12 = pred(d["name"], a0, ups, Vx, cap=cap); sp1 = pred(d["name"], a0, 1.0, Vx, cap=cap)[0]
        e = d["ep"] if d["s"] < sp1 else d["em"]; z1 = (d["s"] - sp1) / e
        eps.append(math.log(d["s"] / sp)); rows.append(dict(name=d["name"], host=d["host"], r12=r12, sigma=d["s"], pred=sp, law=sl, pred_ups1=sp1, z1=z1))
    eps = np.array(eps); rng = np.random.default_rng(876); bs = [rng.choice(eps, len(eps)).mean() for _ in range(nb)]
    E, sE = float(eps.mean()), float(np.std(bs)); nf = sum(r["z1"] <= -3 for r in rows)
    if abs(E) / sE < 2 and nf < 2: cls = "UNIVERSAL HOLDS"
    elif E / sE <= -3 or nf >= 2: cls = "BROKEN"
    elif E / sE >= 3: cls = "UNDER-PREDICTS"
    else: cls = "UNDECIDED"
    return dict(N=len(group), E=E, se_E=sE, N_fail=nf, cls=cls, rows=rows)

for foot in ("canonical", "alt"):
    RES[foot] = {}
    for tag, grp, kw in (("primary B", B, dict(Vx=VX[foot])), ("law alone (B)", B, dict(Vx=0.0)), ("supply-capped (B)", B, dict(Vx=VX[foot], cap=True)),
                         ("MW only (B)", [d for d in B if d["host"] == "mw"], dict(Vx=VX[foot])),
                         ("M31 only (B)", [d for d in B if d["host"] == "m_031"], dict(Vx=VX[foot])), ("small (r12<312)", SM, dict(Vx=VX[foot]))):
        r = score(grp, foot, **kw); RES[foot][tag] = r
        P(f"\n  [{foot} | {tag}]  N {r['N']}  E = {r['E']:+.3f} +- {r['se_E']:.3f} ({r['E']/r['se_E']:+.1f} se)  N_fail(z<=-3 @Ups1) {r['N_fail']}  -> {r['cls']}"
          + ("" if tag == "primary B" else "  (reported)"))
        if tag in ("primary B",) or (tag == "supply-capped (B)" and foot == "canonical"):
            for x in sorted(r["rows"], key=lambda q: -q["r12"]):
                P(f"      {x['name']:17s} {x['host']:6s} r12 {x['r12']:5.0f} pc  sigma {x['sigma']:5.2f}  pred {x['pred']:5.2f} (law {x['law']:4.2f}; Ups1 {x['pred_ups1']:5.2f})  z@Ups1 {x['z1']:+5.1f}")
cc, ca = RES["canonical"]["primary B"]["cls"], RES["alt"]["primary B"]["cls"]; overall = cc if cc == ca else "UNDECIDED"
P(f"\n  CLASS (canonical {cc}; alt {ca}): {overall}")
if MUT: RES["mutate_ok"] = overall == "BROKEN"; P(f"  MUTATE-halve: {'control bites (BROKEN)' if overall == 'BROKEN' else 'CONTROL FAILED'}")
RES["cls"] = overall
json.dump(RES, open(os.path.join(HERE, f"cfg876_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg876{SUF}.out"), "w").write("\n".join(OUT) + "\n")
