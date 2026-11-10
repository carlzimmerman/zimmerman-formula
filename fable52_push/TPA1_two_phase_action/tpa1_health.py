"""TPA1 item 6: health of the two-phase action.  Criteria: FROZEN_CRITERIA.md (b81c28d00c).

Decoupling limit: the metric is frozen at a static weak background ds^2 = -N(x)^2 dt^2 + dx^2 + dy^2, gamma_L = 0, and P is
eliminated exactly by the Legendre maximum (it enters algebraically), leaving the clock Lagrangian
    L_eff = N [ mu_K^2 (Q - 1)^2/(2K) + S(n_d(Q)) J(|A|) ],   J(A) = (a0^2/K)[A/a0 - ln(1 + A/a0)],   A_m = -h_m^n d_n ln Q .
Background: static clock tau = Q_inf t, so Qbar = Q_inf/N and Abar = d ln N.  Perturbation tau = Q_inf t + pi(t, x, y).
The quadratic Lagrangian L2 is the second derivative of L_eff in the jets of pi.  Its Euler-Lagrange operator is applied to
pi = exp(i(k x + q y - w t)) with the x-dependence of every coefficient kept (derivatives of N and of S(Q(x)) act through the
product rule), giving the local symbol P(w, k, q) at the point x = 0.  K = coefficient of w^2 in Re P (kinetic; K < 0 is a
ghost).  The roots of Re P = 0 in w give the modes; complex roots are an instability (growth rate |Im w|).
Numbers: geometric units (m, kg/m^3, K = 4 pi G/c^2, a0 -> a0/c^2), 60-digit arithmetic.
"""
import os, json, math, time, resource
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()
mp.mp.dps = 60

x = sp.Symbol("x")
K, a0, mu, Qinf = sp.symbols("K a0 mu_K Q_inf", positive=True)
nst, dn = sp.symbols("n_star Delta_n", positive=True)
N0 = sp.Symbol("N0", positive=True)
N1, N2, N3, N4 = sp.symbols("N1 N2 N3 N4")
SG = sp.symbols("sigma0:6")          # S and its Q-derivatives at the background value Qbar0 = Q_inf/N0
Nx = N0 + N1 * x + N2 * x**2 / 2 + N3 * x**3 / 6 + N4 * x**4 / 24       # local Taylor model of the lapse at x0 = 0
PARAMS = [K, a0, mu, Qinf, nst, dn, N0, N1, N2, N3, N4] + list(SG)

def S_of_Q(Q, kind):
    if kind == "S0": return sp.Integer(0)
    if kind == "S1": return sp.Integer(1)
    if kind == "abstract": return sp.Function("S")(Q)
    dq = Q - Qinf / N0                                                     # Taylor polynomial of S(Q) about Qbar0:
    return sum(SG[i] * dq**i / sp.factorial(i) for i in range(6))         # exact for every derivative that enters (<= 4)

pt, px, py, ptt, ptx, pty, pxx, pxy, pyy = sp.symbols("pi_t pi_x pi_y pi_tt pi_tx pi_ty pi_xx pi_xy pi_yy")
JETS = [pt, px, py, ptt, ptx, pty, pxx, pxy, pyy]
DER = {pt: {0: ptt, 1: ptx, 2: pty}, px: {0: ptx, 1: pxx, 2: pxy}, py: {0: pty, 1: pxy, 2: pyy}}
e = sp.Symbol("e")

def L_eff(kind):
    ptE, pxE, pyE = e * pt, e * px, e * py
    Q2 = (Qinf + ptE)**2 / Nx**2 - pxE**2 - pyE**2
    dQ2 = []
    for c in range(3):                     # total derivative of Q2 along t, x, y (jets of pi and the x-dependence of N)
        d = (2 * (Qinf + ptE) * e * DER[pt][c] / Nx**2 - 2 * pxE * e * DER[px][c] - 2 * pyE * e * DER[py][c])
        if c == 1:
            d += -2 * (Qinf + ptE)**2 * sp.diff(Nx, x) / Nx**3
        dQ2.append(d)
    Q = sp.sqrt(Q2)
    dl = [dQ2[c] / (2 * Q2) for c in range(3)]
    ginv = [-1 / Nx**2, 1, 1]
    nlow = [-(Qinf + ptE) / Q, -pxE / Q, -pyE / Q]
    nup = [ginv[i] * nlow[i] for i in range(3)]
    ndl = sum(nup[i] * dl[i] for i in range(3))
    A = [-(dl[m] + nlow[m] * ndl) for m in range(3)]                    # A_m = -h_m^n d_n ln Q
    Amod = sp.sqrt(sum(ginv[i] * A[i]**2 for i in range(3)))
    J = (a0**2 / K) * (Amod / a0 - sp.log(1 + Amod / a0))
    LK = mu**2 * (Q - 1)**2 / (2 * K)
    return Nx * (LK + S_of_Q(Q, kind) * J)

def quadratic(kind):
    L = L_eff(kind)
    L2 = sp.diff(L, e, 2).subs(e, 0) / 2
    C = {}
    for i, a_ in enumerate(JETS):
        for b_ in JETS[i:]:
            c = sp.diff(L2, a_, b_)
            if c != 0:
                C[(a_, b_)] = c
    return L2, C

w, k, q = sp.symbols("omega k q", real=True)
XI = {pt: -sp.I * w, px: sp.I * k, py: sp.I * q, ptt: -w**2, ptx: w * k, pty: w * q, pxx: -k**2, pxy: -k * q, pyy: -q**2}
ORDER = {pt: (1, 0, 0), px: (0, 1, 0), py: (0, 0, 1), ptt: (2, 0, 0), ptx: (1, 1, 0), pty: (1, 0, 1), pxx: (0, 2, 0),
         pxy: (0, 1, 1), pyy: (0, 0, 2)}
def apply_D(f, c):
    if c == 0: return -sp.I * w * f
    if c == 1: return sp.diff(f, x) + sp.I * k * f
    return sp.I * q * f
def symbol(L2):
    """P(w, k, q; x) = sum_alpha (-D)^alpha [ dL2/dJ_alpha on the plane wave ] / exp(i theta)."""
    Ptot = 0
    for a_ in JETS:
        dLa = sp.diff(L2, a_)
        if dLa == 0: continue
        f = dLa.subs({j: XI[j] for j in JETS})
        o = ORDER[a_]
        for c in range(3):
            for _ in range(o[c]):
                f = -apply_D(f, c)
        Ptot += f
    return Ptot

# ------------------------------------------------------------------ build: Hessian coefficients C_ab(x) of L_eff in the jets
res = {"lane": "TPA1", "item": 6, "criteria": "b81c28d00c", "phases": {}}
symb = {}
JZ = {j: 0 for j in JETS}
for kind in ("S0", "S1", "wall"):
    tk = time.time()
    L1 = L_eff(kind).subs(e, 1)
    first = {ja: sp.diff(L1, ja) for ja in JETS}
    C = {}
    for i_, ja in enumerate(JETS):
        for jb in JETS[i_:]:
            c = sp.diff(first[ja], jb).subs(JZ)
            if c != 0:
                C[(ja, jb)] = C[(jb, ja)] = sp.lambdify([x] + PARAMS, c, "mpmath")
    symb[kind] = dict(C=C)
    res["phases"][kind] = {"n_hessian_entries": len(C) // 1, "pi_tt_squared_present": bool((ptt, ptt) in C)}
    P_(f"[{kind}] Hessian of L_eff in the 9 jets: {len(C)} non-zero entries; pi_tt^2 present: {(ptt, ptt) in C} "
       f"(absent = no extra mode); built in {time.time()-tk:.1f}s")

def symbol_num(kind, vals, kv, qv):
    """coefficients (in powers of omega) of P(omega, k, q) at x = 0 from the Hessian, with C_ab'(0), C_ab''(0) by mp.diff."""
    pv = [vals[p_] for p_ in PARAMS]
    I = mp.mpc(0, 1)
    coeff = {}
    def add(pw, val):
        coeff[pw] = coeff.get(pw, mp.mpc(0)) + val
    cache = {}
    for (ja, jb), fn in symb[kind]["C"].items():
        oa, ob = ORDER[ja], ORDER[jb]
        nx = oa[1]
        if (ja, jb) not in cache:
            f = lambda xx: fn(xx, *pv)
            cache[(ja, jb)] = [f(mp.mpf(0))] + [mp.diff(f, mp.mpf(0), j) for j in range(1, nx + 1)]
        ders = cache[(ja, jb)]
        # dL2/dJ_a = sum_b C_ab J_b ; J_b on the plane wave = (i xi)^beta_b ; then (-D)^alpha_a
        # t-part: (-(-i w))^{a_t} (-i w)^{b_t};  y-part: (-(i q))^{a_y} (i q)^{b_y};  x-part: (-1)^{a_x} D_x^{a_x}[C (i k)^{b_x}]
        xpart = mp.mpc(0)
        for j in range(nx + 1):
            xpart += mp.binomial(nx, j) * ders[j] * (I * kv) ** (nx - j)
        xpart *= (-1) ** nx * (I * kv) ** ob[1]
        ypart = (-(I * qv)) ** oa[2] * (I * qv) ** ob[2]
        tcoef = (I) ** oa[0] * (-I) ** ob[0]           # (-(-i w))^{a_t} (-i w)^{b_t} = i^{a_t} (-i)^{b_t} w^{a_t+b_t}
        add(oa[0] + ob[0], xpart * ypart * tcoef)
    deg = max(coeff) if coeff else 0
    return [coeff.get(i, mp.mpc(0)) for i in range(deg + 1)]

# KA6: S = 0 phase against the k-essence result: P = (L_K''/N) w^2 - (N L_K'/Qbar) k^2 at N1 = N2 = ... = 0 (flat)
L2s0, _ = quadratic("S0")
P0 = sp.expand(symbol(L2s0).subs(x, 0)).subs({N1: 0, N2: 0, N3: 0, N4: 0})
Qb_ = Qinf / N0
ka_kess = sp.simplify(P0 - ((mu**2 / K) * N0 * w**2 / N0**2 * 1 - N0 * (mu**2 * (Qb_ - 1) / K) / Qb_ * (k**2 + q**2)))
ka6 = sp.simplify(ka_kess) == 0
res["KA6_kessence_S0"] = dict(pass_=bool(ka6), residual=str(ka_kess))
P_(f"KA6 S = 0 phase equals the k-essence clock (L_K'' w^2/N - N L_K'/Qbar k^2) on a flat background: {'PASS' if ka6 else 'FAIL'}")


# ------------------------------------------------------------------ physical numbers (SI -> geometric)
G, CL, MS, PC = 6.6743e-11, 2.99792458e8, 1.98847e30, 3.0856775814913673e16
MPC, KPC = 1e6 * PC, 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MUK = {"canonical": 8.890e6, "alt": 8.889e6}
Kgeo = mp.mpf(4) * mp.pi * mp.mpf(G) / mp.mpf(CL) ** 2
I0geo = mp.mpf("4.037e-8") / mp.mpf(MPC) ** 2
RHO_MEAN = I0geo / (2 * Kgeo)
LOGM = 10.45

def law_g_derivs(r, Mb, a0v):
    def g(rr):
        gn = mp.mpf(G) * Mb / rr ** 2
        return gn / 2 + mp.sqrt(gn * gn / 4 + gn * a0v)
    return [mp.diff(g, r, n) for n in range(4)]

def background(foot, y, nfac, delta):
    a0v = mp.mpf(A0[foot]); Mb = mp.mpf(10) ** LOGM * mp.mpf(MS)
    r = mp.sqrt(mp.mpf(G) * Mb / (a0v * y))
    gs = law_g_derivs(r, Mb, a0v)
    c2 = mp.mpf(CL) ** 2
    g0, g1, g2, g3 = (gv / c2 for gv in gs)           # geometric Phi', Phi'', Phi''', Phi''''  (N = exp(Phi), N(0) = 1)
    n0 = mp.mpf(1)
    vals = {N0: n0, N1: n0 * g0, N2: n0 * (g1 + g0 ** 2), N3: n0 * (g2 + 3 * g0 * g1 + g0 ** 3),
            N4: n0 * (g3 + 4 * g0 * g2 + 3 * g1 ** 2 + 6 * g0 ** 2 * g1 + g0 ** 4)}
    mug = mp.mpf(MUK[foot]) / mp.mpf(MPC)
    n_star = nfac * RHO_MEAN
    n_here = n_star * (1 + delta)
    Qbar = 1 + Kgeo * n_here / mug ** 2
    vals.update({K: Kgeo, a0: a0v / c2, mu: mug, Qinf: Qbar * n0, nst: n_star, dn: n_star})
    l_w = Kgeo * n_star * n0 ** 2 / (mug ** 2 * Qbar * n0 * vals[N1])          # Delta n / |d n_d/dx|
    S_here = 1 / (1 + mp.exp(delta))
    # the logistic switch S(n) = 1/(1 + exp((n - n_star)/Delta n)), Delta n = n_star, and its Q-derivatives at Qbar
    def S_of_Qnum(Qv):
        nv = mug ** 2 * (Qv - 1) / Kgeo
        return 1 / (1 + mp.exp((nv - n_star) / n_star))
    for i in range(6):
        vals[SG[i]] = mp.diff(S_of_Qnum, Qbar, i) if i else S_of_Qnum(Qbar)
    return vals, dict(r_kpc=float(r / KPC), u=float(gs[0] / a0v), l_w_m=float(l_w), Qbar_minus_1=float(Qbar - 1),
                      n_here=float(n_here), S=float(S_here))

def analyse(kind, vals, kv, qv):
    cs = symbol_num(kind, vals, kv, qv)
    while len(cs) < 3: cs.append(mp.mpc(0))
    a_, b_, c_ = (mp.re(cs[2]), mp.re(cs[1]), mp.re(cs[0]))
    disc = b_ * b_ - 4 * a_ * c_
    if a_ != 0:
        sq = mp.sqrt(disc) if disc >= 0 else mp.mpc(0, mp.sqrt(-disc))
        roots = [(-b_ + sq) / (2 * a_), (-b_ - sq) / (2 * a_)]
    else:
        roots = []
    growth = max((abs(mp.im(rt)) for rt in roots), default=mp.mpf(0))
    w2 = -c_ / a_ if a_ != 0 else mp.nan
    return dict(K=float(a_), c1=float(b_), c0=float(c_), w2=float(w2), max_growth_per_m=float(growth),
                ghost=bool(a_ < 0), unstable=bool(disc < 0), omega_degree=len(cs) - 1,
                higher_w=[float(mp.re(c)) for c in cs[3:]],
                imag_parts=[float(mp.im(cs[0])), float(mp.im(cs[1])), float(mp.im(cs[2]))])

def decompose(vals, kv, qv):
    """the kinetic coefficient with S held at its local value (sigma_1.. = 0) and with only sigma_1 kept, for the record."""
    out = {}
    for tag, keep in (("S_held", 0), ("S_and_SQ", 1), ("S_SQ_SQQ", 2), ("full", 5)):
        v2 = dict(vals)
        for i in range(keep + 1, 6):
            v2[SG[i]] = mp.mpf(0)
        an = analyse("wall", v2, kv, qv)
        out[tag] = dict(K=an["K"], c0=an["c0"], w2=an["w2"])
    return out

TABLE = []
for foot in ("canonical", "alt"):
    for nfac in (1, 1000, 1000000):
        for yv in ("0.01", "0.1", "1", "10"):
            for delta in ("-1.5", "-0.5", "0", "0.5", "1.5"):
                vals, info = background(foot, mp.mpf(yv), mp.mpf(nfac), mp.mpf(delta))
                lw = mp.mpf(info["l_w_m"])
                for kap in (10, 1000, 100000):
                    for direction in ("longitudinal", "tangential"):
                        kv = kap / lw if direction == "longitudinal" else 0
                        qv = kap / lw if direction == "tangential" else 0
                        an = analyse("wall", vals, kv, qv)
                        TABLE.append(dict(footing=foot, n_star_over_mean=nfac, y=float(yv), delta=float(delta), k_lw=kap,
                                          direction=direction, **info, **an))
    P_(f"wall grid done for {foot}: {sum(1 for r in TABLE if r['footing'] == foot)} rows")

PH = []
for kind in ("S0", "S1"):
    for foot in ("canonical", "alt"):
        for nfac in (1, 1000, 1000000):
            for yv in ("0.01", "0.1", "1", "10"):
                vals, info = background(foot, mp.mpf(yv), mp.mpf(nfac), mp.mpf(0))
                lw = mp.mpf(info["l_w_m"])
                for kap in (10, 1000, 100000):
                    for direction in ("longitudinal", "tangential"):
                        kv = kap / lw if direction == "longitudinal" else 0
                        qv = kap / lw if direction == "tangential" else 0
                        an = analyse(kind, vals, kv, qv)
                        PH.append(dict(phase=kind, footing=foot, n_star_over_mean=nfac, y=float(yv), k_lw=kap,
                                       direction=direction, **info, **an))
# KA6 numeric: S = 0 on a flat background equals the k-essence clock exactly (K = L_K''/N, -c0/k^2 = N L_K'/Qbar)
vals, info = background("canonical", mp.mpf(1), mp.mpf(1), mp.mpf(0))
for nn in (N1, N2, N3, N4): vals[nn] = mp.mpf(0)
kv = mp.mpf(10) / mp.mpf(info["l_w_m"])
cs = symbol_num("S0", vals, kv, 0)
Qb = vals[Qinf] / vals[N0]
K_exp = vals[mu] ** 2 / vals[K] / vals[N0]
G_exp = vals[N0] * vals[mu] ** 2 * (Qb - 1) / vals[K] / Qb
relK = abs(mp.re(cs[2]) / K_exp - 1); relG = abs(-mp.re(cs[0]) / kv ** 2 / G_exp - 1)
res["KA6_numeric"] = dict(rel_K=float(relK), rel_G=float(relG), pass_=bool(relK < 1e-30 and relG < 1e-20))
P_(f"KA6 (numeric, the symbol machinery itself): S = 0 flat background vs k-essence: rel K {float(relK):.1e}, rel G {float(relG):.1e} "
   f"-> {'PASS' if res['KA6_numeric']['pass_'] else 'FAIL'}")
ph_unst = [r for r in PH if r["unstable"]]
if ph_unst:
    slow = min(ph_unst, key=lambda r: r["max_growth_per_m"]); fast = max(ph_unst, key=lambda r: r["max_growth_per_m"])
    res["phase_growth"] = dict(fastest_efold_yr=1 / (fast["max_growth_per_m"] * CL) / 3.15576e7,
                               slowest_efold_yr=1 / (slow["max_growth_per_m"] * CL) / 3.15576e7,
                               unstable_by_phase={k_: sum(1 for r in ph_unst if r["phase"] == k_) for k_ in ("S0", "S1")},
                               unstable_S1_by_nstar={str(nf): sum(1 for r in ph_unst if r["phase"] == "S1" and r["n_star_over_mean"] == nf)
                                                     for nf in (1, 1000, 1000000)},
                               S1_rows_by_nstar={str(nf): sum(1 for r in PH if r["phase"] == "S1" and r["n_star_over_mean"] == nf)
                                                 for nf in (1, 1000, 1000000)})
    P_(f"phase instability: {res['phase_growth']['unstable_by_phase']}; S1 unstable rows by n_star/mean "
       f"{res['phase_growth']['unstable_S1_by_nstar']} of {res['phase_growth']['S1_rows_by_nstar']}; e-fold "
       f"{res['phase_growth']['fastest_efold_yr']:.3g} to {res['phase_growth']['slowest_efold_yr']:.3g} yr")
    for r in PH:
        if r["phase"] == "S1" and r["k_lw"] == 10 and r["direction"] == "longitudinal" and r["footing"] == "canonical":
            P_(f"  S1 canonical n*/mean {r['n_star_over_mean']:>7g} y {r['y']:>5g}: K {r['K']:+.3e} c0 {r['c0']:+.3e} w^2 {r['w2']:+.3e} "
               f"unstable {r['unstable']}" + (f" (e-fold {1/(r['max_growth_per_m']*CL)/3.15576e7:.3g} yr)" if r['unstable'] else ""))

DEC = []
for foot in ("canonical", "alt"):
    for delta in ("-1.5", "0", "1.5"):
        vals, info = background(foot, mp.mpf("1"), mp.mpf(1), mp.mpf(delta))
        lw = mp.mpf(info["l_w_m"])
        DEC.append(dict(footing=foot, delta=float(delta), S=info["S"], k_lw=10, **decompose(vals, 10 / lw, 0)))
res["decomposition_y1_nstar1_klw10"] = DEC
for d_ in DEC:
    P_(f"  decomposition {d_['footing']:9s} S {d_['S']:.3f}: K held {d_['S_held']['K']:+.3e}, +S_Q {d_['S_and_SQ']['K']:+.3e}, "
       f"+S_QQ {d_['S_SQ_SQQ']['K']:+.3e}, full {d_['full']['K']:+.3e}; c0 held {d_['S_held']['c0']:+.3e}, +S_Q {d_['S_and_SQ']['c0']:+.3e}, "
       f"+S_QQ {d_['S_SQ_SQQ']['c0']:+.3e}, full {d_['full']['c0']:+.3e}")
# S = 1 phase: the clock density below which the static law-on clock is gradient-unstable (k = 1e-3 /m, far above
# every background scale), against the law's phantom density at the same radius (point mass on the law)
def phantom_density(foot, y):
    a0v = mp.mpf(A0[foot]); Mb = mp.mpf(10) ** LOGM * mp.mpf(MS)
    r = mp.sqrt(mp.mpf(G) * Mb / (a0v * y))
    nu = lambda yy: mp.mpf(1) / 2 + mp.sqrt(mp.mpf(1) / 4 + 1 / yy)
    yr = lambda rr: mp.mpf(G) * Mb / (rr ** 2 * a0v)
    dnu_dr = mp.diff(lambda rr: nu(yr(rr)), r)
    return Mb / (4 * mp.pi * r ** 2) * dnu_dr
def c0_S1(foot, y, n, direction):
    vals, info = background(foot, mp.mpf(y), n / RHO_MEAN, mp.mpf(0))
    kv = mp.mpf("1e-3")
    an = analyse("S1", vals, kv if direction == "longitudinal" else 0, kv if direction == "tangential" else 0)
    return an["c0"], an
THR = []
for foot in ("canonical", "alt"):
    for yv in ("0.01", "0.1", "1", "10"):
        for direction in ("longitudinal", "tangential"):
            lo, hi = mp.mpf(0), mp.mpf(12)                       # log10(n / mean)
            clo, _ = c0_S1(foot, yv, RHO_MEAN * 10 ** lo, direction); chi, _ = c0_S1(foot, yv, RHO_MEAN * 10 ** hi, direction)
            row = dict(footing=foot, y=float(yv), direction=direction, unstable_at_mean=bool(clo > 0), stable_at_1e12=bool(chi < 0))
            if clo > 0 and chi < 0:
                for _ in range(60):
                    mid = (lo + hi) / 2
                    cm, _ = c0_S1(foot, yv, RHO_MEAN * 10 ** mid, direction)
                    if cm > 0: lo = mid
                    else: hi = mid
                ncrit = RHO_MEAN * 10 ** ((lo + hi) / 2)
                rph = phantom_density(foot, mp.mpf(yv))
                row.update(n_crit_kg_m3=float(ncrit), n_crit_over_mean=float(ncrit / RHO_MEAN),
                           phantom_kg_m3=float(rph), n_crit_over_phantom=float(ncrit / rph))
            THR.append(row)
res["S1_stability_threshold"] = THR
for r_ in THR:
    if "n_crit_over_mean" in r_:
        P_(f"  S = 1 static clock, {r_['footing']:9s} y {r_['y']:>5g} {r_['direction']:12s}: unstable below n_d = {r_['n_crit_kg_m3']:.3e} kg/m^3 "
           f"= {r_['n_crit_over_mean']:.3e} x mean = {r_['n_crit_over_phantom']:.3f} x the law's phantom density")
    else:
        P_(f"  S = 1 static clock, {r_['footing']:9s} y {r_['y']:>5g} {r_['direction']}: no sign change in [1, 1e12] x mean "
           f"(unstable at mean: {r_['unstable_at_mean']})")
# route 1 (hand gradient expansion, reported): G_long = (N/Qbar)[n_d - S_Q W + S p'/Qbar], G_tan = (N/Qbar)[n_d - S_Q W
# + S (p' + A p)/Qbar], with p = |Pbar| = (a0/K) u/(1+u), p' = A'/(K (1+u)^2), W = W(K p), at k = 1e-3 /m (large-k limit)
def G_hand(vals, direction):
    N0v, N1v, N2v = vals[N0], vals[N1], vals[N2]
    Ab = N1v / N0v; Abp = (N2v * N0v - N1v ** 2) / N0v ** 2
    a0g, Kg = vals[a0], vals[K]
    u = Ab / a0g; xx = u / (1 + u)
    pbar = (a0g / Kg) * xx; pprime = Abp / (Kg * (1 + u) ** 2)
    Wb = (a0g ** 2 / Kg) * (-xx - mp.log(1 - xx))
    Qb = vals[Qinf] / N0v; nd = vals[mu] ** 2 * (Qb - 1) / Kg
    Sv, SQ = vals[SG[0]], vals[SG[1]]
    grad = pprime if direction == "longitudinal" else pprime + Ab * pbar
    return (N0v / Qb) * (nd - SQ * Wb + Sv * grad / Qb)
HANDROWS = []
for kind in ("S1", "wall"):
    for foot in ("canonical", "alt"):
        for nfac in (1, 1000, 1000000):
            for yv in ("0.01", "1", "10"):
                vals, info = background(foot, mp.mpf(yv), mp.mpf(nfac), mp.mpf(0))
                if kind == "S1":
                    vals = dict(vals); vals[SG[0]] = mp.mpf(1)
                    for i in range(1, 6): vals[SG[i]] = mp.mpf(0)
                for direction in ("longitudinal", "tangential"):
                    kv = mp.mpf("1e-3")
                    cs = symbol_num(kind, vals, kv if direction == "longitudinal" else 0, kv if direction == "tangential" else 0)
                    Gnum = -mp.re(cs[0]) / kv ** 2
                    Gh = G_hand(vals, direction)
                    HANDROWS.append(dict(kind=kind, footing=foot, n_star_over_mean=nfac, y=float(yv), direction=direction,
                                         G_numeric=float(Gnum), G_hand=float(Gh), rel=float(abs(Gnum - Gh) / abs(Gh))))
res["gradient_coefficient_two_routes"] = HANDROWS
mxrel = max(r_["rel"] for r_ in HANDROWS)
res["gradient_two_routes_max_rel"] = mxrel
P_(f"gradient coefficient, numeric symbol vs hand formula, {len(HANDROWS)} rows (S = 1 phase and wall): max rel {mxrel:.2e}")
n_ghost = sum(r["ghost"] for r in TABLE); n_unst = sum(r["unstable"] for r in TABLE)
ph_bad = [r for r in PH if r["ghost"] or r["unstable"]]
label = "UNHEALTHY" if (n_ghost or n_unst or ph_bad) else "NO SIGN CHANGE ON THE GRID"
res["grid"] = TABLE; res["phase_rows"] = PH
res["counts"] = dict(rows=len(TABLE), ghost=n_ghost, unstable=n_unst, phase_rows=len(PH), phase_bad=len(ph_bad))
res["label_grid"] = label
unst = [r for r in TABLE if r["unstable"]]
if unst:
    worst = max(unst, key=lambda r: r["max_growth_per_m"])
    res["fastest_growth"] = dict(per_s=worst["max_growth_per_m"] * CL,
                                 efold_years=1 / (worst["max_growth_per_m"] * CL) / 3.15576e7, row=worst)
P_(f"wall grid: {len(TABLE)} WKB rows (k l_w >= 10); ghost rows {n_ghost}; unstable rows {n_unst}")
P_(f"phase rows (S = 0, S = 1): {len(PH)}; ghost or unstable {len(ph_bad)}")
for r in TABLE:
    if r["k_lw"] == 10 and r["n_star_over_mean"] == 1 and r["y"] == 1.0:
        P_(f"  {r['footing']:9s} {r['direction']:12s} S {r['S']:.3f}: K {r['K']:+.3e}  c0 {r['c0']:+.3e}  w^2 {r['w2']:+.3e}  "
           f"ghost {r['ghost']} unstable {r['unstable']}  (l_w {r['l_w_m']:.3e} m)")
for r in PH:
    if r["k_lw"] == 10 and r["y"] == 1.0 and r["footing"] == "canonical":
        P_(f"  phase {r['phase']} {r['direction']:12s}: K {r['K']:+.3e}  c0 {r['c0']:+.3e}  w^2 {r['w2']:+.3e}  "
           f"ghost {r['ghost']} unstable {r['unstable']}")
if unst:
    P_(f"fastest growth on the grid: {res['fastest_growth']['per_s']:.3e} /s (e-fold {res['fastest_growth']['efold_years']:.3g} yr)")
P_(f"ITEM 6 grid label: {label}")

res["seconds"] = round(time.time() - t0, 1)
res["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
res["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
with open(os.path.join(HERE, "tpa1_health.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=str)
P_(f"runtime {res['seconds']} s, peak RSS {res['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "tpa1_health.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
