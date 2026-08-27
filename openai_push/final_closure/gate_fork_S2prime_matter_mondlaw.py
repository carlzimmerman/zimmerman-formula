"""GATE M (repair-fork session 2026-08-27): MATTER CONSERVATION + MOND LAW under the
S2 -> S2' fork, derived not asserted.

BASELINE (FAILED chassis, openai_push/final_closure):
  H_T = H_GR + H_m + int[ lam_N pi_N + mu1 C_M + mu2 S2 + mu3 S3 + shift ],
  second-class set (pi_N, C_M, S2=D^2 q, S3=D^2 p), q=(1/6)ln det gamma, p=pi/sqrt(gamma),
  C_M = D_i[c^2 mu(y) D^i lnN] - 4piG rho_m, y=(c^2/a0)|D lnN|.
  gate_matter_conservation_derivation.py result: S2 forces q=0 => Hperp_grav ~ 0 =>
  r_4 = {pi_N,H_can} = -(Hperp_grav + sqrt(g) eps_n) = -rho c^2 (matter-sourced) =>
  mu1 = -r_4/L_N density-sourced => chi-force DOUBLES Newton (g_m = g_N[1/mu + 1/M_par]),
  grad_mu T^{mu i}|_g = -rho D^i X at NEWTONIAN order, 1.6e11 x the 1-AU ephemeris bound.

THE FORK:  S2 -> S2' = D^2(q + lnN).  S2'=0 + decaying BCs => q = -lnN (Liouville) =>
  gamma_ij = (1 - 2Psi/c^2) delta_ij, Phi = Psi (gamma_PPN = 1 by design).
  NEW STRUCTURE that must be recomputed (NOTHING carries over):
   (a) new off-diagonal Dirac entry E = {pi_N, S2'} = -D^2(1/N .) != 0  -> full 4x4 redone;
   (b) r_4 changes: q = -lnN => R^(3) = 4 D^2 Psi/c^2 + O(2) => Hperp_grav != 0:
         r_4 = (c^2/4piG)[D^2 Psi - 4piG rho] = (c^2/4piG) D_i[(1-mu) D^i Psi]   (on C_M=0)
       i.e. the PHANTOM density, not -rho c^2;
   (c) r_3 = {S3, H_can} must be recomputed on the fork background (it can now feed mu1
       through the new E entry): we show r_3 = -2 D^2[S2'] + O(2) -- WEAKLY ZERO.

THIS SCRIPT DERIVES:
  A. the fork 4x4 Dirac matrix, its Pfaffian L_N*K - E*c_M, the multiplier solve,
     and the E->0 reduction to the certified Gate-8 formulas;
  B. r_4 and r_3 on the fork background: 3d tensor computation (exact conformal metric,
     exact Christoffels/Ricci) of the trace of the ADM pi^ij evolution =>
     gamma_ij pidot^ij = -2 D^2(q + lnN) + O(eps^2) -> r_3 prop to S2' (weakly zero),
     and R^(3) -> r_4 = phantom-density source;
  C. the matter EOM: universal coupling N_eff = N + chi, a = -grad(Psi + X); the exact
     static-spherical Gauss solution c^2 M_par chi' = -(1-mu) Psi'  => the chi-force now
     points OUTWARD:  g_matter = g_Psi [ 1 - (1-mu(y))/M_par(y) ] ;
  D. regimes + kernels (mu_exp, mu_5, mu_10; both a0 footings):
     Newtonian y->inf: g_matter -> g_N EXACTLY (doubling GONE, conservation violation
     suppressed by (1-mu): ~0 at 1 AU); deep MOND y->0: g_matter -> ya0 - a0/2 -> REPULSIVE
     below y_crit ~ 0.44 (kernel-shared);
  E. the observational price: RAR/BTFR destroyed below g_N ~ 0.16 a0 (the SPARC low-g
     branch), circular orbits terminate at ~10 kpc for a 1e10 Msun galaxy.

Discipline: every number computed here or quoted from a committed source named inline.
Baseline conventions reused EXACTLY (make_kernel, y_of_gN, Sereno-Jetzer bound, SPARC span
from gate_matter_conservation_derivation.py; C_q = 1/2 from gate_dirac_branch_proofs.py P2).
"""

import numpy as np
import sympy as sp

ok = True
def check(cond, label, detail=""):
    global ok
    tag = "PASS" if cond else "FAIL"
    if not cond:
        ok = False
    print(f"  [{tag}] {label}" + (f"  -- {detail}" if detail else ""))

# =============================================================================
print("=" * 78)
print("PART A -- the fork 4x4 Dirac matrix and the multiplier solve")
print("=" * 78)
# Ordering (S_4, S_1, S_2', S_3) = (pi_N, C_M, D^2(q+lnN), D^2 p).  Gate-3/8 symbol
# conventions: Delta_AB = {S_A, S_B}, dotS = r + Delta lam = 0.
# Entries:
#   {pi_N, C_M}  = L_N   (C_M depends on lnN; L_N = linearized SL operator, Gate 4)
#   {pi_N, S2'}  = E     (NEW: S2' contains lnN; E = -D^2(1/N .) as an operator)
#   {pi_N, S3}   = 0     (S3 has no N)
#   {C_M, S2'}   = 0     EXACTLY: C_M carries no gravitational momenta (pi^ij, pi_N absent)
#                        and S2' carries no momenta and no matter fields at all; a nonzero
#                        bracket needs a conjugate pair on opposite sides -- there is none.
#   {C_M, S3}    = c_M   (S3 has pi^ij, C_M has gamma_ij: generically nonzero)
#   {S2', S3}    = K     (= C_q k^4 = k^4/2 flat, gate_dirac_branch_proofs.py P2;
#                         the D^2 lnN addition to S2 has no momenta -> K unchanged at
#                         leading order)
LN, E, cM, K = sp.symbols("L_N E c_M K")
lamN, mu1, mu2, mu3 = sp.symbols("lambda_N mu_1 mu_2 mu_3")
r4, r1, r2, r3 = sp.symbols("r_4 r_1 r_2 r_3")

Delta = sp.Matrix([
    [0,   LN,  E,  0],
    [-LN, 0,   0,  cM],
    [-E,  0,   0,  K],
    [0,  -cM, -K,  0],
])
check(sp.simplify(Delta + Delta.T) == sp.zeros(4, 4), "fork Dirac matrix antisymmetric")
Pf = Delta[0,1]*Delta[2,3] - Delta[0,2]*Delta[1,3] + Delta[0,3]*Delta[1,2]
check(sp.simplify(Pf - (LN*K - E*cM)) == 0, "Pfaffian = L_N K - E c_M  (E enters!)",
      f"Pf = {sp.simplify(Pf)}")
check(sp.simplify(Delta.det() - (LN*K - E*cM)**2) == 0, "det = (L_N K - E c_M)^2")
print("  => still second-class/invertible on the generic branch (L_N K != E c_M);")
print("     the exact-flat-vacuum branch (L_N -> 0 AND c_M -> 0) degenerates as in the")
print("     baseline Gate 6 -- same measure-zero caveat, NOT worse.")

lam = sp.Matrix([lamN, mu1, mu2, mu3]); r = sp.Matrix([r4, r1, r2, r3])
sol = Delta.solve(-r)
mu1_fork = sp.simplify(sol[1]); mu2_fork = sp.simplify(sol[2])
print(f"  mu_1 (fork) = {mu1_fork}")
print(f"  mu_2 (fork) = {mu2_fork}")
check(sp.simplify(mu1_fork - (-(K*r4 + E*r3)/(LN*K - E*cM))) == 0,
      "mu_1 = -(K r_4 + E r_3)/(L_N K - E c_M): r_3 now feeds mu_1 through E")
check(sp.simplify(mu1_fork.subs(E, 0) - (-r4/LN)) == 0,
      "E -> 0 recovers certified Gate-8 formula mu_1 = -r_4/L_N")
check(sp.simplify(mu2_fork.subs(E, 0) - (r3/K + cM*r4/(LN*K))) == 0,
      "E -> 0 recovers Gate-8 mu_2 = (r_3 - c_M mu_1)/K")
print("  Matter-force channel: mu_1 C_M is the ONLY multiplier term containing matter")
print("  variables (rho_m in C_M); mu_2 S2' and mu_3 S3 are matter-free.  So the matter")
print("  force is set by mu_1 alone, sourced by r_4 AND (new) by r_3 via E.")
print("  NOTE (interior only): {S3, C_M} also carries a rho_m-proportional piece from")
print("  the gamma-dependence of rho_m (density weight); it corrects the mu_1 equation")
print("  by a rho*mu_1 term INSIDE matter and vanishes identically in vacuum. All")
print("  magnitudes below are evaluated on vacuum exteriors, where it is exactly absent.")

# =============================================================================
print()
print("=" * 78)
print("PART B -- r_4 and r_3 on the fork background (exact 3d tensor computation)")
print("=" * 78)
# Fork background: gamma_ij = e^{2w} delta_ij with w = q = -lnN (S2'=0, Liouville),
# N = e^{nu}, nu = lnN = Psi/c^2.  Static: pi^ij = 0, N^i = 0.
# We need, at linear order in the fields:
#   (i)  R^(3)  -> Hperp_grav -> r_4 = -(Hperp_grav + sqrt(g) eps_n)
#   (ii) T := gamma_ij pidot^ij = (N sqrt(g)/2) R - 2 sqrt(g) D^2 N   (standard ADM trace,
#        static pi=0, vacuum-gravity + lapse terms; matter stress = 0 for dust at rest)
#        -> r_3 = D^2( pdot ) = D^2( T/sqrt(g) )  (p = pi/sqrt(g), pi = 0 static)
x1, x2, x3, eps = sp.symbols("x1 x2 x3 epsilon")
Xs = (x1, x2, x3)
f = sp.Function("f")(x1, x2, x3)    # w = eps*f   (conformal exponent = q)
nu = sp.Function("nu")(x1, x2, x3)  # lnN = eps*nu
w_ = eps * f
N_ = sp.exp(eps * nu)
g = sp.exp(2 * w_) * sp.eye(3)
ginv = sp.exp(-2 * w_) * sp.eye(3)
sqg = sp.exp(3 * w_)

# Christoffels, Ricci: computed from the metric, no shortcut formulas assumed.
Gam = [[[sp.Rational(0)] * 3 for _ in range(3)] for _ in range(3)]
for k in range(3):
    for i in range(3):
        for j in range(3):
            expr = 0
            for l in range(3):
                expr += ginv[k, l] * (sp.diff(g[l, i], Xs[j]) + sp.diff(g[l, j], Xs[i])
                                      - sp.diff(g[i, j], Xs[l]))
            Gam[k][i][j] = sp.simplify(expr / 2)

def Ric(i, j):
    expr = 0
    for k in range(3):
        expr += sp.diff(Gam[k][i][j], Xs[k]) - sp.diff(Gam[k][i][k], Xs[j])
        for l in range(3):
            expr += Gam[k][k][l] * Gam[l][i][j] - Gam[k][j][l] * Gam[l][i][k]
    return expr

Rscal = sp.simplify(sum(ginv[i, i] * Ric(i, i) for i in range(3)))
lapf = sum(sp.diff(f, v, 2) for v in Xs)
lapnu = sum(sp.diff(nu, v, 2) for v in Xs)
gradf2 = sum(sp.diff(f, v) ** 2 for v in Xs)
# closed-form cross-check of the Ricci code: R = e^{-2w}(-4 lap w - 2 |grad w|^2)
R_closed = sp.exp(-2 * w_) * (-4 * eps * lapf - 2 * eps**2 * gradf2)
check(sp.simplify(sp.expand(Rscal - R_closed)) == 0,
      "3d Ricci code == closed form R = e^{-2w}(-4 D^2 w - 2|Dw|^2)")
R_lin = sp.expand(sp.diff(Rscal, eps).subs(eps, 0))
check(sp.simplify(R_lin + 4 * lapf) == 0,
      "R^(3) = -4 D^2 q + O(2); q = -lnN  =>  R^(3) = +4 D^2 Psi / c^2",
      f"R_lin = {R_lin}")

# (ii) the trace of the pi^ij evolution
D2N = 0
for i in range(3):
    for j in range(3):
        expr = sp.diff(N_, Xs[i], Xs[j] if i != j else Xs[i])
        expr = sp.diff(sp.diff(N_, Xs[j]), Xs[i])
        for k in range(3):
            expr -= Gam[k][i][j] * sp.diff(N_, Xs[k])
        D2N += ginv[i, j] * expr
T_trace = sp.simplify(N_ * sqg * Rscal / 2 - 2 * sqg * D2N)
T_lin = sp.expand(sp.diff(T_trace, eps).subs(eps, 0))
check(sp.simplify(T_lin - (-2 * lapf - 2 * lapnu)) == 0,
      "gamma_ij pidot^ij = -2 D^2(q + lnN) + O(2)  == -2 * (flat) S2'",
      f"T_lin = {T_lin}")
T_fork = sp.simplify(T_lin.subs(f, -nu).doit())
# substitute f = -nu properly: recompute with lapf -> -lapnu
T_fork = sp.expand(T_lin.subs(lapf, -lapnu)) if T_fork != 0 else T_fork
check(sp.simplify(T_fork) == 0,
      "on the fork surface q = -lnN:  r_3 = D^2(pdot) = -2 D^2[S2'] ~ 0 WEAKLY",
      "r_3 vanishes as a multiple of the S2' constraint itself")
print("  BASELINE CONTRAST (q = 0): gamma_ij pidot^ij = -2 D^2 lnN != 0 -- but in the")
print("  baseline {pi_N, S2} = 0, so r_3 only fed the harmless mu_2.  In the fork the")
print("  new E entry WOULD feed r_3 into mu_1 -- but r_3 is weakly zero.  So at")
print("  Newtonian order:  mu_1 = -r_4 / L_N  with the FORK r_4.")

# (i) r_4 on the fork surface
print()
print("  r_4 = -(Hperp_grav + sqrt(g) eps_n),  Hperp_grav(static) = -(c^4/16piG) sqrt(g) R")
print("      = +(c^2/4piG) D^2 Psi - rho c^2        [R = 4 D^2 Psi/c^2 from above]")
print("      = (c^2/4piG) [ D^2 Psi - 4piG rho ]")
print("      = (c^2/4piG) D_i[(1-mu) D^i Psi]       [C_M = 0: D_i(mu D^i Psi) = 4piG rho]")
rr = sp.symbols("r", positive=True)
Psi_r = sp.Function("Psi")(rr); mu_r = sp.Function("mu")(rr); rho_r = sp.Function("rho")(rr)
lapPsi = sp.diff(rr**2 * sp.diff(Psi_r, rr), rr) / rr**2
divmu = sp.diff(rr**2 * mu_r * sp.diff(Psi_r, rr), rr) / rr**2
div1mu = sp.diff(rr**2 * (1 - mu_r) * sp.diff(Psi_r, rr), rr) / rr**2
check(sp.simplify(lapPsi - divmu - div1mu) == 0,
      "D^2 Psi - D.(mu D Psi) == D.[(1-mu) D Psi]  (r_4 = phantom-density source)")
print("  => r_4 = c^2 rho_ph  (rho_ph = MOND phantom density >= 0), NOT -rho c^2.")
print("  BASELINE ANCHOR: q=0 gives R=0, r_4 = -rho c^2, chi eqn D.[c^2 M Dchi] = +4piG rho")
print("  (attractive well) => the certified doubling g_m = g_N[1/mu + 1/M_par]. Same")
print("  convention chain, fork r_4 sign FLIPS the chi channel.")

# =============================================================================
print()
print("=" * 78)
print("PART C -- matter EOM in the fork: a = -grad(Psi + X), X now REPULSIVE")
print("=" * 78)
# Universal coupling (unchanged from baseline Part B): the only matter-bearing multiplier
# term is mu_1 C_M => point particle H_p = (N + chi) E_p, chi = -(4piG/c^2) mu_1.
xx = sp.symbols("x")
t = sp.symbols("t")
p_, m_, c_ = sp.symbols("p m c", positive=True)
Psi_f = sp.Function("Psi")(xx); X_f = sp.Function("X")(xx)
H_p = (1 + Psi_f / c_**2 + X_f / c_**2) * sp.sqrt(m_**2 * c_**4 + p_**2 * c_**2)
acc = sp.simplify(-sp.diff(H_p, xx).subs(p_, 0) / m_)
check(sp.simplify(acc + sp.diff(Psi_f, xx) + sp.diff(X_f, xx)) == 0,
      "a = -grad(Psi + X) at (v/c)^0  (slow matter sees lapse only; the -Psi in")
print("        gamma_ij enters at O(v^2/c^2) -- geodesics respond to N_eff = N + chi)")
# div T violation identity (baseline Part B, unchanged in form):
rho_ = sp.Function("rho")(t, xx); v_ = sp.Function("v")(t, xx)
divT = sp.diff(rho_ * v_, t) + sp.diff(rho_ * v_**2, xx) + sp.diff(Psi_f, xx) * rho_
divT = divT.subs({sp.diff(rho_, t): -sp.diff(rho_ * v_, xx),
                  sp.diff(v_, t): -v_ * sp.diff(v_, xx) - sp.diff(Psi_f + X_f, xx)})
check(sp.simplify(sp.expand(divT) + rho_ * sp.diff(X_f, xx)) == 0,
      "grad_mu T^{mu x}|_g = -rho dX/dx  (identity unchanged; MAGNITUDE is what moved)")

# chi equation and exact spherical Gauss solution:
#   D.[c^2 M^{ij} D_j chi] = -(4piG/c^2) r_4 = -D.[(1-mu) D Psi]
#   spherical, regular at origin:  c^2 M_par(y) chi' = -(1-mu(y)) Psi'
u_r = sp.Function("u")(rr, )   # u = Psi' > 0
Mpar_r = sp.Function("M")(rr)
chi_p = -(1 - mu_r) * u_r / (c_**2 * Mpar_r)
lhs = sp.diff(rr**2 * c_**2 * Mpar_r * chi_p, rr)
rhs = -sp.diff(rr**2 * (1 - mu_r) * u_r, rr)
check(sp.simplify(lhs - rhs) == 0,
      "Gauss: c^2 M_par chi' = -(1-mu) Psi' solves D.[c^2 M Dchi] = -D.[(1-mu) DPsi]")
print("  Psi' > 0 (attractive well) => chi' < 0 => X = c^2 chi is a HILL: force OUTWARD.")
print("  NET matter force (spherical):  g_matter = g_Psi [ 1 - (1-mu(y))/M_par(y) ],")
print("  g_Psi = |D Psi| = y a0,  with the UNCHANGED exact AQUAL law mu(y) y a0 = g_N")
print("  (C_M is untouched by the fork at Newtonian order: D_i corrections are O(Psi/c^2)).")
y_s = sp.symbols("y", positive=True)
for name, mu_of_y in [("mu_exp", 1 - sp.exp(-y_s)),
                      ("mu_5", y_s / (1 + y_s**5) ** sp.Rational(1, 5)),
                      ("mu_10", y_s / (1 + y_s**10) ** sp.Rational(1, 10))]:
    Mp = sp.diff(y_s * mu_of_y, y_s)
    fac = 1 - (1 - mu_of_y) / Mp
    check(sp.simplify(fac - (2 * mu_of_y + y_s * sp.diff(mu_of_y, y_s) - 1) / Mp) == 0,
          f"net factor = (2 mu + y mu' - 1)/M_par  [{name}]")

# =============================================================================
print()
print("=" * 78)
print("PART D -- regimes and kernels: Newton EXACT at high y; REPULSIVE below y_crit")
print("=" * 78)

def make_kernel(kind, nn=None):
    if kind == "exp":
        mu  = lambda yv: 1 - np.exp(-yv)
        Mpar= lambda yv: 1 - np.exp(-yv) + yv * np.exp(-yv)
        lab = "mu_exp"
    else:
        mu  = lambda yv: yv * (1 + yv**nn) ** (-1.0 / nn)
        Mpar= lambda yv: yv * (2 + yv**nn) * (1 + yv**nn) ** (-(nn + 1.0) / nn)
        lab = f"mu_{nn}"
    return lab, mu, Mpar

kernels = [make_kernel("exp"), make_kernel("n", 5), make_kernel("n", 10)]

def y_of_gN(gN, a0, mu):
    """Solve mu(y) * y * a0 = g_N for y (the C_M Gauss law).  [baseline verbatim]"""
    yv = np.maximum(gN / a0, np.sqrt(np.maximum(gN / a0, 1e-300)))
    for _ in range(200):
        f = mu(yv) * yv * a0 - gN
        h = 1e-7 * np.maximum(yv, 1e-30)
        fp = (mu(yv + h) * (yv + h) - mu(yv - h) * (yv - h)) / (2 * h) * a0
        yv = np.maximum(yv - f / fp, 1e-30)
    return yv

def net_factor(yv, mu, Mp):
    return 1.0 - (1.0 - mu(yv)) / Mp(yv)

for lab, mu, Mp in kernels:
    hi = 1e8
    check(abs(net_factor(hi, mu, Mp) - 1) < 1e-12,
          f"Newtonian regime: g_matter -> g_N EXACTLY (doubling GONE)  [{lab}]",
          f"factor(1e8) = {net_factor(hi, mu, Mp):.15f}")
    lo = 1e-6
    dm = (1 - mu(lo)) / Mp(lo) * 2 * lo
    check(abs(dm - 1) < 1e-3,
          f"deep MOND: (1-mu)/M_par -> 1/(2y)  =>  g_matter -> y a0 - a0/2  [{lab}]",
          f"(1-mu)/M_par * 2y = {dm:.6f} at y=1e-6")

def bisect(fn, a, b, n=200):
    fa = fn(a)
    for _ in range(n):
        m = 0.5 * (a + b); fm = fn(m)
        if fa * fm <= 0: b = m
        else: a, fa = m, fm
    return 0.5 * (a + b)

print("\n  y_crit (net force = 0; repulsive below), g_N,crit = mu(y_c) y_c a0:")
ycrits = {}
for lab, mu, Mp in kernels:
    yc = bisect(lambda yv: net_factor(yv, mu, Mp), 1e-4, 5.0)
    ycrits[lab] = yc
    for a0v, foot in [(9.36e-11, "canonical"), (1.13e-10, "alt")]:
        gc = mu(yc) * yc * a0v
        print(f"  [{lab:6s} | {foot:9s}] y_crit = {yc:.4f}  g_N,crit = {mu(yc)*yc:.4f} a0"
              f" = {gc:.3e} m/s^2 ; g_Psi at crossing = {yc:.4f} a0")
check(abs(ycrits["mu_exp"] - 0.4429) < 5e-3,
      "mu_exp: y_crit solves e^y + y = 2  => y_crit = 0.4429",
      f"y_crit = {ycrits['mu_exp']:.4f}")

print("\n  (a) SOLAR SYSTEM at 1 AU vs the committed ephemeris bound")
G = 6.674e-11; Msun = 1.989e30; AU = 1.496e11
BOUND = 3.66e-14   # m/s^2, Sereno & Jetzer 2006 Earth bound, committed in
                   # real_research/reviews/a0_local_ephemeris_2026.py (baseline verbatim)
gN_au = G * Msun / AU**2
print(f"  g_N(1 AU) = {gN_au:.4e} m/s^2 ; bound = {BOUND:.2e} m/s^2 ;"
      f" baseline chassis: g_chi = {gN_au:.2e} = 1.62e11 x bound (FAIL)")
# numerically STABLE 1-mu at large y (naive 1-mu(y) is double-precision noise ~1e-16):
#   mu_exp: 1-mu = e^{-y} (log10 path);  mu_n: 1-mu = -expm1(-log1p(y^{-n})/n) ~ y^{-n}/n
onem_stable = {"mu_exp": None,
               "mu_5":  lambda yv: -np.expm1(-np.log1p(yv**-5.0) / 5.0),
               "mu_10": lambda yv: -np.expm1(-np.log1p(yv**-10.0) / 10.0)}
worst = 0.0
for a0v, foot in [(9.36e-11, "canonical rho_DE/cH_Lambda"), (1.13e-10, "alt rho_total/cH0")]:
    for lab, mu, Mp in kernels:
        yloc = float(y_of_gN(np.array([gN_au]), a0v, mu)[0])
        if lab == "mu_exp":
            # 1-mu = e^{-y}: underflows; report log10
            log10gx = -yloc * np.log10(np.e) + np.log10(yloc * a0v / Mp(yloc))
            print(f"  [{foot} | {lab:6s}] y_loc={yloc:.3e}  g_chi = 10^({log10gx:.3e}) m/s^2"
                  f"  -> 10^{log10gx - np.log10(BOUND):.3e} x bound")
        else:
            gx = onem_stable[lab](yloc) / Mp(yloc) * yloc * a0v
            worst = max(worst, gx / BOUND)
            print(f"  [{foot} | {lab:6s}] y_loc={yloc:.3e}  g_chi = {gx:.3e} m/s^2"
                  f"  = {gx/BOUND:.2e} x bound")
# stable-formula sanity at moderate y where the naive form is still accurate:
check(abs(onem_stable["mu_5"](3.0) - (1 - kernels[1][1](3.0))) < 1e-12,
      "stable 1-mu formula == naive 1-mu at y=3 (mu_5)")
check(worst < 1e-20, "1-AU conservation violation now BELOW bound by > 20 orders (all"
      " kernels, both footings)", f"worst (mu_5) = {worst:.2e} x bound")
print("  => grad_mu T^{mu i} violation is (1-mu)-GATED: exp/power suppressed at high y.")
print("     It is NO LONGER Newtonian-order in the solar system.  It remains (v/c)^0")
print("     and O(1) of the MOND force in the low-y regime (see Part E).")
print("\n  EFE channel (galactic y_ext = 1.9 at the Sun, DHF freeze): fractional outward")
print("  chi correction to the ambient MOND field = (1-mu)/M_par:")
for lab, mu, Mp in kernels:
    print(f"  [{lab:6s}] (1-mu)/M_par (y=1.9) = {(1-mu(1.9))/Mp(1.9):.4f}")
print("  => the frozen Q2 = (3/2) q a0/R_M pricing inherits an O(13%) (mu_exp) chi-term:")
print("     rerun needed, but it corrects an ALLOWED effect (not a new violation).")

# =============================================================================
print()
print("=" * 78)
print("PART E -- the MOND law in the physical metric: RAR / BTFR confrontation")
print("=" * 78)
a0c = 9.36e-11
print("  Effective law: g_obs(g_bar) = y a0 [1 - (1-mu)/M_par],  mu(y) y a0 = g_bar")
print("  (no G-doubling: g_bar = g_N directly; kappa=1/2 bookkeeping RESTORED --")
print("   baseline needed kappa_bare = 0.6285, a +1.8/+2.2 sigma strain: GONE).")
print("\n  nu_eff = g_obs/g_bar across the transition (canonical a0):")
ytab = [0.05, 0.1, 0.2, 0.4429, 1.0, 1.9, 3.0, 10.0]
hdr = "  y:      " + "".join(f"{yv:>9.3f}" for yv in ytab)
print(hdr)
for lab, mu, Mp in kernels:
    row = [net_factor(yv, mu, Mp) / mu(yv) for yv in ytab]
    print(f"  [{lab:6s}]" + "".join(f"{v:>9.3f}" for v in row))
print("  (canonical framework nu = g_obs/g_bar = sqrt(1 + a0/g_bar) is >= 1 EVERYWHERE;")
print("   the fork's nu_eff goes NEGATIVE below y_crit.)")

gNb = np.logspace(-12.5, -8.5, 400)   # SPARC-ish span, baseline Part F verbatim
for lab, mu, Mp in kernels:
    yv = y_of_gN(gNb, a0c, mu)
    g_obs = yv * a0c * net_factor(yv, mu, Mp)
    frac_neg = float(np.mean(g_obs <= 0))
    g_can = np.sqrt(gNb**2 + gNb * a0c)   # the framework's own interpolation
    pos = g_obs > 0
    r_dex = np.log10(g_obs[pos]) - np.log10(g_can[pos])
    print(f"  [{lab:6s}] fraction of SPARC span (1e-12.5..1e-8.5) with g_obs <= 0"
          f" (REPULSIVE): {frac_neg*100:.0f}% ; residual vs framework law on the"
          f" positive part: rms = {np.sqrt(np.mean(r_dex**2)):.2f} dex,"
          f" max = {np.max(np.abs(r_dex)):.2f} dex")
lab, mu, Mp = kernels[0]
for gb in [1e-12, 1e-11, 3e-11, 1e-10, 1e-9]:
    yv = float(y_of_gN(np.array([gb]), a0c, mu)[0])
    go = yv * a0c * net_factor(yv, mu, Mp)
    gc = np.sqrt(gb**2 + gb * a0c)
    print(f"  [mu_exp] g_bar = {gb:.0e}:  g_obs(fork) = {go:+.3e}  vs framework"
          f" {gc:.3e}  m/s^2")
yv = y_of_gN(gNb, a0c, kernels[0][1])
g_obs = yv * a0c * net_factor(yv, kernels[0][1], kernels[0][2])
check(float(np.mean(g_obs <= 0)) > 0.3,
      "MOND LAW DESTROYED: net force repulsive over the low-acceleration ~40% of the"
      " SPARC RAR span (observed branch g_obs = +sqrt(g_bar a0) there)")

print("\n  BTFR / rotation curves (point mass M = 1e10 Msun, vacuum exterior):")
M10 = 1e10 * Msun
kpc = 3.086e19
for a0v, foot in [(9.36e-11, "canonical"), (1.13e-10, "alt")]:
    for lab, mu, Mp in kernels:
        gc = mu(ycrits[lab]) * ycrits[lab] * a0v
        rk = np.sqrt(G * M10 / gc) / kpc
        print(f"  [{foot:9s} | {lab:6s}] circular orbits END at r = {rk:.1f} kpc"
              f" (g_N < g_crit beyond); v^2 = r g_obs < 0 there")
vflat = (G * M10 * a0c) ** 0.25
print(f"  framework/MOND BTFR: v_flat = (G M a0)^(1/4) = {vflat/1e3:.0f} km/s, flat")
print(f"  FOREVER; fork: v^2(r) -> -a0 r/2 (unbound repulsion).  BTFR does NOT survive.")
print("  The exact spherical AQUAL solution for Psi SURVIVES (C_M untouched), but")
print("  matter does not orbit on Psi -- it orbits on Psi + X.")
print("\n  Lensing note (defer to Gate L): photons see grad_perp(2 Psi + X); the same")
print("  chi channel turns weak lensing repulsive below y where (1-mu)/M_par = 2:")
for lab, mu, Mp in kernels:
    yl = bisect(lambda yv: (1 - mu(yv)) / Mp(yv) - 2.0, 1e-4, 5.0)
    print(f"  [{lab:6s}] lensing sign flip at y = {yl:.3f} (Mistele KiDS stack probes"
          f" y ~ 0.01-0.3: contaminated)")

# =============================================================================
print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("""  FORK STRUCTURE: new Dirac entry E = {pi_N, S2'} != 0; Pfaffian L_N K - E c_M;
  still second-class generic; mu_1 = -(K r_4 + E r_3)/(L_N K - E c_M).        [Part A]
  r_3 = -2 D^2[S2'] + O(2): WEAKLY ZERO on the fork surface (the q = -lnN tie
  that fixes gamma_PPN also cancels the trace evolution) => mu_1 = -r_4/L_N.  [Part B]
  r_4 FLIPS: q = -lnN revives R^(3) = 4 D^2 Psi/c^2, so r_4 = (c^2/4piG)
  D.[(1-mu) D Psi] = +c^2 rho_phantom, not -rho c^2.                          [Part B]
  Matter EOM: a = -grad(Psi + X); Gauss: c^2 M_par chi' = -(1-mu) Psi' =>
  g_matter = g_Psi [1 - (1-mu)/M_par]  -- the chi force points OUTWARD.       [Part C]
  (1) CONSERVATION: grad_mu T^{mu i}|_g = -rho D^i X still an identity, but the
      magnitude is (1-mu)-gated: 1 AU violation ~ 10^(-2.75e7) (mu_exp) /
      3e-29 x bound (mu_5) -- the baseline's 1.6e11 x FAIL is REPAIRED; the
      exact doubling is GONE (g -> g_N exactly, kappa bookkeeping restored).  [Part D]
  (2) MOND LAW: NOT the same AQUAL law.  Modified nu_eff = [1-(1-mu)/M_par]/mu
      crosses ZERO at y_crit ~ 0.443 (mu_exp; kernel-shared 0.3-0.45) =
      g_N ~ 0.16 a0 ~ 1.5e-11 m/s^2, and the deep-MOND limit is a REPULSIVE
      floor g -> -a0/2.  ~40% of the SPARC RAR span turns repulsive; rotation
      curves terminate (~10 kpc at 1e10 Msun); BTFR does not survive.  Shared
      by mu_exp AND mu_n (any kernel with mu ~ y at small y: (1-mu)/M_par ->
      1/(2y)); NOT repairable by Gate-13 kernel swap.                          [Part E]
  The defect is the SAME structural disease as the baseline (deleted Hamiltonian
  constraint => matter-coupled multiplier mu_1), relocated: the fork moves the
  chi-force from the Newtonian regime (where it killed ephemerides) into the
  MOND regime (where it kills the RAR/BTFR -- the theory's own home turf).
""")
print("GATE RESULT: DERIVED -- FAIL (MOND law destroyed in deep-MOND regime;"
      " conservation pricing repaired)" if ok else "GATE RESULT: SCRIPT INCONSISTENCY")
import sys
sys.exit(0 if ok else 1)
