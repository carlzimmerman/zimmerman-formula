#!/usr/bin/env python3
"""SNP1 snowplow clearing (criteria 9ff5f59a72). TEST lane, quarantined; adopts nothing.
kappa = 1/2 FITTED; not theory closed. One thread. Usage: python3 snp1.py [--mutate] [--ebr-every-other]

Can the law's own wall pressure (SWT1 T3) clear the cold component from around galaxies, dynamically?
  Part A  statics of a wall-supported shell (numbers beside the Lean statements in SNP1.lean)
  Part B  thin-shell dynamics in the record's expanding background:
          graded  sticky (momentum-conserving) snowplow
          bracket energy-conserving front with free collisionless layers (wall force on the innermost cold)
Constants, background, the shell solver, the law, the GSMF and the statistic `compensated` are imported from
../SWT1_switch_theorems/swt1.py (its library part, as swt1_extra.py does it).
"""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
if not hasattr(np, 'trapz'): np.trapz = np.trapezoid

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SWT1 = os.path.join(HERE, "..", "SWT1_switch_theorems")
MUT = "--mutate" in sys.argv
EBR_EVERY_OTHER = "--ebr-every-other" in sys.argv
TAG = "snp1_MUTATE" if MUT else "snp1"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()

src = open(os.path.join(SWT1, "swt1.py")).read(); cut = src.index("RES = dict(lane=")
NS = {"__file__": os.path.abspath(os.path.join(SWT1, "swt1.py")), "__name__": "swt1_lib"}
_argv = sys.argv; sys.argv = ["swt1.py"]; exec(compile(src[:cut], "swt1.py", "exec"), NS); sys.argv = _argv
G, MS, PC, MPC, KPC, A0, LINE = (NS[k] for k in ("G", "MS", "PC", "MPC", "KPC", "A0", "LINE"))
u_in, Wfun, p_wall, Rms, r_ta, shell = (NS[k] for k in ("u_in", "Wfun", "p_wall", "Rms", "r_ta", "shell"))
OB, OD, h, Om, Orr, OL, RHOC, RHO_M0, RHO_D0, R_DUST, Hs, AI = (NS[k] for k in
    ("OB", "OD", "h", "Om", "Orr", "OL", "RHOC", "RHO_M0", "RHO_D0", "R_DUST", "Hs", "AI"))
LG, compensated, radii_table = NS["LG"], NS["compensated"], NS["radii_table"]
RHO_B0 = OB / h ** 2 * RHOC
RHO_L = OL * RHOC
def rho_r(a): return Orr * RHOC / a ** 4

GK = 1.38e-15                                   # KiDS's lowest tabulated g_bar (m/s^2)
BINS = (9.4, 10.45, 10.7, 10.9)
ZNS = (6.0, 3.0, 1.5)
ZOUT = (2.0, 1.0, 0.5, 0.0)
R200 = 200 * KPC
F2LINE = 0.9
GAL1_ALLOW = 0.0197

RES = dict(lane="SNP1", criteria="9ff5f59a72", tag=TAG, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           partA={}, KA={}, runs={}, gates={}, labels={}, reported={}, MUTATE={})

# ====================================================================== the law at the wall
def Fw(R, Mb, a0):
    """outward force on the carrier at a spherical wall of radius R: 4 pi R^2 p_wall = a0 M_b W(u) / y."""
    y = G * Mb / (R * R * a0)
    return a0 * Mb * float(Wfun(u_in(y))) / y
def gabs(r, a, Mpt, Mc):
    """radial gravity in the record's background: point mass, uniform IGM baryons, cold mass Mc inside r, Lambda, radiation."""
    return -G * (Mpt + 4 * math.pi / 3 * RHO_B0 / a ** 3 * r ** 3 + Mc) / r ** 2 + 8 * math.pi * G / 3 * (RHO_L - rho_r(a)) * r
def Psi(u): return float(Wfun(u)) * (1 + u) ** 2 / u ** 4
def Phi(u): return float(Wfun(u)) * (1 + u) / u ** 2
def u_eq(k): return math.exp(brentq(lambda lu: Psi(math.exp(lu)) - k, math.log(1e-9), math.log(1e9), xtol=1e-14, rtol=1e-14))
def RK(Mb): return math.sqrt(G * Mb / GK)

class Bound:
    """bound region at nucleation: share X R M_b as SWT1 placed it (singular isothermal to R_h,n) plus the mean at a_n; static."""
    def __init__(s, Mb, X, Rh, an):
        s.Mb, s.X, s.Rh = Mb, X, Rh; s.rn = RHO_D0 / an ** 3; s.Ms = X * R_DUST * Mb
    def rho(s, r): return s.Ms / (4 * math.pi * s.Rh * r * r) + s.rn
    def M(s, r):
        rr = np.minimum(r, s.Rh); return s.Ms * rr / s.Rh + 4 * math.pi / 3 * s.rn * rr ** 3
    def p(s, r): return s.rho(r) * G * (s.Mb + float(s.M(r))) / (2 * r)

def piston(p_drive, p_ext, rho_e, v_e):
    """elastic front: speed, mass flux per unit area, ejecta speed (reflection in the front's frame)."""
    Vf = v_e + math.sqrt(max(p_drive - p_ext, 0.0) / (2 * rho_e))
    return Vf, rho_e * (Vf - v_e), 2 * Vf - v_e
def sweep(R, V, M, F, rho_e, v_e, p_e):
    """sticky thin-shell step (time derivatives): F the non-contact force on the shell."""
    Md = 4 * math.pi * R * R * rho_e * max(V - v_e, 0.0)
    return V, F - 4 * math.pi * R * R * p_e + Md * v_e, Md          # dR/dt, d(MV)/dt, dM/dt

# ====================================================================== the record's flow for the unbound background
SG0 = math.log(1 / 7.0) - 0.02; NSG = 1401
SGRID = np.linspace(SG0, 0.0, NSG); DSG = SGRID[1] - SGRID[0]
XLAB = np.logspace(math.log10(0.02 * MPC), math.log10(60 * MPC), 160)
RFLOW = 1.0 * KPC
class Flow:
    def __init__(self, dM):
        Rt = np.full((NSG, XLAB.size), np.nan); Vt = np.full((NSG, XLAB.size), np.nan)
        for j, xL in enumerate(XLAB):
            r0 = xL * AI; v0 = Hs(AI) * r0
            def rhs(s, y):
                a = math.exp(s); H = Hs(a)
                acc = -(4 * math.pi * G / 3) * (RHO_M0 / a ** 3 + 2 * Orr * RHOC / a ** 4 - 2 * OL * RHOC) * y[0] - G * dM / y[0] ** 2
                return [y[1] / H, acc / H]
            def ev(s, y): return y[0] - RFLOW
            ev.terminal, ev.direction = True, -1
            so = solve_ivp(rhs, (math.log(AI), 0.0), [r0, v0], method="DOP853", rtol=1e-9, atol=[r0 * 1e-12, 1e-6],
                           t_eval=SGRID, events=ev)
            tt_ = np.asarray(so.t); n = tt_.size
            if n: Rt[:n, j] = np.asarray(so.y)[0]; Vt[:n, j] = np.asarray(so.y)[1]
        self.rows = []
        for i in range(NSG):
            mk = np.isfinite(Rt[i]); rr, vv = Rt[i, mk], Vt[i, mk]; o = np.argsort(rr)
            self.rows.append((rr[o], vv[o]))
    def v(self, r, s):
        x = (s - SG0) / DSG; i = int(min(max(math.floor(x), 0), NSG - 2)); w = min(max(x - i, 0.0), 1.0); out = 0.0
        for k, wt in ((i, 1 - w), (i + 1, w)):
            rr, vv = self.rows[k]
            if rr.size == 0 or r >= rr[-1]: val = Hs(math.exp(SGRID[k])) * r
            elif r <= rr[0]: val = vv[0]
            else: val = float(np.interp(r, rr, vv))
            out += wt * val
        return out
_FLOW = {}
def flow_for(Mb, X):
    key = (round(math.log10(Mb / MS), 6), X)
    if key not in _FLOW: _FLOW[key] = Flow(Mb * (1 + X * R_DUST))
    return _FLOW[key]
_RH = {}
def Rh_n(Mb, zn):
    key = (round(math.log10(Mb / MS), 6), zn)
    if key not in _RH: _RH[key] = Rms("NC", Mb, 0.0, 1 / (1 + zn))
    return _RH[key]

# ====================================================================== graded: sticky snowplow
def sticky(Mb, a0, X, zn, fmult=1.0, R0fac=1.0, pB_on=True):
    an = 1 / (1 + zn); sn = math.log(an)
    rM = math.sqrt(G * Mb / a0); R0 = R0fac * rM; rfl = 0.1 * rM
    Rh = Rh_n(Mb, zn); flow = flow_for(Mb, X); B = Bound(Mb, X, Rh, an)
    def FW(R): return fmult * Fw(R, Mb, a0)
    def pB(R): return B.p(R) if pB_on else 0.0
    def unpack(y): return y[0] * KPC, y[1] * Mb * 1e3, y[2] * Mb
    def force(R, M, s): return FW(R) + M * gabs(R, math.exp(s), Mb, M / 2)
    def deriv(s, y, st):
        R, Pm, M = unpack(y); a = math.exp(s); H = Hs(a); V = Pm / M; F = force(R, M, s)
        if st == "B": dR, dP, dM = sweep(R, V, M, F, B.rho(R), 0.0, pB(R))
        elif st == "U": dR, dP, dM = sweep(R, V, M, F, RHO_D0 / a ** 3, flow.v(R, s), 0.0)
        else: dR, dP, dM = V, F, 0.0
        return [dR / H / KPC, dP / H / (Mb * 1e3), dM / H / Mb]
    st = "B" if R0 < Rh else "U"
    M0 = float(B.M(R0)) if st == "B" else 4 * math.pi / 3 * RHO_D0 / an ** 3 * R0 ** 3
    y = np.array([R0 / KPC, 0.0, M0 / Mb]); s = sn; RmaxB = R0 if st == "B" else Rh
    segs = []; fl = dict(broke_out_z=None, stalls=0, collapsed_z=None, nseg=0, chatter=False, Rh_kpc=Rh / KPC, rM_kpc=rM / KPC)
    while s < -1e-12:
        fl["nseg"] += 1
        if fl["nseg"] > 6000: fl["chatter"] = True; break
        if st == "B" and y[1] <= 0.0:
            R, Pm, M = unpack(y); f2 = force(R, M, s); f1 = f2 - 4 * math.pi * R * R * pB(R)
            if f1 > 0: y[1] = 0.0
            elif f2 >= 0: st = "S"; fl["stalls"] += 1
            else: st = "D"; RmaxB = R; y[1] = min(y[1], 0.0)
        if st == "S":
            R, Pm, M = unpack(y)
            ss = np.linspace(s + 1e-7, 0.0, 600)
            f2s = np.array([force(R, M, x) for x in ss]); f1s = f2s - 4 * math.pi * R * R * pB(R)
            i1 = np.argmax(f1s > 0) if np.any(f1s > 0) else None; i2 = np.argmax(f2s < 0) if np.any(f2s < 0) else None
            if i1 is None and i2 is None:
                segs.append((s, 0.0, "const", y.copy(), st)); s = 0.0; break
            if i2 is None or (i1 is not None and i1 <= i2):
                s1 = ss[i1] if i1 == 0 else brentq(lambda x: force(R, M, x) - 4 * math.pi * R * R * pB(R), ss[i1 - 1], ss[i1]) + 1e-9
                segs.append((s, s1, "const", y.copy(), st)); s = s1; st = "B"; y[1] = 0.0
            else:
                s1 = ss[i2] if i2 == 0 else brentq(lambda x: force(R, M, x), ss[i2 - 1], ss[i2]) + 1e-9
                segs.append((s, s1, "const", y.copy(), st)); s = s1; st = "D"; RmaxB = R
            continue
        evs = []
        if st == "B":
            e1 = lambda s_, y_: y_[1]; e1.terminal, e1.direction = True, -1
            e2 = lambda s_, y_: y_[0] - Rh / KPC; e2.terminal, e2.direction = True, 1
            evs = [e1, e2]
        elif st == "D":
            Rfront = RmaxB if RmaxB < Rh else Rh
            e1 = lambda s_, y_: y_[0] - Rfront / KPC; e1.terminal, e1.direction = True, 1
            e2 = lambda s_, y_: y_[0] - rfl / KPC; e2.terminal, e2.direction = True, -1
            evs = [e1, e2]
        else:
            e1 = lambda s_, y_: y_[0] - Rh / KPC; e1.terminal, e1.direction = True, -1
            evs = [e1]
        so = solve_ivp(lambda s_, y_: deriv(s_, y_, st), (s, 0.0), y, method="LSODA", rtol=1e-8, atol=[1e-9, 1e-9, 1e-12],
                       events=evs, dense_output=True, max_step=0.02)
        segs.append((s, so.t[-1], "sol", so.sol, st)); y = so.y[:, -1].copy(); s = so.t[-1]
        if so.status != 1: break
        fired = [k for k, te in enumerate(so.t_events) if te.size]
        k = fired[0]
        if st == "B":
            if k == 0: y[1] = 0.0
            else: st = "U"; RmaxB = Rh; fl["broke_out_z"] = float(1 / math.exp(s) - 1)
        elif st == "D":
            if k == 0: st = "B" if RmaxB < Rh else "U"; y[1] = max(y[1], 1e-12)
            else: fl["collapsed_z"] = float(1 / math.exp(s) - 1); break
        else:
            st = "D"; RmaxB = Rh
    out = {}
    for z in ZOUT:
        so_ = math.log(1 / (1 + z))
        if so_ < sn - 1e-12: out[str(z)] = dict(R_w_kpc=0.0, nucleated=False); continue
        if fl["collapsed_z"] is not None and z <= fl["collapsed_z"]: out[str(z)] = dict(R_w_kpc=0.0, collapsed=True); continue
        yy = None
        for (a_, b_, kind, data, st_) in segs:
            if a_ - 1e-12 <= so_ <= b_ + 1e-12:
                yy = data if kind == "const" else data(min(max(so_, a_), b_)); stz = st_
        if yy is None: yy = y; stz = st
        R_, Pm_, M_ = unpack(yy)
        out[str(z)] = dict(R_w_kpc=R_ / KPC, V_kms=Pm_ / M_ / 1e3, M_s_over_Mb=M_ / Mb, state=stz)
    # cold inside 200 kpc at z 0
    Rf, Pf, Mf = unpack(y); coll = fl["collapsed_z"] is not None
    if st in ("B", "S") and not coll: RmaxB = max(RmaxB, Rf)          # the swept front is the shell itself
    c200 = 0.0
    if coll or Rf < R200: c200 += Mf
    if RmaxB < Rh and RmaxB < R200: c200 += float(B.M(min(R200, Rh)) - B.M(RmaxB))
    Rcl = Rf if (st == "U" and not coll) else Rh
    if R200 > Rcl: c200 += 4 * math.pi / 3 * RHO_D0 * (R200 ** 3 - Rcl ** 3)
    return dict(out=out, cold200_over_Mb=c200 / Mb, final_state=("collapsed" if coll else st), RmaxB_kpc=RmaxB / KPC, flags=fl,
                R_w0_kpc=(0.0 if coll else Rf / KPC), M_s0_over_Mb=Mf / Mb)

# ====================================================================== bracket: energy-conserving front + free layers
def ebracket(Mb, a0, X, zn, fmult=1.0, test=None):
    """test = dict(p=Pa, rho=kg/m3, R0=m, T=s): no gravity, no expansion, constant drive on a static uniform medium (KA-5)."""
    if test is None:
        an = 1 / (1 + zn); sn = math.log(an)
        rM = math.sqrt(G * Mb / a0); R0 = rM; rfl = 0.1 * rM
        Rh = Rh_n(Mb, zn); flow = flow_for(Mb, X); B = Bound(Mb, X, Rh, an)
        def pdrive(R): return fmult * float(p_wall(G * Mb / (R * R * a0), a0))
        def Fdrive(R): return fmult * Fw(R, Mb, a0)
    else:
        R0 = test["R0"]; rfl = 0.0; Rh = 1e40; sn = 0.0; B = None
        def pdrive(R): return test["p"]
        def Fdrive(R): return 4 * math.pi * R * R * test["p"]
    region = "B" if R0 < Rh else "U"; Rf = R0
    m0 = (float(B.M(R0)) if B is not None else 0.0)
    r = np.array([R0]) if m0 > 0 else np.zeros(0); v = np.zeros(r.size); m = np.array([m0]) if m0 > 0 else np.zeros(0)
    Mc0 = 0.0; mp = 0.0; pp = 0.0; ej = 0.0; work = 0.0; s = sn; tt = 0.0; collapsed = None; nstep = 0
    def ext(R, s_):
        if test is not None: return test["rho"], 0.0, 0.0
        if region == "B": return B.rho(R), 0.0, B.p(R)
        a = math.exp(s_); return RHO_D0 / a ** 3, flow.v(R, s_), 0.0
    def accel(r, m, s_):
        if r.size == 0: return np.zeros(0), False, -1
        o = np.argsort(r); rs, ms = r[o], m[o]
        i0 = int(o[0]); inner = r[i0] < Rf
        if test is not None:
            acc = np.zeros(r.size)
        else:
            a = math.exp(s_); Mc = Mc0 + np.cumsum(ms) - 0.5 * ms
            if region == "B":
                Mc = Mc + np.where(rs > Rf, B.M(rs) - float(B.M(Rf)), 0.0); Ru = Rh
            else: Ru = Rf
            Mc = Mc + np.where(rs > Ru, 4 * math.pi / 3 * RHO_D0 / a ** 3 * (rs ** 3 - Ru ** 3), 0.0)
            accs = -G * (Mb + 4 * math.pi / 3 * RHO_B0 / a ** 3 * rs ** 3 + Mc) / rs ** 2 + 8 * math.pi * G / 3 * (RHO_L - rho_r(a)) * rs
            acc = np.empty(r.size); acc[o] = accs
        if inner: acc[i0] += Fdrive(r[i0]) / m[i0]
        return acc, inner, i0
    acc, inner, i0 = accel(r, m, s)
    outs = sorted([math.log(1 / (1 + z)) for z in ZOUT if math.log(1 / (1 + z)) >= sn - 1e-12]) if test is None else []
    win = {so_: dict(w=0.0, Rw=0.0, c200=0.0) for so_ in outs}
    send = 0.0 if test is None else None
    while True:
        if test is None and s >= -1e-12: break
        if test is not None and tt >= test["T"]: break
        nstep += 1
        if nstep > 2_000_000: break
        H = Hs(math.exp(s)) if test is None else 0.0
        # front speed (predictor at R_f, corrector at the midpoint)
        def front_speed(R):
            rho_e, v_e, p_e = ext(R, s)
            if inner: return (0.0 if region == "B" else v_e), 0.0, 0.0, v_e
            Vf, flux, vej = piston(pdrive(R), p_e, rho_e, v_e); return Vf, flux, vej, v_e
        Vf1 = front_speed(Rf)[0]
        dt = 0.002 / H if test is None else test["T"] / 4000.0
        if Vf1 != 0.0: dt = min(dt, 0.02 * Rf / abs(Vf1))
        if r.size:
            dt = min(dt, float(np.min(0.02 * r / np.maximum(np.abs(v), 1e3))),
                     float(np.min(0.1 * np.sqrt(r / np.maximum(np.abs(acc), 1e-30)))))
        if test is None:
            nxt = min([x for x in outs if x > s + 1e-12] + [0.0])
            if s + H * dt > nxt: dt = (nxt - s) / H
        else:
            dt = min(dt, test["T"] - tt)
        Rm = Rf + 0.5 * dt * Vf1
        Vf, flux, vej, v_e = front_speed(Rm)
        v = v + 0.5 * dt * acc
        r = r + dt * v
        dm = 4 * math.pi * Rm * Rm * flux * dt
        if dm > 0:
            mp += dm; pp += dm * vej; ej += dm; work += pdrive(Rm) * 4 * math.pi * Rm * Rm * (Vf - v_e) * dt
        Rf = Rf + dt * Vf
        if region == "B" and Rf >= Rh: region = "U"
        s = s + H * dt if test is None else s; tt += dt
        if r.size and rfl > 0:
            keep = r >= rfl
            if not np.all(keep): Mc0 += float(m[~keep].sum()); r, v, m = r[keep], v[keep], m[keep]
        if test is None and region == "U" and Rf < rfl:
            collapsed = float(1 / math.exp(s) - 1)
            c_coll = Mc0 + float(m[r < R200].sum()) + mp + 4 * math.pi / 3 * RHO_D0 / math.exp(s) ** 3 * R200 ** 3
            break
        acc, inner, i0 = accel(r, m, s)
        v = v + 0.5 * dt * acc
        if mp > 0 and mp >= max(0.02 * (Mb if test is None else test["mref"]), 0.03 * ej):
            r = np.append(r, Rf); v = np.append(v, pp / mp); m = np.append(m, mp); mp = pp = 0.0
            acc, inner, i0 = accel(r, m, s)
        if test is None:
            Rw = min(Rf, float(r.min())) if r.size else Rf
            for so_ in outs:
                if so_ - 0.05 - 1e-12 <= s <= so_ + 1e-12:
                    a = math.exp(s); c = Mc0 + float(m[r < R200].sum()) + (mp if Rf < R200 else 0.0)
                    if region == "B" and Rf < R200: c += float(B.M(min(R200, Rh)) - B.M(Rf))
                    Ru = Rh if region == "B" else Rf
                    if R200 > Ru: c += 4 * math.pi / 3 * RHO_D0 / a ** 3 * (R200 ** 3 - Ru ** 3)
                    win[so_]["w"] += H * dt; win[so_]["Rw"] += H * dt * Rw; win[so_]["c200"] += H * dt * c
    if test is not None:
        KE = 0.5 * float(np.sum(m * v * v)) + (0.5 * pp * pp / mp if mp > 0 else 0.0)
        return dict(Rf=Rf, Vf_last=Vf, v_layers=v, m=m, KE=KE, work=work, work_exact=test["p"] * 4 * math.pi / 3 * (Rf ** 3 - R0 ** 3),
                    ej=ej, nstep=nstep)
    out = {}
    for z in ZOUT:
        so_ = math.log(1 / (1 + z))
        if so_ < sn - 1e-12: out[str(z)] = dict(R_w_kpc=0.0, nucleated=False); continue
        if collapsed is not None and z <= collapsed: out[str(z)] = dict(R_w_kpc=0.0, collapsed=True); continue
        wv = win[so_]
        out[str(z)] = dict(R_w_kpc=(wv["Rw"] / wv["w"] / KPC if wv["w"] > 0 else Rf / KPC))
    c0 = win[0.0]["c200"] / win[0.0]["w"] if (0.0 in win and win[0.0]["w"] > 0) else float("nan")
    if collapsed is not None: c0 = c_coll
    return dict(out=out, cold200_over_Mb=c0 / Mb, R_w0_kpc=out["0.0"]["R_w_kpc"], front_kpc=Rf / KPC, region=region,
                n_layers=int(r.size), central_over_Mb=Mc0 / Mb, nstep=nstep, collapsed_z=collapsed,
                ejected_over_Mb=ej / Mb, work_over_Mb_c2=work / (Mb * 9e16))

# ====================================================================== KiDS points and gates
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
KIDS = []
for i, lm in enumerate(BINS, 1):
    a_ = np.loadtxt(os.path.join(DATA, f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")
    gbar = a_[:, 0]; gobs = 4 * 4.52e-30 * a_[:, 1] / a_[:, 4] * PC          # as swt1_extra.py loads them
    for gb, go in zip(gbar, gobs):
        if go > 0: KIDS.append(dict(lm=lm, gbar=float(gb), R=math.sqrt(G * 10 ** lm * MS / gb)))

def gate_eval(rows4, tab_runs, a0):
    """rows4: {lm: run}; tab_runs: {lm_grid: run} on LG. Returns gates dict."""
    g = {}
    c = {str(lm): rows4[lm]["cold200_over_Mb"] for lm in BINS}
    g["G_F2"] = dict(cold200_over_Mb=c, pass_=bool(all(x <= F2LINE for x in c.values())))
    rk = {str(lm): rows4[lm]["R_w0_kpc"] * KPC / RK(10 ** lm * MS) for lm in BINS}
    nout = {str(lm): int(sum(1 for p_ in KIDS if p_["lm"] == lm and p_["R"] > rows4[lm]["R_w0_kpc"] * KPC)) for lm in BINS}
    g["G_K"] = dict(Rw_over_RK=rk, R_w0_kpc={str(lm): rows4[lm]["R_w0_kpc"] for lm in BINS},
                    kids_points_outside=nout, kids_outside_total=int(sum(nout.values())), pass_=bool(all(x >= 1.0 for x in rk.values())))
    gl = {}
    for z in ZOUT:
        tab = np.array([max(tab_runs[lm]["out"][str(z)]["R_w_kpc"], 1.0) * KPC for lm in LG])
        d = compensated(tab, a0, z)
        gl[str(z)] = dict(f_V=d["f_V"], dilute=d["dilute"], q_C=d["q_C"], q_ff=d["q_ff"], q_tot=d["q_tot"],
                          pass_line=bool(d["q_tot"] <= LINE), under_GAL1_0197=bool(d["f_V"] <= GAL1_ALLOW),
                          R_Mpc_at_9_10p5_12=d["R_Mpc_at_9_10p5_12"])
    g["G_L"] = dict(by_z=gl, pass_=bool(gl["1.0"]["pass_line"]))
    g["all_pass"] = bool(g["G_F2"]["pass_"] and g["G_K"]["pass_"] and g["G_L"]["pass_"])
    g["failing"] = [k for k in ("G_F2", "G_K", "G_L") if not g[k]["pass_"]]
    return g

def interp_runs(runs_sub, lms_sub):
    """every-other E-bracket contingency: log R_w linear in log M (placeholder 1 kpc where no wall)."""
    full = {}
    for lm in LG:
        o = {}
        for z in ZOUT:
            xs = np.array(lms_sub); ys = np.array([math.log10(max(runs_sub[x]["out"][str(z)]["R_w_kpc"], 1.0)) for x in lms_sub])
            o[str(z)] = dict(R_w_kpc=10 ** float(np.interp(lm, xs, ys)))
        full[lm] = dict(out=o)
    return full

# ====================================================================== PART A numbers
P(f"SNP1 {'MUTATE ' if MUT else ''}run (criteria 9ff5f59a72). R = OD/OB = {R_DUST:.4f}; rho_d0 {RHO_D0:.4e} kg/m^3; "
  f"rho_b0 {RHO_B0:.4e}; line {LINE}; F2 line {F2LINE} M_b inside 200 kpc; g_K {GK:.2e}")
if not MUT:
    P("")
    P("PART A. Statics of a wall-supported shell.")
    kX = {X: (X * R_DUST) * (1 + X * R_DUST / 2) for X in (1, 3)}
    pa = {"k": kX, "rows": {}}
    for X in (1, 3):
        k = kX[X]; u = u_eq(k); req = math.sqrt(1 + u) / u
        pa["rows"][f"X{X}"] = dict(k=k, u_eq=u, Req_over_rM=req, closed_deep=1.5 * k, bracket=[math.sqrt(k * (k + 1)), math.sqrt(2 * k * (2 * k + 1))],
                                   inside_bracket=bool(math.sqrt(k * (k + 1)) < req < math.sqrt(2 * k * (2 * k + 1))))
        P(f"A.2 fixed-mass shell m = {X} R = {X * R_DUST:.3f} M_b, k = m (1 + m/2) = {k:.3f}: exact R_eq = {req:.3f} r_M; deep closed "
          f"form (3/2) k = {1.5 * k:.3f}; Lean bracket ({math.sqrt(k*(k+1)):.3f}, {math.sqrt(2*k*(2*k+1)):.3f}); unstable (A2c)")
    tabA = {}
    for f, a0 in A0.items():
        tabA[f] = {}
        for lm in BINS:
            Mb = 10 ** lm * MS; rM = math.sqrt(G * Mb / a0); vf = (G * Mb * a0) ** 0.25
            Req = {X: pa["rows"][f"X{X}"]["Req_over_rM"] * rM / KPC for X in (1, 3)}
            def bal(withIGM, rho_d=RHO_D0, rho_b=RHO_B0):
                def fn(lr):
                    R = math.exp(lr); Ms = 4 * math.pi / 3 * rho_d * R ** 3
                    Min = Mb + (4 * math.pi / 3 * rho_b * R ** 3 if withIGM else 0.0) + Ms / 2
                    return math.log(Fw(R, Mb, a0) / (G * Ms * Min / R ** 2))
                return math.exp(brentq(fn, math.log(1e-3 * KPC), math.log(1e3 * MPC)))
            Rb, Rbi = bal(False), bal(True)
            Rs = vf / math.sqrt(2 * math.pi * G * RHO_D0); Rl = (3 * Mb * vf ** 2 / (4 * math.pi ** 2 * G * RHO_D0 ** 2)) ** 0.2
            # stability check of the swept balance (numerical sign of net force on either side)
            def net(R): Ms = 4 * math.pi / 3 * RHO_D0 * R ** 3; return Fw(R, Mb, a0) - G * Ms * (Mb + Ms / 2) / R ** 2
            stable = bool(net(0.98 * Rb) > 0 and net(1.02 * Rb) < 0)
            tabA[f][str(lm)] = dict(r_M_kpc=rM / KPC, v_f_kms=vf / 1e3, R_eq_X1_kpc=Req[1], R_eq_X3_kpc=Req[3], swept_balance_Mpc=Rb / MPC,
                                    swept_balance_withIGM_Mpc=Rbi / MPC, deep_limit_small_Mpc=Rs / MPC, deep_limit_large_Mpc=Rl / MPC,
                                    R_K_Mpc=RK(Mb) / MPC, balance_over_RK=Rb / RK(Mb), balance_withIGM_over_RK=Rbi / RK(Mb), stable=stable)
            P(f"[{f}] log M_b {lm}: r_M {rM/KPC:.2f} kpc, v_f {vf/1e3:.1f} km/s; R_eq (share) {Req[1]:.0f} kpc, (3 x share) {Req[3]:.0f} kpc; "
              f"swept balance today {Rb/MPC:.3f} Mpc ({Rbi/MPC:.3f} with IGM baryons; deep limits {Rs/MPC:.2f} / {Rl/MPC:.3f}); "
              f"R_K {RK(Mb)/MPC:.3f} Mpc -> balance / R_K {Rb/RK(Mb):.3f} ({Rbi/RK(Mb):.3f}); stable {stable}")
    pa["table"] = tabA
    RES["partA"] = pa

# ====================================================================== KNOWN ANSWERS
if not MUT:
    P("")
    P("KNOWN ANSWERS")
    # KA-1
    Mb = 10 ** 10.45 * MS; worst = 0.0; worstq = 0.0
    for f, a0 in A0.items():
        rM = math.sqrt(G * Mb / a0)
        for x in np.logspace(-2, math.log10(30), 20):
            R = x * rM; a_ = Fw(R, Mb, a0); b_ = 4 * math.pi * R * R * float(p_wall(G * Mb / (R * R * a0), a0)); worst = max(worst, abs(a_ / b_ - 1))
        for yv in (1e-6, 1e-3, 0.1, 1.0, 10.0, 1e4):
            R = math.sqrt(G * Mb / (yv * a0))
            qv = quad(lambda t: math.sqrt(0.25 * t * t + t) - 0.5 * t, 0.0, yv, epsabs=0, epsrel=1e-13, limit=400)[0]
            worstq = max(worstq, abs(Fw(R, Mb, a0) / (a0 * Mb * qv / yv) - 1))
    ka1 = worst < 1e-12 and worstq < 1e-8
    RES["KA"]["KA_1"] = dict(max_rel_vs_swt1=worst, max_rel_vs_quadrature=worstq, pass_=bool(ka1))
    P(f"KA-1 F_w vs 4 pi R^2 swt1.p_wall: max rel {worst:.2e} (1e-12); vs quadrature: {worstq:.2e} (1e-8) -> {'PASS' if ka1 else 'FAIL'}")
    # KA-2
    def my_turn(dM, a_end):
        def classify(xL):
            r0 = xL * AI
            def rhs(s, y):
                a = math.exp(s); H = Hs(a)
                return [y[1] / H, gabs(y[0], a, dM, 4 * math.pi / 3 * RHO_D0 / a ** 3 * y[0] ** 3) / H]
            def turn(s, y): return y[1]
            turn.terminal, turn.direction = True, -1
            so = solve_ivp(rhs, (math.log(AI), math.log(a_end)), [r0, Hs(AI) * r0], method="LSODA", rtol=1e-11, atol=[r0 * 1e-13, 1e-7], events=turn)
            if so.t_events[0].size: return "early", so.y_events[0][0][0]
            return "late", so.y[0, -1]
        lo, hi = math.log(1e-6 * MPC), math.log(1e3 * MPC)
        for _ in range(80):
            mid = 0.5 * (lo + hi); kind, _r = classify(math.exp(mid))
            if kind == "early": lo = mid
            else: hi = mid
            if hi - lo < 1e-9: break
        return classify(math.exp(hi))[1]
    rows = []
    for lm in (9.4, 10.45, 10.9):
        dM = 10 ** lm * MS * (1 + R_DUST)
        for a_end in (1.0, 0.5):
            mine = my_turn(dM, a_end); rec = r_ta(dM, 0.0, a_end); rows.append(dict(lm=lm, a=a_end, mine_Mpc=mine / MPC, r_ta_Mpc=rec / MPC, rel=abs(mine / rec - 1)))
    ka2 = all(x["rel"] < 1e-4 for x in rows)
    RES["KA"]["KA_2"] = dict(rows=rows, pass_=bool(ka2))
    P("KA-2 my ln-a integrator (absolute gravity, wall off) vs swt1.r_ta: " + "; ".join(f"{x['lm']} a {x['a']}: {x['mine_Mpc']:.5f} vs {x['r_ta_Mpc']:.5f} ({x['rel']:.1e})" for x in rows)
      + f" -> {'PASS' if ka2 else 'FAIL'}")
    # KA-3
    rows = []; ok3 = True
    for k in (0.01, 0.1, 1.0, 10.0, 21.03, 155.9, 1e3):
        u = u_eq(k); req = math.sqrt(1 + u) / u; lo_, hi_ = math.sqrt(k * (k + 1)), math.sqrt(2 * k * (2 * k + 1))
        ins = lo_ < req < hi_; ok3 &= ins; rows.append(dict(k=k, Req_over_rM=req, lo=lo_, hi=hi_, inside=bool(ins)))
    k = 1e4; u = u_eq(k); req = math.sqrt(1 + u) / u; dev = abs(req / (1.5 * k) - 1); ok3 &= dev < 1e-3
    dyn = {}
    a0 = A0["canonical"]; Mb = 10 ** 10.45 * MS; rM = math.sqrt(G * Mb / a0); m_ = R_DUST; kk = m_ * (1 + m_ / 2)
    Req = math.sqrt(1 + u_eq(kk)) / u_eq(kk) * rM; Ms_ = m_ * Mb
    for fac in (0.99, 1.01):
        def rhs(t, y): return [y[1], (Fw(y[0], Mb, a0) - G * Ms_ * (Mb + Ms_ / 2) / y[0] ** 2) / Ms_]
        T = 0.2 * math.sqrt(Req ** 3 / (G * Mb))
        so = solve_ivp(rhs, (0, T), [fac * Req, 0.0], rtol=1e-10, atol=[1e-6 * KPC, 1e-6])
        dyn[str(fac)] = float(so.y[0, -1] / (fac * Req) - 1)
    ok3 &= dyn["0.99"] < 0 and dyn["1.01"] > 0
    RES["KA"]["KA_3"] = dict(bracket_rows=rows, deep_k1e4_rel=dev, dynamic_share={"0.99_R_eq_rel_move": dyn["0.99"], "1.01_R_eq_rel_move": dyn["1.01"]}, pass_=bool(ok3))
    P(f"KA-3 statics: R_eq inside the Lean bracket for all k {all(r_['inside'] for r_ in rows)}; k 1e4 vs (3/2) k: {dev:.1e}; "
      f"shell (share) from rest at 0.99 R_eq moves {dyn['0.99']:+.3e}, at 1.01 R_eq {dyn['1.01']:+.3e} -> {'PASS' if ok3 else 'FAIL'}")
    # KA-4
    rho0, M0, V0, R0 = 1e-24, 1e38, 2e5, 1.0 * KPC
    def rhs4(t, y):
        R, Pm, M = y; dR, dP, dM = sweep(R, Pm / M, M, 0.0, rho0, 0.0, 0.0); return [dR, dP, dM]
    def t_of(R): return (M0 * (R - R0) + 4 * math.pi / 3 * rho0 * ((R ** 4 - R0 ** 4) / 4 - R0 ** 3 * (R - R0))) / (M0 * V0)
    Rs_ = [2 * KPC, 5 * KPC, 10 * KPC, 20 * KPC, 40 * KPC]; ts_ = [t_of(x) for x in Rs_]
    so = solve_ivp(rhs4, (0, ts_[-1]), [R0, M0 * V0, M0], method="DOP853", rtol=1e-12, atol=[1e-6, 1e20, 1e20], t_eval=ts_)
    relR = max(abs(so.y[0, i] / Rs_[i] - 1) for i in range(5)); relP = max(abs(so.y[1, i] / (M0 * V0) - 1) for i in range(5))
    ka4 = relR < 1e-6 and relP < 1e-8
    RES["KA"]["KA_4"] = dict(max_rel_R=relR, max_rel_momentum=relP, pass_=bool(ka4))
    P(f"KA-4 snowplow vs analytic (static medium, no gravity): max rel R {relR:.1e} (1e-6), momentum {relP:.1e} (1e-8) -> {'PASS' if ka4 else 'FAIL'}")
    # KA-5
    tp = dict(p=1e-12, rho=1e-24, R0=1.0 * KPC, T=3e15, mref=1e38)
    e5 = ebracket(None, None, None, None, test=tp)
    Vth = math.sqrt(tp["p"] / (2 * tp["rho"])); relV = abs(e5["Vf_last"] / Vth - 1)
    relej = float(np.max(np.abs(e5["v_layers"] / (2 * Vth) - 1))) if e5["v_layers"].size else 1.0
    relE = abs(e5["KE"] / e5["work_exact"] - 1)
    ka5 = relV < 1e-3 and relej < 1e-3 and relE < 1e-3
    RES["KA"]["KA_5"] = dict(front_rel=relV, ejecta_rel=relej, KE_over_work_rel=relE, layers=int(e5["v_layers"].size), pass_=bool(ka5))
    P(f"KA-5 elastic front: speed rel {relV:.1e}, ejecta 2 V_f rel {relej:.1e}, KE / work rel {relE:.1e} ({e5['v_layers'].size} layers) -> {'PASS' if ka5 else 'FAIL'}")
    # KA-6
    nc = {}
    tabNC = radii_table("NC", 0.0, 1.0)
    for f, a0 in A0.items(): nc[f] = compensated(tabNC, a0, 1.0)["q_tot"]
    ka6 = abs(nc["canonical"] - 0.0180) < 1e-3 and abs(nc["alt"] - 0.0182) < 1e-3 and len(KIDS) == 59
    RES["KA"]["KA_6"] = dict(NC_q_tot=nc, kids_points=len(KIDS), pass_=bool(ka6))
    P(f"KA-6 compensated on NC at z 1: {nc['canonical']:.4f} / {nc['alt']:.4f} (SWT1 0.0180 / 0.0182); KiDS points {len(KIDS)} -> {'PASS' if ka6 else 'FAIL'}")
    KA_OK = all(RES["KA"][k]["pass_"] for k in RES["KA"])
    P(f"known answers: {'ALL PASS' if KA_OK else 'A KNOWN ANSWER FAILED -> NO VERDICT'} ({time.time() - T0:.0f} s)")

# ====================================================================== PART B runs
def fmt_run(r_):
    o = r_["out"]
    return " / ".join(f"{o[str(z)]['R_w_kpc']:.0f}" for z in ZOUT)

if MUT:
    P("")
    P("MUTATE: sticky snowplow, X = 1, four KiDS masses, every z_n, both footings; graded run recomputed alongside.")
    mres = {}
    for f, a0 in A0.items():
        mres[f] = {}
        for zn in ZNS:
            row = {}
            for lm in BINS:
                Mb = 10 ** lm * MS
                g_ = sticky(Mb, a0, 1, zn); off = sticky(Mb, a0, 1, zn, fmult=0.0); sg = sticky(Mb, a0, 1, zn, fmult=-1.0); x100 = sticky(Mb, a0, 1, zn, fmult=100.0)
                row[str(lm)] = dict(graded_Rw0_kpc=g_["R_w0_kpc"], graded_cold200=g_["cold200_over_Mb"],
                                    OFF_cold200=off["cold200_over_Mb"], OFF_F2_fail=bool(off["cold200_over_Mb"] > F2LINE),
                                    SIGN_Rw0_kpc=sg["R_w0_kpc"], SIGN_collapsed=bool(sg["R_w0_kpc"] == 0.0),
                                    x100_Rw0_kpc=x100["R_w0_kpc"],
                                    x100_rise=bool((g_["R_w0_kpc"] == 0.0 and x100["R_w0_kpc"] > 0) or (g_["R_w0_kpc"] > 0 and x100["R_w0_kpc"] >= 2 * g_["R_w0_kpc"])))
                d = row[str(lm)]
                P(f"[{f}] z_n {zn} log M {lm}: graded R_w(0) {d['graded_Rw0_kpc']:.0f} kpc, cold<200 {d['graded_cold200']:.2f} M_b | M-OFF cold<200 "
                  f"{d['OFF_cold200']:.2f} M_b ({'FAIL G-F2' if d['OFF_F2_fail'] else 'passes G-F2'}) | M-SIGN R_w(0) {d['SIGN_Rw0_kpc']:.1f} kpc "
                  f"({'collapsed' if d['SIGN_collapsed'] else 'NOT collapsed'}) | M-x100 R_w(0) {d['x100_Rw0_kpc']:.0f} kpc ({'rise >= 2x' if d['x100_rise'] else 'NO 2x rise'})")
            mres[f][str(zn)] = row
    allrows = [mres[f][str(zn)][str(lm)] for f in A0 for zn in ZNS for lm in BINS]
    RES["MUTATE"] = dict(rows=mres, M_OFF_bites=bool(all(x["OFF_F2_fail"] for x in allrows)),
                         M_SIGN_bites=bool(all(x["SIGN_collapsed"] for x in allrows)), M_x100_bites=bool(all(x["x100_rise"] for x in allrows)))
    P("")
    P(f"M-OFF (G-F2 must fail for all): {'BITES' if RES['MUTATE']['M_OFF_bites'] else 'NO BITE'}")
    P(f"M-SIGN (wall must collapse for all): {'BITES' if RES['MUTATE']['M_SIGN_bites'] else 'NO BITE'}")
    P(f"M-x100 (R_w(0) must rise >= 2x for all): {'BITES' if RES['MUTATE']['M_x100_bites'] else 'NO BITE'}")
else:
    P("")
    P("PART B. Building the record's flow fields (160 labels per mass and X) and R_h,n ...")
    for X in (1, 0, 3):
        for lm in list(BINS) + list(LG):
            flow_for(10 ** lm * MS, X)
    for zn in ZNS:
        for lm in list(BINS) + list(LG): Rh_n(10 ** lm * MS, zn)
    P(f"   done ({time.time() - T0:.0f} s)")
    RES["reported"]["R_h_n_kpc"] = {str(zn): {str(lm): Rh_n(10 ** lm * MS, zn) / KPC for lm in BINS} for zn in ZNS}
    P("R_h,n (the record's NC radius at nucleation, kpc): " + "; ".join(f"z_n {zn}: " + ", ".join(f"{Rh_n(10**lm*MS, zn)/KPC:.0f}" for lm in BINS) for zn in ZNS))

    # ---- sticky, all X, z_n, footings: four KiDS masses + GSMF grid
    P("")
    P("STICKY SNOWPLOW (graded at X = 1). R_w at z 2 / 1 / 0.5 / 0 in kpc; cold inside 200 kpc at z 0.")
    ST = {}
    for f, a0 in A0.items():
        ST[f] = {}
        for X in (1, 0, 3):
            for zn in ZNS:
                key = f"X{X}_zn{zn}"
                rows4 = {lm: sticky(10 ** lm * MS, a0, X, zn) for lm in BINS}
                rowsG = {lm: sticky(10 ** lm * MS, a0, X, zn) for lm in LG}
                g = gate_eval(rows4, rowsG, a0)
                ST[f][key] = dict(kids={str(lm): rows4[lm] for lm in BINS}, gsmf={str(lm): dict(out=rowsG[lm]["out"], final_state=rowsG[lm]["final_state"]) for lm in LG}, gates=g)
                for lm in BINS:
                    r_ = rows4[lm]; fl = r_["flags"]
                    P(f"[{f}] X {X} z_n {zn} log M {lm}: R_w {fmt_run(r_)} kpc; final {r_['final_state']}, M_s {r_['M_s0_over_Mb']:.2f} M_b; "
                      f"cold<200 kpc {r_['cold200_over_Mb']:.3f} M_b; R_w/R_K {g['G_K']['Rw_over_RK'][str(lm)]:.3f}; "
                      f"break-out z {fl['broke_out_z'] if fl['broke_out_z'] is None else round(fl['broke_out_z'], 3)}, stalls {fl['stalls']}, "
                      f"collapse z {fl['collapsed_z'] if fl['collapsed_z'] is None else round(fl['collapsed_z'], 3)}")
                gl = g["G_L"]["by_z"]
                P(f"[{f}] X {X} z_n {zn}: G-F2 {'PASS' if g['G_F2']['pass_'] else 'FAIL'}; G-K {'PASS' if g['G_K']['pass_'] else 'FAIL'} "
                  f"(KiDS points outside the wall {g['G_K']['kids_outside_total']} of 59); G-L z 1 q {gl['1.0']['q_tot']:.4f} filling {gl['1.0']['f_V']:.4f} "
                  f"{'PASS' if g['G_L']['pass_'] else 'FAIL'} (z 0 {gl['0.0']['q_tot']:.4f}, z 0.5 {gl['0.5']['q_tot']:.4f}, z 2 {gl['2.0']['q_tot']:.4f})"
                  f" -> {'ALL PASS' if g['all_pass'] else 'fails ' + ', '.join(g['failing'])}")
            P(f"   [{f}] sticky done ({time.time() - T0:.0f} s)")
    RES["runs"]["sticky"] = ST

    # ---- reported sticky brackets: R_0 and pressureless share (X = 1, four masses)
    rep = {}
    for f, a0 in A0.items():
        rep[f] = {}
        for zn in ZNS:
            for tag, kw in (("R0_0.3rM", dict(R0fac=0.3)), ("R0_3rM", dict(R0fac=3.0)), ("pB_off", dict(pB_on=False))):
                rr = {str(lm): sticky(10 ** lm * MS, a0, 1, zn, **kw) for lm in BINS}
                rep[f][f"zn{zn}_{tag}"] = {k_: dict(R_w0_kpc=v_["R_w0_kpc"], cold200_over_Mb=v_["cold200_over_Mb"], Rw_over_RK=v_["R_w0_kpc"] * KPC / RK(10 ** float(k_) * MS)) for k_, v_ in rr.items()}
                P(f"reported [{f}] z_n {zn} {tag}: R_w(0) " + ", ".join(f"{v_['R_w0_kpc']:.0f}" for v_ in rr.values()) + " kpc; cold<200 "
                  + ", ".join(f"{v_['cold200_over_Mb']:.2f}" for v_ in rr.values()) + " M_b")
    RES["reported"]["sticky_brackets"] = rep

    # ---- energy-conserving bracket
    P("")
    P("ENERGY-CONSERVING BRACKET (elastic front, free layers). Timing one run first (contingency: every other GSMF mass if > 30 min).")
    tt0 = time.time(); _t = ebracket(10 ** 10.45 * MS, A0["canonical"], 1, 6.0); t_one = time.time() - tt0
    n_full = 2 * 3 * 3 * (4 + len(LG)); proj = t_one * n_full / 60
    every_other = EBR_EVERY_OTHER or proj > 30.0
    P(f"   one run {t_one:.1f} s ({_t['nstep']} steps); projected {proj:.1f} min for the full grid -> "
      f"{'EVERY OTHER GSMF MASS (contingency)' if every_other else 'full GSMF grid'}")
    RES["reported"]["ebracket_timing"] = dict(one_run_s=t_one, projected_min=proj, every_other=bool(every_other))
    LGE = list(LG[::2]) if every_other else list(LG)
    EB = {}
    for f, a0 in A0.items():
        EB[f] = {}
        for X in (1, 0, 3):
            for zn in ZNS:
                key = f"X{X}_zn{zn}"
                rows4 = {lm: ebracket(10 ** lm * MS, a0, X, zn) for lm in BINS}
                rowsE = {lm: ebracket(10 ** lm * MS, a0, X, zn) for lm in LGE}
                rowsG = interp_runs(rowsE, LGE) if every_other else rowsE
                g = gate_eval(rows4, rowsG, a0)
                EB[f][key] = dict(kids={str(lm): {k_: v_ for k_, v_ in rows4[lm].items()} for lm in BINS}, gates=g)
                for lm in BINS:
                    r_ = rows4[lm]
                    P(f"[{f}] E X {X} z_n {zn} log M {lm}: R_w {fmt_run(r_)} kpc (front {r_['front_kpc']:.0f}, {r_['region']}); "
                      f"cold<200 kpc {r_['cold200_over_Mb']:.3f} M_b; R_w/R_K {g['G_K']['Rw_over_RK'][str(lm)]:.3f}; layers {r_['n_layers']}, "
                      f"central {r_['central_over_Mb']:.3f} M_b, steps {r_['nstep']}")
                gl = g["G_L"]["by_z"]
                P(f"[{f}] E X {X} z_n {zn}: G-F2 {'PASS' if g['G_F2']['pass_'] else 'FAIL'}; G-K {'PASS' if g['G_K']['pass_'] else 'FAIL'} "
                  f"({g['G_K']['kids_outside_total']} of 59 outside); G-L z 1 q {gl['1.0']['q_tot']:.4f} {'PASS' if g['G_L']['pass_'] else 'FAIL'} "
                  f"(z 0 {gl['0.0']['q_tot']:.4f}) -> {'ALL PASS' if g['all_pass'] else 'fails ' + ', '.join(g['failing'])}")
            P(f"   [{f}] E-bracket done ({time.time() - T0:.0f} s)")
    RES["runs"]["energy_bracket"] = EB

    # ---- labels
    P("")
    def label_of(D, f, X):
        per = {str(zn): D[f][f"X{X}_zn{zn}"]["gates"] for zn in ZNS}
        winners = [zn for zn in per if per[zn]["all_pass"]]
        if winners: return "DELIVERS (z_n " + ", ".join(winners) + ")", True, per
        return "FAILS (" + "; ".join(f"z_n {zn}: " + ", ".join(per[zn]["failing"]) for zn in per) + ")", False, per
    for f in A0:
        if not KA_OK:
            RES["labels"][f] = dict(SNP1="NO VERDICT (known answer failed)"); P(f"LABEL [{f}]: NO VERDICT"); continue
        lab, dl, per = label_of(ST, f, 1)
        labE, dlE, perE = label_of(EB, f, 1)
        diff = [f"z_n {zn} {k}" for zn in per for k in ("G_F2", "G_K", "G_L") if per[zn][k]["pass_"] != perE[zn][k]["pass_"]]
        suffix = "HINGES ON THE STICKY IDEALISATION" if dl != dlE else "SAME UNDER THE ENERGY-CONSERVING BRACKET"
        brk = {f"X{X}": label_of(ST, f, X)[0] for X in (0, 3)}
        brkE = {f"X{X}": label_of(EB, f, X)[0] for X in (0, 3)}
        RES["labels"][f] = dict(SNP1=lab, suffix=suffix, gate_verdicts_differing_in_E=diff, energy_bracket_X1=labE, brackets_sticky=brk, brackets_energy=brkE)
        P(f"LABEL [{f}]: SNP1 {lab}; {suffix}" + (f" (differs: {', '.join(diff)})" if diff else ""))
        P(f"   energy bracket X 1: {labE}")
        P(f"   brackets (sticky): X 0 {brk['X0']}; X 3 {brk['X3']}")
        P(f"   brackets (energy): X 0 {brkE['X0']}; X 3 {brkE['X3']}")

P(f"runtime {time.time() - T0:.0f} s. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def _clean(o):
    if isinstance(o, dict): return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, np.ndarray): return [_clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
RES["end"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
json.dump(_clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
