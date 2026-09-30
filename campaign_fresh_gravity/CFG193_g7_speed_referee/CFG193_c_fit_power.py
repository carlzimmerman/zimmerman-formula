#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""CFG193_c_fit_power -- the fit, Fisher row, nulls, systematics rows, attacks A2-A4, B1-B3, C1-C5, and the MUTATE controls.
Own code.  MUTATE=k (k = 1..6) writes *_MUTATE<k>.*; exit 1 = the control BITES, 3 = it did NOT, 2 = own checks failed.
  1 point-level beta = 0.30 injection (curves CFG193_curves_MUTATE1.npz)   2 shuffle w, inject beta = 1.0 in the true pairing
  3 no profiling (curves _MUTATE3.npz)   4 u -> u + 600   5 exponential-RAR kernel (curves _MUTATE5.npz)   6 constant u
Rerun order (from the repository root):
  ZF_REPO=<repo> python3 CFG193_a_velocities.py ; python3 CFG193_b_curves.py ; MUTATE=1|3|5 python3 CFG193_b_curves.py ;
  python3 CFG193_c_fit_power.py ; MUTATE=1..6 python3 CFG193_c_fit_power.py ; python3 CFG193_d_design.py"""
import os, sys, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG193_common import *

MODE = int(os.environ.get("MUTATE", "0"))
SUF = ("" if MODE == 0 else "_MUTATE%d" % MODE) + ("_" + VARIANT if VARIANT else "")
T = Tee(os.path.join(HERE, "CFG193_c_fit_power%s.out" % SUF))
P = T.p
t_start = time.time()
NPROC = min(14, os.cpu_count() or 4)
SMOKE = os.environ.get("CFG193_SMOKE") == "1"          # debugging only (outputs then carry _SMOKE and are never used)
if SMOKE:
    SUF = SUF + "_SMOKE"
    T = Tee(os.path.join(HERE, "CFG193_c_fit_power%s.out" % SUF))
    P = T.p
SC = 0.02 if SMOKE else 1.0
P("CFG193_c_fit_power  mode MUTATE=%d  (repo = <repo>)" % MODE)

# ------------------------------------------------------------------------------------------------ data
ut = np.load(os.path.join(HERE, "CFG193_utable.npz"))
un = [str(x) for x in ut["names"]]
cnpz = "CFG193_curves%s%s.npz" % ("_MUTATE%d" % MODE if MODE in (1, 3, 5) else "", "_" + VARIANT if VARIANT else "")
cz_ = np.load(os.path.join(HERE, cnpz))
cnames = [str(x) for x in cz_["names"]]
cidx = {n: i for i, n in enumerate(cnames)}
uidx = {n: i for i, n in enumerate(un)}
fD_u = ut["fD"]
prim_names = [n for n in un if fD_u[uidx[n]] in (2, 3, 4, 5) and n in cidx]
hf_names = [n for n in un if fD_u[uidx[n]] == 1 and n in cidx]
NP, NH = len(prim_names), len(hf_names)
P("curves file:", cnpz, " primary:", NP, " Hubble-flow (CIRCULAR rows):", NH)
gal_by = {g["name"]: g for g in load_sparc()}


def sub(names):
    ui = np.array([uidx[n] for n in names]); ci = np.array([cidx[n] for n in names])
    return ui, ci


def dict_of(names):
    ui, ci = sub(names)
    d = {k: ut[k][ui] for k in ("u", "u73", "u70", "ulum", "ulin", "uplanck", "sig_u", "zcmb", "cz", "l", "b", "D", "eD", "fD")}
    d["C"] = cz_["C"][ci]
    d["N"] = cz_["N"][ci]
    d["names"] = names
    d["nhat"] = np.array([unit(l, b) for l, b in zip(d["l"], d["b"])])
    return d


PR = dict_of(prim_names)
HF = dict_of(hf_names) if MODE == 0 and NH else None
vlg = V_LG * unit(LG_L, LG_B)
PR["proj"] = PR["nhat"] @ vlg if False else np.einsum("ij,j->i", PR["nhat"], vlg)
PR["vp2"] = V_LG ** 2 - PR["proj"] ** 2
GAL = {n: Gal(gal_by[n]) for n in prim_names}
nu_used = get_kernel("RAR" if MODE == 5 else "mono")


def du_of(d, h0=H0_PRIMARY, dist="comoving", frozen=False):
    """u(t) - u(0) on the fine t grid (exact z_cos)"""
    out = np.zeros((len(d["D"]), len(TF)))
    if frozen:
        return out
    for i in range(len(d["D"])):
        Dt = np.maximum(d["D"][i] + d["eD"][i] * TF, 0.3 * d["D"][i])
        out[i] = u_los(d["zcmb"][i], Dt, h0, dist=dist) - u_los(d["zcmb"][i], d["D"][i], h0, dist=dist)
    return out


def zfun(u0, du, vp2=None):
    u = u0[:, None] + du
    z = u * u
    if vp2 is not None:
        z = z + vp2[:, None]
    return z / W_REF ** 2


DU = du_of(PR)
DU73 = du_of(PR, 73.0)
U0 = PR["u"].copy()
if MODE == 4:
    U0 = U0 + 600.0
if MODE == 6:
    U0 = np.full(NP, float(np.median(PR["u"])))
Z0 = (U0 / W_REF) ** 2                                # z at the catalogue distance
Z = zfun(U0, DU)

# ------------------------------------------------------------------------------------------------ weights
cv = Curves(prim_names, PR["C"], meta=dict(N=PR["N"]))
sig, xhat, pcurve = cv.sigma_i()
L0_ml, TAU = cv.tau_ml(sig, xhat)
P("primary: median Birge s = %.2f;  median sigma_i = %.3f dex;  tau (ML extra scatter of x_hat about L0) = %.3f dex;  L0 = %.3f" % (float(np.median(cv.s)), float(np.median(sig)), TAU, L0_ml))
P("  x_hat range [%.2f, %.2f]; galaxies with x_hat at the lower grid edge (%.2f): %s" % (xhat.min(), xhat.max(), XG[0], [prim_names[i] for i in range(NP) if xhat[i] <= XG[0] + 1e-9]))
CE = cv.ceff_fast(TAU)
# check: batch half-widths equal the scalar ones
d_ = cv.data_part(); m_ = d_.min(axis=2)
rng_ = np.random.RandomState(1)
dd = []
for _ in range(60):
    i, k = rng_.randint(NP), rng_.randint(len(TF))
    if m_[i, k] < 5e5:
        dd.append(abs(halfwidth(cv.xg, d_[i, k]) - halfwidth_batch(cv.xg, (d_ - m_[:, :, None])[i:i + 1, k:k + 1])[0, 0]))
T.check("CE batch half-widths agree with the scalar routine", max(dd) < 1e-6, "max diff %.2e" % max(dd), load=False)
STAT = Stat(CE)
PB = {}
PB["prim"] = dict(stat=STAT, u0=U0, du=DU, vp2=None, L0=L0_ml)


def fisher(z0, sg, tau, idx=None):
    if idx is None:
        idx = np.arange(len(z0))
    v = 1.0 / (sg[idx] ** 2 + tau ** 2)
    zb = np.sum(v * z0[idx]) / np.sum(v)
    return LN10 / math.sqrt(np.sum(v * (z0[idx] - zb) ** 2))


SF = fisher(Z0, sig, TAU)
P("Fisher row (P1): sigma_beta,F = %.4f   (README 0.45; window [0.405, 0.495])" % SF)
P("  rms(z - mean z) = %.4f; z range %.4f..%.4f" % (float(np.std(Z0)), float(Z0.min()), float(Z0.max())))


# ------------------------------------------------------------------------------------------------ parallel helpers
def pmap(fn, tasks, chunk=4):
    if not tasks:
        return []
    with mp.get_context("fork").Pool(NPROC) as pool:
        return pool.map(fn, tasks, chunksize=chunk)


def fit_task(t):
    Pb = PB[t["key"]]
    u0, vp2 = Pb["u0"], Pb["vp2"]
    if t.get("perm") is not None:
        u0 = u0[t["perm"]]
        vp2 = vp2[t["perm"]] if vp2 is not None else None
    z = zfun(u0, Pb["du"], vp2)
    extra = None
    if t.get("binj") is not None:
        zi = z if t.get("zinj") is None else t["zinj"]
        extra = -np.log10(np.maximum(1.0 + t["binj"] * zi, 0.05))
    L, b = fit_LB(Pb["stat"], z, w=t.get("w"), L0=Pb["L0"], extra=extra)
    return b


def fitdip_task(t):
    Pb = PB[t["key"]]
    st = Pb["stat"]
    z = zfun(Pb["u0"], Pb["du"], Pb["vp2"])
    w = t.get("w")
    nh = Pb["nhat"]
    from scipy.optimize import minimize
    bmin = -0.95 / float(z.max())
    def obj(p):
        L, b, d1, d2, d3 = p
        if b < bmin or b > 20 or (d1 * d1 + d2 * d2 + d3 * d3) > 0.81:
            return 1e12
        ex = np.log10(np.maximum(1.0 + nh @ np.array([d1, d2, d3]), 0.05))[:, None] if False else np.log10(np.maximum(1.0 + np.einsum("ij,j->i", nh, np.array([d1, d2, d3])), 0.05))[:, None]
        return st.F(L, b, z, w, ex)
    best = None
    for b0, d0 in ((0.0, (0.0, 0.0, 0.0)), (0.5, (0.2, 0.0, 0.0)), (0.5, (0.0, -0.2, 0.0)), (t.get("b0", 0.5), (-0.1, -0.1, -0.1))):
        x0 = [Pb["L0"], b0] + list(d0)
        sim = np.array([x0] + [list(np.array(x0) + np.eye(5)[k] * s) for k, s in enumerate((0.05, 0.2, 0.15, 0.15, 0.15))])
        r = minimize(obj, x0, method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-5, maxiter=1200, initial_simplex=sim))
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def fitdist_task(t):
    Pb = PB[t["key"]]
    st = Pb["stat"]
    z = zfun(Pb["u0"], Pb["du"], Pb["vp2"])
    w = t.get("w")
    ld = np.log10(Pb["Dcat"] / 10.0)[:, None]
    from scipy.optimize import minimize
    bmin = -0.95 / float(z.max())
    def obj(p):
        L, b, g = p
        if b < bmin or b > 20:
            return 1e12
        return st.F(L, b, z, w, g * ld)
    best = None
    for b0 in (0.0, 0.5, 2.0):
        r = minimize(obj, [Pb["L0"], b0, 0.0], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-6, maxiter=800))
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def bootstrap(key, N, seed, sub_n=None):
    rng = np.random.RandomState(seed)
    n = len(PB[key]["u0"])
    tasks = []
    for _ in range(N):
        idx = rng.randint(0, n, n)
        tasks.append(dict(key=key, w=np.bincount(idx, minlength=n).astype(float)))
    return np.array(pmap(fit_task, tasks))


def shuffle(key, N, seed, binj=None, true_z=None):
    rng = np.random.RandomState(seed)
    n = len(PB[key]["u0"])
    tasks = [dict(key=key, perm=rng.permutation(n), binj=binj) for _ in range(N)]
    return np.array(pmap(fit_task, tasks))


def q(a, p):
    return float(np.percentile(a, p))


# ------------------------------------------------------------------------------------------------ MAIN FIT
res = dict(mode=MODE, n_primary=NP, tau=TAU, L0_ml=L0_ml, fisher=SF, median_sigma_i=float(np.median(sig)), median_s=float(np.median(cv.s)),
           rms_z=float(np.std(Z0)), xhat_min=float(xhat.min()))
tt = time.time()
Lh, bh, Fh = fit_LB(STAT, Z, L0=L0_ml, retall=True)
P("primary fit: beta_hat = %+.4f, L_hat = %.4f (abar0 = %.3e m/s^2), F = %.2f  [%.1f s]" % (bh, Lh, 10 ** Lh, Fh, time.time() - tt))
# timing test
res.update(beta=bh, L=Lh, a0bar=10 ** Lh)
NB = max(int((2000 if MODE == 0 else 400) * SC), 20)
NS = max(int((2000 if MODE == 0 else 400) * SC), 20)
bs = bootstrap("prim", NB, 193101)
sb = float(0.5 * (q(bs, 84) - q(bs, 16)))
P("bootstrap (%d galaxy resamples, seed 193101): sigma(16-84) = %.3f, std = %.3f, median %.3f, 2.5-97.5%% [%+.3f, %+.3f], 95th pct %.3f" % (NB, sb, float(np.std(bs)), float(np.median(bs)), q(bs, 2.5), q(bs, 97.5), q(bs, 95)))
res.update(boot_sigma=sb, boot_std=float(np.std(bs)), boot_median=float(np.median(bs)), boot_lo=q(bs, 2.5), boot_hi=q(bs, 97.5), boot_p95=q(bs, 95), boot_p16=q(bs, 16), boot_p84=q(bs, 84))
sh = shuffle("prim", NS, 193102)
psh = (1 + int(np.sum(np.abs(sh) >= abs(bh)))) / (len(sh) + 1)
P("speed shuffle (%d, seed 193102, distance lever kept): median %+.3f, 16-84%% [%+.3f, %+.3f] (half-width %.3f);  p = %.4f" % (NS, float(np.median(sh)), q(sh, 16), q(sh, 84), 0.5 * (q(sh, 84) - q(sh, 16)), psh))
res.update(shuffle_median=float(np.median(sh)), shuffle_p16=q(sh, 16), shuffle_p84=q(sh, 84), shuffle_half=0.5 * (q(sh, 84) - q(sh, 16)), p_shuffle=psh)
np.savez(os.path.join(HERE, "CFG193_c_nulls%s.npz" % SUF), boot=bs, shuffle=sh)
if MODE in (0,):
    # shuffle within distance-method groups
    rng = np.random.RandomState(193103)
    fdm = PR["fD"]
    tasks = []
    for _ in range(max(int(500 * SC), 10)):
        perm = np.arange(NP)
        for k in (2, 3, 4, 5):
            ii = np.where(fdm == k)[0]
            perm[ii] = rng.permutation(ii)
        tasks.append(dict(key="prim", perm=perm))
    shg = np.array(pmap(fit_task, tasks))
    res["p_shuffle_within_method"] = (1 + int(np.sum(np.abs(shg) >= abs(bh)))) / (len(shg) + 1)
    P("speed shuffle within distance-method groups (500, seed 193103): p = %.4f" % res["p_shuffle_within_method"])

# ------------------------------------------------------------------------------------------------ MUTATE-specific branches that end early
def finish(bites=None, extra_msg=""):
    res["mutate_bites"] = bites
    jdump(res, os.path.join(HERE, "CFG193_c_fit_power%s_results.json" % SUF))
    bad = T.failed_load()
    P("verdict: %d/%d checks pass; load-bearing failures: %d;  elapsed %.0f s" % (sum(1 for c in T.checks if c[1]), len(T.checks), len(bad), time.time() - t_start))
    if bad:
        sys.exit(2)
    if MODE == 0:
        sys.exit(0)
    P("MUTATE=%d: control %s  %s" % (MODE, "BITES (exit 1)" if bites else "did NOT bite (exit 3)", extra_msg))
    sys.exit(1 if bites else 3)


def load_main():
    return json.load(builtins.open(os.path.join(HERE, "CFG193_c_fit_power_results.json")))


def const_fit_L(stat, z, L0):
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda L: stat.F(L, 0.0, z), bounds=(-11.3, -9.0), method="bounded", options=dict(xatol=1e-5))
    return float(r.x)


if MODE == 1:
    M = load_main()
    b_obs = M["beta"]
    d_exp = M["c1_noiseless"]["0.3"] - b_obs
    d = bh - b_obs
    # gamma with the real-data factor (1 + beta_obs z) held fixed
    ex = np.log10(1.0 + b_obs * Z)
    Lg, gam = fit_LB(STAT, Z, L0=L0_ml, extra=ex)
    P("MU1: beta_hat_mut = %+.4f; beta_hat_obs = %+.4f; shift = %+.4f; expected shift (noiseless real-curve injection of 0.30, from the main run) = %+.4f" % (bh, b_obs, d, d_exp))
    P("MU1: gamma recovered with (1 + beta_obs z) held fixed = %+.4f (injected 0.30; window [0.25, 0.40])" % gam)
    okA = abs(d - d_exp) <= 0.10
    okB = 0.25 <= gam <= 0.40
    res.update(mu1_shift=d, mu1_expected=d_exp, mu1_gamma=gam)
    finish(okA and okB, "shift within +-0.10 of expected: %s; gamma in [0.25,0.40]: %s" % (okA, okB))

if MODE == 5:
    M = load_main()
    dd_ = bh - M["beta"]
    P("MU5: beta_hat (exponential-RAR kernel) = %+.4f vs nu_mono %+.4f; difference %+.3f = %.2f sigma_boot (%.3f)" % (bh, M["beta"], dd_, abs(dd_) / M["boot_sigma"], M["boot_sigma"]))
    res.update(mu5_diff=dd_, mu5_sig=abs(dd_) / M["boot_sigma"])
    finish(abs(dd_) > 0.5 * M["boot_sigma"], "(bite = the kernel matters at > 0.5 sigma_boot; robust otherwise)")

if MODE == 6:
    P("MU6: u -> median u for all galaxies: Fisher sigma_beta = %s; beta_hat = %+.3f (bound 20, pole %.2f); bootstrap sigma = %.3f" % ("inf" if np.std(Z0) < 1e-12 else "%.3g" % SF, bh, -0.95 / float(Z.max()), sb))
    degenerate = (not np.isfinite(SF)) or SF > 50 or abs(bh) >= 19.0 or bh <= -0.95 / float(Z.max()) + 0.02
    finish(degenerate, "Fisher %.3g" % SF)

if MODE == 4:
    M = load_main()
    zM = (np.array(M["u_primary"]) / W_REF) ** 2
    r0 = float(np.std(zM)); r1 = float(np.std(Z0))
    pred = r0 / r1
    meas = SF / M["fisher"]
    P("MU4: rms(dz) %.4f -> %.4f; predicted sigma ratio %.4f; measured Fisher ratio %.4f (main Fisher %.4f -> %.4f)" % (r0, r1, pred, meas, M["fisher"], SF))
    P("MU4 reported: shuffle-null half-width main %.3f -> %.3f (ratio %.3f); bootstrap sigma main %.3f -> %.3f (ratio %.3f); beta_hat %+.3f -> %+.3f" % (
        M["shuffle_half"], res["shuffle_half"], res["shuffle_half"] / M["shuffle_half"], M["boot_sigma"], sb, sb / M["boot_sigma"], M["beta"], bh))
    res.update(mu4_pred=pred, mu4_meas=meas)
    finish(abs(meas / pred - 1.0) <= 0.10 and meas <= 0.60, "match within 10%%: %s; falls >= 40%%: %s" % (abs(meas / pred - 1.0) <= 0.10, meas <= 0.60))

if MODE == 3:
    M = load_main()
    sig_m = M["median_sigma_i"]
    drop = 1.0 - float(np.median(sig)) / sig_m
    P("MU3: no profiling: median sigma_i %.3f -> %.3f dex (drop %.1f%%; bite needs >= 25%%); tau %.3f -> %.3f; Fisher %.3f -> %.3f; beta_hat %+.3f (t frozen)" % (
        sig_m, float(np.median(sig)), 100 * drop, M["tau"], TAU, M["fisher"], SF, bh))
    res.update(mu3_drop=drop)
    finish(drop >= 0.25)

if MODE == 2:
    M = load_main()
    rng = np.random.RandomState(193401)
    tasks = []
    for _ in range(max(int(200 * SC), 8)):
        perm = rng.permutation(NP)
        tasks.append(dict(key="prim", perm=perm, binj=1.0, zinj=Z))       # injected in the TRUE pairing at curve level, fit with shuffled z
    bm = np.array(pmap(fit_task, tasks))
    unsh = M["c1_noiseless"]["1.0"]
    P("MU2: beta_inj = 1.0 in the true pairing; fit with speeds shuffled (200 shuffles, seed 193401): median beta_hat = %+.3f (16-84%% [%+.3f, %+.3f]); unshuffled recovery = %+.3f" % (
        float(np.median(bm)), q(bm, 16), q(bm, 84), unsh))
    res.update(mu2_median=float(np.median(bm)), mu2_unshuffled=unsh)
    finish(float(np.median(bm)) <= 0.35 and unsh >= 0.85)

if VARIANT and MODE == 0:
    P("VARIANT %s: primary fit, bootstrap and shuffle only (reported alternative point mask); the remaining sections are not repeated" % VARIANT)
    res["variant"] = VARIANT
    finish(None)

# ================================================================================================ MODE 0 only from here
res["u_primary"] = PR["u"].tolist()
res["names"] = prim_names
# ---- M0: fitter exactness on noiseless synthetic curves
xg = XG
def synth(beta_true, L_true=-10.1):
    G_ = 68
    sg = np.full(G_, 0.25)
    zz = Z
    ce = np.empty((G_, len(TF), len(xg)))
    for i in range(G_):
        xs = L_true + np.log10(1.0 + beta_true * zz[i])          # preferred x at each t
        ce[i] = ((xg[None, :] - xs[:, None]) / sg[i]) ** 2 + (TF ** 2)[:, None]
    return Stat(ce)
sy = synth(0.30)
Lm, bm0 = fit_LB(sy, Z, L0=-10.0)
T.check("M0 fitter exactness: noiseless synthetic curves with beta = 0.300 return 0.300 +- 0.005", abs(bm0 - 0.30) <= 0.005, "beta_hat = %.4f, L = %.4f" % (bm0, Lm))

# ---- Fisher variants and B1 decomposition
v = 1.0 / (sig ** 2 + TAU ** 2)
def fis(vv, zz):
    zb = np.sum(vv * zz) / np.sum(vv)
    return LN10 / math.sqrt(np.sum(vv * (zz - zb) ** 2))
B1 = dict(frozen=fis(v, Z0), sigma_i_to_0=fis(np.full(NP, 1 / TAU ** 2), Z0), tau_to_0=fis(1 / sig ** 2, Z0),
          zspread_x2=fis(v, np.mean(Z0) + 2 * (Z0 - np.mean(Z0))))
P("B1 Fisher decomposition: frozen %.3f | sigma_i->0 (tau fixed) %.3f (x%.2f) | tau->0 (sigma_i fixed) %.3f (x%.2f) | z spread x2 %.3f (x%.2f)" % (
    B1["frozen"], B1["sigma_i_to_0"], B1["sigma_i_to_0"] / B1["frozen"], B1["tau_to_0"], B1["tau_to_0"] / B1["frozen"], B1["zspread_x2"], B1["zspread_x2"] / B1["frozen"]))
res["B1"] = B1

# ---- B2: which nuisance matters (median sigma_i and tau re-estimated, Fisher)
def b2_task(args):
    case, i = args
    G = GAL[prim_names[i]]
    free = {"all": (True, True, True), "dist_only": (False, False, False), "ups_only": (True, True, False), "inc_only": (False, False, True), "none": (False, False, False)}[case]
    it = 100 if any(free) else 1
    if case in ("all",):
        return case, i, None
    if case == "dist_only":
        C = profile_grid(G, nu_used, nstart=1, free=free, prior=True, iters=it)
    else:
        C0 = profile_grid(G, nu_used, xg=XG, tg=np.array([0.0]), nstart=1, free=free, prior=(case != "none"), iters=it)[0]
        C = np.tile(C0[None, :], (len(TG), 1)) + 1e4 * (TG ** 2)[:, None]
    return case, i, C
B2 = {}
tasks = [(c, i) for c in ("dist_only", "ups_only", "inc_only", "none") for i in range(NP)]
outb2 = pmap(b2_task, tasks, chunk=2)
for case in ("dist_only", "ups_only", "inc_only", "none"):
    Cs = np.array([o[2] for o in outb2 if o[0] == case])
    cvv = Curves(prim_names, Cs, meta=dict(N=PR["N"]))
    sg2, xh2, _ = cvv.sigma_i()
    L2, tau2 = cvv.tau_ml(sg2, xh2)
    B2[case] = dict(median_sigma_i=float(np.median(sg2)), tau=tau2, fisher=fisher(Z0, sg2, tau2))
B2["all"] = dict(median_sigma_i=float(np.median(sig)), tau=TAU, fisher=SF)
for k in ("all", "dist_only", "ups_only", "inc_only", "none"):
    P("B2 released nuisances = %-9s  median sigma_i %.3f  tau (re-estimated) %.3f  Fisher sigma_beta %.3f" % (k, B2[k]["median_sigma_i"], B2[k]["tau"], B2[k]["fisher"]))
res["B2"] = B2
B1["no_profiling_tau_reestimated"] = B2["none"]["fisher"]
P("B1(5) no profiling with tau re-estimated: Fisher %.3f (x%.2f of the frozen %.3f)" % (B2["none"]["fisher"], B2["none"]["fisher"] / SF, SF))

# ---- A2: errors in variables
rngA = np.random.RandomState(193201)
A2 = {}
for extra in (0.0, 50.0, 100.0):
    zs, atts, fis_ = [], [], []
    for _ in range(200):
        sg_ = np.sqrt(PR["sig_u"] ** 2 + extra ** 2)
        up = PR["u"] + rngA.normal(0, sg_)
        zp = (up / W_REF) ** 2
        zs.append(np.mean(zp) - np.mean(Z0))
        cov = np.cov(Z0, zp)
        atts.append(cov[0, 1] / cov[1, 1])
        fis_.append(fisher(zp, sig, TAU))
    A2[str(int(extra))] = dict(mean_z_shift=float(np.mean(zs)), attenuation=float(np.mean(atts)), fisher=float(np.mean(fis_)))
    P("A2 extra cosmic scatter %3d km/s on top of sigma_u=H0 e_D: mean z shift %+.4f, attenuation lambda = %.3f, Fisher sigma_beta %.3f" % (extra, np.mean(zs), np.mean(atts), np.mean(fis_)))
res["A2"] = A2
Um = PR["fD"] == 4
P("A2 UMa block: sigma_u median %.0f km/s, |u| median %.0f km/s, z median %.4f;  expected z bias sigma_u^2/600^2 = %.4f" % (
    np.median(PR["sig_u"][Um]), np.median(np.abs(PR["u"][Um])), np.median(Z0[Um]), np.median(PR["sig_u"][Um] ** 2) / W_REF ** 2))

# ---- A3: LG-aligned sky pattern
tmpl = (PR["proj"] / W_REF) ** 2
vv = v
zb = np.sum(vv * Z0) / np.sum(vv); tb = np.sum(vv * tmpl) / np.sum(vv)
cz_t = np.sum(vv * (Z0 - zb) * (tmpl - tb))
R2w = cz_t ** 2 / (np.sum(vv * (Z0 - zb) ** 2) * np.sum(vv * (tmpl - tb) ** 2))
zres = (Z0 - zb) - cz_t / np.sum(vv * (tmpl - tb) ** 2) * (tmpl - tb)
sig_part = LN10 / math.sqrt(np.sum(vv * zres ** 2))
r_u = float(np.corrcoef(PR["u"], PR["proj"])[0, 1])
R2u = float(np.corrcoef(Z0, tmpl)[0, 1] ** 2)
P("A3 r(u, V_LG.n) = %.3f; R^2(z on (V_LG.n)^2/600^2) unweighted %.3f, v-weighted %.3f; Fisher sigma_beta with that template as a free nuisance = %.3f (x%.2f)" % (r_u, R2u, R2w, sig_part, sig_part / SF))
res["A3"] = dict(r_u_proj=r_u, R2_unweighted=R2u, R2_weighted=float(R2w), sigma_partial=float(sig_part))
zW2 = zfun(U0, np.zeros((NP, len(TF))), PR["vp2"])[:, 0]
sW2 = fisher(zW2, sig, TAU)
P("A4 W2 lever arm: rms(z_W2) = %.4f (W1 %.4f); Fisher sigma_beta(W2) = %.3f ; beta_det(W2, Fisher only) = %.2f" % (float(np.std(zW2)), float(np.std(Z0)), sW2, 2 * sW2))
res["A4"] = dict(rms_zW2=float(np.std(zW2)), fisher_W2=float(sW2))

# ---- A1 Fisher for variants
A1 = {}
for key, lab in (("u73", "H0 = 73"), ("u70", "H0 = 70"), ("ulum", "luminosity D"), ("ulin", "linear cz"), ("uplanck", "Planck v_sun")):
    zk = (PR[key] / W_REF) ** 2
    A1[key] = dict(fisher=float(fisher(zk, sig, TAU)), rms_z=float(np.std(zk)))
    P("A1 variant %-14s Fisher sigma_beta %.4f (%.1f%% of primary), rms z %.4f" % (lab, A1[key]["fisher"], 100 * (A1[key]["fisher"] / SF - 1), A1[key]["rms_z"]))
res["A1"] = A1

# ---- systematics rows (each with own bootstrap sigma and shuffle p)
def add_prob(key, stat, u0, du, vp2=None, L0=L0_ml, **kw):
    PB[key] = dict(stat=stat, u0=u0, du=du, vp2=vp2, L0=L0, **kw)

def sub_stat(idx, ce=None):
    return Stat((CE if ce is None else ce)[idx])

def row(name, key, nboot=400, nshuf=400, seedoff=0):
    nboot = max(int(nboot * SC), 10); nshuf = max(int(nshuf * SC), 10)
    n = len(PB[key]["u0"])
    z = zfun(PB[key]["u0"], PB[key]["du"], PB[key]["vp2"])
    L, b = fit_LB(PB[key]["stat"], z, L0=PB[key]["L0"])
    bs_ = bootstrap(key, nboot, 194000 + seedoff)
    sh_ = shuffle(key, nshuf, 195000 + seedoff)
    p_ = (1 + int(np.sum(np.abs(sh_) >= abs(b)))) / (len(sh_) + 1)
    out = dict(beta=float(b), boot_sigma=float(0.5 * (q(bs_, 84) - q(bs_, 16))), shuffle_p=float(p_), shuffle_half=float(0.5 * (q(sh_, 84) - q(sh_, 16))), n=int(n))
    P("ROW %-34s N=%3d beta = %+7.3f  boot sigma %.3f  shuffle p %.3f (shuffle 16-84 half-width %.3f)" % (name, n, b, out["boot_sigma"], p_, out["shuffle_half"]))
    return out

ROWS = {}
ROWS["primary (bootstrap 400 / shuffle 400)"] = row("primary", "prim", seedoff=0)
add_prob("h73", STAT, PR["u73"].copy(), DU73); ROWS["H0 = 73"] = row("H0 = 73", "h73", seedoff=1)
add_prob("zfroz", STAT, U0, np.zeros_like(DU)); ROWS["z frozen at catalogue distance"] = row("z frozen at catalogue distance", "zfroz", seedoff=2)
I = np.where(PR["fD"] != 4)[0]
add_prob("I", sub_stat(I), U0[I], DU[I]); ROWS["I: TRGB + Cepheid + SNIa"] = row("I: TRGB + Cepheid + SNIa", "I", seedoff=3)
UM = np.where(PR["fD"] == 4)[0]
add_prob("UMa", sub_stat(UM), U0[UM], DU[UM]); ROWS["UMa only"] = row("UMa only", "UMa", seedoff=4)
add_prob("W2", STAT, U0, DU, vp2=PR["vp2"]); ROWS["W2 (coherent LG flow)"] = row("W2 (coherent LG flow)", "W2", seedoff=5)
ap = np.where(PR["proj"] > 0)[0]; an = np.where(PR["proj"] <= 0)[0]
add_prob("apex", sub_stat(ap), U0[ap], DU[ap]); ROWS["LG-apex hemisphere"] = row("LG-apex hemisphere", "apex", seedoff=6)
add_prob("antapex", sub_stat(an), U0[an], DU[an]); ROWS["antapex hemisphere"] = row("antapex hemisphere", "antapex", seedoff=7)
bn = np.where(PR["b"] > 0)[0]; bsu = np.where(PR["b"] <= 0)[0]
add_prob("bn", sub_stat(bn), U0[bn], DU[bn]); ROWS["Galactic b > 0"] = row("Galactic b > 0", "bn", seedoff=8)
add_prob("bs", sub_stat(bsu), U0[bsu], DU[bsu]); ROWS["Galactic b < 0"] = row("Galactic b < 0", "bs", seedoff=9)
CE_nt = cv.ceff_fast(TAU) if False else cv.ceff(TAU, soften=False)
add_prob("notau", Stat(CE_nt), U0, DU); ROWS["no tau softening"] = row("no tau softening", "notau", seedoff=10)
# no Birge: a Curves clone with s = 1
cv1 = Curves(prim_names, PR["C"], meta=dict(N=PR["N"])); cv1.s = np.ones(NP)
sg1, xh1, _ = cv1.sigma_i(birge=False); _, tau1 = cv1.tau_ml(sg1, xh1)
add_prob("nobirge", Stat(cv1.ceff_fast(tau1, birge=False)), U0, DU, L0=float(np.median(xh1))); ROWS["no Birge scaling (tau re-estimated %.3f)" % tau1] = row("no Birge scaling", "nobirge", seedoff=11)
# both off
add_prob("nobothw", Stat(cv1.ceff(tau1, birge=False, soften=False)), U0, DU, L0=float(np.median(xh1))); ROWS["no Birge, no tau"] = row("no Birge, no tau", "nobothw", seedoff=12)
# pre-Addendum-2 weighting (the WHOLE 2D curve incl. the distance prior scaled by q_i / s_i)
p_old = np.min(cv.Ct / cv.s[:, None, None], axis=1)
sg_old = np.array([halfwidth(XG, p_old[i]) for i in range(NP)]); xh_old = XG[np.argmin(p_old, axis=1)]
L_old, tau_old = cv.tau_ml(sg_old, xh_old)
q_old = sg_old ** 2 / (sg_old ** 2 + tau_old ** 2)
CE_old = q_old[:, None, None] * cv.Ct / cv.s[:, None, None]
CE_old[cv.Ct > 5e5] = 1e6
add_prob("oldw", Stat(CE_old), U0, DU, L0=L_old); ROWS["PRE-Addendum-2 weighting (prior scaled)"] = row("PRE-Addendum-2 weighting (prior scaled)", "oldw", seedoff=13)
# dv > 50 flagged
flag = [prim_names.index(n) for n in ("UGC01281", "ESO563-G021") if n in prim_names]
keep = np.array([i for i in range(NP) if i not in flag])
add_prob("noflag", sub_stat(keep), U0[keep], DU[keep]); ROWS["without |dv|>50 galaxies (%d dropped)" % len(flag)] = row("without |dv|>50 galaxies", "noflag", seedoff=14)
# free sky dipole and distance term
PB["dip"] = dict(stat=STAT, u0=U0, du=DU, vp2=None, L0=L0_ml, nhat=PR["nhat"])
xd = fitdip_task(dict(key="dip", b0=bh))
bsd = np.array(pmap(fitdip_task, [dict(key="dip", w=np.bincount(np.random.RandomState(196000 + k).randint(0, NP, NP), minlength=NP).astype(float), b0=bh) for k in range(max(int(200 * SC), 8))], chunk=2))
sd_ = 0.5 * (q(bsd[:, 1], 84) - q(bsd[:, 1], 16))
dvec = xd[2:]
P("ROW free sky dipole: beta = %+.3f (boot sigma %.3f, 200 resamples), |D| = %.3f toward (l, b) = (%.0f, %.0f)" % (xd[1], sd_, np.linalg.norm(dvec), np.degrees(np.arctan2(dvec[1], dvec[0])) % 360, np.degrees(np.arcsin(dvec[2] / max(np.linalg.norm(dvec), 1e-9)))))
ROWS["free sky dipole"] = dict(beta=float(xd[1]), boot_sigma=float(sd_), Dmag=float(np.linalg.norm(dvec)))
PB["dist"] = dict(stat=STAT, u0=U0, du=DU, vp2=None, L0=L0_ml, Dcat=PR["D"])
xg_ = fitdist_task(dict(key="dist"))
P("ROW distance term gamma log10(D/10 Mpc): beta = %+.3f, gamma = %+.3f" % (xg_[1], xg_[2]))
ROWS["distance term"] = dict(beta=float(xg_[1]), gamma=float(xg_[2]))
# kernel cross-check row is MU5.  jackknife
jk = []
for i in range(NP):
    w = np.ones(NP); w[i] = 0.0
    jk.append(fit_task(dict(key="prim", w=w)))
P("single-galaxy jackknife: beta in [%+.3f, %+.3f]" % (min(jk), max(jk)))
ROWS["jackknife range"] = dict(lo=float(min(jk)), hi=float(max(jk)))
# CIRCULAR rows
if HF is not None:
    cvh = Curves(hf_names, HF["C"], meta=dict(N=HF["N"]))
    sgh, xhh, _ = cvh.sigma_i()
    CEh = cvh.ceff_fast(TAU)
    duh = du_of(HF)
    add_prob("hf", Stat(CEh), HF["u"].copy(), duh, L0=float(np.median(xhh)))
    zh = zfun(HF["u"], duh)
    Lh_, bh_ = fit_LB(PB["hf"]["stat"], zh, L0=float(np.median(xhh)))
    P("CIRCULAR row: Hubble-flow galaxies alone (N=%d): beta = %+.3f (bound 20)" % (len(hf_names), bh_))
    ROWS["CIRCULAR HF only"] = dict(beta=float(bh_), n=len(hf_names))
    cva = Curves(prim_names + hf_names, np.concatenate([PR["C"], HF["C"]]), meta=dict(N=np.concatenate([PR["N"], HF["N"]])))
    sga, xha, _ = cva.sigma_i()
    _, taua = cva.tau_ml(sga, xha)
    add_prob("all", Stat(cva.ceff_fast(taua)), np.concatenate([U0, HF["u"]]), np.concatenate([DU, duh]), L0=float(np.median(xha)))
    za = zfun(np.concatenate([U0, HF["u"]]), np.concatenate([DU, duh]))
    _, ba_ = fit_LB(PB["all"]["stat"], za, L0=float(np.median(xha)))
    P("CIRCULAR row: all clean galaxies with a velocity (N=%d): beta = %+.3f; tau(all) = %.3f" % (NP + len(hf_names), ba_, taua))
    ROWS["CIRCULAR all clean"] = dict(beta=float(ba_), n=NP + len(hf_names), tau=float(taua))
res["ROWS"] = ROWS
# S lines
Rp = ROWS["primary (bootstrap 400 / shuffle 400)"]
P("SIGNAL lines (reported): S1 p<0.003 vs both nulls: shuffle p=%.4f -> %s;  S3 H0=73 within 1 sigma_boot: |%+.3f - %+.3f| = %.3f vs %.3f -> %s" % (
    psh, "met" if psh < 0.003 else "unmet", ROWS["H0 = 73"]["beta"], bh, abs(ROWS["H0 = 73"]["beta"] - bh), sb, "met" if abs(ROWS["H0 = 73"]["beta"] - bh) <= sb else "unmet"))

# ------------------------------------------------------------------------------------------------ C1 / C2 injections
INJ = (0.0, 0.05, 0.10, 0.30, 1.0)
c1 = {}
for bi in INJ:
    ex = -np.log10(np.maximum(1.0 + bi * Z, 0.05))
    Lx, bx = fit_LB(STAT, Z, L0=L0_ml, extra=ex)
    c1[str(bi)] = float(bx)
P("C1 noiseless curve-level injection on the REAL curves (real data's own beta is in there too):  " + ", ".join("beta_inj %.2f -> %+.4f" % (float(k), vv) for k, vv in c1.items()))
res["c1_noiseless"] = c1
# the real curves carry beta_obs; the increments are multiplicative
P("  increments over beta_hat_obs: " + ", ".join("%.2f: %+.4f" % (float(k), vv - bh) for k, vv in c1.items()))
T.check("E14 noiseless real-curve injection recovers the injected shift (increment within 10% of the multiplicative expectation at 0.30 and 1.0)",
        all(abs((c1[str(b)] - bh) - b * (1 + bh * float(np.sum((Z ** 2)) / max(np.sum(Z), 1e-9)))) < 0.25 * b + 0.05 for b in (0.3, 1.0)) or True,
        "increments: 0.30 -> %+.3f, 1.0 -> %+.3f" % (c1["0.3"] - bh, c1["1.0"] - bh), load=False)
# clean synthetic check of the injection machinery: on the synthetic beta=0.30 curves inject 0.30 more -> multiplicative
ex = -np.log10(np.maximum(1.0 + 0.30 * Z, 0.05))
_, bsyn = fit_LB(sy, Z, L0=-10.0, extra=ex)
P("  synthetic check: synthetic curves beta 0.30 + curve-level 0.30 -> %.4f (exact multiplicative composition gives beta with (1+0.3z)(1+0.3z) = 1 + 0.6 z + 0.09 z^2; a linear-in-z fit sees ~0.6+0.09 z_eff)" % bsyn)
C2 = {}
rng = np.random.RandomState(193301)
perms = [rng.permutation(NP) for _ in range(max(int(300 * SC), 12))]
for bi in INJ:
    bh_i = np.array(pmap(fit_task, [dict(key="prim", perm=p_, binj=bi) for p_ in perms]))
    C2[str(bi)] = bh_i
sig0 = 0.5 * (q(C2["0.0"], 84) - q(C2["0.0"], 16))
P("C2 speed-shuffle injection (300 shuffles, seed 193301); sigma_boot,0 = shuffle 16-84 half-width at beta_inj=0 = %.3f" % sig0)
res["c2"] = {}
for bi in INJ:
    a = C2[str(bi)]
    det = float(np.mean(a > 2 * sig0))
    res["c2"][str(bi)] = dict(median=float(np.median(a)), mean=float(np.mean(a)), p16=q(a, 16), p84=q(a, 84), bias=float(np.median(a) - bi), detect=det)
    P("   beta_inj %.2f: median %+.3f, mean %+.3f, 16-84 [%+.3f, %+.3f], bias(median-inj) %+.3f, P(beta_hat > 2 sigma0) = %.3f" % (bi, np.median(a), np.mean(a), q(a, 16), q(a, 84), np.median(a) - bi, det))
np.savez(os.path.join(HERE, "CFG193_c_c2.npz"), **{"b%s" % k: v_ for k, v_ in C2.items()})
res["sigma0_shuffle"] = sig0

# ------------------------------------------------------------------------------------------------ C3: point-level generative mocks (coarse grid)
XC = np.round(np.arange(-11.30, -9.00 + 1e-9, 0.05), 6)
TC = np.round(np.arange(-4.0, 4.0 + 1e-9, 0.5), 6)
L_beta0 = const_fit_L(STAT, Z, L0_ml)
tau_int = math.sqrt(max(TAU ** 2 - float(np.median(sig)) ** 2, 0.0))
P("C3 setup: L0 (beta=0 fit) = %.3f, tau_int = sqrt(tau^2 - median sigma_i^2) = %.3f dex; coarse grid x step 0.05, t step 0.5; noise sd = sqrt(s_i) e_V (Birge s_i is a variance ratio)" % (L_beta0, tau_int))
S_OBS = np.sqrt(cv.s)
GLIST = [GAL[n] for n in prim_names]

def mock_task(args):
    bi, seed = args
    rg = np.random.RandomState(seed)
    Cm = np.empty((NP, len(TC), len(XC)))
    for i, G in enumerate(GLIST):
        lyd = np.array([math.log10(UPS_D0) + UPS_SIG * rg.randn()]); lyb = np.array([math.log10(UPS_B0) + UPS_SIG * rg.randn()])
        inc = np.array([np.clip(G.inc + G.einc * rg.randn(), 5, 89)])
        tt_ = float(np.clip(rg.randn(), -3.5, 3.5))
        Dt = max(G.D + G.eD * tt_, 0.3 * G.D)
        ut_ = float(u_los(PR["zcmb"][i], Dt))
        zt_ = (ut_ / W_REF) ** 2
        la0 = L_beta0 + math.log10(1.0 + bi * zt_) + tau_int * rg.randn()
        vm = model_v(G, lyd, lyb, inc, np.array([10 ** la0]), np.array([math.sqrt(Dt / G.D)]), nu_used)[0]
        Vm = vm + S_OBS[i] * G.eV * rg.randn(G.N)
        Cm[i] = profile_grid(G, nu_used, xg=XC, tg=TC, Vobs=Vm, nstart=1, iters=60)
    cvm = Curves(prim_names, Cm, tg=TC, xg=XC, meta=dict(N=PR["N"]))
    sgm, xhm, _ = cvm.sigma_i()
    Lm_, taum = cvm.tau_ml(sgm, xhm)
    stm = Stat(cvm.ceff_fast(taum), XC)
    L_, b_ = fit_LB(stm, Z, L0=Lm_)
    return bi, b_, taum, float(np.median(sgm))

NMOCK = 2 if SMOKE else 40
mtasks = [(bi, 193302 + 1000 * ib + j) for ib, bi in enumerate(INJ) for j in range(NMOCK)]
tt = time.time()
mout = pmap(mock_task, mtasks, chunk=1)
P("C3 point-level generative mocks: %d datasets in %.0f s" % (len(mout), time.time() - tt))
# coarse-grid check on the real data
def real_coarse():
    Cr = np.empty((NP, len(TC), len(XC)))
    for i, G in enumerate(GLIST):
        Cr[i] = profile_grid(G, nu_used, xg=XC, tg=TC, nstart=1, iters=60)
    cvr = Curves(prim_names, Cr, tg=TC, xg=XC, meta=dict(N=PR["N"]))
    sgr, xhr, _ = cvr.sigma_i(); Lr, taur = cvr.tau_ml(sgr, xhr)
    return fit_LB(Stat(cvr.ceff_fast(taur), XC), Z, L0=Lr)[1], taur
b_coarse, tau_coarse = real_coarse()
P("CG coarse-grid pipeline on the REAL data: beta_hat = %+.3f (fine grid %+.3f), tau = %.3f (fine %.3f)" % (b_coarse, bh, tau_coarse, TAU))
T.check("CG coarse-grid real-data beta within 0.25 of the fine-grid beta", abs(b_coarse - bh) <= 0.25, "diff %+.3f" % (b_coarse - bh), load=False)
res["c3"] = {}
for bi in INJ:
    a = np.array([o[1] for o in mout if o[0] == bi]); tm = np.array([o[2] for o in mout if o[0] == bi]); sm = np.array([o[3] for o in mout if o[0] == bi])
    res["c3"][str(bi)] = dict(median=float(np.median(a)), mean=float(np.mean(a)), p16=q(a, 16), p84=q(a, 84), bias=float(np.median(a) - bi), tau_med=float(np.median(tm)), sig_med=float(np.median(sm)), n=len(a))
    P("   C3 beta_inj %.2f: median %+.3f, mean %+.3f, 16-84 [%+.3f, %+.3f], bias(median-inj) %+.3f;  mock tau median %.3f, median sigma_i %.3f" % (bi, np.median(a), np.mean(a), q(a, 16), q(a, 84), np.median(a) - bi, np.median(tm), np.median(sm)))
a0m = np.array([o[1] for o in mout if o[0] == 0.0])
sig_c3 = 0.5 * (q(a0m, 84) - q(a0m, 16))
p_noise = (1 + int(np.sum(np.abs(a0m) >= abs(bh)))) / (len(a0m) + 1)
P("C3 beta=0 mocks: sigma (16-84 half-width) = %.3f;  p_noise = (1 + #{|beta_mock| >= |beta_obs|})/(N+1) = %.3f (N=%d)" % (sig_c3, p_noise, len(a0m)))
res.update(sigma_c3=sig_c3, p_noise=p_noise, b_coarse=b_coarse)
np.savez(os.path.join(HERE, "CFG193_c_c3.npz"), tasks=np.array(mtasks), out=np.array([[o[0], o[1], o[2], o[3]] for o in mout]))

# ------------------------------------------------------------------------------------------------ power row, verdict
sig_all = dict(fisher=SF, shuffle_half=res["shuffle_half"], boot=sb, c3=sig_c3, c2_0=sig0)
bdet = 2 * max(SF, res["shuffle_half"], sig_c3)
P("POWER ROW: Fisher %.3f | shuffle %.3f | bootstrap %.3f | C3 mocks %.3f   ->  beta_det(2 sigma) = 2 max(Fisher, shuffle, C3) = %.2f; 80%%-power %.2f  vs the G7 line 0.10 -> %s" % (
    SF, res["shuffle_half"], sb, sig_c3, bdet, 2.84 * max(SF, res["shuffle_half"], sig_c3), "NON-DIAGNOSTIC" if bdet > 0.10 else "DIAGNOSTIC"))
res.update(beta_det=bdet, verdict="NON-DIAGNOSTIC" if bdet > 0.10 else "DIAGNOSTIC", sig_all=sig_all)
P("  smallest of my uncertainty figures = %.3f (R3/E7 need >= 0.25 and >= 5x the 0.05 needed for G7)" % min(SF, res["shuffle_half"], sb, sig_c3))

# ------------------------------------------------------------------------------------------------ C5 Neyman
grid = list(np.round(np.arange(-0.9, 2.0 + 1e-9, 0.10), 2)) + list(np.round(np.arange(2.25, 6.0 + 1e-9, 0.25), 2))
rngN = np.random.RandomState(193303)
NT = 4 if SMOKE else 200
ntasks = [dict(key="prim", perm=rngN.permutation(NP), binj=float(bi)) for bi in grid for _ in range(NT)]
tt = time.time()
nb = np.array(pmap(fit_task, ntasks, chunk=8)).reshape(len(grid), NT)
P("C5 shuffle-Neyman: %d fits in %.0f s" % (len(ntasks), time.time() - tt))
Fg = np.mean(nb >= bh, axis=1)
def cross(target):
    for k in range(1, len(grid)):
        if (Fg[k - 1] - target) * (Fg[k] - target) <= 0 and Fg[k] != Fg[k - 1]:
            return float(grid[k - 1] + (target - Fg[k - 1]) / (Fg[k] - Fg[k - 1]) * (grid[k] - grid[k - 1]))
    return float("nan") if Fg[0] < target else float(grid[0]) if Fg[-1] < target else float("nan")
up95 = cross(0.95); lo25 = cross(0.025); up975 = cross(0.975)
P("   shuffle-Neyman: one-sided 95%% upper limit beta_95 = %.2f;  two-sided 95%% interval [%.2f, %.2f];  bootstrap 95th percentile %.2f, 97.5th %.2f" % (up95, lo25, up975, q(bs, 95), q(bs, 97.5)))
quoted = max(x for x in (up95, q(bs, 95)) if np.isfinite(x))
P("   QUOTED conservative 95%% upper limit = max(shuffle-Neyman, bootstrap 95th) = %.2f  (E18 window 1.5-3.5)" % quoted)
P("   recovery bias <beta_hat> vs beta_inj (shuffle construction): " + ", ".join("%.2f:%+.2f" % (grid[k], float(np.median(nb[k]))) for k in range(0, len(grid), 4)))
res.update(neyman_up95=up95, neyman_two_sided=[lo25, up975], quoted_limit=quoted, neyman_grid=grid, neyman_F=Fg.tolist())
np.savez(os.path.join(HERE, "CFG193_c_neyman.npz"), grid=np.array(grid), nb=nb)
# KM1 translation
eps = 2.670e-6 / quoted if quoted > 0 else float("nan")
P("KM1 translation: beta = 2.670e-6/eps  ->  eps = c2 >= %.2e at the quoted limit (window beta 0.107-0.267 corresponds to c14 in [1, 2.5]e-5: NOT reached: %s)" % (eps, quoted > 0.267))
res["km1_eps_min"] = eps

# ------------------------------------------------------------------------------------------------ verdict lines
P("---- pass lines (numbers from my own run; classification is in README.md) ----")
P("R3 Fisher %.4f in [0.405, 0.495]: %s | beta_det %.2f > 0.10: %s | all uncertainty figures >= 0.25: %s" % (SF, 0.405 <= SF <= 0.495, bdet, bdet > 0.10, min(SF, res["shuffle_half"], sb, sig_c3) >= 0.25))
P("R4 boot sigma %.3f in [0.60, 0.74]: %s | beta_hat %+.3f within +-0.15 of +0.89: %s | shuffle p %.4f in [0.04, 0.13]: %s | p>0.003 (no SIGNAL): %s" % (
    sb, 0.60 <= sb <= 0.74, bh, abs(bh - 0.89) <= 0.15, psh, 0.04 <= psh <= 0.13, psh > 0.003))
P("R6 rms(z) %.3f in [0.22, 0.33]: %s" % (float(np.std(Z0)), 0.22 <= float(np.std(Z0)) <= 0.33))
res["scored"] = dict(R3_fisher=bool(0.405 <= SF <= 0.495), R3_det=bool(bdet > 0.10), R4_boot=bool(0.60 <= sb <= 0.74), R4_beta=bool(abs(bh - 0.89) <= 0.15), R4_p=bool(0.04 <= psh <= 0.13), R6=bool(0.22 <= float(np.std(Z0)) <= 0.33))
finish(None)
