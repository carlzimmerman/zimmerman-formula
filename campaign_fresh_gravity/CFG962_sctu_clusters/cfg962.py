#!/usr/bin/env python3
"""CFG962 (criteria FROZEN_CRITERIA.md, 0e2421c72): SCT-U clusters.

SCT-U = CFG953 SCT-M (R0-R9) + U1 partial conversion (a domain converts only (1 - u) of its dust, u = f_P = 3 s^2/(v^2 + 3 s^2), CFG959's
derivation; the unconverted u stays real native dust, CFG930 R930 NFW) + U2 partial stripping (a member body's mass beyond its King r_J at
pericentre reverts to unlabelled dust by the D-REV event: same mass distribution, centroid and velocity; the part inside r_J persists).
Clusters: u = 1 (no ordered rotation) -> the host converts nothing and is CFG949's B0; members (red sequence) u = 0.80.

Stages (one process at a time, from this directory, OMP_NUM_THREADS=1 nice -n 10):
  CFG962_STAGE=COMPUTE python3 cfg962.py  -> cfg962_arrays.npz, cfg962_compute_diag.json, cfg962_COMPUTE.out
  CFG962_STAGE=K       python3 cfg962.py  -> cfg962_K.out, cfg962_results_K.json
  CFG962_MUTATE=1      python3 cfg962.py  -> cfg962_MUTATE.out, cfg962_results_MUTATE.json
                       python3 cfg962.py  -> cfg962.out, cfg962_results.json
Smoke (outside the repository only): CFG962_NMAX=n CFG962_SMOKE_DIR=<dir outside the repo> CFG962_STAGE=COMPUTE python3 cfg962.py
Read-only reuse: CFG954's script slice (harness, runner, scorers, toy, UDG and Bullet code) and CFG949's / CFG959's / CFG953's slices,
exec'd with every write outside this lane's directory refused; their committed JSON; CFG954's stored work arrays (../_external_data/
cfg954_work, read only); CFG687 per-cluster npz; CFG686 / ACCEPT inputs; the Coma UDG table. Nothing downloaded. CFG960 is not touched.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, time, resource, contextlib, builtins, warnings, subprocess
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad, cumulative_trapezoid

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
W726 = os.path.join(EXT, "cfg726_work"); W951 = os.path.join(EXT, "cfg951_work"); W954 = os.path.join(EXT, "cfg954_work")
STAGE = "MUTATE" if os.environ.get("CFG962_MUTATE", "") == "1" else os.environ.get("CFG962_STAGE", "MAIN").upper()
assert STAGE in ("COMPUTE", "K", "MUTATE", "MAIN")
NMAX = int(os.environ.get("CFG962_NMAX", "0")); SMOKE = NMAX > 0
if SMOKE:
    _sd = os.path.abspath(os.environ.get("CFG962_SMOKE_DIR", ""))
    assert STAGE == "COMPUTE" and os.environ.get("CFG962_SMOKE_DIR") and not _sd.startswith(REPO + os.sep), "smoke runs write outside the repo only"
    OUTDIR = _sd
else:
    OUTDIR = HERE
TAG = {"COMPUTE": "_COMPUTE", "K": "_K", "MUTATE": "_MUTATE", "MAIN": ""}[STAGE] + ("_SMOKE" if SMOKE else "")
CRIT = "0e2421c72"
RSS_LIMIT_GB = 0.95
try:
    os.nice(10)
except OSError:
    pass

# ------------------------------------------------------------------------------------------------ write guard (whole run)
_REAL_OPEN = builtins.open


def _guarded_open(file, mode="r", *a, **k):
    if isinstance(file, (str, bytes, os.PathLike)) and any(c in mode for c in "wax+"):
        p = os.path.abspath(os.fsdecode(file))
        if not (p.startswith(OUTDIR + os.sep) or p == os.devnull):
            raise PermissionError(f"CFG962 refuses to write {p!r}")
    return _REAL_OPEN(file, mode, *a, **k)


builtins.open = _guarded_open; io.open = _guarded_open
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def Pq(*a):                                                           # quiet logger handed to exec'd slices
    pass


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r * 1024 / 1e9


def avail_gb():
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        pg = 16384
        for l in out.splitlines():
            if "page size of" in l:
                pg = int(l.split("page size of")[1].split()[0])
        val = {l.split(":")[0].strip(): int(l.split(":")[1].strip().rstrip(".")) for l in out.splitlines()[1:] if ":" in l}
        return (val.get("Pages free", 0) + val.get("Pages inactive", 0) + val.get("Pages speculative", 0)) * pg / 1e9
    except Exception:
        return None


def finish_log():
    with _REAL_OPEN(os.path.join(OUTDIR, f"cfg962{TAG}.out"), "w") as fh_:
        fh_.write("\n".join(LOG) + "\n")


def guard(where=""):
    g = rss_gb()
    if g > RSS_LIMIT_GB:
        P(f"RSS GUARD: {g:.3f} GB > {RSS_LIMIT_GB} GB at '{where}' -> abort (exit 3)"); finish_log(); sys.exit(3)
    av = avail_gb(); waited = 0
    while av is not None and av < 3.0:
        if waited >= 1800:
            P(f"MEMORY GUARD: available {av:.1f} GB < 3 GB for 30 min at '{where}' -> exit 75 (rerun later)"); finish_log(); sys.exit(75)
        if waited == 0:
            P(f"  memory guard: available {av:.1f} GB < 3 GB at '{where}': pausing")
        time.sleep(60); waited += 60; av = avail_gb()
    return g


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, (np.floating, float)):
        x = float(o)
        return x if math.isfinite(x) else (None if math.isnan(x) else ("inf" if x > 0 else "-inf"))
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def J(*p):
    with _REAL_OPEN(os.path.join(LANES, *p)) as fh_:
        return json.load(fh_)


_a0 = avail_gb()
P(f"CFG962 [{STAGE}{' SMOKE N=' + str(NMAX) if SMOKE else ''}]  SCT-U clusters; criteria {CRIT}; available memory at start "
  f"{_a0 if _a0 is None else round(_a0, 1)} GB")
P("  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; raw data, framework-native inputs; not theory closed")
if _a0 is not None and _a0 < 8.0:
    P("start guard: available < 8 GB -> exit 75"); finish_log(); sys.exit(75)

FEET = ("canonical", "alt"); FL = {"canonical": "can", "alt": "alt"}


def lane_slice(path, start_key, end_key):
    with _REAL_OPEN(path) as fh_:
        txt = fh_.read()
    i = txt.index(start_key); i = txt.rfind("\n", 0, i) + 1
    j = txt.index(end_key, i); j = txt.rfind("\n", 0, j) + 1
    return txt[i:j]


# ================================================================================================ CFG954 slice (harness, runner, scorers, toy)
for _d in ("CFG637_derived_reservoir", "CFG652_hot_group_discriminator", "CFG599_merger_stopwatch_v2", "CFG540_vizier2026_bfjr_mhongoose"):
    sys.path.insert(0, os.path.join(LANES, _d))
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import cfg637_lib as L                                            # noqa: E402  (read-only)
    import CFG4_common as C4                                          # noqa: E402
    import cfg652_model as M652                                       # noqa: E402
    import cfg599_lib as P599                                         # noqa: E402
assert abs(C4.A0["canonical"] - 9.3603e-11) < 1e-15 and abs(C4.A0["alt"] - 1.1312e-10) < 1e-15
SRC954 = os.path.join(LANES, "CFG954_sct_clusters_mergers", "cfg954.py")
SL954 = lane_slice(SRC954, "CFG726 / CFG951 harness (copied)", "COMPUTE stage")
NS954 = dict(os=os, sys=sys, io=io, json=json, math=math, time=time, contextlib=contextlib, resource=resource, subprocess=subprocess,
             np=np, brentq=brentq, cumulative_trapezoid=cumulative_trapezoid, warnings=warnings, L=L, C4=C4, M652=M652, P599=P599,
             HERE=os.path.dirname(SRC954), LANES=LANES, REPO=REPO, EXT=EXT, W726=W726, W951=W951, WORK=W954, STAGE="MAIN", NMAX=0,
             SMOKE=False, TAG="", WTAG="", T0=T0, LOG=[], RSS_LIMIT=0.9e9, CRIT="68a43b4ff", P=Pq, rss=lambda: rss_gb() * 1e9,
             vm_free_gb=avail_gb, guard=lambda where="": rss_gb(), jclean=jclean, rd=lambda rel: J(rel), FEET=FEET, FL=FL,
             __file__=SRC954, __name__="cfg954_ro")
exec(compile(SL954, SRC954, "exec"), NS954)
for _k in ("nu_s", "A0K", "A0SI", "RE_GAL", "SUP_PER_COND", "A_HERN", "rta_of", "prog_halo", "shell_frac", "convolve_members", "R_OBS",
           "G_SI", "MSUN", "MPC", "RGRID", "RK_GRID", "DK", "DM_", "SM_", "dsig_from_M", "law_M", "erass_gas", "host_table", "rJ_at",
           "NODE_W", "pericentres", "conv_fast", "wmedian", "cluster_ctx", "run_sct", "fh", "cum_placed", "T_law", "PC7", "NE_ALL",
           "score_TR", "accept_inputs", "score_TA", "bullet_sct", "jwin", "toy_sct", "RAP", "RAP2", "KPC_SI", "g_host_coma",
           "rho_host_coma", "nu_e", "plummer_M", "udg_rows", "udg_sct", "RCB"):
    globals()[_k] = NS954[_k]
guard("cfg954 slice")


# ================================================================================================ CFG949 / CFG959 slices (B0 and the galaxy items)
def load_949():
    SRC949 = os.path.join(LANES, "CFG949_clusters_untethered", "cfg949.py")
    sl = lane_slice(SRC949, "CFG686 / CFG687 / CFG922 machinery (exec, read-only)", "======== K stage")
    ns = dict(os=os, sys=sys, io=io, json=json, math=math, time=time, contextlib=contextlib, resource=resource, np=np, brentq=brentq,
              quad=quad, cumulative_trapezoid=cumulative_trapezoid, HERE=os.path.dirname(SRC949), LANES=LANES, MODE="MAIN", T0=T0,
              RSS_LIMIT_GB=RSS_LIMIT_GB, CHECKS=[], __file__=SRC949, __name__="cfg949_ro", P=Pq, guard=lambda label: rss_gb(),
              check=lambda name, ok, detail: bool(ok))
    exec(compile(sl, SRC949, "exec"), ns)
    return ns


def load_959():
    SRC959 = os.path.join(LANES, "CFG959_excess_unrelaxed_native", "cfg959.py")
    sl = lane_slice(SRC959, 'FOOTS = ("canonical", "alt"); LN10 = math.log(10.0)', "======== K stage")
    ns = dict(os=os, sys=sys, io=io, json=json, math=math, time=time, resource=resource, contextlib=contextlib, builtins=builtins,
              warnings=warnings, np=np, brentq=brentq, quad=quad, cumulative_trapezoid=cumulative_trapezoid, T0=T0,
              HERE=os.path.dirname(SRC959), LANES=LANES, REPO=REPO, MODE="MAIN", TAG="", RSS_LIMIT_GB=RSS_LIMIT_GB,
              _REAL_OPEN=_REAL_OPEN, P=Pq, rss_gb=rss_gb, jdef=lambda o: jclean(o), RES={}, guard=lambda label: guard(label),
              check=lambda name, ok, measured: bool(ok), J=J, __file__=SRC959, __name__="cfg959_ro")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        exec(compile(sl, SRC959, "exec"), ns)
    return ns


def load_953():
    """CFG953's constants/census/domain block and its sat_c (exec'd read-only)."""
    SRC953 = os.path.join(LANES, "CFG953_source_changing_theory", "cfg953.py")
    s1 = lane_slice(SRC953, "constants (read-only inputs)", "shared sympy (CFG947 / CFG941)")
    s2 = lane_slice(SRC953, "def sat_c(Mb_sun, a_pc, rkpc, a0):", "\nCc = {}")
    ns = dict(os=os, sys=sys, io=io, json=json, math=math, contextlib=contextlib, np=np, brentq=brentq, LANES=LANES, REPO=REPO,
              P=Pq, RES={}, MUT=False, STAGE="MAIN", CRIT="049a0f867", __file__=SRC953, __name__="cfg953_ro")
    exec(compile(s1, SRC953, "exec"), ns)
    ns["GL_X"], ns["GL_W"] = np.polynomial.legendre.leggauss(64)
    exec(compile(s2, SRC953, "exec"), ns)
    return ns


# ================================================================================================ SCT-U members and runner (this lane)
U_MEM, U_MEM_B3 = 0.80, 0.20                                          # criteria section 2
NFW_C, NFW_BND = 3000.0, "rta"


def member_cold(rg, shape, m, z, foot, um, R930):
    """SCT-U member cold (Msun, cumulative on rg): body = phantom_trunc with supply (1 - u) S (u = 0: CFG954's prog_halo h exactly);
    debris = u S x NFW shape of prof930(M_ta = S / (1 - f_b,N), z, C 3000, r_ta).  S = 53.64 m (harness condensed-floor supply)."""
    S = SUP_PER_COND * m
    rta = rta_of(m / M652.F_COND_FLOOR / L.FB, z)
    if um >= 1.0:
        body = np.zeros_like(rg); xe = None
    else:
        body, xe = L.phantom_trunc(rg / rta, m * shape, rta, A0K[foot], nu_s, (1.0 - um) * S)
    if um > 0.0:
        c, rs, rb, zc = R930["prof930"](S / (1.0 - R930["FBN"]), z, NFW_C, NFW_BND)
        deb = um * S * np.asarray(R930["m_"](np.minimum(rg, rb) / rs), float) / float(R930["m_"](c))
        nfw = dict(c=c, rs=rs, rb=rb, zc=zc)
    else:
        deb = np.zeros_like(rg); nfw = None
    return body, deb, dict(S=S, rta=rta, edge=(None if xe is None else xe * rta), nfw=nfw)


def run_u(ctx, body, deb, Mb_host, src_gas, Mc_shape, S_total, u_cl, foot, epoch="peri", r7=True, place="NFW", strip=True,
          deb_bound=True, Mtot0=None, members=True, maxit=8, tol=1e-4):
    """iterate one SCT-U cluster profile (criteria section 3), Msun on RK_GRID.
    cold = C_J (kept members' body [+ debris] inside r_J) + min(T_law(src), (1 - u_cl) S_unl + M_rem) + u_cl S_unl / S_shape x Mc_shape
           [+ stripped cold placed on the members' orbits (P-ORB)];  S_unl = S_total - C_J,tot - M_rem [- ORB_tot]."""
    nmem, dN, fs = ctx["nmem"], ctx["dN"], ctx["fs"]
    Mg_tr = ctx["Mg"]; dMg = np.diff(np.r_[0.0, Mg_tr])
    mown = (body + deb) if deb_bound else body.copy()
    mcum = ctx["mi"] * ctx["shape"] + mown
    dTk = np.r_[mown[0], np.diff(mown)]
    m_tot = float(mown[-1])
    S_shape = float(Mc_shape[-1]) if Mc_shape is not None else 1.0
    Mtot = (Mb_host + Mc_shape) if Mtot0 is None else Mtot0.copy()
    cold = None; cold_prev = None; hist = []; conv = np.inf; it = 0; Mprev = Mtot
    for it in range(1, maxit + 1):
        if members and strip:
            tab = host_table(RK_GRID, Mtot, Mg_tr)
            if epoch == "peri":
                rp = pericentres(tab, DM_)[0]; wn = NODE_W
            else:
                rp = DM_[:, None].copy(); wn = np.ones(1)
            rJ = rJ_at(tab, rp, R_OBS, mcum)
        else:
            wn = np.ones(1); rJ = np.full((len(DM_), 1), np.inf)
        if members:
            merged = (fh(rJ) < 0.5) if r7 else np.zeros(rJ.shape, bool)
            keep = (SM_[None, None, :] < rJ[:, :, None]) & (~merged)[:, :, None]
            WJ = np.einsum("w,dws->ds", wn, keep.astype(float))
            C = nmem * conv_fast(dN[:, None] * dTk[None, :] * WJ)
            rJc = np.minimum(rJ, R_OBS[-1])
            bJ = np.interp(rJc, R_OBS, body, left=0.0); mJ = np.interp(rJc, R_OBS, mown, left=0.0)
            M_rem = nmem * float(np.sum(dN * ((merged * bJ) @ wn)))
            fhJ = fh(rJ)
            p_host = (1.0 - (fhJ @ wn)) if not r7 else ((1.0 - (~merged) * fhJ) @ wn)
            src = src_gas + fs * cum_placed(dMg, p_host)
            if place == "ORB":
                orb_d = np.where(merged, m_tot - bJ, m_tot - mJ) @ wn
                ORB_tot = nmem * float(np.sum(dN * orb_d))
                orb = cum_placed(dMg, orb_d)
                orb = orb * (ORB_tot / orb[-1]) if orb[-1] > 0 else 0.0 * orb
            else:
                orb = 0.0; ORB_tot = 0.0
            mfrac = float(np.sum(dN * (merged.astype(float) @ wn)))
            rJm = wmedian(np.minimum(rJ, 1e9), dN[:, None] * wn[None, :])
        else:
            C = np.zeros_like(RK_GRID); M_rem = 0.0; src = src_gas.copy(); orb = 0.0; ORB_tot = 0.0; mfrac = 0.0; rJm = np.inf
        C_tot = float(C[-1])
        S_unl = S_total - C_tot - M_rem - ORB_tot
        floor = bool(S_unl < 0.0); S_unl_f = max(S_unl, 0.0)
        Tsrc = T_law(src, foot)
        body_host = np.minimum(Tsrc, (1.0 - u_cl) * S_unl_f + M_rem)
        dust_host = (u_cl * S_unl_f / S_shape) * Mc_shape if u_cl > 0 else 0.0
        cold_prev = cold
        cold = C + body_host + dust_host + orb
        Mn = Mb_host + cold
        ok = Mtot > 0
        conv = float(np.max(np.abs(Mn[ok] / Mtot[ok] - 1)))
        hist.append(conv)
        Mprev = Mtot; Mtot = Mn
        if conv <= tol and it >= 2:
            break
    if cold_prev is None:
        cold_prev = Mprev - Mb_host
    cold_out = float(cold[-1])
    return dict(Mtot=Mtot, Mprev=Mprev, cold=cold, cold_prev=cold_prev, iters=it, conv=conv,
                diag=dict(iters=it, conv=conv, f_U=(u_cl * S_unl_f / S_shape if u_cl > 0 else 0.0), C_over_Mstar=C_tot / ctx["Mstar"],
                          C_over_S=C_tot / S_total, rJ_med=rJm, merged_frac=mfrac, Mrem_over_S=M_rem / S_total, floor=floor,
                          ORB_over_S=ORB_tot / S_total, hostbody_over_S=float(body_host[-1]) / S_total,
                          book_resid=(cold_out - S_total) / S_total))


# ================================================================================================ COMPUTE stage
UVARS = {   # name: (um, epoch, r7, place, deb_bound)   -- the primary and its declared brackets, plus reported rows
    "U": (U_MEM, "peri", True, "NFW", True),
    "U_present": (U_MEM, "present", True, "NFW", True),          # B1
    "U_orb": (U_MEM, "peri", True, "ORB", True),                 # B2
    "U_um02": (U_MEM_B3, "peri", True, "NFW", True),             # B3
    "U_noR7": (U_MEM, "peri", False, "NFW", True),               # B4
    "U_debhost": (U_MEM, "peri", True, "NFW", False),            # B5
    "U_um0": (0.0, "peri", True, "NFW", True),                   # reported
    "U_um1": (1.0, "peri", True, "NFW", True),                   # reported
}
BRACKETS = ("U_present", "U_orb", "U_um02", "U_noR7", "U_debhost")


def compute_one(ctx, Mb_h, gas_h, Mc_h, Pb, foot, z, dsig_newton, MS9, R930):
    """all variants for one cluster and footing.  Mb_h, gas_h, Mc_h: B0 host baryons, gas and native dust (Msun on RGRID)."""
    arr = {}; dg = {}
    S_B0 = float(Mc_h[-1])
    prof = {}
    for um in sorted(set(v[0] for v in UVARS.values()) | {0.0}):
        prof[um] = member_cold(R_OBS, ctx["shape"], ctx["mi"], z, foot, um, R930)
    dsn = lambda cold: Pb + dsig_newton((cold * MS9)[None, :])[0]
    for nm, (um, ep, r7, place, db) in UVARS.items():
        b, d_, _ = prof[um]
        o = run_u(ctx, b, d_, Mb_h, gas_h, Mc_h, S_B0, 1.0, foot, epoch=ep, r7=r7, place=place, deb_bound=db)
        arr[nm] = dsn(o["cold"]); arr[nm + "_prev"] = dsn(o["cold_prev"]); dg[nm] = o["diag"]
    # MUTATE arms (criteria section 6)
    b0, d0, _ = prof[0.0]
    o = run_u(ctx, b0, d0, ctx["Mb"], ctx["Mg"], None, ctx["S_tot"], 0.0, foot, r7=False, Mtot0=ctx["Mlaw"])       # MU-U0 (i): R3
    arr["MU_U0_R3"] = dsig_from_M(o["Mtot"]); dg["MU_U0_R3"] = o["diag"]
    o = run_u(ctx, b0, d0, Mb_h, gas_h, Mc_h, S_B0, 0.0, foot, r7=True)                                             # MU-U0 (ii)
    arr["MU_U0_B0"] = dsn(o["cold"]); dg["MU_U0_B0"] = o["diag"]
    o = run_u(ctx, b0, d0, ctx["Mb"], ctx["Mg"], None, ctx["S_tot"], 0.0, foot, r7=False, strip=False, Mtot0=ctx["Mlaw"])   # MU-NS (i)
    arr["MU_NS_U0"] = dsig_from_M(o["Mtot"]); dg["MU_NS_U0"] = o["diag"]
    bU, dU, _ = prof[U_MEM]
    o = run_u(ctx, bU, dU, Mb_h, gas_h, Mc_h, ctx["S_tot"], 1.0, foot, r7=True, strip=False)                        # MU-NS (ii)
    arr["MU_NS_U"] = dsn(o["cold"]); dg["MU_NS_U"] = o["diag"]
    o = run_u(ctx, bU, dU, Mb_h, gas_h, Mc_h, S_B0, 1.0, foot, members=False)                                      # MU-0 control
    arr["MU_0"] = dsn(o["cold"])
    arr["B0"] = Pb + dsig_newton((Mc_h * MS9)[None, :])[0]
    # K9 facts: member body at u = 0 == CFG954's h; host baryons B0 vs harness
    dg["K9_body_eq_h"] = bool(np.array_equal(b0, ctx["h"]))
    dg["K9_Mb_maxrel"] = float(np.max(np.abs(Mb_h[1:] / ctx["Mb"][1:] - 1)))
    dg["S_B0"] = S_B0; dg["S_tot"] = ctx["S_tot"]; dg["Mstar"] = ctx["Mstar"]; dg["mi"] = ctx["mi"]; dg["nmem"] = ctx["nmem"]
    dg["members_total_over_SB0"] = ctx["nmem"] * float((prof[U_MEM][0] + prof[U_MEM][1])[-1]) / S_B0
    dg["member_nfw"] = prof[U_MEM][2]["nfw"]; dg["member_edge_u08"] = prof[U_MEM][2]["edge"]; dg["member_edge_u0"] = prof[0.0][2]["edge"]
    return arr, dg


def accept_hosts(N9):
    AC = N9["R6"]["clusters"]; MS9 = N9["MSUN"]
    GA = np.array([N9["gas_accept"](c["key"], c["z"])[0] for c in AC]); MBA = GA * 1.2
    McA = np.empty_like(MBA)
    for i, c in enumerate(AC):
        Mta, f = N9["supply"]("S-cen", GA[i, -1] / MS9, np.nan, 0.20); cc, rs, rb, zc = N9["prof930"](Mta, float(c["z"]), 3000.0, "rta")
        McA[i] = N9["cold_profile"](Mta, cc, rs, rb)
    ACD = np.nan_to_num(np.array([c["dsig"] for c in AC])); ACE = np.array([c["err"] for c in AC], float)
    STA = N9["Stack"](ACD, ACE, np.array([c["ra"] for c in AC]), "boot")
    return dict(AC=AC, GA=GA, MBA=MBA, McA=McA, STA=STA)


def stage_compute():
    N9 = load_949(); guard("cfg949 slice")
    MS9 = N9["MSUN"]; dsn = N9["dsig_newton"]
    MB, GAS, ZC = N9["MB"], N9["GAS"], N9["ZC"]
    Mc_all, meta = N9["build_cold"]("C3000|rta", "S-cen", GAS, 0.20)
    lamj = json.load(_REAL_OPEN(os.path.join(W726, "lambda.json"))); Nm = np.array(lamj["Nmem"])
    AH = accept_hosts(N9); acc, C686 = accept_inputs()
    assert [c["name"] for c in AH["AC"]] == [a_["name"] for a_ in acc]
    idx = np.arange(NE_ALL) if not SMOKE else np.arange(min(NMAX, NE_ALL))
    P(f"  inputs ready ({time.time() - T0:.0f} s; RSS {rss_gb():.2f} GB); eRASS1 {len(idx)}, ACCEPT {len(acc)}")
    OUT = {}; DG = {}
    for foot in FEET:
        res = {}; dgs = []
        for k, i in enumerate(idx):
            ctx = cluster_ctx(erass_gas(int(i), PC7), 0.20, float(PC7["z"][i]), float(Nm[i]), foot)
            Pb = dsn(MB[i:i + 1])[0]
            arr, dg = compute_one(ctx, MB[i] / MS9, GAS[i] / MS9, Mc_all[i] / MS9, Pb, foot, float(ZC[i]), dsn, MS9, N9)
            for v, x in arr.items():
                res.setdefault(v, np.zeros((len(idx), 8)))[k] = x
            dgs.append(dg)
            if (k + 1) % 20 == 0 or k == len(idx) - 1:
                its = max(x["U"]["iters"] for x in dgs)
                P(f"  eRASS1 {foot} {k + 1}/{len(idx)} ({time.time() - T0:.0f} s; RSS {rss_gb():.2f} GB; U iterations max {its})")
                guard(f"eRASS1 {foot} {k + 1}")
        for v, x in res.items():
            OUT[f"{foot}|E|{v}"] = x
        DG[f"{foot}|E"] = dgs
        resA = {}; dgA = []
        for j, a_ in enumerate(acc):
            ctx = cluster_ctx(a_["Mg"], 0.20, a_["z"], a_["Nm"], foot)
            Pb = dsn(AH["MBA"][j:j + 1])[0]
            arr, dg = compute_one(ctx, AH["MBA"][j] / MS9, AH["GA"][j] / MS9, AH["McA"][j] / MS9, Pb, foot, float(a_["z"]), dsn, MS9, N9)
            for v, x in arr.items():
                resA.setdefault(v, np.zeros((len(acc), 8)))[j] = x
            dgA.append(dg)
        for v, x in resA.items():
            OUT[f"{foot}|A|{v}"] = x
        DG[f"{foot}|A"] = dgA
        P(f"  ACCEPT {foot} done ({time.time() - T0:.0f} s; RSS {rss_gb():.2f} GB)")
        guard(f"ACCEPT {foot}")
    np.savez_compressed(os.path.join(OUTDIR, f"cfg962_arrays{'_SMOKE' if SMOKE else ''}.npz"), **OUT)
    DG["meta"] = dict(n_eRASS1=len(idx), n_ACCEPT=len(acc), elapsed_s=time.time() - T0, peak_rss_gb=rss_gb(), criteria=CRIT,
                      B0_meta_median=dict(Mta=float(np.median(meta["Mta"][idx])), fret=float(np.median(meta["fret"][idx])),
                                          c=float(np.median(meta["c"][idx])), rs=float(np.median(meta["rs"][idx]))))
    with open(os.path.join(OUTDIR, f"cfg962_compute_diag{'_SMOKE' if SMOKE else ''}.json"), "w") as fh_:
        json.dump(jclean(DG), fh_)
    if SMOKE:
        for foot in FEET:
            for d in DG[f"{foot}|E"]:
                P(f"  [smoke {foot}] U: f_U {d['U']['f_U']:.3f} C/S_B0 {d['U']['C_over_S']:.3f} r_J {d['U']['rJ_med']:.0f} merged {d['U']['merged_frac']:.3f} "
                  f"it {d['U']['iters']} | K9 body==h {d['K9_body_eq_h']} Mb maxrel {d['K9_Mb_maxrel']:.1e}")
    return None


def load_compute():
    with np.load(os.path.join(HERE, "cfg962_arrays.npz")) as z:
        A = {k: z[k] for k in z.files}
    D = json.load(_REAL_OPEN(os.path.join(HERE, "cfg962_compute_diag.json")))
    return A, D


# ================================================================================================ scoring helpers
S_OBS, S_ERR = 0.896, 0.209                                           # CFG687 T2


def cls2(z_by_foot):
    c = [abs(z_by_foot[f]) < 2 for f in FEET]
    return "CONSISTENT" if all(c) else ("INCONSISTENT" if not any(c) else "CONDITIONAL")


def cls_slope(s_by_foot):
    dz = [abs(s_by_foot[f] - S_OBS) / S_ERR for f in FEET]
    if all(x < 2 for x in dz):
        return "CONSISTENT"
    if all(x >= 3 for x in dz):
        return "INCONSISTENT"
    return "CONDITIONAL"


def bandZ(bd, b):
    return (bd[b][0] - 1.0) / bd[b][1]


CHK = {}


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    return bool(ok)


def W954_arrays():
    W = {}
    for foot in FEET:
        with np.load(os.path.join(W954, f"erass_{foot}.npz")) as z:
            W[("E", foot)] = {k: z[k] for k in z.files}
        with np.load(os.path.join(W954, f"accept_{foot}.npz")) as z:
            W[("A", foot)] = {k: z[k] for k in z.files}
        with np.load(os.path.join(W954, f"N_{foot}.npz")) as z:
            W[("N", foot)] = {k: z[k] for k in z.files}
        W[("Ed", foot)] = json.load(_REAL_OPEN(os.path.join(W954, f"erass_{foot}_diag.json")))
    return W


# ================================================================================================ (b-J) SCT-U merger toy
def toy_sctu(q, foot, u, R930, r7=True, n_d=1521):
    """CFG954 (e) set-up with SCT-U rules (criteria (b-J)).  At u = 0 and r7 = False this is CFG954's R2 row."""
    a0 = A0K[foot]; Gk = L.G
    sk = R_OBS; shape = M652.hern(sk, 1.0, RE_GAL); m1 = 1e11; m2 = q * m1
    b1, d1, _ = member_cold(sk, shape, m1, 0.0, foot, u, R930); b2, d2, _ = member_cold(sk, shape, m2, 0.0, foot, u, R930)
    own1 = b1 + d1; own2 = b2 + d2
    Mb1, Mb2 = m1 * shape, m2 * shape
    S1 = SUP_PER_COND * m1
    dMb2 = np.diff(np.r_[0.0, Mb2])
    tab1 = host_table(sk, Mb1 + own1)
    ds = np.r_[np.exp(np.linspace(math.log(1000.0), math.log(0.5), n_d)), 0.0]
    rj = np.array([float(rJ_at(tab1, np.array([d]), sk, Mb2 + own2)[0]) if d > 0 else 0.0 for d in ds])
    rj = np.minimum(rj, 1e12)
    rjl = np.minimum.accumulate(rj)
    if r7:
        trig = np.where((fh(rjl) < 0.5) | (ds == 0.0))[0]; km = int(trig[0])
    else:
        km = len(ds) + 10
    Mlaw1 = Mb1 + own1; Mlaw2 = Mb2 + own2
    v = np.array([math.sqrt(Gk * (float(np.interp(d, sk, Mlaw1)) + float(np.interp(d, sk, Mlaw2))) / d) if d > 0 else np.nan for d in ds])
    t = np.zeros(len(ds))
    for k in range(1, len(ds)):
        vm = v[k - 1] if not np.isfinite(v[k]) else 0.5 * (v[k - 1] + v[k])
        t[k] = t[k - 1] + (ds[k - 1] - ds[k]) / vm
    Mrem = (Mb1 + Mb2) * nu_s(Gk * (Mb1 + Mb2) / sk ** 2 / a0)
    vrem = lambda R: math.sqrt(Gk * float(np.interp(R, sk, Mrem)) / R)
    v2 = lambda R: math.sqrt(Gk * float(np.interp(R, sk, Mlaw2)) / R)
    td1 = {R: R / vrem(R) for R in RAP}; td2 = {R: R / v2(R) for R in RAP2}

    def encl(dM, d, R):
        return float(np.sum(dM * shell_frac(SM_, d, R)))

    def L1(Senc, R, Sup):
        T = Senc * (float(nu_s(Gk * Senc / R ** 2 / a0)) - 1.0)
        return Senc + min(T, Sup)
    Mb1R = {R: float(np.interp(R, sk, Mb1)) for R in RAP}
    d1R = {R: float(np.interp(R, sk, d1)) for R in RAP}
    E1 = {R: [] for R in RAP}; E2 = {R: [] for R in RAP2}; capmax = 0.0
    latch = None
    for k, d in enumerate(ds):
        rJ = rjl[k]
        kept2 = np.where(sk < rJ, own2, np.interp(rJ, sk, own2, left=0.0))
        keptb2 = np.where(sk < rJ, b2, np.interp(rJ, sk, b2, left=0.0)); keptd2 = kept2 - keptb2
        rev2 = u * (own2 - kept2)
        strip_tot = float(own2[-1] - kept2[-1])
        cap1 = (1.0 - u) * S1 + (1.0 - u) * strip_tot
        merged = k >= km
        if merged and latch is None:
            latch = dict(capm=cap1 + float(keptb2[-1]), dust2=keptd2 + rev2)
        if not merged:
            dcarry = np.diff(np.r_[0.0, kept2 + rev2])
        else:
            dcarry = np.diff(np.r_[0.0, latch["dust2"]])
        for R in RAP:
            eb2 = encl(dMb2, d, R); Sg = Mb1R[R] + eb2
            GP = Sg * float(nu_s(Gk * Sg / R ** 2 / a0))
            if not merged:
                T1 = Mb1R[R] * (float(nu_s(Gk * Mb1R[R] / R ** 2 / a0)) - 1.0); capmax = max(capmax, T1 / cap1)
                Mv = L1(Mb1R[R], R, cap1) + d1R[R] + eb2 + encl(dcarry, d, R)
            else:
                Mv = L1(Mb1R[R] + eb2, R, latch["capm"]) + d1R[R] + encl(dcarry, d, R)
            E1[R].append(Mv / GP - 1.0)
        for R in RAP2:
            mb2R = float(np.interp(R, sk, Mb2))
            ownc = float(np.interp(R, sk, own2)); own = mb2R + ownc
            gravc = float(np.interp(min(R, rJ), sk, own2, left=0.0)); grav = mb2R + gravc
            if not merged:
                vin = grav + u * (ownc - gravc)                     # kept inside r_J + the comoving unconverted stripped dust
            else:
                vin = mb2R + float(np.interp(R, sk, latch["dust2"]))
            E2[R].append((vin - grav) / own)
    J1 = {R: jwin(t, np.array(E1[R]), td1[R]) for R in RAP}
    J2 = {R: jwin(t, np.array(E2[R]), td2[R]) for R in RAP2}
    return dict(J1=J1, J2=J2, J_max=max(max(J1.values()), max(J2.values())), J1_max=max(J1.values()), J2_max=max(J2.values()),
                E1_final={str(R): E1[R][-1] for R in RAP}, k_merge=(int(km) if r7 else None), d_merge=(float(ds[km]) if r7 else None),
                rJ_at_merge=(float(rjl[km]) if r7 else None), T1_over_cap1_max=capmax, t_total_Gyr=float(t[-1]),
                E1_maxabs=max(max(abs(x) for x in E1[R]) for R in RAP))


# ================================================================================================ (f) momentum and mass through stripping
def drev_event_algebra(body, deb, rJ, X=np.array([300.0, 40.0, -20.0]), V=np.array([-150.0, 400.0, 30.0]), npair=16, seed=962):
    """one D-REV event on a discretised member (shells on R_OBS); reverted shells -> antipodal particle pairs at the shell radius."""
    rng = np.random.default_rng(seed)
    mown = body + deb; dm = np.diff(np.r_[0.0, mown]); s = R_OBS
    nvec = rng.normal(size=(npair, 3)); nvec /= np.linalg.norm(nvec, axis=1)[:, None]; nvec = np.vstack([nvec, -nvec])
    out_ = s >= rJ
    M0 = float(dm.sum()); P0 = M0 * V; D0 = M0 * X; L0 = np.cross(X, P0)
    Mb = float(dm[~out_].sum()); xs, ms = [], []
    for k in np.where(out_ & (dm > 0))[0]:
        xs.append(X[None, :] + s[k] * nvec); ms.append(np.full(len(nvec), dm[k] / len(nvec)))
    if xs:
        xs = np.vstack(xs); ms = np.concatenate(ms)
    else:
        xs = np.zeros((0, 3)); ms = np.zeros(0)
    M1 = Mb + float(ms.sum()); P1 = Mb * V + (ms[:, None] * V[None, :]).sum(0); D1 = Mb * X + (ms[:, None] * xs).sum(0)
    L1_ = np.cross(X, Mb * V) + np.cross(xs, ms[:, None] * V[None, :]).sum(0)
    sc = M0 * np.linalg.norm(V)
    return dict(dM_rel=abs(M1 - M0) / M0, dP_rel=float(np.linalg.norm(P1 - P0) / sc), dD_rel=float(np.linalg.norm(D1 - D0) / (M0 * np.linalg.norm(X))),
                dL_rel=float(np.linalg.norm(L1_ - L0) / max(np.linalg.norm(L0), 1e-300)), frac_reverted=float(ms.sum()) / M0, rJ=float(rJ))


def nbody_strip(u, foot, R930, mode="drev", M_H=1e13, eps_H=20.0, m_b=1e10, Re_b=3.0, eps_b=3.0, eps_d=1.0, d0=300.0, vfac=0.5,
                t_end=10.0, dt=2e-3, K=48, npair=16, seed=962):
    """(f2): host point + satellite (baryon particle + rigid shells of body and bound debris); D-REV at every pericentre."""
    Gk = L.G; rng = np.random.default_rng(seed)
    sk = R_OBS; shape = M652.hern(sk, 1.0, Re_b)
    body, deb, info = member_cold(sk, shape, m_b, 0.0, foot, u, R930)
    mown = body + deb; tot = float(mown[-1])
    r_out = float(sk[np.searchsorted(mown, tot * (1 - 1e-9))]) if np.any(mown >= tot * (1 - 1e-9)) else float(sk[-1])
    edges = np.r_[0.0, np.geomspace(0.5, r_out, K)]
    cum = np.interp(edges, sk, mown, left=0.0); wk = np.diff(cum); sh = np.sqrt(np.maximum(edges[1:] * np.maximum(edges[:-1], 0.25), 1e-6))
    alive = wk > 0
    nvec = rng.normal(size=(npair, 3)); nvec /= np.linalg.norm(nvec, axis=1)[:, None]; nvec = np.vstack([nvec, -nvec])
    M_S = m_b + float(wk.sum())
    vt = vfac * math.sqrt(Gk * M_H / d0)
    xH = np.zeros(3); xB = np.array([d0, 0.0, 0.0]); XS = xB.copy()
    vS = np.array([0.0, vt, 0.0]); vH = np.zeros(3)
    Mt = M_H + M_S; vcm = (M_S * vS) / Mt; vS = vS - vcm; vH = vH - vcm; vB = vS.copy()
    xcm = (M_S * XS) / Mt; xH -= xcm; xB -= xcm; XS -= xcm
    xd = np.zeros((0, 3)); vd = np.zeros((0, 3)); md = np.zeros(0)
    mH = M_H

    def soft(xa, xb, ma, mb, e2):
        r = xb - xa; d2 = np.sum(r * r, axis=-1) + e2
        return (Gk * ma * mb / d2 ** 1.5)[..., None] * r        # force on a from b

    def shell_on(xp, mp, Xc, w, s, al):
        r = xp - Xc; rr = np.sqrt(np.sum(r * r, axis=-1))
        inside = (rr[..., None] > s[None, :]) & al[None, :] if r.ndim == 2 else (rr > s) & al
        Min = (inside * w[None, :]).sum(-1) if r.ndim == 2 else float(np.sum(w[inside]))
        return -(Gk * mp * Min / np.maximum(rr, 1e-9) ** 3)[..., None] * r if r.ndim == 2 else -(Gk * mp * Min / max(rr, 1e-9) ** 3) * r

    def forces():
        fH = np.zeros(3); fB = np.zeros(3); fS = np.zeros(3)
        f = soft(xH, xB, mH, m_b, eps_H ** 2 + eps_b ** 2); fH += f; fB -= f
        f = shell_on(xH, mH, XS, wk, sh, alive); fH += f; fS -= f
        f = shell_on(xB, m_b, XS, wk, sh, alive); fB += f; fS -= f
        fd = np.zeros_like(xd)
        if len(md):
            f = soft(xd, xH[None, :], md, mH, eps_H ** 2 + eps_d ** 2); fd += f; fH -= f.sum(0)
            f = soft(xd, xB[None, :], md, m_b, eps_b ** 2 + eps_d ** 2); fd += f; fB -= f.sum(0)
            f = shell_on(xd, md, XS, wk, sh, alive); fd += f; fS -= f.sum(0)
        return fH, fB, fS, fd

    def momentum():
        MS_c = float(np.sum(wk[alive]))
        return mH * vH + m_b * vB + MS_c * vS + (md[:, None] * vd).sum(0)

    def mass():
        return mH + m_b + float(np.sum(wk[alive])) + float(md.sum())

    def energy():                                                       # K + W of the pairs the dynamics includes (no dust-dust)
        MS_c = float(np.sum(wk[alive]))
        Kin = 0.5 * (mH * vH @ vH + m_b * vB @ vB + MS_c * vS @ vS + float(np.sum(md * np.sum(vd * vd, 1))))
        Wp = -Gk * mH * m_b / math.sqrt(float(np.sum((xB - xH) ** 2)) + eps_H ** 2 + eps_b ** 2)
        wa = np.where(alive, wk, 0.0)
        shp = lambda xp, mp: -Gk * mp * float(np.sum(wa / np.maximum(np.linalg.norm(xp - XS), sh)))
        Wp += shp(xH, mH) + shp(xB, m_b)
        if len(md):
            Wp += float(np.sum(-Gk * md * mH / np.sqrt(np.sum((xd - xH) ** 2, 1) + eps_H ** 2 + eps_d ** 2)))
            Wp += float(np.sum(-Gk * md * m_b / np.sqrt(np.sum((xd - xB) ** 2, 1) + eps_b ** 2 + eps_d ** 2)))
            rr = np.linalg.norm(xd - XS, axis=1)
            Wp += float(np.sum(-Gk * md * (wa[None, :] / np.maximum(rr[:, None], sh[None, :])).sum(1)))
        return Kin + Wp
    P0 = momentum(); M0 = mass(); pscale = M_S * np.linalg.norm(vS); E0 = energy()
    fH, fB, fS, fd = forces()
    nst = int(round(t_end / dt)); rJ_l = np.inf; events = []; drift = 0.0; mdrift = 0.0
    vr_prev = None
    for it in range(nst):
        MS_c = float(np.sum(wk[alive]))
        vH += 0.5 * dt * fH / mH; vB += 0.5 * dt * fB / m_b; vS += 0.5 * dt * fS / MS_c
        if len(md): vd += 0.5 * dt * fd / md[:, None]
        xH += dt * vH; xB += dt * vB; XS += dt * vS
        if len(md): xd += dt * vd
        fH, fB, fS, fd = forces()
        MS_c = float(np.sum(wk[alive]))
        vH += 0.5 * dt * fH / mH; vB += 0.5 * dt * fB / m_b; vS += 0.5 * dt * fS / MS_c
        if len(md): vd += 0.5 * dt * fd / md[:, None]
        rel = XS - xH; dd = float(np.linalg.norm(rel)); vr = float(np.dot(rel, vS - vH)) / dd
        if vr_prev is not None and vr_prev < 0 <= vr:                      # pericentre: King r_J (point host), latched
            cum_b = m_b * np.interp(sh, sk, shape) + np.cumsum(np.where(alive, wk, 0.0))
            X_ = dd ** 3 / (3.0 * mH)
            q = np.maximum.accumulate(sh ** 3 / np.maximum(cum_b, 1e-300))
            rJ = float(np.exp(np.interp(math.log(X_), np.log(q), np.log(sh)))) if X_ < q[-1] else np.inf
            rJ_l = min(rJ_l, rJ)
            strip = alive & (sh >= rJ_l)
            if strip.any():
                Pb_ = momentum(); Mb_ = mass(); Eb_ = energy(); dM = float(wk[strip].sum()); PS = MS_c * np.linalg.norm(vS - vH)
                if mode == "drev":
                    nx = []; nm = []
                    for kk in np.where(strip)[0]:
                        nx.append(XS[None, :] + sh[kk] * nvec); nm.append(np.full(len(nvec), wk[kk] / len(nvec)))
                    xd = np.vstack([xd] + nx); md = np.concatenate([md] + nm); vd = np.vstack([vd, np.repeat(vS[None, :], len(np.concatenate(nm)), 0)])
                    alive = alive & ~strip
                else:                                                   # relocation into the host at the host's velocity
                    alive = alive & ~strip; mH = mH + dM
                Pa_ = momentum(); Ma_ = mass(); Ea_ = energy()
                fH, fB, fS, fd = forces()
                events.append(dict(t=it * dt, d_kpc=dd, rJ=rJ_l, dM_over_MS=dM / M_S, dP_over_Psat=float(np.linalg.norm(Pa_ - Pb_) / max(PS, 1e-300)),
                                   dM_rel=abs(Ma_ - Mb_) / Mb_, dE_over_absE=(Ea_ - Eb_) / abs(E0)))
        vr_prev = vr
        drift = max(drift, float(np.linalg.norm(momentum() - P0) / pscale)); mdrift = max(mdrift, abs(mass() - M0) / M0)
        if it % 500 == 0:
            guard("nbody")
    E1_ = energy()
    return dict(u=u, mode=mode, n_events=len(events), events=events, P_drift=drift, M_drift=mdrift,
                max_event_dP=max([e["dP_over_Psat"] for e in events], default=0.0), n_dust=int(len(md)), M_S=M_S, frac_body_left=float(np.sum(wk[alive]) / wk.sum()),
                E_change_total_over_absE=(E1_ - E0) / abs(E0), E_events_sum_over_absE=float(sum(e["dE_over_absE"] for e in events)))


# ================================================================================================ (c1) Coma UDG r_J with SCT-U masses
def udg_rj(row, foot, D, um, N959):
    a0 = A0SI[foot]; Mst = row["L"] * row["ML"]; M = Mst * MSUN; a = row["Re"] * KPC_SI; r12 = 4.0 / 3.0 * a
    law = lambda g: g * nu_e(g / a0)
    gNx = lambda x: G_SI * plummer_M(M, a, x) / x ** 2
    if um == 0.0:
        Mfun = lambda x: law(gNx(x)) * x * x / G_SI                  # CFG954 udg_sct: the nu_e-law mass
    else:
        h = N959["halo_gal"](Mst)
        Mfun = lambda x: plummer_M(M, a, x) + um * float(N959["McNFW"](h, x / KPC_SI)) * MSUN + (1 - um) * (law(gNx(x)) * x * x / G_SI - plummer_M(M, a, x))
    r = D * KPC_SI; Mh = g_host_coma(D) * r * r / G_SI; tmg = 2.0 * r * r / (r * r + RCB * RCB)
    fJ = lambda lx: math.log(math.exp(lx) ** 3 * tmg * Mh) - math.log(Mfun(math.exp(lx)) * r ** 3)
    lo, hi = math.log(1e-3 * a), math.log(min(1e4 * a, 0.999 * r))
    rJ = math.exp(brentq(fJ, lo, hi, xtol=1e-12)) if fJ(lo) < 0 < fJ(hi) else (math.exp(hi) if fJ(hi) <= 0 else math.exp(lo))
    return dict(rJ_kpc=rJ / KPC_SI, r12_kpc=r12 / KPC_SI, rJ_over_r12=rJ / r12)


# ================================================================================================ (g) Bullet with native dust (u = 1)
def bullet_sctu(foot, R930):
    f = FL[foot]
    with contextlib.redirect_stdout(io.StringIO()):
        main = P599.Progenitor599(1.5e15, f, cloud=False); sub = P599.Progenitor599(1.5e14, f, cloud=True)
    ok = main.r > 0; r = main.r[ok]; s = sub.r[ok]
    out = {}
    for nm, pr in (("main", main), ("sub", sub)):
        fr, Mta = R930["mta_fixed"](float(pr.Mb)); c, rs, rb, zc = R930["prof930"](Mta, 0.296, 3000.0, "rta")
        Mc = (1 - R930["FBN"]) * Mta * np.asarray(R930["m_"](np.minimum(pr.r[ok], rb) / rs), float) / float(R930["m_"](c))
        out[nm] = dict(Mc=Mc, Mta=Mta, fret=fr, c=c, rs=rs, rb=rb, zc=zc)
    tab = host_table(r, main.Mbar[ok] + out["main"]["Mc"])
    mcum_sub = sub.Mbar[ok] + out["sub"]["Mc"]
    dfine = np.geomspace(1.0, 720.0, 4000)
    rJf = np.minimum(rJ_at(tab, dfine, s, mcum_sub), 1e12)
    Mcs = out["sub"]["Mc"]; core = float(np.interp(200.0, s, Mcs))
    phiJ = 1.0 - np.interp(np.minimum(rJf, 200.0), s, Mcs, left=0.0) / core
    rJ720 = float(np.minimum(rJ_at(tab, np.array([720.0]), s, mcum_sub), 1e12)[0])
    return dict(dfine=dfine, rJ=rJf, phi_J=phiJ, rJ_720=rJ720, main=dict((k, v) for k, v in out["main"].items() if k != "Mc"),
                sub=dict((k, v) for k, v in out["sub"].items() if k != "Mc"), core_cold_200=core)


# ================================================================================================ (h) satellites (CFG953 (c) machinery)
def sat_u(N3, N959, Mb_sun, a_pc, rkpc, a0, mode):
    """mode 'u1': the satellite's cold is its native debris (u = 1), truncated at its Jacobi radius, no body (EFE 0);
    mode 'u0trunc': CFG953's body truncated at the Jacobi radius (U2).  Delta a / g_host as CFG953 sat_c."""
    G_SI3, MS847, PC3, KPC3 = N3["G_SI"], N3["MSUN847"], N3["PC"], N3["KPC847"]
    M = Mb_sun * MS847; a = a_pc * PC3; Mh = N3["HOST938"] * MS847; D = rkpc * KPC3
    Mbr = lambda s: M * s ** 3 / (s * s + a * a) ** 1.5
    gh = lambda rho: N3["law_simple"](G_SI3 * Mh / rho ** 2, a0)
    ghD = float(gh(D)); Mheff = D * D * ghD / G_SI3
    if mode == "u1":
        h = N959["halo_gal"](Mb_sun)
        Mcold = lambda s: float(N959["McNFW"](h, s / KPC3)) * MS847
        r_edge = h["rb"] * KPC3
    else:
        Nn = N3["domain_sct"](Mb_sun, a0)["N"]; Mc = Nn * M
        Mph = lambda s: s * s * (float(N3["law_simple"](G_SI3 * Mbr(s) / s ** 2, a0)) - G_SI3 * Mbr(s) / s ** 2) / G_SI3
        r_edge = math.exp(brentq(lambda ls: Mph(math.exp(ls)) - Mc, math.log(1e-3 * a), math.log(1e7 * a), xtol=1e-14, rtol=1e-14))
        Mcold = lambda s: min(Mph(s), Mc)
    fJ = lambda ls: 3 * ls - math.log(Mbr(math.exp(ls)) + Mcold(math.exp(ls))) - math.log(D ** 3 / (3 * Mheff))
    rJ = math.exp(brentq(fJ, math.log(1e-3 * a), math.log(0.999 * D), xtol=1e-12))
    cut = min(rJ, r_edge)
    sg = np.geomspace(1e-4 * a, cut, 1500); Msg = np.array([Mcold(x) for x in sg]); dMs = np.diff(Msg); sm = np.sqrt(sg[1:] * sg[:-1])
    bg = np.geomspace(1e-4 * a, 1e3 * a, 1500); Mbg = np.array([Mbr(x) for x in bg]); dMb = np.diff(Mbg); bm = np.sqrt(bg[1:] * bg[:-1])
    GLX, GLW = N3["GL_X"], N3["GL_W"]

    def mean_g(s):
        rho = np.sqrt(D * D + s[:, None] ** 2 + 2 * D * s[:, None] * GLX[None, :])
        return 0.5 * (gh(rho) * (D + s[:, None] * GLX[None, :]) / rho * GLW[None, :]).sum(1)
    gs_mean = float(np.sum(dMs * mean_g(sm)) / np.sum(dMs)); gb_mean = float(np.sum(dMb * mean_g(bm)) / np.sum(dMb))
    Da = abs(gs_mean - gb_mean)
    if mode == "u1":
        efe = 0.0; deq = None
    else:
        Mc_cut = Mcold(cut)
        rho_b = lambda s: 3 * M * a * a / (4 * math.pi * (s * s + a * a) ** 2.5)
        Kbs = (4 * math.pi * G_SI3 / 3) * float(np.sum(np.array([rho_b(x) for x in sm]) * dMs))
        deq = Da / (Kbs * (1 / M + 1 / Mc_cut))
        gsig = lambda s: G_SI3 * Mcold(s) / s ** 2
        hh = 1e-4 * a; dgs = abs(gsig(a + hh) - gsig(a - hh)) / (2 * hh)
        dg = max(dgs * deq, gsig(a) * deq / a)
        gsat = float(N3["law_simple"](G_SI3 * Mbr(a) / a ** 2, a0))
        efe = math.log10(1 + dg / gsat)
    return dict(ratio=Da / ghD, efe_dex=efe, rJ_kpc=rJ / KPC3, cut_kpc=cut / KPC3, edge_kpc=r_edge / KPC3,
                cold_in_cut_over_Mb=Mcold(cut) / M, deq_over_a=(None if deq is None else deq / a))


# ================================================================================================ K stage
def stage_K():
    RES = {}
    W = W954_arrays(); acc, C686 = accept_inputs()
    R954 = J("CFG954_sct_clusters_mergers", "cfg954_results.json"); R954M = J("CFG954_sct_clusters_mergers", "cfg954_results_MUTATE.json")
    idx = np.arange(NE_ALL)
    # ---- K1 CFG954 numbers
    d1 = 0.0; k1 = {}
    for foot in FEET:
        tr = score_TR({v: W[("E", foot)][v] for v in ("R1PS", "R2", "R3", "law", "na_sct", "hmm")})
        ta = score_TA({v: W[("A", foot)][v] for v in ("R1PS", "R2", "R3", "law", "na_sct", "hmm")}, C686)
        for v in ("R1PS", "R2", "R3", "law"):
            ref = R954["T_R"][foot][v]; refA = R954["T_A"][foot][v]
            for b in ("MID", "OUTER"):
                d1 = max(d1, abs(tr[v]["A"][b][0] - ref["A"][b][0]), abs(tr[v]["A"][b][1] - ref["A"][b][1]), abs(ta[v]["A"][b][0] - refA["A"][b][0]))
            d1 = max(d1, abs(tr[v]["s"] - ref["s"]), abs(tr[v]["Z_outer"] - ref["Z_outer"]))
        for v in ("na_sct", "hmm"):
            ref = R954M["MU_NA"][foot]["TR"][v]
            d1 = max(d1, max(abs(tr[v]["A"][b][0] - ref["A"][b][0]) for b in ("MID", "OUTER")), abs(tr[v]["Z_outer"] - ref["Z_outer"]))
        k1[foot] = {v: dict(MID=tr[v]["A"]["MID"], OUTER=tr[v]["A"]["OUTER"], Z_mid=tr[v]["Z_mid"], Z_outer=tr[v]["Z_outer"], s=tr[v]["s"],
                            ACC_OUTER=ta[v]["A"]["OUTER"]) for v in tr}
    check("K1 CFG954 stored arrays (R1PS, R2, R3, law, never-absorb, H-MM) scored = cfg954_results(.json, _MUTATE.json) (<= 1e-12)", d1 <= 1e-12,
          f"max |diff| {d1:.1e}; R1[P-S] OUTER {k1['canonical']['R1PS']['OUTER'][0]:.3f} / {k1['alt']['R1PS']['OUTER'][0]:.3f}; R2 OUTER {k1['canonical']['R2']['OUTER'][0]:.3f} / "
          f"{k1['alt']['R2']['OUTER'][0]:.3f}; never-absorb OUTER {k1['canonical']['na_sct']['OUTER'][0]:.3f} / {k1['alt']['na_sct']['OUTER'][0]:.3f}; "
          f"R3 MID {k1['canonical']['R3']['MID'][0]:.3f} / {k1['alt']['R3']['MID'][0]:.3f}")
    RES["K1"] = dict(scored=k1, maxdiff=d1)
    guard("K1")
    # ---- K2 CFG954's runner recomputes R2, R3
    lamj = json.load(_REAL_OPEN(os.path.join(W726, "lambda.json"))); Nm = np.array(lamj["Nmem"])
    d2 = 0.0
    for foot in FEET:
        for i in list(idx[:6]):
            ctx = cluster_ctx(erass_gas(int(i), PC7), 0.20, float(PC7["z"][i]), float(Nm[i]), foot)
            for rule in ("R2", "R3"):
                o = run_sct(ctx, rule, "peri", True)
                d2 = max(d2, float(np.max(np.abs(dsig_from_M(o["Mtot"]) / W[("E", foot)][rule][int(i)] - 1))))
    check("K2 CFG954's exec'd runner recomputes R2 and R3 (6 eRASS1 clusters, both footings) = stored arrays (<= 1e-10)", d2 <= 1e-10, f"max rel {d2:.1e}")
    RES["K2"] = dict(maxrel=d2)
    guard("K2")
    # ---- galaxy / B0 machinery
    N959 = load_959(); N9 = N959["N9"]; guard("cfg959 slice")
    STE, s_model, dsn, MS9 = N9["STE"], N9["s_model"], N9["dsig_newton"], N9["MSUN"]
    R949 = J("CFG949_clusters_untethered", "cfg949_results.json")["main"]
    Mc_all, _m = N9["build_cold"]("C3000|rta", "S-cen", N9["GAS"], 0.20)
    Pb = dsn(N9["MB"]); Pc = dsn(Mc_all); del Mc_all
    bd = STE.band(Pb + Pc); s0 = s_model(Pb + Pc)
    d3 = max(max(max(abs(bd[b][0] - R949["B0_primary"]["A"][b][0]), abs(bd[b][1] - R949["B0_primary"]["A"][b][1])) for b in ("MID", "OUTER")),
             abs(s0 - R949["B0_primary"]["s"]))
    AH = accept_hosts(N9); bA = AH["STA"].band(dsn(AH["MBA"]) + dsn(AH["McA"]))
    d3a = max(max(abs(bA[b][0] - R949["ACCEPT8"]["B0"][b][0]), abs(bA[b][1] - R949["ACCEPT8"]["B0"][b][1])) for b in ("MID", "OUTER"))
    check("K3 CFG949 B0: eRASS1 A_MID, A_OUTER, s and ACCEPT 8 B0 bands = cfg949_results.json (<= 1e-9)", max(d3, d3a) <= 1e-9,
          f"eRASS1 MID {bd['MID'][0]:.4f}±{bd['MID'][1]:.4f} OUTER {bd['OUTER'][0]:.4f}±{bd['OUTER'][1]:.4f} s {s0:.4f}; ACCEPT MID {bA['MID'][0]:.3f}±{bA['MID'][1]:.3f} "
          f"OUTER {bA['OUTER'][0]:.3f}±{bA['OUTER'][1]:.3f} (diff {d3:.1e} / {d3a:.1e})")
    RES["K3"] = dict(eRASS1=bd, s=s0, ACCEPT=bA, maxdiff=[d3, d3a])
    guard("K3")
    # ---- K4 CFG959 numbers through its slice
    R959 = J("CFG959_excess_unrelaxed_native", "cfg959_results.json")["primary"]
    d4 = []; k4 = {}
    for foot in FEET:
        N959["A0F"] = N959["A0X"][foot]; st = R959[foot]
        a = N959["sparc_fit"]("PLIN", "RC", N959["PRIM"]); Ep = N959["dw_pred"](foot, "PLIN", "RC", N959["PRIM"]); b = N959["dw_class"](foot, Ep)
        c = N959["coma_eval"](foot, "PLIN", "RC", N959["PRIM"]); e = N959["lens_class"](foot, "LS", "PLIN", "RC", N959["PRIM"]); f_ = N959["f_items"](foot)
        dcl = N959["cluster_eval"](foot, "PLIN", "RC", N959["PRIM"])
        d4 += [abs(a["rms"] - st["a"]["rms"]), abs(a["U"] - st["a"]["U"]), abs(b["E"] - st["b"]["E"]), abs(b["se"] - st["b"]["se"]),
               abs(c["mean_res"] - st["c"]["mean_res"]), abs(c["se_res"] - st["c"]["se_res"]), abs(e["E"] - st["e"]["obs"]["E"]),
               abs(f_["TDG_dex"]["rbar"] - st["f"]["TDG_dex"]["rbar"]), abs(f_["DF_ln"]["rbar"] - st["f"]["DF_ln"]["rbar"])]
        d4 += [abs(dcl["A"][bb][kk] - st["d"]["A"][bb][kk]) for bb in ("MID", "OUTER") for kk in (0, 1)] + [abs(dcl["s"] - st["d"]["s"])]
        k4[foot] = dict(sparc=(a["rms"], a["U"], a["u_median"]), dsph=(b["E"], b["se"], b["z"]), coma=(c["mean_res"], c["se_res"], c["z"]),
                        red_lens=e["E"], TDG=f_["TDG_dex"]["rbar"], DF=f_["DF_ln"]["rbar"], clusters=(dcl["A"]["MID"], dcl["A"]["OUTER"], dcl["s"]))
    check("K4 CFG959 primary items through its exec'd slice (SPARC, dSph, Coma, red lenses, TDG/DF, clusters = B0) = cfg959_results.json (<= 1e-9)",
          max(d4) <= 1e-9, f"max |diff| {max(d4):.1e}; SPARC {k4['canonical']['sparc'][0]:.4f} / {k4['alt']['sparc'][0]:.4f}; dSph resid {k4['canonical']['dsph'][0]:+.3f} ln; "
          f"Coma resid {k4['canonical']['coma'][0]:+.3f}±{k4['canonical']['coma'][1]:.3f}; clusters MID {k4['canonical']['clusters'][0][0]:.4f} OUTER {k4['canonical']['clusters'][1][0]:.4f}")
    RES["K4"] = dict(items=k4, maxdiff=max(d4))
    guard("K4")
    # ---- K5 reading N
    d5 = 0.0
    for foot in FEET:
        nmm = STE.band(W[("N", foot)]["NM"]); ref = R954["reading_N"]["scores"][foot]["N_members"]
        d5 = max(d5, max(abs(nmm[b][0] - ref["A"][b][0]) for b in ("MID", "OUTER")), abs(s_model(W[("N", foot)]["NM"]) - ref["s"]))
    check("K5 CFG954 reading N (N+members) stored arrays scored with CFG949's STE = cfg954_results.json (<= 1e-12)", d5 <= 1e-12, f"max |diff| {d5:.1e}")
    RES["K5"] = dict(maxdiff=d5)
    # ---- K6 toy
    d6 = 0.0; d6b = 0.0; k6 = {}
    for foot in FEET:
        for q in (1.0, 1 / 3, 0.1):
            ref = R954["toy"][f"{foot}|q{q:.3f}"]["rules"]
            tv = toy_sct(q, foot)
            for rule in ("R1PS", "R1PI", "R2", "R3"):
                d6 = max(d6, abs(tv["rules"][rule]["J_max"] - ref[rule]["J_max"]), abs(tv["rules"][rule]["J1_max"] - ref[rule]["J1_max"]),
                         abs(tv["rules"][rule]["J2_max"] - ref[rule]["J2_max"]))
            mine = toy_sctu(q, foot, 0.0, N9, r7=False)
            d6b = max(d6b, abs(mine["J_max"] - ref["R2"]["J_max"]), abs(mine["J1_max"] - ref["R2"]["J1_max"]), abs(mine["J2_max"] - ref["R2"]["J2_max"]),
                      max(abs(mine["E1_final"][k] - ref["R2"]["E1_final"][k]) for k in mine["E1_final"]))
            k6[f"{foot}|q{q:.3f}"] = dict(R2_J=ref["R2"]["J_max"], mine_u0_noR7=mine["J_max"])
            guard("K6")
    check("K6 CFG954's exec'd toy = its stored J (<= 1e-12); this lane's SCT-U toy at u = 0, R7 off = CFG954's R2 row (J, E1 finals; <= 1e-10)",
          d6 <= 1e-12 and d6b <= 1e-10, f"max |diff| {d6:.1e} / {d6b:.1e}; R2 J (q 1) {k6['canonical|q1.000']['R2_J']:.4f} vs mine {k6['canonical|q1.000']['mine_u0_noR7']:.4f}")
    RES["K6"] = dict(maxdiff=[d6, d6b], rows=k6)
    # ---- K7 King r_J
    C916 = J("CFG916_lock_and_release", "cfg916_cache.json"); d7 = 0.0; bl = {}
    for foot in FEET:
        b_ = bullet_sct(foot); ref = C916["misc"]["B"][FL[foot]]
        d7 = max(d7, abs(b_["rJ_present"] / ref["rJ_present"] - 1), float(np.max(np.abs(b_["rJ_grid"] / np.array(ref["rJ_grid"]) - 1)))); bl[foot] = b_["rJ_present"]
    medK = {f: float(np.median([x["K5_rJp_med"] for x in W[("Ed", f)]])) for f in FEET}
    refK = {f: C916["M"]["eRASS1"]["summary"][FL[f]]["rJp_med_kpc"] for f in FEET}
    d7b = max(abs(medK[f] / refK[f] - 1) for f in FEET)
    check("K7 CFG916 King r_J: Bullet sub at 720 kpc + grid (<= 1e-9); eRASS1 pericentre median from CFG954's stored diagnostics (<= 1e-6)",
          d7 <= 1e-9 and d7b <= 1e-6, f"r_J(720) {bl['canonical']:.2f} / {bl['alt']:.2f} kpc (diff {d7:.1e}); median {medK['canonical']:.3f} / {medK['alt']:.3f} kpc (diff {d7b:.1e})")
    RES["K7"] = dict(rJ_720=bl, eRASS1_med=medK, maxdiff=[d7, d7b])
    # ---- K8 CFG953 sat_c
    N3 = load_953(); R953 = J("CFG953_source_changing_theory", "cfg953_results.json")["c"]["C"]; d8 = 0.0
    for key, ref in R953.items():
        foot, nm, rk = key.split("|"); Mb_, apc = [(m_, a_) for n_, m_, a_ in N3["HOSTS882"] if n_ == nm][0]
        mine = N3["sat_c"](Mb_, apc, float(rk), N3["A0"][foot])
        d8 = max(d8, max(abs(mine[k] - ref[k]) / max(abs(ref[k]), 1e-300) for k in ref))
    check("K8 CFG953's exec'd sat_c reproduces its stored (c) values, 18 cases (<= 1e-12 relative)", d8 <= 1e-12 and len(R953) == 18, f"max rel {d8:.1e}; n {len(R953)}")
    RES["K8"] = dict(maxrel=d8)
    # ---- K9 member body at u = 0 == h; host baryons
    A, D = load_compute(); k9 = all(x["K9_body_eq_h"] for f in FEET for x in D[f"{f}|E"]); mb = max(x["K9_Mb_maxrel"] for f in FEET for x in D[f"{f}|E"])
    k9a = all(x["K9_body_eq_h"] for f in FEET for x in D[f"{f}|A"]); mba = max(x["K9_Mb_maxrel"] for f in FEET for x in D[f"{f}|A"])
    check("K9 member body at u_m = 0 == CFG954's h (every eRASS1 and ACCEPT cluster, both footings); B0 host baryons vs CFG954 ctx (<= 1e-6)",
          k9 and k9a and mb <= 1e-6, f"body == h: eRASS1 {k9}, ACCEPT {k9a}; M_b max rel: eRASS1 {mb:.1e} (ACCEPT, reported: {mba:.1e})")
    RES["K9"] = dict(body_eq_h=[k9, k9a], Mb_maxrel=[mb, mba])
    # ---- K10 scorers
    d10 = 0.0
    for foot in FEET:
        a1 = STE.band(W[("E", foot)]["law"]); a2 = score_TR({"l": W[("E", foot)]["law"]})["l"]
        d10 = max(d10, max(abs(a1[b][0] - a2["A"][b][0]) + abs(a1[b][1] - a2["A"][b][1]) for b in ("MID", "OUTER")))
    check("K10 CFG949 STE.band == CFG954 score_TR on CFG954's stored law arrays (<= 1e-9)", d10 <= 1e-9, f"max |diff| {d10:.1e}")
    RES["K10"] = dict(maxdiff=d10)
    # ---- extra (not frozen): this lane's UDG r_J solver at u = 0 == CFG954 udg_sct
    rows = udg_rows(); names = list(J("CFG948_nocapture_vs_udgs", "cfg948_results.json")["A_per_galaxy"]["canonical"].keys()); dx = 0.0
    for foot in FEET:
        for n in names:
            dx = max(dx, abs(udg_rj(rows[n], foot, rows[n]["dmean"], 0.0, N959)["rJ_kpc"] / udg_sct(rows[n], foot, rows[n]["dmean"])["rJ_kpc"] - 1))
    check("K-extra (not frozen): this lane's UDG King r_J at u = 0 == CFG954 udg_sct (9 UDGs, dmean, both footings; <= 1e-9)", dx <= 1e-9, f"max rel {dx:.1e}")
    RES["K_extra_udg"] = dict(maxrel=dx)
    RES["checks"] = CHK; RES["K_all"] = all(v["ok"] for v in CHK.values())
    P(f"\nK: {sum(v['ok'] for v in CHK.values())}/{len(CHK)} pass")
    return RES


# ================================================================================================ MUTATE stage
def stage_mutate():
    RES = {}
    A, D = load_compute(); W = W954_arrays(); acc, C686 = accept_inputs()
    N9 = load_949(); STE = N9["STE"]
    # MU-U0
    dR3 = 0.0; zi = {}; zii = {}
    for foot in FEET:
        dR3 = max(dR3, float(np.max(np.abs(A[f"{foot}|E|MU_U0_R3"] / W[("E", foot)]["R3"] - 1))), float(np.max(np.abs(A[f"{foot}|A|MU_U0_R3"] / W[("A", foot)]["R3"] - 1))))
        t = score_TR({"x": A[f"{foot}|E|MU_U0_R3"]})["x"]; zi[foot] = dict(MID=t["A"]["MID"], Z_mid=t["Z_mid"], OUTER=t["A"]["OUTER"], Z_outer=t["Z_outer"])
        bd = STE.band(A[f"{foot}|E|MU_U0_B0"]); zii[foot] = dict(MID=bd["MID"], Z_mid=bandZ(bd, "MID"), OUTER=bd["OUTER"], Z_outer=bandZ(bd, "OUTER"))
        P(f"  MU-U0 {foot}: (i) u = 0, CFG954 supply/baryons, R7 off: MID {t['A']['MID'][0]:.3f}±{t['A']['MID'][1]:.3f} (Z {t['Z_mid']:+.2f}) OUTER {t['A']['OUTER'][0]:.3f} "
          f"(Z {t['Z_outer']:+.2f}); (ii) u = 0, B0 baryons/supply, R7 on: MID {bd['MID'][0]:.3f}±{bd['MID'][1]:.3f} (Z {bandZ(bd, 'MID'):+.2f}) OUTER {bd['OUTER'][0]:.3f} (Z {bandZ(bd, 'OUTER'):+.2f})")
    bite_u0 = dR3 <= 1e-10 and all(zi[f]["Z_mid"] >= 2 for f in FEET) and all(zii[f]["Z_mid"] >= 2 for f in FEET)
    check("MU-U0 u = 0: (i) reproduces CFG954's R3 arrays (eRASS1 + ACCEPT, both footings, <= 1e-10) and fails the core; (ii) with B0 baryons/supply also fails the core (Z_MID >= +2 both)",
          bite_u0, f"R3 max rel {dR3:.1e}; Z_MID (i) {zi['canonical']['Z_mid']:+.2f} / {zi['alt']['Z_mid']:+.2f}; (ii) {zii['canonical']['Z_mid']:+.2f} / {zii['alt']['Z_mid']:+.2f}")
    RES["MU_U0"] = dict(i=zi, ii=zii, R3_maxrel=dR3, bites=bite_u0)
    # MU-NS
    dNA = 0.0; ni = {}; nii = {}
    for foot in FEET:
        dNA = max(dNA, float(np.max(np.abs(A[f"{foot}|E|MU_NS_U0"] / W[("E", foot)]["na_sct"] - 1))), float(np.max(np.abs(A[f"{foot}|A|MU_NS_U0"] / W[("A", foot)]["na_sct"] - 1))))
        t = score_TR({"x": A[f"{foot}|E|MU_NS_U0"]})["x"]; ni[foot] = dict(MID=t["A"]["MID"], Z_mid=t["Z_mid"], OUTER=t["A"]["OUTER"], Z_outer=t["Z_outer"])
        bd = STE.band(A[f"{foot}|E|MU_NS_U"]); nii[foot] = dict(MID=bd["MID"], Z_mid=bandZ(bd, "MID"), OUTER=bd["OUTER"], Z_outer=bandZ(bd, "OUTER"))
        P(f"  MU-NS {foot}: (i) u = 0, no stripping: OUTER {t['A']['OUTER'][0]:.3f}±{t['A']['OUTER'][1]:.3f} (Z {t['Z_outer']:+.2f}) MID {t['A']['MID'][0]:.3f}; "
          f"(ii) primary u, no stripping: OUTER {bd['OUTER'][0]:.3f}±{bd['OUTER'][1]:.3f} (Z {bandZ(bd, 'OUTER'):+.2f}) MID {bd['MID'][0]:.3f} (Z {bandZ(bd, 'MID'):+.2f})")
    bite_ns = dNA <= 1e-10 and all(ni[f]["Z_outer"] <= -2 for f in FEET) and all(nii[f]["Z_outer"] <= -2 for f in FEET)
    check("MU-NS no stripping: (i) u = 0 reproduces CFG954's never-absorb arrays (<= 1e-10) and fails OUTER; (ii) the primary u's also fail OUTER (Z_OUTER <= -2 both)",
          bite_ns, f"never-absorb max rel {dNA:.1e}; Z_OUTER (i) {ni['canonical']['Z_outer']:+.2f} / {ni['alt']['Z_outer']:+.2f}; (ii) {nii['canonical']['Z_outer']:+.2f} / {nii['alt']['Z_outer']:+.2f}")
    RES["MU_NS"] = dict(i=ni, ii=nii, na_maxrel=dNA, bites=bite_ns)
    d0 = max(float(np.max(np.abs(A[f"{f}|{s}|MU_0"] / A[f"{f}|{s}|B0"] - 1))) for f in FEET for s in ("E", "A"))
    check("MU-0 control: no members through the SCT-U runner gives B0 exactly (<= 1e-12, every bin, eRASS1 + ACCEPT, both footings)", d0 <= 1e-12, f"max rel {d0:.1e}")
    RES["MU_0"] = dict(maxrel=d0)
    RES["checks"] = CHK
    return RES


# ================================================================================================ MAIN stage
def stage_main():
    RES = {"lane": "CFG962", "criteria": CRIT, "post_hoc": True,
           "settings": dict(kappa="1/2 FITTED", footings=A0SI, kernel="nu_s (bodies); record estimators keep their own", u=dict(
               cluster_domains=1.0, members=U_MEM, members_B3=U_MEM_B3, dSph_UDG_satellites=1.0, SPARC="3 s^2/(V_flat^2 + 3 s^2), s 10 km/s"))}
    A, D = load_compute(); acc, C686 = accept_inputs()
    N959 = load_959(); N9 = N959["N9"]; guard("cfg959 slice")
    STE, s_model = N9["STE"], N9["s_model"]
    AH = accept_hosts(N9); STA = AH["STA"]
    # ---- (a) eRASS1 and (b-ACC) ACCEPT
    VN = ["U"] + list(BRACKETS) + ["U_um0", "U_um1", "B0"]
    TR = {f: {} for f in FEET}; TRp = {f: {} for f in FEET}; TA = {f: {} for f in FEET}
    for f in FEET:
        for v in VN:
            Pm = A[f"{f}|E|{v}"]; bd = STE.band(Pm)
            TR[f][v] = dict(A=bd, Z_mid=bandZ(bd, "MID"), Z_outer=bandZ(bd, "OUTER"), s=s_model(Pm))
            ba = STA.band(A[f"{f}|A|{v}"]); TA[f][v] = dict(A=ba, Z_mid=bandZ(ba, "MID"), Z_outer=bandZ(ba, "OUTER"))
            if v + "_prev" in [k.split("|")[2] for k in A if k.startswith(f"{f}|E|")]:
                Pp = A[f"{f}|E|{v}_prev"]; bp = STE.band(Pp); TRp[f][v] = dict(Z_mid=bandZ(bp, "MID"), Z_outer=bandZ(bp, "OUTER"), s=s_model(Pp))
                bpa = STA.band(A[f"{f}|A|{v}_prev"]); TRp[f][v]["ACC_Z_outer"] = bandZ(bpa, "OUTER")
    RES["T_R"] = TR; RES["T_A"] = TA; RES["T_R_prev_iteration"] = TRp
    P("\n== (a) eRASS1 318 (CFG949 STE jackknife; s vs 0.896 ± 0.209) and (b-ACC) ACCEPT 8 (CFG949 Stack boot)")
    for v in VN:
        for f in FEET:
            t, a = TR[f][v], TA[f][v]
            P(f"  {v:10s} {f[:3]}: MID {t['A']['MID'][0]:.3f}±{t['A']['MID'][1]:.3f} (Z {t['Z_mid']:+.2f}) OUTER {t['A']['OUTER'][0]:.3f}±{t['A']['OUTER'][1]:.3f} "
              f"(Z {t['Z_outer']:+.2f}) INNER {t['A']['INNER'][0]:.3f} s {t['s']:.3f} ({(t['s'] - S_OBS) / S_ERR:+.2f} s_err) | ACCEPT MID {a['A']['MID'][0]:.3f} "
              f"OUTER {a['A']['OUTER'][0]:.3f}±{a['A']['OUTER'][1]:.3f} (Z {a['Z_outer']:+.2f})")
    # diagnostics
    DG = {}
    for f in FEET:
        DG[f] = {}
        for v in list(UVARS) + ["MU_U0_B0", "MU_NS_U"]:
            col = [x[v] for x in D[f"{f}|E"]]
            DG[f][v] = dict(iters_max=int(max(c["iters"] for c in col)), nonconv=int(sum(1 for c in col if c["conv"] > 1e-4)), conv_max=float(max(c["conv"] for c in col)),
                            n_floor=int(sum(1 for c in col if c["floor"])), book_resid_maxabs_unfloored=float(max([abs(c["book_resid"]) for c in col if not c["floor"]], default=0.0)),
                            **{k + "_med": float(np.median([c[k] for c in col])) for k in ("f_U", "C_over_Mstar", "C_over_S", "rJ_med", "merged_frac", "Mrem_over_S", "ORB_over_S")})
        DG[f]["members_total_over_SB0_med"] = float(np.median([x["members_total_over_SB0"] for x in D[f"{f}|E"]]))
        DG[f]["mi_med"] = float(np.median([x["mi"] for x in D[f"{f}|E"]])); DG[f]["SB0_over_Mstar_med"] = float(np.median([x["S_B0"] / x["Mstar"] for x in D[f"{f}|E"]]))
        u = DG[f]["U"]
        P(f"  diagnostics {f[:3]} (eRASS1 medians, primary U): f_U {u['f_U_med']:.3f}, C_J/M* {u['C_over_Mstar_med']:.2f}, C_J/S_B0 {u['C_over_S_med']:.3f}, r_J {u['rJ_med_med']:.0f} kpc, "
          f"merged {u['merged_frac_med']:.3f}, M_rem/S_B0 {u['Mrem_over_S_med']:.4f}; iterations <= {u['iters_max']}, nonconv {u['nonconv']} (max {u['conv_max']:.1e}); floors {u['n_floor']}; "
          f"bookkeeping |resid| max {u['book_resid_maxabs_unfloored']:.1e}; S_B0/M* {DG[f]['SB0_over_Mstar_med']:.1f}; members' whole cold / S_B0 {DG[f]['members_total_over_SB0_med']:.2f}")
    RES["diagnostics"] = DG
    # terciles (primary)
    mg = np.asarray(PC7["mg"], float); qq = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, qq[1:-1]), 0, 2)
    TER = {f: {str(t_): STE.A(A[f"{f}|E|U"], np.where(tid == t_)[0]) for t_ in range(3)} for f in FEET}
    RES["terciles_U"] = TER

    def c_item(key, v):
        c1 = cls2({f: TR[f][v][key] for f in FEET}); c0 = cls2({f: TRp[f][v][key] for f in FEET})
        return c1 if c1 == c0 else "UNDERDETERMINED"

    def c_s(v):
        c1 = cls_slope({f: TR[f][v]["s"] for f in FEET}); c0 = cls_slope({f: TRp[f][v]["s"] for f in FEET})
        return c1 if c1 == c0 else "UNDERDETERMINED"

    def c_acc(v):
        c1 = cls2({f: TA[f][v]["Z_outer"] for f in FEET}); c0 = cls2({f: TRp[f][v]["ACC_Z_outer"] for f in FEET})
        return c1 if c1 == c0 else "UNDERDETERMINED"

    def with_br(prim, brs):
        if prim == "UNDERDETERMINED":
            return "UNDERDETERMINED"
        return prim if all(b == prim for b in brs.values()) else "CONDITIONAL"
    CL = {}
    for item, fn in (("a-MID", lambda v: c_item("Z_mid", v)), ("a-OUTER", lambda v: c_item("Z_outer", v)), ("a-s", c_s), ("b-ACC", c_acc)):
        pr = fn("U"); brs = {b: fn(b) for b in BRACKETS}
        CL[item] = dict(primary=pr, brackets=brs, final=with_br(pr, brs))
    P("== (a)/(b-ACC) classes: " + "; ".join(f"{k} {v['final']} (primary {v['primary']}; brackets {v['brackets']})" for k, v in CL.items()))
    guard("a")
    # ---- (b-J) toy
    uS = float(np.median([N959["fP"](v_, 10.0) for v_ in N959["VFL"]]))
    RES["u_toy_primary_SPARC_median_fP"] = uS
    TOY = {}
    for f in FEET:
        for q in (1.0, 1 / 3, 0.1):
            for uu, lab_ in ((uS, "uS"), (0.80, "u08")):
                tv = TOY[f"{f}|q{q:.3f}|{lab_}"] = toy_sctu(q, f, uu, N9, r7=True)
                tn = toy_sctu(q, f, uu, N9, r7=False)
                tv["noR7"] = dict(J_max=tn["J_max"], J1_max=tn["J1_max"], J2_max=tn["J2_max"], E1_final=tn["E1_final"])
                P(f"  (b-J) toy {f[:3]} q {q:.3f} u {uu:.3f}: J {tv['J_max']:.4f} (E1 {tv['J1_max']:.4f}, E2 {tv['J2_max']:.4f}); R7 at d {tv['d_merge']:.1f} kpc "
                  f"(r_J {tv['rJ_at_merge']:.1f}); no-R7 J {tn['J_max']:.4f}; E1 final {tv['E1_final']}; label-1 cap use max {tv['T1_over_cap1_max']:.3f}")
                guard("toy")
    cJ_p = "CONSISTENT" if all(TOY[k]["J_max"] <= 0.05 for k in TOY if k.endswith("|uS")) else "INCONSISTENT"
    cJ_b = "CONSISTENT" if all(TOY[k]["J_max"] <= 0.05 for k in TOY if k.endswith("|u08")) else "INCONSISTENT"
    CL["b-J"] = dict(primary=cJ_p, brackets={"toy u 0.80": cJ_b}, final=(cJ_p if cJ_p == cJ_b else "CONDITIONAL"),
                     J_max_primary=max(TOY[k]["J_max"] for k in TOY if k.endswith("|uS")), J_max_bracket=max(TOY[k]["J_max"] for k in TOY if k.endswith("|u08")))
    RES["toy"] = TOY
    P(f"== (b-J) continuity: {CL['b-J']['final']} (primary {cJ_p}, max J {CL['b-J']['J_max_primary']:.4f}; u 0.80 bracket {cJ_b}, max J {CL['b-J']['J_max_bracket']:.4f})")
    # ---- (c) Coma UDGs
    rows = udg_rows(); R948 = J("CFG948_nocapture_vs_udgs", "cfg948_results.json"); names = list(R948["A_per_galaxy"]["canonical"].keys())
    UD = {}
    for f in FEET:
        rr = {}
        for dkey in ("dmean", "dproj"):
            rr[dkey] = {n: dict(u1=udg_rj(rows[n], f, rows[n][dkey], 1.0, N959), u0=udg_rj(rows[n], f, rows[n][dkey], 0.0, N959)) for n in names}
        N959["A0F"] = N959["A0X"][f]
        c1 = N959["coma_eval"](f, "PLIN", "RC", N959["PRIM"]); c0 = N959["coma_eval"](f, "ZERO", "RC", N959["PRIM"])
        sy = R948["byfoot"][f]["primary"]["sys_up"]["total"]
        UD[f] = dict(rJ=rr, min_rJ_over_r12_u1_dmean=min(x["u1"]["rJ_over_r12"] for x in rr["dmean"].values()),
                     min_rJ_over_r12_u1_dproj=min(x["u1"]["rJ_over_r12"] for x in rr["dproj"].values()),
                     min_rJ_over_r12_u0_dmean=min(x["u0"]["rJ_over_r12"] for x in rr["dmean"].values()),
                     u1=dict(mean_Eobs=c1["mean_Eobs"], mean_Epred=c1["mean_Epred"], resid=c1["mean_res"], se=c1["se_res"], z=c1["z"],
                             z_sys=c1["mean_res"] / math.sqrt(c1["se_res"] ** 2 + sy ** 2)),
                     u0=dict(mean_Epred=c0["mean_Epred"], resid=c0["mean_res"], se=c0["se_res"], z=c0["z"], z_sys=c0["mean_res"] / math.sqrt(c0["se_res"] ** 2 + sy ** 2)))
        P(f"  (c) UDGs {f[:3]}: r_J/r12 min (u = 1) {UD[f]['min_rJ_over_r12_u1_dmean']:.2f} at dmean, {UD[f]['min_rJ_over_r12_u1_dproj']:.2f} at dproj; (u = 0) {UD[f]['min_rJ_over_r12_u0_dmean']:.2f}; "
          f"u = 1: E_obs {c1['mean_Eobs']:+.3f}, E_pred {c1['mean_Epred']:+.3f}, resid {c1['mean_res']:+.3f}±{c1['se_res']:.3f} ln (z {c1['z']:+.2f}; with sys {UD[f]['u1']['z_sys']:+.2f}); "
          f"u = 0 (whole body kept = the law): resid {c0['mean_res']:+.3f} (z {c0['z']:+.2f}; with sys {UD[f]['u0']['z_sys']:+.2f})")
    CL["c1"] = dict(final="CONSISTENT" if all(UD[f]["min_rJ_over_r12_u1_dmean"] >= 1.0 for f in FEET) else "CONDITIONAL")
    CL["c2"] = dict(final="CONTRADICTED" if all(UD[f]["u1"]["z"] >= 3 for f in FEET) else ("TENSION" if all(UD[f]["u1"]["z"] >= 2 for f in FEET) else "NOT CONTRADICTED"))
    RES["udg"] = UD
    P(f"== (c1) stripping side effect on UDGs: {CL['c1']['final']}; (c2) UDG excess under u = f_P = 1: {CL['c2']['final']}")
    guard("UDG")
    # ---- (d) SPARC, (e) TDG/DF, (i) dSph
    GI = {}
    for f in FEET:
        N959["A0F"] = N959["A0X"][f]
        a = N959["sparc_fit"]("PLIN", "RC", N959["PRIM"]); a["drms"] = a["rms"] - {"canonical": 0.10090811294375761, "alt": 0.09943409571436324}[f]
        fi = N959["f_items"](f)
        Ep1 = N959["dw_pred"](f, "PLIN", "RC", N959["PRIM"]); b1 = N959["dw_class"](f, Ep1)
        Ep0 = N959["dw_pred"](f, "ZERO", "RC", N959["PRIM"]); b0 = N959["dw_class"](f, Ep0)
        ls = N959["lens_class"](f, "LS", "PLIN", "RC", N959["PRIM"]); ld = N959["lens_class"](f, "LD", "PLIN", "RC", N959["PRIM"])
        rB = N959["rot_eval"](f, "B", "PLIN", "RC", N959["PRIM"])
        GI[f] = dict(sparc=a, f=fi, dsph_sctu=dict(E=b1["E"], se=b1["se"], z=b1["z"], dex=b1["E"] / math.log(10), Epred_mean_dex=float(np.mean(Ep1)) / math.log(10)),
                     dsph_sctm=dict(E=b0["E"], se=b0["se"], z=b0["z"], dex=b0["E"] / math.log(10)),
                     red_lens=dict(E=ls["E"], se=ls["se"], z=ls["z"]), blue_lens=dict(E=ld["E"], se=ld["se"], z=ld["z"]),
                     rotators=dict(resid=rB["mean_res"], se=rB["se_res"], z=rB["z"]))
        P(f"  (d) SPARC {f[:3]}: rms {a['rms']:.4f} @ U {a['U']:.2f} (law {a['rms'] - a['drms']:.4f}; Δ {a['drms']:+.4f}); u median {a['u_median']:.3f}, max {a['u_max']:.2f} -> {'PASS' if a['passes'] else 'FAIL'}")
        P(f"  (e) {f[:3]}: TDGs {fi['TDG_dex']['rbar']:+.3f}±{fi['TDG_dex']['se']:.3f} dex (z {fi['TDG_dex']['z']:+.2f}); DF2/DF4 {fi['DF_ln']['rbar']:+.3f}±{fi['DF_ln']['se']:.3f} ln (z {fi['DF_ln']['z']:+.2f})")
        P(f"  (i) dSph {f[:3]}: SCT-U (u = 1) resid {b1['E'] / math.log(10):+.3f} dex (z {b1['z']:+.1f}; predicted mean {np.mean(Ep1) / math.log(10):+.3f} dex) vs SCT-M (law) "
          f"resid {b0['E'] / math.log(10):+.3f} dex (z {b0['z']:+.1f}); carried: red lenses {ls['E']:+.3f} ln (z {ls['z']:+.1f}), blue {ld['E']:+.3f} (z {ld['z']:+.1f}), "
          f"rotators {rB['mean_res']:+.3f} dex (z {rB['z']:+.1f})")
    CL["d"] = dict(final="PASS" if all(GI[f]["sparc"]["passes"] for f in FEET) else "FAIL")
    CL["e"] = dict(final="CONSISTENT" if all(abs(GI[f]["f"]["TDG_dex"]["z"]) < 2 and abs(GI[f]["f"]["DF_ln"]["z"]) < 2 for f in FEET) else "NOT CONSISTENT")
    CL["i"] = dict(final="WORSE" if all(abs(GI[f]["dsph_sctu"]["E"]) > abs(GI[f]["dsph_sctm"]["E"]) for f in FEET) else "NOT WORSE")
    RES["galaxy_items"] = GI
    guard("galaxy items")
    # ---- (f) momentum and mass
    FM = {}
    lamj = json.load(_REAL_OPEN(os.path.join(W726, "lambda.json"))); Nm = np.array(lamj["Nmem"])
    kmed = int(np.argmin(np.abs(mg - np.median(mg))))
    for f in FEET:
        ctx = cluster_ctx(erass_gas(kmed, PC7), 0.20, float(PC7["z"][kmed]), float(Nm[kmed]), f)
        bU, dU, _ = member_cold(R_OBS, ctx["shape"], ctx["mi"], float(PC7["z"][kmed]), f, U_MEM, N9)
        ev_c = drev_event_algebra(bU, dU, D[f"{f}|E"][kmed]["U"]["rJ_med"])
        sk = R_OBS; sh = M652.hern(sk, 1.0, RE_GAL); bt, dt_, _ = member_cold(sk, sh, 1e11, 0.0, f, uS, N9)
        ev_t = drev_event_algebra(bt, dt_, 300.0)
        nb = {}
        for uu, lab_ in ((uS, "uS"), (0.80, "u08")):
            nb[lab_] = nbody_strip(uu, f, N9, "drev"); nb[lab_ + "_reloc"] = nbody_strip(uu, f, N9, "reloc")
            guard("nbody")
        bk = max(DG[f][v]["book_resid_maxabs_unfloored"] for v in UVARS)
        FM[f] = dict(event_cluster_median_member=ev_c, event_toy_secondary=ev_t, nbody=nb, eRASS1_bookkeeping_maxabs=bk,
                     eRASS1_floors={v: DG[f][v]["n_floor"] for v in UVARS})
        P(f"  (f) {f[:3]}: D-REV event (cluster-median member, r_J {ev_c['rJ']:.0f} kpc, {ev_c['frac_reverted']:.2f} reverted): dM {ev_c['dM_rel']:.1e} dP {ev_c['dP_rel']:.1e} "
          f"dD {ev_c['dD_rel']:.1e} dL {ev_c['dL_rel']:.1e}; toy secondary dP {ev_t['dP_rel']:.1e}; N-body u {uS:.3f}: {nb['uS']['n_events']} events, max event dP/P {nb['uS']['max_event_dP']:.1e}, "
          f"drift {nb['uS']['P_drift']:.1e}, mass drift {nb['uS']['M_drift']:.1e}; u 0.80: {nb['u08']['n_events']} events, {nb['u08']['max_event_dP']:.1e}, drift {nb['u08']['P_drift']:.1e}; "
          f"relocation contrast max event dP/P {nb['uS_reloc']['max_event_dP']:.2f} / {nb['u08_reloc']['max_event_dP']:.2f}; eRASS1 bookkeeping max |resid| {bk:.1e}")
    ev_all = [FM[f][k]["dP_rel"] for f in FEET for k in ("event_cluster_median_member", "event_toy_secondary")] + \
             [FM[f]["nbody"][lab_]["max_event_dP"] for f in FEET for lab_ in ("uS", "u08")]
    drift_ok = all(FM[f]["nbody"][lab_]["P_drift"] <= 1e-9 and FM[f]["nbody"][lab_]["M_drift"] <= 1e-12 for f in FEET for lab_ in ("uS", "u08"))
    book_ok = all(FM[f]["eRASS1_bookkeeping_maxabs"] <= 1e-9 for f in FEET)
    nev = all(FM[f]["nbody"][lab_]["n_events"] >= 1 for f in FEET for lab_ in ("uS", "u08"))
    CL["f"] = dict(final=("INCONSISTENT" if max(ev_all) > 0.01 else ("CONSISTENT" if (drift_ok and book_ok and nev) else "CONDITIONAL")),
                   max_event_dP=max(ev_all), drift_ok=drift_ok, book_ok=book_ok, events_present=nev)
    RES["momentum"] = FM
    P(f"== (f) momentum/mass: {CL['f']['final']} (max event dP/P {max(ev_all):.1e}; drift ok {drift_ok}; bookkeeping ok {book_ok}; events present {nev})")
    # ---- (g) Bullet
    PHI = J("CFG915_population_label_mobility", "cfg915_results.json")["phi_lin"]; BC = {}
    for f in FEET:
        b_ = bullet_sctu(f, N9); plH = PHI[FL[f]]["H"]; df = b_["dfine"]; phi = b_["phi_J"]
        cl = np.where(phi <= plH, "C", np.where(phi >= 0.9, "I", "U"))
        BC[f] = dict(rJ_720=b_["rJ_720"], rJ_min=float(np.min(b_["rJ"])), phi_720=float(phi[-1]), classes_present=sorted(set(cl.tolist())), phi_lin_H=plH,
                     d_cons_min=(float(df[np.argmax(phi <= plH)]) if (phi <= plH).any() else None),
                     d_inc_max=(float(df[np.where(phi >= 0.9)[0].max()]) if (phi >= 0.9).any() else None), main=b_["main"], sub=b_["sub"], phi_reloc_DREV=0.0)
        P(f"  (g) Bullet {f[:3]} (u = 1: native dust): sub King r_J(720) {b_['rJ_720']:.0f} kpc, min {BC[f]['rJ_min']:.1f}; phi_J classes {BC[f]['classes_present']}; "
          f"CONSISTENT for d_p >= {BC[f]['d_cons_min']}, INCONSISTENT for d_p <= {BC[f]['d_inc_max']} (phi_lin,H {plH:.4f}); sub native c {b_['sub']['c']:.1f} r_s {b_['sub']['rs']:.0f} kpc; "
          f"reported: under D-REV the stripped dust keeps the sub's velocity, phi_reloc = 0")
    sets = [set(BC[f]["classes_present"]) for f in FEET]
    CL["g"] = dict(final=("CONSISTENT" if all(s == {"C"} for s in sets) else ("INCONSISTENT" if all(s == {"I"} for s in sets) else "UNDERDETERMINED")))
    RES["bullet"] = BC
    P(f"== (g) Bullet: {CL['g']['final']}")
    # ---- (h) satellites
    N3 = load_953(); R953 = J("CFG953_source_changing_theory", "cfg953_results.json")["c"]; SA = {}
    for key, ref in R953["C"].items():
        foot, nm, rk = key.split("|"); Mb_, apc = [(m_, a_) for n_, m_, a_ in N3["HOSTS882"] if n_ == nm][0]
        tf = R953["c1"][key] - ref["ratio"]
        s1 = sat_u(N3, N959, Mb_, apc, float(rk), N3["A0"][foot], "u1"); s0 = sat_u(N3, N959, Mb_, apc, float(rk), N3["A0"][foot], "u0trunc")
        SA[key] = dict(u1=s1, u0trunc=s0, TF=tf, c1_u1=s1["ratio"] + tf, c1_u0=s0["ratio"] + tf, sctm_ratio=ref["ratio"])
    hov = all(SA[k]["c1_u1"] <= N3["EPS_B"][k.split("|")[0]] and SA[k]["c1_u0"] <= N3["EPS_B"][k.split("|")[0]] for k in SA)
    efe = all(abs(SA[k]["u1"]["efe_dex"]) <= N3["DELTA_C"] and abs(SA[k]["u0trunc"]["efe_dex"]) <= N3["DELTA_C"] for k in SA)
    CL["h"] = dict(final="PASS" if (hov and efe) else "FAIL", max_hover=max(max(v["c1_u1"], v["c1_u0"]) for v in SA.values()),
                   max_efe=max(max(abs(v["u1"]["efe_dex"]), abs(v["u0trunc"]["efe_dex"])) for v in SA.values()))
    RES["satellites"] = SA
    P(f"  (h) satellites: max Delta a/g_host (+ retardation) {CL['h']['max_hover']:.2e} (eps_B 0.344 / 0.317); max |EFE| {CL['h']['max_efe']:.2e} dex (delta_c 0.082); "
      f"u = 1 Jacobi cut at H3 50 kpc {SA['canonical|H3|50']['u1']['cut_kpc']:.2f} kpc, u = 0 truncated body {SA['canonical|H3|50']['u0trunc']['cut_kpc']:.2f} kpc (SCT-M body edge {SA['canonical|H3|50']['u0trunc']['edge_kpc']:.2f})")
    P(f"== (h) satellites: {CL['h']['final']}")
    # ---- classes
    a_mid, a_out, a_s, b_acc = CL["a-MID"]["final"], CL["a-OUTER"]["final"], CL["a-s"]["final"], CL["b-ACC"]["final"]
    if a_mid == a_out == a_s == "CONSISTENT" and b_acc != "INCONSISTENT":
        prof = "FIXED"
    elif "INCONSISTENT" in (a_mid, a_out):
        prof = "NOT FIXED"
    else:
        prof = "PARTIAL"
    items_fail = [k for k in ("a-MID", "a-OUTER", "a-s", "b-J", "f") if CL[k]["final"] == "INCONSISTENT"]
    if items_fail or CL["c1"]["final"] == "INCONSISTENT" or CL["g"]["final"] == "INCONSISTENT":
        over = "SCT-U CLUSTERS FAIL"
    elif all(CL[k]["final"] == "CONSISTENT" for k in ("a-MID", "a-OUTER", "a-s", "b-ACC", "b-J", "c1", "f", "g")):
        over = "SCT-U CLUSTERS OK"
    else:
        over = "SCT-U CLUSTERS CONDITIONAL"
    gal_ok = CL["d"]["final"] == "PASS" and CL["e"]["final"] == "CONSISTENT" and CL["h"]["final"] == "PASS"
    gal = ("CONDITIONAL (carried from CFG953: C-E, C-DF)" if gal_ok else "FAIL") + \
          (" + DWARF EXCESS WORSE than SCT-M" if CL["i"]["final"] == "WORSE" else "")
    RES["classes"] = CL; RES["cluster_profile_subclass"] = prof; RES["overall"] = over; RES["galaxy_scale"] = gal; RES["failing_items"] = items_fail
    P("\n== CLASSES: " + "; ".join(f"({k}) {v['final']}" for k, v in CL.items()))
    P(f"== CLUSTER PROFILE: {prof}")
    P(f"== OVERALL: {over}" + (f"  (INCONSISTENT items: {', '.join(items_fail)})" if items_fail else ""))
    P(f"== GALAXY SCALE: {gal}; (c2) UDG excess {CL['c2']['final']}")
    return RES


# ================================================================================================ dispatch
if STAGE == "COMPUTE":
    RESULT = stage_compute()
elif STAGE == "K":
    RESULT = stage_K()
elif STAGE == "MUTATE":
    RESULT = stage_mutate()
else:
    RESULT = stage_main()
P(f"\nelapsed {time.time() - T0:.0f} s; peak RSS {rss_gb():.3f} GB")
P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.")
finish_log()
if RESULT is not None:
    RESULT["runtime_s"] = time.time() - T0; RESULT["peak_rss_gb"] = rss_gb()
    with open(os.path.join(OUTDIR, f"cfg962_results{TAG}.json"), "w") as fh_:
        json.dump(jclean(RESULT), fh_, indent=1)
code = 0
if STAGE in ("MUTATE", "K"):
    code = 0 if all(v["ok"] for v in CHK.values()) else 1
sys.exit(code)
