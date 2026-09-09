#!/usr/bin/env python3
"""Distinct IC20 phase action with v=v0, NOT v0+z².

Keep every other covariant term; choose explicit A,D,E4 below.
No IC26 background or stability verdict is imported.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
from scipy.integrate import DOP853
import ic20_joint_completion as old
import ic24_potential as matter
from ic25_coupled import hamiltonian_generator as generator
from ic27_observables import constraint_fields


def identities():
    S,q,z,R,wc,A,D,E4,P=s.symbols('S q z R wc A D E4 P',real=True)
    v=s.exp(S+2*wc)/2;t=s.exp(2*S)/v
    h=-t*q*q/6-A*q*z-s.exp(S)*P-D*z*z-E4*z**4-v*R
    zz=s.diff(h,z,2)
    def H(i,j):return s.diff(h,i,j)-s.diff(h,i,z)*s.diff(h,j,z)/zz
    a=t/6+H(q,q)/2
    u=s.symbols('u',real=True);B=2*v*(1-u*u)
    cg=(-2*a*v+4*a*H(S,R)**2/B)/s.exp(2*S)
    return dict(tensor_cone=s.simplify(-t*s.diff(h,R)-s.exp(2*S)),
        physical_tensor_coupling=s.simplify(2*s.exp(S-2*wc)/t-1),
        joint_compatibility=s.factor((H(q,q)+t/3)*H(R,R)-H(q,R)**2),
        scalar_kinetic=s.factor(a-A*A/(4*D+24*E4*z*z)),
        no_momentum_curvature_mix=s.factor(H(q,R)),
        no_curvature_square=s.factor(H(R,R)),
        lapse_curvature=s.simplify(H(S,R)+v),
        positive_principal_formula=s.factor(cg-2*a*v*u*u/(s.exp(2*S)*(1-u*u))),
        static_value=s.simplify(h.subs({q:0,z:0})+s.exp(S)*P+v*R))


@lru_cache(None)
def build():
    S,q,z,R,wc=s.symbols('S q z R wc',real=True)
    funcs=[s.Function(name)(S) for name in ('A','D','E4','P')]
    A,D,E4,P=funcs;v=s.exp(S+2*wc)/2
    h=-s.exp(2*S)*q*q/(6*v)-A*q*z-s.exp(S)*P-D*z*z-E4*z**4-v*R
    keys=['h','S','q','z','R','SS','Sq','Sz','SR','qq','qz','qR','zz','zR','RR']
    variables={'S':S,'q':q,'z':z,'R':R}
    expressions=[h]+[s.diff(h,*[variables[c] for c in key]) for key in keys[1:]]
    symbols=[];mapping={}
    for i,fn in enumerate(funcs):
        for order in range(3):
            sym=s.Symbol('j%d_%d'%(i,order));symbols.append(sym);mapping[s.diff(fn,S,order)]=sym
    expressions=[x.subs(mapping,simultaneous=True) for x in expressions]
    return keys,s.lambdify((S,q,z,R,wc,*symbols),expressions,'mpmath',cse=True)


def raw(S,q,z,jets):
    c=old.normalized.constants()
    if S<=-2*c['wc']:raise ValueError('Outside pinned chart')
    def P(x):return old.normalized.legacy.original_pressure()(x,c['wc'],c['Lambda'],c['a02'])
    p,ps=P(S);pss=mp.diff(lambda x:P(x)[1],S)
    keys,fn=build()
    return dict(zip(keys,fn(S,q,z,0,c['wc'],*jets['a'],*jets['d'],*jets['e'],p,ps,pss)))


def fixed(S,q,z,Q,jets,fluids,parameters=None):
    r=raw(S,q,z,jets);entries=matter.matter(S,Q,fluids)
    rho=mp.fsum(x['h'] for x in entries);pressure=mp.fsum(x['w']*x['h'] for x in entries)
    HQ=r['q']/2;qd=-mp.mpf('1.5')*(r['h']-pressure)
    F=mp.matrix([r['S']+rho,r['z']])
    matrix=mp.matrix([[r['SS']+rho,r['Sz']],[r['Sz'],r['zz']]])
    source=mp.matrix([3*HQ*F[0]+r['Sq']*qd-3*HQ*(rho+pressure),3*HQ*F[1]+r['qz']*qd])
    sd,zd=mp.lu_solve(matrix,-source)
    red={key:r[key]-r[az]*r[bz]/r['zz'] for key,az,bz in
         [('SS','Sz','Sz'),('Sq','Sz','qz'),('SR','Sz','zR'),('qq','qz','qz'),('qR','qz','zR'),('RR','zR','zR')]}
    wc=old.normalized.constants()['wc'];v=mp.exp(S+2*wc)/2;t=mp.exp(2*S)/v
    u=(S+2*wc)/(S+wc);B=2*v*(1-u*u);a=t/6+red['qq']/2
    # d=H_qR is identically zero in this action, including its time derivative.
    cg=(-2*a*v+4*a*red['SR']**2/B)/mp.exp(2*S)
    symbol=mp.diag([cg]+[2*x['beta']*x['j']/x['u'] for x in entries])
    return dict(S=S,q=q,z=z,Q=Q,raw=r,red=red,jets=jets,entries=entries,fluids=fluids,
        flow=mp.matrix([sd,qd,zd]),Qdot=HQ,M=red['SS']+rho,t=t,v=v,B=B,a=a,d=red['qR'],
        H_physical=mp.exp(-S-wc)*HQ,charge=mp.exp(3*Q)*(r['h']+rho),
        constraints=list(F),preservation=list(matrix*mp.matrix([sd,zd])+source),
        parameters=parameters,principal=dict(symbol=symbol,gravity_diagonal=cg))


def coefficient_jets(S,p):
    x=S-p['S0'];D=p['D0']*mp.exp(p['d1']*x+p['d2']*x*x/2)
    slope=p['d1']+p['d2']*x
    return dict(a=[p['A0'],0,0],e=[p['E40'],0,0],
                d=[D,D*slope,D*(slope*slope+p['d2'])])


def witness(target_M='-3'):
    S,q,z,Q=map(mp.mpf,('.1','-3','1','0'))
    fluids=[dict(w=mp.mpf(1)/3,c=mp.mpf(3)/4,amplitude=mp.mpf('1e-6')),
            dict(w=mp.mpf('1e-8'),c=mp.mpf(1),amplitude=mp.mpf('1e-6'))]
    jets=dict(a=[mp.mpf('.1'),0,0],e=[mp.mpf('.01'),0,0],d=[0,0,0])
    jets['d'][0]=raw(S,q,z,jets)['z']/(2*z)
    rho=mp.fsum(x['h'] for x in matter.matter(S,Q,fluids))
    jets['d'][1]=(raw(S,q,z,jets)['S']+rho)/(z*z)
    r=raw(S,q,z,jets)
    jets['d'][2]=(r['SS']+rho-r['Sz']**2/r['zz']-mp.mpf(target_M))/(z*z)
    D0,D1,D2=jets['d']
    p=dict(S0=S,A0=jets['a'][0],E40=jets['e'][0],D0=D0,d1=D1/D0,d2=D2/D0-(D1/D0)**2)
    return fixed(S,q,z,Q,coefficient_jets(S,p),fluids,p)


def physical_fields(b,k_squared,phase):
    r=constraint_fields(b,k_squared,phase);dot=generator(b,k_squared)*mp.matrix(phase)
    sd=b['flow'][0];HQ=b['Qdot'];k2=mp.mpf(k_squared)
    sourcedot=dot[3]-mp.mpf('1.5')*mp.fsum(
        f['j']*(dot[i+1]-3*HQ*phase[i+1]) for i,f in enumerate(b['entries']))
    # Actual t=2exp(S-2wc), so tdot/t=Sdot, with no z contribution.
    chidot=(sd+2*HQ)*r['chi']-b['t']*sourcedot/(2*k2)
    r['Phi']=r['delta_S']+mp.exp(-2*b['S'])*(chidot-sd*r['chi'])
    r['Psi']=-phase[0]-mp.exp(-2*b['S'])*HQ*r['chi']
    return r


def integrated_state(S,q,z,Q,fluids,p,target_M='-3'):
    if z<=0:raise ValueError('Integrated D chart requires z>0; no jump across its zero-field boundary')
    jets=dict(a=[p['A0'],0,0],e=[p['E40'],0,0],d=[0,0,0])
    jets['d'][0]=raw(S,q,z,jets)['z']/(2*z)
    rho=mp.fsum(x['h'] for x in matter.matter(S,Q,fluids))
    jets['d'][1]=(raw(S,q,z,jets)['S']+rho)/(z*z)
    r=raw(S,q,z,jets)
    jets['d'][2]=(r['SS']+rho-r['Sz']**2/r['zz']-mp.mpf(target_M))/(z*z)
    result=fixed(S,q,z,Q,jets,fluids,p)
    result.update(profile='integrated',target_M=mp.mpf(target_M))
    return result


def construction_along(b,dt):
    S,q,z=[b[key]+dt*b['flow'][i] for i,key in enumerate(('S','q','z'))]
    return integrated_state(S,q,z,b['Q']+dt*b['Qdot'],b['fluids'],b['parameters'],b['target_M'])


def integrability(b):
    return dict(Ddot=mp.diff(lambda dt:construction_along(b,dt)['jets']['d'][0],0)-b['jets']['d'][1]*b['flow'][0],
                Dprime_dot=mp.diff(lambda dt:construction_along(b,dt)['jets']['d'][1],0)-b['jets']['d'][2]*b['flow'][0],
                charge_dot=mp.diff(lambda dt:construction_along(b,dt)['charge'],0))


def along(b,dt):
    S,q,z=[b[key]+dt*b['flow'][i] for i,key in enumerate(('S','q','z'))]
    if b.get('profile')=='integrated':
        if b['flow'][0]==0:raise ValueError('Stationary clock chart requires separate continuation')
        d3=mp.diff(lambda eps:construction_along(b,eps)['jets']['d'][2],0)/b['flow'][0]
        d0,d1,d2=b['jets']['d'];ds=S-b['S']
        jets=dict(a=b['jets']['a'],e=b['jets']['e'],
            d=[d0+d1*ds+d2*ds*ds/2+d3*ds**3/6,d1+d2*ds+d3*ds*ds/2,d2+d3*ds])
        return fixed(S,q,z,b['Q']+dt*b['Qdot'],jets,b['fluids'],b['parameters'])
    return fixed(S,q,z,b['Q']+dt*b['Qdot'],
                 coefficient_jets(S,b['parameters']),b['fluids'],b['parameters'])


def frequencies(b,k_squared):
    k2=mp.mpf(k_squared);quad=matter.quadratic(b,k2);n=3
    def moved_quad(dt):
        return matter.quadratic(along(b,dt),k2*mp.exp(-2*b['Qdot']*dt))
    Ad=mp.matrix([[mp.diff(lambda dt:moved_quad(dt)['A'][i,j],0) for j in range(n)] for i in range(n)])
    Bd=mp.matrix([[mp.diff(lambda dt:moved_quad(dt)['B'][i,j],0) for j in range(n)] for i in range(n)])
    A,B=quad['A'],quad['B']
    damping=A**-1*(Ad+3*b['Qdot']*A+B-B.T)
    restoring=A**-1*(Bd+3*b['Qdot']*B+quad['potential'])
    G=mp.zeros(6)
    for i in range(3):
        G[i,i+3]=1
        for j in range(3):
            G[i+3,j]=-restoring[i,j];G[i+3,j+3]=-damping[i,j]
    roots,vec=mp.eig(G,left=False,right=True)
    residual=max(mp.norm(G*vec[:,i]-roots[i]*vec[:,i])/max(1,mp.norm(G)*mp.norm(vec[:,i])) for i in range(6))
    return dict(roots=roots,residual=residual,
                nonclaim='Instantaneous full Euler roots, not a cosmological growth history')


def evolve(target_Q=.1,max_step=.0001,max_steps=2000,profile='exponential'):
    with mp.workdps(30):
        b=witness();p=b['parameters'];fluids=b['fluids']
        def point(Q,y):
            S,q,z=map(mp.mpf,y)
            if profile=='integrated':
                return integrated_state(S,q,z,mp.mpf(Q),fluids,p)
            return fixed(S,q,z,mp.mpf(Q),coefficient_jets(S,p),fluids,p)
        def rhs(Q,y):
            r=point(Q,y)
            return [float(x/r['Qdot']) for x in r['flow']]
        solver=DOP853(rhs,0,[float(b[x]) for x in ('S','q','z')],target_Q,
                      rtol=1e-11,atol=1e-13,max_step=max_step)
        rows=[b];reason='requested endpoint reached';success=True
        for _ in range(max_steps):
            if solver.status!='running':break
            try:
                if profile=='integrated':
                    current=rows[-1]
                    if current['z']<=mp.mpf('1e-6'):
                        success=False;reason='positive-z diagnostic floor reached (not a continued zero-field solution)';break
                    rate=abs(current['flow'][2]/current['Qdot'])
                    if rate:
                        solver.max_step=min(max_step,float(current['z']/(4*rate)))
                solver.step()
                if solver.status=='failed':success=False;reason='adaptive integrator failed';break
                r=point(solver.t,solver.y);rows.append(r)
                cg=r['principal']['gravity_diagonal']
                if min(r['H_physical'],r['a'],-r['M'],-r['raw']['zz'],cg,1-cg)<=0:
                    success=False;reason='accepted state violates local regular/causal conditions';break
            except (ValueError,ZeroDivisionError) as error:
                success=False;reason='unaccepted integration stage: '+str(error);break
        else:success=False;reason='step bound exhausted'
        def snapshot(r):
            return {**{x:float(r[x]) for x in ('Q','S','q','z','M','a','H_physical')},
                'cg2':float(r['principal']['gravity_diagonal']),
                'D_jets':[float(x) for x in r['jets']['d']],
                'charge':float(r['charge']),
                'constraint_residual':float(max(abs(x) for x in r['constraints']))}
        return dict(success=success,reason=reason,Q_end=float(rows[-1]['Q']),
            requested_Q=target_Q,profile=profile,states=[snapshot(r) for r in rows],nfev=solver.nfev,
            maximum_charge_drift=float(max(abs(r['charge']-b['charge']) for r in rows)),
            maximum_constraint_residual=float(max(abs(x) for r in rows for x in r['constraints'])))


def report():
    with mp.workdps(50):
        b=witness();rows=[]
        for k in (0,mp.mpf('.001'),1,100,10**12):
            quad=matter.quadratic(b,k)
            rows.append(dict(k_squared=k,brackets=matter.brackets(b,k),
                kinetic_eigenvalues=list(mp.eigsy(quad['A'],eigvals_only=True)),
                slip_basis=[] if k==0 else [physical_fields(b,k,mp.eye(6)[:,i])['Phi']
                    -physical_fields(b,k,mp.eye(6)[:,i])['Psi'] for i in range(6)]))
        exact=identities()
        history=evolve();refined=evolve(max_step=.00005)
        integrated=evolve(target_Q=1,max_step=.005,profile='integrated')
        integrated_fine=evolve(target_Q=1,max_step=.0025,profile='integrated')
        ib=integrated_state(b['S'],b['q'],b['z'],b['Q'],b['fluids'],b['parameters'])
        integral_residuals=integrability(ib)
        spectra=[dict(k_squared=k,**frequencies(b,k)) for k in (mp.mpf('.001'),mp.mpf('.1'),1,100,10**14)]
        integrated_spectra=[dict(k_squared=k,**frequencies(ib,k)) for k in (mp.mpf('.001'),mp.mpf('.1'),1,100,10**14)]
        checks=dict(exact_identities=all(x==0 for x in exact.values()),
            varied_constraints=max(abs(x) for x in b['constraints']+b['preservation'])<mp.mpf('1e-35'),
            expanding=b['H_physical']>0,
            positive_kinetics=all(min(x['kinetic_eigenvalues'])>0 for x in rows),
            auxiliary_no_pole=b['M']<0 and b['B']>0 and b['raw']['zz']<0,
            causal_principal=all(0<x<1 for x in mp.eig(b['principal']['symbol'],left=False,right=False)),
            independent_no_slip=all(abs(x)<mp.mpf('1e-30') for r in rows for x in r['slip_basis']),
            eigen_residuals=all(x['residual']<mp.mpf('1e-30') for x in spectra+integrated_spectra),
            integrated_jets=max(abs(x) for x in integral_residuals.values())<mp.mpf('1e-30'))
        return dict(full_theory='OPEN',checks=checks,identities={k:str(v) for k,v in exact.items()},
            witness=b,rows=rows,spectra=spectra,history=history,refined_history=refined,
            integrated_history=integrated,integrated_refined_history=integrated_fine,
            integrated_jet_residuals=integral_residuals,integrated_initial_spectra=integrated_spectra,
            nonclaims=['Distinct action from IC26; no inherited evolution, static/PPN or full nonlinear closure',
                'Coefficient functions are explicit; bounded history diagnostics are not viable long cosmology',
                'Positive principal speeds do not establish finite-wavelength or nonlinear stability',
                'Static-value agreement at q=z=0 is not the full static variation or pin-off constraint count'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--require-full-closure',action='store_true');args=p.parse_args()
    out=report();print(json.dumps(out,default=matter.serial,indent=2))
    raise SystemExit(1 if not all(out['checks'].values()) else 2 if args.require_full_closure else 0)
