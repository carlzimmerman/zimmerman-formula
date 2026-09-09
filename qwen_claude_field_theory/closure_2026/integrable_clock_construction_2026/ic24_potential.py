#!/usr/bin/env python3
"""Reconstruct ONE local D(S) coefficient by a constrained mixed FLRW IVP.

Algebraic reconstruction selects action jets; partial variations keep those
jets fixed as derivatives of S only. No global/static completion is implied.
"""
import argparse
import json
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
import ic20_joint_completion as model
import ic23_mixture as mixture


def initial():
    return mixture.background()


def matter(S,Q,fluids):
    entries=[]
    for f in fluids:
        w,c,M=f['w'],f['c'],f['amplitude']
        j=(M/c)**(1/(1+w))*mp.exp(-3*Q)
        h=mp.exp(S)*c*j**(1+w);u=(1+w)*h/j
        entries.append(dict(**f,j=j,h=h,u=u,beta=w*u/(2*j)))
    return entries


def fixed_state(S,q,z,Q,parameters,fluids,jets):
    """Vary raw action with supplied S-only coefficient jets."""
    r=model.raw_jets(S,q,z,0,jets);entries=matter(S,Q,fluids)
    total=mp.fsum(f['h'] for f in entries)
    pressure=mp.fsum(f['w']*f['h'] for f in entries)
    Qdot=r['q']/2;qdot=-mp.mpf(3)/2*(r['h']-pressure)
    F=mp.matrix([r['S']+total,r['z']])
    A=mp.matrix([[r['SS']+total,r['Sz']],[r['Sz'],r['zz']]])
    source=mp.matrix([3*Qdot*F[0]+r['Sq']*qdot-3*Qdot*(total+pressure),
                      3*Qdot*F[1]+r['qz']*qdot])
    sd,zd=mp.lu_solve(A,-source)
    wc=model.normalized.constants()['wc'];E=mp.exp(2*S)
    v0=mp.exp(S+2*wc)/2;v=v0+z*z;t=E/v
    u=(S+2*wc)/(S+wc);B=2*v0*(1-u*u)
    red={key:r[key]-r[az]*r[bz]/r['zz'] for key,az,bz in
         [('SS','Sz','Sz'),('Sq','Sz','qz'),('SR','Sz','zR'),
          ('qq','qz','qz'),('qR','qz','zR'),('RR','zR','zR')]}
    a=t/6+red['qq']/2;d=red['qR'];p=r['qz']
    pS=2*E*q*z/(3*v*v)*(2-2*v0/v)-jets['a'][1]
    pq=2*E*z/(3*v*v);pz=2*E*q/(3*v*v)*(1-4*z*z/v)
    ratio=-4*z/p
    ratio_dot=-4*zd/p+4*z*(pS*sd+pq*qdot+pz*zd)/p**2
    cg=(-2*a*v+4*a*(red['SR']-red['Sq']*d/(2*a))**2/B)/E-2*a*(ratio_dot+Qdot*ratio)/E
    symbol=mp.zeros(1+len(entries));symbol[0,0]=cg;mix=[]
    for i,f in enumerate(entries,1):
        symbol[i,i]=2*f['beta']*f['j']/f['u']
        symbol[0,i]=d*t*f['j']/(2*E)
        symbol[i,0]=2*f['beta']*d*t*f['j']/(a*E)
        mix.append(symbol[0,i]*symbol[i,0])
    principal=dict(symbol=symbol,gravity_diagonal=cg,
        gradient_margin=cg-mp.fsum(J/f['w'] for J,f in zip(mix,entries)),
        lightcone_margin=1-cg-mp.fsum(J/(1-f['w']) for J,f in zip(mix,entries)))
    return dict(S=S,q=q,z=z,Q=Q,parameters=parameters,fluids=fluids,jets=jets,
        raw=r,red=red,entries=entries,flow=mp.matrix([sd,qdot,zd]),Qdot=Qdot,
        M=A[0,0]-A[0,1]**2/A[1,1],constraints=list(F),preservation=list(A*mp.matrix([sd,zd])+source),
        charge=mp.exp(3*Q)*(r['h']+total),H_physical=mp.exp(-S-wc)*Qdot,
        a=a,d=d,v=v,t=t,B=B,principal=principal)


def reconstruct(S,q,z,Q,parameters,fluids,target_M='-3'):
    S,q,z,Q=map(mp.mpf,(S,q,z,Q));target_M=mp.mpf(target_M)
    if z<=0 or target_M>=0:raise ValueError('Require z>0 and negative target Schur')
    jets=model.coefficient_jets(S,parameters);jets['d']=[mp.mpf(0)]*3
    r=model.raw_jets(S,q,z,0,jets);jets['d'][0]=r['z']/(2*z)
    r=model.raw_jets(S,q,z,0,jets)
    total=mp.fsum(f['h'] for f in matter(S,Q,fluids))
    jets['d'][1]=(r['S']+total)/(z*z)
    r=model.raw_jets(S,q,z,0,jets)
    jets['d'][2]=(r['SS']+total-r['Sz']**2/r['zz']-target_M)/(z*z)
    b=fixed_state(S,q,z,Q,parameters,fluids,jets);b['target_M']=target_M
    return b


def integrability(b):
    """Differentiate algebraic reconstruction along its actual varied flow."""
    def moved(dt):
        vals=[b[x]+dt*b['flow'][i] for i,x in enumerate(('S','q','z'))]
        return reconstruct(*vals,b['Q']+dt*b['Qdot'],b['parameters'],b['fluids'],b['target_M'])
    return {'D_dot_minus_Dprime_Sdot':mp.diff(lambda dt:moved(dt)['jets']['d'][0],0)-b['jets']['d'][1]*b['flow'][0],
            'Dprime_dot_minus_Dsecond_Sdot':mp.diff(lambda dt:moved(dt)['jets']['d'][1],0)-b['jets']['d'][2]*b['flow'][0],
            'charge_dot':mp.diff(lambda dt:moved(dt)['charge'],0)}


def snapshot(b):
    values=mp.eig(b['principal']['symbol'],left=False,right=False)
    return dict(Q=float(b['Q']),S=float(b['S']),q=float(b['q']),z=float(b['z']),
        D_jets=[float(x) for x in b['jets']['d']],Sdot=float(b['flow'][0]),
        charge=float(b['charge']),M=float(b['M']),hzz=float(b['raw']['zz']),
        H=float(b['H_physical']),a=float(b['a']),
        speeds_squared=[float(mp.re(x)) for x in values],
        maximum_imaginary=float(max(abs(mp.im(x)) for x in values)),
        gradient_margin=float(b['principal']['gradient_margin']),
        lightcone_margin=float(b['principal']['lightcone_margin']))


def quadratic(b,k_squared):
    k2=mp.mpf(k_squared);r=b['red'];entries=b['entries'];n=1+len(entries)
    total=mp.fsum(f['h'] for f in entries)
    Z=4*r['SR']*k2-3*mp.fsum((1+f['w'])*f['h'] for f in entries)
    M=r['SS']+total-2*b['B']*k2
    K=mp.diag([b['a']]+[f['beta'] for f in entries]);L=mp.zeros(n);W=mp.zeros(n)
    L[0,0]=2*r['qR']*k2
    W[0,0]=-2*b['v']*k2+8*r['RR']*k2*k2+mp.mpf(9)/2*mp.fsum(f['w']*(1+f['w'])*f['h'] for f in entries)
    for i,f in enumerate(entries,1):
        L[0,i]=-b['t']*f['j']/4;L[i,0]=-3*f['w']*f['u']/2
        for j,h in enumerate(entries,1):W[i,j]=3*b['t']*f['j']*h['j']/8
        W[i,i]+=mp.exp(2*b['S'])*f['j']*k2/(2*f['u'])
    f=mp.matrix([r['Sq']]+[x['u'] for x in entries]);g=mp.matrix([Z]+[0]*len(entries))
    K-=f*f.T/(2*M);L-=f*g.T/(2*M);W-=g*g.T/(2*M)
    D=mp.diag([2]+[1]*len(entries));inverse=K**-1
    return dict(K=K,L=L,W=W,A=D*inverse*D/2,B=-D*inverse*L,potential=2*(W-L.T*inverse*L),M=M)


def third_jet(b):
    if b['flow'][0]==0:raise ValueError('D third derivative undefined at stationary S without compatibility')
    def second(dt):
        vals=[b[x]+dt*b['flow'][i] for i,x in enumerate(('S','q','z'))]
        return reconstruct(*vals,b['Q']+dt*b['Qdot'],b['parameters'],b['fluids'],b['target_M'])['jets']['d'][2]
    return mp.diff(second,0)/b['flow'][0]


def frequencies(b,k_squared):
    """Full quadratic Euler matrix; off-shell D depends ONLY on S.

    Three Taylor jets plus the IVP-derived third derivative suffice for first
    time derivatives of the quadratic coefficients. No off-shell algebraic
    D(S,q,z,Q) substitution is allowed here.
    """
    k2=mp.mpf(k_squared);base=quadratic(b,k2);n=base['A'].rows
    d3=third_jet(b);d0,d1,d2=b['jets']['d']
    def moved(dt):
        S,q,z=[b[x]+dt*b['flow'][i] for i,x in enumerate(('S','q','z'))]
        ds=S-b['S'];jets=model.coefficient_jets(S,b['parameters'])
        jets['d']=[d0+d1*ds+d2*ds**2/2+d3*ds**3/6,d1+d2*ds+d3*ds**2/2,d2+d3*ds]
        row=fixed_state(S,q,z,b['Q']+dt*b['Qdot'],b['parameters'],b['fluids'],jets)
        return quadratic(row,k2*mp.exp(-2*b['Qdot']*dt))
    Adot=mp.matrix([[mp.diff(lambda dt:moved(dt)['A'][i,j],0) for j in range(n)] for i in range(n)])
    Bdot=mp.matrix([[mp.diff(lambda dt:moved(dt)['B'][i,j],0) for j in range(n)] for i in range(n)])
    A,B=base['A'],base['B'];inverse=A**-1
    damping=inverse*(Adot+3*b['Qdot']*A+B-B.T)
    restoring=inverse*(Bdot+3*b['Qdot']*B+base['potential'])
    gen=mp.zeros(2*n)
    for i in range(n):
        gen[i,i+n]=1
        for j in range(n):gen[i+n,j]=-restoring[i,j];gen[i+n,j+n]=-damping[i,j]
    roots,vec=mp.eig(gen,left=False,right=True)
    residual=max(mp.norm(gen*vec[:,i]-roots[i]*vec[:,i])/max(1,mp.norm(gen)*mp.norm(vec[:,i])) for i in range(2*n))
    return dict(k_squared=k2,roots=roots,residual=residual,D_third=d3,
                kinetic_eigenvalues=list(mp.eigsy(A,eigvals_only=True)))


def brackets(b,k_squared):
    k2=mp.mpf(k_squared);r=b['raw']
    total=mp.fsum(f['h'] for f in b['entries']);pressure=mp.fsum(f['w']*f['h'] for f in b['entries'])
    A=mp.matrix([[r['SS']+total-2*b['B']*k2,r['Sz']],[r['Sz'],r['zz']]])
    fQ=[3*r['S']-3*b['q']*r['Sq']+4*k2*r['SR']-3*pressure,
        3*r['z']-3*b['q']*r['qz']+4*k2*r['zR']]
    fp=[r['Sq'],r['qz']];pb=mp.zeros(4)
    for i in range(2):
        for j in range(2):
            pb[i,j+2]=-A[i,j];pb[i+2,j]=A[i,j]
            pb[i+2,j+2]=(fQ[i]*fp[j]-fp[i]*fQ[j])/2
    singular=list(mp.svd(pb,compute_uv=False));threshold=max(singular)*mp.power(10,-mp.mp.dps/2)
    return dict(matrix=pb,determinant=mp.det(pb),singular_values=singular,
                rank=sum(x>threshold for x in singular),threshold=threshold)


def evolve(target_Q=.01,rtol=1e-10,max_step=.0002,target_M='-3'):
    """Bounded DOP853 integration; rejects first sampled physical/chart failure.

    Dense-output samples are numerical evidence, not an interval proof.
    """
    with mp.workdps(30):
        b=initial();p,fluids=b['parameters'],b['fluids']
        def row(Q,y):return reconstruct(*y,Q,p,fluids,target_M)
        def rhs(Q,y):
            r=row(Q,y)
            return [float(x/r['Qdot']) for x in r['flow']]
        def health(Q,y):
            r=row(Q,y)
            return float(min(r['principal']['gradient_margin'],r['principal']['lightcone_margin'],
                -r['raw']['zz'],-r['M'],r['a'],r['H_physical'],r['jets']['d'][0],r['flow'][0]))
        health.terminal=True;health.direction=-1
        y0=[float(b[x]) for x in ('S','q','z')]
        sol=solve_ivp(rhs,(0,float(target_Q)),y0,method='DOP853',rtol=rtol,atol=rtol*.001,
                      max_step=max_step,dense_output=True,events=health)
        times=np.unique(np.concatenate((sol.t,np.linspace(0,sol.t[-1],101))))
        rows=[row(Q,sol.sol(Q)) for Q in times];states=[snapshot(r) for r in rows]
        c0=rows[0]['charge']
        ids=[0,len(rows)//2,len(rows)-1]
        errors=[{k:float(v) for k,v in integrability(rows[i]).items()} for i in ids]
        return dict(solver_success=bool(sol.success),solver_message=sol.message,nfev=sol.nfev,
            requested_Q=float(target_Q),rtol=rtol,max_step=max_step,states=states,
            maximum_charge_drift=float(max(abs(r['charge']-c0) for r in rows)),
            minimum_gradient_margin=min(x['gradient_margin'] for x in states),
            minimum_lightcone_margin=min(x['lightcone_margin'] for x in states),
            minimum_Sdot=min(x['Sdot'] for x in states),integrability_samples=errors,
            event_times=[list(x) for x in sol.t_events])


def report():
    history=evolve(.1);refined=evolve(.1,rtol=1e-12,max_step=.0001)
    points=[]
    with mp.workdps(65):
        b=initial()
        for Q in (0,.005,.02,.04):
            if Q==0:S,q,z=b['S'],b['q'],b['z']
            else:
                end=evolve(Q,rtol=1e-12,max_step=.0001)['states'][-1]
                S,q,z=map(mp.mpf,(end['S'],end['q'],end['z']))
            row=reconstruct(S,q,z,mp.mpf(Q),b['parameters'],b['fluids'])
            points.append(dict(state=snapshot(row),integrability=integrability(row),
                spectra=[frequencies(row,k2) for k2 in (1,100,1000000,10**14)],
                brackets=[brackets(row,k2) for k2 in (0,1,10000)]))
    checks=dict(integrability=max(abs(x) for p in points for x in p['integrability'].values())<mp.mpf('1e-45'),
        charge_conserved=history['maximum_charge_drift']<1e-9,
        extended_past_old_crossing=history['states'][-1]['Q']>.04,
        event_step_convergence=abs(history['states'][-1]['Q']-refined['states'][-1]['Q'])<1e-8,
        sampled_auxiliaries_regular=all(x['rank']==4 for p in points for x in p['brackets']),
        sampled_kinetic_positive=all(min(f['kinetic_eigenvalues'])>0 for p in points for f in p['spectra']),
        eigen_residuals=all(f['residual']<mp.mpf('1e-40') for p in points for f in p['spectra']))
    return dict(full_theory='OPEN',checks=checks,history=history,refined_history=refined,points=points,
        nonclaims=['Finite sampled trajectory, not interval-certified stability',
          'Endpoint reaches light cone; requested Q=.1 not reached',
          'No static extension, full nonlinear Dirac, relative-flow, PPN, recombination or empirical closure',
          'Finite-k roots are instantaneous; growth histories and strong coupling unproved'])


def serial(x):
    if isinstance(x,mp.matrix):return x.tolist()
    if isinstance(x,mp.mpc):return dict(real=mp.nstr(x.real,35),imag=mp.nstr(x.imag,35))
    if isinstance(x,mp.mpf):return mp.nstr(x,35)
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--require-full-closure',action='store_true');args=parser.parse_args()
    result=report();print(json.dumps(result,default=serial,indent=2))
    raise SystemExit(1 if not all(result['checks'].values()) else 2 if args.require_full_closure else 0)
