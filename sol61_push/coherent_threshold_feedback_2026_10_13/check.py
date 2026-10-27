"""Hamiltonian continuum surrogate with conserved norm and energy diagnostics.

Calibrates initial moment rates only. It is NOT the thermal quantum field theory.
"""
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / 'sol61_push'
feed = json.loads((base / 'carrier_self_feedback_2026_10_13/run/results.json').read_text())['rows'][2]
init = json.loads((base / 'thermal_carrier_initial_production_2026_10_13/run/results.json').read_text())['rows'][2]
HBAR = 6.582119569e-16
D0 = init['effective_pair_excess_eV']
fstar = feed['parent_depletion_fraction_estimate']
tau_star = feed['on_shell_closure_time_toy_s']*D0/HBAR
gamma = 2*fstar/tau_star
kappa = 1/fstar
checks = []


def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    assert value, name


def grid(n, cutoff, lam, strength):
    # epsilon=q^2 resolves the sqrt(epsilon) threshold without a singular grid weight.
    dq = math.sqrt(cutoff)/n
    q = (np.arange(n)+0.5)*dq
    e = q*q
    v = np.sqrt(strength*2*q*q*np.exp(-e/lam)*dq)
    return e, v


def evolve(n, cutoff, lam, step, end, coupling=gamma, repulsion=kappa, source_energy=1.0,
           sample_count=201):
    # J(e)=strength sqrt(e) exp(-e/lam). For source energy 1, 2pi J(1)=coupling.
    strength = coupling*math.exp(1/lam)/(2*math.pi)
    e, v = grid(n, cutoff, lam, strength)
    V = np.linalg.norm(v)
    u = v/V
    intervals = sample_count-1
    steps_per_interval = max(1, math.ceil(end/intervals/step))
    dt = end/(intervals*steps_per_interval)
    free_half = np.exp(-0.5j*e*dt)
    source_half = np.exp(-0.5j*source_energy*dt)
    co, si = math.cos(V*dt), math.sin(V*dt)
    a, b = 1+0j, np.zeros(n, dtype=complex)
    rows = []

    def observe(t):
        weights = np.abs(b)**2
        B = float(weights.sum())
        coherent = float(2*np.real(np.conj(a)*np.dot(v, b)))
        kinetic = float(np.dot(e, weights))
        self_energy = repulsion*B*B/2
        energy = source_energy*abs(a)**2+kinetic+self_energy+coherent
        rows.append({'tau': t, 'B': B, 'B_over_fstar': B/fstar,
                     'norm_error': abs(abs(a)**2+B-1),
                     'energy_error_over_D0_fstar': (energy-source_energy)/fstar,
                     'kinetic_over_D0_fstar': kinetic/fstar,
                     'self_energy_over_D0_fstar': self_energy/fstar,
                     'coherent_energy_over_D0_fstar': coherent/fstar})

    observe(0)
    for it in range(1, intervals*steps_per_interval+1):
        # Exact subflow of diagonal nonlinear Hamiltonian: B is fixed here.
        B = float(np.vdot(b, b).real)
        a *= source_half
        b *= free_half*np.exp(-0.5j*repulsion*B*dt)
        # Exact rank-two source/bright-continuum rotation, preserving norm.
        bright = np.dot(u, b)
        old_a = a
        a = co*old_a-1j*si*bright
        b += u*((co-1)*bright-1j*si*old_a)
        B = float(np.vdot(b, b).real)
        a *= source_half
        b *= free_half*np.exp(-0.5j*repulsion*B*dt)
        if it % steps_per_interval == 0:
            observe(it*dt)
    return {'n': n, 'cutoff': cutoff, 'lambda': lam, 'dt': dt, 'end': end,
            'gamma': coupling, 'kappa': repulsion, 'source_energy': source_energy,
            'rows': rows, 'max_B_over_fstar': max(r['B_over_fstar'] for r in rows),
            'final_B_over_fstar': rows[-1]['B_over_fstar'],
            'max_norm_error': max(r['norm_error'] for r in rows),
            'max_energy_error_over_D0_fstar': max(abs(r['energy_error_over_D0_fstar']) for r in rows)}, (a,b), (e,v)


# Orthogonal check: exact finite-matrix solution, no feedback.
linear, state, ev = evolve(96, 30, 5, .001, 3, coupling=.02, repulsion=0, sample_count=4)
e,v = ev
matrix = np.diag(np.r_[1.0, e])
matrix[0,1:] = v
matrix[1:,0] = v
vals, vectors = eigh(matrix)
exact = vectors @ (np.exp(-3j*vals)*vectors[0,:])
linear_error = float(np.max(np.abs(np.r_[state[0],state[1]]-exact)))
check('Strang evolution versus independent matrix diagonalization', linear_error < 2e-7)

# Threshold finite-pulse benchmark from the previous package, with a finite regulator.
pulse, _, _ = evolve(4096, 100, 5, .01, 10, coupling=1e-8,
                      repulsion=0, source_energy=0, sample_count=11)
g = 1e-8*math.exp(1/5)/(2*math.pi)
born = 4*g*math.sqrt(math.pi)*(np.sqrt(.2-10j).real-math.sqrt(.2))
pulse_error = abs(pulse['rows'][-1]['B']/born-1)
check('weak threshold finite-pulse probability', pulse_error < 2e-4)

runs = []
for n, cutoff, lam, dt in [(2048,120,5,.04), (4096,120,5,.02),
                            (4096,120,5,.01), (8192,160,5,.01),
                            (4096,120,2,.01), (8192,160,10,.01)]:
    run, _, _ = evolve(n,cutoff,lam,dt,2*tau_star)
    check('norm '+str((n,cutoff,lam,dt)),run['max_norm_error']<1e-10)
    check('energy '+str((n,cutoff,lam,dt)),run['max_energy_error_over_D0_fstar']<.003)
    runs.append(run)
fine = np.array([r['B_over_fstar'] for r in runs[2]['rows']])
time_error = float(np.max(np.abs(fine-np.array([r['B_over_fstar'] for r in runs[1]['rows']]))))
grid_error = float(np.max(np.abs(fine-np.array([r['B_over_fstar'] for r in runs[3]['rows']]))))
check('time step refinement of population',time_error<.002)
check('grid and cutoff refinement of population',grid_error<.002)

result={'all_pass':all(c['passed'] for c in checks),'checks':checks,
        'calibration':{'D0_eV':D0,'fstar':fstar,'tau_star':tau_star,'gamma_over_D0':gamma,
                       'kappa_over_D0':kappa,'initial_gradient_parameter':2/tau_star},
        'linear_matrix_max_amplitude_error':linear_error,'threshold_born_relative_error':float(pulse_error),
        'time_refinement_max_B_over_fstar_difference':time_error,
        'grid_refinement_max_B_over_fstar_difference':grid_error,'runs':runs,
        'non_claims':['Effective source/continuum surrogate, not the thermal R-phi field theory',
                      'Cutoff shape, bare initial state and spectral regulator remain model choices',
                      'No full bath evolution, final asymptotic yield, confinement or manufacturing protocol']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_pass':result['all_pass'],'checks':len(checks),
                  'time_error':time_error,'grid_error':grid_error,
                  'runs':[{k:r[k] for k in ['n','lambda','dt','max_B_over_fstar','final_B_over_fstar','max_energy_error_over_D0_fstar']} for r in runs]}))
