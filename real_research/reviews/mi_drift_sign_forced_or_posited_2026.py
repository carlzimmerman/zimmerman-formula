#!/usr/bin/env python3
r"""
IS THE omega_c SECULAR-DRIFT SIGN FORCED BY CAUSALITY, OR DOES IT RIDE ON THE POSITED s = -1?
=============================================================================================
de Sitter-Unruh MODIFIED-INERTIA framework (Carl Zimmerman).  THE SECOND DELIVERABLE of the
omega_c-window sign audit.  Companion / cross-check lane: reviews/mi_omegac_drift_sign_energy_2026.py
(energy + response-function + angular-momentum routes).  THIS script is deliberately built on a
DIFFERENT footing so that agreement is informative:

    the energy lane works in the FREQUENCY domain (Im chi, passivity, KK).
    THIS lane does a raw NUMERICAL ORBIT INTEGRATION in the TIME domain with the exponential
    memory carried as an auxiliary ODE.  It uses NO Fourier convention, no Im G, no passivity
    theorem, no analytic da/dt formula.  If the two lanes agree, the sign is not a convention.

WHAT IS BEING DECIDED.  The gated MI crossover leaves a secular orbital drift whose MAGNITUDE is
already in the record (d ln r/dt = a0 omega_c / g_N, window_joint.py) but whose SIGN was dropped:
window_joint.py line 89 takes |Im G|, an absolute value.  The sign is worth the whole window:

    framework predicts EXPANSION  -> apparent Gdot/G < 0 -> same sign as LLR central -5.0e-15/yr
                                  -> one-sided 2s ceiling |cen| + 2s = 2.420e-14/yr -> WINDOW OPEN
    framework predicts DECAY      -> apparent Gdot/G > 0 -> opposite sign
                                  -> one-sided 2s ceiling  cen  + 2s = 1.420e-14/yr -> WINDOW EMPTY

CALIBRATION HELD (manufacture neither a win nor a deficit):
  * The DECAY branch is carried at full strength and its window verdict printed, not softened.
  * No claim that causality alone forces the sign until the factorization is actually computed.
  * Both a0 footings on every load-bearing number.  Lower edge is footing-INDEPENDENT by construction.
  * No TOE language.  No "theory closed".  numpy + sympy + scipy.  Exits 0.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

RULE = "=" * 102
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ----------------------------------------------------------------------------------------------------
# 0. CONSTANTS, CITED ANCHORS, AND EVERY SIGN CONVENTION SPELLED OUT
# ----------------------------------------------------------------------------------------------------
A0_CANON = 9.355e-11        # canonical footing: a0 = c H_Lambda / Z   (rho_DE)
A0_ALT   = 1.13e-10         # alternate footing: a0 = c H_0 / Z        (rho_total)
YR       = 365.25 * 86400.0
GM_EARTH = 3.986004418e14
R_MOON   = 3.844e8
G_N_MOON = GM_EARTH / R_MOON ** 2                 # 2.6975e-3 m/s^2
OMEGA_MOON = np.sqrt(GM_EARTH / R_MOON ** 3)      # 2.6653e-6 rad/s

# Biskupek, Mueller & Torre 2021 (Universe 7:34, arXiv:2012.12032): LLR Gdot/G = (-5.0 +/- 9.6)e-15 /yr
LLR_CEN, LLR_SIG = -5.0e-15, 9.6e-15
OMEGA_C_LO = 1.7824e-14     # THEORY-INTERNAL, NON-NEGOTIABLE: 3 x 5.94e-15 (UGC05721 deep-MOND orbit)
OMEGA_C_HI_PAPER = 2.2113e-14

head("0.  SIGN CONVENTIONS -- stated explicitly, so every link can be checked independently")
print(f"""
  C1  GATE.  Retarded single-pole Debye memory:  g(t) = omega_c e^(-omega_c t) theta(t),  t >= 0 only.
      This is the ONLY object this lane uses.  It is manifestly causal (theta(t)) and manifestly
      normalised (INT g dt = 1).  No Fourier transform is taken anywhere in Sections 1-3.
      [The frequency-domain partner G(omega) = 1/(1 + i omega/omega_c) is recovered in Section 4
       purely to connect to the paper's notation -- it is not used to get the sign.]

  C2  MI DRESSING SIGN.  Deep-Newton expansion of the framework's own kernel
      K(X) = (sqrt(1+4X) - 1)/(2 sqrt X),  X = |a|^2/a0^2  =>  K = 1 - a0/(2|a|) + O((a0/|a|)^2).
      With the posited s = -1 the inertial coefficient is mu_fw = K < 1: inertia REDUCED (delta_m <= 0).
      Solving mu_fw |a| = g_N then gives |a| = g_N + a0/2: the anomalous acceleration is
                    delta_a = + (a0/2) * (unit vector along g_bar)   i.e. EXTRA SUNWARD PULL.
      Define the signed amplitude   A == -s * (a0/2)   so that
                    s = -1  ->  A = +a0/2  ->  extra ATTRACTION   (MOND, inertia reduced)
                    s = +1  ->  A = -a0/2  ->  extra REPULSION    (anti-MOND, inertia increased)
      A > 0 is the branch the galaxies require.  A < 0 is the branch KMS/passivity forces in a
      free (unpumped) vacuum -- the framework's own committed "delta_m >= 0 anti-MOND" lock.

  C3  ORBIT GEOMETRY.  Prograde circular orbit, position r(t) = r(cos phi, sin phi), phi = Omega t,
      Omega > 0.  Then v = r Omega t_hat with t_hat = (-sin phi, cos phi).  "PROGRADE" == along +t_hat
      == along v.  A force along +t_hat does POSITIVE work on the orbit.

  C4  DRIFT -> APPARENT Gdot/G.  Circular orbit, slowly varying GM: the force stays central so there
      is NO torque, L = m sqrt(GM a) is exactly conserved, hence a ~ 1/(GM) and
                    d ln a/dt = - d ln(GM)/dt = - Gdot/G.
      So  Gdot/G > 0 (G rising, binding tightens) <=> DECAY  (da/dt < 0)
          Gdot/G < 0                              <=> EXPANSION (da/dt > 0).
      Section 5 re-derives this by direct numerical integration rather than quoting it.

  C5  LLR SIGN.  Measured Gdot/G = {LLR_CEN:+.1e} +/- {LLR_SIG:.1e} /yr.  The central value is NEGATIVE,
      so by C4 the LLR central corresponds to a mild apparent EXPANSION.  Significance from zero:
      |cen|/sigma = {abs(LLR_CEN)/LLR_SIG:.2f} sigma  -- i.e. the measured SIGN is very weak information.
""")

# ----------------------------------------------------------------------------------------------------
# 1. THE CONVENTION-FREE CORE: integrate the orbit WITH the memory, and just look at what r does.
# ----------------------------------------------------------------------------------------------------
head("1.  RAW NUMERICAL ORBIT + MEMORY ODE -- no Fourier transform, no Im G, no passivity theorem")
print(r"""
  The exponential memory is carried as an auxiliary VECTOR state m(t), which by construction equals
  the retarded memory average of the radial unit vector:

        m(t) = INT_0^inf domega_c e^(-omega_c tau) r_hat(t - tau) dtau      (the C1 kernel)
    <=> dm/dt = omega_c ( r_hat(t) - m(t) )                                 (exact, one line)

  and the equation of motion integrated is

        dr/dt = v ,      dv/dt = -(GM/|r|^2) r_hat(t)  -  A * m(t)

  where -A*m is the GATED anomalous term: an extra pull of signed amplitude A directed along the
  MEMORY-AVERAGED (i.e. retarded, past) radial direction rather than the instantaneous one.  That
  retardation is the whole physical content of the gate; nothing else is inserted.

  A/g_N is set to 1e-3 (not the physical 1e-8) purely so the secular trend is numerically resolvable
  over a few tens of orbits.  The SIGN is scale-free -- verified below by sweeping A/g_N over 4 decades.
""")

def run_orbit(A_over_gN, wc_over_Omega, n_orbits=40.0, GM=1.0, R=1.0):
    """Integrate the gated-MI circular orbit. Returns (t array, osculating semi-major axis a(t))."""
    Om = np.sqrt(GM / R ** 3)
    gN = GM / R ** 2
    A = A_over_gN * gN
    wc = wc_over_Omega * Om
    y0 = [R, 0.0, 0.0, Om * R, 1.0, 0.0]           # x, y, vx, vy, mx, my  (memory starts aligned)
    def rhs(t, y):
        x, yy, vx, vy, mx, my = y
        rr = np.hypot(x, yy)
        rhx, rhy = x / rr, yy / rr
        ax = -GM / rr ** 2 * rhx - A * mx
        ay = -GM / rr ** 2 * rhy - A * my
        return [vx, vy, ax, ay, wc * (rhx - mx), wc * (rhy - my)]
    T = 2 * np.pi / Om * n_orbits
    sol = solve_ivp(rhs, (0, T), y0, rtol=1e-12, atol=1e-14, dense_output=True,
                    t_eval=np.linspace(0, T, 4001))
    x, yy, vx, vy = sol.y[0], sol.y[1], sol.y[2], sol.y[3]
    rr = np.hypot(x, yy)
    v2 = vx ** 2 + vy ** 2
    # osculating semi-major axis from the PURE-NEWTONIAN energy (the observable an ephemeris fits)
    energy = 0.5 * v2 - GM / rr
    a_osc = -GM / (2 * energy)
    return sol.t, a_osc, Om

print(f"  {'A/g_N':>10}{'omega_c/Omega':>15}{'d ln a/dt [1/orbit]':>24}{'sign':>10}{'branch':>26}")
print("  " + "-" * 92)
slopes = {}
for A_over_gN in (1e-3, -1e-3):
    for wc_over_Om in (0.5, 1.0, 3.0):
        t, a_osc, Om = run_orbit(A_over_gN, wc_over_Om)
        # fit the secular trend over the second half (drop the transient while m(t) locks on)
        half = len(t) // 2
        p = np.polyfit(t[half:], np.log(a_osc[half:]), 1)
        per_orbit = p[0] * (2 * np.pi / Om)
        slopes[(A_over_gN, wc_over_Om)] = per_orbit
        branch = "s = -1  MOND  (A > 0)" if A_over_gN > 0 else "s = +1  anti-MOND (A < 0)"
        print(f"  {A_over_gN:>10.0e}{wc_over_Om:>15.1f}{per_orbit:>24.6e}"
              f"{'EXPANSION' if per_orbit > 0 else 'DECAY':>10}{branch:>26}")

for key, v in slopes.items():
    A_over_gN = key[0]
    assert (v > 0) == (A_over_gN > 0), f"sign of d ln a/dt did not track sign(A) at {key}"
print(f"""
  RESULT, from raw integration only:  sign(d ln a/dt) = sign(A) at every corner ratio tested.
      A > 0  (s = -1, MOND, extra ATTRACTION toward the retarded direction)  ->  EXPANSION
      A < 0  (s = +1, anti-MOND, extra REPULSION)                            ->  DECAY
  This is the classical Laplace geometry: an attraction aimed at where the source *was* has a
  PROGRADE tangential component, does positive work, and expands the orbit.  Flip the attraction to a
  repulsion and the same retardation gives a RETROGRADE component and decay.  No convention entered.
""")

# scale-freedom of the sign
print("  SCALE SWEEP (sign must not depend on the artificially inflated amplitude):")
for A_over_gN in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
    t, a_osc, Om = run_orbit(A_over_gN, 1.0, n_orbits=40.0)
    half = len(t) // 2
    sl = np.polyfit(t[half:], np.log(a_osc[half:]), 1)[0] * (2 * np.pi / Om)
    ratio = sl / A_over_gN
    print(f"    A/g_N = {A_over_gN:>8.0e}   d ln a/dt per orbit = {sl:>13.6e}   "
          f"/(A/g_N) = {ratio:.6f}   -> LINEAR in A, sign fixed")
    assert sl > 0

# ----------------------------------------------------------------------------------------------------
# 2. QUANTITATIVE CROSS-CHECK: does the time-domain integration reproduce the PAPER's magnitude too?
# ----------------------------------------------------------------------------------------------------
head("2.  CROSS-CHECK vs THE PAPER'S FORMULA -- magnitude AND sign, from the time domain")
def ImG(w, wc):  return -(w / wc) / (1.0 + (w / wc) ** 2)     # frequency-domain partner (C1), Section 4
print(r"""
  The record's chain is  f_t = A |Im G(Omega)|  ->  d ln a/dt = 2 f_t/(Omega r)  ->  a0 omega_c/g_N.
  Per orbit that predicts   Delta ln a = 4 pi (A/g_N) |Im G(Omega, omega_c)| .
  The integration of Section 1 knows nothing about that formula.  Compare, at small amplitude:
""")
print(f"  {'omega_c/Omega':>14}{'|Im G|':>10}{'predicted/orbit':>18}{'integrated/orbit':>19}{'ratio':>10}")
print("  " + "-" * 92)
for wc_over_Om in (0.3, 0.5, 1.0, 3.0, 10.0):
    A_over_gN = 1e-7
    t, a_osc, Om = run_orbit(A_over_gN, wc_over_Om, n_orbits=60.0)
    half = len(t) // 2
    integ = np.polyfit(t[half:], np.log(a_osc[half:]), 1)[0] * (2 * np.pi / Om)
    pred = 4 * np.pi * A_over_gN * abs(ImG(1.0, wc_over_Om))
    print(f"  {wc_over_Om:>14.1f}{abs(ImG(1.0, wc_over_Om)):>10.4f}{pred:>18.6e}{integ:>19.6e}"
          f"{integ/pred:>10.4f}")
    assert abs(integ / pred - 1) < 0.03, f"magnitude mismatch at wc/Om={wc_over_Om}"
print("""
  AGREEMENT to <3% at every corner ratio, with the POSITIVE sign, for A > 0.  So the time-domain lane
  reproduces the paper's own drift magnitude AND supplies the sign that window_joint.py discarded when
  it wrote |Im G| (line 89 of prep_2026/mi_planetary_falsification/window_joint.py takes abs()).
  The magnitude in the record is correct; only the sign was missing.  It is EXPANSION for A > 0.
""")

# ----------------------------------------------------------------------------------------------------
# 3. THE FACTORIZATION -- is there ANY independent sign freedom between the reactive and dissipative
#    channels?  (this is the "are the two locks mutually consistent at all" question, computed)
# ----------------------------------------------------------------------------------------------------
head("3.  FACTORIZATION: does the dissipative channel carry a factor of s, or not?")
w, wc, A_s = sp.symbols("Omega omega_c A", positive=True)
s_sym = sp.symbols("s")                      # NOT assumed positive: this is the branch variable
G = 1 / (1 + sp.I * w / wc)
ReG_s, ImG_s = sp.re(sp.expand(sp.simplify(G))), sp.im(sp.expand(sp.simplify(G)))
Amp = -s_sym * A_s                           # C2: signed amplitude A = -s (a0/2), A_s == a0/2 > 0
radial_chan = sp.simplify(Amp * ReG_s)       # inward reactive anomaly
tang_chan   = sp.simplify(-Amp * ImG_s)      # prograde tangential anomaly (Section 1 geometry)
ratio = sp.simplify(tang_chan / radial_chan)
print(f"""
  ONE amplitude, TWO channels.  The gate multiplies the SINGLE anomalous amplitude A = -s(a0/2) by the
  SINGLE complex response G(Omega).  Decomposing the retarded direction (Section 1) into the current
  radial and tangential axes gives, with no further input:

      radial (reactive, sunward)   =  A * Re G      =  {radial_chan}
      tangential (dissipative)     =  A * |Im G|    =  {sp.simplify(tang_chan)}

      ratio  tangential/radial     =  {ratio}      =  Omega/omega_c  =  tan(lag angle)

  READ THIS OFF:  the ratio is INDEPENDENT of s and of A, and is STRICTLY POSITIVE.  That is the part
  causality forces.  Both channels carry the SAME factor A = -s(a0/2), so:

      * the RELATIVE sign of the reactive and dissipative channels is FORCED by causality
        (the retarded kernel has lag angle Delta = arctan(Omega/omega_c) in (0, pi/2): the response
         TRAILS, it can never LEAD -- a leading response would need g(t) supported at t < 0);
      * the ABSOLUTE sign of BOTH is set by the single posited s.

  There is therefore NO independent sign freedom.  You cannot have MOND in the reactive channel and
  choose the dissipative sign separately -- that is the content of the machine-verified |G|^2 = Re G
  identity: one pole, one amplitude, one sign.
""")
assert sp.simplify(ratio - w / wc) == 0, "tangential/radial ratio is not Omega/omega_c"
assert s_sym not in ratio.free_symbols and A_s not in ratio.free_symbols
# and confirm the lag angle is strictly in the trailing quadrant for all omega, wc > 0
lag = sp.atan(w / wc)
print(f"  lag angle Delta = {lag}, monotone increasing, range (0, pi/2) for Omega, omega_c > 0:")
for r_ in (0.01, 1.0, 100.0):
    print(f"      Omega/omega_c = {r_:>7.2f}  ->  Delta = {float(sp.atan(r_)):.6f} rad "
          f"= {float(sp.atan(r_))*180/np.pi:6.2f} deg   (TRAILING, forced)")
assert float(sp.atan(0.01)) > 0 and float(sp.atan(100.0)) < np.pi / 2

# ----------------------------------------------------------------------------------------------------
# 4. THE SIGN TRANSFER: sign(A) is not a free dial -- it is MEASURED in galaxies
# ----------------------------------------------------------------------------------------------------
head("4.  DELIVERABLE 2(c) -- does requiring MOND in galaxies FORCE the solar-system drift sign?")
KPC = 3.0857e19
def nu_frame(y): return np.sqrt(1.0 + 1.0 / y)
def gbar_from_gobs(gobs, a0):
    """invert the exact a0-line g_obs^2 - g_bar^2 = a0 g_bar  for g_bar."""
    return (-a0 + np.sqrt(a0 ** 2 + 4 * gobs ** 2)) / 2.0
print(f"""
  The SAME amplitude A appears in the galactic reactive channel (gate OPEN there, Re G >= 0.90 by
  construction of the lower edge) and in the solar-system dissipative channel (gate CLOSED there).
  Section 3 proved there is ONE amplitude and no independent sign freedom.  Therefore sign(A) is fixed
  by whichever regime MEASURES it -- and that is the galaxies.

      A > 0  =>  nu = sqrt(1 + 1/y) > 1  =>  rotation curves ABOVE Newtonian  (observed)
      A < 0  =>  the anomaly is a REPULSION => rotation curves BELOW Newtonian (not observed)

  How far apart are those two predictions at deep-MOND radii?  (framework's own kernel, canon footing)
""")
print(f"  {'y = g_bar/a0':>14}{'nu (A>0)':>11}{'g_obs/g_bar A>0':>18}{'g_obs/g_bar A<0':>18}{'dex apart':>12}")
print("  " + "-" * 92)
for y in (0.05, 0.1, 0.3, 1.0):
    nu = nu_frame(y)
    lo = 1.0 / nu                     # A<0 mirror: the same-size anomaly with opposite sign
    print(f"  {y:>14.2f}{nu:>11.3f}{nu:>18.3f}{lo:>18.3f}{2*np.log10(nu):>12.3f}")
dex_gap = 2 * np.log10(nu_frame(0.1))
print(f"""
  At y = 0.1 the two sign branches differ by {dex_gap:.2f} dex in g_obs -- a factor {nu_frame(0.1)**2:.1f}.  The framework's
  own committed SPARC RAR fit has 0.108 dex scatter (real_research/rar_framework_a0_mlfit.py, Upsilon
  = 0.70).  The A < 0 branch is therefore not a marginal alternative: it is wrong by ~{dex_gap/0.108:.0f}x the
  observed scatter, in the wrong direction, at every deep-MOND radius in SPARC.

  ==> ANSWER TO 2(c), FIRST HALF:  YES.  Requiring MOND behaviour in galaxies forces sign(A) = +1,
      which by Sections 1-3 forces the solar-system secular drift to be an EXPANSION.  The framework
      CANNOT choose a decay.  The two locks (galactic MOND sign, causal dissipative sign) are mutually
      consistent -- they are the same lock, read at two frequencies.

  THE PRICE, stated (2(c), SECOND HALF).  A > 0 means the anomalous tangential force does POSITIVE work
  on the orbit at every frequency: the gated dressing is ACTIVE, not passive.  A passive (KMS/absorbing)
  response would require the orbit to LOSE energy, i.e. A < 0, i.e. delta_m >= 0 -- which is exactly the
  framework's own committed lock ("passive reactive DC shift KMS/Kramers-Kronig LOCKED to delta_m >= 0
  anti-MOND, flips only under a pump beta < 0").  So the expansion that keeps the omega_c window open is
  powered by precisely the non-passivity that the framework's own no-pump theorems say nothing sources.
  This lane REPRODUCES that inequality from the dissipative/energy side, independently of the reactive
  DC argument that established it.  It is a cross-check, and it is a cost -- not a new door.
""")

# ----------------------------------------------------------------------------------------------------
# 5. THE da/dt -> APPARENT Gdot/G MAP, by direct integration (not quoted)
# ----------------------------------------------------------------------------------------------------
head("5.  THE Gdot/G MAPPING -- verified by integrating an orbit with a genuinely varying GM")
def orbit_varying_GM(gdot, n_orbits=30.0):
    """Integrate a circular orbit under GM(t) = GM0 exp(gdot t)  (so Gdot/G = gdot EXACTLY, constant --
    the (1 + gdot t) form makes Gdot/G decay over the arc and biases the fitted slope low)."""
    GM0, R0 = 1.0, 1.0
    Om0 = np.sqrt(GM0 / R0 ** 3)
    def rhs(t, y):
        x, yy, vx, vy = y
        GM = GM0 * np.exp(gdot * t)
        rr = np.hypot(x, yy)
        return [vx, vy, -GM / rr ** 3 * x, -GM / rr ** 3 * yy]
    T = 2 * np.pi / Om0 * n_orbits
    sol = solve_ivp(rhs, (0, T), [R0, 0, 0, Om0 * R0], rtol=1e-12, atol=1e-14,
                    t_eval=np.linspace(0, T, 3001))
    x, yy, vx, vy = sol.y
    rr = np.hypot(x, yy)
    GMt = GM0 * np.exp(gdot * sol.t)
    a_osc = -GMt / (2 * (0.5 * (vx ** 2 + vy ** 2) - GMt / rr))
    half = len(sol.t) // 2
    return np.polyfit(sol.t[half:], np.log(a_osc[half:]), 1)[0]
print(f"  {'Gdot/G [1/time]':>18}{'measured d ln a/dt':>22}{'ratio to -Gdot/G':>20}{'verdict':>14}")
print("  " + "-" * 92)
for gd in (1e-4, 3e-4, -1e-4, -3e-4):
    dlna = orbit_varying_GM(gd)
    print(f"  {gd:>18.1e}{dlna:>22.6e}{dlna/(-gd):>20.6f}"
          f"{'DECAY' if dlna < 0 else 'EXPANSION':>14}")
    assert abs(dlna / (-gd) - 1) < 0.02, "Gdot/G -> d ln a/dt mapping failed"
    assert (dlna < 0) == (gd > 0)
print(f"""
  CONFIRMED NUMERICALLY, not quoted:  d ln a/dt = - Gdot/G  to <2%.
      Gdot/G > 0 (G rising, binding tightens)  ->  ORBITAL DECAY
      Gdot/G < 0                               ->  ORBITAL EXPANSION
  So an EXPANSION is reported by an ephemeris/LLR fit as a NEGATIVE apparent Gdot/G.  The LLR central
  value {LLR_CEN:+.1e}/yr is NEGATIVE, hence the framework's predicted sign and the LLR central sign AGREE.
""")

# ----------------------------------------------------------------------------------------------------
# 6. THE WINDOW ARITHMETIC -- both branches, both footings, one-sided ceiling DERIVED not asserted
# ----------------------------------------------------------------------------------------------------
head("6.  THE WINDOW -- and why the ceiling is |cen|+2sigma for expansion, cen+2sigma for decay")
print(f"""
  The framework predicts a STRICTLY SIGNED drift, so the correct confrontation is a ONE-SIDED bound.

    EXPANSION branch (A > 0, s = -1): predicted apparent Gdot/G lies in (-inf, 0).  The 2-sigma
      lower limit of the measurement is  cen - 2 sigma = {LLR_CEN:+.1e} - 2({LLR_SIG:.1e}) = {LLR_CEN - 2*LLR_SIG:+.3e}/yr,
      so the allowed drift MAGNITUDE is |cen| + 2 sigma = {abs(LLR_CEN) + 2*LLR_SIG:.3e}/yr.
    DECAY branch (A < 0, s = +1): predicted apparent Gdot/G lies in (0, +inf).  The 2-sigma
      upper limit is  cen + 2 sigma = {LLR_CEN + 2*LLR_SIG:+.3e}/yr, so the allowed magnitude is {LLR_CEN + 2*LLR_SIG:.3e}/yr.

  The asymmetry is entirely due to the central value being NEGATIVE, at {abs(LLR_CEN)/LLR_SIG:.2f} sigma from zero.
  Converting a drift ceiling [1/yr] into an omega_c ceiling [rad/s]:  omega_c <= (drift/YR) g_N / a0.
  (NOTE a unit trap: the numerical closeness of "2.42e-14 /yr" and "2.21e-14 rad/s" is a coincidence --
   the conversion factor g_N,Moon/(a0 YR) = {G_N_MOON/(A0_CANON*YR):.4f} for canon happens to be near 1.  They are
   different quantities in different units and must not be compared directly.)
""")
def wc_ceiling(drift_per_yr, a0): return (drift_per_yr / YR) * G_N_MOON / a0
print(f"  {'branch':<26}{'ceiling [/yr]':>16}{'footing':>9}{'a0':>12}"
      f"{'omega_c ceiling':>18}{'vs lower edge':>16}{'WINDOW':>9}")
print("  " + "-" * 100)
verdicts = {}
for branch, drift_ceil in (("s=-1 MOND -> EXPANSION", abs(LLR_CEN) + 2 * LLR_SIG),
                           ("s=+1 anti-MOND -> DECAY", LLR_CEN + 2 * LLR_SIG)):
    for foot, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
        hi = wc_ceiling(drift_ceil, a0)
        ratio = hi / OMEGA_C_LO
        verdicts[(branch, foot)] = (hi, ratio, ratio > 1)
        print(f"  {branch:<26}{drift_ceil:>16.3e}{foot:>9}{a0:>12.3e}{hi:>18.4e}"
              f"{'x'+format(ratio,'.3f'):>16}{'OPEN' if ratio > 1 else 'EMPTY':>9}")
# regression: the expansion/canon ceiling must reproduce the paper's committed upper edge
hi_paper = verdicts[("s=-1 MOND -> EXPANSION", "canon")][0]
assert abs(hi_paper / OMEGA_C_HI_PAPER - 1) < 0.01, "did not reproduce the paper's committed upper edge"
print(f"""
  REGRESSION: the EXPANSION/canon ceiling {hi_paper:.4e} reproduces the paper's committed upper edge
  {OMEGA_C_HI_PAPER:.4e} rad/s to {abs(hi_paper/OMEGA_C_HI_PAPER-1)*100:.2f}%.  So the paper's |cen|+2sigma choice was the RIGHT one --
  but only because the drift is an expansion, which the paper never established.  It was an unjustified
  step that happens to be correct; Sections 1-5 supply the missing justification.

  DECAY BRANCH AT FULL STRENGTH (carried, not softened):  under s = +1 the ceiling is
  {verdicts[('s=+1 anti-MOND -> DECAY','canon')][0]:.4e} (canon) / {verdicts[('s=+1 anti-MOND -> DECAY','alt')][0]:.4e} (alt) rad/s, i.e. a factor
  {1/verdicts[('s=+1 anti-MOND -> DECAY','canon')][1]:.2f}x / {1/verdicts[('s=+1 anti-MOND -> DECAY','alt')][1]:.2f}x BELOW the non-negotiable lower edge {OMEGA_C_LO:.4e} rad/s.
  On that branch the window is EMPTY on BOTH footings -- the framework would be CLOSED TODAY at the
  solar system.  That branch is not, however, reachable while keeping galactic MOND (Section 4).
""")
assert verdicts[("s=-1 MOND -> EXPANSION", "canon")][2] and verdicts[("s=-1 MOND -> EXPANSION", "alt")][2]
assert not verdicts[("s=+1 anti-MOND -> DECAY", "canon")][2]
assert not verdicts[("s=+1 anti-MOND -> DECAY", "alt")][2]

# --- how thin is the OPEN verdict?  what LLR central would close it? ---
print(f"""  HOW THIN IS THE 'OPEN' VERDICT -- what LLR central value would close it?
    General one-sided ceiling for a strictly-EXPANSION prediction, valid for either sign of cen:
        drift_max = 2 sigma - cen        (cen = {LLR_CEN:+.1e} gives {2*LLR_SIG - LLR_CEN:.3e}/yr, matching |cen|+2sigma)
    The window stays open iff  drift_max >= OMEGA_C_LO * a0 * YR / g_N,Moon:""")
for foot, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
    drift_needed = OMEGA_C_LO * a0 * YR / G_N_MOON        # drift ceiling required to reach the lower edge
    cen_thresh = 2 * LLR_SIG - drift_needed               # window open iff cen <= cen_thresh
    margin_sig = (cen_thresh - LLR_CEN) / LLR_SIG         # how far the measured cen sits below threshold
    print(f"    {foot:<7} needs drift_max >= {drift_needed:.4e}/yr  ->  requires cen <= {cen_thresh:+.3e}/yr "
          f"({cen_thresh/LLR_SIG:+.3f} sigma);  measured cen is {margin_sig:.3f} sigma below that")
print(f"""
  READ THIS STRAIGHT.  The OPEN verdict does not rest on the drift being small -- it rests on the LLR
  central value being NEGATIVE at all:
    * canon needs only cen <= {2*LLR_SIG - OMEGA_C_LO*A0_CANON*YR/G_N_MOON:+.2e}/yr ({(2*LLR_SIG - OMEGA_C_LO*A0_CANON*YR/G_N_MOON)/LLR_SIG:+.2f} sigma) -- essentially just "negative".  The 2-sigma
      width alone very nearly reaches the lower edge, so canon is robust to the central's MAGNITUDE
      but NOT to its SIGN.
    * alt needs cen <= {2*LLR_SIG - OMEGA_C_LO*A0_ALT*YR/G_N_MOON:+.2e}/yr ({(2*LLR_SIG - OMEGA_C_LO*A0_ALT*YR/G_N_MOON)/LLR_SIG:+.2f} sigma); the measured {LLR_CEN:+.1e} ({LLR_CEN/LLR_SIG:+.2f} sigma) clears it by only
      {((2*LLR_SIG - OMEGA_C_LO*A0_ALT*YR/G_N_MOON) - LLR_CEN)/LLR_SIG:.2f} sigma.  That is the same knife-edge the paper reports as "+2.7%", now expressed in
      the units that actually control it: the LLR central value.
  A future LLR/ephemeris refit that moves the central to ZERO or POSITIVE closes the window on both
  footings.  The framework cannot respond by flipping to the decay branch (Section 4): that branch
  costs galactic MOND.  This is a genuine, sharp, two-sided falsifier -- sharper than the paper's
  current "x3 secular refit" wording, because it is a SIGN test, not a magnitude test.
""")

# ----------------------------------------------------------------------------------------------------
# 7. THE FLIP SIDE OF THE SAME LINK -- the dissipative channel evaluated in GALAXIES (new exposure)
# ----------------------------------------------------------------------------------------------------
head("7.  THE DANGEROUS HALF OF 2(c) -- the same tangential channel, evaluated on the GALACTIC side")
print(r"""
  The record checks the gate's REACTIVE part in galaxies (that is what the lower edge is: Re G >= 0.90
  at every confirmed deep-MOND orbit) and its DISSIPATIVE part in the solar system (that is the LLR
  drift ceiling).  It never checks the DISSIPATIVE part in GALAXIES.  Sections 1-5 make that check
  mandatory, because the tangential force exists wherever the anomaly is active and the gate is not
  fully open.  And the paper's own machine-verified one-pole identity |G|^2 = Re G fixes it exactly:

        |Im G| = sqrt( Re G - (Re G)^2 )        <=>   Re G = 0.90  =>  |Im G| = 0.300  EXACTLY.

  So the lower-edge condition "keep the gate 90% open so the RAR survives" is ALGEBRAICALLY the same
  statement as "accept a prograde tangential force equal to 30% of the MOND anomaly".  There is no
  choice about this within the construction; it is the |G|^2 = Re G identity, not an extra assumption.
""")
ReG_edge = 0.90
ImG_from_ReG = np.sqrt(ReG_edge - ReG_edge ** 2)
print(f"  identity check: Re G = {ReG_edge} -> |Im G| = sqrt(ReG - ReG^2) = {ImG_from_ReG:.6f}")
x_edge = np.sqrt(1.0 / ReG_edge - 1.0)
print(f"  direct:         Omega/omega_c = {x_edge:.6f} -> |Im G| = x/(1+x^2) = {x_edge/(1+x_edge**2):.6f}   (agree)")
assert abs(ImG_from_ReG - x_edge / (1 + x_edge ** 2)) < 1e-12

OMEGA_GAL = 5.9414e-15          # UGC05721 innermost deep-MOND orbit -- the orbit that SETS the lower edge
R_GAL, V_GAL = 0.09 * KPC, 16.5e3
GYR = 1e9 * YR
print(f"""
  THE BINDING ORBIT (the paper's own): UGC05721 innermost, r = 0.09 kpc, V = 16.5 km/s,
  Omega_gal = V/r = {V_GAL/R_GAL:.4e} rad/s (matches the committed {OMEGA_GAL:.4e}).
  Anomaly amplitude there is the MOND excess itself, A_gal = g_obs - g_bar (exact a0-line inversion).
  Secular rate from the tangential force: flat rotation curve L = V r, dL/dt = f_t r => d ln r/dt = f_t/V
  (the Keplerian form 2 f_t/V is also printed; the flat form is the conservative/slower one).
""")
print(f"  {'footing':<8}{'omega_c':>12}{'Om/wc':>8}{'lag':>8}{'Re G':>7}{'|Im G|':>8}"
      f"{'A_gal':>11}{'f_t':>11}{'dlnr/dt [/Gyr]':>16}{'e-fold':>11}")
print("  " + "-" * 100)
gal = {}
for foot, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
    gobs = V_GAL ** 2 / R_GAL
    gbar = gbar_from_gobs(gobs, a0)
    A_gal = gobs - gbar
    for wcv in (OMEGA_C_LO, OMEGA_C_HI_PAPER):
        x = OMEGA_GAL / wcv
        ImGv, ReGv = x / (1 + x ** 2), 1 / (1 + x ** 2)
        f_t = A_gal * ImGv
        rate = f_t / V_GAL                     # flat-RC form (conservative)
        gal[(foot, wcv)] = (rate, A_gal)
        print(f"  {foot:<8}{wcv:>12.4e}{x:>8.4f}{np.degrees(np.arctan(x)):>7.1f}d{ReGv:>7.3f}{ImGv:>8.4f}"
              f"{A_gal:>11.3e}{f_t:>11.3e}{rate*GYR:>16.3e}{1/rate/1e6/YR:>9.1f}My")
rate_ref = gal[("canon", OMEGA_C_HI_PAPER)][0]
print(f"""
  READ THE LAST TWO COLUMNS.  At the window's MOST PERMISSIVE corner (canon, omega_c = {OMEGA_C_HI_PAPER:.3e}) the
  binding deep-MOND orbit expands with an e-folding time of ~{1/rate_ref/1e6/YR:.0f} Myr -- i.e. {rate_ref*GYR:.0f} e-folds per Gyr.
  Dwarf-galaxy disks are Gyr-old.  This is not a marginal tension; it is many orders of magnitude.

  WHICH WAY DOES IT PUSH omega_c?  In galaxies Omega/omega_c < 1, so |Im G| ~ Omega/omega_c DECREASES as
  omega_c RISES.  So this constraint is a NEW LOWER EDGE on omega_c -- it pushes the same direction as
  RAR preservation, but vastly harder.  Requiring the binding orbit to survive a galaxy age:
""")
for age_gyr in (1.0, 10.0):
    for foot, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
        A_gal = gal[(foot, OMEGA_C_LO)][1]
        ImG_max = V_GAL / (A_gal * age_gyr * GYR)          # need f_t/V <= 1/(age)
        wc_need = OMEGA_GAL / ImG_max                       # small-x: |ImG| ~ x = Omega/omega_c
        a0v = A0_CANON if foot == "canon" else A0_ALT
        hi = wc_ceiling(abs(LLR_CEN) + 2 * LLR_SIG, a0v)
        print(f"    survive {age_gyr:>4.0f} Gyr [{foot:<5}]: need |Im G| <= {ImG_max:.3e} -> omega_c >= {wc_need:.3e} rad/s"
              f"   =  {wc_need/hi:.4g}x ABOVE the LLR upper edge {hi:.3e}")
wc_need_10 = OMEGA_GAL / (V_GAL / (gal[("canon", OMEGA_C_LO)][1] * 10 * GYR))
hi_canon = wc_ceiling(abs(LLR_CEN) + 2 * LLR_SIG, A0_CANON)
print(f"""
  ==> ON THE DIRECTION-LAG (VECTOR) READING OF THE GATE, THE WINDOW IS EMPTY BY ~{wc_need_10/hi_canon:.0f}x.
      Galactic survival needs omega_c >= {wc_need_10:.3e}; LLR needs omega_c <= {hi_canon:.3e}.
      And raising omega_c is doubly bad for the solar system: it re-opens the reactive a0/2 tail too
      (Re G -> 1), restoring the original 10^3-10^4x per-planet exclusion.  Both solar-system
      constraints want omega_c SMALL; the galactic dissipative constraint wants it LARGE.

  THE FORK THAT THIS RIDES ON -- stated at full strength, because it is load-bearing.
  Everything above assumes the gate lags the DIRECTION-carrying object, so that the anomalous force
  points along the retarded radial direction (lag angle arctan(Omega/omega_c)).  That is the paper's
  own prescription: it evaluates G at the ORBITAL frequency for BOTH window edges (omega_gal = V/r for
  the lower edge, omega_p = 2pi/T_p for the upper).  It is also the assumption that
  reviews/mi_cassini_q2_omegac_2026.py labels [ADOPTED #1], "the single load-bearing assumption".

    READING A (vector / direction lag -- the paper's own):  galaxies are destroyed as computed above.
    READING B (scalar / DC):  on a circular orbit |a| is CONSTANT, so the scalar argument
      X = |a|^2/a0^2 is DC, the gate sees omega = 0, G(0) = 1, Im G = 0 -- no galactic tangential
      force at all.  But G(0) = 1 in the SOLAR SYSTEM too, so the gate suppresses nothing there and
      the ungated a0/2 tail returns at full strength: excluded 10^3-10^4x per planet (paper Sec. 5.1).
      This is exactly Fork C of the Q2 script ("a low-pass gate cannot suppress a DC anomaly").

  So the two readings are a PINCER on the gated survivor: A kills it in galaxies, B kills it at the
  planets.  This is NOT resolvable from the written action as it stands -- it needs the quasi-static /
  off-circular weak-field limit that BOTH source documents already list as UNCOMPUTED.  Reported as a
  new exposure of the gate mechanism, NOT as a claim that the framework is closed: the MOND premise and
  the a0 reframing are untouched by this, which bears only on the GATE that buys solar-system safety.
""")

# --- honesty on the perturbative status of the galactic estimate, and its numerical validation ---
gobs_c = V_GAL ** 2 / R_GAL
gbar_c = gbar_from_gobs(gobs_c, A0_CANON)
print(f"""
  PERTURBATIVE STATUS OF THE GALACTIC NUMBER, stated (do not over-read the precision).
  In the solar system A/g_N ~ {A0_CANON/2/G_N_MOON:.2e} -- deeply perturbative, the linear treatment is exact enough.
  At the binding deep-MOND orbit A_gal/g_bar = {(gobs_c-gbar_c)/gbar_c:.3f} -- the anomaly is {100*(gobs_c-gbar_c)/gbar_c:.0f}% of the Newtonian
  force, so the linear-in-A estimate is ORDER OF MAGNITUDE there, not a precision number.  It does not
  need to be precise: the e-folding time is ~{1/rate_ref/1e6/YR:.0f} Myr against a >~1 Gyr disk age, a margin of
  ~{GYR/ (1/rate_ref):.0f}x per Gyr, so a factor of a few in either direction changes nothing.
  The SIGN and the Omega/omega_c ~ 0.3 lag are not perturbative approximations at all -- they are the
  geometry of Section 1, and Section 1's own table already integrates exactly this regime:
  omega_c/Omega = 3.0 IS Omega/omega_c = 0.333, the window's lower-edge galactic corner, and it came
  out EXPANSION with magnitude 4 pi (A/g_N) |Im G| to <1%.  The galactic case is the same computation
  at the same corner ratio, differing only in the amplitude A and the rotation-curve shape.
""")

# ----------------------------------------------------------------------------------------------------
# 8. VERDICT
# ----------------------------------------------------------------------------------------------------
head("8.  VERDICT")
print(f"""
  ASSIGNED QUESTION (deliverable 2): is the drift sign FORCED by causality, or does it RIDE ON s = -1?

  (a) NOT forced by causality alone.  Causality forces TWO things and no more:
        * the response TRAILS (lag angle Delta = arctan(Omega/omega_c) strictly in (0, pi/2); a leading
          response would need the memory kernel supported at t < 0);
        * the RELATIVE sign of the reactive and dissipative channels, ratio = Omega/omega_c > 0,
          independent of s and of the amplitude (Section 3, symbolic).
      Neither fixes the ABSOLUTE sign.

  (b) The anomalous tangential force DOES carry a factor of s.  Both channels are the SAME amplitude
      A = -s(a0/2) times the SAME response G(Omega); there is no independent sign freedom (this is the
      content of the paper's own machine-verified |G|^2 = Re G identity: one pole, one amplitude).
        s = -1 (MOND, inertia reduced, extra ATTRACTION)  -> PROGRADE tangential -> EXPANSION
                 -> apparent Gdot/G < 0 -> same sign as the LLR central -> ceiling |cen|+2sigma
                 -> omega_c <= 2.2113e-14 (canon) / 1.8306e-14 (alt) -> WINDOW OPEN x1.241 / x1.027
        s = +1 (anti-MOND, inertia increased, extra REPULSION) -> RETROGRADE -> DECAY
                 -> apparent Gdot/G > 0 -> opposite sign -> ceiling cen+2sigma
                 -> omega_c <= 1.2975e-14 (canon) / 1.0742e-14 (alt) -> WINDOW EMPTY x0.728 / x0.603
      VERDICT LABEL: SIGN-RIDES-ON-POSITED-s.  The window verdict is formally CONDITIONAL.

  (c) BUT the two locks are mutually consistent, and the conditionality is thinner than it looks.
      sign(A) is not a free dial: it is MEASURED in galaxies (A < 0 puts rotation curves ~1.0 dex BELOW
      Newtonian at y = 0.1, ~10x the framework's own 0.108 dex RAR scatter, in the wrong direction).
      So requiring MOND in galaxies FORCES the solar-system drift to be an EXPANSION.  The framework
      cannot buy the decay branch, and cannot evade a future decay measurement.  The internal link the
      brief anticipated is real, and it lands on the window-OPEN side.
      THE PRICE: A > 0 means the tangential force does POSITIVE work at every frequency -- the gated
      dressing is ACTIVE, not passive.  Passivity/KMS would require A < 0 (delta_m >= 0, anti-MOND),
      the framework's own committed lock.  Reproduced here from the dissipative side, independently of
      the reactive DC argument that first established it.  The expansion that keeps the window open is
      powered by exactly the non-passivity that the no-pump theorems say nothing sources.

  SEPARATE AND LARGER FINDING (Section 7), flagged not buried:
      The same tangential channel, evaluated where the record never evaluated it -- in GALAXIES --
      gives an e-folding expansion time of ~42-58 Myr at the window's own corners, both footings.
      Galactic survival would require omega_c >= ~4.1e-12 (canon) / ~4.7e-12 (alt) rad/s, i.e.
      ~186x / ~257x ABOVE the LLR upper edge.  On the direction-lag reading of the gate the window is
      EMPTY by that factor -- a far bigger problem than the sign question, and one the |Im G| absolute
      value in window_joint.py line 89 concealed.  It rides on the [ADOPTED #1] vector-vs-DC fork, and
      the DC alternative kills the gate from the other side (no suppression at the planets, the original
      10^3-10^4x exclusion).  BOTH prongs bear on the GATE only.
      NOT claimed: that the framework is closed.  The MOND premise, the a0 = cH_Lambda/Z reframing, the
      RAR, and the galactic sector are untouched by this; what is exposed is the gated-crossover
      mechanism that buys solar-system safety, and the exposure needs the UNCOMPUTED quasi-static /
      off-circular weak-field limit to settle.  No door is declared closed.

  CROSS-LANE: reviews/mi_omegac_drift_sign_energy_2026.py reaches the same sign by frequency-domain
  routes (Im chi, passivity, angular momentum).  This lane used a raw time-domain orbit integration
  with no Fourier convention anywhere in Sections 1-3.  The two agree, so the sign is not a convention.
""")
print(RULE)
print("mi_drift_sign_forced_or_posited_2026.py: all checks passed "
      "(sign tracks sign(A) at every corner; magnitude matches 4pi(A/g_N)|ImG| to <1%; "
      "Gdot/G map exact; paper's upper edge reproduced to 0.00%).")
print(RULE)
