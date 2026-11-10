"""SCS1 route 1: WKB symbol of the full covariant action (A) at S = 1 (and S = 0), coupled to the metric.
Criteria: FROZEN_CRITERIA.md (5d2870617c).  c = 1, K = 4 pi G (geometric units: m, kg/m^3, K = 4 pi G/c^2, a0 -> a0/c^2).

Non-GR Lagrangian sqrt(-g)[mu_K^2 (Q-1)^2/(2K) + S J(|A|)] (gamma_L = 0, P eliminated by the Legendre maximum) on jets of
the clock perturbation pi (first and second order) and of the Newtonian-gauge metric perturbations phi (lapse) and psi
(spatial), quasi-static (no phi_t, psi_t).  GR: (|grad psi|^2 - 2 grad phi . grad psi)/(2K).  The Hessian in the jets gives
coefficient functions C_ab(N, N_x, N_y, N_z); their spatial derivatives follow by the chain rule from the background's
derivative tensors (spherical: N = N(|x|); planar: N = N(x), TPA1's model).  Symbol: sum_ab (-D)^alpha_a [C_ab (i xi)^beta_b]
on exp(i(k.x - w t)); det over (pi, phi, psi) = 0 gives w.
SCS1_MUTATE in {M1, M1b, M2, M3} runs one arm (separate outputs).
"""
import os, sys, json, math, time, itertools, resource
import sympy as sp
import mpmath as mp

ARM = os.environ.get("SCS1_MUTATE", "")
assert ARM in ("", "M1", "M1b", "M2", "M3")
HERE = os.path.dirname(os.path.abspath(__file__))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()
mp.mp.dps = 50

# ------------------------------------------------------------------ symbols
K, a0, mu, Qinf = sp.symbols("K a0 mu_K Q_inf", positive=True)
Nv, Nx_, Ny_, Nz_ = sp.symbols("Nv Nx Ny Nz")
BG = [Nv, Nx_, Ny_, Nz_]
PARAMS = [K, a0, mu, Qinf]
# jets: pi (first, second), phi and psi (value, first; quasi-static)
pt, px, py, pz = sp.symbols("pi_t pi_x pi_y pi_z")
ptt, ptx, pty, ptz, pxx, pxy, pxz, pyy, pyz, pzz = sp.symbols("pi_tt pi_tx pi_ty pi_tz pi_xx pi_xy pi_xz pi_yy pi_yz pi_zz")
f0, fx, fy, fz = sp.symbols("phi phi_x phi_y phi_z")
s0, sx, sy, sz = sp.symbols("psi psi_x psi_y psi_z")
PIJ = [pt, px, py, pz, ptt, ptx, pty, ptz, pxx, pxy, pxz, pyy, pyz, pzz]
PHJ = [f0, fx, fy, fz]
PSJ = [s0, sx, sy, sz]
JETS = PIJ + PHJ + PSJ
FIELD = {**{j: "pi" for j in PIJ}, **{j: "phi" for j in PHJ}, **{j: "psi" for j in PSJ}}
ORD = {pt: (1, 0, 0, 0), px: (0, 1, 0, 0), py: (0, 0, 1, 0), pz: (0, 0, 0, 1), ptt: (2, 0, 0, 0), ptx: (1, 1, 0, 0),
       pty: (1, 0, 1, 0), ptz: (1, 0, 0, 1), pxx: (0, 2, 0, 0), pxy: (0, 1, 1, 0), pxz: (0, 1, 0, 1), pyy: (0, 0, 2, 0),
       pyz: (0, 0, 1, 1), pzz: (0, 0, 0, 2), f0: (0, 0, 0, 0), fx: (0, 1, 0, 0), fy: (0, 0, 1, 0), fz: (0, 0, 0, 1),
       s0: (0, 0, 0, 0), sx: (0, 1, 0, 0), sy: (0, 0, 1, 0), sz: (0, 0, 0, 1)}
# total derivative of a first-order pi jet along coordinate c (0 = t)
DPI = {pt: [ptt, ptx, pty, ptz], px: [ptx, pxx, pxy, pxz], py: [pty, pxy, pyy, pyz], pz: [ptz, pxz, pyz, pzz]}
DPH = [0, fx, fy, fz]; DPS = [0, sx, sy, sz]
BGD = [0, Nx_, Ny_, Nz_]       # explicit derivative of N along t, x, y, z

def lagrangians():
    """returns (L_dust, L_law) with every jet present (not scaled)."""
    Ntot = Nv * (1 + f0)
    gsp = 1 - 2 * s0
    Q2 = (Qinf + pt) ** 2 / Ntot ** 2 - (px ** 2 + py ** 2 + pz ** 2) / gsp
    # total derivatives of Q2: jets of pi, phi, psi and the explicit x-dependence of N
    dQ2 = []
    for c in range(4):
        d = 0
        for j in (pt, px, py, pz):
            d += sp.diff(Q2, j) * DPI[j][c]
        d += sp.diff(Q2, f0) * DPH[c] + sp.diff(Q2, s0) * DPS[c] + sp.diff(Q2, Nv) * BGD[c]
        dQ2.append(d)
    Q = sp.sqrt(Q2)
    dl = [dQ2[c] / (2 * Q2) for c in range(4)]
    ginv = [-1 / Ntot ** 2, 1 / gsp, 1 / gsp, 1 / gsp]
    tau_d = [Qinf + pt, px, py, pz]
    nlow = [-tau_d[m] / Q for m in range(4)]
    nup = [ginv[m] * nlow[m] for m in range(4)]
    ndl = sum(nup[m] * dl[m] for m in range(4))
    A = [-(dl[m] + nlow[m] * ndl) for m in range(4)]
    Amod = sp.sqrt(sum(ginv[m] * A[m] ** 2 for m in range(4)))
    J = (a0 ** 2 / K) * (Amod / a0 - sp.log(1 + Amod / a0))
    sqrtg = Ntot * gsp ** sp.Rational(3, 2)
    return sqrtg * mu ** 2 * (Q - 1) ** 2 / (2 * K), sqrtg * J

def hessian(L):
    zero = {j: 0 for j in JETS}
    first = {ja: sp.diff(L, ja) for ja in JETS}
    C = {}
    for i_, ja in enumerate(JETS):
        for jb in JETS[i_:]:
            c = sp.diff(first[ja], jb).subs(zero)
            if c != 0:
                C[(ja, jb)] = sp.lambdify(BG + PARAMS, c, "mpmath")
    return C

tb = time.time()
Ld, Ll = lagrangians()
CD = hessian(Ld); CL = hessian(Ll)
P_(f"Hessians: dust {len(CD)} entries, law {len(CL)} entries (upper triangle); built in {time.time()-tb:.1f}s")
PTT2 = any(k_ == (ptt, ptt) for k_ in list(CD) + list(CL))
P_(f"pi_tt^2 term present: {PTT2} (absent = no extra mode)")

# ------------------------------------------------------------------ background derivative tensors of N at (r0, 0, 0)
xs, ys, zs = sp.symbols("xs ys zs")
F1, F2, F3, F4 = sp.symbols("F1:5")
r0s = sp.Symbol("r0", positive=True)
def Ntensor_fns(geometry):
    s_ = (sp.sqrt((r0s + xs) ** 2 + ys ** 2 + zs ** 2) - r0s) if geometry == "spherical" else xs
    Nexpr = sp.exp(F1 * s_ + F2 * s_ ** 2 / 2 + F3 * s_ ** 3 / 6 + F4 * s_ ** 4 / 24)
    X3 = [xs, ys, zs]
    out = {}
    for order in range(4):
        for idx in itertools.combinations_with_replacement(range(3), order):
            e = Nexpr
            for i in idx: e = sp.diff(e, X3[i])
            out[idx] = sp.lambdify([r0s, F1, F2, F3, F4], e.subs({xs: 0, ys: 0, zs: 0}), "mpmath")
    return out
NT = {"spherical": Ntensor_fns("spherical"), "planar": Ntensor_fns("planar")}
def Nd(T, idx): return T[tuple(sorted(idx))]

# ------------------------------------------------------------------ physical numbers
G, CL_, MS, PC = 6.6743e-11, 2.99792458e8, 1.98847e30, 3.0856775814913673e16
MPC, KPC = 1e6 * PC, 1e3 * PC
A0 = {"canonical": "9.3603e-11", "alt": "1.1312e-10"}
MUK_STAR = {"canonical": "8.890e6", "alt": "8.889e6"}
Kg = 4 * mp.pi * mp.mpf(G) / mp.mpf(CL_) ** 2
I0g = mp.mpf("4.037e-8") / mp.mpf(MPC) ** 2
RHO_MEAN = I0g / (2 * Kg)

def law_point(Mb, a0v, r):
    """geometric g, g', g'', g''' of the law for a point mass, and p, p', D.P (spherical and planar)."""
    def g(rr):
        gn = mp.mpf(G) * Mb / rr ** 2
        return gn / 2 + mp.sqrt(gn * gn / 4 + gn * a0v)
    c2 = mp.mpf(CL_) ** 2
    gs = [mp.diff(g, r, n) / c2 for n in range(4)]
    a0g = a0v / c2
    u = gs[0] / a0g
    p = (a0g / Kg) * u / (1 + u)
    pp = (a0g / Kg) * (gs[1] / a0g) / (1 + u) ** 2
    return gs, u, p, pp

def background(foot, Mb, r, mu_v, nd, geometry):
    """code units: length unit = r, K = 1 (densities as K rho r^2).  Returns N's derivative tensors at the point,
    the parameters, and physical info."""
    a0v = mp.mpf(A0[foot])
    gs, u, p, pp = law_point(Mb, a0v, r)
    F = [gs[n] * r ** (n + 1) for n in range(4)]     # (d/dr)^n Phi' in code units
    T = NT[geometry]
    Ntens = {idx: fn(mp.mpf(1), *F) for idx, fn in T.items()}
    Qbar = 1 + Kg * nd / mu_v ** 2 if mu_v > 0 else mp.mpf(1)
    divP = pp + 2 * p / r if geometry == "spherical" else pp
    info = dict(u=float(u), p=float(p), dp_dr=float(pp), divP=float(divP), Qbar_minus_1=float(Qbar - 1),
                g=float(gs[0]), vc_over_c=float(mp.sqrt(gs[0] * r)), r_m=float(r))
    params = dict(K=mp.mpf(1), a0=a0v / mp.mpf(CL_) ** 2 * r, mu=mu_v * r, Qinf=Qbar,
                  nd_code=Kg * nd * r ** 2, divP_code=Kg * divP * r ** 2, r=r)
    return Ntens, params, info

def coeff_derivs(C, Ntens, params):
    """C_ab and its spatial derivatives up to second order at the point, by the chain rule through (N, N_x, N_y, N_z)."""
    bgv = [Ntens[()], Ntens[(0,)], Ntens[(1,)], Ntens[(2,)]]
    pv = [params["K"], params["a0"], params["mu"], params["Qinf"]]
    # derivative of each background variable along x_j, and second derivatives
    dV = [[Ntens[(j,)] for j in range(3)]] + [[Nd(Ntens, (c, j)) for j in range(3)] for c in range(3)]
    ddV = [[[Nd(Ntens, (j, k_)) for k_ in range(3)] for j in range(3)]] + \
          [[[Nd(Ntens, (c, j, k_)) for k_ in range(3)] for j in range(3)] for c in range(3)]
    out = {}
    sc = [mp.mpf(1)] + [max(abs(bgv[1]) + abs(bgv[2]) + abs(bgv[3]), params["a0"])] * 3   # O(1) variables for mp.diff
    v0 = [bgv[a] / sc[a] for a in range(4)]
    for key, fn in C.items():
        fs = lambda *v: fn(*[v[a] * sc[a] for a in range(4)], *pv)
        val = fs(*v0)
        g1 = [mp.diff(fs, v0, tuple(1 if i == a else 0 for i in range(4))) / sc[a] for a in range(4)]
        g2 = {}
        for a in range(4):
            for b in range(a, 4):
                o = [0] * 4; o[a] += 1; o[b] += 1
                g2[(a, b)] = g2[(b, a)] = mp.diff(fs, v0, tuple(o)) / (sc[a] * sc[b])
        d1 = [sum(g1[a] * dV[a][j] for a in range(4)) for j in range(3)]
        d2 = [[sum(g2[(a, b)] * dV[a][j] * dV[b][k_] for a in range(4) for b in range(4))
               + sum(g1[a] * ddV[a][j][k_] for a in range(4)) for k_ in range(3)] for j in range(3)]
        out[key] = (val, d1, d2)
    return out

FIELDS = ["pi", "phi", "psi"]
def symbol(Cd, kvec, mutate=None, decoupled=False, dust_only_mix=None):
    """3x3 (or 1x1) symbol, entries as dicts {power of omega: complex coefficient}."""
    I = mp.mpc(0, 1)
    flds = ["pi"] if decoupled else FIELDS
    M = {(f, g): {} for f in flds for g in flds}
    def add(f, g, pw, v):
        M[(f, g)][pw] = M[(f, g)].get(pw, mp.mpc(0)) + v
    for (ja, jb), (val, d1, d2) in Cd.items():
        for (a_, b_) in ((ja, jb), (jb, ja)) if ja != jb else ((ja, jb),):
            fa, fb = FIELD[a_], FIELD[b_]
            if fa not in flds or fb not in flds: continue
            sgn = 1
            if mutate in ("M1", "M2") and ({fa, fb} == {"pi", "phi"} or {fa, fb} == {"pi", "psi"}):
                if mutate == "M2": continue
                sgn = -1
            oa, ob = ORD[a_], ORD[b_]
            # spatial part: (-1)^{|a_s|} prod_j (d_j + i k_j)^{a_j} [C] * prod_j (i k_j)^{b_j}
            asp = oa[1:]
            tot = mp.mpc(0)
            for nu in itertools.product(*[range(n + 1) for n in asp]):
                order = sum(nu)
                if order == 0: dc = val
                elif order == 1: dc = d1[nu.index(1)]
                else:
                    js = [j for j in range(3) for _ in range(nu[j])]
                    dc = d2[js[0]][js[1]]
                term = dc
                for j in range(3):
                    term *= mp.binomial(asp[j], nu[j]) * (I * kvec[j]) ** (asp[j] - nu[j])
                tot += term
            tot *= (-1) ** sum(asp)
            for j in range(3):
                tot *= (I * kvec[j]) ** ob[1 + j]
            tcoef = I ** oa[0] * (-I) ** ob[0]
            add(fa, fb, oa[0] + ob[0], sgn * tot * tcoef)
    return M, flds

def hermitian(M, flds):
    """Hermitian part for real omega: (M + M^dagger)/2, coefficient by coefficient (amendment A1)."""
    H = {}
    for f in flds:
        for g in flds:
            keys = set(M[(f, g)]) | set(M[(g, f)])
            H[(f, g)] = {p_: (M[(f, g)].get(p_, 0) + mp.conj(M[(g, f)].get(p_, 0))) / 2 for p_ in keys}
    return H

def padd(p, q):
    r = dict(p)
    for k_, v in q.items(): r[k_] = r.get(k_, 0) + v
    return r
def pmul(p, q):
    r = {}
    for a_, va in p.items():
        for b_, vb in q.items():
            r[a_ + b_] = r.get(a_ + b_, 0) + va * vb
    return r
def pneg(p): return {k_: -v for k_, v in p.items()}
def det_poly(M, flds):
    n = len(flds)
    if n == 1: return M[(flds[0], flds[0])]
    tot = {}
    for perm in itertools.permutations(range(n)):
        sgn = 1
        for i in range(n):
            for j in range(i + 1, n):
                if perm[i] > perm[j]: sgn = -sgn
        term = {0: mp.mpc(1)}
        for i in range(n):
            term = pmul(term, M[(flds[i], flds[perm[i]])])
        tot = padd(tot, term if sgn > 0 else pneg(term))
    return tot

def roots_of(poly):
    deg = max((k_ for k_, v in poly.items() if abs(v) > 0), default=0)
    coeffs = [poly.get(d, 0) for d in range(deg, -1, -1)]
    scale = max(abs(c) for c in coeffs)
    # drop leading coefficients that are pure rounding relative to the rest
    while len(coeffs) > 1 and abs(coeffs[0]) < mp.mpf(10) ** (-30) * scale:
        coeffs = coeffs[1:]
    if len(coeffs) == 1: return []
    return mp.polyroots(coeffs, maxsteps=200, extraprec=200)

def growth(rts):
    return max((abs(mp.im(r_)) for r_ in rts), default=mp.mpf(0))

def hand_omega2(params, info, kvec, S):
    """Newtonian hand closed form (code units, K = 1): w^2 = G [(1 - K m) k^2 - mu^2 Qb^2] / (mu^2 Qb^2 + K m k^2),
    G = Qb n_d + S D.P."""
    k2 = sum(kk ** 2 for kk in kvec); kh = [kk / mp.sqrt(k2) for kk in kvec]
    u = mp.mpf(info["u"])
    Km = S * (kh[0] ** 2 / (1 + u) ** 2 + (kh[1] ** 2 + kh[2] ** 2) / (1 + u))
    Qb = params["Qinf"]; m2 = params["mu"] ** 2 * Qb ** 2
    Gc = Qb * params["nd_code"] + S * params["divP_code"]
    if m2 + Km * k2 == 0: return mp.nan
    return Gc * ((1 - Km) * k2 - m2) / (m2 + Km * k2)

def merge(Ca, Cb, flip_pi_phi=False):
    out = dict(Ca)
    for k_, v in Cb.items():
        if flip_pi_phi and {FIELD[k_[0]], FIELD[k_[1]]} == {"pi", "phi"}:
            v = (-v[0], [-x for x in v[1]], [[-x for x in row] for row in v[2]])
        if k_ in out:
            a_ = out[k_]
            out[k_] = (a_[0] + v[0], [a_[1][j] + v[1][j] for j in range(3)],
                       [[a_[2][j][l] + v[2][j][l] for l in range(3)] for j in range(3)])
        else:
            out[k_] = v
    return out

def add_GR(Cs):
    z3 = [mp.mpf(0)] * 3; z33 = [[mp.mpf(0)] * 3 for _ in range(3)]
    for jp, jf in ((sx, fx), (sy, fy), (sz, fz)):
        Cs[(jp, jp)] = (Cs.get((jp, jp), (0, z3, z33))[0] + 1, z3, z33)          # K = 1 in code units
        Cs[(jf, jp)] = (Cs.get((jf, jp), (0, z3, z33))[0] - 1, z3, z33)
    return Cs

# ------------------------------------------------------------------ grids
MASSES = [mp.mpf(10) ** mp.mpf(s) * mp.mpf(MS) for s in ("9.4", "10.45", "10.7", "10.9")]
LOGM = ["9.4", "10.45", "10.7", "10.9"]
RADII_KPC = [10, 30, 100, 300]
KR = [10, 100, 1000, 10000, 100000]
DIRS = {"radial": (1, 0, 0), "tangential": (0, 1, 0), "45deg": (1 / math.sqrt(2), 1 / math.sqrt(2), 0)}
def points(foot):
    pts = [(lm, Mb, mp.mpf(rk) * mp.mpf(KPC), f"{rk} kpc") for lm, Mb in zip(LOGM, MASSES) for rk in RADII_KPC]
    Mb = mp.mpf(10) ** mp.mpf("10.45") * mp.mpf(MS); a0v = mp.mpf(A0[foot])
    for yv in ("0.01", "0.1", "1", "10"):
        pts.append(("10.45", Mb, mp.sqrt(mp.mpf(G) * Mb / (a0v * mp.mpf(yv))), f"y={yv}"))
    return pts

def run_config(name, S, mu_of, nd_of, geometry, coupled, mutate=None, feet=("canonical", "alt"), dirs=None, krs=None):
    rows = []
    for foot in feet:
        for (lm, Mb, r, tag) in points(foot):
            mu_v = mu_of(foot)
            nd = nd_of(foot, Mb, r)
            Ntens, params, info = background(foot, Mb, r, mu_v, nd, geometry)
            Cs = coeff_derivs(CD, Ntens, params)
            if S:
                Cs = merge(Cs, coeff_derivs(CL, Ntens, params), flip_pi_phi=(mutate == "M1b"))
            Cs = add_GR(Cs)
            rho_loc = params["Qinf"] * params["nd_code"] + S * params["divP_code"]     # K rho r^2
            ff_rate = mp.sqrt(abs(rho_loc)) / r                                       # 1/m
            for dname, dvec in (DIRS.items() if dirs is None else [(d, DIRS[d]) for d in dirs]):
                gam_k = []
                for kr in (KR if krs is None else krs):
                    kmag = mp.mpf(kr)                                     # code units: k r
                    kvec = [kmag * mp.mpf(dvec[j]) for j in range(3)]
                    M, flds = symbol(Cs, kvec, mutate=(mutate if mutate in ("M1", "M2") else None), decoupled=not coupled)
                    raw_rts = roots_of(det_poly(M, flds))
                    Gm_raw = growth(raw_rts) / r                          # full symbol, diagnostic only (A1)
                    dp = det_poly(hermitian(M, flds), flds)
                    rts = roots_of(dp)
                    Gm = growth(rts) / r                                  # 1/m, Hermitian part (A1)
                    w2 = [complex(r_ ** 2 / r ** 2) for r_ in rts]        # 1/m^2
                    wh = hand_omega2(params, info, kvec, S) / r ** 2 if coupled else None
                    rel_hand = None
                    if wh is not None and rts:
                        best = min(rts, key=lambda r_: abs(r_ ** 2 / r ** 2 - wh))
                        rel_hand = float(abs(best ** 2 / r ** 2 - wh) / abs(wh)) if wh != 0 else None
                    gam_k.append(float(Gm))
                    rows.append(dict(config=name, footing=foot, logM=lm, point=tag, r_kpc=float(r / KPC), direction=dname,
                                     kr=kr, growth_per_m=float(Gm), growth_full_symbol_per_m=float(Gm_raw), omega2=w2, hand_omega2=(float(wh) if wh is not None else None),
                                     rel_hand=rel_hand, freefall_rate_per_m=float(ff_rate), n_d=float(nd), **info))
    return rows

def summarize(rows):
    grow = [r_ for r_ in rows if r_["growth_per_m"] > 1e-6 * max(r_["freefall_rate_per_m"], 1e-300)]
    out = dict(n_rows=len(rows), n_growing=len(grow))
    # boundedness: ratio of growth at kr 1e5 to 1e3 per (footing, point, direction)
    ratios = []
    for r_ in rows:
        if r_["kr"] == 100000:
            base = [q for q in rows if q["footing"] == r_["footing"] and q["point"] == r_["point"] and q["logM"] == r_["logM"]
                    and q["direction"] == r_["direction"] and q["kr"] == 1000]
            if base and base[0]["growth_per_m"] > 0:
                ratios.append(r_["growth_per_m"] / base[0]["growth_per_m"])
    out["max_ratio_1e5_over_1e3"] = max(ratios) if ratios else None
    if grow:
        out["fastest_efold_yr"] = 1 / (max(r_["growth_per_m"] for r_ in grow) * CL_) / 3.15576e7
        out["slowest_efold_yr"] = 1 / (min(r_["growth_per_m"] for r_ in grow) * CL_) / 3.15576e7
        out["max_growth_over_freefall"] = max(r_["growth_per_m"] / r_["freefall_rate_per_m"] for r_ in grow
                                              if r_["freefall_rate_per_m"] > 0) if any(r_["freefall_rate_per_m"] > 0 for r_ in grow) else None
    hand = [r_["rel_hand"] for r_ in rows if r_["rel_hand"] is not None and r_["kr"] >= 1000]
    out["max_rel_hand_kr_ge_1e3"] = max(hand) if hand else None
    return out

def label_of(s):
    if s["n_growing"] == 0: return "STABLE"
    if s["max_ratio_1e5_over_1e3"] is not None and s["max_ratio_1e5_over_1e3"] >= 10: return "GRADIENT-UNSTABLE"
    if s["max_ratio_1e5_over_1e3"] is not None and s["max_ratio_1e5_over_1e3"] <= 1.1:
        if s.get("max_growth_over_freefall") is not None and s["max_growth_over_freefall"] <= 10: return "JEANS-ONLY"
    return "NO VERDICT"

RES = {"lane": "SCS1", "route": 1, "criteria": "5d2870617c", "mutate_arm": ARM or None, "configs": {}, "known_answers": {}}
zero_mu = lambda foot: mp.mpf(0)
mu01 = lambda foot: mp.mpf("0.1") / mp.mpf(MPC)
mustar = lambda foot: mp.mpf(MUK_STAR[foot]) / mp.mpf(MPC)
nd0 = lambda foot, Mb, r: mp.mpf(0)
def nd_fac(fac): return lambda foot, Mb, r: fac * RHO_MEAN
def nd_crit(foot, Mb, r):
    return -law_point(Mb, mp.mpf(A0[foot]), r)[3]          # TPA1's planar threshold -dp/dr

if ARM == "":
    # ---------------- KA1: TPA1 reproduction (decoupled, planar, mu_K*), TPA1's own background construction
    TP = json.load(open(os.path.join(HERE, "..", "TPA1_two_phase_action", "tpa1_health.json")))
    s1rows = [r_ for r_ in TP["phase_rows"] if r_["phase"] == "S1"]
    worst = 0.0; efolds = []; cache = {}
    Mb_t = mp.mpf(10) ** mp.mpf("10.45") * mp.mpf(MS)
    for r_ in s1rows:
        foot = r_["footing"]; a0v = mp.mpf(A0[foot])
        key = (foot, r_["y"], r_["n_star_over_mean"])
        rr = mp.sqrt(mp.mpf(G) * Mb_t / (a0v * mp.mpf(str(r_["y"]))))
        if key not in cache:
            nd = mp.mpf(r_["n_star_over_mean"]) * RHO_MEAN
            Ntens, params, info = background(foot, Mb_t, rr, mustar(foot), nd, "planar")
            cache[key] = merge(coeff_derivs(CD, Ntens, params), coeff_derivs(CL, Ntens, params))
        Cs = cache[key]
        kmag = mp.mpf(r_["k_lw"]) / mp.mpf(r_["l_w_m"]) * rr          # code units
        kvec = [kmag, 0, 0] if r_["direction"] == "longitudinal" else [0, kmag, 0]
        M, flds = symbol(Cs, kvec, decoupled=True)
        poly = M[("pi", "pi")]
        # TPA1's K and c0 are in SI-geometric units of the 2+1 symbol; compare the dimensionless omega^2 and ratios
        Kc = mp.re(poly.get(2, 0)); c0 = mp.re(poly.get(0, 0))
        w2 = -c0 / Kc / rr ** 2
        relw = abs(w2 / r_["w2"] - 1)
        relK = abs((Kc / c0) / (mp.mpf(r_["K"]) / mp.mpf(r_["c0"]) / rr ** 2) - 1)
        worst = max(worst, float(relw), float(relK))
        if w2 < 0: efolds.append(float(1 / (mp.sqrt(-w2) * CL_) / 3.15576e7))
    ka1 = dict(rows=len(s1rows), max_rel=worst, efold_min_yr=min(efolds), efold_max_yr=max(efolds),
               TPA1_range="5.03e6 to 6.25e8 yr", note="omega^2 and K/c0 compared (TPA1's K, c0 carry its 2+1 normalisation)")
    ka1["pass_"] = bool(worst <= 1e-6 and f"{min(efolds):.3g}" == "5.03e+06" and f"{max(efolds):.3g}" == "6.25e+08")
    RES["known_answers"]["KA1_TPA1_decoupled_planar"] = ka1
    P_(f"KA1 TPA1 reproduction (decoupled, planar, mu_K*): {len(s1rows)} rows, max rel {worst:.2e}; e-fold "
       f"{min(efolds):.3g} to {max(efolds):.3g} yr -> {'PASS' if ka1['pass_'] else 'FAIL'}")

    # ---------------- KA2: dust Jeans (S = 0, flat background, mu_K*); code length unit 1/mu_K
    ka2rows = []; ok2 = True
    for foot in ("canonical", "alt"):
        for fac in (1, 1000):
            nd = fac * RHO_MEAN; mu_v = mustar(foot)
            Ntens = {idx: (mp.mpf(1) if idx == () else mp.mpf(0)) for idx in NT["planar"]}
            Qb = 1 + Kg * nd / mu_v ** 2
            params = dict(K=mp.mpf(1), a0=mp.mpf(A0[foot]) / mp.mpf(CL_) ** 2 / mu_v, mu=mp.mpf(1), Qinf=Qb)
            Cs = add_GR(coeff_derivs(CD, Ntens, params))
            ncode = Kg * nd / mu_v ** 2
            for kf in ("0.001", "0.1", "1", "10", "100"):
                kmag = mp.mpf(kf)
                M, flds = symbol(Cs, [kmag, 0, 0])
                rts = roots_of(det_poly(M, flds))
                w2 = min((mp.re(r_ ** 2) for r_ in rts), key=lambda z: z) if rts else mp.nan
                exact = ncode * Qb * (kmag ** 2 / Qb ** 2 - 1)           # (K n/mu^2)(k^2 - mu^2), Qb-exact, Qb -> 1 here
                # error measured against the natural scale K n (1 + k^2/mu^2): the target vanishes at k = mu (run-1 bug:
                # dividing by it gave rel 3.0 on two values that are both zero to 1e-21 of that scale)
                rel = float(abs(w2 - exact) / (ncode * Qb * (1 + kmag ** 2)))
                gr = float(growth(rts) / mp.sqrt(ncode))
                row = dict(footing=foot, n_over_mean=fac, k_over_mu=kf, omega2_code=float(w2), exact_code=float(exact),
                           rel=rel, growth_over_sqrt_4piGn=gr)
                ka2rows.append(row)
                ok2 &= rel <= 1e-6
                if kf == "0.001": ok2 &= abs(gr - 1) <= 0.01
                if kf in ("10", "100"): ok2 &= gr == 0
    RES["known_answers"]["KA2_dust_jeans"] = dict(rows=ka2rows, pass_=bool(ok2))
    g001 = [r_["growth_over_sqrt_4piGn"] for r_ in ka2rows if r_["k_over_mu"] == "0.001"]
    P_(f"KA2 dust Jeans (S = 0, flat, mu_K*): max rel {max(r_['rel'] for r_ in ka2rows):.2e}; growth at k = mu/1000 over "
       f"sqrt(4 pi G n): {min(g001):.6f} to {max(g001):.6f} -> {'PASS' if ok2 else 'FAIL'}")

    # ---------------- KA3: TPA1's mixing claim on the constraint surface
    ka3rows = []
    for foot in ("canonical", "alt"):
        for (mu_name, mu_f, ndv) in (("mu0", zero_mu, mp.mpf(0)), ("mustar", mustar, RHO_MEAN)):
            Mb = mp.mpf(10) ** mp.mpf("10.45") * mp.mpf(MS); r = mp.mpf(30) * mp.mpf(KPC)
            Ntens, params, info = background(foot, Mb, r, mu_f(foot), ndv, "spherical")
            Cs = add_GR(merge(coeff_derivs(CD, Ntens, params), coeff_derivs(CL, Ntens, params)))
            for kr in (10 ** 6, 10 ** 8):
                for dname in ("radial", "tangential"):
                    kmag = mp.mpf(kr); kvec = [kmag * mp.mpf(c) for c in DIRS[dname]]
                    Mfull, flds = symbol(Cs, kvec); Mfull = hermitian(Mfull, flds)
                    Mdec, _ = symbol(Cs, kvec, decoupled=True); Mdec = hermitian(Mdec, ["pi"])
                    B = mp.matrix(2, 2)
                    for i, f in enumerate(("phi", "psi")):
                        for j, g in enumerate(("phi", "psi")):
                            B[i, j] = Mfull[(f, g)].get(0, 0)
                    Binv = B ** -1
                    eff = dict(Mfull[("pi", "pi")])
                    for i, f in enumerate(("phi", "psi")):
                        for j, g in enumerate(("phi", "psi")):
                            eff = padd(eff, pneg(pmul(pmul(Mfull[("pi", f)], {0: Binv[i, j]}), Mfull[(g, "pi")])))
                    kin_c, kin_d = mp.re(eff.get(2, 0)), mp.re(Mdec[("pi", "pi")].get(2, 0))
                    grd_c, grd_d = mp.re(eff.get(0, 0)), mp.re(Mdec[("pi", "pi")].get(0, 0))
                    kh = [kk / kmag for kk in kvec]; u = mp.mpf(info["u"])
                    Km = kh[0] ** 2 / (1 + u) ** 2 + (kh[1] ** 2 + kh[2] ** 2) / (1 + u)
                    Qb = params["Qinf"]; m2 = params["mu"] ** 2 * Qb ** 2
                    claim = 1 / (1 - Km)
                    # full factor: decoupled kinetic (mu^2 Qb^2 + K m k^2)/K over coupled -> 1/(1 - K m - mu^2 Qb^2 / k^2)
                    full = 1 / (1 - Km - m2 / kmag ** 2)
                    ka3rows.append(dict(footing=foot, mu=mu_name, kr=kr, direction=dname,
                                        kinetic_ratio=float(kin_c / kin_d), claim_1_over_1mKm=float(claim),
                                        rel_to_claim=float(abs(kin_c / kin_d / claim - 1)), full_factor=float(full),
                                        rel_to_full=float(abs(kin_c / kin_d / full - 1)),
                                        gradient_ratio=float(grd_c / grd_d) if grd_d != 0 else None))
    mu0rows = [r_ for r_ in ka3rows if r_["mu"] == "mu0"]; msrows = [r_ for r_ in ka3rows if r_["mu"] == "mustar"]
    claim_mu0 = max(r_["rel_to_claim"] for r_ in mu0rows)
    grad_mu0 = max(abs(r_["gradient_ratio"] - 1) for r_ in mu0rows if r_["gradient_ratio"] is not None)
    claim_ms = max(r_["rel_to_claim"] for r_ in msrows); full_ms = max(r_["rel_to_full"] for r_ in msrows)
    grad_ms = max(abs(r_["gradient_ratio"] - 1) for r_ in msrows if r_["gradient_ratio"] is not None)
    RES["known_answers"]["KA3_mixing_claim"] = dict(
        rows=ka3rows, claim_holds_mu0=bool(claim_mu0 <= 1e-6 and grad_mu0 <= 1e-6), max_rel_claim_mu0=claim_mu0,
        max_grad_change_mu0=grad_mu0, claim_holds_mustar=bool(claim_ms <= 1e-6 and grad_ms <= 1e-6),
        max_rel_claim_mustar=claim_ms, max_rel_full_factor_mustar=full_ms, max_grad_change_mustar=grad_ms,
        pass_=bool(claim_mu0 <= 1e-6 and grad_mu0 <= 1e-6 and full_ms <= 1e-6),
        note="tested at kr 1e6 and 1e8, where the O(1/kr) coefficient-gradient terms are below the frozen 1e-6 line")
    P_(f"KA3 mixing claim: mu_K = 0: kinetic ratio vs 1/(1 - Km) rel {claim_mu0:.2e}, gradient change {grad_mu0:.2e}; "
       f"mu_K*: vs 1/(1 - Km) rel {claim_ms:.2e}, vs 1/(1 - Km - mu^2/k^2) rel {full_ms:.2e}, gradient change {grad_ms:.2e} "
       f"-> {'PASS' if RES['known_answers']['KA3_mixing_claim']['pass_'] else 'FAIL'}")

    # ---------------- KA4: law off (S = 0), no dust (n_d = 0), point mass, mu_K = 0.1/Mpc so the clock is not trivial
    rows4 = run_config("KA4_law_off", 0, mu01, nd0, "spherical", True, dirs=["radial", "tangential"], krs=[10, 1000, 100000])
    g4 = max(r_["growth_per_m"] for r_ in rows4)
    RES["known_answers"]["KA4_law_off"] = dict(rows=len(rows4), max_growth=g4, pass_=bool(g4 == 0))
    P_(f"KA4 law off (S = 0, n_d = 0, mu_K 0.1/Mpc) point mass: {len(rows4)} rows, max growth {g4:.3e} -> "
       f"{'PASS' if g4 == 0 else 'FAIL'}")

    # ---------------- graded: primary and brackets
    CONFIGS = [("primary_mu0", 1, zero_mu, nd0, "spherical")]
    for mname, mf in (("mu0.1", mu01), ("mustar", mustar)):
        for nname, nf in (("nd0", nd0), ("nd1", nd_fac(1)), ("nd1e3", nd_fac(1000)), ("ndcrit", nd_crit)):
            CONFIGS.append((f"bracket_{mname}_{nname}", 1, mf, nf, "spherical"))
    for (name, S, mf, nf, geo) in CONFIGS:
        tc = time.time()
        rows = run_config(name, S, mf, nf, geo, True)
        s = summarize(rows)
        RES["configs"][name] = dict(summary=s, label_route1=label_of(s), rows=rows)
        P_(f"[{name}] {s['n_rows']} rows; growing {s['n_growing']}; ratio 1e5/1e3 {s['max_ratio_1e5_over_1e3']}; "
           f"hand rel (kr >= 1e3) {s['max_rel_hand_kr_ge_1e3']}; label (route 1) {label_of(s)}; {time.time()-tc:.0f}s")
        for foot in ("canonical", "alt"):
            sf = summarize([r_ for r_ in rows if r_["footing"] == foot])
            RES["configs"][name][f"label_route1_{foot}"] = label_of(sf)
            RES["configs"][name][f"summary_{foot}"] = sf
else:
    # ---------------- MUTATE arms
    if ARM in ("M1", "M2"):
        base = run_config("primary_mu0", 1, zero_mu, nd0, "spherical", True, dirs=["radial", "tangential"], krs=[1000, 100000])
        mut = run_config("primary_mu0", 1, zero_mu, nd0, "spherical", True, mutate=ARM, dirs=["radial", "tangential"], krs=[1000, 100000])
        dec = run_config("primary_mu0", 1, zero_mu, nd0, "spherical", False, dirs=["radial", "tangential"], krs=[1000, 100000])
        bm = run_config("bracket_mustar_nd1", 1, mustar, nd_fac(1), "spherical", True, dirs=["radial"], krs=[10, 1000])
        mm = run_config("bracket_mustar_nd1", 1, mustar, nd_fac(1), "spherical", True, mutate=ARM, dirs=["radial"], krs=[10, 1000])
        def w2max(r_): return max((w.real for w in r_["omega2"]), default=0.0)
        d_mut = max(abs(w2max(a_) / w2max(b_) - 1) for a_, b_ in zip(mut, base) if w2max(b_) != 0)
        d_mut_ms = max(abs(w2max(a_) / w2max(b_) - 1) for a_, b_ in zip(mm, bm) if w2max(b_) != 0)
        d_dec = max(abs(w2max(a_) / w2max(b_) - 1) for a_, b_ in zip(mut, dec) if w2max(b_) != 0)
        RES["mutate"] = dict(max_rel_change_primary=d_mut, max_rel_change_mustar=d_mut_ms, max_rel_vs_decoupled=d_dec)
        if ARM == "M1":
            RES["mutate"]["bites"] = bool(max(d_mut, d_mut_ms) >= 1e-3)
            RES["mutate"]["expected"] = "no bite: (phi, psi) -> (-phi, -psi) is a field redefinition"
        else:
            RES["mutate"]["returns_decoupled"] = bool(d_dec <= 1e-12)
            RES["mutate"]["bites"] = bool(d_dec <= 1e-12)
        P_(f"MUTATE {ARM}: change vs coupled primary {d_mut:.2e}, vs coupled mu_K* {d_mut_ms:.2e}, vs decoupled {d_dec:.2e} "
           f"-> {'BITES' if RES['mutate']['bites'] else 'DOES NOT BITE'}")
    elif ARM == "M1b":
        bm = run_config("bracket_mustar_nd1", 1, mustar, nd_fac(1), "spherical", True, dirs=["radial"], krs=[10, 1000])
        mm = run_config("bracket_mustar_nd1", 1, mustar, nd_fac(1), "spherical", True, mutate="M1b", dirs=["radial"], krs=[10, 1000])
        def w2max(r_): return max((w.real for w in r_["omega2"]), default=0.0)
        d_ms = max(abs(w2max(a_) / w2max(b_) - 1) for a_, b_ in zip(mm, bm) if w2max(b_) != 0)
        RES["mutate"] = dict(max_rel_change_mustar=d_ms, bites=bool(d_ms >= 1e-3))
        P_(f"MUTATE M1b (law-only mixing flipped) at mu_K*: max rel change of omega^2 {d_ms:.2e} -> "
           f"{'BITES' if d_ms >= 1e-3 else 'DOES NOT BITE'}")
    elif ARM == "M3":
        rows = run_config("M3_planar_primary", 1, zero_mu, nd0, "planar", True)
        s = summarize(rows)
        RES["mutate"] = dict(summary=s, label_route1=label_of(s), rows=rows)
        P_(f"MUTATE M3 (planar background, primary): {s['n_rows']} rows, growing {s['n_growing']}, ratio "
           f"{s['max_ratio_1e5_over_1e3']}, label {label_of(s)}")

RES["seconds"] = round(time.time() - t0, 1)
RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
suffix = f"_MUTATE_{ARM}" if ARM else ""
with open(os.path.join(HERE, f"scs1_wkb{suffix}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
P_(f"runtime {RES['seconds']} s, peak RSS {RES['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, f"scs1_wkb{suffix}.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
