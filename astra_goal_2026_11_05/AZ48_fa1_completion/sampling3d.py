#!/usr/bin/env python3
"""Interior Hessian interpolation and predeclared point/disc diagnostics."""
import itertools,json,math
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import audit_inputs as A
import bullet_source as B
import grid3d as D
import spherical_boundary as R
THRESHOLDS=A.ROOT/'rebuild_2026_10_22/FA1_fresh_action/I6_galileon/i6_results.json'
POINTS=dict(BCG1=[0.,0.,0.],BCG3=[820.,220.,0.],GASM=[190.,90.,0.],GASB=[670.,170.,0.])
def inherited_threshold(foot):
    return float(json.loads(THRESHOLDS.read_text())['xcop']['footings'][foot]['s_c'])
class Sampler:
    def __init__(self,grid,hessian,mutate=False):
        axes=[v[1:-1] for v in grid.axes]
        self.interpolators=[RegularGridInterpolator(axes,h,method='linear',bounds_error=True) for h in hessian]
        _,norm=D.selector(hessian);self.max_norm=float(np.max(norm));self.mutate=mutate
    def __call__(self,points_kpc):
        points=np.asarray(points_kpc,float)/B.L0_KPC
        if points.ndim!=2 or points.shape[1]!=3 or not np.all(np.isfinite(points)):raise ValueError('Finite Nx3 points required')
        h=[interpolator(points) for interpolator in self.interpolators]
        s,norm=D.selector(h,self.mutate)
        tiny=(norm<=64*np.finfo(float).eps*self.max_norm)|(~np.isfinite(norm))|(~np.isfinite(s))
        return dict(s=s,norm=norm,tiny=tiny)
def disc_nodes(centre,nr,nt):
    if nr<=0 or nt<=0:raise ValueError('Positive disc quadrature orders required')
    radius=100*np.sqrt((np.arange(nr)+.5)/nr);angle=2*math.pi*(np.arange(nt)+.5)/nt
    x=(radius[:,None]*np.cos(angle)).ravel();y=(radius[:,None]*np.sin(angle)).ravel()
    points=np.column_stack([x,y,np.zeros(len(x))])+np.asarray(centre)
    return points,np.full(len(points),1/len(points))
def disc(sampler,centre,threshold,nr,nt):
    points,weights=disc_nodes(centre,nr,nt);value=sampler(points)
    mean=float(np.sum(weights*value['s']));fraction=float(np.sum(weights*(value['s']>=threshold)))
    return dict(nr=nr,ntheta=nt,mean_s=mean,on_fraction=fraction,mean_on=bool(mean>=threshold),min_hessian_norm=float(np.min(value['norm'])),tiny_samples=int(np.sum(value['tiny'])))
def threshold_reading(values,threshold):
    flags={name:bool(value>=threshold) for name,value in values.items()}
    wrong=(flags['GASM'] and not flags['BCG1']) or (flags['GASB'] and not flags['BCG3'])
    label='WRONG SIGN' if wrong else ('WEIGHT ALLOWED AT GALAXIES' if flags['BCG1'] and flags['BCG3'] else 'NO SIGN')
    intervals={name:(dict(lower_open=values[bcg],upper_closed=values[gas]) if values[gas]>values[bcg] else None) for name,bcg,gas in [('main','BCG1','GASM'),('bullet','BCG3','GASB')]}
    return dict(inherited_threshold=threshold,on=flags,conditional_reading=label,both_BCG_allowed_threshold_upper_closed=min(values['BCG1'],values['BCG3']),wrong_sign_intervals=intervals)
def plummer_oracle(foot):
    directions=np.r_[np.eye(3),-np.eye(3),np.array(list(itertools.product([-1.,1.],repeat=3)))/math.sqrt(3)]
    ratios=np.repeat([.3,.5,1.,2.,5.],len(directions));points=np.concatenate([ratio*565*directions for ratio in [.3,.5,1.,2.,5.]])
    radial,tangent=R.radial_eigenvalues(ratios*565/B.L0_KPC,B.normalization(foot)['epsilon'],np.array([[2e14,565.,0.,0.,0.]]))
    s=3*math.sqrt(3)*radial*tangent*tangent/(radial*radial+2*tangent*tangent)**1.5
    return dict(points_kpc=points.tolist(),r_over_a=ratios.tolist(),s=s.tolist(),on=(s>=inherited_threshold(foot)).tolist())
