"""Bounded diagnosis of finite-core angular cancellation at unresolved rmin."""
import argparse,json,math
from pathlib import Path
import calculate as C


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    out=dict(hypothesis='Tiny rmin relative to a broad smooth core magnifies roundoff in quadrupole moments by r^-2; use analytic contact and a resolved inner integration radius.',rows=[])
    for foot,a0 in C.old.A0.items():
        eta=C.old.GEXT/a0;ell=.03*C.KPC/math.sqrt(C.old.GM/a0)
        for sigma in [.5,.1]:
            family=[]
            for frac in [.001,.0005,.00025]:
                q=C.quadrupole(eta,ell,sigma,nr=12000,nm=240,rmin=frac*sigma,rmax=1e7)
                q.update(footing=foot,inner_fraction_of_sigma=frac)
                family.append(q);out['rows'].append(q)
            assert max(abs(x['flux_density_difference']) for x in family)<1e-10
            assert max(x['q_signed'] for x in family)-min(x['q_signed'] for x in family)<1e-10
    out['passed']=True
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print('all core-radius families passed density and radius comparisons',flush=True)


if __name__=='__main__':main()
