# AS016 — Pressure mapping versus density mapping (derivation)

**Run:** `run_20260927T2233Z` · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent, single-run worker seed
**Branch:** CORE scale identities (Group A01); Q, RAR, MU2, EXP AQUAL, MONO untouched — no branch translation is performed or claimed anywhere in this document.
**Sources:** README.md `91a5fac4…a6b6ed`, FRIED_CHICKEN_SPEC.md `98d9149f…8e3f`, DERIVATIONS.md `8da8176e…b889`, STANDING.md `660462eb…7bf63`, FRAMEWORK_CONTRACT.md, RESULT_CONTRACT.json — hashes verified against SOURCE_MANIFEST.json (all match; see result.json `input_sha256`).

---

## 1. Symbol dictionary, precise claim, boundary conditions

| Symbol | Meaning | Units | Status |
|---|---|---|---|
| `a0` | vacuum acceleration scale | m/s² | framework input, κ = 1/2 ADOPTED |
| `κ` | normalization (κ = 1/2) | — | adopted input, not derived here |
| `G` | Newton constant | m³ kg⁻¹ s⁻² | measured input 6.67430e-11 |
| `c` | speed of light | m/s | exact 299792458 |
| `ρ_Lambda`, `ε_Lambda` | vacuum mass density / energy density, `ε_L = ρ_L c² = 4a0²/G` | kg/m³, J/m³ | derived from a0, κ (framework identities) |
| `M_b` | baryonic mass (here M_sun) | kg | input per example |
| `r_M` | MOND radius `√(G M_b/a0)` | m | derived |
| `C` | `√(G M_b a0)` = v_flat² | m²/s² | derived |
| σ², ρ_ph(r), P(r) | deep-equilibrium targets `σ² = C/2`, `ρ_ph = C/(4πGr²)`, `P = σ²ρ_ph` | m²/s², kg/m³, Pa | **conditional targets, NOT free laws** (FRAMEWORK_CONTRACT) |
| `ε_DE(z)`, `p_DE(z) = w(z) ε_DE(z)` | cosmological vacuum energy density / pressure | J/m³ | background inputs of the map comparison |
| `w(z)` | equation-of-state parameter | — | input of the pressure map |
| a_ρ² = (G/4)·ε_DE | **density mapping** (candidate vacuum-scale law) | m²/s⁴ | framework's own form (Thm. 1 below) |
| a_p² = (G/4)·(−w)·ε_DE | **pressure mapping** (candidate vacuum-scale law) | m²/s⁴ | candidate alternative, normalization matched to the framework |

**Grounding of the coefficient G/4.** With κ = 1/2, `a0² = κ²c²Gρ_L = (G/4)(ρ_L c²) = (G/4) ε_Lambda` (exact identity, Lean-certified `density_scale_identity`). So the framework's own scale IS a density mapping with coefficient G/4 and **zero w dependence**; the pressure mapping is the candidate that replaces ε_DE by −p_DE = −w ε_DE with the same coefficient (so that w = −1 reproduces the framework exactly). Any other coefficient K_p is a free input and is audited separately in §5.

**Boundary conditions / domain.**
- Density map: defined for all ε_DE > 0; real positive a_ρ for all physical ε_DE.
- Pressure map: a_p² = (G/4)(−w)ε_DE is real-positive **iff −w·ε_DE > 0**, i.e. (ε_DE > 0 and w < 0). At w = 0 ⇒ a_p = 0 (degenerate, no scale); w > 0 ⇒ a_p² < 0 (no real a0).
- Deep-equilibrium quantities: asserted at radii r ≳ r_M (deep regime) by the framework's conditional labelling; ρ_ph, P are pure 1/r² power laws (no cutoff, no scale of their own).
- Newtonian boundary: a0 → 0⁺ (vacuum density → 0) kills C, σ², ρ_ph, P exactly; g → B is handled by the Q/RAR/MU2/MONO branches, not by these targets.
- Everything SI; dimensional exponent vectors recorded in residuals.json (`dimensions`).

**Precise claim established.** For the conditional deep-equilibrium targets on the CORE branch:

1. `P(r) = M_b a0/(8πr²)` exactly; at r_M: `P(r_M) = a0²/(8πG) = ε_Lambda/(32π)` exactly.
2. The pressure mapping differs from the framework's density mapping by the exact factor `a_p²/a_ρ² = −w`, so the relative scale evolutions differ by the extra factor `w(z)/w(0)`.
3. The pressure expression ceases to define a real a0 precisely when `w ≥ 0` (with ε_DE > 0), i.e. p_DE ≥ 0.
4. Degeneracy audit: with the framework-matched coefficient, pressure map ≡ density map **iff w ≡ −1** (exact, both footings, all z); with a free coefficient the degeneracy is one-parameter at a single epoch and is broken by any second epoch with w(z₁) ≠ w(z₀).
5. The framework **uses the density mapping**: a0 is defined from ε_Lambda alone; the P, ρ_ph, σ² relations are derived targets at that scale, and the phantom pressure at r_M reaches only 1/(32π) of ε_Lambda (factor 32π(r/r_M)² suppression at r > r_M).

## 2. Step-2 derivation: relative scale evolution and the w(z)/w(0) factor

Let ε_DE(z) at redshifts z, w(z) < 0 on the pressure-defining domain; a reference epoch z₀ (z = 0).

Density map: a_ρ²(z) = (G/4) ε_DE(z) ⇒ relative evolution `a_ρ²(z)/a_ρ²(0) = ε_DE(z)/ε_DE(0)`.
Pressure map: a_p²(z) = (G/4)(−w(z)) ε_DE(z) ⇒ `a_p²(z)/a_p²(0) = [w(z)/w(0)]·[ε_DE(z)/ε_DE(0)]`.

**Extra factor:** the ratio of the two relative evolutions is exactly

```
[a_p²(z)/a_p²(0)] / [a_ρ²(z)/a_ρ²(0)] = w(z)/w(0)          (E1)
```

(signs: both maps carry the same −; w(z), w(0) < 0 cancel pairwise). Lean-certified (`relative_evolution_extra_factor`); numerically verified at 60 digits for the w(z) window {−1.0, −0.85, −0.70, −0.55, −0.40} at z = {0, 0.5, 1.0, 1.5, 2.0} on both footings: residuals ≤ 9.7e-62. The density-map ratio in (E1) is the ε-model-independent part: any common ε_DE(z) model cancels.

For ΛCDM (w = −1 constant) the factor is 1 at every z: the two maps are co-evolutionary — the masquerade (§5) holds at all z. For any evolving w(z), the factor is w(z)/w(0) ≠ 1 as soon as w changes: **this is the discriminator**.

**Where the pressure expression ceases to define a real a0.** Since a_p² = (G/4)(−w) ε_DE with ε_DE > 0:
- w = 0 (dust-equivalent pressure), p_DE = 0: a_p = 0 exactly — the map collapses to a degenerate zero scale, while the density map still gives a_ρ = a0 > 0.
- w > 0 (e.g. radiation-like w = +1/3, or any positive-pressure component): a_p² < 0, no real a0 exists.
- w → 0⁻: a_p → 0⁺ while a_ρ stays finite: a_p/a_ρ = √(−w) → 0.
Boundary: ε_DE → 0⁺ kills both maps (degenerate agreement point); a0 → 0⁺ kills the whole phantom sector (Newtonian limit, §6).

## 3. Step-3 intermediate algebra (all scale factors, signs, units)

**3.1 Pressure identity (exact).** Using σ² = C/2, ρ_ph = C/(4πGr²), P = σ²ρ_ph, C² = GM_b a0:

```
P(r) = (C/2) · C/(4π G r²) = C²/(8π G r²) = G M_b a0/(8π G r²) = M_b a0/(8π r²)     (E2)
```

Units: [C/2] = m²/s²; [C/(4πGr²)] = (m²/s²)(m³kg⁻¹s⁻²)⁻¹m⁻² = kg/m³ ✓; [P] = (m²/s²)(kg/m³) = kg m⁻¹ s⁻² = Pa = J/m³ ✓. `P·8πr² = M_b a0` — every factor (8π, signs, r²) shown; Lean-certified (`pressure_identity`).

**3.2 Phantom pressure at the MOND radius (exact).** r_M² = GM_b/a0:

```
P(r_M) = M_b a0/(8π r_M²) = M_b a0 · a0/(8π G M_b) = a0²/(8π G)                     (E3)
        = [4a0²/G]/(32π) = ε_Lambda/(32π)                                           (E4)
```

(E4) uses ε_Lambda = 4a0²/G. So P(r_M) is fixed by (a0, G) alone — no M_b, no r — and is 1/(32π) ≈ 0.009947 of the vacuum energy density. In general

```
P(r)/ε_Lambda = (r_M/r)²/(32π)                                                      (E5)
```

an exact pure power law (checked at r_M, 2r_M, 10 kpc, 100 kpc; residuals ≤ 1.3e-61). Enclosed phantom mass: dM_ph = 4πr²ρ_ph dr = (C/G) dr ⇒ M_ph(a→b) = C(b−a)/G (per-shell surface density 4πr²ρ_ph = C/G, r-independent; Lean `surface_phantom_mass`).

**3.3 Map ratio (exact).**

```
a_p² = (G/4)(−w)ε_DE = (−w)·a_ρ² ,   a_p²/a_ρ² = −w ,   a_p/a_ρ = √(−w)             (E6)
```

Lean-certified (`ratio_pressure_density`). Both footings share the same algebra; the product structure shows the pressure channel always carries the factor (−w) on top of the density channel.

**3.4 Signed summary.** Pressure map: real iff w < 0; magnitude factor √(−w) relative to the density map; relative z-evolution extra factor w(z)/w(0). No other coefficient, boundary constant or fitted input enters.

## 4. Both footings carried separately (dimensional examples, M_b = M_sun, r = 10 kpc)

Canonical a0 = 9.3619e-11 m/s² (κ = 1/2): ρ_Lambda = 5.844412454e-27 kg/m³; ε_Lambda = 5.252695960e-10 J/m³; r_M = 1.190639769e15 m (12.6 kpc); C = 1.114665045e5 m²/s² (v_flat = 333.8660 m/s); σ = 236.0789 m/s; ρ_ph(10 kpc) = 1.39581e-27 kg/m³; P(10 kpc) = 7.7793e-23 Pa; P(r_M) = 5.224953e-12 Pa = ε_Lambda/32π (rel. residual 1.4e-61).

Alternative a0 = 1.1279e-10 m/s² (κ = 1/2): ρ_total = 8.483089620e-27 kg/m³; ε_Lambda = 7.624220727e-10 J/m³; r_M = 1.084743572e15 m (11.49 kpc); C = 1.223482274e5 m²/s² (v_flat = 349.7831 m/s); σ = 247.3340 m/s; ρ_ph(10 kpc) = 1.53208e-27 kg/m³; P(10 kpc) = 9.3724e-23 Pa; P(r_M) = 7.583953e-12 Pa = ε_alt/32π (rel. residual 1.5e-61).

**Footing discipline.** The two footings share κ = 1/2 and therefore different densities: ρ_alt/ρ_can = (a0_alt/a0_can)² = 1.451487157 (ratio-of-ratios residual 1.0 to 60 digits). Holding ρ_Lambda fixed at the canonical value while moving to a0_alt forces κ_eff = 0.602388404 — recorded as a relabeling, not a third footing. Every dimensionless statement in this document (E1), (E6), w = −1 locus, √(−w) factors) holds identically for both footings; every dimensional example above is carried separately.

## 5. Step-5 / controls

**5.1 Negative control — w = 0 with positive ε_DE (the two mappings cannot agree).**
ε_DE = ε_Lambda > 0, w = 0: a_ρ = a0 > 0 (9.3619e-11 / 1.1279e-10 m/s² on the two footings), a_p = √(0) = 0 exactly, ratio a_p/a_ρ = 0 ≠ 1. The pressure map has collapsed; the density map has not. **This control is capable of failing:** a claim that the pressure map reproduces the density map identically is killed by this single witness (pass condition: ratio = 0 exactly and a_p² = 0 exactly with a_ρ² > 0 — observed, PASS on both footings). This is the same witness that quantifies step 2's domain: w ≥ 0 ⇒ no real a0 from the pressure expression.

**5.2 Positive control — w = −1 (the exact agreement locus).**
w = −1, any ε_DE > 0, both footings: a_p² = a_ρ² = (G/4)ε exactly (residual 0.0 at 60 digits, PASS). The masquerade is exact on w ≡ −1 — including at every z under ΛCDM (E1 factor = 1). Complementing 5.1, this shows the failure at w = 0 is a genuine dis-agreement, not a trivial "always differ": the family a_p/a_ρ = √(−w) interpolates smoothly from 1 (w = −1) to 0 (w = 0⁻) to undefined (w ≥ 0).

**5.3 Degeneracy audit (masquerade structure).**
- Fixed framework coefficient K_p = G/4 (equivalently: the scale is written in the pressure variable with ΛCDM-normalized coefficient): pressure map ≡ density map **iff w ≡ −1** over the whole spatiotemporal domain (Lean `agreement_iff_w_eq_neg_one`; exact, not approximate; independent of both footings).
- Free coefficient K_p: at a single epoch z₀, any w₀ < 0 is absorbable, K_p = (G/4)/(−w₀), so a single-epoch fit cannot distinguish maps — a genuine one-parameter degeneracy (this is the honest content of "one mapping can masquerade as the other").
- The degeneracy is broken by: (i) any window with w(z) ≠ w(0) — the relative evolutions then differ by w(z)/w(0); (ii) any measured w ≠ −1 under the fixed normalization.
- Answer to the task question: the framework actually uses the **density mapping** (a0 from ε_Lambda, zero w-dependence; P, ρ_ph, σ² are targets computed at that scale, not scale-defining laws — and the phantom pressure reaches only 1/(32π)·(r_M/r)² of ε_Lambda, so the pressure channel cannot carry the vacuum scale at r ≳ r_M: it would require |w_eff| ≤ 1/32π ≪ 1). The pressure mapping is a candidate alternative that is exactly degenerate with the framework only on the w ≡ −1 ΛCDM locus and otherwise only via single-epoch coefficient absorption.

**5.4 Deep/Newtonian limits and boundary cases.**
- Deep: ρ_ph, P are exact 1/r² power laws with no characteristic radius — there is no deep "limit" to take; (E2)–(E5) are exact identities, and high-precision evaluation confirms them as identities (residuals ~1e-61), not finite-order consistency.
- Newtonian: a0 → 0 with (G, M_b, r) fixed makes C, σ², ρ_ph, P, v_flat → 0; exact zeros at a0 = 0 (PASS) and P is exactly linear in a0 (P/(a0) constancy residual 2.0e-61, PASS) — the phantom sector vanishes exactly and monotonically as the vacuum density → 0.
- ε_DE → 0: both maps → 0 together (degenerate agreement point, PASS).
- These are boundary checks of the target identities; the surviving claim on the CORE branch is the algebraic content of §1–§5, whose transfer to the full theory requires the bridge in §8.

**5.5 Worst residuals of the independent checks (step 4, 60-digit mpmath, separate representations):**
P·8πr² = M_b·a0: rel. residual 1.23e-61 (can) / 1.02e-61 (alt); P(r_M)·32π = ε_L: 1.08e-61/1.49e-61; P(r)/ε_L = (r_M/r)²/32π: ≤ 1.23e-61; a_p² = (−w)a_ρ²: ≤ 9.1e-62; extra factor w(z)/w(0): ≤ 9.8e-62; φ-quadrature ∫4πr²ρ_ph dr over [r_M, 10r_M] vs C·9r_M/G: 8.82e-62; central-difference dP/dr vs −2P/r: 2.0e-16 at h = 10⁻⁸ kpc and 2.0e-24 at h = 10⁻¹² kpc with O(h²) ratio −8 decades (PASS, converged; the earlier h = 10⁻⁶ kpc attempt failed at 2.0e-14 exactly as its own truncation error, preserved as a failed attempt in `failed_attempts`).

## 6. Which mapping the framework uses — and the channel-ratio consequence

The framework base `a0 = κc·√(Gρ_Lambda)` with κ = 1/2 is, verbatim, `a0² = (G/4)ε_Lambda` (Lean `density_scale_identity`): a pure **energy-density** mapping with no w(z) or p_DE dependence. The pressure object `P = σ²ρ_ph` is a **target** of the deep equilibrium at that scale. Equating the phantom pressure channel to the vacuum pressure channel gives P/ε_Lambda = (r_M/r)²/(32π) — at r ≥ r_M this ratio is ≤ 1/32π, i.e. the pressure channel reaches at most ~1% of the density channel's magnitude, and for a ΛCDM identification w_eff = −P/ε_Lambda ∈ [−1/32π, 0): the pressure channel cannot masquerade as the source of the scale on its own footing; only the w ≡ −1 density-identified vacuum can.

## 7. Lean certificates

`AS016_pressure_density_certificates.lean` (in this run dir), verified with `lake env lean` (exit 0, zero `sorryAx`, every `#print axioms` line = `[propext, Classical.choice, Quot.sound]`):
1. `density_scale_identity` — a0² = (G/4)ε_Lambda (framework = density map);
2. `pressure_identity` — P·8πr² = M_b·a0;
3. `surface_phantom_mass` — (4πr²ρ_ph)·G = C;
4. `pressure_at_milgrom_radius` — P·8πG = a0² at r_M² = GM_b/a0;
5. `P_at_rM_eps_over_32pi` — P·32π = ε_Lambda at r_M;
6. `ratio_pressure_density` — a_p² = (−w)·a_ρ²;
7. `agreement_iff_w_eq_neg_one` — (a_p² = a_ρ²) ↔ w = −1 (given a_ρ² ≠ 0);
8. `relative_evolution_extra_factor` — (a_p²(z)/a_p²(0))/(a_ρ²(z)/a_ρ²(0)) = w(z)/w(0).

## 8. Strongest surviving statement, limitations, next implication

**Strongest surviving statement.** On the CORE scale-identity branch, for the conditional deep-equilibrium targets (σ² = C/2, ρ_ph = C/(4πGr²), P = σ²ρ_ph) with C = √(GM_ba0), the pressure mapping P = σ²ρ_ph is exactly P(r) = M_ba0/(8πr²) and P(r_M) = ε_Lambda/(32π); the framework uses the density mapping a0² = (G/4)ε_Lambda; the candidate pressure map a_p² = (G/4)(−w)ε_DE is real only for w < 0, differs from the density map by √(−w), carries the extra relative-evolution factor w(z)/w(0), and is exactly degenerate with the density map iff w ≡ −1 — exact identities (Lean-certified, 60-digit residuals ≤ 1.5e-61), identical dimensionless content on both a0 footings.

**Limitations.** (i) These are algebraic consequence/consistency statements about conditional targets; they do not derive κ = 1/2, do not solve any time-dependent relativistic equations, and do not promote the deep-equilibrium relations to free laws. (ii) No observational fit or data is used; nothing here measures w(z). (iii) No branch (Q/RAR/MU2/EXP/MONO) is touched; the Newtonian-regime behaviour remains governed by those branches. (iv) G_N/G_bare/G_cosmo are not identified; only G = 6.67430e-11 appears as the single scale-G of these target identities. (v) The finite-boundary, source-coupling, normalization and logarithmic-well derivations of the equilibrium relations are outside this task's scope (per FRAMEWORK_CONTRACT). (vi) Finite numerical agreement is evidence, not a theorem; the symbolic content is separately Lean-certified.

**Next unresolved implication.** To transfer the map discrimination to the full theory one must supply the bridge from the deep-equilibrium phantom variables to the cosmological vacuum equation of state: derive (or measure) whether the galactic-scale equilibrium vacuum satisfies p_DE = w(z)ε_DE with the SAME ε_DE(z) and w(z) as the cosmological background, and obtain a w(z) window on which w(z) ≠ w(0) — until then, all static (single-epoch) data are compatible with both mappings and the degeneracy is lifted only by the extra factor w(z)/w(0) in the relative evolution, on the CORE branch, conditional on that bridge.

## 9. Commands, bounds, reproducibility

- `python3 compute_AS016_pressure_density.py > raw_output.txt 2> err.txt` (cwd = this run dir); enforced: `ulimit -t 120` (CPU s), single-threaded CPython + mpmath (no vectorized imports), mp.dps = 60, wall 0.047 s measured, memory trivial (<10 MB, no allocation bound needed, far inside the 512 MB budget — recorded in result.json `execution_bounds`).
- `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS016_pressure_density_certificates.lean > lean_check.out 2>&1` — exit 0, Mathlib v4.34.0-rc2.
- All source hashes verified against SOURCE_MANIFEST.json before computing; raw outputs, residuals.json, lean_check.out, err.txt preserved in this run dir.
- Failed attempt preserved: the first derivative control at h = 10⁻⁶ kpc failed at rel. resid 2.0e-14 (its own finite-difference truncation at tolerance 1e-45) and was replaced by the two-step O(h²)-convergence control; the first Newtonian-limit control compared stringified zeros and was replaced by an exact-mpf check — both recorded in `failed_attempts`.