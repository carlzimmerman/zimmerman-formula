# VERIFY_ring.md — adversarial verification of the RING-BY-RING RAR test
Lane CC verify pass, 2026-07-16. Verifier ran independently of the compute author; every number below
is from an exit-0 script (re-run of `ring_by_ring.py`/`rb1_circular_exactness.py`, or my own from-scratch
code in the scratchpad). Rule applied throughout: verify a WIN as hard as a DEFICIT; manufacture neither.
Framework judged on its own terms (dS-Unruh modified INERTIA, ν=√(1+1/y), a₀ FIXED at 9.36e-11 canonical /
1.13e-10 alt; never McGaugh's ν).

---

## 0. Reproduction — PASS
- `ring_by_ring.py` re-run: **exit 0, 7/7 CHECK [PASS]**, every printed number byte-identical to the banked
  `ring_by_ring.out` (diff of all `canonical|alt` result lines: IDENTICAL). Seed-locked bootstrap.
- `rb1_circular_exactness.py` re-run: **exit 0, 15/15 PASS**. MI side is machine-zero algebraic
  (ring residual <1e-12); QUMOND spherical (Plummer) control returns the algebraic law to 1.34e-5
  (solver validated); QUMOND disk deviation max 2.28%.
- Mandatory RAR pre-flight `real_research/rar_framework_a0_mlfit.py` re-run: **exit 0**,
  0.108 dex @ Υ=0.70 (canonical a₀), beats reg-MOND 0.122 @ Υ=0.5. Confirmed before relaying any verdict.

## 1. Independent re-derivation of the zone statistic D — MATCHES
Wrote from-scratch code (own file parsing, own δ=log₁₀g_obs−log₁₀[ν(y)g_bar], own 2.6R_d split, own
1/σ² weighting). Full-sample means:

| footing / Υ | my independent Dbar | banked Dbar | N |
|---|---|---|---|
| canonical, 0.5 | +0.0024 | +0.0024 | 114 |
| canonical, 0.7 | −0.0269 | −0.0269 | 114 |
| alt, 0.5 | +0.0091 | +0.0091 | 114 |
| alt, 0.7 | −0.0194 | −0.0194 | 114 |

Independent per-galaxy D's on 14 random galaxies are individually sensible (range −0.15…+0.12, all-inner
galaxies correctly skipped). **The D statistic reproduces exactly.** Sample = 152 (Chae's count) confirmed.

Independent Chae-style POOLED orthogonal-residual diff (own bootstrap over galaxies, 3000 resamples):
canonical/0.5 −0.0393±0.0146 (**2.7σ**; banked 2.6σ), alt/0.5 −0.0250±0.0148 (**1.7σ**), canonical/0.7
−0.0652±0.0151 (4.3σ). The equal-gal↔precision-weight FLIP reproduces (canonical/0.5: +0.0024 equal vs
−0.0208 precision). **All within bootstrap noise of the banked values — nothing is manufactured.**

## 2. Is the QUMOND template a fair stand-in, or strawmanned? — FAIR (not too small, not too large)
Attacked the Miyamoto–Nagai phantom-density solver three ways:
1. **Solver correctness.** In spherical symmetry QUMOND MUST return the algebraic law; the Plummer control
   does so to 1.3e-5 (rb1). The disk deviation therefore comes purely from the l>0 geometry multipoles,
   not solver error (deviation/error ratio >1700×). Sign is correct: inner suppressed, outer enhanced —
   the established Brada–Milgrom/Chae–Milgrom QUMOND-disk phenomenology.
2. **Magnitude cross-check vs published MG.** The template gives D_MG = −0.024…−0.027 dex. Chae 2022's
   own measured inner−outer offset — which he attributes to AQUAL/MG — is −0.021±0.0045 dex. The template
   lands right on the empirically MG-attributed value. It is **not** inflated (which would manufacture an
   MI win by widening z_MG) nor shrunk (which would manufacture a false discriminant). Literature
   (search 2026-07; Chae & Milgrom 2022, Famaey–Durakovic 2025 review) confirms AQUAL/QUMOND "unambiguously
   predict that the inner part of rotation curves deviate, though by a small amount, from the algebraic
   MOND relation" from disk geometry — the right sign, order, and location.
3. **Systematic bracket is honest.** Thickness B/A=0.1/0.3 and anchor 1.5/3.0R_d span −0.018…−0.032
   (±0.008). The y-collapse mapping (which would wash the signal to −0.002) is transparently EXCLUDED
   with a stated reason (16–84% spread at fixed y ≈ the whole signal; deviation is a function of (R/A,depth),
   not local y). Caveat: QUMOND vs AQUAL differ ~0.1–1% (stated); a minor non-monotonicity in the B/A
   bracket (0.2 gives larger |D| than 0.1) is within the quoted systematic and does not move any verdict.

**Verdict on the template: fair.** The −0.024 dex prediction is corroborated by Chae's own MG-attributed
number and by the QUMOND-disk literature.

## 3. Chae 2022 quoted correctly, and is the 1.7–2.6σ recomputation real? — YES, with one framing correction
- **Chae's numbers, re-fetched (arXiv:2207.11069).** Abstract verbatim confirms "**6.9σ** difference
  between the inner and outer parts on an acceleration plane which would be inconsistent with current
  proposals of modified inertia." v2 body 5.1σ (e-parameter) and orthogonal residuals inner −0.031±0.004,
  outer −0.010±0.002, diff −0.021±0.0045: quoted correctly in RING_RESULTS/PRIOR_ART.
- **The 1.7–2.6σ recomputation is REAL** (independently reproduced above). At fixed a₀ + framework ν the
  pooled inner/outer offset survives at canonical Υ=0.5 (−0.039±0.015, 2.6σ) — same sign as Chae, and
  actually **larger in magnitude** than his −0.021.
- **Framing correction (cuts slightly AGAINST the framework).** RING_RESULTS §4 attributes the 5–7σ→1.7–2.6σ
  drop to "a₀ fixed + framework ν … significance drops ~3×." That is imprecise on the *cause*. The offset
  magnitude is NOT shrunk by the framework (−0.039 > Chae's −0.021); the σ is lower almost entirely because
  this test uses a **conservative galaxy-level bootstrap error (±0.015)** where Chae used **point-level
  standard errors (±0.0045**, i.e. ~√N over ~3000 points). Under Chae's own point-level error the framework's
  larger offset would read *higher* σ, not lower. So the framework does **not dissolve** Chae's pooled signal;
  what yields the MI-consistent null is switching to the **equal-galaxy statistic** (+0.0024). RING_RESULTS
  does expose this decomposition honestly (equal-gal null vs precision-weighted −0.021 = Chae's value, "not
  decidable from SPARC alone"), so the conclusion is sound — but the headline should read "significance under
  a more conservative error model *and* the framework's pre-declared equal-galaxy null statistic," not "the
  framework shrinks Chae's signal."

## 4. The Υ=0.7 MG-lean: genuine framework tension, or artifact? — ARTIFACT-DEGENERATE (not a clean tension)
Milgrom 2023 (arXiv:2310.14334) full text verified verbatim (not just abstract):
- "the correction due to z motion **reduces the value of the predicted rotational speed** relative to that
  predicted by the algebraic relation" (§, Eq. 47 discussion);
- the correction "is **small at large radii, becomes important at small radii, and brings the predicted MI
  velocities closer to those predicted by AQUAL**" (Fig. 2);
- on Chae: Ref.[22] "used for the MI MOND prediction the exact algebraic relation (44). This analysis thus
  **did not test MI MOND**, and would require reevaluation."

Sign analysis: this correction lowers the *predicted* inner V → moves the corrected-MI curve BELOW the bare
algebraic → same sign and same (inner) location as both Chae's measured signal and the QUMOND template.
Therefore a measured D<0 (Υ=0.7: −0.027) is **degenerate three ways**: (a) genuine MG radius-mixing,
(b) the omitted, same-sign, uncomputed noncircular MI correction, (c) simply a higher-than-truth Υ. Because
the correction magnitude is not computed per galaxy, **one cannot attribute Υ=0.7's D=−0.027 to MG over
corrected-MI.** So it is NOT a clean framework tension — and equally NOT a clean MG win. The compute flags
exactly this (verdict 2 + caveats). **Confirmed: the Υ=0.7 lean is an artifact-degenerate, non-diagnostic
result, correctly not scored as a kill.**

## 5. Manufactured-MI-win hunt at Υ=0.5 (as hard as the deficit hunt) — TWO real dents, no fatal one
The MI-favorable reading is "at Υ=0.5, equal-galaxy D≈0 ⇒ data prefer MI-exact." Attacks:

1. **The bare-algebraic MI target D=0 is the most MI-favorable choice, and it may not be the framework's own
   prediction.** The framework's covariant kernel would produce the Milgrom-2023 noncircular correction
   (§4), whose honest prediction is D<0, not 0. If that correction is ~0.01–0.02 dex, then Υ=0.5's +0.0024
   is *above* corrected-MI, i.e. mild tension with corrected-MI too — the "win" exists only because the
   correction was set to zero. Mitigating: cold-gas z-motion is genuinely small (Milgrom), so D=0 is a
   defensible lower bound; magnitude is unknown. Net: the Υ=0.5 "MI win" is a win for *bare-algebraic* MI,
   which the framework itself does not fully endorse. **Real dent, disclosed in the caveats.**
2. **The "win" lives at a Υ the framework's own RAR fit disfavors.** The RAR pre-flight prefers Υ=0.70
   (0.108 dex; Υ=0.50 gives 0.145 dex, +0.100 offset — a poor global fit). The ring-by-ring MI-favorable
   reading requires Υ=0.5; at the framework's *self-consistent* Υ=0.70 the same equal-galaxy statistic
   leans MG (−0.027, 2.5σ from MI-exact). So the MI win sits at a M/L the framework itself doesn't pick.
   Mitigating: once the §4 noncircular correction is admitted (corrected-MI predicts D<0 at all Υ), the
   Υ=0.70 −0.027 could be corrected-MI, dissolving the tension into "undecidable." **Real dent, disclosed
   (verdict 2 names Υ=0.7 as the repo's own best-fit).**
3. **Not a manufactured win via the template** (§2) or via cherry-picked weighting: the equal-galaxy
   statistic is pre-declared as primary in the docstring, is applied symmetrically at both Υ=0.5 and 0.7,
   and the paper openly reports that precision-weighting flips Υ=0.5 to Chae's −0.021. No hidden knob.

**Conclusion of the win-hunt:** the Υ=0.5 MI-consistency is real in the numbers but is (i) bare-algebraic,
not the framework's kernel-corrected prediction, and (ii) at a Υ disfavored by the framework's own RAR.
Both dents are disclosed in RING_RESULTS. It is therefore **not a manufactured win, but it is also not a
clean win** — symmetric with the Υ=0.7 non-clean deficit.

---

## VERDICT
The RING-BY-RING compute is **UPHELD**. Every load-bearing number reproduces (7/7 checks, exit 0, and
independent from-scratch code matches Dbar across all four footings and the pooled/precision statistics).
The QUMOND template is fair (validated solver, magnitude corroborated by Chae's own MG-attributed offset),
Chae's 6.9σ/−0.021±0.0045 are quoted correctly, the framework's 1.7–2.6σ sign-reproduction is real, and the
Milgrom-2023 noncircular-correction quotes are verbatim-accurate.

The compute's own bottom line — **SPARC rotation curves at fixed Υ cannot presently decide between exact
ring-by-ring MI and QUMOND-with-the-same-ν** (discriminant |D_MI−D_MG|≈0.026 dex < the in-hand sliders:
Υ±0.1→∓0.015, weighting→−0.023, split→+0.028, footing→+0.007) — survives adversarial scrutiny. Neither an
MI win nor an MG kill is claimable.

**Two corrections/qualifications for the record (neither flips the verdict):**
- The "5–7σ → 1.7–2.6σ" drop is dominantly the conservative galaxy-level error model + the equal-galaxy
  null statistic, NOT the framework ν shrinking Chae's offset (the pooled offset is −0.039, *larger* than
  his −0.021). The framework does not dissolve Chae's signal; the equal-galaxy weighting choice yields the
  null. (Disclosed in §6 of the compute, but the §4 headline framing overstates the ν/a₀ role.)
- The Υ=0.5 MI-consistency and the Υ=0.7 MG-lean are BOTH non-clean and BOTH degenerate with the uncomputed,
  same-sign Milgrom-2023 noncircular inner correction. The MI-favorable reading additionally sits at Υ=0.5,
  a M/L the framework's own RAR fit disfavors (0.70 preferred). Honest net: undecidable, leaning neither way.

Open item that would make the test diagnostic: compute the framework kernel's noncircular inner correction
per galaxy (Lane RB3) so corrected-MI predicts a specific D≠0 the data can be scored against — until then the
score is against bare-algebraic MI only, which is not the framework's complete prediction.
