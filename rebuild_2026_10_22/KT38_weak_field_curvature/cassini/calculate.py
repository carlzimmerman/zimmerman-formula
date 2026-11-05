#!/usr/bin/env python3
"""Full A/B Cassini diagnostic for z=x+(ell² H:H)²; import safe."""
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


prior=load('kt38_cassini_kt37_reference',RB/'KT37_generalized_action/cassini/calculate.py')
law=load('kt38_cassini_action',HERE.parent/'analytic/law.py')
old=prior.old;KPC=prior.KPC;CC=prior.CC


def scaled_R(z):
    rm=law.Rminus1(z);d1=law.zRprime(z);y=np.sqrt(z)
    zqp=-.5/np.sqrt(y)/np.sqrt(y+4)
    z2qpp=.25*(3*y+10)/(np.sqrt(y)*np.sqrt(y+4)*(y+4))
    d2=zqp-2*d1;d3=z2qpp-3*zqp+6*d1
    return rm,d1,d2,d3


def coefficients(x,z,xr,zr,xrr,zrr,beta,betap,betapp,newtonian):
    if newtonian:return (np.zeros_like(x),)*5
    rm,d1,d2,d3=scaled_R(z)
    f=x/z;u=zr/z;v=zrr/z;xxr=xr/z;xxrr=xrr/z
    c=rm+f*d1;cr=xxr*d1+(d1+f*d2)*u
    ee=f*d1;ep=xxr*d1+f*d2*u
    epp=xxrr*d1+2*xxr*d2*u+f*d3*u*u+f*d2*v
    dd=beta*ee;dp=betap*ee+beta*ep
    dpp=betapp*ee+2*betap*ep+beta*epp
    return c,cr,dd,dp,dpp


def contacts(eta,ell,sigma,newtonian=False):
    if sigma==0 or newtonian:return 0.,0.
    k=CC/(3*sigma**3);x=eta*eta;s=3*ell*ell*k*k;z=np.array(x+s*s)
    _,d1,d2,d3=scaled_R(z);f=x/z;beta=2*ell*ell*s
    cx=(2*d1+f*d2)/z
    dxx=beta/z*(2*d2+f*d3)/z
    return float(8*k*x*cx/15),float(-8*k**3*x*dxx/3)


def quadrupole(eta,ell,sigma=0.,nr=8000,nm=160,rmin=1e-8,rmax=1e6,newtonian=False):
    uu=np.linspace(math.log(rmin),math.log(rmax),nr);r=np.exp(uu)
    mu,w=leggauss(nm);mu=mu[None,:];p=3*mu*mu-1
    qa=np.zeros(nr);qb=np.zeros(nr);qad=np.zeros(nr);qbd=np.zeros(nr)
    sa=np.zeros(nr);sb=np.zeros(nr)
    for first in range(0,nr,128):
        sl=slice(first,min(first+128,nr));rr=r[sl,None]
        g,gp,gpp,gppp,tt,tp,tpp=prior.radial(rr,sigma)
        gt=g/rr;gtp=(gp-gt)/rr;gtpp=gpp/rr-2*gp/rr**2+2*g/rr**3
        ss=ell*ell*(gp*gp+2*gt*gt)
        ssp=ell*ell*(2*gp*gpp+4*gt*gtp)
        sspp=ell*ell*(2*gpp*gpp+2*gp*gppp+4*gtp*gtp+4*gt*gtpp)
        hh=ss*ss;hhp=2*ss*ssp;hhpp=2*ssp*ssp+2*ss*sspp
        beta=2*ell*ell*ss;betap=2*ell*ell*ssp;betapp=2*ell*ell*sspp
        x=g*g+eta*eta+2*g*eta*mu;xr=2*gp*(g+eta*mu)
        xrr=2*gp*gp+2*gpp*(g+eta*mu)
        vals=coefficients(x,x+hh,xr,xr+hhp,xrr,xrr+hhpp,beta,betap,betapp,newtonian)
        x0=g*g+eta*eta;xr0=2*gp*g;xrr0=2*gp*gp+2*gpp*g
        refs=coefficients(x0,x0+hh,xr0,xr0+hhp,xrr0,xrr0+hhpp,beta,betap,betapp,newtonian)
        c,cr,d,dr,drr=[a-b for a,b in zip(vals,refs)]
        av=(c*(g+eta*mu)*p)@w
        bv=(c*(eta*(3*mu-5*mu**3)+g*(1-3*mu*mu)))@w
        apr=((cr*(g+eta*mu)+c*gp)*p)@w
        dv=(d*p)@w;dpr=(dr*p)@w;dppr=(drr*p)@w
        rad=rr[:,0];gpv=gp[:,0];gtv=gt[:,0];tpv=tp[:,0]
        qa[sl]=1.5*bv/rad;qb[sl]=6*(gpv-gtv)*dv/rad**2
        da=apr-av/rad-3*bv/rad
        db=gpv*dppr+(gpp[:,0]+tpv+2*gpv/rad)*dpr+(tpp[:,0]+2*tpv/rad-6*gtv/rad**2)*dv
        qad[sl]=-.5*da;qbd[sl]=.5*db
        sa[sl]=.5*av/rad;sb[sl]=.5*(gpv*dpr/rad+tpv*dv/rad+3*gpv*dv/rad**2)
    aa=float(np.trapz(qa,uu));bb=float(np.trapz(qb,uu))
    ac,bc=contacts(eta,ell,sigma,newtonian)
    q=aa+bb-sa[-1]+sb[-1]+ac+bc
    qdensity=float(np.trapz(qad+qbd,uu))
    annulus=aa+bb-sa[-1]+sa[0]+sb[-1]-sb[0]
    return dict(q_signed=float(q),q_A_flux=aa,q_B_flux=bb,q_A_contact=ac,q_B_contact=bc,
        q_density=qdensity,flux_density_difference=float(q-qdensity),annulus_identity_difference=float(annulus-qdensity),
        outer_A_surface=float(sa[-1]),outer_B_surface=float(sb[-1]),
        finite_inner_A_surface=float(sa[0]),finite_inner_B_surface=float(sb[0]),
        ell_rM=ell,sigma_rM=sigma,nr=nr,nm=nm,rmin=rmin,rmax=rmax)


def api_checks():
    errors=[]
    for rr in [.01,.3,1.,10.]:
        for ell in [.3,3000.]:
            for mu in [-.7,0.,.8]:
                n=np.array([math.sqrt(1-mu*mu),0.,mu]);gv=n/rr**2+np.array([0.,0.,2.48])
                hh=(np.eye(3)-3*np.outer(n,n))/rr**3
                out=law.tensor_terms(gv,hh,ell)
                x=float(gv@gv);s=ell*ell*float(np.sum(hh*hh));z=np.array(x+s*s)
                c,_,d,_,_=coefficients(np.array(x),z,0.,0.,0.,0.,2*ell*ell*s,0.,0.,False)
                errors.append(float(np.max(np.abs(c*gv-out['A']))/max(np.max(np.abs(out['A'])),1e-300)))
                errors.append(float(np.max(np.abs(d*hh-out['B']))/max(np.max(np.abs(out['B'])),1e-300)))
    return dict(cases=24,max_relative_error=max(errors),passed=max(errors)<1e-12)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();start=time.monotonic()
    out=dict(law='full P=xQ(z)/z, z=x+(ell²H:H)²; Q(0)=0, simple nu',footings={},checks={},api_check=api_checks())
    out['checks']['tensor_API']=out['api_check']['passed']
    for foot,a0 in old.A0.items():
        eta=old.GEXT/a0;rm=math.sqrt(old.GM/a0)
        rows=out['footings'][foot]=dict(a0=a0,eta=eta,physical_lengths={},controls={})
        point=quadrupole(eta,0.,nr=12000,nm=240)
        reference=old.quadrupole(eta,0.,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        rows['controls']['plain']=prior.physical(point,a0)
        out['checks'][foot+'|plain_reproduction']=abs(point['q_signed']-reference['q_hessian_signed'])<1e-9
        smooth=quadrupole(eta,0.,sigma=.5,nr=12000,nm=240)
        smooth_ref=old.quadrupole(eta,.5,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        corrected_ref=smooth_ref['q_flux_signed']+smooth_ref['analytic_inner_surface']
        rows['controls']['plain_gaussian_core']=prior.physical(smooth,a0)
        out['checks'][foot+'|smooth_origin_contact']=abs(smooth['q_signed']-corrected_ref)<1e-9
        rows['controls']['newtonian']=quadrupole(eta,1000.,sigma=.1,nr=1000,nm=40,newtonian=True)
        out['checks'][foot+'|newtonian']=rows['controls']['newtonian']['q_signed']==0.
        for length in [.3,1.,3.,5.,10.]:
            ell=length*KPC/rm;base=prior.physical(quadrupole(eta,ell),a0)
            fine=prior.physical(quadrupole(eta,ell,nr=16000,nm=320,rmin=1e-10,rmax=1e7),a0)
            rows['physical_lengths'][str(length)]=dict(base=base,fine=fine)
            scale=max(abs(fine['q_signed']),1e-12)
            out['checks'][foot+f'|{length}|refinement']=abs(base['q_signed']-fine['q_signed'])/scale<2e-4
            out['checks'][foot+f'|{length}|density']=abs(fine['flux_density_difference'])/scale<2e-4
            print(foot,length,'qA',fine['q_A_flux'],'qB',fine['q_B_flux'],'q',fine['q_signed'],'ratio',fine['x_ceiling'],'densitydiff',fine['flux_density_difference'],flush=True)
        ell=.3*KPC/rm;reg=[];point=rows['physical_lengths']['0.3']['fine']['q_signed']
        for sigma in [.5,.1,.01,.001,5e-7]:
            rr=prior.physical(quadrupole(eta,ell,sigma,nr=12000,nm=240,rmin=max(1e-10,.001*sigma),rmax=1e7),a0)
            rr['point_relative_difference']=abs(rr['q_signed']/point-1);reg.append(rr)
        rows['controls']['shrinking_gaussian']=reg
        out['checks'][foot+'|point_regularization']=max(x['point_relative_difference'] for x in reg[-3:])<2e-4
        out['checks'][foot+'|regularized_density']=max(abs(x['flux_density_difference'])/max(abs(x['q_signed']),1e-12) for x in reg)<2e-4
        core=[]
        for sigma in [.5,.1]:
            family=[]
            for frac in [.001,.0005,.00025]:
                q=quadrupole(eta,ell,sigma,nr=12000,nm=240,rmin=frac*sigma,rmax=1e7)
                q['inner_fraction_of_sigma']=frac;family.append(q)
            core.append(dict(sigma=sigma,rows=family))
            out['checks'][foot+f'|{sigma}|inner_radius']=max(x['q_signed'] for x in family)-min(x['q_signed'] for x in family)<1e-10
            out['checks'][foot+f'|{sigma}|inner_density']=max(abs(x['flux_density_difference']) for x in family)<1e-10
        rows['controls']['core_cutoff']=core
    spherical=quadrupole(0.,1000.,sigma=.1,nr=1000,nm=40)
    out['controls_zero_external']=spherical;out['checks']['zero_external']=spherical['q_signed']==0.
    out['all_checks_pass']=all(out['checks'].values());out['runtime_seconds']=time.monotonic()-start
    out['outcome']='finite constant-external-field quadrupole, full variation and Gaussian point limit; empirical quadrature errors'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('all checks',out['all_checks_pass'],'runtime',out['runtime_seconds'],flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
