"""WF1: ground state + envelope with the a0 law on baryons + field (FROZEN_CRITERIA, gate 2-3 profile). Same signature as hf1_fermion.solve. kappa = 1/2 FITTED; not theory closed."""
import math
import numpy as np
from scipy.linalg import eigh_tridiagonal
np.seterr(all="ignore")
HBAR, C_L, EV = 1.054571817e-34, 299792458.0, 1.602176634e-19
G = 6.674e-11
class Cfg: sig_mult = 1.0
STAT = dict(rows=0, unbound=0, unres=0, zero=0, noconv=0, big=0)
import hf1_fermion as _F
FERMION_SOLVE = _F.solve
def lawg(gN, a0):
    gN = np.asarray(gN, float); return np.where(gN > 0, gN * (0.5 + np.sqrt(0.25 + a0 / np.where(gN > 0, gN, 1.0))), gN)
def _cum(y, dl):
    out = np.zeros_like(y); out[1:] = np.cumsum(0.5 * (y[1:] + y[:-1]) * dl); return out
def ground(r, Phi, kap, dl):
    """Lowest state of -kap u'' + Phi u = E u, u = r psi, wall at both ends of a log grid. Returns E and y with sum y^2 = 1, where rho = M y^2 / (4 pi r^3 dl)."""
    d = kap * (2 / dl ** 2 + 0.25) / r ** 2 + Phi; e = -kap / (dl ** 2 * r[:-1] * r[1:])
    w, v = eigh_tridiagonal(d, e, select="i", select_range=(0, 0)); y = v[:, 0]; return float(w[0]), y / math.sqrt(float((y * y).sum()))
def _soliton(rr, dl, Mx, Ms, kap, a0, G_, y0=None, it=60, tol=1e-3):
    """Self-consistent ground state of mass Ms in external enclosed mass Mx, law on the sum. Returns E, y, <v^2>, rms radius."""
    k = rr.size; c = np.zeros(k); dd = 1.0
    if y0 is not None: c = Ms * (np.cumsum(y0 * y0) - 0.5 * y0 * y0)
    for _ in range(it):
        g = lawg(G_ * (Mx + c) / rr ** 2, a0); C_ = _cum(g * rr, dl); Phi = C_ - C_[-1]; E, y = ground(rr, Phi, kap, dl); n = Ms * (np.cumsum(y * y) - 0.5 * y * y); dd = float(np.max(np.abs(n - c))) / max(Ms, 1e-300); c = 0.5 * c + 0.5 * n
        if dd < tol: break
    return E, y, 2 * (E - float((y * y * Phi).sum())), math.sqrt(float((y * y * rr * rr).sum())), dd < tol
def _row(r, Mb, Menv, s2, rta, Mfair, m_ev, a0, G_):
    n = r.size; dl = math.log(r[1] / r[0]); zero = dict(Mf=np.zeros(n), rho=np.zeros(n), Ms=0.0, rs=0.0, flag="none", conv=True)
    if Mfair <= 0: return zero
    inr = r <= rta * (1 + 1e-12); k = int(inr.sum()); rr = r[inr]; w3 = 4 * math.pi * rr ** 3; mk = m_ev * EV / C_L ** 2; kap = (HBAR / mk) ** 2 / 2; Mx = np.maximum(Mb[:k], 0.0) + Menv[:k]; t2 = 3 * s2 * Cfg.sig_mult ** 2
    lo, hi = math.log(1e-8 * Mfair), math.log(Mfair); El, yl, vl, rl, c1 = _soliton(rr, dl, Mx, math.exp(lo), kap, a0, G_); Eh, yh, vh, rh, c2 = _soliton(rr, dl, Mx, math.exp(hi), kap, a0, G_); conv = c1 and c2
    if vl >= t2: Ms, y, rs, flag = 0.0, yl, rl, "zero"
    elif vh <= t2: Ms, y, rs, flag = Mfair, yh, rh, "full"
    else:
        y = yl
        for _ in range(16):
            mid = 0.5 * (lo + hi); E, y, v, rs, c3 = _soliton(rr, dl, Mx, math.exp(mid), kap, a0, G_, y0=y)
            if v < t2: lo = mid
            else: hi = mid
        conv = conv and c3; Ms = math.exp(0.5 * (lo + hi)); flag = "none"
    if rs > 0.5 * rta: zero.update(rs=rs, flag="unbound", conv=conv); return zero
    if rs < 3 * rr[0]: flag = "unres"; Ms = 0.0  # AMENDMENT_A1 part 8
    C_ = _cum(lawg(G_ * Mx / rr ** 2, a0) * rr, dl); ex = np.clip((C_[-1] - C_) / max(s2 * Cfg.sig_mult ** 2, 1e-300), 0, 600); ex = np.minimum(ex, float(np.interp(math.log(rs), np.log(rr), ex))); rs_ = Ms * y * y / (w3 * dl); a, b = -500.0, 500.0
    def tot(lr):
        q = np.maximum(rs_, np.exp(np.minimum(lr + ex, -20.0))); return q, 0.5 * float((q[1:] * w3[1:] + q[:-1] * w3[:-1]).sum()) * dl + q[0] * w3[0] / 3
    for _ in range(60):
        mid = 0.5 * (a + b); q, t = tot(mid)
        if t > Mfair: b = mid
        else: a = mid
    q, t = tot(a)
    if t > 0: q = q * Mfair / t
    c = np.zeros(k); c[1:] = np.cumsum(0.5 * (q[1:] * w3[1:] + q[:-1] * w3[:-1])) * dl; c += q[0] * w3[0] / 3; Mf = np.full(n, c[-1]); Mf[:k] = c; rho = np.zeros(n); rho[:k] = q
    return dict(Mf=Mf, rho=rho, Ms=Ms, rs=rs, flag=flag, conv=conv)
def solve(r, Mb, rta, Rsys, Mfair, m_ev, a0, gf=2.0, capf=1.0, iters=200, tol=1e-4, G_=G):
    Mb = np.asarray(Mb, float); sh = Mb.shape[:-1]; env = FERMION_SOLVE(r, Mb, rta, Rsys, Mfair, 1e6, a0, gf=2.0, capf=1.0, iters=iters, tol=tol, G_=G_)  # cap far above any density: isothermal envelope and sigma
    rta_ = np.broadcast_to(np.asarray(rta, float), sh); F_ = np.broadcast_to(np.asarray(Mfair, float), sh); sg = np.broadcast_to(env["sigma"], sh); Menv = env["Mf"]
    Mf = np.zeros_like(Mb); rho = np.zeros_like(Mb); Ms = np.zeros(sh); RS = np.zeros(sh); conv = bool(env["conv"])
    for idx in np.ndindex(sh):
        q = _row(r, Mb[idx], Menv[idx], float(sg[idx]) ** 2, float(rta_[idx]), float(F_[idx]), m_ev, a0, G_); Mf[idx] = q["Mf"]; rho[idx] = q["rho"]; Ms[idx] = q["Ms"]; RS[idx] = q["rs"]; conv = conv and q["conv"]
        STAT["rows"] += 1; STAT["unbound"] += q["flag"] == "unbound"; STAT["unres"] += q["flag"] == "unres"; STAT["zero"] += q["Ms"] == 0; STAT["noconv"] += not q["conv"]; STAT["big"] += (float(F_[idx]) > 0 and q["Ms"] > 0.3 * float(F_[idx]))
    if not sh: Ms = float(Ms); RS = float(RS)
    return dict(Mf=Mf, sigma=env["sigma"], rho=rho, cap=np.zeros(sh) if sh else 0.0, conv=conv, iters=0, resid=0.0, Ms=Ms, rs=RS, env=Menv)
