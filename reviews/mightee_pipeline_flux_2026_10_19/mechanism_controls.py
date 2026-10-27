"""Controlled mechanisms, not a reproduction of the unpinned production pipeline."""
from pathlib import Path
import sys,json
import numpy as np
from scipy.ndimage import median_filter,gaussian_filter1d
from scipy.signal import fftconvolve,savgol_filter

def main():
    out=Path(sys.argv[1]);out.mkdir(exist_ok=True);n=257;pixel=2.;yy,xx=np.indices((n,n));rr=((xx-n//2)*pixel)**2+((yy-n//2)*pixel)**2
    def beam(theta):return np.exp(-4*np.log(2)*rr/theta**2)
    def area(theta):return np.pi*theta**2/(4*np.log(2))/pixel**2
    original,target=50.,75.;gi=beam(original);gt=beam(target);kernel=beam(np.sqrt(target**2-original**2));kernel/=kernel.sum()
    residue=fftconvolve(gi,kernel,mode='same');rows=[]
    for clean_fraction in [0,.25,.5,.75,1]:
        # The inspected old script uses a fitted-beam model plus a unit-sum-smoothed residual.
        old=clean_fraction*gi+(1-clean_fraction)*residue
        corrected=clean_fraction*gt+(1-clean_fraction)*residue*area(target)/area(original)
        wrong=float(old.sum()/area(target));right=float(corrected.sum()/area(target))
        assert abs(wrong-(original/target)**2)<1e-9
        assert abs(right-1)<1e-9
        rows.append(dict(clean_fraction=clean_fraction,unit_area_residual_and_fitted_model_flux=wrong,target_model_and_area_rescaled_residual_flux=right))
    # Show only the filter's mathematical capacity; exact historical clipping/interpolation is not claimed.
    x=np.arange(1001);responses=[]
    for width in [5,15,25,35,55,85]:
        line=gaussian_filter1d((abs(x-500)<=width/2).astype(float),2)
        estimate=savgol_filter(median_filter(line,size=31,mode='nearest'),31,1)
        within=abs(x-500)<=width/2+10
        unprotected=float(np.sum((line-estimate)[within])/np.sum(line[within]))
        # Perfect exclusion + interpolation across the entire line preserves a zero baseline.
        protected_estimate=np.zeros_like(line)
        protected=float(np.sum((line-protected_estimate)[within])/np.sum(line[within]))
        assert abs(protected-1)<1e-12
        responses.append(dict(line_width_channels=width,unmasked_filter_recovery=unprotected,perfectly_masked_recovery=protected))
    result=dict(status='passed',beam_demo=dict(input_fwhm_arcsec=original,target_fwhm_arcsec=target,analytic_area_ratio=(original/target)**2,results=rows),filter_demo=responses,limits=['Demonstrates possible mechanisms, not evidence that production cubes used the inspected historical script','No simulation-calibrated correction applied to measured galaxies','Continuum filter toy omits noise-dependent sigma clipping and morphological masks; protected/unprotected cases bound a mechanism, not actual data response'])
    (out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
