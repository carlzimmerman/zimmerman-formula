#!/usr/bin/env python3
"""CFG954 (criteria FROZEN_CRITERIA.md, 68a43b4ff): clusters and mergers under the source-changing non-local theory (SCT).

SCT working statement (criteria section 1): G = 8 pi G (T_b + T_c + S); S = sum_q S_q, each conserved, retarded and sourced by its
domain's OWN baryons only (no cross-sourcing); zero-sum per domain => forced edge at the supply root; constant carried weights between
events; domains bounded by the gravitational King r_J at pericentre (no medium tidal tensor in SCT).
Rules: R1 absorption (r_J < own edge -> stars + S_q folded into the host, host recomputed from its total own-domain baryons),
R2 persistence (members keep S_q inside r_J; host law of the gas), R3 hybrid (beyond r_J absorbed, inside r_J persists).
Cold-dust placement: P-S primary (halo S-carried), P-I bracket (dust-held halos); reading N = native dust + clip (CFG949 combination).
Tests (a) eRASS1 OUTER / MID, (b) ACCEPT (reported), (c) outer slope, (d) Bullet, (e) continuity toy, (f) momentum of the absorption
step, (g) Coma UDGs; selector test for the CFG949 combination.

Stages (one process at a time, from this directory, OMP_NUM_THREADS=1 nice -n 10):
  CFG954_STAGE=COMPUTE python3 cfg954.py  -> work arrays outside the repository (../_external_data/cfg954_work from the repo root)
  CFG954_STAGE=K       python3 cfg954.py  -> cfg954_K.out, cfg954_results_K.json
  CFG954_MUTATE=1      python3 cfg954.py  -> cfg954_MUTATE.out, cfg954_results_MUTATE.json
                       python3 cfg954.py  -> cfg954.out, cfg954_results.json
Amendment A1 (AMENDMENT_A1_implementation.md, 2026-10-21, after the 4-cluster smoke runs, before any full-data run): the R1 toy
momentum check uses the exact (interpolated) supply root; the harness grid residual and a convergence figure for r >= 10 kpc are
reported only.
Read-only inputs: cfg637_lib, CFG4_common, cfg652_model, cfg599_lib (imported); CFG726 / CFG916 / CFG947 / CFG951 code (copied, and
CFG951's copy of CFG949's exec recipe for the CFG686 / CFG922 engines); result JSONs of CFG726, 687, 686, 916, 915, 947, 948, 949,
951; CFG687 per-cluster npz; CFG726 and CFG951 work arrays; the Coma UDG table.  Nothing downloaded.
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
W726 = os.path.join(EXT, "cfg726_work"); W951 = os.path.join(EXT, "cfg951_work"); WORK = os.path.join(EXT, "cfg954_work")
os.makedirs(WORK, exist_ok=True)
STAGE = "MUTATE" if os.environ.get("CFG954_MUTATE", "") == "1" else os.environ.get("CFG954_STAGE", "MAIN").upper()
assert STAGE in ("COMPUTE", "K", "MUTATE", "MAIN")
NMAX = int(os.environ.get("CFG954_NMAX", "0"))                     # smoke tests only (outputs suffixed _SMOKE, outside the repo)
SMOKE = NMAX > 0
TAG = {"COMPUTE": "_COMPUTE", "K": "_K", "MUTATE": "_MUTATE", "MAIN": ""}[STAGE] + ("_SMOKE" if SMOKE else "")
WTAG = "_SMOKE" if SMOKE else ""
try:
    os.nice(10)
except OSError:
    pass
T0 = time.time(); LOG = []
RSS_LIMIT = 0.9e9
CRIT = "68a43b4ff"


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
    open(os.path.join(OUTDIR, f"cfg954{TAG}.out"), "w").write("\n".join(LOG) + "\n")


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
P(f"CFG954 [{STAGE}{' SMOKE N=' + str(NMAX) if SMOKE else ''}]  criteria {CRIT}  free+inactive at start {fg0 if fg0 is None else round(fg0, 1)} GB")
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

# ================================================================================================ CFG726 / CFG951 harness (copied)


def nu_s(y):                                                         # CFG695: g_N = g^2/(g + a0)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


A0K = {f: C4.A0[f] * L.SI_TO_KPCGYR2 for f in FEET}                  # kpc / Gyr^2
A0SI = {f: C4.A0[f] for f in FEET}
RE_GAL = M652.RE_BCG                                                 # 15 kpc (inherited)
SUP_PER_COND = M652.COLD_PER_B / M652.F_COND_FLOOR                   # 53.64 x m for a condensed progenitor
RHALF = (1.0 + math.sqrt(2.0)) * RE_GAL / M652.HERN_RE              # Hernquist baryonic half-mass radius (kpc)
A_HERN = RE_GAL / M652.HERN_RE                                       # Hernquist scale a (kpc)
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


def rJ_from_X(X, s, mcum):                                           # CFG916 (copied)
    q = np.maximum.accumulate(s ** 3 / np.maximum(mcum, 1e-300))
    X = np.asarray(X, float)
    out = np.exp(np.interp(np.log(np.maximum(X, 1e-300)), np.log(q), np.log(s)))
    out = np.where(X >= q[-1], np.inf, out)
    return np.where(X <= q[0], s[0], out)


def host_table(r, M, tracerM=None):                                  # CFG916 (copied)
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


def rJ_at(tab, rr, s, mcum):                                         # CFG916 (copied)
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


def pericentres(tab, d):                                             # CFG916 (copied)
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


def amat():                                                          # CFG951 (copied)
    global _AMAT
    if _AMAT is None:
        _AMAT = np.empty((len(DM_) * len(SM_), len(RCOARSE)))
        for j0 in range(0, len(RCOARSE), 34):
            A = shell_frac(SM_[None, :, None], DM_[:, None, None], RCOARSE[j0:j0 + 34][None, None, :])
            _AMAT[:, j0:j0 + 34] = A.reshape(len(DM_) * len(SM_), -1)
    return _AMAT


def conv_fast(dNT, Rout_kpc=RK_GRID):                                # CFG951 (copied)
    Cc = dNT.ravel() @ amat()
    Cc = np.maximum.accumulate(Cc)
    lo = np.log(np.maximum(Cc, 1e-300))
    out = np.exp(np.interp(np.log(Rout_kpc), np.log(RCOARSE), lo, left=-700.0))
    out[Rout_kpc > RCOARSE[-1]] = Cc[-1]
    return np.where(out < 1e-250, 0.0, out)


SQ6 = math.sqrt(6.0) / 3.0


def tau_of(r, M, Gc=L.G):                                            # CFG951 (copied; K1 only)
    dM = np.gradient(M, r, axis=-1)
    return SQ6 * np.abs(Gc * (dM / r ** 2 - 3.0 * M / r ** 3))


def env_of(tau):
    return np.maximum.accumulate(tau[..., ::-1], axis=-1)[..., ::-1]


def rdom_from_env(r, env, thr):                                      # CFG951 (copied)
    thr = np.asarray(thr, float)
    k = np.searchsorted(-env, -thr, side="right")
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


def cluster_ctx(Mg, fs, z, Nmem, foot):                              # CFG951 (copied) + SCT supply
    Mb = Mg * (1 + fs); Ms = fs * Mg; Mstar = float(Ms[-1])
    Ncum = np.interp(DK / 1000.0, RGRID, Mg) / Mg[-1]
    nmem = max(1, int(round(Nmem))); mi = Mstar / nmem
    shape = M652.hern(R_OBS, 1.0, RE_GAL)
    h, rta_i, xe = prog_halo(R_OBS, shape, mi, z, A0K[foot], nu_s)
    Mlaw = law_M(Mb, foot, nu_s)
    rho_gas = np.gradient(Mg, RK_GRID) / (4 * math.pi * RK_GRID ** 2)               # Msun / kpc^3
    Mg_edges = np.interp(DK / 1000.0, RGRID, Mg)
    bc, S_tot, _fr = M652.catchment(Mstar, float(Mg[-1]))
    return dict(Mg=Mg, Mb=Mb, Ms=Ms, Mstar=Mstar, fs=fs, z=z, Ncum=Ncum, dN=np.diff(Ncum), nmem=nmem, mi=mi, shape=shape, h=h,
                rta_i=rta_i, edge_kpc=(None if xe is None else xe * rta_i), Mlaw=Mlaw, T=Mlaw - Mb, foot=foot, mcum=mi * shape + h,
                env=env_of(tau_of(R_OBS, h)), rho_gas_d=np.exp(np.interp(np.log(DM_), np.log(RK_GRID), np.log(np.maximum(rho_gas, 1e-300)))),
                dMg_d=np.diff(Mg_edges), S_tot=float(S_tot), S_members=float(nmem * SUP_PER_COND * mi),
                P2_binds=bool(Mstar / M652.F_COND_FLOOR >= (Mstar + float(Mg[-1])) / M652.F_RET_XCOP))


def run_ldt(ctx, rule="L2", epoch="peri", coal=False, coupling="H1", halos2d=None, maxit=8, tol=1e-4, host0=None):   # CFG951 (copied; K1)
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
        else:
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
    return dict(Mtot=Mtot, Mprev=Mprev, C=C, iters=it, conv=conv)


# ================================================================================================ SCT cluster profiles (this lane)


def fh(x):
    """Hernquist enclosed baryon fraction at x (kpc), member scale a = R_e / 1.8153; fh(inf) = 1."""
    x = np.asarray(x, float)
    return np.where(np.isfinite(x), x * x / np.maximum((x + A_HERN) ** 2, 1e-300), 1.0)


def cum_placed(dMg, p_d):
    """cumulative mass of a gas-co-distributed component with per-host-radius weight p(d) (node-averaged, on DM_), on RK_GRID."""
    p_r = np.interp(np.log(RK_GRID), np.log(DM_), np.asarray(p_d, float))
    return np.cumsum(dMg * p_r)


def T_law(src, foot):
    T = law_M(src, foot, nu_s) - src
    return np.maximum.accumulate(np.maximum(T, 0.0))


def run_sct(ctx, rule, epoch="peri", cap=True, maxit=8, tol=1e-4, force_edge=None):
    """iterate one SCT cluster profile (criteria section 2).  rule R1PS | R1PI | R2 | R3.  epoch peri | present.  cap: forced edge
    (cumulative cap at the host's remaining supply) or the uncut harness law.  force_edge: override r_e,i (MU-0 control only)."""
    foot = ctx["foot"]; Mb, Mg = ctx["Mb"], ctx["Mg"]; nmem = ctx["nmem"]; dN = ctx["dN"]; fs = ctx["fs"]
    S = ctx["S_tot"]
    dT = np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :]
    edge = force_edge if force_edge is not None else (ctx["edge_kpc"] if ctx["edge_kpc"] is not None else ctx["rta_i"])
    dMg = np.diff(np.r_[0.0, Mg])
    Mtot = ctx["Mlaw"].copy(); hist = []; conv = np.inf; it = 0
    for it in range(1, maxit + 1):
        tab = host_table(RK_GRID, Mtot, Mg)
        if epoch == "peri":
            rp = pericentres(tab, DM_)[0]; wn = NODE_W
        else:
            rp = DM_[:, None].copy(); wn = np.ones(1)
        rJ = rJ_at(tab, rp, R_OBS, ctx["mcum"])
        keep = SM_[None, None, :] < rJ[:, :, None]
        WJ = np.einsum("w,dws->ds", wn, keep.astype(float))
        absb = np.ones_like(rJ, dtype=bool) if (force_edge is not None and np.isinf(force_edge)) else (rJ < edge)
        pabs = absb.astype(float) @ wn
        fb = fh(rJ) @ wn
        if rule == "R1PS":
            Wun = np.repeat(((~absb).astype(float) @ wn)[:, None], len(R_OBS), axis=1)
            C = nmem * conv_fast(dN[:, None] * dT * Wun)
            src = Mg + fs * cum_placed(dMg, pabs)
        else:
            C = nmem * conv_fast(dN[:, None] * dT * WJ)
            if rule == "R1PI":
                src = Mg + fs * cum_placed(dMg, pabs)
            elif rule == "R2":
                src = Mg.copy()
            elif rule == "R3":
                src = Mg + fs * cum_placed(dMg, 1.0 - fb)
            else:
                raise ValueError(rule)
        T = T_law(src, foot)
        Shost = S - float(C[-1])
        Tc = np.minimum(T, max(Shost, 0.0)) if cap else T
        Mn = Mb + C + Tc
        ok = Mtot > 0
        conv = float(np.max(np.abs(Mn[ok] / Mtot[ok] - 1)))
        conv10 = float(np.max(np.abs(Mn[ok & (RK_GRID >= 10.0)] / Mtot[ok & (RK_GRID >= 10.0)] - 1)))     # A1: reported only
        hist.append(conv)
        Mprev = Mtot
        Mtot = Mn
        if conv <= tol and it >= 2:
            break
    wgt = dN[:, None] * wn[None, :]
    i1 = int(np.argmin(np.abs(RK_GRID - 1000.0)))
    ke = np.where(T >= max(Shost, 0.0))[0]
    # (f) R1 global-recompute bracket: local QUMOND phantom around the median member (1-D on-axis, CFG947 T-X form)
    d_med = float(np.interp(0.5, ctx["Ncum"], DK)); rJm = wmedian(np.minimum(rJ, 1e9), wgt)
    a0 = A0SI[foot]; mb_m = ctx["mi"] * float(fh(rJm))
    g_h = G_SI * float(np.interp(d_med, RK_GRID, Mb)) * MSUN / (d_med * 3.0857e19) ** 2
    gNm = G_SI * mb_m * MSUN / (rJm * 3.0857e19) ** 2
    lawg = lambda g: g * float(nu_s(g / a0))
    Qm = (lawg(g_h + gNm) - lawg(g_h) - gNm) * (rJm * 3.0857e19) ** 2 / G_SI / MSUN
    hJ = float(np.interp(rJm, R_OBS, ctx["h"]))
    return dict(Mtot=Mtot, Mprev=Mprev, iters=it, conv=conv, hist=hist,
                f_abs=float((wgt * absb).sum() / wgt.sum()), rJ_med=rJm,
                C_tot_over_Mstar=float(C[-1] / ctx["Mstar"]), C_over_Mb_1Mpc=float(C[i1] / Mb[i1]),
                f_bound_stars=float((dN * fb).sum() / dN.sum()), Shost_over_S=Shost / S,
                r_edge_kpc=(float(RK_GRID[ke[0]]) if len(ke) and cap else None),
                Q_R3_PS=float(C[-1] / max(ctx["Mstar"] * float((dN * fb).sum() / dN.sum()), 1e-300)),
                Q_R1glob_over_m=Qm / max(mb_m, 1e-300), hJ_over_m_median=hJ / max(mb_m, 1e-300), d_med_kpc=d_med, conv_r10=conv10)


def supply_tot(ctx):
    return float(M652.catchment(ctx["Mstar"], float(ctx["Mg"][-1]))[1])


# ================================================================================================ scoring (CFG726 / CFG916 / CFG951 copied)
PC7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
NE_ALL = len(PC7["mg"])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
S_OBS, S_ERR = 0.896, 0.209                                          # CFG687 T2 (criteria (c))


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


# ================================================================================================ CFG949 B0 machinery (CFG951's copy; R930 handles exposed)
_B0 = {}


def b0_machinery():
    """CFG951's copy of CFG949's exec recipe for the CFG686 / CFG922 engines (no KiDS sources) and its verbatim R930 code.  This lane
    additionally exposes the R930 helpers (mta_fixed, prof930, m_, FBN) for the selector test.  CFG949's own script is never run."""
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
               selftest=_buf.getvalue().strip().splitlines(), idx=idx, mta_fixed=mta_fixed, prof930=prof930, m_=m_, FBN=FBN)
    return _B0


# ================================================================================================ (d) Bullet (record inputs)
R_CORE = 200.0


def bullet_sct(foot):
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
    dfine = np.geomspace(1.0, 720.0, 4000)
    rJf = np.minimum(rJ_at(tab, dfine, s, sub.Mtot[ok]), 1e12)
    Mph_s = sub.Mph[ok]
    core = float(np.interp(R_CORE, s, Mph_s))
    phiJ = 1.0 - np.interp(np.minimum(rJf, R_CORE), s, Mph_s, left=0.0) / core
    rt = float(sub.rt)
    phiR1 = np.where(rJf < rt, 1.0, 0.0)
    with contextlib.redirect_stdout(io.StringIO()):
        ph_st = P599.phantom_mass(sub.r, sub.Ms, sub.a0)[ok]; ph_all = P599.phantom_mass(sub.r, sub.Mbar, sub.a0)[ok]
    phi_share = 1.0 - float(np.interp(R_CORE, s, ph_st)) / float(np.interp(R_CORE, s, ph_all))
    return dict(rJ_present=rJ_present, rJ_grid=rJ_grid, dfine=dfine, rJ=rJf, phi_J=phiJ, phi_R1PS=phiR1, rt_sub=rt,
                phi_share_posthoc_report=phi_share, Mph_core=core, core_check_ph_all_vs_Mph=float(np.interp(R_CORE, s, ph_all)) / core - 1)


# ================================================================================================ (e) continuity toy (SCT)
RAP = (20.0, 50.0, 100.0, 200.0)
RAP2 = (5.0, 10.0, 20.0)
RULES = ("R1PS", "R1PI", "R2", "R3")


def jwin(tt, Es, tdyn):
    """CFG951's frozen metric: max over windows [t_i, t_i + t_dyn] of |E(t) - E(t_i)| (an instantaneous jump counts in full)."""
    best = 0.0
    for i in range(len(tt)):
        j = int(np.searchsorted(tt, tt[i] + tdyn, side="right"))
        best = max(best, float(np.max(np.abs(Es[i:j] - Es[i]))))
    return best


def toy_sct(q, foot, n_d=1521):
    a0 = A0K[foot]; Gk = L.G
    sk = R_OBS; shape = M652.hern(sk, 1.0, RE_GAL); m1 = 1e11; m2 = q * m1
    h1, rta1, xe1 = prog_halo(sk, shape, m1, 0.0, a0, nu_s); h2, rta2, xe2 = prog_halo(sk, shape, m2, 0.0, a0, nu_s)
    Mb1, Mb2 = m1 * shape, m2 * shape
    re2 = xe2 * rta2 if xe2 is not None else rta2
    S1, S2 = SUP_PER_COND * m1, SUP_PER_COND * m2
    dMb2 = np.diff(np.r_[0.0, Mb2]); dh2 = np.diff(np.r_[0.0, h2])
    tab1 = host_table(sk, Mb1 + h1)
    ds = np.r_[np.exp(np.linspace(math.log(1000.0), math.log(0.5), n_d)), 0.0]
    rj = np.array([float(rJ_at(tab1, np.array([d]), sk, Mb2 + h2)[0]) if d > 0 else 0.0 for d in ds])
    rj = np.minimum(rj, 1e12)
    rjl = np.minimum.accumulate(rj)                                  # latched (irreversible) truncation
    trig = np.where(rjl < re2)[0]; ktr = int(trig[0]) if len(trig) else len(ds) - 1
    Mlaw1 = Mb1 + h1; Mlaw2 = Mb2 + h2
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
    out = {}
    for rule in RULES:
        E1 = {R: [] for R in RAP}; E2 = {R: [] for R in RAP2}
        for k, d in enumerate(ds):
            rJ = rjl[k]; absorbed = rule in ("R1PS", "R1PI") and k >= ktr
            A2 = np.where(sk < rJ, h2, np.interp(rJ, sk, h2, left=0.0)); dA2 = np.diff(np.r_[0.0, A2])
            Mb2b = np.where(sk < rJ, Mb2, np.interp(rJ, sk, Mb2, left=0.0)); dMb2b = np.diff(np.r_[0.0, Mb2b]); dMb2s = dMb2 - dMb2b
            for R in RAP:
                eb2 = encl(dMb2, d, R)
                Sg = Mb1R[R] + eb2
                GP = Sg * float(nu_s(Gk * Sg / R ** 2 / a0))
                if rule in ("R1PS", "R1PI") and not absorbed:
                    Mv = L1(Mb1R[R], R, S1) + eb2 + encl(dh2, d, R)
                elif rule == "R1PS":
                    Mv = L1(Mb1R[R] + eb2, R, S1 + S2)
                elif rule == "R1PI":
                    Mv = L1(Mb1R[R] + eb2, R, S1 + S2 - float(A2[-1])) + encl(dA2, d, R)
                elif rule == "R2":
                    Mv = L1(Mb1R[R], R, S1 + S2 - float(A2[-1])) + eb2 + encl(dA2, d, R)
                else:                                                # R3
                    Mv = L1(Mb1R[R] + encl(dMb2s, d, R), R, S1 + S2 - float(A2[-1])) + encl(dMb2b + dA2, d, R)
                E1[R].append(Mv / GP - 1.0)
            for R in RAP2:
                own = float(np.interp(R, sk, Mb2)) + float(np.interp(R, sk, h2))
                grav = float(np.interp(R, sk, Mb2)) + float(np.interp(min(R, rJ), sk, h2, left=0.0))
                v2in = float(np.interp(R, sk, Mb2)) if (rule == "R1PS" and absorbed) else grav
                E2[R].append((v2in - grav) / own)
        J1 = {R: jwin(t, np.array(E1[R]), td1[R]) for R in RAP}
        J2 = {R: jwin(t, np.array(E2[R]), td2[R]) for R in RAP2}
        jump1 = max(abs(E1[R][ktr] - E1[R][ktr - 1]) for R in RAP) if ktr > 0 else 0.0
        jump2 = max(abs(E2[R][ktr] - E2[R][ktr - 1]) for R in RAP2) if ktr > 0 else 0.0
        out[rule] = dict(J1=J1, J2=J2, J_max=max(max(J1.values()), max(J2.values())), J1_max=max(J1.values()), J2_max=max(J2.values()),
                         jump_at_trigger_E1=jump1, jump_at_trigger_E2=jump2,
                         E1_final={str(R): E1[R][-1] for R in RAP}, E1_maxabs=max(max(abs(x) for x in E1[R]) for R in RAP))
    # (f) toy secondary: R1 monopole at the trigger (whole domain comoving, zero net charge -> 0 exactly); R3 [P-S] cumulative Q_in / m_bound;
    # R1 global-recompute bracket Q_m / m_bound at the trigger.
    Qin_PS = np.array([float(np.interp(r_, sk, h2, left=0.0)) / max(float(np.interp(r_, sk, Mb2, left=0.0)), 1e-300) if r_ > sk[0] else 0.0 for r_ in rjl[:-1]])
    # R1 at the trigger (A1): discretised member with the EXACT (interpolated) supply root; P-S rest cold S2 uniform in ln r on
    # [r_root, r_ta2]; draw q fixed by zero-sum; Q = sum of shell weights (active - rest).  The harness grid residual of prog_halo
    # (its edge sits one grid step past the root) is reported separately, no weight.
    ph_unc = np.maximum.accumulate((nu_s(Gk * Mb2 / sk ** 2 / a0) - 1.0) * Mb2)
    jr = int(np.searchsorted(ph_unc, S2))
    if 0 < jr < len(sk) and sk[jr] <= rta2:
        fr_ = (math.log(S2) - math.log(ph_unc[jr - 1])) / (math.log(ph_unc[jr]) - math.log(ph_unc[jr - 1]))
        r_root = math.exp(math.log(sk[jr - 1]) + fr_ * (math.log(sk[jr]) - math.log(sk[jr - 1])))
    else:
        r_root = rta2
    sh = np.r_[0.0, sk]
    a_in = np.minimum(np.interp(np.minimum(sh, r_root), sk, ph_unc, left=0.0), S2)            # active inside the root, cumulative on shell edges
    a_root = float(a_in[-1])
    lo_, hi_ = math.log(r_root), math.log(max(rta2, r_root * (1 + 1e-9)))
    rest = S2 * np.clip((np.log(np.maximum(sh, 1e-300)) - lo_) / (hi_ - lo_), 0.0, 1.0)          # cumulative rest cold (P-S)
    qd = a_root / S2                                                  # zero-sum draw
    act = a_in + (1.0 - qd) * rest
    w_ = np.diff(act) - np.diff(rest)
    m2_tot_charge = float(np.sum(w_))
    harness_resid = (float(h2[-1]) - S2) / (m2 + S2)
    dtr = ds[ktr]; rJt = rjl[ktr]
    a0s = A0SI[foot]; lawg = lambda g: g * float(nu_s(g / a0s))
    if dtr > 0 and rJt > 0:
        gext = G_SI * float(np.interp(dtr, sk, Mb1)) * MSUN / (dtr * 3.0857e19) ** 2
        mbt = float(np.interp(rJt, sk, Mb2)); gN2 = G_SI * mbt * MSUN / (rJt * 3.0857e19) ** 2
        Qm = (lawg(gext + gN2) - lawg(gext) - gN2) * (rJt * 3.0857e19) ** 2 / G_SI / MSUN; Qg = Qm / mbt
        # reported: the global-recompute E2 (EFE factor of label 2's law in label 1's baryonic field at the trigger), R = 5/10/20 kpc
        E2g = {}
        for R in RAP2:
            gNR = G_SI * float(np.interp(R, sk, Mb2)) * MSUN / (R * 3.0857e19) ** 2
            E2g[str(R)] = (lawg(gext + gNR) - lawg(gext)) / lawg(gNR) - 1.0
    else:
        Qg = None; E2g = None
    return dict(rules=out, d_trigger=float(dtr), rJ_at_trigger=float(rJt), r_e2=float(re2), t_trigger_Gyr=float(t[ktr]),
                t_total_Gyr=float(t[-1]), f_R1_dP_over_P=abs(m2_tot_charge) / (m2 + S2), f_R1_harness_grid_resid_report=harness_resid,
                f_R1_r_root_kpc=r_root, f_R3PS_dP_over_P_max=float(np.max(Qin_PS)),
                f_R3PI_dP_over_P=0.0, f_R1glob_dP_over_P=Qg, E2_global_recompute_report=E2g,
                tdyn1_Gyr={str(R): td1[R] for R in RAP}, tdyn2_Gyr={str(R): td2[R] for R in RAP2})


# ================================================================================================ (g) Coma UDGs
KPC_SI = 3.0857e19                                                   # CFG948's constant
BETA = dict(kT_keV=8.6, rc_kpc=276.0, beta=0.71, mu=0.6, m_p=1.67262e-27, keV=1.602176634e-16)       # CFG948 / L23
CBETA = 3 * BETA["beta"] * BETA["kT_keV"] * BETA["keV"] / (BETA["mu"] * BETA["m_p"])
RCB = BETA["rc_kpc"] * KPC_SI
Z_COMA = 0.0231                                                      # implementation choice (r_ta cap of the UDG edge only)


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


def udg_one(u, foot, D):                                             # CFG951 (copied; MU-GS ii)
    a0 = A0SI[foot]; M = u["L"] * u["ML"] * MSUN; a = u["Re"] * KPC_SI; r12 = 4.0 / 3.0 * a
    gN = G_SI * plummer_M(M, a, r12) / r12 ** 2
    law = lambda g: g * nu_e(g / a0)
    gloc = 4.0 * math.pi / 3.0 * G_SI * rho_host_coma(D) * r12
    dE = math.log(law(gN + gloc) / law(gN))
    EN = -math.log(nu_e(gN / a0))
    us = lambda x: law(G_SI * plummer_M(M, a, x) / x ** 2) - G_SI * plummer_M(M, a, x) / x ** 2
    th = tau_host_coma(D)
    xs = np.geomspace(0.01 * a, 1000 * a, 4001)
    tm = np.array([SQ6 * abs((us(x * (1 + 1e-5)) - us(x * (1 - 1e-5))) / (2e-5 * x) - us(x) / x) for x in xs])
    rdom = float(rdom_from_env(xs, env_of(tm), np.array([th]))[0])
    rh_b = a / math.sqrt(2 ** (2.0 / 3.0) - 1.0)
    u_full = us(r12)
    u_tr = law(gN) - gN if rdom >= r12 else G_SI * (us(rdom) * rdom ** 2 / G_SI) / r12 ** 2
    E_part = math.log((gN + u_tr) / (gN + u_full))
    gt = g_host_coma(D); gbh = gt * gt / (gt + a0)
    efe = math.log((law(gbh + gN) - law(gbh)) / law(gN))
    return dict(dE=dE, EN=EN, rdom_kpc=rdom / KPC_SI, r12_kpc=r12 / KPC_SI, rhalf_b_kpc=rh_b / KPC_SI, E_partial=E_part, efe=efe,
                gN=gN, gloc=gloc, Mloc_over_Mb12=gloc / gN)


def udg_sct(u, foot, D):
    """this lane: King r_J of the UDG in the beta-model host (self-consistent with its own nu_e-law mass), its supply edge, and the
    SCT predictions per rule (criteria (g))."""
    a0 = A0SI[foot]; Mst = u["L"] * u["ML"]; M = Mst * MSUN; a = u["Re"] * KPC_SI; r12 = 4.0 / 3.0 * a
    law = lambda g: g * nu_e(g / a0)
    gNx = lambda x: G_SI * plummer_M(M, a, x) / x ** 2
    Mlaw = lambda x: law(gNx(x)) * x * x / G_SI
    r = D * KPC_SI; Mh = g_host_coma(D) * r * r / G_SI; tmg = 2.0 * r * r / (r * r + RCB * RCB)       # 3 - gamma (beta model)
    fJ = lambda lx: math.log(math.exp(lx) ** 3 * tmg * Mh) - math.log(Mlaw(math.exp(lx)) * r ** 3)
    lo, hi = math.log(1e-3 * a), math.log(min(1e4 * a, 0.999 * r))
    rJ = math.exp(brentq(fJ, lo, hi, xtol=1e-12)) if fJ(lo) < 0 < fJ(hi) else (math.exp(hi) if fJ(hi) <= 0 else math.exp(lo))
    rM = math.sqrt(G_SI * M / a0); re_sup = rM / math.log1p(1.0 / SUP_PER_COND)
    rta = rta_of(Mst / M652.F_COND_FLOOR / L.FB, Z_COMA) * KPC_SI
    re = min(re_sup, rta)
    gN = gNx(r12); gloc = 4.0 * math.pi / 3.0 * G_SI * rho_host_coma(D) * r12
    us = lambda x: law(gNx(x)) - gNx(x)
    u_full = us(r12)
    u_keep = u_full if rJ >= r12 else us(rJ) * rJ * rJ / (r12 * r12)
    E_abs = math.log((gN + gloc) / law(gN))
    E_keep_extra = math.log((gN + u_keep + gloc) / law(gN))         # = ln[(g_law + g_loc)/g_law] when r_J >= r12
    return dict(rJ_kpc=rJ / KPC_SI, re_kpc=re / KPC_SI, re_sup_kpc=re_sup / KPC_SI, rta_kpc=rta / KPC_SI, r12_kpc=r12 / KPC_SI,
                absorbed=bool(rJ < re), E_abs=E_abs, E_keep_extra=E_keep_extra, gloc_over_gN=gloc / gN, rJ_over_r12=rJ / r12)


# ================================================================================================ CFG947 T-X (MU-GS i), copied
MSUN847, KPC847 = 1.989e30, 3.0857e19
HOST938 = 6e10
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]
RHOST = (50.0, 100.0, 250.0)


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
VARS = [("R1PS", "peri", True), ("R1PI", "peri", True), ("R2", "peri", True), ("R3", "peri", True),
        ("R1PS", "present", True), ("R1PI", "present", True), ("R2", "present", True), ("R3", "present", True),
        ("R1PS", "peri", False), ("R1PI", "peri", False), ("R2", "peri", False), ("R3", "peri", False)]


def vname(rule, ep, cap):
    return rule + ("" if ep == "peri" else "_present") + ("" if cap else "_uncut")


DIAGK = ("iters", "conv", "f_abs", "rJ_med", "C_tot_over_Mstar", "C_over_Mb_1Mpc", "f_bound_stars", "Shost_over_S", "r_edge_kpc",
         "Q_R3_PS", "Q_R1glob_over_m", "hJ_over_m_median", "d_med_kpc", "conv_r10")


def compute_cluster(Mg, z, Nm, foot):
    ctx = cluster_ctx(Mg, 0.20, z, Nm, foot)
    arr = {}; dg = {}
    arr["law"] = dsig_from_M(ctx["Mlaw"])
    arr["law_cap"] = dsig_from_M(ctx["Mb"] + np.minimum(ctx["T"], ctx["S_tot"]))
    C1 = ctx["nmem"] * convolve_members(DK, ctx["Ncum"], R_OBS, ctx["h"], RK_GRID)       # CFG726 verbatim (whole halos)
    arr["hmm"] = dsig_from_M(ctx["Mb"] + np.maximum(C1, ctx["T"]))                         # MU-NA (i): H-MM
    Tg = T_law(ctx["Mg"], foot)
    arr["na_sct"] = dsig_from_M(ctx["Mb"] + C1 + np.minimum(Tg, max(ctx["S_tot"] - float(C1[-1]), 0.0)))   # MU-NA (ii)
    for (rule, ep, cap) in VARS:
        o = run_sct(ctx, rule, ep, cap)
        nm = vname(rule, ep, cap)
        arr[nm] = dsig_from_M(o["Mtot"]); arr[nm + "_prev"] = dsig_from_M(o["Mprev"])
        dg[nm] = [o[k] for k in DIAGK]
    # MU-0 control: zero halos through the runner, every member absorbed (edge = inf), no cap -> the plain law
    z0 = dict(ctx); z0["h"] = 0.0 * ctx["h"]; z0["mcum"] = ctx["mi"] * ctx["shape"]
    o0 = run_sct(z0, "R1PS", "peri", False, maxit=2, force_edge=np.inf)
    arr["mu0"] = dsig_from_M(o0["Mtot"])
    # K5 (ii): CFG916's King pericentre median r_J in the plain-law host
    tab = host_table(RK_GRID, ctx["Mlaw"], Mg); rp = pericentres(tab, DM_)[0]
    rJp = rJ_at(tab, rp, R_OBS, ctx["mcum"])
    dg["K5_rJp_med"] = wmedian(np.minimum(rJp, 1e9), ctx["dN"][:, None] * NODE_W[None, :])
    dg["N"] = ctx["nmem"]; dg["edge_kpc"] = ctx["edge_kpc"]; dg["rta_i"] = ctx["rta_i"]; dg["mi"] = ctx["mi"]
    dg["S_tot"] = ctx["S_tot"]; dg["S_members"] = ctx["S_members"]; dg["P2_binds"] = ctx["P2_binds"]
    return arr, dg, ctx


def reading_N(k, ctx, B, foot):
    """reading N (criteria section 2): native dust (CFG949 B0) + clip; N-smooth and N+members, Msun on RGRID."""
    MS = B["MS"]; MBk = B["MB"][k] / MS; Mck = B["Mc"][k] / MS; SB0 = float(Mck[-1])
    T = T_law(MBk, foot)
    dTi = np.diff(np.r_[0.0, T]); dCi = np.diff(np.r_[0.0, Mck])
    NS = MBk + np.minimum(np.cumsum(np.maximum(np.maximum(dTi, dCi), 0.0)), SB0)
    tab = host_table(RK_GRID, NS, ctx["Mg"]); rp = pericentres(tab, DM_)[0]
    rJ = rJ_at(tab, rp, R_OBS, ctx["mcum"])
    WJ = np.einsum("w,dws->ds", NODE_W, (SM_[None, None, :] < rJ[:, :, None]).astype(float))
    CJ = ctx["nmem"] * conv_fast(ctx["dN"][:, None] * np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :] * WJ)
    fU = max(0.0, 1.0 - float(CJ[-1]) / SB0)
    NM = MBk + CJ + np.minimum(np.cumsum(np.maximum(np.maximum(dTi, fU * dCi), 0.0)), max(SB0 - float(CJ[-1]), 0.0))
    band = (RGRID >= 0.5) & (RGRID <= 1.2)
    frac_mid = float(np.mean(dCi[band] > dTi[band]))
    return NS, NM, dict(fU=fU, CJ_over_SB0=float(CJ[-1]) / SB0, frac_MID_dust_gt_phantom=frac_mid,
                        rJ_med=wmedian(np.minimum(rJ, 1e9), ctx["dN"][:, None] * NODE_W[None, :]))


def stage_compute():
    d = PC7; idx = erass_sel()
    lamj = json.load(open(os.path.join(W726, "lambda.json"))); Nm = np.array(lamj["Nmem"])
    B = b0_machinery()
    P(f"  B0 machinery ready ({time.time() - T0:.0f} s); RSS {rss() / 1e9:.2f} GB")
    ctx = cluster_ctx(erass_gas(int(idx[0]), d), 0.20, float(d["z"][idx[0]]), float(Nm[idx[0]]), "canonical")
    rng = np.random.default_rng(954); Wr = rng.random((len(DM_), len(R_OBS)))
    a = ctx["nmem"] * convolve_members_w(ctx["Ncum"], ctx["h"], RK_GRID, Wr)
    b = ctx["nmem"] * conv_fast(ctx["dN"][:, None] * np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :] * Wr)
    kw = float(np.max(np.abs(a - b) / np.maximum(a, 1e-300) * (a > 1e-200)))
    c1 = ctx["nmem"] * convolve_members(DK, ctx["Ncum"], R_OBS, ctx["h"], RK_GRID)
    c2 = ctx["nmem"] * conv_fast(ctx["dN"][:, None] * np.r_[ctx["h"][0], np.diff(ctx["h"])][None, :] * np.ones((len(DM_), len(R_OBS))))
    kw1 = float(np.max(np.abs(c1 - c2) / np.maximum(c1, 1e-300) * (c1 > 1e-200)))
    P(f"  K-W matrix convolution vs CFG916 (random weights) {kw:.1e}; vs CFG726 (weight 1) {kw1:.1e}")
    guard("K-W")
    for foot in FEET:
        res = {}; dgs = []; NSs = []; NMs = []; ndg = []
        for k, i in enumerate(idx):
            arr, dg, ctx = compute_cluster(erass_gas(int(i), d), float(d["z"][i]), float(Nm[i]), foot)
            for v, x in arr.items():
                res.setdefault(v, np.zeros((len(idx), 8)))[k] = x
            NS, NM, nd = reading_N(k, ctx, B, foot)
            NSs.append(NS); NMs.append(NM); ndg.append(nd)
            dgs.append(dg)
            if (k + 1) % 40 == 0 or k == len(idx) - 1:
                its = [x["R2"][0] for x in dgs]
                P(f"  eRASS1 {foot} {k + 1}/{len(idx)} ({time.time() - T0:.0f} s; RSS {rss() / 1e9:.2f} GB; R2 iterations max {max(its)})")
                guard(f"eRASS1 {foot} {k + 1}")
        np.savez(os.path.join(WORK, f"erass_{foot}{WTAG}.npz"), **res)
        json.dump(jclean(dgs), open(os.path.join(WORK, f"erass_{foot}_diag{WTAG}.json"), "w"))
        Bd = B["dsig_newton"]; ms = B["MS"]
        np.savez(os.path.join(WORK, f"N_{foot}{WTAG}.npz"), NS=Bd(np.array(NSs) * ms), NM=Bd(np.array(NMs) * ms))
        json.dump(jclean(ndg), open(os.path.join(WORK, f"N_{foot}_diag{WTAG}.json"), "w"))
        del NSs, NMs
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
        W[("N", foot)] = dict(np.load(os.path.join(WORK, f"N_{foot}{WTAG}.npz")))
        W[("Nd", foot)] = json.load(open(os.path.join(WORK, f"N_{foot}_diag{WTAG}.json")))
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
    R951 = rd("CFG951_ldt_mergers_clusters/cfg951_results.json")
    lamj = json.load(open(os.path.join(W726, "lambda.json"))); Nm = np.array(lamj["Nmem"])
    # ---- K1 CFG951 persistence failure (M3) and its X-OD bracket: stored arrays scored; M3 recomputed for a subset
    d1 = 0.0; d1r = 0.0; k1 = {}
    for foot in FEET:
        E9s = dict(np.load(os.path.join(W951, f"erass_{foot}.npz"))); A9s = dict(np.load(os.path.join(W951, f"accept_{foot}.npz")))
        tr = score_TR({v: E9s[v][idx] for v in ("M3", "M3_OD")}); ta = score_TA({v: A9s[v] for v in ("M3", "M3_OD")}, C686)
        if not SMOKE:
            for v in ("M3", "M3_OD"):
                ref = R951["T_R"][foot][v]; refA = R951["T_A"][foot][v]
                for b in ("MID", "OUTER"):
                    d1 = max(d1, abs(tr[v]["A"][b][0] - ref["A"][b][0]), abs(tr[v]["A"][b][1] - ref["A"][b][1]),
                             abs(ta[v]["A"][b][0] - refA["A"][b][0]), abs(ta[v]["A"][b][1] - refA["A"][b][1]))
                d1 = max(d1, abs(tr[v]["Z_outer"] - ref["Z_outer"]), abs(ta[v]["Z_outer"] - refA["Z_outer"]))
        for i in list(idx[:6]):
            ctx = cluster_ctx(erass_gas(int(i), PC7), 0.20, float(PC7["z"][i]), float(Nm[i]), foot)
            o = run_ldt(ctx, "L2", "peri", False, "H1")
            d1r = max(d1r, float(np.max(np.abs(dsig_from_M(o["Mtot"]) / E9s["M3"][int(i)] - 1))))
        for j, a_ in enumerate(acc):
            ctx = cluster_ctx(a_["Mg"], 0.20, a_["z"], a_["Nm"], foot)
            o = run_ldt(ctx, "L2", "peri", False, "H1")
            d1r = max(d1r, float(np.max(np.abs(dsig_from_M(o["Mtot"]) / A9s["M3"][j] - 1))))
        k1[foot] = dict(TR=tr, TA=ta)
        guard(f"K1 {foot}")
    check("K1 CFG951 persistence (M3) + X-OD stored arrays scored = cfg951_results.json (<= 1e-12); M3 recomputed (6 eRASS1 + 8 ACCEPT, both footings) = stored (<= 1e-10)",
          d1 <= 1e-12 and d1r <= 1e-10,
          f"max |diff| {d1:.1e}, recompute max rel {d1r:.1e}; M3 eRASS1 OUTER {k1['canonical']['TR']['M3']['A']['OUTER'][0]:.4f}±{k1['canonical']['TR']['M3']['A']['OUTER'][1]:.4f} "
          f"(Z {k1['canonical']['TR']['M3']['Z_outer']:+.2f}) / {k1['alt']['TR']['M3']['A']['OUTER'][0]:.4f} (Z {k1['alt']['TR']['M3']['Z_outer']:+.2f}); "
          f"ACCEPT {k1['canonical']['TA']['M3']['A']['OUTER'][0]:.4f} / {k1['alt']['TA']['M3']['A']['OUTER'][0]:.4f}; X-OD OUTER "
          f"{k1['canonical']['TR']['M3_OD']['A']['OUTER'][0]:.4f} / {k1['alt']['TR']['M3_OD']['A']['OUTER'][0]:.4f}")
    RES["K1"] = dict(scored=k1, maxdiff=d1, recompute_maxrel=d1r)
    # ---- K2 CFG726 H-MM
    ER = list(np.load(os.path.join(W726, "erass.npy"), allow_pickle=True)); AC = list(np.load(os.path.join(W726, "accept.npy"), allow_pickle=True))
    dmax = 0.0; dmax2 = 0.0; k2 = {}
    for foot in FEET:
        Ph = np.array([ER[i][f"hmm|s|{foot}|primary"] for i in idx]); tr = score_TR({"h": Ph})["h"]
        PhA = np.array([o[f"hmm|s|{foot}|primary"] for o in AC]); ta = score_TA({"h": PhA}, C686)["h"]
        ref = R726["T_R"][f"s|{foot}|primary"]; refA = R726["T_A"][f"s|{foot}|primary"]
        if not SMOKE:
            for b in ("MID", "OUTER"):
                dmax = max(dmax, abs(tr["A"][b][0] - ref["A"][b][0]), abs(tr["A"][b][1] - ref["A"][b][1]),
                           abs(ta["A"][b][0] - refA["A"][b][0]), abs(ta["A"][b][1] - refA["A"][b][1]))
            dmax = max(dmax, abs(tr["Z_outer"] - ref["Z_outer"]), abs(tr["Z_mid"] - ref["Z_mid"]), abs(ta["Z_outer"] - refA["Z_outer"]))
        dmax2 = max(dmax2, float(np.max(np.abs(W[("E", foot)]["hmm"] / Ph - 1))), float(np.max(np.abs(W[("A", foot)]["hmm"] / PhA - 1))))
        k2[foot] = dict(TR=tr, TA=ta)
    check("K2 CFG726 H-MM stored arrays scored = cfg726_results.json (<= 1e-12); recomputed = stored (<= 1e-10)", dmax <= 1e-12 and dmax2 <= 1e-10,
          f"max |diff| {dmax:.1e}, recompute max rel {dmax2:.1e}; eRASS1 OUTER {k2['canonical']['TR']['A']['OUTER'][0]:.4f} (Z {k2['canonical']['TR']['Z_outer']:+.2f}) / "
          f"{k2['alt']['TR']['A']['OUTER'][0]:.4f} (Z {k2['alt']['TR']['Z_outer']:+.2f}); ACCEPT {k2['canonical']['TA']['A']['OUTER'][0]:.4f} / {k2['alt']['TA']['A']['OUTER'][0]:.4f}")
    RES["K2"] = dict(scored=k2, maxdiff=dmax, recompute_maxrel=dmax2)
    # ---- K3 CFG687
    PL = np.asarray(PC7["PL"], float)[idx]; a3 = score_TR({"pl": PL})["pl"]; ref3 = R687["A"]["canonical|b0.67|rc0.15|f0.20"]
    d3 = 0.0 if SMOKE else max(max(abs(a3["A"][b][0] - ref3[b][0]), abs(a3["A"][b][1] - ref3[b][1])) for b in ("MID", "OUTER"))
    PLa = np.array([dsig_from_M(law_M(erass_gas(int(i), PC7) * 1.2, "alt", C4.nu_mono)) for i in idx])
    a3a = score_TR({"pl": PLa})["pl"]; ref3a = R687["A"]["alt|b0.67|rc0.15|f0.20"]
    d3a = 0.0 if SMOKE else max(max(abs(a3a["A"][b][0] - ref3a[b][0]), abs(a3a["A"][b][1] - ref3a[b][1])) for b in ("MID", "OUTER"))
    d3s = 0.0
    for foot in FEET:
        Pls = np.array([ER[i][f"law|s|{foot}"] for i in idx]); d3s = max(d3s, float(np.max(np.abs(W[("E", foot)]["law"] / Pls - 1))))
    check("K3 CFG687 stored PL -> A (<= 1e-9); alt law recomputed (<= 1e-6); nu_s law arrays = CFG726 stored (<= 1e-10)",
          d3 <= 1e-9 and d3a <= 1e-6 and d3s <= 1e-10,
          f"canonical MID {a3['A']['MID'][0]:.4f}±{a3['A']['MID'][1]:.4f} OUTER {a3['A']['OUTER'][0]:.4f}±{a3['A']['OUTER'][1]:.4f} s {a3['s']:.3f} (diff {d3:.1e}); "
          f"alt MID {a3a['A']['MID'][0]:.4f} OUTER {a3a['A']['OUTER'][0]:.4f} (diff {d3a:.1e}); nu_s law max rel {d3s:.1e}")
    RES["K3"] = dict(PL=a3, PL_alt=a3a, maxdiff=[d3, d3a, d3s])
    guard("K3")
    # ---- K4 CFG949 B0 primary corner
    B = b0_machinery(); Pb = B["dsig_newton"](B["MB"]); Pc = B["dsig_newton"](B["Mc"]); bd = B["STE"].band(Pb + Pc); s0 = B["s_model"](Pb + Pc)
    R949 = rd("CFG949_clusters_untethered/cfg949_results.json")["main"]["B0_primary"]
    d4 = 0.0 if SMOKE else max(max(max(abs(bd[b][0] - R949["A"][b][0]), abs(bd[b][1] - R949["A"][b][1])) for b in ("MID", "OUTER")), abs(s0 - R949["s"]))
    check("K4 CFG949 B0 primary corner recomputed = cfg949_results.json (<= 1e-9)", d4 <= 1e-9,
          f"A_MID {bd['MID'][0]:.4f}±{bd['MID'][1]:.4f}, A_OUTER {bd['OUTER'][0]:.4f}±{bd['OUTER'][1]:.4f}, s {s0:.4f} (diff {d4:.1e})")
    RES["K4"] = dict(A=bd, s=s0, maxdiff=d4)
    guard("K4")
    # ---- K5 CFG916 King r_J
    C916 = rd("CFG916_lock_and_release/cfg916_cache.json")
    d5 = 0.0; bl = {}
    for foot in FEET:
        b_ = bullet_sct(foot); ref = C916["misc"]["B"][FL[foot]]
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
    # ---- K-W and K-S
    RES["K_W"] = dict(maxrel_vs_CFG916=W["meta"]["KW"], maxrel_vs_CFG726=W["meta"]["KW1"])
    check("K-W matrix convolution = CFG916 convolve_members_w and CFG726 convolve_members (<= 1e-10)",
          W["meta"]["KW"] <= 1e-10 and W["meta"]["KW1"] <= 1e-10, f"{W['meta']['KW']:.1e} / {W['meta']['KW1']:.1e}")
    ks = 0.0; nP2 = 0; nall = 0
    for f in FEET:
        for dd in W[("Ed", f)] + W[("Ad", f)]:
            nall += 1
            if dd["P2_binds"]:
                nP2 += 1; ks = max(ks, abs(dd["S_members"] / dd["S_tot"] - 1))
    check("K-S supply identity sum_i S_i = S_tot (<= 1e-12) wherever CFG652's P2 branch binds (count reported)", ks <= 1e-12,
          f"max rel {ks:.1e}; P2 binds in {nP2}/{nall} cluster-footings")
    RES["K_S"] = dict(maxrel=ks, n_P2=nP2, n=nall)
    RES["checks"] = CHK; RES["K_all"] = all(v["ok"] for v in CHK.values())
    P(f"\nK: {sum(v['ok'] for v in CHK.values())}/{len(CHK)} pass")
    return RES


# ================================================================================================ MUTATE stage
def stage_mutate():
    RES = {}; W = load_work(); acc, C686 = accept_inputs(); idx = erass_sel()
    R726 = rd("CFG726_merger_memory/cfg726_results.json")
    # MU-NA
    na = {}; dA = 0.0; bite_h = True; bite_s = True
    for foot in FEET:
        tr = score_TR({"hmm": W[("E", foot)]["hmm"], "na_sct": W[("E", foot)]["na_sct"]})
        ta = score_TA({"hmm": W[("A", foot)]["hmm"], "na_sct": W[("A", foot)]["na_sct"]}, C686)
        ref = R726["T_R"][f"s|{foot}|primary"]; refA = R726["T_A"][f"s|{foot}|primary"]
        if not SMOKE:
            dA = max(dA, max(abs(tr["hmm"]["A"][b][0] - ref["A"][b][0]) for b in ("MID", "OUTER")),
                     max(abs(ta["hmm"]["A"][b][0] - refA["A"][b][0]) for b in ("MID", "OUTER")))
        bite_h &= tr["hmm"]["Z_outer"] <= -2
        bite_s &= tr["na_sct"]["Z_outer"] <= -2
        na[foot] = dict(TR=tr, TA=ta)
        P(f"  MU-NA {foot}: H-MM form eRASS1 OUTER {tr['hmm']['A']['OUTER'][0]:.3f}±{tr['hmm']['A']['OUTER'][1]:.3f} (Z {tr['hmm']['Z_outer']:+.2f}); "
          f"SCT never-absorb OUTER {tr['na_sct']['A']['OUTER'][0]:.3f}±{tr['na_sct']['A']['OUTER'][1]:.3f} (Z {tr['na_sct']['Z_outer']:+.2f}), MID "
          f"{tr['na_sct']['A']['MID'][0]:.3f}; ACCEPT OUTER {ta['na_sct']['A']['OUTER'][0]:.3f} (Z {ta['na_sct']['Z_outer']:+.2f})")
    check("MU-NA never absorb: H-MM form reproduces CFG726 (<= 1e-10) and fails eRASS1 OUTER; SCT's never-absorb form also fails eRASS1 OUTER (both footings)",
          dA <= 1e-10 and bite_h and bite_s, f"max |dA| vs CFG726 {dA:.1e}; H-MM bites {bite_h}; SCT never-absorb bites {bite_s}")
    RES["MU_NA"] = na
    # MU-GS
    R947 = rd("CFG947_option3_nonlocal_parent/cfg947_results.json")["T-X"]
    tx = {f"{f}|{nm_}|{rk:.0f}|{kz}": efe_global_dex(Mb_, apc, rk, A0SI[f], kz) for f in FEET for nm_, Mb_, apc in HOSTS882 for rk in RHOST for kz in KERN947}
    dgp = max(abs(tx[k] - R947[k]) for k in R947); present = max(abs(v) for v in tx.values()) > math.log10(1.01)
    R951 = rd("CFG951_ldt_mergers_clusters/cfg951_results.json"); R948 = rd("CFG948_nocapture_vs_udgs/cfg948_results.json"); rows = udg_rows()
    names = list(R948["A_per_galaxy"]["canonical"].keys()); dud = 0.0; zg = {}
    for f in FEET:
        pr = R948["byfoot"][f]["primary"]; Eo, se, sy, Ec = pr["mean_Eobs"], pr["se_obs"], pr["sys_up"]["total"], pr["E_ceil"]
        pred = float(np.mean([Ec + udg_one(rows[n], f, rows[n]["dmean"])["efe"] for n in names]))
        z = (Eo - pred) / math.sqrt(se ** 2 + sy ** 2); zg[f] = dict(pred=pred, z=z)
        dud = max(dud, abs(pred - R951["udg"][f]["by"]["dmean"]["pred"]["M1-inf"]), abs(z - R951["udg"][f]["by"]["dmean"]["z_sys"]["M1-inf"]))
    ok_gs = dgp <= 1e-12 and present and len(tx) == len(R947) == 36 and dud <= 1e-9 and all(zg[f]["z"] >= 3 for f in FEET)
    check("MU-GS global source: CFG947 T-X reproduced (36 values, <= 1e-12) with an EFE present; Coma UDGs under a global source = CFG951 M1-inf (<= 1e-9) with z >= 3",
          ok_gs, f"T-X max |diff| {dgp:.1e}, EFE {min(tx.values()):.3f}..{max(tx.values()):.3f} dex; UDG global-source pred {zg['canonical']['pred']:+.3f} / "
          f"{zg['alt']['pred']:+.3f} ln, z {zg['canonical']['z']:+.2f} / {zg['alt']['z']:+.2f} (diff {dud:.1e})")
    RES["MU_GS"] = dict(TX=tx, maxdiff=dgp, efe_present=present, udg=zg, udg_maxdiff=dud)
    dlaw = max(max(float(np.max(np.abs(W[(s, f)]["mu0"] / W[(s, f)]["law"] - 1))) for f in FEET) for s in ("E", "A"))
    check("MU-0 control: C = 0, no cap, through the SCT runner gives the plain law exactly (<= 1e-12, eRASS1 + ACCEPT, both footings)", dlaw <= 1e-12, f"max rel {dlaw:.1e}")
    RES["checks"] = CHK
    return RES


# ================================================================================================ MAIN stage
def cls2(z_by_foot):
    """|Z| < 2 both -> CONSISTENT; |Z| >= 2 both -> INCONSISTENT; else CONDITIONAL."""
    c = [abs(z_by_foot[f]) < 2 for f in FEET]
    return "CONSISTENT" if all(c) else ("INCONSISTENT" if not any(c) else "CONDITIONAL")


def cls_slope(s_by_foot):
    dz = [abs(s_by_foot[f] - S_OBS) / S_ERR for f in FEET]
    if all(x < 2 for x in dz):
        return "CONSISTENT"
    if all(x >= 3 for x in dz):
        return "INCONSISTENT"
    return "CONDITIONAL"


def stage_main():
    RES = {"lane": "CFG954", "criteria": CRIT, "post_hoc": True,
           "settings": dict(kappa="1/2 FITTED", footings=A0SI, kernel="nu_s", placement_primary="P-S")}
    W = load_work(); acc, C686 = accept_inputs(); idx = erass_sel()
    VN = ["law", "law_cap"] + [vname(*v) for v in VARS]
    TR = {f: score_TR({v: W[("E", f)][v] for v in VN}) for f in FEET}
    TA = {f: score_TA({v: W[("A", f)][v] for v in VN}, C686) for f in FEET}
    PV = [vname(*v) + "_prev" for v in VARS]
    TRp = {f: score_TR({v: W[("E", f)][v] for v in PV}) for f in FEET}
    RES["T_R"] = TR; RES["T_A"] = TA; RES["T_R_prev_iteration"] = TRp
    P("\n== (a)/(b)/(c) clusters: A = obs / model (eRASS1 30-patch jackknife; ACCEPT bootstrap 1000 seed 1); nu_s; s vs 0.896 ± 0.209")
    for v in VN:
        for f in FEET:
            t, a = TR[f][v], TA[f][v]
            P(f"  {v:14s} {f[:3]}: eRASS1 MID {t['A']['MID'][0]:.3f}±{t['A']['MID'][1]:.3f} (Z {t['Z_mid']:+.2f}) OUTER {t['A']['OUTER'][0]:.3f}±{t['A']['OUTER'][1]:.3f} "
              f"(Z {t['Z_outer']:+.2f}) s {t['s']:.3f} ({(t['s'] - S_OBS) / S_ERR:+.2f} s_err) | ACCEPT MID {a['A']['MID'][0]:.3f} (Z {a['Z_mid']:+.2f}) OUTER "
              f"{a['A']['OUTER'][0]:.3f}±{a['A']['OUTER'][1]:.3f} (Z {a['Z_outer']:+.2f})")
    DG = {}
    for f in FEET:
        dd = W[("Ed", f)]
        DG[f] = {}
        for v in VARS:
            nm = vname(*v); col = {k: [x[nm][j] for x in dd] for j, k in enumerate(DIAGK)}
            DG[f][nm] = dict(iters_max=int(max(col["iters"])), nonconv=int(sum(1 for c in col["conv"] if c > 1e-4)), conv_max=float(max(col["conv"])),
                             conv_r10_max=float(max(col["conv_r10"])), nonconv_r10=int(sum(1 for c in col["conv_r10"] if c > 1e-4)),
                             **{k + "_med": (float(np.median([c for c in col[k] if c is not None])) if any(c is not None for c in col[k]) else None)
                                for k in DIAGK if k not in ("iters", "conv")})
    RES["diagnostics"] = DG
    for f in FEET:
        P(f"  diagnostics {f[:3]} (eRASS1 medians): " + "; ".join(
            f"{nm} f_abs {DG[f][nm]['f_abs_med']:.3f} r_J {DG[f][nm]['rJ_med_med']:.0f} kpc C/M* {DG[f][nm]['C_tot_over_Mstar_med']:.2f} "
            f"C/M_b(1Mpc) {DG[f][nm]['C_over_Mb_1Mpc_med']:.2f} S_host/S {DG[f][nm]['Shost_over_S_med']:.2f} edge {DG[f][nm]['r_edge_kpc_med']} it<= {DG[f][nm]['iters_max']} nonconv {DG[f][nm]['nonconv']} (r >= 10 kpc: {DG[f][nm]['nonconv_r10']}, max {DG[f][nm]['conv_r10_max']:.1e})"
            for nm in ("R1PS", "R1PI", "R2", "R3")))

    def c_a(v, key):                                                 # frozen non-convergence rule: last two iterations of different class -> UNDERDETERMINED
        c1 = cls2({f: TR[f][v][key] for f in FEET}); c0 = cls2({f: TRp[f][v + "_prev"][key] for f in FEET})
        return c1 if c1 == c0 else "UNDERDETERMINED"

    def c_s(v):
        c1 = cls_slope({f: TR[f][v]["s"] for f in FEET}); c0 = cls_slope({f: TRp[f][v + "_prev"]["s"] for f in FEET})
        return c1 if c1 == c0 else "UNDERDETERMINED"

    def with_brackets(prim, brs):
        if prim == "UNDERDETERMINED":
            return "UNDERDETERMINED"
        return prim if all(b == prim for b in brs.values()) else "CONDITIONAL"
    # profile per row: R1 [P-I] uses the R1PI profile; R3 [P-S] / [P-I] share the R3 profile
    PROF = {"R1[P-S]": "R1PS", "R1[P-I]": "R1PI", "R2": "R2", "R3[P-S]": "R3", "R3[P-I]": "R3"}
    BR = {"R1[P-S]": ["R1PS_present", "R1PS_uncut", "R1PI"], "R1[P-I]": ["R1PI_present", "R1PI_uncut"],
          "R2": ["R2_present", "R2_uncut"], "R3[P-S]": ["R3_present", "R3_uncut"], "R3[P-I]": ["R3_present", "R3_uncut"]}
    CA1 = {}; CA2 = {}; CC = {}
    for row, pv in PROF.items():
        brs1 = {b: c_a(b, "Z_outer") for b in BR[row]}; brs2 = {b: c_a(b, "Z_mid") for b in BR[row]}; brs3 = {b: c_s(b) for b in BR[row]}
        CA1[row] = dict(primary=c_a(pv, "Z_outer"), brackets=brs1, final=with_brackets(c_a(pv, "Z_outer"), brs1))
        CA2[row] = dict(primary=c_a(pv, "Z_mid"), brackets=brs2, final=with_brackets(c_a(pv, "Z_mid"), brs2))
        CC[row] = dict(primary=c_s(pv), brackets=brs3, final=with_brackets(c_s(pv), brs3))
    RES["class_a1_memory"] = CA1; RES["class_a2_core"] = CA2; RES["class_c_slope"] = CC
    P("\n== (a1) memory (eRASS1 OUTER): " + "; ".join(f"{k} {v['final']} (primary {v['primary']})" for k, v in CA1.items()))
    P("== (a2) core (eRASS1 MID): " + "; ".join(f"{k} {v['final']} (primary {v['primary']})" for k, v in CA2.items()))
    P("== (c) outer slope: " + "; ".join(f"{k} {v['final']} (primary {v['primary']})" for k, v in CC.items()))
    guard("a-c")
    # ---- (d) Bullet
    PHI = rd("CFG915_population_label_mobility/cfg915_results.json")["phi_lin"]
    BC = {}
    for f in FEET:
        b_ = bullet_sct(f); plH = PHI[FL[f]]["H"]; df = b_["dfine"]
        rec = dict(rJ_present=b_["rJ_present"], rt_sub=b_["rt_sub"], phi_lin_H=plH, phi_share_report=b_["phi_share_posthoc_report"],
                   core_check=b_["core_check_ph_all_vs_Mph"], rJ_min=float(np.min(b_["rJ"])), d_at_rJ_min=float(df[int(np.argmin(b_["rJ"]))]),
                   n_dp_rJ_ge_rt=int(np.sum(b_["rJ"] >= b_["rt_sub"])))
        for var, phi in (("R1[P-S]", b_["phi_R1PS"]), ("J", b_["phi_J"])):
            cl = np.where(phi <= plH, "C", np.where(phi >= 0.9, "I", "U"))
            rec[var] = dict(phi_720=float(phi[-1]), classes_present=sorted(set(cl.tolist())),
                            d_cons_min=(float(df[np.argmax(phi <= plH)]) if (phi <= plH).any() else None),
                            d_inc_max=(float(df[np.where(phi >= 0.9)[0].max()]) if (phi >= 0.9).any() else None))
        BC[f] = rec
        P(f"  (d) Bullet {f[:3]}: sub King r_J(720) {b_['rJ_present']:.0f} kpc vs edge rt {b_['rt_sub']:.0f} kpc; min r_J {rec['rJ_min']:.1f} kpc at d {rec['d_at_rJ_min']:.1f}; "
            f"d_p with r_J >= rt: {rec['n_dp_rJ_ge_rt']}/4000; R1[P-S] phi classes {rec['R1[P-S]']['classes_present']}; phi_J CONSISTENT for d >= {rec['J']['d_cons_min']}, "
            f"INCONSISTENT for d <= {rec['J']['d_inc_max']} (phi_lin,H {plH:.4f}); [reported: R1 stars-only share phi {rec['phi_share_report']:.3f}]")

    def cd_of(sets):
        if all(s == {"C"} for s in sets):
            return "CONSISTENT"
        if all(s == {"I"} for s in sets):
            return "INCONSISTENT"
        return "UNDERDETERMINED"
    CD = {"R1[P-S]": cd_of([set(BC[f]["R1[P-S]"]["classes_present"]) for f in FEET])}
    for row in ("R1[P-I]", "R2", "R3[P-S]", "R3[P-I]"):
        CD[row] = cd_of([set(BC[f]["J"]["classes_present"]) for f in FEET])
    RES["bullet"] = BC; RES["class_d"] = CD
    P("== (d) Bullet: " + "; ".join(f"{k} {v}" for k, v in CD.items()))
    guard("Bullet")
    # ---- (e) toy
    TOY = {}
    for f in FEET:
        for q in (1.0, 1 / 3, 0.1):
            tv = TOY[f"{f}|q{q:.3f}"] = toy_sct(q, f)
            P(f"  (e) toy {f[:3]} q {q:.3f}: trigger d {tv['d_trigger']:.1f} kpc (r_J {tv['rJ_at_trigger']:.0f} < r_e2 {tv['r_e2']:.0f}; t {tv['t_trigger_Gyr']:.2f} of {tv['t_total_Gyr']:.2f} Gyr); J: "
              + "; ".join(f"{r} {tv['rules'][r]['J_max']:.4f} (E1 {tv['rules'][r]['J1_max']:.4f}, E2 {tv['rules'][r]['J2_max']:.4f})" for r in RULES)
              + f"; R1[P-S] E2 jump at trigger {tv['rules']['R1PS']['jump_at_trigger_E2']:.4f}; R2 final E1 {tv['rules']['R2']['E1_final']}")
            guard("toy")
    CE = {}
    for row, r in (("R1[P-S]", "R1PS"), ("R1[P-I]", "R1PI"), ("R2", "R2"), ("R3[P-S]", "R3"), ("R3[P-I]", "R3")):
        CE[row] = "CONSISTENT" if all(TOY[k]["rules"][r]["J_max"] <= 0.05 for k in TOY) else "INCONSISTENT"
    RES["toy"] = TOY; RES["class_e"] = CE
    P("== (e) continuity: " + "; ".join(f"{k} {v} (max J {max(TOY[t]['rules'][PROF[k] if k in PROF else k]['J_max'] for t in TOY):.4f})" for k, v in CE.items()))
    # ---- (f) momentum
    FQ = {}
    for f in FEET:
        dd = W[("Ed", f)]
        q3 = float(np.median([x["R3"][DIAGK.index("Q_R3_PS")] for x in dd]))
        qg = float(np.median([x["R1PS"][DIAGK.index("Q_R1glob_over_m")] for x in dd]))
        FQ[f] = dict(R1_mono=0.0, R1_global_bracket=qg, R2=0.0, R3_PS=q3, R3_PI=0.0,
                     toy_R1=max(TOY[k]["f_R1_dP_over_P"] for k in TOY if k.startswith(f)),
                     toy_R3_PS=max(TOY[k]["f_R3PS_dP_over_P_max"] for k in TOY if k.startswith(f)),
                     toy_R1_global=max((TOY[k]["f_R1glob_dP_over_P"] or 0.0) for k in TOY if k.startswith(f)))
        FQ[f]["toy_R1_harness_grid_resid_report"] = max(abs(TOY[k]["f_R1_harness_grid_resid_report"]) for k in TOY if k.startswith(f))
        P(f"  (f) {f[:3]}: |dP_s|/P_member: R1 monopole {FQ[f]['R1_mono']:.1e} (toy, exact root {FQ[f]['toy_R1']:.1e}; harness-grid residual, reported {FQ[f]['toy_R1_harness_grid_resid_report']:.1e}); R1 global bracket {qg:.3f} (toy {FQ[f]['toy_R1_global']:.3f}); "
          f"R2 0 (no event); R3[P-S] {q3:.2f} (toy {FQ[f]['toy_R3_PS']:.2f}); R3[P-I] 0")

    def cf(vals):
        c = [v <= 0.01 for v in vals]
        return "CONSISTENT" if all(c) else ("INCONSISTENT" if not any(c) else "CONDITIONAL")
    CF = {}
    r1p = cf([max(FQ[f]["R1_mono"], FQ[f]["toy_R1"]) for f in FEET]); r1b = cf([max(FQ[f]["R1_global_bracket"], FQ[f]["toy_R1_global"]) for f in FEET])
    CF["R1[P-S]"] = r1p if r1b == r1p else "CONDITIONAL"
    CF["R1[P-I]"] = CF["R1[P-S]"]
    CF["R2"] = "CONSISTENT"
    CF["R3[P-S]"] = cf([max(FQ[f]["R3_PS"], FQ[f]["toy_R3_PS"]) for f in FEET])
    CF["R3[P-I]"] = "CONSISTENT"
    RES["momentum"] = FQ; RES["class_f"] = CF
    # mass bookkeeping: total active <= S_tot in every capped profile (checked through S_host and the cap): report min S_host/S
    shmin = {f: {nm: float(min(x[nm][DIAGK.index("Shost_over_S")] for x in W[("Ed", f)])) for nm in ("R1PS", "R1PI", "R2", "R3")} for f in FEET}
    RES["mass_bookkeeping_min_Shost_over_S"] = shmin
    P("== (f) momentum: " + "; ".join(f"{k} {v}" for k, v in CF.items()) + f"; min S_host/S_tot over eRASS1 {shmin}")
    # ---- (g) UDGs
    R948 = rd("CFG948_nocapture_vs_udgs/cfg948_results.json"); rows = udg_rows()
    names = list(R948["A_per_galaxy"]["canonical"].keys())
    UE = {}
    for f in FEET:
        pr = R948["byfoot"][f]["primary"]; Eo, se, sy, Ec = pr["mean_Eobs"], pr["se_obs"], pr["sys_up"]["total"], pr["E_ceil"]
        sig = math.sqrt(se ** 2 + sy ** 2); out = {}
        for dkey in ("dmean", "dproj"):
            pp = {n: udg_sct(rows[n], f, rows[n][dkey]) for n in names}
            keep = [Ec + pp[n]["E_keep_extra"] for n in names]       # own phantom kept inside r_J (+ the host's local density, Newtonian)
            pred = {"R1[P-S]": float(np.mean([pp[n]["E_abs"] if pp[n]["absorbed"] else keep[j] for j, n in enumerate(names)])),
                    "keep (R1[P-I], R2, R3)": float(np.mean(keep))}
            z = {k: (Eo - v) / sig for k, v in pred.items()}
            out[dkey] = dict(pred=pred, z_sys=z, z_stat={k: (Eo - v) / se for k, v in pred.items()},
                             n_absorbed=int(sum(pp[n]["absorbed"] for n in names)), n_rJ_lt_r12=int(sum(pp[n]["rJ_kpc"] < pp[n]["r12_kpc"] for n in names)),
                             rJ_over_r12_min=float(min(pp[n]["rJ_over_r12"] for n in names)), rows=pp)
        UE[f] = dict(obs=dict(mean=Eo, se=se, sys=sy, E_ceil=Ec), by=out)
        o = out["dmean"]
        P(f"  (g) UDGs {f[:3]}: <E_obs> {Eo:+.3f}; absorbed (r_J < r_e) {o['n_absorbed']}/9 (dproj {out['dproj']['n_absorbed']}/9); r_J/r12 min {o['rJ_over_r12_min']:.2f}; "
          f"R1[P-S] pred {o['pred']['R1[P-S]']:+.3f} z {o['z_sys']['R1[P-S]']:+.2f}; keep pred {o['pred']['keep (R1[P-I], R2, R3)']:+.4f} z {o['z_sys']['keep (R1[P-I], R2, R3)']:+.2f} "
          f"(stat {o['z_stat']['keep (R1[P-I], R2, R3)']:+.2f})")
    CG = {}
    for row in ("R1[P-S]", "R1[P-I]", "R2", "R3[P-S]", "R3[P-I]"):
        key = "R1[P-S]" if row == "R1[P-S]" else "keep (R1[P-I], R2, R3)"
        CG[row] = "INCONSISTENT" if all(UE[f]["by"]["dmean"]["z_sys"][key] >= 3 for f in FEET) else "NOT DIAGNOSTIC"
    RES["udg"] = UE; RES["class_g"] = CG
    P("== (g) Coma UDGs: " + "; ".join(f"{k} {v}" for k, v in CG.items()))
    guard("UDG")
    # ---- reading N and the selector
    B = b0_machinery()
    NR = {}
    for f in FEET:
        ns = B["STE"].band(W[("N", f)]["NS"]); nmm = B["STE"].band(W[("N", f)]["NM"])
        NR[f] = dict(N_smooth=dict(A=ns, s=B["s_model"](W[("N", f)]["NS"])), N_members=dict(A=nmm, s=B["s_model"](W[("N", f)]["NM"])),
                     fU_med=float(np.median([x["fU"] for x in W[("Nd", f)]])), frac_MID_dust_gt_phantom_med=float(np.median([x["frac_MID_dust_gt_phantom"] for x in W[("Nd", f)]])))
        P(f"  reading N {f[:3]}: N-smooth MID {ns['MID'][0]:.3f}±{ns['MID'][1]:.3f} OUTER {ns['OUTER'][0]:.3f}±{ns['OUTER'][1]:.3f} s {NR[f]['N_smooth']['s']:.3f} | "
          f"N+members MID {nmm['MID'][0]:.3f}±{nmm['MID'][1]:.3f} (Z {(nmm['MID'][0] - 1) / nmm['MID'][1]:+.2f}) OUTER {nmm['OUTER'][0]:.3f}±{nmm['OUTER'][1]:.3f} "
          f"(Z {(nmm['OUTER'][0] - 1) / nmm['OUTER'][1]:+.2f}) s {NR[f]['N_members']['s']:.3f}; f_U {NR[f]['fU_med']:.3f}; median MID fraction dust > phantom {NR[f]['frac_MID_dust_gt_phantom_med']:.2f}")
    zN = {f: dict(MID=(NR[f]["N_members"]["A"]["MID"][0] - 1) / NR[f]["N_members"]["A"]["MID"][1],
                  OUTER=(NR[f]["N_members"]["A"]["OUTER"][0] - 1) / NR[f]["N_members"]["A"]["OUTER"][1]) for f in FEET}
    NCL = dict(a1=cls2({f: zN[f]["OUTER"] for f in FEET}), a2=cls2({f: zN[f]["MID"] for f in FEET}), c=cls_slope({f: NR[f]["N_members"]["s"] for f in FEET}))
    # selector: galaxy side (native dust vs phantom at 2-50 kpc) and cluster side (median-Mgas eRASS1 cluster, whole MID band)
    RS = (2.0, 5.0, 10.0, 20.0, 30.0, 50.0); SEL = {}
    rr = np.geomspace(0.5, 200.0, 4001)
    for f in FEET:
        a0 = A0SI[f]; SEL[f] = {}
        for Mbg in (1e9, 1e10, 4.72e10, 1e11):
            fr, Mta = B["mta_fixed"](Mbg); c, rs, rb, zc = B["prof930"](Mta, 0.0, 3000.0, "rta")
            rhoc = (1 - B["FBN"]) * Mta / (4 * math.pi * rs ** 3 * float(B["m_"](c))) / ((rr / rs) * (1 + rr / rs) ** 2) * (rr < rb)
            gN = G_SI * Mbg * MSUN / (rr * KPC_SI) ** 2; Tph = Mbg * (nu_s(gN / a0) - 1.0)
            rhoph = np.gradient(Tph, rr) / (4 * math.pi * rr ** 2)
            ratio = {str(x): float(np.interp(x, rr, rhoc) / np.interp(x, rr, rhoph)) for x in RS}
            SEL[f][f"{Mbg:.3g}"] = dict(ratio=ratio, f_ret=fr, M_ta=Mta, c=c, r_s=rs, r_b=rb, z_c=zc,
                                        below_phantom_2_30=bool(all(ratio[str(x)] < 1 for x in RS if x <= 30.0)))
        P(f"  selector {f[:3]} (native dust / phantom density): " + "; ".join(f"M_b {k}: " + ", ".join(f"{x:g} kpc {v['ratio'][str(x)]:.2f}" for x in RS) for k, v in SEL[f].items()))
    mg = np.asarray(PC7["mg"], float)[idx]; kmed = int(np.argmin(np.abs(mg - np.median(mg))))
    clus_med = {f: W[("Nd", f)][kmed]["frac_MID_dust_gt_phantom"] for f in FEET}
    gal_ok = all(v["below_phantom_2_30"] for f in FEET for v in SEL[f].values())
    clu_ok = all(clus_med[f] >= 1.0 for f in FEET)
    SELV = "DERIVED" if (gal_ok and clu_ok) else "CHOICE"
    RES["reading_N"] = dict(scores=NR, Z=zN, classes=NCL, selector=dict(galaxies=SEL, cluster_median_frac_MID=clus_med, galaxy_condition=gal_ok,
                                                                        cluster_condition=clu_ok, verdict=SELV))
    P(f"== reading N (native dust + clip, N+members): (a1) {NCL['a1']}, (a2) {NCL['a2']}, (c) {NCL['c']}; selector: galaxy condition {gal_ok}, cluster condition {clu_ok} "
      f"(median-Mgas cluster MID fraction {clus_med}) -> {SELV}")
    # ---- per row, per rule, overall
    ROWS = ("R1[P-S]", "R1[P-I]", "R2", "R3[P-S]", "R3[P-I]")
    VC = {}
    for row in ROWS:
        a1, a2, c_, d_, e_, f_, g_ = CA1[row]["final"], CA2[row]["final"], CC[row]["final"], CD[row], CE[row], CF[row], CG[row]
        if "INCONSISTENT" in (a1, a2, c_, e_, f_, g_) or d_ == "INCONSISTENT":
            VC[row] = "INCONSISTENT"
        elif a1 == a2 == c_ == d_ == e_ == f_ == "CONSISTENT":
            VC[row] = "CONSISTENT"
        else:
            VC[row] = "CONDITIONAL"
    RC = {}
    for rule, rows_ in (("R1", ("R1[P-S]", "R1[P-I]")), ("R2", ("R2",)), ("R3", ("R3[P-S]", "R3[P-I]"))):
        s_ = set(VC[r] for r in rows_)
        RC[rule] = s_.pop() if len(s_) == 1 else "CONDITIONAL"
    if SELV == "DERIVED":                                            # frozen: reading N enters as an R1 row
        a1, a2, c_ = NCL["a1"], NCL["a2"], NCL["c"]
        d_, e_, f_, g_ = CD["R1[P-I]"], CE["R1[P-I]"], CF["R1[P-I]"], CG["R1[P-I]"]
        VC["R1[N]"] = ("INCONSISTENT" if ("INCONSISTENT" in (a1, a2, c_, e_, f_, g_) or d_ == "INCONSISTENT")
                       else ("CONSISTENT" if a1 == a2 == c_ == d_ == e_ == f_ == "CONSISTENT" else "CONDITIONAL"))
        s_ = set(VC[r] for r in ("R1[P-S]", "R1[P-I]", "R1[N]")); RC["R1"] = s_.pop() if len(s_) == 1 else "CONDITIONAL"
    order = {"CONSISTENT": 0, "CONDITIONAL": 1, "INCONSISTENT": 2}
    best = min(RC.values(), key=lambda x: order[x])
    OVER = {"CONSISTENT": "SCT CLUSTERS OK", "CONDITIONAL": "SCT CLUSTERS CONDITIONAL", "INCONSISTENT": "SCT CLUSTERS FAIL"}[best]
    RES["row_class"] = VC; RES["rule_class"] = RC; RES["overall"] = OVER
    P("\n== PER ROW: " + "; ".join(f"{r}: {VC[r]} [(a1) {CA1[r]['final']}, (a2) {CA2[r]['final']}, (c) {CC[r]['final']}, (d) {CD[r]}, (e) {CE[r]}, (f) {CF[r]}, (g) {CG[r]}]" for r in ROWS))
    P("== PER RULE: " + "; ".join(f"{k} {v}" for k, v in RC.items()))
    P(f"== OVERALL: {OVER}")
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
    json.dump(jclean(RESULT), open(os.path.join(OUTDIR, f"cfg954_results{TAG}.json"), "w"), indent=1)
code = 0
if STAGE in ("MUTATE", "K"):
    code = 0 if all(v["ok"] for v in CHK.values()) else 1
sys.exit(code)
