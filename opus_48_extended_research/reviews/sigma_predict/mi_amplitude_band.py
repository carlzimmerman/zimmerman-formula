#!/usr/bin/env python3
r"""
MI NON-ADIABATIC RELATIONAL sigma-SPREAD AMPLITUDE -- the pre-registered prediction band
(topic "mi_amplitude", 2026-06-19, sigma_predict/)
====================================================================================================
DELIVERABLE: the framework's distinctive MODIFIED-INERTIA cluster observable -- the percent SPREAD in a
member's internal velocity dispersion sigma across INFALL PHASE at MATCHED momentary cluster-centric
radius (same external field a_ex) -- computed with the BEST-AVAILABLE Milgrom-2022 A(omega) kernel +
the banked dS-Unruh MI kernel constraints, reported as a BAND with the honest kernel uncertainty.

This consolidates + re-runs the banked physics in
  sigma_spread/mi_sigma_spread_amplitude.py    (the R(y) computation, all theta forms)
  mi_kernel/kernel_constraints.py              (the admissible cone -> the band ceiling/floor)
and reports ONE clean answer: the amplitude band, what sets each end, MG=0 verified, CDM scoped.

PHYSICS (Milgrom 2022 arXiv:2208.07073 = PRD 106 064060, "MOND as a manifestation of modified inertia";
equations verified verbatim from the PDF in the prior banked work; the ABSTRACT independently confirms
the load-bearing structure -- theta is an "extra factor that depends on the frequency ratio of the
external- and internal-field variations" that "appreciably enhance[s] the EFE", and MG uses "the
momentary value of the external acceleration a_ex"):

  Eq(34)-class two-frequency EFE: a member's INTERNAL motion (frequency omega_in) in an external field
  oscillating at omega_ex feels a modified inertia argument
        A  =  a_in + a_ex * theta(y),     y := omega_ex / omega_in
  and the internal boost (sigma^2 magnification) is B = 1/mu_fw(A/a0).
  Eq(35): adiabatic limit y->0 => theta->theta(0)=const => A = a_in + theta(0)*a_ex, EXACTLY a
  modified-GRAVITY EFE with a0 -> a0/theta(0). The a0-DEGENERATE TRAP. The QUASI-STATIC ("relaxed/
  circular at this radius") reference IS this y->0 limit.

  theta(y) PROPERTIES (Milgrom, verbatim text + the banked constraint cone): theta(1)=1, theta>0,
  DECREASING, theta(0) finite "a few". Milgrom's OWN example forms:
        theta_rat = 2/(1+y^2)      theta(0)=2
        theta_e1  = e^{1-|y|}      theta(0)=e ~ 2.718
        theta_e2  = e^{(1-|y|)/2}  theta(0)=e^{1/2} ~ 1.649
  "We have no knowledge of the form of theta(y)." => AMPLITUDE is KERNEL-HOSTAGE. We carry all three
  Milgrom forms + the model-INDEPENDENT cone extrema (kernel_constraints.py STEP 5) and report the BAND.

  dS-Unruh MI kernel input (MI_KERNEL_FROM_DSUNRUH_2026-06-19): the dS-Unruh response is a genuine
  time-nonlocal worldline functional (Obadia-Milgrom; Deser-Levin thermal floor T=(1/2pi)sqrt(a^2+
  (cH_L)^2); Z=cH_L/a0=sqrt(32pi/3) machine-exact) but does NOT DERIVE theta(y) (wrong functional class,
  analytic memory, no sqrt). It only CONSTRAINS: theta(0) in [1,~e], theta(1)=1, decreasing,
  theta(1.5) in (0,1). So the amplitude is bounded but not pinned -- a one-sided cone.

  MG (QUMOND/AQUAL/AeST EFE): depends ONLY on the momentary a_ex (Milgrom, verbatim). B_MG =
  1/mu_fw((a_in+a_ex)/a0), INDEPENDENT of y => ZERO spread across infall phase for ANY a0. Theorem.
  CDM: 0 from the inertia channel (no a0, no memory); BUT tidal-shock heating mimics a same-signed
  ~2-8% infall-phase correlation (scoped + shown separable below; full treatment in
  sigma_spread/discriminator_robustness.py).

OBSERVABLE: a survey bins members at MATCHED cluster-centric radius (= matched a_ex) AND by infall
phase y. The signal is the percent spread in internal sigma across the phase window:
        spread = (sigma_max - sigma_min) / sigma_mean       over the observed y-window,
with sigma ~ sqrt(B). At matched a_ex the overall sigma SCALE cancels -- it is a pure RELATIONAL ratio.

BOTH WAYS (#1 rule): we verify the spread is REAL/above-floor as hard as that it washes out. We do NOT
pick the max-signal kernel -- we report the full Milgrom-form band AND the model-independent cone band.
QUARANTINE: a0/Z/kappa NEVER asserted derived. theta NOT derived (kernel-hostage). The REFUTED
"MI-tangential-vs-MG-radial ellipsoid sign" is NOT used.
"""
import numpy as np

# ----------------------------------------------------------------- framework footing (sealed)
a0 = 9.36e-11                                    # = c^2 sqrt(Lambda/32pi); a0/Z/kappa NOT derived
def mu_fw(x):  x = np.asarray(x, float); return (np.sqrt(1.0 + 4.0*x*x) - 1.0) / (2.0*x)   # inverse inertia

# ----------------------------------------------------------------- theta(y) kernels
# Milgrom's three VERBATIM example forms (the headline bracket) -- we never privilege one:
def theta_rat(y): y = np.abs(np.asarray(y, float)); return 2.0/(1.0 + y*y)         # theta(0)=2
def theta_e1(y):  y = np.abs(np.asarray(y, float)); return np.exp(1.0 - y)         # theta(0)=e
def theta_e2(y):  y = np.abs(np.asarray(y, float)); return np.exp((1.0 - y)/2.0)   # theta(0)=e^0.5
MILGROM = [("rational 2/(1+y^2)", theta_rat, 2.0),
           ("exp e^{1-y}",        theta_e1,  np.e),
           ("exp e^{(1-y)/2}",    theta_e2,  np.exp(0.5))]

# ----------------------------------------------------------------- core: R(y)=sigma_MI(y)/sigma_QS
def boost_mi(a_in, a_ex, y, thetaf):
    """B = 1/mu_fw(A/a0), A = a_in + a_ex*theta(y). sigma^2 ~ B."""
    return 1.0/mu_fw((a_in + a_ex*thetaf(y))/a0)

def R_of_y(a_in, a_ex, y, thetaf):
    """sigma_MI(infall phase y) / sigma_QS;  QS = adiabatic y->0 (theta(0)) at the SAME a_ex. R(0)=1."""
    return np.sqrt(boost_mi(a_in, a_ex, y, thetaf) / boost_mi(a_in, a_ex, 0.0, thetaf))

def spread_over_window(a_in, a_ex, thetaf, ywin):
    Rs = np.array([R_of_y(a_in, a_ex, y, thetaf) for y in ywin])
    return (Rs.max() - Rs.min())/Rs.mean()

print("="*100)
print(" MI NON-ADIABATIC RELATIONAL sigma-SPREAD AMPLITUDE  --  the pre-registered band")
print(" Milgrom 2022 arXiv:2208.07073 Eq(34)/(35); framework mu_fw; theta verbatim + cone; a0 sealed.")
print("="*100)
print(f"  a0 = {a0:.3e} m/s^2 (sealed, NOT derived).  y = omega_ex/omega_in (infall-phase non-adiabaticity).")
print(f"  CANONICAL diffuse/UDG member: a_in = 0.3 a0 (deep-MOND interior), a_ex = 2 a0 (cluster-core EFE).")
print(f"  Observed plunge window: y in [0, 1.5]  (pericenter of a deep-radial orbit; Milgrom dwarf estimate).\n")

# ===================================================================================================
# 1) THE CANONICAL AMPLITUDE -- Milgrom's three verbatim kernels (the headline band)
# ===================================================================================================
a_in, a_ex = 0.3*a0, 2.0*a0          # the canonical diffuse member that sets the banked 6-13%
ywin = np.linspace(0.0, 1.5, 200)
print("-"*100)
print(" (1) AMPLITUDE across Milgrom's THREE verbatim theta kernels (canonical member, window y<=1.5):")
print("-"*100)
milg_spreads = {}
for nm, thf, th0 in MILGROM:
    s = spread_over_window(a_in, a_ex, thf, ywin)
    milg_spreads[nm] = s
    print(f"   {nm:22s}  theta(0)={th0:5.3f}  ->  sigma-spread = {s*100:5.2f}%")
mlo, mhi = min(milg_spreads.values())*100, max(milg_spreads.values())*100
print(f"\n   MILGROM-FORM BAND (canonical member): {mlo:.1f}% - {mhi:.1f}%   (the headline kernel-hostage band)")

# R(y) trajectory (fiducial rational kernel) -- the shape of the prediction
print("\n   R(y) = sigma_MI(infall phase)/sigma_QS, rational theta=2/(1+y^2) (fiducial):")
for y in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]:
    R = R_of_y(a_in, a_ex, y, theta_rat)
    print(f"      y={y:4.2f}: R={R:.4f}  (deviation from quasi-static circular member: {(R-1)*100:+5.1f}%)")

# ===================================================================================================
# 2) THE MODEL-INDEPENDENT CONE BAND -- what sets the floor and the ceiling (kernel_constraints STEP5)
# ===================================================================================================
print("\n"+"-"*100)
print(" (2) MODEL-INDEPENDENT CONE: scan ALL admissible theta (decreasing, theta(1)=1, theta(0) in [1,e],")
print("     theta(1.5) in (0,1)). Because R is monotone in theta evaluated at the window ends, the extremal")
print("     spread sits at the corners of the (theta(0), theta(1.5)) box -- this is the honest band.")
print("-"*100)
# a 2-point admissible theta pinned at the window endpoints (y=0.05 ~ adiabatic, y=1.5 ~ deep plunge):
def two_point_spread(a_in, a_ex, th0, th15):
    """Extremal-corner spread: theta(0.05)=th0 (adiabatic loading), theta(1.5)=th15 (plunge), theta(1)=1."""
    y_lo, y_hi = 0.05, 1.5
    # R at the two ends relative to QS (theta(0)=th0): sigma~sqrt(boost), QS uses th0 at both? No:
    # QS reference = adiabatic member (theta(0)); the window members carry theta(y_lo)~th0 .. theta(y_hi)=th15.
    A_qs  = a_in + a_ex*th0
    A_lo  = a_in + a_ex*th0          # near-adiabatic end ~ theta(0)
    A_hi  = a_in + a_ex*th15         # deep-plunge end
    B = lambda A: 1.0/mu_fw(A/a0)
    Rlo, Rhi = np.sqrt(B(A_lo)/B(A_qs)), np.sqrt(B(A_hi)/B(A_qs))
    Rs = np.array([Rlo, Rhi]); return (Rs.max()-Rs.min())/Rs.mean()

corners = {
    "MAX  (theta0=e,   theta1.5=0.40, deepest drop)": two_point_spread(a_in, a_ex, np.e,  0.40),
    "MILGROM-HI (theta0=e,   theta1.5=0.61)        ": two_point_spread(a_in, a_ex, np.e,  0.61),
    "MILGROM-LO (theta0=1.65, theta1.5=0.78)       ": two_point_spread(a_in, a_ex, 1.649, 0.78),
    "FLOOR (theta0->1, no EFE enhance, theta1.5=0.65)": two_point_spread(a_in, a_ex, 1.0,  0.65),
}
for lab, s in corners.items():
    print(f"   {lab}: spread = {s*100:5.2f}%")
cone_lo = corners["FLOOR (theta0->1, no EFE enhance, theta1.5=0.65)"]*100
cone_hi = corners["MAX  (theta0=e,   theta1.5=0.40, deepest drop)"]*100
print(f"\n   MODEL-INDEPENDENT CONE BAND (canonical member): ~{cone_lo:.0f}% - ~{cone_hi:.0f}%")
print(f"   WHAT SETS IT:  CEILING <- theta(0)<=~e (wide-binary + solar-reflex + causality cap on adiabatic")
print(f"                  loading) x the fall-rate (theta(1.5) as low as ~0.4).  FLOOR <- theta(0)->1 (no EFE")
print(f"                  enhancement) but does NOT vanish (window still spans theta(1.5)<1).")
print(f"   The Milgrom-family ceiling (theta(1.5) in [0.6,0.78]) is ~12-13% = the banked 6-13% upper end.")

# ===================================================================================================
# 3) MG = EXACTLY 0  (verify the theorem: momentary a_ex only, for ANY a0)
# ===================================================================================================
print("\n"+"-"*100)
print(" (3) MG THEOREM CHECK: at matched a_ex, MG boost is y-INDEPENDENT for ANY a0 -> spread = 0 exactly.")
print("-"*100)
for a0_mult in [0.5, 1.0, 2.0]:
    Bs = [1.0/mu_fw((a_in + a_ex)/(a0_mult*a0)) for _ in [0.05, 0.5, 1.0, 1.5]]   # same value, all y
    print(f"   MG a0={a0_mult:.1f}x: boost across y=[0.05,0.5,1.0,1.5] = {np.round(Bs,4).tolist()}"
          f"  -> spread = {(max(Bs)-min(Bs))/np.mean(Bs)*100:.2f}%")
print("   => MG reads ONLY the momentary a_ex (Milgrom verbatim); a free a0 rigidly shifts the single")
print("      shared value but creates NO phase dependence. MG spread = 0 for every a0. NON-a0-degenerate,")
print("      MG-IMPOSSIBLE by construction.  (CDM inertia channel: 0 -- no a0, no acceleration memory.)")

# ===================================================================================================
# 4) CDM TIDAL-HEATING CONFOUND -- amplitude + separability (scoped; full in discriminator_robustness.py)
# ===================================================================================================
print("\n"+"-"*100)
print(" (4) CDM TIDAL-HEATING CONFOUND -- the make-or-break (same sign! but SEPARABLE):")
print("-"*100)
# Gnedin-Ostriker adiabatic shielding: <dE>/<dE>_impulse = (1+1/y^2)^(-gamma), gamma~2.5
def tidal_dsigma_frac(y, eps_imp, gamma=2.5):
    """fractional sigma boost from one pericentric tidal shock vs infall-phase y. sigma^2 -> sigma^2(1+eps_imp*chi)."""
    chi = (1.0 + 1.0/np.maximum(y,1e-6)**2)**(-gamma)
    return np.sqrt(1.0 + eps_imp*chi) - 1.0
print("   Tidal-shock heating is ALSO governed by y (the impulse/adiabatic boundary IS y~1, Gnedin-Ostriker)")
print("   and pushes the SAME sign (plungers hotter). Amplitude at deep plunge y=1.5, MI vs tidal:")
print(f"   {'eps_imp':>8} | {'tidal dsigma@y=1.5':>18} | {'MI dsigma@y=1.5 (rat)':>22}")
mi_15 = (R_of_y(a_in, a_ex, 1.5, theta_rat)-1.0)
for eps in [0.10, 0.25, 0.40]:
    print(f"   {eps*100:7.0f}% | {tidal_dsigma_frac(1.5, eps)*100:17.1f}% | {mi_15*100:21.1f}%")
print(f"\n   => CDM tidal heating fakes a same-signed ~2-8% infall-phase correlation -- COMPARABLE to MI at")
print(f"      deep plunge. The mere correlation does NOT discriminate. SEPARATORS (all MI-specific):")
print(f"      [S1] RADIAL TREND (cleanest): MI EFE spread RISES outward within the MOND zone (a_ex falls")
print(f"           toward a0); tidal heating PEAKS in the core (strongest shock) -> radially ANTI-correlated.")
print(f"      [S2] HYSTERESIS: tidal heating is CUMULATIVE (grows with #pericenters / time-since-infall);")
print(f"           MI is INSTANTANEOUS-relational (set by current y) -> no monotone time-since-infall growth.")
print(f"      [S3] NO MASS LOSS: MI does not strip; tidal shocks bring tidal tails/King truncation. Require")
print(f"           UNDISRUPTED members -> kills the tidal channel, leaves MI.")
print(f"      The joint (radial-rising + non-cumulative + undisrupted) signature is MI-specific.")

# ===================================================================================================
# 5) SYNTHESIS -- the pre-registered amplitude band
# ===================================================================================================
print("\n"+"="*100)
print(" SYNTHESIS -- the pre-registered MI sigma-spread AMPLITUDE")
print("="*100)
print(f"""
 CANONICAL diffuse/UDG plunging member (a_in=0.3a0, a_ex=2a0, window y<=1.5), framework mu_fw, a0 sealed:

   AMPLITUDE (percent spread in internal sigma across infall phase at matched cluster-centric radius):
     * Milgrom's THREE verbatim theta kernels:        {mlo:.1f}% - {mhi:.1f}%   <- the headline band
     * model-INDEPENDENT admissible cone:             ~{cone_lo:.0f}% - ~{cone_hi:.0f}%   <- the honest outer band
       (ceiling set by theta(0)<=~e AND fall-rate; floor by theta(0)->1 with window still spanning theta(1.5)<1)
     * MODIFIED GRAVITY (QUMOND/AeST):                EXACTLY 0%  for ANY a0  (momentary a_ex only -- theorem)
     * CDM inertia channel:                           0%   (tidal heating fakes ~2-8% same-sign, SEPARABLE by
                                                            radial trend / hysteresis / mass-loss)

   WHAT SETS THE BAND (kernel-hostage, NOT max'd): the amplitude scales with the ADIABATIC LOADING the
   plunger sheds, ~ [theta(0) - theta(1.5)]. theta(0) is bounded [1,~e] (wide-binary/solar/causality) and
   the fall-rate is bounded but neither is pinned -> a one-sided cone, NOT a sharp number. Both legs of the
   dS-Unruh kernel work (MI_KERNEL_FROM_DSUNRUH) confirm: the EXISTENCE + SIGN are theorems, the AMPLITUDE
   is an AeST-class free-function value inside this cone.

   FIDUCIAL single number to pre-register (rational theta, the most-cited Milgrom form, canonical member):
     ~{milg_spreads['rational 2/(1+y^2)']*100:.0f}% spread, with the honest uncertainty band {mlo:.0f}-{mhi:.0f}% (Milgrom forms) /
     ~5-18% (model-independent cone).

 BOTH WAYS / QUARANTINE:
   - REAL ASSET (full weight): a nonzero, above-the-MUSE/ELT-floor-IN-PRINCIPLE, MG-IMPOSSIBLE (exact 0
     for any a0), CDM-SEPARABLE (radial-trend) distinctive prediction. Existence + sign are theorems.
   - CONCEDED (full weight): the AMPLITUDE is kernel-hostage (factor ~2-4 across admissible theta); it is a
     TEST not a cluster-residual closure (cycle-averaged MEAN mass NOT raised); the carriers are a SMALL
     subset (plunging diffuse/UDG/dSph at pericenter, y~0.5-1.7); feasibility is MARGINAL (ELT-era, infall-
     phase purity dilutes the observed spread to ~0.4x intrinsic -- see feasibility.py / discriminator_robustness.py).
   - a0/Z/kappa NOT asserted derived; theta NOT derived; refuted ellipsoid-sign NOT used.
""")
