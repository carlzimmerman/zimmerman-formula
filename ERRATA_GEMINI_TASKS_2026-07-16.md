# ERRATA: Gemini Task Commits (2026-07) — What Was Wrong and How We Caught It

**Date:** 2026-07-16
**Scope:** commits `18ebf8a4` (Task 1), `9e85df27` (Task 5), `ed8cc487` (Task 6), `b1ffd4df` (Task 2), `e37c7144` (Task 3) — a batch of task scripts contributed by a Gemini agent session.

This project's standing rule is that every load-bearing claim must be backed by a
runnable, committed script **and survive adversarial re-verification**. The Gemini
task batch was audited under that rule on 2026-07-14 → 2026-07-16. Transparency
beats clean history: the commits are left in place, and this document is the
correction of record.

## Task 6 (`ed8cc487`) — BCG Deep-Core RAR "resolution": **JUNK, withdrawn**

`bcg_environmental_a0_scaling.py` claims environmental a₀ scaling yields "exactly
the missing cluster mass without dark matter." The script **hard-codes the
answer**: `a0_bcg = 17.0 * a0_canonical` — the ×17 is inserted, not derived, so the
"exact match" is circular. The conclusion is withdrawn in full. (The honest
standing of the cluster front is recorded in
`real_research/reviews/cluster_rar_throttle_2026/` and the banked cluster ledger:
a real, shared-MOND, ceiling-bounded deficit — no environmental-a₀ cure. The
local-density-a₀ route was independently and *structurally* closed on 2026-06-14.)

## Task 5 (`9e85df27`) — DESI DR2 + JWST evolving-BTFR forecast: **JUNK, superseded**

`desi_jwst_btfr_forecast.py` carries an **E(z) footing bug**: it conflates the
ρ_DE-based a₀(z) (canonical footing) with a cH(z)E(z) scaling in the same
forecast, producing evolution curves that belong to neither footing. Superseded by
`prep_2026/btfr_forecast_audit/btfr_forecast_check.py` (footing-locked, both
footings run separately) and by the full high-z TFR fork confrontation
(`prep_2026/highz_tfr_fork/`, 2026-07-16), whose verified verdict is
WASH/UNDERPOWERED with the fork ΛCDM-degenerate at every in-hand redshift.

## Task 2 (`b1ffd4df`) — Cluster throttle lensing mock: **code kept, headline claim withdrawn**

`cluster_throttle_lensing_mock.py` is sound as a mock of the y_c = Z/2 kink
location. However its implicit "Euclid should target this" framing is **withdrawn**:
(i) the mock used a₀ = 1.2×10⁻¹⁰ — neither framework footing — and a standard-MOND
ν rather than the framework's ν = √(1+1/y); (ii) the 2026-07-16 pre-registration
(`prep_2026/cluster_kink_spec/PREREGISTRATION_EUCLID_NULL.md`) shows Euclid's
cluster weak-lensing fits run over 0.4–4.0 Mpc with the <100 kpc core excluded,
while the kink sits at 8–23 kpc — **17–50× below the fit floor, structurally
unobservable by Euclid WL at any stacking depth**. The kink remains a real,
footing-independent framework prediction; the near-term-testability claim does not.

## Task 3 (`e37c7144`) — One-loop TT vertex decoupling "at all orders n": **downgraded to n = 1, 2**

`mi_oneloop_tt_vertex_all_n.py` prints an all-orders argument but **both of its
`check()` calls are hard-coded `True`** (lines 56, 66) — it is a narrated argument,
not a CAS proof. The banked status is: TT-vertex-zero **CAS-verified at n = 1, 2
only** (`real_research/reviews/mi_formal_completion_2026/oneloop_laneB_mixing.py`);
the all-orders statement was later established by different means in the
2026-07-16 arc (see `prep_2026/oneloop_finite/`). Lesson enforced since: no
hard-coded booleans in check functions, verified by grep in every subsequent
workflow.

## Task 1 (`18ebf8a4`) — SPARC footing conflation test: **sound, kept**

Reproduced under audit; consistent with the banked footing-conflation ledger
(the ~20% a₀ shift is non-diagnostic on the SPARC RAR, Δχ² ≈ −1.14%).

---

*The corrections above were found by adversarial verification lanes (2026-07-14
"where did Gemini land" audit; 2026-07-16 D2 pre-registration and one-loop
salvage runs). Every replacement result cited here is itself backed by exit-0
scripts in this repository.*
