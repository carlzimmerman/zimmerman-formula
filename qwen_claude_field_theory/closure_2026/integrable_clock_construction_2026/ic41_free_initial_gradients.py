"""IC39 action unchanged: select initial gradients through third-time constraints.

Uses IC40's independent canonical time engine, not IC37's fixed-gradient
second-source evaluator. No action coefficient, kernel, or empirical input fits.
"""
import argparse
from functools import partial
import json
from pathlib import Path
import mpmath as mp
import ic37_local_taylor as local
import ic40_third_preservation as third


class FreeTimeJet(third.TimeJet):
    def __init__(self,U0,U1,order,extra=0,qprime='-100',Sprime='0'):
        self.model=local.LocalJet(U0,U1);m=self.model
        m.initial[7]=mp.mpf(qprime);m.initial[1]=mp.mpf(Sprime)
        if m.initial[7]>=0:raise ValueError('This chart requires x_r>0, hence qprime<0')
        self.order=order;self.degree=order+6+extra;self.nf=len(m.fluids)
        self.Y=local.ode_series(m.rhs,m.r0,m.initial,self.degree)
        zero=lambda:[mp.mpf(0)]*(self.degree+1)
        self.T=[[zero() for _ in range(5+2*self.nf)] for _ in range(4)]
        for field,index in enumerate((0,2,6,4,5)):self.T[0][field]=self.Y[index]
        for i,f in enumerate(m.fluids):self.T[0][5+i][0]=f['j']
        self.T[1][0]=self.Y[8]

    def step(self,n):
        def rhs(x):
            return [v/mp.factorial(n) for v in local.vector_derivative(lambda t:self.physical(x,t),n)]
        rows=local.series(rhs,self.degree)
        for i,row in enumerate(rows):
            if i not in (0,4):self.T[n+1][i]=[v/(n+1) for v in row]

    def evolve(self):
        self.step(0);self.shift(1);self.step(1)
        # Q_tt,q_tt,sh_tt and matter tt depend on S_t, not on S_tt.
        # Thus S_tt=0 yields the inhomogeneous second-constraint source.
        n=self.degree-2;m=self.model
        def coefficients(x):
            point=m.details(m.r0+x,[local.polynomial(row,x) for row in self.Y])
            return [*point['C'],*point['W']]
        coeff=local.series(coefficients,n);self.C,self.W=coeff[:3],coeff[3:]
        source=local.series(lambda x:local.vector_derivative(lambda t:self.constraints(x,t),2),n)
        self.FC,self.FW=source[:2]
        boundary=local.boundary_from_coefficients(self.C,self.W,self.FC,self.FW,n)
        A0,A1=boundary['constants']
        def lapse(x,y):
            return [y[1],-(local.polynomial(self.C[0],x)*y[0]+local.polynomial(self.C[1],x)*y[1]
                           +local.polynomial(self.FC,x))/local.polynomial(self.C[2],x)]
        acc=local.ode_series(lapse,mp.mpf(0),[A0,A1],self.degree)[0]
        self.T[2][0]=[v/2 for v in acc]
        self.shift(2);self.step(2)
        fmt=lambda v:mp.nstr(v,mp.mp.dps)
        self.reference=dict(edge_jets=[fmt(v) for v in boundary['edge_jets']],
            activation_radial_derivative=fmt(m.initial[7]/m.initial[6]))


def field_result(U0='0',U1='0',qprime='-100',Sprime='0',dps=40,order=3,extra=0):
    out=third.field_result(U0,U1,dps,order,extra,
            engine_factory=partial(FreeTimeJet,qprime=qprime,Sprime=Sprime))
    with mp.workdps(dps):
        m=local.LocalJet(U0,U1)
        out.update(qprime=str(qprime),Sprime=str(Sprime),
            activation_radial_derivative=mp.nstr(mp.mpf(qprime)/m.initial[6],dps-12),
            second_source_method='independent canonical time engine; residual is internal consistency')
    return out


def condition_vector(out):
    return [mp.mpf(v) for v in out['second_gate_jets'][2:4]+out['motion_corrected_third_jets'][2:4]]


def search(branch=0,dps=35,max_evaluations=40):
    import numpy as np
    from scipy.optimize import least_squares
    previous=json.loads((Path(__file__).parent/'ic37_run_001/local/stdout.txt').read_text())['joint'][branch]
    initial=np.array([float(previous['U0']),float(previous['U1']),0.,0.])
    # Bounds define this search, not an exclusion of all other initial data.
    scales=np.array([1e7,1e10,1e9,1e12]);evaluations=[];cache={}
    class Budget(Exception):pass
    def evaluate(x):
        key=tuple(x)
        if key in cache:return cache[key]
        if len(evaluations)>=max_evaluations:raise Budget()
        out=field_result(U0=repr(x[0]),U1=repr(x[1]),qprime=repr(-100*np.exp(x[2])),
                         Sprime=repr(x[3]),dps=dps,order=3)
        values=np.array([float(v) for v in condition_vector(out)])/scales
        record=dict(evaluation=len(evaluations)+1,coordinates=x.tolist(),result=out,
                    scaled_conditions=values.tolist(),norm=float(np.linalg.norm(values)))
        evaluations.append(record);cache[key]=values
        print(json.dumps(dict(event='evaluation',**record)),flush=True)
        return values
    result=None;message=''
    try:
        result=least_squares(evaluate,initial,bounds=([-2,-100,-np.log(4),-10],[2,100,np.log(4),10]),
            diff_step=1e-4,xtol=1e-11,ftol=1e-11,gtol=1e-11,x_scale='jac',max_nfev=max_evaluations)
        message=result.message
    except Budget:message='Explicit evaluation budget reached; no universal exclusion'
    best=min(evaluations,key=lambda row:row['norm'])
    return dict(event='summary',branch=branch,evaluations=len(evaluations),best=best,
                solver_success=bool(result.success) if result is not None else False,message=str(message),
                full_theory='OPEN',non_claim='No exact root, global solution, or full Dirac closure certified')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name,default in [('U0','0'),('U1','0'),('qprime','-100'),('Sprime','0')]:p.add_argument('--'+name,default=default)
    p.add_argument('--dps',type=int,default=40);p.add_argument('--order',type=int,default=3)
    p.add_argument('--extra',type=int,default=0);p.add_argument('--strict',action='store_true')
    p.add_argument('--search',action='store_true');p.add_argument('--branch',type=int,default=0,choices=[0,1])
    p.add_argument('--max-evaluations',type=int,default=40)
    args=vars(p.parse_args());strict=args.pop('strict');do_search=args.pop('search')
    branch=args.pop('branch');budget=args.pop('max_evaluations')
    out=search(branch,args['dps'],budget) if do_search else field_result(**args)
    print(json.dumps(out,indent=2));raise SystemExit(2 if strict else 0)
