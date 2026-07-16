# GATE_SPEC — the three-part validator that tells a real relation from a fitted coincidence

*Reverse-engineered from the zimmerman-formula validation lineage. This is the literal specification of "what we did to get
the a₀ discovery" turned into a reusable, pass/fail gate. Same bar both ways: it must certify the one real result
(a₀'s forced kernel, Koide Q=2/3) **and** reject the known coincidences (4Z²+3, 64π+Z, the "dS-Unruh forces √2" derivation).*

Provenance (all read read-only, all re-run and reproduced 2026-06-25):
- `real_research/reviews/false_discovery_rate.py` — the α⁻¹=4Z²+3 look-elsewhere null (~34k-formula search).
- `real_research/reviews/mass_fdr/attack5_fdr.py` + `attack5_fdr_partB.py` — FDR on SM mass ratios; the 164 re-labelings.
- `opus_48_extended_research/reviews/koide_dsunruh/koide_fdr_sqrt2.py` — Q1/Q2 split: Koide is real, "√2 derived" is not.
- `opus_48_extended_research/reviews/koide_dsunruh/koide_geometry_crossfermion.py` — cross-fermion interlock falsification.

A candidate relation is reported as a **lead** only if it passes **ALL THREE** gates: (A) FDR-survival, (B) forced kernel,
(C) interlock. Failing any one ⟹ logged FDR-dead with its tell. A, B, C are independent and necessary; none alone suffices.

---

## GATE A — FDR-survival (look-elsewhere): "how often would this search hit by chance?"

**What it answers.** Given a brute-force search of size *N* over a symbol pool, a 4-digit target is hit to high precision
*by construction*. The α⁻¹=4Z²+3 "0.004% match" is the **expected output** of a 34,000-formula search, not a discovery.
Gate A quantifies the chance rate and demands the observed hit be far rarer than chance.

**The exact mechanism (two equivalent measures used in the lineage):**

1. **Reconstruct the reachable set, not the reported formula.** Build *every* value the engine can emit from the same
   building blocks / integer ranges / families (`build_value_set()` in `false_discovery_rate.py` mirrors the 7 search
   methods verbatim → ~34k values; `attack5_fdr_partB.py` builds a 57,489-expression library over the framework pool).
   The candidate is *one point in this set*; the gate scores the **set's density at the target**, never the formula alone.

2. **Local-density Poisson expectation** (`attack5_fdr_partB.py`, the load-bearing test). For target *t* with measurement
   tolerance `tol`:
   - count library values in the tight window `[t(1−tol), t(1+tol)]` → `n_hit`;
   - count library values in a wide band `[0.9t, 1.1t]` → `n_wide`;
   - **`E_chance = n_wide · (2·tol)/0.2`** = expected hits in the tight window if the reachable set is locally uniform.
   - **Verdict:** `E_chance ≥ 1` ⟹ **BAKED** (the pool densely covers that region; a hit is unsurprising).
     `E_chance ≪ 1` **and** a real hit exists ⟹ candidate **LOOK** (sparse + hit = surprising). This is empirically
     reproduced: every SM mass ratio comes back `BAKED`/`BAKED(dense)` (m_τ/m_μ: 122 hits, E=137; m_c/m_s: 525 hits, E=573).

3. **Random-target baseline / surplus bits** (`false_discovery_rate.py`, `koide_fdr_sqrt2.py`). Draw thousands of
   *arbitrary* (no-physics) log-uniform targets in the same range; measure the fraction matched to the candidate's
   precision. **Surplus bits over chance** `= −log₂( hits_at_target / hits_at_random )`. In the α⁻¹ neighborhood [100,150]
   the search hits an *arbitrary* target to ≤0.004% a large fraction of the time ⟹ ~0 bits ⟹ BAKED. For "dS-Unruh forces
   √2": hits near √2 (12 at 0.5% tol) are *fewer* than hits near a random O(1) (5.68) → surplus = **−1.08 bits** ⟹ NOT special.

**The rational-target exception (Gate-A's own footnote, from `attack5_fdr.py`).** A *small-denominator rational* target
(like 2/3) is hit *exactly* by many symbol combinations (CUBE/GAUGE=8/12 is just one of dozens). So **re-labeling a rational
is FREE and carries no bits** — Gate A on the *number* 2/3 alone is uninformative. This is *why* Koide cannot be certified by
Gate A on the value; its evidence lives in **the random-mass-triple null** instead:
`P(|Q_geo − 2/3| < 1e-5)` over 4M random log-uniform mass triples = **2.08e-5 ≈ 1-in-48,000** (reproduced; banked ~2.3e-5),
and the density peak of Q_geo sits at ~0.997 not 2/3 — so 2/3 is a genuine special angle *for the leptons*, not a generic
attractor. **PASS criterion for Gate A:** the chance rate of the relation (Poisson `E_chance` for a real target, OR the
random-triple/random-target probability for a structural relation) must be `≪ 1` (operational threshold: surplus ≥ ~10 bits,
i.e. chance ≲ 1e-3, with the look-elsewhere correction × #targets searched already folded in).

---

## GATE B — forced kernel: "does a coefficient decompose into factors pinned BEFORE the fit?"

**What it answers.** This is the half that made a₀ real. A fitted coefficient is free; a **forced** coefficient is dictated
by known physics (symmetry/geometry/a conservation law) *independent of and prior to* matching the data. Gate B is a
**detector for forced-before-fitting structure** in the candidate's coefficient.

**The exact criterion (the a₀ exemplar, sympy-verified exact, 2026-06-25):** the kernel √(8π/3) decomposes **uniquely** as
- **√(8π)** ← Einstein normalization ρ_Λ = Λc²/8πG (the 8π is forced by the field equations), ×
- **√(1/3)** ← Friedmann coefficient H² = 8πGρ/3 (the 3 is forced by the FRW metric).

Both factors are written down *before* any number is fit. Verified identities (`sympy.simplify == 0`):
`√(8π)·√(1/3) = √(8π/3)` ✓; `Z = √(32π/3) = 2·√(8π/3)` ✓; `√(2/Z) = (3/8π)^(1/4)` ✓ (the CKN g\*=1 geometric saturation).
**Only ONE number is free:** the outer κ = ½ (the "2" in Z = 2·kernel = 1/κ). One-parameter, not tuned.

**Pass test (forced-kernel detector — what the engine must check for each candidate):**
1. **Provenance, not factorization.** Mechanically factoring a coefficient is trivial; the gate requires each factor be
   **traceable to a named, pre-registered physical constraint** (a field-equation normalization, a metric/measure
   coefficient, a representation dimension, a discrete-group invariant, a root-system/polytope angle) — declared *before*
   seeing the target. A factor with no such tag is a **free fit parameter**, not a forced kernel.
2. **Overdetermination.** The *same* forced factor must appear in **≥2 independent forced places** (√(8π/3) appears in
   Einstein *and* Friedmann), or the **form** be forced a third independent way (a₀∝√Λ via dS-Unruh quadrature). One
   appearance = a definition; two+ independent appearances = a kernel.
3. **Free-parameter count.** Count the genuinely unforced O(1) numbers. **PASS = exactly one** (κ-class) free parameter
   (a₀ is one-parameter); **FAIL** if the "derivation" needs ≥2 free numbers to land the target. (Koide-via-dS-Unruh fails
   here: κ=½→√2 is *two* free numbers, and √(2/Z)=0.588 is the wrong value — recorded in MEMORY as re-label-dead.)

**The asymmetry to expect (the honest prior).** Gravity forces √(8π/3) before fitting; the SM Yukawa sector hands the masses
**no analogous forced kernel** (charged-lepton masses are eigenvalues of a *free* Yukawa matrix). So most SM candidates will
**FAIL Gate B** with the tell "factor has no pre-registered physical provenance / needs ≥2 free numbers." That is the correct,
honest output — not a bug. A SM candidate **passes Gate B** only if its coefficient decomposes into factors forced by a
*declared, pre-fit* symmetry/geometry (a discrete flavor group A₄/S₄/Δ(27), a representation dimension, a root-system angle).

---

## GATE C — interlock: "does the structure force ≥2 independent observables, or tie ≥3 constants with 1 parameter?"

**What it answers.** A relation that fits one number with one knob is a coincidence dressed as physics. Real structure is
**overdetermined**: the same mechanism is pinned from several directions, so it makes a *second* prediction it could fail.
Gate C is the cross-check that the candidate is not a one-number re-description.

**The two pass-modes (either one passes):**

- **Mode C1 — multi-observable forcing.** The structure forces **≥2 independent observables** from the *same* parameters.
  a₀ qualifies: the one forced kernel pins both the Einstein and Friedmann appearances *and* the dS-Unruh form — three
  independent anchors, one free κ.
- **Mode C2 — Koide-class constraint.** The relation **ties ≥3 measured constants with ≤1 free parameter**. Koide qualifies:
  Q = (Σmₗ)/(Σ√mₗ)² = 2/3 ties *three* charged-lepton masses with **zero** free parameters (a pure geometric constraint:
  the √-mass vector at 45° / cos²θ=3/4 to (1,1,1)).

**The interlock falsification (Gate-C's teeth, from `koide_geometry_crossfermion.py`).** A claimed mechanism that is
*universal* must hold on every sector it claims to govern. The gate **applies the same relation to independent triples** and
demands consistency:
- Charged leptons: Q_geo = 0.666661, cos²θ = 0.7500, θ = 45.00°, r = 1.414 — **Koide, exact.**
- Up quarks, down quarks, neutrinos (NO & IO, all m₁): θ ranges ~31–55°, r ≠ √2 — **fail Koide by ~many σ.**
- **Symbolic interlock fact (sympy-exact):** with √mᵢ = M(1 + r·cos(2πk/3 + δ)), Q_geo depends **only on amplitude r, not
  the Z₃ phase δ**; Q_geo = 2/3 ⟺ r = √2. So √2 is a *normalization*; the real content is the per-fermion **kₐ** (=1 for
  leptons, ≠1 for quarks). A mechanism claimed *family-universal* (dS-Unruh is a horizon/kinematic effect, blind to gauge
  charge) is **REFUTED** by the cross-fermion test unless it carries a charged-lepton-specific ingredient.

**PASS criterion for Gate C:** the candidate must satisfy C1 **or** C2, **and** survive its own cross-sector/second-observable
falsification (the prediction it is forced to make elsewhere must not be contradicted by data). A relation that passes A and B
but makes no second forced prediction — or makes one that the data kills — is logged **interlock-FAIL** (a one-number
re-description, the 4Z²+3 failure mode). Note Koide passes A (via the triple-null), passes C2, but the *current framework
mechanism* for it fails B (κ=½→√2 = two free numbers) — so by this gate **Koide is a real interlock without a forced kernel
yet**: that gap is exactly the open target, honestly labeled, not a win.

---

## How the three compose (the pipeline rule)

```
candidate ──▶ GATE A (FDR-survival)        fail ─▶ log FDR-dead  (tell: "E_chance≥1" / "0 surplus bits" / "dense pool")
                 │ pass
                 ▼
              GATE B (forced kernel)        fail ─▶ log kernel-free (tell: "factor has no pre-fit provenance" / "≥2 free #s")
                 │ pass
                 ▼
              GATE C (interlock)            fail ─▶ log interlock-fail (tell: "one-number re-description" / "cross-sector kill")
                 │ pass (C1 or C2, + survives 2nd-observable test)
                 ▼
              REPORT AS LEAD  (one-parameter, forced-kernel, interlocking — the a₀/Koide signature)
```

**Calibration acceptance test (must pass before pointing at PMNS):** the gate must (i) **reject** 4Z²+3 (A: ~0 bits),
64π+Z and the 164 re-labelings (A: BAKED-dense), and "dS-Unruh forces √2" (A: −1.08 bits / B: two free numbers);
(ii) **certify** a₀'s √(8π/3) kernel (B: Einstein×Friedmann, exact; C1: 3 anchors / 1 κ) and Koide Q=2/3 (A: 1-in-48k
triple-null; C2: 3 masses / 0 params), while **honestly flagging Koide's missing forced kernel** (B-gap). A gate that does
not reproduce all of these is not trustworthy on anything new.
