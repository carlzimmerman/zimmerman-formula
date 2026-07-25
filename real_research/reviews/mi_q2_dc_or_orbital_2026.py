#!/usr/bin/env python3
r"""
Q-II: IS THE Q2-GENERATING PIECE DC OR ORBITAL-FREQUENCY?  (Fork C tested, not assumed)
=======================================================================================
Fork C of reviews/mi_cassini_q2_omegac_2026.py claims: the EFE quadrupole is a genuinely STATIC
(DC) anomaly, Re G(0) = 1 for every omega_c, hence a low-pass gate can never suppress it, hence
Q2 is omega_c-UNFIXABLE and the inherited boost stands undiminished (~20% on the framework's own
nu, 28% on McGaugh's, i.e. ~10-14x over the 2% Cassini allowance).

The possible error to test: Box_u is a derivative along the BODY'S OWN worldline.  For a planet on
a circular orbit the direction to the Galactic centre rotates relative to the body's instantaneous
acceleration at omega_orbit, so the EFE cross-term may live at omega_orbit, not at DC.

This script computes, EXACTLY (sympy) and then numerically (both a0 footings):
  (a) the harmonic content, along a circular orbit, of every g_ext-dependent piece of the written
      action's MI response -- the kernel argument X = |a|^2/a0^2 AND the anomalous acceleration
      vector it produces -- order by order in eps = g_ext/g_N;
  (b) what the paper's own documented "theta_0 = sqrt2 DC kernel" prescribes in the static limit,
      and what its E7 attenuated-a0-line gives at Saturn;
  (c) which Fork survives, with the gate applied harmonic-by-harmonic at the paper's window corners.

CALIBRATION HELD (manufacture neither a win nor a deficit):
  * The full-strength entry of g_ext into the kernel ARGUMENT is GRANTED, not evaded: MI's |a| is the
    acceleration relative to the passive frame u, NOT the covariant geodesic proper acceleration.
    (Forced by the framework's own RAR: a star in a galaxy is freely falling, so a covariant-proper-
    acceleration reading would give |a| = 0 and NO MOND anywhere.  The tidal-only reading is therefore
    NOT available to this framework.)  g_ext enters |a| at FULL strength.  SEP is violated; WEP stays exact.
  * What is then COMPUTED (not asserted) is the ORDER IN eps = g_ext/g_N at which g_ext survives in the
    OBSERVABLE (relative, Sun-to-planet) dynamics, and the FREQUENCY each surviving piece sits at.
  * Both a0 footings on every dimensional number.  Every modelling choice printed and labelled.
  * LENSING SECTOR EXCLUDED: the disformal photon metric (GW170817-excluded ~6-7 orders, paper
    erratum v2) is S_photon.  Everything here is S_matter dynamics.  Not conflated.
  * Regressions against the repo's own committed numbers are asserted, including the ones that
    DISAGREE with my normalisation (flagged, not smoothed).
No TOE language.  No "theory closed".  sympy + numpy.  Exits 0.
"""
import numpy as np
import sympy as sp

RULE = "=" * 100
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

nchk = 0
def check(name, cond):
    global nchk
    assert cond, "FAILED: " + name
    nchk += 1
    print(f"  [OK {nchk:2d}] {name}")

# ---------------------------------------------------------------------------------------------
# 0. FOOTINGS, ANCHORS, BOUNDS  (all cited to the repo / literature already in the repo)
# ---------------------------------------------------------------------------------------------
A0 = {"canon": 9.355e-11, "alt": 1.1305e-10}      # cH_Lam/Z (rho_DE)  |  cH0/Z (rho_total)
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
KPC = 3.0857e19
YR = 365.25 * 86400.0

V_SUN, R_SUN_KPC = 233e3, 8.2
G_EXT = V_SUN**2 / (R_SUN_KPC * KPC)              # 2.146e-10 m/s^2, MW field at the Sun
OMEGA_GAL_SUN = V_SUN / (R_SUN_KPC * KPC)         # 9.2e-16 rad/s

# planets: (semi-major axis [m], period [s], Fienga & Minazzoli 2024 per-planet delta_g bound [m/s^2])
PLANETS = {
    "Mercury": (0.387098 * AU,  87.9691 * 86400.0, 4.6e-14),
    "Earth":   (1.000000 * AU, 365.256 * 86400.0, 8.7e-15),
    "Mars":    (1.523679 * AU, 686.980 * 86400.0, 1.4e-15),
    "Saturn":  (9.582000 * AU, 10759.22 * 86400.0, 7.0e-15),
}
Q2_MEAS, Q2_SIG = 1.6e-27, 1.8e-27                # Park+ 2026 (arXiv:2602.17884)
Q2_95 = Q2_MEAS + 1.645 * Q2_SIG                  # 4.56e-27 one-sided 95% (Q2-pass convention)
Q2_CEIL2S = Q2_MEAS + 2 * Q2_SIG                  # 5.20e-27 (ledger convention)
WINDOW = {"canon": (1.78e-14, 2.21e-14), "alt": (1.78e-14, 1.83e-14)}   # paper Sec. 5.2
THETA0 = np.sqrt(2.0)                             # the framework's documented DC weight

print(__doc__)
head("0.  FOOTING AND INPUTS")
print(f"  a0 canon = {A0['canon']:.4e}   a0 alt = {A0['alt']:.4e} m/s^2   (both carried everywhere)")
print(f"  g_ext (MW at the Sun) = V^2/R = {G_EXT:.4e} m/s^2 ;  omega_gal(Sun) = {OMEGA_GAL_SUN:.3e} rad/s")
print(f"  Cassini Q2 = ({Q2_MEAS:.1e} +/- {Q2_SIG:.1e}) s^-2 -> 95% {Q2_95:.3e} / 2-sigma ceiling {Q2_CEIL2S:.3e}")
for p, (a, T, dg) in PLANETS.items():
    gN = GM_SUN / a**2
    print(f"  {p:<8} a={a/AU:6.3f} AU  omega_orb={2*np.pi/T:.4e} rad/s  g_N={gN:.4e}  "
          f"eps=g_ext/g_N={G_EXT/gN:.3e}  FM24 dg<{dg:.1e}")

# ---------------------------------------------------------------------------------------------
# 1. EXACT SYMBOLICS: the harmonic content of every g_ext-dependent piece on a circular orbit
# ---------------------------------------------------------------------------------------------
head("1.  EXACT HARMONIC DECOMPOSITION ALONG A CIRCULAR ORBIT  (sympy, no expansion shortcuts)")
t, w, iota, eps, gN, gx, a0s = sp.symbols("t omega iota epsilon g_N g_ext a_0", positive=True)
# orbit in the xy-plane, planet at r_hat(t); Sun-ward unit vector n_hat = -r_hat.
rhat = sp.Matrix([sp.cos(w * t), sp.sin(w * t), 0])
# Galactic-centre direction e_hat at angle iota to the ORBIT NORMAL (z); iota = pi/2 = in-plane.
ehat = sp.Matrix([sp.sin(iota), 0, sp.cos(iota)])
c_ang = sp.simplify((rhat.T * ehat)[0, 0])                       # cos psi = r_hat . e_hat
print(f"\n  r_hat(t) = {rhat.T}    e_hat = {ehat.T}    cos psi(t) = {c_ang}")

# --- 1a. the KERNEL ARGUMENT.  a_vec = total kinematic acceleration rel. to the frame u:
#         a_vec = -g_N r_hat + g_ext e_hat   (Sun-ward + the solar system's galactic free-fall)
avec = -gN * rhat + gx * ehat
X = sp.simplify((avec.T * avec)[0, 0])                            # |a|^2  (a0^2 X is the kernel arg)
cross = sp.simplify(X - (gN**2 + gx**2))                          # the g_ext-LINEAR cross-term
dc_cross = sp.simplify(sp.integrate(cross, (t, 0, 2 * sp.pi / w)) * w / (2 * sp.pi))
print(f"\n  |a|^2 = {X}")
print(f"  g_ext-linear cross-term      = {cross}          <-- pure FIRST harmonic, amplitude 2 g_N g_ext sin(iota)")
print(f"  its exact orbit average      = {dc_cross}")
check("cross-term in the KERNEL ARGUMENT is a pure cos(omega t) first harmonic",
      sp.simplify(cross - (-2 * gN * gx * sp.sin(iota) * sp.cos(w * t))) == 0)
check("cross-term DC (orbit-average) is EXACTLY ZERO for every iota  -> no DC at O(eps) in X", dc_cross == 0)
check("the only DC g_ext dependence of X is the g_ext^2 monopole (direction-blind, no ell=2)",
      sp.simplify(sp.integrate(X, (t, 0, 2*sp.pi/w)) * w/(2*sp.pi) - (gN**2 + gx**2)) == 0)

# --- 1b. the ANOMALOUS ACCELERATION VECTOR.  Exact MI balance mu_fw(|A|/a0) A = g_tot inverts to
#         A = nu(|g_tot|/a0) g_tot,  nu = sqrt(1 + a0/|g_tot|);  anomalous part = (nu-1) g_tot.
#         Deep-Newtonian at planetary radii (g_N >> a0): (nu-1) g_tot -> (a0/2) g_hat_tot.
e_sym = sp.symbols("e_ps", positive=True)   # eps = g_ext/g_N
ghat = (-rhat + e_sym * ehat) / sp.sqrt((( -rhat + e_sym*ehat).T * (-rhat + e_sym*ehat))[0, 0])
ser = [sp.expand(sp.series(ghat[i], e_sym, 0, 3).removeO()) for i in range(3)]
def coefv(n): return sp.Matrix([sp.simplify(sp.expand(s).coeff(e_sym, n)) for s in ser])
O0, O1, O2 = coefv(0), coefv(1), coefv(2)
def zero(M): return all(sp.simplify(M[i]) == 0 for i in range(3))
# Legendre generating-function identity 1/sqrt(1-2 eps c + eps^2) = sum eps^n P_n(c)
gen = 1/sp.sqrt(1 - 2*e_sym*c_ang + e_sym**2)
check("|g_tot|^-1 expansion IS the Legendre generating function (P_0,P_1,P_2 recovered exactly)",
      all(sp.simplify(sp.series(gen, e_sym, 0, 3).removeO().coeff(e_sym, n)
                      - sp.legendre(n, c_ang)) == 0 for n in (0, 1, 2)))
check("O(eps^0) anomalous direction is exactly Sun-ward (-r_hat): the ell=0 a0/2 tail",
      zero(O0 + rhat))
check("O(eps^1) anomalous direction = e_hat - (r_hat.e_hat) r_hat : TRANSVERSE, radial part EXACTLY 0",
      zero(O1 - (ehat - c_ang * rhat)) and sp.simplify(sp.expand_trig(sp.expand((O1.T * rhat)[0, 0]))) == 0)
rad2 = sp.simplify((O2.T * (-rhat))[0, 0])          # radial (Sun-ward-positive) part at O(eps^2)
print(f"  O(eps^2) radial (Sun-ward-positive) part = {sp.simplify(sp.expand_trig(rad2))}"
      f"  =  -(1 - P_2(cos psi))/3")
check("O(eps^2) RADIAL part = -(1 - P_2(cos psi))/3  -> the FIRST ell=2 (quadrupole) structure",
      sp.simplify(sp.expand_trig(rad2 + (1 - sp.legendre(2, c_ang))/3)) == 0)

# harmonic split of the O(eps) vector in the INERTIAL frame: DC + 2*omega
O1_dc = sp.Matrix([sp.simplify(sp.integrate(O1[i], (t, 0, 2*sp.pi/w)) * w/(2*sp.pi)) for i in range(3)])
O1_ac = sp.simplify(O1 - O1_dc)
check("O(eps) vector in the INERTIAL frame = DC part (sin(iota)/2, 0, cos iota) + a pure 2*omega part",
      zero(O1_dc - sp.Matrix([sp.sin(iota)/2, 0, sp.cos(iota)]))
      and sp.simplify(O1_ac[0] + sp.sin(iota)*sp.cos(2*w*t)/2) == 0
      and sp.simplify(O1_ac[1] + sp.sin(iota)*sp.sin(2*w*t)/2) == 0)
# and in the CO-ROTATING frame it is a pure FIRST harmonic, purely tangential
that = sp.Matrix([-sp.sin(w*t), sp.cos(w*t), 0])
check("O(eps) vector in the CO-ROTATING frame: radial 0, tangential = -sin(iota) sin(omega t) (pure omega)",
      sp.simplify(sp.expand_trig(sp.expand((O1.T*rhat)[0, 0]))) == 0
      and sp.simplify(sp.expand((O1.T*that)[0, 0]) + sp.sin(iota)*sp.sin(w*t)) == 0)
# orbit-average of the ell=2 P_2 factor
P2_dc = sp.simplify(sp.integrate(sp.legendre(2, c_ang), (t, 0, 2*sp.pi/w)) * w/(2*sp.pi))
check("orbit-average of P_2(cos psi) = (3 sin^2(iota)/2 - 1)/2  (= 1/4 for an in-plane g_ext) != 0",
      sp.simplify(P2_dc - (3*sp.sin(iota)**2/2 - 1)/2) == 0 and sp.simplify(P2_dc.subs(iota, sp.pi/2) - sp.Rational(1,4)) == 0)

print(f"""
  RESULT 1 (exact, both structural claims of Fork A and Fork C are PARTLY right):
    * In the KERNEL ARGUMENT X = |a|^2/a0^2 the g_ext-LINEAR term is a PURE FIRST HARMONIC at
      omega_orbit with EXACTLY ZERO orbit average, for every geometry iota.  Fork A's premise is
      CORRECT AT THE LEVEL OF THE SCALAR THE KERNEL ACTS ON: a strictly static external field is
      seen by the body's own worldline operator Box_u at omega_orbit, because the invariant is a dot
      product with the body's own rotating acceleration.  The only DC g_ext dependence of X is the
      direction-blind g_ext^2 monopole (relative size eps^2, and it carries no ell=2 at all).
    * In the ANOMALOUS ACCELERATION VECTOR, however, the O(eps) piece is DC + 2*omega in the inertial
      frame (equal halves for in-plane g_ext) -- so a DC channel DOES exist and G(0)=1 protects it.
      Fork C's structural claim (a gate cannot suppress it) is CORRECT.  Its AMPLITUDE claim is not:
      the O(eps) piece is TRANSVERSE (radial part exactly zero) and ell=1, and the first ell=2
      (Cassini-Q2) structure appears only at O(eps^2) = (g_ext/g_N)^2.
    * The ell=0 a0/2 tail is a pure FIRST harmonic in the inertial frame (it rides -r_hat(t)) --
      which is exactly what lets the paper's Sec. 5.2 gate suppress it at all.
""")

# ---------------------------------------------------------------------------------------------
# 2. NUMBERS: amplitude of each order, each footing, vs the bounds that own it
# ---------------------------------------------------------------------------------------------
head("2.  AMPLITUDES BY ORDER IN eps, vs THE BOUND THAT OWNS EACH ONE  (ungated, full strength)")
print(f"""
  [ADOPTED #1]  Observables are RELATIVE (planet minus Sun/barycentre) accelerations.  The uniform
  anomalous piece (nu(g_ext/a0)-1) g_ext = {np.sqrt(G_EXT**2+G_EXT*A0['canon'])-G_EXT:.3e} m/s^2 (canon) is shared by the Sun and every
  planet and cancels identically in the relative dynamics -- that is what "the solar system is in free
  fall" means.  It is NOT an internal solar-system signal; it only enters the MW rotation-curve fit.
  [ADOPTED #2]  Q2_eff is read off by matching the ell=2 radial anomalous acceleration to Cassini's
  constant-Q2 template at the planet's own radius: delta_Phi = -(Q2/2)[(x.e)^2-x^2/3] => delta_a_r
  = (2 Q2/3) r P_2, so Q2_eff = (3/2) |coef of r P_2|.  MI's ell=2 grows as r^4 (eps^2 ~ r^4), so this
  is a LOCAL match at Saturn, not a global ephemeris fit; the r-scan below shows it stays tiny.
""")
def orders(a0, gN, r, iota=np.pi/2):
    eps_v = G_EXT / gN
    tail0 = a0 / 2.0                                   # ell=0 Sun-ward tail (g_ext-INDEPENDENT)
    ell1 = (a0 / 2.0) * eps_v                          # O(eps): transverse, ell=1  (|e_hat_perp| <= 1)
    ell1_dc = ell1 * np.sqrt((np.sin(iota)/2)**2 + np.cos(iota)**2)   # its gate-immune DC part
    ell1_2w = ell1 * np.sin(iota) / 2.0                # its 2*omega part
    ell2_r = (a0 / 2.0) * eps_v**2 / 3.0               # O(eps^2) radial ell=2 coefficient of -P_2
    Q2_eff = 1.5 * ell2_r / r
    return dict(eps=eps_v, tail0=tail0, ell1=ell1, ell1_dc=ell1_dc, ell1_2w=ell1_2w, Q2=Q2_eff)

print(f"  {'planet':<8}{'footing':<7}{'eps':>10}{'ell=0 a0/2':>12}{'x FM24':>9}"
      f"{'ell=1 O(eps)':>14}{'/FM24':>8}{'ell=1 DC':>11}{'/FM24':>8}{'Q2 ell=2':>11}{'/Q2_95':>9}")
print("  " + "-" * 98)
NUM = {}
for p, (a, T, dg) in PLANETS.items():
    for f, a0 in A0.items():
        d = orders(a0, GM_SUN / a**2, a)
        NUM[(p, f)] = d
        print(f"  {p:<8}{f:<7}{d['eps']:>10.2e}{d['tail0']:>12.3e}{d['tail0']/dg:>8.0f}x"
              f"{d['ell1']:>14.3e}{d['ell1']/dg:>8.2e}{d['ell1_dc']:>11.3e}{d['ell1_dc']/dg:>8.2e}"
              f"{d['Q2']:>11.3e}{d['Q2']/Q2_95:>9.2e}")

s_c, s_a = NUM[("Saturn", "canon")], NUM[("Saturn", "alt")]
print(f"""
  REGRESSIONS against the repo's committed numbers (asserted below):
   * paper Sec. 5.1 ungated ell=0 exclusions: Mercury 1017x, Earth 5379x, Mars 33429x, Saturn 6686x (canon).
   * Q2-pass Sec. 7 "local MI residue": Q2_loc = a0 g_ext r/(2 GM) = {A0['canon']*G_EXT*PLANETS['Saturn'][0]/(2*GM_SUN):.3e} s^-2, "{Q2_95/(A0['canon']*G_EXT*PLANETS['Saturn'][0]/(2*GM_SUN)):.0f}x below Q2_95".
     That object is the GRADIENT OF THE O(eps) ell=1 residue, i.e. ell1/r = {s_c['ell1']/PLANETS['Saturn'][0]:.3e} s^-2 -- an ell=1
     dipole gradient, NOT the ell=2 quadrupole Cassini fits.  Same number, correctly relabelled.
   * planetary_doors/laneR_bounds_compute.py banks, for the MI door: "ell=1 dipole scale 1.5e-28 s^-2"
     and "ell=2 TRUE quadrupole 7.4e-34 s^-2, 2nd order in a_ext".  My independent values are
     {s_c['ell1']/PLANETS['Saturn'][0]:.2e} (ell=1 gradient, factor {1.5e-28/(s_c['ell1']/PLANETS['Saturn'][0]):.1f} of theirs) and {s_c['Q2']:.2e} (ell=2, factor {7.4e-34/s_c['Q2']:.1f} of theirs)
     -- SAME ORDER, SAME CONCLUSION, normalisation differences flagged not smoothed.
   * cassini_mi_q2_saturn_2026.py Step 5 headline "Q2_MI = 2.715e-29 (canon) / 3.278e-29 (alt)" is
     the O(eps) ell=1 amplitude with a P_2 projection imposed by hand ((1/4) x ell1/r = {0.25*s_c['ell1']/PLANETS['Saturn'][0]:.2e}); it is a
     CONSERVATIVE over-estimate of the true ell=2 by ~1/eps = {1/s_c['eps']:.1e}, and it also passes.
""")
check("regression: paper's ungated ell=0 exclusions reproduced (Mars 33429x, Saturn 6686x, canon)",
      abs(NUM[("Mars","canon")]["tail0"]/PLANETS["Mars"][2]/33429 - 1) < 0.02 and
      abs(NUM[("Saturn","canon")]["tail0"]/PLANETS["Saturn"][2]/6686 - 1) < 0.02)
q2loc = A0['canon']*G_EXT*PLANETS['Saturn'][0]/(2*GM_SUN)
check("regression: Q2-pass Sec.7 'local residue' == my O(eps) ell=1 GRADIENT (to <1%)",
      abs(s_c['ell1']/PLANETS['Saturn'][0]/q2loc - 1) < 0.01 and abs(Q2_95/q2loc - 42) < 1.0)
check("regression: committed cassini_mi_q2_saturn_2026 Step-5 value == (1/4) x my ell=1 gradient",
      abs(0.25*s_c['ell1']/PLANETS['Saturn'][0]/2.715e-29 - 1) < 0.02 and
      abs(0.25*s_a['ell1']/PLANETS['Saturn'][0]/3.278e-29 - 1) < 0.05)
check("banked ell=2 7.4e-34 and my ell=2 agree to within a factor 5 (same order, same verdict)",
      1/5.0 < 7.4e-34 / s_c['Q2'] < 5.0)
check("the ell=2 (Cassini) piece is second order: ratio ell2/ell0 == eps^2/3 exactly",
      abs((s_c['Q2']*PLANETS['Saturn'][0]/1.5)/s_c['tail0'] - s_c['eps']**2/3) < 1e-18)

# ---------------------------------------------------------------------------------------------
# 3. THE GATE, HARMONIC BY HARMONIC
# ---------------------------------------------------------------------------------------------
head("3.  THE GATE APPLIED HARMONIC-BY-HARMONIC  (what it suppresses, what it CANNOT touch)")
def ReG(om, wc): return 1.0 / (1.0 + (om / wc) ** 2)
def AbsG(om, wc): return 1.0 / np.sqrt(1.0 + (om / wc) ** 2)
print(f"""
  [ASSUMPTION #3, load-bearing, and it cuts BOTH ways]  The Debye memory G(omega)=1/(1+i omega/omega_c)
  filters the MI response PER HARMONIC of the response vector in the inertial (parallel-transported)
  frame.  This is not a convenience: it is FORCED if the paper's Sec. 5.2 mitigation is to work at all.
  On a circular orbit the SCALAR |a|^2 is constant (DC), so a gate acting only on the scalar argument
  would leave the ell=0 a0/2 tail completely unsuppressed and the framework would stay excluded by the
  10^3-10^4x per-planet bounds.  The tail is gateable only because the RESPONSE VECTOR -(a0/2) r_hat(t)
  rotates at omega_orbit.  The same vector reading is what makes the O(eps) DC residue gate-IMMUNE.
  (Frame note: along a planetary worldline in flat space, parallel/Fermi-Walker transport differs from
  the fixed inertial basis only by Thomas precession, O(v^2/c^2) ~ 1e-9 at Saturn, so the inertial-frame
  harmonic decomposition IS the transported one at the order worked here.)
""")
print(f"  {'piece':<34}{'frequency':>14}{'Re G @ corner':>15}{'gated ampl (canon)':>21}{'bound':>12}{'margin':>11}")
print("  " + "-" * 98)
T_sat = PLANETS["Saturn"][1]; om_sat = 2*np.pi/T_sat; r_sat = PLANETS["Saturn"][0]; dg_sat = PLANETS["Saturn"][2]
wc_hi = WINDOW["canon"][1]
rows = [
    ("ell=0 a0/2 Sun-ward tail",        "omega_orb",   ReG(om_sat, wc_hi),      s_c['tail0'],   dg_sat, "FM24 dg"),
    ("O(eps) ell=1 transverse, 2*omega", "2 omega_orb", ReG(2*om_sat, wc_hi),   s_c['ell1_2w'], dg_sat, "FM24 dg"),
    ("O(eps) ell=1 transverse, DC",      "DC",          1.0,                     s_c['ell1_dc'], dg_sat, "FM24 dg"),
    ("O(eps^2) ell=2 quadrupole, DC",    "DC",          1.0,                     s_c['Q2'],      Q2_95,  "Q2_95"),
]
for name, fr, S, amp, bd, bl in rows:
    print(f"  {name:<34}{fr:>14}{S:>15.3e}{amp*S:>21.3e}{bd:>12.1e}{bd/(amp*S):>10.2e}x")
print(f"""
  READ:
   * the ell=0 tail is crushed by Re G = {ReG(om_sat, wc_hi):.2e} at the window's most permissive corner:
     {s_c['tail0']:.2e} -> {s_c['tail0']*ReG(om_sat,wc_hi):.2e} m/s^2, {dg_sat/(s_c['tail0']*ReG(om_sat,wc_hi)):.1e}x under the Saturn bound.  (This is the paper's own mechanism.)
   * the O(eps) DC residue is GATE-IMMUNE (G(0)=1 for every omega_c) -- Fork C's structure, confirmed --
     but it is {dg_sat/s_c['ell1_dc']:.0f}x BELOW the Saturn delta_g bound ALREADY UNGATED (canon; {dg_sat/s_a['ell1_dc']:.0f}x alt).
   * the ell=2 DC quadrupole is GATE-IMMUNE too, and {Q2_95/s_c['Q2']:.2e}x below Q2_95 ungated
     ({Q2_95/s_a['Q2']:.2e}x alt; vs the 2-sigma ceiling {Q2_CEIL2S/s_c['Q2']:.2e}x / {Q2_CEIL2S/s_a['Q2']:.2e}x).
   * AFTER gating, the DOMINANT solar-system MI anomaly at Saturn is no longer the a0/2 tail
     ({s_c['tail0']*ReG(om_sat,wc_hi):.1e}) but the gate-immune DC EFE residue ({s_c['ell1_dc']:.1e} m/s^2) -- an omega_c-FREE,
     two-sidedly falsifiable prediction: a x{dg_sat/s_c['ell1_dc']:.0f} improvement in the per-planet bound with a
     Galactic-direction (not Sun-ward) template detects or excludes it, and NO choice of omega_c moves it.
""")
check("gate suppresses the ell=0 tail below the Saturn bound at the window's top corner",
      s_c['tail0']*ReG(om_sat, wc_hi) < dg_sat)
check("the gate-immune DC pieces are BELOW their bounds UNGATED, both footings",
      s_c['ell1_dc'] < dg_sat and s_a['ell1_dc'] < dg_sat and s_c['Q2'] < Q2_95 and s_a['Q2'] < Q2_95)
check("Re G(0) = 1 exactly for every corner in the paper's window (Fork C's premise is TRUE)",
      all(abs(ReG(0.0, wc) - 1.0) < 1e-15 for wc in list(WINDOW['canon']) + list(WINDOW['alt'])))

# ---------------------------------------------------------------------------------------------
# 4. WHAT THE DOCUMENTED theta_0 = sqrt2 DC KERNEL PRESCRIBES
# ---------------------------------------------------------------------------------------------
head("4.  THE PAPER'S OWN 'theta_0 = sqrt2 DC KERNEL': what it says in the static limit")
def theta(y, th0=THETA0): return th0 / (1.0 + (th0 - 1.0) * np.asarray(y, float)**2)
print(f"""
  SOURCE (verbatim): prep_2026/mi_field_theory/BASELINE_ACTION.md:49 -- "the external-field kernel
  theta(y) = theta_0/(1+(theta_0-1) y^2), theta_0 = sqrt2 (shape forced by the dS Wightman function)";
  mi_kernel_bath/theta_from_bath.py -- "y = omega_ext/omega_internal ... A(om_in) = a_in + a_ex
  theta(om_ex/om_in) [Milgrom-2022 EFE form]"; equation_book/eqbook_S5_efe.py -- "A QUASI-STATIC
  external field (y_freq -> 0) therefore enters with DC weight sqrt(2): A = g_int + sqrt2 g_ext
  (scalar/aligned worldline composition)", and its own flag: "this DC kernel depends on |g_ext| ONLY
  (direction-blind), fully consistent with 'pure MI predicts zero DIRECTIONAL asymmetry'".

  SO THE THEORY DOES HAVE A DC ANSWER, AND IT IS THIS:
    theta(0) = {theta(0.0):.4f} = sqrt2   -- a strictly static external field enters the inertia
    argument at FULL strength (x sqrt2).  There is no DC suppression of g_ext in the argument.
    theta(1) = {theta(1.0):.4f} (fundamental unmodified), theta(2) = {theta(2.0):.4f} (down-weighted).
  Two consequences, both computed below:
   (i) it is DIRECTION-BLIND (a scalar aligned sum), so it sources NO ell=2 AT ALL -- its entire
       solar-system effect is an ell=0 rescaling of the same a0/2 tail the gate already owns;
   (ii) via E7 its quantitative solar-system content is the attenuation factor g_obs/(g_obs+sqrt2 g_ext),
       which at Saturn differs from 1 by only ~{np.sqrt(2)*G_EXT/(GM_SUN/PLANETS['Saturn'][0]**2)*1e6:.1f} parts per million.
""")
print(f"  {'planet':<8}{'footing':<7}{'sqrt2 g_ext/g_obs':>19}{'E7 attenuation':>17}{'1 - atten':>12}"
      f"{'d(a0/2 tail)':>15}")
print("  " + "-" * 82)
for p, (a, T, dg) in PLANETS.items():
    for f, a0 in A0.items():
        g_bar = GM_SUN / a**2
        g_obs = np.sqrt(g_bar**2 + g_bar * a0)          # the framework's own a0-line
        atten = g_obs / (g_obs + np.sqrt(2) * G_EXT)    # E7 attenuated a0-line factor
        print(f"  {p:<8}{f:<7}{np.sqrt(2)*G_EXT/g_obs:>19.3e}{atten:>17.10f}{1-atten:>12.3e}"
              f"{(a0/2)*(1-atten):>15.3e}")
check("E7's DC-kernel EFE quench at Saturn is <= 10 ppm on both footings (NOT a 22-28% effect)",
      all(1 - (np.sqrt((GM_SUN/PLANETS['Saturn'][0]**2)**2 + (GM_SUN/PLANETS['Saturn'][0]**2)*a0)
               / (np.sqrt((GM_SUN/PLANETS['Saturn'][0]**2)**2 + (GM_SUN/PLANETS['Saturn'][0]**2)*a0)
                  + np.sqrt(2)*G_EXT)) < 1e-5 for a0 in A0.values()))
# the aligned-scalar prescription's own g_ext-dependent anomaly, for the record
print(f"""
  Under the aligned-scalar DC kernel the g_ext-dependent part of the anomalous acceleration is
  -(a0/2)(sqrt2 g_ext/g_N), i.e. {A0['canon']/2*np.sqrt(2)*G_EXT/(GM_SUN/r_sat**2):.3e} m/s^2 at Saturn (canon) -- RADIAL and DIRECTION-BLIND,
  hence ell=0: it cannot produce a quadrupole even in principle.  It is sqrt2 x my O(eps) amplitude
  and carries the same eps = {s_c['eps']:.2e} suppression.  Either way, the DC kernel's solar-system
  footprint is O(eps) x (a0/2), never O(1).
""")
print(f"""
  WHY THE GALACTIC-BOOST NUMBER DOES NOT TRANSFER TO MI (the conflation Fork C inherits):
    nu(g_ext/a0) - 1 = {np.sqrt(1+A0['canon']/G_EXT)-1:.1%} (canon) / {np.sqrt(1+A0['alt']/G_EXT)-1:.1%} (alt) on the framework's own kernel
    ({1/(1-np.exp(-np.sqrt(G_EXT/A0['canon'])))-1:.1%} with McGaugh's nu, {(1+np.sqrt(1+4*A0['canon']/G_EXT))/2-1:.1%} with 'simple') is the boost to the SUN'S OWN GALACTIC
    acceleration.  In MODIFIED GRAVITY that number is tied to the solar-system quadrupole because the
    phantom density rho_ph = (1/4piG) div[(nu-1) g] solves a NONLINEAR POISSON equation: quadrupolar
    boundary data at the Sun's MOND radius r_M = sqrt(GM/a0) = {np.sqrt(GM_SUN/A0['canon'])/AU:.0f} AU leaks inward as a CONSTANT-Q2
    interior harmonic, giving Q2 ~ a0^(3/2)/sqrt(GM) x O(10^-2) = {7.85e-26*0.03:.1e} s^-2 -- the Desmond-Hees-Famaey
    3-15 sigma object.  MI HAS NO SUCH SOLVE: the anomalous acceleration is an algebraic LOCAL function
    of the body's own total acceleration on its own worldline, so there is no inward leakage channel and
    the ell=2 is whatever the LOCAL expansion gives -- O(eps^2), {Q2_95/s_c['Q2']:.1e}x under the bound.  The
    "<= 2% boost at the solar position" <-> Q2 mapping used by Fork C is a MODIFIED-GRAVITY mapping.
""")

# ---------------------------------------------------------------------------------------------
# 5. THE 10^3-10^4x  vs  42x TENSION: same theory, different observables, different order in eps
# ---------------------------------------------------------------------------------------------
head("5.  RESOLVING THE TENSION THE Q2-PASS FLAGGED (why the 42x residue deserves nonzero weight)")
print(f"""
  The Q2 pass gave its 42x tidal/EFE residue ZERO weight because it "cannot be squared with the
  paper's own ungated 10^3-10^4x planetary exclusion".  They are DIFFERENT OBSERVABLES at DIFFERENT
  ORDERS in eps = g_ext/g_N, and the paper's own numbers make that explicit:

    observable                      order      amplitude at Saturn (canon)   bound            status
    ell=0 Sun-ward a0/2 tail        eps^0      {s_c['tail0']:.3e} m/s^2         FM24 {dg_sat:.1e}   EXCLUDED {s_c['tail0']/dg_sat:.0f}x  (needs the gate)
    ell=1 transverse EFE residue    eps^1      {s_c['ell1']:.3e} m/s^2         FM24 {dg_sat:.1e}   passes {dg_sat/s_c['ell1']:.0f}x ungated
    ell=2 EFE quadrupole (Cassini)  eps^2      Q2 = {s_c['Q2']:.3e} s^-2       Q2_95 {Q2_95:.1e}  passes {Q2_95/s_c['Q2']:.1e}x ungated

  The ell=0 tail is sourced by the SUN ALONE and exists at g_ext = 0; the exclusion says nothing about
  the g_ext-sourced pieces, which are smaller by eps = {s_c['eps']:.2e} and eps^2 = {s_c['eps']**2:.2e} -- 5.5 and 11 orders.
  Locality/passive-frame structure does NOT clear the eps^0 tail (the paper is right about that, and
  the gate is still needed and still costs omega_c).  It DOES clear the g_ext-sourced EFE at the
  solar system, ungated, by pure order-counting.  The two statements are consistent, not rival.
""")
check("the two observables differ by exactly eps (5.5 orders) and eps^2 (11 orders) at Saturn",
      abs(np.log10(s_c['tail0']/s_c['ell1']) - abs(np.log10(s_c['eps']))) < 1e-9)

# ---------------------------------------------------------------------------------------------
# 6. PROVE-BY-MOVING
# ---------------------------------------------------------------------------------------------
head("6.  PROVE-BY-MOVING THE NUMBER (geometry, radius, footing, g_ext, kernel weight)")
print("  (a) geometry iota = angle(g_ext, orbit normal): DC vs 2*omega split of the O(eps) ell=1 piece")
print(f"      {'iota[deg]':>10}{'DC frac':>10}{'2w frac':>10}{'<P_2>':>10}{'ell1_DC [m/s^2]':>18}{'/FM24':>10}")
for io in [0, 30, 60, 90]:
    ir = np.radians(io)
    dcf = np.sqrt((np.sin(ir)/2)**2 + np.cos(ir)**2); acf = np.sin(ir)/2
    p2 = (1.5*np.sin(ir)**2 - 1)/2
    amp = s_c['ell1']*dcf
    print(f"      {io:>10}{dcf:>10.3f}{acf:>10.3f}{p2:>10.3f}{amp:>18.3e}{dg_sat/amp:>9.0f}x")
print(f"""      -> the DC fraction never vanishes (it is 1.00 for g_ext along the orbit normal, 0.50 in-plane),
      so the gate-immune channel is real for every geometry; the margin only moves by x2.""")
print("\n  (b) radius scan: the ell=2 grows as r^4 (Q2_eff ~ r^3).  Does it ever reach the bound?")
print(f"      {'r [AU]':>8}{'eps':>11}{'Q2_eff canon':>15}{'/Q2_95':>10}{'Q2_eff alt':>13}{'/Q2_95':>10}")
for rAU in [1, 9.582, 30, 100, 1000, 7000]:
    r = rAU*AU; gNv = GM_SUN/r**2
    qc = orders(A0['canon'], gNv, r)['Q2']; qa = orders(A0['alt'], gNv, r)['Q2']
    print(f"      {rAU:>8.0f}{G_EXT/gNv:>11.2e}{qc:>15.3e}{qc/Q2_95:>10.2e}{qa:>13.3e}{qa/Q2_95:>10.2e}")
print(f"""      -> the local eps-expansion only breaks (eps -> 1) at r ~ r_M = {np.sqrt(GM_SUN/A0['canon'])/AU:.0f} AU, far outside the
      Cassini/ephemeris arc; inside it the ell=2 is bounded by ~1e-31 out to 100 AU.  If instead the
      ell=2 were FULL strength (eps -> 1 by fiat), Q2 would be {1.5*(A0['canon']/2)/3/r_sat:.1e} s^-2 = {1.5*(A0['canon']/2)/3/r_sat/Q2_95:.0e}x the bound
      -> EXCLUDED.  So the verdict is carried entirely by the eps^2 order-counting, and it is falsifiable:
      any mechanism that restores O(1) g_ext dependence in the OBSERVABLE internal dynamics kills it.""")
print("\n  (c) kernel weight theta_0 (sqrt2 forced core vs 2 KMS endpoint) on the O(eps) amplitude:")
for th0 in [1.0, np.sqrt(2), 2.0]:
    print(f"      theta_0 = {th0:.3f}: ell=1 = {s_c['ell1']*th0:.3e} m/s^2 ({dg_sat/(s_c['ell1']*th0):.0f}x under FM24), "
          f"ell=2 = {s_c['Q2']*th0**2:.3e} s^-2 ({Q2_95/(s_c['Q2']*th0**2):.1e}x under Q2_95)")
print("\n  (d) g_ext MW mass-model spread 1.8 - 2.48e-10 m/s^2:")
for gx_v in [1.8e-10, 2.146e-10, 2.48e-10]:
    e_v = gx_v/(GM_SUN/r_sat**2)
    print(f"      g_ext={gx_v:.2e}: ell=1 = {A0['canon']/2*e_v:.3e} ({dg_sat/(A0['canon']/2*e_v):.0f}x under), "
          f"ell=2 Q2 = {1.5*(A0['canon']/2)*e_v**2/3/r_sat:.3e} ({Q2_95/(1.5*(A0['canon']/2)*e_v**2/3/r_sat):.1e}x under)")

# ---------------------------------------------------------------------------------------------
# 7. VERDICT
# ---------------------------------------------------------------------------------------------
head("7.  VERDICT ON THE FORKS")
print(f"""
  Q-II(a) TIME DEPENDENCE, exact, circular orbit, static uniform g_ext toward the Galactic centre:
      kernel argument   X(t) = [g_N^2 + g_ext^2 - 2 g_N g_ext sin(iota) cos(omega_orb t)]/a0^2
        -> the g_ext-LINEAR term is a PURE omega_orb harmonic with EXACTLY ZERO orbit average.
      response vector   delta_a(t) = (a0/2)[ -r_hat(t) + eps (e_hat - (r_hat.e_hat) r_hat)
                                             + eps^2 (...(1-P_2(cos psi))/3 radial...) ] + O(eps^3)
        -> ell=0 at omega_orb (gateable);  O(eps) ell=1 TRANSVERSE, radial part exactly 0, split
           DC + 2 omega_orb (halves for in-plane g_ext);  first ell=2 only at O(eps^2), DC-carrying.
  Q-II(b) THE theta_0 = sqrt2 DC KERNEL: it DOES have a static answer -- theta(0) = sqrt2, full-weight
      DC entry of g_ext into the inertia argument, no suppression -- but it is DIRECTION-BLIND, so it
      sources no ell=2 at all, and its E7 attenuation at Saturn is 1 - {1-(np.sqrt((GM_SUN/r_sat**2)**2+(GM_SUN/r_sat**2)*A0['canon'])/(np.sqrt((GM_SUN/r_sat**2)**2+(GM_SUN/r_sat**2)*A0['canon'])+np.sqrt(2)*G_EXT)):.2e} (a few ppm).
  Q-II(c) FORKS:
      FORK C  DIES AS POSED.  Its structure is right (a DC channel exists; Re G(0) = 1 for every
              omega_c, so the gate cannot touch it -- confirmed here) but its AMPLITUDE is wrong by
              ~1/eps^2 = {1/s_c['eps']**2:.1e}: the DC channel enters the OBSERVABLE internal dynamics at
              O(eps) (ell=1) and O(eps^2) (ell=2), not at the full {np.sqrt(1+A0['canon']/G_EXT)-1:.0%}-{np.sqrt(1+A0['alt']/G_EXT)-1:.0%} galactic boost.  The
              "<=2% boost <-> Q2" mapping it uses is a modified-GRAVITY (phantom-Poisson) mapping.
      FORK A  SURVIVES for the piece it was invented for -- the ell=0 a0/2 tail genuinely rides
              omega_orb and the gate genuinely suppresses it -- and my Sec. 1 derives that frequency
              rule from the action instead of adopting it.  But Fork A is NOT NEEDED for Q2: the EFE
              pieces pass ungated.
      FORK B  MOOT for Q2 (nothing in the internal solar-system EFE rides omega_gal(Sun) = {OMEGA_GAL_SUN:.1e} rad/s;
              that frequency governs the Sun's own galactic orbit, which is external to the observable).
      FOURTH OUTCOME -- the one that actually holds: a uniform external field DOES enter MI at full
              strength in the kernel argument (SEP is violated, WEP stays exact), but in the OBSERVABLE
              relative dynamics its ell=2 (Cassini-Q2) projection is second order in eps = g_ext/g_N,
              DC, gate-immune, and {Q2_95/s_c['Q2']:.1e}x (canon) / {Q2_95/s_a['Q2']:.1e}x (alt) below Q2_95 WITHOUT any gate.
              The AeST/QUMOND 3-15 sigma RAR-vs-Q2 tension therefore does NOT transfer to the MI
              reading of the written action.  It stays a real tension for the MG limb, which is a
              different realization -- exactly the MI/MG split the paper says is its content.
  SCOPE / STANDING (unchanged by this):  omega_c remains a free fifth constant and is still needed for
  the eps^0 tail (10^3-10^4x); a0's value, Z, s = -1 and eta stay postulates; the lensing sector's
  GW170817 exclusion is untouched (S_photon, not S_matter).  No door is claimed closed.  The new
  omega_c-FREE exposure this leaves on the table: the gate-immune DC EFE residue {s_c['ell1_dc']:.1e} m/s^2 in the
  GALACTIC direction at Saturn, {dg_sat/s_c['ell1_dc']:.0f}x under today's per-planet bound.
""")
print(RULE)
print(f"mi_q2_dc_or_orbital_2026.py: {nchk} checks passed (sympy exact + repo regressions). EXIT 0")
print(RULE)
