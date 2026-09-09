"""Periodic plane-symmetric evolution of the same IC29/30 clock action.

A homogeneous anisotropy is retained, not discarded as a k=0 gauge mode.
Only elliptic/algebraic auxiliaries are solved at stages; momentum is NOT projected.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import numpy as np
import sympy as s
import ic30_radial_bridge as radial
import ic32_constraint_preservation as old


@lru_cache(None)
def build():
    d=radial.radial_action(); x=d['r']
    S,w,Q,q,z,sh,beta,ell=d['fields']
    a,b=(s.Function(n)(x) for n in ('aplane','bplane'))
    ad,bd,sd,Xi,Xd=s.symbols('ad bd shdot Xi Xidot',real=True)
    Qd,qd=d['Qdot'],d['qdot']; v=d['v']; t=d['t']
    J=s.exp(a+2*b)
    kinetic=2*(q+2*sh)*ad/3+4*(q-sh)*bd/3
    L0=kinetic-2*t*sh**2/3+t*q**2/6+d['A']*q*z+s.exp(S)*d['P0']+d['D']*z**2+d['E4']*z**4
    L0+=d['eta']*s.exp(S)*ell*(w-d['wc'])
    L0-=2*(q+2*sh)*(s.diff(beta,x)+beta*s.diff(a,x))/3
    L0-=4*(q-sh)*beta*s.diff(b,x)/3
    mixed=2*d['u']*d['xi']*s.diff(d['xi'],x)*s.diff(d['u'],x)+d['xi']**2*s.diff(d['u'],x)**2
    # Curvature integrated by parts; boundary term checked below.
    L=J*L0+s.exp(-a+2*b)*(2*v*s.diff(b,x)**2+4*s.diff(v,x)*s.diff(b,x)+2*v*mixed)
    Ea=radial.euler(L,a,x)-2*J*(qd+2*sd+(ad+2*bd)*(q+2*sh))/3
    Eb=radial.euler(L,b,x)-4*J*(qd-sd+(ad+2*bd)*(q-sh))/3
    def chart(expr):
        return s.simplify(expr.subs({a:Q+2*Xi/3,b:Q-Xi/3,ad:Qd+2*Xd/3,bd:Qd-Xd/3},simultaneous=True).doit())
    def pin(expr):
        return s.simplify(expr.subs(d['eta'],1).doit().subs(w,d['wc']).doit())
    def cp(expr):return pin(chart(expr))
    C=cp(-radial.euler(L,S,x)/J)
    W=cp(radial.euler(L,w,x)/J).subs(ell,0)
    vp=v.subs(w,d['wc']); tp=t.subs(w,d['wc'])
    B=2*vp*(1-d['u'].subs(w,d['wc'])**2)
    h=-tp*q*q/6-d['A']*q*z-s.exp(S)*d['P0'].subs(w,d['wc'])-d['D']*z*z-d['E4']*z**4
    HQ=s.diff(h,q)/2
    Qflow=HQ+beta*s.diff(Q,x)+s.diff(beta,x)/3
    Xflow=s.diff(beta,x)+tp*sh
    ea,eb=cp(Ea/J),cp(Eb/J)
    flowq=s.simplify(((ea+eb)/2).subs({qd:0,sd:0,Qd:Qflow,Xd:Xflow}))
    flows=s.simplify(((2*ea-eb)/4).subs({qd:0,sd:0,Qd:Qflow,Xd:Xflow}))
    Q1,Q2=s.diff(Q,x),s.diff(Q,x,2); S1,S2=s.diff(S,x),s.diff(S,x,2)
    metric=s.exp(-2*Q-4*Xi/3)
    cq=-3*h/2+tp*sh**2+beta*s.diff(q,x)+metric*(-2*vp*Q1**2-4*vp*S1*Q1
        +(B-4*vp)*S1**2-4*vp*(Q2+S2))/2
    cs=beta*s.diff(sh,x)-3*HQ*sh+metric*(vp*(Q2+S2-Q1**2-2*Q1*S1)+(vp-B)*S1**2)
    predictedC=s.diff(h,S)+2*tp*sh**2/3+metric*(4*vp*Q2+2*vp*Q1**2+2*B*Q1*S1
        +2*B*S2+s.diff(B,S)*S1**2)
    R=s.exp(-2*a)*(-4*s.diff(b,x,2)-6*s.diff(b,x)**2+4*s.diff(a,x)*s.diff(b,x))
    raw=J*v*R
    ibp=s.exp(-a+2*b)*(2*v*s.diff(b,x)**2+4*s.diff(v,x)*s.diff(b,x))
    checks={
        'curvature_boundary':s.simplify(raw-ibp+s.diff(4*s.exp(-a+2*b)*v*s.diff(b,x),x)),
        'Q_euler':s.simplify(cp(radial.euler(L,q,x)/J).subs(Qd,Qflow)),
        'anisotropy_gauge':s.simplify(cp(radial.euler(L,sh,x)/J).subs(Xd,Xflow)),
        'trace_evolution':s.simplify(flowq-cq),
        'tracefree_evolution':s.simplify(flows-cs),
        'lapse':s.simplify(C-predictedC),
        'momentum':s.simplify(cp(radial.euler(L,beta,x)/J)
                             -2*s.diff(q,x)/3-4*s.diff(sh,x)/3-4*Q1*sh)}
    hSz=s.diff(h,S,z); hzz=s.diff(h,z,2)
    expressions=dict(C=C,W=W,CS=s.diff(C,S)-s.diff(C,z)*hSz/hzz,
                     CS1=s.diff(C,S1),CS2=s.diff(C,S2),
                     Qdot=Qflow,qdot=flowq,shdot=flows)
    jets=(S,S1,S2,Q,Q1,Q2,q,s.diff(q,x),z,sh,s.diff(sh,x),beta,s.diff(beta,x))
    symbols=s.symbols('Sv S1 S2 Qv Q1 Q2 qv q1 zv shv sh1 bv b1',real=True)
    A,D,D1,D2,E=s.symbols('A D D1 D2 E',real=True)
    sub={d['A']:A,s.diff(d['A'],S):0,s.diff(d['A'],S,2):0,
         d['D']:D,s.diff(d['D'],S):D1,s.diff(d['D'],S,2):D2,
         d['E4']:E,s.diff(d['E4'],S):0,s.diff(d['E4'],S,2):0}
    values=[s.simplify(v.subs(sub,simultaneous=True).subs(dict(zip(jets,symbols)),simultaneous=True))
            for v in expressions.values()]
    args=(*symbols,Xi,d['wc'],d['m'],d['a02'],d['lam'],d['kappa'],A,D,D1,D2,E)
    return checks,list(expressions),s.lambdify(args,values,'numpy',cse=True)


def identities():
    out=dict(build()[0])
    # Independent three-dimensional Christoffel/Ricci calculation.
    x,y,z=s.symbols('x y z',real=True); coords=(x,y,z)
    a,b=s.Function('a')(x),s.Function('b')(x)
    metric=s.diag(s.exp(2*a),s.exp(2*b),s.exp(2*b)); inv=metric.inv()
    gamma=[[[s.simplify(sum(inv[i,l]*(s.diff(metric[l,k],coords[j])
        +s.diff(metric[l,j],coords[k])-s.diff(metric[j,k],coords[l]))/2 for l in range(3)))
        for k in range(3)] for j in range(3)] for i in range(3)]
    ric=s.Matrix(3,3,lambda i,j:sum(s.diff(gamma[k][i][j],coords[k])
        -s.diff(gamma[k][i][k],coords[j])+sum(gamma[k][i][j]*gamma[l][k][l]
        -gamma[l][i][k]*gamma[k][j][l] for l in range(3)) for k in range(3)))
    out['plane_Ricci']=s.simplify(s.trace(inv*ric)-s.exp(-2*a)*(
        -4*s.diff(b,x,2)-6*s.diff(b,x)**2+4*s.diff(a,x)*s.diff(b,x)))
    # Canonical fluid transport derived by variation of Pi sigma_dot - beta Pi sigma' - J H.
    x=s.Symbol('x',real=True); Pi=s.Function('Pi')(x); g=s.Function('g')(x)
    beta,J=s.Function('beta')(x),s.Function('J')(x)
    j,k=s.symbols('j k',positive=True); a=s.Function('a')(x)
    H=s.Function('H')(j,k); sigmad=s.Symbol('sigmad')
    dens=Pi*sigmad-beta*Pi*g-J*H.subs({j:Pi/J,k:s.exp(-2*a)*g*g})
    vels=s.diff(dens,Pi)
    out['matter_velocity']=s.simplify(vels-(sigmad-beta*g-s.diff(H,j).subs({j:Pi/J,k:s.exp(-2*a)*g*g})))
    flux=-s.diff(dens,g)
    out['matter_flux']=s.simplify(flux-(beta*Pi+2*J*s.exp(-2*a)*g*s.diff(H,k).subs({j:Pi/J,k:s.exp(-2*a)*g*g})))
    return out


def grid(nodes):
    if nodes<8 or nodes%2:raise ValueError('Even periodic grid, at least 8 nodes')
    x=2*np.pi*np.arange(nodes)/nodes
    k=np.fft.fftfreq(nodes,1/nodes)
    first=k.copy();first[nodes//2]=0
    F=np.fft.fft(np.eye(nodes),axis=0)
    D=np.fft.ifft(1j*first[:,None]*F,axis=0).real
    D2=np.fft.ifft(-k[:,None]**2*F,axis=0).real
    return x,D,D2


class Evolution:
    def __init__(self,nodes=32,amplitude=.02):
        self.model=old.hermite.repair(old.exterior.models()[1]); m=self.model
        self.x,self.D,self.D2=grid(nodes); self.nodes=nodes
        with mp.workdps(40):
            original=old.exterior.history.initial('-1000','.5')
            entries=old.exterior.history.base.matter.matter(mp.mpf(m.Sref),mp.mpf(m.Q),original['fluids'])
        self.fluids=[{k:float(f[k]) for k in ('w','c','j')} for f in entries]
        q=m.q+amplitude*np.cos(2*self.x)
        fields=[np.full(nodes,m.Q),q,-(q-m.q)/2]
        fields.extend(np.full(nodes,np.log(f['j'])) for f in self.fluids)
        fields.extend(np.zeros(nodes) for _ in self.fluids)
        self.initial=np.r_[np.array(fields).ravel(),0.]
        self.guess=np.full(nodes,m.Sbar)
        self.keys,self.fn=build()[1:]
        self.calls=0; self.newton_iterations=0

    def fields(self,y):
        if not np.all(np.isfinite(y)):raise ValueError('Nonfinite evolved state')
        return y[:-1].reshape(7,self.nodes),y[-1]

    def vacuum(self,F,Xi,S,beta=None,bp=None):
        m=self.model; Q,q,sh=F[:3]; n=self.nodes
        Q1=self.D@Q; Q2=self.D2@Q; S1=self.D@S; S2=self.D2@S
        D,D1,D2=(m.table(S,nu=i) for i in range(3))
        if np.any(D<=0):raise ValueError('Nonconvex z branch')
        z=2*np.sqrt(D/(6*m.E))*np.sinh(np.arcsinh(-3*m.A*q*np.sqrt(6*m.E/D)/(4*D))/3)
        beta=np.zeros(n) if beta is None else beta
        bp=np.zeros(n) if bp is None else bp
        vals=self.fn(S,S1,S2,Q,Q1,Q2,q,self.D@q,z,sh,self.D@sh,beta,bp,
            Xi,m.wc,m.m,m.a02,m.lam,m.kappa,m.A,D,D1,D2,m.E)
        return {**{k:np.broadcast_to(v,(n,)) for k,v in zip(self.keys,vals)},'z':z,
                't':2*np.exp(S-2*m.wc)/m.m}

    def matter(self,F,Xi,S):
        Q=F[0]; a=Q+2*Xi/3; ans=[]
        for i,f in enumerate(self.fluids):
            j=np.exp(F[3+i]); g=F[5+i]
            fm=old.fluid(j,g,S,a,f['w'],f['c'])
            fm.update(j=j,g=g,k=np.exp(-2*a)*g*g)
            ans.append(fm)
        return ans

    def auxiliary(self,F,Xi):
        S=self.guess.copy(); m=self.model
        for iteration in range(20):
            v=self.vacuum(F,Xi,S); matter=self.matter(F,Xi,S)
            rho=sum(f['h'] for f in matter); C=v['C']+rho
            norm=float(np.max(abs(C)))
            self.newton_iterations+=1
            if norm<5e-11:
                self.guess=S
                return S,v,matter,norm
            Jac=np.diag(v['CS']+rho)+v['CS1'][:,None]*self.D+v['CS2'][:,None]*self.D2
            delta=np.linalg.solve(Jac,-C)
            for power in range(16):
                candidate=S+delta/(2**power)
                if np.min(candidate)<=m.table.x[0] or np.max(candidate)>=m.table.x[-1]:continue
                vc=self.vacuum(F,Xi,candidate); mc=self.matter(F,Xi,candidate)
                if np.max(abs(vc['C']+sum(f['h'] for f in mc)))<norm:
                    S=candidate;break
            else:raise RuntimeError('Auxiliary Newton line search failed; no extrapolation')
        raise RuntimeError('Auxiliary Newton iteration cap reached')

    def rhs(self,y,suppress_zero_mode=False):
        self.calls+=1; F,Xi=self.fields(y); Q,q,sh=F[:3]
        S,v,matter,lapse=self.auxiliary(F,Xi)
        Xidot=float(np.mean(v['t']*sh))
        f=Xidot-v['t']*sh
        k=np.fft.fftfreq(self.nodes,1/self.nodes); mask=(k!=0)
        mask[self.nodes//2]=False
        bhat=np.zeros(self.nodes,dtype=complex)
        bhat[mask]=np.fft.fft(f)[mask]/(1j*k[mask])
        beta=np.fft.ifft(bhat).real; bp=self.D@beta
        if suppress_zero_mode:Xidot=0.
        v=self.vacuum(F,Xi,S,beta,bp)
        Qd=v['Qdot']; qd=v['qdot'].copy(); sd=v['shdot'].copy()
        J=np.exp(3*Q); a=Q+2*Xi/3; out=[Qd,qd,sd]; logs=[]; grads=[]
        for fm in matter:
            j,g,vf=fm['j'],fm['g'],fm['v']
            pressure=j*np.exp(S)*vf-fm['h']
            anis=np.exp(S)*j*fm['k']/(2*vf)
            qd+=3*pressure/2+anis; sd+=anis
            flux=J*j*(beta+np.exp(S-2*a)*g/vf)
            logs.append((self.D@flux)/(J*j)-3*Qd)
            grads.append(self.D@(np.exp(S)*vf+beta*g))
        out.extend(logs);out.extend(grads)
        momentum=2*(self.D@q)/3+4*(self.D@sh)/3+4*(self.D@Q)*sh-sum(fm['j']*fm['g'] for fm in matter)
        ell=-np.exp(-S)*(v['W']-sum(fm['pw'] for fm in matter))
        diagnostics=dict(lapse=lapse,momentum=float(np.max(abs(momentum))),
            gauge=float(np.max(abs(Xidot-bp-v['t']*sh))),
            z=float(np.max(abs(self.model.A*q+2*self.model.table(S)*v['z']+4*self.model.E*v['z']**3))),
            w=float(np.max(abs(v['W']-sum(fm['pw'] for fm in matter)+np.exp(S)*ell))),
            fluid_error=float(max(np.max(abs(fm['legendre_error'])) for fm in matter)),
            charges=[float(np.mean(J*fm['j'])) for fm in matter],
            S_range=[float(np.min(S)),float(np.max(S))],
            pin_margin=float(np.min((-np.exp(-3*self.model.wc)*q/(3*.5))**2-.75)),
            physical_expansion=float(np.min(np.exp(-S-self.model.wc)*(
                Qd-beta*(self.D@Q)-bp/3))))
        if diagnostics['pin_margin']<=0:
            raise ValueError('RK stage leaves the active-pin plateau')
        return np.r_[np.array(out).ravel(),Xidot],diagnostics


def experiment(nodes=32,dt=.002,end=.04,amplitude=.02,suppress_zero_mode=False):
    nstep=round(end/dt)
    if nstep<1 or abs(nstep*dt-end)>1e-12:raise ValueError('Choose an integer number of steps')
    model=Evolution(nodes,amplitude); y=model.initial.copy()
    maxima={k:0. for k in ('lapse','momentum','gauge','z','w','fluid_error')}
    rows=[]; first=None; drift=0.; minpin=float('inf'); minH=float('inf')
    try:
        for i in range(nstep+1):
            k1,diag=model.rhs(y,suppress_zero_mode)
            if first is None:first=diag['charges']
            for k in maxima:maxima[k]=max(maxima[k],diag[k])
            drift=max(drift,max(abs(a/b-1) for a,b in zip(diag['charges'],first)))
            minpin=min(minpin,diag['pin_margin'])
            minH=min(minH,diag['physical_expansion'])
            if i in (0,nstep//2,nstep):rows.append(dict(time=i*dt,**diag,Xi=float(y[-1])))
            if i==nstep:break
            k2,_=model.rhs(y+dt*k1/2,suppress_zero_mode)
            k3,_=model.rhs(y+dt*k2/2,suppress_zero_mode)
            k4,_=model.rhs(y+dt*k3,suppress_zero_mode)
            y=y+dt*(k1+2*k2+2*k3+k4)/6
    except (ValueError,RuntimeError,np.linalg.LinAlgError) as error:
        return dict(success=False,reason=str(error),completed_steps=i,nodes=nodes,dt=dt,rows=rows,
                    full_theory='OPEN')
    F,Xi=model.fields(y)
    return dict(success=True,nodes=nodes,dt=dt,end=end,steps=nstep,amplitude=amplitude,
        max_lapse_constraint=maxima['lapse'],max_momentum_constraint=maxima['momentum'],
        max_gauge_residual=maxima['gauge'],max_z_constraint=maxima['z'],max_w_constraint=maxima['w'],
        max_fluid_legendre_error=maxima['fluid_error'],max_relative_matter_charge_drift=drift,
        max_fluid_gradient=float(np.max(abs(F[5:]))),min_pin_margin=minpin,
        min_physical_expansion=minH,
        max_initial_to_final_change=float(np.max(abs(y-model.initial))),
        Xi_final=float(Xi),rhs_calls=model.calls,newton_iterations=model.newton_iterations,
        final_state=y.tolist(),rows=rows,full_theory='OPEN')


def main():
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true')
    p.add_argument('--quick',action='store_true');args=p.parse_args()
    checks={k:v==0 for k,v in identities().items()}
    configs=[(32,.002)] if args.quick else [(32,.02),(32,.01),(32,.005),(64,.005)]
    rows=[experiment(n,dt,end=.04 if args.quick else .2) for n,dt in configs]
    checks['evolution']=all(r['success'] and r['max_momentum_constraint']<1e-6
        and r['max_lapse_constraint']<1e-8 and r['max_relative_matter_charge_drift']<1e-7
        and r['max_gauge_residual']<1e-8 and r['min_pin_margin']>0
        and r['min_physical_expansion']>0 for r in rows)
    convergence={}
    if not args.quick and all(r['success'] for r in rows):
        errors=[float(np.max(abs(np.array(rows[i]['final_state'])-rows[i+1]['final_state']))) for i in (0,1)]
        coarse=np.array(rows[2]['final_state']); fine=np.array(rows[3]['final_state'])
        spatial=float(np.max(abs(coarse-np.r_[fine[:-1].reshape(7,64)[:,::2].ravel(),fine[-1]])))
        convergence=dict(time_errors=errors,time_error_ratio=errors[0]/max(1e-30,errors[1]),
                         spatial_final_state_difference=spatial)
        checks['refinement']=convergence['time_error_ratio']>8 and spatial<1e-7
    control=Evolution(32)
    good=control.rhs(control.initial)[1]['gauge']
    bad=control.rhs(control.initial,True)[1]['gauge']
    checks['zero_mode_control']=good<1e-10 and bad>1e-8
    print(json.dumps(dict(checks=checks,rows=rows,convergence=convergence,
        zero_mode_control=dict(retained=good,suppressed=bad),full_theory='OPEN'),indent=2))
    return 1 if not all(checks.values()) else 2 if args.strict else 0


if __name__=='__main__':
    raise SystemExit(main())
