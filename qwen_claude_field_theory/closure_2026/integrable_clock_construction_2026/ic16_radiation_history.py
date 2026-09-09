#!/usr/bin/env python3
"""IC16: same IC11 phase action, one-sided switch, explicit radiation fluid.

The action definition and limits are in IC16_RADIATION_HISTORY.md. The new
switch is substituted globally, not only in an acceptance flag. These runs
vary and solve its eta=1 restriction; they do not certify the transition.
"""
import argparse
import json
import mpmath as mp
import sympy as sp
import ic11_clock_pressure as vacuum


def eta_up(r):
    r = mp.mpf(r)
    E = lambda x: mp.exp(-1/x) if x > 0 else mp.mpf(0)
    a, b = E(r*r-mp.mpf(1)/2), E(mp.mpf(3)/4-r*r)
    return a/(a+b)


def identities():
    z, Z, c, X, fx, fxx, f, H, R, wS = sp.symbols(
        'z Z c X fx fxx f H R wS', positive=True)
    pressure = c*Z**2
    rz = 2*Z*sp.diff(pressure, Z)-pressure
    q = fx*sp.sqrt(2*X)
    qX = fxx*sp.sqrt(2*X)+fx/sp.sqrt(2*X)
    Q = fx+2*X*fxx
    Xdot = -6*H*X*fx/Q
    rhocX = Q
    # Physical radiation density and scale factor: R/z² and sqrt(z)*Atilde.
    zdot = 6*H*z*fx*wS/Q
    rho_phys = R/z**2
    rho_phys_dot = -4*H*R/z**2-2*R*zdot/z**3
    Hphys = (H+zdot/(2*z))/sp.sqrt(z)
    return dict(
        radiation_conformal_invariance=sp.simplify(z**2*c*(Z/z)**2-pressure),
        radiation_no_auxiliary_source=sp.diff(z**2*c*(Z/z)**2, z),
        radiation_equation_of_state=sp.simplify(rz-3*pressure),
        radiation_kinetic=sp.simplify(sp.diff(pressure,Z)+2*Z*sp.diff(pressure,Z,2)-6*c*Z),
        radiation_sound_speed=sp.simplify(sp.diff(pressure,Z)/(sp.diff(pressure,Z)+2*Z*sp.diff(pressure,Z,2))-sp.Rational(1,3)),
        clock_charge_equation=sp.simplify(qX*Xdot+3*H*q),
        clock_continuity=sp.simplify(rhocX*Xdot+3*H*(2*X*fx)),
        physical_radiation_Ward=sp.simplify(rho_phys_dot/sp.sqrt(z)+4*Hphys*rho_phys),
    )


def state(S, radiation):
    S, radiation = map(mp.mpf, (S, radiation))
    if S <= 0 or radiation < 0:
        raise ValueError('Require S>0 and nonnegative Einstein-frame radiation')
    old = vacuum.state(S)
    w, rho = old['w'], old['energy']
    z = mp.exp(2*w)
    H = mp.sqrt((rho+radiation)/(3*mp.exp(-mp.mpf(1)/6)))
    physical_H = old['physical_H']*H/old['H']
    r = mp.exp(S-mp.mpf(1)/6)*H/z
    A = old['auxiliary_schur']
    matrix = mp.matrix([[0,A],[-A,0]])
    _, singular, _ = mp.svd(matrix)
    rank = sum(abs(value) > mp.mpf('1e-35') for value in singular)
    return dict(S=S, w=w, z=z, X=old['X'], clock_energy=rho,
                radiation=radiation, radiation_fraction=radiation/(rho+radiation),
                physical_radiation=radiation/z**2, H=H, physical_H=physical_H,
                activation_r_squared=r*r,
                compact_plateau=bool(mp.mpf(3)/4 <= r*r <= mp.mpf(5)/4),
                up_plateau=bool(r*r >= mp.mpf(3)/4),
                clock_healthy=old['vacuum_healthy'], kinetic=old['kinetic'],
                clock_speed_squared=old['speed_squared'],
                clock_charge_density=old['clock_charge_density'],
                auxiliary_rank_at_tolerance_1e_35=rank,
                auxiliary_schur=A, constraint=old['constraint'])


def radiation_cap(S):
    bg = state(S, 0)
    r2 = bg['activation_r_squared']
    cap = bg['clock_energy']*(mp.mpf(5)/(4*r2)-1)
    return dict(S=mp.mpf(S), radiation_cap=cap,
                maximum_radiation_fraction=1-4*r2/5,
                vacuum_in_compact_plateau=bg['compact_plateau'])


def condensate_endpoint():
    """Located FX=0 crossing, NOT an accepted endpoint of the healthy theory."""
    return mp.findroot(lambda S: vacuum.state(S)['PX'], (mp.mpf('.45'), mp.mpf('.6')))


def history(start='.03', radiation_start='1e16', barred_efolds=8, samples=65):
    start, radiation_start, barred_efolds = map(mp.mpf, (start, radiation_start, barred_efolds))
    if radiation_start <= 0 or barred_efolds <= 0 or samples < 2:
        raise ValueError('Require positive radiation, expansion, and >=2 samples')
    first = state(start, radiation_start)
    endpoint = condensate_endpoint()
    if not start < endpoint or not first['clock_healthy']:
        raise ValueError('Start must be on the positive-charge healthy branch before FX=0')
    q0 = first['clock_charge_density']
    rows = []
    for i in range(samples):
        N = barred_efolds*i/(samples-1)
        target = q0*mp.exp(-3*N)
        # A bracketed solve avoids extrapolating past the zero-charge endpoint.
        S = start if i == 0 else mp.findroot(
            lambda s: vacuum.state(s)['clock_charge_density']-target,
            (start, endpoint), solver='anderson', maxsteps=200,
            tol=mp.power(10,-mp.mp.dps+8))
        if not start <= S < endpoint:
            raise ArithmeticError('Charge inversion left the defined branch')
        R = radiation_start*mp.exp(-4*N)
        row = state(S, R)
        Nphys = N+row['w']-first['w']
        row.update(barred_efolds=N, physical_efolds=Nphys,
                   clock_charge_ratio=mp.exp(3*N)*row['clock_charge_density']/q0,
                   physical_radiation_conservation_ratio=(
                       row['physical_radiation']*mp.exp(4*Nphys)/first['physical_radiation']))
        rows.append(row)
    return dict(action='IC16 one-sided IC11 phase action plus conformal radiation fluid',
                full_theory_closed=False, interval_certified=False,
                start_S=start, endpoint_FX_zero=endpoint,
                initial_radiation=radiation_start, samples=samples,
                barred_efolds=barred_efolds, physical_efolds=rows[-1]['physical_efolds'],
                rows=rows)


def report():
    mp.mp.dps = 60
    trajectory = history()
    rows = trajectory['rows']
    critical = mp.findroot(lambda S: mp.diff(lambda x: state(x,0)['activation_r_squared'], S),
                           (mp.mpf('.07'),mp.mpf('.1')))
    return dict(candidate='IC16', full_theory='OPEN',
                exact_checks={k: v == 0 for k,v in identities().items()},
                compact_switch_limit=radiation_cap(critical),
                radiation_history=trajectory,
                finite_checks=dict(
                    healthy_clock_samples=sum(r['clock_healthy'] for r in rows),
                    activated_samples=sum(r['up_plateau'] for r in rows),
                    minimum_radiation_fraction=min(r['radiation_fraction'] for r in rows),
                    minimum_clock_speed_squared=min(r['clock_speed_squared'] for r in rows),
                    maximum_charge_residual=max(abs(r['clock_charge_ratio']-1) for r in rows),
                    maximum_physical_radiation_residual=max(abs(r['physical_radiation_conservation_ratio']-1) for r in rows)),
                exposed_ghost_control=state('.001','1e16'),
                nonclaims=[
                    'IC16 changes the global switch; it is not IC14 plus every earlier repair',
                    'Radiation is an isentropic C Z² fluid, not a photon Boltzmann/recombination calculation',
                    'Finite healthy trajectory does not remove the explicitly exposed ghost on another branch',
                    'No scalar strong-coupling cutoff or zero-sound-speed endpoint regularity established',
                    'No tested new transition, global Dirac count, sourced galaxy matching, PPN, or cluster fit',
                    'Initial radiation and clock charge are design initial data, not fitted observations'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure', action='store_true')
    args = parser.parse_args()
    result = report()
    print(json.dumps(result, indent=2, default=lambda v: mp.nstr(v,40)))
    history_result = result['radiation_history']
    if not all(result['exact_checks'].values()) or not all(
            r['up_plateau'] and r['clock_healthy'] for r in history_result['rows']):
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == '__main__':
    raise SystemExit(main())
