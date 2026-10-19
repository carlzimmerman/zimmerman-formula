"""Exact finite algebra checks for the declared local common-PV match."""
import json
from fractions import Fraction as Q
from pathlib import Path


def plus(a, b):
    c = dict(a)
    for key, value in b.items():
        c[key] = c.get(key, Q(0))+value
    return {key: value for key, value in c.items() if value}


def times(a, b):
    c = {}
    for (aq, am), av in a.items():
        for (bq, bm), bv in b.items():
            key = (aq+bq, am+bm)
            c[key] = c.get(key, Q(0))+av*bv
    return {key: value for key, value in c.items() if value}


def scale(a, s):
    return {key: value*s for key, value in a.items() if value*s}


def derivative_q(a):
    return {(q-1,m): value*q for (q,m),value in a.items() if q}


def derivative_power(r, count):
    # d/dq [P*(q^2+M^2)^r] = [P'*(q^2+M^2)+2r*q*P]*(...)^(r-1).
    p = {(0,0): Q(1)}
    base = {(2,0): Q(1), (0,2): Q(1)}
    for _ in range(count):
        p = plus(times(derivative_q(p),base), scale(times({(1,0):Q(1)},p),2*r))
        r -= 1
    return p,r


def coefficients(bulk_a2, collar_a2):
    return {"a_squared": bulk_a2+collar_a2, "a_fourth": -Q(1,3),
            "log2_times_a_squared": Q(11,3), "log2_times_n_squared": Q(11,3)}


def main():
    # Actual finite PV example: M_j^2/M^2 = 0,1,2,3, common fixed ratios.
    pv_c = [Q(1),Q(-3),Q(3),Q(-1)]
    pv_m2 = [Q(0),Q(1),Q(2),Q(3)]
    moments = [sum(c*m**k for c,m in zip(pv_c,pv_m2)) for k in range(3)]
    heavy_sum = sum(pv_c[1:])
    d2, d2exp = derivative_power(Q(1,2),2)
    d4, d4exp = derivative_power(Q(3,2),4)
    assert moments == [0,0,0] and heavy_sum == -1
    assert d2 == {(0,2):Q(1)} and d2exp == -Q(3,2)
    assert d4 == {(0,4):Q(9)} and d4exp == -Q(5,2)
    # Independent canonical heat check, coefficient of partial_in U.
    vector_unormal = -(240-3*120)
    ghosts_unormal = -2*(-(-120))
    boundary_heat_unormal = Q(vector_unormal+ghosts_unormal,360)
    bulk_heat_laplacian = Q(-60*(4-2),360)
    assert boundary_heat_unormal == bulk_heat_laplacian == -Q(1,3)
    # Exact bridge covariance integrals with t=1; formal scaling restores t.
    bridge_quadratic = Q(1,2)-Q(1,3)
    bridge_linear_squared = Q(1,3)-Q(1,4)
    assert bridge_quadratic == Q(1,6) and bridge_linear_squared == Q(1,12)
    # Symbolic coefficient addition in units L/pi; log(2) treated formally.
    ibp = coefficients(-Q(1,6),Q(4,3))
    diagonal = coefficients(Q(1,6),Q(1))
    mismatched = coefficients(Q(1,6),Q(4,3))
    assert ibp == diagonal
    assert ibp["a_squared"] == Q(7,6)
    assert mismatched["a_squared"]-ibp["a_squared"] == Q(1,3)
    # PV Riemann limits are analytic inputs, not numerically sampled here.
    f0_second = heavy_sum
    potential_fourth = -3*heavy_sum*Q(2,3)
    assert f0_second == -1 and potential_fourth == 2
    assert Q(1,3)-2+6-1 == Q(10,3)
    result = {
        "status": "finite exact algebra verified",
        "PV_example_coefficients": list(map(str,pv_c)),
        "PV_example_squared_mass_ratios": list(map(str,pv_m2)),
        "PV_moments_k_0_1_2": list(map(str,moments)),
        "d2_mu": {"numerator": "M^2", "denominator_power_q2_plus_M2": str(-d2exp)},
        "d4_mu_cubed": {"numerator": "9 M^4", "denominator_power_q2_plus_M2": str(-d4exp)},
        "canonical_boundary_heat_normal_U_coefficient": str(boundary_heat_unormal),
        "canonical_bulk_heat_laplacian_U_coefficient": str(bulk_heat_laplacian),
        "bridge_coefficients": {"minus_t2_laplacian_U": str(bridge_quadratic), "plus_t3_gradient_U_squared": str(bridge_linear_squared)},
        "F0_second_units_L_over_pi": str(f0_second),
        "potential_fourth_derivative_units_L_over_pi_squared": str(potential_fourth),
        "matched_Gamma_coefficients_units_L_over_pi": {k:str(v) for k,v in ibp.items()},
        "matched_logweight_coefficients_units_L_over_pi": {k:str(-v) for k,v in ibp.items()},
        "IBP_collar_a2_units_L_over_pi": "4/3",
        "diagonal_collar_a2_units_L_over_pi": "1",
        "diagonal_collar_compensator_a2_units_L_over_pi": "-1/3",
        "mismatched_result_excess_a2_units_L_over_pi": "1/3",
        "Gamma_at_a_n_equal_one": "(L/pi)*(22*log(2)/3+5/6)",
        "non_claims": ["No numerical frequency sum or Riemann-limit fit", "No proof of derivative-expansion completeness", "No global/core/neutral determinant", "Finite wall matching functions fixed to zero only for this benchmark", "No physical alpha"]
    }
    path = Path("fine_structure_puzzle/qcd_closure/common_regulator_match/runs/match-001/result.json")
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
