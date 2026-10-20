"""CFG914 -- one common density threshold for the law's open excesses (dwarfs, red lenses, cluster cores)?
Criteria: FROZEN_CRITERIA.md (6ec526287, committed alone before this script).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg914.py      (CFG914_MUTATE=shuffle|inject -> separate outputs named by mode).
Inputs: committed lane outputs and the repo's raw data files only (CFG880/828/870/829/850/912/687/883); source code of those lanes
is exec'd read-only where noted.  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; not theory closed."""
import os, sys, csv, json, math, re, glob, time, resource, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import chi2, norm, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG914_MUTATE", ""); assert MUT in ("", "shuffle", "inject"); SUF = f"_MUTATE_{MUT}" if MUT else ""
for _e in ("CFG880_MUTATE", "CFG829_MUTATE", "CFG850_MUTATE", "CFG883_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
G = 6.674e-11; MSUN = 1.989e30; PCM = 3.0857e16; KPCM = 3.0857e19; CLIGHT = 2.998e8
RHO_UNIT = MSUN / PCM ** 3                                   # kg/m^3 per Msun/pc^3
FLOOR0 = 0.05 * math.log(10)                                 # 0.05 dex in g, in E units
LN10 = math.log(10)
def lrho(g, r_m):                                            # log10 of 3 g / (4 pi G r) in Msun/pc^3
    return np.log10(3 * np.asarray(g, float) / (4 * math.pi * G * np.asarray(r_m, float)) / RHO_UNIT)
SECTORS = ("DW", "SS", "SL", "LR", "LB", "CL", "GC")
FAILING, DIFFUSE = ("DW", "LR", "CL"), ("SS", "SL", "LB")
SNAME = {"DW": "dwarfs (83 LVD)", "SS": "SPARC small (Mb<=3e9)", "SL": "SPARC large", "LR": "red lenses (B21)",
         "LB": "blue lenses (B21)", "CL": "eRASS1 clusters MID+OUTER", "GC": "globulars (tidally safe)"}
GRID = np.arange(-20.0, 10.0001, 0.5)                        # fixed 0.5-dex edges (log rho or log g)
def J(*p): return json.load(open(os.path.join(LANES, *p)))
def xslice(path, start=None, stop=None, ns=None):
    src = open(path).read()
    if start is not None: src = start + src.split(start, 1)[1]
    if stop is not None: src = src.split(stop, 1)[0]
    ns = ns if ns is not None else {"__file__": path, "__name__": "ro_exec"}
    exec(compile(src, path, "exec"), ns); return ns
RES = dict(lane="CFG914", criteria="6ec526287", mutate=MUT or None, checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return ok

P("CFG914  common density threshold across sectors?  E = ln(g_obs/g_law);  primary rho = 3 g_law/(4 pi G r), V1 rho = 3 g_bar/(4 pi G r)"
  + (f"   [MUTATE {MUT}]" if MUT else ""))

# =====================================================================================================================  DWARFS
P("\n=== inputs and K-tests")
F880 = os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880.py")
N880 = xslice(F880, stop="# ---------------- hierarchical likelihood ----------------")
R880 = J("CFG880_clump_sigma_universality", "cfg880_results.json")
DWR = {}
k1 = []; k1b = []
for f in FOOTS:
    a0 = A0[f]; A = N880["arrays"](N880["SAMP"], a0); law = np.sqrt(A["sl2"]); r12m = A["r12"] * PCM
    rows = {r["name"]: r for r in R880[f]["primary"]["rows"]}
    assert len(rows) == len(A["names"]) == 83
    k1.append(max(abs(law[i] / rows[nm]["law"] - 1) for i, nm in enumerate(A["names"])))
    pu = N880["sig_pred"](A["sl2"], A["r12"], R880[f]["primary"]["sbar_univ"], a0)
    k1b.append(max(abs(pu[i] / rows[nm]["pred_univ"] - 1) for i, nm in enumerate(A["names"])))
    gN = []
    for nm, r12pc in zip(A["names"], A["r12"]):
        L = N880["LVD"][nm]; Ms = 2.0 * 10 ** (0.4 * (4.83 - N880["fnum"](L["M_V"])))
        Mg = N880["gas_in"](N880["fnum"](L.get("mass_HI")), r12pc); gN.append(N880["G"] * (Ms / 2 + Mg) * N880["Msun"] / (r12pc * N880["PC"]) ** 2)
    gN = np.array(gN); gl = 3 * A["sl2"] * 1e6 / r12m
    assert np.max(np.abs(gN * N880["nu"](gN / a0) / gl - 1)) < 1e-12        # internal identity: g_law = g_N nu(g_N/a0)
    s = A["s"]; E = 2 * np.log(s / law); e = np.where(s > law, A["em"], A["ep"]); sE = 2 * e / s
    DWR[f] = dict(names=list(A["names"]), E=E, sE=sE, law=lrho(gl, r12m), bar=lrho(gN, r12m), gbar=np.log10(gN),
                  obs=lrho(3 * (s * 1e3) ** 2 / r12m, r12m), r12=A["r12"], sigma=s, sig_law=law, MV=A["MV"])
check("K1 dwarfs: sigma_law = CFG880 committed law (83 x 2 footings)", max(k1) <= 1e-9, f"max rel {max(k1):.1e}")
check("K1b dwarfs: CFG880 pred_univ from committed sigma_bar_univ", max(k1b) <= 1e-9, f"max rel {max(k1b):.1e}")

# =====================================================================================================================  SPARC
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_e12 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
Q28, Q70 = {}, {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q28[v[0]] = (float(v[5]), int(v[17]))
        except ValueError: pass
        try: Q70[v[0]] = dict(inc=float(v[5]), q=int(v[17]), Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9)
        except Exception: pass
SP = dict(gal=[], R=[], gb=[], go=[], Vobs=[], eV=[], Vg=[], Vd=[], Vb=[])
for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", ""); inc, q = Q28.get(name, (0, 3))
    if q > 2 or inc < 30: continue
    for l in open(fn):
        if l.startswith("#") or not l.strip(): continue
        R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
        if V <= 0 or R <= 0 or eV / V >= 0.10: continue
        g_b = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPCM)
        if g_b <= 0: continue
        SP["gal"].append(name); SP["R"].append(R); SP["gb"].append(g_b); SP["go"].append(V * V * 1e6 / (R * KPCM))
        for k, x in (("Vobs", V), ("eV", eV), ("Vg", Vg), ("Vd", Vd), ("Vb", Vb)): SP[k].append(x)
for k in SP:
    if k != "gal": SP[k] = np.array(SP[k])
SP["gal"] = np.array(SP["gal"])
R828 = J("CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")
k2 = [abs(len(SP["gb"]) - R828["n_sparc"])]
for f in FOOTS:
    med = float(np.median(np.log10(SP["go"] / (SP["gb"] * nu_e12(SP["gb"] / A0[f])))))
    k2.append(abs(med - R828[f"{f}|nu_e"]["sparc_median_all"]))
check("K2a SPARC: CFG828 n_sparc and overall median (both footings)", max(k2) <= 1e-12, f"n {len(SP['gb'])} vs {R828['n_sparc']}; max |d median| {max(k2[1:]):.1e}")
R870 = J("CFG870_cored_component_joint", "cfg870_results.json")
def sparc870(a0, Vx, RCc=104.0):                             # CFG870's sparc(), copied (K2b)
    gal = []
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        nm = os.path.basename(fn).replace("_rotmod.dat", ""); g = Q70.get(nm)
        if not g or g["q"] > 2 or g["inc"] < 30 or g["Mb"] > 3e9: continue
        d_ = []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(t) for t in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10: continue
            gbar = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPCM)
            if gbar <= 0: continue
            gl = float(gbar * nu_e(gbar / a0)); go = V * V * 1e6 / (R * KPCM)
            gx = (Vx * 1e3) ** 2 * (R * KPCM) / ((R * KPCM) ** 2 + (RCc * PCM) ** 2)
            d_.append(math.log10(go / gl) - math.log10((gl + gx) / gl))
        if d_: gal.append(float(np.median(d_)))
    D = np.array(gal); rng = np.random.default_rng(870); bs = [rng.choice(D, len(D)).mean() for _ in range(2000)]
    return float(D.mean()), float(np.std(bs)), len(D)
k2b = []
for f in FOOTS:
    D_, sD_, _ = sparc870(A0[f], R870[f]["Vx"]); k2b += [abs(D_ - R870[f]["sparc_D"]), abs(sD_ - R870[f]["sparc_sD"])]
check("K2b SPARC: CFG870 sparc_D and bootstrap sigma with committed V_x (both footings)", max(k2b) <= 1e-12, f"max |diff| {max(k2b):.1e}")
Mb_gal = np.array([Q70[g]["Mb"] if g in Q70 else np.nan for g in SP["gal"]])
n_noMb = len(set(SP["gal"][~np.isfinite(Mb_gal)]))
SPR = {}
for f in FOOTS:
    gl = SP["gb"] * nu_e(SP["gb"] / A0[f]); Rm = SP["R"] * KPCM
    SPR[f] = dict(E=np.log(SP["go"] / gl), law=lrho(gl, Rm), bar=lrho(SP["gb"], Rm), gbar=np.log10(SP["gb"]), obs=lrho(SP["go"], Rm))
SMALL = np.isfinite(Mb_gal) & (Mb_gal <= 3e9); LARGE = np.isfinite(Mb_gal) & (Mb_gal > 3e9)
P(f"  SPARC: {len(SP['gb'])} points, {len(set(SP['gal']))} galaxies; small {SMALL.sum()} pts / {len(set(SP['gal'][SMALL]))} gal, "
  f"large {LARGE.sum()} pts / {len(set(SP['gal'][LARGE]))} gal; galaxies without M_b in the master table: {n_noMb}")

# =====================================================================================================================  LENSING
F829 = os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py")
N829 = xslice(F829, stop='P("CFG829  KiDS')
load, amp829, nu_e829 = N829["load"], N829["amp"], N829["nu_e"]
FL = {"blue": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
      "red": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
      "disc": ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
      "sph": ("Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0)}
W850 = (10 ** -13.3, 10 ** -11.9)
R850 = J("CFG850_red_split_mstar_systematic", "cfg850_results.json")["rows"]
k3 = []
LDAT = {k: load(*FL[k]) for k in FL}
for f in FOOTS:
    def A850(k, sh):
        gb, go, C = LDAT[k]; gbs = gb * 10 ** sh; return amp829(gbs, go, C, gbs * nu_e829(gbs / A0[f]), W850)
    r, b = A850("red", 0.123), A850("blue", 0.0); z = (r["A"] - b["A"]) / math.hypot(r["sA"], b["sA"])
    ref = R850[f"{f}|0.123|0.0"]; k3 += [abs(r["A"] - ref["A_red"]), abs(b["A"] - ref["A_blue"]), abs(z - ref["z_colour"])]
R829 = J("CFG829_lensing_low_g_vs_dwarf_excess", "cfg829_results.json")
gb, go, C = LDAT["blue"]; a829 = amp829(gb, go, C, gb * nu_e829(gb / A0["canonical"]), W850)
k3.append(abs(a829["A"] - R829["canonical|nu_e|blue (u-r<2.5)"]["window"]["A"]))
check("K3 lensing: CFG850 (+0.123, 0) rows both footings and CFG829 blue window A", max(k3) <= 1e-9, f"max |diff| {max(k3):.1e}")
col = open(os.path.join(LANES, "CFG912_red_excess_two_halo", "cfg912_colour.out")).read()
mm = re.search(r"median log Mgal red\(2\.0\) ([0-9.]+) / blue\(2\.0\) ([0-9.]+)", col); n0 = re.search(r"I0: red\(2\.0\) ([0-9,]+)", col)
LM_MED = {"red": float(mm.group(1)), "blue": float(mm.group(2))}
check("K3b lens medians parsed from cfg912_colour.out", LM_MED == {"red": 10.81, "blue": 10.45}, f"red {LM_MED['red']} blue {LM_MED['blue']} (I0 red {n0.group(1)})")
LWIN = (10 ** -13.3, 10 ** -10.9)
def lens_points(colour, f, shift, dlm=0.0):
    gb, go, C = LDAT[colour]; gbs = gb * 10 ** shift; gl = gbs * nu_e829(gbs / A0[f])
    m = (gbs >= LWIN[0]) & (gbs < LWIN[1]); Ml = 10 ** (LM_MED[colour] + shift + dlm) * MSUN
    R = np.sqrt(G * Ml / gbs)
    return dict(gb=gbs[m], go=go[m], gl=gl[m], C=C[np.ix_(m, m)], law=lrho(gl[m], R[m]), bar=lrho(gbs[m], R[m]),
                gbar=np.log10(gbs[m]), obs=lrho(np.where(go[m] > 0, go[m], np.nan), R[m]), R_kpc=R[m] / KPCM)

# =====================================================================================================================  CLUSTERS
sys.path.insert(0, LANES); import CFG4_common as C4
nu_mono = C4.nu_mono
D687 = os.path.join(LANES, "CFG687_erass1_shear_stack")
NPZ = np.load(os.path.join(D687, "cfg687_percluster.npz"))
CD, CE, CPL, Cmg, CR5, Cra = NPZ["D"], NPZ["E"], NPZ["PL"], NPZ["mg"], NPZ["R500"], NPZ["ra"]
R687 = J("CFG687_erass1_shear_stack", "cfg687_results.json")
G6, MSUN6, MPC6 = 6.674e-11, 1.989e30, 3.0857e22; KG6 = MSUN6 / (3.0857e16) ** 2         # cfg686_shear.py constants
RGRID = np.logspace(-3, np.log10(30), 3000); U_GRID = np.linspace(0, 1, 4001)
EDGES6 = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC6 = np.sqrt(EDGES6[1:] * EDGES6[:-1])
def sigma_proj(rhoL, r, R):                                  # cfg686_shear.py RUN3 projector, copied
    umax = np.arccosh(r[-1] / R); u = U_GRID * umax; rr = R * np.cosh(u)
    lr = np.log(r); pos = rhoL > 0
    rho_u = np.exp(np.interp(np.log(rr), lr[pos], np.log(rhoL[pos])))
    return 2 * np.trapz(rho_u * rr * MPC6, u)
def law687(R500, Mgas500, a0, beta=2 / 3, rcf=0.15, fs=0.20):   # cfg687_stack.py law(), copied; also returns Mb, ML at RC
    r = RGRID; rc = rcf * R500; shape = (1 + (r / rc) ** 2) ** (-1.5 * beta); shape[r > 3.0] = 0
    dm = 4 * np.pi * (r * MPC6) ** 2 * shape; M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC6))]
    Mg = M * (Mgas500 * MSUN6 / np.interp(R500, r, M)); Mb = Mg * (1 + fs); gb = G6 * Mb / (r * MPC6) ** 2
    gL = gb * nu_mono(gb / a0) if a0 > 0 else gb; ML = gL * (r * MPC6) ** 2 / G6; rhoL = np.gradient(ML, r * MPC6) / (4 * np.pi * (r * MPC6) ** 2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC6])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4 * np.pi * (r[r > R] * MPC6) ** 2 * rhoL[r > R] * (1 - np.sqrt(1 - (R / r[r > R]) ** 2)), r[r > R] * MPC6) for R in RC6])
    return (M2 / (np.pi * (RC6 * MPC6) ** 2) - Sig) / KG6, np.interp(RC6, r, Mb), np.interp(RC6, r, ML)
NCL = len(CD); CLP, CLMb, CLML = {}, {}, {}
for f in FOOTS:
    out = [law687(CR5[i], Cmg[i], C4.A0[f]) for i in range(NCL)]   # CFG687's own a0: FP0 unrounded (CFG4_common.A0), as in the source lane
    CLP[f] = np.array([o[0] for o in out]); CLMb[f] = np.array([o[1] for o in out]); CLML[f] = np.array([o[2] for o in out])
k4a = float(np.max(np.abs(CLP["canonical"] / CPL - 1)))
CW = np.where(CE > 0, 1 / CE ** 2, 0)
order = np.argsort(Cra); PATCH = np.empty(NCL, int); PATCH[order] = np.arange(NCL) * 30 // NCL
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
def jk687(fun):
    full = fun(np.ones(NCL, bool)); reps = [fun(PATCH != p) for p in range(30)]
    return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}
k4b = []
for f in FOOTS:
    Pm = CLP[f]
    got = jk687(lambda s: {b: (CW[s][:, j] * CD[s][:, j]).sum() / (CW[s][:, j] * Pm[s][:, j]).sum() for b, j in BANDS.items()})
    ref = R687["A"][f"{f}|b0.67|rc0.15|f0.20"]
    for b in BANDS: k4b += [abs(got[b][0] / ref[b][0] - 1), abs(got[b][1] / ref[b][1] - 1)]
check("K4a clusters: recomputed canonical law = cfg687_percluster.npz PL (318 x 8)", k4a <= 1e-9, f"max rel {k4a:.1e} (cluster law uses CFG687's FP0 a0: {C4.A0['canonical']:.6e} / {C4.A0['alt']:.6e})")
check("K4b clusters: CFG687 primary A (INNER/MID/OUTER, value + jackknife) both footings", max(k4b) <= 1e-9, f"max rel {max(k4b):.1e}")
CLR = {}
for f in FOOTS:
    Rm = RC6[None, :] * MPC6
    CLR[f] = dict(law=lrho(G6 * CLML[f] / Rm ** 2, Rm), bar=lrho(G6 * CLMb[f] / Rm ** 2, Rm), gbar=np.log10(G6 * CLMb[f] / Rm ** 2))

# =====================================================================================================================  GLOBULARS
F883 = os.path.join(LANES, "CFG883_no_cooling_systems", "cfg883.py")
N883 = xslice(F883, stop='P("CFG883  no-atomic-cooling')
N883 = xslice(F883, start="def num1(s):", stop="def run_cluster(", ns=N883)
R883 = J("CFG883_no_cooling_systems", "cfg883_results.json")
GCR = {f: [] for f in FOOTS}; k5 = []; nsafe = {}
for row in R883["T1"]["rows"]:
    nm = row["name"]; p = N883["PAR"][nm]; bins = [x for x in N883["BINS"][nm] if x["typ"] == "RV"]
    R = np.array([b["Ras"] * p["Rsun"] * 1e3 / 206264.806 for b in bins]); keep = R < p["rt"]; bins = [b for b, k in zip(bins, keep) if k]; R = R[keep]
    rc = N883["king_rc_for"](p["rhl"], p["rt"]); tr = N883["Tracer"]("king", rc=rc, rt=p["rt"]) if rc else N883["Tracer"]("plummer", a=p["rhl"])
    LV = p["Mass"] / p["MLV"]; kst = tr.sig2(R, lambda r: np.interp(r, tr.r, tr.Mstar)); s = np.array([b["s"] for b in bins])
    base0 = np.sqrt(1.6 * LV * kst)
    for f in FOOTS:
        d = row["foot"][f]
        if not d["safe"]: continue
        k5 += [float(np.max(np.abs(R / np.array(row["R_pc"]) - 1))), float(np.max(np.abs(s / np.array(d["s_obs"]) - 1))),
               float(np.max(np.abs(base0 / np.array(d["s_B"]) - 1)))]
        i = int(np.argmax(R)); eu, el = N883["lnerr"](bins[i]["s"], bins[i]["up"], bins[i]["lo"])
        e = eu if base0[i] > s[i] else el
        sE = math.sqrt((2 * math.sqrt(e ** 2 + 0.05 ** 2)) ** 2 + (0.15 * LN10) ** 2)
        Mout = 1.6 * LV * float(np.interp(R[i], tr.r, tr.Mstar)); rb = 3 * Mout / (4 * math.pi * R[i] ** 3)
        r12 = 4 / 3 * p["rhl"] * N883["PC"]; yext = N883["G"] * N883["MW_MB"] * N883["Msun"] / (p["RGC"] * N883["KPC"]) ** 2 / A0[f]
        Befe = float(N883["nu"](N883["G"] * (1.6 * LV * N883["Msun"] / 2) / r12 ** 2 / A0[f] + yext))
        E = 2 * math.log(s[i] / base0[i])
        GCR[f].append(dict(name=nm, R_out=float(R[i]), nstar=int(row["nstar"]), E=E, sE=sE, law=math.log10(rb), bar=math.log10(rb),
                           gbar=math.log10(G * Mout * MSUN / (R[i] * PCM) ** 2), obs=math.log10(rb) + E / LN10,
                           E_efe=E - math.log(Befe), law_efe=math.log10(rb * Befe), s_obs=float(s[i]), s_N=float(base0[i])))
for f in FOOTS: nsafe[f] = len(GCR[f])
check("K5 globulars: CFG883 primary rows (R_pc, s_obs, s_B at Ups 1.6) for the tidally safe set; 31 per footing",
      max(k5) <= 1e-9 and all(nsafe[f] == R883["T1"]["summary"]["foot"][f]["N"] == 31 for f in FOOTS), f"max rel {max(k5):.1e}; N {nsafe}")
P(f"  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB] inputs loaded")

# =====================================================================================================================  BINNING
def bins_persystem(lr, E, sE, nb):
    ok = np.isfinite(lr); lr, E, sE = lr[ok], E[ok], sE[ok]; nb = max(1, min(nb, len(lr) // 2))
    out = []
    for g in np.array_split(np.argsort(lr, kind="stable"), nb):
        n = len(g); se = max(np.std(E[g], ddof=1) / math.sqrt(n), math.sqrt(np.sum(sE[g] ** 2)) / n)
        out.append(dict(lr=float(np.mean(lr[g])), E=float(np.mean(E[g])), se=float(se), n=n, lo=float(lr[g].min()), hi=float(lr[g].max())))
    return [b["lr"] for b in out], [b["E"] for b in out], np.diag([b["se"] ** 2 for b in out]), out

def bins_sparc(lr, E, gal, rng):
    ok = np.isfinite(lr); lr, E, gal = lr[ok], E[ok], gal[ok]
    k = np.digitize(lr, GRID) - 1; G_ = sorted(set(gal)); gi = {g: i for i, g in enumerate(G_)}; ig = np.array([gi[g] for g in gal])
    ub = sorted(set(k)); nG, nB = len(G_), len(ub); Msum = np.zeros((nG, nB)); Mn = np.zeros((nG, nB)); Lsum = np.zeros((nG, nB))
    for j, b in enumerate(ub):
        m = k == b; np.add.at(Msum[:, j], ig[m], E[m]); np.add.at(Mn[:, j], ig[m], 1); np.add.at(Lsum[:, j], ig[m], lr[m])
    with np.errstate(invalid="ignore", divide="ignore"):
        Mg_ = Msum / Mn; Lg_ = Lsum / Mn
    ngal = (Mn > 0).sum(0); keep = ngal >= 5
    Mg_, Lg_, ngal = Mg_[:, keep], Lg_[:, keep], ngal[keep]
    val = np.nanmean(Mg_, 0); lrb = np.nanmean(Lg_, 0)
    BS = np.empty((1000, Mg_.shape[1]))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for t in range(1000):
            idx = rng.integers(0, nG, nG); BS[t] = np.nanmean(Mg_[idx], 0)
    nb = len(val); C = np.empty((nb, nb))
    for a in range(nb):
        for b in range(nb):
            m = np.isfinite(BS[:, a]) & np.isfinite(BS[:, b]); x, y = BS[m, a], BS[m, b]
            C[a, b] = np.mean((x - x.mean()) * (y - y.mean())) * len(x) / max(len(x) - 1, 1)
    info = [dict(lr=float(lrb[j]), E=float(val[j]), se=float(math.sqrt(C[j, j])), n=int(ngal[j])) for j in range(nb)]
    return list(lrb), list(val), C, info

def bins_lens(Lp, var, lr_override=None):
    lr = Lp[var] if lr_override is None else lr_override; ok = np.isfinite(lr)
    k = np.where(ok, np.digitize(np.where(ok, lr, 0), GRID) - 1, -999); go, gl, C = Lp["go"], Lp["gl"], Lp["C"]; n = len(go)
    Ws, info = [], []
    for b in sorted(set(k[ok])):
        S = np.where(k == b)[0]; Ci = np.linalg.inv(C[np.ix_(S, S)]); a = gl[S] @ Ci @ gl[S]
        w = np.zeros(n); w[S] = (Ci @ gl[S]) / a; A = float(w @ go); sA = math.sqrt(float(w @ C @ w))
        if A <= 0 or sA / A > 1: continue
        ww = np.abs(w[S] * gl[S]); ww = ww / ww.sum()
        Ws.append(w); info.append(dict(lr=float(np.sum(ww * lr[S])), A=A, sA=sA, n=len(S)))
    if not Ws: return [], [], np.zeros((0, 0)), []
    Wm = np.array(Ws); CA = Wm @ C @ Wm.T; Av = np.array([i["A"] for i in info])
    CEm = CA / np.outer(Av, Av)
    for j, i in enumerate(info): i["E"] = math.log(i["A"]); i["se"] = math.sqrt(CEm[j, j])
    return [i["lr"] for i in info], [i["E"] for i in info], CEm, info

def bins_clusters(LR2, P2, jsel):
    lr = LR2[:, jsel]; D = CD[:, jsel]; W = CW[:, jsel]; Pm = P2[:, jsel]; cid = np.repeat(np.arange(NCL)[:, None], len(jsel), 1)
    k = np.digitize(lr, GRID) - 1; info, cols = [], []
    for b in sorted(set(k.ravel())):
        m = k == b
        if len(set(cid[m])) < 20 or (W[m] * Pm[m]).sum() <= 0: continue
        A = (W[m] * D[m]).sum() / (W[m] * Pm[m]).sum()
        if A <= 0: continue
        reps = []
        for p in range(30):
            mp = m & (PATCH[:, None] != p); reps.append((W[mp] * D[mp]).sum() / (W[mp] * Pm[mp]).sum())
        wl = (W[m] * Pm[m]); info.append(dict(lr=float((wl * lr[m]).sum() / wl.sum()), A=float(A), n=int(m.sum()), ncl=len(set(cid[m])))); cols.append(np.array(reps))
    if not info: return [], [], np.zeros((0, 0)), []
    Rr = np.array(cols); Rm = Rr.mean(1, keepdims=True); CA = 29 / 30 * (Rr - Rm) @ (Rr - Rm).T
    Av = np.array([i["A"] for i in info]); CEm = CA / np.outer(Av, Av)
    for j, i in enumerate(info): i["E"] = math.log(i["A"]); i["se"] = math.sqrt(CEm[j, j]); i["sA"] = math.sqrt(CA[j, j])
    return [i["lr"] for i in info], [i["E"] for i in info], CEm, info

def build(f, var, opt=None, shuffle_rng=None, boot_seed=914):
    """Return {sector: (lr list, E list, cov (no floor), info)} for footing f and ordering variable var ('law'|'bar'|'gbar'|'obs')."""
    opt = opt or {}; S = {}
    perm = (lambda x: x[shuffle_rng.permutation(len(x))]) if shuffle_rng is not None else (lambda x: x)
    d = DWR[f]; S["DW"] = bins_persystem(perm(d[var].copy()), d["E"], d["sE"], 8)
    for sec, msk in (("SS", SMALL), ("SL", LARGE)):
        lr = SPR[f][var][msk].copy(); S[sec] = bins_sparc(perm(lr), SPR[f]["E"][msk], SP["gal"][msk], np.random.default_rng(boot_seed))
    for sec, colour, sh in (("LR", "red", 0.0 if opt.get("red_noshift") else 0.123), ("LB", "blue", 0.0)):
        Lp = lens_points(colour, f, sh, opt.get("dlm", 0.0))
        S[sec] = bins_lens(Lp, var, lr_override=perm(Lp[var].copy()) if shuffle_rng is not None else None)
    jsel = [0, 1, 2, 3, 4, 5, 6, 7] if opt.get("inner") else [3, 4, 5, 6, 7]
    cv = "law" if var == "obs" else var
    LR2 = CLR[f][cv].copy()
    if shuffle_rng is not None:
        sub = LR2[:, jsel].ravel(); LR2[:, jsel] = perm(sub).reshape(NCL, len(jsel))
    lr, E, C, info = bins_clusters(LR2, CLP[f], jsel)
    if var == "obs":                                      # R2 for stacked clusters: relabel the bin by the observed amplitude
        lr = [l + e / LN10 for l, e in zip(lr, E)]
        for i, l in zip(info, lr): i["lr"] = l
    S["CL"] = (lr, E, C, info)
    gc = [r for r in GCR[f] if (not opt.get("gc_n50") or r["nstar"] >= 50)]
    Eg = np.array([r["E_efe" if opt.get("gc_efe") else "E"] for r in gc]); sEg = np.array([r["sE"] for r in gc])
    gv = "law_efe" if (opt.get("gc_efe") and var == "law") else var
    lg = np.array([r[gv] for r in gc]); S["GC"] = bins_persystem(perm(lg), Eg, sEg, min(5, max(1, len(gc) // 4)))
    return S

# =====================================================================================================================  FIT + TESTS
def pava(y, w):                                              # weighted isotonic (non-decreasing) regression
    blocks = []
    for yi, wi in zip(y, w):
        blocks.append([yi * wi, wi, 1])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            a = blocks.pop(); blocks[-1][0] += a[0]; blocks[-1][1] += a[1]; blocks[-1][2] += a[2]
    out = []
    for s_, w_, n_ in blocks: out += [s_ / w_] * n_
    return np.array(out)

def zsec(r, C):                                             # chi2 with n dof -> one-sided Gaussian equivalent (capped at 40)
    c2 = float(r @ np.linalg.solve(C, r)); n = len(r); lp = float(chi2.logsf(c2, n))
    z = float(norm.isf(math.exp(lp))) if lp > -700 else math.sqrt(2 * -lp)
    return c2, n, float(math.exp(lp)), min(z, 40.0)

def _gather(S, secs, invert):
    lr, E, se2, own = [], [], [], []
    for s in secs:
        l, e, C, _ = S[s]
        for j in range(len(l)): lr.append(-l[j] if invert else l[j]); E.append(e[j]); se2.append(C[j, j]); own.append((s, j))
    lr, E, se2 = np.array(lr), np.array(E), np.array(se2); o = np.argsort(lr, kind="stable")
    return lr[o], E[o], se2[o], [own[i] for i in o]

def fit(S, secs, floor, mode="mono", invert=False, a1=False):
    """FROZEN fit (a1=False): weights 1/(SE^2 + floor^2), no offsets.  A1 fit (a1=True, AMENDMENT_A1.md, post hoc): per-sector offsets
    delta_s ~ N(0, floor^2) fitted jointly with f (weights 1/SE^2); the sector test below is identical for both."""
    lr, E, se2, own = _gather(S, secs, invert); w = 1 / (se2 + floor ** 2); N = len(lr); best = None
    offs = np.zeros(N); dsec = {}
    if a1:
        ws = 1 / se2; sid = np.array([secs.index(s_) for s_, j in own])
        posm = {s_: [i for i in range(N) if own[i][0] == s_] for s_ in secs}
        Ci = {s_: np.linalg.inv(S[s_][2]) for s_ in secs}
    for k in range(N + 1):
        if 0 < k < N and lr[k - 1] == lr[k]: continue
        if not a1:
            fv = np.zeros(N)
            if k < N:
                if mode == "mono": fv[k:] = np.maximum(pava(E[k:], w[k:]), 0.0)
                else: fv[k:] = max(float(np.sum(w[k:] * E[k:]) / np.sum(w[k:])), 0.0)
            c = float(np.sum(w * (E - fv) ** 2)); d = None
        else:
            d = np.zeros(len(secs))
            for it in range(200):
                Ec = E - d[sid]; fv = np.zeros(N)
                if k < N:
                    if mode == "mono": fv[k:] = np.maximum(pava(Ec[k:], ws[k:]), 0.0)
                    else: fv[k:] = max(float(np.sum(ws[k:] * Ec[k:]) / np.sum(ws[k:])), 0.0)
                if floor <= 0: break
                dn = np.zeros(len(secs))
                for a, s_ in enumerate(secs):
                    rs = E[posm[s_]] - fv[posm[s_]]; one = np.ones(len(rs))
                    dn[a] = float(one @ Ci[s_] @ rs) / float(one @ Ci[s_] @ one + 1 / floor ** 2)
                conv = np.max(np.abs(dn - d)) < 1e-10; d = dn
                if conv: break
            Ec = E - d[sid]; c = float(np.sum(ws * (Ec - fv) ** 2) + (np.sum(d ** 2) / floor ** 2 if floor > 0 else 0.0))
        if best is None or c < best[0] - 1e-12: best = (c, k, fv, d)
    c, k, fv, d = best
    if a1: offs = d[sid]; dsec = {s_: float(d[a]) for a, s_ in enumerate(secs)}
    Esig = E - offs; m = int(np.sum(fv <= 0))
    valid = 0 < m < N
    tr = 0.5 * (lr[m - 1] + lr[m]) if valid else (lr[0] - 1 if m == 0 else lr[-1] + 1)
    ab = slice(m, N); Ebar = float(np.sum(w[ab] * Esig[ab]) / np.sum(w[ab])) if m < N else float("nan"); se = float(1 / math.sqrt(np.sum(w[ab]))) if m < N else float("nan")
    sig = Ebar / se if m < N else float("nan")
    half = float(lr[int(np.argmax(fv >= 0.5 * fv.max()))]) if (N and fv.max() > 0) else float("nan")
    def feval(x):                                            # step function of the fit (in the fit's own sign convention)
        x = -x if invert else x
        if x < tr: return 0.0
        i = np.searchsorted(lr, x, side="right") - 1
        return float(fv[max(i, m)]) if m < N else 0.0
    fitted = {s_: np.zeros(len(S[s_][0])) for s_ in secs}
    for (s_, j), v in zip(own, fv): fitted[s_][j] = v
    per = {}
    for s_ in S:
        l, e, C, _ = S[s_]
        if not len(l): continue
        fvs = fitted[s_] if s_ in secs else np.array([feval(x) for x in l])
        r = np.array(e) - fvs; Cf = C + floor ** 2 * np.ones_like(C)
        c2, n, p, z = zsec(r, Cf); per[s_] = dict(chi2=c2, n=n, p=p, z=z, f=fvs.tolist(), resid_z=(r / np.sqrt(np.diag(Cf))).tolist(), in_fit=s_ in secs)
    rho_eff = (-tr if invert else tr)
    return dict(chi2=c, valid=bool(valid), rho_star=float(rho_eff), rho_half=(-half if invert else half), n_below=int(m), n_above=int(N - m),
                E_above=Ebar, se_above=se, sig_above=sig, ok_thr=bool(valid and sig >= 3), per=per, secs=list(secs),
                E_hi=float(fv[-1]) if N else 0.0, offsets=dsec, a1=bool(a1))

def greedy(S, floor, mode="mono", invert=False, a1=False):
    secs = [s for s in SECTORS if len(S[s][0])]; dropped = []; first = fit(S, secs, floor, mode, invert, a1)
    cur = first
    while True:
        viol = [(cur["per"][s]["z"], s) for s in secs if cur["per"][s]["z"] > 2]
        if not viol or len(secs) <= 2: break
        z, s = max(viol); dropped.append((s, z)); secs = [x for x in secs if x != s]; cur = fit(S, secs, floor, mode, invert, a1)
    return first, cur, dropped

def classify(S, floor=FLOOR0, a1=False):
    first, surv, dropped = greedy(S, floor, a1=a1)
    allsec = [s for s in SECTORS if len(S[s][0])]
    if len(allsec) == 7 and first["ok_thr"] and all(first["per"][s]["z"] <= 2 for s in allsec): cls = "COMMON THRESHOLD"
    else:
        ss = surv["secs"]
        if sum(s in ss for s in FAILING) >= 2 and sum(s in ss for s in DIFFUSE) >= 1 and surv["ok_thr"]: cls = "PARTIAL"
        else: cls = "NO COMMON ORDERING"
    return dict(cls=cls, first=first, surv=surv, dropped=dropped)

def slope_z(S, s, floor):
    l, e, C, _ = S[s]
    if len(l) < 3: return None
    X = np.c_[np.ones(len(l)), l]; Cf = C + floor ** 2 * np.ones_like(C); Ci = np.linalg.inv(Cf)
    cov = np.linalg.inv(X.T @ Ci @ X); b = cov @ X.T @ Ci @ np.array(e)
    return dict(slope=float(b[1]), se=float(math.sqrt(cov[1, 1])), z=float(b[1] / math.sqrt(cov[1, 1])))

def pooled_spearman(S, nperm=10000, seed=914):
    l = np.concatenate([S[s][0] for s in SECTORS if len(S[s][0])]); e = np.concatenate([S[s][1] for s in SECTORS if len(S[s][0])])
    rs = float(spearmanr(l, e)[0]); rng = np.random.default_rng(seed)
    pr = np.array([spearmanr(l, rng.permutation(e))[0] for _ in range(nperm)])
    return dict(rho=rs, p=float(np.mean(np.abs(pr) >= abs(rs))), n=len(l))

def fmt_cls(C):
    d = ", ".join(f"{s} (z {z:.1f})" for s, z in C["dropped"]) or "none"
    sv = C["surv"]
    return (f"{C['cls']}; all-sector fit rho*_eff {C['first']['rho_star']:+.2f} (valid {C['first']['valid']}, above {C['first']['E_above']:+.2f} at "
            f"{C['first']['sig_above']:.1f} sigma); violators dropped in order: {d}; survivors {sv['secs']} (rho*_eff {sv['rho_star']:+.2f}, "
            f"threshold ok {sv['ok_thr']})")

UNIT = {"law": "log rho_law [Msun/pc^3]", "bar": "log rho_b [Msun/pc^3]", "gbar": "log g_bar [m/s^2]", "obs": "log rho_obs [Msun/pc^3] (CIRCULAR)"}
def table(S, Cf, var):
    P(f"     {'sector':26s} {UNIT[var].split(' [')[0]:>8s}  E (+-se)        n    f_fit  resid_z")
    for s in SECTORS:
        l, e, C, info = S[s]
        if not len(l): P(f"     {SNAME[s]:26s} (no usable bins)"); continue
        pr = Cf["per"].get(s, {})
        for j in range(len(l)):
            nn = info[j].get("n", ""); fval = pr["f"][j] if pr else float("nan"); rz = pr["resid_z"][j] if pr else float("nan")
            P(f"     {SNAME[s] if j == 0 else '':26s} {l[j]:+8.2f}  {e[j]:+6.3f} +- {math.sqrt(C[j, j]):.3f}  {nn!s:>5s}  {fval:+6.3f}  {rz:+6.2f}")
        if pr: P(f"     {'':26s} sector chi2 {pr['chi2']:.1f} / {pr['n']}  p {pr['p']:.2g}  z {pr['z']:.2f}  {'VIOLATES' if pr['z'] > 2 else 'ok'}"
                 + ("" if pr["in_fit"] else "  (not in this fit)"))

def scales(f):
    a0 = A0[f]; H0 = 70e3 / 3.0857e22
    return {"rho_crit(h0.70)": math.log10(3 * H0 ** 2 / (8 * math.pi * G) / RHO_UNIT), "rho_DE=4a0^2/(Gc^2)": math.log10(4 * a0 ** 2 / (G * CLIGHT ** 2) / RHO_UNIT),
            "3a0/(4piG*104pc)": math.log10(3 * a0 / (4 * math.pi * G * 104 * PCM) / RHO_UNIT), "3a0/(4piG*1kpc)": math.log10(3 * a0 / (4 * math.pi * G * KPCM) / RHO_UNIT),
            "3a0/(4piG*100kpc)": math.log10(3 * a0 / (4 * math.pi * G * 100 * KPCM) / RHO_UNIT), "CFG870 clump centre 0.6": math.log10(0.6)}

def sjson(S):
    return {s: dict(lr=list(map(float, S[s][0])), E=list(map(float, S[s][1])), cov=np.asarray(S[s][2]).tolist(), info=S[s][3]) for s in SECTORS}

# =====================================================================================================================  RUN
if MUT == "shuffle":
    P("\n=== MUTATE-SHUFFLE: densities permuted within each sector (200 realisations per footing x variable)")
    RES["shuffle"] = {}
    for f in FOOTS:
        for var in ("law", "bar"):
            real = build(f, var); zr = {s: (slope_z(real, s, FLOOR0) or {}).get("z") for s in SECTORS}
            rng = np.random.default_rng(914 + (0 if f == "canonical" else 1) + (0 if var == "law" else 10)); Z = {s: [] for s in SECTORS}; SPm = []
            cls0 = None
            for t in range(200):
                S = build(f, var, shuffle_rng=rng)
                for s in SECTORS:
                    q = slope_z(S, s, FLOOR0)
                    if q: Z[s].append(q["z"])
                l = np.concatenate([S[s][0] for s in SECTORS if len(S[s][0])]); e = np.concatenate([S[s][1] for s in SECTORS if len(S[s][0])])
                SPm.append(float(spearmanr(l, e)[0]))
                if t == 0: cls0 = classify(S)
            fr = {s: (float(np.mean(np.abs(Z[s]) >= 2)) if Z[s] else None) for s in SECTORS}
            pperm = {s: (float(np.mean(np.abs(Z[s]) >= abs(zr[s]))) if (Z[s] and zr[s] is not None) else None) for s in SECTORS}   # POST HOC (reported)
            ok = all(v is None or v <= 0.15 for v in fr.values())
            sp_real = float(spearmanr(np.concatenate([real[s][0] for s in SECTORS]), np.concatenate([real[s][1] for s in SECTORS]))[0])
            RES["shuffle"][f"{f}|{var}"] = dict(real_slope_z=zr, frac_absz_ge2=fr, median_absz={s: (float(np.median(np.abs(Z[s]))) if Z[s] else None) for s in SECTORS},
                                                pass_=ok, pooled_spearman_real=sp_real, pooled_spearman_shuffled_median=float(np.median(SPm)),
                                                pooled_spearman_shuffled_16_84=[float(np.percentile(SPm, 16)), float(np.percentile(SPm, 84))],
                                                class_realisation0=cls0["cls"], dropped0=cls0["dropped"], perm_p_posthoc=pperm)
            P(f"\n  [{f} | {UNIT[var]}]")
            for s in SECTORS:
                if fr[s] is None: P(f"    {SNAME[s]:26s} < 3 bins (no slope)"); continue
                P(f"    {SNAME[s]:26s} real slope z {zr[s]:+6.2f}   shuffled: median |z| {np.median(np.abs(Z[s])):.2f}, frac |z|>=2 {fr[s]:.3f}"
                  f"   [POST HOC: permutation p of the real slope {pperm[s]:.3f}]")
            P(f"    pooled Spearman: real {sp_real:+.3f}; shuffled median {np.median(SPm):+.3f} (16-84% {np.percentile(SPm, 16):+.3f}..{np.percentile(SPm, 84):+.3f})"
              " -- cross-sector ranges are preserved by a within-sector shuffle")
            P(f"    realisation 0 class: {fmt_cls(cls0)}")
            P(f"    -> within-sector ordering disappears (all frac <= 0.15): {'PASS' if ok else 'FAIL'}")
    RES["shuffle_pass"] = all(v["pass_"] for v in RES["shuffle"].values())
    P(f"\n  MUTATE-SHUFFLE overall: {'PASS' if RES['shuffle_pass'] else 'FAIL'}")
elif MUT == "inject":
    P("\n=== MUTATE-INJECT: bin values replaced by 0.7 H(log rho - log rho*_inj) + draws from each sector's covariance (incl. floor)")
    RES["inject"] = {}; rng = np.random.default_rng(914); allok = True; KEEP = {}
    for f in FOOTS:
        for var in ("law", "bar"):
            S = build(f, var); lall = np.concatenate([S[s][0] for s in SECTORS if len(S[s][0])]); lst = float(np.median(lall))
            S2 = {}
            for s in SECTORS:
                l, e, C, info = S[s]
                if not len(l): S2[s] = S[s]; continue
                Cf = C + FLOOR0 ** 2 * np.ones_like(C); truth = 0.7 * (np.array(l) >= lst)
                S2[s] = (l, list(truth + rng.multivariate_normal(np.zeros(len(l)), Cf)), C, info)
            KEEP[f"{f}|{var}"] = (S, S2, lst)
            Cl = classify(S2); rec = Cl["first"]["rho_star"]; ok = Cl["cls"] == "COMMON THRESHOLD" and abs(rec - lst) <= 0.5; allok &= ok
            RES["inject"][f"{f}|{var}"] = dict(rho_inj=lst, rho_rec=rec, cls=Cl["cls"], dropped=Cl["dropped"],
                                               z={s: Cl["first"]["per"][s]["z"] for s in Cl["first"]["per"]}, ok=ok)
            P(f"  [{f} | {UNIT[var]}] injected {lst:+.2f}, recovered {rec:+.2f}; {fmt_cls(Cl)}  -> {'PASS' if ok else 'FAIL'}")
            P("     per-sector z: " + ", ".join(f"{s} {Cl['first']['per'][s]['z']:.2f}" for s in Cl["first"]["per"]))
    RES["inject_pass"] = bool(allok); P(f"\n  MUTATE-INJECT (frozen) overall: {'PASS' if allok else 'FAIL'}")
    # ---------------- AMENDMENT A1 (post hoc): same single draws re-scored; power over 100 injections; false-positive check
    P("\n=== AMENDMENT A1 (POST HOC): fit with per-sector offsets (prior N(0, floor^2)); sector test unchanged")
    RES["A1"] = {}
    for key, (S, S2, lst) in KEEP.items():
        Cl = classify(S2, a1=True)
        RES["A1"][f"single|{key}"] = dict(cls=Cl["cls"], rho_rec=Cl["first"]["rho_star"], rho_half=Cl["first"]["rho_half"], dropped=Cl["dropped"],
                                          z={x: Cl["first"]["per"][x]["z"] for x in Cl["first"]["per"]}, offsets=Cl["first"]["offsets"])
        P(f"  single seed-914 draw [{key}] injected {lst:+.2f}: A1 {fmt_cls(Cl)}; rho*_half {Cl['first']['rho_half']:+.2f}")
    for key, (S, S2, lst) in KEEP.items():
        rp = np.random.default_rng(914); cF, cA, dA, dH = {}, {}, [], []
        rq = np.random.default_rng(9141); qF, qA = {}, {}
        for t in range(100):
            S3 = {}
            for x in SECTORS:
                l, e, C, info = S[x]; Cf = C + FLOOR0 ** 2 * np.ones_like(C); truth = 0.7 * (np.array(l) >= lst)
                S3[x] = (l, list(truth + rp.multivariate_normal(np.zeros(len(l)), Cf)), C, info)
            a = classify(S3)["cls"]; cF[a] = cF.get(a, 0) + 1
            Cl = classify(S3, a1=True); cA[Cl["cls"]] = cA.get(Cl["cls"], 0) + 1; dA.append(Cl["first"]["rho_star"] - lst); dH.append(Cl["first"]["rho_half"] - lst)
            S4 = {}
            for x in SECTORS:
                l, e, C, info = S[x]; Cf = C + FLOOR0 ** 2 * np.ones_like(C); lsx = lst + rq.uniform(-1.5, 1.5); truth = 0.7 * (np.array(l) >= lsx)
                S4[x] = (l, list(truth + rq.multivariate_normal(np.zeros(len(l)), Cf)), C, info)
            a = classify(S4)["cls"]; qF[a] = qF.get(a, 0) + 1
            a = classify(S4, a1=True)["cls"]; qA[a] = qA.get(a, 0) + 1
        dA, dH = np.abs(np.array(dA)), np.abs(np.array(dH))
        RES["A1"][f"power|{key}"] = dict(frozen=cF, A1=cA, frac_rec_within_0p5=float(np.mean(dA <= 0.5)), frac_half_within_0p5=float(np.nanmean(dH <= 0.5)),
                                         median_abs_drho=float(np.median(dA)), falsepos_frozen=qF, falsepos_A1=qA)
        P(f"  power [{key}] 100 injected common thresholds: frozen {cF};  A1 {cA};  A1 rho*_eff within 0.5 dex {np.mean(dA <= 0.5):.2f}, rho*_half {np.nanmean(dH <= 0.5):.2f}")
        P(f"     false-positive check (per-sector thresholds, median +- U(1.5) dex): frozen {qF};  A1 {qA}")
    RES["A1_power_min"] = min(v["A1"].get("COMMON THRESHOLD", 0) for k, v in RES["A1"].items() if k.startswith("power")) / 100
    P(f"\n  A1 power (min over footing x variable): {RES['A1_power_min']:.2f} COMMON THRESHOLD (stated expectation >= 0.70; seen in scratch before A1 was written)")
else:
    RES["classes"] = {}; RES["bins"] = {}
    for var in ("law", "bar"):
        for f in FOOTS:
            S = build(f, var); Cl = classify(S); RES["bins"][f"{f}|{var}"] = sjson(S)
            st = greedy(S, FLOOR0, mode="step"); inv = greedy(S, FLOOR0, mode="mono", invert=True)
            sz = {s: slope_z(S, s, FLOOR0) for s in SECTORS}; sp = pooled_spearman(S)
            P(f"\n=== {'PRIMARY' if var == 'law' else 'GRADED VARIANT V1'}  [{f}]  ordering variable: {UNIT[var]}")
            P("  -- all-sector monotone-threshold fit (generous form) --"); table(S, Cl["first"], var)
            P(f"  CLASS: {fmt_cls(Cl)}")
            if Cl["dropped"]:
                P("  -- survivors' fit --"); table(S, Cl["surv"], var)
            P(f"  strict step (one common level): rho* {st[0]['rho_star']:+.2f}, E_hi {st[0]['E_hi']:+.3f}; violators "
              + (", ".join(f"{s} (z {z:.1f})" for s, z in st[2]) or "none") + "; z: " + ", ".join(f"{s} {st[0]['per'][s]['z']:.1f}" for s in st[0]["per"]))
            P(f"  inverted (excess only BELOW a threshold): rho* {inv[0]['rho_star']:+.2f}, valid {inv[0]['valid']}, sig {inv[0]['sig_above']:.1f}; violators "
              + (", ".join(f"{s} (z {z:.1f})" for s, z in inv[2]) or "none") + f"; survivors {inv[1]['secs']}")
            P("  within-sector GLS slope dE/dlog: " + "; ".join(f"{s} {q['slope']:+.3f}+-{q['se']:.3f} (z {q['z']:+.1f})" for s, q in sz.items() if q))
            P(f"  pooled Spearman over {sp['n']} bins: {sp['rho']:+.3f} (permutation p {sp['p']:.3g})")
            sc = scales(f)
            if var != "gbar":
                P("  framework scales (POST HOC; any match is not a result): " + ", ".join(f"{k} {v:+.2f}" for k, v in sc.items())
                  + f"  | rho*_eff all-sector {Cl['first']['rho_star']:+.2f}, survivors {Cl['surv']['rho_star']:+.2f}")
            Cl1 = classify(S, a1=True); inv1 = greedy(S, FLOOR0, invert=True, a1=True)
            P("  -- AMENDMENT A1 (post hoc): all-sector fit with per-sector offsets --"); table(S, Cl1["first"], var)
            P("  A1 offsets: " + ", ".join(f"{k} {v:+.3f}" for k, v in Cl1["first"]["offsets"].items()) + f"; rho*_half {Cl1['first']['rho_half']:+.2f}")
            P(f"  A1 CLASS: {fmt_cls(Cl1)}")
            if Cl1["dropped"]:
                P("  -- A1 survivors' fit --"); table(S, Cl1["surv"], var)
            P(f"  A1 inverted: rho* {inv1[0]['rho_star']:+.2f}, valid {inv1[0]['valid']}, sig {inv1[0]['sig_above']:.1f}; violators "
              + (", ".join(f"{s} (z {z:.1f})" for s, z in inv1[2]) or "none") + f"; survivors {inv1[1]['secs']}")
            if var != "gbar": P(f"  A1 rho*_eff all-sector {Cl1['first']['rho_star']:+.2f}, survivors {Cl1['surv']['rho_star']:+.2f} (framework scales as above; POST HOC)")
            RES.setdefault("classes_A1", {})[f"{f}|{var}"] = dict(cls=Cl1["cls"], first=Cl1["first"], surv=Cl1["surv"], dropped=Cl1["dropped"],
                                                                  inverted=dict(first=inv1[0], dropped=inv1[2], surv=inv1[1]["secs"]))
            RES["classes"][f"{f}|{var}"] = dict(cls=Cl["cls"], first={k: v for k, v in Cl["first"].items()}, surv={k: v for k, v in Cl["surv"].items()},
                                               dropped=Cl["dropped"], step=dict(first=st[0], dropped=st[2]), inverted=dict(first=inv[0], dropped=inv[2], surv=inv[1]["secs"]),
                                               slopes=sz, spearman=sp, scales=sc)
    # ---- headline
    h = RES["classes"]["canonical|law"]["cls"]; flags = []
    if RES["classes"]["alt|law"]["cls"] != h: flags.append("footing-dependent")
    if RES["classes"]["canonical|bar"]["cls"] != h: flags.append("density-variable dependent")
    RES["headline"] = h + (f" ({', '.join(flags)})" if flags else "")
    h1 = RES["classes_A1"]["canonical|law"]["cls"]; fl1 = []
    if RES["classes_A1"]["alt|law"]["cls"] != h1: fl1.append("footing-dependent")
    if RES["classes_A1"]["canonical|bar"]["cls"] != h1: fl1.append("density-variable dependent")
    RES["headline_A1"] = h1 + (f" ({', '.join(fl1)})" if fl1 else "")
    # ---- reported variants
    P("\n=== REPORTED VARIANTS (not graded; primary density unless stated)")
    RES["variants"] = {}
    VAR = [("R1 g_bar as ordering variable", "gbar", {}, FLOOR0), ("R2 rho_obs (CIRCULAR)", "obs", {}, FLOOR0),
           ("R3a floor 0", "law", {}, 0.0), ("R3b floor 0.1 dex", "law", {}, 0.1 * LN10),
           ("R4a lens masses -0.3 dex", "law", {"dlm": -0.3}, FLOOR0), ("R4b lens masses +0.3 dex", "law", {"dlm": 0.3}, FLOOR0),
           ("R5 red lenses without M* shift", "law", {"red_noshift": True}, FLOOR0), ("R6 globulars >= 50 RV stars", "law", {"gc_n50": True}, FLOOR0),
           ("R7 globulars vs law+EFE baseline", "law", {"gc_efe": True}, FLOOR0), ("R8 cluster INNER band included", "law", {"inner": True}, FLOOR0)]
    for lab, var, opt, fl in VAR:
        for f in FOOTS:
            S = build(f, var, opt); Cl = classify(S, fl); Cl1 = classify(S, fl, a1=True)
            RES["variants"][f"{lab}|{f}"] = dict(cls=Cl["cls"], dropped=Cl["dropped"], rho_first=Cl["first"]["rho_star"], surv=Cl["surv"]["secs"],
                                                  z={s: Cl["first"]["per"][s]["z"] for s in Cl["first"]["per"]},
                                                  A1=dict(cls=Cl1["cls"], dropped=Cl1["dropped"], rho_first=Cl1["first"]["rho_star"], surv=Cl1["surv"]["secs"],
                                                          z={s: Cl1["first"]["per"][s]["z"] for s in Cl1["first"]["per"]}))
            P(f"  {lab:36s} [{f:9s}] frozen: {fmt_cls(Cl)}")
            P(f"  {'':36s} [{f:9s}] A1:     {fmt_cls(Cl1)}")
            if lab.startswith("R1") and f == "canonical":
                P("     R1 bins (canonical):"); table(S, Cl["first"], "gbar")
    # ---- per-system rows (plots as tables)
    P("\n=== per-system rows (canonical; alt in the JSON)")
    d = DWR["canonical"]; o = np.argsort(d["law"])
    P("  dwarfs: name  log rho_law  log rho_b  log g_bar  E = 2 ln(s_obs/s_law)  +- ")
    for i in o: P(f"    {d['names'][i]:22s} {d['law'][i]:+6.2f} {d['bar'][i]:+6.2f} {d['gbar'][i]:+7.2f}  {d['E'][i]:+6.2f} +- {d['sE'][i]:.2f}")
    P("  globulars (tidally safe): name  R_out(pc)  N*  log rho  E = 2 ln(s_obs/s_N,Ups1.6)  +-  [E vs law+EFE]")
    for r in sorted(GCR["canonical"], key=lambda q: q["law"]):
        P(f"    {r['name']:12s} {r['R_out']:6.1f} {r['nstar']:5d} {r['law']:+6.2f}  {r['E']:+6.2f} +- {r['sE']:.2f}  [{r['E_efe']:+6.2f}]")
    RES["rows"] = {f: dict(dwarfs=[dict(name=DWR[f]["names"][i], log_rho_law=float(DWR[f]["law"][i]), log_rho_b=float(DWR[f]["bar"][i]),
                                         log_gbar=float(DWR[f]["gbar"][i]), E=float(DWR[f]["E"][i]), sE=float(DWR[f]["sE"][i])) for i in range(83)],
                            globulars=GCR[f]) for f in FOOTS}
    P("\n=== CLASSES")
    for k, v in RES["classes"].items(): P(f"  {k:16s} {v['cls']}   violators: " + (", ".join(f"{s} (z {z:.1f})" for s, z in v["dropped"]) or "none") + f"   survivors {v['surv']['secs']}")
    for k, v in RES["classes_A1"].items(): P(f"  A1 {k:13s} {v['cls']}   violators: " + (", ".join(f"{s} (z {z:.1f})" for s, z in v["dropped"]) or "none") + f"   survivors {v['surv']['secs']}")
    P(f"\n  HEADLINE CLASS (primary rho_law, canonical): frozen {RES['headline']};  A1 (post hoc) {RES['headline_A1']}")
    ok_all = all(v["ok"] for v in RES["checks"].values())
    P(f"  K-tests: {sum(v['ok'] for v in RES['checks'].values())}/{len(RES['checks'])} PASS" + ("" if ok_all else "  (FAILURES PRESENT)"))

RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_MB"] = round(rss_mb(), 1)
P(f"\n  [{RES['runtime_s']} s, peak RSS {RES['peak_rss_MB']} MB]  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
def _j(o):
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, np.bool_): return bool(o)
    return str(o)
json.dump(RES, open(os.path.join(HERE, f"cfg914_results{SUF}.json"), "w"), indent=1, default=_j)
open(os.path.join(HERE, f"cfg914{SUF}.out"), "w").write("\n".join(OUT) + "\n")
