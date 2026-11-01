"""Exact canonical tadpole, axion/radial cubic, and net-CC sensitivity identities."""
import sys
sys.dont_write_bytecode=True
import json,argparse,resource
from pathlib import Path
import sympy as S


def main(out):
    R,sg,aa,t=S.symbols('R sigma axion t',positive=True)
    u0,u1,u2,u3,J=S.symbols('u0 u1 u2 u3 J',real=True)
    rad=S.series(S.sqrt((R+t*sg/S.sqrt(2))**2+t*t*aa*aa/2),t,0,4).removeO()
    dr=rad-R
    V=S.series(u0+u1*dr+u2*dr**2/2+u3*dr**3/6-J*(R+t*sg/S.sqrt(2)),t,0,4).removeO().expand()
    checks={}
    def zero(name,x):checks[name]=S.simplify(x)==0;assert checks[name],name
    zero('stationarity_linear_cartesian',V.coeff(t,1).subs(J,u1))
    zero('radial_canonical_mass2',S.diff(V.coeff(t,2),sg,2)-u2/2)
    zero('axion_canonical_mass2',S.diff(V.coeff(t,2),aa,2)-u1/(2*R))
    zero('physical_sigma_aa_cubic',S.diff(V.coeff(t,3),sg,1,aa,2)-(u2-u1/R)/(2*S.sqrt(2)*R))
    ms2,ma2=S.symbols('m_sigma2 m_axion2',positive=True)
    zero('cubic_mass_dictionary',((u2-u1/R)/(2*S.sqrt(2)*R)).subs({u2:2*ms2,u1:2*R*ma2})-(ms2-ma2)/(S.sqrt(2)*R))
    Us,Uss,A,F=S.symbols('U_s U_ss A F',positive=True)
    zero('log_radial_hessian',u2.subs({u2:(Uss-Us)/R**2})-(Uss-Us)/R**2)
    zero('general_pair_threshold',(Uss-Us)/(2*A)-4*Us/(2*F)-(F*Uss-(F+4*A)*Us)/(2*A*F))
    zero('canonical_pair_threshold',(F*Uss-(F+4*A)*Us).subs(A,F)-F*(Uss-5*Us))
    mp,fw,w0,rho=S.symbols('M_P F_eff W_0 rho',positive=True)
    net=fw*fw-3*w0*w0/(mp*mp)
    zero('CC_value_after_tuning',net.subs(w0,mp*S.sqrt((fw*fw-rho)/3))-rho)
    zero('CC_fractional_sensitivity',S.diff(net,w0)*w0+6*w0*w0/mp**2)
    zero('relative_CC_tuning',rho/(6*w0*w0/mp**2).subs(w0,mp*S.sqrt((fw*fw-rho)/3))-rho/(2*(fw*fw-rho)))
    # Euler identity on a generic cubic+linear W: all cubic terms cancel
    # from the canonical term 2W0(sum z_i Wi-3W)/M_P².
    x,y,z,f,a,b,c=S.symbols('x y z f a b c',real=True)
    W=f*x+a*x*y*y+b*y*y*z+c*z*z*z
    Euler=sum(q*S.diff(W,q) for q in [x,y,z])-3*W
    zero('canonical_W0_only_linear_tadpole',2*w0*Euler/mp**2+4*f*w0*x/mp**2)
    result=dict(claim_id='TP05_COORDINATOR_STRUCTURES',checks=checks,all_checks_pass=all(checks.values()),peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                scope='Exact canonical/leading-gravity identities, not a stationary SU5 vacuum or a production result.',
                non_claims=['No full supergravity threshold/loop result','No completed V3 khronon embedding','No selected residual cosmological constant'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
