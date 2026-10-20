"""CFG936 -- systems below the law (Lelli+15 tidal dwarfs; NGC 1052-DF2/DF4).
Part A: score CFG930's SEALED S1 ("tidal dwarfs show zero excess"; seal cbb3b9888, sha256 57b1141e...) with the seal's estimator.
Part B: can the framework put these systems below its own law without an EFE?  Route (i) supply, route (ii) settling clock
(CFG763), route (iii) EFE as a declared contrast (not a framework route).
Criteria: FROZEN_CRITERIA.md (71d010099, committed alone before this script and before any number of this lane).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg936.py
      CFG936_MODE=K | MUTATE_onlaw | MUTATE_plus04 | MUTATE_fullsupply | MUTATE_oldclock   (outputs named by mode)
Inputs (read only): Lelli+15 TDG tables (real_research/data/tidal_dwarfs, real_research/data/tdg); CFG441 Arp 72c; CFG657's code
(exec'd read-only up to its run section: GAL, HOSTS, PRIMARY, BRACKET, capture, zf); CFG933/CFG931/CFG763/CFG768/CFG7 committed
JSON; CFG804's census slice; CFG4_common (nu_mono, A0) for the CFG763 reproduction.  Nothing downloaded; one core; seconds.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, re, csv, json, math, time, hashlib, resource, contextlib, builtins, warnings
import numpy as np
from scipy.stats import chi2 as CHI2

T0 = time.time()
_REAL_OPEN = builtins.open
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG936_MODE", "MAIN") or "MAIN"
MODES = ("MAIN", "K", "MUTATE_onlaw", "MUTATE_plus04", "MUTATE_fullsupply", "MUTATE_oldclock")
assert MODE in MODES, f"CFG936_MODE must be one of {MODES}"
SUF = "" if MODE == "MAIN" else "_" + MODE
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def RJ(*p):
    with _REAL_OPEN(os.path.join(LANES, *p)) as fh: return json.load(fh)
def RT(*p):
    with _REAL_OPEN(os.path.join(REPO, *p)) as fh: return fh.read()
RES = dict(lane="CFG936", criteria="71d010099", seal_scored="CFG930 S1 (cbb3b9888, sha256 57b1141e...)", mode=MODE, checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def jdef(o):
    if hasattr(o, "item"): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
def finish(code):
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_mb"] = round(rss_mb(), 1); RES["exit_code"] = code
    P(f"\n  done [{time.time() - T0:.1f} s, peak RSS {rss_mb():.0f} MB], exit {code}.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    with _REAL_OPEN(os.path.join(HERE, f"cfg936_results{SUF}.json"), "w") as fh: json.dump(RES, fh, indent=1, default=jdef)
    with _REAL_OPEN(os.path.join(HERE, f"cfg936{SUF}.out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
    sys.exit(code)

# ---------------------------------------------------------------------------------------------------- read-only exec helper
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG936 refuses to write {file!r} from re-executed committed code")
    return _REAL_OPEN(file, mode, *a, **k)
class _Exit(Exception): pass
def _exit(code=0): raise _Exit(code)
def sandbox_exec(path, src, name, extra=None):
    ns = {"__file__": path, "__name__": name}; ns.update(extra or {}); buf = io.StringIO(); err = None
    old_open, old_exit = builtins.open, sys.exit
    builtins.open = _ro_open; sys.exit = _exit
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(src, path, "exec"), ns)
    except BaseException as e:                       # noqa: BLE001 -- reported as a K failure
        err = f"{type(e).__name__}: {e}"
    finally:
        builtins.open = old_open; sys.exit = old_exit
    return ns, buf.getvalue(), err

FOOTS = ("canonical", "alt"); A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; LN10 = math.log(10.0)
G, MSUN, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16          # CFG931 / CFG933 constants
RATIO = 5.364
def nu_e(y):
    y = np.maximum(np.asarray(y, float), 1e-15); return 1.0 / (-np.expm1(-np.sqrt(y)))
def nu_s(y):
    y = np.maximum(np.asarray(y, float), 1e-15); return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))
KERN = {"nu_e": nu_e, "nu_simple": nu_s}

P("CFG936  systems below the law: CFG930 sealed S1 on the Lelli+15 TDGs; can the framework put TDGs and NGC 1052-DF2/DF4 below its law without an EFE?"
  + ("" if MODE == "MAIN" else f"   [{MODE}]"))
P("  criteria 71d010099; kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; EFE-free framework numbers (CL-AR, CFG925 R3)")

# ====================================================================================================================  data
TDG = []
for r in csv.DictReader(_REAL_OPEN(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))):
    f = lambda k: float(r[k])
    TDG.append(dict(name=r["object"].replace(" ", ""), V=f("V_circ_kms"), eV=f("e_V_circ_kms"), M=f("M_bar_1e8") * 1e8, eM=f("e_M_bar_1e8") * 1e8,
                    R=f("R_out_kpc"), eR=f("e_R_out_kpc"), Ms=f("M_star_1e8") * 1e8, Mmol=f("M_mol_1e8") * 1e8, Matom=f("M_atom_1e8") * 1e8,
                    LK=f("host_LK_1e10Lsun") * 1e10, Dp=f("D_p_kpc"), t=f("tmerg_over_torb") * f("t_orb_Gyr"),
                    et=f("tmerg_over_torb") * f("e_t_orb_Gyr"), torb=f("t_orb_Gyr"), Mdyn_over_Mbar=f("Mdyn_over_Mbar")))
TD931 = list(csv.DictReader(l for l in _REAL_OPEN(os.path.join(REPO, "real_research", "data", "tdg", "lelli2015_tdgs.csv")) if not l.startswith("#")))
ARP = []
for r in csv.DictReader(_REAL_OPEN(os.path.join(LANES, "CFG441_old_tdgs_tidal_origin", "data", "tierB_arp72c.csv"))):
    f = lambda k: float(r[k])
    ARP.append(dict(name=r["object"], V=f("V_circ_kms"), eV=0.5 * (f("e_V_circ_up") + f("e_V_circ_lo")), M=f("M_bar_1e8") * 1e8,
                    eM=f("e_M_bar_1e8") * 1e8, R=f("R_out_kpc"), eR=f("e_R_out_kpc"), t=f("age_Myr") / 1e3, et=f("e_age_Myr") / 1e3))

# CFG657's code, exec'd read-only up to its run section (exactly as cfg768.py does)
F657 = os.path.join(LANES, "CFG657_trail_capture_rule", "cfg657_capture.py")
with _REAL_OPEN(F657) as _fh: s657 = _fh.read()
s657 = s657[:s657.index("\nlines = []")]
_oldm = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
N657, _o657, e657 = sandbox_exec(F657, s657, "cfg657_ro")
if _oldm is None: os.environ.pop("MUTATE", None)
else: os.environ["MUTATE"] = _oldm
GAL, HOSTS, PRIM657, BRK657 = N657["GAL"], N657["HOSTS"], N657["PRIMARY"], N657["BRACKET"]
capture, zf, angsep, host_halo = N657["capture"], N657["zf"], N657["angsep"], N657["host_halo"]
GK657, KPCM657, LN_EDGE = N657["GK"], N657["KPC_M"], N657["LN_EDGE"]
DFS = ("DF2", "DF4")
S933 = RT("campaign_fresh_gravity", "CFG933_udg_sealed_test", "cfg933.py")
_m = re.search(r'SEC = \{"DF2": \(([0-9.]+), ([0-9.]+), ([0-9.]+)\), "DF4": \(([0-9.]+), ([0-9.]+), ([0-9.]+)\)\}', S933)
SEC = {"DF2": tuple(float(_m.group(i)) for i in (1, 2, 3)), "DF4": tuple(float(_m.group(i)) for i in (4, 5, 6))}

# CFG804 census slice (verbatim) for the catchment N
S804 = RT("campaign_fresh_gravity", "CFG804_catchment_supply_derived", "cfg804.py")
_a, _b = S804.index("def fret_of(lM):"), S804.index("def N_of(logMb):")
_c = S804.index("return 1 / f, lMta", _b) + len("return 1 / f, lMta")
N804, _, e804 = sandbox_exec(os.path.join(LANES, "CFG804_catchment_supply_derived", "cfg804.py"), S804[_a:_c], "cfg804_ro",
                             {"math": math, "MUT": False, "FB": 1 / (1 + RATIO)})
N_of = N804["N_of"]

# ====================================================================================================================  estimators
# ---- class T (CFG931 INFO path): single point at R_out; residual vs a route's nu_eff
def t_gb(M, R): return G * M * MSUN / (R * KPC) ** 2
def t_go(V, R): return (V * 1e3) ** 2 / (R * KPC)
def r_law(o, M, R, a0, nu, n, gb): return n
def r_newton(o, M, R, a0, nu, n, gb): return 1.0
def t_resid(o, a0, nu, route, V, M, R):
    gb = t_gb(M, R); n = float(nu(gb / a0)); ne = route(o, M, R, a0, nu, n, gb)
    return math.log10(t_go(V, R) / (gb * ne)), n, ne, gb
def t_point(o, a0, nu, route, V=None, M=None, verr_only=False):
    V = o["V"] if V is None else V; M = o["M"] if M is None else M; R = o["R"]
    r0, n, ne, gb = t_resid(o, a0, nu, route, V, M, R)
    sV = 2 * o["eV"] / (V * LN10)
    dM = (t_resid(o, a0, nu, route, V, M * 1.01, R)[0] - r0) / 0.01 * o["eM"] / o["M"]
    dR = (t_resid(o, a0, nu, route, V, M, R * 1.01)[0] - r0) / 0.01 * o["eR"] / R
    s = sV if verr_only else math.sqrt(sV ** 2 + dM ** 2 + dR ** 2)
    return dict(name=o["name"], r=r0, s=s, nu=n, nueff=ne, f=(ne - 1) / (n - 1), lgbar=math.log10(gb),
                Delta_obs=math.log10(t_go(V, R) / (gb * n)), Delta_pred=math.log10(ne / n), z=r0 / s)

# ---- class U (CFG933's sealed estimator)
def u_base(g, a0, nu, Ms=None):
    Ms = g["Ms"] if Ms is None else Ms
    r12 = (4.0 / 3.0) * g["Re"] * 1e3 * PC; gb = G * (Ms / 2) * MSUN / r12 ** 2; n = float(nu(gb / a0))
    return r12, gb, n, math.sqrt(r12 * gb * n / 3) / 1e3
def u_point(name, a0, nu, route, sig=None):
    g = GAL[name]; r12, gb, n, sl = u_base(g, a0, nu)
    s, up, lo = g["obs"] if sig is None else sig
    ne = route(name, gb, n, a0)
    Ep = math.log(ne / n); sp = sl * math.exp(Ep / 2); Eo = 2 * math.log(s / sl)
    e = lo if s > sp else up; sE = 2 * e / s
    return dict(name=name, r=Eo - Ep, s=sE, E_obs=Eo, E_pred=Ep, sE=sE, z=(Eo - Ep) / sE, nu=n, nueff=ne, f=(ne - 1) / (n - 1),
                sigma_law=sl, sigma_pred=sp, log_gbar=math.log10(gb))
def u_point_zf(name, foot, f):
    """variant: CFG657's zf form (nu_mono, M* error on sigma_pred; CFG655): residual and error in km/s"""
    g = GAL[name]; s, up, lo = g["obs"]; sp, ep = N657["sig_pred"](name, foot, f)
    e = up if sp > s else lo
    return dict(name=name, r=s - sp, s=math.sqrt(e * e + ep * ep), z=zf(name, foot, f))

# ---- class rule (criteria 5.1)
def stats(pts):
    r = np.array([p["r"] for p in pts]); s = np.array([p["s"] for p in pts]); n = len(r)
    t_sd = float(np.std(r, ddof=1) / math.sqrt(n)); t_me = float(math.sqrt(np.sum(s ** 2)) / n)
    se = max(t_sd, t_me); c2 = float(np.sum((r / s) ** 2)); p = float(CHI2.sf(c2, n))
    return dict(n=n, rbar=float(np.mean(r)), se=se, se_scatter=t_sd, se_meas=t_me, chi2=c2, p=p, z_mean=float(np.mean(r)) / se)
def basic_class(st, rlaw):
    if abs(st["rbar"]) < 2 * st["se"] and st["p"] >= 0.05: return "EXPLAINS"
    if abs(st["rbar"]) <= 0.5 * abs(rlaw): return "PARTIAL"
    return "FAILS"
def route_class(prim, corners, variants, rlaw):
    """prim: stats dict; corners/variants: {label: stats}.  PARTIAL also if EXPLAINS at >= 1 declared corner."""
    c0 = basic_class(prim, rlaw)
    cc = {k: basic_class(v, rlaw) for k, v in corners.items()}
    vc = {k: basic_class(v, rl) for k, (v, rl) in variants.items()}     # each variant carries its own law reference (same units)
    cls = c0
    if c0 == "FAILS" and any(v == "EXPLAINS" for v in cc.values()): cls = "PARTIAL"
    diff = [k for k, v in {**cc, **vc}.items() if v != cls]
    return dict(cls=cls, primary_basic=c0, qualifier="FRAGILE" if diff else "ROBUST", differing=diff, n_corners=len(cc), n_variants=len(vc),
                corner_classes=cc, variant_classes=vc)
def s1_class(mean, se):
    if mean > 2 * se: return "S1 FAILS"
    if mean >= -2 * se: return "S1 HOLDS"
    return "NOT DIAGNOSTIC (BELOW THE LAW)"
def fmt(st): return f"rbar {st['rbar']:+.3f} +- {st['se']:.3f} (z {st['z_mean']:+.2f}); chi2 {st['chi2']:.2f}/{st['n']} (p {st['p']:.3g})"

# ---- route ingredients
def mk_clock_T(tau, agefn):
    def route(o, M, R, a0, nu, n, gb):
        f = 1.0 - math.exp(-agefn(o) / tau); return 1.0 + f * (n - 1.0)
    return route
def mk_clock_U(tau, agefn):
    def route(name, gb, n, a0):
        f = 1.0 - math.exp(-agefn(GAL[name]) / tau); return 1.0 + f * (n - 1.0)
    return route
def mk_F_T(Rfac, hfac, k):
    """recent-catchment upper bound: CFG657 channel F with P_F = 1, applied to TDG inputs (criteria 5.2 i-B)"""
    def route(o, M, R, a0, nu, n, gb):
        a0k = a0 * KPCM657 / 1e6
        Vf, _ = host_halo(0.6 * o["LK"] * hfac, a0k)
        Rr = max(Rfac * o["Dp"], 1.0)
        rho = k * Vf ** 2 / (4 * math.pi * GK657 * Rr ** 2)
        Mgin = Vf ** 2 * Rr / GK657
        RJ_ = Rr * (n * M / (2 * Mgin)) ** (1.0 / 3.0)
        rstar = math.sqrt(GK657 * M / a0k) / LN_EDGE
        MF = rho * (4 * math.pi / 3) * min(RJ_, rstar) ** 3
        f = min(1.0, MF / ((n - 1.0) * M)); return 1.0 + f * (n - 1.0)
    return route
def mk_supply_T(mult_fn):
    def route(o, M, R, a0, nu, n, gb):
        f = min(1.0, mult_fn(M) / (n - 1.0)); return 1.0 + f * (n - 1.0)
    return route
def mk_supply_U(mult_fn):
    def route(name, gb, n, a0):
        Mb = GAL[name]["Ms"] / 2; f = min(1.0, mult_fn(Mb) / (n - 1.0)); return 1.0 + f * (n - 1.0)
    return route
def mk_fixed_U(fdict):
    def route(name, gb, n, a0): return 1.0 + fdict[name] * (n - 1.0)
    return route
def efe_nueff(gNi, gNe, a0, nu):
    if gNe <= 0: return float(nu(gNi / a0))
    ai = gNi * float(nu((gNi + gNe) / a0)) + gNe * (float(nu((gNi + gNe) / a0)) - float(nu(gNe / a0)))
    return ai / gNi
def mk_efe_T(hfac):
    def route(o, M, R, a0, nu, n, gb):
        gNe = G * 0.6 * o["LK"] * hfac * MSUN / (o["Dp"] * KPC) ** 2; return efe_nueff(gb, gNe, a0, nu)
    return route
def u_hosts_gNe(name, Mg=1e11, M35=5e9, only1052=False, Rmul=1.0):
    g = GAL[name]; tot = 0.0
    for h, Mh in (("NGC1052", Mg), ("NGC1035", M35)):
        if only1052 and h != "NGC1052": continue
        Rk = Rmul * g["D"] * 1000 * angsep(g["pos"], HOSTS[h])
        tot += G * Mh * MSUN / (Rk * KPC) ** 2
    return tot
def mk_efe_U(**kw):
    def route(name, gb, n, a0): return efe_nueff(gb, u_hosts_gNe(name, **kw), a0, nu_e)
    return route
def fixed_gne_U(gNe):
    def route(name, gb, n, a0): return efe_nueff(gb, gNe, a0, nu_e)
    return route
def law_U(name, gb, n, a0): return n
def newton_U(name, gb, n, a0): return 1.0

# ---- CFG763's machinery (re-implemented; K3 must reproduce cfg763_results.json exactly)
G_KPC763, KPC_M763 = 4.30091727e-6, 3.0856775814913673e19
ACC763 = 1e6 / KPC_M763
TAUS = 10 ** np.round(np.arange(-2, 2.0001, 0.01), 2)
OBJ763 = [dict(name=o["name"], V=o["V"], eV=o["eV"], M=o["M"], eM=o["eM"], R=o["R"], eR=o["eR"], Mhost=0.6 * o["LK"], Dp=o["Dp"],
               t=o["t"], et=o["et"]) for o in TDG] + [dict(name=a["name"], V=a["V"], eV=a["eV"], M=a["M"], eM=a["eM"], R=a["R"],
                                                           eR=a["eR"], Mhost=None, Dp=None, t=a["t"], et=a["et"]) for a in ARP]
def clock763(a0, NU, efe=True, vobs_law=False):
    def v_newton(M, R): return math.sqrt(G_KPC763 * M / R)
    def v_law(M, R, Mhost=None, Dp=None):
        gNi = G_KPC763 * M / R ** 2 * ACC763
        if Mhost is None or not efe:
            ai = gNi * float(NU(gNi / a0))
        else:
            gNe = G_KPC763 * Mhost / Dp ** 2 * ACC763
            ai = gNi * float(NU((gNi + gNe) / a0)) + gNe * (float(NU((gNi + gNe) / a0)) - float(NU(gNe / a0)))
        return math.sqrt(ai / ACC763 * R)
    def pred_err(fn, M, eM, R, eR):
        v0 = fn(M, R); dm = (fn(M * 1.01, R) - v0) / (0.01 * M) * eM; dr = (fn(M, R * 1.01) - v0) / (0.01 * R) * eR
        return v0, math.hypot(dm, dr)
    pre = []
    for o in OBJ763:
        vn, en = pred_err(v_newton, o["M"], o["eM"], o["R"], o["eR"])
        vl, el = pred_err(lambda M, R, o=o: v_law(M, R, o["Mhost"], o["Dp"]), o["M"], o["eM"], o["R"], o["eR"])
        pre.append((vn, en, vl, el))
    vobs = [p[2] if vobs_law else o["V"] for o, p in zip(OBJ763, pre)]
    def chi2(tau, ages):
        tot = 0.0
        for o, (vn, en, vl, el), v, t in zip(OBJ763, pre, vobs, ages):
            fr = 1.0 if tau == 0 else (0.0 if math.isinf(tau) else 1 - math.exp(-t / tau))
            vm = math.sqrt(vn ** 2 + fr * (vl ** 2 - vn ** 2)); em = en + fr * (el - en)
            tot += (v - vm) ** 2 / (o["eV"] ** 2 + em ** 2)
        return tot
    lo_age = [max(o["t"] - o["et"], 0.05) for o in OBJ763]; nom_age = [o["t"] for o in OBJ763]
    out = dict(chi2_tau0=chi2(0.0, lo_age), chi2_tauinf=chi2(math.inf, lo_age))
    for lab, ages in (("lower_1sigma_ages", lo_age), ("nominal_ages", nom_age)):
        ch = np.array([chi2(t, ages) for t in TAUS]); cmin = min(ch.min(), chi2(math.inf, ages))
        ok = np.where(ch <= cmin + 3.84)[0]
        out[lab] = dict(tau_min95_Gyr=float(TAUS[ok[0]]) if ok.size else None, chi2_min=float(cmin), chi2_at_3p47=chi2(3.47, ages))
    return out

# ====================================================================================================================  K-stage
P("\n=== K-stage")
KOK = []
# K0 seal integrity + exec'd code health
_seal = os.path.join(LANES, "CFG930_energy_limited_settling", "SEALED_PREDICTIONS.md")
with _REAL_OPEN(_seal, "rb") as fh: h_seal = hashlib.sha256(fh.read()).hexdigest()
with _REAL_OPEN(os.path.join(LANES, "CFG930_energy_limited_settling", "SEALED_PREDICTIONS_SHA256.txt")) as fh: h_file = fh.read().split()[0]
s1_text = RT("campaign_fresh_gravity", "CFG930_energy_limited_settling", "SEALED_PREDICTIONS.md")
s1_ok = "A TDG sample (gas counted, the same estimator) with mean excess > 2 se above the law contradicts H-ELS." in s1_text
KOK.append(check("K0 CFG930 seal intact (sha256 == committed file, prefix 57b1141e) and S1 text present; CFG657 / CFG804 slices exec'd read-only without error",
                 h_seal == h_file and h_seal.startswith("57b1141e") and s1_ok and e657 is None and e804 is None,
                 f"sha256 {h_seal[:16]}...; S1 kill clause {'found' if s1_ok else 'MISSING'}; cfg657 {e657 or 'ok'}; cfg804 {e804 or 'ok'}"))
RES["seal_sha256"] = h_seal

# K1 CFG931's TDG INFO
R931 = RJ("CFG931_faint_rotator_discriminator", "cfg931_results.json")["info"]
k1d, k1m, k1id = [], {}, []
for f_ in FOOTS:
    rows = []
    for r in TD931:
        Rm = float(r["Rout"]) * KPC; gb = G * float(r["Mbar"]) * 1e8 * MSUN / Rm ** 2; go = (float(r["Vcirc"]) * 1e3) ** 2 / Rm
        rows.append(dict(name=r["name"], lgbar=math.log10(gb), Delta=math.log10(go / (gb * float(nu_e(gb / A0[f_])))),
                         sDelta=2 * float(r["eVcirc"]) / (float(r["Vcirc"]) * LN10)))
    ref = R931[f"TDG|{f_}"]
    for a, b in zip(rows, ref):
        assert a["name"] == b["name"]
        k1d += [abs(a[k] - b[k]) for k in ("lgbar", "Delta", "sDelta")]
    mine_T = [t_point(o, A0[f_], nu_e, r_law, verr_only=True) for o in TDG]
    refn = {b["name"]: b for b in ref}
    k1d += [abs(a["Delta_obs"] - refn[a["name"]]["Delta"]) for a in mine_T] + [abs(a["s"] - refn[a["name"]]["sDelta"]) for a in mine_T]
    k1m[f_] = (float(np.mean([x["Delta"] for x in rows])), float(np.mean([x["Delta"] for x in ref])))
by931 = {r["name"]: r for r in TD931}
for o in TDG:
    r = by931[o["name"]]
    k1id += [o["V"] == float(r["Vcirc"]), o["eV"] == float(r["eVcirc"]), abs(o["M"] - float(r["Mbar"]) * 1e8) < 1e-3,
             abs(o["eM"] - float(r["eMbar"]) * 1e8) < 1e-3, o["R"] == float(r["Rout"]), o["eR"] == float(r["eRout"]), o["Dp"] == float(r["Dp"])]
KOK.append(check("K1 CFG931's TDG INFO reproduced (per object lgbar, Delta, sDelta from the tdg/ CSV, and through this lane's class-T path from the "
                 "tidal_dwarfs/ CSV); the two CSVs agree on V, eV, M_bar, eM_bar, R_out, eR_out, D_p",
                 max(k1d) <= 1e-12 and all(k1id) and all(abs(a - b) <= 1e-12 for a, b in k1m.values()),
                 f"max |diff| {max(k1d):.1e}; means canonical {k1m['canonical'][0]:+.4f} (CFG931 {k1m['canonical'][1]:+.4f}), alt {k1m['alt'][0]:+.4f} "
                 f"(CFG931 {k1m['alt'][1]:+.4f}); CSV identity {sum(k1id)}/{len(k1id)}"))
RES["K1"] = dict(means=k1m, max_diff=max(k1d))

# K2 CFG933's DF2/DF4
R933 = RJ("CFG933_udg_sealed_test", "cfg933_results.json")
k2d, k2z = [], {}
mem = {m["name"]: m for m in R933["membership"]}
k2id = all(GAL[n]["Ms"] == mem["NGC1052-" + n]["Ms"] and GAL[n]["Re"] == mem["NGC1052-" + n]["Re"]
           and tuple(GAL[n]["obs"]) == (mem["NGC1052-" + n]["sig"], mem["NGC1052-" + n]["ep"], mem["NGC1052-" + n]["em"]) for n in DFS)
for f_ in FOOTS:
    pg = {x["name"]: x for x in R933["byfoot"][f_]["per_galaxy"]}; gz = {x["name"]: x for x in R933["byfoot"][f_]["primary"]["group_per_galaxy"]}
    for n in DFS:
        ref = pg["NGC1052-" + n]; Ep = ref["E_pred"]
        pt = u_point(n, A0[f_], nu_e, lambda name, gb, nn, a0, Ep=Ep: nn * math.exp(Ep))
        spi = abs(ref["E_pred_plus"] - ref["E_pred_minus"]) / 2
        z = (pt["E_obs"] - Ep) / math.hypot(pt["sE"], spi)
        k2d += [abs(pt["sigma_law"] - ref["sigma_law"]), abs(pt["E_obs"] - ref["E_obs"]), abs(pt["sE"] - ref["sE"]),
                abs(pt["log_gbar"] - ref["log_gbar"]), abs(pt["sigma_pred"] - ref["sigma_pred"]), abs(z - gz["NGC1052-" + n]["z"])]
        lawpt = u_point(n, A0[f_], nu_e, law_U)
        k2z[f"{n}|{f_}"] = dict(z_vs_P2=z, z_CFG933=gz["NGC1052-" + n]["z"], E_obs=pt["E_obs"], sE_law=lawpt["sE"], z_vs_bare_law=lawpt["z"],
                                sigma_law=pt["sigma_law"])
KOK.append(check("K2 CFG933's DF2/DF4 reproduced through this lane's class-U path (sigma_law, log g_bar, E_obs, sE, sigma_pred, z vs P2); GAL == CFG933 membership",
                 max(k2d) <= 1e-9 and k2id, f"max |diff| {max(k2d):.1e}; " + "; ".join(
                     f"{k}: E_obs {v['E_obs']:+.3f}, z vs P2 {v['z_vs_P2']:+.2f} (CFG933 {v['z_CFG933']:+.2f}), z vs bare law {v['z_vs_bare_law']:+.2f}"
                     for k, v in k2z.items())))
RES["K2"] = k2z

# K3 CFG763's clock bracket (with the 1-D EFE, nu_mono, CFG4_common.A0)
sys.path.insert(0, LANES)
import CFG4_common as C4   # noqa: E402  (read only: nu_mono, A0)
R763 = RJ("CFG763_formation_clock", "cfg763_results.json")
k3d, k3s = [], {}
for f_ in FOOTS:
    c = clock763(C4.A0[f_], C4.nu_mono, efe=True)
    for lab in ("lower_1sigma_ages", "nominal_ages"):
        k3d += [abs(c[lab]["tau_min95_Gyr"] - R763["numbers"][f_][lab]["tau_min95_Gyr"]), abs(c[lab]["chi2_min"] - R763["numbers"][f_][lab]["chi2_min"])]
    k3s[f_] = dict(tau_lo=c["lower_1sigma_ages"]["tau_min95_Gyr"], tau_nom=c["nominal_ages"]["tau_min95_Gyr"], chi2_tau0=c["chi2_tau0"], chi2_tauinf=c["chi2_tauinf"])
k3k1 = abs(k3s["canonical"]["chi2_tau0"] - 34.018) <= 1e-3 and abs(k3s["alt"]["chi2_tau0"] - 40.290) <= 1e-3 and all(abs(k3s[f_]["chi2_tauinf"] - 1.105) <= 1e-3 for f_ in FOOTS)
TAU_UP = -8.0 / math.log(0.1)
A0_DIFF = {f_: C4.A0[f_] - A0[f_] for f_ in FOOTS}       # AMENDMENT A1: reported only (CFG763 ran on CFG4_common's unrounded FP0 a0)
KOK.append(check("K3 CFG763's clock bracket reproduced (1-D EFE at nominal host, nu_mono, CFG4_common.A0, CFG763 error recipe and grid): tau_min,95 and "
                 "chi2_min at -1 sigma and nominal ages; CFG763 K1 chi2; upper bound -8/ln 0.1 -> 3.47",
                 max(k3d) <= 1e-9 and k3k1 and round(TAU_UP, 2) == 3.47,
                 f"max |diff| {max(k3d):.1e}; canonical tau_min {k3s['canonical']['tau_lo']:.4f} / {k3s['canonical']['tau_nom']:.4f} Gyr, alt "
                 f"{k3s['alt']['tau_lo']:.4f} / {k3s['alt']['tau_nom']:.4f}; chi2 tau->0 {k3s['canonical']['chi2_tau0']:.3f} / {k3s['alt']['chi2_tau0']:.3f}, "
                 f"tau->inf {k3s['canonical']['chi2_tauinf']:.3f}; upper {TAU_UP:.4f} Gyr; [A1] CFG4_common.A0 - rounded footing: canonical {A0_DIFF['canonical']:+.2e} "
                 f"(rel {A0_DIFF['canonical'] / A0['canonical']:+.1e}), alt {A0_DIFF['alt']:+.2e} (rel {A0_DIFF['alt'] / A0['alt']:+.1e})"))
TAU_MIN = {f_: R763["numbers"][f_]["lower_1sigma_ages"]["tau_min95_Gyr"] for f_ in FOOTS}
RES["K3"] = dict(mine=k3s, tau_upper=TAU_UP, tau_min_cfg763=TAU_MIN, A1_CFG4_common_A0_minus_rounded=A0_DIFF)

# K4 CFG768 Part A (alpha_P = 0) and Part B (universal clock) for DF2/DF4
R768 = RJ("CFG768_trail_alpha_and_clocks", "cfg768_results.json")
k4d, FCAP = [], {}
CORN657 = [(k, v) for k, (lo, hi) in BRK657.items() if k != "alpha" for v in (lo, hi)]
for f_ in FOOTS:
    FCAP[f_] = {}
    for n in DFS:
        prim = capture(n, f_, dict(PRIM657, alpha=0.0))["fcap"]
        vals = {f"{k}={v:g}": capture(n, f_, dict(PRIM657, alpha=0.0, **{k: v}))["fcap"] for k, v in CORN657}
        FCAP[f_][n] = dict(primary=prim, corners=vals)
        ref = R768["A"][f_]["f_cap_alpha0"][n]
        k4d += [abs(prim - ref["primary"]), abs(max([prim] + list(vals.values())) - ref["max"]), abs(min([prim] + list(vals.values())) - ref["min"])]
        age, eup, elo = GAL[n]["age"]; t = max(0.0, min(age - elo, 6.0)); fB = 1.0 - math.exp(-t / 3.47)
        rB = R768["B"][f_]["universal"]["rows"][n]
        k4d += [abs(fB - rB["f"]), abs(zf(n, f_, fB) - rB["Z_at_f"])]
KOK.append(check("K4 CFG768 reproduced via CFG657's capture()/zf exec'd read-only: f_cap(alpha 0) primary/min/max over the 16 one-at-a-time ends; "
                 "Part B universal f and Z_at_f (DF2, DF4, both footings)", max(k4d) <= 1e-9,
                 f"max |diff| {max(k4d):.1e}; f_cap primary canonical DF2 {FCAP['canonical']['DF2']['primary']:.2e}, DF4 {FCAP['canonical']['DF4']['primary']:.2e}"))

# K5 CFG7 C2 (Lelli Table 9 by eq. 4 at a0 1.25e-10, n = 1, 2), CFG7's constants
R7 = RJ("CFG7_tdg_fg041_results.json")["numbers"]["C2"]
TR = list(csv.DictReader(_REAL_OPEN(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))))
def nu_n(y, n):
    y = np.maximum(np.asarray(y, float), 1e-300); return (1.0 - np.exp(-y ** (n / 2.0))) ** (-1.0 / n)
def v_pred7(r, a0, nu, efe):
    Mb = float(r["M_bar_1e8"]) * 1e8; Ro = float(r["R_out_kpc"])
    gNi = G_KPC763 * Mb / Ro ** 2 * ACC763
    gNe = (G_KPC763 * 0.6 * float(r["host_LK_1e10Lsun"]) * 1e10 / float(r["D_p_kpc"]) ** 2 * ACC763) if efe else 0.0
    ai = gNi * nu((gNi + gNe) / a0) + (gNe * (nu((gNi + gNe) / a0) - nu(gNe / a0)) if efe else 0.0)
    return math.sqrt(ai / ACC763 * Ro)
di, de = [], []
for r in TR:
    for nn in (1, 2):
        nu = lambda y, nn=nn: nu_n(y, nn)
        di.append(abs(v_pred7(r, 1.25e-10, nu, False) - float(r[f"V_ISO{nn}_kms"]))); de.append(abs(v_pred7(r, 1.25e-10, nu, True) - float(r[f"V_EFE{nn}_kms"])))
KOK.append(check("K5 CFG7 C2 (Lelli+15 Table 9 from its eq. 4 at a0 1.25e-10, n = 1, 2) reproduced by this lane's EFE formula",
                 abs(max(di) - R7["max_dev_iso"]) <= 1e-9 and abs(max(de) - R7["max_dev_efe"]) <= 1e-9,
                 f"max |dV_ISO| {max(di):.10f} (CFG7 {R7['max_dev_iso']:.10f}); max |dV_EFE| {max(de):.10f} (CFG7 {R7['max_dev_efe']:.10f})"))

# K6 CFG804 census
KOK.append(check("K6 CFG804 census (verbatim slice): N_of(10.5) = 10", abs(N_of(10.5)[0] - 10.0) < 1e-9, f"N = {N_of(10.5)[0]:.6f}"))

# K7 limits
k7 = []
for f_ in FOOTS:
    for o in TDG:
        a = t_point(o, A0[f_], nu_e, r_law); b = t_point(o, A0[f_], nu_e, r_newton); c = t_point(o, A0[f_], nu_e, mk_efe_T(0.0))
        k7 += [abs(a["Delta_pred"]), abs(b["Delta_pred"] + math.log10(b["nu"])), abs(c["Delta_pred"])]
    for n in DFS:
        k7 += [abs(u_point(n, A0[f_], nu_e, law_U)["E_pred"]), abs(u_point(n, A0[f_], nu_e, fixed_gne_U(0.0))["E_pred"])]
KOK.append(check("K7 limits: f = 1 -> Delta_pred 0; f = 0 -> -log10 nu; EFE with M_host = 0 -> bare law (T and U)", max(k7) <= 1e-12, f"max {max(k7):.1e}"))

K_ALL = all(KOK); RES["K_all"] = K_ALL
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.1f} s, {rss_mb():.0f} MB]")
if not K_ALL:
    P("  A K-test failed: per criteria section 6 the lane stops; no class is reported."); finish(2)
if MODE == "K":
    P("  CFG936_MODE=K: K-stage only."); finish(0)

# ====================================================================================================================  Part A: S1
def s1_score(f_, nu=nu_e, Vfn=None, mmol=1.0, verr_only=False):
    a0 = A0[f_]
    def Mq(o, q):
        """M_bar with M_star x q and M_mol x mmol; components rescaled by M_bar/(sum of tabulated components) so q = 1, mmol = 1 is M_bar exactly"""
        k = o["M"] / (o["Matom"] + o["Ms"] + o["Mmol"])
        return k * (o["Matom"] + mmol * o["Mmol"] + q * o["Ms"])
    Vs = [None if Vfn is None else Vfn(o, a0, nu) for o in TDG]
    pts = [t_point(o, a0, nu, r_law, V=v, M=(o["M"] if mmol == 1.0 else Mq(o, 1.0)), verr_only=verr_only) for o, v in zip(TDG, Vs)]
    d = np.array([p["Delta_obs"] for p in pts]); s = np.array([p["s"] for p in pts]); n = len(d)
    mq = {}
    for q in (2.0, 0.5):
        mq[q] = float(np.mean([t_point(o, a0, nu, r_law, V=v, M=Mq(o, q))["Delta_obs"] for o, v in zip(TDG, Vs)]))
    floor = abs(mq[2.0] - mq[0.5]) / 2
    sd = float(np.std(d, ddof=1) / math.sqrt(n)); se = math.hypot(sd, floor)
    se_me = math.hypot(float(math.sqrt(np.sum(s ** 2)) / n), floor)
    med = float(np.median(d)); se_med = math.hypot(1.2533 * float(np.sqrt(np.mean((d - d.mean()) ** 2))) / math.sqrt(n), floor)
    return dict(mean=float(d.mean()), sd_over_sqrtn=sd, ups_floor=floor, se=se, cls=s1_class(float(d.mean()), se),
                alt_meas=dict(se=se_me, cls=s1_class(float(d.mean()), se_me)), alt_median=dict(median=med, se=se_med, cls=s1_class(med, se_med)),
                per_object=[dict(name=p["name"], Delta=p["Delta_obs"], sigma=p["s"], lgbar=p["lgbar"]) for p in pts], mean_ups2=mq[2.0], mean_ups_half=mq[0.5])

def V_plant(shift):
    def fn(o, a0, nu):
        gb = t_gb(o["M"], o["R"]); return math.sqrt(gb * float(nu(gb / a0)) * 10 ** shift * o["R"] * KPC) / 1e3
    return fn

DW_ALT = {"canonical": 0.856 / LN10, "alt": 0.765 / LN10}   # CFG919 DW class mean as reproduced in CFG931 K3 (criteria section 4)
if MODE in ("MUTATE_onlaw", "MUTATE_plus04"):
    sh = 0.0 if MODE == "MUTATE_onlaw" else 0.4; want = "S1 HOLDS" if MODE == "MUTATE_onlaw" else "S1 FAILS"
    P(f"\n=== {MODE}: TDG g_obs := g_law x 10^{sh} (V_circ replaced), S1 scored with the seal's estimator")
    ok = True; RES["S1_planted"] = {}
    for f_ in FOOTS:
        s = s1_score(f_, Vfn=V_plant(sh)); RES["S1_planted"][f_] = s
        ok &= s["cls"] == want
        P(f"  [{f_}] mean Delta {s['mean']:+.4f}, se {s['se']:.4f} (sd/sqrt n {s['sd_over_sqrtn']:.4f} (+) Ups floor {s['ups_floor']:.4f}) -> {s['cls']} (required {want})")
    RES["mutate_ok"] = bool(ok)
    P(f"  MUTATE {MODE}: {'BEHAVES' if ok else 'FAILS'}")
    finish(0 if ok else 1)

if MODE == "MUTATE_fullsupply":
    P("\n=== MUTATE_fullsupply: route (i) with M_sup = 5.364 N M_b,ap, N = 1/f_ret(M_ta) (CFG804 census) -> must give f = 1, no deficit")
    ok = True; RES["fullsupply"] = {}
    full = lambda M: RATIO * N_of(math.log10(M))[0]
    for f_ in FOOTS:
        tp = [t_point(o, A0[f_], nu_e, mk_supply_T(full)) for o in TDG]; up = [u_point(n, A0[f_], nu_e, mk_supply_U(full)) for n in DFS]
        mx = max([abs(p["Delta_pred"]) for p in tp] + [abs(p["E_pred"]) for p in up]); fmin = min([p["f"] for p in tp] + [p["f"] for p in up])
        Ns = sorted({round(N_of(math.log10(o["M"]))[0], 6) for o in TDG} | {round(N_of(math.log10(GAL[n]["Ms"] / 2))[0], 6) for n in DFS})
        ok &= mx < 1e-12 and fmin >= 1.0 - 1e-12
        RES["fullsupply"][f_] = dict(max_abs_pred=mx, f_min=fmin, N_values=Ns)
        P(f"  [{f_}] N values {Ns}; min f {fmin:.12f}; max |Delta_pred| / |E_pred| {mx:.1e}")
    RES["mutate_ok"] = bool(ok); P(f"  MUTATE fullsupply: {'BEHAVES (no deficit)' if ok else 'FAILS'}"); finish(0 if ok else 1)

if MODE == "MUTATE_oldclock":
    P("\n=== MUTATE_oldclock: route (ii) with every age = 13.0 Gyr at tau 3.47 -> |Delta_pred| < 0.02 dex (T), |E_pred| < 0.05 (U)")
    ok = True; RES["oldclock"] = {}
    for f_ in FOOTS:
        tp = [t_point(o, A0[f_], nu_e, mk_clock_T(3.47, lambda o: 13.0)) for o in TDG]
        up = [u_point(n, A0[f_], nu_e, mk_clock_U(3.47, lambda g: 13.0)) for n in DFS]
        mt, mu = max(abs(p["Delta_pred"]) for p in tp), max(abs(p["E_pred"]) for p in up)
        ok &= mt < 0.02 and mu < 0.05
        RES["oldclock"][f_] = dict(max_abs_Delta_pred=mt, max_abs_E_pred=mu)
        P(f"  [{f_}] max |Delta_pred| {mt:.4f} dex; max |E_pred| {mu:.4f}")
    RES["mutate_ok"] = bool(ok); P(f"  MUTATE oldclock: {'BITES (old systems sit on the law)' if ok else 'FAILS'}"); finish(0 if ok else 1)

# --------------------------------------------------------------------------------------------------------------- MAIN
P("\n=== PART A: CFG930 sealed S1 (tidal dwarfs show zero excess) on the six Lelli+15 TDGs, the seal's estimator (CFG931 INFO path, gas counted)")
RES["S1"] = {}
for f_ in FOOTS:
    s = s1_score(f_)
    var = {"velocity-only sigma (meas-term se)": s1_score(f_, verr_only=True)["alt_meas"]["cls"],
           "nu_simple kernel": s1_score(f_, nu=nu_s)["cls"], "M_mol x 0": s1_score(f_, mmol=0.0)["cls"], "M_mol x 2": s1_score(f_, mmol=2.0)["cls"],
           "alt se: measurement term": s["alt_meas"]["cls"], "alt: median, 1.2533 rms/sqrt n": s["alt_median"]["cls"]}
    diff = [k for k, v in var.items() if v != s["cls"]]
    s["variants"] = var; s["qualifier"] = "FRAGILE" if diff else "ROBUST"; s["differing"] = diff
    s["kill_clause_met"] = s["mean"] > 2 * s["se"]
    s["power_line"] = dict(uniform_excess_alt_dex=DW_ALT[f_], two_se=2 * s["se"], detectable=bool(2 * s["se"] < DW_ALT[f_]),
                           gap_to_alt_in_se=(DW_ALT[f_] - s["mean"]) / s["se"])
    RES["S1"][f_] = s
    P(f"  [{f_}] mean Delta {s['mean']:+.3f} dex; se {s['se']:.3f} = sd/sqrt6 {s['sd_over_sqrtn']:.3f} (+) Ups floor {s['ups_floor']:.3f} "
      f"(mean at M*x2 {s['mean_ups2']:+.3f}, x1/2 {s['mean_ups_half']:+.3f}); z {s['mean'] / s['se']:+.2f}")
    P(f"      per object: " + "; ".join(f"{p['name']} {p['Delta']:+.2f}+-{p['sigma']:.2f}" for p in s["per_object"]))
    P(f"      alt se (measurement) {s['alt_meas']['se']:.3f} -> {s['alt_meas']['cls']}; median {s['alt_median']['median']:+.3f} +- {s['alt_median']['se']:.3f} -> {s['alt_median']['cls']}")
    P(f"      variants: " + "; ".join(f"{k}: {v}" for k, v in var.items()))
    P(f"      kill clause (mean > +2 se): {'MET' if s['kill_clause_met'] else 'not met'}; power line: uniform-excess alternative {DW_ALT[f_]:+.3f} dex, "
      f"2 se {2 * s['se']:.3f} -> {'detectable' if s['power_line']['detectable'] else 'NOT detectable'}; the sample sits {s['power_line']['gap_to_alt_in_se']:.1f} se below it")
    P(f"  [{f_}] S1 CLASS: {s['cls']}  [{s['qualifier']}]")

# =====================================================================================================  PART B
P("\n=== PART B: the deficit question (class T: six Lelli+15 TDGs, dex; class U: DF2 + DF4, ln sigma^2).  Rule: criteria 5.1")
RES["routes"] = {}
def t_run(f_, route, verr_only=False, nu=nu_e): return [t_point(o, A0[f_], nu, route, verr_only=verr_only) for o in TDG]
def u_run(f_, route, sig=None): return [u_point(n, A0[f_], nu_e, route, sig=(None if sig is None else sig.get(n))) for n in DFS]
def u_run_zf(f_, fvals): return [u_point_zf(n, f_, fvals[n]) for n in DFS]
age_nom_T = lambda o: o["t"]; age_lo_T = lambda o: max(o["t"] - o["et"], 0.05); age_hi_T = lambda o: o["t"] + o["et"]
age_nom_U = lambda g: g["age"][0]; age_lo_U = lambda g: g["age"][0] - g["age"][2]; age_len_U = lambda g: max(0.0, min(g["age"][0] - g["age"][2], 6.0))

for f_ in FOOTS:
    a0 = A0[f_]; RR = RES["routes"][f_] = {}
    lawT = t_run(f_, r_law); lawU = u_run(f_, law_U)
    stT_law, stU_law = stats(lawT), stats(lawU)
    rlawT, rlawU = stT_law["rbar"], stU_law["rbar"]
    rlawU_zf = stats(u_run_zf(f_, {n: 1.0 for n in DFS}))["rbar"]            # law reference of the CFG657-zf variant (km/s)
    RR["law"] = dict(T=dict(stats=stT_law, cls=basic_class(stT_law, rlawT), per_object=lawT), U=dict(stats=stU_law, cls=basic_class(stU_law, rlawU), per_object=lawU))
    P(f"\n  ---------------- footing {f_} (a0 {a0:.4e}) ----------------")
    P(f"  bare law (reference): T {fmt(stT_law)}; U {fmt(stU_law)}")
    P("    T per object (Delta_obs vs law): " + "; ".join(f"{p['name']} {p['Delta_obs']:+.2f}+-{p['s']:.2f}" for p in lawT))
    P("    U per object (E_obs vs law): " + "; ".join(f"{p['name']} {p['E_obs']:+.3f}+-{p['sE']:.3f} (z {p['z']:+.2f})" for p in lawU))

    def report(tag, title, T=None, U=None):
        out = {}
        for cl, dat in (("T", T), ("U", U)):
            if dat is None:
                out[cl] = dict(cls="NOT TESTABLE"); continue
            prim, corners, variants, rlaw = dat
            st = stats(prim); cs = {k: stats(v) for k, v in corners.items()}; vs = {k: (stats(v[0]), v[1]) for k, v in variants.items()}
            rc = route_class(st, cs, vs, rlaw)
            out[cl] = dict(stats=st, corners=cs, variants={k: dict(stats=v[0], rlaw=v[1]) for k, v in vs.items()}, **rc, per_object=prim,
                           frac_of_law_deficit_removed=1.0 - st["rbar"] / rlaw if rlaw else None)
            unit = "dex" if cl == "T" else "ln"
            P(f"  {tag} {cl}: {fmt(st)} [{unit}]; removes {100 * (1 - st['rbar'] / rlaw):.0f}% of the law's mean deficit -> {rc['cls']} [{rc['qualifier']}]"
              + (f"; differing: {rc['differing']}" if rc["differing"] else ""))
            if cl == "T":
                P("      pred Delta: " + "; ".join(f"{p['name']} {p['Delta_pred']:+.2f} (f {p['f']:.3f}, obs {p['Delta_obs']:+.2f}, z {p['z']:+.2f})" for p in prim))
            else:
                P("      pred E: " + "; ".join(f"{p['name']} {p['E_pred']:+.3f} (f {p['f']:.4f}, obs {p['E_obs']:+.3f} +- {p['sE']:.3f}, z {p['z']:+.2f})" for p in prim))
            for k, v in cs.items():
                P(f"        corner {k}: {fmt(v)} -> {rc['corner_classes'][k]}")
            for k, (v, rl) in vs.items():
                P(f"        variant {k}: {fmt(v)} (law ref {rl:+.3f}) -> {rc['variant_classes'][k]}")
        lab = [out[c]["cls"] for c in ("T", "U")]
        overall = (lab[0] if lab[0] == lab[1] and lab[0] in ("EXPLAINS", "FAILS", "NOT TESTABLE") else "PARTIAL")
        out["overall"] = overall
        P(f"  {tag} OVERALL [{f_}]: {overall}  (T {out['T']['cls']}, U {out['U']['cls']})")
        RR[tag] = dict(title=title, **out)
        return out

    # ---------------- route (i): supply
    P(f"\n  ROUTE (i) supply [{f_}]")
    fcap0 = {n: FCAP[f_][n]["primary"] for n in DFS}
    cornT_i = {f"F-channel Rfac {rf} Mhost x{hf} k {k}": t_run(f_, mk_F_T(rf, hf, k)) for rf in (1.0, 0.5) for hf in (0.5, 1.0, 2.0) for k in (1.0, 3.0)}
    cornU_i = {"S4 strict f=0": u_run(f_, newton_U)}
    for lab_, fv in FCAP[f_]["DF2"]["corners"].items():
        cornU_i[f"CFG657 alpha=0 {lab_}"] = u_run(f_, mk_fixed_U({n: FCAP[f_][n]["corners"][lab_] for n in DFS}))
    report("route_i", "supply: T = S4 no-capture + v2 catchment (f = 0); U = CFG657 capture at alpha_P 0 (primary inputs)",
           T=(t_run(f_, r_newton), cornT_i, {"velocity-only sigma": (t_run(f_, r_newton, verr_only=True), rlawT)}, rlawT),
           U=(u_run(f_, mk_fixed_U(fcap0)), cornU_i, {"CFG657 zf form": (u_run_zf(f_, fcap0), rlawU_zf)}, rlawU))
    RR["route_i"]["F_channel_f_range_T"] = [min(p["f"] for v in cornT_i.values() for p in v), max(p["f"] for v in cornT_i.values() for p in v)]
    RR["route_i"]["fcap_alpha0_U"] = FCAP[f_]
    # contrasts (no class weight)
    own = lambda M: RATIO; full = lambda M: RATIO * N_of(math.log10(M))[0]
    cT_a, cU_a = stats(t_run(f_, mk_supply_T(own))), stats(u_run(f_, mk_supply_U(own)))
    cT_b, cU_b = stats(t_run(f_, mk_supply_T(full))), stats(u_run(f_, mk_supply_U(full)))
    RR["route_i_contrasts"] = dict(own_share=dict(T=cT_a, U=cU_a, T_f=[p["f"] for p in t_run(f_, mk_supply_T(own))], U_f=[p["f"] for p in u_run(f_, mk_supply_U(own))]),
                                   isolated_catchment=dict(T=cT_b, U=cU_b))
    P(f"  (i-C a) own cosmic share kept (removed 10-14 rule): T {fmt(cT_a)}; U {fmt(cU_a)}  [no class weight]")
    P(f"  (i-C b) v2 catchment as an isolated system (N = 1/f_ret census): T {fmt(cT_b)}; U {fmt(cU_b)}  [no class weight]")

    # ---------------- route (ii): settling clock (EFE-free)
    P(f"\n  ROUTE (ii) settling clock, EFE-free [{f_}]  (primary tau 3.47 Gyr; nominal ages)")
    cornT_ii = {"ages -1 sigma, tau 3.47": t_run(f_, mk_clock_T(3.47, age_lo_T)), "ages +1 sigma, tau 3.47": t_run(f_, mk_clock_T(3.47, age_hi_T)),
                f"nominal ages, tau_min {TAU_MIN[f_]:.3f} (TDG-calibrated)": t_run(f_, mk_clock_T(TAU_MIN[f_], age_nom_T))}
    cornU_ii = {"ages -1 sigma, tau 3.47": u_run(f_, mk_clock_U(3.47, age_lo_U)), "CFG768 lenient age min(t - s_lo, 6 Gyr), tau 3.47": u_run(f_, mk_clock_U(3.47, age_len_U)),
                f"nominal ages, tau_min {TAU_MIN[f_]:.3f}": u_run(f_, mk_clock_U(TAU_MIN[f_], age_nom_U))}
    fU_ii = {n: 1.0 - math.exp(-age_nom_U(GAL[n]) / 3.47) for n in DFS}
    report("route_ii", "settling clock CFG763, EFE-free, tau 3.47 Gyr (slowest allowed by old discs), nominal ages",
           T=(t_run(f_, mk_clock_T(3.47, age_nom_T)), cornT_ii, {"velocity-only sigma": (t_run(f_, mk_clock_T(3.47, age_nom_T), verr_only=True), rlawT)}, rlawT),
           U=(u_run(f_, mk_clock_U(3.47, age_nom_U)), cornU_ii, {"CFG657 zf form": (u_run_zf(f_, fU_ii), rlawU_zf)}, rlawU))
    RR["route_ii"]["ages_T_Gyr"] = {o["name"]: dict(t=o["t"], et=o["et"], f_at_3p47=1 - math.exp(-o["t"] / 3.47)) for o in TDG}
    RR["route_ii"]["ages_U_Gyr"] = {n: dict(t=GAL[n]["age"][0], f_at_3p47=fU_ii[n]) for n in DFS}

    # ---------------- route (iii): EFE, declared contrast
    P(f"\n  ROUTE (iii) EFE -- DECLARED CONTRAST, NOT A FRAMEWORK ROUTE [{f_}]")
    cornT_iii = {"M_host x 1/2": t_run(f_, mk_efe_T(0.5)), "M_host x 2": t_run(f_, mk_efe_T(2.0))}
    cornU_iii = {"Mg 5e10": u_run(f_, mk_efe_U(Mg=5e10)), "Mg 3e11": u_run(f_, mk_efe_U(Mg=3e11)), "M35 3e9": u_run(f_, mk_efe_U(M35=3e9)),
                 "M35 1e10": u_run(f_, mk_efe_U(M35=1e10)), "NGC 1052 alone at 2 R_proj": u_run(f_, mk_efe_U(only1052=True, Rmul=2.0))}
    efeU0 = u_run(f_, mk_efe_U())
    report("route_iii_EFE_contrast", "EFE contrast (FM12 eq. 60, nu_e): T Lelli hosts 0.6 L_K at D_p; U NGC 1052 + NGC 1035 scalar sum at R_proj",
           T=(t_run(f_, mk_efe_T(1.0)), cornT_iii, {"velocity-only sigma": (t_run(f_, mk_efe_T(1.0), verr_only=True), rlawT)}, rlawT),
           U=(efeU0, cornU_iii, {"CFG657 zf form": (u_run_zf(f_, {p["name"]: p["f"] for p in efeU0}), rlawU_zf)}, rlawU))
    # what an EFE explanation needs
    def rbarT(m): return stats(t_run(f_, mk_efe_T(m)))["rbar"]
    lo, hi = math.log(1e-4), math.log(1e6)
    if rbarT(math.exp(lo)) * rbarT(math.exp(hi)) < 0:
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if rbarT(math.exp(lo)) * rbarT(math.exp(mid)) <= 0: hi = mid
            else: lo = mid
        mneed = math.exp(0.5 * (lo + hi))
    else:
        mneed = None
    gneT = {o["name"]: G * 0.6 * o["LK"] * MSUN / (o["Dp"] * KPC) ** 2 / a0 for o in TDG}
    need = {}
    for n in DFS:
        g = GAL[n]; r12, gb, nn, sl = u_base(g, a0, nu_e); Eo = 2 * math.log(g["obs"][0] / sl)
        h = lambda lx: math.log(efe_nueff(gb, 10 ** lx * a0, a0, nu_e) / nn) - Eo
        xs = np.linspace(-6, 3, 901); hv = [h(x) for x in xs]
        root = None
        for i in range(len(xs) - 1):
            if hv[i] * hv[i + 1] <= 0:
                a_, b_ = xs[i], xs[i + 1]
                for _ in range(80):
                    m_ = 0.5 * (a_ + b_)
                    if h(a_) * h(m_) <= 0: b_ = m_
                    else: a_ = m_
                root = 10 ** (0.5 * (a_ + b_)); break
        need[n] = dict(gNe_over_a0_needed=root, gNe_over_a0_estimate=u_hosts_gNe(n) / a0, gNi_over_a0=gb / a0,
                       E_obs=Eo, E_newton=-math.log(nn), below_newton=bool(Eo < -math.log(nn)),
                       R_proj_kpc={h_: g["D"] * 1000 * angsep(g["pos"], HOSTS[h_]) for h_ in HOSTS})
    RR["route_iii_EFE_contrast"]["needs"] = dict(T_host_mass_multiplier_for_zero_mean=mneed, T_gNe_over_a0_estimate=gneT, U=need)
    P(f"  EFE needs: T common host-mass multiplier for zero mean residual = {('%.2f' % mneed) if mneed else 'no root'} "
      f"(estimated g_Ne/a0 {min(gneT.values()):.3f}-{max(gneT.values()):.3f})")
    for n, v in need.items():
        P(f"    {n}: g_Ne/a0 needed {('%.4f' % v['gNe_over_a0_needed']) if v['gNe_over_a0_needed'] else 'NONE (E_obs below Newton: no EFE reaches it)'}; "
          f"estimate {v['gNe_over_a0_estimate']:.4f}; g_Ni/a0 {v['gNi_over_a0']:.4f}; E_obs {v['E_obs']:+.3f} vs Newton {v['E_newton']:+.3f}; "
          f"R_proj NGC1052 {v['R_proj_kpc']['NGC1052']:.1f} kpc, NGC1035 {v['R_proj_kpc']['NGC1035']:.1f} kpc")

    # ---------------- reported rows (no class weight): nu_simple and R4 dispersions
    nsT = {k: stats(t_run(f_, r, nu=nu_s)) for k, r in (("law", r_law), ("route_i", r_newton), ("route_ii", mk_clock_T(3.47, age_nom_T)))}
    r4 = {k: stats(u_run(f_, r, sig=SEC)) for k, r in (("law", law_U), ("route_i", mk_fixed_U(fcap0)), ("route_ii", mk_clock_U(3.47, age_nom_U)), ("EFE", mk_efe_U()))}
    RR["reported_rows"] = dict(nu_simple_T=nsT, R4_secondary_sigma_U=r4)
    P("  reported (no class weight): nu_simple T: " + "; ".join(f"{k} rbar {v['rbar']:+.3f}+-{v['se']:.3f} p {v['p']:.3g}" for k, v in nsT.items()))
    P("  reported (no class weight): R4 sigma (DF2 10.8, DF4 8.0) U: " + "; ".join(f"{k} rbar {v['rbar']:+.3f}+-{v['se']:.3f} p {v['p']:.3g}" for k, v in r4.items()))

# ---------------- D-ii: CFG763's own F1/F2 re-run EFE-free
P("\n=== D-ii (diagnostic): CFG763's F1/F2 re-run EFE-free (same 7 objects, recipe, grid); window OPEN iff tau_min,95 <= 3.47 Gyr")
RES["D_ii"] = {}
for f_ in FOOTS:
    c = clock763(A0[f_], nu_e, efe=False); cm = clock763(A0[f_], C4.nu_mono, efe=False)
    win = c["lower_1sigma_ages"]["tau_min95_Gyr"] is not None and c["lower_1sigma_ages"]["tau_min95_Gyr"] <= 3.47
    RES["D_ii"][f_] = dict(nu_e=c, nu_mono=cm, window="OPEN" if win else "CLOSED", with_EFE_cfg763=RES["K3"]["mine"][f_])
    P(f"  [{f_}] EFE-free nu_e: chi2 tau->0 (law) {c['chi2_tau0']:.2f}, tau->inf (Newton) {c['chi2_tauinf']:.2f}; tau_min,95 {c['lower_1sigma_ages']['tau_min95_Gyr']} Gyr (-1 sigma ages), "
      f"{c['nominal_ages']['tau_min95_Gyr']} Gyr (nominal); chi2 at 3.47: {c['lower_1sigma_ages']['chi2_at_3p47']:.2f} / {c['nominal_ages']['chi2_at_3p47']:.2f} "
      f"(min {c['lower_1sigma_ages']['chi2_min']:.2f} / {c['nominal_ages']['chi2_min']:.2f}); nu_mono {cm['lower_1sigma_ages']['tau_min95_Gyr']} / {cm['nominal_ages']['tau_min95_Gyr']}"
      f" -> window {RES['D_ii'][f_]['window']}  (with the 1-D EFE, CFG763: {RES['K3']['mine'][f_]['tau_lo']:.3f} / {RES['K3']['mine'][f_]['tau_nom']:.3f})")
RES["D_ii_window_both"] = "OPEN" if all(RES["D_ii"][f_]["window"] == "OPEN" for f_ in FOOTS) else "CLOSED"

# ---------------- summary + plain statement inputs
P("\n=== SUMMARY")
SUMM = {}
for f_ in FOOTS:
    RR = RES["routes"][f_]
    SUMM[f_] = dict(S1=RES["S1"][f_]["cls"] + f" [{RES['S1'][f_]['qualifier']}]",
                    route_i=dict(overall=RR["route_i"]["overall"], T=RR["route_i"]["T"]["cls"] + f" [{RR['route_i']['T']['qualifier']}]",
                                 U=RR["route_i"]["U"]["cls"] + f" [{RR['route_i']['U']['qualifier']}]"),
                    route_ii=dict(overall=RR["route_ii"]["overall"], T=RR["route_ii"]["T"]["cls"] + f" [{RR['route_ii']['T']['qualifier']}]",
                                  U=RR["route_ii"]["U"]["cls"] + f" [{RR['route_ii']['U']['qualifier']}]"),
                    route_iii_EFE_contrast=dict(overall=RR["route_iii_EFE_contrast"]["overall"],
                                                T=RR["route_iii_EFE_contrast"]["T"]["cls"] + f" [{RR['route_iii_EFE_contrast']['T']['qualifier']}]",
                                                U=RR["route_iii_EFE_contrast"]["U"]["cls"] + f" [{RR['route_iii_EFE_contrast']['U']['qualifier']}]"),
                    D_ii_window=RES["D_ii"][f_]["window"])
    P(f"  [{f_}] S1: {SUMM[f_]['S1']}")
    for k in ("route_i", "route_ii", "route_iii_EFE_contrast"):
        P(f"  [{f_}] {k}: {SUMM[f_][k]['overall']}  (T {SUMM[f_][k]['T']}; U {SUMM[f_][k]['U']})")
    P(f"  [{f_}] D-ii EFE-free clock window: {SUMM[f_]['D_ii_window']}")
RES["summary"] = SUMM
fw_explains = {f_: {cl: [k for k in ("route_i", "route_ii") if RES["routes"][f_][k][cl]["cls"] == "EXPLAINS"] for cl in ("T", "U")} for f_ in FOOTS}
RES["framework_routes_that_explain"] = fw_explains
P("  framework-native routes reaching EXPLAINS: " + "; ".join(f"{f_}: T {v['T'] or 'none'}, U {v['U'] or 'none'}" for f_, v in fw_explains.items()))
# MUTATE status (read if present; informational)
ms = {}
for tag in ("MUTATE_onlaw", "MUTATE_plus04", "MUTATE_fullsupply", "MUTATE_oldclock"):
    pth = os.path.join(HERE, f"cfg936_results_{tag}.json")
    if os.path.exists(pth):
        with _REAL_OPEN(pth) as fh: d = json.load(fh)
        ms[tag] = dict(exit_code=d.get("exit_code"), ok=d.get("mutate_ok"))
RES["MUTATE_status_read"] = ms
P("  MUTATE outputs on disk: " + ("; ".join(f"{k}: exit {v['exit_code']}, ok {v['ok']}" for k, v in ms.items()) or "none"))
finish(0)
