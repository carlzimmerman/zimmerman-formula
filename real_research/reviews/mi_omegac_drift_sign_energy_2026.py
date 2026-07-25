#!/usr/bin/env python3
"""
THE SIGN OF THE GATE'S SECULAR DRIFT -- ENERGY-BASED DERIVATION (independent lane)
=================================================================================
The omega_c window of MI_FIELD_THEORY_RESULTS_2026.md Sec. 5.2 is

      omega_c in [1.7824e-14, 2.2113e-14] rad/s   (canonical footing a0 = 9.355e-11)

LOWER edge = THEORY-INTERNAL and NON-NEGOTIABLE (Re G >= 0.9 at every confirmed SPARC deep-MOND orbit;
             binding omega_gal,max = 5.94e-15 rad/s, UGC05721) -- and it is a0-FOOTING-INDEPENDENT.
UPPER edge = LLR Gdot/G (Biskupek, Mueller & Torre 2021: (-5.0 +/- 9.6)e-15 /yr) applied to the gate's
             causally-forced secular drift d ln r/dt = a0 omega_c / g_N -- and it scales as 1/a0.

The paper's upper edge used the ceiling |cen| + 2 sigma = 2.420e-14/yr.  That is the correct 2-sigma
ceiling ONLY IF the framework's predicted drift has the SAME SIGN as the LLR central value (which is
NEGATIVE = apparent expansion).  If the framework's drift has the OPPOSITE sign the ceiling is
cen + 2 sigma = 1.420e-14/yr, whose omega_c image lies BELOW the non-negotiable lower edge
=> THE WINDOW IS EMPTY => CLOSED TODAY.  The drift's SIGN is therefore worth the whole window.

The committed source (reviews/mi_cassini_q2_omegac_2026.py, paper Sec. 5.2) gives the drift MAGNITUDE
only.  This script derives the SIGN, from the ENERGY side, four independent ways, and answers the second
question: is the sign FORCED by causality alone (=> unconditional verdict) or does it RIDE ON the
postulated s = -1 (=> conditional verdict, stated for both branches)?

CALIBRATION HELD THROUGHOUT (manufacture NEITHER a win NOR a deficit):
  * No sign is quoted from a remembered rule.  The load-bearing lag is obtained from an EXPLICIT
    time-domain retarded convolution over the actual circular orbit (Section 2), which uses NO
    Fourier-convention choice at all.  The frequency-domain route is then shown to agree (Section 4).
  * If the honest answer were DECAY, the window is CLOSED and that is reported as a falsification-level
    result.  Section 6 carries the decay branch at full strength and prints its (empty) window.
  * Both a0 footings on every load-bearing number.  No TOE language.  No "theory closed".
sympy + numpy + scipy.  Exits 0.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

RULE = "=" * 102
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ----------------------------------------------------------------------------------------------------
# 0. CONSTANTS, ANCHORS, AND -- EXPLICITLY -- EVERY SIGN CONVENTION USED
# ----------------------------------------------------------------------------------------------------
A0_CANON = 9.355e-11          # canonical footing: a0 = c H_Lambda / Z
A0_ALT   = 1.1305e-10         # alt footing: rho_total / cH0
YR       = 365.25 * 86400.0
GM_EARTH = 3.986004418e14
R_MOON   = 3.844e8            # lunar semi-major axis [m]
T_MOON   = 27.321661 * 86400.0
OMEGA_MOON = 2 * np.pi / T_MOON
G_N_MOON = GM_EARTH / R_MOON ** 2

OMEGA_GAL_MAX = 5.94e-15      # UGC05721 innermost deep-MOND orbit
GATE_KEEP     = 0.90
OMEGA_C_LO    = OMEGA_GAL_MAX / np.sqrt(1.0 / GATE_KEEP - 1.0)   # = 3 * omega_gal,max, footing-free

LLR_CEN, LLR_SIG = -5.0e-15, 9.6e-15    # /yr, Biskupek, Mueller & Torre 2021 -- CENTRAL IS NEGATIVE
CEIL_SAME_SIGN = abs(LLR_CEN) + 2 * LLR_SIG   # 2.420e-14 /yr  (prediction on the same side as central)
CEIL_OPP_SIGN  = LLR_CEN + 2 * LLR_SIG        # 1.420e-14 /yr  (prediction on the opposite side)

head("0.  SIGN CONVENTIONS -- stated, not assumed (a reader must be able to check each link)")
print(f"""
  (C1) GATE / FOURIER.  The paper's gate is G(omega) = 1/(1 + i omega/omega_c) with time-domain kernel
       g(t) = omega_c exp(-omega_c t) theta(t).  That pairing fixes the transform convention to
       G(omega) = INT_0^inf g(t) e^(-i omega t) dt, i.e. phasors ~ e^(+i omega t).  Consequence:
       Im G(omega) = -INT_0^inf g(t) sin(omega t) dt < 0 for omega > 0, because g > 0 and causal.
       Im G < 0 is thus forced by (causal support on t>0) + (positive relaxation kernel), in THIS
       convention.  Sections 2-3 never use this; they use only g(t) itself, so they are convention-proof.

  (C2) MI DRESSING.  K_eff(omega) = 1 - S * G(omega),  S = a0/(2 g_N) in the deep-Newton limit
       (paper Sec. 5, reviews/mi_cassini_q2_omegac_2026.py line 91).  DC: K_eff(0) = 1 - S.
       S > 0  <=>  K_eff < 1  <=>  inertia REDUCED  <=>  nu = 1/K > 1  <=>  MOND sign  <=>  s = -1.
       S < 0  <=>  inertia INCREASED (delta_m >= 0) <=> ANTI-MOND  <=>  s = +1.
       The paper states s = -1 "sets the MOND sign, the dissipation sign, and the causality-preserving
       sign of the disformal term simultaneously" (Sec. 3.5 constant list).  sign(S) = the s branch.

  (C3) ANOMALOUS FORCE.  Writing chi = K_eff - 1 = -S G, the EOM m K_eff a = F_N is
       m a = F_N + F_anom  with  F_anom(t) = m S INT_0^inf dtau g(tau) a(t - tau).
       Ungated (g -> delta): F_anom = m S a = m (a0/2) a_hat -- a SUNWARD (extra-attraction) anomaly of
       magnitude a0/2.  This reproduces the paper's a0/2 tail and fixes the sign of S as the sign of
       "extra inward pull", which is what the 1017x-40357x planetary exclusions are computed against.

  (C4) TANGENTIAL FORCE.  f_theta > 0 means ALONG the velocity (prograde); f_theta < 0 means against it.

  (C5) ORBITAL RESPONSE.  da/dt > 0 = EXPANSION (orbit gains energy); da/dt < 0 = DECAY.

  (C6) APPARENT Gdot/G.  Derived, not quoted, in Section 5: a purely radial force exerts no torque, so
       L = m sqrt(G M a) is exactly conserved => a ~ 1/G => d ln a/dt = -(Gdot/G).
       Gdot/G > 0 (G rising, binding tighter) => DECAY.  Gdot/G < 0 => EXPANSION.
       The LLR central value {LLR_CEN:+.1e}/yr therefore corresponds to a mild apparent EXPANSION.

  Numbers: a0 = {A0_CANON:.3e} (canon) / {A0_ALT:.4e} (alt);  Moon: Omega = {OMEGA_MOON:.4e} rad/s,
  g_N = {G_N_MOON:.4e} m/s^2;  window lower edge {OMEGA_C_LO:.4e} rad/s (= 3 x {OMEGA_GAL_MAX:.2e}, footing-free).
  Omega_Moon / omega_c ~ {OMEGA_MOON/2.2113e-14:.2e}  -- the Moon sits FAR ABOVE the corner (x >> 1).
""")
assert abs(OMEGA_C_LO - 1.7824e-14) / 1.7824e-14 < 2e-3, "lower edge regression failed"
assert abs(CEIL_SAME_SIGN - 2.420e-14) < 1e-17 and abs(CEIL_OPP_SIGN - 1.420e-14) < 1e-17

# ----------------------------------------------------------------------------------------------------
# 1. WHAT THE GATE LEAVES BEHIND AT THE MOON: reactive vs dissipative RESIDUE
# ----------------------------------------------------------------------------------------------------
head("1.  WHY THE DRIFT EXISTS AT ALL -- at omega >> omega_c the surviving anomaly is DISSIPATIVE")
def ReG(w, wc): return 1.0 / (1.0 + (w / wc) ** 2)
def ImG(w, wc): return -(w / wc) / (1.0 + (w / wc) ** 2)
x_moon = OMEGA_MOON / 2.2113e-14
print(f"""
  x = Omega/omega_c = {x_moon:.3e} at the Moon (omega_c = 2.2113e-14).
      Re G   = 1/(1+x^2)  = {ReG(OMEGA_MOON, 2.2113e-14):.3e}   <- REACTIVE residue (the gated a0/2 tail)
      |Im G| = x/(1+x^2)  = {abs(ImG(OMEGA_MOON, 2.2113e-14)):.3e}   <- DISSIPATIVE residue
      ratio |Im G| / Re G = x = {x_moon:.2e}

  So the gate does NOT merely shrink the anomaly: above the corner it converts it.  The reactive
  a0/2 tail is killed by ~1e-16, but causality leaves a dissipative residue LARGER by x ~ 1e8.
  That residue is the drift.  Its MAGNITUDE is already in the paper; its SIGN is what follows.
""")

# ----------------------------------------------------------------------------------------------------
# 2. THE CONVENTION-PROOF CORE: explicit retarded convolution over the circular orbit
# ----------------------------------------------------------------------------------------------------
head("2.  CONVENTION-PROOF LAG: the retarded convolution done in the TIME DOMAIN, symbolically")
tau, Om, wc_s, r_s, S_s, m_s = sp.symbols("tau Omega omega_c r S m", positive=True)
# circular orbit, evaluated at t = 0 (WLOG): position r*(1,0), velocity r*Omega*(0,1) (prograde).
# acceleration history a(-tau) = -Omega^2 r * (cos(Omega tau), -sin(Omega tau))
g_ker = wc_s * sp.exp(-wc_s * tau)
Ax = sp.integrate(g_ker * (-Om**2 * r_s * sp.cos(Om * tau)), (tau, 0, sp.oo))
Ay = sp.integrate(g_ker * (+Om**2 * r_s * sp.sin(Om * tau)), (tau, 0, sp.oo))
Ax, Ay = sp.simplify(Ax), sp.simplify(Ay)
ReG_s = wc_s**2 / (wc_s**2 + Om**2)
ImG_s = -wc_s * Om / (wc_s**2 + Om**2)
chk_x = sp.simplify(Ax - (-Om**2 * r_s * ReG_s))
chk_y = sp.simplify(Ay - (-Om**2 * r_s * ImG_s))
print(f"""
  Body at angle 0 on a circular orbit of radius r, angular frequency Omega, moving PROGRADE (+y).
  Its past acceleration is a(-tau) = -Omega^2 r * (cos(Omega tau), -sin(Omega tau))  [rotated backwards].
  The gated (retarded, memory-averaged) acceleration is A_lag = INT_0^inf dtau g(tau) a(-tau):

      A_lag,x = {sp.simplify(Ax)}
      A_lag,y = {sp.simplify(Ay)}

  Identified against the gate's own real/imaginary parts:
      A_lag = -Omega^2 r * ( Re G(Omega), Im G(Omega) )      residuals {chk_x}, {chk_y}  (must be 0, 0)

  READ THE TWO COMPONENTS:
    * RADIAL   piece = -Omega^2 r Re G  ->  F_r = -m S Omega^2 r Re G = -m (a0/2) Re G  = INWARD,
      magnitude (a0/2) Re G.  This is EXACTLY the paper's "reactive anomalous accel = (a0/2) Re G".
      Reproducing it from scratch validates the whole convention chain before the sign question is asked.
    * TANGENTIAL piece = -Omega^2 r Im G = +Omega^2 r |Im G|  ->  f_theta = +S Omega^2 r |Im G|
      = +(a0/2)|Im G| * sign(S).  For S > 0 this is PROGRADE, i.e. ALONG the velocity.

  GEOMETRIC SANITY CHECK, no algebra: the memory kernel averages the INWARD-pointing, ROTATING vector
  a(t') over a retention time tau_mem = 1/omega_c that is ~1e8 orbital periods long.  The rotation
  almost perfectly cancels it; the surviving residue is the part 90 deg out of phase -- i.e. tangential.
  Its orientation is set by which way the vector was rotating, and a RETARDED average leans toward
  WHERE THE ACCELERATION VECTOR POINTED EARLIER.  At angle 0 that is the direction (-cos d, +sin d),
  d = arctan(x) > 0: an inward force tilted with a +y (PROGRADE) component.  The lag pushes FORWARD.
""")
assert chk_x == 0 and chk_y == 0, "time-domain convolution did not reproduce (Re G, Im G)"

# ----------------------------------------------------------------------------------------------------
# 3. ROUTE 1 (ENERGY): P = F_anom . v  ->  dE/dt  ->  da/dt, symbolically and exactly
# ----------------------------------------------------------------------------------------------------
head("3.  ROUTE 1 -- ENERGY.  P = F_anom . v, then dE/dt = (m g_N/2) da/dt")
P_sym = sp.simplify(m_s * S_s * (Ax * 0 + Ay * (r_s * Om)))     # v = (0, r*Omega) at t = 0
gN_sym = Om**2 * r_s
dadt_sym = sp.simplify(2 * P_sym / (m_s * gN_sym))
dlnadt_sym = sp.simplify(dadt_sym / r_s)
a0_s = sp.symbols("a_0", positive=True)
dlnadt_S = sp.simplify(dlnadt_sym.subs(S_s, a0_s / (2 * gN_sym)))
dlnadt_hi = sp.simplify(sp.limit(dlnadt_S, wc_s, 0) if False else sp.simplify(
    sp.series(dlnadt_S.rewrite(sp.Pow), wc_s, 0, 2).removeO()))
paper_form = a0_s * wc_s / gN_sym
ratio = sp.simplify(dlnadt_S / paper_form)
print(f"""
  P = F_anom . v = m S (A_lag . v) = {P_sym}
      -- MANIFESTLY POSITIVE for S > 0: every factor (m, Omega, r, omega_c) is positive.
      The anomalous force does POSITIVE work on the body.  The ORBIT GAINS ENERGY.

  Orbital energy of a quasi-circular orbit: E = -G M m/(2a), so dE/dt = (m g_N/2) da/dt with g_N = Omega^2 r.
      da/dt      = {dadt_sym}
      d ln a/dt  = {dlnadt_sym}
  Substituting the deep-Newton amplitude S = a0/(2 g_N):
      d ln a/dt  = {dlnadt_S}
                 = (a0 omega_c / g_N) * {ratio}          <- exact, all x
  and x = Omega/omega_c >> 1 (x ~ 1e8 at the Moon) collapses the bracket to 1:

      d ln a/dt  ->  + a0 omega_c / g_N        SIGN = POSITIVE = EXPANSION      [for S > 0]

  This is the paper's drift formula d ln r/dt = a0 omega_c / g_N, REDERIVED FROM SCRATCH -- same
  coefficient, no free factor -- and it arrives WITH A SIGN.  The magnitude agreement is the check
  that no factor of 2 or 1/2 was lost anywhere in the chain that carries the sign.
""")
assert sp.simplify(ratio - Om**2 / (wc_s**2 + Om**2)) == 0, "exact drift form mismatch"
assert sp.limit(ratio, wc_s, 0) == 1, "high-frequency limit does not reduce to the paper's formula"

# --- the "but the inertia is REDUCED, is E = -GMm/2a still the right budget?" check, quantified ---
S_moon = A0_CANON / (2 * G_N_MOON)
dress_moon = S_moon * ReG(OMEGA_MOON, 2.2113e-14)
print(f"""  THE REDUCED-INERTIA CAVEAT, QUANTIFIED (it must not be waved through).  Using E = -GMm/(2a) with
  the BARE mass is only legitimate if the inertia is not appreciably dressed at the Moon's frequency:
      DC dressing amplitude          S       = a0/(2 g_N) = {S_moon:.3e}
      dressing actually retained     S * ReG = {dress_moon:.3e}      <- the gate has switched MI OFF here
  The fractional error in the orbital-energy bookkeeping is therefore ~{dress_moon:.0e} -- negligible.
  This is the resolution of the caveat: at omega >> omega_c the inertia is NOT measurably reduced (that
  is precisely what the gate buys at the planets), so the orbit's energy budget is the STANDARD one, and
  the only non-standard question left is WHERE THE POSITIVE WORK COMES FROM.  It cannot come from the
  orbit (the orbit gains), and it cannot come from a passive bath (Section 4: passivity would require
  Im chi <= 0, i.e. S <= 0).  It comes from the dressing's own reservoir, which must therefore be ACTIVE.
  The energy accounting closes only with a non-passive (pumped) MI bath -- the same open item the
  framework's own record flags.  Stated as a cost, not smuggled in as a win.
""")
assert dress_moon < 1e-20, "inertia dressing at the Moon is not negligible -- energy budget needs redoing"

# ----------------------------------------------------------------------------------------------------
# 4. ROUTE 2 (LINEAR RESPONSE / PASSIVITY): P = m Omega |v|^2 Im chi(Omega)
# ----------------------------------------------------------------------------------------------------
head("4.  ROUTE 2 -- LINEAR RESPONSE.  P = m Omega |v|^2 Im chi, chi = -S G  (frequency domain)")
def P_route1(m, S, Om_, r, wc):      # time-domain convolution result
    return m * S * Om_**4 * r**2 * wc / (wc**2 + Om_**2)
def P_route2(m, S, Om_, r, wc):      # response-function result, Im chi = -S Im G = +S|Im G|
    return m * Om_ * (r * Om_)**2 * (-S * ImG(Om_, wc))
print(f"""
  With F_anom(omega) = -m chi(omega) a(omega) and a = i Omega v (phasor e^(+i Omega t)),
        P = Re[F* . v] = m Omega |v|^2 Im chi(Omega).
  chi = -S G  =>  Im chi = -S Im G = +S |Im G|   (Im G < 0 for omega > 0, convention C1).

  So sign(P) = sign(Im chi) = sign(S) x [ -sign(Im G) ] = sign(S) x (+1).
  The causality factor -sign(Im G) = +1 is FORCED.  The remaining factor is sign(S) -- the s branch.

  PASSIVITY / KMS, stated as the criterion rather than the conclusion: a PASSIVE response absorbs
  energy from the drive at every frequency, i.e. requires Im chi(omega) <= 0 for omega > 0, i.e. S <= 0.
      S <= 0 is ANTI-MOND (delta_m >= 0, inertia increased).
      S >  0 is MOND -- and it VIOLATES passivity: the dressing must be ACTIVE (pumped) to have it.
  This is the SAME inequality the framework's own committed record already reports from the REACTIVE
  side ("passive reactive DC shift KMS/Kramers-Kronig LOCKED to delta_m >= 0 anti-MOND, flips only
  under a pump beta < 0").  The reactive and dissipative locks are not independent: the single-pole
  gate multiplies BOTH Re G and Im G by the SAME S with a causality-fixed RELATIVE sign (the content of
  |G|^2 = Re G).  Landing on the identical inequality from the energy side is a real cross-check, and
  it is also the honest price: the expansion that keeps the window open is powered by exactly the
  non-passivity that the framework's own no-pump theorems say nothing sources.
""")
for lab, (Sv, rv, wv) in {"Moon @ hi corner": (A0_CANON / (2 * G_N_MOON), R_MOON, 2.2113e-14),
                          "Moon @ lo corner": (A0_CANON / (2 * G_N_MOON), R_MOON, OMEGA_C_LO),
                          "toy x ~ 1":        (1e-8, 1.0, 1.0)}.items():
    p1, p2 = P_route1(1.0, Sv, OMEGA_MOON if rv > 1 else 1.0, rv, wv), \
             P_route2(1.0, Sv, OMEGA_MOON if rv > 1 else 1.0, rv, wv)
    print(f"    {lab:<20} route1 P/m = {p1:+.6e}   route2 P/m = {p2:+.6e}   rel.diff = {abs(p1/p2-1):.2e}")
    assert abs(p1 / p2 - 1) < 1e-12, "energy routes 1 and 2 disagree"
print("\n  ROUTES 1 AND 2 AGREE to machine precision, and both give P > 0 for S > 0.")

# ----------------------------------------------------------------------------------------------------
# 5. ROUTE 3 (ANGULAR MOMENTUM) and the Gdot/G MAPPING, both DERIVED
# ----------------------------------------------------------------------------------------------------
head("5.  ROUTE 3 -- ANGULAR MOMENTUM; and the da/dt -> apparent Gdot/G map, derived numerically")
L_s = m_s * Om * r_s**2
f_th = S_s * Om**2 * r_s * (Om * wc_s / (wc_s**2 + Om**2))       # +S Omega^2 r |Im G|
dlnL = sp.simplify(m_s * r_s * f_th / L_s)                        # dL/dt = m r f_theta
dlna_from_L = sp.simplify(2 * dlnL)                               # L ~ sqrt(a) at fixed GM
print(f"""
  A tangential force changes L: dL/dt = m r f_theta, and for a circular orbit L = m sqrt(GM a) so
  d ln a/dt = 2 d ln L/dt.  With f_theta = +S Omega^2 r |Im G|:
      d ln L/dt = {dlnL}
      d ln a/dt = {dlna_from_L}
  Route-3 minus Route-1 residual: {sp.simplify(dlna_from_L - dlnadt_sym)}   (must be 0)
  => three routes (work integral, response function, angular momentum) agree, all POSITIVE for S > 0.
""")
assert sp.simplify(dlna_from_L - dlnadt_sym) == 0, "angular-momentum route disagrees"

# --- the Gdot/G mapping, verified by direct numerical integration rather than quoted ---
def orbit_with_Gdot(eps):
    """Integrate a circular orbit under GM(t) = GM0 (1 + eps t); return d<r>/dt sign."""
    GM0, R0 = 1.0, 1.0
    v0 = np.sqrt(GM0 / R0)
    def rhs(t, y):
        x, yy, vx, vy = y
        rr = np.hypot(x, yy)
        GM = GM0 * (1 + eps * t)
        return [vx, vy, -GM * x / rr**3, -GM * yy / rr**3]
    T = 2 * np.pi * 400
    sol = solve_ivp(rhs, [0, T], [R0, 0, 0, v0], rtol=1e-11, atol=1e-13, dense_output=True)
    ts = np.linspace(0, T, 40001)
    rr = np.hypot(*sol.sol(ts)[:2])
    # mean radius over first vs last 20 orbits
    n = len(ts) // 20
    return rr[:n].mean(), rr[-n:].mean()
print(f"  {'GMdot/GM (=Gdot/G)':>20}{'<r> early':>14}{'<r> late':>14}{'d<r>/dt sign':>16}{'meaning':>14}")
print("  " + "-" * 80)
gd_map = {}
for eps in (+2e-4, -2e-4):
    r0, r1 = orbit_with_Gdot(eps)
    sgn = np.sign(r1 - r0)
    gd_map[np.sign(eps)] = sgn
    print(f"  {eps:>20.1e}{r0:>14.6f}{r1:>14.6f}{sgn:>16.0f}{'DECAY' if sgn < 0 else 'EXPANSION':>14}")
assert gd_map[1.0] < 0 and gd_map[-1.0] > 0, "Gdot/G -> orbit-size mapping came out backwards"
print(f"""
  VERIFIED NUMERICALLY (400-orbit integrations, no analytics): Gdot/G > 0 SHRINKS the orbit (decay);
  Gdot/G < 0 GROWS it (expansion).  Analytic reason, one line: the force stays central, so there is no
  torque, so L = m sqrt(GM a) is exactly conserved, so a ~ 1/G and d ln a/dt = -(Gdot/G).
  Hence: an anomalous EXPANSION registers as an apparent Gdot/G < 0 -- THE SAME SIGN as the LLR
  central value {LLR_CEN:+.1e}/yr.  An anomalous DECAY registers as apparent Gdot/G > 0 -- OPPOSITE.
  (Caveat, stated: LLR fits Gdot/G inside full EIH dynamics; the |d ln a/dt| <-> |Gdot/G| magnitude
  identification is the paper's own 1:1 convention.  The SIGN correspondence is what is used here and
  it does not depend on that magnitude convention.)
""")

# ----------------------------------------------------------------------------------------------------
# 6. THE WINDOW, BOTH BRANCHES, BOTH FOOTINGS -- decay branch carried at full strength
# ----------------------------------------------------------------------------------------------------
head("6.  THE WINDOW ARITHMETIC -- s = -1 (MOND, S>0) vs s = +1 (anti-MOND, S<0), both footings")
def wc_ceiling(gdot_per_yr, a0):
    return (gdot_per_yr / YR) * G_N_MOON / a0
print(f"""  Ceiling on omega_c from  d ln a/dt = a0 omega_c / g_N(Moon) <= |Gdot/G| allowance:
      omega_c <= (allowance/yr) * g_N(Moon) / a0 ,  g_N = {G_N_MOON:.4e} m/s^2
  Lower edge {OMEGA_C_LO:.4e} rad/s is FOOTING-INDEPENDENT; the ceiling scales as 1/a0.
""")
print(f"  {'branch':<26}{'drift sign':<12}{'apparent Gdot/G':<18}{'allowance/yr':>14}"
      f"{'footing':>9}{'omega_c ceiling':>18}{'window':>11}{'width':>9}")
print("  " + "-" * 118)
verd = {}
for s_lab, S_sign in (("s = -1 (MOND, S>0)", +1), ("s = +1 (anti-MOND, S<0)", -1)):
    drift = "EXPANSION" if S_sign > 0 else "DECAY"
    gsign = "< 0 (same side)" if S_sign > 0 else "> 0 (opposite)"
    allow = CEIL_SAME_SIGN if S_sign > 0 else CEIL_OPP_SIGN
    for f_lab, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
        hi = wc_ceiling(allow, a0)
        open_ = hi > OMEGA_C_LO
        verd[(s_lab, f_lab)] = (drift, hi, open_)
        print(f"  {s_lab:<26}{drift:<12}{gsign:<18}{allow:>14.3e}{f_lab:>9}{hi:>18.4e}"
              f"{'OPEN' if open_ else 'EMPTY':>11}{hi/OMEGA_C_LO:>8.3f}x")
assert verd[("s = -1 (MOND, S>0)", "canon")][2] and verd[("s = -1 (MOND, S>0)", "alt")][2]
assert not verd[("s = +1 (anti-MOND, S<0)", "canon")][2]
assert not verd[("s = +1 (anti-MOND, S<0)", "alt")][2]
hi_c = verd[("s = -1 (MOND, S>0)", "canon")][1]
hi_a = verd[("s = -1 (MOND, S>0)", "alt")][1]
lo_c = verd[("s = +1 (anti-MOND, S<0)", "canon")][1]
print(f"""
  REGRESSION: the s = -1 ceilings {hi_c:.4e} (canon) / {hi_a:.4e} (alt) reproduce the paper's committed
  upper edges 2.2113e-14 and 1.83e-14 -- so this script's sign choice for the s = -1 branch is the one
  the committed window already assumes, now DERIVED rather than posited.

  DECAY BRANCH AT FULL STRENGTH (not softened): under s = +1 the ceiling falls to {lo_c:.4e} (canon)
  / {verd[('s = +1 (anti-MOND, S<0)','alt')][1]:.4e} (alt), i.e. {OMEGA_C_LO/lo_c:.2f}x / {OMEGA_C_LO/verd[('s = +1 (anti-MOND, S<0)','alt')][1]:.2f}x BELOW the non-negotiable lower edge
  {OMEGA_C_LO:.4e}.  On BOTH footings the window would be EMPTY -- the gated solar-system survivor would
  be dead today, a falsification-level outcome, and the a0/2 tail's 1017x-40357x exclusions would stand
  unmitigated.  That branch is NOT the framework as written (see Section 7), but it is the real fork.

  Concreteness at the surviving corner (canon, omega_c = {hi_c:.4e}): d ln a/dt = {A0_CANON*hi_c/G_N_MOON:.3e}/s
  = {A0_CANON*hi_c/G_N_MOON*YR:.3e}/yr, i.e. da/dt = {A0_CANON*hi_c/G_N_MOON*R_MOON*YR*1e6:.1f} micron/yr of lunar EXPANSION, on top of the
  ~38 mm/yr tidal recession that LLR models separately.  That is the observable the window is renting.
""")

# ----------------------------------------------------------------------------------------------------
# 7. IS THE SIGN FORCED BY CAUSALITY, OR DOES IT RIDE ON s?  -- the second deliverable
# ----------------------------------------------------------------------------------------------------
head("7.  FORCED, OR RIDING ON THE POSTULATE?  -- the decomposition")
# robustness: orbital sense must not matter (chi(t) real => Im chi odd in omega)
P_pro = P_route2(1.0, +1e-8, +OMEGA_MOON, R_MOON, 2.2113e-14)
P_ret = 1.0 * (-OMEGA_MOON) * (R_MOON * OMEGA_MOON)**2 * (-1e-8 * ImG(-OMEGA_MOON, 2.2113e-14))
print(f"""
  sign(d ln a/dt) = sign(P) = sign(Im chi) = sign(S) x [ -sign(Im G(omega>0)) ]

    FACTOR 1  -sign(Im G) = +1     FORCED by causality.  g(t) = omega_c e^(-omega_c t) theta(t) has
              support only on t > 0 and is positive, so Im G = -INT g sin(omega t) dt < 0 for omega > 0.
              Nothing in the framework can flip it without abandoning retardation or kernel positivity.
              Equivalently, Section 2's convention-free statement: the memory-averaged acceleration LAGS,
              and a lagging inward force on a prograde orbit acquires a PROGRADE tangential component.

    FACTOR 2  sign(S)              NOT forced.  S > 0 is the MOND sign (reduced inertia, sunward a0/2
              tail); it is the postulate s = -1.  The paper says so itself: s = -1 "sets the MOND sign,
              THE DISSIPATION SIGN, and the causality-preserving sign of the disformal term
              simultaneously."  Independently, Section 4's passivity criterion Im chi <= 0 would force
              S <= 0 (anti-MOND) for any genuinely PASSIVE dressing; S > 0 requires an active/pumped
              bath, for which the framework's own record has no pump-free channel.

  => The drift sign is NOT forced by causality alone.  VERDICT = SIGN-RIDES-ON-POSITED-s.

  What causality DOES force is the RELATIVE sign: the same S multiplies Re G (reactive) and Im G
  (dissipative), with the relative sign locked (|G|^2 = Re G).  So the two are rigidly tied:
      reactive tail SUNWARD (MOND, the sign the framework needs and the sign its own planetary
      exclusions are computed against)  =>  drift is EXPANSION, necessarily.
      reactive tail OUTWARD (anti-MOND) =>  drift is DECAY, necessarily.
  There is NO branch with a MOND-signed reactive tail and a decaying orbit.  That is the checkable
  content, and it is why the honest verdict is conditional-but-not-open: s = +1 is not a live branch of
  this framework at all (it has no rotation curves, so nothing for the gate to preserve from below and
  no lower edge either).  On the framework AS WRITTEN -- s = -1, which every other number in the paper
  already assumes -- the drift is EXPANSION and the paper's |cen| + 2 sigma ceiling was the RIGHT one.

  ROBUSTNESS: reversing the orbital sense (prograde -> retrograde) must not change the physics.
      P(prograde) = {P_pro:+.6e}   P(retrograde) = {P_ret:+.6e}   same sign = {np.sign(P_pro)==np.sign(P_ret)}
  (chi(t) real => Im chi odd in omega, and v flips too; the two flips cancel.  A phasor-orientation
  error would have shown up here as an antisymmetric answer.)
""")
assert np.sign(P_pro) == np.sign(P_ret) == 1.0, "orbital-sense robustness failed"

# ----------------------------------------------------------------------------------------------------
# 8. VERDICT
# ----------------------------------------------------------------------------------------------------
head("8.  VERDICT (energy lane)")
print(f"""
  SIGN, stated plainly for cross-lane comparison:
      f_theta = +(a0/2)|Im G| ALONG the velocity   ->   P = F_anom . v > 0   ->   dE/dt > 0
      d ln a/dt = + a0 omega_c / g_N  > 0   =   ORBITAL EXPANSION
      apparent Gdot/G < 0   =   SAME SIGN as the LLR central value ({LLR_CEN:+.1e}/yr)
      applicable 2-sigma ceiling = |cen| + 2 sigma = {CEIL_SAME_SIGN:.3e}/yr
      omega_c window = [{OMEGA_C_LO:.4e}, {hi_c:.4e}] canon (x{hi_c/OMEGA_C_LO:.3f}) / [{OMEGA_C_LO:.4e}, {hi_a:.4e}] alt (x{hi_a/OMEGA_C_LO:.3f})
      => WINDOW OPEN.  The paper's committed edges are CONFIRMED, not corrected.
    ALL OF THE ABOVE IS THE s = -1 BRANCH.  Under s = +1: decay, ceiling {CEIL_OPP_SIGN:.3e}/yr,
      omega_c ceiling {lo_c:.4e} < lower edge {OMEGA_C_LO:.4e} => WINDOW EMPTY on both footings.

  FOUR INDEPENDENT ROUTES INSIDE THIS LANE, ALL AGREEING:
      (1) time-domain retarded convolution + work integral  P = F.v            -> expansion
      (2) linear-response  P = m Omega |v|^2 Im chi                            -> expansion (1e-12 match)
      (3) angular momentum  dL/dt = m r f_theta, L ~ sqrt(a)                   -> expansion (exact match)
      (4) numerical Gdot/G orbit integrations fixing the observational mapping  -> expansion <-> Gdot/G<0
  Route (1) reproduces the paper's own a0/2 Re G reactive term AND its a0 omega_c/g_N drift magnitude
  with no adjustable factor, which is the calibration that the sign-carrying chain is intact.

  WHAT THIS DOES NOT DO:
    * It does not derive s.  The window's survival inherits the s = -1 postulate, and with it the
      framework's own open non-passivity/pump problem: the energy that expands the orbit comes from the
      dressing's active reservoir, not from a passive dS bath.  Section 4 shows the energy side lands on
      the identical inequality (Im chi <= 0 <=> delta_m >= 0 <=> anti-MOND) that the committed reactive
      KMS lock already reports.  Expansion and the MOND sign stand or fall together.
    * It does not make omega_c forced.  omega_c remains a free fifth constant (paper Sec. 5.3).
    * A non-empty window is survival, not evidence.  At planetary accelerations GR and healthy
      MOND-family theories both predict ~0; this number discriminates among the framework's own readings.
    * No door is claimed closed; nothing here bears on the lensing sector.
""")
print(RULE)
print("mi_omegac_drift_sign_energy_2026.py: all assertions passed "
      "(convolution = (ReG,ImG); 3 analytic routes identical; paper drift magnitude + window edges "
      "reproduced; Gdot/G mapping numerically verified; orbital-sense robust).")
print(RULE)
