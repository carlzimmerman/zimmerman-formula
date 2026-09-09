"""Static planar action with independent spatial metric components.

ds^2=-exp(2P)dt^2+exp(2A)dx^2+exp(2B)(dy^2+dz^2), tau=t,
phi=s0*x+perturbation. EH is integrated by parts. C=Lambda/(8piG)+K(0).
No clock/shift/time variation or full gravitational mode count is performed.
"""
import json
import sympy as s
e,G,ca,b,xi,v,C,J0,J1,J2=s.symbols('eps G ca b xi s0 C J0 J1 J2',real=True)
p,a,h,f=s.symbols('P A B f',real=True)
px,ax,hx,fx,fxx=s.symbols('Px Ax Bx fx fxx',real=True)
Y=s.exp(-2*e*a)*(v+e*fx)**2
H=s.exp(-4*e*a)*((e*fxx-e*ax*(v+e*fx))**2+2*(e*hx)**2*(v+e*fx)**2)
argument=Y+xi**2*H
function=J0+J1*(argument-v*v)+J2*(argument-v*v)**2/2
L=s.exp(e*(p-a+2*h))*((2*(e*hx)**2+4*e*px*e*hx)/(16*s.pi*G)+ca*(e*px)**2+2*b*e*px*(v+e*fx))
L-=s.exp(e*(p+a+2*h))*(C+b*function)
L1=s.expand(s.diff(L,e).subs(e,0))
L2=s.expand(s.diff(L,e,2).subs(e,0)/2)
fields=(p,a,h,f);first=(px,ax,hx,fx)
second=s.symbols('Pxx Axx Bxx fxx',real=True)
third=s.symbols('Pxxx Axxx Bxxx fxxx',real=True)
fourth=s.symbols('Pxxxx Axxxx Bxxxx fxxxx',real=True)
mapping=dict(zip(fields+first+second+third,first+second+third+fourth))
def D(expr):return s.expand(sum(s.diff(expr,k)*value for k,value in mapping.items()))
def EL(expr,index):
    return s.simplify(s.diff(expr,fields[index])-D(s.diff(expr,first[index]))+D(D(s.diff(expr,second[index]))))
tadpoles=[EL(L1,i) for i in range(4)]
equations=[EL(L2,i) for i in range(4)]
# Homogeneous background equations require this anisotropic difference.
anisotropy=s.factor(tadpoles[1]-tadpoles[2]/2)
assert s.simplify(anisotropy-2*b*J1*v**2)==0
# Independent spatial components agree with the previous conformal operator.
coherence=s.expand(L2).coeff(xi,2)*xi**2
assert s.simplify(coherence.subs({ax:-px,hx:-px})+b*J1*xi**2*((fxx+v*px)**2+2*v*v*px*px))==0
print(json.dumps(dict(exact_action_taylor_scope=__doc__,quadratic_density=str(L2),
    background_equations=dict(zip(map(str,fields),map(str,tadpoles))),
    linearized_equations=dict(zip(map(str,fields),map(str,equations))),
    background_anisotropic_residual=str(anisotropy),full_theory='OPEN'),indent=2))
