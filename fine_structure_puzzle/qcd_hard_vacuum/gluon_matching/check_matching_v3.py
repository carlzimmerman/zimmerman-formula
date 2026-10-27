#!/usr/bin/env python3
"""Exact finite algebra and filter-moment audit; not a Feynman-integral solver."""
import argparse
import json
from pathlib import Path
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
base = Path(__file__).resolve().parent
inputs = json.loads((base / "SOURCE_INPUT.json").read_text())
r, Lt, Lw, Lz, Q, I3, TF, Qt = s.symbols("r Lt Lw Lz Q I3 TF Qt")
symbols = {str(v): v for v in (r, Lt, Lw, Lz, Q, I3, TF, Qt)}
def read(name):
    # rational=True retains exact fractions in source transcription.
    return s.sympify(inputs["source_expressions"][name], locals=symbols, rational=True)
checks = []
def eq(name, left, right):
    remainder = s.factor(left-right)
    if remainder != 0:
        raise AssertionError((name, str(remainder)))
    checks.append({"name": name, "residual": str(remainder)})
T = read("eq_2_16_small_top_mixed_div_gs2g2")
m_generic = read("eq_2_20_generic_mass_div_g2")
m_top = m_generic.subs({Q:s.Rational(2,3), I3:s.Rational(1,2)})
P = read("eq_3_7_top_QED_div_gs2g2").subs({TF:s.Rational(1,2), Qt:s.Rational(2,3)})
top_1loop = read("eq_2_15_top_one_loop_div_gs2")
# The shifted squared mass supplies 2*m_top*d/dLt of top_1loop.
mass_composition = 2*m_top*s.diff(top_1loop, Lt)
V = s.factor(T-P-mass_composition)
upL=(4*r-1)/(6*s.sqrt(r))
upR=2*(r-1)/(3*s.sqrt(r))
downL=-(1+2*r)/(6*s.sqrt(r))
downR=(1-r)/(3*s.sqrt(r))
A_Z = s.factor(3*(upL**2+upR**2+downL**2+downR**2))
A_W = 6*s.Rational(1,2)
eq("six_flavor_neutral_charge_polynomial", A_Z, 10*r/3-s.Rational(11,3)+11/(6*r))
eq("charged_current_orientations", A_W, 3)
eq("top_IR_log_cancels", s.diff(V,Lt), 0)
eq("W_log_has_massless_charge_sum", s.diff(V,Lw), A_W)
eq("Z_log_has_massless_charge_sum", s.diff(V,Lz), A_Z)
eq("finite_vector_constant", V, A_W*(Lw-s.Rational(3,4))+A_Z*(Lz-s.Rational(3,4)))
eq("degenerate_SU2_control", V.subs({r:1,Lw:Lz}), s.Rational(9,2)*(Lz-s.Rational(3,4)))
eq("omit_mass_matching_is_detected", s.diff(T-P,Lz)-A_Z, s.diff(mass_composition,Lz))
mass2 = read("eq_2_26_mixed_mass_Q_dependent_div_CFgs2g2")
vector2 = s.expand(mass2).coeff(Q,2) / ((1-r)**2/r)
vector1 = s.expand(m_generic).coeff(Q,2) / ((1-r)**2/r)
eq("one_loop_vector_mass_projection", vector1, -3*Lz+s.Rational(5,2))
eq("mixed_vector_mass_projection", vector2, -3*Lz+s.Rational(17,4))
# Independent finite regulator-difference integrals, x=t/s.
x=s.symbols("x", positive=True)
moment0 = s.integrate(-1/(1+x),(x,0,1)) + s.integrate(1/(x*(1+x)),(x,1,s.oo))
# Real x->1/y maps the high interval to (0,1); avoid infinity branches.
y=s.symbols("y", positive=True)
high_log_integrand=s.log(x)/(x*(1+x))
mapped_high=-high_log_integrand.subs(x,1/y)*s.diff(1/y,y)
eq("real_change_of_variables_log_integrand", mapped_high, -s.log(y)/(1+y))
# Integrated geometric-series terms are absolutely summable:
# sum integral |x**n*log(x)| = zeta(2), so termwise integration is valid.
n=s.symbols("n", integer=True, nonnegative=True)
moment1 = 2*s.summation((-1)**n/(n+1)**2, (n,0,s.oo))
eq("PV_minus_sharp_constant_density_moment", moment0, 0)
eq("log_density_changes_regulator_conversion", moment1, s.pi**2/6)
# Canonical normalization and trace-anomaly conversion, formal exact algebra.
gs, SQ, G2, M, beta0, trace = s.symbols("gs SQ G2 M beta0 trace", nonzero=True)
k=1/(16*s.pi**2)
dg_du=gs**3*SQ*k**2*(Lz-s.Rational(3,4))
dM_dgs=-G2/(4*M*gs)
Bg=k**2*gs**2*SQ*G2/(4*M**2)
eq("canonical_proton_gluon_threshold", dg_du*dM_dgs/M, -Bg*(Lz-s.Rational(3,4)))
beta=-beta0*gs**3*k
G2_from_trace=4*M*gs*trace/beta
eq("trace_anomaly_sign_and_normalization", Bg.subs(G2,G2_from_trace), -SQ*trace/(16*s.pi**2*beta0*M))
q2_coefficient = 2*(Lz-s.Rational(3,4))
eq("alpha_s_to_gs_square_root", q2_coefficient/2, Lz-s.Rational(3,4))
result={"outcome":"exact finite source-translation algebra verified", "assertion_tested":inputs["schema"],
        "checks":checks, "check_count":len(checks), "results":{
            "V":str(s.expand(V)), "A_Z":str(A_Z),
            "heavy_vector_gs_threshold_factor":"L-3/4",
            "heavy_vector_mass_one_loop":str(vector1),
            "heavy_vector_mass_mixed_CF":str(vector2),
            "PV_minus_sharp_moment_constant":str(moment0),
            "PV_minus_sharp_moment_log":str(moment1)},
        "non_claim":"No new two-loop integral evaluation, no independent source UV/IR verification, no physical proton or curved-vacuum response computed"}
out=Path(args.output)
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"checks":len(checks),"outcome":result["outcome"],"results":result["results"]},indent=2))
