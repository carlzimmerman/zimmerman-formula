# CLOSURE_MAP — which outcomes close, which stay open (2026-09-17, swing 13)

> **STATUS BOX.** This is a map of which constructions die on which gates — not a finished
> theory and not a law of nature. Every cell cites a landed artifact (file, check, number).
> The words derived/closed/breakthrough are not used as claims; "KILLED" means the
> pre-registered kill condition fired in the cited check.

## 1. The constructions — KILLED (the record, not slogans)

| construction | kill gate | evidence (file, check, number) |
|---|---|---|
| Helmholtz projector | Oort deep response | `SW02_helmholtz_kill.out` A: 130.3x / 143.1x, Cassini-safe |
| Local 2-jet / mu(\|g\|) trigger | the obstruction | `SW10_pair.out` 10/10 (jets 0.00e+00, Gamma moves 1.2x); Lean `SW10_pair.lean` exit 0 |
| Every priced eta_c mechanism | window mismatch | `SW07_eta_c_attack.out` 1/6; tidal/self 1.66e-05, 4 orders below window |
| Photon/graviton metric split | GW170817 dShapiro | `kappa_slot_2026/SW06_lensing_trilemma_quadrature.out` 1a/1b/1c/2a: >= 1e5x the 1.7 s; G11 |
| Smoothed-total-switch action | PPN alpha_1 | `kappa_slot_2026/SW04_ppn_full.out`: alpha1~ = -1.4..-2.1, 1e4-2e4x bound; l-scan no window |
| AeST | Cassini | stop-defending list; Cassini ~15-25 sigma (`PAPER_DELTA.md`) |
| Emergent LCDM | gas dwarfs | L266: 2.24x scatter |
| June CPL bridge | RETRACTED | `RETRACTIONS.md` (owner withdrawal) |

## 2. The constructions — STANDING (rivals included, honestly)

| construction | standing evidence | Lean | DR4 gamma_v band |
|---|---|---|---|
| **Gamma/eta conformal class (this lane)** | SW01b 18/18, SW04 13/13, SW05 9/9, SW06 8/8, SW09 11/11, SW10 10/10, chain 9/9 | 18 theorems (own), exit 0, zero sorry | **1.0000–1.01012** (`SW04_conformal_efe.out` D) |
| **xi-screened covariant candidate** (fable FINAL_THEORY_CANDIDATE / L223) | SW07 ledger Arm B; L47 xi >= 4 pc screens the pair | single-metric, screened | 1.000 + O(1e-4), **ceiling 1.045** |
| **L268 magnitude-only / cap law** (fable rival) | their SW05 12/12, window open 1.2e4; NOT registered | their SW05 quadrature | 1.086–1.155 (NOT registered) |
| **AQUAL EFE** | Amendment 10, in force | — | canonical [1.1614, 1.1814], alt [1.1917, 1.2267] |

**The live split (grok's rule, stated so a referee cannot stop at the table):** this class and
the xi-screened candidate OVERLAP at ~1.00 — the four-way is really
**{this class ∪ candidate} vs {cap/L268} vs {AQUAL}**. The class ∪ candidate distinction is
NOT a DR4 gamma_v discriminator (their windows overlap); the cap and AQUAL distinctions are.
Same-footing gaps >= 0.029; the cross-footing corner gap is 0.006 — **the footing must be
fixed before cap-law vs AQUAL can be told apart** (`kappa_slot_2026/SW07_program_ledger.out` R2).

## 3. The empirical verdicts — OPEN with dates

| prediction | status | discriminator | decision |
|---|---|---|---|
| P1 DR4 gamma_v | OPEN | class 1.0000–1.01012; in 1.086–1.155 kills class+candidate; in 1.1614–1.2267 kills class+candidate+cap | **2026-12-02 (76 days)** |
| P10 LMC DC/AC | OPEN | D_int = 1.1527 vs unsuppressed RAR 1.6742; tide/g_int = 0.0545 (DC dominates) — `SW11_dc_ac.out` 13/13 | LMC rotation/dispersion data |
| P8 a0(z) ratio | TENSION (registered) | R = a0(3)/a0(0) = 1.0000 vs registered 0.775 [0.68, 0.88]; Rubin 3.3 sigma — `SW05_kepler_freeze.out` | Rubin/DESI |
| P2/P3 nulls | computed | A2 = 2.22e-16; solar quadrupole 3.4e-39 s^-2 (`SW05` C1/P3) | archival |
| P4 eta window | OPEN, re-pointed | DE04 eta>=2 sample EMPTY (premise false — audit); window eta ~ 2–3.5 stands | needs new sample |
| Walker Jeans eta_c | OPEN | per-object likelihoods ABSENT in repo (audit) | data assembly |
| P5–P7, P9 | computed, scorable on archival data | SW05 9/9 | as data lands |

## 4. The theory door — G03: OPEN

Checklist **10 HARD / 2 OPEN** (`G03_CONSTRAINTS.md`, this directory): the two OPEN are
**G7 the retarded kernel** (UNSUPPLIED, `SW08_preferred_frame.out` C4 FAIL-as-finding) and
**G8 the ghost quadratic-form theorem** (no landed check). The hard walls a completion
cannot cross: G9 (no local 2-jet trigger — the obstruction), G11 (photon cone = g's),
G12 (alpha_1: gravitomagnetism or the deep-Newton suppression this class supplies via
S(eta_sun) = 0.0078, SW08 B4), G5 (c_S <= 4.23 / <= 423).

## 5. The Lean certificate chain — verified live this swing

`lake env lean` exit codes captured directly (2026-09-17, this session):
`SW06_lemmas.lean` EXIT 0 (5 theorems) · `SW09_meanvalue.lean` EXIT 0 (8) ·
`SW10_pair.lean` EXIT 0 (5, incl A_const) · `lean_2026/SW06_local_nogo.lean` EXIT 0 (3;
axioms propext/Classical.choice/Quot.sound only, per `#print axioms`) ·
`SW12_dr4_disjoint.lean` EXIT 0 (4: class_below_cap, candidate_ceiling_below_cap,
alt_foot_separated, corner_gap_forces_footing_first) = **25 theorems**.
Sorry/admit scan: zero postulates in all five files.

## 6. What would reopen what

- gamma_v measured in [1.086, 1.155] or [1.1614, 1.2267] → the class and candidate die (P1).
- LMC kinematics at the unsuppressed RAR (1.674) → the DC suppression dies (P10).
- A 2-jet invariant reproducing (Gamma, eta) on both pair members → the obstruction dies (SW10 kill, pre-registered).
- Any eta_c mechanism landing in [0.028, 0.203] → reopens the eta_c derivation (SW07 killed the priced class).
