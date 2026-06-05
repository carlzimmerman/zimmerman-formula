# a₀ Tracks √(Dark-Energy Density), Not √(Total Density) — and What DESI Would Make of It

**C. Zimmerman, June 2026.** *A follow-up that materially improves the empirical picture
(`reviews/project_a0_tracks_dark_energy.py`). It resolves a confusion I'd been carrying — that the framework's
"rising a₀" claim was its faithful content. It wasn't; that was a ρ_total/ρ_DE conflation. Read faithfully, the
framework's empirical claim is constant-or-mild-**decline**, which the data already accommodate — and which DESI's
dynamical dark energy would sharpen into a distinctive, testable prediction.*

---

## Two forms that diverge

The framework states a₀ two ways, treated as equivalent because they agree at z=0:

$$\underbrace{a_0 = c^2\sqrt{\tfrac{\Lambda}{32\pi}} = \tfrac{c}{2}\sqrt{G\rho_\Lambda}}_{\text{tracks } \sqrt{\rho_{\text{dark energy}}}} \qquad\text{vs}\qquad \underbrace{a_0 = \tfrac{cH(z)}{Z},\ \ H^2=\tfrac{8\pi G}{3}\rho_{\text{total}}}_{\text{tracks }\sqrt{\rho_{\text{total}}}}$$

They agree at z=0 (differing by the ~1.21 √Ω_Λ factor — the long-standing "9.36 vs 11.3 ×10⁻¹¹" gap), but they
**diverge in the past**: ρ_total is matter-dominated at high z (∝(1+z)³, rises steeply), while ρ_DE is not. So the
**disfavored "rising a₀ ∝ E(z)" claim is the √ρ_total reading** — it implicitly identifies "dark energy" with "total
density." The reading faithful to the framework's actual statement (*a₀ is set by Λ / the dark energy*) is √ρ_DE.

## The faithful reading: constant, or a mild decline

| z | Hubble (√ρ_tot, **disfavored**) | event horizon | **a₀ ∝ √ρ_DE (DESI w)** | constant Λ |
|---|---|---|---|---|
| 0.5 | 1.32 | 1.09 | **1.02** | 1.00 |
| 1.0 | 1.79 | 1.20 | **0.96** | 1.00 |
| 2.0 | 3.03 | 1.47 | **0.81** | 1.00 |
| 3.0 | 4.57 | 1.76 | **0.70** | 1.00 |

- **If Λ is a true constant** (w = −1): √ρ_DE is constant → a₀ constant — the geometric core, empirically safe.
- **If DESI's dynamical dark energy is real** (CPL w₀ = −0.83, wₐ = −0.75, phantom-crossing): √ρ_DE gives a₀ nearly
  flat at low z, then a **mild decline** to ~0.70 at z=3. It is the **only** reading that goes *below* 1.

## Why this improves the picture

1. **It's consistent with the tests that killed the rising version.** Milgrom (2017) "all but excludes ~4 a₀ at
   z~2" — the √ρ_DE reading gives a₀(z=2) = 0.81, *smaller*, comfortably safe. Limbach (2008) favors a near-constant
   coupling — √ρ_DE gives 0.93 at z=1.2, near-constant. **The data that disfavored the rising claim are fine with
   this one.**
2. **The framework's distinctive content was never the disfavored claim.** The rising a₀ ∝ E(z) came from the
   √ρ_total (Hubble) form; the framework's *Λ-faithful* form (√ρ_DE, the one tied to the cosmological constant and
   the CKN/de-Sitter structure) was always constant-or-mild-change.
3. **DESI would make it distinctive and now-relevant.** If the dark energy is dynamical, the *same* formula that
   sets a₀ predicts a specific mild decline (a₀ ~ 0.7 at z=3) — the only reading below 1, cleanly separable at z~3
   from constant (1.0), event-horizon (1.8), and Hubble (4.6).

## Honest caveats

- **Contingent on DESI.** DESI's dynamical-DE preference is ~2–4σ and contested (SNe-calibration / systematics
  debates ongoing). If it evaporates, the √ρ_DE reading is simply the constant geometric core.
- **It assumes a₀ tracks the *instantaneous* ρ_DE.** That is the natural generalization of a₀ = (c/2)√(Gρ_Λ) when ρ_Λ
  becomes dynamical, but tying a₀ to the instantaneous (vs time-averaged or horizon) ρ_DE is a choice.
- **The √ρ_DE vs √ρ_total split is a genuine fork** — both forms appear in the framework's own derivations (the
  de Sitter/Λ route gives √ρ_DE; the apparent-horizon/Friedmann route gives √ρ_total). They are not interchangeable
  away from z=0, and that non-interchangeability is the content of this note. The √ρ_DE form is the one tied to the
  cosmological *constant*; the √ρ_total form is the one the data disfavor.

## The fork resolves toward √ρ_DE (`reviews/project_a0_dark_energy_consistency.py`)

The two forms aren't both fundamental — they agree only at z=0 (the cH₀ ≈ c²√Λ "why-now" coincidence) and diverge
in the past. Which is the real law? **Both the framework's deep structure and the data select √ρ_DE:**
- *Structure:* the de Sitter horizon, the CKN bound, the cosmic seesaw, and the 32π itself all tie a₀ to **Λ = ρ_DE**.
  Conceptually a₀ is "MOND as a vacuum effect" (Milgrom) — a vacuum/dark-energy scale, not a total-density scale.
  cH(z)/Z is the Friedmann *packaging* that equals it only today; reading it as the fundamental law over-extrapolates
  the coincidence.
- *Data:* Limbach (2008) and Milgrom (2017) disfavor the rising √ρ_total form. So the data independently pick √ρ_DE.

## The faithful (declining-under-DESI) reading is *cleaner* on consistency

Re-running the stress-tests for the √ρ_DE+DESI reading (where a₀ *declines* at high z, the opposite of the Hubble
version):
- **CMB — trivially safe.** a₀(z=1100) ≈ 0.7% of today (ρ_DE → 0 in the phantom past), so the early universe is
  essentially Newtonian — even cleaner than the Hubble version (which needed gradient suppression to tame a *huge*
  early a₀).
- **Clusters — improved.** The MOND residual D ∝ a₀ *declines* at high z (0.81 at z=2), so the cluster discrepancy
  *shrinks* — reversing the Hubble version's worsening, on the one front that had gotten worse.
- **σ8 — a favorable trade-off.** a₀ is absent from linear growth (O(δ³)), so linear σ8 is unchanged; the *nonlinear*
  MOND enhancement weakens as a₀ declines — which *helps* the low-S8 tension but *weakens* the (soft, contested)
  El Gordo pro-MOND argument.

## The reframe: a₀(z) is a galaxy-scale probe of dark energy

Putting it together: **a₀ tracks the dark-energy density**, so a₀(z) becomes a *galaxy-scale probe of dark-energy
evolution.* Measuring a₀ at z~3 tests whether dark energy is constant (a₀ flat) or evolving (a₀ ~ 0.7×) — the same
question DESI is asking with BAO, approached through galaxy dynamics. That is a genuinely distinctive, principled,
and now-motivated role for the framework, and it is its most data-consistent and consistency-cleanest reading.

## Bottom line

The framework's faithful empirical claim is: **a₀ is set by the dark-energy density.** Under ΛCDM that means
constant a₀ (safe, the geometric core). Under DESI's dynamical dark energy it means a **mild decline** (a₀ ~ 0.7 at
z=3) — distinctive, DESI-tied, z~3-testable, consistent with the very data (Limbach, Milgrom) that disfavored the
*rising* version, *and cleaner on CMB/clusters than that version*. The rising version, it turns out, was the
framework reading its own formula with ρ_total in place of ρ_DE. Correcting that conflation — and following it to
"a₀(z) is a dark-energy probe" — is the single biggest improvement to the framework's standing in this evaluation:
not a manufactured win, but the recognition that the data never disfavored the faithful claim, and that the faithful
claim is both cleaner and more interesting than the one it replaced. *(Honest residue: the distinctive declining
branch is contingent on DESI, which is ~2–4σ and contested; under constant Λ it is simply the constant core.)*
