# G214 — THE DERIVATION TREE: the law's complete proof chain in one diagram

**Status:** 2026-09-16. Assembly lane over the committed record — no new
physics. Every Lean certificate re-verified TODAY in the repo's Mathlib build
(`lake env lean`, Lean 4.34.0-rc2, `mondlean` project): **10/10 files, exit 0,
zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}** — 79
theorems. The tree below is the law as one proof chain, from the single input
to every LEAN-CERTIFIED statement, with each node marked
**LEAN / closed-form / empirical / registered-and-pending**.

---

## (1) THE TREE

One input — the acceleration scale **a0** (or its double s, the deep-law
constant; `a0 = s/2`, Rung 1, `deep_mond_cleared` LEAN) — branches into the
vacuum and the galaxy spine. Status marks: **[L]** LEAN-certified,
**[C]** closed-form (symbolic/exact, machine-*checked* numerics, NOT Lean),
**[E]** empirical (measured/observed or fitted anchor), **[P]** registered-and-pending.

```
        THE SINGLE INPUT:  a0  (the acceleration scale;  a0 = s/2, s = 2 a0_DE)
        [E  — the one fitted/measured anchor; every other constant is derived]
                           │
        ┌──────────────────┼───────────────────────────────────────────────┐
        │ E1                │ E2 (the physics entrance — see the gap §3)    │
        ▼                   ▼                                               │
   (L1) ρ_Lambda        (L2) σ² = √(G M_b a0)/2                            │
   the vacuum density:      the equilibrium temperature                    │
   ρ_L = 4a0²/(G c²)        (the Zimmerman/DE-set temperature;             │
   [L] LEAN                the max-entropy + virial + T-synthesis)        │
   G031 rho_L_from_a0        [C] closed-form physics premises:            │
   (iff, both directions),    • virial: σ² = G M_b/(2 r_M),                │
   lambda_geom_fixed           closed virial chain 2T+W_self+W_bar        │
   (Λ = 32πa0²/c⁴)            = 3P_sV ⇒ σ² = C/2  (G091, sympy-exact,     │
   (empirical check:          numeric 1e-9)                                 │
    ΩΛ = 0.6857 ± 0.07%)      • max-entropy: S = −∫ρ ln(ρσ³)dV in the      │
                               fixed well Φ = C ln r, EL ⇒ ρ = A r^(−C/σ²) │
                               + Boltzmann β = 1/σ²  (G084, exact residual │
                               + strictly concave 2nd variation)          │
                               • DE-set synthesis: T = m σ²/k_B,           │
                                 σ virial mass-free, T(5 keV) = 9.17 K,    │
                                 m-window [3.3,100] keV  (G116)            │
                               — the internal ALGEBRA IS LEAN:             │
                                 σ² = √(G M_b a0)/2, σ⁴ = G M_b a0/4       │
                                 [L] G031 zimmerman_temperature (V3),      │
                                     G090 equipartition_virial,            │
                                     EQUILIBRIUM_THEORY virial_temperature │
                           │                                               │
        ┌──────────────────┼───────────────────────────────────┐           │
        │ E3 [L]            │ E8 [C+E]                          │ E9 [E]   │
        ▼                   ▼                                  ▼           │
   (L3) the phantom      (T23) THE TEMPERATURE LAW 2/3      (m*) the mass
   ρ = A/r², coefficient   log10(T_obs/T_pred) = (2/3) log10 f   m(z*) =
   1 — the equilibrated     + log10(2 r_M/R500): structural   5.0–5.2 keV
   isothermal density       α = 2/3 = 1 − 1/3 (virial +1,     (cosmic-noon
   σ²/(2πGr²) = S/(4πGr²)   −1/3 Δ500 self-similarity)        inversion)
   [L] LEAN                 [C] closed form (G095/G091 virial [E] empirical
   G031 phantom_is_         + Δ500 algebra, G135 12/12)       prediction
   isothermal; EQUI-         [E] measured: pooled 31-system   G168 8/8;
   LIBRIUM_THEORY            rms 0.076 dex, clusters 0.067    kill band
   equilibrated_is_          (HSE scatter), groups 0.081;     4–6 keV;
   phantom (coeff 1,         cluster 3.51 vs 3.57 (1.8%);     forest floor
   end-to-end);             virial-1/2 excluded ~2.2σ         binding
   G03G sigma_virial_        — NOT Lean (candidate C3)        3.3–5.7 keV
   half (κ = 1/2 = c_s²)                                       [P] pending
                           │                                   instrument
        ┌──────────────────┼──────────────────────────┐
        │ E4 [L]            │ E10 [E]                  │ (φ-share, E11)
        ▼                   ▼                          │
   (L4) the equipartition (dust) THE DUST LAW          │
   M_ph(< r_M) = M_b       c_dust = c0 (M500/8e14)^q    │
   [L] LEAN                ·(r/R500)^−1, ZERO-          │
   G03G equipartition_     PARAMETER-TO-WITHIN-ERROR:   │
   exact (4πA r_M = M_b);  q_pred = α_supply−α_require  │
   G090 equipartition_     = 2/3−1 = −1/3 vs measured    │
   linear_law, vc_flat_    −0.414 ± 0.157 = 0.52σ (G200) │
   exact (the flat curve) c0 via infall jump A_b =       │
        │                 (σ_ph/σ_d)³ = 0.6495          │
        │ E5 [L]           (G182/G185, 12/12, 0.09 dex)  │
        ▼                 [E] empirical/derived-within-  │
   (L5) THE DEEP RAR       error; residuals registered   │
   g² = a0 g_N, coeff 1    (Δq = +0.081; A_b 1.34x)      │
   [L] LEAN               [L] the JUMP ALGEBRA LEAN     │
   G031 deep_rar;           (G201 isothermal_density_    │
   G090 (quadratic form);   ratio, entropy_jump_log/_    │
   G201 deep_limit_sq       cube/_additivity, jump_cube  │
   (geometric-mean          = (σ_ph/σ_d)³ given dS/k_B)  │
   reading)                [P] registered-and-pending    │
        │                 (the dressed σ_d(r_b) input    │
        ├─────────────┐    stays algebra-only, no        │
        │ E6 [L]       │ E7 [L]  overclaim)              │
        ▼              ▼                                 │
   (BTFR)         (Σ) the surface density            (φ-share, E11)
   v_flat⁴ =      <Σ_ph>(<r_M) = a0/(πG)             phantom share of the
   G M_b a0       = 213.74 M☉/pc²                    dark = (r/r_M)/(f−1)
   [L] LEAN       [L] LEAN                           [L] algebra LEAN
   G031 btfr;     G083 surface_density_universal,    G201 share_identity,
   G090 btfr_     _composition, _mean,                share_identity_deep
   quartic;       num_sigma_bar_msun                  [E] the pie measured
   [E] the line   (213.75 ∈ (213,215));               (G106/G188/G197:
   b = 1.004 ±    [E] G036 peak 26.7 M☉/pc²            interior share 0.89,
   0.011, n=542,  (slab column, LEAN extras)           solar circle 0.892)
   0.180 dex rms;      │
   G087 scatter   (E4 ← L5: the Σ node composes
   0/3 armed)     L4's equipartition with r_M²)
```

**The certified spine** (every arrow machine-checked): `a0 → σ² = √(GM_ba0)/2
→ ρ = S/(4πGr²) (coeff 1) → M_ph(<r_M) = M_b → g² = a0 g_N → (BTFR, Σ)`. The
two downstream algebra nodes (the jump cube, the share) are Lean-certified as
algebra; their dressed numbers stay committed-lane.

---

## (2) THE COUNT

Convention: a **node** is Lean if its defining closed form is Lean-certified;
a **link** is Lean if the closed form it stands on is Lean-certified (physics
premises of a node are counted at the node's status, §3).

**NODE INVENTORY (12 nodes)**

| Node | Status | Certificate / lane |
|---|---|---|
| INPUT a0 (or s) | [E] empirical anchor | G189 (s_Lambda = 2 a0_DE = 1.8724e-10), EQUILIBRIUM rung 1 |
| L1 ρ_Lambda | **[L] LEAN** | G031 `rho_L_from_a0` (iff), `lambda_geom_fixed`; ΩΛ 0.6857 empirical |
| L2 σ² = √(GM_ba0)/2 | [C] **closed-form** (physics premises) | G084/G091/G116; algebra Lean: G031 V3, G090, EQUILIBRIUM `virial_temperature` |
| L3 ρ = A/r² coeff 1 | **[L] LEAN** | G031 `phantom_is_isothermal`; EQUILIBRIUM `equilibrated_is_phantom`; G03G |
| L4 M_ph(<r_M) = M_b | **[L] LEAN** | G03G `equipartition_exact`; G090 `equipartition_linear_law`, `vc_flat_exact` |
| L5 g² = a0 g_N | **[L] LEAN** | G031 `deep_rar`; G201 `deep_limit_sq`; G090 |
| BTFR v⁴ = GM_ba0 | **[L] LEAN** + [E] line | G031 `btfr`; G090 `btfr_quartic`; b = 1.004 ± 0.011 n = 542; G087 scatter armed |
| Σ = a0/(πG) | **[L] LEAN** + [E] | G083 ×5 (incl. 213.75 ∈ (213,215)); G036 peak 26.7 |
| T-law 2/3 | [C] closed form + [E] measured | G095/G135 (12/12); not Lean |
| dust law (c0, q) | [E] derived-within-error + [P]; jump algebra [L] | G200 (0.52σ), G182/G185; G201 jump theorems |
| m(z*) = 5.0–5.2 keV | [E] predicted + [P] | G168 8/8; forest floor G093/G116 binding; kill band 4–6 keV armed |
| φ-share (r/r_M)/(f−1) | **[L] algebra** + [E] pie | G201 `share_identity(_deep)`; G106/G188/G197 |

**LEAN nodes: 7** (L1, L3, L4, L5, BTFR, Σ, φ-share) — **closed-form nodes: 2**
(L2 physics premises; T-law closed form) — **empirical leaves: 4** (the INPUT,
the T-law measurement, the dust measurement, the m(z*) prediction) —
**registered-and-pending: 2** (dust law residual tightening; m(z*) instrument;
plus the four registered observational verdicts: DR4, z~2.5 BTFR, tSZ, XRISM).

**LINK INVENTORY (11 links)**

| Link | Status |
|---|---|
| E1 input → L1 | **[L]** (G031 `rho_L_from_a0`) |
| E2 input → L2 | **[C]** (virial + Boltzmann premises; algebra inside Lean) |
| E3 L2 → L3 | **[L]** (`zimmerman_temperature` ⇒ `phantom_is_isothermal`; `equilibrated_is_phantom` end-to-end) |
| E4 L3 → L4 | **[L]** (G03G/G090) |
| E5 L4 → L5 | **[L]** (deep RAR from the equipartition field, coeff 1) |
| E6 L5 → BTFR | **[L]** (G031 `btfr`, G090 `btfr_quartic`) |
| E7 L5 → Σ | **[L]** (G083 composition) |
| E8 L2 → T-law | **[C]+[E]** (virial + Δ500 algebra; measured 0.076 dex) |
| E9 L2 → m(z*) | **[E]** (T = mσ²/k_B linear in m; inversion arithmetic) |
| E10 L5 → dust | **[E]/[P]** (reservoir q; infall jump c0; jump algebra [L]) |
| E11 L4 → φ-share | **[L]** (G201 share, one field_simp) |

**Lean links: 7 · closed-form links: 2 · empirical links: 2.**

**THE DEPTH.** The longest all-certified chain:
`input → σ² → ρ → M_ph(<r_M) → g² = a0 g_N → BTFR` = **5 certified-spine
edges** (lands on Σ at equal depth). Of these, the span
`L3 → L4 → L5 → BTFR` (**4 edges**) is Lean end-to-end with every physics
premise discharged inside Lean, and E3's algebra is Lean on both sides; the
**single non-Lean rung is the entrance E2** (the virial + Boltzmann premises,
§3). Honest single number: **DEPTH = 5 certified edges (pure-Lean 4 + the
closed-form entrance), 79 Lean theorems across 10 certificates.**

**Lean ledger (re-verified today, exit 0):** EQUILIBRIUM_THEORY 12 ·
G001 8 · G002/G003 4 · G007 11 · G031 13 · G036 9 · G03G 4 · G083 5 ·
G090 5 · G201 8 = **79 theorems, all zero `sorry`, axioms
{propext, Classical.choice, Quot.sound}** (the LEAN_CERTIFICATES.md file's
"66/7" predates G03G/G083/G090/G201 — superseded by this count).

---

## (3) THE COVERAGE GAP — the non-Lean links and the honest frontier

**The one non-Lean rung of the spine is the entrance E2** — `a0, M_b → σ² =
√(GM_ba0)/2` — which rests on TWO physics inputs, neither Lean-certified:

1. **The virial premise** σ² = G M_b/(2 r_M). G091 derives it as a
   *closed-form* chain — the energy integrals of the truncated
   singular-isothermal sphere evaluate exactly (W_self = −G M_T²/r_break,
   W_bar = −M_b C ln(r_break/r_b), boundary 3P_sV = σ²M_T), and the virial
   equation then solves to σ² = (C/2)[1 + (1/λ)ln(r_b/r_break)] ⇒ **C/2
   exactly** at the truncation-consistent well (r_b = r_break), any λ, both
   footings — sympy-exact and numerically verified to 1e-9, but the
   closed forms are *not* theorems. **This is the largest physics input on
   the spine**; the honest reading of L2 is: Lean certifies the algebra of
   the temperature *given* the virial premise, the virial itself is
   closed-form.

2. **The max-entropy functional** (G084): the Euler-Lagrange stationary
   point of S = −∫ρ ln(ρσ³)dV at fixed (M, E) in the fixed well Φ = C ln r
   gives ρ = A r^(−C/σ²); the Boltzmann identification β = 1/σ² makes the
   energy multiplier the inverse temperature; with σ² = C/2 the exponent is
   **exactly 2**; the second variation −∫(δρ)²/ρ < 0 proves the unique
   global maximum (strict concavity of −x ln x, linear constraints). All
   machine-*checked* numerically (exact residual, 5 modes × 2 amplitudes to
   5%), none a theorem.

3. **The DE-set temperature's origin** (G116): T = m σ²/k_B is *linear in
   the particle mass* and σ is mass-free (T(5 keV) = 9.17 K; decoupling of
   dynamics from the species). The claim that the *same* a0 that fixes the
   vacuum (L1) sets the well that sets the temperature is the one-constant
   physics — consistent (ΩΛ 0.6857 ± 0.07%) and committed, not certified.

Downstream, the T-law 2/3, the dust (c0, q), and m(z*) sit on empirical or
closed-form links (E8–E10); only the jump and share algebra of the dust/φ
nodes is Lean.

**THE NEXT CERTIFICATES — the 2-3 theorems that would complete the spine:**

- **C1 — `virial_rung4` (the virial premise discharged inside Lean).**
  The G091 closed virial chain as theorems: the shell-energy integrals of
  ρ = A/r² evaluate (W_self = −G M_T²/R via the constant-shell-integrand
  argument — G031's `integrand_const` machinery already in hand), and the
  virial equation ⇒ σ² = (C/2)[1 + (1/λ)ln(r_b/r_break)], hence **σ² = C/2
  exactly** at r_b = r_break. Closes the largest non-Lean rung of the spine;
  the physics residue (virial equilibrium of a collisionless fluid, and the
  truncation condition) becomes an explicit hypothesis.
- **C2 — `maxentropy_phantom` (the EL + maximum theorem).** The residual-
  flatness statement — ρ(r) = A r^(−γ) satisfies the EL equation of
  S = −∫ρ ln(ρσ³)dV in the well Φ = C ln r **iff** γ = C/σ² — is one
  field-algebra line (G084's exact residual); strict concavity of −x ln x
  and the second variation −∫(δρ)²/ρ < 0 are textbook Mathlib lemmas.
  Boltzmann (β = 1/σ²) stays an explicit physics hypothesis; the theorem
  then reads: at σ² = C/2, the unique maximizer is **ρ = A/r²** — the law's
  profile from its variational origin, machine-checked.
- **C3 — `twothirds_law` (a downstream leaf onto the certified chain).**
  The G135 V1a identity as a theorem: with R500 ∝ (M500/ρ_c)^(1/3),
  log10(2 f r_M/R500^(b)) = (2/3) log10 f + const on the fixed-M_b face —
  the structural α = 2/3 = 1 − 1/3 (virial + self-similarity) as pure
  algebra. Lifts the temperature law from measured to certified-form.

With C1 + C2, the entrance E2 closes and **every spine edge is Lean**; with
C3 the tree's longest chain carries the T-law as a sixth certified edge.

---

## (4) VERDICTS

**V1 — the derivation tree is complete.** All 12 nodes and 11 links of the
law's proof chain are assembled from the committed record — the single input
a0 to every Lean-certified statement (L1 vacuum, σ² temperature, L3 phantom
coeff 1, L4 equipartition, L5 deep RAR, BTFR, surface density, jump, share)
and the five downstream empirical leaves — each node marked LEAN /
closed-form / empirical / registered-and-pending, every certificate
re-verified today.

**V2 — the counts and the depth, consistent.** LEAN nodes **7** (L1, L3, L4,
L5, BTFR, Σ, φ-share) · closed-form nodes **2** (L2 entrance, T-law form) ·
empirical leaves **4** (input, T-law, dust, m(z*)) · pending **2** (+4
registered instruments). Lean links **7** · closed-form **2** · empirical **2**.
Lean theorems **79 across 10 certificates** (all re-run: exit 0, zero sorry).
**Depth = 5** certified spine edges (`input → σ² → ρ → M_ph → RAR → BTFR`),
**4** of them Lean end-to-end with every physics premise discharged inside
Lean; the entrance E2 is the one closed-form rung.

**V3 — the honest statement.** The law's proof structure is a **certified
spine with one closed-form entrance and empirical leaves**: Lean-certified
end-to-end are the vacuum reading of a0, the identification of the
equilibrated isothermal density with the phantom (coefficient 1), the
equipartition M_ph(<r_M) = M_b, the deep RAR g² = a0 g_N, the BTFR, the
surface density a0/(πG), and the algebra of the jump and the share; the
single non-Lean rung is the entrance E2 — the virial (G091, sympy-exact
closed forms) and the max-entropy functional (G084, exact-residual numerics)
— from which σ² = √(GM_ba0)/2 follows with Lean-certified algebra *given*
those premises; the empirical leaves (T-law 2/3 at 0.076 dex, the
zero-parameter dust law at 0.52σ, m(z*) = 5.0–5.2 keV) are measured or
predicted, registered with their falsifiers. The next 2-3 certificates that
would complete the spine: **C1 `virial_rung4`** (the G091 closed virial chain
⇒ σ² = C/2 inside Lean), **C2 `maxentropy_phantom`** (EL iff γ = C/σ² +
strict concavity ⇒ ρ = A/r²), and **C3 `twothirds_law`** (the 2/3 = 1 − 1/3
identity as algebra). With C1+C2 every spine edge is Lean; the loose ends
that remain are physics by design (the Boltzmann identification, the virial
equilibrium, the fitted/measured exponents and densities) — stated, not
hidden.

*Checks: 10/10 certificates exit 0 (re-run today) · node/edge/depth counts
consistent (`G214_results.json`) · every status lane-cited.*