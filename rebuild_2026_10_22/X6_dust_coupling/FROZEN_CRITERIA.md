# X6_dust_coupling — FROZEN CRITERIA (2026-10-23, before any script or number of this lane)

The owner's design lane: "run one stop-ruled design lane on the dust coupling" (X0_explanation_map §2, row X6; D5, A, B).
Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt), reported separately, never pooled. No dark-matter particle species: a
field-sector dust is allowed, and any candidate that is CDM under another name is said to be so. No new fitted constant as a
cure. Never "theory closed". Never "the data favour the framework". Inputs and their classes: `ASSUMPTION_LEDGER.md`
(committed with this file, alone, before any script or number).

## 0. The question

v3's dust (Blanchet–Skordis khronon dust) obeys Dv_τ/Dt = −∇φ + ∇Ξ, i.e. it feels ψ = Φ − Ξ. U1 proved T1 (held dust never
exceeds the AQUAL phantom) and T3 (held dust is weightless in a static host, so hosted systems are dust-free: satellites
+2.0 dex STRUCTURAL, Coma UDGs +1.41 dex). Within v3's action family, and with NO new fitted constant, is there a dust
coupling that at once (a) lets hosted systems carry the dust they need, (b) supplies the cluster-core excess without
overshooting the outskirts, (c) restores linear growth (σ₈/σ₈,dust ≥ 0.95), (d) keeps isolated galaxies at the law (no
double count; the SPARC RAR intact), and (e) stays healthy (no ghost, no gradient instability, a radiation era)?

PN system (L1 FROZEN_CRITERIA §1; BS24 eqs. 19, 25, 27, 29, 30 via BSK1; PROVISIONAL transcription):
Ξ = Φ − σ̇ + |∇σ|²/2; 4πGρ_τ = −[∇·(J_Y∇Ξ) + μ_K²Ξ], J_Y = μ(x) − 1, μ = x/(1+x), x = |∇Ξ|/a₀; ∇²Φ = 4πG(ρ_b + ρ_τ);
v_τ = −∇σ, ∂_tρ_τ + ∇·(ρ_τv_τ) = 0; khronon dust Dv/Dt = −∇Φ + α∇Ξ with **α = 1 in v3**; baryons Dv/Dt = −∇Φ.
Linear kernel of the khronon's own gravity (M1, from this system with J_Y(0) = f₀ − 1): s(k; f₀, α) = 1 − αk²/((1−f₀)k² + μ²)
(comoving: μ → aμ_K); v3 is f₀ = 0, α = 1: s = μ²/(k² + μ²).

## 1. The candidate list (finite, frozen; each with its action term)

Notation. S_v3 = (c³/16πG)∫√−g [R − 2J(Y) + 2K(Q)] + S_P + S_m[g], with Y = A·A/c⁴, A_μ = c²n^ν∇_νn_μ, n_μ the unit normal
of the τ-foliation, K = μ_K²(Q − 1)² (BS24 Eq. 7), J = J_x = Λ − 2a₀²[y − ln(1+y)], y = √Y/a₀ (C4 K2), S_P = the covector P
with −(γ_L/2)(D·P)² (C4/C5), matter minimally coupled to g.

| id | coupling | action term | status |
|---|---|---|---|
| **C0** | v3 as is: khronon dust feels ψ = Φ − Ξ (α = 1, f₀ = 0) | S_v3 | **graded (control)**: must reproduce U1's T3/B0, F3's 0.391, S4's CANNOT |
| **C1a** | the khronon's own charge feeling −∇Φ (α = 0) | **none.** For n_μ = −N∂_μτ the 4-acceleration is a_μ = D_μ ln N (kinematic identity, X-D1), and in unitary gauge N = 1 + Ξ/c²; so the charge's force relative to free fall is ∇Ξ by kinematics, not by a coupling constant. α = 0 ⟺ ∇Ξ ≡ 0 ⟺ Y ≡ 0 ⟺ J enters only through J(0) = Λ: no law. U1's MUTATE hybrid (charge on −∇Φ, Ξ still from the hold) has Ξ in no force, so it reduces to Newton + geodesic dust with no selection of the law (CFG946 T-O2 step 3). | **listed and EXCLUDED** (no action) |
| **C1b** | v3 plus a separate geodesic field dust (minimally coupled to g) | S_v3 + S_d, S_d = −∫√−g λ_d [g^{μν}∂_μφ_d∂_νφ_d + 1] (mimetic constraint field, c = 1; λ_d a Lagrange multiplier whose value is the dust density; X-D2: its congruence is geodesic, and the khronon at Q ≡ 1 is the same constraint, Q = 1 + Ξ at PN order) | **graded over its whole free range** f_d ∈ [0, 1] (see below) |
| **C2** | khronon dust with J′(0) = 0 (f₀ = 1; M1's R1) in the limit x_t → 0⁺ (no new constant in the limit; J = J_x for x > 0) | S_v3 with J → J_R1 | **graded** |
| **C3α** | the khronon charge feeling Φ − αΞ, α ∉ {0, 1} | none: α ≡ 1 by X-D1; and the deep law forces α = 1 (X-D3; CFG941 D-T, CFG946 O2c) | **EXCLUDED**; collapses to C0 |
| **C3f** | interior f₀ ∈ (0, 1), i.e. J′(0) = f₀ − 1 | S_v3 with a J whose J′(0) is a free number | **EXCLUDED** (needs a number). Reported only: bracketed by C0 and C2, since ∂s/∂f₀ < 0 (M1; X-D4) |
| **C3β** | baryons on the khronon-frame disformal metric g̃_μν = g_μν − (Q^{−2β} − 1)n_μn_ν (PN: baryons feel Φ − βΞ) | S_v3 with S_m[g̃] | **EXCLUDED** (needs a number; β = 0 ≡ C0). X-D7 records why no β is structural: in a held host the baryon–dust relative acceleration is (1 − β)g_host (T3 survives for β < 1) and baryons feel no host force at β = 1 |
| **C4** | AeST's cold sector: the shift-charge dust of SZ21's scalar with the unit-timelike vector (C1's capped 𝒥 ⇒ μ = x/(1+x); + the γ_L term = v4) | SZ21 (arXiv:2007.00082) action, on disk outside the repo (`_external_data/aest_papers_2026_10_22/`), as used by H1/H2/C5 | **graded from the record only** (H1, H2, C5; no new computation) |
| C5 (not couplings) | K-shape changes: BS25 DBI (λ_D), two-scale K, comoving μ_K = μ_cap/a, H1's floor λ₀ | each adds a fitted or postulated number | **EXCLUDED as candidates.** One exception, declared now: BS25's DBI K at BS24 Fig. 1's *published* sets (P1: μ⁻¹ = 223 kpc, λ_D = 30; P2: μ⁻¹ = 22.3 Mpc, λ_D = 1; Q7) is LITERATURE-INPUT, not fitted here, so every khronon candidate (C0, C1b, C2) is graded with K ∈ {quadratic (v3), DBI-P1, DBI-P2} as sub-rows |

The multi-stream (MS) particle reading of the dust is a reading of the same force law, not a coupling (U1: T1 and T3 hold for
MS); it is not a candidate.

**C1b's free number.** f_d = Ω_d/(Ω_d + Ω_K) is the share of the record's FITTED cold abundance carried by the separate dust (an
initial condition). Its structural endpoints are fixed: **f_d = 0 ≡ C0**; **f_d = 1** ⇒ the khronon has no charge, ρ_τ ≡ 0 is
preserved by the continuity equation, the hold then gives Ξ ≡ 0 (Yukawa-sign operator, unique decaying solution), so there is
no law: **GR + mimetic dust, i.e. CDM under another name** (X-D2, X-D6). Any interior f_d is a second fitted abundance, so C1b
can never be "A CANDIDATE PASSES ALL FIVE". It is graded over the whole range [0, 1] (bounds by monotonicity or root finding;
no value is chosen or fitted) to show where it fails. For every f_d that passes (c), C1b's cold sector is mostly a cold,
geodesic, pressureless dust: CDM under another name; the README says so.

## 2. Parameter points

- μ_K ∈ (0, 10 Mpc⁻¹ physical] (BS24 Eq. 39 cap; 14.8 h/Mpc at F3's h): an existing constant of v3 (external premise; absent
  from v3's parameter table), not fitted here. Each test is reported at μ_K ∈ {BS24's own 0.015637, S4's galaxy-guard edge 0.03,
  the cap 10} Mpc⁻¹ where it depends on μ_K. A candidate passes only if **one** μ_K (and, for C1b, one f_d) passes all five.
- A test is PASS iff it passes on both footings, FAIL iff it fails on both, otherwise COND (counted as UNDECIDED in the
  verdict, the split named). Footing-independent tests are evaluated once.

## 3. Tests and pass lines (taken from the source lanes)

**(a) Hosted systems carry the dust they need.**
- (a1) Dwarf satellites. U1's per-system table `U1_v3_dust_content/u1_satellites_per_system.csv` (45 canonical / 46 alt;
  Delta_* = log₁₀(g_obs/g_bar) − log G_branch, E-W, at r₁₂). Statistic: median over systems, bootstrap sd (4000 resamples).
  - C0, C2: native branch B0 (falling systems are dust-free, T3; T3 uses only Ξ_host = Φ_host + C and momentum, so it is
    J-independent, X-D5); branch range = {B0, B1-MS, B1-LIT} (the static column is not available to a falling system).
  - C1b: the khronon part is dust-free (T3 holds for it, X-D5); the separate dust has weight (falls with the satellite, X-D5) and
    its content M_d(<r₁₂) is history. Native line (zero history): dust traces the baryons at the cosmic ratio,
    Δ(f_d) = Delta_B0 − log₁₀(1 + 5.364 f_d). Branch range: any M_d ≥ 0. Reported: the needed median M_d/M_b(<r₁₂) =
    10^Delta_B0 − 1, and that in units of 5.364.
  - Classes (U1 §3): NATIVE (native line within 2 sd) → PASS; STRUCTURAL (data ≥ 3 sd outside the whole branch range on both
    footings) → FAIL; HISTORY-DEPENDENT or TENSION → UNDECIDED.
- (a2) Coma UDGs. U1's N5 Coma B0 (⟨E⟩ in ln, se, σ_sys; z_sys = ⟨E⟩/√(se² + σ_sys²)). C1b native: ⟨E⟩ − ln(1 + 5.364 f_d)
  with the same se and σ_sys. Classes as (a1) with |z_sys| ≤ 2 → NATIVE, the whole range ≥ 3 → STRUCTURAL.
- (a) = the worse of (a1), (a2) (FAIL > UNDECIDED > PASS). C4: UNDECIDED unless the record holds a T3 analogue for AeST.

**(b) Cluster cores, no outskirt overshoot** (F1 PRIMARY 326-cluster stack; F1/S4 lines). PASS iff A_MID and A_OUTER are both
within 2σ of 1 in all four cells (h 0.672 / 0.686 × footings) and S4's profile χ² ≤ 11.07.
- C0, C2 (and their DBI sub-rows): S4's AMENDMENT-A1 verdict, read (`s4_v3_muk_clusters_results.json`: verdict_A1,
  knob_passes, single_cells_passing). CANNOT ⇒ FAIL. S4's statics are J-independent above x_t, and K enters only through
  K″(1)/2 = μ_K², the same for DBI (X-D10).
- C1b: F1's two record dust shapes sourcing the AQUAL field (`f1_cluster_cores_results.json`: `dust` rows, dust tracing the gas;
  `addendum_L187` "cold c*=0.40 … sourced" rows, NFW c* = 0.40, ΛCDM-PROCESSED), at the fair-sample amplitude: gas-tracing
  dust/gas = 5.364 × 1.20 × f_d = 6.4368 f_d (F1's f* = 0.20), NFW u = f_d. The predicted lensing rises with amplitude, so A
  falls (monotone). FAIL at f_d if, for the gas-tracing shape, 6.4368 f_d ≥ F1's f_needed (A_MID = 1) and F1's A_OUTER there is
  below 1 − 2σ; and, for the NFW shape, f_d ≥ 0.443 and F1's A_OUTER(u = 0.443) is below 1 − 2σ. Evaluated on f_d ∈ [f_c, 1]
  (below f_c, (c) fails). (b) = FAIL if both shapes FAIL on that whole range on both footings, else UNDECIDED. The khronon
  part's static μ_K term is S4's (unchanged in shape; stated, not recomputed).
- C4: H2's AMENDMENT-A1 verdict, read. CANNOT ⇒ FAIL.

**(c) Linear growth**, R = σ₈/σ₈,dust ≥ 0.95. Machinery: this lane's copy of F3/M1's sub-horizon ODE (baryons feel all mass;
khronon own-gravity kernel s(k, a; f₀, α); the separate dust feels all mass) on F3's background A (C2 c2b refit; CLASS P(k) at
z = 0 weights σ₈), a_i = 1e-3 (F3's optimistic start; a_i = 1e-4 reported).
- PASS iff R ≥ 0.95 at a_i = 1e-3 and no record Boltzmann number for the same model is below 0.95; FAIL iff R < 0.95 at
  a_i = 1e-3 at every allowed μ_K (R rises with μ_K, so the cap is the best point). Record Boltzmann numbers quoted: Q6 (0.073
  at the cap), Q7 (DBI 0.259–0.324).
- C1b: three fluids (Ω_b; f_d Ω_c geodesic; (1 − f_d) Ω_c khronon). f_c = the root of R(f_d) = 0.95 (derived bound, root
  finding; not a fit) at the cap and at 0.03 Mpc⁻¹. (c) PASS for f_d ≥ f_c (ODE only: no Boltzmann run here, so the true
  threshold is ≥ f_c).
- C4: H1's growth column (ii) (every family member PASS) ⇒ PASS (record).

**(d) Isolated galaxies stay at the law.**
- (d1) No double count (CFG946 (a), exact line). NGC 3198 (CFG946's file, Υ = 0.61, 43 radii): max |g/g_law − 1| < 1e-6 at all
  radii, and V⁴/(G M_b a₀) at the fair-catchment r_ta within 1e-6 of the law's own value, both footings. C0, C2: held dust is the
  phantom (U1 D2 literal statics, T1) ⇒ PASS (cited theorem). C1b: separate dust = CFG946's D-F content (f_d × 5.364 M_b,
  M(<r) ∝ r out to r_ta) sourcing the AQUAL field universally (X-D6).
- (d2) SPARC RAR (P4 T1 line, adapted to measure the change). 175 galaxies, P4's recipe (spherical approximation, algebraic ν₁ =
  exact spherical AQUAL, one Υ per galaxy on [0.30, 1.20] step 0.01 by the CFG4-weighted mean square). Line: rms ≤ 0.110 dex and
  median Υ ∈ [min(0.50, Υ_law), 0.80], with Υ_law the law's own median Υ on that footing (the law misses P4's 0.50 edge on alt,
  P4 COND; the adapted edge makes (d2) a test of what the candidate changes). C1b: D-F dust per galaxy, M_b(Υ) =
  V_bar²(R_last)·R_last/G, r_ta(M_b) by CFG946's formula. Reported: f_d,max(d2), the largest f_d passing on both footings
  (bisection; a derived bound).
- (d3) Isolated-galaxy lensing guard (S4): |v3/law − 1| ≤ 0.14 at R ≤ 1.1 Mpc in all four mass bins. Read from S4: passes for
  μ_K ≤ 0.03 Mpc⁻¹, fails for μ_K ≥ 0.1. Applies to every khronon candidate's static branch (C0, C1b, C2).
- Reported with (d): U1 A2's frame reading (field galaxies KEPT at the cap; DEPENDS at BS24's own μ_K).
- (d) PASS iff (d1), (d2) and (d3) PASS at the point; FAIL iff one FAILS at every allowed point; else UNDECIDED. C4: the static
  law is identical (cap-n1, H1); AeST's collapsed dust in galaxies is not computed in the record ⇒ UNDECIDED.

**(e) Health and a radiation era.**
- (e1) C5-type sign conditions (no ghost, no gradient instability on the backgrounds C5 tested). C0: C5's verdict (CONDITIONALLY
  HEALTHY, C4-literal form) ⇒ PASS. C2: M1 R1(c) PASS (flag: C5's edge f = 1, M_T = ∞). C1b: the khronon part as C0, the mimetic
  part by X-D9. DBI sub-rows: C5's conditions K″ > 0 and Q̄ ≥ 1 checked for DBI (X-D10). C4: H1's theorem T1 (the ω = 0
  negative-energy mode is the dust growth mode, for every F in AeST's class) ⇒ FAIL.
- (e2) A radiation era: Q6's BBN line ΔN_eff,equiv(1 MeV) ≤ 0.5. Quadratic K: Q6's μ_K,BBN (read) ⇒ FAIL at every allowed μ_K.
  C1b: ΔN_eff ∝ I₀²/μ_K² with I₀ ∝ (1 − f_d) (X-D8) ⇒ PASS iff 1 − f_d ≤ μ_K/μ_K,BBN. DBI sub-rows: Q7 (BBN passes at all four
  sets) ⇒ PASS.
- (e) PASS iff (e1) and (e2).

## 4. Verdict classes (frozen) and the stop rule

1. **A CANDIDATE PASSES ALL FIVE (name):** one candidate row (one K variant), one parameter point, five PASS.
2. **BEST CANDIDATE FAILS <which>:** no five-PASS row, but some row has no FAIL at some point (its non-PASS entries are all
   UNDECIDED); <which> names those tests (it does not pass them). NO-GO is then not claimed.
3. **NO-GO FOR THE STATED CLASS:** every graded row has at least one FAIL at every allowed parameter point. The README names
   the row(s) with the fewest FAILs and which tests they fail.

"The stated class": dust couplings derivable from an action in v3's family (BS khronon + J + K + P/γ_L, matter on g), plus a
separate geodesic field dust, plus AeST's cold sector, each with no new fitted constant.
**Stop rule.** In outcomes 2 and 3 there are no follow-up scans and no new candidates after seeing results. A POST-RESULT
amendment may only correct errors, never add candidates.

## 5. Checks (`x6_dust_coupling.py`; one line each; exit 0 iff all PASS)

Symbolic (sympy; residual 0 = exact):
- **X-D1** kinematic identity: a_i = ∂_i ln N and n^μa_μ = 0 for (i) ds² = −N²dt² + e^{2ζ}δ_ij dx^i dx^j and
  (ii) ds² = −N²dt² + δ_ij(dx^i + β^i dt)(dx^j + β^j dt), N, ζ, β^i general functions of (t, x, y, z).
- **X-D2** mimetic dust: (i) for any scalar φ, u_μ = ∂_μφ: u^ν∇_νu_μ − ½∂_μ(g^{νρ}u_νu_ρ) ≡ 0 on metric (ii) (so the
  constraint g^{μν}∂φ∂φ = −1 makes the congruence geodesic); (ii) PN: X ≡ −g^{μν}∂_μτ∂_ντ = 1 − 2εΞ + O(ε²) for τ = t + σ,
  g = diag(−(1 + 2εΦ), (1 − 2εΦ)δ_ij), σ̇ = O(ε), |∇σ|² = O(ε) (so Q = X^{−1/2} = 1 + εΞ, and Q ≡ 1 ⟺ Ξ = 0).
- **X-D3** α-family statics (spherical, μ_K = 0): static held dust gives (α − 1 + μ(X/a₀))X = g_N with baryon gravity g = αX;
  lim_{g_N→0} g²/(g_N a₀) = 1 at α = 1, = ∞ at α = ½ (floor (1 − α)a₀), = 0 at α = 2 (rescaled Newton).
- **X-D4** the kernel s(k; f₀, α) from the linearised hold (residual 0 against M1's form at α = 1), ∂s/∂f₀ < 0, s(α = 0) = 1.
- **X-D5** T3 statics for any J: σ = −Ct ⇒ Ξ = Φ + C ⇒ ∇ψ = 0 (host force on khronon dust zero); momentum of a bound unit:
  a = g M_b/(M_b + M_τ) for khronon dust (α = 1); a = g for separate geodesic dust.
- **X-D6** C1b statics: with the khronon held (Ξ = Φ + C), Poisson + hold give r²μ(Φ′/a₀)Φ′ = G(M_b + M_d) (spherical,
  μ_K = 0): the separate dust sources the law like baryons (universal; CFG946 O2a-3). And ρ_τ ≡ 0 ⇒ Ξ ≡ 0 (linear hold
  operator ∇² − μ_K² has no decaying homogeneous solution).
- **X-D7** C3β: in a held host the baryon force is (1 − β)g_host and the dust force 0; relative acceleration (1 − β)g_host.
- **X-D8** quadratic K background: 8πGρ̄ = I₀/a³ + I₀²/(4μ_K²a⁶) (stiff term ∝ I₀²).
- **X-D9** mimetic dust about Minkowski (φ = t + π, λ = λ̄ + δλ): the quadratic Lagrangian enforces π̇ = 0 (no propagating mode,
  no gradient term), and the quadratic energy on the constraint surface is λ̄|∇π|² ≥ 0 for λ̄ > 0 (positive dust density).
- **X-D10** DBI: K″(Q) = 2μ²(1 − λ_D(Q−1)²)^{−3/2} > 0 on its domain, K′(1) = 0, K″(1)/2 = μ² (same static mass).

Reproductions and reads:
- **X-K1** U1: my median of Delta_B0 equals U1's N5 B0 median (≤ 1e-9) and my bootstrap sd is within 0.01 of U1's, both
  footings; Coma z_sys = ⟨E⟩/√(se² + σ_sys²) reproduces U1's z_sys (≤ 1e-6).
- **X-K2** the ODE reproduces M1/F3 at μ = 14.79771 h/Mpc, a_i = 1e-3: 0.39080 (f₀ = 0) and 0.12055 (f₀ = 1), ≤ 1e-3 relative;
  the three-fluid ODE at f_d = 0 equals the two-fluid value (≤ 1e-6) and at f_d = 1 equals 1 (≤ 1e-6).
- **X-K3** CFG946: the universal D-F BTFR at r_ta (6.56 / 6.54 in `cfg946_results.json`) to ≤ 1e-3 relative, and the deep limit
  (M_b + M_d)/M_b = 6.364 (symbolic).
- **X-K4** P4: the law's iso_perUps rms within 1e-4 and the same median Υ, both footings (`p4_v3_galaxy_tiles_results.json`).
- **X-K5** record reads: sha256 of every record JSON read is stored; each quoted value is found (S4 verdict_A1 and knob lists;
  F1 `dust` and `addendum_L187` rows; Q6 μ_K,BBN; Q7 BBN and R_B; H1 verdict and T1; H2 verdict_A1; C5 checks; M1 R1b(iii) and
  verdicts; U1 N5).
- **X-G** every grade cell is computed (PASS / FAIL / UNDECIDED with its number and JSON key).
- **X-R** peak RSS < 1 GB.

## 6. Mutation (`X6_MUTATE=1` → `x6_dust_coupling_MUTATE.out`, `x6_dust_coupling_results_MUTATE.json`)

C0's dust coupling is switched to −∇Φ (α = 0, U1's mutation). X-D5 must FAIL (host force on held dust −∇Φ_host ≠ 0; fall
rate g) and X-K2 must FAIL (the khronon kernel becomes s ≡ 1, so R = 1 ≠ 0.391). Everything else unchanged; exit 1.

## 7. Compute

`OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS, ≤ 30 min per run; one CLASS run (background A); no PM simulation;
no downloads; no other lane, `compute_queue/` or the live L1 run touched; `python3 compute_queue/heavyq.py status` checked
before each run.

## 8. What a result here cannot say

No nonlinear growth (L1's job). No native cluster dust profile (C1b's cluster grade uses F1's two record shapes). C1b's dust
content in satellites, UDGs and galaxies uses record estimators (cosmic ratio; CFG946's D-F), not a simulation. AeST (C4) is
graded from the record only. The BS24/BS25 equations are WebFetch transcriptions (PROVISIONAL), checked for self-consistency
by C4/Q6/Q7. The cluster OUTER baseline is F1's β = 2/3 gas extrapolation (X0 A1; lane X2).

## AMENDMENT A1 (POST-RESULT, 2026-10-23; code only, error correction; no line, threshold, candidate or reading changed)

The first complete main run (`x6_dust_coupling_RUN1.out`, `x6_dust_coupling_results_RUN1.json`, kept) failed the frozen
X-R line: peak RSS 4.36 GB against < 1 GB (16/17, exit 1). Cause: `solve_ivp` stored every step of ~150 ODE solves and macOS's
medium malloc zone kept the freed buffers resident (the same effect U1 disclosed). Fix: `solve_ivp(..., t_eval=[0.0])` keeps
only the endpoint, freed blocks are handed back after each solve, and the script re-executes itself with
`MallocMediumZone=0` (as U1). The rerun gives 17/17, peak RSS 0.177 GB, and every one of the 165 numeric leaves of the results
JSON equal to RUN1's (maximum relative difference 0). The free memory on the machine stayed above 30 GB during RUN1; the live
L1 run and `compute_queue/` were not touched.
