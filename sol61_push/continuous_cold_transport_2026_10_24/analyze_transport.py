"""Reproduce scalar capacity/coupling diagnostics and compare saved controls."""
import json
import math
from pathlib import Path

b=Path(__file__).parent
C=3*math.sqrt(2*math.pi)/2
qold=.01146/(1-.01146)
capacity=[{'q_out_over_core':q,'m_max':m,'lambda_removed_max':m*q/math.sqrt(C)}
          for q in [.001,.01,qold,.1] for m in [0,1,2,4,8]]
def law(y):return (y+math.sqrt(y*y+4*y))/2
coupling=[]
for x in [.01,.1,1,10]:
    y=x*x/(1+x)
    for f in [0,.1,1,5]:
        coupling.append({'baryon_only_x':x,'cold_to_baryon_enclosed':f,
                         'sourced_AQUAL_boost':law((1+f)*y)/x,
                         'add_Newton_cold_boost':1+f*y/x,
                         'sourced_AQUAL_plus_direct_cold_boost':law((1+f)*y)/x+f*y/x})
(b/'capacity_and_coupling.json').write_text(json.dumps({'C':C,'capacity_rows':capacity,
    'coupling_rows':coupling,'scope':'conditional Gaussian mode bound; older Sextans fraction only; no predicted spin or profile'},indent=2)+'\n')
tags=['spin48','zero48','reverse48','spin64','halfstep48','pad64L32']
runs={tag:json.loads((b/'transport_runs'/(tag+'.json')).read_text()) for tag in tags
      if (b/'transport_runs'/(tag+'.json')).exists()}
base=runs['spin48']
comparisons={}
for tag in ['spin64','halfstep48']:
    alt=runs[tag];fields={}
    for key in ['export_mass_fraction','export_spin_fraction','export_energy_over_initial_binding','contraction']:
        a,c=base[key],alt[key]
        fields[key]={'base':a,'control':c,'relative_difference':abs(a-c)/max(abs(a),1e-12),
                     'gate':abs(a-c)<=max(.01,.1*abs(a))}
    comparisons[tag]=fields
reverse=runs['reverse48']
parity={key:abs(base['final'][key]-reverse['final'][key])/max(abs(base['final'][key]),1e-12)
        for key in ['mass','E','rhalf']}
parity['Jz_sign_reversal']=abs(base['final']['Jz']+reverse['final']['Jz'])/abs(base['initial']['Jz'])
summary={'runs':{tag:{k:r[k] for k in ['parameters','initial','final','removed','gates',
             'export_spin_fraction','export_mass_fraction','export_energy_over_initial_binding',
             'contraction','late_radius_range_fraction','energy_ledger_relative',
             'spin_ledger_relative','peak_rss_native_units']} for tag,r in runs.items()},
         'controls':comparisons,'parity_relative':parity,'parity_gate':max(parity.values())<=.01,
         'conditional_sextans_quadrupole_lambda_removed_max':2*qold/math.sqrt(C),
         'scope':'No converged physical radiation efficiency or four-dwarf closure inferred; original frozen failures retained'}
# Separate Newtonian compact-launch diagnostic, not a universal wave theorem.
# alpha is the nonrotating Gaussian equilibrium binding coefficient in GMc^2/Rc.
alpha=1/(2*math.sqrt(2*math.pi))
summary['compact_ballistic_diagnostic']={'alpha':alpha,'assumptions':
    'Bound initial cloud, final supported nonrotating Gaussian core, no external energy, '
    'positive escaping test-mass envelope launched at Rc in -GMc/r; advective/WKB limit only',
    'lambda_max_at_old_receiver_q':math.sqrt(2*qold*(alpha+qold)),
    'mass_floor_rows':[{'lambda_removed':lam,'q_min':(math.sqrt(alpha**2+2*lam**2)-alpha)/2}
                       for lam in [.01,.03,.1,.3]]}
(b/'transport_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'parity_gate':summary['parity_gate'],'control_agreement':
    {tag:all(v['gate'] for v in d.values()) for tag,d in comparisons.items()},
    'quad_lambda_max':summary['conditional_sextans_quadrupole_lambda_removed_max'],
    'runs':{tag:{'mass_export':r['export_mass_fraction'],'spin_export':r['export_spin_fraction'],
                 'contraction':r['contraction'],'J_residual':r['spin_ledger_relative']} for tag,r in runs.items()}},indent=2))
