# LOOP_CONDUCTOR — the zimmerman-formula autonomous research loop

**2026-09-23 · swarm constitution · any Hermes session (interactive, delegated, or
scheduled) that runs a wave of research on this repo MUST operate under these rules.
This file is the single source of truth for loop behavior; extend it, never fork it.**

## 1. Purpose

Indefinite, self-sustaining continuation of the programme (memory: "swarm ops —
each landed wave spawns successor lanes; never rehash ruled-out doors"). The loop
is: LAND → VERIFY → REGISTER → SPAWN. Every wave must be grounded in machine
checks (exit codes, SEs, KS tests, Lean compile + zero-sorry) and in real
empirical evidence where data exists; every algebraic claim worth keeping must be
Lean-certifiable (repo toolchain: `fable_independent_2026/lean_2026`, v4.34.0-rc2).

## 2. House rules (non-negotiable)

1. **Append-only.** Never delete or rewrite files; superseded work stays in
   history, corrected by new commits on top. Fix forward.
2. **No fabrication.** Every number in a verdict must exist in a file or a
   command's output. A number "remembered" but not on disk does not exist; if a
   value is needed, re-derive it. Fabrication = kill the lane.
3. **Honest FAILs preserved verbatim.** A failing check is a result. Never tune
   constants or budgets to make a check pass; widen a budget only by measuring
   the estimator's true SE (subsample/Jackknife), and record the change.
4. **No circular reasoning, no theatre.** Claims that restate the engine's own
   sampling rules (Gaussian-kick hierarchy, Poisson atom at central source) must
   be labeled consistency-family, never promoted as discovery. The K01 audit's
   A/B/C classification is the standard: A = model-input restatement (label-only),
   B = genuine joint-law statement, C = observer-falsifiable.
5. **Pre-registered kill conditions.** Each lane states its kill thresholds
   BEFORE reporting numbers, and honors them.
6. **Raw data stays untracked** (GitHub 2 GiB pack / 100 MB blob limit; house
   style cf. G114_data, G236_eRASS3_data). Commit work + math only.
7. **No lane touches another lane's files.** Files are claimed by prefix
   (J-series, K-series, L-series, M-series, G-series, I-series) + name.
8. **Do not collide with the live lab** (`ai_slop/autoresearch_v3/`, seed
   Qb07e5686) or the orchestrator's frozen targets, unless the task says so.
   Do not modify `STANDING.md`; nothing outranks it. New statements go in
   `deepseek_push/`.
9. **No git commits by leaf lanes.** The conductor (or the user's explicit
   instruction) commits; commit messages reference the lane series and file set.
10. **Dedup.** Before spawning a lane, check the register (§3) and running lanes
    (`ps aux | grep python3` + delegate list); never spawn a door already
    launched, closing, or ruled out.

## 3. The register

`deepseek_push/CANDIDATE_LAWS_REGISTER.md` (current: M04 lane in flight) is the
living index. Each row: law/claim · status (PROVEN/MEASURED/KILLED/OPEN/LABEL-ONLY)
· verification file · kill condition · Lean status · who owns it. Every loop
tick must update it (append-don't-rewrite rows where possible). The K01 audit is
the standing referee precedent: six GO items (closure failure R, volume Dynkin
compensation, R_m growth, E[D²] bound, volume taboo, spectral envelopes) plus the
J09p/J10/J11 laws verified later.

## 4. Wave discipline

- 3–7 lanes per wave; each lane owns (prefix)_(topic).py/.out/.json/.md in
  `deepseek_push/`, exits 0 only on real passes, reports honestly otherwise.
- Lane briefs must carry: context (surviving numbers with file refs), goal,
  kill conditions pre-registered, house rules 1–10, deliverable list.
- A wave is not landed until every lane's verdict is on disk AND the register is
  updated AND (for the user) a digest of what survived/what died is reported.

## 5. Loop tick procedure (for the scheduled job)

1. `git status --short deepseek_push/` — find new uncommitted verdict files.
2. For each completed lane set: read verdict(s), check exit code and the JSON,
   append to the register, and — with the user's explicit push authorization
   pattern — commit work+math (never data, never other series).
3. Check the schedule's wave balance: if < 6 lanes running and ≥ 1 open door in
   the register, spawn the next wave (3–7 lanes) on OPEN doors only.
4. Report a terse digest: landed / died / spawned / open.
5. Never spawn a lane that rehashes a KILLED or ruled-out door: consult the
   register's KILLED column and the wave history in it.

## 6. Current campaign state (epoch 2026-09-23)

- Closed: J01–J11 (moment channel; J09 27/27, J09p 21/21, J10 6/6, J11 8/8),
  K01–K06 (audit + three motors + inversion + ray solver + methods), N05 audit,
  I21/I22/I23/I24 Lean certs, G236/G237 (eRASS:3 released/derived), L-series
  wave-4 in flight, K07–K12 wave-3 in flight, M-series wave-5 (register + Lean
  roadmap) in flight.
- Open doors (as of this epoch): the L/K wave verdicts themselves (synthesis),
  the Q-functional closure, the J10-I(z) a0-cosmography port, the M-roads
  Lean roadmap, G237 verdicts pending eRASS:3 WG products, the JWST
  observation design (L05/K09), the RAR moment-discipline transfer (L06).

_End of constitution. Sessions executing under it: read this file first._