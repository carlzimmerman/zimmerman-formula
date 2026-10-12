# CFG635: one dark sector. Can one field be both the dark energy and the cold energy? Not without knobs.

**Bottom line.**
- **No single field tried here, or on the record, does both jobs without new constants.** Every construction that passes the
  behaviour gates turns out to be two components under one label (as CFG288 found for road W), and needs 3 to 5 free
  constants beyond κ. The amount Ω_c/Ω_b = 5.364 is never predicted.
- **Three structural results, all knob-free:**
  1. **A single real field cannot do both jobs.** Its smooth mode and its excitations share one mass, V''. The smooth mode
     needs that mass ≲ H₀; cold excitations need ≥ 2e-20 eV. That is a factor of 1.4e13 (K1). The two jobs need two
     directions in field space.
  2. **A field Hamiltonian has no settling hand-off.** Settling energy cannot pass from a radial (cold) mode to a
     shift-symmetric phase (smooth) mode. The exchange is an exact time derivative at fixed phase momentum, so its secular part
     is zero (K2; numerical drift 2e-6 and 1.4e-4). Energy moves only through explicit symmetry breaking at resonance. That
     route drains the cold mode's REST energy, which is a G9 violation, and has nothing to do with settling (MUTATE: growth
     ×3.7). CFG542's Q stays a coarse-grained, constitutive term with α free; no microscopic field supplies it.
  3. **The energy handed over takes the equation of state of the mode that receives it.** A canonical receiver (frozen
     potential mode) needs Q/φ̇ and stalls at rest (CFG542 K10; astra regular_receiver_lift). A ghost-condensate receiver is
     regular at w = −1, because θ̇₀ ≠ 0 there, and it does not stall: q̇(π = 0) = m θ̇₀² S′ (K4). But what it receives becomes
     a pressureless deposit (δp = 0, c_s² = δX/2X₀), not w = −1 energy. Phonons (C3) receive radiation-like energy.
- **One derived relation (framework-native, uses only the law and a₀ = κc√(Gρ_DE)):** the binding-energy density of the
  settled phantom compares with the local dark-energy density as
  **R = ρ_ph V_c²/(ρ_DE c²) = κ² g²/(4π a₀²)** in the deep regime. κ²/4π = 0.0199 at κ = ½.
  - R is 0.029 at y = 1.
  - With the exponential kernel R is 0.30–0.43 at y = 10–30 (peak 0.43 at y ≈ 24).
  - With the repaired ν_mono, R reaches 1 at y ≈ 36 and keeps growing.

  So a receiver that keeps the energy where it is deposited would have its state changed by order one inside galaxies. It
  stays observationally safe only because it is large where a₀ hardly matters. Under the ρ-bridge with full local retention
  the upper bound is |Δlog g| ≤ 0.002 dex at y = 1 and ≤ 0.003 dex at y = 30. Under the −p bridge it is zero at first order.
  This is a consistency statement, not a test.

κ = ½ is FITTED. The footings are never pooled; a₀ cancels in every ratio used here. The cold energy's mass is required. No
particle species is added to the framework. C1 and C3 would amount to one (a boson of free mass), and this README says so where
it applies. Not "theory closed".

**Files and runs.**
- `FROZEN_CRITERIA.md` was committed alone first (db79a28dc).
- Script: `cfg635.py`, sympy plus tiny ODEs. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg635.py`. It takes about 4 s,
  uses one process and well under 1 GB, and exits 0 with 15/15 checks passing. Outputs: `cfg635.out` and
  `cfg635_results.json`.
- `CFG635_MUTATE=1` writes `cfg635_MUTATE.out` and `cfg635_results_MUTATE.json`, and exits 0. Both teeth bite:
  - K2d: resonant explicit breaking gives secular transfer (+2.67 relative).
  - K4c: a canonical receiver stalls at π = 0.
- Repaired ν_mono is imported read-only from `CFG4_common`. Nothing was downloaded, and no other lane was touched.

## 1. What the record already killed (so this lane did not repeat it)

| construction | where | why it is closed |
|---|---|---|
| one complex field, V = ρ_Λ + m²\|Φ\|² (road W) | CFG288 | behaviour passes, but the amount is free. Theorem A1: the potential height must be ≥ 1.5e10 ρ_Λ, so ρ_Λ is a residual tuned to ≤ 6.6e-11 of it, and ρ_Λ never enters the dust's dynamics. "One field" is a label. Its smooth part is a constant, so it has zero receiver capacity (astra: a constant V₀ is not available energy) |
| ghost-condensate shift-charge dust (road S, the 06-19 GC dark sector) | CFG288, L374, GC thread | the single-valued gradient flow fails stream crossing and mergers. The amount is the conserved charge (free) |
| v9 DBI khronon dust as Ω_dm | condensate μ-pincer (09-02) | the pressure history c_s² ∝ (1+z)³ pins R; growth is suppressed 44–100%. Theorem: pressure cannot keep the dust out of galaxies |
| adiabatic unified (Chaplygin) fluid; fixed ρ_c/ρ_DE | CFG508 | \|α\| ≤ 1e-6; the fixed ratio is excluded (×8 by z = 1). The survivor U-0 is two components with the same two constants |
| elastic one-modulus vacuum; two-phase keyed by boundedness; viscous medium; horizon information | CFG511 | each excluded for a named reason (shear sound speed ~ c; CMB sees a smooth ω_c at z = 1100; friction kills growth; wrong w(z)) |
| interacting vacuum Q(ρ_Λ, ρ_c) with a Lorentz-invariant vacuum | CFG131 | dust with Q_ρ ≠ 0 forces ∇ρ_c = 0; a stationary halo forces Q = 0; new untied constants |
| passive local vacuum sink | astra local_sink_reaction | ∇_μT_v = −∇V forces an order-one momentum reaction on matter |
| canonical scalar partner | CFG542 K10; astra regular_receiver_lift | Q/φ̇ is singular at φ̇ = 0, and a bounded regular lift stalls at receiver rest. A canonical field cannot cross w = −1 intrinsically |
| one-way sink | astra collective_energy_lower | IC-B needs export of 0.27–0.39 and IC-C needs import of 0.50–0.64 M V_f², so both signs occur |
| Bose condensate/normal split (eV boson) | CFG383, CFG428 | free-field relaxation is starved. With the CFG428 unit correction, starvation holds only marginally (about 14 Gyr against 13.8 Gyr) |
| superfluid order parameter + kick (FL1–FL3, FK1) | dark_fluid lanes | constructions with declared m, ε, λ₀, q and misalignment; new field content |
| early running vacuum, baryon-sourced dust charge, seesaw relic | CFG507 | restatements (the amount goes into a free constant); the baryon tie is excluded by the bound on G variation |
| Λ-triggered carrier (L319/L320) | owner STOPPED | not reopened here |
| generated phantom GP0–GP5; vacuum-gated L357–L361; Blanchet–Skordis khronon | memory index | phantom/carrier constructions that fail shear, high z or KiDS; not single-field dark sectors |

What was left open, and what this lane tests:
- a field whose smooth part is dynamical with w ≈ −1 AND can actually receive settling energy regularly;
- whose clumpy part is a multi-streaming wave dust from the same field;
- with the exchange coming from the field's own dynamics.

## 2. Requirements (from the record)

- G1: homogeneous w ≈ −1 today, with ρ_DE fixing a₀.
- G2: the cold part goes as a⁻³ with c_s² ≲ 1e-6, multi-streams, and is collisionless at Bullet level. It clusters as cold
  matter in the linear era, when the switch is off.
- G3: regular settling hand-off to the smooth part:
  - no 1/φ̇ and no stall;
  - a local four-current;
  - both signs available.

  Settling is read through the baryon-reading switch (MS1).
- G4: no ghost or gradient instability on the side of the state that is used.
- G5: causal (K9).
- G6: count the knobs.
- G7: Ω_c/Ω_b = 5.364 or a ρ_c–ρ_DE relation.
- G8: a distinctive observable.

## 3. Candidates

### C1. Weakly broken U(1): the phase (pNGB) is dark energy, the radial oscillation is cold energy

Φ = r e^{iθ}. The phase rolls slowly on V_b = Λ⁴(1 − cos θ) with m_θ ~ H₀. The radial mode oscillates about f with mass m_r.
- **G1: pass.** It thaws, with w ≥ −1 always, so it cannot cross −1 intrinsically. With m_θ = H₀ and θ_i = O(1), ρ_DE fixes
  f = √(3Ω_Λ)(H₀/m_θ) M̄_Pl = 1.43 M̄_Pl (K3). a₀(z) tracks the thawing ρ_DE (A3); a₀ rises slightly into the past.
- **G2: pass.** The cold part is CFG288 road W wave dust in a different guise, for m_r ≥ 2e-20 eV. Then λ = (m_r/f)² ≥ 3.3e-95.
  The r → θθ decay rate is 4.5e-84 H₀ and σ/m ~ 6e-109 cm²/g.
- **G3: FAILS.** The exchange identity is dE_θ/dt = ṙ(∂_r V_b − r θ̇²) (K2a). For a shift-symmetric phase it is d/dt of
  H_θ(r(t), p_θ), so it averages to zero (K2b, K2d). The slow pNGB gives drift 1.4e-4 over 10 phase periods. Settling (a
  gravitational process of the radial quanta) has no term that hands binding energy to the phase. The only secular route is
  resonant breaking, and that eats rest energy (MUTATE). Forcing a hand-off needs a new shift-breaking coupling J(n_c)θ, which
  gives Q = Jθ̇: the canonical singularity and stall again.
- **G6: knobs.** Two of (f, m_θ, θ_i) after ρ_DE, plus m_r: 3 knobs. Any hand-off adds ≥ 1 more. The amount is an input.
- **G7.** Ω_c ∝ m_r^{1/2} (δr_i/f)² f². The needed amplitude is δr_i = 0.0103 f (scaled from CFG288's committed 0.0147 M̄_Pl).
  An O(1) amplitude over-produces by ×9.5e3. Fixing that with the mass needs m_r = 2.2e-28 eV, which is 1e8 below the dust
  floor and about H(z_eq). There is no relation.
- **G8.** Thawing w(z) ≥ −1, so any robust intrinsic crossing kills it. The smallest clump is the wave-dust Jeans scale.
- **Verdict: OBSTRUCTED (G3: no hand-off; shift symmetry plus adiabatic invariance) and KNOB-DEPENDENT (3 + ≥ 1).** It amounts
  to a new light boson (the radial quanta, free mass) sharing a label with a pNGB quintessence.

### C2. Ghost-condensate receiver: P(X) at P′(X₀) = 0 is the smooth part

- **G1: pass, and it is the genuinely new piece.** w = −1 exactly at X₀ while θ̇₀ = √(2X₀) ≠ 0 and π = 0 (K4a). Hamilton's
  equation gives H′(π = 0) = θ̇₀ (K4b).
- **G3, as a receiver: regular.**
  - In astra's pair bracket M = m w wᵀ with w = (H′(π), −D): M∇E = 0, Ė = 0, Ṡ ≥ 0.
  - q̇(π = 0) = m θ̇₀² S′ ≠ 0 (K4c). This escapes both the CFG542 Q/φ̇ singularity and the astra stall theorem, whose proof
    used H′(0) = 0. The MUTATE canonical receiver stalls, as it should.
  - The receiver carries momentum (∇θ), so the local four-current exists.
- **But the receiver turns what it gets into dust.** δρ = 2X₀c δX with δp = 0 at first order (K4d). The deposit is GC dust,
  diluting as a⁻³ and not propagating; it is not w = −1 energy. It stays where it is deposited, which brings in K6's R:
  order one in inner galaxies.
- **G4/G5: export only.** On the export side (the receiver gains energy) c_s² > 0, so it is stable. On the import side (the
  receiver loses energy, needed for IC-C-type states) c_s² < 0, with γ_max = |c_s²| M_k/2 (K5).
  - Stability needs M_k < 2H₀/|c_s²|.
  - Phonons are then superluminal below 2c/M_k: about 8 kpc for the cosmic excursion (3.8e-6) and about 1 Gpc for the local
    one (R = 0.43).
  - So both signs cannot be had without a G4/G5 conflict.
- **G2: FAILS within one real field.** The field's own clumpy part is road S dust (killed). A wave-dust cold part needs a second
  direction (C1's radial mode, with its knobs). The adiabatic theorem then applies again, so the hand-off needs an explicit
  shift-breaking coupling J.
- **G6: knobs.** X₀, the curvature c (ρ_DE fixes only −P(X₀)), M_k, m_r and J: ≥ 5. α stays free as on the record.
- **G7.** None.
- **G8.** A preferred frame. Under the ρ-bridge, a₀ would read the local deposit (≤ 0.006 dex in a₀ at y = 1; ≤ 0.002–0.003 dex
  in g). Under the −p bridge it is invisible at first order. That is a theoretical split between the CFG511 bridges, below
  any test.
- **Verdict: as a receiver alone, a sketch** (regular through w = −1 on the export side). **As one dark sector: OBSTRUCTED** (G2
  for one real field; G4/G5 on the import side). It is **KNOB-DEPENDENT (≥ 5)** in its complex form.

### C3. Superfluid two-fluid: the condensate is dark energy, the gapped normal component is cold energy, settling is Landau drag

- **The Landau dichotomy (K7a).** The critical velocity is min ω/k = c_ph.
  - If c_ph > V_f there is no drag: no settling channel.
  - If c_ph < V_f, drag acts on the cold component's own velocity relative to the condensate frame. That is CFG542's Pc1
    (INCONSISTENT: friction removes the support).
- **What the drag does elsewhere.**
  - If the drag is uniform, it also damps linear-era flows. D(γ)/D(0) = 0.98, 0.82 and 0.33 at Γ = 0.1, 1 and 10 H₀ (K7b);
    halos need Γ ~ 40–140 H₀ for α ~ 1.
  - If the drag scales with density, it acts in cluster mergers, where CFG623 allows only α ≈ 0.
- **Where the energy goes.** It goes into phonons: radiation-like (linear dispersion) or a⁻⁵ (quadratic), not the smooth part.
- **G6: knobs.** m_q, c_ph (or the coupling g), the condensate μ, and the drag cross-section: ≥ 3.
- **Verdict: OBSTRUCTED** (G3 via Pc1; G2 linear growth or the Bullet). It amounts to a boson with a free mass and coupling.

## 4. Scoreboard

| candidate | G1 smooth | G2 cold | G3 hand-off | G4/G5 | knobs beyond κ | 5.364 / relation | verdict |
|---|---|---|---|---|---|---|---|
| C1 pNGB + radial | pass (w ≥ −1) | pass (wave dust) | **fails** (adiabatic theorem) | pass | 3 (+ ≥ 1 for any hand-off) | no / no | OBSTRUCTED + KNOB-DEPENDENT |
| C2 GC receiver | pass (w = −1 with θ̇₀ ≠ 0) | **fails** in one real field | regular, but the deposit is dust; export only | **import side** unstable or superluminal | ≥ 5 (complex form) | no / no | receiver: sketch; sector: OBSTRUCTED |
| C3 superfluid + drag | pass | pass | **fails** (Landau: none, or Pc1 friction) | — | ≥ 3 | no / no | OBSTRUCTED |

**What this changes on the record.**
1. "One field" has to mean at least two field directions with a 1e13 mass hierarchy (K1). Every version is two components with
   one label, so CFG508's NOT DECIDABLE and CFG288's "shared label" stand.
2. The settling hand-off (CFG542 Q, CFG630's 1e-6 trickle) cannot come from field dynamics alone (K2). It is a coarse-grained
   constitutive term, and α stays free.
3. If a regular receiver through w = −1 is wanted, the ghost-condensate point is the one form that works structurally. It works
   for export only, and what it receives is a pressureless deposit, not vacuum energy.
4. R = κ²g²/(4πa₀²) ties the settled phantom's binding-energy density to the local dark energy. Any non-propagating receiver
   meets it.

## 5. Disclosures

1. **Scope.** This is analytic plus tiny ODEs; there is no cosmological perturbation code or simulation. The K7 growth equation
   is the framework's own linear cold-matter equation (the switch is off), compared only with itself at Γ = 0.
2. **R(y) assumptions.** It uses a point mass and local energy release per unit settled mass ≈ V_c². CFG630's c_W = 0.77–1 is
   the integrated version. Above y ≈ 2.5 R depends on the kernel: the exponential peaks at 0.43; ν_mono grows (its tail
   ν − 1 ≈ 0.75/y).
3. **K3 is order of magnitude.** The amplitude comes from CFG288's committed number scaled as m^{-1/4}. σ/m uses σ ~ λ²/(16π m²)
   and the decay uses the standard saxion form. Both miss their thresholds by > 80 orders, so the O(1) factors do not matter.
4. **K5.** β = 2X₀²P″/ρ_DE is set to 1 (a single-scale GC). The superluminal length scales linearly with β⁻¹. "Superluminal"
   is judged in the condensate frame; whether criterion B tolerates that in a preferred-frame theory is not decided here.
5. **K2 window.** The B windows sit at the same small-amplitude θ phase (1000 radial periods = 10 θ periods). The drift of
   1.4e-4 includes the pendulum's finite-amplitude detuning.
6. **The MUTATE run** replaces K2d (A, B -> resonant C) and K4c (GC -> canonical receiver) and re-runs the other checks, which pass identically.
