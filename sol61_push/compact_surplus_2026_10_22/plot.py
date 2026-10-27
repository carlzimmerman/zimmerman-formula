import ast,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
tree=ast.parse((p/'checks.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='interior'],type_ignores=[]),str(p/'checks.py'),'exec'))
r=json.loads((p/'dwarf_run2/result.json').read_text())['rows'][0];ins,_=interior(r['s_center'],0,0,1e-10)
rpc=np.geomspace(.3,3000,400);x=np.minimum(rpc,r['edge_pc'])/440.4221297174536;q=ins.sol(x)[0];z=q/x**2;y=(z+np.sqrt(z*z+4*z))/2;mass=x*x*y;mass*=r['mass_Msun']/mass[-1]
cluster=json.loads((p/'cluster_run/result.json').read_text());d=np.load('campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_percluster.npz');W=np.where(np.isfinite(d['E'])&(d['E']>0),1/d['E']**2,0);R=np.array(cluster['R_Mpc']);stack=lambda a:np.sum(W*a,axis=0)/W.sum(axis=0)
obs=stack(np.nan_to_num(d['D']));law=stack(d['PL']);pn=stack(d['PN']);M=cluster['rows'][2]['mass_median_Msun'];model=law+M/(np.pi*(R*1e6)**2)
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(11,4.6),layout='constrained')
ax[0].loglog(rpc,mass,color='#197c80',lw=2.5);ax[0].axvline(r['edge_pc'],color='grey',ls='--');ax[0].set(xlabel='Radius [pc]',ylabel='Enclosed cold mass [solar masses]',title='Fitted dwarf core: finite mass');ax[0].text(.06,.85,'Canonical: 1.10 × 10⁷ solar masses\nCold edge: 321 pc',transform=ax[0].transAxes,fontsize=10)
ax[1].loglog(R,obs,'o-',color='black',label='Cached cluster stack');ax[1].loglog(R,law,'--',color='#197c80',label='Existing law baseline');ax[1].loglog(R,model,'o-',color='#c45434',label='Law + centred compact core');ax[1].axvspan(.15*20**(3/8),.15*20**(6/8),alpha=.1,color='#c45434',label='MID calibration band');ax[1].set(xlabel='Projected radius [Mpc]',ylabel='DeltaSigma [solar masses / pc²]',title='Cluster core fitted on MID overshoots INNER');ax[1].legend(fontsize=8)
fig.suptitle('Compact surplus: dwarf compatibility survives; central cluster shape fails',fontsize=13)
fig.savefig(p/'compact_surplus.png',dpi=180);fig.savefig(p/'compact_surplus.pdf')
