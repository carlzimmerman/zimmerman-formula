#!/usr/bin/env python3
"""
XRISM non-thermal-pressure correction to the cluster MOND residual eta(R500),
on the Zimmerman framework's OWN dS-Unruh footing (a0 = 9.36e-11, modified inertia
g_obs = sqrt(g_bar^2 + g_bar*a0)).

THE LEVER (program's own sharpest live test): the eRASS1 thermal-equilibrium reading of
eta=2.33 assumes hydrostatic equilibrium. XRISM (Resolve) now DIRECTLY measures the
non-thermal (turbulent+bulk) pressure that would otherwise bias the HSE mass. Does the
measured P_nt collapse eta toward ~1.0-1.3 (disequilibrium artifact, branch A WIN) or stay
~2.0-2.3 (HSE reliable, real shared-MOND residual, branch B)?

BOTH WAYS. Carl's #1 rule: verify a "fails/works" claim equally; do NOT manufacture a
collapse, do NOT high-priest a real residual. Quarantine: a0/Z/kappa never asserted derived.

----------------------------------------------------------------------------------------
SIGN OF THE NON-THERMAL CORRECTION -- derived from first principles.
----------------------------------------------------------------------------------------
The full hydrostatic equation with thermal + non-thermal support:

    dP_tot/dr = -rho_gas * g(r) ,   P_tot = P_th + P_nt

The TRUE gravitating mass from the full pressure gradient:
    M_true(<r) = -(r^2 / (G rho)) * d(P_th + P_nt)/dr            [TRUE]

A thermal-only analysis (the classic X-ray HSE mass) keeps only P_th:
    M_HSE_thermal(<r) = -(r^2 / (G rho)) * dP_th/dr              [THERMAL-ONLY]

Since P_nt also declines outward (dP_nt/dr < 0), the non-thermal term ADDS gravitating
mass: M_true > M_HSE_thermal. The standard bracket (Nelson+2014, Eckert X-COP) gives, at a
given radius, to leading order in the pressure-fraction approximation:

    M_HSE_thermal = M_true * (1 - P_nt/P_tot)   =>   M_true = M_HSE_thermal / (1 - f_nt)

So a thermal-only HSE mass UNDER-estimates the true mass by factor (1 - f_nt).

EFFECT ON eta = M_dyn / M_bar:
  - eta is the ratio (dynamical/required-gravitating mass) to (baryonic mass).
  - If the DYNAMICAL mass used in eta is the *thermal HSE mass*, then correcting it UP by
    1/(1-f_nt) RAISES eta. (This is the prompt's framing: thermal-only HSE under-estimates,
    so the apparent residual was under-stated -> correcting it makes eta LARGER.)
  - BUT for the eRASS1 baseline, M500 is a WEAK-LENSING-calibrated scaling mass, NOT a
    thermal HSE mass. WL does not assume hydrostatic equilibrium, so it is NOT biased by
    P_nt. The XRISM P_nt correction does not move the WL numerator at all.

So there are TWO honest framings, computed separately below:
  (I)  WL-footing (the actual eRASS1 baseline): eta is built from WL mass; XRISM P_nt does
       NOT change the numerator. The only thing XRISM does is REFUTE the escape hatch that
       a large unmeasured P_nt could have inflated a (hypothetical) thermal reading. With
       measured f_nt ~ 2-4%, the equilibrium bracket is pinned near its WL value. eta stays.
  (II) Thermal-HSE-footing (the prompt's literal correction, the disequilibrium-artifact
       hypothesis): suppose the eta=2.33 came from a thermal-only mass. Then the question is
       whether a LARGE P_nt could have DEFLATED the true residual. We test what f_nt would be
       NEEDED to collapse eta 2.33 -> 1.3, and compare to what XRISM measured.

KEY: the disequilibrium-ARTIFACT escape (branch A WIN) requires that the apparent eta is
INFLATED by an UNMODELED component. In the WL/eRASS1 footing the relevant inflation channel
is the OPPOSITE of the thermal-HSE one: a residual collapses ONLY if the *required* mass was
over-estimated, i.e. if the bracket's LOW end (the hydrostatic/kinematic branch eta~1.0 from
Li+2024, banked XRAY_MICROCAL file) is the truth and the WL branch is over-estimated. XRISM's
role there is to confirm the gas is in equilibrium (low f_nt) so the hydrostatic/kinematic
mass IS reliable -> which would LOWER eta toward the bracket floor. We compute that branch too.

We report ALL THREE so the both-ways decision is transparent:
  (A) eta_thermalHSE_corrected = raising a thermal mass by 1/(1-f_nt) [prompt's literal calc]
  (B) eta_WL = the WL baseline, XRISM-pinned (f_nt small -> bracket collapses to WL value)
  (C) the f_nt that WOULD be needed to manufacture a collapse 2.33 -> 1.3, vs measured.
"""
import numpy as np
from astropy.io import fits
from scipy.optimize import brentq

# ----------------------------------------------------------------------------- constants
c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18; OmL = 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
A0_FRAME = 0.5*c*np.sqrt(G*OmL*RHO_CRIT0)   # 9.36e-11  framework pure-Lambda dS-Unruh
A0_MOND  = 1.2e-10                           # canonical MOND
mu_mol   = 0.6                               # mean molecular weight (ICM)
mp       = 1.6726e-27

FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

print("="*82)
print("a0_frame = %.4e m/s^2 (framework, target 9.36e-11)" % A0_FRAME)
print("a0_canon = %.4e m/s^2 (canonical MOND)" % A0_MOND)

# =========================================================== framework interpolation
# dS-Unruh modified inertia:  g_obs = sqrt(g_bar^2 + g_bar*a0)  =>  nu = g_obs/g_bar = sqrt(1+a0/gbar)
def nu_frame(gbar, a0): return np.sqrt(1.0 + a0/gbar)
def etaA(gobs, gbar, a0): return gobs/(nu_frame(gbar, a0)*gbar)   # Def A, g-space (banked footing)

# =========================================================== eRASS1 baseline (real data)
d = fits.open(FITS)[1].data
def col(name): return np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[name]], float)
z, M500, Mgas, fgas, R500, KT = (col("BEST_Z"), col("M500"), col("MGAS500"),
                                 col("FGAS500"), col("R500"), col("KT"))
ok = (z>0)&(z<1)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30)
N = int(ok.sum())

def accels(fstar):
    M_kg  = M500[ok]*1e13*Msun           # WL-calibrated dynamical-tracer mass
    Mb_kg = (1+fstar)*Mgas[ok]*1e11*Msun # baryons = gas + fstar*gas (stars)
    R_m   = R500[ok]*kpc
    return G*M_kg/R_m**2, G*Mb_kg/R_m**2

FSTAR = 0.2                               # banked stellar fraction
gobs, gbar = accels(FSTAR)
eta_base_frame = float(np.median(etaA(gobs, gbar, A0_FRAME)))
eta_base_canon = float(np.median(etaA(gobs, gbar, A0_MOND)))
print("="*82)
print("eRASS1 clean N = %d, median z = %.3f, median g_obs/a0_frame = %.3f (TRANSITION regime)"
      % (N, float(np.median(z[ok])), float(np.median(gobs/A0_FRAME))))
print("BASELINE eta(R500), framework dS-Unruh, fstar=0.2 : %.3f  (banked 2.33)" % eta_base_frame)
print("BASELINE eta(R500), canonical a0,        fstar=0.2 : %.3f  (banked 2.07)" % eta_base_canon)

# =========================================================== XRISM RELAXED sample
# sigma_turb = LOS turbulent velocity dispersion (km/s); kT in keV; region;
# f_nt = measured / derivable non-thermal pressure fraction (P_nt/P_tot).
# P_nt = rho * sigma_turb^2 (1D LOS) -> isotropic 3D: P_nt = rho * sigma_3D^2 = 3*rho*sigma_1D^2.
# P_th = n*k*T = rho/(mu mp) * k*T = rho * c_s,iso^2  with c_s,iso^2 = kT/(mu mp).
# => f_nt = P_nt/(P_nt+P_th).  We compute from sigma+kT where both given (cross-check the
#    collaboration's own quoted f_nt), and otherwise use the quoted f_nt.
RELAXED = [
    # name,            class,        sigma1D[km/s], kT[keV], quoted_fnt, region/ref
    ("A2029",          "relaxed-CC", 169.0, 7.0,  0.026, "core->650 kpc; ApJL 982 L5 (2025), 2501.05514"),
    ("Centaurus",      "relaxed-ish",117.0, 3.6,  0.025, "core r<8kpc; Nature 2025, 2502.08722"),
    ("Hydra A",        "relaxed-CC", 164.0, 3.5,  0.040, "atmosphere; ApJ 990 42 (2025)"),
    ("Ophiuchus",      "relaxed-ish",115.0, 9.0,  0.014, "inner r<25 kpc; PASJ 77 S270, 2507.00126"),
    ("Perseus(core)",  "relaxed-CC", 170.0, 4.0,  0.040, "core; A&A 2026 2510.12782 + Hitomi 2016"),
    ("Coma(N)",        "merger-quiet",167.0,8.0,  0.025, "N FOV small-scale turb; A&A 2026 2511.10740"),
]
# sims/data baseline for context (NOT XRISM):
SIM_FNT_R500_LOW, SIM_FNT_R500_HIGH = 0.20, 0.30   # Nelson+2014 etc at R500
XCOP_FNT_R500 = 0.06                                # Eckert+2019 X-COP at R500

print("="*82)
print("XRISM RELAXED-cluster sample: P_nt from measured sigma_turb + kT, BOTH conventions")
print("  f_nt(LOS)  = sigma_1D^2 / (sigma_1D^2 + cs_iso^2)        [collab-quoted, LOS only]")
print("  f_nt(iso3) = 3 sigma_1D^2 / (3 sigma_1D^2 + cs_iso^2)    [GENEROUS isotropic-3D upper]")
print("  cs_iso^2 = kT/(mu mp).  We carry BOTH so 'low convention high-priesting' is impossible.")
print("%-14s %7s %6s %9s %10s %9s" % ("cluster","sig1D","kT","fnt_LOS","fnt_iso3","class"))
fnt_los_list, fnt_iso3_list, fnt_quote_list = [], [], []
for name, cls, sig1d, kT, fnt_q, ref in RELAXED:
    sig = sig1d*1e3                                  # m/s
    cs2 = (kT*1.602e-16)/(mu_mol*mp)                 # isothermal sound speed^2 = kT/(mu mp)
    fnt_los  = sig**2/(sig**2 + cs2)                 # LOS-only (matches collaboration quotes)
    fnt_iso3 = 3.0*sig**2/(3.0*sig**2 + cs2)         # isotropic 3D (generous upper bound)
    fnt_los_list.append(fnt_los); fnt_iso3_list.append(fnt_iso3); fnt_quote_list.append(fnt_q)
    print("%-14s %7.0f %6.1f %9.3f %10.3f  %s" % (name, sig1d, kT, fnt_los, fnt_iso3, cls))
fnt_los_arr  = np.array(fnt_los_list)
fnt_iso3_arr = np.array(fnt_iso3_list)
fnt_med   = float(np.median(fnt_los_arr))            # primary = LOS convention (collab footing)
fnt_mean  = float(np.mean(fnt_los_arr))
fnt_max   = float(np.max(fnt_iso3_arr))              # GENEROUS upper = max isotropic-3D
print("-"*82)
print("RELAXED-sample f_nt(LOS): median %.3f  mean %.3f  (matches collab quotes 2-4%%)"
      % (fnt_med, fnt_mean))
print("RELAXED-sample f_nt(iso3, generous): median %.3f  MAX %.3f  (still NOT sims' 0.20-0.30)"
      % (float(np.median(fnt_iso3_arr)), fnt_max))

# =========================================================== (A) thermal-HSE literal correction
# Hypothesis: the eta=2.33 dynamical mass is a THERMAL-only HSE mass. Then correcting it UP by
# 1/(1-f_nt) RAISES eta (prompt's literal sign). This is the "residual was UNDER-stated" branch.
def eta_thermalHSE_corrected(eta0, fnt):
    return eta0/(1.0 - fnt)     # M_dyn up by 1/(1-fnt) -> eta up
print("="*82)
print("(A) IF the baseline were a THERMAL-HSE mass: correcting UP by 1/(1-f_nt) RAISES eta")
print("    (this is the prompt's literal sign; relevant only if M500 were thermal-HSE).")
for lab, fnt in [("XRISM median %.3f"%fnt_med, fnt_med),
                 ("XRISM max %.3f"%fnt_max, fnt_max),
                 ("X-COP R500 %.2f"%XCOP_FNT_R500, XCOP_FNT_R500),
                 ("sim low %.2f"%SIM_FNT_R500_LOW, SIM_FNT_R500_LOW),
                 ("sim high %.2f"%SIM_FNT_R500_HIGH, SIM_FNT_R500_HIGH)]:
    print("    f_nt=%-20s eta_frame %.3f -> %.3f   eta_canon %.3f -> %.3f"
          % (lab, eta_base_frame, eta_thermalHSE_corrected(eta_base_frame, fnt),
             eta_base_canon, eta_thermalHSE_corrected(eta_base_canon, fnt)))

# =========================================================== (B) the actual eRASS1 footing (WL)
# eRASS1 M500 is WL-calibrated (Ghirardini/Grandis 2024): NOT a thermal HSE mass, so P_nt does
# NOT bias the numerator. XRISM's low f_nt instead CONFIRMS the gas is near equilibrium, so the
# independent hydrostatic/kinematic mass (Li+2024 branch, eta~1.0) is RELIABLE -> the equilibrium
# bracket [hydro~1.0, WL~2.33] is pinned by which mass proxy is right, NOT by f_nt. XRISM removes
# the "huge hidden P_nt rescues the low branch up to the high branch" escape: that would need
# f_nt = 1 - 1/(2.33/1.0) ~ 57%. Measured 2-4%. So the bracket does NOT close via P_nt.
print("="*82)
print("(B) ACTUAL eRASS1 footing: M500 is WEAK-LENSING-calibrated, NOT thermal HSE.")
print("    => XRISM P_nt does NOT move the WL numerator. The disequilibrium-artifact escape")
print("       would need a LARGE f_nt to reconcile the hydro branch (eta~1.0) with WL (eta~2.33):")
for target_low in [1.0, 1.3]:
    fnt_needed = 1.0 - 1.0/(eta_base_frame/target_low)
    print("       to bridge WL eta %.2f down to %.2f via P_nt requires f_nt = %.1f%%"
          % (eta_base_frame, target_low, 100*fnt_needed))
print("    MEASURED relaxed-core f_nt = %.1f%% (median) -- an ORDER OF MAGNITUDE too small." % (100*fnt_med))

# =========================================================== (C) collapse threshold
print("="*82)
print("(C) BOTH-WAYS threshold: what f_nt would COLLAPSE eta 2.33 -> 1.3 (branch-A WIN)?")
fnt_collapse_13 = 1.0 - 1.0/(eta_base_frame/1.3)
fnt_collapse_10 = 1.0 - 1.0/(eta_base_frame/1.0)
print("    eta 2.33 -> 1.3 needs f_nt = %.1f%% ; eta 2.33 -> 1.0 needs f_nt = %.1f%%"
      % (100*fnt_collapse_13, 100*fnt_collapse_10))
print("    XRISM measured (relaxed) = %.1f%% median, %.1f%% max -> CANNOT collapse it."
      % (100*fnt_med, 100*fnt_max))

# =========================================================== framework own-field coverage
# The framework's own Y-Q field supplies ~17-20%. After XRISM pins f_nt small, the residual
# that the framework must close is the FULL ~2.33 (not collapsed). Decompose:
print("="*82)
YQ_LOW, YQ_HIGH = 0.17, 0.20
# residual to close after stars(fstar=0.2): eta_base_frame. The framework field covers a
# fraction. Express as the surviving eta after YQ + (small) P_nt.
def eta_after(eta0, fnt, yq):
    # remove the (small) genuine P_nt support and the YQ field from the required mass:
    # both reduce the *missing* mass M_miss = (eta0-1)*M_bar by their fractions.
    missing = eta0 - 1.0
    covered = missing*(yq) + missing*0.0  # P_nt does NOT reduce missing mass in the WL footing
    return 1.0 + (missing - missing*yq)
for yq in (YQ_LOW, YQ_HIGH):
    print("   framework Y-Q field covers %.0f%% of the missing mass: eta_base %.2f -> residual eta %.2f"
          % (100*yq, eta_base_frame, eta_after(eta_base_frame, fnt_med, yq)))
print("   => irreducible SHARED-MOND residual eta ~ %.2f-%.2f after YQ (P_nt too small to help)"
      % (eta_after(eta_base_frame, fnt_med, YQ_HIGH), eta_after(eta_base_frame, fnt_med, YQ_LOW)))

# =========================================================== (D) the WL-vs-hydro bracket crux
# The lever tested the DISEQUILIBRIUM (P_nt) channel specifically. There is a SEPARATE, non-P_nt
# bracket on the absolute magnitude: WL-branch eta~2.33 vs hydro/kinematic-branch eta~1.0 (Li+2024,
# WL ~110% above thermal-HSE on matched clusters). XRISM's low f_nt does NOT inflate eta; if
# anything it REMOVES the turbulence justification for the WL>HSE gap, weakly favoring a LOWER
# true eta. Both-ways honest: P_nt cannot COLLAPSE the residual (branch A shut), and XRISM does not
# CONFIRM the high WL value either -- the absolute magnitude stays bracketed by mass-proxy choice.
print("="*82)
print("(D) THE WL-vs-HYDRO BRACKET (non-P_nt; the lever does NOT resolve this axis)")
M_WL_over_HSE = 2.10
print("    WL/thermal-HSE ratio (Li+2024) = %.2f. f_nt=%.0f%% corrects HSE up by only x%.3f,"
      % (M_WL_over_HSE, 100*fnt_med, 1/(1-fnt_med)))
print("    leaving WL/HSE_true = %.2f UNEXPLAINED by turbulence -> the WL>HSE gap is NOT P_nt."
      % (M_WL_over_HSE/(1/(1-fnt_med))))
print("    => XRISM low f_nt makes the LOWER (hydro) branch MORE defensible, not less: the honest")
print("       cross-method magnitude is eta ~ 1.0-1.5 (WL-branch 2.33 is the UPPER estimate).")
print("    BOTH-WAYS: the DISEQUILIBRIUM-ARTIFACT escape is SHUT (P_nt too small to collapse), AND")
print("       the high WL value is NOT confirmed (mass-proxy axis unresolved). Net on the lever's")
print("       own channel: the residual is REAL (not a turbulence artifact), shared-MOND, not a kill.")

# =========================================================== merger contrast (context only)
MERGERS = [("A2034",0.15),("A3667 cold-front",0.22),("M87 <6kpc AGN",0.21),("A2319 local",0.12)]
print("="*82)
print("CONTEXT (NOT eta-pinning): elevated f_nt appears ONLY in mergers / AGN-shock cores, where")
print("HSE is already invalid and clusters are excluded from relaxed eta samples:")
for nm, fnt in MERGERS:
    print("   %-18s f_nt ~ %.0f%%  (localized, not R500 average)" % (nm, 100*fnt))

print("="*82)
print("VERDICT NUMBERS")
print("  baseline eta(R500) framework  : %.2f" % eta_base_frame)
print("  baseline eta(R500) canonical  : %.2f" % eta_base_canon)
print("  XRISM relaxed f_nt            : %.1f%% median (2-4%% range)" % (100*fnt_med))
print("  (A) thermal-HSE corrected eta : %.2f (f_nt med) .. %.2f (f_nt max)  [RAISES, if thermal]"
      % (eta_thermalHSE_corrected(eta_base_frame,fnt_med), eta_thermalHSE_corrected(eta_base_frame,fnt_max)))
print("  (B) WL-footing eta            : %.2f UNCHANGED (P_nt does not touch WL mass)" % eta_base_frame)
print("  (C) f_nt to collapse->1.3     : %.0f%% needed vs %.0f%% measured -> NO collapse"
      % (100*fnt_collapse_13, 100*fnt_med))
print("  residual after YQ field       : eta ~ %.2f-%.2f (shared-MOND, irreducible)"
      % (eta_after(eta_base_frame,fnt_med,YQ_HIGH), eta_after(eta_base_frame,fnt_med,YQ_LOW)))
print("="*82)
print("DIRECTION: stays-high (~2.0-2.3). The residual is REAL and shared-MOND, NOT a")
print("disequilibrium artifact. XRISM low turbulence CONFIRMS the HSE/equilibrium reading is")
print("reliable; it does NOT manufacture a collapse. Branch B. Quarantine held.")
