import json,pathlib,numpy as np
from scipy.interpolate import CubicSpline
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];L=P.parent/'cold_lens_phase_2026_10_25'
rows=[]
for packet in (L,P):
 for f in sorted((packet/'runs').glob('*.json')):
  d=json.loads(f.read_text());h=d['history'][-1];rows.append(dict(packet=packet.name,tag=f.stem,status=d['status'],t=h['t'],phase_bad=h['phase_bad_fraction'],E_error=h['E_relative_error'],gauge_absolute=h.get('gauge_absolute_relative'),J_error=h['J_relative_error'],aperture_Msun=h['field_aperture_Msun'],RSS=d['peak_RSS_bytes']))
matched=[]
for tag in ['draco_HJ_v2_N64','draco_HJ_v2_N96','draco_matched_dt001_T3','draco_matched_nr2049_T3']:
 f=P/'runs'/f'{tag}.json'
 if not f.exists():continue
 d=json.loads(f.read_text());h=min(d['history'],key=lambda h:abs(h['t']-3));assert abs(h['t']-3)<1e-10
 ff=np.load(f.with_suffix('.npz'));i=int(np.argmin(abs(ff['times']-3)));matched.append(dict(tag=tag,E_error=h['E_relative_error'],gauge_absolute=h['gauge_absolute_relative'],gauge_signed=h['gauge_signed_relative'],phase_bad=h['phase_bad_fraction'],J_error=h['J_relative_error'],CDF=ff['physical_CDF'][i].tolist()))
if matched:
 base=matched[0]['CDF']
 for m in matched:m['CDF_difference_from_N64']=float(np.max(abs(np.array(m.pop('CDF'))-base)))
# Actual physical field difference from old static frame at a short common stage.
old=ROOT/'sol61_push/cold_conservative_phase_2026_10_24/runs/draco_short_N64_dt0.02_B28.npz';new=P/'runs/draco_short_nr2049.npz';short=None
if new.exists():
 b=np.load(old);a=np.load(new);x=a['x'];r=np.sqrt(x[:,None,None]**2+x[None,:,None]**2+x[None,None,:]**2);assert np.array_equal(x,b['x'])
 parent=ROOT/'sol61_push/cold_envelope_formation_2026_10_24/runs/draco_escape_long_fields.npz';fp=np.load(parent);lm=fp['lm'];j=next(i for i,x in enumerate(lm) if tuple(x)==(0,0));rv=fp['r'];v=fp['initial'];valid=(rv<21.8)&(abs(v[:,j])>1e-20);eta=json.loads(parent.with_name('draco_escape_long.json').read_text())['physical']['eta_code'];sin=CubicSpline(rv[valid],eta*np.unwrap(np.angle(v[valid,j])));Rend=rv[valid][-1];Sin=np.where(r<=Rend,sin(r),sin(Rend)+sin(Rend,1)*(r-Rend));pa=b['u']*np.exp(1j*Sin/eta);pn=a['u']*np.exp(1j*CubicSpline(a['reference_R'],a['S'])(r)/eta);align=np.angle(np.vdot(pa,pn));short=dict(t=.5,n=64,dt=.02,new_reference_nr=2049,relative_physical_wave_L2=float(np.linalg.norm(pn*np.exp(-1j*align)-pa)/np.linalg.norm(pa)),max_density_cell_mass_difference=float(np.max(abs(abs(pn)**2-abs(pa)**2))))
out=dict(cases=rows,draco_matched_t3=matched,draco_short_static_comparison=short,non_claims=['no improved final cold remnant','no stellar survival/no-overboost verdict','no actual energy/angular momentum escape receiver','no ontology or current Khronon bridge'])
(P/'analysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
