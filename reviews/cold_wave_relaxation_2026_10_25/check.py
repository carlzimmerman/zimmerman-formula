import argparse,importlib.util,json
from pathlib import Path
import numpy as np
s=importlib.util.spec_from_file_location('audit','reviews/cold_shell_covariance_2026_10_24/audit.py'); a=importlib.util.module_from_spec(s); s.loader.exec_module(a); a.SELECTIVE=True
Gpc=a.G*a.MSUN/(a.PC*1e6); GYR=1e9*365.25*86400; conversion=a.PC/1000/GYR

def relax(R,rho,sigma,eta):
    log=np.log(R*sigma/eta)
    assert log>0
    return sigma**6/(Gpc**2*rho**2*eta**3*log)*conversion

def main():
 p=argparse.ArgumentParser(); p.add_argument('--output',required=True); p.add_argument('--mutate',action='store_true'); args=p.parse_args(); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
 old=json.load(open('reviews/cold_shell_covariance_2026_10_24/run_selective/result.json'))
 rows=[]; excluded=[]; maxerr=0
 for footing,a0 in a.inv.FOOTINGS.items():
  for name in old['footings'][footing]:
   d=a.read(name); r=d['r']/a.PC; A=a0*d['r']**2/(a.G*a.MSUN); B=d['gas']+d['star']
   for model,H in d['models'].items():
    mc=H-a.lawmass(B,A)
    prev=next(x['Mc'] for x in old['footings'][footing][name]['models'] if x['model']==model)
    assert np.allclose(mc,prev,rtol=1e-12)
    density=np.diff(mc)/(4*np.pi/3*np.diff(r**3))
    for i,rho in enumerate(density):
     if rho<=0:
      excluded.append(dict(footing=footing,name=name,model=model,shell=i,rho=float(rho))); continue
     R=np.sqrt(r[i]*r[i+1]); total=np.sqrt((B[i]+mc[i])*(B[i+1]+mc[i+1])); vc=np.sqrt(Gpc*total/R)
     for factor in [.5,1/np.sqrt(2),1.]:
      sigma=factor*vc; eta=1500.; t=relax(R,rho,sigma,eta*(1000 if args.mutate else 1))
      rsi=R*a.PC; rhosi=rho*a.MSUN/a.PC**3; ssi=sigma*1000; etasi=eta*a.PC*1000
      tsi=ssi**6/(a.G**2*rhosi**2*etasi**3*np.log(rsi*ssi/etasi))/GYR
      err=abs(t/tsi-1); maxerr=max(maxerr,err); assert err<1e-12,'eta unit mutation / SI mismatch'
      assert np.isclose(relax(R,2*rho,sigma,eta)/t,.25)
      # Scaling R and eta together leaves the Coulomb logarithm fixed.
      assert np.isclose(relax(2*R,rho,sigma,2*eta)/t,.125)
      rows.append(dict(footing=footing,name=name,model=model,shell=i,r_pc=float(R),rho_Msun_pc3=float(rho),sigma_factor=float(factor),sigma_kms=float(sigma),eta_over_sigma_pc=float(eta/sigma),R_over_wave=float(R*sigma/eta),t_Gyr=float(t),t_over_14Gyr=float(t/14),t_divided_by_100_Gyr=float(t/100)))
 summary={}
 for footing in a.inv.FOOTINGS:
  summary[footing]={}
  for model in d['models']:
   rr=[x for x in rows if x['footing']==footing and x['model']==model]
   summary[footing][model]=dict(valid_shells=len(rr)//3,excluded_shells=sum(x['footing']==footing and x['model']==model for x in excluded),min_Gyr=min(x['t_Gyr'] for x in rr),max_Gyr=max(x['t_Gyr'] for x in rr),min_R_over_wave=min(x['R_over_wave'] for x in rr))
 result=dict(summary=summary,rows=rows,excluded=excluded,minimum=min(rows,key=lambda x:x['t_Gyr']),max_SI_relative_error=maxerr,checks=['source reproduction','independent SI units','density scaling','eta scaling with fixed logarithm'],scope='conditional order-of-magnitude secular relaxation estimate; not formation simulation')
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n'); a.b.write_csv(out/'timescales.csv',rows); a.b.write_csv(out/'excluded_shells.csv',excluded)
 print(json.dumps({'summary':summary,'minimum':result['minimum'],'max_SI_relative_error':maxerr},indent=2))
if __name__=='__main__': main()
