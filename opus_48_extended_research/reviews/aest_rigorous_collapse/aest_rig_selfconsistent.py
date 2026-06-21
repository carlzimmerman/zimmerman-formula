#!/usr/bin/env python3
"""
CAVEAT 1: SELF-CONSISTENT N-shell collapse  r'' = -g_AeST  (NOT the cosine proxy).
==================================================================================
The prior scalar-only solve (aest_collapse_solve.py L311-324) PRESCRIBED r_phys via a cosine
contraction; r''=-g was never integrated. Here each Lagrangian shell falls under its OWN
live AeST gravity, with the enclosed mass M_b(<r,t) recomputed from instantaneous shell
positions every step (shell crossing -> multi-stream native). The AeST scalar force g_phi
is solved from the real DS24 field at each step. We then drive the time-dependent KG chi
wave with the SELF-CONSISTENT density history rho_b(r,t) and ask: does the late-time
oscillation phase converge (pin) or track the IC phase (no-go)?

This is caveat-1 AND caveat-3(A) (radial multi-stream) together: the self-consistent bounce
spectrum + the {omega_i} spread of crossing shells. Caveats 2+3(B,C) (vector / non-radial)
are in aest_rig_nonradial_vector.py.

BOTH-WAYS / QUARANTINE per aest_rig_core.py.
"""
import numpy as np, functools
from scipy.integrate import solve_ivp
from aest_rig_core import (c, G_N, Msun, kpc, Mpc, a0, H0, OL, Om_m, Om_aest, Gyr,
                           mu_of, xinv, integrate_static, g_mond_arr, g_aest_static,
                           fit_oscillation_phase, circ_std, slope_theta_vs_ic,
                           t_of_a, H_of_a)
print = functools.partial(print, flush=True)


# ============================================================ N-shell self-consistent collapse
class SelfConsistentCollapse:
    """N onion shells, r'' = -g_AeST(r,t), live M_b(<r), shell crossing native."""
    def __init__(self, Mtot_Msun, R500_phys, n_shell=40, inv_mu_Mpc=1.0,
                 z_dec=20.0, delta_amp=1.0, profile='tophat', seed=0):
        self.Mtot = Mtot_Msun*Msun; self.R500 = R500_phys; self.n = n_shell
        self.mu = mu_of(inv_mu_Mpc); self.mu2 = self.mu**2
        self.a_dec = 1.0/(1+z_dec); self.profile = profile; self.seed = seed
        rng = np.random.default_rng(seed)
        Mfrac = np.linspace(1.0/self.n, 1.0, self.n)
        self.M_i = Mfrac*self.Mtot                 # enclosed Lagrangian mass per shell
        # comoving Lagrangian radius from cosmic mean density
        rho_mean0 = Om_m*3*H0**2/(8*np.pi*G_N)
        R_lag = (3*self.Mtot/(4*np.pi*rho_mean0))**(1/3.)
        if profile == 'tophat':
            q = Mfrac**(1/3.)
        elif profile == 'nfw':
            cc=5.0
            def mnfw(x): return np.log(1+cc*x)-cc*x/(1+cc*x)
            xs=np.geomspace(1e-3,1,4000); mm=mnfw(xs)/mnfw(1.0); q=np.interp(Mfrac,mm,xs)
        elif profile == 'hernquist':
            ah=0.45; q=ah*np.sqrt(Mfrac)/(1-np.sqrt(Mfrac)); q/=q[-1]
        else: raise ValueError(profile)
        self.r_com = q*R_lag
        # initial overdensity (linear) at z_dec, scaled by delta_amp; small per-shell scatter
        self.delta_dec = 1.686*self.a_dec*1.2*delta_amp
        self.delta_shell = self.delta_dec*(1.0 + 0.02*rng.standard_normal(self.n))

    # ---- live enclosed-mass + density from instantaneous shell positions ----
    def Menc_func(self, r_shells):
        order = np.argsort(r_shells)
        rs = np.concatenate([[0.0], r_shells[order]])
        Ms = np.concatenate([[0.0], np.cumsum(self.M_i_per[order])])
        Ms = np.maximum.accumulate(Ms)
        def Menc(r): return np.interp(r, rs, Ms, left=0.0, right=Ms[-1])
        return Menc

    def rho_b_func(self, r_shells):
        order = np.argsort(r_shells); rs = r_shells[order]
        dM = self.M_i_per[order]
        rs_e = np.concatenate([[0.0], rs])
        Vsh = (4*np.pi/3.)*(rs_e[1:]**3 - rs_e[:-1]**3)
        rho_sh = dM/np.maximum(Vsh, 1e-30)
        rc = 0.5*(rs_e[1:]+rs_e[:-1])
        def rho_b(r):
            r=np.atleast_1d(r); out=np.interp(r, rc, rho_sh, left=rho_sh[0], right=0.0)
            return out if out.size>1 else out[0]
        return rho_b

    # ---- AeST radial accel at shell radii (static-per-step) ----
    def g_aest_at(self, r_shells, use_mass_term=True, use_scipy=False):
        mu2 = self.mu2 if use_mass_term else 0.0
        Menc = self.Menc_func(r_shells); rho_b = self.rho_b_func(r_shells)
        rs = np.sort(r_shells); rs = rs[rs>0]
        if rs.size == 0: return np.zeros_like(r_shells)
        r0 = max(0.5*rs[0], 0.01*self.R500); r1 = max(4*rs[-1], 2*r0)
        # use_scipy=False -> RK4 (scipy-free) so it is safe to call every collapse step
        gq,_ = g_aest_static(np.clip(r_shells, r0, r1), rho_b, Menc, mu2, r0, r1,
                             n=1200, use_scipy=use_scipy)
        return gq

    def g_force(self, r, a_now=1.0, use_mass_term=False, mond=True):
        """PHYSICAL spherical-collapse acceleration on each shell (inward positive):
          g = G * dM_excess(<r) / r^2  [MOND-boosted]  -  (Lambda c^2/3) r   [cosmo repulsion]
        dM_excess = M_baryon(<r) - (cosmic mean enclosed in r) -- the shell responds to the
        OVERDENSITY, not the absolute mass (standard spherical collapse). The Lambda term +
        the mean-density subtraction give a finite turnaround + virial radius (no free-fall
        to r=0). Robust closed-form -> stable Verlet (scipy-free)."""
        from aest_rig_core import OL
        r = np.clip(r, 1e-6*self.R500, None)
        Menc = self.Menc_func(r)
        Me = np.array([Menc(ri) for ri in r])
        # cosmic-mean mass enclosed in physical radius r at scale factor a_now
        rho_mean = Om_m*3*H0**2/(8*np.pi*G_N)/a_now**3
        Mmean = (4*np.pi/3.)*rho_mean*r**3
        dM = Me - Mmean                                    # mass excess (can be <0 outer)
        # Newtonian baseline g_N from the EXCESS; MOND-boost the magnitude, keep the sign
        gN = G_N*dM/r**2
        if mond:
            g_grav = np.sign(gN)*a0*xinv(np.abs(gN)/a0)    # deep-MOND interpolation, signed
        else:
            g_grav = self.g_aest_at(r, use_mass_term=use_mass_term, use_scipy=False)
        Lam = 3.0*OL*H0**2/c**2
        g_cosmo = -(Lam*c**2/3.0)*r                        # cosmological repulsion (outward)
        return g_grav + g_cosmo

    def run(self, n_t=400, use_mass_term=False, mond=True, virialize=True):
        """Integrate r_i'' = -g via velocity-Verlet (scipy-FREE -> no f2py reentrancy).
        Live M_b(<r) recomputed every step (self-consistency); shell crossing native.
        Virialization: a shell that has passed turnaround and recollapsed to ~r_ta/2 is
        capped at its virial radius (prevents unphysical free-fall to r=0; standard
        spherical-collapse closure). r_vir is set per shell at first pericenter."""
        self.M_i_per = np.diff(np.concatenate([[0.0], self.M_i]))
        a_arr = np.geomspace(self.a_dec, 1.0, n_t); t_arr = t_of_a(a_arr)
        r = self.r_com*self.a_dec*(1.0 - self.delta_shell/3.0)
        v = H_of_a(self.a_dec)*r*(1.0 - self.delta_shell/3.0)   # seed infall
        r_hist=np.empty((n_t, self.n)); v_hist=np.empty((n_t, self.n))
        r_hist[0]=r; v_hist[0]=v
        r_ta = np.full(self.n, np.nan); turned = np.zeros(self.n, bool)
        r_vir = np.full(self.n, np.nan)
        g = self.g_force(r, a_now=a_arr[0], use_mass_term=use_mass_term, mond=mond)
        for k in range(1, n_t):
            dt = t_arr[k]-t_arr[k-1]; a_now = a_arr[k]
            nsub = max(1, int(dt/(0.01*Gyr))); dts = dt/nsub
            for _ in range(nsub):
                r = r + v*dts + 0.5*(-g)*dts**2
                r = np.clip(r, 1e-6*self.R500, None)
                g_new = self.g_force(r, a_now=a_now, use_mass_term=use_mass_term, mond=mond)
                v = v + 0.5*(-(g+g_new))*dts
                g = g_new
                if virialize:
                    # detect turnaround (v changes sign + -> -) and set r_ta, r_vir=r_ta/2
                    new_turn = (~turned) & (v < 0) & (k > 2)
                    r_ta[new_turn] = r[new_turn]; turned |= new_turn
                    r_vir[turned] = 0.5*r_ta[turned]
                    # cap recollapsed shells at r_vir (virial equilibrium)
                    hit = turned & (r < r_vir)
                    r[hit] = r_vir[hit]; v[hit] = 0.0
            r_hist[k]=r; v_hist[k]=v
        return a_arr, t_arr, r_hist, v_hist


# ============================================================ time-dependent chi wave
def evolve_chi_wave(source_of_t, r_grid, t_grid, mu, cs, ic_phase=0.0, ic_amp=1.0,
                    damping=0.0, sommerfeld=True, nu_num=0.0):
    """
    chi_tt + 2*damping*chi_t - cs^2 lap(chi) + (mu c)^2 chi = S(r,t) + nu_num*lap(chi_t)
    Conservative AeST wave (damping=0 physical). ic_phase seeds the FREE mode phase.
    nu_num is an ARTIFICIAL numerical viscosity (0 physical) -- the adversarial knob.
    """
    Nr = len(r_grid); dr = r_grid[1]-r_grid[0]; om2 = (mu*c)**2
    # seed the free oscillation with the given IC phase (a localized standing chi)
    env = np.exp(-((r_grid - r_grid[Nr//4])/(0.3*(r_grid[-1]-r_grid[0])))**2)
    chi = ic_amp*np.cos(ic_phase)*env
    chidot = -ic_amp*(mu*c)*np.sin(ic_phase)*env
    def lap(f):
        L=np.zeros_like(f)
        L[1:-1]=(f[2:]-2*f[1:-1]+f[:-2])/dr**2 + (2.0/r_grid[1:-1])*(f[2:]-f[:-2])/(2*dr)
        L[0]=6.0*(f[1]-f[0])/dr**2; L[-1]=L[-2]; return L
    dt=t_grid[1]-t_grid[0]; cfl=cs*dt/dr
    nsub = int(np.ceil(cfl/0.4)) if cfl>0.4 else 1; dtl=dt/nsub
    rlo, rhi = r_grid[Nr//3], r_grid[2*Nr//3]
    iprobe = Nr//3                                    # fixed interior probe radius
    hist_t=[]; hist_th=[]; hist_A=[]; hist_probe=[]
    for it,t in enumerate(t_grid):
        S=source_of_t(t, r_grid)
        for _ in range(nsub):
            L=lap(chi); Ld=lap(chidot)
            acc=cs**2*L - om2*chi + S - 2*damping*chidot + nu_num*Ld
            chidot=chidot+acc*dtl; chi=chi+chidot*dtl
            if sommerfeld:
                # outgoing: chi_t = -cs chi_r at outer edge (kills reflection)
                chi[-1]=chi[-2]-cs*dtl*(chi[-2]-chi[-3])/dr
            else:
                chi[-1]=chi[-2]
        A,th=fit_oscillation_phase(r_grid, chi, mu, (rlo,rhi))
        hist_t.append(t); hist_th.append(th); hist_A.append(A); hist_probe.append(chi[iprobe])
    return dict(chi=chi, t=np.array(hist_t), theta=np.array(hist_th),
                amp=np.array(hist_A), probe=np.array(hist_probe))


# ============================================================ driver
def run_selfconsistent(Mtot_Msun=1e14, R500_Mpc=1.3, n_shell=40, z_dec=20.0,
                       delta_amp=1.0, profile='tophat', ic_phase=0.0, seed=0,
                       inv_mu_Mpc=1.0, damping=0.0, nu_num=0.0, verbose=False):
    cl = SelfConsistentCollapse(Mtot_Msun, R500_Mpc*Mpc, n_shell=n_shell,
                                z_dec=z_dec, delta_amp=delta_amp, profile=profile,
                                inv_mu_Mpc=inv_mu_Mpc, seed=seed)
    # SELF-CONSISTENT collapse (mu=0 force on the shells -- MOND/AeST; mass term tiny on shells)
    a_arr, t_arr, r_hist, v_hist = cl.run(n_t=400, use_mass_term=False)
    n_cross = int(np.sum(np.diff(np.argsort(r_hist[-1])) != 1) > 0)  # shell-crossing flag
    # diagnostic: number of shell-crossing events over the history
    cross_events = 0
    for k in range(1, r_hist.shape[0]):
        order_prev = np.argsort(r_hist[k-1]); order_now = np.argsort(r_hist[k])
        cross_events += np.sum(order_prev != order_now)
    # build self-consistent density-history source for the chi wave (NORMALIZED so the
    # forced response is O(1), commensurate with an O(1) IC free-mode seed -- otherwise a
    # huge forced DC numerically swamps the IC phase and FAKES a pin).
    lam_mu = 2*np.pi/cl.mu; Rmax = max(3*cl.R500, 2.5*lam_mu)
    r_grid = np.linspace(0.05*cl.R500, Rmax, 360)
    cl.M_i_per = np.diff(np.concatenate([[0.0], cl.M_i]))
    # source amplitude scale = peak |4 pi G rho_b| over the history (for normalization)
    Speak = 0.0
    for k in range(r_hist.shape[0]):
        rho = cl.rho_b_func(r_hist[k])(r_grid)
        Speak = max(Speak, np.max(np.abs(4*np.pi*G_N*rho)))
    Speak = max(Speak, 1e-40)
    def source_of_t(t, rg, scale=1.0):
        k = np.argmin(np.abs(t_arr - t)); rs = r_hist[k]
        rho = cl.rho_b_func(rs)(rg)
        return scale*(4*np.pi*G_N*np.atleast_1d(rho))/Speak    # O(1) normalized source
    T_mu = 2*np.pi/(cl.mu*c); cs = c
    t0,t1 = t_arr[0], t_arr[-1]
    nt = min(int((t1-t0)/(T_mu/20.0)), 24000)
    t_wave = np.linspace(t0, t1, nt)
    # RIGOROUS free-mode isolation: run (forced + IC seed) and (forced only), DIFFERENCE to
    # extract the IC-seeded free mode, then measure ITS late phase vs ic_phase.
    w_seed = evolve_chi_wave(source_of_t, r_grid, t_wave, cl.mu, cs,
                             ic_phase=ic_phase, ic_amp=1.0, damping=damping, nu_num=nu_num)
    w_forced = evolve_chi_wave(source_of_t, r_grid, t_wave, cl.mu, cs,
                               ic_phase=0.0, ic_amp=0.0, damping=damping, nu_num=nu_num)
    # isolate the IC-seeded FREE mode = (seeded probe) - (forced probe), then TEMPORAL-demod
    # against the carrier mu c over the late window (robust; avoids catastrophic cancellation
    # vs the forced response, and is the same method validated in the adversarial analytic test)
    probe_free = w_seed['probe'] - w_forced['probe']
    tt = w_seed['t']; muc = cl.mu*c
    sel = tt > 0.7*tt[-1]
    Z = np.mean(probe_free[sel]*np.exp(-1j*muc*tt[sel]))
    amp_ref = np.max(np.abs(probe_free[sel])) + 1e-300
    theta_late = np.angle(Z) if np.abs(Z) > 1e-3*amp_ref else np.nan
    # also the total-field late phase (descriptive)
    th = w_seed['theta']; late = th[int(0.9*len(th)):]
    theta_tot = np.nanmean(late[np.isfinite(late)]) if np.any(np.isfinite(late)) else np.nan
    # eta(R500): boost of AeST g over MOND g at R500 from the final static field
    rs_final = r_hist[-1]; cl.M_i_per = np.diff(np.concatenate([[0.0], cl.M_i]))
    Menc = cl.Menc_func(rs_final); rho_b = cl.rho_b_func(rs_final)
    rsf = np.sort(rs_final); rsf=rsf[rsf>0]; r0=max(0.5*rsf[0],0.01*cl.R500); r1=4*rsf[-1]
    gA,_ = g_aest_static(np.array([cl.R500]), rho_b, Menc, cl.mu2, r0, r1, n=2500)
    gM = g_mond_arr(np.array([cl.R500]), Menc)
    eta = float(gA[0]/gM[0]-1.0)
    if verbose:
        print(f"    M={Mtot_Msun:.0e} ic={ic_phase:.2f} -> theta_free={theta_late:+.3f} "
              f"theta_tot={theta_tot:+.3f} eta(R500)={eta:+.3f} cross_events={cross_events}")
    return dict(theta_late=theta_late, theta_tot=theta_tot, eta=eta,
                cross_events=cross_events, a_arr=a_arr, r_hist=r_hist, w=w_seed, cl=cl)


if __name__ == "__main__":
    print("="*92)
    print("CAVEAT 1: SELF-CONSISTENT collapse  r''=-g_AeST  (+ radial multi-stream)")
    print("="*92)

    # ---- self-consistency gate: does the collapse actually bounce/virialize? ----
    print("\n[1] Self-consistent collapse sanity (r''=-g_AeST integrated, NOT a proxy):")
    r0 = run_selfconsistent(Mtot_Msun=1e14, R500_Mpc=1.3, ic_phase=0.0, verbose=True)
    rh = r0['r_hist']
    print(f"    median R500-shell: r_init={np.median(rh[0])/Mpc:.3f} Mpc -> "
          f"r_final={np.median(rh[-1])/Mpc:.3f} Mpc (contraction = collapse happened)")
    print(f"    shell-crossing events over history = {r0['cross_events']} "
          f"(>0 -> multi-stream / caveat-3A spread present)")

    # ---- THE PIN TEST: sweep IC phase, measure d(theta_late)/d(ic_phase) ----
    print("\n[2] PIN TEST -- sweep IC phase, self-consistent collapse (caveat 1 + 3A):")
    ic_phases = np.linspace(0, 2*np.pi, 7, endpoint=False)
    th_late=[]; etas=[]
    for p in ic_phases:
        res = run_selfconsistent(Mtot_Msun=1e14, R500_Mpc=1.3, ic_phase=p, verbose=False)
        th_late.append(res['theta_late']); etas.append(res['eta'])
        print(f"    ic_phase={p:.3f} -> theta_late={res['theta_late']:+.3f}  eta={res['eta']:+.3f}")
    from aest_rig_core import pin_metric
    slope, cs_std, resp = pin_metric(ic_phases, th_late)
    print(f"\n  slope d(theta_free)/d(ic) = {slope:+.3f} | circ_std = {cs_std:.3f} rad | "
          f"|IC-response| = {resp:.3f}")
    print(f"  (|IC-response| ~1 -> free-mode phase tracks IC = NO pin; ~0 -> pinned)")
    print(f"  eta(R500) (descriptive, dPhi0=0) = [{np.nanmin(etas):+.3f}, {np.nanmax(etas):+.3f}]")
    verdict = "NO PIN (IC memory retained)" if resp > 0.15 else "POSSIBLE PIN -- check artifact"
    print(f"\n  CAVEAT-1 VERDICT: {verdict}")
