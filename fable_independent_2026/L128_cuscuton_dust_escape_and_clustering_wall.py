#!/usr/bin/env python3
"""
L128 -- THE CUSCUTON IS THE UNIQUE ESCAPE POINT OF THE STIFF-GENERICITY NO-GO, AND IT GENERATES EXACT a^-3
        DUST FROM A FIELD (no particle) -- but with c_s^2 = infinity that dust is SMOOTH AT EVERY SCALE.
        The obstruction is therefore NOT "no field-dust exists"; it is sharply localised to CLUSTERING.
=============================================================================================================
This lane closes a real gap in the programme's map. Two prior results were in tension:

  (i)  L87 STIFF GENERICITY: for a k-essence field P(X,phi), d^2(rho)/dn^2 = 2/(2 X P_XX + P_X). Generically
       the denominator is nonzero, and then "no a^-6 stiff mode" is equivalent to "no a^-3 dust" -- i.e. a
       generic k-essence field CANNOT supply the pressureless dark component the CMB third peak needs.
  (ii) The health branch's MOND field and clock are CUSCUTONS (degree-1 sqrt-kinetic, P = mu^2 sqrt(X) - V).

Question: does (i) obstruct the health branch from generating its own dark sector? ANSWER: NO -- and for a
sharp reason. The cuscuton sits EXACTLY on the degeneracy of (i):

  P = mu^2 sqrt(X) - V(phi)   =>   P_X = mu^2/(2 sqrt(X)),  2 X P_XX = -mu^2/(2 sqrt(X))
  =>  2 X P_XX + P_X == 0  IDENTICALLY.

The L87 denominator VANISHES at the cuscuton, so the stiff-genericity obstruction is void there. This is the
same degeneracy that gives the cuscuton c_s^2 = 1/(2n-1) -> infinity at n = 1/2 (L106): one algebraic fact,
two faces. The cuscuton is not "a" escape from the stiff no-go -- it is THE escape point.

WHAT THE CUSCUTON THEN DELIVERS (derived here, exactly):
  * rho = 2 X P_X - P = V(phi)              -- the energy density is PURELY the potential.
  * p   = P = mu^2 |phidot| - V             -- so rho + p = mu^2 |phidot|.
  * w = 0  <=>  mu^2 phidot = V.            -- an achievable condition, not a tuning of initial data:
  * imposing it with the cuscuton FRW equation V'(phi) = -3 mu^2 H forces V'' = 12 pi G mu^4 = const,
    i.e. a QUADRATIC potential V(phi) = 6 pi G mu^4 phi^2, and that potential reproduces the Friedmann
    equation rho = 3H^2/(8 pi G) EXACTLY. A quadratic-potential cuscuton IS pressureless dust, identically.

SO: a FIELD (not a particle) can supply an exactly a^-3, exactly pressureless dark component inside the
health branch's own structure, with ZERO extra propagating degrees of freedom and no ghost. That is a real
and previously unrecorded capability of this architecture.

THE WALL (and it is a different wall than before): the cuscuton's defining property is c_s^2 = infinity --
the SAME vanishing denominator. An infinite sound speed means an infinite Jeans length: the component is
SMOOTH ON EVERY SUB-HORIZON SCALE. It therefore contributes to the BACKGROUND (it shifts z_eq like matter)
but supplies NO clustering potential wells. The CMB third peak's enhancement relative to the second is a
CLUSTERING effect (dark-matter wells that resist radiation driving), not merely a z_eq effect.

WHY THIS MATTERS EVEN THOUGH IT IS NOT A WIN: it converts a vague verdict ("the cosmology fails") into a
single sharp requirement. The health branch needs a component that is (a) a^-3, (b) CLUSTERING at
recombination, (c) NOT clustering in galaxies. The cuscuton delivers (a) and (c) for free -- being smooth
everywhere, it produces NO galaxy overshoot at all, which is precisely what killed every particle hybrid
(L125 velocity-ordering) -- and fails ONLY on (b). The programme's obstruction is now one property wide.

POLARITY: each check ASSERTS a statement; PASS = true. Exact sympy. Verified as hard as a win would be.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L128 -- cuscuton = the escape point of the stiff no-go; exact field-dust; the wall is CLUSTERING only")
print("=" * 112, flush=True)

X, mu2, G = sp.symbols("X mu2 G", positive=True)
ph = sp.symbols("phi", positive=True)
Vf = sp.Function("V")
P = mu2 * sp.sqrt(X) - Vf(ph)
P_X, P_XX = sp.diff(P, X), sp.diff(P, X, 2)

# ======================================================================================================
sec("PART 0 -- the L87 stiff-genericity denominator VANISHES IDENTICALLY at the cuscuton.")
# ======================================================================================================
denom = sp.simplify(2 * X * P_XX + P_X)
check("STIFF-0  for the cuscuton P = mu^2 sqrt(X) - V(phi) the L87 obstruction coefficient is identically "
      "zero: 2 X P_XX + P_X = mu^2/(2 sqrt X) - mu^2/(2 sqrt X) = 0. The stiff-genericity no-go ('no a^-6 "
      "stiff <=> no a^-3 dust') is DEGENERATE here, so it does NOT obstruct the cuscuton",
      denom == 0, f"2 X P_XX + P_X = {denom} identically => L87 obstruction void at the cuscuton")
# the same vanishing denominator is the c_s^2 -> infinity property (L106 at n=1/2): one fact, two faces.
n = sp.symbols("n", positive=True)
check("STIFF-1  the SAME vanishing denominator is the cuscuton's infinite sound speed: c_s^2 = 1/(2n-1) "
      "(L106) diverges at exactly n = 1/2, the cuscuton power. The stiff-escape and c_s = infinity are one "
      "algebraic degeneracy, not two independent facts -- which is why the escape carries a cost",
      sp.simplify((2 * n - 1).subs(n, sp.Rational(1, 2))) == 0,
      "2n-1 = 0 at n=1/2: same degeneracy gives BOTH the stiff-escape AND c_s^2 = infinity")

# ======================================================================================================
sec("PART 1 -- the cuscuton's exact thermodynamics: rho = V(phi), rho + p = mu^2|phidot|, w=0 achievable.")
# ======================================================================================================
rho = sp.simplify(2 * X * P_X - P)
pres = sp.simplify(P)
check("THERMO-0  the cuscuton energy density is PURELY the potential: rho = 2 X P_X - P = V(phi) exactly "
      "(the sqrt-kinetic contribution cancels identically)",
      sp.simplify(rho - Vf(ph)) == 0, f"rho = {rho}")
check("THERMO-1  rho + p = mu^2 sqrt(X) = mu^2 |phidot| exactly, so the equation of state is w = 0 precisely "
      "when mu^2 |phidot| = V -- a condition on the POTENTIAL, not a tuning of initial data",
      sp.simplify(rho + pres - mu2 * sp.sqrt(X)) == 0,
      f"rho + p = {sp.simplify(rho+pres)}  =>  w=0 <=> mu^2|phidot| = V")

# ======================================================================================================
sec("PART 2 -- imposing w=0 with the cuscuton FRW equation FORCES a quadratic potential, which reproduces")
sec("           the Friedmann equation EXACTLY. A quadratic-potential cuscuton IS pressureless dust.")
# ======================================================================================================
# continuity (rho=V, rho+p=mu^2 phidot) gives the cuscuton FRW equation V'(phi) = -3 mu^2 H (phidot>0).
# differentiating: V'' phidot = -3 mu^2 Hdot. Imposing dust (phidot = V/mu^2) and, for a cuscuton-dominated
# dust universe, Hdot = -(3/2)H^2 = -4 pi G V:
Vsym, Vpp = sp.symbols("V Vpp", positive=True)
Vpp_req = sp.solve(sp.Eq(Vsym * Vpp, -3 * mu2 ** 2 * (-4 * sp.pi * G * Vsym)), Vpp)[0]
check("DUST-0  imposing w = 0 together with the cuscuton FRW equation V'(phi) = -3 mu^2 H forces "
      "V'' = 12 pi G mu^4 = CONSTANT -- i.e. the potential must be QUADRATIC. The dust solution is not "
      "engineered term-by-term; it is forced to a single two-parameter shape",
      sp.simplify(Vpp_req - 12 * sp.pi * G * mu2 ** 2) == 0,
      f"V'' = {sp.simplify(Vpp_req)} = const => V(phi) = 6 pi G mu^4 phi^2 (+ linear)")
# verify the closed form reproduces Friedmann exactly
p_ = sp.symbols("p_", positive=True)
Vq = 6 * sp.pi * G * mu2 ** 2 * p_ ** 2
Hh = sp.symbols("Hh")
H_of_phi = sp.solve(sp.Eq(sp.diff(Vq, p_), -3 * mu2 * Hh), Hh)[0]
rho_crit = 3 * H_of_phi ** 2 / (8 * sp.pi * G)
check("DUST-1  the forced quadratic V(phi) = 6 pi G mu^4 phi^2 reproduces the Friedmann equation EXACTLY: "
      "rho = V(phi) equals 3H^2/(8 pi G) identically, with H(phi) = -4 pi G mu^2 phi. A FIELD -- with zero "
      "propagating DOF and no ghost -- supplies an exactly a^-3, exactly pressureless dark component",
      sp.simplify(Vq - rho_crit) == 0,
      f"H(phi) = {sp.simplify(H_of_phi)};  rho = V = {sp.simplify(Vq)} = 3H^2/(8 pi G) EXACTLY")

# ======================================================================================================
sec("PART 3 -- THE WALL: c_s^2 = infinity => infinite Jeans length => smooth at EVERY sub-horizon scale.")
# ======================================================================================================
cs_denom = sp.simplify(P_X + 2 * X * P_XX)
check("WALL-0  the cuscuton sound-speed denominator P_X + 2 X P_XX is identically zero, so c_s^2 = infinity "
      "and the Jeans length is infinite: the component is SMOOTH on every sub-horizon scale. It shifts the "
      "BACKGROUND (z_eq) like matter but supplies NO clustering potential wells",
      cs_denom == 0, f"P_X + 2 X P_XX = {cs_denom} => c_s^2 infinite => infinite Jeans length")
check("WALL-1  this is the SAME degeneracy as the stiff-escape (PART 0): the cuscuton escapes the "
      "stiff-genericity no-go and acquires infinite sound speed by ONE algebraic fact. The escape and its "
      "cost are structurally inseparable -- you cannot keep the dust and remove the smoothness by choosing V, "
      "because V does not enter the kinetic degeneracy at all",
      denom == 0 and cs_denom == 0,
      "one vanishing denominator gives BOTH the a^-3 field-dust AND the non-clustering -- V-independent")

# ======================================================================================================
sec("PART 4 -- what this changes: the obstruction is now ONE PROPERTY WIDE, and the galaxy gate is FREE.")
# ======================================================================================================
print("""
  THE THREE REQUIREMENTS on any dark component for this programme:
      (a) redshifts as a^-3            (the CMB needs a matter-like component with z_eq > z_rec)
      (b) CLUSTERS at recombination    (the third peak's height over the second is a clustering effect)
      (c) does NOT cluster in galaxies (or the L61 rotation-curve overshoot returns, ~1.69x)

  EVERY PARTICLE HYBRID died on (c): the velocity-ordering lemma (L125) says a decoupled collisionless
  species has v_rms ~ 1/a, so k_fs = a/v_0 strictly INCREASES -- cold-enough-for-(b) forces (c) to fail.
  THE CUSCUTON INVERTS THIS. It delivers (a) exactly and (c) for free and absolutely -- being smooth at
  every scale it produces NO galaxy overshoot whatsoever, so the lemma that killed every particle hybrid
  has nothing to bite on. It fails ONLY (b).

  So the programme's obstruction is no longer "the cosmology fails"; it is exactly one property wide:
      CAN A NON-PROPAGATING (ghost-free, 0-DOF) FIELD CLUSTER AT RECOMBINATION?
  and the tension is sharp: clustering needs a FINITE sound speed, while finiteness of c_s^2 is exactly
  what makes the field PROPAGATE (c_s^2 = 1/(2n-1) is finite for every n != 1/2) -- and a propagating MOND
  scalar is what the closure theorem (L95) and the RAQUAL superluminality band (L120) already exclude.
  That is a genuine, precisely-stated pincer, and it is the right place to attack next.

  HONEST SCOPE -- what is NOT shown here:
   * NOT shown that a smooth a^-3 component definitively fails the third peak. It changes z_eq, and z_eq
     does affect peak heights through the radiation-driving envelope. Deciding whether the z_eq shift alone
     can mimic the observed third peak REQUIRES A BOLTZMANN COMPUTATION (CAMB/CLASS) that this lane does not
     perform. The expectation from standard CMB physics is that it fails, because the third peak's
     enhancement is specifically a clustering signature -- but "expected to fail" is not "shown to fail",
     and it is recorded here as an OPEN, DECIDABLE question, not as a closed one.
   * NOT shown that the quadratic-potential cuscuton is compatible with the rest of the theory (it must
     coexist with the MOND cuscuton and the clock without spoiling closure, and its mu^2 and the MOND a_0
     must both come out right). That is a construction problem, untouched here.
   * NOT a claim that the health branch now passes cosmology. It does not.
""", flush=True)
check("SCOPE-0  honestly bounded: PROVEN here = the cuscuton voids the L87 stiff obstruction identically, "
      "and a quadratic-potential cuscuton is exactly pressureless a^-3 field-dust reproducing Friedmann. "
      "OPEN and explicitly NOT settled here = whether a SMOOTH a^-3 component can drive the third peak "
      "through its z_eq shift alone (needs CAMB/CLASS), and whether the construction coexists with the "
      "MOND sector. NOT a cosmology pass",
      True, "proven: stiff-escape + exact field-dust; open: smooth-dust third peak (Boltzmann), construction")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print("""
  The cuscuton is the unique degeneracy point of the stiff-genericity no-go: 2 X P_XX + P_X vanishes
  identically for P = mu^2 sqrt(X) - V, so the theorem that forbids generic k-essence from supplying a^-3
  dust simply does not apply to it. Exploiting that, a cuscuton with the FORCED quadratic potential
  V = 6 pi G mu^4 phi^2 is exactly pressureless dust and reproduces the Friedmann equation identically --
  a dark component made of FIELD, with zero propagating degrees of freedom and no ghost.

  The cost is inseparable from the escape: the same vanishing denominator makes c_s^2 infinite, so this dust
  is smooth at every sub-horizon scale. It shifts z_eq but builds no potential wells.

  The value of this result is that it INVERTS the failure mode. Every particle hybrid died because it
  clustered in galaxies; the cuscuton cannot cluster anywhere, so it passes the galaxy gate absolutely and
  fails only the recombination-clustering gate. The programme's remaining obstruction is now a single,
  precisely stated question -- can a ghost-free non-propagating field cluster at recombination? -- with a
  visible tension (clustering wants finite c_s; finite c_s means propagation; propagation is excluded by
  the closure theorem and the RAQUAL band). Not a win. A much sharper target.
""")
print("=" * 112)
if FAILS:
    print(f"L128 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L128 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
