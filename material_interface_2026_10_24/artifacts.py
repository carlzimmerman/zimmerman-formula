import json,argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from carrier_checked import Carrier
from joint import outer,law

def diagnostics(r):
 rad=np.array(r['r']);mass=np.array(r['mass']);q=np.array(r['q']);gt=np.array(r['g_total']);gl=np.array(r['g_law']);err=np.log10(gt/gl);R=r['interpolated_crossings_kpc'][-1];out=rad>1.2*R;inside=(rad>15)&(rad<R)
 windows={}
 for upper in [15,30,50]:
  e=np.r_[np.interp(1.5,rad,err),err[(rad>=1.5)&(rad<=upper)],np.interp(upper,rad,err)]
  windows[str(upper)]=dict(max_abs_dex=float(max(abs(e))),max_abs_fraction=float(max(abs(10**e-1))))
 return dict(n=r['n'],R_kpc=R,all_phase_crossings_kpc=r['interpolated_crossings_kpc'],energy=r['energy'],law_with_interpolated_endpoints=windows,qinner=r['qinner'],historical_qouter_beyond_44kpc=r['qouter'],exterior_definition='r>1.2 R_boundary',exterior_mass_Mb=float(sum(mass[out])),exterior_T_fraction=float(mass[out]@q[out]/sum(mass[out])),total_T_mass_Mb=float(mass@q),total_F_mass_Mb=float(mass@(1-q)),empty_cells_15kpc_to_boundary=int(sum(mass[inside]<1e-8)),minimum_cell_mass_15kpc_to_boundary=float(min(mass[inside])),density_KKT_max=r['density_KKT_max'],phase_softmax_gradient_max=r['gradient_max'],edge_mass_fraction=r['edge_mass_fraction'],cap_slack=r['cap_slack_min'])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);p=Path(__file__).parent
 recovery=json.loads((p/'run_final_recovery/results.json').read_text());bases=[r for r in recovery['runs'] if r['stage']=='base'];current=bases[-1];stiff=json.loads((p/'run_stiffness/results.json').read_text());checks=json.loads((p/'run_final_checks/results.json').read_text());old=json.loads(Path('live_density_interface_2026_10_24/run_stable_recovery/results.json').read_text())['refinement'][0]
 out={'status':'Finite spherical candidate for populated restoring boundary; original law only approximate, full research goal remains open.','parameters':dict(beta=.5,K=15,ell_kpc=10,charge=0,total_mass_Mb=5.364),'grids':[diagnostics(r) for r in bases],'domain_and_seeds':[dict(stage=r['stage'],initialization=r['initialization'],diagnostics=diagnostics(r)) for r in checks['runs']],'restoration':[dict(n=r['n'],displacement_kpc=r['displacement_kpc'],front_change_kpc=r['front_change_kpc'],initial_energy_difference=r['initial_energy_difference'],energy_difference=r['energy_difference']) for r in recovery['runs'] if r['stage']=='recovery'],'stiffness':stiff,'limitations':['No exact galaxy-law preservation through transition; error at exactly50kpc includes interpolated endpoint and is slightly above .05dex.','Historical fixed r>=44kpc outer-fraction gate fails because it includes the populated transition; explicit exterior diagnostics do not retroactively pass that gate.','Energetic minimization from seeds is not physical material transport or a timescale.','Single prescribed spherical baryon profile; no new observational fit, nonspherical stability test, universal galaxy ensemble or microscopic derivation of parameters.']}
 dest.write_text(json.dumps(out,indent=2)+'\n')
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False});fig,ax=plt.subplots(2,2,figsize=(11,8));colors=['#7a8393','#137e8a']
 for rr,label,c in [(old,'Previous depleted state',colors[0]),(current,'Coupled pressure-supported state',colors[1])]:
  rad=np.array(rr['r']);mass=np.array(rr['mass']);q=np.array(rr['q']);edges=[0.]
  for radius in rad:edges.append(2*radius-edges[-1])
  model=Carrier(n=rr['n'],domain=12,beta=.5,K=15);vol=np.diff((np.array(edges)/model.rm)**3)/3;rho=mass/vol
  ax[0,0].plot(rad,np.maximum(rho,1e-10),color=c,label=label);ax[0,1].plot(rad,np.array(rr['g_total'])/rr['g_law'],color=c,label=label);ax[1,0].plot(rad,q,color=c,label=label)
 ax[0,0].set(xscale='log',yscale='log',xlim=(1.5,200),ylim=(1e-10,2),xlabel='Radius (kpc)',ylabel='Dimensionless material density',title='The depleted interval is populated');ax[0,0].legend(fontsize=8);ax[0,0].text(.03,.04,'Display floor: 10⁻¹⁰',transform=ax[0,0].transAxes,fontsize=8)
 ax[0,1].axhline(1,color='black',lw=.8);ax[0,1].axvline(50,color='black',ls=':',lw=.7);ax[0,1].set(xlim=(1.5,100),ylim=(.3,1.15),xlabel='Radius (kpc)',ylabel='Actual gravity / galaxy-law gravity',title='Inner law retained; transition deficit remains')
 R=current['interpolated_crossings_kpc'][-1];ax[1,0].axvline(R,color=colors[1],ls=':');ax[1,0].axvspan(1.2*R,200,color=colors[1],alpha=.08);ax[1,0].set(xlim=(1.5,160),ylim=(-.03,1.03),xlabel='Radius (kpc)',ylabel='Converted fraction q',title='Free exterior; no pinned outer phase')
 K=stiff['curvature'][-1]['relaxed_stiffness_Eunit_per_kpc2'];xx=np.linspace(-.25,.25,100);ax[1,1].plot(xx,-K*xx/1e-5,color=colors[1],label='Relaxed Hessian prediction');ax[1,1].scatter([r['displacement_kpc'] for r in stiff['finite']],[r['force_Eunit_per_kpc']/1e-5 for r in stiff['finite']],color='#b15f20',label='Constrained equilibrium force',zorder=3);ax[1,1].axhline(0,color='black',lw=.7);ax[1,1].axvline(0,color='black',lw=.7);ax[1,1].set(xlabel='Boundary displacement (kpc)',ylabel='Force (10⁻⁵ Eunit/kpc)',title='Restoring force with density relaxed');ax[1,1].legend(fontsize=8)
 fig.suptitle('A populated, restoring boundary — finite spherical calculation',fontsize=14);fig.tight_layout(rect=(0,0,1,.96));fig.savefig(dest.with_name('result.png'),dpi=180);plt.close(fig)
 print(json.dumps({'grids':out['grids'],'domain_and_seeds':out['domain_and_seeds']},indent=2))
