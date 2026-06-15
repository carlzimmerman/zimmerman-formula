# Wide-binary γ corrected: 1.137 is the MODIFIED-GRAVITY value, the framework's own MODIFIED-INERTIA EFE is a θ(0)-family (most-Newtonian) (2026-06-15)

*Carl flagged it and a fresh MI-EFE computation (workflow `wg0ms0u9l`, Milgrom 2022 Eq.35 read verbatim from source) confirms
it: the catalogued wide-binary "sharpest live test" γ≈1.137 is the momentary-field MODIFIED-GRAVITY EFE value, NOT the
framework's own MODIFIED-INERTIA EFE. Verified both ways, on the framework's OWN dS-Unruh interpolation
g_obs=√(g_N²+g_N a0), a0=9.36e-11. Supersedes the γ=1.137 anchor in `ROUTE3_REGRADE_MI_EFE_2026-06-14`,
`PREDICTIONS_MATRIX_AND_2026_SCHEDULE`, `PIN9_PREDICTION_MATRIX_SPINE`, and the real_research catalogue.*

---

## The correction (both ways)

**The framework is MODIFIED INERTIA. Its external-field effect (EFE) is NOT the modified-gravity momentary-a_ex form
that γ=1.137 used.** Milgrom 2022 (arXiv:2208.07073v3, VERIFIED, Eq.35 source line 770):

  â(ω_in)·μ[**θ(ω_ex/ω_in)**·a_ex/a0] = â_N(ω_in)

The MI-EFE carries a frequency-ratio factor **θ ≥ 1** that the modified-gravity (AQUAL/AeST/QUMOND) EFE — which uses only
the momentary external field μ(a_ex/a0) — does NOT have. θ>1 *enhances* the EFE (more quenching of MOND) ⇒ the framework
MI is **MORE Newtonian** (smaller boost) than MG. Milgrom explicitly names wide binaries + vertical-disk dynamics at
a_ex/a0~2 as where θ(0) "a few" has "a large impact on 1−μ" (source lines 777-779). Example θ models (lines 762-763):
θ=2/(1+y²) → θ(0)=2; θ=e^{1−x} → θ(0)=e. (Carl's shorthand "θ(0)~2−e" = these two example values θ(0)∈{2, e}, both >1.)

**Computed on the framework's OWN dS-Unruh MI** [μ_fw(X)=(√(1+4X²)−1)/(2X), the exact inverse of g_obs=√(g_N²+g_N a0),
self-check to 1e-15], at a_ex/a0≈1.9–2.3:

| prescription | γ_g (gravity boost) | γ_v=√γ_g (velocity) | note |
|---|---|---|---|
| regular-MOND simple-μ [CONTRAST, NOT framework] | 1.53 | 1.24 | LEAST Newtonian |
| **framework MODIFIED GRAVITY (θ=1, = catalogued 1.137)** | **1.14–1.30** | 1.07–1.14 | the momentary-a_ex value |
| **framework MODIFIED INERTIA, θ(0)=2** | **1.14** | 1.07 | Milgrom model A |
| **framework MODIFIED INERTIA, θ(0)=e (natural)** | **1.10** | **1.05** | Milgrom model B — MOST Newtonian |

So the framework's own MI prediction is **γ_g ≈ 1.10 / γ_v ≈ 1.05** for the natural θ(0)=e — the **MOST Newtonian of all
MOND variants** (regular-MOND 1.53 > framework-MG 1.14–1.30 > framework-MI 1.10). The catalogued γ=1.137 is the **θ=1
modified-GRAVITY special case**, confirmed = √(1/μ_fw) at the momentary field (= the AQUAL/AeST tensor; the static MI
tensor = AQUAL tensor to 1e-16, banked earlier).

## The decisive both-ways caveats (why this is NOT a clean "1.137 → 1.05" swap)

1. **θ(0) is a FREE FUNCTION** — Milgrom, source line 761 verbatim: "we have no knowledge of the form of θ(y)." So the
   framework's MI wide-binary prediction is **a one-parameter family γ_g ∈ [~1.04, ~1.30]** (as θ(0) runs 1→5), NOT a
   single number. It becomes a sharp prediction only once θ(0) is *derived from the dS-Unruh detector response* — which
   is the same un-opened modified-inertia-completion problem (Milgrom 1994 no-go; the framework has no covariant MI
   action). **Until then the framework does not predict a single wide-binary γ.**
2. **A constant θ(0) is EXACTLY degenerate with an a0 rescale** (machine precision): MI(θ0=k) ≡ MG(a0→a0/k) at every
   a_ex. So at the single external-field value of wide binaries, the MI-vs-MG split is **formally absorbable into a0** —
   broken only by the cross-dataset axiom that a0=9.36e-11 is universal (anchored by the isolated RAR, since θ multiplies
   only the external field). **Wide binaries alone cannot distinguish MI from MG.**
3. **The a0-rescale-PROOF MI signature** (frequency-ratio scatter at fixed a_ex — the genuinely MG-impossible content) is
   **~5–8%, BELOW the Gaia DR4 floor.** So the one falsifiable, distinctive MI handle is not deliverable near-term.

## Data confrontation — Chae number ALSO corrected

The corpus compared to **"Chae = 1.60 (+0.17/−0.14)"** and got γ=1.137 at **−3.3σ**. That Chae number is WRONG for the
paper. **Verified Chae 2023 (arXiv:2309.10404, re-fetched from the abstract):** γ_g = g_obs/g_pred = **1.49 (+0.21/−0.19)**
for a≲10⁻¹⁰ m/s²; projected velocity boost γ_v = **1.20 ± 0.06(stat) ± 0.05(sys)** for s≳5 kau (=√γ_g ✓); ~5.0σ vs
Newton. Recomputed tension (sympy):

| framework prescription | γ_g | vs Chae 1.49(+0.21/−0.19) | vs Saad-Ting 1.12 (Newton camp) |
|---|---|---|---|
| MG (catalogued 1.137) | 1.137 | **−1.9σ** (not −3.3σ) | consistent (+0.02) |
| MI θ(0)=2 | 1.14 | −1.8σ | consistent |
| MI θ(0)=e | 1.10 | −2.1σ | consistent (−0.02) |

So the framework (any θ) sits **~1.8–2.1σ below Chae's central, consistent with the Newton-camp Saad-Ting 1.12** — NOT
the inflated −3.3σ. Both ways: the MI correction makes the framework *slightly more Newtonian* (a touch further from
Chae's pro-MOND signal, a debit), but the verified-correct Chae number (1.49±0.20, lower + wider than the wrong 1.60±0.14)
*reduces* the tension — net the tension is **~2σ, not 3.3σ.** And Chae's central 1.49 sits ABOVE even framework-MG, so
present data, if anything, **disfavor the strong-suppression (large-θ0) MI branch** — a both-ways point against reading
the most-Newtonian MI as a "win."

## How the Gaia DR4 "sharpest live test" should be REFRAMED

The catalogue calls wide binaries the sharpest live test with the anchor "γ_cap=1.137 (dS-Unruh MI)." Corrected framing:
- **The anchor 1.137 is the modified-GRAVITY value, not the framework's MI value.** The framework's own MI prediction is
  the **most-Newtonian variant** (γ_g~1.10, γ_v~1.05 for θ(0)=e) — i.e. the framework predicts the **smallest** deviation
  from Newton of any MOND, making it the **hardest to distinguish from a pure Newtonian null.**
- **It is a θ(0)-family, not a number**, until θ(0) is derived — so wide binaries test the **premise** (boost vs Newton)
  and the **a0 value/interpolation**, but **cannot isolate the framework's distinctive MI θ-factor** (a0-degenerate at one
  a_ex; the proof-signature is below the DR4 floor).
- Gaia DR4 (Dec 2026) remains the sharpest LIVE test, but of the **premise** (is there ANY low-acceleration boost), not of
  the framework-distinctive MI content. A clean Newtonian null still kills the a0=Λ premise; a boost confirms it but
  cannot pick MI from MG or fix θ(0).

## What Carl CAN / MUST NOT say

- **CAN:** the framework is modified inertia, so its wide-binary EFE is the Milgrom-2022 θ-form, predicting the
  **most-Newtonian** boost of any MOND (γ_g~1.10, γ_v~1.05 at the natural θ(0)=e); it is consistent with the Newton-camp
  Saad-Ting (1.12) and ~2σ below Chae's 1.49; Gaia DR4 tests the low-acceleration premise.
- **MUST NOT:** "the framework predicts γ=1.137" (that is the modified-GRAVITY value; the MI value is a θ(0)-family,
  most-Newtonian ~1.10); "Chae 1.60 is 3.3σ above us" (Chae 2309.10404 is 1.49(+0.21/−0.19); tension is ~2σ); "wide
  binaries cleanly test the framework's distinctive MI physics" (MI-vs-MG is a0-degenerate at one a_ex; the proof-signature
  is below the DR4 floor); "1.137 is the dS-Unruh MI value" (it's the θ=1 / momentary-field MG value).

## One line

The catalogued wide-binary "γ≈1.137 (dS-Unruh MI)" is actually the momentary-field MODIFIED-GRAVITY value; the framework
being modified INERTIA, its real EFE carries Milgrom-2022's θ(ω_ex/ω_in)≥1 factor (verified Eq.35) and predicts the
**most-Newtonian** boost of any MOND (γ_g~1.10, γ_v~1.05 at the natural θ(0)=e) — but θ(0) is an underived FREE function
(so the prediction is a family γ_g∈[1.04,1.30], not a number) and a constant θ(0) is exactly a0-degenerate, so wide
binaries test only the premise, not the distinctive MI physics (proof-signature ~5–8%, below the DR4 floor); and against
the VERIFIED Chae 2023 (γ_g=1.49(+0.21/−0.19), not the corpus's wrong 1.60) the framework sits ~2σ below, consistent with
the Newton-camp Saad-Ting — not the catalogued −3.3σ.

*Both ways: the MI θ-form (more Newtonian) is credited as the framework's OWN physics and the catalogued 1.137 is
demoted to the MG value; the free-function θ(0), the a0-degeneracy, the below-floor proof-signature, and Chae's central
sitting above even MG (disfavoring strong suppression) are all conceded at full weight; the Chae-number fix cuts the
tension both ways (more-Newtonian framework vs lower-and-wider Chae → ~2σ, not 3.3σ). Quarantine held: a0/Z never
asserted derived; θ(0) never asserted derived.*
