#!/usr/bin/env python3
"""Exact geometric target, NOT a forward action or PPN prediction.

In areal radius r, ds²=-A dt²+B dr²+r²dOmega². Isotropic radius R obeys
d(log R)/dr=sqrt(B)/r. Define logarithmic Phi=log(A)/2 and
Psi=-log(r/R); these agree with weak-field potentials to first order.
Thus Phi'=g and Psi'=(sqrt(B)-1)/r, independently of any action.
Equal derivatives (and one finite-radius normalization) require B=(1+rg)².
This is stronger than the requested leading-order no-slip, but unlike the
old exact zero-pressure ansatz it implements that nonlinear extension itself.
"""
import json
import sympy as s
import mpmath as mp


def derive():
    r,g=s.symbols('r g',positive=True)
    h=s.symbols('h',positive=True)
    B=(1+r*g)**2
    pr=((1+2*r*g)-B)/(B*r*r)
    b=2/(1+s.sqrt(1-4*h));target=b*b
    checks={
        'independent_log_slip':s.simplify(g-(s.sqrt(B)-1)/r),
        'radial_pressure':s.factor(pr+g*g/B),
        'g_equals_yB_compatibility':s.simplify(target-(1+h*target)**2),
        'newton_branch':s.limit(target,h,0)-1,
        'old_target_difference_begins_second_order':s.limit((target-1/(1-2*h))/h**2,h,0)-1,
    }
    assert all(value==0 for value in checks.values()),checks
    return dict(checks={k:str(v) for k,v in checks.items()},
        B=str(B),geometric_pr=str(s.factor(pr)),target_B=str(target),
        target_series=str(s.series(target,h,0,4)),old_target_series=str(s.series(1/(1-2*h),h,0,4)),
        domain='r,g>0; h=r*y in (0,1/4); positive square-root branch',
        scope='Coordinate geometry and chosen target only, not action-derived slip, gamma/beta, lensing, or global normalization')


def action_point():
    """First-jet inverse on this target, checked against physical equations.

    Does not reuse the eta target for derivatives. Higher action curvatures,
    the EF principal, and two-mass preservation on this target are still open.
    """
    from general_inverse import pressure_inverse as p
    with mp.workdps(60):
        eps,y=mp.mpf('1e-6'),mp.mpf('.1')
        mu=-mp.expm1(-y);lam=mu+y*mp.exp(-y)
        r=eps/mp.sqrt(y*mu);ry=-r*lam/(2*y*mu);h=r*y
        root=mp.sqrt(1-4*h);b=2/(1+root);B=b*b
        bh=4/((1+root)**2*root);Br=2*b*bh*(y+r/ry)
        g=y*B;gr=B/ry+y*Br
        geometry=p.metric_invariants(r,B,Br,g,gr)
        X=mp.mpf('.5');U=X*r*g/4;z=-mp.mpf('1.5')*g
        state=p.coefficients(geometry,X,U,z,mp.mpf('.525'),mp.mpf('.05'),mp.mpf('-3000'))
        residual=p.physical_residuals(state)
        assert max(residual.values())<mp.mpf('1e-40'),residual
        return dict(eps=str(eps),y=str(y),geometric_pr=mp.nstr(geometry['pr'],30),
            pressure_identity_error=mp.nstr(abs(geometry['pr']+g*g/B),10),
            inverse_determinant=mp.nstr(state['inverse_determinant'],30),
            physical_errors={k:mp.nstr(v,10) for k,v in residual.items()},
            scope='One imposed logarithmic-no-slip metric with actual first-jet inverse; no health or common-action-family result')


if __name__=='__main__':print(json.dumps(dict(algebra=derive(),action_point=action_point()),indent=2))
