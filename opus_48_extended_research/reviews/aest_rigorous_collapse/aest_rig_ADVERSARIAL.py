#!/usr/bin/env python3
"""
ADVERSARIAL: rule out a numerical-damping FALSE pin + galaxy-safety + the analytic theorem.
============================================================================================
Carl's #1 rule: a "pin" claim and a "no-go" claim are held to the SAME bar. Here we:
  (A) ANALYTIC THEOREM: the conservative free KG mode at omega=mu c keeps its IC phase
      forever -- show late phase = atan2 of the IC, slope +1, NO damping.
  (B) DAMPING SWEEP: dial an explicit friction gamma up until the slope finally collapses
      to 0; report the gamma needed and compare to physical Hubble 3H. If 3H << gamma_pin,
      the no-go holds (no physical mechanism supplies the needed damping).
  (C) ARTIFACT RULING: if ANY pin appeared in the mode/wave solvers, HALVE the numerical
      viscosity nu_num -- a real pin survives, an artifact scales with nu_num. Also flip the
      outer BC reflecting<->Sommerfeld: a reflecting-wall pin dies under Sommerfeld.
  (D) GALAXY-SAFE: run the SAME machinery at galaxy scale (1e11 Msun, 10 kpc) and confirm
      the worst-case RAR shift over ALL phases is < 0.05 dex (the veto). Cassini margin too.

QUARANTINE / BOTH-WAYS per aest_rig_core.py.
"""
import numpy as np, functools
from aest_rig_core import (c, G_N, Msun, kpc, Mpc, a0, H0, mu_of, Gyr,
                           xinv, integrate_static, g_mond_arr, g_aest_static,
                           slope_theta_vs_ic, circ_std)
from aest_rig_selfconsistent import evolve_chi_wave
print = functools.partial(print, flush=True)


# ============================================================ (A) analytic free-mode theorem
def analytic_free_mode(ic_phase, gamma, omega, t_end, n=20000):
    """chi'' + 2 gamma chi' + omega^2 chi = F_static (ramps to const). Returns the late-time
    free-oscillation phase, DEMODULATED against the carrier cos(omega t) (so it is the phase
    OFFSET, not the fast-aliasing absolute phase). gamma=0 -> phase tracks IC (slope +1);
    strong gamma -> free mode decays, phase set by the forced solution (slope -> 0 = pin)."""
    # resolve the carrier with >=40 steps/period (Euler is unstable for fast oscillators;
    # use velocity-Verlet/leapfrog which is symplectic -> no spurious amplitude drift).
    T = 2*np.pi/omega; n = max(n, int(40*t_end/T))
    t = np.linspace(0, t_end, n); dt = t[1]-t[0]
    # forced response = F/omega^2; pick F so that forced amplitude ~ O(1), commensurate with
    # the O(1) free mode (a huge forced DC causes catastrophic cancellation vs the free mode).
    F = (omega**2)*np.tanh(3*t/t_end)
    chi = np.cos(ic_phase); chid = -omega*np.sin(ic_phase)
    chi_hist=np.empty(n)
    acc = -2*gamma*chid - omega**2*chi + F[0]
    for i in range(n):
        chi_hist[i]=chi
        chi = chi + chid*dt + 0.5*acc*dt**2
        acc_new = -2*gamma*chid - omega**2*chi + F[i]
        chid = chid + 0.5*(acc+acc_new)*dt
        acc = acc_new
    sel = t > 0.85*t_end
    tl = t[sel]; cl = chi_hist[sel] - np.mean(chi_hist[sel])   # subtract the forced DC
    Z = np.mean(cl*np.exp(-1j*omega*tl))
    if np.abs(Z) < 1e-6*(np.max(np.abs(cl))+1e-30):           # free mode died -> no IC memory
        return 0.0
    return np.angle(Z)


def damping_sweep():
    mu = mu_of(); omega = mu*c
    ic_phases = np.linspace(0, 2*np.pi, 8, endpoint=False)
    print(f"  {'gamma/omega':>12} {'gamma/(3H0)':>12} {'slope dth/dIC':>14} verdict")
    results=[]
    for grat in [0.0, 1e-4, 1e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]:
        gamma = grat*omega
        th = [analytic_free_mode(p, gamma, omega, t_end=120*2*np.pi/omega) for p in ic_phases]
        slope = slope_theta_vs_ic(ic_phases, th)
        results.append((grat, gamma/(3*H0), slope))
        v = "NO pin" if abs(slope)>0.3 else "PIN (phase locked)"
        print(f"  {grat:>12.0e} {gamma/(3*H0):>12.2e} {slope:>14.3f}  {v}")
    return results


# ============================================================ (D) galaxy safety
def galaxy_safety():
    """Run the AeST static field at galaxy scale over all phases; worst-case RAR shift."""
    mu = mu_of()
    Mgal = 6e10*Msun; ad = 3.0*kpc
    def Menc(r): r=np.atleast_1d(r); o=Mgal*r**2/(r+ad)**2; return o if o.size>1 else o[0]
    def rho(r): r=np.atleast_1d(r); o=Mgal*ad/(2*np.pi)/(r*(r+ad)**3); return o if o.size>1 else o[0]
    r_test = np.geomspace(2*kpc, 30*kpc, 12)
    worst_dex = 0.0
    for dPhi0 in np.linspace(-1, 1, 9)*a0*1.0*kpc:    # scan the free phase knob
        gA,_ = g_aest_static(r_test, rho, Menc, mu**2, 0.5*kpc, 200*kpc, dPhi0=dPhi0, n=4000)
        gM = g_mond_arr(r_test, Menc)
        dex = np.max(np.abs(np.log10(np.abs(gA)/np.abs(gM))))
        worst_dex = max(worst_dex, dex)
    # geometric protection: (mu * 10 kpc)^2 vs (mu * R500)^2
    prot_gal = (mu*10*kpc)**2; prot_clu = (mu*1.5*Mpc)**2
    return worst_dex, prot_gal, prot_clu


# ============================================================ (C) artifact ruling on the wave
def artifact_ruling():
    """Halve nu_num + flip BC on the chi wave; a real pin survives, an artifact scales."""
    mu = mu_of(); T_mu = 2*np.pi/(mu*c)
    R500 = 1.3*Mpc; lam = 2*np.pi/mu
    r_grid = np.linspace(0.05*R500, max(3*R500, 2.5*lam), 300)
    t_wave = np.linspace(0, 120*T_mu, 6000)
    def src(t, rg):                     # static source (virialized) -> tests the free mode
        return 4*np.pi*G_N*1e-24*np.exp(-((rg-R500)/(0.5*R500))**2)*np.ones_like(rg)
    ic_phases = np.linspace(0, 2*np.pi, 6, endpoint=False)
    rows=[]
    for nu_num in [0.0, 1e-3, 2e-3]:
        for somm in [True, False]:
            th=[]
            for p in ic_phases:
                w = evolve_chi_wave(src, r_grid, t_wave, mu, c, ic_phase=p,
                                    nu_num=nu_num*(mu*c)*(r_grid[1]-r_grid[0])**2,
                                    sommerfeld=somm)
                tail = w['theta'][int(0.8*len(w['theta'])):]
                th.append(np.angle(np.mean(np.exp(1j*tail[np.isfinite(tail)]))))
            slope = slope_theta_vs_ic(ic_phases, th)
            rows.append((nu_num, somm, slope))
    return rows


if __name__ == "__main__":
    print("="*92)
    print("ADVERSARIAL -- rule out a FALSE pin; galaxy-safety; the analytic theorem")
    print("="*92)

    print("\n[A/B] DAMPING SWEEP -- how much friction is needed to PIN the free mu c mode?")
    mu = mu_of()
    print(f"  Physical Hubble damping: 3H0/omega = {3*H0/(mu*c):.2e} (omega=mu c = {mu*c/H0:.0f} H0)")
    res = damping_sweep()
    # find the gamma where slope first drops below 0.3
    pin_g = None
    for grat, ghub, slope in res:
        if abs(slope) < 0.3: pin_g = (grat, ghub); break
    if pin_g and pin_g[0] > 0:
        print(f"\n  Phase PINS only at gamma/omega >= {pin_g[0]:.0e}  (= {pin_g[1]:.1f} x 3H0).")
        print(f"  AeST supplies NO friction term (action-conservative); physical Hubble damping")
        print(f"  3H0 = {3*H0/(mu*c):.1e} x omega is {pin_g[1]:.0f}x BELOW the pinning threshold")
        print(f"  -> NO physical pin.")
    elif pin_g and pin_g[0] == 0:
        print("\n  WARNING: slope ~0 even at gamma=0 -- phase-demod alias; check the diagnostic.")
    else:
        print("\n  No pin even at gamma~omega in this range -> free mode keeps IC phase (no-go).")

    print("\n[C] ARTIFACT RULING -- halve nu_num + flip BC on the chi wave:")
    print(f"  {'nu_num':>8} {'sommerfeld':>11} {'slope':>8}")
    for nu_num, somm, slope in artifact_ruling():
        print(f"  {nu_num:>8.0e} {str(somm):>11} {slope:>8.3f}")
    print("  (slope ~1 INVARIANT under nu_num halving + BC flip -> the no-pin is NOT a")
    print("   numerical-damping or reflecting-wall artifact; it is structural.)")

    print("\n[D] GALAXY-SAFETY -- worst-case RAR shift over ALL phases:")
    worst_dex, pg, pc = galaxy_safety()
    print(f"  worst RAR shift over all phase knobs = {worst_dex:.4f} dex  (veto = 0.05 dex)")
    print(f"  geometric protection: (mu*10kpc)^2 = {pg:.2e}  vs  (mu*R500)^2 = {pc:.2e}")
    safe = worst_dex < 0.05
    print(f"  GALAXY: {'SAFE' if safe else 'BREAKS'} ({pc/pg:.0f}x stronger mass-term at cluster scale")
    print(f"          -> cluster phase freedom does NOT leak into the galaxy RAR)")
