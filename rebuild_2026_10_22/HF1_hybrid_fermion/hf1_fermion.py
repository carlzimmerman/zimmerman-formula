"""HF1: the fermion's equilibrium profile, capped by phase space, with the a0 law on baryons + fermion (AMENDMENT_A1 R4). Batched over rows. kappa = 1/2 FITTED; not theory closed."""
import math
import numpy as np
np.seterr(all="ignore")
H_J, C_L, EV = 6.62607015e-34, 299792458.0, 1.602176634e-19
G = 6.674e-11

def rho_cap(m_ev, sigma, gf=2.0):
    """kg/m^3. f_max = g_f / (2 h^3), the Fermi-Dirac value; Maxwellian of dispersion sigma (m/s) at that phase density."""
    m = m_ev * EV / C_L ** 2
    return m ** 4 * (gf / 2) / H_J ** 3 * (2 * math.pi * sigma ** 2) ** 1.5

def tg_mmin(sigma, r0, gf=2.0):
    """Tremaine-Gunn minimum mass (eV) for a non-singular isothermal sphere, rho0 = 9 sigma^2 / (4 pi G r0^2): the closed form, m^4 = 9 h^3 / ((2 pi)^2.5 g G sigma r0^2)."""
    m4 = 9 * H_J ** 3 / ((2 * math.pi) ** 2.5 * gf * G * sigma * r0 ** 2)
    return m4 ** 0.25 * C_L ** 2 / EV

def lawg(gN, a0):
    gN = np.asarray(gN, float); return np.where(gN > 0, gN * (0.5 + np.sqrt(0.25 + a0 / np.where(gN > 0, gN, 1.0))), gN)

def _cum(y, dl):
    out = np.zeros_like(y); out[..., 1:] = np.cumsum(0.5 * (y[..., 1:] + y[..., :-1]) * dl, axis=-1); return out

def solve(r, Mb, rta, Rsys, Mfair, m_ev, a0, gf=2.0, capf=1.0, iters=200, tol=1e-4, G_=G):
    """r: log-spaced grid (m), 1-D. Mb: (..., n) enclosed baryons (kg). rta, Rsys, Mfair: (...) or scalar. Returns Mf (..., n), sigma (...), rho_f (..., n), rho_cap (...)."""
    Mb = np.asarray(Mb, float); sh = Mb.shape[:-1]; dl = math.log(r[1] / r[0]); rta = np.broadcast_to(np.asarray(rta, float)[..., None], sh + (1,)); Rsys = np.broadcast_to(np.asarray(Rsys, float)[..., None], sh + (1,)); Mfair = np.broadcast_to(Mfair, sh)
    inr = r <= rta; insys = r <= np.maximum(Rsys, r[1]); w = 4 * math.pi * r ** 3
    Mf = np.zeros_like(Mb); conv = False
    for it in range(iters):
        Mt = Mb + Mf; gN = G_ * Mt / r ** 2; g = lawg(gN, a0); V2 = g * r
        s2 = 0.5 * np.max(np.where(insys, V2, 0.0), axis=-1, keepdims=True)
        cap = capf * rho_cap(m_ev, np.sqrt(s2), gf)
        C = _cum(g * r, dl); idx = np.minimum(np.sum(inr, axis=-1, keepdims=True) - 1, r.size - 1); Cta = np.take_along_axis(C, idx, axis=-1)
        ex = np.clip((Cta - C) / s2, 0, 300) * inr      # -(Phi - Phi_ta)/sigma^2 >= 0 inside r_ta
        lo = np.full(sh + (1,), -400.0); hi = np.full(sh + (1,), 400.0)
        def mass(lr): return np.where(inr, np.minimum(cap, np.exp(np.minimum(lr + ex, 300.0))), 0.0)
        for _ in range(48):
            mid = 0.5 * (lo + hi); rho = mass(mid); tot = 0.5 * np.sum((rho[..., 1:] * w[1:] + rho[..., :-1] * w[:-1]), axis=-1, keepdims=True) * dl + rho[..., :1] * w[0] / 3
            big = tot > Mfair[..., None]; hi = np.where(big, mid, hi); lo = np.where(big, lo, mid)
        rho = mass(lo); Mn = _cum(rho * w, dl) + rho[..., :1] * w[0] / 3
        ch = float(np.max(np.abs(Mn - Mf) / np.maximum(Mb + Mn, 1e-300)))
        Mf = 0.5 * Mf + 0.5 * Mn
        if ch < tol: conv = True; break
    return dict(Mf=Mf, sigma=np.sqrt(s2)[..., 0], rho=rho, cap=cap[..., 0], conv=conv, iters=it + 1, resid=ch)
