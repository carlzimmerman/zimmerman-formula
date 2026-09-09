#!/usr/bin/env python3
"""IC20 plus simultaneous radiation and positive-pressure ordinary matter.

Aligned flat-FLRW scalar reduction. No imported separate-fluid health claim.
"""
import argparse
import json
import mpmath as mp
import sympy as s
import ic20_joint_completion as model


def identities():
    cg,w1,w2,f1,f2,g1,g2,lam=s.symbols('cg w1 w2 f1 f2 g1 g2 lam',nonzero=True)
    symbol=s.Matrix([[cg,f1,f2],[g1,w1,0],[g2,0,w2]])
    checks={'mixed_characteristic_polynomial':s.expand((lam*s.eye(3)-symbol).det()-
                ((lam-cg)*(lam-w1)*(lam-w2)-f1*g1*(lam-w2)-f2*g2*(lam-w1)))}
    x0,x1,x2,r1,r2=s.symbols('x0 x1 x2 r1 r2',real=True)
    form=cg*x0*x0+w1*x1*x1+w2*x2*x2+2*r1*x0*x1+2*r2*x0*x2
    square=w1*(x1+r1*x0/w1)**2+w2*(x2+r2*x0/w2)**2+(cg-r1*r1/w1-r2*r2/w2)*x0*x0
    checks['mixed_gradient_completed_square']=s.factor(form-square)
    cone=x0*x0+x1*x1+x2*x2-form
    square=(1-w1)*(x1-r1*x0/(1-w1))**2+(1-w2)*(x2-r2*x0/(1-w2))**2
    square+=(1-cg-r1*r1/(1-w1)-r2*r2/(1-w2))*x0*x0
    checks['mixed_lightcone_completed_square']=s.factor(cone-square)
    time=s.symbols('time');volume=s.Function('volume')(time)
    x=s.Matrix([s.Function('x%d'%i)(time) for i in range(3)])
    A=s.Matrix(3,3,lambda i,j:s.Function('A%d%d'%(min(i,j),max(i,j)))(time))
    B=s.Matrix(3,3,lambda i,j:s.Function('B%d%d'%(i,j))(time))
    C=s.Matrix(3,3,lambda i,j:s.Function('C%d%d'%(min(i,j),max(i,j)))(time))
    lag=volume*((x.diff(time).T*A*x.diff(time))[0]/2+(x.diff(time).T*B*x)[0]-(x.T*C*x)[0]/2)
    expected=A*x.diff(time,2)+(A.diff(time)+volume.diff(time)/volume*A+B-B.T)*x.diff(time)+(B.diff(time)+volume.diff(time)/volume*B+C)*x
    for i in range(3):
        actual=(s.diff(s.diff(lag,x[i].diff(time)),time)-s.diff(lag,x[i]))/volume
        checks['three_field_Euler_%d'%i]=s.simplify(actual-expected[i])
    z,pqz,pSz,pSq,pzz,v0=s.symbols('z pqz pSz pSq pzz v0',nonzero=True)
    a=-pqz**2/(2*pzz);d=2*z*pqz/pzz
    C=pSq-pSz*pqz/pzz;e=-v0+2*z*pSz/pzz
    checks['potential_gradient_jet_cancels']=s.factor(e-C*d/(2*a)-(-v0+2*z*pSq/pqz))
    rs,rq,rz,ratio,qd,HQ,E,a,frozen,target=s.symbols('rs rq rz ratio qd HQ E a frozen target',nonzero=True)
    sd=(E*(frozen-target)/(2*a)-(rq-rz*pqz/pzz)*qd-HQ*ratio)/(rs-rz*pSz/pzz)
    zd=-(pSz*sd+pqz*qd)/pzz
    checks['potential_controller_equation']=s.factor(frozen-2*a*(rs*sd+rq*qd+rz*zd+HQ*ratio)/E-target)
    a,b1,b2,d,C,e,B,t,j1,j2,u1,u2,k2,v,g1,g2=s.symbols('a b1 b2 d C e B t j1 j2 u1 u2 k2 v g1 g2',nonzero=True)
    inverse0=s.diag(1/a,1/b1,1/b2);f=s.Matrix([C,u1,u2])
    inverse=inverse0-inverse0*f*f.T*inverse0/(4*B*k2)
    L=s.Matrix([[2*d*k2+C*e/B,-t*j1/4,-t*j2/4],[-3*w1*u1/2+u1*e/B,0,0],[-3*w2*u2/2+u2*e/B,0,0]])
    W=s.diag(4*d*d/a*k2*k2+(-2*v+4*e*e/B)*k2,g1*k2,g2*k2)
    leading=(2*(W-L.T*inverse*L)).applyfunc(lambda x:s.expand(x).coeff(k2,1))
    expected=s.Matrix([[2*(-2*v+4*(e-C*d/(2*a))**2/B),d*t*j1/a,d*t*j2/a],
                       [d*t*j1/a,2*g1,0],[d*t*j2/a,0,2*g2]])
    for i in range(3):
        for j in range(3):checks['three_field_principal_Schur_%d%d'%(i,j)]=s.factor(leading[i,j]-expected[i,j])
    return checks


def species(radiation='1e-6',matter='1e-6',pressure='1e-8'):
    return [dict(name='radiation',w=mp.mpf(1)/3,c=mp.mpf(3)/4,amplitude=mp.mpf(radiation)),
            dict(name='pressure_matter',w=mp.mpf(pressure),c=mp.mpf(1),amplitude=mp.mpf(matter))]


def state(S,q,z,Q,fluids,parameters):
    raw=model.raw_jets(S,q,z,0,model.coefficient_jets(S,parameters))
    entries=[]
    for f in fluids:
        w,c,M=f['w'],f['c'],f['amplitude']
        if not(0<w<1 and c>0 and M>0):raise ValueError('Regular positive-pressure mixture required')
        j=(M/c)**(1/(1+w))*mp.exp(-3*Q);h=mp.exp(S)*c*j**(1+w)
        u=(1+w)*h/j;beta=w*u/(2*j)
        entries.append(dict(**f,j=j,h=h,u=u,beta=beta))
    total=mp.fsum(f['h'] for f in entries);pressure=mp.fsum(f['w']*f['h'] for f in entries)
    constraints=[raw['S']+total,raw['z']]
    A=mp.matrix([[raw['SS']+total,raw['Sz']],[raw['Sz'],raw['zz']]])
    Qdot=raw['q']/2;qdot=-mp.mpf(3)/2*(raw['h']-pressure)
    source=mp.matrix([3*Qdot*constraints[0]+raw['Sq']*qdot-3*Qdot*(total+pressure),
                      3*Qdot*constraints[1]+raw['qz']*qdot])
    multipliers=mp.lu_solve(A,-source)
    return dict(S=S,q=q,z=z,Q=Q,fluids=fluids,entries=entries,parameters=parameters,raw=raw,
                constraints=constraints,charge=mp.exp(3*Q)*(raw['h']+total),
                Sdot=multipliers[0],zdot=multipliers[1],qdot=qdot,Qdot=Qdot,
                H_physical=mp.exp(-S-model.normalized.constants()['wc'])*Qdot,
                lapse_Schur=A[0,0]-A[0,1]**2/A[1,1],preservation_residual=list(A*multipliers+source))


def background(radiation='1e-6',matter='1e-6',pressure='1e-8'):
    p=model.design();fluids=species(radiation,matter,pressure)
    def eq(S,z):return tuple(state(S,p['q0'],z,mp.mpf(0),fluids,p)['constraints'])
    S,z=mp.findroot(eq,(p['S0'],p['z0']),tol=mp.power(10,-mp.mp.dps+12),maxsteps=60)
    return state(S,p['q0'],z,mp.mpf(0),fluids,p)


def quadratic(b,k_squared):
    k2=mp.mpf(k_squared);g=model.state(b['S'],b['q'],b['z'],0,b['parameters']);r=g['reduced']
    entries=b['entries'];n=1+len(entries);a=g['scalar_UV_momentum'];E=mp.exp(2*b['S'])
    total=mp.fsum(f['h'] for f in entries)
    Z=4*r['SR']*k2-3*mp.fsum((1+f['w'])*f['h'] for f in entries)
    M=r['SS']+total-2*g['B']*k2
    K=mp.diag([a]+[f['beta'] for f in entries]);L=mp.zeros(n);W=mp.zeros(n)
    L[0,0]=2*r['qR']*k2
    W[0,0]=-2*g['v']*k2+8*r['RR']*k2*k2+mp.mpf(9)/2*mp.fsum(f['w']*(1+f['w'])*f['h'] for f in entries)
    for i,f in enumerate(entries,1):
        L[0,i]=-g['T']*f['j']/4;L[i,0]=-3*f['w']*f['u']/2
        for j,h in enumerate(entries,1):W[i,j]=3*g['T']*f['j']*h['j']/8
        W[i,i]+=E*f['j']*k2/(2*f['u'])
    psource=mp.matrix([r['Sq']]+[f['u'] for f in entries]);xsource=mp.matrix([Z]+[0]*len(entries))
    K-=psource*psource.T/(2*M);L-=psource*xsource.T/(2*M);W-=xsource*xsource.T/(2*M)
    D=mp.diag([2]+[1]*len(entries));inverse=K**-1
    return dict(K=K,L=L,W=W,A=D*inverse*D/2,B=-D*inverse*L,potential=2*(W-L.T*inverse*L),M=M)


def frequencies(b,k_squared):
    k2=mp.mpf(k_squared);base=quadratic(b,k2);n=base['A'].rows
    def moved(time):
        args=[b[x]+time*b[x+'dot'] for x in ('S','q','z','Q')]
        return quadratic(state(*args,b['fluids'],b['parameters']),k2*mp.exp(-2*b['Qdot']*time))
    Adot=mp.matrix([[mp.diff(lambda time:moved(time)['A'][i,j],0) for j in range(n)] for i in range(n)])
    Bdot=mp.matrix([[mp.diff(lambda time:moved(time)['B'][i,j],0) for j in range(n)] for i in range(n)])
    A,B=base['A'],base['B']
    damping=(A**-1)*(Adot+3*b['Qdot']*A+B-B.T)
    restoring=(A**-1)*(Bdot+3*b['Qdot']*B+base['potential'])
    generator=mp.zeros(2*n)
    for i in range(n):
        generator[i,i+n]=1
        for j in range(n):generator[i+n,j]=-restoring[i,j];generator[i+n,j+n]=-damping[i,j]
    values,vectors=mp.eig(generator,left=False,right=True)
    residual=max(mp.norm(generator*vectors[:,i]-values[i]*vectors[:,i])/max(1,mp.norm(generator)*mp.norm(vectors[:,i])) for i in range(2*n))
    return dict(k_squared=k2,growth_exponents=[dict(real=mp.re(x),imag=mp.im(x)) for x in values],
                maximum_eigen_residual=residual,kinetic_eigenvalues=list(mp.eigsy(A,eigvals_only=True)),
                interpretation='Instantaneous full-equation roots; only high-frequency limits are characteristic speeds')


def principal(b):
    g=model.state(b['S'],b['q'],b['z'],0,b['parameters']);r=g['reduced'];entries=b['entries']
    a=g['scalar_UV_momentum'];d=r['qR'];E=mp.exp(2*b['S'])
    def ratio(time):
        row=model.state(b['S']+time*b['Sdot'],b['q']+time*b['qdot'],b['z']+time*b['zdot'],0,b['parameters'])
        return row['reduced']['qR']/row['scalar_UV_momentum']
    cg=(-2*a*g['v']+4*a*(r['SR']-r['Sq']*d/(2*a))**2/g['B'])/E-2*a*(mp.diff(ratio,0)+b['Qdot']*d/a)/E
    symbol=mp.zeros(1+len(entries));symbol[0,0]=cg;mix=[]
    for i,f in enumerate(entries,1):
        symbol[i,i]=2*f['beta']*f['j']/f['u']
        symbol[0,i]=d*g['T']*f['j']/(2*E)
        symbol[i,0]=2*f['beta']*d*g['T']*f['j']/(a*E)
        mix.append(symbol[0,i]*symbol[i,0])
    values=list(mp.eig(symbol,left=False,right=False))
    return dict(symbol=symbol.tolist(),speeds_squared=[mp.re(x) for x in values],
                maximum_imaginary_part=max(abs(mp.im(x)) for x in values),
                kinetic_coefficients=[a]+[f['beta'] for f in entries],mixing_products=mix,
                gravity_diagonal=cg,gradient_margin=cg-mp.fsum(J/f['w'] for J,f in zip(mix,entries)),
                lightcone_margin=1-cg-mp.fsum(J/(1-f['w']) for J,f in zip(mix,entries)))


def constraint_matrix(b,k_squared):
    k2=mp.mpf(k_squared);r=b['raw'];g=model.state(b['S'],b['q'],b['z'],0,b['parameters'])
    total=mp.fsum(f['h'] for f in b['entries']);pressure=mp.fsum(f['w']*f['h'] for f in b['entries'])
    A=mp.matrix([[r['SS']+total-2*g['B']*k2,r['Sz']],[r['Sz'],r['zz']]])
    fQ=[3*r['S']-3*b['q']*r['Sq']+4*k2*r['SR']-3*pressure,
        3*r['z']-3*b['q']*r['qz']+4*k2*r['zR']]
    fpi=[r['Sq'],r['qz']];PB=mp.zeros(4)
    for i in range(2):
        for j in range(2):
            PB[i,j+2]=-A[i,j];PB[i+2,j]=A[i,j]
            PB[i+2,j+2]=(fQ[i]*fpi[j]-fpi[i]*fQ[j])/2
    singular=list(mp.svd(PB,compute_uv=False));threshold=max(singular)*mp.power(10,-mp.mp.dps/2)
    return dict(k_squared=k2,matrix=PB.tolist(),singular_values=singular,rank=sum(x>threshold for x in singular),
                determinant=mp.det(PB),rank_threshold=threshold)


def control_diagnostics(b,target=None):
    """Reconstruct the D'' jet needed for a chosen clock diagonal.

    This is a local action-jet design equation, NOT an integrated D(S) function.
    """
    g=model.state(b['S'],b['q'],b['z'],0,b['parameters']);r=b['raw'];z=b['z'];E=mp.exp(2*b['S'])
    a=g['scalar_UV_momentum'];v=g['v'];v0=g['v0'];q=b['q'];p=r['qz']
    jets=model.coefficient_jets(b['S'],b['parameters'])
    pS=2*E*q*z/(3*v*v)*(2-2*v0/v)-jets['a'][1]
    pq=2*E*z/(3*v*v);pz=2*E*q/(3*v*v)*(1-4*z*z/v)
    rho=-4*z/p;rhoS=4*z*pS/p**2;rhoq=4*z*pq/p**2;rhoz=-4/p+4*z*pz/p**2
    Z=-v0+2*z*r['Sq']/p
    frozen=(-2*a*v+4*a*Z*Z/g['B'])/E
    target=principal(b)['gravity_diagonal'] if target is None else mp.mpf(target)
    denominator=rhoS-rhoz*r['Sz']/r['zz']
    Sdot=(E*(frozen-target)/(2*a)-(rhoq-rhoz*r['qz']/r['zz'])*b['qdot']-b['Qdot']*rho)/denominator
    if Sdot==0:raise ValueError('Cannot reconstruct D(S) second jet at a stationary S without an additional compatibility condition')
    total=mp.fsum(f['h'] for f in b['entries']);enthalpy=mp.fsum((1+f['w'])*f['h'] for f in b['entries'])
    rawSS0=r['SS']+z*z*jets['d'][2]
    Dpp=((rawSS0+total-r['Sz']**2/r['zz'])*Sdot+g['reduced']['Sq']*b['qdot']-3*b['Qdot']*enthalpy)/(z*z*Sdot)
    new_M=rawSS0+total-r['Sz']**2/r['zz']-z*z*Dpp
    return dict(target_gravity_diagonal=target,denominator=denominator,reconstructed_Sdot=Sdot,
                original_Dpp=jets['d'][2],required_Dpp=Dpp,reconstructed_lapse_Schur=new_M,
                nonclaim='Pointwise jet equation only; integrability, nonlinear interactions and a globally defined coefficient function unproved')


def lapse_potential_control(b,target_M='-3'):
    """Design only a D'' jet; then vary it to compute its actual multiplier.

    Integrating this jet prescription to ONE D(S) is a separate obligation.
    """
    target_M=mp.mpf(target_M);S,q,z=b['S'],b['q'],b['z']
    g=model.state(S,q,z,0,b['parameters']);old=b['raw'];jets=model.coefficient_jets(S,b['parameters'])
    total=mp.fsum(f['h'] for f in b['entries']);enthalpy=mp.fsum((1+f['w'])*f['h'] for f in b['entries'])
    rawSS0=old['SS']+z*z*jets['d'][2]
    jets['d'][2]=(rawSS0+total-old['Sz']**2/old['zz']-target_M)/(z*z)
    r=model.raw_jets(S,q,z,0,jets)
    A=mp.matrix([[r['SS']+total,r['Sz']],[r['Sz'],r['zz']]])
    source=mp.matrix([r['Sq']*b['qdot']-3*b['Qdot']*enthalpy,r['qz']*b['qdot']])
    multiplier=mp.lu_solve(A,-source)
    p=r['qz'];E=mp.exp(2*S);v=g['v'];v0=g['v0'];a=g['scalar_UV_momentum']
    pS=2*E*q*z/(3*v*v)*(2-2*v0/v)-jets['a'][1]
    pq=2*E*z/(3*v*v);pz=2*E*q/(3*v*v)*(1-4*z*z/v)
    rho=-4*z/p;rhoS=4*z*pS/p**2;rhoq=4*z*pq/p**2;rhoz=-4/p+4*z*pz/p**2
    Z=-v0+2*z*r['Sq']/p
    cg=(-2*a*v+4*a*Z*Z/g['B'])/E-2*a*(rhoS*multiplier[0]+rhoq*b['qdot']+rhoz*multiplier[1]+b['Qdot']*rho)/E
    return dict(target_M=target_M,required_Dpp=jets['d'][2],computed_lapse_Schur=A[0,0]-A[0,1]**2/A[1,1],
                computed_gravity_diagonal=cg,computed_Sdot=multiplier[0],computed_zdot=multiplier[1],
                multiplier_residual=list(A*multiplier+source),
                nonclaim='Second action jet only; no integrated coefficient function or finite-wavelength health certification')


def continuation(target_Q='.01',step='.0001',max_steps=500):
    initial=background();charge=initial['charge'];states=[initial];target_Q=mp.mpf(target_Q);step=mp.mpf(step)
    if target_Q<=0 or step<=0:raise ValueError('This bounded probe evolves toward increasing Q')
    tolerance=mp.power(10,-mp.mp.dps+12);reason='requested endpoint reached';failures=[]
    def solve(Q,seed):
        current=mp.matrix(seed)
        for iteration in range(45):
            b=state(*list(current),Q,initial['fluids'],initial['parameters'])
            residual=mp.matrix([*b['constraints'],b['charge']-charge]);norm=max(map(abs,residual))
            if norm<tolerance:return b
            r=b['raw'];total=mp.fsum(f['h'] for f in b['entries']);volume=mp.exp(3*Q)
            jac=mp.matrix([[r['SS']+total,r['Sq'],r['Sz']],
                           [r['Sz'],r['qz'],r['zz']],
                           [volume*b['constraints'][0],volume*r['q'],volume*r['z']]])
            delta=mp.lu_solve(jac,-residual);accepted=False
            for half in range(30):
                trial=current+delta/mp.power(2,half)
                if trial[0]<=-2*model.normalized.constants()['wc'] or trial[2]<=0:continue
                try:
                    row=state(*list(trial),Q,initial['fluids'],initial['parameters'])
                    trial_norm=max(map(abs,[*row['constraints'],row['charge']-charge]))
                except (ValueError,ZeroDivisionError):continue
                if trial_norm<norm:current=trial;accepted=True;break
            if not accepted:raise ValueError('Damped Newton could not reduce the actual equation residual')
        raise ValueError('Damped Newton iteration bound reached')
    def health(b):
        p=principal(b)
        return (b['H_physical']>0 and b['raw']['zz']<0 and b['lapse_Schur']<0
                and min(p['kinetic_coefficients'])>0 and p['gradient_margin']>0 and p['lightcone_margin']>0)
    boundary=None
    for attempt in range(max_steps):
        old=states[-1]
        if old['Q']>=target_Q:break
        if old['Qdot']<=0:reason='Expansion stopped';break
        dq=min(step,target_Q-old['Q'])
        seed=[old[x]+dq*old[x+'dot']/old['Qdot'] for x in ('S','q','z')]
        try:new=solve(old['Q']+dq,seed)
        except (ValueError,ZeroDivisionError) as exc:
            failures.append(dict(Q=old['Q']+dq,step=dq,error=str(exc)))
            step/=2
            if step<mp.mpf('1e-9'):reason='Minimum continuation step reached without convergence';break
            continue
        states.append(new)
        if not health(new):
            reason='A principal or auxiliary health condition crossed'
            low,high=old,new
            for _ in range(20):
                middle=solve((low['Q']+high['Q'])/2,[(low[x]+high[x])/2 for x in ('S','q','z')])
                if health(middle):low=middle
                else:high=middle
            boundary=dict(lower_Q=low['Q'],upper_Q=high['Q'],lower_principal=principal(low),upper_principal=principal(high),
                          lower_lapse_Schur=low['lapse_Schur'],upper_lapse_Schur=high['lapse_Schur'])
            break
    else:reason='Continuation attempt bound reached'
    return dict(states=states,stop_reason=reason,requested_Q=target_Q,solver_retries=failures,boundary_bracket=boundary,
                maximum_constraint_residual=max(max(map(abs,b['constraints'])) for b in states),
                maximum_charge_residual=max(abs(b['charge']-charge) for b in states),
                maximum_preservation_residual=max(max(map(abs,b['preservation_residual'])) for b in states))


def report():
    mp.mp.dps=70;rows=[]
    for radiation,matter in (('1e-8','1e-6'),('1e-6','1e-6'),('1e-5','1e-5')):
        b=background(radiation,matter)
        rows.append(dict(radiation=radiation,matter=matter,principal=principal(b),
                         background={key:value for key,value in b.items() if key not in ('parameters','raw')},
                         frequencies=frequencies(b,'1e14'),constraints=[constraint_matrix(b,k) for k in (0,1,10000)]))
    checks={key:value==0 for key,value in identities().items()}
    checks['mixed_constraints']=all(max(map(abs,row['background']['constraints']))<mp.mpf('1e-45') for row in rows)
    checks['mixed_positive_kinetic']=all(min(row['principal']['kinetic_coefficients'])>0 for row in rows)
    checks['mixed_principal_bounds']=all(row['principal']['gradient_margin']>0 and row['principal']['lightcone_margin']>0 for row in rows)
    checks['mixed_auxiliary_ranks']=all(x['rank']==4 for row in rows for x in row['constraints'])
    checks['mixed_finite_kinetic']=all(min(row['frequencies']['kinetic_eigenvalues'])>0 for row in rows)
    for row in rows:
        row['observed_speeds_squared']=sorted(x['imag']**2/(mp.exp(2*row['background']['S'])*mp.mpf('1e14'))
                        for x in row['frequencies']['growth_exponents'] if x['imag']>0)
    checks['independent_mixed_frequency_crosscheck']=all(len(row['observed_speeds_squared'])==len(row['principal']['speeds_squared'])
              and max(abs(x-y) for x,y in zip(row['observed_speeds_squared'],sorted(row['principal']['speeds_squared'])))<mp.mpf('1e-7') for row in rows)
    evolution=continuation()
    checks['continuation_constraints']=evolution['maximum_constraint_residual']<mp.mpf('1e-45')
    checks['continuation_charge']=evolution['maximum_charge_residual']<mp.mpf('1e-45')
    controller=dict(initial=control_diagnostics(evolution['states'][0]),
                    endpoint_target_jet=control_diagnostics(evolution['states'][-1],target=principal(evolution['states'][0])['gravity_diagonal']),
                    endpoint_lapse_control=lapse_potential_control(evolution['states'][-1]))
    checks['controller_reconstructs_initial_jet']=abs(controller['initial']['required_Dpp']-controller['initial']['original_Dpp'])<mp.mpf('1e-40')
    checks['local_lapse_control_varied']=abs(controller['endpoint_lapse_control']['computed_lapse_Schur']+3)<mp.mpf('1e-40')
    evolution['states']=[dict(Q=b['Q'],S=b['S'],q=b['q'],z=b['z'],H_physical=b['H_physical'],
                               lapse_Schur=b['lapse_Schur'],principal=principal(b)) for b in evolution['states']]
    return dict(full_theory='OPEN',checks=checks,rows=rows,evolution=evolution,potential_controller=controller,
                nonclaims=['Aligned noninteracting perfect fluids, not photon-baryon transport or recombination',
                           'No relative flow, long healthy history, general nonlinear closure, PPN or empirical pass'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args();result=report();print(json.dumps(result,indent=2,default=lambda x:mp.nstr(x,35)))
    raise SystemExit(1 if not all(result['checks'].values()) else 2 if args.require_full_closure else 0)
