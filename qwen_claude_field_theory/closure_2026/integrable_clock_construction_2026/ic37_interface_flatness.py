"""Finite multiplier acceleration requires interface flatness, not smallness."""
import argparse
import json
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import ic36_second_preservation as previous
import ic37_analytic_second_jet as analytic


def identities():
    tau,r,r0,velocity,acceleration=s.symbols('tau r r0 velocity acceleration',real=True)
    F=s.Function('F');W=tau*tau*F(r)/2
    moving=W.subs(r,r0+velocity*tau+acceleration*tau*tau/2)
    eta,S=s.Function('eta'),s.Function('S');ell2=s.Symbol('ell2',real=True)
    product=eta(tau)*s.exp(S(tau))*tau*tau*ell2/2
    x,p=s.symbols('x p',positive=True)
    a=s.exp(-1/x);b=s.exp(-1/(s.Rational(1,4)-x));switch=a/(a+b)
    return {'moving_interface_second_jet':s.simplify(s.diff(moving,tau,2).subs(tau,0)-F(r0)),
            'multiplier_second_jet':s.simplify(s.diff(product,tau,2).subs(tau,0)-eta(0)*s.exp(S(0))*ell2),
            'reciprocal_activation':s.simplify((1/switch-1-s.exp(1/x-1/(s.Rational(1,4)-x))).replace(
                s.exp,lambda argument:s.exp(s.factor(argument)))),
            'faster_than_any_positive_power':s.limit(switch/x**p,x,0,dir='+')}


def flat_counterexample():
    x,p=s.symbols('x p',positive=True)
    switch=s.exp(-1/x)/(s.exp(-1/x)+s.exp(-1/(s.Rational(1,4)-x)))
    source=s.exp(-1/(2*x))
    return dict(all_power_flat_limit=s.limit(source/x**p,x,0,dir='+'),
                response_limit=s.limit(source/switch,x,0,dir='+'))


def edge_compatibility(r,C,W,FC,FW,degree):
    lo,hi=float(r[0]),float(r[-1]);length=hi-lo
    polys=[previous.fit(r,x,degree) for x in (*C.T,FC)]
    def rhs(x,y):
        a,b,c,f=(p(x) for p in polys);Y=y.reshape(2,3)
        return np.array([Y[1],-(a*Y[0]+b*Y[1]+np.array([f,0.,0.]))/c]).ravel()
    initial=np.array([[0.,1.,0.],[0.,0.,1/length]]).ravel()
    sol=solve_ivp(rhs,(lo,hi),initial,method='DOP853',rtol=2e-12,atol=2e-13,
                  max_step=length/100,dense_output=True)
    if not sol.success:raise RuntimeError('Lapse-acceleration fundamental system failed')
    A,A1=sol.sol(r).reshape(2,3,len(r))
    A2=-(C[:,0]*A+C[:,1]*A1+np.array([FC,np.zeros_like(FC),np.zeros_like(FC)]))/C[:,2]
    response=(W[:,0]*A+W[:,1]*A1+W[:,2]*A2).T
    response[:,0]+=FW
    polynomials=[previous.fit(r,x,degree) for x in response.T]
    matrix=np.array([[p(lo) for p in polynomials[1:]],
                     [length*p.deriv()(lo) for p in polynomials[1:]]])
    target=-np.array([polynomials[0](lo),length*polynomials[0].deriv()(lo)])
    scale=np.linalg.norm(matrix,axis=0);scale=np.where(scale==0,1.,scale)
    normalized=matrix/scale
    constants,_,rank,sv=np.linalg.lstsq(normalized,target,rcond=1e-11);constants=constants/scale
    residue=polynomials[0]+sum(c*p for c,p in zip(constants,polynomials[1:]))
    nodal=response[:,0]+response[:,1:]@constants
    return dict(edge_jets=[float(residue.deriv(n)(lo)) for n in range(5)],
        scaled_edge_jets=[float(residue.deriv(n)(lo)*length**n) for n in range(5)],
        edge_matrix=matrix.tolist(),edge_matrix_determinant=float(np.linalg.det(matrix)),
        edge_rank=int(rank),normalized_singular_values=sv.tolist(),constants=constants.tolist(),
        max_W_second_residual=float(np.max(abs(nodal))),
        response_fit_error=float(np.max(abs(nodal-residue(r)))),
        interval=[lo,hi],degree=degree,nodes=len(r),full_theory='OPEN')


def experiment(U1=0.,degree=10,nodes=65,length=.0015,first=None):
    first=previous.FirstJet(U1=U1) if first is None else first
    data=analytic.sources(first,degree,nodes,(2.,2.+length))
    out=edge_compatibility(*(data[k] for k in ('r','C','W','FC','FW')),degree)
    q=data['v']['q'];m=first.c.model
    alpha2=(-np.exp(-3*m.wc)*q/(3*m.m*.5))**2
    S0=float(data['v']['S'][0]);cell=int(np.searchsorted(m.table.x,S0,side='right')-1)
    return dict(U1=U1,flow_disagreement=data['flow_disagreement'],
        constraint_disagreement=data['constraint_disagreement'],coefficient_cells=data['coefficient_cells'],
        activation_square_range=[float(np.min(alpha2)),float(np.max(alpha2))],
        S_interface=S0,interface_coefficient_cell=cell,
        interface_coefficient_margin=float(min(S0-m.table.x[cell],m.table.x[cell+1]-S0)),
        single_cell_audit=len(data['coefficient_cells'])==1,
        source_scale=float(max(np.max(abs(data['FC'])),np.max(abs(data['FW'])))),**out)


def main():
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');p.add_argument('--quick',action='store_true')
    args=p.parse_args();rows=[]
    for U1 in (0.,-2.6400382455715268):
        first=previous.FirstJet(U1=U1)
        cases=[(10,.0015)] if args.quick else [(10,.003),(8,.0015),(12,.0015),(16,.0015),(12,.002),(12,.001)]
        rows.extend(experiment(U1,d,65,length,first) for d,length in cases)
    roots=[]
    if not args.quick:
        for bracket in ((-10.,0.),(0.,10.)):
            history=[]
            def target(U1):
                value=experiment(U1,10,49)['edge_jets'][2]
                history.append(dict(U1=float(U1),curvature=value));return value
            ends=[target(U1) for U1 in bracket]
            if ends[0]*ends[1]>=0:
                roots.append(dict(bracket=bracket,bracketed=False,history=history));continue
            root=brentq(target,*bracket,xtol=1e-6,rtol=1e-10,maxiter=32)
            first=previous.FirstJet(U1=root)
            audit=[experiment(root,d,97,length,first) for d,length in ((8,.0015),(12,.0015),(16,.0015),(12,.002),(12,.001))]
            roots.append(dict(bracket=bracket,bracketed=True,U1=float(root),history=history,audits=audit))
    checks={k:v==0 for k,v in identities().items()}
    checks['flatness_counterexample']=flat_counterexample()['response_limit']==s.oo
    checks['same_action_sources']=all(x['flow_disagreement']<1e-9 and x['constraint_disagreement']<1e-9 for x in rows)
    print(json.dumps(dict(checks=checks,rows=rows,roots=roots,full_theory='OPEN'),indent=2))
    return 1 if not all(checks.values()) else 2 if args.strict else 0


if __name__=='__main__':raise SystemExit(main())
