"""Vary and solve a local static background of metric_constraint's Hamiltonian.

No background equation, determinant, or causal verdict is prescribed. Keep the
radial metric B until all variations are taken. The branch N'>0 is explicit;
reflection covers N'<0. This is a local vacuum construction, not a global
cosmology, nonlinear Dirac certificate, or physical source experiment.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s


@lru_cache(maxsize=1)
def derive():
    N, A, B, a0, Nd = s.symbols('N A B a0 Nd', positive=True)
    Ad, Bd, Ndd, Add, Bdd, Lam = s.symbols('Ad Bd Ndd Add Bdd Lambda', real=True)
    qs = [N, A, B]; ds = [Nd, Ad, Bd]; dds = [Ndd, Add, Bdd]

    def dz(expr):
        return sum(s.diff(expr, q)*d+s.diff(expr, d)*dd
                   for q, d, dd in zip(qs, ds, dds))

    # Compute three-curvature independently from its connection (z=index 2).
    metric = s.diag(A**2, A**2, B**2); inv = metric.inv()
    def partial(expr, i):
        return dz(expr) if i == 2 else s.S.Zero
    Gamma = [[[sum(inv[i,l]*(partial(metric[l,k],j)+partial(metric[l,j],k)
                   -partial(metric[j,k],l))/2 for l in range(3))
               for k in range(3)] for j in range(3)] for i in range(3)]
    Ricci = s.Matrix(3, 3, lambda i,j: s.expand(sum(
        partial(Gamma[k][i][j],k)-partial(Gamma[k][i][k],j)
        +sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k]
             for l in range(3)) for k in range(3))))
    R3 = s.factor(s.trace(inv*Ricci))
    LEH = (2*N*Ad**2+4*A*Ad*Nd)/B
    boundary = -4*N*A*Ad/B
    ibp = s.factor(N*B*A**2*R3-LEH-dz(boundary))
    delta_Ad,delta_B=s.symbols('delta_Ad delta_B')
    raw=N*B*A**2*R3
    boundary_res=s.factor(s.diff(raw,Add)*delta_Ad+s.diff(raw,Bd)*delta_B
                         -s.diff(boundary,Ad)*delta_Ad-s.diff(boundary,B)*delta_B)
    y = Nd/(N*B*a0)
    F = 2*(1-(1+y)*s.exp(-y))
    L = LEH-2*Lam*N*B*A**2+2*N*B*A**2*a0**2*F
    EL = [s.factor(s.diff(L,q)-dz(s.diff(L,d))) for q,d in zip(qs,ds)]
    noether = s.factor(Nd*EL[0]+Ad*EL[1]-B*dz(EL[2]))

    # Only now fix proper radial distance and use logarithmic derivatives.
    u, b, up, bp = s.symbols('u b up bp', real=True)
    gauge = {B:1, Bd:0, Bdd:0, Nd:N*u, Ad:A*b,
             Ndd:N*(up+u**2), Add:A*(bp+b**2)}
    norm = [2*A**2, 4*N*A, -2*N*A**2]
    eq = [s.factor(e.subs(gauge, simultaneous=True)/v) for e,v in zip(EL,norm)]
    matrix, forcing = s.linear_eq_to_matrix(eq[:2],[up,bp])
    rhs = matrix.inv()*forcing
    rhs = rhs.applyfunc(s.factor)
    C = eq[2]
    propagate = s.factor(s.diff(C,u)*rhs[0]+s.diff(C,b)*rhs[1]+(u+2*b)*C)
    hessian = s.hessian(L,[Nd,Ad])
    det = s.factor(hessian.det())
    mul = 1+(y-1)*s.exp(-y)
    det_res = s.factor(det+16*A**2*mul/B**2)
    LGR = LEH-2*Lam*N*B*A**2
    ELGR = [s.factor(s.diff(LGR,q)-dz(s.diff(LGR,d))) for q,d in zip(qs,ds)]
    rindler = {A:1,B:1,Ad:0,Bd:0,Ndd:0,Add:0,Bdd:0,Lam:0}
    return dict(symbols=(N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp),
                L=L,R3=R3,EL=EL,eq=eq,rhs=rhs,C=C,matrix=matrix,
                hessian=hessian,det=det,ibp=ibp,noether=noether,boundary_res=boundary_res,
                propagate=propagate,det_res=det_res,
                rindler=[s.factor(e.subs(rindler)) for e in ELGR])


def solve_background(y_initial, lambda_over_a0_squared, span=.02):
    """Dimensionless a0=1; z here means a0*z_physical with c=1."""
    if y_initial <= 0:
        raise ValueError('Positive-field patch required; zero field is degenerate')
    d = derive()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp = d['symbols']
    # Obtain roots from the VARIED B equation, not a prescribed background.
    roots = s.solve(d['C'], b)
    initial_roots = [complex(v.subs({u:y_initial,a0:1,Lam:lambda_over_a0_squared}))
                     for v in roots]
    real_roots = [v.real for v in initial_roots if abs(v.imag) < 1e-12]
    if not real_roots:
        raise ValueError('Radial constraint has no real seed on this branch')
    b_initial = max(real_roots)
    subs = {a0:1,Lam:lambda_over_a0_squared}
    ode = s.lambdify((u,b),d['rhs'].subs(subs),'numpy')
    eqfn = s.lambdify((u,b,up,bp),s.Matrix(d['eq']).subs(subs),'numpy')
    def flow(z,state):
        uu,bb = state[2:]
        uu_p,bb_p = np.asarray(ode(uu,bb),dtype=float).reshape(2)
        return [uu,bb,uu_p,bb_p]
    initial = [0.,0.,y_initial,b_initial]  # log N, log A, u, b
    grid = np.linspace(-span,span,81)
    def integrate(rtol,atol,method,max_step):
        pieces = [solve_ivp(flow,(0,sgn*span),initial,method=method,max_step=max_step,
                            rtol=rtol,atol=atol,dense_output=True) for sgn in [-1,1]]
        if not all(p.success for p in pieces):
            raise RuntimeError('Static integration failed: '+str([p.message for p in pieces]))
        values = np.column_stack([pieces[0 if z<0 else 1].sol(z) for z in grid])
        return values
    coarse = integrate(1e-8,1e-10,'RK45',span/4)
    fine = integrate(1e-11,1e-13,'DOP853',span/8)
    residuals=[]; constraints=[]
    for state in fine.T:
        uu,bb=state[2:]
        upp,bpp=np.asarray(ode(uu,bb),dtype=float).reshape(2)
        ee=np.asarray(eqfn(uu,bb,upp,bpp),dtype=float).reshape(3)
        scale=1+abs(lambda_over_a0_squared)+uu**2+bb**2+abs(upp)+abs(bpp)
        residuals.append(max(abs(ee))/scale)
        constraints.append(abs(ee[2]))
    # Reconstruct the exact principal coefficient from the prior full solve.
    # These are numerical evaluations, not causal pass thresholds.
    return dict(label='y0=%g,Lambda/a0^2=%g'%(y_initial,lambda_over_a0_squared),
        y_initial=y_initial,lambda_over_a0_squared=lambda_over_a0_squared,
        integration_success=True,span=[-span,span],grid_points=len(grid),
        methods=['RK45','DOP853'],rtols=[1e-8,1e-11],atols=[1e-10,1e-13],
        maximum_steps=[span/4,span/8],
        b_initial=b_initial,minimum_y=float(np.min(np.abs(fine[2]))),
        maximum_y=float(np.max(np.abs(fine[2]))),
        minimum_N=float(np.min(np.exp(fine[0]))),minimum_A=float(np.min(np.exp(fine[1]))),
        max_scaled_EL_residual=float(max(residuals)),max_constraint_drift=float(max(constraints)),
        refinement_relative_difference=float(np.max(abs(fine-coarse)/(1+abs(fine)))),
        transverse_C4_at_unit_k=float(-9/(4*np.expm1(y_initial))),
        seed=[float(v) for v in initial],end_states=fine[:,[0,-1]].tolist())


def compact_static_obstruction(d):
    """General spatial conformal variation, plus an independent plane check."""
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    eps,sigma,lap_sigma,R,z,lapN_over_N,divFa=s.symbols(
        'eps sigma lap_sigma R z lapN_over_N divFa',real=True)
    f=s.Function('F')
    # h -> exp(2 eps sigma) h: at first order sqrt(h)->exp(3eps sigma),
    # R->exp(-2eps sigma)(R-4eps Delta sigma), z->exp(-2eps sigma)z.
    density=s.exp(3*eps*sigma)*(s.exp(-2*eps*sigma)*(R-4*eps*lap_sigma)
                -2*Lam+2*a0**2*f(z*s.exp(-2*eps*sigma)))
    first=s.expand(s.diff(density,eps).subs(eps,0).doit())
    trace=first.coeff(sigma)+first.coeff(lap_sigma)*lapN_over_N
    # N -> N exp(eps eta): delta a_i=eps D_i eta. Integration by parts
    # of 4 N F_z a^i D_i eta gives -4N[div(F_z a)+F_z a^2] eta.
    lapse=R-2*Lam+2*a0**2*f(z)-4*divFa-4*a0**2*z*s.diff(f(z),z)
    divergence=lapN_over_N-divFa-a0**2*z*s.diff(f(z),z)
    target=divergence-(a0**2*(f(z)-z*s.diff(f(z),z))-Lam)
    full_res=s.simplify(target+(trace-lapse)/4)
    y=s.symbols('y',nonnegative=True)
    fy=2*(1-(1+y)*s.exp(-y))
    remainder=s.factor(2-(fy-y*s.diff(fy,y)/2))
    # On the derived plane system div(mu grad N)/N has this expression.
    yy=u/a0; mt=1-s.exp(-yy); ml=1+(yy-1)*s.exp(-yy)
    plane_target=ml*up+mt*(u**2+2*b*u)-a0**2*(
        fy.subs(y,yy)-yy**2*s.exp(-yy))+Lam
    plane_res=s.factor(plane_target-(-d['eq'][1]+d['eq'][0]/2+d['eq'][2]/2))
    return dict(full_trace_identity_residual=str(full_res),
        conformal_variation_trace=str(trace),lapse_variation=str(lapse),
        plane_identity_residual=str(plane_res),kernel_bound_remainder=str(remainder),
        framework_ratio_excluded=bool(32*s.pi>2),
        hypotheses=['Smooth globally static vacuum','Positive lapse everywhere',
                    'Compact boundaryless spatial leaf','Lambda >= 2 a0^2'],
        conclusion='No such global static vacuum; not an obstruction to expanding FLRW '
                   'or a local static patch with boundaries.')


def curved_matter_jets():
    """KG stress on arbitrary static plane geometry; no flat-space substitution.

    Return half the stress difference for the two states, before the common
    epsilon^2 amplitude factor. Jets are coefficients of coordinate time t.
    """
    z=s.symbols('z',real=True)
    N=s.Function('N')(z); A=s.Function('A')(z); sigma=s.Function('sigma')(z)
    u=s.diff(N,z)/N; b=s.diff(A,z)/A
    # T00, T0z, Tzz, Txx contravariant coordinate components.
    jets=[[s.S.Zero]*4 for _ in range(4)]
    for mass,r,w in [(1,s.S.One,1),(2,s.Rational(1,2),-2),(3,s.Rational(1,3),1)]:
        def wave(v):
            return N**2*(s.diff(v,z,2)+(u+2*b)*s.diff(v,z)-mass**2*v)
        bg=[r,N]; perturb=[s.S.Zero,N*w*sigma]
        for j in range(3):
            bg.append(wave(bg[j])/((j+1)*(j+2)))
            perturb.append(wave(perturb[j])/((j+1)*(j+2)))
        bt=[(j+1)*bg[j+1] for j in range(4)]
        dt=[(j+1)*perturb[j+1] for j in range(4)]
        bz=[s.diff(v,z) for v in bg]; dz=[s.diff(v,z) for v in perturb]
        def conv(v,w,j):
            return sum(v[k]*w[j-k] for k in range(j+1))
        for j in range(4):
            kinetic=conv(bt,dt,j)/N**2
            gradient=conv(bz,dz,j)
            potential=mass**2*conv(bg,perturb,j)
            jets[0][j]+=(kinetic+gradient+potential)/N**2
            jets[1][j]-=(conv(bt,dz,j)+conv(dt,bz,j))/N**2
            jets[2][j]+=kinetic+gradient-potential
            jets[3][j]+=(kinetic-gradient-potential)/A**2
    jets=[[s.simplify(v) for v in row] for row in jets]
    # Direct covariant divergence, including static-metric connection terms.
    ward=[]
    for j in range(3):
        ward.append(s.simplify((j+1)*jets[0][j+1]+s.diff(jets[1][j],z)
                              +(3*u+2*b)*jets[1][j]))
        ward.append(s.simplify((j+1)*jets[1][j+1]+s.diff(jets[2][j],z)
                    +(u+2*b)*jets[2][j]+N*s.diff(N,z)*jets[0][j]
                    -2*A*s.diff(A,z)*jets[3][j]))
    acceleration=s.simplify(2*(jets[2][2]+2*A**2*jets[3][2])/(N**2*sigma))
    amplitude,profile=s.symbols('epsilon profile',real=True)
    energies=[s.expand(amplitude**2*sum(((1+sign*w*profile)**2+mass**2*r**2)/2
                for mass,r,w in [(1,s.S.One,1),(2,s.Rational(1,2),-2),
                                  (3,s.Rational(1,3),1)])) for sign in [-1,1]]
    return dict(initial_stress_and_first_derivative_equal=all(
                    row[j]==0 for row in jets for j in [0,1]),
        proper_time_stress_acceleration_coefficient=str(acceleration),
        covariant_Ward_residuals_zero=all(v==0 for v in ward),
        Ward_residuals=[str(v) for v in ward],
        Ward_checked_through_time_degree=2,
        contravariant_stress_component_order=['00','0z','zz','xx=yy'],
        stress_time_coefficients=[[str(v) for v in row] for row in jets],
        initial_energy_each=str(energies[0]),initial_energy_difference=str(
            s.simplify(energies[1]-energies[0])),
        caveat='Test-matter order epsilon^2 on exact vacuum geometry; not yet a solved '
               'coupled gravitational response to these two physical states.')


def audit():
    start=time.monotonic(); d=derive()
    N,A,B,a0,Nd,Ad,Bd,Ndd,Add,Bdd,Lam,u,b,up,bp=d['symbols']
    # Re-run, don't trust a previous result JSON. Compare the old derived
    # symbol to the independent derivative of this exact action's kernel.
    import metric_causal_symbol
    prior=metric_causal_symbol.derive()
    yy,kk=s.symbols('y kx',positive=True)
    ky,kz=s.symbols('ky kz',real=True)
    old=s.sympify(prior['exponential_time_jet_multiplier'],
                  locals={'y':yy,'kx':kk,'ky':ky,'kz':kz}).subs({ky:0,kz:0})
    kernel_susceptibility=s.diff(d['L']-(2*N*Ad**2+4*A*Ad*Nd)/B+2*Lam*N*B*A**2,
                                 Nd,2)  # radial coefficient; transverse uses F_y/(2y)
    f=2*(1-(1+yy)*s.exp(-yy))
    transverse=s.diff(f,yy)/(2*yy)
    new=-s.Rational(9,4)*transverse/((1-transverse)*kk**2)
    cross=s.simplify(old-new)==0
    backgrounds=[solve_background(1.,0.),solve_background(20.,float(32*s.pi),span=.002)]
    compact=compact_static_obstruction(d)
    matter=curved_matter_jets()
    checks={
        'EH_boundary_identity':d['ibp']==0,
        'Dirichlet_boundary_variation':d['boundary_res']==0,
        'radial_Noether_identity':d['noether']==0,
        'constraint_propagation':d['propagate']==0,
        'computed_Hessian_determinant':d['det_res']==0,
        'GR_Rindler_control':all(v==0 for v in d['rindler']),
        'same_action_principal_crosscheck':cross,
        'full_static_divergence_identity':compact['full_trace_identity_residual']=='0'
                and compact['plane_identity_residual']=='0',
        'curved_matter_covariant_Ward_identity':matter['covariant_Ward_residuals_zero'],
        'curved_matter_equal_initial_stress':matter['initial_stress_and_first_derivative_equal'],
        'all_background_equations_and_refinement':all(
            v['max_scaled_EL_residual']<1e-8 and v['max_constraint_drift']<1e-8
            and v['refinement_relative_difference']<1e-7 for v in backgrounds),
        'nonzero_field_regular_patches':all(v['minimum_y']>0 and v['minimum_N']>0
                                         and v['minimum_A']>0 for v in backgrounds)}
    return dict(checks=checks,static_action_density=str(d['L']),R3=str(d['R3']),
        Euler_Lagrange_equations=[str(e) for e in d['EL']],
        gauge_fixed_normalized_equations=[str(e) for e in d['eq']],
        reduced_ODE_matrix=str(d['matrix']),reduced_ODE_rhs=[str(e) for e in d['rhs']],
        radial_constraint=str(d['C']),radial_Noether_identity_residual=str(d['noether']),
        constraint_propagation_residual=str(d['propagate']),
        EH_integration_by_parts_residual=str(d['ibp']),
        Dirichlet_boundary_variation_residual=str(d['boundary_res']),
        highest_derivative_Hessian=str(d['hessian']),computed_determinant=str(d['det']),
        determinant_identity_residual=str(d['det_res']),
        zero_field_determinant=str(s.simplify(d['det'].subs(Nd,0))),
        unit_field_determinant=str(s.simplify(d['det'].subs(Nd,N*B*a0))),
        GR_Rindler_residuals=[str(e) for e in d['rindler']],
        radial_auxiliary_Hessian=str(kernel_susceptibility),
        principal_crosscheck=cross,backgrounds=backgrounds,
        compact_static_obstruction=compact,
        curved_matter_jets=matter,
        verdict='Local nonlinear vacuum backgrounds exist; principal causal obstruction remains. '
                'Full coupled source experiment and regular inverse limit still OPEN.',
        non_claims=['Global compact-leaf completion','Finite-propagation theorem for the full coupled model',
                    'Full nonlinear Dirac closure','Novelty','Empirical validation'],
        environment={'python':platform.python_version(),'sympy':s.__version__,
                     'numpy':np.__version__,'scipy':scipy.__version__},
        runtime_seconds=time.monotonic()-start)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    p.add_argument('--require-causal-principal-response',action='store_true')
    args=p.parse_args(); r=audit()
    if args.output:
        args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    for i,(name,passed) in enumerate(r['checks'].items(),1):
        print('[%s] %02d %s'%('ok' if passed else 'FAIL',i,name))
    for row in r['backgrounds']:
        print(row['label'], 'constraint drift',row['max_constraint_drift'],
              'C4(k_perp=1)',row['transverse_C4_at_unit_k'])
    print(r['verdict'])
    if not all(r['checks'].values()):
        return 1
    if args.require_causal_principal_response and any(
            v['transverse_C4_at_unit_k']!=0 for v in r['backgrounds']):
        print('FAIL causal principal-response gate (not an unconditional nonlinear no-go)')
        return 2
    return 0


if __name__=='__main__':
    raise SystemExit(main())
