#!/usr/bin/env python3
"""Re-expand the NEW K(Q,tau) action; do not borrow the old Qdot equation."""
import json
import sympy as s


def main():
    a,H,M,A,B,Q,U,C=s.symbols('a H M2 A B Q U C',positive=True)
    qn=s.symbols('Qdot',real=True)
    K0,V,Lam=s.symbols('K0 V Lambda',real=True)
    z,zd,zx,zxx,sg,sd,sx,al,bx,bxx,t=s.symbols('z zd zx zxx sigma sd sx alpha bx bxx t',real=True)
    N=1+t*al
    q=(Q+t*sd-t*t*bx*sx/a**2)/N
    Y=s.exp(-2*t*z)*t*t*sx**2/a**2
    curv=s.exp(-2*t*z)*(-4*t*zxx-2*t*t*zx**2)/a**2
    h=H+t*zd-t*t*bx*zx/a**2
    density=a**3*s.exp(3*t*z)*(M/2*(N*(curv-2*Lam)+(-6*h*h+4*h*t*bxx/a**2)/N)
                  +U-N*V+N*(K0+A*(q-Q)+B*(q-Q)**2/2-C*Y))
    raw=s.expand(s.diff(density,t,2).subs(t,0)/(2*a**3))
    hd=-(U+Q*A)/(2*M)
    rates={a:a*H,H:hd,A:-3*H*A,Q:qn}
    def dt(v):return sum(s.diff(v,x)*d for x,d in rates.items())
    out=s.expand(raw.subs(bx*zx,-bxx*z).subs(bx*sx,-bxx*sg).subs(z*zxx,-zx**2))
    c=out.coeff(zd).coeff(z)
    out=s.expand(out-c*z*zd-(3*H*c+dt(c))*z*z/2)
    c=out.coeff(sd).coeff(z)
    out=s.expand(out-c*z*sd-c*sg*zd-(3*H*c+dt(c))*sg*z)
    out=s.factor(out.subs(V,3*M*H**2-Lam*M-Q*A+K0))
    expected=M*(-3*(zd-H*al)**2+(zx*zx-2*al*zxx+2*(zd-H*al)*bxx)/a**2) \
              +B*(sd-Q*al)**2/2-3*A*sg*zd-C*sx*sx/a**2+A*sg*bxx/a**2
    if s.factor(out-expected)!=0:raise AssertionError('new entropy action expansion')
    # Gradient-free terms suffice for the kinetic mixing after the finite-k shift solve.
    # The spatial-gradient block is identical because it contains no Qdot or K_tau.
    u,ud=s.symbols('u ud',real=True)
    e=qn/H+Q*U/(2*M*H**2); d=Q*A/(2*M*H); f=B*e+3*A
    kin=out.subs({zx:0,zxx:0,sx:0,bxx:0}).subs(al,zd/H+A*sg/(2*M*H))
    kin=s.expand(kin.subs({sg:u+Q*z/H,sd:ud+Q*zd/H+dt(Q/H)*z}))
    c=kin.coeff(zd).coeff(u)
    kin=s.expand(kin-c*u*zd-c*z*ud-(3*H*c+dt(c))*u*z)
    c=kin.coeff(zd).coeff(z)
    kin=s.expand(kin-c*z*zd-(3*H*c+dt(c))*z*z/2)
    target=B*(ud-d*u)**2/2-3*A*A*u*u/(4*M)+f*z*(ud-d*u)+e*f*z*z/2
    if s.factor(kin-target)!=0:raise AssertionError('new e/f kinetic reduction')
    k2,be=s.symbols('k2 beta',positive=True)
    rates[k2]=-2*H*k2 # physical wavenumber squared redshifts during time IBP
    fourier=out.subs({zx**2:a**2*k2*z**2,sx**2:a**2*k2*sg**2,zxx:-a**2*k2*z,bxx:-a**2*k2*be})
    lapse=s.solve(s.diff(fourier,be),al)[0]
    spatial=s.expand(fourier.subs(al,lapse).subs({sg:u+Q*z/H,sd:ud+Q*zd/H+dt(Q/H)*z}))
    for var in (u,z):
        coeff=spatial.coeff(zd).coeff(var)
        spatial=s.expand(spatial-coeff*var*zd-coeff*z*(ud if var==u else 0)
                         -(3*H*coeff+dt(coeff))*z*var/(1 if var==u else 2))
    D=U-Q*A+2*C*Q**2
    target_full=target-C*k2*u*u+k2*(A-2*C*Q)*u*z/H-k2*D*z*z/(2*H*H)
    if s.factor(spatial-target_full)!=0:raise AssertionError('full finite-k entropy action')
    pu,pz,ps,pa,I=s.symbols('pu pz ps palpha I',real=True)
    def pb(x,y,qs,pp):return s.factor(sum(s.diff(x,q)*s.diff(y,p)-s.diff(x,p)*s.diff(y,q) for q,p in zip(qs,pp)))
    velocity=s.solve(pu-s.diff(a**3*spatial,ud),ud)[0]
    ham=s.factor((pu*ud-a**3*spatial).subs(ud,velocity))
    secondary=-s.diff(ham,z)
    finite_matrix=s.Matrix([[pb(x,y,[u,z],[pu,pz]) for y in (pz,secondary)] for x in (pz,secondary)])
    R=3*A*f/B+k2*D/H**2
    if s.factor(finite_matrix[0,1]-a**3*R)!=0:raise AssertionError('finite-k Poisson matrix')
    # Genuine k=0 calculation, before division by a shift equation.
    hom=a**3*fourier.subs(k2,0).subs(A,I/a**3)
    hv=s.solve([pz-s.diff(hom,zd),ps-s.diff(hom,sd)],[zd,sd])
    hh=s.factor((pz*zd+ps*sd-hom).subs(hv))
    hc=s.diff(hh,al)
    ht=s.factor((dt(hc)+pb(hc,hh,[z,sg,al],[pz,ps,pa])).subs(A,I/a**3))
    hD=pz+3*I*sg
    if s.factor(ht-(-U*hD/(2*M)+(qn+3*H*I/(a**3*B))*ps))!=0:raise AssertionError('new homogeneous tertiary')
    change_basis=s.Matrix([[H,Q],[-U/(2*M),qn+3*H*I/(a**3*B)]])
    if s.factor(change_basis.det()-(H**2*f/B).subs(A,I/a**3))!=0:raise AssertionError('homogeneous constraint-basis determinant')
    hE=al+ps/(a**3*B*Q)
    hc_list=[pa,hc,hD,hE]
    hom_matrix=s.Matrix([[pb(x,y,[z,sg,al],[pz,ps,pa]) for y in hc_list] for x in hc_list])
    # Charge, exact dust background and clock background compatibility.
    m,mn=s.symbols('m mn',positive=True)
    qdot=-H*Q*mn/(1+m)
    udot=H*mn*Q*A+m*qdot*A-3*H*m*Q*A
    if s.factor(udot+A*qdot+3*H*m*Q*A)!=0:raise AssertionError('clock Euler-Lagrange background')
    rhodot=H*mn*Q*A+(1+m)*qdot*A-3*H*(1+m)*Q*A
    if s.factor(rhodot+3*H*(1+m)*Q*A)!=0:raise AssertionError('combined dust background')
    print(json.dumps(dict(new_action_quadratic_expansion=True,kinetic_reduction=True,
                         full_finite_k_action=True,finite_k_bracket=str(finite_matrix),finite_k_rank=finite_matrix.rank(),
                         homogeneous_bracket=str(hom_matrix),homogeneous_rank=hom_matrix.rank(),
                         homogeneous_constraint_basis_determinant=str(s.factor(change_basis.det())),
                         e=str(e),f=str(f),clock_background_EL_residual='0',dust_background_residual='0',
                         Qdot_is_independent_of_B=True,
                         scope='Fresh quadratic expansion and separated reduced finite-k/k=0 brackets; no nonlinear Dirac certificate'),indent=2))


if __name__=='__main__':main()
