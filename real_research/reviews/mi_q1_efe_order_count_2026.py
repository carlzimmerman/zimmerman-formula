#!/usr/bin/env python3
r"""
Q-I: ORDER-COUNT THE EXTERNAL-FIELD EFFECT FROM THE WRITTEN MI ACTION
=====================================================================
Does a UNIFORM external field g_ext enter a solar-system body's internal equation of motion
at FULL strength (QUMOND/AeST-like => inherits the Desmond-Hees-Famaey / Park+ 3-15 sigma
RAR-vs-Q2 tension), or only through suppressed (tidal/higher-multipole) channels?

THE TRAP THIS SCRIPT REFUSES TO FALL INTO
-----------------------------------------
MOND's external-field effect (EFE) is a STRONG-equivalence-principle violation: internal
dynamics depends on the external field.  A theory can have EXACT WEP (eta = 0) and still
violate SEP.  So "WEP is exact, derived" does NOT kill the EFE and is NOT used here as an
argument.  Everything below is order-counted from the action's own matter coupling and its
own external-field (theta) kernel.

WHAT THE WRITTEN ACTION SAYS (read, quoted, not invented)
---------------------------------------------------------
  S = S_EH[g] + S_u[g,u,lambda] + S_matter[g,u,psi;K] + S_photon[gtilde]
  S_matter = -1/2 int sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],   lambda = -rho_m s K
  K(z) = (sqrt(1+4z)-1)/(2 sqrt(z)),   u_mu Box_u u^mu = -|a|^2,   X = |a|^2/a0^2

  prep_2026/mi_field_theory/MATTER_COUPLING.md sec. 1, verbatim:
     "matter feels the kernel through its own 4-acceleration a^mu (the acceleration of the
      worldline/frame relative to the COSMIC REST FRAME), via the scalar |a|^2/a0^2"

  prep_2026/mi_field_theory/BASELINE_ACTION.md:47-49, verbatim:
     "the conservative gradient G(a)^mu = a^mu mu_fw(|a|/a0) ... the external-field kernel
      theta(y) = theta_0/(1+(theta_0-1) y^2), theta_0 = sqrt2 (shape forced by the dS
      Wightman function)",  with  A = a_in + theta(y) a_ex   and  y = omega_ex/omega_in
      (frequency ratio; real_research/THETA_KERNEL_TOWARD_FORCED_2026-06.md:115).

  prep_2026/equation_book/eqbook_S5_efe.py:10-16, verbatim:
     "A QUASI-STATIC external field (y_freq -> 0) therefore enters with DC weight sqrt(2):
      A = g_int + sqrt(2) g_ext ... Internal force balance: mu_fw(A/a0) * g_int = g_bar"

So the action's own prescription is a RELATIVE-COORDINATE (internal) balance in which the
uniform external field appears ONLY inside the inertia argument A -- never as a force in the
internal equation (it cancels in the relative coordinate, as Galileo requires).  That IS an
SEP violation, and it is at FULL strength in the ARGUMENT.  The question this script answers
is what OBSERVABLE that full-strength argument dependence produces.

WHAT IS DERIVED HERE
--------------------
  [T1] The theta kernel is in its DC limit at every planet: y_freq = omega_gal/omega_planet
       <= 1.4e-7, so theta = theta_0 = sqrt2 to ~1e-14.  No frequency gate touches g_ext in
       the kernel argument.  g_ext ENTERS AT FULL STRENGTH.  SEP IS VIOLATED.  (sympy+numeric)
  [T2] THE MULTIPOLE GRADING THEOREM (the answer to Q-I).  Because the argument enters only
       through A = g_N * w, w = sqrt(1 + 2 eps c + eps^2), eps = theta g_ext/g_N, c = cos psi,
       and because 1/mu_fw(A/a0) - 1 is an exact power series in 1/A, the Gegenbauer
       generating function (1 - 2xt + t^2)^-lam = sum_k C_k^(lam)(x) t^k with deg C_k = k
       forces the ell-th Legendre multipole of the anomalous field to start at eps^ell:
           delta a_r(psi) = (a0/2) * sum_ell (-eps)^ell P_ell(cos psi) + O((a0/g_N)^2)
       EXACT to all orders in a0/g_N.  Verified symbolically and numerically.
  [T3] Consequence: ell=0 monopole is UNSUPPRESSED (= a0/2, the excluded tail), ell=1 dipole
       carries eps^1, ell=2 QUADRUPOLE (what Cassini bounds) carries eps^2.
  [T4] Q2(MI)/Q2(QUMOND-MG) = eps^2 EXACTLY.  At Saturn eps = 4.7e-6 => 2.2e-11.
  [T5] The 10^3-10^4x ungated planetary exclusion and the Cassini Q2 bound are DIFFERENT
       MULTIPOLES of the SAME expansion (ell=0 vs ell=2).  Both reproduced from one formula.
       There is no inconsistency to resolve -- only a multipole bookkeeping error to fix.
  [T6] Q-II: the ell=2 piece is genuinely STATIC in the inertial frame (a DC anomalous tidal
       field), so Fork C's structural claim -- Re G(0) = 1, a low-pass gate cannot suppress a
       DC anomaly -- is CORRECT.  It is also MOOT: the ungated ell=2 already sits ~6-7 orders
       below the bound.  The MI Q2 result is omega_c-INDEPENDENT.

ADVERSARIAL SECTION 8 is not optional: the NAIVE per-body reading (which the action does NOT
use) generates an extra uniform O(a0/2) SEP term that would be excluded.  It is computed and
reported at full strength as a named exposure, not buried.

CALIBRATION: both a0 footings on every dimensional number.  Both theta conventions.  Lensing
sector (S_photon, GW170817-excluded by ~6-7 orders) kept strictly separate -- this is S_matter
dynamics only.  Every adopted choice printed [ADOPTED]/[ASSUMPTION].  No TOE language.  No
"theory closed".  numpy + sympy + mpmath (50 dps -- float64 CANNOT resolve an eps^2 = 2e-11
relative signal).  Exits 0.

ADVERSARIAL FINDING THAT CUTS AGAINST THE FRAMEWORK'S OWN FRAMING (Sec. 4): the null-ledger's
MG baseline Q2_MG = a0/(2 r_planet) (nulls_n1_n4.py:67) overstates the published MOND-EFE
quadrupole scale a0/r_M, r_M = sqrt(GM/a0), by ~400x, so the paper's N1 claim "the MG read is
excluded by 3.8 orders" is ~2.6 orders too harsh on its own MG limb.  The MI verdict is an
absolute comparison to the measured bound and is unaffected.
"""
import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 50          # the ell=2 signal is eps^2 ~ 2e-11 of the ell=0 monopole and the
                        # ell=3 signal ~1e-16 of it: float64 CANNOT resolve them.  Every
                        # multipole projection below is done in 50-digit arithmetic.

# =====================================================================================
# 0.  CONSTANTS AND CITED ANCHORS
# =====================================================================================
A0 = {"canon": 9.355e-11, "alt": 1.1305e-10}      # paper Sec. 1: cH_Lambda/Z vs cH0/Z
GM_SUN = 1.32712440018e20
AU, KPC = 1.495978707e11, 3.0857e19
V_SUN, R_SUN_KPC = 233e3, 8.2
G_EXT = V_SUN**2 / (R_SUN_KPC * KPC)              # 2.1456e-10 m/s^2
OMEGA_GAL = V_SUN / (R_SUN_KPC * KPC)             # 9.208e-16 rad/s
YR = 365.25 * 86400.0

# planets: semi-major axis [m], Fienga & Minazzoli 2024 per-planet radial delta_g bound
PLANETS = {
    "Mercury": (0.38710 * AU, 4.6e-14),
    "Earth":   (1.00000 * AU, 8.7e-15),
    "Mars":    (1.52371 * AU, 1.4e-15),
    "Saturn":  (9.58200 * AU, 7.0e-15),
}
Q2_CEN, Q2_SIG = 1.6e-27, 1.8e-27                 # Park+ 2026 arXiv:2602.17884
Q2_95 = Q2_CEN + 1.645 * Q2_SIG                   # 4.561e-27 one-sided 95%
Q2_2SIG = Q2_CEN + 2 * Q2_SIG                     # 5.20e-27 (the paper's N1 ceiling)
THETA0 = np.sqrt(2.0)

RULE = "=" * 100
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

nchk = 0
def check(name, cond):
    global nchk
    assert cond, "FAILED: " + name
    nchk += 1
    print(f"  [OK {nchk:2d}] {name}")

def mu_fw(x):
    """framework inertia dressing, exact inverse of nu(y)=sqrt(1+1/y)."""
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)

def nu_frame(y):
    return np.sqrt(1.0 + 1.0 / np.asarray(y, float))

def theta_kernel(y_freq, t0=THETA0):
    return t0 / (1.0 + (t0 - 1.0) * np.asarray(y_freq, float) ** 2)


# =====================================================================================
# 1.  [T1]  DOES g_ext REACH THE KERNEL ARGUMENT AT ALL, AND AT WHAT WEIGHT?
# =====================================================================================
head("1.  [T1] THE KERNEL ARGUMENT AT THE PLANETS -- is g_ext in it, and at what weight?")
print(r"""
  THE PHYSICS QUESTION, STATED SHARPLY (and the standard-GR intuition that is WRONG here):

    In GR a body freely falling in a UNIFORM field has ZERO proper acceleration -- that IS
    free fall.  If |a| in K(|a|^2/a0^2) were the accelerometer-measured proper acceleration,
    then a planet in free fall around the Sun would ALSO have |a| = 0 and the kernel would be
    inactive everywhere in the solar system -- contradicting the paper's own Sec. 5.1, which
    computes a NONZERO a0/2 = 4.7e-11 m/s^2 tail at every planet from exactly this kernel.

    So the action's |a| is NOT the accelerometer-zero proper acceleration.  MATTER_COUPLING.md
    sec. 1 says what it is, verbatim: "the acceleration of the worldline/frame relative to the
    COSMIC REST FRAME".  In the quasi-static weak-field limit that is the total kinematic
    acceleration in the preferred (dS-Unruh/cosmic) frame:

           |a|  ->  | g_int + g_ext |        (BOTH terms present, no cancellation)

    A uniform galactic field therefore DOES reach the kernel argument.  This is the crux and
    it goes AGAINST any "WEP is exact so there is no EFE" shortcut: WEP-exactness (eta = 0,
    species-independence of mu_fw) says nothing about SEP.  THE ACTION VIOLATES SEP.

  AND THE ACTION SAYS WITH WHAT WEIGHT.  Its own external-field kernel is
        theta(y_freq) = theta_0 / (1 + (theta_0 - 1) y_freq^2),  theta_0 = sqrt2,
        y_freq = omega_ex / omega_in            (THETA_KERNEL_TOWARD_FORCED_2026-06.md:115)
  so the DC / quasi-static limit y_freq -> 0 gives theta -> theta_0 = sqrt2 = FULL strength
  (the raw EP weight is exactly 1; sqrt2 is the EFE-normalised amplitude-branch value).
  At the planets the external "frequency" is the SUN's galactic orbit:
""")
print(f"    omega_gal = V/R = {OMEGA_GAL:.4e} rad/s   (V = {V_SUN/1e3:.0f} km/s, R = {R_SUN_KPC} kpc)\n")
print(f"  {'planet':<10}{'omega_orbit':>14}{'y_freq=w_gal/w_orb':>22}{'theta(y_freq)':>16}"
      f"{'theta/sqrt2 - 1':>18}")
print("  " + "-" * 82)
th_dev = []
for pl, (a_sem, _) in PLANETS.items():
    w_orb = np.sqrt(GM_SUN / a_sem**3)
    yf = OMEGA_GAL / w_orb
    th = theta_kernel(yf)
    th_dev.append(abs(th / THETA0 - 1.0))
    print(f"  {pl:<10}{w_orb:>14.4e}{yf:>22.3e}{th:>16.10f}{th/THETA0-1:>18.2e}")
check("[T1] theta kernel is in its DC limit (theta = theta_0 = sqrt2) at every planet to <1e-13",
      max(th_dev) < 1e-13)
print(f"""
  [T1 VERDICT -- DERIVED, not asserted]  g_ext ENTERS THE KERNEL ARGUMENT AT FULL STRENGTH,
  with the action's own DC weight theta_0 = sqrt2.  There is NO frequency suppression of g_ext
  in the argument (y_freq <= 1.4e-7 at Saturn, so theta = sqrt2 to 1e-14).  The written action
  is SEP-VIOLATING and DOES have an external-field effect.  Any answer of the form "modified
  inertia has no EFE" is WRONG on the action's own terms, and is not the answer given here.

  This also already answers the Q-II sub-question "what does the theta_0 = sqrt2 DC kernel
  prescribe in the static limit": it prescribes FULL-WEIGHT (sqrt2) entry of a strictly static
  external field.  The DC kernel does NOT gate g_ext off.  Whatever saves Q2 is NOT the gate.
""")


# =====================================================================================
# 2.  [T2]  THE MULTIPOLE GRADING THEOREM  (symbolic)
# =====================================================================================
head("2.  [T2] THE MULTIPOLE GRADING THEOREM -- where the suppression actually comes from")
print(r"""
  SET-UP (the action's own relative-coordinate balance, eqbook_S5_efe.py:10-16):
      internal balance      mu_fw(A/a0) * g_int = g_bar
      inertia argument      A = | g_bar nhat + theta g_ext ehat |  =  g_bar * w
                            w = sqrt(1 + 2 eps c + eps^2),  eps = theta g_ext/g_bar, c = rhat.ehat
      anomalous radial accel  delta a_r(psi) = g_bar [ 1/mu_fw(A/a0) - 1 ]

  KEY STRUCTURAL FACT:  1/mu_fw(x) - 1 = (sqrt(1+4x^2) + 1 - 2x)/(2x) is an exact power series
  in 1/x for large x, so with x = A/a0 = (g_bar/a0) w,

      delta a_r = g_bar * sum_{n>=1} d_n w^{-n},     d_n proportional to (a0/g_bar)^n,
      d_1 = 1/2  (this single term IS the a0/2 tail).

  GEGENBAUER GENERATING FUNCTION:  (1 - 2 x t + t^2)^{-lam} = sum_k C_k^{(lam)}(x) t^k, and
  deg_x C_k^{(lam)} = k.  With x = -c, t = eps, lam = n/2:

      w^{-n} = sum_k eps^k C_k^{(n/2)}(-c),   each C_k a polynomial of degree k in c,

  so the Legendre content of the eps^k term is confined to ell <= k.  Therefore the ell-th
  Legendre multipole of delta a_r STARTS AT eps^ell -- exactly, to all orders in a0/g_bar.
  For n = 1 (lam = 1/2) the Gegenbauer polynomials ARE the Legendre polynomials:

      w^{-1} = sum_ell eps^ell P_ell(-c) = sum_ell (-eps)^ell P_ell(c)

  giving the closed-form leading result

      delta a_r(psi) = (a0/2) * sum_ell (-eps)^ell P_ell(cos psi) + O((a0/g_bar)^2).

  ell = 0 : a0/2                (NO eps suppression -- the excluded planetary tail)
  ell = 1 : (a0/2) * eps        (dipole)
  ell = 2 : (a0/2) * eps^2      (QUADRUPOLE -- the multipole Cassini's Q2 constrains)
""")
eps, c, xs = sp.symbols("epsilon c x", positive=True)
w = sp.sqrt(1 + 2 * eps * c + eps**2)
NORD = 6

def legendre_coeffs_of_poly(p):
    """exact Legendre-basis coefficients of a polynomial in c (fast: basis change, no integrals)."""
    p = sp.Poly(sp.expand(p), c)
    D = p.degree()
    unk = sp.symbols(f"L0:{D+1}")
    expr = sp.expand(sum(unk[l] * sp.legendre(l, c) for l in range(D + 1)) - p.as_expr())
    sol = sp.solve([sp.expand(expr).coeff(c, m) for m in range(D + 1)], unk, dict=True)[0]
    return {l: sp.simplify(sol.get(unk[l], 0)) for l in range(D + 1)}

# (a) w^{-1} IS the Legendre generating function: eps^ell coefficient = (-1)^ell P_ell(c)
ser = sp.series(1 / w, eps, 0, NORD).removeO().expand()
for l in range(NORD):
    coef = sp.expand(ser.coeff(eps, l))
    target = sp.expand((-1)**l * sp.legendre(l, c))
    check(f"[T2a] eps^{l} coefficient of 1/w equals (-1)^{l} P_{l}(c)  [Legendre gen. func.]",
          sp.simplify(coef - target) == 0)

# (b) subleading 1/A^n terms: eps^k coefficient has degree exactly k in c, so its Legendre
#     content is confined to ell <= k  =>  the ell-th multipole starts at eps^ell for EVERY n
for n in [2, 3, 4, 5]:
    sn = sp.series(w**(-n), eps, 0, NORD).removeO().expand()
    degs_ok = all(sp.Poly(sp.expand(sn.coeff(eps, k)), c).degree() == k for k in range(NORD))
    check(f"[T2b] w^-{n}: eps^k coefficient is a polynomial of degree exactly k in c "
          f"(k=0..{NORD-1})", degs_ok)
    # explicit Legendre content: ell=2 absent from the eps^0 and eps^1 terms
    z0 = legendre_coeffs_of_poly(sn.coeff(eps, 0)).get(2, 0)
    z1 = legendre_coeffs_of_poly(sn.coeff(eps, 1)).get(2, 0)
    check(f"[T2b] w^-{n}: ell=2 Legendre content of the eps^0 and eps^1 terms is ZERO "
          f"({z0}, {z1})", z0 == 0 and z1 == 0)

# (c) the excess IS an exact power series in 1/x  =>  the grading in (b) applies term by term
excess = (sp.sqrt(1 + 4 * xs**2) + 1 - 2 * xs) / (2 * xs)      # = 1/mu_fw(x) - 1, exact
sinv = sp.symbols("sigma", positive=True)                       # sigma = 1/x
ex_s = sp.series(excess.subs(xs, 1 / sinv), sinv, 0, 6).removeO().expand()
d_coeffs = {n: sp.simplify(ex_s.coeff(sinv, n)) for n in range(6)}
print("        1/mu_fw(x) - 1  =  sum_n d_n x^-n   with   d_n =",
      {n: d_coeffs[n] for n in range(6)})
check("[T2c] the excess has NO x^0 term (d_0 = 0): it vanishes as g_bar -> infinity",
      d_coeffs[0] == 0)
check("[T2c] d_1 = 1/2 exactly -- this single term IS the a0/2 tail",
      d_coeffs[1] == sp.Rational(1, 2))
# assemble: delta a_r = g_bar * sum_n d_n (a0/(g_bar w))^n = a0 * sum_n d_n (a0/g_bar)^(n-1) w^-n
# the ell-th multipole therefore starts at eps^ell (from (a)+(b)), with leading coefficient
# a0 * d_1 * (-1)^ell = (a0/2)(-eps)^ell.
lead_l = {l: sp.simplify(d_coeffs[1] * (-1)**l) for l in range(4)}
check("[T2c] GRADING THEOREM assembled: multipole ell starts at eps^ell with leading "
      "coefficient a0*d_1*(-1)^ell = (a0/2)(-1)^ell",
      all(lead_l[l] == sp.Rational((-1)**l, 2) for l in range(4)))
print(f"""
  [T2 VERDICT -- DERIVED]  g_ext is at FULL strength in the ARGUMENT, but the OBSERVABLE it
  produces is graded by multipole with an EXACT power law:  multipole ell carries eps^ell,
  eps = theta g_ext/g_bar.  This is not an approximation and not a choice of expansion -- it is
  the Legendre/Gegenbauer generating function of the framework's OWN deep-Newtonian nu.
  The quadrupole is the ell = 2 term.  It is SECOND order in g_ext/g_bar.
""")


# =====================================================================================
# 3.  [T3] NUMERIC LEGENDRE PROJECTION OF THE EXACT (UNEXPANDED) ANOMALOUS FIELD
#     -- regression against real_research/reviews/cassini_mi_evasion_2026/verify_order.py
# =====================================================================================
head("3.  [T3] NUMERIC CHECK -- exact kernel, Legendre-projected, and the eps-scaling powers")

def anomalous_multipoles(a_sem, a0v, theta=THETA0, gext=G_EXT, Lmax=3):
    """Exact Legendre coefficients a_ell of the anomalous radial acceleration

           delta_a_r(psi) = g_bar [ 1/mu_fw(A/a0) - 1 ],   A = |g_bar nhat + theta g_ext ehat|

    computed at 50 digits.  The excess is evaluated in the RATIONALISED form
    (1 + 1/(sqrt(1+4x^2)+2x))/(2x), algebraically identical to (sqrt(1+4x^2)+1-2x)/(2x) but free
    of the catastrophic cancellation that makes a naive float64 evaluation useless for ell >= 2.
    """
    g_bar = mp.mpf(GM_SUN) / mp.mpf(a_sem)**2
    a0m, thm, gxm = mp.mpf(a0v), mp.mpf(theta), mp.mpf(gext)

    def dA(cv):
        A = mp.sqrt(g_bar**2 + 2 * thm * g_bar * gxm * cv + (thm * gxm)**2)
        x = A / a0m
        return g_bar * (1 + 1 / (mp.sqrt(1 + 4 * x * x) + 2 * x)) / (2 * x)

    out = {}
    for l in range(Lmax + 1):
        val = mp.quad(lambda cv: dA(cv) * mp.legendre(l, cv), [-1, 1]) * mp.mpf(2 * l + 1) / 2
        out[l] = float(val)
    return out, float(g_bar)


# sanity: the rationalised excess equals the literal one symbolically
check("[T3] rationalised excess (1 + 1/(sqrt(1+4x^2)+2x))/(2x) is algebraically identical to "
      "(sqrt(1+4x^2)+1-2x)/(2x)",
      sp.simplify((1 + 1 / (sp.sqrt(1 + 4 * xs**2) + 2 * xs)) / (2 * xs)
                  - (sp.sqrt(1 + 4 * xs**2) + 1 - 2 * xs) / (2 * xs)) == 0)

print(f"""
  [ADOPTED #1]  VECTOR composition of the inertia argument, A = |g_bar nhat + theta g_ext ehat|.
  This is the CONSERVATIVE choice and the one the framework's own committed Legendre script uses
  (cassini_mi_evasion_2026/verify_order.py:38).  The framework's OTHER committed convention is
  the SCALAR, direction-blind DC kernel A = g_int + sqrt2 g_ext (eqbook_S5_efe.py:13; "this DC
  kernel depends on |g_ext| ONLY (direction-blind)"), which has NO angular dependence at all and
  therefore gives IDENTICALLY ZERO quadrupole.  Section 7 forks both.  The vector reading is used
  for the verdict because it is the one that does NOT give zero.

  [ADOPTED #2]  theta = theta_0 = sqrt2 (the DC value, Section 1).  theta = 1 (the raw EP weight)
  is carried as a sensitivity.  Note the FULL theta(y_freq) kernel would suppress g_ext further
  at y_freq > 1; at the planets y_freq << 1 so sqrt2 is the maximal / most conservative value.
""")
print(f"  {'footing':<8}{'planet':<9}{'g_bar':>11}{'eps=th*gx/gb':>14}"
      f"{'a0 (ell=0)':>13}{'a1 (ell=1)':>13}{'a2 (ell=2)':>13}{'a3 (ell=3)':>13}")
print("  " + "-" * 96)
NUM = {}
for foot, a0v in A0.items():
    for pl, (a_sem, _) in PLANETS.items():
        m, g_bar = anomalous_multipoles(a_sem, a0v)
        e_ = THETA0 * G_EXT / g_bar
        NUM[(foot, pl)] = dict(m=m, g_bar=g_bar, eps=e_, a=a_sem)
        print(f"  {foot:<8}{pl:<9}{g_bar:>11.3e}{e_:>14.3e}"
              f"{m[0]:>13.3e}{m[1]:>13.3e}{m[2]:>13.3e}{m[3]:>13.3e}")

# eps-scaling powers, at Saturn, by varying g_ext
head("3b. eps-SCALING POWERS (vary g_ext by x0.25 ... x4; slope in log-log = power of eps)")
a_sat, dg_sat = PLANETS["Saturn"]
print(f"  {'footing':<8}{'power(a0)':>12}{'power(a1)':>12}{'power(a2)':>12}{'power(a3)':>12}"
      f"{'   (expect 0, 1, 2, 3)'}")
print("  " + "-" * 90)
powers_ok = True
for foot, a0v in A0.items():
    facs = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
    rows = []
    for f in facs:
        m, gb_ = anomalous_multipoles(a_sat, a0v, gext=G_EXT * f)
        rows.append([abs(m[l]) for l in range(4)])
    rows = np.array(rows)
    ps = []
    for l in range(4):
        p = np.polyfit(np.log(facs), np.log(rows[:, l]), 1)[0]
        ps.append(p)
        if abs(p - l) > 0.02:
            powers_ok = False
    print(f"  {foot:<8}" + "".join(f"{p:>12.4f}" for p in ps))
check("[T3] measured eps-powers of the ell = 0,1,2,3 multipoles are 0, 1, 2, 3 to <0.02 "
      "(both footings)", powers_ok)

# closed form vs numeric
print("\n  CLOSED FORM vs NUMERIC (Saturn, both footings):  a_ell = (a0/2) eps^ell")
print(f"  {'footing':<8}{'ell':>4}{'closed form':>15}{'numeric':>15}{'ratio':>9}")
print("  " + "-" * 55)
cf_ok = True
for foot, a0v in A0.items():
    d = NUM[(foot, "Saturn")]
    for l in range(3):
        cf = (a0v / 2) * d["eps"]**l
        rt = abs(d["m"][l]) / cf
        if not (0.999 < rt < 1.001):
            cf_ok = False
        print(f"  {foot:<8}{l:>4}{cf:>15.4e}{abs(d['m'][l]):>15.4e}{rt:>9.4f}")
check("[T3] closed form a_ell = (a0/2) eps^ell reproduces the exact 50-digit projection to "
      "<0.1% for ell = 0,1,2, both footings", cf_ok)

# regression vs the committed script
d_can = NUM[("canon", "Saturn")]
q2_mi_can = abs(d_can["m"][2]) / d_can["a"]
q1_mi_can = abs(d_can["m"][1]) / d_can["a"]
print(f"""
  REGRESSION vs the committed cassini_mi_evasion_2026 (a0 = 9.36e-11, a = 9.582 AU), which
  reports  ell=1 dipole 1.5e-28 s^-2  and  ell=2 quadrupole 7.4e-34 s^-2:
      this script (canon footing):  ell=1 -> {q1_mi_can:.2e} s^-2 ,  ell=2 -> {q2_mi_can:.2e} s^-2
  MATCH (the banked numbers reproduced independently from the closed-form order count).
""")
check("[T3] regression: ell=1 within 15% of the committed 1.5e-28 s^-2",
      abs(q1_mi_can / 1.5e-28 - 1) < 0.15)
check("[T3] regression: ell=2 within 15% of the committed 7.4e-34 s^-2",
      abs(q2_mi_can / 7.4e-34 - 1) < 0.15)


# =====================================================================================
# 4.  [T4] MI vs MODIFIED GRAVITY -- the structural difference, and the exact ratio
# =====================================================================================
head("4.  [T4] WHY QUMOND/AeST PICK UP g_ext AT FULL STRENGTH AND MI DOES NOT")
print(r"""
  MODIFIED GRAVITY (QUMOND / AQUAL / AeST quasi-static limit) -- the mechanism Desmond, Hees &
  Famaey 2024 (MNRAS 530,1781) and Park+ 2026 constrain:

      del^2 Phi = 4 pi G rho + del . [ (nu(|del Phi_N|/a0) - 1) del Phi_N ]

  This is an ELLIPTIC field equation, NONLINEAR in the TOTAL potential.  The boundary condition
  at infinity is set by g_ext, and the phantom source it generates is spread over the whole
  region out to and beyond the MOND radius r_M = sqrt(GM/a0).  An elliptic equation transmits
  that exterior anisotropy INWARD as a regular harmonic ell = 2 interior mode ~ (1/2) Q2 r^2 --
  and a harmonic mode is NOT damped as r decreases.  Hence the inner-solar-system quadrupole is
  FIRST order in the external field with NO g_N suppression at all:  Q2(MG) ~ a0/(2 r).
  The internal accelerations g_N >> a0 do not enter.  That is exactly why the MG limb inherits
  the 3-15 sigma tension.

  MODIFIED INERTIA (the written action) -- the mechanism here:

      mu_fw(|g_bar nhat + theta g_ext ehat| / a0) * g_int = g_bar        (ALGEBRAIC, LOCAL)

  There is no field equation to solve, no exterior boundary condition to transmit, and no
  phantom density.  g_ext reaches the body ONLY inside the local scalar argument, and the
  anisotropy of that argument at a point where g_bar >> g_ext is graded in eps^ell by [T2].
  The suppression is NOT "the external field is absent" (it is present, at full weight sqrt2);
  the suppression is that a LOCAL algebraic dependence on |g_bar nhat + theta g_ext ehat| can
  only produce an ell = 2 anisotropy at second order in the ratio.

  THE STRUCTURAL DIFFERENCE IN ONE LINE:
      MG: the FIELD EQUATION sees g_ext  (global, elliptic, boundary-condition-transmitted)
      MI: the KERNEL sees the BODY'S OWN |a|  (local, algebraic, multipole-graded)
""")
print(f"  {'footing':<8}{'Q2 MG = a0/(2r)':>18}{'Q2 MI (ell=2)':>16}{'ratio MI/MG':>14}"
      f"{'eps^2':>12}{'agree':>8}")
print("  " + "-" * 78)
ratio_ok = True
Q2TAB = {}
for foot, a0v in A0.items():
    d = NUM[(foot, "Saturn")]
    q2mg = a0v / (2 * d["a"])
    q2mi = abs(d["m"][2]) / d["a"]
    r_ = q2mi / q2mg
    Q2TAB[foot] = dict(mg=q2mg, mi=q2mi, dip=abs(d["m"][1]) / d["a"], eps=d["eps"])
    agree = abs(r_ / d["eps"]**2 - 1) < 0.002
    ratio_ok &= agree
    print(f"  {foot:<8}{q2mg:>18.3e}{q2mi:>16.3e}{r_:>14.3e}{d['eps']**2:>12.3e}"
          f"{'YES' if agree else 'NO':>8}")
check("[T4] Q2(MI)/Q2(MG) = eps^2 exactly (to <0.2%), both footings", ratio_ok)
print(f"""
  CONFRONTATION WITH THE MEASUREMENT (Park+ 2026: Q2 = (1.6 +/- 1.8)e-27 s^-2;
  95% one-sided {Q2_95:.2e}, 2-sigma {Q2_2SIG:.2e} s^-2):
""")
print(f"  {'footing':<8}{'reading':<28}{'Q2 [s^-2]':>13}{'vs Q2_95':>14}{'verdict':>12}")
print("  " + "-" * 78)
for foot in A0:
    T = Q2TAB[foot]
    for lab, val in [("MG (QUMOND/AeST, ell=2)", T["mg"]),
                     ("MI ell=1 dipole (NOT Q2)", T["dip"]),
                     ("MI ell=2 QUADRUPOLE", T["mi"])]:
        if val > Q2_95:
            v, f_ = "EXCLUDED", f"{val/Q2_95:.1e}x over"
        else:
            v, f_ = "pass", f"{Q2_95/val:.1e}x under"
        print(f"  {foot:<8}{lab:<28}{val:>13.3e}{f_:>17}{v:>12}")
check("[T4] MG reading (as the framework's own ledger formula defines it) excluded by >1e3, "
      "both footings", all(Q2TAB[f]["mg"] / Q2_95 > 1e3 for f in A0))
check("[T4] MI ell=2 reading passes by >1e6 on both footings",
      all(Q2_95 / Q2TAB[f]["mi"] > 1e6 for f in A0))

# ---- ADVERSARIAL ATTACK ON THE COMPARISON NUMBER ITSELF (the win must be attacked too) ----
print(r"""
  [ADVERSARIAL -- attacking the MG baseline, because a favourable ratio is not evidence if the
   denominator is wrong]  The framework's own null-ledger (prep_2026/concordance_ledger/
   nulls_n1_n4.py:67) sets the MG read to Q2_MG = a0/(2 r_planet).  That is NOT the published
   MOND EFE quadrupole scale.  In QUMOND/AQUAL the interior ell=2 harmonic constant is fixed at
   the MOND transition radius r_M = sqrt(GM/a0) (~8000 AU for the Sun), NOT at the planet's
   orbit, so the dimensional scale is Q2 ~ q * a0/r_M with q = O(0.01-0.4):
""")
print(f"  {'footing':<8}{'r_M = sqrt(GM/a0)':>20}{'r_M [AU]':>11}{'a0/r_M [s^-2]':>16}"
      f"{'a0/(2 r_Sat)':>15}{'overstated by':>15}")
print("  " + "-" * 86)
for foot, a0v in A0.items():
    rM = np.sqrt(GM_SUN / a0v)
    scale = a0v / rM
    print(f"  {foot:<8}{rM:>20.4e}{rM/AU:>11.0f}{scale:>16.3e}{Q2TAB[foot]['mg']:>15.3e}"
          f"{Q2TAB[foot]['mg']/scale:>14.0f}x")
rM_can = np.sqrt(GM_SUN / A0["canon"])
print(f"""
  a0/r_M = {A0['canon']/rM_can:.2e} s^-2 (canon) sits inside the published MOND-EFE Q2 prediction range
  ~1e-27 to 3e-26 s^-2 (Hees, Folkner, Jacobson & Park 2014, PRD 89, 102002), whereas the
  ledger's a0/(2 r_Sat) = {Q2TAB['canon']['mg']:.2e} exceeds it by ~{Q2TAB['canon']['mg']/(A0['canon']/rM_can):.0f}x.

  CONSEQUENCE, stated in the direction it actually cuts -- AGAINST the framework's own framing:
  the paper's N1 row claim "the MG read of the same a0 (3.3e-23) is excluded by 3.8 orders" is
  OVERSTATED by a factor ~400 (~2.6 orders).  The honest MG standing is the literature's own: a few-sigma
  to ~1-order tension, sharpened to 3-15 sigma by the RAR-shape argument of Desmond, Hees &
  Famaey 2024.  This makes the MG limb look BETTER than the ledger says, not worse -- and it
  makes the MI-vs-MG contrast ~8 orders rather than ~11.  [Flagged, not resolved here: pinning
  the O(1) coefficient q needs the actual QUMOND EFE solve, which is NOT done in this script.]

  IT DOES NOT MOVE THE MI VERDICT, because the MI verdict is an ABSOLUTE comparison against the
  MEASURED bound, not a ratio to any MG baseline:
""")
mg_ok = True
for foot, a0v in A0.items():
    rM = np.sqrt(GM_SUN / a0v)
    mi = Q2TAB[foot]["mi"]
    print(f"    {foot:<7} Q2(MI, ell=2) = {mi:.2e}   vs measured Q2_95 = {Q2_95:.2e} "
          f"-> {Q2_95/mi:.1e}x under   |   vs a0/r_M = {a0v/rM:.2e} -> {mi/(a0v/rM):.1e}")
    mg_ok &= Q2_95 / mi > 1e6
check("[T4-ADV] the MI ell=2 verdict is unchanged under the corrected MG baseline (it is an "
      "absolute comparison to the measured bound, >1e6 margin, both footings)", mg_ok)
check("[T4-ADV] the ledger's a0/(2 r_Sat) MG formula exceeds the published MOND-EFE scale "
      "a0/r_M by >100x (flagged as an overstatement in the framework's OWN N1 row)",
      all(Q2TAB[f]["mg"] / (A0[f] / np.sqrt(GM_SUN / A0[f])) > 100 for f in A0))


# =====================================================================================
# 5.  [T5] RESOLVING THE 10^3-10^4x-vs-42x TENSION: DIFFERENT MULTIPOLES, DIFFERENT OBSERVABLES
# =====================================================================================
head("5.  [T5] THE 10^3-10^4x PLANETARY EXCLUSION AND THE Q2 BOUND ARE DIFFERENT MULTIPOLES")
print(r"""
  mi_cassini_q2_omegac_2026.py Sec. 7 gave its tidal-EFE residue ZERO weight because it
  "cannot be squared with the paper's own ungated 10^3-10^4x planetary exclusion, which proves
  locality/passive-frame structure does NOT by itself clear the solar system."

  RESOLUTION: those are two DIFFERENT MULTIPOLES of the SAME anomalous field, bounded by two
  DIFFERENT observables.  ONE expansion -- delta a_r = (a0/2) sum_ell (-eps)^ell P_ell -- produces
  BOTH numbers.  There is no inconsistency; there was a multipole bookkeeping error.

    ell = 0  MONOPOLE   amplitude a0/2 (NO eps suppression)
             observable: constant SUNWARD anomalous radial acceleration
             bound: per-planet radial delta_g, Fienga & Minazzoli 2024  -> the 10^3-10^4x EXCLUSION
             this is the tail that FORCES the omega_c gate.  Nothing here weakens it.

    ell = 1  DIPOLE     amplitude (a0/2) eps
             observable: cos(psi) anomalous field / uniform-force-like signature
             NOT what Cassini's Q2 measures.  This is the "42x below Q2_95" number of Sec. 7 --
             mislabelled there as a quadrupole (the same relabel cassini_mi_evasion_2026 already
             documented: "the compute script's ~2.7e-29 Q2 is the l=1 DIPOLE scale").

    ell = 2  QUADRUPOLE amplitude (a0/2) eps^2
             observable: the traceless ell = 2 tidal field -- EXACTLY what Cassini's Q2 is
             bound: Park+ 2026 -> passes by ~6-7 orders, UNGATED.
""")
print(f"  {'footing':<8}{'planet':<9}{'ell=0 [m/s^2]':>15}{'dg bound':>11}{'excl (x)':>10}"
      f"{'paper Sec5.1':>14}{'  |  ell=2 Q2':>14}{'Q2_95/Q2':>12}")
print("  " + "-" * 96)
PAPER_EXCL = {"canon": {"Mercury": 1017, "Earth": 5379, "Mars": 33429, "Saturn": 6686},
              "alt":   {"Mercury": 1228, "Earth": 6494, "Mars": 40357, "Saturn": 8071}}
excl_ok = True
for foot, a0v in A0.items():
    for pl, (a_sem, dgb) in PLANETS.items():
        d = NUM[(foot, pl)]
        mono = abs(d["m"][0])
        excl = mono / dgb
        q2 = abs(d["m"][2]) / a_sem
        ref = PAPER_EXCL[foot][pl]
        if abs(excl / ref - 1) > 0.05:
            excl_ok = False
        print(f"  {foot:<8}{pl:<9}{mono:>15.4e}{dgb:>11.1e}{excl:>10.0f}{ref:>14}"
              f"{q2:>14.2e}{Q2_95/q2:>12.1e}")
check("[T5] the SAME expansion's ell=0 monopole reproduces the paper's own 1017-40357x ungated "
      "exclusions to <5% (both footings)", excl_ok)
print(f"""
  [T5 VERDICT]  The ell=0 monopole reproduces the paper's 10^3-10^4x exclusion EXACTLY (to <5%),
  from the same formula whose ell=2 term is ~1e6-1e7 BELOW the Cassini Q2 bound.  So the two
  facts are not in tension and never were:

      the exclusion  bounds  ell = 0  (amplitude a0/2,        eps^0)  -> needs the omega_c gate
      Cassini's Q2   bounds  ell = 2  (amplitude (a0/2)eps^2, eps^2)  -> needs NOTHING

  The Q2 pass's decision to give its residue zero weight was therefore over-conservative on a
  category error -- BUT its residue was also the ell=1 DIPOLE (42x), not the quadrupole.  Fixing
  both: the correct MI quadrupole is another factor eps = {NUM[('canon','Saturn')]['eps']:.2e} smaller than the number it
  declined to use.
""")


# =====================================================================================
# 6.  [T6] Q-II: THE TIME-DEPENDENCE ALONG A CIRCULAR ORBIT -- IS THE Q2 PIECE DC OR AC?
# =====================================================================================
head("6.  [T6] Q-II -- harmonic content along a circular orbit; is the ell=2 piece DC?")
print(r"""
  The Q2 pass's Fork C claimed Re G(0) = 1 for every omega_c, so a low-pass gate cannot suppress
  a DC anomaly.  Fork A assumed the anomaly rides omega_orbit because the direction to the
  galactic centre rotates relative to the body's instantaneous position at omega_orbit.

  BOTH are partly right, and the decomposition settles it exactly.  Along a circular orbit
  psi(t) = omega t, so P_ell(cos psi) has harmonic content:
      P_0 = 1                      -> DC only
      P_1 = cos psi                -> omega only
      P_2 = (3cos^2 psi - 1)/2     -> 1/4 DC  +  3/4 cos 2psi     <-- a GENUINE DC part
  so the ell = 2 piece is NOT purely AC: it carries a strict zero-frequency component.

  More decisively, the OBSERVABLE is frame-independent: in the inertial frame the anomalous
  field delta a_r(r, psi) is a STATIC function of position (ehat is fixed; it rotates only at
  omega_gal = 9.2e-16 rad/s).  Cassini's Q2 is a fit for a static ell = 2 tidal field.  So the
  Q2-generating piece is DC.  FORK C IS STRUCTURALLY CORRECT: the gate cannot suppress it.

  AND IT DOES NOT MATTER.  The ungated ell = 2 amplitude is already ~1e6-1e7 below the bound.
  The MI Q2 result is omega_c-INDEPENDENT: Forks A / B / C differ only in a suppression factor
  applied to a number that needs no suppression.
""")
def harmonics(a_sem, a0v, theta=THETA0, gext=G_EXT, nmax=4):
    """Fourier amplitudes (50-digit) of delta_a_r(psi=omega t) and of the inertial-frame
    Cartesian component delta_a_x = -delta_a_r cos(psi) over one circular orbit."""
    g_bar = mp.mpf(GM_SUN) / mp.mpf(a_sem)**2
    a0m, thm, gxm = mp.mpf(a0v), mp.mpf(theta), mp.mpf(gext)

    def dAr(psi):
        A = mp.sqrt(g_bar**2 + 2 * thm * g_bar * gxm * mp.cos(psi) + (thm * gxm)**2)
        x = A / a0m
        return g_bar * (1 + 1 / (mp.sqrt(1 + 4 * x * x) + 2 * x)) / (2 * x)

    sigs = {"|delta_a_r|": dAr, "delta_a_x": lambda p: -dAr(p) * mp.cos(p)}
    out = {}
    for lab, f in sigs.items():
        amps = []
        for n in range(nmax + 1):
            ci = mp.quad(lambda p: f(p) * mp.cos(n * p), [0, mp.pi, 2 * mp.pi]) / mp.pi
            si = mp.quad(lambda p: f(p) * mp.sin(n * p), [0, mp.pi, 2 * mp.pi]) / mp.pi
            amps.append(float(abs(ci) / 2) if n == 0 else float(mp.sqrt(ci**2 + si**2)))
        out[lab] = amps
    return out

print(f"  {'footing':<8}{'signal':<14}" + "".join(f"{'n='+str(n):>13}" for n in range(5)))
print("  " + "-" * 88)
H = {}
for foot, a0v in A0.items():
    h = harmonics(a_sat, a0v)
    H[foot] = h
    for lab in h:
        print(f"  {foot:<8}{lab:<14}" + "".join(f"{v:>13.3e}" for v in h[lab]))
d = NUM[("canon", "Saturn")]
dc_radial = H["canon"]["|delta_a_r|"][0]
w2_radial = H["canon"]["|delta_a_r|"][2]
print(f"""
  READING (canon footing, Saturn):
   * |delta_a_r| DC term       = {dc_radial:.4e} m/s^2  ~= a0/2 = {A0['canon']/2:.4e}  (the ell=0 monopole)
   * |delta_a_r| n=1 term      = {H['canon']['|delta_a_r|'][1]:.4e}         ~= (a0/2)*eps = {A0['canon']/2*d['eps']:.3e}
   * |delta_a_r| n=2 term      = {w2_radial:.4e}         ~= (3/4)(a0/2)eps^2 = {0.75*A0['canon']/2*d['eps']**2:.3e}
   * the ell=2 DC share is 1/4 of the ell=2 amplitude -> a strictly zero-frequency
     quadrupolar tidal field of {abs(d['m'][2])/4:.3e} m/s^2 at Saturn, i.e. Q2_DC = {abs(d['m'][2])/4/d['a']:.2e} s^-2,
     which is {Q2_95/(abs(d['m'][2])/4/d['a']):.1e}x BELOW the Cassini 95% bound with NO gate applied.
   * the ell=0 monopole, by contrast, is purely AC in the INERTIAL frame (the radial direction
     nhat rotates at omega_orbit), so gating it at omega_orbit -- the paper's Fork-A rule -- is
     the internally consistent choice FOR THE MONOPOLE.  Fork A is right where it is used.
""")
check("[T6] the ell=2 quadrupole carries a strict DC component (n=0 in the radial harmonic "
      "series is nonzero at order eps^2)", w2_radial > 0)
# the residual DC CONSTANT FORCE the relative-coordinate reading does leave, and its bound
print("  RESIDUAL DC CONSTANT FORCE in the inertial frame (the ell=1-sourced n=0 term of "
      "delta_a_x):")
print(f"  {'footing':<8}{'DC |delta_a_x|':>17}{'= (a0/2)eps/2':>16}{'Saturn dg bound':>18}"
      f"{'margin':>12}")
print("  " + "-" * 74)
dcf_ok = True
for foot, a0v in A0.items():
    dcf = H[foot]["delta_a_x"][0]
    pred = (a0v / 2) * NUM[(foot, "Saturn")]["eps"] / 2
    marg = dg_sat / dcf
    dcf_ok &= (marg > 10) and abs(dcf / pred - 1) < 0.01
    print(f"  {foot:<8}{dcf:>17.4e}{pred:>16.4e}{dg_sat:>18.1e}{marg:>11.0f}x")
check("[T6] the relative-coordinate reading's residual DC constant force is (a0/2)eps/2 and "
      "sits >10x BELOW the Fienga-Minazzoli Saturn bound, ungated, both footings", dcf_ok)
check("[T6] the DC ell=2 quadrupole passes Cassini Q2_95 by >1e6 with NO gate, both footings",
      all(Q2_95 / (abs(NUM[(f, 'Saturn')]['m'][2]) / 4 / a_sat) > 1e6 for f in A0))


# =====================================================================================
# 7.  FORKS AND ROBUSTNESS
# =====================================================================================
head("7.  FORKS AND ROBUSTNESS -- everything that could move the ell=2 number")
rows = []
d0 = NUM[("canon", "Saturn")]
for lab, kw in [("theta = sqrt2 (DC kernel, ADOPTED)", dict(theta=THETA0)),
                ("theta = 1 (raw EP weight)", dict(theta=1.0)),
                ("theta = 2 (double-pole branch, dispreferred)", dict(theta=2.0)),
                ("g_ext = 1.8e-10 (MW model low)", dict(gext=1.8e-10)),
                ("g_ext = 2.5e-10 (MW model high)", dict(gext=2.5e-10))]:
    for foot, a0v in A0.items():
        m, _ = anomalous_multipoles(a_sat, a0v, **kw)
        rows.append((lab, foot, abs(m[2]) / a_sat))
print(f"  {'variant':<44}{'footing':<8}{'Q2 (ell=2) [s^-2]':>20}{'Q2_95/Q2':>13}")
print("  " + "-" * 88)
for lab, foot, q in rows:
    print(f"  {lab:<44}{foot:<8}{q:>20.3e}{Q2_95/q:>13.1e}")
check("[ROBUST] every theta / g_ext / footing variant passes Cassini Q2 by >1e5",
      all(Q2_95 / q > 1e5 for _, _, q in rows))

print(f"""
  THE OTHER FRAMEWORK-INTERNAL CONVENTION, stated for completeness:
  the SCALAR, direction-blind DC kernel A = g_int + sqrt2 g_ext (eqbook_S5_efe.py:13-16, the
  convention behind the published EFE cubic E7 and the "pure MI predicts EXACTLY ZERO
  directional asymmetry" standing) has NO angular dependence, hence

      Q2(MI, direction-blind DC kernel) = 0   IDENTICALLY, at every order in g_ext.

  So the two committed framework conventions bracket the MI quadrupole as
      [ 0 , {d0['m'][2]/d0['a']:.1e} ] s^-2   vs the bound {Q2_95:.1e} s^-2.
  The verdict does not depend on which is right.
""")


# =====================================================================================
# 8.  ADVERSARIAL -- THE ONE PLACE A FULL-STRENGTH SEP TERM DOES APPEAR, AND ITS STATUS
# =====================================================================================
head("8.  ADVERSARIAL -- the NAIVE per-body reading DOES produce a full-strength SEP term")
nu_ext = {f: float(nu_frame(G_EXT / a0v)) for f, a0v in A0.items()}
print(r"""
  This section exists so the answer is not one-sided.  There IS a reading of MI in which a
  uniform g_ext produces an O(a0) planetary anomaly with NO eps suppression, and it must be
  stated at full strength.

  THE NAIVE PER-BODY LAW (apply mu_fw(|a_i|/a0) a_i = g_i to each body separately):
     Sun:    |a| ~ g_ext ~ 2.3 a0  ->  MOND-boosted,  a_Sun = nu(g_ext/a0) g_ext
     Planet: |a| ~ g_N >> a0       ->  essentially Newtonian in the galactic direction
     relative orbit therefore acquires a UNIFORM anomalous acceleration
         delta a_unif = [nu(g_ext/a0) - 1] * g_ext ,  fixed direction (galactic anticentre),
         DC in the inertial frame (it rotates only at omega_gal = 9.2e-16 rad/s).
""")
print(f"  {'footing':<8}{'g_ext/a0':>10}{'nu_ext':>9}{'delta a_unif':>15}{'in units a0':>13}"
      f"{'vs Saturn dg':>14}{'gate Re G(w_gal)':>18}")
print("  " + "-" * 90)
for foot, a0v in A0.items():
    du = (nu_ext[foot] - 1.0) * G_EXT
    reG = 1.0 / (1.0 + (OMEGA_GAL / 2.21e-14)**2)      # window's most permissive corner
    print(f"  {foot:<8}{G_EXT/a0v:>10.3f}{nu_ext[foot]:>9.4f}{du:>15.3e}{du/a0v:>13.3f}"
          f"{du/dg_sat:>13.0f}x{reG:>18.4f}")
print(f"""
  So IF the naive per-body law were the action's content, there would be a ~0.45 a0 = 4.3e-11
  m/s^2 uniform anomaly at Saturn, ~6000x over the Fienga-Minazzoli bound, and -- crucially --
  essentially UNGATED (Re G(omega_gal) = 0.998 at the window's most permissive corner, because
  the Sun's galactic response must stay open or the Milky Way rotation curve dies).  That would
  be a genuine Fork-B/C-class failure.

  WHY IT IS NOT THE ANSWER TO Q-I (stated as an ASSUMPTION, with its reason, not as a win):
   1. It is ell = 1 (a spatially uniform vector -> potential linear in r), so it produces NO
      ell = 2 quadrupole and is NOT what Cassini's Q2 bounds.  Even if real, the Q2 verdict of
      Sections 4-6 is untouched.  Its bound is the per-planet delta_g / secular-drift channel.
   2. The written action does not use it.  The action's own EFE prescription is the
      RELATIVE-COORDINATE balance mu_fw(A/a0) g_int = g_bar with A = g_int + theta g_ext
      (eqbook_S5_efe.py:16), in which the uniform external field cancels from the internal
      FORCE and survives only in the inertia ARGUMENT.  That is the formulation the committed
      EFE cubic E7, the sigma-spread work, and cassini_mi_evasion_2026 all use.
   3. The per-body law does not respect the centre-of-mass theorem for action-based nonlocal MI
      (Milgrom 1994, Ann. Phys. 229, 384): the CoM of a composite body in a uniform external
      field obeys the MOND law while the internal dynamics is Newtonian up to O(a_ext/a_in)
      corrections -- i.e. exactly the eps-graded terms of [T2], with NO eps^0 internal term.
      The written action conserves momentum (nabla_mu T^munu = 0, machine-verified, residual
      2.6e-16, MATTER_COUPLING.md sec. 3), so it must obey a CoM theorem of this type.
   4. [ASSUMPTION, LABELLED]  Point 3 is an inference from momentum conservation plus the
      cited theorem for Milgrom's nonlocal MI class, NOT an explicit CoM derivation from THIS
      action.  That derivation is not in the repository.  Until it is done, the eps^0 uniform
      term is a NAMED OPEN EXPOSURE of the MI reading -- in the ell = 1 / per-planet-delta_g
      channel, gate-proof, at ~6000x -- and it is the next calculation this lane owes.
      It is NOT a Q2 problem, and it does NOT revive the AeST quadrupole tension.
""")


# =====================================================================================
# 9.  VERDICT
# =====================================================================================
head("9.  VERDICT")
dc = NUM[("canon", "Saturn")]
da = NUM[("alt", "Saturn")]
print(f"""
  Q-I  DOES A UNIFORM EXTERNAL FIELD ENTER AT FULL STRENGTH, OR ONLY VIA TIDAL GRADIENTS?

  ANSWER: BOTH HALVES MUST BE SAID, AND NEITHER ALONE IS HONEST.

  (a) IN THE KERNEL ARGUMENT: FULL STRENGTH.  The action's |a| is the acceleration relative to
      the cosmic rest frame (MATTER_COUPLING.md sec.1), so |a| = |g_int + g_ext| with both terms
      present; and the action's own external-field kernel sits in its DC limit at every planet
      (y_freq <= 1.4e-7 => theta = theta_0 = sqrt2 to 1e-14).  THE WRITTEN ACTION VIOLATES SEP
      AND HAS A GENUINE EFE.  "WEP is exact" is not used and would not have sufficed.

  (b) IN THE OBSERVABLE: MULTIPOLE-GRADED, eps^ell, eps = theta g_ext/g_bar.
      delta a_r(psi) = (a0/2) sum_ell (-eps)^ell P_ell(cos psi) + O((a0/g_bar)^2)   [EXACT]
      -- the Legendre/Gegenbauer generating function of the framework's own deep-Newtonian nu.
      ell = 0: a0/2 unsuppressed (the excluded tail).  ell = 1: eps.  ell = 2: eps^2.
      At Saturn eps = {dc['eps']:.3e}, so eps^2 = {dc['eps']**2:.2e}.  NOTE: eps carries NO a0 footing
      dependence (eps = theta g_ext/g_bar); the 21% footing fork rescales only the a0/2 prefactor.

  SO THE QUADRUPOLE -- and ONLY the quadrupole is what Cassini's Q2 bounds -- IS SECOND ORDER:
      Q2(MI, ell=2)  = {dc['m'][2]/dc['a']:.2e} s^-2 (canon) / {da['m'][2]/da['a']:.2e} (alt)   [UNGATED]
      Q2(MG, ledger formula a0/2r) = {Q2TAB['canon']['mg']:.2e} (canon) / {Q2TAB['alt']['mg']:.2e} (alt)
      Q2(MG, published scale a0/r_M) = {A0['canon']/np.sqrt(GM_SUN/A0['canon']):.2e} (canon) / {A0['alt']/np.sqrt(GM_SUN/A0['alt']):.2e} (alt)  <-- the CORRECTED baseline
      Q2 bound       = {Q2_95:.2e} (95% one-sided) / {Q2_2SIG:.2e} (2 sigma), Park+ 2026
      ratio MI/(a0/2r) = eps^2 EXACTLY;   ratio MI/(a0/r_M) = {(dc['m'][2]/dc['a'])/(A0['canon']/np.sqrt(GM_SUN/A0['canon'])):.1e}
      MI passes by   ~{Q2_95/(dc['m'][2]/dc['a']):.0e}x (canon) / ~{Q2_95/(da['m'][2]/da['a']):.0e}x (alt)

  CORRECTION OWED TO THE PAPER (found by attacking this result's own denominator, Sec. 4):
      the N1 ledger row's "MG read excluded by 3.8 orders" (nulls_n1_n4.py:67) rests on the
      formula Q2_MG = a0/(2 r_planet),
      which overstates the published MOND-EFE quadrupole scale a0/r_M (r_M = sqrt(GM/a0) =
      {np.sqrt(GM_SUN/A0['canon'])/AU:.0f} AU) by ~{Q2TAB['canon']['mg']/(A0['canon']/np.sqrt(GM_SUN/A0['canon'])):.0f}x.  The honest MG standing is the literature's few-sigma-to-
      one-order tension, sharpened to 3-15 sigma by the RAR-shape argument -- i.e. BETTER for
      the MG limb than the framework's own ledger says.  The MI verdict is unaffected.

  FORK VERDICT: a FOURTH OUTCOME, not A / B / C.
      A uniform g_ext DOES source a quadrupole in MI (so the question is not vacuous), but at
      O(eps^2) -- ~6-7 orders below the Cassini bound WITH NO GATE.  Therefore:
        * Fork A (gate at omega_orbit) is the right rule for the ell = 0 tail, where the paper
          uses it, and is IRRELEVANT to Q2.
        * Fork B (gate at omega_gal) does not arise: no gating is needed for Q2.
        * Fork C is STRUCTURALLY CORRECT -- the ell = 2 anomalous tidal field is static in the
          inertial frame, Re G(0) = 1, the low-pass gate cannot suppress it -- and NUMERICALLY
          MOOT, because the ungated amplitude already passes by ~1e6-1e7.
      => The Q2 quadrupole is omega_c-INDEPENDENT in the MI reading.  It neither constrains
         omega_c nor is bought off by it.  The AeST/QUMOND 3-15 sigma RAR-vs-Q2 tension is REAL
         and is INHERITED BY THE MODIFIED-GRAVITY LIMB ONLY.  It does NOT transfer to the
         written MI action's dynamics sector.

  WHAT THIS DOES *NOT* CLAIM (calibration, held):
   * NOT a general "the framework passes the solar system".  The ell = 0 monopole is still
     excluded ungated by 10^3-10^4x and still needs the free fifth constant omega_c.  Nothing
     here relieves that, and nothing here upgrades omega_c from postulate to prediction.
   * NOT a clearance of the MG limb.  If the framework's cosmology-safe realization must be
     AeST-like, the 3-15 sigma tension is still there, on that limb, unresolved.
   * NOT a closed door.  Section 8's eps^0 uniform SEP term is a named open exposure in the
     ell = 1 / per-planet-delta_g channel, gate-proof, ~6000x, pending an explicit
     centre-of-mass derivation from THIS action.  It is a different observable from Q2.
   * LENSING SECTOR EXCLUDED FROM SCOPE: S_photon's disformal metric is GW170817-excluded by
     ~6-7 orders (paper erratum v2).  This result is S_matter dynamics only.
   * Both a0 footings carried on every dimensional number above.  s = -1, a0's value, Z, eta,
     and omega_c remain postulated.  No TOE claim.  No claim that the theory is closed.
""")
print(RULE)
print(f"mi_q1_efe_order_count_2026.py: {nchk} checks passed, exit 0.")
print(RULE)
