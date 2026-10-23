import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
r=json.loads((P/'thermal_recycling_evolution_run/results.json').read_text());a=np.genfromtxt(P/'thermal_recycling_dense_run/full.csv',delimiter=',',names=True)
pair=float(np.trapz(a['pair_net_over_H']*a['Yweighted'],a['N']));direct=float(np.trapz(a['quartic_net_over_H']*a['Yweighted'],a['N']));loss=float(a['Yweighted'][0]-a['Yweighted'][-1])
anchors=[]
for i in [0,1,3]:
 rr=json.loads((P/f'thermal_recycling_anchor{i}_run/results.json').read_text());anchors.append({'A_GeV':rr['anchor']['A_GeV'],'Y':rr['cases']['full']['Y_final'],'target_fraction':rr['cases']['full']['target_fraction']})
anchors.append({'A_GeV':.001,'Y':r['cases']['full']['Y_final'],'target_fraction':r['cases']['full']['target_fraction']});anchors.sort(key=lambda x:x['A_GeV'],reverse=True)
# Load model definitions only to calculate independent initial linear-response scales.
ns={'__file__':str(P/'thermal_recycling_evolution.py'),'__name__':'assessment_library'}
exec(compile((P/'thermal_recycling_evolution.py').read_text().split('\ncases={}')[0],'model','exec'),ns)
T=ns['Ts'];eta=ns['etas'];m=ns['m'];n,nx,W,U,pr,J=ns['state'](T,eta);rhoJ=J[1]+m*J[0];rt=rhoJ[1]/rhoJ[0];chi=(J[0,1]-J[0,0]*rt)/(1+m/T*rt);C,sv=ns['rate'](T)
relax=2*(.5*sv*nx*nx+C*n**4)/(chi*ns['Hs'])
source=json.loads((P/'highH_annihilation_gate_run/results.json').read_text())['counterfactual_reservoir_anchors'][2]
weighted_source=2*source['entropy_mappings'][0]['YX_initial']
checks={'integrated_number_loss':abs((pair+direct)/loss-1)<1e-4,'chemical_relaxation_fast_at_start':relax>100,'positive_channel_losses':pair>0 and direct>0}
summary={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':bool(all(checks.values())),'integrated_pair_loss_Y':pair,'integrated_direct_contact_loss_Y':direct,'pair_fraction_of_integrated_loss':pair/(pair+direct),'integrated_loss_relative_error':(pair+direct)/loss-1,'initial_chemical_relaxation_over_H':relax,'final_over_counterfactual_source_weighted_number':r['cases']['full']['Y_final']/weighted_source,'anchor_sensitivity':anchors,'scope':'All yields conditional on thermal matching of a surviving free X reservoir at the chosen anchor. The spread is not a rigorous uncertainty interval or a family of derived cosmological histories.'}
(O/'results.json').write_text(json.dumps(summary,indent=2))
fig,axs=plt.subplots(1,3,figsize=(14,4.3),constrained_layout=True)
for name,label in [('full','Pair recycling + direct 4↔2'),('no_pair','Direct 4↔2 only'),('no_loss','Number conserved')]:
 b=np.genfromtxt(P/'thermal_recycling_evolution_run'/(name+'.csv'),delimiter=',',names=True);axs[0].plot(np.exp(b['N']),b['Yweighted'],label=label)
axs[0].set_xscale('log');axs[0].set_xlabel('Expansion since kinetic start');axs[0].set_ylabel('Weighted number / visible entropy');axs[0].legend(fontsize=8)
axs[1].loglog(np.exp(a['N']),a['T']/.001,label='Evolving bath');axs[1].loglog(np.exp(a['N']),.5*np.exp(-2*a['N']),'--',label='T proportional to a⁻²');axs[1].set_xlabel('Expansion since kinetic start');axs[1].set_ylabel('Dark temperature / m');axs[1].legend(fontsize=8)
axs[2].plot([x['A_GeV'] for x in anchors],[x['target_fraction'] for x in anchors],'o-');axs[2].set_xscale('log');axs[2].set_xlabel('Assumed thermalization anchor |X| (GeV)');axs[2].set_ylabel('Final yield / target');axs[2].set_ylim(0,.32)
for ax in axs:ax.grid(alpha=.2)
fig.suptitle('Conditional thermal branch — source-to-bath matching is not derived',fontsize=13)
fig.savefig(O/'thermal_recycling.png',dpi=180)
print(json.dumps(summary,indent=2));sys.exit(0 if summary['all_pass'] else 1)
