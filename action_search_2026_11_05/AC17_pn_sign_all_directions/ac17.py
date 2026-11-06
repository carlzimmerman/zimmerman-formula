"""AC17: relativistic UV symbol of the khronon/polarization scalar, every direction (criteria 5c1c453e79).
Kappa = 1/2 FITTED; not theory closed. Single thread. AC17_MUTATE=1 flips gamma (separate outputs)."""
import os, sys, json, time, hashlib
import sympy as sp, mpmath as mp
MUT = os.environ.get('AC17_MUTATE') == '1'
tag = '_MUTATE' if MUT else ''
D = os.path.dirname(os.path.abspath(__file__))
t0 = time.time(); checks = []; out = {}
def check(name, ok, info=''):
    checks.append(dict(name=name, ok=bool(ok), info=info)); print(('PASS ' if ok else 'FAIL ') + name + ' ' + info, flush=True)

t, x, y, z = sp.symbols('t x y z', real=True); X = (x, y, z); C = (t, x, y, z)
eps = sp.Symbol('epsilon'); gam0, mu, K, phd = sp.symbols('gamma mu K phidot0', positive=True)
gam = -gam0 if MUT else gam0
N = sp.Function('N')(*X); Ps = sp.Function('Psi')(*X)
P0 = [sp.Function(f'P{i}')(*X) for i in (1, 2, 3)]
W1 = sp.Function('W1')(*X); W2 = sp.Function('W2')(*X)
sig = sp.Function('sigma')(*C); n = sp.Function('n')(*C)
p = [sp.Function(f'p{i}')(*C) for i in (1, 2, 3)]

def lagrangian(model, with_n_gravity=False):
    Nf = N + eps * n; S = eps * sig; Pi = [P0[i] + eps * p[i] for i in range(3)]
    st = 1 + sp.diff(S, t); si = [sp.diff(S, v) for v in X]
    Xt = st**2 / Nf**2 - Ps**-4 * sum(a**2 for a in si)          # -g^{mu nu} d tau d tau
    Pt = -sum(Pi[i] * si[i] for i in range(3)) / st              # P orthogonal to u
    Pmu = [Pt] + Pi
    lnNt = -sp.log(Xt) / 2
    Pa = sum(Pmu[m] * sp.diff(lnNt, C[m]) for m in range(4))     # P^mu a_mu = P^nu d_nu ln N_tau
    sg = Nf * Ps**6
    s = sum(sp.diff(sg * Pmu[m], C[m]) for m in range(4)) / sg - Pa   # leaf divergence D.P
    P2 = -Nf**2 * Pt**2 + Ps**4 * sum(a**2 for a in Pi)
    dx = K * sp.sqrt(P2) - K * sp.sqrt(Ps**4 * sum(a**2 for a in P0))
    Q = sp.sqrt(Xt)
    L = sg * (Pa - (W1 * dx + W2 * dx**2 / 2) + mu**2 * (Q - 1)**2 / (2 * K))
    if model == 'v3s':
        L += sg * (-gam / 2 * s**2)
    else:                                                        # AC2q on-region: -(g/2)(s^2+4sX) + X - V
        Xc = phd**2 / 2 * Xt
        L += sg * (-gam / 2 * (s**2 + 4 * s * Xc) + Xc)
    if with_n_gravity:                                           # PN-order lapse gravity (V3X: -|grad dphi|^2/2K)
        L += -Ps**2 * N * sum(sp.diff(eps * n, v)**2 for v in X) / (2 * K)
    return sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2)

def EL(L, f):
    o = sp.diff(L, f)
    for d in [d for d in L.atoms(sp.Derivative) if d.expr == f]:
        term = sp.diff(L, d)
        for v in d.variables: term = sp.diff(term, v)
        o += (-1)**len(d.variables) * term
    return o

lam, w = sp.symbols('lambda omega'); k = sp.symbols('k1:4', real=True)
Fs = sp.symbols('S Pp1 Pp2 Pp3 Nn'); fields = [sig] + p + [n]
ph = sp.exp(sp.I * lam * (k[0] * x + k[1] * y + k[2] * z - w * t))
def freeze(e):
    rep = {d: sp.Symbol(str(d.expr.func) + '_' + ''.join(str(v) for v in d.variables))
           for d in sorted(e.atoms(sp.Derivative), key=lambda d: -len(d.variables))}
    e = e.xreplace(rep)
    r2 = {N: sp.Symbol('N0', positive=True), Ps: sp.Symbol('Psi0', positive=True), W1: sp.Symbol('w1'), W2: sp.Symbol('w2')}
    for i in range(3): r2[P0[i]] = sp.Symbol(f'q{i+1}')
    return e.xreplace(r2)
def symbol_eqs(L2):
    eqs = []
    for f in fields:
        e = sp.expand(EL(L2, f).subs({fields[i]: Fs[i] * ph for i in range(5)}).doit() / ph)
        eqs.append(e)
    return eqs

N0, Psi0 = sp.symbols('N0 Psi0', positive=True); q = sp.symbols('q1:4'); w1 = sp.Symbol('w1')
kk = sum(a**2 for a in k); qn = sp.sqrt(sum(a**2 for a in q))
xs, ys, zs = X
Nfn, Psfn = N, Ps
s0f = sum(sp.diff(Ps**6 * P0[i], X[i]) for i in range(3)) / Ps**6
PdNs = sum(P0[i] * sp.diff(N * s0f, X[i]) for i in range(3)) / N
PdlnN = sum(P0[i] * sp.diff(N, X[i]) for i in range(3)) / N

res = {}
for model in ['v3s', 'AC2q']:
    L2 = lagrangian(model)
    eqs = symbol_eqs(L2)
    degs = [sp.Poly(e, lam).degree() for e in eqs]
    check(f'G1-UVcount [{model}]', max(degs[:4]) == 2 and degs[4] <= 1,
          f'lambda degrees of EL(sigma,p1,p2,p3,n) = {degs}; no 3rd/4th-derivative terms survive')
    # lapse couples only at lambda^1 to (sigma,p): subprincipal once n has its own k^2 term
    ncoup = [sp.expand(eqs[a]).coeff(lam, 2).coeff(Fs[4]) for a in range(4)]
    check(f'G1-lapse-subprincipal [{model}]', all(c == 0 for c in ncoup), 'n enters sigma/p equations below lambda^2')
    Lg = lagrangian(model, with_n_gravity=True); en = symbol_eqs(Lg)[4]
    ok_n = sp.Poly(en, lam).degree() == 2 and sp.simplify(sp.expand(en).coeff(lam, 2) - sp.expand(en).coeff(lam, 2).coeff(Fs[4]) * Fs[4]) == 0
    check(f'G1-lapse-gravity [{model}]', ok_n, 'with -|grad n|^2 gravity the n equation at lambda^2 is n alone, so n -> 0 at principal order')
    M = sp.zeros(4, 4)
    for a in range(4):
        c2 = sp.expand(eqs[a].subs(Fs[4], 0)).coeff(lam, 2)
        for b in range(4): M[a, b] = freeze(c2.coeff(Fs[b]))
    # longitudinal reduction p = Pi k/|k|; transverse p has zero principal part (auxiliary)
    kv = sp.Matrix(k); pblock = M[1:, 1:]
    trans_ok = sp.simplify(pblock + N0 * Psi0**6 * gam * kv * kv.T) == sp.zeros(3, 3) if model == 'v3s' else None
    A = sp.simplify(M[0, 0].coeff(w, 2)); m0 = sp.expand(M[0, 0].subs(w, 0))
    cpl = [sp.factor(M[0, b + 1] / (k[b] * w)) for b in range(3)]
    cpl_sym = [sp.factor(M[b + 1, 0] / (k[b] * w)) for b in range(3)]
    same = all(sp.simplify(c - cpl[0]) == 0 for c in cpl + cpl_sym)
    pL = sp.factor(M[1, 1] / k[0]**2)
    check(f'G1-structure [{model}]', same and all(sp.simplify(M[a, b] - pL * k[a - 1] * k[b - 1]) == 0 for a in range(1, 4) for b in range(1, 4)),
          f'p block = {pL} k k^T (longitudinal only), coupling = {cpl[0]} * omega * k, symmetric')
    s0 = freeze(s0f)
    G_W = -m0.coeff(w1) * w1; G_rest = -(m0 - m0.coeff(w1) * w1)
    iso = sp.simplify(G_rest / kk)
    check(f'G1-isotropic-part [{model}]', all(sp.diff(iso, kv_) == 0 for kv_ in k), 'non-W part of the gradient weight is proportional to |k|^2')
    # closed form: G = N^3 Psi^2 [ s + P.a + gamma s^2 + gamma P.grad(N s)/N + mu^2(1-N)/(K N^2) ] - K N^3 Psi^4 w1 (k.q)^2/|q|
    cand = N0**3 * Psi0**2 * (s0 + freeze(PdlnN) + gam * s0**2 + gam * freeze(PdNs) + mu**2 * (1 - N0) / (K * N0**2))
    if model == 'AC2q':
        cand_extra = sp.simplify(iso - cand)
    else:
        cand_extra = 0
    r_iso = sp.simplify(sp.expand(iso - cand)) if model == 'v3s' else None
    r_W = sp.simplify(G_W - (-K * N0**3 * Psi0**4 * w1 * sum(k[i] * q[i] for i in range(3))**2 / qn))
    if model == 'v3s':
        check('G1-closed-form [v3s]', r_iso == 0 and r_W == 0,
              'G(k) = N^3 Psi^2 |k|^2 [s + P.a + gamma s^2 + gamma P.grad(Ns)/N + mu^2(1-N)/(K N^2)] - K N^3 Psi^4 W1 (k.P)^2/|P|_flat (residual 0)')
    res[model] = dict(A=A, cpl=cpl[0], pL=pL, iso=iso, G_W=G_W, extra=cand_extra, degs=degs)
    print(model, 'done', round(time.time() - t0, 1), flush=True)

# --- on-shell form. Background P equation (variation of the zeroth-order action):
#   N Psi^6 [d_i ln N - W1 K Psi^4 q_i/(Psi^2 |q|)] + gamma Psi^6 d_i(N s) = 0   =>   K Psi^2 W1 qhat = a + gamma grad(N s)/N.
# Contracting with P: P.a + gamma P.grad(Ns)/N = K Psi^2 W1 |q|. Hence
#   G(khat) = N^3 Psi^2 |k|^2 [ B_tau + K Psi^2 W1 |q| (1 - (khat.qhat)^2) ],   B_tau = s + gamma s^2 + mu^2(1-N)/(K N^2).
L0 = N * Ps**6 * (sum(P0[i] * sp.diff(N, X[i]) for i in range(3)) / N - gam / 2 * s0f**2)
EP = []
for i in range(3):
    e = sp.diff(L0, P0[i])
    for d in [d for d in L0.atoms(sp.Derivative) if d.expr == P0[i]]:
        term = sp.diff(L0, d)
        for v in d.variables: term = sp.diff(term, v)
        e += (-1)**len(d.variables) * term
    EP.append(sp.expand(e))
claimed = [N * Ps**6 * sp.diff(N, X[i]) / N + gam * Ps**6 * sp.diff(N * s0f, X[i]) for i in range(3)]
check('G1-background-P-equation', all(sp.simplify(EP[i] - claimed[i]) == 0 for i in range(3)),
      'E_P (W part aside) = N Psi^6 d_i ln N + gamma Psi^6 d_i(N s) exactly')

v = res['v3s']; khat_q = sp.Symbol('c_theta')
B_tau_s = sp.Symbol('s') + gam * sp.Symbol('s')**2 + mu**2 * (1 - N0) / (K * N0**2)
# dispersion: A_eff omega^2 = G |k|^2, A_eff = A + cpl^2/(-pL)... (Pi eliminated from the longitudinal row)
cpl = v['cpl']; pL = v['pL']; A = v['A']
A_eff = sp.simplify(A - cpl**2 / pL)
print('A_eff v3s =', sp.factor(A_eff))
check('G1-kinetic [v3s]', sp.simplify(A_eff - Psi0**6 * (N0 * (1 + gam * freeze(s0f))**2 / gam + mu**2 / (K * N0))) == 0,
      'A_eff = Psi^6 [N (1+gamma s)^2/gamma + mu^2/(K N)] (> 0 for gamma > 0)')
out['closed_form'] = {
    'principal_symbol': 'omega^2 [N Psi^6 (1+gamma s)^2/gamma + Psi^6 mu^2/(K N)] = |k|^2 N^3 Psi^2 [B_tau + x0 W1 sin^2(theta_kP)] (v3s, on shell)',
    'physical_speed': 'c^2(khat) = gamma [B_tau + x0 W\'(x0) sin^2 theta] / [(1+gamma s)^2 + gamma mu^2/(K N^2)],  x0 = K|P|',
    'A_eff_v3s': str(sp.factor(A_eff)), 'coupling_v3s': str(cpl), 'p_long_v3s': str(pL),
    'AC2q_extra_vs_v3s_isotropic_weight': str(sp.factor(res['AC2q']['extra'])),
    'AC2q_A': str(sp.factor(res['AC2q']['A'])), 'AC2q_coupling': str(res['AC2q']['cpl']), 'AC2q_pL': str(res['AC2q']['pL']),
}
print(json.dumps(out['closed_form'], indent=1), flush=True)
json.dump(dict(symbolic={m: {kk_: str(vv) for kk_, vv in res[m].items()} for m in res}),
          open(os.path.join(D, f'ac17_symbolic{tag}.json'), 'w'), indent=1)
json.dump(dict(checks=checks, closed_form=out['closed_form']), open(os.path.join(D, f'ac17_stage1{tag}.json'), 'w'), indent=1)

# --- on-shell identities, both models: G - N^3 Psi^2 |k|^2 [B_model + K Psi^2 W1 |q| (1-(khat.qhat)^2)]
#     = N^3 Psi^2 |k|^2 [P.a + gamma P.grad(N s_eff)/N - K Psi^2 W1 |q|]  (the contracted background P equation)
X0 = phd**2 / (2 * N**2)
for model in ['v3s', 'AC2q']:
    r_ = res[model]
    G = r_['iso'] * kk + r_['G_W']
    seff = s0f if model == 'v3s' else s0f + 2 * X0
    Bm = freeze(s0f + gam * s0f**2 + mu**2 * (1 - N) / (K * N**2))
    if model == 'AC2q': Bm += freeze(2 * X0 * (1 - gam * s0f))
    Pcon = freeze(PdlnN + gam * sum(P0[i] * sp.diff(N * seff, X[i]) for i in range(3)) / N) - K * Psi0**2 * w1 * qn
    kq = sum(k[i] * q[i] for i in range(3))
    target = N0**3 * Psi0**2 * (kk * Bm + K * Psi0**2 * w1 * qn * (kk - kq**2 / qn**2)) + N0**3 * Psi0**2 * kk * Pcon
    r0 = sp.simplify(sp.expand(G - target))
    check(f'G1-on-shell [{model}]', r0 == 0, 'G = N^3 Psi^2 |k|^2 [B + x0 W1 sin^2 theta] + (contracted P equation) x ..., residual 0'
          + ('; B_AC2q = B_tau + 2X (1 - gamma s)' if model == 'AC2q' else '; B_v3s = B_tau'))
    Aeff = sp.simplify(r_['A'] - r_['cpl']**2 / r_['pL'])
    res[model]['A_eff'] = Aeff
    if model == 'AC2q':
        tgt = Psi0**6 * (N0 * (1 + gam * freeze(s0f) - 2 * gam * freeze(X0))**2 / gam + mu**2 / (K * N0) + phd**2 * (1 - 2 * gam * freeze(s0f)) / N0)
        check('G1-kinetic [AC2q]', sp.simplify(Aeff - tgt) == 0, 'A_eff = Psi^6 [N (1+gamma s-2 gamma X)^2/gamma + mu^2/(K N) + phidot^2 (1-2 gamma s)/N]')
out['closed_form']['B_AC2q'] = 'B_tau + 2X(1 - gamma s) + x0 W1 sin^2 theta;  kinetic Psi^6 [N(1+gamma s-2 gamma X)^2/gamma + mu^2/(KN) + phidot^2(1-2 gamma s)/N]'
out['closed_form']['c2_AC2q'] = 'c^2 = gamma [B_tau + 2X(1-gamma s) + x0 W1 sin^2 theta] / [(1+gamma s-2 gamma X)^2 + gamma mu^2/(K N^2) + gamma phidot^2 (1-2 gamma s)/N^2]'

# --- K3 (GR limit): P sector removed (P0 = p = 0, W = 0) with gamma = mu = 0 -> L2 identically 0
L2v = lagrangian('v3s')
k3 = sp.simplify(L2v.subs({W1: 0, W2: 0}).subs({P0[0]: 0, P0[1]: 0, P0[2]: 0}).subs({p[0]: 0, p[1]: 0, p[2]: 0}).subs({mu: 0}).doit())
check('K3 GR limit', k3 == 0, 'P sector removed (P0 = p = 0, W = 0) and mu = 0: second-order Lagrangian is identically 0 (sigma pure gauge). '
      'Criteria wording corrected: with P0 = 0 but p kept, sigma still couples to p (P is an independent field), so that is not the GR limit.')

# --- K1 (independent numerical chain): spherical Schwarzschild-isotropic + hedgehog, k radial; omega^2 from the 4x4 symbol
#     determinant (with W1 from the radial P equation) vs AZ36's c_rad^2 formula.
mp.mp.dps = 50
pc = mp.mpf('3.0856775814913673e16'); AU = mp.mpf('1.495978707e11'); Msun = mp.mpf('1476.6250')   # GM/c^2 in m
cSI = mp.mpf(299792458)
FOOT = {'canonical': dict(Ls=mp.mpf('21.68') * pc, gphi2=mp.mpf('2.4e-17')), 'alt': dict(Ls=mp.mpf('22.85') * pc, gphi2=mp.mpf('4.0e-17'))}
Kn = 4 * mp.pi; mun = 1 / (100000 * pc)
rS = sp.sqrt(xs**2 + ys**2 + zs**2)
def background(Ls, gext, e_ext, Pext_mag):
    Nsch = (1 - Msun / (2 * rS)) / (1 + Msun / (2 * rS)); Psb = 1 + Msun / (2 * rS)
    Nb = Nsch * sp.exp(gext * zs)                                    # Sun + uniform external field along z
    f = Msun / (4 * sp.pi * Ls**2) / Psb**6                           # hedgehog: s = M/(2 pi L^2 r) Psi^-6
    Pb = [f * X[i] / rS + Pext_mag * e_ext[i] for i in range(3)]
    return Nb, Psb, Pb
Lsy, gsy, Pms, e1s, e2s, e3s = sp.symbols('Lsy gsy Pms e1s e2s e3s')
_NbS, _PsbS, _PbS = background(Lsy, gsy, (e1s, e2s, e3s), Pms)
_cache = {}
def _fn(nm):
    if nm not in _cache:
        base = {'N': _NbS, 'Psi': _PsbS, 'P1': _PbS[0], 'P2': _PbS[1], 'P3': _PbS[2]}
        if nm == 'N0': e = base['N']
        elif nm == 'Psi0': e = base['Psi']
        elif nm in ('q1', 'q2', 'q3'): e = _PbS[int(nm[1]) - 1]
        else:
            fn, ders = nm.split('_')[0], nm.split('_')[1]; e = base[fn]
            for ch in ders: e = sp.diff(e, {'x': xs, 'y': ys, 'z': zs}[ch])
        _cache[nm] = sp.lambdify((xs, ys, zs, Lsy, gsy, Pms, e1s, e2s, e3s), e, 'mpmath')
    return _cache[nm]
def point_values(expr_syms, pars, pt):
    vals = {}
    for sym in expr_syms:
        nm = str(sym)
        if nm in ('N0', 'Psi0', 'q1', 'q2', 'q3') or ('_' in nm and nm.split('_')[0] in ('N', 'Psi', 'P1', 'P2', 'P3')):
            vals[sym] = mp.mpf(_fn(nm)(pt[0], pt[1], pt[2], *pars))
    return vals

def fib_dirs(n):
    ga = mp.pi * (3 - mp.sqrt(5)); outd = []
    for i in range(n):
        zz = 1 - 2 * (mp.mpf(i) + mp.mpf(1) / 2) / n; rr = mp.sqrt(1 - zz**2)
        outd.append((rr * mp.cos(ga * i), rr * mp.sin(ga * i), zz))
    return outd

# K1: radial symbol vs AZ36
Mv = res['v3s']
Bt_sym = freeze(s0f + gam * s0f**2 + mu**2 * (1 - N) / (K * N**2))
k1rows = []
for foot, F in FOOT.items():
    Ls = F['Ls']; gnum = Kn * Ls**2 / 2
    Nb, Psb, Pb = background(Ls, 0, (0, 0, 1), 0); pars = (Ls, 0, 0, 0, 0, 1)
    for rAU in [1, 10, 100, 1000]:
        pt = (rAU * AU, 0, 0)
        exprs = [Mv['A'], Mv['cpl'], Mv['pL'], Mv['iso'], Mv['G_W'], Bt_sym]
        syms = set().union(*[e.free_symbols for e in exprs])
        vals = point_values(syms, pars, pt)
        sub = dict(vals); sub.update({K: Kn, gam0: gnum, mu: mun, phd: 0})
        # W1 from the radial P equation: K Psi^2 W1 = qhat.(a + gamma grad(N s)/N)
        aN = sp.diff(sp.log(Nb), xs); sN = (Nb * s0f.subs({Ps: Psb, P0[0]: Pb[0], P0[1]: Pb[1], P0[2]: Pb[2]}).doit())
        rhs = (aN + (gam.subs(gam0, gnum)) * sp.diff(sN, xs) / Nb).subs({xs: pt[0], ys: 0, zs: 0})
        w1n = mp.mpf(str(sp.N(rhs, 60))) / (Kn * vals[Psi0]**2)
        sub[sp.Symbol('w1')] = w1n
        ev = lambda e: mp.mpf(str(sp.N(e.subs({k[0]: 1, k[1]: 0, k[2]: 0}).xreplace(sub), 60)))
        A_, c_, pL_ = ev(Mv['A']), ev(Mv['cpl']), ev(Mv['pL'])
        G_ = ev(Mv['iso']) + ev(Mv['G_W'])
        om2 = G_ / (A_ - c_**2 / pL_)
        c2 = om2 * vals[Psi0]**4 / vals[N0]**2
        sv = ev(freeze(s0f)); Nv = vals[N0]; gv = gam.subs(gam0, gnum); gv = mp.mpf(str(gv))
        c2_az = gv * (sv + gv * sv**2 + mun**2 * (1 - Nv) / (Kn * Nv**2)) / ((1 + gv * sv)**2 + gv * mun**2 / (Kn * Nv**2))
        k1rows.append(dict(foot=foot, r_AU=rAU, c2_symbol=mp.nstr(c2, 20), c2_AZ36=mp.nstr(c2_az, 20), rel=mp.nstr(abs(c2 / c2_az - 1), 3)))
k1max = max(mp.mpf(r['rel']) for r in k1rows)
check('K1 radial = AZ36', k1max < mp.mpf('1e-30'), f'4x4 symbol (W1 from the radial P equation) vs AZ36 c_rad^2: max rel {mp.nstr(k1max, 3)} over 8 rows')

# G2: Solar background with external field, all directions, both footings, both models
kdirs = fib_dirs(400); edirs = fib_dirs(13)
g2 = []; minB_ratio = mp.inf; minc2 = mp.inf; neg = 0; k2rel = mp.mpf(0)
for model in ['v3s', 'AC2q']:
    r_ = res[model]
    Bm_sym = freeze(s0f + gam * s0f**2 + mu**2 * (1 - N) / (K * N**2)) + (freeze(2 * X0 * (1 - gam * s0f)) if model == 'AC2q' else 0)
    argsyms = sorted((Bm_sym.free_symbols | r_['A_eff'].free_symbols | freeze(s0f).free_symbols), key=str)
    _lB = sp.lambdify(argsyms, Bm_sym, 'mpmath'); _lA = sp.lambdify(argsyms, r_['A_eff'], 'mpmath'); _lS = sp.lambdify(argsyms, freeze(s0f), 'mpmath')
    fB = lambda sub: mp.mpf(_lB(*[sub[a_] for a_ in argsyms])); fA = lambda sub: mp.mpf(_lA(*[sub[a_] for a_ in argsyms]))
    fS = lambda sub: mp.mpf(_lS(*[sub[a_] for a_ in argsyms]))
    for foot, F in FOOT.items():
        Ls = F['Ls']; gnum = Kn * Ls**2 / 2; ph2 = F['gphi2'] / gnum if model == 'AC2q' else 0
        for gSI in ['1.9e-10', '2.3e-10']:
            gext = mp.mpf(gSI) / cSI**2; Pext = gext / Kn                   # unscreened bound |P_ext| = g_ext/(K c^2)
            for ie, e in enumerate(edirs):
                pars = (Ls, gext, Pext, e[0], e[1], e[2])
                for rAU in [1, 3, 10, 30, 100, 300, 1000]:
                    pt = (rAU * AU, 0, 0)
                    syms = set(argsyms)
                    vals = point_values(syms | {sp.Symbol('q1'), sp.Symbol('q2'), sp.Symbol('q3')}, pars, pt)
                    sub = dict(vals); sub.update({K: Kn, gam0: gnum, mu: mun, phd: mp.sqrt(ph2)})
                    Bv = fB(sub); Ae = fA(sub)
                    Nv, Pv = vals[N0], vals[Psi0]
                    qv = [vals[sp.Symbol(f'q{i}')] for i in (1, 2, 3)]; qn_ = mp.sqrt(sum(a**2 for a in qv))
                    x0 = Kn * Pv**2 * qn_; sv = fS(sub)
                    for Mf in [1, mp.mpf('3.2'), mp.mpf('10.24')]:
                        W1v = Mf * x0 / Kn
                        for kd in kdirs:
                            ct = sum(kd[i] * qv[i] for i in range(3)) / qn_
                            Bk = Bv + x0 * W1v * (1 - ct**2)
                            om2 = Nv**3 * Pv**2 * Bk / Ae                       # per |k|^2
                            c2 = om2 * Pv**4 / Nv**2
                            if c2 <= 0 or Bk <= 0 or Ae <= 0: neg += 1
                            minB_ratio = min(minB_ratio, Bk / sv); minc2 = min(minc2, c2)
                    if model == 'v3s' and ie == 0:
                        gv = mp.mpf(str(sp.N(gam.subs(gam0, gnum)))); k2rel = max(k2rel, abs((Nv**3 * Pv**2 * Bv / Ae * Pv**4 / Nv**2) / (gv * sv) - 1))
                    g2.append(dict(model=model, foot=foot, g_ext=gSI, edir=ie, r_AU=rAU, B_over_s_alongP=mp.nstr(Bv / sv, 12),
                                   c2_alongP=mp.nstr(Nv**3 * Pv**2 * Bv / Ae * Pv**4 / Nv**2, 12), gamma_s=mp.nstr(mp.mpf(str(sp.N(gam.subs(gam0, gnum)))) * sv, 6),
                                   x0W1_over_s_max=mp.nstr(x0 * 10.24 * x0 / Kn / sv, 4)))
    print(model, 'G2 done', round(time.time() - t0, 1), flush=True)
npts = 2 * 2 * 2 * 13 * 7 * 3 * 400
if not MUT:
    check('G2 Solar background, all directions', neg == 0, f'{npts} (model, footing, g_ext, P_ext dir, node, W1 bracket, k dir) points: '
          f'{neg} with B <= 0, A_eff <= 0 or c^2 <= 0; min B/s = {mp.nstr(minB_ratio, 12)}; min c^2 = {mp.nstr(minc2, 6)}')
    check('K2 PN limit', k2rel < mp.mpf('1e-6'), f'c^2 along P vs V3X gamma rho_tau: max rel {mp.nstr(k2rel, 4)} (O(gamma s) ~ |Phi| corrections)')
else:
    check('MUTATE bites (gamma -> -gamma)', neg == npts, f'{neg}/{npts} points with c^2 <= 0 (must be all); max c^2 = see json')
lab = 'PASS' if (not MUT and all(c['ok'] for c in checks)) else ('MUTATE' if MUT else 'FAIL/NO VERDICT (see checks)')
res_out = dict(label=lab, checks=checks, closed_form=out['closed_form'], K1=k1rows, G2_alongP_rows=g2,
               min_B_over_s=mp.nstr(minB_ratio, 15), min_c2=mp.nstr(minc2, 10), n_points=npts, n_bad=neg,
               inputs=dict(Msun_m=str(Msun), mu_inv_kpc=100, footings={k_: dict(Ls_pc=str(v_['Ls'] / pc), gamma_phidot2=str(v_['gphi2'])) for k_, v_ in FOOT.items()}),
               script_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest(),
               note='kappa = 1/2 FITTED; not theory closed', runtime_s=round(time.time() - t0, 1))
json.dump(res_out, open(os.path.join(D, f'ac17{tag}.json'), 'w'), indent=1)
print('LABEL', lab, flush=True)
sys.exit(0 if (lab == 'PASS' or (MUT and checks[-1]['ok'])) else 1)
