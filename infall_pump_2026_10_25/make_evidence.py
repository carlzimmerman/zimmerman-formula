import argparse,json,os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/zimmerman-infall-mpl')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from live_collocated import Collocated
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output);base=Path('infall_pump_2026_10_25');m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
load=lambda name:json.loads((base/name/'results.json').read_text())
d=load('run_smooth_infall');assessment=load('run_smooth_assessment');tr=d['trace'];t=np.array([z['time_Myr'] for z in tr]);green='#087f5b';orange='#d97706';blue='#2563eb';gray='#64748b'
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':11,'figure.facecolor':'white'})
fig,ax=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
for key,label,color,style in [('bulk_current_work','Compression work',green,'-'),('conversion_work','Conversion work',orange,'-'),('wave_energy','All scalar field energy',blue,'--'),('far_net_flux','Net crossing 500 kpc',gray,':')]:ax[0,0].plot(t,[z[key]*1e3 for z in tr],label=label,color=color,ls=style,lw=1.8)
ax[0,0].set(title='Unseeded infall: work mostly remains in the field',xlabel='Time (Myr)',ylabel=r'Energy ($10^{-3}E_{\rm unit}$)');ax[0,0].axhline(0,color='#cbd5e1',lw=.7);ax[0,0].legend(fontsize=8,loc='upper left');ax[0,0].text(.98,.08,'Gravity energy decreases;\ndensity-gradient energy increases.',ha='right',va='bottom',transform=ax[0,0].transAxes,fontsize=9)
names=['run_components_time','run_conversion_only_time','run_quiet_time'];vals=[load(z)['trace'][-1]['far_net_flux'] for z in names];ax[0,1].bar(np.arange(3),vals,color=[orange,gray,green],width=.65);ax[0,1].set_yscale('log');ax[0,1].set_ylim(1e-11,8e-5);ax[0,1].set_xticks(np.arange(4));ax[0,1].set_xticklabels(['Initial internal\nmismatch','No transport\n(control)','Internally quiet\ninfall','Quiet + support\n(control)'],fontsize=8);ax[0,1].text(3,1.5e-11,'0 within\ntolerance',ha='center',fontsize=8);ax[0,1].set(title='Initial conversion relaxation was a false pump signal',ylabel='Net 500 kpc energy at 2 Myr (Eunit)')
s=np.load(base/'run_smooth_infall/state.npz');tf=d['completed_time_Myr'];upper=m.c*m.rm/m.tdyn*tf+500;mask=(m.wr*m.rm>=500)&(m.wr*m.rm<=upper);r=m.wr[mask];u=r*s['chi'][mask];ut=r*s['pi'][mask];h=np.mean(np.diff(r));out=(ut[1:]+ut[:-1])/2-m.c*np.diff(u)/h;rm=(r[1:]+r[:-1])/2;retarded=tf-rm/m.c*m.tdyn;power=.25*m.c/m.tdyn*out*out
ax[1,0].plot(retarded[::-1],power[::-1]*1e6,color=green,lw=2);ax[1,0].fill_between(retarded[::-1],power[::-1]*1e6,alpha=.15,color=green);ax[1,0].set(title='A real outgoing pulse survives the smooth quiet test',xlabel=r'Retarded time $t-r/c$ (Myr)',ylabel=r'Outgoing energy density ($10^{-6}E_{\rm unit}$/Myr)');ax[1,0].text(.98,.93,f"Outgoing energy: {assessment['radiative_decomposition']['outgoing_characteristic_energy']:.3g} Eunit\n{100*assessment['outgoing_energy_over_field_work']:.3f}% of transferred field energy\nFinite packet, not a sustained cascade",ha='right',va='top',transform=ax[1,0].transAxes,fontsize=9)
law=(m.gb+np.sqrt(m.gb*m.gb+4*m.gb))/2;rr=m.r*m.rm
for path,label,color,style in [(base/'run_smooth_prepare/state.npz','Initial displaced density',gray,':'),(base/'run_smooth_infall/state.npz','After 5.7 Myr',green,'-'),(base/'run_static_polish/state.npz','Known restoring equilibrium',blue,'--')]:
 a=np.load(path)['a'];gt=m.gb+m.enclosed(np.sum(abs(a)**2,axis=0));sel=(rr>=1.5)&(rr<=50);ax[1,1].plot(rr[sel],100*(law[sel]/gt[sel]-1),label=label,color=color,ls=style,lw=1.8)
ax[1,1].axhline(0,color='#cbd5e1',lw=.7);ax[1,1].set(title='The galaxy law still has not formed',xlabel='Radius (kpc)',ylabel='Target / actual acceleration − 1 (%)');ax[1,1].legend(fontsize=8,loc='upper left');fig.suptitle('Infall pump audit: genuine radiation, unresolved galaxy formation',fontsize=15)
fig.supxlabel('Same physical action; free density and boundary; no supplied fast-mode population. Filled transition and predominantly F exterior at 5.7 Myr.',fontsize=9)
fig.savefig(dest.with_name('evidence.png'),dpi=180);fig.savefig(dest.with_name('evidence.pdf'));plt.close(fig)
out={'figure':'evidence.png','goal_achieved':False,'physical_time_Myr':tf,'outgoing_pulse_energy_Eunit':assessment['radiative_decomposition']['outgoing_characteristic_energy'],'field_work_Eunit':tr[-1]['net_material_to_wave_work'],'law_error_percent':tr[-1]['law_error_percent'],'density_rebound':tr[-1]['density_rebound'],'outer_T_fraction':tr[-1]['outer_T_fraction'],'restoring_scope':'Positive inherited active equilibrium stiffness; live nonlinear trajectory restoration not established.','cascade_scope':'Pulse is real; no sustained noncollinear cascade established.'};dest.write_text(json.dumps(out,indent=2)+'\n');print(out)
