import json,pathlib,hashlib,numpy as np,sys
P=pathlib.Path(__file__).resolve().parent
rows=[]
for f in sorted((P/'runs').glob('*.json')):
 d=json.loads(f.read_text());h=d['history'];last=h[-1]
 rows.append(dict(tag=f.stem,status=d['status'],t=last['t'],elapsed_Myr=last['t']*d['physical']['tunit_Myr'],mass_error=d['initial_mass_relative_error'],generator_error=d['initial_generator_relative_error'],CDF_error=d['initial_CDF_absolute_error'],phase_bad=last['phase_bad_fraction'],E_error=d['energy_relative_error'],bond_residual=d['bond_residual'],tag_mass_error=last['tag_mass']-h[0]['tag_mass'],tag_excess=last['tag_excess'],field_aperture_Msun=last['field_aperture_Msun'],tag_aperture_Msun=last['tag_aperture_Msun'],RSS=d['peak_RSS_bytes']))
def state(tag):
 f=np.load(P/'runs'/f'{tag}.npz');x=f['x'];r=np.sqrt(x[:,None,None]**2+x[None,:,None]**2+x[None,None,:]**2);m=abs(f['u'])**2;i=np.argsort(r.ravel());rr=r.ravel()[i];cdf=np.cumsum(m.ravel()[i]);return f, np.interp(np.linspace(0,18,181),rr,cdf)
controls=[]
for name in ('draco','sextans','fornax','leoi'):
 tags=[f'{name}_short_N{n}_dt{dt}_B{b}' for n,dt,b in [(64,.02,28),(96,.02,28),(96,.01,28),(96,.02,20)]]
 if not all((P/'runs'/f'{t}.npz').exists() for t in tags):continue
 states=[state(t) for t in tags];ref=states[1][0]['u'];dtv=states[2][0]['u'];align=np.vdot(ref,dtv);err=np.linalg.norm(dtv*np.exp(-1j*np.angle(align))-ref)/np.linalg.norm(ref)
 controls.append(dict(galaxy=name,dt_aligned_A_relative_L2=float(err),grid_radial_CDF_absolute_error=float(max(abs(states[0][1]-states[1][1]))),box_radial_CDF_absolute_error=float(max(abs(states[3][1]-states[1][1])))))
models=json.loads((P.parent/'cold_survey_capture_2026_10_24/capture_results.json').read_text())['models']
comparison=[]
for m in models:
 key={'Draco':'draco','Sextans':'sextans','Fornax':'fornax','Leo I':'leoi'}[m['name']]
 d=json.loads((P/'runs'/f'{key}_short_N96_dt0.02_B28.json').read_text());R=d['physical']['Runit_pc'];target=m['cold_mass']*R**3/(R*R+m['cold_scale_pc']**2)**1.5;actual=d['history'][-1]['field_aperture_Msun']
 comparison.append(dict(galaxy=m['name'],stage='incoming code t=.5, not a settled remnant or stars',aperture_fraction=actual/d['physical']['Munit_Msun'],conditional_Plummer_reference_Msun=target,instantaneous_mass_to_conditional_reference=actual/target))
out=dict(cases=rows,short_controls=controls,early_conditional_comparison=comparison,non_claims=['No final bound dwarf remnant','No stellar-heating likelihood or live-star survival','No angular momentum or escape closure','No equivalence to literal Khronon or SCT-M'])
(P/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
for d in rows:print(d['tag'],d['status'],round(d['t'],3),'M_ap',round(d['field_aperture_Msun']),'E',round(d['E_error'],6),'RSS_MB',round(d['RSS']/1e6))
print('controls',controls)
