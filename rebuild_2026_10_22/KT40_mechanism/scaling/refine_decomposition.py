"""Check individual A/B virial contributions, not just their sum."""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import simpson

HERE=Path(__file__).resolve().parent;RB=HERE.parents[1]
sys.dont_write_bytecode=True
sys.path.insert(0,str(RB/'KT39_power_curvature/analytic'))
from radial_reference import plummer_fields,radial_force


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    d=json.loads((HERE/'run_002/results.json').read_text());out=dict(cases=[],all_checks_pass=False)
    for r in d['dwarfs']:
        if r['upsilon']!=3 or r['name'] not in ['Sculptor','Fornax','Leo I']:continue
        rows=[];a=r['a_kpc'];gm=d['constants']['G']*r['mass_Msun'];a0=d['constants']['A0'][r['footing']]
        for n,domain in [(1000,1),(2000,1),(4000,1),(4000,2)]:
            radius=np.geomspace(1e-6*a,domain*(200*a+40*d['ell_kpc']),n)
            rho=3/(4*np.pi*a**3)*(1+(radius/a)**2)**-2.5;W=4*np.pi/3*rho*radius**3
            response=radial_force(radius,*plummer_fields(radius,gm,a),d['ell_kpc'],a0,p=d['power'])
            va=simpson(W*response['A'],x=radius);vb=simpson(W*(response['phantom']-response['A']),x=radius)
            rows.append(dict(n=n,domain=domain,variance_A=va,variance_B=vb))
        maximum=max(abs(row[key]/rows[-1][key]-1) for row in rows for key in ['variance_A','variance_B'])
        assert maximum<1e-5
        out['cases'].append(dict(name=r['name'],footing=r['footing'],rows=rows,max_component_relative_shift=maximum))
    assert len(out['cases'])==6
    out['all_checks_pass']=True
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(all_checks_pass=True,max_component_relative_shift=max(c['max_component_relative_shift'] for c in out['cases']))))


if __name__=='__main__':main()
