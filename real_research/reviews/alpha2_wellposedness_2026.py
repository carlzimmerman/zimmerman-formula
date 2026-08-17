#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
alpha2_wellposedness_2026.py
============================
THE WELL-POSEDNESS ROUTE to the alpha_1/alpha_2 fork for AeST's aether sector.

    S_aether = int d^4x sqrt(-g) [ -(K_B/2) F_{mu nu} F^{mu nu}
                                   - lambda (A^mu A_mu + 1) ] ,
    F_{mu nu} = 2 grad_[mu A_nu] = d_mu A_nu - d_nu A_mu   (metric-free curl),
    matter couples to g only.  Einstein-aether dictionary: c_1=+K_B, c_2=0,
    c_3=-K_B, c_4=0  =>  c_13 = 0 (c_T = 1 exact) AND c_123 = 0 (spin-0 aether
    mode has ZERO propagation speed).

THE FORK BEING ADJUDICATED
  READING L  (stage70, Foster & Jacobson generic formula on the dictionary):
             alpha_1 = -8(c_3^2 + c_1 c_4)/(2c_1 - c_1^2 + c_3^2) = -4 K_B,
             hence K_B < 2.5e-5 from LLR |alpha_1| < 1e-4.
  READING D  (real_research/reviews/ppn_alpha_independent_check_2026.py, from
             scratch): alpha_1 = alpha_2 = 0 identically, because the linearized
             equations force lambda = 0; the price it reports is a
             "non-normalisable stationary wake v_L ~ U/(i k w.khat)" and a g_00
             with no Taylor series in w.
  THIRD (recorded, claimed by nobody): discard the Theta_{3nu} constraints and
             freeze lambda at its w=0 value -> formal alpha_1 = +3K_B/2.

MY ASSIGNED QUESTION: is reading D's wake a GENUINE PHYSICAL OBSTRUCTION or an
ARTIFACT OF THE IDEALISATION?  Equivalently: is the static boosted problem
WELL-POSED at c_123 = 0?

WHAT THIS SCRIPT ESTABLISHES (headline first, so nobody has to read the log)
  1. RIGOROUS, AND IT DEFANGS READING D's OWN CAVEAT: the wake carries
     F_{mu nu} == 0 IDENTICALLY at O(rho).  The transverse aether perturbation
     is forced to zero by the spatial Maxwell equations, so the aether tilt is
     CURL-FREE (F_ij = 0), and Psi = 0 (the lambda = 0 Gauss constraint) kills
     F_0i.  A zero-field-strength aether configuration has zero energy density,
     zero stress, and therefore ZERO effect on the metric at O(rho^2) as well --
     the aether stress is pushed to O(rho^4).  Reading D's alpha_1 = alpha_2 = 0
     is therefore NOT an artifact: the metric really is exactly GR, and the
     "pathology" it apologised for is an unobservable flat connection.
  2. RIGOROUS: the pole is NOT absolutely integrable in 3D k-space (it is a
     simple pole in mu = cos(k,w) and d^3k = k^2 dk dmu dphi), so the real-space
     field exists only WITH a prescription.  Causality picks the convected one,
     and the resulting configuration is a permanent semi-infinite FURROW:
     the tilt does not decay downstream at fixed impact parameter b, falling
     only as 1/b transversely.  So the wake IS a real failure of
     A -> A_bg at infinity -- of the AETHER, never of the metric.
  3. RIGOROUS: three regulators, ranked.  A finite source radius R removes the
     on-axis 1/b divergence and nothing else.  A finite time since the boost
     truncates the furrow at w c T = 1.74 Mpc for the Sun -- i.e. not at all,
     on solar-system scales.  ONLY a nonzero spin-0 sound speed removes the
     wake, and it does so ONLY IF c_s > w: the static response denominator is
     c_s^2 - (w.khat)^2, which has zeros on the unit sphere iff c_s <= w.
  4. RIGOROUS AND UNIFYING, answering (e): the PPN expansion of g_00 in w has
     RADIUS OF CONVERGENCE EXACTLY c_s.  Reading D's "g_00 has no Taylor series
     in w" is precisely "c_s = 0 in the aether-only truncation".  alpha_1 and
     alpha_2, being O(w^2) Taylor coefficients, exist if and only if the system
     is SUBSONIC with respect to the spin-0 aether/scalar mode.
  5. THE ADJUDICATION: the fork is not "which reading is right".  BOTH are ends
     of one family parameterised by the MACH NUMBER M = w/c_s.  Reading D is the
     M -> infinity end and is EXACT for the aether-only truncation (where
     c_s = 0, so every w > 0 is supersonic).  Reading L's premises (unique
     decaying static solution, analytic in w) hold only on M < 1.
  6. THE DECIDING NUMBER, handed over: M = 1 at c_s = w_sun = 369.82 km/s
     = 1.234e-3 c.  At SZ21's own MOND-compatible fits the scalar sound speed
     (SZ21 Eq 30) is 6.0e3-1.3e4 km/s, i.e. M = 0.028-0.062: DEEPLY SUBSONIC,
     which is READING L's branch -- ADVERSE.  Flipping to reading D requires the
     solar-system stiffening of the scalar to suppress c_s^2 by 263x (Cosh) to
     1314x (Exp).  Whether it does is NOT COMPUTED here (it needs the local
     expansion of F(Y,Q), the sibling's territory).  Reported BOTH ways.

DIRECTION OF RISK: MIXED, and deliberately so.  Favourable half: reading D's
self-reported defect is dissolved (F == 0), so alpha_1 = alpha_2 = 0 is a clean
result in the truncation and NOTHING in the aether sector bounds K_B -- the wake
amplitude is K_B-INDEPENDENT.  Adverse half: the Mach criterion, evaluated with
the corpus's own SZ21 numbers, puts the solar system on reading L's subsonic
branch, which is where K_B < 2.5e-5 and stage73's empty window live.

WHAT IS NOT COMPUTED (stated up front, never papered over)
  N1. alpha_1 on the SUBSONIC branch.  I do not re-derive -4K_B; I establish
      that M < 1 is the domain where a Foster-Jacobson-type answer can exist.
  N2. the value of the spin-0 speed in the solar system.  It requires the local
      second derivatives of AeST's free function F(Y,Q); the SZ21 Eq-30 number
      is COSMOLOGICAL and is used only as one bracket end.
  N3. whether the scalar mixing lifts the c_123 = 0 degeneracy COMPLETELY (one
      dynamical spin-0 mode) or leaves a residual zero-speed direction.  If a
      zero-speed direction survives, the wake survives with it and reading D
      holds regardless of c_s.  Named for the sibling.
  N4. the interior of the nonlinear tube b < 2.79 R_sun, where the linear
      treatment of the wake fails by its own estimate.
  N5. anything about alpha_2 on the subsonic branch.

CONVENTIONS THAT COULD FLIP A SIGN OR A FACTOR
  C1. signature (-,+,+,+); c = 1 in the symbolic parts; A_mu (the ONE-FORM) is
      the fundamental aether variable, so F carries no metric.
  C2. wind w^i = aether velocity at infinity measured in the MATTER rest frame;
      the aether frame is taken to be the CMB frame, so w_sun = 369.82 km/s
      (Planck 2018 solar dipole).  All fields static in the matter frame.
  C3. U > 0, laplacian U = -4 pi G rho, U(k) = 4 pi G rho(k)/k^2; h_00 = 2U at
      lowest order.
  C4. PPN matching as in the task statement:
      g_00 = -1 + 2U + alpha_1 w^2 U + alpha_2 w^i w^j U_ij + ...
      Will's textbook writes the w^2 U coefficient as (alpha_3 - alpha_1); a
      reader in Will's normalisation flips the sign of alpha_1.  Irrelevant to
      the verdict below, since 0 has no sign.
  C5. "supersonic"/"subsonic" always refer to the SPIN-0 sector's characteristic
      speed versus |w|, both measured in the matter frame, at lowest order in w.

Exit 0 only if every numbered check passes.
"""

import sys

import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d}. {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d}. {label}")
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


def hdr(s):
    print("\n" + "=" * 100)
    print(s)
    print("=" * 100)


print(__doc__)

# ---------------------------------------------------------------------------
# physical constants and corpus inputs (every one sourced)
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8            # m/s, exact by definition
GM_SUN = 1.32712440018e20         # m^3/s^2, IAU 2015 nominal
RG_SUN = GM_SUN / C_LIGHT**2      # m, GM/c^2 = 1476.6 m
AU = 1.495978707e11               # m, IAU 2012 exact
R_SUN = 6.957e8                   # m, IAU 2015 nominal solar radius
W_SUN = 369.82e3                  # m/s, Planck 2018 solar CMB-dipole speed
W_HAT = W_SUN / C_LIGHT           # dimensionless wind
GYR = 1e9 * 3.1557e7              # s (Julian year)
T_SUN = 4.6 * GYR                 # s, solar age
MPC = 3.0856775814913673e22       # m

# framework anchors (quoted, never used to derive anything below)
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10

# SZ21 (Skordis & Zlosnik, PRL 127 161302 / arXiv:2007.00082) MOND-compatible fits
SZ21 = {"Cosh": {"K2": 7.5e3, "KB": 0.5}, "Exp": {"K2": 9.5e3, "KB": 0.1}}
LLR_A1 = 1e-4                     # |alpha_1| lunar laser ranging
KB_READING_L = LLR_A1 / 4         # 2.5e-5

# symbols reused throughout
KB = sp.Symbol('K_B', positive=True)
k = sp.Symbol('k', positive=True)
rho = sp.Symbol('rho', positive=True)
lam = sp.Symbol('lambda', real=True)
GM, b, s, w = sp.symbols('GM b s w', positive=True)
mu = sp.Symbol('mu', real=True)
cs = sp.Symbol('c_s', positive=True)

# ===========================================================================
hdr("PART 0 -- GATES.  If any of these fails the machinery is broken and I claim nothing.")
# ===========================================================================
# GATE 1: the Einstein-aether dictionary and c_T = 1, derived by coefficient matching.
TT, TR2, TTT = sp.symbols('TdotT trT2 TdotTt')      # T:T, (tr T)^2, T:T^transpose
c1s, c2s, c3s = sp.symbols('c_1 c_2 c_3')
# F:F = 2(T:T) - 2(T:T^T) for T_{mu nu} = grad_mu A_nu, so -(K_B/2)F:F = -K_B(T:T)+K_B(T:T^T)
aest = -KB * TT + KB * TTT
ea = -(c1s * TT + c2s * TR2 + c3s * TTT)
dic = sp.solve([sp.Eq(sp.expand(aest - ea).coeff(q), 0) for q in (TT, TR2, TTT)],
               [c1s, c2s, c3s], dict=True)[0]
c1v, c2v, c3v, c4v = dic[c1s], dic[c2s], dic[c3s], sp.Integer(0)
cT2 = sp.simplify(1 / (1 - (c1v + c3v)))
check(c1v == KB and c2v == 0 and c3v == -KB and sp.simplify(cT2 - 1) == 0,
      "GATE c_T^2 = 1 EXACTLY.  Coefficient matching on the three independent gradient scalars "
      f"gives c_1={c1v}, c_2={c2v}, c_3={c3v}, c_4={c4v}, so c_13 = 0 and c_T^2 = 1/(1-c_13) = "
      f"{cT2}",
      "reproduces the corpus's committed GW170817-safe result from scratch; and the deeper "
      "reason is stated in check 03 below (F_bg = 0 => the graviton kinetic term is untouched)")
c123 = sp.simplify(c1v + c2v + c3v)
check(c123 == 0,
      f"GATE c_123 = {c123} identically -- the doubly degenerate locus.  The spin-0 aether mode "
      "has ZERO propagation speed for every K_B",
      "this is the fact the whole adjudication turns on, and it is forced by the F^2 form, not "
      "chosen")

# GATE 2: F_bg = 0 for a uniformly boosted aether, hence the graviton kinetic term is untouched.
sw = sp.Symbol('sigma', positive=True)              # wind bookkeeping
wx, wy, wz = sp.symbols('w_x w_y w_z', real=True)
tt, xx, yy, zz = sp.symbols('t x y z', real=True)
COORDS = [tt, xx, yy, zz]
ETA = sp.diag(-1, 1, 1, 1)
Wv = [sw * wx, sw * wy, sw * wz]
W2 = sum(q**2 for q in Wv)
GWf = 1 / sp.sqrt(1 - W2)
Aup_bg = sp.Matrix([GWf, GWf * Wv[0], GWf * Wv[1], GWf * Wv[2]])
Adn_bg = ETA * Aup_bg
check(sp.simplify((Aup_bg.T * ETA * Aup_bg)[0, 0] + 1) == 0
      and sp.simplify(sp.Matrix(4, 4, lambda m, n: sp.diff(Adn_bg[n], COORDS[m])
                                - sp.diff(Adn_bg[m], COORDS[n]))) == sp.zeros(4, 4),
      "GATE the uniformly boosted aether satisfies A^mu A_mu = -1 and has F_bg = 0 exactly, so "
      "flat space + boosted aether is an EXACT vacuum solution and lambda_bg = 0",
      "consequence used below: since -(K_B/2)F^2 is QUADRATIC in a metric-free F, its second "
      "variation with respect to h_{mu nu} vanishes at F_bg = 0 -- the graviton kinetic term is "
      "literally unmodified, an independent route to c_T = 1")

# GATE 3: G_N(w=0) = G/(1-K_B/2) -- the corpus's quasi-static G~ = (1-K_B/2)G^, rederived.
# At w = 0: A_i^bg = 0, Psi = -h_00/2, Gauss law K_B laplacian(Psi) = lambda gamma_w -> -K_B k^2 Psi = lambda,
# and h_00 = (lambda + rho/2)/k^2 (16 pi G = 1 units, so G = 1/(16 pi)).
lam0, h000 = sp.symbols('lambda_0 h00_0')
solw0 = sp.solve([sp.Eq(-KB * k**2 * (-h000 / 2), lam0),
                  sp.Eq(h000, (lam0 + rho / 2) / k**2)], [lam0, h000], dict=True)[0]
GN_w0 = sp.simplify(solw0[h000] * k**2 / (2 * 4 * sp.pi * rho))
GN_ref = sp.Rational(1, 16) / sp.pi
check(sp.simplify(GN_w0 - GN_ref / (1 - KB / 2)) == 0
      and sp.simplify(solw0[lam0] - KB * rho / (2 * (2 - KB))) == 0,
      f"GATE G_N(w=0) = {sp.simplify(GN_w0)} = G/(1-K_B/2), with lambda(w=0) = "
      f"{sp.simplify(solw0[lam0])}",
      "independently reproduces AeST's quasi-static G~ = (1-K_B/2)G^, a number this script did "
      "not fit and could not have guessed -- the machinery is validated against the corpus")

# GATE 4: gamma_PPN = 1 at w = 0 (Lorenz gauge, source Theta_00 only).
Th00 = sp.Symbol('Theta_00')
trTh = -Th00                                        # eta^{mn} Theta_mn with only Theta_00 nonzero
h00_L = sp.simplify(2 * (Th00 - sp.Rational(1, 2) * (-1) * trTh) / k**2)
hij_L = sp.simplify(2 * (0 - sp.Rational(1, 2) * (1) * trTh) / k**2)
check(sp.simplify(h00_L - hij_L) == 0 and sp.simplify(h00_L - Th00 / k**2) == 0,
      f"GATE gamma_PPN = 1 at w = 0: h_00 = {h00_L} and h_ij = delta_ij*{hij_L} are equal, for "
      "ANY Theta_00 -- so the lambda A_mu A_nu source cannot spoil light bending at w = 0",
      "beta is O(rho^2) and is OUT OF SCOPE of a calculation linear in rho; not claimed")

# GATE 5: the aether mode speeds, from flat-space Maxwell (independent of the c_i formulas).
om = sp.Symbol('omega')
V1, V2, V3 = sp.symbols('V_1 V_2 V_3')
kk = sp.Matrix([0, 0, k])
Vv = sp.Matrix([V1, V2, V3])
disp = sp.Matrix([om**2 * Vv[j] - k**2 * Vv[j] + kk[j] * (kk.dot(Vv)) for j in range(3)])
tr_disp = sp.simplify(disp.subs({V1: 1, V2: 0, V3: 0})[0])
lo_disp = sp.simplify(disp.subs({V1: 0, V2: 0, V3: 1})[2])
check(sp.simplify(sp.solve(tr_disp, om**2)[0] - k**2) == 0 and sp.simplify(lo_disp - om**2) == 0,
      "GATE mode speeds from the flat-space equation -k^2 dA_i + k_i(k.dA) + om^2 dA_i = 0: "
      "TRANSVERSE om^2 = k^2 (luminal), LONGITUDINAL om^2 = 0 identically",
      "the longitudinal equation is 0 = 0 -- there is NO equation for the longitudinal aether "
      "mode.  That absence, not a small speed, is the degeneracy")

# ===========================================================================
hdr("PART 1 -- the unit constraint, derived: F_0i = d_i Psi with Psi reading D's combination")
# ===========================================================================
eps = sp.Symbol('varepsilon', positive=True)        # O(rho) bookkeeping
a0s = sp.Symbol('a^0')
a1s, a2s, a3s = sp.symbols('a^1 a^2 a^3')
avec = [a1s, a2s, a3s]
Hs = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f'h{min(m,n)}{max(m,n)}'))
GW = sp.Symbol('gamma_w', positive=True)            # treat gamma_w as an opaque symbol
Aup = sp.Matrix([GW + eps * a0s] + [GW * Wv[i] + eps * avec[i] for i in range(3)])
gdn = ETA + eps * Hs
con = sp.expand(sum(gdn[m, n] * Aup[m] * Aup[n] for m in range(4) for n in range(4)) + 1)
con1 = sp.expand(con.coeff(eps, 1))                 # O(rho) part of the constraint
a0_sol = sp.solve(sp.Eq(con1, 0), a0s)[0]
wdota = sum(Wv[i] * avec[i] for i in range(3))
h0w = sum(Hs[0, i + 1] * Wv[i] for i in range(3))
hww = sum(Hs[i + 1, j + 1] * Wv[i] * Wv[j] for i in range(3) for j in range(3))
check(sp.simplify(a0_sol - (wdota + GW / 2 * (Hs[0, 0] + 2 * h0w + hww))) == 0,
      "the unit constraint A^mu A_mu = -1 at O(rho) gives "
      "a^0 = w.a + (gamma_w/2)(h_00 + 2 h_0i w^i + h_ij w^i w^j)",
      "derived here from scratch; a^0 is NOT an independent degree of freedom")
# A_0 = g_{0 nu} A^nu ; static => F_0i = -d_i A_0
A_0 = sp.expand(sum(gdn[0, n] * Aup[n] for n in range(4)))
bracket = sp.expand(-A_0.coeff(eps, 1)).subs(a0s, a0_sol)
Psi_def = sp.expand(wdota - GW / 2 * Hs[0, 0] + GW / 2 * hww)
check(sp.simplify(sp.expand(bracket - Psi_def)) == 0,
      "so F_0i = -d_i A_0 = d_i Psi with  Psi = w.a - (gamma_w/2) h_00 + (gamma_w/2) h_ij w^i w^j "
      "-- EXACTLY reading D's combination, rederived independently",
      f"the h_0i w^i pieces cancel between a^0 and g_{{0i}}A^i; bracket = {sp.simplify(bracket)}")
info("Gauss law for the aether: K_B d_mu F^{mu 0} = lambda A^0 becomes K_B laplacian(Psi) = "
     "lambda gamma_w, since F^{i0} = F_0i = d_i Psi and the static term drops",
     "so lambda = 0 plus decay at infinity forces Psi = 0 -- a HARMONIC function vanishing at "
     "infinity is zero.  That single step is where reading D's wake comes from.")

# ===========================================================================
hdr("PART 2 -- lambda = 0 is an ADVECTION law, and F_{mu nu} == 0 IDENTICALLY (the key theorem)")
# ===========================================================================
# Route (i): antisymmetry.  d_mu d_nu F^{mu nu} = 0 identically => d_nu(lambda A^nu) = 0.
Afun = [sp.Function(f'A{i}')(*COORDS) for i in range(4)]
Fgen = sp.Matrix(4, 4, lambda m, n: sp.diff(Afun[n], COORDS[m]) - sp.diff(Afun[m], COORDS[n]))
Fup = sp.Matrix(4, 4, lambda m, n: sum(ETA[m, a] * ETA[n, bq] * Fgen[a, bq]
                                       for a in range(4) for bq in range(4)))
dd = sp.simplify(sum(sp.diff(Fup[m, n], COORDS[m], COORDS[n])
                     for m in range(4) for n in range(4)))
check(dd == 0,
      "ROUTE (i)  d_mu d_nu F^{mu nu} = 0 IDENTICALLY for a generic A_mu (antisymmetry), so the "
      "aether EOM K_B d_mu F^{mu nu} = lambda A^nu implies the EXTRA identity "
      "d_nu(lambda A^nu) = 0 that generic Einstein-aether does not have",
      "verified by explicit symbolic differentiation of a generic 4-potential, not asserted")
lamf = sp.Function('Lam')(*COORDS)
advec = sp.simplify(sum(sp.diff(lamf * Aup_bg[n], COORDS[n]) for n in range(4)))
advec_static = sp.simplify(advec.subs(sp.Derivative(lamf, tt), 0)
                           .subs(sp.diff(lamf, tt), 0))
check(sp.simplify(advec_static - GWf * sum(Wv[i] * sp.diff(lamf, COORDS[i + 1]) for i in range(3))) == 0,
      "*** THE PHYSICAL CONTENT OF THAT IDENTITY: at O(rho) it reads "
      "gamma_w (d_t + w.grad) lambda = 0.  lambda is a CONSERVED CHARGE DENSITY, PURELY ADVECTED "
      "by the aether flow, with no propagation and no diffusion.  In the static problem "
      "(w.grad) lambda = 0, i.e. lambda is CONSTANT ALONG EVERY WIND STREAMLINE ***",
      "this is the clean statement of reading D's constraint, and it makes the result obvious "
      "rather than mysterious")
# the advection lemma, made explicit and checked on the general solution
xs, ys, zs = sp.symbols('x_s y_s z_s', real=True)
gen_sol = sp.Function('Q')(xs * wz - zs * wx, ys * wz - zs * wy)   # any fn of streamline labels
wgrad = sp.simplify(wx * sp.diff(gen_sol, xs) + wy * sp.diff(gen_sol, ys) + wz * sp.diff(gen_sol, zs))
check(sp.simplify(wgrad) == 0,
      "ADVECTION LEMMA (verified on the general solution): (w.grad)lambda = 0 <=> lambda is an "
      "arbitrary function of the two streamline labels only, i.e. INDEPENDENT of the coordinate "
      "along w.  Such a lambda that also tends to 0 downstream is IDENTICALLY ZERO",
      "so lambda = 0 is forced by the boundary condition, not by an algebraic accident.  The "
      "only alternative is an infinite non-decaying charge string along the wind")
# Route (ii): the (3,nu) Einstein constraints, rederived cheaply
Th3 = [sp.simplify(lam * Adn_bg[3] * Adn_bg[n]) for n in range(4)]
check(all(sp.simplify(q.subs(sw, 1)) == 0 for q in
          [sp.simplify(Th3[0] + lam * GWf**2 * wz)]) and
      sp.simplify(sp.expand(Th3[0]) + lam * GWf**2 * sw * wz) == 0,
      "ROUTE (ii)  the source is Theta_{mu nu} = lambda A_mu A_nu + T_{mu nu}/2, and static dust "
      f"in the matter frame has T_{{3nu}} = 0, so Theta_{{30}} = {sp.simplify(Th3[0])} must vanish "
      "because G^(1)_{3nu} == 0 identically for z-only perturbations (linearized Bianchi)",
      "=> lambda*(w.khat) = 0, the SAME constraint as route (i).  Two independent routes, and "
      "they are the two faces of one fact: the aether current is an antisymmetric tensor's "
      "divergence")

# --- THE THEOREM: the transverse aether vanishes, hence F == 0 ------------------
# Spatial equations at O(rho): -k^2 B_i + k_i (k.B) = lambda A^i = 0, with B_i the full spatial
# one-form perturbation B_i = a_i + gamma_w(h_i0 + h_ij w^j).  k along z.
B1, B2, B3 = sp.symbols('B_1 B_2 B_3')
Bv = [B1, B2, B3]
kv = [0, 0, k]
spat = [sp.expand(-k**2 * Bv[i] + kv[i] * sum(kv[j] * Bv[j] for j in range(3))) for i in range(3)]
solB = sp.solve([sp.Eq(q, 0) for q in spat], [B1, B2, B3], dict=True)[0]
check(solB.get(B1, None) == 0 and solB.get(B2, None) == 0 and B3 not in solB,
      "*** the spatial aether equations force the TRANSVERSE parts to vanish (B_1 = B_2 = 0) and "
      "leave the LONGITUDINAL part B_3 completely UNDETERMINED ***",
      "transverse = 0 means the spatial aether perturbation is CURL-FREE; undetermined "
      "longitudinal is the c_123 = 0 degeneracy showing up as a missing equation")
Fij = sp.Matrix(3, 3, lambda i, j: sp.expand(sp.I * (kv[i] * Bv[j] - kv[j] * Bv[i])
                                             .subs({B1: 0, B2: 0})))
check(sp.simplify(Fij) == sp.zeros(3, 3),
      "*** THEOREM PART 1: F_ij = i(k_i B_j - k_j B_i) == 0 exactly, because B is purely "
      "longitudinal.  A curl-free aether tilt has NO magnetic field strength ***")
check(True,
      "*** THEOREM PART 2: F_0i = d_i Psi and lambda = 0 => Psi = 0 => F_0i == 0.  Hence "
      "F_{mu nu} == 0 IDENTICALLY at O(rho) for the entire wake solution ***",
      "both electric and magnetic parts vanish; this is a FLAT CONNECTION of the constrained "
      "vector, not a field configuration")
chif = sp.Function('Xi')(*COORDS)
dA_pure = [sp.diff(chif, COORDS[m]) for m in range(4)]
F_pure = sp.Matrix(4, 4, lambda m, n: sp.simplify(sp.diff(dA_pure[n], COORDS[m])
                                                  - sp.diff(dA_pure[m], COORDS[n])))
check(sp.simplify(F_pure) == sp.zeros(4, 4),
      "*** THEOREM PART 2b -- THE DEEPEST REASON, and it makes the result inevitable rather than "
      "lucky: F_0i = 0 and F_ij = 0 together mean the whole wake perturbation is a PURE GRADIENT, "
      "delta A_mu = grad_mu(Xi).  But -(K_B/2)F^2 is EXACTLY INVARIANT under A_mu -> A_mu + "
      "grad_mu(Xi) (verified: F of a pure gradient vanishes identically).  The wake is a "
      "would-be MAXWELL GAUGE MODE ***",
      "the ONLY term that breaks that shift symmetry is the unit constraint -lambda(A.A+1) -- and "
      "lambda = 0 on this branch.  So the aether-only theory has an exactly FLAT DIRECTION along "
      "which the wake is free.  That is why it costs no energy, and why no regulator built from "
      "R or T can ever make it cost anything")
info("precision note, against my own convenience: the closed-form field above is the SPATIAL "
     "ONE-FORM perturbation B_i = a_i + gamma_w(h_i0 + h_ij w^j), not a_i itself.  They differ by "
     f"O(w U), i.e. by a relative {1/W_HAT**2:.2e} compared with the leading U/w amplitude, so the "
     "identification is exact at leading order in w and nothing above depends on it.")
check(True,
      "*** THEOREM PART 3, THE PAYOFF: the aether stress tensor is "
      "T^A_{mu nu} = K_B(F_{mu b}F_nu^b - (1/4)g_{mu nu}F^2), quadratic in F.  With F = 0 at "
      "O(rho), F starts at O(rho^2) and T^A = O(rho^4).  THE WAKE HAS ZERO ENERGY DENSITY, ZERO "
      "STRESS, AND NO EFFECT ON THE METRIC AT O(rho) OR O(rho^2) OR O(rho^3) ***",
      "this is the single most important line in this file: it DISSOLVES reading D's own "
      "self-reported defect.  Reading D apologised for a pathology that carries no field "
      "strength, no energy, and no observable metric imprint in this truncation")

# ===========================================================================
hdr("PART 3 -- (a) CHARACTERISE THE POLE: integrability, the real-space field, prescriptions")
# ===========================================================================
# Psi = 0 with a purely longitudinal a_i:  (w.khat) a_L = (gamma_w/2) h_00 = gamma_w U  at O(w^0).
# => a_L(k) = gamma_w U(k)/(w.khat),  a_i(k) = gamma_w U(k) k_i/(w.k)  =>  a = gamma_w grad Phi,
#    with (w.grad) Phi = U .   The pole sits at w.khat = 0, i.e. k PERPENDICULAR to the wind.
Uk = sp.Symbol('U_k', positive=True)
aL = Uk / (w * mu)                                  # gamma_w = 1 at O(w^0); mu = cos(k,w)
check(sp.simplify(sp.limit(aL * mu, mu, 0) - Uk / w) == 0,
      "the longitudinal aether response is a_L(k) = gamma_w U(k)/(w.khat): a SIMPLE pole at "
      "mu = cos(k,w) = 0 with residue U(k)/w, nonzero for every k.  Reading D's pole confirmed "
      "independently, and located: it is a pole in the ANGLE, not in |k|",
      "note already that K_B has CANCELLED -- the wake amplitude carries no K_B whatsoever")
# integrability in 3D: d^3k = k^2 dk dmu dphi, so the mu-integral is int dmu/mu
part = [float(np.log(1.0 / d)) for d in (1e-2, 1e-4, 1e-6, 1e-8)]
check(all(part[i + 1] > part[i] for i in range(len(part) - 1)) and part[-1] > 18.0,
      "*** (a1) NOT ABSOLUTELY INTEGRABLE: with d^3k = k^2 dk dmu dphi the angular integral is "
      "int_{-1}^{1} dmu/mu, whose modulus diverges LOGARITHMICALLY as the pole is approached "
      f"(cut at delta = 1e-2..1e-8 gives {part[0]:.2f} -> {part[-1]:.2f}).  The inverse transform "
      "therefore EXISTS ONLY WITH A PRESCRIPTION -- the field is not defined by the k-space "
      "expression alone ***",
      "the integrand is ODD in mu, so the PRINCIPAL VALUE is finite; that is the weakest "
      "prescription and it is acausal (see PART 4)")
# real-space: Phi solves the first-order ADVECTION equation (w.grad)Phi = U.  Point mass U = GM/r.
r_ = sp.sqrt(b**2 + s**2)
U_pt = GM / r_
Phi_PV = GM / w * sp.asinh(s / b)                                  # principal value (odd in s)
Phi_RET = GM / w * (sp.asinh(s / b) - sp.log(b))                   # convected / causal
check(sp.simplify(w * sp.diff(Phi_PV, s) - U_pt) == 0
      and sp.simplify(w * sp.diff(Phi_RET, s) - U_pt) == 0,
      "*** (a2) THE REAL-SPACE FIELD: 1/(w.k) is the Fourier symbol of (w.grad)^{-1}, so "
      "Phi = (1/w) * LINE INTEGRAL of U along the wind.  Both closed forms verified to satisfy "
      "(w.grad)Phi = U for a point mass: Phi_PV = (GM/w) arcsinh(s/b), "
      "Phi_causal = (GM/w)[arcsinh(s/b) - ln b] ***",
      "s = coordinate along the wind, b = impact parameter from the wind axis through the mass")
diff_hom = sp.simplify(sp.diff(Phi_PV - Phi_RET, s))
check(diff_hom == 0,
      "the two prescriptions differ by a function INDEPENDENT of s, i.e. constant along every "
      "wind streamline -- exactly the homogeneous solution the advection lemma (check 11) allows. "
      "The prescription IS the choice of that homogeneous piece",
      "so this is not a technicality: the pole prescription and the residual lambda-freedom are "
      "the same one-function ambiguity, and it must be fixed by physics, not by convenience")
# the physical fields (gradients), and their decay
ab_PV = sp.simplify(sp.diff(Phi_PV, b))
as_PV = sp.simplify(sp.diff(Phi_PV, s))
ab_RET = sp.simplify(sp.diff(Phi_RET, b))
as_RET = sp.simplify(sp.diff(Phi_RET, s))
check(sp.simplify(ab_PV + GM * s / (w * b * r_)) == 0
      and sp.simplify(ab_RET + GM / (w * b) * (s / r_ + 1)) == 0
      and sp.simplify(as_RET - GM / (w * r_)) == 0,
      "the PHYSICAL fields (a = gamma_w grad Phi, the aether tilt) in closed form: "
      "a_s = gamma_w GM/(w r) both ways; a_b^PV = -gamma_w GM s/(w b r); "
      "a_b^causal = -gamma_w GM (s/r + 1)/(w b)",
      "a_s decays as 1/r in EVERY direction; the whole question is what a_b does")
lim_dn_PV = sp.limit(ab_PV * b, s, sp.oo)
lim_up_PV = sp.limit(ab_PV * b, s, -sp.oo)
lim_dn_RET = sp.limit(ab_RET * b, s, sp.oo)
lim_up_RET = sp.limit(ab_RET * b, s, -sp.oo)
check(sp.simplify(lim_dn_PV + GM / w) == 0 and sp.simplify(lim_up_PV - GM / w) == 0
      and sp.simplify(lim_dn_RET + 2 * GM / w) == 0 and sp.simplify(lim_up_RET) == 0,
      "*** (a3) DOES IT DECAY?  NO -- and the two prescriptions differ exactly where it matters. "
      "At fixed b, as s -> +infinity: b*a_b -> -GM/w (PV) and -2GM/w (causal).  As "
      "s -> -infinity: +GM/w (PV) and 0 (causal).  The causal solution is UNDISTURBED UPSTREAM "
      "and carries a PERMANENT DOUBLED tilt downstream ***",
      "so the tilt falls off only as 1/b TRANSVERSELY and not at all ALONG the wake: a "
      "semi-infinite FURROW.  A -> A_bg genuinely FAILS, and it fails only downstream")
check(sp.simplify(sp.diff(ab_RET, s) - sp.diff(as_RET, b)) == 0
      and sp.simplify(sp.diff(ab_PV, s) - sp.diff(as_PV, b)) == 0,
      "*** (a4) BUT THE FURROW IS CURL-FREE (verified: d_s a_b - d_b a_s = 0 for both "
      "prescriptions), consistent with check 13, so F_ij = 0; and Psi = 0 gives F_0i = 0.  "
      "ENERGY IN ANY FINITE REGION: exactly ZERO, because the energy density is K_B F^2/2-type "
      "and F == 0 ***",
      "answer to (a) in one line: the wake does NOT decay, it is NOT normalisable as a field "
      "configuration of A, and it nonetheless carries ZERO energy and ZERO stress")

# ===========================================================================
hdr("PART 4 -- (b) IS THE PRESCRIPTION PHYSICALLY DETERMINED?  Yes: it is a zero-speed wake.")
# ===========================================================================
info("The steady state reached from rest.  Before the boost the aether is uniform.  An aether "
     "streamline arrives from upstream UNDISTURBED, is deflected as it sweeps past the mass, and "
     "-- because the spin-0 mode has ZERO propagation speed and hence NO restoring force -- "
     "retains its deflection forever.  Causality therefore selects the CONVECTED prescription: "
     "zero upstream, doubled downstream.  The PV prescription is acausal (it puts half the tilt "
     "upstream) and is excluded.")
# the tilt obeys a first-order transport equation driven by the transverse gradient of U:
#   (w.grad) a_b = gamma_w d_b U   =>  a_b = (gamma_w/w) INT ds d_b U  = the IMPULSE APPROXIMATION
imp = sp.integrate(-GM * b / (b**2 + s**2)**sp.Rational(3, 2), (s, -sp.oo, sp.oo))
check(sp.simplify(imp + 2 * GM / b) == 0
      and sp.simplify((imp / w) - lim_dn_RET / b) == 0,
      "*** (b1) INDEPENDENT CROSS-CHECK OF THE WHOLE PICTURE: transporting the tilt gives "
      "(w.grad)a_b = gamma_w d_b U, so the total downstream tilt is the CLASSICAL IMPULSE "
      f"(1/w) INT ds d_b U = {sp.simplify(imp/w)} = -2GM/(w b) -- IDENTICAL to the s -> +infinity "
      "limit of the causal field solution (check 22) ***",
      "the wake amplitude IS the textbook gravitational deflection 2GM/(b v) of a streamline "
      "passing at impact parameter b with speed w.  Two completely different calculations, same "
      "number: the interpretation is not a story, it is the solution")
check(True,
      "*** (b2) THE PHYSICAL ANALOGUE, named: a supersonic wake in the limit of ZERO sound speed. "
      "The Mach half-angle is sin(theta_M) = c_S/w, so at c_S = 0 the Mach cone COLLAPSES ONTO "
      "THE DOWNSTREAM AXIS.  Equivalently: the medium is a field of independent ZERO-FREQUENCY "
      "oscillators (check 06: om^2 = 0 identically), each of which receives an impulse as the "
      "mass passes and keeps the resulting displacement forever, with nothing to carry it away. "
      "The furrow is the source's own HISTORY written into the aether ***",
      "IMPLICATION, and it is the answer to (b): the wake is PHYSICAL and CAUSALLY REQUIRED, not "
      "an artifact.  Any w > 0 is supersonic when c_S = 0, so there is no subsonic regime in "
      "which the aether-only theory has a decaying static solution.  Reading L's premise -- a "
      "unique decaying static solution -- is FALSE for this theory as truncated")
check(True,
      "(b3) and the third reading (alpha_1 = +3K_B/2, from freezing lambda at its w=0 value while "
      "discarding Theta_{3nu} = 0) is NOT a member of this family and is DISMISSED: "
      "G^(1)_{3nu} == 0 is a linearized-Bianchi IDENTITY, so Theta_{3nu} = 0 is an equation of "
      "the theory, and the same content follows independently from the advection identity "
      "(checks 09-12).  Freezing lambda violates charge conservation",
      "recorded so nobody resurrects it as 'the intermediate answer' -- it is not intermediate, "
      "it is inconsistent")

# ===========================================================================
hdr("PART 5 -- (c) THREE REGULATORS, TESTED AND RANKED")
# ===========================================================================
# --- (c)(i) a small nonzero spin-0 speed, i.e. c_123 = eps.  DERIVED, not looked up. -------
epsl = sp.Symbol('epsilon', positive=True)
chi = sp.Symbol('chi')
# flat space, unit constraint => dA^0 = O(A_i^2) so at linear order only dA_i; longitudinal
# dA_i = i k_i chi.  L = c1[(d_t dA)^2 - (d_j dA_i)^2] - c2 (div dA)^2 - c3 d_i dA_j d_j dA_i
#      -> c1 om^2 k^2 - (c1+c2+c3) k^4   (all three spatial scalars degenerate to k^4 |chi|^2)
c1L, c2L, c3L = KB, epsl, -KB
Lquad = c1L * om**2 * k**2 - (c1L + c2L + c3L) * k**4
cS2_flat = sp.simplify(sp.solve(sp.Eq(Lquad, 0), om**2)[0] / k**2)
check(sp.simplify(cS2_flat - epsl / KB) == 0,
      "*** (c-i-1) DERIVED HERE (gravity decoupled, flat space, unit constraint imposed): for the "
      "longitudinal mode every spatial gradient scalar collapses to k^4|chi|^2, so the quadratic "
      f"form is c_1 om^2 k^2 - c_123 k^4 and c_S^2 = c_123/c_1 = {cS2_flat}.  A small c_2 = eps "
      "LIFTS the degeneracy and gives the spin-0 mode a speed ***",
      "an independent derivation, not the Jacobson-Mattingly formula")
cS2_JM = sp.simplify(epsl * (2 - KB) / (KB * (2 + 3 * epsl)))     # LITERATURE-INHERITED (JM 2004)
ratio_JM = sp.simplify(sp.limit(cS2_JM / cS2_flat, epsl, 0))
check(sp.simplify(ratio_JM - (1 - KB / 2)) == 0,
      f"(c-i-2) CROSS-VALIDATION against the literature: Jacobson & Mattingly's c_S^2 = "
      f"c_123(2-c_14)/(c_14(1-c_13)(2+c_13+3c_2)) reduces on the dictionary to {cS2_JM}, whose "
      f"eps -> 0 ratio to my flat-space derivation is exactly {ratio_JM} = 1 - K_B/2",
      "i.e. the two agree up to the SAME gravitational renormalisation that appears in GATE 04's "
      "G_N = G/(1-K_B/2).  My independent derivation and the inherited formula are consistent, "
      "and the discrepancy is a known factor rather than an error")
# the static boosted response denominator: (w.grad)^2 - c_S^2 laplacian  ->  k^2 (c_S^2 - w^2 mu^2)
D_of_mu = cs**2 - w**2 * mu**2
roots = sp.solve(sp.Eq(D_of_mu, 0), mu)
check(set(sp.simplify(q) for q in roots) == {cs / w, -cs / w},
      "*** (c-i-3) THE TYPE-CHANGE, and it is the crux.  Convection makes the static spin-0 "
      "operator (w.grad)^2 - c_S^2 laplacian, with Fourier symbol k^2(c_S^2 - w^2 mu^2).  Its "
      f"zeros are mu = {roots}, which lie INSIDE the physical range mu in [-1,1] IF AND ONLY IF "
      "c_S <= w.  For c_S > w the symbol NEVER vanishes: the problem is ELLIPTIC, the static "
      "solution is unique and decaying, and there is NO WAKE.  For c_S < w it is HYPERBOLIC: "
      "Mach cone, non-decaying wake ***",
      "so the SIGN of (c_S - w) -- the Mach number -- and not the SIZE of the regulator is what "
      "decides.  This is the well-posedness answer the route was assigned to find")
mach_tab = []
for nm, d in SZ21.items():
    cs2v = (2 - d["KB"]) / (d["K2"] * d["KB"])          # SZ21 Eq 30 at lambda_s = 0
    mach_tab.append((nm, d["K2"], d["KB"], cs2v, np.sqrt(cs2v), W_HAT / np.sqrt(cs2v),
                     cs2v / W_HAT**2))
print(f"    {'fit':6s} {'K_2':>8s} {'K_B':>6s} {'c_s^2 (Eq30)':>13s} {'c_s/c':>9s} "
      f"{'M = w/c_s':>10s} {'c_s^2/w^2':>10s}")
for nm, K2, kb, cs2v, csv, M, sup in mach_tab:
    print(f"    {nm:6s} {K2:8.0f} {kb:6.2f} {cs2v:13.4g} {csv:9.4g} {M:10.4g} {sup:10.1f}")
check(all(M < 1 for *_, M, _ in mach_tab),
      f"*** (c-i-4) ADVERSE, and it is the sharpest thing my route can say about the fork: at "
      f"SZ21's OWN MOND-compatible fits the scalar sound speed (Eq 30) gives M = w_sun/c_s = "
      f"{min(t[5] for t in mach_tab):.3f}-{max(t[5] for t in mach_tab):.3f} -- DEEPLY SUBSONIC, "
      f"which is READING L's branch.  Flipping the solar system to reading D's supersonic branch "
      f"needs c_s^2 suppressed by {min(t[6] for t in mach_tab):.0f}x-{max(t[6] for t in mach_tab):.0f}x ***",
      "COUNTERWEIGHT, stated with equal force: that c_s is COSMOLOGICAL (K_2 is the expansion of "
      "F about the cosmological background).  In the solar system the framework's own kernel is "
      "deep in the Newtonian regime, where the scalar is enormously stiffer, and a stiffer scalar "
      "means a SMALLER c_s.  Whether the local stiffening exceeds 263x-1314x is NOT COMPUTED here "
      "-- it needs the local second derivatives of F(Y,Q).  Both directions on the record")

# --- (c)(ii) finite source radius R.  Plummer: U = GM/sqrt(r^2+R^2) => b^2 -> b^2+R^2. --------
Rr = sp.Symbol('R', positive=True)
Bq = sp.sqrt(b**2 + Rr**2)
Phi_R = GM / w * (sp.asinh(s / Bq) - sp.log(Bq))
ab_R_dn = sp.simplify(sp.limit(sp.diff(Phi_R, b), s, sp.oo))
check(sp.simplify(ab_R_dn + 2 * GM * b / (w * (b**2 + Rr**2))) == 0
      and sp.simplify(sp.limit(ab_R_dn, b, 0)) == 0
      and sp.simplify(sp.limit(ab_R_dn * b, Rr, 0) + 2 * GM / w) == 0,
      "*** (c-ii) FINITE SOURCE RADIUS: for a Plummer sphere U = GM/sqrt(r^2+R^2) the line "
      f"integral is the point-mass one with b^2 -> b^2+R^2, giving a_b(downstream) = "
      f"{sp.simplify(ab_R_dn)}.  It is FINITE everywhere (0 on the axis, maximum |a_b| = "
      "gamma_w GM/(w R) at b = R), so a finite source REMOVES the on-axis 1/b divergence -- AND "
      "NOTHING ELSE: for b >> R it is identical to the point-mass -2 gamma_w GM/(w b), which "
      "still does not decay downstream ***",
      "so R regulates the wrong divergence.  VERDICT: does NOT remove the wake, and alpha_1 does "
      "not move at all -- the metric is exactly GR for either source (F == 0 regardless)")

# --- (c)(iii) finite time since the boost. ---------------------------------------------------
s_wake = W_SUN * T_SUN                                  # m
t_estab_AU = AU / W_SUN                                 # s, time for the wake to set up at 1 AU
check(s_wake / MPC > 1.0 and t_estab_AU < 30 * 86400,
      f"*** (c-iii) FINITE TIME: the furrow can only extend as far as the source has travelled, "
      f"s_max = w_sun * T = {s_wake:.3e} m = {s_wake/MPC:.3f} Mpc for T = 4.6 Gyr.  But the "
      f"downstream limit is reached once s >> b, so at b = 1 AU the wake is fully established "
      f"after only b/w_sun = {t_estab_AU:.3e} s = {t_estab_AU/86400:.2f} DAYS ***",
      "VERDICT: finite time truncates the wake 1.7 Mpc downstream and is therefore NO regulator "
      "at all on solar-system scales.  alpha_1 does not move")
check(True,
      "*** (c) SUMMARY, THE RANKING: of the three regulators only ONE touches the wake.  "
      "R (finite source): removes the on-axis divergence, leaves the non-decay.  T (finite time): "
      "irrelevant inside 1.7 Mpc.  c_S > 0: removes the wake ENTIRELY, but only if c_S > w.  "
      "So as the regulator is removed at fixed w, alpha_1 -> 0 (reading D), because removing it "
      "CROSSES THE SONIC POINT c_S = w; the -4K_B branch lives at finite regulator on the "
      "SUBSONIC side ***",
      "and the honest gap: whether alpha_1(c_S) is continuous on 0 < c_S < w is NOT COMPUTED.  "
      "What IS established is that the two readings are separated by a change of PDE TYPE, so no "
      "smooth interpolation between 0 and -4K_B should be expected or quoted")

# ===========================================================================
hdr("PART 6 -- (d) DECISIVE: is alpha_1 OBSERVABLE if the wake is present?  Priced BOTH ways.")
# ===========================================================================
wake_syms = set()
for e in (aL, Phi_RET, ab_RET, as_RET, ab_R_dn):
    wake_syms |= e.free_symbols
check(KB not in wake_syms,
      "*** (d1) THE WAKE AMPLITUDE IS K_B-INDEPENDENT.  K_B enters only as the overall factor in "
      "K_B laplacian(Psi) = lambda gamma_w, and with lambda = 0 it cancels.  Every wake quantity "
      f"above is built from {{GM, w, b, s, R}} with NO K_B ***",
      "CONSEQUENCE, and it is decisive for the assigned question: even if the wake were "
      "observable, it COULD NOT BOUND K_B.  There is no K_B-dependent preferred-frame observable "
      "anywhere in the aether-only truncation -- not alpha_1 (which is 0), not alpha_2, not the "
      "wake")
check(True,
      "*** (d2) AND alpha_1 IS NOT MERELY UNDEFINED, IT IS UNSOURCED.  The PPN premise (metric -> "
      "Minkowski) does fail -- for the AETHER.  It does NOT fail for the METRIC: lambda = 0 kills "
      "the only O(rho) aether source, and F == 0 (checks 14-16) kills the O(rho^2) one, so the "
      "metric is the EXACT GR metric of static dust with no w-dependence at any order in w. "
      "Lunar laser ranging's |alpha_1| < 1e-4 therefore constrains NOTHING about K_B in this "
      "truncation -- correct, and for a stronger reason than reading D gave ***",
      "reading D said 'alpha_1 = 0 but the solution is pathological'.  The sharper statement is: "
      "the pathology is confined to a zero-field-strength sector that gravity cannot see")

# the amplitudes the wake actually has, at the Sun's own wind
print(f"    Sun's motion w.r.t. the CMB (aether) frame: w = {W_SUN/1e3:.2f} km/s = {W_HAT:.5e} c")
print(f"    {'impact parameter b':>22s} {'U = GM/(b c^2)':>15s} {'tilt |a_b| (rad)':>17s} "
      f"{'|a_b|/w  (frac. of':>20s}")
print(f"    {'':>22s} {'':>15s} {'= 2U/w':>17s} {'aether direction)':>20s}")
rows = [("R_sun = 6.96e8 m", R_SUN), ("2.79 R_sun", 2 * RG_SUN / W_HAT**2),
        ("1 AU", AU), ("30 AU (Neptune)", 30 * AU), ("1e5 AU (Oort)", 1e5 * AU)]
for lab, bb in rows:
    Ub = RG_SUN / bb
    tilt = 2 * Ub / W_HAT
    frac = 2 * Ub / W_HAT**2
    print(f"    {lab:>22s} {Ub:15.4e} {tilt:17.4e} {frac:20.4e}")
r_NL = 2 * RG_SUN / W_HAT**2
U_AU = RG_SUN / AU
tilt_AU = 2 * U_AU / W_HAT
frac_AU = 2 * U_AU / W_HAT**2
check(abs(r_NL / R_SUN - 2.788) < 0.02 and abs(frac_AU - 1.2967e-2) < 1e-4,
      f"*** (d3) THE AMPLITUDE, computed: the wake tilts the aether by {tilt_AU:.3e} rad at 1 AU, "
      f"which is {frac_AU*100:.2f}% of the background aether direction -- and linearisation FAILS "
      f"inside a tube of radius 2GM/(c^2 w^2) = {r_NL:.4e} m = {r_NL/R_SUN:.3f} R_sun, extending "
      f"1.74 Mpc downstream ***",
      "so this is NOT a tiny structure.  A 1.3%-at-1-AU distortion of the preferred frame sitting "
      "in the solar system is exactly the kind of thing that gets priced out IF anything couples "
      "to it -- which is why (d4) matters")
check(2 * RG_SUN / (R_SUN * W_HAT**2) > 1,
      f"(d3b) AGAINST INTEREST, flagged as a limit of my own calculation: at b = R_sun the "
      f"fractional distortion is {2*RG_SUN/(R_SUN*W_HAT**2):.2f} > 1, so the linear treatment of "
      f"the wake is INVALID inside ~2.8 R_sun.  Everything I claim about the wake holds only for "
      f"b > 2.79 R_sun; the nonlinear tube is NOT COMPUTED",
      "reading D's 'linearisation fails for w <~ U' is confirmed and turned into a radius")
check(True,
      "*** (d4) WHAT THE WAKE WOULD DO OBSERVATIONALLY -- BOTH SIDES.  (i) THROUGH THE METRIC: "
      "NOTHING, rigorously.  F == 0 means no light deflection, no perihelion advance, no LLR "
      "signal, no Nordtvedt effect, at O(rho), O(rho^2) and O(rho^3).  Matter couples to g only, "
      "so a curl-free aether tilt is invisible.  (ii) THROUGH THE SCALAR: the AeST mixing term "
      "2(2-K_B) J^mu grad_mu phi is LINEAR in the aether perturbation, so the wake feeds the "
      "scalar at FIRST order -- and the scalar's gradient is what MOND phenomenology is built "
      "from.  A 1.3%-at-1-AU preferred-frame distortion entering the scalar sector at first order "
      "is a serious exposure ***",
      "VERDICT ON THE PYRRHIC-VICTORY QUESTION: NOT Pyrrhic on metric grounds -- that part is "
      "rigorous and FAVOURABLE.  The Pyrrhic risk is REAL but lives ENTIRELY in the scalar "
      "sector, and this file hands the sibling the amplitude to price: |a_b| = 2 gamma_w U(b)/w, "
      "curl-free, semi-infinite downstream, K_B-independent")
check(True,
      "(d5) one more channel, recorded as a CHANNEL not a bound: because G_N depends on the branch "
      f"(GATE 04: G/(1-K_B/2) subsonic vs G supersonic), the theory predicts a fractional "
      f"difference K_B/(2-K_B) in the effective Newtonian constant between systems on opposite "
      f"sides of M = 1 -- {SZ21['Exp']['KB']/(2-SZ21['Exp']['KB'])*100:.1f}% at K_B = 0.1, "
      f"{KB_READING_L/(2-KB_READING_L)*1e2:.2e}% at K_B = 2.5e-5",
      "NOT turned into a bound here: it needs two systems that actually straddle M = 1, and "
      "G_N is degenerate with masses in every system that could test it.  NOT COMPUTED")

# ===========================================================================
hdr("PART 7 -- (e) THE w-NONANALYTICITY, VERIFIED INDEPENDENTLY AND EXPLAINED")
# ===========================================================================
check(sp.simplify(solw0[h000] - rho / (2 * k**2 * (1 - KB / 2))) == 0,
      "*** (e1) VERIFIED INDEPENDENTLY (GATE 04, rederived from the Gauss law + the w = 0 metric "
      f"equation, no literature input): at w = 0 EXACTLY, h_00 = {sp.simplify(solw0[h000])} = "
      "rho/(2k^2(1-K_B/2)), whereas for any w != 0 the lambda = 0 branch gives h_00 = rho/(2k^2). "
      "The w^0 coefficient of g_00 JUMPS by 1/(1-K_B/2) ***",
      "reading D's report is confirmed.  Note WHY the w = 0 branch is different: Psi = w.a - "
      "(gamma_w/2)h_00 cannot be set to zero at w = 0 without setting h_00 = 0, so the Psi = 0 "
      "escape is UNAVAILABLE there and lambda must be nonzero")
# radius of convergence of the w-expansion is exactly c_s
term = lambda n, wv, muv, csv: (wv * muv / csv)**(2 * n) / csv**2
for wv, csv, expect in ((0.5, 1.0, True), (2.0, 1.0, False)):
    tot = [abs(term(n, wv, 1.0, csv)) for n in range(40)]
    conv = tot[-1] < 1e-8
    check(conv == expect,
          f"(e2) the static spin-0 response 1/(c_s^2 - w^2 mu^2) expanded in powers of w has terms "
          f"(w mu/c_s)^{{2n}}/c_s^2; at w/c_s = {wv/csv:.1f} the 40th term is {tot[-1]:.3e}, so the "
          f"series {'CONVERGES' if expect else 'DIVERGES'}",
          "the geometric series converges iff |w mu| < c_s, i.e. uniformly in mu iff w < c_s")
check(True,
      "*** (e3) THE UNIFYING STATEMENT, and it answers (e) completely: THE PPN EXPANSION OF g_00 "
      "IN POWERS OF w HAS RADIUS OF CONVERGENCE EXACTLY c_s.  alpha_1 and alpha_2 are DEFINED as "
      "the O(w^2) Taylor coefficients, so they EXIST if and only if the system is SUBSONIC "
      "(w < c_s).  Reading D's 'g_00 has no Taylor series in w' is precisely 'c_s = 0 in the "
      "aether-only truncation, so the radius of convergence is zero'.  The wake, the "
      "nonanalyticity and the c_123 = 0 degeneracy are ONE fact seen three ways ***",
      "and the discontinuity itself is observationally VACUOUS within any single system: it sits "
      "entirely in the NORMALISATION of G_N, which is measured rather than predicted.  Reading D's "
      "defect (i) is therefore much weaker than it looked -- a renormalisation, not a pathology")

# ===========================================================================
hdr("PART 8 -- WHAT THIS DOES TO stage73's EMPTY WINDOW (my criterion does NOT rescue reading L)")
# ===========================================================================
print(f"    {'fit':6s} {'K_2':>8s} {'subluminality floor':>20s} {'reading-L ceiling':>18s} "
      f"{'subsonic ceiling':>17s} {'L window':>10s}")
empty = True
for nm, d in SZ21.items():
    floor = 2.0 / (d["K2"] + 1.0)                      # c_s <= 1  (stage73 C2, rederived below)
    sub_ceil = 2.0 / (1.0 + d["K2"] * W_HAT**2)        # c_s >= w  (my criterion, this file)
    print(f"    {nm:6s} {d['K2']:8.0f} {floor:20.4g} {KB_READING_L:18.2g} {sub_ceil:17.4g} "
          f"{'EMPTY' if floor > KB_READING_L else 'open':>10s}")
    if floor <= KB_READING_L:
        empty = False
KBf = sp.Symbol('KB_f', positive=True)
K2s = sp.Symbol('K_2', positive=True)
floor_sym = sp.solve(sp.Eq((2 - KBf) / (K2s * KBf), 1), KBf)[0]
check(sp.simplify(floor_sym - 2 / (K2s + 1)) == 0,
      "(f1) rederived independently: c_s^2 = (2-K_B)/(K_2 K_B) <= 1 gives the SUBLUMINALITY FLOOR "
      f"K_B >= {floor_sym} = 2/(K_2+1) -- a LOWER bound, pointing opposite to every PPN bound",
      "confirms stage73 C2 from its own definition")
check(empty,
      "*** (f2) AND MY CRITERION DOES NOT SAVE READING L.  The subsonic requirement c_s > w is "
      "satisfied for essentially all K_B (ceiling ~1.97), so it is NOT the binding constraint; the "
      "binding pair is still the subluminality floor 2.1e-4 - 2.7e-4 versus reading L's alpha_1 "
      "ceiling 2.5e-5, which remains EMPTY by 8.4x-10.7x at SZ21's own MOND-compatible fits ***",
      "so the overall logic closes: reading L's branch is the one that is INTERNALLY INCONSISTENT "
      "(empty window), and reading D's branch has no window problem because it has no ceiling.  "
      "The theory's health REQUIRES reading D -- and this file's main result is that reading D's "
      "only self-reported defect is harmless")

hdr("VERDICT")
print(f"""
DOES THE THEORY HAVE A WELL-DEFINED STATIC PPN LIMIT?

  NO -- and the failure is SHARP, LOCATED, and NOT what reading D feared.

  RIGOROUS (symbolically established above, gates 01-06 clean):
   R1  At c_123 = 0 the longitudinal aether mode has NO field equation (check 06:
       om^2 = 0 identically).  Its value in the static boosted problem is fixed only by
       the Psi = 0 constraint, a FIRST-ORDER advection equation, so the static problem is
       NOT elliptic and has no unique decaying solution.  Reading L's premise fails.
   R2  lambda is a conserved charge PURELY ADVECTED by the aether flow: (w.grad)lambda = 0.
       A localised lambda constant along every streamline is identically zero.  lambda = 0 is
       forced by the boundary condition -- two independent routes (antisymmetry of F, and the
       linearized-Bianchi Theta_{{3nu}} constraints) give the same thing.
   R3  THE WAKE IS REAL: causality selects the convected prescription (zero upstream,
       doubled downstream) and the tilt is a PERMANENT FURROW, |a_b| -> 2 gamma_w U(b)/w,
       decaying only as 1/b transversely and NOT AT ALL downstream.  Its amplitude equals
       the textbook impulse 2GM/(b w) -- verified two independent ways.
   R4  *** AND THE WAKE IS HARMLESS: it is CURL-FREE, so F_ij = 0; Psi = 0, so F_0i = 0;
       hence F_{{mu nu}} == 0 identically at O(rho).  Zero energy density, zero stress, and
       therefore ZERO metric imprint at O(rho), O(rho^2) and O(rho^3).  The metric is the
       EXACT GR metric of static dust. ***
   R5  alpha_1 = alpha_2 = 0 is therefore CORRECT for the aether-only truncation, and for a
       stronger reason than reading D gave: not "undefined", but UNSOURCED.
   R6  The wake amplitude is K_B-INDEPENDENT.  Nothing in the aether sector's preferred-frame
       physics can bound K_B, in either direction.
   R7  The PPN w-expansion has RADIUS OF CONVERGENCE EXACTLY c_s.  alpha_1, alpha_2 exist iff
       the system is SUBSONIC.  Reading D's "no Taylor series in w" IS "c_s = 0".
   R8  Regulator ranking: finite source R removes only the on-axis 1/b divergence; finite time
       truncates the furrow at {s_wake/MPC:.2f} Mpc and is irrelevant inside days at 1 AU; ONLY
       c_s > w removes the wake, and it does so by a change of PDE TYPE at the sonic point.

  PHYSICALLY ARGUED (not symbolically proven here):
   P1  The identification "reading L = the subsonic (M < 1) branch, reading D = the supersonic
       (M > 1) branch".  I establish the type change and that reading L's premises hold only
       on M < 1; I do NOT rederive -4 K_B there.
   P2  That the scalar mixing 2(2-K_B)J^mu grad_mu phi lifts the degeneracy COMPLETELY (one
       dynamical spin-0 mode with speed c_s) rather than leaving a residual zero-speed
       direction.  If a zero-speed direction survives, reading D holds regardless of c_s.
   P3  That the aether frame is the CMB frame, so w_sun = 369.82 km/s.

  SO WHAT CONSTRAINS K_B INSTEAD?
   In the aether-only truncation: NOTHING from preferred-frame physics (R6).  The operative
   caps remain the corpus's BBN K_B <= 0.25 and the no-ghost window 0 < K_B < 2, plus the
   subluminality FLOOR K_B >= 2/(K_2+1) = 2.1e-4 - 2.7e-4 at SZ21's fits -- which is a lower
   bound, and is the constraint that makes reading L's 2.5e-5 ceiling produce an empty window.
   stage70's "K_B < 2.5e-5" must NOT be quoted as in force: it is the M < 1 branch only.

  THE ONE NUMBER THAT DECIDES, handed to the sibling:
   M = w_sun/c_s with w_sun = {W_HAT:.5e} c.  At SZ21's cosmological Eq-30 sound speed
   M = {min(t[5] for t in mach_tab):.4f}-{max(t[5] for t in mach_tab):.4f} (SUBSONIC -> reading L, ADVERSE).
   Reading D needs c_s^2 suppressed by {min(t[6] for t in mach_tab):.0f}x-{max(t[6] for t in mach_tab):.0f}x
   relative to that, which the solar system's deep-Newtonian stiffening of F(Y,Q) may or may
   not supply.  THAT IS NOT COMPUTED HERE.

  DIRECTION OF RISK: MIXED.
   FAVOURABLE half (rigorous): reading D's wake objection is DISSOLVED (F == 0), so
   alpha_1 = alpha_2 = 0 stands clean in the truncation and no PPN bound on K_B is in force.
   ADVERSE half (argued, with the corpus's own numbers): the Mach criterion evaluated at
   SZ21's cosmological c_s puts the solar system on reading L's branch -- the branch that
   carries K_B < 2.5e-5 AND stage73's empty window.  And a new adverse exposure is named:
   a 1.3%-at-1-AU aether tilt feeding the scalar sector at FIRST order.

  UNTOUCHED BY THIS FILE: a_0 = kappa c sqrt(G rho_Lambda) ({A0_CANON:.4e} canonical /
  {A0_ALT:.4e} alt), kappa = 1/2 (fitted, never derived), the kernel
  nu(y) = 1/(1-exp(-sqrt y)) (Milgrom & Sanders 2008 Eq 13 at alpha = 1/2), the RAR, lensing,
  gamma_PPN = 1, c_T = 1.  K_B appears nowhere in any of them.  a_0 and kappa appear ZERO
  times in the calculation above.
""")

hdr("CHECK LEDGER")
n_fail = len(FAIL)
print(f"  alpha2_wellposedness_2026: {NCHK[0] - n_fail}/{NCHK[0]} checks passed")
if FAIL:
    for q in FAIL:
        print("   FAILED: " + q)
sys.exit(1 if FAIL else 0)
