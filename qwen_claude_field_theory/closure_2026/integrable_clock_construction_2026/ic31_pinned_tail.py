"""Solve the IC29 nonlinear pinned exterior constraints, not a full galaxy.

One fixed coefficient table per approximate action, varied source amplitude.
Independent full radial EL expressions are imported from IC30.
"""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from scipy.linalg import eigh_tridiagonal
import ic29_slow_clock as history
import ic30_radial_bridge as radial


@lru_cache(None)
def symbolic():
    d=radial.radial_action(); r=d['r']
    S,w,Q,q,z,sh,beta,ell=d['fields']
    eq=radial.radial_equations()
    Qc=s.Symbol('Qc',real=True)
    pin={w:d['wc'],Q:Qc,beta:0}
    def pinned(expr):
        return s.simplify(expr.subs(d['eta'],1).doit().subs(pin).doit())
    C=pinned(-eq['S']/d['J'])
    W=pinned(eq['w']/d['J'])
    Wcoef=s.diff(W,ell); W=W.subs(ell,0)
    v=d['v'].subs(w,d['wc']); t=d['t'].subs(w,d['wc'])
    u=d['u'].subs(w,d['wc']); B=2*v*(1-u*u)
    h=-t*q*q/6-d['A']*q*z-s.exp(S)*d['P0'].subs(w,d['wc'])
    h-=d['D']*z*z+d['E4']*z**4
    hS=s.diff(h,S); hSS=s.diff(h,S,2); hSz=s.diff(h,S,z); hzz=s.diff(h,z,2)
    predicted=hS+2*t*sh*sh/3+s.exp(-2*Qc)*(s.diff(B,S)*s.diff(S,r)**2
                   +2*B*(s.diff(S,r,2)+2*s.diff(S,r)/r))
    checks={'pinned_lapse':s.simplify(C-predicted),
            'ell_coefficient':s.simplify(Wcoef-s.exp(S)),
            'radial_principal':s.simplify(s.diff(C,s.diff(S,r,2))-2*B*s.exp(-2*Qc))}
    principal=2*B*s.exp(-2*Qc)
    potential=hSS-hSz**2/hzz+2*t*sh**2/3+s.exp(-2*Qc)*(
        2*s.diff(B,S)*(s.diff(S,r,2)+2*s.diff(S,r)/r)+s.diff(B,S,2)*s.diff(S,r)**2)
    checks['eliminated_lapse_potential']=s.simplify(s.diff(C,S)-s.diff(C,z)*hSz/hzz-potential)
    checks['self_adjoint_radial_form']=s.simplify(s.diff(C,s.diff(S,r))
                                        -2*principal/r-s.diff(principal,S)*s.diff(S,r))
    # Ordinary fluid Hamiltonian's off-pin w derivative, not total-stress conservation.
    wi,ww,wc,hh=s.symbols('wi ww wc hh',real=True)
    hm=hh*s.exp((1-3*wi)*(ww-wc))
    checks['matter_w_source']=s.simplify(s.diff(hm,ww).subs(ww,wc)-(1-3*wi)*hh)
    funcs=(d['A'],d['D'],d['E4'])
    A,D,D1,D2,E=s.symbols('A D D1 D2 E',real=True)
    jets={funcs[0]:A,s.diff(funcs[0],S):0,s.diff(funcs[0],S,2):0,
          funcs[1]:D,s.diff(funcs[1],S):D1,s.diff(funcs[1],S,2):D2,
          funcs[2]:E,s.diff(funcs[2],S):0,s.diff(funcs[2],S,2):0}
    Sv,S1,S2,qv,zv,sv=s.symbols('Sv S1 S2 qv zv sv',real=True)
    fields={S:Sv,s.diff(S,r):S1,s.diff(S,r,2):S2,q:qv,z:zv,sh:sv}
    keys=('C','W','Wcoef','a','hSS','hSz','hzz','B','B1','B2','t')
    values=(C,W,Wcoef,s.diff(C,s.diff(S,r,2)),hSS,hSz,hzz,B,s.diff(B,S),s.diff(B,S,2),t)
    values=[s.simplify(v.subs(jets,simultaneous=True).subs(fields,simultaneous=True)) for v in values]
    args=(r,Sv,S1,S2,qv,zv,sv,Qc,d['wc'],d['m'],d['a02'],d['lam'],d['kappa'],A,D,D1,D2,E)
    fn=s.lambdify(args,values,'numpy',cse=True)
    return checks,keys,fn


def identities():
    return symbolic()[0]


class Model:
    def __init__(self,reference,table):
        self.table=table
        self.Q=float(reference['Q']); self.q=float(reference['q'])
        self.Sref=float(reference['S'])
        self.A=float(reference['parameters']['A0']); self.E=float(reference['parameters']['E40'])
        self.rho_ref=float(mp.fsum(f['h'] for f in reference['entries']))
        self.pw_ref=float(mp.fsum((1-3*f['w'])*f['h'] for f in reference['entries']))
        c=history.base.old.normalized.constants()
        self.wc=float(c['wc']); self.lam=float(c['Lambda']); self.a02=float(c['a02'])
        self.m=1.; self.kappa=6.
        self.charge=float(radial.collar_construction()['charge'])*(-self.q)
        self.keys,self.fn=symbolic()[1:]
        # Actual fixed-table homogeneous constraint, not imposed target M.
        def baseline(S):return float(self.evaluate(2.,S,0.,0.,0.)['C'])
        self.Sbar=brentq(baseline,self.Sref-1e-6,self.Sref+1e-6,xtol=1e-15)

    def evaluate(self,r,S,Sp,Spp,amplitude):
        r,S,Sp,Spp=np.broadcast_arrays(r,S,Sp,Spp)
        if np.min(S)<self.table.x[0] or np.max(S)>self.table.x[-1]:
            raise ValueError('Constraint iterate leaves the fixed coefficient domain')
        D,D1,D2=(self.table(S,nu=j) for j in range(3))
        if np.min(D)<=0:raise ValueError('Auxiliary branch requires positive D')
        z=2*np.sqrt(D/(6*self.E))*np.sinh(np.arcsinh(
            -3*self.A*self.q*np.sqrt(6*self.E/D)/(4*D))/3)
        shear=amplitude*self.charge/r**3
        vals=self.fn(r,S,Sp,Spp,self.q,z,shear,self.Q,self.wc,self.m,
                     self.a02,self.lam,self.kappa,self.A,D,D1,D2,self.E)
        out={key:np.broadcast_to(value,S.shape) for key,value in zip(self.keys,vals)}
        rho=self.rho_ref*np.exp(S-self.Sref); pw=self.pw_ref*np.exp(S-self.Sref)
        out['C']=out['C']+rho; out['W']=out['W']-pw
        out.update(z=z,shear=shear,D=D,rho=rho,z_residual=self.A*self.q+2*D*z+4*self.E*z**3)
        out['potential']=out['hSS']-out['hSz']**2/out['hzz']+rho+2*out['t']*shear**2/3
        out['potential']+=np.exp(-2*self.Q)*(2*out['B1']*(Spp+2*Sp/r)+out['B2']*Sp**2)
        return out


@lru_cache(None)
def models():
    h=history.evolve(1,max_step=.005,pin_h0='.5',rtol=1e-12)
    if not h['success']:raise RuntimeError(h['reason'])
    with mp.workdps(40):
        b=history.state_at(h,.1)
        return tuple(Model(b,history.coefficient_table(h,n)) for n in (41,81))


def solve(model,amplitude=1.,nodes=201,rmax=8.,tol=1e-9):
    radii=np.linspace(2.,rmax,nodes)
    def rhs(r,y):
        state=model.evaluate(r,y[0],y[1],0.,amplitude)
        return np.vstack((y[1],-state['C']/state['a']))
    def bc(left,right):return np.array([left[1],right[0]-model.Sbar])
    solution=solve_bvp(rhs,bc,radii,np.vstack((np.full(nodes,model.Sbar),np.zeros(nodes))),
                       tol=tol,max_nodes=12000)
    if not solution.success:
        return dict(success=False,message=solution.message,nodes=solution.x.size)
    grid=np.linspace(2.,rmax,2001)
    # Integrate the represented slope so S'=Sp is exact for the reported field.
    anti=solution.sol.antiderivative()
    S=model.Sbar+anti(grid)[1]-anti(rmax)[1]
    Sp=solution.sol(grid)[1]; Spp=solution.sol(grid,1)[1]
    state=model.evaluate(grid,S,Sp,Spp,amplitude)
    ell=-state['W']/state['Wcoef']
    wres=state['W']+state['Wcoef']*ell
    pin_margin=(-np.exp(-3*model.wc)*model.q/(3*.5))**2-.75
    # Solve shear gauge condition with actual variable t, not the constant-t formula.
    # beta/r = - integral_2^r t*s/r dr, fixing only the residual shift convention.
    integrand=state['t']*state['shear']/grid
    shift_integrand=CubicSpline(grid,integrand)
    shift_anti=shift_integrand.antiderivative()
    beta=-grid*(shift_anti(grid)-shift_anti(2.))
    betaprime=beta/grid-grid*shift_integrand(grid)
    Qdot=(betaprime+2*beta/grid)/3-state['t']*model.q/6-model.A*state['z']/2
    displacement=S-model.Sbar
    # Actual finite-volume linearized constraint operator, symmetrized in
    # the r^2 dr measure. Inner Neumann and outer Dirichlet boundary conditions.
    eigenvalues=[]
    def field(points):
        return (model.Sbar+anti(points)[1]-anti(rmax)[1],
                solution.sol(points)[1],solution.sol(points,1)[1])
    mid=(grid[:-1]+grid[1:])/2
    midstate=model.evaluate(mid,*field(mid),amplitude)
    shift_residual=midstate['t']*midstate['shear']-mid*shift_integrand(mid)
    for count in (128,256):
        edges=np.linspace(2.,rmax,count+1); width=edges[1]-edges[0]
        centers=(edges[:-1]+edges[1:])/2
        center_state=model.evaluate(centers,*field(centers),amplitude)
        edge_state=model.evaluate(edges,*field(edges),amplitude)
        flux=edges**2*edge_state['a']
        left=flux[:-1].copy(); right=flux[1:].copy()
        left[0]=0.; right[-1]*=2.  # half-cell distance to the Dirichlet boundary
        diagonal=center_state['potential']-(left+right)/(centers**2*width**2)
        off=flux[1:-1]/(width**2*centers[:-1]*centers[1:])
        eigenvalues.append(float(eigh_tridiagonal(diagonal,off,eigvals_only=True,
                                select='i',select_range=(count-1,count-1))[0]))
    report=dict(success=True,amplitude=amplitude,rmax=rmax,initial_nodes=nodes,
        final_nodes=solution.x.size,tolerance=tol,Sbar=model.Sbar,q=model.q,Q=model.Q,
        coefficient_domain=list(model.table.x[[0,-1]]),
        min_S=float(np.min(S)),max_S=float(np.max(S)),min_D=float(np.min(state['D'])),
        max_lapse_displacement=float(np.max(abs(displacement))),
        max_lapse_residual=float(np.max(abs(state['C']))),
        max_z_residual=float(np.max(abs(state['z_residual']))),
        max_w_residual=float(np.max(abs(wres))),min_pin_margin=float(pin_margin),
        max_shift_residual=float(np.max(abs(shift_residual))),
        max_ell=float(np.max(abs(ell))),min_ell=float(np.min(ell)),
        min_radial_principal=float(np.min(state['a'])),
        max_linearized_potential=float(np.max(state['potential'])),
        constraint_jacobian_largest_eigenvalue=eigenvalues[-1],
        constraint_jacobian_grids=eigenvalues,
        representation_difference=float(np.max(abs(S-solution.sol(grid)[0]))),
        boundary_residuals=[float(Sp[0]),float(S[-1]-model.Sbar)],
        min_coordinate_Qdot=float(np.min(Qdot)),
        # The physical normal expansion equals exp(-S-wc)*(3Qdot-div beta)
        # on this pinned slice, independent of the arbitrary shift integration constant.
        min_physical_H=float(np.min(np.exp(-S-model.wc)*(-state['t']*model.q/6-model.A*state['z']/2))),
        samples=[dict(r=float(grid[i]),S=float(S[i]),Sp=float(Sp[i]),z=float(state['z'][i]),
                      shear=float(state['shear'][i]),ell=float(ell[i])) for i in (0,100,500,1000,2000)],
        nonclaim='Finite pinned initial exterior constraints; not evolved or joined to an unpinned galaxy')
    return report


def report():
    ms=models(); rows=[]
    for amp in (0.,.5,1.,2.):
        rows.append(dict(amplitude=amp,coarse=solve(ms[0],amp,121),fine=solve(ms[1],amp,241)))
    longer=solve(ms[1],1.,241,rmax=12.)
    checks=dict(symbolic=all(x==0 for x in identities().values()),
        solved=all(x[k]['success'] for x in rows for k in ('coarse','fine')) and longer['success'])
    if checks['solved']:
        allrows=[x[k] for x in rows for k in ('coarse','fine')]+[longer]
        checks.update(lapse_residual=all(x['max_lapse_residual']<1e-7 for x in allrows),
            auxiliary_residual=all(x['max_z_residual']<1e-10 and x['max_w_residual']<1e-8 for x in allrows),
            shift_residual=all(x['max_shift_residual']<1e-7 for x in allrows),
            positive_domain=all(x['min_D']>0 and x['min_pin_margin']>0 and x['min_radial_principal']>0 for x in allrows),
            sampled_negative_potential=all(x['max_linearized_potential']<0 for x in allrows),
            radial_constraint_matrix=all(x['constraint_jacobian_largest_eigenvalue']<0 for x in allrows),
            expanding_slice=all(x['min_physical_H']>0 for x in allrows),
            fixed_grid_agreement=all(abs(x['coarse']['max_S']-x['fine']['max_S'])<1e-8 for x in rows))
    return dict(full_theory='OPEN',checks=checks,rows=rows,longer_exterior=longer)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--strict',action='store_true')
    args=parser.parse_args();out=report();print(json.dumps(out,indent=2))
    raise SystemExit(1 if not all(out['checks'].values()) else 2 if args.strict else 0)
