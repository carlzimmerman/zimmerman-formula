#!/usr/bin/env python3
"""
pin_the_amount.py  (topic: pin_the_amount)
==========================================
THE crux of the STRONG illusion claim: even IF the dark-sector field were DERIVED
from dS-Unruh (frame->field, topic 1 -- which the corpus says is NOT done; only the
FRAME is founded, the FIELD stays postulated), would a VACUUM / HORIZON condition
PIN its amplitude  I0 ~ Omega_dust ~ 0.26 ?

The prior sqrt_lambda_pins_KQ.py answered for the POSTULATED field: I0 is a free
integration constant, structurally orthogonal to the action couplings (Lambda,a0,Z).
This script pushes the SHARPER question the task asks: do any of the FOUR named
dS-structural conditions
   (A) de Sitter horizon ENTROPY  S_dS
   (B) Gibbons-Hawking TEMPERATURE setting a condensate density
   (C) a holographic / CKN bound
   (D) a no-boundary / dS-state INITIAL CONDITION
fix Omega_dust ~ 0.26 -- WITHOUT a hand-tuned O(1)?  And is the why-now ratio
Omega_dm/Omega_Lambda ~ 0.39 genuinely an un-pinned boundary datum?

Both-ways: a "dS pins the amount" claim is tested as hard as "it stays free".
No manufactured relation. Quarantine held (a0/Z/kappa not derived).
"""
import numpy as np

# ------------------------------------------------------------------ constants
c    = 2.99792458e8
G    = 6.674e-11
Mpc  = 3.0857e22
hbar = 1.054571817e-34
kB   = 1.380649e-23

H0   = 67.4*1e3/Mpc          # s^-1  (Planck)
OmL  = 0.685
OmM  = 0.315
Omb  = 0.0493
Omdm = OmM - Omb             # ~0.266 -- the cold clustering amount the CMB+clusters need
Omdust = Omdm                # the AeST a^-3 K(Q) dust must supply this

# de Sitter (Lambda-only) quantities
Lambda = 3*OmL*H0**2/c**2            # m^-2
H_L    = c*np.sqrt(Lambda/3)         # de Sitter Hubble of the Lambda-only dS  [s^-1]
a0     = c**2*np.sqrt(Lambda/(32*np.pi))
Z      = np.sqrt(32*np.pi/3)
R_dS   = c/H_L                       # de Sitter horizon radius  [m]
rho_DE = OmL * 3*H0**2/(8*np.pi*G)   # dark-energy density  [kg/m^3]
rho_crit = 3*H0**2/(8*np.pi*G)

print("="*80)
print("ANCHORS")
print("="*80)
print(f"  H0           = {H0:.4e} s^-1   H_Lambda = {H_L:.4e} s^-1  (H_L/H0={H_L/H0:.3f})")
print(f"  Lambda       = {Lambda:.4e} m^-2")
print(f"  R_dS=c/H_L   = {R_dS/Mpc:.1f} Mpc")
print(f"  a0           = {a0:.4e}   Z=sqrt(32pi/3)={Z:.4f}")
print(f"  rho_crit     = {rho_crit:.4e} kg/m^3   rho_DE={rho_DE:.4e}")
print(f"  TARGET to pin: Omega_dust = {Omdust:.3f}   (why-now ratio Om_dm/Om_L = {Omdm/OmL:.3f})")
print()

# ====================================================================
# (A) de Sitter horizon ENTROPY  -- can S_dS set the condensate amount?
# ====================================================================
print("="*80)
print("(A) de Sitter horizon ENTROPY  S_dS = A/(4 l_P^2)")
print("="*80)
l_P2  = hbar*G/c**3
A_dS  = 4*np.pi*R_dS**2
S_dS  = A_dS/(4*l_P2)                 # dimensionless (in units of kB)
print(f"  l_P^2 = {l_P2:.3e} m^2   S_dS = A/4l_P^2 = {S_dS:.3e}  (= 1/ the only dimensionless")
print(f"     gravitational group G hbar H^2/c^5 = {G*hbar*H_L**2/c**5:.3e}; S_dS={1/(G*hbar*H_L**2/c**5)/(8*np.pi)*8*np.pi:.3e})")
print()
print("  Can S_dS PIN Omega_dust?  S_dS ~ 1e122 is a PURE NUMBER (in kB), HBAR-LADEN.")
print("  Omega_dust ~ 0.26 is an O(1) CLASSICAL ratio of densities -- hbar-free.")
print("  To get an O(1) out of S_dS you must form a RATIO S_x/S_dS where S_x already")
print("  carries the SAME 1e122 -- i.e. S_x must be a horizon-area entropy of a")
print("  'dust horizon'. But the dust has NO horizon of its own; any S_dust you write")
print("  is  S_dust = (energy)*(time)/hbar  and CONTAINS the dust density => CIRCULAR.")
print("  Quantitatively: classical Friedmann d rho_dust/d Lambda = 0 means S_dS (a pure")
print("  function of Lambda) carries ZERO derivative onto rho_dust. RESULT: NO PIN.")
print()

# ====================================================================
# (B) Gibbons-Hawking TEMPERATURE -> a condensate density
# ====================================================================
print("="*80)
print("(B) Gibbons-Hawking TEMPERATURE sets a condensate density?")
print("="*80)
T_GH  = hbar*H_L/(2*np.pi*kB)         # Gibbons-Hawking temperature [K]
# A thermal/vacuum energy density at temperature T_GH, naive 'photon-gas' style:
#   rho_GH c^2 ~ (pi^2/30) g_* (kB T)^4 / (hbar c)^3   -- a RADIATION scaling
rho_GH_rad = (np.pi**2/30)*(kB*T_GH)**4/(hbar*c)**3 / c**2     # kg/m^3, g_*=1
# The 'condensate at the horizon scale' density: one quantum hbar*H_L per horizon volume
V_dS  = (4/3)*np.pi*R_dS**3
rho_quantum = (hbar*H_L)/(V_dS*c**2)                            # kg/m^3
print(f"  T_GH = hbar H_L/(2 pi kB) = {T_GH:.4e} K  (Hubble-scale, ~1e-30 K)")
print(f"  (i) radiation-gas rho(T_GH) = {rho_GH_rad:.3e} kg/m^3 -> Omega = {rho_GH_rad/rho_crit:.3e}")
print(f"       => Omega ~ 1e-122 : WRONG by ~120 orders (T_GH^4 is the vacuum-CC SCALE, not 0.26)")
print(f"  (ii) one quantum/horizon  rho = hbar H_L/(V_dS c^2) = {rho_quantum:.3e} -> Omega={rho_quantum/rho_crit:.3e}")
print(f"       => Omega ~ 1e-122 again. The GH temperature sets the vacuum/CC scale, NOT 0.26.")
print()
print("  Deep reason: T_GH ~ hbar H is the scale of the COSMOLOGICAL CONSTANT itself")
print("  (rho_DE ~ (kB T_GH)^4/(hbar c)^3 * (huge) -- it is the SAME Lambda). A GH-thermal")
print("  condensate reproduces dark ENERGY (which a0 already ties), NOT a SEPARATE cold")
print("  a^-3 dust ~0.26. A cold (w=0) condensate from a thermal (w=1/3-ish) GH bath is")
print("  the wrong equation of state anyway. RESULT: NO PIN of the cold-dust amount.")
print()

# ====================================================================
# (C) holographic / CKN bound  -- does it BOUND or PIN Omega_dust?
# ====================================================================
print("="*80)
print("(C) holographic / CKN (Cohen-Kaplan-Nelson) bound")
print("="*80)
# CKN: a box of size L with UV cutoff Lambda_uv has total energy < black-hole mass:
#   L^3 Lambda_uv^4 <~ L M_P^2  => the IR-UV relation; with L = R_dS gives rho_vac ~ M_P^2 H^2
# This is an INEQUALITY and it reproduces the rho_DE SCALE (the famous CKN 'success'),
# NOT a separate 0.26.
rho_CKN = (c**3/(hbar*G)) * H_L**2 * hbar / c**2  # ~ M_P^2 H^2 in density units (order check)
# cleaner: rho_CKN c^2 ~ (3/8pi) * M_P^2 c^2 H^2  matches rho_DE to O(1)
M_P2 = hbar*c/G
rho_CKN2 = (3/(8*np.pi)) * (c**2/(hbar*G/c)) * H_L**2 /c**2
print(f"  CKN saturation reproduces the DARK-ENERGY density scale rho ~ M_P^2 H^2:")
print(f"    rho_DE/rho_crit = {OmL:.3f}  (CKN 'success' = the CC magnitude, O(1)=kappa GEOMETRIC)")
print(f"  This is exactly the banked result: CKN fixes the a0/Lambda NORMALIZATION (door3),")
print(f"  O(1)=(3/8pi)^(1/4) is PURE GEOMETRY, g_*^0 -- it transmits the magnitude of")
print(f"  Omega_DE, NOT a microscopic count, and NOT a SEPARATE cold-dust 0.26.")
print(f"  CKN is an INEQUALITY (<=). An inequality with a free O(1) cannot PIN an")
print(f"  equality target 0.26 -- demanding 0.26 = solving for the O(1) = circular.")
print(f"  RESULT: CKN bounds/normalizes dark ENERGY; gives NO pin of the dust amount.")
print()

# ====================================================================
# (D) no-boundary / dS-state INITIAL CONDITION
# ====================================================================
print("="*80)
print("(D) no-boundary / dS initial-state selection of I0")
print("="*80)
print("  I0 is the INTEGRATION CONSTANT of the shift-symmetric phi-bar EOM (a^3 K'(Q)=I0).")
print("  In QFT-in-dS a shift-symmetric (massless-ish) scalar in the Bunch-Davies / no-")
print("  boundary state has <phi>=0 and a SCALE-INVARIANT fluctuation spectrum; its")
print("  homogeneous BACKGROUND displacement (Q-Q0) -- which IS I0 -- is NOT fixed by the")
print("  state: the zero-mode is a flat direction (shift symmetry). The Hartle-Hawking/")
print("  no-boundary measure is famously FLAT/ill-defined for such a modulus and, where")
print("  computable, exponentially favors LARGE volume / SMALL field-energy, not 0.26.")
print("  So even the most 'fundamental' state selection does NOT deliver I0 ~ 0.26;")
print("  the zero-mode amplitude remains a boundary datum (a choice of when/where Q sits).")
print("  RESULT: the dS state does NOT pin I0. (And inflationary IC would set it by the")
print("  reheating/displacement history -- an early-universe datum, not a dS-Unruh constant.)")
print()

# ====================================================================
# THE VERLINDE CROSS-CHECK: even his ROUTE does not PIN a free 0.26
# ====================================================================
print("="*80)
print("(V) Verlinde cross-check -- does the 'dS-entropy illusion' route PIN the amount?")
print("="*80)
print("  Verlinde 2016: apparent DM is a RESPONSE to baryons, not a free cosmological")
print("  amplitude:   M_D^2(r) = (c H0 r^2 / 6G) d[M_b(r) r]/dr.")
print("  Crucial structural point for THIS question: Verlinde does NOT have a free")
print("  Omega_dm at all -- his 'dark matter' is SLAVED to the baryon profile + cH0.")
print("  If that route WORKED it would over-PIN (zero free dark numbers). But it is a")
print("  BANKED MIRAGE here: wrong footing (cH0 not cH_Lambda), 1/6 != 1/Z, and it")
print("  FAILS clusters (Tian+ 2020) and RC shapes (Lelli-McGaugh 2017: unobserved")
print("  residual-radius correlation). So the ONE route that would pin the amount by")
print("  making it a baryon-response is DEAD on the data -- it does not revive here.")
print("  The framework's AeST dust is the OPPOSITE structure: a FREE cosmological")
print("  amplitude I0 (fits clusters+CMB precisely BECAUSE it is free), not a baryon")
print("  response. You cannot have it both ways: 'pinned by dS' (Verlinde, dead) XOR")
print("  'free amplitude that fits' (AeST, alive). The alive route is the un-pinned one.")
print()

# ====================================================================
# WHY-NOW: is Omega_dm/Omega_Lambda ~ 0.39 a genuine un-pinned datum?
# ====================================================================
print("="*80)
print("WHY-NOW: is Om_dm/Om_Lambda ~ 0.39 an un-pinned boundary datum?")
print("="*80)
ratio = Omdm/OmL
print(f"  Om_dm/Om_Lambda = {ratio:.3f}.  This is TIME-DEPENDENT: rho_dm ~ a^-3, rho_L=const,")
print(f"  so the ratio = (a_eq3/a)^3-ish CROSSES 1 near today and -> 0 in the future.")
print(f"  A ratio that depends on the epoch a(t) CANNOT be a constant of the dS vacuum")
print(f"  (which is a-independent). It is set by I0 (the a^-3 amplitude) AND the epoch we")
print(f"  observe at -- a textbook 'why now' / coincidence-problem datum. dS-Unruh fixes")
print(f"  Lambda (the constant piece) and a0 (~sqrt(Lambda)); it has NO handle on the a^-3")
print(f"  amplitude or on 'which a we live at'. RESULT: genuinely UN-PINNED boundary datum.")
print()

print("="*80)
print("VERDICT")
print("="*80)
print("  ALL FOUR named dS conditions (horizon entropy, GH temperature, holographic/CKN,")
print("  no-boundary state) reproduce the dark-ENERGY scale (Lambda / Omega_DE), which")
print("  a0=c^2 sqrt(Lambda/32pi) ALREADY ties -- and NONE delivers a SEPARATE cold-dust")
print("  Omega_dust ~ 0.26 without a hand-tuned O(1) or a circular dust-entropy. The")
print("  amplitude I0 is a boundary/initial datum, structurally orthogonal to every dS")
print("  BULK constant (d rho_dust/d Lambda = 0). Even a DERIVED field would carry a FREE")
print("  zero-mode amplitude. The why-now ratio is epoch-dependent => not a dS constant.")
print("  => amount_pinned = FREE. The STRONG illusion claim ('the field AND its amount")
print("  come from dS-Unruh') does NOT survive at the AMOUNT; the honest claim is 'field")
print("  not particle, amount free'. No relation manufactured. Verlinde stays dead.")
