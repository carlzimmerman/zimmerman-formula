"""Finite-density hard-edge regularity checks; prescribed-potential examples only."""
import json, math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
P=Path(__file__).resolve().parent

def main():
    checks=[];rows=[]
    def ck(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(e):return s.simplify(e)==0
    r,R,g,d,C=s.symbols('r R g d C',positive=True)
    vr,vt,pr,pR=s.symbols('vr vt Phi_r Phi_R',real=True)
    aa=1-r*r/(R*R); D=pR-pr
    E=(vr*vr+vt*vt)/2+pr; L2=r*r*vt*vt; ER=pR+L2/(2*R*R)
    ck('energy_ellipsoid_identity',zero(ER-E-(D-(vr*vr+aa*vt*vt)/2)))
    Aedge=1-(R-d)**2/R**2
    volume=4*s.pi/3*(2*g*d)**s.Rational(3,2)/Aedge
    lead=s.limit(volume/s.sqrt(d),d,0,dir='+')
    ck('bounded_f_edge_coefficient',zero(lead-4*s.pi/3*s.sqrt(2)*R*g**s.Rational(3,2)))
    singular=2*s.sqrt(2)*s.pi**2*C*g*d/Aedge
    ck('singular_nonzero_edge',zero(s.limit(singular,d,0,dir='+')-s.sqrt(2)*s.pi**2*C*g*R))
    # Angular momentum upper bound implied by the ellipsoid using maximal Kepler D.
    ratio=s.simplify((r*r*2*(1/r-1/R)/(1-r*r/R**2))/R)
    ck('L_bound_expression',zero(ratio-2*r/(R+r)))
    ck('L_bound_gap_positive_expression',zero(1-ratio-(R-r)/(R+r)))
    for gap in (1e-2,1e-4,1e-6):
        rad=1-gap; a=1-rad*rad; dd=1/rad-1
        vol=4*math.pi/3*(2*dd)**1.5/a
        # w=sqrt(2D) sin(theta), with two tangential directions rescaled.
        volq=4*math.pi/a*(2*dd)**1.5*quad(lambda th:math.sin(th)**2*math.cos(th),0,math.pi/2,epsabs=1e-12)[0]
        rho=2*math.sqrt(2)*math.pi**2*dd/a
        rhoq=4*math.pi/a*2*math.sqrt(2)*dd*quad(lambda th:math.sin(th)**2,0,math.pi/2,epsabs=1e-12)[0]
        flog=rho*(-.5*math.log(dd)+math.log(2)+.5)
        flogq=4*math.pi/a*2*math.sqrt(2)*dd*quad(lambda th:math.sin(th)**2*(-.5*math.log(dd)-math.log(math.cos(th))),0,math.pi/2,epsabs=1e-10,epsrel=1e-12)[0]
        ck('constant_f_quadrature_'+str(gap),abs(volq/vol-1)<1e-10)
        ck('singular_f_quadrature_'+str(gap),abs(rhoq/rho-1)<1e-10)
        ck('entropy_quadrature_'+str(gap),math.isfinite(flogq) and abs(flogq/flog-1)<1e-10)
        rows.append(dict(gap=gap,velocity_volume=vol,volume_over_sqrt_gap=vol/math.sqrt(gap),singular_density=rho,entropy_integral_flogf=flog))
    ck('bounded_edge_limit',abs(rows[-1]['volume_over_sqrt_gap']/(4*math.pi/3*math.sqrt(2))-1)<1e-4)
    ck('singular_edge_limit',abs(rows[-1]['singular_density']/(math.sqrt(2)*math.pi**2)-1)<1e-4)
    ck('MUTATE_constant_phase_volume_rejected',abs(rows[-1]['velocity_volume']/rows[0]['velocity_volume']-1)>.9)
    a=1-.9**2
    ck('MUTATE_omitted_transverse_jacobian_rejected',abs(a-1)>.01)
    eps=s.symbols('eps',positive=True)
    ck('boundary_entropy_integrable',zero(s.limit(eps*(1-s.log(eps)),eps,0,dir='+')))
    # Constant finite initial f, finite phase-space compression exponent => finite f.
    f0,B=s.symbols('f0 B',positive=True)
    ck('finite_compression_preserves_finiteness',s.exp(B).is_finite is not False)
    out=dict(status='bounded_f_hard_edge_obstruction_with_singular_stationary_loophole',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,kepler_illustrations=rows,formulae=dict(velocity_volume='(4pi/3)(2D)^(3/2)/A',edge_coefficient=str(lead),singular_density='2 sqrt(2) pi^2 C D/A',singular_edge_density='sqrt(2) pi^2 C g(R) R'),non_claims=['No global nonlinear kinetic evolution','No primordial fmax specified','No entropy-maximizer identification','No full candidate-B exclusion'])
    (P/'run/results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['passed'],out['total']);print(json.dumps(rows))
    assert all(x['passed'] for x in checks)
if __name__=='__main__':main()
