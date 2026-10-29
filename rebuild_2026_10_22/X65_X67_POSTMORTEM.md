# X65–X67 post-mortem: where the core-floor mechanisms stand (2026-10-29)

Standing: κ = ½ FITTED; not theory closed. The mechanisms below were proposed by an external model and relayed by the
owner in chat. Each tested one was frozen before any script and graded by its own lane. This note collects what was
learned and what is now closed.

**The target.** The empirical core rule ρ₀r₀ = max(a₀/(2πG), η Σ_coll) (X43) fits SPARC and most cluster keys. The
question was whether a local, conservative mechanism makes the floor a₀/(2πG) dynamically.

## 1. Lanes run

| Lane | Mechanism | Outcome |
|---|---|---|
| X65 | AQUAL pull on the cold sector, gated by stream-sign Q | **RAISES, NO FLOOR.** Q fires out to the splashback radius (35–120 r₀), so every halo is lifted ×3–5. R_G tracks R_N roughly as R_N^0.86, with no plateau at 1. max() BROKEN; j-DEPENDENT. |
| X66 | Boost confined to the core (dg/dr > 0) up to g_σ = a₀/4 | **FAIL.** At most 3 % of the mass is ever boosted. Where it fires it heats cores: at 1e9 R goes 0.21 → 0.15; the a₀/2 mutation gives 0.07. max() BROKEN; j-DEPENDENT; UNRESOLVED; THRESHOLD-INSENSITIVE. |
| X67 | X65 with μ argument screened by C² = (ρ̄(<r)/ρ)², a_crit = a₀/2 | **FAIL.** A softer X65: lift 0.30 dex against 0.66; R still rises with mass; the boost reaches 50–100 r₀ (as pre-flighted). max() BROKEN; j-DEPENDENT; THRESHOLD-INSENSITIVE. |
| X47 (10-25) | Local a₀ tether | **FAIL.** Without latching, a cored profile has g < g_T everywhere, so no core forms. With latching, the whole sector turns to dust by z ≈ 40–700. |

## 2. Checked in chat (no lane)

- **Potential-depth invariant √((4/π) G ρ̄ |Φ_N|) · C^p.**
  - Its central value is 0.564 a₀R, not the claimed a₀R.
  - It is not flat beyond about 5 r₀.
  - The exponent p was tuned (1 → 3/2 → 5/3).
  - |Φ_N| has a zero point set by the outer boundary, so it is not a local observable.
  - Not run.
- **Slab versus sphere.** A Burkert core at the floor has peak Newtonian pull 0.2545 × 2πGρ₀r₀, not a₀. Several proposals
  assumed the slab value.
- **"κ = ½ from R_dS = 4Λ" or "√(8π/32π)".** The first has wrong units. The second picks 32π as the normalization, which
  restates κ = ½ rather than deriving it.
- **c_f.** The proposed (Δ_vir/Δ_ta)^(1/3) × 2 evaluates to 8.3, not 4.

## 3. Phantom tracking gives a ceiling, not a floor

PROVISIONAL: this is the external model's transcription; the equation numbers and the first term are unverified against
the paper.

Milgrom 2009 (MNRAS 398, 1023; arXiv:0909.5184) gives the central phantom surface density as approximately

Σ_M { (6/π) X₀ [1 − μ(X₀)] + ∫₀^X₀ L(x) dx },  with Σ_M = a₀/(2πG), X₀ = g_max/a₀, L = xμ′/μ.

- It saturates near Σ_M only when X₀ ≫ 1.
- It falls below Σ_M when X₀ ≪ 1.

That is a ceiling, the opposite of the max() floor. Tying the cold sector to the law's phantom profile therefore cannot
make the floor in low-mass halos.

**Exact identity (checked).** For a cored spherical system with Δg ≡ g − g_N → 0 at r = 0 and at r → ∞:

Σ_p(0) = (1/πG) ∫₀^∞ Δg / r dr.

## 4. Pressure-type floors

A minimum dispersion or phase-space cap set by Λ adds outward support, so it can only LOWER ρ₀r₀. Raising low-mass cores to
the floor needs extra binding, and extra binding is the X65 family, which lifts every halo.

## 5. Limits of the 1D harness

Each shell keeps its assigned L_i = j √(G M_i r_i,0). The Newtonian core is then set largely by the centrifugal barrier:
at 1e10, R_N is 0.98 / 0.46 / 0.28 for j = 0.05 / 0.1 / 0.2. So the harness's j-robustness condition is close to
unpassable for any honest force law.

This is a statement about the test bed, not a theorem about physics:
- a self-consistent field does depend on j, through the inner mass profile;
- real 3D halos do not conserve per-shell angular momentum (violent relaxation, radial-orbit instability).

Any future floor mechanism should be tested with 3D relaxation, for example on the X48 zoom setup, not in this harness.

## 6. Where this leaves the record

- a₀ = κ c √(Gρ_DE) with κ = ½, and the max() core rule, remain the two EMPIRICAL pillars.
- Neither is derived. Do not cite either as derived.
- Closed routes:
  - squeezing after collapse (X65–X67);
  - local tethers (X47);
  - pressure and phase-space floors;
  - phantom tracking.
- Still open:
  - c_f from 3D zooms (X48 A4, running);
  - a genuinely new mechanism, which would need a 3D test.
