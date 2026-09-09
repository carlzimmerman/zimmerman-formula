# L67 — emergent MOND: the class the excess-spent-once theorem leaves open by its own hypotheses

`L67_emergent_mond.py` + `.out` — **26 checks, 23 PASS, 3 FAIL; every one of the nine controls passes and every FAIL is
the finding.** Runs in under a second, exit 0. Both a₀ footings (9.3619e-11 canonical, 1.1279e-10 alt) on every
dimensional number; the literature's two parameter sets (BK15: α = 2.5, Λ = 0.2 meV, m = 0.6 eV; BFK18: α = 5.7,
Λ = 0.05 meV, m = 1 eV — recalled from the papers, only α³Λ² pinned by a₀ and Λm³ by the core) carried side by side.

[L61](L61_PERMITTED_BRANCHES.md) proved, branch-independently, that a theory which **(a)** reproduces the deep-MOND relation
with its cold component switched off, **(b)** carries a pressureless component in the CMB's amount, and **(c)** transmits its
pull to baryons no less efficiently in galaxies than at recombination, overshoots the rotation curves pointwise. (c) is
closed on ordering. Every theory this programme has built satisfies (a). **This lane takes the one class that violates (a)
by construction — MOND emergent from the dark sector, with superfluid dark matter (Berezhiani & Khoury 2015; Berezhiani,
Famaey & Khoury 2018) as the representative — and runs it through the gates.**

---

## 0. The answer in one line

> **The hatch is real and the class dies in it. Hypothesis (a) fails for superfluid dark matter (with the condensate off the
> phonon force is identically zero), and on SPARC the P ∝ ρ³ core is so diffuse that the condensate's own pull is ≤ 7% of
> the anomaly — the galaxy anomaly IS spent once, by the phonon, at the CMB's abundance. But the phonon does not bend light
> and its own stress is (1/3)(v/c)² of the phantom, so the class predicts M_dyn/M_lens ≥ 5 where the measured ratio (SPARC
> dynamics against KiDS lensing at the same g_bar) is 1.02; and a condensate normalised to the lensing instead pulls on the
> baryons too, restoring A_X = A_K pointwise and overshooting by 1.64–1.82 — L61's overshoot re-entering through the
> lensing gate. The record had already closed the class on cosmology (superfluid_route_gates_2026, 09-02); this is a second,
> independent closure that does not lean on that run's equation-of-state extrapolation.**

---

## 1. Controls — nine, all PASS

| control | reproduced here | published |
|---|---|---|
| **A1** mode counts | GR **2**, GR+scalar **3**, khronometric **3**, Einstein-aether **5**; GR + phonon **3** | L31/L39/L61 |
| **A2** L61's overshoot | median g_pred/g_obs = **1.692** at η = 1, 2059 deep points | L61 B1: 1.692 |
| **A3** L61's ceilings | **0.355/0.276** (total-sourced), **0.582/0.486** (baryon-sourced) | L49/L50/L61 B2 |
| **A4** the recorded superfluid-route G2/G3 | z_therm = **31235/1324/198** (σ/m = 0.1 cm²/g, v₀ = 1e-3/1/100 km/s); c_s²(z_rec) = **0.33** (200 km/s core at 1e5×), **1.9e-3** (10 km/s at 1e6×) | superfluid_route_gates_2026: 31236/1324/198; 0.33; 1.9e-3 |
| **A5** Lane-Emden n = ½ | ξ₁ = **2.75270**, −ξ₁²θ′ = **3.78865** | tables 2.75270, 3.78865 |
| **A6** KiDS lensing RAR | at the SPARC–KiDS overlap (g_bar ≥ 1e-12) on ν_RAR(1.2e-10) to **0.09/0.06 dex** (raw / hot-gas-corrected); universal across four stellar-mass bins at 30–300 kpc to **0.033 dex** | Brouwer et al. 2021's own statements |
| **A7** κ ↔ α map | α = **0.464** at Λ = Λ_DE for the canonical a₀ | recorded G1: 0.464 |
| **A7b** the literature's a₀ | a₀_ph = **1.17e-10** (BK15) / **8.66e-11** (BFK18) = 0.97 / 0.72 of 1.2e-10 | the coupling is fitted to a₀, like κ |

Two diagnostics are printed and **not** used as controls: the raw isolated KiDS curve sits +0.12 dex above ν_RAR over its
*full* range (the low-g_bar circumgalactic-gas / two-halo excess Brouwer et al. discuss; +0.02 hot-gas-corrected), and
the polytrope's 1e12 M☉ core has ρ₀ = 1.5–1.8e-26 g cm⁻³ (6.6–7.9e3× the mean dark density), R = 119–126 kpc,
central c_s = 223–230 km/s, scaling as M^{1/5}(Λm³)^{−2/5}.

---

## 2. The record, read first: what closed what (B1, B2)

**B1 PASS — the named no-go is of an ADDED sector.** In `THE_ACTION_2026-09-05` the MOND force is 2(2−K_B)J^μ∂_μφ with the
kernel J(Y) carrying a₀; the condensate K(Q) = K₂(Q−Q₀)² supplies dust whose amplitude "is a free cosmological initial
datum"; the static law ∇·[μ∇Φ] = 4πGρ has no dust parameter. g04j's docstring is about keeping "a cold-on-cluster-scales
fluid OUT of galaxies"; g04f's about "the candidate's dark sector as a single thermal species". Every one of g03w–g04j's
closures (four condensates, thermal relic, wave dark matter) is of a component added to a kernel that already works at
zero dust. **Hypothesis (a) holds for all of them, so the named no-go does not cover the emergent class.**

**B2 PASS — but an UNNAMED record does, on one gate.** `qwen_claude_field_theory/closure_2026/condensate_pincer_2026/
superfluid_route_gates_2026.py` (2026-09-02, 4/4) took *"the dark field IS MOND"* — the Berezhiani–Khoury class,
condensing inside galaxies and producing the a₀ force as a phonon — and closed it on the cosmological background: any
self-interaction that thermalises a halo thermalised the background earlier (Γ/H ∝ (1+z)^{2.5}), where nλ_dB³ ≫ 1, so
it condensed and (T/T_c constant under expansion) stays condensed; the condensed background's c_s² ∝ (ρ/ρ_core)² is then
relativistic at recombination for any core the phonons could hold up. Reproduced at A4. **Its scope:** background phase +
the P ∝ ρ³ equation of state extrapolated to recombination densities — the regime the class's own literature flags as
where its EFT is not established. Priced here: a core at 6e3× mean held at 200 km/s has c_s²(z_rec) = 4.4e-7 × (2e5)^{n−1}
for P ∝ ρⁿ, meeting the loose GDM ceiling 1e-5 only for **n ≤ 1.26** — softer than any pressure that could hold the core
(the phonon law needs n = 3). The extrapolation is not the weak point. But that run never touched lensing, the Solar
System, the EFE, the Gaia arms, the preferred frame, or whether the anomaly is spent once. **Those are run here and do
not lean on it.**

The brief's "if the recorded no-go closes the class, say which and stop" was considered: the named no-go does not close
it; the unnamed run closes it on cosmology under an extrapolation; the theorem-driven gates were open and cheap.

---

## 3. Hypothesis (a) fails for the class — derived, not asserted (C1, C2)

From L = P(X) − (αΛ/M_Pl)θρ_b with P = (2Λ(2m)^{3/2}/3)X√|X|, X = μ_loc − (∇θ)²/2m, in the gradient-dominated regime:
P_X/m = 2Λ|∇θ|; the EOM ∇·(|∇θ|∇θ) = αρ_b/(2M_Pl) gives |∇θ| = √(αM_b/(8πM_Pl r²)) and

> **a_θ = (αΛ/M_Pl)|∇θ| = √(a₀_ph a_N),  a₀_ph = α³Λ²/M_Pl** — BK15's scale, recovered symbolically (C1 PASS).

The condensate density in the same regime is ρ_SF = mP_X = 2Λm²|∇θ| (BK15's gradient-locked density). **Switch the cold
component off: ρ_SF → 0 forces P_X → 0, the flux coefficient vanishes, and the EOM carries no force — A_K ≡ 0, not
√(g_bar a₀).** L61's (H-b) — "with A_X = 0 the theory reproduces the observed relation" — is false for the class, the
proof step g_obs = g_bar + A_K cannot be taken, and the conclusion g_pred − g_obs = A_X does not follow. **C2 PASS:
hypothesis (a) fails, exactly as the brief conjectured.** What replaces it is g_pred = g_bar + g_SF + a_θ with a₀_ph a
fitted constant — and whether the anomaly is spent once becomes a computation.

---

## 4. Spent once (D1, D2) — the hatch is real

The cold component is present at the abundance-matched amount (L61's M200) but with the theory's own profile: the
n = ½ polytrope (BFK18's finite-temperature picture; core mass f_core × M200, f_core = 1 and 0.3) and BK15's gradient-locked
ρ_SF ∝ |∇θ| ∝ 1/r. Median of g_SF/(g_obs − g_bar) over the deep-MOND SPARC points:

| profile | set | f_core | share, can / alt | g_SF/a_θ at 10 kpc, L* |
|---|---|---|---|---|
| polytrope core | BK15 | 1.0 | **0.023 / 0.023** | 0.014 |
| polytrope core | BK15 | 0.3 | 0.014 / 0.014 | 0.009 |
| gradient-locked | BK15 | — | 0.066 / 0.066 | 0.046 |
| polytrope core | BFK18 | 1.0 | 0.028 / 0.028 | 0.020 |
| polytrope core | BFK18 | 0.3 | 0.017 / 0.017 | 0.012 |
| gradient-locked | BFK18 | — | **0.070 / 0.069** | 0.056 |
| abundance-matched NFW (L55/L61) | — | 1.0 | **1.086 / 1.085** | |

**D1 PASS — spent once.** The P ∝ ρ³ core is cored with R ~ 120 kpc, so the halo mass sits at ~100 kpc rather than 10 kpc:
the cold component is "somewhere other than in galaxy halos" in exactly the sense L61 caveat 1 names. A superfluid with
its own stiff equation of state achieves the redistribution the added-sector no-go said a lapse-coupled condensate
cannot — at the cost §2 records.

**D2 PASS.** Fitting the one constant a₀_ph on the deep points: with the condensate present the fitted scale moves by
**0.82–0.90** of its no-condensate value and the rms by ≤ 0.013 dex (every profile, set, footing); the NFW halo at the
same abundance cuts it to **0.26** and adds 0.09 dex — L61's overshoot. (The fitted a₀_ph itself sits at ~0.55 × 1.2e-10
even with no condensate: that is the zero-temperature √ law's lack of an interpolation in the 0.3–1 a₀ transition, not
double counting; D3 prints the high-acceleration diagnostic, −0.09/−0.11 dex at g_bar > 3a₀, unscored.)

---

## 5. The gates

| gate | verdict | the number |
|---|---|---|
| **1 lensing vs dynamics** | **DEAD** | E1a: phonon stress / phantom = **(1/3)v_N²/c²** (symbolic; median 2.4e-8 on SPARC). E1b: measured M_dyn/M_lens at the SPARC–KiDS overlap **1.02 raw / 1.02 hot-gas-corrected** (249 SPARC points vs the interpolated KiDS isolated curve); class **5.17–6.65** there, ≥ **2.96** median over all deep points. E1c: on the KiDS mass bins at 30–300 kpc the gradient-locked profile is uniformly **≥ 0.29 dex low** (factor 1.9 in lensing mass) and the polytrope spreads **0.58 dex** across bins where the data are universal to **0.033 dex**. E1d: the lensing-normalised horn overshoots the rotation curves by **1.64–1.82** |
| **2 Solar System** | **NOT PASSED** | bare phonon at Saturn: phantom mass **1.7–2.0e7×** the Pitjev–Pitjeva bound; X(Saturn) = αM_Pl a_N/2m = **0.72 / 0.98 eV** against m = 0.6 / 1 eV — the non-relativistic EFT reaches its boundary at a_N = 5.4–6.6e-5 m s⁻², Saturn's orbit; the chemical-potential (linear, G_eff = 3–4 G) regime lies *below* a_* = 0.16–0.21 a₀, in galaxy outskirts, not in the Solar System; the environmental escape is closed by sf06 (the Sun at 0.67 of the Galaxy's MOND radius). The literature defers to unspecified higher-derivative operators; **no computable pass exists** |
| **3 preferred frame** | **CARRIED** | §7 |
| **4 tensor speed** | PASS | c_T = c (GR tensor sector); phonon c_s = 226–233 km/s in the core |
| **5 mode health** | not deciding | 3 modes; c_s² = 3Kρ² > 0 inside the condensate |
| **6 clusters** | PASS by inheritance | the un-thermalised bulk is cold collisionless matter at the cosmic abundance (Bose-enhanced Γt_dyn: galaxy 1e2–9e2, cluster at 1 Mpc 9e-3–7e-2, ratio 1.2e4); the cluster is ΛCDM's, which g04a says is what the residual needs. **Not a computed cluster fit** |
| **7 cosmology** | CLOSED IN THE RECORD | superfluid_route_gates_2026 G2/G3, reproduced at A4 |
| **L21 ladder** | PASS on the systematic | each L* member's core R = 141–150 kpc > r_p = 132 kpc, so the pair is INSIDE the superfluid: enclosed condensate 26–29 M_b plus a phonon force 8–10× Newton → M_dyn/M_b = **36.8 / 38.2** vs 31.9 ± 1.6 needed (+0.06/+0.08 dex, 3.1–3.9σ_stat, inside the 0.3 dex abundance-matching systematic). The ladder's non-monotonicity (pairs 30.9, clusters 5.7) is ΛCDM's stellar-to-halo relation, inherited; the superfluid transition does not produce it |
| **Gaia arms** | **outside both** | §6 |

### 5.1 The pincer, stated as the theorem it is (E1d)

The class can have the lensing or the dynamics, not both. Normalise the condensate to the lensing (M_SF = M_phantom at
every radius, whatever profile that takes): then g_lens = g_RAR, and the same mass pulls on the baryons, so
g_dyn = g_RAR + a_θ — median g_dyn/g_obs = **1.758 / 1.817** (BK15, can/alt), **1.643 / 1.702** (BFK18), against L61 B1's
kernel + NFW **1.692**.

> **In a theory whose MOND force acts on baryons but not on light, lensing = dynamics forces A_X = A_K pointwise — which is
> (H-a) + (H-c) with η = 1. The lensing gate RESTORES L61's hypotheses, and the overshoot is L61's.** The only escape is a
> phonon that also deflects light — a coupling to the photon stress, i.e. a disformal coupling — which is L61's branch 3,
> dead at the tensor-speed gate by the E1 identity (the slip repaired is the cone tilt created).

This is the structural result of the lane: the excess-spent-once theorem has one hatch, and the hatch closes through
lensing, because the same physics that lets the class spend the anomaly once in dynamics (a force baryons feel that is
not mass) is what makes it fail to spend it at all in lensing.

---

## 6. The external-field effect and the registered Gaia arms (E6)

Linearised about the Galactic gradient, ∇·(|∇θ|∇θ) = αρ_b/2M_Pl becomes an anisotropic Poisson equation with
D = |∇θ_e|(1 + êê): AQUAL's EFE with μ(x) = x exactly (L = 1) and no interpolation. A binary's phonon force over Newton is
√(a₀_ph/a_N,ext) × A_geo with a_N,ext the Galaxy's *baryonic* Newtonian field (the registration's y_extN = 1.28903 a₀) and
A_geo = 0.809 (sphere-averaged; along the field 1.000, across 0.707, ratio √2 with the ALONG direction larger).

| set | footing | force boost | **γ_v** | Arm A band | Arm B ceiling |
|---|---|---|---|---|---|
| BK15 | canonical | 1.796 | **1.3402** | 1.1614–1.1814 | 1.0450 (corrected 1.0000) |
| BK15 | alt | 1.725 | **1.3135** | 1.1917–1.2267 | 1.0300 (corrected 1.0000) |
| BFK18 | canonical | 1.685 | **1.2981** | 1.1614–1.1814 | 1.0450 |
| BFK18 | alt | 1.624 | **1.2744** | 1.1917–1.2267 | 1.0300 |

**E6 FAIL — the class's prediction falls inside neither registered arm**: γ_v = 1.274–1.340 sits 3.3–4.1σ_tot above Arm A's
upper edges and above the 1.23 no-verdict edge, 10–12σ above Newton. **A DR4 result inside Arm A's band, or Newtonian,
is evidence against the phonon; DR4 cannot confirm it.** Stated against the class: this is the point-field EFE asymptote
(the status of Amendment 9's provisional number), not a full nonlinear solve. The anisotropy sign — along-field boost
larger by √2 in force — is testable by the registered Arm-A sample-level rule. Nothing here touches the preregistration.

---

## 7. The preferred frame, and the unification (E7)

The phonon EFT is the non-relativistic limit of a Lorentz-invariant P(X), X = −(∂θ)², expanded about θ = mt: X̄ = m² > 0,
a **timelike gradient vev** — spontaneous Lorentz breaking with the condensate's rest frame as the distinguished u = ∂θ̄/m.
Verified symbolically: h^{μν}∂θ∂θ = |∇θ|² with h = g + uu, so **MOND's argument is exactly L31 Q3's projector contraction**.

**E7 PASS — the class carries a preferred frame in L31's sense, realised by MATTER rather than by geometry.** But u
propagates (the phonon; N = 3 by A1), so this is L61's arm (1c) — a scalar with a timelike gradient vev — not L31's
non-propagating foliation. The extra mode is the price, and it is a mode that does not bend light, which is why gate 1
closes it.

> **The unification, stated:** L31 says a non-propagating MOND scalar needs a distinguished timelike u; L61 says a
> propagating Lorentz-invariant one cannot lens. The superfluid is the matter realisation of the first sentence and dies
> on the second. Where there is no condensate there is no frame and no MOND — L31 Lemma 1 read as a phase.

---

## 8. Verdicts

**F1 FAIL** — the class escapes (a) [C2], spends the anomaly once in dynamics [D1/D2], and dies at gate 1 [E1b–E1d];
gate 2 is not passed [E2]. **F2 FAIL — the emergent-MOND class, represented by superfluid dark matter, is DEAD**, at
the lensing gate, independently of the recorded cosmological closure.

### Three-sentence verdict

**The emergent class is real and the theorem's hatch is real: with the condensate off the phonon force vanishes, so L61's
hypothesis (a) fails by construction, and on SPARC the P ∝ ρ³ core is so diffuse that the condensate's own pull is a few
percent of the anomaly (7% at worst) — the galaxy anomaly IS spent once, by the phonon, at the CMB's abundance.**

**It dies at the first gate: the phonon does not bend light and its own stress is (1/3)(v/c)² of the phantom, so the class
predicts M_dyn/M_lens ≥ 5.2 where the measured ratio is 1.02 (SPARC dynamics against KiDS lensing at the same g_bar), its
lensing at 30–300 kpc is ≥ 0.3 dex low or spread 0.6 dex across mass bins where the data are universal to 0.03 dex; and
normalising the condensate to the lensing instead restores A_X = A_K pointwise and overshoots the rotation curves by
1.64, which is L61's overshoot re-entering through the lensing gate.**

**Two independent closures therefore stand — the recorded cosmological one (background condensed and relativistic at
recombination, reproduced) and this lane's lensing one, which does not lean on the equation-of-state extrapolation —
while the class's distinctive Gaia number, γ_v = 1.27–1.34 with the along-field boost larger, sits above both registered
arms and is the one thing DR4 could still say about it.**

---

## 9. Caveats, stated rather than buried

1. **The representative is the zero-temperature BK15 law plus BFK18's polytrope.** BFK18's finite-temperature term (the
   interpolation that gives the phonon a Newtonian limit) is not modelled; D3 prints what its absence costs at g_bar > 3a₀
   (−0.09/−0.11 dex) and it is not scored. No gate verdict depends on the transition region.
2. **The parameter sets are recalled from the papers**, flagged as such in the code; a₀_ph = α³Λ²/M_Pl is what the
   gates use and both sets land within a factor 1.5 of 1.2e-10 (A7b). The lensing kill is a ratio of the phonon force to
   the condensate's pull and moves by < 15% between the sets.
3. **Dipolar dark matter (Blanchet & Le Tiec) is in the class and is NOT run.** Its polarisation sources the metric, so
   it passes gate 1 by construction; but its MOND regime requires the medium's monopole not to cluster like CDM in
   galaxies (its "weak clustering" hypothesis), which is (H-c) without a mechanism, and L61 B5's density ordering applies
   to it directly. A pressure-supported medium would face §2's cosmological closure. Recorded as untested, not as dead.
4. **The measured M_dyn/M_lens = 1.02 is the RAR-as-universal-relation reading**: SPARC's deepest points (dwarfs at
   5–20 kpc) against KiDS's isolated lenses (~10^10.5 M☉ at 30–100 kpc) at the same g_bar — the comparison Brouwer et al.
   make. Both the raw and the hot-gas-corrected curves give 1.02 at the overlap.
5. **The polytrope's mass is the abundance-matched halo's** (0.3 dex systematic on log M200). The across-bin spread it
   inherits from abundance matching is shared with NFW (0.49 dex) and is the differential failure
   `h_kids_halo_bound_CORRECTION` (b) records; the class-specific statement is the gradient-locked profile's uniform
   0.29–0.42 dex deficit, which is a function of g_bar alone and independent of M200.
6. **Gate 6 is inherited, not computed.** The cluster verdict is ΛCDM's; the galaxy/cluster thermalisation contrast is
   BK15's Bose-enhanced rate at representative densities, not a solved phase boundary.
7. **The Gaia number is the point-field EFE asymptote**, like Amendment 9's provisional value; a full nonlinear solve
   would move it at the level Amendment 10's did for Arm A (~0.05). It stays outside both arms at that level.
8. **The recorded cosmological closure is CITED and reproduced, not re-derived.** Its EoS extrapolation is priced (§2:
   n ≤ 1.26 would be needed) and found not to be the weak point; this lane's kill does not use it.
9. **Nothing here favours any framework over ΛCDM and nothing here constrains ΛCDM.** The halo abundance is ΛCDM's,
   imported wholesale; κ = ½ remains **fitted**; a₀ ∝ H(z) remains the surviving distinctive prediction of the deposited
   theory, untouched by this lane.

---

## 10. Reproduction

```
python3 fable_independent_2026/L67_emergent_mond.py
```

Exit 0, < 1 s. **26 checks: 23 PASS, 3 FAIL** (E6, F1, F2 — the findings). Nine controls rebuild the four mode counts,
L61's overshoot and both ceilings, the recorded superfluid-route G2/G3 numbers, the Lane-Emden constants, the KiDS lensing
pipeline at the overlap and its across-bin universality, and the κ ↔ α map — each from committed data or from scratch in
sympy. Nothing under `closure_2026/` or the lead's directories is imported or executed.
