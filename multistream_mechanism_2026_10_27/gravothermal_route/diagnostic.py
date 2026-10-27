"""Bounded two-reservoir counterexample; see contract.json and REPORT.md."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
rows = []
for B, tc in [(2., 1.01), (2., .99), (.5, 1.01), (.5, 1.11)]:
    Cc, Ce, K, te = -1., B, 1., 1.
    def rhs(t, y):
        luminosity = K * (y[0] - y[1])
        return [-luminosity / Cc, luminosity / Ce]
    times = np.linspace(0., 5., 501)
    sol = solve_ivp(rhs, [0., 5.], [tc, te], t_eval=times,
                    rtol=1e-11, atol=1e-13)
    exponent = -K * (1. / Cc + 1. / Ce)
    delta_exact = (tc - te) * np.exp(exponent * times)
    energy = Cc * sol.y[0] + Ce * sol.y[1]
    energy_error = float(np.max(np.abs(energy - energy[0])))
    delta_error = float(np.max(np.abs(sol.y[0] - sol.y[1] - delta_exact)))
    equilibrium_T = float(energy[0] / (Cc + Ce))
    assert sol.success and energy_error < 1e-12 and delta_error < 1e-9
    rows.append(dict(Ccore=Cc, Cenvelope=Ce, initial_Tcore=tc,
                     exponent=exponent, stable=exponent < 0,
                     final_Tcore=float(sol.y[0,-1]), final_Tenvelope=float(sol.y[1,-1]),
                     equilibrium_T=equilibrium_T,
                     equilibrium_Sigma_normalized=equilibrium_T**2,
                     final_radius_over_initial=float(tc/sol.y[0,-1]),
                     max_energy_error=energy_error, max_delta_error=delta_error))

# Under x -> lambda*x, v -> lambda*v, t unchanged, rho is unchanged,
# M -> lambda^3*M, Phi -> lambda^2*Phi, Sigma -> lambda*Sigma.
scaling = [dict(scale=s, density_ratio=1., mass_ratio=s**3,
                velocity_ratio=s, surface_density_ratio=s)
           for s in [.1, 1., 10.]]

G, c, pc, msun, kappa = 6.67430e-11, 299792458., 3.085677581491367e16, 1.98847e30, .5
vacuum = []
for label, a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
    rhoL = (a0/(kappa*c))**2/G
    sigma = a0/(2*np.pi*G)
    H = np.sqrt(8*np.pi*G*rhoL/3)
    for rk in [1.,300.]:
        R = rk*1000*pc
        rho = sigma/R
        # King core identity rho0*r0^2=9*theta/(4*pi*G).
        # Its central pressure is (4*pi*G/9)*Sigma^2.
        pressure_ratio = (4*np.pi*G/9)*sigma**2/(rhoL*c*c)
        assert abs(pressure_ratio - kappa*kappa/(9*np.pi)) < 1e-16
        vacuum.append(dict(footing=label, radius_kpc=rk,
                           rhoLambda_kgm3=rhoL, HLambda_per_s=H,
                           Sigma_solar_pc2=sigma/(msun/pc**2),
                           vacuum_to_core_uniform_force_ratio=2*rhoL/rho,
                           target_King_pressure_over_vacuum_energy=pressure_ratio))

result = dict(status='completed', reservoir_rows=rows, exact_similarity_examples=scaling,
              vacuum_rows=vacuum,
              checks={'analytic_ODE_solution':True,'energy_conservation':True,
                      'pressure_identity':True},
              verdict='Ordinary core-envelope heat flow does not select the required core density; pure Newtonian Lambda gravity cannot select a universal surface density.')
(HERE/'run'/'result.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
