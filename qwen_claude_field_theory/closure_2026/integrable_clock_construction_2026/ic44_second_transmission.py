"""Construct finite second-derivative transmission jets from the radial action.

This is a local compatibility construction, NOT an existence/closure theorem.
Fields and physical-metric first derivatives are continuous; q and shear may
have first-derivative jumps. lambda is the active clock reaction eta exp(S) ell.
"""
import argparse
from functools import lru_cache
import json
import sympy as s
import ic44_moving_interface as interface


@lru_cache(None)
def derive():
    base=interface.derive();L=base['phase_action_density']
    r=s.Symbol('r',positive=True)
    fields=s.symbols('S w Q q z shear beta',real=True)
    grads=s.symbols('S_r w_r Q_r q_r z_r shear_r beta_r',real=True)
    seconds=s.symbols('S_rr w_rr Q_rr q_rr z_rr shear_rr beta_rr',real=True)
    S,w,Q,q,z,sh,beta=fields;J=r**2*s.exp(3*Q)
    Qt,qt,Qtr=s.symbols('Q_t q_t Q_tr',real=True)
    speed=s.Symbol('Rdot',real=True);reaction=s.Symbol('lambda',real=True)
    ds,dw,dc,dq,dh,db=unknown=s.symbols('dS_rr dw_rr dQ_rr dq_r dshear_r dbeta_rr',real=True)
    def dr(expr):
        return s.diff(expr,r)+sum(s.diff(expr,f)*g for f,g in zip(fields,grads))\
             +sum(s.diff(expr,g)*gg for g,gg in zip(grads,seconds))+s.diff(expr,Qt)*Qtr
    equations=[s.diff(L,f)-dr(s.diff(L,g)) for f,g in zip(fields,grads)]
    # The sole radial metric time momentum is 2Jq; differentiate it, do not
    # replace the metric equation by a prescribed evolution law.
    equations[2]-=s.diff(s.diff(L,Qt),Q)*Qt+s.diff(s.diff(L,Qt),q)*qt
    z_eq=s.diff(L,z)/J;Fz=s.diff(z_eq,z);A=s.diff(z_eq,q)
    # First jets of S,w,Q and beta are continuous. At a continuous metric
    # gradient [Q_tr]=-Rdot [Q_rr]; at continuous q, [q_t]=-Rdot [q_r].
    sub={seconds[0]:seconds[0]+ds,seconds[1]:seconds[1]+dw,seconds[2]:seconds[2]+dc,
         grads[3]:grads[3]+dq,grads[4]:grads[4]-A*dq/Fz,
         grads[5]:grads[5]+dh,seconds[6]:seconds[6]+db,qt:qt-speed*dq,Qtr:Qtr-speed*dc}
    change=lambda expr:s.simplify((expr.subs(sub,simultaneous=True)-expr)/J)
    conditions=s.Matrix([change(equations[0]),change(equations[1])-reaction,
        change(equations[2]),change(equations[6]),change(dr(equations[3])),change(dr(equations[5]))])
    matrix,rhs=s.linear_eq_to_matrix(conditions,unknown)
    # Default Bareiss determinant expansion triggers costly multivariate GCDs
    # in the unreduced lapse exponentials. Factor after each exact Gaussian
    # row operation instead; choose pivots from the computed matrix.
    augmented=matrix.row_join(rhs).applyfunc(s.factor)
    determinant=s.Integer(1);pivots=[]
    for col in range(matrix.cols):
        choices=[i for i in range(len(pivots),matrix.rows) if augmented[i,col]!=0]
        if not choices:continue
        row=len(pivots);chosen=choices[0]
        if chosen!=row:augmented.row_swap(row,chosen);determinant=-determinant
        pivot=augmented[row,col];determinant=s.factor(determinant*pivot)
        for j in range(col,augmented.cols):augmented[row,j]=s.factor(augmented[row,j]/pivot)
        for i in range(matrix.rows):
            if i==row:continue
            multiple=augmented[i,col]
            for j in range(col,augmented.cols):
                augmented[i,j]=s.factor(augmented[i,j]-multiple*augmented[row,j])
        pivots.append(col)
    if len(pivots)!=matrix.cols:raise ValueError('Transmission matrix is not generically invertible')
    solution=augmented[:,-1]
    residual=conditions.subs(dict(zip(unknown,solution))).applyfunc(s.simplify)
    # IC39 uses x=exp(-6w)q^2/(9m^2 h0^2)-1/2. At its negative-q
    # boundary x=0 and w_r=0, differentiation gives x_r=q_r/q_boundary.
    # A negative off-side x_r puts r<R on the WRONG side of the activation.
    m,h0=s.symbols('m h0',positive=True)
    qb=s.Symbol('q_boundary',negative=True);qp=s.Symbol('qprime_on',real=True)
    activation=s.exp(-6*w)*q**2/(9*m**2*h0**2)-s.Rational(1,2)
    dxq=s.diff(activation,q).subs(s.exp(-6*w),9*m**2*h0**2/(2*qb**2)).subs(q,qb)
    off_gradient=s.factor(dxq*(qp+solution[3]))
    return dict(S=S,w=w,beta=beta,speed=speed,reaction=reaction,Fz=Fz,
        q_boundary=qb,qprime_on=qp,activation_gradient_off=off_gradient,
        equation_order=['lapse','inactive_clock','spatial_metric','momentum','radial_q','radial_shear'],
        unknown_order=[str(v) for v in unknown],matrix=matrix,rhs=rhs,determinant=determinant,
        generic_rank=len(pivots),
        jumps=dict(zip(['S_rr','w_rr','Q_rr','q_r','shear_r','beta_rr'],solution)),
        residual=residual,zero_reaction_jumps=solution.subs(reaction,0),
        scope='Exact finite radial transmission jets for Fz !=0, S+w !=0, u !=0, r*m !=0 and Rdot+beta !=0; no evolved free-boundary solution')


if __name__=='__main__':
    from ic43_weighted_multiplier import serial
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');args=p.parse_args()
    print(json.dumps(serial(dict(result=derive(),full_theory='OPEN')),indent=2))
    raise SystemExit(2 if args.strict else 0)
