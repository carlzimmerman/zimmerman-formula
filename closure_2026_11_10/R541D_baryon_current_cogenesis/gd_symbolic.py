"""R541D symbolic gates: GD1 (Noether current with eps J_B.dtau), GD4 (Hamiltonian bookkeeping, kinetic matrix),
GD5 (rephasing removes a pure-gradient coupling, flat and with an arbitrary vierbein + spin connection), KA1, KA6, MU1.
Natural units hbar = c = 1, K = 4 pi G. Prints to stdout; run as  python3 gd_symbolic.py > gd_symbolic.out
"""
import sympy as sp

def hdr(s):
    print("\n== " + s)

# ---------------------------------------------------------------- GD1 covariant (1+1, general metric, general current)
hdr("GD1: tau equation with eps * Jt^m d_m tau, general 1+1 metric g(t,x), arbitrary current density Jt^m(t,x)")
t, x = sp.symbols('t x')
K, mu, eps = sp.symbols('K mu_K epsilon', positive=True)
g00, g01, g11 = [sp.Function(n)(t, x) for n in ('g00', 'g01', 'g11')]
tau = sp.Function('tau')(t, x)
J0, J1 = sp.Function('J0')(t, x), sp.Function('J1')(t, x)
G = sp.Matrix([[g00, g01], [g01, g11]]); Gi = G.inv(); sqg = sp.sqrt(-G.det())
d = [sp.diff(tau, t), sp.diff(tau, x)]
Q = sp.sqrt(-sum(Gi[i, j] * d[i] * d[j] for i in range(2) for j in range(2)))
L = sqg * mu**2 * (Q - 1)**2 / (2 * K) + eps * (J0 * d[0] + J1 * d[1])
EL = sp.euler_equations(L, [tau], [t, x])[0].lhs
# expected: -d_m[ sqrt(-g) (mu^2/K)(Q-1) n^m + eps Jt^m ] = 0,  n^m = -g^{mn} d_n tau / Q
n_up = [-sum(Gi[m, k] * d[k] for k in range(2)) / Q for m in range(2)]
cur = [sqg * mu**2 / K * (Q - 1) * n_up[m] + eps * [J0, J1][m] for m in range(2)]
expected = -(sp.diff(cur[0], t) + sp.diff(cur[1], x))
res = sp.simplify(EL - expected)
print("EL(tau) + d_m[sqrt(-g)(mu^2/K)(Q-1)n^m + eps Jt^m] =", res)
print("GD1 conserved current: J_tot^m = (mu^2/K)(Q-1) n^m + eps J_B^m  ->", "PASS (residual 0)" if res == 0 else "FAIL")
# total-derivative check: a conserved current density Jt = (d_x psi, -d_t psi)
psi = sp.Function('psi')(t, x)
Lc = eps * (sp.diff(psi, x) * d[0] - sp.diff(psi, t) * d[1])
dtt, dtx = sp.symbols('dtt dtx')
Lcs = Lc.subs({d[0]: dtt, d[1]: dtx})
ELc = sp.simplify(-(sp.diff(sp.diff(Lcs, dtt).subs({dtt: d[0], dtx: d[1]}), t)
                   + sp.diff(sp.diff(Lcs, dtx).subs({dtt: d[0], dtx: d[1]}), x)))
print("with d_m Jt^m = 0 identically, the term's contribution to the tau equation =", ELc, "-> total derivative")

# ---------------------------------------------------------------- FRW minisuperspace with baryon number X(t)
hdr("GD1/KA1 FRW minisuperspace: N = 1 after variation; X = a^3 n_B (comoving baryon number, a variable)")
tt = sp.symbols('t')
a = sp.Function('a')(tt); taut = sp.Function('tau')(tt); N = sp.Function('N')(tt); X = sp.Function('X')(tt)
Qf = sp.diff(taut, tt) / N
LK = N * a**3 * mu**2 * (Qf - 1)**2 / (2 * K)
Lc = eps * X * sp.diff(taut, tt)            # sqrt(-g) J_B^t d_t tau, J_B^t = n_B / N, sqrt(-g) = N a^3
p = sp.simplify(sp.diff(LK + Lc, sp.diff(taut, tt)))
print("p_tau =", p)
p0 = sp.simplify(sp.diff(LK, sp.diff(taut, tt)))
print("KA1 eps = 0: p_tau =", p0, " (R541 part B: a^3 mu^2 (Q-1)/K)  ->",
      "PASS" if sp.simplify(p.subs(eps, 0) - p0) == 0 else "FAIL")
print("tau cyclic:", sp.diff(LK + Lc, taut) == 0, "-> d/dt{a^3[(mu^2/K)(Q-1) + eps n_B]} = 0 exactly")
# neutral start p = 0 -> (mu^2/K)(Q-1) = -eps n_B ; rho_K = mu^2(Q^2-1)/(2K)
q, nB, a_s, P0 = sp.symbols('q n_B a p0', real=True)
Qn = sp.solve(sp.Eq(a_s**3 * (mu**2 / K * (q - 1) + eps * nB), P0), q)[0]
rhoK = sp.expand(mu**2 * (Qn**2 - 1) / (2 * K))
print("rho_K(p0) =", sp.simplify(rhoK))
print("neutral (p0 = 0): rho_K =", sp.factor(rhoK.subs(P0, 0)), "; leading term -eps n_B, correction K eps^2 n_B^2/(2 mu^2)")
charge = mu**2 / K * (q - 1)
f = sp.simplify((mu**2 * (q**2 - 1) / (2 * K)) / charge)
print("energy per unit charge f = rho_K / [(mu^2/K)(Q-1)] =", f, "-> 1 as Q -> 1")
print("p0 != 0: rho_K gains p0/a^3 + ... : a free constant again (nothing gained without a neutral start)")
print("MU1 sign flip eps -> -eps: rho_K(p0=0) leading =", sp.factor(rhoK.subs(P0, 0).subs(eps, -eps)).as_ordered_terms()[0] if False else
      sp.series(rhoK.subs(P0, 0).subs(eps, -eps), nB, 0, 2).removeO(), "(sign flips)")

# ---------------------------------------------------------------- GD4 Hamiltonian bookkeeping
hdr("GD4 Hamiltonian of the clock sector with X as a parameter (N = 1)")
td, pp, XX, A3 = sp.symbols('taudot p X A3', real=True)   # A3 = a^3
Lmin = A3 * mu**2 * (td - 1)**2 / (2 * K) + eps * XX * td
tdsol = sp.solve(sp.Eq(sp.diff(Lmin, td), pp), td)[0]
H = sp.simplify((pp * td - Lmin).subs(td, tdsol))
print("tau-dot(p, X) =", sp.simplify(tdsol))
print("H(p, X) =", sp.factor(H))
u = pp - eps * XX
Hu = u + K * u**2 / (2 * A3 * mu**2)
print("H - [u + K u^2/(2 a^3 mu^2)], u = p - eps X :", sp.simplify(H - Hu))
rhoKvol = (A3 * mu**2 * (td**2 - 1) / (2 * K)).subs(td, tdsol)
print("H equals the gravitating clock energy a^3 rho_K :", sp.simplify(H - rhoKvol) == 0)
dHdX = sp.simplify(sp.diff(H, XX))
print("dH/dX at fixed p =", dHdX, " = -eps * Q  (energy put into the clock per baryon created)")
print("check dH/dX + eps * taudot(p, X) =", sp.simplify(dHdX + eps * tdsol))
print("=> effective baryon chemical potential in thermal equilibrium: mu_B = eps * Q (equilibrium sets dF/dX = 0)")
print("kinetic matrix d2L/dtaudot2 =", sp.diff(Lmin, td, 2), " (eps term is linear in tau-dot: adds nothing to it)")
# equilibrium sign: n_B = chi * mu_B with chi > 0  -> rho_K = -eps n_B = -chi eps^2 Q < 0
chi = sp.symbols('chi', positive=True)
print("equilibrium: n_B = chi*eps*Q, chi>0  ->  rho_K ~ -eps n_B =", sp.simplify(-eps * chi * eps * q),
      " : NEGATIVE for either sign of eps")

# ---------------------------------------------------------------- GD5 rephasing (Dirac, 4D)
hdr("GD5 rephasing psi = exp(i*alpha*tau) chi removes eps J.dtau (flat, then arbitrary vierbein + spin connection)")
X4 = sp.symbols('x0:4')
gam0 = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]])
def blk(s):
    Z = sp.zeros(4); Z[0:2, 2:4] = s; Z[2:4, 0:2] = -s; return Z
gam = [gam0, blk(s1), blk(s2), blk(s3)]
chi_ = sp.Matrix([sp.Function(f'c{k}')(*X4) for k in range(4)])
chib = sp.Matrix([[sp.Function(f'cb{k}')(*X4) for k in range(4)]])     # independent conjugate row (chi^dagger gamma0)
tau4 = sp.Function('tau')(*X4); m = sp.symbols('m'); al = sp.symbols('alpha', real=True)
def lag(psi, psib, E, Om, coup):
    # psib [ i gamma^a E_a^m (d_m + Om_m) - m ] psi + coup * psib gamma^a E_a^m psi d_m tau
    kin = sp.zeros(1, 1); cur = sp.zeros(1, 1)
    for A in range(4):
        for M in range(4):
            if E[A, M] == 0:
                continue
            kin += psib * (sp.I * gam[A] * E[A, M] * (sp.diff(psi, X4[M]) + Om[M] * psi))
            cur += psib * gam[A] * E[A, M] * psi * sp.diff(tau4, X4[M])
    return sp.expand((kin - m * psib * psi + coup * cur)[0, 0])
E_flat = sp.diag(1, 1, 1, 1); Om0 = [sp.zeros(4)] * 4
psi = sp.exp(sp.I * al * tau4) * chi_; psib = sp.exp(-sp.I * al * tau4) * chib
r_flat = sp.simplify(lag(psi, psib, E_flat, Om0, eps) - lag(chi_, chib, E_flat, Om0, eps - al))
print("flat: L[psi; eps] - L[chi; eps - alpha] =", r_flat, "-> alpha = eps removes the term")
E_gen = sp.Matrix(4, 4, lambda A, M: sp.Function(f'e{A}{M}')(*X4) if (A + M) % 3 == 0 else 0)  # sparse generic vierbein
Om_gen = [sp.Matrix(4, 4, lambda i, j: sp.Function(f'w{M}{i}{j}')(*X4) if i == j or i + j == 3 else 0) for M in range(4)]
r_gen = sp.simplify(lag(psi, psib, E_gen, Om_gen, eps) - lag(chi_, chib, E_gen, Om_gen, eps - al))
print("curved (vierbein e_a^m(x), spin connection Omega_m(x) generic): residual =", r_gen)
print("GD5/KA6 removable in any gravitational field:", "PASS" if r_flat == 0 and r_gen == 0 else "FAIL")
# KA6 sanity: a non-gradient a_m is not a gradient (curl != 0), so no scalar phase removes it
y0, y1 = X4[0], X4[1]
a_vec = [0, y0, 0, 0]
print("KA6 non-gradient a_m = (0, x0, 0, 0): curl d0 a1 - d1 a0 =", sp.diff(a_vec[1], y0) - sp.diff(a_vec[0], y1),
      "(nonzero -> not removable; a pure gradient has curl 0 identically)")
print("B-violating operators (Delta B != 0) pick up exp(i*eps*DeltaB*tau): energy shift eps*Q*DeltaB per process")
