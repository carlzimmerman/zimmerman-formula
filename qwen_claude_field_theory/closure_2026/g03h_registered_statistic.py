#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03h -- what the pre-registered DR4 estimator returns if the candidate is true: the candidate's velocity boost gamma_v(r, M) = sqrt(gamma_force),
orientation-averaged from the g03g tables, applied to the TRUE relative velocity in the pipeline's own population model (make_population, DR4 noise),
then the pipeline's own estimator (bin medians in log10 y_proj, profile-chi2 fit of the declared shape's gamma_inf with the anchored kappa).
Nothing of the registration is modified: this script imports the frozen pipeline and treats the candidate-boosted MC as the data.
Usage: python3 g03h_registered_statistic.py [newton|candidate]"""
import sys, os, json, math, numpy as np, warnings; warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "prep_2026", "gaia_dr4_prep")); import wide_binary_pipeline as P
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
mode = sys.argv[1] if len(sys.argv) > 1 else "newton"; rng = np.random.default_rng(20261216)
print("=" * 100); print(f"g03h -- the registered DR4 statistic under: {mode}"); print("=" * 100)
NM = 1_500_000
def boost_fn_newton(r3d, Mt): return np.ones_like(r3d)
def load_table(foot):
    T = json.load(open(os.path.join(HERE, f"g03g_table_{foot}.json")))["table"]
    S = sorted({float(k.split("|")[1]) for k in T}); Ms = sorted({float(k.split("|")[0]) for k in T}); TH = sorted({float(k.split("|")[2]) for k in T})
    w = {0.0: 0.0, 45.0: 0.0, 90.0: 0.0}   # isotropic orientation average by Simpson-like weights on cos(theta): theta = 0, 45, 90 -> weights on [0,1] in cos
    # average of f(theta) over sin(theta) dtheta on [0, pi/2] using nodes 0, 45, 90 deg with Simpson on x = cos(theta): x = 1, 0.707, 0 -> non-uniform; use trapezoid in x
    xs = np.array([1.0, math.cos(math.radians(45)), 0.0]); tab = np.zeros((len(Ms), len(S)))
    for i, M in enumerate(Ms):
        for j, s in enumerate(S):
            g0, g90 = T[f"{M}|{s}|0.0"]["gamma"], T[f"{M}|{s}|90.0"]["gamma"]
            if f"{M}|{s}|45.0" in T: g45 = T[f"{M}|{s}|45.0"]["gamma"]
            else:                                                           # angular shape borrowed from the M_tot = 1 row at the same separation
                r0, r45, r90 = (T[f"1.0|{s}|{th}"]["gamma"] - 1 for th in (0.0, 45.0, 90.0)); wgt = r45/(r0 + r90) if (r0 + r90) != 0 else 0.5
                g45 = 1 + wgt*((g0 - 1) + (g90 - 1))
            f = np.array([g0, g45, g90]); tab[i, j] = -np.trapz(f, xs)     # int_0^1 f d(cos theta) (xs descending -> minus)
    return np.array(Ms), np.array(S), tab
def make_boost_fn(foot):
    Ms, S, tab = load_table(foot)
    def fn(r3d, Mt):
        sk = np.clip(r3d/P.KAU, S[0], S[-1]); m = np.clip(Mt, Ms[0], Ms[-1])
        g_lo = np.interp(np.log(sk), np.log(S), tab[0]); g_hi = np.interp(np.log(sk), np.log(S), tab[-1])
        gf = g_lo + (g_hi - g_lo)*(m - Ms[0])/(Ms[-1] - Ms[0])
        return np.sqrt(np.maximum(gf, 1e-6))
    return fn, (Ms, S, tab)
for foot, a0 in (("canonical", P.A0_CAN), ("alt", P.A0_ALT)):
    if mode == "candidate":
        fn, (Ms, S, tab) = make_boost_fn(foot)
        print(f"  [{foot}] orientation-averaged gamma_force table (rows M_tot = {Ms}):"); print("     s [kAU]: " + " ".join(f"{s:6.1f}" for s in S))
        for i, M in enumerate(Ms): print(f"     M = {M:.1f}:  " + " ".join(f"{g:6.4f}" for g in tab[i]))
    else: fn = boost_fn_newton
    pop = P.make_population(NM, rng, dr4=True); logy = np.log10(pop["g_proj"]/a0)
    r3d = np.sqrt(P.G*pop["M_obs"]*P.MSUN/pop["g_true"])*0 + np.sqrt(P.G*(pop["M_obs"])*P.MSUN/pop["g_true"])   # true separation from the true acceleration and the mass
    gam = fn(r3d, pop["M_obs"])
    vX = (gam*pop["pmx"] + pop["npmx"])*4.74e3*(pop["d_obs"]/1000.); vY = (gam*pop["pmy"] + pop["npmy"])*4.74e3*(pop["d_obs"]/1000.)
    vt = np.hypot(vX, vY)/pop["vc_obs"]
    mod = P.model_medians(pop, a0, P.GRID, rng)                                  # the declared-shape model family from the same master
    # the "data": a DR4-sized subsample (30000) and the full MC (asymptotic)
    for label, nsel in (("DR4-sized 30000", 30000), ("full MC", len(vt))):
        idx = rng.choice(len(vt), nsel, replace=False) if nsel < len(vt) else np.arange(len(vt))
        med, sig, cnt = P.bin_medians(logy[idx], vt[idx], boot=300, rng=rng)
        g, sg, chi2, nb, kap = P.fit_gamma(med, sig, mod, P.GRID)
        print(f"  [{foot}] {label}: registered estimator gamma_v = {g:.4f} +/- {sg:.4f} (chi2 {chi2:.1f}, {nb} bins, kappa {kap:.4f}); distance to Newton {(g-1)/sg:+.1f} sigma, to the band floor {P.GAMMA_TARGET if foot == 'canonical' else P.GAMMA_TARGET_ALT:.4f}: {(g - (P.GAMMA_TARGET if foot == 'canonical' else P.GAMMA_TARGET_ALT))/sg:+.1f} sigma")
        if mode == "newton" and label == "full MC":
            check(f"N1 [{foot}] a Newtonian injection is recovered by the registered estimator as gamma_v = 1.000 +/- 0.01", abs(g - 1.0) < 0.01, f"{g:.4f}")
        if mode == "candidate":
            band = (P.GAMMA_TARGET, P.GAMMA_TARGET_TOP) if foot == "canonical" else (P.GAMMA_TARGET_ALT, P.GAMMA_TARGET_ALT_TOP)
            if label == "full MC":
                print(f"  [{foot}] THE NUMBER: if the candidate is true, DR4's registered estimator returns gamma_v = {g:.3f}; the registered band is {band[0]:.4f}-{band[1]:.4f}, Newton is 1.000")
                check(f"C1 [{foot}] the candidate's registered-statistic prediction is finite and below the registered band floor", np.isfinite(g) and g < band[0], f"gamma_v = {g:.4f} vs band floor {band[0]:.4f}")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
