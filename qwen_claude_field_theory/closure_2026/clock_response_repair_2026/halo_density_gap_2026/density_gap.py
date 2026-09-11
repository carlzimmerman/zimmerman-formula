#!/usr/bin/env python3
"""Derive the baryon-density contribution to the constrained radial lapse gap.

Full nonlinear metric/density on one zero-chi-gradient initial-slice family,
gamma=0. No time evolution, equilibrium halo, or dust-depletion assertion.
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
import mpmath as mp
from scipy.special import gammainc
import sympy as s

HERE=Path(__file__).resolve().parent


def budget(mu02,rho,radius,planck2,m):
    mu02,rho,radius,planck2,m=map(s.sympify,(mu02,rho,radius,planck2,m))
    if planck2.is_positive is not True or m.is_positive is not True:
        raise ValueError('positive squared Planck mass and m required')
    return s.factor((mu02+(1+m)*rho/(2*planck2*m))*radius**2)


def run():
    sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
    from equations import derive
    data=derive();z=data['symbols']
    q,H,r=s.symbols('q H r',positive=True)
    rho=z['rho'];M=z['M2'];metric=z['A'];Ar=z['Ar']
    initial={'R':r,'Rr':1,'Rrr':0,'k':H,'h':H,'Q':q,'kr':0,'hr':0,
             'Qr':0,'Qrr':0,'cr':0,'crr':0,'w':0,'gamma':0}
    sub={z[name]:value for name,value in initial.items() if name in z}
    sub[z['u']]=0;sub[z['ur']]=0
    ham=s.factor(data['constraints'][0].subs(sub))
    Ar_solution=s.solve(ham,Ar)[0]
    reduced={**sub,Ar:Ar_solution}
    results=[];checks=dict(inherited_action=all(data['checks'].values()))
    for eta in (0,1):
        subeta={**reduced,z['constraint_addition']:eta}
        matrix=data['matrix'].subs(subeta,simultaneous=True).applyfunc(s.factor)
        forcing=data['forcing'].subs(subeta,simultaneous=True).applyfunc(s.factor)
        # Ar_solution itself is already in the initial family.
        solved=(matrix.inv()*forcing).applyfunc(s.factor)
        for item in matrix*solved-forcing:
            assert s.factor(item)==0
        mu2=s.factor(solved[3,1]/metric**2)
        density_coefficient=s.factor(s.diff(mu2,rho))
        checks['affine_density_'+str(eta)]=s.diff(mu2,rho,2)==0
        results.append((mu2,density_coefficient,solved[3,0]))
    checks['constraint_addition_independent']=s.factor(results[0][0]-results[1][0])==0
    W,WY=z['W'],z['W_Y']
    expected=W/(2*M*(W-2*q*q*WY))
    checks['density_coefficient_bridge']=s.factor(results[0][1]-expected)==0
    m,A=s.symbols('m charge_A',positive=True)
    U=m*q*A;d=A*U/(2*q*(q*A+U))
    coefficient=s.factor(results[0][1].subs({W:U,WY:d},simultaneous=True))
    checks['stationary_density_coefficient']=s.factor(coefficient-(1+m)/(2*M*m))==0
    v=s.symbols('v',real=True)
    B=A*(m+2)/(q*m)
    qdot=-3*A*H*v/B-q*U/(2*M*H)
    # d(P_X(q²,t))/dt=P_Xt+2q*qdot*P_XX; A_dot=-3HA.
    pxt=-(3*H*A+B*qdot)/(2*q)
    background_sub={z['P']:0,z['P_X']:A/(2*q),z['P_XX']:(B-A/q)/(4*q*q),
                    z['P_Xt']:pxt,z['V']:U,z['Lambda']:3*H*H-(q*A+U)/M,W:U,WY:d}
    compact_gap=s.factor(results[0][0].subs(background_sub,simultaneous=True))
    target_gap=9*H*H*(m+1)*(1-v)/(m*(m+2))+(m+1)*rho/(2*M*m)
    checks['full_stationary_gap_bridge']=s.factor(compact_gap-target_gap)==0
    checks['metric_coefficient_cancelled']=metric not in results[0][0].free_symbols
    checks['radial_Laplace_Beltrami_bridge']=s.factor(results[0][2]-(Ar_solution/metric-2/r))==0
    # Keep the actual cubic operator for a second branch; do not substitute
    # a gamma=0 coefficient into the gamma=1e-6 numerical calculation.
    full_sub=dict(sub);full_sub.pop(z['gamma'])
    full_ham=s.factor(data['constraints'][0].subs(full_sub))
    full_ar=s.solve(full_ham,Ar)[0]
    full_sub.update({Ar:full_ar,z['constraint_addition']:1})
    full_matrix=data['matrix'].subs(full_sub,simultaneous=True).applyfunc(s.factor)
    full_forcing=data['forcing'].subs(full_sub,simultaneous=True).applyfunc(s.factor)
    assert all(s.diff(item,rho)==0 for item in full_matrix)
    density_vector=full_forcing[:,1].diff(rho)
    cubic_coefficient=s.factor((full_matrix.inv()*density_vector)[3]/metric**2)
    checks['cubic_zero_limit']=s.factor(cubic_coefficient.subs(z['gamma'],0)-results[0][1])==0
    from constitutive import Model
    from equations import evaluate
    numerical=[]
    for gamma in (0.,1e-6):
        model=Model(0.,gamma);bg=model.background(0.)
        def coefficients(width,amplitude):
            rr=np.linspace(.05,3.,33)*width
            density=amplitude*np.exp(-(rr/width)**2)
            integral=amplitude*width**3*np.sqrt(np.pi)/4*gammainc(1.5,(rr/width)**2)
            ff=1-integral/rr
            assert np.min(ff)>0,'radial metric has crossed its regular branch'
            av=1/np.sqrt(ff);ar=(density*rr-integral/rr**2)/(2*ff**1.5)
            values=model.jets(0.,bg['q']**2,0.)
            values.update(A=av,Ar=ar,R=rr,Rr=1.,Rrr=0.,k=bg['H'],h=bg['H'],
                kr=0.,hr=0.,Q=bg['q'],Qr=0.,Qrr=0.,cr=0.,crr=0.,w=0.,rho=density,
                constraint_addition=1.)
            matrix,forcing,constraints=evaluate(values)
            solution=np.linalg.solve(matrix,forcing)
            gap=solution[:,3,1]/av**2
            return rr,density,gap,constraints,ff,values
        _,_,basegap,_,_,basevalues=coefficients(.03,0.)
        point={symbol:basevalues[str(symbol)] for symbol in cubic_coefficient.free_symbols if str(symbol) in basevalues}
        point[q]=bg['q'];point[H]=bg['H']
        slope=float(cubic_coefficient.subs(point))
        # Direct high-precision assembly BEFORE Hamiltonian elimination. This
        # checks whether small-radius cancellation in float64 is numerical.
        # Constitutive jets remain the fixed float64 background; only spatial
        # geometry and the algebraic constraint solve receive extra precision.
        scalar_values={symbol:s.Rational(str(basevalues[str(symbol)])) for symbol in
            set().union(*(expr.free_symbols for expr in list(data['matrix'])+list(data['forcing'])+list(data['constraints'])))
            if str(symbol) in basevalues and np.ndim(basevalues[str(symbol)])==0}
        raw_sub={**sub,z['gamma']:s.Rational(str(gamma)),z['constraint_addition']:1,
                 q:s.Rational(str(bg['q'])),H:s.Rational(str(bg['H']))}
        raw_expressions=[expr.subs(raw_sub,simultaneous=True).subs(scalar_values).subs(raw_sub)
                         for expr in list(data['matrix'])+list(data['forcing'])+list(data['constraints'])]
        # q,H introduced by simultaneous replacement need their final values.
        raw_expressions=[expr.subs({q:s.Rational(str(bg['q'])),H:s.Rational(str(bg['H']))}) for expr in raw_expressions]
        assert set().union(*(expr.free_symbols for expr in raw_expressions)) <= {metric,Ar,r,rho}
        mpfn=s.lambdify((metric,Ar,r,rho),raw_expressions,'mpmath',cse=True)
        mp.mp.dps=60
        def high_precision(width,amplitude):
            out=[]
            for rr_ratio in ('.05','1','3'):
                ww=mp.mpf(str(width));amp=mp.mpf(str(amplitude));rr=mp.mpf(rr_ratio)*ww
                density=amp*mp.exp(-(rr/ww)**2)
                integral=amp*ww**3*mp.gammainc(mp.mpf('1.5'),0,(rr/ww)**2)/2
                ff=1-integral/rr;av=1/mp.sqrt(ff)
                ar=(density*rr-integral/rr**2)/(2*ff**mp.mpf('1.5'))
                flat=mpfn(av,ar,rr,density)
                mm=mp.matrix([flat[j:j+4] for j in range(0,16,4)])
                vv=mp.matrix([flat[17],flat[20],flat[23],flat[26]])
                gap=mp.lu_solve(mm,vv)[3]/av**2
                out.append((density,gap,max(abs(x) for x in flat[28:])))
            return out
        mpbase=high_precision(.03,0.)[1][1]
        for width in (.03,.003,.0003):
            for density_radius in (1e-6,1e-4,.01,1.):
                rr,density,gap,constraints,ff,_=coefficients(width,density_radius/width**2)
                predicted=basegap+slope*density
                error=float(np.max(np.abs(gap-predicted)/np.maximum(abs(gap),1.)))
                # Constraint errors normalized by curvature/source size, since
                # large densities and tiny radii carry correspondingly large units.
                residual=float(np.max(np.abs(constraints))/max(1.,density_radius/width**2))
                high=high_precision(width,density_radius/width**2)
                mp_error=max(float(abs(gg-(mpbase+mp.mpf(str(slope))*dd))/max(abs(gg),1)) for dd,gg,_ in high)
                mp_residual=max(float(cc/max(1.,density_radius/width**2)) for _,_,cc in high)
                assert mp_error<1e-12 and mp_residual<1e-12,(gamma,width,density_radius,mp_error,mp_residual)
                numerical.append(dict(gamma=gamma,width=width,central_rho_times_width_squared=density_radius,
                    relative_gap_identity_error=error,normalized_constraint_residual=residual,
                    float64_within_1e_minus8=error<1e-8 and residual<1e-8,
                    high_precision_gap_error=mp_error,high_precision_constraint_residual=mp_residual,
                    minimum_metric_f=float(np.min(ff)),density_slope=slope,background_gap=float(basegap[0]),
                    central_gap_times_width_squared=float(basegap[0]*width**2+slope*density_radius)))
    assert all(checks.values()),checks
    return dict(checks=checks,hamiltonian_Ar_solution=str(Ar_solution),
        lapse_gap=str(results[0][0]),density_coefficient_general=str(results[0][1]),
        stationary_density_coefficient=str(coefficient),
        stationary_full_gap=str(compact_gap),
        cubic_density_coefficient=str(cubic_coefficient),numerical_cases=numerical,
        radial_first_derivative_coefficient=str(results[0][2]),
        conventions='Nrr=a Nr+A_metric^2 mu2 N+source; q=Q constant; R=r,Kr=Ko=H,dust initially at rest',
        hypotheses=['gamma=0','Hamiltonian constraint imposed','clock constraint and background jets consistent',
                    'positive regular constitutive domain','all inverted coefficient denominators nonzero'],
        interpretation='density-dependent local lapse gap; not a physical metric response pole or halo equilibrium',
        full_theory_status='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path)
    args=parser.parse_args();result=run()
    if args.result_file:args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
