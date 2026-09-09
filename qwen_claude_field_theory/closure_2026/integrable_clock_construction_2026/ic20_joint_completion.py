#!/usr/bin/env python3
"""IC20 joint tensor/scalar curvature completion with an explicit auxiliary.

The coefficient functions are designed from varied equations at one witness.
Their positive exponential continuation defines an action, not a proof that
the continuation is healthy. See IC20_JOINT_COMPLETION.md for the global scope.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic19_normalized_spatial as normalized


def identities():
    E,v0,q,z,R,A,D,L,b=s.symbols('E v0 q z R A D L b',real=True)
    v=v0+z*z
    H=-E*q*q/(6*v)-A*q*z+b-D*z*z-L*z**4-v*R
    zz=s.diff(H,z,2)
    def reduced(i,j):return s.diff(H,i,j)-s.diff(H,i,z)*s.diff(H,j,z)/zz
    qq,qR,RR=reduced(q,q),reduced(q,R),reduced(R,R)
    tensor=E/v
    checks={
        'tensor_cone':s.simplify(-tensor*s.diff(H,R)-E),
        'joint_compatibility':s.factor((qq+tensor/3)*RR-qR*qR),
        'positive_scalar_Schur':s.factor(tensor/6+qq/2+s.diff(H,q,z)**2/(2*zz)),
        'static_value':s.simplify(H.subs({q:0,z:0})-(b-v0*R)),
        'static_q_jet':s.diff(H,q).subs({q:0,z:0}),
        'static_z_jet':s.diff(H,z).subs({q:0,z:0}),
        'static_R_jet':s.diff(H,R).subs({q:0,z:0})+v0,
    }
    # Use the actual auxiliary equation to simplify its derivative on shell.
    R_on=s.solve(s.diff(H,z),R)[0]
    checks['auxiliary_on_shell_curvature']=s.factor(zz.subs(R,R_on)-(A*q/z-4*E*q*q*z*z/(3*v**3)-8*L*z*z))
    # Partial Legendre transform gives the general nondegenerate local class.
    V=s.symbols('V',positive=True)
    aa,bb=s.Function('a')(V),s.Function('b')(V)
    K=-E*q*q/(6*V)+aa*q+bb
    checks['Legendre_general_class']=s.diff(K,q,2)+E/(3*V)
    t=s.symbols('t',real=True)
    kk,ll,vv,vol,zzeta=[s.Function(name)(t) for name in ('K','L','V','volume','zeta')]
    lag=vol*((s.diff(zzeta,t)-ll*zzeta)**2/kk-vv*zzeta**2)
    EL=(s.diff(s.diff(lag,s.diff(zzeta,t)),t)-s.diff(lag,zzeta))*kk/(2*vol)
    target=(s.diff(zzeta,t,2)+(s.diff(vol,t)/vol-s.diff(kk,t)/kk)*s.diff(zzeta,t)
            +(kk*vv-ll**2-s.diff(ll,t)+(s.diff(kk,t)/kk-s.diff(vol,t)/vol)*ll)*zzeta)
    checks['time_dependent_scalar_Euler']=s.simplify(EL-target)
    f,fq,q0,V0=s.symbols('f fq q0 V0',real=True)
    pidot=-s.Rational(3,2)*V0*(f-q0*fq)
    checks['background_mass_cancellation']=s.Rational(9,2)*(f-q0*fq)+3*pidot/V0
    a,e,B,M,k2,c0,Cdot=s.symbols('a e B M k2 c0 Cdot',nonzero=True)
    IR=c0+2*Cdot*e/(E*M);UV=c0+4*a*e*e/(B*E)
    direct=c0+(-8*a*e*e*k2+2*Cdot*e)/(E*(M-2*B*k2))
    checks['all_wavelength_interpolation']=s.factor(direct-(M*IR-2*B*k2*UV)/(M-2*B*k2))
    return checks


@lru_cache(None)
def build():
    S,q,z,R,wc=s.symbols('S q z R wc',real=True)
    funcs=[s.Function(name)(S) for name in ('a','d','e','P')]
    aa,dd,ee,P=funcs
    v=s.exp(S+2*wc)/2+z*z
    H=-s.exp(2*S)*q*q/(6*v)-aa*q*z-s.exp(S)*P-dd*z*z-ee*z**4-v*R
    keys=['h','S','q','z','R','SS','Sq','Sz','SR','qq','qz','qR','zz','zR','RR']
    variables={'S':S,'q':q,'z':z,'R':R}
    expr=[H]+[s.diff(H,*[variables[t] for t in key]) for key in keys[1:]]
    symbols=[];mapping={}
    for i,fn in enumerate(funcs):
        for order in range(3):
            sym=s.Symbol('c%d_%d'%(i,order),real=True)
            symbols.append(sym)
            mapping[s.diff(fn,S,order)]=sym
    expr=[e.subs(mapping,simultaneous=True) for e in expr]
    return dict(keys=keys,evaluate=s.lambdify((S,q,z,R,wc,*symbols),expr,'mpmath',cse=True))


def raw_jets(S,q,z,R,jets):
    S,q,z,R=map(mp.mpf,(S,q,z,R))
    c=normalized.constants()
    if S<=-2*c['wc']:
        raise ValueError('Outside the regular pinned 0<u<1 chart')
    def P(t):return normalized.legacy.original_pressure()(t,c['wc'],c['Lambda'],c['a02'])
    P0,PS=P(S)
    PSS=mp.diff(lambda t:P(t)[1],S)
    args=[S,q,z,R,c['wc'],*jets['a'],*jets['d'],*jets['e'],P0,PS,PSS]
    return dict(zip(build()['keys'],build()['evaluate'](*args)))


def design(lapse_schur='-3',speed_squared='.2',linear_amplitude='.1',quartic_amplitude='.1'):
    S,q,z,R=mp.mpf('.1'),mp.mpf('-3'),mp.mpf('1'),mp.mpf(0)
    a0,e0=mp.mpf(linear_amplitude),mp.mpf(quartic_amplitude)
    target_speed,target_M=mp.mpf(speed_squared),mp.mpf(lapse_schur)
    jets=dict(a=[a0,0,0],d=[0,0,0],e=[e0,0,0])
    first=raw_jets(S,q,z,R,jets)
    d0=first['z']/(2*z)
    if d0<=0:raise ValueError('Construction did not give positive d0')
    jets['d'][0]=d0
    base=raw_jets(S,q,z,R,jets)
    wc=normalized.constants()['wc']
    v0=mp.exp(S+2*wc)/2
    v=v0+z*z
    u=(S+2*wc)/(S+wc)
    B=mp.exp(S+2*wc)*(1-u*u)
    uv=-base['qz']**2/(2*base['zz'])
    if uv<=0:raise ValueError('Construction has nonpositive scalar UV kinetic')
    # The k² momentum-curvature mixing is time dependent. C_Sq=0 below
    # makes Sdot=0 at this design point, but q and z still evolve.
    qdot=-mp.mpf(3)/2*base['h']
    zdot=-base['qz']/base['zz']*qdot
    E=mp.exp(2*S)
    qz_dot=2*E*z/(3*v*v)*qdot+2*E*q/(3*v*v)*(1-4*z*z/v)*zdot
    ratio=-4*z/base['qz']
    ratio_dot=-4*zdot/base['qz']+4*z*qz_dot/base['qz']**2
    correction=-2*uv/E*(ratio_dot+base['q']/2*ratio)
    frozen_target=target_speed-correction
    Z=-mp.sqrt(B*(2*v+E*frozen_target/uv)/4)
    raw_Sq_target=(Z+v0)*base['qz']/(2*z)
    aS=(base['Sq']-raw_Sq_target)/z
    jets['a'][1]=aS
    first=raw_jets(S,q,z,R,jets)
    Sz_target=first['Sq']*first['zz']/first['qz']
    matrix=mp.matrix([[z*z,z**4],[2*z,4*z**3]])
    dS,eS=mp.lu_solve(matrix,mp.matrix([first['S'],first['Sz']-Sz_target]))
    a1,d1,e1=aS/a0,dS/d0,eS/e0
    jets=dict(a=[a0,aS,a0*a1*a1],d=[d0,dS,d0*d1*d1],e=[e0,eS,e0*e1*e1])
    second=raw_jets(S,q,z,R,jets)
    d2=(second['SS']-second['Sz']**2/second['zz']-target_M)/(d0*z*z)
    return dict(S0=S,q0=q,z0=z,a0=a0,a1=a1,d0=d0,d1=d1,d2=d2,e0=e0,e1=e1,
                design_speed_squared=target_speed,design_lapse_Schur=target_M,
                design_frozen_speed_squared=frozen_target)


def coefficient_jets(S,p):
    t=mp.mpf(S)-p['S0']
    aa=p['a0']*mp.exp(p['a1']*t)
    dd=p['d0']*mp.exp(p['d1']*t+p['d2']*t*t/2)
    ee=p['e0']*mp.exp(p['e1']*t)
    return dict(a=[aa,aa*p['a1'],aa*p['a1']**2],
                d=[dd,dd*(p['d1']+p['d2']*t),dd*((p['d1']+p['d2']*t)**2+p['d2'])],
                e=[ee,ee*p['e1'],ee*p['e1']**2])


def state(S,q,z,R,p):
    S,q,z,R=map(mp.mpf,(S,q,z,R))
    raw=raw_jets(S,q,z,R,coefficient_jets(S,p))
    wc=normalized.constants()['wc']
    v0=mp.exp(S+2*wc)/2
    v=v0+z*z
    T=mp.exp(2*S)/v
    u=(S+2*wc)/(S+wc)
    B=mp.exp(S+2*wc)*(1-u*u)
    if raw['zz']==0:raise ValueError('Auxiliary z is singular')
    red={key:raw[key]-raw[a+'z' if a!='R' else 'zR']*raw[b+'z' if b!='R' else 'zR']/raw['zz']
         for key,a,b in [('SS','S','S'),('Sq','S','q'),('SR','S','R'),('qq','q','q'),('qR','q','R'),('RR','R','R')]}
    uv=T/6+red['qq']/2
    Z=red['SR']-red['Sq']*red['qR']/(2*uv) if uv!=0 else mp.nan
    frozen_cs2=(-2*uv*v+4*uv*Z*Z/B)/mp.exp(2*S)
    flow=preservation(raw,R)
    E=mp.exp(2*S)
    jets=coefficient_jets(S,p)
    qz_S=2*E*q*z/(3*v*v)*(2-2*v0/v)-jets['a'][1]
    qz_q=2*E*z/(3*v*v)
    qz_z=2*E*q/(3*v*v)*(1-4*z*z/v)
    qz_dot=qz_S*flow['Sdot']+qz_q*flow['qdot']+qz_z*flow['zdot']
    ratio=-4*z/raw['qz']
    ratio_dot=-4*flow['zdot']/raw['qz']+4*z*qz_dot/raw['qz']**2
    cs2=frozen_cs2-2*uv/E*(ratio_dot+flow['Qdot']*ratio)
    r=-mp.exp(-3*wc)*q/3
    return dict(S=S,q=q,z=z,R=R,v=v,v0=v0,T=T,B=B,u=u,eta=normalized.legacy.activation(r),
                raw=raw,reduced=red,raw_zz=raw['zz'],constraints=[raw['S'],raw['z']],
                H_physical=mp.exp(-wc-S)*raw['q']/2,
                tensor_speed_squared=-T*raw['R']/mp.exp(2*S),
                scalar_UV_momentum=uv,scalar_UV_speed_squared=cs2,frozen_scalar_UV_speed_squared=frozen_cs2,
                compatibility_residual=(red['qq']+T/3)*red['RR']-red['qR']**2,
                lapse_Schur=red['SS'],clock_momentum_cross=red['Sq'],flow=flow,parameters=p)


def preservation(raw,R=0):
    qdot=-mp.mpf(3)/2*raw['h']+R*raw['R']
    Rdot=-raw['q']*R
    Qdot=raw['q']/2
    matrix=mp.matrix([[raw['SS'],raw['Sz']],[raw['Sz'],raw['zz']]])
    source=mp.matrix([3*Qdot*raw['S']+raw['Sq']*qdot+raw['SR']*Rdot,
                      3*Qdot*raw['z']+raw['qz']*qdot+raw['zR']*Rdot])
    multipliers=mp.lu_solve(matrix,-source)
    return dict(Sdot=multipliers[0],zdot=multipliers[1],qdot=qdot,Rdot=Rdot,Qdot=Qdot,
                preservation_residual=list(matrix*multipliers+source))


def constraint_block(b,k_squared):
    raw=b['raw'];k_squared=mp.mpf(k_squared)
    A=mp.matrix([[raw['SS']-2*b['B']*k_squared,raw['Sz']],[raw['Sz'],raw['zz']]])
    F=[raw['S'],raw['z']];Fq=[raw['Sq'],raw['qz']];FR=[raw['SR'],raw['zR']]
    # delta R=(4 k²-2R) zeta; {zeta,delta pi}=1/2 at unit volume.
    secondary=mp.matrix([[mp.mpf(3)/2*(F[i]*Fq[j]-Fq[i]*F[j])+(2*k_squared-b['R'])*(FR[i]*Fq[j]-Fq[i]*FR[j])
                          for j in range(2)] for i in range(2)])
    PB=mp.zeros(4)
    for i in range(2):
        for j in range(2):
            PB[i,j+2]=-A[i,j];PB[i+2,j]=A[i,j];PB[i+2,j+2]=secondary[i,j]
    singular=list(mp.svd(PB,compute_uv=False))
    threshold=mp.power(10,-mp.mp.dps/2)*max(singular)
    return dict(k_squared=k_squared,operator=A.tolist(),poisson_matrix=PB.tolist(),
                singular_values=singular,rank=sum(v>threshold for v in singular),determinant=mp.det(PB),
                rank_threshold=threshold)


def frozen_matrix(b,k_squared):
    k2=mp.mpf(k_squared)
    a=b['scalar_UV_momentum'];H=b['reduced'];C=H['Sq']
    M=H['SS']-2*b['B']*k2
    K=a-C*C/(2*M)
    cross=2*H['qR']*k2-2*C*H['SR']*k2/M
    V=-2*b['v']*k2+8*H['RR']*k2*k2-8*H['SR']**2*k2*k2/M
    matrix=mp.matrix([[K,cross],[cross,V]])
    omega2=mp.det(matrix)
    return dict(k_squared=k2,K=K,L=cross,V=V,momentum_coefficient=K,quadratic_matrix=matrix.tolist(),
                frequency_squared=omega2,speed_squared=omega2/(mp.exp(2*b['S'])*k2),
                full_background_mass_terms_included=False)


def dispersion(b,k_squared):
    frozen=frozen_matrix(b,k_squared)
    flow=b['flow'];k2=mp.mpf(k_squared)
    def along(t):
        moved=state(b['S']+t*flow['Sdot'],b['q']+t*flow['qdot'],b['z']+t*flow['zdot'],
                    b['R']+t*flow['Rdot'],b['parameters'])
        return frozen_matrix(moved,k2*mp.exp(-2*flow['Qdot']*t))
    Kdot=mp.diff(lambda t:along(t)['K'],0)
    Ldot=mp.diff(lambda t:along(t)['L'],0)
    frequency=(frozen['frequency_squared']-Ldot+(Kdot/frozen['K']-3*flow['Qdot'])*frozen['L'])
    return dict(k_squared=k2,momentum_coefficient=frozen['K'],frequency_squared=frequency,
                speed_squared=frequency/(mp.exp(2*b['S'])*k2),frozen_speed_squared=frozen['speed_squared'],
                coordinate_friction=3*flow['Qdot']-Kdot/frozen['K'],Kdot=Kdot,Ldot=Ldot,
                flat_vacuum_FLRW_quadratic_mass_cancellation_included=True)


def all_wavelength_witness(b):
    """Exact rational reduction at H_Sq=0; numbers evaluate its coefficients.

    A finite-k oscillator/k ratio is not a signal/front velocity. The actual
    ultraviolet characteristic is the limit, not this finite-k quotient.
    """
    if abs(b['reduced']['Sq'])>mp.power(10,-mp.mp.dps/2):
        raise ValueError('All-wavelength simplification requires H_Sq=0')
    f=b['flow']
    def moved_C(t):
        return state(b['S']+t*f['Sdot'],b['q']+t*f['qdot'],b['z']+t*f['zdot'],0,b['parameters'])['reduced']['Sq']
    Cdot=mp.diff(moved_C,0)
    a,e,B,M,E=b['scalar_UV_momentum'],b['reduced']['SR'],b['B'],b['lapse_Schur'],mp.exp(2*b['S'])
    UV=b['scalar_UV_speed_squared'];c0=UV-4*a*e*e/(B*E)
    IR=c0+2*Cdot*e/(E*M)
    residuals=[]
    for k2 in map(mp.mpf,('1e-8','.001','1','100','1e8')):
        formula=(M*IR-2*B*k2*UV)/(M-2*B*k2)
        residuals.append(dispersion(b,k2)['speed_squared']-formula)
    return dict(IR_ratio=IR,UV_ratio=UV,Cdot=Cdot,M=M,B=B,kinetic=a,
                maximum_direct_residual=max(map(abs,residuals)),
                formula='omega²/(exp(2S) k²)=(M IR-2B k² UV)/(M-2B k²)',
                scope='Flat vacuum FLRW design point with H_Sq=0; not a global stability theorem')


def continuation(steps=10,step='-.0001',parameters=None):
    p=design() if parameters is None else parameters
    initial=state(p['S0'],p['q0'],p['z0'],0,p)
    states=[initial];reason='requested steps completed';step=mp.mpf(step)
    quadrature=mp.mpf(0)
    def solve(q,seed):
        def eq(S,z):
            raw=raw_jets(S,q,z,0,coefficient_jets(S,p))
            return raw['S'],raw['z']
        S,z=mp.findroot(eq,seed,tol=mp.power(10,-mp.mp.dps+12),maxsteps=60)
        return state(S,q,z,0,p)
    for _ in range(steps):
        old=states[-1]
        # q is a monotone parameter only while its evolution derivative is nonzero.
        if old['flow']['qdot']==0:
            reason='q evolution ceased to be a valid parameter';break
        dq=step if old['flow']['qdot']<0 else -step
        seed=(old['S']+dq*old['flow']['Sdot']/old['flow']['qdot'],
              old['z']+dq*old['flow']['zdot']/old['flow']['qdot'])
        try:
            new=solve(old['q']+dq,seed)
            mid=solve(old['q']+dq/2,((old['S']+new['S'])/2,(old['z']+new['z'])/2))
        except (ValueError,ZeroDivisionError) as exc:
            reason='continuation solve failed: '+str(exc).split('\n')[0];break
        def integrand(b):return -b['raw']['q']/(3*b['raw']['h'])
        quadrature+=dq*(integrand(old)+4*integrand(mid)+integrand(new))/6
        states.append(new)
        if not (new['eta']==1 and new['raw_zz']<0 and new['lapse_Schur']<0
                and new['scalar_UV_momentum']>0 and 0<new['scalar_UV_speed_squared']<=1 and new['H_physical']>0):
            reason='a tested regularity or principal-health condition failed';break
    ratio=initial['raw']['h']/states[-1]['raw']['h']
    return dict(states=states,stop_reason=reason,efolds_from_charge=mp.log(ratio)/3 if ratio>0 else mp.nan,
                efolds_from_quadrature=quadrature,
                maximum_constraint_residual=max(max(abs(v) for v in b['constraints']) for b in states),
                maximum_preservation_residual=max(max(abs(v) for v in b['flow']['preservation_residual']) for b in states))


def matter_state(S,q,z,Q,Mdust,Mradiation,p):
    """Flat homogeneous Sm: Hm/V=exp(S)(Md exp(-3Q)+Mr exp(-4Q)).

    Md,Mr are conserved nonnegative canonical matter amplitudes, with fixed
    conformal units absorbed. No matter perturbation stability is inferred.
    """
    raw=raw_jets(S,q,z,0,coefficient_jets(S,p))
    dust=mp.exp(S-3*Q)*Mdust;rad=mp.exp(S-4*Q)*Mradiation
    constraints=[raw['S']+dust+rad,raw['z']]
    A=mp.matrix([[raw['SS']+dust+rad,raw['Sz']],[raw['Sz'],raw['zz']]])
    Qdot=raw['q']/2
    qdot=-mp.mpf(3)/2*raw['h']+rad/2
    source=mp.matrix([3*Qdot*constraints[0]+raw['Sq']*qdot-Qdot*(3*dust+4*rad),
                      3*Qdot*constraints[1]+raw['qz']*qdot])
    multipliers=mp.lu_solve(A,-source)
    wc=normalized.constants()['wc']
    return dict(S=S,q=q,z=z,Q=Q,dust_hamiltonian=dust,radiation_hamiltonian=rad,
                constraints=constraints,charge=mp.exp(3*Q)*(raw['h']+dust+rad),
                H_physical=mp.exp(-S-wc)*Qdot,qdot=qdot,Qdot=Qdot,
                Sdot=multipliers[0],zdot=multipliers[1],raw_zz=raw['zz'],
                lapse_Schur=A[0,0]-A[0,1]**2/A[1,1],
                preservation_residual=list(A*multipliers+source))


def matter_continuation(steps=10,step='.00001',dust='.000001',radiation='.000001',parameters=None):
    p=design() if parameters is None else parameters
    Md,Mr=mp.mpf(dust),mp.mpf(radiation);step=mp.mpf(step)
    if Md<0 or Mr<0:raise ValueError('Negative matter density is not in this study')
    tolerance=mp.power(10,-mp.mp.dps+12)
    def initial_equations(S,z):
        b=matter_state(S,p['q0'],z,mp.mpf(0),Md,Mr,p)
        return tuple(b['constraints'])
    S,z=mp.findroot(initial_equations,(p['S0'],p['z0']),tol=tolerance,maxsteps=60)
    initial=matter_state(S,p['q0'],z,mp.mpf(0),Md,Mr,p)
    charge=initial['charge'];states=[initial];integral=mp.mpf(0)
    reason='requested steps completed'
    def solve(Q,seed):
        def eq(S,q,z):
            b=matter_state(S,q,z,Q,Md,Mr,p)
            return (*b['constraints'],b['charge']-charge)
        S,q,z=mp.findroot(eq,seed,tol=tolerance,maxsteps=60)
        return matter_state(S,q,z,Q,Md,Mr,p)
    for _ in range(steps):
        old=states[-1]
        if old['Qdot']==0:
            reason='expansion ceased to be a valid parameter';break
        seed=tuple(old[x]+step*old[x+'dot']/old['Qdot'] for x in ('S','q','z'))
        try:
            new=solve(old['Q']+step,seed)
            mid=solve(old['Q']+step/2,tuple((old[x]+new[x])/2 for x in ('S','q','z')))
        except (ValueError,ZeroDivisionError) as exc:
            reason='continuation solve failed: '+str(exc).split('\n')[0];break
        integral+=step*(old['qdot']/old['Qdot']+4*mid['qdot']/mid['Qdot']+new['qdot']/new['Qdot'])/6
        states.append(new)
        if not(new['raw_zz']<0 and new['lapse_Schur']<0 and new['H_physical']>0):
            reason='homogeneous regularity/expansion condition failed';break
    return dict(states=states,stop_reason=reason,dust_amplitude=Md,radiation_amplitude=Mr,
                maximum_constraint_residual=max(max(abs(x) for x in b['constraints']) for b in states),
                maximum_charge_residual=max(abs(b['charge']-charge) for b in states),
                maximum_preservation_residual=max(max(abs(x) for x in b['preservation_residual']) for b in states),
                canonical_flow_quadrature_error=integral-(states[-1]['q']-initial['q']),
                nonclaim='Homogeneous matter evolution only; coupled matter/clock perturbations uncomputed')


def report():
    mp.mp.dps=70
    p=design();b=state(p['S0'],p['q0'],p['z0'],0,p)
    spectra=[dispersion(b,k) for k in ('1e-4','.01','1','100','1e4','1e8','1e12')]
    evolution=continuation()
    evolution_spectra=[dict(q=row['q'],samples=[dispersion(row,k) for k in ('1e-6','.01','1','100','1e8')])
                       for row in evolution['states']]
    matter=matter_continuation()
    all_k=all_wavelength_witness(b)
    # This is a different coefficient choice, not evidence imported into the
    # main action. It diagnoses why homogeneous longevity alone is insufficient.
    stress_p=design('-1000')
    stress=state(stress_p['S0'],stress_p['q0'],stress_p['z0'],0,stress_p)
    stress_result=dict(parameters=stress_p,infrared=dispersion(stress,'.0001'),
                       ultraviolet=dispersion(stress,'1e12'))
    blocks=[constraint_block(b,k) for k in (0,1,10000)]
    checks={key:value==0 for key,value in identities().items()}
    checks.update(varied_background=max(abs(v) for v in b['constraints'])<mp.mpf('1e-50'),
                  expanding=b['H_physical']>0,active_pin=b['eta']==1,
                  positive_scalar_UV=b['scalar_UV_momentum']>0,
                  subluminal_scalar_UV=0<b['scalar_UV_speed_squared']<1,
                  computed_tensor_cone=abs(b['tensor_speed_squared']-1)<mp.mpf('1e-50'),
                  joint_identity=abs(b['compatibility_residual'])<mp.mpf('1e-50'),
                  auxiliary_negative_schur=b['raw_zz']<0 and b['lapse_Schur']<0,
                  computed_auxiliary_blocks=all(row['rank']==4 for row in blocks),
                  finite_high_frequency_energy=spectra[-1]['frequency_squared']>0 and spectra[-1]['momentum_coefficient']>0,
                  vacuum_continuation=evolution['stop_reason']=='requested steps completed',
                  sampled_evolving_scalar_coefficients=all(d['momentum_coefficient']>0 and d['frequency_squared']>0
                         for row in evolution_spectra for d in row['samples']),
                  vacuum_charge_crosscheck=abs(evolution['efolds_from_charge']-evolution['efolds_from_quadrature'])<mp.mpf('1e-9'),
                  matter_continuation=matter['stop_reason']=='requested steps completed',
                  matter_constraints=matter['maximum_constraint_residual']<mp.mpf('1e-45'),
                  matter_charge=matter['maximum_charge_residual']<mp.mpf('1e-45'),
                  matter_canonical_flow=abs(matter['canonical_flow_quadrature_error'])<mp.mpf('1e-9'),
                  all_wavelength_witness=all_k['IR_ratio']>0 and all_k['UV_ratio']>0 and all_k['maximum_direct_residual']<mp.mpf('1e-40'),
                  adverse_coefficient_control=stress_result['infrared']['frequency_squared']<0)
    evolution['states']=[{key:row[key] for key in ('S','q','z','H_physical','lapse_Schur','raw_zz',
                         'scalar_UV_momentum','scalar_UV_speed_squared')} for row in evolution['states']]
    return dict(candidate='IC20 joint completion with explicit analytic auxiliary z',full_theory='OPEN',
                checks=checks,designed_coefficients=p,witness=b,constraint_modes=blocks,scalar_spectra=spectra,
                continuation=evolution,evolving_scalar_samples=evolution_spectra,
                matter_continuation=matter,all_wavelength_witness=all_k,
                adverse_coefficient_control=stress_result,
                nonclaims=['Designed coefficients and bounded numerical continuation, not a healthy global theory',
                           'Scalar quadratic evolution derived only for flat vacuum FLRW, not matter or general anisotropy',
                           'No inherited IC18/IC19 early pole history, PPN, lensing, or empirical pass'])


def completion_status(result,strict=False):
    if not result['checks'] or not all(result['checks'].values()):return 1
    return 2 if strict else 0


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    result=report()
    print(json.dumps(result,indent=2,default=lambda v:str(v) if isinstance(v,s.Basic) else mp.nstr(v,35)))
    raise SystemExit(completion_status(result,args.require_full_closure))
