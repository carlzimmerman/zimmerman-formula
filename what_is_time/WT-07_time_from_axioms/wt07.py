#!/usr/bin/env python3
"""WT-07: what time structure ("now") do the framework's own axioms force?

Criteria: FROZEN_CRITERIA.md (committed alone first, ed636472e).  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never
pooled; Z = 5.7888; cold energy is real gravitating mass, no particle species; not theory closed.

Run:   OMP_NUM_THREADS=1 nice -n 10 python3 wt07.py                -> wt07.out, wt07_results.json
       WT07_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 wt07.py  -> wt07_MUTATE.out, wt07_results_MUTATE.json
Guard: exits 75 if RSS > 0.9 GB, swap growth > 1 GB, or free+inactive < 8 GB.
Own covariant machinery (sympy, truncated series in eps); nothing imported from other lanes.
"""
import os, sys, re, json, math, itertools, time, subprocess
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("WT07_MUTATE", "0") == "1"
OUTF = os.path.join(HERE, "wt07_MUTATE.out" if MUT else "wt07.out")
JSONF = os.path.join(HERE, "wt07_results_MUTATE.json" if MUT else "wt07_results.json")
_fh = open(OUTF, "w")


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    _fh.write(s + "\n")
    _fh.flush()


# ------------------------------------------------------------------------------------------------------------ guard
def _sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def _swap_used_mb():
    m = re.search(r"used = ([0-9.]+)([MG])", _sh(["sysctl", "-n", "vm.swapusage"]))
    if not m:
        return 0.0
    v = float(m.group(1))
    return v * 1024 if m.group(2) == "G" else v


def _free_inactive_gb():
    s = _sh(["vm_stat"])
    ps = int(re.search(r"page size of (\d+) bytes", s).group(1))
    g = lambda nm: int(re.search(nm + r":\s+(\d+)", s).group(1))
    return (g("Pages free") + g("Pages inactive")) * ps / 1e9


def _rss_gb():
    return int(_sh(["ps", "-o", "rss=", "-p", str(os.getpid())]).strip()) * 1024 / 1e9


SWAP0 = _swap_used_mb()
PEAK = {"rss_gb": 0.0}


def guard(tag=""):
    r = _rss_gb(); sw = _swap_used_mb() - SWAP0; fi = _free_inactive_gb()
    PEAK["rss_gb"] = max(PEAK["rss_gb"], r)
    if r > 0.9 or sw > 1024 or fi < 8:
        P(f"GUARD EXIT 75 at {tag}: rss {r:.2f} GB, swap growth {sw:.0f} MB, free+inactive {fi:.1f} GB")
        sys.exit(75)


guard("start")

# ------------------------------------------------------------------------------------------------------------ constants
G_SI, C_SI, MSUN = 6.67430e-11, 299792458.0, 1.98847e30
PC = 3.0856775814913673e16; KPC = 1e3 * PC; MPC = 1e6 * PC
AU = 1.495978707e11; YR = 3.15576e7; GYR = 1e9 * YR
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
H0 = 67.4e3 / MPC
OMB = 0.0493; OMC = OMB * 5.364; OMM = OMB + OMC; OML = 1.0 - OMM
KAPPA = 0.5; Z_ = 5.7888
LSTAR = {"24pc": 24 * PC, "1kpc": 1 * KPC}
KH_CORNERS = {"F3_lo": (9.62e-14, 7.29e-3), "F3_hi": (3.2e-9, 0.0667)}       # CFG292 window corners (alpha_c, c2)
F3B_ALPHA = {"F3b_hi": 3.2e-9, "F3b_lo": 8.2e-16}                            # FP14 regulator window ends
V_BULLET = 4700e3; CS_MAX = 104e3                                            # ARGON10 G2; WT-02 (L* = 1 kpc)
V_PEC = 370e3
T_AGE = {"13.8Gyr": 13.8 * GYR, "1Gyr": 1.0 * GYR}

RES = {"criteria": "ed636472e", "mutate": MUT, "settings": dict(kappa="1/2 FITTED", Z=Z_, footings=A0, H0_kms_Mpc=67.4,
                                                               Omega_b=OMB, Omega_c=OMC, Omega_L=OML)}
KOK = {}


def chk(name, ok, msg=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    return bool(ok)


P("WT-07  what time structure do the framework's axioms force?" + ("   [MUTATE]" if MUT else ""))
P("  criteria ed636472e; kappa = 1/2 FITTED; Z = 5.7888; footings never pooled; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2")

# ======================================================================================================================
# truncated-series machinery: every quantity is a list [c0, c1, c2] of sympy expressions (coefficients of eps^0..2)
# ======================================================================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
XX = [t, x, y, z]
eps = sp.Symbol("epsilon")
h, hd = sp.symbols("h h_d", real=True)
Km, Ls = sp.symbols("K_m L_s", positive=True)
Akh, ck2 = sp.symbols("A_kh c_k2", real=True)
sig, kk = sp.symbols("sigma k")
a = sp.Function("a", positive=True)(t)
chib = sp.Function("chib")(t)
ZERO = [sp.S(0), sp.S(0), sp.S(0)]


def ex(e):
    return sp.expand(e)


def E(c0=0, c1=0, c2=0):
    return [sp.S(c0), sp.S(c1), sp.S(c2)]


def isz(p):
    return all(c == 0 for c in p)


def add(*ps):
    r = [sp.S(0)] * 3
    for p in ps:
        for i in range(3):
            r[i] += p[i]
    return r


def scal(c, p):
    return [c * p[i] for i in range(3)]


def mul(p, q):
    if isz(p) or isz(q):
        return list(ZERO)
    r = [sp.S(0)] * 3
    for i in range(3):
        if p[i] == 0:
            continue
        for j in range(3 - i):
            if q[j] != 0:
                r[i + j] += p[i] * q[j]
    return r


def inv(p):
    f0, f1, f2 = p
    return [1 / f0, -f1 / f0 ** 2, f1 ** 2 / f0 ** 3 - f2 / f0 ** 2]


def sqrtE(p):
    f0, f1, f2 = p
    s = sp.sqrt(f0)
    return [s, f1 / (2 * s), f2 / (2 * s) - f1 ** 2 / (8 * s * f0)]


def dE(p, v):
    return [sp.diff(c, v) for c in p]


def exE(p):
    return [ex(c) for c in p]


def LC(*idx):
    return sp.LeviCivita(*idx)


# ---------------------------------------------------------------------------------------------- the covariant build
def build(grav=True, frame="leaf", op="intrinsic", sub=True, chibar=False, stiff_frame=None):
    """Quadratic-order covariant ingredients on flat FRW (a(t)), Newtonian potential Phi = Psi (if grav), medium labels
    phi = (x - eps xi, y - eps eta, z), chi = chibar(t) + eps dchi, lambda = eps dlam, leaf T = t + eps dT.
    frame: 'leaf' (normal from T) | 'medium' (normal = medium u).  op: 'intrinsic' | 'projected' | 'box'.
    stiff_frame: frame used for u^2 and tau (default = frame; P1 uses 'medium')."""
    xi = sp.Function("xi")(t, x); eta = sp.Function("eta")(t, x)
    dchi = sp.Function("dchi")(t, x); dlam = sp.Function("dlam")(t, x)
    Phi = sp.Function("Phi")(t, x) if grav else sp.S(0)
    dT = sp.Function("dT")(t, x)
    F = dict(xi=xi, eta=eta, dchi=dchi, dlam=dlam, Phi=Phi, dT=dT)
    # metric (diagonal), exact in eps (linear)
    gdn = [E(-1, -2 * Phi), E(a ** 2, -2 * a ** 2 * Phi), E(a ** 2, -2 * a ** 2 * Phi), E(a ** 2, -2 * a ** 2 * Phi)]
    gup = [inv(gm) for gm in gdn]
    gup = [exE(gm) for gm in gup]
    detg = mul(mul(gdn[0], gdn[1]), mul(gdn[2], gdn[3]))
    sqrtg = exE(sqrtE(scal(-1, detg)))
    # Christoffels Gamma^r_{mn} (diagonal metric)
    dg = [[dE(gdn[m], XX[n]) for n in range(4)] for m in range(4)]       # dg[m][n] = d_n g_mm
    Gam = [[[list(ZERO) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for r in range(4):
        for m in range(4):
            for n in range(4):
                s_ = list(ZERO)
                if r == n:
                    s_ = add(s_, dg[r][m])                               # d_m g_rn
                if r == m:
                    s_ = add(s_, dg[r][n])                               # d_n g_rm
                if m == n:
                    s_ = add(s_, scal(-1, dg[m][r]))                     # - d_r g_mn
                if not isz(s_):
                    Gam[r][m][n] = exE(scal(sp.Rational(1, 2), mul(gup[r], s_)))
    # medium current (Jt = sqrt(-g) J)
    phis = [E(x, -xi), E(y, -eta), E(z, 0)]
    dphi = [[dE(p_, X) for X in XX] for p_ in phis]
    Jt = []
    for mu in range(4):
        s_ = list(ZERO)
        for (al, be, ga) in itertools.permutations([i for i in range(4) if i != mu], 3):
            lc = LC(mu, al, be, ga)
            if lc == 0:
                continue
            term = mul(mul(dphi[0][al], dphi[1][be]), dphi[2][ga])
            if not isz(term):
                s_ = add(s_, scal(lc, term))
        Jt.append(exE(s_))
    assert Jt[0][0] == 1, "J^0 orientation"
    JgJ = list(ZERO)
    for mu in range(4):
        JgJ = add(JgJ, mul(mul(Jt[mu], gdn[mu]), Jt[mu]))
    nsg = exE(sqrtE(scal(-1, JgJ)))                                      # n sqrt(-g)
    isg = exE(inv(sqrtg))
    n_ = exE(mul(nsg, isg))
    inv_nsg = exE(inv(nsg))
    uup = [exE(mul(Jt[mu], inv_nsg)) for mu in range(4)]
    udn = [exE(mul(gdn[mu], uup[mu])) for mu in range(4)]
    theta = list(ZERO)
    for mu in range(4):
        theta = add(theta, dE(mul(sqrtg, uup[mu]), XX[mu]))
    theta = exE(mul(theta, isg))
    # leaf normal
    Tf = [E(1 if mu == 0 else 0, sp.diff(dT, XX[mu])) for mu in range(4)]
    TT = list(ZERO)
    for mu in range(4):
        TT = add(TT, mul(mul(gup[mu], Tf[mu]), Tf[mu]))
    NT = exE(inv(sqrtE(scal(-1, TT))))
    ndn_T = [exE(scal(-1, mul(NT, Tf[mu]))) for mu in range(4)]
    nup_T = [exE(mul(gup[mu], ndn_T[mu])) for mu in range(4)]
    KT = list(ZERO)
    for mu in range(4):
        KT = add(KT, dE(mul(sqrtg, nup_T[mu]), XX[mu]))
    KT = exE(mul(KT, isg))
    # chosen frame for the constraint operator
    if frame == "leaf":
        nup, ndn, Kf = nup_T, ndn_T, KT
    else:
        nup, ndn, Kf = uup, udn, theta
    # chi
    chi = E(chib if chibar else 0, dchi)
    dch = [dE(chi, X) for X in XX]
    nab = [[None] * 4 for _ in range(4)]
    for m in range(4):
        for n in range(4):
            s_ = dE(dE(chi, XX[m]), XX[n])
            for r in range(4):
                if not isz(Gam[r][m][n]) and not isz(dch[r]):
                    s_ = add(s_, scal(-1, mul(Gam[r][m][n], dch[r])))
            nab[m][n] = exE(s_)

    def frame_objs(nup_, ndn_, K_):
        hup_ = [[exE(add(gup[m] if m == n else list(ZERO), mul(nup_[m], nup_[n]))) for n in range(4)] for m in range(4)]
        hdn_ = [[exE(add(gdn[m] if m == n else list(ZERO), mul(ndn_[m], ndn_[n]))) for n in range(4)] for m in range(4)]
        hmix_ = [[exE(add(E(1) if m == n else list(ZERO), mul(ndn_[m], nup_[n]))) for n in range(4)] for m in range(4)]
        ndchi_ = list(ZERO)
        for m in range(4):
            ndchi_ = add(ndchi_, mul(nup_[m], dch[m]))
        ndchi_ = exE(ndchi_)
        hnab = list(ZERO)
        for m in range(4):
            for n in range(4):
                if not isz(hup_[m][n]) and not isz(nab[m][n]):
                    hnab = add(hnab, mul(hup_[m][n], nab[m][n]))
        hnab = exE(hnab)
        return hup_, hdn_, hmix_, ndchi_, hnab

    hup, hdn, hmix, ndchi, hnab = frame_objs(nup, ndn, Kf)
    if op == "intrinsic":
        OP = exE(add(hnab, mul(Kf, ndchi)))
    elif op == "projected":
        OP = hnab
    else:                                                                # box
        OP = list(ZERO)
        for m in range(4):
            OP = add(OP, mul(gup[m], nab[m][m]))
        OP = exE(OP)
    # u^2 and tau in the stiffness frame
    sf = stiff_frame or frame
    if sf == frame:
        shup, shdn, shmix, sndchi, shnab, sK, sn_dn = hup, hdn, hmix, ndchi, hnab, Kf, ndn
        s_intr = (op == "intrinsic")
    else:
        sup_, sdn_, sK = (uup, udn, theta) if sf == "medium" else (nup_T, ndn_T, KT)
        shup, shdn, shmix, sndchi, shnab = frame_objs(sup_, sdn_, sK)
        sn_dn = sdn_
        s_intr = False
    u2 = list(ZERO)
    for m in range(4):
        for n in range(4):
            if not isz(shup[m][n]):
                u2 = add(u2, mul(mul(shup[m][n], dch[m]), dch[n]))
    u2 = exE(u2)
    # Hessian projected (+ extrinsic-curvature term if intrinsic)
    DD = [[list(ZERO) for _ in range(4)] for _ in range(4)]
    for m in range(4):
        for n in range(4):
            s_ = list(ZERO)
            for al in range(4):
                if isz(shmix[m][al]):
                    continue
                for be in range(4):
                    if isz(shmix[n][be]) or isz(nab[al][be]):
                        continue
                    s_ = add(s_, mul(mul(shmix[m][al], shmix[n][be]), nab[al][be]))
            DD[m][n] = s_
    if s_intr:
        # K_mn = h_m^al (d_al n_n - Gam^r_{al n} n_r)
        for m in range(4):
            for n in range(4):
                s_ = list(ZERO)
                for al in range(4):
                    if isz(shmix[m][al]):
                        continue
                    dn_ = dE(sn_dn[n], XX[al])
                    for r in range(4):
                        if not isz(Gam[r][al][n]):
                            dn_ = add(dn_, scal(-1, mul(Gam[r][al][n], sn_dn[r])))
                    s_ = add(s_, mul(shmix[m][al], dn_))
                DD[m][n] = add(DD[m][n], mul(s_, sndchi))
    trace = OP if (sf == frame and op != "box") else shnab
    if s_intr:
        trace = exE(add(shnab, mul(sK, sndchi)))
    tau = [[exE(add(DD[m][n], scal(-sp.Rational(1, 3), mul(shdn[m][n], trace)))) for n in range(4)] for m in range(4)]
    tt = list(ZERO)
    for m in range(4):
        for n in range(4):
            if not isz(tau[m][n]):
                tt = add(tt, mul(mul(mul(tau[m][n], tau[m][n]), gup[m]), gup[n]))
    tt = exE(tt)
    # leaf density n_Sigma = -n_mu J^mu (frame normal), and nbar(T) = a(T)^-3 to O(eps)
    nS = list(ZERO)
    for mu in range(4):
        nS = add(nS, mul(ndn[mu], Jt[mu]))
    nS = exE(scal(-1, mul(nS, isg)))
    nbarT = E(a ** -3, -3 * a ** -4 * sp.diff(a, t) * dT) if frame == "leaf" else E(a ** -3, 0)
    src = exE(add(nS, scal(-1, nbarT))) if sub else nS
    if op == "box" or frame == "medium":
        src = n_ if not sub else exE(add(n_, scal(-1, nbarT)))
    C = exE(add(OP, scal(-Km, src)))
    return dict(F=F, sqrtg=sqrtg, nsg=nsg, n=n_, uup=uup, udn=udn, theta=theta, NT=NT, ndn_T=ndn_T, nup_T=nup_T, KT=KT,
                OP=OP, u2=u2, tt=tt, nS=nS, C=C, Tf=Tf, gdn=gdn, gup=gup)


def lagrangian(B, fol=None):
    """K-rescaled quadratic Lagrangian density (per comoving coordinate volume)."""
    F = B["F"]
    bulk = add(scal(-Km, B["nsg"]),
               mul(B["sqrtg"], add(scal(-sp.Rational(1, 2), B["u2"]), scal(-sp.Rational(3, 8) * Ls ** 2, B["tt"]))))
    lam_term = mul(E(0, F["dlam"]), mul(B["sqrtg"], B["C"]))
    L = bulk[2] + lam_term[2]
    if F["Phi"] != 0:
        L += -a * sp.diff(F["Phi"], x) ** 2 / 2
    if fol is not None:
        L += fol
    return ex(L)


A_SUBS = None


def at0(e):
    e = e.subs(sp.Derivative(a, (t, 3)), h ** 3 + 3 * h * hd).subs(sp.Derivative(a, (t, 2)), h ** 2 + hd)
    e = e.subs(sp.Derivative(a, t), h).subs(a, 1)
    return e.subs(t, 0)


def modes(L2, fields):
    eqs = sp.euler_equations(L2, fields, [t, x])
    amps = sp.symbols(" ".join(f"Amp{i}" for i in range(len(fields))))
    if len(fields) == 1:
        amps = (amps,)
    phase = sig * t + sp.I * kk * x
    M = sp.zeros(len(fields), len(fields))
    for i, e_ in enumerate(eqs):
        q = e_.lhs
        for f_, A_ in zip(fields, amps):
            q = q.subs(f_, A_ * sp.exp(phase))
        q = q.doit()
        q = ex(sp.powsimp(ex(q * sp.exp(-phase))))
        q = ex(at0(q))
        for j, A_ in enumerate(amps):
            M[i, j] = ex(q.coeff(A_))
    return M


def subs_chibar(L2, kind):
    """Background chibar(t): 'C938' -> D^2 chibar = -3H chibar' = K_m nbar (S1d); 'P1' -> box chibar = K_m nbar."""
    if kind == "C938":
        d1 = -Km / (3 * a ** 2 * sp.diff(a, t))
    else:
        d1 = (-Km * t - sp.Rational(2, 3) * Km / h) / a ** 3
    L2 = L2.subs(sp.Derivative(chib, (t, 2)), sp.diff(d1, t)).subs(sp.Derivative(chib, t), d1)
    return ex(L2)


# ======================================================================================================================
# candidate linear systems on FRW
# ======================================================================================================================
def khronon_ck2(alpha, c2):
    return c2 * (2 - alpha) / (alpha * (2 + 3 * c2))          # CFG292 c_S^2 at beta = 0


def system(cid, grav=True, variant="main"):
    """Returns dict(M, fields, names, B, L2).  variant: 'main' | 'MU2' (projected D^2 + chibar, no subtraction)."""
    ell = sp.Function("ell")(t, x); nu = sp.Function("nu")(t, x)
    if cid == "C938":
        B = build(grav, frame="medium", op="projected", sub=False, chibar=True)
        L2 = subs_chibar(lagrangian(B), "C938")
        F = B["F"]; names = ["xi", "eta", "dchi", "dlam"]
    elif cid == "P1":
        B = build(grav, frame="medium", op="box", sub=False, chibar=True)
        L2 = subs_chibar(lagrangian(B), "P1")
        F = B["F"]; names = ["xi", "eta", "dchi", "dlam"]
    else:
        proj = (variant == "MU2")
        B = build(grav, frame="leaf", op="projected" if proj else "intrinsic", sub=not proj, chibar=proj)
        F = dict(B["F"]); F["ell"] = ell; F["nu"] = nu
        dT = F["dT"]; Phi = F["Phi"]
        kin_kh = (Akh / 2) * a * sp.diff(Phi - sp.diff(dT, t), x) ** 2
        if cid == "F0":
            fol = None; names = ["xi", "eta", "dchi", "dlam"]
        elif cid == "F1":
            lock = ex(B["ndn_T"][1][1] - B["udn"][1][1])
            fol = a ** 3 * ell * lock; names = ["xi", "dchi", "dlam", "dT", "ell"]
        elif cid == "F1p":
            s_ = list(ZERO)
            for mu in range(4):
                s_ = add(s_, mul(B["uup"][mu], B["Tf"][mu]))
            lock = ex(s_[1])
            fol = a ** 3 * ell * lock; names = ["xi", "eta", "dchi", "dlam", "dT", "ell"]
        elif cid == "F2":
            fol = a ** 3 * nu * B["KT"][1]; names = ["xi", "eta", "dchi", "dlam", "dT", "nu"]
        elif cid == "F3":
            fol = kin_kh - (Akh * ck2 / 2) * sp.diff(dT, x, 2) ** 2 / a; names = ["xi", "eta", "dchi", "dlam", "dT"]
        elif cid == "F3b":
            fol = a ** 3 * nu * B["KT"][1] + kin_kh; names = ["xi", "eta", "dchi", "dlam", "dT", "nu"]
        else:
            raise ValueError(cid)
        L2 = lagrangian(B, fol)
        if proj:
            L2 = subs_chibar(L2, "C938")
        if cid == "F0":
            L2 = ex(L2.subs(dT, 0).doit())
        if cid == "F1":
            L2 = ex(L2.subs(F["eta"], 0).doit())
    if grav:
        names = names + ["Phi"]
    fields = [F[nm] for nm in names]
    M = modes(L2, fields)
    return dict(M=M, fields=fields, names=names, B=B, L2=L2)


def char_poly(M):
    det = sp.factor(M.det(method="berkowitz"))
    num = sp.numer(sp.together(det))
    pol = sp.Poly(sp.expand(num), sig)
    cs = pol.all_coeffs()
    while len(cs) > 1 and sp.simplify(cs[-1]) == 0:                      # drop sigma = 0 roots
        cs = cs[:-1]
    return det, cs


def hadamard(cs, par, ks, dps=60):
    mp.mp.dps = dps
    syms = (h, hd, Km, Ls, Akh, ck2, kk)
    fns = [sp.lambdify(syms, c_, "mpmath") for c_ in cs]
    out = []
    for kv in ks:
        vals = [mp.mpf(par["h"]), mp.mpf(par["hd"]), mp.mpf(par["Km"]), mp.mpf(par["Ls"]), mp.mpf(par.get("A", 0)),
                mp.mpf(par.get("ck2", 0)), mp.mpf(kv)]
        cf = [mp.mpc(f_(*vals)) for f_ in fns]
        while len(cf) > 1 and abs(cf[0]) == 0:
            cf = cf[1:]
        sc = max(abs(c_) for c_ in cf)
        cf = [c_ / sc for c_ in cf]
        if len(cf) == 1:
            out.append(float("-inf")); continue
        try:
            rts = mp.polyroots(cf, maxsteps=4000, extraprec=4 * dps)
        except mp.libmp.libhyper.NoConvergence:
            rts = mp.polyroots(cf, maxsteps=40000, extraprec=20 * dps)
        out.append(max(float(mp.re(r_)) for r_ in rts))
    return out


def had_label(mx, ks):
    top, prev = mx[-1], mx[-2]
    slope = (math.log10(top) - math.log10(prev)) / (math.log10(ks[-1]) - math.log10(ks[-2])) if (top > 0 and prev > 0) else float("nan")
    if top >= 1e3 and slope >= 0.9:
        return "ILL-POSED", slope
    if all(m_ <= 10 for m_ in mx):
        return "WELL-POSED", slope
    return "UNRESOLVED", slope


def frozen_bg(zv):
    E2 = OMM * (1 + zv) ** 3 + OML
    Hz = H0 * math.sqrt(E2)
    return dict(Km=1.5 * OMC * (1 + zv) ** 3 / E2, hd=-1.5 * OMM * (1 + zv) ** 3 / E2, Hz=Hz)


KS = [10.0 ** p_ for p_ in range(2, 11)]
BGS = []
for zv in (0.0, 10.0):
    fb = frozen_bg(zv)
    for lk, Lv in LSTAR.items():
        for hs, hn in ((1, "expanding"), (-1, "contracting")):
            BGS.append(dict(tag=f"z{zv:g}|{lk}|{hn}", h=hs, hd=fb["hd"], Km=fb["Km"], Ls=Lv * fb["Hz"] / C_SI))


def kh_par(cid, sign=1):
    if cid in ("F3_lo", "F3_hi"):
        al, c2 = KH_CORNERS[cid]
        al = sign * al
        return dict(A=al, ck2=khronon_ck2(al, c2))
    if cid in ("F3b_hi", "F3b_lo"):
        return dict(A=sign * F3B_ALPHA[cid], ck2=0)
    return {}


def base_cid(cid):
    return {"F3_lo": "F3", "F3_hi": "F3", "F3b_hi": "F3b", "F3b_lo": "F3b"}.get(cid, cid)


def rows_have_sigma(M, names, rows=("dlam", "dchi")):
    out = {}
    for r_ in rows:
        if r_ in names:
            i = names.index(r_)
            out[r_] = any(sp.expand(M[i, j]).has(sig) for j in range(M.shape[1]))
    return out


def kinetic_check(M, names, par, kv=1e4):
    C2 = M.applyfunc(lambda e_: sp.expand(e_).coeff(sig, 2))
    sub = {h: par["h"], hd: par["hd"], Km: par["Km"], Ls: par["Ls"], Akh: par.get("A", 0), ck2: par.get("ck2", 0), kk: kv}
    Cn = np.array(C2.subs(sub).evalf(), dtype=complex)
    Kin = -(Cn + Cn.conj().T) / 2
    idx = [i for i in range(len(names)) if np.any(np.abs(Kin[i]) > 0)]
    if not idx:
        return True, []
    ev = np.linalg.eigvalsh(Kin[np.ix_(idx, idx)])
    scale = max(np.max(np.abs(ev)), 1e-300)
    return bool(np.all(ev >= -1e-12 * scale)), [float(v) for v in ev]


# ======================================================================================================================
# K CONTROLS (K3 lemma, K2 static, K5 khronon toy, K6 torus, K7 leaf-gradient form); K1/K4 come with the candidate runs
# ======================================================================================================================
P("\n==================== K CONTROLS ====================")


def diag_metric_tools(coords, gd):
    n_ = len(coords)
    gi = [1 / g_ for g_ in gd]
    Gm = [[[0] * n_ for _ in range(n_)] for _ in range(n_)]
    for r in range(n_):
        for m in range(n_):
            for k_ in range(n_):
                s_ = 0
                if r == k_:
                    s_ += sp.diff(gd[r], coords[m])
                if r == m:
                    s_ += sp.diff(gd[r], coords[k_])
                if m == k_:
                    s_ -= sp.diff(gd[m], coords[r])
                Gm[r][m][k_] = gi[r] * s_ / 2
    return gi, Gm


def lap_beltrami(coords, gd, f):
    sq = sp.sqrt(sp.prod(gd))
    return sum(sp.diff(sq / gd[i] * sp.diff(f, coords[i]), coords[i]) for i in range(len(coords))) / sq


def check_identity_exact(coords, gd, f, leaf_idx):
    """Leaves coords[0] = const with unit normal along d_0 (g_00 = -1): covariant h nabla nabla f + K n.df vs leaf Laplacian."""
    gi, Gm = diag_metric_tools(coords, gd)
    n_ = len(coords)
    nab = [[sp.diff(f, coords[m], coords[k_]) - sum(Gm[r][m][k_] * sp.diff(f, coords[r]) for r in range(n_)) for k_ in range(n_)] for m in range(n_)]
    sq = sp.sqrt(-sp.prod(gd))
    Kx = sp.diff(sq, coords[0]) / sq                                      # div of n = d_0
    cov = sum(gi[i] * nab[i][i] for i in range(1, n_)) + Kx * sp.diff(f, coords[0])
    intr = lap_beltrami(coords[1:], gd[1:], f)
    proj_only = sum(gi[i] * nab[i][i] for i in range(1, n_))
    return sp.simplify(cov - intr), sp.simplify(proj_only - intr), sp.simplify(Kx)


tau_, rho_, th_, ph_ = sp.symbols("tau rho theta phi", positive=True)
fM = sp.Function("f")(tau_, rho_, th_)
r1, r2, KM_ = check_identity_exact([tau_, rho_, th_, ph_], [-1, tau_ ** 2, tau_ ** 2 * sp.sinh(rho_) ** 2,
                                                            tau_ ** 2 * sp.sinh(rho_) ** 2 * sp.sin(th_) ** 2], fM, 0)
a1, a2, a3 = [sp.Function(f"a{i}", positive=True)(t) for i in (1, 2, 3)]
fB = sp.Function("f")(t, x, y, z)
b1, b2, KB_ = check_identity_exact([t, x, y, z], [-1, a1 ** 2, a2 ** 2, a3 ** 2], fB, 0)
# perturbed FRW, tilted leaf T = t + eps dT, Phi, chibar(t) != 0 (O(eps))
Bk3 = build(True, frame="leaf", op="intrinsic", sub=True, chibar=True)
Fk = Bk3["F"]
OP0 = sp.simplify(Bk3["OP"][0])
intr1 = sp.diff(Fk["dchi"] - sp.diff(chib, t) * Fk["dT"], x, 2) / a ** 2
res_tilt = sp.simplify(Bk3["OP"][1] - intr1)
# leaf-constant lemma: chi = f(T) = f(t) + eps f'(t) dT
lemma_intr = sp.simplify(Bk3["OP"][1].subs(Fk["dchi"], sp.diff(chib, t) * Fk["dT"]).doit())
Bproj = build(True, frame="leaf", op="projected", sub=False, chibar=True)
lemma_proj0 = sp.simplify(Bproj["OP"][0])
nd2 = sp.simplify(sp.diff(chib, t, 2))                                      # (n.d)^2 f(T) at eps^0 = f''
KOK["K3"] = chk("K3_identity_and_lemma",
                r1 == 0 and b1 == 0 and res_tilt == 0 and OP0 == 0 and lemma_intr == 0 and lemma_proj0 != 0 and nd2 != 0,
                f"Milne residual {r1}, (projected-only residual {sp.simplify(r2)}; K = {KM_}); Bianchi I residual {b1} "
                f"(K = {KB_}); tilted perturbed FRW O(eps) residual {res_tilt}; intrinsic Laplacian of f(T): O(1) {OP0}, "
                f"O(eps) {lemma_intr}; projected operator on f(T) at O(1): {lemma_proj0}; (n.d)^2 f(T) = {nd2} != 0 => b = 0")
RES["K3"] = dict(milne_residual=str(r1), milne_projected_minus_intrinsic=str(r2), bianchi_residual=str(b1),
                 tilt_residual=str(res_tilt), lemma_intrinsic=str(lemma_intr), lemma_projected_O1=str(lemma_proj0))

# K2 (a): static slices of a general static metric: K_T = 0, so intrinsic = projected for any chi
Phs = sp.Function("Phis")(x, y, z); Pss = sp.Function("Psis")(x, y, z)
# general static metric (lapse N = e^Phi): K_T of the static slices
Ns = sp.exp(Phs)
gd_s = [-Ns ** 2, sp.exp(-2 * Pss), sp.exp(-2 * Pss), sp.exp(-2 * Pss)]
sq_s = sp.sqrt(-sp.prod(gd_s))
K_static = sp.simplify(sp.diff(sq_s * (1 / Ns), t) / sq_s)
# (b) NGC 3198 law reduction from E[M_c]
r_, G_ = sp.symbols("r G", positive=True); uS, gNS, a0S = sp.symbols("u g_N a_0", positive=True)
Wf = (-a0S * uS - a0S ** 2 * sp.log(1 - uS / a0S)) / (4 * sp.pi * G_)
Mc = sp.Function("M_c")(r_); Mb = sp.Function("M_b")(r_)
Lred = -G_ * (Mb + Mc) ** 2 / (2 * r_ ** 2) + 4 * sp.pi * r_ ** 2 * sp.Lambda(uS, Wf)(G_ * Mc / r_ ** 2)
ELr = sp.euler_equations(Lred, [Mc], [r_])[0].lhs.subs({Mc: uS * r_ ** 2 / G_, Mb: gNS * r_ ** 2 / G_}).doit()
fEL = sp.lambdify((uS, gNS, a0S, G_), sp.simplify(ELr), "math")
dat = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
Rr = dat[:, 0] * KPC; Vobs = dat[:, 1] * 1e3; Vg, Vd, Vb = dat[:, 3] * 1e3, dat[:, 4] * 1e3, dat[:, 5] * 1e3
gNb = (Vg * np.abs(Vg) + 0.61 * Vd * np.abs(Vd) + 0.61 * Vb * np.abs(Vb)) / Rr


def law_g(gN, a0):
    return 0.5 * (gN + math.sqrt(gN * gN + 4.0 * gN * a0))


k2b = {}; ULAW = {}
for f_ in FOOTS:
    a0 = A0[f_]; rel = []; us = []
    for gn in gNb:
        uu_ = brentq(lambda q: fEL(q, gn, a0, G_SI), 1e-300, a0 * (1 - 1e-15), xtol=1e-30, rtol=1e-15, maxiter=500)
        rel.append(abs((gn + uu_) / law_g(gn, a0) - 1)); us.append(uu_)
    k2b[f_] = float(max(rel)); ULAW[f_] = np.array(us)
KOK["K2"] = chk("K2_static_reduction", K_static == 0 and all(v_ <= 1e-12 for v_ in k2b.values()) and len(gNb) == 43,
                f"static slices: K_T = {K_static} (so intrinsic = projected = CFG938's D^2 for any chi); NGC 3198 (N = {len(gNb)}) "
                f"max|g/g_law - 1| canonical {k2b['canonical']:.2e}, alt {k2b['alt']:.2e} (line 1e-12)")
RES["K2"] = dict(K_static=str(K_static), ngc3198_maxrel=k2b)
guard("K2")

# K6: torus solvability (FFT, 32^3) + symbolic/numeric divergence on a conformally curved torus
Ng = 32
xs = np.linspace(0, 2 * np.pi, Ng, endpoint=False)
Xg, Yg, Zg = np.meshgrid(xs, xs, xs, indexing="ij")
nfield = 1.0 + 0.3 * np.sin(Xg) * np.cos(2 * Yg) + 0.2 * np.cos(Zg + Xg) + 0.1 * np.sin(3 * Yg)
Kmv = 0.4
nbar_ex = nfield.mean()
kx = np.fft.fftfreq(Ng, 1.0 / Ng)
KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij"); K2g = KX ** 2 + KY ** 2 + KZ ** 2


def torus_residual(nbar_used):
    S = Kmv * (nfield - nbar_used)
    Sk = np.fft.fftn(S)
    k0 = abs(Sk[0, 0, 0]) / Ng ** 3                                        # the k = 0 equation: 0 = mean(S)
    chik = np.zeros_like(Sk); m_ = K2g > 0
    chik[m_] = -Sk[m_] / K2g[m_]
    lap = np.real(np.fft.ifftn(-K2g * chik))
    return k0, float(np.max(np.abs(lap - S)))


k0_ex, res_ex = torus_residual(nbar_ex)
k0_bad, res_bad = torus_residual(1.01 * nbar_ex)
# curved torus: int sqrt(h) Lap_h chi = 0, conformal metric e^{2w} delta
wv = 0.3 * np.sin(Xg) * np.cos(Yg) + 0.1 * np.sin(Zg)
chiv = np.sin(Xg + Zg) + np.cos(2 * Yg) + 0.2 * np.sin(Xg) * np.sin(Yg) * np.sin(Zg)


def dspec(fv, ax):
    kf = [KX, KY, KZ][ax]
    return np.real(np.fft.ifftn(1j * kf * np.fft.fftn(fv)))


div = sum(dspec(np.exp(3 * wv) * np.exp(-2 * wv) * dspec(chiv, i), i) for i in range(3))   # sqrt(h) Lap_h chi
int_curved = float(np.sum(div) * (2 * np.pi / Ng) ** 3)
KOK["K6"] = chk("K6_torus_solvability", k0_ex <= 1e-10 and res_ex <= 1e-10 and abs(k0_bad - Kmv * 0.01 * nbar_ex) <= 1e-12
                and abs(int_curved) <= 1e-10,
                f"exact nbar: k=0 residual {k0_ex:.1e}, max|Lap chi - S| {res_ex:.1e}; nbar x 1.01: k=0 equation fails by "
                f"{k0_bad:.6e} = K_m 0.01 nbar ({Kmv * 0.01 * nbar_ex:.6e}), no solution; curved torus int sqrt(h) Lap_h chi = {int_curved:.1e}")
RES["K6"] = dict(k0_exact=k0_ex, res_exact=res_ex, k0_off=k0_bad, int_curved=int_curved)
guard("K6")

# K5: khronon toy, decoupled limit
Mk = system("F3", grav=False)["M"]
iT = ["xi", "eta", "dchi", "dlam", "dT"].index("dT")
eT = sp.expand(Mk[iT, iT].subs({Km: 0, h: 0, hd: 0}))
s2 = sp.Symbol("s2")
sol = sp.solve(sp.Eq(eT.subs(sig ** 2, s2), 0), s2)
al_, c2_ = KH_CORNERS["F3_hi"]
neg_eT = eT.subs({Akh: -al_, ck2: khronon_ck2(-al_, c2_)})
sol_neg = sp.solve(sp.Eq(neg_eT.subs(sig ** 2, s2), 0), s2)
KOK["K5"] = chk("K5_khronon_toy", len(sol) == 1 and sp.simplify(sol[0] + ck2 * kk ** 2) == 0 and len(sol_neg) == 1
                and float(sol_neg[0].subs(kk, 1)) > 0,
                f"decoupled dT entry {eT}; sigma^2 = {sol}; with alpha_c -> -alpha_c: sigma^2 = {sp.N(sol_neg[0], 4)} > 0 (real sigma ~ k)")
RES["K5"] = dict(entry=str(eT), sigma2=str(sol), sigma2_negative_alpha=str(sol_neg))


# K7: leaf-gradient (local) form of the constraint vs the lambda form, F2 with gravity
def system_grad_F2():
    B = build(True, frame="leaf", op="intrinsic", sub=True, chibar=False)
    F = dict(B["F"]); mu_ = sp.Function("mu")(t, x); nu = sp.Function("nu")(t, x)
    L2 = lagrangian(B, a ** 3 * nu * B["KT"][1]).subs(F["dlam"], 0).doit()
    L2 = ex(L2 + a ** 3 * mu_ * sp.diff(B["C"][1], x))
    fl = [F["xi"], F["eta"], F["dchi"], mu_, F["dT"], nu, F["Phi"]]
    return modes(L2, fl)


Mg = system_grad_F2()
Ml = system("F2", grav=True)["M"]
ratio7 = sp.simplify(Mg.det(method="berkowitz") / Ml.det(method="berkowitz"))
KOK["K7"] = chk("K7_leaf_gradient_form_equivalent", (not ratio7.has(sig)) and ratio7 != 0,
                f"det(leaf-gradient form)/det(lambda form) = {ratio7} (sigma-free, nonzero)")
RES["K7"] = dict(det_ratio=str(ratio7))
guard("K7")

# ======================================================================================================================
# S-THEOREMS
# ======================================================================================================================
P("\n==================== S THEOREMS ====================")
# S2/S4: D_i f(T) = h_i^mu d_mu f(T) vanishes; d_mu f(T) does not
Bs4 = build(True, frame="leaf", op="intrinsic", sub=True, chibar=True)
fT = E(chib, sp.diff(chib, t) * Bs4["F"]["dT"])
hm = [[add(E(1) if m == n else list(ZERO), mul(Bs4["ndn_T"][m], Bs4["nup_T"][n])) for n in range(4)] for m in range(4)]
Dif = []
for m in range(4):
    s_ = list(ZERO)
    for n in range(4):
        s_ = add(s_, mul(hm[m][n], dE(fT, XX[n])))
    Dif.append([sp.simplify(c_) for c_ in s_[:2]])
leafgrad_zero = all(c_ == 0 for row in Dif for c_ in row)
fourgrad = [sp.simplify(dE(fT, XX[m])[0]) for m in range(4)]
P(f"  S4: leaf gradient D_mu f(T) to O(eps): {Dif} (all zero: {leafgrad_zero}); 4-gradient d_mu f(T) at O(1): {fourgrad}")
P("      => a leaf-gradient condition D_i(Lap chi - K_m n_Sigma) = 0 admits an integration 'constant' c(T) on each leaf;")
P("         a 4-gradient condition d_mu(...) = 0 admits only a spacetime constant (as HT's Lambda_0).")
RES["S4"] = dict(leaf_gradient_of_fT=str(Dif), four_gradient_of_fT=str(fourgrad), leafgrad_zero=leafgrad_zero)

# S5: AS206 conformal specialisation in 3D (independent check)
s3x, s3y, s3z = sp.symbols("X Y Z", real=True)
sg = sp.Function("s")(s3x, s3y, s3z); uu3 = sp.Function("w")(s3x, s3y, s3z); epc = sp.Symbol("e")
lap_conf = lap_beltrami([s3x, s3y, s3z], [sp.exp(2 * epc * sg)] * 3, uu3)
dlap = sp.simplify(sp.diff(lap_conf, epc).subs(epc, 0))
target = -2 * sg * (sp.diff(uu3, s3x, 2) + sp.diff(uu3, s3y, 2) + sp.diff(uu3, s3z, 2)) + sum(
    sp.diff(sg, v_) * sp.diff(uu3, v_) for v_ in (s3x, s3y, s3z))
s5ok = sp.simplify(dlap - target) == 0
P(f"  S5 (AS206 conformal case, 3D): delta Lap = -2 s Lap + grad s . grad: residual {sp.simplify(dlap - target)} -> {s5ok}")
RES["S5"] = dict(as206_conformal_ok=s5ok)

# S3: no subtraction on an infinite FRW leaf -> u = K rho r/3 reaches the wall u = a0 at r_wall = 3 a0/(K rho_c)
Krho0 = 4 * math.pi * G_SI * OMC * 3 * H0 ** 2 / (8 * math.pi * G_SI)   # = 1.5 Omega_c H0^2
RW = {f_: 3 * A0[f_] / Krho0 for f_ in FOOTS}
P(f"  S3: K rho_c0 = 1.5 Omega_c H0^2 = {Krho0:.4e} s^-2; without subtraction u = K rho_c r/3 from an arbitrary centre reaches")
P(f"      the W_full wall at r_wall = 3 a0/(K rho_c0): canonical {RW['canonical'] / MPC / 1e3:.3f} Gpc, alt {RW['alt'] / MPC / 1e3:.3f} Gpc")
RES["S3"] = dict(Krho_c0=Krho0, r_wall_Gpc={f_: RW[f_] / MPC / 1e3 for f_ in FOOTS})
guard("S")

# ======================================================================================================================
# CANDIDATE LINEAR SYSTEMS: G-INT, G-NBAR, G-HAD (+K1, K4), G-NOGHOST, G-T
# ======================================================================================================================
CIDS = ["C938", "P1", "F0", "F1", "F1p", "F2", "F3_lo", "F3_hi", "F3b_hi", "F3b_lo"]
SYS = {}; POLY = {}


def get_sys(base, grav, variant="main"):
    key = (base, grav, variant)
    if key not in SYS:
        S_ = system(base, grav, variant)
        det, cs = char_poly(S_["M"])
        S_["det"] = det; S_["cs"] = cs
        SYS[key] = S_
        guard(f"sys {key}")
    return SYS[key]


GATES = {c_: {} for c_ in CIDS}
HADR = {}
if not MUT:
    P("\n==================== CANDIDATES ON FRW (frozen-coefficient WKB; units |H| = 1, c = 1) ====================")
    for cid in CIDS:
        base = base_cid(cid)
        for grav in (True, False):
            S_ = get_sys(base, grav)
            if cid == base or cid in ("F3_lo", "F3b_hi"):
                if grav:
                    P(f"\n  {cid}{' (' + base + ')' if base != cid else ''}: fields {S_['names']}")
                    for i in range(len(S_["names"])):
                        P(f"    EL[{S_['names'][i]:4s}]: {[str(sp.factor(S_['M'][i, j])) for j in range(len(S_['names']))]}")
                    P(f"    sigma-polynomial degree {len(S_['cs']) - 1}")
        # G-INT (gravity on and off)
        gi_ = {}
        for grav in (True, False):
            S_ = get_sys(base, grav)
            gi_[grav] = rows_have_sigma(S_["M"], S_["names"])
        g_int = not any(v_ for d_ in gi_.values() for v_ in d_.values())
        GATES[cid]["G-INT"] = g_int
        # G-HAD
        labs = {}
        for grav in (True, False):
            S_ = get_sys(base, grav)
            for bg in BGS:
                par = dict(bg); par.update(kh_par(cid))
                mx = hadamard(S_["cs"], par, KS, dps=80)
                lab, slope = had_label(mx, KS)
                HADR[f"{cid}|{'grav' if grav else 'nograv'}|{bg['tag']}"] = dict(maxRe=mx, slope=slope, label=lab)
                labs[(grav, bg["tag"])] = lab
            guard(f"had {cid} {grav}")
        lab_on = set(v_ for (g_, _), v_ in labs.items() if g_); lab_off = set(v_ for (g_, _), v_ in labs.items() if not g_)
        if lab_on == {"WELL-POSED"} and lab_off == {"WELL-POSED"}:
            had = "WELL-POSED"
        elif "ILL-POSED" in lab_on and "ILL-POSED" in lab_off:
            had = "ILL-POSED"
        else:
            had = "UNRESOLVED"
        GATES[cid]["G-HAD"] = had
        GATES[cid]["K4_grav_agree"] = (lab_on == lab_off)
        top = {tg: HADR[f"{cid}|grav|{tg}"]["maxRe"][-1] for tg in [b_["tag"] for b_ in BGS]}
        P(f"  {cid:7s}: G-INT {'PASS' if g_int else 'FAIL'} (sigma in chi/lambda rows: {gi_[True]}); G-HAD {had} "
          f"(grav-on labels {sorted(lab_on)}, grav-off {sorted(lab_off)}); max Re sigma/|H| at k = 1e10: "
          f"{min(top.values()):.3e} .. {max(top.values()):.3e}")
        # G-NOGHOST
        S_ = get_sys(base, True)
        par0 = dict(BGS[0]); par0.update(kh_par(cid))
        ok1, ev1 = kinetic_check(S_["M"], S_["names"], par0, 1e4)
        ok2, ev2 = kinetic_check(S_["M"], S_["names"], par0, 1e10)
        GATES[cid]["G-NOGHOST"] = ok1 and ok2
        GATES[cid]["kinetic_eigs"] = dict(k1e4=ev1, k1e10=ev2)
        P(f"           G-NOGHOST {'PASS' if ok1 and ok2 else 'FAIL'}: kinetic Hessian eigenvalues (z=0, 24 pc, H>0) "
          f"k=1e4 {['%.3e' % v_ for v_ in ev1]}; k=1e10 {['%.3e' % v_ for v_ in ev2]}")
    RES["hadamard"] = HADR

    # ---- K1: CFG938 reproduced (WT-02)
    S_ = get_sys("C938", True)
    nm = S_["names"]; Mc_ = S_["M"]
    chi_row = sp.expand(Mc_[nm.index("dlam"), nm.index("dchi")])
    lam_row = sp.expand(Mc_[nm.index("dchi"), nm.index("dlam")])
    fwd = sp.simplify(chi_row - (-kk ** 2 - 3 * h * sig)) == 0
    bwd = sp.simplify(lam_row.coeff(sig) - 3 * h) == 0 and sp.simplify(lam_row.coeff(kk, 2) + 1) == 0
    ratios = []; slopes = []
    for grav in (True, False):
        for bg in BGS:
            r_ = HADR[f"C938|{'grav' if grav else 'nograv'}|{bg['tag']}"]
            ratios.append(r_["maxRe"][-1] / (KS[-1] ** 2 / 3)); slopes.append(r_["slope"])
    sing = any(sp.denom(sp.together(c_)).has(h) for c_ in S_["cs"]) or any(sp.denom(sp.together(e_)).has(h) for e_ in Mc_)
    KOK["K1"] = chk("K1_CFG938_reproduced", fwd and bwd and all(abs(r_ - 1) <= 0.01 for r_ in ratios)
                    and all(abs(s_ - 2) <= 0.02 for s_ in slopes) and GATES["C938"]["G-HAD"] == "ILL-POSED" and sing,
                    f"chi row {chi_row} (forward-parabolic for H>0), lambda row {lam_row} (backward); max Re sigma/(k^2/3|H|) "
                    f"at k=1e10: {min(ratios):.6f} .. {max(ratios):.6f}; slope {min(slopes):.4f} .. {max(slopes):.4f}; "
                    f"G-HAD {GATES['C938']['G-HAD']}; 1/H in coefficients (no H = 0 background): {sing}")
    RES["K1"] = dict(chi_row=str(chi_row), lam_row=str(lam_row), ratio_range=[min(ratios), max(ratios)],
                     slope_range=[min(slopes), max(slopes)], singular_at_H0=sing)
    KOK["K4"] = chk("K4_gravity_on_off_agree", all(GATES[c_]["K4_grav_agree"] for c_ in CIDS),
                    str({c_: GATES[c_]["K4_grav_agree"] for c_ in CIDS}))

    # ---- G-NBAR: background constraint at O(eps^0) with chibar leaf-constant (intrinsic) or chibar(t) (C938/P1)
    Bn = build(True, frame="leaf", op="intrinsic", sub=True, chibar=False)
    C0_int = sp.simplify(Bn["C"][0])
    Bc = build(True, frame="medium", op="projected", sub=False, chibar=True)
    C0_938 = sp.simplify(Bc["C"][0].subs(sp.Derivative(chib, t), -Km / (3 * a ** 2 * sp.diff(a, t))))
    P(f"\n  G-NBAR: intrinsic + subtraction, chibar = const: background constraint = {C0_int}; "
      f"CFG938 with chibar' = -K_m/(3 a^2 a'): {C0_938} (needs 1/H: no background at H = 0)")
    for cid in CIDS:
        if cid in ("C938", "P1"):
            GATES[cid]["G-NBAR"] = False                                  # absorbed by chibar(t), not a leaf subtraction
        else:
            GATES[cid]["G-NBAR"] = (C0_int == 0) and KOK["K6"]
    RES["G_NBAR"] = dict(intrinsic_background=str(C0_int), cfg938_background=str(C0_938))

    # ---- G-T: force on a non-varied foliation (F0)
    B0 = build(True, frame="leaf", op="intrinsic", sub=True, chibar=False)
    L0 = lagrangian(B0)
    F0f = B0["F"]
    ET = sp.euler_equations(L0, [F0f["dT"]], [t, x])[0].lhs
    ET = ex(at0(ET.subs(F0f["dT"], 0).doit()))
    P(f"  G-T: Euler-Lagrange expression of the leaf position in F0 (not varied there): E_T = {ET}")
    P("       => for a prior-geometry foliation, nabla_mu T^{mu 0} = -E_T != 0 wherever H dlam != 0 (energy-momentum not conserved);")
    P("          F1/F1'/F2/F3/F3b vary dT (lock, CMC multiplier or khronon), C938/P1 have no separate foliation: structural PASS.")
    for cid in CIDS:
        GATES[cid]["G-T"] = (cid != "F0")
    RES["G_T"] = dict(E_T_F0=str(ET))
