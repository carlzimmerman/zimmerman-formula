#!/usr/bin/env python3
"""Exact algebra behind the stationary-flow obstruction, with scope witnesses."""
import argparse,json
from pathlib import Path
import sympy as s


def main(output):
    Q,Qr,B,Br,Pr,divP,HQ,nr=s.symbols('Q Qr B Br Pr divP HQ nr',nonzero=True)
    b=B/Q;br=Br/Q-B*Qr/Q**2
    Pi=divP+Pr*Qr/Q
    rho=HQ+(B*divP+Pr*Br)/Q
    direct=nr*(rho-Pr*br)
    factor=nr*(HQ+b*Pi)
    checks={'exact_static_radial_current_factor':s.simplify(direct-factor)==0,
            'omit_Q_derivative_mutant_rejected':s.simplify(nr*(rho-Pr*Br/Q)-factor)!=0,
            'ungated_factor_limit':s.simplify((HQ+b*Pi).subs(B,1)-(HQ+Pi/Q))==0}
    # Algebraic witness only: rho_Q>0 alone does not imply the coefficient>0.
    witness={Q:1,Qr:0,B:1,Br:1,Pr:1,divP:0,HQ:0}
    checks['positive_rho_does_not_imply_positive_flow_coefficient']=rho.subs(witness)==1 and (HQ+b*Pi).subs(witness)==0
    # Direct nonconstant integration-by-parts check with positive periodic n.
    x=s.symbols('x',real=True);n=1+s.cos(x)/2;sig=s.sin(x)
    bulk=s.integrate(n*s.diff(sig,x)**2,(x,0,2*s.pi))
    integrated_eq=s.integrate(sig*s.diff(n*s.diff(sig,x),x),(x,0,2*s.pi))
    checks['stationary_NR_energy_identity']=s.simplify(integrated_eq+bulk)==0
    checks['nonconstant_test_has_strict_positive_energy']=bulk==s.pi
    # Non-single-valued potential on a circle is an actual circulation exception.
    checks['constant_circulation_divergence_free']=s.diff(s.Integer(2)*s.diff(x,x),x)==0
    checks['circulation_potential_not_periodic']=s.simplify(x.subs(x,2*s.pi)-x.subs(x,0))==2*s.pi
    result={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':all(checks.values()),
            'count':len(checks),'factor':str(factor),'positive_density_witness_rho':str(rho.subs(witness)),
            'positive_density_witness_flow_coefficient':str((HQ+b*Pi).subs(witness)),
            'scope':'Exact current identity and integration-by-parts evidence; positivity witness is algebraic, not a full covariant solution'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
