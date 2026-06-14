"""
agentTT ROUTE 2 — Part 3: MODULAR WEIGHT of each placement's observable.
FORBIDDEN (forcing) vs DIFFERENT-REP (permits).

Part 2 established: the boost cannot rotate theta_v; modular covariance singles out
the center as the UNIQUE boost-fixed KMS-at-2pi placement. The remaining question:
is the edge placement carrying a FORBIDDEN modular weight (=> the symmetry EXCLUDES
it, forcing center), or merely a DIFFERENT representation the symmetry tolerates
(=> permits, like SS's weight -1 slide)?

SS standard: SS computed the modular weight of 4j3/j2^2 = weight -1, and a dilation
forces only weight-0 invariants => permits. Here we compute the modular weight of
each PLACEMENT's late-time observable and apply the same forcing criterion:
  - a placement is FORCED/EXCLUDED by modular covariance only if its observable
    carries a weight the symmetry FORBIDS (e.g. a non-thermal weight incompatible
    with the discrete-series/KMS structure that the symmetry MANDATES).
  - if both placements carry symmetry-ALLOWED weights (different reps of SL(2,R)),
    the symmetry PERMITS both and is silent on the choice.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
print("="*78)
print("PART 3 — modular weight of each placement; FORBIDDEN vs DIFFERENT-REP")
print("="*78)

lam, Delta, s = sp.symbols('lambda Delta s', positive=True)
n = sp.symbols('n', integer=True, nonnegative=True)
a = sp.symbols('a', real=True)   # dilation parameter

# ---------------------------------------------------------------------------
# (A) Under the modular flow = boost = dilation s -> e^a s (SS's convention),
# the late-time 2pt G(t) carries a scaling weight. Compute it for each placement.
#
# CENTER: G_center(t) ~ sum_n c_n e^{-Gamma_n t},  Gamma_n = sinh((Delta+n)lambda).
#   This is a DISCRETE exponential ladder. Under the dilation of the spectral
#   variable, an exponential spectrum e^{-Gamma t} maps to e^{-Gamma e^a t}, i.e.
#   the modular flow ACTS WITHIN the discrete-series tower (shifts along the ladder
#   index by the lowest-weight raising/lowering). The weight is the discrete-series
#   weight h = Delta (lowest weight). A discrete-series rep is a HIGHEST/LOWEST-
#   WEIGHT module: it is the carrier space of the modular Hamiltonian L_0 itself.
#   => CENTER weight = the discrete-series lowest weight Delta. This is the
#      KMS-NATURAL weight: L_0 acts ON it diagonally (it IS the modular spectrum).
#
# EDGE: G_edge(t) ~ t^{-3/2} = t^{-(s_E+1)}, s_E=1/2 (continuous soft-edge weight).
#   A power law t^{-p} under a dilation t->e^a t scales by e^{-a p} = HOMOGENEOUS
#   weight -p = -3/2. A pure power law is a PRINCIPAL/CONTINUOUS-series object
#   (scale-covariant, no discrete ladder, a single homogeneous weight), NOT a
#   discrete-series lowest-weight module.
# ---------------------------------------------------------------------------
print("\n(A) Modular (dilation) weight of each late-time observable:")

# CENTER: discrete ladder. Verify it transforms WITHIN the discrete series.
# Model spectral measure as the normalized descendant a_n = 1/(n!(2Delta)_n) on the
# ladder Delta+n (the SL(2,R)-canonical lowest-weight measure, banked from SS).
print("  CENTER: discrete ladder e^{-sinh((Delta+n)lambda) t}, lowest weight h=Delta.")
print("          The modular Hamiltonian L_0 spectrum IS {Delta+n}; the ladder is its")
print("          OWN discrete-series module => G_center is a WEIGHT-Delta lowest-weight")
print("          vector of the modular algebra. KMS-covariant by construction.")

# Confirm: a discrete lowest-weight module is closed under L_0 and L_{+-} (the
# SL(2,R) generators). The ladder matrix elements (n+1)(2Delta+n) (banked SS) are
# exactly the discrete-series raising/lowering norms => closed. Verify symbolically.
n_sym = sp.symbols('n', integer=True, nonnegative=True)
ladder_norm = (n_sym + 1)*(2*Delta + n_sym)   # discrete-series |L_+ |n>|^2
print(f"          discrete-series ladder norm |<n+1|L_+|n>|^2 = {ladder_norm} (>0 all n>=0):")
# positivity for all n>=0, Delta>0:
test_vals = [(0,sp.Rational(1,2)),(1,sp.Rational(1,2)),(5,sp.Rational(1,10)),(10,sp.Rational(7,10))]
allpos = all(ladder_norm.subs({n_sym:nn, Delta:dd})>0 for nn,dd in test_vals)
print(f"          positivity (sampled n,Delta): {allpos}  => unitary lowest-weight module CLOSED.")

# EDGE: power law => homogeneous weight -3/2.
p_edge = sp.Rational(3,2)
print(f"\n  EDGE: power law t^(-3/2) => homogeneous dilation weight = -{p_edge}.")
print(f"        A single homogeneous weight, no ladder => a CONTINUOUS/PRINCIPAL-series-")
print(f"        type scale-covariant object, NOT a discrete-series lowest-weight module.")

# ---------------------------------------------------------------------------
# (B) THE FORCING TEST. Is the edge's weight FORBIDDEN by the modular structure,
# or just a DIFFERENT (allowed) representation?
#
# Tomita-Takesaki / the GH modular flow is realized on a SPECIFIC representation:
# the lowest-weight DISCRETE series (banked SS: "the QNM ladder is its lowest-weight
# discrete-series rep"). The modular Hamiltonian L_0 = boost has DISCRETE spectrum
# Delta+n on the GH state's GNS space. KMS at finite beta=2pi REQUIRES this discrete
# thermal (two-sided) structure.
#
# The edge's homogeneous weight -3/2 is a CONTINUOUS/principal-series object. The
# question: does the discrete-series modular structure EXCLUDE a continuous-series
# observable?
#
# DECISIVE COMPUTATION: The KMS condition at finite beta forces a DISCRETE set of
# Matsubara-type poles / a two-sided exponential structure. A pure power law
# t^{-3/2} has a BRANCH CUT (continuous spectrum from the soft edge), NOT a discrete
# pole ladder. A branch-cut (continuous) spectral function CANNOT satisfy KMS at
# FINITE temperature with a discrete modular Hamiltonian whose GNS rep is purely
# discrete-series. Check the analyticity: KMS at beta=2pi needs analyticity in the
# strip -2pi<Im t_mod<0 with the boundary identification G(t-2pi i)=G_swap(t). A
# t^{-3/2} (branch point at t=0) under the log-clock t=e^{H tau} maps to e^{-3/2 H tau}
# = a SINGLE rate with Delta-INDEPENDENT offset 3/2 (agentS R2-fail), which is NOT a
# lowest-weight module built on Delta => it is NOT in the discrete-series carrier
# space of the GH modular flow.
# ---------------------------------------------------------------------------
print("\n(B) FORCING TEST — is edge's weight FORBIDDEN or DIFFERENT-rep?")
print("    GH modular flow is realized on the lowest-weight DISCRETE series (SS).")
print("    KMS at finite beta=2pi => discrete two-sided thermal ladder (Matsubara).")

# Edge under the log-clock (agentS): t = e^{H tau} maps t^{-3/2} to e^{-(3/2) H tau}.
H_eff, tau = sp.symbols('H_eff tau', positive=True)
edge_logclock = sp.exp(-sp.Rational(3,2)*H_eff*tau)
print(f"    Edge under log-clock t=e^(H tau): t^(-3/2) -> {edge_logclock}")
print(f"      => a SINGLE rate, offset 3/2 INDEPENDENT of Delta (agentS R2-fail).")
print(f"      => NOT a lowest-weight module on Delta; the offset is the WRONG (fixed)")
print(f"         weight, not the discrete-series weight Delta+n. Discrete series with")
print(f"         lowest weight Delta has offset Delta; edge has offset 3/2 for ALL Delta.")

# The crux: is offset-3/2-for-all-Delta FORBIDDEN, or an allowed different rep?
# A genuine SL(2,R) rep with the GH (KMS, finite-T, discrete) structure MUST have
# its tower built on the probe's conformal weight Delta (the Casimir Delta(Delta-1)).
# An observable whose late-time tower is Delta-INDEPENDENT is NOT a discrete-series
# module of the probe at all => it carries NO lowest-weight Delta => it is OUTSIDE
# the discrete-series family that the GH modular flow is realized on.
print("\n    VERDICT of the weight test:")
print("    - CENTER: weight = discrete-series lowest weight Delta; tower Delta+n;")
print("      L_0-diagonal; KMS-covariant. IN the GH modular rep. [ALLOWED + NATURAL]")
print("    - EDGE: homogeneous weight -3/2, Delta-INDEPENDENT offset, branch-cut")
print("      (continuous) spectrum. NOT a discrete-series module on Delta.")
print("      => It does NOT lie in the discrete-series carrier space the GH modular")
print("         flow is realized on. It is a CONTINUOUS-series object.")

# ---------------------------------------------------------------------------
# (C) Now the SS-discipline call: FORBIDDEN or merely DIFFERENT?
# SL(2,R) has BOTH discrete AND continuous (principal) series. They are BOTH
# legitimate unitary reps. The GH modular flow is realized on the DISCRETE series
# (that is a banked FACT about the GH state, SS). So:
#   - If we DEMAND the observable live in the GH modular rep (discrete series), the
#     edge (continuous series) is EXCLUDED => FORCING (relative to that demand).
#   - But "live in the discrete series" = "be the GH thermal state" = the SAME
#     physical premise as Part 2(C). The continuous-series object is a perfectly
#     good SL(2,R) rep; it is excluded ONLY by the demand that it be the GH KMS
#     state, not by SL(2,R) representation theory per se.
# => The modular structure FORBIDS the edge FROM BEING the GH state, but does not
#    forbid the edge as an SL(2,R) object. The exclusion is conditional on the
#    physical identification "dS vacuum = GH KMS state", exactly as Part 2(C).
# ---------------------------------------------------------------------------
print("\n(C) SS-discipline call (FORBIDDEN vs DIFFERENT):")
print("    SL(2,R) has BOTH discrete and continuous series; both are unitary reps.")
print("    GH modular flow is realized on the DISCRETE series (banked SS fact).")
print("    - Edge (continuous-series, weight -3/2) is EXCLUDED FROM the GH discrete-")
print("      series rep => modular covariance EXCLUDES the edge AS the GH state.")
print("    - But the edge is a legitimate SL(2,R) rep in its own right; it is")
print("      excluded ONLY by demanding it be the GH KMS state (the discrete series).")
print("    => Same conditional structure as Part 2: modular covariance FORCES center")
print("       MODULO the physical premise 'dS vacuum = GH boost-KMS state'.")
print("       The premise is the load-bearing input. Status of the premise => Part 4.")
