#!/usr/bin/env python3
"""Bounded exact OPE algebra; no electromagnetic alpha or phenomenological data."""
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path


def matrix(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def traceless_basis(d):
    # Contravariant symmetric tensors; metric (+,-,...,-).
    for i in range(1, d):
        o = matrix(d)
        o[0][0] = o[i][i] = F(1)
        yield o
    for i in range(d):
        for j in range(i+1, d):
            o = matrix(d)
            o[i][j] = o[j][i] = F(1)
            yield o


def angular_trace_checks(d):
    metric = [F(1)] + [F(-1)]*(d-1)
    visited = 0
    for o in traceless_basis(d):
        assert sum(metric[i]*o[i][i] for i in range(d)) == 0
        for c2, c3 in [(F(1), F(0)), (F(0), F(1))]:
            total = F(0)
            for axis in range(d):
                # Wick-rotated unit axis: q^2=-1, (q^0)^2=-1,
                # spatial (q^i)^2=+1. Needed products remain rational.
                qup_outer = matrix(d)
                qup_outer[axis][axis] = -metric[axis]
                p = matrix(d)
                for i in range(d):
                    for j in range(d):
                        p[i][j] = (-metric[i] if i == j else F(0))-qup_outer[i][j]
                qoq_over_q2 = metric[axis]*o[axis][axis]
                trace_direct = F(0)
                for i in range(d):
                    tii = p[i][i]*c2*qoq_over_q2
                    tii += c3*sum(p[i][j]*metric[j]*p[i][k]*metric[k]*o[j][k]
                                  for j in range(d) for k in range(d))
                    trace_direct += metric[i]*tii
                assert trace_direct == -((d-1)*c2+c3)*qoq_over_q2
                total += trace_direct
                assert all(p[axis][j] == 0 for j in range(d))
                visited += 1
            # +/- axes reproduce the O(d) second moment exactly.
            assert total/d == 0
    return {"dimension":d, "basis_dimension":d*(d+1)//2-1,
            "coefficient_basis_pairs":2, "axis_tensor_checks":visited,
            "all_angular_traces_zero":True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    inp = json.loads(Path(args.inputs).read_text())
    charges = list(map(F,inp["charges"]))
    sq = sum(q*q for q in charges)
    assert sum(charges) == 0 and sq == F(2,3)
    qc = {k:F(v) for k,v in inp["quark_coefficients_over_Qf_squared"].items()}
    gc = {k:F(v) for k,v in inp["gluon_coefficients_over_a_SQ"].items()}
    z = F(inp["spin2_Zqg_pole_over_a"])
    poles = inp["bare_gluon_poles_over_a_SQ"]
    pole_residuals = {k:str(F(poles[k])+qc[k]*z) for k in ("c2","c3")}
    assert set(pole_residuals.values()) == {"0"}
    sub_constant = (gc["c2_constant"]-gc["c3_constant"])/4
    sub_log = (gc["c2_log"]-gc["c3_log"])/4
    assert sub_constant == F(-5,3) and sub_log == F(4,3)
    scale_residual = -2*sub_log+2*F(4,3)
    assert scale_residual == 0
    bounds = inp["finite_checks"]
    angular = [angular_trace_checks(d) for d in range(bounds["dimension_min"],bounds["dimension_max"]+1)]
    fixed_points = []
    for nf in range(bounds["nf_min"],bounds["nf_max"]+1):
        sigma, gluon = F(3*nf,16+3*nf), F(16,16+3*nf)
        mix = [[F(-64,9),F(4*nf,3)],[F(64,9),F(-4*nf,3)]]
        assert sigma+gluon == 1
        assert all(sum(mix[i][j]*[sigma,gluon][j] for j in range(2)) == 0 for i in range(2))
        assert all(sum(mix[i][j] for i in range(2)) == 0 for j in range(2))
        assert sum(mix[i][i] for i in range(2)) == -F(64+12*nf,9)
        fixed_points.append({"nf":nf,"singlet":str(sigma),"gluon":str(gluon)})
    # g_s^2 SQ <G^2>/(pi^4 m^2) has been factored out.
    g_shell = F(3,64)*F(1,16)*gc["c1"]
    g_ct = -F(1,256)*F(1,4)
    assert g_shell == F(1,1024) and g_shell+g_ct == 0
    # Q_f^2 f_f^(0)/pi^2 has been factored out.
    q_shell = F(3,64)*qc["c1"]*2
    q_ct = -F(3,16)
    assert q_shell == F(3,16) and q_shell+q_ct == 0
    beta0 = F(9)
    scalar_c = 2*sq/(3*beta0)
    spin2_c = 2*sq*F(3,25)
    full_sub_c = scalar_c+spin2_c
    slope_pi2 = -sq/(16*beta0)
    assert scalar_c == F(4,81) and spin2_c == F(4,25)
    assert full_sub_c == F(424,2025) and slope_pi2 == F(-1,216)
    band_ratio = F(inp["photon_band_Q1_over_Q0"])
    band_log = 2*math.log(float(band_ratio))
    uv = {"SQ":str(sq),"beta0":str(beta0),"W1_scalar_limit":str(scalar_c),
          "W1_spin2_limit":str(spin2_c),"W1_total_limit":str(full_sub_c),
          "band_slope_times_pi_squared":str(slope_pi2),
          "band_slope_float":float(slope_pi2)/math.pi**2,
          "Q1_over_Q0":str(band_ratio),
          "D_band_over_m_per_e_squared":float(slope_pi2)*band_log/math.pi**2,
          "mass_band_per_alpha":4*math.pi*float(slope_pi2)*band_log/math.pi**2}
    result = {"assertion_tested":"Exact bounded charge/tensor/pole/mixing/counterterm algebra; double-precision rendering of exact UV formula",
              "charge_trace":str(sum(charges)),"charge_square_trace":str(sq),
              "spin2_pole_residuals":pole_residuals,
              "subtraction_gluon_spin2":{"constant":str(sub_constant),"log":str(sub_log),"mixed_log_scale_residual":str(scale_residual)},
              "angular_checks":angular,"singlet_fixed_points":fixed_points,
              "canonical_scalar_counterterm_check":{"gluon_shell_factor":str(g_shell),"gluon_counterterm_factor":str(g_ct),"gluon_residual":str(g_shell+g_ct),"quark_residual":str(q_shell+q_ct)},
              "massless_nf3_uv":uv,"all_assertions_passed":True,
              "non_claims":["IR sea matrix element","Complete proton mass","Physical finite-mass calibration","Curved response or R(alpha)"]}
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"all_assertions_passed":True,"massless_nf3_uv":uv},indent=2))


if __name__ == "__main__":
    main()
