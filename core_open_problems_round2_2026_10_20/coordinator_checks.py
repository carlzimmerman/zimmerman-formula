#!/usr/bin/env python3
"""Independent algebra from raw ADM action and band density of states."""
import argparse, json
from pathlib import Path
import sympy as s

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True); args=parser.parse_args()
    checks=[]
    def eq(name, actual, expected=0):
        residual=s.simplify(actual-expected)
        checks.append({'name':name,'passed':residual==0,'residual':str(residual)})
        assert residual==0,(name,residual)
    e,c,H,z,zd,n,Y,b,p,K=s.symbols('e c H z zd n Y b p K',real=True)
    A=2+3*b
    # Exact diagonal ADM curvature extrinsic combination before expansion.
    V=H+e*zd*c+e**2*Y*z*(1-c*c)
    volume=(1+3*e*z*c+s.Rational(9,2)*e**2*z*z*c*c)
    inv_lapse=1-e*n*c+e**2*n*n*c*c
    q=volume*inv_lapse*(-3*A*V*V+2*A*V*e*Y*c-b*e**2*Y*Y*c*c)-3*A*H*H*(1+e*n*c)*volume
    q=s.expand(2*s.expand(q).coeff(e,2)).subs(c*c,s.Rational(1,2))
    q=s.expand(q+2*p*p*z*z+4*p*p*n*z)
    cross=q.coeff(z,1).coeff(zd,1)
    q=s.expand(q-cross*z*zd-cross*3*H*z*z/2)
    expected=-3*A*(zd-H*n)**2+2*A*(zd-H*n)*Y-b*Y*Y+2*p*p*z*z+4*p*p*n*z
    eq('direct_ADM_scalar_Fourier_expansion',q,expected)
    sig,sd,eta,gamma,Z,Zd=s.symbols('sig sd eta gamma Z Zd',real=True)
    C=A/(K*b); B=C*K*K
    L=expected/(4*K)+p*p*n*sig+eta*p*p*sd*sd/2-K*p*p*sig*sig/2-gamma*p**4*sig*sig/2
    Ysol=A*(zd-H*n)/b
    eq('shift_equation',s.diff(L,Y).subs(Y,Ysol))
    L=s.simplify(L.subs(Y,Ysol))
    nsol=zd/H-p*p*(z/K+sig)/(C*H*H)
    eq('lapse_equation',s.diff(L,n).subs(n,nsol))
    L=s.expand(L.subs(n,nsol).subs({z:K*(Z-sig),zd:K*(Zd-sd)}))
    # a^3 p^2 has logarithmic derivative H, on exact de Sitter.
    L=s.expand(L-K*p*p*Z*Zd/H-K*p*p*Z*Z/2)
    Zsol=-C*K*H*(sd+H*sig)/(p*p)
    eq('remaining_algebraic_scalar',s.diff(L,Z).subs(Z,Zsol))
    L=s.simplify(L.subs(Z,Zsol))
    eq('scalar_reduced_before_time_boundary',L,eta*p*p*sd*sd/2+B*(sd+H*sig)**2/2-gamma*p**4*sig*sig/2)
    eq('scalar_reduced_after_time_boundary',s.expand(L-B*H*sig*sd-s.Rational(3,2)*B*H*H*sig*sig),((B+eta*p*p)*sd*sd-(gamma*p**4+2*B*H*H)*sig*sig)/2)
    # Independent rank-one shift elimination, not a determinant-only inference.
    pl,pt1,pt2=s.symbols('pl pt1 pt2',real=True)
    P=s.Matrix([pl,pt1,pt2]); S=s.diag(-b/(2*K),1/(4*K),1/(4*K))
    delta=1+eta*(P.T*S.inv()*P)[0]
    ysol=eta*S.inv()*P*sd/delta
    eq('oblique_shift_constraint_norm',sum(x*x for x in ((S+eta*P*P.T)*ysol-eta*P*sd)))
    kin=eta*(sd-(P.T*ysol)[0])**2/2+(ysol.T*S*ysol)[0]/2
    eq('oblique_reduced_kinetic',kin,eta*sd*sd/(2*delta))
    m,cut,v,nu,lam,u,a0,cap=s.symbols('m cut v nu lam u a0 cap',positive=True)
    band=-((cut**2+m**2)**s.Rational(3,2)-cut**3-m**3)/(3*s.pi*v*v)
    # Differentiate against the upper limit to recover the original DOS integral.
    eq('band_integral_upper_limit',s.diff(band,cut),-cut*(s.sqrt(cut*cut+m*m)-cut)/(s.pi*v*v))
    eq('band_zero_cutoff',band.subs(cut,0))
    eq('band_small_mass_cubic_quartic',s.series(band,m,0,5).removeO(),-cut*m*m/(2*s.pi*v*v)+m**3/(3*s.pi*v*v)-m**4/(8*s.pi*v*v*cut))
    target_force=u*u/(K*(a0-cap*u))
    eq('target_quartic_sign_dictionary',s.series(target_force,u,0,4).removeO(),u*u/(K*a0)+cap*u**3/(K*a0*a0))
    payload={'scope':'Exact algebra under stated raw-action hypotheses, not all-background health or a microscopic origin proof','checks':checks,'passed':all(x['passed'] for x in checks),'sympy':s.__version__,'nonclaims':['k=0 constraint reduction','nonlinear stability','physical medium identification','n or kappa selection']}
    Path(args.output).write_text(json.dumps(payload,indent=2)+'\n');print(len(checks),'independent checks passed')
if __name__=='__main__':main()
