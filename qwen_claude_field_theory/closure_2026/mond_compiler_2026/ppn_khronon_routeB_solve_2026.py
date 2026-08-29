#!/usr/bin/env python3
r"""
*** SUPERSEDED -- kept for provenance only.  Use ppn_khronon_routeB_num_2026.py. ***

TWO DEFECTS found and fixed downstream:
  (1) it gauge-fixes tau = 0, which FAILS on the candidate locus beta+lam = 0 (there tau
      enters the action only through w.grad(tau), so the residual static xi^0 freedom is
      unfixed as w -> 0 and the 5x5 response matrix degenerates; sympy then returns a
      particular solution of a singular system).  The fix is to solve the full 6x6
      underdetermined system and use only xi^0-invariant pieces.
  (2) its "alpha_1" adds alpha_2 to the g_0x readout.  Calibration against the published
      khronometric formulas shows the correct assignment is
          alpha_1 = -2 * d(Z_x/U)/dw_x   (no alpha_2 piece: the alpha_2 term in g_0i is
                                          the pure gradient w^j chi_{,ij}, which has no
                                          x-component when k_x = 0).

ppn_khronon_routeB_solve_2026.py -- solve the linear response and read off gamma, G_N,
alpha_1, alpha_2, alpha_3 for the covariant khronometric family

   S = (1/16 pi G) Int sqrt(-g)[ R + alpha a.a + beta nab_m u_n nab^n u^m + lam (nab.u)^2 ]
       - Int rho_c sqrt(-g_00)

Uses the Fourier field equations built by ppn_khronon_routeB_2026.py.

READOUT (Will TEGP 4.46), static source at rest, preferred frame (khronon) moving at w,
gauge tau = 0 (residual static xi^0 used up), h_ij = 2 Psi delta_ij:

   Phi := h_00/2 ;  U(k) = 4 pi G_N rho/k^2
   Phi/U = 1 - (1/2)(alpha_1 - alpha_3) w^2 + alpha_2 (k.w)^2/k^2      [gauge-safe]
   g_0i  = (alpha_2 - alpha_1)/2 * w_i U + (gauge-dependent) k_i (k.w)/k^2 U
   Psi/Phi = gamma_PPN  at w = 0
"""
import sympy as sp
import pickle
import os

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, '_routeB_feq.pkl'), 'rb') as fh:
    D = pickle.load(fh)
FEQ = {k: sp.sympify(v) for k, v in D['FEQ'].items()}

k1, k2, k3 = sp.symbols('k1 k2 k3', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
G = sp.symbols('G', positive=True)
al, be, lm = sp.symbols('alpha beta lambda_', real=True)
Ph, Ps, Z1h, Z2h, Z3h, Th, Rh = sp.symbols('Phih Psih Z1h Z2h Z3h tauh rhoh')

kk, wx, wz = sp.symbols('kk wx wz', positive=True)

FRAME = {k1: 0, k2: 0, k3: kk, w1: wx, w2: 0, w3: wz, Th: 0}

EQS = {}
for key, e in FEQ.items():
    EQS[key] = sp.expand(sp.simplify(e.subs(FRAME)))

UNK = [Ph, Ps, Z1h, Z2h, Z3h]
SYS = [EQS['Phi'], EQS['Psi'], EQS['Z0'], EQS['Z1'], EQS['Z2']]


def solve_case(subs, label):
    print("=" * 78)
    print("CASE:", label)
    S = [sp.expand(e.subs(subs)) for e in SYS]
    sol = sp.solve(S, UNK, dict=True)
    if not sol:
        print("   *** NO SOLUTION / SINGULAR SYSTEM ***")
        M, rhs = sp.linear_eq_to_matrix(S, UNK)
        print("   det(M) =", sp.factor(sp.simplify(M.det())))
        return None
    sol = sol[0]
    # tau equation redundancy check
    tres = sp.simplify(EQS['tau'].subs(subs).subs(sol))
    print("   tau-equation residual (must be 0):", tres)

    PhiS = sp.simplify(sol[Ph])
    PsiS = sp.simplify(sol[Ps])

    # --- Newton normalisation at w = 0
    Phi0 = sp.simplify(PhiS.subs({wx: 0, wz: 0}))
    GN = sp.simplify(Phi0*kk**2/(4*sp.pi*Rh))          # Phi0 = 4 pi G_N rho/k^2
    print("   G_N/G   =", sp.simplify(GN/G))
    gamma = sp.simplify(PsiS.subs({wx: 0, wz: 0})/Phi0)
    print("   gamma_PPN =", gamma)

    U = 4*sp.pi*GN*Rh/kk**2
    ratio = sp.simplify(PhiS/U)
    r2 = sp.expand(sp.series(sp.series(ratio, wx, 0, 3).removeO(), wz, 0, 3).removeO())
    A = sp.simplify(r2.coeff(wx, 2).subs(wz, 0))       # coeff of w_perp^2  -> A
    C = sp.simplify(r2.coeff(wz, 2).subs(wx, 0))       # coeff of w_par^2   -> A + alpha_2
    a2 = sp.simplify(C - A)
    a1m3 = sp.simplify(-2*A)
    print("   alpha_2          =", sp.simplify(sp.factor(a2)))
    print("   alpha_1 - alpha_3 =", sp.simplify(sp.factor(a1m3)))

    # --- g_0i cross check: coefficient of w_i U in zeta_i.  With k along z:
    #     zeta_x = A_z wx U   (there is no k_x, so no gradient contamination in x!)
    zx = sp.simplify(sol[Z1h])
    Az = sp.simplify(sp.limit(zx/(wx*U), wx, 0))
    a1ma2 = sp.simplify(-2*Az)
    print("   alpha_1 - alpha_2 (from g_0x, gauge-invariant) =", sp.simplify(sp.factor(a1ma2)))
    a1 = sp.simplify(a2 + a1ma2)
    a3 = sp.simplify(a1 - a1m3)
    print("   ==> alpha_1 =", sp.simplify(sp.factor(a1)))
    print("   ==> alpha_2 =", sp.simplify(sp.factor(a2)))
    print("   ==> alpha_3 =", sp.simplify(sp.factor(a3)))
    return {'gamma': gamma, 'GN': sp.simplify(GN/G), 'a1': a1, 'a2': a2, 'a3': a3}


print("#### VALIDATION 1: GR (alpha=beta=lam=0) ####")
solve_case({al: 0, be: 0, lm: 0}, "GR")

print()
print("#### VALIDATION 2: general khronometric (alpha,beta,lam) ####")
res = solve_case({}, "khronometric general")
if res:
    a1_pub = 4*(al - 2*be)/(be - 1)
    a2_pub = a1_pub/2 + (al - 2*be)*(al + be + 3*lm)/((be + lm)*(2 - al))
    print("   published alpha_1 [Blas-Sibiryakov / Foster-Jacobson HO limit] =", a1_pub)
    print("   DIFFERENCE alpha_1 - published :",
          sp.simplify(sp.together(res['a1'] - a1_pub)))
    print("   published alpha_2 =", sp.simplify(a2_pub))
    print("   DIFFERENCE alpha_2 - published :",
          sp.simplify(sp.together(res['a2'] - a2_pub)))

print()
print("#### CANDIDATE: beta = lam = 0 (GR sector K_ijK^ij - K^2 + R3) ####")
solve_case({be: 0, lm: 0}, "candidate beta=lam=0")
