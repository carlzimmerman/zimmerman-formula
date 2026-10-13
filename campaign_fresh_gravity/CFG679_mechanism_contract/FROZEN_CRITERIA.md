# CFG679 — the mechanism contract (frozen criteria, committed alone)

Block CFG670–679. Written 2026-10-12, after CFG678 (no candidate passes the one-action contract) and before any candidate
mechanism is written down or scored. Nothing below was computed for this file.

κ = ½ is fitted. Both footings (9.36e-11, 1.13e-10 m/s²), never pooled. The cold energy's mass is required. No dark-matter
particle may be added. Not theory closed.

## What this contract asks for

The missing physics is a **dynamical mechanism** that (i) moves the cold mass into the law's profile, (ii) accounts for the
energy and momentum it exchanges, and (iii) predicts gravity and lensing consistently on one metric. The acceleration relation
does not supply this. CFG660 shows the law is a static equilibrium of a field-aligned stress, and that stress has no well-posed
dynamics (S5). CFG638 shows the record's settling equations copy ρ_ph from the law. They set timing, not the end state.

This file freezes what a candidate mechanism must do. It extends CFG678 (gates B1, B3/A2, C3, D2) and the selector
specification S1–S9 (`MECHANISM_JOINT_2026-10-12.md` §6). It does not replace either.

## Rules

- **R0. No target in.** The candidate's equations may not contain ρ_ph, ν, F(g_N), σ⁴ = G M_b a₀/4, or any quantity computed
  from the law. The law's profile and the per-system deep temperature must be **outputs**. A candidate that uses one of them as
  an input scores FAIL on M1, whatever else it does.
- **R1. Constants.** Allowed: G, c, a₀ (or ρ_DE), and the baryons. At most **one** new constant. It must be declared in the
  candidate's own criteria file before any number, and held fixed across every system and gate. No per-system constant.
- **R2. No new thresholds.** Every PASS line below is its source lane's frozen line. The single exception is M1b, a physical
  bound labelled as such.
- **R3. One action.** Each gate counts only if its behaviour follows from varying one action, as in CFG678's rule. A prescribed
  mask, a hand-placed edge or a by-hand tie scores UNTESTED, never PASS.
- **Statuses:** PASS / FAIL / CONDITIONAL (passes under a stated, unproved premise) / UNTESTED / PENDING (data not yet released
  or lane not yet run) / DECLARED.
- **Scoring is separate.** Each candidate is scored in its own lane, with its own criteria file pointing here, committed before
  that candidate's scripts. No candidate is named in this file.

## Gates

### M. The three requirements
| id | gate | PASS line (source) |
|---|---|---|
| M1a | **Profile is an attractor.** Hernquist baryons a/r_M ∈ {0.05, 0.3, 1, 3, 10} (CFG660 N1 set). From each of three declared non-law initial states (uniform; Plummer; ρ ∝ r⁻² at half and at twice the law's amplitude), the evolved end state, run through the CFG4 SPARC harness, keeps the law's fit. | CFG4 frozen line: weighted rms ≤ 0.110 dex on **both** footings, separately for each initial state (CFG678 C2) |
| M1b | **Settles in time.** The settled state is reached at the outermost measured SPARC radius within the age of the universe. | physical bound, t_settle ≤ 13.8 Gyr (not from a lane; declared here) |
| M1c | **Well-posed.** Local WKB at CFG660's deep point (g = 0.1 a₀): growth bounded in k. | CFG660 S5 test: no Im ω ∝ √k at k = 10 / 10³ / 10⁵ |
| M2a | **Momentum ledger.** ∇_μ T^μν_total = 0 holds as an identity of the action (sympy). No unbalanced reaction on the baryons. | CFG48 Noether identity: the reaction term that is 0.55–2.2 × baryon weight for the prescribed gate must be exactly balanced (residual 0 symbolically) |
| M2b | **Energy ledger.** The energy settling exports, and imports when reheating, goes to and from a **named reservoir that is a field of the same action**. Both signs are allowed. | CFG541/542/544: export 0.1–0.35 V_f² per unit mass reproduced, with sign; the reservoir appears in the conservation identity of M2a |
| M3a | **Lenses like mass.** On the CFG663 primary (KiDS-1000 blue isolated lenses + SPARC overlap), the candidate is class H-L, not H-NL. | CFG663 frozen classes, with the candidate's own lensing response in place of H-NL: PASS iff Δ ≤ 0.01 dex (CONSISTENT) on both footings; FAIL iff Δ ≥ 0.05 dex and ≥ 95% of draws give Δ ≥ 0.03; TENSION otherwise (not a pass) |
| M3b | **One metric; GW at c.** No sector that bends light but not gravitons. | CFG670 Lean no-go (every direction); c_T = 1 |
| M3c | **Solar System.** | G01/G02 Cassini line |

### S. The selector specification (each row of MECHANISM_JOINT §6, scored as written there)
S1 carries c · S2 own enclosed baryons, EFE-blind · S3 nonlocal · S4 real gravitating mass · S5 the law's interpolation,
Solar-System-silent · S6 not thermal · S7 two-sign energy exchange (= M2b) · S8 slow in mergers (PENDING on CFG639/CFG641) ·
S9 none of the closed agents.

### D. Data gates the current law plus switch fails (CFG678: any new action must change these)
| id | gate | PASS line (source) |
|---|---|---|
| C3 | massive early types at 50–100 kpc, raw KiDS isolated lenses | CFG529 frozen line (Edge PASS iff Δ ≤ 4 and p > 0.01), both footings |
| D2 | structure growth against raw KiDS-1000 | CFG596 frozen classes: CONSISTENT (Δχ² < 4 and robustness max < 9) on both footings |
| D3 | a₀(z) flat, not ∝ H(z) | CFG570/571 sealed predictions; PENDING until 2026-11-06 / 2026-11-28 |

## Verdict

- **MECHANISM PASSES** iff every M gate, every S row except S8 (which may be PENDING), C3 and D2 pass on both footings.
- **MECHANISM WITHOUT DATA** iff all M and S rows pass and C3 or D2 fails. This is a consistent mechanism for the law, which
  inherits the law's data failures. It is reported as such, never as a pass.
- **FAIL** otherwise, listing every failed gate.

## Controls (the contract must be able to fail things; scored in the first scoring lane, before any candidate)
- **K1 (must FAIL R0/M1):** the record's class-A settling (CFG541–554 as written in CFG638). It relaxes toward ρ_ph copied from
  the law.
- **K2 (must FAIL M1a):** GR + Λ with no cold-energy sector. Newton rms 0.2755 dex > 0.110 (CFG678 MUTATE).
- **K3 (must FAIL M3a):** a response that acts on matter but does not lens, for example astra's conformally coupled stiff
  polarization sector (CFG663 reading 1). Excluded at +0.155 / +0.158 dex.
- **K4 (must FAIL M1c):** CFG660's field-aligned stress with an independent density (ill-posed, √k growth).

If any control fails to fail, the contract has no teeth and must be fixed, forward, in a new dated file.
