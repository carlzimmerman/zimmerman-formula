"""CFG926 -- three small reframings of the pressure-supported excess (B):
  R4 fossil a0 (pressure-supported systems keep a0(z_f); rotators re-settle), R5 IMF alpha-sigma for old spheroids,
  R6 the B21 lensing estimator (4 G DeltaSigma, point-mass g_bar) for round vs flat lenses.
Criteria: FROZEN_CRITERIA.md (48a7a31ae, committed alone before this script) + AMENDMENT_A1.md (post-hoc clarifications).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg926.py         -> cfg926.out, cfg926_results.json
     CFG926_KONLY=1 ...                                      -> cfg926_K.out, cfg926_K.json (exit 0 = all K pass)
     CFG926_MUTATE=z0|imf0|geom ...                          -> cfg926_MUTATE_<mode>.out/.json (exit 1 = bites)
Inputs (read-only): CFG921 machinery exec'd (and through it CFG919/914/880/883/687), CFG829 loader, CFG851 calibrate, CFG824 tau
reader, CFG827 SFH M/L, CFG223 a0(z) definitions, CFG922 JSON, ATLAS3D + SLACS tables, B21 ESD files.  Nothing downloaded.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, time, resource, contextlib, builtins, warnings
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import ellipkm1, ellipe, i0e, i1e, k0e, k1e
from scipy.interpolate import CubicSpline

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
MUT = os.environ.get("CFG926_MUTATE", ""); assert MUT in ("", "z0", "imf0", "geom")
KONLY = os.environ.get("CFG926_KONLY", "") == "1"; assert not (KONLY and MUT)
SUF = "_K" if KONLY else (f"_MUTATE_{MUT}" if MUT else "")
for _e in ("CFG921_MUTATE", "CFG921_KONLY", "CFG919_MUTATE", "CFG914_MUTATE", "CFG880_MUTATE", "CFG883_MUTATE", "CFG829_MUTATE",
           "CFG850_MUTATE", "CFG851_MUTATE", "CFG824_MUTATE", "CFG827_MUTATE", "CFG828_MUTATE", "CFG849_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
_REAL_OPEN = builtins.open
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
RES = dict(lane="CFG926", criteria="48a7a31ae", amendment="AMENDMENT_A1.md", mode=("K" if KONLY else (MUT or "main")), checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}"); return bool(ok)
def jdef(o):
    if hasattr(o, "item"): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
def finish(code):
    RES["runtime_s"] = time.time() - T0; RES["peak_rss_mb"] = rss_mb()
    jn = "cfg926_K.json" if KONLY else f"cfg926_results{SUF}.json" if not MUT else f"cfg926_MUTATE_{MUT}.json"
    on = f"cfg926{SUF}.out" if not MUT else f"cfg926_MUTATE_{MUT}.out"
    with _REAL_OPEN(os.path.join(HERE, jn), "w") as fh: json.dump(RES, fh, indent=1, default=jdef)
    with _REAL_OPEN(os.path.join(HERE, on), "w") as fh: fh.write("\n".join(OUT) + "\n")
    sys.exit(code)

FOOTS = ("canonical", "alt"); A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LN10 = math.log(10.0); THR = 0.05 * LN10
G_SI, MSUN, PC, KPC = 6.674e-11, 1.989e30, 3.0857e16, 3.0857e19
GC = G_SI * MSUN / KPC ** 2                      # m/s^2 per (Msun / kpc^2)
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
LM_RED, LM_BLUE, SHIFT_N2 = 10.81, 10.45, 0.123  # CFG921's lens class masses and CFG667's offset

P("CFG926  three small reframings (B): R4 fossil a0, R5 IMF alpha-sigma, R6 lensing estimator round vs flat"
  + (f"   [MUTATE {MUT}]" if MUT else ("   [K only]" if KONLY else "")))
P("  kappa = 1/2 FITTED; footings never pooled; criteria 48a7a31ae + A1 (post-hoc clarifications)")

# =====================================================================================================================  sandboxed exec of committed code
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG926 refuses to write {file!r} from re-executed committed code")
    return _REAL_OPEN(file, mode, *a, **k)
class _Exit(Exception): pass
def _exit(code=0): raise _Exit(code)
def sandbox_exec(path, pieces, name):
    ns = {"__file__": path, "__name__": name}; buf = io.StringIO(); err = None
    old_open, old_exit = builtins.open, sys.exit
    builtins.open = _ro_open; sys.exit = _exit
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for pc in pieces: exec(compile(pc, path, "exec"), ns)
    except BaseException as e:                  # noqa: BLE001 -- reported as a K failure
        err = f"{type(e).__name__}: {e}"
    finally:
        builtins.open = old_open; sys.exit = old_exit
    return ns, buf.getvalue(), err
def src_of(path): return _REAL_OPEN(path).read()
def line_start(src, marker): i = src.index(marker); return src.rfind("\n", 0, i) + 1
def J(*p):
    with _REAL_OPEN(os.path.join(LANES, *p)) as fh: return json.load(fh)

P("\n=== K-stage")
KOK = []
# ---------------------------------------------------------------------------------------------------- K3: CFG921 machinery
F921 = os.path.join(LANES, "CFG921_excess_selector_posits", "cfg921.py"); s921 = src_of(F921)
pA = s921[:line_start(s921, "P5: QUMOND thin-disc quadrature")]
pB = s921[line_start(s921, "observed structures per footing / variant"):s921.index("\nZTF = ")]
N921, _o921, e921 = sandbox_exec(F921, [pA, pB], "cfg921_ro")
c921 = N921.get("RES", {}).get("checks", {})
k3a = e921 is None and len(c921) >= 5 and all(v["ok"] for v in c921.values())
KOK.append(check("K3a CFG921 machinery exec'd read-only: its own K1-K4, K6 pass inside the exec", k3a,
                 f"{sum(v['ok'] for v in c921.values())}/{len(c921)} CFG921 checks pass" + (f"; error {e921}" if e921 else "")))
if not k3a:
    P("  K3a failed: lane stops (criteria section 5)."); RES["class"] = None; finish(2)
obs_struct, obs_facts, fact_values = N921["obs_struct"], N921["obs_facts"], N921["fact_values"]
DWD, CLD, N880, nu_mono, FLOOR0 = N921["DWD"], N921["CLD"], N921["N880"], N921["nu_mono"], N921["FLOOR0"]
lens_set, cells_lens = N921["lens_set"], N921["N919"]["cells_lens"]
R921 = J("CFG921_excess_selector_posits", "cfg921_results.json")
S, OBS = {}, {}
k3b = []
for f in FOOTS:
    S[f] = obs_struct(f, "V0"); v, se, _ = obs_facts(S[f], f); OBS[f] = (v, se)
    for k, r in R921["observed"][f].items():
        k3b += [abs(v[k] - r["obs"]), abs(se[k] - r["se"])]
KOK.append(check("K3b CFG921 observed facts F0-F10 (value and se, both footings) reproduced by obs_facts", max(k3b) <= 1e-9,
                 f"max |diff| {max(k3b):.1e}; canonical F0 {OBS['canonical'][0]['F0']:+.4f} +- {OBS['canonical'][1]['F0']:.4f}, "
                 f"F1 {OBS['canonical'][0]['F1']:+.4f}, F5 {OBS['canonical'][0]['F5']:+.4f}"))

def gls_class(cells, CE):
    E = np.array([c["E"] for c in cells]); Ct = CE + FLOOR0 ** 2 * np.eye(len(cells)); Ci = np.linalg.inv(Ct); one = np.ones(len(cells))
    a = float(one @ Ci @ one); return float(one @ Ci @ E) / a, a ** -0.5, len(cells)
def lens_class(key, cls, f, shift):
    """F1 (key 'sph', cls 'LS') or F2 ('disc', 'LD') rebuilt at an arbitrary M* shift through CFG919's own cell code"""
    gb, go, C_, gl = lens_set(key, f, shift); c, CE = cells_lens(cls, gb, go, C_, gl, 0.8 if cls == "LS" else 0.2); return gls_class(c, CE)
k3c = []
for f in FOOTS:
    m1, s1, _ = lens_class("sph", "LS", f, SHIFT_N2); m2, s2, _ = lens_class("disc", "LD", f, 0.0)
    k3c += [abs(m1 - OBS[f][0]["F1"]), abs(s1 - OBS[f][1]["F1"]), abs(m2 - OBS[f][0]["F2"]), abs(s2 - OBS[f][1]["F2"])]
KOK.append(check("K3c this lane's arbitrary-shift lens path at shift 0.123 (n>2) / 0 (n<2) equals CFG921's F1 / F2", max(k3c) <= 1e-9, f"max |diff| {max(k3c):.1e}"))

# ---------------------------------------------------------------------------------------------------- K1: CFG850 through CFG829's loader
F829 = os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py")
N829, _, e829 = sandbox_exec(F829, [src_of(F829).split('P("CFG829  KiDS')[0]], "cfg829_ro")
load829, amp829, A0_829 = N829["load"], N829["amp"], N829["A0"]
W850 = (10 ** -13.3, 10 ** -11.9)
F850 = {"blue": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
        "red": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
        "disc": ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
        "sph": ("Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0)}
_L850 = {k: load829(*v) for k, v in F850.items()}
def A850(k, foot, sh):
    gb, go, C = _L850[k]; gbs = gb * 10 ** sh; return amp829(gbs, go, C, gbs * nu_e(gbs / A0_829[foot]), W850)
def split850(foot, sr, sb):
    r, b, s, d = A850("red", foot, sr), A850("blue", foot, sb), A850("sph", foot, sr), A850("disc", foot, sb)
    return dict(A_red=r["A"], sA_red=r["sA"], A_blue=b["A"], sA_blue=b["sA"], z_colour=(r["A"] - b["A"]) / math.hypot(r["sA"], b["sA"]),
                A_sph=s["A"], sA_sph=s["sA"], A_disc=d["A"], sA_disc=d["sA"], z_sersic=(s["A"] - d["A"]) / math.hypot(s["sA"], d["sA"]))
R850 = J("CFG850_red_split_mstar_systematic", "cfg850_results.json")["rows"]; k1 = []
for key, row in R850.items():
    foot, sr, sb = key.split("|"); x = split850(foot, float(sr), float(sb))
    k1 += [abs(x[q] - row[q]) for q in ("A_red", "A_blue", "z_colour", "A_sph", "A_disc", "z_sersic")]
KOK.append(check("K1 CFG850 rows (A_red, A_blue, z_colour, A_sph, A_disc, z_sersic; 10 rows) through CFG829's loader", e829 is None and max(k1) <= 1e-9,
                 f"{len(R850)} rows; max |diff| {max(k1):.1e}; canonical +0.123: A_red {R850['canonical|0.123|0.0']['A_red']:.3f}"))

# ---------------------------------------------------------------------------------------------------- K2: CFG851 calibrate
F851 = os.path.join(LANES, "CFG851_spheroidal_excess_law", "cfg851.py")
N851, _, e851 = sandbox_exec(F851, [src_of(F851).split('P("CFG851  one excess')[0]], "cfg851_ro")
cal851, RED851 = N851["calibrate"], N851["RED"]
R851 = J("CFG851_spheroidal_excess_law", "cfg851_results.json"); k2 = []
for foot in FOOTS:
    for sh in (0.123, 0.0):
        c = cal851(RED851, sh, foot); r = R851[f"{foot}|shift{sh}"]["cal"]
        k2 += [abs(c["b"] / r["b"] - 1), abs(c["lgd"] / r["lgd"] - 1), abs(c["chi2"] / r["chi2"] - 1)]
KOK.append(check("K2 CFG851 red calibration (b, log g_dagger, chi2) at shifts 0.123 and 0, both footings", e851 is None and max(k2) <= 1e-6,
                 f"max rel diff {max(k2):.1e}; canonical +0.123: b {R851['canonical|shift0.123']['cal']['b']:.3f}, lgd {R851['canonical|shift0.123']['cal']['lgd']:.2f}"))

# ---------------------------------------------------------------------------------------------------- K4: CFG824 tau reader, CFG827 SFH M/L and slope
F824 = os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824.py"); s824 = src_of(F824)
N824, _, e824 = sandbox_exec(F824, [s824[:s824.index("# ---- LVD kinematics")]], "cfg824_ro"); AGE = N824["AGE"]
R824 = J("CFG824_dwarf_age_fossil", "cfg824_results.json")["rows"]
k4a = [abs(AGE[n]["tau50"] - r["tau50"]) for n, r in R824.items()] + [abs(AGE[n]["tau90"] - r["tau90"]) for n, r in R824.items()]
F827 = os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827.py")
N827, _, e827 = sandbox_exec(F827, [src_of(F827).split('P("CFG827 (= CFG824b)')[0]], "cfg827_ro")
R827 = J("CFG827_dwarf_age_sfh_ml", "cfg827_results.json")
ups_sfh, SFH, law827, nu827, wt827, fit827 = N827["ups_sfh"], N827["SFH"], N827["law"], N827["nu"], N827["wt"], N827["fit"]
OOS827, ROWS827 = N827["OOS"], N827["rows"]
k4b = []
for r in ROWS827:
    U = ups_sfh(SFH[r["name"]], -1.31); E = math.log(r["so"] / law827(r["MV"], r["rhl"], A0["canonical"], U)); jr = R827["rows"][r["name"]]
    k4b += [abs(U - jr["ups"]), abs(E - jr["E_SFH"])]
def cfg827_E(a0):
    return np.array([math.log(r["so"] / law827(r["MV"], r["rhl"], a0, ups_sfh(SFH[r["name"]], -1.31))) for r in OOS827])
t90_827 = np.array([r["tau90"] for r in OOS827]); w827 = wt827(OOS827)
ab, cov = fit827(cfg827_E(A0["canonical"]), t90_827, w827); sc = R827["scores"]["-1.31"]
k4c = [abs(ab[1] - sc["slope"]), abs(math.sqrt(cov[1, 1]) - sc["slope_err"])]
KOK.append(check("K4 CFG824 tau50/tau90 (36 rows), CFG827 Ups_SFH and E_SFH (36 rows) and the OOS slope reproduced",
                 all(e is None for e in (e824, e827)) and max(k4a) <= 1e-9 and max(k4b) <= 1e-9 and max(k4c) <= 1e-9,
                 f"tau max |diff| {max(k4a):.1e} ({len(R824)} rows); Ups/E max |diff| {max(k4b):.1e} ({len(ROWS827)} rows); slope {ab[1]:+.4f} +- "
                 f"{math.sqrt(cov[1, 1]):.4f} vs {sc['slope']:+.4f} +- {sc['slope_err']:.4f}; OOS N {len(OOS827)}"))

# ---------------------------------------------------------------------------------------------------- K5: a0(z) laws and the footing background
C_LIGHT, GYR, MPC_KM = 2.99792458e8, 3.15576e16, 3.0857e19
OL_F = (A0["canonical"] / A0["alt"]) ** 2; OM_F = 1.0 - OL_F
H0_SI = math.sqrt(8 * math.pi / 3) * 2 * A0["alt"] / C_LIGHT; H0_KMS = H0_SI * MPC_KM
def Ez(z, Om): return np.sqrt(Om * (1 + np.asarray(z, float)) ** 3 + 1 - Om)
def R_dec(z, w0=-0.838, wa=-0.62):
    z = np.asarray(z, float); return np.sqrt((1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / (1.0 + z)))
_TL = {}
def tL(z, Om):
    return quad(lambda x: 1.0 / ((1 + x) * float(Ez(x, Om))), 0, z, limit=200, epsabs=1e-12, epsrel=1e-11)[0] / H0_SI / GYR
def age(Om): return quad(lambda x: 1.0 / ((1 + x) * float(Ez(x, Om))), 0, np.inf, limit=400)[0] / H0_SI / GYR
def z_of_tau(tau, Om):
    key = (round(tau, 12), Om)
    if key not in _TL:
        _TL[key] = 0.0 if tau <= 0 else brentq(lambda z: tL(z, Om) - tau, 0.0, 1e4, xtol=1e-12, rtol=1e-12, maxiter=500)
    return _TL[key]
DESI = {"Pantheon+": (-0.838, -0.62), "DESY5": (-0.752, -0.86), "Union3": (-0.667, -1.09)}   # CFG223 (the record's values)
k5v = [float(R_dec(1.0)), float(R_dec(2.0)), float(R_dec(3.0)), float(Ez(1.0, 0.315)), float(Ez(2.0, 0.315))]
k5ok = (abs(k5v[0] - 0.990) <= 0.002 and abs(k5v[1] - 0.874) <= 0.002 and abs(k5v[2] - 0.775) <= 0.002 and abs(k5v[3] - 1.790) <= 0.002
        and abs(k5v[4] - 3.032) <= 0.002 and abs(H0_KMS - 67.40) <= 0.01)
AGE_U = {Om: age(Om) for Om in (OM_F, 0.308)}
TAUMAX = 13.3
KOK.append(check("K5 a0(z) laws (CFG223 C1) and footing background", k5ok and min(AGE_U.values()) > TAUMAX + 0.1,
                 f"M-DEC R(1,2,3) {k5v[0]:.3f} {k5v[1]:.3f} {k5v[2]:.3f}; E(1), E(2) at 0.315 {k5v[3]:.3f} {k5v[4]:.3f}; Omega_m(footings) {OM_F:.5f}, "
                 f"H0 {H0_KMS:.3f} km/s/Mpc; age {AGE_U[OM_F]:.3f} Gyr (Om 0.308: {AGE_U[0.308]:.3f}) > max tau {TAUMAX}"))

# ---------------------------------------------------------------------------------------------------- R6 numerics (used by K6 and the main run)
TT = np.linspace(0.0, 25.0, 5001)
def simpson_w(x):
    n = len(x); h = (x[-1] - x[0]) / (n - 1); w = np.ones(n); w[1:-1:2] = 4; w[2:-1:2] = 2; return w * h / 3
WT = simpson_w(TT); CH = np.cosh(TT); SECH2 = 1.0 / CH ** 2
def esd(R, Mfun, rhofun, rt=None):
    """stacked ESD (Msun/kpc^2) of a spherically averaged profile M(<r); r = R cosh t substitution; optional truncation at rt"""
    with np.errstate(all="ignore"):                                       # spurious Accelerate FP flags in matmul; finiteness asserted
        if rt is None or rt >= R * CH[-1]:
            r = R * CH; Mcyl = WT @ (Mfun(r) * SECH2); Sig = 2 * R * (WT @ (rhofun(r) * CH))
        else:
            tmax = math.acosh(rt / R); t1 = np.linspace(0.0, tmax, 5001); t2 = np.linspace(tmax, 25.0, 5001)
            w1, w2 = simpson_w(t1), simpson_w(t2); c1, c2 = np.cosh(t1), np.cosh(t2); Mt = Mfun(np.array([rt]))[0]
            Mcyl = w1 @ (Mfun(R * c1) / c1 ** 2) + Mt * (w2 @ (1.0 / c2 ** 2)); Sig = 2 * R * (w1 @ (rhofun(R * c1) * c1))
    assert np.isfinite(Mcyl) and np.isfinite(Sig)
    return Mcyl / (math.pi * R ** 2) - Sig
def numderiv(Mfun):
    def rho(r):
        h = 1e-5 * r; return (Mfun(r + h) - Mfun(r - h)) / (2 * h) / (4 * math.pi * r ** 2)
    return rho
def M_pm(M, a0): return lambda r: M * nu_e(GC * M / r ** 2 / a0)
def M_hern(M, a, a0):
    def f(r):
        MN = M * r ** 2 / (r + a) ** 2; return MN * nu_e(GC * MN / r ** 2 / a0)
    return f
def ring_g(a, R, z):
    """field (g_R, g_z) per unit ring mass (m/s^2 per Msun), ring radius a in the plane z = 0, field point (R, z), kpc"""
    s2 = (a + R) ** 2 + z ** 2; s = np.sqrt(s2); p = ((a - R) ** 2 + z ** 2) / s2; m = 1.0 - p
    K = ellipkm1(p); E = ellipe(m)
    with np.errstate(divide="ignore", invalid="ignore"):
        dK = np.where(m < 1e-6, math.pi / 8 + 9 * math.pi * m / 64, (E - p * K) / (2 * m * p))
    dmR = 4 * a * (a ** 2 - R ** 2 + z ** 2) / s2 ** 2; dmz = -8 * a * R * z / s2 ** 2
    gR = (2 * GC / math.pi) * (dK * dmR / s - K * (a + R) / s ** 3); gz = (2 * GC / math.pi) * (dK * dmz / s - K * z / s ** 3)
    return gR, gz
XG, WG = np.polynomial.legendre.leggauss(200)
def gl_panel(lo, hi):
    return 0.5 * (hi - lo) * XG + 0.5 * (hi + lo), 0.5 * (hi - lo) * WG
def disc_g(R, z, M, Rd, amax_fac=40.0):
    """thin exponential disc g_N at (R, z > 0) by ring sums, panels clustered at a = R"""
    amax = amax_fac * Rd; bp = [0.0, amax]
    if R < amax:
        bp += [x for x in (R - 5 * z, R, R + 5 * z) if 0 < x < amax]
    bp = sorted(set(bp)); gR = gz = 0.0
    for lo, hi in zip(bp[:-1], bp[1:]):
        a, w = gl_panel(lo, hi); sig = M / (2 * math.pi * Rd ** 2) * np.exp(-a / Rd); r_, z_ = ring_g(a, R, z)
        gR += np.sum(w * sig * 2 * math.pi * a * r_); gz += np.sum(w * sig * 2 * math.pi * a * z_)
    return gR, gz
def disc_g_mid_paired(R, M, Rd, amax_fac=40.0):
    """midplane g_R by ring sums with a symmetric (principal-value) pairing around a = R (K6 only)"""
    amax = amax_fac * Rd; U = 0.5 * R; sigf = lambda a: M / (2 * math.pi * Rd ** 2) * np.exp(-a / Rd)
    tot = 0.0
    for lo, hi in ((0.0, R - U), (R + U, amax)):
        xg, wg = np.polynomial.legendre.leggauss(600); a = 0.5 * (hi - lo) * xg + 0.5 * (hi + lo); w = 0.5 * (hi - lo) * wg
        tot += np.sum(w * sigf(a) * 2 * math.pi * a * ring_g(a, R, 0.0)[0])
    xg, wg = np.polynomial.legendre.leggauss(600); t = 0.5 * xg + 0.5; wt = 0.5 * wg; u = U * t ** 2; du = 2 * U * t * wt
    fp = sigf(R + u) * 2 * math.pi * (R + u) * ring_g(R + u, R, 0.0)[0]; fm = sigf(R - u) * 2 * math.pi * (R - u) * ring_g(R - u, R, 0.0)[0]
    return tot + np.sum(du * (fp + fm))
MUX, MUW = np.polynomial.legendre.leggauss(32); MUSEL = MUX > 0; MUX, MUW = MUX[MUSEL], MUW[MUSEL]
P2 = 0.5 * (3 * MUX ** 2 - 1)
RGRID = np.geomspace(10.0, 3000.0, 90)
def disc_profile(M, Rd, a0):
    """spherically averaged QUMOND enclosed mass of the disc (Gauss) on RGRID, the delta spline vs the point-mass law, q2(r)"""
    Mt, q2 = np.empty(len(RGRID)), np.empty(len(RGRID))
    for i, r in enumerate(RGRID):
        f = np.empty(len(MUX))
        for j, mu in enumerate(MUX):
            R, z = r * math.sqrt(1 - mu * mu), r * mu; gR, gz = disc_g(R, z, M, Rd); gr = gR * math.sqrt(1 - mu * mu) + gz * mu
            f[j] = float(nu_e(math.hypot(gR, gz) / a0)) * (-gr)
        Mt[i] = r ** 2 / GC * (MUW @ f) / MUW.sum(); q2[i] = 5 * (MUW @ (f * P2)) / (MUW @ f)
    delta = Mt / M_pm(M, a0)(RGRID) - 1.0; sp = CubicSpline(np.log(RGRID), delta)
    def Mfun(r):
        r = np.asarray(r, float); d = np.where(r <= RGRID[-1], sp(np.log(np.clip(r, RGRID[0], RGRID[-1]))), 0.0); return M_pm(M, a0)(r) * (1 + d)
    def rhofun(r):
        r = np.asarray(r, float); inside = r <= RGRID[-1]; lr = np.log(np.clip(r, RGRID[0], RGRID[-1]))
        d = np.where(inside, sp(lr), 0.0); dd = np.where(inside, sp(lr, 1) / r, 0.0); mp = M_pm(M, a0)
        h = 1e-5 * r; dmp = (mp(r + h) - mp(r - h)) / (2 * h)
        return (dmp * (1 + d) + mp(r) * dd) / (4 * math.pi * r ** 2)
    return dict(M=Mfun, rho=rhofun, delta=delta, q2=q2)
def Re_round(lm): return 10 ** (0.56 * lm - 5.54)                                  # CFG921 LS (Shen+03 early types)
def Re_flat(lm): M = 10 ** lm; return 0.10 * M ** 0.14 * (1 + M / 3.98e10) ** 0.25   # CFG921 LD (Shen+03 late types)

# ---------------------------------------------------------------------------------------------------- K6
k6 = {}
R6t = np.array([20.0, 60.0, 200.0, 600.0])
k6["SIS"] = max(abs(4 * GC * esd(R, lambda r: 3e8 * r, lambda r: 3e8 / (4 * math.pi * r ** 2)) / (GC * 3e8 * R / R ** 2) - 1) for R in R6t)
k6["pm"] = max(abs(4 * GC * esd(R, lambda r: 1e11 + 0 * r, lambda r: 0 * r) / (GC * 1e11 / R ** 2) - 4 / math.pi) for R in R6t)
apl = 30.0; Mpl = 1e11
plM = lambda r: Mpl * r ** 3 / (r ** 2 + apl ** 2) ** 1.5; plrho = lambda r: 3 * Mpl * apl ** 2 / (4 * math.pi * (r ** 2 + apl ** 2) ** 2.5)
k6["Plummer"] = max(abs(esd(R, plM, plrho) / (Mpl * R ** 2 / (math.pi * (R ** 2 + apl ** 2) ** 2)) - 1) for R in R6t)
Rd_t, M_t = 2.0, 3e10; yv = 3.0 * Rd_t / (2 * Rd_t)
gF = 2 * GC * M_t / (Rd_t * 3.0 * Rd_t) * yv ** 2 * (i0e(yv) * k0e(yv) - i1e(yv) * k1e(yv))
k6["Freeman"] = abs(-disc_g_mid_paired(3.0 * Rd_t, M_t, Rd_t) / gF - 1)
gfar = disc_g(2000.0 * math.sqrt(1 - 0.3 ** 2), 2000.0 * 0.3, M_t, Rd_t); k6["far_pm"] = abs(math.hypot(*gfar) / (GC * M_t / 2000.0 ** 2) - 1)
ggrid = np.geomspace(10 ** -13.3, 10 ** -10.9, 25); k6e = 0.0
for f in FOOTS:
    bet = []
    for lm in (LM_RED + SHIFT_N2, LM_BLUE):
        M = 10 ** lm; Mf = M_pm(M, A0[f]); rf = numderiv(Mf)
        bet.append(np.array([4 * GC * esd(math.sqrt(GC * M / g), Mf, rf) / (g * nu_e(g / A0[f])) for g in ggrid]))
    k6e = max(k6e, float(np.max(np.abs(bet[0] - bet[1]))))
k6["pm_scale_invariance"] = k6e
rng6 = np.random.default_rng(926); NPT, NOR = 20000, 400
rr = rng6.gamma(2.0, 1.0, NPT); ph = rng6.uniform(0, 2 * math.pi, NPT); zz = rng6.laplace(0, 0.1, NPT)
X3 = np.vstack([rr * np.cos(ph), rr * np.sin(ph), zz]).T; r3 = np.linalg.norm(X3, axis=1)
nv = rng6.normal(size=(NOR, 3)); nv /= np.linalg.norm(nv, axis=1)[:, None]; Rp = np.array([0.5, 1.0, 2.0, 4.0]); mc_ok = True; mc_rep = []
for Rq in Rp:
    with np.errstate(all="ignore"):
        fr = np.array([np.mean(r3 ** 2 - (X3 @ n) ** 2 < Rq ** 2) for n in nv])
    assert np.all(np.isfinite(fr)); sph = np.mean(np.where(r3 < Rq, 1.0, 1.0 - np.sqrt(np.clip(1 - Rq ** 2 / np.maximum(r3, Rq) ** 2, 0, 1))))
    sd = fr.std(ddof=1) / math.sqrt(NOR); zmc = (fr.mean() - sph) / sd; mc_ok &= abs(zmc) <= 4; mc_rep.append(f"R {Rq}: {fr.mean():.4f} vs {sph:.4f} (z {zmc:+.1f})")
del X3
k6ok = (k6["SIS"] <= 1e-4 and k6["pm"] <= 1e-4 and k6["Plummer"] <= 1e-4 and k6["Freeman"] <= 1e-3 and k6["far_pm"] <= 1e-4
        and k6["pm_scale_invariance"] <= 1e-6 and mc_ok)
RES["K6"] = dict(k6, montecarlo=mc_rep)
KOK.append(check("K6 R6 numerics: SIS beta = 1, point mass 4/pi, Plummer ESD closed form, ring-sum disc vs Freeman at 3 R_d, far field = point mass, "
                 "point-mass law scale invariance (A1-1), Monte-Carlo isotropy of M_cyl", k6ok,
                 f"SIS {k6['SIS']:.1e}; pm {k6['pm']:.1e}; Plummer {k6['Plummer']:.1e}; Freeman {k6['Freeman']:.1e}; far {k6['far_pm']:.1e}; "
                 f"scale inv {k6['pm_scale_invariance']:.1e}; MC " + "; ".join(mc_rep)))

# ---------------------------------------------------------------------------------------------------- K7: CFG922 and SLACS
R922 = J("CFG922_cluster_core_baryon_recheck", "cfg922_results_A1.json")
NEED = {}
for f in FOOTS:
    nm = R922["results"][f"eRASS1|s|{f}"]["needed_masses"]; NEED[f] = dict(alpha=nm["4"]["needed_alpha"], M4=nm["4"]["needed"], MU=nm["U"]["needed"], lam=nm["U"]["lam"])
def slacs():
    with _REAL_OPEN(os.path.join(DATA, "slacs_auger2009_lenses.tsv")) as fh:
        lines = [l.rstrip("\n") for l in fh if not l.startswith("#") and l.strip()]
    hdr = lines[0].split("\t"); rows = [l.split("\t") for l in lines[3:]]
    def col(n):
        k = hdr.index(n); v = []
        for r in rows:
            try: v.append(float(r[k]))
            except (ValueError, IndexError): v.append(np.nan)
        return np.array(v)
    Fc, lmc, lms = col("Fc"), col("logMc"), col("logMs"); g = np.isfinite(Fc) & (Fc > 0)
    return dict(alpha_max=float(np.percentile(1 / Fc[g], 95)), sc=float(np.nanmedian(10 ** (lms - lmc))))
SL = slacs(); SC = SL["sc"]
KOK.append(check("K7 CFG922 needed alpha (72.43 / 59.83), SLACS Salpeter/Chabrier 1.778 and alpha_max 3.78 from the files",
                 abs(NEED["canonical"]["alpha"] - 72.43) < 0.01 and abs(NEED["alt"]["alpha"] - 59.83) < 0.01 and abs(SC - 1.778) < 1e-3 and abs(SL["alpha_max"] - 3.782) < 1e-3,
                 f"alpha_need {NEED['canonical']['alpha']:.2f} / {NEED['alt']['alpha']:.2f}; lam {NEED['canonical']['lam']:.3f} / {NEED['alt']['lam']:.3f}; "
                 f"S/C {SC:.4f}; alpha_max {SL['alpha_max']:.3f}"))
K_ALL = all(KOK)
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
if not K_ALL:
    P("  A K-test failed: per criteria section 5 the lane stops; no class."); RES["class"] = None; finish(2)
if KONLY:
    RES["class"] = "K only"; finish(0)

# =====================================================================================================================  grading helpers
def grade_target(Eo, Er):
    if abs(Er) <= 0.5 * abs(Eo): return "RESOLVES"
    if abs(Eo) - abs(Er) >= THR: return "PARTIAL"
    if abs(Er) - abs(Eo) >= THR: return "WORSENS"
    return "NO EFFECT"
def overall(labels, conds_ok, cond_broken):
    """labels: graded-target labels; conds_ok: all conditions hold; cond_broken: a condition broken by >= THR"""
    if all(l == "RESOLVES" for l in labels) and conds_ok: return "RESOLVES"
    good = any(l in ("RESOLVES", "PARTIAL") for l in labels); bad = any(l == "WORSENS" for l in labels) or cond_broken
    if good: return "PARTIAL (MIXED)" if bad else "PARTIAL"
    if bad: return "WORSENS"
    return "NO EFFECT"
def dex(x): return x / LN10

# =====================================================================================================================  R4 fossil a0
def F_law(law, z):
    z = np.asarray(z, float)
    if MUT == "z0": z = np.zeros_like(z)
    if law == "FLAT": return np.ones_like(z)
    if law.startswith("M-DEC"):
        nm = law.split("|")[1] if "|" in law else "Pantheon+"; w0, wa = DESI[nm]
        return R_dec(np.minimum(z, 2.5) if law.startswith("M-DEC-c") else z, w0, wa)
    if law.startswith("H(z)"): return Ez(z, 0.308 if law.endswith("Om0.308") else OM_F)
    raise ValueError(law)
def bg_Om(law): return 0.308 if law.endswith("Om0.308") else OM_F
LAWS = ["FLAT", "M-DEC", "M-DEC|DESY5", "M-DEC|Union3", "M-DEC-c", "H(z)", "H(z)|Om0.308"]
LAWROLE = {"FLAT": "framework", "M-DEC": "framework (primary DESI CPL)", "M-DEC|DESY5": "framework corner", "M-DEC|Union3": "framework corner",
           "M-DEC-c": "framework variant (clamped at z 2.5)", "H(z)": "RIVAL (declared contrast)", "H(z)|Om0.308": "RIVAL variant"}
ZF_LS = (1.0, math.sqrt(8.0) - 1.0, 3.0); ZF_CL = (0.3, math.sqrt(2.6) - 1.0, 1.0)
names = list(DWD["canonical"]["names"]); assert names == list(DWD["alt"]["names"])
MV = np.array([N880["fnum"](N880["LVD"][n]["M_V"]) for n in names])
matched = np.array([n in AGE for n in names]); t50m = np.array([AGE[n]["tau50"] if n in AGE else np.nan for n in names])
ufd = (~matched) & (MV > -7.7); brt = (~matched) & ~(MV > -7.7)
T50MED, T50MIN, T50MAX = float(np.median(t50m[matched])), float(np.min(t50m[matched])), float(np.max(t50m[matched]))
P(f"\n=== R4 fossil a0.  83 LVD dwarfs: Weisz+14 matched {int(matched.sum())}, unmatched UFD (M_V > -7.7) {int(ufd.sum())}, unmatched brighter "
  f"{int(brt.sum())}; matched tau50 median {T50MED:.2f} (min {T50MIN:.2f}, max {T50MAX:.2f}) Gyr")
P(f"  background (footings): Omega_m {OM_F:.5f}, H0 {H0_KMS:.2f}; z_f red lenses {ZF_LS[0]:.3f}/{ZF_LS[1]:.3f}/{ZF_LS[2]:.3f}, clusters "
  f"{ZF_CL[0]:.3f}/{ZF_CL[1]:.3f}/{ZF_CL[2]:.3f} (primary = middle)")
DW_CORNERS = [(tu, tb) for tu in (13.3, 12.59) for tb in ("median", "min", "max")]
def dwarf_tau(tu, tb):
    t = t50m.copy(); t[ufd] = tu; t[brt] = {"median": T50MED, "min": T50MIN, "max": T50MAX}[tb]; return t
def r4_predict(law, f, tu=13.3, tb="median", zls=ZF_LS[1], zcl=ZF_CL[1], hi_resettle=False):
    Om = bg_Om(law); a0 = A0[f]; Sf = S[f]; D = DWD[f]
    tau = dwarf_tau(tu, tb); zf = np.array([z_of_tau(t, Om) for t in tau]); F = F_law(law, zf)
    dwE = np.log(nu_e(D["gb"] / (a0 * F)) / nu_e(D["gb"] / a0))
    if hi_resettle: dwE = np.where(D["hi"], 0.0, dwE)
    cells = {"DW": np.array([np.mean(dwE[m]) for m in Sf["dwcell"]])}
    Fls = float(F_law(law, zls)); Ls = Sf["lens"]["LS"]; pe = np.log(nu_e(Ls["gbs"] / (a0 * Fls)) / nu_e(Ls["gbs"] / a0))
    cells["LS"] = np.array([math.log(float(w @ (Ls["gl"][Sx] * np.exp(pe[Sx])))) for Sx, w in Ls["W"]])
    for c in ("LD", "SS", "SL"): cells[c] = np.zeros(len(Sf["ops"][c]["ix"]))
    C = CLD[f]; Fcl = float(F_law(law, zcl)); ce = np.log(nu_mono(C["gb"] / (C["a0"] * Fcl)) / nu_mono(C["gb"] / C["a0"])); WP = C["W"] * C["Pm"]
    cells["CL"] = np.array([math.log(float((WP[m] * np.exp(ce[m])).sum() / WP[m].sum())) for m in Sf["clus"]])
    return fact_values(Sf, cells, dwE, f), dict(zf_dw_med=float(np.median(zf)), F_dw_med=float(np.median(F)), F_ls=Fls, F_cl=Fcl)
def r4_slope827(law, f):
    Om = bg_Om(law); a0 = A0[f]; Eobs = cfg827_E(a0); Ef = []
    for r in OOS827:
        U = ups_sfh(SFH[r["name"]], -1.31); M = U * 10 ** (0.4 * (4.83 - r["MV"])); y = G_SI * (M / 2) * MSUN / ((4 / 3) * r["rhl"] * PC) ** 2 / a0
        Fz = float(F_law(law, z_of_tau(AGE[r["name"]]["tau50"], Om))); Ef.append(0.5 * math.log(nu827(y / Fz) / nu827(y)))
    Ef = np.array(Ef); ao, co = fit827(Eobs, t90_827, w827); ap, _ = fit827(Ef, t90_827, w827)
    so, se = float(ao[1]), float(math.sqrt(co[1, 1])); sp = float(ap[1])
    return dict(s_obs=so, se_obs=se, s_pred=sp, z=(so - sp) / se, mean_E_obs=float(np.sum(w827 * Eobs) / np.sum(w827)),
                mean_E_fossil=float(np.sum(w827 * Ef) / np.sum(w827)), N=len(Ef))
def r4_grade(law, f, pv_prim, corners_F0, slope):
    v, se = OBS[f]
    F0p = [c["F0"] for c in corners_F0]; s_pred = 0.5 * (max(F0p) - min(F0p))
    tg = {}
    for k in ("F0", "F1", "F5"):
        Eo = v[k]; Er = Eo - pv_prim[k]; tg[k] = dict(obs=Eo, se=se[k], pred=pv_prim[k], res=Er, removed_frac=pv_prim[k] / Eo, label=grade_target(Eo, Er))
    zdw = (v["F0"] - pv_prim["F0"]) / math.sqrt(se["F0"] ** 2 + s_pred ** 2)
    dwarf_ok = abs(zdw) < 2 and abs(slope["z"]) < 2
    rot = {k: dict(obs=v[k], se=se[k], pred=0.0, within_2sig=abs(v[k]) < 2 * se[k]) for k in ("F2", "F3", "F4")}
    rot_ok = all(x["within_2sig"] for x in rot.values())
    cls = overall([tg[k]["label"] for k in tg], dwarf_ok and rot_ok, False)
    return dict(targets=tg, dwarf_condition=dict(z_F0=zdw, s_pred_F0=s_pred, slope=slope, ok=dwarf_ok),
                rotators=dict(by_construction=True, facts=rot, ok=rot_ok), cls=cls)
R4 = {}
for f in FOOTS:
    R4[f] = {}
    for law in LAWS:
        pv, info = r4_predict(law, f)
        cF0 = [r4_predict(law, f, tu, tb)[0] for tu, tb in DW_CORNERS]
        sl = r4_slope827(law, f)
        rec = r4_grade(law, f, pv, cF0, sl)
        # corner classes: dwarf fallback x red-lens z_f x cluster z_f
        ccls, clist = set(), []
        for i, (tu, tb) in enumerate(DW_CORNERS):
            for zls in ZF_LS:
                for zcl in ZF_CL:
                    pvc, _ = r4_predict(law, f, tu, tb, zls, zcl); gc_ = r4_grade(law, f, pvc, cF0, sl); ccls.add(gc_["cls"])
                    clist.append(dict(tau_ufd=tu, tau_bright=tb, zf_ls=zls, zf_cl=zcl, F0=pvc["F0"], F1=pvc["F1"], F5=pvc["F5"], cls=gc_["cls"]))
        hi_pv, _ = r4_predict(law, f, hi_resettle=True); hi_rec = r4_grade(law, f, hi_pv, cF0, sl)
        rec.update(role=LAWROLE[law], info=info, corner_classes=sorted(ccls), bracket_dependent=len(ccls) > 1, corner_list=clist,
                   diagnostics={k: dict(pred=pv[k], obs=OBS[f][0][k], se=OBS[f][1][k]) for k in ("F6", "F7", "F8b", "F9", "F10")},
                   variant_HI_resettle=dict(F0_pred=hi_pv["F0"], cls=hi_rec["cls"]), corners_F0=[c["F0"] for c in cF0])
        R4[f][law] = rec
        t = rec["targets"]
        P(f"  [{f:9s}] {law:13s} ({LAWROLE[law]}): F0 pred {t['F0']['pred']:+.3f} (obs {t['F0']['obs']:+.3f}) {t['F0']['label']}; "
          f"F1 {t['F1']['pred']:+.3f} ({t['F1']['obs']:+.3f}) {t['F1']['label']}; F5 {t['F5']['pred']:+.3f} ({t['F5']['obs']:+.3f}) {t['F5']['label']}  "
          f"| dwarf z {rec['dwarf_condition']['z_F0']:+.2f}, slope pred {sl['s_pred']:+.4f} vs obs {sl['s_obs']:+.4f}+-{sl['se_obs']:.4f} (z {sl['z']:+.2f})  "
          f"=> {rec['cls']}{'  [BRACKET-DEPENDENT: ' + ', '.join(sorted(ccls)) + ']' if len(ccls) > 1 else ''}")
        P(f"              diag: F6 pred {pv['F6']:+.3f} (obs {OBS[f][0]['F6']:+.3f}); F8b {pv['F8b']:+.3f} ({OBS[f][0]['F8b']:+.3f}); F10 {pv['F10']:+.3f} "
          f"({OBS[f][0]['F10']:+.3f}); mean E_sigma CFG827 obs {sl['mean_E_obs']:+.3f} vs fossil {sl['mean_E_fossil']:+.3f}; HI-resettle F0 {hi_pv['F0']:+.3f} -> {hi_rec['cls']}")
        for c_ in clist:
            if c_["cls"] == "RESOLVES":
                P(f"              [post-hoc report] RESOLVES corner: tau_UFD {c_['tau_ufd']}, bright {c_['tau_bright']}, z_f lens {c_['zf_ls']:.3f}, z_f cl {c_['zf_cl']:.3f}: "
                  f"F0 {c_['F0']:+.3f} F1 {c_['F1']:+.3f} F5 {c_['F5']:+.3f}")
RES["R4"] = R4
if MUT == "z0":
    mx = max(abs(R4[f][law]["targets"][k]["pred"]) for f in FOOTS for law in LAWS for k in ("F0", "F1", "F5"))
    mx = max(mx, max(abs(R4[f][law]["dwarf_condition"]["slope"]["s_pred"]) for f in FOOTS for law in LAWS))
    bites = mx <= 1e-12; RES["mutate_z0"] = dict(max_abs_pred=mx, bites=bites)
    P(f"\n  MUTATE z0: max |prediction| over every law, target and footing = {mx:.1e} -> {'BITES (effect removed)' if bites else 'DOES NOT BITE'}")
    finish(1 if bites else 0)

# =====================================================================================================================  R5 IMF alpha-sigma
def atlas3d():
    with _REAL_OPEN(os.path.join(DATA, "atlas3d_fj_table.tsv")) as fh:
        lines = [l.rstrip("\n") for l in fh if l.strip() and not l.startswith("#")]
    hdr = lines[0].split("\t"); rows = []
    for l in lines[1:]:
        v = l.split("\t"); d = dict(zip(hdr, v))
        try:
            rec = {k: float(d[k]) for k in ("logsig_e", "logML_JAM", "qual", "logr12", "logL", "logML_stars", "logML_Salp", "Dist_Mpc")}
        except (ValueError, KeyError):
            continue
        rec["name"] = d["name"]; rows.append(rec)
    return rows
A3 = [r for r in atlas3d() if r["qual"] >= 1]
A3x = np.array([r["logsig_e"] - math.log10(200.0) for r in A3]); A3y = np.array([r["logML_stars"] - r["logML_Salp"] for r in A3])
A3lm = np.array([r["logL"] + r["logML_Salp"] - math.log10(SC) for r in A3]); A3ls = np.array([r["logsig_e"] for r in A3])
def ols(x, y): X = np.vstack([np.ones_like(x), x]).T; return np.linalg.lstsq(X, y, rcond=None)[0]
def law_ups(r, a0):
    L = 10 ** r["logL"]; ups_j = 10 ** r["logML_JAM"]; r12 = 10 ** r["logr12"] * r["Dist_Mpc"] * 1e3 / 206264.806
    f = lambda lu: 10 ** lu * float(nu_e(GC * 10 ** lu * (L / 2) / r12 ** 2 / a0)) - ups_j
    return 10 ** brentq(f, math.log10(ups_j) - 3, math.log10(ups_j), xtol=1e-12)
def r5_pars(idx=None, y=None):
    ii = np.arange(len(A3)) if idx is None else idx; yy = A3y if y is None else y
    a, b = ols(A3x[ii], yy[ii]); c, d = ols(A3lm[ii] - 10.5, A3ls[ii]); return (a, b, c, d)
def dIMF(logM, pars, clip=True):
    a, b, c, d = pars
    if MUT == "imf0": return 0.0
    la = a + b * ((c + d * (logM - 10.5)) - math.log10(200.0)) + math.log10(SC); return max(0.0, la) if clip else la
def alpha_chab_sigma(sig, pars, clip=True):
    a, b, c, d = pars
    if MUT == "imf0": return 1.0
    la = a + b * (math.log10(sig) - math.log10(200.0)) + math.log10(SC); return 10 ** (max(0.0, la) if clip else la)
PARS = r5_pars()
rngb = np.random.default_rng(926); BOOT = [r5_pars(rngb.integers(0, len(A3), len(A3))) for _ in range(2000)]
LMR = LM_RED + SHIFT_N2
P(f"\n=== R5 IMF alpha-sigma.  ATLAS3D qual >= 1: N {len(A3)}; log alpha_Salp = {PARS[0]:+.4f} + {PARS[1]:.4f} log(sigma_e/200); "
  f"log sigma_e = {PARS[2]:.4f} + {PARS[3]:.4f} (log M*_Chab - 10.5); S/C {SC:.4f}")
sig_red = 10 ** (PARS[2] + PARS[3] * (LMR - 10.5)); sig_blue = 10 ** (PARS[2] + PARS[3] * (LM_BLUE - 10.5))
D_red = dIMF(LMR, PARS); D_blue = dIMF(LM_BLUE, PARS)
P(f"  red/n>2 lenses: log M* {LMR:.3f} -> sigma {sig_red:.1f} km/s -> Delta_IMF {D_red:+.4f} dex; blue variant log M* {LM_BLUE:.2f} -> sigma {sig_blue:.1f} -> {D_blue:+.4f}")
R5 = dict(relation=dict(N=len(A3), a=PARS[0], b=PARS[1], c=PARS[2], d=PARS[3], SC=SC, sigma_red=sig_red, sigma_blue=sig_blue, D_red=D_red, D_blue=D_blue), byfoot={})
LAWPARS = {}
for f in FOOTS:
    yl = np.array([math.log10(law_ups(r, A0[f])) - r["logML_Salp"] for r in A3]); LAWPARS[f] = r5_pars(y=yl)
    R5["relation"][f"law_{f}"] = dict(a=LAWPARS[f][0], b=LAWPARS[f][1], D_red=dIMF(LMR, LAWPARS[f]), median_dy_law_minus_lit=float(np.median(yl - A3y)))
    P(f"  R5-law ({f}): log alpha_law = {LAWPARS[f][0]:+.4f} + {LAWPARS[f][1]:.4f} x; median (law - literature) {np.median(yl - A3y):+.4f} dex; "
      f"Delta_IMF(red) {dIMF(LMR, LAWPARS[f]):+.4f}")
def r5_eval(f, Dr, Db=0.0):
    v, se = OBS[f]; m1, s1, n1 = lens_class("sph", "LS", f, SHIFT_N2 + Dr); m2, s2, n2 = lens_class("disc", "LD", f, Db)
    return dict(F1=m1, se1=s1, n1=n1, F2=m2, se2=s2, z_cells=(m1 - m2) / math.hypot(s1, s2))
for f in FOOTS:
    v, se = OBS[f]; rec = {}
    base = r5_eval(f, 0.0); prim = r5_eval(f, D_red); alone_m, alone_s, _ = lens_class("sph", "LS", f, D_red)
    lab = grade_target(v["F1"], prim["F1"])
    # conditions: rotators unchanged (primary), dwarfs clipped -> unchanged
    rot_ok = abs(v["F2"]) < 2 * se["F2"] and abs(v["F3"]) < 2 * se["F3"] and abs(v["F4"]) < 2 * se["F4"]
    # corners
    ccls, cvals = set(), []
    for dm in (-0.2, 0.0, 0.2):
        bd = np.array([dIMF(LMR + dm, p) for p in BOOT]); qs = {"p16": float(np.percentile(bd, 16)), "point": dIMF(LMR + dm, PARS), "p84": float(np.percentile(bd, 84))}
        for qn, Dq in qs.items():
            ev = r5_eval(f, Dq); l_ = grade_target(v["F1"], ev["F1"]); c_ = overall([l_], rot_ok, False); ccls.add(c_)
            cvals.append(dict(dlogM=dm, q=qn, D=Dq, F1=ev["F1"], label=l_, cls=c_))
    cls = overall([lab], rot_ok, False)
    # CFG850 window and CFG851 law after the correction
    w0 = split850(f, SHIFT_N2, 0.0); w1 = split850(f, SHIFT_N2 + D_red, 0.0); wa = split850(f, D_red, 0.0)
    c851 = cal851(RED851, SHIFT_N2 + D_red, f)
    # variants
    law_ev = r5_eval(f, dIMF(LMR, LAWPARS[f])); law_lab = grade_target(v["F1"], law_ev["F1"]); law_cls = overall([law_lab], rot_ok, False)
    blue_ev = r5_eval(f, D_red, D_blue); blue_rot = abs(blue_ev["F2"]) < 2 * blue_ev["se2"] and abs(blue_ev["F2"] - v["F2"]) < THR
    blue_cls = overall([grade_target(v["F1"], blue_ev["F1"])], blue_rot and rot_ok, abs(blue_ev["F2"] - v["F2"]) >= THR)
    D = DWD[f]; sobs = D["sl"] * np.exp(D["E"] / 2.0)
    al = np.array([alpha_chab_sigma(s, PARS, clip=False) for s in sobs]); gbp = D["gb"] * (al * D["w"] + 1 - D["w"])
    Edw = D["E"] - np.log(gbp * nu_e(gbp / D["a0"]) / (D["gb"] * nu_e(D["gb"] / D["a0"])))
    F0dw = float(S[f]["ops"]["DW"]["w"] @ np.array([np.mean(Edw[m]) for m in S[f]["dwcell"]]))
    dw_broken = (F0dw - v["F0"]) >= se["F0"]
    # secondary target: BCG / cluster cores (CFG922 bound)
    cl = {}
    for sg in (250.0, 300.0, 400.0):
        ac = alpha_chab_sigma(sg, PARS); fm = (ac - 1) / (NEED[f]["alpha"] - 1); X = NEED[f]["lam"] * NEED[f]["M4"] / NEED[f]["MU"]
        bnd = math.log(1 + fm * X); cl[sg] = dict(alpha_chab=ac, f_m=fm, X=X, bound=bnd, label=grade_target(v["F5"], v["F5"] - bnd))
    # reported only: zero slope, kept offset (alpha(200) for every class, unclipped)
    d0 = 0.0 if MUT == "imf0" else PARS[0] + math.log10(SC); zs = r5_eval(f, d0, d0)
    d_sl = 0.0 if MUT == "imf0" else max(0.0, math.log10(SC) - 0.120); sl_ev = r5_eval(f, d_sl)       # post hoc: AUDIT_SLUGGS ceiling (Salpeter over-predicts by 0.120 dex under the law)
    rec = dict(target_F1=dict(obs=v["F1"], se=se["F1"], res=prim["F1"], removed=v["F1"] - prim["F1"], removed_frac=(v["F1"] - prim["F1"]) / v["F1"], label=lab),
               IMF_alone_F1=dict(F1=alone_m, se=alone_s, uncorrected_baseline_F1=lens_class("sph", "LS", f, 0.0)[0]),
               split_cells=dict(before=base["z_cells"], after=prim["z_cells"], F1_minus_F2_before=base["F1"] - base["F2"], F1_minus_F2_after=prim["F1"] - prim["F2"]),
               window850=dict(before=w0, after=w1, IMF_alone=wa), law851_after=dict(b=c851["b"], lgd=c851["lgd"], b_lo=c851["b_lo"], b_hi=c851["b_hi"], chi2=c851["chi2"], chi2_law=c851["chi2_law"]),
               rotators=dict(primary_unchanged=True, ok=rot_ok), dwarfs=dict(primary_change=0.0, unclipped_F0=F0dw, unclipped_change=F0dw - v["F0"], unclipped_breaks_condition=bool(dw_broken)),
               secondary_clusters=cl, corners=cvals, corner_classes=sorted(ccls), bracket_dependent=len(ccls) > 1, cls=cls,
               variant_law=dict(D=dIMF(LMR, LAWPARS[f]), F1=law_ev["F1"], label=law_lab, cls=law_cls),
               variant_blue=dict(D_blue=D_blue, F1=blue_ev["F1"], F2=blue_ev["F2"], se2=blue_ev["se2"], z_cells=blue_ev["z_cells"], cls=blue_cls),
               variant_dwarfs_unclipped=dict(F0=F0dw, change=F0dw - v["F0"], cls=overall([lab], rot_ok and not dw_broken, (F0dw - v["F0"]) >= THR)),
               reported_zero_slope=dict(d0=d0, F1=zs["F1"], F2=zs["F2"], split_change=(zs["F1"] - zs["F2"]) - (base["F1"] - base["F2"])),
               posthoc_sluggs_ceiling=dict(note="post hoc 2026-10-20, no class weight: Delta_IMF = log10(S/C) - 0.120 (AUDIT_SLUGGS: under the law a Salpeter mass over-predicts the inner JAM mass by a median 0.120 dex)",
                                           D=d_sl, F1=sl_ev["F1"], removed_frac=(v["F1"] - sl_ev["F1"]) / v["F1"], label=grade_target(v["F1"], sl_ev["F1"]), z_cells=sl_ev["z_cells"]))
    R5["byfoot"][f] = rec
    P(f"  [{f:9s}] F1 {v['F1']:+.3f} -> {prim['F1']:+.3f} (dex {dex(v['F1']):+.3f} -> {dex(prim['F1']):+.3f}; removed {rec['target_F1']['removed_frac'] * 100:.0f}%) {lab}"
      f" => {cls}{'  [BRACKET-DEPENDENT: ' + ', '.join(sorted(ccls)) + ']' if len(ccls) > 1 else ''}")
    P(f"              split cells z {base['z_cells']:+.2f} -> {prim['z_cells']:+.2f};  CFG850 window A_red {w0['A_red']:.3f} -> {w1['A_red']:.3f} (A_blue {w1['A_blue']:.3f}), "
      f"z_colour {w0['z_colour']:+.2f} -> {w1['z_colour']:+.2f}, z_sersic {w0['z_sersic']:+.2f} -> {w1['z_sersic']:+.2f};  IMF alone (no +0.123): F1 {alone_m:+.3f}, A_red {wa['A_red']:.3f}")
    P(f"              CFG851 law after: b {c851['b']:.3f} ({c851['b_lo']:.3f}-{c851['b_hi']:.3f}), log g_dagger {c851['lgd']:.2f};  R5-law F1 {law_ev['F1']:+.3f} -> {law_cls};  "
      f"R5-blue F1 {blue_ev['F1']:+.3f} F2 {blue_ev['F2']:+.3f} -> {blue_cls};  dwarfs unclipped F0 {v['F0']:+.3f} -> {F0dw:+.3f}")
    P(f"              clusters (CFG922 bound): " + "; ".join(f"sigma {int(k)}: alpha_Chab {x['alpha_chab']:.3f}, f_m {x['f_m']:.4f}, removal <= {x['bound']:.4f} ({x['label']})" for k, x in cl.items())
      + f";  zero-slope (reported): split change {rec['reported_zero_slope']['split_change']:+.4f}")
    P(f"              [post-hoc, no class weight] SLUGGS ceiling Delta {d_sl:+.3f}: F1 {sl_ev['F1']:+.3f} (removed {rec['posthoc_sluggs_ceiling']['removed_frac'] * 100:.0f}%) "
      f"{rec['posthoc_sluggs_ceiling']['label']}; split cells z {sl_ev['z_cells']:+.2f}")
RES["R5"] = R5
if MUT == "imf0":
    mx = max(max(abs(R5["byfoot"][f]["target_F1"]["res"] - OBS[f][0]["F1"]), max(abs(x["bound"]) for x in R5["byfoot"][f]["secondary_clusters"].values()),
                 abs(R5["byfoot"][f]["dwarfs"]["unclipped_change"])) for f in FOOTS)
    bites = mx <= 1e-12; RES["mutate_imf0"] = dict(max_abs_change=mx, bites=bites)
    P(f"\n  MUTATE imf0: max |change| (F1, cluster bound, dwarfs) = {mx:.1e} -> {'BITES (effect removed)' if bites else 'DOES NOT BITE'}")
    finish(1 if bites else 0)

# =====================================================================================================================  R6 lensing estimator
P("\n=== R6 lensing estimator (B21 Eq. 7: g_obs = 4 G DeltaSigma; g_bar = G M_b / R^2), QUMOND law, isotropic stack")
def beta_arrays(model, M, Re, gbs, a0, rt=None, prof_cache=None):
    """beta_conv and beta_full at the B21 points gbs for a lens model"""
    if model == "round":
        Mf = M_hern(M, Re / 1.8153, a0); rf = numderiv(Mf); q2max = 0.0
    elif model == "flat":
        pr = prof_cache if prof_cache is not None else disc_profile(M, Re / 1.678, a0); Mf, rf = pr["M"], pr["rho"]
        Rw = np.sqrt(GC * M / gbs); sel = (RGRID >= 0.5 * Rw.min()) & (RGRID <= 2 * Rw.max()); q2max = float(np.max(np.abs(pr["q2"][sel])))
        Q2PTS.append(np.interp(np.log(Rw), np.log(RGRID), pr["q2"]))                     # post hoc: q2 at the window points themselves
    elif model == "pm":
        Mf = M_pm(M, a0); rf = numderiv(Mf); q2max = 0.0
    bc, bf = [], []
    for g in gbs:
        R = math.sqrt(GC * M / g); ds = esd(R, Mf, rf, rt); g4 = 4 * GC * ds
        bc.append(g4 / (GC * float(Mf(np.array([R]))[0]) / R ** 2)); bf.append(g4 / (g * float(nu_e(g / a0))))
    return np.array(bc), np.array(bf), q2max
def class_val(Sf, cl, beta):
    Ls = Sf["lens"][cl]; cells = np.array([math.log(float(w @ (Ls["gl"][Sx] * beta[Sx]))) for Sx, w in Ls["W"]]); return float(Sf["ops"][cl]["w"] @ cells)
R6 = {}; Q2PTS = []
RTS = {"none": None, "3 Mpc": 3000.0, "1 Mpc": 1000.0}
for f in FOOTS:
    v, se = OBS[f]; Sf = S[f]; a0 = A0[f]; R6[f] = {}
    gLS, gLD = Sf["lens"]["LS"]["gbs"], Sf["lens"]["LD"]["gbs"]
    assert np.min(np.sqrt(GC * 10 ** (LM_BLUE - 0.2) / gLD.max())) >= RGRID[0], "window radius below the disc grid"
    prof = {}
    for dmf in (-0.2, 0.0, 0.2):
        lmf = LM_BLUE + dmf; prof[dmf] = disc_profile(10 ** lmf, Re_flat(lmf) / 1.678, a0) if MUT != "geom" else None
    for rtn, rt in RTS.items():
        out = {}
        for dmr in (-0.2, 0.0, 0.2):
            for dmf in (-0.2, 0.0, 0.2):
                lmr, lmf = LMR + dmr, LM_BLUE + dmf; Mr, Mfl = 10 ** lmr, 10 ** lmf
                bcLS, bfLS, _ = beta_arrays("round", Mr, Re_round(lmr), gLS, a0, rt)
                bcLDr, bfLDr, _ = beta_arrays("round", Mr, Re_round(lmr), gLD, a0, rt)          # reference: round model at the n<2 points
                if MUT == "geom":
                    bcLD, bfLD, q2m = beta_arrays("round", Mr, Re_round(lmr), gLD, a0, rt)
                else:
                    bcLD, bfLD, q2m = beta_arrays("flat", Mfl, Re_flat(lmf), gLD, a0, rt, prof_cache=prof[dmf])
                rec = {}
                for kind, bLS, bLD, bLDr in (("conv", bcLS, bcLD, bcLDr), ("full", bfLS, bfLD, bfLDr)):
                    F1b, F2b, F2br = class_val(Sf, "LS", bLS), class_val(Sf, "LD", bLD), class_val(Sf, "LD", bLDr)
                    dest = F1b - F2b; Eo = v["F1"] - v["F2"]; Er = Eo - dest
                    rot_ok = abs(v["F2"] - F2b) < 2 * se["F2"] and abs(F2b) < THR
                    lab = grade_target(Eo, Er); cls = overall([lab], rot_ok, abs(F2b) >= THR)
                    rec[kind] = dict(F1_beta=F1b, F2_beta=F2b, delta_est=dest, delta_samp=F1b - F2br, delta_geom=F2br - F2b, E_obs=Eo, E_res=Er,
                                     removed_frac=dest / Eo, label=lab, rot_ok=rot_ok, cls=cls,
                                     beta_LS_range=[float(bLS.min()), float(bLS.max())], beta_LD_range=[float(bLD.min()), float(bLD.max())])
                rec["q2max_flat"] = q2m; rec["orientation_bound"] = 3 * q2m
                if MUT != "geom":
                    q2p = Q2PTS[-1]; wq = np.zeros(len(gLD))
                    for (Sx, w_), wc in zip(Sf["lens"]["LD"]["W"], Sf["ops"]["LD"]["w"]):
                        wq[Sx] += wc * np.abs(w_ * Sf["lens"]["LD"]["gl"][Sx])
                    rec["posthoc_q2_window"] = dict(note="post hoc 2026-10-20, no class weight: disc q2 at the n<2 window points (R = sqrt(G M / g_bar))",
                                                    R_kpc=np.sqrt(GC * Mfl / gLD).tolist(), q2=q2p.tolist(), weighted_mean_abs_q2=float(np.sum(wq * np.abs(q2p)) / np.sum(wq)),
                                                    max_abs_q2=float(np.max(np.abs(q2p))))
                out[f"{dmr:+.1f}|{dmf:+.1f}"] = rec
        prim = out["+0.0|+0.0"]
        R6[f][rtn] = dict(primary=prim, corners=out, corner_classes_conv=sorted({x["conv"]["cls"] for x in out.values()}),
                          corner_classes_full=sorted({x["full"]["cls"] for x in out.values()}),
                          max_abs_delta_conv=max(abs(x["conv"]["delta_est"]) for x in out.values()), max_abs_delta_full=max(abs(x["full"]["delta_est"]) for x in out.values()))
        pc, pf = prim["conv"], prim["full"]
        P(f"  [{f:9s}] truncation {rtn:6s}: conv  beta n>2 {pc['beta_LS_range'][0]:.4f}-{pc['beta_LS_range'][1]:.4f}, n<2 {pc['beta_LD_range'][0]:.4f}-{pc['beta_LD_range'][1]:.4f};"
          f" Delta_est {pc['delta_est']:+.4f} (samp {pc['delta_samp']:+.4f}, geom {pc['delta_geom']:+.2e}) vs E_obs {pc['E_obs']:+.3f} -> {pc['label']} => {pc['cls']}"
          f"  [corners: {', '.join(R6[f][rtn]['corner_classes_conv'])}; max |Delta| {R6[f][rtn]['max_abs_delta_conv']:.4f}]")
        P(f"              full  beta n>2 {pf['beta_LS_range'][0]:.4f}-{pf['beta_LS_range'][1]:.4f}, n<2 {pf['beta_LD_range'][0]:.4f}-{pf['beta_LD_range'][1]:.4f};"
          f" Delta_est {pf['delta_est']:+.4f} (samp {pf['delta_samp']:+.4f}, geom {pf['delta_geom']:+.2e}) -> {pf['label']} => {pf['cls']}; F2 bias {pf['F2_beta']:+.4f};"
          f" orientation bound {prim['orientation_bound']:.1e}  [corners: {', '.join(R6[f][rtn]['corner_classes_full'])}]")
        if "posthoc_q2_window" in prim:
            qq = prim["posthoc_q2_window"]
            P(f"              [post-hoc, no class weight] disc q2 at the n<2 window points: R {min(qq['R_kpc']):.0f}-{max(qq['R_kpc']):.0f} kpc, max |q2| {qq['max_abs_q2']:.3f}, "
              f"class-weighted mean |q2| {qq['weighted_mean_abs_q2']:.4f}")
    P(f"  [{f}] [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
RES["R6"] = R6
if MUT == "geom":
    mg = max(abs(R6[f][rtn]["corners"][k][kind]["delta_geom"]) for f in FOOTS for rtn in RTS for k in R6[f][rtn]["corners"] for kind in ("conv", "full"))
    bites = mg <= 1e-12; RES["mutate_geom"] = dict(max_abs_delta_geom=mg, bites=bites)
    P(f"\n  MUTATE geom: max |Delta_geom| = {mg:.1e} -> {'BITES (geometry effect removed; Delta_samp unchanged)' if bites else 'DOES NOT BITE'}")
    finish(1 if bites else 0)

# =====================================================================================================================  summary
P("\n=== SUMMARY (class per reframing and footing; ln units, dex = ln/2.3026)")
SUMM = {}
for f in FOOTS:
    SUMM[f] = dict(R4={law: R4[f][law]["cls"] + (" [BRACKET-DEPENDENT]" if R4[f][law]["bracket_dependent"] else "") for law in LAWS},
                   R5=R5["byfoot"][f]["cls"] + (" [BRACKET-DEPENDENT]" if R5["byfoot"][f]["bracket_dependent"] else ""),
                   R5_secondary_clusters=R5["byfoot"][f]["secondary_clusters"][300.0]["label"],
                   R6_conv=R6[f]["none"]["primary"]["conv"]["cls"], R6_full=R6[f]["none"]["primary"]["full"]["cls"])
    P(f"  [{f}] R4: " + "; ".join(f"{k} {x}" for k, x in SUMM[f]["R4"].items()))
    P(f"  [{f}] R5 (red lenses): {SUMM[f]['R5']};  clusters (secondary): {SUMM[f]['R5_secondary_clusters']};  R6 conversion: {SUMM[f]['R6_conv']};  R6 full estimator: {SUMM[f]['R6_full']}")
RES["summary"] = SUMM
P("\n  kappa = 1/2 FITTED; footings never pooled; cold energy, not a particle; not theory closed; nothing here says the data favour the framework.")
P(f"  [{time.time() - T0:.0f} s, peak {rss_mb():.0f} MB]")
finish(0)
