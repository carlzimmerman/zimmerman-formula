"""Independent exact scaling/threshold reductions and DE/Pauli benchmark."""
import sys
sys.dont_write_bytecode = True
import json
import math
from pathlib import Path
import resource
import time
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main(out):
    start = time.monotonic()
    record = json.loads((ROOT / 'reviews/radial_ir_cold_2026_11_01/run_units/result.json').read_text())
    constants = record['constants']
    C = record['photino_mass_coefficient']
    emax = .03
    rho_de = constants['rho_DE_GeV4']
    hbarc = constants['hbarc_GeV_cm']
    mu_de = (31 * rho_de)**.25
    maximum_mass = C * mu_de * emax**2.5
    cases = []
    for rho, v in [(.3, .001), (10., .0001)]:
        density = rho * hbarc**3
        mmin = (6 * math.pi**2 * density / (2 * v**3))**.25
        mu_min = mmin / (C * emax**2.5)
        ratio = (mu_min**4 / 31) / rho_de
        cases.append(dict(rho_GeV_cm3=rho, v_max=v, m_min_GeV=mmin,
                          mu_min_GeV=mu_min, required_raw_energy_over_DE=ratio,
                          required_cancellation_decimal_orders=math.log10(ratio),
                          raw_DE_max_photino_GeV=maximum_mass,
                          min_mass_over_raw_DE_mass=mmin / maximum_mass))

    r = sp.symbols('r', positive=True)
    beta = sp.sqrt(1-r**-2)
    q2 = r / beta
    derivative = sp.simplify(sp.diff(q2, r))
    critical = sp.simplify(derivative.subs(r, sp.sqrt(2)))
    # Independent direct construction of the allowed phase-space volume.
    p, mass, velocity, dof = sp.symbols('p m v g', positive=True)
    rho_bound = sp.simplify(mass * dof / (2*sp.pi)**3 * 4*sp.pi *
                            sp.integrate(p**2, (p, 0, mass*velocity)))
    W0, Planck, F, rho = sp.symbols('W0 M F rho', positive=True)
    net = F**2 - 3*W0**2/Planck**2
    slope = sp.diff(net, W0)*W0
    sensitivity = sp.simplify(slope.subs(W0**2, Planck**2*(F**2-rho)/3))
    powers = {'mu':sp.Rational(5,2), 'R':sp.Integer(2), 'm_parent':sp.Integer(4),
              'm_chi':sp.Integer(5), 'F':sp.Integer(5)}
    pair = 2*powers['m_chi'] + powers['m_parent'] - 2*powers['R']
    loss = 5*powers['m_chi'] - 2*powers['F']
    warmth = powers['m_parent'] - powers['m_chi'] - pair/2
    checks = {
        'direct_phase_space_integral': sp.simplify(rho_bound-dof*mass**4*velocity**3/(6*sp.pi**2)) == 0,
        'W0_sensitivity': sp.simplify(sensitivity+2*(F**2-rho)) == 0,
        'scalar_pair_exponent10': pair == 10,
        'candidate_loss_exponent15': loss == 15,
        'RD_warmth_exponent_minus6': warmth == -6,
        'threshold_stationary_sqrt2': critical == 0,
        'threshold_stationary_is_minimum': sp.diff(q2,r,2).subs(r,sp.sqrt(2)) > 0,
        'threshold_divergence': sp.limit(q2,r,1,dir='+') == sp.oo,
        'both_raw_DE_cases_fail_density': all(c['min_mass_over_raw_DE_mass'] > 1e10 for c in cases),
        'unit_conversion_matches_prior': abs(mu_de/constants['mu_if_raw_vacuum_is_DE_GeV']-1)<1e-14,
    }
    result = dict(claim_id='TP06_STRUCTURAL_SCALE_CONSTRAINTS', checks={k:bool(v) for k,v in checks.items()},
                  mu_if_raw_energy_is_DE_GeV=mu_de, e_max=emax,
                  mass_coefficient_at_inherited_rigid_minimum=C, cases=cases,
                  symbolic_threshold_derivative=str(derivative),
                  scaling_exponents=dict(pair=int(pair), candidate_loss=int(loss), RD_warmth=int(warmth)),
                  scope='Exact stated reductions plus two compact-support density benchmarks at the inherited leading-pole mass coefficient. No new gravity vacuum or production calculation.',
                  runtime_seconds=time.monotonic()-start,
                  peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert all(checks.values()), checks


if __name__ == '__main__':
    main(sys.argv[1])
