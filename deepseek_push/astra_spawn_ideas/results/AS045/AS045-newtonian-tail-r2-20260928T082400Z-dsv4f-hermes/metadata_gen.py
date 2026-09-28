#!/usr/bin/env python3
"""Assemble AS045 result.json (schema v2) from the measured out-file + verified metadata."""
import json, hashlib, os

D = "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/astra_spawn_ideas/results/AS045/AS045-newtonian-tail-r2-20260928T082400Z-dsv4f-hermes"

def sha(p):
    return hashlib.sha256(open(os.path.join(D, p), "rb").read()).hexdigest()

out = json.load(open(os.path.join(D, "as045_newtonian_tail.out")))

artifacts = {}
for p in ["seed_as_dispatched.md", "as045_newtonian_tail.py", "as045_newtonian_tail.out",
          "as045_newtonian_tail.time", "sympy_series_check.py", "sympy_series_check.out",
          "as045_newtonian_tail_certificate.lean", "as045_newtonian_tail_certificate.lean.out",
          "derivation.md"]:
    artifacts[p] = sha(p)

result = {
    "schema_version": 2,
    "task_id": "AS045",
    "task_sha256": "2f7f4fa561e1625a234f4210e10c8bcd64a8d98f869d88b553e094f45187372f",
    "run_id": "AS045-newtonian-tail-r2-20260928T082400Z-dsv4f-hermes",
    "worker": "deepseek/deepseek-v4-flash-0731 via openrouter (Hermes subagent 'dsv4f-hermes')",
    "started_utc": "2026-09-28T08:24:00Z",
    "finished_utc": "2026-09-28T09:30:00Z",
    "execution_status": "completed",
    "outcome": "supports_scoped_claim",
    "exact_claim": ("On y = B/a0 > 0 (B = g_N > 0; both footings a0 = 9.3619e-11 and 1.1279e-10 m/s^2 "
        "enter only through y), Q, RAR, MU2, historical EXP and operative MONO each give a DISTINCT "
        "large-y (Newtonian-tail) law for nu-1, and the relative-vs-absolute split changes the ranking "
        "and even the fate: relative nu-1 ~ MONO (delta*h_p)*ln(y)/y > Q 1/(2y) > MU2 4/y^2 > RAR "
        "e^{-sqrt(y)} > EXP e^{-y}; absolute (g-B)/a0 = y*(nu-1) -> MONO +oo (logarithmic, h* + "
        "delta*h_p*ln((y+y_p)/(y*+y_p))), Q a0/2 (nonzero limit, sharp), MU2 4a0/y, RAR a0*y*e^{-sqrt y}, "
        "EXP a0*y*e^{-y} (both -> 0). Exact closed facts: y*(nu_Q-1) = 1/(sqrt(1+1/y)+1) <= 1/2 "
        "(rationalization; Lean-certified, with lower bound 1/2 - 1/(8y) for y >= 1); "
        "nu_MU2-1 = 4/(x*(x+4)) exactly, x = g/a0 (Lean-certified), hence 4/y^2 - 16/y^3 + 32/y^4 + ... "
        "and nu_MU2-1 <= 4/y^2 (Lean-certified); nu_RAR-1 = e^{-sqrt y} + e^{-2 sqrt y} + ... (series "
        "identity); EXP tail e^{-y}(1+O(y e^{-y})); MONO continuation closed form exactly "
        "h_mono(y) = h_RAR(y*) + delta*h_p*ln((y+y_p)/(y*+y_p)) for y >= y* (structural residual 0.0), "
        "with bridged landmarks y_p = 2.5396382821881653, y* = 2.3374124052663295, h_p = 0.64761024, "
        "h* = 0.64696037 > 1/2 hence nu_MONO-1 > nu_Q-1 on [y*, oo) by proof (no crossing); relative "
        "crossing Q = MU2 EXACTLY at y = 3 (x = 2 sqrt(3), nu = 2/sqrt(3); Lean-certified, RAR does not "
        "share the point), MU2 = RAR at y = 32.5349, so on the ordering window y in [50, 1e8] the strict "
        "hierarchy MONO > Q > MU2 > RAR > EXP holds (min ratio 1.3834/6.7505/1.7446/4.92e18); shared "
        "deep asymptote g^2 = a0*B (y*nu^2 -> 1 with derived corrections +y, +sqrt(y), +(3/4)sqrt(y), "
        "+(1/2)sqrt(y)) does NOT identify kernels (max pairwise |nu_a - nu_b| = 0.4999958). "
        "1%-recovery radii y_1%: MONO 73.594, Q 49.751, MU2 17.921, RAR 21.299, EXP 4.569 "
        "(r_1%/r_M = y_1%^(-1/2)). Domain: y in (0, oo) for the asymptotic statements (y -> oo, y -> 0 "
        "regimes with derived leading neglected terms), confirmed on y in [1e-10, 1e8] log grid "
        "(181 pts, dps 50); all roots and crossings bracketed, not grid-inspected. Negative controls "
        "fire: NC1 (relative-only comparison forgets B, so 'all absolute tails vanish' fails for Q "
        "at 0.5*a0 and MONO at 1.192*a0 growing) and NC2 (shared deep limit does not imply a shared "
        "kernel). All 30 regime/identity checks pass; residuals are actual (IC1 2.4e-35, IC2 2.3e-38, "
        "IC3 1.3e-51, IC4 2-3e-19, IC6 9.9e-47). Kernel-level only: no heat filter action, no field "
        "equation, no transfer to any Cassini/quadrupole verdict."),
    "framework_cell": {
        "action": "none varied here; branch-dictionary constitutive responses only (Q algebraic line, RAR, MU2, EXP comparison, MONO operative continuation); kernel-level statement only - no action variation, no filter action",
        "kernel": "nu_Q(y)=sqrt(1+1/y); nu_RAR(y)=1/(1-exp(-sqrt(y))); mu2(x)=1-(1+x/2)^-2 with mu2(x)*g=B; mu_EXP(x)=1-exp(-x); nu_mono=1+h_mono/y with h_mono = max-rule continuation (delta=0.05)",
        "filter": "not applied (kernel-level tail ordering; the operative MONO field equation uses S=exp((xi^2/2)Delta) but its action is the declared next implication, not computed here)",
        "gate": "Newtonian-tail (y -> oo) and deep (y -> 0) regime fidelity of the five kernels; requirement-1 kernel fidelity (MONO within 0.0104 dex of RAR, verified 0.0103701 at y=14.3507)",
        "coupling": "spherical radial response g = B*nu(B/a0) (Q, RAR) and implicit mu(g/a0)*g = B (MU2, EXP); no matter coupling beyond point-source baryonic field B",
        "parameters": "delta = 0.05 (adopted); kappa = 1/2 (adopted); derived landmarks y_p=2.5396382821881653, y*=2.3374124052663295, h_p=0.6476102378919149, h*=0.6469603693249751; grid k=-10..8 step 0.1",
        "scale_footing": "a0 = kappa*c*sqrt(G*rho_Lambda), kappa=1/2 adopted: canonical a0=9.3619e-11 m/s^2 (rho_Lambda=5.844412454e-27 kg/m^3), alternative 1.1279e-10 m/s^2 (rho_Lambda=8.48308962e-27 kg/m^3, ratio 1.4514872; footings share kappa, NOT density); dimensionless theorem applies to both via y=B/a0",
        "boundaries": "y = B/a0 > 0; no spatial domain (kernel-level); numerical domain [1e-10, 1e8] with bracketed roots; ordering window [50, 1e8]",
        "initial_conditions": "none (static algebraic responses)",
        "units": "SI: a0, B, g in m/s^2; rho_Lambda kg/m^3; epsilon_Lambda J/m^3; Lambda m^-2; r_M m; v_flat m/s; G=6.67430e-11, c=299792458, M_sun=1.98847e30, pc=3.085677581491367e16 (recorded; dimensionless results G-free)"
    },
    "new_assumptions": [
        "None beyond the adopted framework inputs: kappa = 1/2 (adopted, not derived - re-stated per framework contract), delta = 0.05 (amended requirement-1 value), branch-dictionary equations as inputs.",
        "Footing rule: both a0 footings use kappa = 1/2 fixed, so rho_Lambda differs by (1.1279e-10/9.3619e-11)^2 = 1.4514872; the two footings do not share both a fixed density and a fixed kappa.",
        "Cancellation-free evaluation forms (u/(1-u) for RAR, x*e^{-x}/y for EXP, x/y-1 for MU2 at dps 50) - numerical method, not physics; they equal the naive forms identically where the latter do not underflow (verified IC3/IC2b residuals).",
        "Ordering domain statement: asymptotic ranking proved from distinct leading rates; finite-window strict ordering verified on [50, 1e8] with bracketed crossings; MONO > Q proved on [y*, oo)."
    ],
    "input_sha256": {
        "deepseek_push/astra_spawn_ideas/AS045_newtonian_tail_ordering_of_the_three_kernels.md": "2f7f4fa561e1625a234f4210e10c8bcd64a8d98f869d88b553e094f45187372f",
        "deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md": "ca696c7fe7cccbe21d754eff833a4c59df6dee962ea61f50f04b5d20d80dddf9",
        "deepseek_push/astra_spawn_ideas/RESULT_CONTRACT.json": "621fdad0067c731654a0fa95eb7a4dd112f8829b96503d8d57c2ee8ca2cc1517",
        "deepseek_push/astra_spawn_ideas/FIRST_PRINCIPLES_AND_BRANCHING.md": "f633cdb4f487a16d6ad345092faabbeb1db88c6ca27a010732ba31f65f5c570f",
        "deepseek_push/astra_spawn_ideas/ORCHESTRATOR.md": "2eb07b9d1995ff2223a15219bbf7fc813be56fb69337ed4dd14d170c1dcaf671",
        "deepseek_push/astra_spawn_ideas/SOURCE_MANIFEST.json": "fe295b80bddbb0520884036ea5978d8f73174a8520f3ce0f91e2bf0f97f57fba",
        "deepseek_push/astra_spawn_ideas/manifest.json": "ca1b80071185ee3eb895ad61794c9d7a697ec0d5b96a1c07d052907e73a422a3",
        "README.md": "91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed",
        "qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md": "98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f",
        "real_research/peer_review_2026_09_26/README.md": "521d9ac36a93a27dcd6c995f78743ae9b1de4304095911871d81e6a70f9ecaac",
        "STANDING.md": "660462ebe8f98844c418e173a1dada90b9df3800c4d445fd5a0556eb9476bf63"
    },
    "artifacts_sha256": artifacts,
    "commands": [
        {"argv": "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /usr/bin/time -l python3 as045_newtonian_tail.py > as045_newtonian_tail.out 2> as045_newtonian_tail.time", "cwd": D, "exit": 0, "note": "final run; two earlier runs exited 1 during development (cancellation underflow and review corrections) - see failed_attempts"},
        {"argv": "python3 sympy_series_check.py > sympy_series_check.out 2>&1", "cwd": D, "exit": 0, "note": "symbolic closed form + series reversion cross-check"},
        {"argv": "lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/astra_spawn_ideas/results/AS045/AS045-newtonian-tail-r2-20260928T082400Z-dsv4f-hermes/as045_newtonian_tail_certificate.lean", "cwd": "/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026", "exit": 0, "note": "Lean 4.34.0-rc2, lake 5.0.0; compile host only - verified no files written into lean_2026/"}
    ],
    "execution_bounds": {
        "declared": "<=120 s wall, <=512 MB, 1 thread, grid 181 points, two refinements",
        "enforced": "RLIMIT_CPU=(120,121) set in-process (enforced); RLIMIT_AS not settable on this macOS ('current limit exceeds maximum limit') - recorded, RSS measured instead; OPENBLAS/OMP/MKL/NUMEXPR_NUM_THREADS=1 and pure-python mpmath (1 thread); actual wall 2.52 s (/usr/bin/time; script wall_s=2.5094891), peak RSS 19.9 MiB (ru_maxrss 19841024 B; /usr/bin/time 19939328 B); Lean compile 3.7 s real (bounds do not apply to the compile host)",
        "sample_bounds": "181-point log grid (k=-10..8 step 0.1) at dps 50; bisection to residual <= 2e-47 for roots; crossing bisection to ~1e-40; finite-difference derivative steps 1e-9 relative; golden-section dex scan"
    },
    "checks": out["checks"],
    "tested_domain": "y in [1e-10, 1e8] log grid (181 pts, 0.1 dex steps), mpmath dps 50; deep window y <= 1e-2 with slopes on [1e-10, 1e-4]; tail reads at y = 1e8; ordering window [50, 1e8]; EXP tail check at y in {20, 30, 40} (e^y factor cannot be evaluated at 1e8 - 4.3e7 digits); MONO ODE check at {10, 100, 1e5, 1e8}; roots (y_p, y*) and crossings bracketed (never grid inspection); no excluded points; asymptotic statements carry derived leading neglected terms and domains; no spatial domain (kernel-level).",
    "failed_attempts": [
        "as045_newtonian_tail.py first execution exited 1: ZeroDivisionError from cancellation underflow - naive 1/(1-e^{-sqrt(y)}) - 1 returns exactly 0.0 at y=1e8 (u at the 4344th digit at dps 50) and x/y - 1 for EXP cancels similarly; fixed with exact stable forms u/(1-u) and x*e^{-x}/y (identical where naive works; IC3/IC2b residuals verify equivalence). Cause recorded; no separate artifact preserved (same file evolved).",
        "Review of the first full output found two preset defects, corrected and re-run: (a) C2 expected-string used 1 - 1/(8y) + 1/(16y^2) instead of 1 - 1/(4y) + 1/(8y^2) for 2y*(nu-1) (observed value matches the corrected series exactly); (b) C11 ordering window started at y=10 while MU2/RAR cross at 32.53 - window moved to [50, 1e8] with the crossing documented; IC1/IC2 tolerances re-scaled to dps-50 rounding level.",
        "Lean elaboration iterations (exponent typing ^(-2) needs explicit : Z on this build; field_simp closing discipline - ring only where the compiler showed an unresolved ring goal; sq_eq_sq_iff_abs_eq_abs not present - replaced by mul_eq_zero product argument): resolved to zero-error compile with axioms exactly {propext, Classical.choice, Quot.sound}."
    ],
    "limitations": "Kernel-level result only: no heat-filter action, no static field equation solve, no spacetime/PPN/DOF/causality (criterion B) statement; the operative MONO's field-level health is untouched. Finite grid is confirmation, not proof - leading rates are symbolic (exact series/closed forms, Lean-certified identities); strict ordering beyond crossing points rests on distinct proven leading rates plus bracketed crossings. Q's a0/2 offset and MONO's logarithmic absolute anomaly are local statements deliberately NOT transferred to any observable (Cassini/quadrupole/wide-binary verdicts explicitly out of scope per seed). kappa = 1/2 and delta = 0.05 remain adopted inputs; y_p, y*, h_p, h* are derived. G_N/G_bare/G_cosmo not separated further (no dimensional identity needed beyond footings; both footings computed separately with kappa fixed). Spec quote 0.0104 dex reproduced as 0.0103701 at y=14.3507 (rounds to the quoted value; 3e-5 difference flagged). This run supersedes the subperseed run AS045-heatdom-r1-20260928T051523Z-dsv4f-hermes (different seed text; preserved, untouched); it is NOT the same task's evidence and does not certify the heat-filter domain results.",
    "next_unresolved_implication": "The kernel-level logarithmic absolute anomaly of the operative MONO branch (a0*(h* + delta*h_p*ln((y+y_p)/(y*+y_p)))) must be raised through the heat filter S = exp((xi^2/2)Delta) and the divergence structure to the static field equation grad^2 Phi = 4 pi G rho_b + S* div[(nu_mono-1) grad S u]: its spatial realization, finite-density cutoff and field-level Newton-recovery profile are uncomputed - the first missing bridge before any transfer to requirement-10 (Newton recovery / measured G) or any RAR<->MONO field-level transfer.",
    "suggested_followup": "AS045.C01 (ready spec in child_proposals): compute the field-level |g-B| profile of the filtered MONO equation for a compact spherical baryonic source using the filter-domain handoff (AS043 family / AS045-r1 heat-filter artifacts), locate min y_gate with |g-B|/B <= 1e-4, and report the implied 1 AU bound; discriminate against the RAR exp-tail transfer (must fail - NC1 already shows the naive inference breaks).",
    "acceptance_state": "unreviewed",
    "ancestry": None,
    "first_principles_inputs": {
        "primitive_assumptions": ["Branch-dictionary constitutive equations (Q, RAR, MU2, EXP, MONO) from the amended requirement-1/12 text and FRAMEWORK_CONTRACT dictionary (adopted inputs, not derived)", "kappa = 1/2 adopted in a0 = kappa*c*sqrt(G*rho_Lambda)", "delta = 0.05 adopted (amended requirement-1)", "y = B/a0 > 0, x = g/a0, B = g_N > 0 definitions", "domain y in (0, oo)"],
        "measured_calibrations": ["G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI; used only in footings)", "a0 canonical 9.3619e-11 and alternative 1.1279e-10 m/s^2 (framework footings)"],
        "derived_equations": ["nu_Q(y) = sqrt(1+1/y) from g^2 = B^2 + a0 B", "nu-1 binomial and rationalized forms with two-sided bounds (Lean-certified)", "nu_RAR-1 = e^{-sqrt y}/(1-e^{-sqrt y}) series identity", "nu_MU2-1 = 4/(x(x+4)) exact closed form (Lean-certified) and 4/y^2 - 16/y^3 + ... tail", "MONO continuation h_mono closed form on y >= y*, landmarks y_p, y*, h_p, h* (bracketed roots of stated equations)", "EXP tail e^{-y} form", "rankings, exact crossing y = 3, footings densities/anomalies", "all with units and leading neglected terms"],
        "boundary_initial_data": "none (static algebraic responses; numerical bracket endpoints are method, not physics)"
    },
    "closure_implication": {
        "gate": "Requirement 1 (operative filtered MONO kernel fidelity) -> Requirement 10 (Newton recovery / measured G): kernel-level implication - any same-action candidate carrying the operative MONO continuation carries absolute anomaly a0*(h* + delta*h_p*ln((y+y_p)/(y*+y_p))) unbounded in y = B/a0, i.e. the MONO phantom does not vanish in the strong-field interior (vs RAR's e^{-sqrt y}); conversely Q (a0/2 offset) and MU2 (4a0/y) are also mutually distinct. Exact implication: Newtonian-recovery bounds for MONO cannot be certified from RAR/EXP tail decay; the missing bridge is the field-level S-action (next_unresolved_implication). Parameter-cell compatibility: dimensionless result valid for both footings by y = B/a0; kappa = 1/2 in both (rho_Lambda differs); no other cell change needed.",
        "status": "conditionally supported (kernel-level component of requirement-1 fidelity; field-level gates open)"
    },
    "child_proposals": [
        {"id": "AS045.C01", "title": "Newton-recovery gate for operative MONO through the heat filter", "fingerprint": "(source: FRAMEWORK_CONTRACT/FRIED_CHICKEN_SPEC amended req-1 text + this result; branch: MONO operative; kernel: nu_mono; filter: S=exp((xi^2/2)Delta); gate: req-10 Newton recovery; target: min y_gate with |g-B|/B <= 1e-4 for compact spherical baryonic source + implied 1 AU bound)", "why_not_answered_here": "kernel-level y*(nu-1) = h* + delta*h_p*ln(...) has no spatial realization; S-action and divergence structure untouched in AS045", "controls": "cancellation-free numerics at dps 50; filter-domain handoff (adjoint conventions from AS043/AS045-r1); negative control: transfer RAR exp-tail to MONO recovery must fail", "dependencies": "S-domain result (AS043 family; AS045-heatdom-r1 artifacts as handoff), this result's closed forms", "dispatch_state": "spec_only - not dispatched (no runner available in this subagent session)"},
        {"id": "AS045.C02", "title": "MONO tail vs requirement-10 measured-G gate (EPE-multipole, no local-transfer shortcut)", "fingerprint": "(source: this result + seed warning; branch: MONO operative field equation; gate: req-10 Solar-System precision; target: first non-Newtonian multipole of the filtered MONO equation, not the Q-branch estimate, vs committed gates)", "why_not_answered_here": "seed explicitly forbids transferring a local acceleration estimate into a Cassini quadrupole verdict; AS045.C01 is a prerequisite", "controls": "matched forward solve vs committed quadrupole at xi -> 0 (repository f26 conventions); signed chargebook of the log tail", "dependencies": "AS045.C01", "dispatch_state": "spec_only - not dispatched"}
    ],
    "closure_candidate": None
}

with open(os.path.join(D, "result.json"), "w") as f:
    json.dump(result, f, indent=1)
print("written; artifacts:")
for k, v in artifacts.items():
    print(" ", v, k)