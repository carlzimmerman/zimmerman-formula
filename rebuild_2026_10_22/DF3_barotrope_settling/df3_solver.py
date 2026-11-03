"""DF3: hydrostatic barotropic dark fluid with the a0 law on baryons + fluid, integrated out from a central density; signature as hf1_fermion.solve. kappa = 1/2 FITTED; not theory closed."""
import math
import numpy as np
np.seterr(all="ignore")
G = 6.674e-11; MSUN = 1.989e30; PC = 3.0857e16
RHO_A = 0.05 * MSUN / PC ** 3
class Cfg: gamma = 5 / 3; sigma = 1e5; rho_a = RHO_A; K_mult = 1.0; nmax = 200
STAT = dict(rows=0, noeq=0)
LRC = np.log(np.logspace(-34, -10, 49))
def lawg(gN, a0):
    gN = np.asarray(gN, float); return np.where(gN > 0, gN * (0.5 + np.sqrt(0.25 + a0 / np.where(gN > 0, gN, 1.0))), gN)
def _rho(Psi, lrc, gam, s2, ra):
    if abs(gam - 1) < 1e-9: return np.exp(lrc - Psi / s2)
    k = gam - 1; hc = s2 / k * np.exp(k * (lrc - math.log(ra))); h = hc - Psi; a = k * h / s2
    if gam > 1: a = np.maximum(a, 0.0)
    return ra * a ** (1 / k)
def integ(r, Mb, inr, lrc, a0, gam, s2, ra, G_, keep=False):
    """Mb (rows, n); inr (rows, n); lrc (rows, K). Heun in ln r. Returns M at the end (rows, K), and the path if keep."""
    dl = math.log(r[1] / r[0]); n = r.size; rc = np.exp(lrc); M = 4 * math.pi / 3 * r[0] ** 3 * rc; Psi = np.zeros_like(M); path = [M.copy()] if keep else None; rho_p = [rc.copy()] if keep else None
    for i in range(n - 1):
        r0, r1 = r[i], r[i + 1]; m0, m1 = Mb[:, i, None], Mb[:, i + 1, None]; w0, w1 = inr[:, i, None], inr[:, i + 1, None]
        k1P = lawg(G_ * (m0 + M) / r0 ** 2, a0) * r0; k1M = 4 * math.pi * r0 ** 3 * _rho(Psi, lrc, gam, s2, ra) * w0
        Pp = Psi + dl * k1P; Mp = M + dl * k1M
        k2P = lawg(G_ * (m1 + Mp) / r1 ** 2, a0) * r1; k2M = 4 * math.pi * r1 ** 3 * _rho(Pp, lrc, gam, s2, ra) * w1
        Psi = Psi + .5 * dl * (k1P + k2P); M = M + .5 * dl * (k1M + k2M)
        if keep: path.append(M.copy()); rho_p.append(_rho(Psi, lrc, gam, s2, ra) * w1)
    return (M, np.stack(path, -1), np.stack(rho_p, -1)) if keep else M
def solve(r, Mb, rta, Rsys, Mfair, m_ev=None, a0=0.0, gf=2.0, capf=1.0, iters=None, tol=None, G_=G):
    r_all = np.asarray(r); Mb = np.asarray(Mb, float); sh = Mb.shape[:-1]; Mb2 = Mb.reshape(-1, r_all.size); N = Mb2.shape[0]
    st = max(1, int(math.ceil(r_all.size / Cfg.nmax))); idx = np.arange(0, r_all.size, st); idx = idx if idx[-1] == r_all.size - 1 else np.append(idx, r_all.size - 1)
    rr = r_all[idx] if np.allclose(np.diff(np.log(r_all[idx]))[:-1], math.log(r_all[idx[1]] / r_all[idx[0]])) and idx.size == r_all[::st].size else r_all[::st]
    MM = Mb2[:, ::st] if rr.size == r_all[::st].size else Mb2[:, idx]; rta_ = np.broadcast_to(np.asarray(rta, float).reshape(-1) if np.ndim(rta) else float(rta), (N,)); fair = np.broadcast_to(np.asarray(Mfair, float).reshape(-1) if np.ndim(Mfair) else float(Mfair), (N,)); inr = rr[None, :] <= rta_[:, None]
    gam, s2, ra = Cfg.gamma, Cfg.sigma ** 2 * Cfg.K_mult, Cfg.rho_a
    L = np.tile(LRC, (N, 1)); ME = integ(rr, MM, inr, L, a0, gam, s2, ra, G_); ME = np.where(np.isfinite(ME), ME, -1.0); rows = np.arange(N)
    def first_peak(E):
        """Index of the first local maximum; beyond it lies the unstable branch and, at high density, the unresolved one."""
        d = E[:, 1:] < E[:, :-1]; return np.where(d.any(1), d.argmax(1), E.shape[1] - 1)
    jp = first_peak(ME); ok = np.arange(ME.shape[1])[None, :] <= jp[:, None]; hit = (ME >= fair[:, None]) & ok; has = hit.any(1); j = hit.argmax(1)
    lo = LRC[np.maximum(np.where(has, j, jp) - 1, 0)]; hi = LRC[np.where(has, j, np.minimum(jp + 1, LRC.size - 1))]
    for _ in range(3):
        L = lo[:, None] + (hi - lo)[:, None] * np.linspace(0, 1, 13)[None, :]; ME = integ(rr, MM, inr, L, a0, gam, s2, ra, G_); ME = np.where(np.isfinite(ME), ME, -1.0); jp = first_peak(ME); ok = np.arange(13)[None, :] <= jp[:, None]; hit = (ME >= fair[:, None]) & ok; h1 = np.where(hit.any(1), hit.argmax(1), jp)
        cross = has & hit.any(1); lo2 = L[rows, np.maximum(h1 - 1, 0)]; hi2 = L[rows, np.where(cross, h1, np.minimum(h1 + 1, 12))]; lo, hi = lo2, hi2
    lrc = np.where(has, hi, 0.5 * (lo + hi))[:, None]; zero = fair <= 0
    Me, Mp, Rp = integ(rr, MM, inr, lrc, a0, gam, s2, ra, G_, keep=True); Mp = Mp[:, 0, :]; Rp = Rp[:, 0, :]
    Mp = np.where(zero[:, None], 0.0, Mp); Rp = np.where(zero[:, None], 0.0, Rp); noeq = (~has) & (~zero); STAT["rows"] += N; STAT["noeq"] += int(noeq.sum())
    if not np.array_equal(rr, r_all):
        x = np.log(rr); X = np.log(r_all); Mf = np.stack([np.exp(np.interp(X, x, np.log(np.maximum(q, 1e-300)))) for q in Mp]); rho = np.stack([np.exp(np.interp(X, x, np.log(np.maximum(q, 1e-300)))) for q in Rp])
    else: Mf, rho = Mp, Rp
    Rs = np.broadcast_to(np.asarray(Rsys, float).reshape(-1) if np.ndim(Rsys) else float(Rsys), (N,)); rs = np.array([np.interp(math.log(Rs[i]), np.log(r_all), rho[i]) for i in range(N)]); cs = Cfg.sigma * math.sqrt(Cfg.K_mult) * (np.maximum(rs, 1e-300) / ra) ** ((gam - 1) / 2)
    out = dict(Mf=Mf.reshape(sh + (r_all.size,)), sigma=cs.reshape(sh) if sh else float(cs[0]), rho=rho.reshape(sh + (r_all.size,)), cap=ra * np.ones(sh) if sh else ra, conv=True, noeq=noeq.reshape(sh) if sh else bool(noeq[0]), lrc=lrc[:, 0].reshape(sh) if sh else float(lrc[0, 0]), iters=1, resid=0.0)
    return out
