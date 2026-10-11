#!/usr/bin/env python3
"""CFG598 library (FROZEN_CRITERIA.md section 1): the CFG541 class-A radial drift PDE with infall sources over cosmic time.

  d_t rho_c + div(rho_c v_s) = s(r, t),  v_s = -alpha tau G D(<r)/r^2,  D = int 4 pi r^2 max(rho_ph - rho_c, 0) on B n C = {r < r_ta(t)},
  tau = (4 pi G (rho_b + rho_c))^(-1/2), mobility zero beyond r_ta(t).
The flux scheme is CFG541's donor-cell scheme (cfg541.py Model.run: outer donor, CFL 0.4, Gamma dt <= 0.2, trace threshold, last trace
moves whole), re-implemented here with sources.  The transport-clock geometry (sol61_push/transport_clock_2026_10_10) is automatic in the PDE.
Accretion history: CFG557's cfg557_lib (EPS main progenitor, q = 2.2, PROVISIONAL; LCDM-background spherical collapse) -- INHERITED.
Units: kpc, Msun, km/s; time unit kpc/(km/s) = 0.977792 Gyr.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, math, io, contextlib
import numpy as np
from scipy.special import erfc

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LANES, "CFG557_settling_catchment_derived"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg557_lib as L                                   # noqa: E402  (read-only import)

GK = 4.30091e-6                                              # kpc (km/s)^2 / Msun
TU_GYR = 0.977792221                                         # kpc/(km/s) in Gyr
A0SI = {"can": 9.3603e-11, "alt": 1.1312e-10}
A0K = {f: v * 3.0856775814913673e19 / 1e6 for f, v in A0SI.items()}   # (km/s)^2 / kpc
FB = L.FB
h = L.h
XMIN = 0.02
_E0 = None


def epoch0():
    global _E0
    if _E0 is None:
        with contextlib.redirect_stdout(io.StringIO()):
            _E0 = L.Epoch(0.0)
    return _E0


def nu_m1(y):
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        return 1.0 / np.expm1(np.sqrt(y))


class Host:
    """accretion history of one host (CFG557 machinery) in kpc / Msun / code time."""
    def __init__(self, lMta_h=None, mw=False):
        E = epoch0()
        self.mw = mw
        if mw:
            self.Mb0 = 6e10; self.a = 2.5; self.fret = 0.10
            self.Mta = self.Mb0 / (self.fret * FB)               # Msun
            Mta_h = self.Mta * h
        else:
            Mta_h = 10 ** lMta_h; self.Mta = Mta_h / h; self.a = None
            self.fret = L.fret_of(lMta_h)
            self.Mb0 = self.fret * FB * self.Mta
        self.lMta_h = math.log10(Mta_h)
        X, dL = E.mah(Mta_h)
        ld = np.log(np.clip(dL, E.DL[0], E.DL[-1]))
        tta = np.interp(ld, E.lDL, E.TTA); rta_u = np.interp(ld, E.lDL, E.RTA)
        dtc = np.interp(ld, E.lDL, E.DT[:, 0])
        RL = L.r_lagr(X * Mta_h)                                 # comoving Mpc/h
        self.X = X
        self.t_ta = tta * L.GYR_PER_HINV / TU_GYR               # code time
        self.t_coll = (tta + dtc) * L.GYR_PER_HINV / TU_GYR
        self.r_sh = rta_u * RL * 1000.0 / h                       # physical kpc
        self.t0 = E.t_obs * L.GYR_PER_HINV / TU_GYR
        self.t_s = float(self.t_ta[0])
        self.rta0 = float(np.interp(self.t0, self.t_ta, self.r_sh))
        self.mono_t = bool(np.all(np.diff(self.t_ta) > 0)); self.mono_r = bool(np.all(np.diff(self.r_sh) > 0))
        self.Mcat = (1 - FB) * self.Mta

    def X_ta(self, t):
        return float(np.interp(t, self.t_ta, self.X, left=self.X[0], right=1.0))

    def r_ta(self, t):
        return float(np.interp(t, self.t_ta, self.r_sh, left=self.r_sh[0], right=self.rta0))


class Run:
    def __init__(self, host, foot, placement, N=300):
        self.H, self.foot, self.pl, self.N = host, foot, placement, N
        self.a0 = A0K[foot]
        H = host
        rM0 = math.sqrt(GK * H.Mb0 / self.a0)
        self.rM0 = rM0
        rin = 0.01 * (H.a if H.mw else rM0)
        self.rf = rf = np.geomspace(rin, H.rta0, N + 1)
        self.V = 4 * math.pi / 3 * np.diff(rf ** 3); self.A = 4 * math.pi * rf ** 2; self.rc = np.sqrt(rf[1:] * rf[:-1])
        self.Vf0 = (GK * H.Mb0 * self.a0) ** 0.25
        # deposits: per shell bin (mid values)
        Xm = 0.5 * (H.X[1:] + H.X[:-1]); dX = np.diff(H.X)
        self.dep_m = H.Mcat * dX
        if placement == "P0":
            self.dep_t = 0.5 * (H.t_ta[1:] + H.t_ta[:-1]); self.dep_R = 0.5 * (H.r_sh[1:] + H.r_sh[:-1])
            R0 = H.r_sh[0]
        else:
            self.dep_t = 0.5 * (H.t_coll[1:] + H.t_coll[:-1]); self.dep_R = 0.25 * (H.r_sh[1:] + H.r_sh[:-1])
            R0 = 0.5 * H.r_sh[0]
        o = np.argsort(self.dep_t); self.dep_t, self.dep_R, self.dep_m = self.dep_t[o], self.dep_R[o], self.dep_m[o]
        self.R0 = R0
        self.set_baryons(H.X[0])

    # ---------------------------------------------------------------------------------------------------- target
    def set_baryons(self, xb):
        self.xb = xb
        Mb = self.H.Mb0 * xb; rf = self.rf
        if self.H.mw:
            Mbf = Mb * rf ** 2 / (rf + self.H.a) ** 2
            self.rhob = np.diff(Mbf) / self.V
        else:
            Mbf = np.full_like(rf, Mb); self.rhob = np.zeros(self.N)
        y = GK * Mbf / (rf ** 2 * self.a0)
        self.Mphf = Mbf * nu_m1(y)
        self.Mphf[~np.isfinite(self.Mphf)] = 0.0
        self.mph = np.maximum(np.diff(self.Mphf), 0.0)
        self.Mbf = Mbf

    def deposit_profile(self, R, M):
        """cell masses for one deposit of mass M with placement radius R"""
        rf = self.rf; out = np.zeros(self.N)
        if self.pl == "P0":
            i = int(np.clip(np.searchsorted(rf, R) - 1, 0, self.N - 1)); out[i] = M; return out
        with np.errstate(divide="ignore", invalid="ignore"):
            F = np.where(rf < R, erfc(np.sqrt(np.log(R / np.minimum(rf, R)))), 1.0)
        F[0] = 0.0 if rf[0] < R else 1.0
        F[-1] = 1.0
        out = np.diff(F) * M
        if R <= rf[0]: out[:] = 0; out[0] = M
        return out

    def initial(self):
        m = np.zeros(self.N); M = self.H.Mcat * self.H.X[0]
        rf = self.rf; R = max(self.R0, rf[1])
        w = np.clip(np.minimum(rf[1:], R) - rf[:-1], 0, None)
        m += M * w / w.sum()
        return m

    # ---------------------------------------------------------------------------------------------------- dynamics
    def flux_step(self, m, alpha, rta, dtmax):
        """one CFG541 donor-cell step; returns (new m, dt, vmax/Vf)"""
        N, V, A, rf = self.N, self.V, self.A, self.rf
        cellB = rf[:-1] < rta
        rho = m / V
        d = np.where(cellB, np.maximum(self.mph / V - rho, 0.0), 0.0)
        Md = np.concatenate([[0.0], np.cumsum(d * V)])
        dpsi = GK * Md / rf ** 2
        live = m > self.thr
        tau = np.where(live, 1.0 / np.sqrt(4 * math.pi * GK * np.maximum(rho + self.rhob, 1e-300)), 0.0)
        don = slice(1, N)
        ok = live[don] & cellB[don]
        v = alpha * tau[don] * dpsi[1:N]
        flux = rho[don] * v * A[1:N]
        with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
            dtc = np.where(ok & (v > 0), 0.4 * V[don] / np.maximum(A[1:N] * v, 1e-300), np.inf).min()
        sel = live & cellB
        gam = float((4 * math.pi * GK * rho * tau * alpha)[sel].max()) if sel.any() else 0.0
        dt = min(dtc, 0.2 / gam if gam > 0 else np.inf, dtmax)
        tr = np.where(ok, np.minimum(flux * dt, m[don]), 0.0)
        tr = np.where(ok & (m[don] - tr < self.thr[don]) & (tr > 0), m[don], tr)
        m = m.copy(); m[1:] -= tr; m[:-1] += tr
        sig = ok & (m[don] >= 1e-3 * self.mph[don])                 # cells that matter (CFG541's 1e-3 rule, here vs rho_ph)
        vm = float(np.max(np.where(sig, v, 0.0))) if sig.any() else 0.0
        return m, dt, vm

    def settle_inf(self, m, rta):
        """exact alpha -> inf state: CFG541 V4 inside-out minimiser (overfill kept in place)."""
        cellB = self.rf[:-1] < rta; nB = int(cellB.sum())
        q_ok = m[:nB] >= self.mph[:nB] * (1 - 1e-12)
        i0 = int(np.argmin(q_ok)) if not q_ok.all() else nB
        if i0 >= nB: return m
        Mmob = float(m[i0:nB].sum())
        need = np.maximum(self.mph[i0:nB], m[i0:nB])
        cum = np.cumsum(need)
        new = m.copy(); new[i0:nB] = 0.0
        j = int(np.searchsorted(cum, Mmob))
        if j >= len(need):
            new[i0:nB] = need; new[nB - 1] += Mmob - cum[-1]          # (cannot happen unless supply exceeds the whole target)
        else:
            new[i0:i0 + j] = need[:j]
            new[i0 + j] = Mmob - (cum[j - 1] if j > 0 else 0.0)
        return new

    def run(self, alpha, tend=None, maxsteps=4_000_000, dtcap_gyr=0.01, snaps=()):
        H = self.H; tend = H.t0 if tend is None else tend
        m = self.initial(); self.thr = 1e-14 * H.Mcat / self.N * np.ones(self.N)
        t = H.t_s; k = 0; ndep = len(self.dep_t); n = 0; vmax = 0.0
        deposited = float(m.sum()); dtcap = dtcap_gyr / TU_GYR
        inf = not np.isfinite(alpha)
        snapout = {}
        si = 0; snaps = sorted(snaps)
        while t < tend - 1e-12:
            xb = H.X_ta(t)
            if abs(xb / self.xb - 1) > 2e-3: self.set_baryons(xb)
            rta = H.r_ta(t)
            nxt = self.dep_t[k] if k < ndep else np.inf
            dtmax = min(dtcap, tend - t, max(nxt - t, 1e-9))
            if si < len(snaps): dtmax = min(dtmax, max(snaps[si] - t, 1e-9))
            if inf or alpha == 0:
                dt = dtmax
            else:
                m, dt, vm = self.flux_step(m, alpha, rta, dtmax); vmax = max(vmax, vm)
            t += dt; n += 1
            while k < ndep and self.dep_t[k] <= t + 1e-12:
                m = m + self.deposit_profile(self.dep_R[k], self.dep_m[k]); deposited += self.dep_m[k]; k += 1
            if inf: m = self.settle_inf(m, H.r_ta(t))
            while si < len(snaps) and t >= snaps[si] - 1e-12:
                snapout[snaps[si]] = m.copy(); si += 1
            if n >= maxsteps: break
        transit = float(self.dep_m[k:].sum())
        self.set_baryons(H.X_ta(t))
        return dict(m=m, t=t, n=n, hit_cap=n >= maxsteps and t < tend - 1e-9, deposited=deposited, transit=transit,
                    mass_err=abs(m.sum() + transit - H.Mcat) / H.Mcat, vmax_over_Vf=vmax / self.Vf0, snaps=snapout)

    # ---------------------------------------------------------------------------------------------------- diagnostics
    def diag(self, m, xs=(0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0)):
        rf = self.rf; rta = self.H.rta0
        Sf = np.concatenate([[0.0], np.cumsum(np.minimum(m, self.mph))])
        Mcf = np.concatenate([[0.0], np.cumsum(m)])
        lr = np.log(rf)
        at = lambda arr, x: float(np.interp(math.log(x * rta), lr, arr))
        F = {str(x): at(Sf, x) / max(at(self.Mphf - self.Mphf[0], x), 1e-300) for x in xs}
        S = {str(x): at(Sf, x) for x in xs}
        Mc = {str(x): at(Mcf, x) for x in xs}
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.where(self.mph > 0, m / self.mph, np.inf)
        def front(fr):
            bad = np.where(q < fr)[0]
            return float(rf[bad[0]] / rta) if bad.size else 1.0
        return dict(F_set=F, S=S, Mc=Mc, r_f=front(0.9), r_f50=front(0.5), r_f99=front(0.99), q=q)

    def census(self):
        """infinite-age census minimiser with the whole supply (CFG541 edge): S_cen(<r) = min(M_ph(<r), M_cat), M_b = M_b0."""
        self.set_baryons(1.0)
        Mph = self.Mphf - self.Mphf[0]
        return np.minimum(Mph, self.H.Mcat), self.H.Mcat


def alpha_sup(host, foot):
    Vf = (GK * host.Mb0 * A0K[foot]) ** 0.25
    T = host.t0 - float(np.interp(0.5, host.X, host.t_ta)); Ts = host.t0 - host.t_s
    c = 2 / (3 * math.sqrt(3))
    a1 = GK * host.Mcat / (T * Vf ** 3 * c); a2 = GK * host.Mcat / (Ts * Vf ** 3 * c)
    return dict(alpha_sup=a1, alpha_sup_Ts=a2, T_gyr=T * TU_GYR, Ts_gyr=Ts * TU_GYR, Vf_kms=Vf)
