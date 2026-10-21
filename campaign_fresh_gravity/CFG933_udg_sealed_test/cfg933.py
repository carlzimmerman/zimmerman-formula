"""CFG933 -- score CFG928's SEALED P2 prediction (velocity-space capture; seal 3fa5a2bfc) on the ultra-diffuse galaxies already
on disk, with the sealed estimator executed from CFG928's own code.
Criteria: FROZEN_CRITERIA.md (dd6dc4f35, committed alone before this script and before any E of this lane).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg933.py
     CFG933_MODE=K -> K only; CFG933_MODE=onlaw|plus04 -> MUTATE plants, outputs named by mode.
Inputs (read only): cfg921.py exec'd read-only up to its MAIN section (and through it CFG919/914/880); cfg928.py's udg_* functions
exec'd from its text; cfg928_results.json (theta, sealed rows, F0); the Coma UDG table (Freundlich+2022, as used by L23/CFG31);
L23_udg_verify.out and CFG31's JSON (K1); cfg657_capture.py's GAL dict (CFG655's frozen DF2/DF4 table).  Nothing downloaded; one core.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, re, json, math, time, resource, contextlib, builtins, warnings
import numpy as np

T0 = time.time()
_REAL_OPEN = builtins.open
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG933_MODE", ""); assert MODE in ("", "K", "onlaw", "plus04")
SUF = {"": "", "K": "_K", "onlaw": "_MUTATE_onlaw", "plus04": "_MUTATE_plus04"}[MODE]
for _e in ("CFG928_MUTATE", "CFG928_KONLY", "CFG921_MUTATE", "CFG921_KONLY", "CFG919_MUTATE", "CFG914_MUTATE", "CFG880_MUTATE",
           "CFG829_MUTATE", "CFG850_MUTATE", "CFG883_MUTATE", "CFG828_MUTATE", "CFG849_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def J(*p):
    with _REAL_OPEN(os.path.join(LANES, *p)) as fh: return json.load(fh)
def T(*p):
    with _REAL_OPEN(os.path.join(REPO, *p)) as fh: return fh.read()
RES = dict(lane="CFG933", criteria="dd6dc4f35", seal="3fa5a2bfc", mode=MODE or "main", checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def jdef(o):
    if hasattr(o, "item"): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
def finish(code):
    RES["runtime_s"] = time.time() - T0; RES["peak_rss_mb"] = rss_mb(); RES["exit_code"] = code
    with _REAL_OPEN(os.path.join(HERE, f"cfg933_results{SUF}.json"), "w") as fh: json.dump(RES, fh, indent=1, default=jdef)
    with _REAL_OPEN(os.path.join(HERE, f"cfg933{SUF}.out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
    sys.exit(code)

FOOTS = ("canonical", "alt"); LN10 = math.log(10.0)
P("CFG933  score CFG928's sealed P2 (velocity-space capture) UDG prediction with the sealed estimator"
  + {"": "", "K": "   [K only]", "onlaw": "   [MUTATE onlaw]", "plus04": "   [MUTATE plus04]"}[MODE])
P("  criteria dd6dc4f35; seal 3fa5a2bfc; kappa = 1/2 FITTED; footings never pooled; isolated EFE-free nu_e law")

# =====================================================================================================================  K-stage
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG933 refuses to write {file!r} from re-executed committed code")
    return _REAL_OPEN(file, mode, *a, **k)
class _Exit(Exception): pass
def _exit(code=0): raise _Exit(code)
def sandbox_exec(path, src, name):
    ns = {"__file__": path, "__name__": name}; buf = io.StringIO(); err = None
    old_open, old_exit = builtins.open, sys.exit
    builtins.open = _ro_open; sys.exit = _exit
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(src, path, "exec"), ns)
    except BaseException as e:                  # noqa: BLE001 -- reported as a K failure
        err = f"{type(e).__name__}: {e}"
    finally:
        builtins.open = old_open; sys.exit = old_exit
    return ns, buf.getvalue(), err

P("\n=== K-stage")
F921 = os.path.join(LANES, "CFG921_excess_selector_posits", "cfg921.py")
with _REAL_OPEN(F921) as _fh: s921 = _fh.read()
_cut = s921.index("\nSTRUCT = {f: {vk: obs_struct(f, vk) for vk in VARS} for f in FOOTS}")
N, _o921, e921 = sandbox_exec(F921, s921[:_cut], "cfg921_ro")
c921 = N.get("RES", {}).get("checks", {})
k0 = e921 is None and bool(N.get("K_ALL")) and len(c921) >= 7 and all(v["ok"] for v in c921.values())
KOK = [check("K0 cfg921.py exec'd read-only to its MAIN section (as cfg928.py does): its own K-checks pass", k0,
             f"{sum(v['ok'] for v in c921.values())}/{len(c921)} CFG921 checks pass" + (f"; error {e921}" if e921 else ""))]
if not k0:
    P("  K0 failed: lane stops (criteria section 8)."); RES["class"] = None; finish(2)
dw_pred, nu_e, A0, N880, DWD = N["dw_pred"], N["nu_e"], N["A0"], N["N880"], N["DWD"]

# CFG928's own sealed-path functions, exec'd from its text unchanged
F928 = os.path.join(LANES, "CFG928_posit_regrade_imf", "cfg928.py")
with _REAL_OPEN(F928) as _fh: s928 = _fh.read()
_i0, _i1 = s928.index("def udg_inputs("), s928.index("# path self-check (added")
NS928 = {"np": np, "math": math, "N880": N880, "N": N, "A0": A0, "nu_e": nu_e, "DWD": DWD, "dw_pred": dw_pred}
exec(compile(s928[_i0:_i1], F928, "exec"), NS928)
udg_inputs, udg_from, udg_E = NS928["udg_inputs"], NS928["udg_from"], NS928["udg_E"]
R928 = J("CFG928_posit_regrade_imf", "cfg928_results.json")
SEALN = R928["sealed_numbers"]
TH = {f: (SEALN[f"P2|{f}"]["theta"], SEALN[f"P2|{f}"]["theta_plus"], SEALN[f"P2|{f}"]["theta_minus"]) for f in FOOTS}
F0 = {f: float(R928["scenarios"]["C1"][f]["observed"]["F0"]["obs"]) for f in FOOTS}
RES["theta"] = TH; RES["F0_dwarf_class_mean"] = F0

def sealed(f, Ms, Re_kpc, Mg=None, th=None):
    """CFG928's sealed path: sigma_law, E_pred (theta, theta+, theta-) for arrays of (M*, R_e kpc, M_g,in)."""
    Ms = np.asarray(Ms, float); Re_kpc = np.asarray(Re_kpc, float); Mg = np.zeros_like(Ms) if Mg is None else np.asarray(Mg, float)
    D = udg_inputs(f, Ms, Re_kpc, Mg); t0, tp, tm = TH[f] if th is None else th
    return D, udg_E("P2", t0, f, D, 10.0), udg_E("P2", tp, f, D, 10.0), udg_E("P2", tm, f, D, 10.0)

# ---- K2: CFG928's sealed band reproduced from its code
MS_L, RE_L = (3e7, 1e8, 3e8), (1.5, 2.5, 4.0)
k2, k2b = [], {}
for f in FOOTS:
    Ms_g, Re_g = np.meshgrid(MS_L, RE_L, indexing="ij"); Ms_v, Re_v = Ms_g.ravel(), Re_g.ravel()
    D, Ef, Efp, Efm = sealed(f, Ms_v, Re_v)
    rows = SEALN[f"P2|{f}"]["udg_rows"]; assert len(rows) == len(Ms_v)
    for i, r in enumerate(rows):
        assert r["Mstar"] == Ms_v[i] and r["Re_kpc"] == Re_v[i]
        mine = dict(E_free=Ef[i], s_pred=abs(Efp[i] - Efm[i]) / 2, sigma_law=D["sl"][i], log_gbar=math.log10(D["gb"][i]),
                    sigma_pred_star=D["sl"][i] * math.exp(Ef[i] / 2))
        k2 += [abs(mine[k] / r[k] - 1) for k in mine]
    k2b[f] = (round(float(Ef.min()), 3), round(float(Ef.max()), 3))
th_ok = round(TH["canonical"][0], 4) == 6.9503 and round(TH["alt"][0], 4) == 6.4575
band_ok = k2b["canonical"] == (0.022, 0.140) and k2b["alt"] == (0.016, 0.105)
KOK.append(check("K2 CFG928's sealed band reproduced from CFG928's code (udg_* exec'd from cfg928.py text + cfg921 dw_pred): 9 rows x 2 footings "
                 "(E_free, s_pred, sigma_law, log g_bar, sigma_pred) == cfg928_results.json; theta == seal; band ends == seal",
                 max(k2) <= 1e-12 and th_ok and band_ok,
                 f"max rel diff {max(k2):.1e}; theta {TH['canonical'][0]:.4f} / {TH['alt'][0]:.4f}; band canonical {k2b['canonical']}, alt {k2b['alt']}"))
RES["K2"] = dict(max_rel_diff=max(k2), band=k2b)

# ---- this lane's standalone P2 solver (K3)
G_, MSUN_, PC_ = 6.674e-11, 1.989e30, 3.0857e16
def p2_standalone(f, th, Ms, Re_kpc, Mg=None, sg=10.0):
    Ms = np.asarray(Ms, float); Mg = np.zeros_like(Ms) if Mg is None else np.asarray(Mg, float)
    r12 = (4.0 / 3.0) * np.asarray(Re_kpc, float) * 1e3 * PC_; Mb = Ms / 2 + Mg; gb = G_ * Mb * MSUN_ / r12 ** 2
    y = gb / A0[f]; nu = 1.0 / (-np.expm1(-np.sqrt(y))); phi = 1 - 1 / nu; sl = np.sqrt(r12 * gb * nu / 3) / 1e3; w = (Ms / 2) / Mb
    F = lambda t: np.exp(2 * t) - 1 - phi * (w * (th / (np.exp(t) * sl)) ** 3 + (1 - w) * (th / sg) ** 3)
    lo, hi = np.zeros_like(Ms), np.full_like(Ms, 40.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi); pos = F(mid) > 0; hi = np.where(pos, mid, hi); lo = np.where(pos, lo, mid)
    return 2 * 0.5 * (lo + hi), sl

# ---- data: the Coma table (as L23 / CFG31), the NGC 1052 table (CFG655 via cfg657's GAL dict)
_rows = [l.rstrip("\n").split("\t") for l in T("real_research", "data", "freundlich2022_coma_udgs.tsv").splitlines()
         if l.strip() and not l.startswith("#")]
_hd = {h: i for i, h in enumerate(_rows[0])}
COMA = []
for r in _rows[1:]:
    g = lambda k: float(r[_hd[k]])
    COMA.append(dict(name=r[_hd["name"]], L=g("L_1e8") * 1e8, Re=g("Re_kpc"), ML=g("ML"), sig=g("sig"), esig=g("esig"),
                     elgb=g("elgbar"), elgo=g("elgobs"), lgb_pub=g("lgbar"), lgo_pub=g("lgobs")))
_s657 = T("campaign_fresh_gravity", "CFG657_trail_capture_rule", "cfg657_capture.py")
_g0 = _s657.index("GAL = {"); _g1 = _s657.index("\n}\n", _g0) + 2
GAL657 = eval(compile(_s657[_g0 + len("GAL = "):_g1], "cfg657_GAL", "eval"), {"dict": dict, "__builtins__": {}})
# CFG655's printed frozen table (FROZEN_CRITERIA section on inputs), copied for the K4 equality
T655 = {"DF2": dict(Ms=2.0e8, Re=2.0, Dref=20.0, obs=(8.5, 2.3, 3.1)), "DF4": dict(Ms=1.5e8, Re=1.6, Dref=20.0, obs=(6.3, 2.5, 1.6))}

UNIV = []
for c in COMA:
    UNIV.append(dict(name=c["name"], pop="Coma", Ms=c["L"] * c["ML"], L=c["L"], ML=c["ML"], Re=c["Re"], sig=c["sig"], ep=c["esig"],
                     em=c["esig"], label=True, label_src="Freundlich+2022 table header (Coma-cluster UDGs)", gas_free=True,
                     gas_src="L23/CFG31 R1: stars only, the current baryons", press=True, D=None))
for nm in ("DF2", "DF4", "DF9", "LEDA"):
    g = GAL657[nm]; s, up, lo = g["obs"]
    UNIV.append(dict(name=("NGC1052-" + nm) if nm != "LEDA" else "LEDA4014647", key=nm, pop="NGC1052", Ms=g["Ms"], L=None, ML=None,
                     Re=g["Re"], sig=s, ep=up, em=lo, label=nm in ("DF2", "DF4"),
                     label_src="the seal's disclosure ('group UDGs (DF2/DF4)')" if nm in ("DF2", "DF4") else "no UDG label on disk",
                     gas_free=True, gas_src="CFG655: Gas: none", press=True, D=g["D"], Dref=g["Dref"]))
CAL_NAMES = set(DWD["canonical"]["names"])
def norm_name(s): return re.sub(r"[^a-z0-9]", "", s.lower())
CALN = {norm_name(x) for x in CAL_NAMES}
for u in UNIV:
    u["S1"] = u["Re"] >= 1.5; u["S2"] = u["gas_free"]; u["S3"] = u["press"]; u["S4"] = 3e7 <= u["Ms"] <= 3e8
    u["S5"] = norm_name(u["name"]) not in CALN and norm_name(u.get("key", u["name"])) not in CALN
    u["admit"] = u["label"] and u["S1"] and u["S2"] and u["S3"] and u["S4"] and u["S5"]
    u["why_out"] = [k for k in ("S1", "S2", "S3", "S4", "S5") if not u[k]] + ([] if u["label"] else ["no UDG label"])
EXPECT_IN = {"DFX1", "J125848.94+281037.1", "J125904.20+281507.7", "J125929.89+274303.0", "J125937.23+274815.2", "J130005.40+275333.0",
             "J130026.26+272735.2", "J130028.34+274820.5", "J130038.63+272835.3", "NGC1052-DF2", "NGC1052-DF4"}
ADM = np.array([u["admit"] for u in UNIV]); POP = np.array([u["pop"] for u in UNIV]); NAMES = [u["name"] for u in UNIV]

# ---- K4: inputs, constants, membership
k4a = all(GAL657[k]["Ms"] == T655[k]["Ms"] and GAL657[k]["Re"] == T655[k]["Re"] and GAL657[k]["Dref"] == T655[k]["Dref"]
          and tuple(GAL657[k]["obs"]) == T655[k]["obs"] and GAL657[k]["D"] == GAL657[k]["Dref"] for k in ("DF2", "DF4"))
_l23 = T("fable_independent_2026", "L23_udg_verify.py")
_cl23 = re.search(r"G = ([0-9.e+-]+); MSUN = ([0-9.e+-]+); kpc = ([0-9.e+-]+);", _l23)
k4b = (_cl23 is not None and float(_cl23.group(1)) == N880["G"] == G_ and float(_cl23.group(2)) == N880["Msun"] == MSUN_
       and abs(float(_cl23.group(3)) / (1e3 * N880["PC"]) - 1) < 1e-15 and N880["PC"] == N["PC"] == PC_)
mem = {u["name"] for u in UNIV if u["admit"]}
k4c = mem == EXPECT_IN
KOK.append(check("K4 inputs: DF2/DF4 == cfg657 GAL dict == CFG655 printed table; G, Msun, pc == L23's == CFG880's; membership == criteria section 3",
                 k4a and k4b and k4c, f"tables {'equal' if k4a else 'DIFFER'}; constants {'equal' if k4b else 'DIFFER'}; admitted {len(mem)} "
                 f"({'== expectation' if k4c else 'MISMATCH: ' + str(sorted(mem ^ EXPECT_IN))}); calibration-set overlap "
                 f"{[u['name'] for u in UNIV if not u['S5']] or 'none'}"))

# ---- K1: L23's committed isolated offsets through this lane's own code; CFG31's C1 and R1
A0_H9 = {"canonical": 9.36e-11, "alt": 1.13e-10}
def l23_offsets(a0, kern=None):
    kern = nu_e if kern is None else kern
    out, err = [], []
    for c in COMA:
        r12 = 4.0 / 3.0 * c["Re"] * 3.0857e19; Mst = c["L"] * c["ML"] * MSUN_
        gobs = 3.0 * (c["sig"] * 1e3) ** 2 / r12; gbar = G_ * (Mst / 2.0) / r12 ** 2
        out.append(math.log10(gobs) - math.log10(float(kern(gbar / a0)) * gbar)); err.append(math.hypot(c["elgo"], c["elgb"]))
    return np.array(out), np.array(err)
# AMENDMENT A1: CFG31's R1 used the contract kernel nu_mono (FP1's committed slice, as CFG4_common execs it)
from scipy.optimize import brentq as _brentq
_FP1 = T("real_research", "derivation_chain_2026", "FP1_static_sector.py")
_f0, _f1 = _FP1.index("def _h_rar(y):"), _FP1.index("KER, KNAME = ")
_NSFP1 = {"np": np, "math": math, "brentq": _brentq}
exec(compile(_FP1[_f0:_f1], "FP1_static_sector_slice", "exec"), _NSFP1)
nu_mono_fp1 = _NSFP1["nu_mono"]
def wmean(x, e):
    w = 1.0 / np.asarray(e) ** 2; return float(np.sum(w * x) / np.sum(w)), float(1 / math.sqrt(np.sum(w)))
_o23 = T("fable_independent_2026", "L23_udg_verify.out")
c23 = {"canonical": float(re.search(r"canonical isolated ([+-][0-9.]+)", _o23).group(1)),
       "alt": float(re.search(r"alt\s+ISOLATED ([+-][0-9.]+)", _o23).group(1))}
R31 = J("CFG31_coma_udgs_under_b_results.json")
c31m = R31["numbers"]["C1"]["mine"]; c31r = {f: R31["numbers"]["reported"]["R1_stars_only"][f]["mean"] for f in FOOTS}
k1 = {}
for f in FOOTS:
    oh, eh = l23_offsets(A0_H9[f]); oc, ec = l23_offsets(A0[f]); om, em_ = l23_offsets(A0[f], nu_mono_fp1)
    k1[f] = dict(h9=wmean(oh, eh)[0], campaign=wmean(oc, ec)[0], campaign_nu_mono=wmean(om, em_)[0], stat=wmean(oc, ec)[1])
k1ok = all(abs(k1[f]["h9"] - c23[f]) <= 6e-4 and abs(k1[f]["h9"] - c31m[f]) <= 1e-9 and abs(k1[f]["campaign_nu_mono"] - c31r[f]) <= 1e-12
           and abs(k1[f]["campaign"] - k1[f]["campaign_nu_mono"]) <= 1e-8 for f in FOOTS)
KOK.append(check("K1 L23's committed isolated offsets (stars only, inverse-variance) reproduced by this lane's own code; CFG31 C1 'mine'; "
                 "CFG31 R1 through CFG31's own kernel nu_mono (A1: 3a) and the nu_e path within 1e-8 of it (A1: 3b)",
                 k1ok, "; ".join(f"{f}: h9-a0 {k1[f]['h9']:+.4f} (L23 out {c23[f]:+.4f}; CFG31 C1 diff {abs(k1[f]['h9'] - c31m[f]):.1e}), "
                                 f"campaign-a0 nu_mono {k1[f]['campaign_nu_mono']:+.6f} (CFG31 R1 diff {abs(k1[f]['campaign_nu_mono'] - c31r[f]):.1e}), "
                                 f"nu_e - nu_mono {k1[f]['campaign'] - k1[f]['campaign_nu_mono']:+.1e}" for f in FOOTS)))
RES["K1"] = dict(mine=k1, L23_out=c23, CFG31_C1=c31m, CFG31_R1=c31r)

# ---- K3: standalone solver == CFG928 path (grid + every universe galaxy)
k3 = []
Ms_u = np.array([u["Ms"] for u in UNIV]); Re_u = np.array([u["Re"] for u in UNIV])
for f in FOOTS:
    for Ms_t, Re_t in ((np.meshgrid(MS_L, RE_L, indexing="ij")[0].ravel(), np.meshgrid(MS_L, RE_L, indexing="ij")[1].ravel()), (Ms_u, Re_u)):
        D, E0, Ep_, Em_ = sealed(f, Ms_t, Re_t)
        for th, Eref in zip(TH[f], (E0, Ep_, Em_)):
            Es, sls = p2_standalone(f, th, Ms_t, Re_t); k3 += [float(np.max(np.abs(Es - Eref))), float(np.max(np.abs(sls / D["sl"] - 1)))]
KOK.append(check("K3 this lane's standalone P2 solver == CFG928's code path (grid and all universe galaxies; theta, theta+-)", max(k3) <= 1e-9,
                 f"max |diff| {max(k3):.1e}"))

# ---- K5: per-galaxy identity sealed E_obs == ln10 x L23-form offset (campaign footings, M* = L x M/L)
k5 = []
ic = [i for i, u in enumerate(UNIV) if u["pop"] == "Coma"]
for f in FOOTS:
    D, *_ = sealed(f, Ms_u[ic], Re_u[ic]); Eo = 2 * np.log(np.array([UNIV[i]["sig"] for i in ic]) / D["sl"])
    k5.append(float(np.max(np.abs(Eo - LN10 * l23_offsets(A0[f])[0]))))
KOK.append(check("K5 per galaxy, the sealed-path E_obs == ln10 x the L23-form isolated offset (11 Coma UDGs, campaign footings)", max(k5) <= 1e-12,
                 f"max |diff| {max(k5):.1e}"))
K_ALL = all(KOK); RES["K_all"] = K_ALL
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
if not K_ALL:
    P("  A K-test failed: per criteria section 8 the lane stops; no class is reported."); RES["class"] = None; finish(2)
if MODE == "K":
    P("  CFG933_MODE=K: K-stage only."); finish(0)

# =====================================================================================================================  membership
P("\n=== sample (rules S1-S5 applied mechanically; membership fixed at the primary for every variant)")
for u in UNIV:
    P(f"  {u['name']:22s} {u['pop']:8s} M* {u['Ms']:8.2e}  R_e {u['Re']:4.2f}  sigma {u['sig']:5.1f} +{u['ep']:.1f}/-{u['em']:.1f}  "
      + ("ADMITTED" if u["admit"] else "out: " + ", ".join(u["why_out"])))
RES["membership"] = [dict(name=u["name"], pop=u["pop"], Ms=u["Ms"], Re=u["Re"], sig=u["sig"], ep=u["ep"], em=u["em"], label=u["label"],
                          label_src=u["label_src"], gas_src=u["gas_src"], S1=u["S1"], S2=u["S2"], S3=u["S3"], S4=u["S4"], S5=u["S5"],
                          admitted=u["admit"], why_out=u["why_out"]) for u in UNIV]

# =====================================================================================================================  engine
def evaluate(f, mods=None):
    """per-universe-galaxy arrays under the sealed estimator; mods: mfac, dfac(u), afac, ms_of(u), sig_of(u)"""
    mods = mods or {}
    Ms = np.array([mods["ms_of"](u) if "ms_of" in mods else u["Ms"] for u in UNIV], float); Re = Re_u.copy()
    sig = np.array([u["sig"] for u in UNIV], float); ep = np.array([u["ep"] for u in UNIV], float); em = np.array([u["em"] for u in UNIV], float)
    if "sig_of" in mods:
        for i, u in enumerate(UNIV):
            if mods["sig_of"](u) is not None: sig[i], ep[i], em[i] = mods["sig_of"](u)
    if "mfac" in mods: Ms = Ms * mods["mfac"]
    if "dfac" in mods:
        fD = np.array([mods["dfac"](u) for u in UNIV]); Ms = Ms * fD ** 2; Re = Re * fD
    if "afac" in mods: sig, ep, em = sig * mods["afac"], ep * mods["afac"], em * mods["afac"]
    D, Ep, Epp, Epm = sealed(f, Ms, Re)
    sl = D["sl"]; spred = sl * np.exp(Ep / 2); Eo = 2 * np.log(sig / sl)
    e = np.where(sig > spred, em, ep); sE = 2 * e / sig
    return dict(Ms=Ms, Re=Re, sig=sig, ep=ep, em=em, gb=D["gb"], sl=sl, spred=spred, Eo=Eo, Ep=Ep, Epp=Epp, Epm=Epm, sE=sE,
                sp_i=np.abs(Epp - Epm) / 2)

def summ(G, idx, f):
    idx = list(idx); n = len(idx)
    if n == 0: return dict(N=0)
    Eo, Ep, Epp, Epm, sE = (G[k][idx] for k in ("Eo", "Ep", "Epp", "Epm", "sE"))
    t_sd = float(np.std(Eo, ddof=1) / math.sqrt(n)) if n > 1 else float("nan")
    t_me = float(math.sqrt(np.sum(sE ** 2)) / n)
    se_obs = max(t_me, t_sd) if n > 1 else t_me
    sp = float(abs(np.mean(Epp) - np.mean(Epm)) / 2); sec = math.hypot(se_obs, sp)
    mo, mp = float(np.mean(Eo)), float(np.mean(Ep)); D_ = mo - mp; z = D_ / sec
    r = Eo - Ep; se_r = max(t_me, float(np.std(r, ddof=1) / math.sqrt(n))) if n > 1 else t_me
    # R1: L23-style inverse-variance weighting with the per-galaxy sE
    w = 1 / sE ** 2; mw_o, mw_p = float(np.sum(w * Eo) / np.sum(w)), float(np.sum(w * Ep) / np.sum(w))
    spw = float(abs(np.sum(w * Epp) - np.sum(w * Epm)) / np.sum(w) / 2); sew = math.hypot(float(1 / math.sqrt(np.sum(w))), spw)
    return dict(N=n, mean_Eobs=mo, mean_Eobs_dex=mo / LN10, mean_Epred=mp, mean_Epred_dex=mp / LN10, se_term_scatter=t_sd, se_term_meas=t_me,
                se_obs=se_obs, sigma_pred=sp, se_c=sec, Delta=D_, z=z, kill=bool(n >= 5 and abs(D_) >= 3 * sec), kill_threshold=3 * sec,
                power_target=abs(F0[f] - mp), power_ok=bool(3 * sec < abs(F0[f] - mp)), mean_resid=float(np.mean(r)), se_resid=se_r,
                R1_weighted=dict(mean_Eobs=mw_o, mean_Epred=mw_p, se_c=sew, Delta=mw_o - mw_p, z=(mw_o - mw_p) / sew))

ZM = 3.205
def classify(G, f, adm=None, pools=("pool", "coma", "group")):
    adm = ADM if adm is None else adm
    idx = {"pool": np.where(adm)[0], "coma": np.where(adm & (POP == "Coma"))[0], "group": np.where(adm & (POP == "NGC1052"))[0]}
    S = {k: summ(G, idx[k], f) for k in pools}
    graded = [k for k in ("pool", "coma") if k in S and S[k]["N"] >= 5]
    met = [k for k in graded if S[k]["kill"]]
    H = None
    if "group" in S and S["coma"]["N"] >= 2 and S["group"]["N"] >= 2:
        dd = S["coma"]["mean_resid"] - S["group"]["mean_resid"]; sd = math.hypot(S["coma"]["se_resid"], S["group"]["se_resid"])
        H = dict(diff=dd, se=sd, z=dd / sd, fires=bool(abs(dd) >= 3 * sd))
    quals, reasons = [], []
    if met:
        cls = "P2 EXCLUDED"
        if all(abs(S[k]["z"]) < ZM for k in met): quals.append("MARGINAL")
    else:
        if S["pool"]["N"] < 5: reasons.append(f"N(G-pool) = {S['pool']['N']} < 5")
        for k in graded:
            if not S[k]["power_ok"]: reasons.append(f"power fails on G-{k} (3 se_c {S[k]['kill_threshold']:.3f} >= |F0 - <E_pred>| {S[k]['power_target']:.3f})")
        if H and H["fires"]: reasons.append(f"heterogeneity H fires (Coma - group residuals {H['diff']:+.3f} +- {H['se']:.3f}, z {H['z']:+.2f})")
        if reasons: cls = "NOT DIAGNOSTIC"
        else:
            cls = "P2 CONSISTENT"
            if max(abs(S[k]["z"]) for k in graded) >= 2: quals.append("2-3 sigma tension")
    group_z = [dict(name=NAMES[i], E_obs=float(G["Eo"][i]), E_pred=float(G["Ep"][i]), sE=float(G["sE"][i]),
                    z=float((G["Eo"][i] - G["Ep"][i]) / math.hypot(G["sE"][i], G["sp_i"][i]))) for i in idx.get("group", [])]
    return dict(cls=cls, qualifiers=quals, reasons=reasons, met=met, graded=graded, samples=S, H=H, group_per_galaxy=group_z)

def plant(G, kind):
    G = dict(G)
    G["Eo"] = np.zeros_like(G["Eo"]) if kind == "onlaw" else np.full_like(G["Eo"], 0.4 * LN10)
    return G

def line(tag, C):
    s = C["samples"]; parts = []
    for k in ("pool", "coma"):
        if k in s and s[k]["N"]:
            x = s[k]; parts.append(f"G-{k} N {x['N']}: <E_obs> {x['mean_Eobs']:+.3f} vs <E_pred> {x['mean_Epred']:+.3f}, se_c {x['se_c']:.3f}, z {x['z']:+.2f}"
                                   + (" KILL" if x["kill"] else "") + ("" if x["power_ok"] else " (no power)"))
    return f"  {tag:28s} {C['cls']}" + (f" [{', '.join(C['qualifiers'])}]" if C["qualifiers"] else "") + "  |  " + "; ".join(parts)

# =====================================================================================================================  MUTATE
if MODE in ("onlaw", "plus04"):
    want = "P2 CONSISTENT" if MODE == "onlaw" else "P2 EXCLUDED"
    P(f"\n=== MUTATE {MODE}: sigma_obs := sigma_law" + (" (E_obs = 0)" if MODE == "onlaw" else " x 10^0.2 (E_obs = +0.4 dex = +0.921 ln)")
      + f" on the primary membership, real fractional errors; required: {want} on both footings")
    RES["MUTATE"] = {}; ok = True
    for f in FOOTS:
        C = classify(plant(evaluate(f), MODE), f); RES["MUTATE"][f] = C; ok &= C["cls"] == want
        P(line(f"[{f}]", C))
        for r in C["reasons"]: P(f"      reason: {r}")
    RES["MUTATE_ok"] = bool(ok); RES["MUTATE_required"] = want
    P(f"  MUTATE {MODE}: {'BEHAVES (required class on both footings)' if ok else 'FAILS (required class not reached)'}")
    finish(0 if ok else 1)

# =====================================================================================================================  main
MUTR = {}
for m in ("onlaw", "plus04"):
    pth = os.path.join(HERE, f"cfg933_results_MUTATE_{m}.json")
    MUTR[m] = json.load(_REAL_OPEN(pth)).get("MUTATE_ok") if os.path.exists(pth) else None
RES["MUTATE_status"] = MUTR
COMA_IDX = [i for i, u in enumerate(UNIV) if u["pop"] == "Coma"]
SVAR = {"S-M+": dict(mfac=10 ** 0.2), "S-M-": dict(mfac=10 ** -0.2),
        "S-D-": dict(dfac=lambda u: 0.95 if u["pop"] == "Coma" else ((17.6 / 20.0) if u.get("key") == "DF2" else 0.95)),
        "S-D+": dict(dfac=lambda u: 1.05 if u["pop"] == "Coma" else ((21.7 / 20.0) if u.get("key") == "DF2" else 1.05)),
        "S-A-": dict(afac=1 / 1.15), "S-A+": dict(afac=1.15)}
RES["byfoot"] = {}
for f in FOOTS:
    P(f"\n=== [{f}] a0 = {A0[f]:.4e}; v_2 = {TH[f][0]:.4f} km/s (theta+ {TH[f][1]:.4f}, theta- {TH[f][2]:.4f}); F0 (LVD dwarf class mean) {F0[f]:+.4f}")
    G = evaluate(f); C = classify(G, f)
    P(f"  {'galaxy':22s} {'pop':7s} {'M*':>8s} {'R_e':>4s} {'lg gbar':>7s} {'s_law':>6s} {'s_pred':>6s} {'s_obs':>5s} {'E_obs':>7s} {'sE':>5s} {'E_pred':>7s} {'+-':>6s}")
    for i in np.where(ADM)[0]:
        P(f"  {NAMES[i]:22s} {POP[i]:7s} {G['Ms'][i]:8.2e} {G['Re'][i]:4.1f} {math.log10(G['gb'][i]):7.3f} {G['sl'][i]:6.2f} {G['spred'][i]:6.2f} "
          f"{G['sig'][i]:5.1f} {G['Eo'][i]:+7.3f} {G['sE'][i]:5.3f} {G['Ep'][i]:+7.4f} {G['sp_i'][i]:6.4f}")
    P(line("PRIMARY", C))
    for r in C["reasons"]: P(f"      reason: {r}")
    if C["H"]: P(f"      heterogeneity H: Coma - group residual means {C['H']['diff']:+.3f} +- {C['H']['se']:.3f} (z {C['H']['z']:+.2f}) -> {'FIRES' if C['H']['fires'] else 'quiet'}")
    for g in C["group_per_galaxy"]: P(f"      G-group {g['name']}: E_obs {g['E_obs']:+.3f} +- {g['sE']:.3f} vs E_pred {g['E_pred']:+.4f}: z {g['z']:+.2f}")
    for k in ("pool", "coma"):
        x = C["samples"][k]
        P(f"      G-{k}: se_obs {x['se_obs']:.3f} (scatter {x['se_term_scatter']:.3f}, measurement {x['se_term_meas']:.3f}), sigma_pred {x['sigma_pred']:.4f}; "
          f"kill threshold |Delta| >= {x['kill_threshold']:.3f}; power target |F0 - <E_pred>| {x['power_target']:.3f}; "
          f"<E_obs> {x['mean_Eobs_dex']:+.3f} dex; R1 (sE-weighted) <E_obs> {x['R1_weighted']['mean_Eobs']:+.3f}, z {x['R1_weighted']['z']:+.2f}")
    # S-set
    SV = {}
    for k, m in SVAR.items():
        SV[k] = classify(evaluate(f, m), f); P(line(k, SV[k]))
    base = C["cls"]; fragile = [k for k in SV if SV[k]["cls"] != base]
    # R2 sample variants
    lab = np.array([u["label"] for u in UNIV]); s2 = np.array([u["S2"] and u["S3"] and u["S5"] for u in UNIV])
    s1 = np.array([u["S1"] for u in UNIV]); s4 = np.array([u["S4"] for u in UNIV])
    R2 = {"R2a source label only (no S1)": classify(G, f, adm=lab & s2 & s4), "R2b no M* window (no S4)": classify(G, f, adm=lab & s2 & s1),
          "R2c no S1, no S4": classify(G, f, adm=lab & s2)}
    R2["R2d all 11 Coma alone"] = classify(G, f, adm=(POP == "Coma") & lab & s2, pools=("pool", "coma"))
    for k, v in R2.items(): P(line(k, v))
    # R3 Upsilon = 2 on band luminosity (Coma)
    R3 = classify(evaluate(f, dict(ms_of=lambda u: 2.0 * u["L"] if u["pop"] == "Coma" else u["Ms"])), f); P(line("R3 Ups=2 on band L (Coma)", R3))
    # R4 DF2/DF4 secondary dispersions
    SEC = {"DF2": (10.8, 3.2, 4.0), "DF4": (8.0, 2.3, 1.9)}
    G4 = evaluate(f, dict(sig_of=lambda u: SEC.get(u.get("key"))))
    R4 = [dict(name=NAMES[i], sigma=float(G4["sig"][i]), E_obs=float(G4["Eo"][i]), sE=float(G4["sE"][i]), E_pred=float(G4["Ep"][i]),
               z=float((G4["Eo"][i] - G4["Ep"][i]) / math.hypot(G4["sE"][i], G4["sp_i"][i]))) for i in range(len(UNIV)) if UNIV[i].get("key") in SEC]
    for r in R4: P(f"  R4 {r['name']} secondary sigma {r['sigma']:.1f}: E_obs {r['E_obs']:+.3f} +- {r['sE']:.3f} vs E_pred {r['E_pred']:+.4f}: z {r['z']:+.2f}")
    # R5 the disclosed question: all 11 Coma, unweighted and L23-weighted
    o11, e11 = l23_offsets(A0[f]); E11 = G["Eo"][COMA_IDX]; Ep11 = G["Ep"][COMA_IDX]
    mwL = wmean(E11, LN10 * e11)
    R5 = dict(N=11, unweighted_mean_Eobs=float(np.mean(E11)), unweighted_dex=float(np.mean(E11) / LN10), L23_weighted_mean_Eobs=mwL[0],
              L23_weighted_dex=mwL[0] / LN10, L23_weighted_stat=mwL[1], mean_Epred=float(np.mean(Ep11)), summary=R2["R2d all 11 Coma alone"]["samples"]["pool"])
    P(f"  R5 CFG31's 11 Coma UDGs under the sealed estimator: unweighted <E_obs> {R5['unweighted_mean_Eobs']:+.3f} ({R5['unweighted_dex']:+.3f} dex); "
      f"L23-weighted {R5['L23_weighted_mean_Eobs']:+.3f} ({R5['L23_weighted_dex']:+.3f} dex, = CFG31 R1); <E_pred> {R5['mean_Epred']:+.4f}; "
      f"kill-line z (unweighted, record se) {R5['summary']['z']:+.2f}")
    labels = (["FRAGILE"] if fragile else [])
    final = C["cls"]
    if final == "P2 CONSISTENT" and not (MUTR.get("onlaw") and MUTR.get("plus04")):
        final = "NOT DIAGNOSTIC"; labels.append("CONTROL-LIMITED")
    RES["byfoot"][f] = dict(primary=C, final_class=final, qualifiers=C["qualifiers"], labels=labels, fragile_variants=fragile,
                            S_set={k: dict(cls=v["cls"], qualifiers=v["qualifiers"], reasons=v["reasons"], samples=v["samples"]) for k, v in SV.items()},
                            R2={k: dict(cls=v["cls"], qualifiers=v["qualifiers"], reasons=v["reasons"], samples=v["samples"], H=v["H"]) for k, v in R2.items()},
                            R3=dict(cls=R3["cls"], qualifiers=R3["qualifiers"], reasons=R3["reasons"], samples=R3["samples"]), R4=R4, R5=R5,
                            per_galaxy=[dict(name=NAMES[i], pop=str(POP[i]), Ms=float(G["Ms"][i]), Re=float(G["Re"][i]), log_gbar=float(math.log10(G["gb"][i])),
                                             sigma_law=float(G["sl"][i]), sigma_pred=float(G["spred"][i]), sigma_obs=float(G["sig"][i]), E_obs=float(G["Eo"][i]),
                                             sE=float(G["sE"][i]), E_pred=float(G["Ep"][i]), E_pred_plus=float(G["Epp"][i]), E_pred_minus=float(G["Epm"][i]))
                                        for i in np.where(ADM)[0]])
    P(f"  CLASS [{f}]: {final}" + (f" [{', '.join(C['qualifiers'])}]" if C["qualifiers"] else "") + (f"  labels {labels}" if labels else "")
      + (f"  (S-variants changing the class: {fragile})" if fragile else "  (no S-variant changes the class)"))

RES["class"] = {f: RES["byfoot"][f]["final_class"] for f in FOOTS}
P(f"\n  CLASSES: canonical {RES['class']['canonical']}; alt {RES['class']['alt']}  (MUTATE onlaw {MUTR.get('onlaw')}, plus04 {MUTR.get('plus04')})")
P(f"  runtime {time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB")
finish(0)
