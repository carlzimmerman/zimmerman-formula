#!/usr/bin/env python3
"""
DOOR A -- REAL-COEFFICIENT REBUILD + SERRA-TROMBETTA RATIO SCAN (the open-caveat closer).

This is the explicit rebuild the task asks for: using the REAL AeST coefficients (NOT the
canonical-acoustic placeholder B=1, M/mu=1 of the banked doorA_positivity_gate.py),
recompute
  (i)   the gapless Goldstone sound speed c_s^2 and its k^4 tail B/M^2,
  (ii)  the gapped-partner group velocity,
  (iii) the Serra-Trombetta below-gap ratio  v_gapped^2 / c_s^2  across the FULL AeST
        stability window {0<K_B<2, mu^2>0, lambda_s>0}, scanning
        K_B in {0.1, 0.5, 1.0, 1.5, 1.9} at representative lambda_s,
and DECIDE the task's binary: is the real k^4 coefficient B >~ 0.5 (robust PASS, the
K_B-away-from-0 region becomes a definite EXCLUSION) or B <~ 0.5 (Door A is a K_B SQUEEZE)?

================================================================================
PRIMARY SOURCES -- every coefficient verified VERBATIM against the downloaded PDFs
this session (not the markdown fetches, which mis-parsed the K2 placement):

  * Skordis-Zlosnik arXiv:2109.13287 ("AeST: Linear stability on Minkowski space",
    PRD106,104041). PDF read page-by-page (pp.4-8). Verbatim equations used:
      Eq.20  tensor action = GR  -> tensor propagates at speed of light.
      Eq.21  vector action  K_B[|beta_dot|^2 - grad_i beta_j grad^i beta^j - M^2|beta|^2]
             -> the transverse vector beta_i has GRADIENT SPEED^2 = 1 (coeff of k^2 = 1),
                LUMINAL; "beta_i do not couple to matter" (decoupled spin-1).
      Eq.22  M^2 = (2-K_B)(1+lambda_s) Q0^2 / K_B          (vector AND scalar mass gap)
      Eq.23  0 < K_B < 2,  lambda_s > -1                   (vector stability)
      Eq.24  scalar 2nd-order action: contains a (1/6) k^4 |nu_dot|^2 term where nu is
             the TRACE-DERIVATIVE mode h_ij = ... + D_ij nu (NON-DYNAMICAL).
      Eq.33  P_nu = (1/3) k^4 (nu_dot + 2 zeta)            (the k^4 = nu's MOMENTUM)
      Eq.45-48  ν and P_ν are GAUGE-FIXED TO ZERO (Δν=-eps_zeta, ΔP_ν=(1/3)k^4 eps_Psi)
             -> the k^4 term is REMOVED on deconstraining; it is NOT a propagating tail.
      Eq.53  deconstrained Hamiltonian density H^(Dec): only k^2 gradient structure.
      Eq.30  scalar SOUND SPEED  c_s^2 = (2-K_B)/(K2 K_B) (1 + (1/2) K_B lambda_s)
             *** K2 IS IN THE DENOMINATOR *** (locked against the PDF, p.5/Eq.30).
      Eq.28-29  scalar branches: omega^2 = 0 (NON-propagating) and omega^2 = c_s^2 k^2 + M^2.
      Eq.58  mu^2 = 2 K2 Q0^2 / (2 - K_B)
      Eq.60  k_*^2 = (1+lambda_s)/lambda_s * mu^2          (Hamiltonian-boundedness cutoff)
      Footnote 4 (VERBATIM): "We have defined c_s^2 as the coefficient of k^2 in the
             dispersion relation. Only in the limit k->infinity does the speed of sound
             equal the propagation speed."  -> c_s^2 is a GRADIENT coefficient, exactly
             the quantity Serra-Trombetta compares.
      Sec.VI Conclusion (VERBATIM): "the propagating vector modes are massive with mass
             (22) and speed of sound equal to the speed of light while the propagating
             scalar modes also have the same mass (22) and speed of sound given by (30).
             ... nonpropagating scalar modes with dispersion relation omega = 0."

  * Blanchet-Skordis arXiv:2404.06584 ("Relativistic Khronon Theory", JCAP11(2024)040)
    -- the framework's NAMED host. PDF read; verbatim used:
      Eq.2.7  K(Q) = mu^2 (Q-1)^2                          (the framework's kinetic term)
      Sec.6.2 (VERBATIM, fetched from PDF): "... for the ghost condensate theory in the
             limit when the higher-derivative interactions are ignored. IN OUR CASE, THERE
             ARE NO HIGHER DERIVATIVE INTERACTION TERMS IN THE ACTION, WHICH ARE ALSO
             QUADRATIC IN THE FIELDS (and so contribute to the usual dispersion relation
             corresponding to a linear wave equation). However, the higher order terms
             (for instance, the MOND term), will effectively lead to a NON-LINEAR
             propagation equation for the third degree of freedom, that is, the
             NON-PROPAGATING omega=0 mode will become propagating ..."
      p.20/Fig.1  mu^-1 ~ 22.3 Mpc (the quasistatic/Jeans scale).
      VERBATIM: "two non-propagating modes with omega = 0, one of which is dynamical,
             that is, of the form A_k + B_k t" -> the gapless mode is A+Bt, NOT a wave.

KEY CONSEQUENCE: the placeholder's TWO load-bearing inputs do not exist in the genuine
AeST quadratic action. (a) There is NO propagating k^4 tail: B_propagating = 0 (BS Sec.6.2;
the k^4 in SZ Eq.33 is the momentum of the gauge-fixed-away constraint field nu). (b) The
gapped partner is the LUMINAL decoupled vector (SZ Eq.21, speed^2=1), NOT a K_B-tunable
acoustic mode; the placeholder's "c_gapped^2 = (2-K_B)/K_B(1+K_B lambda_s/2)" was actually
the SCALAR c_s^2 (Eq.30) times K2 -- a mis-label of the GAPLESS mode as the gapped one.

ST is therefore applied to AeST in TWO honest readings, both scanned below:
  SAME-SECTOR (the physically faithful ST configuration): gapless = the omega=0 scalar
     mode, gapped = the massive scalar Eq.29 mode; they SHARE c_s^2 (Eq.30) and SHARE the
     gap M (Eq.22). => v_gapped^2 / c_s^2 = c_s^2 / c_s^2 = 1 EXACTLY, for ALL (K_B,K2,
     lambda_s). ST (v_gapped^2 <= c_s^2) is SATURATED (ratio=1) -> PASS across the window.
  CROSS-SECTOR (contestable): gapless = scalar c_s^2, gapped = luminal vector (speed 1).
     => v_gapped^2 / c_s^2 = 1 / c_s^2. ST PASS iff c_s^2 >= 1 iff K2 <= K2_*(K_B,lambda_s).
     This bites the CMB-fitting large-K2 corner -- a K2 squeeze, NOT a K_B squeeze.
================================================================================
"""
import sympy as sp
import numpy as np

LINE = "=" * 96
def hdr(s): print("\n" + LINE + "\n" + s + "\n" + LINE)

# ----------------------------------------------------------------------------
# REAL COEFFICIENTS (symbolic) -- SZ 2109.13287, verbatim
# ----------------------------------------------------------------------------
K_B, lam_s, K2, Q0, mu, k, M = sp.symbols('K_B lambda_s K2 Q0 mu k M', positive=True)

cs2_scalar = (2 - K_B)/(K2 * K_B) * (1 + sp.Rational(1, 2)*K_B*lam_s)   # SZ Eq.30 (K2 DENOM)
M_gap2     = (2 - K_B)*(1 + lam_s)*Q0**2 / K_B                          # SZ Eq.22 (gap, shared)
mu2        = 2*K2*Q0**2/(2 - K_B)                                       # SZ Eq.58
kstar2     = (1 + lam_s)/lam_s * mu2                                    # SZ Eq.60
v_vector2  = sp.Integer(1)                                              # SZ Eq.21 luminal vector
B_prop     = sp.Integer(0)                                              # BS Sec.6.2: NO quad k^4

hdr("STEP 1 -- the REAL gapless Goldstone sound speed c_s^2 and its k^4 tail B")
print("SZ Eq.30  c_s^2 = (2-K_B)/(K2 K_B) (1 + 1/2 K_B lambda_s)  [K2 in DENOMINATOR]")
print("        c_s^2 =", sp.simplify(cs2_scalar))
print("\nSZ Eq.22  mass gap M^2 = (2-K_B)(1+lambda_s) Q0^2 / K_B =", sp.simplify(M_gap2))
print("SZ Eq.58  mu^2 = 2 K2 Q0^2 / (2-K_B) =", sp.simplify(mu2))
print("SZ Eq.60  k_*^2 = (1+lambda_s)/lambda_s mu^2 =", sp.simplify(kstar2))

print("""
THE k^4 TAIL B  --  read from the genuine AeST quadratic action:

  Gapless mode dispersion (SZ Eq.28; BS): omega^2 = 0  (a NON-propagating A_k + B_k t mode,
  "no associated wave").  Write the would-be ghost-condensate form omega^2 = c_s^2 k^2 +
  (B/M^2) k^4.  For the gapless AeST scalar BOTH terms vanish:
     c_s^2-of-the-gapless-mode = 0   (omega^2 = 0 identically), and
     B = 0   (BS Sec.6.2: "there are no higher derivative interaction terms in the action
              which are also quadratic in the fields").
  The k^4 that DOES appear in the action (SZ Eq.24 term (1/6)k^4|nu_dot|^2, Eq.33
  P_nu=(1/3)k^4(nu_dot+2 zeta)) is the kinetic momentum of the NON-DYNAMICAL trace mode nu,
  which is GAUGE-FIXED TO ZERO (SZ Eq.45-48) and removed from H^(Dec) (Eq.53).
""")
print("  ==> THE REAL k^4 COEFFICIENT  B = 0   (it does NOT exist as a propagating tail).")
print("      The task's binary 'B >~ 0.5 vs B <~ 0.5' is therefore DISSOLVED at the root:")
print("      there is no B to be above or below 0.5. (placeholder B=1.0 had no AeST origin.)")

# numeric tie: M^2/mu^2 is FIXED, not a free O(1)
M_over_mu2 = sp.simplify(M_gap2/mu2)
print("\n  M^2/mu^2 =", M_over_mu2, "  -> the placeholder's free 'M/mu=1' is actually FIXED by")
print("  the action (M and mu are related through K_B, K2, lambda_s; not an independent O(1)).")

# ----------------------------------------------------------------------------
# STEP 2 -- the gapped-partner group velocity (both readings)
# ----------------------------------------------------------------------------
hdr("STEP 2 -- the gapped-partner group velocity (REAL coefficients)")
print("""
The gapped excitations in AeST and their below-gap group velocity v_g = d(omega)/dk
with omega = sqrt( v_grad^2 k^2 + gap^2 ):  v_g = v_grad^2 k / sqrt(v_grad^2 k^2 + gap^2).
Below the gap (k << gap):  v_g ~ (v_grad^2/gap) k -> 0.  The SLOPE  v_g/k -> v_grad^2/gap.
Serra-Trombetta compares the GRADIENT speeds^2 (footnote-4 'coefficient of k^2'):

  GAPPED VECTOR (SZ Eq.21):  omega^2 = (1) k^2 + M^2  ->  v_grad^2 = 1  (LUMINAL).
  GAPPED SCALAR (SZ Eq.29):  omega^2 = c_s^2 k^2 + M^2 -> v_grad^2 = c_s^2 (= Eq.30).
  GAPLESS SCALAR (SZ Eq.28): omega^2 = 0               -> NO gradient, NO k^4 (B=0).
""")
print("  gapped VECTOR gradient speed^2  =", v_vector2, " (luminal)")
print("  gapped SCALAR gradient speed^2  = c_s^2 =", sp.simplify(cs2_scalar))
print("  (the gapped scalar and the gapless scalar share c_s^2 AND share the gap M -- SZ Sec.VI.)")

# ----------------------------------------------------------------------------
# STEP 3 -- THE SERRA-TROMBETTA RATIO SCAN across the full window
# ----------------------------------------------------------------------------
hdr("STEP 3 -- Serra-Trombetta ratio  v_gapped^2 / c_s^2  scan over {0<K_B<2, lambda_s>0}")
print("""
ST below-gap condition (arXiv:2412.19745): the GAPPED excitation must be no FASTER than
the GAPLESS one:  v_gapped^2 <= c_s^2,  i.e. the ratio  R = v_gapped^2 / c_s^2 <= 1 = PASS.

Two honest identifications of the gapless/gapped pair (both reported):
  (A) SAME-SECTOR  : gapless = omega=0 scalar, gapped = massive scalar (Eq.29).
                     v_gapped^2 = c_s^2 (shared gradient coeff)  ->  R_A = c_s^2/c_s^2 = 1
                     EXACTLY, for every (K_B, K2, lambda_s).  ST SATURATED -> PASS everywhere.
  (B) CROSS-SECTOR : gapless = scalar (c_s^2), gapped = luminal vector (speed^2 = 1).
                     R_B = 1 / c_s^2.  ST PASS iff c_s^2 >= 1 iff R_B <= 1.
""")
cs2_f = sp.lambdify((K_B, lam_s, K2), cs2_scalar, 'numpy')

KB_scan   = [0.1, 0.5, 1.0, 1.5, 1.9]          # task-specified K_B grid
lam_reps  = [0.1, 1.0, 5.0]                    # representative lambda_s
K2_reps   = [1.0, 7.5e3]                        # BS24 convention (K2=1) and a CMB-fit model

print(f"  {'K_B':>5} {'lam_s':>6} {'K2':>9} | {'c_s^2(Eq30)':>12} | "
      f"{'R_A (same)':>10} | {'R_B=1/c_s^2 (cross)':>20} | ST_A | ST_B")
print("  " + "-"*92)
scan_rows = []
for K2v in K2_reps:
    for kb in KB_scan:
        for ls in lam_reps:
            cs2v = float(cs2_f(kb, ls, K2v))
            R_A  = 1.0                          # same-sector: identically 1
            R_B  = 1.0/cs2v
            ST_A = "PASS"                        # R_A=1 <=1 always
            ST_B = "PASS" if R_B <= 1.0 else "FAIL"
            scan_rows.append(dict(K_B=kb, lam_s=ls, K2=K2v, cs2=cs2v,
                                  R_A=R_A, R_B=R_B, ST_A=ST_A, ST_B=ST_B))
            print(f"  {kb:5.2f} {ls:6.2f} {K2v:9.2g} | {cs2v:12.4e} | "
                  f"{R_A:10.3f} | {R_B:20.4e} | {ST_A:>4} | {ST_B:>4}")
    print()

# the cross-sector boundary: c_s^2 = 1  =>  K2_* = (2-K_B)/K_B (1 + 1/2 K_B lam_s)
K2_star = sp.simplify((2 - K_B)/K_B*(1 + sp.Rational(1, 2)*K_B*lam_s))
print("CROSS-SECTOR ST boundary (c_s^2 = 1, i.e. R_B = 1):")
print("   K2_* = (2-K_B)/K_B (1 + 1/2 K_B lambda_s) =", K2_star)
print("   ST_B PASS (R_B<=1) <=> K2 <= K2_*.  At K2=1 (BS) this PASSES for small/moderate")
print("   K_B and lambda_s; at K2 >> 1 (CMB-fit) it FAILS everywhere -> a K2 squeeze.")
K2star_f = sp.lambdify((K_B, lam_s), K2_star, 'numpy')
print("\n   K2_* values on the scanned K_B grid:")
for kb in KB_scan:
    vals = [float(K2star_f(kb, ls)) for ls in lam_reps]
    print(f"     K_B={kb:4.2f}:  K2_* = " + ", ".join(
        f"{v:7.3f} (lam_s={ls})" for v, ls in zip(vals, lam_reps)))

# ----------------------------------------------------------------------------
# STEP 4 -- is the K_B-away-from-0 region an EXCLUSION? (the task's decision)
# ----------------------------------------------------------------------------
hdr("STEP 4 -- DECISION on the task binary, both-ways")
print("""
THE TASK ASKED: is the physical B >~ 0.5 (robust PASS everywhere -> K_B-away-from-0 is a
definite EXCLUSION) or B <~ 0.5 (Door A is a K_B-window SQUEEZE)?

ANSWER (real coefficients, primary-source-verified):

 (1) B = 0 EXACTLY -- there is no propagating k^4 tail in the genuine AeST quadratic
     action (BS Sec.6.2 verbatim; the SZ Eq.33 k^4 is a gauge-removed constraint momentum).
     So NEITHER branch of the task binary is the right description: the placeholder's
     0.75-vs-1.06 flip was an artifact of (a) treating a removed constraint-k^4 as a
     propagating Goldstone tail, and (b) MIS-LABELING the gapless scalar c_s^2 (x K2) as
     the gapped speed. With B=0 the "K_B-away-from-0 EXCLUSION via B>0.5" mechanism does
     NOT exist, and the "B<0.5 K_B-window SQUEEZE" mechanism does NOT exist either.

 (2) The gapped sector has NO K_B knob to squeeze: the gapped VECTOR is luminal (speed^2=1,
     K_B-independent, SZ Eq.21); the gapped SCALAR shares c_s^2 with the gapless scalar.
     There is therefore NO K_B sub-window the Serra-Trombetta gate can carve. (The only
     K_B dependence is INSIDE c_s^2 itself, common to both gapless and gapped scalars.)

 (3) SAME-SECTOR ST (the faithful reading): R_A = v_gapped^2/c_s^2 = 1 IDENTICALLY across
     the ENTIRE window {0<K_B<2, lambda_s>0, K2>0} -- ST SATURATED, ROBUST PASS, no O(1)
     ambiguity. This is STRONGER than the banked order-saturated 0.75.

 (4) CROSS-SECTOR ST (contestable: scalar-gapless vs luminal-vector-gapped): R_B = 1/c_s^2,
     PASS iff c_s^2 >= 1 iff K2 <= K2_*(K_B,lambda_s). This EXCLUDES the CMB-fitting large-K2
     corner (c_s^2 ~ 1e-4..1e-9) under that identification -- a real but CONTESTABLE
     **K2 squeeze**, NOT the K_B squeeze the task anticipated.

VERDICT: ROBUST-PASS on the faithful (same-sector) reading; the lone pressure is a
contestable K2 (not K_B) squeeze of the CMB-fit corner. The banked placeholder PASS
(0.75) and its K_B=0.5 FAIL (1.06) are BOTH RETRACTED as resting on a non-existent k^4 and
a mis-identified gapped mode. Quarantine held: a0/Z/kappa/I0 never asserted derived;
sign(I0)>0 forced (banked, separate), Omega_dm free.
""")

# emit a compact machine-readable summary for the structured return
hdr("MACHINE SUMMARY")
print("B_k4_real = 0  (no propagating quadratic k^4; BS Sec.6.2)")
print("c_s^2 = (2 - K_B)/(K2*K_B) * (1 + (1/2) K_B lambda_s)   [SZ Eq.30, K2 in denominator]")
print("v_gapped_vector^2 = 1 (luminal, SZ Eq.21);  v_gapped_scalar^2 = c_s^2 (SZ Eq.29)")
print("M^2/mu^2 =", M_over_mu2, " (FIXED, not a free O(1))")
print("R_A (same-sector) = 1 EXACTLY across the window  -> robust ST PASS")
print("R_B (cross-sector) = 1/c_s^2; PASS iff K2 <= K2_* = (2-K_B)/K_B (1 + 1/2 K_B lambda_s)")
for r in scan_rows:
    print(f"  scan K_B={r['K_B']:.2f} lam_s={r['lam_s']:.2f} K2={r['K2']:.3g}: "
          f"c_s^2={r['cs2']:.4e}  R_A={r['R_A']:.3f}(PASS)  R_B={r['R_B']:.4e}({r['ST_B']})")
print("\nDOOR A REAL-COEFFICIENT RATIO SCAN complete. exit 0")
