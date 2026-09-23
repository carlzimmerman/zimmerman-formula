"""Isolated research copy; original builder SHA256 e3ede3132b8692540ed63e92cfb155fcbb899366276604ce1f368203f68a84b0."""
import sympy as sp

def build_frw_perturbation_odes_shift():
    """Audit repair: intrinsic projected-gradient healing, outside kernel, flat FRW.
    Scalar-sector perturbations on FRW from THE_ACTION (+ Lambda), fields Psi, Phi, T, P of (t, x), Newtonian gauge
    ds^2 = -(1 + 2 eps Psi) dt^2 + a(t)^2 (1 - 2 eps Phi) dx^2, clock tau = t + eps T, scalar phi = phibar(t) + eps P with phibar' = Qb(t),
    Q-well expanded about the rolling background: F = F0(t) + F1(t) dQ + F2(t) dQ^2/2 (F0, F1, F2 given functions of time).
    Returns the four Euler-Lagrange equations after the plane-wave substitution field(t, x) = f(t) e^{i k x} (linear ODEs in t with
    complex coefficients) and the symbols.  Radiation is not in the action (it enters only through a(t)): O((aH/k)^2) error sub-horizon."""
    t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
    eps = sp.symbols('epsilon', positive=True)
    KB, c1, c2, c3, c4, beta, xi, Lam = sp.symbols('K_B c_1 c_2 c_3 c_4 beta xi Lambda', real=True)
    a = sp.Function('a')(t); Qb = sp.Function('Qb')(t); F0 = sp.Function('F0')(t); F1 = sp.Function('F1')(t); F2 = sp.Function('F2')(t)
    Psi, Bs, Phi, Tf, P = [sp.Function(n)(t, x) for n in ("Psi", "B", "Phi", "T", "P")]
    N = 1 + eps * Psi; A = a * (1 - eps * Phi)
    g = sp.diag(-N ** 2, A ** 2, A ** 2, A ** 2); g[0, 1] = eps * a * sp.diff(Bs, x); g[1, 0] = g[0, 1]
    ginv = g.inv(); sqrtg = sp.sqrt(-g.det())
    Gam = [[[sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2 for n in range(4)] for m in range(4)] for l in range(4)]
    Ric = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            Ric[m, n] = sum(sp.diff(Gam[l][m][n], X[l]) - sp.diff(Gam[l][m][l], X[n]) + sum(Gam[l][l][s] * Gam[s][m][n] - Gam[l][n][s] * Gam[s][m][l] for s in range(4)) for l in range(4))
    R = sum(ginv[m, n] * Ric[m, n] for m in range(4) for n in range(4))
    tau = t + eps * Tf; dtau = [sp.diff(tau, v) for v in X]
    Xinv = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
    n_dn = [-dtau[m] / sp.sqrt(Xinv) for m in range(4)]; n_up = [sum(ginv[m, n] * n_dn[n] for n in range(4)) for m in range(4)]
    Dn = [[sp.diff(n_dn[n], X[m]) - sum(Gam[l][m][n] * n_dn[l] for l in range(4)) for n in range(4)] for m in range(4)]
    Dn_up = [[sum(ginv[m, a_] * ginv[n, b_] * Dn[a_][b_] for a_ in range(4) for b_ in range(4)) for n in range(4)] for m in range(4)]
    T1 = sum(Dn[m][n] * Dn_up[m][n] for m in range(4) for n in range(4))
    divn = sum(ginv[m, n] * Dn[m][n] for m in range(4) for n in range(4)); T2 = divn ** 2
    T3 = sum(Dn[m][n] * Dn_up[n][m] for m in range(4) for n in range(4))
    J_dn = [sum(n_up[nu] * Dn[nu][m] for nu in range(4)) for m in range(4)]
    J_up = [sum(ginv[m, n] * J_dn[n] for n in range(4)) for m in range(4)]
    T4 = sum(J_dn[m] * J_up[m] for m in range(4))
    phibar = sp.Function('phibar')(t)
    phi = phibar + eps * P; dphi = [sp.diff(phi, v) for v in X]
    Jdphi = sum(J_up[m] * dphi[m] for m in range(4))
    Q = sum(n_up[m] * dphi[m] for m in range(4))
    Y = sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
    dQ = Q - Qb
    Fexp = F0 + F1 * dQ + F2 * dQ ** 2 / 2
    Lbr = R - 2 * Lam - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - Fexp
    L = sqrtg * Lbr
    L = L.subs(sp.Derivative(phibar, t), Qb).subs(sp.Derivative(phibar, (t, 2)), sp.Derivative(Qb, t))
    # Written outside-kernel projected-gradient invariant, expanded on flat FRW.
    # Vbar=0, so only A_ij^(1)=partial_i partial_j(P-Qb*T) contributes at order eps^2.
    # It has no homogeneous contribution and its single-wave quadratic form is exact.
    L2 = sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2)
    L2 -= (2 - KB) * xi**2 / a * sp.diff(P-Qb*Tf, x, 2)**2
    fields = [Psi, Bs, Phi, Tf, P]
    def EL(Lag, f):                  # Euler-Lagrange operator for derivatives of EVERY order (L287: the shift enters the curvature with third derivatives)
        e = sp.diff(Lag, f)
        for d_ in Lag.atoms(sp.Derivative):
            if d_.expr == f:
                vars_ = []
                for v_, cnt in d_.variable_count: vars_ += [v_] * cnt
                e += (-1) ** len(vars_) * sp.diff(sp.diff(Lag, d_), *vars_)
        return sp.expand(e)
    E = [EL(L2, f).subs(Bs, 0).doit() for f in fields]                   # Newtonian gauge after the variation: B = 0
    E = [sp.expand(e.subs(Bs, 0)) for e in E]
    k = sp.symbols('k', positive=True)
    amps = [sp.Function(n)(t) for n in ("psi", "bb", "phi", "tt", "pp")]; ex = sp.exp(sp.I * k * x)
    sub = {f: A_ * ex for f, A_ in zip(fields, amps)}
    ODE = [sp.expand(sp.simplify(e.subs(sub).doit().subs(amps[1], 0) / ex)) for e in E]
    c14 = sp.Symbol('c14'); ODE = [o.subs({c1: KB, c3: -KB, c4: c14 - KB}) for o in ODE]
    syms = dict(t=t, k=k, KB=KB, c2=c2, c14=c14, beta=beta, xi=xi, Lam=Lam, a=a, Qb=Qb, F0=F0, F1=F1, F2=F2, amps=amps)
    return ODE, syms
