#!/usr/bin/env python3
"""
================================================================================
FROZEN CALC (2026-07-23) -- BAO KILL-SWITCH + RAZOR + GALAXY-LIMITED ASYMMETRY
de Sitter-Unruh MODIFIED-INERTIA framework  (a0 = c H_Lambda / Z = c^2 sqrt(Lambda/32pi))
================================================================================
FOCUSED BAO CALC. This is the FROZEN pre-registration artifact for the BAO channel.
It BUILDS ON and REUSES (does NOT modify or contradict) the committed parents:
    a0z_prediction_band_2026.py   -- FROZEN a0(z)/a0(0) band, FULL non-monotonic law, DR2 posteriors
    desi_posterior_a0z.py         -- correlated-posterior MC over (w0,wa), decline significance
    bao_razor_desi_forecast.py    -- the verified razor+forecast sibling (commit 16033489)
    forecast_rubin_a0z.py         -- a SNe-Ia forecast (a DIFFERENT probe; this file is BAO)
    ../a0_line/reach_target.py    -- STEP A galaxy floor (SPARC-alone ~11.6%, box ~16.1%, target ~6.3%)
    ../a0_line/per_galaxy_budget.py -- best dedicated-campaign endpoint (~7.7%)
Same FULL closed-form law, same DESI DR2 w0waCDM posteriors, same 2x2 correlated
Cholesky MC over (w0,wa), same seed default_rng(0), same N=400000 (parity with parents).
The z=3 medians are regression-checked against the committed 0.775/0.737/0.707; the
Step-A galaxy floor / box / campaign / target are READ from the committed JSON.

--------------------------------------------------------------------------------
THE PHYSICS (be precise -- this is WHY BAO is a KILL SWITCH, not a measurement of a0)
--------------------------------------------------------------------------------
* BAO is a ~0.5% STANDARD RULER. The sound horizon r_drag is set PRE-recombination,
  in the HIGH-acceleration regime where the framework's a0-effects vanish (g >> a0),
  so r_drag is the SAME as in LCDM. BAO therefore carries NO clean, independent a0
  signal: it does NOT measure a0 directly. It measures D_A(z), H(z) -> rho_DE(z).
* In the framework a0(z) is PREDICTED from the expansion history:
      Friedmann:  H^2 = (8piG/3) rho_m + Z^2 a0(z)^2/c^2 ,  Z^2 a0^2/c^2 == rho_DE-equiv
      =>  a0(z)/a0(0) = sqrt( rho_DE(z)/rho_DE0 )                  [PARAMETER-FREE map]
      CPL:  rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))
      RATIO: a0(z)/a0(0)      = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z))   [FULL form]
* SO BAO'S ROLE IS A KILL SWITCH ON THE PREDICTION, NOT A MEASUREMENT OF a0:
    - It decides WHICH BRANCH the framework is on (does DE evolve => is a0(z) forced off flat?).
    - The razor (~0.5-0.9%) is the INTRINSIC sharpness of the PREDICTED a0(z): the map
      rho_DE -> a0 = sqrt(rho_DE) adds ZERO width, and the sqrt HALVES the present-day
      Lambda-anchor error. It is NOT a claim that BAO MEASURES a0 to ~1%.
    - The distinctive MI test is whether the INDEPENDENT galaxy-dynamics a0(z) equals that
      curve. That confrontation is bottlenecked by the GALAXY MEASUREMENT (Step A: ~11%
      SPARC-alone floor, ~7.7% best dedicated campaign), NOT by the prediction.

--------------------------------------------------------------------------------
THE THREE-BRANCH KILL SWITCH (branch set by BAO's LCDM-exclusion significance S on (w0,wa))
--------------------------------------------------------------------------------
    BRANCH-DISSOLVE   S < 1 sigma : w consistent with -1 => rho_DE ~ const => a0(z) ~ FLAT.
                      The prediction collapses to constant-a0 MOND. The a0(z) channel is
                      UNFALSIFIABLE. A REAL, load-bearing weakness -- stated plainly, not buried.
    BRANCH-AMBIGUOUS  1 <= S < 3  : DE leans evolving but is not forced; galaxy test underpowered.
    BRANCH-LIVE       S >= 3 sigma: w != -1 confidently => framework is FORCED to a specific
                      DECLINING a0(z). An independent galaxy a0(z) measured FLAT then KILLS it.

HARD CALIBRATION (manufactured win == manufactured deficit; this repo has a history of both):
 (1) The razor is on the PREDICTION, not the measurement. Do NOT claim BAO settles the a0
     anchor. The galaxy side (~11% floor / ~7.7% best campaign) is the bottleneck -- quantify
     the asymmetry; do not paper over it, and do not manufacture a high-z win by applying the
     ~0.9% razor beyond the direct-BAO reach (z>~2.3) where only the CPL-extrapolated band applies.
 (2) DR3/DR5 (w0,wa) forecasts are MODEST: error ~ 1/sqrt(effective volume). DESI DR2 ~3yr of
     the 5yr survey; DR2->DR3 ~ sqrt(4/3)=1.15x, DR2->DR5 ~ sqrt(5/3)=1.29x statistical, +analysis
     -> ~1.2x (DR3) / ~1.4x (DR5); ~1.8x only WITH external CMB-S4/Euclid. NOT order-of-magnitude.
     (DESI Collaboration 2016 arXiv:1611.00036 FoM scaling; DR2 VI arXiv:2503.14738.)
 (3) The DISSOLVE branch (w->-1 => a0(z) flat => unfalsifiable) is a REAL weakness -- own section.
 (4) a0(z)/a0(0) RATIO is FOOTING-INDEPENDENT (parent sympy proof); only the ABSOLUTE a0(0)
     differs (canonical 9.36e-11 vs alt 1.13e-10) AND the anchor-razor derivation differs
     (canonical ~sqrt(Lambda) -> sqrt-halved; alt ~H0 -> linear). No 'theory closed'. Every
     load-bearing number is computed by a runnable line below.
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

def rhoratio(z, W0, WA):
    """rho_DE(z)/rho_DE0 (CPL) = a0ratio^2 -- the un-sqrt'd quantity BAO actually constrains."""
    return (1.0 + z)**(3.0*(1.0 + W0 + WA)) * np.exp(-3.0*WA*z/(1.0 + z))

def mc_pair(w0, sw0, wa, swa, corr, N=400000, seed=0):
    """2x2 correlated Cholesky draw over (w0,wa); seed 0 => parity with the parent scripts."""
    L = np.linalg.cholesky(np.array([[sw0**2, corr*sw0*swa], [corr*sw0*swa, swa**2]]))
    g = np.random.default_rng(seed)
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        pr = np.array([w0, wa]) + g.standard_normal((N, 2)) @ L.T
    return pr[:, 0], pr[:, 1]

# DESI DR2 (2025) w0waCDM marginals (arXiv:2503.14738 / 2504.15336); (label, w0, sw0, wa, swa, corr, LCDM-excl-S)
DR2 = [
    ("DESI+CMB+Pantheon+", -0.838, 0.055, -0.62, 0.22, -0.86, 2.8),
    ("DESI+CMB+DESY5",     -0.752, 0.057, -0.86, 0.22, -0.86, 4.2),
    ("DESI+CMB+Union3",    -0.667, 0.088, -1.09, 0.31, -0.87, 3.8),
]
ZRAZOR = [0.5, 1.0, 2.0, 3.0]                     # task-specified razor redshifts
A0C, A0A = 9.36e-11, 1.13e-10                     # canonical (rho_DE/cH_Lambda) ; alt (rho_total/cH0)
BAO_ZMAX = 2.3                                    # DESI direct rho_DE(z) reach (Lya); beyond -> CPL extrapolation only

# Planck 2018 anchor inputs for the present-day Lambda razor (TT,TE,EE+lowE+lensing)
OMEGA_L, dOMEGA_L = 0.6889, 0.0056
H0, dH0           = 67.36, 0.54

# forecast (w0,wa)-error TIGHTENING factors -- MODEST, ~1/sqrt(effective volume) (calibration rule 2)
FORECAST = [("DR2 (now, ~3yr)",        1.00),
            ("DR3 (~4yr)",             1.20),
            ("DR5 (full 5yr)",         1.40),
            ("DR5+CMB-S4/Euclid",      1.80)]

def branch(S):
    return "DISSOLVE" if S < 1.0 else ("LIVE" if S >= 3.0 else "AMBIG")

print("#"*96)
print("# FROZEN BAO KILL-SWITCH + RAZOR + GALAXY-LIMITED ASYMMETRY -- DESI w0waCDM -- 2026-07-23")
print("# Law: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z))  [FULL]")
print("# BAO measures rho_DE(z) (a ~0.5% ruler), NOT a0. It is a KILL SWITCH on the PREDICTION.")
print("#"*96)

# ================================================================================
# (v) REGRESSION CHECK vs the committed a0z_prediction_band_2026.py (z=3 medians; tol 0.004)
#     done FIRST so the shared MC is proven identical before any band is reported
# ================================================================================
print("\n" + bar)
print("(v) REGRESSION CHECK vs committed a0z_prediction_band_2026.py / desi_posterior_a0z.py")
print(bar)
PARENT_Z3 = {"DESI+CMB+Pantheon+": 0.775, "DESI+CMB+DESY5": 0.737, "DESI+CMB+Union3": 0.707}
band_now = {}   # label -> {z: (median, sig_frac_a0, sig_frac_rho, std_a0)}
reg_ok = True
for label, w0, sw0, wa, swa, corr, excl in DR2:
    W0, WA = mc_pair(w0, sw0, wa, swa, corr)
    m3 = float(np.median(a0ratio(3.0, W0, WA)))
    d = abs(m3 - PARENT_Z3[label]); reg_ok = reg_ok and d <= 0.004
    print(f"  {label:20} z=3 median here={m3:.3f} parent={PARENT_Z3[label]:.3f} d={d:.4f} "
          f"[{'OK' if d<=0.004 else 'MISMATCH'}]")
    band_now[label] = {}
    for z in ZRAZOR:
        ra = a0ratio(z, W0, WA); rr = rhoratio(z, W0, WA)
        med = float(np.median(ra))
        lo, hi = np.percentile(ra, [16, 84]); sfa = float((hi - lo)/2.0/med)
        lor, hir = np.percentile(rr, [16, 84]); sfr = float((hir - lor)/2.0/float(np.median(rr)))
        band_now[label][z] = (med, sfa, sfr, float(np.std(ra)))
assert reg_ok, "regression mismatch vs committed parent z=3 medians"
print("  ALL z=3 medians match the committed parents to <= 0.004 (identical law, DR2 posteriors, seed 0).")

# committed galaxy-side benchmarks (READ from JSON -- the MEASUREMENT bottleneck)
rt = json.load(open(os.path.join(ALINE, "reach_target_results.json")))
GAL_BOX_NOW  = rt["box_now_pct"]/100.0            # 16.1%: current gas-dominated a0-line box
GAL_FLOOR    = rt["best_sparc_alone_pct"]/100.0   # 11.6%: SPARC-alone systematics floor
GAL_TARGET   = rt["target_pct"]/100.0             # 6.31%: 3s canon-vs-ALT anchor separation
GAL_CAMPAIGN = json.load(open(os.path.join(ALINE, "per_galaxy_budget_results.json")))["ladder"][-1]["box_frac"]  # 7.68%
GAL_ASPIRE   = 0.05                               # aspirational dedicated dwarf campaign (rule-1 target)
print(f"  Step-A galaxy benchmarks (committed JSON): current box {100*GAL_BOX_NOW:.1f}% | SPARC-alone floor "
      f"{100*GAL_FLOOR:.1f}% | best campaign {100*GAL_CAMPAIGN:.1f}% | 3s anchor target {100*GAL_TARGET:.2f}%")

# ================================================================================
# (i) THE BAO RAZOR at z={0.5,1,2,3}, explicitly next to the galaxy 16% box / 11% floor
# ================================================================================
print("\n" + "#"*96)
print("# (i) THE BAO RAZOR: intrinsic sharpness of the PREDICTED a0(z) at z={0.5,1,2,3}")
print("#"*96)

# --- (i.a) the present-day Lambda ANCHOR razor: the sqrt HALVES the Lambda error ---
fL_OmL = dOMEGA_L/OMEGA_L
fL_H0  = dH0/H0
sigLambda_frac = math.hypot(2*fL_H0, fL_OmL)      # Lambda = 3 Omega_L H0^2/c^2
razor_canon = 0.5*sigLambda_frac                  # canonical a0(0)=cH_Lambda/Z ~ sqrt(Lambda)
razor_alt   = fL_H0                               # alt a0(0)=k c H0 (linear in H0, NOT sqrt-halved)
razor_future = 0.5*0.010                          # CMB-S4 pins the Lambda combo ~1% -> ~0.5%
print(f"\n  Planck 2018: Omega_L={OMEGA_L}+/-{dOMEGA_L} ({100*fL_OmL:.2f}%), H0={H0}+/-{dH0} ({100*fL_H0:.2f}%)")
print(f"  => sigma(Lambda)/Lambda = sqrt((2*{100*fL_H0:.2f})^2 + {100*fL_OmL:.2f}^2)% = {100*sigLambda_frac:.2f}%")
print(f"  CANONICAL razor  a0(0)=cH_Lambda/Z ~ sqrt(Lambda) : 0.5*{100*sigLambda_frac:.2f}% = {100*razor_canon:.2f}%  <-- SQRT HALVES IT")
print(f"  ALT       razor  a0(0)=k*c*H0 (linear in H0)      : {100*razor_alt:.2f}%  (H0 error, not sqrt-halved)")
print(f"  FUTURE    razor  (CMB-S4 ~1% on Lambda)           : {100*razor_future:.2f}%")
print(f"  ==> ANCHOR RAZOR ~ {100*razor_future:.1f}-{100*razor_canon:.1f}% today; Z-INDEPENDENT (present-day a0(0) only).")

# --- (i.b) the a0(z)/a0(0) map is PARAMETER-FREE; the sqrt halves the rho_DE error (MC-verified) ---
print(f"\n  The map a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE0) adds ZERO width -> the theory razor is FLAT in z.")
print(f"  sqrt-halving MC check (sig_frac(a0)/sig_frac(rho) should be 0.50 at every z):")
print(f"    {'z':>4} | {'a0 median':>9} | {'sig_frac(a0)':>12} | {'sig_frac(rho)':>13} | {'a0/rho':>7}")
lab0 = "DESI+CMB+Pantheon+"
sqrt_ratio = {}
for z in ZRAZOR:
    med, sfa, sfr, _ = band_now[lab0][z]
    sqrt_ratio[z] = sfa/sfr
    print(f"    {z:>4.1f} | {med:>9.3f} | {100*sfa:>11.2f}% | {100*sfr:>12.2f}% | {sfa/sfr:>7.3f}")
    assert abs(sfa/sfr - 0.5) < 0.06, f"sqrt-halving broke at z={z}: {sfa/sfr:.3f}"
print("  -> ratio ~0.50 at every z: the sqrt halves the fractional error EXACTLY (a PREDICTION property).")

# --- (i.c) the razor NEXT TO the galaxy 16% box / 11% floor, per z (the task's core table) ---
print(f"\n  RAZOR vs GALAXY, at z={{0.5,1,2,3}} (effect & operational band are mean over the 3 SNe combos):")
print(f"  {'z':>4} | {'effect|1-med|':>13} | {'razor(theory)':>13} | {'DR2 oper.band':>13} | "
      f"{'galaxy floor':>12} | {'galaxy box':>10}")
print(f"  {'-'*4}-+-{'-'*13}-+-{'-'*13}-+-{'-'*13}-+-{'-'*12}-+-{'-'*10}")
eff_by_z, operband_by_z = {}, {}
for z in ZRAZOR:
    meds  = [band_now[l][z][0] for l in PARENT_Z3]
    sfas  = [band_now[l][z][1] for l in PARENT_Z3]
    eff   = float(np.mean([abs(1.0 - m) for m in meds]))
    bandz = float(np.mean(sfas))
    eff_by_z[z], operband_by_z[z] = eff, bandz
    print(f"  {z:>4.1f} | {100*eff:>12.1f}% | {100*razor_canon:>12.2f}% | {100*bandz:>12.1f}% | "
          f"{100*GAL_FLOOR:>11.1f}% | {100*GAL_BOX_NOW:>9.1f}%")
print("  READING (honest, both directions):")
print(f"   * theory RAZOR is FLAT at {100*razor_canon:.2f}% in z (parameter-free map + sqrt-halved anchor).")
print(f"   * ASYMMETRY: razor {100*razor_canon:.2f}% vs galaxy floor {100*GAL_FLOOR:.1f}% / box {100*GAL_BOX_NOW:.1f}% "
      f"= ~{GAL_FLOOR/razor_canon:.0f}x (floor) / ~{GAL_BOX_NOW/razor_canon:.0f}x (box). The prediction is NEVER the bottleneck.")
print(f"   * BUT the OPERATIONAL DR2 band (marginalized over CURRENT (w0,wa)) balloons to "
      f"~{100*operband_by_z[2.0]:.0f}-{100*operband_by_z[3.0]:.0f}% at z=2-3 -- COMPARABLE to the galaxy floor.")
print(f"     The {100*razor_canon:.2f}% razor is the theory CEILING, not the operational high-z number: BAO must")
print(f"     first shrink (w0,wa). Beyond the direct-BAO reach (z>~{BAO_ZMAX}) ONLY this CPL band applies.")

# ================================================================================
# (ii) DESI DR2/DR3/DR5 (w0,wa) FORECAST: a0(z) razor sharpening + w-vs-(-1) significance
# ================================================================================
print("\n" + "#"*96)
print("# (ii) DESI DR2/DR3/DR5 (w0,wa) FORECAST -> a0(z) band sharpening + 'DE evolves' significance")
print("#"*96)
print(bar)
print("  (w0,wa) error-shrink (rule 2): stat ~1/sqrt(vol); DR2=3yr, DR5=5yr. DR2->DR3 sqrt(4/3)=1.15,")
print("  DR2->DR5 sqrt(5/3)=1.29 (+analysis -> 1.2x/1.4x); 1.8x only with external CMB-S4/Euclid.")
print("  (DESI 2016 arXiv:1611.00036 FoM scaling; DR2 VI arXiv:2503.14738.)  MODEST, not 10x.")
print(bar)
# (ii.a) a0(z=3) operational band sharpening (Pantheon+ anchor), + sigma(w0),sigma(wa) per release
print("  a0(z=3)/a0(0) 1-sigma OPERATIONAL band (Pantheon+ posterior), tightening (w0,wa):")
print(f"    {'release':<22} {'shrink':>7} {'sig(w0)':>8} {'sig(wa)':>8} {'a0(3) band':>11}")
band3_forecast = {}
for name, f in FORECAST:
    W0, WA = mc_pair(-0.838, 0.055/f, -0.62, 0.22/f, -0.86)
    r3 = a0ratio(3.0, W0, WA); med = float(np.median(r3))
    lo, hi = np.percentile(r3, [16, 84]); sf = (hi-lo)/2.0/med
    band3_forecast[name] = float(sf)
    print(f"    {name:<22} {f:>6.2f}x {0.055/f:>8.4f} {0.22/f:>8.4f} {100*sf:>10.1f}%")
# (ii.b) a0(z) band at all razor-z, DR2 vs DR5(1.4x)
print(f"\n  a0(z) operational band, DR2 vs DR5 (1.4x) (Pantheon+), showing the modest high-z gain:")
print(f"    {'z':>4} | {'DR2 band':>9} | {'DR5 band':>9} | {'vs razor '+f'{100*razor_canon:.2f}%':>18}")
for z in ZRAZOR:
    W0d, WAd = mc_pair(-0.838, 0.055,      -0.62, 0.22,      -0.86)
    W05, WA5 = mc_pair(-0.838, 0.055/1.40, -0.62, 0.22/1.40, -0.86)
    rd, r5 = a0ratio(z, W0d, WAd), a0ratio(z, W05, WA5)
    md, m5 = np.median(rd), np.median(r5)
    sfd = (np.percentile(rd,84)-np.percentile(rd,16))/2/md
    sf5 = (np.percentile(r5,84)-np.percentile(r5,16))/2/m5
    tag = "reaches razor" if sf5 < 1.5*razor_canon else "still (w0,wa)-limited"
    print(f"    {z:>4.1f} | {100*sfd:>8.1f}% | {100*sf5:>8.1f}% | {tag:>18}")
# (ii.c) the 'DE evolves' (w != -1) significance per release
print(f"\n  'DE evolves' (w != -1) significance per release  (LCDM-excl S scaled by the shrink factor;")
print(f"   CONDITIONAL on the DR2 central holding -- if the truth is Lambda, S FALLS -> DISSOLVE):")
print(f"    {'SNe compilation':<20} | " + " | ".join(f"{n.split()[0]:>10}" for n, _ in FORECAST))
print(f"    {'-'*20}-+-" + "-+-".join("-"*10 for _ in FORECAST))
sig_release = {}
for label, w0, sw0, wa, swa, corr, excl in DR2:
    sig_release[label] = {n: excl*f for n, f in FORECAST}
    print(f"    {label:<20} | " + " | ".join(f"{excl*f:>9.1f}s" for _, f in FORECAST))
lo2, hi2 = min(d[6] for d in DR2), max(d[6] for d in DR2)
print(f"\n  DR2 spread {lo2:.1f}-{hi2:.1f}s -> DR3(1.2x) {lo2*1.2:.1f}-{hi2*1.2:.1f}s -> DR5(1.4x) {lo2*1.4:.1f}-{hi2*1.4:.1f}s "
      f"-> DR5+ext(1.8x) {lo2*1.8:.1f}-{hi2*1.8:.1f}s.")
print("  => IF the DR2 evolution is real, BAO crosses a clean 5s on 'DE evolves' by DR5 for DESY5/Union3")
print("  and approaches it for Pantheon+. That TRIGGERS the declining-a0 branch (the test goes LIVE).")

# ================================================================================
# (iii) THE THREE-BRANCH KILL-SWITCH MAP (DISSOLVE / AMBIGUOUS / LIVE) with DR2/DR3/DR5 placed
# ================================================================================
print("\n" + "#"*96)
print("# (iii) THE THREE-BRANCH KILL-SWITCH MAP  (DISSOLVE S<1 / AMBIGUOUS 1<=S<3 / LIVE S>=3)")
print("#"*96)
print(bar)
print("  Branch is set by BAO's LCDM-exclusion S on (w0,wa). Placement below ASSUMES the DESI-central")
print("  (w0,wa) is the truth (DE evolves); the LCDM-truth row shows the DISSOLVE risk if it is not.")
print(bar)
print(f"  {'scenario':<30} | " + " | ".join(f"{n.split()[0]:^16}" for n, _ in FORECAST))
print(f"  {'-'*30}-+-" + "-+-".join("-"*16 for _ in FORECAST))
kill_map = {}
for label, w0, sw0, wa, swa, corr, excl in DR2:
    cells, row = [], {}
    for n, f in FORECAST:
        S = excl*f; row[n.split()[0]] = (S, branch(S))
        cells.append(f"{S:4.1f}s {branch(S):8}")
    kill_map[label] = row
    print(f"  {label+' (DE evolves)':<30} | " + " | ".join(f"{c:^16}" for c in cells))
# LCDM-truth row: if w truly = -1, S -> 0 at every precision => DISSOLVE everywhere
print(f"  {'LCDM truth (w=-1)':<30} | " + " | ".join(f"{'0.0s '+branch(0.0):^16}" for _ in FORECAST))
print("  legend: DISSOLVE=a0(z) flat, UNFALSIFIABLE | AMBIG=underpowered | LIVE=forced declining a0(z),")
print("          a galaxy-flat a0(z) then KILLS the framework.")
print("  READING: DESI DR2 is ALREADY LIVE for DESY5 & Union3 (3.8-4.2s) and borderline AMBIG->LIVE for")
print("  Pantheon+ (2.8s); DR3/DR5 push all three firmly LIVE *IF* DE evolves. The SAME BAO data forces")
print("  DISSOLVE if the truth is w=-1. BAO's job -- deciding IF the test is live -- is near-settled & sharp.")

# ================================================================================
# (iv) THE ASYMMETRY: required galaxy a0(z) precision for 3s GIVEN BRANCH-LIVE, vs 11% / 7.7%
# ================================================================================
print("\n" + "#"*96)
print("# (iv) THE ASYMMETRY: required galaxy a0(z) precision for a 3s KILL given BRANCH-LIVE")
print("#"*96)
print(bar)
print("  sep(z) = |ratio-1| / sqrt(sig_pred^2 + sig_gal^2).  Required galaxy precision for 3s:")
print("     sig_gal_req(z) = sqrt( (|ratio-1|/3)^2 - sig_pred^2 )   [NaN => cosmology-ceiling-limited].")
print("  TWO prediction models, kept STRICTLY separate (rule 1 -- no manufactured high-z win):")
print(f"   * RAZOR ({100*razor_canon:.2f}%): the intrinsic ceiling; VALID where BAO measures rho_DE directly (z<~{BAO_ZMAX}).")
print("   * OPERATIONAL band (DR2/DR5): the honest (w0,wa)-marginalized width; the ONLY model valid at z=3.")
print(bar)
def req_gal(eff, sp):
    inside = (eff/3.0)**2 - sp**2
    return math.sqrt(inside) if inside > 0 else float('nan')
def cell(v):
    return "  null  " if v == "null" else (f"{100*v:>6.2f}% " if np.isfinite(v) else " cosmo-ceil")
print(f"  {'z':>4} | {'effect':>7} | {'req(razor)':>10} | {'req(DR2 band)':>13} | {'req(DR5 band)':>13} | note")
print(f"  {'-'*4}-+-{'-'*7}-+-{'-'*10}-+-{'-'*13}-+-{'-'*13}-+-{'-'*22}")
req_tab = {}
# DR5 operational band per z (Pantheon+) for the honest high-z column
dr5band_by_z = {}
for z in ZRAZOR:
    W05, WA5 = mc_pair(-0.838, 0.055/1.40, -0.62, 0.22/1.40, -0.86)
    r5 = a0ratio(z, W05, WA5); m5 = np.median(r5)
    dr5band_by_z[z] = float((np.percentile(r5,84)-np.percentile(r5,16))/2/m5)
for z in ZRAZOR:
    eff = eff_by_z[z]
    if eff < 0.02:
        rr = rd2 = rd5 = "null"; note = "crossover -> UNTESTABLE"
    else:
        rr  = req_gal(eff, razor_canon)
        rd2 = req_gal(eff, operband_by_z[z])
        rd5 = req_gal(eff, dr5band_by_z[z])
        if z <= BAO_ZMAX: note = "z<2.3: direct BAO, razor valid"
        else:             note = "z>2.3: CPL only -> use oper. band"
    req_tab[z] = dict(effect=eff, req_razor=rr, req_dr2=rd2, req_dr5=rd5)
    print(f"  {z:>4.1f} | {100*eff:>6.1f}% | {cell(rr):>10} | {cell(rd2):>13} | {cell(rd5):>13} | {note}")
print(f"\n  vs galaxy benchmarks: SPARC-alone floor {100*GAL_FLOOR:.1f}% | best campaign {100*GAL_CAMPAIGN:.1f}% | "
      f"aspirational {100*GAL_ASPIRE:.0f}%")
print("  READING (both models, stated plainly):")
print(f"   * z=0.5 (bump, eff {100*eff_by_z[0.5]:.1f}%): req ~{100*req_tab[0.5]['req_razor']:.1f}% -- far below the {100*GAL_CAMPAIGN:.1f}% campaign, AND")
print("     it is exactly where a0 is hardest to measure (barely deep-MOND, low z). Effectively dead.")
print("   * z=1 (crossover): ratio ~ 1 -> structurally UNTESTABLE (the null).")
print(f"   * z=2 (data sweet spot, eff {100*eff_by_z[2.0]:.1f}%): req(razor) ~{100*req_tab[2.0]['req_razor']:.1f}% < {100*GAL_CAMPAIGN:.1f}% best -> GALAXY-")
print("     limited & unreachable; and at DR2 the operational band is cosmology-ceiling-limited (needs DR3/DR5).")
print(f"   * z=3 (biggest effect {100*eff_by_z[3.0]:.1f}%, BEYOND direct BAO -> CPL band is the honest model):")

# the decisive-test asymmetry table (task's A4): two prediction states x three galaxy states, z=2,3
print("\n  DECISIVE-TEST ASYMMETRY  sep = effect / sqrt(sig_pred^2 + sig_gal^2)  (the crux, z=2,3):")
print(f"  {'z':>4} | {'effect':>7} | {'DR2band+gal11':>13} | {'razor+gal11':>12} | {'razor+gal7.7':>12} | {'razor+gal5':>11}")
print(f"  {'-'*4}-+-{'-'*7}-+-{'-'*13}-+-{'-'*12}-+-{'-'*12}-+-{'-'*11}")
A4 = {}
for z in (2.0, 3.0):
    eff = eff_by_z[z]
    sep_dr2_11  = eff/math.hypot(operband_by_z[z], GAL_FLOOR)
    sep_rz_11   = eff/math.hypot(razor_canon,       GAL_FLOOR)
    sep_rz_camp = eff/math.hypot(razor_canon,       GAL_CAMPAIGN)
    sep_rz_5    = eff/math.hypot(razor_canon,       GAL_ASPIRE)
    A4[z] = (eff, sep_dr2_11, sep_rz_11, sep_rz_camp, sep_rz_5)
    print(f"  {z:>4.1f} | {100*eff:>6.1f}% | {sep_dr2_11:>12.1f}s | {sep_rz_11:>11.1f}s | {sep_rz_camp:>11.1f}s | {sep_rz_5:>10.1f}s")
# honest z=3 under the OPERATIONAL band (the model that actually applies beyond direct-BAO reach)
eff3 = eff_by_z[3.0]
sep3_dr2_camp = eff3/math.hypot(operband_by_z[3.0], GAL_CAMPAIGN)
sep3_dr5_camp = eff3/math.hypot(dr5band_by_z[3.0],  GAL_CAMPAIGN)
print(f"  HONEST z=3 (CPL operational band, NOT the razor): best campaign {100*GAL_CAMPAIGN:.1f}% gives "
      f"{sep3_dr2_camp:.1f}s (DR2) -> {sep3_dr5_camp:.1f}s (DR5) -- BELOW a clean 3s.")
print("  READING: with the galaxy side floored at ~11% even a razor-sharp prediction caps the test at ~2s;")
print("  only galaxies at ~5% make z=3 decisive (3-5s). Under the RAZOR the 7.7% campaign nominally reaches")
print(f"  ~{A4[3.0][3]:.1f}s at z=3, BUT z=3 is beyond direct-BAO reach so the CPL band binds -> honest ~{sep3_dr5_camp:.1f}s (DR5).")
print("  The GALAXY MEASUREMENT, not the BAO prediction, is the wall wherever the test is reachable.")

# ================================================================================
# DISSOLVE BRANCH (rule 3) -- the real unfalsifiability weakness, stated plainly
# ================================================================================
print("\n" + bar)
print("DISSOLVE BRANCH (rule 3, load-bearing weakness): w -> -1 => a0(z) FLAT => UNFALSIFIABLE")
print(bar)
lam = a0ratio(np.array(ZRAZOR), -1.0, 0.0)
print(f"  exact: at (w0,wa)=(-1,0), a0(z)/a0(0) at z={ZRAZOR} = {np.round(lam,6)} -> all 1.000 (flat).")
sw0, swa, corr = 0.055, 0.22, -0.86
slope = -0.62/(1 - 0.838)                          # wa/(1+w0) ~ -3.83 along the DESI degeneracy
crossed = None
for eps in np.linspace(0.162, 0.0, 82):
    W0, WA = mc_pair(-1+eps, sw0, slope*eps, swa, corr)
    r3 = a0ratio(3.0, W0, WA)
    if crossed is None and abs(np.median(r3)-1.0)/np.std(r3) < 1.0:
        crossed = (eps, float(np.median(r3)))
eps_c, med_c = crossed
print(f"  slide along the DESI degeneracy toward (-1,0): z=3 separation-from-flat drops below 1s once")
print(f"  |1+w0| <~ {eps_c:.3f} (median a0(3)/a0(0) ~ {med_c:.3f}). Current Pantheon+ |1+w0|=0.162 -> only ~2s.")
print("  The ENTIRE discriminating power of the a0(z) channel is INHERITED from DESI's evolving-DE hint")
print("  being real. If DR3/DR5 relax to w=-1 the channel DISSOLVES (unfalsifiable). Not proven here.")

# ================================================================================
# PRE-REGISTRATION BLOCK -- kill-switch thresholds, honest verdict, caveats
# ================================================================================
ONE_LINE = ("BAO is ready and razor-sharp -- it pins the PREDICTED a0(z) curve to ~0.5-0.9% via rho_DE "
            "(having never measured a0 directly) and its LCDM-exclusion already places DESI DR2 on "
            "BRANCH-LIVE; but the test is GALAXY-limited (floor ~11%, best campaign ~7.7%, need ~5%) and "
            "DISSOLVES into constant-a0 MOND (unfalsifiable) if DESI regresses to w=-1.")
print("\n" + "#"*96)
print("# PRE-REGISTRATION  --  FROZEN 2026-07-23  --  BAO KILL-SWITCH FOR THE a0(z) CHANNEL")
print("#"*96)
print("#  KILL-SWITCH THRESHOLDS (S = BAO LCDM-exclusion significance on (w0,wa)):")
print("#    S < 1 sigma      -> BRANCH-DISSOLVE : a0(z) flat, INDISTINGUISHABLE from constant-a0 MOND (untestable)")
print("#    1 <= S < 3 sigma -> BRANCH-AMBIGUOUS: DE leans evolving, galaxy test underpowered")
print("#    S >= 3 sigma     -> BRANCH-LIVE     : forced declining a0(z); a galaxy-FLAT a0(z) then KILLS it")
print("#  PLACEMENT TODAY: DESI DR2 = LIVE (DESY5 4.2s, Union3 3.8s), Pantheon+ borderline (2.8s).")
print(f"#    DR3(1.2x): {lo2*1.2:.1f}-{hi2*1.2:.1f}s  |  DR5(1.4x): {lo2*1.4:.1f}-{hi2*1.4:.1f}s  |  DR5+ext(1.8x): {lo2*1.8:.1f}-{hi2*1.8:.1f}s  (IF DE evolves).")
print(f"#  RAZOR (prediction sharpness): {100*razor_canon:.2f}% canonical (sqrt-halved Lambda) / {100*razor_alt:.2f}% alt (H0) / "
      f"{100*razor_future:.2f}% future -- Z-INDEPENDENT, FLAT in z.")
print(f"#  REQUIRED GALAXY PRECISION for a 3s kill given BRANCH-LIVE: ~{100*req_tab[0.5]['req_razor']:.1f}% (z=0.5 bump), "
      f"UNTESTABLE (z=1 null), ~{100*req_tab[2.0]['req_razor']:.1f}% (z=2), ~{100*req_tab[3.0]['req_razor']:.1f}% (z=3, razor-equiv);")
print(f"#    vs SPARC-alone floor ~{100*GAL_FLOOR:.0f}% and best dedicated campaign ~{100*GAL_CAMPAIGN:.1f}%. Only z~3 is even marginally")
print(f"#    reachable, and only under the razor; the honest CPL band keeps the {100*GAL_CAMPAIGN:.1f}% campaign at ~{sep3_dr5_camp:.1f}s (DR5).")
print("#  HONEST VERDICT:")
for i in range(0, len(ONE_LINE), 90):
    print("#    " + ONE_LINE[i:i+90])
CAVEATS = [
 "BAO does NOT measure a0. r_drag is set pre-recombination at g>>a0 (standard ruler), so BAO carries "
 "no clean independent a0 signal. Its role is a KILL SWITCH on the PREDICTION via rho_DE(z) -> the "
 "predicted a0(z)=a0(0)sqrt(rho_DE(z)/rho_DE0). Do not overclaim 'BAO measures a0 to 1%'.",
 "The razor (~0.5-0.9%) is the INTRINSIC sharpness of the prediction (parameter-free map + sqrt-halved "
 "Lambda anchor), FLAT in z. It is a theory CEILING. The OPERATIONAL band, marginalized over CURRENT "
 "(w0,wa), balloons to ~8-13% at z=2-3 -- comparable to the galaxy floor. Do NOT conflate the two.",
 "DR3/DR5 (w0,wa) tightening is MODEST: ~1.2x (DR3) / ~1.4x (DR5) / <=1.8x (+CMB-S4/Euclid), from "
 "1/sqrt(volume) with DR2 already 3yr of the 5yr survey. NOT order-of-magnitude. a0(z=3) band ~12.6% "
 "-> ~9% only by DR5.",
 "'DE evolves' significance rises only ~1.2-1.8x: DR2 2.8-4.2s -> DR5 ~3.9-5.9s, crossing a clean 5s "
 "by DR5 for DESY5/Union3 IF the DR2 central holds. That TRIGGERS branch-LIVE -- it does NOT settle the "
 "a0(z) OUTCOME, which still needs the independent galaxy measurement.",
 "Where the test is reachable it is GALAXY-limited. Required a0(z) precision for a 3s kill: ~2% at the "
 "z~0.5 bump, UNTESTABLE at the z~1 crossover, ~4.5% at z~2, ~8-9% at z=3 -- vs an ~11% SPARC-alone "
 "floor / ~7.7% best campaign. Only z~3 is even marginally reachable, and z=3 kinematics are data-starved.",
 "Two ceilings kept SEPARATE (rule 1): at z<~2.3 BAO measures rho_DE directly so the ~0.9% razor is "
 "valid and negligible vs the galaxy floor; at z=3 (beyond direct-BAO reach) ONLY the CPL-EXTRAPOLATED "
 "band applies, and it keeps the 7.7% campaign below a clean 3s (~2.2s at DR5). No razor-win at z=3.",
 "BRANCH-DISSOLVE is a REAL unfalsifiability weakness: if BAO relaxes to w=-1 the predicted a0(z) is "
 "EXACTLY flat and indistinguishable from constant-a0 MOND. The z=3 decline already dies (<1s from flat) "
 "once |1+w0|<~0.08; the current 0.162 gives only ~2s. The channel's power is INHERITED, not proven.",
 "The a0(z)/a0(0) RATIO is FOOTING-INDEPENDENT (parent sympy proof: Z, a0(0), c, H all cancel). Only the "
 "ABSOLUTE a0(z)=ratio*a0(0) carries the footing (canonical 9.36e-11 vs alt 1.13e-10), and the anchor "
 "razor differs (canonical sqrt-halved 0.90%, alt H0-linear 0.80%). No 'theory closed'.",
]
print("#  FROZEN HONESTY CAVEATS (each load-bearing, none overrideable):")
for i, c in enumerate(CAVEATS, 1):
    print(f"#   {i}. " + c)
print("#"*96)

# ---------- results JSON (build artifact; self-verification, NOT committed) ----------
out = dict(
    law="a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE0)=(1+z)^{1.5(1+w0+wa)}exp(-1.5 wa z/(1+z))",
    razor=dict(canonical_pct=100*razor_canon, alt_pct=100*razor_alt, future_pct=100*razor_future,
               sigLambda_frac_pct=100*sigLambda_frac, flat_in_z=True),
    operational_band_pct={f"z{z}": 100*operband_by_z[z] for z in ZRAZOR},
    effect_pct={f"z{z}": 100*eff_by_z[z] for z in ZRAZOR},
    a0z3_band_forecast_pct={n: 100*band3_forecast[n] for n, _ in FORECAST},
    forecast_factors={n: f for n, f in FORECAST},
    de_evolves_significance={lab: sig_release[lab] for lab in [d[0] for d in DR2]},
    kill_switch_thresholds=dict(DISSOLVE="S<1", AMBIGUOUS="1<=S<3", LIVE="S>=3"),
    kill_switch_map={lab: {k: dict(S=v[0], branch=v[1]) for k, v in kill_map[lab].items()}
                     for lab in [d[0] for d in DR2]},
    req_gal_precision_pct={f"z{z}": dict(
        razor=(None if req_tab[z]["req_razor"]=="null" else
               (100*req_tab[z]["req_razor"] if np.isfinite(req_tab[z]["req_razor"]) else "cosmo-ceiling")),
        dr5band=(None if req_tab[z]["req_dr5"]=="null" else
                 (100*req_tab[z]["req_dr5"] if np.isfinite(req_tab[z]["req_dr5"]) else "cosmo-ceiling")))
        for z in ZRAZOR},
    galaxy_benchmarks_pct=dict(box_now=100*GAL_BOX_NOW, sparc_floor=100*GAL_FLOOR,
                               best_campaign=100*GAL_CAMPAIGN, anchor_target=100*GAL_TARGET,
                               aspirational=100*GAL_ASPIRE),
    z3_sep_bestcampaign=dict(razor=A4[3.0][3], operational_DR2=sep3_dr2_camp, operational_DR5=sep3_dr5_camp),
    dissolve_threshold_1plusw0=eps_c,
    one_line_verdict=ONE_LINE, caveats=CAVEATS, a0_canon=A0C, a0_alt=A0A)
json.dump(out, open(os.path.join(HERE, "bao_killswitch_a0z_2026_results.json"), "w"), indent=1, default=float)
print("\n[bao_killswitch_a0z_2026_results.json written]")

# ================================================================================
# SELF-CHECKS (frozen invariants; task-mandated + honesty rails)
# ================================================================================
print("\n" + bar); print("SELF-CHECK (frozen invariants)"); print(bar)
# 1. (task) razor width < galaxy floor
assert razor_canon < GAL_FLOOR, (razor_canon, GAL_FLOOR)
# 2. (task) DR3/DR5 (w0,wa) errors are >= a realistic floor (NOT absurdly small): shrink <= 1.8x,
#    DR5 <= 1.5x, and sigma(w0) at the most optimistic release stays >= 0.025 (not order-of-magnitude)
maxfac = max(f for _, f in FORECAST); dr5fac = dict(FORECAST)["DR5 (full 5yr)"]
sig_w0_best = 0.055/maxfac
assert maxfac <= 1.8 and dr5fac <= 1.5, (maxfac, dr5fac)
assert sig_w0_best >= 0.025, sig_w0_best
# 3. razor at least 8x tighter than the galaxy floor (the asymmetry is real)
assert razor_canon < GAL_FLOOR/8.0
# 4. operational band grows with z (bump-then-decline), and DR5 tightens the z=3 band
assert operband_by_z[3.0] > operband_by_z[0.5]
assert band3_forecast["DR5 (full 5yr)"] < band3_forecast["DR2 (now, ~3yr)"]
# 5. kill-switch: DR2 LIVE for DESY5 & Union3; LCDM-truth => DISSOLVE at every release
assert kill_map["DESI+CMB+DESY5"]["DR2"][1] == "LIVE" and kill_map["DESI+CMB+Union3"]["DR2"][1] == "LIVE"
assert branch(0.0) == "DISSOLVE"
# 6. asymmetry: DR2band+gal11 caps z=3 below 2.5s; razor+gal5 makes z=3 decisive (>3s)
assert A4[3.0][1] < 2.5 and A4[3.0][4] > 3.0
# 7. honesty: at z=3 the OPERATIONAL band keeps the best 7.7% campaign below a clean 3s (no razor-win)
assert sep3_dr5_camp < 3.0
# 8. 'DE evolves' significance rises with release for every combo, but modestly (<=1.8x)
_DR2KEY, _EXTKEY = FORECAST[0][0], FORECAST[-1][0]
for lab in [d[0] for d in DR2]:
    assert sig_release[lab][_EXTKEY] > sig_release[lab][_DR2KEY]
    assert sig_release[lab][_EXTKEY] <= sig_release[lab][_DR2KEY]*1.8 + 1e-9
print(f"  1. razor {100*razor_canon:.2f}% < galaxy floor {100*GAL_FLOOR:.1f}%                                  OK")
print(f"  2. (w0,wa) shrink <=1.8x (DR5 {dr5fac}x), sig(w0)_best {sig_w0_best:.3f} >= 0.025 (not tiny)   OK")
print(f"  3. razor >= 8x tighter than the galaxy floor ({GAL_FLOOR/razor_canon:.0f}x)                        OK")
print( "  4. operational band grows with z; DR5 tightens the z=3 band                     OK")
print( "  5. DR2 LIVE for DESY5 & Union3; LCDM-truth => DISSOLVE everywhere               OK")
print(f"  6. asymmetry: DR2band+gal11 z=3 = {A4[3.0][1]:.1f}s (<2.5); razor+gal5 = {A4[3.0][4]:.1f}s (>3)      OK")
print(f"  7. honest z=3 best-campaign under CPL band = {sep3_dr5_camp:.1f}s < 3s (no razor-win at z=3)     OK")
print( "  8. 'DE evolves' significance rises with release, but <=1.8x (modest)            OK")
print("  SELF-CHECK PASSED.")
print("\nEXIT 0: BAO kill-switch + razor + galaxy-limited asymmetry computed. Exit code is not a verdict.")
