# CFG945 DERIVATION: the satellite hover (F2) in the collapse-gated tether

Criteria: `FROZEN_CRITERIA.md` (618b2fc8b, committed alone first). Amendment A1 (8943d188e, POST HOC, after the first MUTATE run and
before any main-stage number). Every load-bearing step has a sympy or numeric check in `cfg945.py`; check names are in brackets.
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. Cold energy, no particle species. Not "theory closed". Nothing
here says the data favour the framework. K = 4πG, u = |Dχ|, R(u) = u²/(a₀ − u), D_full(u) = u + R(u).

**Overall class (frozen rule): CONDITIONAL.**
- In the gated theory the hover is unchanged: a settled or freely translating satellite medium has θ = 0, so its gate is on.
- **Theorem S** shows that, at leading order, every label-free tether gives the hover. Every label-free candidate tested here (P0/R3θ,
  H2g, H3, H4) stays above the data bound once the full cross terms are included.
- Only a per-label (domain-local) tether, H1, passes (a)–(d). Its price is a non-variational label sector with an open seeding rule:
  - **RESOLVED-WITH-COST.**
  - In effect it is class A's "one tether per catchment", written as fields.
- H2 (baryon anchoring), H3 (equivalence-principle restoration) and H4 (dispersion support) are each **NOT RESOLVABLE**.

---

## 0. The force on a medium element

The gated parent (CFG941 R3θ) is
S = ∫√−g [c⁴R/16πG − mc²n − s(θ)(W_full(u) + (3γ/4K²)τ²) + λ(D²χ − Kmn)] + S_b.

In the static weak-field limit (CFG938 §4, CFG941 §1.2), with Φ = Φ_b + χ:
- a medium element feels f = −∇Φ + s(θ)(D_full û)_L = −∇Φ_b + s R(u)û;
- a star feels −∇Φ.

For a satellite inside a host, χ = χ_h + χ_s and Φ_b = Φ_bh + Φ_bs.

## 1. The hover in the gated theory (Q1, Q3)

### 1.1 The nested gate is on [K5, Q1a]
- The quintic gate has s(0⁺) = 1 and s′(0⁺) = s″(0⁺) = 0.
- θ = ∇_μu^μ vanishes for a static medium and for a uniformly translating one. In Minkowski space this is exact. In a static weak
  field sympy gives θ = −3v ∂_xΦ/c² + O(c⁻⁴), at most 1.3e-22 s⁻¹ for these satellites, against θ_s = H₀ = 2.18e-18 s⁻¹.
- So the satellite's medium has s = 1 whether it rests on its stars or falls with them, and so does the host's medium around it.
  Nesting cannot switch the satellite's gate off.
- The satellite sector of R3θ is CFG938's.

### 1.2 Lemma (re-derived) [Q1a, K2, K6]
- The host part of the force on any medium element in the host's settled region is −g_bh − u_h + D_full(u_h) = −g_bh + R(u_h). The
  host's law (R(u_h) = g_bh) makes this zero.
- Stars feel −(g_bh + u_h).
- So at leading order Δa = u_h + R(u_h) = g_host.

CFG941's full centre-of-mass computation is reproduced exactly (K2: 18 ratios, max relative difference 0): **Δa/g_host = 1.017–1.107**.
Its EFE factors are reproduced exactly too (K6): **−0.102 to −0.728 dex**.

### 1.3 Dynamics (estimates; Q3)
The hover is an instantaneous force balance, so what happens next depends on the satellite's own binding.

**Gate crossing.**
- Once the stars move off, the abandoned medium is no longer balanced. Where the stars' density gradient points along their
  displacement it expands.
- With θ(t) = K|∇ρ_b|max Δa t³/6 (free regime, checked: √ω² t < 1 in every case), θ reaches θ_s in **t_gate = 1.4–13.5 Myr**.
- That is the transition band 0 < θ < θ_s, where R3θ's ghost lives (CFG941 d). The gated theory's prediction during separation is
  therefore not defined until the ghost is cured (CFG944).
- A stationary satellite medium is either tether-supported (s = 1, so it hovers) or supported by something else (H4).

**Separation, with the medium's own pull on the stars included.**
- CFG941 compared Δa with the stars' pull on the medium only. Here the medium is a rigid truncated isolated-law phantom and the stars
  an extended Plummer cloud.
- The relative restoring force is the medium's mean pull on the offset cloud, times (1 + M_b/M_m).
- Its maximum, P_max/Δa, is 0.087–1.68:
  - The stars stay bound in **2/18 cases** (H3 at 250 kpc, both footings; P_max/Δa = 1.67 / 1.68).
  - In the other 16 the stars leave in **9.5–114 Myr** (integrated; CFG941 estimated 9–106 Myr).
- **Correction to CFG941's auxiliary estimate:** the medium's pull binds the stars in the H3 at 250 kpc cases. Elsewhere CFG941's
  reading stands.

**The composite.**
- Momentum conservation fixes the composite's fall whether or not the stars stay bound: a_cm/g_host = 1 − f_m ε, with f_m = M_m/(M_m + M_b).
- The EP violation of the composite is **η = f_m ε = 0.76–1.04**. A bound satellite falls at 0 to 0.24 of g_host, and in the
  H1-at-250-kpc cases it does not fall at all.
- An unbound one loses its medium.

## 2. Theorem S (same point) [Q2]

**Hypotheses.**
- The force on a cold medium element is f = −∇Φ + F(x, v; σ). F may be any functional of fields sourced by the whole system, local
  or through elliptic constraints.
- It depends on the element only through its position x, weakly on its velocity v (F = F₀ + F₁v/c* + …), and on gate scalars σ of
  its own flow that take the settled value for a stationary medium.
- There is no membership label.

**Claim.**
- The host's medium at x is cold, static and in equilibrium: F(x, 0; σ_s) = ∇Φ_h(x).
- So any stationary medium element at x, including a satellite's, feels host force F₁v/c* + δ_cross. Stars feel −∇Φ_h.
- The satellite's own linear self-force has zero centre-of-mass integral (Newton's third law; sympy example ∫ρ αχ′dx = 0).
- Hence Δa = g_host + O(v/c*) + δ_cross.

**Scope (stated plainly).**
- The theorem is exact at leading order in (satellite field)/(host field).
- The cross terms δ_cross are F-specific, so the theorem alone does not fix ε when the satellite's field dominates. Each candidate is
  computed:
  - **P0/R3θ:** the cross term pushes the satellite medium away from the host. A hand estimate in the internal-dominated deep limit
    is ⟨T_z⟩ ≈ u_h[R′(u_s)/3 + 2R(u_s)/(3u_s)] ≈ (4/3)(u_s/a₀)u_h, so ε ≥ 1 (computed 1.017–1.107).
  - **QUMOND-type anchoring (H2g):** the cross term reduces ε (computed 0.48–1.00).

**Escapes.**
- E1: a membership label (H1).
- E2: support specific to the stream, such as velocity dispersion (H4).
- E3: O(1) velocity dependence at satellite speeds.
- E4: a non-stationary satellite medium (the §1.3 transient).

**Corollaries.**
- A velocity-gated tether hovers exactly for a satellite at rest relative to the host medium (apocentres, slow satellites). A moving
  satellite still needs its own χ alone for its own support, i.e. a label.
- A filtered tether, χ_f with (1 − ℓ²D²)χ_f = χ, also hovers: the host's medium at the satellite's point is in equilibrium under the
  same filtered force, for every ℓ. The host's own law needs ℓ → ∞ (CFG941 R3ℓ).

## 3. The data bounds ε_B and δ_c (from the record's numbers)

**Stripping model (frozen).**
- A differential acceleration ε g_host strips a dwarf iff ε g_host > κ_r g_int.
  - g_int = 3σ²/r₁₂, CFG874's own numerator.
  - g_host is the settled law field of the nearer host: MW 6e10 M⊙ at distance_gc, M31 1e11 M⊙ at distance_m31.
- A stripped dwarf's prediction is Newtonian, so its residual rises by log₁₀ ν_e(g_bar/a₀).
- CFG874's primary statistic (reproduced exactly, K4) is recomputed against these predictions for all 65 dwarfs.
- ε_B is the largest ε with c ≥ −2 se.

**Results.**

| footing | satellites' g_int/g_host (min, median) | ε_B, κ_r = 1 (graded) | ε_B, κ_r = 2 | c under the hover, κ_r = 1 | c under the hover, κ_r = 2 |
|---|---|---|---|---|---|
| canonical | 0.099, 1.85 | **0.344** | 0.689 | −0.355 ± 0.114 (−3.1 se; 19 satellites stripped) | −0.230 ± 0.112 (−2.05 se; 12) |
| alt | 0.092, 1.70 | **0.317** | 0.634 | −0.364 ± 0.116 (−3.1 se; 19) | −0.234 ± 0.113 (−2.07 se; 12) |

- ε_B is set by the six satellites most exposed to their hosts. In increasing g_int/g_host (canonical): Sagittarius (0.099), And XVII
  (0.102), And XXV (0.122), Hydrus I (0.245), Boötes II (0.323) and And I (0.344).
- Stripping those six gives c = −0.219 ± 0.098. Sagittarius is a tidally disrupting system, so this is a caveat.
- No isolated dwarf is stripped below ε = 1.38.
- **A1 property:** c sees only satellite-specific stripping. Stripping every dwarf moves c from −0.100 to −0.101, because the shift
  depends on g_bar alone and the matched-g_bar regression absorbs it.

**δ_c and cross-checks.**
- δ_c = c + 2se_c = **0.0816 dex** on both footings. That is the largest satellite-specific deficit CFG874 allows at 2σ.
- Cross-checks from the other lanes' published numbers (2σ deficit bounds):
  - CFG873: D + 2se = +0.043.
  - CFG860: c0 + 2se = +0.094 (alt JSON +0.093); cG + 2se = +0.122 (+0.121).
  - CFG875: k + 2se = +0.109 dex per dex toward the host.
- All are of the same size as δ_c.

## 4. H1: the domain-local (per-label) tether: RESOLVED-WITH-COST

**Action (declared in the criteria).**
S_H1 = ∫√−g [c⁴R/16πG − mc²n − s(θ) Σ_q (W_full(|Dχ_q|) + (3γ/4K²)τ_q²) + Σ_q λ_q(D²χ_q − Kmn_q)] + S_b.
- n_q = n·[Q = q], with Q a membership label carried by the medium.
- D² is taken in the mass-weighted mean medium frame.
- New constants: 0.

**Nesting is compatible with the constraint [H1_nesting_superposition].**
- D²χ = Kmn is linear, so χ_total = Σ_q χ_q exactly. P0 and H1 differ only in W.
- The mixed derivative of W(a + b) − W(a) − W(b) at the origin is W″(0) = 1/(4πG). The cross term a·b/K is exactly the cancelled
  mutual gravity between label a and label b.

**(b) Free fall [H1_force_uniform_field].**
- The label-s medium feels the full host field −(g_bh + u_h), as the stars do, because its tether reads χ_s only.
- Δa = 0 in a uniform host field. MUTATE M2 gives 5e-16.
- In the point-mass law host field, with the satellite domain set by the L2 rule (r_dom = 1.1–34 kpc, r_dom/R = 0.012–0.143), the
  tidal residual is **ε = 1.6e-5 to 2.0e-3**. That is below ε_B and also below CFG941's 0.01 line.
- Rule L1 (field dominance) would hand the whole satellite to the host in 10/18 cases (u_s,max < u_h), restoring the hover there.
  L1 therefore fails, and L2 (tidal dominance, no constant) is required.

**(c) No EFE.**
- In the falling frame the satellite's equilibrium is R(u_s) = g_bs, the isolated law: **uniform-field EFE = 0 dex**.
- The host's tidal field changes the phantom at the scale radius by −0.0002 to −0.052 dex; the largest is H2 at 50 kpc. This is
  reported, not graded: tides of this size are present in any metric theory.

**(a) Static law [H1_two_label_equilibrium].**
- A single-label galaxy is P0: 2.2e-16 on both footings, deep BTFR limit 1, numeric +1.0e-7 at y = 1e-14.
- **Cost:**
  - Two labels in one galaxy obey R(u₁) = g_N + u₂ (sympy). An equal split gives an acceleration floor g → a₀ and misses NGC 3198 by
    4.12 / 4.61.
  - Free debris left by a failed re-latch misses the law by about 2.6q (alt 2.9q): 2.6e-6 at q = 1e-6. So (a) at 1e-6 requires every
    settled galaxy to be single-label to q ≲ 3.5e-7 in mass.

**(d) Well-posedness.**
- Per label, CFG938's conditions are inherited (γ > 0; ρc² > Du/K, margins 5.9e4–2.5e8).
- Two co-located labels with relative speed U: their mutual gravity is uncancelled, so this is a gravitational two-stream problem,
  [(ω − kU)² − Ω₂²][ω² − Ω₁²] = K²ρ₁ρ₂.
  - Max Im ω/√(K(ρ₁ + ρ₂)) = 0.707 over U ∈ {0, 0.1, 1, 10}, ρ₂/ρ₁ ∈ {0.1, 1, 10}, A − 1 ∈ {0, 1} and kL* = 1e-2–1e3.
  - That is bounded Jeans-type growth, independent of k, which (d) allows.
- Energy-momentum is conserved for fixed labels, because the action is diffeomorphism-invariant. It is not conserved across a label
  change (a cost).
- R3θ's ghost is inherited.

**(e) Self-gravity [H1_mode_average_labels].**
- ⟨L⟩ = (K/4k²)[(B + C₁ + C₂)² − c₂(C₁² + C₂²)]. Different labels gravitate Newtonianly for every c₂.
- So tethered–tethered gravity between distinct collapsed objects is **restored**.
- Within one label D-T still forces c₂ = 1, so the settled domain's medium has no self-gravity. The linear regime is dust (gate off),
  with n = 1.

**Is it a local action?**
- **The tether sector, given labels:** yes. It is a local Lagrangian in a continuum of auxiliary pairs (χ_q, λ_q), each with an elliptic
  constraint like CFG938's χ.
- **The label sector:** no action.
  - L2 re-latching is pointwise in fields (|τ_q| from χ_q), but it is non-smooth and non-variational.
  - Seeding labels at collapse needs every element of a collapsing region to agree on one label distinct from every other region's.
  - No local rule was found that guarantees single-label galaxies to q ≲ 3.5e-7. Diffusion of the label in the gate band needs a
    constant and mixes labels; a Lagrangian label kernel needs a galaxy-mass-dependent width.
  - Class A's catchment rule (a turnaround ball around a peak) does this, but it is non-local.

**Costs and open condition (all listed).**
- A non-variational label sector: L2 re-latch, plus a seeding rule that is open.
- A continuum of auxiliary fields.
- Per-label single-stream flow in place of CFG938's condition 5.
- Energy-momentum conserved only between label changes.
- **Open condition:** every settled galaxy single-label.

## 5. H2: tether anchored to baryons: NOT RESOLVABLE

**Anchor reaction lemma [H2_anchor_reaction_lemma, H2_reaction_finite_difference].**
- Coupling the medium to ψ (∇ψ = the law field of the baryons) gives, in spherical symmetry, U_int = ∫M_c(r) ν(g_N)g_N dr.
- Moving a baryon shell outward changes U by −dm·M_c(G/r²) d(νg_N)/dg_N. So the baryons feel an extra **outward** acceleration
  a_R = (dg/dg_N) g_c.
- Its deep limit is **a₀/2** (sympy).
- A finite-difference check on a test shell agrees to 2e-5: 5.6403e-11 against 5.6402e-11 m s⁻².

**The four variants.**

| variant | (a) | (b) | (c) | (d) |
|---|---|---|---|---|
| H2v (variational) | **FAIL**: baryons feel g − a_R; NGC 3198 dev 2.62 / 2.88; 15 / 16 of 43 radii pushed outward. Re-tuning the medium leaves lensing off the dynamics by up to a_R/g = 2.6 (slip line 1.9e-5) | as H2g or H2o | as H2g or H2o | PASS formally: bounded Jeans; the law state is unstable for k < √2/L*, e-fold 280 / 267 Myr at NGC 3198's last radius |
| H2n (non-variational) | PASS (no reaction) | as H2g or H2o | as H2g or H2o | **FAIL**: the medium is pushed with no reaction, so ∂_μT^μν ≠ 0 and there is no action |
| H2g (all baryons) | as H2v or H2n | **FAIL**: ε = 0.48–1.00 (Theorem S plus the QUMOND cross term; local approximation, as CFG941) | **FAIL**: QUMOND-type EFE 0.10–0.73 dex | as H2v or H2n |
| H2o (own baryons) | as H2v or H2n | needs H1's labels | needs H1's labels | as H2v or H2n |

Every realization fails (a), (b) or (d). Own anchoring needs labels and still meets the variational / non-variational dichotomy.
**(e):** with no χ tether the settled medium has full Newtonian self-gravity (F1 and tethered–tethered gravity restored), but (a)
fails.

## 6. H3: equivalence-principle restoration: NOT RESOLVABLE

**No gradient-shift symmetry [H3_no_gradient_shift_symmetry].**
- ∂_b W(|∇χ + b|) at b = 0 is W′(u) = D_full(u)/K, whose linear coefficient is 1 (D-T). So W is not invariant under χ → χ + b·x.
- A uniform external χ gradient is physical. The Einstein elevator removes the metric's uniform gradient, not χ's.
- The law forces W′ ≠ 0, so no symmetry of a single-χ tether can make the satellite blind to the host's χ.

**Passive gravitational mass [H3_passive_mass_zero].**
- The host part of the force on the medium, divided by the stars', is 0 at leading order.
- The inertial mass is m. The corrections are D u/(Kρc²) ≤ 1/5.9e4 (CFG938) and the χ̄ term (Ω_c/6)(ρ̄_c/ρ_c) ≤ 8.0e-8 at the
  satellites' scale radii.
- So m_g/m_i = 0.

**Not a static artefact.**
- The forces are instantaneous (χ and λ are constraints).
- The velocity-dependent corrections are the χ̄ boost |βV|/g_host = 2.5e-3 to 1.3e-2 (up to 2.4e-2 at 300 km/s) and v²/c² ≤ 3.6e-7.
- The rigid two-component integrations (§1.3) show either separation or a composite that fails to fall.

(b) and (c) are P0's (ε 1.017–1.107; EFE 0.10–0.73 dex > δ_c).

## 7. H4: dispersion-supported settled medium: NOT RESOLVABLE

[H4_support_split]
- A host element obeys −g + f_T g + F_p = 0.
- A separate cold stream feels the field force f_T g but not the host's pressure, so Δa = f_T g_host.
- The frozen (a) is a cold static limit, F_p → 0, which forces f_T = 1, i.e. the hover with P0's EFE.
- (b) needs f_T ≤ 0.31 / 0.29, so the two are incompatible.

The warm option (small f_T, the medium supported like collisionless matter) would restore free fall, F1 and tethered–tethered
gravity. But the law would then no longer be the static equilibrium of the action. That is a different theory: CFG941's open item 2,
and the way class A's particles are supported.

## 8. Classes and what is not claimed

| candidate | action change | new constants | a | b | c | d | class |
|---|---|---|---|---|---|---|---|
| P0 = R3θ (reference) | none | 0 | PASS | FAIL (1.02–1.11 > 0.34 / 0.32) | FAIL (0.10–0.73 dex > 0.082) | PASS (ghost inherited) | — |
| H1 per-label tether | Σ_q W(\|Dχ_q\|), λ_q(D²χ_q − Kmn_q), label Q with L2 re-latch | 0 | PASS (single label) | PASS (≤ 2.0e-3) | PASS (0) | PASS (bounded; conservation between label changes) | **RESOLVED-WITH-COST** |
| H2 baryon anchor | +mnψ in place of W, λ(D²χ − Kmn) | 0 | FAIL (H2v) | FAIL (H2g) | FAIL (H2g) | FAIL (H2n) | **NOT RESOLVABLE** |
| H3 EP restoration | none possible (no symmetry) | 0 | PASS | FAIL | FAIL | PASS | **NOT RESOLVABLE** |
| H4 dispersion support | support split f_T | 1 | PASS only at f_T = 1 | FAIL | FAIL | n/a (multistream) | **NOT RESOLVABLE** |

**Overall: CONDITIONAL.** The condition is a label sector that keeps each settled galaxy single-label (to q ≲ 3.5e-7), keeps a satellite's
label through infall, and re-latches debris after disruption (L2). Without labels the hover stands: Theorem S at leading order, and
every label-free candidate above ε_B with the full cross terms.

Not claimed:
- that any local dynamics for the labels exists;
- that H1 is a complete theory;
- that κ, a₀ or L* are derived;
- any data verdict beyond the framework-native bounds above.

Not "theory closed".

## 9. Controls and disclosures

**K: 6/6 pass.**
- K1: 2.2e-16 / 2.2e-16.
- K2: 18 hover ratios, max relative difference 0.
- K3: 3.5e-16.
- K4: CFG874 c = −0.100267 ± 0.090955 (alt −0.100335 ± 0.090970), difference 0, N_I 11, N_S 54.
- K5: gate and θ.
- K6: 18 EFE factors, difference 0.
- B0: the vectorised bootstrap equals the literal one to 1e-12.

**MUTATE: exit 3 (A1 rule).**
- M1: labels removed, the hover returns (difference 0).
- M2: tether off gives 3.5e-16; H1 in a uniform field gives 5.0e-16.
- M3: H2 reaction on gives dev 2.62 / 2.88; off gives 0.
- M4: two labels give dev 4.12 / 4.61.
- M5 as frozen is **TOOTHLESS**: ε = 100 gives c −0.101 (flagged; see A1).
- M5b (A1, post hoc): every matched satellite stripped gives c = −1.181 ± 0.110 (−10.7 se) / −1.220 ± 0.110 (−11.1 se).
- M6: tether off, the stars and medium co-move (separation 0, |a_cm/g − 1| 3e-14).

**Disclosures.**
- **K4's first run failed** at 1e-9 / 2e-10. CFG874 hard-codes the rounded footings, while `CFG4_common.A0` is 2.65e-6 (canonical) and
  3.13e-6 (alt) higher. The replica now uses CFG874's literal values. This was a code fix before any main number.
- **A1 (post hoc).** The frozen tooth M5 was toothless. M5b and exit code 3 were added. ε_B is unchanged. A1 was committed before
  any main-stage number.
- **Main attempt 1 was killed after 11 min.** I attributed the stall to the point-star dynamics (the √d cusp of P(d)) and replaced the
  stars with an extended Plummer cloud plus sparse output.
  - The real cause was a slow two-variable sympy series in the H1 nesting check. That check was replaced by the exact equivalent
    (the mixed derivative at the origin, W″(0)).
  - Attempt 1's captured output (`cfg945_main_attempt1_killed_pointstars.out`) was read only after the final run. It holds the Q3
    table with point stars: **8/18 bound** (all 250 kpc cases and H3 at 100 kpc), against 2/18 with the extended cloud. Every other
    number before H1 is identical.
  - The extended cloud is kept as the more physical model. Q3 is an estimate, and no class depends on it.
  - A second attempt stalled at the same series. Its stdout went to /dev/null.
- **Wording-only correction after the first complete main run.** My printed Theorem S text ("hover for every label-free F") overstated
  its scope. It now reads "exact at leading order; cross terms computed per candidate". All three stages were rerun; no number changed.
- **Implementation choices (not frozen; disclosed).**
  - The satellite medium for P0, H2g and Q3 is CFG941's truncated isolated-law phantom.
  - H2g uses the local approximation (no curl projection), as CFG941.
  - The L2 domain is capped to [a, 100a]; the H1 star cloud is truncated at r_dom.
  - The tidal term is taken on the near-side axis.
  - Q3 uses rigid profiles and Plummer stars to 100a.
  - Restoring field for the bound: g_int (Wolf) with κ_r = 1; nearer host only (generous to the hover).
  - t_gate uses the free-regime estimate.
  - The two-label WKB is in units K = ρ₁ = L* = 1.
- **Compute.** One process per stage, peak RSS ≤ 0.29 GB (`/usr/bin/time -l`), 1–10 s per stage. The memory guard was on (start
  ≥ 12 GB free+inactive; it would exit 75 on swap growth > 1 GB). Runs were beside NC2x. Nothing was downloaded. No other lane's
  file was edited; CFG874's code was exec'd read-only (definitions only) to diagnose K4.
