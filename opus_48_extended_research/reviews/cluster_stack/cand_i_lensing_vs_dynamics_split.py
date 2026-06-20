"""
FINAL-DOOR candidate (i): the AeST/relativistic-MOND LENSING-vs-DYNAMICS split.

QUESTION (both ways): does AeST's (and the framework's) LENSING mass DIFFER from its
DYNAMICAL mass in the cluster core? If the lensing slip Sigma = (Phi+Psi)/2 carries EXTRA
deflection beyond what the dynamical potential Phi sources, then the DYNAMICAL residual
(the mass a no-DM theory must actually source as phantom) would be SMALLER than the
LENSING residual -- and the core gap a theory must "close" would shrink.

This is the cleanest possible "third ingredient": if true, it would not ADD mass but
SUBTRACT from the target -- shrinking the gap the stack (B+IGIMF+baryons) must fill.

THE PHYSICS (verified against the literature, both ways):
  - In GR + standard matter, lensing potential Phi_lens = (Phi+Psi)/2; light bends on the
    SUM. Dark matter sources Phi=Psi equally, so lensing mass = dynamical mass.
  - A relativistic MOND theory could in principle have a SLIP eta_slip = Psi/Phi != 1, OR
    a disformal/conformal coupling that makes light see a DIFFERENT effective potential
    than non-relativistic matter (this is the "free function" AeST-class lensing the banked
    no-go flagged). If light bent MORE than matter feels, lensing mass > dynamical mass.

  - AeST (Skordis-Zlosnik 2020; Famaey-Pizzuti-Saltas 2410.02612) is BUILT so that
    Psi = -Phi (no slip) and light bends EXACTLY on the same potential matter feels:
    FPS state verbatim "a dynamical mass equivalent to the lensing mass BY CONSTRUCTION,
    in MONDian gravity" (under Psi=-Phi). This is a DESIGN REQUIREMENT: a relativistic
    MOND theory that did NOT have lensing=dynamics would FAIL the Bullet Cluster / solar
    lensing / GW170817 (c_T=c) -- which is exactly why AeST was constructed with no slip.

  - The framework's banked lensing no-go (TOE Step-2 keystone, fc195ebc / 2820dd9d): a
    covariant Cassini-safe MOND lensing with c_T=c + ghost-freedom + diff-invariance is
    FORBIDDEN to differ from the dynamical sector -- the framework's lensing is
    preferred-frame but STILL gamma_PPN-tied so that on a relaxed core it tracks the
    dynamical mass. The framework's predicted slip gamma = 2*sqrt(1+a0/g_N)-1 GROWS in the
    low-acceleration regime -- but that is the SAME enhancement in BOTH lensing and
    dynamics (it multiplies the deflection AND the orbital potential equally). It does NOT
    open a lensing>dynamics gap; it is the phantom itself, counted once.

CONSEQUENCE: there is NO lensing-vs-dynamics split to exploit. The two-probe agreement is
DATA, not theory: CLASH-lensing core 2.37e14 = eRASS1-X-ray core 2.30e14, RATIO 1.03.
Lensing and dynamics SEE THE SAME core residual to 3%. So the dynamical residual a no-DM
theory must source is NOT smaller than the lensing residual -- they are the same object.

BOTH WAYS: we quantify the MAXIMUM gap-shrink a slip could buy, bounded by the OBSERVED
1.03 two-probe ratio (the data caps any theoretical slip in the core at <=3%), and by the
framework's own gamma-slip prediction.
"""
import numpy as np
import sympy as sp

print("="*94)
print(" FINAL-DOOR candidate (i): AeST/framework LENSING-vs-DYNAMICS split in the core")
print("="*94)

# ---- banked core numbers (reproduced in routeA / Route D) ----
M_target_lens = 1.357e14   # Msun, CLASH lensing residual inside 420 kpc (rich M500=1e15)
M_phantom_MI  = 3.508e13   # Msun, framework MI phantom (dynamical) inside 420 kpc
M_xray_core   = 1.357e14*(2.30/2.37)  # eRASS1 X-ray core, two-probe ratio 1.03 -> dynamical-equivalent
core_gap      = M_target_lens - M_phantom_MI

print("\n[banked core, rich M500=1e15, <420 kpc]")
print("  M_res LENSING (CLASH)      = %.3e Msun" % M_target_lens)
print("  M_res X-RAY/dyn (eRASS1)   = %.3e Msun  (two-probe ratio CLASH/eRASS1 = 1.03)" % M_xray_core)
print("  framework MI phantom (dyn) = %.3e Msun" % M_phantom_MI)
print("  bare core gap              = %.3e Msun  (undershoot x%.2f)" % (core_gap, M_target_lens/M_phantom_MI))

# =====================================================================
# 1. THE SLIP a relativistic MOND theory CAN have, and what the data allows
# =====================================================================
print("\n" + "-"*94)
print(" 1. Is there a lensing-vs-dynamics SLIP that shrinks the DYNAMICAL target? (both ways)")
print("-"*94)

# Define slip s = M_lens / M_dyn (the ratio of what light sees to what orbits/HSE feel).
# If s > 1, light over-bends -> the LENSING residual overstates the dynamical residual ->
# a no-DM theory needs to source only M_dyn = M_lens / s.  We bound s three ways.

# (a) DATA bound: the two-probe ratio. CLASH lensing core / eRASS1 X-ray (HSE) core = 1.03.
#     X-ray (HSE) IS the dynamical probe (it measures Phi via the gas). So OBSERVED s <= 1.03.
s_data = 2.37/2.30
print("  (a) DATA: CLASH-lensing / eRASS1-X-ray(HSE) core ratio = %.3f" % s_data)
print("      -> the OBSERVED slip in the core is at most ~3%%; X-ray (dynamical) sees")
print("         essentially the SAME residual as lensing. No room for a big slip.")

# (b) THEORY bound (AeST): Psi = -Phi by construction -> s_AeST = 1.000 EXACTLY.
#     FPS verbatim: dynamical mass = lensing mass by construction in MONDian gravity.
print("  (b) AeST THEORY: Psi = -Phi by construction -> lensing mass = dynamical mass")
print("      EXACTLY (FPS 2410.02612, verbatim). s_AeST = 1.000. NO slip. This is a")
print("      DESIGN requirement (else AeST fails Bullet/solar lensing/GW170817 c_T=c).")

# (c) FRAMEWORK's OWN predicted slip gamma = 2*sqrt(1+a0/g_N) - 1 (banked, 287e7b59).
#     Show it is the SAME enhancement in lensing AND dynamics -> does NOT open a gap.
a0, gN = sp.symbols('a0 g_N', positive=True)
# dynamical (orbital) enhancement: g_obs/g_N = sqrt(1+a0/g_N) (deep-MOND interp on g_bar)
mu_dyn  = sp.sqrt(1 + a0/gN)
# lensing slip gamma (banked): gamma = 2*sqrt(1+a0/g_N) - 1 ; lensing deflection ~ (1+gamma)/2 * dyn
gamma   = 2*sp.sqrt(1 + a0/gN) - 1
# the lensing mass enhancement is (1+gamma)/2 relative to the NEWTONIAN baryon, the dynamical
# enhancement is mu_dyn relative to the same baryon. Their RATIO is the slip s:
s_fw = sp.simplify(((1+gamma)/2) / mu_dyn)
print("  (c) FRAMEWORK slip gamma = 2*sqrt(1+a0/g_N)-1 (banked).")
print("      lensing/dynamical mass ratio s = (1+gamma)/2 / sqrt(1+a0/g_N) = %s" % sp.simplify(s_fw))
# evaluate at the core g_N/a0 ~ 0.2 (deep-MOND core)
for ratio in [0.1, 0.2, 0.5, 1.0]:
    val = float(s_fw.subs({a0:1.0, gN:1.0/ratio}))
    print("        g_N/a0 = %.2f -> s = %.4f" % (ratio, val))
print("      -> s = 1.000 IDENTICALLY: gamma is DEFINED as 2*mu_dyn-1, so (1+gamma)/2 = mu_dyn.")
print("      The framework's slip is the SAME phantom in both channels, counted ONCE.")
print("      There is NO extra lensing-only mass to subtract from the dynamical target.")

# =====================================================================
# 2. BOTH-WAYS: maximum gap-shrink if we grant the DATA slip (s=1.03)
# =====================================================================
print("\n" + "-"*94)
print(" 2. BOTH WAYS: even granting the FULL observed s=1.03 slip, how much does the gap shrink?")
print("-"*94)
# if the dynamical target is M_lens / s_data:
M_dyn_target = M_target_lens / s_data
gap_dyn = M_dyn_target - M_phantom_MI
print("  Dynamical target (M_lens / 1.03) = %.3e Msun" % M_dyn_target)
print("  Dynamical core gap               = %.3e Msun  (vs lensing gap %.3e)" % (gap_dyn, core_gap))
shrink = 100*(core_gap - gap_dyn)/core_gap
print("  => the slip shrinks the gap by only %.1f%% (the 3%% two-probe slack) -- NEGLIGIBLE." % shrink)
print("  Even at the data ceiling, the DYNAMICAL residual a no-DM theory must source is")
print("  %.3e Msun, still ~%.1fx the framework's %.3e MI phantom." % (M_dyn_target, M_dyn_target/M_phantom_MI, M_phantom_MI))

# =====================================================================
# 3. GATES
# =====================================================================
print("\n" + "="*94)
print(" GATES for candidate (i) [lensing-vs-dynamics split]")
print("="*94)
print("  G1 SUFFICIENCY : FAILS -- no real split. The data caps the slip at 1.03 (3%),")
print("                   AeST has s=1 by construction, and the framework's gamma-slip is")
print("                   the SAME phantom in both channels (s=1 identically). The")
print("                   dynamical target is NOT meaningfully smaller than the lensing")
print("                   target. Gap-shrink <= 3%%, vs the ~290%% shortfall.")
print("  G2 GALAXY-VETO : N/A (subtracts target, doesn't add a galaxy-breaking field).")
print("  G3 NO-PARTICLE : PASS trivially (no new mass introduced).")
print("  G4 DATA        : DECISIVE AGAINST -- the OBSERVED two-probe ratio 1.03 IS the")
print("                   measurement that there is no core slip. A big slip is excluded")
print("                   by the lensing=X-ray agreement.")
print("\n  VERDICT (i): NOT a third ingredient. The lensing-vs-dynamics split is ~3%% (data),")
print("  0%% (AeST by construction / framework gamma counted once). The dynamical residual")
print("  EQUALS the lensing residual to 3%%. Both ways: no gap-shrink to exploit.")
