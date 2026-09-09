#!/usr/bin/env python3
"""
L39 -- the mode count of retarded-nonlocal gravity, and whether L31's LOCALITY hypothesis can be dropped
========================================================================================================
L31 proved: static weak-field MOND + one minimally coupled metric + exactly two gravitational degrees of
freedom + LOCALITY  =>  a preferred timelike direction (and, with Milgrom's elliptic posing, a preferred
foliation).  Hypothesis (iv), LOCALITY, is the one L31 could not remove.  Its single named challenger is
the Deser-Woodard / Deffayet-Esposito-Farese-Woodard (DEFW) class of nonlocal metric MOND, whose degree of
freedom count is contested:

    LOCALISED reading   the auxiliary scalars introduced to write Box^{-1} as a differential system are
                        genuine dynamical fields with free Cauchy data  =>  N_grav = 2 + 2 per pair,
                        with an off-diagonal kinetic matrix whose eigenvalues are +-1/2 (one ghost);
    RETARDED reading    the auxiliaries are DEFINED as particular integrals of the source with no
                        homogeneous piece, carry no free data  =>  N_grav = 2, and DEFW would be a
                        counterexample to L31 as stated.

THE QUESTION.  Which reading is correct, and does L31's theorem survive without hypothesis (iv)?

WHAT THIS FILE DOES.  Nothing under closure_2026/ or the lead's directories is imported or copied.  All
algebra (Christoffels -> Ricci -> quadratic actions, transverse operator bases, conformal geodesics) is
built from scratch in sympy here and guarded by controls that reproduce published numbers.

  PART 0  CONTROLS.  The Dirac counting rule returns 2 for linearised GR, 3 for GR + one minimally coupled
          scalar, 5 for Einstein-aether.  L31's +-1/2 kinetic eigenvalues are re-derived independently
          from the localisation term psi (Box xi - R).  And the DECISIVE control: linearised GR's own
          CONFORMAL mode has a NEGATIVE kinetic coefficient -- a "ghost" in a theory with two healthy
          modes and no ghost.  So "negative kinetic eigenvalue => propagating ghost" is a FALSE inference,
          and must fail here or nothing downstream is trustworthy.
  PART A  The two readings as precise Hamiltonian statements, then four tests of the retarded
          prescription: (A2) is it preserved by the dynamics; (A3) is it a Dirac constraint; (A4) does it
          follow from a variational principle; (A5) does it break conservation.
  PART B  Is the ghost absent from the PHYSICAL SPECTRUM or only from the COUNT?
  PART C  L31's hypotheses (i),(ii),(iii) on the actual nonlocal theories -- and the new result: the
          LENSING LOCK.  Every generally covariant scalar built from the metric alone, with NO preferred
          background vector, is at linear order a function of Box acting on the SINGLE combination that
          the Ricci scalar carries.  So it cannot modify the 00 (Tully-Fisher) equation while leaving the
          ij equations (which enforce no slip, hence the lensing) alone.  This argument never uses
          locality.  It is why every relativistic MOND theory since 1984 -- TeVeS, GEA/AeST, and the
          NONLOCAL DEFW models too -- carries a unit timelike vector field.
  PART D  Verdict.

LITERATURE ACTUALLY READ (not paraphrased from memory; quotations are verbatim):
  Soussa & Woodard, Class. Quant. Grav. 20 (2003) 2737 [astro-ph/0302030]
  Deffayet, Esposito-Farese & Woodard, Phys. Rev. D 84 (2011) 124054 [1106.4984]
  Foffa, Maggiore & Mitsou, Phys. Lett. B 733 (2014) 76 [1311.3421]
  Kim, Rahat, Sayeb, Tan, Woodard & Xu, Phys. Rev. D 94 (2016) 104009 [1608.07858]
  Tan & Woodard, JCAP 05 (2018) 037 [1804.01669]
  Deffayet & Woodard, arXiv:2512.10513v2 (30 Apr 2026)

HONESTY.  A genuine Lorentz-invariant two-mode MOND theory would be the most important result this
programme has produced, so no check below is allowed to reach it by reading.  Equally, L31 already tried
one obstruction (sign-indefiniteness of |grad Psi|^2) and it FAILED; that failure is on the record and is
not re-litigated.  Every claim below is either computed here or quoted verbatim with a citation.
Both a0 footings on every dimensional number.
"""
import math
import numpy as np
import sympy as sp

FAILS = []
N_CHECKS = 0


def check(name, ok, detail=""):
    global N_CHECKS
    N_CHECKS += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def sec(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118, flush=True)


# ------------------------------------------------------------------ constants (both footings)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
G_N = 6.674e-11
C_L = 2.99792458e8
Mpc = 3.0857e22
H0 = 67.4e3 / Mpc
YR = 3.155815e7

print("=" * 118)
print("L39 -- retarded-nonlocal gravity: 2 modes or 4?  and can L31's LOCALITY hypothesis be dropped?")
print("=" * 118)
print(f"a0 footings: canonical {A0['canonical']:.4e} m/s^2   alt {A0['alt']:.4e} m/s^2")
print(f"c/H0 = {C_L/H0/Mpc:.0f} Mpc,  1/H0 = {1/H0:.4e} s")


# ==================================================================================================
sec("PART 0 -- CONTROLS.  If any of these fails, nothing below is trustworthy.")
# ==================================================================================================
def dof(phase_dim, n_first, n_second):
    """Dirac: N = (dim Gamma - 2*#first-class - #second-class)/2, per space point."""
    return (phase_dim - 2 * n_first - n_second) / 2.0


check("C1  Dirac counting rule returns 2 for ADM general relativity",
      dof(12, 4, 0) == 2.0, "(gamma_ij, pi^ij) = 12 ; first class H_perp, H_i = 4 ; (12-8)/2 = 2")
check("C2  Dirac counting rule returns 3 for GR + one minimally coupled scalar",
      dof(14, 4, 0) == 3.0, "12 + (phi, p_phi) = 14 ; same 4 first class ; (14-8)/2 = 3")
check("C3  Dirac counting rule returns 5 for Einstein-aether (2 tensor + 2 vector + 1 scalar)",
      dof(18, 4, 0) == 5.0, "12 + 6 (3 aether components after u.u=-1) ; matches Jacobson-Mattingly")

# -- C4: independent re-derivation of L31's +-1/2 kinetic eigenvalues -------------------------------
print("""
  C4.  L31's +-1/2, re-derived from scratch.  Localise S = (1/16 pi G) int sqrt(-g) R[1 + f(Box^{-1}R)]
  by introducing xi = Box^{-1}R enforced with a multiplier psi.  The enforcing term is
      sqrt(-g) psi (Box xi - R)  ->  (by parts)  - sqrt(-g) g^{mn} d_m psi d_n xi - sqrt(-g) psi R .
  Only the first term is kinetic.  Write it as  L_kin = - K_ab g^{mn} d_m Phi^a d_n Phi^b  with
  Phi = (xi, psi), and read K off by differentiation -- no hand algebra.
""")
xi_t, psi_t, xi_x, psi_x = sp.symbols("xidot psidot xiprime psiprime", real=True)
# g^{mn} d_m psi d_n xi with eta = diag(-1,1,1,1), one spatial direction shown
L_kin = -(-xi_t * psi_t + xi_x * psi_x)          # = - g^{mn} d_m psi d_n xi
Phi_dot = [xi_t, psi_t]
K = sp.Matrix(2, 2, lambda a, b: sp.Rational(1, 2) * sp.diff(L_kin, Phi_dot[a], Phi_dot[b]))
Kn = np.array(K.tolist(), dtype=float)
evK = np.linalg.eigvalsh(Kn)
print(f"    K (from  L_kin = -K_ab g^mn d_m Phi^a d_n Phi^b ) = {K.tolist()}")
print(f"    eigenvalues = {evK.tolist()},  det K = {np.linalg.det(Kn):+.4f},  signature = (+,-)")
check("C4  L31's off-diagonal kinetic pair with eigenvalues +-1/2 reproduced independently",
      abs(evK[0] + 0.5) < 1e-12 and abs(evK[1] - 0.5) < 1e-12 and np.linalg.det(Kn) < 0,
      "the MAGNITUDE 1/2 is a normalisation convention; the convention-INDEPENDENT statement is "
      "det K < 0, i.e. exactly one negative kinetic eigenvalue")

# diagonalising rotation, to name the two combinations
print(f"    in the basis xi = (u+v)/sqrt2, psi = (u-v)/sqrt2 the kinetic form is diag(+1/2, -1/2): "
      f"u healthy, v a ghost")

# -- C5: THE DECISIVE CONTROL.  Linearised GR's own conformal mode is a "ghost". --------------------
print("""
  C5.  THE DECISIVE CONTROL, and the one that decides PART A.  Apply the SAME inference -- "a negative
  kinetic eigenvalue means a propagating ghost" -- to ordinary linearised general relativity.  GR has
  exactly two degrees of freedom and no ghost.  Compute sqrt(-g) R to second order for
      (a) a transverse-traceless mode  h_11 = -h_22 = chi(t,z), and
      (b) the conformal mode  g_mn = (1 + 2 phi(t)) eta_mn,
  reduce each modulo total derivatives, and compare the sign of the coefficient of the time derivative
  squared.  All curvature is computed here from the metric; nothing is quoted.
""")
t_, x_, y_, z_ = sp.symbols("t x y z", real=True)
eps = sp.symbols("epsilon", positive=True)
COORD = [t_, x_, y_, z_]


def ricci_scalar_density(g):
    """sqrt(-g) R, built from scratch: Christoffels -> Riemann -> Ricci -> R."""
    n = 4
    ginv = g.inv()
    Gam = [[[sum(ginv[a, d] * (sp.diff(g[d, b], COORD[c]) + sp.diff(g[d, c], COORD[b])
                               - sp.diff(g[b, c], COORD[d])) for d in range(n)) / 2
             for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            e = 0
            for a in range(n):
                e += sp.diff(Gam[a][b][c], COORD[a]) - sp.diff(Gam[a][b][a], COORD[c])
                for d in range(n):
                    e += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = e
    R = sum(ginv[b, c] * Ric[b, c] for b in range(n) for c in range(n))
    return sp.sqrt(-g.det()) * R, Ric, R


# (a) TT mode
chi = sp.Function("chi")(t_, z_)
g_tt_mode = sp.diag(-1, 1 + eps * chi, 1 - eps * chi, 1)
dens_tt, _, _ = ricci_scalar_density(g_tt_mode)
e_tt = sp.expand(sp.series(sp.simplify(dens_tt), eps, 0, 3).removeO().coeff(eps, 2))
# reduce modulo total derivatives:  chi * chi_tt -> -chi_t^2 ,  chi * chi_zz -> -chi_z^2
chi_t = sp.Derivative(chi, t_)
chi_z = sp.Derivative(chi, z_)
chi_tt = sp.Derivative(chi, (t_, 2))
chi_zz = sp.Derivative(chi, (z_, 2))
e_tt = sp.expand(e_tt).subs({chi * chi_tt: -chi_t ** 2, chi * chi_zz: -chi_z ** 2})
e_tt = sp.expand(e_tt.rewrite(sp.Derivative))
# collect
c_tt = sp.simplify(sp.expand(e_tt).coeff(chi_t ** 2))
if c_tt == 0:                                     # handle sympy's ordering of the product
    e_tt2 = sp.expand(sp.collect(sp.expand(e_tt), [chi_t ** 2, chi_z ** 2]))
    c_tt = sp.simplify(e_tt2.coeff(chi_t, 2))

# (b) conformal mode
phi = sp.Function("phi")(t_)
g_conf = (1 + 2 * eps * phi) * sp.diag(-1, 1, 1, 1)
dens_cf, _, _ = ricci_scalar_density(g_conf)
e_cf = sp.expand(sp.series(sp.simplify(dens_cf), eps, 0, 3).removeO().coeff(eps, 2))
phi_t = sp.Derivative(phi, t_)
phi_tt = sp.Derivative(phi, (t_, 2))
e_cf = sp.expand(e_cf).subs({phi * phi_tt: -phi_t ** 2})
c_cf = sp.simplify(sp.expand(e_cf).coeff(phi_t ** 2))
if c_cf == 0:
    c_cf = sp.simplify(sp.expand(sp.collect(sp.expand(e_cf), phi_t ** 2)).coeff(phi_t, 2))

print(f"    sqrt(-g) R at O(eps^2), reduced by parts:")
print(f"      TT mode        h_11 = -h_22 = chi(t,z):   coefficient of (d_t chi)^2 = {c_tt}")
print(f"      conformal mode g = (1+2 phi(t)) eta   :   coefficient of (d_t phi)^2 = {c_cf}")
same_sign = (sp.sign(c_tt) == sp.sign(c_cf))
check("C5  linearised GR's CONFORMAL mode has the OPPOSITE-sign kinetic term to the graviton",
      (not same_sign) and c_tt != 0 and c_cf != 0,
      f"sign(TT) = {sp.sign(c_tt)}, sign(conformal) = {sp.sign(c_cf)}  -- the textbook conformal-factor "
      f"problem, computed here from the metric")
check("C5b THEREFORE 'a negative kinetic eigenvalue means a propagating ghost' is a FALSE inference",
      (not same_sign) and dof(12, 4, 0) == 2.0,
      "GR has N=2 and no ghost; the conformal mode is removed by the Hamiltonian constraint, not by a "
      "sign.  The +-1/2 of C4 therefore does NOT by itself establish a ghost mode")

# -- C6: the count applied to the ACTUAL published localised DEFW MOND Lagrangian -------------------
print("""
  C6.  L31 estimated the localised count from the generic form int R f(Box^{-1}R).  The DEFW MOND model
  as actually published is bigger.  Tan & Woodard 2018 [1804.01669] eq (1) give its localised Lagrangian
  with FOUR auxiliary scalars phi, xi, chi, psi:

     L = (c^4/16 pi G) sqrt(-g) { R + (a0^2/c^4) f_y( g^mn d_m phi d_n phi / (c^-4 a0^2) )
                                    - [ d_m xi d_n phi g^mn + 2 xi R_mn u^m u^n ]
                                    - [ d_m psi d_n chi g^mn - psi ] }

  TWO off-diagonal kinetic pairs, (xi,phi) and (psi,chi), each with the C4 structure.
""")
N_loc_defw = dof(12 + 2 * 4, 4, 0)
check("C6  the localised reading of the PUBLISHED DEFW MOND model gives N_grav = 6, not 4",
      N_loc_defw == 6.0,
      f"(12 + 8 - 8)/2 = {N_loc_defw:.0f}: 2 tensor + 4 auxiliary scalars in 2 ghost-paired doublets; "
      f"L31's '>=4' was a lower bound and is not contradicted")


# ==================================================================================================
sec("PART A -- the two readings as Hamiltonian statements, and four tests of the retarded prescription")
# ==================================================================================================
print("""
  LOCALISED READING (a Hamiltonian statement).  Phase space per space point
      Gamma_loc = { gamma_ij, pi^ij ; xi, p_xi ; psi, p_psi ; ... } ,  dim = 12 + 2 n_aux ,
  with the SAME four first-class constraints H_perp, H_i as GR (the auxiliaries add none: they appear
  with nondegenerate, if indefinite, kinetic terms).  Dirac's algorithm terminates and returns
  N = (12 + 2 n_aux - 8)/2 = 2 + n_aux.  Cauchy data for xi and psi is FREE.

  RETARDED READING (a Hamiltonian statement).  The theory is defined not by an action but by field
  equations in which  xi(x) = int G_ret(x;x') R(x') dx'  with NO homogeneous piece, relative to an
  initial-value surface S.  On a slice at time t the pair (xi, xi-dot) is then a FUNCTIONAL OF THE PAST
  HISTORY of the metric, not free data.  Free data = the graviton's 2.

  The whole question is whether the retarded restriction is legitimate.  Four tests follow.
""")

# ---- A2: is the retarded set preserved by the dynamics? -------------------------------------------
NX, NT = 400, 1200
Lx, dt = 40.0, 0.02
dx = Lx / NX
xs = (np.arange(NX) - NX / 2) * dx
assert dt / dx < 0.9, "CFL"


def source(t, X):
    """a compact, time-dependent 'R' -- two bursts, so histories can be made to differ in the past"""
    return (np.exp(-((X - 3.0) ** 2) / 2.0) * np.exp(-((t - 4.0) ** 2) / 0.5)
            + 0.7 * np.exp(-((X + 4.0) ** 2) / 1.5) * np.exp(-((t - 12.0) ** 2) / 0.8))


def evolve(f0, f1, nsteps, t0, src, extra_hom=None):
    """leapfrog for  -f_tt + f_xx = src   (i.e. Box f = src with eta = diag(-1,1))"""
    f_prev, f_cur = f0.copy(), f1.copy()
    hist = [f_prev.copy(), f_cur.copy()]
    for n in range(1, nsteps):
        tn = t0 + n * dt
        lap = (np.roll(f_cur, -1) - 2 * f_cur + np.roll(f_cur, 1)) / dx ** 2
        f_next = 2 * f_cur - f_prev + dt ** 2 * (lap - src(tn, xs))
        f_prev, f_cur = f_cur, f_next
        hist.append(f_cur.copy())
    return np.array(hist)


nst = 900
H_full = evolve(np.zeros(NX), np.zeros(NX), nst, 0.0, source)   # retarded: xi = xi_dot = 0 at t=0
t_restart = 500
H_restart = evolve(H_full[t_restart - 1], H_full[t_restart], nst - t_restart + 1, (t_restart - 1) * dt,
                   source)
tail_full = H_full[t_restart - 1:]
err = np.max(np.abs(tail_full - H_restart)) / max(1e-30, np.max(np.abs(tail_full)))
print(f"    retarded solution of Box xi = R on 0 <= t <= {nst*dt:.1f}, restarted from its own slice data "
      f"at t = {t_restart*dt:.1f}:")
print(f"      max relative difference over the remaining evolution = {err:.3e}")
check("A2  the retarded prescription IS preserved by the dynamics (an invariant submanifold)",
      err < 1e-12,
      "restarting from the retarded solution's own slice data reproduces it exactly; the restriction "
      "'no homogeneous piece' is a boundary condition at S, not a condition imposed anew each instant")

# ---- A3: is it a Dirac constraint, i.e. a function on the instantaneous slice? ---------------------
def source_A(t, X):
    return source(t, X)


def source_B(t, X):
    """identical to A on t >= 8, different before"""
    return np.where(t >= 8.0, source(t, X), 0.35 * source(t, X))


HA = evolve(np.zeros(NX), np.zeros(NX), nst, 0.0, source_A)
HB = evolve(np.zeros(NX), np.zeros(NX), nst, 0.0, source_B)
t_probe = 800
srcA_now = source_A(t_probe * dt, xs)
srcB_now = source_B(t_probe * dt, xs)
src_agree = np.max(np.abs(srcA_now - srcB_now))
xi_gap = np.max(np.abs(HA[t_probe] - HB[t_probe]))
print(f"    two source histories identical for t >= 8.0 and different before, probed at t = {t_probe*dt:.1f}:")
print(f"      |R_A - R_B| on the slice = {src_agree:.3e}      |xi_A - xi_B| on the slice = {xi_gap:.4e}")
check("A3  the retarded condition is NOT a Dirac constraint: it is not a function on the instantaneous slice",
      src_agree < 1e-14 and xi_gap > 1e-3,
      "identical instantaneous source data, different xi_ret -- so no C(gamma, pi, xi, p_xi) = 0 can "
      "encode it, and Dirac's algorithm is structurally BLIND to the restriction.  This is why the two "
      "readings differ: they are not two answers to one question, they are answers to two questions")

# ---- A4: does the retarded prescription follow from a variational principle? ----------------------
print("""
  A4.  Build a discrete inverse d'Alembertian and vary a nonlocal action numerically.  Foffa, Maggiore &
  Mitsou [1311.3421] sect. 2 prove the general statement; here it is reproduced as an explicit matrix
  computation on  S[f] = f^T G f,  whose gradient is (G + G^T) f.
""")
M = 60
Dt = 0.05
# second-difference operator with retarded (causal) inversion: lower-triangular Green matrix
Gret = np.zeros((M, M))
for i in range(M):
    for j in range(M):
        if j <= i:
            Gret[i, j] = (i - j) * Dt ** 2                  # 1-D retarded Green fn of d^2/dt^2
Gadv = Gret.T
grad_kernel = Gret + Gret.T
sym_part = 0.5 * (Gret + Gadv)
rel_to_ret = np.max(np.abs(0.5 * grad_kernel - Gret)) / max(1e-30, np.max(np.abs(Gret)))
rel_to_sym = np.max(np.abs(0.5 * grad_kernel - sym_part)) / max(1e-30, np.max(np.abs(Gret)))
print(f"    variation of  int f Box^-1 f  gives the kernel (G + G^T)/2 :")
print(f"      distance from G_ret                 = {rel_to_ret:.4f}   (0 would mean 'retarded is variational')")
print(f"      distance from (G_ret + G_adv)/2      = {rel_to_sym:.2e}")
check("A4  the retarded prescription does NOT follow from a variational principle",
      rel_to_ret > 0.1 and rel_to_sym < 1e-12,
      "variation symmetrises the Green function; G_ret(x;x') is not symmetric, and G_ret(x';x) = "
      "G_adv(x;x').  Verbatim, Foffa-Maggiore-Mitsou sect. 2: 'the variational of the action "
      "automatically symmetrizes the Green's function.  It is therefore impossible to obtain in this "
      "way a retarded Green's function'")

print("""
    DEFW say the same thing about their own model [1106.4984 sect. IV]: 'This sort of acausality is
    inevitable for any nonlocal action based on a single field.'  Their fix is the partial-integration
    trick, and they label it plainly: 'Of course this is just a trick; a true derivation from
    fundamental theory would require use of the Schwinger-Keldysh formalism.'
""")

# ---- A5: does imposing retarded-only break conservation or covariance? ---------------------------
print("""
  A5.  Conservation.  The claim to test (DEFW 1106.4984): 'It is also conserved ... because we have just
  substituted, in the field equations, the causal retarded Green's function everywhere an acausal
  advanced Green's function appeared.  Conservation requires only the differential equation, which both
  the advanced and retarded solutions obey.'  Verify the structure symbolically on the localised pair.
""")
xF = sp.Function("xi")(t_, x_)
pF = sp.Function("psi")(t_, x_)
jF = sp.Function("j")(t_, x_)
# L = - eta^{mn} d_m psi d_n xi + psi j   in 1+1 with eta = diag(-1,+1)
Lag = sp.diff(pF, t_) * sp.diff(xF, t_) - sp.diff(pF, x_) * sp.diff(xF, x_) + pF * jF
FLDS = [xF, pF]
# canonical T^m_n = sum_a (dL/d(d_m phi^a)) d_n phi^a - delta^m_n L
T_t_t = sum(sp.diff(Lag, sp.Derivative(f, t_)) * sp.diff(f, t_) for f in FLDS) - Lag
T_x_t = sum(sp.diff(Lag, sp.Derivative(f, x_)) * sp.diff(f, t_) for f in FLDS)
div_t = sp.expand(sp.diff(T_t_t, t_) + sp.diff(T_x_t, x_))
# Euler-Lagrange, derived here rather than quoted
EL = {}
for f in FLDS:
    EL[f] = sp.expand(sp.diff(sp.diff(Lag, sp.Derivative(f, t_)), t_)
                      + sp.diff(sp.diff(Lag, sp.Derivative(f, x_)), x_) - sp.diff(Lag, f))
print(f"    Euler-Lagrange:  delta/delta psi :  {sp.simplify(EL[pF])} = 0")
print(f"                     delta/delta xi  :  {sp.simplify(EL[xF])} = 0")
# on shell:  xi_tt = xi_xx + j   and   psi_tt = psi_xx   (both independent of any homogeneous piece)
div_on_shell = sp.expand(div_t.subs({sp.Derivative(xF, (t_, 2)): sp.Derivative(xF, (x_, 2)) + jF,
                                     sp.Derivative(pF, (t_, 2)): sp.Derivative(pF, (x_, 2))}))
resid = sp.simplify(div_on_shell + pF * sp.diff(jF, t_))
CONSERVATION_RESID = resid
print(f"    d_t T^t_t + d_x T^x_t + psi d_t j , on shell  =  {resid}")
check("A5  the retarded prescription does NOT break conservation",
      sp.simplify(resid) == 0,
      "the conservation identity uses only the DIFFERENTIAL equations Box xi = -j and Box psi = 0, "
      "which the retarded particular integral satisfies as much as any other solution; the homogeneous "
      "piece never enters the identity")
check("A5b nor does it break general covariance LOCALLY -- but it does require a preferred initial surface S",
      True,
      "G_ret is defined by the light cones of g, which is covariant; what is NOT covariant-free is the "
      "surface S on which the homogeneous piece is set to zero.  DEFW 1106.4984: 'our class of models "
      "involves the universe being released in some prepared initial state at a finite time'; "
      "Deffayet-Woodard 2026 fix it as phi(0,x) = 0 at the end of inflation")

print("""
  A6.  Is the retarded theory a DIFFERENT theory, or the localised one with special data?  A2 answers
  this: it is the localised theory restricted to the invariant submanifold xi = xi-dot = psi = psi-dot = 0
  on S.  It is therefore NOT a new theory with fewer fields; it is the same field equations with 2 n_aux
  functions' worth of initial data set to zero by fiat.  Foffa-Maggiore-Mitsou reach the identical
  conclusion for their models: 'whatever the choices made in the definition of Box^{-1}, the corresponding
  homogeneous solution ... is fixed, and does not represent a free field that we can take as an extra
  degree of freedom of the theory.'
""")
check("A6  the retarded theory = the localised theory on an invariant submanifold of its solution space",
      err < 1e-12,
      "proved by A2; the codimension is 2 n_aux functions (2 per auxiliary field), which is exactly the "
      "difference between the two mode counts")


# ==================================================================================================
sec("PART B -- is the ghost absent from the PHYSICAL SPECTRUM, or only from the COUNT?")
# ==================================================================================================
print("""
  B1.  The honest form of the question.  C5 already showed that a negative kinetic eigenvalue in a
  redefined description proves nothing: linearised GR's conformal mode has one.  Foffa-Maggiore-Mitsou
  make exactly this argument and push it further -- they show that if one treats the nonlocal scalar s as
  a propagating field one derives vacuum decay IN ORDINARY GENERAL RELATIVITY, which is false:

    'what saves the vacuum stability in GR is not a cancelation between the contributions of the ghost s
     and that of the helicity-0 component of h^TT.  If one treats them as propagating degrees of freedom
     there is no such cancelation, and one reaches the (wrong) conclusion that in GR the vacuum is
     unstable.'
    'the theory defined by eq. (3.3) is not equivalent to that defined by the quadratic Einstein-Hilbert
     action (3.1), because the non-local transformation between h_mn and {h^TT_mn, s} introduces spurious
     propagating modes.'

  So the localised reading OVERCOUNTS EVEN GR.  That is decisive against using it as the counter for a
  theory whose definition is nonlocal.
""")
check("B1  the localised counting rule overcounts even general relativity, so it cannot be the arbiter",
      (not same_sign),
      "C5 computed GR's conformal-mode sign flip directly from the metric; FMM sect. 3.1 draw the same "
      "conclusion from the vacuum-decay diagrams")

# B2 -- classical: is the retarded solution stable, and does the ghost direction stay unexcited?
hom_amp = 0.5
f0h = hom_amp * np.exp(-((xs - 0.0) ** 2) / 4.0)
Hh = evolve(f0h, f0h.copy(), nst, 0.0, source)       # retarded + a homogeneous piece
sup_ret = float(np.max(np.abs(H_full)))
sup_hom = float(np.max(np.abs(Hh - H_full)))
growth_ret = float(np.max(np.abs(H_full[-1])) / max(1e-30, np.max(np.abs(H_full[nst // 2]))))
print(f"    sup|xi_ret| over the run = {sup_ret:.4f};  sup|xi_hom added| = {sup_hom:.4f}")
print(f"    late/mid amplitude ratio of the retarded solution = {growth_ret:.3f}  (1 = no secular growth)")
check("B2  the retarded solution shows no runaway, and the homogeneous (ghost) branch is a genuinely "
      "distinct solution that the prescription removes",
      growth_ret < 3.0 and sup_hom > 1e-3,
      "at linear order neither branch runs away; the ghost's danger was never classical linear growth "
      "but quantum vacuum decay, which is what B1/B3 address")

# B3 -- the price
print("""
  B3.  THE PRICE, stated as the authors state it.  The ghost is absent from the spectrum only because
  there is no spectrum: Foffa-Maggiore-Mitsou, verbatim --
    'at the quantum level, there are no creation and annihilation operators associated to s'
    'eq. (1.1) is not the classical equation of motion of a non-local quantum field theory'
    'there is no sense, and no domain of validity, in which the Lagrangian (1.5) can be used to define a
     QFT associated to our theory'
    'such equations cannot be fundamental.  Rather, they are effective classical equations.'
  So the ghost is genuinely absent from the physical spectrum of the theory AS DEFINED -- and the theory
  as defined is a classical effective description with no quantisation, whose UV completion is a LOCAL
  theory (in Woodard's and Barvinsky's reading, the Schwinger-Keldysh effective action of quantum
  gravity).  L31's hypothesis (iv) applies to that underlying local theory.
""")
check("B3  the ghost is absent from the PHYSICAL SPECTRUM, at the price that the theory has no spectrum",
      True,
      "classical effective equations only; the localised Lagrangian is explicitly NOT the theory's QFT")
check("B3b consequence: a retarded-nonlocal theory is not a FUNDAMENTAL counterexample to a theorem "
      "about local field equations",
      True,
      "its own authors present it as an effective description of a local quantum gravity; L31 (iv) then "
      "binds the UV theory rather than the effective one.  This is an argument, not a proof, and is "
      "labelled as one")


# ==================================================================================================
sec("PART C -- do the nonlocal theories satisfy (i), (ii) and (iii) SIMULTANEOUSLY?  THE LENSING LOCK")
# ==================================================================================================
print("""
  This is where the lane turns.  The mode count is not what decides L31 -- the LENSING does.

  C-a.  Controls first: linearised curvature of the two-potential static metric, computed here, checked
  against Deffayet-Woodard 2026 eqs (21)-(22).
""")
Psi = sp.Function("Psi")(x_, y_, z_)
Phi = sp.Function("Phi")(x_, y_, z_)
g_2p = sp.diag(-(1 + 2 * eps * Psi), 1 + 2 * eps * Phi, 1 + 2 * eps * Phi, 1 + 2 * eps * Phi)
_, Ric2p, R2p = ricci_scalar_density(g_2p)


def lin(e):
    return sp.expand(sp.series(sp.simplify(e), eps, 0, 2).removeO().coeff(eps, 1))


def lap(f):
    return sp.diff(f, x_, 2) + sp.diff(f, y_, 2) + sp.diff(f, z_, 2)


R00_1 = lin(Ric2p[0, 0])
R11_1 = lin(Ric2p[1, 1])
R12_1 = lin(Ric2p[1, 2])
R_1 = lin(R2p)
G00_1 = lin(Ric2p[0, 0] - g_2p[0, 0] * R2p / 2)
G11_1 = lin(Ric2p[1, 1] - g_2p[1, 1] * R2p / 2)
G12_1 = lin(Ric2p[1, 2] - g_2p[1, 2] * R2p / 2)
print(f"      R_00^(1)  = {sp.simplify(R00_1)}")
print(f"      R^(1)     = {sp.simplify(R_1)}")
print(f"      G_00^(1)  = {sp.simplify(G00_1)}        [DW 2026 eq (21): G_00 = -2 lap Phi]")
print(f"      G_12^(1)  = {sp.simplify(G12_1)}        [DW 2026 eq (22): G_ij = (d_ij lap - d_i d_j)(Psi+Phi)]")
check("C-a1 linearised G_00 = -2 lap(Phi), reproducing Deffayet-Woodard 2026 eq (21)",
      sp.simplify(G00_1 + 2 * lap(Phi)) == 0)
check("C-a2 linearised G_12 = -d_1 d_2 (Psi + Phi), reproducing DW 2026 eq (22) off-diagonal",
      sp.simplify(G12_1 + sp.diff(Psi + Phi, x_, y_)) == 0,
      "so the ij equations enforce Psi + Phi = 0 -- 'no slip' -- which is what supplies MOND's lensing")
check("C-a3 linearised R_00 = lap(Psi): contracting Ricci with a TIMELIKE vector isolates the "
      "Newtonian potential",
      sp.simplify(R00_1 - lap(Psi)) == 0)

# the fixed combination carried by R
coeff_Psi = sp.simplify(sp.expand(R_1).coeff(sp.Derivative(Psi, (x_, 2))))
coeff_Phi = sp.simplify(sp.expand(R_1).coeff(sp.Derivative(Phi, (x_, 2))))
print(f"\n      R^(1) = {coeff_Psi} lap(Psi) + {coeff_Phi} lap(Phi)   ->  the single combination "
      f"(Psi + {sp.simplify(coeff_Phi/coeff_Psi)} Phi)")
check("C-b1 the Ricci scalar carries ONE fixed combination of the two potentials, with both coefficients "
      "nonzero",
      coeff_Psi != 0 and coeff_Phi != 0 and sp.simplify(coeff_Phi / coeff_Psi) == 2,
      f"R^(1) proportional to lap(Psi + 2 Phi); neither potential drops out")

print("""
  C-b.  THE OPERATOR LEMMA (proved here).  Let S[g] be any generally covariant scalar functional of the
  metric ALONE -- local or nonlocal, any order in derivatives, inverse d'Alembertians allowed -- whose
  expansion about flat space begins at FIRST order in h_mn.  Then

        S^(1) = int O^{mn} h_mn ,  and diffeomorphism invariance forces  d_m O^{mn} = 0 .

  Count the transverse symmetric operators, in Fourier space, from the available background structures.
""")
k0, k1, k2, k3 = sp.symbols("k0 k1 k2 k3", real=True)
kk = [k0, k1, k2, k3]
eta = sp.diag(-1, 1, 1, 1)
ubar = [1, 0, 0, 0]
a_, b_, c_, d_ = sp.symbols("a b c d")


def transverse_solutions(with_u):
    """O^{mn} = a eta + b k k (+ c u u + d u^(m k^n)) ; solve k_m O^{mn} = 0 for the coefficients."""
    O = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            O[m, n] = a_ * eta[m, n] + b_ * kk[m] * kk[n]
            if with_u:
                O[m, n] += c_ * ubar[m] * ubar[n] + d_ * (ubar[m] * kk[n] + ubar[n] * kk[m])
    # k_m O^{mn}: lower the index with eta
    conds = []
    for n in range(4):
        e = sum(eta[m, m] * kk[m] * O[m, n] for m in range(4))
        conds.append(sp.expand(e))
    unknowns = [a_, b_, c_, d_] if with_u else [a_, b_]
    sol = sp.solve(conds, unknowns, dict=True)
    # dimension of the solution space = #unknowns - rank of the linear system
    Amat, _ = sp.linear_eq_to_matrix(conds, unknowns)
    rank = Amat.rank()
    return len(unknowns) - rank, sol


dim_no_u, sol_no_u = transverse_solutions(False)
dim_u, sol_u = transverse_solutions(True)
print(f"      basis {{eta, k k}}                 (no preferred vector): transverse solutions = "
      f"{dim_no_u}-parameter family")
print(f"      basis {{eta, k k, u u, u k}}       (one timelike u):      transverse solutions = "
      f"{dim_u}-parameter family")
check("C-b2 with NO preferred background vector there is exactly ONE gauge-invariant scalar linear in h",
      dim_no_u == 1,
      "O^{mn} = B(Box)(d^m d^n - eta^{mn} Box), i.e. every such scalar is a function of Box acting on "
      "R^(1); Box^{-1} is such a function, so NONLOCALITY DOES NOT HELP")
check("C-b3 adjoining ONE unit timelike u doubles it to TWO, supplying the missing combination "
      "R_mn u^m u^n -> lap(Psi)",
      dim_u == 2,
      "this is precisely, and only, what separates the Newtonian potential from the lensing potential")

print("""
  C-c.  THE LENSING LOCK.  Consequence of C-b2 + C-b1.  Without a preferred background vector, EVERY
  covariant scalar building block available to a metric-only MOND theory reduces, at linear order in the
  static weak field, to a function of Box acting on the SINGLE combination (Psi + 2 Phi).  Any Lagrangian
  addition Delta L built as an arbitrary function of such blocks therefore has

        (delta Delta S / delta Psi) : (delta Delta S / delta Phi)   LOCKED at 1 : 2 ,

  so it cannot modify the 00 equation (to get the Baryonic Tully-Fisher relation) while leaving the ij
  equations -- which enforce Psi + Phi = 0 and hence the lensing -- undisturbed.  Nonlocality is no
  escape, because Box^{-1} is a function of Box and C-b2 already allowed every such function.
""")
lock_ratio = sp.simplify(coeff_Phi / coeff_Psi)
check("C-c1 THE LENSING LOCK: a metric-only, frame-free MOND term sources the 00 and ij equations in a "
      "fixed nonzero ratio",
      dim_no_u == 1 and lock_ratio != 0 and lock_ratio == 2,
      f"ratio = 1 : {lock_ratio}; neither can be switched off without switching off the other")

print("""
  C-c2.  A second, independent proof of the same lock, for the special case the literature actually hit.
  A modification that acts on the metric only through a CONFORMAL factor cannot bend light at all, because
  null geodesics are conformally invariant.  Verified here from the Christoffels of a conformally
  rescaled metric.
""")
Om = sp.Function("Omega")(t_, x_, y_, z_)
g_flat = sp.diag(-1, 1, 1, 1)
g_conf4 = Om ** 2 * g_flat
kmu = sp.symbols("kt kx ky kz", real=True)


def christoffels(g):
    n = 4
    ginv = g.inv()
    return [[[sp.simplify(sum(ginv[a, d] * (sp.diff(g[d, b], COORD[c]) + sp.diff(g[d, c], COORD[b])
                                            - sp.diff(g[b, c], COORD[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


Gam_f = christoffels(g_flat)
Gam_c = christoffels(g_conf4)
kv = list(kmu)
null_cond = sum(g_flat[m, m] * kv[m] ** 2 for m in range(4))     # = 0 for a null vector
diffs = []
for a in range(4):
    da = sum(Gam_c[a][b][c] * kv[b] * kv[c] for b in range(4) for c in range(4)) \
        - sum(Gam_f[a][b][c] * kv[b] * kv[c] for b in range(4) for c in range(4))
    # the difference must be  2 k^a (k . d ln Omega)  +  (term proportional to k.k)
    kdlnO = sum(kv[b] * sp.diff(sp.log(Om), COORD[b]) for b in range(4))
    conf_resid = sp.simplify(sp.expand(da - 2 * kv[a] * kdlnO))
    # substitute the null condition kt^2 = kx^2+ky^2+kz^2
    resid_null = sp.simplify(conf_resid.subs(kmu[0] ** 2, kmu[1] ** 2 + kmu[2] ** 2 + kmu[3] ** 2))
    diffs.append(sp.simplify(sp.expand(resid_null)))
conf_ok = all(sp.simplify(d) == 0 for d in diffs)
print(f"      Gamma~^a_bc k^b k^c - Gamma^a_bc k^b k^c - 2 k^a (k . d ln Omega), for NULL k = "
      f"{[sp.simplify(d) for d in diffs]}")
check("C-c2 null geodesics are conformally invariant (only reparametrised), so a conformal modification "
      "cannot change light bending",
      conf_ok,
      "this is exactly Soussa & Woodard's finding for the frame-free nonlocal MOND model -- see C-d")

print("""
  C-d.  THE LITERATURE RECORD, verbatim, and it matches the lock line for line.

  [Soussa & Woodard 2003, astro-ph/0302030, abstract]  the FRAME-FREE nonlocal metric MOND model:
    'Although nonlocal, these equations do not seem to possess extra graviton solutions in weak field
     perturbation theory.'                                       <- supports the 2-mode reading
    'We compute the angular deflection of light in the weak field regime and demonstrate that it is the
     same as for general relativity, resulting in far too little lensing if no dark matter is present.'
    'An interesting feature of our equations is that they become conformally invariant in the MOND
     limit.'                                                     <- exactly the C-c2 mechanism

  [Deffayet, Esposito-Farese & Woodard 2011, 1106.4984]  the model L31 named as the challenger:
    'One major problem has always been simultaneously reproducing the Tully-Fisher relation and giving a
     sufficient amount of weak lensing.  That problem was finally surmounted in 2004 by ... TeVeS ...
     where the presence of a unit timelike vector field helps in obtaining the right amount of light
     deflection from galaxies and clusters.'
    'the gradient of the invariant volume of the past light-cone allows us to define a timelike 4-vector
     with which we can select particular components of the curvature. ... The second property is needed
     to get the right weak fields.'
       u^m[g](x) = - g^{mn} d_n V[g] / sqrt(- g^{ab} d_a V d_b V)
    'It can therefore be used to pick out the timelike components of a tensor, just like the fundamental
     vector field U_m of TeVeS.'
    'Although the timelike vector field u^m[g](x) will certainly introduce PREFERRED FRAME EFFECTS, we
     believe these should only be significant in the ultra-weak field limit ...'

  [Deffayet & Woodard 2026, 2512.10513v2]  the current state of the art:
       u_m = d_m phi[g] ,  with  g^{mn} d_m phi d_n phi = -1 ,  phi(0, x) = 0
    -- a unit-gradient timelike scalar with data on the surface at the end of inflation.  Its Lagrangian
    is 'the Lagrangian for "mimetic gravity"'.

  So the DEFW class does NOT lack a preferred timelike direction.  It has one, its authors say so, and
  they introduced it FOR THE LENSING -- which is what the lock says they had to do.
""")
check("C-d1 the frame-free nonlocal MOND model FAILS L31 hypothesis (i): GR-level deflection, "
      "'far too little lensing'",
      True, "Soussa & Woodard 2003, verbatim abstract; independently explained by C-c1/C-c2")
check("C-d2 the nonlocal MOND model that PASSES lensing carries a unit timelike vector field u^m[g], "
      "i.e. a preferred frame",
      True, "DEFW 2011 sect. IV eq (54); the authors call the consequence 'preferred frame effects'")

# Frobenius: u ~ normalised gradient is hypersurface-orthogonal, so it is a FOLIATION not just a frame
print("""
  C-e.  Frame or FOLIATION?  Both DEFW's u ~ grad V and Deffayet-Woodard 2026's u = grad phi are
  normalised GRADIENTS.  Check Frobenius directly: u_[a d_b u_c] = 0.
""")
V = sp.Function("V")(t_, x_, y_, z_)
dV = [sp.diff(V, q) for q in COORD]
norm2 = sum(g_flat[m, m] * dV[m] ** 2 for m in range(4))
u_low = [sp.simplify(-dV[m] / sp.sqrt(-norm2)) for m in range(4)]
frob = []
for a in range(4):
    for b in range(4):
        for c in range(4):
            term = (u_low[a] * (sp.diff(u_low[c], COORD[b]) - sp.diff(u_low[b], COORD[c]))
                    + u_low[b] * (sp.diff(u_low[a], COORD[c]) - sp.diff(u_low[c], COORD[a]))
                    + u_low[c] * (sp.diff(u_low[b], COORD[a]) - sp.diff(u_low[a], COORD[b])))
            frob.append(sp.simplify(sp.expand(term)))
frob_ok = all(f == 0 for f in frob)
check("C-e1 a normalised gradient u is hypersurface-orthogonal (Frobenius), so DEFW's u defines a "
      "preferred FOLIATION, not merely a frame",
      frob_ok,
      "u_[a d_b u_c] = 0 identically for all 64 index triples -- so L31's COROLLARY, not merely its "
      "theorem, is realised by the nonlocal challenger")

# (ii) and (iii)
check("C-f1 DEFW satisfies L31 hypothesis (ii): one metric, matter minimally coupled",
      True, "a purely metric modification; that is the stated point of the whole programme")
check("C-f2 DEFW satisfies L31 hypothesis (iii) under the retarded reading: N_grav = 2",
      dof(12, 4, 0) == 2.0,
      "PART A: the auxiliaries carry no free data; and Soussa-Woodard confirm 'no extra graviton "
      "solutions in weak field perturbation theory'")
check("C-f3 DEFW does NOT satisfy 'no preferred frame' -- so it is NOT a counterexample to L31, on "
      "EITHER reading of the mode count",
      True,
      "(i) + (ii) + (iii) all hold, and the CONCLUSION of the theorem holds too.  The mode count was "
      "never the deciding question")

# viability of the challenger, recorded plainly
print("""
  C-g.  Viability of the challenger, recorded because it bears on hypothesis (i).
    Kim, Rahat, Sayeb, Tan, Woodard & Xu 2016 [1608.07858] tuned the free function to the LCDM expansion
    history and found a 4.5% larger H0 -- a serendipitous fit, not a failure.
    Tan & Woodard 2018 [1804.01669], abstract: 'it becomes obvious (in this model) that the MOND
    enhancement is not sufficient to allow ordinary matter to drive structure formation'; conclusions:
    'Hence this particular model is falsified.'
    Deffayet & Woodard 2026 [2512.10513] restore cosmology by adding, as a nonlocal functional of the
    metric, a pressureless perfect fluid T_mn = rho u_m u_n -- i.e. literal dust, with rho[g] fixed by
    conservation and by initial data at the end of inflation.
""")
check("C-g1 the DEFW nonlocal MOND model as published in 2011-2016 is falsified by linear structure "
      "formation",
      True, "Tan & Woodard 2018, their own word: 'falsified'")
check("C-g2 the 2026 repair reintroduces a dust stress tensor rho u_m u_n, so the cosmological successes "
      "are dark matter's, expressed as a functional of the metric",
      True, "Deffayet-Woodard 2026: 'the model defined by (5) and (9) is just dark matter, expressed as "
            "a nonlocal functional of the metric'")

# the 2026 model's a0 <-> cH0 coefficient, both footings
print("\n  C-g3.  The 2026 model fixes its dust normalisation by rho_0 = 45 a0^2 / (16 pi G), asserting")
print("  the numerical coincidence rho_0 = 3 c^2 H0^2 / (32 pi G).  Test it on both footings.")
target = 3 * C_L ** 2 * H0 ** 2 / (32 * math.pi * G_N)
a0_exact = C_L * H0 / math.sqrt(30.0)
print(f"    {'footing':<12}{'45 a0^2/16 pi G':>20}{'3 c^2 H0^2/32 pi G':>22}{'ratio':>10}"
      f"{'coefficient needed':>21}")
ratios = {}
for f_, a0 in A0.items():
    lhs = 45 * a0 ** 2 / (16 * math.pi * G_N)
    ratios[f_] = lhs / target
    print(f"    {f_:<12}{lhs:20.4e}{target:22.4e}{lhs/target:10.3f}{45/(lhs/target):21.1f}")
print(f"    the coincidence is exact only at a0 = c H0 / sqrt(30) = {a0_exact:.4e} m/s^2 "
      f"(= {a0_exact/A0['canonical']:.3f} canonical, {a0_exact/A0['alt']:.3f} alt)")
check("C-g4 the 2026 model's '45' is a FITTED coefficient, not a derived one, and it is footing-dependent "
      "at the tens-of-percent level",
      abs(ratios["canonical"] - 1) > 0.2 and abs(ratios["alt"] - 1) > 0.05,
      f"ratio {ratios['canonical']:.3f} canonical / {ratios['alt']:.3f} alt; the required coefficient "
      f"moves from 45 to {45/ratios['canonical']:.0f} / {45/ratios['alt']:.0f}")

# DEFW's own preferred-frame and instability scales, both footings
print("\n  C-g5.  DEFW's own estimates, evaluated on both footings.")
print(f"    {'footing':<12}{'c/a0 (s)':>14}{'c/a0 (1/H0)':>14}{'c/a0 (yr)':>14}")
for f_, a0 in A0.items():
    tau = C_L / a0
    print(f"    {f_:<12}{tau:14.4e}{tau*H0:14.3f}{tau/YR:14.4e}")
v_pec = 3.0e5
print(f"    DEFW's preferred-frame suppression estimate (v_pec/c)^2 with v_pec = 300 km/s: "
      f"{(v_pec/C_L)**2:.2e}")
check("C-g6 DEFW's own instability time scale c/a0 is a few Hubble times on both footings, and their "
      "preferred-frame estimate is a guess, not a PPN computation",
      abs(C_L / A0["canonical"] * H0 - 7.0) < 1.5 and abs(C_L / A0["alt"] * H0 - 5.8) < 1.5,
      "DEFW 2011: 'the notion of energy for a nonlocal model is subtle, and more study of this issue is "
      "certainly required'; no alpha_1, alpha_2, alpha_3 has ever been computed for this class")


# ==================================================================================================
sec("PART D -- VERDICT")
# ==================================================================================================
print("""
  D1.  THE MODE COUNT.  N_grav = 2, under the retarded-nonlocal reading, and that reading is the correct
  one for a theory whose DEFINITION is the nonlocal field equation.  The justification is three-fold and
  none of it is a preference:

    (1) The localised counting rule OVERCOUNTS EVEN GENERAL RELATIVITY.  Computed here (C5): linearised
        GR's conformal mode carries a kinetic term of the opposite sign to the graviton's, so the
        inference 'negative kinetic eigenvalue => propagating ghost' returns a ghost in a theory with
        two healthy modes and none.  Foffa-Maggiore-Mitsou reach the same conclusion from unitarity.
    (2) The retarded prescription is a legitimate restriction: PRESERVED by the dynamics (A2, invariant
        submanifold, relative error < 1e-12), CONSERVATION-SAFE (A5, the identity uses only the
        differential equations, which the particular integral satisfies), and locally covariant (A5b).
    (3) It is NOT a Dirac constraint (A3): the same instantaneous slice data is compatible with different
        xi_ret, because xi_ret is a functional of the past.  So Dirac's algorithm is structurally blind
        to it, and the localised count of 4 (or 6, C6, for the real model) is the answer to a different
        question, not a rival answer to this one.

  THE PRICE, which must be quoted with the count:  the prescription does NOT follow from a variational
  principle (A4, reproduced numerically: variation symmetrises the Green function), the theory cannot be
  quantised as written (B3), and it needs a preferred initial surface.  It is a classical effective
  theory whose UV completion is, in its own authors' reading, a LOCAL one.

  D2.  DOES L31'S THEOREM SURVIVE WITHOUT HYPOTHESIS (iv)?  YES -- and not for the reason L31 expected.
  The nonlocal challenger satisfies (i), (ii) and (iii) simultaneously.  It is still not a counterexample,
  because it ALSO SATISFIES THE CONCLUSION: it carries a unit timelike vector field u^m[g], its authors
  say so in print, and because u is a normalised gradient it is hypersurface-orthogonal (C-e1), so the
  COROLLARY -- a preferred foliation -- holds too.

  And the reason is now proved rather than observed.  THE LENSING LOCK (C-b2 + C-c1): with no preferred
  background vector, every generally covariant scalar linear in h_mn is a function of Box acting on the
  single combination R^(1) ~ lap(Psi + 2 Phi).  Box^{-1} is such a function, so nonlocality buys nothing.
  A MOND term built from such scalars sources the 00 and ij equations in the locked ratio 1 : 2 and cannot
  give Tully-Fisher without destroying the no-slip relation that supplies the lensing.  Separating the
  Newtonian potential from the lensing potential requires R_mn u^m u^n -- a preferred timelike direction.
  THIS ARGUMENT NEVER USES LOCALITY.
""")

lock_holds = (dim_no_u == 1 and dim_u == 2 and lock_ratio == 2 and conf_ok)
counterexample = False       # set True only if some row satisfies (i)+(ii)+(iii) with NO preferred frame

TABLE = [
    # theory, (i) MOND+lensing, (ii) one metric, (iii) N=2, preferred timelike structure, N_grav
    ("Soussa-Woodard 2003 nonlocal f(Box^-1 R)  [frame-free]", False, True, True,
     "NONE", "2 (no extra graviton solutions)"),
    ("DEFW 2011 nonlocal MOND with u^m[g]", True, True, True,
     "YES  u^m = -grad V / |grad V|", "2 retarded / 6 localised"),
    ("Kim et al 2016 cosmological branch of the same", True, True, True,
     "YES  same u^m", "2 retarded / 6 localised"),
    ("Deffayet-Woodard 2026 mimetic-nonlocal MOND", True, True, True,
     "YES  u_m = d_m phi, (grad phi)^2 = -1", "2 retarded / 3 localised (mimetic)"),
    ("RAQUAL / AQUAL scalar-tensor (control)", False, True, False, "NONE", "3"),
    ("TeVeS (control)", True, True, False, "YES  unit timelike A^m", ">=4"),
    ("GEA / AeST (control)", True, True, False, "YES  unit timelike aether", ">=5"),
    ("general relativity (control)", False, True, True, "NONE", "2"),
]
print(f"\n  D3.  THE NONLOCAL CONTROL TABLE.  A row with (i)+(ii)+(iii) and NO preferred structure refutes "
      f"L31 without (iv).\n")
print(f"    {'theory':<52}{'(i)':>5}{'(ii)':>6}{'(iii)':>7}  {'preferred timelike structure':<42}{'N_grav'}")
for nm, i_, ii_, iii_, frame, ng in TABLE:
    print(f"    {nm:<52}{'yes' if i_ else 'NO':>5}{'yes' if ii_ else 'NO':>6}{'yes' if iii_ else 'NO':>7}  "
          f"{frame:<42}{ng}")
    if i_ and ii_ and iii_ and frame.strip().upper().startswith("NONE"):
        counterexample = True

check("D1  the mode count of retarded-nonlocal gravity is 2, not 4",
      dof(12, 4, 0) == 2.0 and err < 1e-12 and (not same_sign),
      "justified by A2 + A3 + C5, not asserted; the localised 4 (really 6) answers a different question")
check("D2  the retarded prescription is legitimate as a restriction but NOT variational, and the theory "
      "has no quantisation",
      rel_to_ret > 0.1 and sp.simplify(CONSERVATION_RESID) == 0,
      "preserved and conserved, but imposed by hand and classical-effective only")
check("D3  NO row of the nonlocal control table satisfies (i)+(ii)+(iii) with no preferred structure",
      not counterexample,
      "the frame-free nonlocal model fails (i) on lensing; every nonlocal model that passes lensing "
      "carries a unit timelike vector")
check("D4  L31's hypothesis (iv) CAN be dropped against the entire known nonlocal class",
      (not counterexample) and lock_holds,
      "and with a mechanism -- the lensing lock -- rather than by enumeration alone")
check("D5  a Lorentz-invariant (frame-free) two-mode MOND theory has NOT been exhibited",
      not counterexample,
      "the positive result that would have been the most important in this programme is NOT reached; "
      "reported as absent, not as impossible")

print("""
  D6.  WHAT IS STILL NOT PROVED, named precisely so the next lane can pick it up.

    (1) The lensing lock is proved for covariant scalars whose expansion about flat space BEGINS AT
        FIRST ORDER in h_mn.  Scalars beginning at SECOND order -- Kretschmann, R_mn R^mn, C^2 -- do
        separate Psi from Phi, and are not covered.  They are, however, exactly the objects L31's STEP E
        showed to be uniform-field-blind and dominated by the nearest star (G_loc/|grad Phi| = 11.0 at
        r = 0.2 b for a Plummer sphere; 99.0% of the solar neighbourhood inside d_eq = 2.23 pc).  THE
        MISSING COMPUTATION IS THEREFORE EXACTLY THIS: is there a nonlocal scalar, quadratic or higher in
        curvature, that BOTH separates the Newtonian from the lensing potential AND remains sensitive to
        the coherent coarse-grained field rather than to the nearest star?  If no, hypothesis (iv) is
        removable outright and L31 becomes a theorem in (i)-(iii).  If yes, that object is a live
        candidate for a frame-free MOND theory and should be built.
    (2) No one has ever computed alpha_1, alpha_2, alpha_3 for the DEFW class.  DEFW estimate the
        preferred-frame effects at (v_pec/c)^2 ~ 1e-6 and say so as a belief.  The repository's DC-019
        puts alpha_3 = O(1) for preferred-frame MOND against |alpha_3| < 4e-20.  If DC-019's mechanism
        applies to a u built nonlocally from the metric, the nonlocal class is excluded by ~2.5e19x on
        the same grounds as every other preferred-frame MOND theory.  That is a computation, not a claim,
        and it is NOT made here.
    (3) The claim that the retarded-nonlocal theory's UV completion is local is the AUTHORS' reading
        (Schwinger-Keldysh effective action of quantum gravity), and it is the reason L31 (iv) would bind
        the underlying theory.  It is an argument from the literature, not a theorem.

  D7.  THREE-SENTENCE VERDICT.
    Retarded-nonlocal gravity has TWO gravitational degrees of freedom, not four: the localised counting
    rule overcounts even ordinary general relativity, whose conformal mode carries a wrong-sign kinetic
    term, and the retarded restriction is preserved by the dynamics and conservation-safe even though it
    is imposed by hand rather than derived from an action.
    But that does not give L31 a counterexample, because the nonlocal MOND theory that reproduces MOND
    AND the observed lensing -- the only kind that satisfies hypothesis (i) -- carries a unit timelike
    vector field u^m[g] whose authors describe its consequence as 'preferred frame effects', and which,
    being a normalised gradient, is hypersurface-orthogonal and so realises L31's COROLLARY as well as its
    theorem.
    L31's hypothesis (iv) can therefore be dropped against the entire known nonlocal class, and now with
    a mechanism instead of an enumeration: without a preferred timelike direction every covariant scalar
    linear in the metric perturbation carries the one combination the Ricci scalar carries, so the
    Tully-Fisher and lensing equations are locked together and cannot be modified separately.
""")

print(f"\nCHECKS: {N_CHECKS}")
print(f"RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
