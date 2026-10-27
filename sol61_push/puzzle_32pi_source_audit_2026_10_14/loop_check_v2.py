import sympy as s,json
import mpmath as mp
b,p,v,c,kap,S,K,mu,hi,lo=s.symbols('b p v c kap S K mu hi lo',positive=True)
checks=[]
def ck(name,expr):
    assert s.simplify(expr)==0,(name,expr)
    checks.append(name)
I=(p*p+b)**s.Rational(5,2)/5-b*(p*p+b)**s.Rational(3,2)/3
ck('radial determinant integral',s.diff(I,p)-p**3*s.sqrt(p*p+b))
J=I.subs(p,hi)-I.subs(p,lo)
ck('linear shell term',s.diff(J,b).subs(b,0)-(hi**3-lo**3)/6)
ck('quadratic shell term',s.diff(J,b,2).subs(b,0)/2+(hi-lo)/8)
ac=2*kap*(1+c*c)/mu**2
average=lambda f:s.integrate(f,(c,-1,1))/2
coef1=s.simplify(S*average(ac)*(hi**3-lo**3)/(24*s.pi**2*s.sqrt(K)))
coef2=s.simplify(-S**3*average(ac*ac)*(hi-lo)/(32*s.pi**2*s.sqrt(K)))
ck('linear gradient energy coefficient',coef1-kap*S*(hi**3-lo**3)/(9*s.pi**2*s.sqrt(K)*mu**2))
ck('quadratic gradient energy coefficient',coef2+7*kap**2*S**3*(hi-lo)/(30*s.pi**2*s.sqrt(K)*mu**4))
# Independent quadrature over frequency and angles after frequency integration:
# all masses and couplings one; spatial shell 1/16<=p<=1/8; 50 decimal digits.
mp.mp.dps=50
def delta(vv):
    return mp.quad(lambda cc:mp.quad(lambda pp:pp**2*(mp.sqrt(pp**4+2*(1+cc*cc)*vv*pp*pp)-pp*pp),[mp.mpf(1)/16,mp.mpf(1)/8]),[-1,1])/(8*mp.pi**2)
aa=7/(4096*9*mp.pi**2);bb=-7/(480*mp.pi**2)
samples=[]
for vv in [mp.mpf('1e-6'),mp.mpf('1e-7'),mp.mpf('1e-8')]:
    value=delta(vv);rem=value-aa*vv-bb*vv*vv
    assert abs(rem/vv**3)<mp.mpf('1')
    samples.append({'gradient':float(vv),'delta_energy':float(value),'linear_coefficient_estimate':float(value/vv),
                    'quadratic_coefficient_estimate':float((value-aa*vv)/vv**2),'remainder_over_v_cubed':float(rem/vv**3)})
print(json.dumps({'checks':checks,'count':len(checks),'shell':[1/16,1/8],'precision_digits':50,
 'linear_coefficient':float(aa),'quadratic_coefficient':float(bb),'samples':samples,
 'scope':'One-loop scalar determinant in a fixed frame with explicit sharp spatial momentum shell; regulator-dependent local terms, not physical renormalized predictions'},indent=2))
