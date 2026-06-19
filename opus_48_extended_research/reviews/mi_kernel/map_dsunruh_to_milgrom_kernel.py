#!/usr/bin/env python3
r"""
MAP THE dS-UNRUH RESPONSE -> MILGROM'S MI FUNCTIONAL A(omega) AND KERNEL theta(y)
=================================================================================
TOPIC "map_to_milgrom" (2026-06-19)

THE QUESTION (the deepest open one in the MI program):
  Milgrom 2022 (arXiv:2208.07073v3 = PRD 106 064060) defines the modified-INERTIA
  EOM by   a_hat(omega) * mu[ A(omega)/a0 ] = a_hat_N(omega)   (Eq 3/5), with the
  nonlocal acceleration functional (Eq 20, VERBATIM from the PDF this session):

      A(omega) = (1/sqrt(2pi)) INT_0^inf  theta(omega'/omega) |a_hat(omega')| domega'

  and the kernel theta(y) is, in Milgrom's own words (page 12, after Eq 34, verbatim):
      "We have no knowledge of the form of theta(y), but unless it behaves unusually
       below y=1, we can expect theta(0) to be of the order of a few."
  Only theta(1)=1 is fixed -- and even that is a NORMALIZATION CONVENTION degenerate
  with a0 ("The normalization of theta(y) is degenerate with that of a0").  Milgrom's
  three EXAMPLE forms (verbatim): 2/(1+y^2), e^(1-y), e^((1-y)/2).

  The framework's FOUNDATION is the dS-Unruh effective temperature (Deser-Levin
  gr-qc/9706018):  T_eff = (hbar/2 pi c kB) sqrt(a^2 + (cH_Lambda)^2).  And the Unruh
  response for a NON-uniformly accelerated detector is itself nonlocal in time.  SO:
  does the dS-Unruh response to a TIME-VARYING acceleration FIX theta(y)/A(omega)?

WHAT THIS SCRIPT DOES (ruthless about circularity):
  STEP 1.  Write down the two objects EXACTLY and SEPARATELY, from their primary
           sources, WITHOUT assuming MOND:
             (M)  Milgrom's A(omega): a theta-weighted L1 convolution of |a_hat(omega')|
                  in LOG-frequency (kernel argument y=omega'/omega).
             (U)  The dS-Unruh / Unruh-DeWitt response to time-varying acceleration:
                  Kothawala-Padmanabhan (arXiv:0911.1017) exact linear-order result.
  STEP 2.  Read off the ACTUAL functional structure of the Unruh response (the kernel
           it DOES supply) and compare it, term by term, to the structure A(omega)
           requires.  Identify the mismatches.
  STEP 3.  If (and only if) the Unruh response supplies a kernel of Milgrom's form,
           READ OFF theta(y) at y in {0,0.5,1,2} and compare to the 3 guessed forms.
           If it does NOT, say exactly which structural property fails -- and whether
           any RESIDUAL constraint on theta survives (a partial pin), without
           smuggling in the MOND interpolation to manufacture one.

CIRCULARITY GUARD (#1 rule, both ways):
  * We NEVER assume the deep-MOND law g=sqrt(g_N a0) or mu_fw to "derive" theta.  The
    map must run Unruh-response -> theta, not MOND -> theta.
  * We verify a "theta is FIXED by Unruh" claim as hard as a "theta is FREE" claim.
  * The dS-Unruh temperature T_eff(a)=...sqrt(a^2+a_dS^2) is the CONSTANT-a (stationary,
    Killing-horizon) result (Deser-Levin / Gibbons-Hawking).  Using it AT a time-varying
    a is the adiabatic approximation -- which is exactly Milgrom's theta->theta(0)=const
    limit.  We must NOT confuse the adiabatic T_eff(a(t)) with a derived kernel.

QUARANTINE:  deriving theta(y) is a SEPARATE question from deriving a0/Z/kappa.  A
  derived kernel would NOT make a0 derived (a0 lives in mu[A/a0]; theta lives inside A).
  a0/Z NEVER asserted derived here.

PRIMARY SOURCES (text verified firsthand this session):
  - Milgrom 2022 arXiv:2208.07073v3, PDF pages 7,10,11,12: Eq (20) A(omega) kernel;
    Eq (33),(34),(35) two-frequency EFE; "We have no knowledge of the form of theta(y)".
  - Kothawala & Padmanabhan, arXiv:0911.1017 (Phys Rev D 82, 064019): time-dependent-a
    UDW response, exact to O(eta), eta=g_dot/g^2; Eqs (10)-(26): the correction is a
    DERIVATIVE expansion, a single-variable function of s=2pi*omega/g times (eta*t).
  - Deser & Levin gr-qc/9706018: T_eff = sqrt(a^2 + a_dS^2)/2pi (constant-a result;
    global embedding, Killing horizon).
"""
import numpy as np
import sympy as sp

np.set_printoptions(linewidth=120)
PASS = "PASS"; FAIL = "FAIL"
def H(s): print("\n"+"="*100+"\n "+s+"\n"+"="*100)
def h(s): print("\n"+"-"*100+"\n "+s+"\n"+"-"*100)

# ----------------------------------------------------------------- framework footing (sealed)
c, G, hbar, kB = 2.998e8, 6.674e-11, 1.0546e-34, 1.381e-23
a0 = 9.36e-11                                   # = c^2 sqrt(Lambda/32pi); NEVER asserted derived
Lambda = (a0/c**2)**2 * 32*np.pi
cH_Lam = c*np.sqrt(Lambda/3.0)                  # dS floor acceleration
a_dS   = cH_Lam                                 # the floor inside Deser-Levin sqrt

# Milgrom's three EXAMPLE kernels (verbatim, page 12) -- the things we compare AGAINST
def theta_rat(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)        # theta(0)=2
def theta_e1(y):  y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)        # theta(0)=e
def theta_e2(y):  y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)  # theta(0)=e^0.5
GUESSED = [("2/(1+y^2)", theta_rat, 2.0), ("e^(1-y)", theta_e1, np.e), ("e^((1-y)/2)", theta_e2, np.exp(0.5))]
YGRID = [0.0, 0.5, 1.0, 2.0]

H(" STEP 0:  the two objects, stated exactly and separately (NO MOND assumed)")
print(f"""
 framework footing (sealed, quarantined): a0 = {a0:.3e} m/s^2,  a_dS = cH_Lam = {a_dS:.3e} = {a_dS/a0:.3f}*a0

 (M) MILGROM A(omega), Eq (20) verbatim:
        A(omega) = (1/sqrt(2pi)) INT_0^inf theta(omega'/omega) |a_hat(omega')| domega'
     -> a LINEAR (L1) functional of |a_hat|, kernel depends ONLY on the RATIO y=omega'/omega
        (scale-free in frequency: the SAME theta convolves every probe frequency omega).
        theta(y): symmetric, theta(1)=1 (a NORMALIZATION fixing, degenerate with a0),
        "we have no knowledge of the form", theta(0)~few.
     -> the inertia is mu[A/a0]: a0 enters HERE (outside A); theta lives INSIDE A.

 (U) dS-UNRUH RESPONSE to a time-varying acceleration:
     constant-a (stationary):  T_eff = (1/2pi) sqrt(a^2 + a_dS^2)         (Deser-Levin)
     time-varying-a (UDW):      P_dot = I_Planck[g0] + eta*t*omega^2*[1 - (pi^2/s^2) e^s/(e^s-1)^2]
        (Kothawala-Padmanabhan 0911.1017, exact to O(eta)),  s = 2pi*omega/g0,  eta = g_dot/g0^2.
     -> the time-varying correction is a DERIVATIVE EXPANSION in eta=g_dot/g^2, a single-variable
        function of s=omega/g times (eta*t).  It is NOT an L1 convolution of |a_hat| over a
        finite-width kernel in log-frequency.
""")

# =====================================================================================
H(" STEP 1:  STRUCTURAL COMPARISON -- does the Unruh response have Milgrom's A(omega) FORM?")
# =====================================================================================
print(r"""
 We line up the structural properties Milgrom's A(omega) REQUIRES against what the Unruh response
 (constant-a Deser-Levin, and time-varying KP) actually SUPPLIES.  Each is a hard yes/no.
""")

checks = []
def chk(prop, milgrom_needs, unruh_gives, verdict, note=""):
    checks.append((prop, milgrom_needs, unruh_gives, verdict, note))

chk("Linear in |a_hat| (L1 functional)",
    "A = INT theta * |a_hat| d omega'  (linear, homogeneous degree 1 in a_hat)",
    "T_eff = sqrt(a^2+a_dS^2): NONLINEAR in a (deep-a -> |a|, low-a -> a^2/2a_dS); KP corr ~ eta*t = (a_dot/a^2)*t",
    FAIL,
    "Unruh T_eff is sqrt(a^2+..)-nonlinear; A is strictly linear in |a_hat|. Different homogeneity.")

chk("Kernel depends ONLY on the ratio y=omega'/omega (frequency scale-free)",
    "theta(omega'/omega): same kernel convolves EVERY probe frequency; no absolute freq scale in theta",
    "KP correction is a function of s=2pi*omega/g0: omega is measured against the ACCELERATION g0, not omega'",
    FAIL,
    "Unruh introduces an ABSOLUTE scale g0 (or a_dS); theta has NO absolute scale (a0 sits OUTSIDE A).")

chk("Two-frequency coupling theta(omega_ex/omega_in) (EFE)",
    "A(om_in) = om_in^2|r_in| + om_ex^2|r_ex| theta(om_ex/om_in): cross-frequency convolution",
    "KP is single-trajectory g(tau); its correction couples omega (probe/gap) to g and g_dot, NOT om_ex to om_in",
    FAIL,
    "Unruh response has no 'external vs internal frequency' split; it is one detector on one worldline.")

chk("Adiabatic limit theta -> theta(0) = const (a few)",
    "y->0 (om_ex<<om_in): theta(0) ~ few, finite; gives the EFE strength theta(0)*a_ex",
    "adiabatic Unruh: g_dot->0 => eta->0 => correction VANISHES => T_eff(a(t)), pure local sqrt(a^2+a_dS^2)",
    FAIL,
    "CRUX: Unruh's adiabatic limit kills the nonlocal correction (eta->0); Milgrom's adiabatic limit keeps a FINITE theta(0). Opposite content.")

chk("Memory kernel width / nonlocality timescale",
    "set by a0/c-type galactic time (theta width is O(1) in y -> memory ~ orbital time)",
    "set by 1/g_dot and the dS time 1/H_Lambda (a Hubble time); a DIFFERENT, geometry-fixed scale",
    "PARTIAL",
    "Both are genuinely time-nonlocal; the Unruh memory ~1/H_Lambda is REAL but is NOT theta's y-structure.")

print(f"  {'property':52s} | {'verdict':7s} | note")
print("  "+"-"*96)
for prop, mn, ug, v, note in checks:
    print(f"  {prop:52s} | {v:7s} | {note}")

nfail = sum(1 for *_,v,_ in [(0,0,0,v,0) for *_,v,_ in checks] )  # count
nfail = sum(1 for c in checks if c[3]==FAIL)
print(f"\n  STRUCTURAL VERDICT: {nfail}/{len(checks)} load-bearing properties FAIL to match.")
print(r"""  The dS-Unruh response does NOT have the FORM of Milgrom's A(omega):
    - A is LINEAR in |a_hat|; T_eff is sqrt(a^2+a_dS^2)-NONLINEAR.
    - theta is frequency-scale-free (y=om'/om only); the Unruh correction carries an ABSOLUTE scale (g0, a_dS).
    - A couples two DISTINCT frequencies (om_ex, om_in); the UDW response is one worldline, one gap freq.
    - DECISIVE: the adiabatic limits POINT OPPOSITE WAYS -- Unruh's nonlocal piece VANISHES as g_dot->0
      (eta->0), whereas Milgrom's theta->theta(0)=O(few) stays FINITE.  The thing the Unruh response
      computes (the leading correction to thermality from g_dot) is NOT the thing theta(y) parametrizes
      (the relative weighting of distinct Fourier components in the inertia functional).""")

# =====================================================================================
H(" STEP 2:  CAN we still READ OFF a theta(y) from the Unruh response?  (try honestly, both ways)")
# =====================================================================================
print(r"""
 Even though the FORM mismatches, one could ask: is there a DERIVED kernel hiding in the Unruh
 response that, FORCED into Milgrom's A(omega) slot, yields a specific theta(y)?  Three honest attempts;
 each is checked for circularity (did we smuggle in MOND to get MOND?).
""")

# ---- Attempt 2A: identify theta from the KP linear-order response kernel directly --------------------
h(" Attempt 2A:  read theta(y) off the KP time-varying response kernel  K(s)=1 - (pi^2/s^2) e^s/(e^s-1)^2")
s = sp.symbols('s', positive=True)
Kkp = 1 - (sp.pi**2/s**2)*sp.exp(s)/(sp.exp(s)-1)**2
print("  KP correction kernel K(s) (Eq 25), s = 2pi*omega/g0:")
print("     K(s) = 1 - (pi^2/s^2) * e^s/(e^s - 1)^2")
# limits
K0 = sp.limit(Kkp, s, 0)
Kinf = sp.limit(Kkp, s, sp.oo)
print(f"     K(s->0)   = {K0}   (low-freq: correction kernel -> {float(K0):+.4f})")
print(f"     K(s->inf) = {Kinf}   (high-freq: -> {float(Kinf):+.4f}, recovers thermal at T=g(t))")
print(r"""  PROBLEM (fatal for a map): K(s) is a function of s = 2pi*omega/g0 -- the GAP frequency over the
  ACCELERATION.  Milgrom's theta(y) is a function of y = omega'/omega -- a ratio of TWO trajectory
  frequencies, with NO acceleration scale in it.  s and y are DIFFERENT arguments built from different
  objects.  There is no change of variables turning K(2pi*omega/g0) into theta(omega'/omega):
    - K carries the dimensionful g0 (an acceleration); theta is scale-free.
    - K multiplies (eta*t) = (g_dot/g0^2)*t, a SECULAR (grows with t) term -- not a stationary inertia.
  => 2A yields NO theta(y).  Forcing K into the theta slot is a category error (wrong arguments).""")

# Tabulate K(s) just to show it is not any of the guessed theta forms even if one (wrongly) set s<->y
print(f"\n  (For the record, K(s) vs the guessed theta(y) if one ILLEGALLY set s=y -- shows they don't match either:)")
print(f"  {'arg':>5} | {'K(s)  [KP corr]':>16} | {'2/(1+y^2)':>10} {'e^(1-y)':>9} {'e^((1-y)/2)':>12}")
Kf = sp.lambdify(s, Kkp, 'numpy')
for yv in [0.25,0.5,1.0,2.0,4.0]:
    print(f"  {yv:5.2f} | {float(Kf(yv)):16.4f} | {theta_rat(yv):10.4f} {theta_e1(yv):9.4f} {theta_e2(yv):12.4f}")
print("  -> K(s) is NEGATIVE/small and s-shaped; the guessed theta are O(1-2) and decreasing. Not the same object.")

# ---- Attempt 2B: the adiabatic dS-Unruh T_eff as a 'kernel' -> only gives theta(0)-type CONSTANT --------
h(" Attempt 2B:  the adiabatic Deser-Levin T_eff(a) = sqrt(a^2+a_dS^2) -- what theta does IT imply?")
print(r"""  The adiabatic dS-Unruh temperature uses the INSTANTANEOUS a (constant-a Killing-horizon result
  applied quasi-statically).  In Milgrom's language a constant theta = theta(0) is EXACTLY the adiabatic
  limit (Eq 35: a_hat mu[theta(0) a_ex/a0] = a_hat_N).  So the adiabatic dS-Unruh response can AT MOST
  fix theta(0) (a single number), NOT the FUNCTION theta(y).  And even theta(0):""")
# what does adiabatic dS-Unruh fix theta(0) to? The honest reading: it fixes the FLOOR a_dS, not theta(0).
# theta(0) is the relative weight of a near-DC external component. The adiabatic T_eff has NO second
# frequency, so it cannot define theta(0) at all without an external choice.
print(f"""
   The adiabatic T_eff(a)=sqrt(a^2+a_dS^2)/2pi has ONE frequency (DC) and ONE acceleration.  theta(0) is
   the relative WEIGHT a near-DC EXTERNAL component carries in the inertia argument of an INTERNAL mode --
   that requires TWO frequencies.  The adiabatic (single-frequency) dS-Unruh object has no second
   frequency, so it does not even define theta(0), let alone theta(y).
   => 2B fixes a0's FLOOR (a_dS, the cosmological piece) -- the thing the framework already uses -- and
      says NOTHING about the kernel.  (And mapping the floor to theta(0) would be CIRCULAR: it would set
      theta(0) by choosing the response->inertia map, the very ansatz that is unproven.)""")

# ---- Attempt 2C: the full nonlocal worldline integral (prior repo result) -> does it carry theta? ------
h(" Attempt 2C:  the full time-nonlocal dS worldline response (prior repo: NONLOCAL_MI_INTEGRAL_VERDICT)")
print(r"""  The prior repo work (reviews/NONLOCAL_MI_INTEGRAL_VERDICT_2026-06-15, wwgakjpc0) built the genuine
  time-nonlocal dS-Unruh worldline functional for a TIME-VARYING proper acceleration and found its
  deep-a expansion (Synge/Frenet):
      Z5 = ds^2 [ 1 + (a5^2/12) ds^2 + (a5^4/360 + a.a''/240 + a'^2/720) ds^4 + ... ],  a5=sqrt(a^2+a_dS^2)
  The nonlocal (memory) term's period-average is  -A1^2 Omega^2/720  (nonzero, frequency-dependent ->
  genuinely time-nonlocal).  KEY for the kernel question (verified there): the deep-a limit of the
  NONLOCAL piece is ANALYTIC in a-magnitude (~ a'^2/720, a TIME-DERIVATIVE term), carrying at most
  sqrt(a') -- it NEVER reproduces the sqrt(g_N) MOND law (that comes from the LOCAL a5=sqrt(a^2+a_dS^2)
  quadrature, not the nonlocal kernel).  So:
    - the dS worldline response DOES supply a genuine nonlocal kernel (the a.a'', a'^2 derivative terms),
    - but that kernel is a LOCAL DERIVATIVE EXPANSION (a, a', a'' at one time) -- the SAME structural class
      as KP's eta-expansion -- NOT an L1 convolution theta(omega'/omega)|a_hat(omega')| over the spectrum,
    - and it carries the MOND form via the LOCAL piece, not via the nonlocal kernel.
  => 2C: the genuine dS nonlocal response is a DERIVATIVE-expansion memory kernel (a'^2, a.a''), which is
     a DIFFERENT mathematical object from Milgrom's spectral convolution theta(y).  It does not deliver
     theta(y); and where it is nonlocal, it does not carry MOND.""")

# =====================================================================================
H(" STEP 3:  IS THERE A RESIDUAL CONSTRAINT ON theta?  (partial pin vs fully free -- both ways)")
# =====================================================================================
print(r"""
 Having shown the Unruh response does not FIX theta(y), we ask the weaker, honest question: does it
 CONSTRAIN theta at all?  We separate what is genuinely implied from what would be circular to claim.
""")

residual = []
residual.append(("theta(1)=1",
    "NORMALIZATION ONLY (Milgrom: degenerate with a0). Not physics. Neither Unruh nor anything else 'derives' it.",
    "no-op"))
residual.append(("theta symmetric theta(-y)=theta(y)",
    "Follows from a(t) REAL => |a_hat| symmetric (Milgrom Eq 20 footnote). A reality/Fourier fact, NOT from Unruh.",
    "generic"))
residual.append(("theta(0) finite & O(few)",
    "Milgrom's EXPECTATION ('unless it behaves unusually'). The adiabatic dS-Unruh T_eff is FINITE at DC "
    "(sqrt(0+a_dS^2)=a_dS>0), CONSISTENT with theta(0) finite -- but consistency is NOT derivation, and "
    "the NUMBER (2? e? e^0.5?) is NOT fixed.",
    "consistency-only"))
residual.append(("theta decreasing for y>1",
    "Milgrom NEEDS this for the correct center-of-mass motion (Eq 33: high-freq internal modes must "
    "decouple). The dS-Unruh response DOES fall off at high relative frequency (KP: K(s)->1, correction "
    "-> thermal; high-freq modes thermalize/decouple) -- the SAME QUALITATIVE direction. But this is a "
    "decoupling requirement satisfied by MANY kernels, not a unique form.",
    "qualitative-direction"))

print(f"  {'theta property':28s} | {'status from the Unruh map':66s}")
print("  "+"-"*99)
for prop, stat, tag in residual:
    print(f"  {prop:28s} | {tag:66s}")
    for line in [stat[i:i+94] for i in range(0,len(stat),94)]:
        print(f"  {'':28s} |   {line}")
print(r"""
  RESIDUAL VERDICT (both ways):
   * DERIVED:        NOTHING about the FORM of theta(y) is derived from the dS-Unruh response.
   * CONSISTENT:     theta(1)=1 (convention), theta symmetric (reality of a(t)), theta(0) finite (dS floor
                     a_dS>0 => DC response finite), theta decreasing for y>>1 (high-freq modes thermalize).
                     These are CONSISTENCY/QUALITATIVE facts -- 3 of the 4 are generic (Fourier/normalization),
                     and the 4th (high-y falloff) is a direction shared by infinitely many kernels.
   * NOT FIXED:      theta(0)'s VALUE (2 vs e vs e^0.5 -> the 6-13% sigma-spread), the y<1 shape, the falloff
                     rate -- ALL FREE.  The Unruh response neither selects among the 3 guessed forms nor
                     forbids any of them.""")

# Show the 6-13% spread is fully carried by the UNCONSTRAINED theta(0)/shape:
h(" The unconstrained content, quantified: theta(0) and shape set the entire 6-13% sigma-spread")
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
a_in=a_ex=a0
def Rratio(y, thf):  # sigma_MI(y)/sigma_QS, QS=adiabatic theta(0); sigma~sqrt(boost), boost=1/mu_fw(A/a0)
    A_y  = a_in + a_ex*thf(y);  A_qs = a_in + a_ex*thf(0.0)
    return np.sqrt( (1.0/mu_fw(A_y/a0)) / (1.0/mu_fw(A_qs/a0)) )
print(f"  theta(y) at the requested grid y in {YGRID} for the 3 GUESSED forms (none Unruh-derived):")
print(f"  {'y':>5} |" + "".join(f"{nm:>14}" for nm,_,_ in GUESSED))
print("  "+"-"*52)
for y in YGRID:
    print(f"  {y:5.2f} |" + "".join(f"{thf(y):14.4f}" for _,thf,_ in GUESSED))
print(f"\n  resulting sigma-spread across a plunging window y in [0,1.5] (deep-MOND member a_in=a_ex=a0):")
yfull=np.linspace(0,1.5,200)
for nm,thf,th0 in GUESSED:
    Rs=np.array([Rratio(y,thf) for y in yfull]); sp_=(Rs.max()-Rs.min())/Rs.mean()
    print(f"    theta={nm:14s} theta(0)={th0:5.3f}  -> spread = {sp_*100:5.1f}%   (this number is theta-CHOICE-driven)")
print("  => the 6-13% spread is ENTIRELY a function of the UNDERIVED theta(0)/shape.  The Unruh map pins NONE of it.")

# =====================================================================================
H(" STEP 4:  CIRCULARITY AUDIT -- did any attempt smuggle MOND in to get MOND out?")
# =====================================================================================
print(r"""
 We list every place a circular 'derivation' could sneak in, and confirm we did NOT take it:
  [C1] Using g=sqrt(g_N a0) or mu_fw to 'read off' theta:  NOT DONE. mu_fw appears ONLY in Step 3's
       quantification of the (already-free) spread -- never to constrain theta itself.
  [C2] Setting theta(0) by matching the adiabatic dS-Unruh T_eff to the MOND EFE strength:  REFUSED in
       2B as explicitly circular (it presupposes the response->inertia map = the unproven ansatz).
  [C3] Declaring the dS floor a_dS 'is' theta(0)*a_ex:  REFUSED -- a_dS is the COSMOLOGICAL floor that
       sets a0 (one frequency, DC); theta(0) is a TWO-frequency relative weight. Different objects.
  [C4] Picking the kernel that 'reproduces' the observed 0.11-0.13 dex RAR:  NOT DONE -- that would fit
       theta to data, not derive it from the Unruh response.
 => No circular derivation was used.  The honest result stands: the map does NOT fix theta.
""")

# =====================================================================================
H(" FINAL SYNTHESIS")
# =====================================================================================
print(r"""
 DOES THE dS-UNRUH RESPONSE FIX MILGROM'S A(omega) / theta(y)?   NO.  The kernel stays a FREE FUNCTION.

 WHY (structural, from the primary sources, no MOND assumed):
  1. WRONG FUNCTIONAL CLASS.  Milgrom's A(omega) (Eq 20) is an L1 SPECTRAL CONVOLUTION
        A = (1/sqrt2pi) INT theta(omega'/omega)|a_hat(omega')|domega'
     -- linear in |a_hat|, frequency-scale-free (kernel = function of the ratio omega'/omega only).
     The dS-Unruh response to time-varying a is a DERIVATIVE EXPANSION: KP's exact O(eta) result
     (eta=g_dot/g^2) and the prior repo's worldline expansion (a, a', a'' at one time) are LOCAL-in-time
     memory kernels carrying an ABSOLUTE acceleration scale (g0, a_dS) -- a different mathematical object.
     No change of variables maps one onto the other (s=2pi*omega/g0 is not y=omega'/omega).
  2. OPPOSITE ADIABATIC LIMITS (the decisive tell).  As the external field slows (g_dot->0, eta->0) the
     Unruh nonlocal correction VANISHES, leaving the LOCAL T_eff(a(t)).  Milgrom's adiabatic limit
     KEEPS a finite theta(0)~few (Eq 35).  The Unruh response is computing the leading departure from
     LOCAL thermality; theta(y) is parametrizing the RELATIVE WEIGHT of distinct Fourier components.
     These are not the same quantity, so the former cannot fix the latter.
  3. WHAT IS DERIVED is the framework's FLOOR (a_dS = cH_Lam, the cosmological a0-setting piece), which
     it already uses -- NOT the kernel.

 WHAT THE MAP DOES LEAVE (residual, credited honestly, both ways):
  - CONSISTENT (not derived): theta(0) finite (dS DC response finite), theta decreasing for y>>1
    (high-freq modes thermalize/decouple), theta symmetric (a(t) real), theta(1)=1 (normalization).
  - 3 of these 4 are generic Fourier/normalization facts; the 4th (high-y falloff) is a direction shared
    by infinitely many kernels.  None selects among 2/(1+y^2), e^(1-y), e^((1-y)/2), or forbids any.

 theta(y) AT THE REQUESTED GRID:  NOT determined by the Unruh response.  The only y-value the map even
   speaks to is theta(0) (finite, sign-consistent) and the y>>1 tail (decreasing) -- both QUALITATIVE.
   At y in {0, 0.5, 1, 2} the Unruh response supplies NO numbers; the three guessed forms remain the
   honest bracket (theta(0): 2, e=2.72, e^0.5=1.65; theta(0.5): 1.6, 1.65, 1.28; theta(1)=1 all;
   theta(2): 0.4, 0.37, 0.61).

 PINS THE 6-13% sigma-SPREAD?  NO.  The spread is entirely a function of the underived theta(0)/shape;
   the Unruh map constrains none of it.  It stays kernel-GUESSED, exactly like AeST's free function.

 QUARANTINE HELD:  this is about the KERNEL, not a0.  a0/Z/kappa NEVER asserted derived.  (And note the
   kernel question is logically downstream of a0: theta lives INSIDE A; a0 sits in mu[A/a0].  A derived
   kernel would not derive a0, and here the kernel is not derived either.)

 BOTH WAYS:  the genuine partial structure (a REAL time-nonlocal dS worldline functional exists; the
   high-freq decoupling direction matches; the dS floor is the right a0 piece) is credited at full
   weight; the failure to fix theta's FORM/VALUE -- and the resulting un-pinned 6-13% spread -- is
   conceded at full weight.  No manufactured derivation; no dismissed partial constraint.
""")
print("DONE.")
