"""Conditional full-ADM degree-of-freedom count for the relay branch.

The scalar second-class rank is imported from the actual Poisson matrix.  The
six spatial constraints are represented by their first-class algebraic block;
the missing nonlinear hypersurface-deformation calculation remains explicit.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from auxiliary_relay_dirac import relay_dirac


def count_for_mode(k_value: float):
    scalar = relay_dirac(k_value, 2.0, 1.0)
    spatial_bracket = sp.zeros(6)  # six constraints; spatial algebra vanishes on shell
    spatial_rank = int(spatial_bracket.rank())
    first_class = spatial_bracket.rows - spatial_rank
    second_class = scalar["dirac_rank"]
    phase_dimension = 20  # (gamma_ij,pi^ij),(N,pi_N),(N^i,pi_i)
    dof = (phase_dimension - 2 * first_class - second_class) / 2
    return {
        "k": k_value,
        "phase_dimension": phase_dimension,
        "spatial_constraint_matrix_rank": spatial_rank,
        "first_class_spatial_constraints": first_class,
        "second_class_scalar_constraints": second_class,
        "gravitational_dof_count": dof,
        "scalar_matrix_rank": scalar["dirac_rank"],
    }


def run():
    local = count_for_mode(1.0)
    homogeneous = count_for_mode(0.0)
    result = {
        "candidate": "rotated_mmg_auxiliary_relay_2026",
        "local": local,
        "homogeneous": homogeneous,
        "gates": {
            "local_count_is_two": local["gravitational_dof_count"] == 2.0,
            "homogeneous_rank_jump_exposed": homogeneous["gravitational_dof_count"] > local["gravitational_dof_count"],
            "scalar_rank_is_computed": local["second_class_scalar_constraints"] == local["scalar_matrix_rank"],
        },
        "conditional_scope": (
            "The count is valid if the six spatial constraints remain first class "
            "in the full nonlinear metric algebra; that bracket has not yet been derived."
        ),
    }
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "full_adm_dof_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("FULL_ADM_DOF_COUNT_GATE")
    print(f"local_gravitational_dof: {local['gravitational_dof_count']}")
    print(f"homogeneous_gravitational_dof: {homogeneous['gravitational_dof_count']}")
    for name, passed in result["gates"].items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")
    print("STATUS: CONDITIONAL (requires nonlinear spatial-algebra verification)")


if __name__ == "__main__":
    run()
