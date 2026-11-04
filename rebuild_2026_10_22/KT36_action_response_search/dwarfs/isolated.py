#!/usr/bin/env python3
"""Spherical isolated reciprocal-Gaussian dwarf virial test; import safe."""
import argparse
import csv
import json
import math
from pathlib import Path
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import cumulative_trapezoid
from scipy.special import gammainc

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT/'real_research/data/dsph/mcconnachie2012_dsph.csv'
KPC = 3.0856775814913673e19
G = 6.67430e-11*1.98847e30/(KPC*1e6)
A0 = {'canonical':9.3603e-11*KPC/1e6,'alt':1.1312e-10*KPC/1e6}
UPS = np.linspace(1.,3.,41)
ELL = 3.
FOCUS = ('Sculptor','Fornax','Leo I')


def sample():
    rows=[]
    with DATA.open() as handle:
        for d in csv.DictReader(handle):
            if not d['e_sigma*'] or float(d['VMag'])>-8 or d['Name'].startswith(('M32','NGC','Sagittarius')):
                continue
            rows.append(dict(name=d['Name'],sub=d['SubG'],D=float(d['D']),
                L=10**(-.4*(float(d['VMag'])-4.83)),a=float(d['R2'])/1e3,
                obs=float(d['sigma*']),err=float(d['e_sigma*']),
                MHI=float(d['M.HI'])*1e6 if d['M.HI'] else 0.))
    assert len(rows)==24
    return rows


def weights(r):
    w=np.empty_like(r); w[0]=(r[1]-r[0])/2;w[-1]=(r[-1]-r[-2])/2
    w[1:-1]=(r[2:]-r[:-2])/2
    return w


def plummer(r,a):
    return 3/(4*math.pi*a**3)*(1+(r/a)**2)**-2.5


def radial_grid(a,n,domain=1.):
    return np.geomspace(1e-5*min(a,ELL),domain*(80*a+16*ELL),n)


def response(g,a0):
    # A=g(nu-1)=2sqrt(a0*g)/(sqrt(g/a0+4)+sqrt(g/a0)).
    return 2*np.sqrt(a0*g)/(np.sqrt(g/a0+4)+np.sqrt(g/a0))


def kernels(r,s,ell):
    z=r[:,None]*s[None,:]/ell**2
    envelope=np.exp(-.5*((r[:,None]-s[None,:])/ell)**2)
    fac=math.sqrt(2/math.pi)*s[None,:]**2/ell**3*envelope
    p0=-np.expm1(-2*z)/(2*z)
    p1=np.empty_like(z);small=z<.1; x=z[small]
    p1[small]=np.exp(-x)*(x/3+x**3/30+x**5/840+x**7/45360+x**9/3991680)
    x=z[~small]
    p1[~small]=((x-1)+(x+1)*np.exp(-2*x))/(2*x*x)
    assert np.min(p0)>=0 and np.min(p1)>=0
    return fac*p0,fac*p1


def geometry(a,n,domain=1.,checks=False):
    r=radial_grid(a,n,domain);w=weights(r);rho=plummer(r,a)
    vir=4*math.pi/3*rho*r**3*w
    sm=np.zeros_like(r);dual=np.zeros_like(r)
    rg=np.exp(-r*r/(2*.4**2));vg=r*np.exp(-r*r/(2*.7**2))
    smg=np.zeros_like(r);smv=np.zeros_like(r)
    for start in range(0,n,128):
        sl=slice(start,min(start+128,n));k0,k1=kernels(r[sl],r,ELL)
        sm[sl]=k0@(rho*w)
        dual+=(vir[sl]@k1)*w
        if checks:
            smg[sl]=k0@(rg*w);smv[sl]=k1@(vg*w)
    mass=cumulative_trapezoid(4*math.pi*r*r*sm,r,initial=0)+4*math.pi*sm[0]*r[0]**3/3
    source_g=G*mass/r**2
    source_mass=float(mass[-1]);input_mass=float((4*math.pi*r*r*rho)@w)
    ctl=dict(source_mass=source_mass,input_mass=input_mass,
             relative_source_mass_error=abs(source_mass/input_mass-1),
             analytic_input_tail_mass=float(-np.expm1(-1.5*np.log1p((a/r[-1])**2))))
    if checks:
        sg=math.hypot(.4,ELL);sv=math.hypot(.7,ELL)
        eg=(.4/sg)**3*np.exp(-r*r/(2*sg*sg))
        ev=(.7/sv)**5*r*np.exp(-r*r/(2*sv*sv))
        ctl['gaussian_relative_peak_error']=float(np.max(np.abs(smg-eg))/np.max(eg))
        ctl['vector_gaussian_relative_peak_error']=float(np.max(np.abs(smv-ev))/np.max(ev))
    # Orthogonal Newtonian radial integral compared with the exact term.
    gn=G*r/(r*r+a*a)**1.5
    ctl['newton_plummer_relative_error']=float(abs((vir@gn)/(math.pi*G/(32*a))-1))
    return r,w,source_g,dual,ctl


def mixture_geometry(a,r,w,order):
    nodes,ww=leggauss(order);u=(nodes+1)/2;ww=ww/2
    t=(u/(1-u))**2
    mixing=ww*np.exp(-t)*2*u/(1-u)**3
    variance0=a*a/(2*t);variance=variance0+ELL**2
    mass=(gammainc(1.5,r[:,None]**2/(2*variance)))@mixing
    rho=((2*math.pi*variance)**-1.5)[None,:]*np.exp(-r[:,None]**2/(2*variance))
    adjoint=(rho*(variance0/variance)[None,:])@mixing
    dual=4*math.pi/3*r**3*adjoint*w
    return G*mass/r**2,dual,dict(mixture_probability_error=float(abs(mixing.sum()-1)),order=order)


def predict(d,r,w,source_g,dual,foot):
    a0=A0[foot];masses=UPS*d['L']+1.33*d['MHI']
    base=math.pi*G*masses/(32*d['a'])
    pp=dual@response(source_g[:,None]*masses[None,:],a0)
    vals=np.sqrt(base+pp)
    tail=np.sqrt(G*masses*a0)*(-np.expm1(-1.5*np.log1p((d['a']/r[-1])**2)))/3
    plain_g=G*r[:,None]*masses[None,:]/(r[:,None]**2+d['a']**2)**1.5
    vir=4*math.pi/3*plummer(r,d['a'])*r**3*w
    plain=np.sqrt(base+vir@response(plain_g,a0))
    passed=np.abs(vals-d['obs'])<=2*d['err']
    return dict(name=d['name'],footing=foot,sigma=vals.tolist(),
        sigma_U1=float(vals[0]),sigma_U2=float(vals[20]),sigma_U3=float(vals[-1]),
        passed=bool(passed.any()),upsilon_passing=UPS[passed].tolist(),
        plain_sigma=plain.tolist(),plain_passed=bool((np.abs(plain-d['obs'])<=2*d['err']).any()),
        newton_sigma=np.sqrt(base).tolist(),newton_passed=bool((np.abs(np.sqrt(base)-d['obs'])<=2*d['err']).any()),
        outer_virial_sigma_squared_tail_upper=tail.tolist(),
        observed_sigma=d['obs'],observed_error=d['err'],observed_low=d['obs']-2*d['err'])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();start=time.monotonic();rows=sample()
    out=dict(law='universal ell=3kpc reciprocal Gaussian, simple nu',case='isolated spherical',
        constants=dict(G=G,KPC=KPC,A0=A0,ell=ELL),sample=rows,upsilon_grid=UPS.tolist(),
        cases={},checks={})
    for n in [1000,2000]:
        out['cases'][str(n)]={f:[] for f in A0}
        for i,d in enumerate(rows):
            r,w,g,b,c=geometry(d['a'],n,checks=(i==0))
            out['checks'][f'{n}|{d["name"]}']=c
            for foot in A0:
                pred=predict(d,r,w,g,b,foot);out['cases'][str(n)][foot].append(pred)
                if d['name'] in FOCUS:print(n,foot,d['name'],pred['sigma_U1'],pred['sigma_U2'],pred['sigma_U3'],pred['passed'],flush=True)
    out['selected_checks']={}
    for d in rows:
        if d['name'] not in FOCUS:continue
        r,w,g,b,c=geometry(d['a'],2000,domain=2.)
        entry=dict(domain=c,footings={})
        mix={order:mixture_geometry(d['a'],r,w,order) for order in [128,256]}
        entry['mixture_probability_checks']={str(o):m[2] for o,m in mix.items()}
        for foot in A0:
            base=next(x for x in out['cases']['2000'][foot] if x['name']==d['name'])
            low=next(x for x in out['cases']['1000'][foot] if x['name']==d['name'])
            dom=predict(d,r,w,g,b,foot)
            preds={str(o):predict(d,r,w,m[0],m[1],foot) for o,m in mix.items()}
            errors={label:float(np.max(np.abs(np.array(other['sigma'])-base['sigma']))) for label,other in [('radial_1000',low),('domain_2x',dom),*[(f'mixture_{o}',v) for o,v in preds.items()]]}
            entry['footings'][foot]=dict(expanded_domain=dom,mixture=preds,max_sigma_changes=errors)
        out['selected_checks'][d['name']]=entry
    out['summaries']={}
    for n,cases in out['cases'].items():
        out['summaries'][n]={f:dict(n=len(pp),reciprocal_pass=sum(p['passed'] for p in pp),
            plain_isolated_pass=sum(p['plain_passed'] for p in pp),newton_pass=sum(p['newton_passed'] for p in pp)) for f,pp in cases.items()}
    errors=[e for entry in out['selected_checks'].values() for f in entry['footings'].values() for e in f['max_sigma_changes'].values()]
    numeric_ok=all(c['relative_source_mass_error']<1e-3 and c['newton_plummer_relative_error']<1e-3 and c.get('gaussian_relative_peak_error',0)<1e-3 and c.get('vector_gaussian_relative_peak_error',0)<1e-3 for c in out['checks'].values())
    out['all_checks_pass']=bool(numeric_ok and max(errors)<.02)
    out['max_selected_sigma_change']=max(errors)
    out['runtime_seconds']=time.monotonic()-start
    out['outcome']='isolated spherical diagnostic, conditional on empirical numerical errors; not a satellite EFE grade'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(summaries=out['summaries'],checks=out['all_checks_pass'],max_selected_sigma_change=max(errors),runtime_seconds=out['runtime_seconds']),indent=2),flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
