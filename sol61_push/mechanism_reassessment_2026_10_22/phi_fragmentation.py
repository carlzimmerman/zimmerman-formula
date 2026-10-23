"""Linear self-resonance gate for the quantum-generated Phi background.

Uses the leading quartic, radial-orbit limit of the existing action. This is
neither a nonlinear lattice evolution nor a post-fragmentation yield solver.
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import ellipj, ellipk

ROOT = Path(__file__).parent
source = json.loads((ROOT / 'stochastic_source_run/results.json').read_text())
H = source['H_inf_GeV']
lam, g, m = .00881292, 2.168e-6, .001
M = 2*m*np.sqrt(1+.02**2)
period = 2*ellipk(.5)  # cn^2 period, half the background period


def monodromy(k2, coefficient, tol):
    def rhs(z, y):
        cn = ellipj(z, .5)[1]
        omega2 = k2+coefficient*cn*cn
        return [y[1], -omega2*y[0], y[3], -omega2*y[2]]
    sol = solve_ivp(rhs, [0, period], [1., 0., 0., 1.], method='DOP853',
                    rtol=tol, atol=tol*.01)
    if not sol.success:
        raise RuntimeError(sol.message)
    a, b, c, d = sol.y[:, -1]
    trace, det = a+d, a*d-b*c
    mu = np.arccosh(max(1., abs(trace)/2))/period
    return float(mu), float(det), float(trace)


def scan(tol):
    rows = []
    for coefficient in [0, 1, 3]:
        for k2 in np.linspace(.0025, 2., 800):
            mu, det, trace = monodromy(k2, coefficient, tol)
            rows.append(dict(coefficient=coefficient, k2=float(k2),
                             mu=mu, determinant=det, trace=trace))
    return rows


coarse, fine = scan(2e-9), scan(2e-11)
peaks = {}
for c in [1, 3]:
    row = max((r for r in fine if r['coefficient'] == c), key=lambda r:r['mu'])
    peaks[str(c)] = row
mu = peaks['1']['mu']
z20 = 20/mu
samples = np.asarray(source['final_field_samples_over_H'])
F = np.linalg.norm(samples[:, :2], axis=1)  # canonical radial field / H
X = H*np.linalg.norm(samples[:, 2:], axis=1)/np.sqrt(2)


def quantiles(a):
    return np.quantile(a, [.1, .5, .9]).tolist()


matching = []
for choice in ['frozen', 'slow_roll']:
    # Radiation matched at a=1, H_rad=H; a=1+H eta, a''=0.
    # F_conf'=F+dot(f)/H^2. This is a declared momentum bracket, not
    # conjugate momenta extracted from the field-only stochastic samples.
    velocity = F if choice == 'frozen' else F-lam*F**3/3
    amplitude = (F**4+2*velocity**2/lam)**.25
    # Conserved conformal quartic energy gives the amplitude exactly in
    # the decoupled massless homogeneous limit, including onset transient.
    a20 = 1+z20/(np.sqrt(lam)*amplitude)
    H20 = H/a20**2
    phi_peak = H*amplitude/(np.sqrt(2)*a20)
    perturbation_ratio = 2*g*X/(lam*(H*amplitude/a20)**2)
    # Frozen X is self-consistent here only while H20 >> M.
    # Compare secular X acceleration g Phi^2 / (H20^2 X), not just Hessians.
    X_forcing = g*phi_peak**2/(H20**2*X)
    matching.append(dict(momentum_matching=choice,
        a_at_20_asymptotic_growth_efolds_quantiles=quantiles(a20),
        H_at_20_GeV_quantiles=quantiles(H20),
        H_over_M_min=float(np.min(H20/M)),
        trilinear_over_quartic_curvature_max=float(np.max(perturbation_ratio)),
        X_forcing_over_H2X_max=float(np.max(X_forcing)),
        Phi_peak_GeV_quantiles=quantiles(phi_peak),
        conformal_amplitude_over_H_quantiles=quantiles(amplitude)))

# Exact Lamé band intervals in this quartic reduction are checked away
# from edges. They are also obtained independently by the monodromy trace.
interior = [r for r in fine if r['coefficient']==1 and .01<r['k2']<.49]
exterior = [r for r in fine if r['coefficient']==1 and .51<r['k2']<2]
long_in = [r for r in fine if r['coefficient']==3 and 1.51<r['k2']<1.72]
long_out = [r for r in fine if r['coefficient']==3 and
            (.02<r['k2']<1.48 or 1.75<r['k2']<2)]
checks = dict(
    wronskian=max(abs(r['determinant']-1) for r in fine)<1e-8,
    refinement=max(abs(a['mu']-b['mu']) for a,b in zip(coarse,fine))<1e-6,
    free_control=max(r['mu'] for r in fine if r['coefficient']==0)<1e-7,
    transverse_band=min(r['mu'] for r in interior)>0 and max(r['mu'] for r in exterior)<1e-7,
    longitudinal_band=min(r['mu'] for r in long_in)>0 and max(r['mu'] for r in long_out)<1e-7,
    early_decoupling=all(r['H_over_M_min']>1e6 and
        r['trilinear_over_quartic_curvature_max']<1e-5 and
        r['X_forcing_over_H2X_max']<1e-5 for r in matching))
out = dict(checks=checks, all_pass=all(checks.values()), peaks=peaks,
    coefficient_period=period, z_for_20_growth_efolds=z20,
    matching_brackets=matching, fine_scan=fine,
    scope='Conditional radial quartic condensate linear instability. No matched spatial quantum covariance, nonlinear saturation, particle yield, cold fraction, or collapse input is computed. Twenty growth e-folds is a timing diagnostic, not a measured fragmentation time. Orbit charge and reheating matching remain conditional.')
Path(sys.argv[1]).write_text(json.dumps(out, indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='fine_scan'},indent=2))
sys.exit(0 if out['all_pass'] else 1)
