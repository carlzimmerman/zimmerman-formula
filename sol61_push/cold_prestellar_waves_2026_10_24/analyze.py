"""Interpret finite runs without promoting a sink or a low-spin aperture to closure."""
import json,math,hashlib,importlib.util
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
capture=json.loads((ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json').read_text())
previous=json.loads((ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json').read_text())
spec=importlib.util.spec_from_file_location('survey',ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey.py')
survey=importlib.util.module_from_spec(spec);spec.loader.exec_module(survey)
data=survey.load(); ref=json.loads((ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey_results.json').read_text())
ref_nll=min(v['nll'] for v in ref['continuous_best'] if v['footing']=='canonical' and v['beta']==0 and v['tracer_taper_pc'] is None)
summaries={}
for path in sorted((HERE/'runs').glob('*.json')):
    q=json.loads(path.read_text());h=q['history'][-1];i=q['initial'];u=q['physical'];name=q['parameters']['galaxy']
    M=u['Munit_Msun'];R=u['Runit_pc'];V=u['Vunit_kms'];massout=h['removed']['M'];Jout=h['removed']['J']
    g=previous['galaxies'][name]
    if name=='Sextans':
        a1,a2=data['aa'];rr=np.array(q['radial_grid']);cdf=np.array(h['cdf'])
        def gtotal(rad):
            gn=sum(survey.G*250000*rad/(rad*rad+ar*ar)**1.5 for ar in data['aa'])
            cold=survey.G*M*np.interp(rad/R,rr,cdf,left=0,right=cdf[-1])/rad**2
            return .5*(gn+np.sqrt(gn*gn+4*survey.A0['canonical']*gn))+cold
        var=np.array([survey.projection(data['R'],ar,gtotal) for ar in data['aa']]).T
        fitted=survey.fit(data,var,np.zeros_like(var),fixed_mass=0.)
        observational=dict(label='spherical-monopole Jeans diagnostic only; not full nonspherical stellar fit',
            catalogue_nll=fitted['nll'],twice_nll_above_best=2*(fitted['nll']-ref_nll))
        # Full-Plummer monopole moment supplied independently of selected-data fit.
        x,w=np.polynomial.legendre.leggauss(128);t=(x+1)*math.pi/4;w*=math.pi/4
        baselines=[]
        for ar in data['aa']:
            rad=ar*np.tan(t);gn=sum(survey.G*250000*rad/(rad*rad+b*b)**1.5 for b in data['aa'])
            gl=.5*(gn+np.sqrt(gn*gn+4*survey.A0['canonical']*gn))
            baselines.append(float(ar*np.sum(w*np.sin(t)**3*gl)))
    else:
        baselines=[g['moments']['canonical'][0]['sigma_baryon']**2]
        observational=dict(label='spherical stellar virial diagnostic only',observed_sigma=float(g['observations']['vlos_sigma']))
    row=dict(galaxy=name,status=q['status'],T_code=h['t'],T_Myr=h['t']*u['tunit_Myr'],
        angular_lmax=q['parameters']['lmax'],nr=q['parameters']['nr'],dt=q['parameters']['dt'],
        initial_energy_negative=i['E']<0,initial_mass_Msun=M,remaining_mass_Msun=h['M']*M,
        absorbed_mass_Msun=massout*M,absorbed_mass_fraction=massout/i['M'],
        removed_energy_code=h['removed']['E'],positive_sink_energy_code=h['absorber_energy_positive'],
        negative_sink_energy_code=h['absorber_energy_negative'],net_external_work_code=h['source_work'],
        equivalent_removed_specific_energy_speed_kms=V*math.sqrt(2*h['removed']['E']/massout) if massout>1e-10 and h['removed']['E']>0 else None,
        removed_J_fraction=Jout/i['J'],core_J_fraction=h['J_inner']/i['J'],
        core_mass_Msun=h['M_inner']*M,core_aperture_pc=R,
        remaining_specific_J_over_initial=(h['J']/h['M'])/(i['J']/i['M']),
        core_specific_J_over_initial=(h['J_inner']/max(h['M_inner'],1e-30))/(i['J']/i['M']),
        escaped_specific_J_over_initial=(Jout/massout)/(i['J']/i['M']) if massout>1e-10 else None,
        final_predicted_sigma_kms=[math.sqrt(b+c) for b,c in zip(baselines,h['cold_sigma2_kms2'])],
        stationarity=q['stationarity'],observational=observational,
        max_mass_residual=max(abs(z.get('mass_residual',0)) for z in q['history']),
        max_energy_residual=max(abs(z.get('energy_residual',0)) for z in q['history']),
        max_J_residual=max(abs(z.get('J_residual',0)) for z in q['history']),
        final_outward_mass_flux=h['outward_mass_flux'],peak_outward_mass_flux=max(z['outward_mass_flux'] for z in q['history']),
        peak_RSS_bytes_macos=q['peak_RSS_bytes_macos'],seconds=q['seconds'])
    row['numerical_ledger_pass']=row['max_mass_residual']<1e-8 and row['max_energy_residual']<.01 and row['max_J_residual']<.01
    radial=np.array(q['radial_grid']);ix=int(np.argmin(abs(radial-h['flux_radius'])))
    dr=float(radial[min(ix+1,len(radial)-1)]-radial[max(0,ix-1)] )/2*R
    row['radial_phase_per_cell_for_30kms_wave']=30*dr/3000
    row['outer_30kms_wave_accuracy_gate']=row['radial_phase_per_cell_for_30kms_wave']<math.pi/4
    fields=np.load(path.with_name(path.stem+'_fields.npz'));vf=fields['final'];vi=fields['initial'];modes=[tuple(x) for x in fields['lm']]
    def angular_vector(v,mask):
        z=v[mask];jp=0j
        for j,(ll,mm) in enumerate(modes):
            if mm<ll:
                jj=modes.index((ll,mm+1));jp+=math.sqrt(ll*(ll+1)-mm*(mm+1))*np.sum(z[:,jj].conj()*z[:,j])
        jz=float(np.sum(np.array([mm for ll,mm in modes])[None,:]*abs(z)**2))
        return q['physical']['eta_code']*np.array([jp.real,jp.imag,jz])
    ji=angular_vector(vi,np.ones(len(radial),bool));jf=angular_vector(vf,np.ones(len(radial),bool));jc=angular_vector(vf,radial<1)
    row['initial_J_vector']=ji.tolist();row['final_J_vector']=jf.tolist();row['core_J_vector']=jc.tolist()
    row['core_specific_J_vector_norm_over_initial']=float(np.linalg.norm(jc)/max(h['M_inner'],1e-30)/(np.linalg.norm(ji)/i['M']))
    row['initial_s_wave_mass_fraction']=float(np.sum(abs(vi[:,0])**2)/i['M'])
    row['final_s_wave_mass_Msun']=float(np.sum(abs(vf[:,0])**2)*M)
    row['final_core_s_wave_mass_Msun']=float(np.sum(abs(vf[radial<1,0])**2)*M)
    summaries[path.stem]=row
out=dict(scope='finite common-history experiment; no successful four-dwarf/stellar closure established',runs=summaries)
(HERE/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
for name,v in summaries.items():
    print(name,'ledger',v['numerical_ledger_pass'],'loss',round(v['absorbed_mass_fraction'],4),'Jout',round(v['removed_J_fraction'],4),
          'sigma',np.round(v['final_predicted_sigma_kms'],2).tolist(),'core_million',round(v['core_mass_Msun']/1e6,1))
