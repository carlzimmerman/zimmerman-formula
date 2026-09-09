"""Same IC46 equations, with centered auxiliary coordinates for differentiation.

The original absolute-field probe is retained for a roundoff comparison.
No canonical interface or momentum projection is introduced.
"""
import argparse
import json
import numpy as np
from scipy.optimize import root
import ic46_two_phase_evolution as original


class Evolution(original.Evolution):
    def __init__(self,nodes=9,width=3e-5):
        self.metric_deviations={}
        super().__init__(nodes,width)
        self.Sbase=self.coeff[0,0]
        self.centered_initial_S=self.coeff[0].copy();self.centered_initial_S[0]=0.
        self.guess=np.r_[self.poly(self.centered_initial_S,self.offset[0]),
                        np.zeros(nodes),self.poly(self.centered_initial_S,self.offset[1])]

    def derivative(self,side,value,order=1):
        return super().derivative(side,self.metric_deviations.get(id(value),value),order)

    def auxiliary(self,F,R,time):
        n=self.nodes;eps=self.width;wc=self.model.wc
        xs=[R+self.offset[0][0]-2,R+self.offset[1][-1]-2]
        target=[self.poly(self.centered_initial_S,x)+time*self.poly(self.coeff[8],x)
                +time*time*self.poly(self.A[i],x)/2 for i,x in enumerate(xs)]
        wtarget=time*time*self.poly(self.B,xs[0])/2
        def evaluate(g,details=False):
            sm,wm,sp=g[:n],g[n:2*n],g[2*n:]
            Sm=sm+self.Sbase;Wm=wm+wc;Sp=sp+self.Sbase;Wp=np.full(n,wc)
            self.metric_deviations={id(Sm):sm,id(Wm):wm,id(Sp):sp,id(Wp):np.zeros(n)}
            a=self.evaluate(0,F[0],R,Sm,Wm);b=self.evaluate(1,F[1],R,Sp,Wp)
            res=np.r_[eps**2*a['C'][1:-1],eps**2*a['W'][1:-1],eps**2*b['C'][1:-1],
                      sm[0]-target[0],wm[0]-wtarget,sp[-1]-target[1],sm[-1]-sp[0],
                      eps*(a['first'][0][-1]-b['first'][0][0]),wm[-1]]
            return (res,[(Sm,Wm,a),(Sp,Wp,b)]) if details else res
        self.root_calls+=1
        result=root(evaluate,self.guess,method='hybr',options=dict(xtol=1e-10,maxfev=300,eps=1e-12))
        res,states=evaluate(result.x,True);norm=float(np.max(abs(res)))
        if not np.isfinite(norm) or norm>2e-12:
            raise RuntimeError(f'Centered auxiliary solve residual {norm:.6g}: {result.message}')
        self.guess=result.x.copy()
        return states,norm


def experiment(nodes=9,width=3e-5,dt=1e-8,steps=4):
    e=Evolution(nodes,width);y=e.initial.copy();rows=[];i=0
    try:
        for i in range(steps+1):
            k1,diag=e.rhs(y,i*dt);rows.append(diag)
            if i==steps:break
            k2,_=e.rhs(y+dt*k1/2,(i+.5)*dt)
            k3,_=e.rhs(y+dt*k2/2,(i+.5)*dt)
            k4,_=e.rhs(y+dt*k3,(i+1)*dt)
            y+=dt*(k1+2*k2+2*k3+k4)/6
        completed=True;reason=''
    except (ValueError,RuntimeError,np.linalg.LinAlgError) as error:
        completed=False;reason=str(error)
    return dict(completed=completed,reason=reason,completed_steps=i,nodes=nodes,width=width,dt=dt,requested_steps=steps,
        rhs_calls=e.calls,auxiliary_solves=e.root_calls,rows=rows,final_state=y.tolist(),
        junction_projected=False,momentum_projected=False,full_theory='OPEN',auxiliary_coordinates='centered',
        scope='Same finite-patch boundary prescription as absolute-field control; no global closure or long-time stability certificate')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--nodes',type=int,default=9);p.add_argument('--width',type=float,default=3e-5)
    p.add_argument('--dt',type=float,default=1e-8);p.add_argument('--steps',type=int,default=4);p.add_argument('--strict',action='store_true')
    a=vars(p.parse_args());strict=a.pop('strict');result=experiment(**a)
    print(json.dumps(result,indent=2));raise SystemExit(2 if strict else 0 if result['completed'] else 1)
