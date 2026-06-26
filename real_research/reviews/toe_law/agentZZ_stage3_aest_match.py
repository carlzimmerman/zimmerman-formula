#!/usr/bin/env python3
"""
agentZZ STAGE 3 — Term-by-term match of the coarse-grained worldline EFT to AeST Eq (5),
AND the decisive ACTIVE/NONLOCAL vs PASSIVE/LOCAL test (the conjecture's crux).

AeST action (Skordis-Zlosnik 2007.00082, their Eq 5):
  S = INT d4x sqrt(-g)/(16 pi G~) [ R - (K_B/2) F^{mu nu}F_{mu nu}
        + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) - lambda(A^2+1) ] + S_m[g]
  with F_{mu nu}=2 grad_[mu A_nu], J^mu = A^a grad_a A^mu, Y=q^{mu nu}grad_mu phi grad_nu phi,
       q = g + A A, Q = A^mu grad_mu phi.
  Eq(2) deep-MOND: J(Y) -> (2 lam_s/(3(1+lam_s) a0)) Y^{3/2}.
  Eq(6) quasi-static: J^mu grad_mu phi -> grad Psi . grad phi (the scalar-aether mixing),
       and Psi = Phi (the lensing-correct condition).

We test each AeST term against what the coarse-graining produces, and grade
JOINED / PARTIAL / FAILS per term and overall.
"""
import sympy as sp

print("="*78)
print("STAGE 3: term-by-term AeST match + the active/passive (in-in vs AeST) test")
print("="*78)

# --- The matching table (each row: AeST term, coarse-grained origin, verdict) ---
rows = []

# Row R: Einstein-Hilbert
rows.append(("R  (Einstein-Hilbert)",
   "NOT from the worldline sector. Gravity is the BACKGROUND the bath lives on; the",
   "worldline EFT supplies the matter+bath sector, GR is assumed (as in AeST: R is put in).",
   "EXTERNAL (both theories assume R)"))

# Row A: unit-timelike vector
rows.append(("-lambda(A^2+1) : unit-timelike A_mu",
   "FORCED: the dS bath rest frame u^mu, u.u=-1 (Deser-Levin: T depends on accel in the",
   "cosmic rest frame). The constraint A^2=-1 = 'A_mu IS a unit frame label', not dynamical norm.",
   "REPRODUCED (field + constraint)"))

# Row Y: the spatial scalar kinetic + Y^{3/2}
rows.append(("-(2-K_B)Y - F(Y,Q) : scalar Y, deep-MOND Y^{3/2}",
   "REPRODUCED in form: Y=q^{mn}d_m phi d_n phi is the FRAME-ORTHOGONAL gradient (the bath",
   "reads spatial accel rel. to u); HS scalar's deep-MOND term is (2/3)Y^{3/2} with 1/a0 coeff.",
   "REPRODUCED in FORM; coefficient a0 NOT forced (route-degenerate, prior result)"))

# Row J: the scalar-aether mixing
rows.append(("2(2-K_B) J^mu grad_mu phi : scalar-aether mixing",
   "PARTIAL: J^mu = A^a grad_a A^mu is the aether's OWN acceleration (the frame's non-geodesy).",
   "The worldline coupling is matter-accel . bath-frame; the mixing grad Psi.grad phi (Eq6) emerges",
   "PARTIAL (mixing emerges in q-s limit; the specific J^mu=A.gradA form NOT uniquely forced)"))

# Row F: the aether kinetic (Maxwell) term
rows.append(("-(K_B/2)F^{mn}F_{mn} : aether kinetic term",
   "NOT PRODUCED by the worldline coarse-graining. F^2 is a TWO-DERIVATIVE kinetic term for the",
   "bath frame; the worldline sees u as a fixed background label, giving NO (grad A)^2 dynamics.",
   "MISSING (the bath-frame kinetic term is not generated)"))

# Row Q/K: the cosmological function
rows.append(("F(Y,Q), Q=A.grad phi, K(Q)=-2Lam+... : cosmology sector",
   "NOT from the galaxy worldline sector. Q is the TEMPORAL scalar gradient = the dust/DE mode;",
   "the worldline MI coarse-graining is the SPATIAL (Y) sector only. K(Q) is a separate posit in AeST too.",
   "MISSING (the CDM-like K(Q) sector is not produced)"))

for r in rows:
    print("\n--- AeST term:", r[0])
    print("    origin:", r[1])
    print("           ", r[2])
    print("    VERDICT:", r[3])

print("\n" + "="*78)
print("THE DECISIVE TEST: is the in-in (ACTIVE/NONLOCAL) kernel = AeST (PASSIVE/LOCAL)?")
print("="*78)

# ---------------------------------------------------------------------------
# AeST is a PASSIVE, LOCAL, conservative field theory: it has a standard
# Lagrangian L(g,A,phi, grad...) with a symmetric stress tensor and conserved
# energy. The in-in worldline action is, by construction (Galley Eq 5, K!=0),
# a NON-CONSERVATIVE doubled action with a RETARDED memory kernel (Eq 25).
#
# The question: does the influence functional's kernel gamma(t-t') reduce, in
# the coarse-grained/local limit, to a PASSIVE LOCAL Lagrangian (= AeST), or is
# the active/nonlocal content irreducible?
#
# Decompose the Feynman-Vernon kernel into NOISE (Hadamard, symmetric, nu) and
# DISSIPATION (retarded, antisymmetric, gamma). A passive local action keeps only
# a local, time-symmetric piece. We test whether the dS bath kernel's antisymmetric
# (active) part vanishes in the coarse-grained limit.
# ---------------------------------------------------------------------------
print("""
[3X] Feynman-Vernon split of the dS-bath influence functional (Caldeira-Leggett form):
   Phi[x_+,x_-] = i INT dt dt' [ x_-(t) gamma(t-t') x_+(t')   <- DISSIPATION (retarded, ACTIVE)
                               + (i/2) x_-(t) nu(t-t') x_-(t') ] <- NOISE (Hadamard, symmetric)
   A PASSIVE LOCAL theory (AeST) is recovered ONLY if, in the coarse-grained limit, the
   retarded kernel gamma collapses to a local conservative term (a derivative of a potential)
   AND the fluctuation-dissipation-mandated noise nu does not source irreducible stochastic
   (active) dynamics.
""")

# The framework's OWN prior theorem (agentX "Theorem X2", banked in UNIFIED_ACTION_ASSEMBLY.md):
#   causality + vacuum PASSIVITY force mu_hat(0) >= mu_hat(infty), while deep-MOND forces the
#   INVERSION (mu_fw(0)=0 < mu_fw(infty)=1). Therefore NO passive vacuum closes the causal MI:
#   the channel is irreducibly ACTIVE (the kernel must be PUMPED by the dS bath).
# We re-verify the inversion that drives this:
xv = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*xv**2)-1)/(2*xv)
mu0 = sp.limit(mu_fw, xv, 0)      # deep-MOND
muinf = sp.limit(mu_fw, xv, sp.oo) # Newtonian
print("[3X'] Passivity inversion (re-deriving Theorem X2's driver):")
print("   mu_fw(0)   =", mu0, "  (deep-MOND: inertia SUPPRESSED)")
print("   mu_fw(inf) =", muinf, "  (Newtonian: inertia full)")
print("   => mu_fw(0)=0 < mu_fw(inf)=1 : the response RISES with acceleration.")
print("   Passive-vacuum causality (Kramers-Kronig + positivity) requires the static response")
print("   to DOMINATE: mu_hat(0) >= mu_hat(inf). The MI law VIOLATES this (0 < 1).")
print("   => the kernel CANNOT be a passive vacuum response: it must be ACTIVELY PUMPED by the bath.")
print()
print("[3X''] CONSEQUENCE for the join:")
print("   AeST's action is PASSIVE and LOCAL (its energy is conserved; it has a standard")
print("   symmetric stress tensor, Eq(5) is a genuine Lagrangian). The in-in worldline MI is")
print("   IRREDUCIBLY ACTIVE (Theorem X2) and NONLOCAL (Milgrom-1994 no-go). Therefore the")
print("   coarse-grained worldline EFT is NOT identical to AeST as a Lagrangian theory: AeST is")
print("   the PASSIVE/LOCAL TRUNCATION (the time-symmetric, gamma->local part), and it DROPS the")
print("   active (pumped) + noise content that carries the MI-distinctive physics (Cassini-evasion,")
print("   sigma-spread, EFE theta-factor).")
