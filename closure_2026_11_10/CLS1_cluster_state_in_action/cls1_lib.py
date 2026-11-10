#!/usr/bin/env python3
"""CLS1 shared library: necessary-condition windows for a static clock state of action (A) on X-COP.

Units as DT2/DT3: kpc, Msun, km/s; G in kpc (km/s)^2 / Msun. mu_K enters in 1/kpc internally, printed per Mpc.
See FROZEN_CRITERIA.md. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import csv
import itertools
import math
from pathlib import Path
import runpy

import numpy as np
from astropy.io import fits

ROOT = Path(__file__).resolve().parents[2]
PRIOR = runpy.run_path(str(ROOT/'research_closure_2026_11_10/DT2_response_audit/cluster/check_shape.py'),
                       run_name='dt2_cluster_readonly')
G, RHO_BG, A0, NAMES = PRIOR['G'], PRIOR['RHO_BG'], PRIOR['A0'], PRIOR['NAMES']
FOOTINGS = ('canonical', 'alt')
C = 299792.458                      # km/s
ALPHA = 4*math.pi*G/C**2            # kpc/Msun:  x = ALPHA n / mu^2  (n Msun/kpc^3, mu 1/kpc)
KPC_PER_MPC = 1000.0
HECS = ROOT.parent/'_external_data/hecs_omnibus_2026_11_10/table2.tsv'
HECS_ID = {'A85': 'A85', 'A1795': 'A1795', 'ZW1215': 'Zw1215', 'A2029': 'A2029', 'A2142': 'A2142',
           'A2319': 'A2319', 'A644': 'A644'}

# mutation switches (MUTATE twins; never set in the graded run)
MUT = {'MU1': False, 'MU2': False, 'MU3': False}


def alpha_eff():
    return ALPHA*(1e6 if MUT['MU3'] else 1.0)


def law(gN, a0):
    return 0.5*gN + np.sqrt(0.25*gN*gN + a0*gN)


def F_src(M, r, a0):
    """Action-exact inverse of the simple law: source mass from enclosed dynamical mass (DT3)."""
    return M*M/(M + a0*r*r/G) if M > 0 else 0.0


def n_of_m(m, mu):
    """Charge density n from active material density m = n (1 + 2x), x = alpha n / mu^2 (exact inverse)."""
    a = alpha_eff()/mu**2
    m = np.asarray(m, dtype=float)
    return 2*m/(1 + np.sqrt(1 + 8*a*m))


def x_of_m(m, mu):
    return alpha_eff()*n_of_m(m, mu)/mu**2


# ----------------------------------------------------------------------------------------------- data
def baryon_profile(name):
    d = ROOT/'real_research/data/xcop'/name
    with fits.open(d/f'{name}_fgas_profile.fits') as f:
        gas = f[1].data.copy(); rg500 = f[1].header['R500']
    with fits.open(d/f'{name}_mstar.fits') as f:
        st = f[2].data.copy()
    with fits.open(d/f'{name}_hydro_mass.fits') as f:
        r500 = f[1].header['R500']
    rg, mg = np.asarray(gas['RADIUS'])*rg500, np.asarray(gas['MGAS'])
    rs, ms = np.asarray(st['RADIUS']), np.asarray(st['MSTAR'])
    return dict(rg=rg, mg=mg, rs=rs, ms=ms, r500=r500)


def loglog(r, rr, mm, mode):
    """log-log interpolation; below range: first-two-point slope; above: mode 'lo' flat, 'hi' linear in r."""
    lr, lm = np.log(rr), np.log(mm)
    if r < rr[0]:
        s = (lm[1]-lm[0])/(lr[1]-lr[0]); return float(np.exp(lm[0] + s*(math.log(r)-lr[0])))
    if r > rr[-1]:
        return float(mm[-1]*(1.0 if mode == 'lo' else r/rr[-1]))
    return float(np.exp(np.interp(math.log(r), lr, lm)))


def Mb(prof, r, mode='mid'):
    return loglog(r, prof['rg'], prof['mg'], mode) + loglog(r, prof['rs'], prof['ms'], mode)


def read_hecs():
    rows = {}
    with open(HECS) as f:
        lines = [l.rstrip('\n') for l in f if not l.startswith('#') and l.strip()]
    head = lines[0].split('\t')
    for l in lines[3:]:
        p = [c.strip() for c in l.split('\t')]
        if len(p) < len(head): continue
        rows[p[head.index('ID')]] = dict(R200=float(p[head.index('R200')]), eR200=float(p[head.index('e_R200')]),
                                       M200=float(p[head.index('M200')]), eM200=float(p[head.index('e_M200')]),
                                       sigma=float(p[head.index('sigmaCl')]))
    return rows


def load(with_hecs):
    clusters = PRIOR['load']()
    hecs = read_hecs() if with_hecs else {}
    out = {}
    for name in NAMES:
        prof = baryon_profile(name)
        rows = [dict(p, Blo=p['B'], Bhi=p['B']) for p in clusters[name]]
        info = {}
        if with_hecs and HECS_ID[name] in hecs:
            h = hecs[HECS_ID[name]]
            r = h['R200']*1000.0
            covered = r <= prof['rg'][-1] and r <= prof['rs'][-1]
            rows.append(dict(x=r/prof['r500'], r=r, M=h['M200']*1e14, E=h['eM200']*1e14,
                             B=Mb(prof, r), Blo=Mb(prof, r, 'lo'), Bhi=Mb(prof, r, 'hi'), hecs=True))
            info = dict(hecs=h, covered=bool(covered), r200_over_r500=r/prof['r500'])
        out[name] = dict(rows=rows, prof=prof, info=info)
    return out


# ------------------------------------------------------------------------------------- bounds per triple
def bounds(rows, a0, ns):
    rr = np.array([p['r'] for p in rows])
    V = 4*math.pi/3*rr**3
    src_lo = np.array([F_src(max(p['M']-ns*p['E'], 0.0), p['r'], a0) for p in rows])
    src_hi = np.array([F_src(p['M']+ns*p['E'], p['r'], a0) for p in rows])
    Blo = np.array([p['Blo'] for p in rows]); Bhi = np.array([p['Bhi'] for p in rows])
    # absolute dust active mass inside r (background restored, as DT3)
    dmin = src_lo - Bhi + RHO_BG*V
    dmax = src_hi - Blo + RHO_BG*V
    floor = np.maximum.accumulate(np.maximum(src_lo, Blo))
    ceil = np.minimum.accumulate(src_hi[::-1])[::-1]       # nondecreasing source: M(r) <= min of later uppers
    nq = len(rows)-1
    dlo = [PRIOR['potential'](floor[q], rr[q], rr[q+1], a0) for q in range(nq)]
    dhi = [PRIOR['potential'](ceil[q+1], rr[q], rr[q+1], a0) for q in range(nq)]
    tri = []
    for i, j, k in itertools.combinations(range(len(rows)), 3):
        Dmin = float(sum(dlo[i:j])); Dmax = float(sum(dhi[i:k]))
        if MUT['MU2']: Dmin = 0.0
        o = dict(idx=[i, j, k], r=[float(rr[i]), float(rr[j]), float(rr[k])], Dmin=Dmin, Dmax=Dmax,
                 Dmin_c2=Dmin/C**2, Dmax_c2=Dmax/C**2)
        # UP: upper density at i (ball), lower density at j (shell j..k)
        u_up = float(dmax[i]/V[i]); l_up = float((dmin[k]-dmax[j])/(V[k]-V[j]))
        o.update(UP_u=u_up, UP_l=l_up, UP_active=bool(l_up > 0 and u_up > 0))
        # LOW: lower density at i (shell i..j), upper density at k (shell j..k)
        l_lo = float((dmin[j]-dmax[i])/(V[j]-V[i])); u_lo = float((dmax[k]-dmin[j])/(V[k]-V[j]))
        o.update(LOW_l=l_lo, LOW_u=u_lo, LOW_active=bool(l_lo > 0 and l_lo > u_lo and not MUT['MU1']))
        tri.append(o)
    return dict(triples=tri, dmin=dmin.tolist(), dmax=dmax.tolist(), src_lo=src_lo.tolist(), src_hi=src_hi.tolist(),
                floor=floor.tolist(), ceil=ceil.tolist(), r=rr.tolist())


def up_margin(o, mu):
    """allowed log-Q span minus required (>= 0 passes)."""
    if not o['UP_active']: return np.inf*np.ones_like(mu)
    xu, xl = x_of_m(o['UP_u'], mu), x_of_m(o['UP_l'], mu)
    return np.log1p(xu) - np.log1p(xl) - o['Dmin_c2']


def low_margin(o, mu):
    """D_max/c^2 minus the forced log-Q span (>= 0 passes)."""
    if not o['LOW_active']: return np.inf*np.ones_like(mu)
    xl, xu = x_of_m(o['LOW_l'], mu), x_of_m(o['LOW_u'], mu)
    return o['Dmax_c2'] - (np.log1p(xl) - np.log1p(xu))


def passes(tri, mu):
    mu = np.atleast_1d(np.asarray(mu, dtype=float))
    ok = np.ones_like(mu, dtype=bool)
    for o in tri:
        ok &= up_margin(o, mu) >= 0
        ok &= low_margin(o, mu) >= 0
    return ok


def closed_form_edges(o):
    """Leading-order (x linear in m, m = n) edges in mu (1/kpc): UP gives mu <= mu_hi; LOW gives mu >= mu_lo."""
    a = alpha_eff(); res = {}
    if o['UP_active']:
        E = math.exp(o['Dmin_c2']); u, l = o['UP_u'], o['UP_l']
        res['mu_hi'] = (math.inf if E == 1 else math.sqrt(a*(u - l*E)/(E - 1))) if u > l*E else 0.0
    if o['LOW_active']:
        E = math.exp(o['Dmax_c2']); l, u = o['LOW_l'], o['LOW_u']
        res['mu_lo'] = math.sqrt(a*(l - u*E)/(E - 1)) if l > u*E else 0.0
    return res


def window(tri, lo=-6.0, hi=8.0, step=0.002):
    """Pass set on the log grid (mu per Mpc), as intervals with bisection-refined edges."""
    lg = np.arange(lo, hi + step/2, step)
    mu = 10**lg/KPC_PER_MPC
    ok = passes(tri, mu)
    ivs = []
    i = 0
    while i < len(ok):
        if ok[i]:
            j = i
            while j+1 < len(ok) and ok[j+1]: j += 1
            a = refine(tri, lg[i-1], lg[i]) if i > 0 else lo
            b = refine(tri, lg[j], lg[j+1]) if j+1 < len(ok) else hi
            ivs.append([10**a, 10**b])
            i = j+1
        else:
            i += 1
    return ivs, int(ok.sum())


def refine(tri, a, b):
    """bisect in log10 mu (per Mpc) between a pass and a fail point."""
    fa = bool(passes(tri, 10**a/KPC_PER_MPC)[0])
    for _ in range(80):
        m = 0.5*(a+b)
        if bool(passes(tri, 10**m/KPC_PER_MPC)[0]) == fa: a = m
        else: b = m
        if abs(b-a) < 1e-12: break
    return 0.5*(a+b)


def intersect(A, B):
    out = []
    for a0, a1 in A:
        for b0, b1 in B:
            lo, hi = max(a0, b0), min(a1, b1)
            if lo <= hi: out.append([lo, hi])
    return out


def in_window(ivs, mu):
    return any(a <= mu <= b for a, b in ivs)


# --------------------------------------------------------------------------------------- construction ODE
def integrate(prof, a0, mu, x0, r_eval, r_start=1.0, nstep=3000, with_baryons=True, bg=True):
    """Vectorized RK4 in ln r. x0: array of central x. Returns M_dyn at r_eval (array [len(x0), len(r_eval)]),
    min x over the run, and M_dust at r_eval."""
    x0 = np.atleast_1d(np.asarray(x0, dtype=float))
    a_eff = alpha_eff()/mu**2
    r_end = max(r_eval)*1.0000001
    s0, s1 = math.log(r_start), math.log(r_end)
    h = (s1-s0)/nstep
    sgrid = s0 + h*np.arange(nstep+1)
    rgrid = np.exp(sgrid)
    if with_baryons:
        Mbg = np.array([Mb(prof, r) for r in rgrid]); Mbm = np.array([Mb(prof, math.exp(s+h/2)) for s in sgrid])
    else:
        Mbg = np.zeros_like(rgrid); Mbm = np.zeros_like(rgrid)

    def m_of_x(x):
        n = x/a_eff                         # x = alpha n / mu^2
        return n*(1 + 2*x)

    def rhs(s, r, x, Md, mb):
        src = mb + Md - (RHO_BG*4*math.pi/3*r**3 if bg else 0.0)
        src = np.maximum(src, 0.0)
        g = law(G*src/r**2, a0) if a0 > 0 else G*src/r**2
        dx = -(1 + x)*g/C**2*r
        dM = 4*math.pi*r**3*m_of_x(x)
        return dx, dM

    x = x0.copy(); Md = 4*math.pi/3*r_start**3*m_of_x(x)
    xmin = x.copy()
    out_M = np.zeros((len(x0), len(r_eval))); out_D = np.zeros_like(out_M)
    targets = sorted(range(len(r_eval)), key=lambda t: r_eval[t])
    ti = 0
    for k in range(nstep):
        s, r = sgrid[k], rgrid[k]; rm = math.exp(s+h/2); r1 = rgrid[k+1]
        k1 = rhs(s, r, x, Md, Mbg[k])
        k2 = rhs(s+h/2, rm, x+h/2*k1[0], Md+h/2*k1[1], Mbm[k])
        k3 = rhs(s+h/2, rm, x+h/2*k2[0], Md+h/2*k2[1], Mbm[k])
        k4 = rhs(s+h, r1, x+h*k3[0], Md+h*k3[1], Mbg[k+1])
        xn = x + h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); Mn = Md + h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        while ti < len(targets) and r1 >= r_eval[targets[ti]]:
            t = targets[ti]; re = r_eval[t]
            w = (math.log(re)-s)/h
            xe = x + w*(xn-x); Me = Md + w*(Mn-Md)
            src = np.maximum(Mb(prof, re) + Me - (RHO_BG*4*math.pi/3*re**3 if bg else 0.0), 0.0) if with_baryons \
                else np.maximum(Me, 0.0)
            g = law(G*src/re**2, a0) if a0 > 0 else G*src/re**2
            out_M[:, t] = g*re**2/G; out_D[:, t] = Me
            ti += 1
        x, Md = xn, Mn
        xmin = np.minimum(xmin, x)
    return out_M, xmin, out_D

Adopts_nothing = "Adopts nothing. kappa = 1/2 FITTED; not theory closed."
