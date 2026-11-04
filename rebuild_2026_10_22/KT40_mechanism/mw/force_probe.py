"""Independent potential-difference check and fine vertical force profiles."""
import argparse,json,math
from pathlib import Path
import diagnose as D
J,M,E,np=D.J,D.M,D.E,D.np


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();J.set_power(D.P);cells=E.population()
    prior=json.loads((Path(__file__).parent/'hydro_002/results.json').read_text())
    out=dict(power=D.P,ell_kpc=D.ELL,cases=[],complete=False)
    def save():args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    for foot,index in [('canonical',1368),('alt',1287)]:
        for ref in [3,4,5,6]:
            g,mu=D.grid(foot,ref,.005,1.);a0=M.C.A0[foot]
            sol=M.Solver(g,mu,a0);model=J.Generalized(sol)
            rf,_=M.rho_cell(cells[index]);rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4)
            psi=sol.LU.newton(rho);gg,hh=model.fields(psi)
            A,_,_,_=model.coefficients(gg,hh,D.ELL)
            source,_=model.source(psi,D.ELL,fields=(gg,hh))
            sa=-(g.Crr.T@(g.vol*A[0])+g.Cth.T@(g.vol*A[1]))/g.vol
            pa=sol.LU.lu.solve(sa);pb=sol.LU.lu.solve(source-sa);total=psi+pa+pb
            conversion=a0*M.C.PS.KPC/1e6
            fields={}
            for name,potential in [('Newton',psi),('A',pa),('B',pb),('total',total)]:
                gr,gt=g.grad_cells(potential)
                fields[name]=(np.cos(g.t2d)*gr-np.sin(g.t2d)*gt)*conversion
            z=np.linspace(.02,1.5,149);profiles=[]
            for R in [8.122,12.]:
                profiles.append(dict(R_kpc=R,z_kpc=z.tolist(),force={name:g.interp_cells(value,np.full_like(z,R),z).tolist() for name,value in fields.items()}))
            points=[]
            for R,Z in [(8.122,.1),(12.,.3)]:
                interp=lambda field,r,z:float(g.interp_cells(field,np.array([r]),np.array([z]))[0])
                parts={name:interp(value,R,Z) for name,value in fields.items()}
                diffs=[]
                for h in [.005,.01,.02]:
                    fd=(interp(total,R,Z+h)-interp(total,R,Z-h))/(2*h)*conversion
                    diffs.append(dict(step_kpc=h,potential_difference_gz=fd,relative_error=abs(fd-parts['total'])/abs(parts['total'])))
                if ref<6:
                    c=next(c for c in prior['cases'] if c['footing']==foot and c['refine']==ref)
                    old=next(j for j in c['jets'] if j['R_kpc']==R and j['Z_kpc']==Z)['hydrostatic_barotropic_two_gas']['physical_gz_km2_s2_per_kpc']
                    assert abs(parts['total']-old)/abs(old)<1e-8
                if ref==6:
                    assert min(v['relative_error'] for v in diffs)<.05
                    assert all(np.sign(v['potential_difference_gz'])==np.sign(parts['total']) for v in diffs)
                points.append(dict(R_kpc=R,z_kpc=Z,force_parts=parts,potential_differences=diffs))
            out['cases'].append(dict(footing=foot,index=index,refine=ref,points=points,profiles=profiles))
            save();print(foot,ref,[p['force_parts']['total'] for p in points],flush=True)
    for foot in ['canonical','alt']:
        a=next(c for c in out['cases'] if c['footing']==foot and c['refine']==5)
        b=next(c for c in out['cases'] if c['footing']==foot and c['refine']==6)
        assert max(abs(x['force_parts']['total']-y['force_parts']['total'])/abs(y['force_parts']['total']) for x,y in zip(a['points'],b['points']))<.02
    out['complete']=True;out['all_checks_pass']=True;save()


if __name__=='__main__':main()
