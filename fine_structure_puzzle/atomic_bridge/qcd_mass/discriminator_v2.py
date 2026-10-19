#!/usr/bin/env python3
"""FSP-Q bounded exact RG/matching discriminator; no experimental fitting.

Run from repository root, supplying a new result path created by the runner.
The sole nonstdlib dependency is SymPy 1.14.0. Every identity below is exact
in the explicitly stated one-loop or leading chiral/QED truncation, not an
all-orders claim about four-dimensional QCD in cosmological spacetime.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    checks = []

    def check(label, expr):
        ok = bool(expr)
        checks.append({"name": label, "pass": ok})
        if not ok:
            raise AssertionError(label)

    # Log scales are relative to a fixed unit M_ref. beta_n refers to d/dln(mu).
    b = {n: s.Rational(33 - 2*n, 3) for n in range(3, 7)}
    L6, ct, cb, cc = s.symbols("log_Lambda6 log_mt log_mb log_mc", real=True)
    # alpha_(n-1)(m_h)=alpha_n(m_h), exact at this one-loop order.
    L5 = (b[6]*L6 + (b[5]-b[6])*ct)/b[5]
    L4 = (b[5]*L5 + (b[4]-b[5])*cb)/b[4]
    L3 = s.expand((b[4]*L4 + (b[3]-b[4])*cc)/b[3])
    expected_L3 = s.Rational(7, 9)*L6 + s.Rational(2, 27)*(cc+cb+ct)
    check("sequential_thresholds_equal_closed_form", s.simplify(L3-expected_L3) == 0)
    # Independent telescoping invariant: b3 lnLambda3−b6 lnLambda6 = 2/3 sum ln mh.
    check("threshold_telescoping_invariant", s.simplify(b[3]*L3-b[6]*L6-s.Rational(2, 3)*(cc+cb+ct)) == 0)
    # All masses scaled together must scale Lambda3 once, no extra dimension.
    check("threshold_scaling_dimension_one", sum(s.diff(L3,t) for t in (L6,ct,cb,cc)) == 1)

    u, A, le, M = s.symbols("inverse_alpha_s_M inverse_alpha_M log_me log_M", real=True)
    L3uv = s.expand(L3.subs(L6, M-2*s.pi*u/b[6]))
    # Heavy Dirac quarks and the electron in perturbative QED; other thresholds are held
    # in independent matching remainder Delta. Light quarks are NOT free quarks
    # below confinement; the low-energy hadronic remainder requires HVP matching.
    Qc, Qb, Qt = s.Rational(2,3), -s.Rational(1,3), s.Rational(2,3)
    k = [2*3*q*q/(3*s.pi) for q in (Qc,Qb,Qt)]
    Delta = s.Symbol("other_matching_remainder", real=True)
    A0 = A + 2*(M-le)/(3*s.pi) + sum(w*(M-z) for w,z in zip(k,(cc,cb,ct))) + Delta
    params = (u,cc,cb,ct,A,le)
    # This pure-QCD leading limit favors the proposal: c_H and C_p are known,
    # quark ratios fixed. H~Lambda3^3, mp~Lambda3; their derivative rows coincide.
    observables = s.Matrix([3*L3uv,L3uv,A0,le])
    J = observables.jacobian(params)
    check("pure_QCD_vacuum_plus_mp_rank_one", J[:2,:].rank() == 1)
    check("including_charge_and_electron_output_rank_three", J.rank() == 3)
    eA = s.Matrix([0,0,0,0,1,0])
    ee = s.Matrix([0,0,0,0,0,1])
    check("vacuum_and_mp_leave_EM_integration_constant", J[:2,:]*eA == s.zeros(2,1))
    check("EM_integration_constant_changes_inverse_alpha0", (J*eA)[2] == 1)
    check("vacuum_and_mp_leave_electron_Yukawa", J[:2,:]*ee == s.zeros(2,1))
    check("electron_parameter_changes_log_me", (J*ee)[3] == 1)
    check("electron_threshold_response_in_inverse_alpha0", (J*ee)[2] == -2/(3*s.pi))

    # Stronger discriminator retaining proton EM mass and EM correction to the
    # candidate vacuum coefficient. Leading chiral matching C_H=d*q/Lambda,
    # plus leading O(alpha), with fixed low-energy constants d,v,C0,cq,cg.
    # These are symbolic fixed coefficients, NOT fitted values. Lambda and q
    # are independent QCD scale and light-quark mass integration constants.
    L,q,a = s.symbols("Lambda q alpha", positive=True)
    d,C0,cq,cg,v = s.symbols("d C0 cq cg v", real=True)
    H = d*q*L**2*(1+v*a)
    mp = (C0+cg*a)*L+cq*q
    O = s.Matrix([H,mp])
    K = O.jacobian((L,q,a))
    det = s.factor(K[:,:2].det())
    D = C0+cg*a-2*cq*q/L
    check("hadron_compensation_minor", s.simplify(det+d*L**2*(1+v*a)*D) == 0)
    # No normalization ambiguity in this null vector: set delta alpha=1.
    zL = s.factor(-(cg*L-cq*q*v/(1+v*a))/D)
    zq = s.factor(-q*(2*zL/L+v/(1+v*a)))
    tangent = s.Matrix([zL,zq,1])
    check("EM_sensitive_hadron_vacuum_null_direction", all(s.simplify(x)==0 for x in K*tangent))
    check("null_direction_really_changes_alpha", tangent[2] == 1)
    # Independent elimination: H=H* -> q=H*/[d Lambda²(1+v alpha)].
    hs = s.Symbol("fixed_H", positive=True)
    reduced_mp = mp.subs(q,hs/(d*L**2*(1+v*a)))
    check("implicit_curve_tangent_matches_elimination", s.simplify((s.diff(reduced_mp,L)*zL+s.diff(reduced_mp,a)).subs(hs,H)) == 0)
    # A useful positive control: if q is independently supplied and all matching
    # functions are known, a pair of measured H,mp CAN in principle determine a.
    # We report the determinant rather than declaring universal nonidentifiability.
    K_known_q = K[:,[0,2]]
    det_known_q = s.factor(K_known_q.det())
    check("known_quark_mass_can_restore_local_rank", det_known_q != 0)
    check("zero_EM_limit_exposes_selector_loss", det_known_q.subs({cg:0,v:0}) == 0)

    out = {
        "claim_id":"FSP-Q-002",
        "assertion_tested":"Exact threshold and Jacobian identities in declared RG and leading matching truncations",
        "checks":checks,
        "thresholds":{"b_n":{str(n):str(x) for n,x in b.items()},"log_Lambda3":str(L3),"log_Lambda3_UV":str(L3uv),"inverse_alpha0":str(A0)},
        "pure_QCD":{"parameter_order":[str(x) for x in params],"Jacobian":str(J),"rank_H_mp":int(J[:2,:].rank()),"rank_all_outputs":int(J.rank()),"EM_null_vector_fixed_H_mp":list(map(str,eA)),"electron_null_vector_fixed_H_mp":list(map(str,ee))},
        "EM_sensitive_chiral_matching":{"H":str(H),"mp":str(mp),"parameter_order":[str(x) for x in (L,q,a)],"Jacobian":str(K),"compensation_minor":str(det),"null_tangent_delta_alpha_1":list(map(str,tangent)),"known_q_selector_determinant":str(det_known_q),"regular_domain":"Lambda,q,d>0; 1+v*alpha !=0; C0+cg*alpha−2*cq*q/Lambda !=0; truncation corrections small"},
        "interpretation":"Vacuum/proton matching leaves an alpha-varying curve if light-quark mass is not independently selected; with independent quark mass and fully calculated matching coefficients, alpha may be locally identifiable.",
        "non_claims":["No numerical alpha prediction", "No proof of the QCD topological cosmological term", "No all-orders SM exclusion", "No lattice coefficient calculation", "No electron Yukawa selection", "No nonperturbative light-quark QED threshold approximation"]
    }
    Path(args.output).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":len(checks),"all_passed":all(c["pass"] for c in checks),"rank_H_mp":1,"rank_all_outputs":3,"EM_sensitive_null_direction":True,"known_q_control":"generically can restore alpha identifiability"}))


if __name__ == "__main__":
    main()
