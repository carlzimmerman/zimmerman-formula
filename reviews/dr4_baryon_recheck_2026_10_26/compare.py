import ast,json,pathlib,sys
import numpy as np
from scipy.optimize import least_squares
from numpy.polynomial.legendre import leggauss
ROOT=pathlib.Path(__file__).resolve().parents[2]; G=4.30091e-6
# Reuse only previously benchmarked analytic force definitions, without rerunning their experiment.
src=ast.parse((ROOT/'reviews/dr4_flexible_halo_2026_10_26/fit.py').read_text())
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in ('halo','mn','model')],type_ignores=[]),'analytic_force_definitions','exec'))
r=json.loads((ROOT/'reviews/dr4_baryon_recheck_2026_10_26/run/results.json').read_text());out=[]
for selected in r['selected']:
 c=selected['fine'];pts=np.array(c['points_kpc']);total=np.array(c['total_forces']);bar=np.array(c['baryon_forces']);n=18
 for kind in ('spherical','oblate_free','halo_plus_disc'):
  lo=list(np.log([1e3,.5]));hi=list(np.log([1e10,100]))
  if kind=='oblate_free':lo+=[np.log(.08)];hi+=[0.]
  if kind=='halo_plus_disc':lo+=list(np.log([1e7,.1,.03]));hi+=list(np.log([2e11,30,5]))
  def residual(p,sl):return ((bar[sl]+model(p,pts[sl],kind)-total[sl])/total[sl]).ravel()
  fits=[]
  for rs in (5,20,50):
   p=list(np.log([1e7,rs]))
   if kind=='oblate_free':p+=[np.log(.4)]
   if kind=='halo_plus_disc':p+=list(np.log([2e10,8,.3]))
   s=least_squares(residual,p,args=(slice(0,n),),bounds=(lo,hi),max_nfev=400,ftol=1e-10,xtol=1e-10,gtol=1e-10);fits.append(s)
  s=min(fits,key=lambda s:sum(s.fun*s.fun));assert s.success
  d=residual(s.x,slice(n,None)).reshape(-1,2)
  row=dict(footing=selected['footing'],baryon_sigma=selected['sigma_b'],Rd=selected['Rd'],Mbulge=selected['Mbulge'],model=kind,parameters=np.exp(s.x).tolist(),heldout_rms=float(np.sqrt(np.mean(d*d))),heldout_R_rms=float(np.sqrt(np.mean(d[:,0]**2))),heldout_z_rms=float(np.sqrt(np.mean(d[:,1]**2))),max_abs=float(np.max(abs(d))),heldout_residual=d.tolist(),toy_3sigma_independent_error=float(np.linalg.norm(d)/3))
  out.append(row);print(row['footing'],kind,'rms',row['heldout_rms'],'parameters',row['parameters'],flush=True)
(ROOT/sys.argv[1]).write_text(json.dumps({'scope':'fixed revised baryons; fits to selected v3 force targets, not actual observations','training_points':18,'heldout_points':15,'fits':out},indent=2)+'\n')
