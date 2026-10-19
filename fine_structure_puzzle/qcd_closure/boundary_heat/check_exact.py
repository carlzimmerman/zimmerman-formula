"""Finite exact arithmetic audit; no root fitting or unbounded computation."""
import json
from fractions import Fraction as F
from pathlib import Path


def zero():
    return [[F(0) for _ in range(4)] for _ in range(4)]


def diag(ds):
    a = zero()
    for i, d in enumerate(ds):
        a[i][i] = F(d)
    return a


def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(4))
             for j in range(4)] for i in range(4)]


def add(a, b):
    return [[a[i][j]+b[i][j] for j in range(4)] for i in range(4)]


def tr(a):
    return sum(a[i][i] for i in range(4))


def scalar_a4_polynomial(robin_s=None):
    # Independent scalar specialization of the theorem, K=2, |L|^2=2.
    if robin_s is None:
        return F(40*8-264*4+320*2, 21)
    s = F(robin_s)
    return F(280*8+168*4+224*2, 21) + 144*s*4 + 48*s*2 + 480*s*s*2 + 480*s**3


def main():
    pplus = diag([0, 0, 1, 0])
    pminus = diag([1, 1, 0, 1])
    chi = diag([-1, -1, 1, -1])
    s = diag([0, 0, -2, 0])
    derivatives = []
    for a in (0, 1):
        d = zero()
        d[a][2] = d[2][a] = F(2)
        derivatives.append(d)
    d2 = add(*(mul(d, d) for d in derivatives))
    projector_terms = [-12*tr(d2)*2, -24*tr(d2), -120*tr(mul(d2, s))]
    rplus, rminus = tr(pplus), tr(pminus)
    cubic = ((280*rplus+40*rminus)*8
             +(168*rplus-264*rminus)*4
             +(224*rplus+320*rminus)*2)/21
    robin = 144*tr(s)*4+48*tr(s)*2+480*tr(mul(s,s))*2+480*tr(mul(mul(s,s),s))
    vector_poly = cubic+robin+sum(projector_terms)
    ghost_poly = scalar_a4_polynomial()
    combo_poly = vector_poly-2*ghost_poly
    # A4 = pi/R times this rational number.
    vector_A4 = F(4,360)*vector_poly
    ghost_A4 = F(4,360)*ghost_poly
    combo_A4 = vector_A4-2*ghost_A4
    te_tm_A4 = F(4,360)*(scalar_a4_polynomial()+scalar_a4_polynomial(-1))
    gamma_inverse = -combo_A4/8
    # Lower coefficients and smearing-jet tests; powers of pi shown in output.
    vector_a3_poly = (13*rplus-7*rminus)*4+(2*rplus+10*rminus)*2+96*tr(s)*2+192*tr(mul(s,s))-12*tr(d2)
    dirichlet_a3_poly = -7*4+10*2
    combo_a3_poly = vector_a3_poly-2*dirichlet_a3_poly
    heat_constant = combo_a3_poly/384
    vector_fn = (6*rplus+30*rminus)*2+96*tr(s)
    combo_fn_per_K = (vector_fn-2*30*2)/2
    combo_fnn = 24*(tr(chi)-2*(-1))
    results = {
        "status": "finite exact arithmetic verified",
        "R": 1,
        "projector_derivative_trace": str(tr(d2)),
        "projector_derivative_S_trace": str(tr(mul(d2,s))),
        "projector_polynomial_terms": list(map(str,projector_terms)),
        "vector_cubic_polynomial": str(cubic),
        "vector_robin_polynomial": str(robin),
        "vector_a4_polynomial": str(vector_poly),
        "scalar_dirichlet_a4_polynomial": str(ghost_poly),
        "combo_a4_polynomial": str(combo_poly),
        "A4_vector_units_pi_over_R": str(vector_A4),
        "A4_D_units_pi_over_R": str(ghost_A4),
        "A4_combo_units_pi_over_R": str(combo_A4),
        "A4_TE_TM_units_pi_over_R": str(te_tm_A4),
        "Gamma_inverse_units_1_over_mR": str(gamma_inverse),
        "heat_trace_constant": str(heat_constant),
        "a3_smearing_f_n_polynomial_per_K": str(combo_fn_per_K),
        "a3_smearing_f_nn_polynomial": str(combo_fnn),
        "scalar_mass_profile_candidate_s_plus": str(gamma_inverse-F(5,8)),
        "scalar_mass_profile_candidate_s_minus": str(gamma_inverse+F(5,8)),
        "non_claims": ["Does not prove the external heat theorem", "Does not bound a spectral remainder", "Does not sum frequencies", "Does not calculate the monopole determinant or physical stress"]
    }
    assert tr(d2) == 16 and tr(mul(d2,s)) == -16
    assert vector_A4 == -F(32,63)
    assert ghost_A4 == -F(16,315)
    assert combo_A4 == te_tm_A4 == -F(128,315)
    assert gamma_inverse == F(16,315)
    assert heat_constant == F(5,8)
    assert combo_fn_per_K == -60 and combo_fnn == 0
    out = Path("fine_structure_puzzle/qcd_closure/boundary_heat/runs/exact-001/result.json")
    out.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
