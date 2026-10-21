# CFG941: self-gravity repair of CFG938's covariant parent (frozen criteria, committed alone)

Block CFG940–949 (owner, 2026-10-20 ~23:00: "launch the self-gravity fix"). This file is written and committed **before** any
derivation output, script or number of this lane. It fixes the questions, the repairs, the tests, the controls and the class
rules. Any later change is a dated, labelled amendment in this directory.

**Settings.** κ = ½ FITTED (never derived). Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), never pooled.
The extra mass is cold energy, never a dark-matter particle; no particle species is added. Framework-native inputs only; no
ΛCDM or standard-MOND yardstick in any verdict. Not "theory closed"; never "the data favour the framework". STRUCTURAL
OBSTRUCTION is reported as plainly as RESTORED.

**Inputs (read only).** THEORY_CANONICAL_2026-10-14.md S2/S3; CFG938 (README, DERIVATION, cfg938.py: the parent action, its
K1/S4/S6/S8 numbers and its M3 tooth); CFG939 (README, DERIVATION: exact identity through crossing, conservative tether only
expels); CFG888 (no self-gravity under ID; coupling G); CFG925 R3 (satellites: the framework's EFE worsens them; the record's
dwarf numbers are EFE-free); CFG649 R-A1/R-A2 (class A's switch: extra source only on turnaround catchments, zero-sum per
catchment, own baryons); CFG650/CFG654 (class-A engine; T1x/T2x/NC1x shear results); CFG847 (five systems, slip bound
1.9e-5, class line 1e-2); CFG882 (Plummer dwarfs H1 1e4 M⊙/30 pc, H2 3e5/200 pc, H3 2e7/700 pc); `CFG4_common.A0`; the
record's SPARC file for NGC 3198 (Υ = 0.61, as CFG938); declared cosmological inputs as CFG938 (Ω_b 0.0493, Ω_c/Ω_b 5.364,
H₀ 67.4; matter era treated as EdS after recombination, z ≤ 1100). sol61_push/cold_completion_2026_10_20/
GRAVITY_ACTION_AUDIT.md and REVIEW_COMMON_ACTION.md are cited, never edited or duplicated. Nothing is downloaded.

## 1. Diagnosis questions (each answered in DERIVATION.md with a sympy check)

- **D1.** Static weak-field limit of CFG938: vary in Φ. Is the medium's mass counted once in Poisson (∇²Φ = K(ρ_b + ρ_c)), or
  does S2's P·∇Φ double count with mc²n?
- **D2.** Which term cancels the medium's self-gravity? Show it as (i) an energy statement (mode average ⟨L⟩, including the
  C₁C₂ cross term of two tethered components, with a general tether quadratic coefficient c₂, W ≈ c₂u²/2K) and (ii) a force
  identity on a medium element (−∇Φ + D_full(u)∇̂χ with Φ = Φ_b + χ).
- **D-T (theorem).** For any always-on tether force F(u) on a cold static medium whose phantom is its own gravitating mass:
  does the law g_N = g²/(g + a₀) (all g_N > 0) force F = D_full, hence c₂ = 1? Does any law with the deep limit
  g_N → g²/a₀ force c₂ = 1? If so, linear self-gravity of the tethered medium and the mutual gravity of tethered components
  vanish identically wherever the tether acts with its static-law coefficient (F1 and the cross-term part of F2).
- **D5.** CFG938's FRW background has χ = χ̄(t) with D²χ̄ = −3Hχ̄̇/c² = Kρ̄ (its S1d). Compute u² = h^{μν}∂_μχ∂_νχ to second
  order in the medium's peculiar velocity v and δχ (covariant, sympy). Does the timelike gradient enter u at O(c⁰)?
- **D6.** From the quadratic Lagrangian (comoving, sub-horizon, EdS, baryons free after recombination), the growth exponent n
  (δ ∝ aⁿ) of the tethered medium: (i) in CFG938's S6 approximation (medium feels baryons only), (ii) with the full quadratic
  action of D5 (if D5 gives an O(c⁰) term). Both are reported; (i) is the K control.
- **Hover lemma (H).** In any static cold tethered equilibrium the net force on medium at rest vanishes. What does this imply
  for a satellite's tethered medium inside a host's settled medium?

## 2. Repairs (declared now, before any computation)

P0 (unrepaired, CFG938): S = ∫√−g [c⁴R/16πG − mc²n − W_full(u) − (3γ/4K²)τ_μντ^μν + λ(D_μD^μχ − Kmn)] + S_b.

- **R1 — rest-mass gravity separated, tether only redistributes.** P0 with W_full → W_rem (the critical quadratic u²/2K is
  removed from the tether), so the medium gravitates as dust through −mc²n and the tether has no quadratic term. The R1
  *family* is every always-on tether T(u) = c₂u²/2K + O(u³) added to dust gravity; D-T decides the family.
- **R2 — P sources only the settled excess.** The only local realization: two separately conserved label-field media,
  −mc²n_f (free dust, no tether) and −mc²n_t (tethered, the full P0 tether sector with χ sourced by n_t only). No conversion
  term (none follows from an action; conversion is the record's S4/B1 obligation). Cosmological tethered fraction f_t is free.
- **R3 — the record's switch (CFG649 R-A1: no tether before turnaround), realized locally.** A C² gate s ∈ [0, 1] multiplies
  the whole tether sector (W_full and the stiffness); λ(D²χ − Kmn) is left ungated (harmless: λ = 0 when s = 0). Three
  realizations, all declared now:
  - **R3n (density gate):** s = s(ρ_c), s = 1 for ρ_c ≥ ρ_*, 0 for ρ_c ≤ ρ_*e^{−Δ}, quintic smootherstep in ln ρ between;
    Δ = 1; ρ_* = the smallest value keeping s = 1 on all 43 NGC 3198 radii (least restrictive choice for (c)).
  - **R3θ (turnaround gate):** s = s(θ), θ = ∇_μu^μ the medium's expansion; s = 1 for θ ≤ 0, 0 for θ ≥ θ_s, quintic
    smootherstep between; θ_s = H₀ (any θ_s in (0, 3H₀] gives the same classes; stated, not scanned).
  - **R3ℓ (range gate):** finite range of the medium's own potential, D²χ − χ/ℓ² = Kmn.
- **(R3 note)** Class A's own switch (enclosed mean 1 + δ ≥ Δ_ta(z) on balls around resolved peaks) needs the cosmic mean
  density and a ball around a peak: it is not a local covariant scalar and is not a repair of the action; it is discussed, not
  graded.

## 3. Tests per repair

- **(a) Static law + deep BTFR.** The repair's static, spherical, cold, γ → 0 limit; the Euler–Lagrange equation derived by
  sympy from the reduced energy functional. PASS iff max |g/g_law − 1| < 1e-6 at all 43 radii of NGC 3198 on both footings
  AND the deep BTFR holds: lim_{y→0} V⁴/(G M_b a₀) = 1 for a point mass (y = g_N/a₀, sympy), with the numeric value at
  y = 1e-12 within 1e-6 of 1 (both footings). R2 is graded with the galaxy composition its own equations deliver (§4).
- **(b) FRW.** T^μ_ν diagonal and isotropic, w = 0 exactly for the medium(s); the repair's added structure vanishes on FRW
  (sympy).
- **(c) Linear growth.** Local growth exponent n of the medium that settles into the law in galaxies, from the repaired
  action's quadratic Lagrangian on EdS (Ω_c/Ω_b = 5.364, baryons free), with CFG938's χ̄ background where present. Gates take
  the value their own rule assigns to cosmic-mean linear perturbations at each z ≤ 1100. PASS iff |n − 1| < 1e-3 at every
  z ≤ 1100 for every comoving k in [0.01, 5] h/Mpc at super-L* scales (k_phys L* → 0). Sub-L* (k_phys L* ≥ 10): graded only
  for "no growth faster than a¹ and no instability"; Jeans suppression by the stiffness is reported, not graded. a₀ drops out
  at linear order; both footings are printed.
- **(d) Well-posedness.** Linearized about (i) FRW, (ii) the static law state (CFG938 grid: kL* ∈ [1e-2, 1e5], angle
  θ ∈ [0, π/2], u₀/a₀ ∈ {0.0909, 0.5, 0.9, 0.99}, or the repair's own static states), and (iii) for gates, the gate's
  transition region. PASS iff the kinetic matrix is positive definite and ω² is real and bounded below independent of k
  (bounded Jeans growth allowed). CFG938's conditions (γ > 0, ρ_c c² > D(u)u/K) are inherited and stated.
- **(e) Slip.** s_∇ and s_847 (CFG938's definitions) on CFG847's five systems, both footings, on the repair's own static states.
  PASS iff every value ≤ 1.9e-5 (and ≤ 1e-2).
- **(f) F2.** A satellite at the centre of its own medium in a 6e10 M⊙ host's settled field at 50 / 100 / 250 kpc (CFG938 S8's
  host), both footings: Δa = a_medium(CoM) − a_stars, toward the host. PASS iff |Δa| ≤ 0.01 g_host at every radius and footing.
  Reported alongside: the mutual (C₁C₂) term; H1–H3 internal baryonic binding vs Δa and the separation time; the ambient
  medium's response frequency vs the satellite's crossing rate; the on-axis EFE factor of a static satellite phantom.
  "CFG925 R3 respected" iff (f) PASSES and the EFE factor is within 0.01 dex of 1 for H1–H3 at all three radii.
- **(g) Class-A limit.** The NR limit is class A iff (g1) every cold-energy element feels exactly −∇Φ with
  ∇²Φ = K(ρ_b + ρ_c) in every regime (universal coupling, Newtonian self-gravity); (g2) a catchment's settled phantom is the
  law of that catchment's own baryons only (no free-mass, neighbour-medium or host-medium term); (g3) the linear regime is pure
  dust. PASS iff all three hold (structural, from the equations). PASS ⇒ T1x/T2x/NC1x transfer; FAIL ⇒ they do not.

## 4. Joint reading of (a) and (c)

(a) and (c) must hold for the same medium in one history under the repair's own equations ("repair F1 without losing what
CFG938 won"). For R2 this means: if f_t = 1, (c) is graded on the tethered medium; if f_t < 1, galaxies form from the cosmic
mix (the action has no segregation or conversion), so (a) is graded with free mass present at the cosmic free-to-tethered ratio
in the same shape as the tethered phantom (declared minimal model), and the tethered supply (f_t × 5.364 M_b × catchment
factor ≤ 10, CFG888's largest stock 53.64 M_b) is compared with NGC 3198's phantom mass inside its last radius.

## 5. Controls

**K (must pass, else VOID until fixed and disclosed):**
- K1: NGC 3198 law from CFG938's reduced Euler–Lagrange equation, max deviation < 1e-6 both footings (CFG938: 2.2e-16).
- K2: FRW dust w = 0 exactly (sympy).
- K3: CFG938's S6 growth exponent by its own matrix method: n = 0.6096 ± 1e-3.
- K4: this lane's Lagrangian route at (c₂ = 1, no χ̄ gradient) equals K3 to 1e-6; at c₂ = 0 it gives n = 1 to 1e-12.
- K5: CFG938's worst slip s_847 = 1.54e-5 reproduced to 2%.
- K6: R1's static solve reproduces CFG938's M3 law deviation (1.6 canonical / 1.9 alt) to 2%.

**MUTATE (separate `_MUTATE` outputs; each must bite; exit 1 by design, 2 if a tooth fails):**
- M1 remove each repair → the S6-approximation exponent 0.61 returns (within 1e-3): R1 (c₂ → 1), R2 (f_t → 1),
  R3θ (s ≡ 1), R3ℓ (ℓ → ∞).
- M2 double count the phantom → NGC 3198 law deviation > 1e-6 on both footings: (M2a) source multiplicity 2 (dust −ρ_cΦ and
  S2's P·∇Φ both kept under ID); (M2b) an independent-P phantom plus the medium's own mass at the law density.
- M3 boost tooth: dropping the χ̄ timelike-gradient term must change the full-action exponent by > 1e-3 (if D5 finds no O(c⁰)
  term, M3 is toothless and is flagged, not hidden).
- M4 hover tooth: tether off (Newtonian medium) → Δa = 0 to 1e-12 g_host.

## 6. Classes (frozen)

Per repair:
- **REPAIRED:** (a)–(g) all pass.
- **NOT REPAIRABLE:** a theorem or analytic argument (with a sympy or numeric check) shows that within the repair's declared
  structure no choice of its free functions or constants gives the medium that settles into the law a linear growth exponent of
  1 while keeping (a) — i.e. F1 is structural for that repair.
- **PARTIAL:** otherwise; every failing test is listed.

Overall:
- **SELF-GRAVITY RESTORED:** at least one repair is REPAIRED.
- **CONDITIONAL:** none is REPAIRED, but at least one passes (a), (b), (c), (d) and (e) together; (f)/(g) outcomes and every
  condition are listed.
- **STRUCTURAL OBSTRUCTION:** no repair passes (a)–(e) together, and D-T's check passes (F1 proven structural to S2+S3 for
  always-on tethers).
- If no repair passes (a)–(e) and D-T fails its check: **NOT REPAIRED (no proof).**

## 7. Hand expectations (disclosed before any script; not results)

- D1: Poisson counts the medium once; the cancellation is a force cancellation by the tether's quadratic part, not a source
  double count. D-T: the deep law forces c₂ = 1, which cancels both self-gravity and the C₁C₂ cross term.
- D5/D6: the χ̄ timelike gradient probably enters u as |∇δχ + (χ̄̇/c²)v| with χ̄̇/c² = −Kρ̄/(3H), O(c⁰). Hand estimate of the
  full-action exponent of the unrepaired parent: about a^0.69 (not a^0.61), still not a¹. If confirmed, this is a correction to
  CFG938's S6; CFG938's files are not edited.
- R1 ≡ CFG938's M3: fails (a) (acceleration floor a₀/2); D-T makes it NOT REPAIRABLE.
- R2: f_t = 1 fails (c); f_t < 1 puts self-gravitating free mass into galaxies (it enters the law's source) and starves the
  tethered supply: NOT REPAIRABLE expected.
- R3n: the deep BTFR needs the gate on at arbitrarily low density, i.e. s ≡ 1: NOT REPAIRABLE expected. R3ℓ: (a) needs ℓ far
  above galaxy scales, (c) needs ℓ below pc–kpc scales: NOT REPAIRABLE expected. R3θ: passes (a)–(c) and (e) but its
  s″(θ)W(∇·v)² term is a ghost in the transition region: PARTIAL expected.
- Hover lemma: every static tethered equilibrium leaves a satellite's tethered medium with zero host force, so (f) fails for
  every tethered sector; (g) fails for every repair, so the shear results do not transfer.
- Expected overall: STRUCTURAL OBSTRUCTION. These expectations may be wrong; results are reported as they fall.

## 8. Compute

One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, in-script RSS guard aborting above 1 GB, sympy + small
numpy/scipy, seconds to minutes. A live 1024³ job runs beside this lane; nothing touches it.
