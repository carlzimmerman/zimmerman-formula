"""Independent 60-digit reconstruction of sampled ADM residuals from root output.
Checks stored RHS conversion, not dense-solution derivatives or global integration error.
"""
import argparse,json
from pathlib import Path
import mpmath as m
ap=argparse.ArgumentParser();ap.add_argument('--input',required=True,type=Path);ap.add_argument('--output-dir',required=True,type=Path);a=ap.parse_args();b=Path(__file__).resolve().parent;o=a.output_dir.resolve();o.relative_to(b);o.mkdir(parents=True,exist_ok=True);m.mp.dps=60;data=json.loads(a.input.read_text());rows=[]
for row in data['runs']:
 mins={'F':m.inf,'Ugg':m.inf,'k':m.inf};worst={z:m.mpf(0) for z in ['EN','EB','EV','qjr_relative']}
 for z in row['samples']:
  r=m.mpf(str(z['r']));lnN,lnB,w,k=[m.mpf(str(v)) for v in z['y']];dn,db,dw,dk=[m.mpf(str(v)) for v in z['derivative']];N=m.exp(lnN);B=m.exp(lnB);V=-w*r*N;P=N*k/r;BP=B*db/r;VP=V/r*(1+dn+dw/w);PP=N/r**2*(dk+k*dn-k);g=P/(N*B);gp=PP/(N*B)-g*(P/N+BP/B);ga=abs(g);ss=m.sqrt(ga**2+m.mpf('.25'));wg=ss-m.mpf('.5');W=(ga*ss+m.asinh(2*ga)/4)/2-ga/2;Ug=2*(g-m.sign(g)*wg);Ugg=2*(1-ga/ss);U=g*g-2*W;S=3*lnN-3+U;bc=m.mpf(1);c=m.mpf('1.5');T=2*B*r*V*VP+2*r*BP*V*V+B*V*V
  EN=B-1/B+2*r*BP/B**2+T/N**2+B*r*r*(S+2*c-g*Ug)+bc*B*r*r*(VP+BP/B*V+2*V/r)/N-(2*r*Ug+r*r*Ugg*gp)
  EB=N-(N+2*r*P)/B**2+(V*V+2*r*V*VP)/N-2*r*V*V*P/N**2+N*r*r*(S-g*Ug)-bc*r*r*V*P/N
  EV=-B*r/N*(2*V*(BP/B+P/N)+bc*r*P)
  jt=[bc*P/B**2,-3*bc*V,-bc*V/N*(VP+(BP/B+2/r)*V),V/(B*r*r)*(2*r*Ug+r*r*Ugg*gp)];jr=sum(jt);scale=sum(abs(v) for v in jt)
  for key,val in [('EN',EN),('EB',EB),('EV',EV),('qjr_relative',jr/scale)]:worst[key]=max(worst[key],abs(val))
  mins['F']=min(mins['F'],N*N-B*B*V*V);mins['Ugg']=min(mins['Ugg'],Ugg);mins['k']=min(mins['k'],k)
 rows.append({'tol':row['tol'],'minima':{k:str(v) for k,v in mins.items()},'residual_maxima':{k:str(v) for k,v in worst.items()}})
passed=all(all(m.mpf(v)>0 for v in z['minima'].values()) and all(m.mpf(v)<m.mpf('1e-14') for v in z['residual_maxima'].values()) for z in rows)
res={'passed':passed,'sampled_controls':rows,'limitations':['Storedderivatives are RHS evaluations, not independently differentiated dense solutions','SampledF/Ugg signs not continuum positivity proof','No matchedBVP or temporalhealth']};(o/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res));raise SystemExit(0 if passed else 1)
