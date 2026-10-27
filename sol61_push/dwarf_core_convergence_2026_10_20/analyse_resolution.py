"""Standalone, read-only analysis of completed full-3D resolution records.

Outputs are created only in a fresh directory. Pilot/short validation runs are
excluded unless explicitly requested. Snapshot conditional count intervals are
never pooled across correlated times. Numerical convergence remains pending
independent matched controls, initial scrambles, centring and 3D shape checks.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sys

import numpy as np
from scipy.signal import find_peaks, savgol_filter
from scipy.stats import t as student_t

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from profile_diagnostics import classify_flatness, compare_profiles


def _series(times, values):
    times, values = np.asarray(times, float), np.asarray(values, float)
    if (times.ndim != 1 or values.shape[0] != len(times) or np.any(np.diff(times) <= 0.)
            or not np.all(np.isfinite(times))):
        raise ValueError("strictly increasing finite times and matching observations required")
    return times, values


def window_statistics(times, values, start, end, max_gap_Myr=None):
    """Integrate piecewise-linear observations over a fully covered window.

    Temporal standard deviation describes variation, never a standard error.
    No incomplete interval is silently shortened. Optional gap limits reject
    interpolation across missing records even when both endpoints are present.
    """
    times, values = _series(times, values)
    if end <= start:
        raise ValueError("window end must follow start")
    base = dict(interval_Myr=[float(start), float(end)], complete=False, mean=None,
                temporal_std=None, temporal_scatter_is_confidence_interval=False,
                confidence_interval=None, confidence_scope="no temporal/realization confidence interval inferred")
    if len(times) == 0:
        return dict(base, coverage_fraction=0., reason="no_records", sample_count=0, max_gap_Myr=None)
    overlap = max(0., min(end, times[-1]) - max(start, times[0]))
    coverage = min(1., overlap / (end - start))
    base.update(coverage_fraction=float(coverage), sample_count=int(np.sum((times >= start) & (times <= end))))
    if start < times[0] - 1.e-8 or end > times[-1] + 1.e-8 or len(times) < 2:
        return dict(base, reason="incomplete_time_coverage", max_gap_Myr=None)
    segments = (times[:-1] < end) & (times[1:] > start)
    maximum_gap = float(np.max(np.diff(times)[segments])) if np.any(segments) else 0.
    base["max_gap_Myr"] = maximum_gap
    if max_gap_Myr is not None and maximum_gap > max_gap_Myr + 1.e-8:
        return dict(base, reason="recording_gap")
    if not np.all(np.isfinite(values)):
        return dict(base, reason="nonfinite_observations")
    nodes = np.r_[start, times[(times > start) & (times < end)], end]
    flat = values.reshape(len(times), -1)
    samples = np.column_stack([np.interp(nodes, times, column) for column in flat.T])
    width = np.diff(nodes)[:, None]
    duration = end - start
    mean = np.sum(width * .5 * (samples[:-1] + samples[1:]), axis=0) / duration
    # Exact second moment of the linearly interpolated segments.
    second = np.sum(width * (samples[:-1] ** 2 + samples[:-1] * samples[1:] + samples[1:] ** 2) / 3., axis=0) / duration
    scatter = np.sqrt(np.maximum(second - mean * mean, 0.))

    def unpack(array):
        return float(array[0]) if values.ndim == 1 else array.reshape(values.shape[1:]).tolist()

    return dict(base, complete=True, mean=unpack(mean), temporal_std=unpack(scatter),
                minimum=unpack(samples.min(axis=0)), maximum=unpack(samples.max(axis=0)),
                reason=None, interpolation="piecewise linear; no independent-snapshot assumption")


def find_pericentres(times, radii, min_separation_Myr=300., prominence_pc=1000.):
    """Find observed interior radius minima; endpoints never complete a passage."""
    times, radii = _series(times, radii)
    if radii.ndim != 1 or not np.all(np.isfinite(radii)):
        raise ValueError("finite scalar orbit radii required")
    if len(times) < 3:
        return []
    # Small remnant-centre wiggles must not determine the time of a broad
    # orbital passage. Smooth only regularly sampled radii, explicitly, on a
    # 60-Myr scale much shorter than the approximately 1.4-Gyr orbit. Raw
    # measurements remain in each event record; irregular series stay raw.
    fitted_radii = radii
    smoothing_samples = 1
    cadence = float(np.median(np.diff(times)))
    if len(times) >= 5 and np.allclose(np.diff(times), cadence, rtol=.05, atol=1.e-8):
        smoothing_samples = max(5, int(round(60. / cadence)) | 1)
        smoothing_samples = min(smoothing_samples, len(times) if len(times) % 2 else len(times) - 1)
        fitted_radii = savgol_filter(radii, smoothing_samples, 3)
    indices, info = find_peaks(-fitted_radii, prominence=prominence_pc)
    # Stronger minima take precedence when small wiggles occur close together.
    ranked = sorted(range(len(indices)), key=lambda i: (-info["prominences"][i], times[indices[i]]))
    chosen = []
    for rank in ranked:
        index = int(indices[rank])
        if all(abs(times[index] - times[prior]) >= min_separation_Myr for prior in chosen):
            chosen.append(index)
    result = []
    for number, index in enumerate(sorted(chosen), 1):
        local_t = times[index - 1:index + 2] - times[index]
        a, b, c = np.polyfit(local_t, fitted_radii[index - 1:index + 2], 2)
        offset = -b / (2. * a) if a > 0. else 0.
        refined = a > 0. and local_t[0] <= offset <= local_t[-1]
        when = times[index] + offset if refined else times[index]
        radius = a * offset * offset + b * offset + c if refined else fitted_radii[index]
        result.append(dict(number=number, index=index, time_Myr=float(when),
                           radius_pc=float(radius), sample_time_Myr=float(times[index]),
                           sample_radius_pc=float(radii[index]), quadratic_refined=bool(refined),
                           smoothing_samples=smoothing_samples,
                           smoothing_span_Myr=float((smoothing_samples - 1) * cadence)))
    return result


def orbital_windows(times, radii, mass, post_start=100., post_end=300.,
                    min_separation_Myr=300., prominence_pc=1000., max_gap_Myr=None):
    """Last completed peri-to-peri cycle and equally defined numbered windows."""
    times, mass = _series(times, mass)
    peri = find_pericentres(times, radii, min_separation_Myr, prominence_pc)
    if max_gap_Myr is None and len(times) > 1:
        max_gap_Myr = 1.6 * float(np.median(np.diff(times)))
    if len(peri) >= 2:
        start, end = peri[-2], peri[-1]
        cycle = window_statistics(times, mass, start["time_Myr"], end["time_Myr"], max_gap_Myr)
        cycle["pericentre_numbers"] = [start["number"], end["number"]]
    else:
        cycle = dict(complete=False, mean=None, reason="fewer_than_two_observed_pericentres", pericentre_numbers=[])
    windows = []
    for passage in peri:
        item = window_statistics(times, mass, passage["time_Myr"] + post_start,
                                 passage["time_Myr"] + post_end, max_gap_Myr)
        item.update(pericentre_number=passage["number"], offsets_after_pericentre_Myr=[post_start, post_end])
        windows.append(item)
    return dict(pericentres=peri, last_complete_cycle=cycle, post_pericentre_windows=windows,
                min_separation_Myr=min_separation_Myr, prominence_pc=prominence_pc,
                scope="fixed time/orbital windows; temporal scatter is not an ensemble confidence interval")


CONTROL_KEYS = ("host", "collisionless", "collision_method", "ncold", "eps", "h", "dt", "seed", "collision_seed", "duration", "backend", "threads")
DEFAULTS = dict(host=False, collisionless=False, seed=87319, collision_seed=None,
                duration=10000., backend="cpu", threads=4,
                collision_method="legacy_sequential_bernoulli")


def control_difference(a, b):
    """Identify argument factors; initial paths are provenance, checked separately."""
    changes = [key for key in CONTROL_KEYS if a.get(key, DEFAULTS.get(key)) != b.get(key, DEFAULTS.get(key))]
    if a.get("collisionless", False) or b.get("collisionless", False):
        changes = [key for key in changes if key not in ("collision_seed", "collision_method")]
    if a.get("collisionless", False) and b.get("collisionless", False):
        changes = [key for key in changes if key != "h"]
    return len(changes) == 1, changes[0] if len(changes) == 1 else "mixed_controls" if changes else "replicate", changes


def initial_state_admission(args_a, args_b, initial_a, initial_b):
    """Admit equal-N arrays or a recorded preparation family across N.

    A file path is never a physical control axis. A hash is an identity check
    within N, while different-N arrays necessarily require a metadata-family
    check. The latter checks recorded preparation, not a proof of nested
    physical phase space or of an unchanged continuous distribution.
    """
    common = bool(initial_a.get('common_initial_state') and initial_b.get('common_initial_state'))
    ha, hb = initial_a.get('relative_state_sha256'), initial_b.get('relative_state_sha256')
    identical = bool(ha and hb and ha == hb)
    if args_a['ncold'] == args_b['ncold']:
        failed = []
        if not ha or not hb:failed.append('relative_state_sha256_missing')
        elif not identical:failed.append('relative_state_sha256_mismatch')
        caveat = ('Both controls use identical recorded relative x/v/m arrays; only the declared host orbital translation may differ.'
                  if common and not failed else
                  'Common-state control has missing or different saved physical arrays; equal seeds and file paths cannot establish a matched control.'
                  if common else
                  'Legacy states were prepared separately; exact saved-array identity is required for a pure same-N control. Epsilon/backend preparation could change velocity normalization.')
        return dict(compatible=not failed,mode='same_N_saved_state_identity',failed_checks=failed,
                    both_common_initial=common,exact_phase_space_hash_identical=identical,caveat=caveat)

    fields = ('sampling','cold_phase_seed','stellar_phase_seed','reference_softening_pc',
              'cold_mass','stellar_mass','cold.virial_ratio','cold.ordered_fraction',
              'stars.virial_ratio','stars.ordered_fraction')
    def value(initial, args, field):
        if field == 'reference_softening_pc' and not initial.get('common_initial_state'):
            return initial.get(field,args.get('eps'))
        result=initial
        for part in field.split('.'):
            if not isinstance(result,dict) or part not in result:return None
            result=result[part]
        return result
    failed=[];family_a={};family_b={}
    for field in fields:
        aa,bb=value(initial_a,args_a,field),value(initial_b,args_b,field)
        family_a[field],family_b[field]=aa,bb
        equal=(aa is not None and bb is not None and
               (bool(np.isclose(aa,bb,rtol=1.e-12,atol=0.)) if isinstance(aa,(int,float)) and isinstance(bb,(int,float)) else aa==bb))
        if not equal:failed.append(field)
    for label,args,initial in (('a',args_a,initial_a),('b',args_b,initial_b)):
        if initial.get('cold_phase_seed') != args.get('seed',DEFAULTS['seed']):
            failed.append(label+'.initial_seed_argument_mismatch')
    if not ha or not hb:failed.append('relative_state_sha256_missing')
    return dict(compatible=not failed,mode='same_preparation_family_different_N',
                failed_checks=failed,both_common_initial=common,
                exact_phase_space_hash_identical=identical,family_a=family_a,family_b=family_b,
                caveat='N controls share the recorded preparation law and reference softening only if all family checks pass; each N has separately prepared finite-sample velocities. Different hashes are expected across N; this does not imply identical physical particle arrays.',
                scope='recorded metadata compatibility, not proof of nested phase space or empirical convergence')


def radial_screen(profile, screen, eps, age_Myr=10000.):
    radii = np.asarray(profile["edges"], float)
    count = np.asarray(profile["enclosed_count_at_edges"], float)
    relaxation = np.asarray(screen["edge_t_relax_Myr"], float)
    force = radii >= 2.8 * eps
    enough = count >= 200
    age = np.isfinite(relaxation) & (relaxation >= age_Myr)
    passed = force & enough & age
    persistent = np.array([np.all(passed[i:]) for i in range(len(passed))])
    r_screen = float(radii[np.flatnonzero(persistent)[0]]) if np.any(persistent) else None
    return dict(radius_pc=radii.tolist(), force_pass=force.tolist(), count_pass=enough.tolist(),
                relaxation_pass=age.tolist(), all_pass=passed.tolist(), r_screen_pc=r_screen,
                age_Myr=age_Myr, minimum_enclosed_selected_count=200, minimum_radius_over_eps=2.8,
                interpretation="heuristic numerical screen only; no collision-support, centring, 3D shape or empirical convergence guarantee")


def _fit_records(row, eps):
    result = {}
    for name, fit in row.get("fits", {}).items():
        result[name] = dict(fit=fit, classification=classify_flatness(row["profile"], fit, row["relaxation"], eps))
    return result


def summarize_case(name, data, late=(8000., 10000.), post=(100., 300.), peri_separation=300., peri_prominence=1000.):
    args, rows = data["args"], data["snapshots"]
    times = np.array([row["time_Myr"] for row in rows])
    cadence = float(args.get("record_interval", np.median(np.diff(times)) if len(times) > 1 else 10.))
    gap = 1.6 * cadence
    final = rows[-1]
    eps = float(args["eps"])
    late_profile = {}
    for field in ("density", "count", "Neff", "cumulative_mass", "cumulative_count"):
        late_profile[field] = window_statistics(times, [row["profile"][field] for row in rows], *late, max_gap_Myr=gap)
    late_profile["edges"] = final["profile"]["edges"]
    late_profile["interpretation"] = "descriptive time-weighted profiles; averaged counts are never reused as independent Poisson observations"
    gamma = {}
    for key in final.get("fits", {}):
        chosen = [row for row in rows if late[0] <= row["time_Myr"] <= late[1] and key in row.get("fits", {})]
        valid_rows = [row for row in rows if key in row.get("fits", {}) and row["fits"][key].get("gamma") is not None]
        values = [row["fits"][key]["gamma"] for row in valid_rows]
        stats = window_statistics([row["time_Myr"] for row in valid_rows], values, *late, max_gap_Myr=gap)
        gamma[key] = dict(time_summary=stats, snapshot_conditional_intervals=[dict(
            time_Myr=row["time_Myr"], gamma=row["fits"][key]["gamma"],
            gamma_ci95=row["fits"][key]["gamma_ci95"],
            gof_pvalue=row["fits"][key].get("gof_pvalue")) for row in chosen],
            interpretation="each interval is conditional on that snapshot's count model; no pooled temporal confidence interval")
    bound_cuts = {}
    cuts = sorted(set(key for row in rows for key in row.get("instantaneous_bound_cuts", {})), key=float)
    for cut in cuts:
        chosen = [row for row in rows if cut in row.get("instantaneous_bound_cuts", {})]
        fields = {}
        for field in ("total_mass", "cold_mass", "cold_M300"):
            fields[field] = window_statistics([row["time_Myr"] for row in chosen],
                                              [row["instantaneous_bound_cuts"][cut][field] for row in chosen],
                                              *late, max_gap_Myr=max(160., gap))
        bound_cuts[cut] = dict(final=final.get("instantaneous_bound_cuts", {}).get(cut), late_window=fields,
                              interpretation="instantaneous finite-radius isolated self-unbinding; no tidal-survival theorem")
    mass100 = window_statistics(times, [row["M100"] for row in rows], *late, max_gap_Myr=gap)
    mass300 = window_statistics(times, [row["M300"] for row in rows], *late, max_gap_Myr=gap)
    orbit = None
    if args.get("host", False):
        orbit = orbital_windows(times, [row["host_radius_pc"] for row in rows], [row["M300"] for row in rows],
                                 *post, peri_separation, peri_prominence, gap)
    screen = radial_screen(final["profile"], final["relaxation"], eps)
    preferred = radial_screen(final["profile"], final["relaxation"], eps, age_Myr=20000.)
    late_screen_rows = [row for row in rows if late[0] <= row["time_Myr"] <= late[1]]
    late_screens = [radial_screen(row["profile"], row["relaxation"], eps) for row in late_screen_rows]
    radius = np.asarray(final["profile"]["edges"], float)
    all_late_pass = np.all([row["all_pass"] for row in late_screens], axis=0) if late_screens else np.zeros(len(radius), bool)
    late_pass = [np.all(all_late_pass[i:]) for i in range(len(radius))]
    late_r = float(radius[np.flatnonzero(late_pass)[0]]) if np.any(late_pass) and mass300["complete"] else None
    return dict(name=name, args=args, model=data.get("model"), integrator=data.get("integrator"),
                initial_conditions=data.get("initial_conditions", {}),
                final=dict(time_Myr=final["time_Myr"], M100=final["M100"], M300=final["M300"],
                           cold_count100=final.get("cold_count100"), cold_count300=final.get("cold_count300"),
                           star_count300=final.get("star_count300"), profile=final["profile"],
                           gamma_fits=_fit_records(final, eps), screen=screen, preferred_screen=preferred,
                           collision_support_locality=[float(r) >= 2. * args["h"] for r in radius]),
                late_window=dict(interval_Myr=list(late), M100=mass100, M300=mass300,
                                 profile=late_profile, gamma=gamma, all_snapshot_screen_pass=all_late_pass.tolist(),
                                 r_screen_pc=late_r, snapshot_count=len(late_screen_rows)),
                bound_cuts=bound_cuts, orbit=orbit, maxima=data.get("maxima", {}),
                collisions=data.get("collisions"), mean_collisions_per_cold_particle=data.get("mean_collisions_per_cold_particle"),
                runtime_seconds=data.get("runtime_seconds"),
                numerical_convergence="pending matched controls and independent initial realizations",
                core_established=False, uncertainty="conditional count intervals plus descriptive temporal scatter only; no numerical-bias confidence interval")


def _relative(a, b):
    return None if a is None or b is None or a == 0. else float((b - a) / a)


def recorded_conservation_failures(case):
    """Expose known invariant failures; this is not a replacement for audit."""
    maxima=case.get('maxima',{})
    limits=dict(E=.001,internal_work=.001,host_work=.001,Jint=1.e-7,Jorb=1.e-7,Jtotal=1.e-7,P=1.e-7)
    return [key for key,limit in limits.items() if key in maxima and
            (not np.isfinite(maxima[key]) or maxima[key]>limit if key in ('internal_work','host_work')
             else not np.isfinite(maxima[key]) or maxima[key]>=limit)]


def _screened_comparison(a, b, screen_a, screen_b):
    if screen_a is None or screen_b is None:
        return dict(available=False, reason="one_or_both_cases_have_no_complete_radial_screen")
    common = max(screen_a, screen_b)
    edges_a, edges_b = np.asarray(a["edges"]), np.asarray(b["edges"])
    if not np.array_equal(edges_a, edges_b):
        return dict(available=False, reason="radial_coverage_mismatch")
    keep = edges_a[:-1] >= common
    if not np.any(keep):
        return dict(available=False, reason="screen_outside_profile_coverage")
    first = int(np.flatnonzero(keep)[0])
    reduced_a = dict(edges=a["edges"][first:], density=a["density"][first:])
    reduced_b = dict(edges=b["edges"][first:], density=b["density"][first:])
    return dict(available=True, independently_screened_rmin_pc=common,
                original_bin_indices=np.flatnonzero(keep).tolist(),
                comparison=compare_profiles(reduced_a, reduced_b),
                interpretation="bins selected only by pre-existing force/count/relaxation gates; full unfiltered comparison also retained")


def compare_cases(cases):
    comparisons = []
    names = sorted(cases)
    for offset, name_a in enumerate(names):
        for name_b in names[offset + 1:]:
            a, b = cases[name_a], cases[name_b]
            matched, kind, changes = control_difference(a["args"], b["args"])
            # Different initial scrambles alone are realizations, not a
            # parameter-refinement comparison. Other mixed changes are explicit.
            if not changes or set(changes).issubset({"seed", "collision_seed"}):
                continue
            initial_admission=initial_state_admission(a['args'],b['args'],a['initial_conditions'],b['initial_conditions'])
            arguments_matched=matched
            matched=matched and initial_admission['compatible']
            if arguments_matched and not matched:kind='incompatible_initial_states'
            full = compare_profiles(a["final"]["profile"], b["final"]["profile"])
            failures = [i for i, flag in enumerate(full["within_tolerance"]) if not flag]
            row = dict(case_a=name_a, case_b=name_b, kind=kind, matched_single_factor=matched,
                       changed_arguments=changes, arguments_a=a["args"], arguments_b=b["args"],
                       final_M100_relative_change=_relative(a["final"]["M100"], b["final"]["M100"]),
                       final_M300_relative_change=_relative(a["final"]["M300"], b["final"]["M300"]),
                       late_M300_relative_change=_relative(a["late_window"]["M300"]["mean"], b["late_window"]["M300"]["mean"]),
                       full_final_density_comparison=full, full_radial_failure_bins=failures,
                       independently_screened_final=_screened_comparison(a["final"]["profile"], b["final"]["profile"],
                            a["final"]["screen"]["r_screen_pc"], b["final"]["screen"]["r_screen_pc"]),
                       initial_phase_space_hash_identical=initial_admission['exact_phase_space_hash_identical'],
                       initial_state_admission=initial_admission,arguments_single_factor=arguments_matched,
                       initial_state_caveat=initial_admission['caveat'],
                       backend_admission=('separate backend validation/control; not an N-only refinement' if 'backend' in changes else 'same recorded backend; source/binary provenance remains in manifests'),
                       recorded_conservation_failures=dict(a=recorded_conservation_failures(a),b=recorded_conservation_failures(b)),
                       numerical_convergence="pending independent seeds and complete matched-control matrix")
            late_a, late_b = a["late_window"]["profile"], b["late_window"]["profile"]
            if late_a["density"]["complete"] and late_b["density"]["complete"]:
                pa = dict(edges=late_a["edges"], density=late_a["density"]["mean"])
                pb = dict(edges=late_b["edges"], density=late_b["density"]["mean"])
                row["full_late_density_comparison"] = compare_profiles(pa, pb)
                row["independently_screened_late"] = _screened_comparison(pa, pb, a["late_window"]["r_screen_pc"], b["late_window"]["r_screen_pc"])
            else:
                row["full_late_density_comparison"] = dict(coverage_complete=False, reason="incomplete_8to10Gyr_window")
            comparisons.append(row)
    return comparisons


def _t_interval(values):
    values = np.asarray(values, float)
    if len(values) == 0:
        return dict(count=0, mean=None, ci95=None)
    mean = float(np.mean(values))
    interval = None
    if len(values) > 1:
        error = float(student_t.ppf(.975, len(values) - 1) * np.std(values, ddof=1) / np.sqrt(len(values)))
        interval = [mean - error, mean + error]
    return dict(count=len(values), mean=mean, ci95=interval,
                method="Student-t interval across independent initial scrambles; excludes numerical bias; small samples are descriptive")


def summarize_realizations(cases):
    groups = {}
    for name, case in cases.items():
        args = case["args"]
        controls = {key: args.get(key, DEFAULTS.get(key)) for key in CONTROL_KEYS if key not in ("seed", "collision_seed")}
        key = json.dumps(controls, sort_keys=True)
        groups.setdefault(key, dict(controls=controls, cases=[], by_seed={}))
        group = groups[key]; group["cases"].append(name)
        group["by_seed"].setdefault(str(args.get("seed", 87319)), []).append(case)
    output = []
    for group in groups.values():
        per_seed_final, per_seed_late = [], []
        for seed_cases in group["by_seed"].values():
            per_seed_final.append(float(np.mean([case["final"]["M300"] for case in seed_cases])))
            late = [case["late_window"]["M300"]["mean"] for case in seed_cases if case["late_window"]["M300"]["complete"]]
            if late:
                per_seed_late.append(float(np.mean(late)))
        output.append(dict(controls=group["controls"], cases=group["cases"],
                           independent_initial_seeds=sorted(group["by_seed"]),
                           n_initial_realizations=len(group["by_seed"]),
                           final_M300=_t_interval(per_seed_final), late_M300=_t_interval(per_seed_late),
                           interpretation="multiple collision RNGs with one initial seed are grouped, never counted as independent initial realizations"))
    return output


def load_completed(root, include_pilots, late_end):
    loaded, exclusions, inputs = {}, [], []
    for path in sorted(Path(root).glob("run_*/results.json")):
        name = path.parent.name[4:]
        manifest_path = path.with_name("manifest.json")
        if not manifest_path.exists():
            exclusions.append(dict(case=name, reason="missing_manifest")); continue
        manifest = json.loads(manifest_path.read_text())
        if manifest.get("run", {}).get("status") != "completed":
            exclusions.append(dict(case=name, reason="manifest_not_completed", status=manifest.get("run", {}).get("status"))); continue
        data = json.loads(path.read_text())
        pilot = "pilot" in name.lower() or data["args"].get("duration", 0.) < late_end
        if pilot and not include_pilots:
            exclusions.append(dict(case=name, reason="pilot_or_short_validation_excluded", duration_Myr=data["args"].get("duration"))); continue
        loaded[name] = data
        for source in (path, manifest_path):
            inputs.append(dict(path=str(source.resolve()), sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
    return loaded, exclusions, inputs


def _label(case):
    a = case["args"]
    failed=recorded_conservation_failures(case)
    failure=(('E FAIL ' if 'E' in failed else 'ledger FAIL ') if failed else '')
    return failure + ("pilot " if case.get("pilot_or_short_validation") else "") + ("H" if a.get("host") else "I") + (" CL" if a.get("collisionless") else " el") + f" N{a['ncold']} e{a['eps']:g} h{a['h']:g} dt{a['dt']:g} s{a.get('seed',87319)} {a.get('backend',DEFAULTS['backend'])}"


def make_figure(output, cases, raw, comparisons):
    os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/dwarf_resolution_matplotlib")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(14., 10.), constrained_layout=True)
    colors = plt.cm.tab20(np.linspace(0., 1., max(len(cases), 1)))
    for color, (name, case) in zip(colors, sorted(cases.items())):
        args, final = case["args"], case["final"]
        profile = final["profile"]
        density = np.asarray(profile["density"])
        late = case["late_window"]["profile"]["density"]
        if late["complete"]:
            density = np.asarray(late["mean"])
        radius = np.asarray(profile["radius"])
        style = ":" if args.get("collisionless") else "--" if args.get("host") else "-"
        axes[0, 0].plot(radius, np.where(density > 0., density, np.nan), style, color=color, label=_label(case), lw=1.4)
        for fit_summary in final["gamma_fits"].values():
            fit = fit_summary["fit"]
            if fit["gamma"] is None:
                continue
            position = np.sqrt(np.prod(fit["interval"]))
            lower, upper = fit["gamma_ci95"]
            error = [[max(0., fit["gamma"] - lower)], [max(0., upper - fit["gamma"])]] if lower is not None and upper is not None else None
            axes[0, 1].errorbar([position], [fit["gamma"]], yerr=error, fmt="o", color=color,
                               mfc=color if fit_summary["classification"]["numerical_screen_pass"] else "white", ms=3., alpha=.65, lw=.65)
        if args.get("host"):
            rows = raw[name]["snapshots"]
            axes[1, 0].plot(np.array([row["time_Myr"] for row in rows]) / 1000.,
                            np.array([row["M300"] for row in rows]) / 1.e6, style, color=color, label=_label(case), lw=1.25)
    axes[0, 0].set(xscale="log", yscale="log", xlabel="Radius (pc)", ylabel=r"Cold density ($M_\odot\,\mathrm{pc}^{-3}$)",
                    title="8–10 Gyr mean where complete; otherwise endpoint")
    axes[0, 1].axhspan(-.3, .3, color=".8", alpha=.35)
    axes[0, 1].set(xscale="log", xlabel="Geometric centre of fitted interval (pc)", ylabel=r"Effective $\gamma$ in $\rho\propto r^{-\gamma}$",
                    title="Endpoint fits; bars: conditional count 95% intervals")
    axes[0, 1].text(.02, .02, "Hollow markers fail a numerical screen.\nSlope alone never establishes a core.", transform=axes[0, 1].transAxes, fontsize=8)
    axes[1, 0].set(xlabel="Time (Gyr)", ylabel=r"Host-remnant $M(<300\,\mathrm{pc})$ (million $M_\odot$)",
                    title="Individual host realizations; orbital windows in JSON")
    chosen = [row for row in comparisons if row["matched_single_factor"] and row["kind"] in ("ncold", "eps", "h", "dt", "collisionless", "collision_method")]
    shown = chosen[:24]
    if shown:
        values = [100. * row["final_M300_relative_change"] if row["final_M300_relative_change"] is not None else np.nan for row in shown]
        bad=[any(row['recorded_conservation_failures'].values()) for row in shown]
        axes[1, 1].bar(np.arange(len(shown)), values, color=['#bd722d' if failed else '#657b8a' for failed in bad], width=.7)
        if any(bad):
            axes[1, 1].text(.02,.98,'Orange: a member fails a conservation gate; diagnostic only',va='top',transform=axes[1,1].transAxes,fontsize=7)
        axes[1, 1].axhspan(-10., 10., color="#b9d3be", alpha=.45)
        labels = []
        for row in shown:
            aa, bb, key = row["arguments_a"], row["arguments_b"], row["kind"]
            before, after = aa.get(key, DEFAULTS.get(key)), bb.get(key, DEFAULTS.get(key))
            before = f"{before:g}" if isinstance(before, (int, float)) else str(before)
            after = f"{after:g}" if isinstance(after, (int, float)) else str(after)
            labels.append(("H " if aa.get("host") else "I ") + key + " " + before + "→" + after + (f" N{aa['ncold']}" if key != "ncold" else ""))
        axes[1, 1].set_xticks(np.arange(len(shown)), labels, rotation=45, ha="right", fontsize=7)
    else:
        axes[1, 1].text(.5, .5, "No matched single-factor controls completed", ha="center", va="center", transform=axes[1, 1].transAxes)
    axes[1, 1].axhline(0., color=".4", lw=.7)
    axes[1, 1].set(ylabel="Endpoint M300 change (%)", title=f"Matched controls ({len(shown)}/{len(chosen)} shown); convergence pending")
    if cases:
        axes[0, 0].legend(frameon=False, fontsize=6, ncol=1 if len(cases) < 8 else 2)
    else:
        axes[0, 0].text(.5, .5, "No completed non-pilot cases", ha="center", transform=axes[0, 0].transAxes)
    title = "Prepared 3D carrier dwarf: resolution and elastic/collisionless controls\nConditional profile diagnostics; numerical convergence requires matched controls and independent realizations"
    if any(case.get("pilot_or_short_validation") for case in cases.values()):
        title += "\nIncludes short validation pilots; not 10-Gyr production evidence"
    fig.suptitle(title, fontsize=12)
    fig.savefig(Path(output) / "resolution_summary.png", dpi=190)
    plt.close(fig)


def write_tables(output, cases, comparisons):
    with (Path(output) / "cases.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["case", "pilot_or_short_validation", "host", "collisionless", "ncold", "eps_pc", "h_pc", "dt_Myr", "seed", "final_M100", "final_M300", "mean8to10Gyr_M300", "temporal_std8to10Gyr_M300", "r_screen_pc", "preferred_r_screen_pc", "pericentre_count", "last_complete_cycle_mean_M300", "max_E_error", "runtime_seconds", "convergence"])
        for name, case in sorted(cases.items()):
            a, final, late, orbit = case["args"], case["final"], case["late_window"], case["orbit"]
            writer.writerow([name, case["pilot_or_short_validation"], a.get("host", False), a.get("collisionless", False), a["ncold"], a["eps"], a["h"], a["dt"], a.get("seed"), final["M100"], final["M300"], late["M300"]["mean"], late["M300"]["temporal_std"], final["screen"]["r_screen_pc"], final["preferred_screen"]["r_screen_pc"], len(orbit["pericentres"]) if orbit else 0, orbit["last_complete_cycle"].get("mean") if orbit else None, case["maxima"].get("E"), case["runtime_seconds"], case["numerical_convergence"]])
    with (Path(output) / "comparisons.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["case_a", "case_b", "kind", "matched_single_factor", "changed_arguments", "final_M100_relative_change", "final_M300_relative_change", "late_M300_relative_change", "radial_coverage_match", "all_radial_bins_within10percent", "radial_failure_bin_indices", "convergence"])
        for row in comparisons:
            writer.writerow([row["case_a"], row["case_b"], row["kind"], row["matched_single_factor"], ",".join(row["changed_arguments"]), row["final_M100_relative_change"], row["final_M300_relative_change"], row["late_M300_relative_change"], row["full_final_density_comparison"]["coverage_match"], row["full_final_density_comparison"]["all_within_tolerance"], ",".join(map(str, row["full_radial_failure_bins"])), row["numerical_convergence"]])


def main(output, input_root=HERE, include_pilots=False, late=(8000., 10000.), post=(100., 300.), peri_separation=300., peri_prominence=1000.):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError("analysis output must be a fresh directory")
    raw, exclusions, inputs = load_completed(input_root, include_pilots, late[1])
    cases = {name: summarize_case(name, data, late, post, peri_separation, peri_prominence) for name, data in raw.items()}
    for name, case in cases.items():
        case["pilot_or_short_validation"] = "pilot" in name.lower() or case["args"].get("duration", 0.) < late[1]
    comparisons = compare_cases(cases)
    result = dict(cases=cases, comparisons=comparisons, realization_groups=summarize_realizations(cases), exclusions=exclusions,
                  policy=dict(include_pilots=include_pilots, late_interval_Myr=list(late), fixed_post_pericentre_offsets_Myr=list(post),
                              numerical_convergence="always pending independent matched-control/seed/shape/centring assessment; passing one band is not a convergence claim",
                              uncertainty="snapshot Poisson intervals and temporal scatter are separate; no pooled correlated-snapshot CI",
                              manifest_hashes_revalidated=False), inputs=inputs)
    for filename in ("analyse_resolution.py", "profile_diagnostics.py"):
        path = HERE / filename
        result["inputs"].append(dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    output.mkdir(parents=True, exist_ok=False)
    (output / "analysis.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    write_tables(output, cases, comparisons)
    make_figure(output, cases, raw, comparisons)
    print(json.dumps(dict(output=str(output), completed_cases=len(cases), excluded_records=len(exclusions), comparisons=len(comparisons), numerical_convergence="pending")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--input-root", default=str(HERE))
    parser.add_argument("--include-pilots", action="store_true")
    parser.add_argument("--late-start", type=float, default=8000.)
    parser.add_argument("--late-end", type=float, default=10000.)
    parser.add_argument("--post-peri-start", type=float, default=100.)
    parser.add_argument("--post-peri-end", type=float, default=300.)
    parser.add_argument("--min-peri-separation", type=float, default=300.)
    parser.add_argument("--peri-prominence", type=float, default=1000.)
    args = parser.parse_args()
    main(args.output, args.input_root, args.include_pilots, (args.late_start, args.late_end),
         (args.post_peri_start, args.post_peri_end), args.min_peri_separation, args.peri_prominence)
