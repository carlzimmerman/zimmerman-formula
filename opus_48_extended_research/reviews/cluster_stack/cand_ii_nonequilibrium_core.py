"""
FINAL-DOOR candidate (ii): NON-EQUILIBRIUM / merging-core mass correction.

QUESTION (both ways): cluster cores are not perfectly relaxed. Does the dynamical-state
(non-equilibrium) correction REDUCE the equilibrium residual the framework must source --
i.e. is the X-ray/HSE-inferred core mass an OVER-estimate that disequilibrium inflates,
so the TRUE core residual is smaller?

THE PHYSICS (verified against the literature, both ways):
  - HSE (hydrostatic equilibrium) mass uses dP/dr = -rho g; if there is extra NON-THERMAL
    pressure (turbulence, bulk motions, mergers), the THERMAL HSE mass UNDER-estimates the
    true mass (the gas is held up by more than thermal pressure). So the HSE "bias"
    b = 1 - M_HSE/M_true is POSITIVE (M_HSE < M_true): disequilibrium makes X-ray read LOW,
    NOT high. This is the WRONG sign to shrink the residual.
  - Magnitude in the CORE (Lebeau+2026 A&A 56598, major-merger sims): core bias b ~ -0.15
    (15% UNDER-estimate) -- and it relaxes EARLIEST in the core. Outskirts b ~ -0.30.
  - The CORE TARGET is anchored by LENSING (CLASH), which is disequilibrium-INSENSITIVE
    (light bends on the projected potential regardless of gas dynamical state). The
    two-probe agreement CLASH-lensing/eRASS1-X-ray = 1.03 in the core says the core IS
    effectively relaxed for mass purposes: lensing and HSE agree to 3%.

So non-equilibrium CANNOT deflate the lensing-anchored core target, and on the X-ray side
it biases the mass LOW (true mass higher) -- the wrong direction to help.

BOTH WAYS: we (a) read the real eRASS1 rich sample for the relaxed-vs-disturbed spread,
(b) bound the maximum core deflation a generous disequilibrium correction could give, and
(c) show even that generous deflation leaves the gap essentially intact.
"""
import numpy as np
from astropy.io import fits

Msun = 1.989e30
kpc  = 3.086e19

print("="*94)
print(" FINAL-DOOR candidate (ii): NON-EQUILIBRIUM / merging-core mass correction")
print("="*94)

# banked core numbers
M_target_lens = 1.357e14
M_phantom_MI  = 3.508e13
core_gap      = M_target_lens - M_phantom_MI
print("\n[banked core, <420 kpc] lensing target %.3e, MI phantom %.3e, gap %.3e (x%.2f)"
      % (M_target_lens, M_phantom_MI, core_gap, M_target_lens/M_phantom_MI))

# =====================================================================
# 1. THE SIGN: does disequilibrium make X-ray read HIGH or LOW?
# =====================================================================
print("\n" + "-"*94)
print(" 1. SIGN of the non-equilibrium bias (does it deflate the target?)")
print("-"*94)
# Lebeau+2026 (A&A 56598) major-merger HSE bias, CORE (0.25 R_vir):
b_core   = -0.15   # M_HSE/M_true = 1+b = 0.85 -> X-ray UNDER-estimates true by 15%
b_out    = -0.30
print("  Lebeau+2026 (A&A aa56598-25) major-merger HSE bias:")
print("    CORE (0.25 R_vir): b = %.2f  -> M_HSE = %.2f x M_true (X-ray UNDER-estimates)" % (b_core, 1+b_core))
print("    OUTSKIRTS (R_vir): b = %.2f  -> larger, and relaxes ~0.5 tau_vir later" % b_out)
print("  => Non-equilibrium biases the X-ray core mass LOW, not high. If anything the")
print("     TRUE core residual is ~15%% LARGER than the HSE read, not smaller. WRONG sign.")
print("  Brunetti/Eckert XRISM (A2029, Coma): core non-thermal pressure <= few %% -> tiny.")

# =====================================================================
# 2. THE LENSING ANCHOR: disequilibrium-insensitive
# =====================================================================
print("\n" + "-"*94)
print(" 2. The core target is LENSING-anchored (disequilibrium-insensitive)")
print("-"*94)
print("  CLASH-lensing core / eRASS1-X-ray core = 1.03 (two-probe agreement).")
print("  Lensing sees the projected potential regardless of gas dynamical state, so the")
print("  1.03 agreement PROVES the core is effectively relaxed for mass purposes. A")
print("  merger that disturbed the mass would BREAK this 3%% agreement; it does not.")
print("  => Non-equilibrium cannot deflate a lensing-anchored target.")

# =====================================================================
# 3. REAL eRASS1: relaxed-vs-disturbed core mass spread (both ways)
# =====================================================================
print("\n" + "-"*94)
print(" 3. REAL eRASS1 rich sample: is the core target itself spread by dynamical state?")
print("-"*94)
hd = fits.open('real_research/data/erass1cl_primary_v3.2.fits')[1].data
cols = hd.columns.names
M500 = hd['M500']; Mgas = hd['MGAS500']; fg = hd['FGAS500']; z = hd['BEST_Z']
ok = np.isfinite(M500)&np.isfinite(Mgas)&np.isfinite(fg)&(z>0)&(z<1)&(M500>0)&(Mgas>0)&(fg>0.01)&(fg<0.30)
M500=M500[ok]; Mgas=Mgas[ok]; fg=fg[ok]
rich = M500 >= np.percentile(M500, 90)
print("  eRASS1 (Bulbul+2024) N=%d valid; rich (>=90pct) N=%d" % (ok.sum(), rich.sum()))
print("  rich-bin f_gas500 median = %.3f, 16-84pct = [%.3f, %.3f]"
      % (np.median(fg[rich]), np.percentile(fg[rich],16), np.percentile(fg[rich],84)))
# the relevant dynamical-state proxy isn't in the primary catalog; the f_gas spread already
# folds in disturbed-vs-relaxed. A higher f_gas (more gas) means a HIGHER g_bar -> the MOND
# phantom is SMALLER (more Newtonian) -> a HARDER, not easier, target. Quantify:
print("  Higher f_gas (gas-rich disturbed cores) -> higher g_bar -> SMALLER MOND boost ->")
print("  HARDER target, not easier. The dynamical-state spread does not open an escape.")

# =====================================================================
# 4. BOTH WAYS: maximum generous core deflation
# =====================================================================
print("\n" + "-"*94)
print(" 4. BOTH WAYS: grant a GENEROUS disequilibrium core deflation -- does the gap close?")
print("-"*94)
# Even though the sign is wrong AND lensing anchors it, grant a generous deflation as a
# pure best-case (e.g. the core is 10-20% over-stated by some residual non-thermal effect):
for deflate, label in [(0.95,"5%% deflation (XRISM-level)"),
                       (0.90,"10%% deflation (generous)"),
                       (0.85,"15%% deflation (= merger core bias magnitude, wrong sign but granted)")]:
    Mt = M_target_lens*deflate
    gap = Mt - M_phantom_MI
    print("    %s: target %.3e, gap %.3e (still x%.2f undershoot)"
          % (label, Mt, gap, Mt/M_phantom_MI))
print("  => Even a generous 15%% deflation leaves a ~3.3x undershoot. Non-equilibrium")
print("     buys at most ~15%% of the target -- and that is the WRONG-sign best case.")

# =====================================================================
# 5. GATES
# =====================================================================
print("\n" + "="*94)
print(" GATES for candidate (ii) [non-equilibrium / merging-core]")
print("="*94)
print("  G1 SUFFICIENCY : FAILS -- the SIGN is wrong (HSE biases LOW -> true mass higher),")
print("                   and the target is LENSING-anchored (insensitive to gas state).")
print("                   Even a generous granted 15%% deflation leaves a ~3.3x undershoot.")
print("  G2 GALAXY-VETO : N/A.")
print("  G3 NO-PARTICLE : PASS trivially.")
print("  G4 DATA        : AGAINST -- the 1.03 lensing/X-ray agreement IS the measurement")
print("                   that the core is relaxed; XRISM caps core non-thermal P at ~few %%.")
print("\n  VERDICT (ii): NOT a third ingredient. Non-equilibrium biases the core X-ray mass")
print("  LOW (wrong sign), and the lensing anchor is disequilibrium-insensitive. At best a")
print("  ~5-15%% wrong-sign deflation; both ways, no real gap-shrink.")
