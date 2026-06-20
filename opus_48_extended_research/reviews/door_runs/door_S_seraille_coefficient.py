#!/usr/bin/env python3
"""
DOOR S (GAP-3 coefficient) -- the Seraille a0 ~ sqrt(Lambda) coefficient cross-check.

QUESTION:  Blanchet-Seraille (arXiv:2502.14686, JCAP 12(2025)036) build an
INDEPENDENT mechanism -- a non-Abelian Yang-Mills graviphoton -- that gives MOND.
In their construction:
   a0  ~  c^2 / alpha          (their Eq. 60/61; alpha = EFT length scale)
   Lambda ~ 1 / alpha^2        (their Eq. 13; "natural order of magnitude")
Eliminating alpha gives  a0 ~ c^2 * sqrt(Lambda),  the SAME FORM as the framework's
   a0 = c^2 * sqrt(Lambda / 32pi).
DOOR: extract the COEFFICIENT C_S in a0 = c^2 * sqrt(Lambda / C_S) from Seraille's
normalization and COMPARE to the framework's 32pi.

OUTPUT (both ways, quarantine HARD -- a MATCH is NOT a derivation of kappa=1/2):
  AGREE  : C_S = 32pi within a gauge O(1)  -> cross-mechanism hint the O(1) is GEOMETRIC
  DISAGREE: the FORM a0~sqrt(Lambda) is multiply-realized but the COEFFICIENT is
            mechanism-dependent (undetermined in Seraille) -> strengthens the banked
            KAPPA_FORCING_DOOR_CLOSED.

WebFetch of arXiv:2502.14686v2 (this session) established the LITERAL normalization:
  Eq.(12):  L_YM = Tr{ c^2 Pi^{mu nu} H_{mu nu}
                     + c^4/(8 pi G) [ -Lambda/2 + H_{mu nu}H^{mu nu}
                                      + alpha H_{mu tau}H^{nu tau}H*^{mu nu} + O(alpha^2) ] }
  Eq.(13):  Lambda ~ 1/alpha^2          (the "~" is the AUTHORS' OWN symbol: a
                                         "natural order of magnitude", NOT an "=")
  Eq.(60):  a0 = -(8/3) * (1/alphabar) * (eta1 eta2 eta3)/(k2 k3 sin theta23)
            with alphabar = alpha/c^2  (Eq.27)
  Eq.(61):  a0 ~ c^2/alpha
  The eta_i are particle properties; k2,k3,sin theta23 are stated by the authors to
  depend on INITIAL CONDITIONS and are "a priori questionable" -> the O(1) is NOT
  fixed by the theory.
"""
import sympy as sp

print("="*80)
print("DOOR S -- Seraille a0 ~ sqrt(Lambda) coefficient cross-check vs framework 32pi")
print("="*80)

# ----------------------------------------------------------------------------
# 0. THE FRAMEWORK SIDE (the target coefficient).
# ----------------------------------------------------------------------------
c, G, hbar, pi = sp.symbols('c G hbar pi', positive=True)
Lambda, alpha = sp.symbols('Lambda alpha', positive=True)  # cosmological const, EFT length

C_fw = 32*sp.pi   # framework: a0 = c^2 sqrt(Lambda/32pi)
a0_fw = c**2 * sp.sqrt(Lambda/C_fw)
print("\n[framework]   a0 = c^2 * sqrt(Lambda / C),  C_fw = 32*pi =",
      float(32*sp.pi))
print("              (a0 = c^2 sqrt(Lambda/32pi) = c^2 sqrt(Lambda)/sqrt(32pi))")

# ----------------------------------------------------------------------------
# 1. THE SERAILLE SIDE -- what is FIXED vs what is FREE.
#    Eq.61:  a0 = c^2/alpha           (an EXACT relation up to the O(1) of Eq.60)
#    Eq.13:  Lambda ~ 1/alpha^2       (the AUTHORS' "~": dimensional naturalness ONLY)
#    We introduce an EXPLICIT unknown coefficient C_S for the Lambda relation:
#         Lambda = K_S / alpha^2,     and a generic O(1)  b_S in a0 = b_S c^2/alpha.
#    Then eliminating alpha:
#         alpha = b_S c^2 / a0   =>  Lambda = K_S / (b_S c^2/a0)^2 = K_S a0^2/(b_S^2 c^4)
#         => a0^2 = (b_S^2/K_S) c^4 Lambda  =>  a0 = c^2 sqrt(Lambda * b_S^2/K_S)
#         => a0 = c^2 sqrt(Lambda / C_S)    with  C_S = K_S / b_S^2.
# ----------------------------------------------------------------------------
K_S, b_S = sp.symbols('K_S b_S', positive=True)   # the two UNKNOWN O(1)'s in Seraille
a0_sym = sp.symbols('a0', positive=True)

# Eq.61 generalized: a0 = b_S c^2/alpha  -> solve for alpha
alpha_of_a0 = sp.solve(sp.Eq(a0_sym, b_S*c**2/alpha), alpha)[0]
print("\n[Seraille] from a0 = b_S c^2/alpha  ->  alpha =", alpha_of_a0)

# Eq.13 generalized: Lambda = K_S/alpha^2  -> substitute alpha(a0)
Lambda_expr = (K_S/alpha**2).subs(alpha, alpha_of_a0)
Lambda_expr = sp.simplify(Lambda_expr)
print("[Seraille] Lambda = K_S/alpha^2  ->  Lambda(a0) =", Lambda_expr)

# Solve back for a0 in terms of Lambda  -> read off C_S
a0_sol = sp.solve(sp.Eq(Lambda, Lambda_expr), a0_sym)
a0_sol = [s for s in a0_sol if s.is_positive][0] if any(s.is_positive for s in a0_sol) else a0_sol[0]
a0_sol = sp.simplify(a0_sol)
print("[Seraille] invert  ->  a0 =", a0_sol)

# Cast into the framework's form  a0 = c^2 sqrt(Lambda/C_S):  match C_S
C_S = sp.symbols('C_S', positive=True)
# a0_sol should equal c^2 sqrt(Lambda * b_S^2/K_S); so C_S = K_S/b_S^2
target = c**2*sp.sqrt(Lambda/C_S)
sol_CS = sp.solve(sp.Eq(a0_sol, target), C_S)
sol_CS = sp.simplify(sol_CS[0])
print("\n[Seraille] matched to a0 = c^2 sqrt(Lambda/C_S)  ->  C_S =", sol_CS)
print("           i.e.  C_S = K_S / b_S^2   (RATIO of the two undetermined O(1)'s)")

# Sanity: the FORM is identical (a0 ~ c^2 sqrt(Lambda)) regardless of K_S, b_S.
form_ok = sp.simplify(a0_sol/ (c**2*sp.sqrt(Lambda)) ).free_symbols.isdisjoint({Lambda, c})
print("\n[FORM CHECK]  a0/(c^2 sqrt(Lambda)) =",
      sp.simplify(a0_sol/(c**2*sp.sqrt(Lambda))),
      " (Lambda-, c-independent => the FORM a0 ~ c^2 sqrt(Lambda) is REPRODUCED)")

# ----------------------------------------------------------------------------
# 2. IS C_S DETERMINED?  -- the crux.
#    Seraille fixes NEITHER K_S nor b_S:
#      * b_S  : Eq.60 O(1) = (8/3)(eta1 eta2 eta3)/(k2 k3 sin theta23); the k_i,
#               theta_23 "depend on initial conditions" (authors), eta_i are particle
#               properties -> b_S is a FREE, IC-dependent O(1).
#      * K_S  : Eq.13 is "Lambda ~ 1/alpha^2", an order-of-magnitude/naturalness
#               estimate with the "~" symbol -> K_S is UNSPECIFIED (no prefactor).
#    => C_S = K_S/b_S^2 is a RATIO of two undetermined O(1) numbers. It is NOT a
#       definite number in the Seraille construction.
# ----------------------------------------------------------------------------
print("\n" + "="*80)
print("IS C_S A DEFINITE NUMBER IN SERAILLE?  -- NO")
print("="*80)
print("""
  C_S = K_S / b_S^2  where:
    K_S : the prefactor in Lambda = K_S/alpha^2.  Seraille Eq.13 writes 'Lambda ~ 1/alpha^2'
          with the order-of-magnitude '~' (a NATURALNESS/dimensional estimate), NO prefactor.
          => K_S is UNSPECIFIED.
    b_S : the O(1) in a0 = b_S c^2/alpha, = (8/3)(eta1 eta2 eta3)/(k2 k3 sin theta23) (Eq.60).
          The authors state k2,k3,sin theta23 'depend on initial conditions' and are
          'a priori questionable'.  => b_S is FREE / IC-dependent.
  Therefore C_S is the RATIO of two undetermined O(1)'s -> NOT a definite number.
""")

# ----------------------------------------------------------------------------
# 3. WHAT WOULD K_S HAVE TO BE to make C_S = 32pi?  (the "coincidence-or-not" test)
#    If we ALSO take the Seraille O(1) to its simplest normalization b_S = 1
#    (a0 = c^2/alpha exactly, Eq.61), then C_S = K_S, and matching 32pi DEMANDS
#    K_S = 32pi ~= 100.5 in Lambda = K_S/alpha^2.  Ask: is 32pi a "natural" O(1) for
#    a dimensional estimate Lambda ~ 1/alpha^2?  A naturalness estimate expects K_S ~ O(1),
#    i.e. order 0.1 - 10.  32pi ~ 100 is ~2 orders ABOVE a natural O(1).
# ----------------------------------------------------------------------------
print("="*80)
print("COINCIDENCE-OR-NOT:  what K_S forces C_S = 32pi (taking Seraille b_S=1, Eq.61)?")
print("="*80)
val_32pi = float(32*sp.pi)
print(f"  Framework C = 32*pi = {val_32pi:.4f}")
print(f"  With b_S=1 (a0=c^2/alpha exactly): C_S = K_S, so matching DEMANDS")
print(f"     K_S = 32*pi = {val_32pi:.4f}  in  Lambda = K_S/alpha^2.")
print(f"  A naturalness estimate 'Lambda ~ 1/alpha^2' expects K_S = O(1) ~ [0.1, 10].")
print(f"  32*pi ~= {val_32pi:.1f}  is ~{val_32pi/10:.0f}x above the TOP of a natural O(1) band,")
print(f"     ~{val_32pi/1:.0f}x above K_S=1.  => NOT a natural landing; would need tuning.")

# Equivalently, fold the 32pi into the framework: a0 = c^2 sqrt(Lambda/32pi)
#   <=> alpha_eff = c^2/a0 = sqrt(32pi/Lambda).  The framework's "alpha" is sqrt(32pi)*alpha_natural.
import numpy as np
# numeric Lambda (de Sitter), to show the FORM agrees numerically irrespective of C_S.
c_val   = 2.99792458e8           # m/s
Lam_val = 1.1056e-52             # m^-2  (Lambda; Planck-consistent)
# framework a0:
a0_framework = c_val**2*np.sqrt(Lam_val/val_32pi)
print(f"\n[numeric] framework a0 = c^2 sqrt(Lambda/32pi) = {a0_framework:.3e} m/s^2"
      f"   (target ~9.36e-11)")
# Seraille with b_S=1, K_S=1 ("most natural"): a0 = c^2 sqrt(Lambda)
a0_seraille_natural = c_val**2*np.sqrt(Lam_val/1.0)
print(f"[numeric] Seraille (b_S=K_S=1, 'most natural'): a0 = c^2 sqrt(Lambda) = "
      f"{a0_seraille_natural:.3e} m/s^2")
ratio = a0_seraille_natural/a0_framework
print(f"[numeric] ratio (natural Seraille)/(framework) = {ratio:.3f} = sqrt(32pi) = "
      f"{np.sqrt(val_32pi):.3f}")
print(f"          => the FORM matches; the COEFFICIENT differs by sqrt(32pi) ~ {np.sqrt(val_32pi):.1f}")
print(f"             between the framework and the SIMPLEST Seraille normalization.")

# ----------------------------------------------------------------------------
# 4. VERDICT
# ----------------------------------------------------------------------------
print("\n" + "="*80)
print("VERDICT")
print("="*80)
print(f"""
FORM:        a0 ~ c^2 sqrt(Lambda) is REPRODUCED by the Seraille YM-graviphoton
             mechanism (sympy-exact: a0 = c^2 sqrt(Lambda/C_S) for ANY O(1)'s), an
             INDEPENDENT mechanism from the framework's dS-Unruh modified inertia.
             => the FORM a0 ~ c^2 sqrt(Lambda) is MULTIPLY-REALIZED (cross-mechanism).

COEFFICIENT: C_S = K_S/b_S^2 is a RATIO of two UNDETERMINED O(1)'s in Seraille:
               - K_S unspecified (Eq.13 is 'Lambda ~ 1/alpha^2', the authors' '~',
                 a naturalness/dimensional estimate, NO prefactor),
               - b_S = (8/3)(eta1 eta2 eta3)/(k2 k3 sin theta23) IC-dependent (Eq.60).
             To force C_S = 32pi ~ {val_32pi:.1f} with the simplest b_S=1 needs
             K_S = 32pi ~ {val_32pi:.0f}, ~2 orders above a natural O(1) -> tuning.

=> DISAGREE (in the strict sense the door asks): the COEFFICIENT is MECHANISM-DEPENDENT
   and is NOT a definite number in Seraille -- it CANNOT be matched to 32pi because
   Seraille never fixes it (no prefactor on Lambda, IC-dependent a0 O(1)).
   This STRENGTHENS the banked KAPPA_FORCING_DOOR_CLOSED: the FORM a0~sqrt(Lambda) is
   multiply-realized (a0~Lambda^(1/2) is robust across mechanisms), but the
   coefficient 32pi (hence kappa=1/2) is NOT pinned by this cross-mechanism check.

QUARANTINE (hard): NOTHING here derives kappa=1/2. A 'match' was not even available to
   manufacture -- Seraille's coefficient is undetermined. The framework's 32pi remains a
   one-parameter input; this door is a CONFIRMING NULL on the coefficient (the FORM
   agrees, the NUMBER does not transmit), weighted EQUAL to a bridge per the #1 rule.
""")

print("[DONE] DOOR S verdict = DISAGREE (coefficient mechanism-dependent/undetermined);")
print("       FORM a0~c^2 sqrt(Lambda) cross-mechanism CONFIRMED; 32pi NOT pinned;")
print("       strengthens KAPPA_FORCING_DOOR_CLOSED. Quarantine held.")
