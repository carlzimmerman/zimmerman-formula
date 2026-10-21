#!/usr/bin/env python3
"""Independent analytic angular mass/half-disk checks for V2 importance quadrature."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import quad
from scipy.special import erf, ndtr

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from forward_model_v2 import component_geometry


def exact_halves(phase,sigma):
    if sigma==0:return 0.,0.
    lo,hi=phase-np.pi,phase+np.pi
    first=int(np.ceil((lo-np.pi/2)/np.pi));last=int(np.floor((hi-np.pi/2)/np.pi))
    cuts=[lo]+[np.pi/2+k*np.pi for k in range(first,last+1) if lo<np.pi/2+k*np.pi<hi]+[hi]
    red=blue=0.
    for a,b in zip(cuts[:-1],cuts[1:]):
        mass=sigma*np.sqrt(2*np.pi)*(ndtr((b-phase)/sigma)-ndtr((a-phase)/sigma))
        if np.cos((a+b)/2)>=0:red+=mass
        else:blue+=mass
    return red,blue


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    cases=[]
    for phase_deg in [15.,89.99,90.,90.01,270.,-179.,578.]:
        for width in [0.,1e-5,1.,40.,300.]:
            radius=100.;sigma=width/radius;phase=np.deg2rad(phase_deg)
            p={'radius':[1.,500.],'interpolation':'linear','arm_wedge_deg':360.,
                'arm1':{'width':[width,width],'phase':[phase_deg-180,phase_deg-180],'sbr':[1.,1.]}}
            _,phi,_,w=component_geometry(p,np.array([radius]),1,256,64)
            total=sigma*np.sqrt(2*np.pi)*erf(np.pi/(np.sqrt(2)*sigma)) if sigma else 0.
            red,blue=exact_halves(phase,sigma)
            numerical=np.array([w.sum(),w[np.cos(phi)>=0].sum(),w[np.cos(phi)<0].sum()])
            exact=np.array([total,red,blue])
            denom=max(total,1e-30)
            error=float(np.max(abs(numerical-exact))/denom)
            if sigma:
                # Integrate in standardized Gaussian variable so very narrow
                # angular arms do not disappear inside adaptive radial sampling.
                bound=min(np.pi/sigma,12.)
                moment=quad(lambda t:np.cos(phase+sigma*t)*np.exp(-t*t/2)*sigma,
                            -bound,bound,epsabs=1e-13,epsrel=1e-12,limit=200)[0]
                moment_error=abs(np.dot(w,np.cos(phi))-moment)/denom
            else:moment_error=0.
            cases.append({'phase_deg':phase_deg,'width_arcsec':width,'source_radius_arcsec':radius,
               'nodes':int(len(phi)),'exact_total_receding_approaching':exact.tolist(),
               'numeric_total_receding_approaching':numerical.tolist(),
               'max_normalized_mass_error':error,'normalized_cosine_moment_error':float(moment_error),
               'passed':bool(error<1e-8 and moment_error<5e-4)})
    result={'cases':cases,'case_count':len(cases),'all_passed':all(v['passed'] for v in cases),
      'max_normalized_mass_error':max(v['max_normalized_mass_error'] for v in cases),
      'max_normalized_cosine_moment_error':max(v['normalized_cosine_moment_error'] for v in cases),
      'scope':'Finite importance-quadrature mass/half-disk/moment checks; no observed cube or universal renderer accuracy claim.'}
    (out/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if result['all_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
