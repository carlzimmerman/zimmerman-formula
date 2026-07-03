#!/usr/bin/env python3
"""
LANE B, TASK 2 -- THE GALACTIC BAND, COMPUTED PROPERLY, AND THE PERSISTENCE BUDGET
FOR A TRANSIENT (COHERENCE/INVERSION) MOND-SIGN CHANNEL.

Band: quasi-circular Omega = v/R over v in [30,300] km/s, R in [0.5,30] kpc.
Persistence spec: delta_m/m ~ O(1) in-band must hold >= 10 orbital periods.
Against it, three model-independent clocks:
  (1) 1/H_Lambda  -- the Hubble/dS clock (canonical footing) and 1/H0 (alt footing):
      a one-shot prepared transient with the most generous decoherence floor
      Gamma_2 ~ H cannot outlive this.
  (2) 1/(3 H0)    -- the kernel-lane environment requirement (R2: Gamma >= 3 H0 on
      orbits, from the committed pump-hunt spec) -- the framework's OWN floor.
  (3) redshift-drift dephasing: any bath mode riding the expansion detunes as
      delta_omega = omega0 * H * t  =>  pi/2 phase slip at t_rs = sqrt(pi/(omega0 H)).
      (Caveat printed: modes rigidly bound to the galaxy evade this one -- but the
      framework's bath is HORIZON-derived, i.e. cosmological.)
Also: the framework-relevant DEEP-MOND subset g_obs = v^2/R < a0, run on BOTH
footings (canonical 9.36e-11 vs alt 1.13e-10), with the spread printed.
Luo (arXiv:2602.14515) short-time-broadening door: after N_orb orbits the
finite-time fraction of the response is ~ 1/(2 pi N_orb) -- printed at 10 orbits.
Exit 0 = all assertions hold.
"""
import numpy as np

c   = 2.99792458e8
kpc = 3.0856775814913673e19
Mpc = 1e3*kpc
yr  = 3.1557e7
Gyr = 1e9*yr

# footings
H0  = 67.4e3/Mpc                    # 2.184e-18 s^-1
OmL = 0.685
HL  = H0*np.sqrt(OmL)               # 1.808e-18 s^-1
Z   = np.sqrt(32*np.pi/3)
a0_can = c*HL/Z                     # canonical: 9.36e-11
a0_alt = c*H0/Z                     # alt footing (rho_total/cH0 family): 1.13e-10
assert abs(a0_can - 9.36e-11) < 0.01e-11
assert abs(a0_alt - 1.13e-10) < 0.01e-10

ok = []

# ---- the band ----
v = np.geomspace(30e3, 300e3, 200)                 # m/s
R = np.geomspace(0.5*kpc, 30*kpc, 200)             # m
V, RR = np.meshgrid(v, R, indexing='ij')
Om = V/RR                                          # rad/s
Om_min, Om_max = Om.min(), Om.max()
T_orb = 2*np.pi/Om
t_need = 10*T_orb                                  # persistence spec
assert 3e-17 < Om_min < 3.5e-17 and 1.8e-14 < Om_max < 2.1e-14
ok.append(f"band: Omega = v/R in [{Om_min:.2e}, {Om_max:.2e}] rad/s "
          f"(= [{Om_min/H0:.0f}, {Om_max/H0:.0f}] H0, 2.8 decades); "
          f"T_orb in [{T_orb.min()/(1e6*yr):.1f} Myr, {T_orb.max()/Gyr:.2f} Gyr]; "
          f"10 T_orb in [{t_need.min()/Gyr:.3f}, {t_need.max()/Gyr:.1f}] Gyr = "
          f"[{t_need.min():.1e}, {t_need.max():.1e}] s")

# ---- clocks ----
tH_can, tH_alt = 1/HL, 1/H0
t_R2 = 1/(3*H0)
for a0, Hf, tH, tag in [(a0_can, HL, tH_can, "CANONICAL a0=9.36e-11 (H_L)"),
                        (a0_alt, H0, tH_alt, "ALT a0=1.13e-10 (H0)")]:
    g_obs = V**2/RR
    deep = g_obs < a0                              # the region MOND is FOR
    frac_deep = deep.mean()
    # one-shot transient at the decoherence FLOOR Gamma_2 = H: fails where 10T > 1/H
    fail_floor = (t_need > tH)
    f_all  = fail_floor.mean()
    f_deep = (fail_floor & deep).sum()/max(deep.sum(), 1)
    # at the framework's own R2 floor Gamma = 3 H0:
    fail_R2 = (t_need > t_R2)
    f_deep_R2 = (fail_R2 & deep).sum()/max(deep.sum(), 1)
    # redshift-drift dephasing for an in-band bath mode omega0 = Omega (resonant route)
    t_rs = np.sqrt(np.pi/(Om*Hf))
    fail_rs = (t_need > t_rs)
    f_deep_rs = (fail_rs & deep).sum()/max(deep.sum(), 1)
    ok.append(f"[{tag}] deep-MOND (g_obs<a0) = {frac_deep*100:.0f}% of band; "
              f"10T > 1/H for {f_all*100:.0f}% of band, {f_deep*100:.0f}% of the DEEP-MOND part; "
              f"10T > 1/(3H0) for {f_deep_R2*100:.0f}% of deep-MOND; "
              f"redshift-drift dephasing kills {f_deep_rs*100:.0f}% of deep-MOND "
              f"(t_rs at band-mid = {np.sqrt(np.pi/(np.sqrt(Om_min*Om_max)*Hf)):.1e} s)")
    if tag.startswith("CANON"):
        f_deep_can, f_R2_can, f_rs_can = f_deep, f_deep_R2, f_deep_rs
    else:
        f_deep_alt, f_R2_alt, f_rs_alt = f_deep, f_deep_R2, f_deep_rs

# the deep-MOND boundary orbit is the WORST case and it is where MOND lives:
# at g_obs = a0: Omega = a0/v -> 10T = 20 pi v/a0
for a0, tH, tag in [(a0_can, tH_can, "canonical"), (a0_alt, tH_alt, "alt")]:
    t10_fast = 20*np.pi*30e3/a0                    # v=30 km/s at the boundary
    t10_slow = 20*np.pi*300e3/a0                   # v=300 km/s at the boundary
    ok.append(f"  at the MOND boundary (g_obs=a0, {tag}): 10T = 20 pi v/a0 = "
              f"[{t10_fast:.1e}, {t10_slow:.1e}] s vs 1/H = {tH:.1e} s -> "
              f"ratio [{t10_fast/tH:.2f}, {t10_slow/tH:.2f}]; DEEPER MOND (g<a0) only gets longer")

# spec sanity: some of deep-MOND fails even at the H-floor, and ALL of it fails at 3H0? print truth
assert f_deep_can > 0.10 and f_deep_alt > 0.10     # a nontrivial chunk outlives 1/H
assert f_R2_can > f_deep_can and f_R2_alt > f_deep_alt

# Luo short-time door at the persistence spec
N_orb = 10
frac_luo = 1/(2*np.pi*N_orb)
ok.append(f"Luo-type short-time (finite-T Unruh broadening) correction after {N_orb} orbits: "
          f"~1/(2 pi N_orb) = {frac_luo*100:.1f}% -- a settled quasi-circular orbit is in the "
          "LONG-TIME regime; per-orbit transients cannot carry an O(1) persistent delta_m. "
          "(It CAN matter for genuinely unsettled populations -- mergers, first infall -- "
          "which is a different observable class, not the RAR.)")

ok.append("CONCLUSION (task 2): a ONE-SHOT transient, even at the most generous decoherence "
          "floor Gamma_2 = H (nothing outlives the horizon clock), covers at most the inner/fast "
          "part of the band; the DEEP-MOND region -- the only region the mechanism is FOR -- "
          "needs 10T up to ~3.5/H: 15-19% of it outlives ANY one-shot transient even at the "
          "Gamma_2=H floor, ~60% at the framework's own R2 floor (3H0), and 100% under "
          "redshift-drift dephasing of a horizon-tied in-band mode. Persistence therefore "
          "REQUIRES continuous regeneration -> the power budget (laneB_regen_budget).")

print("ALL ASSERTIONS PASSED (laneB band persistence)")
for line in ok: print(" *", line)
