#!/usr/bin/env python3
"""CFG648 library (FROZEN_CRITERIA.md, 2e9dffba1): phase-mixed settling H-SP on CFG637's self-similar infall solver.

InfallSP subclasses cfg637_lib.Infall (imported read-only). With hsp=False every method falls through to CFG637's code path
unchanged (MUTATE M-ta). With hsp=True it adds only:
  * pericentre / first-apocentre tracking per Lagrangian shell (radial-velocity sign changes after turnaround);
  * r_sp(t): PRIMARY 'max' = largest current radius among shells past pericentre (outermost caustic); bracket 'apo' = median
    first-apocentre radius of shells whose first apocentre fell within the last dln a = 0.1 (latest apocentre if none);
    the settling cut uses the running maximum r_sp,eff (settled cold energy is never taken back, R5);
  * the settled target = law phantom of the source truncated at min(supply edge, r_sp,eff), confined to r_ta, applied LIVE;
  * draw: PRIMARY 'phase' = outer-first from the cold weight of shells past pericentre; bracket 'R5lit' = CFG637's rule with the
    edge replaced by min(edge, r_sp,eff);
  * read-out: phase-mixed reservoir shells orbit-averaged (CFG637 routine), first-infall shells at their current radius;
  * Gamma = dln M_ta / dln a over the last dln a = 0.4 (turned-around mass history).
Seed: power law eps (CFG637) or a tabulated shape delta_L(M/M_ta) (CFG557 EPS, CONTEXT) via seed=callable(x)->shape.
Units: kpc, Msun, Gyr (cfg637_lib).  kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LANES, "CFG637_derived_reservoir"))
import cfg637_lib as L                                                        # noqa: E402

G, OM, OL, H0, RHOC0, FB, COLD_PER_B = L.G, L.OM, L.OL, L.H0, L.RHOC0, L.FB, L.COLD_PER_B
GAMMA_DLNA = 0.4
APO_WINDOW = 0.1


class InfallSP(L.Infall):
    def __init__(self, M_ta, fret, x_core, S_core, S_src, a0, nu, hsp=True, rsp_mode="max", draw_sp="phase", seed=None,
                 **kw):
        super().__init__(M_ta, fret, x_core, S_core, S_src, a0, nu, **kw)
        self.hsp, self.rsp_mode, self.draw_sp, self.seed = hsp, rsp_mode, draw_sp, seed
        if seed is not None:                       # tabulated seed shape (normalisation delta0 as in CFG637)
            delta = np.minimum(self.delta0 * seed(self.Mk / M_ta) / seed(1.0), L.DELTA_CAP)
            self.r, self.v = L.initial_shell(self.Mk, delta)
        N = len(self.r)
        self.peri = np.zeros(N, bool); self.apo_r = np.full(N, np.nan); self.apo_a = np.full(N, np.nan)
        self.rsp_eff = 0.0; self.rsp_inst = 0.0; self.excess_drawn = 0.0; self.hist_a, self.hist_M = [], []
        self.peri_t = np.full(N, np.nan); self.apo_t = np.full(N, np.nan)
        self.rta_i = np.full(N, np.inf)            # each shell's own turnaround radius (scattering guard, disclosed)
        self.n_scattered = 0

    # ------------------------------------------------------------------ r_sp
    def _rsp_now(self, a_now):
        # POST-FREEZE ENGINEERING GUARD (disclosed): in a potential that only deepens, a collisionless shell past pericentre
        # cannot exceed its own turnaround radius; shells that do were scattered numerically through the softened centre and
        # are excluded from the caustic statistic (counted in n_scattered).
        bad = self.peri & (self.r > self.rta_i)
        self.n_scattered = max(self.n_scattered, int(bad.sum()))
        pm = self.peri & ~bad
        if not pm.any():
            return 0.0
        if self.rsp_mode == "max":
            return float(self.r[pm].max())
        ok = np.isfinite(self.apo_a) & ~(self.apo_r > self.rta_i)
        if not ok.any():
            return 0.0
        rec = ok & (np.log(a_now / np.where(ok, self.apo_a, a_now)) <= APO_WINDOW)
        if rec.any():
            return float(np.median(self.apo_r[rec]))
        k = np.nanargmax(self.apo_a)
        return float(self.apo_r[k])

    # ------------------------------------------------------------------ settled profile with the H-SP cut
    def core_set(self, r, rta, Mret_turned, cold_turned, draw=True):
        if not self.hsp:
            return super().core_set(r, rta, Mret_turned, cold_turned, draw)
        xg = self.x_core
        Mc = Mret_turned * self.S_core
        Ms = Mret_turned * self.S_src
        # R2 under H-SP: the supply available for settling is the cold energy of phase-mixed shells (drawn + remaining)
        # for the PRIMARY draw; the bracket R5lit keeps CFG637's supply (all turned-around cold energy)
        sup = cold_turned
        if self.draw_sp == "phase":
            sup = min(cold_turned, self.drawn + float(self.m_cold[self.turned & self.peri].sum()))
        mph, xe = L.phantom_trunc(xg, Ms, rta, self.a0, self.nu, sup)
        self._xe_sp = xe
        xs = self.rsp_eff / rta
        if xs < 1.0:
            mcut = float(np.interp(xs, xg, mph))
            mph = np.where(xg > xs, mcut, mph)
        self._xcut = min(xs, xe if xe is not None else np.inf, 1.0)
        return Mc, mph, float(mph[-1]), xe

    def _accel(self, rta, Mret_t, cold_t, draw):
        if not self.hsp:
            return super()._accel(rta, Mret_t, cold_t, draw)
        r = self.r
        if rta is not None:
            Mc, mph, target, xe = self.core_set(r, rta, Mret_t, cold_t)
            if draw and target > self.drawn:
                dS = target - self.drawn
                if self.draw_sp == "phase":
                    elig = np.where(self.turned & self.peri & (self.m_cold > 0))[0]
                else:                                                   # R5lit: CFG637's rule, edge -> min(edge, r_sp)
                    elig = None
                    rc = self._xcut * rta
                    if self._xcut < 1.0:
                        el = self.turned & (self.m_cold > 0) & (r >= rc) & (r <= rta * 1.0000001)
                        avail = float(self.m_cold[el].sum()); take = min(dS, avail)
                        if avail > 0:
                            self.m_cold[el] *= (1 - take / avail)
                    else:
                        elig = np.where(self.turned & (self.m_cold > 0))[0]
                if elig is not None:
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
            if target > 0 and self.drawn > target:
                self.excess_drawn = max(self.excess_drawn, (self.drawn - target) / target)
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

    # ------------------------------------------------------------------ run (CFG637's loop + tracking)
    def run(self):
        if not self.hsp:
            super().run()
            return self
        t = float(L.t_of_a(L.A_INIT)); t_obs = float(L.t_of_a(self.a_obs))
        avgM = None; avg_w = 0.0; self.rgrid_avg = None; nstep = 0; rta = None
        while t < t_obs:
            tt = self.turned
            if tt.any():
                k_last = np.max(np.where(tt)[0]); rta = float(self.r[k_last])
            a_now = float(L.a_of_t(t))
            self.rsp_inst = self._rsp_now(a_now); self.rsp_eff = max(self.rsp_eff, self.rsp_inst)
            Mret_t = float(self.m_bret[tt].sum()); cold_t = float((self.dm[tt] * (1 - FB)).sum())
            acc, Menc = self._accel(rta, Mret_t, cold_t, draw=True)
            rr = np.sqrt(self.r ** 2 + (self.soft_x * (rta if rta else self.r[-1])) ** 2)
            tdyn = np.sqrt(rr ** 3 / (G * np.maximum(Menc, 1e-30)))
            sel = self.r > 0.004 * (rta if rta else 0.0)
            dt = min(self.C_dyn * float(np.min(tdyn[sel])), 0.01 * t, t_obs - t)
            vold = self.v.copy(); turned_before = self.turned.copy()
            self.v += 0.5 * dt * acc
            self.r = np.abs(self.r + dt * self.v)
            t += dt
            acc2, Menc = self._accel(rta, Mret_t, cold_t, draw=False)
            self.v += 0.5 * dt * acc2
            new = (~self.turned) & (self.v <= 0)
            if new.any():
                self.turned |= new
                self.j2[new] = 2 * G * Menc[new] * self.r[new] * self.q / (1 + self.q)
                self.rta_i[new] = self.r[new]
            a_now = float(L.a_of_t(t))
            pnew = turned_before & (~self.peri) & (vold < 0) & (self.v >= 0)
            if pnew.any():
                self.peri |= pnew; self.peri_t[pnew] = t
            anew = self.peri & (~pnew) & np.isnan(self.apo_r) & (vold > 0) & (self.v <= 0)
            if anew.any():
                self.apo_r[anew] = self.r[anew]; self.apo_a[anew] = a_now; self.apo_t[anew] = t
            self.hist_a.append(a_now); self.hist_M.append(float(self.dm[self.turned].sum()))
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
        self.nstep = nstep; self.t_obs = t_obs
        tt = self.turned
        k_last = np.max(np.where(tt)[0]); self.rta = float(self.r[k_last])
        self.M_turned = float(self.dm[tt].sum())
        self.M_res_avg = avgM / avg_w if avg_w > 0 else None
        Mret_t = float(self.m_bret[tt].sum()); cold_t = float((self.dm[tt] * (1 - FB)).sum())
        self.Mret_t, self.cold_t = Mret_t, cold_t
        Mc, mph, target, xe = self.core_set(None, self.rta, Mret_t, cold_t)
        self.settle_target, self.x_edge = target, xe
        self.supply_turned = cold_t
        Ms = Mret_t * self.S_src
        self.x_edge_B = L.phantom_trunc(self.x_core, Ms, self.rta, self.a0, self.nu, cold_t)[1]
        self.Mset_B_target = float(L.phantom_trunc(self.x_core, Ms, self.rta, self.a0, self.nu, cold_t)[0][-1])
        return self

    def gamma(self):
        if not self.hist_a:
            return float("nan")
        a = np.array(self.hist_a); M = np.array(self.hist_M)
        a1 = self.a_obs * math.exp(-GAMMA_DLNA)
        M1 = float(np.interp(a1, a, M)); M2 = float(M[-1])
        return math.log(M2 / M1) / GAMMA_DLNA if M1 > 0 else float("nan")

    def final_profile(self, nr=500, ntheta=160):
        if not self.hsp:
            return super().final_profile(nr, ntheta)
        # identical to CFG637's routine except: first-infall reservoir shells are placed at their current radius
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
        Phi = np.zeros(nr)
        Phi[-1] = -G * Mtot[-1] / rg[-1] - 0.5 * OL * H0 ** 2 * rg[-1] ** 2
        seg = 0.5 * (g[1:] + g[:-1]) * np.diff(rg)
        Phi[:-1] = Phi[-1] - np.cumsum(seg[::-1])[::-1]
        self.rg, self.Mtot_g, self.Phi_g = rg, Mtot, Phi
        res = np.where(self.turned & (self.m_cold > 0))[0]
        lrg = np.log(rg)
        Mres = np.zeros(nr); Etot = 0.0; Mres_pm = np.zeros(nr)
        th = (np.arange(ntheta) + 0.5) / ntheta * math.pi
        for i in res:
            ri, vi, j2, m = self.r[i], self.v[i], self.j2[i], self.m_cold[i]
            Etot += m * (0.5 * vi ** 2 + 0.5 * j2 / ri ** 2 + np.interp(np.log(max(ri, rg[0])), lrg, Phi))
            if not self.peri[i]:
                Mres += m * (rg >= ri); continue
            Pe = np.interp(np.log(max(ri, rg[0])), lrg, Phi) + 0.5 * j2 / ri ** 2
            E = 0.5 * vi ** 2 + Pe
            f = E - (Phi + 0.5 * j2 / rg ** 2)
            ki = int(np.searchsorted(rg, ri)); ki = min(max(ki, 1), nr - 1)
            below = np.where(f[:ki] < 0)[0]; above = np.where(f[ki:] < 0)[0]
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
                Mres += m * (rg >= ri); Mres_pm += m * (rg >= ri); continue
            cw = np.cumsum(w) / w.sum()
            add = m * np.interp(rg, rr, cw, left=0.0, right=1.0)
            Mres += add; Mres_pm += add
        self.M_res_g = Mres; self.M_res_pm_g = Mres_pm
        self.E_res = Etot
        self.M_res_tot = float(self.m_cold[res].sum())
        self.M_res_firstinfall = float(self.m_cold[res][~self.peri[res]].sum())
        return self

    def sp_summary(self):
        d = self.summary()
        if self.hsp:
            pm = self.peri
            d.update(rsp_eff_kpc=self.rsp_eff, rsp_inst_kpc=self.rsp_inst, s=self.rsp_eff / self.rta, s_inst=self.rsp_inst / self.rta,
                     x_cut=min(self.rsp_eff / self.rta, self._xe_sp if self._xe_sp is not None else np.inf, 1.0),
                     n_peri=int(pm.sum()), frac_turned_mass_peri=float(self.dm[pm].sum() / self.dm[self.turned].sum()),
                     excess_drawn=self.excess_drawn, gamma=self.gamma(), n_scattered=self.n_scattered,
                     x_edge_B=self.x_edge_B, x_edge_sp=self._xe_sp, settled_over_Btarget=self.drawn / max(self.Mset_B_target, 1e-30),
                     final_shortfall=1 - self.drawn / max(self.settle_target, 1e-30),
                     res_firstinfall_frac=getattr(self, "M_res_firstinfall", 0.0) / max(self.supply_turned, 1e-30))
            # phase-mixing time of the shells near r_sp: pericentre -> first apocentre (Gyr)
            ok = np.isfinite(self.apo_t) & np.isfinite(self.peri_t)
            if ok.any():
                k = np.argsort(-self.apo_a[ok])[:20]
                d["t_peri_to_apo_gyr_recent"] = float(np.median((self.apo_t[ok] - self.peri_t[ok])[k]))
                d["t_ta_to_peri_gyr_proxy"] = None
            else:
                d["t_peri_to_apo_gyr_recent"] = None
        return d


def derive_sp(M_ta, fret, r_obs, Mcore_obs, Msrc_obs, a0, nu, a_obs=1.0, tol=0.01, **kw):
    """CFG637's derive() with InfallSP (identical iteration on delta0)."""
    rta_p, d0 = L.r_ta_single(M_ta, a_obs)
    x = np.geomspace(1e-4, 4.0, 700)
    Mtot = float(Mcore_obs[-1])
    Sc = np.interp(x * rta_p, r_obs, Mcore_obs, left=0.0, right=Mcore_obs[-1]) / Mtot
    Ss = np.interp(x * rta_p, r_obs, Msrc_obs, left=0.0, right=Msrc_obs[-1]) / Mtot
    hist = []
    d = d0
    for it in range(6):
        I = InfallSP(M_ta, fret, x, Sc, Ss, a0, nu, a_obs=a_obs, delta0=d, **kw).run()
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


def eps_seed(X, dL):
    """seed shape callable from a tabulated delta_L(x) (x = M/M_ta); power-law extrapolation at both ends."""
    lx, ld = np.log(X), np.log(dL)
    s_lo = np.polyfit(lx[:10], ld[:10], 1)[0]; s_hi = np.polyfit(lx[-20:], ld[-20:], 1)[0]

    def f(x):
        x = np.asarray(x, float); l = np.log(np.maximum(x, 1e-300))
        out = np.interp(l, lx, ld)
        out = np.where(l < lx[0], ld[0] + s_lo * (l - lx[0]), out)
        out = np.where(l > lx[-1], ld[-1] + s_hi * (l - lx[-1]), out)
        return np.exp(out)
    f.slope_hi = s_hi; f.slope_lo = s_lo
    return f


def esd(rg, Mtot, a_obs, R):
    """excess surface density Delta Sigma(R) (Msun/kpc^2) of the excess over the mean matter density, projected to rg[-1]."""
    rhob = OM * RHOC0 / a_obs ** 3
    rho = np.gradient(Mtot, rg) / (4 * math.pi * rg ** 2) - rhob
    lr = np.log(rg)
    zmax = rg[-1]
    zz = np.geomspace(1e-3, zmax, 1500)

    def Sig(Rv):
        rr = np.sqrt(Rv ** 2 + zz ** 2); ok = rr < rg[-1]
        return 2 * np.trapz(np.where(ok, np.interp(np.log(np.minimum(rr, rg[-1])), lr, rho), 0.0), zz)
    Rg = np.geomspace(min(rg[0], 0.5 * np.min(R)), np.max(R), 300)
    S = np.array([Sig(x) for x in Rg])
    cum = np.r_[0.0, np.cumsum(0.5 * (S[1:] * Rg[1:] + S[:-1] * Rg[:-1]) * np.diff(Rg))] * 2 * math.pi
    Mbar = cum + S[0] * math.pi * Rg[0] ** 2
    out = []
    for x in np.atleast_1d(R):
        out.append(np.interp(x, Rg, Mbar) / (math.pi * x ** 2) - np.interp(x, Rg, S))
    return np.array(out)
