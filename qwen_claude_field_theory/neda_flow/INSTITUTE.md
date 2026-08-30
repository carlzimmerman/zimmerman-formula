# THE NEDA INSTITUTE — autonomous search for a relativistic completion of the a₀ framework
*A standing research institute run by machines, audited by humans. Mission: certify OR exhaust a viable
relativistic field theory reproducing μ(y)=1−e^{−y}, a₀=κc√(Gρ_Λ)=9.36e-11, correct MOND lensing,
c_T=1, ghost-free — or map the impossibility with theorem-grade rigor.*

## Divisions (each a code module or state store — one institute, defined roles)
| Division | Charter | Implemented in |
|---|---|---|
| **Proposal & Generation** | propose candidate architectures | `runner.py` (Architect via `ollama_client.py`) |
| **Aleatoric Lab** | novelty beyond the literature prior (seeded PRNG over the grammar) | `mutation_engine.py` |
| **Gate Review Board** | deterministic, pre-verified judges; the authority | `evaluator.py`, `gate_templates.py` |
| **Theory Registry** | permanent IDs, canonical fingerprints, genealogy, dead classes | `candidate_manager.py`, `state/` |
| **Coverage Office** | exhaustive class-level map of the theory space | `../aella_flow/` |
| **Archive / Lab Notebook** | append-only record of every candidate & verdict | `database/*.jsonl` |
| **Escalation & External Review** | survivors → hostile human/Claude audit (the A–P ladder) | `escalation/` |
| **Standards & Reward** | the falsification battery = the measured universe + frozen recipe | `state/FALSIFICATION_BATTERY.json` |
| **Integrity Board** | research-conduct rules; blocks manufactured results | `institute/INTEGRITY_BOARD.md` |
| **Scientific Charter** | the immutable law (CRISPY FRIED CHICKEN RECIPE) | `global_protocol.md` |
| **Director's Log** | live research frontier / status board | `institute/DIRECTORS_LOG.md` (auto) |

## How the institute runs (one command; needs no human, no tokens)
    ollama serve &                 # optional: enables the Architect (Qwen) division
    python3 runner.py              # the persistent loop; Ctrl+C = clean stop, state survives
    python3 ../aella_flow/sweep.py # Coverage Office: re-map the space (seconds) after new theorems
Results self-commit LOCALLY every 50 dispositions (never pushed — humans control the remote).

## The research pipeline (a candidate's life)
proposal (Architect|Aleatoric) → canonicalize + fingerprint (Registry) → dedup vs dead classes →
G0 structural + P-rules → trusted templates G1–G3 → theorem gates G4/G5/G6/G8 → survivor? →
Escalation Desk → hostile human/Claude audit (A–P ladder) → verdict → **generalize failure to a
dead-class theorem** → Coverage Office re-maps → space shrinks. See `institute/PIPELINE.md`.

## Onboarding a new researcher (human or AI): read `institute/ONBOARDING.md`.
