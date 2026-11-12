import sys,pathlib,json,math
import numpy as np
from scipy.optimize import least_squares
from scipy.interpolate import PchipInterpolator
root=pathlib.Path(__file__).parent;out=root/sys.argv[1];out.mkdir(exist_ok=True)
cfg=json.loads((root/'route_redshift_injection_selection.json').read_text())
data=np.loadtxt(root/'route_redshift_sparc_inputs/NGC2403_rotmod.dat')
valid=(data[:,0]>0)&(data[:,1]>0)&(data[:,2]>0);data=data[valid];data=data[np.argsort(data[:,0])]
R,V,eV,Vg,Vd,Vbul,SB=data[:,:7].T
assert np.all(Vbul==0)
rows=len(R);hold=np.array(cfg['holdout_zero_based_sorted_indices']);train=np.setdiff1d(np.arange(rows),hold)
assert len(hold)==12 and len(np.unique(hold))==12 and max(hold)<rows
rd=1.39;inc0=np.deg2rad(cfg['truth_inclination_deg']);sigi=np.deg2rad(cfg['inclination_prior_sigma_deg']);sigg=cfg['profiled_gamma_prior_sigma_dimensionless']
for line in (root/'route_redshift_sparc_inputs/SPARC_Lelli2016c.mrt').read_text().splitlines():
 z=line.split()
 if z and z[0]=='NGC2403':assert float(z[11])==rd and float(z[5])==63 and float(z[6])==3
nr=cfg['ring_model']['radial_points'];np_=cfg['ring_model']['azimuthal_points'];rmax=2*max(R);rp=(np.arange(nr)+.5)*rmax/nr;dr=rmax/nr
rr=R[SB>0];ls=np.log(SB[SB>0]);slope=(ls[-1]-ls[-2])/(rr[-1]-rr[-2]);assert slope<0
lns=np.interp(rp,rr,ls,left=ls[0],right=ls[-1]);tail=rp>rr[-1];lns[tail]=ls[-1]+slope*(rp[tail]-rr[-1]);Sigma=np.exp(lns)
phi=(np.arange(np_)+.5)*2*np.pi/np_;co=np.cos(phi)[None,:];rpr=rp[:,None];h=.1*rd;weight=rp*Sigma*dr*2*np.pi/np_;L=np.log(rp/rd)
H=[]
for r in R:
 ker=(r-rpr*co)/(r*r+rpr*rpr-2*r*rpr*co+h*h)**1.5;H.append(ker.sum(axis=1)*weight)
H=np.array(H);g0=H@np.ones(nr);assert np.all(g0>0)
ggrid=np.linspace(-.4,.4,161);forces=(H@np.exp(L[:,None]*ggrid[None,:])).T/g0[None,:]
interp=PchipInterpolator(ggrid,forces,axis=0)
kpc=3.085677581491367e19;star=.5*Vd**2*1e6/(R*kpc);gas=np.sign(Vg)*Vg**2*1e6/(R*kpc);a00=cfg['fiducial_a0_m_s2']
def model(par,law,profiled,exact_gamma=False):
 if profiled:ls_,lg,lt,gamma,di=par
 else:ls_,lg,lt,di=par;gamma=0.
 response=(H@np.exp(gamma*L))/g0 if exact_gamma else interp(gamma)
 B=np.exp(ls_)*star*response+np.exp(lg)*gas;a=a00*np.exp(lt)
 if np.any(B<=0):return np.full(len(R),np.nan)
 g=(B+np.sqrt(B*B+4*a*B))/2 if law=='simple_mu' else np.sqrt(B*B+a*B)
 return np.sqrt(R*kpc*g)/1000*np.sin(inc0+di)/np.sin(inc0)
result=[];checks={};all_starts=[]
for law in cfg['laws']:
 for injected in cfg['gamma_injections']:
  truep=np.array([0,0,0,injected,0.]);truth=model(truep,law,True,True)
  checks[f'{law}_{injected}_interp_truth']=float(np.max(np.abs(model(truep,law,True)-truth)/eV))
  for profiled in [False,True]:
   label='profiled' if profiled else 'fixed';starts=cfg['starts'][label]
   lo=[-2,-2,-2,-.3,-np.deg2rad(10)] if profiled else [-2,-2,-2,-np.deg2rad(10)]
   hi=[2,2,2,.3,np.deg2rad(10)] if profiled else [2,2,2,np.deg2rad(10)]
   def fun(p):
    vals=(model(p,law,profiled)[train]-truth[train])/eV[train]
    prior=[p[-1]/sigi]
    if profiled:prior.append(p[3]/sigg)
    return np.r_[vals,prior]
   opts=[least_squares(fun,np.array(st),bounds=(lo,hi),xtol=1e-12,ftol=1e-12,gtol=1e-10,max_nfev=1000) for st in starts]
   best=min(opts,key=lambda f:float(f.fun@f.fun));p=best.x;pred=model(p,law,profiled);rhold=pred[hold]-truth[hold]
   # Holdout prediction covariance from train-only local posterior curvature.
   Jall=[];eps=1e-5
   for j in range(len(p)):
    pp=p.copy();pm=p.copy();pp[j]+=eps;pm[j]-=eps
    Jall.append((model(pp,law,profiled)-model(pm,law,profiled))/(2*eps))
   Jh=np.array(Jall).T[hold];F=best.jac.T@best.jac;cov=np.linalg.inv(F);cp=np.diag(eV[hold]**2)+Jh@cov@Jh.T
   exactpred=model(p,law,profiled,True)
   row=dict(law=law,gamma_injected=injected,model=label,log10_T_bias=float(p[2]/np.log(10)),T_ratio_recovered=float(np.exp(p[2])),gamma_recovered=float(p[3]) if profiled else 0.,inclination_recovered_deg=float(np.rad2deg(inc0+p[-1])),star_amplitude=float(np.exp(p[0])),angular_gas_amplitude=float(np.exp(p[1])),train_data_residual_power=float(np.sum(((pred[train]-truth[train])/eV[train])**2)),total_objective=float(best.fun@best.fun),holdout_fixed_prediction_residual_power=float(np.sum((rhold/eV[hold])**2)),holdout_predictive_covariance_residual_power=float(rhold@np.linalg.solve(cp,rhold)),max_holdout_fractional_velocity_residual=float(np.max(np.abs(rhold/truth[hold]))),max_interpolation_error_in_errorV=float(np.max(np.abs(exactpred-pred)/eV)),optimization_success=bool(best.success),optimization_messages=[x.message for x in opts],objective_maximum_start_difference=float(max(x.fun@x.fun for x in opts)-min(x.fun@x.fun for x in opts)),covariance_condition=float(np.linalg.cond(F)),parameters=p.tolist(),all_starts=[dict(success=bool(x.success),objective=float(x.fun@x.fun),parameters=x.x.tolist()) for x in opts])
   result.append(row)
   if injected==0:checks[f'{law}_{label}_zero_gradient_recovery']=abs(row['log10_T_bias'])<1e-7 and row['holdout_fixed_prediction_residual_power']<1e-8
   checks[f'{law}_{injected}_{label}_interpolation']=row['max_interpolation_error_in_errorV']<1e-3
   checks[f'{law}_{injected}_{label}_multistart']=row['objective_maximum_start_difference']<1e-5
allchecks=all((v<1e-6) if 'interp_truth' in k else bool(v) for k,v in checks.items())
res=dict(assertion_tested='Nonlinear recovery of T under direct source-gradient injections,with frozen train/holdout annuli on one olddevelopmenttemplate; no observed law residuals fitted.',selected_target='NGC2403',selection=cfg,rows=rows,training_indices=train.tolist(),holdout_indices=hold.tolist(),training_radii_kpc=R[train].tolist(),holdout_radii_kpc=R[hold].tolist(),checks=checks,all_checks=allchecks,results=result,interpretation='Both truth and inverse use the specified scoped pointwise prescription and softened disk response; this tests numerical inverse/identification and train-to-heldout extrapolation only. Predictive covariance is local Gaussian,not calibrated nonlinear coverage.')
(out/'results.json').write_text(json.dumps(res,indent=2))
for x in result:print(x['law'],x['gamma_injected'],x['model'],'T_bias_dex',round(x['log10_T_bias'],6),'gamma_fit',round(x['gamma_recovered'],5),'trainpower',round(x['train_data_residual_power'],4),'hold_pred_power',round(x['holdout_predictive_covariance_residual_power'],4))
print('all checks',allchecks)
if not allchecks:raise SystemExit(1)
