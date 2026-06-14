import sympy as sp
# =====================================================================
# VERIFY (c) — the CENTRAL mission. EVEN granting both = R, does Connes
# genuinely REDUCE phi to a checkable state-matching, or does the surviving
# EDGE sector / observer dressing / relative-commutant freedom (agentTT)
# block the state match the same way phi was blocked before?
#
# The route's claim: Connes-Stormer => phi exists iff the two modular flows
# sigma^{chord-vac} and sigma^{GH-boost} are CONJUGATE in Aut(R), and that
# is "strictly easier" than constructing phi.
#
# HOSTILE TEST: is the residual genuinely a SINGLE checkable conjugacy
# problem, or does it inherit ALL of agentTT/agentUU's open structure?
# =====================================================================

print("=== C1: what Connes-Stormer ACTUALLY says (get the theorem right) ===")
print("""
 The route cites: 'two faithful normal states w1,w2 on R are aut-conjugate
 iff their modular flows sigma^{w1}~sigma^{w2} are conjugate in Aut(R)'.
 CHECK the direction/strength:
  - For a II_1 FACTOR, the canonical TRACE tau is the unique tracial state,
    and its modular flow is TRIVIAL (sigma^tau_t = id).
  - A faithful normal state w with NONtrivial modular flow is NOT the trace.
  - Connes-Stormer (1976, 'Homogeneity of the state space of factors of
    type III_1'): the state space of R (a II_1 / finite factor) is NOT
    homogeneous in the same way as III_1. The cited 'conjugate iff modular
    flows conjugate' is the correct invariant-theoretic statement, BUT the
    conjugacy must hold AS FLOWS ON R (an outer/cocycle conjugacy), which
    requires matching the FULL Connes invariant of the flow, not just one
    number.
""")

print("=== C2: the residual is NOT a single number -- it is GAP A + GAP B, ===")
print("===     i.e. the FULL modular spectrum + the generator. Quantify. ===")
# UU established: at fixed beta=2pi, the central-moment ratio R=4j3/j2^2 ranges
# 11..147 over a one-param Lorentzian KMS family. So beta alone (one number)
# does NOT pin the flow. Reproduce the spread to confirm the conjugacy is
# multi-parameter, i.e. NOT a 1-number check.
import numpy as np
def moment_ratio(width):
    # Lorentzian spectral density at beta=2pi: rho(E) ~ width/((E)^2+width^2),
    # KMS-thermal occupation; central moments j2, j3 of the modular Hamiltonian.
    E = np.linspace(-50,50,400001)
    beta=2*np.pi
    rho = (width/np.pi)/(E**2+width**2)
    w = rho*np.exp(-beta*E/2)        # KMS-symmetrized weight
    w/=np.trapz(w,E)
    m1=np.trapz(E*w,E); m2=np.trapz((E-m1)**2*w,E); m3=np.trapz((E-m1)**3*w,E)
    return 4*m3/m2**2 if m2>0 else np.nan
print("  R=4j3/j2^2 over KMS-consistent Lorentzian widths at FIXED beta=2pi:")
for wdt in [0.3,1.0,3.0,8.0,20.0]:
    print(f"    width={wdt:5.1f}: R = {moment_ratio(wdt): .3f}")
print("  => at fixed beta the ratio SLIDES (a surviving line-shape knob). The")
print("     conjugacy requires matching the WHOLE spectral measure, not beta alone.")
print("     => residual is GAP B (full weights) + GAP A (generator), NOT 1 number.\n")

print("=== C3 (DECISIVE): does agentTT's surviving EDGE sector BLOCK the match? ===")
print("""
 agentTT (banked, CENTER-FAVORED-STRENGTHENED, NOT forced): the chord algebra
 admits a WRITABLE, ADMISSIBLE edge GNS sector in the SAME Hilbert space,
 distinct from the center/GH sector. The center vacuum's modular flow is the
 q-deformed boost (-> could match sigma^{GH-boost}); the EDGE vacuum's modular
 flow carries a DIFFERENT weight (the t^{-3/2}/continuous-series branch).

 IMPLICATION for Connes-Stormer matching:
  - Connes-Stormer gives an aut psi with psi_*(w_chord)=w_GH IFF the chosen
    chord state w_chord has modular flow conjugate to the GH boost.
  - The CENTER chord vacuum is the candidate that MIGHT match (GAP A asks
    exactly whether its generator = the boost; UNPROVEN, agentR GATE-UNMOVED).
  - The EDGE chord vacuum provably does NOT match (wrong modular weight,
    agentTT verified) -- so for the edge state, NO state-matching iso exists.
  => Connes-Stormer does NOT by itself select the center over the edge. The
     STATE on the DSSYK side is NOT pinned by the abstract iso; it is an extra
     choice. WHICH chord cyclic vector to feed into Connes-Stormer is EXACTLY
     agentTT's open placement question. So the 'state-matching' residual still
     CONTAINS the placement gap -- it did not get easier on that axis.
""")

print("=== C4: the relative-commutant / observer-dressing freedom (agentTT) ===")
print("""
 agentTT residual (1): the boost is INNER/diagonal on the placement label
 (sigma_t|E_v> = e^{iE_v t}|E_v>), so theta_v is a modular-INVARIANT the boost
 CANNOT rotate. Translated into Connes-Stormer language: the modular flow does
 not move between the center and edge cyclic vectors; they are in DIFFERENT
 unitary/cocycle classes. So the conjugacy question is NOT 'auto-solved by the
 hugeness of Aut(R)' -- the relevant states sit in inequivalent modular classes,
 and Aut(R) acting transitively on the FACTOR does NOT act transitively on these
 physically-distinguished STATES with their fixed modular data.
""")

print("VERDICT (c): the reduction is REAL but PARTIAL and its residual is NOT")
print("a single checkable number. Connes removes the 'do non-isomorphic factors")
print("obstruct?' horn (genuine, IF both=R). But the residual state-matching")
print("(i) still requires matching the FULL modular spectrum (GAP B, multi-param,")
print("not pinned by beta), AND (ii) still contains the center-vs-edge PLACEMENT")
print("choice (GAP A, agentTT/agentR GATE-UNMOVED) -- the abstract iso does NOT")
print("select which chord state to match. So state-matching is NOT 'strictly")
print("easier' on the load-bearing axis (placement); it is the SAME open problem")
print("agentUU/agentTT named, re-expressed as a flow-conjugacy. The existence horn")
print("is cheaper; the dictionary is exactly as open as before.")
