#!/usr/bin/env python3
"""CFG637 library: DERIVE the radial profile of the UNSETTLED cold-energy reservoir from the framework itself (FROZEN_CRITERIA.md).

Method A (primary): spherical self-similar secondary infall (Fillmore-Goldreich / Bertschinger type) of the catchment's matter
in the framework's own background (flat, cold energy behaves as cold matter outside bound systems, w = -1, so a0 is flat).
  * Every Lagrangian shell carries baryons + cold energy at the cosmic ratio until it turns around (candidate B's switch selects
    the turnaround ball, CFG557 D1). At turnaround the shell's RETAINED baryons (f_ret of its baryons) join the condensed core,
    whose z_obs shape is the observed system's baryon profile, grown self-similarly (amplitude = retained baryons turned around so
    far, radius scaled with r_ta(t)). Non-retained baryons stay on the shell (diffuse, they gravitate, never drawn).
  * Settled cold energy (R1) = the law's round phantom (R6) of the SOURCE baryons of the core (all baryons: candidate B;
    condensed only: H-CB), truncated at the supply edge (R2: where M_ph(<r) reaches the cold energy turned around so far) and
    confined to the turnaround ball. It is DRAWN (R5) from the cold weight of turned-around shells located between the edge and
    r_ta (fallback when the edge lies at/after r_ta: uniform draw from all turned-around cold weight; counted and reported).
  * The reservoir = the remaining cold weight of turned-around shells. It is collisionless and moves in the TOTAL Newtonian
    potential of real mass (G9): baryons (core + diffuse) + settled cold energy + reservoir itself + not-yet-turned shells + the
    Lambda term. No extra phantom force acts on it: under G9 the law's extra pull IS the settled cold energy's mass.
  * Angular momentum (INHERITED bracket, as CFG118): at turnaround j^2 = 2 G M(<r) r q/(1+q) (point-mass pericentre q r_ta).
  * Seed perturbation (INHERITED context, from the initial power-spectrum shape): delta_i(M) = delta0 (M/M_ta)^-eps, capped at
    DELTA_CAP; delta0 calibrated so the catchment shell M_ta turns around at a_obs (single-shell, pre-crossing).
  * Read-out at a_obs: phase-mixed M_res(<r) from each reservoir shell's (E, j) in the final potential (time fraction inside r);
    the time-averaged snapshot binning over the last 1 Gyr is reported as a numerical cross-check.
Method B (secondary): maximum-entropy (non-degenerate Lynden-Bell = lowered Maxwell-Boltzmann, Woolley) F(E) of the reservoir
  in the same total potential, bounded at r_ta (E < Phi(r_ta)), mass = Method A's reservoir mass, temperature fixed by the energy
  the infall delivered (Method A's total reservoir energy in the final potential). Self-consistent Poisson including itself.

Units: kpc, Msun, Gyr. Background constants as cfg557_lib (h 0.6736, omega_b 0.02237, omega_c 0.1200; INHERITED context).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import math
import numpy as np

G = 4.49850215e-6                       # kpc^3 Gyr^-2 Msun^-1
KMS = 1.0227121650537077                # km/s -> kpc/Gyr
SI_TO_KPCGYR2 = (3.15576e16 ** 2) / 3.0857e19
h = 0.6736; OM_B, OM_C = 0.02237, 0.1200
OM = (OM_B + OM_C) / h ** 2; OL = 1.0 - OM; FB = OM_B / (OM_B + OM_C); COLD_PER_B = (1 - FB) / FB
H0 = 100 * h * KMS / 1000.0             # 1/Gyr
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G)
DELTA_CAP = 0.3
A_INIT = 0.02


def t_of_a(a):
    return 2.0 / (3 * H0 * math.sqrt(OL)) * np.arcsinh(np.sqrt(OL / OM) * np.asarray(a, float) ** 1.5)


def a_of_t(t):
    return (OM / OL) ** (1 / 3) * np.sinh(1.5 * H0 * math.sqrt(OL) * np.asarray(t, float)) ** (2 / 3)


def H_of_a(a):
    return H0 * np.sqrt(OM / np.asarray(a, float) ** 3 + OL)


def nu_exp(y):
    s = np.sqrt(np.maximum(y, 1e-300))
    return np.where(s > 1e-8, 1.0 / (-np.expm1(-s)), 1.0 / np.maximum(s, 1e-300))


def initial_shell(M, delta):
    rhom = OM * RHOC0 / A_INIT ** 3
    r = (3 * M / (4 * math.pi * rhom * (1 + delta))) ** (1 / 3)
    v = H_of_a(A_INIT) * r * (1 - delta / 3.0)
    return r, v


def single_shell_ta(M, delta):
    """time of turnaround of an isolated shell (no crossing), leapfrog in t; returns a_ta."""
    r, v = initial_shell(M, delta)
    t = float(t_of_a(A_INIT)); tend = float(t_of_a(3.0))
    dt = 1e-3 * t
    acc = lambda rr: -G * M / rr ** 2 + OL * H0 ** 2 * rr
    while t < tend:
        dt = min(2e-3 * math.sqrt(r ** 3 / (G * M)), 0.002 * t + 1e-6)
        v2 = v + 0.5 * dt * acc(r); r2 = r + dt * v2; v2 = v2 + 0.5 * dt * acc(r2)
        if v2 <= 0:
            f = v / (v - v2)
            single_shell_ta.r_ta = r + f * (r2 - r)
            return float(a_of_t(t + f * dt))
        r, v, t = r2, v2, t + dt
    return float("inf")


def calibrate_delta0(M_ta, a_obs):
    lo, hi = 1e-4, 0.5
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        if single_shell_ta(M_ta, mid) > a_obs:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def phantom_trunc(x, Msrc, rta, a0, nu, supply):
    """law phantom of the source inside r = x r_ta, truncated at the supply edge, confined to the turnaround ball.
    returns (Mph(<x), x_edge or None)."""
    r = x * rta
    gN = G * np.maximum(Msrc, 0) / np.maximum(r, 1e-6) ** 2
    mph = np.where(Msrc > 0, (nu(gN / a0) - 1.0) * Msrc, 0.0)
    mph = np.maximum.accumulate(mph)
    xe = None
    k = np.where(mph >= supply)[0]
    if len(k):
        mph = np.where(np.arange(len(x)) > k[0], mph[k[0]], mph); xe = float(x[k[0]])
    kt = np.searchsorted(x, 1.0)
    mph = np.where(x > 1.0, mph[min(kt, len(x) - 1)], mph)
    return mph, xe


class Infall:
    """one derivation run (Method A) for one system."""

    def __init__(self, M_ta, fret, x_core, S_core, S_src, a0, nu, a_obs=1.0, eps=1.0, q=0.1, N=1600, selfgrav=True,
                 m_frac_lo=1e-3, m_frac_hi=3.0, C_dyn=0.03, soft=2e-3, avg_gyr=1.0, draw_mode="outer", delta0=None):
        self.M_ta, self.fret, self.a0, self.nu, self.a_obs = M_ta, fret, a0, nu, a_obs
        self.eps, self.q, self.selfgrav = eps, q, selfgrav
        self.x_core, self.S_core, self.S_src = x_core, S_core, S_src      # cumulative shapes, -> fractions at x_core (r / r_ta)
        Mk = M_ta * np.geomspace(m_frac_lo, m_frac_hi, N)
        dm = np.diff(np.r_[0.0, Mk])
        self.draw_mode = draw_mode
        self.delta0 = calibrate_delta0(M_ta, a_obs) if delta0 is None else delta0
        delta = np.minimum(self.delta0 * (Mk / M_ta) ** (-eps), DELTA_CAP)
        r, v = initial_shell(Mk, delta)
        self.r, self.v, self.dm, self.Mk = r, v, dm, Mk
        self.m_cold = dm * (1 - FB); self.m_bret = dm * FB * fret; self.m_bdiff = dm * FB * (1 - fret)
        self.turned = np.zeros(N, bool); self.j2 = np.zeros(N)
        self.drawn = 0.0; self.fallback_steps = 0; self.draw_short = 0.0
        self.C_dyn, self.soft_x, self.avg_gyr = C_dyn, soft, avg_gyr
        self.rta0_guess = None

    # ---------------- core + settled cumulative mass at radii r (time t)
    def core_set(self, r, rta, Mret_turned, cold_turned, draw=True):
        xg = self.x_core
        Mc = Mret_turned * self.S_core
        Ms = Mret_turned * self.S_src
        mph, xe = phantom_trunc(xg, Ms, rta, self.a0, self.nu, cold_turned)
        target = float(mph[-1])
        return Mc, mph, target, xe

    def run(self):
        t = float(t_of_a(A_INIT)); t_obs = float(t_of_a(self.a_obs))
        N = len(self.r); avgM = None; avg_w = 0.0
        self.rgrid_avg = None
        nstep = 0
        rta = None
        while t < t_obs:
            # ---- state-dependent quantities
            tt = self.turned
            if tt.any():
                k_last = np.max(np.where(tt)[0]); rta = float(self.r[k_last])
            Mret_t = float(self.m_bret[tt].sum()); cold_t = float((self.dm[tt] * (1 - FB)).sum())
            acc, Menc = self._accel(rta, Mret_t, cold_t, draw=True)
            if nstep == 0:
                self._acc = acc
            # time step
            rr = np.sqrt(self.r ** 2 + (self.soft_x * (rta if rta else self.r[-1])) ** 2)
            tdyn = np.sqrt(rr ** 3 / (G * np.maximum(Menc, 1e-30)))
            sel = self.r > 0.004 * (rta if rta else 0.0)
            dt = min(self.C_dyn * float(np.min(tdyn[sel])), 0.01 * t, t_obs - t)
            # KDK
            self.v += 0.5 * dt * acc
            self.r = np.abs(self.r + dt * self.v)
            t += dt
            acc2, Menc = self._accel(rta, Mret_t, cold_t, draw=False)
            self.v += 0.5 * dt * acc2
            # turnaround detection
            new = (~self.turned) & (self.v <= 0)
            if new.any():
                self.turned |= new
                self.j2[new] = 2 * G * Menc[new] * self.r[new] * self.q / (1 + self.q)
            # time-averaged snapshot (last avg_gyr)
            if t_obs - t < self.avg_gyr and rta:
                if avgM is None:
                    self.rgrid_avg = np.geomspace(1e-3, 3.0, 300) * rta
                    avgM = np.zeros_like(self.rgrid_avg)
                res = self.turned & (self.m_cold > 0)
                if res.any():
                    o = np.argsort(self.r[res]); cr = np.cumsum(self.m_cold[res][o])
                    avgM += dt * np.interp(self.rgrid_avg, self.r[res][o], cr, left=0.0)
                avg_w += dt
            nstep += 1
        self.nstep = nstep
        self.t_obs = t_obs
        tt = self.turned
        k_last = np.max(np.where(tt)[0]); self.rta = float(self.r[k_last])
        self.M_turned = float(self.dm[tt].sum())
        self.M_res_avg = avgM / avg_w if avg_w > 0 else None
        Mret_t = float(self.m_bret[tt].sum()); cold_t = float((self.dm[tt] * (1 - FB)).sum())
        self.Mret_t, self.cold_t = Mret_t, cold_t
        Mc, mph, target, xe = self.core_set(None, self.rta, Mret_t, cold_t)
        self.settle_target, self.x_edge = target, xe
        self.supply_turned = cold_t
        return self

    def _accel(self, rta, Mret_t, cold_t, draw):
        r = self.r
        if rta is not None:
            Mc, mph, target, xe = self.core_set(r, rta, Mret_t, cold_t)
            if draw and target > self.drawn:
                dS = target - self.drawn
                re = (xe if xe is not None else 1.0) * rta
                if xe is not None and xe < 1.0:
                    # R5: uniform draw from the cold weight of turned-around shells between the edge and r_ta
                    elig = self.turned & (self.m_cold > 0) & (r >= re) & (r <= rta * 1.0000001)
                    avail = float(self.m_cold[elig].sum())
                    take = min(dS, avail)
                    if avail > 0:
                        self.m_cold[elig] *= (1 - take / avail)
                else:
                    # edge at/after r_ta: the R5 shell is empty; its continuous limit (r_e -> r_ta) is outer-first
                    self.fallback_steps += 1
                    elig = np.where(self.turned & (self.m_cold > 0))[0]
                    if self.draw_mode == "uniform":
                        avail = float(self.m_cold[elig].sum()); take = min(dS, avail)
                        if avail > 0:
                            self.m_cold[elig] *= (1 - take / avail)
                    else:
                        o = elig[np.argsort(-r[elig])]
                        cm = np.cumsum(self.m_cold[o]); avail = float(cm[-1]) if len(cm) else 0.0
                        take = min(dS, avail)
                        if take > 0:
                            kf = int(np.searchsorted(cm, take))
                            prev = cm[kf - 1] if kf > 0 else 0.0
                            self.m_cold[o[:kf]] = 0.0
                            if kf < len(o):
                                self.m_cold[o[kf]] -= (take - prev)
                self.drawn += take
                if take < dS:
                    self.draw_short = max(self.draw_short, (dS - take) / max(target, 1e-30))
            fset = min(1.0, self.drawn / target) if target > 0 else 0.0
            Mfix = np.interp(r / rta, self.x_core, Mc + fset * mph, left=0.0)
        else:
            Mfix = np.zeros_like(r)
        mg = np.where(self.turned, self.m_bdiff + (self.m_cold if self.selfgrav else 0.0), self.dm)
        o = np.argsort(r); cs = np.cumsum(mg[o]) - 0.5 * mg[o]
        Msh = np.empty_like(r); Msh[o] = cs
        Menc = Msh + Mfix
        s = self.soft_x * (rta if rta else 0.0)
        acc = -G * Menc * r / (r ** 2 + s ** 2) ** 1.5 + OL * H0 ** 2 * r + self.j2 / np.maximum(r, 1e-6) ** 3
        return acc, Menc

    # ---------------- final-state potential and phase-mixed reservoir
    def final_profile(self, nr=500, ntheta=160):
        rta = self.rta
        rg = np.geomspace(1e-3, 4.0, nr) * rta
        Mc, mph, target, xe = self.core_set(None, rta, self.Mret_t, self.cold_t)
        fset = min(1.0, self.drawn / target) if target > 0 else 0.0
        Mfix = np.interp(rg / rta, self.x_core, Mc + fset * mph, left=0.0)
        self.M_core_g = np.interp(rg / rta, self.x_core, Mc, left=0.0)
        self.M_set_g = np.interp(rg / rta, self.x_core, fset * mph, left=0.0)
        mg = np.where(self.turned, self.m_bdiff + self.m_cold, self.dm)
        o = np.argsort(self.r)
        Msh = np.interp(rg, self.r[o], np.cumsum(mg[o]), left=0.0)
        Mtot = Mfix + Msh
        g = G * Mtot / rg ** 2 - OL * H0 ** 2 * rg
        # Phi(r) = -int_r^inf g ; beyond the grid: point mass + Lambda
        Phi = np.zeros(nr)
        Phi[-1] = -G * Mtot[-1] / rg[-1] - 0.5 * OL * H0 ** 2 * rg[-1] ** 2
        seg = 0.5 * (g[1:] + g[:-1]) * np.diff(rg)
        Phi[:-1] = Phi[-1] - np.cumsum(seg[::-1])[::-1]
        self.rg, self.Mtot_g, self.Phi_g = rg, Mtot, Phi
        res = np.where(self.turned & (self.m_cold > 0))[0]
        lrg = np.log(rg)
        Mres = np.zeros(nr); Etot = 0.0
        th = (np.arange(ntheta) + 0.5) / ntheta * math.pi
        for i in res:
            ri, vi, j2, m = self.r[i], self.v[i], self.j2[i], self.m_cold[i]
            Pe = np.interp(np.log(max(ri, rg[0])), lrg, Phi) + 0.5 * j2 / ri ** 2
            E = 0.5 * vi ** 2 + Pe
            Etot += m * (0.5 * vi ** 2 + 0.5 * j2 / ri ** 2 + np.interp(np.log(max(ri, rg[0])), lrg, Phi))
            f = E - (Phi + 0.5 * j2 / rg ** 2)
            ki = int(np.searchsorted(rg, ri))
            ki = min(max(ki, 1), nr - 1)
            below = np.where(f[:ki] < 0)[0]
            above = np.where(f[ki:] < 0)[0]
            if len(below):
                k = below[-1]; rp = rg[k] + (rg[k + 1] - rg[k]) * (-f[k]) / (f[k + 1] - f[k])
            else:
                rp = rg[0]
            if len(above):
                k = ki + above[0] - 1; ra = rg[k] + (rg[k + 1] - rg[k]) * f[k] / (f[k] - f[k + 1])
            else:
                ra = rg[-1]
            ra = max(ra, ri); rp = min(rp, ri)
            rr = rp + (ra - rp) * 0.5 * (1 - np.cos(th))
            ff = np.maximum(E - (np.interp(np.log(rr), lrg, Phi) + 0.5 * j2 / rr ** 2), 0.0)
            vr = np.sqrt(2 * ff)
            drdth = (ra - rp) * 0.5 * np.sin(th)
            w = np.where(vr > 0, drdth / np.maximum(vr, 1e-30), 0.0)
            if w.sum() <= 0:
                Mres += m * (rg >= ri); continue
            cw = np.cumsum(w) / w.sum()
            Mres += m * np.interp(rg, rr, cw, left=0.0, right=1.0)
        self.M_res_g = Mres
        self.E_res = Etot
        self.M_res_tot = float(self.m_cold[res].sum())
        return self

    def summary(self):
        return dict(M_ta=self.M_ta, delta0=self.delta0, eps=self.eps, q=self.q, selfgrav=self.selfgrav, a_obs=self.a_obs,
                    r_ta_kpc=self.rta, M_turned_over_Mta=self.M_turned / self.M_ta, settled_target=self.settle_target,
                    settled_drawn=self.drawn, reservoir_total=self.M_res_tot, supply_turned=self.supply_turned,
                    x_edge=self.x_edge, fallback_steps=self.fallback_steps, draw_short_max=self.draw_short, nstep=self.nstep)


def maxent_reservoir(rg, Mfix, Mres_tot, Etarget, rta, nit=60):
    """Method B: Woolley (lowered isothermal) F(E) = A (exp((Phi_t - E)/s2) - 1), E < Phi_t = Phi(r_ta); the reservoir's mass and
    its energy in the total potential fixed; self-consistent with its own gravity. Mfix = everything else's M(<r) on rg (kpc grid).
    returns M_res(<r) on rg, s2, energy reached."""
    from scipy.special import erf
    lr = np.log(rg)

    def rho_of_W(W):
        W = np.maximum(W, 0.0); Wm = float(W.max())     # overall factor exp(-Wm) only (normalisation is free)
        return np.exp(W - Wm) * erf(np.sqrt(W)) - np.exp(-Wm) * np.sqrt(4 * W / math.pi) * (1 + 2 * W / 3)

    def eps_of_W(W):   # kinetic energy density per unit rho1*s2
        W = np.maximum(W, 0.0)
        # integral of 4 pi v^2 (v^2/2) [exp(W - v^2/2) - 1] dv (v in units of s), normalised like rho_of_W
        v = np.linspace(0, 1, 400)[None, :] * np.sqrt(2 * W)[:, None]
        f = np.maximum(np.exp(W[:, None] - v ** 2 / 2 - W[:, None]) - np.exp(-W[:, None]), 0.0)   # per-radius factor cancels in I/J
        I = np.trapz(v ** 4 / 2 * f, v, axis=1)
        J = np.trapz(v ** 2 * f, v, axis=1)
        return np.where(J > 0, I / np.maximum(J, 1e-300), 0.0)

    def solve(s2):
        Mr = Mres_tot * np.clip(rg / rta, 0, 1) ** 1.0
        for _ in range(nit):
            Mt = Mfix + Mr
            g = G * Mt / rg ** 2 - OL * H0 ** 2 * rg
            Phi = np.zeros(len(rg)); Phi[-1] = -G * Mt[-1] / rg[-1] - 0.5 * OL * H0 ** 2 * rg[-1] ** 2
            seg = 0.5 * (g[1:] + g[:-1]) * np.diff(rg)
            Phi[:-1] = Phi[-1] - np.cumsum(seg[::-1])[::-1]
            Pt = np.interp(math.log(rta), lr, Phi)
            W = (Pt - Phi) / s2
            rho = rho_of_W(W) * (rg <= rta)
            sh = 4 * math.pi * rg ** 2 * rho
            M = np.r_[0, np.cumsum(0.5 * (sh[1:] + sh[:-1]) * np.diff(rg))]
            if M[-1] <= 0:
                return None
            Mnew = Mres_tot * M / M[-1]
            if np.max(np.abs(Mnew - Mr)) < 1e-6 * Mres_tot:
                Mr = Mnew; break
            Mr = 0.5 * Mr + 0.5 * Mnew
        kin = eps_of_W(np.maximum(W, 0)) * s2
        E = np.trapz(sh * (Phi + kin), rg) / np.trapz(sh, rg) * Mres_tot
        return Mr, E

    lo, hi = None, None
    s2s = np.geomspace(1e-3, 1e3, 25) * (G * (Mfix[-1] + Mres_tot) / rta)
    vals = []
    for s2 in s2s:
        out = solve(s2)
        vals.append(np.nan if out is None else out[1])
    vals = np.array(vals)
    ok = np.isfinite(vals)
    k = np.where(ok[:-1] & ok[1:] & (np.sign(vals[:-1] - Etarget) != np.sign(vals[1:] - Etarget)))[0]
    if not ok.any():
        return np.full(len(rg), np.nan), float("nan"), float("nan"), False
    if not len(k):
        kk = int(np.nanargmin(np.abs(vals - Etarget)))
        out = solve(s2s[kk]); return out[0], float(s2s[kk]), float(out[1]), False
    a, b = s2s[k[0]], s2s[k[0] + 1]
    fa = vals[k[0]] - Etarget
    for _ in range(40):
        m = math.sqrt(a * b); out = solve(m)
        fm = out[1] - Etarget
        if np.sign(fm) == np.sign(fa):
            a, fa = m, fm
        else:
            b = m
    out = solve(math.sqrt(a * b))
    return out[0], float(math.sqrt(a * b)), float(out[1]), True


def r_ta_single(M_ta, a_obs):
    d0 = calibrate_delta0(M_ta, a_obs)
    single_shell_ta(M_ta, d0)
    return float(single_shell_ta.r_ta), d0


def derive(M_ta, fret, r_obs, Mcore_obs, Msrc_obs, a0, nu, a_obs=1.0, tol=0.01, **kw):
    """Method A for one system. r_obs (kpc), Mcore_obs / Msrc_obs: the observed retained-baryon and source cumulative profiles
    at a_obs (Msun). The core shape is placed in x = r / r_ta using the single-shell r_ta; delta0 is then iterated (secant in
    log) until the turned-around mass at a_obs equals M_ta to tol. Returns the finished Infall object."""
    rta_p, d0 = r_ta_single(M_ta, a_obs)
    x = np.geomspace(1e-4, 4.0, 700)
    Mtot = float(Mcore_obs[-1])
    Sc = np.interp(x * rta_p, r_obs, Mcore_obs, left=0.0, right=Mcore_obs[-1]) / Mtot
    Ss = np.interp(x * rta_p, r_obs, Msrc_obs, left=0.0, right=Msrc_obs[-1]) / Mtot
    hist = []
    d = d0
    for it in range(6):
        I = Infall(M_ta, fret, x, Sc, Ss, a0, nu, a_obs=a_obs, delta0=d, **kw).run()
        ratio = I.M_turned / M_ta
        hist.append((d, ratio))
        if abs(ratio - 1) <= tol:
            break
        if len(hist) == 1:
            d = d * ratio ** -0.5
        else:
            (d1, r1), (d2, r2) = hist[-2], hist[-1]
            sl = (math.log(r2) - math.log(r1)) / (math.log(d2) - math.log(d1)) if d2 != d1 else 2.0
            sl = sl if sl > 0.2 else 2.0
            d = d2 * math.exp(-math.log(r2) / sl)
    I.final_profile()
    I.rta_pred = rta_p; I.delta_hist = hist
    return I
