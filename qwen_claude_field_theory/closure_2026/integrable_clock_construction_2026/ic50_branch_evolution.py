"""Longer IC49 evolution with interior branch checks excluding the interface.

Activation is evaluated relative to the stored initial interface q, using
log1p/expm1 and canonical deviations to avoid cancellation at the threshold.
Its initial threshold normalization error is reported separately.
"""
import json
import numpy as np
import ic49_deviation_evolution as base


class Evolution(base.Evolution):
    def evaluate(self,side,F,R,S,w,beta=None,bp=None):
        result=super().evaluate(side,F,R,S,w,beta,bp)
        if not hasattr(self,'branch'):self.branch={}
        coefficients=self.coeff[6].copy();coefficients[0]=0.
        dq=self.poly(coefficients,self.offset[side])+self.deviations[side,1]
        dw=self.metric_deviations.get(id(w),w-self.model.wc)
        exponent=2*np.log1p(dq/self.coeff[6,0])-6*dw
        self.branch[side]=.5*np.expm1(exponent)
        return result

    def rhs(self,y,time):
        flow,d=super().rhs(y,time)
        d['off_interior_max']=float(np.max(self.branch[0][:-1]))
        d['on_interior_min']=float(np.min(self.branch[1][1:]))
        d['off_interface_activation']=float(self.branch[0][-1])
        d['on_interface_activation']=float(self.branch[1][0])
        d['reference_threshold_roundoff'] = float(
            (np.exp(-3*self.model.wc)*self.coeff[6,0]/(1.5*self.model.m))**2-.5)
        return flow,d


if __name__=='__main__':
    old=base.Evolution
    try:
        base.Evolution=Evolution
        runs=[base.experiment(7,dt,steps) for dt,steps in [(4e-8,50),(2e-8,100)]]
    finally:
        base.Evolution=old
    print(json.dumps(dict(full_theory='OPEN',runs=runs,
        limitation='Finite patch, seven nodes, initial threshold used as reference; no interval arithmetic or global certificate'),indent=2))
    raise SystemExit(0 if all(r['completed'] for r in runs) else 1)
