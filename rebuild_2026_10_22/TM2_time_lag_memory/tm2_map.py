#!/usr/bin/env python3
"""TM2 Part A: lagged gas term on UX6's static map of the Bullet. Criteria FROZEN_CRITERIA.md, committed alone first. TM2_MUTATE=1 for the twin.
A description: no action. Histories PROVISIONAL, from simulations with massive halos, kinematics only. kappa = 1/2 FITTED; not theory closed. Reinstates nothing."""
import os, sys, json, math, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
MUT = os.environ.get("TM2_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"tm2_map{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CHECKS = {}
def check(n, ok, d):
    CHECKS[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30; MYR = 3.15576e13; C = 299792458.0; KMS = 1.02271e-3  # kpc/Myr per km/s
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt")
KFIT = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json"))); PI2 = math.pi**2
SIG_CRIT = 1.827e9; Z_BOX = 18000.0; SIG_DELTA = math.sqrt((1/8)**2 + 0.15**2); SIG_O3 = 0.15
GAS = [(2.0e14, 565.0, 190.0, 90.0), (1.5e13, 505.0, 525.0, 120.0), (1.5e13, 90.0, 670.0, 170.0), (-6.8e12, 70.0, 670.0, 170.0)]
GAL = [(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)]
BCG = np.array([[0.0, 0.0], [820.0, 220.0]]); GASP = np.array([[190.0, 90.0], [670.0, 170.0]])
GRP = [0, 1, 1, 1]  # X32's assignment
OBS300 = (3.5e14, 2.3e14); PAIRS = {"main": (BCG[0], GASP[0]), "sub": (BCG[1], GASP[1])}
D0 = float(np.hypot(*BCG[1])); UH = BCG[1]/D0; NH = np.array([-UH[1], UH[0]]); DMAX = 3500.0; TH = 10000.0
HIST = dict(P=dict(t=180., q=.12, p=1, b=0.), t150=dict(t=150., q=.12, p=1, b=0.), t260=dict(t=260., q=.12, p=1, b=0.), q09=dict(t=180., q=.09, p=1, b=0.), q40=dict(t=180., q=.40, p=1, b=0.), p2=dict(t=180., q=.12, p=2, b=0.), b256=dict(t=180., q=.12, p=1, b=256.))
FIT_TAUS = (5., 10., 20., 40., 80., 150., 300., 600., 1200., 2500., 5000., 10000.)

def law(g, a): return 0.5*g + np.sqrt(0.25*g*g + a*g)
def fld(X, Y, Z, c):
    M, a, xc, yc = c; dx = X - xc; dy = Y - yc
    f = -G*M*MSUN/((dx*dx + dy*dy + Z*Z + a*a)**1.5*KPC**3)*KPC
    return f*dx, f*dy, f*Z
def rho_pl(X, Y, Z, c):
    M, a, xc, yc = c; return M/a**3*(1 + ((X - xc)**2 + (Y - yc)**2 + Z*Z)/a**2)**-2.5
def enc_table(comps, centre):
    r = np.geomspace(0.5, 3e5, 1200); nod, wt = np.polynomial.legendre.leggauss(64); tot = np.zeros_like(r)
    for M, a, x, y in comps:
        d = float(np.hypot(x - centre[0], y - centre[1]))
        s2 = r[:, None]**2 + d*d - 2*r[:, None]*d*nod[None, :]; rho = 3*M/(4*math.pi*a**3)*(1 + s2/a**2)**-2.5
        sh = 4*math.pi*r*r*(0.5*(rho*wt[None, :]).sum(1)); lg = np.log(r)
        tot += np.r_[0.0, np.cumsum(0.5*(sh[1:]*r[1:] + sh[:-1]*r[:-1])*np.diff(lg))] + M*(r[0]/a)**3/(1 + (r[0]/a)**2)**1.5*(d == 0)
    return r, np.maximum(tot, 0.0)

class Sys:
    """history + baryon model. Node 0 is a delta at s = 0, last node reads pre-merger."""
    def __init__(s, hist, gas=GAS, gal=GAL, bcg=BCG, grp=GRP, gasfac=1.0, nsub=(8, 16), Vf=(0.0, 0.0), kernel="exp", static=False):
        s.h, s.gas, s.gal, s.bcg, s.grp, s.gasfac, s.Vf, s.kernel, s.static = hist, gas, gal, bcg, grp, gasfac, np.array(Vf, float)*KMS, kernel, static
        t = hist["t"]; s.e = np.r_[np.linspace(0, t, nsub[0] + 1), np.geomspace(t, TH, nsub[1] + 1)[1:]]; s.mid = 0.5*(s.e[1:] + s.e[:-1]); s.nn = len(s.mid) + 1
        s.sn = np.r_[0.0, s.mid]; s.o = [np.array(g[2:4]) - bcg[grp[i]] for i, g in enumerate(gas)]
        s.ngrp = len(gal); s.tr = np.array([[s.x_c(c, q) for q in s.sn] for c in range(s.ngrp)]); s.dl = s.tr[:, 0:1, :] - s.tr  # Delta_c(s)
        s.comps = [s.comps_at(q) for q in s.sn]
        ctab = [[(i, s.grp[i]) for i in range(len(gas)) if s.grp[i] == c] for c in range(s.ngrp)]; s.ctab = ctab
        s.tab = {}; s._dyn = {}
        for c in range(s.ngrp):
            r, ms = enc_table([gal[c]], bcg[c]); lst = []
            for j, q in enumerate(s.sn):
                _, mg = enc_table([s.comps[j][i] for i, _ in ctab[c]], bcg[c]) if not static else enc_table([gas[i] for i, _ in ctab[c]], bcg[c])
                if j > 0: _, mg = enc_table([s.restored(i, q) for i, _ in ctab[c]], bcg[c])
                lst.append(mg)
            f = G*MSUN/(r*KPC)**2; s.tab[c] = (r, np.log(r), f*np.array(lst), f*ms)
    def rel(s, q):
        if s.static: return s.bcg[-1] - s.bcg[0]
        h = s.h; v = D0*UH + (q/h["t"])*(h["b"]*NH - D0*UH); n = np.hypot(*v); return v*min(1.0, DMAX/n) if n > 0 else v
    def x_c(s, c, q):
        if s.static: return s.bcg[c]
        com = s.bcg[0] + s.h["q"]*D0*UH; return com - s.h["q"]*s.rel(q) if c == 0 else com + (1 - s.h["q"])*s.rel(q)
    def g_of(s, q):
        if s.static: return 1.0
        return max(0.0, 1 - q/s.h["t"])**s.h["p"]
    def mfac(s, i, q):
        return s.gasfac if (s.grp[i] == 1 and q > s.h["t"]) else 1.0
    def comps_at(s, q):
        out = []
        for i, g_ in enumerate(s.gas):
            p = s.x_c(s.grp[i], q) + s.o[i]*s.g_of(q); out.append((g_[0]*s.mfac(i, q), g_[1], p[0], p[1]))
        return out
    def restored(s, i, q):
        """component i, in its own BCG's frame, at offset g(s) o_i, about its present BCG"""
        g_ = s.gas[i]; p = s.bcg[s.grp[i]] + s.o[i]*s.g_of(q); return (g_[0]*s.mfac(i, q), g_[1], p[0], p[1])
    def weights(s, tau):
        """tau scalar or array; rule 'tau0', 'inf' as strings"""
        if isinstance(tau, str):
            w = np.zeros(s.nn); w[0 if tau == "tau0" else -1] = 1.0; return w
        tau = np.asarray(tau, float); e = s.e.reshape((-1,) + (1,)*tau.ndim)
        if s.kernel == "exp":
            w = np.exp(-e[:-1]/tau) - np.exp(-e[1:]/tau)
        else:
            w = (np.minimum(e[1:], 2*tau) - np.minimum(e[:-1], 2*tau))
        w = w/np.maximum(w.sum(0), 1e-300)
        return np.concatenate([np.zeros((1,) + tau.shape), w], axis=0)
    def tau_rule(s, rule, foot, r):
        a0 = A0F[foot]
        if rule == "R-a0": return C/a0/MYR
        if rule == "R-a0b": return C/(2*math.pi*a0)/MYR
        if rule in ("tau0", "inf"): return rule
        if rule.startswith("T"): return float(rule[1:])
        fac = 2*math.pi if rule == "R-dyn2" else 1.0; return fac*r
    def rdyn(s, foot, R3, c):
        """sqrt(r/law(g_group(r))) in Myr, r in kpc, present baryons"""
        k = (foot, c)
        if k not in s._dyn:
            r, lr, tg, ts = s.tab[c]; rr = r*KPC; tau = np.sqrt(rr/law(tg[0] + ts, A0F[foot]))/MYR; s._dyn[k] = (lr, np.maximum(tau, 0.0))
        lr, tau = s._dyn[k]; return np.interp(np.log(np.maximum(R3, 20.0)), lr, tau)
    def fields(s, X, Y, Z, which):
        """which: -1 fixed frame, else flow c. Returns V (nn, 3, ...), M (nn, ...)"""
        V = np.zeros((s.nn, 3) + X.shape); M = np.zeros((s.nn,) + X.shape)
        for j, q in enumerate(s.sn):
            sh = (s.Vf*q if which < 0 else s.dl[which, j])
            for c_ in s.comps[j]:
                f = fld(X, Y, Z, (c_[0], c_[1], c_[2] + sh[0], c_[3] + sh[1]))
                V[j, 0] += f[0]; V[j, 1] += f[1]; V[j, 2] += f[2]
            M[j] = np.sqrt(V[j, 0]**2 + V[j, 1]**2 + V[j, 2]**2)
        return V, M
    def present(s, X, Y, Z):
        v = [fld(X, Y, Z, c) for c in s.gas]; gv = tuple(sum(q[i] for q in v) for i in range(3)); st = [fld(X, Y, Z, c) for c in s.gal]; st = tuple(sum(q[i] for q in st) for i in range(3)); return gv, st

def mix(w, A):
    """w (nn,) or (nn, ...); A (nn, ...) or (nn, 3, ...)"""
    if w.ndim == 1: return np.tensordot(w, A, axes=1)
    if A.ndim == w.ndim + 1: return np.einsum("i...,ij...->j...", w, A)
    return (w*A).sum(0)

def evaluate(sys_, specs, X, Y, Z, reg=True):
    """specs: name -> (form, rule, foot, k). Returns name -> extra field tuple"""
    gv, st = sys_.present(X, Y, Z); out = {}; FF = {}; memo = {}
    forms = {sp[0] for sp in specs.values()}
    def need(w_):
        if w_ not in FF: FF[w_] = sys_.fields(X, Y, Z, w_)
        return FF[w_]
    rc = [np.sqrt((X - sys_.bcg[c][0])**2 + (Y - sys_.bcg[c][1])**2 + Z*Z) for c in range(sys_.ngrp)]
    wstar = [rho_pl(X, Y, Z, c) for c in sys_.gal]; tot = sum(wstar); wstar = [w_/tot for w_ in wstar]
    def tauval(rule, foot):
        if rule in ("R-dyn", "R-dyn2"):
            near = np.argmin(np.array(rc), axis=0); t = np.choose(near, [sys_.rdyn(foot, rc[c], c) for c in range(sys_.ngrp)]) if sys_.ngrp > 1 else sys_.rdyn(foot, rc[0], 0)
            return sys_.tau_rule(rule, foot, t)
        return sys_.tau_rule(rule, foot, None)
    def mem(kind, rule, foot):
        key = (kind, rule, foot if rule in ("R-dyn", "R-dyn2", "R-a0", "R-a0b") else "")
        if key not in memo:
            w = sys_.weights(tauval(rule, foot))
            if kind == "F":
                V, M = need(-1); memo[key] = (mix(w, V), mix(w, M))
            else:
                vv = 0.0; mm = 0.0
                for c in range(sys_.ngrp):
                    V, M = need(c); vv = vv + wstar[c]*mix(w, V); mm = mm + wstar[c]*mix(w, M)
                memo[key] = (vv, mm)
        return memo[key]
    def w3tab(rule, foot, c):
        key = ("W3", rule, foot, c)
        if key not in memo:
            r, lr, tg, ts = sys_.tab[c]
            if rule in ("R-dyn", "R-dyn2"):
                sys_.rdyn(foot, r, c); tau = np.interp(lr, *sys_._dyn[(foot, c)]) * (2*math.pi if rule == "R-dyn2" else 1.0); w = sys_.weights(tau); gm = (w*tg).sum(0)
            else:
                gm = np.tensordot(sys_.weights(sys_.tau_rule(rule, foot, None)), tg, axes=1)
            memo[key] = (lr, gm, gm + ts)
        return memo[key]
    for n, (form, rule, foot, k) in specs.items():
        a0 = A0F[foot]; gb = [gv[i] + st[i] for i in range(3)]
        if reg: gb[1] = gb[1] + a0/1000.0
        g = np.sqrt(gb[0]**2 + gb[1]**2 + gb[2]**2); L = law(g, a0); m = L/np.maximum(g, 1e-300)
        if form == "LAW": out[n] = tuple(gb[i]*(m - 1) for i in range(3)); continue
        if form in ("F1", "W1"):
            _, mg = mem(form[0], rule, foot); h = k*mg/a0; out[n] = tuple(gb[i]*(m*(1 + h) - 1) for i in range(3))
        elif form in ("F2", "W2"):
            v, _ = mem(form[0], rule, foot); sg = -1.0 if (MUT and form == "F2") else 1.0; o = [gb[i]*(m - 1) + sg*k*(L/a0)*v[i] for i in range(3)]; out[n] = tuple(o)
        else:
            o = [gb[i]*(m - 1) for i in range(3)]
            for c in range(sys_.ngrp):
                lr, gm, gt = w3tab(rule, foot, c); r_ = np.maximum(rc[c], 0.5); q = np.log(r_); f = -law(np.interp(q, lr, gt), a0)*k*np.interp(q, lr, gm)/a0/r_
                o[0] = o[0] + f*(X - sys_.bcg[c][0]); o[1] = o[1] + f*(Y - sys_.bcg[c][1]); o[2] = o[2] + f*Z
            out[n] = tuple(o)
    return out

def zgrid(Z, n_in, n_out, z_in):
    return np.concatenate([np.linspace(0.0, z_in, n_in + 1), np.geomspace(z_in, Z, n_out + 1)[1:]])
ZS = zgrid(Z_BOX, 150, 150, 1500.0); ZM = np.concatenate([np.linspace(0.0, 1200.0, 61), np.geomspace(1200.0, 6000.0, 41)[1:]])
def sig_pl(D, M, a): return M*a*a/(math.pi*(D*D + a*a)**2)
def M2D(x0, y0, R, plum, nrho=400, nphi=720):
    rho = np.linspace(0.0, R, nrho + 1); phi = (np.arange(nphi) + 0.5)*2*math.pi/nphi
    X = x0 + rho[:, None]*np.cos(phi)[None, :]; Y = y0 + rho[:, None]*np.sin(phi)[None, :]; S = np.zeros_like(X)
    for M, a, xc, yc in plum: S += sig_pl(np.sqrt((X - xc)**2 + (Y - yc)**2), M, a)
    return float(np.trapz(np.sum(S, axis=1)*(2*math.pi/nphi)*rho, rho))
def surface(sys_, specs, x0, y0, R, nphi=120, nrho=60):
    phi = (np.arange(nphi) + 0.5)*2*math.pi/nphi; CP, SP = np.cos(phi), np.sin(phi)
    X = (x0 + R*CP)[:, None]*np.ones((1, len(ZS))); Y = (y0 + R*SP)[:, None]*np.ones((1, len(ZS))); Zg = np.broadcast_to(ZS[None, :], X.shape)
    e = evaluate(sys_, specs, X, Y, Zg); side = {n: 2.0*np.trapz(np.sum(e[n][0]*CP[:, None] + e[n][1]*SP[:, None], axis=0)*(2*math.pi/nphi)*R, ZS) for n in specs}
    rho = np.linspace(0.0, R, nrho + 1); Xc = x0 + rho[:, None]*CP[None, :]; Yc = y0 + rho[:, None]*SP[None, :]
    e = evaluate(sys_, specs, Xc, Yc, np.full_like(Xc, Z_BOX)); out = {}
    for n in specs:
        caps = 2.0*np.trapz(np.sum(e[n][2], axis=1)*(2*math.pi/nphi)*rho, rho); out[n] = -(side[n] + caps)*KPC**2/(4*math.pi*G)/MSUN
    return out
STEP = 20.0; XS = np.arange(-500.0, 1400.0 + 1e-9, STEP); YS = np.arange(-400.0, 700.0 + 1e-9, STEP); XX, YY = np.meshgrid(XS, YS, indexing="ij")
def maps(sys_, specs, h=2.0):
    S = {n: np.zeros_like(XX) for n in specs}
    for j0 in range(0, len(YS), 6):
        ys = YS[j0:j0 + 6]; X, Y, Z = np.meshgrid(XS, ys, ZM, indexing="ij"); div = {n: 0.0 for n in specs}
        for ax, (dx, dy, dz) in enumerate(((h, 0, 0), (0, h, 0), (0, 0, h))):
            for sgn in (1.0, -1.0):
                e = evaluate(sys_, specs, X + sgn*dx, Y + sgn*dy, Z + sgn*dz)
                for n in specs: div[n] = div[n] + sgn*e[n][ax]
        for n in specs: S[n][:, j0:j0 + 6] = 2.0*np.trapz(-div[n]/(2*h)/(4*math.pi*G)*KPC**2/MSUN, ZM, axis=2)
    base = sum(sig_pl(np.hypot(XX - c[2], YY - c[3]), c[0], c[1]) for c in GAS + GAL)
    for n in specs: S[n] += base
    return S
def peak(S, A, B):
    mid = 0.5*(A + B); w = np.hypot(XX - mid[0], YY - mid[1]) <= 350.0
    i = int(np.argmax(np.where(w, S, -np.inf))); a, b = np.unravel_index(i, S.shape)
    edge = not (0 < a < S.shape[0] - 1 and 0 < b < S.shape[1] - 1) or not w[a - 1:a + 2, b - 1:b + 2].all()
    lm = (not edge) and S[a, b] >= S[a - 1:a + 2, b - 1:b + 2].max() and (S[a - 1:a + 2, b - 1:b + 2] == S[a, b]).sum() == 1
    return np.array([XX[a, b], YY[a, b]]), bool(lm)
def observe(S, m):
    o = {}
    for k, (bc, gc) in PAIRS.items():
        pk, lm = peak(S, bc, gc); dg = float(np.hypot(*(pk - gc))); db = float(np.hypot(*(pk - bc))); sep = float(np.hypot(*(bc - gc)))
        o[k] = dict(peak=pk.tolist(), local_max=lm, d_gas=dg, d_bcg=db, delta=dg/sep, Z=(dg/sep - 1)/SIG_DELTA, guard=bool(lm and db < dg), dkappa=(m[f"bcg_{k}"] - m[f"gas_{k}"])/(math.pi*1e4)/SIG_CRIT)
    o["M300"] = [m["BCG1"], m["BCG3"]]; o["ZO3"] = [(m["BCG1"]/OBS300[0] - 1)/SIG_O3, (m["BCG3"]/OBS300[1] - 1)/SIG_O3]; o["ratio"] = m["BCG3"]/m["BCG1"]
    pos = [not (o[k]["guard"] and abs(o[k]["Z"]) <= 3 and o[k]["dkappa"] > 0) for k in PAIRS]; o["pos_or_sign_fail"] = bool(any(pos)); o["mass_fail"] = bool(any(abs(z) > 3 for z in o["ZO3"]))
    o["cls"] = "FAIL" if (o["pos_or_sign_fail"] or o["mass_fail"]) else ("PASS" if all(abs(o[k]["Z"]) <= 2 for k in PAIRS) and all(abs(z) <= 2 for z in o["ZO3"]) else "TENSION")
    o["margin"] = max(abs(o["main"]["Z"]), abs(o["sub"]["Z"]), abs(o["ZO3"][0]), abs(o["ZO3"][1]))
    return o
APS = dict(BCG1=(BCG[0], 300.0), BCG3=(BCG[1], 300.0), bcg_main=(BCG[0], 100.0), gas_main=(GASP[0], 100.0), bcg_sub=(BCG[1], 100.0), gas_sub=(GASP[1], 100.0))
PLUM = GAS + GAL
_b = {a: M2D(*c, R, PLUM) for a, (c, R) in APS.items()}
def run(sys_, specs):
    sf = {a: surface(sys_, specs, *c, R) for a, (c, R) in APS.items()}; S = maps(sys_, specs); res = {}
    for n in specs:
        m = {a: _b[a] + sf[a][n] for a in APS}; res[n] = (observe(S[n], m), S[n], m)
    return res

say("="*90); say("TM2_time_lag_memory Part A" + ("  [MUTATE]" if MUT else "")); say("="*90)
say(f"c/a0 Gyr canonical {C/A0F['canonical']/MYR/1e3:.1f}, alt {C/A0F['alt']/MYR/1e3:.1f}; c/(2 pi a0) {C/A0F['canonical']/MYR/1e3/(2*math.pi):.1f}, {C/A0F['alt']/MYR/1e3/(2*math.pi):.1f}. History numbers PROVISIONAL.")
say(f"Light-cone size: v r/c at 2700 km/s = {2700e3/C*1000:.1f} kpc per Mpc; uniform motion has no lag to O(v^2/c^2) (retarded field points at the present position).")
# K2
a = A0F["canonical"]; k = 10.0
SK2 = Sys(dict(t=180., q=.12, p=1, b=0.), gas=[(1e14, 400.0, 0.0, 0.0)], gal=[(1e13, 100.0, 0.0, 0.0)], bcg=np.zeros((1, 2)), grp=[0], static=True)
rt = np.array([20.0, 100.0, 300.0, 1000.0, 3000.0]); z0 = np.zeros(5); gv, st = SK2.present(rt, z0, z0); gg = np.abs(gv[0]); gb = gg + np.abs(st[0]); want = law(gb, a)*(1 + k*gg/a); dev = {}
SK2.x_c = lambda c, q: np.zeros(2)
for fm in ("F1", "F2", "W1", "W2", "W3"):
    e = evaluate(SK2, {"x": (fm, "T300", "canonical", k)}, rt, z0, z0, reg=False)["x"]; dev[fm] = float(np.max(np.abs((gb + np.abs(e[0]))/want - 1)))
    if MUT and fm == "F2": dev[fm] = float(np.max(np.abs((gb - e[0])/want - 1)))  # signed: the flipped term no longer adds
check("K2", max(dev.values()) <= 1e-3, f"concentric static vs law x (1 + k g_gas/a0), {dev}")

RULES = ["R-a0", "R-a0b", "R-dyn", "R-dyn2"] + [f"T{t:g}" for t in FIT_TAUS]; FORMS = ("F1", "F2", "W1", "W2", "W3")
def kval(f, kl): return {"fit": KFIT[f], "pi2": PI2, "k065": .65*KFIT[f], "k135": 1.35*KFIT[f]}[kl]
def specs_P():
    d = {}
    for f in FEET:
        d[f"LAW|-|{f}|0"] = ("LAW", "tau0", f, 0.0)
        for fm in FORMS:
            for kl in ("fit", "pi2"):
                for r in RULES + ["tau0"]: d[f"{fm}|{r}|{f}|{kl}"] = (fm, r, f, kval(f, kl))
        d[f"W3|inf|{f}|fit"] = ("W3", "inf", f, KFIT[f]); d[f"W3|inf|{f}|pi2"] = ("W3", "inf", f, PI2)
        for fm in ("W2", "W3"):
            for kl in ("k065", "k135"):
                for r in ("R-dyn", "T300", "T1200"): d[f"{fm}|{r}|{f}|{kl}"] = (fm, r, f, kval(f, kl))
    return d
def specs_H(forms=FORMS):
    return {f"{fm}|{r}|{f}|fit": (fm, r, f, KFIT[f]) for f in FEET for fm in forms for r in RULES}
RES = {}
def row(tag, n, o):
    a_, b_ = o["main"], o["sub"]
    say(f"{tag:9s} {n:24s} m {a_['peak']} {a_['d_gas']:.0f},{a_['d_bcg']:.0f} Z{a_['Z']:+.2f} lm{int(a_['local_max'])} | s {b_['peak']} {b_['d_gas']:.0f},{b_['d_bcg']:.0f} Z{b_['Z']:+.2f} lm{int(b_['local_max'])} | dk {a_['dkappa']:+.3f} {b_['dkappa']:+.3f} | M300 {o['M300'][0]/1e14:.2f} ({o['ZO3'][0]:+.1f}) {o['M300'][1]/1e14:.2f} ({o['ZO3'][1]:+.1f}) | {o['ratio']:.2f} | {o['cls']} | margin {o['margin']:.2f}")
if MUT:
    sp = {f"LAW|-|{f}|0": ("LAW", "tau0", f, 0.0) for f in FEET}
    sp.update({f"F1|tau0|{f}|fit": ("F1", "tau0", f, KFIT[f]) for f in FEET})
    # K1 mutate: gas x 2 in the reference system
    gas2 = [(2*c[0],) + c[1:] for c in GAS]; S0 = Sys(HIST["P"], gas=gas2); P = run(S0, sp)
else:
    S0 = Sys(HIST["P"]); P = run(S0, specs_P())
# K7
dmax = 0.0
for hn, h in HIST.items():
    S_ = Sys(h); v = np.hypot(S_.dl[:, 1:, 0], S_.dl[:, 1:, 1])/np.maximum(S_.sn[1:], 1e-9)  # kpc/Myr
    dmax = max(dmax, float(v.max()))
if MUT: dmax *= 1e5
cc = C/1e3*KMS
check("K7", dmax < cc, f"max |Delta_c(s)|/s over nodes and histories {dmax/KMS:.0f} km/s against c; v/c {dmax/cc:.3f}")
# K1
UX6 = json.load(open(os.path.join(RB, "UX6_gas_term_bullet", "ux6_results.json")))["rows"]
pairs = []
for f in FEET:
    pairs += [(f"LAW|-|{f}|0", f"LAW|{f}")]
    if not MUT:
        pairs += [(f"F1|tau0|{f}|fit", f"L1|{f}|fit"), (f"F2|tau0|{f}|fit", f"L2|{f}|fit"), (f"W1|tau0|{f}|fit", f"L1|{f}|fit"), (f"W2|tau0|{f}|fit", f"L2|{f}|fit"), (f"W3|tau0|{f}|fit", f"N1|{f}|fit"), (f"W3|inf|{f}|fit", f"N2|{f}|fit")]
devm = []; devk = []; pkb = 0.0; detail = []
for a_, b_ in pairs:
    o = P[a_][0]; u = UX6[b_]; dm = max(abs(o["M300"][0]/u["M300"][0] - 1), abs(o["M300"][1]/u["M300"][1] - 1)); dk = max(abs(o[q]["dkappa"]/u[q]["dkappa"] - 1) for q in PAIRS); pb = max(float(np.hypot(*(np.array(o[q]["peak"]) - np.array(u[q]["peak"])))) for q in PAIRS)
    devm.append(dm); devk.append(dk); pkb = max(pkb, pb); detail.append(f"{b_}: M {dm:.4f} dk {dk:.4f} pk {pb:.0f}")
check("K1", max(devm) <= 0.02 and max(devk) <= 0.02 and pkb <= STEP*math.sqrt(2) + 1e-9, f"tau to 0 and limits vs UX6, max M {max(devm):.4f}, dkappa {max(devk):.4f}, peak {pkb:.0f} kpc; " + "; ".join(detail))
# K6
CTRL = {}
for f in FEET:
    S0m = P[f"LAW|-|{f}|0"]; S_, m0 = S0m[1], S0m[2]; a_ = 150.0; tgt = np.array([OBS300[0] - m0["BCG1"], OBS300[1] - m0["BCG3"]])
    A = np.array([[M2D(*BCG[0], 300.0, [(1.0, a_, *BCG[0])]), M2D(*BCG[0], 300.0, [(1.0, a_, *BCG[1])])], [M2D(*BCG[1], 300.0, [(1.0, a_, *BCG[0])]), M2D(*BCG[1], 300.0, [(1.0, a_, *BCG[1])])]]); Mc = np.linalg.solve(A, tgt)
    for lab, cen in (("onBCG", BCG), ("onGas", GASP)):
        if MUT and lab == "onBCG": cen = GASP
        pl = [(Mc[0], a_, *cen[0]), (Mc[1], a_, *cen[1])]; T_ = S_ + sum(sig_pl(np.hypot(XX - c[2], YY - c[3]), c[0], c[1]) for c in pl); m = {q: m0[q] + M2D(*APS[q][0], APS[q][1], pl) for q in APS}; CTRL[f"{lab}|{f}"] = observe(T_, m)
check("K6", all(CTRL[f"onBCG|{f}"]["cls"] == "PASS" and CTRL[f"onGas|{f}"]["cls"] == "FAIL" for f in FEET), str({k: v["cls"] for k, v in CTRL.items()}))
if MUT:
    json.dump(dict(checks=CHECKS), open(os.path.join(HERE, "tm2_map_MUTATE.json"), "w"), indent=1)
    say("MUTATE required failures: " + ", ".join(f"{k} {'FAILED' if not CHECKS[k] else 'passed (BAD)'}" for k in ("K1", "K2", "K6", "K7"))); OUT.close(); sys.exit(1)
# K4, K3
n = "F2|R-dyn|canonical|fit"; mp = float(P[n][1][np.hypot(XX, YY) < 300.0].sum()*STEP*STEP); ms = P[n][0]["M300"][0]
check("K4", abs(mp/ms - 1) <= 0.08, f"map {mp:.3e} vs surface {ms:.3e} at BCG1, {100*(mp/ms - 1):+.1f} %")
sk = {f"{fm}|T300|canonical|fit": (fm, "T300", "canonical", KFIT["canonical"]) for fm in ("F2", "W2")}
Sd = Sys(HIST["P"], nsub=(16, 32)); sf = {a_: surface(Sd, sk, *c, R) for a_, (c, R) in APS.items() if a_ in ("BCG1", "BCG3")}
dv = max(abs((_b[a_] + sf[a_][q])/(P[q][2][a_]) - 1) for a_ in ("BCG1", "BCG3") for q in sk); check("K3", dv <= 0.01, f"nodes x 2 M300 max rel {dv:.2e}")
say("\n=== primary history P: every cell ===")
for n, v in P.items(): RES["P|" + n] = v[0]; row("P", n, v[0])
for n, c in CTRL.items(): row("ctrl", n, c)
del P
say("\n=== other histories, k fit ===")
for hn, h in HIST.items():
    if hn == "P": continue
    R_ = run(Sys(h), specs_H())
    for n, v in R_.items(): RES[f"{hn}|{n}"] = v[0]; row(hn, n, v[0])
    say(f"  RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB")
say("\n=== frames, F forms, P, k fit ===")
qq = HIST["P"]; Vm = -qq["q"]*D0/qq["t"]/KMS*UH; Vs = (1 - qq["q"])*D0/qq["t"]/KMS*UH; FR = {"main_rest": Vm, "sub_rest": Vs, "+600u": 600*UH, "-600u": -600*UH, "+600n": 600*NH, "-600n": -600*NH}
for fn, Vf in FR.items():
    R_ = run(Sys(HIST["P"], Vf=tuple(Vf)), specs_H(("F1", "F2")))
    for n, v in R_.items(): RES[f"{fn}|{n}"] = v[0]; row(fn, n, v[0])
say("\n=== reported: bullet-side pre-merger gas x 2, boxcar kernel; P, k fit ===")
sp2 = specs_H(("W2", "W3"))
for tag, s_ in (("gasx2", Sys(HIST["P"], gasfac=2.0)), ("boxcar", Sys(HIST["P"], kernel="box"))):
    R_ = run(s_, sp2 if tag == "gasx2" else specs_H())
    for n, v in R_.items(): RES[f"{tag}|{n}"] = v[0]; row(tag, n, v[0])
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9; check("K5", rss < 4.0, "RSS under 4 GB"); print(f"RSS {rss:.2f}", file=sys.stderr)
# labels
say("\n=== labels on P, frozen; form x rule ===")
LAB = {}; OTHER = [h for h in HIST if h != "P"]
for fm in FORMS:
    for r in RULES:
        cells = [RES[f"P|{fm}|{r}|{f}|{kl}"] for f in FEET for kl in ("fit", "pi2")]; fit = [RES[f"P|{fm}|{r}|{f}|fit"] for f in FEET]
        if all(c["pos_or_sign_fail"] for c in cells): l = "DEAD"
        elif all(c["cls"] == "PASS" for c in fit):
            ok = sum(all(RES[f"{h}|{fm}|{r}|{f}|fit"]["cls"] in ("PASS", "TENSION") for f in FEET) for h in OTHER); l = "BULLET PASS" + (" ROBUST" if ok >= 5 else "")
        elif all(not c["pos_or_sign_fail"] for c in fit): l = "WOUNDED"
        else: l = "MIXED"
        LAB[f"{fm}|{r}"] = l; m_ = [round(c["margin"], 2) for c in fit]; say(f"  {fm} {r}: {l}; margins {m_}; classes {[c['cls'] for c in cells]}; dk sub {[round(c['sub']['dkappa'], 3) for c in fit]}; ratio {[round(c['ratio'], 2) for c in fit]}")
need = ("K1", "K2", "K6"); json.dump(dict(checks=CHECKS, labels=LAB, rows=RES), open(os.path.join(HERE, "tm2_map.json"), "w"), indent=0, default=float)
say(f"\nVerdict allowed: {all(CHECKS[k] for k in need)}; failed checks: {[k for k, v in CHECKS.items() if not v]}"); OUT.close()
