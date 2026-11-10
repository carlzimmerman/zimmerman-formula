"""TK1 A1: well-posedness of the theta-keyed dust term (criteria 98f2ab2b6e).

K1  covariant khronon current vs direct Euler-Lagrange variation (1+1, diagonal metric, jet variables via sympy).
K2  unitary gauge: theta = K (extrinsic-curvature trace) with lapse and shift; velocities theta depends on;
    velocity Hessian of EH + F(Q, K) on the isotropic sector: trace eigenvalue.
K3  principal part of the khronon equation (4th-order coefficients) vs F_thth (h xi xi)^2 / Q^2.
KA2 minisuperspace identity E + N L_N = -a^3 F_Q, Friedmann form of the N-equation.
KA3 M_2 constant -> rho_K = n + K n^2/(2 M^2).
KA4 lambda-term -> G_cosmo = G/(1 + 3 lambda/2).
K4  scalar quadratic action around flat FRW in unitary gauge (gravity + clock + Lambda), auxiliary fields eliminated:
    kinetic coefficient A_z and gradient coefficient at high k, as closed forms in F's derivatives.
Env TK1_MUTATE = MU1 (drop theta F_theta in rho_K) | MU3 (drop F_thth in K4).
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time
import sympy as sp

MUT = os.environ.get("TK1_MUTATE", "")
out = {"mutate": MUT}
T0 = time.time()
def say(*a):
    print(*a, flush=True)

t, x = sp.symbols("t x", real=True)
Kg = sp.symbols("K", positive=True)

# ---------------------------------------------------------------- K1
say("== K1: covariant current vs Euler-Lagrange (1+1, metric -e^{2A}dt^2 + e^{2B}dx^2), jet variables")
A = sp.Function("A")(t, x); B = sp.Function("B")(t, x); tau = sp.Function("tau")(t, x)
m0, m2, m4 = sp.symbols("m0 m2 m4")
def Ffun(Q, th):
    return (Q - 1)**2 * (m0 + m2*th**2 + m4*th**4)
X = [t, x]
# jet symbols for tau and for the metric functions (values and first derivatives)
p_t, p_x, p_tt, p_tx, p_xx = sp.symbols("p_t p_x p_tt p_tx p_xx")
Av, At, Ax, Bv, Bt, Bx = sp.symbols("Av At Ax Bv Bt Bx")
jet_tau = {sp.Derivative(tau, t): p_t, sp.Derivative(tau, x): p_x, sp.Derivative(tau, t, t): p_tt,
           sp.Derivative(tau, t, x): p_tx, sp.Derivative(tau, x, x): p_xx}
def build_L(Avv, Att, Axx, Bvv, Btt, Bxx):
    ginv00, ginv11 = -sp.exp(-2*Avv), sp.exp(-2*Bvv)
    sqg_ = sp.exp(Avv + Bvv)
    Q_ = sp.sqrt(-(ginv00*p_t**2 + ginv11*p_x**2))
    # theta = (1/sqg) d_m (sqg g^{mm} n_m), n_m = -p_m/Q; expand d_m with jets
    def dm(expr, m):  # total derivative of an expression of jets (first-order jets and metric)
        if m == 0:
            return (sp.diff(expr, p_t)*p_tt + sp.diff(expr, p_x)*p_tx + sp.diff(expr, Avv)*Att + sp.diff(expr, Bvv)*Btt)
        return (sp.diff(expr, p_t)*p_tx + sp.diff(expr, p_x)*p_xx + sp.diff(expr, Avv)*Axx + sp.diff(expr, Bvv)*Bxx)
    nu0 = ginv00*(-p_t/Q_); nu1 = ginv11*(-p_x/Q_)
    th_ = (dm(sqg_*nu0, 0) + dm(sqg_*nu1, 1))/sqg_
    return sqg_, Q_, th_, nu0, nu1
sqg_j, Q_j, th_j, nu0_j, nu1_j = build_L(Av, At, Ax, Bv, Bt, Bx)
L_j = sqg_j*Ffun(Q_j, th_j)
dL = {s_: sp.diff(L_j, s_) for s_ in (p_t, p_x, p_tt, p_tx, p_xx)}
qs, ths = sp.symbols("qs ths")
FQ_j = sp.diff(Ffun(qs, ths), qs).subs({qs: Q_j, ths: th_j})
Fth_j = sp.diff(Ffun(qs, ths), ths).subs({qs: Q_j, ths: th_j})
Fthth_j = sp.diff(Ffun(qs, ths), ths, 2).subs({qs: Q_j, ths: th_j})
import random
# full jet space: tau derivatives up to order 4, A and B up to order 3; total derivative operators D_t, D_x
from itertools import product
def jname(base, i, j):
    return sp.Symbol("%s_%d_%d" % (base, i, j))
TJ = {(i, j): jname("T", i, j) for i in range(5) for j in range(5) if 1 <= i + j <= 4}
AJ = {(i, j): jname("A", i, j) for i in range(4) for j in range(4) if i + j <= 3}
BJ = {(i, j): jname("B", i, j) for i in range(4) for j in range(4) if i + j <= 3}
to_full = {p_t: TJ[(1, 0)], p_x: TJ[(0, 1)], p_tt: TJ[(2, 0)], p_tx: TJ[(1, 1)], p_xx: TJ[(0, 2)],
           Av: AJ[(0, 0)], At: AJ[(1, 0)], Ax: AJ[(0, 1)], Bv: BJ[(0, 0)], Bt: BJ[(1, 0)], Bx: BJ[(0, 1)]}
def Dtot(expr, d):
    res = 0
    for J_, lim in ((TJ, 4), (AJ, 3), (BJ, 3)):
        for (i, j), sym in J_.items():
            if not expr.has(sym):
                continue
            nxt = (i + 1, j) if d == 0 else (i, j + 1)
            if nxt not in J_:
                raise ValueError("jet order exceeded")
            res += sp.diff(expr, sym)*J_[nxt]
    return res
parv = {m0: sp.Rational(3, 7), m2: sp.Rational(-5, 11), m4: sp.Rational(2, 13)}
dLf = {k_: v_.subs(parv).subs(to_full) for k_, v_ in dL.items()}
ELj = (-Dtot(dLf[p_t], 0) - Dtot(dLf[p_x], 1) + Dtot(Dtot(dLf[p_tt], 0), 0) + Dtot(Dtot(dLf[p_tx], 0), 1)
       + Dtot(Dtot(dLf[p_xx], 1), 1))
say("  EL built in jets %.0f s" % (time.time() - T0))
sqg_f = sqg_j.subs(to_full); Q_f = Q_j.subs(to_full)
nup_f = [nu0_j.subs(to_full), nu1_j.subs(to_full)]
ginv_f = [-sp.exp(-2*AJ[(0, 0)]), sp.exp(-2*BJ[(0, 0)])]
FQ_f = FQ_j.subs(parv).subs(to_full); Fth_f = Fth_j.subs(parv).subs(to_full)
hup_f = [[(ginv_f[i] if i == j else 0) + nup_f[i]*nup_f[j] for j in range(2)] for i in range(2)]
Jf = [FQ_f*nup_f[k_] + sum(hup_f[k_][m_]*Dtot(Fth_f, m_) for m_ in range(2))/Q_f for k_ in range(2)]
divJ = Dtot(sqg_f*Jf[0], 0) + Dtot(sqg_f*Jf[1], 1)
say("  div J built %.0f s" % (time.time() - T0))
k1_res = []
rr = random.Random(3)
allsyms = sorted((ELj + divJ).free_symbols | ELj.free_symbols, key=str)
fEL = sp.lambdify(allsyms, ELj, "mpmath"); fRes = sp.lambdify(allsyms, ELj + divJ, "mpmath")
say("  lambdified %.0f s" % (time.time() - T0))
import mpmath as mpm
mpm.mp.dps = 40
for trial in range(6):
    vals = {}
    for J_ in (TJ, AJ, BJ):
        for key_, sym in J_.items():
            vals[sym] = mpm.mpf(rr.randint(-9, 9))/rr.randint(4, 13)
    vals[TJ[(1, 0)]] = mpm.mpf(rr.randint(25, 45))/9   # timelike gradient
    vals[TJ[(0, 1)]] = mpm.mpf(rr.randint(-5, 5))/9
    args = [vals.get(s_, 0) for s_ in allsyms]
    rv = fRes(*args); sv = fEL(*args)
    k1_res.append(float(abs(rv)/max(abs(sv), mpm.mpf("1e-30"))))
say("  K1 relative residuals |EL + d_k(sqrt(-g) J^k)| / |EL| at 6 random jets (40 digits):", ["%.1e" % r for r in k1_res])
out["K1_residuals"] = k1_res
# order: EL contains 4th jets of tau (and not 5th: by construction of the jet space)
out["K1_EL_has_4th_jets"] = any(ELj.has(TJ[k_]) for k_ in TJ if sum(k_) == 4)

# ---------------------------------------------------------------- K3 principal part
say("== K3: principal part of the khronon equation")
# For a Lagrangian of second-order jets, the 4th-order part of EL is sum d2L/dp_ab dp_cd d_abcd tau:
# symbol P(xi) = sum_{ab,cd} L_{ab,cd} xi_a xi_b xi_c xi_d  (p_tx counted with its multiplicity).
xi0, xi1 = sp.symbols("xi0 xi1")
mono = {p_tt: xi0**2, p_tx: xi0*xi1, p_xx: xi1**2}
symb = sum(sp.diff(L_j, a1, b1)*mono[a1]*mono[b1] for a1 in mono for b1 in mono)
ginv_j = [-sp.exp(-2*Av), sp.exp(-2*Bv)]
nup_j = [nu0_j, nu1_j]
hxx = sum(((ginv_j[a1] if a1 == b1 else 0) + nup_j[a1]*nup_j[b1])*[xi0, xi1][a1]*[xi0, xi1][b1]
          for a1 in range(2) for b1 in range(2))
hand = sqg_j*Fthth_j*hxx**2/Q_j**2
rr = random.Random(7)
k3 = []
for _ in range(6):
    vals = {s_: sp.Rational(rr.randint(-9, 9), rr.randint(3, 11)) for s_ in (p_x, p_tt, p_tx, p_xx, Av, At, Ax, Bv, Bt, Bx, xi0, xi1)}
    vals[p_t] = sp.Rational(rr.randint(20, 40), 7)  # timelike gradient
    vals.update(parv)
    a_ = sp.N(symb.subs(vals), 30); b_ = sp.N(hand.subs(vals), 30)
    k3.append(float(a_/b_))
    say("   K3 trial done %.0f s" % (time.time() - T0))
say("  symbol / [sqrt(-g) F_thth (h xi xi)^2 / Q^2] at 6 random jets:", ["%.15f" % r for r in k3])
out["K3_symbol_ratio"] = k3
out["K3_max_order"] = 4
out["K3_note"] = ("principal symbol = sqrt(-g) F_thth (h^ab xi_a xi_b)^2 / Q^2 (ratio printed): it vanishes only for xi "
                  "along n, so the 4th-order part acts within the leaves (an instantaneous, leaf-elliptic mode, no new "
                  "propagating cone); its coefficient changes sign where F_thth = 0 (type change)")

# ---------------------------------------------------------------- K2 unitary gauge (1+1 with lapse and shift)
say("== K2: unitary gauge (tau = t), lapse N, shift, spatial metric gam")
N = sp.Function("N")(t, x); Nx = sp.Function("Nx")(t, x); gam = sp.Function("gam")(t, x)
g = sp.Matrix([[-N**2 + Nx**2/gam, Nx], [Nx, gam]])
gi = sp.simplify(g.inv())
sqg2 = N*sp.sqrt(gam)
tauU = t
dtU = [sp.Integer(1), sp.Integer(0)]
QU = sp.sqrt(-gi[0, 0])
nlo = [-dtU[i]/QU for i in range(2)]
nup = [sum(gi[i, j]*nlo[j] for j in range(2)) for i in range(2)]
thU = sp.simplify(sum(sp.diff(sqg2*nup[i], X[i]) for i in range(2))/sqg2)
# ADM: K = (1/2N) gam^{-1} (gam_t - 2 D_x N_x),  D_x N_x = d_x Nx - Gamma^x_xx Nx, Gamma = gam_x/(2 gam)
Kadm = (sp.diff(gam, t) - 2*(sp.diff(Nx, x) - sp.diff(gam, x)/(2*gam)*Nx))/(2*N*gam)
k2a = sp.simplify(thU - Kadm)
say("  theta(unitary) - K_ADM =", k2a, "; Q - 1/N =", sp.simplify(QU - 1/N))
vel = {"N_t": sp.diff(N, t), "Nx_t": sp.diff(Nx, t), "gam_t": sp.diff(gam, t)}
dep = {k: bool(sp.simplify(sp.diff(thU, v)) != 0) for k, v in vel.items()}
say("  theta depends on velocities:", dep)
out["K2_theta_minus_KADM"] = str(k2a); out["K2_velocities"] = dep

# isotropic 3+1 Hessian of EH kinetic + F(Q, K) in gamma-dot_ii at gamma = a^2 delta (diagonal sector)
say("== K2c: velocity Hessian, 3+1 diagonal sector")
a_, N_ = sp.symbols("a N", positive=True)
v = sp.symbols("v1:4")  # gamma-dot_ii
Fth0, Fthth0, Fq = sp.symbols("F_th F_thth F_Q")
th0s = sp.symbols("theta0")
Kij = [v[i]/(2*N_) for i in range(3)]          # K_ii (lower), shift zero
gup = 1/a_**2
Ktr = sum(gup*Kij[i] for i in range(3))
S2 = sum(gup**2*Kij[i]**2 for i in range(3))
sqrtgam = a_**3
LEH = N_*sqrtgam*(S2 - Ktr**2)/(4*Kg)
# F expanded to second order about theta0 (only F's theta dependence carries velocities)
LF = N_*sqrtgam*(Fth0*(Ktr - th0s) + Fthth0*(Ktr - th0s)**2/2)
Hs = sp.hessian(LEH + LF, v)
evec_tr = sp.Matrix([1, 1, 1]); evec_tl = sp.Matrix([1, -1, 0])
ev_tr = sp.simplify((evec_tr.T*Hs*evec_tr)[0]/(evec_tr.T*evec_tr)[0])
ev_tl = sp.simplify((evec_tl.T*Hs*evec_tl)[0]/(evec_tl.T*evec_tl)[0])
say("  trace eigenvalue:", ev_tr, "  traceless eigenvalue:", ev_tl)
# expected trace: (3 N a^3)/(4 N^2 a^4) * [-1/(6K)... ] -> write in units: dK/dv_i = 1/(2 N a^2)
exp_tr = sp.simplify(3*(N_*a_**3)*(1/(2*N_*a_**2))**2*2*(-sp.Rational(1, 6)/Kg + Fthth0/2)*1)
say("  trace eigenvalue / [N a^3 (1/(2Na^2))^2 * 3] =", sp.simplify(ev_tr/(N_*a_**3*3/(4*N_**2*a_**4))),
    "  (hand: 2*(-1/(6K) + F_thth/2) = -1/(3K) + F_thth)")
k2c = sp.simplify(ev_tr/(N_*a_**3*3/(4*N_**2*a_**4)) - (-sp.Rational(1, 3)/Kg + Fthth0))
say("  K2c residual:", k2c)
out["K2c_residual"] = str(k2c)
out["K2c_trace_eig"] = str(ev_tr)

# ---------------------------------------------------------------- KA2 minisuperspace
say("== KA2: closed-FRW minisuperspace, unitary gauge")
a, ad, Nn, kc, rb0 = sp.symbols("a adot N k rho_b0", real=True)
FF = sp.Function("F")
qq, tt_ = sp.symbols("q th")
thM = 3*ad/(Nn*a)
Lmini = sp.Rational(3, 2)/Kg*(-a*ad**2/Nn + kc*Nn*a) + Nn*a**3*FF(1/Nn, thM) - rb0*Nn
E = ad*sp.diff(Lmini, ad) - Lmini
LN = sp.diff(Lmini, Nn)
FQexpr = sp.Subs(sp.Derivative(FF(qq, tt_), qq), (qq, tt_), (1/Nn, thM)).doit()
ka2 = sp.simplify((E + Nn*LN + a**3*FQexpr).doit())
say("  E + N L_N + a^3 F_Q =", ka2)
out["KA2_identity_residual"] = str(ka2)
# Friedmann form: L_N / a^3 = (3/2K)(H^2 + k/a^2) - rho_b - rho_K, rho_K = Q F_Q + th F_th - F
Hs_ = ad/(Nn*a)
Fth_expr = sp.Subs(sp.Derivative(FF(qq, tt_), tt_), (qq, tt_), (1/Nn, thM)).doit()
rhoK = (1/Nn)*FQexpr + (0 if MUT == "MU1" else thM*Fth_expr) - FF(1/Nn, thM)
ka2b = sp.simplify((LN/a**3 - (sp.Rational(3, 2)/Kg*(Hs_**2 + kc/a**2) - rb0/a**3 - rhoK)).doit())
say("  N-equation - Friedmann form =", ka2b)
out["KA2_friedmann_residual"] = str(ka2b)

# KA3: M_2 constant
Mc, nn = sp.symbols("M n", positive=True)
Fq_ = Mc*(qq - 1)**2/(2*Kg)
Qn = 1 + Kg*nn/Mc  # from n = F_Q
rhoK3 = (qq*sp.diff(Fq_, qq) + 0 - Fq_).subs(qq, Qn)
ka3 = sp.simplify(rhoK3 - (nn + Kg*nn**2/(2*Mc)))
say("== KA3: rho_K - (n + K n^2/2M) =", ka3)
out["KA3_residual"] = str(ka3)

# G ratio machinery: Friedmann (3/(2K)) H^2 = rho_rest + rho_K(H) at fixed n; G_cosmo/G = 1/(1 - (2K/3) d rho_K/d(H^2))
lam, H2 = sp.symbols("lambda H2", real=True)
def Gratio(Fexpr_q_th):
    # rho_K as function of theta at fixed n: Q from n = F_Q (solve), here only for F linear in Q or Q-free
    rk = (qq*sp.diff(Fexpr_q_th, qq) + tt_*sp.diff(Fexpr_q_th, tt_) - Fexpr_q_th)
    rk = rk.subs(tt_, 3*sp.sqrt(H2))
    return sp.simplify(1/(1 - sp.Rational(2, 3)*Kg*sp.diff(rk, H2)))
ka4 = sp.simplify(Gratio(-lam*tt_**2/(4*Kg)) - 1/(1 + sp.Rational(3, 2)*lam))
say("== KA4: G_cosmo/G - 1/(1 + 3 lambda/2) =", ka4)
out["KA4_residual"] = str(ka4)

# K4 lives in tk1_k4.py
with open(os.path.join(os.path.dirname(__file__), "tk1_a1%s.json" % ("_MUTATE_" + MUT if MUT else "")), "w") as fh:
    json.dump(out, fh, indent=1, default=str)
say("done %.1f s" % (time.time() - T0))
