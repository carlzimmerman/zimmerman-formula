"""Independent post-comparison scalar normalization and order-counting checks."""
import json
import pathlib
import sys
import sympy as s

g, k, M, SQ, beta0, beta1, H, L, unknown = s.symbols("g k M SQ beta0 beta1 H L unknown",nonzero=True)
Sigma = s.symbols("Sigma")  # sum (1+gamma_mq) sigma_q
beta = -beta0*g**3*k
trace_H = 2*g*(M-Sigma)/beta
checks=[]
def eq(name, left, right):
    residual=s.factor(left-right)
    if residual!=0:raise AssertionError((name,str(residual)))
    checks.append({"name":name,"residual":"0"})

# RG + dimensional homogeneity: beta*dM/dg=-M+Sigma.
dM_from_RG=(-M+Sigma)/beta
eq("coupling_derivative_equals_canonical_gluon_insertion",dM_from_RG,-trace_H/(2*g))
# Rescaled field calG=g*G; changing the coupling in -calG^2/(4g^2)
# gives dL/dg=G^2/(2g), and Feynman-Hellmann changes the mass by minus its insertion.
calG2=s.symbols("calG2")
eq("canonical_action_derivative",s.diff(-calG2/(4*g**2),g).subs(calG2,g**2*H),H/(2*g))
dg=g**3*SQ*k**2*(L-s.Rational(3,4))
Bg=k**2*g**2*SQ*H/(2*M)
eq("proton_threshold_sign_and_factor",dg*(-H/(2*g))/M,-Bg*(L-s.Rational(3,4)))
eq("trace_expression_for_Bg",Bg.subs(H,trace_H),-SQ*k/beta0*(1-Sigma/M))
SQ3=sum(q*q for q in [s.Rational(2,3),s.Rational(-1,3),s.Rational(-1,3)])
eq("three_flavor_charge_sum",SQ3,s.Rational(2,3))
Bg3=s.factor(Bg.subs(H,trace_H).subs({SQ:SQ3,beta0:9,Sigma:0,k:1/(16*s.pi**2)}))
eq("massless_three_flavor_Bg",Bg3,-1/(216*s.pi**2))
eq("finite_local_matching_constant",s.Rational(3,4)*Bg3,-1/(288*s.pi**2))
# A not-yet-calculated next gluon Wilson coefficient is parametrically relevant.
next_dg=g**5*k**3*unknown
next_response=s.factor((next_dg*dM_from_RG/M).subs(Sigma,0))
eq("missing_next_gluon_enters_relative_g_squared",next_response,g**2*k**2*unknown/beta0)
# Higher terms of beta modify the same leading expression only at O(g^2).
beta_two=-beta0*g**3*k-beta1*g**5*k**2
Bg_two=s.factor((g**3*SQ*k**2/beta_two))
eq("two_loop_trace_same_chiral_leading_limit",s.limit(Bg_two,g,0),-SQ*k/beta0)
eq("vector_piece_extractable_without_axial_finite_assumption",s.Rational(3,5)*(s.Rational(10,3)*L-s.Rational(5,2)),2*L-s.Rational(3,2))

result={"check_count":len(checks),"checks":checks,"finite_chiral_local_constant":str(s.Rational(3,4)*Bg3),"next_gluon_response_per_u":str(next_response),"interpretation":"The matched Nf=3 chiral local subtraction is verified algebraically at leading strong order. The unknown next gluon coefficient contributes at the displayed mixed-quark hadronic order.","non_claims":["No matrix element computed", "No proton full mass response or QCD R", "No alpha value", "No all-order sharp-heavy equality"]}
pathlib.Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"check_count":len(checks),"all_passed":True}))
