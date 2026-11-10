"""AKD1 A1 part 1: K1 covariant current vs direct Euler-Lagrange (1+1 jets), K2 unitary-gauge content, K3 principal symbol.
Criteria d88d310eb1. F = F(Q, Y), Y = A_m A^m, A_m = -h_m^k d_k ln Q. Built on TK1's jet method (tk1_a1.py, read only).
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, json, time, random
import sympy as sp
import mpmath as mpm

out = {}
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
def say(*a):
    print(*a, flush=True)

# ---------------------------------------------------------------- K1
say("== K1: covariant current vs Euler-Lagrange (1+1, metric -e^{2A}dt^2 + e^{2B}dx^2), jet variables")
m0, m1, m2 = sp.symbols("m0 m1 m2")
def Ffun(Q, Y):
    return (Q - 1)**2 * (m0 + m1*Y + m2*Y**2)
p_t, p_x, p_tt, p_tx, p_xx = sp.symbols("p_t p_x p_tt p_tx p_xx")
Av, At, Ax, Bv, Bt, Bx = sp.symbols("Av At Ax Bv Bt Bx")

def dm(expr, m):
    """total derivative of an expression of first-order jets of tau and of the metric values (A, B)."""
    if m == 0:
        return (sp.diff(expr, p_t)*p_tt + sp.diff(expr, p_x)*p_tx + sp.diff(expr, Av)*At + sp.diff(expr, Bv)*Bt)
    return (sp.diff(expr, p_t)*p_tx + sp.diff(expr, p_x)*p_xx + sp.diff(expr, Av)*Ax + sp.diff(expr, Bv)*Bx)

ginv = [-sp.exp(-2*Av), sp.exp(-2*Bv)]
sqg = sp.exp(Av + Bv)
Qj = sp.sqrt(-(ginv[0]*p_t**2 + ginv[1]*p_x**2))
nup = [ginv[0]*(-p_t/Qj), ginv[1]*(-p_x/Qj)]          # n^m
hup = [[(ginv[i] if i == j else 0) + nup[i]*nup[j] for j in range(2)] for i in range(2)]
lnQ = sp.log(Qj)
Lm = [dm(lnQ, 0), dm(lnQ, 1)]                          # d_m ln Q (second-order jets)
Aup = [-sum(hup[m][k]*Lm[k] for k in range(2)) for m in range(2)]   # A^m = -h^{mk} d_k ln Q
Yj = sum(hup[m][k]*Lm[m]*Lm[k] for m in range(2) for k in range(2))
nL = sum(nup[k]*Lm[k] for k in range(2))               # n^k d_k ln Q
Lag = sqg*Ffun(Qj, Yj)
dL = {s_: sp.diff(Lag, s_) for s_ in (p_t, p_x, p_tt, p_tx, p_xx)}
qs, ys = sp.symbols("qs ys")
FQj = sp.diff(Ffun(qs, ys), qs).subs({qs: Qj, ys: Yj})
FYj = sp.diff(Ffun(qs, ys), ys).subs({qs: Qj, ys: Yj})
FYYj = sp.diff(Ffun(qs, ys), ys, 2).subs({qs: Qj, ys: Yj})

def jname(base, i, j):
    return sp.Symbol("%s_%d_%d" % (base, i, j))
TJ = {(i, j): jname("T", i, j) for i in range(5) for j in range(5) if 1 <= i + j <= 4}
AJ = {(i, j): jname("A", i, j) for i in range(4) for j in range(4) if i + j <= 3}
BJ = {(i, j): jname("B", i, j) for i in range(4) for j in range(4) if i + j <= 3}
to_full = {p_t: TJ[(1, 0)], p_x: TJ[(0, 1)], p_tt: TJ[(2, 0)], p_tx: TJ[(1, 1)], p_xx: TJ[(0, 2)],
           Av: AJ[(0, 0)], At: AJ[(1, 0)], Ax: AJ[(0, 1)], Bv: BJ[(0, 0)], Bt: BJ[(1, 0)], Bx: BJ[(0, 1)]}
def Dtot(expr, d):
    res = 0
    for J_ in (TJ, AJ, BJ):
        for (i, j), sym in J_.items():
            if not expr.has(sym):
                continue
            nxt = (i + 1, j) if d == 0 else (i, j + 1)
            if nxt not in J_:
                raise ValueError("jet order exceeded")
            res += sp.diff(expr, sym)*J_[nxt]
    return res
parv = {m0: sp.Rational(3, 7), m1: sp.Rational(-5, 11), m2: sp.Rational(2, 13)}
dLf = {k_: v_.subs(parv).subs(to_full) for k_, v_ in dL.items()}
ELj = (-Dtot(dLf[p_t], 0) - Dtot(dLf[p_x], 1) + Dtot(Dtot(dLf[p_tt], 0), 0) + Dtot(Dtot(dLf[p_tx], 0), 1)
       + Dtot(Dtot(dLf[p_xx], 1), 1))
say("  EL built in jets %.0f s" % (time.time() - T0))
F_ = lambda e: e.subs(parv).subs(to_full)
sqg_f, Q_f = F_(sqg), F_(Qj)
nup_f = [F_(v) for v in nup]
Aup_f = [F_(v) for v in Aup]
FQ_f, FY_f, nL_f = F_(FQj), F_(FYj), F_(nL)
# hand current: J^m = [F_Q + (2/Q) nabla_k(F_Y A^k)] n^m + (2/Q) F_Y (n.d ln Q) A^m ;  nabla_k V^k = d_k(sqg V^k)/sqg
divFA = (Dtot(sqg_f*FY_f*Aup_f[0], 0) + Dtot(sqg_f*FY_f*Aup_f[1], 1))/sqg_f
charge = FQ_f + 2*divFA/Q_f
Jf = [charge*nup_f[m] + 2*FY_f*nL_f*Aup_f[m]/Q_f for m in range(2)]
divJ = Dtot(sqg_f*Jf[0], 0) + Dtot(sqg_f*Jf[1], 1)
say("  div J built %.0f s" % (time.time() - T0))
allsyms = sorted((ELj + divJ).free_symbols, key=str)
fEL = sp.lambdify(allsyms, ELj, "mpmath"); fRes = sp.lambdify(allsyms, ELj + divJ, "mpmath")
fDiff = sp.lambdify(allsyms, ELj - divJ, "mpmath")
say("  lambdified %.0f s" % (time.time() - T0))
mpm.mp.dps = 40
rr = random.Random(3)
k1, k1_wrongsign = [], []
for trial in range(6):
    vals = {}
    for J_ in (TJ, AJ, BJ):
        for key_, sym in J_.items():
            vals[sym] = mpm.mpf(rr.randint(-9, 9))/rr.randint(4, 13)
    vals[TJ[(1, 0)]] = mpm.mpf(rr.randint(25, 45))/9
    vals[TJ[(0, 1)]] = mpm.mpf(rr.randint(-5, 5))/9
    args = [vals.get(s_, 0) for s_ in allsyms]
    rv, sv, dv = fRes(*args), fEL(*args), fDiff(*args)
    k1.append(float(abs(rv)/max(abs(sv), mpm.mpf("1e-30"))))
    k1_wrongsign.append(float(abs(dv)/max(abs(sv), mpm.mpf("1e-30"))))
say("  K1 |EL + d_k(sqrt(-g) J^k)| / |EL| at 6 random jets (40 digits):", ["%.1e" % r for r in k1])
say("  (control, opposite sign |EL - div|/|EL|):", ["%.2f" % r for r in k1_wrongsign])
out["K1_residuals"] = k1
out["K1_control_opposite_sign"] = k1_wrongsign
out["K1_pass"] = max(k1) <= 1e-30
out["K1_EL_has_4th_jets"] = any(ELj.has(TJ[k_]) for k_ in TJ if sum(k_) == 4)
out["K1_current"] = "J^m = [F_Q + (2/Q) nabla_k(F_Y A^k)] n^m + (2/Q) F_Y (n^k d_k ln Q) A^m; EL = -d_m(sqrt(-g) J^m)"
say("  EL contains 4th jets of tau:", out["K1_EL_has_4th_jets"])

# ---------------------------------------------------------------- K3 principal symbol
say("== K3: principal symbol of the khronon equation")
xi0, xi1 = sp.symbols("xi0 xi1")
mono = {p_tt: xi0**2, p_tx: xi0*xi1, p_xx: xi1**2}
symb = sum(sp.diff(Lag, a1, b1)*mono[a1]*mono[b1] for a1 in mono for b1 in mono)
xi = [xi0, xi1]
nxi = sum(nup[i]*xi[i] for i in range(2))
hxx = sum(hup[i][j]*xi[i]*xi[j] for i in range(2) for j in range(2))
Axi = sum(Aup[i]*xi[i] for i in range(2))
hand = 2*sqg*nxi**2*(FYj*hxx + 2*FYYj*Axi**2)/Qj**2
rr = random.Random(7)
k3 = []
for _ in range(6):
    vals = {s_: sp.Rational(rr.randint(-9, 9), rr.randint(3, 11)) for s_ in (p_x, p_tt, p_tx, p_xx, Av, At, Ax, Bv, Bt, Bx, xi0, xi1)}
    vals[p_t] = sp.Rational(rr.randint(20, 40), 7)
    vals.update(parv)
    a_ = sp.N(symb.subs(vals), 30); b_ = sp.N(hand.subs(vals), 30)
    k3.append(float(a_/b_) if b_ != 0 else None)
say("  symbol / [2 sqrt(-g) (n.xi)^2 (F_Y h(xi,xi) + 2 F_YY (A.xi)^2) / Q^2] at 6 random jets:", k3)
out["K3_symbol_ratio"] = k3
out["K3_note"] = ("principal (4th-order) symbol = 2 sqrt(-g) (n.xi)^2 [F_Y h(xi,xi) + 2 F_YY (A.xi)^2] / Q^2: "
                  "two derivatives along n acting on a leaf operator; it vanishes for xi annihilating n (characteristic "
                  "surfaces contain the clock's worldlines) and for xi along n; no new propagating cone. Sign of the "
                  "inertia: K4.")

# ---------------------------------------------------------------- K2 unitary gauge content
say("== K2: unitary gauge (tau = t) in 1+1 with lapse, shift and spatial metric: what Y depends on")
t, x = sp.symbols("t x", real=True)
N = sp.Function("N")(t, x); S = sp.Function("S")(t, x); g = sp.Function("g")(t, x)   # lapse, shift N^x, gamma_xx
# metric: -N^2 dt^2 + g (dx + S dt)^2
gm = sp.Matrix([[-N**2 + g*S**2, g*S], [g*S, g]])
gi = sp.simplify(gm.inv())
sq = sp.sqrt(-gm.det())
X = [t, x]
du = [1, 0]                                   # d_m tau, tau = t
Qu = sp.sqrt(-sum(gi[i, j]*du[i]*du[j] for i in range(2) for j in range(2)))
Qu = sp.simplify(Qu)
nl = [-du[i]/Qu for i in range(2)]
nu_ = [sum(gi[i, j]*nl[j] for j in range(2)) for i in range(2)]
hu = [[gi[i, j] + nu_[i]*nu_[j] for j in range(2)] for i in range(2)]
lq = sp.log(Qu)
dlq = [sp.diff(lq, X[i]) for i in range(2)]
Yu = sp.simplify(sum(hu[i][j]*dlq[i]*dlq[j] for i in range(2) for j in range(2)))
Yexp = sp.simplify(Yu - (sp.diff(N, x)/N)**2/g)
say("  Q =", Qu, "  Y - (d_x ln N)^2 / gamma_xx =", Yexp)
vel = [sp.Derivative(N, t), sp.Derivative(S, t), sp.Derivative(g, t), S]
deps = {str(v): bool(Yu.has(v)) for v in vel}
say("  Y depends on N-dot, S-dot, gamma-dot, shift:", deps)
out["K2_Q_unitary"] = str(Qu)
out["K2_Y_minus_unitary_form"] = str(Yexp)
out["K2_Y_depends_on"] = deps
out["K2_Q_squared_times_N_squared_minus_1"] = str(sp.simplify(Qu**2*N**2 - 1))   # Q = 1/|N| = 1/N for N > 0
out["K2_pass"] = (Yexp == 0) and not any(deps.values()) and sp.simplify(Qu**2*N**2 - 1) == 0
out["K2_note"] = ("in unitary gauge L_K = N sqrt(gamma) M_2(gamma^ij d_i ln N d_j ln N) (1/N - 1)^2/(2K): no velocity of any "
                  "field; matter couples to g only; the lapse obeys a constraint (an elliptic equation on the leaves, "
                  "Horava's healthy-extension class). Metric and matter stay second order in time.")
say("  K2 pass:", out["K2_pass"])
json.dump(out, open(os.path.join(HERE, "akd1_a1.json"), "w"), indent=1, default=str)
say("done %.0f s" % (time.time() - T0))
