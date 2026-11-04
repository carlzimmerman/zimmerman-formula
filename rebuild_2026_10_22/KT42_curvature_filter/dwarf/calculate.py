"""Curvature-only Gaussian KT39 response: fixed-filter Plummer virial."""
import argparse,csv,importlib.util,json,math,sys,time
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
from scipy.special import gammainc
from numpy.polynomial.legendre import leggauss
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
_spec=importlib.util.spec_from_file_location('kt42_primitive',ROOT/'rebuild_2026_10_22/KT37_generalized_action/analytic/law.py')
L=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(L)
KPC=3.0856775814913673e19
G=6.67430e-11*1.98847e30/(KPC*1e6)
A0={'canonical':9.3603e-11*KPC/1e6,'alt':1.1312e-10*KPC/1e6}
POWER=1.125;ELL=3.;ETA=.01
WIDTHS=[0.,.0001,.001,.003,.01,.03,.1,.3,1.]
CASES={'Draco':2.,'Fornax':3.}


def sample():
    rows=[]
    with (ROOT/'real_research/data/dsph/mcconnachie2012_dsph.csv').open() as f:
        for d in csv.DictReader(f):
            if d['Name'] in CASES:
                rows.append(dict(name=d['Name'],L=10**(-.4*(float(d['VMag'])-4.83)),b=float(d['R2'])/1e3,
                    obs=float(d['sigma*']),err=float(d['e_sigma*']),MHI=float(d['M.HI'])*1e6 if d['M.HI'] else 0.))
    assert set(d['name'] for d in rows)==set(CASES)
    return rows


def plummer(r,gm,b):
    q=r*r+b*b
    g=gm*r/q**1.5;hp=gm*(b*b-2*r*r)/q**2.5;ht=g/r
    dg=3*gm*b*b*r/q**2.5
    dht=3*gm*b*b/q**2.5;dhp=dht*(1-5*r*r/q)
    return g,hp,ht,dg,dhp,dht


def filtered_hessian(r,gm,b,width,nt,force_mixture=False):
    if width==0 and not force_mixture:
        _,hp,ht,_,dhp,dht=plummer(r,gm,b)
        return hp,ht,dhp,dht
    u=np.linspace(-32.,8.,nt);t=np.exp(u);weight=np.exp(-t)*t
    chi=b*b/(2*t);v=width*width+chi
    hp=np.empty_like(r);ht=np.empty_like(r);dhp=np.empty_like(r);dht=np.empty_like(r)
    for start in range(0,len(r),256):
        rr=r[start:start+256,None];v2=v[None,:];chi2=chi[None,:]
        exponent=np.exp(-rr*rr/(2*v2))
        F=gammainc(1.5,rr*rr/(2*v2))
        tt=F/rr**3
        pp=math.sqrt(2/math.pi)*v2**-1.5*exponent-2*tt
        dtt=math.sqrt(2/math.pi)*chi2*v2**-2.5*exponent
        dpp=dtt*(1-rr*rr/v2)
        for out,arr in [(hp,pp),(ht,tt),(dhp,dpp),(dht,dtt)]:
            out[start:start+len(rr)]=gm*simpson(arr*weight[None,:],x=u,axis=1)
    return hp,ht,dhp,dht


def integrands(d,foot,width,r,nmu,nt,source_b=None,mutate_adjoint=False):
    b=d['b'] if source_b is None else source_b
    gm=G*(CASES[d['name']]*d['L']+1.33*d['MHI'])
    a0=A0[foot];e=ETA*a0
    g,hp,ht,dg,dhp,dht=plummer(r,gm,b)
    bp,bt,dbp,dbt=filtered_hessian(r,gm,b,width,nt)
    mu,mw=leggauss(nmu)
    g2=g[:,None]**2+e*e+2*g[:,None]*e*mu[None,:]
    x=g2/a0**2;s=ELL**2*(bp*bp+2*bt*bt)/a0**2
    z=x+s[:,None]**POWER
    rm=L.Rminus1(z);dd=L.zRprime(z);f=x/z
    C=rm+f*dd;D=POWER*ELL**2*s[:,None]**(POWER-1)*f*dd
    Aext=float((L.Qprime(ETA**2)-1)*e)
    aa=np.sum(mw[None,:]*(C*(g[:,None]+e*mu[None,:])-Aext*mu[None,:])*dg[:,None],axis=1)
    if mutate_adjoint:dbp,dbt=dhp,dht
    bb=np.sum(mw[None,:]*D,axis=1)*(bp*dbp+2*bt*dbt)
    energy=np.sum(mw[None,:]*g2*rm,axis=1)
    return aa,bb,energy,gm


def predict(d,foot,width,n,nmu,nt,domain):
    r=np.geomspace(1e-6*d['b'],domain*(200*d['b']+40*ELL),n)
    aa,bb,_,gm=integrands(d,foot,width,r,nmu,nt)
    va=float(simpson(r*r*aa,x=r)/(6*gm));vb=float(simpson(r*r*bb,x=r)/(6*gm));vn=math.pi*gm/(32*d['b'])
    total=vn+va+vb
    assert np.isfinite(total)
    sigma=math.sqrt(total) if total>0 else None
    return dict(name=d['name'],upsilon=CASES[d['name']],footing=foot,eta=ETA,width_kpc=width,
        n=n,nmu=nmu,nt=nt,domain=domain,variance_Newton=vn,variance_A=va,variance_B=vb,variance=total,
        scalar_sigma=sigma,orientation_averaged_2sigma_screen=(sigma is not None and abs(sigma-d['obs'])<=2*d['err']),
        observed_sigma=d['obs'],observed_error=d['err'])


def mixture_control(d):
    gm=G*(CASES[d['name']]*d['L']+1.33*d['MHI']);b=d['b']
    r=np.geomspace(1e-6*b,1000*b,1001)
    _,hp,ht,_,dhp,dht=plummer(r,gm,b)
    out=[]
    for nt in [401,801,1201]:
        bp,bt,dbp,dbt=filtered_hessian(r,gm,b,0,nt,True)
        herr=float(np.max(np.maximum(abs(bp-hp),abs(bt-ht))/(abs(hp)+2*abs(ht))))
        derr=float(np.max(np.maximum(abs(dbp-dhp),abs(dbt-dht))/(abs(dhp)+2*abs(dht))))
        out.append(dict(nt=nt,hessian_scaled_error=herr,homology_scaled_error=derr,passed=max(herr,derr)<1e-7))
    return dict(name=d['name'],rows=out,passed=all(c['passed'] for c in out))


def energy_control(d,foot,width):
    r=np.geomspace(.01*d['b'],10*d['b'],301)
    aa,bb,_,gm=integrands(d,foot,width,r,48,801)
    analytic=float(simpson(r*r*(aa+bb),x=r)/(6*gm))
    rows=[]
    for h in [1e-4,5e-5]:
        ep=integrands(d,foot,width,r,48,801,source_b=d['b']*math.exp(-h))[2]
        em=integrands(d,foot,width,r,48,801,source_b=d['b']*math.exp(h))[2]
        fd=float(simpson(r*r*(ep-em)/(2*h),x=r)/(12*gm))
        error=abs(fd-analytic);relative=error/max(abs(analytic),1e-7)
        rows.append(dict(h=h,energy_fd=fd,absolute_error=error,relative_error=relative,passed=relative<5e-5 or error<1e-5))
    _,mut,_,_=integrands(d,foot,width,r,48,801,mutate_adjoint=True)
    mutated=float(simpson(r*r*(aa+mut),x=r)/(6*gm))
    return dict(name=d['name'],footing=foot,width_kpc=width,analytic=analytic,rows=rows,
        mutated_omitted_adjoint=mutated,mutation_difference=abs(mutated-analytic),passed=all(c['passed'] for c in rows))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();start=time.monotonic()
    dwarfs=sample();out=dict(law='Curvature-only Gaussian KT39 E=g²R(x+s^p), unfiltered g, full T_a adjoint',
        p=POWER,ell_kpc=ELL,constants=dict(G=G,KPC=KPC,A0=A0),widths_kpc=WIDTHS,sample=dwarfs,cases={},controls={},all_checks_pass=False)
    def save():args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    def check(ok):
        if not ok:
            save();raise AssertionError('See saved failed numerical control')
    out['controls']['mixture']=[mixture_control(d) for d in dwarfs]
    save();check(all(c['passed'] for c in out['controls']['mixture']))
    out['controls']['energy']=[]
    for d in dwarfs:
        for foot in A0:
            for width in [0.,.03,.3,1.]:
                c=energy_control(d,foot,width);out['controls']['energy'].append(c);save();check(c['passed'])
                if width==.3:check(c['mutation_difference']>1e-3)
                print('energy',d['name'],foot,width,c['analytic'],c['rows'][-1]['relative_error'],flush=True)
    for n,nmu,nt,domain,label in [(801,32,401,1.,'coarse'),(1601,64,801,1.,'fine'),(2401,96,1201,2.,'expanded')]:
        rows=[];out['cases'][label]=rows
        for d in dwarfs:
            for foot in A0:
                for width in WIDTHS:
                    row=predict(d,foot,width,n,nmu,nt,domain);rows.append(row);save()
                    print(label,d['name'],foot,width,row['variance'],row['variance_A'],row['variance_B'],flush=True)
    shifts=[]
    for i,row in enumerate(out['cases']['fine']):
        for label in ['coarse','expanded']:
            old=out['cases'][label][i]
            shift=abs(row['variance']-old['variance']);shifts.append(shift)
            check(shift<.02 and (row['variance']>0)==(old['variance']>0))
    out['controls']['maximum_absolute_variance_refinement_change']=max(shifts)
    previous=json.loads((ROOT/'rebuild_2026_10_22/KT40_mechanism/efe/low_001/results.json').read_text())
    baseline=[]
    for row in out['cases']['expanded']:
        if row['width_kpc']!=0:continue
        old=next(x for x in previous['cases']['expanded'] if x['name']==row['name'] and x['footing']==row['footing'] and x['eta']==ETA)
        idx=20 if row['upsilon']==2 else 40
        error=abs(row['variance']-old['variance'][idx]);baseline.append(dict(name=row['name'],footing=row['footing'],old=old['variance'][idx],new=row['variance'],absolute_error=error));check(error<.001)
    out['controls']['zero_filter_baseline']=baseline
    out['summaries']=out['cases']['expanded']
    out['all_checks_pass']=True;out['runtime_seconds']=time.monotonic()-start;save()
    print('complete',out['runtime_seconds'],'max variance shift',max(shifts),flush=True)

if __name__=='__main__':main()
