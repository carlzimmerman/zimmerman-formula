# Foundation programme: charter and standards (DRAFT v0.1, 2026-10-08)

Status: **draft for the owner's approval.** Nothing in `foundation/` is built until this charter is approved. It supersedes `a0kit/`, which uses the retired kernel √(1+1/y) and a retired motivation.

## 0. Purpose
Rebuild the programme's core so that every published claim can be reproduced from one clean checkout, by one command, by someone outside the programme. The legacy record stays as history: `campaign_fresh_gravity/` and the other lane folders are not edited. Legacy results enter the foundation only by passing the migration rule in §9.

## 1. One source of truth for the framework (`foundation/framework/`)
A single versioned module defines:
- the law: a₀ = κ c √(G ρ_Λ), with κ = ½ **fitted**;
- the kernel ν_mono(y) = 1/(1 − e^(−√y));
- the two footings, which are never pooled;
- a₀(z) for flat and dark-energy-tracking a₀;
- the phantom;
- candidate B's switch;
- the cold-fluid rule (the mass-conserving edge and the turnaround catchment).

Every number has a docstring citing where it comes from. Tests import these definitions and never re-type a constant.

**Change control:**
- A change to any definition bumps the framework version (`FRAMEWORK_VERSION`) and needs a dated entry in `CHANGELOG.md` with the reason.
- It needs the owner's explicit approval.
- Every test re-runs after a change, and the board shows which version produced each verdict.

## 2. Data with provenance (`foundation/data/`)
`DATA_REGISTRY.yaml` has one entry per dataset:
- source (paper, catalogue, DOI or URL) and access date;
- SHA-256 of the raw file;
- licence and units;
- the exact cuts, with the reason for each;
- the inherited assumptions, by ID (§3).

Raw data lives outside git, in `../_external_data/foundation/`. Loaders verify the checksum before use. Downloads need the owner's go, and every fetch is logged with no home paths.

## 3. Assumption register (`foundation/ASSUMPTIONS.md`)
Every assumption inherited from other scientists' work gets an ID (A01, A02, …) with:
- what it is, and where it enters;
- the direction it could bias a test of this framework;
- a framework-native alternative, where one exists.

Examples: hydrostatic equilibrium with constant bias; NFW or ΛCDM halo templates; ΛCDM-calibrated stellar M/L; star-formation-law gas masses; ΛCDM turnaround overdensity and initial power spectrum; ΛCDM-defined lens isolation; void-finder bias; Jeans equilibrium.

**Rule:** a verdict counts only if it survives the framework-native alternative, or if the dependence is stated on the board.

## 4. Tests (`foundation/tests/<ID>/`)
Each test has:
- `PREREG.md`: the question, the scope tag, the data, the statistic, the pass/fail rule, the tolerances and the controls. It is committed and its hash recorded **before** any data are touched by the test code.
- `run.py`: imports only `foundation.framework` and `foundation.data`, and writes `result.json` to a fixed schema.
- A **broken control (MUTATE)** that must flip the verdict. If it doesn't, the test is void.
- Both footings, reported separately.

The **scope tag** says what the test covers:
- **B:** candidate B (the switch plus the cold fluid);
- **CHASSIS:** the ungated relativistic chassis;
- **READING:** a named alternative reading.

A result never moves between scopes.

**Blinding where possible:** the analysis is fixed on mocks or a held-out half before it sees the real statistic.

## 5. Verification tiers (shown on every board tile)
- **T0 Draft:** the script exists.
- **T1 Reproduced:** it re-runs from a clean checkout with a pinned environment and matches to the stated tolerance.
- **T2 Replicated:** an independent implementation (a different agent or person, not shown the first code) gets the same verdict.
- **T3 External:** an outside scientist has checked it.

Headline claims (papers, the board's PASS tiles) need **T2**.

## 6. Claims policy
- The wording allowed depends on the tier:
  - T0/T1: "preliminary";
  - T2: "replicated";
  - T3: "independently verified".
- "Solved", "closed" and "final theory" are never used. κ is always written as fitted. No dark-matter particle is claimed. The cold fluid's mass is always stated as required.
- Corrections go forward: errata and `RETRACTIONS.md` entries are added and git history is never rewritten.

## 7. Reproducibility
- The environment is pinned (`foundation/environment.lock`).
- Random seeds are stored in `result.json`.
- `make board` runs every test at its declared tier and regenerates the status board and a results table from `result.json` files only. The board is never hand-edited.
- Heavy simulations declare their compute and cache outputs, with checksums, outside git.

## 8. Roles and separation of duties
- **Owner:** approves the charter, framework changes, downloads, deposits and outreach.
- **Builder** (the orchestrating session): writes tests and code.
- **Auditor:** a separate session that never audits its own code. It runs T1, checks data against the registry, and checks scope.
- **Replicator:** a separate session that writes T2 implementations without seeing the builder's code.
- **External:** outside scientists, for T3.

## 9. Migration of legacy results
A legacy lane's result enters the foundation only if the new test, written from scratch on the foundation modules, reproduces it within its stated tolerance, or if the difference is explained and recorded. The first build covers the essential tests, in this order:
1. **F01** Rotation curves (SPARC RAR) and κ, on both footings.
2. **F02** Local a₀ from MeerKAT.
3. **F03** Weak lensing (KiDS-1000), with the two-halo term stated.
4. **F04** Clusters and the Bullet Cluster (needs the cold mass), with the hydrostatic assumption stated.
5. **F05** Structure growth with the zero-knob rule (PM).
6. **F06** Milky Way satellites and ultra-faint dwarfs.
7. **F07** Andromeda and Local Volume dwarfs.
8. **F08** Local gravity (Solar System, Cassini, binary pulsars).
9. **F09** a₀(z) from public high-z discs (calibration wall stated).
10. **F10** Gaia DR4 wide binaries (the frozen pre-registration, imported unchanged).
11. **F11** Void lensing (reservoir smoothness).
12. **F12** The cold-fluid settling requirement (a theory test of what a mechanism must do).

## 10. Inputs to this draft (pending)
- The data and assumptions audit of the 10-07/08 lanes (`campaign_fresh_gravity/AUDIT_data_and_assumptions_2026-10-08/`).
- The failure-mechanism ledger (`campaign_fresh_gravity/LEDGER_failure_mechanisms_2026-10-08/`).

Their findings will be folded into §3 and §9 before v1.0.
