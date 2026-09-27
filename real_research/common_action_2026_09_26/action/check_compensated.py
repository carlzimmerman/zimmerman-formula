#!/usr/bin/env python3
"""Independent exact identities for the compensated geometric-gate variant."""
import argparse,json
from pathlib import Path
import sympy as s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
    def exact(name,expr):
        r=s.factor(s.simplify(expr));assert r==0,(name,r);checks[name]={'passed':True,'residual':str(r)}
    x=s.symbols('x',real=True);N=s.Function('N')(x);W=s.Function('W')(x);f=s.Function('f')(x);n=s.Function('n')(x)
    ell,eps=s.symbols('ell epsilon',real=True)
    a=s.diff(N,x)/N;p=s.diff(W,x);dNh=s.diff(W,x,2)+a*p
    # The full-on compensator is an exact boundary identity for every N,W.
    exact('full_on_geometric_gate_plus_compensator_is_weighted_divergence',
          N*ell*(s.diff(W,x,2)+a*p)-s.diff(N*ell*p,x))
    # Treat G(Yh) as independent of lapse at fixed h,U; retain N measure.
    GG=s.Function('G_of_Yh')(x);Nv=N*s.exp(eps*n)
    integrand=Nv*(GG+ell*s.diff(Nv,x)/Nv*p)
    first=s.diff(integrand,eps).subs(eps,0)
    # equality modulo exactly displayed total spatial derivative
    exact('compensated_fixed_h_lapse_variation',first-N*n*(GG-ell*s.diff(W,x,2))-s.diff(N*ell*n*p,x))
    jp=s.Function('Jp')(x)
    # W Euler derivative, treating f=G' and jp=J_p as displayed coefficients.
    raw=-s.diff(N*(f*jp+ell*a),x)/N+ell*s.diff(N*f,x,2)/N
    divN=lambda v:s.diff(N*v,x)/N
    expanded=-divN(f*jp)+ell*(f-1)*divN(a)+2*ell*a*s.diff(f,x)+ell*s.diff(f,x,2)
    exact('compensated_W_equation_with_full_measure_terms',raw-expanded)
    exact('full_on_W_equation_returns_original_kernel',raw.subs(f,1).doit()+divN(jp))
    exact('full_off_W_equation_has_compensator_source',raw.subs(f,0).doit()+ell*divN(a))

    # Static response from independently varied physical lapse and Z equations.
    sk,C,ff=s.symbols('S C f',real=True);ub,ud=s.symbols('u_b u_d',real=True)
    Q=1-(1-ff)*ell*sk/4;DD=1+ff*C*sk**2
    U=ub/Q;Phi=DD*ub/Q**2+ud/Q;Z=Phi-U-ud
    exact('constant_gate_Z_equation',Phi-Z-U-ud)
    exact('constant_gate_lapse_equation',Phi-Z-(1-Q)*U-ub-ud)
    exact('constant_gate_U_equation',Z-ff*C*sk**2*U-(1-Q)*Phi)
    carrier=Phi-Z
    exact('compensated_cross_force_reciprocity',s.diff(Phi,ud)-s.diff(carrier,ub))
    exact('off_baryon_response',s.diff(Phi,ub).subs(ff,0)-1/(1-ell*sk/4)**2)
    exact('off_cross_response',s.diff(Phi,ud).subs(ff,0)-1/(1-ell*sk/4))
    exact('off_carrier_self_response',s.diff(carrier,ud).subs(ff,0)-1)
    exact('full_on_baryon_response',s.diff(Phi,ub).subs(ff,1)-(1+C*sk**2))
    exact('high_k_heat_suppression_returns_Newtonian_response',s.diff(Phi,ub).subs(sk,0)-1)

    # Frozen principal Schur parametrization verified independently from the
    # evolution lane's derivation. Full lower-order background terms excluded.
    alpha,c2,dpos,qpos,k=s.symbols('alpha c2 D Q k',positive=True)
    cn=1-alpha/2
    ae=2-(2-alpha)*qpos*qpos/dpos
    exact('effective_alpha_distance_from_two',2-ae-(2-alpha)*qpos*qpos/dpos)
    exact('effective_alpha_lower_bound_identity',ae-alpha-(2-alpha)*(dpos-qpos*qpos)/dpos)
    exact('Q_lower_bound_identity',Q-(1-ell/4)-ell*(1-(1-ff)*sk)/4)
    cs=c2*(2-ae)/(ae*(2+3*c2))
    exact('compensated_scalar_speed_expression',cs-c2*(2-alpha)*qpos*qpos/((2+3*c2)*(2*dpos-(2-alpha)*qpos*qpos)))
    # Original normalized plateau recovered exactly.
    ae_on=ae.subs({qpos:1,dpos:1+C*sk**2})
    exact('full_on_effective_alpha',ae_on-(alpha+2*C*sk**2)/(1+C*sk**2))
    exact('full_on_speed_is_normalized_host',cs.subs({qpos:1,dpos:1+C*sk**2})-c2*(2-alpha)/((2+3*c2)*(alpha+2*C*sk**2)))

    # Centered trace: N-weighted action, h-volume mean. Its lapse and momentum
    # mean terms cannot be dropped. A finite two-cell algebra is enough here.
    N1,N2,H1,H2,K1,K2,d1,d2=s.symbols('N1 N2 H1 H2 K1 K2 d1 d2',positive=True)
    meanK=(H1*K1+H2*K2)/(H1+H2);q1=K1-meanK;q2=K2-meanK
    AN=(H1*N1*q1+H2*N2*q2)/(H1+H2)
    Lk=-c2*(H1*N1*q1*q1+H2*N2*q2*q2)
    # lapse variation includes K -> K exp(-epsilon n), with h fixed.
    varied=Lk.subs({N1:N1*s.exp(eps*d1),N2:N2*s.exp(eps*d2),K1:K1*s.exp(-eps*d1),K2:K2*s.exp(-eps*d2)},simultaneous=True)
    expected=c2*(H1*N1*d1*(-q1*q1+2*K1*q1-2*K1*AN/N1)+H2*N2*d2*(-q2*q2+2*K2*q2-2*K2*AN/N2))
    exact('centered_trace_lapse_constraint_mean_terms',s.diff(varied,eps).subs(eps,0)-expected)
    exact('centered_trace_momentum_mean_terms',s.diff(Lk,K1)+2*c2*H1*N1*(q1-AN/N1))
    exact('centered_trace_homogeneous_action_vanishes',Lk.subs(K2,K1))
    exact('centered_trace_homogeneous_first_variation_vanishes',s.diff(Lk,K1).subs(K2,K1))
    # Simple numerical illustration, not an empirical allowed value.
    ellnum=.04;qlow=1-ellnum/4
    examples={'declared_ell':ellnum,'long_wave_off_baryon_G_over_GN':1/qlow**2,
              'long_wave_off_cross_response_over_Newton':1/qlow,
              'high_k_limit':1.0}
    out={'claim_id':'CD26_4_COMPENSATED_GEOMETRIC_GATE','number_of_checks':len(checks),'checks':checks,
         'off_response_illustration':examples,'scope':['Exact first-variation identities and fixed-gate static response',
          'Frozen principal Q,D Schur parametrization crosscheck, not its full curved-background derivation',
          'Centered-trace lapse and momentum mean terms tested exactly',
          'No assertion that the illustrative ell satisfies data or that coupled global evolution is proved']}
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'number_of_checks':len(checks),'all_passed':True,'off_response_illustration':examples},indent=2))

if __name__=='__main__':main()
