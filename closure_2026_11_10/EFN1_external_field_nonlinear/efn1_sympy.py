"""EFN1 known answer KA-a (criteria 98364c8d20): the nonlinear Newtonian-order equations of action (A) at mu_K = 0,
gamma_L = 0, n_d = 0, and their linearisation against SCS1's quadratic Lagrangian L2 and SCS3's route-L symbol.

(i)   the leaf lapse: ln N_tau = eps (Phi - pi_t + |grad pi|^2/2) + O(eps^2), from -g^{mn} d_m tau d_n tau with
      tau = t + pi, pi ~ eps^1/2, d_t ~ eps^1/2 d_x (Newtonian gauge, psi kept separate to show it drops out at this order);
(ii)  Euler-Lagrange equations of L = -|grad Phi|^2/(2K) - rho Phi + j(|grad S|^2) (j generic), and the identities
      E_pi = -d_t N + div(N grad pi), E_Phi = lap Phi/K - rho - N, with N = div P, P = 2 j'(Y) grad S;
(iii) the linearisation about the static state (pi = 0, Phi = Phi0(x)) against the Euler-Lagrange equations of
      L2 = -|grad phi|^2/(2K) + (1/2) grad chi . J'' . grad chi + Pbar . grad(|grad pi|^2)/2, chi = phi - pi_t;
(iv)  the constant-coefficient symbol: omega^2 = G (1 - K m)/m;
(v)   order counting of the dropped multiplier flux lambda P / Q against the advective flux N v.
Every residual must be exactly 0.  Writes efn1_sympy.out / .json next to this file.
"""
import os, json
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P_(s):
    print(s, flush=True); OUT.append(str(s))
RES = {}

# ---------------------------------------------------------------- (i) lapse
eps = sp.symbols('epsilon', positive=True)
Phi_, Psi_, pT, px, py, pz = sp.symbols('Phi Psi p_T p_x p_y p_z', real=True)
# tau = t + eps^(1/2) p(T, x), T = eps^(1/2) t:  d_t tau = 1 + eps p_T,  d_i tau = eps^(1/2) p_i
gtt_inv = -1 / (1 + 2 * eps * Phi_)
gij_inv = 1 / (1 - 2 * eps * Psi_)
X = -(gtt_inv * (1 + eps * pT) ** 2 + gij_inv * eps * (px ** 2 + py ** 2 + pz ** 2))
lnN = -sp.log(X) / 2
ser = sp.series(lnN, eps, 0, 2).removeO()
first = sp.simplify(ser.coeff(eps, 1))
target = Phi_ - pT + (px ** 2 + py ** 2 + pz ** 2) / 2
r1 = sp.simplify(first - target)
P_(f"(i) lapse: order-eps coefficient of ln N_tau = {first};  residual against Phi - pi_t + |grad pi|^2/2: {r1}")
P_(f"    order eps^0 term: {sp.simplify(ser.coeff(eps, 0))} (psi enters only at order eps^2)")
RES["i_lapse_residual"] = str(r1)

# ---------------------------------------------------------------- (ii) Euler-Lagrange equations
t, x, y, z = sp.symbols('t x y z', real=True)
K = sp.symbols('K', positive=True)
DIM = int(os.environ.get('EFN1_DIM', '3'))
co = (x, y, z)[:DIM]
Phi = sp.Function('Phi')(t, *co)
pi = sp.Function('pi')(t, *co)
rho = sp.Function('rho')(*co)
j = sp.Function('j')
DJ = {k_: sp.Function(f'jd{k_}') for k_ in range(1, 5)}
def canon(e):
    """evaluate Derivative(0, .) and write Subs(d^k j(xi)/dxi^k, xi, E) as jd_k(E), so equal terms compare equal"""
    e = e.doit()
    def rep(a):
        ex = a.expr
        if isinstance(ex, sp.Derivative) and ex.expr.func == j:
            return DJ[ex.derivative_count](a.point[0])
        return a
    e = e.replace(lambda a: isinstance(a, sp.Subs), rep)
    e = e.replace(lambda a: isinstance(a, sp.Derivative) and a.expr.func == j and len(a.variables) > 0
                  and a.expr.args[0] in a.variables, lambda a: DJ[a.derivative_count](a.expr.args[0]))
    return sp.expand(e.doit())
grad = lambda f: [sp.diff(f, c) for c in co]
div = lambda F: sum(sp.diff(Fc, c) for Fc, c in zip(F, co))
S = Phi - sp.diff(pi, t) + sum(gp ** 2 for gp in grad(pi)) / 2
Aa = grad(S)
Y = sum(a ** 2 for a in Aa)
L = -sum(g ** 2 for g in grad(Phi)) / (2 * K) - rho * Phi + j(Y)
EL = euler_equations(L, [Phi, pi], [t, *co])
E_Phi = EL[0].lhs
E_pi = EL[1].lhs
jp = sp.Subs(sp.Derivative(j(sp.Symbol('Y_')), sp.Symbol('Y_')), sp.Symbol('Y_'), Y).doit()
Pvec = [2 * jp * a for a in Aa]
N = div(Pvec)
id_phi = canon(E_Phi - (div(grad(Phi)) / K - rho - N))
id_pi = canon(E_pi - (-sp.diff(N, t) + div([N * gp for gp in grad(pi)])))
P_(f"(ii) [dimension {DIM}] E_Phi - [lap Phi/K - rho - div P] = {id_phi}")
P_(f"(ii) E_pi  - [-d_t N + div(N grad pi)] = {id_pi}")
RES["ii_E_Phi_residual"] = str(id_phi); RES["ii_E_pi_residual"] = str(id_pi)

# ---------------------------------------------------------------- (iii) linearisation against SCS1's L2
d = sp.symbols('delta')
Phi0 = sp.Function('Phi0')(*co)
phi1 = sp.Function('phi1')(t, *co)
pi1 = sp.Function('pi1')(t, *co)
sub = {Phi: Phi0 + d * phi1, pi: d * pi1}
def lin(E):
    e = E.subs(sub).doit()
    return canon(sp.diff(e, d).subs(d, 0))
lin_phi = lin(E_Phi); lin_pi = lin(E_pi)
# L2 with Jbar = j(|grad Phi0|^2): P-bar = dJ/dA at A0, J'' = d2J/dA dA at A0, written from j
A0 = grad(Phi0)
Ys = sp.Symbol('Y_')
j1 = sp.diff(j(Ys), Ys).subs(Ys, sum(a ** 2 for a in A0))
j2 = sp.diff(j(Ys), Ys, 2).subs(Ys, sum(a ** 2 for a in A0))
Pbar = [2 * j1 * a for a in A0]
Jpp = [[2 * j1 * (1 if i == k else 0) + 4 * j2 * A0[i] * A0[k] for k in range(DIM)] for i in range(DIM)]
chi = phi1 - sp.diff(pi1, t)
gchi = grad(chi)
L2 = (-sum(g ** 2 for g in grad(phi1)) / (2 * K)
      + sp.Rational(1, 2) * sum(gchi[i] * Jpp[i][k] * gchi[k] for i in range(DIM) for k in range(DIM))
      + sum(Pbar[i] * sp.diff(sum(gp ** 2 for gp in grad(pi1)), co[i]) for i in range(DIM)) / 2)
EL2 = euler_equations(L2, [phi1, pi1], [t, *co])
# the background equation is used: lap Phi0/K - rho - div Pbar = 0 (static E_Phi); its terms do not appear at order delta
r_phi = canon(lin_phi - canon(EL2[0].lhs))
r_pi = canon(lin_pi - canon(EL2[1].lhs))
P_(f"(iii) linearised E_Phi minus EL of SCS1's L2 (phi): {r_phi}")
P_(f"(iii) linearised E_pi  minus EL of SCS1's L2 (pi):  {r_pi}")
RES["iii_phi_residual"] = str(r_phi); RES["iii_pi_residual"] = str(r_pi)

# ---------------------------------------------------------------- (iv) symbol omega^2 = G (1 - K m)/m
w, k1, k2, k3, Gs = sp.symbols('omega k1 k2 k3 G', real=True)
J = sp.Matrix(3, 3, lambda i, k: sp.Symbol(f'J{min(i, k)}{max(i, k)}'))
kv = sp.Matrix([k1, k2, k3]); kk = (kv.T * kv)[0]; m = (kv.T * J * kv)[0] / kk
ph, pp = sp.symbols('phihat pihat')
chih = ph + sp.I * w * pp                                   # chi = phi - pi_t with e^{i k.x - i omega t}
# constant-coefficient linear equations (E_Phi lin, E_pi lin with N0 = G): -k^2 phi/K + (k.J.k) chi = 0 ;
# -d_t n + G lap pi = 0, n = div(J grad chi) = -(k.J.k) chi
eq1 = -kk * ph / K + (kv.T * J * kv)[0] * chih
n_h = -(kv.T * J * kv)[0] * chih
eq2 = sp.I * w * n_h - Gs * kk * pp
Mx = sp.Matrix([[sp.diff(e, v) for v in (ph, pp)] for e in (eq1, eq2)])
cand = [sp.simplify(s_) for s_ in sp.solve(sp.Eq(Mx.det(), 0), w)]
w2s = sorted(set(sp.simplify(c_ ** 2) for c_ in cand), key=str)
r4 = [sp.simplify(c_ - Gs * (1 - K * m) / m) for c_ in w2s]
P_(f"(iv) roots omega^2 of the symbol: {w2s};  minus G (1 - K m)/m: {r4}")
RES["iv_symbol_residual"] = [str(r_) for r_ in r4]
# along / across the field for K J = a0 A - a0^2 ln(1 + A/a0): K J'' = 1/(1+u)^2 along, K J'/A = 1/(1+u) across
a0, A = sp.symbols('a0 A', positive=True)
KJ = a0 * A - a0 ** 2 * sp.log(1 + A / a0)
along = sp.simplify(sp.diff(KJ, A, 2) - 1 / (1 + A / a0) ** 2)
across = sp.simplify(sp.diff(KJ, A) / A - 1 / (1 + A / a0))
u = sp.symbols('u', positive=True)
lean = sp.simplify((1 - 1 / (1 + u) ** 2) / (1 / (1 + u) ** 2) - u * (2 + u))
P_(f"(iv) K J'' - 1/(1+u)^2 = {along};  K J'/A - 1/(1+u) = {across};  (1 - Km)/(Km) - u(2+u) along = {lean}")
RES["iv_law_residuals"] = [str(along), str(across), str(lean)]

# ---------------------------------------------------------------- (v) order counting of the multiplier flux
# lambda = n.d ln N ~ d_t S ~ eps^(1/2) * eps / L ; P ~ eps (K P ~ A ~ eps/L) ; N = div P ~ eps ; v = -grad pi ~ eps^(1/2)
order_lamP = sp.Rational(1, 2) + 1 + 1
order_Nv = 1 + sp.Rational(1, 2)
P_(f"(v) lambda P/Q ~ eps^{order_lamP}, N v ~ eps^{order_Nv}: ratio eps^{order_lamP - order_Nv} (dropped, 1PN)")
RES["v_order_ratio"] = str(order_lamP - order_Nv)

zero = (r1 == 0 and id_phi == 0 and id_pi == 0 and r_phi == 0 and r_pi == 0 and all(r_ == 0 for r_ in r4)
        and along == 0 and across == 0 and lean == 0)
RES["KA_a_pass"] = bool(zero)
P_(f"KA-a: {'PASS' if zero else 'FAIL'} (every residual exactly 0: {zero})")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
RES["dimension"] = DIM
suf = "" if DIM == 3 else f"_dim{DIM}"
json.dump(RES, open(os.path.join(HERE, f"efn1_sympy{suf}.json"), "w"), indent=1)
open(os.path.join(HERE, f"efn1_sympy{suf}.out"), "w").write("\n".join(OUT) + "\n")
