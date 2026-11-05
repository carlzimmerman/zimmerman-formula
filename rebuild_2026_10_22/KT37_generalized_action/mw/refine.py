"""Literal selected-source and 2D Hessian/domain refinement for KT37."""
import argparse,json,math,time
from pathlib import Path
import generalized as J
from invariants_v2 import spherical_formula
M,E,np=J.M,J.E,J.np


def grid(foot,refine,rmin=.005,outer=1.):
    a0=M.C.A0[foot];mu=M.C.PS.mass_unit(a0)
    re=M.C.PS.log_edges(rmin,outer*300*max(60,math.sqrt(6.6e10/mu)),30*refine)
    return M.C.PS.Grid(re,M.C.PS.theta_edges(48*refine,full=False,stretch_min=.002/refine)),mu


def geometric_tests(model):
    g=model.g;r,t=g.r2d,g.t2d
    ii=np.arange(g.n)//g.Nt;jj=np.arange(g.n)%g.Nt
    middle=(ii>=2)&(ii<g.Nr-2)
    axial=.5*r*r*np.cos(t)**2
    exact=np.array([np.cos(t)**2,-np.cos(t)*np.sin(t),np.sin(t)**2,np.zeros_like(t)])
    err=model.fields(axial)[1]-exact
    output=dict(axial_quadratic_interior_max=float(np.max(abs(err[:,middle&(jj>=2)&(jj<g.Nt-2)]))),
                axial_quadratic_boundary_max=float(np.max(abs(err[:,middle&((jj==0)|(jj==g.Nt-1))]))))
    psi=-1/np.sqrt(r*r+4)
    q=r/(r*r+4)**1.5;qp=(4-2*r*r)/(r*r+4)**2.5
    hh=model.fields(psi)[1]
    he=np.array([qp,np.zeros_like(q),q/r,q/r]);reg=(r>.05)&(r<20)
    output['plummer_hessian_relative_max']=float(np.max(abs(hh[:,reg]-he[:,reg]))/np.max(abs(he[:,reg])))
    output['spherical_force']=[]
    for ell in (0.,1.,10.):
        ph,_=model.phantom(psi,ell)
        dr,dt=g.grad_cells(ph);expected=spherical_formula(r,ell)
        scale=np.max(abs(expected[reg]))
        output['spherical_force'].append(dict(ell_kpc=ell,radial_relative_max=float(np.max(abs(dr[reg]-expected[reg]))/scale),
            spurious_polar_relative_max=float(np.max(abs(dt[reg]))/scale)))
    return output


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);ap.add_argument('--scan',required=True,type=Path)
    args=ap.parse_args();start=time.monotonic();prior=json.loads(args.scan.read_text());cells=E.population()
    # One independently selected best-D cell per tested length and footing.
    chosen={foot:[(s['ell_kpc'],s['summary']['best_D_index']) for s in f['scans']] for foot,f in prior['footings'].items()}
    out=dict(selection='Frozen best-D cell at each of six scanned lengths; selected refinement only',chosen=chosen,footings={},geometry=[],complete=False)
    def save():args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    for foot,pairs in chosen.items():
        f=[];out['footings'][foot]=f
        for refinement,rmin,outer in [(2,.005,1),(3,.005,1),(4,.005,1),(3,.0025,1),(3,.005,2)]:
            g,mu=grid(foot,refinement,rmin,outer);sol=M.Solver(g,mu,M.C.A0[foot]);model=J.Generalized(sol)
            if foot=='canonical':
                ctl=geometric_tests(model);out['geometry'].append(dict(refine=refinement,rmin=rmin,outer=outer,controls=ctl))
                print('geometry',refinement,rmin,outer,ctl,flush=True)
            for ell,index in pairs:
                rho_fun,_=M.rho_cell(cells[index]);rho=g.rho_axisym(lambda R,z:rho_fun(R,z)/mu,nq=4)
                psi=sol.LU.newton(rho);ph,stats=model.phantom(psi,ell)
                score=sol.evaluate(psi+ph)
                recomputed=M.C.lines(score['vc'],score['K'],score['K0'],score['vc_Ou'])
                assert all(score[k]==recomputed[k] for k in (*M.GATE,'Lh'))
                f.append(dict(index=index,cell=cells[index],ell_kpc=ell,refine=refinement,rmin=rmin,outer=outer,score=score,source_stats=stats))
                print(foot,ell,index,refinement,rmin,outer,{k:score[k] for k in ['vc','K0','cK','cO','D','all_four','Lh']},flush=True)
            save()
    out['complete']=True;out['runtime_seconds']=time.monotonic()-start;save()


if __name__=='__main__':main()
