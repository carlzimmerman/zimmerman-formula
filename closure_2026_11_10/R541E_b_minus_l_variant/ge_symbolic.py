"""R541E symbolic gates: algebra re-check with J_X (X = B-L), GE6 rephasing for two species of different B-L charge
(flat and generic vierbein + spin connection) with an X-conserving and an X-violating interaction, anomaly sums
(KA5), MU6. Natural units, K = 4 pi G. Run:  python3 ge_symbolic.py > ge_symbolic.out
Adapted from R541D's gd_symbolic.py (copied, not edited in place).
"""
import sympy as sp
from fractions import Fraction as Fr

def hdr(s):
    print("\n== " + s)

# ---------------------------------------------------------------- FRW minisuperspace with X = a^3 n_(B-L)
hdr("Algebra with J_X, X = B-L: conserved total, Hamiltonian, bias (R541D GD1/GD4 with B -> B-L)")
t = sp.symbols('t')
K, mu, eps = sp.symbols('K mu_K epsilon', positive=True)
a = sp.Function('a')(t); tau = sp.Function('tau')(t); N = sp.Function('N')(t); X = sp.Function('X')(t)
Qf = sp.diff(tau, t) / N
L = N * a**3 * mu**2 * (Qf - 1)**2 / (2 * K) + eps * X * sp.diff(tau, t)
p = sp.simplify(sp.diff(L, sp.diff(tau, t)))
print("p_tau =", p, "; tau cyclic:", sp.diff(L, tau) == 0)
td, pp, XX, A3 = sp.symbols('taudot p X A3', real=True)
Lm = A3 * mu**2 * (td - 1)**2 / (2 * K) + eps * XX * td
tds = sp.solve(sp.Eq(sp.diff(Lm, td), pp), td)[0]
H = sp.simplify((pp * td - Lm).subs(td, tds))
print("H - [u + K u^2/(2 a^3 mu^2)], u = p - eps X :", sp.simplify(H - ((pp - eps*XX) + K*(pp - eps*XX)**2/(2*A3*mu**2))))
print("dH/dX + eps * taudot =", sp.simplify(sp.diff(H, XX) + eps * tds), " -> bias mu_X = eps Q")
nn, T, chi = sp.symbols('n T chi', positive=True)
F = nn**2 / (2 * chi * T**2) - eps * nn + K * eps**2 * nn**2 / (2 * mu**2)      # p = 0, per volume
neq = sp.solve(sp.diff(F, nn), nn)[0]
print("equilibrium with the clock's quadratic energy (p = 0): n_X =", sp.simplify(neq))
rho = sp.simplify((-eps * nn + K * eps**2 * nn**2 / (2 * mu**2)).subs(nn, neq))
print("rho_K at that equilibrium =", sp.factor(rho), " (negative: numerator", sp.factor(sp.numer(sp.together(rho))), ")")

# ---------------------------------------------------------------- GE6 rephasing, two species
hdr("GE6 rephasing psi_i = exp(i eps X_i tau) chi_i, quark-like X = 1/3 and lepton-like X = -1")
X4 = sp.symbols('x0:4')
g0 = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]])
def blk(s):
    Z = sp.zeros(4); Z[0:2, 2:4] = s; Z[2:4, 0:2] = -s; return Z
gam = [g0, blk(s1), blk(s2), blk(s3)]
tau4 = sp.Function('tau')(*X4); m = sp.symbols('m')
def lag(psi, psib, E, Om, coup):
    kin = sp.zeros(1, 1); cur = sp.zeros(1, 1)
    for A_ in range(4):
        for M in range(4):
            if E[A_, M] == 0:
                continue
            kin += psib * (sp.I * gam[A_] * E[A_, M] * (sp.diff(psi, X4[M]) + Om[M] * psi))
            cur += psib * gam[A_] * E[A_, M] * psi * sp.diff(tau4, X4[M])
    return sp.expand((kin - m * psib * psi + coup * cur)[0, 0])
E_flat = sp.diag(1, 1, 1, 1); Om0 = [sp.zeros(4)] * 4
E_gen = sp.Matrix(4, 4, lambda A_, M: sp.Function(f'e{A_}{M}')(*X4) if (A_ + M) % 3 == 0 else 0)
Om_gen = [sp.Matrix(4, 4, lambda i, j: sp.Function(f'w{M}{i}{j}')(*X4) if i == j or i + j == 3 else 0) for M in range(4)]
charges = {"q": sp.Rational(1, 3), "l": -1}
fields = {}
ok = True
for nm, qx in charges.items():
    chi_ = sp.Matrix([sp.Function(f'{nm}c{k}')(*X4) for k in range(4)])
    chib = sp.Matrix([[sp.Function(f'{nm}b{k}')(*X4) for k in range(4)]])
    al = eps * qx
    psi = sp.exp(sp.I * al * tau4) * chi_; psib = sp.exp(-sp.I * al * tau4) * chib
    fields[nm] = (chi_, chib, psi, psib)
    for lab, E, Om in (("flat", E_flat, Om0), ("generic vierbein + spin connection", E_gen, Om_gen)):
        r = sp.simplify(lag(psi, psib, E, Om, eps * qx) - lag(chi_, chib, E, Om, 0))
        print(f"species {nm} (X = {qx}), {lab}: L[psi; eps X] - L[chi; 0] = {r}")
        ok = ok and r == 0
# interactions: phase picked up by a product of fields carrying net X
cq, cqb, pq, pqb = fields["q"]; cl, clb, pl, plb = fields["l"]
cons = pq[0] * pq[1] * pq[2] * pl[3]             # qqq l : X = 1 - 1 = 0 (Delta(B-L) = 0, like p -> e+ pi0)
viol = pq[0] * pq[1] * pq[2] * plb[0, 3]          # qqq lbar : X = 1 + 1 = 2 (Delta(B-L) = 2, like p -> nu pi+)
rc = sp.simplify(cons / (cq[0] * cq[1] * cq[2] * cl[3]))
rv = sp.simplify(viol / (cq[0] * cq[1] * cq[2] * clb[0, 3]))
print("X-conserving qqql term picks up phase:", rc, " (removed)")
print("MU6 X-violating qqq lbar term picks up phase:", rv, " (kept: exp(2 i eps tau) -> GE4)")
mnu = sp.Function('nu')(*X4)
print("Majorana mass (m/2) nu nu (lepton X = -1 each) picks up:", sp.simplify((sp.exp(-sp.I*eps*tau4)*mnu)**2 / mnu**2))
print("GE6/KA5 rephasing removes eps J_(B-L).dtau from every X-conserving term in any gravitational field:",
      "PASS" if ok and rc == 1 else "FAIL")
x0, x1 = X4[0], X4[1]
print("KA5 sanity: a non-gradient a_m = (0, x0, 0, 0) has curl", sp.diff(x0, x0) - sp.diff(0, x1), "(not removable)")

# ---------------------------------------------------------------- anomaly sums, exact
hdr("KA5 anomalies (left-handed Weyl fields per generation, conjugates for right-handed): exact fractions")
# (name, SU(2) dim, colour dim, Y, B, L)
LH = [("Q", 2, 3, Fr(1, 6), Fr(1, 3), 0), ("u^c", 1, 3, Fr(-2, 3), Fr(-1, 3), 0), ("d^c", 1, 3, Fr(1, 3), Fr(-1, 3), 0),
      ("L", 2, 1, Fr(-1, 2), 0, 1), ("e^c", 1, 1, Fr(1), 0, -1)]
NUC = ("nu^c", 1, 1, Fr(0), 0, -1)
def sums(withnu, chg):
    fl = LH + ([NUC] if withnu else [])
    c = lambda f: chg(f[4], f[5])
    su2 = sum(Fr(1, 2) * f[2] * c(f) for f in fl if f[1] == 2)     # T(fund) = 1/2, colour multiplicity
    yy = sum(f[1] * f[2] * f[3] ** 2 * c(f) for f in fl)
    gr = sum(f[1] * f[2] * c(f) for f in fl)
    return su2, yy, gr
for lab, chg in (("B-L", lambda B, L: B - L), ("B", lambda B, L: B), ("L", lambda B, L: L)):
    for wn in (False, True):
        s = sums(wn, chg)
        print(f"{lab:3s} nu_R {'with' if wn else 'w/o '}: SU(2)^2 X = {s[0]}, Y^2 X = {s[1]}, grav X = {s[2]}  (per generation)")
s_bl = sums(True, lambda B, L: B - L); s_bl0 = sums(False, lambda B, L: B - L); s_b = sums(True, lambda B, L: B)
print("KA5: B-L anomaly-free with nu_R:", s_bl == (0, 0, 0), "; grav(B-L) without nu_R = 3 x", s_bl0[2], "=", 3 * s_bl0[2],
      "; SU(2)^2 B nonzero:", s_b[0] != 0)
