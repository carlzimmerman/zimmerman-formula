#!/usr/bin/env python3
"""Full generalized-action Solar quadrupole, with smooth-origin contacts."""
import argparse
import json
import math
from pathlib import Path
import sys
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import gammainc

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'analytic'))
import law
RB=HERE.parents[1]
sys.path.insert(0,str(RB/'KT33_reciprocal_filter/cassini'))
import cassini_v2 as old
KPC=3.0856775814913673e19
CC=math.sqrt(2/math.pi)


def radial(r,sigma):
    if sigma==0:
        g=r**-2;gp=-2*r**-3;gpp=6*r**-4;gppp=-24*r**-5
        return g,gp,gpp,gppp,np.zeros_like(r),np.zeros_like(r),np.zeros_like(r)
    u=r/sigma
    g=gammainc(1.5,.5*u*u)/r**2
    tt=CC/sigma**3*np.exp(-.5*u*u)
    tp=-r/sigma**2*tt;tpp=(r*r/sigma**4-1/sigma**2)*tt
    gp=tt-2*g/r;gpp=tp-2*gp/r+2*g/r**2
    gppp=tpp-2*gpp/r+4*gp/r**2-4*g/r**3
    mask=u<.1
    if np.any(mask):
        v=u[mask];series=[np.zeros_like(v) for _ in range(4)]
        for k in range(8):
            power=2*k+1;coef=(-1.)**k/(2**k*math.factorial(k)*(2*k+3))
            for deriv in range(4):
                if power>=deriv:
                    mul=math.factorial(power)/math.factorial(power-deriv)
                    series[deriv]+=coef*mul*v**(power-deriv)
        for deriv,arr in enumerate((g,gp,gpp,gppp)):
            arr[mask]=CC*series[deriv]/sigma**(deriv+2)
    return g,gp,gpp,gppp,tt,tp,tpp


def r_derivatives(z):
    rm=law.Rminus1(z);zd=law.zRprime(z)
    rp=zd/z
    zp=law.Qsecond(z)*z
    y=np.sqrt(z)
    z2pp=z*z*(3*y+10)/(4*y**4.5*(y+4)**1.5)
    rpp=(zp-2*zd)/(z*z)
    rppp=(z2pp-3*zp+6*zd)/(z*z*z)
    return rm,rp,rpp,rppp


def coefficients(x,z,xr,zr,xrr,zrr,ell,newtonian):
    if newtonian:return (np.zeros_like(x),)*5
    rm,rp,rpp,rppp=r_derivatives(z)
    c=rm+x*rp
    cr=rp*xr+(rp+x*rpp)*zr
    d=ell*ell*x*rp
    dr=ell*ell*(xr*rp+x*rpp*zr)
    drr=ell*ell*(xrr*rp+2*xr*rpp*zr+x*rppp*zr*zr+x*rpp*zrr)
    return c,cr,d,dr,drr


def contacts(eta,ell,sigma,newtonian=False):
    if sigma==0 or newtonian:return 0.,0.
    k=CC/(3*sigma**3);x=eta*eta;z=np.array(x+3*ell*ell*k*k)
    _,rp,rpp,rppp=r_derivatives(z)
    cx=2*rp+x*rpp;dxx=ell*ell*(2*rpp+x*rppp)
    return float(8*k*x*cx/15),float(-8*k**3*x*dxx/3)


def quadrupole(eta,ell,sigma=0.,nr=8000,nm=160,rmin=1e-8,rmax=1e6,newtonian=False):
    uu=np.linspace(math.log(rmin),math.log(rmax),nr);r=np.exp(uu)
    mu,w=leggauss(nm);mu=mu[None,:];p=3*mu*mu-1
    qa=np.zeros(nr);qb=np.zeros(nr);qad=np.zeros(nr);qbd=np.zeros(nr)
    sa=np.zeros(nr);sb=np.zeros(nr)
    for first in range(0,nr,128):
        sl=slice(first,min(first+128,nr));rr=r[sl,None]
        g,gp,gpp,gppp,tt,tp,tpp=radial(rr,sigma)
        gt=g/rr;gtp=(gp-gt)/rr;gtpp=gpp/rr-2*gp/rr**2+2*g/rr**3
        hh=ell*ell*(gp*gp+2*gt*gt)
        hhp=ell*ell*(2*gp*gpp+4*gt*gtp)
        hhpp=ell*ell*(2*gpp*gpp+2*gp*gppp+4*gtp*gtp+4*gt*gtpp)
        x=g*g+eta*eta+2*g*eta*mu;xr=2*gp*(g+eta*mu)
        xrr=2*gp*gp+2*gpp*(g+eta*mu)
        vals=coefficients(x,x+hh,xr,xr+hhp,xrr,xrr+hhpp,ell,newtonian)
        x0=g*g+eta*eta;xr0=2*gp*g;xrr0=2*gp*gp+2*gpp*g
        refs=coefficients(x0,x0+hh,xr0,xr0+hhp,xrr0,xrr0+hhpp,ell,newtonian)
        c,cr,d,dr,drr=[a-b for a,b in zip(vals,refs)]
        av=(c*(g+eta*mu)*p)@w
        bv=(c*(eta*(3*mu-5*mu**3)+g*(1-3*mu*mu)))@w
        apr=((cr*(g+eta*mu)+c*gp)*p)@w
        dv=(d*p)@w;dpr=(dr*p)@w;dppr=(drr*p)@w
        rad=rr[:,0];gpv=gp[:,0];gtv=gt[:,0];tpv=tp[:,0]
        qa[sl]=1.5*bv/rad
        qb[sl]=6*(gpv-gtv)*dv/rad**2
        da=apr-av/rad-3*bv/rad
        db=gpv*dppr+(gpp[:,0]+tpv+2*gpv/rad)*dpr+(tpp[:,0]+2*tpv/rad-6*gtv/rad**2)*dv
        qad[sl]=-.5*da;qbd[sl]=.5*db
        sa[sl]=.5*av/rad
        sb[sl]=.5*(gpv*dpr/rad+tpv*dv/rad+3*gpv*dv/rad**2)
    aa=float(np.trapz(qa,uu));bb=float(np.trapz(qb,uu))
    ac,bc=contacts(eta,ell,sigma,newtonian)
    q=aa+bb-sa[-1]+sb[-1]+ac+bc
    qdensity=float(np.trapz(qad+qbd,uu))
    annulus=aa+bb-sa[-1]+sa[0]+sb[-1]-sb[0]
    return dict(q_signed=float(q),q_A_flux=aa,q_B_flux=bb,q_A_contact=ac,q_B_contact=bc,
        q_density=qdensity,flux_density_difference=float(q-qdensity),
        annulus_identity_difference=float(annulus-qdensity),
        outer_A_surface=float(sa[-1]),outer_B_surface=float(sb[-1]),
        finite_inner_A_surface=float(sa[0]),finite_inner_B_surface=float(sb[0]),
        ell_rM=ell,sigma_rM=sigma,nr=nr,nm=nm,rmin=rmin,rmax=rmax)


def physical(row,a0):
    rm=math.sqrt(old.GM/a0);pref=1.5*a0/rm
    return dict(row,Q2_signed_s_minus_2=row['q_signed']*pref,
        x_ceiling=abs(row['q_signed'])*pref/old.CEILING,
        cassini_pass=abs(row['q_signed'])*pref<=old.CEILING)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();start=time.monotonic()
    out=dict(law='full P=xQ(z)/z, z=x+ell²H:H; Q(0)=0, simple nu',footings={},checks={})
    for foot,a0 in old.A0.items():
        eta=old.GEXT/a0;rm=math.sqrt(old.GM/a0)
        rows=out['footings'][foot]=dict(a0=a0,eta=eta,physical_lengths={},controls={})
        point=quadrupole(eta,0.,nr=12000,nm=240)
        reference=old.quadrupole(eta,0.,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        rows['controls']['plain']=physical(point,a0)
        out['checks'][foot+'|plain_reproduction']=abs(point['q_signed']-reference['q_hessian_signed'])<1e-9
        smooth=quadrupole(eta,0.,sigma=.5,nr=12000,nm=240)
        smooth_ref=old.quadrupole(eta,.5,0.,nr=12000,nm=240,rmin=1e-8,rmax=1e6)
        corrected_ref=smooth_ref['q_flux_signed']+smooth_ref['analytic_inner_surface']
        rows['controls']['plain_gaussian_core']=physical(smooth,a0)
        out['checks'][foot+'|smooth_origin_contact']=abs(smooth['q_signed']-corrected_ref)<1e-9
        rows['controls']['newtonian']=quadrupole(eta,1000.,sigma=.1,nr=1000,nm=40,newtonian=True)
        out['checks'][foot+'|newtonian']=rows['controls']['newtonian']['q_signed']==0.
        for length in [.03,.1,.3,1.]:
            ell=length*KPC/rm
            base=physical(quadrupole(eta,ell),a0)
            fine=physical(quadrupole(eta,ell,nr=16000,nm=320,rmin=1e-10,rmax=1e7),a0)
            rows['physical_lengths'][str(length)]=dict(base=base,fine=fine)
            scale=max(abs(fine['q_signed']),1e-12)
            out['checks'][foot+f'|{length}|refinement']=abs(base['q_signed']-fine['q_signed'])/scale<2e-4
            out['checks'][foot+f'|{length}|density']=abs(fine['flux_density_difference'])/scale<2e-4
            print(foot,length,'q_A',fine['q_A_flux'],'q_B',fine['q_B_flux'],'q',fine['q_signed'],'ratio',fine['x_ceiling'],'densitydiff',fine['flux_density_difference'],flush=True)
        ell=.03*KPC/rm;reg=[];point=rows['physical_lengths']['0.03']['fine']['q_signed']
        for sigma in [.5,.1,.01,.001,5e-7]:
            rr=physical(quadrupole(eta,ell,sigma,nr=12000,nm=240,rmin=1e-10,rmax=1e7),a0)
            rr['point_relative_difference']=abs(rr['q_signed']/point-1)
            reg.append(rr)
        rows['controls']['shrinking_gaussian']=reg
        out['checks'][foot+'|point_regularization']=max(x['point_relative_difference'] for x in reg[-3:])<2e-4
        out['checks'][foot+'|regularized_density']=max(abs(x['flux_density_difference'])/max(abs(x['q_signed']),1e-12) for x in reg)<2e-4
    spherical=quadrupole(0.,1000.,sigma=.1,nr=1000,nm=40)
    out['controls_zero_external']=spherical
    out['checks']['zero_external']=spherical['q_signed']==0.
    out['all_checks_pass']=all(out['checks'].values())
    out['runtime_seconds']=time.monotonic()-start
    out['outcome']='finite constant-external-field quadrupole, full variation and Gaussian point limit; empirical quadrature errors'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('checks',out['checks'],'runtime',out['runtime_seconds'],flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
