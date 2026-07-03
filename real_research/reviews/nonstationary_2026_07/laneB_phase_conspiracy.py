#!/usr/bin/env python3
"""
LANE B, TASK 2b/3b -- CAN THE RESONANT-COHERENCE CHANNEL BE UNIVERSAL?
(The one channel where coherence beats inversion parametrically -- first order in g,
laneB_transient_gain_model case D -- requires FREQUENCY and PHASE matching to each
orbit. Quantify what universality costs.)

 (1) Frequency comb: phase slip < pi/2 over N_orb=10 orbits needs |omega0/Omega - 1|
     < 1/(4 pi N_orb) ~ 1/126; covering the 2.8-decade band needs ~ln(600)/ln(1+1/63)
     ~ 400 channels -- a designed comb, nothing horizon-derived (one scale, cH_L/Z).
 (2) Phase: a coherent bath amplitude in a region is ONE c-number phase; the stars in
     any kpc^3 have RANDOM orbital phases. Monte Carlo: net delta_m averages to zero
     as 1/sqrt(N_star); HALF the stars get the ANTI-MOND sign. There is no state of a
     shared medium that phase-locks to 1e11 independent orbital phases; per-star
     locking information can only be sourced by the star itself, and a self-sourced
     coherence is linear response of the stationary bath = the c-number kernel =
     theorems III/IV apply (state-blind, no in-band softening without a ghost).
 (3) The unmatched remainder is not neutral: a random-phase coherent force of the
     required amplitude f*a0 with coherence time tau_2 random-walks stellar velocities:
     sigma_v^2 = (f a0)^2 tau_2 t. At tau_2 = 1/(3H0) over 10 Gyr this over-heats the
     disk by ~2 orders in sigma (>4 orders in energy) vs the observed ~30 km/s.
     Run BOTH a0 footings.
Exit 0 = all assertions hold.
"""
import numpy as np

rng = np.random.default_rng(20260702)
c   = 2.99792458e8
Mpc = 3.0856775814913673e22
yr  = 3.1557e7
H0  = 67.4e3/Mpc
HL  = H0*np.sqrt(0.685)
Z   = np.sqrt(32*np.pi/3)
a0_can, a0_alt = c*HL/Z, c*H0/Z
ok = []

# (1) comb
N_orb = 10
tol = 1/(4*np.pi*N_orb)                       # |dOmega|/Omega for < pi/2 slip over N_orb orbits
band_ratio = (300/0.5)/(30/30)                # Omega_max/Omega_min = 600
N_ch = np.log(band_ratio)/np.log(1 + 2*tol)   # channels of full width 2*tol
assert 350 < N_ch < 450
ok.append(f"(1) tolerance |omega0/Omega-1| < {tol:.2e} for <pi/2 slip over {N_orb} orbits; "
          f"band ratio 600 -> N_channels ~ {N_ch:.0f}. The framework supplies ONE horizon scale "
          "(cH_L/Z); a ~400-channel tuned comb is pure design, nothing forces it.")

# (2) phase Monte Carlo: apparent delta_m_i = -|dm0| * cos(phi_bath - phi_i)
for N_star in (1e4, 1e7, 1e11):
    N = int(min(N_star, 2e6))                 # sample; scaling is exact 1/sqrt(N)
    phi = rng.uniform(0, 2*np.pi, N)
    dm_i = -np.cos(phi)                       # units of |dm0|
    net = dm_i.mean(); anti = (dm_i > 0).mean()
    exp_net = 1/np.sqrt(N)
    assert abs(net) < 5*exp_net
    assert abs(anti - 0.5) < 0.01
ok.append(f"(2) MC (2e6 draws): net <delta_m> = {net:+.2e} |dm0| ~ 1/sqrt(N) -> at N=1e11 stars "
          "the coherent net effect is ~3e-6 of the per-star amplitude, and 50.0% of stars get "
          "the ANTI-MOND sign. One shared phase cannot serve a galaxy. Per-star phase info can "
          "only come from the star itself => self-induced coherence = stationary linear response "
          "= c-number kernel (theorem III state-blind clause) => no new door there.")

# (3) heating of the unmatched population
f = 0.5                                        # delta_m/m target (mu >= 1/2 EP cap)
t_disk = 10e9*yr
sig_obs = 30e3                                 # m/s, old-disk vertical dispersion
for a0, tag in [(a0_can, "canonical"), (a0_alt, "alt")]:
    for tau2, tlab in [(1/(3*H0), "tau2=1/(3H0)"), (1/HL, "tau2=1/H_L")]:
        sig = f*a0*np.sqrt(tau2*t_disk)
        ratio = sig/sig_obs
        ok.append(f"(3) [{tag}, {tlab}] random-phase coherent force f*a0={f*a0:.2e} m/s^2 -> "
                  f"sigma_v = {sig/1e3:.0f} km/s over 10 Gyr = {ratio:.0f}x observed 30 km/s "
                  f"({ratio**2:.0f}x in energy)")
        assert ratio > 50                      # catastrophic in every fork

ok.append("CONCLUSION: the only parametrically-cheap coherence channel (resonant, first order "
          "in g) is EITHER phase-locked per star -- which no universal bath state can be, and a "
          "self-locked version collapses back into the stationary kernel covered by theorems "
          "III/IV -- OR phase-random, in which case it nets ~1/sqrt(N_star) of the effect while "
          "heating disks by >=2 orders in sigma_v. Universality kills the resonant-coherence "
          "route independently of the power budget. Robust to the a0 footing fork (both shown).")

print("ALL ASSERTIONS PASSED (laneB phase conspiracy)")
for line in ok: print(" *", line)
