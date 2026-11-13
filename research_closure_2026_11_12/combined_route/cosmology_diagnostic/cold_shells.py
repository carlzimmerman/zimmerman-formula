#!/usr/bin/env python3
"""Independent Newtonian cold-shell reference; NOT the DT2/v3 charge equation.

Units: kpc, Gyr, Msun.  Cold shell mass is exactly the initial homogeneous mass
inside its Lagrangian radius, including the central ball.  Homogeneous baryons
and Lambda are prescribed cosmological sources.  A Plummer central EXCESS is
externally ramped on; the ramp does not conserve the prescribed baryon inventory.
No pressure, polarization, EFE, absorption, or post-caustic continuation.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

KPC = 3.0856775814913673e19
GYR = 1.e9 * 3.1557e7  # same year as corrected DT2 formation driver
MSUN = 1.98892e30
G = 6.6743e-11 * MSUN * GYR**2 / KPC**3
H0 = 70.e3 / (1000 * KPC) * GYR
OC, OB, OL = .26, .05, .69
OM = OC + OB
AI = 1 / 11
A = .5 * OC * H0**2 / AI**3
MB = 10**10.45
SOFT = 1.0
RAMP = 1.0
HI = H0 * np.sqrt(OM / AI**3 + OL)


def age(a):
    return 2 / (3 * H0 * np.sqrt(OL)) * np.arcsinh(np.sqrt(OL / OM) * np.asarray(a)**1.5)


TI = float(age(AI))
TEND = float(age(1) - TI)


def scale(t):
    return (np.sqrt(OM / OL) * np.sinh(1.5 * H0 * np.sqrt(OL) * (TI + np.asarray(t))))**(2 / 3)


def mass(t, central):
    return MB * np.clip(t / RAMP, 0, 1) if central else 0.0


def background(t):
    a = scale(t)
    return -.5 * OB * H0**2 / a**3 + OL * H0**2


def regularized_rhs(tau, y, radii, central):
    """Center-limit u=s^2, dt/dtau=s^2 removes its Kepler collision singularity.

    E=.5*udot^2-A/u is a mechanical auxiliary, not a conserved total energy
    in the time-dependent external force.  E'=2*w*s*F.  Positive-radius shells
    use ordinary u,udot with this shared monotone physical clock.
    """
    s, w, energy, t = y[:4]
    u, v = np.split(y[4:], 2)
    b = background(t)
    gm = G * mass(t, central)
    force_center = (b - gm / SOFT**3) * s**2
    force = -A / u**2 + b * u - gm * u / (radii**2 * u**2 + SOFT**2)**1.5
    return np.concatenate(([w, .5 * energy * s + .5 * force_center * s**3,
                            2 * w * s * force_center, s**2], v * s**2, force * s**2))


def direct_rhs(t, y, radii, central):
    """Independent physical-time implementation for pre-caustic cross-checks."""
    u, v = np.split(y, 2)
    a = scale(t)
    # Written in physical radii/masses, independently of the regularized RHS.
    r = radii * u
    enclosed_cold_mass = OC * (3 * H0**2 / (8 * np.pi * G)) / AI**3 * (4 * np.pi / 3) * radii**3
    density_b = OB * (3 * H0**2 / (8 * np.pi * G)) / a**3
    acc = (-G * enclosed_cold_mass / r**2 - (4 * np.pi * G / 3) * density_b * r
           + OL * H0**2 * r - G * mass(t, central) * r / (r**2 + SOFT**2)**1.5)
    return np.concatenate((v, acc / radii))


def original_stencil_witness(n):
    f = np.geomspace(1., 2000., n + 1)
    rc = .75 * (f[1:]**4 - f[:-1]**4) / (f[1:]**3 - f[:-1]**3)
    dv = f[1:]**3 - f[:-1]**3
    old = np.cumsum(dv) - .5 * dv
    # Common factor 4*pi*rho/3 cancels in these mass ratios.
    exact = rc**3
    half_with_inner_ball = old + f[0]**3
    return dict(n=n, inner_hubble_velocity_relative_error=float(rc[0] / f[0] - 1),
                first_enclosed_mass_old_over_exact=float(old[0] / exact[0]),
                half_cell_only_relative_error=float(half_with_inner_ball[0] / exact[0] - 1),
                max_half_cell_only_relative_error=float(np.max(np.abs(half_with_inner_ball / exact - 1))),
                missing_inner_ball_mass_Msun=float(A / G))


def run(n, central, rtol, atol, out):
    start = time.perf_counter()
    radii = np.geomspace(1., 2000., n + 1)
    y0 = np.concatenate(([1., HI / 2, .5 * HI**2 - A, 0.],
                         np.ones(len(radii)), np.full(len(radii), HI)))

    def focus(tau, y):
        return y[0]

    def crossing(tau, y):
        rr = radii * y[4:4 + len(radii)]
        return np.min(np.diff(rr) / np.diff(radii))

    def zzero(tau, y):
        return y[3] - TEND

    for event in (focus, crossing, zzero):
        event.terminal = True
    focus.direction = crossing.direction = -1
    zzero.direction = 1
    sol = solve_ivp(lambda tau, y: regularized_rhs(tau, y, radii, central), (0., 100.), y0,
                    method='DOP853', rtol=rtol, atol=atol, events=(focus, crossing, zzero),
                    dense_output=True, max_step=.01 if central else .1)
    if not sol.success or sol.status != 1:
        raise RuntimeError('No physical stopping event: ' + sol.message)
    event_index = next(i for i, tt in enumerate(sol.t_events) if len(tt))
    event_name = ('central_limit_focusing', 'finite_shell_crossing', 'z0')[event_index]
    tau = np.linspace(0, sol.t[-1], 1501)
    sample = sol.sol(tau)
    s, w, ee, tt = sample[:4]
    u, v = np.split(sample[4:], 2)
    aa = scale(tt)
    rr = radii[:, None] * u
    spacing = np.diff(rr, axis=0) / np.diff(radii)[:, None]
    # First ball [0,r1] included.  dm has its exact initial homogeneous value.
    radius0 = np.concatenate(([0.], radii))
    initial_volume = np.diff(radius0**3)
    evolved_volume = np.diff(np.vstack((np.zeros(len(tt)), rr))**3, axis=0)
    q = AI**-3 * initial_volume[:, None] / evolved_volume
    constraint = 2 * w**2 - ee * s**2 - A
    homogeneous = aa / AI
    checks = {'regularized_energy_constraint_abs': float(np.max(np.abs(constraint))),
              'sampled_min_normalized_finite_spacing': float(np.min(spacing)),
              'sampled_min_finite_cell_density_over_present_cold': float(np.min(q)),
              'cold_mass_is_constant_by_lagrangian_definition': True}
    if not central:
        checks.update(homogeneous_u_max_relative_error=float(np.max(np.abs(u / homogeneous - 1))),
                      homogeneous_center_u_max_relative_error=float(np.max(np.abs(s**2 / homogeneous - 1))),
                      homogeneous_velocity_max_relative_error=float(np.max(np.abs(v / (H0 * np.sqrt(OM / aa**3 + OL) * homogeneous) - 1))),
                      all_shell_velocities_outward=bool(np.all(v > 0)),
                      initial_acceleration_is_inward=bool(-A + background(0) < 0))
    # Independent physical-time integration; avoids the singular center marker.
    # Finite shells remain ordered and positive throughout these pre-focus paths.
    direct = solve_ivp(lambda t, y: direct_rhs(t, y, radii, central), (0., tt[-1]), y0[4:],
                       method='DOP853', rtol=rtol / 2, atol=atol / 2, dense_output=True,
                       max_step=.001 if central else .05)
    if not direct.success:
        raise RuntimeError(direct.message)
    direct_sample = direct.sol(tt)
    checks['independent_physical_time_max_u_difference'] = float(np.max(np.abs(direct_sample[:len(radii)] - u)))
    checks['independent_physical_time_max_v_difference'] = float(np.max(np.abs(direct_sample[len(radii):] - v)))
    first_turn = []
    for label, vel in [('center_limit', w), ('first_finite_shell', v[0])]:
        ix = np.flatnonzero(vel <= 0)
        if len(ix):
            from scipy.optimize import brentq
            j = ix[0]
            if j == 0:
                turn_tau = 0.
            else:
                vi = 1 if label == 'center_limit' else 4 + len(radii)
                turn_tau = brentq(lambda x: sol.sol(x)[vi], tau[j - 1], tau[j], xtol=1.e-14)
            ys = sol.sol(turn_tau)
            first_turn.append(dict(marker=label, elapsed_Gyr=float(ys[3]), z=float(1 / scale(ys[3]) - 1),
                                   r_kpc=None if label == 'center_limit' else float(radii[0] * ys[4])))
    result = dict(model='Independent Newtonian pressureless reference; not DT2/v3 charge transport',
                  n=n, central=central, rtol=rtol, atol=atol, constants=dict(G=G, H0_Gyr_inv=H0,
                  Omega_c=OC, Omega_b=OB, Omega_Lambda=OL, z_i=10, central_Msun=MB,
                  soft_kpc=SOFT, ramp_Gyr=RAMP, r_min_kpc=1, r_max_kpc=2000),
                  event=event_name, elapsed_Gyr=float(tt[-1]), end_z=float(1 / aa[-1] - 1),
                  central_mass_fraction_on=float(mass(tt[-1], central) / MB),
                  center_u_at_end=float(s[-1]**2), first_finite_r_at_end_kpc=float(rr[0, -1]),
                  first_finite_v_at_end_kpc_per_Gyr=float(radii[0] * v[0, -1]),
                  first_turnarounds=first_turn, checks=checks, nfev=sol.nfev,
                  original_stencil_witness=original_stencil_witness(n),
                  wall_seconds=time.perf_counter() - start,
                  non_claims=['No DT2 equivalence; no exact charge-current equation',
                              'No post-caustic state, halo equilibrium, EFE or retained mass prediction',
                              'Prescribed baryon excess ramp is not a mass-conserving galaxy formation model',
                              'Discrete shell-order check alone is not a continuum proof'])
    assert checks['regularized_energy_constraint_abs'] < 2.e-7
    assert checks['sampled_min_normalized_finite_spacing'] > 0
    assert checks['independent_physical_time_max_u_difference'] < 2.e-7
    assert checks['independent_physical_time_max_v_difference'] < 2.e-6
    if not central:
        assert checks['homogeneous_u_max_relative_error'] < 2.e-7
        assert checks['homogeneous_velocity_max_relative_error'] < 2.e-7
        assert checks['all_shell_velocities_outward']
        assert checks['initial_acceleration_is_inward']
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(out / 'trajectory.npz', tau_Gyr=tau, time_Gyr=tt, scale_factor=aa,
                        initial_radii_kpc=radii, u=u, udot_Gyr_inv=v, center_s=s, center_w=w,
                        energy_center=ee, density_over_present_cold=q)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=130)
    parser.add_argument('--central', action='store_true')
    parser.add_argument('--rtol', type=float, default=2.e-10)
    parser.add_argument('--atol', type=float, default=1.e-12)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    run(args.n, args.central, args.rtol, args.atol, args.output)
