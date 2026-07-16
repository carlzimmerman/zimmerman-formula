#!/usr/bin/env python3
r"""
CD1 -- THE FREQUENCY FINGERPRINT AS AN OBSERVABLE: wide-binary gamma, Gaia DR3/DR4 reach,
       and the solar-system limit of the published MI kernel (BOTH CHANNELS, BOTH FOOTINGS).
==========================================================================================
Framework (Carl Zimmerman): de Sitter-Unruh MODIFIED INERTIA (not standard MOND).
  a0 = c H_Lambda / Z = 9.36e-11 m/s^2 (canonical, rho_DE); ALT footing 1.13e-10 (rho_total/cH0).
  Own interpolation nu(y) = sqrt(1 + 1/y), y = g_bar/a0  <=>  inertia dressing
  mu_fw(x) = (sqrt(1+4x^2)-1)/(2x), x = |a|/a0  (exact inverse pair, rb1 Theorem A).
Published action: S_m = -(1/2) Int rho_m [s u K(box_u/a0^2) u], K Herglotz-Nevanlinna,
  measure UNIQUE (Herglotz class + RAR calibration, rb2[3]), retarded boundary value
  K(-w^2+i0) = exp(i arcsin(1/(2w))) EXACTLY for w = omega c/a0 >= 1/2 (rb2[2]).

WHAT THIS SCRIPT DOES (Lane CD, task 1):
  [1] Turns the rb2 frequency split into the WIDE-BINARY OBSERVABLE gamma_v and confronts
      the banked Gaia DR3 dry-run (gamma = 1.205 +/- 0.035, prep_2026/gaia_dr4_prep/) and
      the banked DR4 error model (sigma(gamma) = 0.0191 @ N=30k).
  [2] Solar-system FREQUENCY channel: verifies the kernel phase suppression at planetary
      frequencies (this is the channel the kernel actually adds on top of nu).
  [3] Solar-system AMPLITUDE channel: the forced high-x tail mu_fw -> 1 - 1/(2x), i.e. a
      universal extra sunward acceleration -> a0/2, confronted with the PLANETARY EPHEMERIS
      supplementary perihelion precessions (Pitjev & Pitjeva 2013, EPM2011, fetched values).
      This is reported with the SAME rigor as the wins: it is a wall on the closure family,
      quantified, with the two named escapes and their own testable side-effects.
  [4] The frequency-gate requirement implied by [3] + the RAR, and what it would do to
      wide binaries (a DR4-testable side-effect).

Sources for every external number are cited inline. Exit 0 <=> all checks pass.
"""
import numpy as np
import sys

CHECKS = []
def check(name, ok):
    CHECKS.append((name, bool(ok)))
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}")

def hdr(s):
    print("\n" + "#" * 100)
    print("# " + s)
    print("#" * 100)

# ---------------------------------------------------------------- constants + both footings
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
AU   = 1.495978707e11
YR   = 3.15576e7
MAS  = 1.0 / (206264.806 * 1000.0)      # 1 mas in rad
FOOTINGS = {"canonical rho_DE (cH_Lambda/Z)": 9.36e-11,
            "alt rho_total (cH0)":            1.13e-10}

def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)

def nu_fw(y):
    return np.sqrt(1.0 + 1.0 / np.asarray(y, float))

def phase(w):
    """Retarded kernel phase phi(w) = arcsin(1/(2w)) on the physical branch (rb2[2])."""
    return np.arcsin(1.0 / (2.0 * np.asarray(w, float)))

# ================================================================================================
hdr("[1] WIDE-BINARY OBSERVABLE: the kernel's omega-dependence mapped to gamma_v")
# ================================================================================================
# Circular balance with the reactive (conservative) part of the kernel phase:
#     mu_fw(x) * cos(phi(w)) * x = y ,   w = omega c / a0 = x * (c / v)   (omega = a/v on a circle)
# nu_eff = x / y. The wide-binary gamma_v observable of the banked pipeline is the deep-regime
# velocity boost v/v_N = sqrt(g_obs/g_bar) = sqrt(nu), so  d(gamma)/gamma = (1/2) d(nu)/nu.
def nu_eff(y, v, a0):
    cv = c / v
    x = y * nu_fw(y)                       # zero-phase seed
    for _ in range(60):                    # fixed point on the exact balance
        w = x * cv
        x = np.sqrt(y**2 / np.cos(phase(w))**2 / mu_fw(x)**2 * mu_fw(x)**2) if False else x
        # solve mu_fw(x)*cos(phi)*x = y by Newton on f(x)
        f  = mu_fw(x) * np.cos(phase(x * cv)) * x - y
        dx = 1e-7 * x
        fp = (mu_fw(x + dx) * np.cos(phase((x + dx) * cv)) * (x + dx) - y - f) / dx
        x  = x - f / fp
    return x / y

V_WB, V_DSPH, V_GAL = 0.45e3, 10e3, 150e3   # m/s: wide binary, dSph, galaxy-outskirt speeds (rb2)
print("\n  Delta nu / nu and Delta gamma_v / gamma_v (wide binary vs galactic calibration, same y):")
print(f"  {'footing':<34}{'y':>6}{'nu_gal/nu_wb-1':>17}{'dgamma/gamma':>15}")
split_bank = {}
for lab, a0 in FOOTINGS.items():
    for y in (1.0, 0.3, 0.1):
        ng = nu_eff(y, V_GAL, a0); nw = nu_eff(y, V_WB, a0)
        dnu = ng / nw - 1.0
        split_bank[(lab, y)] = dnu
        print(f"  {lab:<34}{y:>6.2f}{dnu:>17.3e}{0.5*dnu:>15.3e}")
ok = abs(split_bank[("canonical rho_DE (cH_Lambda/Z)", 1.0)] - 2.3e-8) < 0.7e-8
check("reproduces rb2: Delta nu/nu (wb vs gal, y=1) = +2.3e-8 (+-30%), galactic MORE boosted", ok)
sp = [abs(split_bank[(l, 1.0)]) for l in FOOTINGS]
check("footing-independence: both footings give the same 1e-8-scale split (spread < 3x)",
      max(sp) / min(sp) < 3.0)

DG = 0.5 * split_bank[("canonical rho_DE (cH_Lambda/Z)", 1.0)]   # gamma shift at y=1
print(f"""
  CONFRONTATION WITH THE BANKED GAIA NUMBERS (prep_2026/gaia_dr4_prep/wide_binary_pipeline.out):
    * DR3-era dry run (El-Badry+2021 eDR3 cuts, contamination-biased HIGH by construction):
        gamma = 1.205 +/- 0.035 (canonical) / 1.2025 +/- 0.0337 (alt).
      The kernel's frequency shift d(gamma) = {DG:.2e} is {DG/0.035:.1e} of that error bar:
      the dry run cannot see it, and NOTHING in the dry-run value is attributable to omega-dependence.
    * DR4 error model: sigma(gamma) = 0.0191 at N = 30,000 pairs (gates PASS at 1.00/1.09/1.33).""")
N30, SIG30 = 30000, 0.0191
N_needed = N30 * (3.0 * SIG30 / DG) ** 2
print(f"    * N(pairs) for a 3-sigma detection of d(gamma) = {DG:.1e}:  N ~ {N_needed:.1e}")
print(f"      (Gaia's entire usable wide-binary reservoir is ~1e6-1e7 pairs: shortfall ~ {N_needed/1e7:.0e}x.)")
check("frequency fingerprint is UNRESOLVABLE by Gaia DR4 (N needed > 1e15 pairs)", N_needed > 1e15)
# what DR4 CAN resolve in the frequency channel:
dnu_min_2sig = 2.0 * 2.0 * SIG30 / 1.09    # 2-sigma on nu split via gamma (dnu = 2 dgamma/gamma)
print(f"""
  WHAT DR4 *CAN* SEE: the smallest frequency-split RAR it can resolve at 2 sigma (N=30k) is
    |Delta nu / nu| ~ {dnu_min_2sig:.3f}  (~{100*dnu_min_2sig:.1f}%).
  => DR4 is blind to the published kernel's omega-dependence (1e-8) by ~6 orders, but it CAN
     kill/confirm O(10%) orbital-frequency-corner MI closures (Milgrom-1994-style averaging with a
     corner at the orbital scale). For the published kernel the DR4 wide-binary gamma is therefore a
     PURE EFE-channel measurement: banked framework-MI target gamma_v ~ 1.09 (band 1.05-1.10),
     vs MG-with-same-nu 1.137, vs Newton 1.00 -- exactly the pre-registered Door-4A ladder.
  FALSIFIER (kernel side): ANY confirmed frequency-split RAR at fixed g_bar beyond ~1e-7
     kills the published kernel outright (measure uniqueness, rb2[3] -- no freedom to absorb it).""")

# ================================================================================================
hdr("[2] SOLAR SYSTEM, FREQUENCY (PHASE) CHANNEL: kernel suppression VERIFIED")
# ================================================================================================
planets = [
    # name,     a [AU],    P [yr],    e        (IAU nominal orbital elements)
    ("Mercury", 0.38710,   0.24085,  0.20564),
    ("Earth",   1.00000,   1.00000,  0.01671),
    ("Mars",    1.52368,   1.88085,  0.09340),
    ("Saturn",  9.58200,  29.45700,  0.05650),
]
print("\n  w = omega c/a0, reactive fractional correction 1-cos(phi) ~ 1/(8w^2), phase phi = 1/(2w):")
for lab, a0 in FOOTINGS.items():
    print(f"  -- {lab}: tau_diss = 2c/a0 = {2*c/a0/YR/1e9:.0f} Gyr (universal perturbation-decay scale)")
    for nm, aau, P, e in planets:
        om = 2 * np.pi / (P * YR)
        w = om * c / a0
        print(f"     {nm:<8} omega={om:.2e}/s  w={w:.2e}  phi={phase(w):.2e} rad  1-cos(phi)={1-np.cos(phase(w)):.2e}")
w_sat = (2 * np.pi / (29.457 * YR)) * c / FOOTINGS["canonical rho_DE (cH_Lambda/Z)"]
check("Saturn reactive correction 1-cos(phi) < 1e-20 (vs ephemeris sensitivity ~1e-9 fractional): "
      "frequency channel SAFE by > 10 orders", (1 - np.cos(phase(w_sat))) < 1e-20)
print("""  The dissipative phase acts only on PERTURBATIONS about the orbit (first-moment closure:
  orbital DC dynamics are dressed by the real K(a^2/a0^2); rb2[5]) with decay/gain scale
  2c/a0 ~ 200 Gyr -- ~1e-11/yr fractional, invisible to ephemerides. Under the (already dead)
  literal closure the same phase would be a secular drift a0/2c ~ 0.4 m/yr in the Earth-Sun
  distance -- the ephemeris kill of THAT closure, consistent with rb1[3].""")

# ================================================================================================
hdr("[3] SOLAR SYSTEM, AMPLITUDE (DC) CHANNEL: the forced tail -> a0/2 -- THE HONEST WALL")
# ================================================================================================
print(r"""
  The circular balance of the surviving (RAR-reproducing) first-moment closure family inverts
  EXACTLY (rb1 Theorem A):  x = sqrt(y^2 + y),  so the extra acceleration over Newton is
      delta_a = a0 (x - y) = a0 [sqrt(y^2+y) - y]  --->  a0/2  for y >> 1 (all planets),
  a UNIVERSAL constant sunward anomaly. This tail is FORCED: the Herglotz measure is unique
  (rb2[3]), circles are closure-degenerate WITHIN the first-moment family (rb1[4]), and every
  time-weighting of |a|^2 on Saturn's worldline is dominated by the planetary term
  (galactic contribution to <|a|^2> is fractionally ~1e-9). No knob exists inside the family.

  Secular apsidal precession of a constant radial perturbation R = -delta_a (Gauss equation,
  time-averaged <cos f> = -e):   pomega_dot = -delta_a sqrt(1-e^2) / (n a)   (retrograde).

  EPHEMERIS CONFRONTATION -- fetched, not from memory: Pitjev & Pitjeva 2013 (Astron. Lett. 39,
  141; arXiv:1306.3043), Table 4, EPM2011 'additional perihelion precessions' [mas/yr]:
      Mercury -0.020   +/- 0.030
      Earth    0.0019  +/- 0.0019
      Mars    -0.00020 +/- 0.00037
      Saturn  -0.0032  +/- 0.0047     (Cassini-era; Iorio 2018 arXiv:1810.13415: EPM2017-class
                                       perihelion-rate uncertainties ~1 mas/cty for Saturn,
                                       formal, with a suggested realistic inflation kappa ~ 10-50)
""")
EPHEM = {  # mas/yr, 1-sigma, Pitjev & Pitjeva 2013 Table 4 (EPM2011)
    "Mercury": 0.030, "Earth": 0.0019, "Mars": 0.00037, "Saturn": 0.0047}
wall = {}
for lab, a0 in FOOTINGS.items():
    print(f"  -- footing: {lab}  (a0/2 = {a0/2:.2e} m/s^2)")
    print(f"     {'planet':<9}{'y=gN/a0':>10}{'delta_a':>11}{'pred pomega_dot':>17}{'EPM2011 1sig':>14}{'|N_sigma|':>11}{'x10 infl.':>11}")
    for nm, aau, P, e in planets:
        a_m = aau * AU
        n = 2 * np.pi / (P * YR)
        gN = G * Msun / a_m ** 2
        y = gN / a0
        da = a0 * (np.sqrt(y * y + y) - y)          # exact, not just a0/2
        pom = da * np.sqrt(1 - e * e) / (n * a_m)   # rad/s
        pom_masyr = pom / MAS * YR
        nsig = pom_masyr / EPHEM[nm]
        wall[(lab, nm)] = nsig
        print(f"     {nm:<9}{y:>10.2e}{da:>11.3e}{pom_masyr:>14.2f} mas/yr{EPHEM[nm]:>11.4f}{nsig:>11.0f}{nsig/10:>11.0f}")
check("Saturn: predicted ~31 mas/yr vs 0.0047 mas/yr -> excluded at ~6.7e3 sigma (canonical)",
      6000 < wall[("canonical rho_DE (cH_Lambda/Z)", "Saturn")] < 7500)
check("Mars: excluded at ~3.4e4 sigma (canonical); >300 sigma even with x100 error inflation",
      wall[("canonical rho_DE (cH_Lambda/Z)", "Mars")] > 3e4)
check("both footings excluded (alt footing is ~21% WORSE, not better)",
      wall[("alt rho_total (cH0)", "Saturn")] > wall[("canonical rho_DE (cH_Lambda/Z)", "Saturn")])

# --- numerical cross-check of the Gauss formula: integrate a perturbed Kepler orbit
def apsidal_drift(delta_a0, a_m, e, n_orbits=60, steps_per_orbit=6000):
    """2D integrator, force = -GM/r^2 - delta_a(r) (sunward); returns d(pomega)/dt [rad/s]."""
    GM = G * Msun
    P = 2 * np.pi * np.sqrt(a_m ** 3 / GM)
    dt = P / steps_per_orbit
    r0 = a_m * (1 - e)
    v0 = np.sqrt(GM / a_m * (1 + e) / (1 - e))
    pos = np.array([r0, 0.0]); vel = np.array([0.0, v0])
    def acc(p):
        r = np.hypot(*p)
        return -(GM / r ** 2 + delta_a0) * p / r
    peri_angles, peri_times = [], []
    rprev2, rprev = None, None; t = 0.0
    aold = acc(pos)
    for i in range(int(n_orbits * steps_per_orbit)):
        pos = pos + vel * dt + 0.5 * aold * dt * dt
        anew = acc(pos)
        vel = vel + 0.5 * (aold + anew) * dt
        aold = anew; t += dt
        r = np.hypot(*pos)
        if rprev2 is not None and rprev < rprev2 and rprev < r:   # local min = perihelion
            peri_angles.append(np.arctan2(pos[1], pos[0])); peri_times.append(t)
        rprev2, rprev = rprev, r
    th = np.unwrap(np.array(peri_angles)); tt = np.array(peri_times)
    return np.polyfit(tt, th, 1)[0]
a0c = FOOTINGS["canonical rho_DE (cH_Lambda/Z)"]
a_mer = 0.38710 * AU
num = apsidal_drift(a0c / 2, a_mer, 0.20564)
n_mer = 2 * np.pi / (0.24085 * YR)
ana = -(a0c / 2) * np.sqrt(1 - 0.20564 ** 2) / (n_mer * a_mer)
print(f"\n  numeric cross-check (Mercury, delta_a = a0/2): integrator {num:.3e} rad/s "
      f"vs Gauss {ana:.3e} rad/s (ratio {num/ana:.3f})")
check("orbit-integrator reproduces the Gauss secular formula within 10%", abs(num / ana - 1) < 0.10)

print("""
  OWNERSHIP AND SHARING (framework's own terms):
  * This wall does NOT come from the kernel's omega-dependence (channel [2] is clean); it is the
    DC amplitude tail of nu(y) = sqrt(1+1/y) itself: nu - 1 -> 1/(2y), the SLOWEST tail in the
    MOND-IF families. It is MOND-SHARED with modified-GRAVITY-with-the-same-nu (AQUAL/QUMOND
    around a dominant point mass give the same local law), i.e. it is the same knife as the
    published RAR-vs-Cassini-Q2 tension (Desmond-Hees-Famaey 2024; Famaey-Durakovic 2025:
    'modified gravity MOND needs a new scale in addition to acceleration ... to pass Solar
    System constraints, or that MOND rather results from a more radical modification of
    inertia') -- here in its DIRECT perihelion form, computed for the framework's nu.
  * WITHIN the published action, the exposure lands on the CLOSURE MAP (the O(1) open item,
    rb1[3]/rb2[6]): every member of the RAR-reproducing first-moment family inherits the tail;
    the literal-frequency closure evades Saturn but has no MOND and its own ephemeris kill.
    So the ephemerides do not falsify the ACTION; they falsify the closure family used so far
    and turn 'off-circular completion FREE (bounded)' into a QUANTITATIVE requirement ([4]).
  * This is a DEFICIT finding verified at the same rigor as the wins (pre-flight per working
    rule: rar_framework_a0_mlfit.py re-run 2026-07-16 -> 0.108 dex @ Upsilon=0.70, the RAR
    itself is NOT the issue; the issue is the y >> 1 analytic tail, which SPARC never probes:
    at the SPARC maximum y ~ 1e2 the tail is a 0.002-dex effect, 50x below the RAR scatter).""")

# ================================================================================================
hdr("[4] THE IMPLIED FREQUENCY GATE -- and its DR4-testable side effect")
# ================================================================================================
# Requirement: an amplitude-channel suppression S(w) multiplying the MOND boost, with
#   S(w_gal) ~ 1 (RAR intact; allow <~1% suppression at the galactic calibration points)
#   S(w_planet) <= 1/N_sigma (ephemeris safe at 1 sigma)
# Kepler circles: w = x c/v. Representative points (canonical footing):
regimes = []
for nm, v, y in [("galaxy outskirt", 150e3, 0.5), ("galaxy inner", 180e3, 10.0),
                 ("dSph", 10e3, 0.1), ("wide binary", 0.45e3, 0.15),
                 ("Saturn", 9.68e3, None), ("Mars", 24.1e3, None), ("Mercury", 47.4e3, None)]:
    if y is None:
        aau = {"Saturn": 9.582, "Mars": 1.52368, "Mercury": 0.3871}[nm]
        gN = G * Msun / (aau * AU) ** 2
        y = gN / a0c
    x = y * nu_fw(y)
    w = x * c / v
    regimes.append((nm, y, w))
    print(f"   {nm:<16} y={y:9.2e}   w = x c/v = {w:9.2e}")
w_gal_in = dict((r[0], r[2]) for r in regimes)["galaxy inner"]
w_mars = dict((r[0], r[2]) for r in regimes)["Mars"]
w_wb = dict((r[0], r[2]) for r in regimes)["wide binary"]
w_dsph = dict((r[0], r[2]) for r in regimes)["dSph"]
S_need_mars = 1.0 / wall[("canonical rho_DE (cH_Lambda/Z)", "Mars")]
# single-power gate S = 1/(1 + w/w_c): keep inner galaxies at >= 99%
w_c = w_gal_in * 99.0
S = lambda w: 1.0 / (1.0 + w / w_c)
print(f"""
  Required: S(w_gal,inner={w_gal_in:.1e}) >= 0.99  AND  S(w_Mars={w_mars:.1e}) <= {S_need_mars:.1e}.
  A single-power corner S = 1/(1+w/w_c) with w_c = {w_c:.2e} (99% at the inner-galaxy point) gives
     S(Mars)   = {S(w_mars):.2e}  (need <= {S_need_mars:.1e})  -> {'PASS' if S(w_mars)<=S_need_mars else 'FAIL'}
     S(Saturn) = {S(dict((r[0],r[2]) for r in regimes)['Saturn']):.2e}
     corner frequency omega_c = w_c a0/c = {w_c*a0c/c:.2e} s^-1  (period ~ {2*np.pi/(w_c*a0c/c)/YR/1e6:.0f} Myr)
  i.e. the ephemerides + the RAR jointly demand an amplitude corner at a GALACTIC-DYNAMICAL
  timescale (10-100 Myr periods), 4-5 dex away from the published kernel's own memory corner
  (w = 1/2, period ~ 1275 Gyr, the horizon scale). That corner is NOT in the published action:
  it is new physics the closure map would have to supply (exactly Milgrom-1994's averaging
  postulate, made quantitative).""")
check("a p=1 frequency gate at w_c ~ 1e5 rescues Mars/Saturn while keeping inner galaxies at 99%",
      S(w_mars) <= S_need_mars and S(w_gal_in) >= 0.989)
print(f"""
  THE TESTABLE SIDE EFFECT (this is what makes the gate honest rather than a tuned patch):
  wide binaries sit at w ~ {w_wb:.1e} and dSphs at w ~ {w_dsph:.1e} -- BETWEEN galaxies and planets.
  The same p=1 gate that rescues the ephemerides predicts
     S(wide binary) = {S(w_wb):.2f}   -> the WB MOND boost is quenched to ~{100*S(w_wb):.0f}% of full:
                        gamma_v -> ~ 1 + {S(w_wb):.2f} x (gamma_v,EFE - 1) ~ {1+S(w_wb)*0.09:.3f} (vs banked 1.09)
     S(dSph)        = {S(w_dsph):.2f}   -> dwarf dispersions mildly suppressed (~{100*(1-S(w_dsph))*0.5:.0f}% in sigma)
  => Gaia DR4 (sigma_gamma = 0.019 @ 30k pairs) SEPARATES the gated closure (~{1+S(w_wb)*0.09:.2f}) from the
     ungated kernel's EFE band (1.05-1.10) at ~{abs(S(w_wb)*0.09-0.09)/ (0.0191):.0f}-sigma-class if the gate is p=1 at w_c={w_c:.0e};
     steeper gates (p=2, corner nearer w~1e6) leave WBs untouched -- DR4 then cannot distinguish,
     and the discriminant moves to dSph internal kinematics (cd2 lane) and inner-disk shapes.
  HONESTY: the gate is NOT derived; it is the quantified REQUIREMENT the solar system imposes on
  the open closure item, with its parameter window and observable consequences stated. The
  published first-moment closure family as it stands FAILS the ephemeris test at 1e3-1e4 sigma.""")

# ================================================================================================
hdr("SUMMARY OF CHECKS")
# ================================================================================================
bad = [n for n, ok in CHECKS if not ok]
for n, ok in CHECKS:
    print(f"   {'PASS' if ok else 'FAIL'}  {n}")
print("\n" + "=" * 100)
print(f" CD1 RESULT: {'ALL CHECKS PASS' if not bad else 'FAILURES: ' + '; '.join(bad)}")
print("=" * 100)
sys.exit(0 if not bad else 1)
