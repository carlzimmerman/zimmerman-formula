"""Reconstruct a passing dilute state for an independently contracted screen.

Importing this module performs no scientific calculation. Calling
reconstruct_endpoint follows the frozen .025 path and must be run under the
caller's bounded contract. It returns the actual SciPy BVP object, not a
spline interpolated from the 400-point presentation profile.

Dependencies to pin: this file, static_dilute.py, static_response.py,
inputs/check_gradient.py, and static_dilute_run_001/result.json, with their
declared mathematical contracts/conventions as applicable.
"""
import json
import static_dilute as dilute


def reconstruct_endpoint(pc, family, fraction=1.0):
    """Return baseline/forced full BVPs and agreement with the saved state.

The supported grid is pc in (.2,.4,.6), epsilon=.01, named frozen family,
and fraction=j/40. The requested state must have passed the saved run.
No alternative guesses, failed-step retries or eigenvalue calculations occur.

Return keys: baseline_record, baseline_solution, record, solution,
reference_record, reconstruction_relative_differences, auxiliary_record.
"""
    original = dilute.original
    if pc not in (0.2, 0.4, 0.6) or family not in original.FAMILIES:
        raise ValueError("Requested state is outside the frozen dilute controls")
    last_index = round(40*fraction)
    if not 0 <= last_index <= 40 or abs(last_index/40 - fraction) > 1e-12:
        raise ValueError("Requested fraction is not on the frozen .025 grid")
    reference = json.loads((original.ROOT / "static_dilute_run_001/result.json").read_text())
    saved = next((r for r in reference["cases"] if
                  (r["baseline_psi_c"], r["epsilon"], r["family"], r["fraction"]) ==
                  (pc, 0.01, family, fraction)), None)
    if saved is None or not saved.get("passed", False):
        raise ValueError("Requested state did not pass the saved dilute run")
    frozen = original.load_baseline()
    auxiliary, guess = frozen.local_solution(pc)
    baseline, previous = frozen.solve_case(pc, 0.01, auxiliary, guess)
    if not baseline.get("passed", False):
        raise RuntimeError("Baseline reconstruction did not pass")
    baseline_solution = previous
    core_mass = dilute.enclosed_mass(previous, baseline["quarter_radius"], baseline["radius"])
    baseline["original_core_dark_mass"] = core_mass
    mass_ratio, scale_ratio = original.FAMILIES[family]
    final_mb = mass_ratio*baseline["mass_dimensionless"]
    a = scale_ratio*baseline["radius"]
    for index in range(last_index + 1):
        current_fraction = index/40
        row, sol = original.solve_response(baseline, 0.01, current_fraction*final_mb, a, previous.sol)
        if not row.get("passed", False):
            raise RuntimeError(f"Reconstruction failed at frozen fraction {current_fraction}: {row}")
        core = dilute.core_diagnostics(baseline, core_mass, row, sol, current_fraction*final_mb, a)
        if not core["passed"]:
            raise RuntimeError(f"Material-core reconstruction failed at fraction {current_fraction}")
        row.update({"baseline_psi_c": pc, "epsilon": 0.01, "family": family,
                    "fraction": current_fraction, "continuation_index": index,
                    "material_core": core})
        row["checks"]["material_core_checks"] = True
        previous = sol
    differences = {key: abs(row[key]/saved[key] - 1) for key in
                   ("density_c", "radius", "quarter_radius", "core_column_coefficient")}
    differences.update({key: abs(row["material_core"][key]/saved["material_core"][key] - 1) for key in
                        ("enclosed_core_mass_ratio", "material_core_radius_ratio")})
    if max(differences.values()) >= 5e-5:
        raise RuntimeError(f"Reconstructed state differs from the saved state: {differences}")
    return {"baseline_record": baseline, "baseline_solution": baseline_solution,
            "record": row, "solution": sol, "reference_record": saved,
            "reconstruction_relative_differences": differences,
            "auxiliary_record": auxiliary}
