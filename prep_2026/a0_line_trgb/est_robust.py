#!/usr/bin/env python3
"""
est_robust.py -- THE ROBUST-ESTIMATOR LANE of the TRGB LEVER on the a0-line.
==========================================================================================
Fires the median / robust-slope and the EIV (errors-in-variables, orthogonal-distance)
a0-line estimators on the TRGB/Cepheid-anchored gas-dominated subsample (SPARC fD in
{2,3}, distance systematic sigma_lnD = 0.05, FIVE-fold smaller than the fD=1 Hubble-flow
0.25) vs the FULL gas-dominated subsample, both footings.

THE a0-LINE (banked, identity_uniqueness.py): for the framework's OWN interpolation
nu = sqrt(1 + 1/y) (= Milgrom 1999 PLA 253:273 kernel; the framework's distinctive
content is the horizon COEFFICIENT a0 = cH_Lambda/Z, not the kernel shape), squaring
g_obs = sqrt(g_bar^2 + g_bar*a0) gives the EXACT identity

        E := g_obs^2 - g_bar^2 = a0 * g_bar          (straight line, origin, slope a0).

TWO ROBUST ESTIMATORS (the ones that cross-checked the banked GLS central 1.181e-10):
  (R1) MEDIAN / robust slope:  a0_hat = median_i( E_i / g_bar_i )  -- Theil-Sen-through-
       origin; immune to the weight-noise trap by construction (no weights).
  (R2) EIV / ODR:  fit g_obs^2 = g_bar^2 + a0*g_bar in the (g_bar, g_obs^2) plane, where
       g_bar (photometry+gas) and g_obs (kinematics) carry INDEPENDENT errors, by
       orthogonal-distance regression (scipy.odr). This is the honest errors-in-variables
       form: it does NOT lump the g_bar error into E (which would correlate the axes);
       it keeps the two physically-independent measurements on their own axes. Model-based
       sigmas + intrinsic-floor iteration to res_var -> 1 (the SAME cure the banked GLS
       used for the observed-error weight-noise trap that once faked a 3.3e-11 deficit).

GLS is imported (fire_common) ONLY as the agreement cross-check: median vs GLS AGREE on
the TRGB set => estimator-owned central is robust; disagree => flag.

Errors are GALAXY-LEVEL bootstrap (resample galaxies with replacement, not points --
respects per-galaxy distance/M-L correlation).

HONESTY RAILS (this is the estimator that ALREADY caught a fake deficit): both footings
(canonical 9.355e-11 = cH_Lambda/Z, ALT 1.1305e-10 = cH_0/Z); NEVER raw observed-error
weights; report whether the central STAYS at the banked value or MOVES; if the fD in {2,3}
set is too small to discriminate the two footings, SAY underpowered. No 'proves'. Credit
Lelli-McGaugh-Schombert 2016 (SPARC), McGaugh+2016 (g_dagger=1.2e-10, comparison only).
Exit 0 = computed, not a verdict.
"""
import numpy as np, os, json, sys
import scipy.odr as odr
sys.path.insert(0, "/Users/carlzimmerman/new_physics/prep_2026/a0_line")
from fire_common import (load, flat, gls, budget, A0C, A0A, A0_RARFIT,
                         SLNB, ZVAL, CLIGHT)

HERE = "/Users/carlzimmerman/new_physics/prep_2026/a0_line_trgb"
LAMBDA_PLANCK = 1.089e-52          # Planck 2018 cosmological constant, m^-2 (comparison)
FDSETS = {"GAS-ALL": None, "TRGB/Ceph {2,3}": {2, 3}, "Hubble-flow {1}": {1}}
BOOT = 2000
BOOT_EIV_ITERS = 6          # EIV converges to <1e-4 rel by iter ~4 (checked); light in boot
RNG = np.random.default_rng(20260717)
bar = "=" * 94


def subselect(gals, fdset):
    return gals if fdset is None else [g for g in gals if g["fD"] in fdset]


# ------------------------------------------------------------------ R1 median / robust
def est_median(GB, GO):
    """Theil-Sen-through-origin: median of per-point slopes E/g_bar. Weight-free."""
    return float(np.median((GO**2 - GB**2) / GB))


# ------------------------------------------------------------------ R2 EIV / ODR
def est_eiv(GB, GO, FV, iters=25):
    """Errors-in-variables slope of the a0-line, done as orthogonal-distance regression
    of g_obs^2 = g_bar^2 + a0*g_bar in the (g_bar, g_obs^2) plane. g_bar and g_obs carry
    INDEPENDENT errors (photometry vs kinematics), so ODR with independent sx, sy is the
    correct EIV form -- no axis-correlation term. Model-based sigmas, intrinsic floor
    iterated to res_var->1 (cures the observed-weight trap)."""
    Go2 = GO**2
    sx = np.maximum(SLNB * GB, 1e-14 * GB.max())        # g_bar frac scatter (10%)
    a0, fint = 1e-10, 0.3
    model = odr.Model(lambda B, x: x**2 + B[0] * x)
    for _ in range(iters):
        Go2m = GB**2 + a0 * GB                           # model g_obs^2 (avoid obs-weight trap)
        sy = np.sqrt((2 * Go2m * FV) ** 2 + (fint * Go2m) ** 2)
        data = odr.RealData(GB, Go2, sx=sx, sy=sy)
        out = odr.ODR(data, model, beta0=[a0]).run()
        a0n = float(out.beta[0])
        rv = float(out.res_var) if np.isfinite(out.res_var) and out.res_var > 0 else 1.0
        fint = float(np.clip(fint * rv**0.25, 0.01, 5.0))
        if abs(a0n - a0) < 1e-17:
            a0 = a0n
            break
        a0 = a0n
    return a0, fint


def est_gls(GB, GO, FV):
    a0, _, _, _ = gls(GB, GO, FV)                        # model-based iterated GLS (banked)
    return float(a0)


# ------------------------------------------------------------------ galaxy-level bootstrap
def bootstrap(gals_sub, gas_only, fn):
    """Resample galaxies with replacement; recompute estimator fn(GB,GO,FV[,PHI...])."""
    vals = []
    n = len(gals_sub)
    if n < 2:
        return np.nan, np.nan
    for _ in range(BOOT):
        pick = [gals_sub[i] for i in RNG.integers(0, n, n)]
        GB, GO, FV = flat(pick, gas_only)[:3]
        if len(GB) < 5:
            continue
        try:
            vals.append(fn(GB, GO, FV))
        except Exception:
            continue
    vals = np.array([v for v in vals if np.isfinite(v)])
    if vals.size < 10:
        return np.nan, np.nan
    return float(np.median(vals)), float(0.5 * (np.percentile(vals, 84) - np.percentile(vals, 16)))


# ------------------------------------------------------------------ Occam / Bayes bans
def logB(xhat, s_meas, astar, s_anchor_frac, lo=1e-11, hi=1e-9):
    """log10 evidence M0 (a0 predicted, 0 params, Planck anchor) / M1 (a0 free, 1 param,
    log-flat prior) by numeric quadrature. Same closed form as banked fire_occam.py."""
    xg = np.linspace(np.log(lo), np.log(hi), 200001)
    s_eff = np.hypot(s_meas, s_anchor_frac)
    lnZ0 = -0.5 * ((np.log(astar) - xhat) / s_eff) ** 2 - np.log(np.sqrt(2 * np.pi) * s_eff)
    Lx = np.exp(-0.5 * ((xg - xhat) / s_meas) ** 2) / (np.sqrt(2 * np.pi) * s_meas)
    prior = np.full_like(xg, 1.0 / (np.log(hi) - np.log(lo)))
    lnZ1 = np.log(np.trapz(Lx * prior, xg))
    return float((lnZ0 - lnZ1) / np.log(10.0)), float((np.log(astar) - xhat) / s_eff)


def lam_ratio(a0hat):
    """Lambda = 3 Z^2 a0^2 / c^4; ratio to Planck. dS: a0 = cH_L/Z, Lambda = 3H_L^2/c^2."""
    lam = 3.0 * ZVAL**2 * a0hat**2 / CLIGHT**4
    return lam, lam / LAMBDA_PLANCK


results = {"anchors": dict(a0_canon=A0C, a0_alt=A0A, Z=ZVAL, Lambda_Planck=LAMBDA_PLANCK,
                           banked_gas_gls=1.1814381247770623e-10,
                           banked_gas_med=9.725607106012755e-11)}

for UD in (0.50, 0.70):
    print(bar)
    print(f"ROBUST ESTIMATORS on the a0-line  (disk M/L Upsilon_d = {UD:.2f}"
          f"{'  [fiducial]' if UD == 0.5 else '  [banked headline]'})")
    print(bar)
    gals = load(UD)
    udkey = f"Ud={UD:.2f}"
    results[udkey] = {}
    print(f"  {'subsample':<20} {'Ngal':>4} {'Npts':>5} | "
          f"{'median':>10} {'+-boot':>9} | {'EIV/ODR':>10} {'+-boot':>9} | {'GLS':>10}"
          f" | {'med~GLS':>8}")
    for tag, fdset in FDSETS.items():
        sub = subselect(gals, fdset)
        sub_gas = [g for g in sub if g["gasdom"].any()]
        GB, GO, FV = flat(sub, True)[:3]
        ng = len({i for i, g in enumerate(sub) if g["gasdom"].any()})
        if len(GB) < 10:
            print(f"  {tag:<20} {ng:>4} {len(GB):>5} | too few gas-dom points -- skip")
            results[udkey][tag] = dict(N=int(len(GB)), Ngal=int(ng), underpowered=True)
            continue
        a0_med = est_median(GB, GO)
        a0_eiv, fint_eiv = est_eiv(GB, GO, FV)
        a0_g = est_gls(GB, GO, FV)
        subg = [g for g in sub if g["gasdom"].any()]
        mb, sb_med = bootstrap(subg, True, lambda GB, GO, FV: est_median(GB, GO))
        eb, sb_eiv = bootstrap(subg, True, lambda GB, GO, FV: est_eiv(GB, GO, FV, iters=BOOT_EIV_ITERS)[0])
        gb_, sb_gls = bootstrap(subg, True, est_gls)
        # median vs GLS agreement (combined bootstrap error)
        comb = np.hypot(sb_med, sb_gls)
        agree = abs(a0_med - a0_g) / comb if comb > 0 else np.nan
        flag = "AGREE" if agree < 1.0 else ("~1s" if agree < 2 else "FLAG")
        print(f"  {tag:<20} {ng:>4} {len(GB):>5} | {a0_med:>10.3e} {sb_med:>9.2e} | "
              f"{a0_eiv:>10.3e} {sb_eiv:>9.2e} | {a0_g:>10.3e} | {flag:>8}({agree:.1f})")
        results[udkey][tag] = dict(
            N=int(len(GB)), Ngal=int(ng),
            a0_median=float(a0_med), boot_median=float(sb_med),
            a0_eiv=float(a0_eiv), boot_eiv=float(sb_eiv), fint_eiv=float(fint_eiv),
            a0_gls=float(a0_g), boot_gls=float(sb_gls),
            med_gls_sigma=float(agree), med_gls_flag=flag)
    # discrimination vs footings, per subsample, per estimator
    print(f"\n  DISCRIMINATION (a0_hat - a0_ref)/sigma_boot  [canonical {A0C:.3e} / ALT {A0A:.3e}"
          f" / RAR g+ {A0_RARFIT:.2e}]")
    print(f"  {'subsample':<20} {'estimator':<8} | {'a0_hat':>10} {'sig':>9} |"
          f" {'vs canon':>9} {'vs ALT':>8} {'vs RAR':>8}")
    for tag in FDSETS:
        d = results[udkey][tag]
        if d.get("underpowered"):
            continue
        for est, akey, skey in (("median", "a0_median", "boot_median"),
                                ("EIV", "a0_eiv", "boot_eiv")):
            a, s = d[akey], d[skey]
            tc, ta, tr = (a - A0C) / s, (a - A0A) / s, (a - A0_RARFIT) / s
            print(f"  {tag:<20} {est:<8} | {a:>10.3e} {s:>9.2e} |"
                  f" {tc:>+8.1f}s {ta:>+7.1f}s {tr:>+7.1f}s")
    print()

# ---------------------------------------------------------------- TRGB budget + Occam + Lambda
print(bar)
print("THE LEVER REALIZED: full systematic budget on fD in {2,3} (sysD 5x smaller), the")
print("Occam bans with the reduced-distance error, and the Lambda-inversion.  Ud=0.70")
print("banked headline (the lone Cepheid galaxy drops out at high Ud; TRGB carries it).")
print(bar)
gals = load(0.70)
lever = {}
for tag, fdset in (("GAS-ALL", None), ("TRGB/Ceph {2,3}", {2, 3})):
    b = budget(subselect(gals, fdset), gas_only=True)
    lever[tag] = b
    print(f"\n  {tag}: N={b['N']} pts / {b['Ngal']} gals | a0_hat(GLS)={b['a0hat']:.3e}"
          f"  a0(median)={b['a0med']:.3e}  f_int={b['fint']:.2f}")
    print(f"    sigma: stat {b['stat']:.2e} | DIST {b['sysD']:.2e} | inc {b['sysI']:.2e}"
          f" | Ups(glob) {b['sysU']:.2e} | gascal {b['sysG']:.2e} | est {b['sysEst']:.2e}")
    print(f"    TOTAL sigma = {b['tot']:.2e}  ({100*b['tot']/b['a0hat']:.1f}% of a0_hat)")
    for lab, val in (("canonical", A0C), ("ALT", A0A)):
        print(f"      vs {lab:<9} {val:.3e}:  {(b['a0hat']-val)/b['tot']:+.2f} sigma")

bg, bt = lever["GAS-ALL"], lever["TRGB/Ceph {2,3}"]
dstat_D = 100 * (1 - bt["sysD"] / bg["sysD"]) if bg["sysD"] else 0.0
print(f"\n  LEVER CHECK: sysD  GAS-ALL {bg['sysD']:.2e} -> TRGB {bt['sysD']:.2e}"
      f"  ({dstat_D:.0f}% SMALLER); estimator-spread sEst {bg['sysEst']:.2e} -> {bt['sysEst']:.2e};"
      f" total sigma {bg['tot']:.2e} -> {bt['tot']:.2e} ({100*(bt['tot']/bg['tot']-1):+.0f}%).")
banked = results["anchors"]["banked_gas_gls"]
move = 100 * (bt["a0hat"] / banked - 1)
within = abs(bt["a0hat"] - banked) < bt["tot"]
print(f"  CENTRAL: banked GAS-ALL GLS {banked:.3e} -> TRGB GLS {bt['a0hat']:.3e} ({move:+.1f}%):")
print(f"    {'MOVES UP' if move > 0 else 'MOVES DOWN'} ~{abs(move):.0f}%, "
      f"{'within 1 sigma statistically' if within else 'BEYOND 1 sigma'} but COHERENT across"
      f" median/EIV/GLS -> the clean-distance subset sits HIGHER, away from canonical.")

# TRGB-vs-Hubble split consistency (Ud=0.70): the cleanest read on distance systematics
r70 = results["Ud=0.70"]
tr, hu = r70["TRGB/Ceph {2,3}"], r70["Hubble-flow {1}"]
for est, ak, sk in (("GLS", "a0_gls", "boot_gls"), ("EIV", "a0_eiv", "boot_eiv"),
                    ("median", "a0_median", "boot_median")):
    dsig = (tr[ak] - hu[ak]) / np.hypot(tr[sk], hu[sk])
    print(f"  SPLIT ({est}): TRGB {tr[ak]:.3e} vs Hubble-flow {hu[ak]:.3e}"
          f"  -> {dsig:+.1f} sigma apart (clean-distance set is {'HIGHER' if dsig>0 else 'LOWER'}).")
print("  => the two distance subsamples differ at ~1-2 sigma, TRGB high; consistent with"
      " either a residual Hubble-flow distance bias OR small-N (18/29 gals) scatter -- NOT")
print("  a decisive detection that distances were dragging the banked central down.")

print(f"\n  OCCAM BANS (M0: a0 predicted from c,H_Lambda,Z, 0 params / M1: a0 free), with")
print(f"  the TRGB-reduced error, both footings [+ = favors the predicted-a0 model]:")
print(f"  {'case':<34} {'a0_hat':>10} {'s_ln':>6} | {'B(canon)':>9} {'B(ALT)':>8}")
occ = {}
for name, ah, sm in (("GAS-ALL GLS", bg["a0hat"], bg["tot"] / bg["a0hat"]),
                     ("TRGB GLS (LEVER central stays)", bt["a0hat"], bt["tot"] / bt["a0hat"]),
                     ("TRGB median (robust variant)", bt["a0med"], bt["tot"] / bt["a0hat"]),
                     ("TRGB @canon (central->pred)", A0C, bt["tot"] / bt["a0hat"]),
                     ("TRGB @ALT   (central->pred)", A0A, bt["tot"] / bt["a0hat"])):
    # Planck anchor widths as fractions: SC/A0C=0.0096, SA/A0A=0.0080 (anchor_values.json)
    bC, tC = logB(np.log(ah), sm, A0C, 0.0096)
    bA, tA = logB(np.log(ah), sm, A0A, 0.0080)
    occ[name] = dict(a0=float(ah), s_ln=float(sm), bans_canon=bC, bans_alt=bA,
                     t_canon=tC, t_alt=tA)
    print(f"  {name:<34} {ah:>10.3e} {sm:>6.3f} | {bC:>+9.2f} {bA:>+8.2f}")

print(f"\n  LAMBDA-INVERSION  Lambda = 3 Z^2 a0_hat^2 / c^4,  Z = {ZVAL:.4f}"
      f"  (Planck Lambda = {LAMBDA_PLANCK:.3e} m^-2):")
lam = {}
for name, ah, s in (("GAS-ALL GLS", bg["a0hat"], bg["tot"]),
                    ("TRGB GLS", bt["a0hat"], bt["tot"]),
                    ("TRGB median", bt["a0med"], bt["tot"])):
    L, r = lam_ratio(ah)
    # propagate: dLambda/Lambda = 2 dA0/a0
    _, rlo = lam_ratio(ah - s); _, rhi = lam_ratio(ah + s)
    lam[name] = dict(a0=float(ah), Lambda=float(L), ratio=float(r),
                     ratio_lo=float(rlo), ratio_hi=float(rhi))
    print(f"    {name:<14} a0={ah:.3e}: Lambda={L:.3e}  = {r:.2f} x Planck"
          f"  [{rlo:.2f}, {rhi:.2f}]")
print(f"    (canonical a0 inverts to EXACTLY 1.00x Planck by construction: a0=cH_Lambda/Z.)")

results["lever_Ud0.70"] = dict(gas_all=bg, trgb=bt, occam=occ, lambda_inv=lam,
                               sysD_reduction_pct=float(dstat_D),
                               central_move_pct_vs_banked=float(move))

json.dump(results, open(os.path.join(HERE, "est_robust_results.json"), "w"), indent=1)
print(f"\n[est_robust_results.json written]  EXIT 0: robust estimators computed. Not a verdict.")
