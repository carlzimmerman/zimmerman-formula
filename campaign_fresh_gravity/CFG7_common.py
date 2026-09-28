#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG7 common: the shared engine for the campaign's top-five swing (FG016, FG001, FG004, FG041, FG097).

  * the background: flat LCDM with Planck 2018's Omega_m = 0.3153 (CFG4's value), the linear growth D(a) and f(a), and the GR
    top-hat's turnaround contrast 1 + delta_ta(a) and linear threshold delta_lin,ta(a) (checked against CFG4_switch's D1 table);
  * the linear power spectrum from CLASS (classy), normalised to sigma_8 = 0.811 -- NOT the record's T_EH98, which carries a
    units error (CFG1 B03);
  * a spherical collisionless shell code in physical coordinates (leapfrog in time with an adaptive step, angular momentum
    assigned at turnaround as in XR28, pericentre and apocentre counting, a softened static core for the earliest-collapsed
    mass), with two readings of the interior:
      N  Newtonian: the enclosed mass is the shells' own (the cold component IS the phantom and gravitates normally);
      G  ground state: inside the current outermost caustic the enclosed mass is redistributed to the framework's law's shape
         M_law(r) = M_b nu(G M_b / r^2 a0), normalised to the shells' mass at the caustic (M_b solved from that condition);
  * the framework's law and CFG4's turnaround convention: r_ta = where the UNTRUNCATED law's mean enclosed density equals
    (1 + delta_ta) times the mean matter density.

Units: Mpc, Msun, km/s; time in Mpc/(km/s) (1 unit = 977.79 Gyr); accelerations in (km/s)^2/Mpc.
"""
import os, sys, math, json, time, builtins
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import CFG4_common as C4                                                              # kernels, exec_slices, SPARC loader

GMPC = 4.30091727e-9                                                                  # G [Mpc (km/s)^2 / Msun]
MPC_M = 3.0856775814913673e22
SI_ACC = 1e6 / MPC_M                                                                  # (km/s)^2/Mpc -> m/s^2
UNIT_GYR = MPC_M / 1e3 / (3.15576e16)                                                 # Mpc/(km/s) in Gyr (977.79)
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0 = {k: v / SI_ACC for k, v in A0_SI.items()}                                       # (km/s)^2/Mpc
FOOTS = ("canonical", "alt")
nu_p2, nu_mono = C4.nu_p2, C4.nu_mono
KERNELS = {"P2": nu_p2, "nu_mono": nu_mono}

H_PL, OM_PL = 0.6736, 0.3153                                                          # Planck 2018 (CFG4's Omega_m)


class Cosmo:
    """flat Lambda + matter (radiation neglected: every epoch used here is z <= 200)."""

    def __init__(self, Om=OM_PL, h=H_PL, name="LCDM"):
        self.Om, self.OL, self.h, self.name = Om, 1.0 - Om, h, name
        self.H0 = 100.0 * h
        self.rhoc0 = 3 * self.H0 ** 2 / (8 * math.pi * GMPC)                           # Msun/Mpc^3
        self.rhom0 = Om * self.rhoc0
        lna = np.linspace(math.log(1e-4), math.log(3.0), 6001)
        rhs = lambda s, Y: [Y[1], 1.5 * self.Om_a(math.exp(s)) * Y[0] - (2 + self.dlnH(math.exp(s))) * Y[1]]
        sol = solve_ivp(rhs, (lna[0], lna[-1]), [1e-4, 1e-4], t_eval=lna, rtol=1e-11, atol=1e-16, method="DOP853")
        D = sol.y[0]; self._lna = lna; self._D = D / np.interp(0.0, lna, D); self._f = sol.y[1] / sol.y[0]
        # cosmic time t(ln a) [Mpc/(km/s)]
        tt = np.concatenate([[0.0], np.cumsum(0.5 * (1 / self.H(np.exp(lna[1:])) + 1 / self.H(np.exp(lna[:-1]))) * np.diff(lna))])
        a_first = math.exp(lna[0])
        self._t = tt + 2.0 / (3.0 * self.H0 * math.sqrt(self.Om)) * a_first ** 1.5          # matter-era start
        self._ta = None

    def E(self, a):
        return np.sqrt(self.Om / np.asarray(a, float) ** 3 + self.OL)

    def H(self, a):
        return self.H0 * self.E(a)

    def Om_a(self, a):
        return self.Om / a ** 3 / float(self.E(a)) ** 2

    def dlnH(self, a):
        return -1.5 * self.Om / a ** 3 / float(self.E(a)) ** 2

    def rhom(self, a):
        return self.rhom0 / np.asarray(a, float) ** 3

    def D(self, a):
        return np.interp(np.log(a), self._lna, self._D)

    def f(self, a):
        return np.interp(np.log(a), self._lna, self._f)

    def t(self, a):
        return np.interp(np.log(a), self._lna, self._t)

    # ---------------------------------------------------------------------- the GR top-hat at turnaround
    def _tophat(self, dL_i, a_i):
        """a top-hat of linear (growing-mode) mean overdensity dL_i at a_i: (a_ta, 1 + delta_NL at turnaround)."""
        R_i = 1.0; M = 4 * math.pi / 3 * float(self.rhom(a_i)) * R_i ** 3
        r0 = R_i * (1 - dL_i / 3.0); H_i = float(self.H(a_i)); f_i = float(self.f(a_i))
        v0 = H_i * r0 - f_i * H_i * dL_i / 3.0 * R_i

        def rhs(s, y):
            a = math.exp(s); Ha = float(self.H(a))
            return [y[1] / Ha, (-GMPC * M / y[0] ** 2 + self.OL * self.H0 ** 2 * y[0]) / Ha]

        ev = lambda s, y: y[1]
        ev.terminal, ev.direction = True, -1
        sol = solve_ivp(rhs, (math.log(a_i), math.log(3.0)), [r0, v0], events=ev, rtol=1e-11, atol=1e-14, method="DOP853")
        if not len(sol.t_events[0]):
            return None, None
        s_ta = float(sol.t_events[0][0]); r_ta = float(sol.y_events[0][0][0])
        a_ta = math.exp(s_ta)
        return a_ta, M / (4 * math.pi / 3 * r_ta ** 3) / float(self.rhom(a_ta))

    def turnaround(self, a_ta, a_i=1e-3):
        """(1 + delta_ta, delta_lin at turnaround extrapolated with D) for a top-hat turning around at a_ta."""
        lo, hi = 1e-6, 0.3
        for _ in range(80):
            mid = math.sqrt(lo * hi)
            at, _ = self._tophat(mid, a_i)
            if at is None or at > a_ta:
                lo = mid
            else:
                hi = mid
            if hi / lo < 1 + 1e-10:
                break
        dL = math.sqrt(lo * hi)
        at, one_d = self._tophat(dL, a_i)
        return one_d, dL * float(self.D(a_ta) / self.D(a_i))

    def ta_table(self):
        if self._ta is None:
            from scipy.interpolate import CubicSpline
            lna = np.linspace(math.log(1 / 11.0), math.log(1.35), 36)                    # z = 10 ... -0.26, smooth in ln a
            rows = [self.turnaround(math.exp(x)) for x in lna]
            d1 = np.array([r[0] for r in rows]); dl = np.array([r[1] for r in rows])
            self._ta = (lna, d1, dl, CubicSpline(lna, np.log(d1)), CubicSpline(lna, np.log(dl)))
        return self._ta

    def one_plus_delta_ta(self, a):
        return float(np.exp(self.ta_table()[3](math.log(float(a)))))

    def delta_lin_ta(self, a):
        return float(np.exp(self.ta_table()[4](math.log(float(a)))))

    def dln_delta_lin_ta(self, a):
        return float(self.ta_table()[4](math.log(float(a)), 1))


LCDM = Cosmo()
EDS = Cosmo(Om=1.0, h=H_PL, name="EdS")


# ---------------------------------------------------------------------------------------------- the linear power spectrum (CLASS)
_PK = {}


def class_pk(cosmo=LCDM, sigma8=0.811):
    """Delta^2(k) at z = 0 on a log-k grid (k in 1/Mpc), from CLASS, rescaled to sigma_8 (R = 8/h Mpc)."""
    key = (cosmo.Om, cosmo.h, sigma8)
    if key in _PK:
        return _PK[key]
    from classy import Class
    cl = Class()
    om_b = 0.02237; om_nu = 0.06 / 93.14; om_c = cosmo.Om * cosmo.h ** 2 - om_b - om_nu
    cl.set({"output": "mPk", "P_k_max_1/Mpc": 60.0, "z_max_pk": 0.0, "h": cosmo.h, "omega_b": om_b, "omega_cdm": om_c,
            "n_s": 0.9649, "A_s": 2.1e-9, "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06})
    cl.compute()
    lk = np.linspace(math.log(1e-4), math.log(50.0), 3000); kk = np.exp(lk)
    pk = np.array([cl.pk_lin(k, 0.0) for k in kk])
    s8_class = cl.sigma8()
    cl.struct_cleanup(); cl.empty()
    D2 = kk ** 3 * pk / (2 * math.pi ** 2)
    s8_now = math.sqrt(float(np.trapz(D2 * Wth(kk * 8.0 / cosmo.h) ** 2, lk)))
    D2 = D2 * (sigma8 / s8_now) ** 2
    _PK[key] = (lk, kk, D2, s8_class, s8_now)
    return _PK[key]


def Wth(x):
    x = np.asarray(x, float)
    return np.where(x > 1e-3, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-3) ** 3, 1.0 - x * x / 10.0)


def dWth_dlnx(x):
    x = np.asarray(x, float)
    return np.where(x > 1e-3, 3 * ((x * x - 3) * np.sin(x) + 3 * x * np.cos(x)) / np.maximum(x, 1e-3) ** 3, -x * x / 5.0)


def sig2(R1, R2, cosmo=LCDM):
    """<delta(<R1) delta(<R2)> at z = 0 for top hats of comoving radii R1, R2 [Mpc] (linear, CLASS)."""
    lk, kk, D2, _, _ = class_pk(cosmo)
    return float(np.trapz(D2 * Wth(kk * R1) * Wth(kk * R2), lk))


def R_lagr(M, cosmo=LCDM):
    return (3 * np.asarray(M, float) / (4 * math.pi * cosmo.rhom0)) ** (1 / 3)


def accretion_slope(M, cosmo=LCDM):
    """the constrained mean profile around a region of Lagrangian mass M whose mean linear overdensity is fixed: delta(<q) =
    delta(<R) sigma^2(q, R) / sigma^2(R, R).  Returns eps = -dln delta(<q)/dln M at q = R (its own scale), and its 1-sigma
    conditional scatter (the slope's conditional variance given the constraint, per unit of the constraint's typical value)."""
    lk, kk, D2, _, _ = class_pk(cosmo)
    R = float(R_lagr(M, cosmo))
    W = Wth(kk * R); dW = dWth_dlnx(kk * R)
    s_RR = float(np.trapz(D2 * W * W, lk))
    s_dR = float(np.trapz(D2 * dW * W, lk))                                               # <d delta(<q)/dln q |_R  delta(<R)>
    s_dd = float(np.trapz(D2 * dW * dW, lk))
    eps = -(s_dR / s_RR) / 3.0                                                           # dln/dlnM = (1/3) dln/dlnq
    cond_var = s_dd - s_dR ** 2 / s_RR
    return eps, math.sqrt(max(cond_var, 0.0)), math.sqrt(s_RR)


# ---------------------------------------------------------------------------------------------- the law and CFG4's turnaround convention
def M_law(Mb, r, a0, kfun=nu_p2):
    return Mb * kfun(GMPC * Mb / np.maximum(np.asarray(r, float), 1e-12) ** 2 / a0)


def r_where_density(Mb, a0, kfun, a, Delta, cosmo=LCDM):
    """radius [Mpc, physical] where the law's (untruncated) mean enclosed density equals Delta x rho_m(a)."""
    rho = float(cosmo.rhom(a))
    fn = lambda lr: math.log(float(M_law(Mb, math.exp(lr), a0, kfun)) / (4 * math.pi / 3 * math.exp(3 * lr) * rho)) - math.log(Delta)
    return math.exp(brentq(fn, math.log(1e-5), math.log(1e3), xtol=1e-13))


def r_ta_law(Mb, a0, kfun, a, cosmo=LCDM):
    """CFG4's convention: each galaxy's own turnaround radius from its untruncated law and the top-hat contrast."""
    return r_where_density(Mb, a0, kfun, a, cosmo.one_plus_delta_ta(a), cosmo)


def x_edge_from_Delta(Delta_c, Mb, a0, kfun, a, cosmo=LCDM):
    """T5 closure: the phantom IS the cold matter inside the edge, so the law's mean enclosed density at the edge equals the
    dynamical mean density inside the caustic; returns x_e = r_edge / r_ta (CFG4's r_ta)."""
    return r_where_density(Mb, a0, kfun, a, Delta_c, cosmo) / r_ta_law(Mb, a0, kfun, a, cosmo)


# ---------------------------------------------------------------------------------------------- initial conditions
def ics_powerlaw(eps, M_ta_obs, a_obs, cosmo=LCDM, N=2000, a_i=0.005, span=(3e-3, 25.0), dcap=0.25):
    """shells whose mean enclosed LINEAR overdensity (extrapolated to a = 1) is dL(M) = dL_ta (M / M_ta_obs)^-eps, with dL_ta set
    so that the shell M_ta_obs turns around exactly at a_obs (GR top-hat); mass inside the shell whose dL D(a_i) reaches dcap is a
    static softened core.  Returns a dict for run_shells."""
    dL_ta = cosmo.delta_lin_ta(a_obs) / float(cosmo.D(a_obs))
    Di = float(cosmo.D(a_i))
    M_core = M_ta_obs * max(span[0], (dL_ta * Di / dcap) ** (1.0 / eps))
    Me = np.geomspace(M_core, span[1] * M_ta_obs, N + 1)
    Mk = 0.5 * (Me[1:] + Me[:-1]); m = np.diff(Me)
    dL = dL_ta * (Mk / M_ta_obs) ** (-eps)
    return dict(kind="powerlaw", eps=eps, Mk=Mk, m=m, dL=dL, M_core=M_core, a_i=a_i, M_ta_obs=M_ta_obs, a_obs=a_obs)


def ics_constrained(M_ta_obs, a_obs, cosmo=LCDM, N=2000, a_i=0.005, span=(3e-3, 25.0), dcap=0.25, t_env=0.0, eps_in=None):
    """the constrained mean linear profile around the region M_ta_obs that turns around at a_obs (its own mean overdensity fixed),
    dL(<q) = dL_ta sigma^2(q, R) / sigma^2(R, R) outside, plus t_env x the conditional scatter; inside M_ta_obs / 4 the profile is
    continued as a power law with the local slope there (the region's own earlier accretion, steepened to eps_in if given)."""
    dL_ta = cosmo.delta_lin_ta(a_obs) / float(cosmo.D(a_obs))
    R = float(R_lagr(M_ta_obs, cosmo)); sRR = sig2(R, R, cosmo)
    Me = np.geomspace(span[0] * M_ta_obs, span[1] * M_ta_obs, N + 1)
    Mk = 0.5 * (Me[1:] + Me[:-1]); m = np.diff(Me)
    q = R_lagr(Mk, cosmo)
    s_qR = np.array([sig2(qq, R, cosmo) for qq in q])
    dL = dL_ta * s_qR / sRR
    if t_env != 0.0:
        s_qq = np.array([sig2(qq, qq, cosmo) for qq in q])
        dL = dL + t_env * np.sqrt(np.maximum(s_qq - s_qR ** 2 / sRR, 0.0))
    Mj = M_ta_obs / 4.0
    j = int(np.searchsorted(Mk, Mj))
    loc = -np.gradient(np.log(dL), np.log(Mk))[j]
    e_in = max(loc, eps_in if eps_in else 0.0)
    inner = Mk < Mj
    dL[inner] = dL[j] * (Mk[inner] / Mk[j]) ** (-e_in)
    dL = np.minimum.accumulate(dL)                                                       # non-increasing outward
    Di = float(cosmo.D(a_i))
    keep = dL * Di < dcap
    M_core = float(Me[np.argmax(keep)]) if not keep.all() else float(Me[0])
    return dict(kind="constrained", eps=float(loc), eps_in=e_in, Mk=Mk[keep], m=m[keep], dL=dL[keep], M_core=M_core, a_i=a_i,
                M_ta_obs=M_ta_obs, a_obs=a_obs, t_env=t_env)


# ---------------------------------------------------------------------------------------------- the shell code
def run_shells(ics, cosmo=LCDM, snaps=(1.0,), mode="N", jf=(0.15, 0.35), seed=7, eta=0.02, ds_max=0.004, soft_frac=2e-4,
               a0=None, kfun=nu_p2, pct=99.0, mutate_frozen=False, max_steps=6_000_000, tpct=0.0, n_resolve=15):
    """integrate the shells from a_i to each snapshot scale factor; returns a list of snapshot dicts.
    mode 'N': Newtonian enclosed mass.  mode 'G': inside the current outermost caustic (the pct-th percentile radius of shells
    past their first pericentre) the enclosed mass follows the law's shape normalised to the shells' mass at the caustic.
    mutate_frozen: the enclosed mass is frozen at its initial Lagrangian value (no shell crossing) -- a control that must fail."""
    rng = np.random.default_rng(seed)
    Mk, m, dL, a_i = ics["Mk"], ics["m"], ics["dL"], ics["a_i"]
    M_core = ics["M_core"]
    N = len(Mk)
    Di, fi, Hi = float(cosmo.D(a_i)), float(cosmo.f(a_i)), float(cosmo.H(a_i))
    q = R_lagr(Mk, cosmo)                                                               # comoving Lagrangian radii
    d_i = dL * Di
    r = a_i * q * (1 - d_i / 3.0)
    v = Hi * r - fi * Hi * d_i / 3.0 * a_i * q
    jfr = rng.uniform(jf[0], jf[1], N)
    j2 = np.zeros(N); turned = np.zeros(N, bool); nperi = np.zeros(N, int); napo = np.zeros(N, int)
    r_apo1 = np.full(N, np.nan); a_apo1 = np.full(N, np.nan); a_turn = np.full(N, np.nan); r_turn = np.full(N, np.nan)
    rta_apo1 = np.full(N, np.nan); rho_apo1 = np.full(N, np.nan)
    soft_c = soft_frac * float(R_lagr(ics["M_ta_obs"], cosmo))                          # COMOVING softening: soft(a) = soft_c a
    OLH2 = cosmo.OL * cosmo.H0 ** 2
    M0_frozen = M_core + np.cumsum(m) - 0.5 * m
    state = dict(Mb_G=np.nan, r_c=np.nan)

    def encl(rr):
        if mutate_frozen:
            return M0_frozen.copy()
        o = np.argsort(rr, kind="stable")
        cm = M_core + np.cumsum(m[o]) - 0.5 * m[o]
        out = np.empty(N); out[o] = cm
        return out

    def r_ta_now(rr, a):
        o = np.argsort(rr); rs = rr[o]; cm = M_core + np.cumsum(m[o])
        dens = cm / (4 * math.pi / 3 * rs ** 3) / float(cosmo.rhom(a))
        j = np.where(dens >= cosmo.one_plus_delta_ta(a))[0]
        return float(rs[j[-1]]) if len(j) else float("nan")

    def accel(rr, a):
        soft = soft_c * a
        Me = encl(rr)
        if mode == "G":
            cr = nperi >= 1
            if cr.sum() >= 20:
                okw = np.isfinite(a_apo1) & (a_apo1 >= a * math.exp(-0.2))
                if okw.sum() >= 8:
                    r_c = float(np.percentile(r_apo1[okw] / rta_apo1[okw], 87.0)) * r_ta_now(rr, a)
                else:
                    r_c = float(np.percentile(rr[cr], pct))
                o = np.argsort(rr); cm = M_core + np.cumsum(m[o])
                M_c = float(np.interp(r_c, rr[o], cm))
                if M_c > 0 and r_c > 0:
                    fn = lambda lmb: math.log(float(M_law(math.exp(lmb), r_c, a0, kfun))) - math.log(M_c)
                    try:
                        lmb = brentq(fn, math.log(M_c) - 40, math.log(M_c) + 1e-9)
                    except ValueError:
                        lmb = None
                    if lmb is not None:
                        Mb = math.exp(lmb)
                        inside = rr < r_c
                        # the law's shape inside the caustic; inside 3% of r_c a uniform-density core (the law's point-mass limit
                        # would make a Keplerian spike whose orbits cost tiny steps and do not shape the outer caustic)
                        r_core = 0.03 * r_c
                        Ml = M_law(Mb, np.maximum(rr, r_core), a0, kfun) * np.where(rr < r_core, (rr / r_core) ** 3, 1.0)
                        Me = np.where(inside, Ml, Me)
                        state["Mb_G"], state["r_c"] = Mb, r_c
        g = -GMPC * Me * rr / (rr * rr + soft * soft) ** 1.5 + j2 / np.maximum(rr, 1e-9) ** 3 + OLH2 * rr
        return g, Me

    out = []
    si = 0; snaps = sorted(snaps)
    s = math.log(a_i); a = a_i
    g, Me = accel(r, a)
    nstep = 0
    while si < len(snaps):
        # the adaptive step: resolve every turned shell's local dynamical time
        soft = soft_c * a
        rr_ = np.maximum(r, soft)
        gmag = GMPC * Me / (rr_ * rr_) + j2 / rr_ ** 3                                   # the SIZE of each pull (they cancel at pericentre)
        tau = np.sqrt(rr_ / np.maximum(gmag, 1e-30))
        tv = rr_ / np.maximum(np.abs(v), 1e-30)
        tt = np.minimum(tau, tv)
        # shells past n_resolve pericentres sit deep in the settled core: they still move (with this step) but no longer set it
        res_ = turned & (nperi < n_resolve)
        tmin = float(np.percentile(tt[res_], tpct)) if res_.sum() > 10 else (float(tt[turned].min()) if turned.any() else float(tt.min()))
        dt_lim = eta * tmin
        Ha = float(cosmo.H(a))
        ds = min(ds_max, dt_lim * Ha)
        s_next = math.log(snaps[si])
        last = s + ds >= s_next - 1e-12
        if last:
            ds = s_next - s
        a1 = math.exp(s + ds)
        dt = float(cosmo.t(a1) - cosmo.t(a))
        vh = v + 0.5 * dt * g
        r = r + dt * vh
        neg = r < 0
        if neg.any():
            r[neg] = -r[neg]; vh[neg] = -vh[neg]
        g1, Me = accel(r, a1)
        vn = vh + 0.5 * dt * g1
        # events
        newt = (~turned) & (v > 0) & (vn <= 0)
        if newt.any():
            gN = np.abs(-GMPC * Me[newt] * r[newt] / (r[newt] ** 2 + (soft_c * a1) ** 2) ** 1.5)
            j2[newt] = (jfr[newt] * r[newt]) ** 2 * r[newt] * gN
            turned |= newt; a_turn[newt] = a1; r_turn[newt] = r[newt]
        peri = turned & (v < 0) & (vn >= 0)
        nperi[peri] += 1
        apo = turned & (nperi >= 1) & (v > 0) & (vn <= 0)
        if apo.any():
            first = apo & (napo == 0)
            if first.any():
                r_apo1[first] = r[first]; a_apo1[first] = a1
                rta_apo1[first] = r_ta_now(r, a1)
                # the mean enclosed (shell) density at the apocentre, in units of rho_m(a1)
                o_ = np.argsort(r); cm_ = M_core + np.cumsum(m[o_])
                rho_apo1[first] = np.interp(r[first], r[o_], cm_) / (4 * math.pi / 3 * r[first] ** 3) / float(cosmo.rhom(a1))
            napo[apo] += 1
        v, g, s, a = vn, g1, s + ds, a1
        nstep += 1
        if nstep > max_steps:
            raise RuntimeError("step budget exceeded")
        if last:
            out.append(dict(a=a, r=r.copy(), v=v.copy(), turned=turned.copy(), nperi=nperi.copy(), napo=napo.copy(), m=m.copy(),
                            M_core=M_core, Mk=Mk.copy(), r_apo1=r_apo1.copy(), a_apo1=a_apo1.copy(), a_turn=a_turn.copy(),
                            rta_apo1=rta_apo1.copy(), rho_apo1=rho_apo1.copy(),
                            r_turn=r_turn.copy(), nstep=nstep, Mb_G=state["Mb_G"], r_c_G=state["r_c"], soft=soft_c * a))
            si += 1
    return out


def measure(sn, cosmo=LCDM, pct=99.0):
    """the observables of one snapshot: turnaround radius (zero velocity; top-hat contrast), the outermost caustic (pct-th
    percentile radius of shells past their first pericentre; also max and 95th), the steepest-slope radius, r_200m, and the mean
    enclosed density at each, in units of rho_m(a)."""
    a, r, v, m = sn["a"], sn["r"], sn["v"], sn["m"]
    rho = float(cosmo.rhom(a))
    o = np.argsort(r); rs = r[o]; cm = sn["M_core"] + np.cumsum(m[o])
    Dm = cm / (4 * math.pi / 3 * rs ** 3) / rho
    dta = cosmo.one_plus_delta_ta(a)
    # zero-velocity radius: the innermost Lagrangian shell beyond which every shell still expands
    k = np.where(v <= 0)[0]
    zv = float("nan")
    if len(k) and k[-1] + 1 < len(r):
        kk = k[-1]
        zv = float(r[kk] + (r[kk + 1] - r[kk]) * (0 - v[kk]) / (v[kk + 1] - v[kk]))
    j = np.where(Dm >= dta)[0]
    r_dta = float(rs[j[-1]]) if len(j) else float("nan")
    cr = sn["nperi"] >= 1
    res = dict(a=a, z=1 / a - 1, r_ta_zv=zv, r_ta_dta=r_dta, n_crossed=int(cr.sum()), one_plus_delta_ta=dta, nstep=sn["nstep"],
               guard_frac_beyond_rta=(float(np.mean(r[cr] > r_dta)) if cr.any() and r_dta == r_dta else float("nan")))
    for p in (pct, 95.0, 100.0):
        if cr.sum() >= 20:
            rc = float(np.percentile(r[cr], p))
            Mc = float(np.interp(rc, rs, cm))
            res[f"r_c{p:g}"] = rc
            res[f"Delta_c{p:g}"] = Mc / (4 * math.pi / 3 * rc ** 3) / rho
            res[f"x_c{p:g}"] = rc / r_dta
            res[f"M_c{p:g}"] = Mc
        else:
            res[f"r_c{p:g}"] = res[f"Delta_c{p:g}"] = res[f"x_c{p:g}"] = res[f"M_c{p:g}"] = float("nan")
    # steepest logarithmic slope of the shell density between 0.15 and 1.0 r_ta
    edges = np.geomspace(0.05 * r_dta, 1.6 * r_dta, 90)
    h, _ = np.histogram(r, bins=edges, weights=m)
    vol = 4 * math.pi / 3 * (edges[1:] ** 3 - edges[:-1] ** 3)
    rho_r = np.maximum(h / vol, 1e-300); rm = np.sqrt(edges[1:] * edges[:-1])
    lr = np.log(rho_r); ker = np.exp(-0.5 * (np.arange(-5, 6) / 2.0) ** 2); ker /= ker.sum()
    lrs = np.convolve(np.pad(lr, 5, mode="edge"), ker, mode="valid")
    sl = np.gradient(lrs, np.log(rm))
    win = (rm > 0.15 * r_dta) & (rm < 1.0 * r_dta)
    if win.any():
        rsl = float(rm[win][np.argmin(sl[win])])
        res["r_slope"] = rsl; res["x_slope"] = rsl / r_dta; res["slope_min"] = float(sl[win].min())
        res["Delta_slope"] = float(np.interp(rsl, rs, cm)) / (4 * math.pi / 3 * rsl ** 3) / rho
    else:
        res["r_slope"] = res["x_slope"] = res["slope_min"] = res["Delta_slope"] = float("nan")
    # SPLASHBACK from the first apocentres that happened within |dln a| <= w of this epoch, each in units of r_ta at its own time
    for w in (0.1,):
        ok = np.isfinite(sn["a_apo1"]) & np.isfinite(sn["rta_apo1"]) & (np.abs(np.log(sn["a_apo1"] / a)) <= w)
        res["n_apo_window"] = int(ok.sum())
        xa = sn["r_apo1"][ok] / sn["rta_apo1"][ok]
        for p in (50.0, 75.0, 87.0, 95.0):
            if ok.sum() >= 8:
                xs = float(np.percentile(xa, p))
                rs_ = xs * r_dta
                res[f"x_sp{p:g}"] = xs
                res[f"Delta_sp{p:g}"] = float(np.interp(rs_, rs, cm)) / (4 * math.pi / 3 * rs_ ** 3) / rho
                res[f"Delta_apo{p:g}"] = float(np.percentile(sn["rho_apo1"][ok], 100.0 - p))
            else:
                res[f"x_sp{p:g}"] = res[f"Delta_sp{p:g}"] = res[f"Delta_apo{p:g}"] = float("nan")
    j2 = np.where(Dm >= 200.0)[0]
    res["r200m"] = float(rs[j2[-1]]) if len(j2) else float("nan")
    res["M200m"] = float(cm[j2[-1]]) if len(j2) else float("nan")
    res["M_ta"] = float(np.interp(r_dta, rs, cm))
    return res


def s_ta(ics, a_obs, cosmo=LCDM, dlna=0.05):
    """the turnaround mass's growth rate dln M_ta / dln a at a_obs, exactly from the linear profile (no crossing reaches it)."""
    if ics.get("kind") == "powerlaw":
        return (float(cosmo.f(a_obs)) - cosmo.dln_delta_lin_ta(a_obs)) / ics["eps"]
    def Mta(a):
        target = cosmo.delta_lin_ta(a) / float(cosmo.D(a))
        lM = np.log(ics["Mk"]); ld = np.log(ics["dL"])
        return math.exp(float(np.interp(-math.log(target), -ld, lM)))
    return (math.log(Mta(a_obs * math.exp(dlna))) - math.log(Mta(a_obs * math.exp(-dlna)))) / (2 * dlna)


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    return o


class Report:
    def __init__(self, slug, mutate):
        self.slug = slug + ("_MUTATE" if mutate else ""); self.lines = []; self.checks = []; self.numbers = {}; self.t0 = time.time()

    def P(self, s=""):
        print(s, flush=True); self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def check(self, name, detail, ok, load_bearing=True):
        self.checks.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def num(self, k, v):
        self.numbers[k] = v

    def el(self):
        return f"({time.time() - self.t0:.0f} s)"

    def write(self, here=HERE):
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        summ = dict(n_checks=len(self.checks), n_pass=sum(c["ok"] for c in self.checks), load_bearing_failures=nf,
                    failed=[c["name"][:90] for c in self.checks if not c["ok"]], seconds=round(time.time() - self.t0, 1))
        self.P(f"\n  {summ['n_pass']}/{summ['n_checks']} checks pass; load-bearing failures: {nf}   {self.el()}")
        json.dump(jclean(dict(slug=self.slug, summary=summ, checks=self.checks, numbers=self.numbers)),
                  builtins.open(os.path.join(here, self.slug + "_results.json"), "w"), indent=1)
        builtins.open(os.path.join(here, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf


# ---------------------------------------------------------------------------------------------- one run, for a process pool
def measure_pooled(snaps_by_seed, a_obs, cosmo=LCDM, w=0.1):
    """pool several seeds: the profile observables from each seed's snapshot at a_obs (medians), the splashback percentiles from
    the pooled first apocentres within |dln a| <= w of a_obs (each in units of r_ta at its own time; records from each seed's
    final state, so apocentres after a_obs count)."""
    xs, rho_ap, per = [], [], []
    for sn_obs, sn_end in snaps_by_seed:
        m_ = measure(sn_obs, cosmo)
        per.append(m_)
        ok = np.isfinite(sn_end["a_apo1"]) & np.isfinite(sn_end["rta_apo1"]) & (np.abs(np.log(sn_end["a_apo1"] / a_obs)) <= w)
        xs.append(sn_end["r_apo1"][ok] / sn_end["rta_apo1"][ok]); rho_ap.append(sn_end["rho_apo1"][ok])
    xs = np.concatenate(xs); rho_ap = np.concatenate(rho_ap)
    out = dict(a=a_obs, n_apo=int(len(xs)), per_seed=per)
    for k in ("r_ta_dta", "r_ta_zv", "x_c99", "Delta_c99", "r200m", "M200m", "M_ta", "guard_frac_beyond_rta"):
        vals = [p_.get(k, float("nan")) for p_ in per]
        out[k] = float(np.nanmedian(vals)) if np.isfinite(vals).any() else float("nan")
    for p in (50.0, 75.0, 87.0, 95.0):
        if len(xs) >= 12:
            x_ = float(np.percentile(xs, p))
            out[f"x_sp{p:g}"] = x_
            # the mean enclosed density at x_ r_ta(a_obs) in each seed's profile at a_obs (median over seeds)
            ds = []
            for (sn_obs, _), p_ in zip(snaps_by_seed, per):
                o = np.argsort(sn_obs["r"]); rs = sn_obs["r"][o]; cm = sn_obs["M_core"] + np.cumsum(sn_obs["m"][o])
                rr_ = x_ * p_["r_ta_dta"]
                ds.append(float(np.interp(rr_, rs, cm)) / (4 * math.pi / 3 * rr_ ** 3) / float(cosmo.rhom(a_obs)))
            out[f"Delta_sp{p:g}"] = float(np.median(ds))
            out[f"Delta_apo{p:g}"] = float(np.percentile(rho_ap, 100.0 - p))
            # bootstrap error on the percentile
            rng = np.random.default_rng(11)
            bs = [np.percentile(rng.choice(xs, len(xs)), p) for _ in range(300)]
            out[f"x_sp{p:g}_err"] = float(np.std(bs))
        else:
            out[f"x_sp{p:g}"] = out[f"Delta_sp{p:g}"] = out[f"Delta_apo{p:g}"] = out[f"x_sp{p:g}_err"] = float("nan")
    return out


def job(spec):
    """run one shell model from a spec dict and return its measurements (picklable): per snapshot the observables, the energy
    guard (crossed shells beyond the top-hat turnaround radius), the exact turnaround-mass growth rate and a downsampled
    enclosed-mass profile M(<r) (physical Mpc, Msun)."""
    t0 = time.time()
    cos = EDS if spec.get("cosmo", "LCDM") == "EdS" else LCDM
    if spec["kind"] == "powerlaw":
        ics = ics_powerlaw(spec["eps"], spec["M_ta_obs"], spec["a_obs"], cos, N=spec.get("N", 1000), a_i=spec.get("a_i", 0.002),
                           span=tuple(spec.get("span", (1e-3, 25.0))), dcap=spec.get("dcap", 0.25))
    else:
        ics = ics_constrained(spec["M_ta_obs"], spec["a_obs"], cos, N=spec.get("N", 1000), a_i=spec.get("a_i", 0.002),
                              span=tuple(spec.get("span", (1e-3, 25.0))), dcap=spec.get("dcap", 0.25), t_env=spec.get("t_env", 0.0))
    kf = KERNELS[spec.get("kern", "P2")]
    a0 = A0[spec["foot"]] if spec.get("foot") else None
    sn = run_shells(ics, cos, snaps=tuple(spec["snaps"]), mode=spec.get("mode", "N"), jf=tuple(spec.get("jf", (0.15, 0.35))),
                    seed=spec.get("seed", 7), eta=spec.get("eta", 0.03), a0=a0, kfun=kf, mutate_frozen=spec.get("mutate_frozen", False))
    outs = []
    for s_ in sn:
        m_ = measure(s_, cos)
        cr = s_["nperi"] >= 1
        m_["guard_frac_beyond_rta"] = float(np.mean(s_["r"][cr] > m_["r_ta_dta"])) if cr.any() and m_["r_ta_dta"] == m_["r_ta_dta"] else float("nan")
        m_["s_ta"] = s_ta(ics, s_["a"], cos)
        o = np.argsort(s_["r"]); rs = s_["r"][o]; cm = s_["M_core"] + np.cumsum(s_["m"][o])
        rg = np.geomspace(max(rs[0], 1e-4 * m_["r_ta_dta"]), rs[-1], 700)
        m_["prof_r"] = rg.tolist(); m_["prof_M"] = np.interp(rg, rs, cm).tolist()
        m_["Mb_G"] = s_["Mb_G"]; m_["r_c_G"] = s_["r_c_G"]
        outs.append(m_)
    return dict(spec=spec, snaps=outs, eps_ics=ics.get("eps"), M_core=ics["M_core"], seconds=time.time() - t0)


def job_pooled(spec):
    """several seeds of one configuration, each run to a_end = max(a_obs) e^0.12; returns pooled measurements at each a_obs and the
    per-seed mass profiles at each a_obs (for the lensing profile)."""
    t0 = time.time()
    cos = EDS if spec.get("cosmo", "LCDM") == "EdS" else LCDM
    a_obs_list = list(spec["a_obs_list"])
    a_end = max(a_obs_list) * math.exp(0.12)
    kf = KERNELS[spec.get("kern", "P2")]
    a0 = A0[spec["foot"]] if spec.get("foot") else None
    runs = []
    for sd in spec.get("seeds", (7, 8, 9)):
        ics = ics_powerlaw(spec["eps"], spec["M_ta_obs"], spec["a_norm"], cos, N=spec.get("N", 2000), a_i=spec.get("a_i", 0.002),
                           span=tuple(spec.get("span", (3e-3, 12.0))), dcap=spec.get("dcap", 0.25))
        sn = run_shells(ics, cos, snaps=tuple(sorted(a_obs_list + [a_end])), mode=spec.get("mode", "N"),
                        jf=tuple(spec.get("jf", (0.15, 0.35))), seed=sd, eta=spec.get("eta", 0.03), a0=a0, kfun=kf,
                        mutate_frozen=spec.get("mutate_frozen", False), n_resolve=spec.get("n_resolve", 15))
        runs.append((ics, {round(x["a"], 6): x for x in sn}))
    out = dict(spec=spec, seconds=None, res={})
    for ao in a_obs_list:
        pairs = [(d[round(ao, 6)], d[round(a_end, 6)]) for _, d in runs]
        mres = measure_pooled(pairs, ao, cos)
        mres["s_ta"] = s_ta(runs[0][0], ao, cos)
        mres["Mb_G"] = float(np.median([p[0]["Mb_G"] for p in pairs])) if spec.get("mode") == "G" else float("nan")
        # profiles (physical Mpc, Msun) per seed at a_obs, downsampled
        profs = []
        for sn_obs, _ in pairs:
            o = np.argsort(sn_obs["r"]); rs = sn_obs["r"][o]; cm = sn_obs["M_core"] + np.cumsum(sn_obs["m"][o])
            rg = np.geomspace(max(rs[0], 1e-3 * mres["r_ta_dta"]), rs[-1], 600)
            profs.append(dict(r=rg.tolist(), M=np.interp(rg, rs, cm).tolist()))
        mres["profiles"] = profs
        mres["nstep"] = [p[0]["nstep"] for p in pairs]
        out["res"][f"{ao:.4f}"] = mres
    out["seconds"] = time.time() - t0
    return out
