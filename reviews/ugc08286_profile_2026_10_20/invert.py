"""Deterministic finite axisymmetric source/stellar-gradient feasibility."""
import argparse
import json
import os
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from numpy.polynomial.legendre import leggauss
from kernel.disk_kernel import build_annular_kernel, G_KPC_KMS2_MSUN as G

ap=argparse.ArgumentParser()
ap.add_argument('--output-dir',required=True)
args=ap.parse_args()
out=Path(args.output_dir)
packet=Path(__file__).resolve().parent
repo=packet.parents[1]
d=np.loadtxt(packet/'data/UGC08286_rotmod.dat')
r,v,ev,vg,vd,vb,sb=d[:,:7].T
assert len(r)==17 and np.all(vb==0) and np.all(sb>0)
gas=np.sign(vg)*vg**2
foot=json.loads((repo/'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
a0s={'canonical':foot['a0_canonical'],'alt':foot['a0_rho_total']}
stellar=json.loads((packet/'stellar/observed_constraints.json').read_text())
caps=[float(x['upper']) for x in stellar['conditional_ML_envelopes_not_observed_bounds']]
h=0.196*1.05**0.633
rhi=8.07
light_cut=float(np.loadtxt(packet/'data/UGC08286.dens')[-1,0])
beam=6.5e3*30*np.pi/(180*3600)
kpc_m=3.0857e19
model_arrays={}

def edges(cut,step):
    return np.r_[np.arange(0,cut,step),cut]

def law_v2(b,a0,R=r):
    assert np.all(b>0)
    return (b+np.sqrt(b*b+4*a0*R*kpc_m/1e6*b))/2

def inverse_law_v2(w,a0,R):
    return w*w/(w+a0*R*kpc_m/1e6)

def interval_v2(nsig,idx):
    return np.maximum(v[idx]-nsig*ev[idx],0)**2,(v[idx]+nsig*ev[idx])**2

def pack_lp(ans,A,b,c):
    result=dict(success=bool(ans.success),status=int(ans.status),message=ans.message)
    if ans.success:
        y=np.asarray(ans.ineqlin.marginals)
        result.update(objective=float(c@ans.x),x=ans.x.tolist(),
            max_primal_violation=float(max(np.max(A@ans.x-b),-np.min(ans.x),0)),
            max_dual_violation=float(max(np.max(y),np.max(A.T@y-c),0)),
            dual_objective=float(b@y),dual_marginals=y.tolist(),
            duality_gap=float(c@ans.x-b@y))
    return result

def extra_lp(A,lo,hi,maximize=False):
    # Annular source variables are 1e9 Msun. No regularization or profile law.
    Ab=np.r_[A,-A]*1e9
    bb=np.r_[hi,-lo]
    c=np.ones(A.shape[1])*(-1 if maximize else 1)
    ans=linprog(c,A_ub=Ab,b_ub=bb,bounds=(0,None),method='highs')
    q=pack_lp(ans,Ab,bb,c)
    if ans.success:
        m=ans.x*1e9
        q.update(total_mass_msun=float(m.sum()),masses_msun=m.tolist(),
                 predicted_extra_v2=(A@m).tolist())
    return q

def ceiling_lp(B,lo,hi):
    n=B.shape[1]
    A=np.r_[np.c_[B,np.zeros(len(lo))],np.c_[-B,np.zeros(len(lo))],
             np.c_[np.eye(n),-np.ones(n)]]
    bb=np.r_[hi,-lo,np.zeros(n)]
    c=np.r_[np.zeros(n),1.0]
    ans=linprog(c,A_ub=A,b_ub=bb,bounds=(0,None),method='highs')
    q=pack_lp(ans,A,bb,c)
    if ans.success:
        q.update(required_pointwise_ceiling=float(ans.x[-1]),
                 Upsilon=ans.x[:-1].tolist(),
                 predicted_stellar_v2=(B@ans.x[:-1]).tolist())
    return q

def light_profile(R,kind):
    if kind=='loglinear':
        f=np.interp(R,r,np.log(sb))
        left=R<r[0];right=R>r[-1]
        f[left]=np.log(sb[0])+(R[left]-r[0])*np.log(sb[1]/sb[0])/(r[1]-r[0])
        f[right]=np.log(sb[-1])+(R[right]-r[-1])*np.log(sb[-1]/sb[-2])/(r[-1]-r[-2])
        return np.exp(f)
    f=np.interp(R,r,sb)
    left=R<r[0];right=R>r[-1]
    f[left]=sb[0]+(R[left]-r[0])*(sb[1]-sb[0])/(r[1]-r[0])
    f[right]=sb[-1]*np.exp((R[right]-r[-1])*np.log(sb[-1]/sb[-2])/(r[-1]-r[-2]))
    return np.maximum(f,0)

def light_masses(e,kind):
    x,w=leggauss(20)
    R=(e[1:]+e[:-1])[:,None]/2+(e[1:]-e[:-1])[:,None]*x/2
    return 2*np.pi*1e6*(e[1:]-e[:-1])/2*np.sum(w*R*light_profile(R,kind),axis=1)

extra_results=[]
for support in (rhi,2*rhi):
    for step in (beam,beam/2,beam/4):
        e=edges(support,step)
        for hf in (0.5,1.0,2.0):
            A=build_annular_kernel(r,e,h*hf,order=192)
            A96=build_annular_kernel(r,e,h*hf,order=96)
            key=f'extra_s{support:.2f}_step{step:.5f}_h{hf}'
            model_arrays[key]=A;model_arrays[key+'_edges']=e
            for footing,a0 in a0s.items():
                baseline=law_v2(gas+0.5*vd**2,a0)
                for nsig in (0,1,2):
                    vlo,vhi=interval_v2(nsig,np.arange(len(r)))
                    q=extra_lp(A,vlo-baseline,vhi-baseline)
                    if q['success']:
                        m=np.array(q['masses_msun'])
                        q['quadrature_delta_v2_bound']=float(np.max(np.abs(A-A96)@m))
                    q.update(footing=footing,nsigma=nsig,support_kpc=support,
                             step_kpc=step,height_kpc=h*hf,model_key=key)
                    extra_results.append(q)

stellar_results=[]
light_models=[]
distance_controls={'nominal':1.0,'D_minus_quoted_error':1-0.21/6.5,
                   'D_plus_quoted_error':1+0.21/6.5,'CF4_ratio_diagnostic':0.9100948218084219}
samples={'all17':np.arange(17),'alternate_even':np.arange(0,17,2),
         'alternate_odd':np.arange(1,17,2)}
for kind in ('loglinear','linear'):
    for step in (beam/2,beam/4,beam/8):
        # Include photometric sample knots to keep all interpolation changes
        # within integration cells. No observed-rotation residual enters here.
        e=np.unique(np.r_[edges(light_cut,step),r])
        e=e[(e>=0)&(e<=light_cut)]
        L=light_masses(e,kind)
        A=build_annular_kernel(r,e,h,order=192)
        B=A*L[None,:]
        key=f'light_{kind}_step{step:.5f}'
        model_arrays[key]=B;model_arrays[key+'_edges']=e;model_arrays[key+'_L']=L
        pub=vd**2
        model_v=np.sqrt(np.maximum(B.sum(1),0))
        light_models.append(dict(model_key=key,kind=kind,step_kpc=step,
            luminosity_Lsun=float(L.sum()),published_total_Lsun=1.255e9,
            total_luminosity_fraction=float(L.sum()/1.255e9),
            reconstructed_unit_vdisk=model_v.tolist(),
            max_abs_template_delta_v=float(np.max(np.abs(model_v-vd))),
            rms_template_delta_v=float(np.sqrt(np.mean((model_v-vd)**2))),
            max_fractional_vdisk_error=float(np.max(np.abs(model_v/vd-1))),
            source_profile_assumption='17 corrected light samples; fixed specified interpolation/central and outer extrapolation; full65 projected profile NOT deprojected or renormalized'))
        for footing,a0 in a0s.items():
            for distance,df in distance_controls.items():
                for sampling,idx in samples.items():
                    for nsig in (0,1,2):
                        vlo,vhi=interval_v2(nsig,idx)
                        lo=inverse_law_v2(vlo,a0,r[idx]*df)-gas[idx]*df
                        hi=inverse_law_v2(vhi,a0,r[idx]*df)-gas[idx]*df
                        q=ceiling_lp(B[idx]*df,lo,hi)
                        q.update(footing=footing,nsigma=nsig,distance_control=distance,
                                 distance_factor=df,sampling=sampling,model_key=key,
                                 calibration_caps=caps,
                                 cap_feasible=[bool(q['success'] and q['required_pointwise_ceiling']<=cap+1e-8) for cap in caps])
                        stellar_results.append(q)

# Explicit maximum-mass witness/range in the fixed primary geometry, not a
# statement that inverse profiles are unique or smooth.
fid=[x for x in extra_results if x['footing']=='canonical' and x['nsigma']==1 and
     x['support_kpc']==rhi and abs(x['step_kpc']-beam/2)<1e-9 and abs(x['height_kpc']-h)<1e-9][0]
Af=model_arrays[fid['model_key']]
base=law_v2(gas+0.5*vd**2,a0s['canonical'])
vlo,vhi=interval_v2(1,np.arange(17))
massmax=extra_lp(Af,vlo-base,vhi-base,True)

summary=dict(
    extra_cases=len(extra_results),extra_feasible=sum(q['success'] for q in extra_results),
    fixed_geometry_1sigma_minimum_mass_msun=fid.get('total_mass_msun'),
    fixed_geometry_1sigma_maximum_mass_msun=massmax.get('total_mass_msun'),
    stellar_ceiling_cases=len(stellar_results),
    nominal_all17_ceiling_ranges={footing:{str(nsig):[
        min(q['required_pointwise_ceiling'] for q in stellar_results if q['success'] and q['footing']==footing and q['nsigma']==nsig and q['distance_control']=='nominal' and q['sampling']=='all17'),
        max(q['required_pointwise_ceiling'] for q in stellar_results if q['success'] and q['footing']==footing and q['nsigma']==nsig and q['distance_control']=='nominal' and q['sampling']=='all17')]
        for nsig in (0,1,2)} for footing in a0s})
result=dict(assertion_tested='Finite disk source feasibility and minimal required annular stellar M/L ceiling using the same nonlocal kernel, fixed law and independent population calibration sensitivity boxes.',
    summary=summary,extra_results=extra_results,stellar_results=stellar_results,
    light_models=light_models,fiducial_extra=fid,fiducial_maximum=massmax,
    geometry=dict(vertical='exponential',height_kpc=h,HI_radius_kpc=rhi,
                  beam_kpc=beam,light_support_cut_kpc=light_cut),
    r_kpc=r.tolist(),v_obs=v.tolist(),v_error=ev.tolist(),baseline_v2=base.tolist(),
    calibration_caveat='Calibrated old-star dust-corrected M/L boxes are NOT recovered intrinsic radial data bounds. Applying an effective [0,Ucap] ceiling to the total SPARC light is conditional on extinction, projection, IMF and contamination ordering.',
    covariance_caveat='No observed covariance. Velocity-error boxes and odd/even subsamples are feasibility controls, not significance or joint confidence.',
    deprojection_caveat='Full corrected radial photometric profile unavailable; both declared17point reconstructions are checked against published unit disk velocities and never renormalized.',
    new_fitted_physical_parameters=0,empirical_mass_detection=False,memory_lifetime_derived=False)
out.mkdir(exist_ok=True,parents=True)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
np.savez_compressed(out/'matrices.npz',**model_arrays)
np.savetxt(out/'residual.csv',np.c_[r,v,ev,np.sqrt(base),v*v-base],delimiter=',',
           header='R_kpc,Vobs_kms,eV_kms,Vbaseline_kms,residual_V2_kms2',comments='')
os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
ax[0].errorbar(r,v,yerr=ev,fmt='o',ms=4,color='#222222',label='HI rotation data')
ax[0].plot(r,np.sqrt(base),color='#3e73ab',label='Fixed law + published stellar disk')
if fid['success']:
    ax[0].plot(r,np.sqrt(base+np.array(fid['predicted_extra_v2'])),color='#bd5c3c',label='One positive finite disk witness')
ax[0].set(xlabel='Radius [kpc]',ylabel='Circular speed [km/s]')
ax[0].legend(fontsize=8,frameon=False)
for kind,color in [('loglinear','#3e73ab'),('linear','#b36b34')]:
    qs=[q for q in stellar_results if q['success'] and q['footing']=='canonical' and
        q['nsigma']==1 and q['distance_control']=='nominal' and q['sampling']=='all17' and kind in q['model_key']]
    q=qs[-1];e=model_arrays[q['model_key']+'_edges']
    ax[1].stairs(q['Upsilon'],e,color=color,label=f'Required ceiling witness ({kind})')
ax[1].axhline(caps[-1],ls='--',color='#777777',label='Conditional old-star +0.2 dex ceiling')
ax[1].set(xlim=(0,light_cut),xlabel='Radius [kpc]',ylabel='Stellar M/L at 3.6 microns')
ax[1].legend(fontsize=8,frameon=False)
fig.suptitle('UGC08286: conditional disk inversion, not a unique density or detection',fontsize=11)
fig.savefig(out/'profile.png',dpi=170)
plt.close(fig)
print(json.dumps(summary,indent=2))
