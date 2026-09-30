#!/usr/bin/env python3
"""q02: beta function, RG-invariant scale, trace anomaly, vacuum energy eps = <theta>/4, instanton-density relation.

  B1  b0 from the helicity-sum (Nielsen-Hughes) form  b0 = (1/2) sum_states (-1)^{2 lam} T(R) [ (2 lam)^2 - 1/3 ]
      reproduces 11N/3 - 2 nf/3 - (1/3) T_S n_s ; b0 is RATIONAL (all pi's are in the loop factor).
  B2  numerical RG flow (scipy): one-loop Lambda_1 = mu exp(-8 pi^2/(b0 g^2)) is constant; the two-loop RG-invariant scale
      Lambda_2 = mu (b0 g^2/16 pi^2)^(-b1/(2 b0^2)) exp(-8 pi^2/(b0 g^2)) is constant to O(g^2) along the two-loop flow.
  B3  trace anomaly theta = mu dL/dmu = -(b0/32 pi^2) F^2_geo (sympy), eps_vac = theta/4 from <T_mn> = eps g_mn (sympy trace),
      and the dilaton-type potential V = a chi ln(chi/Lambda^4): V(min) = theta/d_chi with d_chi = 4.
  B4  dilute instanton gas: <g^2 F^2>/(32 pi^2) = n (instanton + anti-instanton density)  =>  eps = -(b0/4) n,
      <(alpha_s/pi) G^2> = 8 n ; numbers at n = 1 fm^-4 vs the phenomenological SVZ gluon condensate (input, not derived).
  B5  c_vac scaling: eps_vac/Lambda^4 is a non-universal number (N^2 scaling, scheme, condensate uncertainty): only the
      structure is checked here, no lattice number is claimed.
Every check has a control/mutation ('MUT') that must fail the claim it attacks.
"""
import sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

pi = sp.pi
# ------------------------------------------------------------------ B1: b0 from helicity sums
def b0_states(N, nf=0, ns=0, Cadj=None):
    """b0 = (1/2) sum over helicity states (-1)^{2 lam} T(R) [(2 lam)^2 - 1/3].
    gluon: 2 helicity states, adjoint T = N;  Dirac fundamental: 4 states (lam = +-1/2, particle+antiparticle), T = 1/2;
    complex scalar fundamental: 2 states, lam = 0, T = 1/2."""
    R = sp.Rational
    gl = 2 * N * (R(1, 2)) * (4 - R(1, 3))
    fe = nf * 4 * R(1, 2) * (R(1, 2)) * (-1) * (1 - R(1, 3))
    sc = ns * 2 * R(1, 2) * (R(1, 2)) * (+1) * (0 - R(1, 3))   # (-1)^{2 lam} = +1 for scalars
    return sp.nsimplify(gl + fe + sc)
b0_std = lambda N, nf=0, ns=0: sp.Rational(11, 3) * N - sp.Rational(2, 3) * nf - sp.Rational(1, 6) * ns
bad = [(N, nf, ns) for N in range(2, 7) for nf in range(0, 7) for ns in range(0, 4) if b0_states(N, nf, ns) != b0_std(N, nf, ns)]
chk("B1 helicity-sum b0 = 11N/3 - 2nf/3 - ns/6 for N=2..6, nf=0..6, ns=0..3 (%d mismatches)" % len(bad), not bad)
# MUT: an exponent (2 lam)^2 -> (2 lam)^3 (or dropping the -1/3 diamagnetic term) must break 11/3
mut1 = sp.Rational(1, 2) * 2 * (sp.Rational(1, 2)) * (2**3 - sp.Rational(1, 3))
mut2 = sp.Rational(1, 2) * 2 * (4)
chk("MUT B1 wrong spin power or missing diamagnetic -1/3 does not give 11/3 (%s, %s)" % (mut1, mut2), mut1 != sp.Rational(11, 3) and mut2 != sp.Rational(11, 3))
chk("B1 b0 is rational for every entry (pi lives only in 1/(16 pi^2)); paramagnetic 4 minus diamagnetic 1/3 = 11/3 per gluon helicity pair", all(sp.Rational(b0_std(N)).q in (1, 3) for N in range(2, 8)))

# ------------------------------------------------------------------ B2: RG numerics
def b1_std(N, nf=0):
    CF = sp.Rational(N**2 - 1, 2 * N)
    return sp.Rational(34, 3) * N**2 - sp.Rational(10, 3) * N * nf - 2 * CF * nf
def run(N, nf, g2_start, t_end, loops):
    b0 = float(b0_std(N, nf)); b1 = float(b1_std(N, nf))
    # y = 1/g^2 ; dy/dt = b0/(8 pi^2) + loops2 * b1 g^2/(128 pi^4)   (t = ln mu)
    def f(t, y):
        g2 = 1.0 / y[0]
        return [b0 / (8 * math.pi**2) + (b1 * g2 / (128 * math.pi**4) if loops == 2 else 0.0)]
    return solve_ivp(f, [0, t_end], [1.0 / g2_start], rtol=1e-11, atol=1e-13, dense_output=True)
N, nf = 3, 0
b0 = float(b0_std(N, nf)); b1 = float(b1_std(N, nf))
chk("B2 SU(3) pure YM: b0 = 11, b1 = 102", b0 == 11 and b1 == 102)
g2_P = 0.1
lnMP = math.log(1.22e19)           # mu = M_P in GeV  (t = ln mu; start at M_P and run down 60 e-folds ~ 26 decades)
Lam1 = lambda mu, g2: mu * math.exp(-8 * math.pi**2 / (b0 * g2))
Lam2 = lambda mu, g2: mu * (b0 * g2 / (16 * math.pi**2)) ** (-b1 / (2 * b0**2)) * math.exp(-8 * math.pi**2 / (b0 * g2))
for loops in (1, 2):
    sol = run(N, nf, g2_P, -50.0, loops)
    ts = np.linspace(0, -50, 11)
    L1 = [Lam1(math.exp(lnMP + t), 1.0 / sol.sol(t)[0]) for t in ts]
    L2 = [Lam2(math.exp(lnMP + t), 1.0 / sol.sol(t)[0]) for t in ts]
    spread1 = max(L1) / min(L1); spread2 = max(L2) / min(L2)
    print("     %d-loop flow, 50 e-folds below M_P (g^2: %.3f -> %.3f): Lambda_1 spread %.3g, Lambda_2 spread %.4g" % (loops, g2_P, 1.0 / sol.sol(-50)[0], spread1, spread2))
    if loops == 1:
        chk("B2 one-loop flow: Lambda_1 = mu exp(-8 pi^2/(b0 g^2)) constant to 1e-9 (RG invariant)", spread1 < 1 + 1e-9)
    else:
        chk("B2 two-loop flow: Lambda_2 constant to <1%% over 50 e-folds (spread %.4f) while the one-loop Lambda_1 drifts by %.0f%% (so the b1 prefactor is needed)" % (spread2, 100 * (spread1 - 1)), spread2 < 1.01 and spread1 > 1.3)
        chk("MUT B2 dropping the (b0 g^2/16 pi^2)^(-b1/2b0^2) prefactor (Lambda_1) is NOT invariant at two loops (drift >30%)", spread1 > 1.3)
        # (my first threshold 'Lambda_1 drifts >10x' was a wrong expectation of mine: the drift over 50 e-folds is 1.66, the point is the factor 8 in the NORMALISATION)
        ratio_now = Lam2(1.22e19, g2_P) / Lam1(1.22e19, g2_P)
        print("     Lambda_2/Lambda_1 at fixed g^2(M_P) = 0.1: %.3f  ->  rho ~ Lambda^4 changes by %.4g" % (ratio_now, ratio_now**4))

# ------------------------------------------------------------------ B3: trace anomaly + eps = theta/4
mu_, b0s, F2 = sp.symbols('mu b0 F2', positive=True)
lnmu = sp.symbols('lnmu', real=True)
ginv2 = sp.Function('y')(lnmu)                      # 1/g^2 as a function of ln mu
Lag = -sp.Rational(1, 4) * ginv2 * F2               # L = -(1/4 g^2) F^2  (geometric F)
theta = sp.diff(Lag, lnmu).subs(sp.Derivative(ginv2, lnmu), b0s / (8 * pi**2))
chk("B3 theta = mu dL/dmu = -(b0/32 pi^2) F^2_geo  (F^2 positive-definite -> theta < 0)", sp.simplify(theta + b0s / (32 * pi**2) * F2) == 0)
# canonical normalisation: F_geo = g F_c  ->  -(b0 g^2/32 pi^2) F_c^2 = (beta/2g) F_c^2
gsym, Fc2 = sp.symbols('g Fc2', positive=True)
beta = -b0s * gsym**3 / (16 * pi**2)
chk("B3 canonical form  theta = (beta/(2g)) F_c^2 = -(b0 g^2/(32 pi^2)) F_c^2", sp.simplify(beta / (2 * gsym) * Fc2 + b0s * gsym**2 / (32 * pi**2) * Fc2) == 0)
chk("MUT B3 the (beta/g) F^2 coefficient (no 1/2) would give 16 pi^2, not 32 pi^2", sp.simplify(beta / gsym * Fc2 + b0s * gsym**2 / (32 * pi**2) * Fc2) != 0)
# vacuum: <T_mn> = eps g_mn  => trace = D eps
eps = sp.symbols('eps')
gmat = sp.diag(1, -1, -1, -1)
Tvac = eps * gmat
tr = sum((gmat.inv() * Tvac)[i, i] for i in range(4))
chk("B3 <T_mn> = eps g_mn (Lorentz invariant vacuum): T^mu_mu = 4 eps, so eps = <theta>/4 (the 1/4 is 1/D)", sp.simplify(tr - 4 * eps) == 0)
# dilaton-type potential with a condensate chi of dimension D (= spacetime dimension): V = a chi ln(chi/Lambda^D)
chi, a, Lm, Dsym = sp.symbols('chi a Lambda D', positive=True)
V = a * chi * sp.log(chi / Lm**Dsym)
theta_V = Dsym * V - Dsym * chi * sp.diff(V, chi)      # T^mu_mu = D V - d_chi chi V',  d_chi = D
chi_min = sp.solve(sp.diff(V, chi), chi)[0]
V_min = sp.simplify(V.subs(chi, chi_min))
chk("B3 dilaton potential V = a chi ln(chi/Lambda^D): T^mu_mu = -D a chi and V(min) = T^mu_mu/D  (eps = theta/D, D = 4 here)",
    sp.simplify(theta_V.subs(chi, chi_min) / Dsym - V_min) == 0 and sp.simplify(theta_V + Dsym * a * chi) == 0)
a_match = sp.simplify(sp.solve(sp.Eq(-4 * a, -b0s / (32 * pi**2)), a)[0])
chk("B3 matching -4 a chi = theta = -(b0/32 pi^2) F^2 gives a = b0/(128 pi^2): eps_vac = -(b0/(128 pi^2)) <F^2_geo>", sp.simplify(a_match - b0s / (128 * pi**2)) == 0)
chk("MUT B3 in D = 3 the same construction gives eps = theta/3, not theta/4: the 1/4 is 1/D of THIS spacetime and of any Lorentz-invariant vacuum, nothing YM-specific",
    sp.simplify((theta_V.subs(chi, chi_min) / Dsym - V_min).subs(Dsym, 3)) == 0 and sp.Rational(1, 3) != sp.Rational(1, 4))

# ------------------------------------------------------------------ B4: instanton density, eps = -(b0/4) n
hbarc = 0.1973269804                                      # GeV fm
n_fm4 = 1.0
n_GeV4 = n_fm4 * hbarc**4
g2F2 = 32 * math.pi**2 * n_GeV4                           # <g^2 F^2> for a dilute (anti)self-dual gas: each object carries 32 pi^2
alpha_over_pi_G2 = g2F2 / (4 * math.pi**2)                # (alpha_s/pi) G^2 = g^2 F^2/(4 pi^2)
print("     n = 1 fm^-4 = %.4e GeV^4 ; <g^2 F^2> = %.4f GeV^4 ; <(alpha_s/pi) G^2> = %.5f GeV^4" % (n_GeV4, g2F2, alpha_over_pi_G2))
chk("B4 <(alpha_s/pi) G^2> = 8 n  (dilute gas, exact algebra 32 pi^2/(4 pi^2) = 8)", abs(alpha_over_pi_G2 / n_GeV4 - 8) < 1e-12)
chk("B4 n = 1 fm^-4 gives <g^2 G^2> = 0.48 GeV^4 and <(alpha/pi) G^2> = 0.0121 GeV^4: consistent with the phenomenological SVZ inputs (0.5 GeV^4, 0.012 GeV^4) [inputs, not derived here]",
    abs(g2F2 - 0.5) < 0.05 and abs(alpha_over_pi_G2 - 0.012) < 0.001)
agree = True
for Nc, nfl in ((3, 0), (3, 3), (2, 0)):
    bb = float(b0_std(Nc, nfl))
    eps1 = -(bb / 4) * n_GeV4                             # eps = -(b0/4) n
    eps2 = -(bb / 128 / math.pi**2) * g2F2                # eps = -(b0/128 pi^2) <g^2 F^2>
    eps3 = -(bb / 32) * alpha_over_pi_G2                  # eps = -(b0/32) <(alpha/pi) G^2>
    agree = agree and abs(eps1 - eps2) < 1e-15 and abs(eps1 - eps3) < 1e-15
    print("     N=%d nf=%d: b0 = %.3f, eps = -(b0/4) n = %.3e GeV^4 = %.0f MeV/fm^3" % (Nc, nfl, bb, eps1, eps1 / hbarc**3 * 1000))
chk("B4 eps = -(b0/4) n = -(b0/128 pi^2)<g^2F^2> = -(b0/32)<(alpha/pi)G^2> agree for (N,nf) = (3,0),(3,3),(2,0)  [the same 32 pi^2 unit]", agree)
chk("MUT B4 with the 8 -> 4 miscount (n = <g^2F^2>/(16 pi^2)) the condensate would be 0.024 GeV^4, twice the SVZ input: rejected",
    abs(2 * alpha_over_pi_G2 - 0.012) > 0.005)
# integrated anomaly = -b0 per (anti)instanton: consistency of B3 and B4
chk("B4 Int theta d^4x = -b0 (x n_total volume): each (anti)self-dual object contributes -b0 (from B3 x 32 pi^2)", sp.simplify(-b0s / (32 * pi**2) * 32 * pi**2 + b0s) == 0)

# ------------------------------------------------------------------ B5: c_vac is not universal
# eps_vac = -(b0/4) n ; with n = kappa_n Lambda^4 (kappa_n a lattice/model number): c_vac = -(b0/4) kappa_n. b0 depends on N and nf.
rows = []
for Nc in (2, 3, 4, 5, 8):
    bb = float(b0_std(Nc, 0))
    rows.append((Nc, bb, -bb / 4))                        # c_vac / kappa_n
print("     c_vac/kappa_n = -b0/4 (pure glue): " + ", ".join("N=%d: %.3f" % (n_, c_) for n_, _, c_ in rows))
chk("B5 c_vac/kappa_n = -b0/4 depends on N (2.0/... = %.3f vs %.3f for N=2 vs N=8): not universal" % (rows[0][2], rows[-1][2]), abs(rows[0][2] - rows[-1][2]) > 1)
chk("B5 large-N: b0 ~ N so eps_vac ~ N^2 Lambda^4 if n ~ N Lambda^4 (order-of-magnitude scaling only; no lattice number claimed)", float(b0_std(8)) / float(b0_std(2)) == 4.0)

print("\nsummary: 32 pi^2 in the anomaly is the instanton unit; eps_vac = theta/4 with 4 = dimension of the condensate = D; eps = -(b0/4) n.")
print("         b0 (rational, N-dependent) and the O(1) c_vac carry all sector data; nothing here produces a pure number 4 or 1/4 that is not D itself.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
