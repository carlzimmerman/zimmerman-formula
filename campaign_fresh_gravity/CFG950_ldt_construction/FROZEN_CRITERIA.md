# CFG950 FROZEN CRITERIA: the labelled-domain theory (LDT), written down and tested

Committed alone, before any CFG950 script, derivation output or number. Block CFG950–959 (LEDGER reservation row; this
lane is CFG950, the formal construction). κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s²,
scored separately, never pooled. Cold energy (its mass is required; no particle species is added). Framework-native inputs
only; no ΛCDM yardstick enters a verdict. Not "theory closed" whatever the outcome; nothing here can say the data favour
the framework. Any change after this commit is a dated, labelled amendment.

## 0. What LDT is, and the choice of primary formulation

LDT is the one construction left standing by CFG941 (D-T), CFG944 (G), CFG945 (S; H1 resolves the hover with labels),
CFG946 (T-O2 / L-G) and CFG947 (no exact non-local parent; an approximate labelled parent untested). Two formulations are
on the table:

- **(A) per-label tether** (CFG945 H1): the labelled cold medium *is* the phantom; each label q has its own medium potential
  χ_q and tether W(|Dχ_q|).
- **(B) per-domain non-local source** (CFG947 N1 + merge rule + dipole-free draw): untethered geodesic dust plus a
  conserved retarded source 𝒮_q per domain.

**Declared primary: (A).** Reasons, stated before computing:
1. Between label events (A) is a local, diffeomorphism-invariant action (CFG938's per label), so energy-momentum
   conservation between events is a theorem; (B) has no action at all (retarded kernels).
2. In (A) positivity, the edge and zero-sum follow from the conserved medium mass; (B) needs a cap, a deficit clip and the
   kernel's own supply root imposed.
3. In (A) the phantom is real mass, so the gravitational field cannot jump at a label event; (B)'s own-label phantom is
   non-additive (T-L), so a merge recomputation jumps.
4. In (A) relocation is real motion under internal forces, so CFG947's T-M condition holds automatically; (B) must impose
   a dipole-free draw.

(B) is kept as the comparison. Structural statement **T-EQ** (§4) tests the claim that the two coincide on settled static
domains (same gravitating density when B's edge is the kernel's own supply root), and the derivation states where they
differ dynamically.

## 1. The specification to be written down (DERIVATION.md), primary formulation (A)

**Fields.** Metric g; baryons S_b (geodesic); cold medium = per-label populations q = 1, 2, … each with comoving labels
φ_q^I, n_q, current J_q = n_q u_q, plus an unlabelled population q = 0 (untethered dust, collisionless). Per label q ≥ 1:
auxiliary χ_q, multiplier λ_q.

**Action between label events** (label membership fixed):

  S = ∫√−g [ c⁴R/16πG − Σ_{q≥0} m c² n_q − Σ_{q≥1} ( W_full(u_q) + (3γ/4K²) τ_q:τ_q ) + Σ_{q≥1} λ_q (D_(q)² χ_q − K m n_q) ] + S_b,

with u_q² = h_(q)^{μν}∂_μχ_q∂_νχ_q in label q's own frame, W_full(u) = [−a₀u − a₀² ln(1 − u/a₀)]/K, γ = KL*²/2, τ_q the
traceless medium-frame tidal tensor of χ_q (CFG938's definitions, one copy per label). No θ appears in the action.

**Label sector (no action; declared plainly).** Rules (i)–(v), each causal (NR limit: instantaneous fields; covariantly
retarded):

- **(i) Assignment at collapse.** LATCH: an unlabelled element latches when its own expansion θ = ∇_μu^μ first becomes
  ≤ 0 (the record's turnaround switch, CFG649/941, used as a non-variational latch, not as an action gate). IDENTITY:
  it takes the label of the labelled medium within the contact length L* (24 pc primary; 1 kpc bracket) whose ball domain
  (rule iv) contains it, choosing the dominant (largest-mass) one if several; if no labelled medium lies within L*, it
  seeds a new label. The θ-latch is compared with class A's catchment balls (E3: mean enclosed (1 + δ) ≥ Δ_ta) in the
  T-θ toy (§4).
- **(ii) Merge rule M-R.** Ball domain of label p: r_dom,p = the outermost radius r about p's mass centroid X_p at which
  p's shell-averaged traceless tidal strength ⟨|τ_p|⟩(r) ≥ ⟨|τ_ext|⟩(r), where τ_ext is the tidal tensor of all other
  labels' χ fields. Label p merges into the dominant external label q (M_q ≥ M_p; ties to the older label) when
  r_dom,p = 0. The remaining core is transferred with fractional weights linear in time over τ_m (one dynamical time at
  q's half-mass radius); the instantaneous limit is used in the toy. Mass moves only by dynamics, never by the rule.
- **(iii) Source / draw.** The phantom is the labelled medium's own rest mass. Its relocation is the medium's motion
  under the per-label action plus a declared dissipative extension: internal (Galilean-invariant) viscosity, as CFG938
  S3d. The toy uses the overdamped gradient flow of the same energy (spherical). Mass is conserved by continuity per label
  between events, and by events, which move no mass. Momentum is conserved by translation invariance and internal
  dissipation, so the relocation is dipole-preserving by construction.
- **(iv) Satellites / tidal re-latch L2.** A satellite keeps its label. An element of label p lying outside p's ball
  domain re-latches to the largest-mass label whose ball domain contains it. One-way rule: re-latching goes only to a label
  of larger mass at the event time. In the far-host limit ⟨|τ_ext|⟩(r) → |τ_h(R)|, which is CFG945's L2 radius; that
  computation is used, capped to [a, 100a] as CFG945.
- **(v) Unlabelled / foreign debris.** Medium inside a settled galaxy's edge that carries neither the galaxy's label nor
  a satellite's own-domain label. Allowed fraction q_max = 3.5e-7 of the galaxy's medium (CFG945: the law at 1e-6 with
  debris deviation ≈ 2.6q / 2.9q). The derivation states what the rules leave as debris.

**R-E (declared bookkeeping option for energy; not part of the dynamics).** At every label event each transferred element
carries a comoving label-energy scalar e_L, with Δe_L = −(its share of the event's ΔE_W). It gravitates as ρ e_L/c² and has
no NR dynamics.

## 2. Tests and pass lines (both footings unless a toy is in code units, which are footing-free by scaling)

### (a) Law in a single-label galaxy
- **a1.** Static single-label equilibrium (CFG938's reduced EL, W_full) at NGC 3198's 43 radii (record rotmod file,
  Υ = 0.61, spherical-equivalent m_N = r² g_bar/G): max |g/g_law − 1| ≤ 1e-6.
- **a2.** Deep BTFR: the sympy limit of V⁴/(G M_b a₀) as y → 0 is 1, and the numeric value at y = 1e-14 is within 1e-6
  of the exact law's own value there.
- **a3.** Every one of the 43 radii and the deep points y ∈ {1e-2, 1e-3} lie inside the label's edge r_e, where
  M_ph,simple(< r_e) = M_c,q. The label mass is the census catchment cold mass M_c,q = (1 − f_b) M_ta (CFG947 domain():
  engine constants, native Δ_ta(0) from CFG654's JSON, f_ret census). Graded on the census mass; the θ-latch mass
  (f_θ M_c,q, from T-θ) is reported.
- **PASS** iff a1, a2 and a3 hold. Costs reported, not graded: two co-spatial labels (CFG945: 4.12 / 4.61) and the debris
  line q_max.

### (b) FRW and linear growth
- **b1.** The unlabelled medium is dust: T^μν with w = 0 and isotropic stress (sympy, as CFG941 K2).
- **b2.** Labels are unset in the linear regime:
  - at linear order θ = 3H(1 − f δ/3), so no latch for δ < 3/f (sympy);
  - top-hat: the first θ = 0 is at turnaround (cycloid η = π), with δ_lin = 1.0624 and 1 + δ = 9π²/16 (sympy / numeric).
- **b3.** Growth with no tether in the linear regime: |n − 1| ≤ 1e-6 (CFG941's Lagrangian growth determinant at c₂ = 0;
  EdS, Ω_c/Ω_b = 5.364, free baryons).
- **PASS** iff b1–b3.

### (c) No hover
- **Setup.** CFG882's dwarfs H1–H3 at 50 / 100 / 250 kpc in a 6e10 M⊙ point-mass law host (CFG941/945).
- **Measure.** Δa/g_host between the satellite's own-label medium and its stars, centre-of-mass over the L2 domain, in the
  host's point-mass law field (CFG945's H1 computation).
- **PASS** iff max Δa/g_host ≤ ε_B on each footing (ε_B recomputed from the CFG874 replica; CFG945: 0.344 / 0.317).
- **Reported, not graded:** the comparison with CFG941's 0.01 line; a 1-Gyr two-body integration of stars and own-label
  medium (CFG945's restoring_and_dyn, with Δa = the tidal residual) showing whether they stay bound.

### (d) Slip
- **Measures** (CFG938 S4): s_grad = 4πG r|p_r|/(c² g) and s_847 = 8πG r² max(|p_r|, |p_t|)/(c² v_c²).
- **Where.** Per label on CFG847's five systems (stiffness L* ∈ {0, 24 pc, 1 kpc}), plus a satellite inside a host: the
  summed label stresses at the satellite's scale radius, H1–H3 × 3 radii.
- **PASS** iff the worst value is ≤ 1.9e-5.

### (e) Energy and momentum through label assignment, a merger and a tidal re-latch
- **e1. Momentum.** A 1-D slab toy: baryons, two labels, unlabelled dust; leapfrog; exact pair gravity; per-label tether
  from the discrete gap energy Σ W(|χ_q′|) Δx, whose forces telescope. Events:
  - latching of converging dust (rule i, by contact);
  - merging label 2 into label 1 (rule ii);
  - re-latching label 2's outer slabs (rule iv, prescribed in 1-D, which has no tides).

  Line: |P(t) − P(0)| ≤ 1e-12 Σ m|v| at every recorded time, across all events. A structural proof is also required:
  events move no mass and change no velocity, and each epoch's action is translation-invariant.
- **e2. Energy jumps (spherical, NR).** First-order chemical potential δE_W/δm = Kλ_q(x) = ∫_x^∞ D_full(u_q) dr (sympy
  identity plus numeric check). Exact finite jumps for:
  - assembling NGC 3198's label, a range between joining at r_ON and joining inside-out at the final radii;
  - concentric merger of two NGC-3198-like labels, baryon ratios 1:1 and 1:3, each with its census label mass;
  - re-latching a shell at r_dom for H1–H3 (per unit mass, against the shell's specific orbital energy g_host R).

  Each jump is compared with the event system's Newtonian |E_grav|. Books close iff |ΔE|/|E_grav| ≤ 1e-6.
- **e3.** R-E's cost, reported: max |e_L|/c², and the post-Newtonian local (Bianchi) residual ~ ΔE/(M c²) at events.
- **Grades.**

  | grade | condition |
  |---|---|
  | PASS | e1 holds and every e2 jump closes with the specification's dynamical fields only |
  | CONDITIONAL | e1 holds; energy closes only through R-E (a non-dynamical label energy, a stated cost); the violation without R-E is quantified |
  | FAIL | e1 fails, or energy cannot be closed even through R-E |

### (f) Mergers (continuity and final law)
- **Toy.** Code units G = a₀ = 1. Concentric Hernquist baryons (b = 2) with M_b1 = 1 and M_b2 ∈ {1, 1/3}. Each label's
  medium starts as its own isolated settled law phantom, with label mass 6 M_b,q (edge at its supply root). Superposed at
  t = 0 (sudden coalescence). Lagrangian medium shells per label (N₀ = 300 per unit label mass ratio, and 2N₀), with
  energy-exact shell forces.
- **f1. Continuity.** J_LDT = max over shells and probe radii of |g(t_m⁺) − g(t_m⁻)|/g(t_m⁻) across the label merge must
  be ≤ 1e-12, where g = G(M_b + Σ_q M_q)(< r)/r² is the field stars and light feel. The class-A-type comparator J_A (an
  own-label phantom recomputed at the merge, CFG947 T-L form) is reported; MUTATE M5 shows it is > 0.01.
- **f2. Evolution.** Overdamped gradient flow after the merge: every accepted step has ΔE ≤ 1e-12|E| (monotone), and the
  distance to the discrete merged equilibrium falls by at least ×10 over the run.
- **f3. Final law.** The discrete merged single-label equilibrium (per-shell force balance solved directly), evaluated at
  shell mass midpoints inside 0.9 r_e,merged: max |g_mid/g_law − 1| ≤ 1e-3 at 2N₀, and ≤ 0.6 × the N₀ value (convergence),
  for both mass ratios.
- **Energy reported:** ΔE_W at the merge and the heat dissipated.
- **PASS** iff f1, f2 and f3.

### (g) Well-posedness inside a label and at label boundaries
- **g1. Per label.** CFG938's linear dispersion ω² = γρ₀k² + Kρ₀[R′cos²θ + (R/u)sin²θ] ≥ 0 for u₀/a₀ ∈ {0.0909, 0.5,
  0.9, 0.99}, kL* ∈ [1e-2, 1e5], all angles. Inertia margin ρ_c c²/(D u/K) > 1 on CFG847's systems.
- **g2. No ghost.** No θ in the action, so the longitudinal kinetic coefficient is ρ₀ (sympy second variation: F_θθ = 0).
  Theorem G's hypothesis (a local L(θ, u)) is not met because the latch is outside the action.
- **g3. Label boundaries.** Co-located labels interpenetrate (each label's stress acts on its own medium only). The
  two-label WKB problem must give max Im ω ≤ the k-independent Jeans bound √(K(ρ₁ + ρ₂)) over CFG945's grid. The label
  field enters the equations only through n_q (no derivative of the label), so a label front adds no characteristic.
- **g4. Events.** Under the one-way rule each element changes label finitely often (a monotonicity argument), so there
  is no Zeno chattering. The latch time depends continuously on the data when θ crosses zero transversally; top-hat
  θ̇ ≠ 0 at η = π is checked.
- **Grade.** CONDITIONAL if g1–g4 all pass (CFG938's γ > 0, the inertia inequality and per-label single-stream flow are
  inherited premises; nonlinear well-posedness is unproved). FAIL if any check fails.

### (h) Forced edge and zero-sum, edge radius per galaxy
- **h1.** The edge is forced: M_ph,simple(< r_ON) > M_c,q for every M_b in 1e7–1e15 M⊙ (17 log-spaced points), both
  footings. CFG947's T-E table is reproduced as K4.
- **h2.** Edge radius r_e (the label's supply root, simple kernel) per galaxy, with r_e/r_ON and r_e/r_M: NGC 3198,
  CFG847's five systems and the M_b grid. The RAR-kernel E7 edge is reported alongside.
- **h3.** No SPARC point (175 galaxies, Υ = 0.61 for M_b as CFG947) and no NGC 3198 radius lies beyond its galaxy's r_e.
- **h4.** Zero-sum is mass conservation: total medium mass is exactly conserved through every event and the flow in the
  toys (round-off).
- **PASS** iff h1, h3 and h4 hold.

### (i) The satellite data bound
- **PASS** iff (c)'s max Δa/g_host ≤ ε_B on each footing *and* the uniform-field EFE on the satellite's phantom has
  |·| ≤ δ_c (CFG874 replica; CFG945: 0.0816 dex). The tidal term at the scale radius is reported, not graded (CFG945:
  ≤ 0.052 dex).

## 3. Reported computations (no class weight)
- **R1. Other labels act as baryon-like sources.** A label's equilibrium reads R(u_q) = g_b + Σ_{p≠q} u_p (CFG945's
  two-label equation). Estimate the boost of a host's law from satellites' own-domain media, using CFG945's H1–H3 domain
  masses (M_med,dom/M_star,dom).
- **R2. Baryon-free labels.** With g_b = 0 the force on labelled medium is +R(u_q) outward, so a label without baryons
  disperses. Stated with its sympy line.
- **R3. Formulation (B) costs**, cited from CFG947 (no action; cap; own-root kernel; T-M dipole condition; T-L jump).

## 4. Structural statements to test (each counts only with a sympy or numeric check)

| id | statement | test, and what falsifies it |
|---|---|---|
| T-EQ | (A)'s settled single-label configuration and (B)'s P-S configuration with the kernel's own supply root (q = 1) have the same gravitating density | NGC 3198 and CFG847's systems, radial grid to r_ON: falsified if \|g_A/g_B − 1\| > 1e-12 anywhere |
| T-LE | Labelling bound cold medium cannot be paid kinetically. For x < r_e, Kλ_q(x) − [Φ(r_ON) − Φ(x)] = GM_c/r_ON + ∫_{r_e}^∞ R(GM_c/r²)dr − GM_b(1/r_e − 1/r_ON) ≡ Δ, independent of x; Δ > 0 means infall from rest at r_ON (or any bound orbit with apocentre ≤ r_ON) lacks the energy for an energy-conserving, momentum-conserving latch | M_b grid, both footings: falsified if Δ ≤ 0 for any M_b. The x-independence is checked numerically on NGC 3198's 43 radii (spread ≤ 1e-6 relative) |
| T-P | Momentum is conserved exactly through label events | e1 |
| T-T | Concentric two-label equilibria have u₁ = u₂ (D_full strictly increasing), so element-wise tidal comparisons tie and cannot complete a merger: M-R must be a whole-label rule | sympy: D_full′ > 0 on [0, a₀); numeric two-label equilibrium on NGC 3198 |
| T-G | No θ in the action, so no CFG944 ghost | g2 |
| T-θ | The θ-latch front lies inside the turnaround (v = 0) front for decreasing profiles. f_θ = M_θ/M_ta for EdS power-law profiles δ̄_i ∝ q^{−3ε}, ε ∈ {0.2, 1/3, 0.5, 2/3, 0.9} (pre-shell-crossing cycloids); top-hat f_θ = 1 | reported value; falsified if f_θ > 1 for any decreasing profile |

## 5. Controls and MUTATE

**K controls** (VOID rule: if any K fails, the main classes are VOID, reported but not graded).

| id | target | line |
|---|---|---|
| K1 | CFG938 NGC 3198 law, reduced EL: 2.2e-16 | ≤ 1e-6, both footings |
| K2 | CFG941 growth exponents 0.60954 / 0.69433 / 1 | first two within 1e-4; third within 1e-12 |
| K3 | CFG945 H1: 18 tidal ε values (1.6e-5 – 2.0e-3); two-label 4.12 / 4.61; debris at q = 1e-6; ε_B 0.344 / 0.317; δ_c 0.0816 | each equal to CFG945's JSON within 1e-9 relative |
| K4 | CFG947 positive results: T-F retardation bound max 1.21e-6; dust n = 1; T-M identity ≤ 6.9e-18 and R/(M_dom g_ref) = π²ε/4; T-E min ratio 1.8466 | each within 1e-9 relative of CFG947's JSON (identity ≤ 1e-16) |
| K5 | CFG938 slip: worst s_847 1.5398e-5 | within 2% |
| K6 | CFG938 dispersion minima 0.1 / 1 / 9 / 99 at u₀/a₀ = 0.0909 / 0.5 / 0.9 / 0.99; CFG945 two-label max Im ω/Jeans 0.707 | within 1e-3 relative |
| K7 | CFG941's 18 hover ratios (1.017–1.107) | within 1e-9 relative |

**MUTATE** (separate `_MUTATE` outputs; exit 1 when every tooth bites, 2 if any does not).

| tooth | change | bites if |
|---|---|---|
| M1 | labels removed: all collapsed medium shares one label (the label-free tether) | Theorem S's hover returns: satellite Δa/g_host equals CFG941's within 1e-9 and is ≥ 0.5 |
| M2 | non-dipole-preserving draw: in the 1-D toy, label 1's tether is replaced by untethered dust plus prescribed source weights (core phantom, draw on an asymmetric shell, dipole fraction ε = 0.3, growth (1 − cos πt/t_g)/2); total momentum P_m + Ḋ_s is tracked | \|ΔP_tot\| > 1e-6 Σ m\|v\| (CFG947 T-M), while the ε = 0 control conserves to ≤ 1e-10 |
| M3 | labels in the linear regime (one global always-on label) | n = 0.69433 (\|n − 1\| > 1e-3) |
| M4 | no merge rule: two labels persist after coalescence | NGC 3198 law deviation > 1e-6 (CFG945: 4.12 / 4.61), and the toy's two-label equilibrium deviates from the law by > 1e-2 |
| M5 | class-A-type instantaneous own-label source recomputation at the merge | J_A > 0.01 in the toy |
| M6 | tether removed (dust only) | the labelling energy jump vanishes exactly (\|ΔE\| ≤ 1e-14 \|E_grav\|), showing e2's jumps come from the tether |

## 6. Classes

| class | condition |
|---|---|
| LDT CONSISTENT | (a)–(i) all PASS; costs listed |
| LDT CONDITIONAL | no test FAILs and at least one is CONDITIONAL; each condition and cost named |
| LDT INCONSISTENT | at least one FAIL, *and* a §4 statement that passes its check shows the failing property is generic to LDT (any per-label tether with label events), not only to the rules chosen here |
| NOT CONSISTENT AS SPECIFIED | at least one FAIL with no such generic statement |

The non-local, action-less label sector is a declared cost in every class, never scored as a pass. The CFG678 scorecard
(20 gates: PASS / FAIL / CONDITIONAL / UNTESTED / DECLARED / PENDING / NOT DECIDED, each with its source) follows
CFG678's rules: a prescribed mask scores UNTESTED, never PASS.

## 7. Design-stage disclosures (not blind)

**Read before freezing:**
- CFG938, 941, 944, 945, 946 and 947: README, DERIVATION, and code where needed for K;
- CFG678: criteria and scorecard;
- THEORY_CANONICAL_2026-10-18's last notes;
- the class-A engine (CFG654's engine: forces(), cover_peaks(), cover_balls(), x_supply()), read with the Read tool;
- CFG945 / 947 / 941 result JSON keys, for K.

**Hand expectations, formed while designing; no script run.** The class follows only the rules above.
1. (a), (b), (c), (d), (h), (i) PASS (per-label reduction to P0; CFG945 H1).
2. (e): momentum closes exactly. Energy jumps by +Kλ_q per unit labelled mass, of order the medium's cancelled
   self-binding, plausibly O(1) of |E_grav|. T-LE is expected true, so energy closes only through R-E: CONDITIONAL.
3. (f): J_LDT = 0 against a class-A-type jump of 20–41%; the toy relaxes to the merged law.
4. (g) CONDITIONAL.
5. f_θ < 1.
6. T-T true: element-wise tidal rules cannot finish a concentric merger.
7. R1: satellites' media count in a host's law (a ~10% effect for a MW-like host is my guess).
8. Overall: LDT CONDITIONAL.

## 8. Compute
- One process at a time; OMP_NUM_THREADS=1; nice -n 10; in-script RSS guard at 1 GB; swap-growth guard (exit 75).
- Small sympy and numpy only. No downloads. No other lane's files touched.
- Read-only inputs: CFG4_common; the record's SPARC files; CFG654's Δ_ta JSON; CFG874's LVD CSVs and JSON; CFG941 / 945
  / 947 result JSONs.
- Stages K, MUTATE, main, in that order, with separate outputs.
