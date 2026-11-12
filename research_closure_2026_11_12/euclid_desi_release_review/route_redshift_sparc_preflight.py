import pathlib,json,math,sys,hashlib
import numpy as np
import sympy as sp
root=pathlib.Path(__file__).parent;out=root/sys.argv[1];out.mkdir(exist_ok=True)
sel=json.loads((root/'route_redshift_sparc_selection.json').read_text())
# All geometries/targets/scenarios are fixed in selection before Fisher evaluation.
meta={}
for line in (root/'route_redshift_sparc_inputs/SPARC_Lelli2016c.mrt').read_text().splitlines():
 t=line.split()
 if t and t[0] in sel['targets']:meta[t[0]]=dict(D_Mpc=float(t[2]),inc_deg=float(t[5]),inc_error_deg=float(t[6]),Rd_kpc=float(t[11]),quality=int(t[17]))
KPC=3.085677581491367e19

def radial_gradient_response(R,SB,Rd,nr,nphi,hfrac):
 # Softened ring gravity; baseline amplitude is calibrated to published disk force.
 # This supplies a physical radial-source-gradient derivative, not an AQUAL disk solve.
 rp=(np.arange(nr)+.5)*(max(R)*2/nr);dr=max(R)*2/nr
 positive=SB>0;rr=R[positive];ls=np.log(SB[positive]);slope=(ls[-1]-ls[-2])/(rr[-1]-rr[-2])
 if slope>=0:slope=-1/Rd
 lnSigma=np.interp(rp,rr,ls,left=ls[0],right=ls[-1])
 tail=rp>rr[-1];lnSigma[tail]=ls[-1]+slope*(rp[tail]-rr[-1]);Sigma=np.exp(lnSigma)
 phi=(np.arange(nphi)+.5)*(2*np.pi/nphi);co=np.cos(phi)[None,:];rpr=rp[:,None];h=hfrac*Rd
 weight=rp*Sigma*dr*(2*np.pi/nphi);weight_grad=weight*np.log(rp/Rd)
 g0=[];gg=[]
 for r in R:
  kernel=(r-rpr*co)/(r*r+rpr*rpr-2*r*rpr*co+h*h)**1.5
  angular=kernel.sum(axis=1);g0.append(weight@angular);gg.append(weight_grad@angular)
 g0=np.array(g0);gg=np.array(gg)
 return gg/g0,dict(min_reference_force=float(g0.min()),finite=bool(np.isfinite(gg/g0).all()))

def fisher_summary(J,e,indices,priors):
 X=J[:,indices]/e[:,None];F=X.T@X
 for idx,sigma in priors.items():
  if idx in indices:F[indices.index(idx),indices.index(idx)]+=1/sigma**2
 sv=np.linalg.svd(F,compute_uv=False);rank=int(np.sum(sv>sv[0]*1e-11));it=indices.index(2)
 ans=dict(parameter_indices=indices,rank=rank,columns=len(indices),condition=float(sv[0]/sv[-1]) if sv[-1]>0 else None,priors=priors)
 if rank<len(indices):ans.update(sigma_logT=None,reason='Rank deficient at relative eigenvalue threshold1e-11; no finite marginalized error claimed.')
 else:
  cov=np.linalg.inv(F);ans.update(sigma_logT=float(np.sqrt(cov[it,it])),sigma_log10T=float(np.sqrt(cov[it,it])/np.log(10)))
 return ans
allrows=[];benchmarks={};profiles=[]
for name in sel['targets']:
 dat=np.loadtxt(root/f'route_redshift_sparc_inputs/{name}_rotmod.dat');R,V,eV,Vgas,Vdisk,Vbul,SB=dat[:,:7].T
 valid=(R>0)&(V>0)&(eV>0);R,V,eV,Vgas,Vdisk,Vbul,SB=[x[valid] for x in [R,V,eV,Vgas,Vdisk,Vbul,SB]]
 if np.any(Vbul!=0):raise RuntimeError('preselected zero-bulge condition fails: '+name)
 m=meta[name];theta=R/(m['D_Mpc']*1000);bstar=sel['Upsilon_reference']*Vdisk**2*1e6/(R*KPC);bgas=np.sign(Vgas)*Vgas**2*1e6/(R*KPC);S=bstar+bgas
 if not np.all(S>0):raise RuntimeError('nonpositive baryonic field')
 d0,chk0=radial_gradient_response(R,SB,m['Rd_kpc'],1024,256,.1)
 d1,chk1=radial_gradient_response(R,SB,m['Rd_kpc'],2048,512,.1)
 grad_convergence=float(np.max(np.abs(d1-d0)))
 profiles.append(dict(name=name,rows=len(R),radius_kpc=[float(R.min()),float(R.max())],theta_arcsec=[float(theta.min()*206264.806),float(theta.max()*206264.806)],gbar_over_a0=[float(S.min()/sel['a0']),float(S.max()/sel['a0'])],median_fractional_V_error=float(np.median(eV/V)),gradient_response_max_grid_difference=grad_convergence,ring_checks=[chk0,chk1]))
 for law in ['simple_mu','quadratic']:
  a=sel['a0'];g=(S+np.sqrt(S*S+4*S*a))/2 if law=='simple_mu' else np.sqrt(S*S+a*S)
  t=a/(g+2*a) if law=='simple_mu' else 1/(2*(S/a+1));ab=1-t
  fstar=bstar/S;fgas=bgas/S
  inc=math.radians(m['inc_deg']);si=math.radians(m['inc_error_deg'])
  # Parameters:lnA_star,lnA_gas,lnT,source-M/L power gamma,delta_i radians.
  J=np.column_stack([ab*fstar,ab*fgas,t,ab*fstar*d1,np.full(len(R),2/math.tan(inc))])
  e=2*eV/V
  exact_null=J[:,0]+J[:,1]+J[:,2]-J[:,4]*math.tan(inc)/2
  benchmarks[name+'_'+law+'_inclination_null']=float(np.max(np.abs(exact_null)))
  cases=[('gas_known_i_fixed_gradient_fixed',[0,2],{}),('gas_free_i_fixed_gradient_fixed',[0,1,2],{}),('gas_free_i_catalogue_prior_gradient_fixed',[0,1,2,4],{4:si}),('gas_free_i_catalogue_prior_gradient_sigma0.1',[0,1,2,3,4],{4:si,3:.1}),('gas_free_i_catalogue_prior_gradient_sigma0.3',[0,1,2,3,4],{4:si,3:.3}),('gas_free_i_catalogue_prior_gradient_free',[0,1,2,3,4],{4:si}),('gas_free_i_free_gradient_sigma0.1',[0,1,2,3,4],{3:.1})]
  for label,ids,pri in cases:
   row=fisher_summary(J,e,ids,pri);row.update(name=name,law=law,scenario=label,inclination_only_log10T_floor=float(2/math.tan(inc)*si/np.log(10)));allrows.append(row)
# Exact portal shape and background-operator checks.
t=sp.symbols('t',positive=True);Am,Ar,K=sp.symbols('Am Ar K');F=sp.Function('F')(t);E=F-Am*t**3-Ar*t**4-K*t**2;P=E-t*sp.diff(E,t)/3;VP=E-t*sp.diff(E,t)/6
w,wr=sp.symbols('w wr');portalchecks={'pressure_operator_dust_cancels':sp.simplify(3*P-(3*F-t*sp.diff(F,t)+Ar*t**4-K*t**2))==0,'potential_operator':sp.simplify(VP-(F-t*sp.diff(F,t)/6-Am*t**3/2-Ar*t**4/3-2*K*t**2/3))==0,'pressure_potential_equal_only_if_w_equal':sp.factor(w*(1-wr)-wr*(1-w))==w-wr}
res=dict(assertion_tested='Local information only on three preselected old SPARC templates at actual radial sampling and quoted velocity errors;no law residual or fitted a0 scored.',selection=sel,geometry=meta,profiles=profiles,fisher_rows=allrows,inclination_null_residuals=benchmarks,portal_symbolic_checks={k:bool(v) for k,v in portalchecks.items()},all_benchmarks_pass=all(v<1e-12 for v in benchmarks.values()) and all(portalchecks.values()),limits=['Pointwise algebraic gravity,not AQUAL disk solution','Diagonal velocity errors only;no measured radial covariance','Local Fisher at fixed fiducialUpsilon0.5,a0=9.3603e-11;not fit to observed velocity residuals','Disk source-gradient response uses softened ring model with h=.1Rd and catalog force calibration','Inclination effect only velocity deprojection;changes to photometric deprojection omitted','No gas or stellar template measurement covariance','No new observations or external data downloads'])
(out/'results.json').write_text(json.dumps(res,indent=2));print('rows',len(allrows),'benchmarks',res['all_benchmarks_pass'])
for row in allrows:
 if 'sigma0.1' in row['scenario'] and 'catalogue' in row['scenario']:print(row['name'],row['law'],row['sigma_log10T'])
if not res['all_benchmarks_pass']:raise SystemExit(1)
