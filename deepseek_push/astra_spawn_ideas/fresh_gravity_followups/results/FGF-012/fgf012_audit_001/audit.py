"""Independent raw-catalog audit. Only inherited M force is shared code."""
import sys, json, csv, math, itertools, argparse
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
ROOT=Path.cwd(); sys.path.insert(0,str(ROOT))
from campaign_fresh_gravity_astra.stage_03.cluster_precision.constraint import force as registered_force
ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True); OUT=ap.parse_args().out
OUT.mkdir(parents=True,exist_ok=True)
DATA=ROOT/'real_research/data'; OLD=ROOT/'campaign_fresh_gravity_astra/stage_04/cluster_observables/run_002'
NAMES=['A1795','A2029','A2142','A2319','A644','A85','ZW1215']
G,MSUN,KPC=6.67430e-11,1.98847e30,3.085677581491367e19
checks=[]
def check(name, observed, limit, passed):
 checks.append(dict(name=name,observed=observed,tolerance=limit,pass_=bool(passed)))
def sep(ra,dec,ras,decs):
 d=np.deg2rad(decs); d0=math.radians(dec)
 q=np.sin((d-d0)/2)**2+np.cos(d)*math.cos(d0)*np.sin(np.deg2rad(ras-ra)/2)**2
 return np.rad2deg(2*np.arctan2(np.sqrt(q),np.sqrt(np.maximum(0,1-q))))*60
# Parsing, units and interpolation are independent of the worker helpers.
def profile(n,kind,ext):
 with fits.open(DATA/'xcop'/n/(n+'_'+kind+'.fits')) as h:
  t=h[ext]; unit=t.columns['RADIUS'].unit
  fac={'kpc':1.,'Mpc':1000.}.get(unit)
  if unit=='R/R500':fac=float(t.header['R500'])
  assert fac is not None
  r=np.asarray(t.data['RADIUS'],dtype=float)*fac
  assert np.all(np.diff(r)>0)
  cols={k:np.asarray(t.data[k],dtype=float) for k in t.columns.names}
  return r,cols,dict(units={k:t.columns[k].unit for k in t.columns.names},header={k:t.header[k] for k in ['RA','DEC','REDSHIFT','R500'] if k in t.header})
def logat(r,x,y):
 assert x[0]<=r<=x[-1] and np.all(y>0)
 j=min(int(np.searchsorted(x,r,side='right'))-1,len(x)-2); j=max(j,0)
 w=math.log10(r/x[j])/math.log10(x[j+1]/x[j])
 return float(y[j]*(y[j+1]/y[j])**w)
def force(B,a,k):
 if k=='Q':return math.hypot(B,math.sqrt(a*B))
 if k=='R':return B/-math.expm1(-math.sqrt(B/a))
 return float(registered_force(B,a,'M'))
def bisect(fun,lo=.01,hi=100.):
 assert fun(lo)<0<fun(hi)
 for _ in range(100):
  mid=(lo+hi)/2
  if fun(mid)>0:hi=mid
  else:lo=mid
 return (lo+hi)/2
zs=json.loads((DATA/'xcop/xcop_r500_ettori2019.json').read_text())
with fits.open(DATA/'erass1cl_primary_v3.2.fits') as h:
 e=h[1].data.copy(); eu={k:h[1].columns[k].unit for k in h[1].columns.names}
 ehead=str(h[1].header)
assert eu['MGAS500']=='10**11 solMass' and eu['R500']=='kpc'
lines=(DATA/'psz2_union.tsv').read_text().splitlines(); hi=next(i for i,s in enumerate(lines) if s.startswith('Index\t'))
fields=lines[hi].split('\t'); psz=[]
for s in lines[hi+1:]:
 vals=s.split('\t')
 if len(vals)==len(fields) and vals[0].strip().isdigit():psz.append(dict(zip(fields,vals)))
pra=np.array([float(p['RAJ2000']) for p in psz]); pdec=np.array([float(p['DEJ2000']) for p in psz])
oldmatch={x['name']:x for x in csv.DictReader((OLD/'catalogue_matches.csv').open())}
oldclosure={(x['name'],x['footing'],x['scaling'],x['kernel']):x for x in csv.DictReader((OLD/'closure_requirements.csv').open())}
matched=[]; matches=[]; masses=[]; results=[]; shapes=[]; semantics=[]; deps=[]
maxsep=maxforce=maxroot=maxalt=0.
for n in NAMES:
 profiles={k:profile(n,k,ex) for k,ex in [('fgas_profile',1),('hydro_mass',1),('mstar',2)]}
 meta=profiles['mstar'][2]; ra=meta['header']['RA'];dec=meta['header']['DEC'];z=zs[n]['z']
 ed=sep(ra,dec,e['RA'],e['DEC']);i=int(np.argmin(ed)); er=e[i]
 pd=sep(ra,dec,pra,pdec);j=int(np.argmin(pd));pr=psz[j]
 ez=float(er['BEST_Z']);pz=float(pr['z'])
 em=bool(ed[i]<=5 and abs(ez-z)<=.01);pm=bool(pd[j]<=5 and abs(pz-z)<=.01)
 row=dict(name=n,RA=ra,DEC=dec,z=z,erass_zero_based_row=i,erass_name=str(er['NAME']).strip(),erass_DETUID=str(er['DETUID']).strip(),erass_separation_arcmin=float(ed[i]),erass_z=ez,erass_match=em,psz_Index=pr['Index'].strip(),psz_name=pr['Name'].strip(),psz_separation_arcmin=float(pd[j]),psz_z=pz,psz_match=pm,erass_candidates_within_gate=int(np.sum((ed<=5)&(abs(e['BEST_Z']-z)<=.01))))
 matches.append(row)
 assert em==(oldmatch[n]['erass_match']=='True') and pm==(oldmatch[n]['psz_match']=='True')
 maxsep=max(maxsep,abs(ed[i]-float(oldmatch[n]['erass_separation_arcmin'])),abs(pd[j]-float(oldmatch[n]['psz_separation_arcmin'])))
 rg,cg,_=profiles['fgas_profile']; d=abs(cg['FGAS']/(cg['MGAS']/cg['M_NFW'])-1)
 deps.append(dict(name=n,relation='FGAS=MGAS/M_NFW',median=float(np.median(d)),max=float(max(d))))
 if not em:continue
 matched.append(n);r=float(er['R500']);bounds={};alt={};brackets={}
 for kind,key,low,high,errors in [('fgas_profile','MGAS','MGAS_LO','MGAS_HI',True),('hydro_mass','M_FORW','EM_FORW','EM_FORW',True),('mstar','MSTAR','MSTAR_LO','MSTAR_HI',False)]:
  x,d,m=profiles[kind]
  for k in (key,low,high):assert m['units'][k] in ('Msun','M_sun')
  c=logat(r,x,d[key]);l=logat(r,x,d[low]);h=logat(r,x,d[high])
  bounds[kind]=(c-l,c,c+h) if errors else (l,c,h)
  alt[kind]=(logat(r,x,d[key]-d[low]),c,logat(r,x,d[key]+d[high])) if errors else (l,c,h)
  assert 0<bounds[kind][0]<c<bounds[kind][2]
  j=int(np.searchsorted(x,r));brackets[kind]=dict(support=[float(x[0]),float(x[-1])],bracket_indices=[j-1,j],radii=[float(x[j-1]),float(x[j])],metadata=m)
 elo,emass,ehi=[float(er[k])*1e11 for k in ('MGAS500_L','MGAS500','MGAS500_H')]
 assert 0<elo<emass<ehi
 xl,xc,xh=bounds['fgas_profile'];sl,sc,sh=bounds['mstar'];hl,hc,hh=bounds['hydro_mass'];eta=emass/xc
 masses.append(dict(name=n,radius_kpc=r,erass_R500_endpoints=[float(er['R500_L']),float(er['R500_H'])],erass_gas=[elo,emass,ehi],xcop_boxes=bounds,gas_ratio=eta,gas_ratio_box=[elo/xh,ehi/xl],radial_evidence=brackets,erass_KT=[float(er[k]) for k in ('KT_L','KT','KT_H')],erass_RA_XFIT=float(er['RA_XFIT']),erass_DEC_XFIT=float(er['DEC_XFIT']),erass_refit_center_offset_arcmin=float(sep(ra,dec,np.array([er['RA_XFIT']]),np.array([er['DEC_XFIT']]))[0])))
 for label,val in [('YX/(KT MGAS)',float(er['YX500'])/(float(er['KT'])*float(er['MGAS500']))),('FGAS/(MGAS/M500)',float(er['FGAS500'])/(float(er['MGAS500'])/(100*float(er['M500']))))]:deps.append(dict(name=n,relation=label,ratio=val))
 C=G*MSUN/(r*KPC)**2
 for foot,a0 in [('canonical',9.3619e-11),('alternative',1.1279e-10)]:
  for scaling in ['vacuum','H']:
   a=a0*(1 if scaling=='vacuum' else math.sqrt(.315*(1+z)**3+.685))
   for k in ['Q','R','M']:
    def p(me,mx,ms,mh):return me/mx*force(C*(me+ms),a,k)/(C*mh)
    vals=[p(*v) for v in itertools.product([elo,ehi],[xl,xh],[sl,sh],[hl,hh])]
    p0=p(emass,xc,sc,hc);pl=p(elo,xh,sl,hh);ph=p(ehi,xl,sh,hl)
    assert min(vals)==pl and max(vals)==ph
    b=bisect(lambda b:p(b*emass,xc,sc,hc)-1);blo=bisect(lambda b:p(b*ehi,xl,sh,hl)-1)
    maxroot=max(maxroot,abs(p(b*emass,xc,sc,hc)-1),abs(p(blo*ehi,xl,sh,hl)-1))
    old=oldclosure[n,foot,scaling,k]
    for v,key in [(p0,'pressure_gradient_ratio_required'),(pl,'pressure_gradient_ratio_box_low'),(ph,'pressure_gradient_ratio_box_high'),(b,'further_erass_gas_multiplier_needed_at_fixed_pressure'),(blo,'smallest_further_erass_gas_multiplier_in_box')]:maxforce=max(maxforce,abs(v-float(old[key])))
    pah=p(ehi,alt['fgas_profile'][0],sh,alt['hydro_mass'][0]);maxalt=max(maxalt,abs(pah/ph-1))
    results.append(dict(name=n,footing=foot,scaling=scaling,kernel=k,a=a,pcentral=p0,pmin=pl,pmax=ph,gas_boost=b,box_gas_boost=blo,ellcentral=b**-2,ellmax=blo**-2,endpoint_interpolation_pmax=pah))
    L=eta/p0;f=.05;inner=(eta-f*L)/(1-f)
    reconstructed=(1-f)*inner+f*L
    # p=1 and a changed local density L give F/(gH/L)=1 exactly.
    closure=force(C*(emass+sc),a,k)/(C*hc/L)
    shapes.append(dict(name=n,footing=foot,scaling=scaling,kernel=k,enclosed_ratio=eta,outer_original_gas_fraction=f,outer_density_ratio=L,inner_density_ratio=inner,reconstructed_enclosed_ratio=reconstructed,force_ratio=closure))
    assert inner>0 and abs(reconstructed-eta)<1e-14 and abs(closure-1)<1e-14
# Independent mask read and map/mask WCS equality, still using shared astropy library.
mapfile=ROOT/'deepseek_push/Z06_data/ilc_actplanck_ymap.fits'; maskfile=ROOT/'deepseek_push/Z06_data/wide_mask_GAL070_apod_1.50_deg_wExtended.fits'
with fits.open(mapfile,memmap=True) as h, fits.open(maskfile,memmap=True) as mh:
 w=WCS(h[0].header);mw=WCS(mh[0].header); ny,nx=h[0].shape
 assert h[0].shape==mh[0].shape
 for row in matches:
  x,y=[float(t) for t in w.world_to_pixel_values(row['RA'],row['DEC'])];mx,my=[float(t) for t in mw.world_to_pixel_values(row['RA'],row['DEC'])]
  assert abs(x-mx)+abs(y-my)<1e-9
  inside=0<=x<nx and 0<=y<ny
  row.update(map_xy=[x,y],map_in_bounds=inside,mask_value=float(mh[0].data[round(y),round(x)]) if inside else None)
  old=oldmatch[row['name']];assert inside==(old['ACT_map_in_rectangular_bounds']=='True')
  if inside:assert row['mask_value']==float(old['ACT_center_mask'])
# Authenticate only schema contents, not absence of thermal information in all possible catalogs.
for path in sorted((ROOT/'deepseek_push/G236_eRASS3_data').glob('*.fits.gz')):
 with fits.open(path,memmap=False,lazy_load_hdus=True) as h:
  cols=h[1].columns.names
  semantics.append(dict(path=str(path.relative_to(ROOT)),rows=h[1].header['NAXIS2'],thermal_named_columns=[k for k in cols if k.upper() in ['KT','MGAS500','M500','TEMPERATURE','PRESSURE','DENSITY']]))
check('source matched objects',matched,['A644','ZW1215'],matched==['A644','ZW1215'])
check('independent haversine versus worker separation max arcmin',maxsep,1e-8,maxsep<1e-8)
check('independent mass/Q/R algebra, registered M, and bisection versus worker max absolute difference',maxforce,1e-10,maxforce<1e-10)
check('48 independent bisection roots forward residual',maxroot,1e-12,maxroot<1e-12)
check('24 box ceilings below one',max(x['pmax'] for x in results),1,all(x['pmax']<1 for x in results))
check('endpoint-mass interpolation sensitivity max fractional difference',maxalt,0.01,maxalt<.01)
check('positive nonuniform density countermodels',min(x['inner_density_ratio'] for x in shapes),0,all(x['inner_density_ratio']>0 for x in shapes))
check('A644 geometric coverage is insufficient',next(x['mask_value'] for x in matches if x['name']=='A644'),0,next(x['mask_value'] for x in matches if x['name']=='A644')==0)
summary=dict(checks=checks,ceilings={n:max(x['pmax'] for x in results if x['name']==n) for n in matched},emissivity_ceilings={n:max(x['ellmax'] for x in results if x['name']==n) for n in matched},matched_count=len(matched),psz_match_count=sum(x['psz_match'] for x in matches),no_external_pipeline_semantics_authenticated=True,shared_code='Only M uses source-pinned constraint.force; its algorithm is not independently validated by this run.',finite_assertion_pass=all(x['pass_'] for x in checks))
for filename,obj in [('checks.json',summary),('matches.json',matches),('masses_and_apertures.json',masses),('force_boxes.json',results),('nonuniform_countermodels.json',shapes),('dependency_diagnostics.json',deps),('schema_audit.json',semantics)]:
 (OUT/filename).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(summary,indent=2));assert summary['finite_assertion_pass']
