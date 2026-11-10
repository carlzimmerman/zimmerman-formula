"""COL1 solver library: Lagrangian thin shells for the clock of action (A), spherical, Newtonian order, gamma_L = 0.

Reduced Lagrangian (FROZEN_CRITERIA.md section 4; checked in col1_system.py):
    L = mu^2 h^2/(2K) + J(|grad h|) - |grad Phi|^2/(2K) - rho_b Phi,   h = -(phi_t + |grad phi|^2/2 + Phi),
    J(s) = (a0^2/K)[s/a0 - ln(1 + s/a0)]  (the Legendre maximum of P.A - W(K|P|), QX17 K0).
Clock charge N = mu^2 h/K + div P on nodes (m_j, conserved). h on the nodes, piecewise linear (hat functions), from the
unique maximiser of U = max_h [sum_j m_j h_j - sum_gaps Int (mu^2 h^2/(2K) + J(|h'|)) dV] with h fixed at the outer node.
Force on node j = +d(sum_gaps G)/dr_j at fixed h (envelope theorem). Gravity: point mass (Plummer eps) + Lagrangian enclosed
clock charge (fixed per node) + background. KDK leapfrog, adaptive step.

Units kpc, km/s, Msun; time unit kpc/(km/s) = 0.977792 Gyr. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import math
import numpy as np
from scipy.linalg import solve_banded
from scipy.integrate import quad

G = 4.30091e-6
K = 4 * math.pi * G
KPC_M = 3.0857e19
TU = 0.977792            # Gyr per kpc/(km/s)
FOOT = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
PI = math.pi


def a0_of(f):
    return FOOT[f] * KPC_M / 1e6


class Law:
    """J(s) with s the signed radial derivative of h. kind: law (action A), off (S = 0, M1), neg (J -> -J, M2),
    flip (P.A -> -P.A, M2a: the Legendre maximum of -P.A - W, evaluated with P = -p Ahat), lin (U(y) -> y, M3)."""

    def __init__(self, a0, kind='law'):
        self.a0, self.kind = a0, kind

    def J(self, s):
        a0, k = self.a0, self.kind
        x = np.abs(s)
        if k == 'off':
            return np.zeros_like(s)
        if k == 'lin':
            return s * s / (2 * K)
        j = (a0 * a0 / K) * (x / a0 - np.log1p(x / a0))
        if k == 'flip':   # -P.A - W at P = -p Ahat, K p = a0 x/(a0 + x): p x - W(K p)
            p = (a0 / K) * x / (a0 + x)
            W = (a0 * a0 / K) * (-K * p / a0 - np.log1p(-K * p / a0))
            return p * x - W
        return -j if k == 'neg' else j

    def Jp(self, s):
        a0, k = self.a0, self.kind
        if k == 'off':
            return np.zeros_like(s)
        if k == 'lin':
            return s / K
        jp = (a0 / K) * s / (a0 + np.abs(s))
        if k == 'flip':   # d/ds of (-P.A - W) at its maximum: -(-P) = the same polarization
            jp = -(-(a0 / K) * s / (a0 + np.abs(s)))
        return -jp if k == 'neg' else jp

    def Jpp(self, s):
        a0, k = self.a0, self.kind
        if k == 'off':
            return np.zeros_like(s)
        if k == 'lin':
            return np.full_like(s, 1 / K)
        jpp = (1 / K) * (a0 / (a0 + np.abs(s))) ** 2
        return -jpp if k == 'neg' else jpp


# Gap 0 = [0, r_1] (the centre): quadratic element h = h0 + (h1 - h0) rho^2, rho = r/r1 (zero slope at the origin;
# a uniform core is exact). Gaps i >= 1: linear elements. Gauss-Legendre in rho for the J integral of gap 0.
_XG, _WG = np.polynomial.legendre.leggauss(32)
RHO = 0.5 * (_XG + 1.0); WQ = 0.5 * _WG
I00, I01, I11 = 8.0 / 105.0, 2.0 / 35.0, 1.0 / 7.0          # Int (1-rho^2)^2 rho^2, (1-rho^2) rho^4, rho^6
V00, V01 = 2.0 / 15.0, 1.0 / 5.0                          # Int (1-rho^2) rho^2, Int rho^4 (hat volumes / 4 pi r1^3)


def lumped_pieces(r):
    """Hat-volume pieces of the linear gaps 1 .. n-2: Ia (node a's share), Ib (node b's share) and their derivatives."""
    a, b = r[1:-1], r[2:]
    D = b - a
    Ia = PI * D * (3 * a * a + 2 * a * b + b * b) / 3
    Ib = PI * D * (a * a + 2 * a * b + 3 * b * b) / 3
    dIa_da = PI * (-(3 * a * a + 2 * a * b + b * b) + D * (6 * a + 2 * b)) / 3
    dIa_db = PI * ((3 * a * a + 2 * a * b + b * b) + D * (2 * a + 2 * b)) / 3
    dIb_da = PI * (-(a * a + 2 * a * b + 3 * b * b) + D * (2 * a + 2 * b)) / 3
    dIb_db = PI * ((a * a + 2 * a * b + 3 * b * b) + D * (2 * a + 6 * b)) / 3
    return Ia, Ib, dIa_da, dIa_db, dIb_da, dIb_db


def gap_geom(r):
    """Linear elements for gaps 1 .. n-2 (between nodes i and i+1, i >= 1)."""
    a, b = r[1:-1], r[2:]
    D = b - a
    Iaa = 2 * PI * D * (6 * a * a + 3 * a * b + b * b) / 15
    Iab = PI * D * (3 * a * a + 4 * a * b + 3 * b * b) / 15
    Ibb = 2 * PI * D * (a * a + 3 * a * b + 6 * b * b) / 15
    V = 4 * PI * (b ** 3 - a ** 3) / 3
    La = PI * D * (3 * a * a + 2 * a * b + b * b) / 3      # lumped shares (A2)
    Lb = PI * D * (a * a + 2 * a * b + 3 * b * b) / 3
    return a, b, D, Iaa, Iab, Ibb, V, La, Lb


def gap0(h0, h1, r1, mu2K, law):
    """Gap 0: quadratic element for J; the mu^2 h^2 term lumped onto the two nodes (A2)."""
    c = 4 * PI * r1 ** 3
    s = 2 * (h1 - h0) * RHO / r1
    Jq, Jpq, Jppq = law.J(s), law.Jp(s), law.Jpp(s)
    dsd = 2 * RHO / r1                                      # ds/dh1 = -ds/dh0
    WJ = (WQ * RHO ** 2 * Jq).sum()
    WJp = (WQ * RHO ** 2 * Jpq * dsd).sum()
    WJpp = (WQ * RHO ** 2 * Jppq * dsd * dsd).sum()
    lump = h0 * h0 * V00 + h1 * h1 * V01
    G0 = 0.5 * mu2K * c * lump + c * WJ
    t0 = mu2K * c * h0 * V00; t1 = mu2K * c * h1 * V01; tj = c * WJp
    H00 = mu2K * c * V00 + c * WJpp; H01 = -c * WJpp; H11 = mu2K * c * V01 + c * WJpp
    dc = 12 * PI * r1 ** 2
    dG_r1 = 0.5 * mu2K * dc * lump + dc * WJ + c * (WQ * RHO ** 2 * Jpq * (-s / r1)).sum()
    return G0, t0, t1, tj, H00, H01, H11, dG_r1


def hat_volumes(r):
    """Int phi_j dV for every node (left part, right part); gap 0 quadratic."""
    a, b, D = r[1:-1], r[2:], r[2:] - r[1:-1]
    Ia = PI * D * (3 * a * a + 2 * a * b + b * b) / 3   # Int phi_a over the gap
    Ib = PI * D * (a * a + 2 * a * b + 3 * b * b) / 3   # Int phi_b over the gap
    left = np.zeros(len(r)); right = np.zeros(len(r))
    left[2:] = Ib; right[1:-1] = Ia
    c = 4 * PI * r[1] ** 3
    right[0] = c * V00; left[1] = c * V01
    return left, right


class HSolveError(RuntimeError):
    pass


def objective(h, m, mu2K, law, geo, r1):
    a, b, D, Iaa, Iab, Ibb, V = geo[:7]
    ha, hb = h[1:-1], h[2:]
    s = (hb - ha) / D
    Gs = 0.5 * mu2K * (ha * ha * geo[7] + hb * hb * geo[8]) + V * law.J(s)
    return Gs.sum() + gap0(h[0], h[1], r1, mu2K, law)[0] - (m * h).sum()


def hsolve(r, m, hb, mu2K, law, h0, tol=1e-11, maxit=80):
    """Stationary point of sum_gaps G - sum m h with h[-1] = hb (a minimum when mu2K >= 0 and J convex).
    Solved in u = h - hb so that differences of h keep full precision."""
    geo = gap_geom(r)
    a, b, D, Iaa, Iab, Ibb, V, La, Lb = geo
    VD = V / D
    n = len(r); r1 = r[1]
    left, right = hat_volumes(r)
    meff = m - mu2K * hb * (left + right)          # charge left after the uniform part mu^2 hb/K
    u = h0 - hb; u[-1] = 0.0
    convex = law.kind not in ('neg',)
    prev_err = np.inf
    for it in range(maxit):
        sl = (u[2:] - u[1:-1]) / D
        jp, jpp = law.Jp(sl), law.Jpp(sl)
        R = np.zeros(n); S = np.abs(m).astype(float)
        ta = mu2K * u[1:-1] * La; tb = mu2K * u[2:] * Lb; tj = VD * jp
        R[1:-1] += ta - tj
        R[2:] += tb + tj
        S[1:-1] += np.abs(ta) + np.abs(tj); S[2:] += np.abs(tb) + np.abs(tj)
        _, g0a, g0b, g0j, H00, H01, H11, _ = gap0(u[0], u[1], r1, mu2K, law)
        R[0] += g0a - g0j; R[1] += g0b + g0j
        S[0] += abs(g0a) + abs(g0j); S[1] += abs(g0b) + abs(g0j)
        R -= meff
        res = R[:-1]
        err = (np.abs(res) / np.maximum(S[:-1], 1e-300)).max()
        if err < tol:
            return u + hb, it, err
        if it > 3 and err < 1e-6 and err >= 0.5 * prev_err:
            return u + hb, it, err          # stalled at round-off
        prev_err = err
        Haa = mu2K * La + VD * jpp / D
        Hab = -VD * jpp / D
        Hbb = mu2K * Lb + VD * jpp / D
        diag = np.zeros(n - 1); off = np.zeros(n - 2)
        diag[0] = H00; diag[1] += H11; off[0] = H01
        diag[1:] += Haa                      # nodes 1 .. n-2 as the a-end of gaps 1 .. n-2
        diag[2:] += Hbb[:-1]                 # nodes 2 .. n-2 as the b-end of gaps 1 .. n-3
        off[1:] = Hab[:-1]                   # couplings (i, i+1), i = 1 .. n-3
        ab = np.zeros((3, n - 1))
        ab[0, 1:] = off; ab[1] = diag; ab[2, :-1] = off
        try:
            du = solve_banded((1, 1), ab, -res, check_finite=False)
        except Exception as e:  # singular
            raise HSolveError(f'banded solve failed: {e}')
        if not np.all(np.isfinite(du)):
            raise HSolveError('non-finite Newton step')
        if convex and err > 1e-4:          # damped Newton far from the solution; full steps near it
            f0 = objective(u, meff, mu2K, law, geo, r1)
            lam = 1.0
            un = u.copy()
            for _ in range(40):
                un[:-1] = u[:-1] + lam * du
                f1 = objective(un, meff, mu2K, law, geo, r1)
                if np.isfinite(f1) and f1 <= f0 + 1e-13 * abs(f0):
                    break
                lam *= 0.5
            u = un
        else:
            u[:-1] = u[:-1] + du
    raise HSolveError(f'Newton did not converge (err {err:.3e})')


def hforce(r, h, mu2K, law):
    """Force on every node: + d(sum_gaps G)/dr_j at fixed h (J on linear elements; mu^2 h^2 lumped, A2)."""
    a, b, D, Iaa, Iab, Ibb, V, La, Lb = gap_geom(r)
    ha, hb = h[1:-1], h[2:]
    s = (hb - ha) / D
    Jv, jp = law.J(s), law.Jp(s)
    _, _, dIa_da, dIa_db, dIb_da, dIb_db = lumped_pieces(r)
    q_da = 0.5 * mu2K * (ha * ha * dIa_da + hb * hb * dIb_da)
    q_db = 0.5 * mu2K * (ha * ha * dIa_db + hb * hb * dIb_db)
    dG_da = q_da - 4 * PI * a * a * Jv + V * jp * s / D
    dG_db = q_db + 4 * PI * b * b * Jv - V * jp * s / D
    F = np.zeros(len(r))
    F[1:-1] += dG_da
    F[2:] += dG_db
    F[1] += gap0(h[0], h[1], r[1], mu2K, law)[7]
    return F


def U_internal(r, h, m, mu2K, law):
    return -objective(h, m, mu2K, law, gap_geom(r), r[1])


def Md_cum(r, h, mu2K):
    """Cumulative static-dust charge (mu^2/K) Int h dV at the nodes (gap 0 quadratic)."""
    a, b, D = r[1:-1], r[2:], r[2:] - r[1:-1]
    Ia = PI * D * (3 * a * a + 2 * a * b + b * b) / 3
    Ib = PI * D * (a * a + 2 * a * b + 3 * b * b) / 3
    g0 = mu2K * 4 * PI * r[1] ** 3 * (h[0] * V00 + h[1] * V01)
    return np.concatenate([[0.0, g0], g0 + np.cumsum(mu2K * (h[1:-1] * Ia + h[2:] * Ib))])


def law_g(gN, a0):
    return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * a0))


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


class Cosmo:
    def __init__(self, h, omega_d, omega_b):
        self.h = h
        self.H0 = 0.1 * h                        # km/s/kpc
        self.Om_d = omega_d / h ** 2
        self.Om_b = omega_b / h ** 2
        self.Om = self.Om_d + self.Om_b
        self.OL = 1 - self.Om
        self.rhoc0 = 3 * self.H0 ** 2 / (8 * PI * G)
        self.nbar0 = self.Om_d * self.rhoc0
        self.rhob0 = self.Om_b * self.rhoc0
        aa = np.logspace(-4, 0.05, 6001)
        Ha = self.H0 * np.sqrt(self.Om * aa ** -3 + self.OL)
        f = 1 / (aa * Ha)
        tt = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(aa))])
        tt += (2.0 / 3.0) / (self.H0 * math.sqrt(self.Om)) * aa[0] ** 1.5    # matter-era start
        self.aa, self.tt = aa, tt
        self.la, self.lt = np.log(aa), np.log(tt)

    def t_of_a(self, a):
        return float(np.exp(np.interp(math.log(a), self.la, self.lt)))

    def a_of_t(self, t):
        return float(np.exp(np.interp(math.log(t), self.lt, self.la)))

    def H_of_a(self, a):
        return self.H0 * math.sqrt(self.Om * a ** -3 + self.OL)


class Model:
    """mode: 'hubble' (primary), 'rest' (Jeans-swindle bracket), 'static' (isolated, outer node fixed, no background)."""

    def __init__(self, mu_Mpc, a0, lawkind, r0, v0, m, Mlag, hb_fn, mode, Mb=0.0, eps=1.0, cosmo=None,
                 ramp=None, rout_fn=None, visc=0.0, nbar_swindle=0.0, gap_ref=None):
        self.mu = mu_Mpc / 1000.0
        self.mu2K = self.mu ** 2 / K
        self.law = Law(a0, lawkind)
        self.a0 = a0
        self.r = r0.astype(float).copy(); self.v = v0.astype(float).copy()
        self.m = m.astype(float); self.Mlag = Mlag.astype(float)
        self.hb_fn, self.mode, self.Mb, self.eps = hb_fn, mode, Mb, eps
        self.cosmo, self.ramp, self.rout_fn, self.visc = cosmo, ramp, rout_fn, visc
        self.nbar_sw = nbar_swindle
        self.gap_ref = gap_ref               # function t -> reference gap array for the caustic test
        self.h = np.full(len(self.r), hb_fn(0.0) if mode != 'hubble' else 0.0)
        self.newton_its = 0; self.nsolve = 0

    def Mb_t(self, t):
        return self.Mb * (1.0 if self.ramp is None else float(smoothstep((t - self.ramp[0]) / self.ramp[1])))

    def accel(self, t, r, v, want=False):
        hb = self.hb_fn(t)
        h, its, err = hsolve(r, self.m, hb, self.mu2K, self.law, self.h)
        self.h = h; self.newton_its += its; self.nsolve += 1
        F = hforce(r, h, self.mu2K, self.law)
        ah = np.zeros_like(r)
        ah[1:-1] = F[1:-1] / self.m[1:-1]
        rr = r[1:-1]
        ag = np.zeros_like(r)
        Mb = self.Mb_t(t)
        ag[1:-1] = -G * Mb * rr / (rr * rr + self.eps ** 2) ** 1.5 - G * self.Mlag[1:-1] / rr ** 2
        if self.mode == 'hubble':
            a = self.cosmo.a_of_t(t)
            ag[1:-1] += (-(4 * PI / 3) * G * self.cosmo.rhob0 * a ** -3 + self.cosmo.OL * self.cosmo.H0 ** 2) * rr
        elif self.mode == 'rest':
            ag[1:-1] += (4 * PI / 3) * G * self.nbar_sw * rr
        av = np.zeros_like(r)
        if self.visc > 0:
            dv = np.diff(v)
            a_, b_ = r[:-1], r[1:]
            Vg = 4 * PI * (b_ ** 3 - a_ ** 3) / 3
            rho = 0.5 * (self.m[:-1] + self.m[1:]) / Vg
            q = np.where(dv < 0, self.visc * rho * dv * dv, 0.0)
            Fv = np.zeros_like(r)
            Fv[:-1] -= 4 * PI * a_ * a_ * q
            Fv[1:] += 4 * PI * b_ * b_ * q
            av[1:-1] = Fv[1:-1] / self.m[1:-1]
        acc = ah + ag + av
        acc[0] = 0.0; acc[-1] = 0.0
        if want:
            return acc, ah, ag, av
        return acc

    def energy(self, t):
        """KE + U + W for the isolated ('static' mode) system (fixed outer node, constant M_b)."""
        r, v, m = self.r, self.v, self.m
        U = U_internal(r, self.h, m, self.mu2K, self.law)
        KE = 0.5 * (m[1:-1] * v[1:-1] ** 2).sum()
        rr = r[1:-1]
        W = -(G * self.Mb_t(t) * m[1:-1] / np.sqrt(rr * rr + self.eps ** 2)).sum() - (G * self.Mlag[1:-1] * m[1:-1] / rr).sum()
        return KE, U, W

    def step_dt(self, acc, dt_max, c=(0.2, 0.2, 0.05)):
        r, v = self.r, self.v
        gap = np.diff(r); dv = np.diff(v)
        with np.errstate(divide='ignore', invalid='ignore'):
            tc = np.where(dv < 0, gap / (-dv), np.inf).min()
            da = np.abs(np.diff(acc))
            ta = np.sqrt(2 * gap / np.maximum(da, 1e-300)).min()
            td = np.sqrt(r[1:-1] / np.maximum(np.abs(acc[1:-1]), 1e-300)).min()
        return min(c[0] * tc, c[1] * ta, c[2] * td, dt_max)

    def caustic(self, t):
        gap = np.diff(self.r)
        ref = self.gap_ref(t)
        bad = np.where(gap <= 1e-6 * ref)[0]
        if len(bad):
            i = bad[0]
            return {'gap_index': int(i), 'r_kpc': float(0.5 * (self.r[i] + self.r[i + 1])), 'gap': float(gap[i])}
        return None

    def run(self, t0, t1, dt_max, snap_every, on_snap=None, fixed_dt=None, max_steps=20_000_000, dt_floor=None):
        t = t0
        acc = self.accel(t, self.r, self.v)
        next_snap = t0
        steps = 0
        event = None
        while True:
            if t >= next_snap - 1e-12:
                if on_snap:
                    on_snap(self, t, acc)
                next_snap += snap_every
            if t >= t1 - 1e-12:
                break
            dt = fixed_dt if fixed_dt else self.step_dt(acc, dt_max)
            dt = min(dt, t1 - t, max(next_snap - t, 1e-12))
            if dt_floor and dt < dt_floor and not fixed_dt:
                event = {'kind': 'STALL', 'reason': 'step below floor (numerical, not a frozen event)', 't': t, 'r_kpc': float(self.r[1]), 'gap0': float(self.r[1])}
                break
            vh = self.v + 0.5 * dt * acc
            rn = self.r + dt * vh
            tn = t + dt
            if self.rout_fn is not None:
                rn[-1] = self.rout_fn(tn)
                vh[-1] = 0.0
            rn[0] = 0.0
            if np.any(np.diff(rn) <= 0):
                self.r = rn
                event = {'kind': 'E1', 'reason': 'shells crossed', 't': tn, **(self.caustic(tn) or {'r_kpc': float(rn[np.argmin(np.diff(rn))])})}
                break
            self.r = rn
            try:
                acc = self.accel(tn, self.r, vh)
            except HSolveError as e:
                gap = np.diff(self.r); ref = self.gap_ref(tn); i = int(np.argmin(gap / ref))
                event = {'kind': 'E2', 'reason': str(e), 't': tn, 'r_kpc': float(0.5 * (self.r[i] + self.r[i + 1])),
                         'gap_index': i, 'min_gap_over_ref': float(gap[i] / ref[i]), 'r_innermost_kpc': float(self.r[1])}
                break
            self.v = vh + 0.5 * dt * acc
            if self.rout_fn is not None:
                self.v[-1] = (self.rout_fn(tn + 1e-6) - self.rout_fn(tn - 1e-6)) / 2e-6 if self.mode == 'hubble' else 0.0
            self.v[0] = 0.0
            t = tn
            steps += 1
            c = self.caustic(t)
            if c:
                event = {'kind': 'E1', 'reason': 'gap below 1e-6 of reference', 't': t, **c}
                break
            if steps >= max_steps:
                event = {'kind': 'STOP', 'reason': 'max steps', 't': t}
                break
        if on_snap and event:
            on_snap(self, t, acc, final=True)
        return t, steps, event


# ---------------- builders ----------------

def log_nodes(Xin, Xout, J):
    """Amendment A1: J log-spaced nodes from Xin to Xout, plus linear nodes inside Xin at the log spacing there
    (spacing Xin * dln), so the centre refines with J. Node 0 is the centre."""
    dln = math.log(Xout / Xin) / (J - 1)
    nlin = max(int(round(1.0 / dln)), 1)
    lin = Xin * np.arange(1, nlin) / nlin
    return np.concatenate([[0.0], lin, np.logspace(math.log10(Xin), math.log10(Xout), J)])


def hubble_model(mu_Mpc, footing, logMb, J, kd1, lawkind='law', Xin=20.0, Xout=8000.0, zi=10.0, eps=1.0,
                 ramp_gyr=1.0, visc=0.0):
    s = kd1['footings'][footing]['setting']
    cos = Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = a0_of(footing)
    X = log_nodes(Xin, Xout, J)
    left, right = hat_volumes(X)
    m = cos.nbar0 * (left + right)          # node 0 (the centre, fixed) carries its hat's charge
    Mlag = cos.nbar0 * (4 * PI / 3) * X ** 3
    ai = 1.0 / (1.0 + zi)
    ti = cos.t_of_a(ai)
    r0 = ai * X
    v0 = cos.H_of_a(ai) * r0
    mu = mu_Mpc / 1000.0
    hb_fn = (lambda t: K * cos.nbar0 * cos.a_of_t(t) ** -3 / mu ** 2) if mu > 0 else (lambda t: 0.0)
    rout = lambda t: cos.a_of_t(t) * X[-1]
    dX = np.diff(X)
    gref = lambda t: cos.a_of_t(t) * dX
    mdl = Model(mu_Mpc, a0, lawkind, r0, v0, m, Mlag, hb_fn, 'hubble', Mb=10 ** logMb, eps=eps, cosmo=cos,
                ramp=(ti, ramp_gyr / TU), rout_fn=rout, visc=visc, gap_ref=gref)
    mdl.h = np.full(len(r0), hb_fn(ti))
    mdl.X = X
    return mdl, ti, cos.t_of_a(1.0), cos


def rest_model(mu_Mpc, footing, logMb, J, kd1, lawkind='law', Xin=20.0, Xout=8000.0, eps=1.0, ramp_gyr=1.0, visc=0.0):
    s = kd1['footings'][footing]['setting']
    cos = Cosmo(s['h'], s['omega_d'], s['omega_b'])
    a0 = a0_of(footing)
    X = log_nodes(Xin, Xout, J)
    left, right = hat_volumes(X)
    m = cos.nbar0 * (left + right)          # node 0 (the centre, fixed) carries its hat's charge
    Mlag = cos.nbar0 * (4 * PI / 3) * X ** 3
    mu = mu_Mpc / 1000.0
    hb = K * cos.nbar0 / mu ** 2
    dX = np.diff(X)
    mdl = Model(mu_Mpc, a0, lawkind, X.copy(), np.zeros_like(X), m, Mlag, lambda t: hb, 'rest', Mb=10 ** logMb, eps=eps,
                ramp=(0.0, ramp_gyr / TU), rout_fn=lambda t: X[-1], visc=visc, nbar_swindle=cos.nbar0,
                gap_ref=lambda t: dX)
    mdl.h = np.full(len(X), hb)
    mdl.X = X
    return mdl, 0.0, 10.0 / TU, cos


def static_law_profile(Mb, a0, mu_Mpc, Rout, hb, eps=1.0, lawkind='law', rmin=1e-3, n=200001):
    """Static clock: h' = -g, g = law(G (M_b(<r) + M_d(<r))/r^2), M_d' = 4 pi r^2 mu^2 h/K; h(Rout) = hb.
    Returns r grid, h, M_N(<r) (charge), M_d(<r). Shooting on h at rmin (bisection on the outer value)."""
    from scipy.integrate import solve_ivp
    mu = mu_Mpc / 1000.0
    r = np.concatenate([[0.0], np.logspace(math.log10(rmin), math.log10(Rout), n)])

    def gfun(gN):
        if lawkind == 'off':
            return gN
        return law_g(gN, a0)

    def Mbr(x):
        return Mb * x ** 3 / (x * x + eps * eps) ** 1.5

    def rhs(lr, y):
        x = math.exp(lr)
        gN = G * (Mbr(x) + y[1]) / x ** 2
        return [-float(gfun(gN)) * x, 4 * PI * x ** 3 * mu * mu * y[0] / K]

    def integ(hc, dense=False):
        sol = solve_ivp(rhs, (math.log(rmin), math.log(Rout)), [hc, 0.0], method='DOP853', rtol=1e-11, atol=1e-9,
                        dense_output=dense)
        return sol

    if mu == 0:
        sol = integ(0.0, True)
        shift = hb - sol.y[0, -1]
    else:
        f = lambda hc: integ(hc).y[0, -1] - hb
        lo, hi = -1e9, 1e9
        flo, fhi = f(lo), f(hi)
        if flo * fhi > 0:
            raise RuntimeError('static profile: no bracket (Jeans feedback; no static state with this boundary)')
        for _ in range(200):
            mid = 0.5 * (lo + hi); fm = f(mid)
            if fm * flo <= 0:
                hi, fhi = mid, fm
            else:
                lo, flo = mid, fm
            if hi - lo < 1e-11 * max(1.0, abs(mid)):
                break
        sol = integ(0.5 * (lo + hi), True); shift = 0.0
    lr = np.log(np.maximum(r, rmin))
    y = sol.sol(lr)
    h = y[0] + shift; Md = y[1]; Md[0] = 0.0
    gN = np.zeros_like(r); gN[1:] = G * (Mbr(r[1:]) + Md[1:]) / r[1:] ** 2
    g = np.zeros_like(r); g[1:] = gfun(gN[1:])
    MN = Md + r * r * (g - gN) / G
    MN[0] = 0.0

    def MNf(x):
        x = np.asarray(x, dtype=float)
        shp = x.shape
        x = x.ravel()
        xs = np.maximum(x, rmin)
        yy = sol.sol(np.log(xs))
        Mdx = yy[1]
        gNx = G * (Mbr(xs) + Mdx) / xs ** 2
        out = Mdx + xs * xs * (gfun(gNx) - gNx) / G
        # below rmin: uniform-core scaling M ~ x^3
        return np.where(x < rmin, out * (x / rmin) ** 3, out).reshape(shp)
    static_law_profile.last_MNf = MNf
    return r, h, MN, Md


def charges_from_profile(Xn, r, MN):
    """Node charges m_j = Int phi_j dM_N (linear hats; gap 0 quadratic: phi_1 = (r/X_1)^2), from a fine profile M_N(r)."""
    dM = np.diff(MN)
    rc = 0.5 * (r[1:] + r[:-1])
    m = np.zeros(len(Xn))
    idx = np.searchsorted(Xn, rc) - 1
    idx = np.clip(idx, 0, len(Xn) - 2)
    a, b = Xn[idx], Xn[idx + 1]
    wb = np.where(idx == 0, (rc / Xn[1]) ** 2, (rc - a) / (b - a))
    np.add.at(m, idx, dM * (1 - wb))
    np.add.at(m, idx + 1, dM * wb)
    return m


_XG16, _WG16 = np.polynomial.legendre.leggauss(16)


def charges_exact(Xn, Mf):
    """m_j = Int phi_j dM for a smooth callable M(r) (vectorised), by parts: Int_a^b phi_b dM = M(b) - (1/D) Int_a^b M dr,
    Int_a^b phi_a dM = -M(a) + (1/D) Int_a^b M dr; gap 0: Int phi_1 dM = M(r1) - Int_0^r1 M 2r/r1^2 dr. Gauss 16 per gap."""
    n = len(Xn)
    m = np.zeros(n)
    a, b = Xn[1:-1], Xn[2:]
    D = b - a
    xq = 0.5 * (a[:, None] + b[:, None]) + 0.5 * D[:, None] * _XG16[None, :]
    IM = 0.5 * D * (Mf(xq) * _WG16[None, :]).sum(axis=1)          # Int_a^b M dr
    Ma, Mb = Mf(a), Mf(b)
    m[1:-1] += -Ma + IM / D
    m[2:] += Mb - IM / D
    r1 = Xn[1]
    xq0 = 0.5 * r1 * (_XG16 + 1)
    I0 = 0.5 * r1 * (Mf(xq0) * 2 * xq0 / r1 ** 2 * _WG16).sum()
    M1 = float(Mf(np.array([r1]))[0])
    m[1] += M1 - I0
    m[0] += I0                                                    # = Int phi_0 dM with phi_0 = 1 - (r/r1)^2
    return m


def enclosed_at_nodes(Xn, r, MN):
    return np.interp(Xn, r, MN)
