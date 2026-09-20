"""Shared covariant build of the candidate's action (THE_ACTION with the AeST coupling), used by L283+.
build_fourier_matrix(): Minkowski, tau = t, phi = Q0 t, Newtonian-gauge scalar perturbations Psi, Phi, clock T, scalar P of (t, x);
quadratic Lagrangian by machine (as L282), Euler-Lagrange equations, plane-wave matrix M(omega, k) with an optional matter source
column for the lapse equation.  The scalar's Q-potential enters only through its curvature F_QQ at the background: K2 := F_QQ/2."""
import sympy as sp

def build_fourier_matrix():
    t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
    eps = sp.symbols('epsilon', positive=True)
    KB, c1, c2, c3, c4, K2, Q0, beta, xi = sp.symbols('K_B c_1 c_2 c_3 c_4 K_2 Q_0 beta xi', real=True)
    Psi, Phi, Tf, P = [sp.Function(n)(t, x) for n in ("Psi", "Phi", "T", "P")]
    N = 1 + eps * Psi; a = 1 - eps * Phi
    g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); ginv = g.inv(); sqrtg = N * a ** 3
    Gam = [[[sp.simplify(sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2) for n in range(4)] for m in range(4)] for l in range(4)]
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
    phi = Q0 * t + eps * P; dphi = [sp.diff(phi, v) for v in X]
    Jdphi = sum(J_up[m] * dphi[m] for m in range(4))
    Q = sum(n_up[m] * dphi[m] for m in range(4))
    Y = sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
    Lbr = R - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - K2 * (Q - Q0) ** 2
    L = sqrtg * Lbr
    L2 = sp.simplify(sp.diff(L, eps, 2).subs(eps, 0) / 2) - (2 - KB) * xi ** 2 * sp.diff(P, x, 2) ** 2
    fields = [Psi, Phi, Tf, P]
    def EL(Lag, f):
        e = sp.diff(Lag, f)
        for v in (t, x):
            e -= sp.diff(sp.diff(Lag, sp.diff(f, v)), v)
        for v1, v2 in ((t, t), (t, x), (x, x)):
            d2 = sp.diff(f, v1, v2)
            if Lag.has(d2): e += sp.diff(sp.diff(Lag, d2), v1, v2)
        return sp.expand(e)
    E = [EL(L2, f) for f in fields]
    w, k = sp.symbols('omega k', positive=True)
    amps = sp.symbols('A_Psi A_Phi A_T A_P'); ex = sp.exp(sp.I * (k * x - w * t))
    sub = {f: A * ex for f, A in zip(fields, amps)}
    M = sp.zeros(4, 4)
    for i, e in enumerate(E):
        ee = sp.expand(sp.simplify(e.subs(sub).doit() / ex))
        for j, A in enumerate(amps):
            M[i, j] = sp.simplify(ee.coeff(A))
    c14 = sp.Symbol('c14')
    M = M.subs({c1: KB, c3: -KB, c4: c14 - KB})
    syms = dict(w=w, k=k, KB=KB, c2=c2, c14=c14, K2=K2, Q0=Q0, beta=beta, xi=xi, amps=amps)
    return M, syms


def build_fourier_matrix_generalF():
    """Same build with a GENERIC Q-well F(Q) about a background Qbar (symbol Q_0 reused as Qbar): the quadratic action carries
    F0 = F(Qbar), F1 = F_Q(Qbar), F2 = F_QQ(Qbar).  With F1 != 0 the background carries dust (16 pi G rho_d = F0 - Qbar F1) and
    Minkowski is not an exact solution: the O(eps) tadpole is dropped (Jeans swindle), which is exact to O((aH/k)^2) sub-horizon."""
    t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
    eps = sp.symbols('epsilon', positive=True)
    KB, c1, c2, c3, c4, Q0, beta, xi = sp.symbols('K_B c_1 c_2 c_3 c_4 Q_0 beta xi', real=True)
    F0, F1, F2 = sp.symbols('F_0 F_1 F_2', real=True)
    Psi, Phi, Tf, P = [sp.Function(n)(t, x) for n in ("Psi", "Phi", "T", "P")]
    N = 1 + eps * Psi; a = 1 - eps * Phi
    g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); ginv = g.inv(); sqrtg = N * a ** 3
    Gam = [[[sp.simplify(sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2) for n in range(4)] for m in range(4)] for l in range(4)]
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
    phi = Q0 * t + eps * P; dphi = [sp.diff(phi, v) for v in X]
    Jdphi = sum(J_up[m] * dphi[m] for m in range(4))
    Q = sum(n_up[m] * dphi[m] for m in range(4))
    Y = sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
    dQ = Q - Q0
    Fexp = F0 + F1 * dQ + F2 * dQ ** 2 / 2                     # F(Q) to the order that survives at eps^2 (dQ = O(eps))
    Lbr = R - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - Fexp
    L = sqrtg * Lbr
    L2 = sp.simplify(sp.diff(L, eps, 2).subs(eps, 0) / 2) - (2 - KB) * xi ** 2 * sp.diff(P, x, 2) ** 2
    fields = [Psi, Phi, Tf, P]
    def EL(Lag, f):
        e = sp.diff(Lag, f)
        for v in (t, x):
            e -= sp.diff(sp.diff(Lag, sp.diff(f, v)), v)
        for v1, v2 in ((t, t), (t, x), (x, x)):
            d2 = sp.diff(f, v1, v2)
            if Lag.has(d2): e += sp.diff(sp.diff(Lag, d2), v1, v2)
        return sp.expand(e)
    E = [EL(L2, f) for f in fields]
    w, k = sp.symbols('omega k', positive=True)
    amps = sp.symbols('A_Psi A_Phi A_T A_P'); ex = sp.exp(sp.I * (k * x - w * t))
    sub = {f: A * ex for f, A in zip(fields, amps)}
    M = sp.zeros(4, 4)
    for i, e in enumerate(E):
        ee = sp.expand(sp.simplify(e.subs(sub).doit() / ex))
        for j, A in enumerate(amps):
            M[i, j] = sp.simplify(ee.coeff(A))
    c14 = sp.Symbol('c14')
    M = M.subs({c1: KB, c3: -KB, c4: c14 - KB})
    syms = dict(w=w, k=k, KB=KB, c2=c2, c14=c14, Q0=Q0, beta=beta, xi=xi, F0=F0, F1=F1, F2=F2, amps=amps)
    return M, syms


def build_frw_perturbation_odes():
    """Scalar-sector perturbations on FRW from THE_ACTION (+ Lambda), fields Psi, Phi, T, P of (t, x), Newtonian gauge
    ds^2 = -(1 + 2 eps Psi) dt^2 + a(t)^2 (1 - 2 eps Phi) dx^2, clock tau = t + eps T, scalar phi = phibar(t) + eps P with phibar' = Qb(t),
    Q-well expanded about the rolling background: F = F0(t) + F1(t) dQ + F2(t) dQ^2/2 (F0, F1, F2 given functions of time).
    Returns the four Euler-Lagrange equations after the plane-wave substitution field(t, x) = f(t) e^{i k x} (linear ODEs in t with
    complex coefficients) and the symbols.  Radiation is not in the action (it enters only through a(t)): O((aH/k)^2) error sub-horizon."""
    t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
    eps = sp.symbols('epsilon', positive=True)
    KB, c1, c2, c3, c4, beta, xi, Lam = sp.symbols('K_B c_1 c_2 c_3 c_4 beta xi Lambda', real=True)
    a = sp.Function('a')(t); Qb = sp.Function('Qb')(t); F0 = sp.Function('F0')(t); F1 = sp.Function('F1')(t); F2 = sp.Function('F2')(t)
    Psi, Phi, Tf, P = [sp.Function(n)(t, x) for n in ("Psi", "Phi", "T", "P")]
    N = 1 + eps * Psi; A = a * (1 - eps * Phi)
    g = sp.diag(-N ** 2, A ** 2, A ** 2, A ** 2); ginv = g.inv(); sqrtg = N * A ** 3
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
    L2 = sp.diff(L, eps, 2).subs(eps, 0) / 2
    L2 = L2 - (2 - KB) * xi ** 2 * sp.diff(P, x, 2) ** 2 / a           # healing term: -(2-K_B) xi^2 (D^2 phi)^2 sqrt(-g), D^2 = lap/a^2
    L2 = sp.expand(L2)
    fields = [Psi, Phi, Tf, P]
    def EL(Lag, f):
        e = sp.diff(Lag, f)
        for v in (t, x):
            e -= sp.diff(sp.diff(Lag, sp.diff(f, v)), v)
        for v1, v2 in ((t, t), (t, x), (x, x)):
            d2 = sp.diff(f, v1, v2)
            if Lag.has(d2): e += sp.diff(sp.diff(Lag, d2), v1, v2)
        return sp.expand(e)
    E = [EL(L2, f) for f in fields]
    k = sp.symbols('k', positive=True)
    amps = [sp.Function(n)(t) for n in ("psi", "phi", "tt", "pp")]; ex = sp.exp(sp.I * k * x)
    sub = {f: A_ * ex for f, A_ in zip(fields, amps)}
    ODE = [sp.expand(sp.simplify(e.subs(sub).doit() / ex)) for e in E]
    c14 = sp.Symbol('c14'); ODE = [o.subs({c1: KB, c3: -KB, c4: c14 - KB}) for o in ODE]
    syms = dict(t=t, k=k, KB=KB, c2=c2, c14=c14, beta=beta, xi=xi, Lam=Lam, a=a, Qb=Qb, F0=F0, F1=F1, F2=F2, amps=amps)
    return ODE, syms


def build_frw_perturbation_odes_shift():
    """[EL operator general-order and healing term covariant, 2026-09-19 after L287]
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
    # covariant healing term (L287): -(2-K_B) xi^2 (D^2 phi)^2 with D^2 phi = h^{mu nu}(d_mu d_nu phi - Gamma^l_{mu nu} d_l phi)
    Hess = [[sp.diff(phi, X[m], X[n]) - sum(Gam[l][m][n] * dphi[l] for l in range(4)) for n in range(4)] for m in range(4)]
    D2phi = sum((ginv[m, n] + n_up[m] * n_up[n]) * Hess[m][n] for m in range(4) for n in range(4))
    L = L - sqrtg * (2 - KB) * xi ** 2 * D2phi ** 2
    L = L.subs(sp.Derivative(phibar, t), Qb).subs(sp.Derivative(phibar, (t, 2)), sp.Derivative(Qb, t))
    L2 = sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2)
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


def build_frw_perturbation_odes_chi():
    """[2026-09-19, L291] The L290 Y-modulated carrier on FRW: the same sector as build_frw_perturbation_odes_shift
    (Psi, B, Phi, T, P; general-order EL; covariant healing) PLUS the chi-dust field Xc, L_chi = -(G1 dX + (G2/2) dX^2),
    dX = X_chi - Cc^2, X_chi = -g^{mu nu} d_mu chi d_nu chi, background chi = Cc t (chi' = Cc const: the shift-symmetric
    charge a^3 P_X chi' = const), G1 = -p1 < 0 (positive dust density 16 pi G rho = 2 Cc^2 p1), G2 = -g2 (the Y = 0 state of
    the L290 modulation: c_s^2 = p1/(p1 + 2 Cc^2 g2) = 1/A = 1e-10, the forest-cold value).  At the homogeneous background
    dY = 0 exactly, so the modulation's Y-dependence does not enter the linear system (L290 V3): the chi-dust is the
    carrier's cosmological state.  Returns the six Euler-Lagrange equations after the plane-wave substitution
    field(t, x) = f(t) e^{i k x}."""

    t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
    eps = sp.symbols('epsilon', positive=True)
    KB, c1, c2, c3, c4, beta, xi, Lam, Cc, G1, G2 = sp.symbols('K_B c_1 c_2 c_3 c_4 beta xi Lambda C G_1 G_2', real=True)
    a = sp.Function('a')(t); Qb = sp.Function('Qb')(t); F0 = sp.Function('F0')(t); F1 = sp.Function('F1')(t); F2 = sp.Function('F2')(t)
    Psi, Bs, Phi, Tf, P, Xc = [sp.Function(n)(t, x) for n in ("Psi", "B", "Phi", "T", "P", "chi")]
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
    chibar = sp.Function('chibar')(t)
    chi = chibar + eps * Xc; dchi = [sp.diff(chi, v) for v in X]
    Xchi = -sum(ginv[m, n] * dchi[m] * dchi[n] for m in range(4) for n in range(4)); dX2 = Xchi - Cc ** 2
    Lbr = R - 2 * Lam - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - Fexp - (G1 * dX2 + G2 * dX2 ** 2 / 2)
    L = sqrtg * Lbr
    L = L.subs(sp.Derivative(phibar, t), Qb).subs(sp.Derivative(phibar, (t, 2)), sp.Derivative(Qb, t))
    L = L.subs(sp.Derivative(chibar, t), Cc).subs(sp.Derivative(chibar, (t, 2)), 0)
    # covariant healing term (L287): -(2-K_B) xi^2 (D^2 phi)^2 with D^2 phi = h^{mu nu}(d_mu d_nu phi - Gamma^l_{mu nu} d_l phi)
    Hess = [[sp.diff(phi, X[m], X[n]) - sum(Gam[l][m][n] * dphi[l] for l in range(4)) for n in range(4)] for m in range(4)]
    D2phi = sum((ginv[m, n] + n_up[m] * n_up[n]) * Hess[m][n] for m in range(4) for n in range(4))
    L = L - sqrtg * (2 - KB) * xi ** 2 * D2phi ** 2
    L = L.subs(sp.Derivative(phibar, t), Qb).subs(sp.Derivative(phibar, (t, 2)), sp.Derivative(Qb, t))
    L2 = sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2)
    fields = [Psi, Bs, Phi, Tf, P, Xc]
    def EL(Lag, f):
        e = sp.diff(Lag, f)
        for d_ in Lag.atoms(sp.Derivative):
            if d_.expr == f:
                vars_ = []
                for v_, cnt in d_.variable_count: vars_ += [v_] * cnt
                e += (-1) ** len(vars_) * sp.diff(sp.diff(Lag, d_), *vars_)
        return sp.expand(e)
    E = [EL(L2, f).subs(Bs, 0).doit() for f in fields]
    E = [sp.expand(e.subs(Bs, 0)) for e in E]
    k = sp.symbols('k', positive=True)
    amps = [sp.Function(n)(t) for n in ("psi", "bb", "phi", "tt", "pp", "cc")]; ex = sp.exp(sp.I * k * x)
    sub = {f: A_ * ex for f, A_ in zip(fields, amps)}
    ODE = [sp.expand(e.subs(sub).doit().subs(amps[1], 0) / ex) for e in E]
    c14 = sp.Symbol('c14'); ODE = [o.subs({c1: KB, c3: -KB, c4: c14 - KB}) for o in ODE]
    syms = dict(t=t, k=k, KB=KB, c2=c2, c14=c14, beta=beta, xi=xi, Lam=Lam, a=a, Qb=Qb, F0=F0, F1=F1, F2=F2,
                Cc=Cc, G1=G1, G2=G2, amps=amps)
    return ODE, syms