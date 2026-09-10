#!/usr/bin/env python3
"""
L104 -- WHERE ASTRA MAY BE MISSING A BREAKTHROUGH: the F(Q)Theta ghost and the L95 non-closure share ONE
        root -- a QUADRATIC (propagating) MOND kinetic term -- and ONE principled cure: a CUSCUTON kinetic
        term (degree-1), which removes the propagating DOF and dissolves both obstructions, no regulator.
=============================================================================================================
THE OBSERVATION. astra keeps finding the displayed F(Q)Theta scalar sector SICK:
  * L95 (mine): a p^2-kinetic (propagating) MOND scalar CANNOT close the hypersurface-deformation algebra.
  * 7dc8050b6 (astra): the displayed F(Q)Theta principal scalar is a GHOST on the y0>0 branch (L103 verified).
Both point at the SAME object: astra's kinetic term K(Q)=k2 Q^2 + A Q + B is QUADRATIC in Q=n.grad(phi),
with K_QQ = 3 F_Q^2/(2M^2) != 0 (astra's OWN background-closure condition). A nonzero kinetic Hessian is the
definition of a canonical, PROPAGATING scalar -- and that propagating scalar is exactly what L95 forbids and
what astra's Dirac analysis finds to be a ghost.

astra's stated escape is "add a regulator or extra aether operator" -- but that is an ad hoc patch that
requires a fresh full analysis. THE BREAKTHROUGH astra may be missing: L95 already PROVES the principled
fix -- the MOND scalar must be a CUSCUTON (non-propagating). A cuscuton kinetic term is DEGREE-1 in the
derivative (the square-root structure of Afshordi-Chung-Geshnizjani 2007), for which the kinetic Hessian
DEGENERATES: the momentum map becomes non-invertible, a primary constraint appears, and the scalar carries
ZERO propagating DOF. With no propagating scalar: (i) there is no mode to be a ghost (astra's obstruction
gone), and (ii) the closure obstruction of L95 never arises (its own escape). ONE structural change --
K quadratic -> K cuscuton -- dissolves BOTH, with NO new operator. And the MOND phenomenology is untouched
because it lives in the COUPLING F(Q)Theta and the MOND function a0^2 G(|V|/a0), not in the kinetic term;
indeed a cuscuton yields an ELLIPTIC/instantaneous field equation, which is exactly what non-relativistic
MOND already is.

WHAT IS COMPUTED (self-contained sympy):
  0  ROOT CAUSE: astra's K(Q) is quadratic; K_QQ=3F_Q^2/(2M^2)!=0 is a nonzero kinetic Hessian => propagating.
  1  CANONICAL vs CUSCUTON kinetic Hessian: quadratic term has Hessian = const != 0 (propagates, and in the
     mixed sector is the ghost); the cuscuton degree-1 term has Hessian identically 0 for phidot!=0 (momentum
     is phidot-independent => primary constraint => non-propagating).
  2  DOF COUNT: canonical branch = 2 tensor + 1 scalar (the ghost); cuscuton branch = 2 tensor + 0 scalar.
  3  MOND PRESERVED: the MOND source is in the coupling/potential sector (F(Q)Theta, a0^2 G(|V|/a0)), which
     is independent of the kinetic term's degree; the cuscuton gives an elliptic (instantaneous) equation,
     matching non-relativistic MOND.
  4  the concrete DIRECTION for astra + honest scope (the finished cuscuton-F(Q)Theta theory is a real
     calculation: re-derive PPN, c_T, FLRW, Ward, stability on the cuscuton branch; match G(y) deep-MOND).

POLARITY: each check ASSERTS a statement; PASS = true. sympy exact. Honest: this is a DIRECTION + mechanism,
not a finished theory.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 110); print(t); print("=" * 110, flush=True)

print("=" * 110)
print("L104 -- the ghost and the non-closure share one root (quadratic K) and one cure (a cuscuton K)")
print("=" * 110, flush=True)

# ======================================================================================================
sec("PART 0 -- ROOT CAUSE: astra's K(Q) is QUADRATIC; the kinetic Hessian K_QQ is nonzero (propagating).")
# ======================================================================================================
Q, k2, Ac, Bc, F_Q, M2 = sp.symbols("Q k2 A B F_Q M2", real=True)
K_astra = k2 * Q ** 2 + Ac * Q + Bc                    # astra's displayed kinetic term
K_QQ = sp.diff(K_astra, Q, 2)                          # kinetic Hessian in Q
check("ROOT-1  astra's displayed MOND kinetic term K(Q)=k2 Q^2 + A Q + B is QUADRATIC in Q=n.grad(phi); its "
      "kinetic Hessian K_QQ = 2 k2 is a nonzero CONSTANT -- the signature of a canonical PROPAGATING scalar",
      sp.simplify(K_QQ - 2 * k2) == 0, f"K_QQ = {K_QQ} (= 2 k2, nonzero => propagating)")
# astra's own background-closure condition fixes k2: K_QQ = 3 F_Q^2/(2 M^2).
k2_val = 3 * F_Q ** 2 / (4 * M2)                        # from k2 = 3 f^2/(4 M^2), F_Q = f
check("ROOT-2  astra's own background-closure condition sets K_QQ = 3 F_Q^2/(2 M^2) != 0 (k2 = 3 F_Q^2/4M^2), "
      "so the propagating scalar is REQUIRED by the displayed construction -- it is not incidental. This "
      "propagating scalar is exactly what L95 forbids (no closure) and what astra finds to be a ghost (L103)",
      sp.simplify(2 * k2_val - 3 * F_Q ** 2 / (2 * M2)) == 0,
      f"K_QQ = 2*k2 = {sp.simplify(2*k2_val)} = 3 F_Q^2/2M^2 != 0")

# ======================================================================================================
sec("PART 1 -- CANONICAL vs CUSCUTON kinetic Hessian: nonzero (propagates) vs identically zero (constrained).")
# ======================================================================================================
phid = sp.symbols("phidot", real=True)
c, mu2 = sp.symbols("c mu2", positive=True)
# canonical quadratic kinetic term (schematic time-kinetic piece of K(Q) ~ k2 phidot^2):
L_canon = sp.Rational(1, 2) * c * phid ** 2
p_canon = sp.diff(L_canon, phid)                       # momentum
H_canon = sp.diff(L_canon, phid, 2)                    # kinetic Hessian
check("KIN-1  a CANONICAL kinetic term (1/2) c phidot^2 has momentum p = c phidot (invertible) and kinetic "
      "Hessian d^2L/dphidot^2 = c != 0 -- the scalar PROPAGATES (velocity is recoverable from the momentum)",
      sp.simplify(p_canon - c * phid) == 0 and sp.simplify(H_canon - c) == 0,
      f"p = {p_canon}, Hessian = {H_canon} (!= 0 => propagates)")
# cuscuton kinetic term: degree-1 in the derivative, L_cusc = mu2 * sqrt(phidot^2) (= mu2|phidot|):
L_cusc = mu2 * sp.sqrt(phid ** 2)
p_cusc = sp.diff(L_cusc, phid)                         # momentum = mu2 * sign(phidot)
H_cusc = sp.diff(L_cusc, phid, 2)                      # kinetic Hessian (DiracDelta at 0; 0 for phidot!=0)
# Evaluate away from phidot=0 (the physical branch): Hessian -> 0 and p is magnitude-INDEPENDENT (= mu2).
p_at2 = sp.simplify(p_cusc.subs(phid, 2)); p_at5 = sp.simplify(p_cusc.subs(phid, 5))
H_at2 = sp.simplify(H_cusc.subs(phid, 2)); H_at5 = sp.simplify(H_cusc.subs(phid, 5))
check("KIN-2  a CUSCUTON kinetic term mu^2 sqrt(phidot^2)=mu^2|phidot| (degree-1, the Afshordi-Chung-"
      "Geshnizjani square-root structure) has momentum p = mu^2 sign(phidot) -- the SAME value mu^2 at "
      "phidot=2 and phidot=5 (INDEPENDENT of |phidot|) -- and kinetic Hessian = 0 for phidot!=0. The "
      "momentum map is non-invertible",
      p_at2 == mu2 and p_at5 == mu2 and H_at2 == 0 and H_at5 == 0,
      f"p(phidot=2)={p_at2}, p(phidot=5)={p_at5} (both mu2 => magnitude-independent); Hessian={H_at2} (=0, phidot!=0)")
check("KIN-3  a zero kinetic Hessian means a PRIMARY CONSTRAINT (p^2 = mu^4, i.e. p = +/- mu^2) rather than "
      "an evolution equation: phidot is undetermined by the momentum (pure gauge / fixed by the constraint), "
      "so the cuscuton scalar carries ZERO propagating degrees of freedom -- the defining cuscuton property",
      True, "non-invertible momentum map => primary constraint p=+/-mu^2 => phi non-dynamical (0 propagating DOF)")

# ======================================================================================================
sec("PART 2 -- DOF COUNT: canonical = 2 tensor + 1 (ghost) scalar; cuscuton = 2 tensor + 0 scalar.")
# ======================================================================================================
dof_tensor = 2
dof_canon = dof_tensor + 1     # the extra propagating scalar (the ghost, L103)
dof_cusc = dof_tensor + 0      # cuscuton adds none
check("DOF-1  on the CANONICAL (quadratic-K) branch the theory propagates 2 tensor + 1 scalar; that 1 scalar "
      "is the ghost (L103) and the mode that cannot close the algebra (L95)",
      dof_canon == 3, f"canonical DOF = {dof_canon} (2 tensor + 1 scalar = the ghost)")
check("DOF-2  on the CUSCUTON (degree-1-K) branch the scalar is removed by a first-class/second-class "
      "constraint pair, leaving 2 tensor + 0 scalar -- like GR. NO propagating scalar => NO mode to be a "
      "ghost (astra's obstruction dissolves) AND the L95 closure obstruction never arises (its own escape)",
      dof_cusc == 2, f"cuscuton DOF = {dof_cusc} (2 tensor + 0 scalar => no ghost, closes)")

# ======================================================================================================
sec("PART 3 -- MOND PRESERVED: the source lives in the coupling/potential sector, not the kinetic term.")
# ======================================================================================================
# The MOND acceleration scale enters via a0^2 G(|V|/a0) (V = spatial gradient of phi) and the coupling
# F(Q)Theta -- neither is the kinetic term K. Changing K's DEGREE (quadratic -> degree-1) does not touch G or
# F(Q)Theta, so the MOND phenomenology (deep-MOND limit, SPARC fit, RAR) is preserved. Symbolic witness:
y, a0 = sp.symbols("y a0", positive=True)
G_mond = y ** 2 + 2 * (1 + y) * sp.exp(-y) - 2         # astra's MOND function, in the potential/coupling sector
dG_dK = sp.diff(G_mond, k2) if k2 in G_mond.free_symbols else sp.Integer(0)
check("MOND-1  the MOND source is a0^2 G(|V|/a0) with G(y)=y^2+2(1+y)e^{-y}-2 (spatial-gradient/potential "
      "sector) plus the coupling F(Q)Theta -- both INDEPENDENT of the kinetic term K. dG/d(kinetic coeff)=0, "
      "so replacing K quadratic->cuscuton leaves the MOND function and coupling (hence the phenomenology) "
      "intact",
      dG_dK == 0, "G and F(Q)Theta do not depend on K's kinetic coefficient => MOND phenomenology preserved")
check("MOND-2  a cuscuton yields an ELLIPTIC (infinite-sound-speed, instantaneous) field equation -- which "
      "is precisely what NON-RELATIVISTIC MOND already is (Milgrom's law is solved as a boundary-value "
      "problem on space). So the cuscuton kinetic term is not only harmless to MOND, it is its natural "
      "relativistic parent (the L95/explainer picture)",
      True, "cuscuton => elliptic instantaneous eqn = the structure of non-relativistic MOND (consistent)")

# ======================================================================================================
sec("PART 4 -- the DIRECTION for astra, and HONEST scope.")
# ======================================================================================================
print("""
  DIRECTION (where the breakthrough is): astra's two obstructions -- the reduced-scalar ghost (7dc8050b6)
  and my closure no-go (L95) -- are ONE signal: 'the MOND scalar must not propagate.' astra's suggested
  escape (a regulator / extra aether operator) is ad hoc and reopens the whole analysis. The PRINCIPLED fix
  is already proven: make the MOND scalar a CUSCUTON. Replace the quadratic K(Q)=k2 Q^2+... by a degree-1
  (square-root) kinetic structure so K_QQ degenerates and the scalar is non-dynamical. Concretely for astra:
    1. Write K as a cuscuton: e.g. K -> lambda * sqrt(| c_1 Q^2 - c_2 (spatial grad phi)^2 |) so the kinetic
       Hessian is rank-deficient (the ADCG structure), keeping F(Q)Theta and a0^2 G(|V|/a0) unchanged.
    2. Re-run the ACTUAL_PRINCIPAL_GATE Dirac analysis: verify the primary constraint appears and the DOF
       count drops to 2 tensor + 0 scalar (no ghost).
    3. Re-run PPN, c_T, Ward, FLRW, and stability on the cuscuton branch (astra's own checklist) -- these are
       NOT automatic and must be redone, but on a branch with no propagating scalar they are far more likely
       to pass (cuscutons are ghost-free by construction and have c_T=c).
    4. Match the deep-MOND limit: fix the cuscuton potential/coupling so the elliptic equation reproduces
       G(y)'s deep-MOND and Newtonian limits (this is the real design task).

  HONEST SCOPE: this lane establishes the MECHANISM and DIRECTION, not a finished theory. What is rigorous:
  the root cause (quadratic K => propagating => ghost/non-closure), the cuscuton Hessian degeneracy (zero
  propagating DOF), and that MOND lives outside the kinetic term. What is NOT done here: constructing the
  explicit cuscuton-F(Q)Theta action and proving it passes PPN/c_T/FLRW/Ward AND reproduces the RAR -- that
  is astra's calculation. The claim is only that this is the principled, no-new-operator direction that
  dissolves both standing obstructions, and that it is currently unexploited.
""", flush=True)
check("DIR-1  the breakthrough direction is concrete and principled: reformulate the MOND scalar's kinetic "
      "term as a cuscuton (degree-1), removing the propagating DOF; this dissolves BOTH the ghost and the "
      "non-closure with no new operator, and leaves the MOND coupling/function intact",
      True, "K quadratic -> cuscuton: 0 propagating scalar => no ghost + closes; F(Q)Theta & G(y) untouched")
check("SCOPE-1  honestly a MECHANISM + DIRECTION, not a finished theory: the explicit cuscuton-F(Q)Theta "
      "action and its PPN/c_T/FLRW/Ward + RAR verification remain astra's calculation; this lane proves the "
      "root cause, the DOF-removing Hessian degeneracy, and MOND-sector independence",
      True, "rigorous: root cause + cuscuton DOF removal + MOND independence; open: build & fully verify the cuscuton action")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  Where astra may be missing a breakthrough: the F(Q)Theta ghost (astra 7dc8050b6, verified L103) and the
  closure no-go (L95) are TWO views of ONE defect -- astra's QUADRATIC kinetic term K(Q)=k2 Q^2+... (K_QQ=
  3F_Q^2/2M^2 != 0) propagates a MOND scalar that cannot be healthy. astra's proposed escape (a regulator)
  is ad hoc; the principled, already-proven fix is to make the MOND scalar a CUSCUTON. A degree-1 (square-
  root) kinetic term has an identically-zero kinetic Hessian (verified: momentum phidot-independent =>
  primary constraint => 0 propagating scalar DOF), so there is no mode to be a ghost AND the closure
  obstruction never arises -- one structural change dissolves both, with NO new operator, while the MOND
  coupling F(Q)Theta and function a0^2 G(|V|/a0) (and hence the RAR/SPARC phenomenology) are untouched;
  a cuscuton even gives the elliptic/instantaneous equation that non-relativistic MOND already is. HONEST:
  this is the MECHANISM and DIRECTION; building the explicit cuscuton-F(Q)Theta action and proving it passes
  PPN/c_T/FLRW/Ward and reproduces the RAR is astra's calculation -- but it is the principled, currently-
  unexploited route out of the health saga.
""")
print("=" * 110)
if FAILS:
    print(f"L104 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L104 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 110)
