"""Two explicitly authorized post-MW Solar checks; original portfolio untouched."""
import argparse,json,math,time
from pathlib import Path
import numpy as np
import calculate as C

CHOICES=[(1.125,3.),(1.25,2.75)]


def hessian_zero_checks():
    out={};g=np.array([.3,.4,.7]);hh=np.zeros((3,3));length=3.
    h=float(np.linalg.norm(g));expected=(.5+math.sqrt(.25+1/h)-1)*g
    for p in [1.125,1.25,1.5,1.75]:
        value=C.law.tensor_terms(g,hh,length,p=p)
        zero=C.law.tensor_terms(np.zeros(3),hh,length,p=p)
        err=float(np.max(np.abs(value['A']-expected)))
        passed=err<1e-12 and bool(np.all(value['B']==0)) and bool(np.all(zero['A']==0)) and bool(np.all(zero['B']==0)) and float(zero['energy'])==0.
        out[str(p)]=dict(A_absolute_error=err,B_exactly_zero=bool(np.all(value['B']==0)),joint_origin_continuous_value_zero=float(zero['energy'])==0.,passed=passed)
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    started=time.monotonic();original=C.HERE/'run_001/results.json'
    original_data=json.loads(original.read_text());assert original_data['all_checks_pass']
    out=dict(law=original_data['law'],selection='Adaptive: p=1.125 at3kpc andp=1.25 at2.75kpc, explicitly requested after initial MW portfolio',choices=CHOICES,
        inherited_zero_length_controls=str(original.relative_to(C.RB.parent)),api={str(p):C.api_check(p) for p,_ in CHOICES},hessian_zero=hessian_zero_checks(),footings={},checks={})
    out['checks']['API']=all(x['passed'] for x in out['api'].values())
    out['checks']['zero_H_API']=all(x['passed'] for x in out['hessian_zero'].values())
    for foot,a0 in C.old.A0.items():
        eta=C.old.GEXT/a0;rm=math.sqrt(C.old.GM/a0);rows=out['footings'][foot]={}
        for p,length in CHOICES:
            ell=length*C.KPC/rm;key=f'p{p}|ell{length}'
            coarse=C.base.prior.physical(C.quadrupole(eta,ell,p),a0)
            fine=C.base.prior.physical(C.quadrupole(eta,ell,p,nr=16000,nm=320,rmin=1e-10,rmax=1e7),a0)
            record=rows[key]=dict(power=p,length_kpc=length,base=coarse,fine=fine)
            scale=max(abs(fine['q_signed']),1e-12)
            out['checks'][foot+'|'+key+'|refinement']=abs(coarse['q_signed']-fine['q_signed'])/scale<2e-4
            out['checks'][foot+'|'+key+'|density']=abs(fine['flux_density_difference'])/scale<2e-4
            print(foot,key,'ratio',fine['x_ceiling'],'qA',fine['q_A_flux'],'qB',fine['q_B_flux'],flush=True)
            if p==1.125:
                reg=[]
                for sigma in [.5,.1,.01,.001,5e-7]:
                    row=C.quadrupole(eta,ell,p,sigma,nr=12000,nm=240,rmin=max(1e-10,.001*sigma),rmax=1e7)
                    row['point_relative_difference']=abs(row['q_signed']/fine['q_signed']-1);reg.append(row)
                record['shrinking_gaussian']=reg
                out['checks'][foot+'|new_power_core']=max(x['point_relative_difference'] for x in reg[-3:])<2e-4
                out['checks'][foot+'|new_power_density']=max(abs(x['flux_density_difference'])/max(abs(x['q_signed']),1e-12) for x in reg)<2e-4
                family=[dict(reg[0],inner_fraction_of_sigma=.001)]
                for frac in [.0005,.00025]:
                    row=C.quadrupole(eta,ell,p,.5,nr=12000,nm=240,rmin=frac*.5,rmax=1e7)
                    row['inner_fraction_of_sigma']=frac;family.append(row)
                record['core_cutoff']=family
                out['checks'][foot+'|new_power_cutoff']=max(x['q_signed'] for x in family)-min(x['q_signed'] for x in family)<1e-10
                out['checks'][foot+'|new_power_absolute_density']=max(abs(x['flux_density_difference']) for x in family)<1e-10
                newton=C.quadrupole(eta,1000.,p,sigma=.1,nr=1000,nm=40,newtonian=True)
                record['newtonian']=newton;out['checks'][foot+'|new_power_newton']=newton['q_signed']==0.
    out['new_power_zero_external']=C.quadrupole(0.,1000.,1.125,sigma=.1,nr=1000,nm=40)
    out['checks']['new_power_zero_external']=out['new_power_zero_external']['q_signed']==0.
    out['all_checks_pass']=all(out['checks'].values());out['runtime_seconds']=time.monotonic()-started
    out['outcome']='Two adaptive finite choices, unchanged physical inputs and full variation; no parameter-family closure'
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('all checks',out['all_checks_pass'],'runtime',out['runtime_seconds'],flush=True)
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
