"""Analytic time differentiation on the fixed coefficient's local cells.

Third coefficient jets are one-sided at knots, not a global C3 declaration.
"""
from functools import lru_cache
import json
import numpy as np
import sympy as s
import ic36_second_preservation as previous
import ic32_constraint_preservation as base
import ic30_radial_bridge as radial


def third_jet(table,S):
    S=np.asarray(S)
    if np.min(S)<table.x[0] or np.max(S)>table.x[-1]:raise ValueError('No coefficient extrapolation')
    i=np.clip(np.searchsorted(table.x,S,side='right')-1,0,len(table.x)-2)
    h=table.x[i+1]-table.x[i];x=(S-table.x[i])/h
    a,b,c=table.jets[i].T;d,e,f=table.jets[i+1].T
    R=(d-a-h*b-h*h*c/2,h*(e-b)-h*h*c,h*h*(f-c))
    # Third derivatives of IC32's three normalized quintic Hermite corrections.
    H=(60-360*x+360*x*x,-24+168*x-180*x*x,3-24*x+30*x*x)
    return sum(v*fn for v,fn in zip(R,H))/h**3


def matter_constraints_second(h,j,jd,jdd,U,gd,S,Q,w,vf):
    zero=h*(U*U+2*(1+w)*U*jd/j+(1+w)*w*(jd/j)**2+(1+w)*jdd/j)
    gradient=np.exp(S-2*Q)*j*gd*gd/vf
    return zero+gradient,(1-3*w)*(zero-gradient)


@lru_cache(None)
def build():
    d=radial.radial_action();r=d['r'];Sf,w,Qf,qf,zf,shf,bf,ell=d['fields']
    X=s.symbols('S S1 S2 Q Q1 Q2 q z sh',real=True)
    S,S1,S2,Q,Q1,Q2,q,z,sh=X
    rates=s.symbols('U U1 U2 VQ VQ1 VQ2 Vq Vz Vsh',real=True)
    extras=s.symbols('q1 sh1 beta beta1',real=True);q1,sh1,beta,beta1=extras
    erates=s.symbols('Vq1 Vsh1 Vbeta Vbeta1',real=True)
    A,D,D1,D2,D3,E=s.symbols('A D D1 D2 D3 E',real=True)
    coeff={d['A']:A,s.diff(d['A'],Sf):0,s.diff(d['A'],Sf,2):0,
           d['D']:D,s.diff(d['D'],Sf):D1,s.diff(d['D'],Sf,2):D2,
           d['E4']:E,s.diff(d['E4'],Sf):0,s.diff(d['E4'],Sf,2):0}
    fields=dict(zip((Sf,s.diff(Sf,r),s.diff(Sf,r,2),Qf,s.diff(Qf,r),s.diff(Qf,r,2),qf,zf,shf),X))
    def pin(expr):return s.simplify(expr.subs(ell,0).doit().subs(w,d['wc']).doit())
    def convert(expr):return pin(expr).subs(coeff,simultaneous=True).subs(fields,simultaneous=True)
    C=convert(-radial.euler(d['L'],Sf,r)/d['J'])
    W=convert(radial.euler(d['L'],w,r)/d['J'])
    vp=convert(d['v']);tp=convert(d['t']);up=convert(d['u']);B=2*vp*(1-up*up)
    h=-tp*q*q/6-A*q*z-s.exp(S)*convert(d['P0'])-D*z*z-E*z**4
    HQ=-tp*q/6-A*z/2
    Qflow=HQ+beta*Q1+(beta1+2*beta/r)/3
    qflow=-3*h/2+tp*sh**2+beta*q1+s.exp(-2*Q)*(-2*vp*Q1**2-4*vp*S1*Q1
           +(B-4*vp)*S1**2-4*vp*(Q2+S2+2*(Q1+S1)/r))/2
    # IC33's full trace expression differs from its shear-gauge reduction by this term.
    qflow-=2*sh*(beta1-beta/r+tp*sh)
    shflow=beta*sh1-3*HQ*sh+s.exp(-2*Q)*(vp*(Q2+S2-(Q1+S1)/r-Q1**2-2*Q1*S1)+(vp-B)*S1**2)
    def direction(expr,with_extras=False):
        out=sum(s.diff(expr,x)*v for x,v in zip(X,rates))
        out+=rates[0]*(s.diff(expr,D)*D1+s.diff(expr,D1)*D2+s.diff(expr,D2)*D3)
        if with_extras:out+=sum(s.diff(expr,x)*v for x,v in zip(extras,erates))
        return out
    accelerations=s.symbols('AQ AQ1 AQ2 Aq Az Ash',real=True)
    acceleration_vector=(0,0,0,*accelerations)
    source=[direction(direction(F))+sum(s.diff(F,x)*a for x,a in zip(X,acceleration_vector)) for F in (C,W)]
    parameters=(d['m'],d['wc'],d['a02'],d['lam'],d['kappa'],A,D,D1,D2,D3,E)
    flowfn=s.lambdify((r,*X,*extras,*rates,*erates,*parameters),
        [Qflow,qflow,shflow,*[direction(f,True) for f in (Qflow,qflow,shflow)]],'numpy',cse=True)
    sourcefn=s.lambdify((r,*X,*rates,*accelerations,*parameters),[C,W,*source],'numpy',cse=True)
    flowmp=s.lambdify((r,*X,*extras,*rates,*erates,*parameters),
        [Qflow,qflow,shflow,*[direction(f,True) for f in (Qflow,qflow,shflow)]],'mpmath',cse=True)
    sourcemp=s.lambdify((r,*X,*rates,*accelerations,*parameters),[C,W,*source],'mpmath',cse=True)
    grads=[]
    for F in (C,W):
        row=[s.diff(F,x) for x in X]
        row[0]+=s.diff(F,D)*D1+s.diff(F,D1)*D2
        grads.extend([F,*row])
    gradmp=s.lambdify((r,*X,*parameters),grads,'mpmath',cse=True)
    return flowfn,sourcefn,flowmp,sourcemp,gradmp


def sources(first,degree=10,nodes=65,interval=(2.,2.0015)):
    r,v,time,initial,HQ,C,W=first.sample(degree,nodes,interval);m=first.c.model
    v=dict(v);time=dict(time);v['z']=initial['z'];eq=initial['eq']
    time['z']=-(eq['hSz']*time['S']+eq['hqz']*time['q'])/eq['hzz']
    D,D1,D2=(m.table(v['S'],nu=i) for i in range(3));D3=third_jet(m.table,v['S'])
    params=(m.m,m.wc,m.a02,m.lam,m.kappa,m.A,D,D1,D2,D3,m.E)
    names=('S','S1','S2','Q','Q1','Q2','q','z','sh');en=('q1','sh1','beta','beta1')
    vals=build()[0](r,*(v[k] for k in names),*(v[k] for k in en),
                    *(time[k] for k in names),*(time[k] for k in en),*params)
    vals=[np.broadcast_to(x,r.shape).copy() for x in vals]
    flow=dict(zip(('Q','q','sh'),vals[:3]));acc=dict(zip(('Q','q','sh'),vals[3:]))
    for i,f in enumerate(first.c.fluids):
        h=f['h']*np.exp(v['S']-m.Sref)
        flow['q']+=3*f['w']*h/2
        acc['q']+=3*f['w']*h*(time['S']+(1+f['w'])*time['j'+str(i)]/f['j'])/2
    for k in ('Q','q','sh'):
        p=previous.fit(r,acc[k],degree);acc[k+'1']=p.deriv()(r)
        if k=='Q':acc['Q2']=p.deriv(2)(r)
    Fz=2*D+12*m.E*v['z']**2
    acc['z']=-(m.A*acc['q']+2*D2*v['z']*time['S']**2+4*D1*time['S']*time['z']
               +24*m.E*v['z']*time['z']**2)/Fz
    t=2*np.exp(v['S']-2*m.wc)/m.m
    HQd=-t*(time['S']*v['q']+time['q'])/6-m.A*time['z']/2
    ans=build()[1](r,*(v[k] for k in names),*(time[k] for k in names),
                  *(acc[k] for k in ('Q','Q1','Q2','q','z','sh')),*params)
    Cv,Wv,FC,FW=[np.broadcast_to(x,r.shape).copy() for x in ans]
    for i,f in enumerate(first.c.fluids):
        jd=time['j'+str(i)];gd=time['g'+str(i)]
        vf=(1+f['w'])*f['c']*f['j']**f['w'];h=f['h']*np.exp(v['S']-m.Sref)
        jdd=previous.matter_second(f['j'],jd,previous.fit(r,jd,degree).deriv()(r),v['beta'],HQ,HQd,
               v['Q1'],v['S1'],r,np.exp(v['S']-2*v['Q'])/vf,gd,previous.fit(r,gd,degree).deriv()(r))
        acc['j'+str(i)]=jdd
        hdd,pwdd=matter_constraints_second(h,f['j'],jd,jdd,time['S'],gd,v['S'],v['Q'],f['w'],vf)
        FC+=hdd;FW-=pwdd;Cv+=h;Wv-=(1-3*f['w'])*h
    return dict(r=r,v=v,time=time,acc=acc,initial=initial,HQ=HQ,C=C,W=W,FC=FC,FW=FW,
        flow_disagreement=float(max(np.max(abs(flow[k]-initial[k+'dot'])) for k in ('Q','q','sh'))),
        constraint_disagreement=float(max(np.max(abs(Cv-initial['C'])),np.max(abs(Wv-initial['W'])))),
        coefficient_cells=np.unique(np.searchsorted(m.table.x,v['S'],side='right')-1).tolist(),
        max_D3=float(np.max(abs(D3))))


def audit(first=None,step=1e-4):
    first=previous.FirstJet() if first is None else first
    data=sources(first);r,v,time,acc=(data[k] for k in ('r','v','time','acc'))
    def kick(h,quadratic):
        return {k:x+h*time[k]+(h*h*acc.get(k,0.)/2 if quadratic else 0.) for k,x in v.items()}
    fplus=first.evaluate(r,kick(step,False));fminus=first.evaluate(r,kick(-step,False))
    acceleration_error=max(np.max(abs((fplus[k+'dot']-fminus[k+'dot'])/(2*step)-acc[k])/
                          np.maximum(1.,abs(acc[k]))) for k in ('Q','q','sh'))
    plus=first.evaluate(r,kick(step,True));minus=first.evaluate(r,kick(-step,True))
    errors={k:float(np.max(abs((plus[k]+minus[k]-2*data['initial'][k])/step**2-data['F'+k]))) for k in ('C','W')}
    scale=max(1.,np.max(abs(data['FC'])),np.max(abs(data['FW'])))
    return dict(flow_disagreement=data['flow_disagreement'],constraint_disagreement=data['constraint_disagreement'],
        relative_acceleration_disagreement=float(acceleration_error),constraint_source_errors=errors,
        relative_constraint_source_disagreement=max(errors.values())/scale,
        coefficient_cells=data['coefficient_cells'],max_D3=data['max_D3'],full_theory='OPEN')


if __name__=='__main__':
    report=audit();print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['flow_disagreement']<1e-9 and
        report['relative_acceleration_disagreement']<1e-5 and report['relative_constraint_source_disagreement']<1e-5 else 1)
