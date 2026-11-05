"""Independent density-weighted force monopole check of EFE homology virial."""
import argparse,json,math,time
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
from numpy.polynomial.legendre import leggauss
import calculate as C
I,L=C.I,C.L


def force_virial(d,foot,eta,n=1800,nmu=80,domain=2.):
    a=d['a'];a0=I.A0[foot];e=eta*a0;p=C.POWER;ell=C.ELL
    r=np.geomspace(1e-6*a,domain*(200*a+40*ell),n);mu,w=leggauss(nmu)
    rr=r[:,None,None];mm=mu[None,:,None];masses=I.UPS*d['L']+1.33*d['MHI'];gm=I.G*masses
    resultA=[];resultB=[];minforce=[]
    for start in range(0,len(gm),5):
        g,gp,gpp=I.plummer_fields(rr,gm[None,None,start:start+5],a);gt=g/rr
        x=(g*g+e*e+2*g*e*mm)/a0**2
        xp=2*(g+e*mm)*gp/a0**2
        s=ell**2*(gp*gp+2*gt*gt)/a0**2
        sp=2*ell**2*(gp*gpp+2*gt*(gp/rr-g/rr**2))/a0**2
        z=x+s**p;zp=xp+p*s**(p-1)*sp
        rp=L.Rprime(z);rpp=L.Rsecond(z)
        ar=(L.Rminus1(z)+x*rp)*(g+e*mm)
        D=p*ell**2*s**(p-1)*x*rp
        Dp=p*ell**2*((p-1)*s**(p-2)*sp*x*rp+s**(p-1)*(xp*rp+x*rpp*zp))
        forceB=-Dp*gp-D*(gpp+2*(gp-gt)/rr)
        amean=np.sum(w[None,:,None]*ar,axis=1)/2
        bmean=np.sum(w[None,:,None]*forceB,axis=1)/2
        weight=(4*math.pi/3*I.rho_unit(r,a)*r**3)[:,None]
        resultA.extend(simpson(weight*amean,x=r,axis=0).tolist())
        resultB.extend(simpson(weight*bmean,x=r,axis=0).tolist())
        minforce.extend(np.min(g[:,0,:]+amean+bmean,axis=0).tolist())
    va=np.asarray(resultA);vb=np.asarray(resultB);vn=np.pi*gm/(32*a)
    return dict(variance= (vn+va+vb).tolist(),variance_A=va.tolist(),variance_B=vb.tolist(),minimum_total_radial_monopole=minforce)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();start=time.monotonic()
    previous=json.loads((C.HERE/'run_001/results.json').read_text());rows=[];maxerr=0.
    for old in previous['cases']['fine']:
        d=next(d for d in previous['sample'] if d['name']==old['name'])
        new=force_virial(d,old['footing'],old['eta'])
        errors={k:float(np.max(np.abs(np.asarray(new[k])-old[k])/np.maximum(np.abs(old[k]),1.))) for k in ['variance','variance_A','variance_B']}
        maxerr=max(maxerr,*errors.values());assert max(errors.values())<1e-4
        assert np.array_equal(np.asarray(new['variance'])>0,np.asarray(old['variance'])>0)
        row=dict(name=old['name'],footing=old['footing'],eta=old['eta'],relative_differences=errors,**new);rows.append(row)
        print(old['footing'],old['name'],old['eta'],errors,flush=True)
    out=dict(assertion='Angular-monopole full radial force, density-weighted virial, independent chain derivative of D vs energy-homology calculation',
             quadrature=dict(nr=1800,nmu=80,domain=2.),rows=rows,maximum_relative_difference=maxerr,
             all_checks_pass=True,runtime_seconds=time.monotonic()-start)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':main()
