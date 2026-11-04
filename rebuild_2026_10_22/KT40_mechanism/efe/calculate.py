"""Exact scalar homology virial in a constant auxiliary Newtonian field."""
import argparse,json,math,sys,time
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
from numpy.polynomial.legendre import leggauss
import mpmath as mp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'rebuild_2026_10_22/KT39_power_curvature/dwarfs'))
import isolated as I
L=I.law
POWER=1.125
ELL=3.
ETAS=[0.,.1,.3,1.,3.]
NAMES=['Draco','Sculptor','Leo II','Fornax']


def grid_arrays(d,foot,eta,n,nmu,domain=1.,masses=None,r=None):
    a=d['a'];a0=I.A0[foot]
    masses=I.UPS*d['L']+1.33*d['MHI'] if masses is None else np.asarray(masses,float)
    r=np.geomspace(1e-6*a,domain*(200*a+40*ELL),n) if r is None else np.asarray(r,float)
    mu,w=leggauss(nmu);rr=r[:,None,None];mm=mu[None,:,None]
    gm=I.G*masses
    resultA=[];resultB=[]
    for start in range(0,len(gm),5):
        gmblock=gm[start:start+5][None,None,:]
        g,gp,gpp=I.plummer_fields(rr,gmblock,a);gt=g/rr
        e=eta*a0
        x=(g*g+e*e+2*g*e*mm)/a0**2
        s=ELL**2*(gp*gp+2*gt*gt)/a0**2;z=x+s**POWER
        rm=L.Rminus1(z);dd=L.zRprime(z);ratio=x/z
        C=rm+ratio*dd
        D=POWER*ELL**2*s**(POWER-1)*ratio*dd
        delta_g=2*g+rr*gp
        delta_rr=3*gp+rr*gpp
        delta_tt=2*gt+gp
        Ae=0. if eta==0 else float((L.Qprime(eta*eta)-1)*e)
        ar=C*(g+e*mm)-Ae*mm
        amean=np.sum(w[None,:,None]*ar*delta_g,axis=1)
        bmean=np.sum(w[None,:,None]*D*(gp*delta_rr+2*gt*delta_tt),axis=1)
        resultA.append(amean);resultB.append(bmean)
    return r,np.concatenate(resultA,axis=1),np.concatenate(resultB,axis=1),gm


def predict(d,foot,eta,n,nmu,domain):
    r,aa,bb,gm=grid_arrays(d,foot,eta,n,nmu,domain)
    va=simpson(r[:,None]**2*aa,x=r,axis=0)/(6*gm)
    vb=simpson(r[:,None]**2*bb,x=r,axis=0)/(6*gm)
    vn=np.pi*gm/(32*d['a']);variance=vn+va+vb
    assert np.all(np.isfinite(variance))
    valid=variance>0;sigma=np.sqrt(np.maximum(variance,0))
    passed=valid&(abs(sigma-d['obs'])<=2*d['err'])
    return dict(name=d['name'],footing=foot,eta=eta,power=POWER,ell_kpc=ELL,n=n,nmu=nmu,domain=domain,
        variance=variance.tolist(),variance_Newton=vn.tolist(),variance_A=va.tolist(),variance_B=vb.tolist(),
        sigma=[float(s) if ok else None for s,ok in zip(sigma,valid)],
        invalid_variance_indices=np.flatnonzero(~valid).tolist(),passed=bool(np.any(passed)),
        upsilon_passing=I.UPS[passed].tolist(),observed_sigma=d['obs'],observed_error=d['err'],
        sigma_U1=float(sigma[0]) if valid[0] else None,sigma_U2=float(sigma[20]) if valid[20] else None,
        sigma_U3=float(sigma[-1]) if valid[-1] else None)


def mp_energy(r,mu,gm,a,a0,e):
    """Independent closed-form primitive at high precision; phantom energy."""
    q=r*r+a*a;g=gm*r/q**mp.mpf('1.5');gp=gm*(a*a-2*r*r)/q**mp.mpf('2.5');gt=g/r
    g2=g*g+e*e+2*g*e*mu;x=g2/(a0*a0)
    s=ELL**2*(gp*gp+2*gt*gt)/(a0*a0);z=x+s**(mp.mpf(9)/8)
    y=mp.sqrt(z)
    Q=y*y/2+(y+2)*mp.sqrt(y*(y+4))/2-4*mp.asinh(mp.sqrt(y)/2)
    return g2*(Q/z-1)


def homology_control(d,foot,eta):
    """Fixed finite domain, same quadrature: direct MP energy difference vs A/B."""
    mp.mp.dps=40
    a=d['a'];a0=I.A0[foot];gm=I.G*(2*d['L']+1.33*d['MHI'])
    t,tw=leggauss(48);mu,mw=leggauss(24)
    lo,hi=math.log(.01*a),math.log(10*a)
    logs=(hi+lo)/2+(hi-lo)/2*t;r=np.exp(logs);weights=tw*(hi-lo)/2*r**3
    _,aa,bb,_=grid_arrays(d,foot,eta,len(r),len(mu),masses=[gm/I.G],r=r)
    analytic=float(weights@(aa[:,0]+bb[:,0]))/(6*gm)
    h=mp.mpf('0.0001');total=mp.mpf(0)
    for ri,wi in zip(r,weights):
        rr=mp.mpf(float(ri));ang=mp.mpf(0)
        for mui,wmi in zip(mu,mw):
            args=[rr,mp.mpf(float(mui)),mp.mpf(gm),None,mp.mpf(a0),mp.mpf(eta*a0)]
            args[3]=mp.mpf(a)*mp.exp(-h);plus=mp_energy(*args)
            args[3]=mp.mpf(a)*mp.exp(h);minus=mp_energy(*args)
            ang+=mp.mpf(float(wmi))*(plus-minus)/(2*h)
        total+=mp.mpf(float(wi))*ang
    fd=float(total)/(12*gm)
    error=abs(fd-analytic)/max(abs(analytic),1e-8)
    return dict(name=d['name'],footing=foot,eta=eta,finite_radius_a=[.01,10.],
                nlogr=48,nmu=24,mp_digits=40,h=float(h),analytic=analytic,energy_fd=fd,relative_error=error,passed=error<1e-5)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();start=time.monotonic()
    dwarfs=[d for d in I.sample() if d['name'] in NAMES];assert {d['name'] for d in dwarfs}==set(NAMES)
    previous=json.loads((ROOT/'rebuild_2026_10_22/KT39_power_curvature/dwarfs/continuation_001/results.json').read_text())
    out=dict(law='KT39 p9/8 ell3kpc with constant auxiliary Newtonian external gradient',
             qualification='Scalar trace virial/orientation-averaged dispersion; not an actual satellite LOS or equilibrium grade',
             sample=dwarfs,etas=ETAS,upsilon_grid=I.UPS.tolist(),cases={},controls=[],all_checks_pass=False)
    def save():args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    newton=L.tensor_terms(np.array([1.,2.,3.]),np.diag([1.,-2.,3.]),ELL,a0=2.,p=POWER,newtonian=True)
    assert np.array_equal(newton['A'],np.zeros(3)) and np.array_equal(newton['B'],np.zeros((3,3)))
    assert newton['energy']==14.
    newton_errors=[]
    for d in dwarfs:
        r=np.geomspace(1e-6*d['a'],2*(200*d['a']+40*ELL),2400)
        gm=I.G*(2*d['L']+1.33*d['MHI']);g=I.plummer_fields(r,gm,d['a'])[0]
        numeric=simpson((4*math.pi/3)*I.rho_unit(r,d['a'])*r**3*g,x=r)
        err=abs(numeric/(math.pi*gm/(32*d['a']))-1);assert err<1e-3;newton_errors.append(err)
    out['newton_control']=dict(exact_mutation=True,maximum_virial_relative_error=max(newton_errors))
    for name in ['Draco','Fornax']:
        dwarf=next(d for d in dwarfs if d['name']==name)
        for eta in [0.,.1,1.,3.]:
            c=homology_control(dwarf,'canonical',eta);out['controls'].append(c);save();print('control',c,flush=True)
            assert c['passed']
    for n,nmu,domain,label in [(800,32,1.,'coarse'),(1600,64,1.,'fine'),(2400,96,2.,'expanded')]:
        rows=[];out['cases'][label]=rows
        for foot in I.A0:
            for d in dwarfs:
                for eta in ETAS:
                    row=predict(d,foot,eta,n,nmu,domain);rows.append(row)
                    print(label,foot,d['name'],eta,'U3',row['sigma_U3'],'passed',row['passed'],flush=True)
            save()
    shifts=[];isolated_errors=[];summaries=[]
    for i,row in enumerate(out['cases']['fine']):
        other=[out['cases'][lab][i] for lab in ['coarse','expanded']]
        for old in other:
            assert old['invalid_variance_indices']==row['invalid_variance_indices']
            ds=max([abs(a-b) for a,b in zip(row['sigma'],old['sigma']) if a is not None and b is not None],default=0.)
            shifts.append(ds);assert ds<.02
        if row['eta']==0:
            old=next(r for r in previous['cases']['fine']['1.125|3'][row['footing']] if r['name']==row['name'])
            ds=max(abs(a-b) for a,b in zip(row['sigma'],old['sigma']));isolated_errors.append(ds);assert ds<.02
        summaries.append({k:row[k] for k in ['name','footing','eta','sigma_U1','sigma_U2','sigma_U3','passed','upsilon_passing','invalid_variance_indices']})
    out.update(summaries=summaries,maximum_sigma_refinement_change=max(shifts),
        maximum_isolated_reproduction_change=max(isolated_errors),all_checks_pass=True,runtime_seconds=time.monotonic()-start)
    save();print('completed',out['runtime_seconds'],'max shift',max(shifts),'isolated',max(isolated_errors),flush=True)

if __name__=='__main__':main()
