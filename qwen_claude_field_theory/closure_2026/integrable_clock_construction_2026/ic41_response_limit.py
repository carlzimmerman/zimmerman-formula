"""Conditional finite third pin response, retaining moving-face Laurent terms."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import sympy as s
import ic37_local_taylor as local
from ic41_free_initial_gradients import FreeTimeJet


def residual_fourth(E4,E5,T4,a,c,xt,xtr,U,b):
    constant=4*xtr/a-2*xt*c/a**2+4*xt/b
    return T4-3*(4*xt*E5/(5*a)+(constant+U)*E4)


def identity():
    d,u=s.symbols('delta u');a,b=s.symbols('a b',positive=True)
    c,xt,xtr,U,E4,E5,T4=s.symbols('c xt xtr U E4 E5 T4')
    eta=u**4/(u**4+(b-u)**4);x=a*d+c*d*d/2
    logarithmic=s.series((s.diff(eta,u)/eta).subs(u,x)*(xt+xtr*d),d,0,1).removeO()
    E=E4*d**4/24+E5*d**5/120
    T=3*E4*xt/a*d**3/6+T4*d**4/24
    actual=s.expand(T-3*(logarithmic+U)*E).coeff(d,4)*24
    return s.simplify(actual-residual_fourth(E4,E5,T4,a,c,xt,xtr,U,b))


def read_summary(source):
    text=Path(source).read_text();decoder=json.JSONDecoder();items=[]
    while text.strip():
        text=text.lstrip();obj,end=decoder.raw_decode(text);items.append(obj);text=text[end:]
    return next(x for x in reversed(items) if x.get('event')=='summary')


def evaluate(source,dps=60,extra=1):
    data=read_summary(source)['result']
    with mp.workdps(dps):
        engine=FreeTimeJet(data['U0'],data['U1'],4,extra,qprime=data['qprime'],Sprime=data['Sprime'])
        engine.evolve();m=engine.model
        q,q1=engine.T[0][2][0:2];q2=2*engine.T[0][2][2]
        qt=engine.T[1][2][0];qtr=engine.T[1][2][1]
        a=q1/q;c=(q1/q)**2+q2/q;xt=qt/q;xtr=(q1*qt+q*qtr)/q**2
        E=list(map(mp.mpf,engine.reference['edge_jets']));E4,E5=E[4:6]
        third=local.series(lambda x:local.vector_derivative(lambda t:engine.constraints(x,t),3),4)
        boundary=local.boundary_from_coefficients([row[:5] for row in engine.C],
                     [row[:5] for row in engine.W],third[0],third[1],4)
        T=boundary['edge_jets'];b=mp.mpf(1)/4;U=mp.mpf(data['U0']);S=m.initial[0]
        R4=residual_fourth(E4,E5,T[4],a,c,xt,xtr,U,b)
        factor=-b**4/(24*mp.exp(S)*a**4);fmt=lambda v:mp.nstr(v,dps-10)
        return dict(event='summary',dps=dps,spatial_degree=engine.degree,input_parameters=
            {k:data[k] for k in ['U0','U1','qprime','Sprime']},
            second_lower_jets=[fmt(v) for v in E[:4]],
            third_lower_residual_jets=[fmt(T[0]),fmt(T[1]),fmt(T[2]),fmt(T[3]-3*E4*xt/a)],
            E4=fmt(E4),E5=fmt(E5),third_W_fourth_jet=fmt(T[4]),residual_fourth=fmt(R4),
            conditional_ell_tt_limit=fmt(factor*E4),conditional_ell_ttt_limit=fmt(factor*R4),
            a=fmt(a),x_rr=fmt(c),x_t=fmt(xt),x_tr=fmt(xtr),
            boundary_matrix_determinant=fmt(boundary['determinant']),
            momentum_third_max=fmt(max(abs(v)*mp.factorial(i) for i,v in enumerate(third[2]))),
            full_theory='OPEN',non_claim='Limits conditional on EXACT vanishing of lower jets; rounded data alone give no boundedness proof')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True)
    p.add_argument('--dps',type=int,default=60);p.add_argument('--extra',type=int,default=1)
    p.add_argument('--strict',action='store_true');a=p.parse_args()
    print(json.dumps(dict(identity=str(identity()),**evaluate(a.input,a.dps,a.extra)),indent=2))
    raise SystemExit(2 if a.strict else 0)
