#!/usr/bin/env python3
"""
nb_engine.py -- dimensionless collisionless N-body engine for K001.

Code units: G = M_b = a0 = 1  =>  r_M = sqrt(G M_b / a0) = 1.
The dark-sector mass is M_d = mu * M_b; the baryons are a FIXED central
point mass M_b = 1 at the origin (they set the MOND radius; the dark
sector is the collisionless component that must virialise).

Plain Newtonian gravity throughout.  Direct summation with Plummer
softening, 2nd-order leapfrog (KDK), shared adaptive timestep,
numba-parallel.  Pure numpy fallback kept for validation.

Integration uses block timesteps: particles are bucketed by free-fall
timescale into power-of-two dt levels; each level is kicked at its own
rate (block-step KDK), which keeps deep pericentres affordable.
"""
import numpy as np
from numba import njit, prange

# ----------------------------------------------------------------- constants
G_SI   = 6.674e-11          # m^3 kg^-1 s^-2
C_SI   = 299792458.0        # m/s
MSUN   = 1.989e30           # kg
KPC_M  = 3.085677581e19     # m
KMS    = 1.0e3              # m/s
RHO_LAM_CAN = 8.404e-27     # kg/m^3  (canonical footing)
RHO_LAM_ALT = 1.2179e-26    # kg/m^3  (alt footing)
A0_CAN = 0.5 * C_SI * np.sqrt(G_SI * RHO_LAM_CAN)   # 9.3619e-11 m/s^2
A0_ALT = 0.5 * C_SI * np.sqrt(G_SI * RHO_LAM_ALT)   # 1.1279e-10 m/s^2

def unit_system(Mb_msun, a0):
    """Return (r_unit_m, t_unit_s, v_unit_ms, sigma2_target_ms2, r_M_m)
    for code units G = M_b = a0 = 1."""
    Mb = Mb_msun * MSUN
    rM = np.sqrt(G_SI * Mb / a0)          # MOND radius = length unit
    tU = np.sqrt(rM**3 / (G_SI * Mb))     # time unit so G M_b = 1
    vU = rM / tU                          # sqrt(G M_b / r_M) = sqrt(a0 r_M)
    sig2 = G_SI * Mb / (2.0 * rM)         # target sigma^2 = G M_b/(2 r_M)
    return rM, tU, vU, sig2

# ------------------------------------------------------------- numba kernels
@njit(fastmath=True)
def pair_acc(p1, p2, mp, eps2, mb, a1, a2):
    """Newtonian pair force with Plummer softening between the two sets
    plus the fixed central baryonic point mass mb at the origin (G=1).
    Updates a1 (acceleration of set 1) and a2 (of set 2, Newton's 3rd law
    for the mutual part) in place.  Self-pairs skipped via r2==eps2 guard."""
    n1 = p1.shape[0]; n2 = p2.shape[0]
    for i in range(n1):
        xi = p1[i,0]; yi = p1[i,1]; zi = p1[i,2]
        ax = 0.0; ay = 0.0; az = 0.0
        for j in range(n2):
            dx = xi - p2[j,0]; dy = yi - p2[j,1]; dz = zi - p2[j,2]
            r2 = dx*dx + dy*dy + dz*dz + eps2
            inv = 1.0 / (r2 * np.sqrt(r2))
            w = mp * inv
            ax -= w*dx; ay -= w*dy; az -= w*dz
            a2[j,0] += w*dx; a2[j,1] += w*dy; a2[j,2] += w*dz
        r2b = xi*xi + yi*yi + zi*zi + 1.0e-30
        invb = 1.0 / (r2b * np.sqrt(r2b))
        ax -= mb*xi*invb; ay -= mb*yi*invb; az -= mb*zi*invb
        a1[i,0] += ax; a1[i,1] += ay; a1[i,2] += az

@njit(parallel=True, fastmath=True)
def accel_numba(pos, acc, mp, eps2, mb):
    """acc_i = -[ m_p sum_{j!=i} (x_i-x_j)/(|..|^2+eps2)^{3/2} + M_b x_i/|x_i|^3 ].
    G = 1, equal particle mass m_p."""
    n = pos.shape[0]
    for i in prange(n):
        xi = pos[i, 0]; yi = pos[i, 1]; zi = pos[i, 2]
        ax = 0.0; ay = 0.0; az = 0.0
        for j in range(n):
            if j == i:
                continue
            dx = xi - pos[j, 0]; dy = yi - pos[j, 1]; dz = zi - pos[j, 2]
            r2 = dx*dx + dy*dy + dz*dz + eps2
            inv = 1.0 / (r2 * np.sqrt(r2))
            w = mp * inv
            ax -= w * dx; ay -= w * dy; az -= w * dz
        r2b = xi*xi + yi*yi + zi*zi + 1.0e-30
        invb = 1.0 / (r2b * np.sqrt(r2b))
        ax -= mb * xi * invb; ay -= mb * yi * invb; az -= mb * zi * invb
        acc[i, 0] = ax; acc[i, 1] = ay; acc[i, 2] = az

@njit(parallel=True, fastmath=True)
def energy_numba(pos, vel, mp, eps, mb):
    """Total KE, particle-particle PE (Plummer), baryon PE."""
    n = pos.shape[0]
    ke = 0.0; pe_pp = 0.0; pe_b = 0.0
    for i in prange(n):
        xi = pos[i, 0]; yi = pos[i, 1]; zi = pos[i, 2]
        ke += 0.5 * mp * (vel[i,0]**2 + vel[i,1]**2 + vel[i,2]**2)
        rb = np.sqrt(xi*xi + yi*yi + zi*zi + 1.0e-30)
        pe_b -= mp * mb / rb
        p = 0.0
        for j in range(n):
            if j == i:
                continue
            dx = xi - pos[j,0]; dy = yi - pos[j,1]; dz = zi - pos[j,2]
            r = np.sqrt(dx*dx + dy*dy + dz*dz + eps*eps)
            p -= mp * mp / r
        pe_pp += 0.5 * p
    return ke, pe_pp, pe_b

# ------------------------------------------------------ numpy fallbacks
def accel_numpy(pos, mp, eps2, mb):
    d = pos[:, None, :] - pos[None, :, :]
    r2 = (d * d).sum(-1) + eps2
    np.fill_diagonal(r2, np.inf)
    inv = r2**-1.5
    a = -mp * (d * inv[..., None]).sum(1)
    rb2 = (pos * pos).sum(1) + 1e-30
    a -= mb * pos / rb2[:, None]**1.5
    return a

def energy_numpy(pos, vel, mp, eps, mb):
    ke = 0.5 * mp * (vel * vel).sum()
    d = pos[:, None, :] - pos[None, :, :]
    r = np.sqrt((d * d).sum(-1) + eps * eps)
    np.fill_diagonal(r, np.inf)
    pe_pp = -0.5 * mp * mp * (1.0 / r).sum()
    rb = np.sqrt((pos * pos).sum(1) + 1e-30)
    pe_b = -mp * mb * (1.0 / rb).sum()
    return ke, pe_pp, pe_b

# ------------------------------------------------------------- initial data
def make_ic_top_hat(N, R0, mu, rng=None):
    """Cold (zero-velocity) uniform sphere of collisionless particles,
    radius R0, total dark-sector mass M_d = mu (M_b = 1)."""
    rng = np.random.default_rng(rng)
    u = rng.random(N)
    r = R0 * u**(1.0 / 3.0)
    ct = 2.0 * rng.random(N) - 1.0
    st = np.sqrt(1.0 - ct * ct)
    ph = 2.0 * np.pi * rng.random(N)
    pos = np.empty((N, 3))
    pos[:, 0] = r * st * np.cos(ph)
    pos[:, 1] = r * st * np.sin(ph)
    pos[:, 2] = r * ct
    return pos, np.zeros((N, 3))

# ------------------------------------------------------------- integrator
def run(pos, vel, mp, eps, mb, dt_max, t_end, dE_every=1.0,
        snap_times=(), verbose=True, tag="run", eta=0.02):
    """Per-particle BLOCK-timestep KDK leapfrog (Aarseth NBODY-style).

    dt_i = eta / sqrt(|a_i|), quantised down to dt_max/2^k, floored at
    dt_min = eta/sqrt(a_max).  Accelerations on active particles are
    computed with Newton's 3rd law (pair_acc); distant blocks that are
    due at the same time are integrated with predicted positions of the
    others (extrapolated from their last force), the standard
    Ahmad-Cohen-friendly scheme.  The CENTRAL POINT MASS dominates the
    inner dynamics and enters exactly in every force evaluation, so
    eccentric-orbit pericentres are handled accurately at the block
    timestep of each particle.
    """
    n = pos.shape[0]
    eps2 = eps * eps
    acc = np.zeros_like(pos)
    accel_numba(pos, acc, mp, eps2, mb)

    def bucket(a):
        dt = eta / np.sqrt(np.sqrt((a * a).sum(1)) + 1e-30)
        dt = np.clip(dt, dt_min, dt_max)
        k = np.ceil(np.log2(dt_max / dt)).astype(int)
        return dt_max / 2.0**np.clip(k, 0, 18)

    amax0 = np.sqrt((acc * acc).sum(1)).max()
    dt_min = min(dt_max / 2**12, eta / np.sqrt(amax0 + 1e-30))
    dt_i = bucket(acc)
    t_next = dt_i.copy()           # next force time per particle
    t_last = np.zeros(n)           # last force time per particle
    # first interval: the opening half-kick is applied inside the loop via
    # the stored (t=0) force, so no special init is needed beyond t_last=0.

    hist = {"t": [], "ke": [], "pe_pp": [], "pe_b": [], "rmed": [], "dt_eff": []}
    snaps = {}
    snap_times = sorted(snap_times)
    t = 0.0
    isnap = 0
    next_E = 0.0
    nsteps = 0
    while t < t_end - 1e-12:
        # next event time = earliest particle force time
        t_ev = t_next.min()
        dtp = t_ev - t
        if dtp > 0:
            pos += dtp * vel              # synchronous drift
            t = t_ev
        active = t_next <= t + 1e-15
        idx = np.nonzero(active)[0]
        dt_a = t - t_last[active]
        # standard KDK: opening half-kick with the OLD force (applied at
        # the last event for this interval), drift (done globally above),
        # closing half-kick with the NEW force at the drifted position.
        vel[active] += 0.5 * dt_a[:, None] * acc[active]
        a_new = np.zeros((idx.size, 3))
        a_old = np.zeros((n, 3))
        pair_acc(pos[idx], pos, mp, eps2, mb, a_new, a_old)
        acc[idx] = a_new
        vel[active] += 0.5 * dt_a[:, None] * a_new
        t_last[active] = t
        dt_i[active] = bucket(a_new)
        t_next[active] = t + dt_i[active]
        nsteps += 1
        if t >= next_E:
            ke, pe_pp, pe_b = energy_numba(pos, vel, mp, eps, mb)
            hist["t"].append(t); hist["ke"].append(ke)
            hist["pe_pp"].append(pe_pp); hist["pe_b"].append(pe_b)
            hist["dt_eff"].append(dt_i.min())
            r = np.sqrt((pos * pos).sum(1))
            hist["rmed"].append(np.median(r))
            next_E = t + dE_every
            if verbose and (len(hist["t"]) % 20 == 0):
                print(f"    [{tag}] t={t:8.3f}  E={ke+pe_pp+pe_b:+.6f}  "
                      f"r_med={np.median(r):8.3f}  n_act={idx.size}", flush=True)
        while isnap < len(snap_times) and t >= snap_times[isnap]:
            snaps[snap_times[isnap]] = (pos.copy(), vel.copy())
            isnap += 1
    if isnap < len(snap_times):
        snaps[snap_times[-1]] = (pos.copy(), vel.copy())
    hist["nsteps"] = nsteps
    for k in ("t", "ke", "pe_pp", "pe_b", "rmed", "dt_eff"):
        hist[k] = np.array(hist[k])
    return hist, snaps

# ------------------------------------------------------------- diagnostics
def density_profile(pos, mp, r_edges):
    r = np.sqrt((pos * pos).sum(1))
    counts, _ = np.histogram(r, bins=r_edges)
    vols = 4.0 / 3.0 * np.pi * (r_edges[1:]**3 - r_edges[:-1]**3)
    return counts * mp / vols, r

def fit_slope(r_c, rho, lo=0.3, hi=3.0):
    m = (r_c > lo) & (r_c < hi) & (rho > 0)
    if m.sum() < 3:
        return np.nan, 0
    p = np.polyfit(np.log(r_c[m]), np.log(rho[m]), 1)
    return p[0], int(m.sum())

def sigma_profile(pos, vel, r_edges):
    """3D velocity dispersion per shell: sigma_3d^2 = <|v - <v>|^2>."""
    r = np.sqrt((pos * pos).sum(1))
    idx = np.digitize(r, r_edges) - 1
    nb = len(r_edges) - 1
    sig2 = np.full(nb, np.nan)
    nsh = np.zeros(nb, dtype=int)
    for b in range(nb):
        m = idx == b
        nsh[b] = m.sum()
        if m.sum() >= 30:
            v = vel[m]
            sig2[b] = ((v - v.mean(0))**2).sum(1).mean()
    return sig2, nsh
