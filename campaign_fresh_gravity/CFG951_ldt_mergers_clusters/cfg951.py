#!/usr/bin/env python3
"""CFG951 (criteria FROZEN_CRITERIA.md, a29366301): mergers and clusters under the labelled-domain theory (LDT).

LDT working statement (criteria section 1): per-label tether (CFG945 H1), label equilibrium C2 = every mass outside a label is a
Newtonian source of its law (M_tot = S nu(S)), L2 re-latch by medium tidal dominance (CFG945), static relaxation (CFG916 LR-c),
CFG726/CFG916 harness conventions.  Merge variants M1 (instant relabel at coalescence), M2 (blend over t_dyn; = M1 for static
cluster scoring), M3 (labels persist until L2 disruption).  Tests (a) merger memory vs eRASS1 / ACCEPT OUTER, (b) core A_MID under
reading T (implied) and U (CFG949 + labelled members), (c) Bullet, (d) continuity toy, (e) Coma UDG ceiling.

Stages (one process at a time, from this directory, OMP_NUM_THREADS=1 nice -n 10):
  CFG951_STAGE=COMPUTE python3 cfg951.py  -> cluster arrays in ../../../_external_data/cfg951_work (progress only: cfg951_COMPUTE.out)
  CFG951_STAGE=K       python3 cfg951.py  -> cfg951_K.out, cfg951_results_K.json
  CFG951_MUTATE=1      python3 cfg951.py  -> cfg951_MUTATE.out, cfg951_results_MUTATE.json
                       python3 cfg951.py  -> cfg951.out, cfg951_results.json
Amendment A1 (AMENDMENT_A1_post_hoc.md, 2026-10-21, after the first MAIN run): a reported (ungraded) toy with tau_1 from label 1's
isolated medium; the first MAIN run is kept as cfg951_RUN1_toyartefact.*.
Read-only inputs: cfg637_lib, CFG4_common, cfg652_model, cfg599_lib (imported); CFG726 / CFG916 / CFG945 / CFG947 / CFG949 code
(copied, or exec'd slices of CFG686 / CFG922 exactly as CFG949 did; CFG949's own script is never executed); result JSONs of CFG726,
687, 686, 916, 915, 945, 947, 948, 949; CFG687 per-cluster npz; CFG726 work arrays; the Coma UDG table.  Nothing downloaded.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, contextlib, resource, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import cumulative_trapezoid

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
W726 = os.path.join(EXT, "cfg726_work"); WORK = os.path.join(EXT, "cfg951_work"); os.makedirs(WORK, exist_ok=True)
STAGE = "MUTATE" if os.environ.get("CFG951_MUTATE", "") == "1" else os.environ.get("CFG951_STAGE", "MAIN").upper()
assert STAGE in ("COMPUTE", "K", "MUTATE", "MAIN")
NMAX = int(os.environ.get("CFG951_NMAX", "0"))                     # smoke tests only (outputs suffixed _SMOKE)
SMOKE = NMAX > 0
TAG = {"COMPUTE": "_COMPUTE", "K": "_K", "MUTATE": "_MUTATE", "MAIN": ""}[STAGE] + ("_SMOKE" if SMOKE else "")
WTAG = "_SMOKE" if SMOKE else ""
try:
    os.nice(10)
except OSError:
    pass
T0 = time.time(); LOG = []
RSS_LIMIT = 0.9e9


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def rss():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def vm_free_gb():
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
        pg = 16384
        for l in out.splitlines():
            if "page size of" in l:
                pg = int(l.split("page size of")[1].split()[0])
        val = {l.split(":")[0].strip(): int(l.split(":")[1].strip().rstrip(".")) for l in out.splitlines()[1:] if ":" in l}
        return (val.get("Pages free", 0) + val.get("Pages inactive", 0)) * pg / 1e9
    except Exception:
        return None


OUTDIR = WORK if SMOKE else HERE                                    # smoke-test outputs never land in the repository


def finish_log():
    open(os.path.join(OUTDIR, f"cfg951{TAG}.out"), "w").write("\n".join(LOG) + "\n")


def guard(where=""):
    r = rss()
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.3f} GB > 0.9 GB at '{where}' -> abort (exit 3)"); finish_log(); sys.exit(3)
    fg = vm_free_gb()
    if fg is not None and fg < 8.0:
        P(f"VM GUARD: free+inactive {fg:.1f} GB < 8 GB at '{where}' -> exit 75 (rerun later)"); finish_log(); sys.exit(75)
    return r


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


def rd(rel):
    return json.load(open(os.path.join(LANES, rel)))


fg0 = vm_free_gb()
P(f"CFG951 [{STAGE}{' SMOKE N=' + str(NMAX) if SMOKE else ''}]  criteria a29366301  free+inactive at start {fg0 if fg0 is None else round(fg0, 1)} GB")
if fg0 is not None and fg0 < 10.0:
    P("start guard: free+inactive < 10 GB -> exit 75"); finish_log(); sys.exit(75)

for d in ("CFG637_derived_reservoir", "CFG652_hot_group_discriminator", "CFG599_merger_stopwatch_v2", "CFG540_vizier2026_bfjr_mhongoose"):
    sys.path.insert(0, os.path.join(LANES, d))
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import cfg637_lib as L                                          # noqa: E402  (read-only)
    import CFG4_common as C4                                        # noqa: E402
    import cfg652_model as M652                                     # noqa: E402
    import cfg599_lib as P599                                       # noqa: E402
FEET = ("canonical", "alt")
FL = {"canonical": "can", "alt": "alt"}
assert abs(C4.A0["canonical"] - 9.3603e-11) < 1e-15 and abs(C4.A0["alt"] - 1.1312e-10) < 1e-15

# ================================================================================================ CFG726 harness (copied)


def nu_s(y):                                                         # CFG695: g_N = g^2/(g + a0)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


A0K = {f: C4.A0[f] * L.SI_TO_KPCGYR2 for f in FEET}                  # kpc / Gyr^2
A0SI = {f: C4.A0[f] for f in FEET}
RE_GAL = M652.RE_BCG                                                 # 15 kpc (inherited)
SUP_PER_COND = M652.COLD_PER_B / M652.F_COND_FLOOR                   # 53.64 x m for a condensed progenitor
RHALF = (1.0 + math.sqrt(2.0)) * RE_GAL / M652.HERN_RE              # Hernquist baryonic half-mass radius (kpc)
_RTA = {}


def rta_of(M_ta, z):
    k = (round(math.log10(M_ta), 4), round(z, 4))
    if k not in _RTA:
        _RTA[k] = L.r_ta_single(M_ta, 1.0 / (1.0 + z))[0]
    return _RTA[k]


def prog_halo(rg, Mshape, m, z, a0, nu):
    rta = rta_of(m / M652.F_COND_FLOOR / L.FB, z)
    mph, xe = L.phantom_trunc(rg / rta, m * Mshape, rta, a0, nu, SUP_PER_COND * m)
    return mph, rta, xe


def shell_frac(s, d, R):
    f = (R ** 2 - (d - s) ** 2) / (4.0 * np.maximum(d * s, 1e-300))
    f = np.clip(f, 0.0, 1.0)
    f = np.where(R >= s + d, 1.0, f)
    f = np.where(R <= np.abs(s - d), 0.0, f)
    return f


RCOARSE = np.geomspace(0.3, 3.0e4, 170)


def convolve_members(dk, Ncum, sk, Tcum, Rout_kpc):                 # CFG726 (verbatim)
    dN = np.diff(Ncum); dm = np.sqrt(dk[1:] * dk[:-1])
    dT = np.r_[Tcum[0], np.diff(Tcum)]; sm = np.r_[sk[0] * 0.5, np.sqrt(sk[1:] * sk[:-1])]
    Cc = np.zeros(len(RCOARSE))
    for j0 in range(0, len(RCOARSE), 34):
        Rj = RCOARSE[j0:j0 + 34]
        A = shell_frac(sm[None, :, None], dm[:, None, None], Rj[None, None, :])
        Cc[j0:j0 + 34] = np.einsum("d,s,dsr->r", dN, dT, A)
    Cc = np.maximum.accumulate(Cc)
    lo = np.log(np.maximum(Cc, 1e-300))
    out = np.exp(np.interp(np.log(Rout_kpc), np.log(RCOARSE), lo, left=-700.0))
    out[Rout_kpc > RCOARSE[-1]] = Cc[-1]
    return np.where(out < 1e-250, 0.0, out)


R_OBS = np.geomspace(0.5, 6e4, 900)
G_SI = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KG = MSUN / (3.0857e16) ** 2
RGRID = np.logspace(-3, np.log10(30), 3000); U_GRID = np.linspace(0, 1, 4001)
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:] * EDGES[:-1])
RK_GRID = RGRID * 1000.0
DK = np.geomspace(1.0, 3000.0, 140)
DM_ = np.sqrt(DK[1:] * DK[:-1])
SM_ = np.r_[R_OBS[0] * 0.5, np.sqrt(R_OBS[1:] * R_OBS[:-1])]


def sigma_proj(rhoL, r, R):
    umax = np.arccosh(r[-1] / R); u = U_GRID * umax; rr = R * np.cosh(u)
    rho_u = np.exp(np.interp(np.log(rr), np.log(r), np.log(np.maximum(rhoL, 1e-300))))
    return 2 * np.trapz(rho_u * rr * MPC, u)


def dsig_from_M(ML_msun):
    ML = ML_msun * MSUN; r = RGRID
    rhoL = np.gradient(ML, r * MPC) / (4 * np.pi * (r * MPC) ** 2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4 * np.pi * (r[r > R] * MPC) ** 2 * rhoL[r > R] * (1 - np.sqrt(1 - (R / r[r > R]) ** 2)), r[r > R] * MPC) for R in RC])
    return (M2 / (np.pi * (RC * MPC) ** 2) - Sig) / KG


def law_M(Mb_msun, foot, nu):
    gb = G_SI * Mb_msun * MSUN / (RGRID * MPC) ** 2
    return Mb_msun * nu(gb / A0SI[foot])


def erass_gas(i, d):
    R5, mgas = float(d["R500"][i]), float(d["mg"][i])
    r = RGRID; rc = 0.15 * R5; shape = (1 + (r / rc) ** 2) ** (-1.0); shape[r > 3.0] = 0
    dm = 4 * np.pi * (r * MPC) ** 2 * shape; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r * MPC))]
    return Mm * (mgas / np.interp(R5, r, Mm))


# ================================================================================================ CFG916 orbits / r_J (copied)


def rJ_from_X(X, s, mcum):
    q = np.maximum.accumulate(s ** 3 / np.maximum(mcum, 1e-300))
    X = np.asarray(X, float)
    out = np.exp(np.interp(np.log(np.maximum(X, 1e-300)), np.log(q), np.log(s)))
    out = np.where(X >= q[-1], np.inf, out)
    return np.where(X <= q[0], s[0], out)


def host_table(r, M, tracerM=None):
    GK = 4.30091e-6
    g = GK * M / r ** 2
    Phi = np.r_[0.0, np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(r))]
    gam = np.gradient(np.log(np.maximum(M, 1e-300)), np.log(r))
    tab = dict(r=r, lr=np.log(r), M=M, lM=np.log(np.maximum(M, 1e-300)), g=g, Phi=Phi, gam=gam)
    if tracerM is not None:
        n = np.maximum(np.gradient(tracerM, r), 0.0) / (4 * math.pi * r ** 2)
        f = n * g
        I = np.zeros_like(r); I[:-1] = np.cumsum((0.5 * (f[1:] + f[:-1]) * np.diff(r))[::-1])[::-1]
        tab["sig2"] = np.where(n > 0, I / np.maximum(n, 1e-300), 0.0)
    return tab


def rJ_at(tab, rr, s, mcum):
    lrr = np.log(np.asarray(rr, float))
    M = np.exp(np.interp(lrr, tab["lr"], tab["lM"]))
    den = 3.0 - np.interp(lrr, tab["lr"], tab["gam"])
    X = np.where(den > 0, np.asarray(rr, float) ** 3 / (np.maximum(den, 1e-300) * M), 1e300)
    return np.where(den > 0, rJ_from_X(X, s, mcum), np.inf)


HX, HW = np.polynomial.hermite.hermgauss(8)
_sel = HX > 0
LX, LW = np.polynomial.laguerre.laggauss(8)
NODE_XR = np.repeat(HX[_sel], 8); NODE_U = np.tile(LX, int(_sel.sum()))
NODE_W = np.outer(2 * HW[_sel] / math.sqrt(math.pi), LW).ravel()          # sums to 1


def pericentres(tab, d):
    ld = np.log(d)
    Phid = np.interp(ld, tab["lr"], tab["Phi"]); s2 = np.maximum(np.interp(ld, tab["lr"], tab["sig2"]), 0.0)
    vr = np.sqrt(2 * s2)[:, None] * NODE_XR[None, :]; vt = np.sqrt(2 * s2[:, None] * NODE_U[None, :])
    E = Phid[:, None] + 0.5 * (vr ** 2 + vt ** 2); Lsq = (d[:, None] * vt) ** 2
    F = lambda rr: 2 * (E - np.interp(np.log(rr), tab["lr"], tab["Phi"])) - Lsq / rr ** 2
    lo = np.full(vr.shape, tab["r"][0]); hi = np.broadcast_to(d[:, None], vr.shape).astype(float).copy()
    floor = F(lo) >= 0
    for _ in range(60):
        mid = np.sqrt(lo * hi); pos = F(mid) > 0
        hi = np.where(pos, mid, hi); lo = np.where(pos, lo, mid)
    rp = np.where(floor, tab["r"][0], hi)
    return np.minimum(rp, d[:, None]), vr, vt


def convolve_members_w(Ncum, Tcum, Rout_kpc, Wt):                   # CFG916 (copied; blocks built on the fly)
    dN = np.diff(Ncum); dT = np.r_[Tcum[0], np.diff(Tcum)]
    dNT = dN[:, None] * dT[None, :] * Wt
    Cc = np.zeros(len(RCOARSE))
    for j0 in range(0, len(RCOARSE), 34):
        A = shell_frac(SM_[None, :, None], DM_[:, None, None], RCOARSE[j0:j0 + 34][None, None, :])
        Cc[j0:j0 + 34] = np.einsum("ds,dsr->r", dNT, A)
    Cc = np.maximum.accumulate(Cc)
    lo = np.log(np.maximum(Cc, 1e-300))
    out = np.exp(np.interp(np.log(Rout_kpc), np.log(RCOARSE), lo, left=-700.0))
    out[Rout_kpc > RCOARSE[-1]] = Cc[-1]
    return np.where(out < 1e-250, 0.0, out)


_AMAT = None


def amat():
    """(len(DM_) * len(SM_), len(RCOARSE)) shell-overlap matrix: the CFG916 convolution as one matrix product (this lane)."""
    global _AMAT
    if _AMAT is None:
        _AMAT = np.empty((len(DM_) * len(SM_), len(RCOARSE)))
        for j0 in range(0, len(RCOARSE), 34):
            A = shell_frac(SM_[None, :, None], DM_[:, None, None], RCOARSE[j0:j0 + 34][None, None, :])
            _AMAT[:, j0:j0 + 34] = A.reshape(len(DM_) * len(SM_), -1)
    return _AMAT


def conv_fast(dNT, Rout_kpc=RK_GRID):
    """sum_d,s dNT[d, s] x shell overlap -> cluster-centric cumulative on Rout (CFG916's tail: running max, log interpolation)."""
    Cc = dNT.ravel() @ amat()
    Cc = np.maximum.accumulate(Cc)
    lo = np.log(np.maximum(Cc, 1e-300))
    out = np.exp(np.interp(np.log(Rout_kpc), np.log(RCOARSE), lo, left=-700.0))
    out[Rout_kpc > RCOARSE[-1]] = Cc[-1]
    return np.where(out < 1e-250, 0.0, out)


# ================================================================================================ LDT pieces (this lane)
SQ6 = math.sqrt(6.0) / 3.0


def tau_of(r, M, Gc=L.G):
    """|tau| = (sqrt6/3)|u' - u/r| of the radial field u = G M(<r)/r^2 of a cumulative medium mass M on grid r."""
    dM = np.gradient(M, r, axis=-1)
    return SQ6 * np.abs(Gc * (dM / r ** 2 - 3.0 * M / r ** 3))


def env_of(tau):
    """outer envelope: max of tau over s' >= s (non-increasing), so 'outermost s with tau >= thr' = 'largest s with env >= thr'."""
    return np.maximum.accumulate(tau[..., ::-1], axis=-1)[..., ::-1]


def rdom_from_env(r, env, thr):
    """largest r with env(r) >= thr (log interpolation); thr array; 0 if env[0] < thr; r[-1] if env[-1] >= thr."""
    thr = np.asarray(thr, float)
    k = np.searchsorted(-env, -thr, side="right")                      # number of nodes with env >= thr
    kk = np.clip(k, 1, len(r) - 1)
    e0, e1 = env[kk - 1], env[kk]
    l0, l1 = np.log(r[kk - 1]), np.log(r[kk])
    with np.errstate(divide="ignore", invalid="ignore"):
        fr = np.where(e0 > e1, (np.log(e0) - np.log(np.maximum(thr, 1e-300))) / (np.log(e0) - np.log(np.maximum(e1, 1e-300))), 1.0)
    out = np.exp(l0 + np.clip(fr, 0.0, 1.0) * (l1 - l0))
    out = np.where(k == 0, 0.0, out)
    return np.where(k >= len(r), r[-1], out)


def tau_at(r, tau, x):
    return np.exp(np.interp(np.log(x), np.log(r), np.log(np.maximum(tau, 1e-300))))


def wmedian(x, w):
    x = np.asarray(x, float).ravel(); w = np.asarray(w, float).ravel()
    ok = w > 0
    x, w = x[ok], w[ok]
    o = np.argsort(x); c = np.cumsum(w[o]) / w.sum()
    return float(x[o][np.searchsorted(c, 0.5)])


def cluster_ctx(Mg, fs, z, Nmem, foot):
    """members (CFG726 primary model) for one cluster and footing."""
    Mb = Mg * (1 + fs); Ms = fs * Mg; Mstar = float(Ms[-1])
    Ncum = np.interp(DK / 1000.0, RGRID, Mg) / Mg[-1]
    nmem = max(1, int(round(Nmem))); mi = Mstar / nmem
    shape = M652.hern(R_OBS, 1.0, RE_GAL)
    h, rta_i, xe = prog_halo(R_OBS, shape, mi, z, A0K[foot], nu_s)
    Mlaw = law_M(Mb, foot, nu_s)
    rho_gas = np.gradient(Mg, RK_GRID) / (4 * math.pi * RK_GRID ** 2)               # Msun / kpc^3
    Mg_edges = np.interp(DK / 1000.0, RGRID, Mg)
    return dict(Mg=Mg, Mb=Mb, Ms=Ms, Mstar=Mstar, fs=fs, z=z, Ncum=Ncum, dN=np.diff(Ncum), nmem=nmem, mi=mi, shape=shape, h=h,
                rta_i=rta_i, edge_kpc=(None if xe is None else xe * rta_i), Mlaw=Mlaw, T=Mlaw - Mb, foot=foot, mcum=mi * shape + h,
                env=env_of(tau_of(R_OBS, h)), rho_gas_d=np.exp(np.interp(np.log(DM_), np.log(RK_GRID), np.log(np.maximum(rho_gas, 1e-300)))),
                dMg_d=np.diff(Mg_edges))


def icm_halos(ctx):
    """ICM-sourced member halos (bracket): law phantom of the member's stars + the local gas monopole (4 pi/3) s^3 rho_gas(d),
    cut at the member's own supply edge and r_ta.  Returns (139 x 900) cumulative halos and their envelopes."""
    a0 = A0K[ctx["foot"]]; mi = ctx["mi"]; rta = ctx["rta_i"]
    H = np.empty((len(DM_), len(R_OBS)))
    for k, rho in enumerate(ctx["rho_gas_d"]):
        src = mi * ctx["shape"] + (4.0 * math.pi / 3.0) * R_OBS ** 3 * rho
        H[k], _ = L.phantom_trunc(R_OBS / rta, src, rta, a0, nu_s, SUP_PER_COND * mi)
    return H, env_of(tau_of(R_OBS, H))


def run_ldt(ctx, rule="L2", epoch="peri", coal=False, coupling="H1", halos2d=None, maxit=8, tol=1e-4, host0=None):
    """iterate the LDT cluster profile.  rule L2 (medium tidal dominance) | King (CFG916 r_J); epoch peri | present;
    coal: M1/M2 mask (members with r_dom <= r_half,b relabelled); coupling H1 (C2: host law of M_b + C) | OD (own-domain);
    halos2d: (H, env) ICM bracket.  host0: initial host total (default: the plain law)."""
    foot = ctx["foot"]; Mb, Mg = ctx["Mb"], ctx["Mg"]; nmem = ctx["nmem"]; dN = ctx["dN"]
    Mtot = (ctx["Mlaw"] if host0 is None else host0).copy()
    Mh = Mtot - Mb if host0 is None else None
    if halos2d is None:
        dT = np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :]
    else:
        H, Henv = halos2d; dT = np.c_[H[:, :1], np.diff(H, axis=1)]
    C = np.zeros_like(Mtot); hist = []; conv = np.inf; it = 0; rdom = None; Wt = None
    if Mh is None:
        Mh = Mtot - Mb
    for it in range(1, maxit + 1):
        tab = host_table(RK_GRID, Mtot, Mg)
        if epoch == "peri":
            rp = pericentres(tab, DM_)[0]; wn = NODE_W
        else:
            rp = DM_[:, None].copy(); wn = np.ones(1)
        if rule == "L2":
            th = tau_at(RK_GRID, tau_of(RK_GRID, np.maximum(Mh, 0.0)), rp)
            if halos2d is None:
                rdom = rdom_from_env(R_OBS, ctx["env"], th)
            else:
                rdom = np.vstack([rdom_from_env(R_OBS, Henv[k], th[k]) for k in range(len(DM_))])
            rdom = np.minimum(rdom, ctx["rta_i"])
        else:
            rdom = rJ_at(tab, rp, R_OBS, ctx["mcum"])
        keep = SM_[None, None, :] < rdom[:, :, None]
        if coal:
            keep = keep & (rdom >= RHALF)[:, :, None]
        Wt = np.einsum("w,dws->ds", wn, keep.astype(float))
        Cn = nmem * conv_fast(dN[:, None] * dT * Wt)
        if coupling == "H1":
            Mn = law_M(Mb + Cn, foot, nu_s); Mhn = Mn - Mb - Cn
        else:                                                        # X-OD: host law of host-domain baryons only
            pco = np.einsum("w,dw->d", wn, (rdom < RHALF).astype(float))
            Mstar_co = np.interp(RK_GRID, DM_, np.cumsum(ctx["dMg_d"] * pco)) * ctx["fs"]
            Mhd = Mg + Mstar_co
            Tod = law_M(Mhd, foot, nu_s) - Mhd
            Mn = Mb + Cn + Tod; Mhn = Tod
        ok = Mtot > 0
        conv = float(np.max(np.abs(Mn[ok] / Mtot[ok] - 1)))
        hist.append(conv)
        Mprev = Mtot
        Mtot, C, Mh = Mn, Cn, Mhn
        if conv <= tol and it >= 2:
            break
    wgt = dN[:, None] * (NODE_W[None, :] if epoch == "peri" else np.ones((1, 1)))
    rd_med = wmedian(np.minimum(rdom, 1e9), wgt)
    fco = float((wgt * (rdom < RHALF)).sum() / wgt.sum())
    i1 = int(np.argmin(np.abs(RK_GRID - 1000.0)))
    return dict(Mtot=Mtot, Mprev=Mprev, C=C, iters=it, conv=conv, hist=hist, rdom_med=rd_med, f_coal=fco,
                C_over_Mb_1Mpc=float(C[i1] / ctx["Mb"][i1]), C_tot=float(C[-1]))


def supply_tot(ctx):
    return float(M652.catchment(ctx["Mstar"], float(ctx["Mg"][-1]))[1])


def capped(ctx, Mtot):
    Mc = np.minimum(Mtot - ctx["Mb"], supply_tot(ctx))
    return ctx["Mb"] + Mc


# ================================================================================================ scoring (CFG726 / CFG916 copied)
PC7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
NE_ALL = len(PC7["mg"])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}


def erass_sel():
    return np.arange(NE_ALL) if not SMOKE else np.arange(min(NMAX, NE_ALL))


def score_TR(arrs_by_var):
    d = PC7; idx = erass_sel()
    D, E = d["D"][idx], d["E"][idx]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
    order = np.argsort(d["ra"][idx]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
    mg = d["mg"][idx]; q = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2)

    def A_of(sel, Pm):
        return {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}

    def jk(fun):
        full = fun(np.ones(n, bool)); reps = [fun(patch != p) for p in range(30)]
        return {k: (float(full[k]), float(np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2)))) for k in full}

    def slope(sel, arr):
        xs, ys = [], []
        for t in range(3):
            s = sel & (tid == t); j = BANDS["OUTER"]; v = (W[s][:, j] * arr[s][:, j]).sum() / W[s][:, j].sum()
            if v <= 0:
                return np.nan
            xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
        return np.polyfit(xs, ys, 1)[0]
    out = {}
    for v, Pm in arrs_by_var.items():
        A = jk(lambda s: A_of(s, Pm))
        AtO = [float((W[tid == t][:, 6:8] * D[tid == t][:, 6:8]).sum() / (W[tid == t][:, 6:8] * Pm[tid == t][:, 6:8]).sum()) for t in range(3)]
        out[v] = dict(A=A, Z_mid=(A["MID"][0] - 1) / A["MID"][1], Z_outer=(A["OUTER"][0] - 1) / A["OUTER"][1],
                      s=float(slope(np.ones(n, bool), Pm)), A_tercile_OUTER=AtO)
    return out


def accept_inputs():                                                 # CFG916 (copied)
    from scipy.interpolate import PchipInterpolator
    c = 2.998e8; MP = 1.6726e-27
    zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
    DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DMb = np.sqrt(7.942 ** 3 / (0.295 * DHb))
    pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54 / 0.70
    DM = lambda z: pch(np.minimum(np.asarray(z, float), 2.33)) * RD
    prof = {}
    for l in open(os.path.join(EXT, "cfg686_inputs", "accept", "all_profiles.dat")):
        if l.startswith("#"):
            continue
        pp = l.split()
        try:
            prof.setdefault(pp[0], []).append([float(x) for x in pp[1:14]])
        except ValueError:
            pass
    C686 = rd("CFG686_cluster_shear_vs_law/cfg686_results.json")["clusters"]
    p = json.load(open(os.path.join(W726, "lambda.json")))["p"]
    res = []
    for cl in C686:
        Pp = np.array(prof[cl["key"]]); Pp = Pp[np.argsort(Pp[:, 0])]; rin, rout, ne = Pp[:, 0], Pp[:, 1], Pp[:, 2]
        ok_ = ne > 0; rin, rout, ne = rin[ok_], rout[ok_], ne[ok_]
        zl = cl["z"]; zz = np.linspace(0, zl, 400); Ez = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7); DA_acc = np.trapz(1 / Ez, zz) * c / (70e3 / MPC) / MPC / (1 + zl)
        q = (float(DM(zl)) / (1 + zl)) / DA_acc; rin, rout, ne = rin * q, rout * q, ne * q ** -0.5
        rm = 0.5 * (rin + rout); rho = 1.17 * MP * ne * 1e6
        half = rm >= np.exp(0.5 * (np.log(rm[0]) + np.log(rm[-1]))); b0 = -np.polyfit(np.log(rm[half]), np.log(rho[half]), 1)[0]
        flag = not (b0 >= 1.5); b = 2.0 if flag else b0
        r = RGRID; rho_g = np.interp(r, rm, rho, left=rho[0], right=np.nan)
        out_ = r > rm[-1]; rho_g[out_] = rho[-1] * (r[out_] / rm[-1]) ** (-b); rho_g[r > 3.0] = 0.0
        Mg = np.r_[0, np.cumsum(0.5 * (4 * np.pi * (r[1:] * MPC) ** 2 * rho_g[1:] + 4 * np.pi * (r[:-1] * MPC) ** 2 * rho_g[:-1]) * np.diff(r) * MPC)] / MSUN
        mg1 = float(np.interp(1.0, RGRID, Mg)); Nm = 10 ** (p[0] * math.log10(mg1) + p[1])
        res.append(dict(Mg=Mg, z=zl, Nm=Nm, name=cl["name"]))
    return res, C686


def score_TA(arrs_by_var, C686):                                     # CFG916 (copied)
    D_ = np.nan_to_num(np.array([x["dsig"] for x in C686])); E_ = np.array([x["err"] for x in C686])
    W_ = np.where(np.isfinite(E_) & (E_ > 0), 1 / E_ ** 2, 0)

    def bandA(Pm, sel):
        o_ = {}
        for b, j in BANDS.items():
            num = (W_[sel][:, j] * D_[sel][:, j]).sum(); den = (W_[sel][:, j] * Pm[sel][:, j]).sum(); o_[b] = num / den if den != 0 else np.nan
        return o_
    out = {}
    for v, Pm in arrs_by_var.items():
        A = bandA(Pm, np.arange(len(C686))); rb = np.random.default_rng(1)
        boots = [bandA(Pm, rb.integers(0, len(C686), len(C686))) for _ in range(1000)]
        sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}
        out[v] = dict(A={b: [float(A[b]), sig[b]] for b in BANDS}, Z_mid=float((A["MID"] - 1) / sig["MID"]), Z_outer=float((A["OUTER"] - 1) / sig["OUTER"]))
    return out


# ================================================================================================ CFG949 B0 machinery (exec recipe + copied R930)
_B0 = {}


def b0_machinery():
    """CFG949's exec recipe for the CFG686 / CFG922 engines (no KiDS sources) and its R930 native-collapse code (copied verbatim);
    CFG949's own script is never executed (it opens its own output files at import)."""
    if _B0:
        return _B0
    SRC686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py"); TXT686 = open(SRC686).read()
    NS = {"__file__": SRC686, "__name__": "cfg686"}
    _argv = sys.argv; sys.argv = [SRC686, "UNUSED"]
    os.environ.pop("MUTATE", None)
    with contextlib.redirect_stdout(io.StringIO()) as _buf:
        exec(TXT686.split("# ---- sources ----")[0], NS)
        NS["EDGES"] = np.logspace(np.log10(0.15), np.log10(3.0), 9); NS["RC"] = np.sqrt(NS["EDGES"][1:] * NS["EDGES"][:-1]); NS["M_BIAS"] = -0.01
        exec(TXT686.split("# ---- the law's prediction from ACCEPT gas ----")[1].split("# ---- measure ----")[0], NS)
    sys.argv = _argv
    G, MS, MP_, KGc, DMf, RCc, RG = NS["G"], NS["MSUN"], NS["MPC"], NS["KG_PER_MSUN_PC2"], NS["DM"], NS["RC"], NS["RGRID"]
    assert np.array_equal(RG, RGRID)
    SRC922 = os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922.py"); TXT922 = open(SRC922).read()
    E9 = dict(np=np, math=math, G=G, MSUN=MS, MPC=MP_, KG=KGc, DM=DMf, RC=RCc, RGRID=RG, CLIGHT=NS["c"], NS=NS, TRAPZ=np.trapz)
    exec("R = RGRID; RM = R * MPC" + TXT922.split("R = RGRID; RM = R * MPC")[1].split("A_BCG = 0.015")[0], E9)
    exec(TXT922.split("# ---- band amplitudes ----")[1].split("# ---- inputs ----")[0], E9)
    R = RG; RM = R * MP_; NR = len(R); RKPC = R * 1e3; PRE = E9["PRE"]

    def dsig_newton(M3, chunk=40):                                   # CFG949 (copied verbatim)
        M3 = np.atleast_2d(M3)
        if M3.shape[0] > chunk:
            return np.vstack([dsig_newton(M3[i:i + chunk], chunk) for i in range(0, M3.shape[0], chunk)])
        rho = np.gradient(M3, RM, axis=1) / (4 * np.pi * RM ** 2)
        lrho = np.log(np.where(rho > 0, rho, 1e-300)); out = np.empty((M3.shape[0], len(RCc)))
        for j, (u, rr, i0, f, sel, fac) in enumerate(PRE):
            Sig = 2 * np.trapz(np.exp((1 - f) * lrho[:, i0] + f * lrho[:, i0 + 1]) * rr * MP_, u, axis=1)
            M2 = np.array([np.interp(RCc[j], R, m) for m in M3]) + np.trapz(rho[:, sel] * fac, R[sel] * MP_, axis=1)
            out[:, j] = (M2 / (np.pi * (RCc[j] * MP_) ** 2) - Sig) / KGc
        return out
    # ---- R930 (CFG949 copy of CFG930, verbatim)
    GMPC = 4.30091727e-9
    SUP = 5.364; FBN = 1.0 / (1.0 + SUP)
    DELTA_C, FPROG, MED_HN = 1.686, 0.01, 0.6744897501960817
    TS = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_scorer_tables_cmb.npz"))
    TI = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_ics_tables_cmb.npz"))
    DTA = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta_cmb.json")))
    h_, Om, Or, OL, NSI = float(TS["h"]), float(TS["Om"]), float(TS["Or"]), float(TS["OL"]), float(TI["ns"])
    KH, PK = np.asarray(TS["kh"], float), np.asarray(TS["Plin_z0"], float)
    LNA_T, LND_T = np.asarray(TS["lna"], float), np.asarray(TS["lnD"], float)
    ZTA, DTAV = np.array(DTA["z"], float), np.array(DTA["D"], float)
    RHOC_H = 3 * 100.0 ** 2 / (8 * math.pi * GMPC); RHOM0_H = Om * RHOC_H; RHOM0_KPC = Om * RHOC_H * h_ ** 2 / 1e9
    GAM = Om * h_
    KK = np.logspace(-4, 5, 9001); LKK = np.log(KK); KMAX = float(KH[-1])
    PT = np.exp(np.interp(LKK, np.log(KH), np.log(PK)))
    _ext = KK > KMAX
    PT[_ext] = PK[-1] * (KK[_ext] / KMAX) ** (NSI - 4.0) * (np.log1p(2.34 * KK[_ext] / GAM) / math.log1p(2.34 * KMAX / GAM)) ** 2

    def W_th(x):
        x = np.asarray(x, float); out = np.empty_like(x); s = x < 1e-3
        out[s] = 1.0 - x[s] ** 2 / 10.0; xx = x[~s]; out[~s] = 3.0 * (np.sin(xx) - xx * np.cos(xx)) / xx ** 3
        return out

    def sig2_R(R_):
        return float(np.trapz(KK ** 3 * PT * W_th(KK * R_) ** 2, LKK) / (2 * math.pi ** 2))
    LMG = np.arange(0.0, 17.0001, 0.01)
    SIG2G = np.array([sig2_R((3 * 10 ** lm * h_ / (4 * math.pi * RHOM0_H)) ** (1.0 / 3.0)) for lm in LMG])

    def sig2M(M): return float(np.exp(np.interp(math.log10(M), LMG, np.log(SIG2G))))
    LND0 = float(np.interp(0.0, LNA_T, LND_T)); LNDN = LND_T - LND0

    def D_of_z(z): return float(math.exp(np.interp(-math.log1p(z), LNA_T, LNDN)))

    def z_of_D(D): return float(math.exp(-np.interp(math.log(D), LNDN, LNA_T)) - 1.0)

    def m_(x):
        x = np.asarray(x, float)
        return np.where(x < 1e-3, x * x / 2 - 2 * x ** 3 / 3 + 3 * x ** 4 / 4, np.log1p(x) - x / (1 + x))

    def conc_from(rhs):
        return math.exp(brentq(lambda lc: math.log(float(m_(math.exp(lc)))) - 3 * lc - math.log(rhs), math.log(1e-4), math.log(1e8), xtol=1e-13))
    _lna = np.linspace(-20.0, 0.0, 20001); _a = np.exp(_lna)
    _H = 100 * h_ * np.sqrt(Om / _a ** 3 + Or / _a ** 4 + OL)
    _t = cumulative_trapezoid(1.0 / _H, _lna, initial=0.0) + 0.5 / (100 * h_ * math.sqrt(Or)) * _a[0] ** 2

    def dta_of(z): return float(np.interp(math.log1p(z), np.log1p(ZTA), DTAV))

    def dvir_of(z):
        tz = float(np.interp(-math.log1p(z), _lna, _t)); a_ta = float(np.exp(np.interp(0.5 * tz, _t, _lna))); zt = 1.0 / a_ta - 1.0
        return 8.0 * dta_of(zt) * ((1.0 + zt) / (1.0 + z)) ** 3

    def fret_of(lM):
        if lM < 12.5: f = 0.10
        elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
        else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
        return min(f, 1.0)

    def mta_fixed(Mb):
        f = 0.10; lMb = math.log10(Mb)
        for _ in range(200):
            lMta = lMb - math.log10(f * FBN); fn = fret_of(lMta)
            if abs(fn - f) < 1e-12: break
            f = 0.5 * (f + fn)
        return f, 10 ** lMta

    def zcoll930(M, zi):
        ds2 = sig2M(FPROG * M) - sig2M(M)
        if ds2 <= 0: return zi
        Dc = 1.0 / (1.0 / D_of_z(zi) + MED_HN * math.sqrt(ds2) / DELTA_C)
        return max(z_of_D(Dc), zi)

    def prof930(Mta, zi, C, bnd):
        zc = zcoll930(Mta, zi); Db = dta_of(zi) if bnd == "rta" else dvir_of(zi)
        rb = (3 * Mta / (4 * math.pi * Db * RHOM0_KPC * (1 + zi) ** 3)) ** (1.0 / 3.0)
        c = conc_from(Db * (1 + zi) ** 3 / (3 * C * (1 + zc) ** 3))
        return c, rb / c, rb, zc
    MG7, R5007, ZC7, RA7 = (np.asarray(PC7[k], float) for k in ("mg", "R500", "z", "ra"))
    D7 = np.nan_to_num(np.asarray(PC7["D"], float)); E7 = np.asarray(PC7["E"], float)
    idx = erass_sel()
    STE = E9["Stack"](D7[idx], E7[idx], RA7[idx], "jk")
    W7 = np.where(E7 > 0, 1 / E7 ** 2, 0)[idx]; NE = len(idx); MGs = MG7[idx]
    _q = np.quantile(MGs, [0, 1 / 3, 2 / 3, 1]); TID = np.clip(np.digitize(MGs, _q[1:-1]), 0, 2)

    def s_model(arr):                                                # CFG687 T2 (CFG949 copy)
        xs, ys = [], []
        for t in range(3):
            s = TID == t; j = BANDS["OUTER"]; v = (W7[s][:, j] * arr[s][:, j]).sum() / W7[s][:, j].sum()
            if v <= 0: return np.nan
            xs.append(np.log10(np.median(MGs[s]))); ys.append(np.log10(v))
        return float(np.polyfit(xs, ys, 1)[0])
    GAS = E9["gas_beta"](MG7[idx], R5007[idx])                        # kg
    Mc = np.empty((NE, NR)); meta = []
    for k, i in enumerate(idx):                                      # B0 primary: S-cen x R930 C3000 r_ta at z_i (CFG949 build_cold)
        Mret = 1.20 * float(GAS[k, -1] / MS); f, Mta = mta_fixed(Mret)
        c, rs, rb, zc = prof930(Mta, float(ZC7[i]), 3000.0, "rta")
        Mc[k] = (1 - FBN) * Mta * m_(np.minimum(RKPC, rb) / rs) / float(m_(c)) * MS
        meta.append((Mta, f, c, rs, rb, zc))
    _B0.update(dsig_newton=dsig_newton, STE=STE, s_model=s_model, GAS=GAS, MB=GAS * 1.20, Mc=Mc, meta=np.array(meta), MS=MS,
               selftest=_buf.getvalue().strip().splitlines(), idx=idx)
    return _B0


# ================================================================================================ (c) Bullet (record inputs)
R_CORE = 200.0


def bullet(foot):
    f = FL[foot]
    with contextlib.redirect_stdout(io.StringIO()):
        main = P599.Progenitor599(1.5e15, f, cloud=False)
        sub = P599.Progenitor599(1.5e14, f, cloud=True)
    ok = main.r > 0
    r = main.r[ok]; s = sub.r[ok]
    tab = host_table(r, main.Mtot[ok])
    dgrid = np.geomspace(5.0, 720.0, 240)
    rJ_present = float(rJ_at(tab, np.array([720.0]), s, sub.Mtot[ok])[0])
    rJ_grid = np.minimum(rJ_at(tab, dgrid, s, sub.Mtot[ok]), 1e12)
    # L2: tau from each progenitor's own medium (Mph, P599 units kpc / Msun; G cancels in the comparison)
    tau_main = tau_of(r, main.Mph[ok], Gc=1.0); tau_sub = tau_of(s, sub.Mph[ok], Gc=1.0)
    env_sub = env_of(tau_sub)
    dfine = np.geomspace(1.0, 720.0, 4000)
    rdom = rdom_from_env(s, env_sub, tau_at(r, tau_main, dfine))
    Mph_s = sub.Mph[ok]; Mb_s = sub.Mbar[ok]
    core = float(np.interp(R_CORE, s, Mph_s))
    rhalf_b = float(np.interp(0.5 * Mb_s[-1], Mb_s, s))
    Ms_s = sub.Ms[ok]; rhalf_star = float(np.interp(0.5 * Ms_s[-1], Ms_s, s))          # POST-HOC diagnostic only
    keep = np.interp(np.minimum(rdom, R_CORE), s, Mph_s, left=0.0)
    phi3 = 1.0 - keep / core
    phi1 = np.where(rdom <= rhalf_b, 1.0, phi3)
    return dict(rJ_present=rJ_present, rJ_grid=rJ_grid, dgrid=dgrid, dfine=dfine, rdom=rdom, phi_M3=phi3, phi_M1=phi1,
                rhalf_b=rhalf_b, rhalf_star_posthoc=rhalf_star,
                d_trigger_star_posthoc=(float(dfine[np.where(rdom <= rhalf_star)[0].max()]) if (rdom <= rhalf_star).any() else None),
                rdom_720=float(rdom[-1]), phi_M3_720=float(phi3[-1]), phi_M1_720=float(phi1[-1]),
                Mph_core=core, rt_sub=float(sub.rt))


def first_below(d, y, thr):
    """largest d at which y crosses thr from below (y >= thr at smaller d): returns the d where y(d) = thr (log interp), or None."""
    above = y >= thr
    if not above.any():
        return None
    if above.all():
        return float(d[-1])
    j = np.where(above)[0].max()
    if j == len(d) - 1:
        return float(d[-1])
    y0, y1 = y[j], y[j + 1]
    if y0 == y1:
        return float(d[j])
    t = (thr - y0) / (y1 - y0)
    return float(math.exp(math.log(d[j]) + t * (math.log(d[j + 1]) - math.log(d[j]))))


# ================================================================================================ (d) continuity toy
RAP = (20.0, 50.0, 100.0, 200.0)


def toy(q, foot, n_d=1521, tau_mode="C2"):
    """tau_mode 'C2' (frozen: tau_1 from label 1's iterated C2 monopole medium) | 'iso' (AMENDMENT A1, POST HOC, reported only:
    tau_1 from label 1's isolated medium, the convention of CFG945 and of this lane's Bullet; removes the shell-smearing artefact)."""
    a0 = A0K[foot]; Gk = L.G
    sk = R_OBS; shape = M652.hern(sk, 1.0, RE_GAL); m1 = 1e11; m2 = q * m1
    h1, _, _ = prog_halo(sk, shape, m1, 0.0, a0, nu_s); h2, rta2, _ = prog_halo(sk, shape, m2, 0.0, a0, nu_s)
    Mb1, Mb2 = m1 * shape, m2 * shape
    env2 = env_of(tau_of(sk, h2))
    dMb2 = np.diff(np.r_[0.0, Mb2]); dh2 = np.diff(np.r_[0.0, h2])

    def encl(dM, d, R):
        return float(np.sum(dM * shell_frac(SM_, d, R)))

    def C2_of(rdom):
        return np.where(sk < rdom, h2, np.interp(rdom, sk, h2, left=0.0))

    def tot(d, dC2, R):
        S = float(np.interp(R, sk, Mb1)) + encl(dMb2 + dC2, d, R)
        return S * float(nu_s(Gk * S / R ** 2 / a0)), S

    def gp(d, R):
        S = float(np.interp(R, sk, Mb1)) + encl(dMb2, d, R)
        return S * float(nu_s(Gk * S / R ** 2 / a0))

    def tau1(d, dC2):
        if d <= 0:
            return np.inf
        rr = d * np.array([1 - 1e-3, 1.0, 1 + 1e-3])
        M1m = np.array([tot(d, dC2, x)[0] - tot(d, dC2, x)[1] for x in rr])           # label-1 medium about centre 1
        dM = (M1m[2] - M1m[0]) / (rr[2] - rr[0])
        return SQ6 * abs(Gk * (dM / d ** 2 - 3.0 * M1m[1] / d ** 3))

    tau1_iso = tau_of(sk, h1)

    def rdom_at(d):
        if d <= 0:
            return 0.0
        if tau_mode == "iso":
            return float(min(rdom_from_env(sk, env2, tau_at(sk, tau1_iso, np.array([d])))[0], rta2))
        rdm = float(rta2)
        for _ in range(8):
            dC2 = np.diff(np.r_[0.0, C2_of(rdm)])
            new = float(min(rdom_from_env(sk, env2, np.array([tau1(d, dC2)]))[0], rta2))
            if abs(new - rdm) <= 1e-6 * max(rdm, 1e-9):
                rdm = new; break
            rdm = new
        return rdm
    ds = np.r_[np.exp(np.linspace(math.log(1000.0), math.log(0.5), n_d)), 0.0]
    rdom = np.array([rdom_at(d) for d in ds])
    Mlaw1 = Mb1 + h1; Mlaw2 = Mb2 + h2
    v = np.array([math.sqrt(Gk * (float(np.interp(d, sk, Mlaw1)) + float(np.interp(d, sk, Mlaw2))) / d) if d > 0 else np.nan for d in ds])
    t = np.zeros(len(ds))
    for k in range(1, len(ds)):
        vm = v[k - 1] if not np.isfinite(v[k]) else 0.5 * (v[k - 1] + v[k])
        t[k] = t[k - 1] + (ds[k - 1] - ds[k]) / vm
    Mrem = law_toy = (Mb1 + Mb2) * nu_s(Gk * (Mb1 + Mb2) / sk ** 2 / a0)
    vrem = lambda R: math.sqrt(Gk * float(np.interp(R, sk, Mrem)) / R)
    tdyn = {R: R / vrem(R) for R in RAP}
    tblend = RHALF / vrem(RHALF)
    # trigger (M1/M2): first d (descending) with rdom <= r_half,b
    ktr = int(np.argmax(rdom <= RHALF)) if (rdom <= RHALF).any() else len(ds) - 1
    out = {}
    for var in ("M3", "M1", "M2"):
        # state per step: (d, label-2 cumulative medium); label-induced change per step at FIXED configuration
        dLab = {R: [] for R in RAP}; tt = []; Eabs = {R: 0.0 for R in RAP}; jmax_inst = {R: 0.0 for R in RAP}; Eser = {R: [] for R in RAP}
        C2prev = C2_of(rdom[0]); f_prev = 1.0
        C2trig = C2_of(rdom[ktr])
        times = list(t)
        steps = [(k, ds[k], None) for k in range(1, len(ds))]
        if var == "M2":                                              # extend at d = 0 until the blend completes
            nb = 200; t_end = t[ktr] + tblend
            if t_end > t[-1]:
                extra = np.linspace(t[-1], t_end, nb + 1)[1:]
                steps += [(len(ds) - 1 + j + 1, 0.0, extra[j]) for j in range(nb)]
        for (k, d, tex) in steps:
            tk = t[k] if tex is None else tex
            if var == "M3" or k < ktr:
                C2new = C2_of(rdom[min(k, len(ds) - 1)]) if tex is None else C2_of(0.0)
            elif var == "M1":
                C2new = np.zeros_like(sk)
            else:                                                    # M2: frozen trigger content, fraction falls over t_blend
                fr = max(0.0, 1.0 - (tk - t[ktr]) / tblend); C2new = fr * C2trig
            for R in RAP:
                a = tot(d, np.diff(np.r_[0.0, C2new]), R)[0]; b = tot(d, np.diff(np.r_[0.0, C2prev]), R)[0]
                dLab[R].append((a - b) / b if b > 0 else 0.0)
                jmax_inst[R] = max(jmax_inst[R], abs(a - b) / b if b > 0 else 0.0)
                g = gp(d, R); Eabs[R] = max(Eabs[R], abs(a / g - 1) if g > 0 else 0.0); Eser[R].append(a / g - 1 if g > 0 else 0.0)
            tt.append(tk); C2prev = C2new
        tt = np.array(tt); J = {}; JF = {}
        for R in RAP:
            # FROZEN metric: change of E_v = M_v/M_GP - 1 over any window of one remnant t_dyn(R)
            Es = np.array(Eser[R]); best = 0.0
            for i in range(len(tt)):
                j = int(np.searchsorted(tt, tt[i] + tdyn[R], side="right"))
                best = max(best, float(np.max(np.abs(Es[i:j] - Es[i]))))
            J[R] = best
            # POST-HOC diagnostic (2026-10-20, no class weight): label-induced change at FIXED configuration, accumulated per window
            cum = np.r_[0.0, np.cumsum(dLab[R])]; tcum = np.r_[tt[0] - 1e-12, tt]; bf = 0.0
            for i in range(len(tcum)):
                j = int(np.searchsorted(tcum, tcum[i] + tdyn[R], side="right")) - 1
                bf = max(bf, float(np.max(np.abs(cum[i:j + 1] - cum[i]))))
            JF[R] = bf
        out[var] = dict(J=J, J_max=max(J.values()), jump_inst_max=max(jmax_inst.values()), E_abs_max=max(Eabs.values()),
                        J_by_R={str(R): J[R] for R in RAP}, J_fixedconf_posthoc_max=max(JF.values()),
                        J_fixedconf_posthoc_by_R={str(R): JF[R] for R in RAP})
    lr = np.log(np.maximum(rdom[:-1], 1e-3))
    return dict(variants=out, d_trigger=float(ds[ktr]), rdom_at_trigger=float(rdom[ktr]), tdyn_Gyr={str(R): tdyn[R] for R in RAP},
                rdom_max_over_d_below_300=float(np.max(rdom[:-1][ds[:-1] < 300.0] / ds[:-1][ds[:-1] < 300.0])),
                n_rdom_capped=int(np.sum(rdom[:-1] >= rta2 * (1 - 1e-9))), max_dln_rdom_step_d_gt_1kpc=float(np.max(np.abs(np.diff(lr))[ds[1:-1] > 1.0])),
                t_blend_Gyr=tblend, rdom_samples={f"{d:.0f}": float(np.interp(math.log(d), np.log(ds[:-1][::-1]), rdom[:-1][::-1])) for d in (500, 200, 100, 50, 20)})


# ================================================================================================ (e) Coma UDGs
KPC_SI = 3.0857e19                                                   # CFG948's constant
BETA = dict(kT_keV=8.6, rc_kpc=276.0, beta=0.71, mu=0.6, m_p=1.67262e-27, keV=1.602176634e-16)       # CFG948 / L23
CBETA = 3 * BETA["beta"] * BETA["kT_keV"] * BETA["keV"] / (BETA["mu"] * BETA["m_p"])
RCB = BETA["rc_kpc"] * KPC_SI


def g_host_coma(D_kpc):
    r = D_kpc * KPC_SI; return CBETA * r / (r * r + RCB * RCB)


def rho_host_coma(D_kpc):
    r = D_kpc * KPC_SI; return CBETA * (r * r + 3 * RCB * RCB) / (4 * math.pi * G_SI * (r * r + RCB * RCB) ** 2)


def tau_host_coma(D_kpc):
    r = D_kpc * KPC_SI; return SQ6 * 2 * CBETA * r * r / (r * r + RCB * RCB) ** 2


def nu_e(y):
    return 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))


def plummer_M(M, a, r):
    return M * r ** 3 / (r * r + a * a) ** 1.5


def udg_rows():
    path = os.path.join(REPO, "real_research", "data", "freundlich2022_coma_udgs.tsv")
    rows = [l.rstrip("\n").split("\t") for l in open(path) if l.strip() and not l.startswith("#")]
    hd = {h: i for i, h in enumerate(rows[0])}
    return {r[hd["name"]]: dict(L=float(r[hd["L_1e8"]]) * 1e8, Re=float(r[hd["Re_kpc"]]), ML=float(r[hd["ML"]]),
                                dproj=float(r[hd["d_kpc"]]), dmean=float(r[hd["dmean_kpc"]])) for r in rows[1:]}


def udg_one(u, foot, D):
    a0 = A0SI[foot]; M = u["L"] * u["ML"] * MSUN; a = u["Re"] * KPC_SI; r12 = 4.0 / 3.0 * a
    gN = G_SI * plummer_M(M, a, r12) / r12 ** 2
    law = lambda g: g * nu_e(g / a0)
    gloc = 4.0 * math.pi / 3.0 * G_SI * rho_host_coma(D) * r12
    dE = math.log(law(gN + gloc) / law(gN))
    EN = -math.log(nu_e(gN / a0))
    # L2 domain of the UDG medium (nu_e law of a Plummer M, a) vs the beta-model total-field tidal tensor (upper bound)
    us = lambda x: law(G_SI * plummer_M(M, a, x) / x ** 2) - G_SI * plummer_M(M, a, x) / x ** 2
    th = tau_host_coma(D)
    xs = np.geomspace(0.01 * a, 1000 * a, 4001)
    tm = np.array([SQ6 * abs((us(x * (1 + 1e-5)) - us(x * (1 - 1e-5))) / (2e-5 * x) - us(x) / x) for x in xs])
    rdom = float(rdom_from_env(xs, env_of(tm), np.array([th]))[0])
    rh_b = a / math.sqrt(2 ** (2.0 / 3.0) - 1.0)
    u_full = us(r12)
    u_tr = law(gN) - gN if rdom >= r12 else G_SI * (us(rdom) * rdom ** 2 / G_SI) / r12 ** 2
    E_part = math.log((gN + u_tr) / (gN + u_full))
    # global phantom (M1-inf): QUMOND 1-D EFE with the host's baryonic field from the simple-law inversion of the total
    gt = g_host_coma(D); gbh = gt * gt / (gt + a0)
    efe = math.log((law(gbh + gN) - law(gbh)) / law(gN))
    return dict(dE=dE, EN=EN, rdom_kpc=rdom / KPC_SI, r12_kpc=r12 / KPC_SI, rhalf_b_kpc=rh_b / KPC_SI, E_partial=E_part, efe=efe,
                gN=gN, gloc=gloc, Mloc_over_Mb12=gloc / gN)


# ================================================================================================ CFG945 L2 (K4) and CFG947 T-X (MU-GP), copied
G945, PC945, MSUN847, KPC847 = 6.67430e-11, 3.0856775814913673e16, 1.989e30, 3.0857e19
HOST938 = 6e10
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]
RHOST = (50.0, 100.0, 250.0)


def law_g945(gN, a0):
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def plummer_g945(M, a, x):
    return G945 * M * x / (x * x + a * a) ** 1.5


def h1_l2_radius_945(Mb_sun, a_pc, rk, a0):                         # CFG945 (copied)
    Mh = HOST938 * MSUN847; rh = rk * KPC847
    M = Mb_sun * MSUN847; a = a_pc * PC945
    us_of = lambda x: law_g945(plummer_g945(M, a, x), a0) - plummer_g945(M, a, x)
    uhost = lambda R: law_g945(G945 * Mh / R ** 2, a0) - G945 * Mh / R ** 2

    def tmag(f, x, h=1e-5):
        return math.sqrt(6) / 3 * abs((f(x * (1 + h)) - f(x * (1 - h))) / (2 * h * x) - f(x) / x)
    tau_h = tmag(uhost, rh)
    xg = np.logspace(math.log10(a), math.log10(100 * a), 801); tg = np.array([tmag(us_of, x) for x in xg])
    above = np.where(tg >= tau_h)[0]
    if len(above) == 0:
        return a
    if above[-1] == len(xg) - 1:
        return 100 * a
    j = above[-1]
    return brentq(lambda x: tmag(us_of, x) - tau_h, xg[j], xg[j + 1])


def l2_grid_lane(Mb_sun, a_pc, rk, a0, npts=40001):
    """this lane's grid L2 (tau_of + env_of + rdom_from_env on cumulative medium masses), capped to [a, 100a] as CFG945."""
    Mh = HOST938 * MSUN847; rh = rk * KPC847; M = Mb_sun * MSUN847; a = a_pc * PC945
    xs = np.geomspace(0.5 * a, 200 * a, npts)
    gs = plummer_g945(M, a, xs); Ms = (law_g945(gs, a0) - gs) * xs ** 2 / G945
    rr = np.geomspace(0.5 * rh, 2.0 * rh, 2001); gh = G945 * Mh / rr ** 2; Mhm = (law_g945(gh, a0) - gh) * rr ** 2 / G945
    th = tau_at(rr, tau_of(rr, Mhm, Gc=G945), np.array([rh]))
    rd_ = float(rdom_from_env(xs, env_of(tau_of(xs, Ms, Gc=G945)), th)[0])
    return min(max(rd_, a), 100 * a)


def law_simple947(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def law_mono947(gN, a0):
    gN = np.asarray(gN, float)
    return gN * C4.nu_mono(gN / a0)


KERN947 = {"simple": law_simple947, "mono": law_mono947}


def efe_global_dex(Mb_sun, a_pc, rkpc, a0, kern):                    # CFG947 (copied)
    law = KERN947[kern]
    gbh = C4.G_SI * HOST938 * MSUN847 / (rkpc * KPC847) ** 2
    gbs = C4.G_SI * (Mb_sun * MSUN847) * (a_pc * C4.PC) / ((a_pc * C4.PC) ** 2 + (a_pc * C4.PC) ** 2) ** 1.5
    return math.log10(float((law(gbh + gbs, a0) - law(gbh, a0)) / law(gbs, a0)))


# ================================================================================================ COMPUTE stage
VARS = [("M3", "L2", "peri", False, "H1", False), ("M1", "L2", "peri", True, "H1", False),
        ("M3_present", "L2", "present", False, "H1", False), ("M1_present", "L2", "present", True, "H1", False),
        ("M3_King", "King", "peri", False, "H1", False), ("M1_King", "King", "peri", True, "H1", False),
        ("M3_ICM", "L2", "peri", False, "H1", True), ("M1_ICM", "L2", "peri", True, "H1", True),
        ("M3_OD", "L2", "peri", False, "OD", False), ("M1_OD", "L2", "peri", True, "OD", False)]


def compute_cluster(Mg, z, Nm, foot, b0Mc=None):
    ctx = cluster_ctx(Mg, 0.20, z, Nm, foot)
    arr = {}; dg = {}
    arr["law"] = dsig_from_M(ctx["Mlaw"])
    C1 = ctx["nmem"] * convolve_members(DK, ctx["Ncum"], R_OBS, ctx["h"], RK_GRID)       # CFG726 verbatim (whole halos)
    arr["hmm"] = dsig_from_M(ctx["Mb"] + np.maximum(C1, ctx["T"]))                         # MU-NM shared target = H-MM
    arr["nm_H1"] = dsig_from_M(law_M(ctx["Mb"] + C1, foot, nu_s))                            # MU-NM under C2
    icm = None
    for (name, rule, ep, coal, cpl, use_icm) in VARS:
        if use_icm and icm is None:
            icm = icm_halos(ctx)
        o = run_ldt(ctx, rule, ep, coal, cpl, icm if use_icm else None)
        arr[name] = dsig_from_M(o["Mtot"])
        arr[name + "_prev"] = dsig_from_M(o["Mprev"])                                     # frozen non-convergence rule
        dg[name] = [o["iters"], o["conv"], o["rdom_med"], o["f_coal"], o["C_over_Mb_1Mpc"], o["C_tot"] / ctx["Mstar"]]
        if name in ("M3", "M1"):
            arr[name + "_cap"] = dsig_from_M(capped(ctx, o["Mtot"]))
    arr["law_cap"] = dsig_from_M(capped(ctx, ctx["Mlaw"]))
    # MU-0 control: zero halos through the same runner -> the plain law
    z0 = dict(ctx); z0["h"] = 0.0 * ctx["h"]; z0["env"] = env_of(tau_of(R_OBS, 1e-300 + 0.0 * ctx["h"]))
    o0 = run_ldt(z0, "L2", "peri", False, "H1", None, maxit=2)
    arr["mu0"] = dsig_from_M(o0["Mtot"])
    # K5 (ii): CFG916's King pericentre median r_J in the plain-law host (iteration 0)
    tab = host_table(RK_GRID, ctx["Mlaw"], Mg); rp = pericentres(tab, DM_)[0]
    rJp = rJ_at(tab, rp, R_OBS, ctx["mcum"])
    dg["K5_rJp_med"] = wmedian(np.minimum(rJp, 1e9), ctx["dN"][:, None] * NODE_W[None, :])
    dg["N"] = ctx["nmem"]; dg["edge_kpc"] = ctx["edge_kpc"]
    # reading U: untethered host (CFG949 B0 cold matter) + labelled members truncated at King r_J at pericentre
    if b0Mc is not None:
        MU = ctx["Mb"] + b0Mc
        tabU = host_table(RK_GRID, MU, Mg); rpU = pericentres(tabU, DM_)[0]
        rJU = rJ_at(tabU, rpU, R_OBS, ctx["mcum"])
        WU = np.einsum("w,dws->ds", NODE_W, (SM_[None, None, :] < rJU[:, :, None]).astype(float))
        CU = ctx["nmem"] * conv_fast(ctx["dN"][:, None] * np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :] * WU)
        fU = max(0.0, 1.0 - CU[-1] / b0Mc[-1]); fF = max(0.0, 1.0 - C1[-1] / b0Mc[-1])
        dg["U"] = [float(CU[-1] / b0Mc[-1]), float(C1[-1] / b0Mc[-1]), wmedian(np.minimum(rJU, 1e9), ctx["dN"][:, None] * NODE_W[None, :])]
        return arr, dg, dict(UM=ctx["Mb"] + fU * b0Mc + CU, UF=ctx["Mb"] + fF * b0Mc + C1)
    return arr, dg, None


def stage_compute():
    d = PC7; idx = erass_sel()
    lamj = json.load(open(os.path.join(W726, "lambda.json"))); Nm = np.array(lamj["Nmem"])
    B = b0_machinery(); b0Mc_msun = B["Mc"] / B["MS"]
    P(f"  B0 machinery ready ({time.time() - T0:.0f} s); RSS {rss() / 1e9:.2f} GB")
    # K-W: the matrix convolution equals CFG916's convolve_members_w (first cluster, canonical, random weights)
    ctx = cluster_ctx(erass_gas(int(idx[0]), d), 0.20, float(d["z"][idx[0]]), float(Nm[idx[0]]), "canonical")
    rng = np.random.default_rng(951); Wr = rng.random((len(DM_), len(R_OBS)))
    a = ctx["nmem"] * convolve_members_w(ctx["Ncum"], ctx["h"], RK_GRID, Wr)
    b = ctx["nmem"] * conv_fast(ctx["dN"][:, None] * np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :] * Wr)
    kw = float(np.max(np.abs(a - b) / np.maximum(a, 1e-300) * (a > 1e-200)))
    c1 = ctx["nmem"] * convolve_members(DK, ctx["Ncum"], R_OBS, ctx["h"], RK_GRID)
    c2 = ctx["nmem"] * conv_fast(ctx["dN"][:, None] * np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :] * np.ones((len(DM_), len(R_OBS))))
    kw1 = float(np.max(np.abs(c1 - c2) / np.maximum(c1, 1e-300) * (c1 > 1e-200)))
    P(f"  K-W matrix convolution vs CFG916 convolve_members_w (random weights): max rel {kw:.1e}; vs CFG726 convolve_members (weight 1): {kw1:.1e}")
    guard("K-W")
    for foot in FEET:
        res = {}; dgs = []; UM = []; UF = []
        for k, i in enumerate(idx):
            arr, dg, U = compute_cluster(erass_gas(int(i), d), float(d["z"][i]), float(Nm[i]), foot, b0Mc_msun[k])
            for v, x in arr.items():
                res.setdefault(v, np.zeros((len(idx), 8)))[k] = x
            dgs.append(dg); UM.append(U["UM"]); UF.append(U["UF"])
            if (k + 1) % 40 == 0 or k == len(idx) - 1:
                its = [x["M3"][0] for x in dgs]
                P(f"  eRASS1 {foot} {k + 1}/{len(idx)} ({time.time() - T0:.0f} s; RSS {rss() / 1e9:.2f} GB; M3 iterations max {max(its)})")
                guard(f"eRASS1 {foot} {k + 1}")
        np.savez(os.path.join(WORK, f"erass_{foot}{WTAG}.npz"), **{k: v for k, v in res.items()})
        json.dump(jclean(dgs), open(os.path.join(WORK, f"erass_{foot}_diag{WTAG}.json"), "w"))
        Bd = B["dsig_newton"]; ms = B["MS"]
        np.savez(os.path.join(WORK, f"U_{foot}{WTAG}.npz"), UM=Bd(np.array(UM) * ms), UF=Bd(np.array(UF) * ms))
        del UM, UF
        acc, C686 = accept_inputs(); resA = {}; dgA = []
        for j, a_ in enumerate(acc):
            arr, dg, _ = compute_cluster(a_["Mg"], a_["z"], a_["Nm"], foot)
            for v, x in arr.items():
                resA.setdefault(v, np.zeros((len(acc), 8)))[j] = x
            dgA.append(dg)
        np.savez(os.path.join(WORK, f"accept_{foot}{WTAG}.npz"), **resA)
        json.dump(jclean(dgA), open(os.path.join(WORK, f"accept_{foot}_diag{WTAG}.json"), "w"))
        P(f"  ACCEPT {foot} done ({time.time() - T0:.0f} s)")
        guard(f"ACCEPT {foot}")
    json.dump(dict(KW=kw, KW1=kw1, n=len(idx), elapsed=time.time() - T0, peak_rss_gb=rss() / 1e9),
              open(os.path.join(WORK, f"compute_meta{WTAG}.json"), "w"))


def load_work():
    W = {}
    for foot in FEET:
        W[("E", foot)] = dict(np.load(os.path.join(WORK, f"erass_{foot}{WTAG}.npz")))
        W[("A", foot)] = dict(np.load(os.path.join(WORK, f"accept_{foot}{WTAG}.npz")))
        W[("Ed", foot)] = json.load(open(os.path.join(WORK, f"erass_{foot}_diag{WTAG}.json")))
        W[("Ad", foot)] = json.load(open(os.path.join(WORK, f"accept_{foot}_diag{WTAG}.json")))
        W[("U", foot)] = dict(np.load(os.path.join(WORK, f"U_{foot}{WTAG}.npz")))
    W["meta"] = json.load(open(os.path.join(WORK, f"compute_meta{WTAG}.json")))
    return W


# ================================================================================================ K stage
CHK = {}


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    return bool(ok)


def stage_K():
    RES = {}
    W = load_work(); acc, C686 = accept_inputs(); idx = erass_sel()
    R726 = rd("CFG726_merger_memory/cfg726_results.json"); R687 = rd("CFG687_erass1_shear_stack/cfg687_results.json")
    # ---- K1 (i): stored CFG726 arrays scored
    ER = list(np.load(os.path.join(W726, "erass.npy"), allow_pickle=True)); AC = list(np.load(os.path.join(W726, "accept.npy"), allow_pickle=True))
    dmax = 0.0; dmax2 = 0.0; k1 = {}
    for foot in FEET:
        Ph = np.array([ER[i][f"hmm|s|{foot}|primary"] for i in idx]); tr = score_TR({"h": Ph})["h"]
        PhA = np.array([o[f"hmm|s|{foot}|primary"] for o in AC]); ta = score_TA({"h": PhA}, C686)["h"]
        ref = R726["T_R"][f"s|{foot}|primary"]; refA = R726["T_A"][f"s|{foot}|primary"]
        if not SMOKE:
            for b in ("MID", "OUTER"):
                dmax = max(dmax, abs(tr["A"][b][0] - ref["A"][b][0]), abs(tr["A"][b][1] - ref["A"][b][1]),
                           abs(ta["A"][b][0] - refA["A"][b][0]), abs(ta["A"][b][1] - refA["A"][b][1]))
            dmax = max(dmax, abs(tr["Z_outer"] - ref["Z_outer"]), abs(tr["Z_mid"] - ref["Z_mid"]), abs(ta["Z_outer"] - refA["Z_outer"]))
        # (ii) recomputed H-MM arrays vs stored
        dmax2 = max(dmax2, float(np.max(np.abs(W[("E", foot)]["hmm"] / Ph - 1))), float(np.max(np.abs(W[("A", foot)]["hmm"] / PhA - 1))))
        k1[foot] = dict(TR=tr, TA=ta)
    check("K1(i) CFG726 H-MM stored arrays scored = cfg726_results.json T_R/T_A primary (nu_s, both footings)", dmax <= 1e-12,
          f"max |diff| {dmax:.1e}; eRASS1 OUTER can {k1['canonical']['TR']['A']['OUTER'][0]:.4f}±{k1['canonical']['TR']['A']['OUTER'][1]:.4f} "
          f"(Z {k1['canonical']['TR']['Z_outer']:+.2f}), alt {k1['alt']['TR']['A']['OUTER'][0]:.4f} (Z {k1['alt']['TR']['Z_outer']:+.2f}); "
          f"ACCEPT OUTER {k1['canonical']['TA']['A']['OUTER'][0]:.4f} / {k1['alt']['TA']['A']['OUTER'][0]:.4f} (Z {k1['canonical']['TA']['Z_outer']:+.2f} / {k1['alt']['TA']['Z_outer']:+.2f})")
    check("K1(ii) H-MM recomputed with the copied cluster code = stored arrays (<= 1e-10 rel)", dmax2 <= 1e-10, f"max rel {dmax2:.1e}")
    RES["K1"] = dict(scored=k1, maxdiff=dmax, recompute_maxrel=dmax2)
    # ---- K2
    PL = np.asarray(PC7["PL"], float)[idx]; a2 = score_TR({"pl": PL})["pl"]; ref2 = R687["A"]["canonical|b0.67|rc0.15|f0.20"]
    d2 = 0.0 if SMOKE else max(abs(a2["A"][b][0] - ref2[b][0]) for b in ("MID", "OUTER"))
    d2 = max(d2, 0.0 if SMOKE else max(abs(a2["A"][b][1] - ref2[b][1]) for b in ("MID", "OUTER")))
    dd = PC7; PLa = np.array([dsig_from_M(law_M(erass_gas(int(i), dd) * 1.2, "alt", C4.nu_mono)) for i in idx])
    a2a = score_TR({"pl": PLa})["pl"]; ref2a = R687["A"]["alt|b0.67|rc0.15|f0.20"]
    d2a = 0.0 if SMOKE else max(max(abs(a2a["A"][b][0] - ref2a[b][0]), abs(a2a["A"][b][1] - ref2a[b][1])) for b in ("MID", "OUTER"))
    check("K2(i) CFG687 stored PL (nu_mono canonical) -> A = cfg687_results.json (<= 1e-9); alt law recomputed (<= 1e-6)",
          d2 <= 1e-9 and d2a <= 1e-6, f"canonical MID {a2['A']['MID'][0]:.4f}±{a2['A']['MID'][1]:.4f} OUTER {a2['A']['OUTER'][0]:.4f}±{a2['A']['OUTER'][1]:.4f} "
          f"(diff {d2:.1e}); alt MID {a2a['A']['MID'][0]:.4f} OUTER {a2a['A']['OUTER'][0]:.4f} (diff {d2a:.1e})")
    d2s = 0.0; amid = {}
    for foot in FEET:
        Pls = np.array([ER[i][f"law|s|{foot}"] for i in idx])
        d2s = max(d2s, float(np.max(np.abs(W[("E", foot)]["law"] / Pls - 1))))
        amid[foot] = score_TR({"l": W[("E", foot)]["law"]})["l"]
    refm = {f: R726["T_R"][f"s|{f}|primary"]["A_law"]["MID"][0] for f in FEET}
    dm = 0.0 if SMOKE else max(abs(amid[f]["A"]["MID"][0] - refm[f]) for f in FEET)
    check("K2(ii) nu_s law arrays = CFG726 stored law arrays (<= 1e-10); nu_s A_MID = 1.9068 / 1.7510 (<= 1e-4)", d2s <= 1e-10 and dm <= 1e-4,
          f"max rel {d2s:.1e}; A_MID {amid['canonical']['A']['MID'][0]:.4f} / {amid['alt']['A']['MID'][0]:.4f}; OUTER "
          f"{amid['canonical']['A']['OUTER'][0]:.4f} / {amid['alt']['A']['OUTER'][0]:.4f}")
    RES["K2"] = dict(PL=a2, PL_alt=a2a, nu_s_law=amid, maxdiff=[d2, d2a, d2s, dm])
    guard("K2")
    # ---- K3 CFG949 B0 primary corner
    B = b0_machinery(); Pb = B["dsig_newton"](B["MB"]); Pc = B["dsig_newton"](B["Mc"]); bd = B["STE"].band(Pb + Pc); s0 = B["s_model"](Pb + Pc)
    R949 = rd("CFG949_clusters_untethered/cfg949_results.json")["main"]["B0_primary"]
    d3 = 0.0 if SMOKE else max(max(abs(bd[b][0] - R949["A"][b][0]), abs(bd[b][1] - R949["A"][b][1])) for b in ("MID", "OUTER"))
    d3 = max(d3, 0.0 if SMOKE else abs(s0 - R949["s"]))
    check("K3 CFG949 B0 primary corner recomputed (copied R930 + CFG949's exec recipe) = cfg949_results.json (<= 1e-9)", d3 <= 1e-9,
          f"A_MID {bd['MID'][0]:.4f}±{bd['MID'][1]:.4f}, A_OUTER {bd['OUTER'][0]:.4f}±{bd['OUTER'][1]:.4f}, s {s0:.4f} (diff {d3:.1e}); "
          f"CFG686 self-test {B['selftest'][-1] if B['selftest'] else 'n/a'}")
    RES["K3"] = dict(A=bd, s=s0, maxdiff=d3)
    guard("K3")
    # ---- K4 CFG945 L2 radii
    S945 = rd("CFG945_gated_tether_satellite_hover/cfg945_results.json")["H1"]["b"]
    d4 = 0.0; d4c = 0.0; d4lo = 0.0; rows4 = {}
    for foot in FEET:
        for nm, Mb_, apc in HOSTS882:
            for rk in RHOST:
                ref = S945[f"{foot}|{nm}|{rk:.0f}"]["r_dom_pc"]
                rc_ = h1_l2_radius_945(Mb_, apc, rk, A0SI[foot]) / PC945
                rl = l2_grid_lane(Mb_, apc, rk, A0SI[foot]) / PC945
                rlo = l2_grid_lane(Mb_, apc, rk, A0SI[foot], npts=int(math.log(400.0) / math.log(R_OBS[1] / R_OBS[0])) + 1) / PC945
                d4c = max(d4c, abs(rc_ / ref - 1)); d4 = max(d4, abs(rl / ref - 1)); d4lo = max(d4lo, abs(rlo / ref - 1))
                rows4[f"{foot}|{nm}|{rk:.0f}"] = dict(ref=ref, copy=rc_, lane=rl, lane_cluster_res=rlo)
    check("K4 this lane's grid L2 radius = CFG945's 18 stored r_dom (<= 1e-6 rel)", d4 <= 1e-6,
          f"lane grid max rel {d4:.1e} (CFG945 code copy {d4c:.1e}); at the cluster member-grid resolution (reported, no weight) {d4lo:.1e}")
    RES["K4"] = dict(rows=rows4, maxrel_lane=d4, maxrel_copy=d4c, maxrel_cluster_res=d4lo)
    # ---- K5 CFG916 Bullet r_J and eRASS1 King median
    C916 = rd("CFG916_lock_and_release/cfg916_cache.json")
    d5 = 0.0; bl = {}
    for foot in FEET:
        b_ = bullet(foot); ref = C916["misc"]["B"][FL[foot]]
        d5 = max(d5, abs(b_["rJ_present"] / ref["rJ_present"] - 1), float(np.max(np.abs(b_["rJ_grid"] / np.array(ref["rJ_grid"]) - 1))))
        bl[foot] = b_["rJ_present"]
    medK = {f: float(np.median([x["K5_rJp_med"] for x in W[("Ed", f)]])) for f in FEET}
    refK = {f: C916["M"]["eRASS1"]["summary"][FL[f]]["rJp_med_kpc"] for f in FEET}
    d5b = 0.0 if SMOKE else max(abs(medK[f] / refK[f] - 1) for f in FEET)
    check("K5 CFG916 Bullet sub King r_J (720 kpc + grid, <= 1e-9) and eRASS1 King pericentre median r_J (<= 1e-6)", d5 <= 1e-9 and d5b <= 1e-6,
          f"r_J(720) {bl['canonical']:.2f} / {bl['alt']:.2f} kpc (diff {d5:.1e}); eRASS1 median {medK['canonical']:.3f} / {medK['alt']:.3f} kpc (diff {d5b:.1e})")
    RES["K5"] = dict(rJ_present=bl, eRASS1_rJp_med=medK, maxdiff=[d5, d5b])
    # ---- K6 CFG948
    R948 = rd("CFG948_nocapture_vs_udgs/cfg948_results.json")
    d6 = 0.0; z6 = {}
    for foot in FEET:
        pr = R948["byfoot"][foot]["primary"]
        z = (pr["mean_Eobs"] - pr["E_ceil"]) / math.sqrt(pr["se_obs"] ** 2 + pr["sys_up"]["total"] ** 2)
        d6 = max(d6, abs(z - pr["z_up"])); z6[foot] = z
    gh = g_host_coma(1000.0)
    check("K6 CFG948 z_up from stored components (<= 1e-9); beta-model g_host(1 Mpc) = 8.806e-11 (<= 1e-3 rel)",
          d6 <= 1e-9 and abs(gh / 8.806e-11 - 1) <= 1e-3, f"z_up {z6['canonical']:.4f} / {z6['alt']:.4f} (diff {d6:.1e}); g_host(1 Mpc) {gh:.4e}")
    RES["K6"] = dict(z_up=z6, g_host_1Mpc=gh)
    RES["K_W"] = dict(maxrel_vs_CFG916=W["meta"]["KW"], maxrel_vs_CFG726=W["meta"]["KW1"])
    check("K-W (implementation) matrix convolution = CFG916 convolve_members_w and CFG726 convolve_members (<= 1e-10)",
          W["meta"]["KW"] <= 1e-10 and W["meta"]["KW1"] <= 1e-10, f"{W['meta']['KW']:.1e} / {W['meta']['KW1']:.1e}")
    RES["checks"] = CHK; RES["K_all"] = all(v["ok"] for v in CHK.values())
    P(f"\nK: {sum(v['ok'] for v in CHK.values())}/{len(CHK)} pass")
    return RES


# ================================================================================================ MUTATE stage
def stage_mutate():
    RES = {}; W = load_work(); acc, C686 = accept_inputs(); idx = erass_sel()
    R726 = rd("CFG726_merger_memory/cfg726_results.json")
    # MU-NM
    nm = {}; dA = 0.0; bite_s = True; bite_h1 = True
    for foot in FEET:
        tr = score_TR({"hmm": W[("E", foot)]["hmm"], "nm_H1": W[("E", foot)]["nm_H1"]})
        ta = score_TA({"hmm": W[("A", foot)]["hmm"], "nm_H1": W[("A", foot)]["nm_H1"]}, C686)
        ref = R726["T_R"][f"s|{foot}|primary"]; refA = R726["T_A"][f"s|{foot}|primary"]
        if not SMOKE:
            dA = max(dA, max(abs(tr["hmm"]["A"][b][0] - ref["A"][b][0]) for b in ("MID", "OUTER")),
                     max(abs(ta["hmm"]["A"][b][0] - refA["A"][b][0]) for b in ("MID", "OUTER")))
        bite_s &= tr["hmm"]["Z_outer"] <= -2 and ta["hmm"]["Z_outer"] <= -2
        bite_h1 &= tr["nm_H1"]["Z_outer"] <= -2 and ta["nm_H1"]["Z_outer"] <= -2
        nm[foot] = dict(TR=tr, TA=ta)
        P(f"  MU-NM {foot}: shared target (= H-MM) eRASS1 OUTER {tr['hmm']['A']['OUTER'][0]:.3f}±{tr['hmm']['A']['OUTER'][1]:.3f} (Z {tr['hmm']['Z_outer']:+.2f}), "
          f"ACCEPT {ta['hmm']['A']['OUTER'][0]:.3f} (Z {ta['hmm']['Z_outer']:+.2f}); C2 never-merge eRASS1 OUTER {tr['nm_H1']['A']['OUTER'][0]:.3f}±{tr['nm_H1']['A']['OUTER'][1]:.3f} "
          f"(Z {tr['nm_H1']['Z_outer']:+.2f}), MID {tr['nm_H1']['A']['MID'][0]:.3f}; ACCEPT OUTER {ta['nm_H1']['A']['OUTER'][0]:.3f} (Z {ta['nm_H1']['Z_outer']:+.2f})")
    ok_nm = dA <= 1e-10 and bite_s and bite_h1
    check("MU-NM labels never merge: shared target reproduces CFG726 (<= 1e-10) and fails OUTER; C2 never-merge also fails OUTER (both samples, both footings)",
          ok_nm, f"max |dA| vs CFG726 {dA:.1e}; shared-target bites {bite_s}; C2 bites {bite_h1}")
    RES["MU_NM"] = nm
    # MU-GP
    R947 = rd("CFG947_option3_nonlocal_parent/cfg947_results.json")["T-X"]
    tx = {f"{f}|{nm_}|{rk:.0f}|{kz}": efe_global_dex(Mb_, apc, rk, A0SI[f], kz) for f in FEET for nm_, Mb_, apc in HOSTS882 for rk in RHOST for kz in KERN947}
    dgp = max(abs(tx[k] - R947[k]) for k in R947); present = max(abs(v) for v in tx.values()) > math.log10(1.01)
    dlaw = max(float(np.max(np.abs(W[("E", f)]["mu0"] / W[("E", f)]["law"] - 1))) for f in FEET)
    ok_gp = dgp <= 1e-12 and present and len(tx) == len(R947) == 36
    check("MU-GP global phantom: CFG947 T-X reproduced (36 values, <= 1e-12) with an EFE present; cluster global phantom = plain law",
          ok_gp and dlaw <= 1e-12, f"max |diff| {dgp:.1e}; EFE {min(tx.values()):.3f}..{max(tx.values()):.3f} dex; cluster: zero-label runner vs law {dlaw:.1e}")
    RES["MU_GP"] = dict(TX=tx, maxdiff=dgp, efe_present=present)
    check("MU-0 control: C = 0 through the LDT runner gives the plain law exactly (<= 1e-12, eRASS1 + ACCEPT, both footings)",
          max(dlaw, max(float(np.max(np.abs(W[("A", f)]["mu0"] / W[("A", f)]["law"] - 1))) for f in FEET)) <= 1e-12, f"max rel {dlaw:.1e}")
    RES["checks"] = CHK
    return RES


# ================================================================================================ MAIN stage
def cls_a(trs, tas):
    """class (a) per footing dicts: tr/ta score dicts per footing."""
    per = {}
    for f in FEET:
        ze, za = trs[f]["Z_outer"], tas[f]["Z_outer"]
        if abs(ze) < 2 and abs(za) < 2:
            per[f] = "CONSISTENT"
        elif ze <= -2 or za <= -2 or ze >= 2:
            per[f] = "INCONSISTENT"
        else:
            per[f] = "CONDITIONAL"
    v = set(per.values())
    return (per["canonical"] if len(v) == 1 and per["canonical"] in ("CONSISTENT", "INCONSISTENT") else "CONDITIONAL"), per


def cls_b(trs):
    per = {f: ("CONSISTENT" if abs(trs[f]["Z_mid"]) < 2 else "INCONSISTENT") for f in FEET}
    v = set(per.values())
    return (per["canonical"] if len(v) == 1 else "CONDITIONAL"), per


def stage_main():
    RES = {"lane": "CFG951", "criteria": "a29366301", "post_hoc": True,
           "settings": dict(kappa="1/2 FITTED", footings=A0SI, kernel="nu_s", r_half_b_kpc=RHALF)}
    W = load_work(); acc, C686 = accept_inputs(); idx = erass_sel()
    VN = ["law", "hmm", "nm_H1"] + [v[0] for v in VARS] + ["M3_cap", "M1_cap", "law_cap"]
    TR = {f: score_TR({v: W[("E", f)][v] for v in VN}) for f in FEET}
    TA = {f: score_TA({v: W[("A", f)][v] for v in VN}, C686) for f in FEET}
    RES["T_R"] = TR; RES["T_A"] = TA
    P("\n== (a)/(b) clusters: A = obs / model (eRASS1 30-patch jackknife; ACCEPT bootstrap 1000 seed 1); nu_s")
    for v in VN:
        for f in FEET:
            t, a = TR[f][v], TA[f][v]
            P(f"  {v:11s} {f[:3]}: eRASS1 MID {t['A']['MID'][0]:.3f}±{t['A']['MID'][1]:.3f} (Z {t['Z_mid']:+.2f}) OUTER {t['A']['OUTER'][0]:.3f}±{t['A']['OUTER'][1]:.3f} "
              f"(Z {t['Z_outer']:+.2f}) s {t['s']:.3f} | ACCEPT MID {a['A']['MID'][0]:.3f}±{a['A']['MID'][1]:.3f} (Z {a['Z_mid']:+.2f}) OUTER "
              f"{a['A']['OUTER'][0]:.3f}±{a['A']['OUTER'][1]:.3f} (Z {a['Z_outer']:+.2f})")
    # diagnostics
    DG = {}
    for f in FEET:
        dd = W[("Ed", f)]
        DG[f] = {v[0]: dict(iters_max=int(max(x[v[0]][0] for x in dd)), conv_max=float(max(x[v[0]][1] for x in dd)),
                            nonconv=int(sum(1 for x in dd if x[v[0]][1] > 1e-4)), rdom_med_kpc=float(np.median([x[v[0]][2] for x in dd])),
                            f_coal_med=float(np.median([x[v[0]][3] for x in dd])), C_over_Mb_1Mpc_med=float(np.median([x[v[0]][4] for x in dd])),
                            C_over_Mstar_med=float(np.median([x[v[0]][5] for x in dd]))) for v in VARS}
        DG[f]["U"] = dict(CU_over_Mc_med=float(np.median([x["U"][0] for x in dd])), Cfull_over_Mc_med=float(np.median([x["U"][1] for x in dd])),
                          rJ_U_med_kpc=float(np.median([x["U"][2] for x in dd])))
    RES["diagnostics"] = DG
    P("\n  diagnostics (medians over eRASS1): " + "; ".join(f"{v[0]} r_dom {DG['canonical'][v[0]]['rdom_med_kpc']:.0f}/{DG['alt'][v[0]]['rdom_med_kpc']:.0f} kpc "
                                                         f"C/M_b(1Mpc) {DG['canonical'][v[0]]['C_over_Mb_1Mpc_med']:.2f}/{DG['alt'][v[0]]['C_over_Mb_1Mpc_med']:.2f} "
                                                         f"f_coal {DG['canonical'][v[0]]['f_coal_med']:.3f} it<= {DG['canonical'][v[0]]['iters_max']} nonconv {DG['canonical'][v[0]]['nonconv']}"
                                                         for v in VARS))
    # ---- classes (a), (b)
    BRK = {"M3": ["M3_present", "M3_King", "M3_ICM", "M3_OD"], "M1": ["M1_present", "M1_King", "M1_ICM", "M1_OD"]}
    PV = [v[0] + "_prev" for v in VARS]
    TRp = {f: score_TR({v: W[("E", f)][v] for v in PV}) for f in FEET}
    TAp = {f: score_TA({v: W[("A", f)][v] for v in PV}, C686) for f in FEET}
    RES["T_R_prev_iteration"] = TRp; RES["T_A_prev_iteration"] = TAp

    def ca_cell(v):                                                  # frozen: last two iterations of different class -> UNDERDETERMINED
        c1 = cls_a({f: TR[f][v] for f in FEET}, {f: TA[f][v] for f in FEET})[0]
        c0 = cls_a({f: TRp[f][v + "_prev"] for f in FEET}, {f: TAp[f][v + "_prev"] for f in FEET})[0]
        return c1 if c1 == c0 else "UNDERDETERMINED"

    def cb_cell(v):
        c1 = cls_b({f: TR[f][v] for f in FEET})[0]; c0 = cls_b({f: TRp[f][v + "_prev"] for f in FEET})[0]
        return c1 if c1 == c0 else "UNDERDETERMINED"
    CA = {}; CB = {}
    for base in ("M3", "M1"):
        _, per = cls_a({f: TR[f][base] for f in FEET}, {f: TA[f][base] for f in FEET})
        _, perb = cls_b({f: TR[f][base] for f in FEET})
        ca, cb = ca_cell(base), cb_cell(base)
        br_a = {b: ca_cell(b) for b in BRK[base]}
        br_b = {b: cb_cell(b) for b in BRK[base]}
        ca_f = ca if (ca != "UNDERDETERMINED" and all(x == ca for x in br_a.values())) else ("UNDERDETERMINED" if ca == "UNDERDETERMINED" else "CONDITIONAL")
        cb_f = cb if (cb != "UNDERDETERMINED" and all(x == cb for x in br_b.values())) else ("UNDERDETERMINED" if cb == "UNDERDETERMINED" else "CONDITIONAL")
        CA[base] = dict(primary=ca, per_footing=per, brackets=br_a, final=ca_f)
        CB[base] = dict(primary=cb, per_footing=perb, brackets=br_b, final=cb_f)
    CA["M2"] = dict(CA["M1"], note="M2 = M1 for static cluster scoring (criteria section 2)"); CB["M2"] = dict(CB["M1"], note=CA["M2"]["note"])
    RES["class_a"] = CA; RES["class_b"] = CB
    P("\n== class (a) merger memory: " + "; ".join(f"{k} {CA[k]['final']} (primary {CA[k]['primary']}, brackets {CA[k].get('brackets')})" for k in ("M1", "M2", "M3")))
    P("== class (b) core (reading T): " + "; ".join(f"{k} {CB[k]['final']} (primary {CB[k]['primary']}, brackets {CB[k].get('brackets')})" for k in ("M1", "M2", "M3")))
    # ---- reading U
    B = b0_machinery(); Pb = B["dsig_newton"](B["MB"]); Pc = B["dsig_newton"](B["Mc"]); b0 = B["STE"].band(Pb + Pc)
    U = {}
    for f in FEET:
        um = B["STE"].band(W[("U", f)]["UM"]); uf = B["STE"].band(W[("U", f)]["UF"])
        U[f] = dict(B0=b0, U_members_King=um, U_members_full=uf, s_UM=B["s_model"](W[("U", f)]["UM"]))
    RES["reading_U"] = U
    for f in FEET:
        um, uf = U[f]["U_members_King"], U[f]["U_members_full"]
        P(f"  reading U {f[:3]}: B0 MID {b0['MID'][0]:.3f}±{b0['MID'][1]:.3f} OUTER {b0['OUTER'][0]:.3f}±{b0['OUTER'][1]:.3f} | + labelled members (King r_J, conserved) "
          f"MID {um['MID'][0]:.3f}±{um['MID'][1]:.3f} (Z {(um['MID'][0] - 1) / um['MID'][1]:+.2f}) OUTER {um['OUTER'][0]:.3f}±{um['OUTER'][1]:.3f} "
          f"(Z {(um['OUTER'][0] - 1) / um['OUTER'][1]:+.2f}) | full halos MID {uf['MID'][0]:.3f} OUTER {uf['OUTER'][0]:.3f}")
    zU = {f: dict(MID=(U[f]["U_members_King"]["MID"][0] - 1) / U[f]["U_members_King"]["MID"][1],
                  OUTER=(U[f]["U_members_King"]["OUTER"][0] - 1) / U[f]["U_members_King"]["OUTER"][1]) for f in FEET}
    U_a = "CONSISTENT" if all(abs(zU[f]["OUTER"]) < 2 for f in FEET) else ("INCONSISTENT" if all(abs(zU[f]["OUTER"]) >= 2 for f in FEET) else "CONDITIONAL")
    U_b = "CONSISTENT" if all(abs(zU[f]["MID"]) < 2 for f in FEET) else ("INCONSISTENT" if all(abs(zU[f]["MID"]) >= 2 for f in FEET) else "CONDITIONAL")
    RES["reading_U_classes"] = dict(a_eRASS1=U_a, b=U_b, Z=zU, note="LDT + an untethered-cluster selector (not in LDT); eRASS1 only (CFG949 B0 has no ACCEPT grade)")
    guard("reading U")
    # ---- (c) Bullet
    PHI = rd("CFG915_population_label_mobility/cfg915_results.json")["phi_lin"]
    C916 = rd("CFG916_lock_and_release/cfg916_cache.json")["misc"]["B"]
    BC = {}
    for f in FEET:
        b_ = bullet(f); plH = PHI[FL[f]]["H"]
        rec = dict(rJ_present=b_["rJ_present"], rdom_720=b_["rdom_720"], rhalf_b=b_["rhalf_b"], rt_sub=b_["rt_sub"], phi_lin_H=plH,
                   rhalf_star_posthoc=b_["rhalf_star_posthoc"], d_trigger_star_posthoc=b_["d_trigger_star_posthoc"],
                   dmin_headon_model=C916[FL[f]].get("dmin_model_kpc"))
        for var, phi in (("M3", b_["phi_M3"]), ("M1", b_["phi_M1"])):
            cls = np.where(phi <= plH, "C", np.where(phi >= 0.9, "I", "U"))
            rec[var] = dict(phi_720=float(phi[-1]),
                            d_cons_min=float(b_["dfine"][np.argmax(phi <= plH)]) if (phi <= plH).any() else None,
                            d_inc_max=float(b_["dfine"][np.where(phi >= 0.9)[0].max()]) if (phi >= 0.9).any() else None,
                            classes_present=sorted(set(cls.tolist())))
        rec["d_trigger"] = float(b_["dfine"][np.where(b_["rdom"] <= b_["rhalf_b"])[0].max()]) if (b_["rdom"] <= b_["rhalf_b"]).any() else None
        rec["d_core"] = float(b_["dfine"][np.where(b_["rdom"] <= R_CORE)[0].max()]) if (b_["rdom"] <= R_CORE).any() else None
        if rec["dmin_headon_model"]:
            k = int(np.argmin(np.abs(b_["dfine"] - rec["dmin_headon_model"]))); rec["phi_M3_at_headon_model"] = float(b_["phi_M3"][k])
            rec["phi_M1_at_headon_model"] = float(b_["phi_M1"][k])
        BC[f] = rec
        P(f"  (c) Bullet {f[:3]}: sub L2 r_dom(720) {b_['rdom_720']:.0f} kpc (King r_J {b_['rJ_present']:.0f}); r_dom <= 200 kpc core below d = {rec['d_core']} kpc; "
          f"trigger (r_dom <= r_half,b {b_['rhalf_b']:.0f} kpc) below d = {rec['d_trigger']} kpc; M3 phi CONSISTENT for d >= {rec['M3']['d_cons_min']}, "
          f"INCONSISTENT for d <= {rec['M3']['d_inc_max']}; M1 INCONSISTENT for d <= {rec['M1']['d_inc_max']}; phi_lin,H {plH:.4f}; "
          f"head-on model d_min {rec['dmin_headon_model']} -> phi M3 {rec.get('phi_M3_at_headon_model')}; "
          f"[POST HOC, no weight: stellar r_half {rec['rhalf_star_posthoc']:.0f} kpc -> trigger below d = {rec['d_trigger_star_posthoc']}]")
    CC = {}
    for var in ("M1", "M2", "M3"):
        srcs = {"M1": ("M1",), "M2": ("M3", "M1"), "M3": ("M3",)}[var]          # M2: bracket [M3, M1]
        sets = [set().union(*[set(BC[f][sv]["classes_present"]) for sv in srcs]) for f in FEET]
        if all(s == {"C"} for s in sets):
            CC[var] = "CONSISTENT"
        elif all(s == {"I"} for s in sets):
            CC[var] = "INCONSISTENT"
        else:
            CC[var] = "UNDERDETERMINED"
    RES["bullet"] = BC; RES["class_c"] = CC
    P("== class (c) Bullet: " + "; ".join(f"{k} {v}" for k, v in CC.items()) + " (M2 bracket [M3, M1]; pericentre not in the record)")
    guard("Bullet")
    # ---- (d) toy
    TOY = {}
    for f in FEET:
        for q in (1.0, 1 / 3, 0.1):
            TOY[f"{f}|q{q:.3f}"] = toy(q, f)
            tv = TOY[f"{f}|q{q:.3f}"]
            P(f"  (d) toy {f[:3]} q {q:.3f}: trigger d {tv['d_trigger']:.1f} kpc; J per t_dyn M3 {tv['variants']['M3']['J_max']:.4f} M1 {tv['variants']['M1']['J_max']:.4f} "
              f"(instant {tv['variants']['M1']['jump_inst_max']:.4f}) M2 {tv['variants']['M2']['J_max']:.4f}; max |label-induced excess| M3 {tv['variants']['M3']['E_abs_max']:.3f}; "
              f"[POST HOC fixed-configuration J: M3 {tv['variants']['M3']['J_fixedconf_posthoc_max']:.4f} M1 {tv['variants']['M1']['J_fixedconf_posthoc_max']:.4f} "
              f"M2 {tv['variants']['M2']['J_fixedconf_posthoc_max']:.4f}]")
            guard("toy")
    CD = {}
    for var in ("M1", "M2", "M3"):
        CD[var] = "CONSISTENT" if all(TOY[k]["variants"][var]["J_max"] <= 0.05 for k in TOY) else "INCONSISTENT"
    RES["toy"] = TOY; RES["class_d"] = CD
    # AMENDMENT A1 (2026-10-21, POST HOC, after the first MAIN run; reported, NO class weight): tau_1 from label 1's isolated medium
    TOYI = {}
    for f in FEET:
        for q in (1.0, 1 / 3, 0.1):
            tv = TOYI[f"{f}|q{q:.3f}"] = toy(q, f, tau_mode="iso"); tc = TOY[f"{f}|q{q:.3f}"]
            P(f"  (d) A1 iso-tau toy {f[:3]} q {q:.3f}: r_dom capped at {tv['n_rdom_capped']} steps (frozen C2-tau: {tc['n_rdom_capped']}), max r_dom/d below 300 kpc "
              f"{tv['rdom_max_over_d_below_300']:.2f} (frozen {tc['rdom_max_over_d_below_300']:.2f}); J M3 {tv['variants']['M3']['J_max']:.4f} M1 {tv['variants']['M1']['J_max']:.4f} "
              f"M2 {tv['variants']['M2']['J_max']:.4f} (instant M1 {tv['variants']['M1']['jump_inst_max']:.4f}); fixed-configuration M3 "
              f"{tv['variants']['M3']['J_fixedconf_posthoc_max']:.4f}; J at R = 20 kpc M3 {tv['variants']['M3']['J_by_R']['20.0']:.4f}")
            guard("toy A1")
    RES["toy_A1_iso_tau_posthoc"] = TOYI
    RES["class_d_A1_iso_tau_posthoc"] = {var: ("CONSISTENT" if all(TOYI[k]["variants"][var]["J_max"] <= 0.05 for k in TOYI) else "INCONSISTENT")
                                         for var in ("M1", "M2", "M3")}
    P("== (d) A1 (post hoc, no class weight): " + "; ".join(f"{k} {v}" for k, v in RES["class_d_A1_iso_tau_posthoc"].items()))
    P("== class (d) continuity: " + "; ".join(f"{k} {v} (max J {max(TOY[t]['variants'][k]['J_max'] for t in TOY):.4f})" for k, v in CD.items()))
    # ---- (e) UDGs
    R948 = rd("CFG948_nocapture_vs_udgs/cfg948_results.json"); rows = udg_rows()
    names = list(R948["A_per_galaxy"]["canonical"].keys())
    UE = {}
    for f in FEET:
        pr = R948["byfoot"][f]["primary"]; Eo, se, sy, Ec = pr["mean_Eobs"], pr["se_obs"], pr["sys_up"]["total"], pr["E_ceil"]
        sig = math.sqrt(se ** 2 + sy ** 2)
        per = {}
        for dkey in ("dmean", "dproj"):
            per[dkey] = {nm_: udg_one(rows[nm_], f, rows[nm_][dkey]) for nm_ in names}
        out = {}
        for dkey in ("dmean", "dproj"):
            pp = per[dkey]
            dE = np.mean([pp[n]["dE"] for n in names])
            pred = {}
            for var in ("M1", "M2", "M3"):
                vals = []
                for n in names:
                    x = pp[n]
                    if var in ("M1", "M2") and x["rdom_kpc"] <= x["rhalf_b_kpc"]:
                        vals.append(x["EN"])
                    else:
                        vals.append(Ec + x["dE"] + (x["E_partial"] if x["rdom_kpc"] < x["r12_kpc"] else 0.0))
                pred[var] = float(np.mean(vals))
            pred["M1-inf"] = float(np.mean([Ec + pp[n]["efe"] for n in names]))
            z = {k: (Eo - v) / sig for k, v in pred.items()}; zst = {k: (Eo - v) / se for k, v in pred.items()}
            out[dkey] = dict(mean_dE=float(dE), max_dE=float(max(pp[n]["dE"] for n in names)), pred=pred, z_sys=z, z_stat=zst,
                             n_rdom_lt_r12=int(sum(pp[n]["rdom_kpc"] < pp[n]["r12_kpc"] for n in names)),
                             n_relabel=int(sum(pp[n]["rdom_kpc"] <= pp[n]["rhalf_b_kpc"] for n in names)),
                             rdom_over_r12_min=float(min(pp[n]["rdom_kpc"] / pp[n]["r12_kpc"] for n in names)),
                             rows=per[dkey])
        UE[f] = dict(obs=dict(mean=Eo, se=se, sys=sy, E_ceil=Ec), by=out)
        o = out["dmean"]
        P(f"  (e) UDGs {f[:3]}: <E_obs> {Eo:+.3f}; LDT ceiling = {Ec:+.4f} + <dE> {o['mean_dE']:+.4f} (max {o['max_dE']:+.4f}; dproj {out['dproj']['mean_dE']:+.4f}); "
          f"z (sys) M3 {o['z_sys']['M3']:+.2f} M1 {o['z_sys']['M1']:+.2f} (stat {o['z_stat']['M3']:+.2f}); r_dom < r12 in {o['n_rdom_lt_r12']}/9, relabelled {o['n_relabel']}/9 "
          f"(min r_dom/r12 {o['rdom_over_r12_min']:.1f}); M1-inf (global phantom EFE) pred {o['pred']['M1-inf']:+.3f} z {o['z_sys']['M1-inf']:+.2f}")
    CE = {}
    for var in ("M1", "M2", "M3"):
        CE[var] = "INCONSISTENT" if all(UE[f]["by"]["dmean"]["z_sys"][var] >= 3 for f in FEET) else "NOT DIAGNOSTIC"
    RES["udg"] = UE; RES["class_e"] = CE
    P("== class (e) Coma UDGs: " + "; ".join(f"{k} {v}" for k, v in CE.items()))
    # ---- per-variant and overall
    VC = {}
    for var in ("M1", "M2", "M3"):
        a_, b_, c_, d_, e_ = CA[var]["final"], CB[var]["final"], CC[var], CD[var], CE[var]
        if "INCONSISTENT" in (a_, b_, d_, e_) or c_ == "INCONSISTENT":
            VC[var] = "INCONSISTENT"
        elif a_ == b_ == c_ == d_ == "CONSISTENT":
            VC[var] = "CONSISTENT"
        else:
            VC[var] = "CONDITIONAL"
    order = {"CONSISTENT": 0, "CONDITIONAL": 1, "INCONSISTENT": 2}
    best = min(VC.values(), key=lambda x: order[x])
    OVER = {"CONSISTENT": "LDT MERGERS OK", "CONDITIONAL": "CONDITIONAL", "INCONSISTENT": "FAIL"}[best]
    # reading U as "LDT + selector": (a) U-members eRASS1, (b) U-members MID, (c)-(e) as the variants
    VU = {}
    for var in ("M1", "M2", "M3"):
        a_, b_ = U_a, U_b
        if "INCONSISTENT" in (a_, b_, CD[var], CE[var]) or CC[var] == "INCONSISTENT":
            VU[var] = "INCONSISTENT"
        elif a_ == b_ == CC[var] == CD[var] == "CONSISTENT":
            VU[var] = "CONSISTENT"
        else:
            VU[var] = "CONDITIONAL"
    RES["variant_class"] = VC; RES["overall"] = OVER; RES["selector_reading_classes"] = VU
    P(f"\n== PER VARIANT: " + "; ".join(f"{k}: {v} [(a) {CA[k]['final']}, (b) {CB[k]['final']}, (c) {CC[k]}, (d) {CD[k]}, (e) {CE[k]}]" for k, v in VC.items()))
    P(f"== OVERALL (reading T, which LDT implies): {OVER}")
    P(f"== reported: 'LDT + untethered-cluster selector' (reading U; not LDT): " + "; ".join(f"{k} {v}" for k, v in VU.items()))
    # T-K reading (reported): coalesced remnants are single-label in every variant -> no early-type lift
    tk = rd("CFG726_merger_memory/cfg726_results.json")["T_K"]
    RES["T_K_reported"] = {f: dict(pred=tk[f"s|{f}|N1"]["pred"], Z=tk[f"s|{f}|N1"]["Z"]) for f in FEET}
    P(f"  reported: KiDS early types (CFG669 T2 +0.280 ± 0.083): single-label remnants give the law's {tk['s|canonical|N1']['pred']:+.3f} "
      f"(Z {tk['s|canonical|N1']['Z']:+.2f} / {tk['s|alt|N1']['Z']:+.2f}), CFG726's N = 1 cell")
    return RES


# ================================================================================================ dispatch
if STAGE == "COMPUTE":
    stage_compute()
    RESULT = None
elif STAGE == "K":
    RESULT = stage_K()
elif STAGE == "MUTATE":
    RESULT = stage_mutate()
else:
    RESULT = stage_main()
P(f"\nelapsed {time.time() - T0:.0f} s; peak RSS {rss() / 1e9:.3f} GB")
P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.")
finish_log()
if RESULT is not None:
    RESULT["runtime_s"] = time.time() - T0; RESULT["peak_rss_gb"] = rss() / 1e9
    json.dump(jclean(RESULT), open(os.path.join(OUTDIR, f"cfg951_results{TAG}.json"), "w"), indent=1)
code = 0
if STAGE == "MUTATE":
    code = 0 if all(v["ok"] for v in CHK.values()) else 1
if STAGE == "K":
    code = 0 if all(v["ok"] for v in CHK.values()) else 1
sys.exit(code)
