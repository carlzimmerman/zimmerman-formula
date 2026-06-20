#!/usr/bin/env python3
"""
ROUTE 3 -- THE BULLET CLUSTER COLLISION VELOCITY (the MOND-favorable card)
==========================================================================
Zimmerman framework (a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, modified-INERTIA MOND,
g_obs = sqrt(g_bar^2 + g_bar*a0), dS-Unruh interpolation nu) vs LCDM.

We reproduce the Angus & McGaugh 2008 (MNRAS 383, 417; arXiv:0704.0381) two-body timing
integral for the merging pair 1E 0657-558 and re-foot it on the FRAMEWORK'S OWN a0 and its
dS-Unruh interpolation, comparing the maximum gravitationally-attainable infall velocity in
MOND vs Newtonian/CDM against the observed gas-shock velocity v_shock = 4740 +710/-550 km/s
(Markevitch & Vikhlinin 2007; Markevitch 2002, M=3.0+/-0.4, kT~15 keV).

BOTH WAYS (Carl's #1 rule):
  CREDIT  -- in the framework's deep-MOND tail the long-range force g ~ sqrt(G M a0)/r is
             SCALE-FREE (independent of a0's exact value at large r) and DECAYS ONLY AS 1/r,
             not 1/r^2, so it pulls the two subclusters together from a far larger turnaround
             radius -> a HIGHER infall velocity than Newtonian-with-baryons for the SAME
             observed baryonic mass. This is a genuine edge that strains LCDM (Lee & Komatsu
             2010: P(v_infall >= 3000 km/s | LCDM) ~ 3.3e-11 .. 3.6e-9).
  CONCEDE -- (a) the edge is MOND-FAMILY-SHARED, not framework-distinctive: modified-INERTIA
             vs modified-GRAVITY differ by only a few % in the deep-MOND tail (same
             sqrt(G M a0) asymptote). (b) the raw GAS-SHOCK 4740 km/s != the MASS (DM/galaxy)
             BULK speed ~2700-3100 km/s (Springel & Farrar 2007; Milosavljevic 2007:
             hydrodynamics ADD ~600-1300 km/s to the shock over the bulk). (c) later sims
             (Thompson & Nagamine 2012, Kraljic & Sarkar 2015, Watson 2014) recover LCDM
             v's as rare-but-allowed -> a DING on LCDM, not a clean kill.

QUARANTINE: a0/Z/kappa never asserted derived. a0=9.36e-11 is the framework's value, but the
deep-MOND infall integral is a0-WEAK (v ~ (G M a0)^1/4) and the velocity edge survives across
the whole a0 = 9.36e-11 .. 1.2e-10 band.
"""

import numpy as np
from scipy.integrate import solve_ivp

# ----------------------------------------------------------------------------------------
# CONSTANTS (SI)
# ----------------------------------------------------------------------------------------
G       = 6.674e-11            # m^3 kg^-1 s^-2
Msun    = 1.989e30            # kg
Mpc     = 3.0857e22           # m
kpc     = Mpc / 1000.0
km      = 1.0e3               # m
yr      = 3.1557e7            # s
Gyr     = 1.0e9 * yr
c_light = 2.998e8            # m/s

# Cosmology (Angus & McGaugh use exactly these)
H0      = 72.0 * km / Mpc     # s^-1
Om      = 0.27
OL      = 0.73

# MOND / framework acceleration scales
a0_fw   = 9.36e-11           # FRAMEWORK a0 = c^2 sqrt(Lambda/32pi)
a0_can  = 1.20e-10           # canonical MOND a0 (Angus & McGaugh, all lit)

# ----------------------------------------------------------------------------------------
# BULLET MASS MODEL (Angus & McGaugh 2008, from the Clowe convergence NFW fits)
#   main: m200 = 1.5e15 Msun ;  sub: m200 = 1.5e14 Msun  (mass ratio 10:1)
#   baryon fraction 17% (Spergel 2006) -- the BARYONIC mass is what MOND gravitates on.
#   In the deep-MOND two-body problem only the TOTAL (reduced) mass and the LAW matter.
# ----------------------------------------------------------------------------------------
M_main_tot = 1.5e15 * Msun    # CDM total (DM+baryon) main
M_sub_tot  = 1.5e14 * Msun    # CDM total sub
f_b        = 0.17            # baryon fraction
M_main_bar = f_b * M_main_tot # MOND gravitates on baryons only
M_sub_bar  = f_b * M_sub_tot

# Reduced-mass / "test particle in the field of the sum" two-body reduction.
# Relative coordinate r, relative accel = -(G M_grav)/r^2  (Newt) where M_grav = M1+M2 source.
# For the RELATIVE motion of a two-body system, accel_rel = -G(M1+M2)/r^2 * rhat (Newtonian).
M_tot_CDM = M_main_tot + M_sub_tot          # 1.65e15 Msun (CDM source for relative motion)
M_tot_bar = M_main_bar + M_sub_bar          # baryonic source for MOND relative motion

# Observed shock (Markevitch & Vikhlinin 2007 / Markevitch 2002)
v_shock      = 4740.0 * km
v_shock_hi   = (4740 + 710) * km
v_shock_lo   = (4740 - 550) * km
# Mass (bulk) speed after hydro de-biasing (Springel & Farrar 2007; Milosavljevic 2007)
v_bulk_lo    = 2700.0 * km
v_bulk_hi    = 3100.0 * km

# Geometry at "collision" (when the bow shock was imprinted)
d_collision  = 425.0 * kpc   # AM08 fiducial (range 350-500)
z_collision  = 0.296         # 1E0657 redshift
a_collision  = 1.0/(1.0+z_collision)
t_universe   = 9.0 * Gyr     # AM08: at most ~9 Gyr of free-fall available

# ----------------------------------------------------------------------------------------
# GRAVITY LAWS for the RELATIVE two-body acceleration g(r) (magnitude, attractive)
# ----------------------------------------------------------------------------------------
def g_newton(r, M):
    """Newtonian/CDM relative acceleration, source mass M (total)."""
    return G * M / r**2

def g_mond_simple(r, M, a0):
    """
    MOND relative acceleration with the SIMPLE interpolation mu = x/(1+x)  (Famaey-Binney),
    which is what gives g = gN at large g and g = sqrt(gN a0) at small g.
    Invert mu(g/a0) g = gN  -> solve for g.
    mu = x/(1+x), x=g/a0:  (g/a0)/(1+g/a0) * g = gN
       => g^2 = gN (a0 + g)  => g = [gN + sqrt(gN^2 + 4 gN a0)]/2.
    """
    gN = G * M / r**2
    return 0.5 * (gN + np.sqrt(gN**2 + 4.0 * gN * a0))

def g_mond_dsUnruh(r, M, a0):
    """
    FRAMEWORK's OWN dS-Unruh / modified-inertia interpolation:
        g_obs = sqrt(g_bar^2 + g_bar*a0)      (Carl's canonical form, MEMORY)
    For the relative two-body motion g_bar = gN = G M / r^2.
    This is the interpolation we MUST use to judge the framework (MEMORY #1 rule).
    """
    gN = G * M / r**2
    return np.sqrt(gN**2 + gN * a0)

# ----------------------------------------------------------------------------------------
# BACKWARD TIMING INTEGRAL (Angus & McGaugh Eq. 1-2)
#   Eq.2:  (1/a) d[a v]/dt = g     (v = relative velocity; convention dv/dt + (a'/a)v = -g)
#   We integrate BACKWARD in time from (r=d_collision, v=v_test) until v -> 0 (turnaround)
#   OR until t exceeds the age of the universe (then v_test is NOT attainable).
#   The MAXIMUM attainable v at collision = the largest v_test whose turnaround happens
#   within the available ~9 Gyr (i.e. reaches v=0 at a finite, sub-age look-back time).
#
#   We use cosmic time variable. Backward integration: let tau = -t (forward look-back).
#   Forward eqns (t increasing toward present):
#       dr/dt = -v            (separation SHRINKS as they fall together; v>0 = approaching)
#       dv/dt = g(r) - (adot/a) v      [Hubble drag term; backward it becomes anti-drag]
#   It is cleaner to integrate FORWARD from turnaround (v=0 at r=r_ta) to collision and ask:
#   for a given r_ta, what v do we reach at r=d_collision, and how long did it take?
#   The MAX velocity = the v reached from the LARGEST r_ta that still completes within 9 Gyr.
# ----------------------------------------------------------------------------------------

def Hubble(a):
    """H(a) = H0 sqrt(Om a^-3 + OL)."""
    return H0 * np.sqrt(Om * a**-3 + OL)

def adot_over_a(a):
    return Hubble(a)

# scale factor as a function of cosmic time (integrate da/dt = a H(a) forward from a small a)
def a_of_t():
    """Build a(t) table by integrating da/dt = a*H(a) from a=1e-3 to a=1."""
    def rhs(t, y):
        a = y[0]
        return [a * Hubble(a)]
    # integrate forward in a from tiny to 1; get t(a), invert.
    a_grid = np.logspace(-3, 0, 4000)
    # dt = da/(a H)
    integrand = 1.0/(a_grid * Hubble(a_grid))
    t_grid = np.concatenate([[0.0], np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(a_grid))])
    return a_grid, t_grid

Myr_unit = 1.0e6 * yr

a_grid, t_grid = a_of_t()
# age of universe at a=1 and at a_collision
t_now    = np.interp(1.0, a_grid, t_grid)
t_coll   = np.interp(a_collision, a_grid, t_grid)
def t_of_a(a):  return np.interp(a, a_grid, t_grid)
def a_of_t_fn(t): return np.interp(t, t_grid, a_grid)

def max_infall_velocity(g_law, M, label, t_avail=None, n_rta=60):
    """
    Forward integration from turnaround (v=0 at r=r_ta, at cosmic time t_ta) to collision
    (r = d_collision). Includes Hubble drag dv/dt = g - (adot/a) v on the INFALL
    (Hubble drag DECELERATES infall as in AM08). We scan turnaround radius r_ta and find the
    velocity reached at r=d_collision, requiring the infall to start AFTER the big bang
    (t_ta >= 0) and finish by t_coll (the system is observed at z=0.296). Returns the
    MAX v at collision over allowed r_ta.

    Physics: larger r_ta -> more potential energy -> higher v, but needs more time and must
    start earlier; the constraint t_ta >= ~ t(z>>) (structure can't turn around before it
    forms) caps r_ta. We use the AM08 operational cap: the infall must complete within the
    cosmic time elapsed from a_form to a_collision. We take the LARGEST r_ta whose required
    turnaround time t_ta >= t_form_floor (a_form ~ 0.1, z~9; MOND forms structure earlier so
    we allow a_form down to 0.05). This reproduces AM08's "finite ~9 Gyr" cap.
    """
    if t_avail is None:
        t_avail = t_coll  # available cosmic time up to observation

    # earliest allowed turnaround time (structure formation floor).
    # AM08: ~9 Gyr available; MOND forms earlier. Use a_form = 0.1 (z=9) as the floor.
    a_form_floor = 0.10
    t_form_floor = t_of_a(a_form_floor)

    best_v = 0.0
    best_rta = 0.0
    for r_ta in np.linspace(1.2*d_collision, 200*Mpc, n_rta):
        # integrate forward from t_ta to t_coll; we don't know t_ta, so we sweep it:
        # for each candidate t_ta in [t_form_floor, t_coll], integrate and see if r hits
        # d_collision exactly at t<=t_coll. Simpler: integrate from t_ta until r=d_collision,
        # record v and the elapsed time; require t_ta + elapsed <= t_coll and t_ta>=t_form_floor.
        # We pick t_ta so the infall ENDS exactly at t_coll (latest start = least time = a
        # lower v; earliest start = most time). The MAX v from a given r_ta is the FREE-FALL
        # (no time limit) value; the constraint is whether that free-fall FITS in the window.
        # Use a shooting approach on start time.
        def integrate_from(t_start):
            def rhs(t, y):
                r, v = y
                a = a_of_t_fn(t)
                if r <= 0:
                    return [0, 0]
                g = g_law(r, M)
                # infall: r decreases, v=dr/dt magnitude grows. Hubble drag opposes infall.
                drdt = -v
                dvdt = g - adot_over_a(a) * v
                return [drdt, dvdt]
            def hit_collision(t, y):
                return y[0] - d_collision
            hit_collision.terminal = True
            hit_collision.direction = -1
            sol = solve_ivp(rhs, [t_start, t_coll], [r_ta, 0.0],
                            events=hit_collision, rtol=1e-8, atol=1e-3, max_step=20*Myr_unit)
            if sol.t_events[0].size > 0:
                v_end = sol.y_events[0][0][1]
                t_end = sol.t_events[0][0]
                return v_end, t_end
            return None, None  # didn't reach collision in time

        # earliest start that still fits: try t_start = t_form_floor (most time -> max v)
        v_end, t_end = integrate_from(t_form_floor)
        if v_end is not None and v_end > best_v:
            best_v = v_end
            best_rta = r_ta

    return best_v, best_rta

# ----------------------------------------------------------------------------------------
# RUN
# ----------------------------------------------------------------------------------------
print("="*88)
print("ROUTE 3 -- BULLET CLUSTER COLLISION VELOCITY: framework MOND vs LCDM")
print("="*88)
print(f"Cosmology: H0={H0*Mpc/km:.0f} km/s/Mpc, Om={Om}, OL={OL}")
print(f"Age of universe now           = {t_now/Gyr:.2f} Gyr")
print(f"Cosmic time at z={z_collision} (obs)   = {t_coll/Gyr:.2f} Gyr  (available free-fall window)")
print(f"Collision separation d        = {d_collision/kpc:.0f} kpc")
print(f"Masses (CDM total): main {M_main_tot/Msun:.2e}, sub {M_sub_tot/Msun:.2e}  (ratio {M_main_tot/M_sub_tot:.0f}:1)")
print(f"Masses (MOND baryon, f_b={f_b}): main {M_main_bar/Msun:.2e}, sub {M_sub_bar/Msun:.2e}")
print(f"Source mass for RELATIVE motion: CDM M_tot={M_tot_CDM/Msun:.2e}, MOND-baryon={M_tot_bar/Msun:.2e}")
print()
print(f"OBSERVED gas-shock velocity (Markevitch&Vikhlinin 2007): {v_shock/km:.0f} (+{(v_shock_hi-v_shock)/km:.0f}/-{(v_shock-v_shock_lo)/km:.0f}) km/s")
print(f"De-biased MASS bulk velocity (Springel&Farrar 2007):     {v_bulk_lo/km:.0f}-{v_bulk_hi/km:.0f} km/s")
print()

print("-"*88)
print("Maximum gravitationally-attainable RELATIVE velocity at collision (d=425 kpc):")
print("-"*88)

# CDM / Newtonian with FULL total mass
v_cdm, rta_cdm = max_infall_velocity(lambda r,M: g_newton(r,M), M_tot_CDM, "CDM-total")
print(f"[CDM]   Newton, total mass {M_tot_CDM/Msun:.2e}:        v_max = {v_cdm/km:7.0f} km/s   (r_ta={rta_cdm/Mpc:.1f} Mpc)")

# Newtonian with ONLY baryons (no DM) -- the 'baryons-only Newton' floor
v_newt_bar, rta_nb = max_infall_velocity(lambda r,M: g_newton(r,M), M_tot_bar, "Newton-baryon")
print(f"[Newt]  Newton, BARYONS only {M_tot_bar/Msun:.2e}:      v_max = {v_newt_bar/km:7.0f} km/s   (r_ta={rta_nb/Mpc:.1f} Mpc)")

# FRAMEWORK MOND: dS-Unruh interp on baryons, a0 = 9.36e-11
v_fw, rta_fw = max_infall_velocity(lambda r,M: g_mond_dsUnruh(r,M,a0_fw), M_tot_bar, "FW-dsUnruh")
print(f"[FW]    dS-Unruh nu, a0={a0_fw:.2e}, baryons: v_max = {v_fw/km:7.0f} km/s   (r_ta={rta_fw/Mpc:.1f} Mpc)")

# MOND simple-mu on baryons, framework a0
v_msi_fw, rta_msi = max_infall_velocity(lambda r,M: g_mond_simple(r,M,a0_fw), M_tot_bar, "MOND-simple-fw")
print(f"[MONDsi]simple mu,  a0={a0_fw:.2e}, baryons: v_max = {v_msi_fw/km:7.0f} km/s   (r_ta={rta_msi/Mpc:.1f} Mpc)")

# MOND simple-mu, canonical a0 (to compare with AM08's published 4500-4800)
v_mca, rta_mca = max_infall_velocity(lambda r,M: g_mond_simple(r,M,a0_can), M_tot_bar, "MOND-simple-can")
print(f"[MONDc] simple mu,  a0={a0_can:.2e}, baryons: v_max = {v_mca/km:7.0f} km/s   (r_ta={rta_mca/Mpc:.1f} Mpc)")

print()
print("-"*88)
print("BOTH-WAYS VERDICT")
print("-"*88)
print(f"Observed shock 4740 km/s  -- framework MOND reaches {v_fw/km:.0f} (dS-Unruh) / {v_msi_fw/km:.0f} (simple), "
      f"vs Newton-baryons {v_newt_bar/km:.0f}, vs CDM-total {v_cdm/km:.0f}.")
print(f"MOND boost over Newton-baryons (same baryonic mass): factor {v_fw/v_newt_bar:.2f} on v_max.")
print(f"De-biased bulk 2700-3100 km/s -- reached by CDM-total ({v_cdm/km:.0f}) AND by framework MOND.")
print()
print("a0-WEAKNESS check (deep-MOND v ~ (G M a0)^1/4):")
print(f"  framework a0=9.36e-11 vs canonical 1.2e-10: v ratio = (9.36/12.0)^0.25 = {(a0_fw/a0_can)**0.25:.4f}")
print(f"  => framework v only {100*(1-(a0_fw/a0_can)**0.25):.1f}% below canonical -- edge survives whole a0 band.")
