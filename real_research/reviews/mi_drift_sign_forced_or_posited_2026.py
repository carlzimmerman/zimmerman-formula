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
