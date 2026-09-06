"""Physical KG initial-jet response on a solved static metric background.

Retains the global trace degree: c=delta(bar pi)''' is solved, not set to zero.
Results are numerical boundary-value evidence conditional on smooth coupled
perturbative solvability, not a complete nonlinear Dirac classification.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate import simpson
import sympy as s

from metric_static_background import derive, solve_background, curved_matter_jets


@lru_cache(maxsize=1)
def operators():
    d=derive()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    w,wp,wpp,v,vp,vpp=s.symbols('w wp wpp v vp vpp')
    qs=[N,A,B,Nd,Ad,Bd,Ndd,Add,Bdd]
    variations=[N*v,A*w,B*w,Nd*v+N*vp,Ad*w+A*wp,Bd*w+B*wp,
                Ndd*v+2*Nd*vp+N*vpp,Add*w+2*Ad*wp+A*wpp,
                Bdd*w+2*Bd*wp+B*wpp]
    eq=[d['EL'][0]/(A**2*B),(A*d['EL'][1]+B*d['EL'][2])/(N*A**2*B)]
    gauge={B:1,Bd:0,Bdd:0,Nd:N*u,Ad:A*b,Ndd:N*(up+u**2),Add:A*(bp+b**2)}
    linear=[s.factor(sum(s.diff(e,q)*dq for q,dq in zip(qs,variations))
                     .subs(gauge,simultaneous=True)) for e in eq]
    coeff=s.Matrix([[s.factor(s.diff(e,q)) for q in [w,wp,wpp,v,vp,vpp]] for e in linear])
    # Compute the changed time derivatives of the connection at t=0.
    # Initial metric and all its first derivatives agree, so connection-product
    # differences vanish. Spatial derivatives of initial differences vanish too.
    metric=s.diag(-N**2,A**2,A**2,B**2); inv=metric.inv()
    gddot=s.diag(-2*N**2*v,2*w*A**2,2*w*A**2,2*w*B**2)
    def dtGamma(alpha,beta,gamma):
        return sum(inv[alpha,j]*((gddot[j,gamma] if beta==0 else 0)
            +(gddot[j,beta] if gamma==0 else 0)
            -(gddot[beta,gamma] if j==0 else 0))/2 for j in range(4))
    Ruu=s.simplify((dtGamma(0,0,0)-sum(dtGamma(j,0,j) for j in range(4)))/N**2)
    # GR lapse equation R3-2Lambda has no lapse variation, independent of F.
    GRlapse=d['R3']-2*Lam
    GRlinear=s.simplify(sum(s.diff(GRlapse,q)*dq for q,dq in zip(qs,variations)))
    GRv=s.simplify(GRlinear.diff(v))
    GRrindler=s.simplify(GRlinear.subs({A:1,B:1,Ad:0,Add:0,Bd:0,Bdd:0,Lam:0}))
    return d,coeff,dict(Ricci_initial_jet_identity_residual=str(s.simplify(Ruu+3*w/N**2)),
        GR_lapse_response_to_v=str(GRv),GR_Rindler_lapse_equation=str(GRrindler),
        linearized_lapse_and_trace=[str(e) for e in linear],
        coefficient_matrix=str(coeff))


def response(y_initial,ratio,span):
    d,coeff,_=operators()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    background=solve_background(y_initial,ratio,span)
    matter=curved_matter_jets()
    if not matter['initial_stress_and_first_derivative_equal'] or any(
            s.sympify(matter['stress_time_coefficients'][0][j])!=0 for j in [0,1,2]):
        raise ValueError('The chosen matter pair no longer satisfies the required density jets')
    stress_acceleration=float(s.sympify(matter['proper_time_stress_acceleration_coefficient']))
    rhs=s.lambdify((u,b),d['rhs'].subs({a0:1,Lam:ratio}),'numpy')
    def bgflow(z,Y):
        return [Y[2],Y[3],*np.asarray(rhs(*Y[2:]),float).reshape(2)]
    pieces=[solve_ivp(bgflow,(0,sign*span),background['seed'],method='DOP853',
                      rtol=2e-13,atol=2e-14,dense_output=True,max_step=span/16)
            for sign in [-1,1]]
    if not all(p.success for p in pieces):
        raise RuntimeError('Background integration failed')
    cf=s.lambdify((N,A,u,b,up,bp),coeff.subs({a0:1,Lam:ratio}),'numpy')
    eta=np.exp(-y_initial)  # scale w=eta W to avoid small-kernel cancellation
    def values(z):
        nn,aa,uu,bb=pieces[0 if z<0 else 1].sol(z)
        upp,bpp=np.asarray(rhs(uu,bb),float).reshape(2)
        nn,aa=np.exp(nn),np.exp(aa)
        C=np.asarray(cf(nn,aa,uu,bb,upp,bpp),float)
        C[:,:3]*=eta; C[0,:]/=eta
        return nn,aa,C
    def source(z):
        x=z/(.35*span)
        return np.exp(1-1/(1-x*x)) if abs(x)<1 else 0.
    def flow(z,Y,c,forcing):
        nn,aa,C=values(z)
        W,Wp,V,Vp,_=Y
        source_vector=np.array([0.,-stress_acceleration*nn**2*source(z)*forcing+2*c/nn])
        highest=C[:,[2,5]]
        low=C[:,[0,1,3,4]]@np.array([W,Wp,V,Vp])
        Wpp,Vpp=np.linalg.solve(highest,source_vector-low)
        return np.array([Wp,Wpp,Vp,Vpp,aa**2*W])
    grid=np.linspace(-span,span,1001)
    def solve(method,rtol,atol,step):
        solutions=[]
        for initial,c,forcing in [([0,0,0,0,0],0.,1.),
            ([0,1/span,0,0,0],0.,0.),([0,0,0,1/span,0],0.,0.),
            ([0,0,0,0,0],1/span**2,0.)]:
            sol=solve_ivp(lambda z,Y:flow(z,Y,c,forcing),(-span,span),initial,
                method=method,rtol=rtol,atol=atol,max_step=step,dense_output=True)
            if not sol.success:
                raise RuntimeError('Response fundamental integration failed')
            solutions.append(sol)
        def boundary(Y):
            return np.array([Y[0],Y[2],Y[4]/span])
        matrix=np.column_stack([boundary(sol.y[:,-1]) for sol in solutions[1:]])
        forcing=boundary(solutions[0].y[:,-1])
        weights=np.linalg.solve(matrix,-forcing)
        out=solutions[0].sol(grid)+sum(weight*sol.sol(grid)
                                      for weight,sol in zip(weights,solutions[1:]))
        return out,weights[2]/span**2,matrix,solutions,weights
    coarse=solve('RK45',1e-8,1e-11,span/32)
    fine=solve('DOP853',1e-11,1e-14,span/64)
    Y,c,matrix,solutions,weights=fine
    nn=np.array([values(z)[0] for z in grid]); aa=np.array([values(z)[1] for z in grid])
    curvature=-3*eta*Y[0]/nn**2
    curvature_coarse=-3*eta*coarse[0][0]/nn**2
    peak=np.max(abs(curvature))
    outside=abs(grid)>.5*span
    # Check ODE independently against derivatives of the integrated dense output
    # using a centered finite difference on a finer test interval.
    residual=[]
    def dense(z):
        return solutions[0].sol(z)+sum(wt*sol.sol(z) for wt,sol in zip(weights,solutions[1:]))
    dz=span*1e-5
    for z in np.linspace(-.99*span,.99*span,101):
        derivative=(dense(z+dz)-dense(z-dz))/(2*dz)
        predicted=flow(z,dense(z),c,1.)
        residual.append(np.max(abs(derivative-predicted)/(1+abs(predicted))))
    singular=np.linalg.svd(matrix,compute_uv=False)
    return dict(label=background['label'],success=True,span=[-span,span],
        physical_source='Half difference of positive-energy KG states; overall epsilon^2 suppressed',
        w_scaling=eta,global_c=float(c),boundary_matching_matrix=matrix.tolist(),
        computed_boundary_matrix_rank=int(np.linalg.matrix_rank(matrix)),
        boundary_matrix_singular_values=singular.tolist(),
        boundary_matrix_condition_number=float(singular[0]/singular[-1]),
        maximum_boundary_residual=float(max(abs(Y[[0,2,4],0]).max(),abs(Y[[0,2,4],-1]).max())),
        relative_mean_w_residual=float(abs(simpson(aa**2*Y[0],x=grid))/
                                      (span*np.max(abs(Y[0])))),
        maximum_ODE_residual=float(max(residual)),
        peak_curvature=float(peak),outside_peak_curvature=float(np.max(abs(curvature[outside]))),
        outside_to_peak_curvature_ratio=float(np.max(abs(curvature[outside]))/peak),
        relative_refinement_difference=float(np.max(abs(curvature-curvature_coarse))/peak),
        source_and_initial_matter_difference_zero_at_probe=source(.7*span)==0,
        source_support=[-.35*span,.35*span],
        sampled_z=grid[::50].tolist(),sampled_curvature=curvature[::50].tolist(),
        methods=['RK45','DOP853'],rtols=[1e-8,1e-11],atols=[1e-11,1e-14])


def audit():
    start=time.monotonic(); _,_,symbolic=operators()
    matter=curved_matter_jets()
    rows=[response(.5,0.,.02),response(10.5,float(32*s.pi),.002)]
    checks=dict(Ricci_identity=symbolic['Ricci_initial_jet_identity_residual']=='0',
        GR_lapse_control=symbolic['GR_lapse_response_to_v']=='0',
        covariant_physical_source=matter['covariant_Ward_residuals_zero'],
        boundary_and_mean_constraints=all(r['maximum_boundary_residual']<1e-9 and
            r['relative_mean_w_residual']<1e-6 for r in rows),
        numerical_ODE_and_refinement=all(r['maximum_ODE_residual']<1e-5 and
            r['relative_refinement_difference']<1e-4 for r in rows))
    return dict(**symbolic,checks=checks,responses=rows,runtime_seconds=time.monotonic()-start,
        verdict='Numerical physical initial-jet response, including global mode; '
            'interpret only with explicit smooth coupled-solvability and boundary assumptions.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    p.add_argument('--require-local-initial-curvature',action='store_true')
    args=p.parse_args(); result=audit()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    for k,v in result['checks'].items():
        print('[%s] %s'%('ok' if v else 'FAIL',k))
    for row in result['responses']:
        print(row['label'],'outside/peak',row['outside_to_peak_curvature_ratio'],
              'relative refinement',row['relative_refinement_difference'],
              'global c',row['global_c'])
    if not all(result['checks'].values()):
        return 1
    if args.require_local_initial_curvature and any(
            r['outside_to_peak_curvature_ratio']>100*r['relative_refinement_difference']
            for r in result['responses']):
        print('FAIL: nonzero physical initial curvature outside the matter difference support')
        return 2
    return 0


if __name__=='__main__':
    raise SystemExit(main())
