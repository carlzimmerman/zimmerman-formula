"""Runtime settings. Imports never start model calls or services."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CONFIG = {
    "root": ROOT, "runtime": ROOT/"runtime_v2", "contracts": ROOT/"contracts",
    "worker": {
        "base_url": os.environ.get("OLLAMA_URL", "http://localhost:11434"),
        "model": os.environ.get("WORKER_MODEL", "qwen3.8:27b-mlx"),
        "timeout_s": 180, "max_tokens": 4096,
    },
    "referee": {
        "enabled": os.environ.get("ORCH_REMOTE_REFEREE", "0") == "1",
        "base_url": os.environ.get("ORCH_API_URL", "https://openrouter.ai/api/v1"),
        "model": os.environ.get("AGG_MODEL", "deepseek/deepseek-chat"),
        "api_key_env": "OPENROUTER_API_KEY",
        "budget_usd": float(os.environ.get("ORCH_BUDGET_USD", "20")),
        "reserve_per_call_usd": float(os.environ.get("ORCH_CALL_RESERVE_USD", "0.10")),
        # Estimates only: configure current provider prices before enabling calls.
        "price_in_per_mtok": 0.30, "price_out_per_mtok": 1.10,
        "timeout_s": 180, "max_tokens": 4096,
    },
    "doors": {"max_depth": 4, "repair_attempts": 2},
    # Four routes cross the three role phases instead of permanently pairing a
    # role with one route. These are research questions, never established facts.
    "research_routes": {
        "kappa-normalization": [
            {"id":"mixed-symmetry", "question":
             "Propose one explicit particle-free interaction or symmetry transformation mixing the vacuum and response operators. Derive its coefficient constraint by variation, then test whether lambda=1 and lambda=2 satisfy it. Label a changed action explicitly. Do not insert the desired coefficient, kappa=1/count, or unit channel slope as a premise. A precise failed selector is useful only if this mechanism has not already been tested."},
            {"id":"physical-spectral-measure", "question":
             "Starting from an explicit classical field operator or energy functional, derive a response spectral measure and compute its infrared weight in independently fixed s units. Test whether its normalization actually fixes the infrared weight or leaves a coupling free. Do not choose f(nu)=exp(-nu) just because it has f(0)=1. Target one derivable relation, not the whole theory."},
            {"id":"nonlinear-vacuum-coupling", "question":
             "Test a specified nonzero-gradient background or mixed vacuum-response condition that could constrain the cubic response coefficient. The homogeneous vacuum and quadratic jet alone leave this coefficient free. Derive the new condition from the specified action, compute the actual response, and test both weights without rescaling s or fitting a0."},
            {"id":"selector-countermodel", "question":
             "Take a genuinely new selector from recent attempts and construct its smallest admissible counterexample or establish its exact limited lemma. Explicitly check all of that selector's hypotheses. Merely substituting lambda=2 into kappa=1/(2 lambda), or repeating the existing static no-go, is not a new test. The static action/shape obstruction is documented in real_research/reviews/kappa_selection_2026_09_21/README.md; identify what additional physics your test probes."},
        ],
        "common-action-consistency": [
            {"id":"constraint-rank", "question":
             "Choose one explicit particle-free action and derive its lapse/auxiliary constraints and kinetic Hessian in a specified background. Test the constraint rank and physical sign under one controlled deformation. A nonzero determinant or a coefficient named healthy is not a derivation; show the eliminated and retained variables."},
            {"id":"background-to-growth", "question":
             "Derive one background equation and one linear perturbation coefficient from the SAME explicit action and normalization. Test their compatibility and conservation identity. Do not combine equations from different candidate actions or silently supply a dust particle component."},
            {"id":"local-to-cosmological-bridge", "question":
             "Compute a shared coupling in the static sourced limit and in a cosmological perturbation limit of one specified action. Test whether the two calculations actually constrain the same parameter, with dimensions and field normalizations explicit. Restrict the hypothesis to the precise bridge calculated."},
            {"id":"finite-background-health", "question":
             "Test a previously unexamined finite-gradient background of an explicit candidate action. Derive the principal or constraint operator and find a sign/degeneracy condition using real algebra. Distinguish static ellipticity from time-dependent stability and use the same physical criterion in the controls."},
        ],
        "cluster-source-closure": [
            {"id":"xcop-radial-residual", "question":
             "Use actual X-COP fgas/hydro/mstar files from the input catalogue to compute one cluster's radial residual with uncertainties and a named gravity kernel. Compare both a0 footings 9.3619e-11 and 1.1279e-10 in SI. Explain the new question beyond the existing C02 analysis. Never invent a gas fraction, derive a constant ratio from one mass, or present assumed parameters as measurements."},
            {"id":"active-source-accounting", "question":
             "Derive an active gravitational source from one explicit stress tensor and integrate it for a specified profile. Test conservation and whether adding its force double-counts a response already present in the modified field equation. State the exact limited hypothesis; use a genuine perturbation of the computation for controls."},
            {"id":"boundary-truncation", "question":
             "Propose an explicit boundary or matching condition for a finite field-generated cluster source, and test mass continuity and flux conservation across it. Derive the edge from that condition instead of selecting it to match an observed mass. Identify any surviving free parameter."},
            {"id":"force-lensing-consistency", "question":
             "From the same action or explicitly stated pair of metric equations, derive dynamical and lensing responses to a fixed baryonic source. Test whether one mechanism can supply both without changing normalizations. Reading a dataset or comparing a definition with itself is not a test of this relation."},
        ],
    },
    "lean_project": ROOT.parent.parent/"fable_independent_2026/lean_2026",
}
