"""Bounded variational and analytic-Hessian controls before physical grading."""
import argparse,json,math,time
from pathlib import Path
import generalized as J
M,E,L,np=J.M,J.E,J.L,J.np


def spherical_formula(r,ell,mass=1.,a=2.):
    def terms(rr):
        q=mass*rr/(rr*rr+a*a)**1.5
        qp=mass*(a*a-2*rr*rr)/(rr*rr+a*a)**2.5
        gg=np.array([q,np.zeros_like(q)])
        hh=np.array([qp,np.zeros_like(q),q/rr,q/rr])
        aa,bb,_,_=J.Generalized.coefficients(gg,hh,ell)
        return aa[0],bb[0],bb[2]
    aa,br,bt=terms(r)
    step=1e-4*r
    derivative=(terms(r+step)[1]-terms(r-step)[1])/(2*step)
    return aa-derivative-2*(br-bt)/r


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();start=time.monotonic()
    g,mu=M.make_grid(M.C.A0['canonical'],1,1);sol=M.Solver(g,mu,M.C.A0['canonical']);model=J.Generalized(sol)
    out=dict(contract='Finite discrete action invariants and continuum spherical controls',checks={},spherical=[],variational=[],all_checks_pass=False)
    def checkpoint():
        args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    rr,tt=g.r2d,g.t2d;ir=np.arange(g.n)//g.Nt;j=np.arange(g.n)%g.Nt
    interior=(ir>=2)&(ir<g.Nr-2)&(j>=2)&(j<g.Nt-2)
    radial=(ir>=2)&(ir<g.Nr-2)
    for label,potential,exact in [
        ('radial_quadratic',.5*rr**2,np.array([np.ones(g.n),np.zeros(g.n),np.ones(g.n),np.ones(g.n)])),
        ('axial_quadratic',.5*rr**2*np.cos(tt)**2,np.array([np.cos(tt)**2,-np.sin(tt)*np.cos(tt),np.sin(tt)**2,np.zeros(g.n)]))]:
        actual=model.fields(potential)[1]
        err=actual-exact
        row=dict(max_interior_error=float(np.max(abs(err[:,interior]))),max_polar_boundary_error=float(np.max(abs(err[:,radial&((j==0)|(j==g.Nt-1))]))))
        out['checks'][label]=row
        checkpoint();print(label,row,flush=True)
        assert row['max_interior_error']<.03 and row['max_polar_boundary_error']<.08
    base=.05*np.exp(-rr*rr/100)
    rho=base*(1+.2*np.cos(2*tt))
    u=base*np.cos(2*tt);v=base*np.cos(4*tt)
    for q in (u,v):q-=base*float(g.vol@q)/float(g.vol@base)
    psi=sol.LU.newton(rho)
    zero,st=model.phantom(psi,1.,newtonian=True)
    assert np.array_equal(zero,np.zeros_like(zero))
    out['checks']['newtonian_zero']=True
    ph0,_=model.phantom(psi,0.)
    plain=sol.phantom(psi)
    err=float(np.max(abs(ph0-plain))/np.max(abs(plain)))
    out['checks']['ell_zero_plain_relative']=err;assert err<1e-10
    checkpoint()
    for ell in (.1,1.):
        ph,stats=model.phantom(psi,ell)
        target=float(g.vol@(u*ph))
        rows=[]
        for h in (1e-3,1e-4,1e-5):
            ep=model.energy(rho+h*u,ell);em=model.energy(rho-h*u,ell)
            fd=(ep-em)/(2*h)
            fu=(model.response(rho+h*u,ell)[0]-model.response(rho-h*u,ell)[0])/(2*h)
            fv=(model.response(rho+h*v,ell)[0]-model.response(rho-h*v,ell)[0])/(2*h)
            left=float(g.vol@(v*fu));right=float(g.vol@(u*fv))
            rows.append(dict(step=h,energy_fd=fd,energy_target=target,energy_relative=abs(fd-target)/max(abs(target),1e-15),
                reciprocity_left=left,reciprocity_right=right,reciprocity_relative=abs(left-right)/max(abs(left),abs(right),1e-15)))
        assert min(r['energy_relative'] for r in rows)<2e-5
        assert min(r['reciprocity_relative'] for r in rows)<2e-5
        out['variational'].append(dict(ell_kpc=ell,source_stats=stats,steps=rows))
        checkpoint();print('variational',ell,rows,flush=True)
    for perdecade in (30,60,120):
        re=M.C.PS.log_edges(.002,200.,perdecade)
        sg=M.C.PS.Grid(re,np.array([0.,math.pi/2]));ss=M.Solver(sg,1.,1.);sm=J.Generalized(ss)
        r=sg.r2d;psi=-1/np.sqrt(r*r+4)
        gg,hh=sm.fields(psi)
        q=r/(r*r+4)**1.5;qp=(4-2*r*r)/(r*r+4)**2.5
        exact=np.array([qp,np.zeros_like(q),q/r,q/r]);region=(r>.05)&(r<20)
        herr=float(np.max(abs(hh[:,region]-exact[:,region]))/np.max(abs(exact[:,region])))
        for ell in (0.,.1,1.):
            ph,stats=sm.phantom(psi,ell)
            actual=sg.Crr@ph;expected=spherical_formula(r,ell)
            er=float(np.max(abs(actual[region]-expected[region]))/np.max(abs(expected[region])))
            out['spherical'].append(dict(per_decade=perdecade,ell_kpc=ell,hessian_relative_error=herr,phantom_force_relative_error=er))
            checkpoint();print('spherical',out['spherical'][-1],flush=True)
    for ell in (0.,.1,1.):
        rows=[x for x in out['spherical'] if x['ell_kpc']==ell]
        assert rows[-1]['phantom_force_relative_error']<.03
        assert rows[-1]['hessian_relative_error']<.01
        assert rows[-1]['phantom_force_relative_error']<rows[0]['phantom_force_relative_error']
    out['all_checks_pass']=True;out['runtime_seconds']=time.monotonic()-start
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
