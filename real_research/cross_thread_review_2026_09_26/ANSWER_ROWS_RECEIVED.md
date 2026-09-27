# ANSWER-ROWs received from the owning sessions

These are the raw rows the owning sessions sent back under the assembly protocol, copied verbatim apart from line
wrapping. ANSWER_AS_IT_STANDS.md is built from them.

Format: `lane | commit | MODEL TAG | gate(s) | verdict + numbers | scope | controls`. Model M*: the MOND-sector switch
(CV3's constrained form), MS5's κ-form cap, p = 1, x_c0 = 2.5, w ≤ 0.25, ν_mono, σ = 1, and L388's carrier.

## Dark-energy thread

**DE9 | 8c3bfe8f3 (+aa5705194, numbers unchanged)**
- **Model tag:** two switch readings, reported separately:
  - the MOND sector, ρ_b + ρ_ph − f_b ρ̄ (on-branch and static; not CV3's varied form);
  - curvature.
- Cap none. p ∈ {0.5, 1, 1.5, 1.9}; x_c0 scanned; w ∈ {0.1, 0.25, 0.5, 0.75}, plus a near-hard 0.02. ν_mono.
  σ = 1, 1/m = 0.1 Mpc (DE8's operator). No carrier (switch-only). Both footings.
- **Gates:** the KiDS cap and the flagship cap (z = 2.5, 1e11), recomputed with the smooth gate. The forest by a
  dominance bracket. Shear not used.
- **Verdict:**
  - At p = 1 the MOND-sector reading allows w ≤ 0.5: x_c0 ∈ [2.0, 3.35] at w = 0.25 (M*'s 2.5 is inside) and
    [3.0, 3.09] at w = 0.5. The curvature reading allows w ≤ 0.25.
  - The KiDS cap falls from 4.48 to 3.76 as w goes 0.1 → 0.75 on the MOND-sector reading.
  - There is no window at w = 1.
- **Scope:** isolated spherical lenses, and no carrier lensing (that was added in DE10).
- **Controls:** C1/C2 reproduce DE2's hard caps to 0.1% and 0.7%. MUTATE (a hard gate at the midpoint) fails W1,
  rc = 1.

**DE10 | dabce1b73**
- **Model tag:**
  - The switch is the MOND-sector reading, carrier-blind: an on-branch static profile, prescribed rather than varied.
  - The cap is MS3's local |g|²/∇²Φ form, which MS5 withdrew. It does not bind on any KiDS lens (scaling 1.0000), and
    the κ form doesn't bind either for v_f ≤ 247 < 325 km/s, **so the result carries to M* unchanged.**
  - p = 1, x_c0 = 2.5, w ∈ {0.02, 0.25}. ν_mono. σ = 1, 1/m = 0.1 Mpc.
  - The carrier is L375's shell model at L390's settings, kicked at 600 and 650 km/s, amplitude 1. Both footings.
- **Gate:** KiDS-1000 (L352's fit, with a free 2-halo term).
- **Verdict: PASS.**
  - At 600 km/s: −37.0/−34.0 (hard) and −32.3/−29.3 (w = 0.25).
  - At 650 km/s: −36.8/−33.7 and −32.1/−29.0.
  - That beats the curvature branch with the same carrier (L390: −13.1/−7.2).
- **Scope:**
  - Isolated lenses; L375's fiducial accretion history.
  - The carrier masses come from L390's curvature-branch refit, not a refit on M*.
  - The 2-halo amplitude is free, and XR9 reports it.
- **Controls:** C1 reproduces L390 exactly. MUTATE (v_k = 0) fails at +133/+137, rc = 1.

**DE11 | aa6588d56**
- **Model tag:**
  - The switch is the MOND-sector reading x = 1.5 Ω_m(a)[f_b δ + δ_ph], with the phantom lagged one step. No cap
    (it doesn't bind in the IGM).
  - p = 1, x_c0 = 2.5, w ∈ {0.25, 0.02}. ν_mono.
  - The operator is L347's single-fluid particle-mesh QUMOND. Its kernel reads ALL matter, so it OVER-states M*'s
    phantom, which makes it conservative. No carrier. Both footings.
- **Gate:** the Lyman-α 1D flux power, L347's rule: deviation ≤ 0.10 for k_par = 0.2–2 h/Mpc at z = 3 and 2, in both
  boxes.
- **Verdict: PASS.** The worst deviation is 0.0041 (25 Mpc/h, alt, z = 2); it is 0.0009 at 50 Mpc/h. The active
  mesh fraction is 2–5e-4 at z = 2.
- **Scope:** convergence is being tested in DE11b, since the deviation grows ×4.6 from 50 to 25 Mpc/h. One phase per
  box. FGPA.
- **Controls:** C1 reproduces L347 exactly; C2 (never on) is ΛCDM exactly. MUTATE (L358's matter-reading cell)
  reproduces L358's 0.174 and fails, rc = 1.

## Advancement thread

**AT4 | b844a87b3**
- **Model tag:**
  - The switch is the MOND-sector door on MS3's halo model, with both edge conventions (door and upper).
  - The cap is MS3's fixed radius (∞, 2, 1.75, 1.5, 1.2 and 1 Mpc at z = 0.5). That is the radius the κ form gives
    at z = 0.5, not the κ term itself.
  - p = 1, x_c0 = 2.5, plus DE5's corner. Hard switch. ν_mono.
  - The carrier is the ACCELERATION-TRIGGERED one, a labelled alternative and not M*'s.
  - The operator is L363's region phantom. Both footings.
- **Gate:** cosmic shear, R ≤ 1.2.
- **Verdict: FAILS** at every KiDS-safe cap (≥ 1.75 Mpc), for every kick Harvey allows (≤ 800 km/s). The best is
  1.26 against 1.2. The carrier keeps 61–95% of itself in 1e13–1e14.5 halos, which is where the phantom's k = 1 power
  lives.
- **Scope:** the halo model with isolated regions, at one lens epoch.
- **Controls:** C1 reproduces MS3's K1 exactly. MUTATE (L388's retention) fails H1, rc = 1.
- **Next:** AT5, a two-sided acceleration trigger that also converts in the deep-MOND outskirts. Its first look is
  1.01/1.08 at the 1.75 Mpc cap, but it is unscored on Harvey, X-COP, KiDS, S₈, the forest and high z. It is a
  labelled alternative.

**L361 | 65add0e46** (the region kernel of record)
- **Model tag:**
  - The switch is L359's vacuum-gated f, prescribed. The kernel is region-local QUMOND.
  - The carrier couples to φ only.
  - The operator: (∇² − M²)w = 4πG f ρ_b and (∇² − M²)P = ∇·[f(ν−1)∇w] + M²w, with M² = m²(1 − f).
- **Checks:** 6/6.
  - R0: the action's Euler–Lagrange equations have zero residual.
  - R1: transmission through the gap is 9.5e-5.
  - R2: the Sun keeps the Galaxy's field to 3.7e-12.
  - R3: KiDS +0.0/+0.0 against isolated MOND.
  - R4: 1/m ≤ 0.5 Mpc.
  - R5: the phantom's monopole is zero beyond the edge.
- **Scope:** non-relativistic, with f prescribed. σ = 1 (later found negligible for KiDS and Harvey: DE8, XR5). The
  relativistic embedding is not redone.
- **Liabilities (XR4/XR6):** LG, EFE, Coma UDGs, scored with the withdrawn cap form; the κ-form re-score is pending
  in XR9. Filament gas at z ≲ 0.5 is open.
- **Controls:** MUTATE fails R1 and R3, rc = 1.

## Merger lane (condensed from the owner's rows; every number is from committed results)

Every lane in this group has a sharp switch (w = 0) and no cap. None was scored for cosmic shear on MS3's halo model:
L373's shear column is mock-based, so not established, and L372/L392 have no shear gate. The L370 README's 10/14 is
corrected to the JSON's 11/14 in 51a8a009a.

- **L370 | 732bbe510** (scope 8850550c4, helpers 77f79072c)
  - **Model tag:** an absolute density mask at p = 1, x_c0 = 1.5, w = 0; the carrier Newtonian-only; the operator
    L370/L361 with σ = 0.
  - **El Gordo:** slightly EASIER than in ΛCDM (Δχ −0.58..−0.12), because the lensing mass is phantom-heavy and the
    infall slower.
  - **Harvey:** the intact carrier passes; core-decayed carriers fail at 1.7–4.0σ, and it is the hollow core that does
    it, not the boost.
  - **Checks:** 11/14; MUTATE (kernel off) fails A1 and A2.
- **L371 | fe4fb762d**
  - L366's slow-kick carrier FAILS Harvey at 2.1σ, 2.5σ and 5.4σ. Only each bin's maximum retention passes.
- **L372 | 5562a5dac**
  - **Model tag:** KiDS was scored switch-free and Harvey at L370's p1_x1.5 cell (joined per XR1). The carrier is two
    modes: a uniform mode U plus the gated density mode G, at 750–1050 km/s. Static retention.
  - **Verdict:** passes the alternative set (forest, S₈, X-COP, galaxies, KiDS, Harvey); the strict set fails. No
    shear gate. Its switch-dependent gates are superseded by L392.
- **L373 | 9df26672f** (edge addendum 622987d9b)
  - **Model tag:** particle-mesh, matter-only contrast switch, p = 2, x_c0 = 2 (a cell that fails the flagship), no
    cap.
  - **Verdict:** NO window. Four of five cells fall under the X-COP floor. u25_g750 fails Harvey S2 at +0.116; the
    line-of-sight cap moves β by ≤ 0.0006, so the miss is real.
  - **Checks:** 5/6. The MUTATE was not run, by its rule.
- **L392 | 1eaac841b** (σ note 3d3fe8184)
  - **Model tag:** static, p = 1, x_c0 = 2.5, w = 0, L372's two-mode carrier, branches never pooled.
  - **Curvature (signed phantom):** PASSES KiDS (−41/−34 cut at r200; −60/−55 NFW-continued) and Harvey (+0.046 to
    +0.062).
  - **Matter:** FAILS KiDS (+322/+332, +118/+128).
  - **Scope:** a prescribed-mask pass only (MS1: the curvature reading leaks). No shear gate; uncapped curvature fails
    halo-model shear (MS3 X1). The carried gates are the alt set.
  - **Checks:** 7/9; MUTATE (intact carrier) fails every cell.

## Dark-fluid lanes (condensed)

- **L374 | 4366a5625**
  - **Model tag:** the minimal ghost condensate, i.e. a dispersive γ = 2 fluid with D = √(εβ).
  - **Verdict:** FALSIFIED at shell crossing. The cold cells go c_s² < 0 at 0.81–1.05 t_sc and break down at
    0.98–1.37 t_sc; the warm one misplaces 21.5%.
  - **MUTATE:** a linear complex field (Gross–Pitaevskii–Poisson, same D and ε) passes 6/6. So the failure is in the
    FORM of the dispersion.
  - **Scope:** 1-D, the minimal action only. The completions are being tested in XR8.
- **L382 | 9b6e560f8**
  - At every forest-allowed boson mass, the particle-mesh box cannot tell a wave field from the collisionless carrier
    (variance ≤ 1.3e-4). The box runs therefore ARE the wave field's runs. The de Broglie lengths are 9–30 pc.
  - **Checks:** 5/5; MUTATE (1e-24 eV) flips it.
- **L383 | f091dc718**
  - **Verdict:** R1 FALSIFIED. The framework's clearing lowers the dwarf-heating floor on a wave field only ~2.5×,
    to 1.9–5.2e-19 eV, still 10–25× above the forest bound. Heating goes as ρ², with a coefficient 3–5× the textbook
    value.
  - **Checks:** 8/9, rc = 1; MUTATE (frozen granules) still fails R1.

## MOND-sector gate lanes, "Path forward" (condensed from the owner's rows)

The front-page synthesis is real_research/mond_sector_gate_2026/README.md (the four-step path plus "Said plainly").

- **MS1 | 2a5def6d9**
  - **Method:** all four switch readings, with the gate varied as an action term (CV1's non-relativistic Lagrangian,
    1-D, sympy).
  - **Verdict:** V_d − u_N = 0 identically on the MOND-sector and baryon-only readings. The curvature reading leaks
    −½CW′B and the matter reading −CW′B/8πG. Around an L* lens that is 0.06–6× and 0.6–60× the carrier's own gravity;
    around a z = 2.5 flagship host, 1.5–150× and 23–2300×.
  - **Checks:** 5/5, Lean 8 theorems; MUTATE fails A3.
- **MS2 | 2a5def6d9**
  - **Verdict:** the MOND-sector switch is carrier-blind (0 of 3696 states change). It is on at r_F at every CGM share,
    including none, and needs S ≤ 0.059 retained at r_F. z_max is 4.26/4.52, against the matter reading's
    1.95/2.15. The web switches on only at δ ≥ 29–34 (z ≤ 0.5) and 105–228 (z = 2–3).
  - **Checks:** 7/7; MUTATE fails D1.
- **MS3 | 2a5def6d9**
  - **U1/M1:** the mock cannot grow regions from isolated seeds and is cluster-poor.
  - **On the halo model:** s²(k = 1) = 0.80/1.07, ≥ 73% of it from ≥ 1e14 halos. Uncapped fails at 2.47–4.32. A
    1.75 Mpc cap with L388's retention PASSES (1.047/1.121). A 2.0 Mpc cap gives 1.244/1.357 and 1.5 Mpc gives
    0.986/0.987. With the carrier intact only 1.0 Mpc passes. Clearing only below 1e13 fails at 1.75 Mpc
    (1.64/1.74).
  - **Checks:** 5/5; MUTATE fails K1.
- **MS4 | e53409e64** (scope fix 969a15e7f)
  - **Verdict:** with the smooth C∞ gate and the 1.75 Mpc cap, (0.25, 2.5) gives 1.049/1.124 and (0.5, 3.0) gives
    1.025/1.096, both PASS. Uncapped fails. The width doesn't matter; the cap binds.
  - **Checks:** 4/4; MUTATE fails S1.
- **MS5 | 61a3a0858** (README label ed555bc34)
  - **The cap as an action term:** U_cap = C·min(∇²Φ_X, v_cap² κ_X²).
  - **A1:** reciprocity holds for any F(Φ_X′, Φ_X″).
  - **A2:** κ = 1/r for any spherical profile.
  - **N1 and S1:** the κ form reproduces MS3 K1 (1.047/1.121). L395's form on extended baryons FAILS (1.418/1.567).
  - **P1:** the fourth-order term changes sign in the layer, so DE7's repair is still needed.
  - (v_cap/c)² = 1.18e-6, declared.
  - **Checks:** 5/5; MUTATE fails A1 and S1.

**Next (Path forward):** the kick, built on FL1's order parameter Φ in real_research/dark_fluid_kick_2026/. A small
U(1)-breaking mass term splits Φ into two real components, with δm/m = v_k²/2c² ≈ 2e-6. |Φ|⁴ then converts
φ_Hφ_H → φ_Lφ_L into back-to-back waves at v_k. The conversion is density-triggered (rate ∝ n²), with its coupling
vacuum-gated through K. One new constant, ε.

## The author's idea, reading 4 (the clock's time slices)

**FL3 | ba60f163f** (V0 writer; within CV4's quasi-static linear khronon)
- **Verdict:** the dark fluid CAN SWIRL WITHOUT DISTURBING THE CLOCK. A rotating halo's fluid holds its angular
  momentum in quantised vortices.
  - At every core the gate's khronon source vanishes smoothly, as r²; it is exactly zero at all 37 lattice cores and
    before conversion.
  - δK/K at the lattice scale is only the conversion's shift: ≤ 1.1e-3 at c₂ = 1e-3 and 1.5e-4 at 7.3e-3, both below
    CV4's 4.8e-3. The swirl's own channel is ≤ 2e-13.
  - No vorticity reaches τ at linear order: the khronon's normal is twist-free. The second-order leak is ≤ 2e-9.
  - Criterion B holds: τ stays single-valued, with no fold.
- **Vortex spacing:** 146–188 pc at 2e-19 eV (spin 0.03–0.05), and 2–27 pc at 1e-17 to 1e-15 eV.
- **Scope:** the lattice geometry is illustrative (a product ansatz); the halo numbers are order-of-magnitude.
- **Checks:** 4/4. MUTATE (a clock made of the fluid's own dust) gives a screw dislocation at every core and fails
  S4, rc = 1. Lean FL3: 4 theorems.

**CV3 (corrected) | a7abb4d4f** (supersedes the G4 label of ab6f31b61)
- **Rule, unchanged:** multipliers enter linearly, so a gate that reads only constrained fields leaves the constraint
  determinant gate-independent. Reading B is singular at 4πGC²BW″k² = 1. Reading A+ is leak-free and slip-free.
- **OBSTRUCTED when varied:** A+'s second variation is a k⁰ negative pressure on the gas, ∝ A². A ≈ 56 (radial) to 112
  (transverse) at the z = 0.25 edge (DE12, DE13).
- **The correction:** G4's c_g = 91 km/s was reading A's A = 1 scale, mislabelled as A+'s cost.
- **Checks:** 7/7; MUTATE (the gate reads the carrier) fails G1. The V0 writer is now standing by.
