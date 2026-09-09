"""IC33: vary independent radial/angular metrics BEFORE imposing isotropy.

This closes a missing evolution-equation audit, not the full gravity theory.
"""
import argparse
from functools import lru_cache
import json
import numpy as np
import sympy as s
import ic30_radial_bridge as radial
import ic32_constraint_preservation as tangent


@lru_cache(None)
def build():
    d=radial.radial_action(); r=d['r']
    S,w,Q,q,z,sh,beta,ell=d['fields']
    ar,bt=(s.Function(n)(r) for n in ('ar','bt'))
    ad,bd,qd,sd=s.symbols('adot bdot qdot shdot',real=True)
    J=r**2*s.exp(ar+2*bt); v=d['v']; t=d['t']
    ap,bp=s.diff(ar,r),s.diff(bt,r)
    # Ricci scalar of diag(exp(2ar), exp(2bt) r^2, exp(2bt) r^2 sin^2 theta).
    R=s.exp(-2*ar)*(-4*s.diff(bt,r,2)-6*bp**2+4*ap*bp
        +4*ap/r-12*bp/r-2/r**2)+2*s.exp(-2*bt)/r**2
    mixed=2*d['u']*d['xi']*s.diff(d['xi'],r)*s.diff(d['u'],r)+d['xi']**2*s.diff(d['u'],r)**2
    L0=2*(q+2*sh)*ad/3+4*(q-sh)*bd/3-2*t*sh**2/3+t*q**2/6
    L0+=d['A']*q*z+s.exp(S)*d['P0']+d['D']*z**2+d['E4']*z**4
    L0+=d['eta']*s.exp(S)*ell*(w-d['wc'])
    L0-=2*(q+2*sh)*(s.diff(beta,r)+beta*ap)/3
    L0-=4*(q-sh)*beta*(bp+1/r)/3
    L=J*(L0+v*R+2*v*s.exp(-2*ar)*mixed)
    Ea=radial.euler(L,ar,r,2)-2*J*(qd+2*sd+(ad+2*bd)*(q+2*sh))/3
    Eb=radial.euler(L,bt,r,2)-4*J*(qd-sd+(ad+2*bd)*(q-sh))/3
    def iso(x):
        return s.simplify(x.subs({ar:Q,bt:Q,ad:d['Qdot'],bd:d['Qdot']},simultaneous=True).doit())
    def pin(x):
        return s.simplify(x.subs(d['eta'],1).doit().subs(w,d['wc']).doit())
    Ea,Eb=pin(iso(Ea/J)),pin(iso(Eb/J))
    qflow=s.simplify((Ea+Eb).subs({qd:0,sd:0})/2)
    sflow=s.simplify((2*Ea-Eb).subs({qd:0,sd:0})/4)
    vp=v.subs(w,d['wc']); tp=t.subs(w,d['wc'])
    u=d['u'].subs(w,d['wc']); B=2*vp*(1-u*u)
    h=-tp*q*q/6-d['A']*q*z-s.exp(S)*d['P0'].subs(w,d['wc'])-d['D']*z*z-d['E4']*z**4
    HQ=s.diff(h,q)/2
    div=s.diff(beta,r)+3*beta*s.diff(Q,r)+2*beta/r
    Qflow=HQ+div/3
    sflow=s.simplify(sflow.subs(d['Qdot'],Qflow))
    qflow=s.simplify(qflow.subs(d['Qdot'],Qflow))
    Q1,Q2=s.diff(Q,r),s.diff(Q,r,2); S1,S2=s.diff(S,r),s.diff(S,r,2)
    qexpected=-3*h/2+tp*sh**2+beta*s.diff(q,r)
    qexpected+=s.exp(-2*Q)*(-2*vp*Q1**2-4*vp*S1*Q1+(B-4*vp)*S1**2
                             -4*vp*(Q2+S2+2*(Q1+S1)/r))/2
    sexpected=beta*s.diff(sh,r)-3*HQ*sh+s.exp(-2*Q)*(
        vp*(Q2+S2-(Q1+S1)/r-Q1**2-2*Q1*S1)+(vp-B)*S1**2)
    # Actual Ricci boundary relation, not an equality after dropping an equation.
    boundary=4*r**2*s.exp(Q)*v*s.diff(Q,r)
    action_check=s.simplify(iso(L)-d['L']+s.diff(boundary,r))
    trace_from_old=pin(radial.radial_equations()['Q']/d['J'])
    checks={'isotropic_action':action_check,
        'trace_evolution':s.simplify(Ea+Eb-trace_from_old.subs(d['qdot'],qd)),
        'tracefree_evolution':s.simplify(sflow-sexpected),
        'trace_formula':s.simplify((qflow-qexpected).subs(s.diff(beta,r),beta/r-tp*sh))}
    jets=(S,S1,S2,Q,Q1,Q2,q,s.diff(q,r),z,sh,s.diff(sh,r),beta,s.diff(beta,r))
    symbols=s.symbols('S S1 S2 Q Q1 Q2 q q1 z sh sh1 beta beta1',real=True)
    A,D,E=s.symbols('A D E',real=True)
    sub={d['A']:A,d['D']:D,d['E4']:E}
    exprs=[x.subs(sub).subs(dict(zip(jets,symbols)),simultaneous=True) for x in (Qflow,qflow,sflow)]
    args=(r,*symbols,d['wc'],d['m'],d['a02'],d['lam'],d['kappa'],A,D,E)
    return checks,s.lambdify(args,exprs,'numpy',cse=True)


def identities():
    out=dict(build()[0])
    # Vary the same minimally coupled Hamiltonian at fixed canonical Pi,sigma.
    ar,bt,Pi,g,S=s.symbols('ar bt Pi g S',real=True)
    j,k=s.symbols('j k',positive=True)
    H=s.Function('H')(j,k)
    J=s.exp(ar+2*bt)
    L=-J*H.subs({j:Pi/J,k:s.exp(-2*ar)*g**2})
    replace={Pi:j,g:s.sqrt(k),ar:0,bt:0}
    a=s.diff(L,ar).subs(replace,simultaneous=True).doit()
    b=s.diff(L,bt).subs(replace,simultaneous=True).doit()
    p=j*s.diff(H,j)-H
    out['matter_trace']=s.simplify((a+b)/2-3*p/2-k*s.diff(H,k))
    out['matter_tracefree']=s.simplify((2*a-b)/4-k*s.diff(H,k))
    return out


def evaluate(model,r,S,S1,S2,Q,Q1,Q2,q,q1,z,sh,sh1,beta,beta1):
    a=np.broadcast_arrays(r,S,S1,S2,Q,Q1,Q2,q,q1,z,sh,sh1,beta,beta1)
    if np.min(a[1])<model.table.x[0] or np.max(a[1])>model.table.x[-1]:
        raise ValueError('No coefficient extrapolation')
    vals=build()[1](*a,model.wc,model.m,model.a02,model.lam,model.kappa,model.A,
                    model.table(a[1]),model.E)
    return dict(zip(('Qdot','qdot','shdot'),[np.broadcast_to(x,a[0].shape) for x in vals]))


def initial_audit(amplitude=1.,nodes=1601):
    model=tangent.hermite.repair(tangent.exterior.models()[1])
    data=tangent.initial_slice(model,amplitude,nodes); r=data['r']; old=data['old']
    flow=evaluate(model,r,data['S'],data['S1'],data['S2'],model.Q,0.,0.,model.q,0.,
                  old['z'],old['shear'],-3*old['shear']/r,data['beta'],data['bp'])
    flow['qdot']=flow['qdot']+3*data['pressure']/2
    # Fluid gradients vanish on this slice; anisotropic fluid stress is zero.
    mismatch=data['shdot']-flow['shdot']
    weighted=r**3*mismatch
    return dict(amplitude=amplitude,nodes=nodes,
        max_trace_disagreement=float(np.max(abs(flow['qdot']-data['qdot']))),
        max_Q_disagreement=float(np.max(abs(flow['Qdot']-data['Qdot']))),
        action_inner_shdot=float(flow['shdot'][0]),
        imposed_inner_shdot=float(data['shdot'][0]),
        max_missing_tracefree_residual=float(np.max(abs(mismatch))),
        weighted_difference_range=[float(np.min(weighted)),float(np.max(weighted))],
        boundary_corrected_max_residual=float(np.max(abs(mismatch+flow['shdot'][0]*8/r**3))),
        full_theory='OPEN')



def curvature_check():
    d=radial.static_geometry(); r=d['r']; a=d['a']; b=d['b']
    ap,bp=s.diff(a,r),s.diff(b,r)
    want=s.exp(-2*a)*(-4*s.diff(b,r,2)-6*bp**2+4*ap*bp+4*ap/r-12*bp/r-2/r**2)
    want+=2*s.exp(-2*b)/r**2
    return s.simplify(d['R']-want)


def full_tangent(amplitude=1.,nodes=1601):
    """Use full metric evolution to determine, not assign, inner shear rate.

    Momentum preservation then propagates that datum. This remains a first
    derivative and finite-kick audit, NOT multi-step evolution.
    """
    model=tangent.hermite.repair(tangent.exterior.models()[1])
    data=tangent.initial_slice(model,amplitude,nodes)
    r,S,S1,S2=(data[k] for k in ('r','S','S1','S2'))
    old=data['old']; b=data['base']; Qd=data['Qd']; qd=data['qd']
    qdot=data['qdot']; Qdot=data['Qdot']; rho=data['rho']; pw=data['pw']
    flow=evaluate(model,r,S,S1,S2,model.Q,0.,0.,model.q,0.,old['z'],
                  old['shear'],-3*old['shear']/r,data['beta'],data['bp'])
    inner=float(flow['shdot'][0]); charge=8*inner
    def sh_velocity(x,order=0):
        return data['sh_velocity'](x,order)+(charge/x**3 if order==0 else -3*charge/x**4)
    shdot=sh_velocity(r); shdot1=sh_velocity(r,1)
    bg=model.evaluate(2.,model.Sbar,0.,0.,0.)
    bx=tangent.evaluate(model,2.,model.Sbar,0.,0.,model.Q,0.,0.,model.q,bg['z'],0.)
    bgent=sum((1+f['w'])*f['h']*np.exp(model.Sbar-model.Sref) for f in data['fluids'])
    bgp=sum(f['w']*f['h']*np.exp(model.Sbar-model.Sref) for f in data['fluids'])
    bgqd=bx['qdot']+3*bgp/2
    Sdbar=float((3*bx['hq']*bgent/2-(bx['C_q']-bx['C_z']*bx['hqz']/bx['hzz'])*bgqd)/bg['potential'])
    def coefficients(x):
        sx,sx1,sx2=data['field'](x); ox=model.evaluate(x,sx,sx1,sx2,amplitude)
        vx=tangent.evaluate(model,x,sx,sx1,sx2,model.Q,0.,0.,model.q,ox['z'],ox['shear'])
        ent=sum((1+f['w'])*f['h']*np.exp(sx-model.Sref) for f in data['fluids'])
        beta=-x*(data['shift'](x)-data['shift'](2.))
        div=3*beta/x-x*data['shift'](x,1)
        src=(vx['C_q']-vx['C_z']*vx['hqz']/vx['hzz'])*qd(x)+vx['C_sh']*sh_velocity(x)
        src+=vx['C_Q']*Qd(x)+vx['C_Q1']*Qd(x,1)+vx['C_Q2']*Qd(x,2)+(div-3*Qd(x))*ent
        return vx['C_S2'],vx['C_S1'],ox['potential'],src
    def rhs(x,y):
        a,b,c,f=coefficients(x)
        return np.vstack((y[1],-(b*y[1]+c*y[0]+f)/a))
    sol=tangent.solve_bvp(rhs,lambda l,rr:np.array([l[1],rr[0]-Sdbar]),r,
        np.vstack((np.full(r.size,Sdbar),np.zeros(r.size))),tol=1e-9,max_nodes=60000)
    if not sol.success:return dict(solved=False,message=sol.message)
    anti=sol.sol.antiderivative()
    Sd=Sdbar+anti(r)[1]-anti(8.)[1]; Sd1=sol.sol(r)[1]; Sd2=sol.sol(r,1)[1]
    zd=-(b['hSz']*Sd+b['hqz']*qdot)/b['hzz']
    ell=-old['W']/old['Wcoef']
    timejets=dict(S=Sd,S1=Sd1,S2=Sd2,Q=Qdot,Q1=Qd(r,1),Q2=Qd(r,2),
                  q=qdot,z=zd,sh=shdot)
    Wdot=sum(b['W_'+k]*v for k,v in timejets.items())-pw*Sd+3*data['HQ']*data['pw_ent']
    elld=-np.exp(-S)*Wdot-ell*Sd
    beta_anti=tangent.CubicSpline(r,old['t']*(shdot+old['shear']*Sd)/r).antiderivative()
    betad=-r*(beta_anti(r)-beta_anti(2.)); betad1=betad/r-r*beta_anti(r,1)
    Cdot=sum(b['C_'+k]*v for k,v in timejets.items())+rho*Sd-3*data['HQ']*data['ent']
    mid=(r[:-1]+r[1:])/2
    ac,bc,cc,fc=coefficients(mid)
    midSd=Sdbar+anti(mid)[1]-anti(8.)[1]
    offC=ac*sol.sol(mid,1)[1]+bc*sol.sol(mid)[1]+cc*midSd+fc
    sx,sx1,sx2=data['field'](mid); ox=model.evaluate(mid,sx,sx1,sx2,amplitude)
    betax=-mid*(data['shift'](mid)-data['shift'](2.)); bpx=betax/mid-mid*data['shift'](mid,1)
    midflow=evaluate(model,mid,sx,sx1,sx2,model.Q,0.,0.,model.q,0.,ox['z'],
                    ox['shear'],-3*ox['shear']/mid,betax,bpx)
    shear_error=max(np.max(abs(shdot-flow['shdot'])),np.max(abs(sh_velocity(mid)-midflow['shdot'])))
    mpres=2*qd(r,1)/3+4*shdot1/3+4*shdot/r+4*old['shear']*Qd(r,1)-data['ent']*S1
    def kick(dt):
        Sn=S+dt*Sd; Qn=model.Q+dt*Qdot; qn=model.q+dt*qdot
        zn=old['z']+dt*zd; shn=old['shear']+dt*shdot
        nxt=tangent.evaluate(model,r,Sn,S1+dt*Sd1,S2+dt*Sd2,Qn,dt*Qd(r,1),
                             dt*Qd(r,2),qn,zn,shn)
        hsum=np.zeros_like(r); pwsum=np.zeros_like(r); momentum=np.zeros_like(r)
        for f in data['fluids']:
            j=f['j']*(1+dt*data['divb'])*np.exp(-3*dt*Qdot)
            grad=dt*np.exp(S)*(1+f['w'])*f['c']*f['j']**f['w']*S1
            fm=tangent.fluid(j,grad,Sn,Qn,f['w'],f['c'])
            hsum+=fm['h']; pwsum+=fm['pw']; momentum+=j*grad
        mom=2*dt*qd(r,1)/3+4*(-3*old['shear']/r+dt*shdot1)/3
        mom+=4*(dt*Qd(r,1)+1/r)*shn-momentum
        sg=2*np.exp(Sn-2*model.wc)/model.m*shn+data['bp']+dt*betad1-(data['beta']+dt*betad)/r
        return dict(dt=dt,lapse=float(np.max(abs(nxt['C']+hsum))),
            z=float(np.max(abs(model.A*qn+2*model.table(Sn)*zn+4*model.E*zn**3))),
            w=float(np.max(abs(nxt['W']-pwsum+np.exp(Sn)*(ell+dt*elld)))),
            momentum=float(np.max(abs(mom))),shear_gauge=float(np.max(abs(sg))))
    kicks=[kick(dt) for dt in (.001,.0005,.00025)]
    keys=('lapse','z','w','momentum','shear_gauge')
    ratios=[{k:kicks[i][k]/max(1e-30,kicks[i+1][k]) for k in keys} for i in (0,1)]
    return dict(solved=True,amplitude=amplitude,nodes=nodes,bvp_nodes=int(sol.x.size),
        action_inner_shdot=inner,full_shear_euler_defect=float(shear_error),
        momentum_preservation=float(np.max(abs(mpres))),
        max_preservation_residual=float(max(np.max(abs(Cdot)),np.max(abs(offC)))),
        Sdot_range=[float(np.min(Sd)),float(np.max(Sd))],
        kicks=kicks,kick_ratios=ratios,first_order_only=True,full_theory='OPEN')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--strict',action='store_true')
    args=parser.parse_args()
    checks={name:value==0 for name,value in identities().items()}
    checks['curvature_from_christoffels']=curvature_check()==0
    rows=[initial_audit(a,n) for a,n in ((0.,1601),(1.,1601),(1.,3201),(2.,1601))]
    coarse=full_tangent(1.,1601)
    repaired=[full_tangent(a,n) for a,n in ((1.,3201),(2.,3201),(2.,6401))]
    checks['repaired_tangents']=all(x['solved'] and x['full_shear_euler_defect']<1e-7
        and x['max_preservation_residual']<1e-5
        and x['momentum_preservation']<1e-8
        and min(v for rr in x['kick_ratios'] for v in rr.values())>3.2 for x in repaired)
    checks['spatial_refinement']=coarse['solved'] and (
        repaired[0]['full_shear_euler_defect']<coarse['full_shear_euler_defect']/8
        and repaired[2]['full_shear_euler_defect']<repaired[1]['full_shear_euler_defect']/8)
    out=dict(checks=checks,rows=rows,coarse_tangent_control=coarse,repaired=repaired,full_theory='OPEN')
    print(json.dumps(out,indent=2))
    if not all(checks.values()):return 1
    return 2 if args.strict else 0


if __name__=='__main__':
    raise SystemExit(main())
