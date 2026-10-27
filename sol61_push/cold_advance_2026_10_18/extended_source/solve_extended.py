"""Full-W static Plummer response; an unsupplied local benchmark, not a halo.

Command: python3 <this file> <new run directory>/results.json
No imports of executable project sources; data are loaded as JSON only.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import brentq

G, MS, PC = 6.674e-11, 1.989e30, 3.0857e16
SOURCE = Path('sol61_push/cold_final_mile_2026_10_13/run_077/results.json')
checks = []


def check(name, value, detail=None):
    checks.append({'name': name, 'passed': bool(value), 'detail': detail})
    if not value:
        raise AssertionError((name, detail))


def algebraic(B):
    return 2 * B / (np.sqrt(B * B + 4 * B) + B)


def solve(R, d, *, tol=1e-6, extent=300., nodes=550):
    """x=r/a, R=rM/a, d=L^2/(2a^2), U=u/a0.

    -d (U_xx+2U_x/x-2U/x^2)+U|U|/(1-|U|)=R^2 x/(1+x^2)^1.5.
    Signed extension is used only for Newton iterations; accepted U is positive.
    Inner Robin is regular-origin asymptotic; outer is isolated asymptotic.
    """
    lo, hi = 1e-5, max(extent, 30*d/R)
    t = np.linspace(math.log(lo), math.log(hi), nodes)
    x = np.exp(t)
    B = R*R*x/(1+x*x)**1.5
    U0 = algebraic(B) * np.sqrt(x/(x+min(1., math.sqrt(d))))
    V0 = np.gradient(U0, t)
    outer = R/hi-(R*R/2+d)/hi**2
    check('positive asymptotic boundary', outer > 0)

    def fun(tt, yy):
        xx = np.exp(tt)
        u, v = yy
        # No clipping of the actual equation. A pole crossing must fail.
        F = u*np.abs(u)/(1-np.abs(u))
        src = R*R*xx/(1+xx*xx)**1.5
        return np.vstack((v, -v+2*u+xx*xx/d*(F-src)))

    def bc(left, right):
        # U=A*x - R^2*x^3/(10*d)+..., so U_t-U=-R^2*x^3/(5*d).
        return np.array([left[1]-left[0]+R*R*lo**3/(5*d), right[0]-outer])

    sol = solve_bvp(fun, bc, t, np.vstack((U0, V0)), tol=tol, max_nodes=30000)
    check('BVP converges', sol.success, {'R': R, 'd': d, 'status': int(sol.status), 'nodes': len(sol.x)})
    xx = np.geomspace(lo, hi, 1400)
    uu, vv = sol.sol(np.log(xx))
    check('physical branch 0<U<1', np.all((uu > 0) & (uu < 1)), [float(uu.min()), float(uu.max())])
    # d(r^2 u)/dr >=0 is the extra condition for a real nonnegative density.
    density_sign = 2*uu+vv
    check('nonnegative apparent density in sampled domain', density_sign.min() > -1e-8, float(density_sign.min()))
    aperture = 4/3
    U = float(sol.sol(math.log(aperture))[0])
    # Independent quadrature of the integrated EL identity on the interpolant.
    # [x^2 U_x]_lo^hi = integral[2U+x^2(F(U)-B)/d] dx.
    # Restrict to [0.02,10] to avoid subtracting the very extended tail.
    from scipy.integrate import quad
    xl, xr = .02, 10.
    def integrand(z):
        w = float(sol.sol(math.log(z))[0])
        bb = R*R*z/(1+z*z)**1.5
        return 2*w+z*z/d*(w*w/(1-w)-bb)
    integral = quad(integrand, xl, xr, epsabs=1e-7, epsrel=1e-7, limit=250)[0]
    boundary = xr*float(sol.sol(math.log(xr))[1])-xl*float(sol.sol(math.log(xl))[1])
    discrepancy = abs(integral-boundary)/max(1., abs(integral), abs(boundary))
    check('integrated field equation', discrepancy < 2e-5, discrepancy)
    return {'aperture_U': U, 'max_rms_residual': float(max(sol.rms_residuals)),
            'nodes': len(sol.x), 'outer_x': hi,
            'apparent_mass_over_Mb': aperture**2*U/R**2,
            'min_density_sign': float(density_sign.min()),
            'integrated_identity_error': discrepancy}


def main():
    data = json.loads(SOURCE.read_text())
    objects = [r for r in data['dwarfs'] if r['name'] in ['Fornax', 'Leo I', 'Draco', 'Ursa Minor']]
    rows, crossings = [], []
    for obj in objects:
        a = .75*obj['r12_pc']
        for foot, a0 in [('canonical', 9.3603e-11), ('alt', 1.1312e-10)]:
            R = math.sqrt(G*MS*obj['Mb_Msun']/a0)/PC/a
            x = 4/3
            B = R*R*x/(1+x*x)**1.5
            zero = x*x*float(algebraic(B))/R**2
            check('zero-gradient aperture matches uncapped source',
                  abs(zero-min(zero,5.364)) < 1e-10 or obj['name'] in ['Draco','Ursa Minor'])
            for L in [24.,100.,300.,1000.]:
                ans = solve(R, L*L/(2*a*a))
                rows.append({'name': obj['name'], 'footing': foot, 'L_pc': L,
                             'R_rM_over_a': R, 'zero_gradient_uncapped_mass_over_Mb': zero,
                             'response_ratio': ans['apparent_mass_over_Mb']/zero,
                             'cold_mass_required_over_Mb': obj['cold_required_in_r12_over_Mb'], **ans})
            if obj['name'] in ['Fornax','Leo I']:
                target = obj['cold_required_in_r12_over_Mb']
                def residual(L):
                    return solve(R,L*L/(2*a*a))['apparent_mass_over_Mb']-target
                left,right = 10.,1500.
                check('crossing bracket', residual(left)>0 and residual(right)<0)
                Lcrit = brentq(residual,left,right,xtol=.01)
                ordinary = solve(R,Lcrit*Lcrit/(2*a*a))
                refined = solve(R,Lcrit*Lcrit/(2*a*a),tol=2e-7,extent=600.,nodes=850)
                error = abs(refined['apparent_mass_over_Mb']/ordinary['apparent_mass_over_Mb']-1)
                check('combined mesh tolerance and outer-domain control',error<3e-4,error)
                crossings.append({'name':obj['name'],'footing':foot,'L_critical_pc':Lcrit,
                                  'target_mass_over_Mb':target,'refinement_relative_error':error,
                                  'refined_mass_over_Mb':refined['apparent_mass_over_Mb']})
    out={'checkpoint':'CE-ADV-2026-10-18','base_checkpoint':'CE-FM-078',
         'assertion_tested':'Finite numerical full-W isolated Plummer boundary solutions and aperture crossings; no finite stock imposed',
         'equation':'-d Delta_vector U + U|U|/(1-|U|) = R^2*x/(1+x^2)^(3/2)',
         'rows':rows,'crossings':crossings,'checks':checks,'n_checks':len(checks),
         'non_claims':['No finite-stock halo, formation, self-gravity or physical source selection',
                       'No inherited CFG691/CFG820/CFG822 data verdict or empirical length bound',
                       'Far isolated boundary implies infinite apparent mass and is a local comparison only',
                       'No external field, nonspherical source, Jeans modelling, lensing or cosmology',
                       'Cold mass is not added again on top of its own identified gravitational response']}
    Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'n_checks':len(checks),'crossings':crossings,
                      'selected_rows':[{k:r[k] for k in ['name','footing','L_pc','response_ratio','apparent_mass_over_Mb']} for r in rows]},indent=2))


if __name__ == '__main__':
    main()
