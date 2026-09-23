"""Exact algebra audit. The written proof supplies the stochastic limits."""
import json
from pathlib import Path
import sympy as S

t, s, z, k, mu, u, phi = S.symbols('t s z k mu u phi', real=True)
Qs, Qz, e = S.symbols('Qs Qz e', real=True)
M, d, R, c, cap, mean_time = S.symbols('M d R c cap mean_time', positive=True)
F = S.Function('F')(s)
checks = {}
def zero(x):
    return S.cancel(S.expand(x)) == 0

def derive(coordinate, direction_cosine, density, lo, hi):
    moments = [S.integrate(density*direction_cosine**j,(coordinate,lo,hi)) for j in range(3)]
    ec = S.integrate(S.cos(phi),(phi,0,2*S.pi))/(2*S.pi)
    ec2 = S.integrate(S.cos(phi)**2,(phi,0,2*S.pi))/(2*S.pi)
    norm, first, second = moments
    kz = z*first  # azimuthal first moment is zero
    kz2 = S.expand(z*z*second+(s-z*z)*(norm-second)*ec2)
    bracket = S.expand(kz2-2*z*kz+z*z*norm)
    generator_jump = S.expand(kz2-z*z)
    A = generator_jump.coeff(s)
    B = generator_jump.coeff(z,2)
    qz_solution = S.solve(S.Eq(e,1+A*Qs+B*Qz),Qz)[0]
    variance = S.expand(bracket.coeff(s)*Qs+bracket.coeff(z,2)*Qz)
    eliminated = S.factor(variance.subs(Qz,qz_solution))
    residual = S.factor(eliminated-(S.Rational(2,3)*Qs+S.Rational(11,9)*(1-e)))
    predicate = all([norm==1,first==0,ec==0,ec2==S.Rational(1,2),
        zero(kz2-(3*s+z*z)/10),zero(bracket-(3*s+11*z*z)/10),zero(residual)])
    return dict(moments=list(map(str,moments)),Kz=str(kz),Kz2=str(kz2),
        bracket=str(bracket),generator_jump=str(generator_jump),
        eliminated=str(eliminated),residual=str(residual),certificate=predicate)

cases = {
    'main':derive(mu,mu,3*(1+mu*mu)/8,-1,1),
    'positive':derive(u,2*u-1,2*3*(1+(2*u-1)**2)/8,0,1),
    'negative':derive(mu,mu,S.Rational(1,2),-1,1),
}
checks['main_computed_certificate']=cases['main']['certificate']
checks['positive_computed_certificate']=cases['positive']['certificate']
checks['negative_computed_certificate_rejects']=not cases['negative']['certificate']
checks['positive_same_algebra']=all(cases['main'][n]==cases['positive'][n] for n in cases['main'])

# Independently apply the full space-time generator to Y and Y^2.
Kz2=(3*s+z*z)/10
def K(poly):
    p=S.Poly(S.expand(poly),z)
    assert p.degree()<=2
    return p.nth(0)+p.nth(2)*Kz2
def G(expr):
    return S.expand(S.diff(expr,t)+2*z*S.diff(expr,s)+S.diff(expr,z)+k*(K(expr)-expr)).subs(S.diff(F,s),-k/2).expand()
Y=t+F-z
checks['mean_zero_drift']=zero(G(Y))
checks['square_drift_actual_bracket']=zero(G(Y*Y)-k*(3*s+11*z*z)/10)
checks['z2_generator']=zero(G(z*z)-(2*z+k*(3*s-9*z*z)/10))
checks['s_generator']=zero(G(s)-2*z)
checks['wrong_sign_detected']=bool((Kz2-z*z).subs({s:1,z:1})<0)
checks['actual_square_nonnegative_witness']=bool((Kz2+z*z).subs({s:1,z:1})>0)

r, a, h, v=S.symbols('r a h v', nonnegative=True)
checks['inner_signed_integrand']=zero((a-h)*(-h)*(-v)-h*v*(a-h))
checks['outer_signed_integrand']=zero((a+h)*h*v-h*v*(a+h))
step_mean=S.integrate(M*r,(r,0,a))
step_second=S.integrate(M*r*r,(r,0,a))
a0=S.sqrt(2*d/M)
checks['step_mean_constraint']=zero(step_mean.subs(a,a0)-d)
bound=S.Rational(2,3)*step_second.subs(a,a0)
target=2*(2*d)**S.Rational(3,2)/(9*S.sqrt(M))
checks['cap_constant']=S.simplify(bound-target)==0
checks['relative_constant']=S.simplify(bound/d**2-4*S.sqrt(2)/(9*S.sqrt(M*d)))==0
checks['mean_endpoint']=S.simplify((bound/d**2).subs(d,M/2)-8/(9*M))==0
checks['zero_mean_endpoint']=S.limit(bound,d,0,dir='+')==0
q=S.symbols('q',positive=True)
relative_at_fraction=S.simplify((bound/d**2).subs(d,M*q/2))
checks['fractional_mean_floor_form']=S.simplify(relative_at_fraction-8/(9*M*S.sqrt(q)))==0
# The proof uses 0<q<=1, so 1/sqrt(q)>=1, not an unrestricted sign claim.
physical=S.simplify((R/c)**2*bound.subs({M:R*cap,d:c*mean_time/R}))
checks['physical_units']=S.simplify(physical-4*S.sqrt(2)*mean_time**S.Rational(3,2)/(9*S.sqrt(c*cap)))==0
result={'checks':checks,'all_checks_pass':all(checks.values()),'controls':cases,
 'bound':str(S.simplify(bound)),'physical_bound':str(physical),
 'scope':'Exact algebra only. THEOREM.md separately proves integrability, stopping, radial traversal, and all-profile signed-integrand inequality. No novelty or observation certificate.'}
out=Path(__file__).parent/'certified'/'result.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
