"""Bounded time-local threshold audit; not a self-consistent kinetic solver."""
import cmath
import json
import math
from pathlib import Path
import sys

from scipy.integrate import quad
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'sol61_push'
initial = json.loads((BASE / 'thermal_carrier_initial_production_2026_10_13/run/results.json').read_text())
feedback = json.loads((BASE / 'carrier_self_feedback_2026_10_13/run/results.json').read_text())
source = json.loads((BASE / 'ordinary_lepton_source_2026_10_13/run/results.json').read_text())
HBAR = 6.582119569e-16  # eV s; inherited numerical convention
checks = []


def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    assert value, name


# Exact algebra for the previously derived, time-local trajectory.
s, d0, ts, h = sp.symbols('s d0 ts h', positive=True)
d = d0 * (1-s)**2
minus_ddot = -sp.diff(d, s) / ts
eps = h * minus_ddot / d**2
check('threshold-gradient identity', sp.simplify(eps - 2*h/(d0*ts*(1-s)**3)) == 0)
check('threshold variation time', sp.simplify(d/minus_ddot - ts*(1-s)/2) == 0)

rows = []
for f, i in zip(feedback['rows'], initial['rows']):
    check('matching bath temperature ' + str(f['T_MeV']), f['T_MeV']*1e6 == i['T_MeV']*1e6)
    D = i['effective_pair_excess_eV']
    tstar = f['on_shell_closure_time_toy_s']
    gamma_phi0 = i['quasiparticle_spontaneous_partial_width_eV']
    gamma_g = source['reduced_muon_case']['photon_width_eV']
    eps0 = 2*HBAR/(D*tstar)
    u = eps0**(1/3)  # u = 1-s; epsilon=1
    Dmem = D*u*u
    # In the SAME narrow on-shell model, width falls as sqrt(D/D0).
    gamma_at_mem = gamma_g + gamma_phi0*u
    tau_form = HBAR/Dmem
    tau_variation = tstar*u/2
    check('formation/variation crossing ' + str(f['T_MeV']), abs(tau_form/tau_variation - 1) < 1e-13)
    check('crossing before formal closure ' + str(f['T_MeV']), 0 < u < 1)
    rows.append({
        'T_MeV': f['T_MeV'], 'D0_eV': D, 'tstar_s': tstar,
        'initial_gradient_parameter': eps0,
        'epsilon_one_time_over_tstar': 1-u,
        'epsilon_one_gap_over_D0': u*u,
        'epsilon_one_J_over_Jstar': 1-u*u,
        'epsilon_one_gap_eV': Dmem,
        'formation_and_variation_time_s': tau_form,
        'rest_decay_width_at_crossing_eV': gamma_at_mem,
        'gap_over_rest_decay_width': Dmem/gamma_at_mem,
        'remaining_time_times_rest_decay_width_over_hbar': tstar*u*gamma_at_mem/HBAR,
    })


# A separate, deliberately simple finite-pulse continuum benchmark.
# epsilon=(pair kinetic energy); spectral weight g sqrt(epsilon) exp(-epsilon/Lambda).
# At D=0 set x=epsilon*t/hbar and L=Lambda*t/hbar. After dividing by
# g sqrt(t/hbar), P is this dimensionless integral. No reservoir inference.
def finite_pulse_integral(L):
    low = quad(lambda x: math.sqrt(x)*math.exp(-x/L)*(math.sin(x/2)/(x/2))**2,
               0, 1, epsabs=1e-11, epsrel=1e-11)[0]
    tail = quad(lambda x: 2*math.exp(-x/L)/x**1.5,
                1, math.inf, epsabs=1e-11, epsrel=1e-11)[0]
    oscillatory = quad(lambda x: 2*math.exp(-x/L)/x**1.5,
                      1, math.inf, weight='cos', wvar=1,
                      epsabs=1e-11, limlst=200)[0]
    return low + tail - oscillatory


kernel_rows = []
for L in [0.01, 0.1, 1, 10, 100, 1000]:
    exact = 4*math.sqrt(math.pi)*(cmath.sqrt(1/L-1j).real - math.sqrt(1/L))
    numerical = finite_pulse_integral(L)
    error = abs(numerical/exact - 1)
    check('finite-pulse regulated threshold integral ' + str(L), error < 2e-9)
    kernel_rows.append({'Lambda_t_over_hbar': L, 'dimensionless_probability_coefficient': exact,
                        'independent_quadrature_relative_error': error})

result = {'all_pass': all(c['passed'] for c in checks), 'checks': checks,
          'rows': rows, 'finite_pulse_rows': kernel_rows,
          'unregulated_threshold_coefficient': 2*math.sqrt(2*math.pi),
          'non_claims': [
              'epsilon=1 is a timescale diagnostic, not a sharp physical transition or error bound',
              'Rest-source reference only; moving-parent momentum-dependent memory not integrated',
              'Decay-width comparison excludes uncomputed thermal scattering/decoherence',
              'Finite-pulse benchmark has prescribed switching and no self-consistent feedback',
              'No final yield, experimentally established particles or manufacturing protocol'
          ]}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'all_pass': result['all_pass'], 'checks': len(checks), 'T2': rows[2]}))
