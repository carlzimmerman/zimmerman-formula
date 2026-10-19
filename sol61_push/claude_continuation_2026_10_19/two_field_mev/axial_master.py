"""Axial (odd-parity) perturbations of the static two-field scalar star (PLAN N1).

Background ds^2 = e^{2nu}dt^2 - e^{2lam}dr^2 - r^2 dOmega^2 with anisotropic scalar
stress T^m_n = diag(rho, -p_r, -p_t, -p_t). Scalar-field perturbations are polar, so the
axial sector has no matter degree of freedom; for complex scalars delta L = 0 under axial
h_{mn} and L = p_t on the background, hence EXACTLY delta T_{mn} = -p_t h_{mn}.
Regge-Wheeler gauge: h_{t phi} = h0(r) e^{-i s t} sin(th) dP_l/dth, h_{r phi} = h1(r) (same).
The script (1) linearizes the Einstein tensor symbolically, (2) eliminates h0 using the
(theta,phi) equation, (3) writes the (r,phi) equation as a Z-equation, Z = e^{nu-lam} h1/r,
d/dr* = e^{nu-lam} d/dr, reads off V, (4) re-expresses V through m, rho, p_r, p_t with the
background Einstein/TOV relations, (5) checks the vacuum Regge-Wheeler limit, and
(6) evaluates V on the saved GR profile for l = 2, 3, 10.
"""
import json, math, sys
import numpy as np
import sympy as sp
from common import dump, peak_rss_mb, Timer

tm = Timer()
t, r, th, ph = sp.symbols('t r theta phi', real=True)
eps, s, Gn = sp.symbols('epsilon sigma G', positive=True)
nu = sp.Function('nu')(r)
la_ = sp.Function('lam')(r)
h0 = sp.Function('h0')(r)
h1 = sp.Function('h1')(r)
X = [t, r, th, ph]


def linear_einstein(l):
    P = sp.legendre(l, sp.cos(th))
    S = sp.simplify(sp.sin(th) * sp.diff(P, th))
    E = sp.exp(-sp.I * s * t)
    g0 = sp.diag(sp.exp(2 * nu), -sp.exp(2 * la_), -r ** 2, -r ** 2 * sp.sin(th) ** 2)
    hm = sp.zeros(4)
    hm[0, 3] = hm[3, 0] = h0 * S * E
    hm[1, 3] = hm[3, 1] = h1 * S * E
    g = g0 + eps * hm
    g0i = g0.inv()
    gi = g0i - eps * g0i * hm * g0i
    Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for m in range(4):
            for n in range(m, 4):
                v = 0
                for b in range(4):
                    if gi[a, b] != 0:
                        v += gi[a, b] * (sp.diff(g[b, n], X[m]) + sp.diff(g[b, m], X[n]) - sp.diff(g[m, n], X[b]))
                v = sp.expand(v / 2)
                # keep through O(eps)
                v = v.subs(eps, 0) + eps * sp.diff(v, eps).subs(eps, 0)
                Gam[a][m][n] = Gam[a][n][m] = v

    def ricci(m, n):
        v = 0
        for a in range(4):
            v += sp.diff(Gam[a][m][n], X[a]) - sp.diff(Gam[a][a][m], X[n])
            for b in range(4):
                v += Gam[a][a][b] * Gam[b][m][n] - Gam[a][n][b] * Gam[b][a][m]
        return sp.expand(v)

    R0 = sp.simplify(sum((g0i[a, a] * ricci(a, a)).subs(eps, 0) for a in range(4)))
    out = {}
    for (m, n) in [(0, 3), (1, 3), (2, 3)]:
        Rmn = ricci(m, n)
        dR = sp.diff(Rmn, eps).subs(eps, 0)
        dG = dR - sp.Rational(1, 2) * hm[m, n] * R0     # delta R = 0 for axial (parity)
        out[(m, n)] = sp.simplify(dG / E)
    return out, S, R0, g0


def background_subs():
    """Matter form: e^{-2lam} = 1 - 2 G m/r, m' = 4 pi r^2 rho,
    nu' = G(m + 4 pi r^3 p_r)/(r^2 N), p_r' = -(rho+p_r) nu' + 2(p_t-p_r)/r."""
    mm = sp.Function('m')(r)
    rho = sp.Function('rho')(r)
    pr = sp.Function('p_r')(r)
    pt = sp.Function('p_t')(r)
    N = 1 - 2 * Gn * mm / r
    lam_e = -sp.log(N) / 2
    nup = Gn * (mm + 4 * sp.pi * r ** 3 * pr) / (r ** 2 * N)
    rules_m = {sp.Derivative(mm, r): 4 * sp.pi * r ** 2 * rho,
               sp.Derivative(pr, r): -(rho + pr) * nup + 2 * (pt - pr) / r}
    lamp = sp.diff(lam_e, r).subs(rules_m)
    lampp = sp.diff(lamp, r).subs(rules_m)
    nupp = sp.diff(nup, r).subs(rules_m)
    return dict(mm=mm, rho=rho, pr=pr, pt=pt, N=N, lam=lam_e, lamp=lamp, lampp=lampp, nup=nup, nupp=nupp)


def derive(l):
    eq, S, R0, g0 = linear_einstein(l)
    B = background_subs()
    pt = B['pt']
    # background R0 must equal -8 pi G T (T = rho - p_r - 2 p_t with signature +---): check later
    E_tp = eq[(0, 3)] + 8 * sp.pi * Gn * pt * h0 * S
    E_rp = eq[(1, 3)] + 8 * sp.pi * Gn * pt * h1 * S
    E_thp = eq[(2, 3)]
    # angular separation: evaluate at two angles; the ratio must be r-independent
    def separate(Eq):
        Ea = sp.simplify(Eq.subs(th, sp.pi / 3))
        Eb = sp.simplify(Eq.subs(th, sp.pi / 5))
        ratio = sp.simplify(Ea / Eb)
        return Ea, bool(sp.simplify(sp.diff(ratio, r)) == 0)
    Etp, ok_tp = separate(E_tp)
    Erp, ok_rp = separate(E_rp)
    Ethp, ok_thp = separate(E_thp)
    sep = dict(tp=[ok_tp], rp=[ok_rp], thp=[ok_thp])
    # theta-phi equation: solve for h0
    h0sol = sp.solve(Ethp, h0)
    assert len(h0sol) == 1
    h0s = h0sol[0]
    ode = sp.simplify(Erp.subs(h0, h0s).doit())
    # Z variable
    Z = sp.Function('Z')(r)
    h1Z = r * sp.exp(la_ - nu) * Z
    odeZ = sp.simplify((ode.subs(h1, h1Z).doit()))
    odeZ = sp.expand(odeZ)
    a = odeZ.coeff(sp.Derivative(Z, (r, 2)))
    b = odeZ.coeff(sp.Derivative(Z, r))
    c = sp.expand(odeZ - a * sp.Derivative(Z, (r, 2)) - b * sp.Derivative(Z, r)).coeff(Z)
    a = sp.simplify(a); b = sp.simplify(b); c = sp.simplify(c)
    check_b = sp.simplify(b / a - (sp.diff(nu, r) - sp.diff(la_, r)))
    V = sp.simplify(s ** 2 - sp.exp(2 * (nu - la_)) * c / a)
    # substitute background (matter form); nu itself stays as e^{2 nu} prefactor
    rules = {sp.Derivative(la_, (r, 2)): B['lampp'], sp.Derivative(nu, (r, 2)): B['nupp'],
             sp.Derivative(la_, r): B['lamp'], sp.Derivative(nu, r): B['nup']}
    Vm = V.subs(rules).subs(sp.exp(-2 * la_), B['N']).subs(sp.exp(2 * la_), 1 / B['N'])
    Vm = sp.simplify(Vm.subs(la_, B['lam']))
    mm, rho, pr = B['mm'], B['rho'], B['pr']
    cand = sp.exp(2 * nu) * (l * (l + 1) / r ** 2 - 6 * Gn * mm / r ** 3 + 4 * sp.pi * Gn * (rho - pr))
    diff = sp.simplify(Vm - cand)
    # vacuum check
    vac = sp.simplify(Vm.subs({rho: 0, pr: 0, pt: 0}))
    rw = sp.exp(2 * nu) * (l * (l + 1) / r ** 2 - 6 * Gn * mm / r ** 3)
    return dict(l=l, V=Vm, candidate_difference=diff, vacuum_minus_RW=sp.simplify(vac - rw),
                damping_coeff_check=check_b, separation=sep, h0_solution=h0s, R0=R0)


def main():
    res = {}
    exprs = {}
    for l in (2, 3):
        d = derive(l)
        exprs[l] = d
        res[str(l)] = dict(V=str(d['V']), V_minus_candidate=str(d['candidate_difference']),
                           vacuum_minus_ReggeWheeler=str(d['vacuum_minus_RW']),
                           Zprime_coefficient_minus_nu_minus_lam=str(d['damping_coeff_check']),
                           angular_separation_ok={k: bool(v[0]) for k, v in d['separation'].items()},
                           h0_from_theta_phi=str(d['h0_solution']))
        print(l, res[str(l)], flush=True)
    # numeric evaluation of the derived V on the GR profile (fields physical, G=1e-8)
    prof = np.load(sys.argv[1])
    G = float(prof['G'])
    rr = np.asarray(prof['r'])
    f, h, fp, hp = (np.asarray(prof[k]) for k in ('f', 'h', 'fp', 'hp'))
    alpha = np.asarray(prof['alpha'])
    a = np.asarray(prof['a'])
    N = 1 / a ** 2
    om = float(prof['omega'])
    Om = om / alpha
    M2 = float(prof['M']) ** 2
    g = float(prof['g'])
    lam = float(prof['lambda_total'])
    T = Om ** 2 * (f ** 2 + 4 * h ** 2)
    K = N * (fp ** 2 + hp ** 2)
    Vp = f ** 2 + M2 * h ** 2 - 2 * g * h * f ** 2 + lam * f ** 4
    rho, p_r, p_t = T + K + Vp, T + K - Vp, T - K - Vp
    mass = (1 - N) * rr / (2 * G)
    num = {}
    mm_s, rho_s, pr_s, pt_s = sp.Function('m')(r), sp.Function('rho')(r), sp.Function('p_r')(r), sp.Function('p_t')(r)
    for l in (2, 3, 10):
        if l in exprs:
            Vexpr = exprs[l]['V']
        else:   # l-dependence checked symbolically to enter only via l(l+1) (l=2 vs 3)
            Vexpr = exprs[2]['V'] + sp.exp(2 * nu) * (l * (l + 1) - 6) / r ** 2
        ms, rs_, ps_, qs_, nus, drs = sp.symbols('m_s rho_s pr_s pt_s nu_s drho_s')
        Vsym = Vexpr.subs(sp.Derivative(rho_s, r), drs)
        Vsym = Vsym.subs({mm_s: ms, rho_s: rs_, pr_s: ps_, pt_s: qs_}).subs(nu, nus)
        assert not Vsym.has(sp.Derivative), Vsym
        fn0 = sp.lambdify((r, ms, rs_, ps_, qs_, nus, Gn, drs), Vsym, 'numpy')
        drho = np.gradient(rho, rr)
        fn = lambda *args: fn0(*args, drho)
        res.setdefault('V_depends_on', {})[str(l)] = sorted(str(s_) for s_ in Vsym.free_symbols)
        Vn = fn(rr, mass, rho, p_r, p_t, np.log(alpha), G)
        Vflat = l * (l + 1) / rr ** 2
        sel = rr > 0.5
        num[str(l)] = dict(min_V_times_r2=float(np.min(Vn[sel] * rr[sel] ** 2)),
                           max_rel_dev_from_flat=float(np.max(np.abs(Vn[sel] / Vflat[sel] - 1))),
                           V_positive=bool(np.all(Vn[sel] > 0)))
    res['numeric_on_GR_profile'] = num
    res['max_2Gm_over_r'] = float(np.max(2 * G * mass[rr > 1] / rr[rr > 1]))
    res['runtime_s'] = tm()
    res['peak_rss_MB'] = peak_rss_mb()
    dump(sys.argv[2], res)


if __name__ == '__main__':
    main()
