"""Boundary/null-source and independent-global-mass controls after run001."""
import argparse,json,os
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from kernel.disk_kernel import build_annular_kernel,G_KPC_KMS2_MSUN as G

ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
p=Path(__file__).resolve().parent;out=Path(args.output_dir);out.mkdir(exist_ok=True,parents=True)
x=json.loads((p/'inversion_run/results.json').read_text())
mat=np.load(p/'inversion_run/matrices.npz')
qdata=np.loadtxt(p/'data/UGC08286_rotmod.dat')
r,v,ev,vg,vd=qdata[:,:5].T;gas=np.sign(vg)*vg**2
a0s={q['footing']:q['a0_si'] for q in json.loads((p/'baseline_run02/results.json').read_text())['footings'].values()} if False else None
foot=json.loads((p.parents[1]/'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
a0s={'canonical':foot['a0_canonical'],'alt':foot['a0_rho_total']}
h=x['geometry']['height_kpc'];beam=x['geometry']['beam_kpc'];kpc=3.0857e19
law=lambda b,a:(b+np.sqrt(b*b+4*a*r*kpc/1e6*b))/2
inv=lambda w,a:w*w/(w+a*r*kpc/1e6)

def mass_lp(A,lo,hi,sign=1):
    Ab=np.r_[A,-A]*1e9;bb=np.r_[hi,-lo];c=np.full(A.shape[1],sign,dtype=float)
    z=linprog(c,A_ub=Ab,b_ub=bb,bounds=(0,None),method='highs')
    q=dict(success=bool(z.success),status=int(z.status),message=z.message)
    if z.success:
        m=z.x*1e9;y=z.ineqlin.marginals
        q.update(total_mass_msun=float(m.sum()),masses_msun=m.tolist(),predicted_v2=(A@m).tolist(),
                 max_primal_violation=float(max(np.max(Ab@z.x-bb),-np.min(z.x),0)),
                 max_dual_violation=float(max(np.max(y),np.max(Ab.T@y-c),0)),
                 duality_gap=float(c@z.x-bb@y))
    return q

def null_mass(A):
    # Positive normalized source with zero force at all observed nodes.
    scaled=A/G
    z=linprog(np.zeros(A.shape[1]),A_eq=np.r_[scaled,np.ones((1,A.shape[1]))],
              b_eq=np.r_[np.zeros(len(r)),1],bounds=(0,None),method='highs')
    q=dict(success=bool(z.success),status=int(z.status))
    if z.success:
        q.update(fractions=z.x.tolist(),sum_fractions=float(z.x.sum()),
                 max_abs_scaled_node_force=float(np.max(np.abs(scaled@z.x))))
    return q

uniform=[];nulls=[]
fid=x['fiducial_extra'];Af=mat[fid['model_key']];ef=mat[fid['model_key']+'_edges']
nulls.append(dict(geometry='original arange terminal-cell grid',edges_kpc=ef.tolist(),**null_mass(Af)))
for support in (8.07,16.14):
    for targetstep in (beam,beam/2,beam/4):
        n=int(np.ceil(support/targetstep));e=np.linspace(0,support,n+1)
        A=build_annular_kernel(r,e,h,order=192)
        for footing,a0 in a0s.items():
            base=law(gas+.5*vd**2,a0)
            for nsig in (0,1,2):
                lo=np.maximum(v-nsig*ev,0)**2-base;hi=(v+nsig*ev)**2-base
                mi=mass_lp(A,lo,hi)
                ma=mass_lp(A,lo,hi,-1) if nsig==1 else None
                uniform.append(dict(support_kpc=support,annuli=n,step_kpc=float(e[1]),
                     footing=footing,nsigma=nsig,minimum=mi,maximum=ma,edges_kpc=e.tolist()))
        if support==8.07 and abs(targetstep-beam/2)<1e-9:
            nulls.append(dict(geometry='equal-width cells, same count',edges_kpc=e.tolist(),**null_mass(A)))

star=[]
nominal_global=10**8.75*(6.5/8.59)**2
for lm in x['light_models']:
    key=lm['model_key'];B=mat[key];L=mat[key+'_L'];n=B.shape[1]
    for footing,a0 in a0s.items():
        for nsig in (0,1,2):
            lo=inv(np.maximum(v-nsig*ev,0)**2,a0)-gas
            hi=inv((v+nsig*ev)**2,a0)-gas
            A=np.r_[B,-B];bb=np.r_[hi,-lo]
            z=linprog(L/1e9,A_ub=A,b_ub=bb,bounds=(0,None),method='highs')
            row=dict(model_key=key,footing=footing,nsigma=nsig,success=bool(z.success),
                     source_global_mass_msun=nominal_global,
                     global_mass_comparison_conditional=True)
            if z.success:
                y=z.ineqlin.marginals;c=L/1e9
                row.update(minimum_stellar_mass_msun=float(L@z.x),
                           ratio_to_nominal_aperture_mass=float(L@z.x/nominal_global),
                           Upsilon=z.x.tolist(),max_Upsilon=float(z.x.max()),
                           max_primal_violation=float(max(np.max(A@z.x-bb),-np.min(z.x),0)),
                           max_dual_violation=float(max(np.max(y),np.max(A.T@y-c),0)),
                           duality_gap=float(c@z.x-bb@y))
            # Is any no-upper-ceiling gradient compatible with the nominal
            # aperture mass if that were the whole-star budget? This is only
            # an explicit aperture/absolute-population sensitivity control.
            zz=linprog(np.zeros(n),A_ub=np.r_[A,L[None,:]/1e9],
                       b_ub=np.r_[bb,nominal_global/1e9],bounds=(0,None),method='highs')
            row['nominal_aperture_as_total_budget_feasible']=bool(zz.success)
            star.append(row)

summary=dict(equal_cell_cases=len(uniform),
    primary_1sigma_equal_cell_mass_ranges={footing:[
        min(z['minimum']['total_mass_msun'] for z in uniform if z['footing']==footing and z['nsigma']==1 and z['minimum']['success']),
        max(z['minimum']['total_mass_msun'] for z in uniform if z['footing']==footing and z['nsigma']==1 and z['minimum']['success'])]
        for footing in a0s},
    null_sources=[dict(geometry=z['geometry'],exists=z['success'],scaled_residual=z.get('max_abs_scaled_node_force')) for z in nulls],
    nominal_independent_aperture_stellar_mass_msun=nominal_global,
    minimum_stellar_mass_1sigma_ranges={footing:[
        min(z['minimum_stellar_mass_msun'] for z in star if z['footing']==footing and z['nsigma']==1 and z['success']),
        max(z['minimum_stellar_mass_msun'] for z in star if z['footing']==footing and z['nsigma']==1 and z['success'])]
        for footing in a0s})
res=dict(assertion_tested='Post-run boundary-grid and positive-null-source controls, plus minimal total stellar mass over all nonnegative annular gradients under the same disk/law geometry.',
         rationale='First run found unbounded maximum mass with a tiny terminal annulus. Equal-width grids and explicit normalized null rays distinguish genuine finite-node source nonidentifiability from a coding/solver failure.',
         summary=summary,equal_cell_results=uniform,null_sources=nulls,stellar_total_mass_controls=star,
         independent_global_mass_caveat='JPLUS nominal mass integrates a finite analysis footprint at mu_r~24mag/arcsec2; no object-specific global uncertainty or complete-aperture correction recovered. It is not a whole-galaxy hard upper bound.',
         main_quadrature_field_interpretation='Main run quadrature_delta_v2_bound is a 96-vs192 order discrepancy only, not a proved error bound; independent adaptive integration is in audit/.',
         new_fitted_physical_parameters=0)
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n')
os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl_cache'))
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,2,figsize=(10,4),layout='constrained')
ax[0].errorbar(r,v,yerr=ev,fmt='o',ms=4,color='#222',label='Published HI speeds')
base=np.array(x['baseline_v2']);ax[0].plot(r,np.sqrt(base),color='#4477aa',label='Fixed law, stellar M/L=0.5')
fq=next(z for z in uniform if z['footing']=='canonical' and z['nsigma']==1 and z['support_kpc']==8.07 and z['annuli']==int(np.ceil(8.07/(beam/2))))
if fq['minimum']['success']:
    ax[0].plot(r,np.sqrt(base+np.array(fq['minimum']['predicted_v2'])),color='#c65d38',label='One positive disk solution')
ax[0].set(xlabel='Radius [kpc]',ylabel='Circular speed [km/s]');ax[0].legend(fontsize=8,frameon=False)
for j,nsig in enumerate((1,2)):
    qs=[z['required_pointwise_ceiling'] for z in x['stellar_results'] if z['success'] and z['footing']=='canonical' and z['nsigma']==nsig and z['distance_control']=='nominal' and z['sampling']=='all17']
    lo,hi=min(qs),max(qs);mid=(lo+hi)/2
    ax[1].errorbar(j,mid,yerr=[[mid-lo],[hi-mid]],fmt='o',capsize=5,color='#c65d38',label='Required maximum M/L' if j==0 else None)
ax[1].axhline(.6*10**.2,color='#555',ls='--',label='Conditional +0.2 dex calibration ceiling')
ax[1].axhline(.6,color='#999',ls=':',label='Old-star calibration center')
ax[1].set(xticks=[0,1],xticklabels=['±1 quoted error box','±2 quoted error box'],xlim=(-.4,1.4),ylim=(.45,1.55),ylabel='Necessary stellar M/L ceiling, 3.6 microns')
ax[1].legend(fontsize=8,frameon=False)
fig.suptitle('UGC08286: disk feasibility; stellar limits remain conditional',fontsize=11)
fig.savefig(out/'summary.png',dpi=180);plt.close(fig)
print(json.dumps(summary,indent=2))
