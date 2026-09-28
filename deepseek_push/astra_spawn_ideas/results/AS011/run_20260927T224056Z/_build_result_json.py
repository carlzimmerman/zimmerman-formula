#!/usr/bin/env python3
"""Build result.json for AS011 run run_20260927T224056Z from raw_output.json + hashes."""
import json, hashlib, os

RUN = "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/astra_spawn_ideas/results/AS011/run_20260927T224056Z"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

raw = json.load(open(os.path.join(RUN, "raw_output.json")))

# ------------------------------------------------------------------ inputs
input_paths = {
    "deepseek_push/astra_spawn_ideas/AS011_alternative_footing_as_a_separate_hypothesis.md": None,
    "deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md": None,
    "deepseek_push/astra_spawn_ideas/RESULT_CONTRACT.json": None,
    "deepseek_push/astra_spawn_ideas/FIRST_PRINCIPLES_AND_BRANCHING.md": None,
    "deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json": None,
    "deepseek_push/astra_spawn_ideas/ORCHESTRATOR.md": None,
    "README.md": None,
    "STANDING.md": None,
    "qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md": None,
    "campaign_fresh_gravity_astra/DERIVATIONS.md": None,
}
input_sha256 = {}
for p in input_paths:
    ap = os.path.join(REPO, p)
    try:
        input_sha256[p] = sha256(ap)
    except FileNotFoundError as e:
        input_sha256[p] = "MISSING: " + str(e)

# ------------------------------------------------------------------ artifacts (exclude result.json itself)
artifact_names = [
    "derivation.md",
    "compute_AS011_footing_separation.py",
    "raw_output.txt",
    "raw_output.json",
    "time_err.txt",
    "AS011_footing_separation_certificates.lean",
    "lean_check.out",
    "_build_result_json.py",
]
artifacts_sha256 = {n: sha256(os.path.join(RUN, n)) for n in artifact_names}
child_spec = "deepseek_push/astra_spawn_ideas/branches/AS011/AS011.C01.md"
artifacts_sha256[child_spec] = sha256(os.path.join(REPO, child_spec))

# ------------------------------------------------------------------ checks (compact, from raw)
checks = []
for ch in raw["checks"]:
    checks.append({
        "name": ch["name"],
        "observed": ch["observed"],
        "reference": ch["reference"],
        "residual": ch.get("relresidual", ch.get("absresidual")),
        "tolerance": ch.get("tol", ch.get("atol")),
        "kind": ch["kind"],
        "unit": ch["unit"],
        "pass": ch["pass"],
    })

execution_bounds = {
    "declared": {"wall_time_s": 120, "memory_mb": 512, "threads": 1},
    "enforced": {
        "rlimit_cpu_s": 120, "rlimit_as_bytes": 536870912,
        "threads_actually_spawned": 0,
        "single_process": True,
    },
    "measured": {"wall_s": raw["wall_seconds"], "maxrss_bytes": raw["maxrss_bytes"],
                 "wall_under_120s": raw["bounds"]["wall_under_120s"],
                 "rss_under_512MB": raw["bounds"]["rss_under_512MB"]},
}

result = {
    "schema_version": 2,
    "task_id": "AS011",
    "task_sha256": input_sha256["deepseek_push/astra_spawn_ideas/AS011_alternative_footing_as_a_separate_hypothesis.md"],
    "run_id": "run_20260927T224056Z",
    "worker": "deepseek/deepseek-v4-flash-0731 (model) via openrouter, Hermes platform subagent on macOS host (Python 3.13.9; decimal 60-digit arithmetic; Lean 4.34.0-rc2 via lake). Not 'DeepSeek-by-folder-name': identity taken from runtime context.",
    "started_utc": "2026-09-27T22:40:56Z",
    "finished_utc": "2026-09-27T22:59:12Z",
    "execution_status": "completed",
    "outcome": "supports_scoped_claim",
    "exact_claim": (
        "Given a0 = kappa*c*sqrt(G*rho_Lambda) with positive G, c, kappa, rho_Lambda, the adopted kappa_can = 1/2 "
        "and the given roundings a0_can = 9.3619e-11 m/s^2 and a0_alt = 1.1279e-10 m/s^2 (R_a = a0_alt/a0_can = 1.2047768081...): "
        "the alternative footing is a SEPARATE hypothesis realizable in exactly two mutually exclusive one-cell models — "
        "(A) fixed density: kappa_alt = R_a/2 = 0.6023884040... (Delta kappa = +0.1023884040, +20.4767% relative; a NEW adopted "
        "coefficient, not derived), or (B) fixed kappa: rho_Lambda_alt = R_a^2 * rho_Lambda_can = 1.45148716 * rho_Lambda_can "
        "(+45.15%, Lambda_alt = R_a^2 Lambda_can under G_E = G_N). Both cannot hold in one (kappa, rho_Lambda) cell "
        "(uniqueness certified in Lean). Dimensionless relations in y = B/a0 are footing-covariant in form; at fixed (G, M_b) "
        "the dimensional predictions rescale exactly: Newtonian g x1, deep g x R_a^(1/2) = 1.0976232542, v_flat x R_a^(1/4) = "
        "1.0476751663, r_M x R_a^(-1/2) = 0.9110594151. Domain: all variables positive; no per-object a0 fit; no dynamics "
        "beyond the CORE scale identities (Q/RAR/MU2 appear only as labelled comparisons; operative filtered-MONO gate untouched)."
    ),
    "framework_cell": {
        "branch": "CORE scale identities (AS011 declared branch); Q, RAR, MU2, EXP AQUAL, MONO kept distinct and unmerged",
        "kernel": "none (scale identities only); labelled Q-branch v^4 identity used as comparison witness",
        "filter": "none (no heat filter in this seed)",
        "gate": "requirement 13 cosmological acceleration-scale relation: a0 = (c/2)*sqrt(G*rho_Lambda) preserved as INPUT; kappa = 1/2 adopted (fitted 0.551 +/- 0.043 recorded in README is noted, not used)",
        "coupling": "single G = 6.67430e-11 for the scale identity; G_E/G_N ratio carried (Lambda statement conditional on G_E = G_N)",
        "parameters": "a0_can = 9.3619e-11, a0_alt = 1.1279e-10 m/s^2; kappa_can = 1/2; c = 299792458 m/s; M_sun = 1.98847e30 kg; pc = 3.085677581491367e16 m; k_B = 1.380649e-23 J/K (carried, unused)",
        "scale_footing": "BOTH footings carried separately in every dimensional example; ratio (a0_alt/a0_can)^2 = 1.45148716 is the fixed-kappa density shift; kappa_alt = R_a/2 is the fixed-density kappa shift",
        "boundaries": "positive variables only; r > 0; deep-limit domain r >> r_M with leading neglected term (r_M/r)^2 stated",
        "initial_conditions": "none (static algebraic identities)",
        "units": "SI (m, kg, s, J); kpc for r_M displays",
    },
    "new_assumptions": [],
    "input_sha256": input_sha256,
    "artifacts_sha256": artifacts_sha256,
    "commands": [
        "shasum -a 256 README.md deepseek_push/astra_spawn_ideas/AS011_alternative_footing_as_a_separate_hypothesis.md deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md deepseek_push/astra_spawn_ideas/RESULT_CONTRACT.json qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md campaign_fresh_gravity_astra/DERIVATIONS.md STANDING.md (cwd: repo root; source-hash verification)",
        "python3 compute_AS011_footing_separation.py > raw_output.txt (cwd: run dir; enforced RLIMIT_CPU=120 s, RLIMIT_AS=512 MB in-script)",
        "lake env lean <run_dir>/AS011_footing_separation_certificates.lean > lean_check.out (cwd: fable_independent_2026/lean_2026; Mathlib cached)",
        "python3 <inline builder> -> result.json (cwd: run dir)",
    ],
    "execution_bounds": execution_bounds,
    "checks": checks,
    "tested_domain": (
        "Exact real-arithmetic domain: G, c, kappa, rho_Lambda, M_b, r all positive. Numerical witnesses at 60 significant "
        "digits (decimal); Q-branch v^4 identity sampled at r/r_M in {2, 3, 10, 100, 1e4} with M_b = 1e11*M_sun; "
        "y = B/a0 = 1 boundary on both footings. Dimensional examples: M_b = M_sun and M_b = 1e11*M_sun. Input roundings "
        "carry 5 significant digits, hence ratio statements are physically significant to ~1e-5 relative (algebraic identities "
        "hold to 1e-50..1e-60). No stochastic sampling, no fits, no seeds."
    ),
    "failed_attempts": [
        {"artifact": "none preserved separately (intermediate compiles overwrote lean_check.out)",
         "cause": "Lean v1: mul_pos application shape (1/2)*c mistaken; rw [← h3] direction wrong (h3 : a0a = 2*kappa_a*a0c needs forward rw); rw [← mul_assoc] on kappa*c*sqrt needs forward mul_assoc. All three fixed; final compile clean, zero sorry.",
         "final_evidence": "lean_check.out (exit 0, axioms {propext, Classical.choice, Quot.sound} for all 8 theorems)"},
        {"artifact": "none", "cause": "Compute v1: JSON dump failed on Decimal (added JSONEncoder); negative-control checks initially reported FAIL on expected-inconsistency (switched to check_flag semantics that PASS by detecting the inconsistency); NC2b ref=0 relative-residual undefined (switched to absolute residual 6.4e-60 < 1e-50); one junk self-referential check removed. Final raw_output.json/raw_output.txt reflect the corrected run (all 22 pass)."}
    ],
    "limitations": [
        "kappa = 1/2 remains ADOPTED (fitted value 0.551 ± 0.043 recorded elsewhere); this seed derives no kappa and no a0 value.",
        "No dynamics: the operative gate is filtered MONO + criterion B (amended requirement 1 of FRIED_CHICKEN_SPEC); this seed's CORE identities neither certify nor constrain MONO dynamics. Q/RAR/MU2/EXP appear only as labelled comparisons.",
        "The a0–Lambda link is conditional on G_E = G_N; the G_E/G_N ratio is carried, not set equal, in any Lambda consequence.",
        "The identification of rho_Lambda with the cosmic vacuum density is a framework postulate, not derived here.",
        "Inputs a0_can, a0_alt are 5-digit roundings; R_a^2 = 1.45148716 matches the campaign-stated constant to 1.8e-9 relative, i.e. within rounding.",
        "The choice between footing A and footing B (and between canonical and alternative a0) is not settled by this algebra; it requires an independent kappa or rho_Lambda determination and MONO-branch dimensional data.",
        "Numerical witnesses are finite-precision consistency checks with recorded residuals; exactness lives in the Lean-certified identities and direct algebra.",
    ],
    "next_unresolved_implication": (
        "Which footing the operative theory realizes: requirement 13's a0–vacuum relation is still an input. The missing bridge is an "
        "independent determination of kappa or rho_Lambda (respectively: a derivation of the 1/2 normalization, or a measured vacuum "
        "density compatible with one footing), followed by propagation of the chosen footing through the operative filtered-MONO branch "
        "so the 4.77% v_flat difference at fixed M_b becomes a falsifiable dimensional prediction."
    ),
    "suggested_followup": (
        "Child AS011.C01 (spec written, NOT dispatched — no spawn mechanism in this worker): forward-map both footings through the "
        "operative filtered nu_mono branch (amended requirement 1) for SPARC-like M_b(r) inputs, quote v_flat/r_M differences at fixed "
        "M_b, and construct the discriminating statistic (e.g., BTFR intercept shift of 0.0477 dex-equivalent vs reported intrinsic "
        "scatter) so the two footings separate at the data level. Duplicate check: closest seeds AS007 (CORE v_flat sensitivity, already "
        "run, CORE branch) and AS012 (uncertainty propagation — different object); child changes branch (CORE -> MONO), target claim "
        "(footing discrimination statistic), and observable (SPARC/BTFR forward map)."
    ),
    "acceptance_state": "unreviewed",
    "ancestry": None,
    "first_principles_inputs": {
        "primitive_assumptions": [
            "a0 = kappa*c*sqrt(G*rho_Lambda) with kappa = 1/2 adopted (framework input, not derived)",
            "r_M = sqrt(G*M_b/a0), v_flat^4 = G*M_b*a0 (framework CORE identities)",
            "a0_can = 9.3619e-11 and a0_alt = 1.1279e-10 m/s^2 as given footings",
            "G = 6.67430e-11 m^3 kg^-1 s^-2, c = 299792458 m/s, M_sun = 1.98847e30 kg, pc = 3.085677581491367e16 m, k_B = 1.380649e-23 J/K",
            "positivity of all physical variables (domain)",
        ],
        "measured_calibrations": ["none added; a0 values are stated conventions, kappa is adopted"],
        "boundary_initial_data": ["none (algebraic identities on the positive domain)"],
        "derived_equations": [
            "rho_Lambda = 4 a0^2/(G c^2) (exact rearrangement at kappa = 1/2)",
            "Lambda = 32*pi*a0^2/c^4 conditional on G_E = G_N",
            "R_a^2 = (kappa_alt/kappa_can)^2 * (rho_alt/rho_can) factorization (Lean: footing_factorization)",
            "kappa_alt = R_a/2 at fixed rho (Lean: alt_kappa_effective)",
            "(a0_alt/a0_can)^2 = rho_alt/rho_can at fixed kappa (Lean: fixed_kappa_density_ratio)",
            "v^4 = G*M_b*a0 + (G*M_b/r)^2 exact on labelled Q branch; deep-limit leading neglected term (r_M/r)^2",
            "uniqueness: same (kappa, rho) cell -> same a0; same kappa + same a0 -> same rho (Lean: both_fixed_implies_same_a0, a0_determines_rho, different_a0_forces_different_rho)",
        ],
    },
    "closure_implication": {
        "named_gate": "Requirement 13 (cosmological acceleration-scale relation) — a0 = (c/2)*sqrt(G*rho_Lambda) preserved as input",
        "exact_implication": (
            "AS011 establishes the exact bookkeeping of the two footings: a single (kappa, rho_Lambda) cell cannot realize both "
            "stated a0 values; the alternative footing is a separate hypothesis requiring either a new adopted kappa = 0.6023884040... "
            "(fixed density) or a 45.15% denser vacuum (fixed kappa = 1/2). Any closure witness that cites an a0 value must therefore "
            "declare its footing and its (kappa, rho_Lambda) cell; mixing footings is a model error, not an uncertainty band. "
            "This constrains the parameter cell of the common-action witness but does not by itself close requirement 13 (kappa and rho_Lambda "
            "remain inputs)."
        ),
        "common_action_parameter_domain_compatibility": (
            "The residual freedom (kappa, rho_Lambda) with the constraint R_a^2 = K^2*D is a one-dimensional family: choosing the footing "
            "fixes the ratio K^2*D = 1.45148716. Any same-action witness adopting a0 must supply exactly one (kappa, rho_Lambda) pair "
            "consistent with this constraint; the four candidate coefficients recorded in the framework's kappa discussion (kappa = 1/2, "
            "0.461, 0.551±0.043, 0.6023884040...) are distinct cells, not interchangeable."
        ),
    },
    "child_proposals": [
        {
            "child_id": "AS011.C01",
            "dispatch_state": "spec written to deepseek_push/astra_spawn_ideas/branches/AS011/AS011.C01.md; NOT dispatched (no spawn mechanism in this worker)",
            "scientific_fingerprint": "(MONO filtered-nu_mono branch, kappa=1/2, positive domain + SPARC-like M_b(r), target: footing-discrimination statistic for a0_can vs a0_alt at fixed baryonic mass, observable: v_flat/r_M forward map and BTFR intercept shift vs intrinsic scatter, new input: none — continuation of AS011/run_20260927T224056Z)",
            "new_target_claim": "quote the alternative-footing shift in MONO-branch dimensional predictions at fixed M_b (v_flat x 1.047675..., r_M x 0.911059...) and state whether any reported SPARC/BTFR scatter band separates the two footings at the stated tolerance, with the actual kernel nu_mono (requirement 1 amended text) — not the CORE identities.",
            "why_existing_evidence_does_not_answer_it": "AS011 certifies the CORE-scale bookkeeping only; the operative gate (filtered MONO) changes finite-radius predictions through nu_mono and the heat filter, and no seed in the catalog carries both footings through the MONO forward map with a discrimination statistic.",
            "controls": "negative control: re-run the same statistic with the a0 values swapped (must reverse the classification); limit checks: y -> infinity (Newtonian regime, identical footings) and y -> 0 (deep regime, 4.77% shift).",
            "dependencies": ["AS011 result.json", "amended requirement-1 kernel specification (FRIED_CHICKEN_SPEC.md)", "SPARC/BTFR summary table or equivalent public dataset"],
        }
    ],
    "closure_candidate": None,
}

with open(os.path.join(RUN, "result.json"), "w") as f:
    json.dump(result, f, indent=2)
print("written", os.path.join(RUN, "result.json"))
print("input hashes:", json.dumps(input_sha256, indent=1))