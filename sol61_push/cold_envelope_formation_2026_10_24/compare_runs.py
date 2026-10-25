"""Saved finite comparisons; record sensitivities rather than manufacture pass flags."""
import pathlib,json,hashlib,numpy as np
P=pathlib.Path(__file__).resolve().parent
names=['sextans_nogas_L12','sextans_monopole','sextans_nogas_refine','sextans_L24','sextans_M6_control','sextans_L24_long','sextans_late_dt02','restart_original_check','restart_fast_check']
files=[pathlib.Path(__file__),P/'stellar_probes.json']+[P/'runs'/f'{t}.json' for t in names]+[P/'runs'/f'{t}_fields.npz' for t in ['sextans_nogas_L12','sextans_monopole','restart_original_check','restart_fast_check']]
def hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=hashes();q={t:json.loads((P/'runs'/f'{t}.json').read_text()) for t in names}
def at(tag,t):return next(h for h in q[tag]['history'] if abs(h['t']-t)<1e-7)
a=np.load(P/'runs/sextans_nogas_L12_fields.npz')['initial'];b=np.load(P/'runs/sextans_monopole_fields.npz')['initial'];initial_difference=float(np.linalg.norm(a-b));assert initial_difference<1e-15
ctrl=[]
for tag in ['sextans_nogas_L12','sextans_monopole']:
 p=q[tag]['parameters'];assert p['lmax']==12 and p['nr']==512 and p['dt']==.02
 hs=[h for h in q[tag]['history'] if h['t']<=15+1e-8];emax=max(abs(h.get('E_residual',0)) for h in hs);jmax=max(abs(h.get('J_residual',0)) for h in hs);assert emax<.01 and jmax<.01
 ctrl.append({'tag':tag,'T':15,'high_l_mass':at(tag,15)['l_gt4_mass'],'max_energy_residual':emax,'max_spin_residual':jmax})
# Cell-face, not node-centre cumulative interpolation.
def cdf_on(tag,h,rad):
 r=np.array(q[tag]['radial_grid']);ed=np.r_[0,(r+np.r_[r[1:],q[tag]['parameters']['rmax']])/2];return np.interp(rad,ed,np.r_[0,h['cdf']])
rad=np.geomspace(.02,16,300);radial=[]
for T in [15.,20.]:
 a=at('sextans_nogas_L12',T);b=at('sextans_nogas_refine',T)
 radial.append({'T':T,'coarse_high_l':a['l_gt4_mass'],'refined_high_l':b['l_gt4_mass'],'max_CDF_absolute_difference':float(np.max(abs(cdf_on('sextans_nogas_L12',a,rad)-cdf_on('sextans_nogas_refine',b,rad))))})
az=[]
for T in [0.,5.,10.,15.,20.]:
 a=at('sextans_L24',T);b=at('sextans_M6_control',T)
 az.append({'T':T,'M4_high_l':a['l_gt4_mass'],'M6_high_l':b['l_gt4_mass'],'max_CDF_difference':float(np.max(abs(np.array(a['cdf'])-b['cdf'])))})
assert az[0]['max_CDF_difference']<1e-12
coarse=at('sextans_L24_long',80.);fine=at('sextans_late_dt02',80.)
dt={'T':80,'max_CDF_difference':float(np.max(abs(np.array(coarse['cdf'])-fine['cdf']))),'mass_difference':coarse['M']-fine['M'],'Jz_difference':coarse['Jz']-fine['Jz']}
a=np.load(P/'runs/restart_original_check_fields.npz')['final'];b=np.load(P/'runs/restart_fast_check_fields.npz')['final'];restart=float(np.linalg.norm(a-b)/np.linalg.norm(a));assert restart<1e-12
probes=json.loads((P/'stellar_probes.json').read_text())['results'];probecheck=[]
for v in [r for r in probes if r['dt_code']==.005]:
 coarse=next(r for r in probes if r['tag']==v['tag'] and r['birth_t']==v['birth_t'] and r['population']==v['population'] and r['dt_code']==.01)
 a=coarse['results']['varying'];b=v['results']['varying'];err=abs(a['final_r50_over_initial']-b['final_r50_over_initial']);static=v['results']['static_mean']['max_starwise_fractional_radius_change'];assert err<1e-5 and static<1e-10
 probecheck.append({'tag':v['tag'],'birth_t':v['birth_t'],'population':v['population'],'dt_halving_final_r50_ratio_difference':err,'static_control_max_fractional_radius_change':static})
after=hashes();assert before==after
out={'scope':'finite controls and unresolved sensitivities, no continuum/theory completion','inputs_before':before,'inputs_after':after,'initial_matched_field_norm_difference':initial_difference,'matched_mode_control':ctrl,'radial_and_dt_sensitivity':radial,'azimuthal_sensitivity':az,'late_dt_sensitivity':dt,'restart_relative_field_difference':restart,'probe_integration_checks':probecheck}
(P/'run_comparisons.json').write_text(json.dumps(out,indent=2)+'\n');print('Matched control passed; sensitivities recorded; restart/probe numerical comparisons passed.');print(radial);print(dt)
