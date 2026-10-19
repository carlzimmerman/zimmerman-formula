"""Exploratory full-GR single-X BVP, used only as an independent reference."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_bvp


def solve(central, radius=100.0, tol=1e-6, previous=None):
    # Source mass M=1, 4*pi*G=1; v=G*ADM_enclosed, N=1-2v/r.
    r = np.linspace(0, radius, 600)
    if previous is None:
        length = 1.5/math.sqrt(central)
        field = central*np.exp(-r*r/(2*length*length))
        deriv = -r/length**2*field
        mass = cumulative_trapezoid(2*r*r*field**2, r, initial=0)
        lapse = -mass[-1]/np.sqrt(r*r+length*length)
        y = np.array([field, deriv, mass, lapse])
        freq = 1-0.5*central
        par = [math.log(freq/(1-freq))]
    else:
        y = previous.sol(r)
        factor = central/y[0,0]
        y[0:2] *= factor
        y[2:4] *= factor*factor
        par = previous.p.copy()

    def frequency(p):
        return 1/(1+np.exp(-np.clip(p[0], -35, 35)))

    def equations(r, y, p):
        field, deriv, mass, lapse = y
        rr = np.where(r == 0, 1, r)
        invr = np.where(r == 0, 0, 1/rr)
        freq = frequency(p)
        N = 1-2*mass*invr
        al = np.exp(np.clip(lapse, -40, 40))
        kinetic_t = (freq/al)**2*field**2
        rho = kinetic_t+N*deriv**2+field**2
        pressure = kinetic_t+N*deriv**2-field**2
        md = r*r*rho
        ld = (mass*invr**2+r*pressure)/N
        nd_half_over_n = (-md*invr+mass*invr**2)/N
        fd2 = (1-(freq/al)**2)*field/N-(ld+nd_half_over_n)*deriv
        return np.array([deriv, fd2, md, ld])

    def boundary(a, b, p):
        freq = frequency(p)
        kappa = np.sqrt(1-freq**2)
        return np.array([a[0]-central, a[1], a[2], b[3],
                         b[1]+(kappa+1/radius)*b[0]])

    singular = np.zeros((4,4))
    singular[1,1] = -2
    solution = solve_bvp(equations, boundary, r, y, p=par, S=singular,
                         tol=tol, max_nodes=20000)
    freq = frequency(solution.p)
    grid = np.linspace(0, radius, 3000)
    profile = solution.sol(grid)
    mass = profile[2,-1]
    r99 = np.interp(.99*mass, profile[2], grid)
    row = {'central':central, 'radius':radius, 'tol':tol,
           'success':bool(solution.success), 'message':solution.message,
           'frequency':float(freq), 'v_total':float(mass), 'r99':float(r99),
           'C99':float(mass/r99), 'max_rms_residual':float(max(solution.rms_residuals)),
           'field_tail':float(profile[0,-1]),
           'field_min':float(profile[0].min()), 'nodes':len(solution.x)}
    return solution, grid, profile, row


if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
    solution = None
    rows=[]
    for central in [.01,.02,.04]:
        solution,grid,profile,row=solve(central, previous=solution)
        rows.append(row)
        print(json.dumps(row),flush=True)
        if not solution.success or row['field_min'] < -1e-7:
            break
        np.savez(out/f'pureX_{central:.3f}.npz',r=grid,h=profile[0],hp=profile[1],
                 mass_G=profile[2],logalpha=profile[3],omega_X=row['frequency'],
                 central=central,source_mass=1.,four_pi_G=1.)
    (out/'results.json').write_text(json.dumps({'rows':rows,'non_claim':'Reference only; no stability claim or mixed two-field solution.'},indent=2)+'\n')
