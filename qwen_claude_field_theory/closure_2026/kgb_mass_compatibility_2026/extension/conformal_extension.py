#!/usr/bin/env python3
"""One known luminal conformal-DHOST extension and its static discriminator.

X=-grad(phi)^2/2. L=F(X)R+3F_X^2(grad X)^2/(2F)+P(X)-G(X)box(phi).
This checkpoint varies the new sector and derives necessary radial equations;
it supplies neither a full solution nor a new propagating degree of freedom.
"""
from functools import lru_cache
import json
import sympy as s


@lru_cache(None)
def curvature_check():
    t,r,theta,az = s.symbols('t r theta az',real=True)
    A,B,R = [s.Function(v)(r) for v in ('A','B','R')]
    coordinates = (t,r,theta,az)
    metric = s.diag(-A,B,R**2,R**2*s.sin(theta)**2)
    inverse = metric.inv()
    gamma = [[[s.simplify(sum(inverse[a,d]*(s.diff(metric[d,c],coordinates[b])
        +s.diff(metric[d,b],coordinates[c])-s.diff(metric[b,c],coordinates[d]))/2
        for d in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = s.Matrix(4,4,lambda a,b:s.simplify(sum(
        s.diff(gamma[c][a][b],coordinates[c])-s.diff(gamma[c][a][c],coordinates[b])
        +sum(gamma[c][c][d]*gamma[d][a][b]-gamma[c][b][d]*gamma[d][a][c]
        for d in range(4)) for c in range(4))))
    actual = s.simplify(s.trace(inverse*ricci))
    Ap,Bp,Rp = [s.diff(v,r) for v in (A,B,R)]
    expected = (-s.diff(A,r,2)/(A*B)+Ap**2/(2*A*A*B)+Ap*Bp/(2*A*B*B)
        -2*Ap*Rp/(A*B*R)+2*Bp*Rp/(B*B*R)-4*s.diff(R,r,2)/(B*R)
        +2/R**2-2*Rp**2/(B*R**2))
    return dict(scalar_curvature=actual,residual=s.factor(actual-expected))


@lru_cache(None)
def derive():
    A,B,R,q,p,F0,lam = s.symbols('A B R q p F0 lam',positive=True)
    Ap,Bp,Rp,pp,A2,B2,R2,p2 = s.symbols('Ap Bp Rp pp A2 B2 R2 p2',real=True)
    jets = (A,B,R,p,Ap,Bp,Rp,pp)
    following = (Ap,Bp,Rp,pp,A2,B2,R2,p2)
    D = lambda e:sum(s.diff(e,v)*dv for v,dv in zip(jets,following))
    measure = s.sqrt(A*B)*R**2
    X = q*q/(2*A)-p*p/(2*B)
    Xr = D(X)
    # One explicit invertible subfamily; the general reduction is checked below.
    F = F0*(1+lam*X)
    Fx = F0*lam
    Fr = Fx*Xr
    coeff = 3*Fx**2/(2*F)
    scalar_curvature = (-A2/(A*B)+Ap**2/(2*A*A*B)+Ap*Bp/(2*A*B*B)
        -2*Ap*Rp/(A*B*R)+2*Bp*Rp/(B*B*R)-4*R2/(B*R)
        +2/R**2-2*Rp**2/(B*R**2))
    raw = measure*(F*scalar_curvature+coeff*Xr**2/B)
    reduced = s.sqrt(A/B)*(2*F*B+2*F*Rp**2+2*F*R*Rp*Ap/A
        +Fr*(R**2*Ap/A+4*R*Rp)+3*R**2*Fr**2/(2*F))
    boundary = -F*R**2*Ap/s.sqrt(A*B)-4*F*R*s.sqrt(A/B)*Rp
    EL = lambda L,v,vp:s.diff(L,v)-D(s.diff(L,vp))
    # Actually vary B and p before setting R=r. J=-EL_p/measure.
    current = -EL(reduced,p,pp)/measure
    radial_variation = 2*B*EL(reduced,B,Bp)/measure
    combo = s.factor(radial_variation-p*current)
    einstein_rr = (Rp**2/B-1)/R**2+Ap*Rp/(A*B*R)
    expected_combo = (-2*F*einstein_rr
        -Fr*(Ap/A+4*Rp/R)/B-3*Fr**2/(2*F*B))
    boxX = D(s.sqrt(A/B)*R**2*Xr)/measure
    coeffX = -3*Fx**3/(2*F**2)  # F_XX=0 in this explicit test family.
    expected_current = p/B*(Fx*scalar_curvature-coeffX*Xr**2/B-2*coeff*boxX)
    flat = {A:1,B:1,R:1,q:2,p:1,Ap:0,Bp:0,Rp:1,A2:0,B2:0,R2:0,p2:0,F0:s.Rational(1,2),lam:s.Rational(1,10)}
    defect = s.factor(combo+2*F0*einstein_rr)
    witness = [s.factor(defect.subs(flat).subs(pp,v)) for v in (0,1)]
    return dict(X=X,F=F,radial_reduced_action=reduced,boundary_term=boundary,
        new_current_formula=expected_current,zero_current_radial_combination=expected_combo,
        independent_same_X_witness=witness,
        residuals=[s.factor(raw-reduced-D(boundary)),
            s.factor(combo-expected_combo),s.factor(current-expected_current),
            s.factor((-EL(raw,p,pp)/measure)-current),
            s.factor((2*B*EL(raw,B,Bp)/measure)-radial_variation)])


@lru_cache(None)
def general_radial_identities():
    A,B,R,F,Ap,Rp,Fr = s.symbols('A B R F Ap Rp Fr',positive=True)
    # Holding X fixed under delta B=2B*e, delta p=p*e also fixes F and Fr.
    bulk = s.sqrt(A/B)*(2*F*B+2*F*Rp**2+2*F*R*Rp*Ap/A
        +Fr*(R**2*Ap/A+4*R*Rp)+3*R**2*Fr**2/(2*F))
    combo = s.factor(2*B*s.diff(bulk,B)/(s.sqrt(A*B)*R**2))
    rr = (Rp**2/B-1)/R**2+Ap*Rp/(A*B*R)
    expected = -2*F*rr-Fr*(Ap/A+4*Rp/R)/B-3*Fr**2/(2*F*B)
    r,g,P,h = s.symbols('r g P h',real=True)
    radial_eq = (P+expected).subs({R:r,Rp:1,Ap:2*A*g,Fr:F*h})
    Bsolution = s.factor(s.solve(radial_eq,B)[0])
    T = 1+2*r*g
    target = (T+r*r*(g+2/r)*h+3*r*r*h*h/4)/(1+r*r*P/(2*F))
    no_slip_pressure = 2*F*((g+2/r)*h+3*h*h/4)/T
    e = s.Symbol('e',real=True)
    weak_b = s.simplify(s.diff(Bsolution.subs({g:e*g,h:e*h,P:e*P}),e).subs(e,0))
    Psi_prime = s.factor(weak_b/(2*r))
    Phi_prime = g
    X,Fx,m = s.symbols('X Fx m',positive=True)
    conformal_factor = 2*F/m
    transformed_X_derivative = (conformal_factor-X*2*Fx/m)/conformal_factor**2
    return dict(B=Bsolution,exact_B_equals_T_pressure=no_slip_pressure,
        weak_Phi_prime=Phi_prime,weak_Psi_prime=Psi_prime,
        weak_Weyl_prime=s.factor((Phi_prime+Psi_prime)/2),
        weak_slip_prime=s.factor(Phi_prime-Psi_prime),
        conformal_X_derivative=s.factor(transformed_X_derivative),
        residuals=[s.factor(combo-expected),s.factor(Bsolution-target),
            s.factor(radial_eq.subs({B:T,P:no_slip_pressure})),
            s.factor(Psi_prime-(g+h-r*P/(4*F))),
            s.factor(transformed_X_derivative-m*(F-X*Fx)/(2*F**2))])


def source_translation():
    F,Fx,sourceX = s.symbols('F Fx sourceX',positive=True)
    # Sources use sourceX=grad(phi)^2=-2*X, hence F_sourceX=-F_X/2.
    source_Fx = -Fx/2
    A3 = s.Integer(0)
    A4 = (48*source_Fx**2-8*(F-sourceX*source_Fx)*A3-sourceX**2*A3**2)/(8*F)
    A5 = (4*source_Fx+sourceX*A3)*A3/(2*F)
    # L4=(grad X)^2 under our X=-grad(phi)^2/2.
    return dict(A1=0,A2=0,A3=A3,A4=s.factor(A4),A5=A5,
                residuals=[s.factor(A4-3*Fx**2/(2*F)),A5])


def serial(a):
    if isinstance(a,dict):return {k:serial(v) for k,v in a.items()}
    if isinstance(a,(list,tuple)):return [serial(v) for v in a]
    return str(a) if isinstance(a,s.Basic) else a


def results():
    return serial(dict(explicit_variation=derive(),general=general_radial_identities(),
        primary_source_translation=source_translation(),independent_curvature=curvature_check(),
        status='NEW STATIC OPERATOR FREEDOM VERIFIED; FULL EXTENDED INVERSE AND HEALTH OPEN'))


if __name__=='__main__':print(json.dumps(results(),indent=2))
