# L86 — Is the dust=DM BBN fine-tuning FATAL, BENIGN, or REMOVABLE?

**Script:** `L86_fine_tuning_assessment.py` · **Output:** `L86_fine_tuning_assessment.out` · **Result:** 16/16 checks PASS
(each PASS = the stated claim is TRUE). Self-contained sympy/numpy; imports nothing from `qwen_claude_field_theory/`.
Controls first (including a faithful reproduction of L84's `|C|/|A|` bound). Both a₀ footings on every dimensional
number — a₀ is absent from the FLRW/tuning sector, so both give bit-identical numbers (demonstrated, check **FOOT**).

## Verdict — one line

**GENUINE FINE-TUNING, NOT REMOVABLE from the action as it stands.** Not *fatal* (no hard theorem kill — BBN is
satisfied *at* the tuned point, so the theory is unnatural, not excluded); not *benign* (one **extra ~24-order-of-magnitude
hierarchy** beyond ΛCDM's freedom, tuned along an *unstable* direction); not *removable* (every escape either relocates
the tuning at ~1:1 severity or deletes the dark matter). This is a real naturalness liability recorded honestly — a
**cost**, not a clean kill.

## The setup (reproduced faithfully first — check C0)

astra's F(Q)Θ affine action gives, on flat FLRW, `ρ = B + 3M²H² − (M²/3f²)(A + C/a³)²`, which expands to

```
ρ = [ B − M²A²/(3f²) ]        ← Λ-like constant   (DARK ENERGY)
    + 3 M² H²                  ← gravitational back-reaction
    − (2 M² A C)/(3f²) · a⁻³    ← DUST cross term    (the DARK MATTER, w=0)      [L81/L82]
    − (M² C²)/(3f²)   · a⁻⁶    ← STIFF term          (w=1, NEGATIVE)             [L84]
```

`C = a³(−K_Q + 3H F_Q)` is the shift-symmetric conserved Noether charge (L81). **Control C1** reproduces L84 exactly:
BBN/N_eff crushes the stiff piece to `Ω_stiff,0 ≲ 4.1×10⁻²⁵`, and because the *same* charge sources dust (∝ A·C) and
stiff (∝ C²), the split today is `Ω_stiff,0/Ω_dust,0 = |C|/(2|A|)` — so dust=DM (`Ω_dust,0 ≈ 0.264`) forces
**`|C|/|A| ≲ 3.1×10⁻²⁴`**, a ~24-order hierarchy at fixed product `|A·C|`.

## Q1 — Is it genuinely worse than ΛCDM? **Yes, by one ~24-order tuning.** (checks Q1a, Q1b)

- **ΛCDM (this sector):** two unexplained relic/IC numbers — `Ω_Λ` and `Ω_dm` — **neither tuned against a pathology**.
- **F(Q)Θ affine:** fixes the *same* two (`Ω_Λ ↔ B − M²A²/3f²`; `Ω_dm ↔` product `|A·C|`) **plus** the BBN-forced ratio
  `|C|/|A| ≲ 3×10⁻²⁴`. That ratio is the genuinely **extra** constraint, and it lies along an **unstable direction**:
  natural `|C| ~ |A|` overshoots the BBN radiation budget by >20 orders (L84 F2). So it is one *more* fine-tuning than
  ΛCDM, and a worse *kind* (avoiding a pathology, not a free relic choice).
- **Honest mitigation (Q1b), and why it does not dissolve the cost:** `C` is a *conserved Noether charge* = an
  integration constant (initial data), so its smallness can be framed as an initial-condition choice rather than a
  Lagrangian tuning. But (i) being **exactly conserved, it cannot dynamically relax** to a small value (no attractor /
  relaxion route), and (ii) hitting `Ω_dm` at small `C` forces the **coefficient `A` large**, which *is* a Lagrangian
  tuning (Q2). The "just initial data" framing softens the language; it does not remove the cost.

## Q2 — Protection mechanism? **No. Large A relocates the tuning; it does not remove it.** (checks Q2a–Q2d)

- **Q2a — no escape via M, f.** `Ω_stiff/Ω_dust = |C|/(2|A|)` is **independent of M and f** (both densities carry the
  same `M²/3f²`), so the gravitational scale and the affine slope cannot touch the ratio. The only lever is `A`, `C`.
- **Large A is *allowed* by the structure:** the affine degeneracy fixes the **quadratic** coefficient `k₂ = 3f²/4M²`
  (`K_QQ = 2k₂`), which is **A-blind** (check C2 — `A` is the *linear* coefficient); and the background positivity is
  A-blind too — `ρ_bare = K − Q K_Q = B − k₂Q²`, with the linear term cancelling (check C3, witness `ρ_bare = 3/2`).
  So neither the degeneracy nor background positivity forbids large `|A|`.
- **Q2b [KEY] — but large A moves the tuning into the cosmological-constant sector, at ~1:1 severity.** Taking `|A|`
  large (at fixed product `|A·C| = Ω_dm`) drives the `A²` piece of the Λ-like constant, `M²A²/(3f²)`, to `≳10²² ×` the DM
  density, so `B` must **cancel** it to fractional precision
  ```
  δ_CC = Ω_Λ/Ω_{A²} = 2 (Ω_Λ/Ω_dm) · (|C|/|A|) ≲ 1.6×10⁻²³ ,
  ```
  which is **proportional to `|C|/|A|`** (ratio ≈ 5): the same ~23-order fine-tuning, relocated from the (C,A) sector to
  the (B, A²) cosmological-constant cancellation. Not removed — moved.
- **Q2c — large A also aggravates the open health warning.** The decoupling sound speed `c_bare² = K_Q/(Q K_QQ) =
  1 + A/(2k₂Q)` depends on `A` (witness `A=−3 ⇒ c_bare² = −1`, astra's flagged value); `|A| → ∞` drives `|c_bare²| → ∞`,
  pushing the diagnostic *further* from a healthy O(1) value. This is the *decoupling* limit — non-decisive per astra
  (the deciding test is the full ADM Dirac/eigenanalysis) — so it is a **secondary** concern, not a kill; but it means
  large `A` does not come free on the health side either.
- **Q2d — no symmetry caps C/A.** The shift symmetry `φ→φ+const` makes `C` *conserved* but leaves its **value** as free
  initial data; there is no scaling symmetry relating the coefficient `A` to the charge `C`; and conservation forbids
  dynamical relaxation. The smallness is **unprotected** (reaffirms and sharpens L84 F3).

## Q3 — Does the tuning-free A=0 corner have any other dark-matter route? **No.** (checks Q3a–Q3e)

Setting `A=0` kills the `a⁻³` dust identically (Q3a) and leaves only `B + 3M²H² − (M²C²/3f²)a⁻⁶`. None of the survivors
is cosmological dark matter:

- **B** — a constant, `w=−1` dark energy: does **not** cluster (Q3c).
- **3M²H²** — gravitational back-reaction (a piece of the Friedmann LHS), not an independent source.
- **stiff `−C²/a⁶`** — `w=+1`, **negative-energy**, dilutes faster than radiation, negligible today, no matter-like
  clustering (Q3c).
- **No higher term is available:** the affine degeneracy forces `K_QQ = const`, so any cubic `k₃Q³` needs `k₃=0` —
  **K is capped at quadratic**, and the only background scalings from the scalar sector are `{const, a⁻³, a⁻⁶}` (Q3b).
- **The MOND term is absent from the background:** `V_μ = q_μ^ν∂_νφ` is the spatial/transverse gradient, `=0` by
  homogeneity, and `G(0) = 0` exactly (Q3d). It is the *galactic* "apparent DM" of rotation curves — not a cosmological
  `a⁻³ Ω_dm` source.

**Therefore (Q3e): the theory is *forced* into `A≠0` — the tuned corner — to have cosmological dark matter.** There is
no tuning-free corner that also contains dark matter.

## Confidence

- **HIGH** on the algebra: the CC relocation `δ_CC ∝ |C|/|A|` (exact), the A-blindness of the degeneracy and background,
  the A=0 no-DM result (with the degeneracy forbidding higher terms and the MOND term vanishing on the background), and
  the absence of a protecting symmetry are all exact sympy statements.
- **MEDIUM** on the "worse than ΛCDM" characterization *as a naturalness judgment* — the "C is initial data" framing has
  limited but real force, and naturalness is not a falsification. The theory is not excluded; it is unnatural.

**Bottom line.** astra's F(Q)Θ dust=DM route survives BBN only at a ~24-order fine-tuning that the action can neither
remove nor protect — one extra tuning beyond ΛCDM, relocatable into the cosmological-constant sector but not eliminable,
with the A=0 escape closed because it has no dark matter. A genuine cost, honestly recorded; not a clean kill.
