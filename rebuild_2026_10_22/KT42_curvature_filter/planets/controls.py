import argparse,json,math
from pathlib import Path
import numpy as np
import calculate as P


def local_b(R,eta,ell,width):
    r=np.array([R]);hr,ht,*_=P.S.softened_tidal(r,width)
    mu,w=P.S.leggauss(160);g=R**-2;x=g*g+eta*eta+2*g*eta*mu
    s=ell*ell*(hr[0]**2+2*ht[0]**2);h=s**P.S.P
    beta=P.S.P*ell*ell*s**(P.S.P-1)
    _,d1,*_=P.S.C.base.scaled_R(x+h)
    avg=.5*float(np.sum(w*beta*x/(x+h)*d1))
    return avg*hr[0],avg*ht[0]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    data=json.loads((P.HERE/'run_001/results.json').read_text())
    out={'model_null':[],'omitted_return':[],'orbital_series_domain':[],'checks':{}}
    original=P.S.C.base.scaled_R
    def newtonian_R(z):return tuple(np.zeros_like(z) for _ in range(4))
    try:
        P.S.C.base.scaled_R=newtonian_R
        for foot,ff in data['footings'].items():
            rm=ff['rM_m'];eta=ff['eta'];ell=3*P.S.C.KPC/rm
            for width_kpc in [.0001,.001]:
                model=P.Monopole(eta,ell,width_kpc*P.S.C.KPC/rm,nr=1000,nm=80)
                for name,e in P.ECC.items():
                    row=next(r for r in ff['rows'] if r['planet']==name)
                    axis=row['a_au']*P.S.C.old.AU;R=axis/rm;n=math.sqrt(P.S.C.old.GM/axis**3)
                    vals=[float(model.A(R)[0]),float(model.B(R)[0]),model.B_ball(R),P.rate(lambda r:model.total(r/rm),axis,e,n,64)]
                    out['model_null'].append(dict(footing=foot,width_kpc=width_kpc,planet=name,values=vals))
    finally:P.S.C.base.scaled_R=original
    for foot,ff in data['footings'].items():
        rm=ff['rM_m'];eta=ff['eta'];ell=3*P.S.C.KPC/rm
        for row in ff['rows']:
            R=row['a_au']*P.S.C.old.AU/rm;width=row['width_kpc']*P.S.C.KPC/rm
            bound=row['max_i1_argument']*(1+row['eccentricity'])
            six=P.i1_pair(np.array([bound]),6);eight=P.i1_pair(np.array([bound]),8)
            out['orbital_series_domain'].append(dict(footing=foot,planet=row['planet'],width_kpc=row['width_kpc'],max_z_bound=bound,
                                                     six_eight_difference=max(float(np.max(np.abs(a-b))) for a,b in zip(six,eight))))
            if row['width_kpc'] not in [.0001,.001]:continue
            br,bt=local_b(R,eta,ell,width);values=[]
            for frac in [.001,.0003,.0001]:
                plus=local_b(R*(1+frac),eta,ell,width)[0];minus=local_b(R*(1-frac),eta,ell,width)[0]
                derivative=(plus-minus)/(2*R*frac)
                values.append(float(-derivative-2*(br-bt)/R))
            out['omitted_return'].append(dict(footing=foot,planet=row['planet'],width_kpc=row['width_kpc'],unreturned_B=values,
                                              full_returned_B=row['B_over_a0'],difference=values[-1]-row['B_over_a0'],
                                              derivative_refinement=abs(values[-1]-values[-2])))
    out['checks']['full_model_null']=all(all(v==0 for v in r['values']) for r in out['model_null'])
    out['checks']['omitted_return_mutation_bites']=max(abs(r['difference']) for r in out['omitted_return'])>1e-4
    out['checks']['local_derivative_refinement']=max(r['derivative_refinement']/max(1.,abs(r['unreturned_B'][-1])) for r in out['omitted_return'])<1e-6
    out['checks']['orbital_z_domain']=max(r['max_z_bound'] for r in out['orbital_series_domain'])<.02
    out['checks']['orbital_series_convergence']=max(r['six_eight_difference'] for r in out['orbital_series_domain'])<1e-14
    out['all_checks_pass']=all(out['checks'].values())
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'all_checks_pass':out['all_checks_pass'],'checks':out['checks']}))
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
