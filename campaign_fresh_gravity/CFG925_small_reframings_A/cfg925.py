"""CFG925 -- three small zero-constant reframings of the pressure-supported excess (A): R1 law-Jeans estimator, R2 self-sourcing,
R3 EFE sign.
Criteria: FROZEN_CRITERIA.md (661668f32, committed alone before this script and before any number of this lane);
AMENDMENT_A1.md (cc07e00a3, POST HOC after the first K-only run, before MUTATE/main): K6 residual bar conditioning-aware.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg925.py      (CFG925_KONLY=1 -> _K outputs; CFG925_MUTATE=1 -> _MUTATE outputs).
Inputs: CFG921's source up to its "posit engines" marker exec'd read-only (which exec's CFG919 -> CFG914 -> CFG880/883/687) plus
CFG921's obs_struct / fact operators extracted by AST; CFG874's source up to its main block exec'd read-only; committed JSON of
CFG921, CFG874, CFG828.  Nothing downloaded; no other lane's file is written (open() is read-only during every re-execution).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, ast, json, math, time, resource, contextlib, builtins, warnings
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
KONLY = os.environ.get("CFG925_KONLY", "") == "1"; MUT = os.environ.get("CFG925_MUTATE", "") == "1"; assert not (KONLY and MUT)
SUF = "_K" if KONLY else ("_MUTATE" if MUT else "")
for _e in ("CFG921_MUTATE", "CFG921_KONLY", "CFG919_MUTATE", "CFG914_MUTATE", "CFG880_MUTATE", "CFG829_MUTATE", "CFG850_MUTATE",
           "CFG883_MUTATE", "CFG828_MUTATE", "CFG849_MUTATE", "CFG874_MUTATE", "CFG880_POSTHOC", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
_REAL_OPEN, _REAL_EXIT = builtins.open, sys.exit
def J(*p): return json.load(_REAL_OPEN(os.path.join(LANES, *p)))
RES = dict(lane="CFG925", criteria="661668f32", amendment_A1="cc07e00a3", mode=("K" if KONLY else ("MUTATE" if MUT else "main")), checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def jdef(o):
    if hasattr(o, "item"): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
def finish(code):
    RES["runtime_s"] = time.time() - T0; RES["peak_rss_mb"] = rss_mb()
    P(f"\n  done [{RES['runtime_s']:.0f} s, peak RSS {RES['peak_rss_mb']:.0f} MB].  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    json.dump(RES, _REAL_OPEN(os.path.join(HERE, f"cfg925_results{SUF}.json"), "w"), indent=1, default=jdef)
    _REAL_OPEN(os.path.join(HERE, f"cfg925{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    _REAL_EXIT(code)

FOOTS = ("canonical", "alt"); A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LN10 = math.log(10.0); DEX05 = 0.05 * LN10
G, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_e12 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-12))))
MW_M, M31_M = 6.0e10, 1.0e11; MW_MB, M31_MB = 8.0e10, 1.5e11                  # record host baryons (CFG820/838/839/883); brackets
A0MUT = 10.0                                                                 # MUTATE M2
P("CFG925  small reframings A: R1 law-Jeans estimator, R2 self-sourcing, R3 EFE sign (zero new constants)"
  + ("   [K-only]" if KONLY else ("   [MUTATE]" if MUT else "")))
P("  kappa = 1/2 FITTED; footings never pooled; criteria 661668f32")

# =====================================================================================================================  read-only re-execution
class _Exit(Exception): pass
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG925 refuses to write {file!r} from re-executed committed code")
    return _REAL_OPEN(file, mode, *a, **k)
def _trap_exit(code=0): raise _Exit(code)
builtins.open = _ro_open                                                     # whole run: only this lane's own writes use _REAL_OPEN
def ro_exec(src, path, ns):
    buf = io.StringIO(); sys.exit = _trap_exit
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(src, path, "exec"), ns)
    finally:
        sys.exit = _REAL_EXIT
    return buf.getvalue()

P("\n=== K-stage")
F921 = os.path.join(LANES, "CFG921_excess_selector_posits", "cfg921.py")
SRC921 = _REAL_OPEN(F921).read(); MARK = "# =====================================================================================================================  posit engines"
N921 = {"__file__": F921, "__name__": "cfg921_ro"}
try:
    _log921 = ro_exec(SRC921[:SRC921.index(MARK)], F921, N921); _ok921 = True
except (_Exit, PermissionError, Exception) as ex:                          # any failure of the re-executed K-stage = K2 FAIL
    _log921 = repr(ex); _ok921 = False
for _l in _log921.splitlines():
    if "[PASS]" in _l or "[FAIL]" in _l: P("    cfg921> " + _l.strip()[:190])
_tree = ast.parse(SRC921); _want = {"obs_struct", "fact_values", "obs_facts", "boot_ops", "ols_obs"}
_defs = [n for n in _tree.body if isinstance(n, ast.FunctionDef) and n.name in _want]
_vars = [n for n in _tree.body if isinstance(n, ast.Assign) and any(getattr(t, "id", None) in ("VARS", "BOOT") for t in n.targets)]
if _ok921:
    ro_exec(ast.unparse(ast.Module(body=_vars + _defs, type_ignores=[])), F921, N921)
c919 = N921.get("N919", {}).get("RES", {}).get("checks", {}) if _ok921 else {}
KOK = [check("K1 CFG919 exec'd read-only (via CFG921): all its checks pass, incl. CFG828 exact and CFG914's 9",
             _ok921 and len(c919) == 7 and all(v["ok"] for v in c919.values()), f"{sum(v['ok'] for v in c919.values())}/{len(c919)} CFG919 checks pass")]
KOK.append(check("K2 CFG921 prefix exec'd read-only: its K1-K4, K6 pass; CFG919 V0 cells reproduced; 5 helper functions extracted",
                 _ok921 and len(N921.get("KOK", [])) == 5 and all(N921["KOK"]) and len(_defs) == 5 and len(_vars) == 2,
                 f"{sum(N921.get('KOK', []))}/{len(N921.get('KOK', []))} CFG921 K-checks; helpers {sorted(d.name for d in _defs)}"))
if not all(KOK):
    P("  K1/K2 failed: lane stops (FROZEN_CRITERIA section 4)."); RES["class"] = None; finish(2)
DWD, CLD, GRID, lens_set = N921["DWD"], N921["CLD"], N921["GRID"], N921["lens_set"]
sp_gb, N919, N880 = N921["sp_gb"], N921["N919"], N921["N880"]
obs_struct, fact_values, obs_facts = N921["obs_struct"], N921["fact_values"], N921["obs_facts"]
nu_mono = N921["nu_mono"]

# K3: observed facts vs CFG921's committed JSON
R921 = J("CFG921_excess_selector_posits", "cfg921_results.json")["observed"]
STR, OBS = {}, {}
k3 = []
FK = ("F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8b")
for f in FOOTS:
    S = obs_struct(f, "V0"); STR[f] = S; v, se, _ = obs_facts(S, f); OBS[f] = (v, se)
    for k in FK:
        k3 += [abs(v[k] - R921[f][k]["obs"]), abs(se[k] - R921[f][k]["se"])]
KOK.append(check("K3 CFG921 observed facts F0-F8b (value and se) reproduced, both footings", max(k3) <= 1e-9,
                 f"max |diff| {max(k3):.1e}; canonical F0 {OBS['canonical'][0]['F0']:+.3f} ({OBS['canonical'][0]['F0'] / LN10:+.3f} dex), "
                 f"F1 {OBS['canonical'][0]['F1']:+.3f}, F5 {OBS['canonical'][0]['F5']:+.3f}"))

# =====================================================================================================================  per-dwarf inputs (K4)
LVD = N880["LVD"]; fnum = N880["fnum"]
def gas_profile(lHI):
    """own copy of CFG874/CFG880 extended-root HI disc: returns (M_gas total, R_s) in (Msun, pc), or None"""
    if lHI is None: return None
    Mg = 1.33 * 10 ** lHI; MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3
    fz = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [fz(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    return Mg, (max(roots) if roots else RHI / 2)
def gas_enc(gp, r_pc):
    if gp is None: return np.zeros_like(np.asarray(r_pc, float))
    Mg, Rs = gp; x = np.asarray(r_pc, float) / Rs; return Mg * (1 - (1 + x) * np.exp(-x))
DWX = {}; k4a, k4b = [], []
for f in FOOTS:
    D = DWD[f]; a0 = A0[f]; rows = []
    for i, nm in enumerate(D["names"]):
        L = LVD[nm]; gp = gas_profile(fnum(L.get("mass_HI"))); r12 = float(D["r12"][i])
        Mg12 = float(gas_enc(gp, r12)); k4b.append(abs(Mg12 - N880["gas_in"](fnum(L.get("mass_HI")), r12)) / max(1.0, Mg12))
        Ms = 2.0 * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gN = G * (Ms / 2 + Mg12) * MSUN / (r12 * PC) ** 2
        sW = math.sqrt(float(gN * nu_e(gN / a0)) * r12 * PC / 3) / 1e3
        k4a.append(abs(sW / float(N919["DWR"][f]["sig_law"][i]) - 1))
        rows.append(dict(name=nm, a_pc=0.75 * r12, r12=r12, Ms=Ms, gp=gp, gN=gN, sW=sW, so=float(N919["DWR"][f]["sigma"][i])))
    DWX[f] = rows
# CFG828 path: CFG827 SFH Ups, CFG824 sigma, no gas, nu_e12
R828 = J("CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json"); k4c = []; D828 = {}
SPLG = np.log10(np.asarray(N919["SP"]["gb"], float))
for f in FOOTS:
    a0 = A0[f]; ref = {r["name"]: r for r in R828[f"{f}|nu_e"]["rows"]}; rows = []
    for d in N919["DW828"]:
        nm = d["name"]; MV, rh = N919["LVD828"][nm]; Ms = N919["R27"][nm]["ups"] * 10 ** (0.4 * (4.83 - MV)); r12 = (4 / 3) * rh
        gN = G * (Ms / 2) * MSUN / (r12 * PC) ** 2; so = N919["R24"][nm]["so"]; sW2 = float(gN * nu_e12(gN / a0)) * r12 * PC / 3
        dl = math.log10(3 * (so * 1e3) ** 2 / (r12 * PC) / float(gN * nu_e12(gN / a0)))
        inr = int((np.abs(SPLG - math.log10(gN)) <= 0.15).sum()) >= 20
        rows.append(dict(name=nm, a_pc=rh, r12=r12, Ms=Ms, gp=None, gN=gN, sW=math.sqrt(sW2) / 1e3, so=so, delta=dl, inrange=inr))
        if nm in ref: k4c.append(abs(dl - ref[nm]["delta"]))
    oor = float(np.mean([r["delta"] for r in rows if not r["inrange"]]))
    k4c.append(abs(oor - R828[f"{f}|nu_e"]["out_of_range_mean_delta"])); D828[f] = rows
    k4c.append(0.0 if len([r for r in rows if r["name"] in ref]) == len(ref) else 1.0)
KOK.append(check("K4 Wolf path: CFG880 sigma_law (83 x 2), own gas copy = CFG880 gas_in at r12, CFG828 rows + out-of-range mean",
                 max(k4a) <= 1e-9 and max(k4b) <= 1e-12 and max(k4c) <= 1e-9,
                 f"max rel d sigma_law {max(k4a):.1e}; gas {max(k4b):.1e}; CFG828 {max(k4c):.1e} ({len(R828['canonical|nu_e']['rows'])} rows; "
                 f"out-of-range mean canonical {np.mean([r['delta'] for r in D828['canonical'] if not r['inrange']]):+.3f} dex); "
                 f"HI-bearing {sum(r['gp'] is not None for r in DWX['canonical'])}/83"))

# =====================================================================================================================  R1 Jeans engine (K5)
XG = np.unique(np.concatenate([np.geomspace(1e-5, 1e5, 20001), [0.1, 0.5, 1.0, 2.0]]))
LXG = np.log(XG); NUS = (1 + XG ** 2) ** -2.5                                # Plummer tracer, unnormalised (int x^2 nu dx = 1/3)
def rev_cumint(fx):
    """int_x^inf f dx' on XG by trapezoid in ln x (f x d ln x)"""
    h = fx * XG; seg = 0.5 * (h[1:] + h[:-1]) * np.diff(LXG); return np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
def trapz_ln(fx): h = fx * XG; return float(np.sum(0.5 * (h[1:] + h[:-1]) * np.diff(LXG)))
def jeans_ap(gx, beta, Xap):
    """luminosity-weighted <sigma_los^2> inside projected aperture Xap (units: [g]*a) for tracer NUS in field gx(XG);
    beta: float (constant) or ('OM', x_a)."""
    q = NUS * gx
    if isinstance(beta, tuple):
        xa = beta[1]; K = XG ** 2 + xa ** 2; b = XG ** 2 / K
    else:
        K = XG ** (2 * beta); b = np.full(XG.shape, float(beta))
    p = rev_cumint(K * q) / K
    if math.isinf(Xap):
        w = 1 - 2 * b / 3; lw = np.ones_like(XG)
    else:
        s2 = np.clip((Xap / XG) ** 2, 0, 1); c = np.where(XG > Xap, np.sqrt(1 - s2), 0.0)
        w = (1 - c) - b * ((1 - c) - (1 - c ** 3) / 3); lw = 1 - c
    return trapz_ln(XG ** 2 * p * w) / trapz_ln(XG ** 2 * NUS * lw)
mP = XG ** 3 / (1 + XG ** 2) ** 1.5
k5 = {}
yN = mP / XG ** 2                                                            # Newtonian Plummer, Y = GM/(a^2 a0) = 1
for X in (0.1, 0.5, 1.0, 2.0, math.inf):
    an = (math.pi / 32) * (1.0 if math.isinf(X) else (1 - (1 + X * X) ** -1.5) / (1 - 1 / (1 + X * X)))
    k5[f"Newton iso <s2>(<{X})"] = abs(jeans_ap(yN, 0.0, X) / an - 1)
for X in (0.5, 1.0, 2.0):
    s2 = np.clip((X / XG) ** 2, 0, 1); c = np.where(XG > X, np.sqrt(1 - s2), 0.0)
    k5[f"L(<{X})"] = abs(trapz_ln(XG ** 2 * NUS * (1 - c)) / ((1 / 3) * X * X / (1 + X * X)) - 1)
vir = trapz_ln(XG ** 3 * NUS * yN) / 3 / trapz_ln(XG ** 2 * NUS)
for bt in (0.5, ("OM", 1.0), 0.9):
    k5[f"virial beta={bt}"] = abs(jeans_ap(yN, bt, math.inf) / vir - 1)
for Y in (1e-3, 1.0):
    k5[f"deep-law global Y={Y}"] = abs(jeans_ap(np.sqrt(Y * yN), 0.0, math.inf) / ((2 / 9) * math.sqrt(Y)) - 1)
K5MAX = max(k5.values()); RES["K5"] = k5
KOK.append(check("K5 Jeans solver: Newton Plummer aperture <s2> (X 0.1..inf), L(<X), virial identity (beta 0.5/OM/0.9), deep-law global",
                 K5MAX < 1e-2, f"max rel error {K5MAX:.1e} (task bar 1e-2; target 1e-3); Newton <s2>(<1) "
                 f"{jeans_ap(yN, 0.0, 1.0):.6f} vs analytic {(math.pi / 16) * (1 - 2 ** -1.5):.6f} GM/a"))

def dwarf_gfield(row, a0):
    """g(XG)/a0 for one dwarf: law on Plummer stars + gas; returns (g/a0 array, a in m)"""
    a = row["a_pc"]; r_pc = XG * a; M = row["Ms"] * mP + gas_enc(row["gp"], r_pc)
    y = G * M * MSUN / (r_pc * PC) ** 2 / a0; return y * nu_e(y), a * PC
def sigma_J(row, a0, beta, Xap):
    gy, am = dwarf_gfield(row, a0); return math.sqrt(jeans_ap(gy, beta, Xap) * a0 * am) / 1e3

# ---- K5x (ADDED POST-FREEZE, after the first main run; diagnostic only, NOT a gate): the anisotropic aperture weight checked against
# a direct line-of-sight projection Sigma sigma_p^2(R) = 2 int_0^inf (1 - beta(r) R^2/r^2) p(r) dz, r = sqrt(R^2 + z^2), then the aperture
# integral over R.  K5 checked the weight only at R_ap = inf (virial) and for beta = 0 (analytic); R1's corner classes use beta != 0 at R_e.
def proj_aperture(gx, beta, Xap):
    q = NUS * gx
    if isinstance(beta, tuple):
        K = XG ** 2 + beta[1] ** 2; bfun = lambda r: r ** 2 / (r ** 2 + beta[1] ** 2)
    else:
        K = XG ** (2 * beta); bfun = lambda r: np.full(np.shape(r), float(beta))
    p = np.maximum(rev_cumint(K * q) / K, 1e-300); lp = np.log(p)
    Rg = np.concatenate([np.geomspace(1e-4, Xap, 400)]); zg = np.concatenate([[0.0], np.geomspace(1e-6, 1e4, 3000)])
    RR, ZZ = np.meshgrid(Rg, zg, indexing="ij"); rr = np.sqrt(RR ** 2 + ZZ ** 2)
    pr = np.exp(np.interp(np.log(rr), LXG, lp)); nr = (1 + rr ** 2) ** -2.5
    Ss = 2 * np.trapz((1 - bfun(rr) * RR ** 2 / rr ** 2) * pr, zg, axis=1); Sn = 2 * np.trapz(nr, zg, axis=1)
    wR = Rg; return float(np.trapz(Ss * wR, Rg) / np.trapz(Sn * wR, Rg))
k5x = {}
for bt, lab in ((0.0, "0"), (0.5, "0.5"), (("OM", 1.0), "OM r_a=a")):
    k5x[f"Newton Plummer beta {lab}, R_e"] = abs(proj_aperture(yN, bt, 1.0) / jeans_ap(yN, bt, 1.0) - 1)
_gx0, _ = dwarf_gfield(DWX["canonical"][0], A0["canonical"])
for bt, lab in ((0.5, "0.5"), (("OM", 1.0), "OM r_a=a")):
    k5x[f"{DWX['canonical'][0]['name']} law field beta {lab}, R_e"] = abs(proj_aperture(_gx0, bt, 1.0) / jeans_ap(_gx0, bt, 1.0) - 1)
RES["K5x_posthoc_diagnostic"] = k5x
P(f"  [{'OK  ' if max(k5x.values()) < 1e-3 else 'WARN'}] K5x (post-freeze diagnostic, not a gate): anisotropic R_e aperture weight vs direct LOS projection: "
  f"max rel diff {max(k5x.values()):.1e} over {len(k5x)} cases (Newton Plummer beta 0 / 0.5 / OM; {DWX['canonical'][0]['name']} law field beta 0.5 / OM)")

# =====================================================================================================================  R2 solvers (K6)
def bisect(F, lo, hi, n=200):
    lo, hi = np.array(lo, float), np.array(hi, float)
    for _ in range(n):
        m = np.sqrt(lo * hi); pos = F(m) > 0; hi = np.where(pos, m, hi); lo = np.where(pos, lo, m)
    return np.sqrt(lo * hi)
def yfloor(nu):
    F = lambda y: 2.0 - nu(y)                                                # >0 above the floor
    return float(bisect(F, np.array([1e-8]), np.array([1e3]))[0])
YF = {"nu_e": yfloor(nu_e), "nu_mono": yfloor(nu_mono)}
def r2A(yb, nu, yf):
    yb = np.asarray(yb, float); return bisect(lambda y: y * (2 - nu(y)) - yb, np.full(yb.shape, yf * (1 + 1e-12)), 3 * yb + 3)
def r2B(yb, nu):
    yb = np.asarray(yb, float); return bisect(lambda y: y / nu(y) - yb, yb * (1 - 1e-12), yb * nu(yb) * (1 + 1e-12))
def pe_R2(yb, nu, form):
    yl = yb * nu(yb); y = r2A(yb, nu, YF["nu_e" if nu is nu_e else "nu_mono"]) if form == "A" else r2B(yb, nu); return np.log(y / yl), y
ytest = np.geomspace(1e-6, 1e3, 400); k6 = {}
for nm_, nu in (("nu_e", nu_e), ("nu_mono", nu_mono)):
    yA = r2A(ytest, nu, YF[nm_]); yB = r2B(ytest, nu)
    k6[f"{nm_} R2-A rel residual [info]"] = float(np.max(np.abs(yA * (2 - nu(yA)) / ytest - 1)))
    k6[f"{nm_} R2-B rel residual [info]"] = float(np.max(np.abs(yB / nu(yB) / ytest - 1)))
    EPS = float(np.finfo(float).eps)                                          # A1: |h(y) - y_b| <= 1e-10 y_b + 16 eps y
    k6[f"{nm_} R2-A A1 residual ratio"] = float(np.max(np.abs(yA * (2 - nu(yA)) - ytest) / (1e-10 * ytest + 16 * EPS * yA)))
    k6[f"{nm_} R2-B A1 residual ratio"] = float(np.max(np.abs(yB / nu(yB) - ytest) / (1e-10 * ytest + 16 * EPS * yB)))
    hh = ytest[ytest > YF[nm_]]; hv = hh * (2 - nu(hh)); k6[f"{nm_} h(y) monotone above floor"] = 0.0 if np.all(np.diff(hv) > 0) else 1.0
    k6[f"{nm_} nu decreasing, >=1"] = 0.0 if (np.all(np.diff(nu(ytest)) <= 0) and np.all(nu(ytest) >= 1)) else 1.0
    k6[f"{nm_} Newtonian limit y_b=100 (A,B)" + ("" if nm_ == "nu_e" else " [info]")] = float(max(abs(pe_R2(np.array([100.0]), nu, "A")[0][0]), abs(pe_R2(np.array([100.0]), nu, "B")[0][0])))
k6["nu_mono(100) - 1 [info]"] = float(nu_mono(np.array([100.0]))[0] - 1)
yg = np.geomspace(1e-6, 1e3, 2000); k6["R2-0 nu_e - 1 > 0 on grid"] = 0.0 if np.all(nu_e(yg) - 1 > 0) else 1.0
seq = []
for yb in (1e-3, 0.1, 10.0):
    y = float(yb * nu_e(yb)); s = [y]
    for _ in range(200): y = float(y * nu_e(y)); s.append(y)
    seq.append(s)
k6["R2-0 iteration monotone increasing, no fixed point"] = 0.0 if all(np.all(np.diff(s) > 0) for s in seq) else 1.0
RES["K6"] = k6; RES["R2_floor"] = YF; RES["R2_0_iter_end"] = [s[-1] for s in seq]
KOK.append(check("K6 R2 solvers: residuals, monotone h above floor, Newtonian limit, R2-0 ill-posed (nu > 1, runaway iteration)",
                 max(v for k, v in k6.items() if "A1 residual ratio" in k) <= 1.0 and all(v == 0 for k, v in k6.items() if "monotone" in k or "decreasing" in k or "R2-0" in k)
                 and max(v for k, v in k6.items() if "Newtonian" in k and "[info]" not in k) <= 1e-6,
                 f"A1 residual ratio max {max(v for k, v in k6.items() if 'A1 residual ratio' in k):.2f} (<= 1; rel residual max "
                 f"{max(v for k, v in k6.items() if 'rel residual' in k):.1e}); data min y_b {min(float(np.min(np.asarray(DWD[ff]['gb']) / A0[ff])) for ff in FOOTS):.1e}; Newtonian limit nu_e {k6['nu_e Newtonian limit y_b=100 (A,B)']:.1e} (nu_mono, info: {k6['nu_mono Newtonian limit y_b=100 (A,B) [info]']:.1e}, nu_mono(100)-1 {k6['nu_mono(100) - 1 [info]']:.1e}); "
                 f"floors y_f nu_e {YF['nu_e']:.5f} ((ln2)^2 = {math.log(2) ** 2:.5f}), nu_mono {YF['nu_mono']:.5f}; R2-0 iterates after 200 steps "
                 f"{', '.join(f'{s[-1]:.3g}' for s in seq)} a0 (still rising)"))

# =====================================================================================================================  R3 EFE (K7)
DSEP = fnum(LVD["M 32"]["distance_gc"])
def g_ext(nm, Mmw, Mm31):
    L = LVD[nm]; dgc, dm = fnum(L.get("distance_gc")), fnum(L.get("distance_m31"))
    if dgc is None or dm is None:                                            # fallback: host point mass at distance_host (counted in K7)
        dh = fnum(L.get("distance_host")); Mh = {"mw": Mmw, "m_031": Mm31}.get(L.get("host") or "")
        return ((G * Mh * MSUN / (dh * KPC) ** 2) if (dh and Mh) else 0.0), (dh if dh else math.inf), False
    g1 = G * Mmw * MSUN / (dgc * KPC) ** 2; g2 = G * Mm31 * MSUN / (dm * KPC) ** 2
    ct = (dgc ** 2 + dm ** 2 - DSEP ** 2) / (2 * dgc * dm); clip = abs(ct) > 1; ct = max(-1.0, min(1.0, ct))
    return math.sqrt(max(g1 * g1 + g2 * g2 + 2 * g1 * g2 * ct, 0.0)), min(dgc, dm), clip
def efe_ratio(gi, ge, a0, form):
    """g_EFE / g_iso at internal Newtonian gi, external Newtonian ge"""
    gi, ge = np.asarray(gi, float), np.asarray(ge, float); iso = gi * nu_e(gi / a0)
    if form == "E0": return np.ones_like(gi)
    if form == "E1": return gi * nu_e((gi + ge) / a0) / iso
    if form == "E2": return ((gi + ge) * nu_e((gi + ge) / a0) - ge * nu_e(ge / a0)) / iso
    raise ValueError(form)
k7 = {}
_miss = [nm for nm in DWD["canonical"]["names"] if fnum(LVD[nm].get("distance_gc")) is None or fnum(LVD[nm].get("distance_m31")) is None]
for f in FOOTS:
    gi = np.array([r["gN"] for r in DWX[f]])
    k7[f"{f} g_e->0 (E1,E2)"] = float(max(np.max(np.abs(efe_ratio(gi, 0 * gi, A0[f], fm) - 1)) for fm in ("E1", "E2")))
ye = 0.05; a0t = 1.0; gi_t = np.array([1e-8 * ye]); nue = float(nu_e(ye)); dl = 1e-6
Le = float((math.log(nu_e(ye * (1 + dl))) - math.log(nu_e(ye * (1 - dl)))) / (math.log(1 + dl) - math.log(1 - dl)))
b1 = float(efe_ratio(gi_t, np.array([ye]), a0t, "E1")[0] * nu_e(gi_t / a0t)[0]); b2 = float(efe_ratio(gi_t, np.array([ye]), a0t, "E2")[0] * nu_e(gi_t / a0t)[0])
bq = nue * (1 + Le / 3)
k7["EFE limit E1 -> nu_e"] = abs(b1 / nue - 1); k7["EFE limit E2 -> nu_e(1+L_e)"] = abs(b2 / (nue * (1 + Le)) - 1)
k7["bracket E2 <= QUMOND <= E1"] = 0.0 if (b2 <= bq <= b1) else 1.0
SRC874 = os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874.py"); s874 = _REAL_OPEN(SRC874).read()
N874 = {"__file__": SRC874, "__name__": "cfg874_ro"}; ro_exec(s874[:s874.index('P("CFG874  all isolated')], SRC874, N874)
R874 = J("CFG874_isolated_dwarfs_pooled", "cfg874_results.json")
def run874(f, form, Mmw, Mm31, a0=None):
    a0 = A0[f] if a0 is None else a0; rows = N874["build"](f, gas="disc")
    for r in rows:
        ge, _, _ = g_ext(r["name"], Mmw, Mm31); gi = 10 ** r["lg"]
        r["D"] = r["D"] - math.log10(float(efe_ratio(np.array([gi]), np.array([ge]), a0, form)[0]))
    return N874["analyse"](rows)
for f in FOOTS:
    r0 = run874(f, "E0", MW_M, M31_M); ref = R874[f]["primary"]
    k7[f"{f} CFG874 primary at E0"] = max(abs(r0[k] - ref[k]) for k in ("c", "se_c", "E", "se_E")) + (0.0 if r0["cls"] == ref["cls"] else 1.0)
RES["K7"] = k7
KOK.append(check("K7 R3: g_e -> 0 = isolated law; EFE-dominated limits; E2 <= exact linear QUMOND <= E1; CFG874 primary reproduced at E0",
                 max(k7.values()) <= 1e-6 and all(k7[f"{f} CFG874 primary at E0"] <= 1e-9 for f in FOOTS),
                 f"max {max(k7.values()):.1e}; at y_e 0.05: E1 {b1:.4f}, exact-linear QUMOND {bq:.4f}, E2 {b2:.4f} (nu_e {nue:.4f}, L_e {Le:+.4f}); "
                 f"MW-M31 separation (LVD M 32 distance_gc) {DSEP:.1f} kpc; dwarfs without distance_gc/m31: {len(_miss)}"))
K_ALL = all(KOK)
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
RES["K_all"] = K_ALL
if not K_ALL:
    P("  A K-test failed: per FROZEN_CRITERIA section 4 the lane stops; no class is reported."); RES["class"] = None; finish(2)
if KONLY:
    P("  CFG925_KONLY=1: K-stage only (no reframing number or class printed)."); finish(0)

# =====================================================================================================================  residual-fact machinery
def zero_pe(f, S):
    return dict(DW=np.zeros(len(DWD[f]["names"])), SP=np.zeros(len(sp_gb)), LD=np.zeros(len(S["lens"]["LD"]["gbs"])),
                LS=np.zeros(len(S["lens"]["LS"]["gbs"])), CL=np.zeros(CLD[f]["gb"].shape))
def residual_facts(f, pe):
    S = STR[f]; D = CLD[f]; pred = {}
    pred["DW"] = np.array([np.mean(pe["DW"][m]) for m in S["dwcell"]])
    for cl in ("SS", "SL"):
        pred[cl] = np.array([np.mean(np.bincount(inv, pe["SP"][sel]) / np.bincount(inv)) for sel, inv, n in S["sparc"][cl]])
    for cl in ("LD", "LS"):
        Ls = S["lens"][cl]; pred[cl] = np.array([math.log(float(w @ (Ls["gl"][Sx] * np.exp(pe[cl][Sx])))) for Sx, w in Ls["W"]])
    WP = D["W"] * D["Pm"]; pred["CL"] = np.array([math.log(float((WP[m] * np.exp(pe["CL"][m])).sum() / WP[m].sum())) for m in S["clus"]])
    cells = {cl: S["E"][S["ops"][cl]["ix"]] - pred[cl] for cl in pred}
    return fact_values(S, cells, DWD[f]["E"] - pe["DW"], f)
def grade(f, res):
    v, se = OBS[f]; d = {k: abs(res[k]) - abs(v[k]) for k in ("F0", "F1", "F5")}
    dam = [k for k in ("F2", "F3", "F4") if abs(res[k]) >= abs(v[k]) + DEX05 and abs(res[k]) >= 2 * se[k]]
    split = ("F2" in dam) or (res["F1"] - res["F2"] <= -2 * math.hypot(se["F1"], se["F2"]))
    if abs(res["F0"]) <= 0.5 * abs(v["F0"]) and not dam and not split and d["F1"] < DEX05 and d["F5"] < DEX05: cls = "RESOLVES"
    elif dam or split or any(x >= DEX05 for x in d.values()): cls = "WORSENS"
    elif any(x <= -DEX05 for x in d.values()): cls = "PARTIAL"
    else: cls = "NO EFFECT"
    return dict(cls=cls, dabs_dex={k: x / LN10 for k, x in d.items()}, damage=dam, split_broken=bool(split),
                res_dex={k: res[k] / LN10 for k in ("F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8b")},
                shift_dex={k: (res[k] - v[k]) / LN10 for k in ("F0", "F1", "F2", "F3", "F4", "F5")})
def fmt_g(g):
    r = g["res_dex"]; s = g["shift_dex"]
    return (f"{g['cls']:9s} | F0 DW {r['F0']:+.3f} ({s['F0']:+.3f})  F1 red {r['F1']:+.3f} ({s['F1']:+.3f})  F5 CL {r['F5']:+.3f} ({s['F5']:+.3f}) | "
            f"F2 blue {r['F2']:+.3f} ({s['F2']:+.3f})  F3 SS {r['F3']:+.3f} ({s['F3']:+.3f})  F4 SL {r['F4']:+.3f} ({s['F4']:+.3f}) dex"
            + (f"  DAMAGE {g['damage']}" if g["damage"] else "") + ("  SPLIT BROKEN" if g["split_broken"] else ""))
LOWG = {f: np.asarray(DWD[f]["lg"]) < -12.0 for f in FOOTS}

# ---- R1
BETAS = {"J0": 0.0, "J1": ("OM", 1.0), "J2": 0.5}; APS = {"A1": 1.0, "A2": math.inf}
CORNERS = [("J0", "A1"), ("J1", "A1"), ("J2", "A1"), ("J0", "A2")]
def r1_run(f, beta, Xap, a0=None):
    a0 = A0[f] if a0 is None else a0; rows = DWX[f]
    sJ = np.array([sigma_J(r, a0, beta, Xap) for r in rows])
    sW = np.array([r["sW"] for r in rows]) if a0 == A0[f] else np.array([math.sqrt(float(r["gN"] * nu_e(r["gN"] / a0)) * r["r12"] * PC / 3) / 1e3 for r in rows])
    so = np.array([r["so"] for r in rows]); pe = zero_pe(f, STR[f]); pe["DW"] = 2 * np.log(sJ / sW)
    EJ = 2 * np.log(so / sJ); EW = 2 * np.log(so / sW)
    return sJ, sW, EJ, EW, pe
def r1_828(f, beta, Xap):
    rows = D828[f]; sJ = np.array([sigma_J(r, A0[f], beta, Xap) for r in rows]); so = np.array([r["so"] for r in rows])
    dJ = 2 * np.log10(so / sJ); oor = np.array([not r["inrange"] for r in rows])
    return float(np.mean([r["delta"] for r in rows if not r["inrange"]])), float(np.mean(dJ[oor])), int(oor.sum())

# ---- R2
def r2_pe(f, form, a0=None):
    a0 = A0[f] if a0 is None else a0; S = STR[f]; pe = zero_pe(f, S); D = CLD[f]
    pe["DW"] = pe_R2(np.asarray(DWD[f]["gb"]) / a0, nu_e, form)[0]
    pe["SP"] = pe_R2(np.asarray(sp_gb) / a0, nu_e, form)[0]
    for cl in ("LD", "LS"): pe[cl] = pe_R2(np.asarray(S["lens"][cl]["gbs"]) / a0, nu_e, form)[0]
    a0c = D["a0"] * (a0 / A0[f]); pe["CL"] = pe_R2(D["gb"] / a0c, nu_mono, form)[0]
    return pe
def r2S(f):
    """diagnostic: surplus needed under Newtonian addition (class A) vs self-sourcing (law(g_b + g_x)), dwarfs with an excess"""
    a0 = A0[f]; out = []
    for r in DWX[f]:
        gobs = 3 * (r["so"] * 1e3) ** 2 / (r["r12"] * PC); gb = r["gN"]; gl = gb * float(nu_e(gb / a0))
        if gobs <= gl: continue
        yinv = float(bisect(lambda y: y * nu_e(y) - gobs / a0, np.array([1e-12]), np.array([gobs / a0 + 1]))[0])
        out.append((gobs - gl) / (yinv * a0 - gb))
    return float(np.median(out)), float(np.percentile(out, 16)), float(np.percentile(out, 84)), len(out)

# ---- R3
def r3_shift(f, form, Mmw, Mm31, a0=None):
    a0 = A0[f] if a0 is None else a0; gi = np.array([r["gN"] for r in DWX[f]])
    ge = np.array([g_ext(r["name"], Mmw, Mm31)[0] for r in DWX[f]]); dmin = np.array([g_ext(r["name"], Mmw, Mm31)[1] for r in DWX[f]])
    pe = zero_pe(f, STR[f]); pe["DW"] = np.log(efe_ratio(gi, ge, a0, form)); return pe, dmin, ge

# =====================================================================================================================  MUTATE
if MUT:
    P("\n=== MUTATE (teeth must bite: |move| >= 0.02 dex)")
    T = {}
    for f in FOOTS:
        a0 = A0[f]; S = STR[f]
        _, _, _, _, pe0 = r1_run(f, 0.0, 1.0); F0J = residual_facts(f, pe0)["F0"]
        _, _, _, _, pe9 = r1_run(f, 0.9, 1.0); F0J9 = residual_facts(f, pe9)["F0"]
        T[f"{f} M1 R1 beta 0.9 vs 0"] = (F0J9 - F0J) / LN10
        sJ, sW, EJ, EW, _ = r1_run(f, 0.0, 1.0, a0=a0 * A0MUT)
        cE = np.array([np.mean(EJ[m]) for m in S["dwcell"]]); F0J10 = float(S["ops"]["DW"]["w"] @ cE)
        T[f"{f} M2 R1 F0_J a0x10 vs main"] = (F0J10 - F0J) / LN10
        dA = residual_facts(f, r2_pe(f, "A"))["F0"] - OBS[f][0]["F0"]; dA10 = residual_facts(f, r2_pe(f, "A", a0=a0 * A0MUT))["F0"] - OBS[f][0]["F0"]
        T[f"{f} M2 R2-A dF0 a0x10 vs main"] = (dA10 - dA) / LN10
        d1 = residual_facts(f, r3_shift(f, "E1", MW_M, M31_M)[0])["F0"]; d10 = residual_facts(f, r3_shift(f, "E1", MW_M, M31_M, a0=a0 * A0MUT)[0])["F0"]
        T[f"{f} M2 R3-E1 dF0 a0x10 vs main"] = (d10 - d1) / LN10
        pe1, dmin, _ = r3_shift(f, "E1", MW_M, M31_M); pe10, _, _ = r3_shift(f, "E1", 10 * MW_M, 10 * M31_M); sat = dmin < 300
        T[f"{f} M3 R3 host x10 sat mean shift"] = float(np.mean(-pe10["DW"][sat]) - np.mean(-pe1["DW"][sat])) / LN10
    bites = {k: abs(v) >= 0.02 for k, v in T.items()}
    for k, v in T.items(): P(f"  {k:38s} move {v:+.3f} dex -> {'BITES' if bites[k] else 'TOOTHLESS'}")
    RES["mutate"] = dict(moves_dex=T, bites=bites, all_bite=all(bites.values()))
    P(f"  MUTATE: {'ALL TEETH BITE (exit 1 by design)' if all(bites.values()) else 'TOOTHLESS tooth present (exit 3)'}")
    finish(1 if all(bites.values()) else 3)

# =====================================================================================================================  MAIN
RES["observed_dex"] = {f: {k: OBS[f][0][k] / LN10 for k in FK} for f in FOOTS}
RES["observed_se_dex"] = {f: {k: OBS[f][1][k] / LN10 for k in FK} for f in FOOTS}
CLS = {}
P("\n=== R1 estimator: law-Jeans sigma_los (Plummer stars + gas, law potential) instead of Wolf g(r12) = 3 sigma^2/r12")
RES["R1"] = {}
for f in FOOTS:
    R = RES["R1"][f] = {"corners": {}}
    for jb, ap in CORNERS:
        sJ, sW, EJ, EW, pe = r1_run(f, BETAS[jb], APS[ap]); res = residual_facts(f, pe); g = grade(f, res)
        o828 = r1_828(f, BETAS[jb], APS[ap])
        rec = dict(grade=g, ratio_sJ_sW=dict(median=float(np.median(sJ / sW)), p16=float(np.percentile(sJ / sW, 16)), p84=float(np.percentile(sJ / sW, 84)),
                                             min=float(np.min(sJ / sW)), max=float(np.max(sJ / sW))),
                   F0_wolf_dex=OBS[f][0]["F0"] / LN10, F0_jeans_dex=res["F0"] / LN10,
                   lowg_mean_wolf_dex=float(np.mean(EW[LOWG[f]])) / LN10, lowg_mean_jeans_dex=float(np.mean(EJ[LOWG[f]])) / LN10, n_lowg=int(LOWG[f].sum()),
                   cfg828_oor_wolf_dex=o828[0], cfg828_oor_jeans_dex=o828[1], cfg828_n_oor=o828[2])
        R["corners"][f"{jb}|{ap}"] = rec
        P(f"  [{f} {jb} {ap}] sigma_J/sigma_W median {rec['ratio_sJ_sW']['median']:.4f} ({rec['ratio_sJ_sW']['min']:.3f}-{rec['ratio_sJ_sW']['max']:.3f}); "
          f"F0 Wolf {rec['F0_wolf_dex']:+.3f} -> Jeans {rec['F0_jeans_dex']:+.3f} dex; g_bar<1e-12 mean ({rec['n_lowg']}) {rec['lowg_mean_wolf_dex']:+.3f} -> "
          f"{rec['lowg_mean_jeans_dex']:+.3f}; CFG828 oor ({o828[2]}) {o828[0]:+.3f} -> {o828[1]:+.3f}  => {g['cls']}")
    prim = R["corners"]["J0|A1"]["grade"]["cls"]; allc = {c["grade"]["cls"] for c in R["corners"].values()}
    R["class"] = prim; R["robust"] = "ROBUST" if allc == {prim} else "BRACKET-DEPENDENT"; R["corner_classes"] = sorted(allc); CLS[f"R1|{f}"] = prim
    P(f"  [{f}] R1 CLASS {prim} ({R['robust']}; corner classes {sorted(allc)})")

P("\n=== R2 self-sourcing: cold energy's own mass in the law's argument")
P(f"  R2-0 literal (g = nu(g/a0) g): ILL-POSED - nu_e > 1 for all finite y; iterates rise without a fixed point (K6). No class.")
RES["R2"] = {"R2-0": "ILL-POSED", "floor_y": YF}
for f in FOOTS:
    RES["R2"][f] = {}
    for form, lab in (("A", "R2-A primary  g_b = g (2 - nu(g/a0))"), ("B", "R2-B second   g = nu(g/a0) g_b")):
        pe = r2_pe(f, form); res = residual_facts(f, pe); g = grade(f, res)
        RES["R2"][f][form] = dict(grade=g, pe_DW_median_dex=float(np.median(pe["DW"])) / LN10, pe_SP_median_dex=float(np.median(pe["SP"])) / LN10,
                                  pe_LD_range_dex=[float(pe["LD"].min()) / LN10, float(pe["LD"].max()) / LN10],
                                  pe_LS_range_dex=[float(pe["LS"].min()) / LN10, float(pe["LS"].max()) / LN10],
                                  pe_CL_range_dex=[float(pe["CL"].min()) / LN10, float(pe["CL"].max()) / LN10])
        P(f"  [{f} {lab}]  {fmt_g(g)}")
        P(f"      median shift dwarfs {RES['R2'][f][form]['pe_DW_median_dex']:+.3f} dex, SPARC points {RES['R2'][f][form]['pe_SP_median_dex']:+.3f}, "
          f"blue bins {RES['R2'][f][form]['pe_LD_range_dex'][0]:+.2f}..{RES['R2'][f][form]['pe_LD_range_dex'][1]:+.2f}, "
          f"red bins {RES['R2'][f][form]['pe_LS_range_dex'][0]:+.2f}..{RES['R2'][f][form]['pe_LS_range_dex'][1]:+.2f}, "
          f"clusters {RES['R2'][f][form]['pe_CL_range_dex'][0]:+.2f}..{RES['R2'][f][form]['pe_CL_range_dex'][1]:+.2f}")
    CLS[f"R2|{f}"] = RES["R2"][f]["A"]["grade"]["cls"]; CLS[f"R2B|{f}"] = RES["R2"][f]["B"]["grade"]["cls"]
    m, lo, hi, n = r2S(f); RES["R2"][f]["R2-S"] = dict(median_ratio=m, p16=lo, p84=hi, n=n)
    P(f"  [{f}] R2 CLASS {CLS[f'R2|{f}']} (R2-B {CLS[f'R2B|{f}']}).  Diagnostic R2-S (no class): surplus needed, Newtonian / self-sourced, "
      f"median {m:.2f} (16-84% {lo:.2f}-{hi:.2f}, {n} dwarfs with an excess)")

P("\n=== R3 EFE sign: E0 none (baseline), E1 record's algebraic nu((gNi + gNe)/a0), E2 1-D QUMOND subtraction")
RES["R3"] = {}
for f in FOOTS:
    R = RES["R3"][f] = {"corners": {}}
    for form in ("E0", "E1", "E2"):
        for hm, (Mmw, Mm31) in (("nom", (MW_M, M31_M)), ("brk", (MW_MB, M31_MB))):
            if form == "E0" and hm == "brk": continue
            pe, dmin, ge = r3_shift(f, form, Mmw, Mm31); res = residual_facts(f, pe); g = grade(f, res); sat = dmin < 300
            dE = -pe["DW"] / LN10; r874 = run874(f, form, Mmw, Mm31)
            rec = dict(grade=g, sat_n=int(sat.sum()), field_n=int((~sat).sum()), sat_mean_shift_dex=float(np.mean(dE[sat])), sat_median_shift_dex=float(np.median(dE[sat])),
                       sat_max_shift_dex=float(np.max(dE[sat])), field_mean_shift_dex=float(np.mean(dE[~sat])) if (~sat).any() else None,
                       sat_mean_E_dex=float(np.mean((DWD[f]["E"] - pe["DW"])[sat])) / LN10, field_mean_E_dex=float(np.mean((DWD[f]["E"] - pe["DW"])[~sat])) / LN10,
                       cfg874=dict(c=r874["c"], se_c=r874["se_c"], E=r874["E"], se_E=r874["se_E"], cls=r874["cls"], N_I=r874["N_I"], N_S=r874["N_S"]))
            if form != "E0":
                top = np.argsort(-dE)[:5]; rec["largest"] = [(DWD[f]["names"][i], float(dE[i]), float(dmin[i])) for i in top]
            R["corners"][f"{form}|{hm}"] = rec
            P(f"  [{f} {form} {hm}] satellites ({rec['sat_n']}) mean EFE shift {rec['sat_mean_shift_dex']:+.3f} dex (median {rec['sat_median_shift_dex']:+.3f}, "
              f"max {rec['sat_max_shift_dex']:+.3f}); field ({rec['field_n']}) {(rec['field_mean_shift_dex'] or 0.0):+.3f}; mean E sat {rec['sat_mean_E_dex']:+.3f} / field "
              f"{rec['field_mean_E_dex']:+.3f} dex")
            P(f"      F0 {g['res_dex']['F0']:+.3f} ({g['shift_dex']['F0']:+.3f}) => {g['cls']};  CFG874: c {r874['c']:+.3f} +- {r874['se_c']:.3f}, "
              f"E {r874['E']:+.3f} +- {r874['se_E']:.3f} -> {r874['cls']}")
    prim = R["corners"]["E1|nom"]["grade"]["cls"]; allc = {R["corners"][k]["grade"]["cls"] for k in R["corners"] if not k.startswith("E0")}
    c0 = R["corners"]["E0|nom"]["cfg874"]; chg = {k: (R["corners"][k]["cfg874"]["cls"] != c0["cls"]) or abs(R["corners"][k]["cfg874"]["c"] - c0["c"]) >= 0.05
                                                   for k in R["corners"] if not k.startswith("E0")}
    R["class_include"] = prim; R["robust"] = "ROBUST" if allc == {prim} else "BRACKET-DEPENDENT"; R["class_remove"] = "NO EFFECT (baseline is EFE-free; dF0 = 0)"
    R["sat_field_changes"] = chg; CLS[f"R3|{f}"] = prim
    P(f"  [{f}] R3 CLASS include-EFE {prim} ({R['robust']}); remove-EFE NO EFFECT (identical to the baseline); satellite-field comparison changed: "
      f"{ {k: v for k, v in chg.items()} }")

RES["classes"] = CLS
P("\n=== CLASSES (per footing; never pooled)")
for k, v in CLS.items(): P(f"  {k:14s} {v}")
finish(0)
