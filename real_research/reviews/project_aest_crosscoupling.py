#!/usr/bin/env python3
"""
DOOR 3 worked to the term: can a non-separable AeST free function F(Y,Q) FORCE a0 = c^2 sqrt(Lambda/32pi)?
=========================================================================================================
The Zimmerman framework welds the MOND scale to the cosmological constant: a0 = c^2 sqrt(Lambda/32pi)
(Z^2 = 32pi/3). AeST (Skordis-Zlosnik, PRL 127, 161302 (2021); arXiv:2007.00082) is the leading covariant
MOND theory -- fits the CMB acoustic peaks, has c_GW=c (survives GW170817), and reproduces deep-MOND via the
Y^{3/2} term of a free function F(Y,Q). ALREADY VERIFIED in this repo (clean_slate_field_theory.py,
bridge1_aest_equations.md, project02_aest_K_of_Q.py):
   (i)   a0 genuinely lives in F's Y^{3/2} coefficient (incl. the factor-3 normalization);
   (ii)  an evolving a0 is CMB-safe at linear order (Ybar=0 on FRW -> the MOND term is O(delta phi^3));
   (iii) CRUCIALLY, a0 (in the Y-sector) and Lambda (the -2 Lambda floor in the Q-sector K(Q)) enter AeST
         as TWO INDEPENDENT inputs.

THE TASK (Door 3, the buildable home): try to CONSTRUCT a non-separable F(Y,Q) -- coupling the kinetic/shift
invariant Y to the cosmological invariant Q -- whose small-Y coefficient is FORCED to equal sqrt(Lambda) with
the 1/sqrt(32pi) factor, so that a0 = c^2 sqrt(Lambda/32pi) EMERGES rather than being a free input. Then ask
the only question that matters: can the welding be FORCED by a symmetry / consistency principle (shift
symmetry, scale invariance, c_GW=c, ghost-freedom), or can it only be INSERTED by hand (a tuned coefficient)?

THE HONEST VERDICT (computed below, not hoped for): **INSERTED.** A non-separable F(Y,Q) that produces
a0 = c^2 sqrt(Lambda/32pi) is easy to WRITE, and there is even a Lambda-free-looking form. But:
   * the form whose coupling is a pure number requires the cross term to carry an INVERSE power (-K(Q))^{-1/2},
     which goes imaginary / singular where K(Q) crosses zero on the cosmological background -> killed by
     ghost-freedom / hyperbolicity;
   * the ghost-safe form (positive power sqrt(-K(Q))) leaves the coupling carrying 1/Lambda -> a TUNED constant;
   * none of shift symmetry / scale invariance / c_GW=c SELECTS the welding exponent (each is shown below to be
     silent, hostile, or off-sector);
   * and the same Door-3c/3d locality obstruction reappears: the welded coefficient is evaluated at the LOCAL Q
     inside a galaxy, which is not pinned to the cosmological Q0.
So the welding a0 ~ sqrt(Lambda) is a CHOICE of free function inserted by hand, exactly as it is in every other
covariant MOND theory. No symmetry forces it. This is the expected, acceptable, honest answer.

Needs sympy + numpy.  Run:  python real_research/reviews/project_aest_crosscoupling.py

----------------------------------------------------------------------------------------------------------------------
CROSS-REFERENCE (resolved 2026-06-09): Part 4's locality worry above -- "the welded coefficient is evaluated at the
LOCAL Q inside a galaxy, not pinned to the cosmological Q0 -> environment-dependent a0" -- is RESOLVED (against this
worry, in favor of project_aest_locality_check.py) by aest_locality_theta_profile.py. Under the static-aether theorem
(Eling & Jacobson 2006, gr-qc/0603058) a virialized galaxy forces the unit aether purely timelike (A^i = 0), so
Q = phibar-dot / sqrt(1+2Phi) ~ Q0 to ~1e-6; the cross term v*dphi' that makes Q look environment-dependent in Part 4
VANISHES for the correct static aether (Part 4 implicitly used a non-static A^i != 0 aether). Contingent on staticity;
only merging/collapsing (dPhi/dt != 0) systems get a transient ~few-% wobble. NOTE: this resolves only the Q-LOCALITY
sub-point; this file's MAIN verdict (the a0 ~ sqrt(Lambda) welding is INSERTED, not symmetry-forced) is unaffected.
"""
import sympy as sp
import numpy as np

# ----------------------------------------------------------------------------------------------------
# physical constants (only used for the closing numeric sanity check)
c = 2.99792458e8
G = 6.674e-11
Mpc = 3.0857e22
H0 = 67.4e3 / Mpc
OmL = 0.685
Z = 2 * np.sqrt(8 * np.pi / 3)        # the framework's coefficient, 5.78881...


def part0_action():
    print("=" * 100)
    print("PART 0 -- the AeST action and where the two debts (a0, Lambda) live")
    print("=" * 100)
    print(r"""  Skordis-Zlosnik 2021, Eq. (5) (schematic, geometric units; transcribed in bridge1_aest_equations.md):

      S = INT d^4x sqrt(-g)/(16 pi Gtilde) [ R - (K_B/2) F^{mu nu}F_{mu nu}
                                             + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y
                                             - F(Y, Q) - lambda(A^mu A_mu + 1) ]  +  S_m[g]

    fields:   metric g_{mu nu};  unit-timelike aether A^mu (A.A=-1 enforced by lambda);  scalar phi.
    F_{mu nu} = 2 grad_[mu A_nu]  (vector kinetic; its coeff K_B is what keeps c_GW=c).
    invariants of the free function F:
        Y = q^{mu nu} grad_mu phi grad_nu phi,   q^{mu nu} = g^{mu nu} + A^mu A^nu   (SPATIAL projector)
        Q = A^mu grad_mu phi                                                          (TEMPORAL part)

  WHERE THE TWO INPUTS SIT (verified previously):
    * a0  lives in the SMALL-Y limit of F:   F(Y,Q) -> [2 lambda_s / (3(1+lambda_s) a0)] Y^{3/2}  as Y->0.
          (The Y^{3/2} power is the deep-MOND sqrt-law; a0 is its coefficient.  The exact O(1) -- the 3 and
           lambda_s -- is the published normalization and does NOT affect the welding argument; it only
           rescales the constant C below.)
    * Lambda lives in the Q-sector:          K(Q) := F(0,Q) = -2 Lambda + (1/2) K2 (Q - Q0)^2 + ...
          The constant floor -K(Q0) = 2 Lambda is the cosmological-constant sector; the (Q-Q0)^2 piece
          (coeff K2) builds the CDM-like 'dust' mode that fits the CMB peaks.

  THE POINT: in a SEPARABLE F = K(Q) + J(Y), the Y^{3/2} coefficient (a0) and K(Q0) (Lambda) are
  ALGEBRAICALLY UNRELATED -- two independent dials. The framework's a0 = c^2 sqrt(Lambda/32pi) asks us to
  TIE them with one specific coefficient.  Door 3 is: can a NON-SEPARABLE F force that tie?
""")


def part1_candidate():
    print("=" * 100)
    print("PART 1 -- the candidate non-separable F(Y,Q): weld the Y^{3/2} coefficient to the K(Q) floor")
    print("=" * 100)
    Y, Q, Q0, Lam, K2, b, C, p, lam_s = sp.symbols(
        'Y Q Q0 Lambda K2 beta C p lambda_s', positive=True)

    # cosmological (Q) sector: the standard AeST shift-symmetric k-essence with a Lambda floor
    K = -2 * Lam + sp.Rational(1, 2) * K2 * (Q - Q0)**2
    floor = sp.simplify(-K.subs(Q, Q0))            # = 2 Lambda  (the "Q-sector vacuum energy")

    print(f"  Cosmological sector:   K(Q) = F(0,Q) = {K}")
    print(f"  Its floor (Q=Q0):     -K(Q0) = {floor}   == 2 Lambda  (the cosmological-constant sector).\n")

    print("  GENERAL non-separable ansatz (the most natural weld -- multiply the MOND term by a power of")
    print("  the SAME object that carries Lambda, so the two cannot be dialed independently):")
    print("       F(Y,Q) = K(Q)  +  C * (-K(Q))^p * Y^{3/2}  +  (higher Y) ...")
    print("  At the cosmological background Q=Q0, the Y^{3/2} coefficient becomes  C * (2 Lambda)^p.")
    print("  We DEMAND this equal the deep-MOND coefficient with a0 welded to Lambda:\n")

    # target coefficient: [2 lam_s/(3(1+lam_s) a0)] with a0 = sqrt(Lambda/32pi)  (geometric c=1)
    a0_geo = sp.sqrt(Lam / (32 * sp.pi))
    target = (2 * lam_s / (3 * (1 + lam_s))) / a0_geo
    target = sp.simplify(target)
    print(f"     a0 (geometric, c=1) = sqrt(Lambda/32pi);  target Y^{{3/2}} coeff = {target}")
    print(f"        (note: target ~ Lambda^(-1/2) -- it RISES as Lambda falls, since a0 ~ sqrt(Lambda).)\n")

    # match power-of-Lambda: C*(2 Lambda)^p == const * Lambda^{-1/2}  for ALL Lambda
    print("  MATCHING as functions of Lambda (this is the crux):  C*(2 Lambda)^p = const * Lambda^(-1/2).")
    print("  Two inequivalent ways to satisfy it:\n")

    # ---- Route 1: p = +1/2 (ghost-safe power) -> C must carry 1/Lambda (TUNED) ----
    beta_sol = sp.solve(sp.Eq(b * sp.sqrt(floor), target), b)[0]
    print("  ROUTE 1  (p = +1/2, the ghost-SAFE positive power):  F = K + beta*sqrt(-K(Q))*Y^{3/2}.")
    print(f"     coeff at Q0 = beta*sqrt(2 Lambda) = target  =>  beta = {sp.simplify(beta_sol)}")
    print("     ==> beta STILL CONTAINS 1/Lambda. The coupling is NOT a pure number; to make a0=sqrt(Lambda/32pi)")
    print("         come out, beta must be tuned proportional to 1/Lambda. This is INSERTION, transparently.\n")

    # ---- Route 2: p = -1/2 (makes C a pure number) -> inverse power of K(Q) (GHOST/singular) ----
    p_val = sp.Rational(-1, 2)
    C_sol = sp.solve(sp.Eq(C * (2 * Lam)**p_val, target), C)[0]
    print("  ROUTE 2  (p = -1/2, the ONLY power that makes the coupling Lambda-free):")
    print(f"     F = K + C*(-K(Q))^(-1/2)*Y^{{3/2}},   C = {sp.simplify(C_sol)}  <-- a PURE NUMBER (no Lambda).")
    chk = sp.simplify(C_sol * (2 * Lam)**p_val - target)
    print(f"     check: coeff(Q0) - target = {chk}  (0 => the weld a0=sqrt(Lambda/32pi) is exact at Q0).")
    print("     ==> SUPERFICIALLY this looks 'forced': a dimensionless C, and a0 ~ sqrt(Lambda) falls out for")
    print("         ANY value of Lambda. BUT it pays a fatal price (Part 3): the cross term now carries an")
    print("         INVERSE power of K(Q), 1/sqrt(-K(Q)), which is singular/imaginary where K(Q) crosses zero.\n")
    return dict(Y=Y, Q=Q, Q0=Q0, Lam=Lam, K2=K2, p_val=p_val, C_sol=C_sol)


def part2_principles():
    print("=" * 100)
    print("PART 2 -- do any of the named consistency PRINCIPLES select the welding? (shift / scale / c_GW)")
    print("=" * 100)
    print("""  The weld is the choice of the exponent p (and that the cross term uses K(Q) at all). For the welding
  to be FORCED rather than inserted, some principle must SELECT p = -1/2 (Route 2). Test each:

  (A) SHIFT SYMMETRY  phi -> phi + const.
      Y = q^{mu nu} grad_mu phi grad_nu phi and Q = A^mu grad_mu phi are BOTH built only from grad phi, so
      BOTH are shift-invariant. Therefore EVERY F(Y,Q) is automatically shift-symmetric -- including the
      separable one. Shift symmetry is the reason F depends on (Y,Q) at all, but it places NO constraint on
      the power p or on whether F is separable. => shift symmetry does NOT force the weld.

  (B) SCALE / DILATION INVARIANCE  (phi -> s phi, x -> x/s).
      Under phi -> s phi:  Y -> s^2 Y (so Y^{3/2} -> s^3 Y^{3/2}),  Q -> s Q.  A scale-invariant action needs
      a single homogeneous weight -- but K(Q) = -2 Lambda + (1/2)K2 (Q-Q0)^2 contains a CONSTANT floor
      (-2 Lambda, weight 0) and Q0 != 0, both of which carry the dimensionful scale Lambda and EXPLICITLY
      break dilation symmetry. Demanding scale invariance would FORBID the Lambda floor outright (Lambda IS a
      scale), which is the opposite of welding a0 to it. => scale invariance cannot force a0 ~ sqrt(Lambda);
      it would delete Lambda.

  (C) c_GW = c   (GW170817).
      In AeST the graviton speed is fixed by the TENSOR sector: the vector kinetic coefficient K_B and any
      disformal (grad phi)-graviton couplings. The free function F(Y,Q) is a SCALAR potential of (Y,Q); in
      minimal AeST it does not multiply the graviton kinetic term, so it does not shift c_GW at all. c_GW=c
      constrains K_B and the disformal terms -- NOT the (Y,Q) power structure of F. => c_GW=c is satisfied for
      ANY F(Y,Q); it neither forces nor forbids the weld. (It is an off-sector constraint here.)

  NET: none of shift symmetry, scale invariance, or c_GW=c selects p = -1/2 (or even non-separability).
       Only ghost-freedom / hyperbolicity actually bites on F(Y,Q) -- Part 3 -- and it OPPOSES the weld.
""")


def part3_ghost(sym):
    print("=" * 100)
    print("PART 3 -- ghost-freedom / hyperbolicity: the one principle that bites -- and it KILLS Route 2")
    print("=" * 100)
    Lam, K2 = sym['Lam'], sym['K2']
    Q, Q0 = sym['Q'], sym['Q0']
    I0, a = sp.symbols('I0 a', positive=True)

    print("""  Ghost-freedom requires the Hessian of F w.r.t. field derivatives to have the right signs (F_Y > 0 and
  a convexity condition on F_{YY} in the deep-MOND range); hyperbolicity requires REAL characteristic speeds.
  The Route-2 cross term  C*(-K(Q))^(-1/2)*Y^{3/2}  carries 1/sqrt(-K(Q)). On the cosmological background the
  AeST scalar EOM integrates to dK/dQ ~ I0/a^3, i.e. Q - Q0 ~ I0/a^3 (bridge1_aest_equations.md). So along
  the background K(Q) sweeps:
""")
    mK = 2 * Lam - sp.Rational(1, 2) * K2 * (I0 / a**3)**2     # = -K(Q(a))
    print(f"     -K(Q(a)) = 2 Lambda - (1/2) K2 (I0/a^3)^2 = {mK}")
    a_cross = sp.solve(sp.Eq(mK, 0), a)
    a_cross = [sp.simplify(s) for s in a_cross]
    # pick the positive real root expression
    print(f"     This CROSSES ZERO at a = {a_cross[0]}  (and its sign partner).")
    print("""     For a < a_cross (early times, higher z), -K(Q) < 0, so (-K)^(-1/2) is IMAGINARY and DIVERGES at
     the crossing. The welded MOND coefficient becomes complex; F_{YY} loses the correct sign --> a GHOST /
     loss of hyperbolicity in the scalar sector at a FINITE redshift. The 'Lambda-free, forced-looking'
     Route 2 is therefore admissible only on a restricted patch -K(Q) > 0, NOT on the full cosmological
     history. Ghost-freedom forbids exactly the form that made the coupling dimensionless.

  AND Route 1 (p=+1/2, ghost-safe sqrt(-K)) leaves beta ~ 1/Lambda -- a tuned constant (Part 1). So the
  ghost-free branch is the INSERTED branch, and the pure-number branch is the GHOSTLY branch. There is no
  branch that is BOTH ghost-free AND has a pure-number (forced) coupling.
""")


def part4_locality():
    print("=" * 100)
    print("PART 4 -- the residual structural obstruction (same as Door 3c/3d): WHERE is K(Q) evaluated?")
    print("=" * 100)
    print("""  Even GRANTING a non-separable F whose Y^{3/2} coefficient is a function of K(Q), there is a locality
  problem that the framework's other doors already exposed:

    * a0 is read off in the QUASI-STATIC GALAXY limit, where Y = |grad phi|^2 != 0.
    * In that same limit the welded coefficient is (-K(Q_local))^p, with Q_local = A^mu grad_mu phi the LOCAL
      temporal scalar gradient.
    * For a0 to equal the cosmological c^2 sqrt(Lambda/32pi), we need K(Q_local) = K(Q0) = -2 Lambda INSIDE the
      galaxy -- i.e. Q_local pinned to the cosmological value Q0.
    * But Q_local is set by the LOCAL scalar configuration, not pinned to Q0. So the welded a0 becomes
      ENVIRONMENT-DEPENDENT (varies with the local Q), contradicting the tight, universal RAR -- UNLESS K(Q)
      is essentially flat near its minimum (K2 -> 0). And K2 is precisely the curvature that builds the
      CDM-like dust mode for the CMB. So 'universal a0' and 'CMB dust mode' pull against each other.

  This is the SAME obstruction found in project03c/03d (theta -> 0 in galaxies; no LOCAL covariant scalar
  reproduces the uniform COSMIC a0). Welding a0 to the Q-sector does not escape it; it inherits it. The only
  fully clean reading remains the CONSTANT-a0 (event-horizon / bare-Lambda) one -- where Lambda is a true
  constant, uniform by definition -- which is exactly the reading that needs NO weld inside F at all.
""")


def part5_numeric():
    print("=" * 100)
    print("PART 5 -- numeric sanity (the weld is real arithmetic; only its FORCING is the open question)")
    print("=" * 100)
    Lambda = 3 * OmL * H0**2 / c**2                 # Lambda = 3 Omega_L H0^2 / c^2  [1/m^2]
    a0_pred = c**2 * np.sqrt(Lambda / (32 * np.pi))
    ratio = Lambda * c**4 / a0_pred**2
    print(f"  Lambda = 3 Omega_L H0^2 / c^2          = {Lambda:.3e} m^-2")
    print(f"  a0 = c^2 sqrt(Lambda/32pi)             = {a0_pred:.3e} m/s^2   (framework ~9.4e-11; obs ~1.2e-10)")
    print(f"  dimensionless weld  32pi = Lambda c^4/a0^2 = {ratio:.3f}   vs  32pi = {32*np.pi:.3f}  (exact by constr.)")
    print(f"  (for reference Z = 2 sqrt(8pi/3) = {Z:.5f}, Z^2 = 32pi/3 = {Z**2:.4f})")
    print("""
  The arithmetic closes perfectly -- that was never in doubt. The deliverable's question is whether the
  COEFFICIENT in the F(Y,Q) free function is FORCED to put it there, and the answer (Parts 1-4) is no.
""")


def verdict():
    print("#" * 100)
    print("# VERDICT -- Door 3 (AeST cross-coupling), reported straight")
    print("#" * 100)
    print("""
  CANDIDATE F(Y,Q):   F(Y,Q) = K(Q) + C * (-K(Q))^p * Y^{3/2} + ... ,
                      K(Q) = -2 Lambda + (1/2) K2 (Q-Q0)^2,   floor -K(Q0) = 2 Lambda,
                      Y^{3/2} coefficient at Q0 = C (2 Lambda)^p, demanded = [2 lam_s/(3(1+lam_s))]/a0
                      with a0 = c^2 sqrt(Lambda/32pi).

  WHAT EACH CONSISTENCY CONDITION REQUIRES OF F:
    - shift symmetry      : automatically satisfied by ANY F(Y,Q) (Y,Q both ~ grad phi). Selects nothing.
    - scale invariance    : would FORBID the -2 Lambda floor (Lambda is a scale). Hostile to the weld.
    - c_GW = c            : constrains the TENSOR sector (K_B, disformal terms), not F(Y,Q)'s (Y,Q) powers.
                            Off-sector; satisfied for any F(Y,Q).
    - ghost-free/hyperbolic: the ONLY condition that bites. Forces F_Y>0 and the right F_{YY} sign. It KILLS
                            the only Lambda-free ('forced-looking') form -- the p=-1/2 cross term 1/sqrt(-K(Q))
                            goes imaginary/singular where K(Q) crosses zero on the background (finite z).
    - (locality / RAR)    : the welded coeff is evaluated at the LOCAL Q in a galaxy, not pinned to Q0 -> a0
                            becomes environment-dependent unless K2->0 (which would kill the CMB dust mode).
                            Same Door-3c/3d obstruction.

  ONE-WORD VERDICT:  **INSERTED.**

  REASON (one paragraph): A non-separable F(Y,Q) whose small-Y coefficient reproduces a0 = c^2 sqrt(Lambda/32pi)
  is trivial to WRITE, but the welding is a free choice, not a consequence. There are exactly two ways to make
  the Y^{3/2} coefficient track Lambda: a ghost-SAFE positive power sqrt(-K(Q)), whose coupling beta is then
  forced to carry 1/Lambda (a hand-tuned, dimensionful constant -- manifest insertion); or the UNIQUE negative
  power (-K(Q))^{-1/2} that makes the coupling a pure number, which is destroyed by ghost-freedom/hyperbolicity
  because 1/sqrt(-K(Q)) goes imaginary and singular where K(Q) crosses zero on the cosmological background at
  finite redshift. None of the principles that could have forced the choice does so: shift symmetry is silent
  (every F(Y,Q) has it), scale invariance is hostile (it forbids the Lambda floor it would have to relate),
  and c_GW=c lives in the tensor sector and never sees the (Y,Q) powers. On top of that, the same locality
  obstruction from Doors 3c/3d returns -- the welded coefficient is read at the LOCAL Q inside galaxies, not at
  the cosmological Q0. So the a0 ~ sqrt(Lambda) marriage in AeST can only be put into the free function by hand,
  exactly as it is in every covariant MOND theory in the zoo. The number 32pi is GR-traceable (Friedmann 3 x
  Einstein 8pi / surface-gravity 4), but AeST's own consistency conditions do not FORCE it into F. Verdict:
  INSERTED, not FORCED -- and (unlike the DSSYK route, Door 6) not BLOCKED: the welded theory is a perfectly
  good, CMB-safe, GW170817-safe member of the AeST family; it is simply one choice of free function among many,
  with no principle singling it out.
""")
    print("#" * 100)


def main():
    print("#" * 100)
    print("# project_aest_crosscoupling.py -- can a non-separable AeST F(Y,Q) FORCE a0 = c^2 sqrt(Lambda/32pi)?")
    print("#" * 100 + "\n")
    part0_action()
    sym = part1_candidate()
    part2_principles()
    part3_ghost(sym)
    part4_locality()
    part5_numeric()
    verdict()


if __name__ == "__main__":
    main()
