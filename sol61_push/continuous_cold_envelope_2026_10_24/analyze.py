"""Compare stored envelope trajectories without rerunning the PDE."""
import json
from pathlib import Path

b=Path(__file__).parent
tags=['f0','f20','f40','f20_refine','f20_pad']
runs={t:json.loads((b/'runs'/(t+'.json')).read_text()) for t in tags}
summary={};checks={}
for tag,d in runs.items():
    i,f=d['initial'],d['final'];sgn=1 if i['J_inner']>=0 else -1;j0=abs(i['J_inner'])
    scan=[]
    for h in d['history']:
        scan.append({'t':h['t'],'mass_removed':h['removed']['M'],
          'inner_spin_loss':sgn*(i['J_inner']-h['J_inner'])/j0,
          'outer_spin_gain':sgn*(h['J_outer']-i['J_outer'])/j0})
    allowed=[h for h in scan if h['mass_removed']<=.01146]
    peak=max(allowed,key=lambda h:h['outer_spin_gain'])
    residual=abs(f['M']+f['removed']['M']-i['M'])
    checks[tag+'_mass_ledger']=residual<1e-8
    checks[tag+'_core_outer_mass_partition']=abs(f['M_inner']+f['M_outer']-f['M'])<1e-12
    checks[tag+'_core_outer_spin_partition']=abs(f['J_inner']+f['J_outer']-f['J'])<1e-12
    summary[tag]={'parameters':d['parameters'],'initial_inner_mass':i['M_inner'],
        'final_inner_mass':f['M_inner'],'final_mass_retained':f['M'],
        'final_mass_removed':f['removed']['M'],
        'inner_mass_ratio':d['final_inner_mass_ratio'],
        'inner_specific_spin_ratio':d['final_inner_specific_spin_ratio'],
        'J_ledger_relative':d['J_ledger_relative'],'E_ledger_relative':d['E_ledger_relative'],
        'gates':d['gates'],'max_transient_outer_gain_under_cap_REPORTED_ONLY':peak,
        'virial_moment_ratios':d['final_virial_moment_ratios'],
        'peak_rss_bytes_macos':d['peak_rss_bytes_macos']}
comparisons={}
for tag in ['f20_refine','f20_pad']:
    fields={}
    for key in ['M','M_inner','J_inner']:
        x,y=runs['f20']['final'][key],runs[tag]['final'][key]
        fields[key]={'base':x,'control':y,'relative_difference':abs(x-y)/max(abs(x),1e-12),
                     'contract_gate':abs(x-y)<=max(.01,.1*abs(x))}
    comparisons[tag]=fields
assert all(checks.values()),checks
result={'runs':summary,'partition_and_mass_checks':checks,'control_comparisons':comparisons,
        'scope':'Frozen T30 storage and T60 formation gates retained. Transient scan is reported-only; virial moment is not live stellar heating. Base-box J-ledger failures prevent a converged transfer-rate claim.'}
(b/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({t:{k:r[k] for k in ['final_mass_removed','inner_mass_ratio','inner_specific_spin_ratio',
                  'J_ledger_relative','max_transient_outer_gain_under_cap_REPORTED_ONLY']} for t,r in summary.items()},indent=2))
