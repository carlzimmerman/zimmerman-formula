import json,sys,runpy
from pathlib import Path
out=Path(sys.argv[1]);sys.argv=['calculate.py','--output',str(out.parent/'replica.json')]
g=runpy.run_path(str(Path(__file__).with_name('calculate.py')))
r=g['result'];rad=g['radiate'];records=[]
for x in r['rows']:
 if x['power']==0:continue
 m=x['mass_Msun']/g['M0'];R=x['R_kpc']/g['ell'];a=rad(m,R,x['omega'],128);b=rad(m,R,x['omega'],256)
 records.append(dict(z=x['z'],factor=x['factor'],M=x['mass_Msun'],weak=x['weak_valid'],err64=abs(x['power']/b['power']-1),err128=abs(a['power']/b['power']-1),cooling_Gyr=m*m/(2*g['np'].sqrt(g['np'].pi)*R)/b['power']*g['t0']))
weak=[x for x in records if x['weak']]
# Exact dust reference and continuity sensitivity, independent split implementations.
np=g['np'];solve=g['solve_ivp'];fb=g['fb'];fc=g['fc'];N0=g['N0'];ai=np.exp(N0)
def solve_growth(z,k,rtol):
 nf=-np.log(1+z)
 def rhs(S):
  def f(N,y):
   b,bp,c,cp=y;s=1/(1+(k*g['ellMpc']/np.exp(N))**2) if S else 1
   return [bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*s*c)]
  return f
 a=solve(rhs(True),(N0,nf),[ai]*4,rtol=rtol,atol=rtol*1e-3)
 b=solve(rhs(False),(nf,0),a.y[:,-1],rtol=rtol,atol=rtol*1e-3)
 return fb*b.y[0,-1]+fc*b.y[2,-1]
dust=solve_growth(20,0,1e-11)
gerr=max(abs(solve_growth(x['z'],x['k'],1e-11)-x['retained']) for x in r['growth'])
checks=[dict(name='all_radiating_128_vs_256_below_2pct',passed=max(x['err128'] for x in records)<.02,value=max(x['err128'] for x in records)),dict(name='weak_64_vs_256_below_2pct',passed=max(x['err64'] for x in weak)<.02,value=max(x['err64'] for x in weak)),dict(name='dust_reference',passed=abs(dust-1)<1e-8,value=dust),dict(name='growth_split_repeat',passed=gerr<1e-8,value=gerr)]
out.write_text(json.dumps(dict(checks=checks,records=records),indent=2)+'\n')
