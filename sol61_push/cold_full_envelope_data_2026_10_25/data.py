"""Explicit exploratory selection; not a reconstruction of published membership."""
import csv,gzip,json,math,sys
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
CATS={r['name']:r for r in csv.DictReader((ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv').open())}
def geometry(ra,dec,cat):
 dx=np.deg2rad(np.asarray(ra)-float(cat['ra']))*math.cos(math.radians(float(cat['dec'])))
 dy=np.deg2rad(np.asarray(dec)-float(cat['dec']));pa=math.radians(float(cat['position_angle']));q=1-float(cat['ellipticity']);distance=float(cat['distance'])
 R=np.sqrt((dx*np.sin(pa)+dy*np.cos(pa))**2+((dx*np.cos(pa)-dy*np.sin(pa))/q)**2)*distance*1000*np.sqrt(q)
 perspective=4.74047*distance*(float(cat['pmra'])*dx+float(cat['pmdec'])*dy)
 return R,perspective

def load(name,halfwindow=50.,pmfloor=.05,variables=False):
 cat=CATS[name];vs=float(cat['vlos_systemic']);aa=[float(cat['rhalf_sph_physical'])]
 if name=='Sextans':
  sys.path.insert(0,str(ROOT/'sol61_push/cold_survey_capture_2026_10_24'))
  import survey
  d=survey.load();d.update(lo=180-d['perspective'],hi=260-d['perspective'],name=name,cat=cat)
  return d
 file,target={'Draco':('hectocat.dat.gz','Draco_1'),'Leo I':('hectocat.dat.gz','Leo_1'),'Fornax':('m2fshi.dat.gz','Fornax_1')}[name]
 rows=[];counts=dict(target_rows=0,unique_first=0,quality=0,astrometry=0,velocity=0);seen=set()
 for line_num,l in enumerate(gzip.open(ROOT/'real_research/data/walker2023'/file,'rt'),1):
  if l[12:28].strip()!=target:continue
  counts['target_rows']+=1
  if l[679:681].strip()!='1':continue
  counts['unique_first']+=1
  def n(a,b):
   try:return float(l[a-1:b])
   except ValueError:return float('nan')
  id=l[71:90].strip();v=n(700,706);ev=n(708,711)
  if not (id and n(689,690)>0 and 0<ev<5 and n(754,758)<3.5 and n(846,846)==0 and n(848,848)==0 and (variables or n(850,850)==0) and n(874,874)==0 and n(876,876)==0):continue
  counts['quality']+=1
  pmra,pmdec,era,edec,par,ep=[n(a,b) for a,b in [(188,195),(197,204),(206,210),(212,216),(218,224),(226,232)]]
  if not np.isfinite([pmra,pmdec,era,edec,par,ep]).all():continue
  chi=sum((p-float(cat[k]))**2/(e*e+float(cat[k+'_em'])**2+pmfloor**2) for p,e,k in [(pmra,era,'pmra'),(pmdec,edec,'pmdec')])
  if not (chi<9 and abs(par-1/float(cat['distance']))<3*math.sqrt(ep*ep+.02**2)):continue
  counts['astrometry']+=1
  if not abs(v-vs)<halfwindow:continue
  counts['velocity']+=1
  assert id not in seen,('duplicate source',name,id);seen.add(id)
  rows.append(dict(id=id,source_line=line_num,RA=n(234,248),DE=n(250,264),v=v,ev=ev,PM_chi2=chi,goodNobs=n(689,690),variable=n(850,850)))
 assert rows
 R,persp=geometry([r['RA'] for r in rows],[r['DE'] for r in rows],cat)
 return dict(name=name,cat=cat,R=R,v=np.array([r['v'] for r in rows])-persp,ev=np.array([r['ev'] for r in rows]),perspective=persp,lo=vs-halfwindow-persp,hi=vs+halfwindow-persp,aa=np.array(aa),ids=[r['id'] for r in rows],source_rows=rows,counts=counts,coverage=dict(R_pc_percentiles=np.percentile(R,[0,10,50,90,100]).tolist()),selection=dict(halfwindow=halfwindow,pmfloor=pmfloor,include_velocity_variables=variables))
