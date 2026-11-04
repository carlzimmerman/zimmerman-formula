"""Independent adjoint/kernel checks, exterior-source control, and targeted Solar crossing."""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.integrate import quad_vec
from scipy.optimize import brentq
import calculate_v2 as M

M.leggauss = lru_cache(maxsize=None)(M.leggauss)


def adjoint_energy_check():
    n = 13
    x = np.arange(n)*2*np.pi/n
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    psi = .2*np.sin(X)+.13*np.cos(Y+Z)+.07*np.sin(2*X-Y)
    variation = .3*np.cos(X+Y)+.12*np.sin(Y+Z)+.14*np.sin(2*X-Y)
    k = np.fft.fftfreq(n, d=1/n)
    ks = np.meshgrid(k, k, k, indexing='ij')
    filt = np.exp(-.5*.6**2*sum(ki*ki for ki in ks))
    def deriv(v, i, j=None):
        symbol = 1j*ks[i] if j is None else -ks[i]*ks[j]
        return np.fft.ifftn(symbol*np.fft.fftn(v)).real
    def smooth(v):
        return np.fft.ifftn(filt*np.fft.fftn(v)).real
    def fields(v):
        g = np.stack([deriv(v,i) for i in range(3)], axis=-1)+np.array([.8,.3,.6])
        h = np.stack([np.stack([smooth(deriv(v,i,j)) for j in range(3)],axis=-1) for i in range(3)],axis=-2)
        return g,h
    g,h=fields(psi)
    terms=M.C.law.tensor_terms(g,h,1.7,p=M.P)
    dg,dh=fields(variation);dg-=np.array([.8,.3,.6])
    predicted=2*np.mean(np.sum((g+terms['A'])*dg,axis=-1)+np.sum(terms['B']*dh,axis=(-2,-1)))
    source=sum(deriv(g[...,i]+terms['A'][...,i],i) for i in range(3))
    source-=sum(deriv(smooth(terms['B'][...,i,j]),i,j) for i in range(3) for j in range(3))
    wrong=sum(deriv(g[...,i]+terms['A'][...,i],i) for i in range(3))
    wrong-=sum(deriv(terms['B'][...,i,j],i,j) for i in range(3) for j in range(3))
    weak=-2*np.mean(source*variation);wrong_weak=-2*np.mean(wrong*variation)
    fd=[]
    for eps in [1e-3,3e-4,1e-4]:
        gp,hp=fields(psi+eps*variation);gm,hm=fields(psi-eps*variation)
        ep=np.mean(M.C.law.tensor_terms(gp,hp,1.7,p=M.P)['energy'])
        em=np.mean(M.C.law.tensor_terms(gm,hm,1.7,p=M.P)['energy'])
        fd.append(dict(epsilon=eps,derivative=float((ep-em)/(2*eps)),error=float(abs((ep-em)/(2*eps)-predicted))))
    return dict(predicted=float(predicted),weak_adjoint=float(weak),missing_return=float(wrong_weak),finite_differences=fd,
                passed=bool(abs(predicted-weak)<1e-12 and fd[-1]['error']<1e-8 and abs(wrong_weak-weak)>1e-4))


def cartesian_kernel_check():
    def F(v):
        r=np.linalg.norm(v);mu=v[2]/r
        t=M.softened_tidal(np.array([r]),1.)[2][0]
        return t*(3*mu*mu-1)/3
    rows=[]
    for r in [.03,.3,1.,3.]:
        for mu in [-.63,.17,.81]:
            n=np.array([math.sqrt(1-mu*mu),0.,mu]);v=r*n
            hr,ht,t,tp,tpp=[a[0] for a in M.softened_tidal(np.array([r]),1.)]
            hh=ht*np.eye(3)+(hr-ht)*np.outer(n,n)
            expected=(3*mu*mu-1)/3*(hr*tpp+ht*(2*tp/r-6*t/r**2))
            values=[]
            for step in [2e-3,1e-3,5e-4]:
                hes=np.zeros((3,3));basis=np.eye(3)*step
                for i in range(3):
                    hes[i,i]=(F(v+basis[i])-2*F(v)+F(v-basis[i]))/step**2
                    for j in range(i):
                        hes[i,j]=hes[j,i]=(F(v+basis[i]+basis[j])-F(v+basis[i]-basis[j])-F(v-basis[i]+basis[j])+F(v-basis[i]-basis[j]))/(4*step**2)
                values.append(float(np.sum(hh*hes)))
            error=abs(values[-1]-expected)
            rows.append(dict(r=r,mu=mu,expected=float(expected),finite_difference=values,absolute_error=float(error)))
    return dict(rows=rows,max_absolute_error=max(r['absolute_error'] for r in rows),passed=max(r['absolute_error'] for r in rows)<2e-8)


def adaptive_radial(eta,ell,width,nm=256):
    lo,hi=math.log(1e-10),math.log(1e7)
    anchors=[math.log(1/math.sqrt(eta)),math.log(width),math.log(ell**(1/3))]
    anchors=[v for v in anchors if lo<v<hi]
    def fun(u):
        a,b=M.integrands(np.array([math.exp(u)]),eta,ell,width,nm)
        return np.array([a[0],b[0]])
    val,err=quad_vec(fun,lo,hi,epsabs=2e-11,epsrel=2e-8,points=anchors,limit=300)
    return dict(q_A=float(val[0]),q_B=float(val[1]),q_signed=float(sum(val)),reported_error=float(err))


def exterior_A(eta,ell,width,R,sigma,nr=8000,nm=256):
    mu,w=M.leggauss(nm);mu=mu[None,:];pol=3*mu*mu-1
    def ab(r):
        rr=r[:,None]
        g=M.C.base.prior.radial(rr,sigma)[0]
        hr,ht,*_=M.softened_tidal(rr,math.hypot(width,sigma))
        hh=(ell*ell*(hr*hr+2*ht*ht))**M.P
        x=g*g+eta*eta+2*g*eta*mu;x0=g*g+eta*eta
        rm,d1,*_=M.C.base.scaled_R(x+hh);rm0,d10,*_=M.C.base.scaled_R(x0+hh)
        c=(rm+x/(x+hh)*d1)-(rm0+x0/(x0+hh)*d10)
        av=np.sum(c*(g+eta*mu)*pol*w,axis=1)
        bv=np.sum(c*(eta*(3*mu-5*mu**3)+g*(1-3*mu*mu))*w,axis=1)
        return av,bv
    pieces=[]
    for inner,(lo,hi) in enumerate([(R,1e7),(1e-14,R)]):
        u=np.linspace(math.log(lo),math.log(hi),nr);r=np.exp(u);f=np.zeros(nr)
        for start in range(0,nr,128):
            sl=slice(start,min(nr,start+128));aa,bb=ab(r[sl])
            f[sl]=(5*aa+3*bb)*r[sl]**4/(2*R**5) if inner else 1.5*bb/r[sl]
        pieces.append(float(np.trapz(f,u)))
    return dict(q_A_effective=sum(pieces),outer=pieces[0],inner=pieces[1],source_sigma_rM=sigma,observable_radius_rM=R)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    started=time.monotonic();baseline=json.loads((M.HERE/'run_002/results.json').read_text())
    out=dict(adjoint=adjoint_energy_check(),cartesian_kernel=cartesian_kernel_check(),footings={},checks={})
    out['checks']['full_adjoint']=out['adjoint']['passed'];out['checks']['Cartesian_B_kernel']=out['cartesian_kernel']['passed']
    lengths_pc=[.2,.3,.4,.5,.6,.7,.8,.9,1.5,2.,5.]
    for foot,a0 in M.C.old.A0.items():
        eta=M.C.old.GEXT/a0;rm=math.sqrt(M.C.old.GM/a0);ell=3*M.C.KPC/rm;unit=M.C.KPC/rm/1000
        pref=1.5*a0/rm/M.C.old.CEILING
        ff=out['footings'][foot]=dict(lengths_pc=lengths_pc,rows={},crossing_evaluations=[])
        for pc in lengths_pc:
            base=M.quadrupole(eta,ell,pc*unit,nr=4000,nm=128)
            fine=M.quadrupole(eta,ell,pc*unit,nr=8000,nm=256,rmin=1e-10,rmax=1e7)
            ff['rows'][str(pc)]=dict(base=M.C.base.prior.physical(base,a0),fine=M.C.base.prior.physical(fine,a0))
            out['checks'][f'{foot}|{pc}|refinement']=abs(abs(base['q_signed'])-abs(fine['q_signed']))*pref<2e-4
        def objective(pc):
            value=M.quadrupole(eta,ell,pc*unit,nr=5000,nm=192)
            ratio=abs(value['q_signed'])*pref
            ff['crossing_evaluations'].append(dict(a_pc=float(pc),ratio=float(ratio)))
            return ratio-1
        crossing=brentq(objective,.1,1.,xtol=2e-7,rtol=2e-7)
        independent=adaptive_radial(eta,ell,crossing*unit)
        ff['crossing']=dict(a_pc=crossing,adaptive=independent,adaptive_ratio=abs(independent['q_signed'])*pref,
                            interpretation='one bracketed numerical crossing; not a global uniqueness or no-island theorem')
        out['checks'][foot+'|crossing_adaptive']=abs(abs(independent['q_signed'])*pref-1)<2e-4
        # A exterior multipole at Saturn, at an enlarged10-Solar-radius core and a shrinking core.
        R=9.58*M.C.old.AU/rm
        ff['exterior_A']={}
        for pc in [.1,1.,100.]:
            values=[exterior_A(eta,ell,pc*unit,R,sigma) for sigma in [0.,5e-6,5e-7]]
            reference=M.quadrupole(eta,ell,pc*unit,nr=8000,nm=256,rmin=1e-10,rmax=1e7)['q_A']
            ff['exterior_A'][str(pc)]=dict(rows=values,point_regular_qA=reference,ceiling_scaled_difference=(values[-1]['q_A_effective']-reference)*pref)
            out['checks'][f'{foot}|{pc}|exterior_core']=max(abs(v['q_A_effective']-values[0]['q_A_effective']) for v in values)*pref<2e-5
            out['checks'][f'{foot}|{pc}|exterior_vs_regular']=abs(values[-1]['q_A_effective']-reference)*pref<2e-4
        print(foot,'crossing_pc',crossing,'adaptive_ratio',ff['crossing']['adaptive_ratio'],flush=True)
    out['all_checks_pass']=all(out['checks'].values());out['runtime_seconds']=time.monotonic()-started
    out['scope']='Independent action/Cartesian observable controls and empirically converged finite Solar grid; no all-width exclusion.'
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('all checks',out['all_checks_pass'],'seconds',out['runtime_seconds'],flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
