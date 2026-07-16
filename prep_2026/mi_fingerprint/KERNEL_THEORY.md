# Kernel Theory of the de Sitter–Unruh Modified-Inertia Action: Circular Exactness, Frequency Dependence, and the Off-Circular Split (Lane RB, 2026-07)

**Framework:** Zimmerman de Sitter–Unruh **modified inertia**. a₀ = cH_Λ/Z = 9.36e-11 m/s² (canonical, ρ_DE), alt footing 1.13e-10 (ρ_total/cH0) — both run everywhere a scale enters. The framework's OWN interpolation ν(y)=√(1+1/y), y = g_bar/a₀ (never McGaugh's ν).

**Object of study:** the published covariant MI action (MI_COMPLETION_WRITTEN_2026-07.md v4–v13, Zenodo concept 21253644; loop arc DOI 21284144):

    S_matter = −(1/2) ∫√−g ρ_m [ s u^μ K(□_u/a₀²) u_μ ],   K(z) = (√(1+4z)−1)/(2√z),
    □_u f = u^a∇_a(u^b∇_b f),   s = −1 (postulate),

with the v4 spectral data (Herglotz–Nevanlinna measure ρ_A=(1−√(1−4|t|))/(2π√|t|) on −¼<t<0, ρ_B=1/(2π√|t|) on t<−¼; ‖K‖≤1; causal-retarded) and the v11 sum rule ∫dμ(t)/|t| = 1. Everything below is re-derived independently, not trusted from the repo (which is read-only for this lane).

**Scripts (all exit 0, this directory):** `rb1_circular_exactness.py` (15 checks), `rb2_frequency_dependence.py` (13), `rb3_eccentric_offset.py` (19). Outputs banked as `.out` files.

---

## 1. Result (i): the circular-orbit / quasistatic limit — exact ring-by-ring, and *why*

**Theorem A (ring exactness).** The kernel evaluated at the squared-acceleration argument is exactly the inertia dressing: K(x²) = μ_fw(x) = (√(1+4x²)−1)/(2x), x = a/a₀ (sympy-exact). The circular balance μ_fw(x)·x = y inverts in closed form to x = y·ν(y) with ν(y) = √(1+1/y) — because 1+4(y²+y) = (2y+1)² collapses the nested radical. So **g_obs(R) = ν(g_bar(R)/a₀)·g_bar(R) holds EXACTLY at every ring independently**: the law is algebraic in the local acceleration; there is no field equation and hence no radius mixing. Numeric residual over y ∈ [1e-4, 1e4]: 3.4e-13 (machine zero). This realizes Milgrom (1994, Ann. Phys. 229, 384)'s circular-orbit statement for this specific kernel.

**Theorem B (the reduction is the exact first-moment closure — new).** For **any** timelike worldline (curved space included, by metric compatibility):

    u_μ □_u u^μ = u·ȧ = −|a|²   ⇒   ⟨□_u⟩_u ≡ (u·□_u u)/(u·u) = +|a|²  exactly.

So the published prescription K(□_u/a₀²) → K(a²/a₀²) = μ_fw(a/a₀) is not an ansatz: it is the **exact first spectral moment** of the nonlocal operator in the u-contraction, valid for every orbit shape. The positive sign of the moment — despite the operator's spectrum sitting at −ω² on the cut — comes from the Lorentzian-signature weights of the time (eigenvalue 0, weight −γ²) and spatial (eigenvalue −ω², weight +γ²v²) parts. This is the derivational backbone of the RAR in this framework.

**Finding C (the closure gap is O(1) — new, honesty-critical).** The **literal** spectral evaluation of the kernel on the exact helical worldline u = (γ, γv cos ωτ, γv sin ωτ, 0) is

    u·K(□_u/a₀²)u = γ²v² K(−(ωc/a₀)²)   (exact; resolvent action verified symbolically),

which is **not** −μ_fw(a/a₀): the moment expansion is uncontrolled (each order grows by (c/v)²), and at real orbital frequencies K is a pure phase of unit modulus (§2), i.e. **the literal frequency-domain closure gives NO MOND at all** (at a=a₀, galactic w=c/v≈2.0e3: K = 0.99999997 + 2.5e-4 i vs the prescription K(1)=0.618). The literal closure is dead twice over: (a) it fails the RAR outright; (b) its imaginary part implies a universal secular orbital-energy drift at rate a₀/2c (~0.4 m/yr in the Earth–Sun distance — the scale modern ephemerides bound at ~cm/yr; a proper cited confrontation belongs to the data lane). **Consequence:** the papers' own named open item ("off-circular jerk/congruence-shear terms") is now quantitative — the closure map from the operator to the orbit dynamics carries an O(1) choice, and **only the first-moment family reproduces the RAR.** Within that family, ring exactness is **closure-independent** (on a circle |a| is constant, so every time-weighting of |a|² coincides). Surviving residuals on an exact ring: SR kinematics ≲2.5e-7 (galaxies), frequency-phase ≲3.1e-8 — total ≲3e-7 relative, both footings.

**The MG contrast (the in-hand discriminator, computed).** QUMOND with the SAME ν on a Miyamoto–Nagai disk (A=1, B=0.2), multipole phantom-density solve (spherical Plummer control returns the algebraic law to 1.3e-5): the in-plane ring-by-ring ratio (g_QUMOND/g_N)/ν(y) runs from **−1.05% (inner, y≈11) through 0 to +2.28% (outer, y≈0.4)** — a signed inner/outer split purely from the field equation's radius mixing. The framework's MI predicts exactly 0 at every ring. The footing only relabels *where* on the disk the transition sits.

---

## 2. Result (ii): the frequency dependence ν_eff(a, ω) — forced form, forced numbers

**The measure, re-derived.** Stieltjes inversion of K reproduces the two closed-form densities (max err <1e-4 against direct boundary values), and the v11 sum rule is re-derived independently: region B contributes ∫dμ/|t| = **2/π exactly** (sympy closed form), region A the numeric complement 1−2/π; total = 1 to 1e-8. Physical content: unit resolvent weight = the inertia interpolates from 0 (deep IR) to exactly the Newtonian value (UV); no spare weight for an a₀ tadpole (v11) — and, here, it pins the DC normalization of the frequency response.

**The forced form (new closed-form result).** On the physical (oscillatory) branch, the retarded boundary value is **unimodular**:

    K(−w² + i0) = exp[ i·arcsin(1/2w) ]   EXACTLY for w ≥ 1/2,   w = ωc/a₀
    (Re K = √(1−1/4w²), Im K = 1/2w; Re² + Im² = 1, sympy-exact).

Every bound orbit has w ≫ 1/2 (the branch point sits at period ~4e19 s ≈ 1275 Gyr; the kernel's memory time is the **horizon scale** τ_mem = 2c/a₀ = 2Z/H_Λ, not any orbital scale). So the entire frequency dependence of the kernel at real orbital frequencies is a **phase lag** φ(ω) = arcsin(a₀/2cω): a reactive part cos φ and a dissipative part sin φ, with **zero amplitude modification**. The MOND amplitude cannot live in the frequency channel (consistent with Finding C); it lives in the first-moment amplitude channel.

**Uniqueness — no measure freedom exists.** K is Herglotz, and the RAR calibration fixes K on the positive real axis (the first-moment argument sweeps z = a²/a₀² across ~[1e-4, 1e8] in observed systems). By the identity theorem, a Nevanlinna function agreeing on a real interval inside its analyticity domain is determined **everywhere**; the measure is unique. Numerical witness: the single measure reconstructs K on z>0 to <1e-7 **and** the cut boundary values (PV + iπρ) to <1e-3. **So the frequency response is forced by (Herglotz class) + (the RAR): there is nothing left to tune.**

**The numbers.** For a circular orbit, ω = a/v, so w = ac/(v a₀); at the same a, wide binaries and galaxy outskirts differ in w by 2.5–3 dex. At a = a₀ (where w = c/v, **footing-independent**):

| system | v | w | φ (rad) | 1−cos φ |
|---|---|---|---|---|
| wide binary | 0.45 km/s | 6.7e5 | 7.5e-7 | 2.8e-13 |
| dSph | 10 km/s | 3.0e4 | 1.7e-5 | 1.4e-10 |
| galaxy outskirts | 150 km/s | 2.0e3 | 2.5e-4 | 3.1e-8 |
| cluster | 1000 km/s | 3.0e2 | 1.7e-3 | 1.4e-6 |

Mapped through the circular balance (μ_fw(x)cos φ·x = y):

- **Δν/ν (wide binary vs galactic, same a = a₀): +2.3e-8 at y=1 (+1.7e-8 at y=0.1), galactic side more boosted. Footing-independent.**
- Dissipative phase split: |Δφ| ≈ 2.5e-4 rad (acts on perturbations, not on ν).
- Universal secular scale of the dissipative channel: **τ = 2c/a₀ = 203 Gyr (canonical) / 168 Gyr (alt)** ≈ 7–8% per Hubble time, orbit-independent (ω sin φ = a₀/2c exactly). Ownership: this drift belongs to the already-dead literal closure for the orbit's own motion; under the published first-moment closure the orbital secular drift is exactly zero (K(a²/a₀²) is real) and the phase acts only on perturbations (epicycles, tides, waves). Its **sign** inherits the s = −1 postulate status (KMS-passive = damping; the Machian/pumped reading = gain).

**The headline prediction: frequency universality of the RAR.** The published kernel forces wide binaries and galaxies at the same g_bar to share the same ν to ~3 parts in 10⁸. Any confirmed O(10%) wide-binary deviation from the galactic RAR at the same g_bar (Chae-type wide-binary claims) **cannot** be the kernel's ω-dependence; in this framework it must be the EFE channel (solar neighbourhood g_ext ≈ 2.3a₀ — the separate, already-published lane, γ ~ 1.05–1.10). **Falsifier:** a confirmed frequency-split RAR at fixed g_bar beyond ~1e-7 kills the published kernel outright — uniqueness leaves no measure freedom to absorb it.

---

## 3. Result (iii): eccentric orbits and dispersion-supported systems — the closure fork, computed

Theorem B makes the first-moment closure exact for any worldline, but off circles the **time-weighting** of |a(τ)|² is the open choice (the repo's own `mi_offcircular_completion_SPEC.py` verdict: FREE, bounded). Two natural members:

- **Closure A (ultralocal):** x_A(τ) = |a(τ)|/a₀ instantaneous → the law is pointwise-algebraic → **every spherical dispersion-supported system sits EXACTLY on the rotation RAR** (identical to spherical MG-with-same-ν). Offset ≡ 0.
- **Closure B (adiabatic / orbit-averaged):** x_B = √⟨a²⟩_orbit/a₀ — the period-averaged first moment, ⟨□_u⟩_orbit = ⟨|a|²⟩_t (the natural action-angle/adiabatic-invariant closure). Solved self-consistently per orbit (fixed point μ̄ = μ_fw(√⟨g_N²⟩/(μ̄a₀))).

**Epicyclic law (analytic, sympy).** For r(t) = r₀(1+ε cos κt) in a local power-law field g ∝ r^(−β):

    Δlog₁₀ g_obs = −(dln μ/dln x)·(C/2)·ε²/ln10,   C = β(2β+1)/2,
    deep-MOND flat-curve limit (β→1): **−0.326 ε² dex** — strictly negative.

MC cross-check at ε = 0.075: analytic −0.00021 dex vs MC −0.00023 dex.

**Monte Carlo (isotropic Plummer tracer, virial-level σ² proxy, 350 orbits/regime).** Deep regime (y(b) ≈ 0.15, dSph-like):

- controlled orbits: ε = 0.24 → −0.0009 dex; ε = 0.41 → +0.0005; ε = 0.62 → **+0.005 dex**;
- isotropic ensemble: **mean −0.024 dex, median −0.011, 16–84% [−0.051, +0.000] dex**;
- alt footing: mean −0.022 dex (footing-stable to ~10%); intermediate depth: mean −0.019 dex.

**Honest finding (the MC overruled the naive conjecture):** the offset is **not one-signed**. Near-circular and moderate-e orbits sit below (apocentre-weighted dressing pulled up by the orbit-rms acceleration), but **plunging orbits (ε ≳ 0.5) flip positive** — in deep MOND the closure-B acceleration at pericentre scales as g_N/μ̄ ~ 1/r versus g_A ~ 1/√r, so the pericentre kinetic pump wins and radial orbits run **hotter**. Same direction as the framework's published σ-hysteresis door (plunging dwarfs run hot, DOI 10.5281/zenodo.20947913 — that is the *external-field-memory* channel of a satellite; this is the *internal-eccentricity* channel of an isolated system; distinct observables).

**The discriminator this yields:** MG-with-same-ν predicts **zero offset and zero anisotropy dependence** for isolated spherical systems. The MI closure-B family predicts an **anisotropy-correlated signed pattern**: isotropic/tangential dispersion systems a few hundredths of a dex **below** the rotation RAR; radially-anisotropic systems pulled back toward or above it. Closure A gives exactly zero — so the framework's derived bracket for isolated dispersion systems is **[0, −0.02…−0.05 dex net, with a radial-bias-correlated positive tail]**. Confound: the EFE pushes MW-satellite dSphs down in both MI and MG readings — the clean test set is isolated quiescent dwarfs, stratified by anisotropy.

---

## 4. Prior art, confronted (fetched 2026-07-16, not from memory)

- **Milgrom 1994 (Ann. Phys. 229, 384):** MI foundations; circular-orbit theorem. Our Theorem A realizes it for this kernel; Theorem B upgrades the reduction to a derived first-moment identity.
- **Petersen & Lelli 2020 (arXiv:2001.03348, A&A 636, A56):** the deep-MOND Q parameter (predicted to differ ~10% between MG and MI); 15 SPARC galaxies pass quality cuts; mean/median Q **mildly favor MG, but both MG and MI agree with the data within 1.5σ** — not decisive either way.
- **Chae 2022 (arXiv:2207.11069, ApJ):** claims "a 6.9σ difference between the inner and outer parts on an acceleration plane which would be inconsistent with current proposals of modified inertia," concluding rotation curves are "most naturally explained by modified gravity." Taken at face value this bites **closure A everywhere and the ring-exactness prediction on truly circular inner orbits** — it is the sharpest standing data threat to this lane's cleanest signature and must be adjudicated by the data lane on SPARC directly (inner regions carry the largest pressure-support/asymmetric-drift/beam corrections, i.e. exactly non-circular contamination, which is where the closure fork of §3 — not the algebraic law — governs this framework's prediction; note our own QUMOND solve (§1) produces an inner-vs-outer split of the same signed kind Chae attributes to MG).
- **Milgrom 2022 (arXiv:2208.07073):** explicit time-nonlocal MI models with conserved charges and exact rotation-curve solutions; MI vs MG differ on the EFE. This is the same model class as our closure-B constructions; his amplitude functionals are pericentre-weighted, consistent with our radial-orbit flip.

We do **not** assert a data verdict here: Petersen–Lelli is a ≤1.5σ non-result; Chae's 6.9σ is a face-value claim against algebraic MI whose contested territory (inner-region non-circularity, EFE handling) is precisely the closure fork this lane has now made quantitative.

## 5. Honesty ledger — derived vs free

**Derived from the published action (no knobs):**
1. Ring-by-ring RAR exactness across the whole first-moment closure family; residual ≲3e-7 (Theorems A, B; rb1).
2. The first-moment identity u·□_u u = −|a|² (any worldline) — the reduction's derivation.
3. The unique Herglotz measure (Herglotz + RAR calibration ⇒ identity theorem); the sum rule ∫dμ/|t| = 1 (region B = 2/π exactly).
4. The unimodular phase law K(−w²+i0) = e^{i arcsin(1/2w)}; frequency universality of the RAR: Δν/ν(wb↔gal, same a=a₀) = +2.3e-8, footing-independent; dissipative scale 2c/a₀ = 203/168 Gyr.
5. The epicyclic offset law −0.326 ε² dex (deep MOND) and the closure-B ensemble bracket (−0.02 dex net; radial-orbit positive flip).

**Free / open (named, not tuned away):**
1. The **closure map** beyond first moment (the O(1) ordering of the nonlinear □_u on a worldline). The literal-frequency closure is dead (no MOND + secular drift ~0.4 m/yr Earth–Sun, pending a cited ephemeris confrontation); inside the surviving first-moment family, circles are degenerate and only non-circular orbits split it (the A↔B bracket of §3). This is the papers' own "off-circular completion FREE (bounded)" — now with the bracket computed.
2. The θ(y) bath-kernel corner ω_c of the EFE channel (separate parametrization; repo SPEC: FREE). A hand-inserted corner at the orbital frequency (Milgrom-1994 averaging postulate) could produce O(1) frequency splits — but no such corner exists in the published action, whose memory time is the horizon scale 2c/a₀.
3. The MOND sign s = −1 (postulate; also owns the dissipation sign). a₀'s value remains underived. No completeness claim.

The sum rule alone does **not** pin the finite-ω response; uniqueness requires Herglotz class + the RAR calibration — with both, everything in §2 is forced.

## 6. Reproduction

```bash
cd /Users/carlzimmerman/new_physics/prep_2026/mi_fingerprint
python3 rb1_circular_exactness.py    # exit 0; 15 checks (ring exactness, first-moment identity, helix gap, QUMOND contrast)
python3 rb2_frequency_dependence.py  # exit 0; 13 checks (measure, sum rule 2/pi + rest, phase law, uniqueness, numbers)
python3 rb3_eccentric_offset.py      # exit 0; 19 checks (closure fork, epicyclic law, MC ensemble, radial flip)
```

Sources read (READ-ONLY): `zimmerman-formula/real_research/papers/MI_COMPLETION_WRITTEN_2026-07.md`, `real_research/reviews/mi_formal_completion_2026/operator_definition.py`, `real_research/reviews/mi_kinetic_completion_2026/kinetic_compute.py`, `real_research/reviews/mi_offcircular_completion_SPEC.py`, `real_research/reviews/MI_NONLOCAL_ECCENTRICITY_2026.md`, `real_research/papers/DSUNRUH_MI_THEORY_2026.md` §4. Prior art fetched: arXiv 2207.11069, 2001.03348, 2208.07073.
