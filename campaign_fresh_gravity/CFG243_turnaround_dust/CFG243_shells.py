#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_shells -- the spherical shell toy used by the POST-HOC gates (G0, AMOUNT, HIERARCHY ledger rows).  A fresh numpy leapfrog, modelled on
the design of CFG118 / CFG7_common's shell code (physical coordinates, Planck-like LCDM background, a static softened core for the earliest
collapsed mass, angular momentum fixed at turnaround by a pericentre bracket).  Imports CFG7_common read-only for the growth D(a) and
the committed turnaround threshold only.

WHAT THE TOY IS (declared; every item is a departure from a full simulation):
  * 1-D spherical, N baryon shells (collisionless in the toy: no gas physics), geometric in the Lagrangian radius q, masses = the cosmic
    baryon density Omega_b rho_crit; the REST of the matter (Omega_m - Omega_b) is a smooth uniform background that does NOT cluster (so the
    unperturbed flow is exactly the Friedmann flow; nothing in this toy supplies cosmic cold matter).  Radiation neglected (a_i = 0.005).
  * a static point core of mass M_b: M_pert (the excess that seeds the infall) plus M_lump (the baryons inside the radius where the initial
    linear overdensity reaches 0.25, as CFG7 caps it); M_b = M_pert + M_lump is the galaxy baryon mass used in the target.
  * the trigger: theta_b of the shell i is d ln J_i / dt with J_i = r_i^2 |r_{i+1} - r_{i-1}| (the Lagrangian volume element of equal-label
    neighbours; exact for single-stream spherical flow).  A downward zero of theta_b is a local maximum of ln J_i.  The first one fires the
    source (flag n); later ones are counted with a hysteresis (prominence p in ln J) and never create (version F).
  * the source (the AMT-2 closure, uniform-sphere form): dust of mass Q m_i with Q = a0 / (3 g_loc), created at the position and velocity of
    the baryon shell, g_loc = G DeltaM(<r)/r^2 the PECULIAR field (excess over the Hubble-flow mass), computed at the creation step.
  * j (angular momentum) is fixed at each particle's own first turnaround from a Kepler pericentre bracket r_peri/r_ta = qj, as CFG118.
Units: kpc, km/s, Msun, time kpc/(km/s) (= 0.9778 Gyr).
"""
import os, sys, math
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG243_common as C

G = C.G
GYR = C.GYR_PER_KPC_KMS
H0 = 100.0 * C.P18["h"] / 1000.0                  # km/s/kpc
OM, OB = C.OMEGA_M, C.OMEGA_B
OL = 1.0 - OM
RHOC0 = 3.0 * H0 ** 2 / (8.0 * math.pi * G)       # Msun/kpc^3
RHOM0 = OM * RHOC0
RHOB0 = OB * RHOC0
DCAP = 0.25


class Background:
    def __init__(self):
        la = np.linspace(math.log(1e-3), math.log(1.5), 8001)
        a = np.exp(la)
        H = H0 * np.sqrt(OM / a ** 3 + OL)
        # t(a) = int da/(a H); matter-era start
        f = 1.0 / H
        t = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(la))])
        t = t + 2.0 / (3.0 * H0 * math.sqrt(OM)) * a[0] ** 1.5
        self.a, self.t, self.la = a, t, la

    def a_of_t(self, t):
        return float(np.interp(t, self.t, self.a))

    def t_of_a(self, a):
        return float(np.interp(math.log(a), self.la, self.t))

    def H(self, a):
        return H0 * math.sqrt(OM / a ** 3 + OL)


BG = Background()


def lagrangian_setup(Mb, N, a_i, qmax_fac, dcap=DCAP, qj=0.1, core=True, rho_s0=None):
    """Return the initial conditions: shell edges, masses, M_pert, M_lump (core), q_ta0."""
    rho_s0 = RHOB0 if rho_s0 is None else rho_s0
    C7 = C.load_c7()
    L = C7.LCDM
    dlin_ta = float(L.delta_lin_ta(1.0))
    DD = float(L.D(1.0) / L.D(a_i))
    # M_pert + M_lump = Mb with M_lump = (Omega_b/Omega_m) M_pert / dcap  (the baryons inside the cap radius)
    ratio = rho_s0 / RHOM0 / dcap
    M_pert = Mb / (1.0 + ratio) if core else 0.0
    di_ta = dlin_ta / DD                                       # initial overdensity at the shell that turns around at a = 1
    Mm_ta = max(M_pert, 1e-30) / di_ta                         # comoving matter mass inside q_ta0
    q_ta0 = (3.0 * Mm_ta / (4.0 * math.pi * RHOM0)) ** (1.0 / 3.0)
    q_cut = q_ta0 * (di_ta / dcap) ** (1.0 / 3.0)
    if not core:                                               # control: same grid, no perturbation
        M_pert0 = Mb / (1.0 + ratio)
        Mm_ta = M_pert0 / di_ta
        q_ta0 = (3.0 * Mm_ta / (4.0 * math.pi * RHOM0)) ** (1.0 / 3.0)
        q_cut = q_ta0 * (di_ta / dcap) ** (1.0 / 3.0)
    q_max = qmax_fac * q_ta0
    e = np.geomspace(q_cut, q_max, N + 1)
    m = 4.0 * math.pi / 3.0 * rho_s0 * (e[1:] ** 3 - e[:-1] ** 3)
    q = (0.5 * (e[1:] ** 3 + e[:-1] ** 3)) ** (1.0 / 3.0)
    M_lump = 4.0 * math.pi / 3.0 * rho_s0 * q_cut ** 3
    return dict(q=q, m=m, M_pert=M_pert, M_lump=M_lump, q_ta0=q_ta0, q_cut=q_cut, q_max=q_max, Mb=Mb)


def run(Mb, a0, qj=0.1, create=True, flag=True, N=1200, a_i=0.005, qmax_fac=8.0, eta=0.04, tpct=2.0, soft=0.02,
        snap_a=(1.0,), snap_t_extra=(), hyst=(0.01, 0.05, 0.2), core=True, max_steps=2_000_000, dt_min_frac=5e-3, verbose=False,
        trigger_floor=0, creation_scale=1.0, hubble_cap=5e-4, shell_density=None):
    """integrate to the last snapshot.  Returns a dict of arrays."""
    rho_s0 = RHOB0 if shell_density is None else shell_density
    S = lagrangian_setup(Mb, N, a_i, qmax_fac, qj=qj, core=core, rho_s0=rho_s0)
    q, m, M_pert, M_lump = S["q"], S["m"], S["M_pert"], S["M_lump"]
    M_core = M_pert + M_lump
    Hi = BG.H(a_i)
    di = M_pert / (4.0 * math.pi / 3.0 * RHOM0 * q ** 3)
    rb = a_i * q * (1.0 - di / 3.0)
    vb = Hi * rb - 1.0 * Hi * di * a_i * q / 3.0
    t = BG.t_of_a(a_i)
    rM = math.sqrt(G * Mb / a0)
    dt_min = dt_min_frac * math.sqrt(rM ** 3 / (G * Mb))
    cap = N + 5
    rd = np.zeros(cap); vd = np.zeros(cap); md = np.zeros(cap); j2d = np.zeros(cap); turned_d = np.zeros(cap, bool)
    nd = 0
    j2b = np.zeros(N); turned_b = np.zeros(N, bool)
    t_ta = np.full(N, np.nan); r_ta = np.full(N, np.nan); a_ta = np.full(N, np.nan)
    t_th0 = np.full(N, np.nan); r_th0 = np.full(N, np.nan); v_th0 = np.full(N, np.nan)
    Qc = np.zeros(N); g_loc_arr = np.full(N, np.nan); trig = np.zeros(N, bool)
    ncross = {p: np.zeros(N, int) for p in hyst}
    rising = {p: np.ones(N, bool) for p in hyst}
    extreme = {p: None for p in hyst}
    nobound = 0
    th_prev = np.full(N, np.nan)
    dthdr = np.full(N, np.nan); Dthdt = np.full(N, np.nan); r_nb = np.full((N, 2), np.nan)
    soft2 = soft * soft
    four3 = 4.0 * math.pi / 3.0

    def lnJ(r):
        J = np.full(N, np.nan)
        J[1:-1] = r[1:-1] ** 2 * np.abs(r[2:] - r[:-2])
        return np.log(np.maximum(J, 1e-300))

    def acc(rb, rd, nd, a):
        rho_rest = (RHOM0 - rho_s0) / a ** 3
        rho_b = rho_s0 / a ** 3
        r_all = np.concatenate([rb, rd[:nd]])
        m_all = np.concatenate([m, md[:nd]])
        o = np.argsort(r_all, kind="stable")
        cm = M_core + np.cumsum(m_all[o]) - 0.5 * m_all[o]
        Me = np.empty_like(cm); Me[o] = cm
        r_s2 = r_all ** 2 + soft2
        a_all = -G * Me * r_all / r_s2 ** 1.5 - G * four3 * rho_rest * r_all + OL * H0 ** 2 * r_all
        dM = Me - four3 * rho_b * r_all ** 3                     # excess over the Hubble-flow mass (baryon part uniform)
        return a_all, Me, dM

    a_t = a_i
    a_all, Me, dM = acc(rb, rd, nd, a_t)
    ab = a_all[:N] + j2b / np.maximum(rb, 1e-9) ** 3
    ad = a_all[N:] + j2d[:nd] / np.maximum(rd[:nd], 1e-9) ** 3
    L_prev = lnJ(rb)
    for p in hyst:
        extreme[p] = L_prev.copy()
    snaps = []
    pending = sorted([BG.t_of_a(a) for a in snap_a] + list(snap_t_extra))
    si = 0
    nstep = 0
    ntri = 0
    while si < len(pending):
        # adaptive step: resolve the turned particles' dynamical time; Hubble-time cap
        rr = np.concatenate([rb, rd[:nd]])
        vv = np.concatenate([vb, vd[:nd]])
        tu = np.concatenate([turned_b, turned_d[:nd]])
        jj = np.concatenate([j2b, j2d[:nd]])
        r_use = np.maximum(rr, 0.5 * soft)
        gmag = G * Me / r_use ** 2 + jj / r_use ** 3
        tau = np.sqrt(r_use / np.maximum(gmag, 1e-30))
        tv = r_use / np.maximum(np.abs(vv), 1e-30)
        tt = np.minimum(tau, tv)
        if tu.sum() > 20:
            tmin = float(np.percentile(tt[tu], tpct))
        else:
            tmin = float(tt.min())
        dt = max(dt_min, eta * tmin)
        dt = min(dt, hubble_cap / BG.H(a_t), 0.02)
        last = False
        if t + dt >= pending[si] - 1e-15:
            dt = pending[si] - t
            last = True
        vb_old = vb.copy(); vd_old = vd[:nd].copy()
        vb = vb + 0.5 * dt * ab
        vd[:nd] = vd[:nd] + 0.5 * dt * ad
        rb = rb + dt * vb
        rd[:nd] = rd[:nd] + dt * vd[:nd]
        neg = rb < 0
        if neg.any():
            rb[neg] = -rb[neg]; vb[neg] = -vb[neg]
        negd = rd[:nd] < 0
        if negd.any():
            rd[:nd][negd] = -rd[:nd][negd]; vd[:nd][negd] = -vd[:nd][negd]
        t += dt
        a_t = BG.a_of_t(t)
        a_all, Me, dM = acc(rb, rd, nd, a_t)
        # ---------------- events (baryon shells): turnaround, theta_b zero crossings
        Lc = lnJ(rb)
        dl = Lc - L_prev
        # first downward zero of theta_b: raw sign change, interior shells, not yet triggered
        # (before the first maximum ln J grows monotonically, so the raw sign change is exact to one step)
        new_trig = None
        if nstep > 0:
            new_trig = (~trig) & (prev_dl_arr[0] > 0) & (dl <= 0) & np.isfinite(dl) & np.isfinite(prev_dl_arr[0])
        prev_dl_arr = [dl]
        # hysteresis counters
        for p in hyst:
            ex = extreme[p]
            ris = rising[p]
            ok = np.isfinite(Lc)
            up = ok & ris
            ex_up = np.where(up, np.maximum(ex, Lc), ex)
            cnt = up & (Lc < ex_up - p)
            ncross[p] += cnt
            dn = ok & (~ris)
            ex_dn = np.where(dn, np.minimum(ex, Lc), ex_up)
            rev = dn & (Lc > ex_dn + p)
            ris_new = np.where(cnt, False, np.where(rev, True, ris))
            ex_new = np.where(cnt, Lc, np.where(rev, Lc, np.where(up, ex_up, np.where(dn, ex_dn, ex))))
            rising[p] = ris_new
            extreme[p] = ex_new
        theta_now = dl / dt
        L_prev = Lc
        # ---------------- the source
        if new_trig is not None and new_trig.any():
            idx = np.where(new_trig)[0]
            trig[idx] = True
            t_th0[idx] = t; r_th0[idx] = rb[idx]; v_th0[idx] = vb[idx]
            g = G * dM[idx] / np.maximum(rb[idx], 1e-9) ** 2
            g_loc_arr[idx] = g
            ii_ = idx[(idx > 1) & (idx < N - 2)]
            dthdr[ii_] = (theta_now[ii_ + 1] - theta_now[ii_ - 1]) / (rb[ii_ + 1] - rb[ii_ - 1])
            Dthdt[ii_] = (theta_now[ii_] - th_prev[ii_]) / dt
            g_loc_arr[idx] = g
            if create:
                okq = g > 0
                for ii, gg, ok in zip(idx, g, okq):
                    if not ok or nd >= cap:
                        continue
                    Q = creation_scale * a0 / (3.0 * gg)
                    Qc[ii] = Q
                    rd[nd] = rb[ii]; vd[nd] = vb[ii]; md[nd] = Q * m[ii]
                    if vb[ii] <= 0 and turned_b[ii]:
                        j2d[nd] = j2b[ii]; turned_d[nd] = True
                    elif vb[ii] <= 0:
                        gq = gg
                        j2d[nd] = 2.0 * gq * rb[ii] ** 3 * qj / (1.0 + qj); turned_d[nd] = True
                    nd += 1
                a_all, Me, dM = acc(rb, rd, nd, a_t)
        th_prev = theta_now
        ab = a_all[:N] + j2b / np.maximum(rb, 1e-9) ** 3
        ad = a_all[N:] + j2d[:nd] / np.maximum(rd[:nd], 1e-9) ** 3
        vb = vb + 0.5 * dt * ab
        vd[:nd] = vd[:nd] + 0.5 * dt * ad
        # ---------------- turnaround events, detected on the FULL-step velocities (v_old at the step start, v at its end)
        newt = (~turned_b) & (vb_old > 0) & (vb <= 0)
        if newt.any():
            g = G * dM[:N][newt] / np.maximum(rb[newt], 1e-9) ** 2
            okg = g > 0
            jj2 = np.where(okg, 2.0 * g * rb[newt] ** 3 * qj / (1.0 + qj), 0.0)
            nobound += int((~okg).sum())
            j2b[newt] = jj2
            turned_b |= newt
            t_ta[newt] = t; r_ta[newt] = rb[newt]; a_ta[newt] = a_t
            ab = a_all[:N] + j2b / np.maximum(rb, 1e-9) ** 3
        if nd:
            vd_old_ = vd_old if len(vd_old) == nd else np.concatenate([vd_old, np.full(nd - len(vd_old), np.inf)])
            newd = (~turned_d[:nd]) & (vd_old_ > 0) & (vd[:nd] <= 0)
            if newd.any():
                g = G * dM[N:][newd] / np.maximum(rd[:nd][newd], 1e-9) ** 2
                jj2 = np.where(g > 0, 2.0 * g * rd[:nd][newd] ** 3 * qj / (1.0 + qj), 0.0)
                j2d[:nd][newd] = jj2
                turned_d[:nd] |= newd
                ad = a_all[N:] + j2d[:nd] / np.maximum(rd[:nd], 1e-9) ** 3
        nstep += 1
        if nstep > max_steps:
            raise RuntimeError("step budget exceeded")
        if verbose and nstep % 20000 == 0:
            print(f"   step {nstep} a={a_t:.4f} nd={nd} dt={dt:.2e}", flush=True)
        if last:
            snaps.append(dict(t=t, a=a_t, rb=rb.copy(), vb=vb.copy(), rd=rd[:nd].copy(), vd=vd[:nd].copy(), md=md[:nd].copy(), Me_b=Me[:N].copy(),
                              dM_b=dM[:N].copy()))
            si += 1
    return dict(S=S, snaps=snaps, t_ta=t_ta, r_ta=r_ta, a_ta=a_ta, t_th0=t_th0, r_th0=r_th0, v_th0=v_th0, Q=Qc, g_loc=g_loc_arr, trig=trig,
                ncross=ncross, nstep=nstep, nd=nd, m=m, q=q, nobound=nobound, M_core=M_core, rM=rM, md=md[:nd].copy(),
                turned_b=turned_b, dthdr=dthdr, Dthdt=Dthdt)
