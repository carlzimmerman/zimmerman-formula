"""CFG875 -- does the dwarf excess fade with host distance at fixed g_bar?  Criteria: FROZEN_CRITERIA.md (bdc023e85).
Estimators identical to CFG874's primary.  Run: python3 cfg875.py  (CFG875_MUTATE=inject|shuffle).  kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG875_MUTATE", ""); assert MUT in ("", "inject", "shuffle"); SUF = f"_MUTATE_{MUT}" if MUT else ""; OUT = []
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
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R874 = json.load(open(os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874_results.json")))

def gas_in(lHI, r12_pc, mode="disc"):                    # = CFG874
    if lHI is None or mode == "zero": return 0.0
    Mg = 1.33 * 10 ** lHI; MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = max(roots) if roots else RHI / 2; x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))

SAMPLE = []
for nm, r in LVD.items():
    if nm in EXCL: continue
    s = fnum(r.get("vlos_sigma"))
    if s is None or fnum(r.get("vlos_sigma_ul")) is not None: continue
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")); MV = fnum(r.get("M_V"))
    dmw, dm31 = fnum(r.get("distance_gc")), fnum(r.get("distance_m31"))
    if rh is None or MV is None or dmw is None or dm31 is None: continue
    det = fnum(r.get("mass_HI")); dmin = min(dmw, dm31)
    SAMPLE.append(dict(name=nm, grp="I" if dmin >= 300 else ("S" if det is None else "SG"), side="mw" if dmw <= dm31 else "m31",
                       s=s, rh=rh, MV=MV, lHI=det, d=dmin))

def build(foot, gas="disc", ups="2"):
    a0 = A0[foot]; rows = []
    for d in SAMPLE:
        r12_pc = (4 / 3) * d["rh"]; r12 = r12_pc * PC
        U = R27[d["name"]]["ups"] if (ups == "SFH" and d["name"] in R27) else 2.0
        Ms = U * 10 ** (0.4 * (4.83 - d["MV"])); gb = G * (Ms / 2 + gas_in(d["lHI"], r12_pc, gas)) * Msun / r12 ** 2
        rows.append(dict(d, lg=math.log10(gb), D=math.log10(3 * (d["s"] * 1e3) ** 2 / r12 / (gb * nu_e(gb / a0)))))
    return rows

ISO_LG = [r["lg"] for r in build("canonical") if r["grp"] == "I"]; LO, HI = min(ISO_LG) - 0.5, max(ISO_LG) + 0.5

def ranks(x):
    o = np.argsort(x); r = np.empty(len(x)); r[o] = np.arange(len(x)); return r
def analyse(rows, window=True, keep=lambda r: True, step=False, seed=875, nb=4000):
    U = [r for r in rows if keep(r) and (not window or LO <= r["lg"] <= HI)]
    lg = np.array([r["lg"] + 12.5 for r in U]); ld = np.log10([r["d"] for r in U]) - 2.5; D = np.array([r["D"] for r in U])
    if MUT == "inject": D = D - 0.4 * ld
    if MUT == "shuffle": ld = np.random.default_rng(875).permutation(ld)
    xk = (ld >= math.log10(300) - 2.5).astype(float) if step else ld
    X = np.column_stack([np.ones(len(U)), lg, xk])
    beta = np.linalg.lstsq(X, D, rcond=None)[0]; rng = np.random.default_rng(seed); bk = []
    for _ in range(nb):
        i = rng.integers(0, len(U), len(U)); bk.append(np.linalg.lstsq(X[i], D[i], rcond=None)[0][2])
    k, sk = float(beta[2]), float(np.std(bk))
    rD, rd, rg = ranks(D), ranks(xk), ranks(lg)                                  # partial Spearman (ranks, g_bar removed)
    res = lambda y: y - np.column_stack([np.ones(len(U)), rg]) @ np.linalg.lstsq(np.column_stack([np.ones(len(U)), rg]), y, rcond=None)[0]
    rho = float(np.corrcoef(res(rD), res(rd))[0, 1])
    if sk > 0.20: cls = "NOT DIAGNOSTIC"
    elif k / sk <= -3: cls = "ENVIRONMENTAL"
    elif k / sk <= -2: cls = "WEAK TREND"
    elif abs(k) / sk < 2 and k - 2 * sk > -0.20: cls = "NO TREND"
    elif k / sk >= 2: cls = "OPPOSITE"
    else: cls = "UNDECIDED"
    return dict(N=len(U), N_I=sum(r["grp"] == "I" for r in U), b=float(beta[1]), k=k, se_k=sk, rho=rho, cls=cls,
                dmin=float(min(r["d"] for r in U)), dmax=float(max(r["d"] for r in U)))

P("CFG875  dwarf excess vs host distance at fixed g_bar" + (f"  [MUTATE {MUT}]" if MUT else ""))
RES = dict(lane="CFG875", mutate=MUT or None, window=[LO, HI])
b = {r["name"]: r for r in build("canonical")}
ref = {x["name"]: x["D"] for x in R874["canonical"]["primary"]["iso"]}
dev = max(abs(b[n]["D"] - v) for n, v in ref.items()); RES["K1_maxdev"] = dev
P(f"  K1 isolated Delta vs CFG874 primary (N {len(ref)}): max |dDelta| = {dev:.2e} -> {'PASS' if dev < 1e-9 else 'FAIL'}")
P(f"  log g_bar window [{LO:.2f}, {HI:.2f}] (CFG874's)")
for foot in ("canonical", "alt"):
    RES[foot] = {}
    runs = [("primary", dict(), dict()),
            ("satellites only (<300 kpc)", dict(), dict(keep=lambda r: r["d"] < 300)),
            ("M_V <= -6", dict(), dict(keep=lambda r: r["MV"] <= -6)),
            ("MW satellites + isolated", dict(), dict(keep=lambda r: r["grp"] == "I" or r["side"] == "mw")),
            ("M31 satellites + isolated", dict(), dict(keep=lambda r: r["grp"] == "I" or r["side"] == "m31")),
            ("Ups_SFH", dict(ups="SFH"), dict()), ("no gas", dict(gas="zero"), dict()),
            ("full g_bar range", dict(), dict(window=False)), ("step at 300 kpc", dict(), dict(step=True))]
    for tag, bk, ak in runs:
        r = analyse(build(foot, **bk), **ak); RES[foot][tag] = r
        unit = "(step)" if tag.startswith("step") else "per dex"
        P(f"  [{foot} | {tag}]  N {r['N']} (isolated {r['N_I']}; d {r['dmin']:.0f}-{r['dmax']:.0f} kpc)  b {r['b']:+.3f}  "
          f"k = {r['k']:+.3f} +- {r['se_k']:.3f} {unit} ({r['k']/r['se_k']:+.1f} se)  partial rho {r['rho']:+.2f}  -> {r['cls']}" + ("" if tag == "primary" else "  (variant)"))
cc, ca = RES["canonical"]["primary"]["cls"], RES["alt"]["primary"]["cls"]; overall = cc if cc == ca else "UNDECIDED"
P(f"\n  CLASS (canonical {cc}; alt {ca}): {overall}")
if MUT:
    ok = (overall == "ENVIRONMENTAL") if MUT == "inject" else (overall not in ("ENVIRONMENTAL", "WEAK TREND"))
    RES["mutate_ok"] = ok; P(f"  MUTATE-{MUT}: {'control behaves as required' if ok else 'CONTROL FAILED'}")
RES["cls"] = overall
json.dump(RES, open(os.path.join(HERE, f"cfg875_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg875{SUF}.out"), "w").write("\n".join(OUT) + "\n")
