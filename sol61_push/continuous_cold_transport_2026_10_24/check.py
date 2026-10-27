"""Small algebraic controls; no galaxy simulation or theory-completion claim."""
import json
import math
from fractions import Fraction as F
from pathlib import Path

checks = {}
# Homologous Gaussian E=A/R^2-C/R: evaluate exact dimensionless stationary point.
A, C = F(3, 4), F(1)
R = 2*A/C
checks['gaussian_stationary'] = -2*A/R**3+C/R**2 == 0
checks['gaussian_positive_curvature'] = 6*A/R**4-2*C/R**3 > 0
checks['gaussian_bound'] = A/R**2-C/R < 0
# Equal counterstreams: mean velocity is zero but stress is not.
v0 = F(2)
mean = (v0-v0)/2
stress = ((v0-mean)**2+(-v0-mean)**2)/2
checks['counterstream_stress'] = mean == 0 and stress == v0**2
# A collapsing pressureless map reaches zero Jacobian in finite time.
checks['single_stream_crossing'] = 1-F(2)*F(1,2) == 0
# Outgoing monochromatic mode, arbitrary dimensionless eta,k and integer m.
eta,k,m,flux = F(2),F(3),2,F(5)
omega = eta*k*k/2
energy, angular = eta*omega*flux, eta*m*flux
checks['mode_energy_to_angular'] = angular/energy == m/omega
checks['spherical_export_has_no_spin'] = eta*0*flux == 0
# Cauchy control and its saturation for an advected shell, M=R=1.
weights = [F(1,2),F(1,2)]
vt = [F(1),F(3)]
J = sum(w*v for w,v in zip(weights,vt))
K = sum(w*v*v/2 for w,v in zip(weights,vt))
checks['ballistic_cauchy'] = J*J <= 2*K
checks['ballistic_bound_saturates_uniform_v'] = F(2)**2 == 2*(F(2)**2/2)
checks['universal_eta_gaussian_MR'] = math.isclose(
    2*(3*math.sqrt(2*math.pi)/(2*2)),
    7*(3*math.sqrt(2*math.pi)/(2*7)), rel_tol=1e-14)
assert all(checks.values()), checks
result = {'assertion_tested': 'Ten scalar/algebraic controls of explicitly stated trial, stream and outgoing-mode classes',
          'checks': checks, 'passed': sum(checks.values()),
          'not_tested': ['nonlinear wave formation', 'covariant completion', 'eta origin',
                         'phase conversion', 'four dwarf budgets', 'stellar heating', 'actual mode excitation']}
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
