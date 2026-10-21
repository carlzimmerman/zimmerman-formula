"""CFG948 -- the derived no-capture criterion (CFG939: v_rel > V_esc,b => no capture) confronted with the Coma UDGs (CFG933's
excess) and the NGC 1052 / tidal dwarfs (Newton).
Criteria: FROZEN_CRITERIA.md (e5cc927ce, committed alone before this script and before any number of this lane);
AMENDMENT_A1.md (523a09954, post hoc after the first K-only run: K2 control wording only).
Run (one core, one process at a time, in this order):
  CFG948_MODE=K       OMP_NUM_THREADS=1 nice -n 10 python3 cfg948.py   -> cfg948_K.out, cfg948_results_K.json
  CFG948_MODE=engine  ...                                               -> cfg948_engine.out, cfg948_results_engine.json
  CFG948_MODE=onlaw   ... ; CFG948_MODE=plus04 ...                      -> cfg948_MUTATE_<mode>.out / cfg948_results_MUTATE_<mode>.json
  (no mode)           ...                                               -> cfg948.out, cfg948_results.json
Inputs (read only): cfg933.py exec'd read-only through its K-stage (through it cfg921/cfg928, the Coma table, CFG655's DF2/DF4
table) and its evaluate/summ/classify functions exec'd from its text; cfg939.py's kernel, spherical-shell and N5 code exec'd from
its text; cfg933/cfg939 result JSONs (K1, K2); L23's text (Coma beta-model constants); the Coma table's distance columns; the
Leisman+2017 HUD table.  Nothing downloaded.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, re, json, math, time, resource, contextlib, builtins, warnings, csv
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

T0 = time.time()
_REAL_OPEN = builtins.open
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG948_MODE", ""); assert MODE in ("", "K", "engine", "onlaw", "plus04"), MODE
SUF = {"": "", "K": "_K", "engine": "_engine", "onlaw": "_MUTATE_onlaw", "plus04": "_MUTATE_plus04"}[MODE]
for _e in ("CFG933_MODE", "CFG939_MUTATE", "CFG939_A2", "CFG928_MUTATE", "CFG928_KONLY", "CFG921_MUTATE", "CFG921_KONLY",
           "CFG919_MUTATE", "CFG914_MUTATE", "CFG880_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
RES = dict(lane="CFG948", criteria="e5cc927ce", amendment_A1="523a09954", mode=MODE or "main", checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def jdef(o):
    if hasattr(o, "item"): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
def finish(code):
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_mb"] = round(rss_mb(), 1); RES["exit_code"] = code
    P(f"\ndone [{time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB], exit {code}.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    with _REAL_OPEN(os.path.join(HERE, f"cfg948_results{SUF}.json"), "w") as fh: json.dump(RES, fh, indent=1, default=jdef)
    with _REAL_OPEN(os.path.join(HERE, f"cfg948{SUF}.out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
    sys.exit(code)
def guard():
    if rss_mb() > 950:
        P(f"RSS GUARD: {rss_mb():.0f} MB > 950 MB -> abort"); finish(3)
def J(*p):
    with _REAL_OPEN(os.path.join(LANES, *p)) as fh: return json.load(fh)
def T(*p):
    with _REAL_OPEN(os.path.join(REPO, *p)) as fh: return fh.read()

FOOTS = ("canonical", "alt"); LN10 = math.log(10.0)
P("CFG948  the derived no-capture criterion (CFG939) vs the Coma UDGs (CFG933) and the NGC 1052 / tidal dwarfs"
  + {"": "", "K": "   [K only]", "engine": "   [engine: sudden-loss ceiling]", "onlaw": "   [MUTATE onlaw]", "plus04": "   [MUTATE plus04]"}[MODE])
P("  criteria e5cc927ce; kappa = 1/2 FITTED; footings never pooled; isolated EFE-free law as the most generous ceiling")

# ===================================================================================================================== sandbox
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG948 refuses to write {file!r} from re-executed committed code")
    return _REAL_OPEN(file, mode, *a, **k)
class _Exit(Exception): pass
def _exit(code=0): raise _Exit(code)
def sandbox_exec(path, src, ns):
    buf = io.StringIO(); err = None
    old_open, old_exit = builtins.open, sys.exit
    builtins.open = _ro_open; sys.exit = _exit
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(src, path, "exec"), ns)
    except BaseException as e:                      # noqa: BLE001 -- reported as a K failure
        err = f"{type(e).__name__}: {e}"
    finally:
        builtins.open = old_open; sys.exit = old_exit
    return buf.getvalue(), err

KOK = []
# ===================================================================================================================== CFG933 (read only)
P("\n=== CFG933's sealed estimator, exec'd read-only through its K-stage")
F933 = os.path.join(LANES, "CFG933_udg_sealed_test", "cfg933.py")
with _REAL_OPEN(F933) as _fh: s933 = _fh.read()
_k = s933.index("K_ALL = all(KOK); RES[\"K_all\"] = K_ALL")
N3 = {"__file__": F933, "__name__": "cfg933_ro"}
o933, e933 = sandbox_exec(F933, s933[:_k] + "K_ALL = all(KOK)\n", N3)
c933 = N3.get("RES", {}).get("checks", {})
k0 = e933 is None and bool(N3.get("K_ALL")) and len(c933) >= 6 and all(v["ok"] for v in c933.values())
KOK.append(check("K0 cfg933.py exec'd read-only through its K-stage: its own K-checks pass", k0,
                 f"{sum(v['ok'] for v in c933.values())}/{len(c933)} CFG933 checks pass" + (f"; error {e933}" if e933 else "")))
if not k0:
    P("  K0 failed: the lane stops (criteria section 7)."); RES["class"] = None; finish(2)
_b0, _b1 = s933.index("def evaluate(f, mods=None):"), s933.index("def plant(G, kind):")
_o, _e = sandbox_exec(F933, s933[_b0:_b1], N3)
if _e:
    P(f"  exec of cfg933's evaluate/summ/classify failed: {_e}"); finish(2)
evaluate, summ, classify, sealed = N3["evaluate"], N3["summ"], N3["classify"], N3["sealed"]
UNIV, ADM, POP, NAMES, A0, nu_e = N3["UNIV"], N3["ADM"], N3["POP"], N3["NAMES"], N3["A0"], N3["nu_e"]
G_SI, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
IC = [i for i in range(len(UNIV)) if ADM[i] and POP[i] == "Coma"]            # G-Coma (9)
IG = [i for i in range(len(UNIV)) if ADM[i] and POP[i] == "NGC1052"]         # G-group (DF2, DF4)
IC11 = [i for i in range(len(UNIV)) if POP[i] == "Coma"]                     # R3 (all 11 Coma)

# Coma distances (table columns d_kpc, dmean_kpc) by name
_rows = [l.rstrip("\n").split("\t") for l in T("real_research", "data", "freundlich2022_coma_udgs.tsv").splitlines()
         if l.strip() and not l.startswith("#")]
_hd = {h: i for i, h in enumerate(_rows[0])}
DIST = {r[_hd["name"]]: dict(dproj=float(r[_hd["d_kpc"]]), dmean=float(r[_hd["dmean_kpc"]])) for r in _rows[1:]}

# ===================================================================================================================== CFG939 (read only)
F939 = os.path.join(LANES, "CFG939_lagrangian_displacement_shell_crossing", "cfg939.py")
with _REAL_OPEN(F939) as _fh: s939 = _fh.read()
def _slice(a, b): return s939[s939.index(a):s939.index(b)]
MK = "# ============================================================================================ "
N9 = {"np": np, "math": math, "brentq": brentq, "quad": quad, "csv": csv, "os": os, "REPO": REPO, "guard": (lambda: None),
      "__name__": "cfg939_ro"}
for a_, b_ in ((MK + "kernels", MK + "1-D sheet code"), (MK + "spherical shells", MK + "A2 report-only"),
               (MK + "N5 consequences + grading", "AGE = {")):
    _o, _e = sandbox_exec(F939, _slice(a_, b_), N9)
    if _e:
        P(f"  exec of cfg939 slice '{a_[len(MK):]}' failed: {_e}"); finish(2)
Wdiff, Gant, Hpot, fcrit_x = N9["Wdiff"], N9["Gant"], N9["Hpot"], N9["fcrit_x"]
FOOT939, plummer939, sys_numbers = N9["FOOT"], N9["plummer"], N9["sys_numbers"]
R939 = J("CFG939_lagrangian_displacement_shell_crossing", "cfg939_results.json")

# ===================================================================================================================== engine (S2 + S3 shells)
RMIN, R0, NSH = 1.0, 50.0, 2000
def bary(kind, M, A=None):
    """(M_b(<r), Phi_b(r), rho_b(r)) in G = a0 = 1 units"""
    if kind == "point":
        return (lambda r: M * np.ones_like(np.asarray(r, float)), lambda r: -M / np.asarray(r, float), lambda r: 0.0 * np.asarray(r, float))
    return (lambda r: M * np.asarray(r, float) ** 3 / (np.asarray(r, float) ** 2 + A * A) ** 1.5,
            lambda r: -M / np.sqrt(np.asarray(r, float) ** 2 + A * A),
            lambda r: 3 * M * A * A / (4 * math.pi * (np.asarray(r, float) ** 2 + A * A) ** 2.5))
def u_of_g(g): g = np.asarray(g, float); return (-g + np.sqrt(g * g + 4 * g)) / 2       # law: R(u) = u^2/(1-u) = g  (a0 = 1)
def m_law_b(r, Mbf): r = np.asarray(r, float); return u_of_g(Mbf(r) / r ** 2) * r ** 2
def accel(r, dm, mcore, Mbf):
    order = np.argsort(r); rs = r[order]
    m_in = mcore + dm * np.arange(r.size)
    s_in = m_in / rs ** 2; s_out = (m_in + dm) / rs ** 2
    if np.any(s_out >= 1): s_out = np.minimum(s_out, 1 - 1e-12); s_in = np.minimum(s_in, s_out - 1e-15)
    a_s = -Mbf(rs) / rs ** 2 + rs ** 2 * Wdiff(s_out, s_in) / dm
    a = np.empty_like(r); a[order] = a_s
    return a, order
def energy(r, v, dm, mcore, Phif):
    rs = np.sort(r); N = r.size; m_in = mcore + dm * np.arange(N); m_out = m_in + dm
    E = 0.5 * dm * float(np.sum(v * v)) + dm * float(np.sum(Phif(rs)))
    Et = 0.5 * mcore ** 1.5 * (Gant(mcore / RMIN ** 2) - Gant(mcore / rs[0] ** 2))
    Et += float(np.sum(0.5 * m_out[:-1] ** 1.5 * (Gant(m_out[:-1] / rs[:-1] ** 2) - Gant(m_out[:-1] / rs[1:] ** 2))))
    Et += float(0.5 * m_out[-1] ** 1.5 * Gant(np.array([m_out[-1] / rs[-1] ** 2]))[0])
    return E + Et
def shell_E(r, v, dm, mcore, Phif, order):
    rs = r[order]; N = r.size; m_in = mcore + dm * np.arange(N); m_out = m_in + dm; m_mid = m_in + dm / 2
    rnext = np.append(rs[1:], np.inf)
    Tj = Hpot(m_mid, rs) - np.where(np.isfinite(rnext), Hpot(m_mid, np.where(np.isfinite(rnext), rnext, 1.0)), 0.0)
    Pi_frozen = np.cumsum(Tj[::-1])[::-1]
    Pi_q = 0.5 * (m_out ** 1.5 * Gant(m_out / rs ** 2) - m_in ** 1.5 * Gant(m_in / rs ** 2)) / dm
    vs = v[order]
    Etf_s = 0.5 * vs ** 2 + Phif(rs) + Pi_frozen; Eq_s = 0.5 * vs ** 2 + Phif(rs) + Pi_q
    Etf = np.empty(N); Eq = np.empty(N); Etf[order] = Etf_s; Eq[order] = Eq_s
    return Etf, Eq
def law_ic(mcore, Mbf, N=NSH, Rout=R0):
    mtot = float(m_law_b(Rout, Mbf)) - mcore; dm = mtot / N; r = np.empty(N)
    for i in range(N):
        mi = mcore + i * dm; mo = mi + dm
        f = lambda rr: rr ** 2 * float(Wdiff(np.array(mo / rr ** 2), np.array(mi / rr ** 2))) / dm - float(Mbf(rr)) / rr ** 2
        lo = max(math.sqrt(mo) * 1.0000001, RMIN * 0.5); hi = Rout * 3
        r[i] = brentq(f, lo, hi, xtol=1e-15, rtol=1e-15, maxiter=500)
    return r, dm

def engine_run(A, f, dt=0.02, absorb=None, tq_mult=10.0):
    """sudden uniform loss of baryon fraction f at t = 0 (pre-loss M_b = 1/(1-f), post-loss 1, Plummer scale A); medium in the
    discrete pre-loss law at rest; E(t) at r12 = (4/3) A relative to the CURRENT baryons' law."""
    bpre, bpost = bary("plummer", 1.0 / (1.0 - f), A), bary("plummer", 1.0, A)
    mcore = float(m_law_b(RMIN, bpre[0])); r, dm = law_ic(mcore, bpre[0]); v = np.zeros_like(r)
    r12 = 4.0 * A / 3.0; Mb12 = float(bpost[0](r12)); ml12 = float(m_law_b(r12, bpost[0])); ml12pre = float(m_law_b(r12, bpre[0]))
    g12 = Mb12 / r12 ** 2; u12 = float(u_of_g(g12))
    om2 = 4 * math.pi * float(bpost[2](r12)) + (2 * g12 / r12) / (1 - u12); Tq = 2 * math.pi / math.sqrt(om2); tend = tq_mult * Tq
    n0 = r.size
    if absorb is not None:
        keep = r <= absorb; r = r[keep]; v = v[keep]
    order = np.argsort(r); _, Eq0 = shell_E(r, v, dm, mcore, bpost[1], order)
    unb0 = float(np.sum(Eq0 > 0)) / n0
    E0 = energy(r, v, dm, mcore, bpost[1])
    scaleE = dm * float(np.sum(np.abs(bpost[1](r)))) + abs(E0)
    def Emeas(r_, order_):
        mc = mcore + dm * np.searchsorted(r_[order_], r12); return math.log((Mb12 + mc) / (Mb12 + ml12))
    a, order = accel(r, dm, mcore, bpost[0])
    E_closed = math.log((Mb12 + ml12pre) / (Mb12 + ml12)); E_eng0 = Emeas(r, order)
    nst = int(round(tend / dt)); se_ = max(1, int(round(0.5 / dt))); ts = [0.0]; Es = [E_eng0]
    for n in range(nst):
        v += 0.5 * dt * a; r += dt * v
        low = r < RMIN; r[low] = 2 * RMIN - r[low]; v[low] = -v[low]
        if absorb is not None:
            out = r > absorb
            if np.any(out): r = r[~out]; v = v[~out]
        a, order = accel(r, dm, mcore, bpost[0]); v += 0.5 * dt * a
        if (n + 1) % se_ == 0: ts.append((n + 1) * dt); Es.append(Emeas(r, order))
        if n % 20000 == 0: guard()
    E1 = energy(r, v, dm, mcore, bpost[1])
    ts = np.array(ts); Es = np.array(Es)
    w1 = (ts >= Tq) & (ts <= 10 * Tq); w0 = ts <= Tq
    esc = float(np.sum((r > 10 * R0) & (v > 0))) / n0
    return dict(A=A, f=f, dt=dt, Tq=Tq, tend=tend, r12=r12, E0plus_engine=E_eng0, E0plus_closed=E_closed, W1=float(Es[w1].mean()),
                W0=float(Es[w0].mean()), maxE_after_Tq=float(Es[ts >= Tq].max()), minE_after_Tq=float(Es[ts >= Tq].min()),
                unbound_t0=unb0, escaping_end=esc, dE_rel=abs(E1 - E0) / abs(E0), dE_over_scale=abs(E1 - E0) / scaleE,
                n_kept_end=int(r.size), absorb=absorb, E_series_coarse=[[float(t_), float(e_)] for t_, e_ in zip(ts[::40], Es[::40])])

def run_with_rule(A, f, absorb=None):
    """criteria 2.3: dt 0.02, halved (at most 3 times) while |dE/E| > 1e-3 (absorbing runs are not energy-checked)"""
    dt = 0.02
    for k in range(4):
        o = engine_run(A, f, dt=dt, absorb=absorb)
        if absorb is not None or o["dE_rel"] <= 1e-3 or k == 3: o["halvings"] = k; return o
        dt /= 2

# ===================================================================================================================== per-galaxy helpers
def a0k(f): return A0[f] * KPC / 1e6                                              # (km/s)^2/kpc
GK = 4.30091e-6
def A_of(u, f): return u["Re"] / math.sqrt(GK * u["Ms"] / a0k(f))                # R_e / r_M (current M*)
_l23 = T("fable_independent_2026", "L23_udg_verify.py")
_mb = re.search(r"kT_C, rc_C, bet_C, mu_mol = ([0-9.]+) \* keV, ([0-9.]+) \* kpc, ([0-9.]+), ([0-9.]+)", _l23)
_mc = re.search(r"m_p = ([0-9.e+-]+); keV = ([0-9.e+-]+)", _l23)
BETA = dict(kT_keV=8.6, rc_kpc=276.0, beta=0.71, mu=0.6, m_p=1.67262e-27, keV=1.602176634e-16)
CBETA = 3 * BETA["beta"] * BETA["kT_keV"] * BETA["keV"] / (BETA["mu"] * BETA["m_p"])   # m^2/s^2
RC = BETA["rc_kpc"] * KPC
def g_host(D_kpc): r = D_kpc * KPC; return CBETA * r / (r * r + RC * RC)                # m/s^2 (X-ray hydrostatic total field)
def q_host(D_kpc): r = D_kpc * KPC; return 2 * CBETA * r * r / (r * r + RC * RC) ** 2     # Omega^2 - Phi'' (1/s^2)
def plummer_Min(M, a, r): return M * r ** 3 / (r * r + a * a) ** 1.5
def g_law_udg(u, r_m, f, Ms=None):
    Ms = u["Ms"] if Ms is None else Ms; a = u["Re"] * KPC
    gN = G_SI * plummer_Min(Ms * MSUN, a, r_m) / r_m ** 2
    return float(nu_e(np.array([gN / A0[f]]))[0]) * gN
def r_jacobi(u, D_kpc, f):
    q = q_host(D_kpc)
    F = lambda r: r ** 3 * q - g_law_udg(u, r, f) * r * r                          # r^3 q = G m_eff(<r), G m_eff = g_law r^2
    return brentq(F, 0.01 * KPC, 2000 * KPC, xtol=1e-6 * KPC) / KPC               # kpc
def proj_frac(R, a, rt):
    """projected mass fraction inside R for a Plummer (scale a) truncated at rt (3-D)"""
    rho = lambda r: (1 + r * r / (a * a)) ** -2.5
    m3 = lambda r: (r / a) ** 3 / (1 + (r / a) ** 2) ** 1.5
    if R >= rt: return 1.0
    inner = m3(R)                                                                  # times a^3 * 4 pi/3 ... common factor below
    shell = quad(lambda r: 3 * r * r * rho(r) * (1 - math.sqrt(1 - R * R / (r * r))) / a ** 3, R, rt, limit=200)[0]
    return (inner + shell) / m3(rt)
def trunc_ratio(tau):
    """r_h,3D / R_e for a Plummer truncated at r_t = tau R_e with projected half-light radius R_e; (ratio, capped)"""
    if not np.isfinite(tau): return 1.0 / math.sqrt(1.0 / 0.5 ** (2.0 / 3.0) - 1.0), False      # untruncated Plummer: 1.30477
    Re = 1.0; rt = tau
    if tau <= 1.0 / math.sqrt(1 - 0.5 ** (2 / 3)) * 1.0000001:                    # uniform-sphere limit (a -> inf)
        return 0.5 ** (1 / 3) * rt, True
    Fa = lambda a: proj_frac(Re, a, rt) - 0.5
    lo, hi = 1e-3, 1e3
    if Fa(hi) > 0: return 0.5 ** (1 / 3) * rt, True
    a = brentq(Fa, lo, hi, xtol=1e-12)
    m3 = lambda r: (r / a) ** 3 / (1 + (r / a) ** 2) ** 1.5
    rh = brentq(lambda r: m3(r) - 0.5 * m3(rt), 1e-6, rt, xtol=1e-12)
    return rh / Re, False

# ===================================================================================================================== K-tests shared by modes
P("\n=== K1  CFG933 reproduced (G-Coma <E_obs>, se_obs, z vs its P2 prediction; DF2/DF4 E_obs and z; H)")
R933 = J("CFG933_udg_sealed_test", "cfg933_results.json")
k1d = []; K1N = {}
for f in FOOTS:
    G = evaluate(f); C = classify(G, f); ref = R933["byfoot"][f]["primary"]
    for k in ("mean_Eobs", "se_obs", "z"): k1d.append(abs(C["samples"]["coma"][k] - ref["samples"]["coma"][k]))
    for g_, gr in zip(C["group_per_galaxy"], ref["group_per_galaxy"]):
        k1d += [abs(g_["E_obs"] - gr["E_obs"]), abs(g_["z"] - gr["z"])]
    for k in ("diff", "se", "z"): k1d.append(abs(C["H"][k] - ref["H"][k]))
    K1N[f] = dict(coma_mean_Eobs=C["samples"]["coma"]["mean_Eobs"], coma_se_obs=C["samples"]["coma"]["se_obs"], coma_z_P2=C["samples"]["coma"]["z"],
                  group=[(g_["name"], g_["E_obs"], g_["z"]) for g_ in C["group_per_galaxy"]], H=C["H"])
KOK.append(check("K1 CFG933's G-Coma <E_obs>, se_obs, z; DF2/DF4 E_obs, z; H (diff, se, z) == cfg933_results.json (abs <= 1e-12), both footings",
                 max(k1d) <= 1e-12, f"max |diff| {max(k1d):.1e}; " + "; ".join(
                     f"{f}: Coma <E_obs> {K1N[f]['coma_mean_Eobs']:+.4f} (se {K1N[f]['coma_se_obs']:.4f}, z vs P2 {K1N[f]['coma_z_P2']:+.2f}), "
                     f"DF2/DF4 E_obs {K1N[f]['group'][0][1]:+.3f}/{K1N[f]['group'][1][1]:+.3f}, H {K1N[f]['H']['diff']:+.3f} +- {K1N[f]['H']['se']:.3f} "
                     f"(z {K1N[f]['H']['z']:+.2f})" for f in FOOTS)))
RES["K1"] = K1N

P("\n=== K2  CFG939's V_esc,b-based classification reproduced from its own N5 code (exec'd from its text)")
N5ROWS = {}
k2d, k2s, k2t = [], [], []
SYS939 = N9["systems"]()
for fk, a0k939 in FOOT939.items():
    rows = []
    for s in SYS939:
        rows.append(dict(name=s["name"], cls=s["cls"], collapsed=s["collapsed"], **sys_numbers(s, a0k939)))
    N5ROWS[fk] = rows
    ref = {r_["name"]: r_ for r_ in R939["N5"][fk]}
    for r_ in rows:
        if r_["cls"] in ("tidal dwarfs", "DF2/DF4"):
            for k in ("v_in_kms", "T_c_Gyr", "fcrit_pointmass", "gN_over_a0"): k2d.append(abs(r_[k] / ref[r_["name"]][k] - 1))
    for Ls in (24, 100, 300, 1000):
        for vrel in (100.0, 50.0):
            pred = N9["predicted_sides"](rows, Ls, "derived", vrel)
            refp = R939["alignment"]["derived"][f"{fk}|L{Ls}pc|vrel{vrel:.0f}"]["pred"]
            # AMENDMENT A1 (523a09954): (ii-a) sides == JSON in all 16 cells; (ii-b) TDGs and DF2/DF4 BELOW at v_rel 100;
            # (ii-c) DF2/DF4 BELOW at v_rel 50 (the TDGs' MIXED there is CFG939's own record, reported)
            k2s.append(pred == refp and pred["DF2/DF4"] == "BELOW" and (vrel != 100.0 or pred["tidal dwarfs"] == "BELOW"))
            k2t.append((fk, Ls, vrel, pred["tidal dwarfs"], pred["DF2/DF4"]))
vt = {r_["name"]: r_["v_in_kms"] for r_ in N5ROWS["canonical"] if r_["cls"] in ("tidal dwarfs", "DF2/DF4")}
KOK.append(check("K2 (A1) CFG939 N5 rows (v_in = V_esc,b, T_c, f_crit, g_N/a0) for 6 TDGs + DF2/DF4 == cfg939_results.json (rel <= 1e-9); derived "
                 "sides == JSON in all 16 cells; TDGs and DF2/DF4 BELOW at v_rel 100; DF2/DF4 BELOW at 50", max(k2d) <= 1e-9 and all(k2s) and len(k2s) == 16,
                 f"max rel diff {max(k2d):.1e}; cells passing {sum(k2s)}/16; TDGs at v_rel 50: {sorted(set(t[3] for t in k2t if t[2] == 50.0))} "
                 f"(reported, A1); V_esc,b (canonical) " + ", ".join(f"{k} {v:.1f}" for k, v in vt.items()) + " km/s"))
RES["K2"] = dict(v_in_canonical=vt, max_rel=max(k2d), cells_passing=int(sum(k2s)), cells=k2t)

P("\n=== K3  engine: point-mass identity with CFG939, N4 t=0+ unbound fractions, Plummer law IC")
rng = np.random.default_rng(948)
rL9, dmL9 = N9["law_ic"]()
bp1 = bary("point", 1.0)
rLm, dmLm = law_ic(N9["MCORE"], bp1[0])
rr = np.sort(rng.uniform(1.2, 60.0, NSH)); rng.shuffle(rr); vv = rng.normal(0, 0.05, NSH); dmx = dmL9
a9, o9 = N9["sph_accel"](rr.copy(), dmx, 0.7, True); am, om = accel(rr.copy(), dmx, N9["MCORE"], bary("point", 0.7)[0])
E9 = N9["sph_energy"](rr, vv, dmx, 0.7, True); Em = energy(rr, vv, dmx, N9["MCORE"], bary("point", 0.7)[1])
Etf9, Eq9 = N9["shell_energies"](rr, vv, dmx, 0.7, o9); Etfm, Eqm = shell_E(rr, vv, dmx, N9["MCORE"], bary("point", 0.7)[1], om)
def _nrm(x, y): return float(np.max(np.abs(np.asarray(x) - np.asarray(y))) / np.max(np.abs(np.asarray(y))))
k3a = max(float(np.max(np.abs(rLm / rL9 - 1))), abs(dmLm / dmL9 - 1), _nrm(am, a9), abs(Em / E9 - 1), _nrm(Etfm, Etf9), _nrm(Eqm, Eq9))
KOK.append(check("K3a point-mass mode == CFG939's law_ic / sph_accel / sph_energy / shell_energies (rel <= 1e-12)", k3a <= 1e-12, f"max rel {k3a:.1e}"))
k3b = []
for fs in ("0.5", "0.6", "0.7", "0.8", "0.9"):
    _, Eq0 = shell_E(rLm, np.zeros(NSH), dmLm, N9["MCORE"], bary("point", 1 - float(fs))[1], np.argsort(rLm))
    k3b.append((fs, float(np.mean(Eq0 > 0)), R939["N4"][fs]["unbound_t0_Eq"]))
KOK.append(check("K3b point-mass t=0+ unbound fractions (co-moving E_q > 0) == CFG939 N4 for f 0.5-0.9", all(abs(a_ - b_) <= 1e-12 for _, a_, b_ in k3b),
                 "; ".join(f"f {fs}: {a_:.3f} (CFG939 {b_:.3f})" for fs, a_, b_ in k3b)))
AGRID = [5.0, 7.0, 9.5]
Aall = {f: {UNIV[i]["name"]: A_of(UNIV[i], f) for i in IC} for f in FOOTS}
amin = min(min(v.values()) for v in Aall.values()); amax = max(max(v.values()) for v in Aall.values())
while amin < min(AGRID): AGRID.insert(0, math.floor(amin * 2) / 2)
while amax > max(AGRID): AGRID.append(math.ceil(amax * 2) / 2)
k3c = []
for A_ in AGRID:
    for Mpre in (1.0, 2.0):
        b_ = bary("plummer", Mpre, A_); mc_ = float(m_law_b(RMIN, b_[0])); r_, dm_ = law_ic(mc_, b_[0])
        a_, _ = accel(r_, dm_, mc_, b_[0]); k3c.append(float(np.max(np.abs(a_) / (b_[0](r_) / r_ ** 2))))
KOK.append(check("K3c Plummer law IC: |force| <= 1e-10 g_N (each A of the grid; M_b 1 and 2)", max(k3c) <= 1e-10, f"max {max(k3c):.1e}"))
KOK.append(check("K4a A-grid covers every admitted Coma UDG's A = R_e/r_M on both footings (extended mechanically if not)",
                 min(AGRID) <= amin and max(AGRID) >= amax,
                 f"A range {amin:.2f}-{amax:.2f}; grid {AGRID}; per footing " + "; ".join(f"{f} {min(v.values()):.2f}-{max(v.values()):.2f}" for f, v in Aall.items())))
RES["A_grid"] = AGRID; RES["A_per_galaxy"] = Aall
k4b = (_mb is not None and _mc is not None and float(_mb.group(1)) == BETA["kT_keV"] and float(_mb.group(2)) == BETA["rc_kpc"]
       and float(_mb.group(3)) == BETA["beta"] and float(_mb.group(4)) == BETA["mu"] and float(_mc.group(1)) == BETA["m_p"]
       and float(_mc.group(2)) == BETA["keV"])
k4c = []
for f in FOOTS:
    G = evaluate(f)
    for i in IC + IG:
        r12 = (4.0 / 3.0) * G["Re"][i] * 1e3 * 3.0857e16
        sN = math.sqrt(r12 * G["gb"][i] / 3) / 1e3
        k4c.append(abs(-math.log(float(nu_e(np.array([G["gb"][i] / A0[f]]))[0])) - 2 * math.log(sN / G["sl"][i])))
KOK.append(check("K4b L23's Coma beta-model constants == the lane's; E_N,i = -ln nu_e(g_bar/a0) == 2 ln(sigma_N/sigma_law) (<= 1e-12)",
                 k4b and max(k4c) <= 1e-12, f"constants {'equal' if k4b else 'DIFFER'}; max |dE_N| {max(k4c):.1e}; "
                 f"g_host(1 Mpc) = {g_host(1000.0):.3e} m/s^2 ({g_host(1000.0) / A0['canonical']:.3f} a0 canonical)"))
K_ALL = all(KOK); RES["K_all_shared"] = K_ALL
if not K_ALL:
    P("  A K-test failed: per criteria section 7 the lane stops; no class is reported."); RES["class"] = None; finish(2)

# ===================================================================================================================== MODE K
if MODE == "K":
    P("\n=== K3e  f = 0 control (A = 5, t = 200): static law state")
    oc = engine_run(5.0, 0.0, dt=0.02, tq_mult=200.0 / 83.0)
    k3e = abs(oc["E0plus_engine"]) <= 0.01 and abs(oc["maxE_after_Tq"]) <= 0.01 and abs(oc["minE_after_Tq"]) <= 0.01 and oc["dE_rel"] <= 1e-6
    KOK.append(check("K3e f = 0 control keeps |E(t)| <= 0.01 and |dE/E| <= 1e-6 (short K-mode run)", k3e,
                     f"E(0) {oc['E0plus_engine']:+.4f}, E range after T_q [{oc['minE_after_Tq']:+.4f}, {oc['maxE_after_Tq']:+.4f}], dE/E {oc['dE_rel']:.1e}"))
    RES["K_all"] = all(KOK); P(f"\n  K-stage {'ALL PASS' if RES['K_all'] else 'FAILED'}")
    finish(0 if RES["K_all"] else 2)

# ===================================================================================================================== MODE engine
def rj_table(f, key):
    return {UNIV[i]["name"]: r_jacobi(UNIV[i], DIST[UNIV[i]["name"]][key], f) for i in IC11}
if MODE == "engine":
    P("\n=== ENGINE  sudden uniform baryon loss f at t = 0 in the exact S2 + S3 Lagrangian shell dynamics (gamma 0, CFG939 kernel);"
      " Plummer baryons, current M_b = 1, scale A; E(t) at r12 = (4/3) A relative to the CURRENT baryons' law")
    P(f"    grid A {AGRID}, f (0, 0.1, ..., 0.8); W1 = mean over [T_q, 10 T_q] (PRIMARY); N {NSH}, R0 {R0}, RMIN {RMIN}")
    FG = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.65, 0.7, 0.8]
    GRID = {}; kd, kf, kg, ke = [], [], [], []
    P(f"  {'A':>4s} {'f':>5s} {'T_q':>7s} {'dt':>7s} {'E(0+) eng':>9s} {'closed':>8s} {'W0':>8s} {'W1':>8s} {'max>Tq':>8s} {'unb0':>6s} {'esc':>6s} {'dE/E':>8s}")
    for A_ in AGRID:
        for f_ in FG:
            o = run_with_rule(A_, f_); GRID[f"A{A_}|f{f_}"] = o
            P(f"  {A_:4.1f} {f_:5.2f} {o['Tq']:7.1f} {o['dt']:7.4f} {o['E0plus_engine']:+9.4f} {o['E0plus_closed']:+8.4f} {o['W0']:+8.4f} {o['W1']:+8.4f} "
              f"{o['maxE_after_Tq']:+8.4f} {o['unbound_t0']:6.3f} {o['escaping_end']:6.3f} {o['dE_rel']:8.1e}  [{time.time() - T0:.0f} s]")
            kd.append(abs(o["E0plus_engine"] - o["E0plus_closed"])); kf.append(o["dE_rel"])
            if f_ == 0.0: ke.append(max(abs(o["E0plus_engine"]), abs(o["maxE_after_Tq"]), abs(o["minE_after_Tq"])) <= 0.01 and o["dE_rel"] <= 1e-6)
            else: kg.append(o["E0plus_engine"] > 0)
    KOK.append(check("K3d engine E(0+) == closed form within 0.01 (every grid run)", max(kd) <= 0.01, f"max |diff| {max(kd):.4f}"))
    KOK.append(check("K3e f = 0 controls: |E(t)| <= 0.01 and |dE/E| <= 1e-6 (each A)", all(ke), f"{sum(ke)}/{len(ke)}"))
    KOK.append(check("K3f every grid run |dE/E| <= 1e-3 after <= 3 dt halvings", max(kf) <= 1e-3, f"max {max(kf):.1e}"))
    KOK.append(check("K3g frozen-medium tooth: E(0+) > 0 for every f > 0 (the measure registers a surplus)", all(kg), f"{sum(kg)}/{len(kg)}"))
    cand = {k: v["W1"] for k, v in GRID.items() if v["f"] > 0}
    kmax = max(cand, key=cand.get); C_dyn = cand[kmax]; E_ceil = max(0.0, C_dyn)
    P(f"\n  C_dyn = max over (A, f > 0) of W1 = {C_dyn:+.4f} at {kmax}  ->  E_ceil = max(0, C_dyn) = {E_ceil:+.4f}")
    P("  W1 by f (max over A): " + ", ".join(f"f {f_}: {max(GRID[f'A{A_}|f{f_}']['W1'] for A_ in AGRID):+.4f}" for f_ in FG[1:]))
    P("  W0 (first period, transient) by f (max over A): " + ", ".join(f"f {f_}: {max(GRID[f'A{A_}|f{f_}']['W0'] for A_ in AGRID):+.4f}" for f_ in FG[1:]))
    # TT reported variant (tides): absorbing boundary at r_J, A = 7, r_J/r_M = median over the 9 admitted (canonical, dmean)
    rjm = rj_table("canonical", "dmean")
    rM = {UNIV[i]["name"]: math.sqrt(GK * UNIV[i]["Ms"] / a0k("canonical")) for i in IC}
    rj_over_rM = float(np.median([rjm[n] / rM[n] for n in rM]))
    P(f"\n  TT (reported): absorbing boundary at r_J = {rj_over_rM:.2f} r_M (median over the 9 admitted, canonical, dmean), A = 7")
    TT = {}
    for f_ in FG:
        o = run_with_rule(7.0, f_, absorb=rj_over_rM); TT[f"f{f_}"] = o
        P(f"    f {f_:4.2f}: W1 {o['W1']:+.4f}, W0 {o['W0']:+.4f}, E(0+) {o['E0plus_engine']:+.4f}, shells kept at end {o['n_kept_end']}/{NSH}  [{time.time() - T0:.0f} s]")
    RES.update(grid=GRID, C_dyn=C_dyn, C_dyn_at=kmax, E_ceil=E_ceil, TT=dict(rJ_over_rM=rj_over_rM, runs=TT))
    RES["K_all"] = all(KOK); P(f"\n  engine K {'ALL PASS' if RES['K_all'] else 'FAILED'}")
    finish(0 if RES["K_all"] else 2)

# ===================================================================================================================== Q1 machinery
ENG = J("CFG948_nocapture_vs_udgs", "cfg948_results_engine.json")
if not ENG.get("K_all"):
    P("  engine K failed or missing: no ceiling, the lane stops."); finish(2)
E_CEIL = float(ENG["E_ceil"]); RES["E_ceil"] = E_CEIL; RES["C_dyn"] = ENG["C_dyn"]
P(f"\n  derived ceiling (engine): C_dyn {ENG['C_dyn']:+.4f} at {ENG['C_dyn_at']} -> E_ceil = {E_CEIL:+.4f}")
RJ = {f: {k: rj_table(f, k) for k in ("dmean", "dproj")} for f in FOOTS}
TRUNC = {f: {k: {n: trunc_ratio(RJ[f][k][n] / next(u["Re"] for u in UNIV if u["name"] == n)) for n in RJ[f][k]} for k in RJ[f]} for f in FOOTS}
R_UNTR = trunc_ratio(float("inf"))[0]

def est_T(f, key, sig_of=None):
    """S-T_k: light truncated at r_J(D_k); r12 = (4/3) R_e x ratio_T / ratio_inf; M*, sigma unchanged (Coma only)"""
    G = evaluate(f, dict(sig_of=sig_of)) if sig_of else evaluate(f)
    Re = np.array(G["Re"], float).copy()
    for i in IC11:
        Re[i] = Re[i] * TRUNC[f][key][NAMES[i]][0] / R_UNTR
    D = sealed(f, G["Ms"], Re)[0]
    Eo = 2 * np.log(G["sig"] / D["sl"]); EN = -np.log(nu_e(D["gb"] / A0[f]))
    return Eo, EN
def EN_of(G, f): return -np.log(nu_e(np.asarray(G["gb"]) / A0[f]))
VARS = {"S-M+": dict(mfac=10 ** 0.2), "S-M-": dict(mfac=10 ** -0.2),
        "S-D-": dict(dfac=lambda u: 0.95 if u["pop"] == "Coma" else ((17.6 / 20.0) if u.get("key") == "DF2" else 0.95)),
        "S-D+": dict(dfac=lambda u: 1.05 if u["pop"] == "Coma" else ((21.7 / 20.0) if u.get("key") == "DF2" else 1.05)),
        "S-A-": dict(afac=1 / 1.15), "S-A+": dict(afac=1.15)}
def all_variants(f, sig_of=None):
    """per-universe-galaxy (E_obs, E_N, sE) under the primary and every declared variant"""
    out = {}
    G = evaluate(f, dict(sig_of=sig_of)) if sig_of else evaluate(f)
    out["primary"] = (np.array(G["Eo"]), EN_of(G, f), np.array(G["sE"]), G)
    for k, m in VARS.items():
        mm = dict(m)
        if sig_of: mm["sig_of"] = sig_of
        Gv = evaluate(f, mm); out[k] = (np.array(Gv["Eo"]), EN_of(Gv, f), np.array(Gv["sE"]), Gv)
    for key in ("dmean", "dproj"):
        Eo, EN = est_T(f, key, sig_of); out[f"S-T_{key}"] = (Eo, EN, out["primary"][2], None)
    return out
def se_conv(x, sE):
    n = len(x); t_sd = float(np.std(x, ddof=1) / math.sqrt(n)) if n > 1 else float("nan"); t_me = float(math.sqrt(np.sum(np.asarray(sE) ** 2)) / n)
    return (max(t_sd, t_me) if n > 1 else t_me), t_sd, t_me
def classify948(V, idx, eceil, use_sys=True):
    idx = list(idx); n = len(idx)
    Eo, EN, sE, _ = V["primary"]; x = Eo[idx]; s = sE[idx]; xn = (Eo - EN)[idx]
    m = float(np.mean(x)); se, t_sd, t_me = se_conv(x, s); se_n = se_conv(xn, s)[0]
    vm = {k: float(np.mean(V[k][0][idx])) for k in V}; vmn = {k: float(np.mean((V[k][0] - V[k][1])[idx])) for k in V}
    def sysq(d):
        sM = abs(d["S-M+"] - d["S-M-"]) / 2; sA = abs(d["S-A+"] - d["S-A-"]) / 2; sD = abs(d["S-D+"] - d["S-D-"]) / 2
        sT = max(abs(d["S-T_dmean"] - d["primary"]), abs(d["S-T_dproj"] - d["primary"]))
        return dict(s_M=sM, s_A=sA, s_D=sD, s_T=sT, total=math.sqrt(sM ** 2 + sA ** 2 + sD ** 2 + sT ** 2))
    su, sl = sysq(vm), sysq(vmn)
    tu = su["total"] if use_sys else 0.0; tl = sl["total"] if use_sys else 0.0
    d_up = m - eceil; z_up = d_up / math.hypot(se, tu); z_stat = d_up / se
    d_low = -float(np.mean(xn)); z_low = d_low / math.hypot(se_n, tl)
    p_ok = 3 * math.hypot(se, tu) < 0.4 * LN10
    reasons, quals = [], []
    if z_up >= 3: cls = "CONTRADICTED (ABOVE THE CEILING)"
    elif z_low >= 3: cls = "CONTRADICTED (BELOW THE FLOOR)"
    else:
        if n < 5: reasons.append(f"N = {n} < 5")
        if not p_ok: reasons.append(f"power fails: 3 sqrt(se^2 + sigma_sys^2) = {3 * math.hypot(se, tu):.3f} >= 0.921 (a +0.4 dex excess would not be contradicted)")
        cls = "NOT DIAGNOSTIC" if reasons else "CONSISTENT"
        if cls == "CONSISTENT" and max(z_up, z_low) >= 2: quals.append("2-3 sigma tension")
    # H_b / H_a,sup: Newton for every galaxy
    dN = float(np.mean(xn)); zN = dN / math.hypot(se_n, tl)
    return dict(cls=cls, qualifiers=quals, reasons=reasons, N=n, mean_Eobs=m, mean_Eobs_dex=m / LN10, se_obs=se, se_scatter=t_sd, se_meas=t_me,
                mean_EN=float(np.mean(EN[idx])), E_ceil=eceil, Delta_up=d_up, sys_up=su, z_up=z_up, z_stat_up=z_stat, Delta_low=d_low, sys_low=sl,
                se_low=se_n, z_low=z_low, power_ok=p_ok, power_threshold=3 * math.hypot(se, tu), variant_means=vm, variant_means_minus_EN=vmn,
                H_newton=dict(Delta=dN, z=zN, word="EXCLUDED" if zN >= 3 else "NOT EXCLUDED"))
def qline(tag, C):
    return (f"  {tag:30s} {C['cls']}" + (f" [{', '.join(C['qualifiers'])}]" if C["qualifiers"] else "")
            + f" | N {C['N']}: <E_obs> {C['mean_Eobs']:+.3f} ({C['mean_Eobs_dex']:+.3f} dex) vs ceiling {C['E_ceil']:+.3f}; se {C['se_obs']:.3f}, sigma_sys "
              f"{C['sys_up']['total']:.3f} -> z_up {C['z_up']:+.2f} (stat-only {C['z_stat_up']:+.2f}); floor <E_N> {C['mean_EN']:+.3f}, z_low {C['z_low']:+.2f}")

def plant_sig(f, e_plant):
    G = evaluate(f); pl = {}
    for i in IC:
        sp = G["sl"][i] * math.exp(e_plant / 2); fr = sp / UNIV[i]["sig"]
        pl[NAMES[i]] = (sp, UNIV[i]["ep"] * fr, UNIV[i]["em"] * fr)
    return lambda u: pl.get(u["name"])

# ===================================================================================================================== MUTATE
if MODE in ("onlaw", "plus04"):
    want = "CONSISTENT" if MODE == "onlaw" else "CONTRADICTED (ABOVE THE CEILING)"
    ep_ = E_CEIL + (0.0 if MODE == "onlaw" else 0.4 * LN10)
    P(f"\n=== MUTATE {MODE}: sigma_obs := sigma_law x exp(E_plant/2), E_plant = {ep_:+.3f} ln, G-Coma, real fractional errors; required {want} on both footings")
    RES["MUTATE"] = {}; ok = True
    for f in FOOTS:
        V = all_variants(f, plant_sig(f, ep_)); C = classify948(V, IC, E_CEIL)
        RES["MUTATE"][f] = C; ok &= C["cls"] == want
        P(qline(f"[{f}]", C))
        for r_ in C["reasons"]: P(f"      reason: {r_}")
        P(f"      sigma_sys parts: s_M {C['sys_up']['s_M']:.3f}, s_A {C['sys_up']['s_A']:.3f}, s_D {C['sys_up']['s_D']:.3f}, s_T {C['sys_up']['s_T']:.3f}")
    RES["MUTATE_ok"] = bool(ok); RES["MUTATE_required"] = want
    P(f"  MUTATE {MODE}: {'BEHAVES (required class on both footings)' if ok else 'FAILS (required class not reached)'}")
    finish(0 if ok else 1)

# ===================================================================================================================== main
MUTR = {}
for m in ("onlaw", "plus04"):
    pth = os.path.join(HERE, f"cfg948_results_MUTATE_{m}.json")
    MUTR[m] = json.load(_REAL_OPEN(pth)).get("MUTATE_ok") if os.path.exists(pth) else None
RES["MUTATE_status"] = MUTR
P(f"  MUTATE status: onlaw {MUTR['onlaw']}, plus04 {MUTR['plus04']}")

# HUD gas fractions (R6) -- footing independent
_hl = T("real_research", "data", "alfalfa_huds_leisman2017.tsv").splitlines()
_h0 = next(i for i, l in enumerate(_hl) if l.startswith("recno\tAGC"))
_hh = {h: i for i, h in enumerate(_hl[_h0].split("\t"))}
HUD = []
for l in _hl[_h0 + 3:]:
    if not l.strip() or l.startswith("#"): continue
    c = l.split("\t")
    try: HUD.append(dict(logMHI=float(c[_hh["logMHI"]]), gMAG=float(c[_hh["gMAG"]]), Set=c[_hh["Set"]].strip()))
    except ValueError: continue
R6 = {}
for ups in (0.5, 1.0, 2.0):
    for sset in ("all", "R"):
        rows_ = [h for h in HUD if sset == "all" or h["Set"] == "R"]
        fg = np.array([1.33 * 10 ** h["logMHI"] / (1.33 * 10 ** h["logMHI"] + ups * 10 ** (-0.4 * (h["gMAG"] - 5.11))) for h in rows_])
        R6[f"Ups{ups}|{sset}"] = dict(N=len(rows_), median=float(np.median(fg)), frac_above_2_3=float(np.mean(fg > 2 / 3)),
                                      p16=float(np.percentile(fg, 16)), p84=float(np.percentile(fg, 84)))
RES["R6_HUD"] = R6

RES["byfoot"] = {}
for f in FOOTS:
    P(f"\n=== [{f}] a0 = {A0[f]:.4e} m/s^2; ceiling E_ceil = {E_CEIL:+.4f}")
    V = all_variants(f); Eo, EN, sE, G = V["primary"]
    C = classify948(V, IC, E_CEIL)
    final = C["cls"]; labels = []
    if final == "CONSISTENT" and not (MUTR.get("onlaw") and MUTR.get("plus04")):
        final = "NOT DIAGNOSTIC"; labels.append("CONTROL-LIMITED")
    elif final == "NOT DIAGNOSTIC" and not (MUTR.get("onlaw") and MUTR.get("plus04")):
        labels.append("CONTROL-LIMITED")
    P(qline("PRIMARY G-Coma", C))
    for r_ in C["reasons"]: P(f"      reason: {r_}")
    P(f"      sigma_sys (upper) parts: s_M {C['sys_up']['s_M']:.3f}, s_A {C['sys_up']['s_A']:.3f}, s_D {C['sys_up']['s_D']:.3f}, s_T {C['sys_up']['s_T']:.3f}; "
      f"se_obs {C['se_obs']:.3f} (scatter {C['se_scatter']:.3f}, measurement {C['se_meas']:.3f})")
    P(f"      H_b (all born in the cluster) and H_a,sup (field-born, f > f_crit): Newton; <E_obs - E_N> {C['H_newton']['Delta']:+.3f}, sigma_sys "
      f"{C['sys_low']['total']:.3f}, z_N {C['H_newton']['z']:+.2f} -> {C['H_newton']['word']}")
    # P-c: DF2/DF4 per galaxy vs Newton
    pc = []
    for i in IG:
        e_ = UNIV[i]["em"] if Eo[i] > EN[i] else UNIV[i]["ep"]; s_ = 2 * e_ / UNIV[i]["sig"]
        pc.append(dict(name=NAMES[i], E_obs=float(Eo[i]), E_N=float(EN[i]), sE=s_, z=float((Eo[i] - EN[i]) / s_)))
        P(f"      P-c {NAMES[i]}: E_obs {Eo[i]:+.3f} vs Newton E_N {EN[i]:+.3f} (+- {s_:.3f}): z {pc[-1]['z']:+.2f}")
    pm = float(np.mean([p["E_obs"] - p["E_N"] for p in pc])); pse = math.sqrt(sum(p["sE"] ** 2 for p in pc)) / 2
    P(f"      P-c pair: <E_obs - E_N> {pm:+.3f} +- {pse:.3f} ln (CFG936 reported +0.021 +- 0.539 with its own estimator)")
    # environment difference
    xg = Eo[IG]; sg = np.array([(UNIV[i]["ep"] + UNIV[i]["em"]) / UNIV[i]["sig"] for i in IG])
    se_g = se_conv(xg, sg)[0]; Dobs = C["mean_Eobs"] - float(np.mean(xg)); seD = math.hypot(C["se_obs"], se_g)
    Dmin = C["mean_EN"] - float(np.mean(EN[IG])); Dmax = E_CEIL - float(np.mean(EN[IG]))
    dist_out = (Dobs - Dmax) if Dobs > Dmax else ((Dmin - Dobs) if Dobs < Dmin else 0.0)
    zD = dist_out / seD; zDs = dist_out / math.hypot(seD, C["sys_up"]["total"])
    wD = ("ABOVE THE FRAMEWORK'S MAXIMUM" if (Dobs > Dmax and zD >= 3) else ("BELOW THE FRAMEWORK'S MINIMUM" if (Dobs < Dmin and zD >= 3)
          else ("INSIDE" if dist_out == 0 else "WITHIN 3 sigma")))
    P(f"      environment difference Coma - group: D_obs {Dobs:+.3f} +- {seD:.3f}; framework interval [{Dmin:+.3f}, {Dmax:+.3f}]; outside by {dist_out:+.3f} "
      f"-> z_D {zD:+.2f} stat (with Coma sigma_sys {zDs:+.2f}) -> {wD}")
    # Q2 sign verdict
    grp_ok = float(np.mean(EN[IG])) < 0 and float(np.mean(xg)) < 0
    if E_CEIL > 0:
        q2 = "PREDICTED" if (C["z_up"] < 3 and grp_ok) else ("CONTRADICTED" if C["z_up"] >= 3 else "NOT PREDICTED, NOT EXCLUDED")
    else:
        q2 = "CONTRADICTED" if C["cls"].startswith("CONTRADICTED (ABOVE") else "NOT PREDICTED, NOT EXCLUDED"
    P(f"      Q2 sign: group below the law {'PREDICTED' if grp_ok else 'NOT PREDICTED'} (Newton <E_N> {np.mean(EN[IG]):+.3f}, observed {np.mean(xg):+.3f}); "
      f"Coma above the law {'FORBIDDEN' if E_CEIL <= 0 else 'ALLOWED up to the ceiling'} by the derived dynamics (observed {C['mean_Eobs']:+.3f}) -> {q2}")
    # R1 statistics-only + per-variant
    C1 = classify948(V, IC, E_CEIL, use_sys=False)
    r1v = {}
    for k in V:
        if k == "primary": continue
        Vk = dict(V); Vk["primary"] = V[k] if V[k][3] is not None else (V[k][0], V[k][1], V[k][2], None)
        Ck = classify948(Vk, IC, E_CEIL, use_sys=False); r1v[k] = dict(cls=Ck["cls"], z_stat=Ck["z_stat_up"], mean=Ck["mean_Eobs"])
    frag = [k for k in r1v if r1v[k]["cls"] != C1["cls"]]
    P(qline("R1 statistics-only", C1) + (f"  FRAGILE (flipped by {frag})" if frag else ""))
    P("      R1 per variant (stat-only z_up): " + "; ".join(f"{k} {v['z_stat']:+.2f} ({v['cls'].split(' (')[0]})" for k, v in r1v.items()))
    # R2 L23 weighting
    w = 1 / sE[IC] ** 2; mw = float(np.sum(w * Eo[IC]) / np.sum(w)); sw = float(1 / math.sqrt(np.sum(w)))
    R2 = dict(mean=mw, se=sw, z_stat=(mw - E_CEIL) / sw, z_sys=(mw - E_CEIL) / math.hypot(sw, C["sys_up"]["total"]))
    P(f"  R2 L23 weighting (sE^-2): <E_obs> {mw:+.3f} +- {sw:.3f} -> z {R2['z_stat']:+.2f} stat, {R2['z_sys']:+.2f} with sigma_sys")
    # R3 all 11 Coma
    C3 = classify948(V, IC11, E_CEIL); P(qline("R3 all 11 Coma", C3))
    # R4 H-EX reading (S4 working rule; NOT DERIVABLE per CFG939)
    gb = np.asarray(G["gb"])[IC] / A0[f]
    def ehex(fl): u1 = u_of_g(gb / (1 - fl)); u0 = u_of_g(gb); return np.log((gb + u1) / (gb + u0))
    tgt = C["mean_Eobs"]
    fstar = brentq(lambda fl: float(np.mean(ehex(fl))) - tgt, 0.0, 0.9999) if float(np.mean(ehex(0.9999))) > tgt else None
    fh = R6["Ups1.0|all"]["median"]
    R4 = dict(f_star=fstar, E_HEX_at_2_3=float(np.mean(ehex(2 / 3))), E_HEX_at_HUD_median=float(np.mean(ehex(fh))), HUD_median_fgas=fh,
              kernel_note_max_ln_nu_simple_over_nu_e=float(np.max(np.abs(np.log((0.5 + np.sqrt(0.25 + 1 / gb)) / nu_e(gb))))))
    P(f"  R4 H-EX reading (NOT DERIVABLE, CFG939): frozen free cold share of lost baryons at r12: <E_HEX> {R4['E_HEX_at_2_3']:+.3f} at f = 2/3, "
      f"{R4['E_HEX_at_HUD_median']:+.3f} at the HUD median f_gas {fh:.2f}; f* for <E_HEX> = <E_obs> ({tgt:+.3f}): "
      + (f"{fstar:.3f}" if fstar is not None else "none") + f"  [max |ln(nu_simple/nu_e)| over G-Coma {R4['kernel_note_max_ln_nu_simple_over_nu_e']:.1e}]")
    # R5, R7, R8, R9 per galaxy
    P(f"  per galaxy (R7; R5 strict D-T hover ratio; R8 stiffness 'ram' bound at L* = 1 kpc):")
    P(f"  {'galaxy':22s} {'E_obs':>7s} {'sE':>5s} {'E_N':>7s} {'z_ceil':>6s} {'z_N':>6s} {'Vesc':>5s} {'T_c':>5s} {'fcrit':>5s} {'rJ/r12 m':>8s} {'rJ/r12 p':>8s} "
      f"{'Tr m':>5s} {'Tr p':>5s} {'u_h/gNmx m':>10s} {'p':>7s} {'a_gam/g':>8s}")
    PG = []
    for i in IC11:
        u = UNIV[i]; nm = u["name"]; D_ = DIST[nm]
        srow = dict(name=nm, cls="Coma UDG", prof=plummer939(u["Ms"], u["Re"]), r_obs=1.305 * u["Re"], collapsed=False)
        sn = sys_numbers(srow, FOOT939[f])
        r12k = (4.0 / 3.0) * u["Re"]; r12m = r12k * KPC
        gbar_i = float(G["gb"][i]); x_ = float(u_of_g(gbar_i / A0[f])); fc = float(fcrit_x(x_))
        rjm, rjp = RJ[f]["dmean"][nm], RJ[f]["dproj"][nm]
        gnmax = 2 * G_SI * u["Ms"] * MSUN / (3 * math.sqrt(3) * (u["Re"] * KPC) ** 2)
        uh = {k: g_host(D_[k]) * A0[f] / (g_host(D_[k]) + A0[f]) for k in ("dmean", "dproj")}
        rr_ = D_["dmean"] * KPC; agam = (1.0 * KPC) ** 2 * CBETA * rr_ * (rr_ ** 2 + 5 * RC ** 2) / (rr_ ** 2 + RC ** 2) ** 3
        glaw = float(nu_e(np.array([gbar_i / A0[f]]))[0]) * gbar_i
        zc = (Eo[i] - E_CEIL) / sE[i]; zn = (Eo[i] - EN[i]) / sE[i]
        row = dict(name=nm, admitted=bool(ADM[i]), E_obs=float(Eo[i]), sE=float(sE[i]), E_N=float(EN[i]), z_vs_ceiling=float(zc), z_vs_newton=float(zn),
                   V_esc_b_kms=sn["v_in_kms"], T_c_Gyr=sn["T_c_Gyr"], fcrit_r12=fc, x_r12=x_, rJ_kpc=dict(dmean=rjm, dproj=rjp),
                   rJ_over_r12=dict(dmean=rjm / r12k, dproj=rjp / r12k), trunc_ratio=dict(dmean=TRUNC[f]["dmean"][nm], dproj=TRUNC[f]["dproj"][nm]),
                   u_host_over_gNmax=dict(dmean=uh["dmean"] / gnmax, dproj=uh["dproj"] / gnmax), a_gamma_over_glaw=agam / glaw,
                   cfg939_side_Pa="ON LAW", cfg939_side_Pb_vrel100="ON LAW" if sn["v_in_kms"] >= 100 else "BELOW",
                   cfg939_side_Pb_vrel50="ON LAW" if sn["v_in_kms"] >= 50 else "BELOW")
        PG.append(row)
        P(f"  {nm:22s} {Eo[i]:+7.3f} {sE[i]:5.3f} {EN[i]:+7.3f} {zc:+6.2f} {zn:+6.2f} {sn['v_in_kms']:5.1f} {sn['T_c_Gyr']:5.2f} {fc:5.3f} "
          f"{rjm / r12k:8.2f} {rjp / r12k:8.2f} {TRUNC[f]['dmean'][nm][0]:5.3f} {TRUNC[f]['dproj'][nm][0]:5.3f} {uh['dmean'] / gnmax:10.1f} "
          f"{uh['dproj'] / gnmax:7.1f} {agam / glaw:8.1e}" + ("" if ADM[i] else "  (R3 only)") + (" [Tr capped]" if (TRUNC[f]['dmean'][nm][1] or TRUNC[f]['dproj'][nm][1]) else ""))
    adm_rows = [r_ for r_ in PG if r_["admitted"]]
    P(f"  R9 CFG939 grader: P-a (collapsed) -> ON LAW for all; P-b (debris) at v_rel 100/50 -> "
      f"{sorted(set(r_['cfg939_side_Pb_vrel100'] for r_ in adm_rows))}/{sorted(set(r_['cfg939_side_Pb_vrel50'] for r_ in adm_rows))}; observed side EXCESS "
      f"({sum(r_['E_obs'] > 0 for r_ in adm_rows)}/9 above the law)")
    P(f"  R5 strict D-T: u_host/g_N,max range {min(r_['u_host_over_gNmax']['dmean'] for r_ in adm_rows):.0f}-{max(r_['u_host_over_gNmax']['dmean'] for r_ in adm_rows):.0f} (dmean), "
      f"{min(r_['u_host_over_gNmax']['dproj'] for r_ in adm_rows):.0f}-{max(r_['u_host_over_gNmax']['dproj'] for r_ in adm_rows):.0f} (dproj); "
      f"R8 max a_gamma/g_law {max(r_['a_gamma_over_glaw'] for r_ in adm_rows):.1e}; V_esc,b {min(r_['V_esc_b_kms'] for r_ in adm_rows):.1f}-"
      f"{max(r_['V_esc_b_kms'] for r_ in adm_rows):.1f} km/s; T_c {min(r_['T_c_Gyr'] for r_ in adm_rows):.2f}-{max(r_['T_c_Gyr'] for r_ in adm_rows):.2f} Gyr")
    P(f"  CLASS [{f}]: {final}" + (f" [{', '.join(C['qualifiers'])}]" if C["qualifiers"] else "") + (f"  labels {labels}" if labels else "")
      + f"   |   Q2: {q2}")
    def strip(Cx): return {k: v for k, v in Cx.items()}
    RES["byfoot"][f] = dict(primary=strip(C), final_class=final, labels=labels, P_c=pc, P_c_pair=dict(mean=pm, se=pse),
                            env_difference=dict(D_obs=Dobs, se=seD, interval=[Dmin, Dmax], outside_by=dist_out, z_stat=zD, z_with_sys=zDs, word=wD),
                            Q2=q2, group_sign_predicted=grp_ok, R1=dict(primary=strip(C1), per_variant=r1v, fragile=frag), R2=R2, R3=strip(C3),
                            R4=R4, per_galaxy=PG)

RES["class"] = {f: RES["byfoot"][f]["final_class"] for f in FOOTS}; RES["Q2"] = {f: RES["byfoot"][f]["Q2"] for f in FOOTS}
P(f"\n  R6 HUD gas fractions (Leisman+17): " + "; ".join(f"{k}: N {v['N']}, median {v['median']:.2f}, > 2/3 {v['frac_above_2_3']:.2f}" for k, v in R6.items()))
P(f"\n  CLASSES: canonical {RES['class']['canonical']}; alt {RES['class']['alt']}   Q2: canonical {RES['Q2']['canonical']}; alt {RES['Q2']['alt']}"
  f"   (MUTATE onlaw {MUTR['onlaw']}, plus04 {MUTR['plus04']})")
finish(0)
