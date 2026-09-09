"""Third physical time jets of IC39, including canonical fluid flux and face motion."""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import time
import mpmath as mp
import sympy as s
import ic37_local_taylor as local


@lru_cache(None)
def identities():
    t=s.Symbol('t',real=True);L,B=s.symbols('L B',real=True)
    eta,S=s.Function('eta')(t),s.Function('S')(t)
    pin=eta*s.exp(S)*(L*t*t/2+B*t**3/6)
    expected=(eta*s.exp(S)*B+3*s.exp(S)*(s.diff(eta,t)+eta*s.diff(S,t))*L).subs(t,0)
    delta=s.Symbol('delta',real=True);a,b=s.symbols('a b',positive=True)
    xt,E4,S0=s.symbols('xt E4 S0',real=True);x=a*delta+xt*t
    switch=x**4/(x**4+(b-x)**4);Lv=-E4*b**4/(24*s.exp(S0)*a**4)
    W=-s.exp(S0)*switch*Lv*t*t/2
    cubic=s.diff(s.diff(W,t,3).subs(t,0),delta,3).subs(delta,0)
    v,k,c,n=s.symbols('v k c n',positive=True)
    pressure=c*(v*v-k)**n;momentum=s.diff(pressure,v)
    hk=-s.diff(pressure,k)
    j,wf,C=s.symbols('j wf C',positive=True);v0=(1+wf)*C*j**wf;h2=j/(2*v0)
    return dict(third_pin_derivative=s.simplify(s.diff(pin,t,3).subs(t,0)-expected),
                moving_cubic_term=s.simplify(cubic-3*E4*xt/a),
                fluid_quadratic_gradient=s.simplify(hk-momentum/(2*v)),
                fluid_pressure_gradient=s.simplify(j*s.diff(h2,j)-h2+wf*h2))


class TimeJet:
    # Field order S,Q,q,sh,beta,j0,...,g0,...; time entries are Taylor coefficients.
    def __init__(self,U0,U1,order,extra=0):
        self.model=local.LocalJet(U0,U1);m=self.model
        self.order=order;self.degree=order+6+extra;self.nf=len(m.fluids)
        Y=local.ode_series(m.rhs,m.r0,m.initial,self.degree)
        self.reference=local.local_result(U0=U0,U1=U1,dps=mp.mp.dps,order=self.degree-2,with_coefficients=True)
        data=[[mp.mpf(v) for v in row] for row in self.reference['source_coefficients']]
        self.C,self.W,self.FC,self.FW=data[:3],data[3:6],data[6],data[7]
        A0,A1=map(mp.mpf,self.reference['constants'])
        def lapse(x,y):
            return [y[1],-(local.polynomial(self.C[0],x)*y[0]+local.polynomial(self.C[1],x)*y[1]
                           +local.polynomial(self.FC,x))/local.polynomial(self.C[2],x)]
        acceleration=local.ode_series(lapse,mp.mpf(0),[A0,A1],self.degree)[0]
        zero=lambda:[mp.mpf(0)]*(self.degree+1)
        count=5+2*self.nf
        self.T=[[zero() for _ in range(count)] for _ in range(4)]
        for field,index in enumerate((0,2,6,4,5)):self.T[0][field]=Y[index]
        for i,f in enumerate(m.fluids):self.T[0][5+i][0]=f['j']
        self.T[1][0]=Y[8];self.T[2][0]=[v/2 for v in acceleration]

    def value(self,x,t,derivative=0):
        return [local.polynomial([local.polynomial(level[i],x,derivative) for level in self.T],t)
                for i in range(len(self.T[0]))]

    def physical(self,x,t):
        m=self.model;r=m.r0+x;v=self.value(x,t);d=self.value(x,t,1);dd=self.value(x,t,2)
        S,Q,q,sh,beta=v[:5];S1,Q1,q1,sh1,bp=d[:5];S2,Q2=dd[:2]
        D=m.D(S);z=2*mp.sqrt(D/(6*m.E))*mp.sinh(mp.asinh(-3*m.A*q*mp.sqrt(6*m.E/D)/(4*D))/3)
        args=(r,S,S1,S2,Q,Q1,Q2,q,z,sh,q1,sh1,beta,bp,*([mp.mpf(0)]*13),*m.params(S))
        Qd,qd,sd=m.flowfn(*args)[:3]
        HQ=-2*mp.exp(S-2*m.wc)*q/(6*m.m)-m.A*z/2
        out=[mp.mpf(0),Qd,qd,sd,mp.mpf(0),*([mp.mpf(0)]*(2*self.nf))]
        for i,f in enumerate(m.fluids):
            j,g=v[5+i],v[5+self.nf+i];jp,gp=d[5+i],d[5+self.nf+i]
            w,c=f['w'],f['c'];vf=(1+w)*c*j**w;k=mp.exp(-2*Q)*g*g
            kp=2*mp.exp(-2*Q)*(g*gp-Q1*g*g);h0=c*j**(1+w)
            out[2]+=mp.exp(S)*(3*w*h0/2+(2-3*w)*j*k/(4*vf))
            out[3]+=mp.exp(S)*j*k/(2*vf)
            flux=mp.exp(S-2*Q)*j/vf*(gp+(2/r+Q1+S1+(1-w)*jp/j)*g)
            out[5+i]=beta*jp-3*HQ*j+flux
            out[5+self.nf+i]=mp.exp(S)*(vf*(S1+w*jp/j)+(1-w)/(2*vf)*(kp+(S1-w*jp/j)*k))+bp*g+beta*gp
        return out

    def shift(self,n):
        m=self.model
        def source(x):
            def timevalue(t):
                v=self.value(x,t);return [-2*mp.exp(v[0]-2*m.wc)*v[3]/(m.m*(m.r0+x))]
            return [local.vector_derivative(timevalue,n)[0]/mp.factorial(n)]
        g=local.series(source,self.degree-1)[0];result=[mp.mpf(0)]*(self.degree+2)
        for k,v in enumerate(g):result[k+1]+=m.r0*v/(k+1);result[k+2]+=v/(k+1)
        self.T[n][4]=result[:self.degree+1]

    def evolve(self):
        for n in range(3):
            def rhs_coefficient(x):
                return [v/mp.factorial(n) for v in local.vector_derivative(lambda t:self.physical(x,t),n)]
            rows=local.series(rhs_coefficient,self.degree)
            for i,row in enumerate(rows):
                if i not in (0,4):self.T[n+1][i]=[v/(n+1) for v in row]
            if n<2:self.shift(n+1)

    def constraints(self,x,t):
        m=self.model;r=m.r0+x;v=self.value(x,t);d=self.value(x,t,1);dd=self.value(x,t,2)
        S,Q,q,sh=v[:4];D=m.D(S)
        z=2*mp.sqrt(D/(6*m.E))*mp.sinh(mp.asinh(-3*m.A*q*mp.sqrt(6*m.E/D)/(4*D))/3)
        ans=m.gradfn(r,S,d[0],dd[0],Q,d[1],dd[1],q,z,sh,*m.params(S));C,W=ans[0],ans[10]
        momentum=2*d[2]/3+4*d[3]/3+4*(d[1]+1/r)*sh
        for i,f in enumerate(m.fluids):
            j,g=v[5+i],v[5+self.nf+i];w,c=f['w'],f['c'];vf=(1+w)*c*j**w
            h0=mp.exp(S)*c*j**(1+w);gradient=mp.exp(S-2*Q)*j*g*g/(2*vf)
            C+=h0+gradient;W-=(1-3*w)*(h0-gradient);momentum-=j*g
        return [C,W,momentum]


def field_result(U0='0',U1='0',dps=50,order=3,extra=0,engine_factory=TimeJet):
    started=time.perf_counter()
    with mp.workdps(dps):
        engine=engine_factory(U0,U1,order,extra);engine.evolve();zero=mp.mpf(0)
        first=local.vector_derivative(lambda t:engine.constraints(zero,t),1)
        second=local.series(lambda x:local.vector_derivative(lambda t:engine.constraints(x,t),2),order)
        second_jets=[[v*mp.factorial(n) for n,v in enumerate(row)] for row in second]
        old=list(map(mp.mpf,engine.reference['edge_jets'][:order+1]))
        error=max(abs(a-b)/max(1,abs(b)) for a,b in zip(second_jets[1],old))
        third=local.series(lambda x:local.vector_derivative(lambda t:engine.constraints(x,t),3),order)
        result=local.boundary_from_coefficients([r[:order+1] for r in engine.C],
                    [r[:order+1] for r in engine.W],third[0],third[1],order)
        a=mp.mpf(engine.reference['activation_radial_derivative'])
        q0=engine.T[0][2][0];qt=engine.T[1][2][0]
        # alpha^2=1/2 on the face, w_t=0, so x_t=2 alpha^2 q_t/q=q_t/q.
        xt=qt/q0;speed=-xt/a;E4=mp.mpf(engine.reference['edge_jets'][4])
        corrected=list(result['edge_jets'])
        if order>=3:corrected[3]-=3*E4*xt/a
        fmt=lambda v:mp.nstr(v,dps-12)
        return dict(U0=str(U0),U1=str(U1),dps=dps,order=order,spatial_degree=engine.degree,
                    first_constraint_error=fmt(max(abs(v) for v in first)),
                    second_gate_relative_error=fmt(error),second_gate_jets=[fmt(v) for v in second_jets[1]],
                    second_lapse_residual=fmt(max(abs(v) for v in second_jets[0])),
                    second_momentum_residual=fmt(max(abs(v) for v in second_jets[2])),
                    third_momentum_residual=fmt(max(abs(v)*mp.factorial(n) for n,v in enumerate(third[2]))),
                    third_W_boundary_jets=[fmt(v) for v in result['edge_jets']],
                    motion_corrected_third_jets=[fmt(v) for v in corrected],
                    lapse_third_boundary_constants=[fmt(v) for v in result['constants']],
                    boundary_matrix_determinant=fmt(result['determinant']),boundary_matrix_rank=result['rank'],
                    face_x_t=fmt(xt),face_coordinate_speed=fmt(speed),required_cubic_jet=fmt(3*E4*xt/a),
                    elapsed_seconds=time.perf_counter()-started,full_theory='OPEN')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--input');parser.add_argument('--dps',type=int,default=40)
    parser.add_argument('--order',type=int,default=3);parser.add_argument('--extra',type=int,default=0)
    parser.add_argument('--strict',action='store_true');args=parser.parse_args()
    choices=[dict(U0='0',U1='0')]
    if args.input:choices=[dict(U0=x['U0'],U1=x['U1']) for x in json.loads(Path(args.input).read_text())['joint'] if 'U0' in x]
    out=dict(identities={k:str(v) for k,v in identities().items()},
             rows=[field_result(**v,dps=args.dps,order=args.order,extra=args.extra) for v in choices],full_theory='OPEN')
    print(json.dumps(out,indent=2));raise SystemExit(2 if args.strict else 0)
