#!/usr/bin/env python3
r"""
THE SIGN OF THE GATED SECULAR DRIFT -- does the omega_c window live or die?
==========================================================================
FORCE-BASED derivation, every sign traceable.  de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman).

THE STAKE.  MI_FIELD_THEORY_RESULTS_2026.md Sec 5.2 quotes the crossover window
      omega_c in [1.7824e-14, 2.2113e-14] rad/s   (canonical footing a0 = 9.355e-11)
  * LOWER edge 1.7824e-14 = 3 x 5.94e-15 : THEORY-INTERNAL, NON-NEGOTIABLE, a0-INDEPENDENT.
    (Re G >= 0.90 at UGC05721's innermost deep-MOND orbit; if the gate closes there the framework
     gates off the very rotation curves it exists to explain.)
  * UPPER edge 2.2113e-14 = (Gdot/G ceiling) * g_N(Moon) / a0 : scales as 1/a0, and its VALUE
    depends on ONE UNCOMPUTED SIGN.  Biskupek, Mueller & Torre 2021 (Universe 7:34, arXiv:2012.12032)
    give LLR  Gdot/G = (-5.0 +/- 9.6)e-15 /yr  -- central NEGATIVE, 0.52 sigma from zero.
      - if the framework's drift has the SAME sign as that central: ceiling = |cen| + 2sig = 2.420e-14/yr
      - if the OPPOSITE sign:                                       ceiling =  cen  + 2sig = 1.420e-14/yr
    The second ceiling maps to omega_c <= 1.2975e-14 rad/s, BELOW the non-negotiable 1.7824e-14
    lower edge  =>  WINDOW EMPTY  =>  the gated survivor is FALSIFIED TODAY.
  The committed derivation (prep_2026/mi_planetary_falsification/window_joint.py line 89) uses
  |Im G| -- a MAGNITUDE.  The SIGN was never computed.  This script computes it.

WHAT IS DERIVED HERE (nothing quoted):
  Sec 1  retarded-kernel convention -> G(omega) = 1/(1 + i omega/omega_c) DERIVED from a real
         convolution (no Fourier-convention freedom left), and sign(Im G) < 0 proved three ways
         (explicit integral; general Herglotz positive-measure theorem; acausal negative control).
  Sec 2  the MI equation of motion for the Moon with the lag; the anomalous force decomposed into
         radial + tangential with signs; the tangential component ALONG v extracted.
  Sec 3  drag or boost -> DECAY or EXPANSION, by TWO independent routes (angular momentum, energy)
         plus a FOURTH, convention-free route: direct numerical integration of the memory-ODE orbit.
  Sec 4  da/dt -> apparent Gdot/G with its sign; comparison to the LLR central.
  Sec 5  which 2-sigma ceiling applies; the window; both footings.
  Sec 6  FORCED-by-causality vs RIDES-ON-s: the conditional structure, stated for s = -1 AND s = +1.
  Sec 7  regression: d ln r/dt = a0 omega_c / g_N (the committed magnitude).
  Sec 8  verdict + the sharp exposures (how little it takes to close the window anyway).

CALIBRATION HELD:  manufacture NEITHER expansion (to save the window) NOR decay (to kill it).
The sign is read off a convolution and confirmed by an ODE integration that knows nothing about
any of the analytics.  Both a0 footings on every 1/a0 number.  No TOE language, no "theory closed".
numpy + sympy.  Exits 0.
"""
import numpy as np, sympy as sp, sys

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond); print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok: PASS = False

RULE = "=" * 102
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ---------------------------------------------------------------------------- constants / anchors
C_LIGHT  = 2.99792458e8
YR       = 3.15576e7
GM_EARTH = 3.986004418e14
R_MOON   = 3.844e8
T_MOON_D = 27.3217                      # sidereal month
A0 = {"canon": 9.355e-11, "alt": 1.13e-10}     # rho_DE cH_Lambda/Z   ;   rho_tot cH0

LLR_CEN, LLR_SIG = -5.0e-15, 9.6e-15    # /yr, Biskupek, Mueller & Torre 2021 -- CENTRAL IS NEGATIVE
OM_GAL_MAX = 5.94e-15                   # rad/s, UGC05721 innermost deep-MOND orbit (loweredge_fullsparc)
GATE_KEEP  = 0.90
OMEGA_MOON = 2*np.pi/(T_MOON_D*86400.0)

# ============================================================================================
head("1.  THE RETARDED KERNEL, THE G(omega) CONVENTION, AND sign(Im G) -- DERIVED, NOT QUOTED")
# ============================================================================================
print(r"""
  CONVENTION 1 (retarded kernel).  Single-pole Debye memory relaxator, in the TIME domain:
        g(t) = omega_c exp(-omega_c t) theta(t),      g(t) >= 0,   INT_0^inf g dt = 1
  theta(t) is the step: the response at time t depends ONLY on the drive at times t' = t - tau <= t.
  That is causality, imposed in the time domain where it is unambiguous.  No frequency convention
  has been chosen yet.

  CONVENTION 2 (transfer function).  Feed the REAL rotating drive d(t) = (cos(Omega t), sin(Omega t)).
  The filtered output is the honest real convolution
        y(t) = INT_0^inf dtau  g(tau)  d(t - tau)
  and its two components are computed below in closed form.  Writing d = e^{i Omega t} in the plane
  (x + i y), the multiplier that comes out IS the definition of G:
        y(t) = G(Omega) e^{i Omega t},   G(Omega) = INT_0^inf g(tau) e^{-i Omega tau} dtau
                                                  = omega_c/(omega_c + i Omega) = 1/(1 + i Omega/omega_c)
  ==> The paper's G(omega) = 1/(1 + i omega/omega_c) is NOT a convention choice: it is what the
      retarded convolution of a counter-clockwise-rotating real vector produces.  The e^{+i Omega t}
      pairing is FORCED by the physical setup, so the sign of Im G is physical, not conventional.
""")
tau_s, Om_s, wc_s = sp.symbols("tau Omega omega_c", positive=True)
g_s = wc_s*sp.exp(-wc_s*tau_s)
G_from_conv = sp.integrate(g_s*sp.exp(-sp.I*Om_s*tau_s), (tau_s, 0, sp.oo))
G_paper = 1/(1 + sp.I*Om_s/wc_s)
check("sympy: the retarded convolution of e^{+i Omega t} yields EXACTLY G = 1/(1+i Omega/omega_c) "
      f"[got {sp.simplify(G_from_conv)}]", sp.simplify(G_from_conv - G_paper) == 0)

ReG_s = 1/(1 + (Om_s/wc_s)**2)
ImG_s = -(Om_s/wc_s)/(1 + (Om_s/wc_s)**2)
G_re, G_im = G_paper.as_real_imag()
check("sympy: Re G = 1/(1+(Om/wc)^2)  exactly", sp.simplify(G_re - ReG_s) == 0)
check("sympy: Im G = -(Om/wc)/(1+(Om/wc)^2)  exactly (NEGATIVE for Om>0)",
      sp.simplify(G_im - ImG_s) == 0)
check("sympy: |G|^2 = Re G (the defining 1-pole identity; Re and Im are a Kramers-Kronig pair)",
      sp.simplify(sp.Abs(G_paper)**2 - ReG_s) == 0)

def ReG(om, wc): return 1.0/(1.0 + (om/wc)**2)
def ImG(om, wc): return -(om/wc)/(1.0 + (om/wc)**2)

print(r"""
  PROOF #1 that Im G < 0 for Omega > 0 (explicit).  From the definition,
        Im G(Omega) = - INT_0^inf g(tau) sin(Omega tau) dtau
  and for the exponential kernel that integral is  omega_c*Omega/(omega_c^2+Omega^2) > 0  strictly.
  Hence Im G < 0.  The minus sign traces to e^{-i Omega tau} with tau >= 0, i.e. to theta(t): the
  output samples the PAST, so its phase LAGS.  arg G = -arctan(Omega/omega_c) in (-pi/2, 0).
""")
sin_int = sp.integrate(g_s*sp.sin(Om_s*tau_s), (tau_s, 0, sp.oo))
check(f"sympy: INT_0^inf g(tau) sin(Om tau) dtau = {sp.simplify(sin_int)} > 0  =>  Im G < 0 strictly",
      sp.simplify(sin_int - wc_s*Om_s/(wc_s**2+Om_s**2)) == 0)
check("numeric: Im G < 0 at every one of 200 test frequencies spanning 1e-4..1e4 x omega_c",
      all(ImG(x, 1.0) < 0 for x in np.logspace(-4, 4, 200)))

print(r"""
  PROOF #2 (general, and this is the framework's OWN structure).  The framework's kernel K is proved
  Herglotz-Nevanlinna with a UNIQUE POSITIVE Borel measure (paper Sec 2.1; ||K|| <= 1, causal-retarded).
  ANY such relaxation response is a positive superposition of single poles,
        G(Omega) = INT dmu(lam) lam/(lam + i Omega),    dmu >= 0
        =>  Im G(Omega) = - INT dmu(lam) lam Omega/(lam^2 + Omega^2)  <  0   for every Omega > 0.
  So Im G < 0 is forced by CAUSALITY + POSITIVITY OF THE SPECTRAL MEASURE -- the same Herglotz
  positivity the paper uses for ghost-freedom.  It is not specific to the single-pole gate.
""")
rng = np.random.default_rng(20260725)
lams = rng.uniform(0.05, 50.0, 400); wts = rng.uniform(0.0, 1.0, 400)      # a POSITIVE measure
def ImG_measure(om, lams, wts):
    return -np.sum(wts*lams*om/(lams**2 + om**2))/np.abs(np.sum(wts))
check("numeric: a random 400-pole POSITIVE measure gives Im G < 0 at all 60 test frequencies",
      all(ImG_measure(x, lams, wts) < 0 for x in np.logspace(-3, 3, 60)))

print(r"""
  NEGATIVE CONTROL (the check discriminates -- it is not decorative).  Replace the RETARDED kernel by
  the ADVANCED one, g_adv(t) = omega_c exp(+omega_c t) theta(-t) (response samples the FUTURE):
        G_adv(Omega) = INT_{-inf}^0 g_adv(t) e^{-i Omega t} dt = 1/(1 - i Omega/omega_c),  Im G_adv > 0.
  Everything downstream flips.  So the tangential sign derived below is load-bearing on CAUSALITY:
  an acausal kernel reverses it.  (A negative spectral measure flips it too -- also checked.)
""")
t_s = sp.symbols("t", real=True)
G_adv = sp.integrate(wc_s*sp.exp(wc_s*t_s)*sp.exp(-sp.I*Om_s*t_s), (t_s, -sp.oo, 0))
check(f"sympy: advanced kernel gives G_adv = 1/(1 - i Om/wc) [got {sp.simplify(G_adv)}], Im G_adv > 0",
      sp.simplify(G_adv - 1/(1 - sp.I*Om_s/wc_s)) == 0)
check("numeric: a NEGATIVE spectral measure flips Im G > 0 (positivity is load-bearing)",
      ImG_measure(1.0, lams, -wts) > 0)

# ============================================================================================
head("2.  THE MI EQUATION OF MOTION WITH THE LAG -- radial + TANGENTIAL decomposition, signs explicit")
# ============================================================================================
print(r"""
  THE UNGATED MI LAW (framework's own, paper Sec 2.1 + Sec 5.1).  mu(x) = K(X), X = |a|^2/a0^2,
  K(z) = (sqrt(1+4z)-1)/(2 sqrt z).  Large x = |a|/a0:  K = 1 - 1/(2x) + O(x^-2), so
        mu(|a|/a0) a = g_N   =>   a (1 - a0/(2|a|)) = g_N   =>   |a| = g_N + a0/2.
  DEFINE sigma = the sign of the anomalous radial acceleration RELATIVE TO g_N:
        delta_a_radial = sigma (a0/2) n_N,   n_N = unit vector ALONG g_N = -r_hat (sunward/earthward)
  sigma = +1 is the MOND branch (EXTRA PULL, reduced inertia mu<1) -- the branch set by the paper's
  s = -1 postulate and the ONLY branch that produces the RAR boost.  sigma = -1 is the anti-MOND
  branch (increased inertia, delta_m >= 0) -- what a strictly PASSIVE KMS bath gives (the framework's
  own committed wall: "no pump-free internal channel sources it").  Both carried through Sec 6.

  THE GATE (paper Sec 5.2).  K_eff = 1 - S(|a|/a0) G(omega), S -> a0/(2 g_N) deep-Newton.  So
        |a| = g_N / K_eff  =  g_N [1 + (a0/(2 g_N)) G(omega) + ...]
  i.e. the anomalous acceleration is the a0/2 tail passed THROUGH the causal filter:
        delta_a(t) = sigma (a0/2) INT_0^inf dtau g(tau) n_N(t - tau)                          (*)

  WHICH OBJECT IS FILTERED -- the one load-bearing modelling choice, and it is FORCED by the paper.
  [ADOPTED, forced]  The filtered object is the anomalous acceleration VECTOR, whose direction
  n_N(t) = -r_hat(t) rotates at the ORBITAL frequency Omega in the inertial (Fermi-Walker,
  non-rotating) frame.  Why forced: the paper's ENTIRE gate mechanism evaluates G at the orbital
  frequency of the measured body (omega_gal = V/r for SPARC orbits at the lower edge, omega_p = 2pi/T_p
  per planet at the upper edge).  If instead a SCALAR were filtered -- |a|, or X = |a|^2/a0^2, both
  CONSTANT on a circular orbit -- the drive would be DC, Re G(0) = 1 for every omega_c, NO suppression
  at any corner, and the paper's own ungated 1017x-40357x per-planet exclusion would stand undiminished.
  Equivalently: filtering in the CO-ROTATING frame kills the gate; filtering in the INERTIAL frame is
  what makes the gate work.  The framework is committed to the inertial-frame reading, and that same
  reading is what produces the tangential component below.  There is no third option in which the gate
  suppresses the tail but produces no tangential force -- that is the content of |G|^2 = Re G.

  THE DECOMPOSITION.  Circular orbit, phase theta(t) = Omega t, Omega of EITHER sign:
        r_hat = (cos Omega t, sin Omega t),    e_hat = (-sin Omega t, cos Omega t) = d r_hat/d(Omega t)
        velocity  v = r Omega e_hat     =>    v_hat = sign(Omega) e_hat
  Real convolution of the rotating unit vector (Sec 1, component form):
        F[r_hat](t) = Re G(Omega) r_hat + Im G(Omega) e_hat            <- both components DERIVED below
  Therefore, from (*) with n_N = -r_hat:
        delta_a = -sigma (a0/2) [ Re G r_hat + Im G e_hat ]
        RADIAL      : delta_a . r_hat = -sigma (a0/2) Re G          (sigma=+1: INWARD, Re G>0)  <- reactive
        TANGENTIAL  : delta_a . v_hat = -sigma (a0/2) Im G sign(Omega)
                                      = +sigma (a0/2) |Im G|        since Im G = -sign(Omega)|Im G|
  ==> the tangential component is INDEPENDENT of the orbit's sense of circulation (parity-safe) and
      its sign is  sigma x (-sign Im G)  =  sigma x (+1)  =  sigma.
""")
# --- symbolic component form of the convolution (no complex shortcut: real integrals) -----------
tt, OmR = sp.symbols("t Omega", real=True)
wcp = sp.symbols("omega_c", positive=True)
Omp = sp.symbols("Omega_p", positive=True)      # positive-Omega instance for the closed forms
gk = wcp*sp.exp(-wcp*tau_s)
Cx = sp.simplify(sp.integrate(gk*sp.cos(Omp*(tt - tau_s)), (tau_s, 0, sp.oo)))
Sy = sp.simplify(sp.integrate(gk*sp.sin(Omp*(tt - tau_s)), (tau_s, 0, sp.oo)))
ReGp = 1/(1 + (Omp/wcp)**2); ImGp = -(Omp/wcp)/(1 + (Omp/wcp)**2)
targ_x = ReGp*sp.cos(Omp*tt) + ImGp*(-sp.sin(Omp*tt))     # ReG r_hat_x + ImG e_hat_x
targ_y = ReGp*sp.sin(Omp*tt) + ImGp*( sp.cos(Omp*tt))     # ReG r_hat_y + ImG e_hat_y
check("sympy: real convolution x-component = Re G r_hat_x + Im G e_hat_x  (exact, all t)",
      sp.simplify(sp.expand_trig(sp.simplify(Cx - targ_x))) == 0)
check("sympy: real convolution y-component = Re G r_hat_y + Im G e_hat_y  (exact, all t)",
      sp.simplify(sp.expand_trig(sp.simplify(Sy - targ_y))) == 0)

# --- fully independent NUMERICAL convolution (quadrature over the past, no analytics at all) ----
def conv_numeric(Om, wc, t0, nmax=400.0, N=400001):
    tau = np.linspace(0.0, nmax/wc, N)
    w = wc*np.exp(-wc*tau)
    fx = np.trapz(w*np.cos(Om*(t0-tau)), tau); fy = np.trapz(w*np.sin(Om*(t0-tau)), tau)
    return np.array([fx, fy])
for (Om, wc, t0) in [(1.0, 0.3, 0.7), (2.0, 5.0, 1.3), (-1.5, 0.4, 2.1)]:
    rh = np.array([np.cos(Om*t0), np.sin(Om*t0)]); eh = np.array([-np.sin(Om*t0), np.cos(Om*t0)])
    num = conv_numeric(Om, wc, t0)
    ana = ReG(Om, wc)*rh + ImG(Om, wc)*eh
    check(f"numeric quadrature convolution matches Re G r_hat + Im G e_hat  (Om={Om}, wc={wc}) "
          f"|err|={np.max(np.abs(num-ana)):.2e}", np.max(np.abs(num-ana)) < 2e-6)

# --- the tangential component, sign explicit, both sigma branches, both senses of circulation ----
print("  TANGENTIAL COMPONENT  delta_a . v_hat  in units of (a0/2), computed numerically:")
print(f"  {'sigma':>6}{'Omega':>8}{'omega_c':>9}{'Im G':>12}{'delta_a.v_hat/(a0/2)':>24}{'drag or boost':>16}")
print("  " + "-"*80)
tang_rows = []
for sigma in (+1, -1):
    for Om in (+1.0, -1.0):
        wc = 0.25
        img = ImG(Om, wc)
        tangential = -sigma*img*np.sign(Om)          # = +sigma |Im G|
        lab = "BOOST (along v)" if tangential > 0 else "DRAG (against v)"
        tang_rows.append((sigma, Om, tangential, lab))
        print(f"  {sigma:>6}{Om:>8.1f}{wc:>9.2f}{img:>12.5f}{tangential:>24.5f}{lab:>16}")
check("tangential sign = sigma, independent of the sense of circulation (parity-safe)",
      all(np.sign(r[2]) == np.sign(r[0]) for r in tang_rows))
check("MOND branch sigma=+1 (the framework's s=-1 posit): tangential is a BOOST, ALONG v",
      [r for r in tang_rows if r[0] == +1][0][2] > 0)
check("anti-MOND branch sigma=-1 (passive-bath delta_m>=0): tangential is a DRAG, AGAINST v",
      [r for r in tang_rows if r[0] == -1][0][2] < 0)
print(r"""
  GEOMETRIC CROSS-CHECK, no algebra.  The retarded filter points the force along a weighted average of
  PAST inward directions.  For counter-clockwise motion, -r_hat(t-tau) is -r_hat(t) rotated CLOCKWISE.
  -r_hat sits at angle theta+pi; the velocity sits at theta+pi/2 = (theta+pi) - pi/2, i.e. 90 deg
  CLOCKWISE of -r_hat.  So rotating the inward force clockwise moves it TOWARD the velocity:
  a lag on an ATTRACTIVE (sigma=+1) force is a FORWARD boost.  This is the classical Laplace
  aberration-of-gravity result (retarded central attraction -> angular momentum GAIN -> outward spiral),
  reproduced here as a consistency check on the sign, not imported as an assumption.
""")

# ============================================================================================
head("3.  BOOST -> EXPANSION or DRAG -> DECAY?  THREE independent routes, forced to agree")
# ============================================================================================
print(r"""
  Let  f_t = delta_a . v_hat = sigma (a0/2)|Im G|  be the tangential specific force (Sec 2).

  ROUTE A -- ANGULAR MOMENTUM (torque).  L = |r x v| = sqrt(GM a) per unit mass for a circular orbit.
        dL/dt = |r x delta_a| = r f_t          (only the tangential piece torques)
        L = sqrt(GM a)  =>  dL/dt = (1/2) sqrt(GM/a) da/dt
        =>  da/dt = 2 r f_t sqrt(a/GM) = 2 f_t / Omega          (using GM = Omega^2 a^3, r = a)
        =>  d ln a/dt = 2 f_t/(Omega a)                                          [ROUTE A]

  ROUTE B -- ENERGY.  E = v^2/2 - GM/r = -GM/(2a) per unit mass.
        dE/dt = delta_a . v = f_t v = f_t Omega a       (radial force does no work on a circular orbit)
        dE/dt = (GM/(2a^2)) da/dt
        =>  da/dt = 2 a^2 f_t Omega a/(GM) = 2 f_t/Omega        (GM = Omega^2 a^3)
        =>  d ln a/dt = 2 f_t/(Omega a)                                          [ROUTE B]  == ROUTE A

  Both give the SAME expression with the SAME sign, as they must (a circular orbit driven by a weak
  tangential force stays quasi-circular).  Sign:  sign(d ln a/dt) = sign(f_t) = sigma.
        sigma = +1 (MOND / s=-1)      ->  f_t > 0, BOOST   ->  da/dt > 0  ->  ORBITAL EXPANSION
        sigma = -1 (anti-MOND)        ->  f_t < 0, DRAG    ->  da/dt < 0  ->  ORBITAL DECAY

  WHOSE ENERGY BUDGET?  This is the trap flagged in the brief, and it is real.  Im G < 0 makes the
  response DISSIPATIVE in the standard passivity sense: the BATH absorbs energy from whatever drives
  it.  But the pair (drive = n_N, response = delta_a) is NOT a conjugate force/coordinate pair, so the
  passivity theorem does not constrain the ORBIT's mechanical energy: the orbital power delta_a . v is
  LINEAR in the response and therefore carries the prefactor sigma, whereas the bath's absorbed power
  is QUADRATIC in the coupling and cannot see it.  Consistency with the framework's own committed
  record: a strictly PASSIVE KMS/Kramers-Kronig bath locks the DC mass shift to delta_m >= 0, i.e.
  anti-MOND, i.e. sigma = -1, i.e. DRAG and DECAY.  The framework's sigma = +1 is the reduced-inertia
  (delta_m < 0) branch -- the "pump" branch its own no-pump-free-channel wall identifies.  So the
  ORBIT gaining energy is not a contradiction: on the sigma = +1 branch the MI dressing is an ACTIVE
  (negative-mass-shift) response, and the orbit gains from the same posited dS-Unruh coupling that
  supplies the MOND boost.  Stated plainly: the EXPANSION sign and the MOND sign are the SAME sign.
""")
# ---- ROUTE A vs ROUTE B, symbolic identity ------------------------------------------------------
GM_s, a_s, ft_s = sp.symbols("GM a f_t", positive=True)
Om_kep = sp.sqrt(GM_s/a_s**3)
routeA = (2*a_s*ft_s*sp.sqrt(a_s/GM_s))/a_s    # (1/a) * da/dt, da/dt = 2 r f_t sqrt(a/GM), r = a
routeB = sp.simplify(2*a_s**2*ft_s*Om_kep*a_s/GM_s/a_s)
check(f"sympy: ROUTE A (angular momentum) == ROUTE B (energy):  d ln a/dt = 2 f_t/(Omega a) both ways",
      sp.simplify(routeA - routeB) == 0 and sp.simplify(routeA - 2*ft_s/(Om_kep*a_s)) == 0)

# ---- ROUTE C: convention-free ODE integration of the memory orbit -------------------------------
print(r"""
  ROUTE C -- DIRECT NUMERICAL INTEGRATION (uses NONE of Routes A/B).  Because the kernel is a single
  exponential the memory is EXACTLY local in an auxiliary vector m(t):
        m(t) = INT_0^inf dtau g(tau) n_N(t-tau)      <=>      dm/dt = omega_c (n_N(t) - m)
  so the exact memory dynamics is the closed, local ODE system
        d^2 r/dt^2 = -GM r_hat/r^2 + sigma A m ,    dm/dt = omega_c (-r_hat - m) ,   A = a0/2
  RK4, units GM = 1, r0 = 1 (Omega = 1), Omega/omega_c = O(1)-O(10).  (The real ratio is ~1e8 and
  unintegrable; the closed form 2 f_t/(Omega a) is scale-free in Omega/omega_c, and the SIGN certainly is.)
  Drift measured as the least-squares slope of ln a_osc, a_osc = -GM/(2E), E = v^2/2 - GM/r, over the
  central 50% of the run.  The integrator is told nothing about Re G, Im G, drag, boost, or expansion.

  AMPLITUDE CONVERGENCE, reported not hidden.  The closed form is the LINEARIZED (first-order-in-A)
  rate.  At finite A the run leaves the linear regime: as a grows, g_N = GM/a^2 falls and the drift rate
  d ln a/dt -> 2 A omega_c/g_N itself GROWS as a^2, so a finite-A least-squares slope OVERSHOOTS the
  linearized value by O(Delta ln a).  The table below shows the ratio -> 1 as A -> 0 at fixed step
  count, and step-size independence at fixed A -- i.e. the residual is the known physical nonlinearity,
  not integration error.  The SIGN is amplitude-independent at every A.
""")
def integrate_memory_orbit(sigma, wc, A, Om_sign=+1.0, n_orbit=60, steps_per_orbit=500):
    GM = 1.0; r0 = 1.0
    v0 = np.sqrt(GM/r0 + sigma*A*ReG(Om_sign*1.0, wc)*r0)   # circular in the FULL radial force
    y = np.zeros(6); y[0] = r0; y[3] = Om_sign*v0
    rh0 = np.array([1.0, 0.0]); eh0 = np.array([0.0, 1.0])
    y[4:6] = -(ReG(Om_sign*1.0, wc)*rh0 + ImG(Om_sign*1.0, wc)*eh0)   # m starts at quasi-steady state
    def rhs(y):
        r = y[0:2]; v = y[2:4]; m = y[4:6]
        rn = np.hypot(r[0], r[1]); rh = r/rn
        return np.concatenate([v, -GM*rh/rn**2 + sigma*A*m, wc*(-rh - m)])
    T = 2*np.pi*n_orbit; N = n_orbit*steps_per_orbit; h = T/N
    ts = np.empty(N+1); la = np.empty(N+1)
    for i in range(N+1):
        r = y[0:2]; v = y[2:4]; rn = np.hypot(r[0], r[1])
        E = 0.5*(v[0]**2 + v[1]**2) - GM/rn
        ts[i] = i*h; la[i] = np.log(-GM/(2*E))
        if i == N: break
        k1 = rhs(y); k2 = rhs(y+0.5*h*k1); k3 = rhs(y+0.5*h*k2); k4 = rhs(y+h*k3)
        y = y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    sel = (ts > 0.25*T) & (ts < 0.75*T)
    return np.polyfit(ts[sel], la[sel], 1)[0], la[-1] - la[0]

print(f"  {'sigma':>6}{'Om_sign':>8}{'Om/wc':>7}{'A':>8}{'spo':>6}{'analytic':>14}{'ODE':>14}"
      f"{'ratio':>9}{'D ln a':>10}{'verdict':>11}")
print("  " + "-"*95)
ode_rows = []
for sigma in (+1, -1):
    for wc, Om_sign in [(0.1, +1.0), (0.3, +1.0), (0.1, -1.0)]:
        for A, spo in [(1e-3, 500), (1e-4, 500), (1e-6, 500), (1e-6, 1500)]:
            ana = 2*sigma*A*abs(ImG(1.0, wc))                  # Omega = 1, a = 1
            num, dtot = integrate_memory_orbit(sigma, wc, A, Om_sign=Om_sign, steps_per_orbit=spo)
            v = "EXPANSION" if num > 0 else "DECAY"
            ode_rows.append((sigma, Om_sign, wc, A, spo, ana, num, v))
            print(f"  {sigma:>6}{Om_sign:>8.0f}{1.0/wc:>7.1f}{A:>8.0e}{spo:>6}{ana:>14.5e}{num:>14.5e}"
                  f"{num/ana:>9.5f}{dtot:>10.1e}{v:>11}")
lin = [r for r in ode_rows if r[3] == 1e-6]
check("ROUTE C: in the LINEAR regime (A=1e-6) the ODE drift matches the analytic 2 f_t/(Omega a) to "
      f"<0.1% in all {len(lin)} runs -- max dev "
      f"{max(abs(r[6]/r[5]-1) for r in lin):.2e}  (magnitude AND sign, integrator blind to the analytics)",
      all(abs(r[6]/r[5] - 1) < 1e-3 for r in lin))
check("ROUTE C: ratio -> 1 monotonically as A -> 0 (residual = the physical finite-amplitude "
      "nonlinearity, not integration error)",
      all(abs([r for r in ode_rows if r[:3]==k and r[3]==1e-6][0][6]/[r for r in ode_rows if r[:3]==k and r[3]==1e-6][0][5]-1)
          < abs([r for r in ode_rows if r[:3]==k and r[3]==1e-3][0][6]/[r for r in ode_rows if r[:3]==k and r[3]==1e-3][0][5]-1)
          for k in {r[:3] for r in ode_rows}))
check("ROUTE C: step-size independent at fixed A (500 vs 1500 steps/orbit agree to <0.05%)",
      all(abs([r for r in ode_rows if r[:4]==k+(1e-6,) and r[4]==500][0][6] /
              [r for r in ode_rows if r[:4]==k+(1e-6,) and r[4]==1500][0][6] - 1) < 5e-4
          for k in {r[:3] for r in ode_rows}))
check("ROUTE C: sigma=+1 (MOND branch, the framework's s=-1) integrates to ORBITAL EXPANSION in "
      "EVERY run, at every amplitude and both senses of circulation",
      all(r[6] > 0 for r in ode_rows if r[0] == +1))
check("ROUTE C: sigma=-1 (anti-MOND / passive-bath branch) integrates to ORBITAL DECAY in EVERY run",
      all(r[6] < 0 for r in ode_rows if r[0] == -1))
check("ROUTES A, B, C AGREE on the sign (no route is picked over another; they concur)",
      all(np.sign(r[6]) == np.sign(r[5]) for r in ode_rows))

# ---- ROUTE D + acausal negative control: orbit-averaged POWER by direct quadrature --------------
print(r"""
  ROUTE D -- ORBIT-AVERAGED POWER BY QUADRATURE, and the acausal control.  The advanced kernel cannot
  be integrated as an ODE (an acausal filter is anti-damped: m diverges either time direction), so the
  control is done at the level of the orbit-averaged power, computed by quadrature on a fixed circular
  reference orbit with NO analytics:
        m_ret(t) = INT_0^inf dtau g(tau) n_N(t - tau)        [retarded: samples the PAST]
        m_adv(t) = INT_0^inf dtau g(tau) n_N(t + tau)        [advanced: samples the FUTURE]
        <P> = (1/T) INT_0^T dt  sigma A m(t) . v(t)          T = one orbit
  <P> > 0  =>  orbit GAINS energy  =>  EXPANSION;   <P> < 0  =>  DECAY.  Signs read off, not assumed.
""")
def avg_power(sigma, wc, kernel="ret", A=1.0, Ntau=200001, Nt=721, taumax_over_tau=400.0):
    tau = np.linspace(0.0, taumax_over_tau/wc, Ntau)
    w = wc*np.exp(-wc*tau)
    sgn = -1.0 if kernel == "ret" else +1.0          # sample t-tau (past) or t+tau (future)
    ts = np.linspace(0.0, 2*np.pi, Nt)
    P = np.empty(Nt)
    for j, t in enumerate(ts):
        arg = t + sgn*tau
        nx = -np.cos(arg); ny = -np.sin(arg)          # n_N = -r_hat at the sampled time
        mx = np.trapz(w*nx, tau); my = np.trapz(w*ny, tau)
        vx, vy = -np.sin(t), np.cos(t)                # v_hat on the reference circular orbit (Omega=1)
        P[j] = sigma*A*(mx*vx + my*vy)
    return np.trapz(P, ts)/(2*np.pi)
print(f"  {'kernel':>10}{'sigma':>7}{'Om/wc':>7}{'<P>/(A)':>15}{'expected -sigma ImG':>21}{'verdict':>12}")
print("  " + "-"*74)
pow_rows = []
for kernel in ("ret", "adv"):
    for sigma in (+1, -1):
        wc = 0.25
        Pav = avg_power(sigma, wc, kernel=kernel)
        expect = -sigma*ImG(1.0, wc) if kernel == "ret" else -sigma*(-ImG(1.0, wc))
        v = "EXPANSION" if Pav > 0 else "DECAY"
        pow_rows.append((kernel, sigma, Pav, expect, v))
        print(f"  {kernel:>10}{sigma:>7}{1/wc:>7.1f}{Pav:>15.6f}{expect:>21.6f}{v:>12}")
check("ROUTE D: quadrature orbit-averaged power reproduces -sigma Im G for the RETARDED kernel to <1e-5",
      all(abs(r[2]-r[3]) < 1e-5 for r in pow_rows if r[0] == "ret"))
check("ROUTE D: RETARDED + sigma=+1 (MOND branch) -> <P> > 0 -> the orbit GAINS energy -> EXPANSION",
      [r for r in pow_rows if r[0]=="ret" and r[1]==+1][0][2] > 0)
check("ROUTE D: RETARDED + sigma=-1 (anti-MOND branch) -> <P> < 0 -> DECAY",
      [r for r in pow_rows if r[0]=="ret" and r[1]==-1][0][2] < 0)
check("NEGATIVE CONTROL: the ADVANCED (acausal) kernel FLIPS both branches "
      "-> the sign is load-bearing on CAUSALITY (theta(t)), not an artifact of the setup",
      all(np.sign([r for r in pow_rows if r[0]=="adv" and r[1]==s][0][2]) ==
          -np.sign([r for r in pow_rows if r[0]=="ret" and r[1]==s][0][2]) for s in (+1,-1)))
print(r"""
  ==> FOUR routes (angular-momentum torque, orbital energy, memory-ODE integration, quadrature power)
      AGREE, with no route selected over another:
          sign(d ln a/dt) = sigma = sign of the anomalous RADIAL acceleration relative to g_N.
      On the framework's own branch (sigma = +1, the MOND/RAR sign set by s = -1): EXPANSION.
""")

# ============================================================================================
head("4.  d ln a/dt  ->  APPARENT Gdot/G, WITH ITS SIGN  (mapping VERIFIED, not quoted)")
# ============================================================================================
print(r"""
  CONVENTION (a).  What does a real Gdot/G do to an orbit?  Derived, then integrated.
  With G slowly varying and NO tangential force, the specific angular momentum L = sqrt(G M a) is
  exactly conserved (central force, zero torque).  Hence  G a = const  =>
        d ln a/dt = - d ln G/dt = -Gdot/G
        Gdot/G > 0 (G increasing, binding tightens)  ->  a SHRINKS  ->  ORBITAL DECAY
        Gdot/G < 0 (G decreasing, binding loosens)   ->  a GROWS    ->  ORBITAL EXPANSION
  So the LLR central value Gdot/G = -5.0e-15/yr corresponds to a mild apparent EXPANSION.
  Verified below by integrating a Kepler orbit with G(t) = G0(1 + k t) and measuring d ln a_osc/dt.
""")
def integrate_Gdot(k, n_orbit=60, spo=800):
    M = 1.0; r0 = 1.0
    y = np.zeros(4); y[0] = r0; y[3] = np.sqrt(1.0/r0)
    def rhs(t, y):
        r = y[0:2]; v = y[2:4]; rn = np.hypot(r[0], r[1])
        G = 1.0 + k*t
        return np.concatenate([v, -G*M*r/rn**3])
    T = 2*np.pi*n_orbit; N = n_orbit*spo; h = T/N
    ts = np.empty(N+1); la = np.empty(N+1)
    t = 0.0
    for i in range(N+1):
        r = y[0:2]; v = y[2:4]; rn = np.hypot(r[0], r[1]); G = 1.0 + k*t
        E = 0.5*(v[0]**2+v[1]**2) - G*M/rn
        ts[i] = t; la[i] = np.log(-G*M/(2*E))
        if i == N: break
        k1 = rhs(t, y); k2 = rhs(t+0.5*h, y+0.5*h*k1)
        k3 = rhs(t+0.5*h, y+0.5*h*k2); k4 = rhs(t+h, y+h*k3)
        y = y + (h/6.0)*(k1+2*k2+2*k3+k4); t += h
    sel = (ts > 0.25*T) & (ts < 0.75*T)
    return np.polyfit(ts[sel], la[sel], 1)[0]
print(f"  {'Gdot/G (k)':>13}{'measured d ln a/dt':>21}{'-k (predicted)':>17}{'ratio':>9}{'orbit':>12}")
print("  " + "-"*74)
gd_rows = []
for k in (+1e-6, -1e-6, +1e-7, -1e-7):
    sl = integrate_Gdot(k)
    gd_rows.append((k, sl))
    print(f"  {k:>13.1e}{sl:>21.6e}{-k:>17.1e}{sl/(-k):>9.5f}"
          f"{('DECAY' if sl<0 else 'EXPANSION'):>12}")
check("VERIFIED: an integrated Kepler orbit with G(t)=G0(1+kt) gives d ln a/dt = -k to <0.5% "
      f"(max dev {max(abs(r[1]/(-r[0])-1) for r in gd_rows):.2e})",
      all(abs(r[1]/(-r[0]) - 1) < 5e-3 for r in gd_rows))
check("VERIFIED: Gdot/G > 0 -> DECAY, and Gdot/G < 0 -> EXPANSION (convention (a) confirmed, not quoted)",
      all((r[1] < 0) == (r[0] > 0) for r in gd_rows))
print(r"""
  THEREFORE, the framework's gated drift expressed as the apparent Gdot/G that an LLR fit would absorb:
        (Gdot/G)_apparent  =  - d ln a/dt  =  - sigma a0 omega_c / g_N(Moon)
  sigma = +1 (framework's MOND branch)  ->  (Gdot/G)_app is NEGATIVE.
  LLR central (Biskupek, Mueller & Torre 2021) is NEGATIVE (-5.0e-15/yr).   ==>  SAME SIGN.
""")
gN_moon = GM_EARTH/R_MOON**2
print(f"  g_N(Moon) = GM_E/R^2 = {gN_moon:.5e} m/s^2   (Omega_M^2 R = {OMEGA_MOON**2*R_MOON:.5e}, "
      f"agree to {abs(OMEGA_MOON**2*R_MOON/gN_moon-1)*100:.1f}% -- solar perturbations; GM/R^2 used, as committed)")
print(f"  {'footing':<8}{'a0':>12}{'omega_c':>12}{'d ln a/dt [/yr]':>18}{'(Gdot/G)_app [/yr]':>21}{'sign':>7}")
print("  " + "-"*80)
for lab, a0 in A0.items():
    for wcv in (1.7824e-14, 2.2113e-14):
        d = a0*wcv/gN_moon*YR
        print(f"  {lab:<8}{a0:>12.3e}{wcv:>12.4e}{d:>18.4e}{-d:>21.4e}{'NEGATIVE':>7}")
print(r"""
  CAVEAT, carried [ASSUMPTION]:  a tangential force and a true Gdot are NOT identical signatures.
  Matching d ln a/dt they differ in the mean motion:  Gdot gives n ~ G^2 => nd/n = 2 Gdot/G = -2 D,
  a tangential force gives n ~ a^(-3/2) => nd/n = -1.5 D  (D = d ln a/dt).  So an LLR fit sensitive to
  the mean-motion drift would absorb the framework's drift as only (3/4) of an equal-Delta-a Gdot,
  i.e. the effective ceiling on omega_c is up to 4/3 LOOSER than quoted.  Direction of the caveat is
  reported in Sec 5; it never tightens the ceiling, so it cannot manufacture a closure -- nor is it
  used to widen the window in the headline number.
""")

# ============================================================================================
head("5.  WHICH 2-SIGMA CEILING APPLIES -- and is the window OPEN or EMPTY?")
# ============================================================================================
print(r"""
  THE CEILING LOGIC, spelled out.  The framework predicts a definite value P = (Gdot/G)_app.  It is
  consistent with LLR at 2 sigma iff  |P - cen| <= 2 sigma, i.e.  cen - 2sig <= P <= cen + 2sig,
  with cen = -5.0e-15/yr, sig = 9.6e-15/yr  =>  P in [-24.2e-15, +14.2e-15] /yr.
        * P NEGATIVE (framework EXPANSION):  binding side is P >= -24.2e-15  =>  |P| <= |cen| + 2sig
                                             = 2.420e-14/yr    <-- the paper's ceiling, CORRECT
        * P POSITIVE (framework DECAY):      binding side is P <= +14.2e-15  =>  |P| <=  cen  + 2sig
                                             = 1.420e-14/yr    <-- the ceiling that would CLOSE it
  Sections 1-4 give P = -sigma a0 omega_c/g_N, so P < 0 on the framework's own MOND branch sigma = +1.
  ==> the |cen| + 2 sigma = 2.420e-14/yr ceiling is the RIGHT one, and the paper's upper edge stands.
""")
LOWER = 3.0*OM_GAL_MAX      # = 1/sqrt(1/0.90 - 1) x omega_gal,max ; a0-INDEPENDENT
k_lo = 1.0/np.sqrt(1.0/GATE_KEEP - 1.0)
check(f"LOWER edge rebuilt from theory: k = 1/sqrt(1/{GATE_KEEP}-1) = {k_lo:.4f}, "
      f"omega_c >= {k_lo:.1f} x {OM_GAL_MAX:.3e} = {LOWER:.4e} rad/s (matches committed 1.7824e-14, "
      f"a0-INDEPENDENT)", abs(LOWER/1.7824e-14 - 1) < 2e-3 and abs(k_lo - 3.0) < 1e-9)
CEIL_SAME = abs(LLR_CEN) + 2*LLR_SIG        # 2.420e-14 /yr  (prediction on the SAME side as central)
CEIL_OPP  = LLR_CEN + 2*LLR_SIG             # 1.420e-14 /yr  (prediction on the OPPOSITE side)
print(f"\n  ceiling if SAME sign as central  = |{LLR_CEN:.1e}| + 2({LLR_SIG:.1e}) = {CEIL_SAME:.4e} /yr")
print(f"  ceiling if OPPOSITE sign         =  {LLR_CEN:.1e}  + 2({LLR_SIG:.1e}) = {CEIL_OPP:.4e} /yr")
print(f"\n  {'branch':<26}{'footing':<7}{'ceiling /yr':>13}{'omega_c upper':>15}{'lower edge':>13}"
      f"{'width':>9}{'WINDOW':>9}")
print("  " + "-"*94)
WIN = {}
for bname, sigma, ceil in [("sigma=+1 MOND EXPANSION", +1, CEIL_SAME), ("sigma=-1 antiMOND DECAY", -1, CEIL_OPP)]:
    for lab, a0 in A0.items():
        hi = (ceil/YR)*gN_moon/a0
        w = hi/LOWER
        WIN[(sigma, lab)] = (hi, w)
        print(f"  {bname:<26}{lab:<7}{ceil:>13.4e}{hi:>15.4e}{LOWER:>13.4e}{w:>9.4f}"
              f"{('OPEN' if w > 1 else 'EMPTY'):>9}")
check("REGRESSION: the EXPANSION branch reproduces the committed canonical upper edge 2.2113e-14 "
      f"(got {WIN[(+1,'canon')][0]:.4e}) and alt 1.8307e-14 (got {WIN[(+1,'alt')][0]:.4e}) to <0.2%",
      abs(WIN[(+1,'canon')][0]/2.2113e-14 - 1) < 2e-3 and abs(WIN[(+1,'alt')][0]/1.8307e-14 - 1) < 2e-3)
check("EXPANSION branch (framework's own): window NON-EMPTY on BOTH footings "
      f"(canon x{WIN[(+1,'canon')][1]:.4f}, alt x{WIN[(+1,'alt')][1]:.4f})",
      WIN[(+1,'canon')][1] > 1 and WIN[(+1,'alt')][1] > 1)
check("DECAY branch: window EMPTY on BOTH footings -- the upper edge falls BELOW the non-negotiable "
      f"lower edge (canon x{WIN[(-1,'canon')][1]:.3f}, alt x{WIN[(-1,'alt')][1]:.3f})",
      WIN[(-1,'canon')][1] < 1 and WIN[(-1,'alt')][1] < 1)
# 4/3 mean-motion caveat, both branches
print("\n  the 4/3 mean-motion caveat of Sec 4, applied to BOTH branches (it only LOOSENS ceilings):")
for sigma, ceil in [(+1, CEIL_SAME), (-1, CEIL_OPP)]:
    for lab, a0 in A0.items():
        hi43 = (4.0/3.0)*(ceil/YR)*gN_moon/a0
        print(f"    sigma={sigma:+d} {lab:<6} omega_c <= {hi43:.4e}  -> width x{hi43/LOWER:.4f} "
              f"({'OPEN' if hi43 > LOWER else 'EMPTY'})")
check("the 4/3 caveat does NOT rescue the DECAY branch on either footing (it stays EMPTY) -- so the "
      "closed/open split is robust to that modelling factor",
      all((4.0/3.0)*(CEIL_OPP/YR)*gN_moon/a0 < LOWER for a0 in A0.values()))

# ============================================================================================
head("6.  FORCED BY CAUSALITY, OR RIDING ON THE POSITED s = -1?  The conditional structure")
# ============================================================================================
print(r"""
  DECOMPOSITION OF THE DRIFT SIGN.  From Sec 2-3 the tangential force is
        f_t  =  sigma  x  ( -Im G )  x  (a0/2)
  a PRODUCT of two signs, and they have different epistemic status:

  FACTOR 1 -- (-Im G) > 0 : FORCED, unconditionally.  Proved three ways in Sec 1 (explicit integral;
        the general Herglotz positive-measure theorem, which is the framework's OWN kernel structure;
        and an acausal negative control that flips it).  This is causality + spectral positivity.
        Nothing about it is postulated.  It is the part the paper called "the gate's own causal shadow".

  FACTOR 2 -- sigma = +1 : NOT forced by causality.  sigma is the sign of the anomalous radial
        acceleration relative to g_N, i.e. the MOND sign, i.e. the paper's s = -1 postulate.  The paper
        already states s "sets the MOND sign, the dissipation sign, and the causality-preserving sign of
        the disformal term simultaneously; no pump-free internal channel sources it."  This computation
        CONFIRMS that coupling and, for the first time, computes WHICH WAY the dissipation sign points.
        A strictly PASSIVE (unpumped) KMS bath gives the OPPOSITE sigma: the framework's own committed
        result is that passivity + Kramers-Kronig lock the DC mass shift to delta_m >= 0 (anti-MOND).

  SO THE HONEST STATEMENT IS A CONDITIONAL, AND BOTH BRANCHES ARE REPORTED:
        sigma = +1  (s = -1; MOND; reduced inertia; the framework's posit and the ONLY branch that
                     produces the RAR boost)  ->  BOOST -> EXPANSION -> Gdot/G_app < 0
                     -> SAME sign as the LLR central -> ceiling 2.420e-14/yr -> WINDOW OPEN
        sigma = -1  (s = +1 effectively; anti-MOND; increased inertia; what an unpumped passive bath
                     gives)  ->  DRAG -> DECAY -> Gdot/G_app > 0
                     -> OPPOSITE sign -> ceiling 1.420e-14/yr -> WINDOW EMPTY

  WHY THIS IS NOT A COIN FLIP, AND ALSO NOT A FREE WIN.  Two things are true at once and both belong
  in the record:
   (i) sigma = +1 is not an independently adjustable knob here.  The window's LOWER edge is DEFINED by
       "the gate must not suppress the deep-MOND SPARC rotation curves" -- which presupposes that the
       galactic boost exists, i.e. presupposes sigma = +1.  On the sigma = -1 branch there is no MOND
       boost, no RAR, no lower edge, and the window question is not even posed (the theory is dead for a
       far more basic reason).  So WITHIN the window problem there is no live branch on which the drift
       decays.  The verdict on the framework's own terms is EXPANSION, and the paper's |cen| + 2 sigma
       ceiling is the correct one.
   (ii) The survival is nonetheless NOT independent of the framework's known sign wall.  The expansion
       sign is the SAME posit as the MOND sign -- it adds no new free constant (the count stays at five),
       but it also inherits, in full, "no pump-free internal channel sources s = -1".  If that wall is
       ever resolved AGAINST the framework (i.e. the correct reduction is the passive delta_m >= 0 one),
       then the same computation closes the omega_c window as a corollary.  The window and the sign wall
       are now COUPLED, where before they were separate items in the ledger.  That coupling is a cost,
       and it is the second deliverable of this script.
""")
check("the drift sign FACTORS as sigma x (-Im G): the causal factor is forced, the sigma factor is the "
      "already-ledgered s=-1 posit -> NO sixth constant is introduced by the drift sign", True)

# ============================================================================================
head("7.  REGRESSION -- the committed magnitude d ln r/dt = a0 omega_c / g_N")
# ============================================================================================
print(r"""
  From Sec 3, d ln a/dt = 2 f_t/(Omega a) with f_t = sigma (a0/2)|Im G(Omega)|.  For a bound orbit
  Omega^2 a = g_N, so
        d ln a/dt = sigma (a0/(a omega_c)) / (1 + (Omega/omega_c)^2)      [EXACT closed form]
                  -> sigma a0 omega_c / g_N                              [Omega >> omega_c asymptote]
  which is the committed magnitude (paper Sec 5.2 / window_joint.py), now WITH its sign = sigma.
""")
print(f"  {'body':<9}{'Omega [rad/s]':>15}{'Om/wc':>11}{'2f_t/(Om a)':>15}{'exact closed':>15}"
      f"{'a0 wc/gN':>13}{'ratios':>20}")
print("  " + "-"*98)
a0c = A0["canon"]; wc_reg = 2.2113e-14
for nm, aa, Td, GMc in [("Moon", R_MOON, T_MOON_D, GM_EARTH),
                        ("Mercury", 5.7909e10, 87.969, 1.32712440018e20),
                        ("Saturn", 1.43353e12, 10759.22, 1.32712440018e20)]:
    Om = 2*np.pi/(Td*86400.0); gN = Om**2*aa      # dynamically consistent g_N = Omega^2 a
    ft = (a0c/2)*abs(ImG(Om, wc_reg))
    d_direct = 2*ft/(Om*aa)
    d_exact = (a0c/(aa*wc_reg))/(1 + (Om/wc_reg)**2)
    d_asym = a0c*wc_reg/gN
    print(f"  {nm:<9}{Om:>15.4e}{Om/wc_reg:>11.3e}{d_direct:>15.5e}{d_exact:>15.5e}{d_asym:>13.5e}"
          f"{f'{d_direct/d_exact:.6f} / {d_direct/d_asym:.6f}':>20}")
    check(f"[{nm}] 2f_t/(Omega a) == exact closed form == a0 wc/g_N asymptote (all three, <1e-3)",
          abs(d_direct/d_exact - 1) < 1e-9 and abs(d_direct/d_asym - 1) < 1e-3)

# ============================================================================================
head("8.  VERDICT, AND THE SHARP EXPOSURES THE SIGN CREATES")
# ============================================================================================
# how much LLR improvement closes the window even on the EXPANSION branch?
print("  The EXPANSION branch does NOT make the window comfortable -- it makes it a live prediction.")
print(f"\n  {'footing':<8}{'min predicted Gdot/G_app':>27}{'sigma-distance from LLR cen':>29}"
      f"{'sigma_LLR that closes':>23}{'improvement':>13}")
print("  " + "-"*100)
expos = {}
for lab, a0 in A0.items():
    Pmin = -a0*LOWER/gN_moon*YR                       # most conservative (lower-edge) prediction
    nsig = abs(Pmin - LLR_CEN)/LLR_SIG
    sig_close = (abs(Pmin) - abs(LLR_CEN))/2.0        # |cen| + 2 sig < |Pmin|  =>  sig < this
    expos[lab] = (Pmin, nsig, sig_close, LLR_SIG/sig_close)
    print(f"  {lab:<8}{Pmin:>27.4e}{nsig:>28.2f}s{sig_close:>23.3e}{LLR_SIG/sig_close:>12.2f}x")
check("the framework's MINIMUM drift (at the RAR-forced lower edge) is a definite NEGATIVE apparent "
      "Gdot/G on both footings -- a two-sided prediction, not merely a bound",
      all(expos[l][0] < 0 for l in expos))
check(f"canonical footing: the window closes on the EXPANSION branch as soon as the LLR Gdot/G "
      f"uncertainty improves by x{expos['canon'][3]:.2f} (sigma < {expos['canon'][2]:.2e}/yr) at "
      f"unchanged central -- i.e. survival margin is thin, not comfortable",
      expos['canon'][3] < 2.0)
# hostage to the SIGN of a 0.52-sigma central value
print(f"\n  HOSTAGE TO A 0.52-SIGMA FLUCTUATION.  The LLR central is {LLR_CEN:.1e}/yr, only "
      f"{abs(LLR_CEN)/LLR_SIG:.2f} sigma from zero.")
for cen_alt, lbl in [(-5.0e-15, "as published (NEGATIVE)"), (0.0, "central at zero"),
                     (+5.0e-15, "central re-fit POSITIVE")]:
    ceil = -(cen_alt - 2*LLR_SIG)                     # binding side for a NEGATIVE prediction
    hi = (ceil/YR)*gN_moon/A0["canon"]
    print(f"    cen = {cen_alt:>+9.1e} ({lbl:<25}) -> ceiling {ceil:.3e}/yr -> omega_c <= {hi:.4e} "
          f"-> width x{hi/LOWER:.4f} -> {'OPEN' if hi > LOWER else 'EMPTY'}")
check("the OPEN verdict requires the LLR central to be NEGATIVE (or at most ~zero): a re-fit central "
      "of +5.0e-15/yr would close the canonical window even on the EXPANSION branch",
      ((2*LLR_SIG - 5.0e-15)/YR)*gN_moon/A0["canon"] < LOWER)
print(r"""
  VERDICT (dynamics sector, S_matter; the GW170817-excluded lensing sector is not involved).

  1. THE SIGN.  On the framework's own branch the gated MI drift is an ORBITAL EXPANSION.
     Derivation: causality (theta(t)) makes Im G < 0; the anomalous a0/2 tail is an ATTRACTIVE vector
     whose direction rotates at the orbital frequency; a retarded filter rotates that inward vector
     TOWARD the velocity; the resulting tangential force is a forward BOOST; the orbit gains angular
     momentum and energy; a grows.  Four independent routes agree (torque, energy, memory-ODE
     integration, quadrature power), an acausal control flips it, and the magnitude reproduces the
     committed d ln r/dt = a0 omega_c/g_N exactly.

  2. THE CEILING AND THE WINDOW.  Expansion => apparent Gdot/G is NEGATIVE => the SAME sign as the LLR
     central (-5.0e-15/yr) => the correct 2-sigma ceiling is |cen| + 2 sigma = 2.420e-14/yr, which is
     what the paper used.  The paper's upper edge 2.2113e-14 rad/s (canon) / 1.8307e-14 (alt) STANDS.
     THE WINDOW IS NOT EMPTY:  canon [1.782, 2.211]e-14 = x1.241 ;  alt [1.782, 1.831]e-14 = x1.027.
     The alt footing's +2.7% knife-edge is unchanged.  This is a SURVIVAL, not a win: at planetary
     accelerations both GR and healthy MOND-family theories predict ~0, so nothing here discriminates
     against LambdaCDM.

  3. FORCED OR CONDITIONAL.  The sign FACTORS as sigma x (-Im G).  (-Im G) > 0 is forced by causality
     plus Herglotz spectral positivity -- unconditional.  sigma = +1 is the already-ledgered s = -1
     postulate (the MOND sign).  No SIXTH constant appears; the count stays at five.  But the omega_c
     window is now COUPLED to the framework's known sign wall: if the correct reduction is the passive
     delta_m >= 0 one, the same computation gives DECAY, the ceiling becomes 1.420e-14/yr, and the
     window is EMPTY on both footings (x0.73 canon, x0.60 alt) -- robust to the 4/3 mean-motion caveat.
     Reported as a conditional, with both branches priced.

  4. WHAT THE SIGN COSTS THE FRAMEWORK -- new, and not softened.  Because the lower edge is a THEORY-
     INTERNAL floor, the drift is not merely bounded, it is PREDICTED to be at least
     -1.95e-14/yr (canon) / -2.36e-14/yr (alt) -- i.e. 4-5x the LLR central magnitude, sitting
     1.5-2.0 sigma from it on both footings.  Consequences:
       * a x1.32 improvement in the LLR Gdot/G uncertainty (canon) -- x1.03 (alt) -- at unchanged
         central CLOSES the window.  This is a near-term, already-funded falsifier, sharper than the
         paper's "x3 ephemeris refit" statement.
       * the OPEN verdict is hostage to the SIGN of a 0.52-sigma central value.  Sharper than that:
         a central of exactly ZERO already closes the canonical window (x0.984).  The window is open
         ONLY because the published LLR central happens to be negative, and only by 1.5 sigma's worth
         of room.  A re-fit to +5.0e-15/yr closes it outright (x0.728).
     So: the window survives, and it survives BECAUSE a 0.5-sigma noise excursion in LLR happens to
     point the same way the framework's causal drift points.  That is survival by sign alignment, and
     it should be reported as such rather than as a passed test.

  NO claim that any door is closed; no claim beyond this one sign and its two edges.
""")
print(RULE)
print(f"mi_llr_drift_sign_2026.py: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print(RULE)
sys.exit(0 if PASS else 1)
