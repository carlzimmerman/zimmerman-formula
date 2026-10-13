"""Conditional dipolar growing-mode repair audit; not a halo simulation."""
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import solve_ivp

P = Path(__file__).parent
G = 6.67430e-11
GYR = 365.25*86400*1e9
KPC = 3.085677581491367e19
checks, rows = {}, []
# Dimensionless q''+d*q'-q=0. Stable expression avoids subtraction.
for d in [0., .01, 1., 10., 100.]:
    lp = 2/(math.sqrt(d*d+4)+d)
    lm = -(math.sqrt(d*d+4)+d)/2
    checks[f'positive_root_{d}'] = lp > 0
    checks[f'root_product_{d}'] = abs(lp*lm+1) < 1e-12
    sol = solve_ivp(lambda t,y: [y[1], y[0]-d*y[1]],
                    [0,2], [1,0], rtol=2e-10, atol=1e-12)
    exact = (-lm*math.exp(2*lp)+lp*math.exp(2*lm))/(lp-lm)
    checks[f'ode_{d}'] = bool(sol.success and abs(sol.y[0,-1]/exact-1)<1e-8)

T, S, v = 10*GYR, .03, 2e5  # SI: .3 cm^2/g; illustrative speed.
for rho in [1e-27, 1e-25, 1e-23, 1e-21]:
    omega2 = 4*math.pi*G*rho
    omega = math.sqrt(omega2)
    gamma = rho*S*v
    lp = 2*omega2/(math.sqrt(gamma*gamma+4*omega2)+gamma)
    required_gamma = max(0., omega2*T-1/T)
    required_S = required_gamma/(rho*v)
    checks[f'damped_slower_{rho}'] = lp <= omega*(1+1e-14)
    if required_gamma:
        repaired = 2*omega2/(math.sqrt(required_gamma**2+4*omega2)+required_gamma)
        checks[f'ten_gyr_root_{rho}'] = abs(repaired*T-1)<1e-12
    rows.append(dict(rho_kg_m3=rho, e_fold_Gyr=1/(omega*GYR),
                     damped_e_fold_Gyr=1/(lp*GYR), gamma_over_omega=gamma/omega,
                     S_for_ten_Gyr_cm2_g=10*required_S,
                     stiffness_speed_100kpc_km_s=omega*100*KPC/math.pi/1000))
# Spatial restoring force shifts the finite-domain spectrum, not k=0.
for ck, omega0 in [(0.,0.), (.5,0.), (2.,0.), (0.,2.)]:
    eig = np.linalg.eigvals([[0.,1.], [1-ck*ck-omega0*omega0,-.1]])
    expected_stable = ck*ck+omega0*omega0 > 1
    checks[f'stability_{ck}_{omega0}'] = bool((max(eig.real)<0)==expected_stable)
result = dict(checks=checks, all_pass=all(checks.values()), rows=rows,
              undamped_density_for_ten_Gyr_kg_m3=1/(4*math.pi*G*T*T),
              interpretation='Conditional reduced growing mode. Collision frequency is only an optimistic proxy for damping, not a derived polarization coupling. Spatial boundary and restoring terms are hypothetical.')
(P/'polarization_repair_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['all_pass']
