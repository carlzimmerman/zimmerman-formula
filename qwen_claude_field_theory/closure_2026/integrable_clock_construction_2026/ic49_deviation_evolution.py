"""Evolve canonical deviations from fixed initial polynomials on the moving grid.

The grid offsets are fixed: their background has zero time derivative, so
the inherited moving-grid RHS is also the deviation RHS. No projection.
"""
import json
import numpy as np
import ic46_centered_evolution as centered
from ic47_jacobian_evolution import fixed_jacobian


class Evolution(centered.Evolution):
    def __init__(self,nodes=9,width=3e-5):
        super().__init__(nodes,width)
        self.background=self.initial[:-1].reshape(2,self.count,nodes).copy()
        self.initial[:-1]=0.
        self.current_fields=None

    def fields(self,y):
        self.deviations=y[:-1].reshape(2,self.count,self.nodes)
        self.current_fields=self.background+self.deviations
        return self.current_fields,float(y[-1])

    def derivative(self,side,value,order=1):
        if self.current_fields is not None:
            for index in range(self.count):
                target=self.current_fields[side,index]
                if (np.shares_memory(value,target) and value.shape==target.shape
                        and value.strides==target.strides
                        and value.ctypes.data==target.ctypes.data):
                    result=super().derivative(side,self.deviations[side,index],order)
                    if index<3:
                        row=(2,6,4)[index]
                        coeff=np.polynomial.polynomial.polyder(self.coeff[row],order)
                        result=result+self.poly(coeff,self.offset[side])
                    return result
        return super().derivative(side,value,order)


def experiment(nodes,dt,steps):
    e=Evolution(nodes);y=e.initial.copy();rows=[];reason='';completed=False
    with fixed_jacobian(1e-8):
        try:
            for i in range(steps+1):
                k1,d=e.rhs(y,i*dt);rows.append(d)
                if i==steps:break
                k2,_=e.rhs(y+dt*k1/2,(i+.5)*dt)
                k3,_=e.rhs(y+dt*k2/2,(i+.5)*dt)
                k4,_=e.rhs(y+dt*k3,(i+1)*dt)
                y+=dt*(k1+2*k2+2*k3+k4)/6
            completed=True
        except (ValueError,RuntimeError,np.linalg.LinAlgError) as error:
            reason=str(error)
    return dict(nodes=nodes,dt=dt,steps=steps,completed=completed,reason=reason,
                rows=rows,full_theory='OPEN',projection=False,
                scope='Same IC46 finite-patch boundaries; fixed-background canonical deviations')


if __name__=='__main__':
    runs=[experiment(*args) for args in [(7,1e-8,20),(7,5e-9,40),(9,5e-9,40)]]
    print(json.dumps(dict(runs=runs,full_theory='OPEN'),indent=2))
    raise SystemExit(0 if all(r['completed'] for r in runs) else 1)
