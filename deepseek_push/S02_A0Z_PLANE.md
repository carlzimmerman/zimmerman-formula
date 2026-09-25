# S02_A0Z_PLANE — The a₀(z) Cross-Constraint Synthesis

**2026-09-25 · every on-record a₀_eff-vs-epoch measurement on ONE (z, Δlog₁₀ a₀_eff) plane · 8/8 PASS · no git commit**

Sister lane `S02_mightee_mirror` owns the slot file `S02_results.json` (read by
U02/U03) — additive-only rule: it is **not** overwritten. This lane's results live in
`S02_a0z_plane_results.json`; `S02_a0z_plane.py` → `S02_a0z_plane.out`.

All numbers below are recomputed from the cited on-record files (O02, G237 commit
a2e7c821e, N05, O01, G208, M04) — nothing invented; derived quantities are arithmetic
on recorded values with the SE carried through (assumptions A1–A5, §6).

---

## 1. The HeCS translate — the KILL-CANDIDATE's translate (O02 → this lane)

G237 Case A is exact: `T_X(z₂)/T_X(z₁)|_{M_b} = [a₀(z₂)/a₀(z₁)]^{1/2}`, so
**Δlog₁₀ a₀ = 2·Δlog₁₀ T** — both the signal and the SE double:

| quantity | value | source |
|---|---|---|
| Δlog₁₀ T(vir), median-z split, fixed M200 | **+0.0620 ± 0.0198 dex** (jackknife) | O02 C04 |
| → Δlog₁₀ a₀ (Case A translate) | **+0.1240 ± 0.0396 dex** | ×2 (SE 2×0.01981) |
| Δz (arm medians 0.1333 → 0.21705) | 0.0837 (~0.084) | O02 key_numbers |
| **σ-slope α_HeCS** | **+1.4801 ± 0.4731 dex/unit z** (~1.5 ± 0.5/unit z) | 0.1240/0.0837 |
| z vs framework 0.000 | **3.13 SE** | unchanged by the ×2 (O02 C05: 3.128) |
| z vs M-RISE-scaled (+0.0238 dex T ⇒ +0.0477 dex a₀) | **1.93 SE** | O02 C06 (K2 not satisfied) |

Restated: the HeCS gradient translates to **+0.124 ± 0.040 dex of Δlog₁₀ a₀ over
Δz = 0.084**, sitting 3.13 SE from G237's flat 0.000. The SE count is conversion-
invariant — the factor 2 scales signal and error together; the tension is exactly the
on-record one, now expressed in a₀ units. K1 FIRED, K2 NOT satisfied (M-RISE not
excluded); C08's mass-dependent structure (low-edge +0.15 → high-edge ~0 dex) is the
pre-registered LX flux-selection signature → **KILL-CANDIDATE, NOT adjudication**.

## 2. The impossibility leg (registered constraining statement)

If a₀_eff differences were a₀(z) at G237's rate, the numbers are impossible — both in
size and sign:

| reading | arithmetic | implied slope |
|---|---|---|
| MIGHTEE deep: a₀_eff/a₀ = 2.164 at z_med = 0.04426 (N05, G208) | 2.164 = 1 + α·0.044 | **α ≈ +26.3/unit z** (linear) |
| SPARC deep: a₀_eff/a₀ = 0.724 at z ≈ 0 (N05) | 0.724 = 1 + α·z | **α ≈ −6.2/unit z** (ref. 0.044 epoch; **−55/unit z** at its own z ≈ 0.005) |
| SPARC(z≈0) → MIGHTEE(z=0.044): Δlog₁₀ a₀ = +0.476 dex (N05) | over Δz = 0.039 | **+12.1 dex/unit z = 9.3×10⁵ × G237's −1.3×10⁻⁵ dex/unit z** |
| G208 C6 (on record): z-evolution available (G011 at z_med) | +2.19% vs 191.5% needed (2.915×) | **~87× short (~100×)** |

The staircase/sign-mirror **cannot be a redshift effect under G237's law**: the
required between-survey slope is ~10⁶× G237's committed rate, the local SPARC deficit
lives at the z = 0 anchor epoch where no z-law normalized at a₀(0) = 1 can act, and
MIGHTEE violates even M-RISE's growth law at 8.6 SE (its amplitude matches M-RISE only
at z ≈ 0.69 — 15× its actual epoch). HeCS's own +1.48 dex/unit z is ~10⁵× G237's rate,
and even *that* slope can supply only ~0.06 dex across the SPARC→MIGHTEE gap versus the
0.48 dex actually present — i.e. the between-survey spread is ~8× steeper than the
HeCS candidate itself.

**REGISTERED CONSTRAINING STATEMENT:** *if a₀(z) obeys G237, the survey-to-survey a₀_eff
spread is environmental/systematic, and HeCS's low-z candidate (if not selection) is
ALSO too large to be a₀(z) at G237's rate.* An amendment of G237's z-law can at most
absorb the HeCS gradient (~1.5 dex/unit z, if the WG leg adjudicates it real); it
cannot absorb the staircase, which stays environmental by construction.

## 3. THE PLANE (z, Δlog₁₀ a₀_eff)

**Overlay curves (exact amplitudes recovered from the G237 commit files):**
G237 (S3-05): `a₀(z)/a₀(0) = 1 − 3×10⁻⁵ z` → Δlog₁₀ a₀ = −1.303×10⁻⁵ dex/unit z
(the task's "~1e-5/unit z"); M-RISE (Ciocan): `a₀(z)/a₀(0) = 1 + 1.6986 z`
(1.59×10⁻¹⁰ m/s² per z over the canonical 9.3619×10⁻¹¹) → +0.431 dex at z = 1.

| row | z | Δlog₁₀ a₀_eff ± SE | vs G237 | G237 pred | M-RISE pred | vs M-RISE | class |
|---|---|---|---:|---:|---:|---:|---|
| MW(0) anchor | 0.0000 | 0.0000 ± 0.0000 | 0.00 | 0.000e+00 | +0.0000 | 0.00 | BOTH (definitional; a₀(0) anchors the frame, G03C) |
| O01 dwarfs (N=16; g_N<0.2) | ~0 | −0.1955 ± 0.1107 | 1.77 | ~0 | +0.0007 | 1.77 | BOTH (deep tail N=7: −0.509 ± 0.166, robustness only) |
| SPARC deep (1152 rings, 135 gal) | ~0.005 | −0.1402 ± 0.0382 | 3.67 | −6.5e-08 | +0.0037 | 3.77 | NEITHER — z≈0 environmental by construction |
| MIGHTEE deep (72 rings, 18 groups) | 0.04426 | +0.3355 ± 0.0355 | 9.44 | −5.8e-07 | +0.0315 | 8.56 | NEITHER — registered environmental/systematic (G208 C6, G133 M/L collapse 1.87→1.08) |
| HeCS-lo (N=27) | 0.1333 | −0.0620 ± 0.0198 | **3.13** | −1.7e-06 | +0.0886 | **1.93** | G237-inconsistent, selection-flagged; <2 SE from M-RISE |
| HeCS-hi (N=28) | 0.21705 | +0.0620 ± 0.0198 | **3.13** | −2.8e-06 | +0.1363 | **1.93** | (pair stats; A1: only the hi−lo difference is measured) |

SE sources: SPARC — O01's recorded reconstruction of the L06 4.2σ statement
(SE_dex = 0.0382; N05's own z_clustered = −4.17 is the linear-fraction reading);
MIGHTEE — derived from N05's point estimate + reported two-sided z = 6.58
(σ_dex = 0.0355, A3); O01/O02 — as recorded. Note the registered spread of SPARC-deep
estimates themselves (Q02 0.8314 ± 0.0422, O04b 0.7172 ± 0.0593, L06 0.73) — the
z = 0 landscape is internally scattered at the 0.1-dex level, i.e. environmental.

**Classes and verdict:** consistent with **BOTH** laws — MW(0) (by definition) and O01
(1.77/1.77 σ). Consistent with **NEITHER** — SPARC (3.7/3.8 σ) and MIGHTEE
(9.4/8.6 σ); both z≈0 rows, so no z-law can carry them; MIGHTEE overshoots even
M-RISE. The **only z-spaced tension** is HeCS: 3.13 SE from G237-flat, within 2 SE of
the M-RISE-scaled prediction but overshooting it, and selection-flagged (its
mass-dependent structure is the pre-registered LX flux-selection signature).

**Verdict — honest:** *G237's a₀(z) law SURVIVES this plane, but as an UNCONFIRMED
flatness, not a confirmed law.* There is **zero adjudicative z-spaced kill on record**
(0/0 by C7's rule: z ≥ 0.05 ∧ >3 SE ∧ un-flagged). The plane kills nothing: the large
deviations are either z = 0-environmental (SPARC, O01, MIGHTEE — MIGHTEE breaks every
z-law in this plane at >8 SE, so it adjudicates nothing either), or the HeCS gradient,
which is a KILL-**CANDIDATE** pending the WG high-z leg (X-ray/SZ masses, matched
temperatures). If HeCS survives that leg, G237 **needs amendment** — at a rate ≤ ~1.5
dex/unit z, still 10⁵× above its committed −1.3×10⁻⁵ dex/unit z — and the impossibility
leg still bars a₀(z) from carrying the between-survey staircase. No row on this plane
discriminates G237-flat from M-RISE at z < 0.3 with adjudicative power; that is the M04
leg's job.

## 4. The future leg — M04's BLR cosmography (Δlog₁₀ a₀ at z ~ 1–2)

M04 (14/14, M04_results.json): one S/N = 30 BLR object measures J10-I at 3.56% relative
precision (σ_J10I = 0.0356) → per-object 3σ sensitivity on Δlog₁₀ a₀ (a₀ ∝ J10-I²)
**≈ 0.093 dex** (the task's 0.1–0.2 dex bracket, C8), with the 3σ lag floor
6.14 d (6.55 d with atom term) at σ(d̄) = d̄/30 = 2.045 d. Anchor: one object at z = 1
resolves framework vs M-RISE at **11.7σ** (Δd̄ = 24.0 d vs 61.351 d framework lag).

Can it distinguish **G237-flat from the HeCS-translated slope**
(α = 1.48 dex/unit z, extrapolated linearly — assumption A2, a sensitivity yardstick
only)? **Yes — with N = 1, and it is not close:**

| discriminator | value |
|---|---|
| 3σ crossing for one object | **z ≈ 0.062** (lag dev = 6.14 d floor; 0.066 with atom term) |
| one S/N=30 object at z = 1 | lag dev 50.2 d → **~24–25σ** (M04's σ convention, A5; σ evaluated at the model lag: 135σ) — 2.1× the M-RISE anchor signal |
| one pair (z₁ = 0.3, z₂ = 1.0), F-COSMO ratio probe | **4.9σ** (threshold 3·√2/30; ≥3σ for any z₂ ≳ 0.4) |

So the BLR cosmography resolves the two hypotheses at 3σ from **a single object at
z ≳ 0.06–0.1**, or a single pair spanning (0.3, 1.0); at z = 1–2 the separation is
tens of σ. The binding constraint is NOT the probe's sensitivity — it is that the HeCS
gradient is only 3.1σ on its own data and selection-flagged (§1): the BLR leg turns a
true HeCS gradient into a ~25σ, N=1 cosmography disproof of G237-flatness, which is
precisely why the WG adjudication of HeCS matters more than any future instrument.

## 5. What the framework can and cannot absorb — one line each

- **CAN absorb (without amendment):** every >3σ plane deviation that is z≈0 or
  environment-registered (SPARC deep deficit, O01 dwarfs, MIGHTEE's 2.16 — the deep
  tension is an a₀_eff/environment problem, on record at G208/G133/O01/N05).
- **CANNOT absorb (would require amendment):** a *real* HeCS gradient (would need
  ~1.5 dex/unit z, 10⁵× G237's rate, and would then be instantly decisive via M04).
  An amended a₀(z) still **cannot** carry the between-survey staircase (impossibility
  leg: +26/−6 per-unit-z readings, 9.3×10⁵× G237's rate, opposite-signed).

## 6. Assumptions ledger (stated, not hidden)

- **A1** HeCS absolute placement: only the hi−lo difference is measured; the pair is
  displayed centred on the framework 0.000 (midpoint anchored), preserving the
  +0.1240-dex gradient and its SE. Absolute normalization unmeasured.
- **A2** HeCS future-leg extrapolation is **linear** in z, used as a diagnostic
  sensitivity yardstick, NOT a committed law (taken literally it implies a₀ ~ 30× by
  z = 1 — unphysical away from the HeCS band).
- **A3** MIGHTEE SE_dex = 0.0355 derived from N05's point estimate (fraction +1.1638)
  and its reported two-sided z = 6.58 (ring SE; the S02_results.json colour-group SE is
  smaller and not used).
- **A4** Epochs: SPARC z ≈ 0.005 (task band 0.001–0.01); O01 dwarfs z ≈ 0 (within
  ~10 Mpc); MW(0) definitional 0.000 ± 0.000.
- **A5** BLR σ evaluated at the framework expectation d̄ = 61.351 d (M04's own
  convention).

## 7. Files & status

- `S02_a0z_plane.py` (lane, re-runnable; 8/8 PASS, `S02_A0Z_PLANE COMPLETE: 8/8 checks PASS.`)
- `S02_a0z_plane.out`, `S02_a0z_plane_results.json`
- `S02_A0Z_PLANE.md` (this file)
- **No git commit** (per instruction). `S02_results.json` untouched (additive-only;
  belongs to S02_mightee_mirror).
- Sources: O02_results.json; G237 commit a2e7c821e (README/G237_results.json/
  G237_eRASS3_zlaw.py); N05_results.json; O01_results.json; G208_results.json;
  M04_results.json + M04_J10Z_COSMOGRAPHY.md.