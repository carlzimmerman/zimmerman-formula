#!/usr/bin/env python3
"""IC20 with varied positive-density irrotational dust, not a radiation limit."""
import argparse
import json
import mpmath as mp
import sympy as s
import ic20_joint_completion as model


def identities():
    N,V,rho,p,velocity,grad=s.symbols('N V rho p velocity grad',positive=True)
    lag=V*rho*velocity**2/(2*N)-N*V*rho*(1+grad)/2
    solved=N*p/(V*rho)
    ham=N*(p*p/(2*V*rho)+V*rho*(1+grad)/2)
    secondary=s.diff(ham,rho)/N
    eliminated=p/(V*s.sqrt(1+grad))
    checks={
        'dust_momentum':s.simplify(s.diff(lag,velocity).subs(velocity,solved)-p),
        'dust_Hamiltonian':s.simplify((p*velocity-lag).subs(velocity,solved)-ham),
        'dust_density_secondary':s.simplify(secondary.subs(rho,eliminated)),
        'dust_eliminated_Hamiltonian':s.simplify(ham.subs(rho,eliminated)-N*p*s.sqrt(1+grad)),
        'dust_primary_secondary_bracket':s.simplify(-s.diff(secondary,rho)+p*p/(V*rho**3)),
    }
    a,C,u,M,Z,d,k2,v,t,j=s.symbols('a C u M Z d k2 v t j',nonzero=True)
    f=s.Matrix([C,u]);g=s.Matrix([Z,0])
    K=s.diag(a,0)-f*f.T/(2*M)
    L=s.Matrix([[2*d*k2,-t*j/4],[0,0]])-f*g.T/(2*M)
    W=s.diag(-2*v*k2+4*d*d/a*k2*k2,s.Symbol('Wdust'))-g*g.T/(2*M)
    inverse=s.Matrix([[1/a,-C/(a*u)],[-C/(a*u),-2*M/u**2+C*C/(a*u*u)]])
    checks['dust_momentum_inverse_00']=s.factor((K*inverse-s.eye(2))[0,0])
    checks['dust_momentum_inverse_01']=s.factor((K*inverse-s.eye(2))[0,1])
    checks['dust_momentum_inverse_10']=s.factor((K*inverse-s.eye(2))[1,0])
    checks['dust_momentum_inverse_11']=s.factor((K*inverse-s.eye(2))[1,1])
    checks['dust_kinetic_determinant']=s.factor(K.det()+a*u*u/(2*M))
    checks['dust_restoring_cancellation']=s.factor((2*(W-L.T*inverse*L))[0,0]+4*v*k2)
    pq,pm,zeta,dtau=s.symbols('pq pm zeta dtau')
    moment=s.Matrix([pq,pm]);field=s.Matrix([zeta,dtau])
    checks['dust_norm_equation']=s.factor((2*(K*moment+L*field))[1]+u*(C*pq+u*pm+Z*zeta)/M)
    actualW=s.diag(-2*v*k2+4*d*d/a*k2*k2,3*t*j*j/8+u*j*k2/2)-g*g.T/(2*M)
    checks['dust_density_current']=s.factor((-2*(L.T*moment+actualW*field))[1]-j*(t*pq/2-(3*t*j/4+u*k2)*dtau))
    A1,A2,F,G,omega=s.symbols('A1 A2 F G omega',nonzero=True)
    symbol=s.Matrix([[G-A1*omega**2,-s.I*omega*F],[s.I*omega*F,-A2*omega**2]])
    checks['gyroscopic_principal_polynomial']=s.expand(symbol.det()-omega**2*(A1*A2*omega**2-A2*G-F**2))
    generator=s.Matrix([[0,0,1,0],[0,0,0,1],[-G/A1,0,0,-F/A1],[0,0,F/A2,0]])
    eigenvector=s.Matrix([0,1,0,0]);generalized=s.Matrix([-F/G,0,0,1])
    checks['dust_exact_zero_eigenvector']=sum(s.simplify(x)**2 for x in generator*eigenvector)
    checks['dust_exact_Jordan_chain']=sum(s.simplify(x)**2 for x in generator*generalized-eigenvector)
    jpos,w=s.symbols('jpos w',positive=True)
    velocity=(1+w)*jpos**w;ell=w*jpos**(1+w)
    checks['positive_pressure_Legendre']=s.simplify(s.diff(ell,jpos)/s.diff(velocity,jpos)-jpos)
    return checks


def fluid_state(S,q,z,Q,Md,w,p):
    raw=model.raw_jets(S,q,z,0,model.coefficient_jets(S,p))
    h=mp.exp(S-3*(1+w)*Q)*Md
    constraints=[raw['S']+h,raw['z']]
    A=mp.matrix([[raw['SS']+h,raw['Sz']],[raw['Sz'],raw['zz']]])
    Qdot=raw['q']/2;qdot=-mp.mpf(3)/2*raw['h']+mp.mpf(3)/2*w*h
    source=mp.matrix([3*Qdot*constraints[0]+raw['Sq']*qdot-3*(1+w)*Qdot*h,
                      3*Qdot*constraints[1]+raw['qz']*qdot])
    multipliers=mp.lu_solve(A,-source)
    return dict(S=S,q=q,z=z,Q=Q,Md=Md,w=w,parameters=p,constraints=constraints,
                H_physical=mp.exp(-S-model.normalized.constants()['wc'])*Qdot,
                Sdot=multipliers[0],zdot=multipliers[1],qdot=qdot,Qdot=Qdot,
                preservation_residual=list(A*multipliers+source))


def background(amplitude='1e-6',pressure='0'):
    p=model.design();Md=mp.mpf(amplitude)
    w=mp.mpf(pressure)
    if Md<=0:raise ValueError('Positive dust density required; vacuum is a singular dust field chart')
    if not 0<=w<=1:raise ValueError('Fluid pressure ratio outside tested causal range')
    def eq(S,z):return tuple(fluid_state(S,p['q0'],z,0,Md,w,p)['constraints'])
    S,z=mp.findroot(eq,(p['S0'],p['z0']),tol=mp.power(10,-mp.mp.dps+12),maxsteps=60)
    return fluid_state(S,p['q0'],z,mp.mpf(0),Md,w,p)


def quadratic(b,k_squared):
    S,q,z,Q=[b[x] for x in ('S','q','z','Q')];k2=mp.mpf(k_squared)
    g=model.state(S,q,z,0,b['parameters']);r=g['reduced']
    w=b['w'];j=b['Md']**(1/(1+w))*mp.exp(-3*Q)
    hd=mp.exp(S)*j**(1+w);u=mp.exp(S)*(1+w)*j**w;beta=w*u/(2*j)
    C=r['Sq'];Z=4*r['SR']*k2-3*(1+w)*hd;M=r['SS']+hd-2*g['B']*k2
    f=mp.matrix([C,u]);field=mp.matrix([Z,0])
    K=mp.matrix([[g['scalar_UV_momentum'],0],[0,beta]])-f*f.T/(2*M)
    L=mp.matrix([[2*r['qR']*k2,-g['T']*j/4],[-3*w*u/2,0]])-f*field.T/(2*M)
    W=mp.matrix([[-2*g['v']*k2+8*r['RR']*k2*k2+mp.mpf(9)/2*w*(1+w)*hd,0],
                 [0,3*g['T']*j*j/8+mp.exp(2*S)*j*k2/(2*u)]])-field*field.T/(2*M)
    D=mp.diag([2,1]);inverse=K**-1
    return dict(K=K,L=L,W=W,A=D*inverse*D/2,B=-D*inverse*L,
                potential=2*(W-L.T*inverse*L),M=M,j=j,beta=beta,u=u)


def time_matrices(b,k_squared):
    k2=mp.mpf(k_squared);base=quadratic(b,k2)
    def moved(time):
        args=[b[x]+time*b[x+'dot'] for x in ('S','q','z','Q')]
        row=fluid_state(*args,b['Md'],b['w'],b['parameters'])
        return quadratic(row,k2*mp.exp(-2*b['Qdot']*time))
    Adot=mp.matrix([[mp.diff(lambda time:moved(time)['A'][i,j],0) for j in range(2)] for i in range(2)])
    Bdot=mp.matrix([[mp.diff(lambda time:moved(time)['B'][i,j],0) for j in range(2)] for i in range(2)])
    A,B=base['A'],base['B']
    return dict(A=A,F=Adot+3*b['Qdot']*A+B-B.T,
                G=Bdot+3*b['Qdot']*B+base['potential'],M=base['M'])


def frequencies(b,k_squared):
    k2=mp.mpf(k_squared);m=time_matrices(b,k2)
    damping=(m['A']**-1)*m['F'];restoring=(m['A']**-1)*m['G']
    generator=mp.zeros(4)
    for i in range(2):
        generator[i,i+2]=1
        for j in range(2):generator[i+2,j]=-restoring[i,j];generator[i+2,j+2]=-damping[i,j]
    values,vectors=mp.eig(generator,left=False,right=True)
    residuals=[mp.norm(generator*vectors[:,i]-values[i]*vectors[:,i])/
               max(mp.mpf(1),mp.norm(generator)*mp.norm(vectors[:,i])) for i in range(4)]
    return dict(k_squared=k2,growth_exponents=[dict(real=mp.re(x),imag=mp.im(x)) for x in values],
                maximum_eigen_residual=max(residuals),kinetic_eigenvalues=list(mp.eigsy(m['A'],eigvals_only=True)),
                fastest_oscillatory_speed_squared=max(abs(mp.im(x)) for x in values)**2/(mp.exp(2*b['S'])*k2),
                maximum_real_growth=max(mp.re(x) for x in values),
                interpretation='Instantaneous roots of full time-dependent local equation; slow roots are not a cosmological growth solution')


def principal_symbol(b):
    if b['w']!=0:raise ValueError('Dust principal scaling applies only at exactly zero pressure')
    g=model.state(b['S'],b['q'],b['z'],0,b['parameters']);r=g['reduced']
    a=g['scalar_UV_momentum'];d=r['qR'];Z=r['SR']-r['Sq']*d/(2*a)
    u=mp.exp(b['S']);E=u*u
    def ratio(time):
        row=model.state(b['S']+time*b['Sdot'],b['q']+time*b['qdot'],b['z']+time*b['zdot'],0,b['parameters'])
        return row['reduced']['qR']/row['scalar_UV_momentum']
    derivative=mp.diff(ratio,0)
    A1,A2=2/a,2*g['B']/u**2
    F=4*Z/u
    G=-4*(g['v']+derivative+b['Qdot']*d/a)
    # Det(-omega² A-i omega F+G), after dust field rescaling by 1/k.
    polynomial=[A1*A2,mp.mpf(0),-A2*G-F*F,mp.mpf(0),mp.mpf(0)]
    nonzero=(A2*G+F*F)/(A1*A2*E)
    multiplicity=0
    for coefficient in reversed(polynomial):
        if coefficient!=0:break
        multiplicity+=1
    generator=mp.matrix([[0,0,1,0],[0,0,0,1],[-G/A1,0,0,-F/A1],[0,0,F/A2,0]])
    singular=list(mp.svd(generator,compute_uv=False));threshold=max(singular)*mp.power(10,-mp.mp.dps/2)
    rank=sum(x>threshold for x in singular)
    return dict(A_diagonal=[A1,A2],gyroscopic_off_diagonal=F,restoring_gravity=G,
                frequency_polynomial_descending=polynomial,nonzero_speed_squared=nonzero,
                without_gyroscopic_speed_squared=G/(A1*E),
                zero_frequency_multiplicity=multiplicity,
                zero_eigenspace_dimension=generator.rows-rank,principal_generator=generator.tolist(),
                principal_singular_values=singular,rank_threshold=threshold,
                caveat='Zero-speed dust sector requires subprincipal evolution and energy/caustic analysis')


def pressure_principal(b):
    if b['w']<=0:raise ValueError('Positive pressure required for the regular fluid principal scaling')
    g=model.state(b['S'],b['q'],b['z'],0,b['parameters']);r=g['reduced']
    matter=quadratic(b,1);a=g['scalar_UV_momentum'];d=r['qR'];E=mp.exp(2*b['S'])
    def ratio(time):
        row=model.state(b['S']+time*b['Sdot'],b['q']+time*b['qdot'],b['z']+time*b['zdot'],0,b['parameters'])
        return row['reduced']['qR']/row['scalar_UV_momentum']
    cg=(-2*a*g['v']+4*a*(r['SR']-r['Sq']*d/(2*a))**2/g['B'])/E-2*a*(mp.diff(ratio,0)+b['Qdot']*d/a)/E
    beta,j,u=matter['beta'],matter['j'],matter['u']
    cf=2*beta*j/u
    symbol=mp.matrix([[cg,d*g['T']*j/(2*E)],[2*beta*d*g['T']*j/(a*E),cf]])
    eigen=list(mp.eig(symbol,left=False,right=False))
    return dict(symbol=symbol.tolist(),speeds_squared=[mp.re(x) for x in eigen],
                maximum_imaginary_part=max(abs(mp.im(x)) for x in eigen),
                kinetic_coefficients=[a,beta],gradient_determinant=mp.det(symbol),
                lightcone_margin_determinant=mp.det(mp.eye(2)-symbol))


def auxiliary_matrix(b,k_squared):
    if b['w']!=0:raise ValueError('Density multiplier belongs to the exactly pressureless action')
    k2=mp.mpf(k_squared);g=model.state(b['S'],b['q'],b['z'],0,b['parameters']);r=g['raw']
    N=mp.exp(b['S']);j=b['Md']*mp.exp(-3*b['Q']);hd=N*j
    A=mp.matrix([[r['SS']+hd-2*g['B']*k2,r['Sz'],0],
                 [r['Sz'],r['zz'],0],[0,0,N/j]])
    fQ=[3*r['S']-3*b['q']*r['Sq']+4*k2*r['SR'],
        3*r['z']-3*b['q']*r['qz']+4*k2*r['zR'],3*N]
    fpi=[r['Sq'],r['qz'],mp.mpf(0)]
    PB=mp.zeros(6)
    for i in range(3):
        for jdx in range(3):
            PB[i,jdx+3]=-A[i,jdx];PB[i+3,jdx]=A[i,jdx]
            PB[i+3,jdx+3]=(fQ[i]*fpi[jdx]-fpi[i]*fQ[jdx])/2
    singular=list(mp.svd(PB,compute_uv=False));threshold=max(singular)*mp.power(10,-mp.mp.dps/2)
    return dict(k_squared=k2,matrix=PB.tolist(),singular_values=singular,rank=sum(x>threshold for x in singular),
                determinant=mp.det(PB),rank_threshold=threshold)


def report():
    mp.mp.dps=70;rows=[]
    for amplitude in ('1e-12','1e-8','1e-6','1e-5','1e-4'):
        try:
            b=background(amplitude)
            rows.append(dict(amplitude=amplitude,background={key:value for key,value in b.items() if key!='parameters'},
                             principal=principal_symbol(b),frequencies=[frequencies(b,k) for k in ('1e2','1e6','1e10')],
                             auxiliary_matrices=[auxiliary_matrix(b,k) for k in (0,1,10000)]))
        except (ValueError,ZeroDivisionError) as exc:
            rows.append(dict(amplitude=amplitude,error=str(exc).split('\n')[0]))
    checks={key:value==0 for key,value in identities().items()}
    checks['all_requested_backgrounds_solved']=all('error' not in row for row in rows)
    good=[row for row in rows if 'error' not in row]
    checks['sampled_positive_kinetic']=all(min(f['kinetic_eigenvalues'])>0 for row in good for f in row['frequencies'])
    checks['dust_fast_principal_crosscheck']=all(abs(row['frequencies'][-1]['fastest_oscillatory_speed_squared']-
                      row['principal']['nonzero_speed_squared'])<mp.mpf('1e-7') for row in good)
    checks['dust_Jordan_defect_recorded']=all(row['principal']['zero_eigenspace_dimension']<row['principal']['zero_frequency_multiplicity'] for row in good)
    checks['computed_full_auxiliary_ranks']=all(m['rank']==6 for row in good for m in row['auxiliary_matrices'])
    pressure_rows=[]
    for w in ('.001','1e-6','1e-8'):
        b=background('1e-6',pressure=w)
        finite=frequencies(b,'1e14')
        observed=sorted(x['imag']**2/(mp.exp(2*b['S'])*mp.mpf('1e14')) for x in finite['growth_exponents'] if x['imag']>0)
        pressure_rows.append(dict(w=w,principal=pressure_principal(b),frequencies=finite,observed_speeds_squared=observed))
    checks['positive_pressure_principal']=all(row['principal']['maximum_imaginary_part']<mp.mpf('1e-50')
                and min(row['principal']['kinetic_coefficients'])>0
                and min(row['frequencies']['kinetic_eigenvalues'])>0
                and all(0<x<1 for x in row['principal']['speeds_squared']) for row in pressure_rows)
    checks['positive_pressure_frequency_crosscheck']=all(len(row['observed_speeds_squared'])==len(row['principal']['speeds_squared'])
         and max(abs(x-y) for x,y in zip(sorted(row['principal']['speeds_squared']),row['observed_speeds_squared']))<mp.mpf('1e-7') for row in pressure_rows)
    return dict(full_theory='OPEN',checks=checks,rows=rows,positive_pressure_completion=pressure_rows,
                nonclaims=['Aligned flat pressureless fluid only; no relative flow, nonlinear caustics, long evolution or empirical pass',
                           'Exact dust has a defective zero-speed principal sector; positive fast speed is not strong hyperbolicity',
                           'Positive-pressure probes change the explicit matter equation of state, not gravitational coefficients; no global matter guarantee'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args();result=report()
    print(json.dumps(result,indent=2,default=lambda x:mp.nstr(x,35)))
    raise SystemExit(1 if not all(result['checks'].values()) else 2 if args.require_full_closure else 0)
