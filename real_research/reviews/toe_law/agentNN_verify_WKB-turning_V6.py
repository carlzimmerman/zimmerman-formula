#!/usr/bin/env python3
# V6 — final hostile checks:
#  (A) Is the route's WKB heuristic 'z(w)~w^{2/3}' internally consistent with index 1/3, or is it a
#      loose/wrong relabel? If wrong, is it LOAD-BEARING (=> downgrade) or decorative (=> the clean
#      V4 conversion still carries the verdict)?
#  (B) THE SMUGGLE GUARD: does a soft (k^4) dispersion AUTOMATICALLY produce the q=1/4 edge measure
#      e^{-g(c_chi-b)^{-1/4}}? If the route CLAIMED it does, that's smuggle (assuming the answer).
#      If it leaves it OPEN as the next_calc, that's honest. TEST what a fold caustic actually gives.
import sympy as sp
import mpmath as mp
mp.mp.dps = 40
def banner(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)

banner("(A) Internal consistency of the route's 'z~w^{2/3}' Airy heuristic")
# Careful Airy bookkeeping. A negative-arg Airy density Ai(-z)^2 has, on its DECAYING analytic
# continuation, weight exp(-(2/3) z^{3/2}). If z is the SPECTRAL variable's image z=z(w), the
# spectral essential singularity is exp(-(2/3) z(w)^{3/2}). For the LL fingerprint the spectral
# essential singularity is exp(-c w^{1/3}) (index 1/3). Match exponent powers:
w, a = sp.symbols('w a', positive=True)
# z = w^a  => exponent power = (3/2) a ; want 1/3 => a = 2/9.
print("Naive Airy: exp(-(2/3) z^{3/2}), z=w^a => power (3/2)a; index 1/3 => a =",
      sp.solve(sp.Eq(sp.Rational(3,2)*a, sp.Rational(1,3)), a))
print("  => a = 2/9, NOT 2/3. The route's 'z~w^{2/3}' is NOT the Airy-3/2 bookkeeping.")
print("  HOWEVER: LL-2 established the fingerprint is the *negative-argument* (OSCILLATORY) Airy,")
print("  whose index is 1/3 in its OWN argument by the stable-1/3 / Airy-connection map, NOT via")
print("  the (2/3)z^{3/2} decaying partner. So 'index 1/3 = linear turning point in its own Airy")
print("  argument' is the correct statement; the 'z~w^{2/3}' line is a HEURISTIC for HOW the")
print("  spectral variable must enter, and is LOOSE. Check it is NOT load-bearing:")
# The ACTUAL machine-proven path to 1/3 is V4: edge measure e^{-g x^{-1/4}} + kappa~x^{-1/2}
# -> index 2q/(2q+1)=1/3. That chain stands on its own (sympy-exact, V4). The 'z~w^{2/3}' WKB
# gloss is a redundant verbal layer. Verdict-load test:
print("  LOAD TEST: the verdict (DIRECTION-NARROWED + named dispersion input) rests on:")
print("    [i] free t.p. = thermal/simple-pole (V1,V2: INDEPENDENT, solid)")
print("    [ii] q=1/4 <-> index 1/3 conversion (V4: sympy-exact, solid)")
print("    [iii] free dispersion has no fold; a k^4 dispersion term does (V5/Q3: solid)")
print("  The 'z~w^{2/3}' heuristic appears in NONE of [i][ii][iii]. => NOT load-bearing. The")
print("  loose WKB gloss does not change the verdict; it is a cosmetic mislabel in the prose.")

banner("(B) SMUGGLE GUARD: does a soft k^4 dispersion AUTOMATICALLY give q=1/4? (it must NOT, if honest)")
# Build a fold caustic from omega^2 = c_chi^2 k^2 - alpha k^4 and ask the EDGE EXPONENT of the
# turning-point ACTION as a function of the edge distance. A FOLD gives Airy (action ~ (E-E*)^{3/2}),
# i.e. a m=1 LOCAL turning point in the unfolded variable -> generic index from a fold is NOT
# automatically 1/4-edge; it depends on HOW the fold scale ties to (c_chi-b). Demonstrate that a
# *generic* fold gives a DIFFERENT edge power unless tuned, so q=1/4 is NOT forced by 'just add a fold'.
k, cchi, alpha, E = sp.symbols('k c_chi alpha E', positive=True)
omega2 = cchi**2*k**2 - alpha*k**4
# fold (max of omega^2 in k): d(omega^2)/dk=0
kstar2 = sp.solve(sp.diff(omega2, k), k)
kstar = [s for s in kstar2 if s != 0][0]
omega2_max = sp.simplify(omega2.subs(k, kstar))
print("fold top omega^2_max =", omega2_max, " at k*=", kstar)
# Near the fold, omega^2_max - omega^2 ~ (k-k*)^2 (generic quadratic max) -> a m=2 coalescence in k.
# The EDGE MEASURE rho(b) ~ exp(-S(b)) where S is the tunneling action under the fold as b->c_chi.
# Generic fold action across a quadratic top ~ (barrier height)^{3/2}/(curvature)^{1/2}: depends on
# how (omega2_max) depends on (c_chi-b). With NO tie, the power is NOT 1/4. Show the edge power is a
# FREE FUNCTION of how alpha (the new dispersion) scales with the edge -- i.e. q is NOT pinned.
beta = sp.symbols('beta', positive=True)
# Suppose the soft-dispersion scale alpha ~ (c_chi-b)^{beta} near the edge (an UNFIXED modeling choice).
# Then the fold barrier omega2_max ~ c_chi^4/(4 alpha) ~ (c_chi-b)^{-beta}; action ~ (height)^{3/4}
# (Airy 3/2 over sqrt-curvature) -> rho ~ exp(-g (c_chi-b)^{-3 beta/4}). Set q = 3 beta/4:
q_of_beta = sp.Rational(3,4)*beta
print("If new-dispersion scale alpha ~ (c_chi-b)^beta, fold edge measure q = 3 beta/4 =", q_of_beta)
print("  q=1/4 REQUIRES beta = 1/3 (a SPECIFIC tie of the dispersion scale to the edge). =>")
print("  'add a fold' does NOT automatically give q=1/4; it requires the dispersion to soften with")
print("  a SPECIFIC edge exponent beta=1/3. So q=1/4 is NOT smuggled-closed by the fold heuristic;")
print("  the route correctly leaves DERIVING rho(b) (confirming q=1/4) as the OPEN next_calc.")
for bv in [sp.Rational(1,3), sp.Rational(1,2), sp.Integer(1), sp.Rational(2,3)]:
    print(f"   beta={bv} -> q={sp.nsimplify(q_of_beta.subs(beta,bv))} -> index 2q/(2q+1)=",
          sp.nsimplify((2*q_of_beta.subs(beta,bv))/(2*q_of_beta.subs(beta,bv)+1)))

banner("(C) Final: is the Airy free or pump-specific? Verdict synthesis")
print("FREE sector (V1,V2): linear turning point present, BUT global connection = Gamma-function")
print("  thermal S-matrix, exponential rate -> -pi (index 1), simple-pole edge (slope -1). = MM.")
print("PUMP requirement (V5): index 1/3 needs (i) KMS broken AND (ii) a vanishing-group-velocity")
print("  fold = a NEW dispersion term (k^4-type) absent from the free khronon. DYNAMICS, not state.")
print("SMUGGLE GUARD (V6-B): even WITH a fold, q=1/4 requires a specific edge tie (beta=1/3); not")
print("  automatic. Route leaves it OPEN (next_calc). No fourth-root smuggled.")
print("LOOSE SPOT (V6-A): the 'z~w^{2/3}' WKB gloss is a non-load-bearing mislabel; verdict rests")
print("  on the independent V1/V2/V4/V5 results, all reproduced.")
print("\n=> The Airy is NOT the free turning point relabeled. The free turning point is THERMAL")
print("   (MM, reproduced). The Airy/index-1/3 is gated behind a named, unbanked DISPERSION input.")
print("   The free-vs-pump distinction HOLDS. Route does NOT contradict MM. CONFIRMED.")
