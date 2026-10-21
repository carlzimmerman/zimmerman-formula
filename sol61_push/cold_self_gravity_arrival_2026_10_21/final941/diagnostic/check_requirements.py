"""Independent algebra/arithmetic diagnostics of final CFG941. No model imported."""
from pathlib import Path
import sympy as s,json,sys,resource,time
out=Path(sys.argv[1]);start=time.monotonic();here=Path(__file__).resolve().parent
raw=json.loads((here/'evidence/cfg941_results.json').read_text());checks=[]
def ck(name,x):checks.append({'check':name,'passed':bool(x)})
f=s.Rational(1341,1591);fb=1-f;I=1-f/6
old=s.Matrix([[fb,f],[fb,0]])
new=s.Matrix([[fb,f],[fb/I,f/(6*I)]])
def exponent(M):
 mu=max(M.eigenvals(),key=lambda v:float(v));return float((-s.Rational(1,2)+s.sqrt(s.Rational(1,4)+6*mu))/2)
n0,n1=exponent(old),exponent(new)
ck('old two-fluid saved S6 arithmetic',abs(n0-raw['D6']['n_S6'])<1e-12)
ck('boost-retained two-fluid saved arithmetic',abs(n1-raw['D6']['n_full'])<1e-12)
ck('boost inertia positive',I>0)
ck('boost correction does not restore dust exponent',n0<n1<1)
ck('clamped third-component row is not the primary number',abs(n1-raw['R2']['n_ft']['1.0'][1])>1e-8)
x,eps=s.symbols('x eps',positive=True)
# x=g_law(g_b)/a0; g_b/a0=x²/(1+x).
N=x*x/(1+x);Bp=(1+eps)**2*x*x/(1+(1+eps)*x)
free_bound=s.factor(Bp/N-1)
simple=eps*(1+(1+eps)/(1+(1+eps)*x))
ck('inverse law extra-source bound identity',s.simplify(free_bound-simple)==0)
ck('deep bound',s.simplify(s.limit(free_bound,x,0,dir='+')-eps*(2+eps))==0)
ck('Newtonian bound',s.simplify(s.limit(free_bound,x,s.oo)-eps)==0)
ck('zero tolerance permits no positive enclosed free source',s.simplify(free_bound.subs(eps,0))==0)
ck('strict lower positive-source bound',s.simplify((free_bound-eps)*(1+(1+eps)*x)-eps*(1+eps))==0)
ck('strict upper positive-source bound',s.simplify((eps*(2+eps)-free_bound)*(1+(1+eps)*x)-eps*(1+eps)**2*x)==0)
stock=s.Rational(5364,100);ft=float(raw['R2']['ft_max']);avail=float(stock)*ft
foot={}
for key in ['canonical','alt']:
 need=raw['R2']['a'][key]['phantom_over_Mb'];minimum_ft=need/float(stock)
 ratio=avail/need
 ck(key+' declared stock ratio reproduced',abs(ratio-raw['R2']['a'][key]['tethered_supply_over_need'])<1e-12)
 ck(key+' growth-compatible stock short under max-catchment assumption',ratio<1)
 foot[key]={'need_tethered_mass_per_Mb':need,'max_available_tethered_per_Mb':avail,'minimum_local_tethered_fraction_if_total_stock_bound_kept':minimum_ft,'cosmic_tethered_fraction_bound_used':ft,'required_local_enrichment_factor_at_least':minimum_ft/ft,'additional_tethered_mass_per_Mb_if_total_stock_kept':need-avail}
controls=[]
for value in [s.Rational(1,10**6),s.Rational(1,20),s.Rational(1,10)]:
 controls.append({'epsilon':float(value),'min_bound':float(value),'max_deep_bound':float(value*(2+value))})
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;rss=int(rss if sys.platform=='darwin' else rss*1024);ck('RSS below oneGB',rss<1000000000)
result={'scope':'Exact static R2 free-source necessary bound plus saved approximation arithmetic and conditional stock requirements. No halo profile/segregation/conversion mechanism constructed, no observational error tolerance inferred, no full covariant growth calculation.','growth':{'old':n0,'boost_retained':n1,'I':str(I),'M':str(new),'assumptions':'Prescribed EdS subhorizon NR Poisson-eliminated two-fluid approximation, lambda0, not complete covariant constraints'},'static_bound':{'x':'g_law(g_b)/a0>0','epsilon':'nonnegative allowed fractional acceleration change','inequality':'g_free/g_b <= epsilon*[1+(1+epsilon)/(1+(1+epsilon)*x)]','domain':'Cold spherical static tethered equilibrium, same S2 law with free component entering positive source, no changed force/operator, no stellar-pressure/EFE corrections','interpretation':'Frozenepsilon1e-6 is numerical law-preservation criterion, not empirical precision; 0.05/0.10 are illustrative only','illustrations':controls},'stock':{'total_cold_to_Mb_bound':float(stock),'requirements':foot,'assumptions':'Source max-catchment10 and its growth-compatible cosmic ft bound; no extra catchment, active conversion or imported tethered mass. Enrichment arithmetic does not exclude any unspecified process.'},'checks':checks,'passed':all(c['passed'] for c in checks),'maximum_measured_RSS_bytes':rss,'runtime_seconds':time.monotonic()-start}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks),'RSS_bytes':rss,'growth':result['growth'],'stock':foot}));sys.exit(0 if result['passed'] else 1)
