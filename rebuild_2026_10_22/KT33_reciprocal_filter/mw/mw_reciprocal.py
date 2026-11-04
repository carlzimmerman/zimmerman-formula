#!/usr/bin/env python3
"""Fixed-parameter MW diagnostic; import-safe. Original lanes read-only.

The Gaussian is represented on UX5's spherical finite-volume grid by even
Legendre modes. H is W-self-adjoint, d=H1, S=H diag(1/d), S*=diag(1/d)H.
The phantom map is the derivative of a discrete cell-gradient energy.
"""
import argparse
import itertools
import json
import math
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.special import eval_legendre, ive
from scipy.sparse import diags

HERE = Path(__file__).resolve().parent
RB = HERE.parents[1]
sys.path.insert(0, str(RB / "UX5_mw_stellar_mass"))
import ux5_core as C

KEYS = ("box", "sb", "mbb", "rd", "ht", "hk", "fk", "rdk")
GATE = ("L1", "L2a", "L2b", "L3")


def cells():
    """Exact KT25 iteration, before fixed original prior filter."""
    for sb, mbb, rd in itertools.product(C.L.SIG_B_GRID, C.L.MBB_GRID, C.L.RD_GRID):
        yield dict(box="B175", sb=sb, mbb=mbb, rd=rd)
    for sb, mbb, rd, ht, hk, fk in itertools.product(C.L.SIG_B_GRID, C.L.MBB_GRID, C.L.RD_GRID, (.25,.30,.35), (.72,.90,1.08), (.12,.26,.35)):
        yield dict(box="BV", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk)
    for sb, mbb, rd, ht, hk, fk in itertools.product(C.L.SIG_B_GRID, C.L.MBB_GRID, C.L.RD_GRID[2:5], (.25,.30,.35), (.72,.90,1.08), (.12,.26,.35)):
        yield dict(box="BV2", sb=sb, mbb=mbb, rd=rd, ht=ht, hk=hk, fk=fk, rdk=2.)


def rho_cell(c):
    return C.rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))


def gas_density(R,z):
    R=np.maximum(R,1e-6)
    return C.ns["S0_HI"]*np.exp(-4/R-R/7)/(4*.085)/np.cosh(np.minimum(np.abs(z)/.17,300))**2 + C.ns["S0_H2"]*np.exp(-12/R-R/1.5)/(4*.045)/np.cosh(np.minimum(np.abs(z)/.09,300))**2


def gas_mass():
    r=np.linspace(1e-4,150,300001)
    return float(np.trapz(2*np.pi*r*(C.ns["S0_HI"]*np.exp(-4/r-r/7)+C.ns["S0_H2"]*np.exp(-12/r-r/1.5)),r))


def width(c,foot):
    ms=rho_cell(c)[1]
    # Preserve KT25 constants/quantization, including its 3.0857e19 conversion.
    raw=.5*math.sqrt(4.30091e-6*(ms+gas_mass())/(C.A0[foot]*3.0857e19/1e6))
    return math.exp(round(math.log(raw)/.005)*.005)


def make_grid(a0, refine=1, outer=1):
    if refine==1 and outer==1:
        return C.grid(a0)
    mu=C.PS.mass_unit(a0)
    re=C.PS.log_edges(.005, outer*300*max(60,math.sqrt(6.6e10/mu)),30*refine)
    return C.PS.Grid(re,C.PS.theta_edges(48*refine,full=False,stretch_min=.002/refine)),mu


class Gaussian:
    """Axisymmetric fixed Gaussian with exact discrete weighted transpose.

    An orthonormalized even-Legendre quadrature preserves q0=1 exactly.
    Identity exterior closes the finite operator; no density padding is lost.
    Radius and mode refinement test this numerical boundary approximation.
    """
    def __init__(self,g,sigma,lmax=24,cut=120):
        self.g,self.sigma,self.lmax,self.cut=g,float(sigma),int(lmax),float(cut)
        self.nr=int(np.searchsorted(g.rc,cut,side="right"))
        if sigma==0:
            self.d=np.ones(self.nr)
            return
        r=g.rc[:self.nr]
        self.wr=(g.re[1:self.nr+1]**3-g.re[:self.nr]**3)/3
        wa=g.dcos
        ell=np.arange(0,min(lmax,2*(g.Nt-1))+1,2)
        P=np.stack([np.sqrt(2*l+1)*eval_legendre(l,np.cos(g.tc)) for l in ell],axis=1)
        q,_=np.linalg.qr(np.sqrt(wa)[:,None]*P)
        # Sign does not affect projection; first column is explicitly positive.
        self.q=q/np.sqrt(wa)[:,None]
        self.q[:,0]=1
        self.qa=self.q*wa[:,None]
        a=r[:,None]*r[None,:]/sigma**2
        base=(4*np.pi/(2*np.pi*sigma*sigma)**1.5)*np.exp(-(r[:,None]-r[None,:])**2/(2*sigma*sigma))*np.sqrt(np.pi/(2*a))
        self.k=np.stack([base*ive(l+.5,a) for l in ell])
        self.d=self.k[0]@self.wr
        if not np.all(self.d>0): raise RuntimeError("nonpositive Gaussian column normalization")

    def raw(self,x):
        if self.sigma==0: return np.array(x,copy=True)
        a=np.asarray(x).reshape(self.g.Nr,self.g.Nt)
        coef=a[:self.nr]@self.qa
        sm=np.einsum("lij,jl,j->il",self.k,coef,self.wr,optimize=True)
        out=a.copy()
        out[:self.nr]=sm@self.q.T
        return out.ravel()

    def forward(self,x):
        if self.sigma==0: return np.array(x,copy=True)
        a=np.array(x,copy=True).reshape(self.g.Nr,self.g.Nt)
        a[:self.nr]/=self.d[:,None]
        return self.raw(a.ravel())

    def adjoint(self,x):
        if self.sigma==0: return np.array(x,copy=True)
        a=self.raw(x).reshape(self.g.Nr,self.g.Nt)
        a[:self.nr]/=self.d[:,None]
        return a.ravel()


class Solver:
    def __init__(self,g,mu,a0):
        self.g,self.mu,self.a0=g,mu,a0
        self.LU=C.Lapl(g)
        self.filters={}

    def phantom(self,pn,mut=False):
        if mut: return np.zeros_like(pn)
        g=self.g
        dr,dt=g.grad_cells(pn)
        a=C.nu(np.hypot(dr,dt))-1
        b=-(g.Crr.T@(g.vol*a*dr)+g.Cth.T@(g.vol*a*dt))/g.vol
        return self.LU.lu.solve(b)

    def get_filter(self,sigma,lmax=24,cut=120):
        k=(float(sigma),lmax,cut)
        if k not in self.filters:
            if len(self.filters)>2: self.filters.clear()
            self.filters[k]=Gaussian(self.g,sigma,lmax,cut)
        return self.filters[k]

    def evaluate(self,p):
        g,a0=self.g,self.a0
        obs=C.ns["mw_obs"](g,p,a0)
        vo=C.L.vc_plane(C.ns,g,p,a0,C.OR)
        q=C.lines(obs["vc_R0"],obs["K"],obs["K_R0"],vo)
        q.update(K=obs["K"],vc_Ou=vo.tolist())
        q["all_four"]=all(q[k] for k in GATE)
        return q

    def solve(self,c,sigma,lmax=24,cut=120,plain=False):
        rf,ms=rho_cell(c)
        rho=self.g.rho_axisym(lambda R,z:rf(R,z)/self.mu,nq=4)
        pn=self.LU.newton(rho)
        S=self.get_filter(sigma,lmax,cut)
        rx=S.forward(rho)
        px=self.LU.newton(rx)
        ph=self.phantom(px)
        out=dict(cell=c,xi=sigma,Mstar=ms,newton=self.evaluate(pn),source_only=self.evaluate(pn+ph),corrected=self.evaluate(pn+S.adjoint(ph)),mass=dict(full_source=float(2*np.dot(self.g.vol,rho)*self.mu),full_smoothed=float(2*np.dot(self.g.vol,rx)*self.mu)))
        if plain:
            out["plain_energy"]=self.evaluate(pn+self.phantom(pn))
            out["plain_legacy"]=self.evaluate(self.LU.qumond(pn))
        return out


def legacy_module():
    """Compile only KT25 function/constant definitions, never its run blocks."""
    import ast
    p=RB/"KT25_eps_equals_kappa"/"kt25.py"
    tree=ast.parse(p.read_text(),filename=str(p))
    keep=[]
    for node in tree.body:
        if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign)):
            # Selected assignments with side effects occur only in final RES dump section.
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="sfx" for t in node.targets): continue
            keep.append(node)
    ns={"__file__":str(p),"__name__":"kt25_readonly_definitions"}
    exec(compile(ast.Module(body=keep,type_ignores=[]),str(p),"exec"),ns)
    return ns


def invariant_checks(solver,sigma=5,lmax=24,cut=120):
    g=solver.g;S=solver.get_filter(sigma,lmax,cut);w=g.vol
    r,t=g.r2d,g.t2d
    x=np.exp(-((r-8)/5)**2)*(1+.3*np.cos(2*t))
    y=np.exp(-((r-14)/7)**2)*(1-.2*np.cos(4*t))
    dot=lambda a,b:float(np.dot(w*a,b))
    rel=lambda a,b:abs(a-b)/max(abs(a),abs(b),1e-300)
    adj=rel(dot(S.forward(x),y),dot(x,S.adjoint(y)))
    mass=rel(dot(S.forward(x),np.ones(g.n)),dot(x,np.ones(g.n)))
    const=float(np.max(np.abs(S.adjoint(np.ones(g.n))-1)))
    # Independent analytic Gaussian test; density width 6 avoids unresolved cells.
    q=6.;f=np.exp(-r*r/(2*q*q));exact=(q*q/(q*q+sigma*sigma))**1.5*np.exp(-r*r/(2*(q*q+sigma*sigma)))
    region=r<30
    gauss=float(np.max(np.abs(S.forward(f)[region]-exact[region]))/np.max(exact))
    WL=diags(w)@g.Lap
    d=WL-WL.T
    lap_sym=float(np.max(np.abs(d.data))/np.max(np.abs(WL.data))) if d.nnz else 0.
    # Finite-difference nonlinear response on fixed filter; spatially asymmetric
    # within axisymmetry: even quadrupole background and distinct source modes.
    rho0=.05*np.exp(-r*r/100)*(1+.3*np.cos(2*t))
    u=np.exp(-r*r/40)*np.cos(2*t);v=np.exp(-r*r/120)*np.cos(4*t)
    u-=np.exp(-r*r/40)*dot(u,np.ones(g.n))/dot(np.exp(-r*r/40),np.ones(g.n))
    v-=np.exp(-r*r/120)*dot(v,np.ones(g.n))/dot(np.exp(-r*r/120),np.ones(g.n))
    def F(rho):
        return solver.LU.newton(rho)+S.adjoint(solver.phantom(solver.LU.newton(S.forward(rho))))
    rec=[]
    for h in (1e-4,1e-5,1e-6):
        du=(F(rho0+h*u)-F(rho0-h*u))/(2*h)
        dv=(F(rho0+h*v)-F(rho0-h*v))/(2*h)
        aa,bb=dot(v,du),dot(u,dv)
        rec.append(dict(step=h,a=aa,b=bb,relative=rel(aa,bb)))
    pn=solver.LU.newton(x)
    n1=float(np.max(np.abs(S.adjoint(solver.phantom(pn,mut=True)))))
    zi=solver.get_filter(0).adjoint(solver.phantom(pn))
    zerr=float(np.max(np.abs(zi-solver.phantom(pn))))
    gm=gas_mass();half=float(np.dot(w,g.rho_axisym(lambda R,z:gas_density(R,z)/solver.mu,nq=4))*solver.mu)
    return dict(adjoint_relative=adj,source_mass_relative=mass,outer_constant_error=const,gaussian_max_absolute_over_peak=gauss,laplacian_weighted_symmetry_relative=lap_sym,reciprocity=rec,nu_one_phantom_max=n1,xi_zero_identity_error=zerr,gas_mass=dict(analytic_full=gm,inherited_half_grid=half,inherited_ratio=half/gm,corrected_accounting_ratio=2*half/gm),interior_normalization_max=float(np.max(np.abs(S.d[g.rc[:S.nr]<50]-1))))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True)
    ap.add_argument("--mode",choices=("pilot","saved","grid","refine"),default="pilot")
    ap.add_argument("--refine",type=int,default=1)
    ap.add_argument("--outer",type=float,default=1)
    ap.add_argument("--lmax",type=int,default=24)
    ap.add_argument("--cut",type=float,default=120)
    ap.add_argument("--legacy",action="store_true")
    args=ap.parse_args();start=time.time()
    old=json.loads((RB/"KT25_eps_equals_kappa"/"kt25.json").read_text())
    out=dict(parameters=vars(args),equation="Phi=N rho + S* Phi_ph[S rho]",epsilon=.5,footings={})
    legacy=legacy_module() if args.legacy else None
    for foot,a0 in C.A0.items():
        g,mu=make_grid(a0,args.refine,args.outer);sol=Solver(g,mu,a0)
        checks=invariant_checks(sol,lmax=args.lmax,cut=args.cut)
        print(foot,"checks",json.dumps(checks),flush=True)
        saved=old[f"mw|{foot}|0.5"]["passing"]
        if args.mode=="grid":
            chosen=[c for c in cells() if C.L.RD_TAG[0]<=c["rd"]<=C.L.RD_TAG[1] and C.L.MSTAR_TAG[0]<=rho_cell(c)[1]<=C.L.MSTAR_TAG[1]]
        else:
            chosen=[{k:c[k] for k in KEYS if c.get(k) is not None} for c in saved]
            if args.mode in ("pilot","refine"): chosen=chosen[:1]
        rows=[]
        for i,c in enumerate(chosen):
            s=width(c,foot)
            row=sol.solve(c,s,args.lmax,args.cut,plain=(args.mode!="grid"))
            if legacy:
                row["legacy_source_only"]=legacy["solve"](c,s,a0,g,mu,sol.LU)["Q"]
            rows.append(row)
            if i%25==0:print(foot,i+1,"/",len(chosen),"vc",row["corrected"]["vc"],"K",row["corrected"]["K0"],"elapsed",time.time()-start,flush=True)
        summary={}
        for form in ("source_only","corrected"):
            good=[r for r in rows if r[form]["all_four"]]
            best=min(rows,key=lambda r:r[form]["D"])
            summary[form]=dict(n_pass=len(good),n_strict=sum(r[form]["Lh"] for r in good),n_share_012=sum(r["cell"].get("fk")==.12 for r in good),lines={k:sum(r[form][k] for r in rows) for k in (*GATE,"Lh")},vc_max=max(r[form]["vc"] for r in rows),best=dict(cell=best["cell"],xi=best["xi"],scores={k:best[form][k] for k in ("vc","K0","cK","cO","h","D")}))
        out["footings"][foot]=dict(grid=dict(nr=g.Nr,nt=g.Nt,outer_radius=float(g.re[-1])),checks=checks,n_tested=len(rows),summary=summary,rows=rows)
        print(foot,"summary",json.dumps(summary),flush=True)
        Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
    out["runtime_seconds"]=time.time()-start
    Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))


if __name__=="__main__": main()
