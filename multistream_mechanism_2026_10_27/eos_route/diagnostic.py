"""Conditional logotropic core equilibrium, radial modes and radiative outlet.

No multistream transition or microscopic coefficient is derived by this code.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def equilibrium(tol):
    x0 = 1e-6
    def rhs(x, y):
        return [y[1], 1/y[0]-2*y[1]/x]
    # theta = 1+x^2/6-x^4/120+O(x^6)
    return solve_ivp(rhs, [x0, 40], [1+x0*x0/6, x0/3], rtol=tol,
                     atol=tol*0.01, dense_output=True, max_step=.04)


eq = equilibrium(2e-10)
eq2 = equilibrium(2e-12)
xi4 = brentq(lambda x: eq.sol(x)[0]-4, 1, 12, xtol=1e-12)
xi4b = brentq(lambda x: eq2.sol(x)[0]-4, 1, 12, xtol=1e-12)
xi_crit = brentq(lambda x: eq2.sol(x)[1]-1/math.sqrt(2), 1, 20)
contrast_crit = float(eq2.sol(xi_crit)[0])


def radial_mode(lam, edge, tol=3e-9):
    x0 = 1e-5
    c = 4/3+lam
    def rhs(x, y):
        th, tp = eq2.sol(x)
        return [y[1], -4*y[1]/x-(4*tp/(x*th)+lam/th)*y[0]]
    z = solve_ivp(rhs, [x0, edge], [1-c*x0*x0/10, -c*x0/5],
                  rtol=tol, atol=tol*.01, max_step=.025, dense_output=True)
    y = z.y[:, -1]
    return float(3*y[0]+edge*y[1]), z


def lowest_root(edge):
    # Brackets are synthetic finite diagnostic bounds, not a theorem on all modes.
    grid = np.linspace(-.8, 1.5, 116)
    roots = []
    prev, _ = radial_mode(grid[0], edge)
    for a, b in zip(grid[:-1], grid[1:]):
        val, _ = radial_mode(b, edge)
        if prev*val < 0:
            rt = brentq(lambda la: radial_mode(la, edge)[0], a, b, xtol=1e-10)
            _, z = radial_mode(rt, edge)
            sample = z.sol(np.linspace(1e-5, edge, 2001))[0]
            nodes = int(np.sum(sample[1:]*sample[:-1] < 0))
            roots.append({"lambda": float(rt), "nodes": nodes,
                          "boundary_residual": radial_mode(rt, edge)[0]})
            if nodes == 0:
                return roots[-1]
        prev = val
    raise RuntimeError('No nodeless root within declared bracket')


mode = lowest_root(xi4)
unstable = lowest_root(xi_crit*1.15)
coefficient_refined, _ = radial_mode(mode['lambda'], xi4, tol=3e-11)

# Exact hydrostatic scaling at fixed A: physical core radii from three rho0.
G = 6.67430e-11
c_light = 299792458.
hbar = 1.054571817e-34
rho_planck = c_light**5/(hbar*G*G)
msun = 1.98847e30
pc = 3.085677581491367e16
normalization = {}
for foot, a0 in [('canonical', 9.3603e-11), ('alt', 1.1312e-10)]:
    sig = a0/(2*math.pi*G)
    a_req = a0*a0/(math.pi*G*xi4*xi4)
    physical = []
    for rhoc in [1e-23, 1e-21, 1e-19]:
        rquarter = xi4*math.sqrt(a_req/(4*math.pi*G))/rhoc
        physical.append({'rho0_kg_m3':rhoc, 'rquarter_pc':rquarter/pc,
                         'Sigma_kg_m2':rhoc*rquarter})
    normalization[foot] = {'a0': a0, 'Sigma_target_Msun_pc2':sig*pc*pc/msun,
                           'A_required_Pa':a_req, 'cores':physical}
rho_lambda = 4*(9.3603e-11)**2/(G*c_light*c_light)
B_planck = 1/math.log(rho_planck/rho_lambda)
B_req = 1/(4*math.pi*xi4*xi4)
sigma_planck = xi4*math.sqrt(B_planck*rho_lambda*c_light*c_light/(4*math.pi*G))

# Linear normal-mode displacement q exports energy into a half-line mediator.
# Normalize modal mass=1, omega=1; Gamma=0.4; q(0)=0.1, qdot(0)=0.
gamma = .4
def oscillator(t, y):
    q, v, outgoing = y
    return [v, -q-gamma*v, gamma*v*v]
sol = solve_ivp(oscillator, [0, 100], [.1, 0, 0], rtol=1e-11, atol=1e-14,
                t_eval=np.linspace(0, 100, 4001))
q,v,out = sol.y
Ecore = .5*(q*q+v*v)
ledger_error = np.max(np.abs(Ecore+out-.005))/.005
omega_d = math.sqrt(1-gamma*gamma/4)
q_exact = .1*np.exp(-gamma*sol.t/2)*(np.cos(omega_d*sol.t)
                 +gamma/(2*omega_d)*np.sin(omega_d*sol.t))

checks = {
 'quarter_radius_refinement':abs(xi4-xi4b)<1e-8,
 'known_quarter_radius':abs(xi4-5.85)<.02,
 'core_nodeless_mode_positive':mode['lambda']>0 and mode['nodes']==0,
 'past_mass_turning_point_mode_negative':unstable['lambda']<0 and unstable['nodes']==0,
 'mode_refinement_boundary':abs(coefficient_refined)<1e-7,
 'mass_turning_point_zero_mode':abs(radial_mode(0,xi_crit)[0])<1e-7,
 'radiative_energy_ledger':ledger_error<1e-8,
 'analytic_damped_mode':float(np.max(np.abs(q-q_exact)))<1e-9,
 'perturbation_damped':float(Ecore[-1]/Ecore[0])<1e-12,
 'positive_outgoing_energy':float(np.min(np.diff(out)))>-1e-14,
 'surface_density_scale_independence':all(abs(v['Sigma_kg_m2']/
     normalization[foot]['cores'][0]['Sigma_kg_m2']-1)<1e-12
     for foot in normalization for v in normalization[foot]['cores']),
}
checks = {k:bool(v) for k,v in checks.items()}
result = {'scope':'conditional fixed-phase logotropic core; fixed external pressure; linear radial stability; modal wave outlet',
 'xi_quarter':float(xi4), 'xi_mass_turning_point':float(xi_crit),
 'critical_density_contrast':contrast_crit, 'core_mode':mode,
 'beyond_critical_mode':unstable,
 'B_required_for_canonical_target':B_req,'B_from_Planck_log_approximation':B_planck,
 'Planck_log_Sigma_over_target':sigma_planck/(9.3603e-11/(2*math.pi*G)),
 'normalization':normalization,
 'radiative_ledger_relative_error':float(ledger_error),
 'radiative_final_perturbation_energy_fraction':float(Ecore[-1]/Ecore[0]),
 'checks':checks,
 'non_claims':['Does not derive logotropic EOS from multistream dynamics',
 'Does not derive the required coefficient from Lambda','No nonlinear formation or open-halo stability',
 'No baryon potential or full kinetic stress','External pressure and active-phase retention are imposed boundary/phase assumptions',
 'No cosmological safety claim for a globally active EOS']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
