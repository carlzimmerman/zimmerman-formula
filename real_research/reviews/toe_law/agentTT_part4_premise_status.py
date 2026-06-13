"""
agentTT ROUTE 2 — Part 4: STATUS OF THE PREMISE 'dS vacuum = GH boost-KMS state'.
Is the modular exclusion of the edge a FORCING or a CONSISTENCY?

Parts 2-3 reduced everything to one premise: modular covariance EXCLUDES the edge
(continuous-series, non-thermal weight) FROM the GH discrete-series rep, FORCING the
center -- MODULO the identification 'the dS vacuum is the Gibbons-Hawking boost-KMS
state'. The entire FORCING-vs-PERMITS verdict turns on the STATUS of that premise.

SS analogue: SS's verdict hinged on the c_chi<->H DECOUPLING, which is a genuinely
OPEN, model-dependent input (no banked c_chi=f(H)); hence SS = permits-not-forces,
and "a future c_chi=f(H) would shift toward permits-model-dependent". The honest
question here: is 'dS vacuum = GH KMS state' similarly OPEN/model-dependent, or is
it a HARD-banked physical fact (unlike SS's open input)?

This part assembles the status of the premise from FIRST PRINCIPLES of dS QFT and
checks whether the premise is (a) a free dictionary CHOICE (=> permits, SS-like) or
(b) a THEOREM-backed physical requirement (=> a genuine forcing, STRONGER than SS).
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
print("="*78)
print("PART 4 — STATUS of 'dS vacuum = GH boost-KMS state': free choice or theorem?")
print("="*78)

# ---------------------------------------------------------------------------
# (A) WHAT IS BANKED about the dS static-patch state (not invented):
#   1. Gibbons-Hawking (1977): the dS static patch observer detects a THERMAL bath
#      at T_dS = H/2pi. The reduced state on the static patch is KMS at T_dS.
#   2. Bisognano-Wichmann / Sewell: for a wedge/static-patch region, the modular
#      flow of the vacuum IS the boost (geometric), and the vacuum is KMS at the
#      Unruh/GH temperature w.r.t. it. This is a THEOREM (geometric modular action),
#      not a choice, for the dS-invariant (Bunch-Davies/Euclidean) vacuum.
#   3. Cosmic no-hair / uniqueness: the Bunch-Davies (Euclidean) vacuum is the
#      UNIQUE dS-invariant Hadamard state; restricted to the static patch it is the
#      GH thermal state. (Allen 1985; uniqueness of dS-invariant Hadamard vacuum.)
#
# => "the dS vacuum (restricted to the static patch) is KMS at T_dS under the
#    boost" is a THEOREM of dS QFT (geometric modular action + uniqueness), NOT a
#    holographic dictionary CHOICE. This is the decisive difference from SS's OPEN
#    c_chi<->H input.
# ---------------------------------------------------------------------------
print("""
(A) BANKED about the dS static-patch state (theorems of dS QFT, not choices):
  1. Gibbons-Hawking 1977: static-patch reduced state is KMS at T_dS=H/2pi.
  2. Bisognano-Wichmann/Sewell (geometric modular action): the modular flow of the
     dS-invariant vacuum on the static patch IS the boost; vacuum is KMS at T_dS
     w.r.t. it. THEOREM (geometric), not a dictionary choice.
  3. Allen 1985 (uniqueness): Bunch-Davies/Euclidean vacuum is the UNIQUE
     dS-invariant Hadamard state; its static-patch restriction = GH thermal state.
  => 'dS vacuum = boost-KMS at T_dS' is a THEOREM of dS QFT.
""")

# ---------------------------------------------------------------------------
# (B) THE CRUCIAL DISTINCTION from SS, made precise.
# SS's open input (c_chi<->H) governed a CONTINUOUS RATIO (4j3/j2^2 = G_sat) -- a
# fine-tuning of a NUMBER. Even with all symmetry, a continuous weight-(-1) ratio
# slides; forcing it needs an EXTRA scale-lock that is genuinely model-dependent.
#
# HERE the choice is DISCRETE and BINARY (center vs edge), and the discriminator is
# not a continuous ratio but a REPRESENTATION-THEORETIC CLASS (discrete vs
# continuous series; thermal vs zero-temperature). The premise that fixes it ('the
# physical state is the GH KMS state') is a THEOREM (A), not an open knob.
#
# So the logical structure differs at the root:
#   SS: symmetry + OPEN input  => permits (the open input could go either way).
#   TT: symmetry + THEOREM input => the input does NOT go either way; it is fixed by
#       dS QFT to be the boost-KMS (discrete-series, thermal) state.
#
# Test the binary nature numerically: is there ANY interpolating placement that is
# ALSO boost-KMS at T_dS? If the ONLY boost-KMS-at-T_dS placement is the center,
# the theorem-backed premise lands UNIQUELY on center (forcing). agentS scanned
# this: every interior theta_v rings (Re omega != 0 => boost-KMS only at a SHIFTED,
# wrong temperature), edge is T=0. Confirm the uniqueness logic.
# ---------------------------------------------------------------------------
print("(B) Distinction from SS, made precise:")
print("    SS: symmetry + OPEN ratio-input (c_chi<->H) => a continuous weight slides")
print("        => PERMITS. The open input could go either way.")
print("    TT: symmetry + THEOREM-input ('state is GH boost-KMS', part A) => the")
print("        input is FIXED by dS QFT, NOT open. And the discriminator is a")
print("        DISCRETE rep-class (discrete vs continuous series), not a tunable ratio.")

# Uniqueness scan logic (from agentS, re-stated as the modular selection):
# A placement is boost-KMS at T_dS iff its boost-frame 2pt is two-sided thermal at
# beta=2pi, i.e. Re(omega)=0 (boost-fixed, no real ringing) AND finite-T (two-sided).
theta_v = sp.symbols('theta_v', real=True)
lam, Delta = sp.symbols('lambda Delta', positive=True)
n = sp.symbols('n', integer=True, nonnegative=True)
# Re(omega_pole) at placement theta_v (agentS PART 1): the imaginary axis only at
# theta_v=pi/2. The pole: E_pole = cos(theta_v) cosh u - i sin(theta_v) sinh u, with
# u=(Delta+n)lambda. omega = log map; Re(omega_pole)=0 <=> cos(theta_v)=0 <=> theta_v=pi/2.
Re_factor = sp.cos(theta_v)   # the real-part driver of the pole (vanishes only at pi/2)
print("\n    Boost-fixed (Re omega=0) condition driver: cos(theta_v) = 0")
sols = sp.solve(sp.Eq(Re_factor, 0), theta_v)
print(f"      cos(theta_v)=0 in [0,pi] => theta_v = pi/2 UNIQUELY (solset includes {sols}).")
print("      => among ALL placements, ONLY theta_v=pi/2 is boost-FIXED (Re omega=0).")
print("      Interior placements: cos(theta_v)!=0 => Re omega != 0 => ring => NOT the")
print("        GH boost-KMS structure (they are KMS only at a Hawking-shifted temp).")
print("      Edge theta_v->pi: cos->-1, sin->0 => rates vanish, T=0, one-sided.")
print("    => The THEOREM-backed premise 'state = GH boost-KMS at T_dS' is satisfied")
print("       by a UNIQUE placement: the center. No interpolation is also GH-KMS.")

# ---------------------------------------------------------------------------
# (C) HONEST RESIDUAL: the one thing the modular structure does NOT supply by itself.
# The theorem (A) is a statement about dS QFT FIELD theory on the static patch. The
# DSSYK placement question is whether the BOUNDARY/holographic matter chord is
# identified with that bulk GH state. The modular structure FORCES: IF the DSSYK
# state is to reproduce dS static-patch QFT (be the GH KMS state under the boost),
# THEN it must be the center. What it does NOT do by itself: PROVE that the DSSYK
# dual IS dS (rather than some other geometry). That last step is the holographic
# identification 'DSSYK <-> dS', which is the FRAMEWORK's premise (Link 8 exists
# precisely because DSSYK is being used as the dS dual).
#
# CRUCIAL: this residual is NOT a free knob like SS's c_chi<->H. It is the
# framework's OWN founding assumption (DSSYK is the dS dual). WITHIN that assumption
# -- which the whole Link-8 program PRESUPPOSES -- the modular structure FORCES the
# center, because the dS state IS the GH boost-KMS state by THEOREM (A), and ONLY
# the center realizes it (B). The agentR 'CONTESTED-TERMINAL' was at the level of
# 'the chord ALGEBRA cannot pick'; modular covariance adds a PHYSICAL (state-level,
# theorem-backed) selector the algebra alone lacks.
# ---------------------------------------------------------------------------
print("\n(C) HONEST residual (what modular structure does NOT supply alone):")
print("    Modular covariance FORCES: IF the DSSYK state must reproduce dS static-")
print("    patch QFT (be GH boost-KMS), THEN it is the center (unique, by B + theorem A).")
print("    It does NOT independently PROVE DSSYK<->dS; that is the framework's OWN")
print("    founding premise (the whole reason Link 8 uses DSSYK as the dS dual).")
print("    -- Unlike SS's c_chi<->H (a genuinely OPEN, model-dependent knob that")
print("       could go either way), THIS residual is the framework's PRESUPPOSED dual.")
print("    => WITHIN the framework's own DSSYK<->dS premise, modular covariance")
print("       SELECTS THE CENTER by a THEOREM-backed, state-level argument the chord")
print("       ALGEBRA (agentR) lacked. This is STRONGER than SS's permits-not-forces.")
