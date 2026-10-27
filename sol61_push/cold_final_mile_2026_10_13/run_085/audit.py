import csv,json,math,hashlib,subprocess,sys,datetime
from pathlib import Path
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');O=Path(__file__).parent
paths=['campaign_fresh_gravity/CFG842_satellite_capture_liouville/'+n for n in ['cfg842.py','FROZEN_CRITERIA.md','cfg842_results.json','cfg842_results_MUTATE.json']]+['campaign_fresh_gravity/'+n for n in ['CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json','CFG839_pericentre_tides/cfg839_results.json','CFG827_dwarf_age_sfh_ml/cfg827_results.json','CFG824_dwarf_age_fossil/cfg824_results.json']]+['real_research/data/dsph/lvd_dwarf_mw.csv']
def hashes():return {p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths}
before=hashes();j=lambda i:json.loads((R/paths[i]).read_text());source=j(2);mutation=j(3);ex={x['name']:x for x in j(4)['canonical|nu_e']['rows']};orbit=j(5)['rows'];ups=j(6)['rows'];raw=j(7)['rows'];cat={x['name']:x for x in csv.DictReader((R/paths[8]).open())}
G,MS,PC,KPC,A0=6.674e-11,1.989e30,3.0857e16,3.0857e19,9.3603e-11; checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
def eq(n,a,b):ck(n,math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12))
def gfield(m,r):
 gn=G*m*MS/r**2;return gn/(-math.expm1(-math.sqrt(gn/A0)))
def host(m,r):
 rm2=G*m*MS/A0;q=math.sqrt(1+4*r*r/rm2)
 return m/(2*math.pi*rm2*r*q),math.sqrt(r*gfield(m,r)/2)
B=(4*math.pi/3)*5**1.5/(2*math.pi)**1.5 # moment-density inequality coefficient for Maxwellian donor fmax
rows=[]
for n,o in orbit.items():
 c=cat[n];lum=10**(.4*(4.83-float(c['M_V'])));m=ups[n]['ups']*lum;r=4/3*float(c.get('rhalf_sph_physical') or c['rhalf_physical'])*PC
 extra=gfield(m/2,r)*math.expm1(math.log(10)*ex[n]['delta'])*r*r/G/MS;need=3*max(extra,0)/(4*math.pi*r**3);ss=raw[n]['so']*1000
 for mass in [6e10,8e10]:
  cells=[]
  for D in [o['rnow'],o['rp']]:
   rh,sh=host(mass,D*KPC);cells.append({'ratio':rh/need*(ss/sh)**3,'no_dilution':rh/need,'rho':rh*KPC**3,'sh':sh/1000})
  best=max(x['ratio'] for x in cells);s=source['rows'][n][f'{mass:.0e}'];mu=mutation['rows'][n][f'{mass:.0e}']
  eq(n+' need '+str(mass),need*KPC**3,s['rho_need']);eq(n+' ratio '+str(mass),best,s['ratio']);eq(n+' now '+str(mass),cells[0]['rho'],s['rho_now']);eq(n+' peri '+str(mass),cells[1]['rho'],s['rho_peri']);eq(n+' mutation '+str(mass),max(x['no_dilution'] for x in cells),mu['ratio'])
  rows.append({'name':n,'host_mass':mass,'source_ratio':best,'moment_bound_ratio_if_Maxwellian_donor_and_sigma_c_equals_stars':B*best,'sigma_c_over_sigma_stars_needed_for_unit_moment_bound':(1/(B*best))**(1/3),'delta':ex[n]['delta'],'rho_need':need*KPC**3})
# Numerical radial integral independent midpoint quadrature for K1.
N=20000;radius=100*KPC;m=6e10;dr=radius/N;integ=sum(4*math.pi*((i+.5)*dr)**2*host(m,(i+.5)*dr)[0]*dr for i in range(N));mc=.5*m*(math.sqrt(1+4*radius**2/(G*m*MS/A0))-1);ck('K1 midpoint profile integral',abs(integ/mc-1)<1e-7)
ck('12 source satellites',len(orbit)==12);ck('Sextans not covered','Sextans' not in orbit)
active=[x for x in rows if x['name']!='Sagittarius'];ck('all 11 non-Sagittarius have positive excess',all(x['delta']>0 for x in active));ck('all moment bounds below 1e-4',max(x['moment_bound_ratio_if_Maxwellian_donor_and_sigma_c_equals_stars'] for x in active)<1e-4)
eq('Sagittarius frozen maximum',max(x['source_ratio'] for x in rows),source['max_ratio']);ck('frozen class preserved',source['cls']=='MARGINAL');ck('Sagittarius not exactly zero',ex['Sagittarius']['delta']>0 and ex['Sagittarius']['delta']<.001)
# Extremizer check: f=fmax in velocity ball radius sqrt(5)*sigma gives E[v^2]=3 sigma^2 and saturates coefficient.
v=math.sqrt(5);rho=4*math.pi*v**3/3;second=4*math.pi*v**5/5;eq('waterbag 3D second moment',second/rho,3);eq('coefficient saturation',rho/(2*math.pi)**1.5,B)
epsilon=.01; narrow=.001; warm=math.sqrt((1-epsilon*narrow**2)/(1-epsilon)); peak=epsilon/narrow**3+(1-epsilon)/warm**3
ck('mixture preserves density',epsilon+(1-epsilon)==1);eq('mixture preserves variance',epsilon*narrow**2+(1-epsilon)*warm**2,1);ck('same moments admit peak enhancement over 1e7',peak>1e7)
after=hashes();ck('inputs unchanged',after==before)
res={'claim_id':'CE-FM-085','status':'completed','n_checks':len(checks),'checks':checks,'moment_bound_factor':B,'same_moment_counterexample':{'cold_density_fraction':epsilon,'cold_sigma_over_host_sigma':narrow,'warm_sigma_over_host_sigma':warm,'peak_f_over_single_Maxwellian':peak},'rows':rows,'K1_ratio':integ/mc,'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'source_inputs_before':before,'source_inputs_after':after,'versions':{'python':sys.version},'assertion_tested':'Replay declared CFG842 arithmetic for 12 satellites at two positions and two masses, and conditional smooth-Maxwellian donor phase-space moment-bound sensitivity.','non_claims':['Not a general Liouville exclusion: rho/sigma^3 does not determine fine-grained fmax','Cold component velocity dispersion need not equal stellar tracer dispersion','No source distribution function, capture dynamics, dissipation or primordial fragment model derived','Sextans absent; no Sextans capture verdict','Frozen MARGINAL unchanged; profile density and orbit dispersion use different interpolation kernels']}
(O/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'checks':len(checks),'B':B,'active_max':max(x['source_ratio'] for x in active),'targets':[x for x in rows if x['name'] in ['Draco','Fornax','Leo I']]},indent=2))
