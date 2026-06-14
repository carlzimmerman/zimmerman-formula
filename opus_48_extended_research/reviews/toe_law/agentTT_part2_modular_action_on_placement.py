"""
agentTT ROUTE 2 — Part 2: DOES THE BOOST MODULAR FLOW ACT ON THE PLACEMENT LABEL?

This is the decisive forcing-vs-preference test, and the SS failure mode transposed.

SS found a REAL symmetry that PERMITS-NOT-FORCES because it acted by a scale-free
DILATION on a SCALE-DECOUPLED target (weight -1 => slides, pins nothing). The
analogue here: if the boost modular flow does NOT move the placement label
theta_v (i.e. theta_v is an invariant / superselection label the modular flow is
blind to), then modular covariance is SILENT on the placement => permits/agnostic.
If the modular flow MOVES theta_v and only theta_v=pi/2 is a fixed point carrying
the KMS-required (finite-temperature, two-sided) weight while the edge theta_v->pi
carries a FORBIDDEN weight, that is a genuine SELECTION.

THE PLACEMENT, precisely (banked from agentR/agentS):
  - DSSYK energy variable E = cos(theta), theta in [0, pi]. The matter chord is
    placed at theta_v. CENTER = theta_v = pi/2 (E=0, top of band, N-hat vacuum /
    infinite-T). EDGE = theta_v -> pi (E -> E0 = -1, band edge, H-extremal).
  - The transfer matrix / boost generator in the chord Hilbert space: the
    static-patch boost L_0 is realized on the q-deformed oscillator. Its action on
    energy eigenstates is a SHIFT in the conjugate (chord-number / time) variable,
    i.e. a DILATION on the spectral plane.

We compute the orbit of theta_v under the boost/dilation modular flow and ask
whether it is moved or fixed, and with what weight.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
print("="*78)
print("PART 2 — modular (boost/dilation) action on the placement label theta_v")
print("="*78)

# ---------------------------------------------------------------------------
# (A) The boost = dilation acts on the static-patch TIME/ENERGY plane.
# In the static patch, the boost generator K (= L_0 = modular Hamiltonian/2pi)
# generates the Killing flow that is a boost near the horizon and a time-
# translation in the bulk. On the energy axis it acts as omega -> omega (energy
# is the boost charge: [K, |omega>] = omega |omega>, eigen-shift in modular time).
# Crucially: the boost is DIAGONAL on energy eigenstates. The placement theta_v
# selects an energy E_v = cos(theta_v). The boost does NOT change an energy
# eigenvalue (energy is its conserved charge). So:
#
#   sigma_t |E_v> = e^{i E_v t / something}|E_v>   (a phase, fixed |E_v|)
#
# => the boost modular flow leaves the placement ENERGY (hence theta_v) FIXED.
# This is the first crucial finding: theta_v is a MODULAR-INVARIANT label.
# ---------------------------------------------------------------------------
theta_v, t_mod, E = sp.symbols('theta_v t_mod E', real=True)
Ev = sp.cos(theta_v)
print("\n(A) Boost is diagonal on energy eigenstates (energy = boost charge).")
print(f"    Placement energy E_v = cos(theta_v). Under modular flow sigma_t:")
print(f"    sigma_t |E_v> = e^(i E_v t_mod)|E_v>  => |E_v| FIXED => theta_v INVARIANT.")
print("    => The modular flow does NOT rotate one placement into another.")
print("    => theta_v is a SUPERSELECTION / which-rep label the boost is BLIND to.")

# ---------------------------------------------------------------------------
# (B) BUT: that is not the end. The modular flow being blind to theta_v means it
# cannot DYNAMICALLY rotate edge into center. The forcing question is sharper:
# modular covariance requires the PHYSICAL state to BE KMS at beta_mod=2pi w.r.t.
# the boost. Each placement defines a DIFFERENT GNS state (different cyclic vector
# = the matter chord at theta_v). For EACH such state we ask: is the boost its
# modular flow at beta=2pi? Tomita-Takesaki gives a UNIQUE answer per algebra+vector.
#
# So the real test is: for which theta_v is the boost L_0 the modular generator of
# the GNS state, at the correct temperature? This is decided by the KMS analyticity
# strip width = beta. Compute the effective inverse temperature beta(theta_v) that
# the placement's 2pt actually realizes under the boost, and see whether beta=2pi
# (=> GH) selects a placement.
# ---------------------------------------------------------------------------
print("\n(B) Per-placement effective modular temperature (KMS strip width).")
print("    The boost is the SAME operator for all placements; what differs is the")
print("    STATE (cyclic vector = chord at theta_v). T-T: the boost is the modular")
print("    flow of the GH state at beta_mod=2pi. Ask: does the placement's 2pt obey")
print("    KMS at beta_mod=2pi under the boost? Decide by the decay/period structure.")

# From agentS, the boost-frame 2pt decay rates are:
#   Gamma_n(theta_v) = sin(theta_v) * sinh((Delta+n) lambda)   [the PLACEMENT-rate]
# (center theta_v=pi/2: sin=1, full ladder; edge theta_v->pi: sin->0, rates vanish).
lam, Delta = sp.symbols('lambda Delta', positive=True)
n = sp.symbols('n', integer=True, nonnegative=True)
Gamma_n = sp.sin(theta_v) * sp.sinh((Delta + n) * lam)
print(f"\n    Boost-frame decay rate (agentS): Gamma_n = sin(theta_v) sinh((Delta+n)lambda)")

# KMS detailed balance under the boost requires the spectral function to be
# two-sided with ratio e^{-beta_mod omega_mod}. The KEY modular fact:
# Re(omega_pole) = 0 (purely imaginary) is the signature that the mode sits at the
# modular FIXED axis. A NONZERO Re(omega) = real oscillation = the mode is NOT
# boost-fixed and breaks the KMS-at-2pi structure (it is a BH-like ringing mode,
# which is KMS only at a DIFFERENT (Hawking) temperature, not the GH one).
#
# agentS: only theta_v = pi/2 gives Re(omega)=0 exactly; every interior theta_v
# rings (Re omega != 0); the edge theta_v->pi has NO ladder at all (power law).
print("\n    Re(omega_pole) per placement (agentS scan): ")
print("       theta_v = pi/2  : Re omega = 0   (boost-FIXED => KMS-at-2pi structure)")
print("       theta_v interior: Re omega != 0  (rings; KMS only at a SHIFTED temp)")
print("       theta_v -> pi    : no ladder, |G|~t^-3/2 (one-sided, T=0)")

# ---------------------------------------------------------------------------
# (C) The decisive distinction (FORCING vs PREFERENCE), computed cleanly.
# The boost cannot MOVE theta_v (part A). So modular covariance cannot DYNAMICALLY
# forbid the edge by rotating it away. What it CAN do: declare which placements
# yield a state whose modular flow IS the boost at beta_mod=2pi. That is a
# CONSTRAINT on BEING the GH state. Is that constraint a FORCING of the placement?
#
# It is a forcing IF AND ONLY IF the physical input "the dS vacuum = the GH state
# (KMS at T_dS under the boost)" is ITSELF forced/banked, rather than an
# identification we are choosing. THIS is the crux, and it is exactly parallel to
# SS's c_chi<->H decoupling dependency. Make it explicit and test it in Part 3-5.
# ---------------------------------------------------------------------------
print("\n(C) FORCING-vs-PREFERENCE crux (to resolve in Parts 3-5):")
print("    - The boost cannot rotate theta_v (energy is its charge) => it cannot")
print("      DYNAMICALLY forbid the edge. [PART A: theta_v modular-INVARIANT.]")
print("    - Modular covariance DOES single out theta_v=pi/2 as the UNIQUE")
print("      boost-fixed (Re omega=0), KMS-at-2pi placement. [structural, agentS+T-T]")
print("    - WHETHER this FORCES the placement hinges on whether 'dS vacuum = the GH")
print("      KMS state under the boost' is a BANKED physical requirement or a CHOSEN")
print("      identification. This is the TT analogue of SS's c_chi<->H dependency.")
print("\n    => Provisional: modular covariance is a NECESSARY CONDITION that the")
print("       center UNIQUELY passes and the edge FAILS, but it FORCES the placement")
print("       only modulo the (physical, not algebraic) premise that the dS vacuum")
print("       must be the boost-KMS state. Test that premise's status next.")
