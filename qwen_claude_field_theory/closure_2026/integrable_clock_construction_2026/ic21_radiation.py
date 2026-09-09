#!/usr/bin/env python3
"""IC20 plus explicit minimally coupled P(X_sigma)=X_sigma² radiation.

Aligned flat-FLRW scalar reduction only, not relative-flow or CMB closure.
"""
import argparse
import json
import mpmath as mp
import sympy as s
import ic20_joint_completion as model


def identities():
    N,V,p,velocity,gradient=s.symbols('N V p velocity gradient',positive=True)
    X=(velocity**2/N**2-gradient)/2
    lag=N*V*X**2
    solved=N*(p/V)**s.Rational(1,3)
    h=s.Rational(3,4)*N*p**s.Rational(4,3)/V**s.Rational(1,3)
    checks={
        'matter_momentum':s.simplify(s.diff(lag,velocity).subs({gradient:0,velocity:solved})-p),
        'matter_Hamiltonian':s.simplify((p*velocity-lag).subs({gradient:0,velocity:solved})-h),
        'matter_gradient':s.simplify(-s.diff(lag,gradient).subs({gradient:0,velocity:solved})
                                   -N*V**s.Rational(1,3)*p**s.Rational(2,3)/2),
    }
    dq,j,v,amp=s.symbols('dq j v amp')
    solution=s.solve(-4*amp/3-2*dq/3+j*v,amp)[0]
    checks['sourced_momentum_constraint']=s.expand(s.Rational(2,3)*solution**2-(dq-s.Rational(3,2)*j*v)**2/6)
    hr,hg,q,hq=s.symbols('hr hg q hq')
    pidot=-s.Rational(3,2)*(hg-q*hq-hr/3)
    checks['matter_background_mass']=s.expand(s.Rational(9,2)*(hg-q*hq)+3*pidot+hr/2-2*hr)
    time=s.symbols('time')
    x=s.Matrix([s.Function('x')(time),s.Function('y')(time)])
    a,b,c=[s.Function(n)(time) for n in ('a','b','c')]
    A=s.Matrix([[a,b],[b,c]])
    B=s.Matrix(2,2,lambda i,j:s.Function('B%d%d'%(i,j))(time))
    C=s.Matrix([[s.Function('d')(time),s.Function('e')(time)],
                [s.Function('e')(time),s.Function('f')(time)]])
    volume=s.Function('volume')(time)
    ell=volume*((x.diff(time).T*A*x.diff(time))[0]/2+(x.diff(time).T*B*x)[0]-(x.T*C*x)[0]/2)
    expected=A*x.diff(time,2)+(A.diff(time)+volume.diff(time)/volume*A+B-B.T)*x.diff(time)+(B.diff(time)+volume.diff(time)/volume*B+C)*x
    for i in range(2):
        EL=(s.diff(s.diff(ell,x[i].diff(time)),time)-s.diff(ell,x[i]))/volume
        checks['coupled_Euler_%d'%i]=s.simplify(EL-expected[i])
    cg,cr,off1,off2,lam=s.symbols('cg cr off1 off2 lam')
    symbol=s.Matrix([[cg,off1],[off2,cr]])
    checks['principal_characteristic_polynomial']=s.expand((symbol-lam*s.eye(2)).det()-((lam-cg)*(lam-cr)-off1*off2))
    checks['principal_lightcone_margin']=s.expand((s.eye(2)-symbol).det()-((1-cg)*(1-cr)-off1*off2))
    a,beta,d,C,e,B,t,j,u,v,k2,grad=s.symbols('a beta d C e B t j u v k2 grad',nonzero=True)
    inverse0=s.diag(1/a,1/beta);source=s.Matrix([C,u])
    inverse=inverse0-inverse0*source*source.T*inverse0/(4*B*k2)
    L=s.Matrix([[2*d*k2+C*e/B,-t*j/4],[-u/2+u*e/B,0]])
    W=s.diag(4*d*d/a*k2*k2+(-2*v+4*e*e/B)*k2,grad*k2)
    reduced=2*(W-L.T*inverse*L)
    leading=reduced.applyfunc(lambda x:s.expand(x).coeff(k2,1))
    expected=s.Matrix([[2*(-2*v+4*(e-C*d/(2*a))**2/B),d*t*j/a],[d*t*j/a,2*grad]])
    for i in range(2):
        for jdx in range(2):checks['principal_Schur_%d%d'%(i,jdx)]=s.factor(leading[i,jdx]-expected[i,jdx])
    return checks


def background(amplitude='1e-6',q=None):
    p=model.design();Mr=mp.mpf(amplitude);Q=mp.mpf(0)
    if Mr<=0:raise ValueError('Use positive radiation; zero is a limiting field chart')
    q=p['q0'] if q is None else mp.mpf(q)
    def eq(S,z):return tuple(model.matter_state(S,q,z,Q,0,Mr,p)['constraints'])
    S,z=mp.findroot(eq,(p['S0'],p['z0']),tol=mp.power(10,-mp.mp.dps+12),maxsteps=60)
    b=model.matter_state(S,q,z,Q,0,Mr,p)
    b.update(parameters=p,Mr=Mr)
    return b


def quadratic(b,k_squared):
    S,q,z,Q=[b[x] for x in ('S','q','z','Q')]
    k2=mp.mpf(k_squared);p=b['parameters']
    # Use IC20 only for raw partial derivatives, not its vacuum flow.
    g=model.state(S,q,z,0,p);red=g['reduced']
    j=(4*b['Mr']/3)**mp.mpf('.75')*mp.exp(-3*Q)
    hr=mp.exp(S)*mp.mpf(3)/4*j**(mp.mpf(4)/3)
    u=mp.exp(S)*j**(mp.mpf(1)/3)
    C=red['Sq'];Z=4*red['SR']*k2-4*hr
    M=red['SS']+hr-2*g['B']*k2
    # H2/V = momenta^T K momenta + 2 momenta^T L fields + fields^T W fields.
    # Fields=(zeta,delta sigma), momenta=(delta q,delta P_sigma/V).
    K=mp.matrix([[g['scalar_UV_momentum'],0],[0,mp.exp(S)*j**(-mp.mpf(2)/3)/6]])
    L=mp.matrix([[2*red['qR']*k2,-g['T']*j/4],[-u/2,0]])
    W=mp.matrix([[-2*g['v']*k2+8*red['RR']*k2*k2+2*hr,0],
                 [0,3*g['T']*j*j/8+mp.exp(S)*j**(mp.mpf(2)/3)*k2/2]])
    moment=mp.matrix([C,u]);field=mp.matrix([Z,0])
    K-=moment*moment.T/(2*M)
    L-=moment*field.T/(2*M)
    W-=field*field.T/(2*M)
    D=mp.diag([2,1]);inverse=K**-1
    A=D*inverse*D/2
    B=-D*inverse*L
    potential=2*(W-L.T*inverse*L)
    return dict(K=K,L=L,W=W,A=A,B=B,potential=potential,M=M,j=j,hr=hr)


def constraint_matrix(b,k_squared):
    k2=mp.mpf(k_squared)
    g=model.state(b['S'],b['q'],b['z'],0,b['parameters']);r=g['raw']
    hr=b['radiation_hamiltonian']
    A=mp.matrix([[r['SS']+hr-2*g['B']*k2,r['Sz']],[r['Sz'],r['zz']]])
    # Canonical Q derivatives at fixed trace pi and radiation momentum.
    csQ=3*r['S']-3*b['q']*r['Sq']+4*k2*r['SR']-hr
    czQ=3*r['z']-3*b['q']*r['qz']+4*k2*r['zR']
    secondary=(csQ*r['qz']-r['Sq']*czQ)/2
    PB=mp.zeros(4)
    for i in range(2):
        for j in range(2):PB[i,j+2]=-A[i,j];PB[i+2,j]=A[i,j]
    PB[2,3]=secondary;PB[3,2]=-secondary
    singular=list(mp.svd(PB,compute_uv=False));threshold=max(singular)*mp.power(10,-mp.mp.dps/2)
    return dict(k_squared=k2,matrix=PB.tolist(),rank=sum(x>threshold for x in singular),
                singular_values=singular,threshold=threshold,determinant=mp.det(PB))


def principal(b,k_squared):
    k2=mp.mpf(k_squared);base=quadratic(b,k2)
    def moved(t):
        args=[b[x]+t*b[x+'dot'] for x in ('S','q','z','Q')]
        row=model.matter_state(*args,0,b['Mr'],b['parameters'])
        row.update(parameters=b['parameters'],Mr=b['Mr'])
        return quadratic(row,k2*mp.exp(-2*b['Qdot']*t))
    Adot=mp.matrix([[mp.diff(lambda t:moved(t)['A'][i,j],0) for j in range(2)] for i in range(2)])
    Bdot=mp.matrix([[mp.diff(lambda t:moved(t)['B'][i,j],0) for j in range(2)] for i in range(2)])
    A,B=base['A'],base['B']
    damping=Adot+3*b['Qdot']*A+B-B.T
    restoring=Bdot+3*b['Qdot']*B+base['potential']
    operator=(A**-1)*restoring/(mp.exp(2*b['S'])*k2)
    eigen=list(mp.eig(operator,left=False,right=False))
    imag=max(abs(mp.im(x)) for x in eigen)
    return dict(k_squared=k2,speeds_squared=[mp.re(x) for x in eigen],maximum_imaginary_part=imag,
                kinetic_eigenvalues=list(mp.eigsy(A,eigvals_only=True)),
                kinetic_matrix=A.tolist(),scaled_restoring_operator=operator.tolist(),
                damping_matrix=((A**-1)*damping).tolist(),lapse_operator=base['M'],
                interpretation='Large-k characteristic estimate; finite-k eigenvalues are not signal speeds')


def principal_limit(b):
    S,q,z,Q=[b[x] for x in ('S','q','z','Q')]
    g=model.state(S,q,z,0,b['parameters']);red=g['reduced']
    a,d,C,e,t,B,E=g['scalar_UV_momentum'],red['qR'],red['Sq'],red['SR'],g['T'],g['B'],mp.exp(2*S)
    j=(4*b['Mr']/3)**mp.mpf('.75')*mp.exp(-3*Q)
    beta=mp.exp(S)*j**(-mp.mpf(2)/3)/6
    def ratio(time):
        row=model.state(S+time*b['Sdot'],q+time*b['qdot'],z+time*b['zdot'],0,b['parameters'])
        return row['reduced']['qR']/row['scalar_UV_momentum']
    cg=(-2*a*g['v']+4*a*(e-C*d/(2*a))**2/B)/E-2*a*(mp.diff(ratio,0)+b['Qdot']*d/a)/E
    # Both matter diagonal and off-diagonal entries come from the reduced
    # Hamiltonian, including the radiation source of the momentum constraint.
    cr=2*beta*mp.exp(S)*j**(mp.mpf(2)/3)/E
    off1=d*t*j/(2*E);off2=2*beta*d*t*j/(a*E)
    symbol=mp.matrix([[cg,off1],[off2,cr]])
    eigen=list(mp.eig(symbol,left=False,right=False))
    return dict(symbol=symbol.tolist(),speeds_squared=[mp.re(x) for x in eigen],
                maximum_imaginary_part=max(abs(mp.im(x)) for x in eigen),
                kinetic_coefficients=[a,beta],gradient_determinant=mp.det(symbol),
                lightcone_margin_determinant=mp.det(mp.eye(2)-symbol),mixing_product=off1*off2,
                gravity_diagonal=cg,radiation_diagonal=cr,
                scope='Exact aligned flat-FLRW principal formula, numerical evaluation of action coefficients')


def report():
    mp.mp.dps=70
    rows=[]
    for amplitude in ('1e-12','1e-8','1e-6','1e-5','1e-4'):
        try:
            b=background(amplitude)
            rows.append(dict(amplitude=amplitude,background={key:value for key,value in b.items() if key!='parameters'},
                             spectra=[principal(b,k) for k in ('1e6','1e10','1e12')],limit=principal_limit(b),
                             constraints=[constraint_matrix(b,k) for k in (0,1,10000)]))
        except (ValueError,ZeroDivisionError) as exc:
            rows.append(dict(amplitude=amplitude,error=str(exc).split('\n')[0]))
    checks={key:value==0 for key,value in identities().items()}
    checks['dilute_regular_background']=('error' not in rows[0])
    checks['all_requested_backgrounds_solved']=all('error' not in row for row in rows)
    good=[row for row in rows if 'error' not in row]
    checks['sampled_positive_kinetic']=all(min(row['limit']['kinetic_coefficients'])>0 for row in good)
    checks['computed_matter_auxiliary_ranks']=all(block['rank']==4 for row in good for block in row['constraints'])
    checks['sampled_causal_real_principal_modes']=all(row['limit']['maximum_imaginary_part']<mp.mpf('1e-50')
                and all(0<x<1 for x in row['limit']['speeds_squared']) for row in good)
    checks['independent_principal_limit']=all(max(abs(x-y) for x,y in zip(sorted(row['limit']['speeds_squared']),
                sorted(row['spectra'][-1]['speeds_squared'])))<mp.mpf('1e-8') for row in good)
    evolution=model.matter_continuation(dust='0',radiation='1e-6')
    evolving=[]
    for b in evolution['states']:
        row=dict(b,parameters=model.design(),Mr=mp.mpf('1e-6'))
        evolving.append(dict(Q=b['Q'],limit=principal_limit(row)))
    checks['radiation_evolution_completed']=evolution['stop_reason']=='requested steps completed'
    checks['evolving_principal_modes']=all(min(x['limit']['kinetic_coefficients'])>0
               and x['limit']['maximum_imaginary_part']<mp.mpf('1e-50')
               and all(0<c<1 for c in x['limit']['speeds_squared']) for x in evolving)
    return dict(full_theory='OPEN',checks=checks,rows=rows,evolving_principal_modes=evolving,
                background_evolution={key:value for key,value in evolution.items() if key!='states'},
                nonclaims=['Aligned irrotational radiation only; no dust or relative flow perturbation test',
                           'No empirical recombination calculation, global stability, or complete theory'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true');args=parser.parse_args()
    result=report();print(json.dumps(result,indent=2,default=lambda x:mp.nstr(x,35)))
    raise SystemExit(1 if not all(result['checks'].values()) else 2 if args.require_full_closure else 0)
