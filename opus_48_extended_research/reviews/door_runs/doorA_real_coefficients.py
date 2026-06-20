#!/usr/bin/env python3
"""
DOOR A -- REAL COEFFICIENTS (the open-caveat closer).

The banked doorA_positivity_gate.py PASS hinged on two PLACEHOLDERS:
    B_k4     = 1.0   # the k^4 ghost-condensate coefficient (canonical-acoustic guess)
    M_over_mu= 1.0   # the k^4 scale M vs the quasistatic mass mu (guessed equal)
With those, the Serra-Trombetta below-gap ratio v_gapped^2/c_s^2 was 0.75 (PASS) at
K_B=lambda_s=1 but FLIPPED to 1.06 (FAIL) at K_B=0.5. So the PASS was ORDER-SATURATED
and depended on numbers that were GUESSED, not read from the AeST action.

THIS SCRIPT replaces the guesses with the REAL coefficients extracted (this session,
verbatim-with-equation-numbers) from:
  * Skordis-Zlosnik arXiv:2007.00082 (PRL 127,161302) -- the 6-dof dispersion relations,
    Eq.(5) action, Eq.(13) quadratic action, stability window.
  * Blanchet-Skordis arXiv:2404.06584 (JCAP11(2024)040) -- Eq.(7) K(Q)=mu^2(Q-1)^2,
    Sec.5 (Eq.5.3-5.23) the Minkowski second-order action + deconstrained Hamiltonian,
    Sec.6.2 Eq.(6.8) the propagating dispersion in the Horava completion.

THE DECISIVE EXTRACTED FACTS (all quoted in-line):
 (E1) GAPPED PARTNER = the AeST massive VECTOR (spin-1) mode. SZ21 verbatim:
      "the dispersion relation for beta_i is  omega^2 = k^2 + M^2  where their mass is
       M^2 = (2-K_B)(1+lambda_s)Q0^2/K_B,  healthy if 0<K_B<2 and lambda_s>-1."
      => the gapped GRADIENT SPEED is EXACTLY c (coefficient of k^2 is 1), NOT an
         O(1) factor of K_B. THE PRIOR PLACEHOLDER MIS-IDENTIFIED THE GAPPED MODE:
         it used (2-K_B)/K_B*(1+K_B lam_s/2), which is the SCALAR sound speed (the
         GAPLESS Goldstone gradient coeff, modulo K2), NOT the gapped vector.
 (E2) GAPLESS GOLDSTONE = the scalar/Khronon mode. SZ21 verbatim:
      "omega^2 = 0  and  omega^2 = (2-K_B)/(K2 K_B) (1 + 1/2 K_B lambda_s) k^2 + M^2.
       Thus we require K2>0 in addition to the vector stability conditions."
      => the SCALAR sound speed is  c_s^2 = (2-K_B)/(K2 K_B) (1 + K_B lambda_s/2).
      The k^2-coefficient that the PRIOR script called "c_gapped^2" is ACTUALLY c_s^2.
 (E3) THE k^4 TAIL: there is NONE in the genuine AeST quadratic action.
      Blanchet-Skordis Sec.6.2 verbatim: "there are no higher derivative interaction
      terms in the action, which are also quadratic in the fields (and so contribute to
      the usual dispersion relation corresponding to a linear wave equation)."
      The Minkowski quadratic action (BS Eq.5.8) gives det M = 0 => omega^2 = 0
      IDENTICALLY for the scalar -- a NON-propagating (gapless, ZERO sound speed) mode.
      The k^4 tail B/M^2 used by ACLM ghost condensate is generated ONLY by adding the
      Horava higher-spatial-derivative terms (BS Eq.6.2 ellipsis), which are an
      EXTERNAL UV completion, "suppressed below some high energy scale" -- NOT part of
      the AeST action the framework uses. So B is NOT an O(1) AeST number; it is either
      ZERO (pure AeST) or a free Horava UV scale.

CONSEQUENCE FOR THE SERRA-TROMBETTA GATE (both-ways, honest):
  The ST theorem (arXiv:2412.19745) compares a GAPLESS Goldstone to a GAPPED partner
  BELOW the gap and requires v_gapped^2 <= c_s^2. With the REAL coefficients:
   - gapped (vector) gradient speed^2 = 1 (luminal, E1);
   - gapless (scalar) sound speed^2   = c_s^2 = (2-K_B)/(K2 K_B)(1+K_B lam_s/2) (E2);
   - the gapless mode has NO k^4 tail (E3): on the pure AeST action it is the omega=0
     non-propagating mode (c_s^2 set by the FLRW/MOND completion, not a Minkowski k^4).
  => Read literally, v_gapped^2 = 1 vs c_s^2.  ST PASS iff  c_s^2 >= 1.
     The ACTUAL gapped/gapless ordering test is therefore NOT the prior "0.75 vs B"
     placeholder; it is a CLEAN function of (K_B, K2, lambda_s) -- the real window.
"""

import sympy as sp
import numpy as np

LINE = "="*94
def hdr(s): print("\n"+LINE+"\n"+s+"\n"+LINE)

# ----------------------------------------------------------------------------
# REAL COEFFICIENTS (symbolic), as extracted
# ----------------------------------------------------------------------------
K_B, lam_s, K2, Q0, mu, k = sp.symbols('K_B lambda_s K2 Q0 mu k', positive=True)

# (E1) GAPPED vector mode  (SZ21):  omega^2 = k^2 + M_vec^2,  M_vec^2 = (2-K_B)(1+lam_s)Q0^2/K_B
M_vec2     = (2 - K_B)*(1 + lam_s)*Q0**2 / K_B          # gapped MASS^2
v_gapped2  = sp.Integer(1)                              # gapped GRADIENT speed^2 = 1 (luminal)

# (E2) GAPLESS scalar mode (SZ21):  omega^2 = c_s^2 k^2 + M_sc^2 (the propagating branch),
#      c_s^2 = (2-K_B)/(K2 K_B) (1 + K_B lam_s/2);  also a true omega^2=0 branch on Minkowski.
cs2_scalar = (2 - K_B)/(K2 * K_B) * (1 + K_B*lam_s/2)
M_sc2      = M_vec2                                     # same mass gap M (SZ21: "+ M^2")

hdr("(E1)-(E2) REAL AeST dispersion coefficients (Skordis-Zlosnik Eq. for beta_i and scalar)")
print("GAPPED vector (spin-1):  omega^2 = (1)*k^2 + M_vec^2")
print("   gradient speed^2  v_gapped^2 =", v_gapped2, "  (LUMINAL -- coefficient of k^2 is exactly 1)")
print("   mass^2  M_vec^2 = (2-K_B)(1+lambda_s)Q0^2/K_B =", M_vec2)
print("\nGAPLESS scalar (Khronon):  omega^2 = c_s^2 k^2 + M_sc^2   (propagating branch)")
print("   sound speed^2  c_s^2 = (2-K_B)/(K2 K_B) (1 + K_B lambda_s/2)")
print("   c_s^2 =", sp.simplify(cs2_scalar))
print("\n   *** PRIOR-SCRIPT ERROR EXPOSED ***")
print("   The banked doorA_positivity_gate.py set")
print("        c_gapped^2 := (2-K_B)/K_B (1+K_B lambda_s/2)   [its 'gapped' speed]")
print("   That is c_s^2 * K2  -- i.e. the GAPLESS SCALAR gradient coefficient (times K2),")
print("   NOT the gapped vector. The genuine gapped vector gradient speed is 1 (luminal).")
prior_cgap2 = (2 - K_B)/K_B*(1 + K_B*lam_s/2)
print("   check:  prior_c_gapped^2 / c_s^2 =", sp.simplify(prior_cgap2/cs2_scalar), " (= K2)")

# ----------------------------------------------------------------------------
# (E3) THE k^4 TAIL: NONE in the genuine AeST quadratic action
# ----------------------------------------------------------------------------
hdr("(E3) THE k^4 TAIL -- read from the genuine AeST quadratic action: B = 0")
print("""
Blanchet-Skordis Eq.(5.8): the Minkowski scalar normal-mode matrix M has det M = 0
=> omega^2 = 0 IDENTICALLY. The scalar is NON-PROPAGATING at quadratic order (an
A_k + B_k t mode), NOT an omega^2 ~ k^4 ghost-condensate wave. BS Sec.6.2 verbatim:
  'there are no higher derivative interaction terms in the action, which are also
   quadratic in the fields (and so contribute to the usual dispersion relation
   corresponding to a linear wave equation).'
The deconstrained Hamiltonian (BS Eq.5.23) is
   H_dec ~ [ ((1-alpha)k^2 - mu^2)/(alpha k^2 + mu^2) ] k^2 |psi_k|^2.
This is a GRADIENT (k^2) structure with a Jeans mass mu, NOT a k^4 tail. The genuine
AeST k^4 coefficient is therefore  B_AeST = 0  (no quadratic higher-derivative term).
A nonzero k^4 arises ONLY from the Horava completion (BS Eq.6.2 ellipsis: 'terms which
are of high order (fourth and sixth) in spatial derivatives ... suppressed below some
high energy scale') -- an EXTERNAL UV addition with a FREE scale M, NOT an AeST O(1).
""")
B_AeST = sp.Integer(0)
print("   B_AeST (k^4 coefficient in the genuine AeST quadratic action) =", B_AeST)
print("   => the prior placeholder B_k4=1.0 and M_over_mu=1.0 are NOT AeST numbers;")
print("      the AeST action has NO k^4 tail at all. The k^4 was an ACLM/Horava import.")

# ----------------------------------------------------------------------------
# THE SERRA-TROMBETTA GATE WITH THE REAL COEFFICIENTS
# ----------------------------------------------------------------------------
hdr("SERRA-TROMBETTA below-gap gate with the REAL coefficients:  v_gapped^2 <= c_s^2")
print("""
ST (arXiv:2412.19745): below the mass gap the GAPPED excitation must be SLOWER than
the GAPLESS one:  v_gapped^2 <= c_s^2 (gradient speeds compared in the same units).
REAL inputs:
   v_gapped^2 = 1                                  (luminal vector, E1)
   c_s^2      = (2-K_B)/(K2 K_B) (1 + K_B lam_s/2) (scalar Goldstone, E2)
=> ST is satisfied  <=>  c_s^2 >= 1.
We scan the AeST stability window {0<K_B<2, lambda_s>0, K2>0, mu^2>0}.
""")
cs2_f = sp.lambdify((K_B, lam_s, K2), cs2_scalar, 'numpy')

# solve the boundary c_s^2 = 1 for K2:  K2* = (2-K_B)/K_B (1+K_B lam_s/2)
K2_star = sp.simplify((2 - K_B)/K_B*(1 + K_B*lam_s/2))
print("ST-boundary (c_s^2 = 1) solved for K2:   K2* =", K2_star)
print("   ST PASS (c_s^2>=1, gapped not faster than gapless) <=>  K2 <= K2*")
print("   ST FAIL (c_s^2<1, gapped FASTER than gapless)      <=>  K2 >  K2*\n")

# numeric: what K2 do the PUBLISHED AeST models use? (SZ21 Fig.1 caption / parameter table)
#   "Cosh : KB=0.5, Q0=0.1, K2=7.5e3" ; "Higgs: KB=0.3, Q0=1, K2=8.5e8" ; "Exp: KB=0.1,K2=9.5e3"
#   Blanchet-Skordis convention: K2=1.
published = [
    ("BS24 quadratic convention", dict(K_B=0.5, lam_s=1.0, K2=1.0)),
    ("SZ21 'Cosh'  KB=0.5",       dict(K_B=0.5, lam_s=1.0, K2=7.5e3)),
    ("SZ21 'Higgs' KB=0.3",       dict(K_B=0.3, lam_s=1.0, K2=8.5e8)),
    ("SZ21 'Exp'   KB=0.1",       dict(K_B=0.1, lam_s=1.0, K2=9.5e3)),
]
print(f"  {'model':>26} | {'K_B':>5} {'lam_s':>6} {'K2':>10} | {'c_s^2':>11} | ST (c_s^2>=1)?")
for name, p in published:
    val = float(cs2_f(p['K_B'], p['lam_s'], p['K2']))
    print(f"  {name:>26} | {p['K_B']:5.2f} {p['lam_s']:6.2f} {p['K2']:10.3g} | "
          f"{val:11.3e} | {'PASS' if val>=1 else 'FAIL (gapped faster)'}")

# scan the window broadly at K2=1 (BS) and across K2
hdr("WINDOW SCAN:  is c_s^2 >= 1 (ST PASS) anywhere/everywhere?")
KB_grid  = np.linspace(0.02, 1.98, 99)
ls_grid  = np.array([0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
for K2v in [1.0, 7.5e3, 1e6]:
    vals = np.array([cs2_f(kb, ls, K2v) for kb in KB_grid for ls in ls_grid])
    frac_pass = float((vals >= 1.0).mean())
    print(f"  K2={K2v:>9.3g}:  c_s^2 range [{vals.min():.3e}, {vals.max():.3e}],  "
          f"fraction with c_s^2>=1 (ST PASS): {frac_pass:.1%}")

# the BS24 convention K2=1: c_s^2 = (2-K_B)/K_B (1+K_B lam_s/2); when is this >= 1?
hdr("BS24 convention K2=1: c_s^2 = (2-K_B)/K_B (1 + K_B lambda_s/2). ST PASS region")
cs2_K2_1 = sp.simplify(cs2_scalar.subs(K2, 1))
print("c_s^2(K2=1) =", cs2_K2_1)
# solve c_s^2 = 1 boundary in (K_B, lam_s):
boundary = sp.solve(sp.Eq(cs2_K2_1, 1), lam_s)
print("c_s^2 = 1 boundary (solve for lambda_s):  lambda_s =", [sp.simplify(b) for b in boundary])
# At lam_s -> 0: c_s^2 = (2-K_B)/K_B; >=1 iff K_B<=1. So for SMALL lam_s, ST PASS iff K_B<=1.
cs2_lam0 = sp.simplify(cs2_K2_1.subs(lam_s, 0))
print("  lambda_s->0:  c_s^2 = (2-K_B)/K_B =", cs2_lam0, " ; >=1  <=>  K_B <= 1")
KBcrit = sp.solve(sp.Eq(cs2_lam0, 1), K_B)
print("  => ST boundary at lambda_s=0:  K_B =", KBcrit, " (K_B<=1 PASS, K_B>1 FAIL)")
# general: c_s^2 increases with lam_s (coeff +1/2>0), so larger lam_s only helps PASS.
print("  d c_s^2/d lambda_s = (2-K_B)/(2 K2) > 0  on 0<K_B<2  -> larger lambda_s => larger c_s^2,")
print("  so the ST-PASS region GROWS with lambda_s. The binding corner is lambda_s->0.")

# ----------------------------------------------------------------------------
# SYNTHESIS
# ----------------------------------------------------------------------------
hdr("SYNTHESIS -- DOOR A with the REAL coefficients (both-ways, quarantine held)")
# evaluate the two decisive corners numerically
cs2_K2_1_f = sp.lambdify((K_B, lam_s), cs2_K2_1, 'numpy')
print(f"""
WHAT THE REAL COEFFICIENTS CHANGED (vs the placeholder PASS):

(1) The k^4 coefficient B and the M/mu ratio that the banked PASS hinged on DO NOT
    EXIST in the genuine AeST action (E3, Blanchet-Skordis Sec.6.2 + Eq.5.8): the AeST
    scalar is the NON-PROPAGATING omega^2=0 mode, with NO quadratic higher-derivative
    term, so B_AeST = 0. The k^4 tail (and hence the 0.75-vs-1.06 placeholder ratio)
    was an ACLM/Horava import with a FREE UV scale, not an AeST O(1) number. The
    open caveat's premise ("read B and M/mu from the real action") resolves to:
    THE REAL ACTION HAS NO k^4 -- the placeholder question was ill-posed against AeST.

(2) The GAPPED partner was MIS-IDENTIFIED in the banked script. The genuine gapped
    mode is the massive VECTOR (SZ21), whose gradient speed is EXACTLY 1 (luminal),
    not (2-K_B)/K_B*(...). The thing the banked script called "c_gapped^2" is in fact
    the GAPLESS SCALAR sound speed times K2. So the ST comparison, done with the REAL
    modes, is:   v_gapped^2 = 1   vs   c_s^2 = (2-K_B)/(K2 K_B)(1+K_B lambda_s/2).

(3) ST GATE, REAL:  PASS <=> c_s^2 >= 1.
    - In the SZ21 published models (K2 = 7.5e3 .. 8.5e8, chosen to fit the CMB) the
      scalar sound speed is c_s^2 ~ 1e-4 .. 1e-9 << 1 -> v_gapped(=1) >> c_s
      -> the gapped vector is FASTER than the gapless scalar -> ST literally FAILS
      in every CMB-fitting AeST model.
    - In the BS24 convention K2=1, c_s^2 = (2-K_B)/K_B (1+K_B lambda_s/2): ST PASSES
      for K_B <~ 1 (e.g. K_B=0.5: c_s^2={cs2_K2_1_f(0.5,1.0):.2f}>=1 PASS) and FAILS
      for K_B -> 2.

(4) HONEST READING (both-ways).  This is NOT a clean "robust PASS" and NOT a clean
    "K_B squeeze" -- the REAL coefficients reveal the prior ST framing was built on a
    MIS-IDENTIFIED gapped mode and a NON-EXISTENT k^4 tail. The genuine situation:

      * The Serra-Trombetta theorem, as a below-gap GAPPED-vs-GAPLESS speed ordering,
        is APPLIED to AeST only by IDENTIFYING gapless=scalar (c_s^2) and gapped=vector
        (speed 1). On that identification it requires c_s^2 >= 1, i.e. K2 <= (2-K_B)/K_B
        (1+K_B lam_s/2). The CMB-fitting AeST models (large K2) VIOLATE this -> a REAL,
        sharp EXCLUSION of the large-K2 (CMB-tuned) corner BY the home-institute IR
        theorem, IF its gapped/gapless identification is granted.

      * BUT the identification is itself contestable: in genuine AeST the scalar is
        the omega=0 NON-propagating mode (c_s^2 is a FLRW/MOND-completion quantity, not
        a Minkowski Goldstone speed), and the vector is a SEPARATE spin-1 sector that
        DECOUPLES from matter (SZ21: "They decouple from T_munu and are not expected to
        be generated to leading order by compact objects"). A below-gap ordering theorem
        between two DECOUPLED sectors with DIFFERENT gaps (M_vec vs the scalar's
        nonlinear scale) is NOT obviously the configuration ST assumes (one gapless +
        one gapped sharing a single EFT). So the ST gate does NOT cleanly bind AeST
        either way.

VERDICT (both-ways, NO manufactured win, NO reflexive squeeze):
  The banked Door-A "order-saturated PASS at 0.75" is RETRACTED as resting on a
  MIS-IDENTIFIED gapped mode + a GUESSED k^4 that the real AeST action does not contain.
  With the REAL coefficients:
   - There is NO k^4 tail in AeST (B=0); the scalar is the omega=0 mode (E3).
   - The gapped vector is LUMINAL (speed 1), the gapless scalar has c_s^2 =
     (2-K_B)/(K2 K_B)(1+K_B lambda_s/2) (E1,E2).
   - The literal ST ordering c_s^2>=1 is SATISFIED in the BS24 K2=1 small-K_B corner
     and badly VIOLATED in the CMB-fitting large-K2 SZ21 models -> a real K2/K_B
     EXCLUSION *if* the scalar-gapless/vector-gapped identification is granted.
   - That identification is contestable (decoupled sectors, scalar is non-propagating),
     so ST is NON-DIAGNOSTIC of AeST as it stands -- it neither robustly passes nor
     cleanly squeezes; it EXCLUDES the CMB-tuned large-K2 corner only under an
     identification AeST does not obviously satisfy.
  NET: the open caveat resolves NOT to "B>~0.5 robust pass" nor "B<~0.5 K_B squeeze"
  but to a THIRD answer the placeholder hid: the AeST quadratic action has NO k^4 and
  the gapped mode is luminal, so the sharp content is a c_s^2>=1 (=> K2 bounded)
  ordering that bites the CMB-fitting corner under a contestable identification.
  Quarantine held: a0/Z/kappa/I0 never asserted derived.
""")
print("DOOR A real-coefficient run complete. exit 0")
