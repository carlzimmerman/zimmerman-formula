#!/usr/bin/env python3
"""Full generalized-action Solar quadrupole for three fixed noninteger powers."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import time
import numpy as np
from numpy.polynomial.legendre import leggauss

HERE=Path(__file__).resolve().parent;RB=HERE.parents[1]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


base=load('kt39_solar_readonly_kt38',RB/'KT38_weak_field_curvature/cassini/calculate.py')
law=load('kt39_solar_action',HERE.parent/'analytic/law.py')
old=base.old;KPC=base.KPC;CC=base.CC
POWERS=[1.25,1.5,1.75];LENGTHS=[1.5,2.,2.5,3.,3.5,4.]


def curvature(s,sp,spp,ell,p):
    if ell==0:
        zz=np.zeros_like(s)
        return zz,zz,zz,zz,zz,zz
    assert np.all(s>0)
    u=sp/s;v=spp/s
    h=s**p;hp=h*p*u;hpp=h*(p*v+p*(p-1)*u*u)
    beta=p*ell*ell*s**(p-1)
    betap=beta*(p-1)*u
    betapp=beta*((p-1)*v+(p-1)*(p-2)*u*u)
    return h,hp,hpp,beta,betap,betapp


def contacts(eta,ell,sigma,p,newtonian=False):
    if sigma==0 or eta==0 or newtonian:return 0.,0.
    k=CC/(3*sigma**3);x=eta*eta;s=3*ell*ell*k*k;z=np.array(x+s**p)
    _,d1,d2,d3=base.scaled_R(z);f=x/z
    beta=0. if ell==0 else p*ell*ell*s**(p-1)
    cx=(2*d1+f*d2)/z;dxx=beta/z*(2*d2+f*d3)/z
    return float(8*k*x*cx/15),float(-8*k**3*x*dxx/3)


def quadrupole(eta,ell,p,sigma=0.,nr=8000,nm=160,rmin=1e-8,rmax=1e6,newtonian=False):
    uu=np.linspace(math.log(rmin),math.log(rmax),nr);r=np.exp(uu)
    mu,w=leggauss(nm);mu=mu[None,:];angular_p=3*mu*mu-1
    qa=np.zeros(nr);qb=np.zeros(nr);qad=np.zeros(nr);qbd=np.zeros(nr)
    sa=np.zeros(nr);sb=np.zeros(nr)
    for first in range(0,nr,128):
        sl=slice(first,min(first+128,nr));rr=r[sl,None]
        g,gp,gpp,gppp,tt,tp,tpp=base.prior.radial(rr,sigma)
        gt=g/rr;gtp=(gp-gt)/rr;gtpp=gpp/rr-2*gp/rr**2+2*g/rr**3
        ss=ell*ell*(gp*gp+2*gt*gt)
        ssp=ell*ell*(2*gp*gpp+4*gt*gtp)
        sspp=ell*ell*(2*gpp*gpp+2*gp*gppp+4*gtp*gtp+4*gt*gtpp)
        hh,hhp,hhpp,beta,betap,betapp=curvature(ss,ssp,sspp,ell,p)
        x=g*g+eta*eta+2*g*eta*mu;xr=2*gp*(g+eta*mu)
        xrr=2*gp*gp+2*gpp*(g+eta*mu)
        vals=base.coefficients(x,x+hh,xr,xr+hhp,xrr,xrr+hhpp,beta,betap,betapp,newtonian)
        x0=g*g+eta*eta;xr0=2*gp*g;xrr0=2*gp*gp+2*gpp*g
        refs=base.coefficients(x0,x0+hh,xr0,xr0+hhp,xrr0,xrr0+hhpp,beta,betap,betapp,newtonian)
        c,cr,d,dr,drr=[a-b for a,b in zip(vals,refs)]
        av=(c*(g+eta*mu)*angular_p)@w
        bv=(c*(eta*(3*mu-5*mu**3)+g*(1-3*mu*mu)))@w
        apr=((cr*(g+eta*mu)+c*gp)*angular_p)@w
        dv=(d*angular_p)@w;dpr=(dr*angular_p)@w;dppr=(drr*angular_p)@w
        rad=rr[:,0];gpv=gp[:,0];gtv=gt[:,0];tpv=tp[:,0]
        qa[sl]=1.5*bv/rad;qb[sl]=6*(gpv-gtv)*dv/rad**2
        da=apr-av/rad-3*bv/rad
        db=gpv*dppr+(gpp[:,0]+tpv+2*gpv/rad)*dpr+(tpp[:,0]+2*tpv/rad-6*gtv/rad**2)*dv
        qad[sl]=-.5*da;qbd[sl]=.5*db
        sa[sl]=.5*av/rad;sb[sl]=.5*(gpv*dpr/rad+tpv*dv/rad+3*gpv*dv/rad**2)
    aa=float(np.trapz(qa,uu));bb=float(np.trapz(qb,uu))
    ac,bc=contacts(eta,ell,sigma,p,newtonian)
    q=aa+bb-sa[-1]+sb[-1]+ac+bc
    qdensity=float(np.trapz(qad+qbd,uu))
    annulus=aa+bb-sa[-1]+sa[0]+sb[-1]-sb[0]
    return dict(q_signed=float(q),q_A_flux=aa,q_B_flux=bb,q_A_contact=ac,q_B_contact=bc,
        q_density=qdensity,flux_density_difference=float(q-qdensity),annulus_identity_difference=float(annulus-qdensity),
        outer_A_surface=float(sa[-1]),outer_B_surface=float(sb[-1]),
        finite_inner_A_surface=float(sa[0]),finite_inner_B_surface=float(sb[0]),
        power=p,ell_rM=ell,sigma_rM=sigma,nr=nr,nm=nm,rmin=rmin,rmax=rmax)


def api_check(p):
    errors=[]
    for rr in [.01,.3,1.,10.]:
        for ell in [.3,3000.]:
            for mu in [-.7,0.,.8]:
                n=np.array([math.sqrt(1-mu*mu),0.,mu]);gv=n/rr**2+np.array([0.,0.,2.48])
                hh=(np.eye(3)-3*np.outer(n,n))/rr**3
                out=law.tensor_terms(gv,hh,ell,p=p)
                x=float(gv@gv);s=ell*ell*float(np.sum(hh*hh));z=np.array(x+s**p)
                c,_,d,_,_=base.coefficients(np.array(x),z,0.,0.,0.,0.,p*ell*ell*s**(p-1),0.,0.,False)
                errors.append(float(np.max(np.abs(c*gv-out['A']))/max(np.max(np.abs(out['A'])),1e-300)))
                errors.append(float(np.max(np.abs(d*hh-out['B']))/max(np.max(np.abs(out['B'])),1e-300)))
    return dict(cases=24,max_relative_error=max(errors),passed=max(errors)<1e-12)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();started=time.monotonic()
    out=dict(law='full P=xQ(z)/z, z=x+(ell²H:H)^p',powers=POWERS,lengths_kpc=LENGTHS,
        footings={},checks={},api={str(p):api_check(p) for p in POWERS})
    out['checks']['tensor_API']=all(x['passed'] for x in out['api'].values())
    for foot,a0 in old.A0.items():
        eta=old.GEXT/a0;rm=math.sqrt(old.GM/a0)
        ff=out['footings'][foot]=dict(a0=a0,eta=eta,powers={},shared_zero_length_controls={})
        point=quadrupole(eta,0.,POWERS[0],nr=12000,nm=240)
        ref=old.quadrupole(eta,0.,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        ff['shared_zero_length_controls']['plain']=base.prior.physical(point,a0)
        out['checks'][foot+'|plain']=abs(point['q_signed']-ref['q_hessian_signed'])<1e-9
        smooth=quadrupole(eta,0.,POWERS[0],sigma=.5,nr=12000,nm=240)
        ref=old.quadrupole(eta,.5,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        ff['shared_zero_length_controls']['smooth']=base.prior.physical(smooth,a0)
        out['checks'][foot+'|smooth_zero_length']=abs(smooth['q_signed']-ref['q_flux_signed']-ref['analytic_inner_surface'])<1e-9
        for p in POWERS:
            rows=ff['powers'][str(p)]=dict(physical_lengths={},controls={})
            for length in LENGTHS:
                ell=length*KPC/rm
                coarse=base.prior.physical(quadrupole(eta,ell,p),a0)
                fine=base.prior.physical(quadrupole(eta,ell,p,nr=16000,nm=320,rmin=1e-10,rmax=1e7),a0)
                rows['physical_lengths'][str(length)]=dict(base=coarse,fine=fine)
                scale=max(abs(fine['q_signed']),1e-12);key=f'{foot}|p{p}|ell{length}'
                out['checks'][key+'|refinement']=abs(coarse['q_signed']-fine['q_signed'])/scale<2e-4
                out['checks'][key+'|density']=abs(fine['flux_density_difference'])/scale<2e-4
                print(foot,p,length,'qA',fine['q_A_flux'],'qB',fine['q_B_flux'],'ratio',fine['x_ceiling'],'densitydiff',fine['flux_density_difference'],flush=True)
            rows['controls']['newtonian']=quadrupole(eta,1000.,p,sigma=.1,nr=1000,nm=40,newtonian=True)
            out['checks'][f'{foot}|p{p}|newton']=rows['controls']['newtonian']['q_signed']==0.
            ell=1.5*KPC/rm;point=rows['physical_lengths']['1.5']['fine']['q_signed'];reg=[]
            for sigma in [.5,.1,.01,.001,5e-7]:
                row=quadrupole(eta,ell,p,sigma,nr=12000,nm=240,rmin=max(1e-10,.001*sigma),rmax=1e7)
                row['point_relative_difference']=abs(row['q_signed']/point-1);reg.append(row)
            rows['controls']['shrinking_gaussian']=reg
            out['checks'][f'{foot}|p{p}|regularization']=max(x['point_relative_difference'] for x in reg[-3:])<2e-4
            out['checks'][f'{foot}|p{p}|core_density']=max(abs(x['flux_density_difference'])/max(abs(x['q_signed']),1e-12) for x in reg)<2e-4
            family=[dict(reg[0],inner_fraction_of_sigma=.001)]
            for frac in [.0005,.00025]:
                row=quadrupole(eta,ell,p,.5,nr=12000,nm=240,rmin=frac*.5,rmax=1e7)
                row['inner_fraction_of_sigma']=frac;family.append(row)
            rows['controls']['core_cutoff']=family
            out['checks'][f'{foot}|p{p}|core_radius']=max(x['q_signed'] for x in family)-min(x['q_signed'] for x in family)<1e-10
            out['checks'][f'{foot}|p{p}|core_absolute_density']=max(abs(x['flux_density_difference']) for x in family)<1e-10
    out['zero_external']={str(p):quadrupole(0.,1000.,p,sigma=.1,nr=1000,nm=40) for p in POWERS}
    out['checks']['zero_external']=all(x['q_signed']==0. for x in out['zero_external'].values())
    a0=old.A0['canonical'];eta=old.GEXT/a0;ell=3*KPC/math.sqrt(old.GM/a0)
    old37=json.loads((RB/'KT37_generalized_action/cassini/run_002/results.json').read_text())
    old38=json.loads((RB/'KT38_weak_field_curvature/cassini/run_001/results.json').read_text())
    out['endpoint_controls']={}
    for p,reference in [(1.,old37),(2.,old38)]:
        now=quadrupole(eta,ell,p,nr=16000,nm=320,rmin=1e-10,rmax=1e7)
        expected=reference['footings']['canonical']['physical_lengths']['3.0']['fine']['q_signed']
        err=abs(now['q_signed']/expected-1)
        out['endpoint_controls'][str(p)]=dict(row=now,reference_q=expected,relative_error=err)
        out['checks'][f'endpoint_p{p}']=err<1e-7
    out['all_checks_pass']=all(out['checks'].values());out['runtime_seconds']=time.monotonic()-started
    out['outcome']='finite 18-choice, two-footing constant-external-field quadrupoles with full A/B variation; no global parameter theorem'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('all checks',out['all_checks_pass'],'runtime',out['runtime_seconds'],flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
