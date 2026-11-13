import argparse,json,time
from pathlib import Path
import numpy as np
from aqual_lensing import make_field, projected_deflection, spherical_abel_alpha, geometry

def main(out):
    out=Path(out); out.mkdir(exist_ok=True,parents=True)
    mass=10**11.8310873126; re=1.0621496555*geometry()[0]; n=5.663353615
    theta=np.array([.1,.3,.7,1.,1.5,2.,3.,5.])
    exact=spherical_abel_alpha(mass,re,n,theta)
    records=[]
    for nr,nt,rmax in [(128,32,500),(256,48,500),(256,48,1000)]:
        start=time.monotonic()
        field=make_field(mass,re,n,1.,nr=nr,nt=nt,rmax_re=rmax)
        au,av=projected_deflection(field,theta,np.zeros_like(theta),nlos=256)
        rec=dict(nr=nr,nt=nt,rmax_re=rmax,theta=theta.tolist(),numeric=au.tolist(),
            reference=exact.tolist(),relative_error=(au/exact-1).tolist(),
            mass_error=field['deposited_mass']/mass-1,residual=field['residual'],
            iterations=field['iterations'],seconds=time.monotonic()-start)
        print(json.dumps(rec),flush=True);records.append(rec)
    # Numerical validation threshold only; stricter image-error checks follow.
    assert max(abs(np.array(records[-1]['relative_error'])))<.005
    (out/'validation.json').write_text(json.dumps(dict(records=records,scope='spherical field/projection finite benchmark'),indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
