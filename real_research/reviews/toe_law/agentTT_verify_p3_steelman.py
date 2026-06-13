"""
agentTT VERIFY — Part 3: STEELMAN the route (both-ways rule). Where is the route
GENUINELY right, and exactly where does FORCING fail? Avoid manufacturing an
overturn as hard as avoiding rubber-stamping a forcing.

Carl's working rule: verify a 'fails/not-forced' claim as rigorously as a 'works'
claim. So before concluding 'not forcing', I must check my OWN p2 attacks survive
the route's best rebuttals. Three steelman checks:

  (S1) Is my p2(A) [continuous series is generic for dS scalars] a CATEGORY ERROR?
       The route's object is the STATIC-PATCH boost-KMS structure, whose modular
       Hamiltonian L_0 has a DISCRETE real spectrum (the QNM ladder). The global
       SO(d,1) Bunch-Davies decomposition (principal/complementary series) is a
       DIFFERENT decomposition. Does the static-patch L_0 spectrum being discrete
       rescue 'GH flow = discrete series' and thus re-forbid the edge?

  (S2) The route's STRONGEST claim: the edge is at beta=inf (T=0), and dS is ALWAYS
       at finite T_dS>0, so the edge is excluded from the ENTIRE finite-T line --
       NOT an SS-style slide to another finite value. Test whether this is a genuine
       EXCLUSION (forcing) or whether 'the probe sits at the band edge' is itself a
       legitimate finite-T configuration whose ONE-SIDEDNESS is the kinematic edge
       artifact of p2(C), leaving the edge as a valid (if non-GH) dS observable.

  (S3) The DECISIVE arbiter for FORCING vs CONSISTENCY (per the brief): is there a
       SURVIVING admissible edge sector? Concretely -- does the edge placement
       correspond to a real, physically admissible state in the DSSYK Hilbert space
       (so it CAN be written down, just isn't the GH state), or is it algebraically
       FORBIDDEN (cannot be written down at all)? agentR is the arbiter: the chord
       algebra supplies BOTH center and edge states. Confirm the edge state EXISTS.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
print("="*78)
print("VERIFY PART 3 — STEELMAN the route; locate exactly where forcing fails")
print("="*78)

# ===========================================================================
# (S1) static-patch L_0 discrete spectrum vs global SO(d,1) continuous series.
# The route is RIGHT that the static-patch modular Hamiltonian L_0 (=boost) has a
# DISCRETE spectrum on the GH GNS space -- the QNM ladder {Delta+n}. This is the
# resolvent/QNM (resonance) spectrum, not the global L^2 spectrum. So 'the modular
# flow's GNS carrier is a lowest-weight discrete tower' is a DEFENSIBLE reading for
# the RELAXATION (QNM) content. My p2(A) point (global=continuous) does NOT directly
# refute this; it refutes the BLANKET claim 'continuous-series is forbidden for dS'.
# HONEST CONCESSION: for the QNM/relaxation content specifically, the center's
# discrete ladder IS the natural L_0 module, and the edge's NON-ladder (power law)
# genuinely is NOT that module. So the route's CONSISTENCY/favoring is real here.
# But: is it FORCING? Only if NO admissible dS relaxation can be a continuous
# (branch-cut) spectrum. Counterexample test: a HEAVY (principal-series) dS scalar's
# static-patch 2pt has a CONTINUOUS (principal-series) contribution AND its QNMs ring
# (Re!=0). Conversely, the edge's branch cut is a continuous spectrum that is purely
# damped. Is 'purely-damped continuous (branch-cut) relaxation' forbidden in dS?
# ===========================================================================
print("\n(S1) static-patch L_0 (discrete QNM ladder) vs continuous spectrum:")
print("    CONCEDE: the static-patch modular Hamiltonian L_0 has the DISCRETE QNM")
print("    ladder {Delta+n} as its resonance spectrum; the center IS its lowest-weight")
print("    module; the edge's power-law (branch cut) is NOT that module. The route's")
print("    CONSISTENCY/favoring of the center for the RELAXATION content is REAL.")
print("    BUT the FORCING question: is a purely-damped CONTINUOUS (branch-cut)")
print("    relaxation FORBIDDEN for a dS static patch? A branch cut = a CONTINUUM of")
print("    damped modes. dS static-patch correlators of HEAVY fields DO carry")
print("    continuous (principal-series) spectral weight. So a continuous spectral")
print("    contribution is NOT forbidden in dS; it is the edge's PURELY-DAMPED +")
print("    ONE-SIDED character (not its continuity) that the route flags. And one-")
print("    sidedness is the band-edge kinematic artifact (p2C), not a rep-theoretic")
print("    ban. => still CONSISTENCY (edge is non-GH), not FORCING (edge forbidden).")

# ===========================================================================
# (S2) is beta=inf a genuine EXCLUSION from the finite-T line, or a kinematic edge?
# The route: edge=T=0, dS always finite-T, so edge excluded from the WHOLE finite-T
# line (stronger than SS). Test: the 'temperature' the route reads off the edge is
# the SPECTRAL ASYMMETRY A (A=1/2<=>beta=2pi; A=0<=>beta=inf). But p2(C) showed A is
# a CONTINUOUS function of placement E_v: A(E_v) slides 1/2 -> 0 smoothly. So the
# 'inverse temperature' beta_eff(E_v) implied by A is ALSO continuous and DIVERGES
# only in the strict edge LIMIT E_v->-1. Compute beta_eff(A) and show:
#   - it is a CONTINUOUS family (every interior placement has a FINITE beta_eff),
#   - so the placements DO form a continuous one-parameter family of 'temperatures',
#   - and the edge is the beta->inf ENDPOINT of that family.
# This is the SS slide structure AFTER ALL: a continuous family of effective temps,
# with the edge at the boundary. The route's 'binary discrete/continuous SERIES' is
# the q->1 idealization; at finite lambda the placements interpolate continuously.
# ===========================================================================
print("\n(S2) is the edge a genuine exclusion, or the endpoint of a CONTINUOUS family?")
A = sp.symbols('A', positive=True)
# A = 1/(1+e^{beta*omega0}) style two-level detailed-balance proxy:
#   define A = (absorption)/(emission+absorption) = e^{-beta w}/(1+e^{-beta w})
# then beta = (1/w) ln((1-A)/A). Map the placement-A to an effective beta.
betaw = sp.symbols('betaw', real=True)
A_of_beta = sp.exp(-betaw)/(1+sp.exp(-betaw))    # in [0,1/2] for betaw>=0
beta_of_A = sp.solve(sp.Eq(A_of_beta, A), betaw)[0]
print(f"    detailed-balance two-level proxy: A = e^(-beta w)/(1+e^(-beta w))")
print(f"    => beta*w = {sp.simplify(beta_of_A)} (= ln((1-A)/A))")
for a_ in [sp.Rational(1,2), sp.Rational(1,4), sp.Rational(1,20), sp.Rational(1,2000)]:
    bw = sp.log((1-a_)/a_)
    print(f"      A={float(a_):.4f} -> beta*w = {float(bw):.4f}  "
          f"({'center, finite' if a_==sp.Rational(1,2) else 'interior, FINITE' if a_>sp.Rational(1,100) else 'edge limit, DIVERGES'})")
print(f"    => beta_eff(A) is a CONTINUOUS family; interior placements have FINITE")
print(f"       beta_eff; the edge (A->0) is the beta->inf ENDPOINT. So the placement")
print(f"       family IS a continuous one-parameter line of effective temperatures,")
print(f"       with the edge at its boundary -- STRUCTURALLY the SS slide, NOT a")
print(f"       discrete exclusion. The route's H3 refutation ('edge is the degenerate")
print(f"       boundary point no dS occupies') is TRUE but it does NOT FORBID the edge:")
print(f"       it says the edge is the NON-GH endpoint, i.e. CONSISTENCY/favoring.")
print(f"    HOWEVER, in fairness: A=1/2 (center) is the UNIQUE value matching the FIXED")
print(f"       T_dS=H/2pi, and it sits at the SYMMETRIC point, not tuned -- so the")
print(f"       center is genuinely SPECIAL (favored), even though the edge is not banned.")

# ===========================================================================
# (S3) DECISIVE arbiter: does the edge state EXIST (writable) or is it FORBIDDEN?
# Per the brief: 'Any surviving edge sector => CENTER-FAVORED-STRENGTHENED at best,
# not FORCED.' agentR (banked): the chord algebra supplies BOTH a natural center
# state (N-hat vacuum/infinite-T) AND natural edge states (H-extremal). Both are
# admissible vectors in the SAME chord Hilbert space. Confirm the edge is an
# EXISTING, writable state (not algebraically forbidden), which is exactly a
# SURVIVING admissible sector => not FORCED.
# ===========================================================================
print("\n(S3) DECISIVE: does the edge state EXIST (=> surviving sector => not FORCED)?")
print("    agentR (banked, CONTESTED-TERMINAL): the chord algebra supplies BOTH")
print("    a natural CENTER state (N-hat vacuum / infinite-T, theta=pi/2) AND natural")
print("    EDGE states (H-extremal, theta->pi). BOTH are admissible vectors in the")
print("    SAME chord Hilbert space. The edge is NOT algebraically forbidden -- it is")
print("    a writable cyclic vector defining a perfectly good GNS state (its OWN")
print("    modular flow, at beta=inf / its own structure).")
print("    => There IS a surviving admissible edge sector. By the brief's own")
print("       criterion ('Any surviving edge sector => not FORCED'), the verdict")
print("       CANNOT be CENTER-FORCED. The modular structure FAVORS the center")
print("       (the edge fails to be the GH boost-KMS state), but does NOT EXCLUDE the")
print("       edge from existing. FORCING(edge excluded) is FALSE; CONSISTENCY/")
print("       FAVORING(center fits uniquely, edge is non-GH but writable) is TRUE.")

print("\n" + "="*78)
print("STEELMAN NET:")
print(" - The route is GENUINELY RIGHT that (i) only the center is boost-fixed +")
print("   two-sided + the discrete L_0 module, and (ii) the GH premise is a THEOREM")
print("   at FIXED T_dS, not an SS open knob. So the FAVORING is real and STRONGER")
print("   than a mere coincidence -- agentS's edge-wound is genuinely DEEPENED.")
print(" - But FORCING (edge EXCLUDED) is NOT established: (A) continuous-series is not")
print("   forbidden in dS; (B) Re=0 is not a discrete-series selector; (C) the edge's")
print("   one-sidedness is a CONTINUOUS band-edge artifact (beta_eff slides, S2); (D)")
print("   the boost does not act on theta_v (route concedes); (S3) the edge state")
print("   EXISTS (agentR) = a surviving admissible sector.")
print(" => REGRADE: CONFIRMED at CENTER-FAVORED-STRENGTHENED. The route's own verdict")
print("    word is already CENTER-FAVORED-STRENGTHENED (NOT center-forced), so the")
print("    route did NOT overclaim a forcing. The modular argument is a CONSISTENCY/")
print("    FAVORING (theorem-backed, state-level), not a FORCING. agentR's 'terminal")
print("    at the algebra' stands; nothing new is DERIVED at the algebra level.")
print("="*78)
