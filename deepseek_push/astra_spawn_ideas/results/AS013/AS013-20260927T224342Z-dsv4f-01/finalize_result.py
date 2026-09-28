#!/usr/bin/env python3
"""Finalize AS013 result: compute artifact SHA-256 hashes and write result.json
(schema v2 per RESULT_CONTRACT.json). result.json is self-referential-excluded."""
import hashlib, json, os, time
from datetime import datetime, timezone

RD = "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/astra_spawn_ideas/results/AS013/AS013-20260927T224342Z-dsv4f-01"
ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula"

def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

artifacts = sorted(os.listdir(RD))
artifacts_sha = {}
for a in artifacts:
    full = os.path.join(RD, a)
    if os.path.isfile(full) and a != "result.json":
        artifacts_sha["deepseek_push/astra_spawn_ideas/results/AS013/AS013-20260927T224342Z-dsv4f-01/" + a] = sha(full)

# ---- parse check rows from raw_output.txt ----
checks = []
with open(os.path.join(RD, "raw_output.txt")) as f:
    for line in f:
        if line.startswith("CHECKROW |"):
            parts = line.strip().split(" | ")
            # parts: ['CHECKROW', name, result, observed, tolerance]
            checks.append({"name": parts[1], "result": parts[2],
                           "observed": parts[3], "tolerance": parts[4]})
assert len(checks) == 43, len(checks)
checks.append({"name": "LEAN_compile_exit0",
               "observed": "lake env lean exit 0; 6 theorems; zero sorry; #print axioms for all six: [propext, Classical.choice, Quot.sound]",
               "tolerance": "exit 0, axioms subset {propext, Classical.choice, Quot.sound}", "result": "PASS"})
checks.append({"name": "SOURCE_HASH_MATCH",
               "observed": "README.md, FRIED_CHICKEN_SPEC.md, DERIVATIONS.md match SOURCE_MANIFEST.json pins exactly",
               "tolerance": "all three pinned task sources match", "result": "PASS"})

input_sha = {
  "README.md": "91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed",
  "STANDING.md": "660462ebe8f98844c418e173a1dada90b9df3800c4d445fd5a0556eb9476bf63",
  "qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md": "98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f",
  "campaign_fresh_gravity_astra/DERIVATIONS.md": "8da8176e3daeaeeaf9e42edb1585f271c92a50c0d9fdd842aa10caee462fb889",
  "deepseek_push/astra_spawn_ideas/AS013_a_distance_scaling_degeneracy_of_the_deep_law.md": "064ff7d011d3946dd1e28c883ffdee75a08d08314cce3852d1c9e962071963af",
  "deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md": "ca696c7fe7cccbe21d754eff833a4c59df6dee962ea61f50f04b5d20d80dddf9",
  "deepseek_push/astra_spawn_ideas/RESULT_CONTRACT.json": "621fdad0067c731654a0fa95eb7a4dd112f8829b96503d8d57c2ee8ca2cc1517",
  "deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json": "fe295b80bddbb0520884036ea5978d8f73174a8520f3ce0f91e2bf0f97f57fba",
}

now = datetime.now(timezone.utc)
finished = now.strftime("%Y-%m-%dT%H:%M:%SZ")

result = {
  "schema_version": 2,
  "task_id": "AS013",
  "task_sha256": input_sha["deepseek_push/astra_spawn_ideas/AS013_a_distance_scaling_degeneracy_of_the_deep_law.md"],
  "run_id": "AS013-20260927T224342Z-dsv4f-01",
  "worker": "deepseek/deepseek-v4-flash-0731 (provider: openrouter); Hermes Agent focused subagent; identity taken from the executing agent's own system context, not guessed from the deepseek_push destination folder",
  "started_utc": "2026-09-27T22:43:42Z",
  "finished_utc": finished,
  "execution_status": "completed",
  "outcome": "supports_scoped_claim",
  "exact_claim": ("Conditional exact theorem (identifiability audit of the deep law). "
    "Let lam, s > 0; flux-derived baryonic masses M_b = 4*pi*(M/L)*D^2*F(theta) (fixed mass-to-light), "
    "circular velocities v = v_los/sin(i), and the deep law v_flat^4 = G*M_b*a0 with "
    "a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 adopted. Then (i) the deep-law prediction — the whole "
    "deep-MOND angular profile v^4(theta) = G*a0*M_b(theta) — is EXACTLY invariant under the two-parameter "
    "distance–inclination group (D, sin i, M_b, a0) -> (lam*D, s*sin i, lam^2*M_b, lam^(-2)*s^(-4)*a0) "
    "with v_los(theta) fixed; equivalently a0 ∝ D^(-2) s^(-4) at fixed velocity (the task's claim is exact); "
    "(ii) the plateau pins exactly the inclination-corrected product M_b*a0*sin^4 i = v_los^4/G; the "
    "individual quantities are degenerate along the orbit: M_b ∝ D^2, a0 ∝ D^(-2), r_M -> lam^2*r_M, "
    "theta_M -> lam*theta_M, y = B/a0 -> lam^2*y; (iii) the degeneracy is exact in the deep regime for "
    "EVERY framework kernel (Q, RAR, MONO all have nu(y) -> y^(-1/2)); it is broken at finite y by "
    "v'^4/v^4 = lam^2*[nu(lam^2*y)/nu(y)]^2 — exactly (lam^2*y+1)/(y+1) = 1 + y(lam^2-1)/(y+1) for the Q "
    "branch (leading neglected deep term y*(lam^2-1), next -(lam^2-1)*y^2, both exact) — and the Newtonian "
    "regime pins D via v(theta) ∝ D^(1/2) at fixed theta; RAR/MONO deep-approach rate (lam-1)*sqrt(y). "
    "Negative control: changing D while freezing M_b (and a0) is internally inconsistent — flux mass "
    "ratio lam^2 = 2.25, Newtonian velocity ratio sqrt(lam) = 1.2247, transition-angle ratio lam^2 = 2.25, "
    "flux-implied a0/a0_adopted = lam^(-2) = 0.4444 — while the joint orbit update passes at relative "
    "residual 9.239e-61 (checker sensitivity proven). Domain: lam, s, y, sin i > 0; point-mass/"
    "spherical-circular idealization for the profile form; SI units; both a0 footings carried separately "
    "(canonical 9.3619e-11, alternative 1.1279e-10 m/s^2); mock galaxy M_b = 1e9 M_sun, D = 10 Mpc, "
    "i = 60 deg: v_flat = 59.3707 / 62.2012 km/s, r_M = 1.2202 / 1.1117 kpc, theta_M = 25.17 / 22.93 "
    "arcsec. Certified: Lean 4, 6 theorems, zero sorry, axioms subset {propext, Classical.choice, "
    "Quot.sound}; sympy residuals exactly 0; 60-dps numerical residuals of the exact identities all "
    "<= 2.5e-60. It is an identifiability statement, not a derivation of dynamics, of kappa, or an "
    "observational fit."),
  "framework_cell": {
    "action": "none beyond the CORE scale identities of group A01 (a0 = kappa*c*sqrt(G*rho_Lambda), "
      "r_M = sqrt(G*M_b/a0), v_flat^4 = G*M_b*a0). No branch action (Q, RAR, MU2, EXP, MONO) is "
      "imported as the mechanism; branches enter only as labelled kernels for the break factor (∗).",
    "source_hashes": {
      "README.md": "91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed",
      "qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md": "98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f",
      "campaign_fresh_gravity_astra/DERIVATIONS.md": "8da8176e3daeaeeaf9e42edb1585f271c92a50c0d9fdd842aa10caee462fb889"
    },
    "kernel": "Q: nu(y)=sqrt(1+1/y); RAR: nu(y)=1/(1-exp(-sqrt(y))); MONO: h_mono construction of the "
      "contract (y_p = 2.539638, h_p = 0.647610, y* = 2.337412, delta = 0.05; derivative-continuous join "
      "verified to relerr 0; within 0.01037 dex of RAR, max at y = 14.4). All used as labelled curves only.",
    "filter": "heat filter S = exp((xi^2/2) Delta) NOT exercised: smoothing operator on the field; the "
      "audited object is the pointwise deep asymptotics v^4 = G a0 M_b (requirement 1 content of the "
      "operative target).",
    "gate": "A01 CORE scale identities / identifiability of the deep law; causality criterion B not "
      "exercised (statics/algebra only). Operative target: filtered MONO with criterion B, amended "
      "thirteen-item spec — the degeneracy applies to its declared deep content regardless of the "
      "filter/branch choice in the deep limit.",
    "coupling": "single Newton coupling G = 6.67430e-11 SI throughout; G_N vs G_bare vs G_cosmo do not "
      "separate in this algebraic object (one G factors out of every identity); no assertion that they "
      "are equal.",
    "parameters": {
      "kappa": "1/2 adopted as input (not derived); the degeneracy is scale-free, so it cannot fix "
        "kappa and kappa's freedom is not removed here.",
      "a0_footings": ["9.3619e-11 m/s^2 (canonical)", "1.1279e-10 m/s^2 (alternative)",
        "carried separately; never share fixed rho_Lambda AND fixed kappa simultaneously"],
      "mass_flux_scaling": "M_b = 4*pi*(M/L)*D^2*F(theta), fixed mass-to-light (task premise)",
      "inclination": "v = v_los/sin i, sin i > 0 (task premise)"
    },
    "scale_footing_note": "a0_alt/a0_can = 1.204776808127; if rho_Lambda held fixed, effective "
      "kappa = 0.602388404063 != 1/2; if kappa held fixed at 1/2, rho ratio = 1.451487157400 "
      "(consistent with sibling AS010 bookkeeping).",
    "boundaries": "r = r_M > 0 (boundary case: B(r_M) = a0 identically, g_Q(r_M)^2 = 2 a0^2); "
      "theta_M = r_M/D; y = B/a0 in (0, inf); lam, s in (0, inf); the point-mass/spherical-circular "
      "idealization for the profile statement.",
    "initial_conditions": "none (static algebraic identities; no evolution)",
    "units": "SI: m/s^2 for a0, g; m^4/s^4 for v^4; kg for M_b; m for r_M, D; rad for theta_M; "
      "kg/m^3 for rho_Lambda; W/m^2 for flux F."
  },
  "new_assumptions": [],
  "input_sha256": input_sha,
  "artifacts_sha256": artifacts_sha,
  "commands": [
    "python3 deepseek_push/astra_spawn_ideas/results/AS013/AS013-20260927T224342Z-dsv4f-01/compute_as013.py "
    "> .../raw_output.txt 2>&1   (cwd: repo root; exit 0; 43/43 checks pass; elapsed 0.137 s; ru_maxrss 58,916,864 B)",
    "cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS013_distance_degeneracy.lean "
    "> .../lean_axioms_out.txt 2>&1   (exit 0; Lean 4.34.0-rc2; 6 theorems; #print axioms lists all clean)",
    "hash verification of README.md, FRIED_CHICKEN_SPEC.md, DERIVATIONS.md, STANDING.md, SOURCE_MANIFEST.json, "
    "task/contract files against SOURCE_MANIFEST.json pins (hashlib; all match)"
  ],
  "execution_bounds": {
    "declared": {"wall_clock_s": 120, "memory_MB": 512, "threads": 1, "precision_dps": 60},
    "enforced": {
      "wall_clock_s": "ENFORCED via signal.alarm(120); observed elapsed 0.137 s",
      "memory_MB": "NOT ENFORCEABLE on this macOS host (resource.setrlimit(RLIMIT_AS, ...) rejected: "
        "'current limit exceeds maximum limit'); observed peak RSS 58,916,864 bytes = 56.2 MB "
        "(ru_maxrss in bytes on macOS), far below the declared 512 MB",
      "threads": "ENFORCED: single-threaded mpmath/sympy prototype; no threads or subprocesses spawned",
      "precision_dps": "mpmath mp.prec = 200 bits (~60 decimal digits)"
    },
    "scale_note": "Cheapest bounded discriminating calculation (0.137 s): the object is exact algebra "
      "plus a finite mock; no larger computation exists or is needed."
  },
  "checks": checks,
  "tested_domain": ("Exact algebraic domain: lam, s, y, sin i > 0; lambda grid {0.5, 0.8, 1.2, 1.5, 2.0, "
    "3.3} x s-grid {0.8, 1.25} x y-grid {1e-4..1e6} (14 points) x both a0 footings; mock M_b = 1e9 M_sun, "
    "D = 10 Mpc, i = 60 deg; RAR/MONO deep-approach rate checked on y in {1e-9, 1e-7, 1e-5}; sympy "
    "symbolic residuals with positive-symbol assumptions; Lean 4 real-algebra certificate. No random "
    "sampling, no seeds, no refinement history beyond the bounded single prototype run and its honest "
    "debug iterations (recorded in failed_attempts)."),
  "failed_attempts": [
    {"artifact": "NC1d code bug: 're-fit a0' recomputed the frozen adopted a0 (identity), making the "
      "control vacuous", "cause": "implementation error in the demo inference step",
     "resolution": "replaced by the flux-implied scale a0_implied = v^4/(G*M_flux) = a0/lam^2 = "
      "0.4444*a0; control now fails as required (NC1d PASS-as-failure)"},
    {"artifact": "CK-G deep-limit probes for RAR/MONO at y=1e-3 observed 1.583e-2 > tolerance 5e-3 "
      "(deviation scales as sqrt(y), not y)", "cause": "tolerance mis-matched the true approach rate",
     "resolution": "probe at y=1e-6 (5.0e-4) plus a dedicated leading-term check dev vs (lam-1)*sqrt(y) "
      "over three decades, max relerr 1.3e-4; all pass with actual residuals"},
    {"artifact": "NC1e absolute tolerance < 1e-50 on a product of magnitude ~1e19 (residual 1.1e-41 = "
      "relative 9e-60, i.e. pure 60-dps roundoff)", "cause": "absolute vs relative tolerance mismatch",
     "resolution": "relative residual criterion; passes at 9.239e-61"},
    {"artifact": "Lean round 1: 'let lam := ... in' inside a theorem statement is not parseable at that "
      "position (error at 74:34)", "cause": "Lean 4 syntax restriction",
     "resolution": "lambda moved to an explicit hypothesis lam = Real.sqrt(M'/M) with subst; compiled"},
    {"artifact": "Lean round 1: 'rw [← hp]' applied to the wrong side of hp in the calc step of "
      "orbit_characterization; 'field_simp' alone left an unsolved polynomial goal in q_break_identity",
     "cause": "rewrite direction error; field_simp does not close that goal in this Mathlib version",
     "resolution": "rw [hp] (rewrite G*M*a -> G*M'*a'); q_break_identity keeps 'field_simp [hy]; ring' "
      "(ring IS needed, contrary to the unused-tactic linter warning at the <;> form)"},
    {"artifact": "linter warnings 'ring does nothing' at the <;> ring sites of the three pure-field "
      "theorems (T1, T2, q_break before its ring was proved necessary)", "cause": "field_simp closes "
      "these goals already",
     "resolution": "trailing ring removed where field_simp closes; final compile exit 0 with a clean "
      "log (one informational linter note resolved)"}
  ],
  "limitations": [
    "Identifiability statement about the deep law; not a statement about real data quality, pipelines, "
      "or any observational fit.",
    "Profile statement v^4(theta) = G a0 M_b(theta) uses the point-mass/spherical-circular idealization; "
      "real disks alter B(theta) but not the algebraic orbit (B stays distance-free).",
    "Mass-to-light held fixed in the flux scaling; a free M/L adds a third degenerate direction (the "
      "knee argument pins a0 only up to M/L).",
    "The exact break factor is proved for Q; RAR and MONO breaks are finite numerical evaluations "
      "(with the exact deep-limit statement common to all kernels via nu(y) ~ y^(-1/2)).",
    "kappa = 1/2 remains adopted, not derived; the scale-free degeneracy cannot remove its freedom.",
    "The univariate statements are exact identities (Lean/sympy); all 60-dps residuals are consistency "
      "checks of those identities, not independent evidence.",
    "A completed task is not closure of gravity; v^4 = G M_b a0 is the operative target's declared deep "
      "content, not a derivation of the constitutive dynamics."
  ],
  "next_unresolved_implication": ("Quantitative identifiability transfer: the per-object and population "
    "sensitivity of a0 (hence of the framework's kappa fit) to the breakers of sect. 3.4 — how much "
    "transition/Newtonian-regime data (knee resolution) and which distance/inclination anchors are needed "
    "for the operative MONO branch (through the heat filter) to pin a0 against realistic (lam, s, M/L) "
    "uncertainties, i.e. the exact error budget of deep-regime-only a0 determinations which inherit the "
    "lambda^(-2) degeneracy."),
  "suggested_followup": ("Dispatch ready child AS013.C01 (spec in derivation.md sect. 11): derive the "
    "degeneracy-breaking power of the interpolating regime under the operative MONO kernel — a Fisher-type "
    "bound/worst-case a0 error from knee-region data under (lam, s, M/L) noise, with the lambda=1 no-bias "
    "and deep-only-collapse controls. Duplicate check: no AS/MY/FGF seed targets the distance–inclination "
    "degeneracy of the deep law; closest A17 high-z seeds (AS1711, AS1765) cover redshift-space "
    "identifiability from the same joint_identifiability source, a distinct fingerprint."),
  "acceptance_state": "unreviewed",
  "ancestry": None,
  "first_principles_inputs": {
    "primitives": [
      "G = 6.67430e-11 m^3 kg^-1 s^-2",
      "c = 299792458 m/s",
      "M_sun = 1.98847e30 kg, pc = 3.085677581491367e16 m",
      "kappa = 1/2 ADOPTED (not derived)",
      "a0 = 9.3619e-11 m/s^2 (canonical) and 1.1279e-10 m/s^2 (alternative), separate footings"
    ],
    "definitions": [
      "a0 = kappa*c*sqrt(G*rho_Lambda) with rho_Lambda = 4 a0^2/(G c^2)",
      "r_M = sqrt(G*M_b/a0), theta_M = r_M/D",
      "v_flat^4 = G*M_b*a0 (deep law, operative target requirement 1)",
      "M_b = 4*pi*(M/L)*D^2*F(theta) (flux-derived mass, fixed mass-to-light)",
      "v = v_los/sin i (inclination projection)"
    ],
    "conditional_inputs_task_declared": [
      "the shape of M_b vs D at fixed flux (M_b proportional to D^2)",
      "inclination scaling v = v_los/sin(i)",
      "kernel labels Q, RAR, MONO as defined in FRAMEWORK_CONTRACT (used as curves only)"
    ],
    "genuinely_derived_here": [
      "exact two-parameter invariance group R_{lam,s} of the deep law (T1, T2 Lean)",
      "pinning: M_b*a0*sin^4 i = v_los^4/G; two same-plateau models differ by exactly one orbit element "
        "(T6 Lean: orbit_characterization)",
      "r_M -> lam^2 r_M (T3 Lean); theta_M -> lam theta_M; y -> lam^2 y",
      "orbit composition law (T4 Lean: orbit_composition)",
      "exact Q-branch break v'^4/v^4 - 1 = y*(lam^2-1)/(y+1) and its leading deep term (T5 Lean)", 
      "RAR/MONO deep-approach rate (lam-1)*sqrt(y) and Newtonian pinning v(theta) ∝ D^(1/2)",
      "internal inconsistency of the frozen-M_b distance update (four recorded magnitudes)",
      "MONO construction parameters y_p = 2.539638, y* = 2.337412, h_p = 0.647610 from the contract text"
    ],
    "measured_calibrations": [],
    "not_derived": ["kappa = 1/2", "the constitutive dynamics behind the deep law",
      "any empirical test or fit; no dataset used"]
  },
  "closure_implication": {
    "gate": "A01 CORE scale identities (identifiability of a0), feeding the measured-scale gates "
      "(kappa measurement, BTFR zero point, pre-registered a0(z) target): any determination of a0/κ from "
      "deep-regime data alone inherits the exact a0 ∝ D^(-2) sin^4 i degeneracy.",
    "implication": "For the operative thirteen-item target (filtered MONO, criterion B), the declared "
      "deep content v^4 = G a0 M_b is not invertible for a0 from a single deep plateau: the degenerate "
      "direction is the two-parameter orbit R_{lam,s} with the pinned combination v_los^4/(G sin^4 i). "
      "Same-action/parameter-domain compatibility: the statement is branch-common in the deep limit "
      "(all framework kernels have nu(y) ~ y^(-1/2)), so no branch translation is needed for the deep "
      "part; the interpolating kernels break the orbit at finite y with the recorded factors and the "
      "Newtonian regime pins D to the half power.",
    "breaking_requirements": ["knee/transition-region data (per-object)", "distance anchors "
      "(ladder, lensing, standard candles)", "distance-free probes (wide binaries, in-repo "
      "distance-free kappa measurement)"]
  },
  "child_proposals": [
    {"id": "AS013.C01",
     "title": "Distance-degeneracy breaking power of the interpolating regime (operative MONO, "
       "through the heat filter)",
     "claim": "per-object/worst-case bound on a0 inference error from knee-region data under Gaussian "
       "(lam, s, M/L) uncertainties, based on the exact break factor v'^4/v^4 = lam^2[nu(lam^2 y)/nu(y)]^2 "
       "and the MONO kernel of the operative target; population-level distance-ladder error budget for "
       "the kappa = 0.551 ± 0.043 distance-free claim to survive",
     "parent": "AS013 run AS013-20260927T224342Z-dsv4f-01 (hashes in result.json)",
     "controls": ["lam = 1 limit must give zero bias", "the bound must collapse as the knee sample "
       "approaches deep-only data"],
     "dependencies": ["FRAMEWORK_CONTRACT MONO definitions", "campaign_fresh_gravity_astra/DERIVATIONS.md "
       "sect. 2 moment machinery (pinned hashes)"],
     "duplicate_check": "no AS/MY/FGF task found with this fingerprint (manifest/INDEX/claims/catalog "
       "scanned); closest are AS1711/AS1765 (A17 redshift-space identifiability, distinct target)",
     "dispatch_state": "NOT DISPATCHED — no subagent spawn mechanism available to this worker; ready "
       "spec returned for the orchestrator per FIRST_PRINCIPLES_AND_BRANCHING.md"}
  ],
  "closure_candidate": None
  }

out = os.path.join(RD, "result.json")
with open(out, "w") as f:
    json.dump(result, f, indent=2)
print("wrote", out)
print("artifacts_sha256:", json.dumps(artifacts_sha, indent=1))
print("checks:", len(checks))
print("finished_utc:", finished)