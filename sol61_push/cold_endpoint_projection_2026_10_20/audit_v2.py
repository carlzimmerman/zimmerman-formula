"""Independent fixed-endpoint stellar projection. No source code executed."""
from pathlib import Path
import json,math,sys,resource
from scipy.integrate import quad
B=Path(__file__).resolve().parent
d=json.loads((B/'inputs/cfg918_results.json').read_text())
q=json.loads((B/'inputs/guard_results.json').read_text())
G=d['constants']['G'];RC=d['constants']['RC_CORE'];checks=[]
def ck(label,condition):
 checks.append({'name':label,'pass':bool(condition)})
 assert condition,label

def aperture_moment(Menc,a,X,breaks):
 """4pi/(3L_ap) integral nu(r) g(r) r^3 W_ap(r) dr; x=r/a."""
 L=1. if math.isinf(X) else X*X/(1+X*X)
 def f(x):
  if math.isinf(X) or x<=X:w=1.
  else:w=-math.expm1(1.5*math.log1p(-(X/x)**2))
  return x*(1+x*x)**(-2.5)*Menc(a*x)*w
 cuts=sorted(set([0.]+[r/a for r in breaks if r>0]+([] if math.isinf(X) else [X])))
 vals=[quad(f,l,h,epsabs=1e-12,epsrel=2e-10,limit=150)[0] for l,h in zip(cuts,cuts[1:])]
 vals.append(quad(f,cuts[-1],math.inf,epsabs=1e-12,epsrel=2e-10,limit=150)[0])
 return G/a*sum(vals)/L

for X in [.1,.5,1.,2.,math.inf]:
 z=aperture_moment(lambda r:r**3/(1+r*r)**1.5,1.,X,[])/G
 an=math.pi/32*(1. if math.isinf(X) else (1-(1+X*X)**(-1.5))/(X*X/(1+X*X)))
 ck('analytic Newton-Plummer aperture '+str(X),abs(z/an-1)<1e-8)
ck('global point-mass response',abs(aperture_moment(lambda r:1.,1.,math.inf,[])/G-1/3)<1e-9)
rows=[]
for name in ['Draco','Sextans','Fornax','Leo I']:
 src=d['results']['canonical']['B0'][name];b=src['base'];a=b['a'];R=b['R'];Mx=b['Mx'];gR=R**3/(R*R+RC*RC)
 gr=src['geoms']['G1']
 if name in ['Draco','Sextans']:
  k=next(k for k in gr['rb']['RE']['opt'] if k.startswith('1.0|C|'))
  c=gr['rb']['RE']['opt'][k][-1]['cfg'];mA,mB,rA,rB=c['mA'],c['mB'],c['r1'],c['r2']
 else:
  rec=next(x for x in q['separate_PH1_partial_guard'] if x['name']==name)
  c=rec['full_static_snapshot_optimum'];mA,mB,rA,rB=c['mA_Msun'],c['mB_Msun'],c['rA_pc'],c['rB_pc']
 funcs={
 'stars':lambda r,b=b,a=a:b['Ms']*r**3/(r*r+a*a)**1.5,
 'tether':lambda r,b=b,R=R:b['s']*b['Ms']*min(r/R,1.),
 'core':lambda r,Mx=Mx,gR=gR,R=R:Mx*min(r,R)**3/(min(r,R)**2+RC*RC)/gR,
 'A':lambda r,mA=mA,rA=rA:mA if r>=rA else 0.,
 'B':lambda r,mB=mB,rB=rB:mB if r>=rB else 0.}
 ck(name+' unchanged finite-stock endpoint',abs((Mx+mA+mB)/b['Mrem']-1)<1e-12)
 out={'name':name,'observed_catalogue_sigma_kms':b['sig'],'source_stellar_scale_pc':a,'source_core_mass_Msun':Mx,'endpoint_wind_mass_Msun':mB,'endpoint_rA_pc':rA,'endpoint_rB_pc':rB,'apertures':{}}
 for label,X in [('Re',1.),('global',math.inf)]:
  parts={n:aperture_moment(f,a,X,[R,rA,rB]) for n,f in funcs.items()}
  total=sum(parts.values());direct=aperture_moment(lambda r:sum(f(r) for f in funcs.values()),a,X,[R,rA,rB])
  ck(name+' '+label+' linearity of projection',abs(total/direct-1)<1e-9)
  out['apertures'][label]={'sigma2_contributions_kms2':parts,'sigma_stars_kms':math.sqrt(total),'sigma_over_observed':math.sqrt(total)/b['sig']}
 # Independent global reconstruction using the mass-shell kernel.
 dm=lambda r:Mx/gR*r*r*(r*r+3*RC*RC)/(r*r+RC*RC)**2
 core=G/(3*a)*quad(lambda r:(1+(r/a)**2)**(-1.5)*dm(r),0,R,epsabs=1e-7,epsrel=1e-10)[0]
 exact={'stars':math.pi*G*b['Ms']/(32*a),'tether':G*b['s']*b['Ms']/(3*a*math.sqrt(1+(R/a)**2)),'core':core,'A':G*mA/(3*a)*(1+(rA/a)**2)**(-1.5),'B':G*mB/(3*a)*(1+(rB/a)**2)**(-1.5)}
 for k,v in exact.items():
  ck(name+' independent global shell component '+k,abs(out['apertures']['global']['sigma2_contributions_kms2'][k]-v)<1e-8*max(1.,abs(v)))
 if name in ['Fornax','Leo I']:
  ck(name+' prior guarded static snapshot reproduced',abs(out['apertures']['global']['sigma_stars_kms']/c['sigma_stars_static_snapshot']-1)<1e-8)
 rows.append(out)
r={'assertion_tested':'Independent fixed-endpoint Plummer stellar projection under source mass profiles; no mass re-fit','rows':rows,'checks':checks,'n_checks':len(checks),'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Static canonical B0/G1/C endpoints; isotropic Re plus anisotropy-independent global moment; spherical Plummer with source Newtonian mass profiles, observed selection unknown. Not confidence exclusion, source regrade, thermal rerun, or evolving transport.'}
assert r['peak_rss_bytes_macos']<1_000_000_000
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'rows':[{k:x[k] for k in ['name','observed_catalogue_sigma_kms','apertures']} for x in rows]},indent=2))
