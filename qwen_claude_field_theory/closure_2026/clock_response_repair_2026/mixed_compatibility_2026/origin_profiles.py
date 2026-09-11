#!/usr/bin/env python3
"""Compare derivative representations on fixed fresh states; not evolution."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from collocated_probe import CollocatedEvolution
from integrated_probe import radial_profiles


def inspect(n):
    here=Path(__file__).resolve().parent
    with np.load(here/f'evolution_001/state_{n}.npz') as saved:
        r=saved['r'];state=saved['state']
    system=CollocatedEvolution(.02,.3,n,3.,.022,1e-6)
    rates,_=system.rhs(.02,state);f=system.latest_fields;z=r*r
    # Subtract constant background before spline differentiation.
    product=f['N']*f['Q'];fit=CubicSpline(z,product-product[0])
    shared_rate=2*r*fit(z,1)
    shared_second=2*fit(z,1)+4*z*fit(z,2)
    refit=CubicSpline(z[1:],shared_rate[1:]/r[1:])
    resampled_second=refit(z)+2*z*refit(z,1)
    actual_second=radial_profiles(r,*rates[[1,4,5,6,7]])[2](r,1)
    action=system.mixed_target
    errors=dict(shared_minus_action=shared_second-action,
                resample_minus_shared=resampled_second-shared_second,
                candidate_minus_action=actual_second-action,
                shared_rate_minus_kinematic=shared_rate-f['Nr']*f['Q']-f['N']*f['Qr'])
    bands={}
    for lower in (0.,.1):
        mask=(r>=lower)&(r<2.8)
        bands[str(lower)]={name:dict(max=float(np.max(abs(value[mask]))),
                                     radius=float(r[mask][np.argmax(abs(value[mask]))]))
                           for name,value in errors.items()}
    rows=[dict(index=i,r=float(r[i]),action=float(action[i]),
               shared_second=float(shared_second[i]),
               **{key:float(value[i]) for key,value in errors.items()}) for i in range(10)]
    return dict(points=n,bands=bands,first_ten_nodes=rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args()
    result=dict(cases=[inspect(n) for n in (129,257,513)],
                scope='Fixed-state representation comparison; neither shared spline nor FD is an exact continuum solution')
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
