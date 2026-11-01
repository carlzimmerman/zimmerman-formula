#!/usr/bin/env python3
"""Passive aggregation and plotting of existing DR01 result artifacts.

Does not import or execute the response solver. Run only in a fresh output
directory under the root's bounded runner. INPUTS is the complete set of
project-relative result/manifest reads; the caller also pins this script.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


DIRECTORY = "dynamical_response_2026_11_01"
RUNS = (
    "baseline_basis12_001", "compact_basis24_001", "compact_final_k1536_001",
    "baseline_bare_001", "compact_bare_001",
    "baseline_l1_k512_001", "baseline_l2_k768_001", "baseline_l2_k1152_001",
    "baseline_L64_001", "baseline_spectral_001",
    "compact_l2_k768_001", "compact_basis16_001", "compact_basis20_001",
    "compact_L64_001", "compact_time1536_001", "compact_spectral_001",
    "baseline_long_k1152_001", "baseline_long_k1536_001",
    "compact_long_k1152_001", "compact_long_k1536_001",
    "diffuse_l1_001", "diffuse_l2_001",
)
INPUTS = tuple(f"{DIRECTORY}/{run}/{file}" for run in RUNS
               for file in ("result.json", "manifest.json"))
PRIMARY = {"baseline": "baseline_basis12_001", "compact": "compact_final_k1536_001"}
BARE = {"baseline": "baseline_bare_001", "compact": "compact_bare_001"}
PATTERNS = (0.25, 0.5, 1.0, 2.0, 4.0)
METRICS = ("work_per_amplitude_squared", "torque_integral", "late_to_peak",
           "core_forcing_work_fraction", "source_normalized_ode_residual_max")
COMPARISONS = (
    ("baseline_l1_to_l2", "baseline_l1_k512_001", "baseline_l2_k768_001"),
    ("baseline_basis10_to12", "baseline_l2_k1152_001", "baseline_basis12_001"),
    ("baseline_L40_to64", "baseline_l2_k1152_001", "baseline_L64_001"),
    ("baseline_krylov768_to1152", "baseline_l2_k768_001", "baseline_l2_k1152_001"),
    ("baseline_spectral", "baseline_l2_k1152_001", "baseline_spectral_001"),
    ("compact_basis16_to20_with_spectral_change", "compact_basis16_001", "compact_basis20_001"),
    ("compact_basis20_to24", "compact_basis20_001", "compact_basis24_001"),
    ("compact_final_krylov1152_to1536", "compact_basis24_001", "compact_final_k1536_001"),
    ("compact_L40_to64_with_krylov_change", "compact_l2_k768_001", "compact_L64_001"),
    ("compact_krylov768_to1536", "compact_l2_k768_001", "compact_time1536_001"),
    ("compact_spectral_with_krylov_change", "compact_time1536_001", "compact_spectral_001"),
    ("baseline_long_krylov1152_to1536", "baseline_long_k1152_001", "baseline_long_k1536_001"),
    ("compact_long_krylov1152_to1536", "compact_long_k1152_001", "compact_long_k1536_001"),
    ("diffuse_l1_to_l2", "diffuse_l1_001", "diffuse_l2_001"),
)


def ratio(new, old):
    return new/old if old != 0 else None


def run_metadata(record):
    return {"state": record["state"], "grid": record["grid"],
            "grid_axes": ["L_nodes", "orbital_phase_nodes", "radial_harmonic_limit", "radial_basis"],
            "krylov_count": record["krylov"]["count"],
            "bare": record["bare"], "approximation": record["approximation"],
            "omega_dyn": record["background"]["omega_dyn"],
            "radius": record["background"]["radius"],
            "core_radius": record["background"]["core_radius"],
            "hamiltonian_minimum": record["hamiltonian_minimum"],
            "hamiltonian_maximum": record["hamiltonian_maximum"],
            "high_frequency_sum_rule": record.get("high_frequency_sum_rule"),
            "pulse_duration_times_omega_dyn": [
                case["pulse_duration"]*record["background"]["omega_dyn"] for case in record["cases"]]}


def read_runs(root):
    records, provenance = {}, []
    for run in RUNS:
        result_path = root/DIRECTORY/run/"result.json"
        manifest_path = result_path.with_name("manifest.json")
        record = json.loads(result_path.read_text())
        manifest = json.loads(manifest_path.read_text())
        if tuple(case["pattern_ratio"] for case in record["cases"]) != PATTERNS:
            raise ValueError(f"Unexpected frequency cases in {run}")
        for case in record["cases"]:
            work = case["work_per_amplitude_squared"]
            if not math.isfinite(work) or work <= 0:
                raise ValueError(f"Log plotting requires positive finite work: {run}")
        if manifest["run"]["status"] != "completed":
            raise ValueError(f"Refusing incomplete input record {run}")
        records[run] = record
        provenance.append({"run": run, "run_status": manifest["run"]["status"],
            "result_path": str(result_path.relative_to(root)),
            "manifest_path": str(manifest_path.relative_to(root)),
            "result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
            "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()})
    return records, provenance


def compare(label, old_name, new_name, records):
    old, new = records[old_name], records[new_name]
    rows = []
    for a, b in zip(old["cases"], new["cases"]):
        changes = {key: {"old": a[key], "new": b[key],
                         "absolute_difference": abs(b[key]-a[key]),
                         "relative_difference_to_old": abs(b[key]-a[key])/abs(a[key]) if a[key] != 0 else None}
                   for key in METRICS if key in a and key in b}
        rows.append({"pattern_ratio": a["pattern_ratio"], "metrics": changes})
    om, nm = run_metadata(old), run_metadata(new)
    return {"label": label, "old_run": old_name, "new_run": new_name,
            "old_metadata": om, "new_metadata": nm,
            "changed_grid_axes": [name for name, a, b in zip(om["grid_axes"], old["grid"], new["grid"]) if a != b],
            "krylov_count_changed": om["krylov_count"] != nm["krylov_count"],
            "cases": rows,
            "maximum_relative_work_change_to_old": max(
                row["metrics"]["work_per_amplitude_squared"]["relative_difference_to_old"] for row in rows)}


def duration_comparison(short_name, long_name, records):
    short, long = records[short_name], records[long_name]
    if short["grid"] != long["grid"] or short["state"] != long["state"]:
        raise ValueError("Duration comparison requires identical state and spatial grid")
    rows = []
    for a, b in zip(short["cases"], long["cases"]):
        rows.append({"pattern_ratio": a["pattern_ratio"],
                     "duration_ratio": b["pulse_duration"]/a["pulse_duration"],
                     "work_ratio": b["work_per_amplitude_squared"]/a["work_per_amplitude_squared"],
                     "short_work_per_amplitude_squared": a["work_per_amplitude_squared"],
                     "long_work_per_amplitude_squared": b["work_per_amplitude_squared"]})
    return {"short_run": short_name, "long_run": long_name,
            "short_metadata": run_metadata(short), "long_metadata": run_metadata(long), "cases": rows}


def plot_response(records, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FixedFormatter
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "savefig.dpi": 180, "pdf.fonttype": 42})
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.8), sharey=True)
    for ax, state, title in zip(axes, ("baseline", "compact"), ("Dilute baseline", "Compact baryon endpoint")):
        for run, label, marker, color in ((PRIMARY[state], "Full feedback", "o", "#245a81"),
                                           (BARE[state], "Bare orbits", "s", "#b85e30")):
            values = [c["work_per_amplitude_squared"] for c in records[run]["cases"]]
            ax.plot(PATTERNS, values, marker=marker, color=color, linewidth=1.0,
                    markersize=5.5, markeredgecolor="white", markeredgewidth=.7, label=label)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.xaxis.set_major_locator(FixedLocator(PATTERNS))
        ax.xaxis.set_major_formatter(FixedFormatter(["0.25", "0.5", "1", "2", "4"]))
        ax.set_xlim(.22, 4.55)
        ax.set_xlabel(r"Pattern speed $\Omega_p/\omega_{\rm dyn}$")
        ax.set_title(title, fontsize=11, pad=10)
        ax.grid(axis="y", which="major", alpha=.2)
        ax.legend(frameon=False, loc="best", fontsize=9)
    axes[0].set_ylabel(r"Total finite-pulse work $W/A^2$ (dimensionless)")
    fig.suptitle(r"Fast-scalar kinetic response • pulse duration $20/\omega_{\rm dyn}$", fontsize=12, y=.97)
    fig.text(.5, .035, "Five sampled frequencies; connecting lines guide the eye. Frequencies use each state's own dynamical scale.\n"
             "Total work is not a measurement of irreversible heating or core expansion.", ha="center", va="bottom", fontsize=8.5)
    fig.subplots_adjust(left=.10, right=.97, top=.85, bottom=.23, wspace=.16)
    fig.savefig(output/"response.png")
    fig.savefig(output/"response.pdf")
    plt.close(fig)


def plot_duration(comparison, output):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FixedFormatter
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    y = [row["work_ratio"] for row in comparison["cases"]]
    duration_ratio = comparison["cases"][0]["duration_ratio"]
    ax.plot(PATTERNS, y, "o-", color="#245a81", linewidth=1, markersize=6)
    ax.axhline(duration_ratio, linestyle="--", color="#777777", linewidth=1,
               label=rf"Duration ratio $T_{{long}}/T_{{short}}={duration_ratio:g}$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.xaxis.set_major_locator(FixedLocator(PATTERNS))
    ax.xaxis.set_major_formatter(FixedFormatter(["0.25", "0.5", "1", "2", "4"]))
    ax.set_xlabel(r"Pattern speed $\Omega_p/\omega_{\rm dyn}$")
    ax.set_ylabel(r"Finite-pulse work ratio $W_{long}/W_{short}$")
    ax.set_title("Baseline pulse-duration comparison • fast-scalar limit", fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", alpha=.2)
    fig.text(.5, .025, "Five isolated frequency samples; lines are guides, not a duration-scaling fit.\n"
             "Compact-state duration comparison omitted because its Krylov sensitivity remains unresolved.",
             ha="center", va="bottom", fontsize=8)
    fig.subplots_adjust(left=.13, right=.97, top=.88, bottom=.25)
    fig.savefig(output/"duration.png")
    fig.savefig(output/"duration.pdf")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    output = args.output_directory.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name in ("summary.json", "response.png", "response.pdf", "duration.png", "duration.pdf"):
        if (output/name).exists():
            raise FileExistsError(f"Refusing to overwrite {output/name}")
    records, provenance = read_runs(root)
    primary_rows = []
    for state in ("baseline", "compact"):
        full, bare = records[PRIMARY[state]], records[BARE[state]]
        for key in ("radius", "core_radius", "omega_dyn"):
            if abs(full["background"][key]/bare["background"][key]-1) > 1e-10:
                raise ValueError(f"Full/bare background mismatch: {state}, {key}")
        for f, b in zip(full["cases"], bare["cases"]):
            if abs(f["pulse_duration"]/b["pulse_duration"]-1) > 1e-10:
                raise ValueError("Full/bare pulse duration mismatch")
            primary_rows.append({"state": state, "pattern_ratio": f["pattern_ratio"],
                "full_run": PRIMARY[state], "bare_run": BARE[state],
                "full": f, "bare": b,
                "full_to_bare_work_ratio": ratio(f["work_per_amplitude_squared"], b["work_per_amplitude_squared"])})
    baseline_duration = duration_comparison("baseline_basis12_001", "baseline_long_k1536_001", records)
    compact_duration = duration_comparison("compact_basis20_001", "compact_long_k1536_001", records)
    summary = {"claim_id": "DR01_PASSIVE_SUMMARY", "scope": "Arithmetic aggregation and figures from existing inputs; no response solver executed.",
        "primary_runs": PRIMARY, "bare_runs": BARE, "primary_cases": primary_rows,
        "run_metadata": {name: run_metadata(record) for name, record in records.items()},
        "comparisons": [compare(*item, records) for item in COMPARISONS],
        "duration_comparisons": {"baseline": baseline_duration, "compact": compact_duration},
        "compact_duration_plot_included": False,
        "compact_duration_plot_exclusion": "Coordinator decision: unresolved long-pulse Krylov sensitivity; values retained in JSON.",
        "display_notes": ["Five isolated frequencies; lines are visual guides.",
            "Pattern frequencies and pulse durations are normalized separately for each background.",
            "Work is total supplied energy, not irreversible heating or inferred core expansion.",
            "Core-restricted source work is not retained core energy.",
            "Mixed refinement comparisons retain all changed grid/Krylov metadata."],
        "inputs": provenance}
    (output/"summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False)+"\n")
    plot_response(records, output)
    plot_duration(baseline_duration, output)
    print(json.dumps({"primary_runs": PRIMARY, "input_runs": len(records), "comparisons": len(COMPARISONS),
                      "outputs": ["summary.json", "response.png", "response.pdf", "duration.png", "duration.pdf"]}))


if __name__ == "__main__":
    main()
