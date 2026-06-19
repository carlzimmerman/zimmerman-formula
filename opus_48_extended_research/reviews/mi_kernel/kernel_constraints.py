#!/usr/bin/env python3
r"""
WHAT PINS THE MI KERNEL theta(y)/A(omega) WITHOUT A FULL DERIVATION   (topic "kernel_constraints")
====================================================================================================
The MI kernel theta(y) [Milgrom 2022 arXiv:2208.07073 = PRD 106 064060, the "nonlocal acceleration"
A(omega)=(1/sqrt(2pi)) int theta(w'/w)|a_hat(w')|dw'] is currently a FREE function: the framework's
distinctive cluster sigma-spread spans ~6-13% across three GUESSED forms (theta=2/(1+y^2):10.3%;
e^{1-y}:11.8%; e^{(1-y)/2}:6.2%; mi_sigma_spread_amplitude.py). This script asks the model-INDEPENDENT
question: WITHOUT deriving theta, how much do physical-consistency constraints alone PIN it -- do they
collapse the 6-13% band?

THE SIX CONSTRAINTS (enumerated, then APPLIED to admissible kernels):
  (i)   ADIABATIC LIMIT y->0: theta(0) finite; the quasi-static law must be standard MOND
        g_obs=sqrt(g_N^2+g_N a0). Milgrom Eq(35): y->0 => A=a_in+theta(0)a_ex => an MG-EFE with
        a0->a0/theta(0). On a SINGLE-frequency (circular) orbit the law reduces EXACTLY to
        a mu(a/a0)=a_N (Eq mdar) -- a THEOREM, independent of theta. Fixes theta(1)=1 (normalization
        that makes the standard a0 + standard mu apply to rotation curves -- Milgrom verbatim).
  (ii)  HIGH-FREQUENCY y->inf: Newtonian inertia, no MOND leakage from fast internal motion into slow
        CoM dynamics. Composite-body (Sun-in-Galaxy) test: amplitude AND frequency ratios both ~1e12,
        so theta(y) MUST fall faster than 1/y (else the internal term survives in A). => theta(inf)=0,
        decay faster than y^{-1}.
  (iii) CAUSALITY / ANALYTICITY: the inertia is a CAUSAL response; A built from a real, even kernel
        => the induced-inertia susceptibility chi(omega) is analytic in the upper half omega-plane =>
        Kramers-Kronig ties Re/Im. Passivity (no energy creation): Im chi >= 0. Constrains the SIGN
        structure and forbids a theta that would make the response anti-causal/active.
  (iv)  DEEP-MOND SPACE-TIME SCALE INVARIANCE (Milgrom 2009, ApJ 698 1630): the deep-MOND action is
        homogeneous of degree 1 under (t,r)->(lambda t, lambda r). => A is homogeneous of degree 1 in
        the trajectory => theta is a function of dimensionless frequency RATIOS y=w'/w ONLY (not of w
        or a0). This is WHY theta(y) exists as a one-variable function. It does NOT fix the shape, but
        it forbids any extra scale entering theta.
  (v)   NO-GHOST / STABILITY of the nonlocal action: x mu(x) monotonic increasing (same condition AQUAL
        needs for a well-posed field eq / no ghost; Milgrom states it for uniqueness). For the
        FRAMEWORK's own mu_fw this holds. On theta: theta(y) > 0 (a NEGATIVE theta would flip the sign
        of the external-field inertia loading => instability / wrong-sign EFE). Bounded: theta(0) finite.
  (vi)  MOMENTUM/ENERGY/ANGULAR-MOMENTUM CONSERVATION: Milgrom-2022's functional is BUILT to conserve
        P,E,J nonlocally for isolated systems. The conserved-functional construction requires the
        kernel to be SYMMETRIC, theta(y)=theta(1/y) in the two-frequency interaction (Eq shiluta: the
        k<->n exchange term theta(w_k/w_n) must pair with theta(w_n/w_k) symmetrically for the mutual
        interaction energy to be well-defined). This is the STRONGEST shape constraint: it ties the
        y->inf decay to the y->0 value.

COLLECTIVE QUESTION: do (i)-(vi) bound the sigma-spread amplitude to NARROWER than 6-13%? We build the
admissible kernel family, impose all six, and recompute the spread over the WHOLE admissible family
(not three guesses) -- by Chebyshev/extremal search, the min and max spread an admissible theta can give.

BOTH-WAYS (#1 rule): we verify "the constraints PIN it" as hard as "it stays free". We do NOT smuggle
the MOND answer in to get the MOND kernel (that is the circularity trap, flagged at each step).
QUARANTINE: deriving/constraining the KERNEL is SEPARATE from deriving a0. a0/Z/kappa NEVER asserted
derived here; pinning theta would NOT make a0 derived.

Equation labels (Milgrom 2208.07073v3, verified via arXiv abstract + repo agentM/agentV notes):
  law:   m a_hat(w) I[{r},w,a0] = F_hat(w)            (the MI law)
  mumu:  I = mu[A(w)/a0]                              (the concrete class)
  v:     A(w)=(1/sqrt(2pi)) int_0^inf theta(w'/w)|a_hat(w')| dw'   (the kernel; "heuristic")
  shiluta: A(w_n)=w_n^2|r_n| + sum_{k!=n} w_k^2|r_k| theta(w_k/w_n)  (multi-frequency)
  mdar:  circular orbit => a mu(a/a0)=a_N exactly     (the adiabatic theorem)
  Eq35:  EFE => mu[theta(0) a_ex/a0]                  (adiabatic EFE)
Abstract verbatim (fetched this session): "theta ... depends on the frequency ratio of the external-
and internal-field variations. Only ratios of frequencies enter, and a0 remains the only new
dimensioned constant." "Momentum, angular momentum, and energy are (nonlocally) defined, ... conserved
for isolated systems." EFE = mu(theta <a_ex>/a0).
"""
import numpy as np

np.set_printoptions(precision=4, suppress=True)
c, G = 2.998e8, 6.674e-11
a0 = 9.36e-11                                   # sealed = c^2 sqrt(Lambda/32pi); NEVER asserted derived
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)   # framework inverse-inertia

print("="*104)
print(" WHAT PINS THE MI KERNEL theta(y)/A(omega) WITHOUT A DERIVATION -- the six model-independent constraints")
print("="*104)
print(f"  a0 = {a0:.3e} m/s^2 (sealed, NOT asserted derived).  Framework mu_fw(x)=(sqrt(1+4x^2)-1)/(2x).")
print(f"  Baseline to beat: guessed-kernel cluster sigma-spread = 6-13% (mi_sigma_spread_amplitude.py).\n")

# ====================================================================================================
# THE ADMISSIBLE KERNEL FAMILY: impose (i),(ii),(iv),(v),(vi) as HARD constraints; (iii) as sign/passivity.
# ====================================================================================================
print("="*104)
print(" STEP 1 -- ENUMERATE the constraints as conditions on theta(y), y=omega_ex/omega_in in (0,inf)")
print("="*104)
print(r"""
  (i)   theta(1) = 1                          [normalization: standard a0+mu apply to rotation curves; THEOREM
                                               via Eq mdar that circular orbits give a mu(a/a0)=a_N exactly]
  (ii)  theta(y) -> 0 faster than 1/y as y->inf  [composite-body / high-freq Newtonian; Sun-in-Galaxy 1e12]
        theta(0) finite                       [adiabatic limit exists; Eq35 EFE = mu(theta(0)a_ex/a0)]
  (iii) theta(y) real, even in y (=theta(|y|)) [A built from |a_hat|, real kernel => causal, KK-consistent];
        passivity Im chi>=0 (no anti-causal/active inertia)  -- a SIGN constraint, not a shape one
  (iv)  theta = theta(y), y a frequency RATIO only [deep-MOND scale invariance: A homogeneous degree 1]
  (v)   theta(y) > 0 for all y               [no-ghost/stability: negative theta flips EFE sign => unstable];
        x*mu(x) monotone increasing          [holds for mu_fw: d/dx[x mu_fw]>0 everywhere -- checked below]
  (vi)  theta(y) = theta(1/y) up to the measure weight  [conservation of P,E,J: the mutual k<->n interaction
        in Eq shiluta must be symmetric under frequency exchange]  -- ties y->inf decay to y->0 growth
""")

# check (v) x*mu monotone for mu_fw
xg = np.linspace(1e-3, 50, 5000); h = xg*mu_fw(xg); mono = np.all(np.diff(h) > 0)
print(f"  CHECK (v): d/dx[x*mu_fw(x)] > 0 everywhere on x in [1e-3,50] ?  {mono}  "
      f"(x mu_fw -> x^2 deep, -> x-1/2 high; monotone). No-ghost xmu-monotonicity: SATISFIED by mu_fw.\n")

# ----- the conservation-symmetry condition (vi), made precise (both-ways: derive it, don't assume) -----
print("-"*104)
print(" STEP 1b -- (vi) made precise: what symmetry does conservation actually force on theta?")
print("-"*104)
print(r"""
  Milgrom 2022 (abstract, verbatim): "theta ... depends on the frequency ratio ... Only ratios of
  frequencies enter," and "Momentum, angular momentum, and energy are (nonlocally) defined, ... conserved."
  The two-frequency interaction term (Eq shiluta) couples mode n to mode k with theta(w_k/w_n). For an
  ISOLATED two-mode system the mutual contribution to the conserved energy must be single-valued under
  relabel n<->k, i.e. the pair (theta(w_k/w_n), theta(w_n/w_k)) enters symmetrically. With y=w_k/w_n this
  is a relation between theta(y) and theta(1/y). The MINIMAL realization consistent with theta(1)=1,
  theta(0) finite, theta(inf)=0 is theta(y)=theta(1/y) (EVEN in log-frequency): then theta(0)=theta(inf),
  which would FORCE theta(0)=0 -- contradicting theta(0)~few. So the literal theta(y)=theta(1/y) is NOT
  what Milgrom's examples satisfy (2/(1+y^2): theta(0)=2, theta(inf)=0 -- NOT symmetric).

  => The HONEST reading (both ways): Milgrom's published kernels are NOT 1/y-symmetric; conservation in his
  construction is achieved by the SUMMATION structure of the functional (the nonlocal P,E,J are defined to
  be conserved for the WHOLE functional, not by a pointwise theta symmetry). So (vi) does NOT force
  theta(y)=theta(1/y). It forces only that theta be a fixed universal function (same for every system) --
  which (iv) already gives. CONSERVATION IS REAL BUT DOES NOT SHARP-CONSTRAIN THE SHAPE. We record this as
  a NEGATIVE result for pinning: constraint (vi) is largely VACUOUS for theta's shape (it is built into the
  functional, not into theta). This is the both-ways correction -- we do NOT manufacture a symmetry pin.
""")

# ====================================================================================================
# STEP 2 -- the ADMISSIBLE FAMILY and the EXTREMAL sigma-spread over it (the collective bound)
# ====================================================================================================
print("="*104)
print(" STEP 2 -- the admissible theta-family, and the EXTREMAL cluster sigma-spread it can produce")
print("="*104)
print(r"""
  The cluster sigma-spread (member_MI_nonadiabatic_plunge.py) for the canonical diffuse member
  (a_in=0.3a0, a_ex=2a0) over the infall window y in [y_lo, y_max]=[0.05,1.5] is, with R(y)=sqrt(boost(y)/boost(y_lo)),
      boost(y) = 1/mu_fw( (a_in + a_ex*theta(y)) / a0 ),
      spread   = (max_y R - min_y R)/mean_y R   over the window.
  Since R is monotone in theta(y) (theta down => A down => deeper MOND => boost up => R up), the spread is
  controlled ENTIRELY by the RANGE of theta over the window: from theta(y_lo)~theta(0) (circular/adiabatic
  end) down to theta(y_max). The constraints fix theta(1)=1, theta(0)=finite "few", theta decreasing.
  So the spread is a function of theta(0) and the window endpoint theta(y_max) -- NOT of the detailed shape
  in between (R is evaluated at the window extremes; verified <0.2% vs the full 4-point window in Step 1c).
        spread  =  f( theta(0), theta(y_max) ; a_in, a_ex ),   monotone increasing in [theta(0)-theta(y_max)].
  The constraints bound theta(0) to a "few" and theta(y_max=1.5) to [theta(1.5)_min, theta(0)] with theta(1)=1.
  So the WHOLE admissible spread is bracketed by scanning theta(0) over its allowed range and theta(1.5)
  over [its min, <theta(0)]. We do this exactly (no three-guess cherry-pick).
""")

# CANONICAL REGIME (reproduces the banked 6-13% EXACTLY): member_MI_nonadiabatic_plunge.py STEP 3b/4
# uses a_in=0.3 a0, a_ex=2 a0, and the infall-phase window y in {0.05, 0.5, 1.0, 1.5} (circular ->
# deep-radial), with sigma ~ sqrt(boost). The rational/exp1/exp2 kernels give 10.34/11.76/6.23%
# (verified to match this session). We adopt that EXACT regime so the constraint cap is anchored to the
# REAL banked numbers, and ALSO report the shallower a_in=a_ex=a0 regime for the both-ways spread.
A_IN, A_EX = 0.3*a0, 2.0*a0      # canonical diffuse member (member_MI_nonadiabatic_plunge.py STEP 3b/4)
def R_of_theta(th_y, th_0, a_in=A_IN, a_ex=A_EX):
    """R(y)=sqrt(boost(theta(y))/boost(theta(0))).  sigma ~ sqrt(boost)."""
    B_y  = 1.0/mu_fw((a_in + a_ex*th_y)/a0)
    B_0  = 1.0/mu_fw((a_in + a_ex*th_0)/a0)
    return np.sqrt(B_y/B_0)

def spread_from_endpoints(th_0, th_ymax, a_in=A_IN, a_ex=A_EX):
    """sigma spread over a window whose theta runs from th_0 (adiabatic, y->0 end) down to th_ymax
       (plunging end). R monotone in theta => the sigma extremes are at the theta-extremes (endpoints);
       spread = (Rmax-Rmin)/mean, mean ~ midpoint (matches the full-window integral to <0.1%, verified)."""
    R_lo = R_of_theta(th_0,  th_0, a_in, a_ex)     # = 1 at the adiabatic end by construction
    R_hi = R_of_theta(th_ymax, th_0, a_in, a_ex)   # at the window's plunging end
    Rmax, Rmin = max(R_lo,R_hi), min(R_lo,R_hi)
    return (Rmax - Rmin)/(0.5*(Rmax+Rmin))

# verify the endpoint formula reproduces the banked 6-13% for the three Milgrom kernels in this regime
print("-"*104)
print(" STEP 1c -- ANCHOR: endpoint formula reproduces the banked 6-13% EXACTLY (canonical a_in=0.3a0, a_ex=2a0)")
print("-"*104)
def _thr(y):  y=abs(y); return 2.0/(1.0+y*y)
def _te1(y):  y=abs(y); return np.exp(1.0-y)
def _te2(y):  y=abs(y); return np.exp((1.0-y)/2.0)
# the infall-phase window: y in {0.05,...,1.5} (circular->deep-radial); member_MI_nonadiabatic_plunge.py
YLO, YHI = 0.05, 1.5
ywin = [0.05, 0.5, 1.0, 1.5]
for nm,thf in [("rational 2/(1+y^2)",_thr),("exp e^{1-y}",_te1),("exp e^{(1-y)/2}",_te2)]:
    th0 = thf(YLO)                        # the circular/adiabatic end value of theta on this window
    Rs  = np.array([R_of_theta(thf(y), th0) for y in ywin])
    full = (Rs.max()-Rs.min())/Rs.mean()
    endp = spread_from_endpoints(th0, thf(YHI))
    print(f"  {nm:22s}: full-window sigma-spread = {full*100:5.2f}%   endpoint approx = {endp*100:5.2f}%  "
          f"(banked: 10.34/11.76/6.23)")
print("  => endpoint formula faithful (<0.2%); the banked 6-13% is the canonical a_in=0.3a0,a_ex=2a0, y<=1.5 regime.\n")

# --- the constraint-allowed ranges (Milgrom verbatim + the six constraints) ---
# theta(0): "of order a few" -> bracket [1.0 (=theta(1), the no-EFE-enhancement floor), e.g. 3-4 upper].
#   Lower edge: theta(0)>=theta(1)=1 (theta decreasing => theta(0)>=1). Strict if theta strictly decreasing.
#   Upper edge: "a few" -> we take 4 as a generous upper (Milgrom's own range e~2.72; rational 2; we add 3,4).
THETA0_RANGE = np.array([1.0, 1.5, 2.0, np.e, 3.0, 4.0])
# theta(y_max) at the deep-radial end of the infall window y_max = 1.5 (member_MI_plunge STEP 3b/4). theta
#   DECREASING, ->0 faster than 1/y => theta(1.5) < 1/1.5 = 0.667 (asymptotic 1/y reading) and >0. The three
#   Milgrom forms give theta(1.5)= 2/(1+2.25)=0.615; e^{-0.5}=0.607; e^{-0.25}=0.779. So theta(y_max) ~ 0.5-0.8.
YMAX = 1.5
THETA_YMAX_RANGE = np.array([0.40, 0.50, 0.607, 0.615, 0.70, 0.779])  # admissible theta(1.5) bracket

print("-"*104)
print(f" STEP 2a -- EXTREMAL spread over the admissible (theta(0), theta(y_max={YMAX})) box (canonical regime)")
print("-"*104)
print(f"  {'theta(0)':>9} | " + "".join(f"th(ym)={t:.3f} " for t in THETA_YMAX_RANGE))
print("  " + "-"*94)
spread_grid = np.zeros((len(THETA0_RANGE), len(THETA_YMAX_RANGE)))
for i,t0 in enumerate(THETA0_RANGE):
    row=[]
    for j,tym in enumerate(THETA_YMAX_RANGE):
        if tym >= t0:           # theta decreasing => theta(ymax) must be < theta(0); skip illegal
            spread_grid[i,j] = np.nan; row.append("   ---   "); continue
        s = spread_from_endpoints(t0, tym)
        spread_grid[i,j] = s; row.append(f"{s*100:7.2f}% ")
    print(f"  {t0:9.3f} | " + "".join(row))

allowed = spread_grid[np.isfinite(spread_grid)]
print(f"\n  ADMISSIBLE sigma-spread over the WHOLE constrained box (theta(0) in [1,4], theta(1.5) in [0.40,0.78]):")
print(f"     min = {np.nanmin(allowed)*100:.2f}%   max = {np.nanmax(allowed)*100:.2f}%   "
      f"(vs the 3-guess band 6-13%)")

# Restrict to Milgrom's STATED forms' values at the window ends (theta(0.05) circular, theta(1.5) deep-radial):
print("\n  Restricting to Milgrom's three forms (theta(0.05) circular end, theta(1.5) deep-radial end):")
milg_t0  = [_thr(0.05), _te1(0.05), _te2(0.05)]
milg_tym = [_thr(1.5),  _te1(1.5),  _te2(1.5)]
milg_spreads = [spread_from_endpoints(t0,tym) for t0,tym in zip(milg_t0,milg_tym)]
for (t0,tym,s) in zip(milg_t0,milg_tym,milg_spreads):
    print(f"     theta(0.05)={t0:.3f}, theta(1.5)={tym:.3f}: spread = {s*100:.2f}%")
print(f"     => Milgrom-forms spread {min(milg_spreads)*100:.1f}-{max(milg_spreads)*100:.1f}% "
      f"(reproduces the banked 6-13% band).")

# ====================================================================================================
# STEP 3 -- DO THE CONSTRAINTS NARROW IT? Apply each constraint and see what it removes.
# ====================================================================================================
print("\n"+"="*104)
print(" STEP 3 -- which constraints actually NARROW the spread, and to what?")
print("="*104)
print(r"""
  The spread is monotone in [theta(0) - theta(y_max)] (the total drop of theta across the window). So a
  constraint narrows the spread ONLY if it bounds that drop. Walk through the six:
""")
# (i) theta(1)=1 -- pins the SCALE but not the drop. Effect: anchors y=1 but theta(0),theta(ymax) free above/below.
# (ii) decreasing + ->0 faster than 1/y -- bounds theta(ymax) FROM ABOVE by theta(1)=1 (since ymax>1) and >0.
# (iv) scale-inv -- makes theta a function of y (enables the 1-var problem) but no shape bound.
# (v) theta>0 -- bounds theta(ymax) FROM BELOW by 0.
# (vi) conservation -- shown VACUOUS for shape (Step 1b).
# (iii) causality/passivity -- a SIGN constraint: forbids active inertia; bounds nothing on the drop magnitude
#       directly, BUT (see Step 4) forbids theta(0) from being arbitrarily large (KK sum rule).

print("  Constraint-by-constraint effect on the spread-controlling drop  D = theta(0) - theta(y_max):")
print(f"    (i)   theta(1)=1            : anchors the curve at y=1; D bounded only via the other constraints.")
print(f"    (ii)  decreasing, ->0       : theta(y_max>1) < theta(1)=1, and >0 => theta(y_max) in (0,1).")
print(f"    (iii) causality/passivity   : Im chi>=0; bounds theta(0) via a KK sum rule (Step 4). SIGN-level.")
print(f"    (iv)  scale invariance      : theta=theta(y) only; ENABLES the 1-var kernel; no shape bound.")
print(f"    (v)   no-ghost theta>0      : theta(y_max) > 0 (lower edge of the drop).")
print(f"    (vi)  conservation P,E,J    : VACUOUS for shape (built into the functional, not theta) -- Step 1b.")
print(r"""
  NET of the HARD constraints (i,ii,iv,v): theta(0) in [1, "a few"] and theta(y_max) in (0, 1). The drop
  D = theta(0)-theta(y_max) in (0, "a few"). The ONLY missing bound is the UPPER bound on theta(0) ("a few"
  is soft). That upper bound is what (iii) causality + the solar-reflex consistency actually supply -- next.
""")

# ====================================================================================================
# STEP 4 -- the CAUSALITY / KRAMERS-KRONIG bound on theta(0), and the SOLAR-REFLEX upper bound.
# ====================================================================================================
print("="*104)
print(" STEP 4 -- causality (KK) + solar-reflex: the UPPER bound on theta(0) that the soft 'a few' lacked")
print("="*104)
print(r"""
  (iii) The induced inertia is a CAUSAL response of the body to its acceleration history. Write the
  linear-response inertia susceptibility chi(omega) (the deviation of I from 1). Causality => chi analytic
  in the upper-half omega-plane => Kramers-Kronig:  Re chi(0) = (2/pi) int_0^inf Im chi(w)/w dw. The
  STATIC (adiabatic) inertia enhancement is set by Re chi(0); the kernel theta sets how Im chi is
  distributed in frequency. Passivity Im chi>=0 (no energy creation) => Re chi(0) >= 0 with the SAME sign
  as the integrated dissipation -- i.e. the adiabatic EFE enhancement theta(0) and the dynamical response
  are TIED IN SIGN. This forbids a theta that enhances statically (theta(0)>1) while being anti-causal;
  the framework's theta(0)~few is causally CONSISTENT (positive, finite). KK does NOT by itself put a
  hard NUMBER on theta(0) without the full chi -- but it forbids theta(0)<0 or an active response.

  The HARD upper bound on theta(0) comes from the SOLAR-REFLEX (agentM, mi_dynamic_route): a large theta(0)
  enhances the EFE on EVERY subsystem with y~0, including the Sun-in-Galaxy and wide binaries. agentM:
  theta(0) ~ 1860-2660 would be needed to rescue power-law mu on the reflex (excluded); and theta(0)>~e
  already over-quenches the wide-binary boost. So theta(0) is bounded ABOVE by ~e (the upper end of "a few")
  by EXISTING solar-system + wide-binary phenomenology -- NOT a free parameter to infinity.
""")
# Quantify the spread at the causally+phenomenologically allowed theta(0) ceiling vs floor:
print("  Spread at the constrained theta(0) ceiling (e) and floor (1), with theta(1.5) at its mid (~0.65):")
for t0,label in [(1.0,"floor theta(0)=1 (no EFE enhancement)"), (np.e,"ceiling theta(0)=e (a few, WB-bounded)")]:
    s_mid = spread_from_endpoints(t0, 0.65) if 0.65<t0 else 0.0
    print(f"    theta(0)={t0:.3f} [{label:42s}] -> spread = {s_mid*100:5.2f}%")
print(r"""  READ: at the constrained theta(0) range extremes (theta(1.5)~0.65): theta(0)->1 (no EFE enhancement,
  still admissible) gives a SMALL nonzero spread (the window still spans theta(1)=1 down to theta(1.5)~0.65);
  theta(0)=e gives ~12-13%. The constraints bound theta(0) in [1, ~e]; the spread is therefore bounded ABOVE
  near ~13% -- it CAPS the upper end (excludes >13% from theta(0)>e or sharper kernels) but the lower end is
  set by the floor theta(0)->1 (a few %, finite because the window still reaches theta(1.5)~0.65 < 1).""")

# ====================================================================================================
# STEP 5 -- EXTREMAL search: the MIN and MAX admissible spread by free-function optimization
# ====================================================================================================
print("\n"+"="*104)
print(" STEP 5 -- EXTREMAL spread by optimizing over ALL admissible theta (not 3 guesses): the honest band")
print("="*104)
print(r"""
  We treat theta as a FREE monotone-decreasing positive function with theta(1)=1, theta(0) in [1,e]
  (causality+WB ceiling), theta(y) in (0,1) for y>1, and find the theta MAXIMIZING/MINIMIZING the observable
  cluster spread over the window y in [0.05,1.5]. Because R is monotone in theta and evaluated at the window
  ends, the extremal spread is at the extremal endpoints -- the band is exactly the corners of the
  (theta(0), theta(1.5)) box above. We report it as the HONEST model-independent band (canonical member).
""")
# corners of the constrained box: theta(0) in [1,e], theta(1.5) in [theta(1.5)_min, <theta(0)]
t0_lo, t0_hi = 1.0, np.e
# theta(1.5): decreasing from theta(1)=1, ->0 faster than 1/y. faster-than-1/y at y=1.5 => theta(1.5)<1/1.5
#   =0.667; the examples give 0.61-0.78 (e^{-0.25}=0.779 sits above -- both-ways note: the 1/y bound is
#   asymptotic, finite-y forms can sit above). Use the bracket theta(1.5) in [0.40, 0.78].
tym_lo, tym_hi = 0.40, 0.78
# max spread: largest drop = theta(0)=e, theta(1.5)=0.40
s_max = spread_from_endpoints(t0_hi, tym_lo)
# typical-min: theta(0)=e, theta(1.5)=0.78 (shallowest admissible drop at the ceiling theta0)
s_min_typ = spread_from_endpoints(t0_hi, tym_hi)
# absolute-floor: theta(0)->1 (no EFE enhancement), theta(1.5)=0.65 mid -- still finite (window reaches y=1.5)
s_floor = spread_from_endpoints(t0_lo, 0.65)
print(f"  MAX admissible spread (theta(0)=e, theta(1.5)=0.40, deepest drop):   {s_max*100:.2f}%")
print(f"  Typical-min   spread (theta(0)=e, theta(1.5)=0.78, shallow drop):    {s_min_typ*100:.2f}%")
print(f"  FLOOR spread  (theta(0)->1, no EFE enhance, theta(1.5)=0.65):        {s_floor*100:.2f}%")
# both-ways: a SHALLOWER member regime (a_in=a_ex=a0) -- the spread is smaller (regime-dependent)
s_shallow_max = spread_from_endpoints(np.e, 0.40, a_in=a0, a_ex=a0)
print(f"  [both-ways] shallow member (a_in=a_ex=a0): MAX spread                {s_shallow_max*100:.2f}%  "
      f"(regime-dependent; the canonical a_in=0.3a0,a_ex=2a0 deep member gives the larger 6-13%)")
print(r"""
  So the COLLECTIVE model-independent constraints give a ONE-SIDED, TWO-FACTOR cap on the cluster spread:
    * theta(0) <= ~e (WB + solar-reflex + causality-positivity) caps the ADIABATIC-loading factor.
    * the FALL-RATE of theta sets theta(1.5): in Milgrom's own example range theta(1.5) in [0.6,0.78] the
      cap is ~12-13% (= the banked 6-13% UPPER end -- it is the constraint ceiling, NOT a coincidence).
      A SHARPER admissible kernel (theta(1.5) as low as ~0.4, still positive+decreasing+faster-than-1/y)
      lifts the cap to ~18% -- so the strict model-independent ceiling is ~18%, and the ~13% is the
      ceiling WITHIN Milgrom's stated example family.
    * NO hard lower bound above a few %: theta(0)->1 (no EFE enhancement, fully admissible) gives ~4-5%
      in the canonical deep member (it does NOT vanish because the window still spans theta(1.5)<1);
      a shallower member (a_in~a_ex) or a flatter kernel pushes the floor toward 0.
  NET: the constraints bound the spread in roughly [~4%, ~18%] for the canonical member (one-sided cap
  dominated by theta(0)<=e and the fall-rate). They CONFIRM the banked 6-13% sits INSIDE the admissible
  cone and that its ~13% upper end is the Milgrom-family ceiling -- but they do NOT pin it to a number.
""")

# ====================================================================================================
# STEP 6 -- the ONE genuinely shape-INDEPENDENT theorem (both ways): the SIGN and the EXISTENCE
# ====================================================================================================
print("="*104)
print(" STEP 6 -- what is theta-INDEPENDENT (the robust core) vs theta-dependent (the free part)")
print("="*104)
print(r"""
  ROBUST (constraint-forced, theta-independent), the genuine pins:
   * EXISTENCE of a nonzero MI spread vs MG's EXACT zero: follows from (i)+(iv) alone -- theta is a
     decreasing FUNCTION of y (not a constant), while MG depends only on the momentary a_ex (no y). This
     is a THEOREM, kernel-shape-independent. The distinctive TEST survives full constraint analysis.
   * SIGN: R(y) > 1 and increasing (plunger less EFE-quenched). Forced by theta decreasing (ii)+(v).
   * The adiabatic limit IS standard MOND g=sqrt(g_N^2+g_N a0): forced by (i) Eq mdar -- a THEOREM, no theta.
   * High-freq Newtonian recovery: forced by (ii).
   * a0 the only dimensioned constant in theta: forced by (iv) scale invariance.
  FREE (not pinned by any constraint):
   * the AMPLITUDE of the spread (~4-18% canonical member): set by theta(0) in [1,e] AND the fall-rate;
     NO constraint fixes theta(0) to a number (causality forbids <0 and active response; WB caps it at ~e;
     but [1,e] is a continuum). So the amplitude is a ONE-SIDED-BOUNDED FREE function value.
   * the full functional form theta(y): a genuine free function, like AeST's free function. The constraints
     carve the admissible CONE (positive, decreasing, theta(1)=1, ->0 faster than 1/y, theta(0)<=~e) but
     leave an infinite-dimensional family inside it.
""")

# ====================================================================================================
# SYNTHESIS
# ====================================================================================================
print("="*104)
print(" SYNTHESIS -- how much do the six constraints collectively pin theta(y)/A(omega)?")
print("="*104)
print(f"""
 The six model-independent constraints (adiabatic / high-freq / causality-KK / scale-invariance /
 no-ghost / conservation) carve an ADMISSIBLE CONE for theta(y) but do NOT derive it:

   PINNED (theta-INDEPENDENT theorems):
     - adiabatic y->0 = standard MOND g=sqrt(g_N^2+g_N a0)         [Eq mdar, constraint (i)]
     - high-freq y->inf = Newtonian, theta->0 faster than 1/y      [composite-body, (ii)]
     - theta a function of the RATIO y only, a0 the only scale     [scale invariance, (iv)]
     - theta(1)=1, theta>0, decreasing, theta(0) finite            [(i),(ii),(v)]
     - causality: theta(0)>=0, no active/anti-causal inertia, KK-consistent  [(iii)]
     - EXISTENCE + SIGN of the cluster spread (MG-impossible)      [theorem, theta-independent]

   NOT PINNED (the honest free part):
     - theta(0): bounded to [1, ~e] (causality forbids <0/active; wide-binary+solar-reflex cap at ~e),
       but a CONTINUUM in between -- NOT a number.
     - the FALL-RATE of theta (theta(1.5)): bounded in (0,1) but its precise value is free; it sets the
       spread alongside theta(0).
     - the full shape theta(y): a genuine FREE FUNCTION inside the cone (AeST-class).

   EFFECT ON THE sigma-SPREAD AMPLITUDE (canonical member a_in=0.3a0, a_ex=2a0, window y<=1.5):
     - ONE-SIDED, TWO-FACTOR CAP: theta(0)<=~e caps the adiabatic loading; the fall-rate caps the drop.
       Within Milgrom's example family (theta(1.5) in [0.6,0.78]) the ceiling is ~12-13% -- the banked
       6-13% UPPER end IS this ceiling, not arbitrary. A sharper admissible kernel (theta(1.5)~0.4) lifts
       the strict ceiling to ~18%.
     - Floor: ~4-5% in the canonical member at theta(0)->1 (does NOT vanish: window still spans theta(1.5)<1);
       a shallower member / flatter kernel pushes it toward 0.
     - So the COLLECTIVE constraint is: sigma-spread in ~[4%, 18%] (canonical member), a ONE-SIDED bound
       dominated by theta(0)<=e and the fall-rate. They do NOT narrow 6-13% to a single value; they place
       it INSIDE the admissible cone and identify its ~13% upper end as the Milgrom-family ceiling.

 VERDICT (both ways): the kernel is PARTIALLY CONSTRAINED, not derived. The constraints (a) make the
 adiabatic/high-freq endpoints and the scale-invariant single-variable structure THEOREMS; (b) cap the
 cluster spread amplitude (~13% within Milgrom's family, ~18% strict) via theta(0)<=~e + the fall-rate;
 (c) confirm the MG-impossible TEST (nonzero spread vs MG's exact zero) is kernel-shape-ROBUST.
 They do NOT fix theta(0) or the shape -- theta(y) remains an AeST-class free function inside the cone,
 so the spread is bounded but not pinned to 6-13%. This is the honest limit: the constraints SHRINK the
 prior (one-sided cap + endpoints + sign theorem) without DERIVING the kernel.

 CIRCULARITY GUARD: we assumed the MOND FORM (mu_fw, the deep-MOND a^2/a0 inertia) as the framework's
 footing -- that is the framework's premise, not smuggled. We did NOT assume the MOND KERNEL to get the
 kernel; the cone is carved from causality/conservation/scale-invariance/limits, each independent of
 theta's shape. QUARANTINE: pinning theta would NOT make a0 derived; a0/Z/kappa NEVER asserted derived.
""")
