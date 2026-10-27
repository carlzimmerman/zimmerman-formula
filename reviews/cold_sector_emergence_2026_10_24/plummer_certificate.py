"""Exact positive-basis certificate for all positive Plummer mass/scale choices."""
import json
from pathlib import Path
import sympy as s
z,q=s.symbols('z q')
# z=r^2/(1+r^2); q=sqrt(b/(1+b)); b=A*r/(1+r^2)^(3/2).
# D=d/dlog(r); density = [A/(4*pi*(1+r^2)^(3/2))]*R.
R=(1-q)*(5-q-3*z+3*z*q)/(2*q)
def D(v):
    return 2*z*(1-z)*s.diff(v,z)+q*(1-q*q)*(1-3*z)*s.diff(v,q)/2
first=s.factor(D(R)-3*z*R)
second=s.factor(D(first)-3*z*first-(1+(1-3*z)*(1+q*q)/2)*first)
# second has sign of d2rho/dPhi2; all omitted prefactors are positive.
poly=s.Poly(s.cancel(8*q*second/(1-q)),z,q)
n,m=poly.degree(z),poly.degree(q)
coeff=[]
reconstruction=0
for i in range(n+1):
    row=[]
    for j in range(m+1):
        value=sum(poly.coeff_monomial(z**k*q**l)*s.binomial(i,k)/s.binomial(n,k)*s.binomial(j,l)/s.binomial(m,l) for k in range(i+1) for l in range(j+1))
        row.append(value)
        reconstruction+=value*s.binomial(n,i)*z**i*(1-z)**(n-i)*s.binomial(m,j)*q**j*(1-q)**(m-j)
    coeff.append(row)
assert s.expand(reconstruction-poly.as_expr())==0
assert all(v>=0 for row in coeff for v in row)
assert any(v>0 for row in coeff for v in row)

# Check density factor independently from spherical Poisson, using b/r prefactor.
b=s.symbols('b',positive=True)
F=s.sqrt(b*b+b)-b
raw=2*F/b+(1-3*z)*s.diff(F,b)
# b=q^2/(1-q^2), q in (0,1); substitute the known positive square root explicitly.
raw=s.simplify(raw.subs(s.sqrt(b*b+b), b/q))
raw=s.factor(raw.subs(b,q*q/(1-q*q)))
assert s.simplify(raw-R)==0

result={'polynomial':str(poly.as_expr()),'degrees':[n,m],
        'bernstein_coefficients':[[str(v) for v in row] for row in coeff],
        'exact_reconstruction':True,'all_coefficients_nonnegative':True,
        'domain':'0<z<1 and 0<q<1, hence every r>0,A>0 in dimensionless Plummer family',
        'conclusion':'d2rho_c/dPhi2>0; with Abel inversion and outer decay this proves a nonnegative isotropic stationary distribution',
        'non_claims':['No nonlinear stability','No formation selection','No finite total halo mass','No nonspherical result']}
Path('reviews/cold_sector_emergence_2026_10_24/certificate_run/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
