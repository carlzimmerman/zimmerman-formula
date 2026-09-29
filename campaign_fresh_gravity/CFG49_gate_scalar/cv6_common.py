# cv6_common.py -- loads DE12's machinery UNEDITED (read-only) exactly as DE13 does, plus the reduced chi-sector operator.
# Nothing in the repo is written.  Scratchpad-only.
import os, math, io, contextlib, json
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P12 = os.path.join(REPO, "real_research/dark_energy_2026/DE12_mond_sector_gate_stiffness.py")
D12 = {"__name__": "de12", "__file__": P12}
_src = open(P12).read()
_head = _src.split("# ============================================================================================ C1 the amplification")[0]
_trans = _src.split("# ============================================================================================ the transitions")[1].split(
    "# ============================================================================================ G1 G2 the budget")[0]
_trans = _trans.split('banner("C2')[0]
_GRID_LINE = "r = np.geomspace(1.0, 2e4, 20000) * KPC"
assert _trans.count(_GRID_LINE) == 1
_trans_on = "def transition_on(rgrid, " + _trans.split("def transition(")[1].replace(_GRID_LINE, "r = rgrid")
with contextlib.redirect_stdout(io.StringIO()):
    exec((_head + _trans + "\n" + _trans_on).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
transition, transition_on, Wd, G, MS, KPC, A0, CS, nu_of, FB = [D12[k] for k in (
    "transition", "transition_on", "Wd", "G", "MS", "KPC", "A0", "CS", "nu_of", "FB")]
h_of, dh_of = D12["h_of"], D12["dh_of"]
C_LIGHT = D12["L52"]["c"]
W_M = 0.25; TU = 1 / (2 * W_M)
CS2 = CS["1e6K"] ** 2
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in ("canonical", "alt")]
WINS = [(0.0, 0.5), (0.125, 0.625), (0.25, 0.75), (0.375, 0.875), (0.5, 1.0)]


def layer_fine(z, Mb, foot, N=8000, tlo=0.004, thi=0.996, w=W_M):
    tr = transition(z, Mb, foot, w)
    r, t = tr["r"], tr["t"]
    if not ((t > 0) & (t < 1)).any():
        return None
    ri = float(np.interp(thi, t[::-1], r[::-1])); ro = float(np.interp(tlo, t[::-1], r[::-1]))
    return transition_on(np.geomspace(ri, ro, N), z, Mb, foot, w)


def layer_coeffs(trf, cs2=CS2):
    """local (frozen-background) coefficients of the layer, in eps = delta t units (DE13's convention, A = nu, transverse)."""
    r, t, rho, B = trf["r"], trf["t"], trf["rho_b"], trf["B"]
    _, W1, W2 = Wd(t)
    h = TU * 4 * math.pi * G * nu_of(trf["y"]) / (trf["H"] ** 2 * trf["xce"])
    a = cs2 / (rho * h ** 2)                    # gas modulus in eps units:  E_gas = (1/2) a eps^2
    return dict(r=r, t=t, rho=rho, B=B, W1=W1, W2=W2, h=h, a=a, BW2=B * W2, H=trf["H"], xce=trf["xce"])


def reduced_diag(co, m2=np.inf):
    """diagonal ('base') term of the chi-only reduced quadratic form after eliminating eps (algebraic):
       g_eff - B W'',  g_eff = a m2/(a+m2)   (m2 = inf: g_eff = a, DE13's form (i) with chi = t)."""
    a = co["a"]
    g = a if not np.isfinite(m2) else a * m2 / (a + m2)
    return g - co["BW2"]


def _tri(r, base, mu):
    dr = np.diff(r); rm = 0.5 * (r[1:] + r[:-1])
    wgt = np.zeros_like(r); wgt[1:] += 0.5 * dr; wgt[:-1] += 0.5 * dr
    off = mu * rm ** 2 / dr
    diag = base * r ** 2 * wgt
    diag[1:] += off; diag[:-1] += off
    return diag[1:-1], -off[1:-1], (r ** 2 * wgt)[1:-1]


def lowest_eig_sign(r, base, mu):
    """lowest eigenvalue of the (scaled) tridiagonal form; <0  <=>  a negative mode exists (Sylvester, congruence)."""
    d, e, m = _tri(r, base, mu)
    s = 1.0 / np.sqrt(m)
    ds = d * s * s; es = e * s[:-1] * s[1:]
    return float(eigvalsh_tridiagonal(ds, es, select="i", select_range=(0, 0))[0])


def has_neg(co, base, mu):
    """negative mode inside any of DE13's five half-layer windows (t-width 0.5)."""
    for wn in WINS:
        m = (co["t"] >= wn[0]) & (co["t"] <= wn[1])
        if m.sum() < 5: continue
        if lowest_eig_sign(co["r"][m], base[m], mu) < 0:
            return True
    return False


def mu_min(co, base, lo=-30.0, hi=30.0, iters=60):
    """smallest gradient stiffness mu (J/m, i.e. energy density x length^2, in eps=t units) with no negative half-window mode.
       returns 0 if stable at mu = 0, inf if unstable at 10^hi."""
    if not has_neg(co, base, 0.0): return 0.0
    unit = 1.0
    if has_neg(co, base, 10 ** hi): return np.inf
    l, h = lo, hi
    for _ in range(iters):
        mid = 0.5 * (l + h)
        if has_neg(co, base, 10 ** mid): l = mid
        else: h = mid
    return 10 ** h


# ------------------------------------------------------------------------------------------------ nonlinear chi profile
from scipy.linalg import solve_banded


def chi_energy_parts(r, chi, t, B, mu, m2):
    dr = np.diff(r); rm = 0.5 * (r[1:] + r[:-1])
    wgt = np.zeros_like(r); wgt[1:] += 0.5 * dr; wgt[:-1] += 0.5 * dr
    W, W1, W2 = Wd(chi)
    M = r ** 2 * wgt
    E = np.sum(M * (0.5 * m2 * (chi - t) ** 2 - B * W)) + 0.5 * mu * np.sum(rm ** 2 * np.diff(chi) ** 2 / dr)
    off = mu * rm ** 2 / dr
    g = M * (m2 * (chi - t) - B * W1)
    lap = np.zeros_like(r)
    lap[1:] += off * (chi[1:] - chi[:-1]); lap[:-1] -= off * (chi[1:] - chi[:-1])
    g = g - 0 * lap
    # gradient of gradient-energy:  d/dchi_i = -off_{i-1}(chi_i-chi_{i-1})... written as A chi
    ag = np.zeros_like(r)
    d = np.diff(chi)
    ag[1:] += off * d; ag[:-1] -= off * d
    g = g + ag
    diag = M * (m2 - B * W2)
    diag[1:] += off; diag[:-1] += off
    return E, g, diag, -off, M


def solve_chi(r, t, B, mu, m2, iters=400, tol=1e-7):
    """minimise E[chi] = int r^2 [ mu/2 |chi'|^2 + m2/2 (chi-t)^2 - B W(chi) ]  (Levenberg-damped Newton, tridiagonal).
       converged when the relative residual (|g| over the sum of the absolute terms) < tol everywhere."""
    chi = t.copy()
    E, g, diag, off, M = chi_energy_parts(r, chi, t, B, mu, m2)
    lam = 0.0
    it = 0; res = np.inf
    for it in range(iters):
        for _ in range(60):
            ab = np.zeros((3, len(r)))
            ab[1] = diag + lam * M * (m2 if m2 > 0 else 1.0)
            ab[0, 1:] = off; ab[2, :-1] = off
            try:
                dlt = solve_banded((1, 1), ab, -g)
            except Exception:
                lam = max(2 * lam, 1e-6); continue
            En, gn, dn, on, Mn = chi_energy_parts(r, chi + dlt, t, B, mu, m2)
            if En <= E + 1e-14 * abs(E) and np.all(np.isfinite(dlt)):
                chi = chi + dlt; E, g, diag, off = En, gn, dn, on
                lam = lam / 4 if lam > 1e-12 else 0.0
                break
            lam = max(4 * lam, 1e-4)
        else:
            break
        _, W1c, _ = Wd(chi)
        dch = np.abs(np.diff(chi)); rmid = 0.5 * (r[1:] + r[:-1]); offv = mu * rmid ** 2 / np.diff(r)
        lapabs = np.zeros_like(r); lapabs[1:] += offv * dch; lapabs[:-1] += offv * dch
        scale = np.abs(M * m2 * (chi - t)) + np.abs(M * B * W1c) + lapabs
        res = float(np.max(np.abs(g) / np.maximum(scale, 1e-300)))
        if res < tol: break
    return chi, dict(iters=it, res=res)


def edge_radius(r, x, level=0.5):
    """outermost radius where x crosses `level` going down (x falls outward)."""
    idx = np.where((x[:-1] >= level) & (x[1:] < level))[0]
    if len(idx) == 0: return np.nan
    i = idx[-1]
    f = (x[i] - level) / (x[i] - x[i + 1])
    return float(np.exp(np.log(r[i]) + f * (np.log(r[i + 1]) - np.log(r[i]))))


def layer_stability(z, Mb, foot, mu, m2, use_chi0=True, chi0_cache=None):
    """stability of the chi-sector on one layer at (mu, m2) about the EXACT chi0 profile (not chi0 = t).
       returns (unstable_bool, chi0_full, tr_full)"""
    tr = transition(z, Mb, foot, W_M, amp=True)
    r, t, B = tr["r"], tr["t"], tr["B"]
    if np.isfinite(m2):
        chi0, _ = solve_chi(r, t, B, mu, m2)
    else:
        chi0 = t
    trf = layer_fine(z, Mb, foot)
    co = layer_coeffs(trf)
    c_on_layer = np.exp(np.interp(np.log(co["r"]), np.log(r), np.log(np.maximum(np.abs(chi0), 1e-300)))) * np.sign(np.interp(np.log(co["r"]), np.log(r), chi0))
    chi_l = np.interp(np.log(co["r"]), np.log(r), chi0)
    _, _, W2c = Wd(chi_l)
    base = (co["a"] if not np.isfinite(m2) else co["a"] * m2 / (co["a"] + m2)) - co["B"] * W2c
    return has_neg(co, base, mu), chi0, tr, co, base


# ------------------------------------------------------------------------------------------------ switched stiffness mu(chi)
def smoothstep(x):
    """C^infinity step 0->1 on [0,1] (the same smoothTransition family as the gate W)."""
    x = np.asarray(x, float)
    inside = (x > 0) & (x < 1)
    xx = np.where(inside, x, 0.5)
    ell = np.clip(1 / xx - 1 / (1 - xx), -700, 700)
    v = 1 / (1 + np.exp(ell))
    return np.where(x >= 1, 1.0, np.where(x <= 0, 0.0, v))


class SwitchedStiff:
    """mu(chi) = mu0 * s(chi),  s = 1 for chi <= ca, s_inf for chi >= cb (smooth in between).  psi = int sqrt(s) dchi
       makes the gradient energy canonical:  (mu0/2)|grad psi|^2.  Provides chi(psi), chi_psi = s^-1/2, chi_psipsi = -s'/(2 s^2)."""
    def __init__(self, ca, cb, s_inf, lo=-6.0):
        self.ca, self.cb, self.s_inf = ca, cb, s_inf
        x = np.linspace(lo, cb, 200001)
        s = self.s(x)
        psi = lo + np.concatenate([[0.0], np.cumsum(0.5 * (np.sqrt(s[1:]) + np.sqrt(s[:-1])) * np.diff(x))])
        self.x, self.psi = x, psi
        self.psi_b = psi[-1]; self.lo = lo

    def s(self, chi):
        chi = np.asarray(chi, float)
        return 1.0 - (1.0 - self.s_inf) * smoothstep((chi - self.ca) / (self.cb - self.ca))

    def ds(self, chi, d=1e-6):
        return (self.s(chi + d) - self.s(chi - d)) / (2 * d)

    def chi_of_psi(self, psi):
        psi = np.asarray(psi, float)
        out = np.interp(psi, self.psi, self.x)
        hi = psi > self.psi_b
        out = np.where(hi, self.cb + (psi - self.psi_b) / math.sqrt(self.s_inf), out)
        lo = psi < self.lo
        out = np.where(lo, self.lo + (psi - self.lo), out)
        return out

    def psi_of_chi(self, chi):
        chi = np.asarray(chi, float)
        out = np.interp(chi, self.x, self.psi)
        out = np.where(chi > self.cb, self.psi_b + math.sqrt(self.s_inf) * (chi - self.cb), out)
        out = np.where(chi < self.lo, self.lo + (chi - self.lo), out)
        return out

    def chi_psi(self, chi): return self.s(chi) ** -0.5
    def chi_psipsi(self, chi): return -0.5 * self.ds(chi) * self.s(chi) ** -2


def psi_parts(r, psi, t, B, mu0, m2, S):
    dr = np.diff(r); rm = 0.5 * (r[1:] + r[:-1])
    wgt = np.zeros_like(r); wgt[1:] += 0.5 * dr; wgt[:-1] += 0.5 * dr
    M = r ** 2 * wgt
    chi = S.chi_of_psi(psi)
    W, W1, W2 = Wd(chi)
    cp, cpp = S.chi_psi(chi), S.chi_psipsi(chi)
    E = np.sum(M * (0.5 * m2 * (chi - t) ** 2 - B * W)) + 0.5 * mu0 * np.sum(rm ** 2 * np.diff(psi) ** 2 / dr)
    F1 = m2 * (chi - t) - B * W1
    off = mu0 * rm ** 2 / dr
    d = np.diff(psi)
    ag = np.zeros_like(r); ag[1:] += off * d; ag[:-1] -= off * d
    g = M * F1 * cp + ag
    diag = M * ((m2 - B * W2) * cp ** 2 + F1 * cpp)
    diag[1:] += off; diag[:-1] += off
    return E, g, diag, -off, M, chi, F1


def solve_psi(r, t, B, mu0, m2, S, iters=600, tol=1e-7):
    psi = S.psi_of_chi(t)
    E, g, diag, off, M, chi, F1 = psi_parts(r, psi, t, B, mu0, m2, S)
    lam = 0.0; it = 0; res = np.inf
    for it in range(iters):
        for _ in range(80):
            ab = np.zeros((3, len(r)))
            ab[1] = diag + lam * M * (m2 if m2 > 0 else 1.0)
            ab[0, 1:] = off; ab[2, :-1] = off
            try:
                dlt = solve_banded((1, 1), ab, -g)
            except Exception:
                lam = max(2 * lam, 1e-6); continue
            En = psi_parts(r, psi + dlt, t, B, mu0, m2, S)
            if En[0] <= E + 1e-14 * abs(E) and np.all(np.isfinite(dlt)):
                psi = psi + dlt; E, g, diag, off, M, chi, F1 = En
                lam = lam / 4 if lam > 1e-12 else 0.0
                break
            lam = max(4 * lam, 1e-4)
        else:
            break
        dps = np.abs(np.diff(psi)); rmid = 0.5 * (r[1:] + r[:-1]); offv = mu0 * rmid ** 2 / np.diff(r)
        lapabs = np.zeros_like(r); lapabs[1:] += offv * dps; lapabs[:-1] += offv * dps
        scale = np.abs(M * F1 * S.chi_psi(chi)) + lapabs
        res = float(np.max(np.abs(g) / np.maximum(scale, 1e-300)))
        if res < tol: break
    return psi, chi, dict(iters=it, res=res)


def layer_stability_S(z, Mb, foot, mu0, m2, S):
    tr = transition(z, Mb, foot, W_M, amp=True)
    r, t, B = tr["r"], tr["t"], tr["B"]
    psi, chi0, inf = solve_psi(r, t, B, mu0, m2, S)
    trf = layer_fine(z, Mb, foot)
    co = layer_coeffs(trf)
    lr = np.log(co["r"]); Lr = np.log(r)
    chi_l = np.interp(lr, Lr, chi0)
    F1 = np.interp(lr, Lr, m2 * (chi0 - t) - B * Wd(chi0)[1])
    _, _, W2c = Wd(chi_l)
    cp, cpp = S.chi_psi(chi_l), S.chi_psipsi(chi_l)
    a = co["a"]
    geff = a * m2 / (a + m2) if np.isfinite(m2) else a
    base = cp ** 2 * (geff - co["B"] * W2c) + F1 * cpp
    return has_neg(co, base, mu0), chi0, tr, co, base, inf
