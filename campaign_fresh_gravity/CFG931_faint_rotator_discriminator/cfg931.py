"""CFG931 -- faint-rotator discriminator: energy picture E vs kinematic picture K at matched g_bar.
Criteria: FROZEN_CRITERIA.md (cad92ca1c, committed alone before this script); AMENDMENT_A1.md (165bb5c71, post-freeze, before
any run): I-30 recovery needs the lever gate too; S2 rng 9312; exit codes; V4 error source; one UGCA 444 INFO line.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg931.py      (CFG931_KONLY=1 -> K only; CFG931_MUTATE=inject|shuffle -> separate
outputs named by mode).  Exit 0 = K passed and every required control in the mode met; 1 = a required MUTATE control failed;
2 = a K-test failed (no class).
Inputs: SPARC (Lelli+16) rotmod files + Table 1; CFG880's 83 LVD dwarfs (input slice exec'd read-only, writes refused); CFG828's
29 dwarfs (CFG827/CFG824 rows, LVD); Lelli+15 tidal dwarfs (INFO).  K-tests against committed CFG828 / CFG919 outputs.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; raw data, framework-native only; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, csv, json, math, glob, time, resource, warnings, contextlib, builtins
import numpy as np
from scipy.stats import spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG931_MUTATE", ""); assert MUT in ("", "inject", "shuffle")
KONLY = os.environ.get("CFG931_KONLY", "") == "1"; assert not (KONLY and MUT)
SUF = "_K" if KONLY else (f"_MUTATE_{MUT}" if MUT else "")
for _e in ("CFG880_MUTATE", "CFG828_MUTATE", "CFG919_MUTATE", "CFG914_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def J(*p): return json.load(builtins.open(os.path.join(LANES, *p)))
def jdef(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
RES = dict(lane="CFG931", criteria="cad92ca1c", amendment_A1="165bb5c71", mode=("K" if KONLY else (MUT or "main")), checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def finish(code):
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_mb"] = round(rss_mb(), 1); RES["exit"] = code
    P(f"\n  done [{time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB], exit {code}.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    json.dump(RES, builtins.open(os.path.join(HERE, f"cfg931_results{SUF}.json"), "w"), indent=1, default=jdef)
    builtins.open(os.path.join(HERE, f"cfg931{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
LN10 = math.log(10.0)
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
GRID = np.arange(-20.0, 10.0001, 0.5)                        # CFG914/919 fixed 0.5-dex edges
W_PRIMARY, W_V5 = (15, 16), (15, 16, 17)                     # [-12.5,-12), [-12,-11.5) (+ [-11.5,-11) for V5)
SPLITS = (1e7, 3e7, 1e8); PRIMARY_SPLIT = 1e7
FLOOR = 0.05; NBOOT = 4000; ZK = 2.0; MDDF = 2.84            # dex floor per group mean; z threshold; MDD factor (z 2, 80 % power)
SIG_AD = 8.0                                                 # V3 pressure-support bracket (km/s)
I30 = 0.30
VARIANTS = ("V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7")
VDESC = {"V0": "primary", "V1": "floor 0 (stat only)", "V2": "floor 0.10 dex", "V3": "rotators g_obs=(V^2+2*8^2)/R",
         "V4": "CFG828 dwarfs (Ups_SFH, no gas)", "V5": "window [-12.5,-11.0)", "V6": "pairwise cells", "V7": "(iii) M* within [min M*_i, split)"}
nu_e12 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
nu_e15 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_s12 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-12)))
FLOOR0_919 = 0.05 * LN10

P("CFG931  faint-rotator discriminator: energy picture E vs kinematic picture K at matched g_bar"
  + (f"   [MUTATE {MUT}]" if MUT else ("   [K only]" if KONLY else "")))
P("  groups: (i) SPARC rotators M* < split, (ii) M* >= split, (iii) CFG880 dSphs M* < split; W = [1e-12.5, 1e-11.5); kappa = 1/2 FITTED")

# =====================================================================================================================  SPARC
QG = {}
for l in builtins.open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: QG[v[0]] = dict(inc=float(v[5]), q=int(v[17]), L=float(v[7]), MHI=float(v[13]), Vflat=float(v[15]),
                             Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9, Ms=0.5 * float(v[7]) * 1e9)
        except ValueError: pass
def load_sparc(cut=True, only=None):
    S = dict(gal=[], R=[], V=[], eV=[], Vg=[], Vd=[], Vb=[], gb=[], go=[])
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        name = os.path.basename(fn).replace("_rotmod.dat", ""); q_ = QG.get(name)
        if only is not None and name != only: continue
        inc, q = (q_["inc"], q_["q"]) if q_ else (0, 3)
        if q > 2 or inc < 30: continue
        for l in builtins.open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
            if V <= 0 or R <= 0 or (cut and eV / V >= 0.10): continue
            g_b = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if g_b <= 0: continue
            for k_, x_ in (("gal", name), ("R", R), ("V", V), ("eV", eV), ("Vg", Vg), ("Vd", Vd), ("Vb", Vb), ("gb", g_b), ("go", V * V * 1e6 / (R * KPC))):
                S[k_].append(x_)
    return {k_: np.array(x_) for k_, x_ in S.items()}
SP = load_sparc()
GALS = sorted(set(SP["gal"])); LGSP = np.log10(SP["gb"]); KSP = np.digitize(LGSP, GRID) - 1
MSTAR = {g: QG[g]["Ms"] for g in GALS}

P("\n=== K-stage")
# ---------------------------------------------------------------------------------------------------------------- K1 CFG828
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
    DW828.append(dict(name=nm, gbar=G * (Ms / 2) * MSUN / r12 ** 2, gobs=3 * (s * 1e3) ** 2 / r12, Ms=Ms, so=s, eso=R24[nm]["eso"]))
R828 = J("CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")
rng828 = np.random.default_rng(828); K1 = {}; k1d = []
for foot in FOOTS:
    for kn, nu in (("nu_e", nu_e12), ("nu_simple", nu_s12)):
        if foot == "alt" and kn == "nu_simple": continue
        a0 = A0[foot]; dS = np.log10(SP["go"] / (SP["gb"] * nu(SP["gb"] / a0))); lg = LGSP; rows = []
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
c828 = K1["canonical|nu_e"]; RES["K1"] = K1
KOK = [check("K1 CFG828 reproduced (own code; N_in, mean D, se D, SPARC median, out-of-range mean; canonical+alt nu_e)", max(k1d) <= 1e-9,
             f"max |diff| {max(k1d):.1e}; canonical: N_in {c828['N_in']}, D {c828['mean_D']:+.3f}+-{c828['se_D']:.3f} dex, "
             f"out-of-range mean {c828['out_of_range_mean_delta']:+.3f}, SPARC median {c828['sparc_median_all']:+.3f}")]

# ---------------------------------------------------------------------------------------------------------------- K2 CFG919 SPARC
R919 = J("CFG919_pressure_support_selector", "cfg919_results.json")
def cells_sparc(cls, lg, E, gal, fgal, seed=919):               # CFG919's recipe (mean of galaxy means, >= 5 galaxies, 1000-draw bootstrap)
    k = np.digitize(lg, GRID) - 1; G_ = sorted(set(gal)); gi = {g: i for i, g in enumerate(G_)}; ig = np.array([gi[g] for g in gal])
    ub = sorted(set(k)); nG, nB = len(G_), len(ub); Ms_, Mn, Ls_ = np.zeros((nG, nB)), np.zeros((nG, nB)), np.zeros((nG, nB))
    for j, b in enumerate(ub):
        m = k == b; np.add.at(Ms_[:, j], ig[m], E[m]); np.add.at(Mn[:, j], ig[m], 1); np.add.at(Ls_[:, j], ig[m], lg[m])
    with np.errstate(invalid="ignore", divide="ignore"):
        Mg_, Lg_ = Ms_ / Mn, Ls_ / Mn
    ngal = (Mn > 0).sum(0); keep = ngal >= 5
    Mg_, Lg_, Mn_k = Mg_[:, keep], Lg_[:, keep], Mn[:, keep]; ubk = [b for b, kk in zip(ub, keep) if kk]
    val, lrb = np.nanmean(Mg_, 0), np.nanmean(Lg_, 0)
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
    return [dict(cls=cls, w=int(ubk[j]), lg=float(lrb[j]), E=float(val[j]), n=int((Mn_k[:, j] > 0).sum())) for j in range(nb)], C
def gls_mean(E, C):
    Ci = np.linalg.inv(C); one = np.ones(len(E)); return float(one @ Ci @ E / (one @ Ci @ one)), float((one @ Ci @ one) ** -0.5)
Mb_pt = np.array([QG[g]["Mb"] for g in SP["gal"]]); SMALL, LARGE = Mb_pt <= 3e9, Mb_pt > 3e9
VGAL = {g: (QG[g]["Vflat"] if QG[g]["Vflat"] > 0 else float(SP["V"][SP["gal"] == g].max())) for g in GALS}
FGAL = {g: 3 * 10.0 ** 2 / (VGAL[g] ** 2 + 3 * 10.0 ** 2) for g in GALS}
k2d = []; K2 = {}
for f in FOOTS:
    E_sp = np.log(SP["go"] / (SP["gb"] * nu_e15(SP["gb"] / A0[f])))
    for cls, msk in (("SS", SMALL), ("SL", LARGE)):
        c, C = cells_sparc(cls, LGSP[msk], E_sp[msk], SP["gal"][msk], FGAL)
        m, s = gls_mean(np.array([x["E"] for x in c]), C + FLOOR0_919 ** 2 * np.eye(len(c))); ref = R919["byfoot"][f]["V0"]["class_summary"][cls]
        K2[f"{f}|{cls}"] = dict(E=m, se=s, dex=m / LN10, n_cells=len(c)); k2d += [abs(m - ref["E"]), abs(s - ref["se"])]
    k25 = np.digitize(LGSP, np.arange(-20.0, 10.0001, 0.25)); epsp = np.empty_like(E_sp)
    for b in set(k25):
        m = k25 == b; epsp[m] = E_sp[m] - np.median(E_sp[m])
    okg = SMALL | LARGE; gal_ok = sorted(set(SP["gal"][okg]))
    eps_g = np.array([float(np.mean(epsp[okg & (SP["gal"] == g)])) for g in gal_ok]); f_g = np.array([FGAL[g] for g in gal_ok])
    r2, p2 = spearmanr(f_g, eps_g); ref = R919["byfoot"][f]["V0"]["W"]["W2"]; K2[f"{f}|W2"] = dict(rho=float(r2), p=float(p2), n=len(gal_ok))
    k2d += [abs(r2 - ref["rho"]), abs(p2 - ref["p"])]
RES["K2"] = K2
KOK.append(check("K2 CFG919 SPARC class means SS/SL (E, se; V0) and W2 (rho, p) reproduced, both footings", max(k2d) <= 1e-9,
                 f"max |diff| {max(k2d):.1e}; canonical SS {K2['canonical|SS']['E']:+.3f}+-{K2['canonical|SS']['se']:.3f}, "
                 f"SL {K2['canonical|SL']['E']:+.3f}+-{K2['canonical|SL']['se']:.3f} (ln); W2 rho {K2['canonical|W2']['rho']:+.3f} p {K2['canonical|W2']['p']:.3f}"))

# ---------------------------------------------------------------------------------------------------------------- K3 CFG880 dwarfs / CFG919 DW
F880 = os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880.py")
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG931 refuses to write {file!r} from re-executed committed code")
    return builtins.open(file, mode, *a, **k)
_src = builtins.open(F880).read().split("# ---------------- hierarchical likelihood ----------------", 1)[0]
N880 = {"__file__": F880, "__name__": "cfg880_inputs_ro", "open": _ro_open}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src, F880, "exec"), N880)
def cells_persys(lg, E, sE):                                    # CFG919's per-system cells (n >= 3)
    k = np.digitize(lg, GRID) - 1; out = []
    for b in sorted(set(k)):
        g = np.where(k == b)[0]; n = len(g)
        if n < 3: continue
        se = max(np.std(E[g], ddof=1) / math.sqrt(n), math.sqrt(np.sum(sE[g] ** 2)) / n)
        out.append(dict(w=int(b), E=float(np.mean(E[g])), n=int(n), se=float(se)))
    return out
DWD = {}; k3d = []; K3 = {}
for f in FOOTS:
    a0 = A0[f]; A = N880["arrays"](N880["SAMP"], a0); law = np.sqrt(A["sl2"]); s = A["s"]
    E = 2 * np.log(s / law); e = np.where(s > law, A["em"], A["ep"]); sE = 2 * e / s; gN, Ms_ = [], []
    for nm, r12pc in zip(A["names"], A["r12"]):
        L = N880["LVD"][nm]; Ms = 2.0 * 10 ** (0.4 * (4.83 - N880["fnum"](L["M_V"])))
        Mg = N880["gas_in"](N880["fnum"](L.get("mass_HI")), r12pc); gN.append(N880["G"] * (Ms / 2 + Mg) * N880["Msun"] / (r12pc * N880["PC"]) ** 2); Ms_.append(Ms)
    lgb = np.log10(np.array(gN)); c = cells_persys(lgb, E, sE)
    m, se = gls_mean(np.array([x["E"] for x in c]), np.diag([x["se"] ** 2 for x in c]) + FLOOR0_919 ** 2 * np.eye(len(c)))
    ref = R919["byfoot"][f]["V0"]["class_summary"]["DW"]; k3d += [abs(m - ref["E"]), abs(se - ref["se"])]; K3[f] = dict(E=m, se=se, dex=m / LN10, n=len(A["names"]))
    DWD[f] = dict(names=list(A["names"]), lg=lgb, D=E / LN10, sD=sE / LN10, Ms=np.array(Ms_))
RES["K3"] = K3
KOK.append(check("K3 CFG919 DW class mean reproduced via CFG880 input slice exec'd read-only (E, se; both footings)", max(k3d) <= 1e-9,
                 f"max |diff| {max(k3d):.1e}; {K3['canonical']['n']} dwarfs; canonical {K3['canonical']['E']:+.3f}+-{K3['canonical']['se']:.3f} ln "
                 f"({K3['canonical']['dex']:+.3f} dex), alt {K3['alt']['E']:+.3f}"))
# V4 dwarfs (CFG828 sample, Ups_SFH, no gas)
DWV4 = {}
for f in FOOTS:
    a0 = A0[f]; gb4 = np.array([d["gbar"] for d in DW828]); go4 = np.array([d["gobs"] for d in DW828])
    DWV4[f] = dict(names=[d["name"] for d in DW828], lg=np.log10(gb4), D=np.log10(go4 / (gb4 * nu_e15(gb4 / a0))),
                   sD=np.array([2 * d["eso"] / (d["so"] * LN10) for d in DW828]), Ms=np.array([d["Ms"] for d in DW828]))

# ---------------------------------------------------------------------------------------------------------------- K4 inventory
lowest = min(QG, key=lambda g: QG[g]["Ms"])
KOK.append(check("K4 SPARC loader 2696 points / 147 galaxies; lowest-M* Table 1 galaxy UGCA444 at 6.0e6", len(SP["gb"]) == 2696 and len(GALS) == 147
                 and lowest == "UGCA444" and round(QG[lowest]["Ms"] / 1e6, 1) == 6.0, f"{len(SP['gb'])} points, {len(GALS)} galaxies; lowest {lowest} {QG[lowest]['Ms']:.2e}"))
K_ALL = all(KOK)
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
RES["K_all_pass"] = K_ALL
if not K_ALL:
    P("  A K-test failed: per FROZEN_CRITERIA section 8 the lane stops; no class is reported."); RES["class"] = None; finish(2)
if KONLY: finish(0)

# =====================================================================================================================  inventory
INV = dict(sparc_points=int(len(SP["gb"])), sparc_galaxies=len(GALS), splits={})
P("\n=== Inventory (on disk; rotators with resolved rotation = SPARC after Q<=2, Inc>=30, errV/V<0.10)")
for sp_ in SPLITS:
    lo = [g for g in GALS if MSTAR[g] < sp_]; lo115 = [g for g in lo if np.any(LGSP[SP["gal"] == g] < -11.5)]
    percell = {}
    for c in W_V5:
        nl = sum(1 for g in GALS if MSTAR[g] < sp_ and np.any((SP["gal"] == g) & (KSP == c)))
        nh = sum(1 for g in GALS if MSTAR[g] >= sp_ and np.any((SP["gal"] == g) & (KSP == c)))
        nd = int(np.sum((DWD["canonical"]["Ms"] < sp_) & (np.digitize(DWD["canonical"]["lg"], GRID) - 1 == c)))
        percell[str(c)] = dict(low=nl, high=nh, dwarfs=nd)
    INV["splits"][f"{sp_:.0e}"] = dict(n_low=len(lo), n_low_gbar_lt_m11p5=len(lo115), low_gbar_lt_m11p5=lo115, per_cell=percell)
    P(f"  M* < {sp_:.0e}: {len(lo)} rotators pass the cuts; with g_bar < 1e-11.5: {len(lo115)} {lo115}")
    P("     per cell (low rot / high rot / dSph M*<split): " + "  ".join(f"[{GRID[int(c)]:.1f},{GRID[int(c)] + 0.5:.1f}) {v['low']}/{v['high']}/{v['dwarfs']}" for c, v in percell.items()))
low8 = sorted([g for g in GALS if MSTAR[g] < 1e8], key=lambda g: MSTAR[g])
P("  rotators with M* < 1e8 (name, M*, min log g_bar, points in W, Q, Inc):")
for g in low8:
    m = SP["gal"] == g; P(f"    {g:12s} {MSTAR[g]:.1e}  {LGSP[m].min():6.2f}  {int(np.sum(m & np.isin(KSP, W_PRIMARY))):3d}  Q{QG[g]['q']}  {QG[g]['inc']:.0f}")
INV["low_1e8_table"] = [dict(name=g, Ms=MSTAR[g], min_lgbar=float(LGSP[SP["gal"] == g].min()), n_W=int(np.sum((SP["gal"] == g) & np.isin(KSP, W_PRIMARY)))) for g in low8]
P("  not usable as graded rotators (inventory only): Lelli+15 TDGs (6; INFO line), UNGC (W50/i/vAmp but no radius on disk), ALFALFA a100 /"
  " Durbala+20 / Leisman+17 HUDs, FASHI DR2, MIGHTEE-HI (unresolved widths); LVD (no rotation column; WLM, NGC 6822, IC 1613, Leo A, Sag dIrr,"
  " Pegasus dIrr carry no rotation data on disk); no LITTLE THINGS / SHIELD / FIGGS / Leo P kinematics on disk.")
RES["inventory"] = INV

# =====================================================================================================================  analysis
def rot_delta(f, v3=False, S=None):
    S = SP if S is None else S
    go = S["go"] if not v3 else (S["V"] ** 2 + 2 * SIG_AD ** 2) * 1e6 / (S["R"] * KPC)
    return np.log10(go / (S["gb"] * nu_e15(S["gb"] / A0[f])))

def rot_cells(delta, cells, S=None):
    S = SP if S is None else S; k = np.digitize(np.log10(S["gb"]), GRID) - 1; out = {}
    for g in sorted(set(S["gal"])):
        m = S["gal"] == g; d = {}
        for c in cells:
            mm = m & (k == c)
            if mm.any(): d[c] = float(np.mean(delta[mm]))
        if d: out[g] = d
    return out

def boot_E(V, w, rng):
    n = V.shape[0]; idx = rng.integers(0, n, (NBOOT, n)); X = V[idx]
    with warnings.catch_warnings(), np.errstate(invalid="ignore", divide="ignore"):
        warnings.simplefilter("ignore"); m = np.nanmean(X, axis=1)
    ok = np.isfinite(m); ww = np.where(ok, w[None, :], 0.0); ww = ww / ww.sum(1, keepdims=True)
    return np.sum(np.where(ok, m, 0.0) * ww, 1)

def mat(groupd, cells):
    names = [g for g in groupd if any(c in groupd[g] for c in cells)]
    V = np.full((len(names), len(cells)), np.nan)
    for i, g in enumerate(names):
        for j, c in enumerate(cells):
            if c in groupd[g]: V[i, j] = groupd[g][c]
    return names, V

def classify(Nok, zref, zK, zE):
    if not Nok: return "NOT DIAGNOSTIC (DATA)"
    if not (zref >= ZK): return "NOT DIAGNOSTIC (NO LEVER)"
    if zK >= ZK and zE < ZK: return "E-FAVOURED"
    if zE >= ZK and zK < ZK: return "K-FAVOURED"
    return "NOT DIAGNOSTIC (INTERMEDIATE)" if (zK >= ZK and zE >= ZK) else "NOT DIAGNOSTIC (UNRESOLVED)"

def evaluate(gi, gii, giii, sdw, cells, floor, pairwise=False, seed=931):
    """gi, gii: {galaxy: {cell: mean Delta}}; giii: {dwarf: {cell: Delta}}; sdw: {dwarf: sigma_Delta}."""
    n_i = {c: sum(1 for g in gi if c in gi[g]) for c in cells}; n_ii = {c: sum(1 for g in gii if c in gii[g]) for c in cells}
    n_iii = {c: sum(1 for g in giii if c in giii[g]) for c in cells}
    if pairwise:
        cK = [c for c in cells if n_i[c] >= 1 and n_ii[c] >= 3]; cE = [c for c in cells if n_i[c] >= 1 and n_iii[c] >= 3]
    else:
        cK = cE = [c for c in cells if n_i[c] >= 1 and n_ii[c] >= 3 and n_iii[c] >= 3]
    out = dict(n_i=n_i, n_ii=n_ii, n_iii=n_iii, cells_K=cK, cells_E=cE)
    cU = sorted(set(cK) | set(cE))
    Ni = len([g for g in gi if any(c in gi[g] for c in cU)]); Nii = len([g for g in gii if any(c in gii[g] for c in cK)])
    Niii = len([g for g in giii if any(c in giii[g] for c in cE)])
    out.update(N_i=Ni, N_ii=Nii, N_iii=Niii)
    Nok = bool(cK) and bool(cE) and Ni >= 5 and Nii >= 5 and Niii >= 3
    if not (cK and cE):
        out.update(cls=classify(False, 0, 0, 0)); return out
    wK = np.array([n_i[c] for c in cK], float); wK /= wK.sum(); wE = np.array([n_i[c] for c in cE], float); wE /= wE.sum()
    rng = np.random.default_rng(seed)
    ni, Vi = mat(gi, cU); jK = [cU.index(c) for c in cK]; jE = [cU.index(c) for c in cE]
    nii, Vii = mat(gii, cK); niii, Viii = mat(giii, cE)
    with warnings.catch_warnings(), np.errstate(invalid="ignore"):
        warnings.simplefilter("ignore")
        mi = np.nanmean(Vi, 0); mii = np.nanmean(Vii, 0); miii = np.nanmean(Viii, 0)
    EiK = float(np.sum(wK * mi[jK])); EiE = float(np.sum(wE * mi[jE])); Eii = float(np.sum(wK * mii)); Eiii = float(np.sum(wE * miii))
    # bootstrap: group i drawn once over its union of cells (draw order i, ii, iii)
    idx = rng.integers(0, Vi.shape[0], (NBOOT, Vi.shape[0])); X = Vi[idx]
    with warnings.catch_warnings(), np.errstate(invalid="ignore", divide="ignore"):
        warnings.simplefilter("ignore"); m = np.nanmean(X, axis=1)
    def wsum(mm, w):
        ok = np.isfinite(mm); ww = np.where(ok, w[None, :], 0.0); ww = ww / ww.sum(1, keepdims=True); return np.sum(np.where(ok, mm, 0.0) * ww, 1)
    bK, bE = wsum(m[:, jK], wK), wsum(m[:, jE], wE); bii = boot_E(Vii, wK, rng); biii = boot_E(Viii, wE, rng)
    s_iK, s_iE, s_ii = float(np.std(bK, ddof=1)), float(np.std(bE, ddof=1)), float(np.std(bii, ddof=1))
    meas = math.sqrt(sum(wE[j] ** 2 * sum(sdw[g] ** 2 for g in niii if c in giii[g]) / n_iii[c] ** 2 for j, c in enumerate(cE)))
    s_iii = max(float(np.std(biii, ddof=1)), meas)
    s_idiff = float(np.std(bK - bE, ddof=1)) if pairwise else 0.0
    dK, dE = EiK - Eii, Eiii - EiE; dref = dK + dE
    sK = math.sqrt(s_iK ** 2 + s_ii ** 2 + 2 * floor ** 2); sE = math.sqrt(s_iii ** 2 + s_iE ** 2 + 2 * floor ** 2)
    sref = math.sqrt(s_idiff ** 2 + s_ii ** 2 + s_iii ** 2 + 2 * floor ** 2)
    zK, zE, zref = dK / sK, dE / sE, dref / sref
    out.update(E_i=EiK, E_i_Ecells=EiE, E_ii=Eii, E_iii=Eiii, s_i=s_iK, s_i_Ecells=s_iE, s_ii=s_ii, s_iii=s_iii, s_iii_boot=float(np.std(biii, ddof=1)),
               s_iii_meas=meas, d_K=dK, s_K=sK, z_K=zK, d_E=dE, s_E=sE, z_E=zE, lever=dref, s_lever=sref, z_lever=zref,
               MDD_K=MDDF * sK, MDD_E=MDDF * sE, w_K=wK.tolist(), w_E=wE.tolist(), names_i=ni, names_ii=nii, names_iii=niii,
               cls=classify(Nok, zref, zK, zE))
    return out

_RC_CACHE = {}
def groups(f, split, var, inj=0.0, inj_set=None, labels=None):
    """Build the three groups for footing f, split, variant; optional injection (dex) into the galaxies of inj_set (default:
    the true group i), optional relabelling (set of galaxy names to call group i)."""
    cells = W_V5 if var == "V5" else W_PRIMARY
    tgt = (frozenset(inj_set) if inj_set is not None else frozenset(g for g in GALS if MSTAR[g] < split)) if inj else frozenset()
    ck = (f, var == "V3", cells, float(inj), tgt)
    if ck not in _RC_CACHE:
        delta = rot_delta(f, v3=(var == "V3"))
        if inj: delta = delta + inj * np.isin(SP["gal"], sorted(tgt))
        _RC_CACHE[ck] = rot_cells(delta, cells)
    RC = _RC_CACHE[ck]
    isI = (lambda g: g in labels) if labels is not None else (lambda g: MSTAR[g] < split)
    gi = {g: v for g, v in RC.items() if isI(g)}; gii = {g: v for g, v in RC.items() if not isI(g)}
    dw = DWV4[f] if var == "V4" else DWD[f]; kd = np.digitize(dw["lg"], GRID) - 1
    lo = min((MSTAR[g] for g in gi), default=None) if var == "V7" else None
    giii, sdw = {}, {}
    for j, nm in enumerate(dw["names"]):
        if not (dw["Ms"][j] < split): continue
        if var == "V7" and (lo is None or dw["Ms"][j] < lo): continue
        if kd[j] in cells: giii[nm] = {int(kd[j]): float(dw["D"][j])}; sdw[nm] = float(dw["sD"][j])
    floor = {"V1": 0.0, "V2": 0.10}.get(var, FLOOR)
    return gi, gii, giii, sdw, cells, floor

def run(f, split, var, **kw):
    gi, gii, giii, sdw, cells, floor = groups(f, split, var, **kw)
    return evaluate(gi, gii, giii, sdw, cells, floor, pairwise=(var == "V6"))

def line(r):
    if "d_K" not in r: return f"{r['cls']}  (N_i {r['N_i']}, N_ii {r['N_ii']}, N_iii {r['N_iii']}; no eligible cell)"
    return (f"{r['cls']:30s} N {r['N_i']}/{r['N_ii']}/{r['N_iii']}  E(i) {r['E_i']:+.3f} E(ii) {r['E_ii']:+.3f} E(iii) {r['E_iii']:+.3f}  "
            f"d_K {r['d_K']:+.3f}+-{r['s_K']:.3f} (z {r['z_K']:+.1f})  d_E {r['d_E']:+.3f}+-{r['s_E']:.3f} (z {r['z_E']:+.1f})  "
            f"lever {r['lever']:+.3f}+-{r['s_lever']:.3f} (z {r['z_lever']:+.1f})  MDD_K {r['MDD_K']:.2f} MDD_E {r['MDD_E']:.2f}")

def main_token(c): return c.split(" (")[0]

# real V0 at every footing / split (needed by every mode)
REAL = {f: {sp_: run(f, sp_, "V0") for sp_ in SPLITS} for f in FOOTS}

def allows(r):                                                  # A1-1: data gate, lever gate, 2.84 sigma(d_K) <= 0.30
    if "d_K" not in r: return False, "no eligible cell"
    if not (r["N_i"] >= 5 and r["N_ii"] >= 5 and r["N_iii"] >= 3): return False, "data gate"
    if not (r["z_lever"] >= ZK): return False, f"lever gate (z {r['z_lever']:+.2f})"
    if not (r["MDD_K"] <= I30): return False, f"power (MDD_K {r['MDD_K']:.2f} > 0.30)"
    return True, "allowed"

# =====================================================================================================================  MUTATE inject
if MUT == "inject":
    P("\n=== MUTATE inject (I-30: +0.30 dex on every group-(i) point; I-E: group (i) shifted so E(i) = E(iii))")
    ok_all = True; MI = {}
    for f in FOOTS:
        for sp_ in SPLITS:
            r0 = REAL[f][sp_]; key = f"{f}|{sp_:.0e}"
            if "d_K" not in r0:
                MI[key] = dict(status="no eligible cell: not recoverable at this N", N_i=r0["N_i"]); P(f"  [{f} | {sp_:.0e}] no eligible cell (N_i {r0['N_i']}): I-30 / I-E not recoverable at this N"); continue
            r30 = run(f, sp_, "V0", inj=I30); shift = r30["d_K"] - r0["d_K"]
            pipe = abs(shift - I30) <= 1e-9 and abs(r30["s_K"] - r0["s_K"]) <= 1e-12 and abs(r30["lever"] - r0["lever"]) <= 1e-12
            al, why = allows(r0); rec = (main_token(r30["cls"]) == "E-FAVOURED") if al else None
            if not pipe or (al and not rec): ok_all = False
            rE = run(f, sp_, "V0", inj=r0["d_E"])
            MI[key] = dict(pipeline_ok=pipe, shift=shift, allowed=al, why=why, recovered=rec, I30=r30, IE=rE, IE_shift=r0["d_E"])
            P(f"  [{f} | {sp_:.0e}] I-30 pipeline: d_K moved {shift:+.12f} (s_K, lever unchanged) -> {'PASS' if pipe else 'FAIL'};  "
              f"N allows: {al} ({why});  I-30 class {r30['cls']}" + (f" -> {'RECOVERED' if rec else 'NOT RECOVERED'}" if al else " -> not required (reported)"))
            P(f"      I-30: {line(r30)}")
            P(f"      I-E (shift {r0['d_E']:+.3f}): {line(rE)}")
    RES["mutate_inject"] = MI; RES["mutate_ok"] = ok_all
    P(f"\n  MUTATE inject: {'all required controls met' if ok_all else 'A REQUIRED CONTROL FAILED'}")
    finish(0 if ok_all else 1)

# =====================================================================================================================  MUTATE shuffle
if MUT == "shuffle":
    P("\n=== MUTATE shuffle (S1: labels shuffled on the I-30 data, rng 9311; S2: real-data permutation p of d_K, rng 9312)")
    ok_all = True; MS = {}
    for f in FOOTS:
        for sp_ in SPLITS:
            r0 = REAL[f][sp_]; key = f"{f}|{sp_:.0e}"
            if "d_K" not in r0 or not (r0["N_i"] >= 5 and r0["N_ii"] >= 5 and r0["N_iii"] >= 3):
                MS[key] = dict(status="data gate fails: shuffle not run"); P(f"  [{f} | {sp_:.0e}] data gate fails (N_i {r0['N_i']}): S1/S2 not run"); continue
            pool = sorted(set(r0["names_i"]) | set(r0["names_ii"])); Ni = len(r0["names_i"]); true_i = set(r0["names_i"])
            r30 = run(f, sp_, "V0", inj=I30, inj_set=true_i); al, why = allows(r0)
            rng = np.random.default_rng(9311); dks, ef = [], 0
            for t in range(1000):
                lab = set(rng.choice(pool, Ni, replace=False).tolist()); rs = run(f, sp_, "V0", inj=I30, inj_set=true_i, labels=lab)
                if "d_K" in rs: dks.append(rs["d_K"]); ef += main_token(rs["cls"]) == "E-FAVOURED"
            med = float(np.median(dks)); frac = ef / 1000; bite = (med <= 0.5 * r30["d_K"]) and (frac <= 0.10)
            if al and not bite: ok_all = False
            rng2 = np.random.default_rng(9312); dk2 = []
            for t in range(1000):
                lab = set(rng2.choice(pool, Ni, replace=False).tolist()); rs = run(f, sp_, "V0", labels=lab)
                if "d_K" in rs: dk2.append(rs["d_K"])
            p_one = float(np.mean(np.array(dk2) >= r0["d_K"])); p_two = float(np.mean(np.abs(np.array(dk2)) >= abs(r0["d_K"])))
            MS[key] = dict(allowed=al, why=why, dK_I30=r30["d_K"], cls_I30=r30["cls"], S1_median_dK=med, S1_frac_E=frac, S1_bites=bite,
                           S1_n=len(dks), S2_dK_real=r0["d_K"], S2_p_one_sided=p_one, S2_p_two_sided=p_two, S2_n=len(dk2))
            P(f"  [{f} | {sp_:.0e}] S1 on I-30: true d_K {r30['d_K']:+.3f} ({r30['cls']}); shuffled median d_K {med:+.3f}, E-FAVOURED in {100 * frac:.1f}% "
              f"-> {'BITES' if bite else 'DOES NOT BITE'} ({'required' if al else 'not required: ' + why})")
            P(f"      S2 real data: d_K {r0['d_K']:+.3f}; permutation p (d_K_shuf >= real) {p_one:.3f}, two-sided {p_two:.3f}  (no class weight)")
    RES["mutate_shuffle"] = MS; RES["mutate_ok"] = ok_all
    P(f"\n  MUTATE shuffle: {'all required controls met' if ok_all else 'A REQUIRED CONTROL FAILED'}")
    finish(0 if ok_all else 1)

# =====================================================================================================================  MAIN
P("\n=== Main (dex; Delta = log10(g_obs/g_law), nu_e; floor 0.05 dex per group mean)")
MAIN = {}
for f in FOOTS:
    MAIN[f] = {}
    for sp_ in SPLITS:
        MAIN[f][f"{sp_:.0e}"] = {v: (REAL[f][sp_] if v == "V0" else run(f, sp_, v)) for v in VARIANTS}
for sp_ in SPLITS:
    tag = "PRIMARY" if sp_ == PRIMARY_SPLIT else "EXTENDED (E')"
    P(f"\n  --- split M* = {sp_:.0e}  [{tag}]")
    for f in FOOTS:
        P(f"   [{f}]")
        for v in VARIANTS:
            P(f"     {v:3s} {VDESC[v]:34s} {line(MAIN[f][f'{sp_:.0e}'][v])}")
# per-cell detail at the extended split 1e8 (V0)
P("\n  V0 cell detail (cell: n_i/n_ii/n_iii; group cell means i/ii/iii), canonical:")
for sp_ in SPLITS:
    gi, gii, giii, sdw, cells, floor = groups("canonical", sp_, "V0")
    for c in cells:
        mi = [gi[g][c] for g in gi if c in gi[g]]; mii = [gii[g][c] for g in gii if c in gii[g]]; miii = [giii[g][c] for g in giii if c in giii[g]]
        f3 = lambda x: f"{np.mean(x):+.3f}" if x else "  -   "
        P(f"    split {sp_:.0e} cell [{GRID[c]:.1f},{GRID[c] + 0.5:.1f}): {len(mi)}/{len(mii)}/{len(miii)};  {f3(mi)} / {f3(mii)} / {f3(miii)}")
    if sp_ == 1e8:
        P("    group (i) galaxies at 1e8 (window mean Delta, canonical): " + ", ".join(f"{g} {np.mean(list(gi[g].values())):+.2f}" for g in sorted(gi, key=lambda g: MSTAR[g])))

# classes
CLS = {}
for sp_ in SPLITS:
    k = f"{sp_:.0e}"; per = {f: MAIN[f][k]["V0"]["cls"] for f in FOOTS}
    toks = {f: main_token(per[f]) for f in FOOTS}
    overall = per["canonical"] if per["canonical"] == per["alt"] else (toks["canonical"] if toks["canonical"] == toks["alt"] else "NOT DIAGNOSTIC (SPLIT BY FOOTING)")
    changing = [f"{v}/{f}: {MAIN[f][k][v]['cls']}" for f in FOOTS for v in VARIANTS[1:] if main_token(MAIN[f][k][v]["cls"]) != toks[f]]
    sublabel = [f"{v}/{f}: {MAIN[f][k][v]['cls']}" for f in FOOTS for v in VARIANTS[1:]
                if main_token(MAIN[f][k][v]["cls"]) == toks[f] and MAIN[f][k][v]["cls"] != per[f]]
    if sp_ != PRIMARY_SPLIT and main_token(overall) == "E-FAVOURED": overall = overall.replace("E-FAVOURED", "E'-FAVOURED")
    CLS[k] = dict(per_footing=per, overall=overall, fragile=bool(changing), variants_changing=changing, sublabel_changes=sublabel)
    P(f"\n  CLASS split {k} ({'PRIMARY' if sp_ == PRIMARY_SPLIT else 'extended, secondary'}): {overall}" + ("  [FRAGILE]" if changing else "")
      + f"   (canonical {per['canonical']}; alt {per['alt']})")
    if changing: P("    variants changing the class: " + "; ".join(changing))
    if sublabel: P("    sub-label changes only: " + "; ".join(sublabel))
RES["main"] = MAIN; RES["classes"] = CLS
RES["lane_class"] = CLS[f"{PRIMARY_SPLIT:.0e}"]["overall"]
RES["secondary_class"] = {k: CLS[k]["overall"] + ("  [FRAGILE]" if CLS[k]["fragile"] else "") for k in CLS if k != f"{PRIMARY_SPLIT:.0e}"}
P(f"\n=== LANE CLASS (primary split 1e7): {RES['lane_class']}")
P("=== secondary (extended E' splits): " + "; ".join(f"{k}: {v}" for k, v in RES["secondary_class"].items()))

# =====================================================================================================================  INFO lines (no class weight)
P("\n=== INFO (no class weight)")
INFO = {}
S444 = load_sparc(cut=False, only="UGCA444")
for f in FOOTS:
    d444 = rot_delta(f, S=S444); c444 = rot_cells(d444, W_PRIMARY, S=S444).get("UGCA444", {})
    gi, gii, giii, sdw, cells, floor = groups(f, 1e7, "V0")
    rows = {}
    for c in W_PRIMARY:
        mii = [gii[g][c] for g in gii if c in gii[g]]; miii = [giii[g][c] for g in giii if c in giii[g]]
        rows[str(c)] = dict(ugca444=c444.get(c), n444=int(np.sum(np.digitize(np.log10(S444["gb"]), GRID) - 1 == c)),
                            high_rot=float(np.mean(mii)) if mii else None, n_high=len(mii), dsph=float(np.mean(miii)) if miii else None, n_dsph=len(miii))
    INFO[f"UGCA444|{f}"] = rows
    P(f"  A1-3 UGCA 444 (M* 6.0e6; NO point cut; errV/V >= 0.10 on every point) [{f}]: " + "  ".join(
        f"[{GRID[int(c)]:.1f},{GRID[int(c)] + 0.5:.1f}) UGCA444 {('%+.2f' % v['ugca444']) if v['ugca444'] is not None else '  -  '} ({v['n444']} pts) | "
        f"rot M*>=1e7 {('%+.2f' % v['high_rot']) if v['high_rot'] is not None else '  -  '} ({v['n_high']}) | dSph M*<1e7 {('%+.2f' % v['dsph']) if v['dsph'] is not None else '  -  '} ({v['n_dsph']})"
        for c, v in rows.items()))
TD = list(csv.DictReader(l for l in builtins.open(os.path.join(REPO, "real_research", "data", "tdg", "lelli2015_tdgs.csv")) if not l.startswith("#")))
TS = {r["object"].replace(" ", ""): r for r in csv.DictReader(builtins.open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv")))}
for f in FOOTS:
    rows = []
    for r in TD:
        Rm = float(r["Rout"]) * KPC; gb = G * float(r["Mbar"]) * 1e8 * MSUN / Rm ** 2; go = (float(r["Vcirc"]) * 1e3) ** 2 / Rm
        Ms = float(TS[r["name"]]["M_star_1e8"]) * 1e8 if r["name"] in TS else None
        rows.append(dict(name=r["name"], lgbar=math.log10(gb), Delta=math.log10(go / (gb * float(nu_e15(gb / A0[f])))), Ms=Ms,
                         sDelta=2 * float(r["eVcirc"]) / (float(r["Vcirc"]) * LN10)))
    INFO[f"TDG|{f}"] = rows
    P(f"  TDGs (Lelli+15; single point at R_out, M_bar inside; INFO) [{f}]: " + "; ".join(
        f"{x['name']} M* {x['Ms']:.1e} log g_bar {x['lgbar']:.2f} Delta {x['Delta']:+.2f}+-{x['sDelta']:.2f}" for x in rows))
    P(f"      TDG mean Delta {np.mean([x['Delta'] for x in rows]):+.3f} (N {len(rows)}; log g_bar {min(x['lgbar'] for x in rows):.2f}..{max(x['lgbar'] for x in rows):.2f})")
RES["info"] = INFO
finish(0)
