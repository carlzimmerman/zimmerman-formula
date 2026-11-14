"""Read-only summarization and corrected-label rendering of completed results."""
import os,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR',str(P/'.mplcache'))
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((P/'positive_01/result.json').read_text());summary=[]
for f in result['fixtures']:
    for c in f['cases']:
        summary.append(dict(fixture=f['fixture'],loglambda=c['loglambda'],logmass_total=c['logmass_total'],mass_msun=c['mass_msun'],
            shear=c['aqual']['shear_magnitude'],chi2_aqual=c['aqual']['chi2'],chi2_sie=c['sie']['chi2'],
            delta_penalized_MAP=c['delta_penalized_MAP_objective'],KKT_scaled=c['aqual']['projected_gradient_scaled_inf'],
            field_path=str(P/'positive_01'/f['fixture']/('lnlambda_'+str(int(c['loglambda'])))/'best_field.npz')))
    data=P/'positive_01'/f['fixture']/'lnlambda_2/reconstruction.npz';z=np.load(data);fig,axes=plt.subplots(2,3,figsize=(12,8))
    mask=z['mask'];noise=z['noise'];raw=z['data'];stretch=np.percentile(raw[mask],99)/8
    for row,(label,mkey,skey) in enumerate([('AQUAL','model_valid','source'),('matched SIE','sie_model_valid','sie_source')]):
        model=np.full(raw.shape,np.nan);model[mask]=z[mkey]
        images=[np.arcsinh(model/stretch),np.where(mask,(raw-model)/noise,np.nan),z[skey]]
        for col,(ax,im,title) in enumerate(zip(axes[row],images,[label+' total model',label+' residual / RMS',label+' nonnegative source'])):
            ax.imshow(im,origin='lower',extent=[-5,5,-5,5] if col<2 else [-.63,.63,-.63,.63],
                cmap='RdBu_r' if col==1 else 'magma',vmin=-4 if col==1 else None,vmax=4 if col==1 else None)
            ax.set_title(title);ax.set_xlabel('West (arcsec)' if col<2 else 'Source west relative to quasar (arcsec)')
            if col<2:ax.set_xlim(-3.1,3.1);ax.set_ylim(-3.1,3.1)
            ax.set_ylabel('North (arcsec)')
    fig.suptitle(f['fixture']+' — physical source, fixed ln(lambda)=2; conditional model comparison')
    fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(P/(f['fixture']+'_positive_final.png'),dpi=145);plt.close(fig)
(P/'summary.json').write_text(json.dumps(dict(scope='Completed finite conditional host results; not evidence or exclusion.',cases=summary),indent=2)+'\n')
paths=[P/x for x in ['run_host.py','operator_controls.py','final_field_check.py','positive_profiles.py','render_summary.py','README.md','summary.json']]
paths+=list(P.glob('contract*.json'))+list(P.glob('launch*.json'))+list(P.glob('*_positive_final.png'))
state=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),known_active_owned_scientific_jobs=False,
    OS_process_inventory=dict(status='unavailable in default sandbox',observed_error="PermissionError: Operation not permitted: ps"),
    scientific_child_states={},unified_exec_sessions=dict(run_01='64588 observed terminal exit0',operator_01='11812 observed terminal exit0',
        field_check_01='outer session handle not retained; bounded scientific child observed terminal exit0 in manifest',positive_01='50215 observed terminal exit0'),sha256={})
for tag in ['run_01','operator_01','field_check_01','positive_01']:
    p=P/tag/'manifest.json';m=json.loads(p.read_text());assert m['run']['status']=='completed' and m['run']['exit_status']==0
    state['scientific_child_states'][tag]=m['run'];paths.extend([p,P/tag/'result.json'])
paths+=list((P/'field_check_01').glob('*/best_field*.npz'))+list((P/'positive_01').glob('*/*/best_field.npz'))
for p in paths:state['sha256'][str(p.relative_to(P))]=sha(p)
(P/'terminal_state.json').write_text(json.dumps(state,indent=2)+'\n')
print(json.dumps(dict(terminal_runs=list(state['scientific_child_states']),cases=len(summary),hash_count=len(state['sha256'])),indent=2))
