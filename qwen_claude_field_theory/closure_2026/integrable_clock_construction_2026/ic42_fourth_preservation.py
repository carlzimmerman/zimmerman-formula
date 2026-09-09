"""Fourth-time gate of the unchanged IC39 action on the IC41 selected data."""
import argparse
from functools import lru_cache
import json
import mpmath as mp
import sympy as s
import ic37_local_taylor as local
from ic41_free_initial_gradients import FreeTimeJet
from ic41_response_limit import read_summary


@lru_cache(None)
def identities():
    v,k,C,n,j,w=s.symbols('v k C n j w',positive=True)
    P=C*(v*v-k)**n;momentum=s.diff(P,v)
    vk=-s.diff(momentum,k)/s.diff(momentum,v)
    Hkk=(-j*vk/(2*v*v)).subs(k,0).subs(n,(1+w)/(2*w))
    h4=-(1-w)*j/(8*((1+w)*C*j**w)**3)
    trace=3*j*s.diff(h4,j)-4*h4+4*h4
    t=s.Symbol('t');A=s.Function('A')(t);L,M,B=s.symbols('L M B')
    pin=A*(L*t*t/2+M*t**3/6+B*t**4/24)
    expected=(A*B+4*s.diff(A,t)*M+6*s.diff(A,t,2)*L).subs(t,0)
    a,xt,E4=s.symbols('a xt E4',nonzero=True)
    T3=3*E4*xt/a;bm=4*xt/a;hm=120*xt**2/a**2
    required=4*bm*T3/3-hm*E4/12
    return dict(fluid_Hkk=s.simplify(Hkk+(1-w)*j/(4*v**3)),
        fluid_clock_trace=s.simplify(trace-3*(1-3*w)*h4),
        fourth_pin=s.simplify(s.diff(pin,t,4).subs(t,0)-expected),
        quadratic_face=s.simplify(required-6*E4*xt**2/a**2))


class FourthJet(FreeTimeJet):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.T.append([[mp.mpf(0)]*(self.degree+1) for _ in self.T[0]])

    def physical(self,x,t):
        out=super().physical(x,t);v=self.value(x,t);d=self.value(x,t,1)
        S,Q=v[:2];S1,Q1=d[:2];r=self.model.r0+x
        for i,f in enumerate(self.model.fluids):
            j,g=v[5+i],v[5+self.nf+i];jp,gp=d[5+i],d[5+self.nf+i]
            w,c=f['w'],f['c'];vf=(1+w)*c*j**w;h4=-(1-w)*j/(8*vf**3)
            k=mp.exp(-2*Q)*g*g;kp=2*mp.exp(-2*Q)*(g*gp-Q1*g*g)
            out[2]+=mp.exp(S)*(2-9*w/2)*h4*k*k
            out[3]+=2*mp.exp(S)*h4*k*k
            out[5+i]+=4*mp.exp(S-4*Q)*h4*(3*g*g*gp+(S1-Q1+2/r+(1-3*w)*jp/j)*g**3)
            out[5+self.nf+i]+=mp.exp(S)*(1-3*w)*h4/j*((S1-3*w*jp/j)*k*k+2*k*kp)
        return out

    def constraints(self,x,t):
        out=super().constraints(x,t);v=self.value(x,t);S,Q=v[:2]
        for i,f in enumerate(self.model.fluids):
            j,g=v[5+i],v[5+self.nf+i];w,c=f['w'],f['c'];vf=(1+w)*c*j**w
            correction=-mp.exp(S)*(1-w)*j*(mp.exp(-2*Q)*g*g)**2/(8*vf**3)
            out[0]+=correction;out[1]+=3*(1-3*w)*correction
        return out

    def evolve(self):
        super().evolve();n=self.degree-2
        source=local.series(lambda x:local.vector_derivative(lambda t:self.constraints(x,t),3),n)
        boundary=local.boundary_from_coefficients(self.C,self.W,source[0],source[1],n)
        def lapse(x,y):
            return [y[1],-(local.polynomial(self.C[0],x)*y[0]+local.polynomial(self.C[1],x)*y[1]
                           +local.polynomial(source[0],x))/local.polynomial(self.C[2],x)]
        coeff=local.ode_series(lapse,mp.mpf(0),boundary['constants'],self.degree)[0]
        self.T[3][0]=[v/6 for v in coeff];self.third_boundary=boundary
        self.shift(3);self.step(3)


def evaluate(source,dps=40,extra=0):
    data=read_summary(source)['result']
    with mp.workdps(dps):
        engine=FourthJet(data['U0'],data['U1'],3,extra+2,qprime=data['qprime'],Sprime=data['Sprime'])
        engine.evolve();order=3
        rows=local.series(lambda x:local.vector_derivative(lambda t:engine.constraints(x,t),4),order)
        out=local.boundary_from_coefficients([r[:4] for r in engine.C],[r[:4] for r in engine.W],rows[0],rows[1],order)
        q,q1=engine.T[0][2][:2];q2=2*engine.T[0][2][2]
        qt,qtr=engine.T[1][2][:2];qtt=2*engine.T[2][2][0]
        a=q1/q;c=(q1/q)**2+q2/q;xt=qt/q;xtr=(q1*qt+q*qtr)/q**2;xtt=(qt/q)**2+qtt/q
        U=mp.mpf(data['U0']);b=mp.mpf(1)/4
        E=list(map(mp.mpf,engine.reference['edge_jets']));T=engine.third_boundary['edge_jets']
        bm=4*xt/a;b0=4*xtr/a-2*xt*c/a**2+4*xt/b+U
        dm1=24*xt*xtr/a**2-12*xt**2*c/a**3+32*xt**2/(b*a)+4*xtt/a+8*U*xt/a
        hm2=120*xt**2/a**2;hm1=24*bm*b0-6*dm1
        corrected=list(out['edge_jets']);corrected[2]-=6*E[4]*xt**2/a**2
        corrected[3]+=-bm*T[4]-4*b0*T[3]+hm2*E[5]/20+hm1*E[4]/4
        fmt=lambda v:mp.nstr(v,dps-10)
        return dict(dps=dps,spatial_degree=engine.degree,
            selected_parameters={k:data[k] for k in ['U0','U1','qprime','Sprime']},
            second_lower_jets=[fmt(v) for v in E[:4]],
            third_lower_jets=[fmt(T[0]),fmt(T[1]),fmt(T[2]),fmt(T[3]-3*E[4]*xt/a)],
            fourth_boundary_jets=[fmt(v) for v in out['edge_jets']],
            fourth_motion_corrected_jets=[fmt(v) for v in corrected],
            fourth_lapse_boundary_constants=[fmt(v) for v in out['constants']],
            fourth_boundary_matrix_determinant=fmt(out['determinant']),
            fourth_momentum_max=fmt(max(abs(v)*mp.factorial(i) for i,v in enumerate(rows[2]))),
            full_theory='OPEN',non_claim='Conditional lower exact-jet matching; no global existence or Dirac certificate')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True)
    p.add_argument('--dps',type=int,default=40);p.add_argument('--extra',type=int,default=0)
    p.add_argument('--strict',action='store_true');a=p.parse_args()
    print(json.dumps(dict(identities={k:str(v) for k,v in identities().items()},
                          result=evaluate(a.input,a.dps,a.extra)),indent=2))
    raise SystemExit(2 if a.strict else 0)
