# DECISION BANDS FREEZE — directional-EFE aligned statistic, l=1-corrected (2026-07-16)

**Status: FROZEN.** This file pre-declares the corrected three-way interpretation bands
for the aligned directional-EFE statistic, incorporating the l=1 BVP result of
2026-07-16 (adversarially verified, UPHELD — see provenance below), BEFORE any
WALLABY-scale firing result is read. It was written without inspecting any
WALLABY-237 statistic value (only the running workflow's premise headers were read,
to name them in the supersession note). Any aligned-statistic firing evaluated on or
after 2026-07-16 — including the currently running WALLABY-237 lane — is to be
interpreted against THIS file, not against the banked w = 0.304 premise.

---

## 0. SUPERSESSION NOTE (read first)

A WALLABY-237 firing is currently RUNNING at
`/Users/carlzimmerman/new_physics/prep_2026/wallaby_firing/` with the OLD premise
baked into its headers and theory targets: "Branch B <= w x AQUAL, w = 0.304
(natural) / 0.24 (Cassini-max)" (verbatim in `xstrat_filter.py:99-100` with targets
"BranchB(0.304 nat / 0.24 Cass-max)", and in the firewall headers of
`run_extraction_237.py`, `run_gext_237.py`, `W1_EXTRACTION.md`, `W2_VECTORS.md`,
`XSTRAT_SPEC.md`, `QC_FROZEN.md`). **That Branch-B interpretation line is
SUPERSEDED by this freeze:** the l=1 BVP shows the committed moduli make the
transfer factor run with radius, and at the rotation-curve sourcing radii
(x = g_bar/a0 = 0.05–0.5) the Branch-B suppression is w(x) = 0.513–0.769 at natural
beta = 2/7 — NOT 0.304. The running firing's extraction, vectors, QC, and statistic
machinery are untouched and remain valid; only the Branch-B AMPLITUDE row of its
theory-target table and any "AQUAL-vs-BranchB at N~1,157" separation claim must be
re-read through Section 3–4 below when its result lands. Its pure-MI (=0) and
AQUAL (banked map) rows are unaffected. Nothing in the wallaby_firing directory has
been modified by this freeze.

---

## 1. PROVENANCE + HASHES

**l=1 source of the correction** (all at `/Users/carlzimmerman/new_physics/prep_2026/l1_bvp/`):
- `l1_bvp.py` — re-run 2026-07-16 for this freeze: **exit 0, 14/14 gates PASS**,
  output consistent with the banked `l1_bvp.out` (w_l1(2/7) at r_t shell = 0.3043;
  w(x) profile 0.5128–0.7690; corrected N-targets 6,007 / 379,641 / 7,391 / 467,659).
- `L1_RESULT.md` — result note; `VERIFY.md` + `verify_l1_independent.py` —
  independent-method adversarial verification (box-scheme sparse-LU, no initial
  guess; harmonic-projected extraction; zero-mode attacks), verdict **UPHELD**,
  12/12 independent checks pass.

**Frozen pre-registration being corrected** (READ-ONLY, cite-never-modify):
`zimmerman-formula/real_research/reviews/directional_efe_2026/`
(`laneA_predictions.py` — the banked A(x,e) map and the flagged l=1 caveat at
lines 388–399; `confrontation.py`/`confrontation.out` — the pre-registered kill
conditions and the N table; `laneA_predictions_results.json` — the banked map values).

**SHA-256 (computed 2026-07-16):**
```
5bdd7a43c9274158774caa87f4855362582d17de0a51634915f2df9628763848  l1_bvp.py
7a56387b1cb1c42c1def4082106ed57c5613c18f73a14a373620d745d984c544  laneA_predictions_results.json
```

---

## 2. RETRACTION NOTICE — the 0.304 bound, with l=1 provenance

**RETRACTED for the aligned statistic:** the banked inequality
`A_BranchB <= w x A_AQUAL with w = w_l2 = 1/(1 + 4 beta/kappa_t) = 7/23 = 0.304`
(natural beta = 2/7, kappa_t pinned 0.5), carried in
`laneA_predictions.py:388-399` with the honest caveat that "an explicit l=1 BVP …
has NOT been run" and used as the Branch-B premise in `confrontation.py` and the
running WALLABY-237 lane.

**What the l=1 BVP found (both halves reported straight):**
- (a) The banked STRUCTURAL claim was right — at fixed (beta, kappa_t) the l=1
  transfer factor equals the l=2 one exactly: w_l1 = w_l2 = 1/(1 + 4 beta/kappa_t)
  to 0.01% (BVP-computed, independently re-derived by a guess-free method). The
  feared O(1) l-geometric coefficient does not exist; the "<=" was "=" at fixed
  kappa_t.
- (b) The bound was nonetheless **INVALID AS APPLIED** to the aligned statistic:
  the committed moduli themselves (`methodA_ode.py:11`, lane-1 sqrt-branch tangent
  K_t = K_eff/(2 sqrt(J0))) make kappa_t RUN with radius. The 0.304 lives at the
  r_t shell (rho ~ 1, J0 ~ 1 — the Cassini Q2 sourcing region). The aligned RC
  statistic sources at x = g_bar/a0 = 0.05–0.5 (rho = sqrt(y_c/x) ~ 2.4–7.6),
  where local kappa_t(x) = 0.5 sqrt(y_c/x) = 1.2–3.8 and the BVP-computed
  suppression is w(x) = 0.513–0.769 at natural beta. Using 0.304 as an upper bound
  out there contradicts the committed moduli.
- **Cassini/Q2 untouched:** Q2 sources at rho ~ 1, where the same solve still gives
  w = 0.304 at natural beta; the committed Q2 gate verdict (beta_crit ~ 0.40 canon
  / 0.60 alt) is not modified.

**Replacement (the frozen Branch-B law):**
```
A_B(x, e, gamma) = w(x) x A_AQUAL(x, e, gamma)
w(x) = 1 / (1 + (4 beta / K0hat) sqrt(x / y_c))
     = 1 / (1 + 8 beta sqrt(2x / Z))        [K0hat = 0.5 pinned, y_c = Z/2]
Z = sqrt(32 pi / 3) = 5.7884
```
BVP-computed at l=1 (tracks the local law to <=0.02% at the relevant rho);
K0hat = 1.0 (saturated floor) pushes w(x) HIGHER still — there is no defensible
moduli reading that restores w = 0.304 at the RC radii. w is dimensionless and
a0-footing-independent at fixed x (checked to 4 decimals, both footings,
g_ext in {0.2, 1.9, 2.2, 2.6} a0).

---

## 3. THE FROZEN THREE-WAY BANDS (per theory, as functions of x = g_bar/a0)

Amplitudes are the aligned per-side RC asymmetry A (laneA convention,
A = 2(v_rec - v_appr)/(v_rec + v_appr) projected on cos(psi) x G(gamma)); all
values at the LOCAL-FORCE FLOOR — the loop-orbit amplification bracket multiplies
every MG amplitude by ~1–5 (bracket top x4.4–5.7) without changing the ratios
between theories. Sign convention (banked, all theories with nonzero amplitude):
attractor-facing side FASTER for x >~ 2e, with the EFE-REVERSAL sign flip at
x <~ e (the banked map carries it).

### (i) Pure MI (the framework proper, modified inertia)
```
A(x) = 0 exactly, at every x.
```
A uniform g_ext is a frame acceleration; the aligned asymmetry vanishes
identically. No band, no envelope.

### (ii) Branch B (published elastic-medium action, trace-only h(J) coupling)
`A_B(x) = A_AQUAL(x) / (1 + 8 beta sqrt(2x/Z))`, beta the lane-2 free parameter
in (0, 2), natural beta = 2/7 (natural window 0.18–0.33). Frozen w(x) values
(BVP-computed; r_t-shell column shown only to locate the retracted 0.304 — it is
NOT an aligned-statistic value):

| beta | x=0.50 | x=0.30 | x=0.20 | x=0.10 | x=0.05 | (r_t shell, Cassini) |
|---|---|---|---|---|---|---|
| **2/7 (natural)** | **0.513** | **0.576** | **0.625** | **0.702** | **0.769** | 0.304 |
| 0.40 (beta_crit canon) | 0.429 | 0.493 | 0.543 | 0.627 | 0.704 | 0.238 |
| 0.60 (beta_crit alt) | 0.334 | 0.393 | 0.442 | 0.529 | 0.613 | 0.172 |
| 2.00 (all-shear corner) | 0.131 | 0.163 | 0.192 | 0.252 | 0.322 | 0.059 |

Against the committed representative AQUAL band (~1% at x=0.5 rising to ~4% at
x=0.05, typical e), the natural-beta Branch-B aligned band is
**A_B ~ 0.51%–3.08%** (was banked <~0.3–1.2%). Over the full beta in (0,2)
envelope the band spans from ~w=0.13 x A_AQUAL (all-shear corner) up to
arbitrarily close to A_AQUAL as beta -> 0. Note the Cassini-Q2 gate independently
prefers beta >= beta_crit (0.40 canon / 0.60 alt) — at those beta the aligned
band is w(x) = 0.33–0.70 of AQUAL, still far above the retracted 0.304 ceiling.
Branch B moves TOWARD AQUAL: easier to detect against the null, harder to
separate from AQUAL. Sign and shape (attractor-side-faster, EFE reversal at
x <~ e) identical to AQUAL.

### (iii) AQUAL / QUMOND (MG-class comparator)
The banked laneA map A(x, e), gamma = 0, framework nu, in percent
(`laneA_predictions_results.json`, hash above; rows x, columns e; negative =
EFE-reversed sign at x <~ e):

| x \ e | 0.02 | 0.05 | 0.10 | 0.20 | 0.30 |
|---|---|---|---|---|---|
| 0.50 | +0.64 | +1.46 | +2.61 | +4.39 | +5.69 |
| 0.20 | +1.79 | +3.86 | +6.28 | +3.62 | -3.93 |
| 0.10 | +3.47 | +6.76 | +3.60 | -5.67 | -6.19 |
| 0.05 | +6.07 | +3.50 | -6.74 | -7.63 | -7.11 |

Representative committed band ~1–4% over the RC regime; representative footing
point (illustrative outer galaxy, g_bar = 1e-11, g_ext = 3e-12 m/s^2):
A_AQUAL = +4.74% (canonical a0: x = 0.107, e = 0.032) / +4.81% (alt a0:
x = 0.088, e = 0.027). Gamma factor: banked A(gamma)/A(0) ~ [1, 1.37, 0.78, 0]
at [0, 30, 60, 90] deg.

**Both a0 footings (standing rule, both always run):** canonical
a0 = 9.36e-11 m/s^2 (cH_Lambda/Z, Z = sqrt(32 pi/3) = 5.789) and alt
a0 = 1.13e-10 m/s^2 (rho_total/cH0). w(x) is footing-independent at fixed x;
per-galaxy x and e shift with the footing; N-targets below are given for both.
Verdicts must be checked on both footings before being called.

---

## 4. PRE-DECLARED DECISION RULES (corrected; these replace the banked kill conditions)

The stacked matched-filter statistic Ahat (pre-registered, E[Ahat] = 1 under
AQUAL at the local-force floor, E[Ahat] = w(x)-weighted ~ 0.5–0.77 under natural-
beta Branch B, E[Ahat] = 0 under pure MI and under the null). Representative
outer point x = 0.107 (the confrontation footing) -> w* = 0.695. All N in
"galaxies with per-side RC + g_ext VECTOR"; scaling law is the committed one
(N proportional to 1/amplitude^2; N_3sig(alpha) = N_null/alpha^2, anchored to the
frozen confrontation.out row N_null = 560 canon/maxclu, 689 alt/maxclu;
35,390 / 43,595 no-clustering).

**R1 — DETECTION at AQUAL amplitude** (Ahat consistent with 1 [up to the 1–5x
loop-orbit bracket], >= 3 sigma from 0):
**Pure MI is killed at the stated sigma** (its prediction is exactly 0). **BOTH
MG doors stay live:** under the corrected band, natural-beta Branch B sits at
0.51–0.77 of AQUAL, so an AQUAL-amplitude detection no longer excludes Branch B
by amplitude alone (the banked rule "detection at AQUAL amplitude -> Branch B
dead" is SUPERSEDED — see Section 6). Separating the two doors at 3 sigma
requires **N ~ 6,000** canon/maxclu (x-band 2,359–10,490 over x = 0.5–0.05),
**~7,400** alt/maxclu (x-band 2,903–12,906); no-clustering ~380,000 / ~468,000.
The x4.4–5.7 loop-orbit bracket-top and robust-sigma (x0.21) reductions of
confrontation.out apply multiplicatively (bracket-top canon/maxclu: ~310).

**R2 — DETECTION at Branch-B-band amplitude, below AQUAL** (Ahat >= 3 sigma from
0, point estimate inside the natural-beta band 0.51–0.77): **pure MI is killed at
the stated sigma; consistent with Branch B; AQUAL disfavored only at the achieved
separation sigma** — a 3-sigma AQUAL-vs-Branch-B call requires the same
**N ~ 6,000** (canon/maxclu) as R1. **Pre-declared: WALLABY-237 CANNOT make this
separation.** At N = 237 the achieved sensitivity at AQUAL amplitude is
~1–1.5 sigma (the running lane's own firewall estimate; idealized max-clustering
scaling gives 3 x sqrt(237/560) = 1.95 sigma), so the AQUAL-vs-Branch-B
separation sensitivity is (1 - w*) x that ~ 0.6 sigma. Whatever amplitude
WALLABY-237 returns, it is not an AQUAL-vs-Branch-B verdict.

**R3 — DEEP NULL below the Branch-B band floor** (Ahat + 3 sigma(Ahat) < w*,
i.e. the natural-beta Branch-B expectation is excluded at 3 sigma): **BOTH AQUAL
and Branch B are killed at the stated sigma; pure MI alone survives** (it is the
only door predicting exactly 0; the null hypothesis "no directional physics" is
of course degenerate with it in this statistic). Decidability (derived in this
freeze from the committed scaling, arithmetic shown):
- AQUAL excluded at 3 sigma: N = 560 canon/maxclu (689 alt) — unchanged.
- Natural-beta Branch B excluded at 3 sigma: N = N_null / w*^2 = 560 / 0.695^2
  ~ **1,160** canon/maxclu (x-band 947 [w=0.769] – 2,130 [w=0.513]);
  689 / 0.695^2 ~ **1,430** alt/maxclu.
- Full beta-in-(0,2) envelope excluded (all-shear corner, w(beta=2, x=0.107)
  = 0.245): N ~ 560 / 0.245^2 ~ **9,300** canon/maxclu.
- Loop-orbit bracket-top divides these N by ~19–32 IF that amplification holds;
  since the bracket only AMPLIFIES the MG signal, a floor-level null is
  conservative — bracket-top makes the R3 kill easier, never harder.
Note the corrected band makes the R3 Branch-B kill EASIER than banked
(N ~ 1,160 vs the ~6,050 the old w = 0.304 would have implied) while making the
R1/R2 separation HARDER (N ~ 6,000 vs 1,157) — reported straight, both
directions. At N = 237 the R3 kill cannot fire at the local-force floor
(237 < 947 even at the most favorable x).

**Detection-vs-null target unchanged:** N = 560 canon/maxclu (does not involve w).

---

## 5. THE EXPLORATORY n=16 RESULT (firewall intact — context only)

The first firing of the pre-registered statistic (this directory,
`FIRST_FIRING.md`, 2026-07-16) returned Ahat = +2.95 (perm p1 = 0.029,
p2 = 0.061) on n = 16. **EXPLORATORY:** computed sensitivity sigma(Ahat) = 3.13,
i.e. ~0.3 sigma at the AQUAL floor — it CANNOT trigger any pre-registered or
pre-declared condition (banked or corrected), and it is firewalled from the
decision rules above. It neither kills Branch B nor supports it. One line of
FIRST_FIRING.md is superseded by this freeze: its Branch-B expectation
"~0.24–0.30" (in Ahat units) becomes ~0.51–0.77 under the corrected band; this
changes no conclusion of that run (still underpowered by an order of magnitude).

---

## 6. INCONSISTENCIES FOUND: the l=1 result vs the old pre-registration

Beyond the retracted amplitude bound, the corrected band FLIPS the logic of both
banked kill conditions (`confrontation.py`, verdict section):

1. **Old kill condition 1** — "aligned asymmetry DETECTED at AQUAL amplitude ->
   Branch B dead" (rationale: w ~ 1 would fail Cassini Q2 x4–6). SUPERSEDED: at
   the RC radii natural-beta Branch B is 0.51–0.77 of AQUAL, not <= 0.304, so an
   AQUAL-amplitude detection no longer excludes Branch B by amplitude below the
   N ~ 6,000 separation scale. The Cassini rationale survives only against
   w(rho~1) ~ 1, which an RC-radius amplitude does not measure.
2. **Old kill condition 2** — "NULL at < 0.5% aligned -> first empirical support
   for suppressed shear [Branch B]". INVERTED: 0.5% now sits AT/BELOW the
   natural-beta Branch-B floor (0.51% at x = 0.5), so a < 0.5% null no longer
   supports Branch B — at sufficient N (Section 4, R3) it kills it, together
   with AQUAL, leaving pure MI alone. Likewise the old MI-caveat line "a future
   NULL supports Branch B AND pure MI against AQUAL-class MG" now holds only in
   the shallow-null regime (Ahat excluding 1 but not w*); a DEEP null separates
   pure MI from Branch B too.
3. No numerical inconsistency was found: the l=1 solve reproduces the committed
   l=2 anchor (0.3043 = 7/23, dev 0.00%), the committed N-scaling
   (560/(1-0.3043)^2 = 1,157 = confrontation.out), and the frozen map values;
   the correction is entirely the evaluation-point issue the banked caveat
   itself flagged as unproven.

---

## 7. HONESTY RAILS (carried forward)

- Nothing here is described as proven about nature; w(x) is BVP-computed within
  the committed elastic-medium model and adversarially verified as such; the
  galaxy application goes through the local law w = kappa_t/(kappa_t + 4 beta)
  (validated in the Sun+g_ext testbed geometry to <=0.02% at the relevant rho);
  a disk-geometry l=1 solve remains the gold standard.
- beta stays the lane-2 free parameter in (0, 2); all headline numbers at
  natural beta = 2/7 with the envelope stated.
- Both a0 footings run on every verdict; neither footing flips any band or rule
  above (w is footing-independent at fixed x).
- Amplitudes quoted at the local-force floor; the 1–5x loop-orbit bracket is an
  amplification bracket, not a fitted value.
- The n=16 exploratory number is firewalled and stays firewalled.

**FREEZE DECLARATION:** these bands and rules were fixed on 2026-07-16, prior to
reading any WALLABY-237 statistic value. Post-hoc modification of this file after
the WALLABY-237 result lands would defeat its purpose; corrections, if any, go in
a dated successor file that cites this one.
