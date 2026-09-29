"""CFG154 -- referee of CFG122 (door 4, superfluid dark matter): shared machinery.

Self-contained: nothing is imported from the repository.  Frozen criteria: ../CFG154_FROZEN_CRITERIA.md
(its sha256 is printed at the top of every output).

The model is CFG122's frozen model (zero-temperature Berezhiani-Khoury EFT; static, spherical, non-relativistic):
    X = Y - s,  Y = mu - m Phi,  s = phi'^2/(2m),  P(X) = (2 Lambda (2m)^{3/2}/3) X sqrt|X|,
    n = P'(X) = Lambda (2m)^{3/2} sqrt|X|,  rho_DM = m n,
    Gauss:  n phi' = m alpha Lambda M_b(<r)/(4 pi r^2 M_Pl)   <=>   s |Y - s| = J^2,  J = alpha M_b(<r)/(16 pi m r^2 M_Pl),
    dY/dr = -m G (M_b(<r) + M_DM(<r))/r^2,  tie a0 = N_a alpha^3 Lambda^2/M_Pl (N_a derived in cfg154_headline, S3).
The target (CFG44): rho_c g_tot = a0 M_b(<r)/(4 pi r^3), i.e. w' = a0 r u_N/u, u = u_N + w, u_N = G M_b(<r), w = G M_c(<r).

Two solvers:
  solver B  physical (natural) units; the branch root by brentq; scipy solve_ivp (DOP853).
  solver C  the dimensionless reduction S6 (x = r/r_M, yhat = Y/J_M, mu = M_DM/M_b; only eps = m^2 r_M/(alpha M_Pl)
            enters); closed-form stable roots; vectorised fixed-step RK4 in ln x.
kappa = 1/2 is FITTED; nothing here fits anything.
"""
import hashlib
import json
import math
import os
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('ZF_REPO') or os.path.dirname(os.path.dirname(HERE))
SPEC = os.path.join(REPO, 'campaign_fresh_gravity', 'CFG154_FROZEN_CRITERIA.md')

# ---------------------------------------------------------------- constants (CODATA 2018; IAU 2015 nominal GM_sun)
HBAR = 1.054571817e-34          # J s
C_LIGHT = 2.99792458e8          # m/s
E_CHARGE = 1.602176634e-19      # J per eV
G_SI = 6.67430e-11              # m^3 kg^-1 s^-2
GM_SUN = 1.3271244e20           # m^3 s^-2
M_SUN = GM_SUN / G_SI           # kg
A0 = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}     # m/s^2 (the two footings)
MASSES = [1e9, 1e10, 1e11, 1e12]                     # Msun
GEOMS = [('point', None), ('exp', 0.3), ('exp', 3.0)]  # exp: h / r_M (self-similar spheres, CFG122's G1.2)

L_EV = HBAR * C_LIGHT / E_CHARGE                       # metres per eV^-1
MPL = math.sqrt(HBAR * C_LIGHT / (8 * math.pi * G_SI)) * C_LIGHT ** 2 / E_CHARGE   # reduced Planck mass, eV
G_NAT = 1.0 / (8 * math.pi * MPL ** 2)                # eV^-2 (consistent with G_SI by construction)
MSUN_EV = M_SUN * C_LIGHT ** 2 / E_CHARGE
RHO_NAT_TO_SI = E_CHARGE / (C_LIGHT ** 2 * L_EV ** 3)  # (kg/m^3) per eV^4
ACC_SI_TO_NAT = HBAR / (C_LIGHT * E_CHARGE)            # eV per (m/s^2)

X_EVAL = np.logspace(-1.0, math.log10(30.0), 200)       # CFG122's convention: 200 log points on [0.1, 30]


def r_M_SI(Msun, a0):
    return math.sqrt(GM_SUN * Msun / a0)


def r_M_nat(Msun, a0):
    return r_M_SI(Msun, a0) / L_EV


def eps_of(m, alpha, Msun, a0):
    """eps = m^2 r_M/(alpha M_Pl) (dimensionless; m in eV, r_M in eV^-1)."""
    return m ** 2 * r_M_nat(Msun, a0) / (alpha * MPL)


def lam_tie(alpha, a0, N_a=1.0):
    """Lambda (eV) from a0 = N_a alpha^3 Lambda^2 / M_Pl."""
    return math.sqrt(a0 * ACC_SI_TO_NAT * MPL / (N_a * alpha ** 3))


def P3(s):
    """closed form M_b(<r)/M_b of CFG44's exponential sphere (used ONLY for comparisons, never inside a solver)."""
    return 1.0 - (1.0 + s + 0.5 * s * s) * math.exp(-s)


def P3_series(s):
    """regular-point initial value of the integrated M_b(<r)/M_b at tiny s (Taylor series; s <= 1e-2 only)."""
    return s ** 3 / 6 - s ** 4 / 8 + s ** 5 / 20 - s ** 6 / 72 + s ** 7 / 336


# ---------------------------------------------------------------- reporting
def spec_sha256():
    with open(SPEC, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        f = float(o)
        if math.isnan(f):
            return 'nan'
        if math.isinf(f):
            return 'inf' if f > 0 else '-inf'
        return f
    return o


class Report:
    def __init__(self, slug, mutate=False):
        self.slug, self.mutate = slug, mutate
        self.lines, self.checks, self.nums = [], [], {}
        self.t0 = time.time()
        sha = spec_sha256()
        self.nums['spec_sha256'] = sha
        self.p(f'frozen spec campaign_fresh_gravity/CFG154_FROZEN_CRITERIA.md  sha256 {sha}')
        self.p(f'{slug}  mode = {"MUTATE" if mutate else "main"}')
        self.p(f'constants: M_Pl = {MPL:.6e} eV (reduced, from G), 1 eV^-1 = {L_EV:.9e} m, Msun = {MSUN_EV:.6e} eV, '
               f'1 eV^4 = {RHO_NAT_TO_SI:.6e} kg/m^3')

    def p(self, s=''):
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.p('')
        self.p('=' * 110)
        self.p(s)
        self.p('=' * 110)

    def check(self, name, ok, detail, kind='control'):
        ok = bool(ok)
        self.checks.append({'name': name, 'kind': kind, 'pass': ok, 'detail': detail})
        self.p(f'[{"PASS" if ok else "FAIL"}] ({kind}) {name}: {detail}')
        return ok

    def num(self, k, v):
        self.nums[k] = v

    def write(self, exit_code):
        suffix = '_MUTATE' if self.mutate else ''
        self.p(f'elapsed {time.time() - self.t0:.1f} s; exit code {exit_code}')
        base = os.path.join(HERE, self.slug + suffix)
        with open(base + '.out', 'w') as f:
            f.write('\n'.join(self.lines) + '\n')
        with open(base + '_results.json', 'w') as f:
            json.dump({'slug': self.slug, 'mode': 'MUTATE' if self.mutate else 'main', 'exit_code': exit_code,
                       'checks': self.checks, 'numbers': clean(self.nums)}, f, indent=1)


# ---------------------------------------------------------------- the target (CFG44), integrated in SI
def target(Msun, geom, a0, x_eval=X_EVAL, x_dense=None, rtol=1e-12, x_in=1e-4, x_out=40.0):
    """Integrate w' = a0 r u_N/(u_N + w) and u_N' = 4 pi G r^2 rho_b in t = ln(r/m), state scaled by GM.
    rho_c is taken from the closure at the integrated w: rho_c = a0 u_N/(4 pi G r u).  Returns SI arrays."""
    kind, hq = geom
    GM = GM_SUN * Msun
    rM = math.sqrt(GM / a0)
    h = None if kind == 'point' else hq * rM

    def rhs(t, q):
        r = math.exp(t)
        uN, w = q
        duN = 0.0 if kind == 'point' else 0.5 * (r / h) ** 3 * math.exp(-r / h)
        dw = a0 * r * r * uN / (GM * (uN + w))
        return [duN, dw]

    r_in = x_in * rM
    if kind == 'point':
        q0 = [1.0, x_in ** 2 / 2 - x_in ** 4 / 8]
    else:
        s = r_in / h
        q0 = [P3_series(s), math.sqrt(a0 * r_in ** 5 / (15.0 * GM * h ** 3))]
    sol = solve_ivp(rhs, [math.log(r_in), math.log(x_out * rM)], q0, method='DOP853', rtol=rtol, atol=1e-30,
                    dense_output=True)
    if not sol.success:
        raise RuntimeError('target integration failed: ' + sol.message)

    def fields(xs):
        r = np.asarray(xs) * rM
        uN, w = sol.sol(np.log(r))
        uN, w = uN * GM, w * GM
        u = uN + w
        return {'x': np.asarray(xs), 'r': r, 'uN': uN, 'w': w, 'Mb': uN / G_SI, 'Mc': w / G_SI,
                'rho_c': a0 * uN / (4 * math.pi * G_SI * r * u), 'g_tot': u / r ** 2, 'g_N': uN / r ** 2}

    out = fields(x_eval)
    if x_dense is not None:
        out['dense'] = fields(x_dense)
    out['rM'] = rM
    return out


# ---------------------------------------------------------------- solver B: physical (natural) units
class SolverB:
    """Masses in eV, lengths in eV^-1, Y in eV.  State (scaled): [M_b(<r)/Ms, M_DM(<r)/Ms, Y/Ys] against t = ln r."""

    def __init__(self, m, alpha, Lam, Mb_sun, geom, a0, branch, flux=True, selfgrav=True):
        self.m, self.alpha, self.Lam = m, alpha, Lam
        self.kind, hq = geom
        self.Mb = Mb_sun * MSUN_EV if Mb_sun else 0.0
        self.rM = r_M_nat(Mb_sun, a0) if Mb_sun else None
        self.h = hq * self.rM if self.kind == 'exp' else None
        self.branch, self.flux, self.selfgrav = branch, flux, selfgrav
        self.nfac = Lam * (2 * m) ** 1.5              # n = nfac sqrt|X|
        self.Ms, self.Ys = 1.0, 1.0

    def J(self, r, Mb_enc):
        if (not self.flux) or Mb_enc <= 0.0:
            return 0.0
        return self.alpha * Mb_enc / (16 * math.pi * self.m * r * r * MPL)

    def roots(self, Y, J):
        """(|X|, s) on the chosen branch by bracketed root finding; None where a B+ root does not exist.
        FIRSTRUN fix (disclosed): for Y < 0 the first draft bracketed z = |X| on [-Y, -Y + J], and -Y + J rounds to -Y
        once |Y|/J > ~1e16 (brentq then saw no sign change).  It now solves for s on [0, J] (no cancellation)."""
        if self.branch == 'B-':
            if J == 0.0:
                return max(-Y, 0.0), max(Y, 0.0)
            if Y >= 0.0:                               # z = |X| in [0, J]:  z (z + Y) = J^2,  s = Y + z
                z = brentq(lambda z: z * (z + Y) - J * J, 0.0, J, xtol=1e-300, rtol=1e-15, maxiter=500)
                return z, Y + z
            s = brentq(lambda s: s * (s - Y) - J * J, 0.0, J, xtol=1e-300, rtol=1e-15, maxiter=500)
            return s - Y, s                            # Y < 0:  s (s + |Y|) = J^2,  |X| = |Y| + s
        if Y <= 0.0 or Y < 2.0 * J:                    # X > 0 branches need Y >= 2J
            return None
        if J == 0.0:
            return (Y, 0.0) if self.branch == 'B+a' else (0.0, Y)
        g = lambda v: v * (Y - v) - J * J              # v = X in (0, Y)
        if self.branch == 'B+a':
            v = brentq(g, 0.5 * Y, Y, xtol=1e-300, rtol=1e-15, maxiter=500)
        else:
            v = brentq(g, 0.0, 0.5 * Y, xtol=1e-300, rtol=1e-15, maxiter=500)
        return v, Y - v

    def absX(self, Y, J):
        rt = self.roots(Y, J)
        return None if rt is None else rt[0]

    def unpack(self, t, q):
        r = math.exp(t)
        Mb_enc = q[0] * self.Ms if self.kind == 'exp' else self.Mb
        return r, Mb_enc, q[1] * self.Ms, q[2] * self.Ys

    def rhs(self, t, q):
        r, Mb_enc, Mdm, Y = self.unpack(t, q)
        J = self.J(r, Mb_enc)
        ax = self.absX(Y, J)
        if ax is None:                                  # at/after a B+ fold: continuous clamp; the event stops the run
            ax = max(0.5 * Y, 0.0)
        rho = self.m * self.nfac * math.sqrt(ax)
        dMb = 0.0
        if self.kind == 'exp':
            dMb = 4 * math.pi * r ** 3 * self.Mb * math.exp(-r / self.h) / (8 * math.pi * self.h ** 3)
        dMdm = 4 * math.pi * r ** 3 * rho
        dY = -self.m * G_NAT * ((Mb_enc + Mdm) if self.selfgrav else Mb_enc) / r
        return [dMb / self.Ms, dMdm / self.Ms, dY / self.Ys]

    def fold(self, t, q):
        r, Mb_enc, Mdm, Y = self.unpack(t, q)
        return Y - 2.0 * self.J(r, Mb_enc)

    def solve(self, r_start, Y_start, Mdm_start, r_eval, r_stop, rtol=1e-10, Ys=None, Ms=None):
        self.Ys = Ys if Ys else (abs(Y_start) if Y_start != 0.0 else 1.0)
        self.Ms = Ms if Ms else (self.Mb if self.Mb > 0 else 1.0)
        Mb0 = self.Mb * P3_series(r_start / self.h) if self.kind == 'exp' else self.Mb
        q0 = [Mb0 / self.Ms, Mdm_start / self.Ms, Y_start / self.Ys]
        events = None
        if self.branch != 'B-':
            ev = self.fold
            ev.__func__.terminal = True
            ev.__func__.direction = -1
            events = ev
        t_eval = np.log(np.asarray(r_eval, float))
        sol = solve_ivp(self.rhs, [math.log(r_start), math.log(r_stop)], q0, method='DOP853', t_eval=t_eval,
                        rtol=rtol, atol=[1e-22, 1e-22, 1e-14], events=events)
        if sol.status == -1:
            raise RuntimeError('solver B failed: ' + sol.message)
        n_ok = sol.y.shape[1]
        out = {k: np.full(len(t_eval), np.nan) for k in ('Mb', 'Mdm', 'Y', 'J', 'absX', 's', 'rho')}
        for i in range(n_ok):
            r, Mb_enc, Mdm, Y = self.unpack(sol.t[i], sol.y[:, i])
            J = self.J(r, Mb_enc)
            rt = self.roots(Y, J)
            if rt is None:
                n_ok = i
                break
            ax, s_ = rt
            out['Mb'][i], out['Mdm'][i], out['Y'][i], out['J'][i] = Mb_enc, Mdm, Y, J
            out['absX'][i], out['s'][i] = ax, s_
            out['rho'][i] = self.m * self.nfac * math.sqrt(ax)
        out['n_ok'] = n_ok
        out['r_edge'] = (math.exp(sol.t_events[0][0]) if (events is not None and len(sol.t_events[0]) > 0)
                         else np.inf)
        out['Mdm_edge'] = (sol.y_events[0][0][1] * self.Ms if (events is not None and len(sol.t_events[0]) > 0)
                           else np.nan)
        out['rho_SI'] = out['rho'] * RHO_NAT_TO_SI
        return out


def phi_b_minus(Mb_eV, geom, r, rM):
    """-Phi_b(r) (dimensionless, Phi_b(inf) = 0) of the baryons in natural units."""
    kind, hq = geom
    if kind == 'point':
        return G_NAT * Mb_eV / r
    h = hq * rM
    s = r / h
    return G_NAT * Mb_eV * (P3(s) / r + (r + h) * math.exp(-s) / (2 * h * h))


# ---------------------------------------------------------------- solver C: the dimensionless reduction (point mass)
NSUB = 6


def xnodes(nsub=NSUB):
    k = np.arange(199 * nsub + 1)
    return 0.1 * 300.0 ** (k / (199 * nsub))


def absxhat(yh, jh, branch):
    """closed-form stable roots of s|Y - s| = J^2 in units of J_M; returns (|xhat|, root-exists mask)."""
    if branch == 'B-':
        d = np.sqrt(yh * yh + 4.0 * jh * jh)
        pos = yh >= 0
        ax = np.where(pos, 2.0 * jh * jh / np.where(pos, d + yh, 1.0), 0.5 * (d - yh))
        return ax, np.ones(np.shape(yh), dtype=bool)
    ok = yh >= 2.0 * jh
    d = np.sqrt(np.where(ok, yh * yh - 4.0 * jh * jh, 0.0))
    if branch == 'B+a':
        ax = 0.5 * (yh + d)
    else:
        ax = 2.0 * jh * jh / np.where(ok, yh + d, 1.0)
    return np.where(ok, ax, np.nan), ok


def solver_C(eps, y0, branch, mu0=0.0, nsub=NSUB, fake=None, keep_eval=False, keep_full=False):
    """Vectorised RK4 in t = ln x from x = 0.1 to 30 for the point mass:
         dyhat/dt = -2 eps (1 + mu)/x,   dmu/dt = eps x^3 sqrt|xhat|,   R = eps x sqrt(1+x^2) sqrt|xhat|  (jhat = 1/x^2).
    E = max over the evaluation nodes in [0.1, min(30, x_edge)] of |R/fake - 1| (fake = 1: the CFG44 target);
    E = inf if x_edge < 3 (CFG122's coverage rule)."""
    eps = np.asarray(eps, float)
    y = np.array(y0, float, copy=True)
    N = y.size
    mu = np.full(N, float(mu0))
    xs = xnodes(nsub)
    h = math.log(xs[1] / xs[0])
    alive = np.ones(N, bool)
    xedge = np.full(N, np.inf)
    E = np.zeros(N)
    Rev = np.full((N, 200), np.nan) if keep_eval else None
    Rfull = np.full((N, xs.size), np.nan) if keep_full else None

    def deriv(x, yv, muv):
        ax, ok = absxhat(yv, 1.0 / (x * x), branch)
        return -2.0 * eps * (1.0 + muv) / x, eps * x ** 3 * np.sqrt(np.where(ok, ax, 0.0)), ok

    def record(k):
        x = xs[k]
        ax, ok = absxhat(y, 1.0 / (x * x), branch)
        newly = alive & ~ok
        xedge[newly] = xs[k - 1] if k > 0 else xs[0] * 0.999
        alive[:] = alive & ok
        R = eps * x * math.sqrt(1.0 + x * x) * np.sqrt(np.where(ok, ax, 0.0))
        if keep_full:
            Rfull[:, k] = np.where(alive, R, np.nan)
        if k % nsub == 0:
            j = k // nsub
            Rr = R / (fake[j] if fake is not None else 1.0)
            np.maximum(E, np.where(alive, np.abs(Rr - 1.0), 0.0), out=E)
            if keep_eval:
                Rev[:, j] = np.where(alive, R, np.nan)

    record(0)
    for k in range(xs.size - 1):
        x0, x1 = xs[k], xs[k + 1]
        xm = x0 * math.exp(0.5 * h)
        k1y, k1m, o1 = deriv(x0, y, mu)
        k2y, k2m, o2 = deriv(xm, y + 0.5 * h * k1y, mu + 0.5 * h * k1m)
        k3y, k3m, o3 = deriv(xm, y + 0.5 * h * k2y, mu + 0.5 * h * k2m)
        k4y, k4m, o4 = deriv(x1, y + h * k3y, mu + h * k3m)
        ok = o1 & o2 & o3 & o4
        newly = alive & ~ok
        xedge[newly] = x0
        alive &= ok
        y = np.where(alive, y + h / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y), y)
        mu = np.where(alive, mu + h / 6.0 * (k1m + 2 * k2m + 2 * k3m + k4m), mu)
        record(k + 1)
    E = np.where(xedge < 3.0, np.inf, E)
    return {'E': E, 'xedge': xedge, 'Rev': Rev, 'Rfull': Rfull, 'xs': xs, 'mu_end': mu, 'y_end': y}


# ---------------------------------------------------------------- the two-stage search over yhat(0.1)
GRID = np.concatenate([-(10.0 ** (np.arange(110, -41, -1) / 10.0)), [0.0], 10.0 ** (np.arange(-40, 111) / 10.0)])
BRANCHES = ('B-', 'B+a', 'B+b')


def local_minima(Erow, nmax=3):
    n = len(Erow)
    idx = []
    for i in range(n):
        if not np.isfinite(Erow[i]):
            continue
        left = Erow[i - 1] if i > 0 else np.inf
        right = Erow[i + 1] if i < n - 1 else np.inf
        if Erow[i] <= left and Erow[i] <= right:
            idx.append(i)
    idx.sort(key=lambda i: (Erow[i], i))
    return idx[:nmax]


def refine_points(i):
    lo = GRID[max(i - 1, 0)]
    hi = GRID[min(i + 1, len(GRID) - 1)]
    if lo != 0.0 and hi != 0.0 and np.sign(lo) == np.sign(hi):
        return np.sign(lo) * np.logspace(math.log10(abs(lo)), math.log10(abs(hi)), 41)
    return np.linspace(lo, hi, 41)


def search(eps_list, mu0=0.0, fake=None, nsub=NSUB, branches=BRANCHES):
    """E*(eps): the lowest E over the grid (stage 1) and the refinements (stage 2), per branch and overall."""
    eps_list = np.asarray(eps_list, float)
    N, G = eps_list.size, GRID.size
    res = {'eps': eps_list, 'branch': {}}
    for b in branches:
        c1 = solver_C(np.repeat(eps_list, G), np.tile(GRID, N), b, mu0=mu0, nsub=nsub, fake=fake)
        E1 = c1['E'].reshape(N, G)
        e_list, y_list, owner = [], [], []
        for i in range(N):
            for jmin in local_minima(E1[i]):
                pts = refine_points(jmin)
                e_list.append(np.full(pts.size, eps_list[i]))
                y_list.append(pts)
                owner.append(np.full(pts.size, i))
        best_E = E1.min(axis=1)
        best_y = GRID[np.argmin(E1, axis=1)]
        if e_list:
            ee, yy, ow = np.concatenate(e_list), np.concatenate(y_list), np.concatenate(owner)
            c2 = solver_C(ee, yy, b, mu0=mu0, nsub=nsub, fake=fake)
            for i in range(N):
                sel = ow == i
                if sel.any():
                    j = np.argmin(c2['E'][sel])
                    if c2['E'][sel][j] < best_E[i]:
                        best_E[i] = c2['E'][sel][j]
                        best_y[i] = yy[sel][j]
        res['branch'][b] = {'E1': E1, 'best_E': best_E, 'best_y': best_y}
    allE = np.vstack([res['branch'][b]['best_E'] for b in branches])
    k = np.argmin(allE, axis=0)
    res['best_E'] = allE[k, np.arange(N)]
    res['best_branch'] = [branches[i] for i in k]
    res['best_y'] = np.array([res['branch'][branches[k[i]]]['best_y'][i] for i in range(N)])
    return res


# ---------------------------------------------------------------- Lane-Emden integrator (the RK4 routine of C, in xi)
def le_rk4(n, xi_max, hstep=1e-3, xi0=1e-3, xi_out=None):
    """theta'' + (2/xi) theta' + theta^n = 0, series start at xi0; fixed-step RK4 in xi to xi_max.
    theta^n uses the real power (n = 0, 1, 5 are analytic through theta = 0; n = 1/2 is run only where theta > 0).
    Returns theta at xi_out (linear-in-step Hermite-free: xi_out must be multiples of hstep from xi0) and the arrays."""
    def f(xi, th, dth):
        if n == 0:
            src = np.ones_like(th)
        elif n == 0.5:
            src = np.sqrt(th)
        else:
            src = th ** n
        return dth, -src - 2.0 * dth / xi

    th = 1 - xi0 ** 2 / 6 + n * xi0 ** 4 / 120
    dth = -xi0 / 3 + n * xi0 ** 3 / 30
    nsteps = int(round((xi_max - xi0) / hstep))
    xis = xi0 + hstep * np.arange(nsteps + 1)
    TH = np.empty(nsteps + 1)
    DTH = np.empty(nsteps + 1)
    TH[0], DTH[0] = th, dth
    for k in range(nsteps):
        xi = xis[k]
        a1, b1 = f(xi, th, dth)
        a2, b2 = f(xi + hstep / 2, th + hstep / 2 * a1, dth + hstep / 2 * b1)
        a3, b3 = f(xi + hstep / 2, th + hstep / 2 * a2, dth + hstep / 2 * b2)
        a4, b4 = f(xi + hstep, th + hstep * a3, dth + hstep * b3)
        th = th + hstep / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        dth = dth + hstep / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
        TH[k + 1], DTH[k + 1] = th, dth
    return xis, TH, DTH


def le_half_edge_rk4(xi_s, th_s, dth_s, nsteps=20000):
    """n = 1/2 near the surface: u = sqrt(theta), v = u_s - u in [0, u_s]; state (xi, p = theta') is smooth in v:
       dxi/dv = -2u/p,  dp/dv = (u + 2p/xi)(2u/p).  RK4 to v = u_s gives xi_1 and theta'(xi_1)."""
    u_s = math.sqrt(th_s)
    hv = u_s / nsteps

    def g(v, xi, p):
        u = u_s - v
        return -2 * u / p, (u + 2 * p / xi) * (2 * u / p)

    xi, p, v = xi_s, dth_s, 0.0
    for _ in range(nsteps):
        a1, b1 = g(v, xi, p)
        a2, b2 = g(v + hv / 2, xi + hv / 2 * a1, p + hv / 2 * b1)
        a3, b3 = g(v + hv / 2, xi + hv / 2 * a2, p + hv / 2 * b2)
        a4, b4 = g(v + hv, xi + hv * a3, p + hv * b3)
        xi += hv / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        p += hv / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
        v += hv
    return xi, p
