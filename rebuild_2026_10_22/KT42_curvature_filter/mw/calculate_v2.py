"""Prospectively bounded checks and fixed-baryon curvature-filter diagnostics."""
import argparse
import json
import math
from pathlib import Path
import time
import filtered_model as F
J, M, E, np = F.J, F.M, F.E, F.np
WIDTHS = [0., .0001, .001, .003, .01, .03, .1, .3, 1.]


def invariant_checks():
    J.set_power(1.125)
    g, mu = F.grid('canonical', 2, .005, 1.)
    sol = M.Solver(g, mu, M.C.A0['canonical'])
    model = F.Filtered(sol, .3, 32)
    w, r, th = g.vol, g.r2d, g.t2d
    u = np.exp(-((r-8)/4)**2)*(1+.2*np.cos(2*th))
    v = np.exp(-((r-11)/6)**2)*(1-.3*np.cos(4*th))
    dot = lambda a,b: float((w*a)@b)
    a, b = dot(u, model.filter.forward(v)), dot(model.filter.adjoint(u), v)
    adjoint = abs(a-b)/max(abs(a),abs(b))
    assert adjoint < 1e-12
    WL = F.J.J.diags(w)@g.Lap
    diff = WL-WL.T
    symmetry = np.max(abs(diff.data))/np.max(abs(WL.data)) if diff.nnz else 0.
    assert symmetry < 1e-12
    rho = .02*np.exp(-r*r/64)*(1+.2*np.cos(2*th))
    psi = sol.LU.newton(rho)
    gg, hh = model.fields(psi)
    src, _ = model.source(psi, 3., fields=(gg,hh))
    dgg, dhh = model.fields(u)
    fd = []
    target = dot(src, u)/(4*np.pi)
    for h in [1e-3, 1e-4, 1e-5]:
        ep = model.coefficients(gg+h*dgg,hh+h*dhh,3.)[2]
        em = model.coefficients(gg-h*dgg,hh-h*dhh,3.)[2]
        value = -float(w@(ep-em))/(16*np.pi*h)
        fd.append(dict(step=h, value=value, relative_error=abs(value-target)/abs(target)))
    assert min(row['relative_error'] for row in fd) < 2e-7
    zmodel = F.Filtered(sol, 0., 16)
    old = J.PowerCurvature(sol)
    zs = zmodel.source(psi, 3.)[0]; os = old.source(psi, 3.)[0]
    zero_error = float(np.max(abs(zs-os))/np.max(abs(os)))
    assert zero_error < 1e-13
    # Independent analytic scalar Gaussian convolution away from boundaries.
    heat_checks = []
    q = 2.; value = np.exp(-r*r/(2*q*q)); region = r < 10
    for width in [.3, 1.]:
        exact = (q*q/(q*q+width*width))**1.5*np.exp(-r*r/(2*(q*q+width*width)))
        for m in [32,64,128]:
            result = F.Heat(g,width,m).forward(value)
            err = float(np.max(abs(result[region]-exact[region]))/np.max(exact))
            heat_checks.append(dict(width=width,steps=m,max_error_over_peak=err))
    print('analytic_heat',json.dumps(heat_checks),flush=True)
    assert max(row['max_error_over_peak'] for row in heat_checks) < .004
    # Response reciprocity checks the complete N/adjoint chain, not just T.
    rec = []
    for h in [1e-4,1e-5]:
        du = (model.response(rho+h*u*.001,3.)[0]-model.response(rho-h*u*.001,3.)[0])/(2*h)
        dv = (model.response(rho+h*v*.001,3.)[0]-model.response(rho-h*v*.001,3.)[0])/(2*h)
        aa, bb = dot(v*.001,du),dot(u*.001,dv)
        rec.append(dict(step=h,relative_error=abs(aa-bb)/max(abs(aa),abs(bb))))
    assert min(row['relative_error'] for row in rec) < 1e-6
    return dict(complete=True,all_checks_pass=True,heat_adjoint_relative=adjoint,
        laplacian_weighted_symmetry=symmetry,energy_derivative_target=target,
        energy_derivative=fd,zero_width_source_relative=zero_error,
        analytic_heat=heat_checks,response_reciprocity=rec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--mode',choices=['checks','scan'],default='checks')
    ap.add_argument('--refine',type=int,default=3)
    ap.add_argument('--steps',type=int,default=16)
    ap.add_argument('--widths',type=float,nargs='+',default=WIDTHS)
    ap.add_argument('--rmin',type=float,default=.005)
    ap.add_argument('--outer',type=float,default=1.)
    args = ap.parse_args()
    def save(out): args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    if args.mode == 'checks':
        out = invariant_checks();save(out);print(json.dumps(out),flush=True);return
    J.set_power(1.125); cells = E.population()
    old = json.loads((F.RB/'KT39_power_curvature/mw/refine_001/results.json').read_text())
    out = dict(power=1.125,ell_kpc=3.,widths_kpc=args.widths,
        heat_steps=args.steps,refine=args.refine,rmin=args.rmin,outer=args.outer,
        coverage='Two frozen baryon witnesses, not the 1375-cell population',
        cases=[],complete=False)
    start = time.monotonic()
    for foot,index in [('canonical',1368),('alt',1287)]:
        g,mu = F.grid(foot,args.refine,args.rmin,args.outer)
        a0=M.C.A0[foot];sol=M.Solver(g,mu,a0)
        rf,_=M.rho_cell(cells[index]);rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4)
        psi=sol.LU.newton(rho)
        for width in args.widths:
            model=F.Filtered(sol,width,args.steps)
            ph,stats=model.phantom(psi,3.);total=psi+ph
            score=sol.evaluate(total)
            recomputed=M.C.lines(score['vc'],score['K'],score['K0'],score['vc_Ou'])
            assert all(score[k]==recomputed[k] for k in (*M.GATE,'Lh'))
            if width == 0 and args.refine in [2,3,4,5] and args.rmin == .005 and args.outer == 1:
                prior=next(r['score'] for r in old['rows'] if r['footing']==foot and r['power']==1.125 and r['refine']==args.refine and r['rmin']==.005 and r['outer']==1)
                assert max(abs(score[k]-prior[k])/max(abs(prior[k]),1) for k in ['vc','K0','cK','cO'])<1e-8
            if not math.isfinite(score['h']):
                assert score['h']==float('inf') and not score['Lh']
                score['h']=None;score['h_status']='nonnegative fitted log-K slope'
            gr,gt=g.grad_cells(total)
            gz=(np.cos(g.t2d)*gr-np.sin(g.t2d)*gt)*a0*M.C.PS.KPC/1e6
            at=lambda field,R,Z:float(g.interp_cells(field,np.array([R]),np.array([Z]))[0])
            gz0=at(gz,12.,.3)
            diffs=[dict(step_kpc=h,gz=(at(total,12.,.3+h)-at(total,12.,.3-h))/(2*h)*a0*M.C.PS.KPC/1e6) for h in [.005,.01,.02]]
            z=np.linspace(.02,1.5,149)
            row=dict(footing=foot,index=index,cell=cells[index],a0=a0,width_kpc=width,
                score=score,source_stats=stats,gz_R12_z03=gz0,potential_differences=diffs,
                profile_R12=dict(z_kpc=z.tolist(),gz=g.interp_cells(gz,np.full_like(z,12.),z).tolist()))
            out['cases'].append(row);save(out)
            print(foot,width,'gz',gz0,'score',{k:score[k] for k in ['vc','K0','cK','cO','all_four','Lh']},'elapsed',time.monotonic()-start,flush=True)
    out['complete']=True;out['runtime_seconds']=time.monotonic()-start;save(out)


if __name__=='__main__':main()
