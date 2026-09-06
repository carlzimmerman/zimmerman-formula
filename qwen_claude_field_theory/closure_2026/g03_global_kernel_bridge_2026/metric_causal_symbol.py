"""All-metric spacetime principal response of the metric_constraint Hamiltonian.

No expected curvature response, rank or causality verdict is an input to the
linear solve. All six metric coordinates, six momenta, three shifts, lapse
and trace multiplier are varied. See METRIC_CAUSAL_SYMBOL.md for the exact
regular-tangent-limit hypothesis needed to lift the result to a no-go.
"""
import argparse
import json
from pathlib import Path
import platform
import time

import sympy as s
from metric_constraint import linear_dirac


def derive():
    start=time.monotonic()
    k,omega=s.symbols('k omega',positive=True)
    alpha=s.symbols('alpha',real=True)
    q=k**2
    hs=s.symbols('hxx hyy hzz hxy hxz hyz',real=True)
    ps=s.symbols('pxx pyy pzz pxy pxz pyz',real=True)
    bx,by,bz,n,lam=s.symbols('bx by bz n lam',real=True)
    shifts=s.Matrix([bx,by,bz]); kv=s.Matrix([0,0,k])
    h=s.Matrix([[hs[0],hs[3],hs[4]],[hs[3],hs[1],hs[5]],[hs[4],hs[5],hs[2]]])
    # Off-diagonal canonical p=2*pi, because pi^{ij} dot(h_ij) sums i,j.
    pi=s.Matrix([[ps[0],ps[3]/2,ps[4]/2],[ps[3]/2,ps[1],ps[5]/2],
                 [ps[4]/2,ps[5]/2,ps[2]]])
    tr=s.trace(h); p_trace=s.trace(pi)
    kinetic=s.trace(pi*pi)-p_trace**2/2
    R1=q*tr-(kv.T*h*kv)[0]
    L_R2=-q*s.trace(h*h)/4+q*tr**2/4+(h*kv).dot(h*kv)/2-(kv.T*h*kv)[0]*tr/2
    H=kinetic+2*(pi*kv).dot(shifts)-L_R2-n*R1-2*alpha*q*n**2+lam*p_trace
    pn,pbx,pby,pbz,pl=s.symbols('pn pbx pby pbz pl',real=True)
    primary=[pn,pbx,pby,pbz,pl]
    all_dirac=linear_dirac(H,list(hs)+[n,bx,by,bz,lam],list(ps)+primary,primary)
    # The reused generic algorithm labels its count 'scalar_mode_count'; this
    # call contains every metric polarization, so report the correct meaning.
    all_dirac['physical_gravitational_pairs']=all_dirac.pop('scalar_mode_count')

    rho,sxx,syy,sxy,sxz,syz=s.symbols('rho Sxx Syy Sxy Sxz Syz',real=True)
    stress=s.Matrix([[sxx,sxy,sxz],[sxy,syy,syz],[sxz,syz,omega**2*rho/q]])
    current=s.Matrix([s.I*k*sxz/omega,s.I*k*syz/omega,s.I*omega*rho/k])
    Hsource=H+n*rho-(h*stress).trace()/2-shifts.dot(current)
    source_conservation=[-s.I*omega*rho+k*current[2]]+list(-s.I*omega*current-stress*kv)
    # h and T_ij use cosine spatial amplitudes; shifts and T_0i sine amplitudes.
    # Time dependence exp(-i omega t); generic omega !=0 and k !=0.
    equations=[-s.I*omega*x-s.diff(Hsource,p) for x,p in zip(hs,ps)]
    equations += [-s.I*omega*p+s.diff(Hsource,x) for x,p in zip(hs,ps)]
    equations += [s.diff(Hsource,x) for x in [n,bx,by,bz,lam]]
    # Spatial gauge only, imposed after variation; no lapse/time gauge.
    equations += [hs[2],hs[4],hs[5]]
    variables=list(hs)+list(ps)+[n,bx,by,bz,lam]
    A,b=s.linear_eq_to_matrix(equations,variables)
    solutions=s.linsolve((A,b),variables)
    if not solutions:
        raise RuntimeError('Inconsistent all-metric equations')
    solution=dict(zip(variables,list(solutions)[0]))
    residuals=[s.cancel(e.subs(solution)) for e in equations]
    closed=all(v==0 for v in residuals)

    # Direct contraction of linearized Ricci; no potential-only causality test.
    R00=-s.I*omega*k*bz-q*n+omega**2*tr/2
    R00=s.factor(R00.subs(solution))
    trace_source=s.trace(stress)
    GR=s.factor(R00.subs(alpha,0))
    GR_res=s.factor(GR-(rho+trace_source)/4)
    delta=s.factor(R00-GR)
    scalar_form=s.factor(R00/((rho+trace_source)/4))
    tensor_denominator=s.denom(s.factor(solution[hs[3]]))
    tensor_pole=s.rem(s.Poly(tensor_denominator,omega),s.Poly(omega**2-q,omega)).is_zero
    tensor_independent=all(s.diff(R00,x)==0 for x in [sxy,sxz,syz]) and s.diff(R00,sxx)==s.diff(R00,syy)

    # Expand the FULL added lapse/metric density about any a=a0*y zhat.
    # Jet expansion includes every quadratic n,h,dn term, not only its winner.
    y,a0,z,scale=s.symbols('y a0 z scale',positive=True)
    kx,ky,kz=s.symbols('kx ky kz',real=True)
    dns=s.symbols('dnx dny dnz',real=True)
    dn=s.Matrix(dns); av=s.Matrix([0,0,a0*y])
    F=2*(1-(1+s.sqrt(z))*s.exp(-s.sqrt(z)))
    F0=F.subs(z,y**2); Fz=s.diff(F,z).subs(z,y**2); Fzz=s.diff(F,z,2).subs(z,y**2)
    z1=(2*av.dot(dn)-(av.T*h*av)[0])/a0**2
    z2=(dn.dot(dn)-2*n*av.dot(dn)-2*(av.T*h*dn)[0]+(av.T*h*h*av)[0])/a0**2
    volume1=n+tr/2
    volume2=n*tr/2+tr**2/8-s.trace(h*h)/4
    Laux2=s.expand(2*a0**2*(F0*volume2+Fz*(z2+volume1*z1)+Fzz*z1**2/2))
    derivative_scaled=s.expand(Laux2.subs(dict(zip(dns,[scale*kx*n,scale*ky*n,scale*kz*n]))))
    principal=s.factor(derivative_scaled.coeff(scale,2))
    spatial_q=kx**2+ky**2+kz**2
    M=s.hessian(2*a0**2*F.subs(z,(s.Symbol('gx')**2+s.Symbol('gy')**2+s.Symbol('gz')**2)/a0**2),
                [s.Symbol('gx'),s.Symbol('gy'),s.Symbol('gz')])/4
    M=M.subs({s.Symbol('gx'):0,s.Symbol('gy'):0,s.Symbol('gz'):a0*y}).applyfunc(s.simplify)
    wave=s.Matrix([kx,ky,kz]); anisotropic_alpha=s.factor((wave.T*M*wave)[0]/spatial_q)
    mixed=[s.diff(Laux2,x,d) for x in hs for d in dns]
    metric=[s.diff(Laux2,x,v) for x in hs for v in hs]
    # Count derivative degree from the exact quadratic density, before IBP.
    mixed_degree=max(s.Poly(s.diff(derivative_scaled,x,n),scale).degree() for x in hs)
    metric_degree=max(s.Poly(s.diff(derivative_scaled,x,v),scale).degree() for x in hs for v in hs)

    # Pure scalar conserved source: rho=f Delta sigma, J_i=-f' partial_i sigma,
    # S_ij=f'' sigma delta_ij. Its tensor/vector projections vanish exactly.
    f=s.symbols('f')
    probe_delta=s.factor(delta.subs({rho:-q*f,sxx:-omega**2*f,syy:-omega**2*f})/f)
    mt,ml=s.symbols('mu_t mu_l',positive=True)
    D=mt*(kx**2+ky**2)+ml*kz**2
    transfer=s.factor(probe_delta.subs({alpha:1-D/spatial_q,k:s.sqrt(spatial_q)}))
    # Since response is polynomial in omega, each coefficient multiplies a
    # derivative of delta(t). Causal cone support requires spatial locality.
    jet=s.factor(s.expand(transfer).coeff(omega,4))
    jet_numerator=s.factor(s.together(jet).as_numer_denom()[0])
    locality_eqs=s.Poly(jet_numerator,kx,ky,kz).coeffs()
    locality_solutions=s.solve(locality_eqs,[mt,ml],dict=True)
    exp_jet=s.factor(jet.subs({mt:1-s.exp(-y),ml:1+(y-1)*s.exp(-y)}))
    transverse_jet=s.factor(exp_jet.subs({ky:0,kz:0}))
    # Any nonzero homogeneous degree -2 multiplier cannot be a polynomial.
    homogeneity=s.factor(jet.subs({kx:scale*kx,ky:scale*ky,kz:scale*kz})-jet/scale**2)

    # Independent admissibility check: local stress jets of healthy canonical
    # matter. This is NOT a solved finite-gradient gravitational background.
    t,eps,sigma=s.symbols('t eps sigma',real=True)
    masses=[1,2,3]; initial=[s.S.One,s.Rational(1,2),s.Rational(1,3)]
    velocities=[1,1,1]; perturb=[1,-2,1]
    backgrounds=[]; perturbations=[]
    for m,a,v,du in zip(masses,initial,velocities,perturb):
        backgrounds.append(sum((-m*m)**j*(a*t**(2*j)/s.factorial(2*j)+v*t**(2*j+1)/s.factorial(2*j+1)) for j in range(4)))
        perturbations.append(sum(du*(-(q+m*m))**j*t**(2*j+1)/s.factorial(2*j+1) for j in range(4)))
    density=sum(s.diff(bg,t)*s.diff(dp,t)+m*m*bg*dp for bg,dp,m in zip(backgrounds,perturbations,masses))
    pressure=sum(s.diff(bg,t)*s.diff(dp,t)-m*m*bg*dp for bg,dp,m in zip(backgrounds,perturbations,masses))
    current_coefficient=-sum(s.diff(bg,t)*dp for bg,dp in zip(backgrounds,perturbations))
    trunc=lambda expr,order:s.series(s.expand(expr),t,0,order).removeO()
    density=trunc(density,6); pressure=trunc(pressure,5); current_coefficient=trunc(current_coefficient,5)
    energy_signs=[s.expand(sum(((v+sign*eps*du*sigma)**2+m*m*a*a)/2
                              for m,a,v,du in zip(masses,initial,velocities,perturb))) for sign in [-1,1]]
    matter_conserved=trunc(s.diff(density,t)-q*current_coefficient,4)==0 and trunc(s.diff(current_coefficient,t)+pressure,4)==0
    matter={'density_jet_coefficient':str(density),'pressure_jet_coefficient':str(pressure),
            'current_jet_coefficient':str(current_coefficient),
            'stress_trace_second_time_derivative':str(s.diff(3*pressure,t,2).subs(t,0)),
            'initial_energy_difference':str(s.simplify(energy_signs[1]-energy_signs[0])),
            'initial_stress_difference':str(pressure.subs(t,0)),
            'both_initial_energies_positive':all(e.is_positive for e in energy_signs),
            'initial_energies':list(map(str,energy_signs)),
            'conservation_to_computed_order':matter_conserved,
            'scope':'Three positive-mass canonical Klein-Gordon fields on flat space; local source jets, not a coupled nonzero-acceleration gravity solution.'}
    checks={
        'conserved_arbitrary_tensor_source':all(s.simplify(v)==0 for v in source_conservation),
        'all_twenty_equation_residuals_zero':closed,
        'all_metric_Dirac_preservation_closed':all_dirac['preservation_closed'],
        'GR_Ricci_identity':GR_res==0,
        'full_auxiliary_order_two_matches_lapse_Hessian':s.factor(principal-2*n**2*spatial_q*anisotropic_alpha)==0,
        'no_hidden_metric_derivative_in_auxiliary_density':all(not e.has(*dns) for e in metric),
        'nonlocal_time_jet_degree_minus_two':homogeneity==0,
        'GR_probe_difference_zero':s.simplify(transfer.subs({mt:1,ml:1}))==0,
        'scalar_probe_matches_independent_contracted_equation':s.factor(probe_delta+alpha*(q+3*omega**2)**2/(4*q*(1-alpha)))==0,
        'healthy_matter_stress_jets_conserved':matter_conserved,
    }
    return {'checks':checks,'python':platform.python_version(),'sympy':s.__version__,
        'canonical_metric_coordinates':list(map(str,hs)),'shift_coordinates':list(map(str,shifts)),
        'canonical_Hamiltonian':str(H),'matter_Hamiltonian':str(Hsource-H),
        'equation_count':len(equations),'unknown_count':len(variables),
        'all_metric_dirac':all_dirac,
        'all_equation_residuals_zero':closed,'equation_residuals':list(map(str,residuals)),
        'metric_solution':{str(x):str(s.factor(v)) for x,v in solution.items()},
        'Ricci_00':str(R00),'Ricci_source_factor':str(scalar_form),'GR_Ricci_identity_residual':str(GR_res),
        'tensor_wave_pole_present':bool(tensor_pole),'Ricci_trace_independent_of_tensor_source':tensor_independent,
        'full_auxiliary_quadratic_density':str(s.factor(Laux2)),
        'auxiliary_mixed_derivative_degree':int(mixed_degree),'auxiliary_metric_derivative_degree':int(metric_degree),
        'principal_auxiliary_density':str(principal),'anisotropic_alpha':str(anisotropic_alpha),
        'conserved_scalar_probe_Ricci_transfer':str(transfer),'time_jet_multiplier':str(jet),
        'exponential_time_jet_multiplier':str(exp_jet),'exponential_transverse_time_jet':str(transverse_jet),
        'locality_solutions':[{str(x):str(v) for x,v in row.items()} for row in locality_solutions],
        'GR_locality':s.simplify(jet.subs({mt:1,ml:1}))==0,
        'exponential_locality':s.simplify(transverse_jet)==0,
        'healthy_matter_jets':matter,
        'scope':'Complete spacetime principal metric/source symbol. Nonlinear no-go requires regular causal tangent response on a smooth nonzero-field solution and admissible conserved-stress probes; no unconditional all-gravity no-go.',
        'runtime_seconds':round(time.monotonic()-start,3)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    p.add_argument('--require-causal-conserved-source-response',action='store_true')
    args=p.parse_args(); result=derive()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    for i,(name,ok) in enumerate(result['checks'].items(),1):
        print('[{}] {} {}'.format('ok' if ok else 'FAIL',i,name))
    print('All-metric Ricci source factor:',result['Ricci_source_factor'])
    print('Time-jet locality conditions:',result['locality_solutions'])
    print('Exponential transverse time-jet:',result['exponential_transverse_time_jet'])
    print('Scope:',result['scope'])
    raise SystemExit(1 if not all(result['checks'].values()) else
                     2 if args.require_causal_conserved_source_response and not result['exponential_locality'] else 0)
