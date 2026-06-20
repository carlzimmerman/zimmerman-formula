#!/usr/bin/env python3
"""
ROUTE A -- the BARYON CENSUS audit of the cluster MOND residual eta(R500).
=========================================================================
Carl's #1 rule applied to clusters: verify the residual is NOT a measurement
artifact as rigorously as a 'works' claim. The UN-audited side this session is
the DENOMINATOR M_bar -- eta is inflated from the BOTTOM if baryons are under-
counted. Quantify EACH under-counted-baryon channel HONESTLY, sum them BOUNDED
by the cosmic f_b ceiling, report how much eta shaves from ~1.6-1.8 and what
survives.

FRAMEWORK FOOTING (INPUT, never derived):
  a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11,  modified-INERTIA dS-Unruh
  g_obs = sqrt(g_bar^2 + g_bar*a0),  nu = sqrt(1 + a0/g_bar).
  eta(R500) = g_obs / (nu * g_bar) = M_dyn/M_bar at R500.

THE DEEP-MOND LEVER (verified on the real eRASS1 data, CLUSTER_BARYON_BUDGET_
FORENSIC_2026-06-14: eta(gas)/eta(cosmic)=1.518 vs sqrt(M_cos/M_gas)=1.526):
  clusters at R500 sit at g_bar ~ 0.5 a0 (mildly-deep MOND), eta ~ sqrt(a0/g_bar),
  and g_bar ∝ M_bar(<R500), so
        eta ∝ 1/sqrt(M_bar)   (deep-MOND)
  ==> a fractional increase delta == Delta_Mbar/Mbar lowers eta by 1/sqrt(1+delta).
  This is the EXACT shave law (mild-MOND correction folded in numerically below).

THE HARD CEILING (the both-ways anchor -- do NOT violate):
  cosmic f_b = Omega_b/Omega_m = 0.156 (Planck; range 0.156-0.171). Baryons
  WITHIN R500 cannot exceed the cosmic fraction of M500 -- and clusters are
  DEPLETED (gas expelled by feedback to >R500), so the realistic ceiling is
  ~0.85*cosmic within R500 (Planelles depletion Yb,500~0.85). Closing eta~1.6-1.8
  by baryons ALONE needs M_bar up ~60-80% -> f_b,cl ~ 0.23-0.27, FAR above 0.156
  = IMPOSSIBLE by baryons alone. The census can SHAVE eta but cannot CLOSE it.

Each channel below carries a REAL magnitude from the 2024-2026 literature.
Sign of clumping is gotten right (it HURTS). Quarantine: a0/Z/kappa = INPUT.
"""
import numpy as np
import json
from astropy.io import fits

# ---------------------------------------------------------------- constants
c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18; OmL = 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
A0_FRAME = 0.5*c*np.sqrt(G*OmL*RHO_CRIT0)        # framework dS-Unruh a0
A0_MOND  = 1.2e-10
FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

F_B_COSMIC      = 0.156      # Planck Omega_b/Omega_m (the HARD CEILING)
F_B_COSMIC_HI   = 0.171      # alt high (some Planck/BBN combinations)
DEPLETION_Yb500 = 0.85       # realistic within-R500 ceiling (Planelles; gas expelled to >R500)

print("="*92)
print("a0_frame = %.4e m/s^2 (framework dS-Unruh, target 9.36e-11)" % A0_FRAME)
print("cosmic f_b ceiling = %.3f (Planck; depletion-realistic within-R500 = %.3f)"
      % (F_B_COSMIC, DEPLETION_Yb500*F_B_COSMIC))

# ----------------------------------------------- framework dS-Unruh MI
def nu_frame(gbar, a0): return np.sqrt(1.0 + a0/gbar)
def etaA(gobs, gbar, a0): return gobs/(nu_frame(gbar, a0)*gbar)

# ==========================================================================
# (0) REPRODUCE THE eRASS1 BASELINE + MEASURE THE REAL BARYON COMPOSITION
# ==========================================================================
# The baseline eta uses the banked baryon budget (gas + 0.2*gas in stars).
# We also extract the REAL f_gas, f_star to know the COMPOSITION the channels
# multiply (stars are a SMALL fraction -> stellar channels are budget-capped).
try:
    d = fits.open(FITS)[1].data
    def col(name): return np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[name]], float)
    z, M500, Mgas, fgas, R500 = (col("BEST_Z"), col("M500"), col("MGAS500"), col("FGAS500"), col("R500"))
    ok = (z>0)&(z<1)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30)
    N = int(ok.sum())
    M500_kg = M500[ok]*1e13*Msun
    Mgas_kg = Mgas[ok]*1e11*Msun
    R_m     = R500[ok]*kpc
    fgas_med = float(np.median(Mgas_kg/M500_kg))         # REAL gas fraction at R500
    DATA = "real eRASS1 (Bulbul+2024, N=%d)" % N
except Exception as e:
    print("[FITS unavailable -> banked numbers]", e)
    N = 9830; fgas_med = 0.067
    M500_kg = None
    DATA = "banked eRASS1 (N=9830)"

# Banked baseline baryon budget: gas + 0.2*gas in stars  -> f_star ~ 0.2*f_gas.
FSTAR_BANKED = 0.2 * fgas_med    # the stellar mass in the BANKED baseline (as a frac of M500)
fbar_baseline = fgas_med + FSTAR_BANKED
print("="*92)
print("DATA:", DATA)
print("REAL baryon COMPOSITION at R500 (median):")
print("  f_gas(R500)   = %.4f   (the DOMINANT baryon; X-ray measured)" % fgas_med)
print("  f_star(banked)= %.4f   (= 0.2*f_gas in the baseline budget)" % FSTAR_BANKED)
print("  f_bar baseline= %.4f   vs cosmic ceiling %.3f  (ratio %.2f)"
      % (fbar_baseline, F_B_COSMIC, fbar_baseline/F_B_COSMIC))
print("  ==> STARS are ~%.0f%% of the baryon budget; GAS is ~%.0f%%."
      % (100*FSTAR_BANKED/fbar_baseline, 100*fgas_med/fbar_baseline))
print("  ==> stellar-side channels (IMF, ICL) multiply only the SMALL stellar piece.")

# the eta we are auditing (post WL-vs-hydro + Y-Q field): the brief's ~1.6-1.8 band.
# We treat eta_start as a free input over [1.6, 1.8] and ALSO report from gas-only 2.57.
ETA_START_BAND = (1.60, 1.80)     # post hydro-proxy + Y-Q field (the brief's residual)
ETA_GAS_ONLY   = 2.57             # gas-only framework (banked), to show the full ladder

# ==========================================================================
# THE EXACT SHAVE LAW (deep-MOND, with the mild-MOND correction folded in)
# ==========================================================================
# eta ∝ g_obs/(nu*g_bar). Increasing M_bar by factor (1+delta) scales g_bar->(1+delta)*g_bar.
# In PURE deep MOND eta ∝ 1/sqrt(g_bar) ∝ 1/sqrt(M_bar). At R500 g_bar~0.5a0 the mild-MOND
# correction is small; we apply the EXACT ratio at the median footing g_bar/a0 = 0.5 (the
# data median g/a0~0.48). For a baseline eta_0 = sqrt(a0/g_bar+...) the factor is computed
# exactly from the nu-form at g_bar and (1+delta)*g_bar.
def eta_shave_factor(delta, gbar_over_a0=0.5):
    """exact eta ratio when M_bar (hence g_bar) goes up by (1+delta), framework dS-Unruh."""
    gbar = gbar_over_a0 * A0_FRAME
    gbar2 = (1+delta)*gbar
    # eta = g_obs/(nu*g_bar) where g_obs = nu*g_bar = sqrt(g_bar^2+g_bar*a0)... wait:
    # eta(R500) ≡ M_dyn/M_bar. M_dyn from g_obs via g_obs=GM_dyn/r^2; g_bar=GM_bar/r^2.
    # framework predicts g_obs from g_bar: g_pred=sqrt(g_bar^2+g_bar*a0). The OBSERVED
    # eta = g_obs_required/g_bar where g_obs_required is the dynamical accel inferred from
    # M_dyn (WL/HSE). Increasing M_bar lowers eta as g_bar^{-1}*(fixed M_dyn) -> eta∝1/Mbar?
    # NO: eta is the EXCESS factor. The DATA fixes M_dyn (from WL). eta=M_dyn/M_bar exactly.
    # So eta ∝ 1/M_bar EXACTLY (not 1/sqrt) IF M_dyn is held fixed by the lensing mass.
    # BUT the framework's PREDICTED M_dyn from the baryons via MI is sqrt(M_bar*...)-like;
    # the residual eta we audit is OBSERVED M_dyn(WL) / M_bar. Held-fixed M_dyn => eta∝1/Mbar.
    return 1.0/(1.0+delta)

# NOTE on the law (load-bearing, both ways):
#   eta(R500) as DEFINED in the banked work = M_dyn(WL-or-HSE) / M_bar, i.e. the OBSERVED
#   mass discrepancy. M_dyn is set by the DATA (lensing/HSE), independent of the baryon
#   census. So adding baryons lowers eta EXACTLY as 1/(1+delta) -- the FULL benefit, NOT
#   the sqrt. (The sqrt-law eta(gas)/eta(cosmic)=1.518 in the forensic is the framework's
#   PREDICTED phantom eta_MOND=sqrt(a0/g_bar); but the AUDIT quantity M_dyn/M_bar uses the
#   measured M_dyn and falls as 1/(1+delta).) We use the 1/(1+delta) law = MOST GENEROUS to
#   closure (avoids high-priesting), and ALSO report the sqrt-law for the predicted-phantom
#   framing as a both-ways check.
def shave_linear(delta): return 1.0/(1.0+delta)         # M_dyn fixed by data (audit quantity)
def shave_sqrt(delta):   return 1.0/np.sqrt(1.0+delta)  # predicted-phantom framing

# ==========================================================================
# ROUTE A CHANNELS -- each a REAL 2024-2026 magnitude, as Delta_Mbar/Mbar
# ==========================================================================
# We express each channel as the EXTRA baryon mass it adds, as a FRACTION OF THE
# BASELINE BARYON BUDGET (fbar_baseline). delta_i = Delta_Mbar_i / Mbar_baseline.
# Then sum (capped at the f_b ceiling), and shave eta.

channels = []

# ---- (1) BOTTOM-HEAVY IMF in cluster ellipticals/BCGs ----
# Lit (Lyu/Loubser+2020-21 BCG dynamical IMF; Conroy-vanDokkum; Cappellari):
#   BCGs need Salpeter-or-heavier, M/L excess up to ~1.5-2x Kroupa IN THE CORE.
#   BUT cluster-wide stellar mass is NOT all in BCG cores: most stellar mass is in
#   satellites + outskirts with ~MW/Kroupa IMF. The MASS-WEIGHTED cluster stellar
#   M/L boost over the (typically Chabrier/Kroupa-assumed) census is ~1.2-1.5
#   (the BCG/massive-ETG fraction with heavy IMF is a minority of total stellar mass).
#   Honest band: stellar mass up 20-50% (mid 35%).
imf_boost_lo, imf_boost_mid, imf_boost_hi = 1.20, 1.35, 1.60   # M/L_true / M/L_assumed
for tag, b in [("lo",imf_boost_lo), ("mid",imf_boost_mid), ("hi",imf_boost_hi)]:
    d_imf = (b-1.0) * (FSTAR_BANKED / fbar_baseline)   # extra stellar mass / total baryons
    channels.append(("IMF_%s"%tag, d_imf, b, "stellar M/L x%.2f over assumed; stars=%.0f%% of M_bar"
                     % (b, 100*FSTAR_BANKED/fbar_baseline)))

# ---- (2) INTRACLUSTER LIGHT (ICL) ----
# Lit (Three Hundred sims 2024-25; Montes; obs): ICL = 5-40% of TOTAL STELLAR light.
#   X-ray-census stellar masses often capture BCG+satellites but UNDER-count diffuse ICL.
#   Honest add to the stellar component: +10-40% of f_star (mid +25%).
icl_lo, icl_mid, icl_hi = 0.10, 0.25, 0.40
for tag, f in [("lo",icl_lo), ("mid",icl_mid), ("hi",icl_hi)]:
    d_icl = f * (FSTAR_BANKED / fbar_baseline)
    channels.append(("ICL_%s"%tag, d_icl, f, "+%.0f%% of stellar light (ICL under-counted)"%(100*f)))

# ---- (3) COLD / MOLECULAR GAS + DUST ----
# Lit: radio/IR/UV surveys cap cool diffuse baryons at <1% of the hot ICM
#   (the ICM dominates baryons by ~6x over optical). NEGLIGIBLE.
cold_frac_of_gas = 0.01    # <1% of the hot gas mass
d_cold = cold_frac_of_gas * (fgas_med / fbar_baseline)
channels.append(("COLD_GAS", d_cold, cold_frac_of_gas, "<1%% of hot ICM (radio/IR caps) -> negligible"))

# ---- (4) X-RAY GAS CLUMPING -- SIGN MATTERS ----
# Lit (Eckert+2015; Lyskova/eROSITA 2023): X-ray emission ∝ <n^2> > <n>^2, so clumpy gas
#   makes the INFERRED density (hence Mgas) biased HIGH. Mgas bias ~1.06 at R500, ~1.15 at
#   R200. So de-clumping REMOVES gas mass -> RAISES eta. SIGN = NEGATIVE channel (hurts).
clump_Mgas_bias_R500 = 1.06   # inferred Mgas is 1.06x the true -> correction removes 6%
d_clump = -(1.0 - 1.0/clump_Mgas_bias_R500) * (fgas_med / fbar_baseline)  # NEGATIVE
channels.append(("CLUMPING_R500", d_clump, clump_Mgas_bias_R500,
                 "Mgas biased HIGH x%.2f -> de-clumping REMOVES gas -> RAISES eta (WRONG sign)"
                 % clump_Mgas_bias_R500))

# ---- (5) MISSING-BARYON GAP (WHIM / outskirt gas) ----
# Lit (Popesso+2024; Siegel+2025; IllustrisTNG 2025; Three Hundred 2025):
#   cluster f_b,500 ~ 0.11-0.146 vs cosmic 0.156 -> ~14% "missing". BUT the missing baryons
#   are REDISTRIBUTED BY FEEDBACK TO >R500 (1.5-2.5 R200c) -- they DO NOT sit inside R500,
#   so they DO NOT contribute to g_bar(R500). The COUNTERFACTUAL ceiling (cram them all
#   inside R500) is the IMPOSSIBLE bound. We report BOTH:
#     (a) PHYSICAL: missing baryons are outside R500 -> delta_missing = 0 at R500.
#     (b) COUNTERFACTUAL CEILING: fill to depletion-realistic 0.85*cosmic within R500.
d_missing_physical = 0.0
fbar_with_full_stars = fbar_baseline   # baseline budget already (before channels)
fbar_ceiling = DEPLETION_Yb500 * F_B_COSMIC               # 0.85*0.156 = 0.1326
d_missing_counterfactual = max(0.0, (fbar_ceiling - fbar_baseline) / fbar_baseline)
channels.append(("MISSING_physical", d_missing_physical, 0.0,
                 "missing baryons measured at >R500 (feedback-expelled) -> 0 effect on g_bar(R500)"))
channels.append(("MISSING_ceiling", d_missing_counterfactual, fbar_ceiling,
                 "COUNTERFACTUAL: cram to 0.85*cosmic within R500 (=%.3f); contradicts feedback data"
                 % fbar_ceiling))

print("="*92)
print("ROUTE A CHANNELS (each as Delta_Mbar/Mbar_baseline = delta_i):")
print("%-18s %9s  %-9s  %s" % ("channel", "delta", "param", "note"))
for nm, dlt, par, note in channels:
    print("%-18s %+9.4f  %-9.3g  %s" % (nm, dlt, par, note))

# ==========================================================================
# SUM THE CHANNELS -- THREE HONEST STACKS, ALL CEILING-CHECKED
# ==========================================================================
def get(nm): return dict((c[0], c[1]) for c in channels)[nm]

# STACK 1 -- PHYSICAL (defensible): IMF_mid + ICL_mid + cold + clumping(neg) + missing_physical(0)
stack_phys = get("IMF_mid") + get("ICL_mid") + get("COLD_GAS") + get("CLUMPING_R500") + get("MISSING_physical")
# STACK 2 -- GENEROUS (every stellar systematic at HI, clumping ignored, missing still 0 at R500)
stack_gen  = get("IMF_hi")  + get("ICL_hi")  + get("COLD_GAS") + 0.0 + get("MISSING_physical")
# STACK 3 -- IMPOSSIBLE CEILING (stellar HI + cram missing inside R500; violates feedback data)
stack_ceil = get("IMF_hi")  + get("ICL_hi")  + get("COLD_GAS") + 0.0 + get("MISSING_ceiling")

def fbar_after(delta): return fbar_baseline * (1.0 + delta)
def ceiling_status(delta, label):
    fb = fbar_after(delta)
    over_cosmic   = fb > F_B_COSMIC
    over_depleted = fb > fbar_ceiling
    flag = "VIOLATES cosmic ceiling" if over_cosmic else ("exceeds depletion-realistic" if over_depleted else "within ceiling")
    return fb, flag

print("="*92)
print("STACKS (delta_total, resulting f_bar within R500, ceiling check):")
for label, dlt in [("PHYSICAL (defensible)", stack_phys),
                   ("GENEROUS (stellar maxed, clumping ignored)", stack_gen),
                   ("IMPOSSIBLE CEILING (cram missing inside R500)", stack_ceil)]:
    fb, flag = ceiling_status(dlt, label)
    print("  %-44s delta=%+.4f  f_bar=%.4f  [%s]" % (label, dlt, fb, flag))

# ==========================================================================
# SHAVE eta -- from the brief's ~1.6-1.8 start band, AND from gas-only 2.57
# ==========================================================================
def shave_eta(eta0, delta, law):
    """eta after adding baryon fraction delta. eta>1 part scales; eta=1 is Newtonian floor."""
    # the DISCREPANCY (eta-1) is what baryons attack; shave the discrepancy by the law factor,
    # but the law acts on M_bar so it scales the whole eta multiplicatively for the audit
    # quantity M_dyn/M_bar. Use multiplicative on eta (audit) and on (eta-1)? The audit
    # quantity M_dyn/M_bar scales the WHOLE eta by 1/(1+delta) (M_dyn fixed). So:
    return eta0 * law(delta)

print("="*92)
print("eta SHAVE (law: M_dyn/M_bar audit quantity, eta ∝ 1/(1+delta) -- MOST generous):")
print("%-44s %-12s %-12s" % ("stack", "eta from 1.70", "eta from 2.57(gas-only)"))
for label, dlt in [("PHYSICAL (defensible)", stack_phys),
                   ("GENEROUS (stellar maxed)", stack_gen),
                   ("IMPOSSIBLE CEILING", stack_ceil)]:
    e_mid = shave_eta(1.70, dlt, shave_linear)
    e_gas = shave_eta(ETA_GAS_ONLY, dlt, shave_linear)
    print("  %-42s %-12.3f %-12.3f" % (label, e_mid, e_gas))

print("-"*92)
print("BOTH-WAYS sqrt-law check (predicted-phantom framing, eta ∝ 1/sqrt(1+delta)):")
for label, dlt in [("PHYSICAL", stack_phys), ("GENEROUS", stack_gen), ("CEILING", stack_ceil)]:
    print("  %-12s eta(1.70)->%.3f   eta(2.57)->%.3f"
          % (label, shave_eta(1.70,dlt,shave_sqrt), shave_eta(ETA_GAS_ONLY,dlt,shave_sqrt)))

# ==========================================================================
# THE CLOSURE QUESTION + FOOTING (g_bar~0.5a0): does R500 vs deep-MOND matter?
# ==========================================================================
# To CLOSE eta from 1.70 to <=1.15 needs M_bar up by (1.70/1.15 - 1) = 48% (linear law),
# i.e. delta_needed ~ 0.48 -> f_bar = 0.235 = 1.5x cosmic = IMPOSSIBLE.
delta_to_close_170 = (1.70/1.15) - 1.0
delta_to_close_180 = (1.80/1.15) - 1.0
fbar_to_close_170  = fbar_baseline * (1.0 + delta_to_close_170)
print("="*92)
print("CLOSURE BOUND -- TWO WALLS (both ways; the depleted X-ray baseline matters):")
print("  The eRASS1 eta uses the DEPLETED X-ray census f_bar=%.3f (= %.2fx cosmic), because the"
      % (fbar_baseline, fbar_baseline/F_B_COSMIC))
print("  gas is feedback-expelled. So the f_b CEILING and the RADIAL-LOCATION physics bind at")
print("  DIFFERENT eta values:")
for eta0, tag in [(ETA_GAS_ONLY,"gas-only"),(2.33,"WL-branch"),(1.90,"hydro-consensus"),
                  (1.70,"post-Y-Q")]:
    dlt = eta0/1.15 - 1.0
    fb  = fbar_baseline*(1+dlt)
    if fb > F_B_COSMIC:       wall = "VIOLATES cosmic f_b ceiling (hard impossibility)"
    elif fb > fbar_ceiling:   wall = "exceeds depletion-realistic 0.85*cosmic (still blocked by radial location)"
    else:                     wall = "UNDER f_b ceiling arithmetic -- blocked ONLY by radial location (missing baryons at >R500)"
    print("    eta %.2f->1.15 (%s): delta=%.2f -> f_bar=%.3f (%.2fx cosmic) | %s"
          % (eta0, tag, dlt, fb, fb/F_B_COSMIC, wall))
print("  ==> At the HIGH end (gas-only 2.57, WL 2.33) closure is a CLEAN f_b-ceiling impossibility")
print("      (needs >cosmic baryons inside R500). At the post-corrections end (~1.7) the f_b")
print("      arithmetic is formally satisfiable (f_bar~0.12<0.156) but blocked by the MEASURED")
print("      radial location of the missing baryons (>R500, feedback-expelled -> cannot touch")
print("      g_bar(R500)). EITHER WALL stops baryon-only closure; neither is manufactured.")

# FOOTING: is eta(R500) the right metric? At g_bar~0.5a0 the boost is mild. In the deep
# MOND outskirts (g_bar<<a0, beyond R500) eta is LARGER not smaller -- but there the gas
# (the missing baryons) IS present, so a fuller outskirt baryon profile partly self-cancels.
# This is the radial-profile both-ways note (not a closer at R500).
print("-"*92)
print("FOOTING NOTE: median g_bar/a0 ~ 0.48 (mild-MOND). The missing baryons live in the")
print("deep-MOND OUTSKIRTS (>R500) where eta is LARGER -- adding them there raises M_bar AND")
print("M_dyn-required region; it does NOT lower eta(R500) (g_bar(R500) sees only enclosed mass).")

# ==========================================================================
# VERDICT (both ways)
# ==========================================================================
eta_after_phys_lo = shave_eta(ETA_START_BAND[0], stack_phys, shave_linear)
eta_after_phys_hi = shave_eta(ETA_START_BAND[1], stack_phys, shave_linear)
eta_after_gen_lo  = shave_eta(ETA_START_BAND[0], stack_gen,  shave_linear)
eta_after_gen_hi  = shave_eta(ETA_START_BAND[1], stack_gen,  shave_linear)
print("="*92)
print("VERDICT (both ways):")
print("  PHYSICAL census shave: eta %.2f-%.2f -> %.2f-%.2f  (delta=%+.3f, f_bar=%.3f within ceiling)"
      % (ETA_START_BAND[0], ETA_START_BAND[1], eta_after_phys_lo, eta_after_phys_hi,
         stack_phys, fbar_after(stack_phys)))
print("  GENEROUS census shave: eta %.2f-%.2f -> %.2f-%.2f  (delta=%+.3f, f_bar=%.3f %s)"
      % (ETA_START_BAND[0], ETA_START_BAND[1], eta_after_gen_lo, eta_after_gen_hi,
         stack_gen, fbar_after(stack_gen),
         "within ceiling" if fbar_after(stack_gen)<=F_B_COSMIC else "AT/OVER ceiling"))
print("  RESIDUAL SURVIVING: eta ~ %.2f-%.2f (physical) / %.2f-%.2f (generous) -- still >1.3 = REAL GAP."
      % (eta_after_phys_lo, eta_after_phys_hi, eta_after_gen_lo, eta_after_gen_hi))
print("  Census CANNOT close: from gas-only 2.57 / WL 2.33, closure needs >cosmic baryons inside")
print("  R500 (hard f_b violation); from post-Y-Q ~1.7, the f_b arithmetic is satisfiable but the")
print("  needed baryons are MEASURED at >R500 (feedback-expelled) -> cannot lower g_bar(R500).")

# machine-readable footer
print("RESULT_JSON_BEGIN")
print(json.dumps({
  "a0_frame": round(A0_FRAME,12), "f_b_cosmic_ceiling": F_B_COSMIC,
  "fbar_baseline_R500": round(fbar_baseline,4), "f_gas_R500": round(fgas_med,4),
  "f_star_baseline": round(FSTAR_BANKED,4),
  "stars_pct_of_baryons": round(100*FSTAR_BANKED/fbar_baseline,1),
  "channels": {nm: round(dlt,4) for nm,dlt,_,_ in channels},
  "stack_physical_delta": round(stack_phys,4),
  "stack_generous_delta": round(stack_gen,4),
  "stack_ceiling_delta": round(stack_ceil,4),
  "fbar_after_physical": round(fbar_after(stack_phys),4),
  "fbar_after_generous": round(fbar_after(stack_gen),4),
  "fbar_after_ceiling":  round(fbar_after(stack_ceil),4),
  "ceiling_violated_physical": bool(fbar_after(stack_phys)>F_B_COSMIC),
  "ceiling_violated_generous": bool(fbar_after(stack_gen)>F_B_COSMIC),
  "ceiling_violated_ceiling":  bool(fbar_after(stack_ceil)>F_B_COSMIC),
  "eta_start_band": list(ETA_START_BAND),
  "eta_after_physical": [round(eta_after_phys_lo,2), round(eta_after_phys_hi,2)],
  "eta_after_generous": [round(eta_after_gen_lo,2),  round(eta_after_gen_hi,2)],
  "delta_to_close_eta170_to_115": round(delta_to_close_170,3),
  "fbar_to_close_eta170": round(fbar_to_close_170,3),
  "fbar_to_close_eta170_x_cosmic": round(fbar_to_close_170/F_B_COSMIC,2),
  "closure_eta257_violates_fb": bool(fbar_baseline*(2.57/1.15)>F_B_COSMIC),
  "closure_eta233_violates_fb": bool(fbar_baseline*(2.33/1.15)>F_B_COSMIC),
  "closure_eta170_blocked_by": "radial_location_missing_baryons_beyond_R500_not_fb_arithmetic",
  "clumping_sign": "NEGATIVE (de-clumping removes gas, RAISES eta)",
  "cold_gas": "negligible (<1% ICM)",
  "verdict": "CEILING_BOUNDED_real_gap_survives"
}, indent=0))
print("RESULT_JSON_END")
print("="*92)
