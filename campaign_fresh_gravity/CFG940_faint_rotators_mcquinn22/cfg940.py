"""CFG940 -- faint gas-rich rotators (McQuinn+2022, 25 dwarfs): ABOVE, ON or BELOW the law at g_bar < 1e-12, vs dSphs at matched g_bar.
Criteria: FROZEN_CRITERIA.md (798e98d78, committed alone before this script); AMENDMENT_A1.md (bda93d8db, post hoc after the
frozen K3 failed, before any residual): K3 R_max tolerance + 0.5 arcsec x Dist.
Run (one core, seconds; the two data tables are passed as arguments, untrusted, parsed by MRT byte positions, never executed):
  OMP_NUM_THREADS=1 nice -n 10 python3 -I cfg940.py --t1 <apjac9285t1_mrt.txt> --t2 <apjac9285t2_mrt.txt> --mode K|plant|shuffle|main
Outputs named by mode: cfg940_K.out / cfg940_results_K.json; cfg940_MUTATE_plant.*; cfg940_MUTATE_shuffle.*; cfg940.out / cfg940_results.json.
Exit 0 = K passed and every required control in the mode met; 1 = a required MUTATE control failed; 2 = a K-test failed (no class).
Record inputs read only: SPARC (Lelli+16); CFG827/CFG824 rows + LVD csvs (CFG828's 29 dwarfs, via CFG931's K1 code path, copied);
CFG880's input slice exec'd read-only with writes refused (variant V10 only, as CFG931 did); K targets cfg828/cfg919 results.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; raw data, framework-native only; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import argparse, io, csv, json, math, glob, time, resource, warnings, contextlib, builtins, hashlib
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e

T0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--t1", required=True); ap.add_argument("--t2", required=True)
ap.add_argument("--mode", choices=("K", "plant", "shuffle", "main"), required=True)
ARGS = ap.parse_args(); MODE = ARGS.mode
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
SUF = {"K": "_K", "plant": "_MUTATE_plant", "shuffle": "_MUTATE_shuffle", "main": ""}[MODE]
for _e in ("CFG880_MUTATE", "CFG828_MUTATE", "CFG919_MUTATE", "CFG914_MUTATE", "CFG931_MUTATE", "MUTATE"):
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
    if isinstance(o, (set, frozenset)): return sorted(o)
    return str(o)
RES = dict(lane="CFG940", criteria="798e98d78", amendment_A1="bda93d8db", mode=MODE, checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def finish(code):
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_mb"] = round(rss_mb(), 1); RES["exit"] = code
    P(f"\n  done [{time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB], exit {code}.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    json.dump(RES, builtins.open(os.path.join(HERE, f"cfg940_results{SUF}.json"), "w"), indent=1, default=jdef)
    builtins.open(os.path.join(HERE, f"cfg940{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
LN10 = math.log(10.0)
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
G_KPC = 4.30091e-6                                            # kpc (km/s)^2 / Msun (K1 only)
ARCSEC = math.pi / 648000.0
GRID = np.arange(-20.0, 10.0001, 0.5)                         # CFG914/919/931 fixed 0.5-dex edges
FLOOR = 0.05; LGW1 = -12.0; NMIN = 5; THR_ABOVE = 0.20; PL = 0.37
nu_e12 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
nu_e15 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_s12 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-12)))
nu_s15 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-15)))
KERN = {"e": nu_e15, "s": nu_s15}
FLOOR0_919 = 0.05 * LN10
def cell(lg): return int(np.digitize([lg], GRID)[0] - 1)
def cname(c): return f"[{GRID[c]:.1f},{GRID[c] + 0.5:.1f})"

P(f"CFG940  faint gas-rich rotators (McQuinn+2022): ABOVE / ON / BELOW the law at g_bar < 1e-12   [mode {MODE}]")
P("  estimator A = total M_bary at R_max (primary, upper bound on spherical g_bar); B = exponential-disc enclosed fractions (bracket); kappa = 1/2 FITTED")

# =====================================================================================================================  parse (untrusted data)
SHA = {"apjac9285t1_mrt.txt": "476bc7c70f87d685530e49a3301975ba131e2b3bee96d74e4f8e189bcdf54914",
       "apjac9285t2_mrt.txt": "46dc6a2df7b4689a67b791c6de3fb17d3201709fb055fa137df4df4b5b265e2d"}
def sha256(p): return hashlib.sha256(builtins.open(p, "rb").read()).hexdigest()
def data_lines(p):
    L = builtins.open(p, encoding="latin-1").read().split("\n")
    last = max(i for i, l in enumerate(L) if l.startswith("-----"))
    return [l for l in L[last + 1:] if l.strip()]
def fx(s):
    s = s.strip(); return float(s) if s else None
T1 = {}
for l in data_lines(ARGS.t1):
    l = l.ljust(92)
    T1[l[0:9].strip()] = dict(D=fx(l[10:15]), eD=fx(l[16:20]), lMs=fx(l[46:50]), elMs=fx(l[51:55]), lHI=fx(l[73:77]),
                             elHI=fx(l[78:82]), lMb=fx(l[83:87]), elMb=fx(l[88:92]))
ORDER = []
T2 = {}
for l in data_lines(ARGS.t2):
    l = l.ljust(65); nm = l[0:9].strip(); ORDER.append(nm)
    T2[nm] = dict(RP=l[10:11], i=fx(l[20:22]), ei=fx(l[23:24]), DPV=fx(l[25:29]), eDPV=fx(l[30:32]), Rtab=fx(l[33:36]), eR=fx(l[37:40]),
                  VPV=fx(l[41:44]), eVPV=fx(l[45:46]), Vrot=fx(l[47:49]), eVrot=fx(l[50:51]), Vcor=fx(l[52:54]), eVcor=fx(l[55:56]),
                  lMdyn=fx(l[57:60]), elMdyn=fx(l[61:65]))
ORDER1 = list(T1.keys())
SURVEY = {nm: ("SHIELD" if j < 7 else ("VLA-ANGST" if j < 19 else "LITTLE THINGS")) for j, nm in enumerate(ORDER1)}

P("\n=== K-stage")
KOK = []
# K0 integrity
h1, h2 = sha256(ARGS.t1), sha256(ARGS.t2)
prov = builtins.open(os.path.join(os.path.dirname(os.path.abspath(ARGS.t1)), "PROVENANCE.md")).read()
k0 = (h1 == SHA["apjac9285t1_mrt.txt"] and h2 == SHA["apjac9285t2_mrt.txt"] and SHA["apjac9285t1_mrt.txt"] in prov and SHA["apjac9285t2_mrt.txt"] in prov
      and len(T1) == 25 and len(T2) == 25 and ORDER1 == ORDER and sum(nm.startswith("AGC") for nm in ORDER1[:7]) == 7
      and all(v is not None for g in T1.values() for k, v in g.items() if k != "eD") and all(v is not None for g in T2.values() for v in g.values()))
KOK.append(check("K0 sha256 = PROVENANCE; 25 rows each, same names/order; 7 AGC (SHIELD) rows first; all needed fields parse", k0,
                 f"t1 {h1[:12]}.. t2 {h2[:12]}..; rows {len(T1)}/{len(T2)}; order match {ORDER1 == ORDER}"))
GALS = []
for nm in ORDER1:
    g = dict(name=nm, survey=SURVEY[nm]); g.update(T1[nm]); g.update(T2[nm]); GALS.append(g)
for g in GALS:
    g["R"] = 0.5 * g["DPV"] * ARCSEC * g["D"] * 1e3       # kpc, unrounded

# K1 log Mdyn
k1 = []; k1r = []
for g in GALS:
    tol = 0.05 + 2 * 0.5 / (g["Vcor"] * LN10) + 0.05 / (g["Rtab"] * LN10)
    lm = math.log10(g["Vcor"] ** 2 * g["Rtab"] / G_KPC); lmr = math.log10(g["Vrot"] ** 2 * g["Rtab"] / G_KPC)
    k1.append((g["name"], lm, g["lMdyn"], abs(lm - g["lMdyn"]) <= tol, tol)); k1r.append(abs(lmr - g["lMdyn"]) <= 0.05 + 2 * 0.5 / (g["Vrot"] * LN10) + 0.05 / (g["Rtab"] * LN10))
KOK.append(check("K1 log M_dyn = log10(V_cor^2 R_max / G) reproduces Table 2 to rounding (all 25)", all(x[3] for x in k1),
                 f"V_cor: {sum(x[3] for x in k1)}/25 within tol (max |diff| {max(abs(x[1] - x[2]) for x in k1):.3f}); V_rot instead: {sum(k1r)}/25"))
RES["K1_rows"] = [dict(name=x[0], calc=x[1], table=x[2], ok=x[3], tol=x[4]) for x in k1]
# K2 helium
fits = {}
for fhe in (1.00, 1.33, 1.36, 1.40):
    d = [math.log10(10 ** g["lMs"] + fhe * 10 ** g["lHI"]) - g["lMb"] for g in GALS]
    fits[fhe] = dict(maxabs=max(abs(x) for x in d), rms=float(np.sqrt(np.mean(np.square(d)))), ok=max(abs(x) for x in d) <= 0.015)
okf = [f for f in fits if fits[f]["ok"]]; FHE = min(okf, key=lambda f: fits[f]["rms"]) if okf else None
KOK.append(check("K2 helium: some f_He in {1.00,1.33,1.36,1.40} reproduces logMbary for all 25 to <= 0.015 dex", bool(okf),
                 "; ".join(f"f {f:.2f}: max {fits[f]['maxabs']:.3f} rms {fits[f]['rms']:.4f}" for f in fits) + f"  -> best passing f_He = {FHE}"))
HE_INCLUDED = FHE is not None and FHE >= 1.33
RES["K2"] = dict(fits=fits, f_he=FHE, helium_included=HE_INCLUDED)
for g in GALS:
    g["lMbA"] = g["lMb"] if HE_INCLUDED else math.log10(10 ** g["lMs"] + 1.33 * 10 ** g["lHI"])
# K3 V_rot and R_max
dv = [abs(g["VPV"] / (2 * math.sin(math.radians(g["i"]))) - g["Vrot"]) for g in GALS]; dr = [abs(g["R"] - g["Rtab"]) for g in GALS]
tolR = [0.051 + 0.5 * ARCSEC * g["D"] * 1e3 for g in GALS]          # AMENDMENT A1-1: + integer-arcsec rounding of D_PV
KOK.append(check("K3 V_rot = V_PV/(2 sin i) to <= 1.0 km/s and recomputed R_max = (D_PV/2) x Dist to <= 0.051 kpc + 0.5 arcsec x Dist (A1) (all 25)",
                 max(dv) <= 1.0 and all(x <= t for x, t in zip(dr, tolR)),
                 f"max |dV| {max(dv):.2f} km/s; max |dR| {max(dr):.3f} kpc; max |dR|/tol_R {max(x / t for x, t in zip(dr, tolR)):.2f}"))
# K4 inclination-error decision
pw = []; po = []
for g in GALS:
    ir = math.radians(g["i"]); a = g["eVPV"] / (2 * math.sin(ir)); b = g["Vrot"] * (math.cos(ir) / math.sin(ir)) * math.radians(g["ei"])
    pw.append(g["eVrot"] - math.hypot(a, b)); po.append(g["eVrot"] - a)
rw, ro = float(np.sqrt(np.mean(np.square(pw)))), float(np.sqrt(np.mean(np.square(po))))
INC_INCLUDED = rw < ro
P(f"  [DECISION] K4 inclination error inside e_Vrot/e_Vcor: rms residual with i-term {rw:.2f} km/s vs without {ro:.2f} -> "
  f"{'INCLUDED (not added again)' if INC_INCLUDED else 'NOT included (added in quadrature)'}")
RES["K4"] = dict(rms_with=rw, rms_without=ro, included=INC_INCLUDED)
for g in GALS:
    ir = math.radians(g["i"]); ti = g["Vrot"] * (math.cos(ir) / math.sin(ir)) * math.radians(g["ei"])
    g["eV"] = g["eVcor"] if INC_INCLUDED else math.hypot(g["eVcor"], ti * g["Vrot"] / g["Vcor"])
    g["eVr"] = g["eVrot"] if INC_INCLUDED else math.hypot(g["eVrot"], ti)

# ---------------------------------------------------------------------------------------------------------------- SPARC (CFG931 loader)
QG = {}; QG2 = {}
for l in builtins.open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try:
            QG[v[0]] = dict(inc=float(v[5]), q=int(v[17]), L=float(v[7]), MHI=float(v[13]), Vflat=float(v[15]),
                            Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9, Ms=0.5 * float(v[7]) * 1e9)
            QG2[v[0]] = dict(D=float(v[2]), Rdisk=float(v[11]), RHI=float(v[14]))
        except ValueError: pass
def load_sparc(cut=True, only=None):
    S = dict(gal=[], R=[], V=[], eV=[], Vg=[], Vd=[], Vb=[], gb=[], go=[])
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        name = os.path.basename(fn).replace("_rotmod.dat", ""); q_ = QG.get(name)
        if only is not None and name != only: continue
        inc, q = (q_["inc"], q_["q"]) if q_ else (0, 3)
        if only is None and (q > 2 or inc < 30): continue
        for l in builtins.open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
            if V <= 0 or R <= 0 or (cut and eV / V >= 0.10): continue
            g_b = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if g_b <= 0: continue
            for k_, x_ in (("gal", name), ("R", R), ("V", V), ("eV", eV), ("Vg", Vg), ("Vd", Vd), ("Vb", Vb), ("gb", g_b), ("go", V * V * 1e6 / (R * KPC))):
                S[k_].append(x_)
    return {k_: np.array(x_) for k_, x_ in S.items()}
SP = load_sparc(); SPG = sorted(set(SP["gal"])); LGSP = np.log10(SP["gb"])

# ---------------------------------------------------------------------------------------------------------------- K5 CFG828 (CFG931's K1 code path)
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
rng828 = np.random.default_rng(828); K5 = {}; k5d = []
for foot in FOOTS:
    for kn, nu in (("nu_e", nu_e12), ("nu_simple", nu_s12)):
        if foot == "alt" and kn == "nu_simple": continue
        a0 = A0[foot]; dS = np.log10(SP["go"] / (SP["gb"] * nu(SP["gb"] / a0))); lg = LGSP; rows = []
        for d in DW828:
            dd = math.log10(d["gobs"] / (d["gbar"] * float(nu(d["gbar"] / a0)))); w = np.abs(lg - math.log10(d["gbar"])) <= 0.15
            rows.append(dict(delta=dd, dS=float(np.median(dS[w])) if w.sum() >= 20 else None))
        inr = [r for r in rows if r["dS"] is not None]; Dd = np.array([r["delta"] - r["dS"] for r in inr])
        boot = [rng828.choice(Dd, len(Dd)).mean() for _ in range(2000)] if len(Dd) else [0]
        out_ = [r["delta"] for r in rows if r["dS"] is None]
        K5[f"{foot}|{kn}"] = dict(N_in=len(inr), mean_D=float(Dd.mean()), se_D=float(np.std(boot)), sparc_median_all=float(np.median(dS)),
                                  out_of_range_mean_delta=float(np.mean(out_)) if out_ else None)
for key in ("canonical|nu_e", "alt|nu_e"):
    for q in ("N_in", "mean_D", "se_D", "sparc_median_all", "out_of_range_mean_delta"):
        k5d.append(abs(K5[key][q] - R828[key][q]))
c828 = K5["canonical|nu_e"]; RES["K5"] = K5
KOK.append(check("K5 CFG828 reproduced through this code path (N_in, mean D, se D, SPARC median, out-of-range mean; canonical+alt nu_e)", max(k5d) <= 1e-9,
                 f"max |diff| {max(k5d):.1e}; canonical: N_in {c828['N_in']}, D {c828['mean_D']:+.3f}+-{c828['se_D']:.3f} dex, dSph out-of-range mean "
                 f"{c828['out_of_range_mean_delta']:+.3f} (alt {K5['alt|nu_e']['out_of_range_mean_delta']:+.3f}), SPARC median {c828['sparc_median_all']:+.3f}"))

# ---------------------------------------------------------------------------------------------------------------- K6 CFG880 dwarfs / CFG919 DW
R919 = J("CFG919_pressure_support_selector", "cfg919_results.json")
F880 = os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880.py")
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG940 refuses to write {file!r} from re-executed committed code")
    return builtins.open(file, mode, *a, **k)
_src = builtins.open(F880).read().split("# ---------------- hierarchical likelihood ----------------", 1)[0]
N880 = {"__file__": F880, "__name__": "cfg880_inputs_ro", "open": _ro_open}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src, F880, "exec"), N880)
def cells_persys(lg, E, sE):
    k = np.digitize(lg, GRID) - 1; out = []
    for b in sorted(set(k)):
        g = np.where(k == b)[0]; n = len(g)
        if n < 3: continue
        se = max(np.std(E[g], ddof=1) / math.sqrt(n), math.sqrt(np.sum(sE[g] ** 2)) / n)
        out.append(dict(w=int(b), E=float(np.mean(E[g])), n=int(n), se=float(se)))
    return out
def gls_mean(E, C):
    Ci = np.linalg.inv(C); one = np.ones(len(E)); return float(one @ Ci @ E / (one @ Ci @ one)), float((one @ Ci @ one) ** -0.5)
DW880 = {}; k6d = []; K6 = {}
for f in FOOTS:
    a0 = A0[f]; A = N880["arrays"](N880["SAMP"], a0); law = np.sqrt(A["sl2"]); s = A["s"]
    E = 2 * np.log(s / law); e = np.where(s > law, A["em"], A["ep"]); sE = 2 * e / s; gN, Ms_ = [], []
    for nm, r12pc in zip(A["names"], A["r12"]):
        L = N880["LVD"][nm]; Ms = 2.0 * 10 ** (0.4 * (4.83 - N880["fnum"](L["M_V"])))
        Mg = N880["gas_in"](N880["fnum"](L.get("mass_HI")), r12pc); gN.append(N880["G"] * (Ms / 2 + Mg) * N880["Msun"] / (r12pc * N880["PC"]) ** 2); Ms_.append(Ms)
    lgb = np.log10(np.array(gN)); c = cells_persys(lgb, E, sE)
    m, se = gls_mean(np.array([x["E"] for x in c]), np.diag([x["se"] ** 2 for x in c]) + FLOOR0_919 ** 2 * np.eye(len(c)))
    ref = R919["byfoot"][f]["V0"]["class_summary"]["DW"]; k6d += [abs(m - ref["E"]), abs(se - ref["se"])]; K6[f] = dict(E=m, se=se, dex=m / LN10, n=len(A["names"]))
    DW880[f] = dict(names=list(A["names"]), lg=lgb, E=E / LN10, sE=sE / LN10)
RES["K6"] = K6
KOK.append(check("K6 CFG919 DW class mean reproduced via CFG880 input slice exec'd read-only (E, se; both footings)", max(k6d) <= 1e-9,
                 f"max |diff| {max(k6d):.1e}; {K6['canonical']['n']} dwarfs; canonical {K6['canonical']['dex']:+.3f} dex, alt {K6['alt']['dex']:+.3f} dex"))
# K7 SPARC loader
KOK.append(check("K7 SPARC loader 2696 points / 147 galaxies", len(SP["gb"]) == 2696 and len(SPG) == 147, f"{len(SP['gb'])} points, {len(SPG)} galaxies"))
K_ALL = all(KOK)
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
RES["K_all_pass"] = K_ALL
if not K_ALL:
    P("  A K-test failed: per FROZEN_CRITERIA section 9 the lane stops; no class is reported."); RES["class"] = None; finish(2)
if MODE == "K":
    P("\n  K only: stopping before any residual is computed.")
    finish(0)

# =====================================================================================================================  estimators
# stellar size relation: OLS log10 Rdisk on log10 M* over SPARC Table 1, 0 < M* < 1e9, Rdisk > 0
xs = np.array([math.log10(QG[g]["Ms"]) for g in QG if 0 < QG[g]["Ms"] < 1e9 and QG2[g]["Rdisk"] > 0])
ys = np.array([math.log10(QG2[g]["Rdisk"]) for g in QG if 0 < QG[g]["Ms"] < 1e9 and QG2[g]["Rdisk"] > 0])
FB, FA = np.polyfit(xs, ys, 1); FRMS = float(np.std(ys - (FA + FB * xs), ddof=2))
P(f"\n  stellar size relation (SPARC Table 1, M* < 1e9, N {len(xs)}): log10 R_d = {FA:+.3f} + {FB:.3f} log10 M*  (rms {FRMS:.3f} dex)")
RES["size_relation"] = dict(a=float(FA), b=float(FB), rms=FRMS, n=int(len(xs)))
_GS = {}
def gas_scale(lHI, root="large", RHI_kpc=None):
    """CFG873/874 recipe (Wang+16 R_HI, Sigma(R_HI) = 1 Msun/pc^2, exponential disc; extended root primary; fallback R_HI/2). kpc."""
    key = (round(lHI, 12), root, None if RHI_kpc is None else round(RHI_kpc, 12))
    if key not in _GS:
        MHI = 10 ** lHI; RHI = (0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3) if RHI_kpc is None else RHI_kpc * 1e3   # pc
        grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); vals = MHI / (2 * math.pi * grid * grid) * np.exp(-RHI / grid) - 1.0
        roots = [grid[i] for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
        Rs = (max(roots) if root == "large" else min(roots)) if roots else RHI / 2
        _GS[key] = (Rs / 1e3, not roots, RHI / 1e3)
    return _GS[key]
fexp = lambda x: 1.0 - (1.0 + x) * math.exp(-x)
def freeman_g(M, Rd, R):                                       # thin exponential disc, SI acceleration at R (kpc inputs)
    y = R / (2 * Rd); br = i0e(y) * k0e(y) - i1e(y) * k1e(y)
    V2 = 2 * G * M * MSUN / (Rd * KPC) * y * y * br
    return V2 / (R * KPC)
def gbar_of(est, s):
    R = s["R"]
    if est == "A": return G * 10 ** s["lMbA"] * MSUN / (R * KPC) ** 2
    Ms, MHI = 10 ** s["lMs"], 10 ** s["lHI"]
    Rd = 10 ** (FA + FB * s["lMs"]) * (2.0 if est == "B4" else (0.5 if est == "B6" else 1.0))
    Rs = gas_scale(s["lHI"], "small" if est == "B2" else "large", R if est == "B3" else None)[0]
    if est == "B5": return freeman_g(Ms, Rd, R) + freeman_g(1.33 * MHI, Rs, R)
    return G * (fexp(R / Rd) * Ms + fexp(R / Rs) * 1.33 * MHI) * MSUN / (R * KPC) ** 2
EST_ALL = ("A", "B", "B2", "B3", "B4", "B5", "B6")

def state(g, var):
    s = dict(V=g["Vcor"], eV=g["eV"], R=g["R"], eR=g["eR"], lMs=g["lMs"], lHI=g["lHI"], lMbA=g["lMbA"], elMs=g["elMs"], elHI=g["elHI"], elMb=g["elMb"])
    ad = g["Vcor"] ** 2 - g["Vrot"] ** 2
    if var == "V1": s["V"], s["eV"] = g["Vrot"], g["eVr"]
    if var == "V2": s["V"] = math.sqrt(g["Vrot"] ** 2 + 2 * ad)
    if var in ("V3", "V4", "CUP"):
        ip = max(g["i"] - g["ei"], 10.0) if var in ("V3", "CUP") else min(g["i"] + g["ei"], 90.0)
        vr = g["Vrot"] * math.sin(math.radians(g["i"])) / math.sin(math.radians(ip))
        s["V"] = math.sqrt(vr ** 2 + (2 if var == "CUP" else 1) * ad)
    fD = {"V6": 0.9, "CUP": 0.9, "V7": 1.1}.get(var)
    if fD:
        s["R"] *= fD; s["eR"] *= fD; dl = math.log10(fD * fD)
        s["lMs"] += dl; s["lHI"] += dl; s["lMbA"] += dl
    if var == "V16": s["R"] = g["Rtab"]
    return s

def resid(s, est, foot, kern="e"):
    gobs = (s["V"] * 1e3) ** 2 / (s["R"] * KPC); gb = gbar_of(est, s)
    return math.log10(gobs / (gb * float(KERN[kern](gb / A0[foot])))), gb, gobs

def galaxy_E(g, est, foot, var="V0", kern="e"):
    s = state(g, var); E, gb, go = resid(s, est, foot, kern)
    pert = [("V", "eV", False), ("R", "eR", False)] + ([("lMbA", "elMb", True)] if est == "A" else [("lMs", "elMs", True), ("lHI", "elHI", True)])
    v2 = 0.0
    for k_, ek, _ in pert:
        sp, sm = dict(s), dict(s); sp[k_] = s[k_] + s[ek]; sm[k_] = s[k_] - s[ek]
        v2 += ((resid(sp, est, foot, kern)[0] - resid(sm, est, foot, kern)[0]) / 2) ** 2
    return dict(name=g["name"], E=E, sE=math.sqrt(v2), lg=math.log10(gb), gb=gb, go=go, lgN=math.log10(go / gb), RP=g["RP"], i=g["i"],
                DPV=g["DPV"], lMs=g["lMs"], survey=g["survey"])

SUBSET = {"V5": lambda g: g["i"] >= 40, "V13": lambda g: g["RP"] == "P", "V14": lambda g: g["RP"] == "R", "V15": lambda g: g["DPV"] >= 100}
def rotators(est, foot, var="V0", kern="e"):
    sel = [g for g in GALS if SUBSET.get(var, lambda g: True)(g)]
    vv = var if var in ("V1", "V2", "V3", "V4", "V6", "V7", "V16", "CUP") else "V0"
    return [galaxy_E(g, est, foot, vv, kern) for g in sel]

# ---------------------------------------------------------------------------------------------------------------- comparison groups
def dsph_group(foot, var="V0"):
    if var == "V10":
        d = DW880[foot]; return dict(names=d["names"], lg=np.array(d["lg"]), E=np.array(d["E"]), sE=np.array(d["sE"]))
    nu = KERN["s" if var == "V9" else "e"]; gb = np.array([d["gbar"] for d in DW828]); go = np.array([d["gobs"] for d in DW828])
    return dict(names=[d["name"] for d in DW828], lg=np.log10(gb), E=np.log10(go / (gb * nu(gb / A0[foot]))),
                sE=np.array([2 * d["eso"] / (d["so"] * LN10) for d in DW828]))
OVERLAP = {"DDO154": "DDO154", "NGC3109": "NGC3109", "NGC3741": "NGC3741", "HoII": "UGC04305", "UGC04483": "UGC04483",
           "DDO126": "UGC07559", "DDO125": "UGC07577", "WLM": "UGCA444"}
_SPC = {}
def sparc_group(foot, kern="e"):
    if (foot, kern) not in _SPC:
        dl = np.log10(SP["go"] / (SP["gb"] * KERN[kern](SP["gb"] / A0[foot]))); k = np.digitize(LGSP, GRID) - 1; out = {}
        for gname in SPG:
            if gname in OVERLAP.values(): continue
            m = SP["gal"] == gname; out[gname] = {int(c): float(np.mean(dl[m & (k == c)])) for c in sorted(set(k[m]))}
        _SPC[(foot, kern)] = out
    return _SPC[(foot, kern)]

# ---------------------------------------------------------------------------------------------------------------- statistics
def se_of(E, s):
    n = len(E); sd = float(np.std(E, ddof=1)) / math.sqrt(n) if n > 1 else 0.0
    return max(sd, math.sqrt(float(np.sum(np.square(s)))) / n)

def stats(rot, dsph, sparc, window, F, Eover=None):
    """rot: list of per-galaxy dicts; window: 'W1' or 'WS'; Eover: optional {name: E} replacing E (plants)."""
    sel = [r for r in rot if (window == "WS" or r["lg"] < LGW1)]
    st = dict(N=len(sel), names=[r["name"] for r in sel], F=F)
    if not sel:
        st.update(mean=None, se=None, D=None, sD=None, E_dsph_m=None, D_SP=None); return st
    E = np.array([Eover[r["name"]] if Eover else r["E"] for r in sel]); s = np.array([r["sE"] for r in sel])
    cr = np.array([cell(r["lg"]) for r in sel])
    st["mean"] = float(E.mean()); st["se"] = math.sqrt(se_of(E, s) ** 2 + F ** 2); st["se_stat"] = se_of(E, s)
    cd = np.digitize(dsph["lg"], GRID) - 1
    elig = sorted(c for c in set(cr.tolist()) if np.sum(cd == c) >= 3)
    st["cells_rot"] = {cname(c): int(np.sum(cr == c)) for c in sorted(set(cr.tolist()))}
    if elig:
        m = np.isin(cr, elig); Nm = int(m.sum()); w = {c: np.sum(cr == c) / Nm for c in elig}
        mc = {c: float(np.mean(dsph["E"][cd == c])) for c in elig}
        sec = {c: max(float(np.std(dsph["E"][cd == c], ddof=1)) / math.sqrt(np.sum(cd == c)),
                      math.sqrt(float(np.sum(dsph["sE"][cd == c] ** 2))) / np.sum(cd == c)) for c in elig}
        Ed = sum(w[c] * mc[c] for c in elig); sed = math.sqrt(sum(w[c] ** 2 * sec[c] ** 2 for c in elig))
        Erm = float(E[m].mean()); serm = se_of(E[m], s[m])
        st.update(E_dsph_m=Ed, se_dsph_m=sed, E_rot_m=Erm, se_rot_m=serm, N_m=Nm, D=Ed - Erm,
                  sD=math.sqrt(serm ** 2 + sed ** 2 + 2 * F ** 2), cells_dsph={cname(c): dict(n=int(np.sum(cd == c)), mean=mc[c], w=float(w[c])) for c in elig},
                  elig=elig)
    else:
        st.update(E_dsph_m=None, D=None, sD=None, elig=[])
    if sparc is not None:
        eligS = sorted(c for c in set(cr.tolist()) if sum(1 for gname in sparc if c in sparc[gname]) >= 3)
        if eligS:
            m = np.isin(cr, eligS); Nm = int(m.sum()); w = {c: np.sum(cr == c) / Nm for c in eligS}
            vals = {c: np.array([sparc[gname][c] for gname in sparc if c in sparc[gname]]) for c in eligS}
            Es = sum(w[c] * vals[c].mean() for c in eligS); ses = math.sqrt(sum(w[c] ** 2 * (np.std(vals[c], ddof=1) / math.sqrt(len(vals[c]))) ** 2 for c in eligS))
            Erm = float(E[m].mean()); serm = se_of(E[m], s[m])
            st.update(E_SP_m=float(Es), D_SP=Erm - float(Es), sD_SP=math.sqrt(serm ** 2 + ses ** 2 + 2 * F ** 2), N_SP_m=Nm,
                      cells_SP={cname(c): int(len(vals[c])) for c in eligS})
        else:
            st.update(E_SP_m=None, D_SP=None, sD_SP=None)
    return st

def cls_W1(st):
    if st["N"] < NMIN: return "NOT DIAGNOSTIC (DATA)"
    m, se = st["mean"], st["se"]; hasD = st["D"] is not None
    if m <= -2 * se: return "BELOW"
    if m >= THR_ABOVE and hasD and abs(st["D"]) < 2 * st["sD"]: return "ABOVE" + (" (z < 2)" if m < 2 * se else "")
    if abs(m) < 2 * se and hasD and st["D"] >= 3 * st["sD"]: return "ON"
    if not hasD: return "NOT DIAGNOSTIC (NO dSph MATCH)"
    if m >= 2 * se and st["D"] > -2 * st["sD"]: return "NOT DIAGNOSTIC (ELEVATED BELOW dSph LEVEL)"
    if abs(m) < 2 * se: return "NOT DIAGNOSTIC (UNRESOLVED)"
    return "NOT DIAGNOSTIC (OTHER)"
def cls_WS(st):
    if st["N"] < NMIN: return "NOT DIAGNOSTIC (DATA)"
    m, se = st["mean"], st["se"]
    return "S-BELOW" if m <= -2 * se else ("S-ABOVE" if m >= 2 * se else "S-ON")
def tok(c): return c.split(" (")[0]
def combine(per):
    if per["canonical"] == per["alt"]: return per["canonical"]
    if tok(per["canonical"]) == tok(per["alt"]): return tok(per["canonical"]) + f" (canonical {per['canonical']}; alt {per['alt']})"
    return "NOT DIAGNOSTIC (SPLIT BY FOOTING)"

def run(est, foot, var="V0", window="W1", Eover=None, rot=None):
    kern = "s" if var == "V9" else "e"
    rot = rotators(est, foot, var, kern) if rot is None else rot
    F = {"V11": 0.0, "V12": 0.10}.get(var, FLOOR)
    st = stats(rot, dsph_group(foot, var), sparc_group(foot, kern), window, F, Eover)
    st["cls"] = cls_W1(st) if window == "W1" else cls_WS(st)
    return st, rot

def fmt(st):
    if st["N"] == 0: return f"{st['cls']:40s} N 0"
    s = f"{st['cls']:40s} N {st['N']:2d}  mean E {st['mean']:+.3f} +- {st['se']:.3f} (z {st['mean'] / st['se']:+.1f})"
    if st.get("D") is not None: s += f"  dSph_m {st['E_dsph_m']:+.3f} D {st['D']:+.3f} +- {st['sD']:.3f} (z {st['D'] / st['sD']:+.1f}, N_m {st['N_m']})"
    else: s += "  (no dSph match)"
    if st.get("D_SP") is not None: s += f"  D_SP {st['D_SP']:+.3f} +- {st['sD_SP']:.3f}"
    return s

# =====================================================================================================================  real V0 (needed by every mode)
REAL = {(e, f, w): run(e, f, "V0", w)[0] for e in ("A", "B") for f in FOOTS for w in ("W1", "WS")}
ROT0 = {(e, f): rotators(e, f) for e in EST_ALL for f in FOOTS}

# =====================================================================================================================  MUTATE plant
if MODE == "plant":
    P("\n=== MUTATE plant (each window rotator's E -> T + (E_i - mean); sigma_E kept; g_bar and window membership unchanged)")
    ok_all = True; MP = {}
    for e in ("A", "B"):
        for f in FOOTS:
            for w in ("W1", "WS"):
                r0 = REAL[(e, f, w)]; key = f"{e}|{f}|{w}"; rot = ROT0[(e, f)]
                if r0["N"] == 0:
                    MP[key] = dict(status="no rotator in window"); P(f"  [{key}] no rotator in the window: plants not required (not recoverable at N = 0)"); continue
                inw = [r for r in rot if (w == "WS" or r["lg"] < LGW1)]; mE = float(np.mean([r["E"] for r in inw]))
                res = {}
                plants = [("P37", PL), ("P0", 0.0), ("P-37", -PL)] + ([("PdSph", r0["E_dsph_m"])] if r0.get("E_dsph_m") is not None else [])
                for nm, T in plants:
                    Eo = {r["name"]: T + (r["E"] - mE) for r in inw}
                    st = run(e, f, "V0", w, Eover=Eo, rot=rot)[0]; pipe = abs(st["mean"] - T) <= 1e-9
                    gate = r0["N"] >= NMIN
                    if w == "W1":
                        hasD = r0.get("D") is not None
                        if nm == "P37": req, why = (gate and hasD and abs(r0["E_dsph_m"] - PL) < 2 * r0["sD"]), "gate+D+|E_dSph,m-0.37|<2sD"; want = "ABOVE"
                        elif nm == "PdSph": req, why = (gate and hasD and r0["E_dsph_m"] >= THR_ABOVE), "gate+D+E_dSph,m>=0.20"; want = "ABOVE"
                        elif nm == "P0": req, why = (gate and hasD and r0["E_dsph_m"] >= 3 * r0["sD"]), "gate+D+E_dSph,m>=3sD (power)"; want = "ON"
                        else: req, why = (gate and PL > 2 * r0["se"]), "gate+0.37>2se"; want = "BELOW"
                    else:
                        want = {"P37": "S-ABOVE", "P0": "S-ON", "P-37": "S-BELOW", "PdSph": None}[nm]
                        req = gate and (want is not None) and (nm == "P0" or PL > 2 * r0["se"]) if nm != "PdSph" else False
                        why = "gate+0.37>2se" if nm in ("P37", "P-37") else ("gate" if nm == "P0" else "reported only")
                    got = tok(st["cls"]); passed = (got == want) if req else None
                    if not pipe or (req and not passed): ok_all = False
                    res[nm] = dict(T=T, pipeline_ok=pipe, required=req, why=why, want=want, cls=st["cls"], passed=passed, mean=st["mean"], se=st["se"],
                                   D=st.get("D"), sD=st.get("sD"))
                    P(f"  [{key}] {nm:5s} T {T:+.3f}: pipeline {'OK' if pipe else 'FAIL'}; {fmt(st)}  -> "
                      + (f"required {want}: {'PASS' if passed else 'FAIL'}" if req else f"not required ({why} not met; reported)"))
                MP[key] = res
    RES["mutate_plant"] = MP; RES["mutate_ok"] = ok_all
    P(f"\n  MUTATE plant: {'all required controls met' if ok_all else 'A REQUIRED CONTROL FAILED'}")
    finish(0 if ok_all else 1)

# =====================================================================================================================  MUTATE shuffle
def shuffle_D(rot_in, dsph, F, rng, Eover=None, ndraw=1000):
    """Within-cell permutation of rotator/dSph labels over eligible cells; returns arrays of D and z."""
    cr = np.array([cell(r["lg"]) for r in rot_in]); cd = np.digitize(dsph["lg"], GRID) - 1
    elig = sorted(c for c in set(cr.tolist()) if np.sum(cd == c) >= 3)
    if not elig: return None
    pools = []
    for c in elig:
        Er = [Eover[r["name"]] if Eover else r["E"] for r, cc in zip(rot_in, cr) if cc == c]; sr = [r["sE"] for r, cc in zip(rot_in, cr) if cc == c]
        Edc = dsph["E"][cd == c].tolist(); sdc = dsph["sE"][cd == c].tolist()
        pools.append((c, np.array(Er + Edc), np.array(sr + sdc), len(Er), len(Edc)))
    Nm = sum(p[3] for p in pools); Ds, Zs = [], []
    for t in range(ndraw):
        ER, SR, Ed, sed2 = [], [], 0.0, 0.0
        for c, Ev, sv, nr, nd in pools:
            perm = rng.permutation(nr + nd); ir, idd = perm[:nr], perm[nr:]
            ER += Ev[ir].tolist(); SR += sv[ir].tolist(); wc = nr / Nm
            mc = Ev[idd].mean(); sec = max(np.std(Ev[idd], ddof=1) / math.sqrt(nd), math.sqrt(np.sum(sv[idd] ** 2)) / nd)
            Ed += wc * mc; sed2 += wc ** 2 * sec ** 2
        ER, SR = np.array(ER), np.array(SR); D = Ed - ER.mean(); sD = math.sqrt(se_of(ER, SR) ** 2 + sed2 + 2 * F ** 2)
        Ds.append(D); Zs.append(D / sD)
    return np.array(Ds), np.array(Zs)

if MODE == "shuffle":
    P("\n=== MUTATE shuffle (rotator/dSph labels permuted within each eligible cell; 1000 draws, rng 9401)")
    ok_all = True; MS = {}
    for e in ("A", "B"):
        for f in FOOTS:
            for w in ("W1", "WS"):
                r0 = REAL[(e, f, w)]; key = f"{e}|{f}|{w}"
                if r0["N"] < NMIN or r0.get("D") is None:
                    MS[key] = dict(status="not run: " + ("data gate (N < 5)" if r0["N"] < NMIN else "no dSph match")); P(f"  [{key}] {MS[key]['status']}"); continue
                rot = [r for r in ROT0[(e, f)] if (w == "WS" or r["lg"] < LGW1)]; rin = [r for r in rot if cell(r["lg"]) in r0["elig"]]
                dsph = dsph_group(f); rng = np.random.default_rng(9401)
                Ds, Zs = shuffle_D(rin, dsph, FLOOR, rng)
                med = float(np.median(Ds)); f3 = float(np.mean(np.abs(Zs) >= 3)); f2 = float(np.mean(np.abs(Zs) >= 2))
                s1 = abs(med) <= 0.25 * r0["sD"] and f3 <= 0.05
                # S2 on the P0 data
                mE = float(np.mean([r["E"] for r in rot])); Eo = {r["name"]: 0.0 + (r["E"] - mE) for r in rot}
                p0 = run(e, f, "V0", w, Eover=Eo, rot=ROT0[(e, f)])[0]
                req2 = p0.get("D") is not None and p0["D"] >= 2 * p0["sD"]
                Ds2, Zs2 = shuffle_D(rin, dsph, FLOOR, np.random.default_rng(9402), Eover=Eo)
                med2 = float(np.median(Ds2)); s2 = (med2 <= 0.5 * p0["D"]) if req2 else None
                if not s1 or (req2 and not s2): ok_all = False
                MS[key] = dict(D_real=r0["D"], sD_real=r0["sD"], S1_median_D=med, S1_frac_z3=f3, S1_frac_z2=f2, S1_pass=s1,
                               P0_D=p0.get("D"), P0_sD=p0.get("sD"), S2_required=req2, S2_median_D=med2, S2_pass=s2)
                P(f"  [{key}] S1 real: D {r0['D']:+.3f} +- {r0['sD']:.3f}; shuffled median D {med:+.3f} (bar {0.25 * r0['sD']:.3f}), |z|>=3 {100 * f3:.1f}% "
                  f"(bar 5%), |z|>=2 {100 * f2:.1f}% -> {'PASS' if s1 else 'FAIL'}")
                P(f"           S2 on P0: D(P0) {p0['D']:+.3f} +- {p0['sD']:.3f}; shuffled median {med2:+.3f} -> "
                  + (f"required <= {0.5 * p0['D']:.3f}: {'PASS' if s2 else 'FAIL'}" if req2 else "not required (D(P0) < 2 sD)"))
    RES["mutate_shuffle"] = MS; RES["mutate_ok"] = ok_all
    P(f"\n  MUTATE shuffle: {'all required controls met' if ok_all else 'A REQUIRED CONTROL FAILED'}")
    finish(0 if ok_all else 1)

# =====================================================================================================================  MAIN
P("\n=== Per-galaxy table (V = V_cor, R = (D_PV/2) x Dist; E in dex; A = total M_bary, B = exponential-disc enclosed)")
P("  name       survey        R/P   i   R_kpc  V   log g_obs  log gA   log gB   E_A can   E_A alt   E_B can   E_B alt   sE_A  sE_B  log(gobs/gA) log(gobs/gB)  fallback")
TABLE = []
for j, g in enumerate(GALS):
    ra = {f: ROT0[("A", f)][j] for f in FOOTS}; rb = {f: ROT0[("B", f)][j] for f in FOOTS}
    fb = gas_scale(g["lHI"])[1]
    row = dict(name=g["name"], survey=g["survey"], RP=g["RP"], i=g["i"], R=g["R"], Vcor=g["Vcor"], eV=g["eV"], lMs=g["lMs"], lHI=g["lHI"], lMb=g["lMbA"],
               lgobs=math.log10(ra["canonical"]["go"]), lgA=ra["canonical"]["lg"], lgB=rb["canonical"]["lg"],
               E_A={f: ra[f]["E"] for f in FOOTS}, E_B={f: rb[f]["E"] for f in FOOTS}, sE_A=ra["canonical"]["sE"], sE_B=rb["canonical"]["sE"],
               lgN_A=ra["canonical"]["lgN"], lgN_B=rb["canonical"]["lgN"], gas_root_fallback=fb,
               Rs=gas_scale(g["lHI"])[0], RHI_wang=gas_scale(g["lHI"])[2], Rd=10 ** (FA + FB * g["lMs"]))
    TABLE.append(row)
    P(f"  {g['name']:10s} {g['survey']:13s} {g['RP']}   {g['i']:3.0f} {g['R']:6.2f} {g['Vcor']:3.0f}  {row['lgobs']:7.2f}  {row['lgA']:7.2f}  {row['lgB']:7.2f}  "
      f"{row['E_A']['canonical']:+7.3f}  {row['E_A']['alt']:+7.3f}   {row['E_B']['canonical']:+7.3f}  {row['E_B']['alt']:+7.3f}   {row['sE_A']:.3f} {row['sE_B']:.3f}"
      f"   {row['lgN_A']:+6.2f}       {row['lgN_B']:+6.2f}     {'yes' if fb else 'no'}")
RES["table"] = TABLE
P(f"  gas root fallbacks: {sum(r['gas_root_fallback'] for r in TABLE)}/25;  median R_max/R_HI(Wang) {np.median([r['R'] / r['RHI_wang'] for r in TABLE]):.2f};"
  f"  median R_max/R_s {np.median([r['R'] / r['Rs'] for r in TABLE]):.2f};  median R_max/R_d* {np.median([r['R'] / r['Rd'] for r in TABLE]):.2f}")

P("\n=== N at g_bar < 1e-12 per estimator (canonical footing; g_bar does not depend on the footing)")
for e in EST_ALL:
    P(f"  {e:3s}: N(W1) = {sum(1 for r in ROT0[(e, 'canonical')] if r['lg'] < LGW1):2d}   " + ", ".join(r["name"] for r in ROT0[(e, "canonical")] if r["lg"] < LGW1))

VARS = ("V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16")
VDESC = {"V0": "primary", "V1": "V = V_rot (no AD)", "V2": "AD term x2", "V3": "i - e_i", "V4": "i + e_i", "V5": "subset i >= 40",
         "V6": "distance -10%", "V7": "distance +10%", "V9": "kernel nu_simple", "V10": "dSphs = CFG880 83 LVD", "V11": "floor 0",
         "V12": "floor 0.10", "V13": "subset plateau (P)", "V14": "subset rising (R)", "V15": "subset D_PV >= 100\"", "V16": "tabulated R_max"}
NONSUB = ("V1", "V2", "V3", "V4", "V6", "V7", "V9", "V10", "V11", "V12", "V16")
MAIN = {}
for w in ("W1", "WS"):
    P(f"\n=== {'PRIMARY window W1: g_bar < 1e-12' if w == 'W1' else 'SECONDARY WS: all g_bar (labelled secondary)'}")
    for e in EST_ALL:
        for f in FOOTS:
            for v in (VARS if e in ("A", "B") else ("V0",)):
                MAIN[(w, e, f, v)] = REAL[(e, f, w)] if (v == "V0" and e in ("A", "B")) else run(e, f, v, w)[0]
    for e in EST_ALL:
        P(f"  --- estimator {e}")
        for f in FOOTS:
            P(f"   [{f}]")
            for v in (VARS if e in ("A", "B") else ("V0",)):
                P(f"     {v:4s} {VDESC[v]:24s} {fmt(MAIN[(w, e, f, v)])}")

# C-UP corner (B + V2 + V3 + V6), INFO
CUP = {}
for w in ("W1", "WS"):
    for f in FOOTS:
        st = run("B", f, "CUP", w)[0]; CUP[f"{w}|{f}"] = st
P("\n=== C-UP corner (INFO, no class weight): B + AD x2 + i - e_i + distance -10%")
for k_, st in CUP.items(): P(f"  {k_:14s} {fmt(st)}")

# classes
CLS = {}
for w in ("W1", "WS"):
    per = {e: {f: MAIN[(w, e, f, "V0")]["cls"] for f in FOOTS} for e in EST_ALL}
    comb = {e: combine(per[e]) for e in EST_ALL}
    brk = [f"{e}: {comb[e]}" for e in EST_ALL[1:] if tok(comb[e]) != tok(comb["A"])]
    brk_sub = [f"{e}: {comb[e]}" for e in EST_ALL[1:] if tok(comb[e]) == tok(comb["A"]) and comb[e] != comb["A"]]
    frag = [f"{v}/{f}: {MAIN[(w, 'A', f, v)]['cls']}" for f in FOOTS for v in NONSUB if tok(MAIN[(w, "A", f, v)]["cls"]) != tok(per["A"][f])]
    subchg = [f"{v}/{f}: {MAIN[(w, 'A', f, v)]['cls']}" for f in FOOTS for v in ("V5", "V13", "V14", "V15") if tok(MAIN[(w, "A", f, v)]["cls"]) != tok(per["A"][f])]
    fragB = [f"{v}/{f}: {MAIN[(w, 'B', f, v)]['cls']}" for f in FOOTS for v in NONSUB if tok(MAIN[(w, "B", f, v)]["cls"]) != tok(per["B"][f])]
    label = comb["A"] + (f"  [BRACKET-DEPENDENT: {'; '.join(brk)}]" if brk else "") + ("  [FRAGILE]" if frag else "")
    CLS[w] = dict(per_estimator=per, combined=comb, bracket_differs=brk, bracket_sublabel=brk_sub, fragile=frag, subset_changes=subchg,
                  B_variant_changes=fragB, label=label)
    P(f"\n=== {'LANE CLASS (W1, estimator A)' if w == 'W1' else 'SECONDARY CLASS (WS, estimator A)'}: {label}")
    for e in EST_ALL: P(f"    {e:3s}: {comb[e]}   (canonical {per[e]['canonical']}; alt {per[e]['alt']})")
    if frag: P("    FRAGILE (non-subset variants changing A's class): " + "; ".join(frag))
    if subchg: P("    subset variants changing A's class (no FRAGILE weight): " + "; ".join(subchg))
    if fragB: P("    variants changing B's class (reported): " + "; ".join(fragB))
RES["classes"] = CLS; RES["lane_class"] = CLS["W1"]["label"]; RES["secondary_class"] = CLS["WS"]["label"]
RES["main"] = {"|".join(k): v for k, v in MAIN.items()}; RES["cup"] = CUP

# =====================================================================================================================  INFO
P("\n=== INFO (no class weight)")
INFO = {}
# I1 rising vs plateau
P("  I1 rising (R) vs plateau (P) (mean E +- se, N), WS:")
for e in ("A", "B"):
    for f in FOOTS:
        a, b = MAIN[("WS", e, f, "V14")], MAIN[("WS", e, f, "V13")]
        INFO[f"I1|{e}|{f}"] = dict(rising=dict(N=a["N"], mean=a["mean"], se=a["se"]), plateau=dict(N=b["N"], mean=b["mean"], se=b["se"]))
        P(f"     {e} {f:9s}: rising {a['mean']:+.3f} +- {a['se']:.3f} (N {a['N']}); plateau {b['mean']:+.3f} +- {b['se']:.3f} (N {b['N']}); R - P {a['mean'] - b['mean']:+.3f}")
# I2 M* < 1e7
P("  I2 M* < 1e7 subset (log M* < 7):")
for e in ("A", "B"):
    for f in FOOTS:
        rr = [r for r in ROT0[(e, f)] if r["lMs"] < 7.0]
        for w in ("W1", "WS"):
            sel = [r for r in rr if (w == "WS" or r["lg"] < LGW1)]
            if sel:
                E_ = np.array([r["E"] for r in sel]); s_ = np.array([r["sE"] for r in sel]); se_ = math.sqrt(se_of(E_, s_) ** 2 + FLOOR ** 2)
                INFO[f"I2|{e}|{f}|{w}"] = dict(N=len(sel), mean=float(E_.mean()), se=se_, names=[r["name"] for r in sel])
                P(f"     {e} {f:9s} {w}: N {len(sel)}, mean E {E_.mean():+.3f} +- {se_:.3f}  ({', '.join(r['name'] for r in sel)})")
            else:
                INFO[f"I2|{e}|{f}|{w}"] = dict(N=0); P(f"     {e} {f:9s} {w}: N 0")
# I3 Newton reading
P("  I3 Newtonian reading (CFG936): mean log10(g_obs/g_bar) +- se:")
for e in EST_ALL:
    for w in ("W1", "WS"):
        sel = [r for r in ROT0[(e, "canonical")] if (w == "WS" or r["lg"] < LGW1)]
        if not sel: P(f"     {e:3s} {w}: N 0"); continue
        x = np.array([r["lgN"] for r in sel]); s_ = np.array([r["sE"] for r in sel])
        se_ = math.sqrt(se_of(x, s_) ** 2 + FLOOR ** 2); lab = "AT NEWTON" if abs(x.mean()) < 2 * se_ else ("ABOVE NEWTON" if x.mean() > 0 else "BELOW NEWTON")
        INFO[f"I3|{e}|{w}"] = dict(N=len(sel), mean=float(x.mean()), se=se_, label=lab)
        P(f"     {e:3s} {w}: N {len(sel):2d}, {x.mean():+.3f} +- {se_:.3f} -> {lab}")
# I4 overlap calibration
P("  I4 overlap calibration vs SPARC at the same angular radius (rotmod without point cut; R_SP = R_max x D_SP/D_McQ):")
P("     name      SPARC     Q  Inc   D_McQ  D_SP   R_McQ  R_SP  [SPARC R range]   V_McQ  V_SP   E_McQ(A) E_McQ(B) E_SP    log(gSP/gA) log(gSP/gB)  (canonical)")
I4 = []
for mn, sn in OVERLAP.items():
    g = next(x for x in GALS if x["name"] == mn); S1 = load_sparc(cut=False, only=sn)
    Dsp = QG2[sn]["D"]; Rsp = g["R"] * Dsp / g["D"]; Rlo, Rhi = float(S1["R"].min()), float(S1["R"].max())
    row = dict(name=mn, sparc=sn, Q=QG[sn]["q"], inc=QG[sn]["inc"], D_mcq=g["D"], D_sp=Dsp, R_mcq=g["R"], R_sp=Rsp, R_range=(Rlo, Rhi), V_mcq=g["Vcor"])
    if Rsp > 1.1 * Rhi or Rsp < Rlo / 1.1:
        row["status"] = "out of range"; I4.append(row)
        P(f"     {mn:9s} {sn:9s} {QG[sn]['q']}  {QG[sn]['inc']:4.0f}  {g['D']:5.2f}  {Dsp:5.2f}  {g['R']:5.2f}  {Rsp:5.2f}  [{Rlo:.2f}, {Rhi:.2f}]   out of range"); continue
    o = np.argsort(S1["R"]); Rr = S1["R"][o]
    Vi = float(np.interp(Rsp, Rr, S1["V"][o])); Vg = float(np.interp(Rsp, Rr, S1["Vg"][o])); Vd = float(np.interp(Rsp, Rr, S1["Vd"][o])); Vb = float(np.interp(Rsp, Rr, S1["Vb"][o]))
    gsp = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (Rsp * KPC); gosp = Vi * Vi * 1e6 / (Rsp * KPC)
    j = [x["name"] for x in GALS].index(mn); ra, rb = ROT0[("A", "canonical")][j], ROT0[("B", "canonical")][j]
    Esp = math.log10(gosp / (gsp * float(nu_e15(gsp / A0["canonical"]))))
    row.update(status="ok", V_sp=Vi, E_A=ra["E"], E_B=rb["E"], E_sp=Esp, lr_A=math.log10(gsp / ra["gb"]), lr_B=math.log10(gsp / rb["gb"]),
               extrapolated=bool(Rsp > Rhi or Rsp < Rlo))
    I4.append(row)
    P(f"     {mn:9s} {sn:9s} {QG[sn]['q']}  {QG[sn]['inc']:4.0f}  {g['D']:5.2f}  {Dsp:5.2f}  {g['R']:5.2f}  {Rsp:5.2f}  [{Rlo:.2f}, {Rhi:.2f}]{'*' if row['extrapolated'] else ' '}  "
      f"{g['Vcor']:4.0f}  {Vi:5.1f}   {ra['E']:+.3f}   {rb['E']:+.3f}   {Esp:+.3f}    {row['lr_A']:+.3f}      {row['lr_B']:+.3f}")
okr = [r for r in I4 if r["status"] == "ok"]
if okr:
    mA, mB = float(np.median([r["lr_A"] for r in okr])), float(np.median([r["lr_B"] for r in okr]))
    better = "A" if abs(mA) < abs(mB) else "B"
    P(f"     median log(g_bar^SPARC/g_bar^A) {mA:+.3f}, /g_bar^B {mB:+.3f} (N {len(okr)}) -> better-calibrated end of the bracket: {better};"
      f"  median E_McQ(A) - E_SP {np.median([r['E_A'] - r['E_sp'] for r in okr]):+.3f}, E_McQ(B) - E_SP {np.median([r['E_B'] - r['E_sp'] for r in okr]):+.3f};"
      f"  median V_McQ/V_SP {np.median([r['V_mcq'] / r['V_sp'] for r in okr]):.3f}   (* = held at the SPARC edge, within 10 %)")
    INFO["I4_summary"] = dict(median_lr_A=mA, median_lr_B=mB, better=better, N=len(okr))
INFO["I4"] = I4
# I5 survey split
P("  I5 survey split (mean E, N), WS:")
for e in ("A", "B"):
    for f in FOOTS:
        parts = []
        for sv in ("SHIELD", "VLA-ANGST", "LITTLE THINGS"):
            x = [r["E"] for r in ROT0[(e, f)] if r["survey"] == sv]; parts.append(f"{sv} {np.mean(x):+.3f} (N {len(x)})")
            INFO[f"I5|{e}|{f}|{sv}"] = dict(N=len(x), mean=float(np.mean(x)))
        P(f"     {e} {f:9s}: " + "; ".join(parts))
RES["info"] = INFO
finish(0)
