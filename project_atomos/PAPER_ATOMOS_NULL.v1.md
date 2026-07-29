# When Is a Numerological Search Finished? An Exhaustive Null to Depth 10, and a Depth Ceiling That Explains Why Deeper Cannot Help

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC*

*Draft 2026-07-28. Local-only working document. All numbers are printed by committed scripts in this
repository; script names are given per section.*

---

## Abstract

Searches for closed-form expressions reproducing Standard-Model dimensionless constants are common and
almost never conclude: a null is reported as "we did not find one," which is not a statement about the
space. We do two things about that, for one concrete search.

**First, a worked exhaustive null.** For a modified-inertia gravity framework whose acceleration scale
is tied to the cosmological constant, `a0 = cH_Lambda/Z` with `Z = sqrt(32pi/3)`, we exhaustively
enumerate every dimensionless value constructible at depth <= 10 from the framework's two forced germs —
the generation count `3` and the kernel germ `sqrt(8pi/3)` — and confront all of them with 19 measured
SM targets through three gates (germ content, cross-sector interlock, and false-discovery control).
Result: **42,534,139 distinct values, 82,613 in-window hits, ZERO surviving the gate.** Depths 3–9 were
already exhaustive clean nulls; depth 10 extends the proven-empty range and is the first depth past 9
where the word *exhaustive* applies rather than *sampled*.

**Second, a depth ceiling.** The diagnostic is not the null itself but *where the hits land*: hit count
tracks measurement-window width and nothing else. The six most precisely measured targets return
**exactly zero** hits across 42.5 million values; the loosely measured neutrino mixing angles return
15,000–26,000. Formalising that, a constructive enumeration whose candidate count grows as `B^(D-D0)`
exhausts any *fixed* measurement precision `w` at a computable depth,

    D_max  =  D0 + ln(1/w) / ln(B) ,

beyond which a single-target match is expected by chance and therefore carries no information however
many digits it displays. For this vocabulary (`B = 30`, `D0 = 4`) the ceiling is **D = 10.4 for
1/alpha** and **D = 13.1 for m_p/m_e**, the most precisely measured ratio in physics. Depth 18 sampling
— which we also ran — was statistically empty *by construction*. All discriminating power at depth must
therefore come from *simultaneous* matching across independent sectors, with a threshold in bits:
`SUM_i log2(1/w_i) > log2(N(D)) + margin`. Counting interlocked targets is the wrong statistic; three
loosely measured targets carry 24.7 bits where two tight ones carry 76.3.

**What is not claimed.** The look-elsewhere/multiple-comparisons argument is standard (Gross & Vitells
2010); nothing here is new statistics. The contribution is its quantitative instantiation as a *depth*
ceiling for constructive-enumeration searches, plus a worked exhaustive null. The null is about one
germ vocabulary at one depth under one gate — it is not a statement about numerology in general, and
not evidence for or against the framework whose germs it uses. We also report an error of our own: the
naive expected-count model `N*2w` **overestimates observed hits by ~100x** because the value set
clusters rather than distributing uniformly, so our own bits thresholds should be read as conservative
rather than exact.

---

## 1. What was searched, and what "forced" means

The framework supplies exactly two germs and one free O(1) coefficient:

| germ | origin in the framework |
|---|---|
| `3` | the generation count |
| `sqrt(8pi/3)` | the kernel germ, half of `Z = sqrt(32pi/3)` |

"Forced" is load-bearing and is what makes the search falsifiable rather than open-ended. A candidate
expression must *contain* the germs (Gate B); it is not enough to be some function of pi and small
integers. Without that requirement the space is unbounded and no null means anything.

Expressions are built by constructive enumeration: a base leaf followed by `D-4` steps from a fixed
30-entry menu (leaf append with MUL/DIV, five power exponents, three unaries), decorated by canonical
germ recipes. Candidate count therefore grows as `11 * 30^(D-4)`. Value-identical expressions are
deduplicated at mpmath precision, so the object counted is *distinct values*, not distinct formulas.

**Targets.** 19 measured dimensionless SM quantities, spanning eleven orders of magnitude in relative
precision — from `m_p/m_e` at 1.7e-11 to the PMNS mixing angles at ~6e-2. Two further targets
(`koide_Q_lep`, `r_tau_mu`) were **held back** and never entered the search; §6.

## 2. The exhaustive null at depth <= 10

`sharded_build.py`, `sweep_depth.py`, `NULL_RESULT_DEPTH10_EXHAUSTIVE.md`.

```
raw candidates enumerated : 174,890,804
distinct values           :  42,534,139
targets swept             :          19   (held-back pair excluded)
in-window hits            :      82,613
CERTIFIED (gate-passing)  :           0
RE-LABELED                :           0
```

Depths 3–9 are exhaustive clean nulls under the same machinery. Depth 10 was previously attempted and
abandoned partway; §7 describes what made it tractable.

## 3. The hit distribution is the result, not the null

| target | rel. window | hits |
|---|---|---|
| `m_p/m_e`, `a_e`, `1/alpha`, `m_n/m_p` | 1.7e-11 – 1.5e-10 | **0** |
| `m_mu/m_e`, `a_mu` | 2.2e-8 – 4.0e-7 | **0** |
| `r_tau_e`, `1/alpha(M_Z)`, `sin^2 theta_W` | 7e-5 – 1.7e-4 | 28 / 50 / 72 |
| `koide_Q_up`, `higgs_lambda`, `ckm_lambda`, `koide_Q_down` | 2e-3 – 5e-3 | 838 / 1130 / 2121 / 2098 |
| `r_b_tau`, `r_t_b`, `alpha_s(M_Z)` | 7.6e-3 – 1.1e-2 | 4747 / 4443 / 4933 |
| `pmns_sin2_13/12/23` | 3.5e-2 – 6e-2 | 15212 / 26142 / 20799 |

Hit count is a monotone function of window width and of nothing else. The six most precisely measured
quantities in the set return **zero** hits across 42.5 million values; the least precisely measured
return tens of thousands. Every one of the 82,613 died in the FDR gate. This is what chance looks like
when it is drawn to scale, and it is a far more informative statement than "we found nothing."

## 4. The depth ceiling

`GATE_POWER_ANALYSIS.py`, `BITS_RULE.py`.

With `N(D)` candidates and a target of relative window `w`, the expected number of chance matches is
`N(D)*w`; a hit is informative only when that is well below 1. Solving `N(D)*w = 1` for `D` with
`N(D) = B^(D-D0)` gives the ceiling quoted in the abstract. For `B = 30`, `D0 = 4`:

| target | rel. window | informative ceiling | expected chance hits at D=18 |
|---|---|---|---|
| `1/alpha` | 3.1e-10 | **D = 10.4** | 1.5e+11 |
| `m_p/m_e` | 3.5e-14 | **D = 13.1** | 1.7e+07 |
| `alpha_s(M_Z)` | 1.5e-2 | D = 5.2 | — |

Two consequences.

**(a) Deeper is worse, not better.** Each additional depth costs `log2(B) = 4.9` bits of look-elsewhere
for nothing, while available target precision is fixed. Depth 18 costs 68.7 bits; the two most
precisely measured numbers in physics supply 76.3 between them, which does not clear it. Our own
depth-10–18 sampling campaign (1,059 passes, ~29,000 in-window hits, zero survivors) was therefore
incapable of establishing a single-target result *by construction* — a fact we did not appreciate until
after running it.

**(b) Interlock, weighted by bits.** Requiring one expression to match `k` targets simultaneously
multiplies the windows, so bits add. But *counting* targets is the wrong statistic: three loose targets
give 24.7 bits, two tight ones 76.3. The threshold is
`SUM_i log2(1/w_i) > log2(N(D)) + margin`, over targets a search is permitted to fit.

## 5. Why nothing was there — four independent structural obstructions

These were established separately and each would stand without the search:

1. **Number field.** `Z` carries a transcendental `sqrt(pi)`; the flavour and coupling data are
   algebraic. An exact identity therefore requires the `sqrt(pi)` to cancel, in which case the germ was
   not load-bearing.
2. **Period ring.** Half-integer versus integer weight, with the weight-1 slot empty — the two rings
   are disjoint exactly where a bridge would have to live.
3. **Dictionary/category.** `u = a0/g` is an acceleration *ratio*; a renormalisation scale is an
   *energy*. The only dimensional bridge, `a0/2c` with hbar and c, lands ~38 orders below the electron.
4. **Varying constants — the one experimental closure.** If any SM constant tracked the dark-energy
   density as strongly as `a0` does, atomic clocks would have seen it; the coupling is bounded to
   `|p| <= 6e-8`.

Four structural arguments plus the depth 3–9 nulls plus this depth-10 null plus a separate audit of a
`12pi`-based alpha coincidence make seven independent lines reaching the same place.

## 6. Method: a held-back validation set, and why one of them is nearly worthless

`targets/pdg_constants.py` (`HOLDOUT_KEYS`).

A search that iterates until a gate passes is fitting to the gate. Two targets are therefore excluded
from every search pool: `koide_Q_lep` (tight, rel ~1e-5) and `r_tau_mu` (loose, ~1e-4). A survivor
would have to *predict* them.

**Reported against interest:** the tight one is nearly worthless as a holdout. Measured
`koide_Q_lep = 0.666660511 +/- 6.8e-6` sits **0.91 sigma** from exact `2/3` — an answer known since
Koide (1981). A survivor landing on `2/3` passes while predicting nothing new. `r_tau_mu` has no famous
closed form and is therefore the stronger test despite being the looser one. Any holdout whose answer
is already in the literature measures nothing.

## 7. Method: what made depth 10 tractable, and three bugs the guards caught

Depth 10's cost is concentrated in a single budget split whose skeleton layer enumerates
**8,019,000,000** step sequences at ~90,000/s — about 25 hours — and which collapses to only **22,708**
distinct skeletons. Sharding the *search* alone does not help, because every shard rebuilds that same
layer; the layer itself had to be parallelised and cached (`parallel_skeleton_layer.py`). With it
cached, the depth-10 build runs in ~15 minutes.

Three bugs in the new code were caught by consistency guards rather than by inspection, and are
recorded because the guards are the reason the null is trustworthy:

1. **A merge that re-keyed float64** silently discarded 19% of depth 8's distinct values. Caught by
   requiring the sharded path to reproduce the committed serial counts *exactly* before being pointed
   at new depth.
2. **Shard-local record indices** made the hit records disagree with the merged value array. Caught by
   an existing `REBUILD MISMATCH` assertion in the committed sweep. Without it the null would have been
   computed against misaligned records.
3. **A holdout leak**: two hard-coded target lists re-added `koide_Q_lep` by name after the
   dataset-level exclusion, so the search was fitting a target documented as held back.

A fourth, in the opposite direction: applying the holdout filter unconditionally *broke the replay
gate*, which must sweep the full historical target list to reproduce committed ground truth. A replay
is a machinery check, not a search, and needs the holdout included. Suppressing a guard to satisfy a
methodological rule is its own failure mode.

## 8. What this does and does not establish

**Does.** No expression built from these two forced germs at depth <= 10 matches any of 19 SM targets
with surplus information over chance, exhaustively. And: single-target matching in searches of this
form is uninformative past a computable depth, so most such searches cannot conclude anything even in
principle.

**Does not.** Say anything about depth 11+ (~13.5 days sharded) or 12 (~16 days) — and per §4 those
depths could not carry a single-target result anyway. Say anything about other germ vocabularies. Bear
on the framework whose germs were used: its acceleration scale, the constant `Z`, the response sign,
and the gate frequency remain postulated, not derived, and this search neither supports nor damages
them. Constitute new statistics: the look-elsewhere argument is standard, and our own instantiation of
it was quantitatively wrong by ~100x until measured empirically (abstract).

**Honest scale.** This is one increment on a wall that already had six supports, obtained at
substantial engineering cost, in a search whose prior was low and remains low. Its value is that it
*closes* rather than *leaves ajar*: the range 3–10 is now proven empty rather than unexamined, and the
ceiling says where examining further stops meaning anything.

---

## References

Gross, E. & Vitells, O. 2010, *Eur. Phys. J. C* **70**, 525 — trial factors / the look-elsewhere effect.
Koide, Y. 1981 — the charged-lepton mass relation `Q = 2/3`.
Milgrom, M. 1999, *Phys. Lett. A* **253**, 273 — the kernel and identity the framework's germ derives from.
Wilczek, F. — *Scaling Mount Planck*, Physics Today (dimensional-analysis numerology, context).
