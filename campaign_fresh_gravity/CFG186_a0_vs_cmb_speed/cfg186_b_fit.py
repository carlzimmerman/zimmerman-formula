#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG186 part B -- the speed dependence of SPARC's acceleration scale: a0_i = a0_bar (1 + beta (w_i/600 km/s)^2), fitted
with the distance shared between each rotation curve and its CMB-frame speed; nulls (speed shuffle, noise injection),
systematics, Neyman limits, the translation to KM1's khronon parameter (conditional on KM1's model), and G7.

Frozen question: FROZEN_QUESTION.md (with Addenda 1-3), written before this script.  Part A's power row is printed first.
MUTATE=1 reads part A's MUTATE curves (beta = 0.30 injected at the point level) and requires
beta_hat_mut - beta_hat_obs in [0.24, 0.36] (M1, load-bearing).

kappa = 1/2 stays FITTED; a0 is fitted (a0_bar free).  Run from the repository root (after part A, both modes; the
MUTATE run after the real run):
    python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_b_fit.py
    MUTATE=1 python3 campaign_fresh_gravity/CFG186_a0_vs_cmb_speed/cfg186_b_fit.py
"""
import os
import sys
import json
import math
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cfg186_common as C

R = C.Run("cfg186_b_fit")
P, check = R.P, R.check
P(__doc__.split("Frozen question")[0].strip())
P(f"mode: {'MUTATE (curves built from data with beta = 0.30 injected)' if C.MUTATE else 'REAL DATA'}")
NPROC = 14

# ============================================================================================ B0
R.banner("B0  THE POWER ROW (part A, computed before any beta fit) AND THE INPUTS")
ja = json.load(open(os.path.join(C.HERE, "cfg186_a_curves_power_results.json")))
pw = ja["numbers"]["power"]
POWER = ja["numbers"]["POWER_VERDICT"]
for k, v in pw.items():
    P(f"  {k:10s}: sigma_beta Fisher {v['sigma_fisher']:.3f}, mocks {v['sigma_mock']:.3f} -> beta_det(2 sigma) "
      f"{v['beta_det_2sigma']:.2f} vs the G7 line 0.10: {'DIAGNOSTIC' if v['diagnostic'] else 'NON-DIAGNOSTIC'}")
P(f"  POWER VERDICT (declared before the fit): {POWER}")
R.num("POWER_VERDICT", POWER)

z = np.load(os.path.join(C.HERE, f"cfg186_a_curves{R.suf}.npz"), allow_pickle=True)
names = list(z["names"])
gals, _ = C.load_galaxies()
gd = {g["name"]: g for g in gals}
use = [gd[n] for n in names]
chi, feas, npt = z["chi"].astype(float), z["feas"], z["npt"]
Cf = C.fine_curves(chi, feas)
k0 = int(np.argmin(np.abs(C.TFINE)))
isprim = z["isprim"]
hasv = np.array([np.isfinite(g["cz_hel"]) for g in use])
ip = np.where(isprim)[0]
prim = [use[i] for i in ip]
cv_raw = C.Curves(Cf, npt, birge=True)
L0, tau = C.fit_tau(cv_raw.subset(ip).xhat, cv_raw.subset(ip).sig)
cv_all = cv_raw.with_tau(tau)
cvp = cv_all.subset(ip)
P(f"  primary: {len(ip)} galaxies; L0 = {L0:.3f}, tau = {tau:.3f} dex (Gaussian ML at beta = 0, as in part A)")


def speeds(gl, H0):
    U = C.u_matrix(gl, H0)
    VP = np.array([C.vperp2_lg(g["n"]) for g in gl])
    return U, VP


U1, VP = speeds(prim, C.H0_PRIMARY)
U73, _ = speeds(prim, C.H0_VARIANT)
Z1 = C.zmat(U1, np.zeros(len(prim)))
Z2 = C.zmat(U1, VP)
Z73 = C.zmat(U73, np.zeros(len(prim)))
Zfr = np.repeat(Z1[:, k0:k0 + 1], len(C.TFINE), axis=1)
fD = np.array([g["fD"] for g in prim])
nv = np.array([g["n"] for g in prim])


def fitv(cv, Z, starts=(-0.3, 0.0, 0.5, 2.0, 6.0), **kw):
    return C.Fitter(cv, Z, **kw).fit(beta_starts=starts, L0=L0)


# ============================================================================================ B1
R.banner("B1  FITTER EXACTNESS (M0: synthetic noiseless curves, beta = 0.30)")
Csyn = np.array([((C.XGRID[None, :] - L0 - np.log10(1 + 0.30 * Z1[i][:, None])) ** 2) / cvp.sig[i] ** 2
                 + C.TFINE[:, None] ** 2 for i in range(len(ip))])
rs = C.Fitter(C.Curves(Csyn, np.full(len(ip), 10 ** 7), birge=False), Z1).fit(beta_starts=(0.0, 0.5))
check("M0 the fitter returns beta = 0.300 +- 0.005 on noiseless synthetic curves", f"{rs['beta']:.4f}",
      abs(rs["beta"] - 0.30) <= 0.005)

# ============================================================================================ B2
R.banner("B2  THE PRIMARY FIT (W1: w^2 -> u^2, H0 = 67.66, nu_mono, Birge + tau softening, distance shared)")
r1 = fitv(cvp, Z1)
r_single = C.Fitter(cvp, Z1).fit(beta_starts=(0.0,), L0=L0)
r0 = C.Fitter(cvp, Z1).fit(fix_beta=0.0, L0=L0)
bhat, Lhat = r1["beta"], r1["L"]
dF = r0["F"] - r1["F"]
P(f"  beta_hat = {bhat:+.3f}, log10 a0_bar = {Lhat:.3f} (a0_bar = {10 ** Lhat:.3e} m/s^2); F(beta = 0) - F_min = {dF:.3f}")
P(f"  single start from beta = 0 (the null ensembles' setting): beta = {r_single['beta']:+.4f}")
R.num("primary", {"beta": bhat, "L": Lhat, "dF_beta0": dF, "beta_single_start": r_single["beta"]})
check("CONV the single-start fit (used in every ensemble) finds the multi-start minimum (|d beta| <= 0.02 or dF <= 0.01)",
      f"d beta = {r_single['beta'] - bhat:+.4f}, dF = {r_single['F'] - r1['F']:.4f}",
      abs(r_single["beta"] - bhat) <= 0.02 or (r_single["F"] - r1["F"]) <= 0.01)
bgrid = np.round(np.concatenate([np.arange(-0.90, 1.0, 0.05), np.arange(1.0, 3.0, 0.1), np.arange(3.0, 10.01, 0.25)]), 3)
Fprof = np.array([C.Fitter(cvp, Z1).fit(fix_beta=b, L0=Lhat)["F"] for b in bgrid]) - r1["F"]
inside = bgrid[Fprof <= 1.0]
P(f"  profile F(beta) - F_min: " + ", ".join(f"{b:+.2f}:{f:.2f}" for b, f in zip(bgrid[::6], Fprof[::6])))
P(f"  Delta F = 1 profile interval (reported): [{inside.min():+.2f}, {inside.max():+.2f}]"
  f"{' (at the scan edge)' if inside.max() >= bgrid[-1] or inside.min() <= bgrid[0] else ''}")
R.num("profile_interval_dF1", [float(inside.min()), float(inside.max())])
ts = C.Fitter(cvp, Z1).tstar(r1["q"])
P(f"  profiled distances at the best fit: t* median {np.median(ts):+.2f}, |t*| > 2 for {int(np.sum(np.abs(ts) > 2))} galaxies")

# ============================================================================================ B3
R.banner("B3  BOOTSTRAP (2000 galaxy resamples) AND THE NULLS")


def pool(func, tasks, state):
    return C.run_pool(func, tasks, state, nproc=NPROC)


t1 = time.time()
st = {"cv": cvp, "Z": Z1, "L0": L0, "tau": tau, "k0": k0}
bb = np.array(pool(C.task_boot, list(range(20000, 22000)), st))[:, 0]
sb = 0.5 * (np.percentile(bb, 84) - np.percentile(bb, 16))
P(f"  bootstrap: beta 16-84% [{np.percentile(bb, 16):+.3f}, {np.percentile(bb, 84):+.3f}] -> sigma_boot = {sb:.3f}; "
  f"2.5-97.5% [{np.percentile(bb, 2.5):+.3f}, {np.percentile(bb, 97.5):+.3f}] [{time.time() - t1:.0f} s]")
R.num("bootstrap", {"sigma": sb, "p16": np.percentile(bb, 16), "p84": np.percentile(bb, 84),
                    "p2.5": np.percentile(bb, 2.5), "p97.5": np.percentile(bb, 97.5)})

t1 = time.time()
st = {"cv": cvp, "U": U1, "VP2": np.zeros(len(prim)), "k0": k0, "L0": L0}
bp = np.array(pool(C.task_perm, list(range(30000, 32000)), st))
groups = [np.where(fD != 4)[0], np.where(fD == 4)[0]]
stg = dict(st, groups=groups)
bpg = np.array(pool(C.task_perm, list(range(40000, 41000)), stg))
st = {"cv": cvp, "Z": Z1, "L0": L0, "tau": tau, "k0": k0}
bn = np.array(pool(C.task_noise, list(range(50000, 51000)), st))


def pvals(null, obs):
    two = (1 + np.sum(np.abs(null) >= abs(obs))) / (len(null) + 1)
    one = (1 + np.sum(null >= obs)) / (len(null) + 1)
    return float(two), float(one)


pp, pp1 = pvals(bp, bhat)
pg, pg1 = pvals(bpg, bhat)
pn, pn1 = pvals(bn, bhat)
for lab, arr, p2, p1 in (("speed shuffle (2000)", bp, pp, pp1), ("shuffle within method groups (1000)", bpg, pg, pg1),
                         ("noise injection (1000)", bn, pn, pn1)):
    P(f"  {lab:38s}: null beta median {np.median(arr):+.3f}, 16-84% [{np.percentile(arr, 16):+.3f}, "
      f"{np.percentile(arr, 84):+.3f}]; p(|beta| >= |obs|) = {p2:.4f}, p(beta >= obs) = {p1:.4f}")
P(f"  [{time.time() - t1:.0f} s]")
R.num("nulls", {"perm": {"p_two": pp, "p_one": pp1, "median": np.median(bp), "p16": np.percentile(bp, 16),
                         "p84": np.percentile(bp, 84)},
                "perm_within_groups": {"p_two": pg, "p_one": pg1},
                "noise": {"p_two": pn, "p_one": pn1, "median": np.median(bn), "p16": np.percentile(bn, 16),
                          "p84": np.percentile(bn, 84)}})
S1 = pp < 0.003 and pn < 0.003
check("S1 (reported) p < 0.003 against both the speed shuffle and the noise injection", f"p_perm = {pp:.4f}, "
      f"p_noise = {pn:.4f}", S1, load_bearing=False)

# ============================================================================================ B4
R.banner("B4  SYSTEMATICS (each: point estimate + 1000 bootstrap resamples)")


def boot_sigma(cv, Z, n=1000, seed0=60000, L0v=None):
    stt = {"cv": cv, "Z": Z, "L0": L0 if L0v is None else L0v, "tau": tau, "k0": k0}
    b = np.array(pool(C.task_boot, list(range(seed0, seed0 + n)), stt))[:, 0]
    return 0.5 * (np.percentile(b, 84) - np.percentile(b, 16)), b


sysrows = {}


def row(lab, cv, Z, seed0, note="", U=None, VP2=None):
    r = fitv(cv, Z)
    s, b = boot_sigma(cv, Z, seed0=seed0)
    pperm = float("nan")
    if U is not None:
        stt = {"cv": cv, "U": U, "VP2": np.zeros(len(U)) if VP2 is None else VP2, "k0": k0, "L0": L0}
        bpr = np.array(pool(C.task_perm, list(range(seed0 + 500000, seed0 + 500500)), stt))
        pperm = pvals(bpr, r["beta"])[0]
    sysrows[lab] = {"N": int(cv.N), "beta": r["beta"], "sigma": s, "p_shuffle": pperm, "L": r["L"], "note": note}
    P(f"  {lab:37s} N = {cv.N:3d}: beta = {r['beta']:+.3f} +- {s:.3f} (boot); shuffle p = {pperm:.3f}; "
      f"log a0_bar = {r['L']:.3f}  {note}")
    return r, s


Ufr = np.repeat(U1[:, k0:k0 + 1], len(C.TFINE), axis=1)
row("H0 = 73", cvp, Z73, 61000, U=U73)
row("W2 (LG-coherent transverse motion)", cvp, Z2, 62000, U=U1, VP2=VP)
row("z frozen at catalogue distance", cvp, Zfr, 63000, "(Addendum 3)", U=Ufr)
iI, iU = np.where(fD != 4)[0], np.where(fD == 4)[0]
rI, sI = row("I: TRGB + Cepheid + SNIa", cv_all.subset(ip[iI]), Z1[iI], 64000, U=U1[iI])
rU, sU = row("UMa (one cluster distance)", cv_all.subset(ip[iU]), Z1[iU], 65000, U=U1[iU])
apex = nv @ C.VEC_LG > 0
rA, sA = row("LG-apex hemisphere (n.V_LG > 0)", cv_all.subset(ip[apex]), Z1[apex], 66000, U=U1[apex])
rB, sB = row("LG-antapex hemisphere (n.V_LG < 0)", cv_all.subset(ip[~apex]), Z1[~apex], 67000, U=U1[~apex])
bN = np.array([g["b"] for g in prim]) > 0
if bN.sum() >= 10 and (~bN).sum() >= 10:
    row("Galactic north (b > 0)", cv_all.subset(ip[bN]), Z1[bN], 68000, U=U1[bN])
    row("Galactic south (b < 0)", cv_all.subset(ip[~bN]), Z1[~bN], 69000, U=U1[~bN])
else:
    P(f"  Galactic split skipped: {int(bN.sum())} north, {int((~bN).sum())} south (< 10 in one half)")
cv_nt = cv_raw.with_tau(0.0)
row("no tau softening (tau = 0)", cv_nt.subset(ip), Z1, 70000, U=U1)
cv_nb_raw = C.Curves(Cf, npt, birge=False)
L0nb, taunb = C.fit_tau(cv_nb_raw.subset(ip).xhat, cv_nb_raw.subset(ip).sig)
row("no Birge scaling", cv_nb_raw.with_tau(taunb).subset(ip), Z1, 71000, f"(tau = {taunb:.3f})", U=U1)
bad = set(d[0] for d in ja["numbers"]["velocity_disagreements"])
keep = np.array([g["name"] not in bad for g in prim])
if (~keep).any():
    row("velocity-source disagreements dropped", cv_all.subset(ip[keep]), Z1[keep], 72000,
        f"(dropped: {', '.join(g['name'] for g, k in zip(prim, keep) if not k)})", U=U1[keep])
# free dipole and distance term (point estimates + bootstrap of beta)


def task_boot_ext(seed):
    S = C._POOL_STATE
    rng = np.random.default_rng(int(seed))
    N = S["Z"].shape[0]
    idx = rng.integers(0, N, N)
    r = C.Fitter(S["cv"], S["Z"], nvec=S.get("nvec"), G=S.get("G"), idx=idx).fit(beta_starts=(0.0,), L0=S["L0"])
    return r["beta"]


rd = C.Fitter(cvp, Z1, nvec=nv).fit(beta_starts=(0.0, 0.5, 2.0), L0=L0)
bdip = np.array(pool(task_boot_ext, list(range(73000, 73500)), {"cv": cvp, "Z": Z1, "nvec": nv, "L0": L0}))
sdip = 0.5 * (np.percentile(bdip, 84) - np.percentile(bdip, 16))
Ad = float(np.linalg.norm(rd["theta"]))
ld, bd = C.lb_of(rd["theta"]) if Ad > 0 else (float("nan"), float("nan"))
P(f"  {'beta with a free sky dipole':34s} N = {cvp.N:3d}: beta = {rd['beta']:+.3f} +- {sdip:.3f} (boot 500); dipole "
  f"|D| = {Ad:.3f} toward (l, b) = ({ld:.0f}, {bd:.0f})")
sysrows["free sky dipole"] = {"beta": rd["beta"], "sigma": sdip, "dipole_amp": Ad, "dipole_lb": [ld, bd]}
Gd = np.log10(np.array([g["D"] for g in prim]) / 10.0)[:, None]
rg = C.Fitter(cvp, Z1, G=Gd).fit(beta_starts=(0.0, 0.5, 2.0), L0=L0)
bgd = np.array(pool(task_boot_ext, list(range(74000, 74500)), {"cv": cvp, "Z": Z1, "G": Gd, "L0": L0}))
sgd = 0.5 * (np.percentile(bgd, 84) - np.percentile(bgd, 16))
P(f"  {'beta with a distance term':34s} N = {cvp.N:3d}: beta = {rg['beta']:+.3f} +- {sgd:.3f} (boot 500); "
  f"gamma = {rg['gamma'][0]:+.3f} (log a0 per dex of D)")
sysrows["distance term"] = {"beta": rg["beta"], "sigma": sgd, "gamma": float(rg["gamma"][0])}

# single-galaxy jackknife (reported): is the primary beta carried by one galaxy?
jk = []
for j in range(len(ip)):
    keepj = np.delete(np.arange(len(ip)), j)
    bj = C.Fitter(cvp, Z1, idx=keepj).fit(beta_starts=(0.0, 0.5, 2.0), L0=L0)["beta"]
    jk.append((bj - bhat, prim[j]["name"]))
jk.sort(key=lambda r: -abs(r[0]))
P(f"  {'single-galaxy jackknife':37s} N = {cvp.N - 1:3d}: beta range [{bhat + min(r[0] for r in jk):+.3f}, "
  f"{bhat + max(r[0] for r in jk):+.3f}]; largest moves: " + ", ".join(f"{n} {d:+.2f}" for d, n in jk[:3]))
sysrows["jackknife"] = {"min": bhat + min(r[0] for r in jk), "max": bhat + max(r[0] for r in jk),
                        "largest": [[n, d] for d, n in jk[:5]]}

# the CIRCULAR rows
for lab, sel in (("CIRCULAR: Hubble-flow galaxies only", np.where((z["fD"] == 1) & hasv)[0]),
                 ("CIRCULAR: all clean galaxies with v", np.where(hasv)[0])):
    cvr = cv_raw.subset(sel)
    L0c, tauc = C.fit_tau(cvr.xhat, cvr.sig)
    cvc = cv_raw.with_tau(tauc).subset(sel)
    Zc = C.zmat(C.u_matrix([use[i] for i in sel], C.H0_PRIMARY), np.zeros(len(sel)))
    rc = C.Fitter(cvc, Zc).fit(beta_starts=(-0.3, 0.0, 0.5, 2.0, 6.0), L0=L0c)
    bc = np.array(pool(C.task_boot, list(range(75000, 76000)), {"cv": cvc, "Z": Zc, "L0": L0c, "tau": tauc, "k0": k0}))[:, 0]
    sc = 0.5 * (np.percentile(bc, 84) - np.percentile(bc, 16))
    sysrows[lab] = {"N": int(len(sel)), "beta": rc["beta"], "sigma": sc, "tau": tauc,
                    "note": "u is a function of sky position and the flow model, not a measurement"}
    P(f"  {lab:34s} N = {len(sel):3d}: beta = {rc['beta']:+.3f} +- {sc:.3f} (tau = {tauc:.3f}) -- NOT a measurement")
R.num("systematics", sysrows)

# pass-line pieces
pIU = math.erfc(abs(rI["beta"] - rU["beta"]) / math.sqrt(sI ** 2 + sU ** 2) / math.sqrt(2))
S2 = (np.sign(rI["beta"]) == np.sign(bhat)) and abs(rI["beta"]) >= 2 * sI and pIU > 0.05
S3 = abs(sysrows["H0 = 73"]["beta"] - bhat) < sb
pAB = math.erfc(abs(rA["beta"] - rB["beta"]) / math.sqrt(sA ** 2 + sB ** 2) / math.sqrt(2))
S4 = pAB > 0.05
P(f"\n  S2: beta_I = {rI['beta']:+.3f} +- {sI:.3f} ({abs(rI['beta']) / sI:.1f} sigma, sign {'=' if np.sign(rI['beta']) == np.sign(bhat) else '!='} "
  f"primary); I vs UMa p = {pIU:.3f} -> {'pass' if S2 else 'fail'}")
P(f"  S3: |beta(H0 = 73) - beta| = {abs(sysrows['H0 = 73']['beta'] - bhat):.3f} vs sigma_boot {sb:.3f} -> "
  f"{'pass' if S3 else 'fail'}")
P(f"  S4: apex vs antapex p = {pAB:.3f} -> {'pass' if S4 else 'fail'}")
R.num("signal_lines", {"S1": S1, "S2": bool(S2), "S3": bool(S3), "S4": bool(S4), "p_I_vs_UMa": pIU, "p_apex_antapex": pAB})

# ============================================================================================ B5
R.banner("B5  LIMITS BY NEYMAN CONSTRUCTION (curve-level mocks + injected beta, 200 trials per grid value)")
gridN = np.round(np.concatenate([np.arange(-0.90, 1.0001, 0.05), np.arange(1.1, 3.0001, 0.1), np.arange(3.25, 10.0001, 0.25)]), 3)


def task_ney(args):
    b_inj, seed = args
    S = C._POOL_STATE
    S2_ = dict(S)
    S2_["beta_inj"] = b_inj
    C._POOL_STATE.update(S2_)
    out = C.task_noise(seed)
    C._POOL_STATE["beta_inj"] = 0.0
    return out


t1 = time.time()
NT = 200
tasks = [(float(b), 80000 + 1000 * j + k) for j, b in enumerate(gridN) for k in range(NT)]
res = np.array(pool(task_ney, tasks, {"cv": cvp, "Z": Z1, "L0": L0, "tau": tau, "k0": k0, "beta_inj": 0.0}))
res = res.reshape(len(gridN), NT)
Fcov = np.mean(res >= bhat, axis=1)
med = np.median(res, axis=1)
P(f"  {len(tasks)} fits [{time.time() - t1:.0f} s]")
P("  beta_inj : P(beta_hat >= beta_obs), median beta_hat")
for j in list(range(0, len(gridN), 4)) + [len(gridN) - 1]:
    P(f"    {gridN[j]:+6.2f} : {Fcov[j]:.3f}, {med[j]:+.3f}")


def first_above(level):
    ok = np.where(Fcov >= level)[0]
    return float(gridN[ok[0]]) if len(ok) else float("inf")


def last_below(level):
    ok = np.where(Fcov <= level)[0]
    return float(gridN[ok[-1]]) if len(ok) else float("-inf")


b95_decl = first_above(0.95)
bhi = first_above(0.975)
blo = last_below(0.025)
P(f"  DECLARED (noise mocks): one-sided 95% upper limit {b95_decl:.2f}; two-sided 95% interval [{blo:.2f}, {bhi:.2f}] "
  f"('-inf' = below the physical floor beta ~ -1/z_max, 'inf' = above 10)")
R.num("neyman", {"grid": gridN, "coverage": Fcov, "median_beta_hat": med, "beta95": b95_decl, "two_sided": [blo, bhi]})


def task_ney_perm(args):
    """Addendum 4: real curves and preferred values, speeds shuffled (any real beta destroyed), beta_inj injected as a
    curve shift log10(1 + beta_inj z_pi(i)(0)) consistent with the shuffled speeds."""
    b_inj, seed = args
    S = C._POOL_STATE
    rng = np.random.default_rng(int(seed))
    U, kk = S["U"], S["k0"]
    pi = rng.permutation(U.shape[0])
    Up = U[pi, kk][:, None] + (U - U[:, kk][:, None])
    Zp = C.zmat(Up, np.zeros(U.shape[0]))
    shift = np.log10(np.maximum(1.0 + b_inj * Zp[:, kk], 1e-3))
    return C.Fitter(S["cv"], Zp, delta=shift).fit(beta_starts=(0.0,), L0=S["L0"])["beta"]


t1 = time.time()
tasks = [(float(b), 180000 + 1000 * j + k) for j, b in enumerate(gridN) for k in range(NT)]
resp = np.array(pool(task_ney_perm, tasks, {"cv": cvp, "U": U1, "k0": k0, "L0": L0})).reshape(len(gridN), NT)
Fcov_p = np.mean(resp >= bhat, axis=1)
med_p = np.median(resp, axis=1)
P(f"  ADDED (Addendum 4) Neyman on speed-shuffled real data: {len(tasks)} fits [{time.time() - t1:.0f} s]")
P("  beta_inj : P(beta_hat >= beta_obs), median beta_hat")
for j in list(range(0, len(gridN), 4)) + [len(gridN) - 1]:
    P(f"    {gridN[j]:+6.2f} : {Fcov_p[j]:.3f}, {med_p[j]:+.3f}")
okp = np.where(Fcov_p >= 0.95)[0]
b95_perm = float(gridN[okp[0]]) if len(okp) else float("inf")
okp2 = np.where(Fcov_p >= 0.975)[0]
bhi_p = float(gridN[okp2[0]]) if len(okp2) else float("inf")
okp3 = np.where(Fcov_p <= 0.025)[0]
blo_p = float(gridN[okp3[-1]]) if len(okp3) else float("-inf")
b95_boot = float(np.percentile(bb, 95))
b95 = max(b95_decl, b95_perm, b95_boot)
P(f"  shuffle-Neyman: one-sided 95% upper limit {b95_perm:.2f}; two-sided [{blo_p:.2f}, {bhi_p:.2f}]; bootstrap 95th "
  f"percentile {b95_boot:.2f}")
P(f"  QUOTED beta_95 = max(declared {b95_decl:.2f}, shuffle {b95_perm:.2f}, bootstrap {b95_boot:.2f}) = {b95:.2f} "
  f"(the conservative choice, Addendum 4)")
R.num("neyman_shuffle", {"coverage": Fcov_p, "median_beta_hat": med_p, "beta95": b95_perm, "two_sided": [blo_p, bhi_p]})
R.num("beta95_bootstrap", b95_boot)
R.num("beta95_quoted", b95)
rb = {f"{b:.2f}": float(m) for b, m in zip(gridN, med) if abs(b - round(b)) < 1e-9 or abs(b - 0.1) < 1e-9 or abs(b - 0.3) < 1e-9}
P(f"  recovery (median beta_hat at beta_inj): {rb}")

# ============================================================================================ B6
R.banner("B6  TRANSLATION TO KM1'S KHRONON PARAMETER (conditional on KM1's model) AND G7")
eps_min = C.KM1_COEF / b95 if np.isfinite(b95) and b95 > 0 else 0.0
c14_min = eps_min / (1 + 2 * eps_min)
bw = [C.KM1_COEF / (c / (1 - 2 * c)) for c in (1e-5, 2.5e-5)]
P(f"  KM1 (C7): a0 -> a0 (1 + D/3), D = 2 w^2/(eps c^2)  =>  beta = 2 w_ref^2/(3 eps c^2) = {C.KM1_COEF:.4e}/eps")
P(f"  KM1's window c14 in [1e-5, 2.5e-5] (eps = c2 = c14/(1 - 2 c14)) predicts beta in [{bw[1]:.3f}, {bw[0]:.3f}]; "
  f"G7's line beta = 0.10 is eps = {C.KM1_COEF / 0.10:.2e}")
P(f"  SPARC's beta_95 = {b95:.2f}  =>  eps >= {eps_min:.2e} (c14 >= {c14_min:.2e}) at 95%, conditional on KM1's model, the "
  f"sphere average D/3, and W1 (independent velocity components)")
excl = [c for c, b in zip((1e-5, 2.5e-5), bw) if b > b95]
P(f"  KM1's window: {'EXCLUDED at 95% for c14 = ' + str(excl) if excl else 'NOT reached (beta_95 exceeds the window by ' + f'{b95 / bw[0]:.0f}-{b95 / bw[1]:.0f}x)'}")
R.num("KM1", {"coef": C.KM1_COEF, "eps_min_95": eps_min, "c14_min_95": c14_min, "window_beta": bw,
              "window_excluded": bool(excl)})

SIGNAL = bool(S1 and S2 and S3 and S4)
if POWER == "DIAGNOSTIC":
    g7 = "PASS" if (blo >= -0.10 and bhi <= 0.10) else ("FAIL" if (SIGNAL and abs(bhat) > 0.10) else "INCONCLUSIVE")
else:
    g7 = "NO VERDICT (NON-DIAGNOSTIC)"
P(f"\n  SIGNAL ('a0 tracks CMB-frame speed'): {'DECLARED' if SIGNAL else 'NOT declared'} "
  f"(S1 {S1}, S2 {bool(S2)}, S3 {bool(S3)}, S4 {bool(S4)})")
P(f"  G7 from SPARC: {g7}")
R.num("SIGNAL", SIGNAL)
R.num("G7", g7)
check("VERD (reported) the verdict follows the frozen pass lines (a NULL or NON-DIAGNOSTIC result is valid)",
      f"POWER {POWER}; SIGNAL {SIGNAL}; G7 {g7}", True, load_bearing=False)

# ============================================================================================ MUTATE
if C.MUTATE:
    R.banner("M  MUTATE CONTROL: beta = 0.30 injected at the point level")
    jr = os.path.join(C.HERE, "cfg186_b_fit_results.json")
    if os.path.exists(jr):
        bobs = json.load(open(jr))["numbers"]["primary"]["beta"]
        dB = bhat - bobs
        check("M1 beta_hat_mut - beta_hat_obs lies in [0.24, 0.36] (injected 0.30)", f"{dB:+.3f} (mut {bhat:+.3f}, "
              f"obs {bobs:+.3f})", 0.24 <= dB <= 0.36,
              reading="the model is multiplicative in (1 + beta z): an injection on top of beta_obs moves beta_hat by "
                      "0.30 (1 + beta_obs z) to first order, so a large beta_obs inflates the shift")
        # Addendum 5 diagnostics (reported): is the M1 miss the pipeline or the multiplicative composition?
        za = np.load(os.path.join(C.HERE, "cfg186_a_curves.npz"), allow_pickle=True)
        Cf_real = C.fine_curves(za["chi"].astype(float), za["feas"])
        cr_raw = C.Curves(Cf_real, za["npt"], birge=True)
        L0r, taur = C.fit_tau(cr_raw.subset(ip).xhat, cr_raw.subset(ip).sig)
        cr = cr_raw.with_tau(taur).subset(ip)
        shift_c = np.log10(1.0 + C.BETA_MUT * Z1[:, k0])
        rcur = C.Fitter(cr, Z1, delta=shift_c).fit(beta_starts=(-0.3, 0.0, 0.5, 2.0, 6.0), L0=L0r)
        dB_curve = rcur["beta"] - bobs
        check("M1b (reported, Addendum 5) the same injection applied at the CURVE level to the REAL curves moves beta_hat "
              "by the same amount as the point-level MUTATE (|difference| <= 0.10)",
              f"curve-level d beta = {dB_curve:+.3f} vs point-level {dB:+.3f}", abs(dB_curve - dB) <= 0.10,
              load_bearing=False)
        rg_ = C.Fitter(cvp, Z1, offset=np.log10(1.0 + bobs * Z1)).fit(beta_starts=(-0.3, 0.0, 0.5, 2.0), L0=L0)
        check("M1c (reported, Addendum 5) on the MUTATE curves, with the real-data factor (1 + beta_obs z) held fixed, "
              "the extra factor (1 + gamma z) recovers the injected 0.30 (|gamma - 0.30| <= 0.06)",
              f"gamma = {rg_['beta']:+.3f}", abs(rg_["beta"] - 0.30) <= 0.06, load_bearing=False)
        wz = np.sum(Z1[:, k0] ** 2 * cvp.q) / np.sum(Z1[:, k0] * cvp.q)
        P(f"  composition law: (1 + beta_obs z)(1 + 0.30 z) = 1 + (beta_obs + 0.30 + 0.30 beta_obs z) z  => d beta ~ "
          f"0.30 (1 + beta_obs z_eff); the leverage-weighted z_eff = sum z^2 / sum z = {wz:.2f} gives "
          f"{0.30 * (1 + bobs * wz):.3f}")
        R.num("M1_diagnostics", {"d_beta_point": dB, "d_beta_curve": dB_curve, "gamma_fixed_obs": rg_["beta"],
                                 "z_eff": wz, "d_beta_composition": 0.30 * (1 + bobs * wz)})
        sb_real = json.load(open(jr))["numbers"]["bootstrap"]["sigma"]
        need = 0.30 >= 4 * sb_real
        check("M2 (reported) the mutated data's p values (< 0.003 required only if 0.30 >= 4 sigma_boot of the real data)",
              f"p_perm = {pp:.4f}, p_noise = {pn:.4f}; 0.30 vs 4 sigma = {4 * sb_real:.2f} -> required: {need}",
              (pp < 0.003 and pn < 0.003) if need else True, load_bearing=False)
    else:
        check("M1 the real-data run exists (run part B without MUTATE first)", "missing", False)

sys.exit(R.finish())
