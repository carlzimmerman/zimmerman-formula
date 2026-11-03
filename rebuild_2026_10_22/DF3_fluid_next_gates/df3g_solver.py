"""DF3_fluid_next_gates solver. Hydrostatic barotrope in the a0 law's field, integrated out from a central density, reading N or S, own code. Signature as HF1's solve so CRG1's chain can call it. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import math
import numpy as np
np.seterr(all="ignore")
G = 6.674e-11; MSUN = 1.989e30; PC = 3.0857e16; CL = 2.99792458e8
RHO_A = 0.05 * MSUN / PC ** 3
class Cfg:
    gamma = 1.0; sigma = 1e5; rho_a = RHO_A; K = 1.0; reading = "N"; gself = 1.0; noeq = "H"; dln = 0.06; r_start = PC
STAT = dict(rows=0, noeq=0, unres=0)
LOGS = dict(gmrc2=[], csc=[])
def law(gN, a0):
    gN = np.asarray(gN, float)
    if a0 <= 0: return gN
    return np.where(gN > 0, 0.5 * gN + np.sqrt(0.25 * gN * gN + a0 * np.maximum(gN, 0)), gN)
def rho_of(Psi, lrc):
    """rho from enthalpy H(rho) = H(rho_c) - Psi, H = s2/k (rho/rho_a)^k, k = Gamma - 1; k = 0 is log."""
    k = Cfg.gamma - 1; s2 = Cfg.sigma ** 2 * Cfg.K
    if abs(k) < 1e-9: return np.exp(np.clip(lrc - Psi / s2, -700, 700))
    a = np.exp(k * (lrc - math.log(Cfg.rho_a))) - k * Psi / s2
    if k > 0: a = np.maximum(a, 0.0)
    return Cfg.rho_a * a ** (1 / k)
def field(Mb, M, r, a0):
    if Cfg.reading == "N": return law(G * Mb / r ** 2, a0) + Cfg.gself * G * M / r ** 2
    return law(G * (Mb + Cfg.gself * M) / r ** 2, a0)
def shoot(rr, Mb, inr, lrc, a0, keep=False):
    """rows x K. Returns final M, and M at grid cell 10; with keep the paths."""
    dl = math.log(rr[1] / rr[0]); rc = np.exp(lrc); M = 4 * math.pi / 3 * rr[0] ** 3 * rc; Psi = np.zeros_like(M); M10 = None; pm = [M.copy()]; pr = [rc.copy()]
    for i in range(rr.size - 1):
        a, b = rr[i], rr[i + 1]; ma, mb = Mb[:, i, None], Mb[:, i + 1, None]; wa, wb = inr[:, i, None], inr[:, i + 1, None]
        kP = field(ma, M, a, a0) * a; kM = 4 * math.pi * a ** 3 * rho_of(Psi, lrc) * wa
        Pq = Psi + dl * kP; Mq = M + dl * kM
        lP = field(mb, Mq, b, a0) * b; lM = 4 * math.pi * b ** 3 * rho_of(Pq, lrc) * wb
        Psi = Psi + 0.5 * dl * (kP + lP); M = M + 0.5 * dl * (kM + lM)
        if i == 9: M10 = M.copy()
        if keep: pm.append(M.copy()); pr.append(rho_of(Psi, lrc) * wb)
    M = np.where(np.isfinite(M), M, -1.0)
    if keep: return M, M10, np.stack(pm, -1), np.stack(pr, -1)
    return M, M10
def pick(ME, M10, fair):
    """First local maximum of M_f(rho_c), scan low to high; first crossing of fair share before it, resolved. Returns has, j, jp."""
    n, K = ME.shape; fall = ME[:, 1:] < ME[:, :-1] * (1 - 1e-9); jp = np.where(fall.any(1), fall.argmax(1), K - 1); idx = np.arange(K)[None, :]; before = idx <= jp[:, None]; resolved = (M10 < 0.5 * ME) | (Cfg.gamma > 4 / 3); cr = (ME >= fair[:, None]) & before; good = cr & resolved; return good.any(1), good.argmax(1), jp, cr.any(1)
def solve(r, Mb, rta, Rsys, Mfair, m_ev=None, a0=0.0, gf=2.0, capf=1.0, iters=None, tol=None):
    r_all = np.asarray(r, float); Mb = np.asarray(Mb, float); sh = Mb.shape[:-1]; Mb2 = Mb.reshape(-1, r_all.size); N = Mb2.shape[0]
    rta_ = np.broadcast_to(np.asarray(rta, float).reshape(-1) if np.ndim(rta) else float(rta), (N,)).copy(); fair = np.broadcast_to(np.asarray(Mfair, float).reshape(-1) if np.ndim(Mfair) else float(Mfair), (N,)).copy()
    rs = min(Cfg.r_start, 0.5 * r_all[0]); top = max(r_all[-1], rta_.max() * 1.0001); nr = int(math.ceil(math.log(top / rs) / Cfg.dln)) + 1; rr = np.geomspace(rs, top, nr); lr = np.log(rr); lq = np.log(r_all)
    MM = np.empty((N, nr))
    for i in range(N):
        y = np.log(np.maximum(np.maximum.accumulate(Mb2[i]), 1e-300)); v = np.exp(np.interp(lr, lq, y)); lo = rr < r_all[0]; v[lo] = max(Mb2[i, 0], 0.0) * (rr[lo] / r_all[0]) ** 2; MM[i] = v
    inr = rr[None, :] <= rta_[:, None]; Lg = np.linspace(math.log(1e-36), math.log(1e-8), 57) if Cfg.gamma <= 4 / 3 else np.linspace(math.log(1e-36), math.log(1e-1), 71)  # A2: Gamma > 4/3 ceiling raised
    L = np.tile(Lg, (N, 1)); ME, M10 = shoot(rr, MM, inr, L, a0); has, j, jp, _ = pick(ME, M10, fair); rows = np.arange(N)
    lo = L[rows, np.maximum(np.where(has, j, jp) - 1, 0)]; hi = L[rows, np.where(has, j, np.minimum(jp + 1, Lg.size - 1))]
    for _ in range(4):
        L = lo[:, None] + (hi - lo)[:, None] * np.linspace(0, 1, 9)[None, :]; ME, M10 = shoot(rr, MM, inr, L, a0); h2, j2, jp2, _ = pick(ME, M10, fair)
        hit = has & h2; lo = np.where(hit, L[rows, np.maximum(j2 - 1, 0)], L[rows, np.maximum(jp2 - 1, 0)]); hi = np.where(hit, L[rows, j2], L[rows, np.minimum(jp2 + 1, 8)])
        has = has & h2 | has & (fair <= 0)
    lrc = hi if False else np.where(has, hi, 0.5 * (lo + hi)); zero = fair <= 0
    Me, M10f, Pm, Pr = shoot(rr, MM, inr, lrc[:, None], a0, keep=True); Pm = Pm[:, 0, :]; Pr = Pr[:, 0, :]; Pm = np.where(zero[:, None], 0.0, Pm); Pr = np.where(zero[:, None], 0.0, Pr); noeq = (~has) & (~zero)
    STAT["rows"] += N; STAT["noeq"] += int(noeq.sum()); end = Pm[:, -1]; idx = (Pm >= 0.5 * end[:, None]).argmax(1); un = (idx < 10) & ~zero & ~noeq; STAT["unres"] += int(un.sum())
    if Cfg.noeq == "C":
        Pm = Pm + (noeq * np.maximum(fair - end, 0.0))[:, None]
    x = np.log(rr); Mf = np.empty((N, r_all.size)); Ro = np.empty((N, r_all.size))
    for i in range(N):
        Mf[i] = np.exp(np.interp(lq, x, np.log(np.maximum(Pm[i], 1e-300)))); Ro[i] = np.exp(np.interp(lq, x, np.log(np.maximum(Pr[i], 1e-300))))
    Rs = np.broadcast_to(np.asarray(Rsys, float).reshape(-1) if np.ndim(Rsys) else float(Rsys), (N,)); rs_ = np.array([math.exp(np.interp(math.log(Rs[i]), lq, np.log(np.maximum(Ro[i], 1e-300)))) for i in range(N)]); cs = cs_of(rs_)
    rh = rr[idx]; gm = G * end / np.maximum(rh, 1e-30) / CL ** 2; csc = cs_of(np.exp(lrc)) / CL; LOGS["gmrc2"].extend(gm.tolist()); LOGS["csc"].extend(csc.tolist())
    sq = lambda v: v.reshape(sh) if sh else (float(v[0]) if v.dtype != bool else bool(v[0]))
    return dict(Mf=Mf.reshape(sh + (r_all.size,)), rho=Ro.reshape(sh + (r_all.size,)), sigma=sq(cs), cap=sq(np.full(N, Cfg.rho_a)), conv=True, noeq=sq(noeq), lrc=sq(lrc), held=sq(end), rhalf=sq(rh), gmrc2=sq(gm), csc=sq(csc), unres=sq(un), iters=1, resid=0.0)
def cs_of(rho):
    return Cfg.sigma * math.sqrt(Cfg.K) * (np.maximum(np.asarray(rho, float), 1e-300) / Cfg.rho_a) ** ((Cfg.gamma - 1) / 2)
# ---------------- TOV, Fermi-gas equation of state matched to K in the non-relativistic limit; EOS only, no particle adopted
HBAR = 1.054571817e-34
def m_of_K(K):
    return ((3 * math.pi ** 2) ** (2 / 3) * HBAR ** 2 / (5 * K)) ** (3 / 8)
def tov_max(m):
    """Largest stable mass, dimensionless integration, Msun."""
    e0 = m ** 4 * CL ** 5 / (math.pi ** 2 * HBAR ** 3)
    def eps(x):
        s = np.sqrt(1 + x * x); return e0 * (x * s * (2 * x * x + 1) - np.arcsinh(x)) / 8
    def prs(x):
        s = np.sqrt(1 + x * x); return e0 * (x * s * (2 * x * x - 3) + 3 * np.arcsinh(x)) / 24
    xt = np.geomspace(1e-3, 300, 6000); et = eps(xt); pt = prs(xt)
    lpt = np.log(pt); let = np.log(et); best = 0.0
    r_u = 1 / math.sqrt(G * e0 / CL ** 4 * 4 * math.pi) * 1.0
    for xc in np.geomspace(0.3, 30, 60):
        p = float(prs(xc)); r = 1e-4; mm = 4 / 3 * math.pi * r ** 3 * float(eps(xc)) / e0
        pc = p; h = 2e-3
        y = math.log(r); P_ = p / e0
        while P_ > 1e-9 * pc / e0 and y < 12:
            def f(y_, P__, m__):
                r_ = math.exp(y_); e_ = math.exp(float(np.interp(math.log(max(P__ * e0, pt[0])), lpt, let))) / e0
                d = r_ - 2 * m__
                return -(e_ + P__) * (m__ + 4 * math.pi * r_ ** 3 * P__) / (r_ * d) * r_, 4 * math.pi * r_ ** 3 * e_
            a1, b1 = f(y, P_, mm); a2, b2 = f(y + h / 2, P_ + h / 2 * a1, mm + h / 2 * b1); a3, b3 = f(y + h / 2, P_ + h / 2 * a2, mm + h / 2 * b2); a4, b4 = f(y + h, P_ + h * a3, mm + h * b3)
            P2 = P_ + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
            if P2 <= 0: break
            P_ = P2; mm += h / 6 * (b1 + 2 * b2 + 2 * b3 + b4); y += h
        best = max(best, mm)
    L = CL ** 2 / math.sqrt(G * e0)  # length unit where G e / c^4 = 1/L^2
    return best * L * CL ** 2 / G / MSUN
