import argparse,json,time
from pathlib import Path
import numpy as np
from aqual_lensing import make_field, polar_map, geometry

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    q=.8133792204448107; re=1.139181788743383; n=5.868719099803722
    masses=np.linspace(11.55,12.4,35); maps=[]; records=[]
    for m in masses:
        start=time.monotonic()
        field=make_field(10**m,re/np.sqrt(q)*geometry()[0],n,q,nr=320,nt=64)
        rad,ang,au,av=polar_map(field,nr=150,na=65,nlos=256)
        maps.append(np.stack((au,av)))
        record=dict(logmass=float(m),residual=field['residual'],iterations=field['iterations'],
                    deposited_mass_ratio=field['deposited_mass']/10**m,seconds=time.monotonic()-start)
        records.append(record);print(json.dumps(record),flush=True)
    np.savez_compressed(out/'library.npz',logmass=masses,rad=rad,angle=ang,alpha=np.array(maps),
        re_geom=re,n=n,q=q,a0=9.3603e-11,inclination=90.)
    (out/'summary.json').write_text(json.dumps(dict(parameters={'re_geometric_arcsec':re,'n':n,'q':q,
        'inclination_degrees':90,'a0_si':9.3603e-11,'nr':320,'nt':64,'nlos':256},records=records),indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
