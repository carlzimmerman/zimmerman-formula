"""Render explicitly synthetic inverse-problem illustrations from checked inputs."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output-dir',required=True);args=ap.parse_args()
checked=json.loads(Path(args.input).read_text());out=Path(args.output_dir);out.mkdir(exist_ok=True)
w0=checked['synthetic_CPL_parameters']['w0'];wa=checked['synthetic_CPL_parameters']['wa']
z=np.linspace(0,5,501);a=1/(1+z);w=w0+wa*(1-a)
er=a**(-3*(1+w0+wa))*np.exp(3*wa*(a-1))
ad=np.sqrt(er);apress=np.sqrt((w/w0)*er)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#243544','text.color':'#243544','axes.edgecolor':'#bbc5cc'})
fig,axs=plt.subplots(1,2,figsize=(12.2,4.9));fig.subplots_adjust(top=.72,bottom=.16,wspace=.26,left=.075,right=.98)
fig.text(.075,.95,'What the inverse relationships can—and cannot—identify',fontsize=18,weight='bold')
fig.text(.075,.885,'Exact model illustrations • chosen parameters • no observational fit',fontsize=11,color='#637180')
ax=axs[0];ax.plot(z,ad,color='#166e9b',lw=2.7,label='Scale tied to energy density')
ax.plot(z,apress,color='#d16a26',lw=2.7,label='Scale tied to negative pressure')
ax.axhline(1,color='#8b969e',ls='--',lw=1.3,label='Constant vacuum reference')
ax.set(title='Same evolving fluid, different scale predictions',xlabel='Redshift z',ylabel=r'$a_0(z) / a_0(0)$')
ax.legend(loc='lower left',frameon=False,fontsize=9);ax.grid(alpha=.16);ax.set_xlim(0,5)
ax=axs[1]
for d,color in [(0,'#166e9b'),(.1,'#2e8f79'),(.4,'#d16a26')]:
    ww=-1/(1+d*(1+z)**3)
    ax.plot(z,ww,color=color,lw=2.6,label=f'D / tension = {d:g} today')
ax.set(title='Same constant pressure and scale, different w',xlabel='Redshift z',ylabel=r'$w(z)=p/\epsilon$')
ax.set_ylim(-1.06,.04);ax.set_xlim(0,5);ax.legend(loc='lower right',frameon=False,fontsize=9);ax.grid(alpha=.16)
fig.savefig(out/'inverse_relationships.png',dpi=180,facecolor='white')
fig.savefig(out/'inverse_relationships.pdf',facecolor='white')
metadata={'source':args.input,'synthetic':True,'w0':w0,'wa':wa,'dust_to_tension_today':[0,.1,.4],'samples':len(z),'matplotlib':matplotlib.__version__}
(out/'plot_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata))
