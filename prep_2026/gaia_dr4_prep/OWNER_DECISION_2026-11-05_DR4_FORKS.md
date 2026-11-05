# OWNER DECISION, 2026-11-05 (pre-data): Gaia DR4 outcome map and scoring choices

**Status: filed.** The owner accepted, in chat on 2026-11-05, before any DR4 byte exists (DR4 due 2026-12-02): "Accept
all recommended". That adopts the recommended option of D1-D6 (section 3). **D7 and D8 carried no recommended option
and remain OPEN**; each needs its own dated pre-data decision. This file is committed alone. After commit, never edit
it; any change goes in a new dated file. It edits no frozen file: not PREREGISTRATION_DR4.md
or its 22 amendments, not the D2 note (NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md) or A1-A3, not CW1, CQ2, FN6, CFG740,
CFG800/825, or the 10-21 kill-line note. Every band below is arithmetic on rules already frozen; no prediction changes.
κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## 0. Why this note

The adopted theory (v3s, scoped; owner 2026-11-04, 7ac515f958) predicts **screened, Newtonian** wide binaries
(CQ2, 95303af61c: γ_r − 1 ≤ 4.5e-5 at 30 kAU; through the frozen pipeline γ_inf identical to Newton's in every
realisation). The bare law (plain QUMOND, CW1) predicts **1.149 / 1.208**. CQ2 adds no scoring rule. The D2 rows already
score "screened/medium-first" against "law-first", so the outcome can be laid out now, before the data. This note does
that and lists the choices that must be fixed pre-data.

## 1. The theories on the table

| reading | source | DR4 γ_v (canonical / alt) | status |
|---|---|---|---|
| **v3s, screened** | CQ2 | = Newton (1.000) | adopted theory |
| bare law, unscreened (plain QUMOND) | CW1 | 1.149 ± 0.027 / 1.208 ± 0.007 | the law without its action |
| law-first anchor used by the D2 rows | Arm A floor (A10) | 1.1614 / 1.1917 | frozen anchor |
| law-first AQUAL (D2 A1, named in A3's text) | D2 A1 | 1.167 / 1.199 (alt g_ext 1.145 / 1.173) | frozen, see decision D2 |
| FN6 screening-length window | FN6 seal | 1.00-1.04 (p ≤ 0.4); alt p 0.45 1.13-1.21 | description, not adopted |
| CFG740 stiff hedgehog (same s² form as v3s) | CFG740, R rule | ≤ 8.9e-4 at 50 kAU | scored by R, not γ̂ |

## 2. The outcome map (the forks)

Frozen D2 rows, with σ = √(σ_fit² + σ_sys²), σ_fit = 0.019 √(30000/N), σ_sys by definition (b) measured on DR4:
- **Gate:** σ_sys(b) < 0.048 canonical / 0.058 alt (D2 A1), and definitions (a), (e), (g2) give the same verdict at
  ≥ 3σ (A3). Otherwise **UNDECIDED** on that footing, whatever γ̂ is.
- **Screened (medium-first) excluded:** γ̂ − 1.000 ≥ 3σ, and γ̂ not below the law-first anchor by ≥ 3σ.
- **Law-first excluded:** anchor − γ̂ ≥ 3σ.
- **Guard zone:** γ̂ > 1.23 is no verdict for every arm (prereg, kill-line note N3).
- Footings and both g_ext values are scored separately.

### 2a. Plain-words map, canonical footing, registered error (N = 30,000, σ_sys 0.020, σ = 0.0276)

| DR4 γ̂ lands at | v3s (adopted) | bare law | reads as |
|---|---|---|---|
| ≤ 0.917 | — | — | **sub-Newtonian: no frozen row** (decision D4) |
| 0.917 – 1.079 | survives (not confirmed) | **EXCLUDED** | "screened side": Newton-like sky |
| 1.079 – 1.083 | survives | survives | UNDECIDED (a 0.004-wide gap) |
| 1.083 – 1.23 | **EXCLUDED** | survives | "law-first side": a boost |
| > 1.23 | no verdict | no verdict | guard zone (contamination) |

(Anchor = Arm A floor 1.1614. With the A1 AQUAL anchor 1.167 the law-first edge is 1.084, and the UNDECIDED gap vanishes.)

### 2b. Alt footing, registered error: the two exclusions OVERLAP

Medium-first edge 1.083; law-first edge 1.109 (Arm A 1.1917) or 1.116 (A1 1.199).
In **1.083 – 1.109** γ̂ is ≥ 3σ above Newton **and** ≥ 3σ below the law. As frozen, the D2 precedence reads this as
"law-first excluded" only, i.e. it **would not exclude v3s although the sky is 3σ above Newton**. This is a real
pathology of the frozen rows (decision D5).

### 2c. The map moves with N and σ_sys (canonical, Arm A anchor; arithmetic only)

| N | σ_sys | σ | law-first excluded if γ̂ ≤ | screened excluded if γ̂ ≥ | UNDECIDED band |
|---|---|---|---|---|---|
| 30,000 | 0.020 | 0.0276 | 1.079 | 1.083 | 1.079–1.083 |
| 30,000 | 0.0375 (DR3 (b)) | 0.0420 | 1.035 | 1.126 | 1.035–1.126 |
| 15,000 | 0.020 | 0.0335 | 1.061 | 1.100 | 1.061–1.100 |
| 6,210 (DR3's N) | 0.020 | 0.0463 | 1.022 | 1.139 | 1.022–1.139 |
| 6,210 | 0.0375 | 0.0561 | 0.993 | 1.168 | 0.993–1.168 |

Alt: law-first edges are 0.03 higher (1.053 at N 6,210 / σ_sys 0.020; 1.023 at 0.0375).
In words: **with a small sample or a large σ_sys, a Newtonian sky (~1.00) reads UNDECIDED, not "bare law excluded".**

### 2d. Separate fork: the R statistic (CFG740/CFG825, A22; kill-line note 2026-10-21)

KILL iff R − 1 ≥ max(0.01, 3σ_R), σ_R from the pairs entering R (N_R). CONSISTENT is unreachable (σ_R ≥ 0.02).
At ~2,100 pairs in R (catalogue N 30,000) σ_R ≈ 0.075, so a kill needs R ≥ 1.22. R is reported beside γ̂; if they
disagree it is a **split**, never merged (N6).

### 2e. Split outcomes, reported as splits

- canonical and alt disagree;
- primary and alternative g_ext disagree;
- γ̂ rows and R disagree;
- (b) passes but (a), (e) or (g2) disagrees → UNDECIDED (A3).

## 3. Decisions (pre-data)

**Ruling (owner, 2026-11-05):** D1 (a), D2 (a), D3 (a), D4 (a), D5 (a), D6 (a) ADOPTED. D7, D8 OPEN.
Consequences, stated now: v3s is scored in DR4 as the screened / medium-first reading of the frozen D2 rows plus the R
rule; the law-first anchor stays Arm A's floor; Newton = 1.000; γ̂ ≤ 1 − 3σ is NO VERDICT for every reading; in the alt
overlap of section 2b the reading is BOTH EXCLUDED; a Newton-side reading is worded "v3s survives", never "confirmed".
The options as presented:

- **D1. Does DR4 score v3s?** v3s's scope (7ac515f958) names galaxies, Solar System, lensing, GWs; Milky Way-hosted wide
  binaries are not named.
  (a) Yes: v3s is scored as the **screened / medium-first** reading of the D2 rows, plus the R rule. *Recommended:
  this is the only dated test of v3s's screening before 2027.* (b) No: DR4 scores only the bare law.
- **D2. Law-first anchor.** The D2 rows use Arm A's floor (1.1614 / 1.1917); A3's text names the A1 AQUAL values
  (1.167 / 1.199); CW1's bare law is 1.149 / 1.208. (a) Keep the frozen rows (Arm A), report the others as information.
  *Recommended: no change of a frozen row.* (b) Re-anchor on CW1 by amendment.
- **D3. Newton reference.** (a) 1.000 exactly, as in the D2 rows; the pipeline's own Newton draws (CW1/CQ2 1.0019 /
  1.0100, FN6 0.9919 / 0.9794) are reported as information. *Recommended.* (b) the pipeline Newton γ_inf.
- **D4. Sub-Newtonian row.** γ̂ ≤ 1 − 3σ has no row. (a) Read as "pipeline or contamination fault: NO VERDICT for every
  reading". *Recommended.* (b) leave unregistered.
- **D5. Alt overlap (2b).** (a) In the overlap, report **BOTH EXCLUDED** (neither screened nor law-first fits).
  *Recommended: otherwise a 3σ boost cannot exclude v3s.* (b) keep the frozen precedence.
- **D6. Wording.** A Newton-side reading is stated as "v3s survives; bare law excluded (if the gate holds)", **never**
  "v3s confirmed" (Arm C's own phrase: survival, never confirmation). (a) adopt. (b) other wording.
- **D7. Readiness items that shape the map (CFG943 notes).** N1 (σ_R from N_R, already used by the kill-line note),
  N4 (NSS-off rung: implement or declare absent), N5 (which catalogue feeds R), N9 (cut-13 mode for the seed sweep).
  Each needs a dated go or no-go.
- **D8. σ_sys(b) and the NSS-off probe.** As frozen, a stronger DR4 NSS screen enlarges the NSS-off shift and so σ_sys(b),
  widening the UNDECIDED band (2c). (a) Leave as frozen. (b) Commission a mock-triple injection test and decide by a
  separate dated amendment before 2026-12-02. No change after the data.

## 4. What follows on each branch (information, not a rule)

- **Newton-side (law-first excluded, gate holds):** the bare law's unscreened wide-binary prediction fails; v3s's
  screening survives its first dated test; PAPER67's "a Newtonian result would count against the law" must be read as
  the bare law only (addendum listing CQ2 owed).
- **Boost-side (screened excluded):** v3s's screening fails in wide binaries; the bare law survives this test; FN6 alt
  p 0.45 is the only sealed screening form left in range.
- **UNDECIDED / guard zone / split:** report raw γ̂, σ by every definition, both distances, R; no verdict word.

## 5. Sources

D2 note lines 22-31 (rows), 90-94 (A1 gate 0.048 / 0.058), 182-205 (A3); CQ2 SEALED_PREDICTION.md lines 1-39;
CW1 seal (df7801238b); FN6 seal (7ab147288d); kill-line note campaign_fresh_gravity/OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md
§1-2; FN2 fn2_dr4.out C3 (edges 1.0786 / 1.0828 canonical, 1.1089 alt, reproduced here); review
reviews/GAIA_DR4_DEEP_REVIEW_2026-11-05.md. Band arithmetic: σ_fit = 0.019 √(30000/N), edges = anchor ∓ 3σ.
