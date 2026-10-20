"""True-origin stationary BVP, no time evolution or stability claim.

Final solve tolerance is 1e-8. SciPy singular interface supplies -2 y'/r.
Inputs and all outputs are declared by the adjacent computation contract.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import sys
import time

import numpy as np
import scipy
from scipy.integrate import simpson, solve_bvp

ROOT = Path(__file__).resolve().parents[3]
PRIOR = ROOT / 'sol61_push/cold_completion_2026_10_20'
BASE = json.loads((PRIOR / 'run_001/results.json').read_text())
P = BASE['parameters']
M = P['M_chi']; a = P['a']; g = P['g']; MX2 = P['MX2']; lam = P['lambda']
TOL = 1e-8
L = 60.0
MAX_NODES = 24000
S = np.diag([0., -2., 0., -2., 0., -2., 0.])
checks = []
rows = []

def check(name, passed, value=None):
    record = {'name': name, 'pass': bool(passed)}
    if value is not None:
        record['value'] = float(value)
    checks.append(record)

def make_problem(Q):
    def fun(r, y, p):
        f, u, b, w, h, v, q = y
        om = p[0]
        return np.vstack([u, (1-om*om+2*lam*f*f+a*h+2*g*b)*f,
                          w, (MX2-4*om*om)*b+g*f*f,
                          v, M*M*h-3*M*h*h/8+h**3+a*f*f,
                          8*math.pi*om*r*r*(f*f+4*b*b)/Q])
    def jac(r, y, p):
        f, u, b, w, h, v, q = y
        om = p[0]
        J = np.zeros((7, 7, len(r)))
        J[0, 1] = 1.
        J[1, 0] = 1-om*om+6*lam*f*f+a*h+2*g*b
        J[1, 2] = 2*g*f
        J[1, 4] = a*f
        J[2, 3] = 1.
        J[3, 0] = 2*g*f
        J[3, 2] = MX2-4*om*om
        J[4, 5] = 1.
        J[5, 0] = 2*a*f
        J[5, 4] = M*M-3*M*h/4+3*h*h
        J[6, 0] = 16*math.pi*om*r*r*f/Q
        J[6, 2] = 64*math.pi*om*r*r*b/Q
        K = np.zeros((7, 1, len(r)))
        K[1, 0] = -2*om*f
        K[3, 0] = -8*om*b
        K[6, 0] = 8*math.pi*r*r*(f*f+4*b*b)/Q
        return J, K
    def bc(ya, yb, p):
        return np.array([ya[1], ya[3], ya[5], ya[6], yb[0], yb[2], yb[4], yb[6]-1])
    def bc_jac(ya, yb, p):
        A = np.zeros((8, 7)); B = np.zeros((8, 7))
        A[np.arange(4), [1,3,5,6]] = 1.
        B[np.arange(4,8), [0,2,4,6]] = 1.
        return A, B, np.zeros((8,1))
    return fun, jac, bc, bc_jac

def regular_benchmark():
    # u''+2u'/r=-6, u'(0)=0, u(1)=0 has u=1-r^2.
    def fun(r, y):
        return np.vstack([y[1], -6*np.ones_like(r)])
    def bc(ya, yb):
        return np.array([ya[1], yb[0]])
    x = np.linspace(0.,1.,21)
    yy = np.array([1-x*x, -2*x])
    sol = solve_bvp(fun, bc, x, yy, S=np.diag([0.,-2.]), tol=TOL, max_nodes=1000)
    err = float(np.max(np.abs(sol.sol(x)-yy)))
    check('singular-interface analytic regular-origin benchmark status', sol.status==0)
    check('singular-interface analytic regular-origin benchmark error <1e-10', err<1e-10, err)

def solve_profile(Q, out):
    start = time.monotonic()
    om = .94
    r = np.linspace(0., L, 1201)
    r0 = (3*Q/(8*math.pi*om*50.))**(1/3)
    z = np.exp((r-r0)/1.2)
    f = math.sqrt(50.)/(1+z)
    fp = -math.sqrt(50.)*z/(1.2*(1+z)**2)
    b = -g*f*f/(MX2-4*om*om)
    bp = -2*g*f*fp/(MX2-4*om*om)
    h = -.02*f*f
    hp = -.04*f*fp
    integrand = 8*math.pi*om*r*r*(f*f+4*b*b)/Q
    q = np.r_[0., np.cumsum((integrand[1:]+integrand[:-1])*.5*np.diff(r))]
    q /= q[-1]
    y = np.array([f,fp,b,bp,h,hp,q])
    y[[1,3,5],0] = 0.
    fun, jac, bc, bc_jac = make_problem(Q)
    sol = solve_bvp(fun, bc, r, y, p=[om], S=S, fun_jac=jac, bc_jac=bc_jac,
                    tol=TOL, bc_tol=1e-11, max_nodes=MAX_NODES)
    rr = np.linspace(0.,L,24001)
    yy = sol.sol(rr)
    f,fp,b,bp,h,hp,q = yy
    om = float(sol.p[0])
    wt = 4*math.pi*rr*rr
    U = .5*M*M*h*h-M*h**3/8+.25*h**4
    V = f*f+MX2*b*b+2*g*b*f*f+lam*f**4+a*h*f*f+U
    rot = float(simpson(wt*om*om*(f*f+4*b*b),x=rr))
    grad = float(simpson(wt*(fp*fp+bp*bp+.5*hp*hp),x=rr))
    pot = float(simpson(wt*V,x=rr))
    E = rot+grad+pot
    Qi = float(simpson(wt*2*om*(f*f+4*b*b),x=rr))
    virial = (grad+3*pot-3*rot)/E
    mask = rr>.8*L
    tail = float(simpson((wt*(om*om*(f*f+4*b*b)+fp*fp+bp*bp+.5*hp*hp+V))[mask],x=rr[mask]))/E
    origin_rhs = fun(np.array([0.]),sol.sol(np.array([0.])),sol.p)[:,0]
    origin_second = sol.sol(0.,1)[[1,3,5]]
    origin_error = float(np.max(np.abs(origin_second-origin_rhs[[1,3,5]]/3)))
    baseline = next(row for row in BASE['rows'] if row['Q']==Q and row['L']==L)
    error_E = abs(E/baseline['E']-1)
    error_om = abs(om/baseline['omega']-1)
    ires = int(np.argmax(sol.rms_residuals))
    row = {'Q_target':Q, 'L':L, 'tol':TOL, 'bc_tol':1e-11,
           'max_nodes':MAX_NODES, 'status':int(sol.status), 'message':sol.message,
           'nodes':len(sol.x), 'iterations':int(sol.niter), 'omega':om,
           'E':E, 'Q_integrated':Qi, 'E_over_Q':E/Qi,
           'gradient':grad,'rotation':rot,'potential':pot,
           'virial_relative':virial,'tail_energy_fraction_outer20percent':tail,
           'origin_second_derivative_identity_max_abs':origin_error,
           'origin_first_derivatives': [float(x) for x in yy[[1,3,5],0]],
           'origin_cumulative_charge':float(q[0]),
           'rms_residual_max':float(np.max(sol.rms_residuals)),
           'rms_residual_max_interval':[float(sol.x[ires]),float(sol.x[ires+1])],
           'baseline_energy_relative_difference':error_E,
           'baseline_omega_relative_difference':error_om,
           'f_min':float(f.min()),'f_max':float(f.max()),'b_min':float(b.min()),
           'chi_min':float(h.min()),'runtime_seconds':time.monotonic()-start}
    tag = f'Q{int(Q)}'
    check(tag+' final solver status zero', sol.status==0)
    check(tag+' rms residual <=1e-8', row['rms_residual_max']<=TOL, row['rms_residual_max'])
    check(tag+' all eight BC residuals <1e-10', np.max(np.abs(bc(yy[:,0],yy[:,-1],sol.p)))<1e-10)
    check(tag+' origin radial second-derivative identity <1e-9', origin_error<1e-9, origin_error)
    check(tag+' independently integrated charge relative error <1e-9', abs(Qi/Q-1)<1e-9, abs(Qi/Q-1))
    check(tag+' virial relative error <1e-8', abs(virial)<1e-8, abs(virial))
    check(tag+' tail energy fraction <1e-9', abs(tail)<1e-9, abs(tail))
    check(tag+' energy agrees prior finite-origin solution within1e-7', error_E<1e-7,error_E)
    check(tag+' omega agrees prior finite-origin solution within1e-7', error_om<1e-7,error_om)
    check(tag+' positive nodeless subthreshold branch', 0<om<1 and f.min()>-1e-8 and .85<E/Qi<1)
    np.savez_compressed(out/f'Q{int(Q)}.npz',r=rr,y=yy,f=f,fp=fp,b=b,bp=bp,h=h,hp=hp,q=q,
                        omega=om,Q=Q,E=E,mesh_x=sol.x,mesh_y=sol.y,ppoly_c=sol.sol.c,
                        metadata_json=json.dumps(row))
    rows.append(row)
    print(json.dumps(row),flush=True)

def main():
    out = Path(sys.argv[1])
    regular_benchmark()
    for Q in [80000.,160000.]:
        solve_profile(Q,out)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    check('measured peak RSS <1GB',rss<1_000_000_000,rss)
    result = {'scope':'True-origin finite numerical stationary profiles for a specified alternative matter action; no stability or formation conclusion.',
              'origin_convention':'r=0; y=fun+Sy/r; S derivative diagonal entries -2; radial second derivatives at origin equal regular force/3.',
              'parameters':P,'software':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},
              'source_common_action_sha256':hashlib.sha256((PRIOR/'common_action.py').read_bytes()).hexdigest(),
              'baseline_results_sha256':hashlib.sha256((PRIOR/'run_001/results.json').read_bytes()).hexdigest(),
              'rows':rows,'gap':2*rows[0]['E']-rows[1]['E'],
              'peak_rss_bytes_macos':rss,'checks':checks,'n_checks':len(checks),
              'all_checks_pass':all(x['pass'] for x in checks),
              'non_claims':['No ground-state proof','No spectral or nonlinear stability claim','No dynamics or merger rate','No dwarf mass or observational fit']}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    raise SystemExit(0 if result['all_checks_pass'] else 1)

if __name__=='__main__':
    main()
