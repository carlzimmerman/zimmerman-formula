"""Full-action KT39 power curvature Plummer virial discriminator, import-safe."""
import argparse,csv,json,math,sys,time,itertools
from pathlib import Path
import numpy as np
from scipy.integrate import simpson

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'analytic'))
import law
from radial_reference import plummer_fields,radial_force

DATA=ROOT/'real_research/data/dsph/mcconnachie2012_dsph.csv'
KPC=3.0856775814913673e19
G=6.67430e-11*1.98847e30/(KPC*1e6)
A0={'canonical':9.3603e-11*KPC/1e6,'alt':1.1312e-10*KPC/1e6}
UPS=np.linspace(1.,3.,41)
ELLS=[2.75,3.]
POWERS=[1.125,1.25]
MODEL_CHOICES=[(1.125,3.),(1.25,2.75)]
FOCUS=('Sculptor','Fornax','Leo I')


def sample():
    rows=[]
    with DATA.open() as handle:
        for d in csv.DictReader(handle):
            if not d['e_sigma*'] or float(d['VMag'])>-8 or d['Name'].startswith(('M32','NGC','Sagittarius')):continue
            rows.append(dict(name=d['Name'],sub=d['SubG'],D=float(d['D']),
                             L=10**(-.4*(float(d['VMag'])-4.83)),a=float(d['R2'])/1e3,
                             obs=float(d['sigma*']),err=float(d['e_sigma*']),
                             MHI=float(d['M.HI'])*1e6 if d['M.HI'] else 0.))
    assert len(rows)==24
    return rows


def rho_unit(r,a):return 3/(4*math.pi*a**3)*(1+(r/a)**2)**-2.5


def predict(d,foot,ell,n,domain=1.,energy_fd=False,p=1.5):
    a=d['a'];a0=A0[foot];masses=UPS*d['L']+1.33*d['MHI'];gm=G*masses
    r=np.geomspace(1e-6*a,domain*(200*a+40*ell),n);rr=r[:,None]
    g,gp,gpp=plummer_fields(rr,gm[None,:],a)
    response=radial_force(rr,g,gp,gpp,ell,a0,p=p)
    W=(4*math.pi/3*rho_unit(r,a)*r**3)[:,None]
    integ=lambda q:simpson(q,x=r,axis=0)
    variance_N=np.pi*gm/(32*a)
    variance_ph=integ(W*response['phantom'])
    weak=integ(W*response['A']+W*(1/rr-5*rr/(a*a+rr*rr))*response['Br']
               +2*W/rr*response['Bt'])-(W[-1]*response['Br'][-1]-W[0]*response['Br'][0])
    energy=integ(rr**2*(response['A']*(2*g+rr*gp)+response['Br']*(3*gp+rr*gpp)
                       +2*response['Bt']*(2*g/rr+gp)))/(3*gm)
    errors=np.maximum(np.abs(variance_ph-weak),np.abs(variance_ph-energy))
    rel=errors/np.maximum(np.abs(variance_ph),1e-7)
    numeric_N=integ(W*g)
    plain_ph=integ(W*2*np.sqrt(a0*g)/(np.sqrt(g/a0+4)+np.sqrt(g/a0)))
    total=variance_N+variance_ph
    valid=total>0
    sigma=np.sqrt(np.maximum(total,0))
    passed=valid&(np.abs(sigma-d['obs'])<=2*d['err'])
    plain=np.sqrt(variance_N+plain_ph)
    checks=dict(maximum_virial_absolute_difference=float(errors.max()),
                maximum_virial_relative_difference=float(rel.max()),
                newton_relative_error=float(np.max(np.abs(numeric_N/variance_N-1))),
                all_finite=bool(np.all(np.isfinite(total))),
                minimum_radial_total_gradient=float(response['total'].min()))
    if energy_fd:
        h=1e-4;fs=[]
        for sign in [-1,1]:
            aa=a*math.exp(-sign*h)
            gg,gpg,gppg=plummer_fields(rr,gm[None,:],aa)
            ss=ell**2*(gpg*gpg+2*(gg/rr)**2)/a0**2
            z=gg*gg/a0**2+ss**p
            fs.append(gg*gg*law.Rminus1(z))
        fd=integ(rr**2*(fs[1]-fs[0])/(2*h))/(6*gm)
        checks['energy_fd_relative_difference']=float(np.max(np.abs(fd-variance_ph)/np.maximum(np.abs(variance_ph),1e-7)))
    return dict(name=d['name'],footing=foot,ell_kpc=ell,power=p,n=n,domain=domain,
                sigma=[float(s) if v else None for s,v in zip(sigma,valid)],
                sigma_U1=float(sigma[0]) if valid[0] else None,
                sigma_U2=float(sigma[20]) if valid[20] else None,
                sigma_U3=float(sigma[-1]) if valid[-1] else None,
                variance=total.tolist(),invalid_variance_indices=np.flatnonzero(~valid).tolist(),
                passed=bool(passed.any()),upsilon_passing=UPS[passed].tolist(),
                plain_sigma=plain.tolist(),plain_passed=bool((np.abs(plain-d['obs'])<=2*d['err']).any()),
                newton_sigma=np.sqrt(variance_N).tolist(),newton_passed=bool((np.abs(np.sqrt(variance_N)-d['obs'])<=2*d['err']).any()),
                observed_sigma=d['obs'],observed_error=d['err'],observed_low=d['obs']-2*d['err'],checks=checks)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    start=time.monotonic();dwarfs=sample();cases={};checks={}
    old=json.loads((ROOT/'rebuild_2026_10_22/KT36_action_response_search/dwarfs/run_001/results.json').read_text())
    checks['original_sample_exact']=dict(passed=dwarfs==old['sample'])
    for n,domain,label in [(1000,1.,'coarse'),(2000,1.,'fine'),(2000,2.,'expanded')]:
        cases[label]={}
        for power,ell in MODEL_CHOICES:
            key=f'{power:g}|{ell:g}'
            cases[label][key]={}
            for foot in A0:
                rows=[predict(d,foot,ell,n,domain,energy_fd=(label=='fine' and d['name'] in FOCUS),p=power) for d in dwarfs]
                cases[label][key][foot]=rows
                print(label,power,ell,foot,'pass',sum(x['passed'] for x in rows),'plain',sum(x['plain_passed'] for x in rows),flush=True)
    maxshift=0.;maxerr=0.;maxfd=0.;maxnewton=0.
    summaries={}
    for power,ell in MODEL_CHOICES:
        key=f'{power:g}|{ell:g}'
        summaries[key]={}
        for foot in A0:
            rows=cases['fine'][key][foot]
            summaries[key][foot]=dict(n=24,pass_count=sum(x['passed'] for x in rows),
                plain_isolated_pass=sum(x['plain_passed'] for x in rows),newton_pass=sum(x['newton_passed'] for x in rows),
                names_passing=[x['name'] for x in rows if x['passed']])
            for i,row in enumerate(rows):
                for label in ['coarse','expanded']:
                    other=cases[label][key][foot][i]
                    vals=[abs(x-y) for x,y in zip(row['sigma'],other['sigma']) if x is not None and y is not None]
                    shift=max(vals,default=0.);maxshift=max(maxshift,shift)
                    check_key=f'{power}|{ell}|{foot}|{row["name"]}|{label}'
                    checks[check_key]=dict(passed=shift<.02 and row['invalid_variance_indices']==other['invalid_variance_indices'],sigma_change=shift)
                for label in ['coarse','fine','expanded']:
                    c=cases[label][key][foot][i]['checks']
                    maxerr=max(maxerr,c['maximum_virial_relative_difference']);maxnewton=max(maxnewton,c['newton_relative_error']);maxfd=max(maxfd,c.get('energy_fd_relative_difference',0))
                    ok=c['all_finite'] and (c['maximum_virial_relative_difference']<1e-3 or c['maximum_virial_absolute_difference']<1e-7) and c['newton_relative_error']<1e-3 and c.get('energy_fd_relative_difference',0)<1e-3
                    checks[f'{power}|{ell}|{foot}|{row["name"]}|{label}|virial']=dict(passed=ok,**c)
    checks['plain_isolated_counts']=dict(passed=all(x['plain_isolated_pass']==19 for fs in summaries.values() for x in fs.values()))
    out=dict(law='Phenomenological KT39 P=xQ(x+s^p)/(x+s^p), s=ell²H:H/a0², Qprime=simple nu(sqrtz), full Hessian variation',case='isolated spherical',
             constants=dict(G=G,KPC=KPC,A0=A0),ells_kpc=ELLS,powers=POWERS,model_choices=MODEL_CHOICES,sample=dwarfs,upsilon_grid=UPS.tolist(),cases=cases,summaries=summaries,
             checks=checks,all_checks_pass=all(x['passed'] for x in checks.values()),maximum_sigma_refinement_change=maxshift,
             maximum_relative_virial_disagreement=maxerr,maximum_relative_energy_fd_disagreement=maxfd,maximum_newton_integral_error=maxnewton,
             runtime_seconds=time.monotonic()-start,
             qualification='Finite41-Upsilon isolated spherical counts only; no continuous-Upsilon or external-field upper-bound claim')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(summaries=summaries,all_checks_pass=out['all_checks_pass'],max_sigma_shift=maxshift,max_virial_relative=maxerr,max_energy_fd_relative=maxfd,runtime_seconds=out['runtime_seconds']),indent=2),flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
