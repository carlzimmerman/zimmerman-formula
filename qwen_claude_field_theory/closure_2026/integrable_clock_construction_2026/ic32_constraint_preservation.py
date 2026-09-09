"""First-order inhomogeneous constraint preservation with unprojected kicks.

This is a tangent to constrained exterior data, not an evolved galaxy or a
complete nonlinear Dirac proof. All coefficient functions stay fixed.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline, PPoly
from scipy.optimize import brentq
import ic31_pinned_tail as exterior
import ic30_radial_bridge as radial
import ic32_hermite_coefficients as hermite


@lru_cache(None)
def build():
    d=radial.radial_action(); r=d['r']; S,w,Q,q,z,sh,beta,ell=d['fields']
    eq=radial.radial_equations()
    def pin(expr):
        return s.simplify(expr.subs(d['eta'],1).doit().subs(w,d['wc']).doit())
    C=pin(-eq['S']/d['J']); W=pin(eq['w']/d['J']).subs(ell,0)
    v=d['v'].subs(w,d['wc']); t=d['t'].subs(w,d['wc'])
    u=d['u'].subs(w,d['wc']); B=2*v*(1-u*u)
    h=-t*q*q/6-d['A']*q*z-s.exp(S)*d['P0'].subs(w,d['wc'])-d['D']*z*z-d['E4']*z**4
    Qc=s.Symbol('Qc',real=True)
    qdot=pin(eq['Q'].subs(d['qdot'],0)/(2*d['J']))
    qdot=qdot.subs(Q,Qc).doit().subs(s.diff(q,r),0)
    qdot=s.simplify(qdot.subs(s.diff(beta,r),beta/r-t*sh))
    expected=-3*h/2+t*sh**2+s.exp(-2*Qc)*((B-4*v)*s.diff(S,r)**2
                                       -4*v*(s.diff(S,r,2)+2*s.diff(S,r)/r))/2
    checks={'qdot_from_full_Q_euler':s.simplify(qdot-expected),
            'curvature_time_second_jet':s.simplify(s.diff(C,s.diff(Q,r,2))-4*v*s.exp(-2*Q))}
    derivatives=(S,s.diff(S,r),s.diff(S,r,2),Q,s.diff(Q,r),s.diff(Q,r,2),q,z,sh)
    names=('S','S1','S2','Q','Q1','Q2','q','z','sh')
    values={'C':C,'W':W,'h':h,'hq':s.diff(h,q),'hSq':s.diff(h,S,q),
            'hSz':s.diff(h,S,z),'hzz':s.diff(h,z,2),'hqz':s.diff(h,q,z),'qdot':qdot.subs(Qc,Q)}
    for label,expr in (('C',C),('W',W)):
        values.update({label+'_'+name:s.diff(expr,var) for name,var in zip(names,derivatives)})
    symbols=s.symbols('Sv S1 S2 Qv Q1 Q2 qv zv shv',real=True)
    mapping=dict(zip(derivatives,symbols))
    A,D,D1,D2,E=s.symbols('A D D1 D2 E',real=True)
    jets={d['A']:A,s.diff(d['A'],S):0,s.diff(d['A'],S,2):0,
          d['D']:D,s.diff(d['D'],S):D1,s.diff(d['D'],S,2):D2,
          d['E4']:E,s.diff(d['E4'],S):0,s.diff(d['E4'],S,2):0}
    keys=list(values)
    expressions=[s.simplify(x.subs(jets,simultaneous=True).subs(mapping,simultaneous=True))
                 for x in values.values()]
    args=(r,*symbols,d['wc'],d['m'],d['a02'],d['lam'],d['kappa'],A,D,D1,D2,E)
    return checks,keys,s.lambdify(args,expressions,'numpy',cse=True)


def identities():
    out=dict(build()[0])
    out.update(hermite.identities())
    # Differentiate the actual initial momentum constraint, including fluid flow.
    r=s.Symbol('r',positive=True)
    sd,qd,Qd,sh,ent,Sp=s.symbols('sd qd Qd sh ent Sp',cls=s.Function)
    source=-s.diff(qd(r),r)/2-3*sh(r)*s.diff(Qd(r),r)+3*ent(r)*Sp(r)/4
    mdot=2*s.diff(qd(r),r)/3+4*s.diff(sd(r),r)/3+4*sd(r)/r
    mdot+=4*sh(r)*s.diff(Qd(r),r)-ent(r)*Sp(r)
    out['momentum_preservation_source']=s.simplify(mdot.subs(s.diff(sd(r),r),source-3*sd(r)/r))
    return out


def merge_mesh(values):
    """Merge roundoff-equivalent abscissas, not distinct physical breakpoints."""
    merged=[]
    for x in np.sort(values):
        if not merged or x-merged[-1]>64*np.finfo(float).eps*max(1.,abs(x)):
            merged.append(x)
    return np.array(merged)


def evaluate(model,r,S,S1,S2,Q,Q1,Q2,q,z,sh):
    arrays=np.broadcast_arrays(r,S,S1,S2,Q,Q1,Q2,q,z,sh)
    Sv=arrays[1]
    if np.min(Sv)<model.table.x[0] or np.max(Sv)>model.table.x[-1]:
        raise ValueError('Time tangent leaves the fixed coefficient domain')
    D,D1,D2=(model.table(Sv,nu=j) for j in range(3))
    keys,fn=build()[1:]
    vals=fn(*arrays,model.wc,model.m,model.a02,model.lam,model.kappa,model.A,D,D1,D2,model.E)
    return {key:np.broadcast_to(value,Sv.shape) for key,value in zip(keys,vals)}


def fluid(j,gradient,S,Q,w,c):
    """Full same-action Legendre transform, including generated spatial gradients.

    v is the normal derivative in the constant-wc conformally rescaled metric.
    The log equation avoids enormous powers for w=1e-8.
    """
    if not np.all(np.isfinite(j)) or np.min(j)<=0:
        raise ValueError('Finite positive fluid canonical density required')
    k2=np.exp(-2*Q)*gradient**2
    v0=(1+w)*c*j**w
    v=np.sqrt(v0**2+k2)
    for _ in range(8):
        ratio=k2/v**2
        f=np.log(v/v0)+(1-w)*np.log1p(-ratio)/2
        derivative=(1+(1-w)*ratio/(1-ratio))/v
        v=v-f/derivative
    error=np.log(v/v0)+(1-w)*np.log1p(-k2/v**2)/2
    if not np.all(np.isfinite(error)) or np.any(v*v<=k2):
        raise ValueError('Fluid Legendre solve left its timelike domain')
    energy=j*(v+w*k2/v)/(1+w)
    trace=(1-3*w)*j*(v-k2/v)/(1+w)
    return dict(h=np.exp(S)*energy,pw=np.exp(S)*trace,v=v,legendre_error=error)


def initial_slice(model,amplitude,nodes):
    radii=np.linspace(2.,8.,241)
    def rhs(r,y):
        a=model.evaluate(r,y[0],y[1],0.,amplitude)
        return np.vstack((y[1],-a['C']/a['a']))
    sol=solve_bvp(rhs,lambda l,r:np.array([l[1],r[0]-model.Sbar]),radii,
                  np.vstack((np.full(radii.size,model.Sbar),np.zeros(radii.size))),
                  tol=1e-10,max_nodes=16000)
    if not sol.success:raise RuntimeError(sol.message)
    r=np.linspace(2.,8.,nodes); anti=sol.sol.antiderivative()
    S=model.Sbar+anti(r)[1]-anti(8.)[1]; S1=sol.sol(r)[1]; S2=sol.sol(r,1)[1]
    old=model.evaluate(r,S,S1,S2,amplitude)
    base=evaluate(model,r,S,S1,S2,model.Q,0.,0.,model.q,old['z'],old['shear'])
    with mp.workdps(40):
        original=exterior.history.initial('-1000','.5')
        entries=exterior.history.base.matter.matter(mp.mpf(model.Sref),mp.mpf(model.Q),original['fluids'])
    fs=[{k:float(f[k]) for k in ('w','c','j','h')} for f in entries]
    hi=[f['h']*np.exp(S-model.Sref) for f in fs]
    rho=sum(hi); pressure=sum(f['w']*h for f,h in zip(fs,hi))
    ent=rho+pressure
    pw=sum((1-3*f['w'])*h for f,h in zip(fs,hi))
    pw_ent=sum((1-3*f['w'])*(1+f['w'])*h for f,h in zip(fs,hi))
    HQ=base['hq']/2
    shift=CubicSpline(r,old['t']*old['shear']/r).antiderivative()
    beta=-r*(shift(r)-shift(2.)); bp=beta/r-r*shift(r,1)
    divb=bp+2*beta/r
    Qdot=HQ+divb/3; qdot=base['qdot']+3*pressure/2
    Qd=CubicSpline(r,Qdot); qd=CubicSpline(r,qdot)
    # Moment preservation with the explicit boundary datum shdot(2)=0.
    # Integrate differentiated interpolants exactly, instead of interpolating
    # their derivatives a second time. R^2*qd is a degree-five piecewise polynomial.
    products=np.array([np.convolve(qd.c[::-1,i],[x*x,2*x,1])
                      for i,x in enumerate(qd.x[:-1])]).T[::-1]
    q_integral=PPoly(products,qd.x).antiderivative()
    matter_integral=CubicSpline(r,r**3*ent*S1).antiderivative()
    charge=amplitude*model.charge
    def sh_velocity(x,order=0):
        numerator=-(x**3*qd(x)-8*qd(2.))/2+3*(q_integral(x)-q_integral(2.))/2
        numerator-=3*charge*(Qd(x)-Qd(2.))
        numerator+=3*(matter_integral(x)-matter_integral(2.))/4
        value=numerator/x**3
        if order==0:return value
        return -qd(x,1)/2-3*charge*Qd(x,1)/x**3+3*matter_integral(x,1)/(4*x**3)-3*value/x
    shdot=sh_velocity(r); shdot1=sh_velocity(r,1)
    def field(x):
        return model.Sbar+anti(x)[1]-anti(8.)[1],sol.sol(x)[1],sol.sol(x,1)[1]
    return dict(model=model,r=r,S=S,S1=S1,S2=S2,old=old,base=base,fluids=fs,field=field,
                rho=rho,pressure=pressure,ent=ent,pw=pw,pw_ent=pw_ent,HQ=HQ,
                beta=beta,divb=divb,Qdot=Qdot,Qd=Qd,qdot=qdot,qd=qd,
                shdot=shdot,shdot1=shdot1,sh_velocity=sh_velocity,shift=shift,bp=bp,initial_mesh=sol.x)


def experiment(amplitude=1.,nodes=1601,table_index=1,align_breakpoints=False,repair_coefficients=True):
    model=exterior.models()[table_index]
    if repair_coefficients:model=hermite.repair(model)
    data=initial_slice(model,amplitude,nodes)
    r,S,S1,S2=(data[k] for k in ('r','S','S1','S2')); old=data['old']; b=data['base']
    rho,ent,pw,pwent=(data[k] for k in ('rho','ent','pw','pw_ent'))
    qdot,Qdot,shdot=(data[k] for k in ('qdot','Qdot','shdot'))
    Qd=data['Qd']; qd=data['qd']
    Cq=b['C_q']-b['C_z']*b['hqz']/b['hzz']
    source=Cq*qdot+b['C_sh']*shdot-3*data['HQ']*ent
    source+=b['C_Q']*Qdot+b['C_Q1']*Qd(r,1)+b['C_Q2']*Qd(r,2)
    coefficient=CubicSpline(r,np.array([b['C_S2'],b['C_S1'],old['potential'],source]).T)
    bg=model.evaluate(2.,model.Sbar,0.,0.,0.)
    bgx=evaluate(model,2.,model.Sbar,0.,0.,model.Q,0.,0.,model.q,bg['z'],0.)
    bg_ent=sum((1+f['w'])*f['h']*np.exp(model.Sbar-model.Sref) for f in data['fluids'])
    bg_pressure=sum(f['w']*f['h']*np.exp(model.Sbar-model.Sref) for f in data['fluids'])
    bgqdot=bgx['qdot']+3*bg_pressure/2
    bgCq=bgx['C_q']-bgx['C_z']*bgx['hqz']/bgx['hzz']
    Sdbar=float((3*bgx['hq']*bg_ent/2-bgCq*bgqdot)/bg['potential'])
    def direct_coefficients(x):
        sx,sx1,sx2=data['field'](x)
        ox=model.evaluate(x,sx,sx1,sx2,amplitude)
        bx=evaluate(model,x,sx,sx1,sx2,model.Q,0.,0.,model.q,ox['z'],ox['shear'])
        hx_ent=sum((1+f['w'])*f['h']*np.exp(sx-model.Sref) for f in data['fluids'])
        betax=-x*(data['shift'](x)-data['shift'](2.))
        divx=3*betax/x-x*data['shift'](x,1)
        src=(bx['C_q']-bx['C_z']*bx['hqz']/bx['hzz'])*qd(x)+bx['C_sh']*data['sh_velocity'](x)
        src+=bx['C_Q']*Qd(x)+bx['C_Q1']*Qd(x,1)+bx['C_Q2']*Qd(x,2)
        src+=(divx-3*Qd(x))*hx_ent
        return bx['C_S2'],bx['C_S1'],ox['potential'],src
    def rhs(x,y):
        a,c1,c0,src=direct_coefficients(x)
        return np.vstack((y[1],-(c1*y[1]+c0*y[0]+src)/a))
    # The fixed coefficient action and initial solution are piecewise smooth.
    # Put their actual joins on the solve mesh instead of refining blindly
    # toward undisclosed breakpoints of the differential-equation source.
    joins=list(data['initial_mesh'])+list(r) if align_breakpoints else list(r)
    boundary_precision=128*np.finfo(float).eps*max(1.,abs(S[0]),abs(S[-1]))
    if amplitude and align_breakpoints:
        for knot in model.table.x:
            # Do not seed a near-zero radial cell from a coefficient value
            # indistinguishable from the boundary S in this arithmetic.
            # The coefficient function itself is NOT snapped or modified.
            if S[-1]+boundary_precision<knot<S[0]-boundary_precision:
                joins.append(brentq(lambda x:data['field'](x)[0]-knot,2.,8.,xtol=1e-14))
    mesh=merge_mesh(joins)
    sol=solve_bvp(rhs,lambda l,rr:np.array([l[1],rr[0]-Sdbar]),mesh,
                  np.vstack((np.full(mesh.size,Sdbar),np.zeros(mesh.size))),tol=1e-9,max_nodes=60000)
    if not sol.success:
        worst=int(np.argmax(sol.rms_residuals)); point=(sol.x[worst]+sol.x[worst+1])/2
        value=data['field'](point)[0]
        return dict(solved=False,message=sol.message,amplitude=amplitude,
            align_breakpoints=align_breakpoints,
            repair_coefficients=repair_coefficients,
            nodes=nodes,final_nodes=sol.x.size,max_collocation_residual=(float(np.max(sol.rms_residuals))
                 if np.all(np.isfinite(sol.rms_residuals)) else 'nonfinite'),
            worst_interval=list(sol.x[worst:worst+2]),
            nearest_initial_mesh_distance=float(np.min(abs(data['initial_mesh']-point))),
            nearest_coefficient_knot_distance=float(np.min(abs(model.table.x-value))))
    anti=sol.sol.antiderivative()
    Sd=Sdbar+anti(r)[1]-anti(8.)[1]; Sd1=sol.sol(r)[1]; Sd2=sol.sol(r,1)[1]
    zd=-(b['hSz']*Sd+b['hqz']*qdot)/b['hzz']
    ell=-old['W']/old['Wcoef']
    time_jets={'S':Sd,'S1':Sd1,'S2':Sd2,'Q':Qdot,'Q1':Qd(r,1),'Q2':Qd(r,2),
               'q':qdot,'z':zd,'sh':shdot}
    Wdot=sum(b['W_'+k]*v for k,v in time_jets.items())-pw*Sd+3*data['HQ']*pwent
    elld=-np.exp(-S)*Wdot-ell*Sd
    Cdot=sum(b['C_'+k]*v for k,v in time_jets.items())+rho*Sd-3*data['HQ']*ent
    zpres=b['hSz']*Sd+b['hzz']*zd+b['hqz']*qdot
    wpres=Wdot+np.exp(S)*(elld+ell*Sd)
    mpres=2*qd(r,1)/3+4*data['shdot1']/3+4*shdot/r+4*old['shear']*Qd(r,1)-ent*S1
    beta_anti=CubicSpline(r,old['t']*(shdot+old['shear']*Sd)/r).antiderivative()
    betad=-r*(beta_anti(r)-beta_anti(2.))
    betad1=betad/r-r*beta_anti(r,1)
    shear_pres=old['t']*(shdot+old['shear']*Sd)+betad1-betad/r
    # Off-node audit: re-evaluate the actual action and the independently
    # represented jets, not the interpolated differential-equation coefficients.
    mid=(r[:-1]+r[1:])/2
    Sm,Sm1,Sm2=data['field'](mid)
    om=model.evaluate(mid,Sm,Sm1,Sm2,amplitude)
    bm=evaluate(model,mid,Sm,Sm1,Sm2,model.Q,0.,0.,model.q,om['z'],om['shear'])
    rm=sum(f['h']*np.exp(Sm-model.Sref) for f in data['fluids'])
    pm=sum(f['w']*f['h']*np.exp(Sm-model.Sref) for f in data['fluids'])
    Sdm=Sdbar+anti(mid)[1]-anti(8.)[1]
    shdm=data['sh_velocity'](mid)
    shdm1=data['sh_velocity'](mid,1)
    bmid=-mid*(data['shift'](mid)-data['shift'](2.))
    divmid=3*bmid/mid-mid*data['shift'](mid,1)
    zdm=-(bm['hSz']*Sdm+bm['hqz']*qd(mid))/bm['hzz']
    midjets=dict(S=Sdm,S1=sol.sol(mid)[1],S2=sol.sol(mid,1)[1],
                 Q=Qd(mid),Q1=Qd(mid,1),Q2=Qd(mid,2),q=qd(mid),z=zdm,sh=shdm)
    offC=sum(bm['C_'+k]*val for k,val in midjets.items())+rm*Sdm+(divmid-3*Qd(mid))*(rm+pm)
    offmom=2*qd(mid,1)/3+4*shdm1/3+4*shdm/mid+4*om['shear']*Qd(mid,1)-(rm+pm)*Sm1
    offshear=om['t']*(shdm+om['shear']*Sdm)-mid*beta_anti(mid,1)
    offq=qd(mid)-bm['qdot']-3*pm/2
    offQ=Qd(mid)-bm['hq']/2-divmid/3
    direct_mid_source=(bm['C_q']-bm['C_z']*bm['hqz']/bm['hzz'])*qd(mid)+bm['C_sh']*shdm
    direct_mid_source+=bm['C_Q']*Qd(mid)+bm['C_Q1']*Qd(mid,1)+bm['C_Q2']*Qd(mid,2)
    direct_mid_source+=(divmid-3*Qd(mid))*(rm+pm)

    def kick(dt,freeze=False):
        Sn=S if freeze else S+dt*Sd
        Sn1=S1 if freeze else S1+dt*Sd1; Sn2=S2 if freeze else S2+dt*Sd2
        zn=old['z'] if freeze else old['z']+dt*zd
        ln=ell if freeze else ell+dt*elld
        Qn=model.Q+dt*Qdot; qn=model.q+dt*qdot
        shn=old['shear']+dt*shdot
        new=evaluate(model,r,Sn,Sn1,Sn2,Qn,dt*Qd(r,1),dt*Qd(r,2),qn,zn,shn)
        hsum=np.zeros_like(r); pwsum=np.zeros_like(r); momentum=np.zeros_like(r); ferr=0.
        for f in data['fluids']:
            j=f['j']*(1+dt*data['divb'])*np.exp(-3*dt*Qdot)
            ui=np.exp(S)*(1+f['w'])*f['c']*f['j']**f['w']
            grad=dt*ui*S1
            fm=fluid(j,grad,Sn,Qn,f['w'],f['c'])
            hsum+=fm['h']; pwsum+=fm['pw']; momentum+=j*grad
            ferr=max(ferr,float(np.max(abs(fm['legendre_error']))))
        Cz=model.A*qn+2*model.table(Sn)*zn+4*model.E*zn**3
        mom=2*dt*qd(r,1)/3+4*(-3*old['shear']/r+dt*data['shdot1'])/3
        mom+=4*(dt*Qd(r,1)+1/r)*shn-momentum
        shear_gauge=2*np.exp(Sn-2*model.wc)/model.m*shn
        shear_gauge+=data['bp']+dt*betad1-(data['beta']+dt*betad)/r
        return dict(dt=dt,lapse=float(np.max(abs(new['C']+hsum))),
                    z=float(np.max(abs(Cz))),w=float(np.max(abs(new['W']-pwsum+np.exp(Sn)*ln))),
                    momentum=float(np.max(abs(mom))),shear_gauge=float(np.max(abs(shear_gauge))),
                    fluid_legendre_error=ferr,
                    min_pin_margin=float(np.min((-np.exp(-3*model.wc)*qn/(3*.5))**2-.75)))
    kicks=[kick(dt) for dt in (.001,.0005,.00025)]
    ratio_keys=('lapse','z','w','momentum','shear_gauge')
    ratios={k:kicks[0][k]/max(1e-30,kicks[1][k]) for k in ratio_keys}
    fine_ratios={k:kicks[1][k]/max(1e-30,kicks[2][k]) for k in ratio_keys}
    return dict(solved=True,amplitude=amplitude,nodes=nodes,table_index=table_index,
        align_breakpoints=align_breakpoints,
        repair_coefficients=repair_coefficients,
        preservation_mesh_nodes=sol.x.size,
        Sdot_background=Sdbar,Sdot_range=[float(np.min(Sd)),float(np.max(Sd))],
        qdot_range=[float(np.min(qdot)),float(np.max(qdot))],
        shdot_range=[float(np.min(shdot)),float(np.max(shdot))],
        elldot_range=[float(np.min(elld)),float(np.max(elld))],
        max_preservation_residual=float(max(np.max(abs(Cdot)),np.max(abs(offC)))),
        node_preservation_residual=float(np.max(abs(Cdot))),
        source_reinterpolation_error=float(np.max(abs(coefficient(mid)[:,3]-direct_mid_source))),
        offnode=dict(lapse=float(np.max(abs(offC))),momentum=float(np.max(abs(offmom))),
                     shear_gauge=float(np.max(abs(offshear))),q_euler=float(np.max(abs(offq))),
                     Q_euler=float(np.max(abs(offQ)))),
        z_preservation=float(np.max(abs(zpres))),w_preservation=float(np.max(abs(wpres))),
        momentum_preservation=float(np.max(abs(mpres))),shear_preservation=float(np.max(abs(shear_pres))),
        boundary_residuals=[float(Sd1[0]),float(Sd[-1]-Sdbar)],
        kicks=kicks,kick_ratios=ratios,kick_ratios_fine=fine_ratios,
        frozen_auxiliary_violation=kick(.001,True)['lapse'],
        first_order_only=True,full_theory='OPEN')


def coefficient_continuity(model):
    """Audit literal expanded floating coefficients with 80-digit evaluation."""
    maxima=[mp.mpf(0)]*3; locations=[None]*3
    with mp.workdps(80):
        for i in range(1,len(model.table.x)-1):
            left=[mp.mpf(v) for v in model.table.c[:,i-1]]
            right=[mp.mpf(v) for v in model.table.c[:,i]]
            dx=mp.mpf(model.table.x[i])-mp.mpf(model.table.x[i-1])
            for order in range(3):
                jump=abs(mp.polyval(left,dx)-mp.polyval(right,mp.mpf(0)))
                if jump>maxima[order]:maxima[order]=jump;locations[order]=float(model.table.x[i])
                degree=len(left)-1
                left=[c*(degree-j) for j,c in enumerate(left[:-1])]
                right=[c*(degree-j) for j,c in enumerate(right[:-1])]
        return dict(max_absolute_jumps=[mp.nstr(x,30) for x in maxima],S_at_max=locations,
            scope='Literal expanded float polynomials; not a proof of continuity of the underlying implicit D(S)')


def report():
    rows=[experiment(amp,n) for amp,n in ((0.,1601),(1.,1601),(1.,3201),(2.,1601))]
    rows.append(experiment(2.,1601,align_breakpoints=True))
    solved=[x for x in rows if x['solved']]
    checks=dict(symbolic=all(x==0 for x in identities().values()),
                all_requested_domains_solved=len(solved)==len(rows))
    if solved:
        checks.update(preservation=all(x['max_preservation_residual']<1e-5 for x in solved),
            auxiliary_preservation=all(max(x['z_preservation'],x['w_preservation'],x['momentum_preservation'],
                                          x['shear_preservation'])<1e-8 for x in solved),
            offnode_euler=all(max(x['offnode']['q_euler'],x['offnode']['Q_euler'])<1e-5 for x in solved),
            offnode_secondary=all(max(x['offnode']['momentum'],x['offnode']['shear_gauge'])<1e-5 for x in solved),
            unprojected_kicks=all(min(list(x['kick_ratios'].values())+list(x['kick_ratios_fine'].values()))>3.2
                                 for x in solved if x['amplitude']),
            negative_control=all(x['frozen_auxiliary_violation']>x['kicks'][0]['lapse'] for x in solved),
            fluid_legendre=all(k['fluid_legendre_error']<1e-12 and k['min_pin_margin']>0
                              for x in solved for k in x['kicks']))
    return dict(checks=checks,rows=rows,coefficient_continuity=coefficient_continuity(exterior.models()[1]),
                full_theory='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--strict',action='store_true')
    parser.add_argument('--legacy-control',action='store_true')
    args=parser.parse_args()
    if args.legacy_control:
        row=experiment(2.,1601,repair_coefficients=False)
        out=dict(checks=dict(legacy_solved=row['solved']),row=row,full_theory='OPEN',
                 coefficient_continuity=coefficient_continuity(exterior.models()[1]))
    else:out=report()
    print(json.dumps(out,indent=2))
    raise SystemExit(1 if not all(out['checks'].values()) else 2 if args.strict else 0)
