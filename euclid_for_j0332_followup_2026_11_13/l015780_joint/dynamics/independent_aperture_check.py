"""Independent rectangle-minus-rejected-pixels aperture integration.
No dependency on the pixel renderer for the new integral.
"""
import argparse,csv,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad,dblquad,cumulative_trapezoid
from scipy.special import gammainc,gammaincinv,gammaln
from scipy.stats import norm
from astropy.io import fits
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    old=json.loads((HERE/'run_01/result.json').read_text());a=old['central']['aperture']
    cx,cy,q,phi,n,re=[a[k] for k in ['center_west_arcsec','center_north_arcsec','q','phi_west_radians','n','Re_major_arcsec']]
    bn=gammaincinv(2*n,.5);co,si=np.cos(phi),np.sin(phi)
    norm0=np.exp(2*n*np.log(bn)-np.log(2*np.pi*q*n)-2*np.log(re)-gammaln(2*n))
    edges=np.unique(np.sort(np.r_[0.,2*np.pi,[np.arctan2(y-cy,x-cx)%(2*np.pi) for x in [-5,5] for y in [-5,5]]]))
    def angular(t):
        cost,sint=np.cos(t),np.sin(t)
        rx=((5-cx) if cost>0 else (-5-cx))/cost if abs(cost)>1e-14 else np.inf
        ry=((5-cy) if sint>0 else (-5-cy))/sint if abs(sint)>1e-14 else np.inf
        rad=min(rx,ry);metric=(co*cost+si*sint)**2+(-si*cost+co*sint)**2/q**2
        return gammainc(2*n,bn*(rad*np.sqrt(metric)/re)**(1/n))/(2*np.pi*q*metric)
    valerrs=[quad(angular,left,right,epsabs=1e-12,epsrel=1e-12) for left,right in zip(edges[:-1],edges[1:])]
    full=float(sum(x[0] for x in valerrs));error=float(sum(x[1] for x in valerrs))
    yy,xx=np.indices((100,100));X=(xx-49.5)*.1;Y=(yy-49.5)*.1;info=a['mask']
    keep=(X-info['mask_centre'][1])**2+(Y+info['mask_centre'][0])**2<info['mask_radius']**2
    def surface(y,x):
        dx,dy=x-cx,y-cy;rad=np.sqrt((co*dx+si*dy)**2+(-si*dx+co*dy)**2/q**2)
        return norm0*np.exp(-bn*(rad/re)**(1/n))
    dropped=[]
    for i,j in zip(*np.where(~keep)):
        v,e=dblquad(surface,X[i,j]-.05,X[i,j]+.05,lambda _:Y[i,j]-.05,lambda _:Y[i,j]+.05,epsabs=1e-13,epsrel=1e-11)
        dropped.append(dict(row=int(i),col=int(j),flux=float(v),quad_estimated_error=float(e)))
    f=full-sum(v['flux'] for v in dropped);delta=f-a['fraction_pixel_union']
    assert abs(delta)<1e-8
    # Pure prior-normalization sensitivity using the already validated sigma
    # curves. This does not reinterpret the released map as an exact profile.
    with (HERE/'run_01/mass_scan.csv').open() as file:
        rows=list(csv.DictReader(file))
    scan={k:np.array([float(r[k]) for r in rows]) for k in rows[0]}
    x=scan['log10_total_mass'];ma=old['central']['logM_aperture_SED_median'];lo=old['central']['SED_error_lower'];hi=old['central']['SED_error_upper']
    comparisons=[]
    for label,fraction in [('pixel_union',f),('released_map_normalization',a['fraction_released_map_over_analytic_infinite'])]:
        med=ma-np.log10(fraction);sig=np.where(x<med,lo,hi);prior=norm.pdf((x-med)/sig)/sig
        j=np.argmin(abs(x-med))
        if abs(x[j]-med)<1e-10:prior[j]=.5*norm.pdf(0)*(1/lo+1/hi)
        prior/=np.trapz(prior,x);result=dict(label=label,aperture_fraction=fraction,logMtotal_SED_median=med,scenarios=[])
        for row in old['scenarios']:
            beta,seeing=row['beta'],row['seeing_fwhm_arcsec'];key=f'v21_likelihood_beta{beta}_seeing{seeing}'
            like=scan[key];post=prior*like;post/=np.trapz(post,x);cdf=cumulative_trapezoid(post,x,initial=0)
            result['scenarios'].append(dict(beta=beta,seeing=seeing,conditional_logM_quantiles=np.interp([.025,.16,.5,.84,.975],cdf,x).tolist()))
        comparisons.append(result)
    result=dict(assertion_tested='Independent exact radial rectangle quadrature minus 17 smooth excluded-pixel integrals matches the adopted pixel-union fraction; map normalization is a separate prior sensitivity.',
        rectangle_fraction=full,angular_adaptive_error_estimate=error,dropped_pixels=dropped,pixel_union_fraction_independent=f,
        fraction_renderer=a['fraction_pixel_union'],absolute_difference=delta,normalization_sensitivity=comparisons,
        non_claims=['No attribution of map/profile difference to a unique export or sampling mechanism','No new oblate, rotation, source-redshift or lensing inference','Map-normalization sensitivity does not modify adopted spatial shape'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
