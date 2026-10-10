# Audit: deepseek_push GF2 "κ = ½ derived" (commit 5b173a046, 2026-10-08)

**Verdict: NOT A DERIVATION OF THE LAW'S κ. The two κ's are different quantities that share a name.** κ in a₀ = κ c √(G ρ_Λ) stays **FITTED**. Nothing in `deepseek_push/` is edited by this note; it is added to the record only.

## What GF2 computes (correct)
- **Inputs:** a log potential Φ = C ln r and Poisson's equation, giving ρ ∝ r⁻². With stationarity and barotropy, the hydrostatic dispersion is σ² = C/2 = v_flat²/2.
- **Result:** GF2 defines κ := σ²/v_flat² = ½.
- **This is the textbook singular isothermal sphere** relation v_c² = 2σ² (e.g. Binney & Tremaine §4.3). The algebra and the uniqueness lemma (γ = 2) are right.

## Why that is not the κ in the law
1. **Different definitions.** The law's κ fixes the *value* of a₀ against the vacuum: a₀ = κ c √(G ρ_Λ). GF2's κ is a dimensionless velocity ratio, σ²/v² inside a halo. It contains no c, no ρ_Λ and no a₀. GF2's README says so itself: "κ is a₀-free", and "The vacuum coupling (why a₀'s value is the vacuum's scale) — OUT of scope here."
2. **The bridge is a naming identification.** It goes through GF1's "web" (κ = 1/n ⇒ n = 2). That step equates the SIS ratio ½ with the coefficient in a₀ = c√(Gρ_Λ)/n, but no equation in GF2 links σ²/v² to a₀/(c√(Gρ_Λ)). That missing link is exactly the open problem: why a₀ takes the value κ c √(Gρ_Λ).
3. **Test of independence:** change the law's κ to 0.4. GF2's output stays ½, because the SIS ratio does not know a₀'s normalisation. A derivation of the law's κ would have to fail under that change.
4. **The record's standing results are consistent with this reading:**
   - κ is underivable from the routes tried (12 attempts; see STANDING_2026-09-29.md);
   - the 32π puzzle has no derivation, and pasted "derivations" were circular (EXT01/EXT02);
   - measured κ is 0.42 ± 0.10 (CFG493, canonical), so ½ is consistent but not pinned.

## What GF2 does establish (worth keeping)
Within the framework's static log branch, the hydrostatic σ²/v_flat² = ½ follows with no imported ½. This removes the "rung 4 import" label from σ² = C/2 in the record's anchor chain. That result concerns the **halo's internal state**, not the vacuum normalisation of a₀.

## Rule for citing
Never cite GF2 as "κ derived". Cite it as: "the SIS dispersion ratio σ²/v² = ½ follows from the log branch plus hydrostatics (GF2); the coefficient κ in a₀ = κ c√(Gρ_Λ) remains fitted."
