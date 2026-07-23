#!/usr/bin/env python3
"""
================================================================================
BAO KILL-SWITCH MAP + THE GALAXY-LIMITED ASYMMETRY  (FOCUSED BAO CALC, 2026-07-23)
de Sitter-Unruh MODIFIED-INERTIA framework  --  what BAO decides, and what it does NOT
================================================================================

BUILDS ON / REUSES (does NOT modify or contradict) the committed parents:
    a0z_prediction_band_2026.py   -- FROZEN a0(z)/a0(0) band, FULL non-monotonic law, DR2 posteriors
    desi_posterior_a0z.py         -- correlated-posterior MC, decline significance
    forecast_rubin_a0z.py         -- SNe-Ia forecast (a DIFFERENT probe; this file is BAO)
    ../a0_line/reach_target.py    -- STEP A galaxy floor (SPARC-alone ~11%, best campaign ~7.7%)
    ../a0_line/per_galaxy_budget.py
Same law, same DR2 (w0,wa) posteriors, same 2x2 correlated Cholesky MC (seed 0). The parent
z=3 medians and part-(iii) sigma_pred are reproduced here as REGRESSION ANCHORS; the Step-A
floor / target percentages are read straight from the committed JSON and asserted.

--------------------------------------------------------------------------------
THE PHYSICS (be precise -- this is why BAO is a KILL SWITCH, not a measurement of a0)
--------------------------------------------------------------------------------
* BAO is a ~0.5% STANDARD RULER. The sound horizon r_drag is set PRE-recombination, in the
  HIGH-acceleration regime where the framework's a0-effects vanish (g >> a0), so r_drag is
  the SAME as in LCDM. BAO therefore carries NO clean, independent a0 signal: it does not
  measure a0 directly. What it measures is D_A(z), H(z) -> rho_DE(z) / the expansion history.
* In the framework a0 = c H_Lambda / Z = c^2 sqrt(Lambda/32pi) is PREDICTED from Lambda, and
  the Friedmann term is H^2 = (8piG/3) rho_m + Z^2 a0(z)^2/c^2, i.e. Z^2 a0(z)^2/c^2 == the
  rho_DE-equivalent. Hence  a0(z)/a0(0) = sqrt( rho_DE(z)/rho_DE0 ). BAO pins rho_DE(z) to
  ~1% => it pins the PREDICTED a0(z) curve razor-sharp (the sqrt HALVES the fractional error).
* SO BAO'S ROLE IS A KILL SWITCH ON THE PREDICTION, NOT A MEASUREMENT OF a0:
    - It decides WHICH BRANCH the framework is on (does DE evolve => is a0(z) forced off flat?).
    - The distinctive MI test is whether the INDEPENDENT galaxy-dynamics a0(z) equals that curve.
    - The razor is on the cosmology PREDICTION; the confrontation is bottlenecked by the GALAXY
      MEASUREMENT, which Step A shows is floored at ~11% (SPARC-alone) / ~7.7% (best campaign).

--------------------------------------------------------------------------------
THE THREE-BRANCH KILL SWITCH (decided by BAO's LCDM-exclusion significance S on (w0,wa))
--------------------------------------------------------------------------------
    BRANCH-DISSOLVE   S < 1 sigma : w consistent with -1 => rho_DE ~ const => a0(z) ~ FLAT.
                      The framework's prediction collapses to constant-a0 MOND. The a0(z)
                      channel is UNFALSIFIABLE. A REAL, load-bearing weakness -- stated plainly.
    BRANCH-AMBIGUOUS  1 <= S < 3  : DE leans evolving but is not forced; the galaxy test is
                      underpowered / inconclusive.
    BRANCH-LIVE       S >= 3 sigma: w != -1 confidently => framework is FORCED to a specific
                      DECLINING a0(z). A galaxy measurement of CONSTANT a0(z) then KILLS it.

HARD CALIBRATION (manufactured win == manufactured deficit; this repo has a history of both):
 (1) The BAO razor is on the PREDICTION, not the measurement. Do NOT claim BAO settles the
     a0 anchor. The galaxy side (~11% floor / ~7.7% best campaign) is the bottleneck -- quantify
     the asymmetry, do not paper over it.
 (2) DR3/DR5 (w0,wa) forecasts are MODEST: error ~ 1/sqrt(effective volume). DESI DR2 ~3yr,
     final ~5yr => sqrt(5/3)~1.29x from DESI volume; with contemporaneous SNe (DES-5yr, Union3,
     later Rubin) + CMB (ACT/SPT, later CMB-S4) the (w0,wa) tightening reaches ~1.3-1.8x, NOT
     order-of-magnitude. These forecasts are labelled by PRECISION MILESTONE, not release name.
 (3) The DISSOLVE branch (w->-1 => unfalsifiable) is a REAL weakness -- it is a whole section.
 (4) a0(z)/a0(0) RATIO is FOOTING-INDEPENDENT (parent sympy proof); only the absolute a0(0)
     differs (canonical 9.36e-11 vs alt 1.13e-10). Razor is on the ratio + the Planck-Lambda
     anchor. No 'theory closed'. Every load-bearing number is computed by a runnable line below.
================================================================================
"""
import numpy as np, os, json, math
from scipy.special import erfcinv

HERE = os.path.dirname(os.path.abspath(__file__))
ALINE = os.path.join(HERE, "..", "a0_line")
bar = "=" * 96

# ================================================================================
# SHARED LAW + DESI DR2 POSTERIORS + CORRELATED-POSTERIOR MC  (identical to parents)
# ================================================================================
def a0ratio(z, W0, WA):
    """FULL non-monotonic closed form a0(z)/a0(0); NEVER Taylor-truncated, never drop the wa exp."""
    return (1.0 + z)**(1.5*(1.0 + W0 + WA)) * np.exp(-1.5*WA*z/(1.0 + z))

def mc_pair(w0, sw0, wa, swa, corr, N=400000):
    """2x2 correlated Cholesky draw over (w0,wa); seed 0 -- parity with the parent scripts."""
    L = np.linalg.cholesky(np.array([[sw0**2, corr*sw0*swa], [corr*sw0*swa, swa**2]]))
    g = np.random.default_rng(0)
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        pr = np.array([w0, wa]) + g.standard_normal((N, 2)) @ L.T
    return pr[:, 0], pr[:, 1]

def maha_from_lcdm(w0, sw0, wa, swa, corr):
    """LCDM-exclusion significance S = Mahalanobis distance of (w0,wa) from (-1,0) in the 2D
    marginal (Gaussian approx to DESI's full profile-likelihood; agrees with the quoted
    2.8/4.2/3.8 sigma to ~5-7%)."""
    C = np.array([[sw0**2, corr*sw0*swa], [corr*sw0*swa, swa**2]])
    d = np.array([w0 + 1.0, wa - 0.0])
    return float(np.sqrt(d @ np.linalg.inv(C) @ d))

# DESI DR2 (2025) w0waCDM marginals (arXiv:2503.14738 / 2504.15336); (label, w0, sw0, wa, swa, corr, quoted-S)
DR2 = [
    ("DESI+CMB+Pantheon+", -0.838, 0.055, -0.62, 0.22, -0.86, 2.8),
    ("DESI+CMB+DESY5",     -0.752, 0.057, -0.86, 0.22, -0.86, 4.2),
    ("DESI+CMB+Union3",    -0.667, 0.088, -1.09, 0.31, -0.87, 3.8),
]
ZTEST = [0.35, 1.0, 2.0, 3.0]
A0C, A0A = 9.36e-11, 1.13e-10                      # canonical (rho_DE/cH_Lambda) ; alt (rho_total/cH0)
DIRECT_RAZOR = 0.01                               # sig_pred from DIRECT BAO rho_DE recon (~2% -> a0 ~1%)
BAO_ZMAX = 2.3                                    # DESI direct rho_DE reach (Lya); beyond -> CPL extrapolation only

# forecast (w0,wa)-error TIGHTENING factors -- MODEST, ~1/sqrt(volume) (calibration rule 2)
FORECAST = [("DR2  (now, ~3yr)",              1.00),
            ("DR3  (~5yr DESI-final class)",  1.30),
            ("DR5  (Stage-V + CMB-S4 class)", 1.80)]

print("#"*96)
print("# BAO KILL-SWITCH MAP + GALAXY-LIMITED ASYMMETRY  --  DESI w0waCDM  --  FOCUSED BAO CALC 2026-07-23")
print("# Law: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z))  [FULL]")
print("# BAO measures rho_DE(z) (a ~0.5% ruler), NOT a0. It is a KILL SWITCH on the PREDICTION.")
print("#"*96)

# ================================================================================
# S0 -- REGRESSION ANCHORS (parent band z=3 medians + part-(iii) sigma_pred; Step-A floors)
# ================================================================================
print("\n" + bar); print("S0 -- REGRESSION ANCHORS (reproduce parents exactly; read Step-A committed floors)"); print(bar)
PARENT_MED3 = {"DESI+CMB+Pantheon+": 0.775, "DESI+CMB+DESY5": 0.737, "DESI+CMB+Union3": 0.706}
PARENT_SPRED3 = {"DESI+CMB+Pantheon+": 0.099, "DESI+CMB+DESY5": 0.092, "DESI+CMB+Union3": 0.118}
sig_pred_DR2 = {}   # (label,z) -> (median, sigma_pred) at DR2 precision
for label, w0, sw0, wa, swa, corr, qS in DR2:
    W0, WA = mc_pair(w0, sw0, wa, swa, corr)
    for z in ZTEST:
        r = a0ratio(z, W0, WA)
        sig_pred_DR2[(label, z)] = (float(np.median(r)), float(np.std(r)))
    m3, s3 = sig_pred_DR2[(label, 3.0)]
    dM, dS = abs(m3 - PARENT_MED3[label]), abs(s3 - PARENT_SPRED3[label])
    assert dM <= 0.004 and dS <= 0.004, (label, m3, s3, dM, dS)
    print(f"  {label:20} z=3: median={m3:.3f} (parent {PARENT_MED3[label]:.3f}, d={dM:.4f}) "
          f"sigma_pred={s3:.3f} (parent {PARENT_SPRED3[label]:.3f}, d={dS:.4f})  [OK]")
# Step-A galaxy floor (committed JSON) -- the MEASUREMENT bottleneck
rt = json.load(open(os.path.join(ALINE, "reach_target_results.json")))
GAL_TARGET_ANCHOR = rt["target_pct"]              # 6.31% : 3s canon-vs-ALT (the ABSOLUTE anchor, z~0)
GAL_FLOOR_SPARC   = rt["best_sparc_alone_pct"]    # 11.62%: SPARC-alone best
GAL_BEST_CAMPAIGN = json.load(open(os.path.join(ALINE, "per_galaxy_budget_results.json")))["ladder"][-1]["box_frac"]*100  # 7.68%
print(f"  Step-A (committed): SPARC-alone floor = {GAL_FLOOR_SPARC:.2f}% ; best dedicated campaign = "
      f"{GAL_BEST_CAMPAIGN:.2f}% ; absolute-anchor target = {GAL_TARGET_ANCHOR:.2f}%  [read from JSON]")
print("  NOTE: those Step-A percentages are the LOCAL (z~0) a0-slope floor. Transporting even the")
print("  best-case ~7.7% to z=2-3 is OPTIMISTIC (high-z kinematics are turbulence/beam-smearing")
print("  starved); they are used here as the galaxy-side BENCHMARK, the friendliest one available.")

# ================================================================================
# S1 -- THE RAZOR: BAO pins rho_DE(z) => the PREDICTED a0(z) curve (sqrt halves the error)
#       sigma_pred(z) from propagating the (w0,wa) covariance at each BAO precision milestone
# ================================================================================
print("\n" + bar); print("S1 -- THE BAO RAZOR ON THE PREDICTION: sigma_pred(z) of a0(z)/a0(0) at DR2/DR3/DR5"); print(bar)
print("  sigma(a0)/a0 = 0.5 * sigma(rho_DE)/rho_DE  (the sqrt).  DIRECT BAO rho_DE(z) at the")
print("  well-measured pivot (z~0.5-1) is ~1-3%, so a0(z) there is pinned to ~0.5-1.5% -- the")
print("  razor. The CPL-PROPAGATED band below is the conservative (w0,wa)-extrapolation width;")
print("  it is ~1.5% near the low-z bump and widens only on EXTRAPOLATION out to z=3.")
razor = {}   # (label, fac_label, z) -> (median, sigma_pred)
print(f"\n  {'dataset':20} {'precision':28} | " + " | ".join(f"sig_pred(z={z})" for z in ZTEST))
for label, w0, sw0, wa, swa, corr, qS in DR2:
    for flab, fac in FORECAST:
        W0, WA = mc_pair(w0, sw0/fac, wa, swa/fac, corr)   # tighten (w0,wa) errors by 1/fac
        cells = []
        for z in ZTEST:
            r = a0ratio(z, W0, WA)
            razor[(label, flab, z)] = (float(np.median(r)), float(np.std(r)))
            cells.append(f"{100*np.std(r):11.2f}%")
        print(f"  {label:20} {flab:28} | " + " | ".join(cells))
print(f"\n  TWO PREDICTION MODELS carried explicitly (the honest distinction):")
print(f"   * DIRECT razor : where BAO has a direct rho_DE(z) bin (z<~{BAO_ZMAX}), rho_DE ~1-3% -> a0(z) pinned")
print(f"     to ~0.5-1.5%. Benchmark sig_pred_direct = {100*DIRECT_RAZOR:.0f}%. This is the task's '~1% razor'.")
print(f"   * CPL-propagated: the conservative parent band above (couples w0,wa; EXTRAPOLATES). ~1.5% at")
print(f"     the z~0.35 bump, but ~7-10% by z=2-3. At z>~{BAO_ZMAX} ONLY this model applies (no direct bin).")
print("  The confrontation conclusion is reported under BOTH models in S4 (robust to the choice).")

# ================================================================================
# S2 -- THE KILL-SWITCH MAP: branch as a function of (TRUE deviation from LCDM, BAO precision)
# ================================================================================
print("\n" + bar); print("S2 -- THE THREE-BRANCH KILL-SWITCH MAP  (branch set by LCDM-exclusion S on (w0,wa))"); print(bar)
def branch(S):
    return "DISSOLVE" if S < 1.0 else ("LIVE" if S >= 3.0 else "AMBIG")
# S at DR2 from Mahalanobis (cross-check vs quoted), then scaled by the precision factor.
print("  (a) DR2 exclusion S: Mahalanobis(2D-marginal) vs DESI-quoted, then DR3/DR5 = S * fac:")
S_DR2 = {}
print(f"  {'dataset':20} {'S_maha':>7} {'S_quoted':>9}  |  " + "  ".join(f"{fl.split()[0]:>6}" for fl, _ in FORECAST))
for label, w0, sw0, wa, swa, corr, qS in DR2:
    Sm = maha_from_lcdm(w0, sw0, wa, swa, corr)
    S_DR2[label] = Sm
    scaled = "  ".join(f"{Sm*fac:>5.1f}{'*' if branch(Sm*fac)=='LIVE' else ('.' if branch(Sm*fac)=='DISSOLVE' else '~'):<1}" for _, fac in FORECAST)
    print(f"  {label:20} {Sm:>7.2f} {qS:>9.1f}  |  {scaled}   [{branch(Sm)} @ DR2]")
print("     legend: *=LIVE(S>=3)  ~=AMBIG(1<=S<3)  .=DISSOLVE(S<1).  This row ASSUMES the")
print("     DESI-central (w0,wa) is the TRUTH (DE evolves) -- then tighter BAO STRENGTHENS LIVE.")

# (b) the full 2D map: if the TRUE deviation from LCDM is a fraction f_true of the DESI-central
# deviation, S(true, precision) = S_DR2_central * f_true * fac. Shows the DISSOLVE risk directly.
print("\n  (b) 2D MAP -- branch vs (true deviation from LCDM as fraction of DESI-central) x (BAO precision).")
print("      Uses the Pantheon+ anchor (most conservative DR2 S=%.2f). S = S_anchor * f_true * fac." % S_DR2["DESI+CMB+Pantheon+"])
Sanchor = S_DR2["DESI+CMB+Pantheon+"]
ftrues = [("LCDM truth (f=0.00)", 0.00), ("quarter (f=0.25)", 0.25), ("half (f=0.50)", 0.50),
          ("DESI-central (f=1.00)", 1.00), ("stronger (f=1.25)", 1.25)]
print(f"  {'true deviation':24} | " + " | ".join(f"{fl.split()[0]:^14}" for fl, _ in FORECAST))
print(f"  {'-'*24}-+-" + "-+-".join("-"*14 for _ in FORECAST))
for tlab, ft in ftrues:
    cells = []
    for flab, fac in FORECAST:
        S = Sanchor * ft * fac
        cells.append(f"{S:4.1f}s {branch(S):8}")
    print(f"  {tlab:24} | " + " | ".join(f"{c:^14}" for c in cells))
print("  READING: along the DESI-central row the test is ALREADY LIVE at DR2 and hardens. But if")
print("  the truth is nearer LCDM (upper rows) BAO tightening drives S DOWN into DISSOLVE -- the")
print("  SAME data either confirms LIVE or forces DISSOLVE. BAO decides WHICH; it is the fulcrum.")

# placement of the three real DR2 datasets, propagated to DR3/DR5 (DESI-central truth)
print("\n  (c) PLACEMENT of the three real DESI DR2 combos (assuming DE evolves at the DESI-central rate):")
for label, w0, sw0, wa, swa, corr, qS in DR2:
    row = []
    for flab, fac in FORECAST:
        S = S_DR2[label]*fac
        row.append(f"{flab.split()[0]}={S:.1f}s[{branch(S)}]")
    print(f"    {label:20}: " + "  ".join(row))
print("    => DR2 is ALREADY LIVE for DESY5 & Union3 and borderline (AMBIG->LIVE) for Pantheon+;")
print("       DR3/DR5 push all three firmly LIVE *IF* DE evolves. The branch is live TODAY, modulo")
print("       the DISSOLVE risk in S3 -- BAO's job (deciding IF) is essentially already done, sharp.")

# ================================================================================
# S3 -- THE DISSOLVE BRANCH quantified (the honest unfalsifiability weakness)
# ================================================================================
print("\n" + bar); print("S3 -- BRANCH-DISSOLVE: the real unfalsifiability risk if BAO regresses toward w=-1"); print(bar)
lam = a0ratio(np.array(ZTEST), -1.0, 0.0)
print(f"  exact: at (w0,wa)=(-1,0), a0(z)/a0(0) at z={ZTEST} = {np.round(lam,6)}  -> FLAT 1.000 for all z.")
print("  => if DE does not evolve, the framework's a0(z) is EXACTLY constant and INDISTINGUISHABLE")
print("     from constant-a0 MOND. The a0(z) channel is then UNFALSIFIABLE (not falsified -- untestable).")
# slide along the DESI (Pantheon+) degeneracy toward (-1,0); where does the z=3 test die (<1s from flat)?
sw0, swa, corr = 0.055, 0.22, -0.86
slope = -0.62/(1 - 0.838)                          # wa/(1+w0) ~ -3.83
crossed = None
for eps in np.linspace(0.162, 0.0, 82):
    W0, WA = mc_pair(-1+eps, sw0, slope*eps, swa, corr)
    r3 = a0ratio(3.0, W0, WA)
    if crossed is None and abs(np.median(r3)-1.0)/np.std(r3) < 1.0:
        crossed = (eps, float(np.median(r3)))
eps_c, med_c = crossed
print(f"  slide along the DESI degeneracy (slope wa/(1+w0)={slope:.2f}) toward (-1,0), DR2 errors:")
print(f"    z=3 separation-from-flat drops below 1 sigma once |1+w0| <~ {eps_c:.3f}  (median a0(3)/a0(0) ~ {med_c:.3f}).")
print(f"    Current Pantheon+ central |1+w0| = 0.162 -> the decline is only ~2 sigma even now.")
print("  This is a load-bearing weakness: the ENTIRE discriminating power of the a0(z) channel is")
print("  INHERITED from DESI's evolving-DE hint being real. If DR3/DR5 relax to w=-1, the channel")
print("  DISSOLVES. It is not proven here -- BAO is the sole arbiter of whether the test lives.")

# ================================================================================
# S4 -- THE ASYMMETRY: razor prediction (~1%) vs galaxy floor (~11%/7.7%) => galaxy-limited
#       required galaxy precision for 3s GIVEN BRANCH-LIVE, per z, both bottlenecks separated
# ================================================================================
print("\n" + bar); print("S4 -- THE ASYMMETRY (the crux): cosmology razor vs galaxy floor ~11%/7.7%"); print(bar)
print("  Separation-from-flat significance combines BOTH sides in quadrature:")
print("     sep(z) = |ratio(z)-1| / sqrt( sigma_pred(z)^2 + sigma_gal^2 )")
print("  Required galaxy precision for a 3-sigma kill GIVEN BRANCH-LIVE:")
print("     sigma_gal_req(z) = sqrt( (|ratio-1|/3)^2 - sigma_pred(z)^2 )   [real only if the razor")
print("     leaves room; if |ratio-1|/3 <= sigma_pred the node is COSMOLOGY-CEILING-limited, not galaxy].")
print("  (deep-MOND penalty, parent rule 4: the UNDERLYING RC precision must be sigma_gal_req/2.)")
HEAD = "DESI+CMB+DESY5"                                # mid combo, firmly LIVE (LCDM-excl 4.2s)
def req_gal(eff, sp):
    inside = (eff/3.0)**2 - sp**2
    return math.sqrt(inside) if inside > 0 else float('nan')     # NaN => cosmology-ceiling-limited
print(f"\n  [{HEAD}, firmly LIVE at {S_DR2[HEAD]:.1f}s]  req galaxy precision under the DIRECT razor (1%)")
print(f"  and under the CPL-propagated band at DR2/DR3/DR5. Galaxy benchmarks: 7.7% best / 11% floor.")
print(f"  {'z':>5} | {'ratio':>6} | {'effect':>7} | {'req(direct1%)':>13} | "
      f"{'req(CPL DR2)':>12} | {'req(CPL DR3)':>12} | {'req(CPL DR5)':>12}")
print(f"  {'-'*5}-+-{'-'*6}-+-{'-'*7}-+-{'-'*13}-+-{'-'*12}-+-{'-'*12}-+-{'-'*12}")
asym = {}
def cell(v):
    return "   null   " if v == "null" else (f"{100*v:>7.2f}%  " if np.isfinite(v) else " cosmo-ceil ")
for z in ZTEST:
    med = razor[(HEAD, "DR2  (now, ~3yr)", z)][0]
    eff = abs(med - 1.0)
    if eff < 0.02:
        rd = r2 = r3 = r5 = "null"
    else:
        rd = req_gal(eff, DIRECT_RAZOR)
        r2 = req_gal(eff, razor[(HEAD, "DR2  (now, ~3yr)", z)][1])
        r3 = req_gal(eff, razor[(HEAD, "DR3  (~5yr DESI-final class)", z)][1])
        r5 = req_gal(eff, razor[(HEAD, "DR5  (Stage-V + CMB-S4 class)", z)][1])
    asym[z] = dict(ratio=med, effect=eff, req_direct=rd, req_cpl_dr2=r2, req_cpl_dr3=r3, req_cpl_dr5=r5)
    print(f"  {z:>5.2f} | {med:>6.3f} | {100*eff:>6.1f}% | {cell(rd):>13} | "
          f"{cell(r2):>12} | {cell(r3):>12} | {cell(r5):>12}")
print("  READING (the asymmetry, both models, stated plainly):")
print("   * z=0.35 (bump ~6%): req ~2% galaxy precision (either model) -- ~4x below the 7.7% best")
print("     campaign, and it is exactly where a0 is hardest to measure (barely deep-MOND, low z). Dead.")
print("   * z=1 (crossover): ratio ~ 1 (null) -> the test is structurally UNTESTABLE at the crossover.")
print("   * z=2 (data sweet spot, effect ~14%): DIRECT razor -> req ~4.5% (< 7.7% best -> GALAXY-limited,")
print("     unreachable); CPL band at DR2 is COSMOLOGY-ceiling-limited (theory ceiling ~2s), needing")
print("     DR3/DR5 razor-sharpening BEFORE galaxies even matter. z<~2.3 is where a direct BAO bin exists.")
print("   * z=3 (effect ~26%, BEYOND the direct-BAO reach -> CPL only): req ~8.7% (direct-equiv) but at")
print("     DR2 the CPL razor (sig_pred ~9%) caps the ceiling ~2.8s; DR3->req 5.2%, DR5->req 7.1%. This is")
print("     the ONLY node the 7.7% best campaign could reach -- and z=3 kinematics are the most data-starved.")

# bottleneck split -- WHERE the razor is free (direct-BAO z<2.3) vs where it CO-BINDS (z=3 extrap)
print("\n  WHERE IS THE RAZOR FREE? variance-share of the quadrature (galaxy = 7.7% best campaign):")
print(f"  {'node':36} | {'sig_pred':>8} | {'sig_gal':>8} | {'BAO var%':>8} | {'gal var%':>8} | {'sep':>6}")
sg = GAL_BEST_CAMPAIGN/100
def vshare(sp, sgg):
    return 100*sp**2/(sp**2+sgg**2), 100*sgg**2/(sp**2+sgg**2)
med2d = razor[(HEAD, "DR2  (now, ~3yr)", 2.0)][0]; eff2 = abs(med2d-1.0)
bp, gp = vshare(DIRECT_RAZOR, sg)
print(f"  {'z=2, DIRECT razor (z<2.3, BAO bin)':36} | {100*DIRECT_RAZOR:>7.2f}% | {100*sg:>7.2f}% | "
      f"{bp:>7.0f}% | {gp:>7.0f}% | {eff2/math.hypot(DIRECT_RAZOR,sg):>5.2f}s")
med5 = sp5 = None
for flab, fac in FORECAST:
    med, sp = razor[(HEAD, flab, 3.0)]
    eff = abs(med-1.0); bp, gp = vshare(sp, sg)
    print(f"  {'z=3, CPL razor '+flab.split()[0]+' (z>2.3, extrap)':36} | {100*sp:>7.2f}% | {100*sg:>7.2f}% | "
          f"{bp:>7.0f}% | {gp:>7.0f}% | {eff/math.hypot(sp,sg):>5.2f}s")
    if flab.startswith("DR5"): med5, sp5 = med, sp
print("  READING (the asymmetry, PRECISELY -- NOT 'razor free everywhere'):")
print("   * z<~2.3 (BAO measures rho_DE DIRECTLY): razor ~1% is negligible vs the 7.7% galaxy floor")
print("     -> the confrontation is ~98% GALAXY-limited, the razor IS essentially free. But the effect")
print("     is small (<=14%) and req ~4.5% < 7.7% best -> galaxy-UNREACHABLE. This is the true asymmetry.")
print("   * z=3 (BEYOND direct BAO -> CPL EXTRAPOLATION): the razor is NOT free -- at DR2 the extrapolated")
print("     sig_pred (~9%) actually DOMINATES the error (~59% of variance), flipping to galaxy-dominated")
print("     (~69%) only by DR5. At the one node with a big effect, BAO CO-BINDS until DR5, THEN galaxies.")
print(f"   * NET: best galaxy campaign at z=3 tops out {eff/math.hypot(sp5,sg):.2f}s (DR5) -- still < a clean 3s.")
# what galaxy precision WOULD give a clean 3s at z=3 with a razor-limited (DR5) prediction?
need = math.sqrt(max((abs(med5-1.0)/3.0)**2 - sp5**2, 0.0))
print(f"  With a DR5 razor (sig_pred~{100*sp5:.1f}% at z=3), a clean 3s kill needs sigma_gal <= {100*need:.1f}%")
print(f"  -- vs 7.7% best campaign / 11% SPARC-alone floor. The remaining gap is on the galaxy side.")

# ================================================================================
# S5 -- SYNTHESIS + FROZEN one-liner + honesty caveats + JSON
# ================================================================================
print("\n" + bar); print("S5 -- SYNTHESIS (BAO decides IF; galaxies decide the OUTCOME; DISSOLVE is the real risk)"); print(bar)
ONE = ("BAO decides IF the a0(z) test is live and does so RAZOR-SHARP (it pins the predicted a0(z) "
       "curve to ~0.5-1% via rho_DE, having never measured a0 directly); GALAXIES decide the OUTCOME "
       "and are the sole bottleneck (~11% floor / ~7.7% best campaign, worse at high z); and the "
       "DISSOLVE branch -- if DESI regresses to w=-1 -- makes the channel UNFALSIFIABLE, a real weakness.")
print("  ONE-LINE:")
for i in range(0, len(ONE), 92):
    print("    " + ONE[i:i+92])
print("\n  BRANCH PLACEMENT (today): DESI DR2 is ALREADY BRANCH-LIVE (DESY5 4.2s, Union3 3.8s; Pantheon+")
print("  2.8s borderline). DR3/DR5 harden LIVE ~1.3-1.8x IF DE evolves, or collapse to DISSOLVE if it")
print("  does not. The test's liveness is essentially settled and sharp; its outcome is not fundable")
print("  with existing galaxy data.")
print("\n  THE ASYMMETRY IN ONE NUMBER: at the DIRECT-BAO redshifts (z<~2.3) the prediction precision")
print(f"  is ~0.5-1.5% (razor) vs a galaxy floor ~{GAL_FLOOR_SPARC:.0f}% (SPARC-alone) / ~{GAL_BEST_CAMPAIGN:.1f}% (best campaign) -- the razor")
print(f"  is ~{GAL_BEST_CAMPAIGN/1.0:.0f}-{GAL_FLOOR_SPARC/1.0:.0f}x sharper, so there the confrontation is ~98% GALAXY-limited. The one CAVEAT: at")
print("  z=3 (beyond direct-BAO reach) the CPL-EXTRAPOLATED razor co-binds and even dominates at DR2,")
print("  clearing only by DR5. Net: galaxies are the wall wherever the test is reachable; BAO is not.")

CAVEATS = [
 "BAO does NOT measure a0. r_drag is set pre-recombination at g>>a0 (standard ruler), so BAO "
 "carries no clean independent a0 signal. Its role is a KILL SWITCH on the PREDICTION (which "
 "branch), via rho_DE(z) -> the predicted a0(z)=a0(0)sqrt(rho_DE(z)/rho_DE0). Do not overclaim.",
 "The razor is razor-sharp (~0.5-1.5%) where BAO actually measures (z<~2); it softens on CPL "
 "EXTRAPOLATION to z=3 (sigma_pred ~7-12% at DR2). DR3/DR5 tighten it ~1.3-1.8x -- MODEST, "
 "~1/sqrt(volume), NOT order-of-magnitude (DESI 3yr->5yr = sqrt(5/3)~1.29x; external SNe/CMB the rest).",
 "Where the test is reachable it is GALAXY-limited. Required galaxy a0(z) precision for a 3-sigma "
 "kill: ~2% at the z~0.35 bump, ~4.5% at z~2 (direct-BAO regime), ~8-9% at z=3 -- vs a ~11% SPARC-"
 "alone floor / ~7.7% best dedicated campaign (Step A). Only z=3 is even marginally reachable, and "
 "z=3 galaxy kinematics are the most data-starved. z~2 has usable data but needs ~4.5% (< 7.7% best).",
 "TWO ceilings, kept separate and NOT conflated: (i) at z<~2.3 BAO measures rho_DE directly so the "
 "razor (~1%) is negligible -> ~98% galaxy-limited; (ii) at z=3 the CPL-EXTRAPOLATED sig_pred (~9% at "
 "DR2) actually DOMINATES the error (~59% variance) and co-binds until DR5 lifts it. The best galaxy "
 "campaign at z=3 still tops out ~2.3-2.9 sigma (DR2->DR5) -- below a clean 3s. Do NOT claim 'razor free everywhere'.",
 "BRANCH-DISSOLVE is a REAL unfalsifiability weakness: if BAO relaxes to w=-1 the predicted a0(z) is "
 "EXACTLY flat and indistinguishable from constant-a0 MOND. The z=3 decline already dies (<1s from flat) "
 "once |1+w0|<~0.08; the current 0.162 gives only ~2s. The channel's power is INHERITED, not proven.",
 "The a0(z)/a0(0) RATIO is FOOTING-INDEPENDENT (parent sympy proof: Z, a0(0), c, H all cancel). Only "
 "the ABSOLUTE a0(z)=ratio*a0(0) carries the footing (canonical 9.36e-11 vs alt 1.13e-10). The razor "
 "is on the ratio + the Planck-Lambda anchor.",
 "The Step-A ~11%/7.7% are the LOCAL (z~0) a0-slope floor; using them at z=2-3 is OPTIMISTIC. This is "
 "the friendliest galaxy benchmark, and it STILL does not clear a clean 3s at the only reachable node. "
 "No 'theory closed': BAO's liveness verdict is sharp and near-settled; the galaxy outcome is unfunded.",
]
print("\n  FROZEN HONESTY CAVEATS (each load-bearing, none overrideable):")
for i, c in enumerate(CAVEATS, 1):
    print(f"   {i}. " + c)

# ---------- JSON ----------
out = dict(
    law="a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE0)=(1+z)^{1.5(1+w0+wa)}exp(-1.5 wa z/(1+z))",
    branches=dict(DISSOLVE="S<1s (w~-1): a0(z) flat, UNFALSIFIABLE",
                  AMBIG="1<=S<3s: underpowered", LIVE="S>=3s: forced declining a0(z), galaxy-flat kills"),
    forecast_tightening={fl: fac for fl, fac in FORECAST},
    DR2_exclusion_sigma={lab: dict(maha=S_DR2[lab], quoted=qS) for lab, *_ , qS in [(d[0],)+tuple(d[1:]) for d in DR2]},
    branch_placement={lab: {fl.split()[0]: dict(S=S_DR2[lab]*fac, branch=branch(S_DR2[lab]*fac))
                            for fl, fac in FORECAST} for lab in [d[0] for d in DR2]},
    razor_sigma_pred_pct={f"{lab}|{fl.split()[0]}|z{z}": 100*razor[(lab, fl, z)][1]
                          for lab in [d[0] for d in DR2] for fl, _ in FORECAST for z in ZTEST},
    galaxy_floor_pct=dict(sparc_alone=GAL_FLOOR_SPARC, best_campaign=GAL_BEST_CAMPAIGN,
                          absolute_anchor_target=GAL_TARGET_ANCHOR),
    asymmetry_z3=dict(effect=asym[3.0]["effect"], sig_pred_cpl_DR2=razor[(HEAD,"DR2  (now, ~3yr)",3.0)][1],
                      req_gal_3s_direct=asym[3.0]["req_direct"], req_gal_3s_cpl_DR2=asym[3.0]["req_cpl_dr2"],
                      req_gal_3s_cpl_DR3=asym[3.0]["req_cpl_dr3"], req_gal_3s_cpl_DR5=need,
                      best_campaign=GAL_BEST_CAMPAIGN/100,
                      sep_bestcampaign_DR2=abs(razor[(HEAD,"DR2  (now, ~3yr)",3.0)][0]-1)/math.hypot(razor[(HEAD,"DR2  (now, ~3yr)",3.0)][1], GAL_BEST_CAMPAIGN/100),
                      sep_bestcampaign_DR5=abs(med5-1)/math.hypot(sp5, GAL_BEST_CAMPAIGN/100)),
    asymmetry_z2=dict(effect=asym[2.0]["effect"], req_gal_3s_direct=asym[2.0]["req_direct"],
                      req_gal_3s_cpl_DR2=asym[2.0]["req_cpl_dr2"]),
    dissolve_threshold_1plusw0=eps_c,
    one_line=ONE, caveats=CAVEATS, a0_canon=A0C, a0_alt=A0A)
json.dump(out, open(os.path.join(HERE, "bao_killswitch_a0z_results.json"), "w"), indent=1, default=float)
print("\n[bao_killswitch_a0z_results.json written]")

# ================================================================================
# SELF-CHECK (frozen invariants)
# ================================================================================
print("\n" + bar); print("SELF-CHECK (frozen invariants)"); print(bar)
# 1. DR2 already LIVE for DESY5 & Union3 (borderline AMBIG for Pantheon+, S~3.0 vs quoted 2.8)
assert branch(S_DR2["DESI+CMB+DESY5"]) == "LIVE" and branch(S_DR2["DESI+CMB+Union3"]) == "LIVE"
# 2. LCDM truth => DISSOLVE at every precision (the unfalsifiability branch)
assert all(branch(Sanchor*0.0*fac) == "DISSOLVE" for _, fac in FORECAST)
# 3. DESI-central truth => LIVE by DR3 & DR5 on the MOST CONSERVATIVE (Pantheon+) anchor
assert branch(Sanchor*1.0*1.30) == "LIVE" and branch(Sanchor*1.0*1.80) == "LIVE"
# 4. galaxy-limited: best campaign at z=3 stays below a clean 3s even at the DR5 razor
assert abs(med5-1)/math.hypot(sp5, GAL_BEST_CAMPAIGN/100) < 3.0
# 5. under the DIRECT razor, req galaxy precision at z=2 is BELOW the 7.7% best campaign (unreachable)
req2_direct = req_gal(asym[2.0]["effect"], DIRECT_RAZOR)
assert np.isfinite(req2_direct) and req2_direct < GAL_BEST_CAMPAIGN/100, (req2_direct, GAL_BEST_CAMPAIGN/100)
# 6. at DR2 the CPL band is cosmology-ceiling-limited at z=2 (theory ceiling < 3s regardless of galaxies)
assert not np.isfinite(asym[2.0]["req_cpl_dr2"])
print("  1. DESI DR2 already BRANCH-LIVE for DESY5 & Union3 (Pantheon+ borderline ~3.0s)  OK")
print("  2. LCDM truth (f=0) => BRANCH-DISSOLVE at DR2/DR3/DR5 (unfalsifiable)            OK")
print("  3. DESI-central truth => BRANCH-LIVE by DR3 & DR5 (conservative Pantheon+ anchor) OK")
print(f"  4. best galaxy campaign at z=3 tops out {abs(med5-1)/math.hypot(sp5, GAL_BEST_CAMPAIGN/100):.2f}s < 3s even at the DR5 razor    OK")
print(f"  5. direct-razor req galaxy precision at z=2 ({100*req2_direct:.1f}%) < 7.7% best (galaxy-unreachable) OK")
print("  6. CPL band at DR2, z=2 is COSMOLOGY-ceiling-limited (needs DR3/DR5 razor first)  OK")
print("  SELF-CHECK PASSED.")
print("\nEXIT 0: BAO kill-switch map + galaxy-limited asymmetry computed. Exit code is not a verdict.")
