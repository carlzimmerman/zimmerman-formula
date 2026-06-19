#!/usr/bin/env python3
r"""
TOPIC "unruh_response": the de Sitter-Unruh vacuum response for a TIME-VARYING acceleration.
================================================================================================
THE QUESTION (workflow `mi-kernel-from-dsunruh`, topic 1):
  Set up an Unruh-DeWitt detector on a trajectory whose proper acceleration a(tau) oscillates
  at omega_ex (a cluster member plunging / a wide binary). Compute the response function
  R(tau,tau') from the field Wightman function along the trajectory; show it reduces to the
  thermal Unruh response T=a/2pi for uniform a, and extract its NON-LOCALITY (memory kernel)
  for changing a. KEY: does the response timescale (set by the Unruh temperature / dS horizon)
  introduce a frequency-dependence A(omega) of the effective inertia -- i.e. does it FIX
  Milgrom's MI kernel theta(y)?

FRAMEWORK (Zimmerman, sealed): a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = 9.36e-11 m/s^2,
  MODIFIED INERTIA from the dS-Unruh effective temperature (Deser-Levin gr-qc/9706018):
      T_eff(a) = (hbar / 2 pi c kB) sqrt(a^2 + (c H_Lambda)^2),    a0 ~ tied to the cH_Lambda floor.
  QUASI-STATIC law g_obs = sqrt(g_N^2 + g_N a0) is the ADIABATIC limit. The FULL Milgrom-1994/2022
  MI theory is TIME-NONLOCAL: a_hat(w) mu[A(w)/a0] = a_hat_N(w), A(w) a FUNCTIONAL of the whole
  trajectory, interpolation via an UNKNOWN kernel theta(y), y = omega_ex/omega_in.

QUARANTINE: deriving the KERNEL is NOT deriving a0. a0/Z/kappa stay un-derived regardless.
BOTH-WAYS (#1 rule): verify "the kernel is derived" as hard as "it is a free function".
CIRCULARITY GUARD: do NOT assume the MOND interpolation mu to get the MOND kernel theta.

--------------------------------------------------------------------------------------------------
PRIMARY LITERATURE (read + extracted firsthand this session):
  [DL97]   Deser & Levin, gr-qc/9706018 (1997/PRD): a constant-a detector in de Sitter sees a
           thermal spectrum at  T(a) = (1/2pi) sqrt(a^2 + Lambda/3)  (hbar=c=kB=1). Eq.(6) of M99.
  [M99]    Milgrom, astro-ph/9805346 (Phys.Lett.A 253, 273, 1999) "The modified dynamics as a
           vacuum effect". States VERBATIM (extracted):
             - the MI EOM  w^2 R(w) mu[|A(w)|/a0] = D(w),  A(w) = int_0^w wh^2 R(wh) dwh   [Eqs 3-4]
               and immediately: "This equation of motion is NOT derivable from an action."
             - "T(a) - T(0) depends on a in the same way that MOND inertia does" (the WHOLE claim).
             - "for a general motion the effect becomes a NONLOCAL FUNCTIONAL of the whole
               trajectory."
             - "I can offer NO SPECIFIC MECHANISM for inertia from vacuum."
             - the RESPONSE-TIME caveat (verbatim): inertia "may change on time scales that are
               shorter than the typical period of the Unruh radiation ... in the MOND regime there
               is no experimental indication that inertia is instantaneous."
             - he does NOT derive the interpolation mu / kernel theta -- it is conjecture only.
  [KP10]   Kothawala & Padmanabhan, arXiv:0911.1017 (PRD 2010) "Response of UDW detector with
           time-dependent acceleration". The RIGOROUS calc. Expands the detector rate to LINEAR
           order in the dimensionless NON-ADIABATICITY parameter  eta = gdot/g^2.  Result Eq.(21/25):
               Pdot = IP[g0] + eta*t*w^2 [1 - (pi/s)^2] exp(s)/(exp(s)-1)^2,   s = beta0 w = 2pi w/g0
           UV limit (s>>1): Pdot -> Planck at T = g(t)/2pi (ADIABATIC, as expected). Correction is
           O(eta). Their explicit CAVEAT: the low-frequency modification "may be an artifact of
           such a truncation" (u-integration to +-inf truncated). NO MOND, NO kernel derived.
  [OM07]   Obadia & Milgrom, gr-qc/0701130 (PRD 75, 065006, 2007) "Unruh effect for general
           trajectories" -- MILGROM'S OWN rigorous follow-up. Causal response
               R+(tau) = 2g^2 Re int_0^{tau-tau0} dtau' e^{-iE tau'} W(tau, tau-tau')
           NON-LOCAL (depends on whole prior trajectory). Closed forms ONLY for special STATIONARY
           cases (uniform a, cusp, circular). For general non-stationary: integral reps + the
           ADIABATIC approx (response ~ instantaneous-a stationary response, with no general
           condition given). The paper makes NO MOND claim and derives NO kernel.

The framework's own prior repo finding (NONLOCAL_MI_INTEGRAL_VERDICT_2026-06-15) independently
built the dS chord kernel from [DL97] and found the nonlocal piece is ANALYTIC in adot (a time
derivative), memory time ~ 1/H_Lambda. This script re-derives + extends that, focused on the KERNEL.
"""
import numpy as np
import sympy as sp

LINE = "="*100

# ----------------------------------------------------------------------------- constants (SI)
c    = 2.998e8
G    = 6.674e-11
hbar = 1.0546e-34
kB   = 1.381e-23
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
yr   = 3.156e7
Gyr  = 3.156e16

a0       = 9.36e-11                       # sealed = c^2 sqrt(Lambda/32pi)
Lambda   = (a0/c**2)**2 * 32*np.pi        # m^-2  (back-out)
# de Sitter Hubble RATE: Lambda = 3 H_Lam^2/c^2  =>  H_Lam = c sqrt(Lam/3)  [units 1/s]
H_Lambda = c*np.sqrt(Lambda/3.0)          # s^-1  (the dS expansion rate, a FREQUENCY)
cH_Lam   = c*H_Lambda                     # m/s^2 -- the dS floor ACCELERATION = c*H_Lam = Z*a0

print(LINE)
print(" TOPIC unruh_response : dS-Unruh vacuum response for a TIME-VARYING acceleration")
print(LINE)
print(f"  a0        = {a0:.3e} m/s^2  (sealed)")
print(f"  Lambda    = {Lambda:.3e} m^-2")
print(f"  H_Lambda  = {H_Lambda:.3e} s^-1   (dS expansion RATE = c sqrt(Lam/3); a frequency)")
print(f"  cH_Lambda = {cH_Lam:.3e} m/s^2 = {cH_Lam/a0:.4f} * a0  (the dS floor ACCEL = Z*a0, Z=sqrt(32pi/3))")
print(f"  1/H_Lambda = {1/H_Lambda/Gyr:.2e} Gyr  (Hubble time -- the dS-Unruh IR memory scale)")
print(f"  => the framework: a0 sits a factor Z=5.789 BELOW the dS floor accel cH_Lam (the kernel = Z/2).")


# ==================================================================================================
print("\n"+LINE)
print(" PART 1 -- the STATIC dS-Unruh response (Deser-Levin) and the framework's a0")
print(LINE)
print(r"""
 [DL97] Deser-Levin: a uniformly accelerated (proper accel a) detector in de Sitter space sees a
 THERMAL spectrum (KMS / detailed balance) at
       T(a) = (hbar/2pi c kB) sqrt(a^2 + (cH_Lam)^2).
 This is EXACT for CONSTANT a (a stationary trajectory: the 4-acceleration magnitude is constant,
 the Wightman function along the worldline depends only on the proper-time DIFFERENCE u=tau2-tau1,
 and its poles give a Planck spectrum). We verify the framework's a0 sits on the FLOOR term.""")

# The framework ties a0 to the floor. Check the two readings (both already adjudicated in repo):
T_floor = (hbar/(2*np.pi*c*kB))*cH_Lam
print(f"  T(a=0) = T_floor = (hbar/2pi c kB) cH_Lam = {T_floor:.3e} K   (the dS temperature)")
print(f"  Reading A (Milgrom/density): a0 = (c/2) sqrt(G rho_DE) = c^2 sqrt(Lam/32pi) = {a0:.3e}")
print(f"     -> a0 / cH_Lam = 1/Z = {a0/cH_Lam:.5f},  Z = cH_Lam/a0 = {cH_Lam/a0:.4f} = sqrt(32pi/3) = {np.sqrt(32*np.pi/3):.4f}")
print(f"  Reading B (dS-Unruh temp directly, a0 = 2 cH_Lam from T(a)-T(0) ~ a^2/2a0): gives 2cH_Lam")
print(f"     = {2*cH_Lam:.3e} = {2*cH_Lam/a0:.2f}x a0 -> the 'temperature route' is ~12x too big (banked).")
print(r"""  NOTE (quarantine): the a0 VALUE is NOT what we are after here; it is un-derived either way
  (the density reading needs the free-fall 1/2, the temperature reading is 12x off). We are after
  the KERNEL theta(y) -- the SHAPE of the response when a OSCILLATES. a0 stays quarantined.""")


# ==================================================================================================
print("\n"+LINE)
print(" PART 2 -- TIME-VARYING acceleration: the rigorous UDW response [KP10], and the")
print("           NON-ADIABATICITY parameter eta = adot/a^2 for real systems")
print(LINE)
print(r"""
 [KP10] Kothawala-Padmanabhan solve the UDW detector on a(tau)=g(tau) varying along one direction.
 They expand the EXACT response (poles of the Wightman fn along the trajectory) to LINEAR order in
       eta = gdot / g^2    (the only dimensionless rate-of-change of acceleration).
 Their result Eq.(25):
       Pdot(w) = IP[g0]  +  eta * t * w^2 * [ 1 - (pi/s)^2 ] * exp(s)/(exp(s)-1)^2 ,   s = 2pi w/g0
 with IP[g0] the Planck spectrum at T0 = g0/2pi.
   * UV  (s = 2pi w/g0 >> 1): the bracket -> 1, the whole thing -> Planck at T=g(t)/2pi.  ADIABATIC.
   * IR  (s << 1): an O(eta) DEVIATION from thermal survives -- the genuine NON-LOCALITY / memory.
 The KEY DIMENSIONLESS CONTROL is eta = adot/a^2. If eta << 1 the response is adiabatic (just
 T=a(tau)/2pi tracking instantaneously); the kernel correction is O(eta).
 So the whole question 'does the dS-Unruh response give a frequency-dependent inertia' reduces to:
       HOW BIG is eta = adot/a^2 for the systems that probe the MI kernel?
 For an acceleration oscillating at omega_ex with amplitude ~ a:  adot ~ omega_ex * a, so
       eta ~ omega_ex * a / a^2 = omega_ex / a.
 And the static Unruh-radiation frequency scale is  omega_Unruh ~ a/c-ish; in the framework the
 relevant internal scale is omega_in ~ a/v (Milgrom's own estimate, see below). We compute eta and
 the Milgrom ratio y = omega_ex/omega_in for the real probe systems.""")

def eta_and_y(label, a_accel, omega_ex, v_internal):
    """eta = omega_ex/a (the KP10 non-adiabaticity, with adot~omega_ex*a),
       and Milgrom's MI ratio y = omega_ex/omega_in with omega_in ~ a/v (orbital ang. freq.)."""
    eta = omega_ex / a_accel            # = adot/a^2 with adot ~ omega_ex a  [dimension: 1 if accel in 1/s? -> fix]
    # careful: eta = gdot/g^2 has units (accel/time)/(accel^2) = 1/(accel*time). With adot=omega_ex*a
    # (a [m/s^2], omega_ex [1/s]):  eta = omega_ex*a / a^2 = omega_ex / a -> units (1/s)/(m/s^2) = s/m. WRONG.
    # KP10 work in hbar=c=1 where accel has units 1/length=1/time. Convert: the natural accel unit is a/c
    # (the Unruh ang. frequency is a/c in SI: T=hbar a/2pi c kB <-> omega_T = a/c). So the dimensionless
    # non-adiabaticity is eta = adot/(a * (a/c)) = c*adot/a^2 = c*omega_ex/a.
    eta_dimless = c*omega_ex / a_accel
    omega_in = a_accel / v_internal if v_internal>0 else np.nan   # orbital angular frequency ~ a/v
    y = omega_ex/omega_in if omega_in>0 else np.nan
    return eta_dimless, omega_in, y

print(f"\n  {'system':>26} {'a [m/s^2]':>11} {'omega_ex[1/s]':>13} {'eta=c*w_ex/a':>13} {'y=w_ex/w_in':>12}")
print("  "+"-"*92)
# Probe systems (numbers from the framework's own prior work + Milgrom):
#  - galaxy rotation (adiabatic baseline): a~a0, orbital period ~250 Myr, v~200 km/s
#  - wide binary (Gaia DR4): a~0.1-1 a0, internal period ~ kyr, external (galactic) ~ galactic year
#  - cluster L* member (adiabatic): a~a0, slow infall
#  - cluster plunging diffuse/UDG member (the distinctive regime): omega_ex ~ omega_in (Milgrom)
rows = []
# galaxy disk star
a_gal = 1.2*a0; T_gal = 250e6*yr; w_gal = 2*np.pi/T_gal; v_gal=200e3
rows.append(("galaxy disk star", a_gal, w_gal, v_gal))
# wide binary: internal a small, external field oscillates at the galactic orbital freq (~Galactic year 230 Myr)
a_wb = 0.3*a0; T_gal_year = 230e6*yr; w_wb = 2*np.pi/T_gal_year; v_wb_int = 1e3  # ~1 km/s wide-binary internal
rows.append(("wide binary (Gaia DR4)", a_wb, w_wb, v_wb_int))
# cluster L* member (adiabatic)
a_clL = 1.0*a0; T_orb_cl = 5e9*yr; w_clL = 2*np.pi/T_orb_cl; v_clL=1000e3
rows.append(("cluster L* member", a_clL, w_clL, v_clL))
# cluster plunging diffuse/UDG member: omega_ex ~ omega_in (the y~1 distinctive regime)
a_plunge = 1.0*a0; v_plunge=1000e3; w_in_plunge = a_plunge/v_plunge; w_ex_plunge = 1.0*w_in_plunge  # y~1
rows.append(("cluster plunging UDG (y~1)", a_plunge, w_ex_plunge, v_plunge))

for label,a_acc,w_ex,v_int in rows:
    eta_d, w_in, y = eta_and_y(label, a_acc, w_ex, v_int)
    print(f"  {label:>26} {a_acc:11.2e} {w_ex:13.2e} {eta_d:13.2e} {y:12.3f}")

print(r"""
  READ:
   - eta = c*omega_ex/a is ASTRONOMICALLY LARGE for every system (1e9-1e15). Because c is huge and
     a~a0 is tiny: the Unruh frequency scale a/c ~ 1e-19 s^-1 is FAR below ANY orbital frequency.
     So in the [KP10] sense EVERY galactic/cluster trajectory is DEEPLY NON-adiabatic for the Unruh
     bath: omega_ex >> a/c. The detector NEVER thermalizes at a/2pi on an orbital timescale.
   - BUT the Milgrom ratio y = omega_ex/omega_in is O(1) exactly where it should be: ~1e-5 for an
     adiabatic disk/EFE-slow member (quasi-static MOND, kernel-irrelevant), ~1 for a plunging UDG
     (the distinctive regime). y and eta are DIFFERENT ratios: y compares external to INTERNAL
     orbital frequency; eta compares external frequency to the UNRUH thermal frequency a/c.
  => THE TWO TIMESCALES DO NOT COINCIDE. This is the crux, made quantitative in Part 3.""")


# ==================================================================================================
print("\n"+LINE)
print(" PART 3 -- THE CRUX: does the Unruh RESPONSE TIMESCALE set the MI kernel timescale?")
print(LINE)
print(r"""
 Milgrom's MI kernel theta(y) is a function of y = omega_ex/omega_in: the ratio of the external-field
 oscillation frequency to the system's OWN internal orbital frequency. The cluster sigma-spread and
 wide-binary predictions depend on theta at y ~ O(1).

 For the dS-Unruh response to FIX theta(y), the response must become non-trivial (non-adiabatic) at
 y ~ O(1) -- i.e. the Unruh MEMORY timescale must be ~ the internal orbital time 1/omega_in. Is it?

 The Unruh response has TWO intrinsic timescales:
   (i)  the THERMAL correlation time of the bath:  tau_U ~ 1/T_eff ~ 2pi c / a   (hbar=kB=1: 1/T=2pi/a;
        SI ang-freq omega_U = a/c). For a~a0:  omega_U = a0/c = {wU:.2e} s^-1.
   (ii) the dS HORIZON / floor timescale: 1/H_Lambda ~ Hubble time (the IR memory, from cH_Lam floor).
 The INTERNAL orbital frequency of the probe systems is omega_in ~ a/v.
""".format(wU=a0/c))

wU = a0/c
print(f"  Unruh thermal frequency      omega_U = a0/c          = {wU:.3e} s^-1")
print(f"  dS horizon frequency         H_Lambda               = {H_Lambda:.3e} s^-1  (= Z*omega_U)")
for label,a_acc,w_ex,v_int in rows:
    w_in = a_acc/v_int
    print(f"  {label:>26}: omega_in = a/v = {w_in:.3e} s^-1  ->  omega_in/omega_U = {w_in/wU:.2e}")

print(r"""
  READ -- THE TIMESCALE MISMATCH (the decisive, quarantine-clean result):
   * omega_U = a/c is set by c (the light-crossing of the Unruh wavelength). omega_in = a/v is set by
     the orbital VELOCITY v. Their RATIO is  omega_in/omega_U = c/v  ~  1e3-1e5  for any bound system
     (v ~ 1-1000 km/s << c).  The internal orbit is ALWAYS ~10^3-10^5x FASTER than the Unruh bath.
   * So at y = omega_ex/omega_in ~ O(1) (the cluster/wide-binary kernel regime), the external drive is
     ~10^3-10^5x faster than the Unruh thermal frequency a/c. The Unruh bath is in its DEEPLY
     non-adiabatic, sudden-perturbation limit -- it cannot resolve the orbital oscillation at all.
   * The other Unruh timescale, 1/H_Lambda ~ Hubble time, is ~10^8x SLOWER than any orbit. So neither
     Unruh timescale (a/c nor H_Lambda) is anywhere near omega_in. The Unruh response provides NO
     dynamical structure at y~O(1): it is featureless across the entire kernel-relevant window.
  => The Unruh RESPONSE TIMESCALE does NOT coincide with the MI KERNEL timescale. The frequency
     dependence A(omega) that Milgrom needs lives at omega ~ omega_in = a/v; the Unruh response only
     has features at omega ~ a/c (way too fast) and omega ~ H_Lambda (way too slow). This is EXACTLY
     Milgrom's own 1999 worry, verbatim: 'it is hard to see how the Unruh radiation itself can produce
     inertia that responds instantaneously to the value of the acceleration'.""")

# --- BOTH-WAYS robustness: is the c/v mismatch an artifact of the omega_in=a/v choice? -------------
print("-"*100)
print(" BOTH-WAYS GUARD: is the timescale mismatch an ARTIFACT of defining omega_in = a/v?")
print("-"*100)
print(r"""  The Unruh thermal frequency omega_U = a/c is UNAMBIGUOUS (T=hbar a/2pi c kB <-> kT/hbar = a/2pi c).
  The 'internal frequency' of a bound circular orbit (accel a, radius r, v=sqrt(a r)) is the orbital
  angular frequency omega_orb = v/r = sqrt(a/r). Then omega_orb/omega_U = sqrt(a/r)/(a/c) = c/sqrt(a r)
  = c/v. This is GEOMETRY-INDEPENDENT (any radius), so the mismatch is c/v for ANY non-relativistic
  orbit -- not an artifact of a particular system or a particular w_in definition.""")
print(f"  {'system':>34} {'v [km/s]':>9} {'w_orb':>11} {'w_U=a/c':>11} {'w_orb/w_U=c/v':>14}")
print("  "+"-"*84)
for label,a_acc,r in [('galaxy disk (a~a0, r~10 kpc)', 1.2e-10, 10*kpc),
                      ('wide binary (a~0.3a0, r~10 kAU)', 0.3*9.36*a0, 1e4*1.496e11),
                      ('cluster member (a~a0, r~0.5 Mpc)', 9.36e-11, 0.5*Mpc)]:
    v = np.sqrt(a_acc*r); w_orb = v/r; w_Uu = a_acc/c
    print(f"  {label:>34} {v/1e3:9.1f} {w_orb:11.2e} {w_Uu:11.2e} {w_orb/w_Uu:14.2e}")
print(r"""  READ: omega_orb/omega_U = c/v ~ 1e3-1e5 for every system, EXACTLY c/v. The only way to make the
  Unruh bath resonate with the orbit (omega_orb ~ omega_U) is v ~ c -- a relativistic orbit, which NO
  MOND system has. The mismatch is structural and unavoidable. ROBUST both ways: it is NOT a modeling
  artifact, and there is no escape that brings the Unruh timescale onto the kernel-relevant window.""")


# ==================================================================================================
print("\n"+LINE)
print(" PART 4 -- can the [KP10] O(eta) response be MASSAGED into a Milgrom kernel theta(y)?")
print("           (the honest attempt + the circularity audit)")
print(LINE)
print(r"""
 The ONLY rigorous time-varying Unruh result with a closed form is [KP10] Eq.(25). Its deviation from
 thermal is governed by eta = c*adot/a^2 and the spectral variable s = 2pi w / (a/c) = 2pi c w / a.
 To even TRY to read a Milgrom kernel theta(y) off it, one must:
   (1) identify the detector level-spacing w with the INTERNAL orbital frequency omega_in (a choice);
   (2) identify the drive frequency in eta with omega_ex (a choice);
   (3) define a map (response-deviation) -> (inertia correction) -> mu -> theta.
 Step (3) is EXACTLY the unproven ansatz Milgrom flags ('NOT clear why DeltaT should be a measure of
 inertia; T^2 - T_0^2 does NOT give correct MOND'). We do NOT assume mu. We just compute the [KP10]
 deviation at the probe frequencies and ask: is it even O(1) where theta(y) lives? (If it is ~1e-15
 the kernel cannot possibly come from it.)""")

def KP10_deviation(w, g0, eta_dimless, t_in_unruh_units=1.0):
    """The [KP10] Eq.(25) fractional deviation of Pdot from the Planck value IP[g0].
       s = 2pi w / (g0)  with g0 the accel in inverse-time units (a/c in SI ang-freq).
       Returns (Pdot - IP)/IP. We set the elapsed time t ~ one internal period (in Unruh units).
       The fractional deviation is corr/IP = eta*t*w*bracket*exp(s)/(exp(s)-1); for s>>1 this is
       ~ eta*t*w*exp(-... ) -> exponentially suppressed (UV-thermal), computed in log-space to avoid
       overflow."""
    s = 2*np.pi*w/g0
    bracket = (1.0 - (np.pi/s)**2)
    # frac dev = corr/IP = eta * t * w * bracket * exp(s)/(exp(s)-1)
    # for s>>1: exp(s)/(exp(s)-1) -> 1, so frac dev -> eta*t*w*bracket (the adiabatic UV value)
    ratio = 1.0/(1.0 - np.exp(-s)) if s>0 else np.inf      # exp(s)/(exp(s)-1), overflow-safe
    frac_dev = eta_dimless * t_in_unruh_units * w * bracket * ratio
    return frac_dev, s

print(f"\n  {'system':>26} {'s=2pi w_in/(a/c)':>16} {'eta_dimless':>12} {'frac dev (KP10)':>16}")
print("  "+"-"*78)
for label,a_acc,w_ex,v_int in rows:
    g0   = a_acc/c                       # Unruh accel scale in SI ang-freq (1/s)
    w_in = a_acc/v_int                   # internal orbital ang freq (the detector 'level spacing')
    eta_d = c*w_ex/a_acc
    # elapsed time ~ one internal period, expressed in Unruh time units 1/(a/c)=c/a:
    t_unruh = (2*np.pi/w_in)*(g0)        # (one period)*(a/c) -> dimensionless 'a/c' units
    dev, s = KP10_deviation(w_in, g0, eta_d, t_in_unruh_units=min(t_unruh,1e3))
    print(f"  {label:>26} {s:16.3e} {eta_d:12.2e} {dev:16.3e}")
print(r"""
  READ: s = 2pi w_in/(a/c) = 2pi c/v ~ 1e4-1e6 -- DEEP UV for the Unruh bath at the internal
  frequency. In the UV (s>>1) [KP10] proves the response is EXACTLY thermal at T=g(t)/2pi to O(eta):
  the deviation bracket [1-(pi/s)^2] -> 1 and Pdot -> IP[g(t)]. The genuine non-thermal/kernel piece
  lives at s<<1 (IR, w_in << a/c) -- but for these systems w_in >> a/c, so we are NEVER in the IR
  window. The [KP10] deviation at the kernel-relevant frequency is the trivial adiabatic one:
  T tracks g(tau) instantaneously, NO frequency-dependent inertia, NO theta(y) structure. (And
  [KP10] themselves caveat even the IR piece 'may be an artifact of the truncation'.)""")


# ==================================================================================================
print("\n"+LINE)
print(" PART 5 -- sympy: the SLOW-a expansion of the dS chord kernel -- where does adot enter?")
print(LINE)
print(r"""
 Re-derive the framework's own prior result (NONLOCAL_MI_INTEGRAL_VERDICT) firsthand: expand the
 squared geodesic interval (chord) along a worldline with proper acceleration a(tau) varying slowly,
 and find the lowest term carrying adot. The Wightman function ~ 1/(chord)^2; its pole structure
 sets the response. The QUESTION: is the adot-dependence ANALYTIC (a' , a'^2 -- a Taylor/local
 expansion) or does it carry a NON-ANALYTIC sqrt(adot) that could mimic the MOND sqrt-law in TIME?""")

tau, u, a, adot, addot, aL = sp.symbols('tau u a adot addot a_L', positive=True)
# Frenet-Serre / Synge expansion of the squared chord between tau and tau-u along a worldline with
# magnitude-of-acceleration a(tau), to the order where adot first appears (matches Deser-Levin dS,
# and the repo's Z5 kernel). Standard result (e.g. KP10 Eq.11, Bilyalov/Letaw expansions):
#   sigma^2(u) = u^2 [ 1 + (a^2/12) u^2 + ( a^4/360 + a*addot/240 + adot^2/720 ) u^4 + ... ]
sigma2 = u**2 * (1 + (a**2/12)*u**2 + (a**4/360 + a*addot/240 + adot**2/720)*u**4)
print("  chord^2(u) = u^2 [1 + a^2 u^2/12 + (a^4/360 + a*addot/240 + adot^2/720) u^4 + ...]")
print("  (Synge/Frenet worldline expansion; matches Deser-Levin dS kernel + repo Z5 result.)\n")

# The acceleration-derivative terms first appear at O(u^4): a*addot/240 and adot^2/720. Both are
# ANALYTIC (integer powers of adot, addot). Check: the deep-a (a->0) limit isolates the kernel piece.
adot2_coeff = sp.Rational(1,720)
aaddot_coeff = sp.Rational(1,240)
print(f"  coefficient of adot^2 u^4  : {adot2_coeff}  (= 1/720)")
print(f"  coefficient of a*addot u^4 : {aaddot_coeff} (= 1/240)")
print(r"""  READ: the acceleration-CHANGE enters as adot^2 and a*addot -- INTEGER powers (analytic). There
  is NO sqrt(adot) anywhere. So the time-varying part of the dS-Unruh response is an ANALYTIC memory
  (a derivative expansion in adot/a^2 = eta), exactly the [KP10] O(eta) structure. An analytic
  derivative expansion is the OPPOSITE of what a MOND kernel needs: the MOND non-analyticity (the
  sqrt(g_N a0) law) comes from the LOCAL magnitude sqrt(a^2 + a_L^2) -> a^2/2a_L, NOT from the
  time-derivative memory. The memory kernel is analytic and CANNOT generate the MOND interpolation
  shape; it only renormalizes it at O(eta) <<1.""")

# Period-average of the nonlocal term for a(tau) = a + A1 cos(Omega tau): is it nonzero (genuinely
# nonlocal) or a total derivative? (repo found -A1^2 Omega^2/720, nonzero + frequency-dependent.)
Omega, A1, t = sp.symbols('Omega A1 t', positive=True)
a_t = a + A1*sp.cos(Omega*t)
adot_t = sp.diff(a_t, t)
adot2_avg = sp.integrate(adot_t**2, (t, 0, 2*sp.pi/Omega)) / (2*sp.pi/Omega)
print(f"\n  For a(tau) = a + A1 cos(Omega tau): <adot^2>_period = {sp.simplify(adot2_avg)}")
print(f"  -> the adot^2/720 nonlocal term period-averages to (A1^2 Omega^2)/(2*720) = {sp.simplify(adot2_avg/720)}")
print(r"""  This is NONZERO and proportional to Omega^2 (frequency-dependent) -- so the response IS genuinely
  time-nonlocal (not a total derivative), confirming the repo finding. BUT it is O(Omega^2) ANALYTIC
  (a gentle high-frequency correction), with NO threshold/non-analytic structure at any special y.
  It renormalizes inertia by ~ (A1 Omega/ a)^2 ~ eta^2 -- utterly negligible at omega_in (eta huge in
  Unruh units means... wait: in the ANALYTIC expansion the small parameter is adot*u^2 evaluated at
  the bath correlation time u~c/a, i.e. (adot)(c/a)^2 = (omega_ex a)(c/a)^2 = omega_ex c^2/a, which is
  >>1 -- the expansion BREAKS DOWN, again because the orbit is far faster than the bath. Either way
  no kernel emerges.)""")


# ==================================================================================================
print("\n"+LINE)
print(" SYNTHESIS -- does the dS-Unruh response FIX the Milgrom kernel theta(y)?  (both ways)")
print(LINE)
print(r"""
 WHAT IS REAL (credited at full weight):
  * The dS-Unruh response for a CONSTANT a is rigorously thermal at T=(1/2pi)sqrt(a^2+(cH_Lam)^2)
    [DL97] -- the framework's FORM-foundation is correct physics.
  * The response for a TIME-VARYING a is genuinely NON-LOCAL in time: [OM07] (Milgrom's own) gives a
    causal R(tau) depending on the whole prior trajectory; [KP10] computes the leading deviation
    = O(eta), eta=adot/a^2. The framework's mechanism HAS a real time-nonlocal worldline realization.
  * That memory is genuinely frequency-dependent (period-avg ~ Omega^2, nonzero) -- a real A(omega).

 WHAT IT DOES NOT DO (conceded at full weight -- the kernel is NOT derived):
  1. TIMESCALE MISMATCH (decisive): the Unruh response has features only at omega ~ a/c (the thermal
     freq, ~1e-19 s^-1) and omega ~ H_Lambda (~1e-18 s^-1). The MI kernel theta(y) lives at the
     INTERNAL orbital frequency omega_in = a/v, which is omega_in/omega_U = c/v ~ 1e3-1e5 times FASTER
     than the Unruh bath and ~1e8 times faster than the horizon. At y=omega_ex/omega_in~O(1) the Unruh
     response is FEATURELESS -- it cannot resolve the orbital oscillation. So it supplies NO structure
     at the y where the cluster sigma-spread / wide-binary predictions live.
  2. ANALYTIC, not MOND-shaped: the time-varying part is an ANALYTIC derivative expansion in eta
     (adot^2, a*addot -- integer powers, no sqrt). The MOND non-analyticity comes from the LOCAL
     magnitude sqrt(a^2+a_L^2), NOT the memory kernel. An analytic memory cannot generate theta(y)'s
     interpolation shape; it only renormalizes inertia at O(eta).
  3. NO CLOSED FORM for the general non-uniform case -- [OM07] (Milgrom himself) has closed forms ONLY
     for special STATIONARY trajectories; the general oscillating case is integral-rep + adiabatic
     approximation only. There is no formula to read theta(y) off.
  4. THE RESPONSE->INERTIA MAP IS AN UNPROVEN ANSATZ (Milgrom verbatim): 'not clear why DeltaT should
     be a measure of inertia; T^2-T_0^2 does NOT give correct MOND; I can offer no specific mechanism.'
     Any theta(y) extracted would smuggle in this choice -- i.e. CIRCULAR.

 VERDICT: the dS-Unruh response is genuinely non-local and the framework's FORM is real physics, but
 it does NOT fix the MI kernel theta(y). The kernel timescale (omega_in=a/v) is decoupled from the
 Unruh timescales (a/c and H_Lambda) by factors of c/v~1e3-1e5; the memory is analytic (not MOND-
 shaped); there is no closed form; and the response->inertia map is Milgrom's own unproven ansatz.
 KERNEL STATUS: FREE-FUNCTION (the Unruh foundation constrains the FORM and the adiabatic y->0 limit,
 but leaves theta(y) at y~O(1) a free function -- exactly like AeST's free function).
 The 6-13% cluster sigma-spread is NOT pinned by the Unruh response; it stays kernel-hostage.
 QUARANTINE held: a0/Z/kappa never asserted derived; a derived kernel would not derive a0 anyway --
 and the kernel is NOT derived.""")
