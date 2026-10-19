"""Source-first independent algebra. No author modules/data are read."""
import hashlib
import json
import pathlib
import sys
import sympy as sp
import mpmath as mp

BASE = pathlib.Path(__file__).resolve().parent
INPUT = BASE / "independent_inputs.json"
data = json.loads(INPUT.read_text())
R = sp.Rational
r, Lt, LW, LZ, L, z, a, d = sp.symbols("r Lt LW LZ L z a d", positive=True)
s = 1-r
TF = R(data["colors"]["T_F"])
CF = R(data["colors"]["C_F"])
checks = []

def exact(name, expression, expected=0):
    residual = sp.factor(expression-expected)
    if residual != 0:
        raise AssertionError((name, str(residual)))
    checks.append({"name": name, "status": "pass", "residual": "0"})

# Independently transcribed from PDF (2.16), after the documented Yukawa limit.
full = -R(8,9)*s*Lt + 3*LW + (R(25,18)/r-R(13,9)+R(14,9)*r)*LZ
full += -R(49,27)-r/R(18)-R(163,216)/r
# Section III vartheta converted to the theta convention using alpha=e^2/(4pi).
top = -s*TF*R(2,3)**2*(4*Lt+R(13,3))
# PDF (2.20), evaluated for the external up-type top in the small-Yukawa limit.
mtop = (6+3/r)/16+s*(4*r-1)/(9*r)*(3*LZ-R(5,2))
subtracted = sp.expand(full-top-R(4,3)*mtop)
target = 3*LW+(R(11,6)/r-R(11,3)+R(10,3)*r)*LZ
target += R(1,2)-R(5,2)*r-R(11,8)/r
exact("sequential_decoupling_all_terms", subtracted, target)
exact("infrared_top_log_cancels", sp.diff(subtracted,Lt))
exact("one_loop_mass_composition_factor", sp.diff(R(2,3)*sp.log(z*(1+a*d)**2),a).subs(a,0),R(4,3)*d)
exact("omitting_top_mass_subtraction_has_nonzero_specific_defect", full-top-target,R(4,3)*mtop)
if sp.factor(mtop)==0:
    raise AssertionError("The omission control must be a nonzero polynomial")

# Direct group trace rather than a polynomial borrowed from the target expression.
six = [R(q) for q in data["six_quark_charges"]]
isos = [R(1,2),R(-1,2)]*3
neutral_sum = sum(TF*((iso-q*s)**2+(q*s)**2)/r for q,iso in zip(six,isos))
charged_sum = 3*2*TF*R(1,2)
factorized = charged_sum*(2*LW-R(3,2))+neutral_sum*(2*LZ-R(3,2))
exact("charged_neutral_factorization_finite_and_logs", subtracted,factorized)
exact("neutral_group_trace",neutral_sum,R(11,12)/r-R(11,6)+R(5,3)*r)
exact("six_charge_trace",sum(q*q for q in six),R(5,3))
exact("five_charge_trace",sum(R(q)**2 for q in data["five_quark_charges"]),R(11,9))
exact("canonical_vector_color_trace_has_no_Nc_factor",2*TF,1)
exact("alpha_s_to_g_s_factor_two",sp.diff(sp.sqrt(1+a*d),a).subs(a,0),d/2)

# Inspect up, down and lepton structures independently, including the axial terms.
for f in data["fermions"]:
    q, iso = R(f["charge"]), R(f["isospin"])
    lr = -s/r*q*(iso-q*s)
    delta_sq = iso**2/r
    mass1_from_source = (9+3*s/r)/16+s/r*q*(iso-q*s)*(3*LZ-R(5,2))
    mass1_charged = R(3,8)
    mass1_projected = -lr*(3*LZ-R(5,2))+R(3,4)*delta_sq
    exact(f["name"]+"_one_loop_neutral_projection",mass1_from_source-mass1_charged,mass1_projected)
    mixed_from_source = 3*s/r*q*(iso-q*s)*(LZ-R(17,12))+R(9,4)*LW+R(9,8)/r*LZ-R(15,32)*(3+s/r)
    mixed_charged = R(9,4)*LW-R(15,16)
    mixed_projected = -3*lr*(LZ-R(17,12))+delta_sq*(R(9,2)*LZ-R(15,8))
    exact(f["name"]+"_mixed_neutral_projection",mixed_from_source-mixed_charged,mixed_projected)

mass1_vector = -(3*L-R(5,2))
mixed_vector = -3*(L-R(17,12))
exact("vector_mass_finite_and_log",mixed_vector,-3*L+R(17,4))
# Sign of the log follows beta_low-beta_high at fixed MSbar matching parameters.
strong_vector = sum(q*q for q in six)*(2*L-R(3,2))
exact("strong_log_beta_difference",-2*sp.diff(strong_vector,L),-R(data["beta_cross_alpha_s_coefficient"])*sum(q*q for q in six))

# A regulator-transfer diagnostic. y=log(k^2/lambda^2) avoids branch choices.
# Smooth fraction is sigmoid(y), sharp fraction is theta(y). Their difference is odd.
mp.mp.dps = data["quadrature_decimal_digits"]
tol = mp.mpf(data["quadrature_tolerance"])
w = lambda y: 1/(4*mp.cosh(y/2)**2)
moment0 = 2*mp.quad(w,[0,1,4,mp.inf])
moment1 = mp.mpf(0)  # exactly odd, integrated over symmetric domain
moment2 = 2*mp.quad(lambda y:y*y*w(y),[0,1,4,mp.inf])
stepdiff0 = mp.mpf(0)  # exactly odd
stepdiff1 = -2*mp.quad(lambda y:y/(1+mp.exp(y)),[0,1,4,mp.inf])
numeric = [
    ("smooth_derivative_zeroth_moment",moment0,mp.mpf(1)),
    ("smooth_derivative_first_moment",moment1,mp.mpf(0)),
    ("smooth_derivative_second_moment",moment2,mp.pi**2/3),
    ("smooth_minus_sharp_zeroth_moment",stepdiff0,mp.mpf(0)),
    ("smooth_minus_sharp_log_moment",stepdiff1,-mp.pi**2/6)
]
for name, observed, expected in numeric:
    residual = abs(observed-expected)
    if residual > tol:
        raise AssertionError((name,str(residual)))
    checks.append({"name":name,"status":"pass","observed":mp.nstr(observed,55),"absolute_residual":mp.nstr(residual,8),"tolerance":str(tol)})

out = pathlib.Path(sys.argv[1])
result = {
    "assertion_tested": "Exact source-composition/group/projection algebra and five mathematical filter moments; no author code imported",
    "input_sha256":hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    "source_pdf_sha256":data["source"]["pdf_sha256"],
    "checks":checks,
    "check_count":len(checks),
    "strong_vector_six_flavor":str(sp.expand(strong_vector)),
    "mass1_vector_per_e2Q2":str(mass1_vector),
    "mixed_mass_vector_per_CFgs2e2Q2":str(mixed_vector),
    "uniform_scope": "Rational identities hold for every r != 0; physical extraction assumes 0<r<1, fixed positive W,Z,h and y_t -> 0 at fixed v. Quadrature is numerical at the recorded tolerance.",
    "non_claims": ["No two-loop integrals recomputed", "No d-dimensional counterterm reconstruction", "No full regulator transfer established", "No complete relative-g_s^2 proton response", "No physical QCD R or alpha"]
}
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"check_count":len(checks),"all_passed":True,"result":str(out)}))
