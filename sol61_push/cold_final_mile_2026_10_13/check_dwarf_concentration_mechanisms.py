"""CE-FM-078: stellar ordering, Kepler residence envelope, tidal stock budget."""
import json,math,sys,csv
from pathlib import Path
r=json.loads(Path('sol61_push/cold_final_mile_2026_10_13/run_077/results.json').read_text());rows=r['dwarfs'];by={x['name']:x for x in rows};checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
def cdf(x,q):
 if x>=1:return 1.
 if x<=q:return 0.
 e=(1-q)/(1+q);u=math.acos(max(-1.,min(1.,(1+q-2*x)/(1-q))))
 return (u-e*math.sin(u))/math.pi
def envelope(x):
 if x<=0:return 0.
 if x>=1:return 1.
 u=math.acos(1-x-x*x)
 return (u-math.sin(u)/(1+x))/math.pi
for x in [.001,.01,.1,.2,.5,.8,.95]:
 qm=x/(x+2);best=cdf(x,qm)
 ck('stationary residence envelope x'+str(x),abs(best-envelope(x))<1e-12)
 ck('q grid does not exceed envelope x'+str(x),max(cdf(x,x*j/1000) for j in range(1001))<=best+1e-12)
ck('radial benchmark',abs(cdf(.5,0)-(.5-1/math.pi))<1e-12)
# Monotonic contraction/stellar-density selection has wrong ordering for dense DM targets.
order={}
for x in rows:
 rh=x['r12_pc']*.75;order[x['name']]={'stellar_density_proxy_Mb_over_rh3':x['Mb_Msun']/rh**3,'stellar_surface_proxy_Mb_over_rh2':x['Mb_Msun']/rh**2,'stellar_potential_proxy_Mb_over_rh':x['Mb_Msun']/rh}
for a in ['Fornax','Leo I']:
 for other in ['Draco','Ursa Minor']:
  for metric in ['stellar_density_proxy_Mb_over_rh3','stellar_surface_proxy_Mb_over_rh2','stellar_potential_proxy_Mb_over_rh']:
   ck(a+' exceeds '+other+' '+metric,order[a][metric]>order[other][metric])
# Fixed fully-settled baseline must itself be reduced to permit nonnegative free mass.
settle_limits={}
for name in ['Fornax','Leo I']:
 x=by[name];draw=x['footings']['canonical']['retained_settled_over_Mb'];lim=(x['Mdyn_in_r12_over_Mb']-.512)/draw;settle_limits[name]=lim
 ck(name+' original retained baseline too high',0<lim<1)
output=[]
for x in rows:
 eta=x['fraction_all_cold_needed_inside_r12'];R=x['r12_pc']
 # At least this fraction must be on more compact orbits if all others have ra>=10R.
 compact=max(0,(eta-envelope(.1))/(1-envelope(.1)))
 lo,hi=0.,1.
 if 0<eta<1:
  for _ in range(70):
   mid=(lo+hi)/2
   if envelope(mid)<eta:lo=mid
   else:hi=mid
  xmax=(lo+hi)/2;ra_max=R/xmax
  ck(x['name']+' inverse envelope',abs(envelope(xmax)-eta)<1e-10)
 else:ra_max=None
 req_survive=eta;lossmax=1-eta
 output.append({'name':x['name'],'cold_fraction_inside_r12':eta,'minimum_fraction_compact_ra_lt_10r12':compact,'common_apocentre_upper_pc_if_all_cold_has_same_ra':ra_max,'largest_permitted_total_cold_loss_fraction':lossmax,'fret_max_if_80percent_stock_lost':.2*x['retention_max_for_cold_only_budget']})
ck('outer residence at10r below2percent',0<envelope(.1)<.02)
ck('at fixed energy initial ra10R implies final ra at least5R',envelope(.2)<.06)
# Reference simulations are explicitly not the inventory-normalized project model.
refmass={'Draco':4e9,'Fornax':1.5e10};mismatch={n:refmass[n]/(53.64*by[n]['Mb_Msun']) for n in refmass}
ck('reference Draco initial mass over100times project stock',mismatch['Draco']>100)
ck('reference Fornax initial mass over7times project stock',mismatch['Fornax']>7)
res={'claim_id':'CE-FM-078','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'stellar_ordering':order,'maximum_retained_settlement_multiplier':settle_limits,'Kepler_max_time_fraction_inside_R_for_apocentre10R':envelope(.1),'Kepler_max_fraction_for_ra_at_least5R':envelope(.2),'dwarf_targets':output,'reference_initial_mass_over_project_stock':mismatch,'scope':'Conditional analytical Kepler-orbit residence model, fixed inventory/central-value Wolf estimates, and stellar-proxy ordering. Not a full extended self-gravitating/tidal model or real self-interaction prediction.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k not in ['checks','stellar_ordering']},indent=2))
