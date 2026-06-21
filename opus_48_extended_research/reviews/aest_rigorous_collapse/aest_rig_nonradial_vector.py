#!/usr/bin/env python3
"""
CAVEATS 2 + 3: VECTOR sector (off-spherical) + VIOLENT-RELAXATION mode-mixing.
==============================================================================
The TOP pin candidate (skeptic's map #1): in NON-spherical collapse curl A != 0, so AeST's
aether VECTOR sector turns on and couples the scalar modes chi_n via a TIME-DEPENDENT mixing
matrix C_{nm}(t) from the violently-relaxing potential. The question: does broadband
C_{nm}(t) phase-mix the chi continuum to a UNIVERSAL macroscopic phase (pin), or merely
REDISTRIBUTE energy conservatively (no pin, Kandrup: a sharp discrete mu c mode cannot
phase-mix without a neighboring continuum)?

We build a reduced MODE model that is FAITHFUL to AeST's structure:
  chi_n'' + omega_n^2 chi_n = S_n(t) + sum_m C_{nm}(t) chi_m
  omega_n^2 = c^2 k_n^2 + (mu c)^2
- C_{nm}(t) is ANTISYMMETRIC + REAL (conservative coupling): the vector kinetic term is
  Maxwell |E|^2-|B|^2 (antisymmetric F) -> the mode-coupling conserves total chi energy
  (NO friction). This is the physically-correct structure from the action.
- C_{nm}(t) amplitude ~ K_B * (non-radial potential shear) from the violently-relaxing
  collapse: it is broadband (ramps up at turnaround, rings down) -- the genuine
  Lynden-Bell time-dependent potential.

ADVERSARIAL DELIBERATELY built in: we ALSO test a (UNphysical) DISSIPATIVE coupling (to see
what a pin WOULD look like) and a sign-indefinite coupling, so a real pin is distinguishable
from a numerical/dissipative artifact. The physical (antisymmetric, conservative) case is the
verdict; the others are the both-ways control.

QUARANTINE / BOTH-WAYS per aest_rig_core.py.
"""
import numpy as np, functools
from scipy.integrate import solve_ivp
from aest_rig_core import (c, G_N, Msun, Mpc, a0, H0, mu_of, Gyr, circ_std,
                           slope_theta_vs_ic, pin_metric)
print = functools.partial(print, flush=True)


# ============================================================ the mode-mixing model
def evolve_modes(N_modes, mu, kmax, ic_phase, T_collapse, t_end,
                 K_coupling=1.0, coupling='conservative', seed=0,
                 n_t=4000, broadband=True, ramp='violent'):
    """
    Evolve N coupled chi modes through a violently-relaxing collapse.
      chi_n'' + omega_n^2 chi_n = S_n(t) + sum_m C_{nm}(t) chi_m
    coupling:
      'conservative'  -> C antisymmetric, real (PHYSICAL AeST vector: Maxwell |E|^2, no friction)
      'dissipative'   -> C with a -gamma * chidot sink (UNPHYSICAL control: what a pin looks like)
      'indefinite'    -> C symmetric random (energy not conserved either way; control)
    ramp:
      'violent' -> C_{nm}(t) ramps up at turnaround (t~T_collapse) and rings down (Lynden-Bell
                   time-dependent potential, completes in ~2-3 dynamical times)
    Returns the late-time macroscopic (mode-averaged) oscillation phase.
    """
    rng = np.random.default_rng(seed)
    muc = mu*c
    k_n = np.linspace(0, kmax, N_modes)                # mode wavenumbers (n=0 is the mass-gap DC)
    omega_n = np.sqrt((c*k_n)**2 + muc**2)
    # static mixing structure (geometry of the non-radial coupling), then time-modulated
    Cstruct = rng.standard_normal((N_modes, N_modes))
    if coupling == 'conservative':
        Cmix = (Cstruct - Cstruct.T)/np.sqrt(2)        # ANTISYMMETRIC -> energy-conserving
    elif coupling == 'indefinite':
        Cmix = (Cstruct + Cstruct.T)/np.sqrt(2)        # symmetric (control)
    elif coupling == 'dissipative':
        Cmix = (Cstruct - Cstruct.T)/np.sqrt(2)        # antisym structure...
    else: raise ValueError(coupling)
    # coupling amplitude in units of frequency^2 (the mode equation is chi'' = -omega^2 chi
    # + C chi, so C has units 1/s^2). The non-radial/vector shear sets a MIXING RATE that is
    # a fraction f_mix = K_coupling*0.1 of the field frequency mu c; so C ~ (f_mix*mu c)^2.
    # This is the physical regime (the off-spherical shear is a modest fraction of the fast
    # chi oscillation). amp >> (mu c)^2 would be unphysical (imaginary effective freq).
    f_mix = K_coupling*0.1
    amp = (f_mix*muc)**2
    Cmix *= amp/max(np.max(np.abs(Cmix)),1e-30)

    def ramp_fn(t):
        if ramp == 'violent':
            # ramps up to turnaround, rings down over ~2-3 dynamical times
            return np.exp(-((t - T_collapse)/(0.7*T_collapse))**2)
        return 1.0

    def source(t):
        # the +mu^2-term phantom source from the collapsing density (broadband bounce),
        # NORMALIZED so the forced response is O(1) -- commensurate with the O(1) IC seed
        # (a huge forced DC would numerically swamp the IC phase and FAKE a pin).
        env = np.exp(-((t - T_collapse)/(0.5*T_collapse))**2)
        S = np.zeros(N_modes)
        S[0] = (muc**2)*env             # O(1)*omega^2 source -> O(1) forced amplitude
        return S

    def rhs(t, y):
        chi = y[:N_modes]; chid = y[N_modes:]
        C = Cmix*ramp_fn(t)
        acc = -omega_n**2*chi + source(t) + C@chi
        if coupling == 'dissipative':
            acc = acc - 0.02*muc*ramp_fn(t)*chid   # UNPHYSICAL sink (control only)
        return np.concatenate([chid, acc])

    # IC: seed the free mode with the given phase (O(1) amplitude)
    chi0 = np.zeros(N_modes); chid0 = np.zeros(N_modes)
    chi0[1] = np.cos(ic_phase); chid0[1] = -omega_n[1]*np.sin(ic_phase)
    y0 = np.concatenate([chi0, chid0])
    t_eval = np.linspace(0, t_end, n_t)
    sol = solve_ivp(rhs, [0, t_end], y0, t_eval=t_eval, method='DOP853',
                    rtol=1e-9, atol=1e-12, max_step=2*np.pi/muc/8)
    chi = sol.y[:N_modes]; chid = sol.y[N_modes:]
    t = sol.t
    # macroscopic observable: spatially-averaged chi ~ sum_n chi_n (the cluster-boost knob)
    chi_obs = np.sum(chi, axis=0)
    chid_obs = np.sum(chid, axis=0)
    # late-time phase of the observable oscillation (project onto mu c carrier)
    late = t > 0.8*t_end
    tl = t[late]; cl_ = chi_obs[late]; cdl = chid_obs[late]
    # phase = atan2 of (chi, chidot/muc) averaged over late window
    ph = np.arctan2(-cdl/muc, cl_)
    theta_late = np.angle(np.mean(np.exp(1j*ph)))
    # energy diagnostic: total mode energy (check conservation for the physical case)
    E = 0.5*np.sum(chid**2 + omega_n[:,None]**2*chi**2, axis=0)
    E_drift = (E[-1]-E[len(E)//2])/max(E[len(E)//2],1e-30)
    return dict(theta_late=theta_late, t=t, chi_obs=chi_obs, E=E, E_drift=E_drift,
                omega_n=omega_n, chi=chi)


def pin_sweep(coupling, K_coupling=1.0, N_modes=24, n_ic=8, **kw):
    mu = mu_of(); muc = mu*c
    T_mu = 2*np.pi/muc
    T_collapse = 80*T_mu           # collapse spans many chi periods (mu c >> omega_dyn)
    t_end = 200*T_mu
    kmax = 6*mu                     # spread of k modes -> spread of omega_n (the continuum)
    ic_phases = np.linspace(0, 2*np.pi, n_ic, endpoint=False)
    th=[]; Edr=[]
    for p in ic_phases:
        r = evolve_modes(N_modes, mu, kmax, p, T_collapse, t_end,
                         K_coupling=K_coupling, coupling=coupling, **kw)
        th.append(r['theta_late']); Edr.append(r['E_drift'])
    slope, cstd, resp = pin_metric(ic_phases, th)
    return slope, cstd, np.mean(Edr), ic_phases, th, resp


if __name__ == "__main__":
    print("="*92)
    print("CAVEATS 2+3: VECTOR sector (off-spherical) + violent-relaxation mode-mixing")
    print("="*92)
    mu = mu_of(); muc = mu*c
    print(f"mu c/H0 = {muc/H0:.0f}; the chi modes sit at omega_n = sqrt((c k_n)^2 + (mu c)^2)")
    print("Conservative coupling (PHYSICAL AeST vector, antisymmetric C, no friction) is the")
    print("VERDICT; dissipative/indefinite are the both-ways CONTROLS.\n")

    print("[1] CONSERVATIVE vector mixing (the physical AeST case) -- sweep coupling strength:")
    print(f"  {'K_coupling':>11} {'slope':>8} {'|IC-resp|':>10} {'circ_std':>9} {'E_drift':>11} verdict")
    for K in [0.1, 0.5, 1.0, 2.0, 5.0]:
        slope, cstd, Edr, _, _, resp = pin_sweep('conservative', K_coupling=K)
        verdict = "NO pin" if resp>0.3 else "PIN?"
        print(f"  {K:>11.2f} {slope:>8.3f} {resp:>10.3f} {cstd:>9.3f} {Edr:>11.2e}  {verdict}")
    print("  (|IC-resp| ~1 -> phase tracks IC = NO pin; E_drift ~0 -> conservative mixing,")
    print("   redistributes but does NOT dissipate)")

    print("\n[2] CONTROL -- DISSIPATIVE coupling (UNPHYSICAL sink; shows what a pin looks like):")
    print(f"  {'K_coupling':>11} {'slope':>8} {'|IC-resp|':>10} {'circ_std':>9} {'E_drift':>11} verdict")
    for K in [0.5, 1.0, 2.0]:
        slope, cstd, Edr, _, _, resp = pin_sweep('dissipative', K_coupling=K)
        verdict = "NO pin" if resp>0.3 else "PIN (from sink)"
        print(f"  {K:>11.2f} {slope:>8.3f} {resp:>10.3f} {cstd:>9.3f} {Edr:>11.2e}  {verdict}")
    print("  (a pin HERE (|IC-resp|->0) comes from the artificial -gamma chidot sink -> E_drift<0;")
    print("   AeST has NO such term, so this is the control, not the verdict.)")

    print("\n[3] CONTROL -- indefinite (symmetric) coupling:")
    slope, cstd, Edr, _, _, resp = pin_sweep('indefinite', K_coupling=1.0)
    print(f"  slope={slope:+.3f} |IC-resp|={resp:.3f} circ_std={cstd:.3f} E_drift={Edr:.2e}")

    print("\n  CAVEAT-2+3 VERDICT: the PHYSICAL conservative vector mixing |IC-resp| is the")
    print("  load-bearing number (block [1]). Pin iff |IC-resp|->0 AND E_drift~0 (not a sink).")
