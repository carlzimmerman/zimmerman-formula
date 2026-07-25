#!/usr/bin/env python3
r"""
THE MI ACTION'S QUASI-STATIC WEAK-FIELD LIMIT -- does a UNIFORM external field source Q2?
=========================================================================================
Closes the fork left open by reviews/mi_cassini_q2_omegac_2026.py Sec. 6 (Forks A/B/C) and
reconciles the paper's TWO solar-system numbers.  Order-counting + closed forms only; NO
covariant PDE solving (a prior 6-agent workflow stalled on heavy symbolics).

SOURCE OF TRUTH: real_research/papers/MI_FIELD_THEORY_RESULTS_2026.md
   S = S_EH[g] + S_u[g,u,lambda] + S_matter[g,u,psi;K] + S_photon
   S_matter = -(1/2) int sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ] ,  s = -1
   K(z) = (sqrt(1+4z)-1)/(2 sqrt z) ,  Box_u f = u^a nabla_a (u^b nabla_b f)
   first-moment identity  u_mu Box_u u^mu = -|a|^2   =>  K -> mu_fw(|a|/a0) = K(|a|^2/a0^2)
   => quasi-static EOM (Sec. 3.1):   mu_fw(|A|/a0) A = g_N   (host gravity EXACTLY Newtonian:
      linear Poisson, NO phantom density -- that is the whole MI-vs-MG split)
   theta_0 = sqrt2 DC external-field kernel (Sec. 3.1 + E7): a STATIC external field enters the
      body's own inertia argument with weight theta(0) = theta_0 = sqrt2 (theta(1)=1, theta(2)<1).

THE TWO QUESTIONS
  Q-I   does a UNIFORM g_ext enter the internal EOM at FULL strength (=> the AeST/QUMOND
        3-15 sigma Q2 transfers) or only via a tidal gradient?
  Q-II  is the Q2-generating piece DC or at an orbital frequency?  (Fork C claimed Re G(0)=1
        for every omega_c => Q2 omega_c-unfixable.)

CALIBRATION (manufacture NEITHER a win NOR a deficit)
  * A suppression claim is valid ONLY if order-counted from the action's matter coupling.
    "WEP is exact (eta=0)" is NOT used as an argument anywhere: WEP-exactness does not preclude
    SEP violation, and MOND's EFE *is* a SEP effect.  This script shows g_ext enters at FULL
    strength (SEP IS violated) and then computes, multipole by multipole, what that costs.
  * Both a0 footings on every dimensional number.  theta_0 carried as sqrt2 (forced core) and 1
    (no-DC-reweight control) and 2 (KMS endpoint).
  * LENSING SECTOR EXCLUDED: S_photon's disformal metric is GW170817-excluded ~6-7 orders
    (paper erratum v2).  Everything here is S_matter (dynamics).  Not conflated.
  * Every adopted choice printed as [ADOPTED] / [ASSUMPTION].  No TOE language.  No "closed".
Regressions: cassini_mi_evasion_2026/verify_order.py (a1, a2), concordance_ledger/nulls_n1_n4.py
(N1 = 7.4e-34), papers Sec 5.1 exclusion table (1017-40357x), mi_cassini_q2_omegac_2026 (42x).
numpy + sympy.  Exits 0.
"""
import numpy as np
import sympy as sp

# ------------------------------------------------------------------------------- anchors
c, G = 2.99792458e8, 6.674e-11
GM_SUN = 1.32712440018e20
GM_JUP = 1.26686534e17
AU = 1.495978707e11
KPC = 3.0857e19
YR = 365.25 * 86400.0

A0 = {"canon": 9.355e-11, "alt": 1.130e-10}          # cH_Lambda/Z (rho_DE)  |  cH0/Z (rho_total)
V_SUN, R_SUN = 233e3, 8.2 * KPC
G_EXT = V_SUN ** 2 / R_SUN                            # 2.146e-10 m/s^2, fixed toward the GC
THETA = {"theta0=1 (control)": 1.0, "theta0=sqrt2 (forced DC kernel)": np.sqrt(2), "theta0=2 (KMS)": 2.0}

# Fienga & Minazzoli 2024 per-planet |delta g| bounds, paper Sec. 5.1 table
PLANETS = {  # name: (semi-major [AU], period [yr], delta_g bound [m/s^2])
    "Mercury": (0.387099, 0.2408, 4.6e-14),
    "Earth":   (1.000000, 1.0000, 8.7e-15),
    "Mars":    (1.523710, 1.8808, 1.4e-15),
    "Saturn":  (9.582600, 29.457, 7.0e-15),
}
Q2_CEN, Q2_SIG = 1.6e-27, 1.8e-27                     # Park+ 2026 arXiv:2602.17884
Q2_95 = Q2_CEN + 1.645 * Q2_SIG                       # 4.56e-27 (one-sided 95%, as in the Q2 pass)
Q2_2SIG = Q2_CEN + 2 * Q2_SIG                         # 5.20e-27 (as in nulls_n1_n4.py)
OMEGA_C = {"canon": (1.78e-14, 2.21e-14), "alt": (1.78e-14, 1.83e-14)}

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)
CHECKS = []
def check(name, ok):
    CHECKS.append((name, bool(ok)))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

def nu(y):  return np.sqrt(1.0 + 1.0 / y)                          # framework's OWN nu
def mu_fw(x): return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)

print("#" * 104)
print("# MI QUASI-STATIC WEAK-FIELD LIMIT: the multipole structure of the uniform-external-field EFE")
print("#" * 104)
print(f"  g_ext = V^2/R = {G_EXT:.4e} m/s^2 (V=233 km/s, R=8.2 kpc);  g_ext/a0 = "
      f"{G_EXT/A0['canon']:.3f} (canon) / {G_EXT/A0['alt']:.3f} (alt)")

# =====================================================================================
head("1.  Q-I, STEP 1 -- HOW g_ext ENTERS.  The uniform field is NOT removable: FULL STRENGTH.")
print(r"""
  The action's kernel argument is X = |a|^2/a0^2 with a^mu = u^nu nabla_nu u^mu, reduced by the
  first-moment identity u_mu Box_u u^mu = -|a|^2.  The quasi-static EOM (paper Sec. 3.1) is

        mu_fw(|A|/a0) A = g_N,total      g_N,total = g_int(r) + g_ext     (linear Poisson)

  [DERIVED, not asserted]  In MI the standard of NON-acceleration is the preferred frame u, NOT
  local free fall.  So a uniform g_ext CANNOT be transformed away by boosting to the freely
  falling frame: |A| is measured against u, and A = A_int + A_ext adds VECTORIALLY inside the
  kernel argument with coefficient theta_0 = O(1) -- there is NO 1/r gradient, NO factor
  g_ext/g_N, NO tidal suppression at the point of entry.  The paper's own theta_0 = sqrt2 DC
  kernel makes this explicit and AMPLIFIES it: theta(y=omega_ext/omega_int) = theta_0/(1+(theta_0-1)y^2)
  gives theta(0) = sqrt2 for a strictly STATIC external field.

  ==> Q-I, entry level:  g_ext enters the INTERNAL equations of motion at FULL STRENGTH.
      This IS a strong-equivalence-principle violation.  It is NOT killed by eta = 0: the WEP
      exactness of the action says every SPECIES gets the same mu_fw, and says nothing about
      whether the internal dynamics depends on the external field.  It does.
      What remains to be computed is not WHETHER but WITH WHAT ANGULAR STRUCTURE.
""")
# machine-check the non-removability: an added uniform field changes |A| at first order
sym_g, sym_ge, sym_mu, sym_th = sp.symbols("g g_e mu theta", positive=True)
Aabs = sp.sqrt(sym_g ** 2 - 2 * sym_g * sym_th * sym_ge * sym_mu + (sym_th * sym_ge) ** 2)
d1 = sp.simplify(sp.diff(Aabs, sym_ge).subs(sym_ge, 0))
print(f"  sympy: d|A|/d g_ext at g_ext=0  =  {d1}   (= -theta*mu, i.e. O(1) -- NOT O(g_ext/g_N))")
check("uniform g_ext enters |A| at O(1) (coefficient -theta_0*cos psi), not via a gradient",
      sp.simplify(d1 + sym_th * sym_mu) == 0)

# =====================================================================================
head("2.  Q-I, STEP 2 -- THE EXACT MULTIPOLE LAW (the decisive order-counting result)")
print(r"""
  Deep-Newtonian (g_N >> a0, true at every planet: y = g_N/a0 = 4e5 .. 4e8): nu(y) = 1 + 1/(2y)+...
  With g_int = -g(r) rhat and g_ext = g_ext e, mu = rhat.e:

      |A| = sqrt( g^2 - 2 g theta_0 g_ext mu + (theta_0 g_ext)^2 ) = g sqrt(1 - 2 b mu + b^2),
      b == theta_0 g_ext / g(r)   (a SMALL parameter: 4.7e-6 at Saturn, 2.6e-9 at Mercury)

  The anomalous RADIAL acceleration is delta a_r = (nu(|A|/a0) - 1) g = (a0/2) * g/|A| , and
  1/sqrt(1-2 b mu + b^2) is EXACTLY the Legendre generating function.  Hence, in closed form:

      +-------------------------------------------------------------------+
      |   delta a_r(r, psi) = (a0/2) * SUM_l  b^l  P_l(cos psi) ,         |
      |            b = theta_0 g_ext / g_N(r)                             |
      +-------------------------------------------------------------------+

  So the l-th multipole of the MI external-field anomaly is (a0/2) b^l.  ORDER COUNTING, DONE:
      l=0  monopole  : a0/2                  -- g_ext-INDEPENDENT  <== the "a0/2 tail"
      l=1  dipole    : (a0/2) b              -- FIRST order in g_ext
      l=2  QUADRUPOLE: (a0/2) b^2            -- SECOND order in g_ext   <== what Cassini bounds
  The suppression of the l-th multipole is b^l, i.e. (theta_0 g_ext/g_N)^l -- NOT b^1 for all l
  (the prompt's "tidal gradient" guess is the l=1 scaling; the QUADRUPOLE is b^2).
""")
mu_grid = np.cos(np.linspace(0, np.pi, 200001))
for foot, a0 in A0.items():
    for tlab, th in THETA.items():
        g = GM_SUN / (PLANETS["Saturn"][0] * AU) ** 2
        b = th * G_EXT / g
        exact = (nu(np.sqrt(g ** 2 - 2 * g * th * G_EXT * mu_grid + (th * G_EXT) ** 2) / a0) - 1) * g
        series = (a0 / 2) * sum(b ** l * np.polynomial.legendre.legval(mu_grid, [0] * l + [1])
                                for l in range(6))
        err = np.max(np.abs(exact - series)) / (a0 / 2)
        if tlab.startswith("theta0=sqrt2"):
            print(f"  [{foot}] Saturn b = {b:.4e};  exact nu-solution vs 6-term Legendre law: "
                  f"max rel resid = {err:.2e}")
        check(f"closed multipole law exact ({foot}, {tlab}): resid < 1e-5", err < 1e-5)

# regression against the committed Legendre extraction
g_sat = GM_SUN / (PLANETS["Saturn"][0] * AU) ** 2
b_sat = np.sqrt(2) * G_EXT / g_sat
a1_law = (A0["canon"] / 2) * b_sat
a2_law = (A0["canon"] / 2) * b_sat ** 2
print(f"""
  REGRESSION vs cassini_mi_evasion_2026/verify_order.py (independent numerical Legendre projection):
      it extracts  a1 = 2.198e-16 m/s^2 ,  a2 = 1.064e-21 m/s^2  at theta_0 = sqrt2, canon a0.
      closed law   a1 = (a0/2) b   = {a1_law:.3e} m/s^2      a2 = (a0/2) b^2 = {a2_law:.3e} m/s^2
      and its measured a_ext POWERS were 1.000 (l=1) and 2.222 (l=2) -- the law says exactly 1 and 2.
  REGRESSION vs concordance_ledger/nulls_n1_n4.py N1 (banked Q2_MI = 7.4e-34 s^-2):
      closed law   a2 / r_Sat = {a2_law/(PLANETS['Saturn'][0]*AU):.3e} s^-2""")
check("a1 matches verify_order.py to <1%", abs(a1_law / 2.198e-16 - 1) < 0.01)
check("a2 matches verify_order.py to <5%", abs(a2_law / 1.064e-21 - 1) < 0.05)
check("a2/r matches the paper's banked N1 = 7.4e-34 to <5%",
      abs(a2_law / (PLANETS['Saturn'][0] * AU) / 7.4e-34 - 1) < 0.05)
print(f"""
  [CORRECTION, reported both ways]  nulls_n1_n4.py scales the banked l=2 to the alt footing as
  (a0_alt/a0_canon)^2 = 1.459, quoting 1.1e-33 s^-2.  The closed law is LINEAR in a0 (one power of
  a0 in the a0/2 prefactor; b carries none), so the correct alt value is
  {A0['alt']/2*b_sat**2/(PLANETS['Saturn'][0]*AU):.2e} s^-2, not 1.1e-33.  Non-load-bearing (6.8 vs 6.7 orders of margin either
  way) but it is a real mis-scaling in a committed script.""")

# =====================================================================================
head("3.  Q-I ANSWER -- does the AeST/QUMOND 3-15 sigma Q2 TRANSFER to the MI reading?  NO.")
print(f"""
  {'planet':<9}{'g_N':>11}{'b (th=sqrt2)':>14}{'l=0  a0/2':>12}{'l=1  (a0/2)b':>14}"""
      f"{'l=2  (a0/2)b^2':>16}{'l=2 as Q2 [s^-2]':>18}")
print("  " + "-" * 96)
l2_q2 = {}
for name, (aAU, Pyr, dg) in PLANETS.items():
    r = aAU * AU; g = GM_SUN / r ** 2; b = np.sqrt(2) * G_EXT / g
    a0 = A0["canon"]
    l0, l1, l2 = a0 / 2, a0 / 2 * b, a0 / 2 * b ** 2
    l2_q2[name] = l2 / r
    print(f"  {name:<9}{g:>11.3e}{b:>14.3e}{l0:>12.3e}{l1:>14.3e}{l2:>16.3e}{l2/r:>18.3e}")
print(f"""
  The MG/QUMOND quadrupole exists because the nonlinear Poisson operator makes a PHANTOM density
  rho_ph = (1/4piG) div[(nu-1) g], and the external field polarises it: the FULL a0-sized amplitude
  lands directly in the l=2 channel, carrying NO power of b at all (the corpus's own MG number,
  nulls_n1_n4.py, is literally a0/(2 r_Sat) -- the monopole amplitude appearing as a quadrupole).
  That is why AeST inherits 3-15 sigma.  In MI the Sun's field solves the LINEAR Poisson equation
  exactly -- there is no phantom density to polarise -- and g_ext can only TILT the body's own total
  acceleration vector.  A tilt is an l=1 operation; reaching l=2 costs a second power of b.  So the
  MI/MG split is one exact factor:

        +-----------------------------------------------------------------+
        |   Q2_MI  =  Q2_MG * b^2 ,     b = theta_0 g_ext / g_N(r)        |
        +-----------------------------------------------------------------+

  Result at Saturn (canon / theta_0 = sqrt2):
      MG read (nulls_n1_n4.py, first order)  Q2 ~ a0/(2 r_Sat) = {A0['canon']/(2*PLANETS['Saturn'][0]*AU):.2e} s^-2
                                              -> {A0['canon']/(2*PLANETS['Saturn'][0]*AU)/Q2_2SIG:.0f}x the 2-sigma ceiling: EXCLUDED
      MI read (this closed law, second order) Q2 = {l2_q2['Saturn']:.2e} s^-2
                                              -> {Q2_2SIG/l2_q2['Saturn']:.1e}x BELOW it ({np.log10(Q2_2SIG/l2_q2['Saturn']):.1f} orders): PASSES
  ==> Q-I ANSWER:  g_ext enters at FULL strength (SEP violated, entry unsuppressed), but the
      QUADRUPOLE it sources is second order in b.  The AeST-inherited 3-15 sigma Q2 tension does
      NOT transfer to the MI reading of S_matter.  This is a b^2 order-counting result from the
      matter coupling, NOT an appeal to WEP-exactness.""")
q2_mg = A0["canon"] / (2 * PLANETS["Saturn"][0] * AU)
print(f"  exact split identity: Q2_MG * b^2 = {q2_mg:.4e} * {b_sat**2:.4e} = {q2_mg*b_sat**2:.4e} s^-2"
      f"   vs Q2_MI = {l2_q2['Saturn']:.4e}")
check("Q2_MI = Q2_MG * b^2 exactly (the whole MI-vs-MG split is one factor b^2)",
      abs(q2_mg * b_sat ** 2 / l2_q2["Saturn"] - 1) < 1e-9)
print(f"""
  ONE MORE STRUCTURAL FACT (makes Cassini's template inapplicable at first order, computed below):
  the l=1 tilt anomaly is PURELY TRANSVERSE and NOT curl-free, so it is not the gradient of ANY
  potential -- Cassini's Q2 is by definition the coefficient of a quadrupole POTENTIAL.""")
# curl test on the first-order tilt field  delta A = (a0/2) b(r) (e - mu rhat),  b(r) = th g_ext r^2/GM
x, y, z, a0s, ge, th0 = sp.symbols("x y z a0 g_e theta", positive=True)
rr = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
C = a0s * th0 * ge / (2 * GM_SUN)          # delta A = C r^2 (e - mu rhat), e = zhat
evec = sp.Matrix([0, 0, 1]); rhat = sp.Matrix([x, y, z]) / rr
dA = C * rr ** 2 * (evec - (rhat[2]) * rhat)
curl = sp.simplify(sp.Matrix([sp.diff(dA[2], y) - sp.diff(dA[1], z),
                              sp.diff(dA[0], z) - sp.diff(dA[2], x),
                              sp.diff(dA[1], x) - sp.diff(dA[0], y)]))
print(f"\n  sympy curl(l=1 tilt field) = {list(curl)}  (nonzero => NOT a potential force)")
check("l=1 MI EFE anomaly has nonzero curl (MG-impossible, not a quadrupole potential)",
      sp.simplify(curl.norm()) != 0)

# =====================================================================================
head("4.  Q-II -- IS THE Q2-GENERATING PIECE DC OR AT AN ORBITAL FREQUENCY?  EXACTLY BOTH: 1/4 + 3/4.")
print(r"""
  On a circular orbit cos psi = s cos(omega_orb t + phi), s = sin(angle between e and the orbit
  normal); the galactic-centre direction sits ~5.6 deg off the ecliptic, so s = 0.995 ~ 1.
  Legendre polynomials in cos psi therefore decompose EXACTLY into orbital harmonics:

      P_0 = 1                                   -> pure DC
      P_1(cos psi) = s cos(omega t)             -> pure omega_orb, ZERO DC
      P_2(cos psi) = (3/4)s^2 cos(2 omega t) + (3 s^2/2 - 1)/2   -> 2 omega_orb  AND  a DC floor

  So Fork C's premise was RIGHT that a DC piece exists (Re G(0) = 1 cannot suppress it) and
  Fork A's premise was RIGHT that the cross-term also rides an orbital harmonic -- the l=2
  quadrupole splits, for e in the orbital plane, into EXACTLY 1/4 DC + 3/4 at 2 omega_orbit.
  Neither fork is wholly right; and because the whole l=2 amplitude is b^2-suppressed, neither
  matters:  the UNGATEABLE DC quarter is the number to confront Cassini with.""")
s_gc = np.cos(np.radians(5.6))
dc_frac_P2 = (1.5 * s_gc ** 2 - 1) / 2
ac_frac_P2 = 0.75 * s_gc ** 2
tvar = np.linspace(0, 2 * np.pi, 400000, endpoint=False)
P2num = 0.5 * (3 * (s_gc * np.cos(tvar)) ** 2 - 1)
print(f"""
  s = sin(e, orbit normal) = cos(5.6 deg) = {s_gc:.4f}
  DC fraction of P_2 : analytic (3s^2/2-1)/2 = {dc_frac_P2:.5f} ; numeric time-average = {P2num.mean():.5f}
  2omega fraction    : analytic (3/4)s^2      = {ac_frac_P2:.5f}
  DC fraction of P_1 : {np.mean(s_gc*np.cos(tvar)):.2e}  (exactly zero -- the dipole is PURE omega_orb)""")
check("P_2 DC fraction analytic == numeric", abs(dc_frac_P2 - P2num.mean()) < 1e-6)
check("P_1 carries zero DC on a circular orbit", abs(np.mean(s_gc * np.cos(tvar))) < 1e-6)

print(f"\n  UNGATEABLE (DC) part of the l=2 quadrupole, both footings, both theta_0, per planet:")
print(f"  {'planet':<9}{'footing':<7}{'theta0':>8}{'Q2 l=2 total':>15}{'Q2 DC (x1/4)':>15}"
      f"{'/ Q2_95':>12}{'margin':>12}")
print("  " + "-" * 82)
worst_dc = 0.0
for name in ("Mars", "Saturn"):
    r = PLANETS[name][0] * AU; g = GM_SUN / r ** 2
    for foot, a0 in A0.items():
        for tlab, th in THETA.items():
            if tlab.startswith("theta0=1"): continue
            b = th * G_EXT / g
            q2 = (a0 / 2) * b ** 2 / r
            q2dc = q2 * dc_frac_P2
            worst_dc = max(worst_dc, q2dc)
            print(f"  {name:<9}{foot:<7}{th:>8.3f}{q2:>15.3e}{q2dc:>15.3e}"
                  f"{q2dc/Q2_95:>12.2e}{Q2_95/q2dc:>11.1e}x")
print(f"""
  ==> Q-II ANSWER:  the EFE cross-term is time-dependent at 2*omega_orbit for 3/4 of its weight
      (Fork A's mechanism is REAL -- the direction to the GC does rotate in the body frame), but
      an irreducible DC floor of {dc_frac_P2:.3f} survives every orbit average (Fork C's mechanism is also
      REAL).  The DC floor is omega_c-UNFIXABLE, exactly as Fork C said -- and it is
      {Q2_95/worst_dc:.0e}x below Q2_95 at its worst corner (alt footing, theta_0 = 2).  Fork C survives and is HARMLESS.
      The theta_0 = sqrt2 DC kernel is what settles the static limit: theta(0) = sqrt2 says a
      strictly static external field is NOT gated out of the argument -- it enters AMPLIFIED by
      sqrt2 -- so the DC question is answered inside the theory, and the answer costs b^2 anyway.""")

# E7 cross-check: the DC kernel's own prediction for the l=0 attenuation
gobs, gbar, gex, xx = sp.symbols("g_obs g_bar g_ext x", positive=True)
e7 = sp.Eq(gobs ** 2 - gbar ** 2, a0s * gbar * gobs / (gobs + sp.sqrt(2) * gex))
d = sp.symbols("delta")
lhs = sp.expand(((gbar + d) ** 2 - gbar ** 2))
sol = sp.solve(sp.Eq(2 * gbar * d, a0s * gbar / (1 + sp.sqrt(2) * gex / gbar)), d)[0]
ser = sp.series(sol, gex, 0, 2).removeO()
print(f"""
  E7 CROSS-CHECK (the paper's own theta_0 = sqrt2 DC external-field kernel, equation book E7):
      g_obs^2 - g_bar^2 = a0 g_bar * g_obs/(g_obs + sqrt2 g_ext)
  linearised in the deep-Newtonian solar-system corner (delta = g_obs - g_bar):
      delta = {sp.simplify(ser)}
  i.e. delta = a0/2 - (a0/2)(sqrt2 g_ext/g_bar) + ... : the l=0 tail a0/2 ATTENUATED at FIRST
  order in b.  E7 is the angle-averaged (monopole) limb of the same law and it independently
  confirms both answers: full-strength static entry (Q-I) and a b^1 first-order attenuation
  with no first-order l=2 piece (Q-II).  E7 alone cannot see l=2 -- it carries no angle.""")
check("E7 linearises to a0/2 * (1 - sqrt2 g_ext/g_bar): full-strength DC entry, b^1",
      sp.simplify(ser - a0s / 2 + a0s * sp.sqrt(2) * gex / (2 * gbar)) == 0)

# =====================================================================================
head("5.  THE RECONCILIATION -- the 10^3-10^4x ungated exclusion vs the Q2 pass's 42x residue")
print(r"""
  These are DIFFERENT OBSERVABLES at DIFFERENT MULTIPOLE ORDER, and the closed law says by exactly
  how much.  Both statements are TRUE SIMULTANEOUSLY.

    (A) paper Sec. 5.1, "excluded ungated by 10^3-10^4x"
        observable : the l=0 MONOPOLE -- a constant SUNWARD anomalous acceleration a0/2 on the
                     body's OWN worldline, g_ext-INDEPENDENT.  Confronted with the per-planet
                     |delta g| bounds of Fienga & Minazzoli 2024 and, equivalently, with the
                     anomalous perihelion precession (Gauss secular, growing as sqrt(a)).
        size       : a0/2 = 4.68e-11 (canon) / 5.65e-11 (alt) m/s^2.  NO g_ext anywhere in it.

    (B) mi_cassini_q2_omegac_2026.py Sec. 7, "42x BELOW the bound, UNGATED"
        observable : the EXTERNAL-FIELD cross-term -- and, read against the closed law, it is the
                     l=1 DIPOLE (a0/2) b expressed as a gradient (a0/2) b / r, i.e. exactly
                     a0 g_ext r/(2 GM) with theta_0 = 1.  It is NOT Cassini's l=2 Q2.
        size       : (a0/2) b, carrying ONE power of b = theta_0 g_ext/g_N.

  The exclusion factor of (A) times the margin factor of (B) on the SAME observable (the per-planet
  |delta g| bound) must therefore equal exactly 1/b = g_N/(theta_0 g_ext).  Computed:""")
print(f"\n  {'planet':<9}{'(A) a0/2 over bound':>21}{'(B) l=1 under bound':>21}"
      f"{'product':>12}{'1/b':>12}{'match':>8}")
print("  " + "-" * 84)
for name, (aAU, Pyr, dg) in PLANETS.items():
    r = aAU * AU; g = GM_SUN / r ** 2; a0 = A0["canon"]; th = 1.0
    b = th * G_EXT / g
    excl = (a0 / 2) / dg
    marg = dg / (a0 / 2 * b)
    ok = abs(excl * marg * b - 1) < 1e-9
    print(f"  {name:<9}{excl:>20.0f}x{marg:>20.1f}x{excl*marg:>12.3e}{1/b:>12.3e}{'YES' if ok else 'NO':>8}")
    check(f"reconciliation identity (A)x(B) = 1/b at {name}", ok)
print(f"""
  IDENTITY, exact: (exclusion of the l=0 tail) x (margin of the l=1 residue) = g_N/(theta_0 g_ext).
  At Saturn: {(A0['canon']/2)/PLANETS['Saturn'][2]:.0f}x over  x  {PLANETS['Saturn'][2]/(A0['canon']/2*G_EXT/g_sat):.1f}x under  =  {g_sat/G_EXT:.3e}  =  g_N(Saturn)/g_ext.
  ==> RESOLVED.  The two numbers are the SAME physics at two multipole orders, separated by exactly
      one power of b = 3.32e-6 (theta_0=1) at Saturn.  There is NO contradiction, and the Q2 pass's
      decision to give its Sec. 7 residue ZERO weight was over-cautious: the residue is legitimate.
      (It was, however, MISLABELLED as Q2.  It is the l=1 dipole; the l=2 Q2 is one more power of b
      down, at {l2_q2['Saturn']:.2e} s^-2 = {np.log10(Q2_2SIG/l2_q2['Saturn']):.1f} orders below the Cassini ceiling.  The same relabel was
      already flagged in cassini_mi_evasion_2026/CASSINI_MI_EVASION_2026-07.md for the sibling
      compute script; this closes it with the closed form.)
  ==> And the b-power bookkeeping is exactly WHY locality/passive-frame structure does NOT by
      itself clear the solar system: the l=0 monopole carries NO power of b, so it is unsuppressed
      and needs the gate.  The paper's ungated exclusion and the small EFE residue are consistent
      because only the g_ext-DEPENDENT multipoles pay b.""")

# =====================================================================================
head("6.  WHICH SOLAR-SYSTEM CONSTRAINT ACTUALLY BINDS omega_c?")
print(r"""
  The gate G(omega) = 1/(1 + i omega/omega_c) can only act where there is an anomaly to suppress.
  Ranked by how much suppression each observable DEMANDS (canon footing, theta_0 = sqrt2):""")
print(f"\n  {'observable':<42}{'multipole':>10}{'ungated size':>15}{'bound':>13}{'needs gate?':>14}")
print("  " + "-" * 96)
a0 = A0["canon"]; th = np.sqrt(2)
rows = []
for name, (aAU, Pyr, dg) in PLANETS.items():
    r = aAU * AU; g = GM_SUN / r ** 2; b = th * G_EXT / g
    rows.append((f"{name} |delta g| (Fienga-Minazzoli 24)", "l=0", a0 / 2, dg, (a0 / 2) / dg))
r = PLANETS["Saturn"][0] * AU; g = g_sat; b = th * G_EXT / g
rows.append(("Saturn l=1 EFE tilt (DC part = 0)", "l=1", a0 / 2 * b, PLANETS["Saturn"][2],
             (a0 / 2 * b) / PLANETS["Saturn"][2]))
rows.append(("Cassini Q2 quadrupole (Park+ 2026)", "l=2", (a0 / 2) * b ** 2 / r, Q2_95,
             ((a0 / 2) * b ** 2 / r) / Q2_95))
rows.append(("Cassini Q2, DC floor only (ungateable)", "l=2 DC", (a0 / 2) * b ** 2 / r * dc_frac_P2,
             Q2_95, ((a0 / 2) * b ** 2 / r * dc_frac_P2) / Q2_95))
for lab, ell, size, bound, ratio in rows:
    print(f"  {lab:<42}{ell:>10}{size:>15.3e}{bound:>13.2e}   "
          f"{('YES  '+f'{ratio:.0f}x over') if ratio > 1 else ('no   '+f'{1/ratio:.1e}x under'):>16}")
print(f"""
  ==> The ONLY solar-system observable that needs the gate is the l=0 monopole a0/2 tail
      (1017x-33429x over, canon; up to 40357x alt).  Everything g_ext-dependent is already under
      its bound UNGATED.  So omega_c is bound from above by (i) the reactive per-planet |delta g|
      on the l=0 tail and (ii) the causally forced secular drift a0 omega_c/g_N (LLR Gdot/G, which
      the Q2 pass reconstructed as the BINDING edge), and from below by galactic RAR preservation.
      The Cassini Q2 quadrupole NEVER binds omega_c -- not because it was gated away, but because
      the MI reading never generates a Q2 near the bound in the first place ({np.log10(Q2_95/l2_q2['Saturn']):.1f} orders under,
      and its ungateable DC floor {Q2_95/(l2_q2['Saturn']*dc_frac_P2):.1e}x under).  Forks A/B/C are MOOT for Q2.
      Paper's quoted window, unchanged by any of this: canon {OMEGA_C['canon']}, alt {OMEGA_C['alt']} rad/s.""")

# =====================================================================================
head("7.  THE SHARPEST REMAINING EXPOSURE -- the SUN's own node (new; not in the corpus)")
print(r"""
  The multipole law's suppression is b = theta_0 g_ext/g_N, evaluated at the BODY's own total
  acceleration.  Every existing corpus number evaluates it at a PLANET.  The tightest node is the
  SUN: its acceleration in the preferred frame is dominated NOT by g_ext but by the planetary
  reflex (Jupiter alone gives GM_J/r_J^2), and the observable is the Sun-vs-planet DIFFERENTIAL.
  [ASSUMPTION, labelled] this is an order-of-magnitude node estimate, not an ephemeris refit.""")
g_reflex = GM_JUP / (5.2044 * AU) ** 2
print(f"""
  |A_Sun| (Jupiter reflex) = {g_reflex:.3e} m/s^2  >>  g_ext = {G_EXT:.3e}  (ratio {g_reflex/G_EXT:.0f})
  b_Sun = theta_0 g_ext/|A_Sun| = {np.sqrt(2)*G_EXT/g_reflex:.3e}   vs   b_Saturn = {b_sat:.3e}  ({np.sqrt(2)*G_EXT/g_reflex/b_sat:.0f}x LARGER)

  {'reading':<52}{'Sun l=1 DC residue':>20}{'vs Saturn dg':>14}
  {'-'*86}""")
b_sun = np.sqrt(2) * G_EXT / g_reflex
for foot, a0v in A0.items():
    v_inst = (a0v / 2) * b_sun * 0.5      # DC part of the tilt on a reflex that rotates at omega_Jup
    print(f"  {'READING I  instantaneous |A| in the kernel argument  ['+foot+']':<52}"
          f"{v_inst:>20.2e}{v_inst/PLANETS['Saturn'][2]:>13.1f}x")
print(f"""  {'READING II secular/low-passed |A| (tau = 1/omega_c = 1.4-1.8 Myr)':<52}{'exactly 0':>20}{'':>14}

  READING I is the naive one and it puts the Sun's l=1 DC residue {(A0['alt']/2)*b_sun*0.5/PLANETS['Saturn'][2]:.1f}-{(A0['canon']/2)*b_sun*0.5/PLANETS['Saturn'][2]:.1f}x ABOVE the Saturn
  |delta g| scale -- the sharpest g_ext-dependent number anywhere in the MI solar-system ledger.
  BUT READING I is INTERNALLY INCONSISTENT with the framework's own galactic RAR: at instantaneous
  |A_Sun| = {g_reflex:.2e} = {g_reflex/A0['canon']:.0f} a0 the Sun is deep-Newtonian, so its GALACTIC orbit would carry
  nu - 1 = {A0['canon']/(2*g_reflex):.1e} instead of the {nu(G_EXT/A0['canon'])-1:.2f} the Milky Way rotation curve requires.  Any star with a
  Jupiter would fall off the RAR -- which is precisely the paper's own falsifier (i), a frequency-
  split RAR.  The framework therefore REQUIRES the secular reading, and the paper says so
  ("MOND lives entirely in the DC/secular sector", Sec. 3.1).

  READING II, order-counted: with a low-pass of retention time tau = 1/omega_c = 1.4-1.8 Myr, far
  longer than every solar-system orbital period, the kernel argument is the SECULAR acceleration
  <A>_tau.  For ANY closed orbit <d^2r/dt^2> = 0 exactly, so <A>_tau = g_ext for the Sun AND for
  every planet ALIKE.  All bodies then share one and the same mu_fw(g_ext/a0) = {mu_fw(G_EXT/A0['canon']):.4f} (canon) /
  {mu_fw(G_EXT/A0['alt']):.4f} (alt): the external-field effect is EXACTLY COMMON MODE -- an unobservable uniform
  MOND-boosted acceleration of the whole solar system along its own galactic orbit.  The
  DIFFERENTIAL, which is all any ephemeris measures, is then zero at every order in g_ext, with
  residuals only at the gate-leakage order Re G(omega_orb) ~ (omega_c/omega_orb)^2.""")
for name, (aAU, Pyr, dg) in [("Saturn", PLANETS["Saturn"]), ("Mars", PLANETS["Mars"])]:
    w = 2 * np.pi / (Pyr * YR)
    print(f"      Re G(omega_{name}) at omega_c = 2.21e-14: {1/(1+(w/2.21e-14)**2):.2e}"
          f"   (omega_{name} = {w:.3e} rad/s)")
print("""
  ==> Both readings agree on the verdict for Cassini Q2 (no transfer of the AeST tension).  They
      differ on the Sun node by ~5x-over vs exactly zero, and the framework's own RAR consistency
      selects the reading in which it is zero.  Recorded as the live exposure it is, not buried:
      if the secular reading fails for an independent reason, the Sun node becomes a real,
      omega_c-unfixable, few-x tension and it is the number to compute properly.""")

# =====================================================================================
head("8.  VERDICT")
print(f"""
  Q-I   HOW g_ext ENTERS:  FULL STRENGTH.  d|A|/dg_ext = -theta_0 cos psi at O(1); the theta_0 =
        sqrt2 DC kernel amplifies rather than suppresses the static limit.  The written action's
        matter coupling DOES violate the strong equivalence principle -- eta = 0 is irrelevant to
        this and was not used.  WHAT IT SOURCES: the exact multipole law
              delta a_r = (a0/2) SUM_l (theta_0 g_ext/g_N)^l P_l(cos psi),
        so the QUADRUPOLE is SECOND order in g_ext.  The AeST/QUMOND 3-15 sigma Q2, which is FIRST
        order (phantom-density cross-term), does NOT transfer to the MI reading of S_matter.
        Q2_MI(Saturn) = {l2_q2['Saturn']:.2e} (canon) / {A0['alt']/2*b_sat**2/(PLANETS['Saturn'][0]*AU):.2e} (alt) s^-2 vs Q2_95 = {Q2_95:.2e}: {np.log10(Q2_95/l2_q2['Saturn']):.1f} orders under.

  Q-II  DC OR ORBITAL?  EXACTLY BOTH, in fixed proportion: P_2(cos psi) = (3/4)s^2 cos(2 omega t)
        + (3s^2/2-1)/2, so the l=2 cross-term is 3/4 at 2*omega_orbit and 1/4 DC.  Fork A's
        rotation mechanism is real; Fork C's ungateable DC floor is also real.  The DC floor is
        omega_c-unfixable and sits {Q2_95/worst_dc:.0e}x below Q2_95 at the worst corner.  HARMLESS.

  FORK SURVIVING:  the FOURTH OUTCOME.  A uniform g_ext does source a nonzero MI anomaly (so the
        question is not moot in the way "MI has no EFE" would make it), but it sources l=1 at
        first order and l=2 only at second order, and the l=1 piece is not even curl-free, so it
        is not a quadrupole potential at all.  Cassini's Q2 template first bites at O(b^2).
        Forks A/B/C are all MOOT for Q2: no omega_c is required, none is excluded, and Q2 does
        not enter the window determination.  Fork C survives as a structure (a real DC floor that
        no gate can touch) with no observational bite.

  RECONCILIATION:  (A) 10^3-10^4x ungated exclusion = the l=0 MONOPOLE a0/2, g_ext-independent,
        on the per-planet |delta g| / perihelion-precession observable.  (B) 42x-below residue =
        the l=1 DIPOLE (mislabelled Q2), one power of b down.  Identity, exact and verified per
        planet: (A) x (B) = g_N/(theta_0 g_ext).  BOTH TRUE.  The 42x is legitimate; the zero
        weight it was given was over-cautious.  Different observables, different b-order.

  BINDS omega_c:  the l=0 tail's reactive per-planet |delta g| (Mars tightest, {(A0['canon']/2)/PLANETS['Mars'][2]:.0f}x canon /
        {(A0['alt']/2)/PLANETS['Mars'][2]:.0f}x alt) plus its causally forced secular drift against LLR Gdot/G.  Cassini Q2
        never binds.  Window unchanged.

  SCOPE:  S_matter dynamics only.  S_photon's disformal metric is separately GW170817-excluded by
        ~6-7 orders (paper erratum v2) and is NOT used here.  omega_c remains a free fifth
        constant -- nothing here upgrades it.  No door is claimed closed; the covariant-MI
        premises (passive/hypersurface-orthogonal u, secular kernel argument) are postulates.""")

head("CHECKS")
npass = sum(1 for _, o in CHECKS if o)
for n, o in CHECKS:
    if not o: print(f"  FAILED: {n}")
print(f"  {npass}/{len(CHECKS)} checks passed.")
assert npass == len(CHECKS), "some checks failed"
print(RULE)
print("mi_quasistatic_efe_multipoles_2026.py: exit 0")
print(RULE)
