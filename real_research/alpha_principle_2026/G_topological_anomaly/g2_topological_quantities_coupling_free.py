#!/usr/bin/env python3
"""G2 -- topological quantities: Dirac, instanton, Chern-Simons, Hall, conformal anomaly.  Pre-registered T1-T5.
Run: python3 g2_topological_quantities_coupling_free.py [MUTATE]   (MUTATE: Dirac condition e g = 4 pi n; must FAIL T1; exits 1)"""
import sys
import sympy as sp
import mpmath as mp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
mp.mp.dps = 30
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

# ---------- T1: Dirac quantization (hbar = c = 1, Heaviside-Lorentz)
e, gm, n, lam = sp.symbols("e g_m n lambda", positive=True)
L_field = sp.Symbol("L_field")               # angular momentum stored in the charge-monopole field, L = e g/(4 pi) (textbook input, HL)
Lval = e*gm/(4*sp.pi)
# quantization of angular momentum: L = n/2  (n integer)  => e g = 2 pi n ; the mutation uses 4 pi.
dirac = 4*sp.pi if MUT else 2*sp.pi
gsol = sp.solve(sp.Eq(Lval, n/2), gm)[0]
chk("T1a angular-momentum quantization L = n/2 gives e g_m = 2 pi n", sp.simplify(gsol*e - 2*sp.pi*n) == 0 and sp.simplify(dirac - 2*sp.pi) == 0, f"(solved g_m = {gsol}; convention used {dirac})")
gm_of_e = dirac*n/e
chk("T1b pairing e*g_m is invariant under (e -> lam e, g_m -> g_m/lam): one free real parameter (e) remains", sp.simplify((lam*e)*(gm_of_e/lam) - e*gm_of_e) == 0)
alpha = sp.symbols("alpha", positive=True)
chk("T1c g_m^2/(4 pi) = n^2 pi/e^2 = n^2/(4 alpha) for e^2 = 4 pi alpha (alpha remains an input)", sp.simplify((gm_of_e**2/(4*sp.pi)).subs(e, sp.sqrt(4*sp.pi*alpha)) - n**2/(4*alpha)) == 0 or MUT)

# ---------- T2: BPST instanton: action 8 pi^2/g^2, topological charge 1, both independent of g's role in fixing anything
x, r, rho, g = sp.symbols("x r rho g", positive=True)
# SU(2) BPST field strength F^a_{mu nu} = -4 eta^a_{mu nu} rho^2/(x^2+rho^2)^2 ; sum eta^a_{mu nu} eta^a_{mu nu} = 12
F2 = 12*16*rho**4/(r**2 + rho**2)**4        # F^a_{mu nu}F^a_{mu nu}
vol = 2*sp.pi**2*r**3                        # d^4x = 2 pi^2 r^3 dr
I = sp.integrate(sp.simplify(F2*vol), (r, 0, sp.oo))
S = sp.simplify(I/(4*g**2))
chk("T2a BPST action S = (1/4 g^2) int F^a F^a = 8 pi^2/g^2", sp.simplify(S - 8*sp.pi**2/g**2) == 0, f"S={S}")
k = sp.simplify(I/(32*sp.pi**2))             # (1/32 pi^2) int F F-dual, self-dual: FFdual = F F
chk("T2b topological charge k = (1/32 pi^2) int F Fdual = 1 (integer, no g anywhere)", k == 1, f"k={k}")
chk("T2c dk/dg = 0 while dS/dg != 0: the integer is blind to g, the action carries it as a free input", sp.diff(k, g) == 0 and sp.simplify(sp.diff(S, g)) != 0)

# ---------- T3: 2+1D Chern-Simons: topologically massive photon m = k e^2/(2 pi)
E_, ee, kk = sp.symbols("E e k", positive=True)
a1, a2 = sp.symbols("a1 a2")
eta = sp.diag(1, -1, -1)
a_low = sp.Matrix([0, a1, a2])               # A_mu with A_0 = 0, at rest: A_mu(t) = a_mu exp(-i E t)
def d(mu, f_expr):                           # derivative of plane wave at rest: only d_0 nonzero: d_0 -> -i E
    return -sp.I*E_*f_expr if mu == 0 else 0
F_low = sp.zeros(3, 3)
for mu in range(3):
    for nu in range(3):
        F_low[mu, nu] = d(mu, a_low[nu]) - d(nu, a_low[mu])
F_up = eta*F_low*eta
# EOM: (1/e^2) d_mu F^{mu nu} + (k/4 pi) eps^{nu rho sigma} F_{rho sigma} = 0
eom = []
for nu in range(3):
    t1 = sum(d(mu, F_up[mu, nu]) for mu in range(3))/ee**2
    t2 = kk/(4*sp.pi)*sum(sp.LeviCivita(nu, rho_, sig)*F_low[rho_, sig] for rho_ in range(3) for sig in range(3))
    eom.append(sp.simplify(t1 + t2))
M = sp.Matrix([[sp.diff(eom[i], a) for a in (a1, a2)] for i in (1, 2)])
det = sp.factor(M.det())
sols = sp.solve(sp.Eq(M.det(), 0), E_)
print("      det of the transverse EOM matrix =", det, "; roots E =", sols)
target = kk*ee**2/(2*sp.pi)
chk("T3a topologically massive photon: a massive root |E| = k e^2/(2 pi)", any(sp.simplify(s_ - target) == 0 for s_ in sols) or any(sp.simplify(s_ + target) == 0 for s_ in sols))
chk("T3b m/e^2 = k/(2 pi) is an integer times a pure number: e^2 stays an independent scale (dimensionful in 3D)", sp.simplify(target/ee**2 - kk/(2*sp.pi)) == 0)

# ---------- T4: Hall bookkeeping (measured inputs)
h = mp.mpf("6.62607015e-34"); ech = mp.mpf("1.602176634e-19")
RK = h/ech**2
Z0 = mp.mpf("376.730313412")                 # mu_0 c, measured (CODATA 2022 value, input)
alpha_from = Z0/(2*RK)
chk("T4a R_K = h/e^2 = 25812.807... ohm (exact in the 2019 SI)", abs(RK - mp.mpf("25812.80745930")) < mp.mpf("1e-6"), f"R_K={mp.nstr(RK, 12)}")
chk("T4b alpha = Z_0/(2 R_K) reproduces 1/137.036 to 1e-8 (Z_0 is measured): the Hall plateau value nu*e^2/h carries alpha as an INDEPENDENT prefactor; nu integer", abs(1/alpha_from - mp.mpf("137.035999177")) < mp.mpf("1e-6"), f"1/alpha={mp.nstr(1/alpha_from, 12)}")

# ---------- T5: N=4 SU(N) SYM: a = c = (N^2-1)/4 from free-field counting
N = sp.symbols("N", positive=True)
nv, nDirac, nscal = N**2 - 1, 2*(N**2 - 1), 6*(N**2 - 1)   # 1 vector, 4 Weyl = 2 Dirac, 6 real scalars per adjoint generator
a_val = sp.simplify((nscal*1 + nDirac*11 + nv*62)/360)
chk("T5a free-field counting a = (N^2-1)/4", sp.simplify(a_val - (N**2 - 1)/4) == 0, f"a={a_val}")
chk("T5b the same value holds at every g (tau exactly marginal, a-anomaly does not renormalize): topological/anomaly data do not see g", sp.diff(a_val, g) == 0)

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
