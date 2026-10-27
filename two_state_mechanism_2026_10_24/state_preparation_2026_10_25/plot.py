import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from prepare import response
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
root=Path(__file__).resolve().parent
prep=json.loads((root/'run_prepare/results.json').read_text())
ref=json.loads((root/'run_refine/results.json').read_text())
bounds=json.loads((root/'run_combined_v2/results.json').read_text())
plt.rcParams.update({'font.size':10,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(2,2,figsize=(12,8.5),layout='constrained')
a0=ax[0,0]
rows=[r for r in prep['runs'] if r['T']==1000 and r['initial_temperature']==.1]
a0.bar(['Linear gap removal','Slow near closure'],[100*r['source_relative_error'] for r in rows],color=['#ba6e3e','#277c8e'],width=.6)
a0.axhline(100*rows[0]['eigenvalue_lower_bound_error'],color='#555',ls=':',label='Occupation floor (0.364%)')
a0.set_yscale('log');a0.set_ylim(.1,100);a0.set_ylabel('Diagonal source-remainder error (%)')
a0.set_title('A  |  Controlled preparation from a thermal gapped band')
a0.text(.03,.96,'T initial = 0.1; initial gap parameter = 1\nFinal field = 0.01; duration = 1000',transform=a0.transAxes,va='top',fontsize=9)
a0.legend(loc='upper right',bbox_to_anchor=(1,.82),fontsize=8)
a1=ax[0,1];r=ref['autonomous'][-1]
a1.plot(r['trace']['t'],r['trace']['mass'],color='#754e98',lw=1.4)
a1.axhline(0,color='#555',ls=':',label='Required nodal value')
a1.set_xlabel('Time (hbar / Lambda)');a1.set_ylabel('Collective gap coordinate m')
a1.set_title('B  |  Autonomous field + coordinate keeps oscillating')
a1.text(.03,.05,'I = 100; 256 modes\nRelative energy drift < 2e-11',transform=a1.transAxes,fontsize=9)
a2=ax[1,0];x=np.logspace(-4,4,1001)
best=prep['interactions']['grid_best'];base=prep['interactions']['fits'][0]
for lam,chi,label,color in [(0,base['chi_effective'],'Bare band, fitted susceptibility','#ba6e3e'),(best['coupling'],best['chi_effective'],'Contact interaction + susceptibility fitted','#277c8e')]:
 err,_=response(lam,chi,x);a2.semilogx(x,err,color=color,label=label)
a2.axhline(0,color='#555',ls=':',lw=.8);a2.set_xlabel('g / a0');a2.set_ylabel('Acceleration residual (dex)')
a2.set_title('C  |  Static fit improves; constants are not derived')
a2.legend(fontsize=8,loc='upper right');a2.set_ylim(-.042,.042)
a3=ax[1,1]
rs=[r for r in bounds['rows'] if r['model']=='bare' and r['epsilon']==.1]
xx=np.arange(4);a3.semilogy(xx,[r['fermi_mass_lower_eV'] for r in rs],'o-',color='#9f3737',label='Fermi packing: mass must be ABOVE')
a3.semilogy(xx,[r['current_mass_upper_eV'] for r in rs],'s-',color='#277c8e',label='Local current: mass must be BELOW')
a3.set_xticks(xx,['Small dwarf','Large dwarf','Disk','Cluster']);a3.set_ylabel('Constituent mass (eV/c²)');a3.set_ylim(1e-22,10)
a3.set_title('D  |  No overlap for local fundamental fermionic units')
a3.legend(fontsize=8,loc='center');a3.grid(axis='y',alpha=.2)
fig.suptitle('Preparation and microscopic consistency: distinct tests, no galaxy mechanism yet',fontsize=14)
fig.savefig(a.output,dpi=160)
