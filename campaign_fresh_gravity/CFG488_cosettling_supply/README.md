# CFG488: co-settling shell by shell does not supply the 5.85 r_M edge. FAIL (RESTATEMENT ONLY)

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in 88f3bdcaa. The script is `cfg488_cosettling.py`. The infall
runs are done by `cfg488_infall.py`, which copies CFG118's machinery and compiles CFG118's `shellcore.c` read-only. Twelve runs
take about 1 minute; the whole analysis takes about 2 minutes.
- Main run: exit 0, because controls K1–K5 pass. K6 (resolution) fails; it is reported and kept.
- `CFG488_MUTATE=1` (cosmic ratio × 2): exit 1. The teeth were detected, as designed.

κ = ½ is FITTED. Both footings are scored separately and never pooled. No dark-matter particle is added: the cold fluid's mass
is still required, and its amount (Ω_c/Ω_b = 5.364) is an input. This is not "theory closed".

## The question

CFG462 left one gap: the SUPPLY. The growth fix's edge r_edge = r_M/ln(1/(1 − f_b)) = 5.8498 r_M is where the phantom has used
up exactly 5.364 M_b. A halo's turnaround catchment holds about 4 times that. Why would a halo settle only the cold fluid that
came with its present baryons?

The idea tested is co-settling. Every Lagrangian shell starts with cold fluid and baryons in the ratio 5.364. A shell's cold
fluid is eligible to settle only while that shell's baryons are in the galaxy. Cold fluid whose baryons never arrived, stayed
hot, or were expelled stays unsettled.

## The identity that decides most of it (stated in the criteria before any run)

For any accretion history, the eligible cold mass is 5.364 × (the galaxy's baryons). The code selects eligible shells by their
baryon content, never by a cold-mass number, and every history gives 5.364000000000 M_b (spread 9e-16).
- So the 5.364 M_b is not inserted by hand. It enters as the shells' composition, an initial condition.
- But that total is the SHARE supply of CFG462's restatement control, whatever the history. The history can only change WHERE
  the eligible fluid settles. That is what the five readings below test.

## The five readings (all scored; none dropped)

"Settles into the phantom sourced by those same baryons" can be read five ways:

| reading | what the eligible cold fluid does |
|---|---|
| CS-P | pooled, free transport: fills the present phantom inside-out (CFG462's F-H equilibrium) |
| CS-I | pooled, inward-only: a parcel can settle only inside its own radius (settling loses energy); the rest stays put |
| CS-0 | in place: settles only where it already is, up to the local phantom density |
| CS-M | per shell: each increment of baryons fills its own marginal phantom at accretion and stays there |
| CS-F | per shell: each increment fills its proportional share of the phantom at accretion and stays there |

**Accretion history.** H-N (scored) is CFG118's point-core secondary infall in ΛCDM, N = 20,000 shells, q = r_peri/r_ta =
0.05, 0.1, 0.2. It is the framework's own collapse under mass conservation: the phantom IS the settled cold fluid, so the
enclosed real mass sets every shell's field. H-B (Bertschinger, Einstein–de Sitter) is reported only.

**Retention.** R1 (scored) is inner-first: the galaxy's baryons are the innermost shells'. R2 (uniform fraction) is reported
only.

The host is a point mass (scored). Hernquist a = 0.3 r_M is reported for the scale-free readings.

## Verdict table

Edges are log₁₀(r_e/5.8498 r_M), where r_e encloses 99.9% of the settled mass. "Law" is the largest deviation of the eligible
cold mass from M_ph(<r) over [0.1, 0.8] r_edge, in all six cells (10⁹, 10^10.5, 10^11.5 M☉ × 2 footings). The line is 0.05 for
both.

| reading | edge (6 cells) | law carried? | R-EQ | (1) | (2) clusters: u inside R500 | (2) | (3) G9 |
|---|---|---|---|---|---|---|---|
| CS-P | −0.0004 (all) | 0 | **yes** | PASS | 0 (can and alt) | FAIL | FAIL |
| CS-I | −0.095 … +0.003 | 0.00 … +0.58 at 10⁹; +0.92 … +3.12 above | no | FAIL | 0.452 / 0.389 | PASS | FAIL |
| CS-0 | +0.46 … +0.94 | −0.49 … +3.12 | no | FAIL | 0.452 / 0.389 | PASS | FAIL |
| CS-M | +0.288 (all) | −0.22 | no | FAIL | 0 | FAIL | FAIL |
| CS-F | −0.013 (all) | **+2.16** | no | FAIL | 0 | FAIL | FAIL |

The record range for u is [0.433, 0.628] canonical and [0.368, 0.584] alt. It comes from CFG453's committed medians,
5.364 x_A/x_T15 at b = 0 to 0.3.

**Lane verdict: FAIL (RESTATEMENT ONLY).**
- No reading passes (1), (2) and (3) together.
- The only reading that passes (1) is CS-P, and it is restatement-equivalent: its profile is CFG462's SHARE control exactly,
  and no history changes it.
- (4) depletion: LIVE gives a MISS; SET is CONDITIONAL.

## What was found

1. **The edge lands only as the share control (CS-P).**
   - Under CS-P the eligible fluid fills the present phantom inside-out until the composition supply runs out: 5.8498 r_M for
     a point host and +0.017 dex for Hernquist a = 0.3 r_M. This is CFG462's K3.
   - The accretion history drops out exactly. Co-settling supplies a reason for the 5.364 M_b, but the edge arithmetic is the
     T10 S6 definition with the supply relabelled.

2. **The per-shell readings do not carry the law.**
   - **CS-M** puts each increment's cold fluid into its own marginal phantom. Its marginal edge is x_k = 11.707 r_M (from
     ν + yν′ − 1 = 5.364), so the support reaches +0.288 dex past the edge. The law is under-filled by 6–22% between 0.5 and
     4.7 r_M, and only 73% of the supply ends up inside r_edge.
   - **CS-F** ends on r_edge (−0.013 dex) only because its last increment's exhaustion radius IS r_edge.
     - Its early increments, accreted when the galaxy was small, pile cold fluid at small radii: 3.4×, 2.4× and 1.8× the
       phantom at 0.5, 1 and 2 r_M.
     - It lands on the edge number with the wrong galaxy inside.

3. **The in-place readings inherit CFG118's infall pool, whose scale goes as M^(1/3) rather than r_M ∝ M^(1/2).**
   - **CS-0:** the in-place edge is the outer tail of the eligible orbits, at +0.46 to +0.94 dex.
   - **CS-I:** the edge lands only at 10⁹ M☉ (−0.014 to +0.003). There the eligible pool is about as diffuse as the phantom
     (P/T at r_M = 0.74–1.09), so at most 0.14 M_b strands. With q = 0.2 nothing strands and CS-I reduces to CS-P exactly;
     with q = 0.05 and 0.1 the law is still exceeded by +0.25 to +0.58 near 0.6 r_M.
   - At 10^10.5–10^11.5 the pool is 1.5–2.6× the phantom at r_M. Then 0.26–1.19 M_b of eligible fluid strands inside the
     galaxy (most of it inside r_M) and the edge drops to −0.016 … −0.095 dex. The eligible cold mass near 0.6 r_M, the inner end
     of the law window, exceeds the law by +0.9 to +3.1 (as a fraction of the law).
   - H-B is worse: edges −0.02 to −0.19 dex, and the law is exceeded by +0.65 to +6.4.

4. **Clusters split the readings the other way.**
   - The record treats clusters as closed boxes (0.95 cosmic shares inside R500, CFG453), so all their cold fluid is eligible.
   - Free placement (CS-P/M/F) puts it all into the phantom: inside R500 only M_ph = 2.94 / 3.28 M_b remains, against a
     measured 5.12–7.74 M_b. So u = 0, and MOND's cluster deficit returns.
   - In-place readings (CS-I/0) cannot move the surplus out, so it stays unsettled: u = 1 − (ν − 1)/5.364 = 0.452 / 0.389. That
     is inside the record range, but only by +0.019 / +0.022 at the low (b = 0) end.
   - **The reading that fits clusters does not land on galaxies, and the reading that lands on galaxies empties clusters.**

5. **G9: keying settling to the baryons' accretion history needs a direct baryon–cold coupling.** The precise argument:
   - **What co-settling needs.** Eligibility E(q, t) = [q ∈ Gal(t)] is a property of the BARYON parcel with label q: where it
     is, and whether it cooled, stayed hot or left. These are decided by shocks, cooling and feedback after the two species have
     separated.
   - **What G9 allows.** Matter couples to gravity only (CFG329). The cold parcel can know about baryons only through the
     gravitational field along its own worldline.
   - **The per-parcel signal is zero in the continuum.** Flipping the fate of parcel q's own baryons changes the field on parcel q
     by its own baryon mass over the enclosed mass. That is δg/g = 7.0e-5 at N = 20,000 and 4.7e-4 at N = 5,000.
     - The raw ratio is 6.7, not 4, because the boundary shell's own time-averaged radius differs between the runs. At one
       common radius the ratio is 4.4 (post-hoc line).
     - The signal goes as 1/N. In the continuum, any gravity-only rule gives parcel q the same settling decision whatever its
       partner did.
     - So the literal rule needs a term that reads the baryon parcel carrying the same Lagrangian label. That is a two-species
       label and a direct baryon–cold coupling, nonlocal once the partners have separated. **All five readings are G9-FAIL as
       stated.**
   - **The collective signal is visible but does not rescue it.** The halo-level fate is visible at O(f_b): δg/g = 0.054 at
     r_edge if the galaxy's baryons had stayed on the eligible orbits. But a gravity-only rule built on it must say "settle
     until the settled mass equals (Ω_c/Ω_b) × the galaxy's baryon mass". That needs:
     - the galaxy's baryon mass apart from the cold fluid's own (a species-split field: G9-TENSION, CFG462's F-H class);
     - Ω_c/Ω_b inside the settling law, either inserted by hand or read from the fluid's own density and the expansion at a
       latch.
   - **Either way the surrogate is the edge definition written as a law.**

6. **Co-settling leaves the ineligible cold fluid unsettled, and much of it sits inside the edge.** These are H-N time
   averages.
   - Under R1 the ineligible cold inside r_edge is 1–11% of M_ph(<r_edge) at 10⁹, 11–29% at 10^10.5 and 30–52% at 10^11.5
     (both footings). It is flagged "law contaminated" at 10^10.5 and 10^11.5.
   - That is unsettled, CDM-like mass inside the galaxy on top of the law.

7. **R2 (uniform retention; reported only) is the closest call, and it is still the share fill.**
   - R2 + CS-I with q = 0.2 passes (1) in all six cells: edges +0.001 to +0.002 dex, law within +0.047.
   - It passes because R2 spreads the eligible fluid over the whole catchment, so nothing strands and inward-only filling is
     CFG462's SHARE control in substance (within 5%, q-dependent).
   - It is G9-FAIL like the rest.
   - It leaves 39–109% of M_ph(<r_edge) as ineligible unsettled cold fluid inside the edge, because R2 makes 77% of every inner
     shell ineligible.
   - Had R2 been scored, the label would be plain FAIL rather than RESTATEMENT ONLY. The pass/fail outcome would not change.

8. **Depletion (4): LIVE misses KiDS; SET matches only in an extreme limit.**
   - These use CFG413's 1,953 KiDS lens groups.
   - Control: the unweighted group median r_ta is 1.088 Mpc, against CFG413's 1.09.
   - **LIVE.** The edge stays at 5.85 r_M of the present baryons. The lensing-weighted median x_edge is 0.038 r_ta canonical
     (16–84%: 0.030–0.044) and 0.033 alt. None of the weight falls in the window 0.3–0.5. CFG413 rejects x = 0.05 by Δχ² +40.
     **MISS.**
   - **SET.** The partners of baryons that were once in the galaxy stay settled, so the edge is r_M/ln(1 + f_ret/5.364).
     - To reach the window, f_ret = present/ever-in-galaxy baryons must be 0.070–0.117 canonical (0.060–0.101 alt). That is the
       halo-level census, 0.07–0.10.
     - Co-settling never settles the partners of baryons that never reached the galaxy, so f_ret,gal ≥ the census value.
     - Matching therefore needs essentially all of each halo's missing baryons to have passed through the galaxy and been
       expelled.
     - The edge would then be ~54–77 r_M. That is the census-retention edge PAPER45 found marginal for growth at 512³
       (max|P − 1| 0.092 / 0.101).
     - **CONDITIONAL.**

## MUTATE (Ω_c/Ω_b → 10.728 at fixed Ω_m; law, host and r_edge true)

- **CS-P** moves +0.2829 dex, as predicted (+0.2829), and fails P1 against the true edge.
- **CS-M** moves +0.2824 (predicted +0.2827) and **CS-F** +0.2826. **CS-I** moves +0.277 to +0.299 across q and cells: it is
  supply-keyed.
- **CS-0** moves +0.016 to +0.269, not as predicted: its edge is the orbit tail, not the supply.
- The in-place cluster u moves to 0.726 / 0.695, outside the range.
- f_b-test (finite difference over the pair): d ln y_e/d ln f_b = 2.13 for CS-P/M/F, against 2.18 locally. The edge is keyed
  to f_b through the composition, which is why it is keyed at all.
- **TEETH DETECTED**, exit 1.

## Controls

- **K1 PASS (sympy).** Checks:
  - the composition identity;
  - ν − 1 = 1/(e^(1/x) − 1) for a point mass;
  - x_e = 1/ln(1 + 1/S);
  - the marginal phantom = ν + yν′ − 1;
  - self-similarity of the marginal edge (x_k √m);
  - x_k against the closed form, to 7e-6.
- **K2 PASS.** CS-P gives 5.849761 r_M.
- **K3 PASS.** The CS-M superposition matches the closed form to 4e-6.
- **K4 PASS.** H-N reproduces CFG118:
  - M_ta = 23.632 M_b (CFG118 23.642; f_b 0.157134 vs 0.157);
  - r_ta0 = 507.94 kpc (508.00);
  - zero-velocity radius / single shell = 1.0000.
- **K5 PASS.** CS-I's min-cut equals the greedy fill to 4e-16.
- **K6 FAIL (reported, kept).** CS-0's edge moves by up to 0.315 dex between 5,000 and 20,000 shells, because it is the pool's
  outer tail. CS-I's edges agree within 0.020 dex. No (1) verdict flips at 5,000 shells.

## Disclosures (changes after the first output; none moves a verdict)

- **The frozen K1 text wrote the CS-M closed form without the early increments that have already placed all their fluid inside
  r (+S m*).**
  - The first run's K3 failed (relative error 9.5) on exactly that.
  - The scored CS-M profile is the direct superposition, which never used the closed form. K3 now uses the corrected form.
  - The sympy "telescoping" item is implemented as the self-similarity identity. The telescoping itself is the fundamental
    theorem of calculus, and sympy cannot integrate ν_mono's derivative in closed form.
- **The marginal phantom's finite-difference step was raised from 1e-6 to 1e-3.** The committed ν_mono is a table, and its
  interpolation noise was amplified at the smaller step. With the larger step the error is ≤ 6e-6. The K1 numeric tolerance on
  x_k (1e-4, not frozen) was set to match.
- **The infall worker's first bin was changed to include r below the innermost edge.** This was done after a 2,000-shell test
  and before the scored runs.
- **Added after the first full output (printing only):**
  - the per-reading K6 breakdown and its verdict-flip check;
  - R2 and H-B rows for both footings;
  - the R2 contamination row;
  - the G9 common-radius line, labelled POST-HOC.
- **My "expected" text was close but not exact:**
  - CS-M's edge is +0.288, not ~+0.30.
  - CS-F over-fills by up to 3.4×, not ~2×.
  - The KiDS LIVE median is 0.033–0.038, below the 0.05–0.1 I wrote.
- **Side note on CFG462.** CFG462 is not edited; its verdict is unaffected, and its F-H edge would move from about 23.4 to about
  24.4 r_M.
  - CFG118's M_ta field is the COLD Lagrangian mass of the turnaround shell; the core is extra.
  - The cold mass inside r_ta at z = 0 is 23.63 M_b (K4), not the 22.6 M_b used for CFG462's catchment supply.

## Caveats

- Everything is spherical.
- The pool is the pre-settling infall, with settling applied afterwards. Settling's back-reaction on the orbits is not modelled.
- In H-N the galaxy's baryons sit in the core from z = 100 (CFG118's set-up), while eligibility follows the inner shells (R1).
  H-B's seed is extra mass on top of the shells' own baryons.
- The cluster prediction uses the closed-box assumption and the X-COP medians at R500. CS-0 is evaluated cumulatively there, as
  declared.
- The q brackets are an initial-condition bracket, not a fit. Time averages over one local dynamical time carry stream noise:
  the binned pool closes to 0.99–1.02, and K6 applies.
- KiDS's window depends on CFG413's free two-halo term.

## What this leaves

Co-settling relabels the supply; it does not derive it.
- With free transport it reproduces the 5.85 r_M edge only as CFG462's share control, and it then empties clusters.
- With in-place or inward-only settling it fits the cluster split, but the infall pool's M^(1/3) scale puts the edge and the
  inner law off at 10^10.5–10^11.5 M☉.
- In every reading the rule needs each cold parcel to know its own partner baryons' fate. That is a direct baryon–cold coupling
  (G9).
- Its only gravitational surrogate, "settle until (Ω_c/Ω_b) × the galaxy's baryons", is the edge definition again.

The supply gap stands as CFG462 left it.

## Run

```
python3 campaign_fresh_gravity/CFG488_cosettling_supply/cfg488_cosettling.py                    # exit 0; reuses cfg488_sims.json if its hash matches
CFG488_MUTATE=1 python3 campaign_fresh_gravity/CFG488_cosettling_supply/cfg488_cosettling.py    # exit 1 = teeth detected
```

Inputs, all read-only:
- `CFG118_secondary_infall/shellcore.c`
- `CFG4_common` (ν_mono)
- `CFG453_t15_deficit_units/cfg453_results.json`
- `CFG100_kids_mass_rederivation/cfg100_lib.py`
- `real_research/data/lensing_rar/{lr_lenses,cfg110_perlens}.npz`
