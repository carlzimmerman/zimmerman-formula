#!/usr/bin/env python3
"""AKS1 model library: spherical multi-stream clock-dust shells with an acceleration-keyed drag (FROZEN_CRITERIA.md s. 2-4).

Candidate: action (A) without W and P (GR + clock dust F(Q) = mu_K^2 (Q-1)^2/(4K) + baryons), plus Galley's in-in drag
Gamma(A) = (a0/c) f(|A|/a0) on the clock's velocity relative to the static (Kodama) frame, open budget.
Per shell j:  r'' = g_j + A_p(r_j) - Gamma_j r'.  g_j: Plummer point mass (ramped), sorted enclosed clock charge,
uniform cosmic baryon background, Lambda.  A_p = -(K/mu_K^2) d rho_N/dr: the n = 1 pressure of the dust (its 4-acceleration
once W and P are removed).  Strang split: exact exponential drag half-steps around a KDK leapfrog.

Units kpc, km/s, Msun; time unit kpc/(km/s) = 0.977792 Gyr.  Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, time
import numpy as np
from scipy.ndimage import gaussian_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
G = 4.30091e-6
K = 4 * math.pi * G
KPC_M = 3.0857e19
TU = 0.977792                       # Gyr per kpc/(km/s)
CKMS = 299792.458
FOOT = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
MU_J = 2.512e4                      # per Mpc: CMB-lensing Jeans line (KD1 G9a, MK1)
MU_W = {'canonical': 198.25, 'alt': 198.24}   # per Mpc: KD1's w <= 0.01 at z 3400
LAMBDA_382 = 0.028                  # CFG382's c-free settling constant
RS = 0.3
EPS = 1.0
KD1 = json.load(open(os.path.join(HERE, '../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json')))
PI = math.pi


def a0_of(f):
    return FOOT[f] * KPC_M / 1e6


def setting(f):
    return KD1['footings'][f]['setting']


def smoothstep(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


class Cosmo:
    """Flat matter + Lambda (the COL1/FLD1 background). omega_d, omega_b physical densities."""

    def __init__(self, h, omega_d, omega_b, eds=False):
        self.h = h
        self.H0 = 0.1 * h                                   # km/s/kpc
        if eds:
            self.Om_d, self.Om_b = 1.0, 0.0
        else:
            self.Om_d, self.Om_b = omega_d / h ** 2, omega_b / h ** 2
        self.Om = self.Om_d + self.Om_b
        self.OL = 1 - self.Om
        self.rhoc0 = 3 * self.H0 ** 2 / (8 * PI * G)
        self.nbar0 = self.Om_d * self.rhoc0
        self.rhob0 = self.Om_b * self.rhoc0
        aa = np.logspace(-4, 0.05, 6001)
        Ha = self.H0 * np.sqrt(self.Om * aa ** -3 + self.OL)
        f = 1 / (aa * Ha)
        tt = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(aa))])
        tt += (2.0 / 3.0) / (self.H0 * math.sqrt(self.Om)) * aa[0] ** 1.5
        self.la, self.lt = np.log(aa), np.log(tt)

    def t_of_a(self, a):
        return float(np.exp(np.interp(math.log(a), self.la, self.lt)))

    def a_of_t(self, t):
        return float(np.exp(np.interp(math.log(t), self.lt, self.la)))

    def H_of_a(self, a):
        return self.H0 * math.sqrt(self.Om * a ** -3 + self.OL)


def cosmo_of(f, eds=False):
    s = setting(f)
    return Cosmo(s['h'], s['omega_d'], s['omega_b'], eds=eds)


def target_edge(f, Mb):
    """CFG461's edge with KD1's share: g_e* = ln^2(1/(1-f_b)) a0, r_e* = sqrt(G M_b/g_e*)."""
    s = setting(f)
    fb = s['omega_b'] / (s['omega_b'] + s['omega_d'])
    ge = math.log(1 / (1 - fb)) ** 2 * a0_of(f)
    return ge, math.sqrt(G * Mb / ge)


# profile bins (FROZEN s. 4): 20 per decade from 1 kpc to 10^3.7 kpc
PEDGES = 10 ** (np.arange(75) * 0.05)
PCEN = np.sqrt(PEDGES[1:] * PEDGES[:-1])
PVOL = (4 * PI / 3) * (PEDGES[1:] ** 3 - PEDGES[:-1] ** 3)


def profile(snaps, dm, Mb):
    """Time-averaged profile over snapshots [(r, v), ...]."""
    nb = len(PCEN); ns = len(snaps)
    cnt = np.zeros(nb); sm = np.zeros(nb); smv = np.zeros(nb); smv2 = np.zeros(nb); Menc = np.zeros(nb)
    for r, v in snaps:
        idx = np.searchsorted(PEDGES, r) - 1
        ok = (idx >= 0) & (idx < nb)
        cnt += np.bincount(idx[ok], minlength=nb)
        sm += np.bincount(idx[ok], weights=dm[ok], minlength=nb)
        smv += np.bincount(idx[ok], weights=(dm * v)[ok], minlength=nb)
        smv2 += np.bincount(idx[ok], weights=(dm * v * v)[ok], minlength=nb)
        o = np.argsort(r); cm = np.cumsum(dm[o])
        Menc += np.interp(PCEN, r[o], cm, left=0.0)
    with np.errstate(invalid='ignore', divide='ignore'):
        rho = sm / ns / PVOL
        vm = smv / sm
        sig = np.sqrt(np.maximum(smv2 / sm - vm * vm, 0.0))
    Menc /= ns
    vc = np.sqrt(G * (Mb + Menc) / PCEN)
    return {'r': PCEN.tolist(), 'count': cnt.tolist(), 'rho': rho.tolist(), 'vmean': vm.tolist(), 'sigma_r': sig.tolist(),
            'vc': vc.tolist(), 'Menc': Menc.tolist()}


class Binned:
    """n = 1 pressure (and the binned density used by the c-free key) from the shells' total density."""

    def __init__(self, nper=30, smooth=1.5):
        self.nper, self.smooth = nper, smooth

    def __call__(self, r, dm, rmax_ok):
        lo = math.log10(0.03); hi = math.log10(max(rmax_ok, 0.1))
        nb = max(int(math.ceil((hi - lo) * self.nper)), 4)
        e = 10 ** (lo + np.arange(nb + 1) / self.nper)
        m, _ = np.histogram(r, bins=e, weights=dm)
        rho = m / ((4 * PI / 3) * (e[1:] ** 3 - e[:-1] ** 3))
        rho_s = gaussian_filter1d(rho, self.smooth, mode='nearest')
        cen = np.sqrt(e[1:] * e[:-1])
        drho = np.gradient(rho_s, cen)
        return cen, rho_s, drho, float((e[1:] - e[:-1]).min())


def run(footing, lM, key='P', N=2000, mu_Mpc=None, C=1.0, fshape='x', cfac=1.0, zi=10.0, homogeneous=False,
        snap_path=None, eds=False, Ms_seed=None, Xlo=0.03, Xhi=15.0, ramp_gyr=1.0, rs=RS, tmax_gyr=None,
        static=None, verbose=False, dtfac=1.0, reflect='ecorr', nsnap=51, snap_dt_gyr=0.01):
    """One row. key: 'A' (A_p-keyed, P), 'gpec' (as-if-standing |g_pec|), 'rho' (c-free MU2), 'off' (MU1).
    fshape 'x' or 'x2'; C the coefficient; cfac the c-test factor (c -> cfac c, a0 -> cfac a0, a0/c fixed).
    static: dict for KA5 (no cosmology): {'Mb':..., 'Mc':..., 'r1':..., 'r2':..., 'T_gyr':...}.
    A1: reflect='ecorr' (energy-consistent centre reflection; 'mirror' = the frozen pre-A1 rule); nsnap 51 at 0.01 Gyr
    (pre-A1: 11 at 0.05 Gyr); dtfac scales the 0.02 / 0.05 step factors (1 = frozen)."""
    a0 = a0_of(footing)
    T0 = time.time()
    mu = (MU_J if mu_Mpc is None else mu_Mpc) / 1000.0           # per kpc
    pressure_on = (mu_Mpc != 0) and static is None and not eds
    k_over_mu2 = K / mu ** 2 if pressure_on else 0.0
    binned = Binned()
    if static is not None:
        cos = None
        Mb = static['Mb']
        rr = np.logspace(math.log10(static['r1']), math.log10(static['r2']), N + 1)
        m_sh = (4 * PI / 3) * (rr[1:] ** 3 - rr[:-1] ** 3)
        dm = static['Mc'] * m_sh / m_sh.sum()
        r = np.sqrt(rr[1:] * rr[:-1]).copy(); v = np.zeros(N)
        X = r.copy(); MX = np.cumsum(dm)
        ti, tend = 0.0, static['T_gyr'] / TU
    else:
        cos = cosmo_of(footing, eds=eds)
        Mb = 0.0 if homogeneous else (Ms_seed if eds else 10 ** lM)
        Mscale = Ms_seed if eds else 10 ** lM
        XM = (Mscale / ((4 * PI / 3) * cos.nbar0)) ** (1 / 3)
        X = np.logspace(math.log10(Xlo * XM), math.log10(Xhi * XM), N)
        MX = (4 * PI / 3) * cos.nbar0 * X ** 3
        dm = np.diff(np.concatenate([[0.0], MX]))
        ai = 1 / (1 + zi); ti = cos.t_of_a(ai); tend = cos.t_of_a(1.0)
        r = X * ai; v = cos.H_of_a(ai) * r
    if tmax_gyr is not None:
        tend = ti + tmax_gyr / TU
    ramp = None if (eds or static is not None) else ramp_gyr / TU
    rmax_ok_idx = max(N - 50, 1)
    order_lag = np.arange(N)

    def background(t):
        if static is not None:
            return 0.0, 0.0, 1.0
        a = cos.a_of_t(t)
        return (-(4 * PI / 3) * G * cos.rhob0 * a ** -3 + cos.OL * cos.H0 ** 2), \
               (-(4 * PI / 3) * G * (cos.nbar0 + cos.rhob0) * a ** -3 + cos.OL * cos.H0 ** 2), a

    def nbar(t):
        if static is not None:
            return 0.0
        return cos.nbar0 * cos.a_of_t(t) ** -3

    def forces(t, r):
        Mt = Mb if ramp is None else Mb * smoothstep((t - ti) / ramp)
        o = np.argsort(r, kind='stable')
        cs = np.cumsum(dm[o])
        Menc = np.empty(N); Menc[o] = cs                    # strictly inside + own (uniform -> exact Hubble)
        bb, bH, a = background(t)
        g = -G * Mt * r / (r * r + EPS * EPS) ** 1.5 - G * Menc / r ** 2 + bb * r
        gpec = g - bH * r
        Ap = np.zeros(N); rho_at = None; cs_max = 0.0; dr_min = 1.0
        if pressure_on or key == 'rho':
            rmax_ok = 0.95 * np.sort(r)[rmax_ok_idx - 1]
            cen, rho_s, drho, dr_min = binned(r, dm, rmax_ok)
            inside = r <= cen[-1]
            if pressure_on:
                Ap[inside] = np.interp(r[inside], cen, -k_over_mu2 * drho)
                cs_max = math.sqrt(k_over_mu2 * max(rho_s.max(), 0.0))
            if key == 'rho':
                rho_at = np.zeros(N); rho_at[inside] = np.interp(r[inside], cen, rho_s)
        return g, gpec, Ap, rho_at, cs_max, dr_min, Menc

    def phi_shell(t, rr, idx, rho_q):
        """A1: potential of shells idx at radii rho_q in the field of all OTHER shells at rr (sorted), the Plummer
        baryons and the smooth background (-g_bg r^2/2)."""
        Mt = Mb if ramp is None else Mb * smoothstep((t - ti) / ramp)
        o = np.argsort(rr, kind='stable'); rs = rr[o]; ms = dm[o]
        cm = np.concatenate([[0.0], np.cumsum(ms)])
        ro = np.concatenate([np.cumsum((ms / rs)[::-1])[::-1], [0.0]])
        k = np.searchsorted(rs, rho_q, side='left')
        Mlt = cm[k]; Sout = ro[k]
        own_in = rr[idx] < rho_q
        Mlt = Mlt - np.where(own_in, dm[idx], 0.0)
        Sout = Sout - np.where(own_in, 0.0, dm[idx] / rr[idx])
        bb, bH, a = background(t)
        return -G * (Mlt + dm[idx]) / rho_q - G * Sout - G * Mt / np.sqrt(rho_q * rho_q + EPS * EPS) - 0.5 * bb * rho_q * rho_q

    def gamma(t, gpec, Ap, rho_at):
        if key == 'off':
            return np.zeros(N)
        if key == 'rho':
            return LAMBDA_382 * np.sqrt(K * np.maximum(rho_at - nbar(t), 0.0))
        Aabs = np.abs(Ap) if key == 'A' else np.abs(gpec)
        x = Aabs / (cfac * a0)
        fx = x if fshape == 'x' else x * x
        return C * (a0 / CKMS) * fx                          # a0/c unchanged under the c-test (cfac)

    t = ti
    g, gpec, Ap, rho_at, cs_max, dr_min, Menc = forces(t, r)
    acc = g + Ap
    Gam = gamma(t, gpec, Ap, rho_at)
    Ediss = np.zeros(N); Pdiss = np.zeros(N); NG = np.zeros(N); maxA = np.abs(Ap).copy()
    crossed = np.zeros(N, bool); t_first_cross = None; t_first_centre = None
    snaps = []; snap_times = [tend - (snap_dt_gyr * (nsnap - 1) - snap_dt_gyr * k) / TU for k in range(nsnap)]
    snap_times = [s for s in snap_times if s > ti]
    si = 0
    series = []; next_series = ti
    E_hist = []
    nsteps = 0

    def energy():
        o = np.argsort(r, kind='stable'); cs = np.cumsum(dm[o]); Mi = np.empty(N); Mi[o] = cs
        W = -np.sum(G * dm * Mi / r) - np.sum(G * Mb * dm / np.sqrt(r * r + EPS * EPS))
        return float(0.5 * np.sum(dm * v * v) + W)

    E0 = energy() if static is not None else None
    while t < tend - 1e-12:
        dt = min(dtfac * 0.02 * np.min(r / np.maximum(np.abs(v), 1e-3)), dtfac * 0.05 * np.min(np.sqrt(r / np.maximum(np.abs(acc), 1e-12))),
                 1e-3, tend - t)
        if cs_max > 0:
            dt = min(dt, 0.3 * dr_min / cs_max)
        if si < len(snap_times) and snap_times[si] > t:
            dt = min(dt, snap_times[si] - t)
        dt = max(dt, 1e-12)
        # drag half-step
        fac = np.exp(-Gam * 0.5 * dt)
        vb = v; v = v * fac
        Ediss += 0.5 * dm * (vb * vb - v * v); Pdiss += dm * (vb - v); NG += Gam * 0.5 * dt
        # KDK
        r_prev = r.copy(); v_prev = v.copy()
        vh = v + 0.5 * dt * acc
        rn = r + dt * vh
        hit = rn < rs
        if hit.any():
            rn[hit] = 2 * rs - rn[hit]; vh[hit] = np.abs(vh[hit])
            if t_first_centre is None:
                t_first_centre = (t + dt - ti) * TU
        t += dt; r = rn
        g, gpec, Ap, rho_at, cs_max, dr_min, Menc = forces(t, r)
        acc = g + Ap
        v = vh + 0.5 * dt * acc
        if reflect == 'ecorr' and hit.any():          # A1: energy-consistent centre reflection
            idx = np.where(hit)[0]
            ph_old = phi_shell(t, r, idx, r_prev[idx]); ph_new = phi_shell(t, r, idx, r[idx])
            ke = v_prev[idx] ** 2 - 2 * (ph_new - ph_old)
            ok = ke >= 0
            v[idx[ok]] = np.sqrt(ke[ok])
            bad = idx[~ok]
            if len(bad):
                r[bad] = r_prev[bad]; v[bad] = np.abs(v_prev[bad])
                g, gpec, Ap, rho_at, cs_max, dr_min, Menc = forces(t, r); acc = g + Ap
        Gam = gamma(t, gpec, Ap, rho_at)
        fac = np.exp(-Gam * 0.5 * dt)
        vb = v; v = v * fac
        Ediss += 0.5 * dm * (vb * vb - v * v); Pdiss += dm * (vb - v); NG += Gam * 0.5 * dt
        maxA = np.maximum(maxA, np.abs(Ap))
        nsteps += 1
        inv = np.where(np.diff(r) <= 0)[0]
        if len(inv):
            crossed[inv] = True; crossed[inv + 1] = True
            if t_first_cross is None:
                t_first_cross = (t - ti) * TU
        if si < len(snap_times) and t >= snap_times[si] - 1e-12:
            snaps.append((r.copy(), v.copy())); si += 1
        if t >= next_series or t >= tend - 1e-12:
            rf = float(r[crossed].max()) if crossed.any() else 0.0
            fall = v <= 0
            series.append([(t - ti) * TU, (1 / cos.a_of_t(t) - 1) if cos is not None else None, rf,
                           float(r[fall].max()) if fall.any() else 0.0, float(Ediss.sum()), float(np.median(NG))])
            next_series += 0.1 / TU
            if static is not None:
                E_hist.append([(t - ti) * TU, energy(), float(Ediss.sum())])
        if verbose and nsteps % 200000 == 0:
            print(f'  {footing} {lM} {key}: t {(t - ti) * TU:.3f} Gyr, steps {nsteps}, {time.time() - T0:.0f}s', flush=True)
    out = {'A1': {'reflect': reflect, 'nsnap': nsnap, 'snap_dt_gyr': snap_dt_gyr, 'dtfac': dtfac},
           'footing': footing, 'logMb': lM, 'key': key, 'N': N, 'mu_Mpc': (MU_J if mu_Mpc is None else mu_Mpc), 'C': C,
           'fshape': fshape, 'cfac': cfac, 'zi': zi, 'homogeneous': homogeneous, 'eds': eds, 'Mb': Mb,
           'steps': nsteps, 'wall_s': time.time() - T0, 't_first_cross_gyr': t_first_cross,
           't_first_centre_gyr': t_first_centre, 'series_cols': ['t_gyr', 'z', 'R_fold', 'R_ta', 'Ediss_total', 'NG_median'],
           'series': series, 'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
    out['_r'] = r; out['_v'] = v; out['_X'] = X; out['_MX'] = MX; out['_dm'] = dm; out['_NG'] = NG; out['_Ediss'] = Ediss
    out['_Pdiss'] = Pdiss; out['_maxA'] = maxA; out['_snaps'] = snaps; out['_crossed'] = crossed
    if cos is not None:
        out['a_end'] = cos.a_of_t(t)
    if static is not None:
        out['E0'] = E0; out['E_hist'] = E_hist
    if snap_path:
        np.savez_compressed(snap_path, r=np.array([s[0] for s in snaps], np.float32),
                            v=np.array([s[1] for s in snaps], np.float32), X=X, dm=dm, NG=NG, Ediss=Ediss)
    return out


def summarize(o, footing, lM):
    """Grading inputs for a galaxy row (FROZEN s. 4), small enough for JSON."""
    Mb = 10 ** lM; a0 = a0_of(footing)
    s = setting(footing)
    Mc = s['omega_d'] / s['omega_b'] * Mb
    ge, re = target_edge(footing, Mb)
    dm, r, NG, Ed, Pd, MX = o['_dm'], o['_r'], o['_NG'], o['_Ediss'], o['_Pdiss'], o['_MX']
    prof = profile(o['_snaps'], dm, Mb)
    inMc = MX <= Mc * (1 + 1e-12)
    near = (r >= 0.8 * re) & (r <= 1.25 * re)
    S = {'profile': prof, 'r_e_star': re, 'g_e_star': ge, 'M_c': Mc,
         'Ediss_total': float(Ed.sum()), 'Ediss_Mc': float(Ed[inMc].sum()), 'Pdiss_total': float(Pd.sum()),
         'Pdiss_Mc': float(Pd[inMc].sum()), 'n_near_edge': int(near.sum()),
         'NG_median_near_edge': float(np.median(NG[near])) if near.any() else None,
         'NG_max': float(NG.max()), 'NG_median': float(np.median(NG)),
         'maxA_over_a0_max': float(o['_maxA'].max() / a0), 'maxA_over_a0_median': float(np.median(o['_maxA']) / a0),
         'charge_t0_over_start_minus_1': float(dm.sum() / o['_MX'][-1] - 1.0),
         'R_fold_end': o['series'][-1][2], 'R_ta_end': o['series'][-1][3]}
    return S
