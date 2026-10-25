import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
BASE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();d=json.loads((BASE/'run_audit/results.json').read_text())
 rows=d['refinement']['order6'][:2]+d['refinement']['order9_disk_cluster'];f=np.array([s['molecular_mass_fraction'] for s in rows])
 fig,ax=plt.subplots(figsize=(9,5.6));ax.bar(np.arange(4),f,color=['#64748b','#64748b','#0369a1','#b45309'],width=.58)
 ax.set_yscale('log');ax.set_ylim(1e-8,1.8);ax.set_xticks(np.arange(4),['Small dwarf\nproxy','Large dwarf\nproxy','Disk\nproxy','Cluster\nproxy'])
 ax.set_ylabel('Charged molecular mass fraction');ax.axhline(.8,color='#0369a1',ls='--',lw=1);ax.text(3.47,.85,'80% disk target',ha='right',fontsize=9,color='#0369a1')
 ax.axhline(.2,color='#78716c',ls=':',lw=1);ax.text(-.3,.24,'20% ceiling for other profiles',ha='left',fontsize=9,color='#78716c')
 for i,z in enumerate(f):ax.text(i,z/1.4 if i==3 else z*1.4,f'{z*100:.5g}%',ha='center',va='top' if i==3 else 'bottom',color='white' if i==3 else 'black',fontsize=11,fontweight='bold')
 ax.set_title('Photon recycling does not produce the requested separation',loc='left',pad=18,fontsize=13)
 ax.grid(axis='y',which='major',alpha=.18);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
 fig.text(.12,.025,'Common alpha = 0.2; light mass = 10 MeV; mass ratio = 100; elapsed time = 10 Gyr.\nHomogeneous radiative model; finite nonradiative collision rates remain unresolved.',fontsize=9,color='#475569')
 fig.tight_layout(rect=(0,.11,1,1));path=Path(a.output).parent/'fractions.png';fig.savefig(path,dpi=170)
 Path(a.output).write_text(json.dumps(dict(fractions=f.tolist(),figure=str(path)),indent=2)+'\n')
if __name__=='__main__':main()
