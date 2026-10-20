"""CFG919 -- is the baryons' kinematic state (pressure vs rotation support) the selector of the law's excesses?
Criteria: FROZEN_CRITERIA.md (8d34dc761, committed alone before this script); AMENDMENT_A1.md (5c9edd07b, POST HOC after the frozen
INJECT I1 failed, before the main run): C1 comparison clause; every class reported AS FROZEN and UNDER A1.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg919.py      (CFG919_MUTATE=shuffle|inject -> separate outputs named by mode).
Inputs: CFG914's input section exec'd read-only (83 LVD dwarfs of CFG880, eRASS1 shear stack of CFG687, 31 globulars of
CFG883, with CFG914's own K-checks); this lane's own SPARC and B21 loaders (checked equal to CFG914's arrays); Baumgardt GC
ARot/sigma0; SPARC Table 1 V_flat.  K-tests against committed CFG828 / CFG829 / CFG849 outputs.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, csv, json, math, re, glob, time, resource, warnings, contextlib, builtins
import numpy as np
from scipy.stats import chi2 as CHI2, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG919_MUTATE", ""); assert MUT in ("", "shuffle", "inject"); SUF = f"_MUTATE_{MUT}" if MUT else ""
for _e in ("CFG914_MUTATE", "CFG880_MUTATE", "CFG829_MUTATE", "CFG850_MUTATE", "CFG883_MUTATE", "CFG828_MUTATE",
           "CFG849_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def J(*p): return json.load(builtins.open(os.path.join(LANES, *p)))

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
LN10 = math.log(10.0)
FLOOR0, FLOOR_V6 = 0.05 * LN10, 0.10 * LN10                 # 0.05 / 0.10 dex in g, in E units
GRID = np.arange(-20.0, 10.0001, 0.5)                        # CFG914's fixed 0.5-dex edges
LWIN = (10 ** -13.3, 10 ** -10.9)                            # CFG914's lens window
CLASSES = ("DW", "SS", "SL", "LD", "LS", "CL", "GC")
CNAME = {"DW": "dwarfs (83 LVD, CFG880)", "SS": "SPARC small (Mb<=3e9)", "SL": "SPARC large", "LD": "lenses disc (n<2)",
         "LS": "lenses sph (n>2)", "CL": "eRASS1 clusters", "GC": "globulars (31, CFG883)"}
E_C1_ABS = math.log(10 ** 0.15)                              # 0.345: C1 absolute excess level (0.15 dex)
RES = dict(lane="CFG919", criteria="8d34dc761", amendment_A1="5c9edd07b", mutate=MUT or None, checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)

P("CFG919  pressure-support selector H-KIN: does ONE kinematic measure order the excess E = ln(g_obs/g_pred) at matched g_bar?"
  + (f"   [MUTATE {MUT}]" if MUT else ""))
P("  primary f_P = 3 sigma^2/(v^2 + 3 sigma^2); alternative f_sph = pressure-supported mass fraction; kappa = 1/2 FITTED")

# =====================================================================================================================  K4
P("\n=== K-stage")
F914 = os.path.join(LANES, "CFG914_common_density_threshold", "cfg914.py")
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG919 refuses to write {file!r} from re-executed committed code")
    return builtins.open(file, mode, *a, **k)
_src = builtins.open(F914).read(); _stop = _src.index("def bins_persystem(")
N914 = {"__file__": F914, "__name__": "cfg914_inputs_ro", "open": _ro_open}
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_src[:_stop], F914, "exec"), N914)
for _l in _buf.getvalue().splitlines():
    if "[PASS]" in _l or "[FAIL]" in _l or "inputs loaded" in _l or _l.strip().startswith("SPARC:"):
        P("    cfg914> " + _l.strip())
_chk = N914["RES"]["checks"]
_need = ("K1 ", "K1b ", "K2a ", "K2b ", "K3 ", "K3b ", "K4a ", "K4b ", "K5 ")
_have = [n for n in _chk if n.startswith(_need)]
KOK = [check("K4 CFG914 input section exec'd read-only: all its input checks pass", len(_have) == 9 and all(v["ok"] for v in _chk.values()),
             f"{sum(v['ok'] for v in _chk.values())}/{len(_chk)} pass ({', '.join(n.split(' ')[0] for n in _have)})")]
DWR, GCR, N880 = N914["DWR"], N914["GCR"], N914["N880"]
CD, CW, CLP, CLR, PATCH, NCL = N914["CD"], N914["CW"], N914["CLP"], N914["CLR"], N914["PATCH"], N914["NCL"]

# =====================================================================================================================  own SPARC loader (K1 + main)
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
nu_e12 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
nu_e15 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_s12 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-12)))
QG = {}
for l in builtins.open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: QG[v[0]] = dict(inc=float(v[5]), q=int(v[17]), Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9, Vflat=float(v[15]))
        except ValueError: pass
SP = dict(gal=[], R=[], gb=[], go=[], V=[], Vg=[], Vd=[], Vb=[])
for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", ""); q_ = QG.get(name)
    inc, q = (q_["inc"], q_["q"]) if q_ else (0, 3)
    if q > 2 or inc < 30: continue
    for l in builtins.open(fn):
        if l.startswith("#") or not l.strip(): continue
        R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
        if V <= 0 or R <= 0 or eV / V >= 0.10: continue
        g_b = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
        if g_b <= 0: continue
        for k_, x_ in (("gal", name), ("R", R), ("gb", g_b), ("go", V * V * 1e6 / (R * KPC)), ("V", V), ("Vg", Vg), ("Vd", Vd), ("Vb", Vb)):
            SP[k_].append(x_)
for k_ in SP: SP[k_] = np.array(SP[k_])
_eq_sp = (np.array_equal(SP["gb"], N914["SP"]["gb"]) and np.array_equal(SP["go"], N914["SP"]["go"])
          and np.array_equal(SP["gal"], N914["SP"]["gal"]))
check("K-extra own SPARC loader == CFG914 SP arrays (bit-for-bit)", _eq_sp, f"{len(SP['gb'])} points, {len(set(SP['gal']))} galaxies")

# =====================================================================================================================  K1 CFG828
def fn828(x):
    try: return float(x)
    except Exception: return None
R27 = J("CFG827_dwarf_age_sfh_ml", "cfg827_results.json")["rows"]; R24 = J("CFG824_dwarf_age_fossil", "cfg824_results.json")["rows"]
LVD828 = {}
for f_ in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(builtins.open(os.path.join(REPO, "real_research", "data", "dsph", f_))):
        LVD828[r["name"]] = (fn828(r.get("M_V")), fn828(r.get("rhalf_sph_physical")) or fn828(r.get("rhalf_physical")))
EXCL828 = {"WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
DW828 = []
for nm, r in R27.items():
    if nm in EXCL828: continue
    MV, rh = LVD828[nm]; s = R24[nm]["so"]; r12 = (4 / 3) * rh * PC; Ms = r["ups"] * 10 ** (0.4 * (4.83 - MV))
    DW828.append(dict(name=nm, gbar=G * (Ms / 2) * MSUN / r12 ** 2, gobs=3 * (s * 1e3) ** 2 / r12))
R828 = J("CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")
rng828 = np.random.default_rng(828); K1 = {}; k1d = []
for foot in FOOTS:
    for kn, nu in (("nu_e", nu_e12), ("nu_simple", nu_s12)):
        if foot == "alt" and kn == "nu_simple": continue
        a0 = A0[foot]; dS = np.log10(SP["go"] / (SP["gb"] * nu(SP["gb"] / a0))); lg = np.log10(SP["gb"]); rows = []
        for d in DW828:
            dd = math.log10(d["gobs"] / (d["gbar"] * float(nu(d["gbar"] / a0)))); w = np.abs(lg - math.log10(d["gbar"])) <= 0.15
            rows.append(dict(delta=dd, dS=float(np.median(dS[w])) if w.sum() >= 20 else None))
        inr = [r for r in rows if r["dS"] is not None]; D = np.array([r["delta"] - r["dS"] for r in inr])
        boot = [rng828.choice(D, len(D)).mean() for _ in range(2000)] if len(D) else [0]
        out_ = [r["delta"] for r in rows if r["dS"] is None]
        K1[f"{foot}|{kn}"] = dict(N_in=len(inr), mean_D=float(D.mean()), se_D=float(np.std(boot)), sparc_median_all=float(np.median(dS)),
                                  out_of_range_mean_delta=float(np.mean(out_)) if out_ else None)
for key in ("canonical|nu_e", "alt|nu_e"):
    for q in ("N_in", "mean_D", "se_D", "sparc_median_all", "out_of_range_mean_delta"):
        k1d.append(abs(K1[key][q] - R828[key][q]))
c828 = K1["canonical|nu_e"]
KOK.append(check("K1 CFG828 reproduced (own code; N_in, mean D, se D, SPARC median, out-of-range mean; canonical+alt nu_e)", max(k1d) <= 1e-9,
                 f"max |diff| {max(k1d):.1e}; canonical: N_in {c828['N_in']}, D {c828['mean_D']:+.3f}+-{c828['se_D']:.3f} dex, "
                 f"out-of-range mean {c828['out_of_range_mean_delta']:+.3f}, SPARC median {c828['sparc_median_all']:+.3f}"))

# =====================================================================================================================  own B21 loader (K2, K3 + main)
B21 = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
G_pc, PCm = 4.52e-30, 3.086e16
def b21_load(esd, cov, binmin=None):
    d = np.loadtxt(os.path.join(B21, esd)); gb, esdt, bias = d[:, 0], d[:, 1], d[:, 4]
    go = 4 * G_pc * esdt / bias * PCm
    c = np.loadtxt(os.path.join(B21, cov)); n = len(gb); C = np.zeros((n, n))
    sel = c if binmin is None else c[(np.isclose(c[:, 0], binmin)) & (np.isclose(c[:, 1], binmin))]
    def idx(x):
        k = int(np.argmin(np.abs(gb / x - 1))); return k if abs(gb[k] / x - 1) < 1e-3 else None
    for row in sel:
        i, j = idx(row[2]), idx(row[3])
        if i is not None and j is not None: C[i, j] = row[4] / row[6]
    return gb, go, C * (4 * G_pc * PCm) ** 2
def gls_amp(gb, go, C, gl, win):
    m = (gb >= win[0]) & (gb < win[1])
    if m.sum() < 2: return None
    Ci = np.linalg.inv(C[np.ix_(m, m)]); a = gl[m] @ Ci @ gl[m]
    return dict(A=float(gl[m] @ Ci @ go[m] / a), sA=float(a ** -0.5), n=int(m.sum()))
LF = {"blue": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
      "red": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
      "disc": ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
      "sph": ("Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0)}
LD_ = {k: b21_load(*v) for k, v in LF.items()}
_eq_l = all(np.array_equal(LD_[k][i], N914["LDAT"][k][i]) for k in LF for i in range(3))
check("K-extra own B21 loader == CFG914 LDAT (blue, red, disc, sph; bit-for-bit)", _eq_l, "4 lens sets")
W829 = (10 ** -13.3, 10 ** -11.9)
R829 = J("CFG829_lensing_low_g_vs_dwarf_excess", "cfg829_results.json"); k2d = []; K2 = {}
for foot in FOOTS:
    for col, key in (("blue", "blue (u-r<2.5)"), ("red", "red (u-r>2.5)")):
        gb, go, C = LD_[col]; a = gls_amp(gb, go, C, gb * nu_e15(gb / A0[foot]), W829); K2[f"{foot}|{col}"] = a
        ref = R829[f"{foot}|nu_e|{key}"]["window"]; k2d += [abs(a["A"] - ref["A"]), abs(a["sA"] - ref["sA"])]
b = K2["canonical|blue"]; cls829 = "LAW HOLDS AT LOW g" if (abs(b["A"] - 1) < 2 * b["sA"] and (10 ** 0.44 - b["A"]) >= 3 * b["sA"]) else "OTHER"
KOK.append(check("K2 CFG829 reproduced (own B21 loader + GLS; blue/red window A, sA, both footings; class)", max(k2d) <= 1e-9 and cls829 == R829["cls"],
                 f"max |diff| {max(k2d):.1e}; canonical blue A {b['A']:.3f}+-{b['sA']:.3f}, red A {K2['canonical|red']['A']:.3f}; class '{cls829}'"))
R849 = J("CFG849_structure_vs_colour_lensing", "cfg849_results.json"); k3d = []
for foot in FOOTS:
    for col, key in (("disc", "disc n<2"), ("sph", "sph n>2")):
        gb, go, C = LD_[col]; a = gls_amp(gb, go, C, gb * nu_e15(gb / A0[foot]), W829)
        k3d += [abs(a["A"] - R849[foot]["A"][key][0]), abs(a["sA"] - R849[foot]["A"][key][1])]
KOK.append(check("K3 CFG849 Sersic disc/sph window A, sA reproduced (both footings)", max(k3d) <= 1e-9,
                 f"max |diff| {max(k3d):.1e}; canonical disc {R849['canonical']['A']['disc n<2'][0]:.3f}, sph {R849['canonical']['A']['sph n>2'][0]:.3f}"))

# =====================================================================================================================  K5 Baumgardt kinematics
def num1(s):
    s = s.strip()
    if not s or s in ("—", "-"): return None
    if "·" in s:
        a, e = s.split("·"); return float(a.split("+-")[0]) * 10 ** int(e.strip()[2:])
    return float(s.split("+-")[0])
GKIN = {}
for l in builtins.open(os.path.join(REPO, "real_research", "data", "globular_clusters", "baumgardt_gc_parameters.tsv")):
    if l.startswith("#") or l.startswith("ClusterName"): continue
    c = l.rstrip("\n").split("\t"); nm = re.split(r"\s{2,}", c[0].strip())[0]
    try: GKIN[nm] = dict(sig0=num1(c[21]), arot=num1(c[25]))
    except (IndexError, ValueError): GKIN[nm] = dict(sig0=None, arot=None)
def fP(vs): return 3.0 / (vs * vs + 3.0)                     # f_P from v/sigma
gc_names = [r["name"] for r in GCR["canonical"]]
gc_vs = {nm: (GKIN[nm]["arot"] / GKIN[nm]["sig0"]) if (nm in GKIN and GKIN[nm]["arot"] is not None and GKIN[nm]["sig0"]) else None for nm in gc_names}
_fgc = [fP(v) for v in gc_vs.values() if v is not None]
KOK.append(check("K5 Baumgardt ARot/sigma0 parse (47 Tuc 5.00/11.9) and every globular f_P in (0, 1]",
                 GKIN.get("NGC 104", {}).get("arot") == 5.00 and GKIN["NGC 104"]["sig0"] == 11.9 and all(0 < x <= 1 for x in _fgc),
                 f"{len(_fgc)}/{len(gc_names)} safe globulars with ARot and sigma0; f_P {min(_fgc):.3f}..{max(_fgc):.3f}, "
                 f"median v/sigma {np.median([v for v in gc_vs.values() if v is not None]):.3f}"))
K_ALL = all(KOK)
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
if not K_ALL:
    P("  A K-test failed: per FROZEN_CRITERIA section 8 the lane stops; no class is reported.")
    RES["class"] = None
    json.dump(RES, builtins.open(os.path.join(HERE, f"cfg919_results{SUF}.json"), "w"), indent=1, default=float)
    builtins.open(os.path.join(HERE, f"cfg919{SUF}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)

# =====================================================================================================================  members and measures
# dwarfs: HI-bearing flag and f_sph from CFG880's own gas accounting
DWM = {}
for f in FOOTS:
    d = DWR[f]; hi, fs = [], []
    for nm, r12pc in zip(d["names"], d["r12"]):
        L = N880["LVD"][nm]; Ms = 2.0 * 10 ** (0.4 * (4.83 - N880["fnum"](L["M_V"])))
        Mg = N880["gas_in"](N880["fnum"](L.get("mass_HI")), r12pc); hi.append(Mg > 0); fs.append((Ms / 2) / (Ms / 2 + Mg))
    DWM[f] = dict(hi=np.array(hi), fsph=np.array(fs))
# SPARC galaxies
Mb_pt = np.array([QG[g]["Mb"] if g in QG else np.nan for g in SP["gal"]])
SMALL = np.isfinite(Mb_pt) & (Mb_pt <= 3e9); LARGE = np.isfinite(Mb_pt) & (Mb_pt > 3e9)
GALS = sorted(set(SP["gal"]))
VGAL = {}
for g in GALS:
    vf = QG[g]["Vflat"] if g in QG else 0.0
    VGAL[g] = vf if vf > 0 else float(SP["V"][SP["gal"] == g].max())
bfrac = np.clip(0.7 * SP["Vb"] * np.abs(SP["Vb"]) / (SP["Vg"] * np.abs(SP["Vg"]) + 0.5 * SP["Vd"] * np.abs(SP["Vd"]) + 0.7 * SP["Vb"] * np.abs(SP["Vb"])), 0, 1)
FSPH_GAL = {g: float(np.mean(bfrac[SP["gal"] == g])) for g in GALS}
n_vf0 = sum(1 for g in GALS if not (g in QG and QG[g]["Vflat"] > 0))
P(f"\n  SPARC: {len(SP['gb'])} pts / {len(GALS)} gal (small {len(set(SP['gal'][SMALL]))}, large {len(set(SP['gal'][LARGE]))}); "
  f"V_flat = 0 -> max V_obs for {n_vf0} galaxies")
P(f"  dwarfs: {len(DWR['canonical']['names'])}; HI-bearing (gas inside r1/2 > 0): {int(DWM['canonical']['hi'].sum())}; "
  f"globulars: {len(gc_names)} (ARot/sigma0 for {len(_fgc)}); clusters: {NCL}")

# =====================================================================================================================  cells
def cells_persys(cls, lg, E, sE, fm):
    k = np.digitize(lg, GRID) - 1; out = []
    for b in sorted(set(k)):
        g = np.where(k == b)[0]; n = len(g)
        if n < 3: continue
        se = max(np.std(E[g], ddof=1) / math.sqrt(n), math.sqrt(np.sum(sE[g] ** 2)) / n)
        out.append(dict(cls=cls, w=int(b), lg=float(np.mean(lg[g])), E=float(np.mean(E[g])), f=float(np.mean(fm[g])), n=int(n), se_stat=float(se)))
    return out, np.diag([c["se_stat"] ** 2 for c in out])

def cells_sparc(cls, lg, E, gal, fgal, seed=919):
    k = np.digitize(lg, GRID) - 1; G_ = sorted(set(gal)); gi = {g: i for i, g in enumerate(G_)}; ig = np.array([gi[g] for g in gal])
    ub = sorted(set(k)); nG, nB = len(G_), len(ub); Ms_, Mn, Ls_ = np.zeros((nG, nB)), np.zeros((nG, nB)), np.zeros((nG, nB))
    for j, b in enumerate(ub):
        m = k == b; np.add.at(Ms_[:, j], ig[m], E[m]); np.add.at(Mn[:, j], ig[m], 1); np.add.at(Ls_[:, j], ig[m], lg[m])
    with np.errstate(invalid="ignore", divide="ignore"):
        Mg_, Lg_ = Ms_ / Mn, Ls_ / Mn
    ngal = (Mn > 0).sum(0); keep = ngal >= 5
    Mg_, Lg_, Mn_k = Mg_[:, keep], Lg_[:, keep], Mn[:, keep]; ubk = [b for b, kk in zip(ub, keep) if kk]
    val, lrb = np.nanmean(Mg_, 0), np.nanmean(Lg_, 0)
    fg = np.array([fgal[g] for g in G_]); fcell = [float(np.mean(fg[Mn_k[:, j] > 0])) for j in range(len(ubk))]
    rng = np.random.default_rng(seed); BS = np.empty((1000, Mg_.shape[1]))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for t in range(1000):
            BS[t] = np.nanmean(Mg_[rng.integers(0, nG, nG)], 0)
    nb = len(val); C = np.empty((nb, nb))
    for a in range(nb):
        for b in range(nb):
            m = np.isfinite(BS[:, a]) & np.isfinite(BS[:, b]); x, y = BS[m, a], BS[m, b]
            C[a, b] = np.mean((x - x.mean()) * (y - y.mean())) * len(x) / max(len(x) - 1, 1)
    out = [dict(cls=cls, w=int(ubk[j]), lg=float(lrb[j]), E=float(val[j]), f=fcell[j], n=int((Mn_k[:, j] > 0).sum()), se_stat=float(math.sqrt(C[j, j])))
           for j in range(nb)]
    return out, C

def lens_set(key, f, shift):
    gb, go, C = LD_[key]; gbs = gb * 10 ** shift; gl = gbs * nu_e15(gbs / A0[f]); m = (gbs >= LWIN[0]) & (gbs < LWIN[1])
    return gbs[m], go[m], C[np.ix_(m, m)], gl[m]

def cells_lens(cls, gb, go, C, gl, fval):
    lr = np.log10(gb); k = np.digitize(lr, GRID) - 1; n = len(go); Ws, info = [], []
    for b in sorted(set(k)):
        S = np.where(k == b)[0]; Ci = np.linalg.inv(C[np.ix_(S, S)]); a = gl[S] @ Ci @ gl[S]
        w = np.zeros(n); w[S] = (Ci @ gl[S]) / a; A = float(w @ go); sA = math.sqrt(float(w @ C @ w))
        if A <= 0 or sA / A > 1: continue
        ww = np.abs(w[S] * gl[S]); ww = ww / ww.sum(); Ws.append(w)
        info.append(dict(cls=cls, w=int(b), lg=float(np.sum(ww * lr[S])), A=A, n=int(len(S)), f=float(fval)))
    if not Ws: return [], np.zeros((0, 0))
    Wm = np.array(Ws); CA = Wm @ C @ Wm.T; Av = np.array([i["A"] for i in info]); CE = CA / np.outer(Av, Av)
    for j, i in enumerate(info): i["E"] = math.log(i["A"]); i["se_stat"] = math.sqrt(CE[j, j])
    return info, CE

def cells_clusters(f, jsel, fval):
    lr = CLR[f]["gbar"][:, jsel]; D = CD[:, jsel]; W = CW[:, jsel]; Pm = CLP[f][:, jsel]
    cid = np.repeat(np.arange(NCL)[:, None], len(jsel), 1); k = np.digitize(lr, GRID) - 1; info, cols = [], []
    for b in sorted(set(k.ravel())):
        m = k == b
        if len(set(cid[m])) < 20 or (W[m] * Pm[m]).sum() <= 0: continue
        A = (W[m] * D[m]).sum() / (W[m] * Pm[m]).sum()
        if A <= 0: continue
        reps = []
        for p in range(30):
            mp = m & (PATCH[:, None] != p); reps.append((W[mp] * D[mp]).sum() / (W[mp] * Pm[mp]).sum())
        wl = W[m] * Pm[m]
        info.append(dict(cls="CL", w=int(b), lg=float((wl * lr[m]).sum() / wl.sum()), A=float(A), n=int(len(set(cid[m]))), f=float(fval)))
        cols.append(np.array(reps))
    if not info: return [], np.zeros((0, 0))
    Rr = np.array(cols); Rm = Rr.mean(1, keepdims=True); CA = 29 / 30 * (Rr - Rm) @ (Rr - Rm).T
    Av = np.array([i["A"] for i in info]); CE = CA / np.outer(Av, Av)
    for j, i in enumerate(info): i["E"] = math.log(i["A"]); i["se_stat"] = math.sqrt(CE[j, j])
    return info, CE

def blockdiag(mats):
    n = sum(m.shape[0] for m in mats); C = np.zeros((n, n)); o = 0
    for m in mats:
        k = m.shape[0]; C[o:o + k, o:o + k] = m; o += k
    return C

VARIANTS = {"V0": {}, "V1": {"measure": "fsph"}, "V2": {"colour": True}, "V3a": {"bracket": "a"}, "V3b": {"bracket": "b"},
            "V4": {"gc_efe": True}, "V5": {"inner": True}, "V6": {"floor": FLOOR_V6}, "V7": {"noshift": True}}
VDESC = {"V0": "primary", "V1": "alternative measure f_sph", "V2": "colour lens bins", "V3a": "f brackets: less pressure",
         "V3b": "f brackets: more extreme", "V4": "globulars vs law+EFE", "V5": "clusters + INNER band", "V6": "floor 0.10 dex",
         "V7": "no +0.123 M* shift on n>2/red"}

def build(f, opt):
    """cells + statistical covariance (block diagonal by class) + member-level data for the W tests."""
    meas = opt.get("measure", "fP"); br = opt.get("bracket"); cells, mats = [], []
    # DW
    d = DWR[f]
    if meas == "fsph": fdw = DWM[f]["fsph"]
    elif br == "a": fdw = np.where(DWM[f]["hi"], fP(1.0), fP(0.5))
    else: fdw = np.ones(len(d["names"]))
    c, C = cells_persys("DW", np.asarray(d["gbar"], float), np.asarray(d["E"], float), np.asarray(d["sE"], float), fdw); cells += c; mats.append(C)
    # SPARC
    sig = {"a": 20.0, "b": 6.0}.get(br, 10.0)
    fgal = {g: FSPH_GAL[g] for g in GALS} if meas == "fsph" else {g: 3 * sig ** 2 / (VGAL[g] ** 2 + 3 * sig ** 2) for g in GALS}
    E_sp = np.log(SP["go"] / (SP["gb"] * nu_e15(SP["gb"] / A0[f]))); lg_sp = np.log10(SP["gb"])
    for cls, msk in (("SS", SMALL), ("SL", LARGE)):
        c, C = cells_sparc(cls, lg_sp[msk], E_sp[msk], SP["gal"][msk], fgal); cells += c; mats.append(C)
    # lenses
    kd, ks = ("blue", "red") if opt.get("colour") else ("disc", "sph"); sh = 0.0 if opt.get("noshift") else 0.123
    if meas == "fsph": fd, fs_ = 0.15, 0.70
    else: fd, fs_ = {"a": (0.43, 0.57), "b": (0.10, 0.97)}.get(br, (0.20, 0.80))
    lens_comb = {}
    for cls, key, shift, fv in (("LD", kd, 0.0, fd), ("LS", ks, sh, fs_)):
        gb, go, C_, gl = lens_set(key, f, shift); c, C = cells_lens(cls, gb, go, C_, gl, fv); cells += c; mats.append(C)
        a = gls_amp(gb, go, C_, gl, LWIN); lens_comb[cls] = (math.log(a["A"]), a["sA"] / a["A"], fv)
    # clusters
    jsel = list(range(8)) if opt.get("inner") else [3, 4, 5, 6, 7]
    c, C = cells_clusters(f, jsel, 1.0 if meas == "fsph" else (0.9 if br == "a" else 1.0)); cells += c; mats.append(C)
    # globulars
    gl_ = GCR[f]; s0 = 0.7 if (br == "a" and meas != "fsph") else 1.0
    vs = [((GKIN[r["name"]]["arot"] / (s0 * GKIN[r["name"]]["sig0"])) if gc_vs.get(r["name"]) is not None else None) for r in gl_]
    fg = np.array([fP(v) if v is not None else np.nan for v in vs]); fg = np.where(np.isfinite(fg), fg, np.nanmedian(fg))
    if meas == "fsph": fg = np.ones(len(gl_))
    Eg = np.array([r["E_efe" if opt.get("gc_efe") else "E"] for r in gl_]); sEg = np.array([r["sE"] for r in gl_])
    c, C = cells_persys("GC", np.array([r["gbar"] for r in gl_]), Eg, sEg, fg); cells += c; mats.append(C)
    # member-level data for W2 / W3
    k25 = np.digitize(lg_sp, np.arange(-20.0, 10.0001, 0.25)); epsp = np.empty_like(E_sp)
    for b in set(k25):
        m = k25 == b; epsp[m] = E_sp[m] - np.median(E_sp[m])
    okg = SMALL | LARGE; gal_ok = sorted(set(SP["gal"][okg]))
    eps_g = np.array([float(np.mean(epsp[okg & (SP["gal"] == g)])) for g in gal_ok]); f_g = np.array([fgal[g] for g in gal_ok])
    mem = dict(lens=lens_comb, sp_f=f_g, sp_eps=eps_g, gc_f=fg, gc_E=Eg, gc_sE=sEg)
    return cells, blockdiag(mats), mem

# =====================================================================================================================  tests
def fit_form(x, E, C, cls):
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):     # spurious Accelerate FP flags (A1); finiteness asserted
        return _fit_form(x, E, C, cls)
def _fit_form(x, E, C, cls):
    Ci = np.linalg.inv(C); a = float(x @ Ci @ x); assert np.isfinite(a)
    if a <= 0: return dict(A=float("nan"), sA=float("nan"), AsA=float("nan"), chi2=float("nan"), dof=len(E) - 1, p=0.0, zc={}, maxz=float("nan"),
                           grade="FAIL", note="x == 0")
    A = float(x @ Ci @ E) / a; sA = a ** -0.5; r = E - A * x; chi2 = float(r @ Ci @ r); dof = len(E) - 1; p = float(CHI2.sf(chi2, dof))
    assert np.isfinite(A) and np.isfinite(chi2)
    zc = {}
    for c in dict.fromkeys(cls):
        ix = np.where(cls == c)[0]; Cc = np.linalg.inv(C[np.ix_(ix, ix)]); one = np.ones(len(ix))
        zc[c] = float(one @ Cc @ r[ix] / math.sqrt(one @ Cc @ one))
    mz = max(abs(v) for v in zc.values())
    grade = "PASS" if (p >= 0.05 and mz <= 3) else ("FAIL" if (p < 0.01 or mz > 3) else "MARGINAL")
    return dict(A=A, sA=sA, AsA=A / sA, chi2=chi2, dof=dof, p=p, zc=zc, maxz=mz, grade=grade)

def evaluate(cells, Ctot, mem=None, level="full"):
    E = np.array([c["E"] for c in cells]); fm = np.array([c["f"] for c in cells]); cls = np.array([c["cls"] for c in cells])
    w = np.array([c["w"] for c in cells]); sg = np.sqrt(np.diag(Ctot)); isgc = cls == "GC"; rot, prs = fm <= 0.3, fm >= 0.7
    C1, C1f = [], []                                       # C1 = AMENDMENT A1 rule (governing); C1f = frozen rule (reported)
    for i in np.where(rot)[0]:
        if E[i] / sg[i] < 3: continue
        Pj = [j for j in range(len(E)) if w[j] == w[i] and prs[j] and not isgc[j]]
        if Pj:
            wt = 1 / sg[Pj] ** 2; EP = float(np.sum(wt * E[Pj]) / wt.sum()); sP = float(wt.sum() ** -0.5)
            cond_f = E[i] >= EP - 2 * math.sqrt(sg[i] ** 2 + sP ** 2); cond_a = E[i] >= EP; ref = f"pressure mean {EP:+.3f}+-{sP:.3f}"
        else:
            cond_f = cond_a = E[i] >= E_C1_ABS; ref = "absolute 0.15 dex"
        el = dict(cls=str(cls[i]), w=int(w[i]), lg=cells[i]["lg"], E=float(E[i]), z=float(E[i] / sg[i]), f=float(fm[i]), ref=ref)
        if cond_a: C1.append(el)
        if cond_f: C1f.append(el)
    C2 = []
    for i in np.where(prs)[0]:
        if E[i] >= 2 * sg[i]: continue
        for j in range(len(E)):
            if j == i or w[j] != w[i] or fm[j] > fm[i]: continue
            z = (E[j] - E[i]) / math.sqrt(sg[i] ** 2 + sg[j] ** 2)
            if z >= 3:
                C2.append(dict(i=str(cls[i]), j=str(cls[j]), w=int(w[i]), lg_i=cells[i]["lg"], lg_j=cells[j]["lg"], f_i=float(fm[i]), f_j=float(fm[j]),
                               E_i=float(E[i]), E_j=float(E[j]), z=float(z), gc_conditional=bool(isgc[i] or isgc[j])))
    ng = ~isgc
    F = {}
    F["F1"] = fit_form(fm[ng], E[ng], Ctot[np.ix_(ng, ng)], cls[ng])
    F["F2"] = fit_form((fm[ng] > 0.5).astype(float), E[ng], Ctot[np.ix_(ng, ng)], cls[ng])
    # ordering statistic T (non-GC, same window, |df| > 0.1)
    tt = []
    for i in np.where(ng)[0]:
        for j in np.where(ng)[0]:
            if j <= i or w[j] != w[i] or abs(fm[i] - fm[j]) <= 0.1: continue
            tt.append(np.sign(fm[i] - fm[j]) * math.tanh((E[i] - E[j]) / math.sqrt(sg[i] ** 2 + sg[j] ** 2)))
    T = float(np.mean(tt)) if tt else float("nan")
    Wt = {}
    if level == "full" and mem is not None:
        (eS, sS, fS), (eD, sD, fD) = mem["lens"]["LS"], mem["lens"]["LD"]; zW1 = (eS - eD) / math.hypot(sS, sD)
        Wt["W1"] = dict(dE=eS - eD, z=zW1, violation=bool(zW1 <= -2 and fS > fD), gc=False)
        r2, p2 = spearmanr(mem["sp_f"], mem["sp_eps"]); Wt["W2"] = dict(rho=float(r2), p=float(p2), n=int(len(mem["sp_f"])), violation=bool(r2 < 0 and p2 < 0.01), gc=False)
        if np.ptp(mem["gc_f"]) > 0:
            r3, p3 = spearmanr(mem["gc_f"], mem["gc_E"]); Wt["W3"] = dict(rho=float(r3), p=float(p3), n=int(len(mem["gc_f"])), violation=bool(r3 < 0 and p3 < 0.01), gc=True)
        else:
            Wt["W3"] = dict(rho=None, p=None, n=int(len(mem["gc_f"])), violation=False, gc=True, note="no spread in f")
    present = set(cls[ng]); rot_cls = {c for c in present if np.any(rot[ng][cls[ng] == c])}
    prs_cls = {c for c in present if np.any(prs[ng][cls[ng] == c])}
    coverage = len(present) >= 4 and len(rot_cls) >= 1 and len(prs_cls) >= 2
    c2w = [x for x in C2 if not x["gc_conditional"]]; wv = [k for k, v in Wt.items() if v["violation"] and not v["gc"]]
    sup_form = [k for k in ("F1", "F2") if F[k]["grade"] == "PASS" and F[k]["AsA"] >= 3]
    def decide(c1list):
        contra = []
        if c1list: contra.append("C1")
        if c2w: contra.append("C2")
        if wv: contra += wv
        if F["F1"]["grade"] == "FAIL" and F["F2"]["grade"] == "FAIL": contra.append("C3 (F1 and F2 FAIL)")
        if not coverage: cl = "NOT DIAGNOSTIC (coverage)"
        elif contra: cl = "SELECTOR CONTRADICTED"
        elif sup_form: cl = "SELECTOR SUPPORTED"
        else: cl = "NOT DIAGNOSTIC"
        return cl, contra
    cl, contra = decide(C1); cl_f, contra_f = decide(C1f)
    return dict(cls=cl, contra=contra, cls_frozen=cl_f, contra_frozen=contra_f, sup_form=sup_form, C1=C1, C1_frozen=C1f, C2=C2, F=F, W=Wt, T=T,
                npairs=len(tt), coverage=coverage, classes=sorted(present), rot_classes=sorted(rot_cls), prs_classes=sorted(prs_cls))

def class_summary(cells, Ctot):
    cls = np.array([c["cls"] for c in cells]); E = np.array([c["E"] for c in cells]); out = {}
    for c in CLASSES:
        ix = np.where(cls == c)[0]
        if not len(ix): out[c] = None; continue
        Ci = np.linalg.inv(Ctot[np.ix_(ix, ix)]); one = np.ones(len(ix)); m = float(one @ Ci @ E[ix] / (one @ Ci @ one)); s = float((one @ Ci @ one) ** -0.5)
        out[c] = dict(E=m, se=s, dex=m / LN10, n_cells=int(len(ix)), f=float(np.mean([cells[i]["f"] for i in ix])),
                      lg=(float(min(cells[i]["lg"] for i in ix)), float(max(cells[i]["lg"] for i in ix))))
    return out

def run_variant(f, vk):
    opt = VARIANTS[vk]; cells, C, mem = build(f, opt); fl = opt.get("floor", FLOOR0); Ctot = C + fl ** 2 * np.eye(len(cells))
    for c, s in zip(cells, np.sqrt(np.diag(Ctot))): c["se_tot"] = float(s)
    return cells, Ctot, mem, evaluate(cells, Ctot, mem, "full")

def jcells(cells): return [{k: v for k, v in c.items() if k != "A"} for c in cells]

def mv(L, z):
    """L @ z.  macOS Accelerate BLAS raises spurious overflow/invalid FP flags in matmul (checked against an explicit sum
    to 1e-15); the flags are silenced here and finiteness is asserted instead."""
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        y = L @ z
    assert np.all(np.isfinite(y)) and np.allclose(y, (L * z).sum(1), rtol=1e-12, atol=1e-12)
    return y

# =====================================================================================================================  MAIN
EXIT = 0
if not MUT:
    BYF = {}
    for f in FOOTS:
        P(f"\n=== [{f}] V0 primary (f_P; Sersic lenses +0.123 on n>2; clusters MID+OUTER; globulars vs screened baseline; floor 0.05 dex)")
        cells, Ctot, mem, ev = run_variant(f, "V0")
        P("    class window  <log g_bar>  n     f      E        sigma_tot   dex")
        for c in cells:
            P(f"    {c['cls']:3s}  [{GRID[c['w']]:+.1f},{GRID[c['w'] + 1]:+.1f})  {c['lg']:+7.2f}  {c['n']:4d}  {c['f']:.3f}  {c['E']:+.3f}  +- {c['se_tot']:.3f}   {c['E'] / LN10:+.3f}")
        cs = class_summary(cells, Ctot)
        P("    class means (GLS over the class's cells):")
        for c in CLASSES:
            if cs[c]: P(f"      {CNAME[c]:26s} f {cs[c]['f']:.3f}  E {cs[c]['E']:+.3f} +- {cs[c]['se']:.3f} ({cs[c]['dex']:+.3f} dex)  cells {cs[c]['n_cells']}  log g_bar {cs[c]['lg'][0]:+.2f}..{cs[c]['lg'][1]:+.2f}")
        P(f"    C1 rotating with excess (A1 rule): {len(ev['C1'])}" + "".join(f"\n      {x['cls']} w[{GRID[x['w']]:+.1f}) E {x['E']:+.3f} z {x['z']:+.1f} f {x['f']:.2f} vs {x['ref']}" for x in ev["C1"]))
        P(f"    C1 (frozen rule): {len(ev['C1_frozen'])}" + "".join(f"\n      {x['cls']} w[{GRID[x['w']]:+.1f}) E {x['E']:+.3f} z {x['z']:+.1f} f {x['f']:.2f} vs {x['ref']}" for x in ev["C1_frozen"]))
        P(f"    C2 pressure-supported on the law at the same g_bar: {len(ev['C2'])} ({sum(not x['gc_conditional'] for x in ev['C2'])} non-GC)")
        for x in ev["C2"]:
            P(f"      i={x['i']} (f {x['f_i']:.2f}, E {x['E_i']:+.3f}) vs j={x['j']} (f {x['f_j']:.2f}, E {x['E_j']:+.3f}) in [{GRID[x['w']]:+.1f},{GRID[x['w'] + 1]:+.1f}): z {x['z']:+.1f}"
              + ("   [STIFFNESS-CONDITIONAL]" if x["gc_conditional"] else ""))
        for k, v in ev["W"].items():
            if k == "W1": P(f"    W1 lenses sph - disc (combined window): dE {v['dE']:+.3f} (z {v['z']:+.1f}) -> {'VIOLATION' if v['violation'] else 'ok'}")
            else: P(f"    {k} {'SPARC' if k == 'W2' else 'globulars'} Spearman(f, E) rho {v['rho'] if v['rho'] is None else round(v['rho'], 3)} p {v['p'] if v['p'] is None else '%.3g' % v['p']} (n {v['n']}) -> {'VIOLATION' if v['violation'] else 'ok'}" + ("  [STIFFNESS-CONDITIONAL]" if v["gc"] else ""))
        for k in ("F1", "F2"):
            F_ = ev["F"][k]
            P(f"    {k} {'E = A f' if k == 'F1' else 'E = A step(f-0.5)'}: A {F_['A']:+.3f} +- {F_['sA']:.3f} (A/sA {F_['AsA']:+.1f}); chi2 {F_['chi2']:.1f}/{F_['dof']} p {F_['p']:.2e}; "
              f"class z: " + " ".join(f"{c} {z:+.1f}" for c, z in F_["zc"].items()) + f" -> {F_['grade']}")
        P(f"    ordering statistic T {ev['T']:+.3f} over {ev['npairs']} pairs;  coverage {ev['coverage']} (rotating {ev['rot_classes']}, pressure {ev['prs_classes']})")
        P(f"    ==> [{f}] V0 class AS FROZEN: {ev['cls_frozen']}" + (f"  (because: {', '.join(ev['contra_frozen'])})" if ev["contra_frozen"] else "")
          + (f"  (form {ev['sup_form']})" if ev["sup_form"] else ""))
        P(f"    ==> [{f}] V0 class UNDER A1:  {ev['cls']}" + (f"  (because: {', '.join(ev['contra'])})" if ev["contra"] else "") + (f"  (form {ev['sup_form']})" if ev["sup_form"] else ""))
        # secondary (no class weight)
        E = np.array([c["E"] for c in cells]); fm = np.array([c["f"] for c in cells]); cl = np.array([c["cls"] for c in cells])
        wq = np.array([c["w"] for c in cells]); ng = cl != "GC"
        gate = np.array([GRID[x + 1] <= -12.0 for x in wq]).astype(float)
        F3 = fit_form((fm * gate)[ng], E[ng], Ctot[np.ix_(ng, ng)], cl[ng])
        F1g = fit_form(fm, E, Ctot, cl); F2g = fit_form((fm > 0.5).astype(float), E, Ctot, cl)
        P(f"    secondary (no class weight): F3 A f step(g_bar<1e-12): A {F3['A']:+.3f}+-{F3['sA']:.3f} chi2 {F3['chi2']:.1f}/{F3['dof']} p {F3['p']:.2e} "
          + " ".join(f"{c} {z:+.1f}" for c, z in F3["zc"].items()) + f" -> {F3['grade']};  with GC: F1 {F1g['grade']} (p {F1g['p']:.1e}), F2 {F2g['grade']} (p {F2g['p']:.1e})")
        BYF[f] = dict(V0=dict(cells=jcells(cells), class_summary=cs, **{k: v for k, v in ev.items()}), secondary=dict(F3=F3, F1_with_GC=F1g, F2_with_GC=F2g), variants={})
        P(f"\n    variants [{f}]:")
        for vk in VARIANTS:
            if vk == "V0": continue
            cv, Cv, mvv, evv = run_variant(f, vk)
            BYF[f]["variants"][vk] = dict(desc=VDESC[vk], cells=jcells(cv), class_summary=class_summary(cv, Cv), **{k: v for k, v in evv.items()})
            P(f"      {vk:4s} {VDESC[vk]:32s} -> A1 {evv['cls']:22s} frozen {evv['cls_frozen']:22s} C1 {len(evv['C1'])}/{len(evv['C1_frozen'])}  C2(non-GC) {sum(not x['gc_conditional'] for x in evv['C2'])}  "
              f"F1 {evv['F']['F1']['grade']} (p {evv['F']['F1']['p']:.1e}, A {evv['F']['F1']['A']:+.2f})  F2 {evv['F']['F2']['grade']} (p {evv['F']['F2']['p']:.1e})  T {evv['T']:+.2f}"
              + (f"  [{', '.join(evv['contra'])}]" if evv["contra"] else ""))
        P(f"    [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
    def overall_of(key):
        c0 = {f: BYF[f]["V0"][key] for f in FOOTS}
        if all(c == "SELECTOR CONTRADICTED" for c in c0.values()): ov = "SELECTOR CONTRADICTED"
        elif all(c == "SELECTOR SUPPORTED" for c in c0.values()): ov = "SELECTOR SUPPORTED"
        else: ov = "SPLIT BY FOOTING -> NOT DIAGNOSTIC" if len(set(c0.values())) > 1 else "NOT DIAGNOSTIC"
        ch = [f"{f}:{vk}" for f in FOOTS for vk, v in BYF[f]["variants"].items() if v[key] != c0[f]]
        return c0, ov, ch, ("FRAGILE" if ch else "ROBUST (no variant changes the class)")
    c0f, ovf, chf, labf = overall_of("cls_frozen"); c0, overall, changed, label = overall_of("cls")
    P(f"\n=== CLASS AS FROZEN: {ovf}  (canonical {c0f['canonical']}; alt {c0f['alt']});  {labf}" + (f"  changed in: {', '.join(chf)}" if chf else ""))
    P(f"=== CLASS UNDER A1:  {overall}  (canonical {c0['canonical']}; alt {c0['alt']});  {label}" + (f"  changed in: {', '.join(changed)}" if changed else ""))
    RES.update(byfoot=BYF, class_per_footing=c0, overall=overall, robustness=label, variants_changing=changed,
               class_per_footing_frozen=c0f, overall_frozen=ovf, robustness_frozen=labf, variants_changing_frozen=chf)

elif MUT == "shuffle":
    S = {}; bites = []
    for f in FOOTS:
        cells, Ctot, mem, ev = run_variant(f, "V0"); fm = np.array([c["f"] for c in cells]); n = len(cells)
        L = np.linalg.cholesky(Ctot); rng = np.random.default_rng(919); z = rng.standard_normal(n)
        Einj = 1.0 * fm + mv(L, z)
        def with_E_f(Ev, fv):
            cc = [dict(c) for c in cells]
            for c, e, ff in zip(cc, Ev, fv): c["E"], c["f"] = float(e), float(ff)
            return cc
        ev_true = evaluate(with_E_f(Einj, fm), Ctot, None, "cell")
        rs = np.random.default_rng(9191); ns, nsf, Ts = 0, 0, []
        for t in range(1000):
            ev_s = evaluate(with_E_f(Einj, rs.permutation(fm)), Ctot, None, "cell"); ns += ev_s["cls"] == "SELECTOR SUPPORTED"
            nsf += ev_s["cls_frozen"] == "SELECTOR SUPPORTED"; Ts.append(ev_s["T"])
        frac, fracf = ns / 1000, nsf / 1000; medT = float(np.nanmedian(Ts)); bite = (frac <= 0.10) and (medT <= 0.5 * ev_true["T"])
        bitef = (fracf <= 0.10) and (medT <= 0.5 * ev_true["T"]); bites.append(bite)
        Ereal = np.array([c["E"] for c in cells]); Tr = ev["T"]; rs2 = np.random.default_rng(9192); Tsr = []
        for t in range(1000):
            Tsr.append(evaluate(with_E_f(Ereal, rs2.permutation(fm)), Ctot, None, "cell")["T"])
        pr = float(np.mean(np.array(Tsr) >= Tr))
        S[f] = dict(S1=dict(true_class=ev_true["cls"], true_class_frozen=ev_true["cls_frozen"], T_true=ev_true["T"], F1_true=ev_true["F"]["F1"],
                            frac_supported_shuffled=frac, frac_supported_shuffled_frozen=fracf, median_T_shuffled=medT, bites=bite, bites_frozen=bitef),
                    S2=dict(T_real=Tr, median_T_shuffled=float(np.nanmedian(Tsr)), p_perm=pr))
        P(f"\n  [{f}] S1 planted (E = 1.0 f + noise): true labels -> A1 {ev_true['cls']} / frozen {ev_true['cls_frozen']} (T {ev_true['T']:+.3f}, "
          f"F1 A {ev_true['F']['F1']['A']:+.3f}+-{ev_true['F']['F1']['sA']:.3f}); 1000 label shuffles -> SUPPORTED in {100 * frac:.1f}% (A1) / {100 * fracf:.1f}% (frozen), "
          f"median T {medT:+.3f} -> A1 {'BITES' if bite else 'DOES NOT BITE'}, frozen {'BITES' if bitef else 'DOES NOT BITE'}")
        P(f"  [{f}] S2 real cells: T {Tr:+.3f}; shuffled median T {np.nanmedian(Tsr):+.3f}; permutation p(T_shuf >= T) = {pr:.3f}  (no class weight)")
    RES.update(shuffle=S, bites=all(bites)); EXIT = 1 if all(bites) else 0
    P(f"\n  MUTATE shuffle: {'BITES on both footings (exit 1, as designed)' if all(bites) else 'does NOT bite (control failure, exit 0)'}")

elif MUT == "inject":
    INJ = {}; ok_all = True; okf_all = [True]
    sig_fun = {"I0": lambda x: 0.0 * x, "I1": lambda x: 1.0 * x, "I2": lambda x: 1.0 * (x > 0.5)}
    for f in FOOTS:
        cells, Ctot, mem, ev = run_variant(f, "V0"); fm = np.array([c["f"] for c in cells]); n = len(cells); L = np.linalg.cholesky(Ctot)
        sd_g = float(np.std(mem["sp_eps"], ddof=1)); INJ[f] = {}
        for ik, sfun in sig_fun.items():
            rng = np.random.default_rng(919); cnt, cntf = {}, {}; Ahat, rec = [], 0
            for t in range(200):
                Ev = sfun(fm) + mv(L, rng.standard_normal(n))
                cc = [dict(c) for c in cells]
                for c, e in zip(cc, Ev): c["E"] = float(e)
                (eS, sS, fS), (eD, sD, fD) = mem["lens"]["LS"], mem["lens"]["LD"]
                dW1 = float(sfun(np.array([fS]))[0] - sfun(np.array([fD]))[0]) + rng.normal(0, math.hypot(sS, sD))
                m2 = dict(lens={"LS": (dW1, sS, fS), "LD": (0.0, sD, fD)},
                          sp_f=mem["sp_f"], sp_eps=sfun(mem["sp_f"]) + rng.normal(0, sd_g, len(mem["sp_f"])),
                          gc_f=mem["gc_f"], gc_E=sfun(mem["gc_f"]) + rng.normal(0, 1, len(mem["gc_f"])) * mem["gc_sE"], gc_sE=mem["gc_sE"])
                e_ = evaluate(cc, Ctot, m2, "full"); cnt[e_["cls"]] = cnt.get(e_["cls"], 0) + 1; cntf[e_["cls_frozen"]] = cntf.get(e_["cls_frozen"], 0) + 1
                A1, s1 = e_["F"]["F1"]["A"], e_["F"]["F1"]["sA"]; Ahat.append(A1); rec += abs(A1 - 1.0) / s1 <= 2
            fs, fsf = cnt.get("SELECTOR SUPPORTED", 0) / 200, cntf.get("SELECTOR SUPPORTED", 0) / 200
            req = lambda x: {"I0": x <= 0.10, "I1": x >= 0.90 and rec / 200 >= 0.90, "I2": x >= 0.90}[ik]
            need, needf = req(fs), req(fsf); ok_all &= need; okf_all[0] &= needf
            INJ[f][ik] = dict(counts=cnt, frac_supported=fs, required_met=bool(need), counts_frozen=cntf, frac_supported_frozen=fsf, required_met_frozen=bool(needf),
                              median_A_F1=float(np.median(Ahat)), frac_A_within_2sigma_of_1=rec / 200)
            P(f"  [{f}] {ik} ({'E = 0' if ik == 'I0' else ('E = 1.0 f' if ik == 'I1' else 'E = 1.0 step(f-0.5)')}): median A_F1 {np.median(Ahat):+.3f}  |A-1|<=2sA {100 * rec / 200:.1f}%")
            P(f"        AS FROZEN: SUPPORTED {100 * fsf:.1f}%  classes {cntf} -> {'OK' if needf else 'FAIL'}")
            P(f"        UNDER A1:  SUPPORTED {100 * fs:.1f}%  classes {cnt} -> {'OK' if need else 'FAIL'}")
    RES.update(inject=INJ, recovered=bool(ok_all), recovered_frozen=bool(okf_all[0])); EXIT = 0 if ok_all else 1
    P(f"\n  INJECT AS FROZEN: {'all required recoveries met' if okf_all[0] else 'a required recovery FAILED (frozen C1; see AMENDMENT_A1.md)'}")
    P(f"  INJECT UNDER A1:  {'all required recoveries met (exit 0)' if ok_all else 'a required recovery FAILED (exit 1)'}")

P(f"\n  done [{time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB].  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
RES["runtime_s"] = time.time() - T0; RES["peak_rss_mb"] = rss_mb()
json.dump(RES, builtins.open(os.path.join(HERE, f"cfg919_results{SUF}.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
builtins.open(os.path.join(HERE, f"cfg919{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(EXIT)
