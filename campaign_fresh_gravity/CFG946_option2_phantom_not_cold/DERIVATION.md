# CFG946 DERIVATION: option 2, cold energy is NOT literally the law's phantom

Criteria: `FROZEN_CRITERIA.md` (08f3b30a6, committed alone first). Amendment A1 (23e0a5765; code and reporting only, no class
change). Every load-bearing step has a sympy or numeric check in `cfg946.py`; check names are in brackets. κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m s⁻², never pooled. K = 4πG. Law: g_law(g_N) = [g_N + √(g_N² + 4g_N a₀)]/2, u_ph = g_law − g_N,
R(u) = u²/(a₀ − u), so R(u_ph) = g_N. Not "theory closed". Nothing here says the data favour the framework.

**Overall class (frozen rule): NO-GO (theorem T-O2).** All eight constructions are NOT VIABLE. The four lemmas behind the
theorem pass their checks.
- The decisive structural fact is L-G. Any local, second-order field sector that supplies the profile-independent deep law
  breaks uniform-field superposition, so it carries an external-field effect (EFE).
- With CL-AR and CFG925 R3 read as "no EFE", the deep-regime extra force must therefore be the dust's own mass. That means
  cold energy *is* the phantom in the deep regime, which contradicts option 2's premise.
- Taking that fallback anyway does not help. Static selection of the dust profile then needs held (tethered) dust. D-T′ shows
  the holding force cancels the dust's linear self-gravity, which is CFG941's obstruction again.
- Dropping the no-EFE assumption costs data instead:
  - satellites would need 0.28–0.37 dex more bound cold mass than isolated dwarfs (z 2.7–3.7);
  - tidal dwarfs stay 3.5σ / 3.8σ below a field-supplied law;
  - every field sector also fails a¹ growth, well-posedness about FRW, or lensing.

---

## 1. The constructions (as frozen)

All of them share these elements:
- dust (F = −mc²n), with ∇²Φ_N = K(ρ_b + ρ_d);
- Ω_c/Ω_b = 5.364;
- universal free fall of the dust, which feels its own gravity once.

| id | separate sector | coupling |
|---|---|---|
| O2a-1 | QUMOND-type X: ∇²φ_X = ∇·[ν̃(\|∇ψ_b\|/a₀)∇ψ_b], ∇²ψ_b = Kρ_b | literal: X in the metric, felt by all matter and light, sourced by baryons only |
| O2a-2 | same | variational, baryon-only: X sourced and felt by baryons only (a fifth force) |
| O2a-3 | same, ψ sourced by ρ_b + ρ_d | variational, universal ("MOND + cold dust") |
| O2a-G | O2a-1/3 × CFG941's turnaround gate s(θ) | X off where the medium expands |
| O2b | QUMOND-type in the field of the dust's settled excess, ∇²ψ_ex = Kρ_ex | felt by all matter |
| O2c | tether W = W_rem + c₂u²/(2K) on the dust (CFG941's c₂ ≠ 1 branch) | dust gravity kept (multiplicity 1) |
| O2d1 | Galilean-symmetric field (equations in second derivatives only; Galileon class) | universal |
| O2d2 | none; the dust halo is held by velocity dispersion and equals the phantom | universal gravity |

AQUAL form of X (used for the static stress and the spherical checks): L_X = −W_rem(|∇φ_X|) − σφ_X with K W_rem′ = R. In
spherical symmetry it gives |∇φ_X| = u_ph exactly, as QUMOND does.

## 2. Four lemmas

### 2.1 L-AR: felt-by = sourced-by [L-AR]
- In an action, a coupling −σ_iρ_iφ produces both the force −σ_i∇φ on species i and the source σ_iρ_i in φ's field equation.
  The sympy check reads off both coefficients from L = −W(φ′) − (σ_bρ_b + σ_dρ_d)φ.
- So O2a-1 ("sourced by baryons, felt by dust") and O2b ("sourced by dust, felt by baryons") are not variational, and total
  momentum is not conserved.
- Example: NGC 3198's baryons plus 5.364 M_b of dust at 50 kpc. The pair self-accelerates at a_cm = 1.22e-11 m s⁻² = 0.130 a₀
  (canonical).
- The consistent versions are O2a-2 (X not felt by dust) and O2a-3 (dust sources X).

### 2.2 L-G: no-EFE fields cannot supply the deep law [L-G]
**Statement.** Let φ be a field whose gradient is a universal force. Its static equation E = 0 is local, second order and
translation/rotation invariant. Assume exact uniform-gradient superposition: if φ solves E with source ρ, so does φ + b·x for
every constant b. This is the statement that a satellite in a host field that is uniform across it keeps its internal dynamics,
and only its centre of mass accelerates. Under these assumptions:
1. E depends on φ only through ∂∂φ.
2. Its flat-field amplitude A = lim r|∇φ| obeys A(μ³M, μR) = μ²A(M, R).
3. The deep law requires A = √(GMa₀), i.e. μ^{3/2}.

Hence no such sector supplies the deep law. Contrapositively, every sector that does supply it has an EFE.

**Proof.**
1. Solutions of a second-order elliptic equation realise every admissible 2-jet at a point, so the zero set of E must be
   invariant under ∇φ → ∇φ + b and under the induced shift of φ. Hence E = E(∂∂φ; ρ). With several fields, the same applies to
   each.
   - Higher derivatives are excluded by second order (no Ostrogradsky ghost).
   - Constants such as G, a₀, c and H₀ can enter. From s⁻² quantities they can only form frequencies, which the dilation below
     leaves unchanged.
2. For φ_μ(x) = μ²φ(x/μ), the identity ∂_i∂_jφ_μ(x) = (∂_i∂_jφ)(x/μ) holds. Sympy verifies it for a generic φ(x, y, z). So φ_μ
   solves the same equation with ρ_μ(x) = ρ(x/μ): the same density, size ×μ, mass ×μ³.
3. If rφ′ → A, then rφ_μ′ → μ²A (sympy).
4. The deep law gives μ^{3/2}A for every μ ≤ 1. Smaller systems at equal density are deeper (g_N ∝ μ), so the deep regime is
   preserved. μ² = μ^{3/2} only at μ = 1 (sympy). ∎

**Corollary (share).** Suppose a sector respects superposition but supplies part of the force. At fixed density its share of
the deep amplitude scales as μ^{1/2} → 0, so small deep systems must take their whole extra force from mass.

**Examples (the checks).**
- Deep AQUAL, div(|∇φ|∇φ): it vanishes on A ln r and is 0.154 after adding b z.
- QUMOND, div(ν̃∇ψ) on the point potential −A/r: 0.690 without the uniform gradient and 0.497 with it.
- Both are therefore not Galilean, and both have an EFE.
- A cubic Galileon (Galilean): c₁x + c₂x² = GM/r³ gives r²x → 0 at both r → 0 and r → ∞, so it has no flat regime.

### 2.3 D-T′: the holding force cancels whatever self-gravity the dust feels [D-T']
- Setup: cold static dust held in the law by an always-on local force F(u), where u is the dust's own Newtonian field. Its field
  acts on baryons with multiplicity m and on itself with multiplicity m′.
- Equilibrium is F(u) = g_N + m′u. The law gives g_N = R(mu) (simple law), or (mu)²/a₀ + O(u³) for any law with the deep limit
  g_N → g²/a₀; h₁, h₂, h₃ are left free in the sympy check.
- Hence F(u) = m′u + O(u²), and F′(0) = m′ for every m and every deep-limit law.
- In the linear regime the dust feels m′Kδρ from itself. The holding force removes F′(0)Kδρ = m′Kδρ, so the net is zero.
- This is CFG941's D-T (m = m′ = 1), generalised. Amplifying the dust's gravity with an extra sector does not help: the holding
  force always cancels whatever self-gravity the dust actually feels.

### 2.4 N-L: a field-supplied deep law has no linear regime about FRW [N-L]
- g_X(y) = a₀(√(y² + 4y) − y)/2, so dg_X/dg_N → ∞ as g_N → 0. The response of such a sector to small perturbations of a
  zero-field (homogeneous) background is not Lipschitz.
- For the plane-wave displacement in the deep regime, ξ̈ = C√ξ with ξ(0) = ξ̇(0) = 0 has two solutions, ξ ≡ 0 and ξ = C²t⁴/144.
  The Cauchy problem about FRW is not unique.
- A sector that supplies the deep law and acts on cosmological perturbations is therefore ill-posed there, unless it is gated
  off.

## 3. Theorem T-O2 (option 2 has no local construction)

**Assumptions.**
- **A1 (option 2).** Cold energy is pressureless, universally coupled dust in free fall, with Poisson self-gravity.
- **A2 (locality).** Every other sector is local, second order and translation/rotation invariant. Every force is universal
  (passive = inertial).
- **A3 (the law).** Isolated rotators obey the law with the profile-independent deep amplitude A = √(GM_b a₀), for any assembly
  history. The law is selected by static equations.
- **A4 (no EFE).** A uniform external field leaves a satellite's internal dynamics unchanged. This is CL-AR at uniform order and
  the record's reading of CFG925 R3.

**Claim.** No construction satisfies A1–A4.

**Proof.**
1. By A2 and A4, every field sector respects uniform-gradient superposition. By L-G, its share of the deep amplitude vanishes as
   μ^{1/2}, and it cannot produce A ∝ M^{1/2}.
2. So the deep extra field of isolated rotators is the dust's own Newtonian field: cold energy is the law's phantom in the deep
   regime. Option 2's defining premise (the extra force comes from a separate sector) fails. This already settles option 2
   proper.
3. Fallback: accept dust = phantom. A3 then needs the dust profile to be selected by the baryons through static equations.
   - By CL-AR Proposition 2, a local Galilean-covariant law can read |g| only through matter held static by non-gravitational
     stress (a_rel = −g).
   - Free-falling dust (A1) has a_rel = 0. Its static (Jeans/Vlasov) equations admit a family of equilibria for the same
     baryons. Shown: dust × 0.5 is another hydrostatic equilibrium, and it misses the law by 0.414 / 0.421 on NGC 3198. So
     free-falling dust has no selection.
   - Held dust falls under D-T′. The holding force cancels its linear self-gravity wherever it acts, which contradicts A1.
   - Restricting the holding force to settled regions is CFG941's gate family: R3θ has a ghost, and R3n / R3ℓ fail the BTFR.
   - ∎

**Scope (stated, not hidden).** The theorem covers static selection by local, second-order sectors. Four routes are outside it:
1. **Non-static, non-local supply.** CL-AR's open branch: assembly over ℓ ≳ r. NGC 3198's phantom (4.78 / 5.30 M_b inside
   44.1 kpc) assembled from cosmic-mean dust needs ℓ_min = 1129 / 1171 kpc = 25.6 / 26.6 R, while a local response generates at
   most ≈ 3ℓ/r. This is option 3 (CFG947), not option 2.
2. Non-local or higher-derivative field sectors.
3. Modified inertia (non-local in time).
4. EP-violating charges, CL-AR's other exit.

Routes 2–4 drop A2.

## 4. Results per test

### (a) The law in rotators without double counting
NGC 3198 (43 radii, M_b = 4.72e10 M⊙ inside 44.1 kpc, fair-catchment turnaround radius r_ta = 688.7 kpc). Values are the max
deviation from the law, relative and in dex, canonical / alt:

| dust content | X baryon-sourced (O2a-1/2/G) | X universal (O2a-3) |
|---|---|---|
| D-A (class-A dust = phantom) | 0.827 / 0.841 (0.26 dex) | 1.743 / 1.856 (0.44 / 0.46 dex) = CFG941 M2b |
| D-F (5.364 M_b isothermal to r_ta) | 0.501 / 0.483 (0.18 dex) | 0.520 / 0.507 (0.18 dex) |
| D-U (uniform at turnaround dust density) | 2.4e-4 / 2.2e-4 (1e-4 dex) | 7.7e-4 / 7.6e-4 (3e-4 dex) |

- **BTFR V⁴/(G M_b a₀) at r_ta.** Bare law 1.012 (its own √y correction at finite radius).
  - Baryon-sourced X with D-F/D-U dust: 1.148 / 1.134.
  - Baryon-sourced X with D-A dust: 4.000.
  - Universal X: **6.56 / 6.54**.
- **Symbolic deep limits.** Baryon-sourced X with finite dust → 1; with class-A dust → 4; universal X → (M_b + M_d)/M_b = 6.364.
- No O2a rule keeps dust out of galaxies, and dust feels at least their Newtonian pull. At data level the most diffuse dust
  (D-U) is invisible in NGC 3198. The fair-catchment and class-A contents are not (0.18–0.46 dex). O2a-3's catchment-edge BTFR
  fails structurally (×6.4).
- **O2b.**
  - The law needs the settled dust slaved to the baryons: g_ex = u²/(u + a₀), so M_ex/M_ph = 0.147 / 0.137 at the last radius.
  - O2b has no slaving rule. A second admissible equilibrium (dust × 0.5) misses by 0.256 / 0.259, and fair-catchment dust
    misses by 0.481 / 0.459.
- **O2c.** The static law becomes **g_N = R(u) − (1 − c₂)u**.
  - For c₂ < 1 it has an acceleration floor u_f = a₀(1 − c₂)/(2 − c₂). Deep BTFR limits: c₂ = 0 and ½ → ∞; c₂ = 1 → 1;
    c₂ = 2 → 0 (rescaled Newton).
  - Growth needs c₂ ≤ 3.517e-3 (full action with the χ̄ term; 2.346e-3 without it, as CFG941). There, the law deviation is
    1.641 / 1.880, the floor is 0.4991 a₀, and V⁴/(GMa₀) at y = 1e-14 is 2.5e13.
  - No c₂ passes (a) and (b) together.
- **O2d1.** Fails structurally by L-G (cubic Galileon BTFR limit 0).
  - Its best two-parameter fit to NGC 3198's 43 radii misses by 0.154 / 0.169 (0.07 / 0.08 dex). Over one finite curve that is
    not far off.
  - It needs c₁ = 0.205 / 0.189, a linear fifth force 4.9 / 5.3 × Newton.
- **O2d2.** The law holds only if the dust is exactly the phantom, and nothing selects that (see T-O2 step 3, and the ℓ_min
  above). Isothermal identity σ² = V_f²/2: verified (sympy).

**(a) FAILS for all eight constructions.**

### (b) a¹ growth
- **Inputs.** The n-line |n − 1| < 1e-3 corresponds to ε_max = 1.6673e-3 (EdS constant-ε mapping). The largest linear-regime
  field at z = 0 (δ = 1 on R = 1/k at k = 0.01 h/Mpc) is y_max = 0.0366 / 0.0303.
- **Reading.** Every ungated field sector is in its deep regime on linear scales and dominates the dust's own force.
  - O2a-1: n = 1.88 / 1.96; a¹ would need y ≥ 593.
  - O2a-2 (two-fluid): n = 1.60 / 1.68; needs y ≥ 89.
  - O2a-3: n = 2.70 / 2.83; needs y ≥ 599.
  - O2b: n = 2.61 / 2.73; needs y ≥ 599.
  - **All FAIL**, by four orders of magnitude in field strength.
- **The other constructions.**
  - O2a-G: the gate is off for the cosmic mean, so pure dust, n = 1: PASS.
  - O2c: PASS only for c₂ ≤ 3.5e-3, where (a) fails. The BTFR value c₂ = 1 gives n = 0.694.
  - O2d1: PASS only for c₁ ≥ 600. At the c₁ its (a) fit needs, n = 2.73 / 2.83.
  - O2d2: n = 1, PASS.

### (c) Satellites and CL-AR
Exact Gauss-flux factor of the enclosed dynamical mass at the Plummer scale radius (the curl part has zero flux). Units are dex,
canonical; alt agrees within 0.01. H1 = 1e4 M⊙ / 30 pc, H2 = 3e5 / 200 pc, H3 = 2e7 / 700 pc, in a 6e10 M⊙ host:

| | 50 kpc | 100 kpc | 250 kpc |
|---|---|---|---|
| g_bh/a₀ (host baryons) | 0.036 | 0.0089 | 0.0014 |
| O2a-1/2/G (H1, H2, H3) | −0.44, −0.52, −0.18 | −0.17, −0.25, −0.015 | −0.005, −0.012, −0.0004 |
| O2a-3 (+ host D-F dust, g_dh/g_bh 0.36 / 0.72 / 1.80) | −0.50, −0.58, −0.23 | −0.27, −0.36, −0.043 | −0.041, −0.092, −0.003 |
| O2b (host settled-dust field) | −0.36, −0.43, −0.14 | −0.15, −0.22, −0.015 | −0.006, −0.012, −0.0005 |

**Record satellites (read only, CFG925 R3).** O2a-1/2's EFE is CFG925's E1/E2: it uses the host baryonic fields with a
QUMOND-type law (CFG925's K7 brackets exact linear QUMOND; this lane's K5 reproduces K7's 4.249).
- Satellites sit +0.489 / +0.449 dex above the EFE-free law.
- E1/E2 lower the prediction by a further +0.480 / +0.710 dex.
- CFG874's isolated-minus-satellite statistic moves from −0.100 ± 0.091 (E0) to −0.284 ± 0.105 (E1, z −2.7) and
  −0.370 ± 0.101 (E2, z −3.7).

Option 2 could in principle fill the gap with bound dust. To do so, satellites would have to hold 0.28–0.37 dex more bound cold
mass than matched isolated dwarfs, against tidal stripping, at z 2.7–3.7 under that assumption.

**(c) FAILS** for O2a-1/2/3/G and O2b (no superposition, 0.1–0.6 dex near the host). It also FAILS for O2c, by hover: Δa/g_host = 1
for any c₂, as CFG941 found. It PASSES for O2d1 (Galilean by construction) and O2d2 (real mass; CL-AR Theorem 1, K3).

### (d) Well-posedness
- **O2a-1:** FAIL on d0 (non-variational, 0.130 a₀ self-acceleration) and d1 (N-L).
- **O2a-2, O2a-3:** d0 passes; d1 FAILS (N-L about FRW).
- **O2a-G:**
  - The gate removes X at linear order.
  - Its kinetic term −½s″(θ)W_X(∇·v)², with W_X = W_rem(u₀), is a ghost band for k > k_g. Here k_g R = 0.088–3.1 and
    k_g L* = 8e-7 to 2e-4, so the band lies well inside the EFT range. This is CFG941's R3θ mechanism: FAIL.
- **O2b:** FAIL on d0 and d1.
- **O2c:** PASS. Min ω²/(Kρ₀) about its static states is 0.004 / 8.0 / 98.0 (bounded Jeans type).
- **O2d1:** PASS, linear order only.
- **O2d2:** PASS (Vlasov/Euler–Poisson).

### (e) Slip on CFG847's five systems
- **Field sectors, minimal (conformal) light coupling.** Light misses X, so s = u/g reaches 0.40–0.92: FAIL by 4–5 orders of
  magnitude. Applies to O2a-*, O2b and O2d1.
  - Best case: X enters both potentials, which needs an extra disformal or vector sector. Worst s_847 = 6.6e-6 and
    s_∇ = 3.3e-6, which would pass, conditionally.
- **O2c** on its own static states: s_847 = 3.27e-5 > 1.9e-5, FAIL (CFG941 R1: 3.28e-5).
- **O2d2:** dispersion pressure of the phantom-shaped dust gives worst s_847 1.54e-5 and s_∇ 7.7e-6: PASS.
  - Observation: in the deep regime the isotropic pressure V⁴/(8πGr²) equals CFG938's tangential tether stress u²/2K. That is
    why the worst value repeats CFG938's 1.54e-5.

### (f) Class-A limit (cosmic shear)
- **Field-supplied phantom is a net source.** Inside NGC 3198's r_ta it is 12.8 / 14.1 × the catchment's whole mass (6.364 M_b).
  Class A's source is zero-sum (CFG649 R-A2).
  - The field sectors fail g2, and g1 or g3 as well.
  - O2a-2 keeps g1 (the dust feels Newton only), but lensing then sees no phantom.
- **O2c** fails g1 and g2 (CFG941 R1).
- **O2d2** has g1 and g3. g2 needs a selection rule, and with the catchment rule added it *is* class A, i.e. option 3.

**(f) FAILS for all eight. The T1x/T2x/NC1x shear passes do not transfer to any option-2 construction.**

### (g) Excess family and below-law systems (reported)
- **Excess family.** Under Newtonian addition the excess facts need dust fractions f = 10^Δ − 1 (canonical): dwarfs F0 1.35,
  red lenses F1 0.34, clusters F5 0.75, against blue lenses F2 0.008, small SPARC F3 0.15 and large SPARC F4 0.002.
  - Option 2 has dust everywhere, so it **re-describes** the excess family by class-dependent dust fractions from 0.002 to 1.35,
    with no derived selector that keeps late-type rotators nearly dust-free.
  - Under alt, F2 and F4 are slightly negative, which dust cannot give.
- **Below-law systems.**
  - Field-supplied branches (O2a-*) act on every baryonic system. Their TDG prediction is CFG936's route (iii): −0.381 ± 0.110 dex
    (z −3.48) canonical, −0.414 ± 0.109 (z −3.79) alt. DF4 lies below Newton, which no EFE reaches. **FAILS.**
  - In O2a-3, host dust raises the external field by only ×1.36–2.80 at 50–250 kpc. The TDGs need ×29–36.
  - Dust-supplied branches (O2b, O2c, O2d2) give zero dust → Newton, CFG936's route (i): EXPLAINS, with the same caveat that the
    zero-supply label is not derived.

## 5. Classes (frozen rules)

| construction | (a) | (b) | (c) | (d) | (e) | (f) | (g) | class |
|---|---|---|---|---|---|---|---|---|
| O2a-1 literal | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAILS | **NOT VIABLE** |
| O2a-2 baryon-only | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAILS | **NOT VIABLE** |
| O2a-3 universal | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAILS | **NOT VIABLE** |
| O2a-G gated | FAIL | PASS | FAIL | FAIL (ghost) | FAIL | FAIL | FAILS | **NOT VIABLE** |
| O2b dust-excess source | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | RE-DESCRIBES | **NOT VIABLE** |
| O2c c₂ ≠ 1 tether | FAIL | PASS (c₂ ≤ 3.5e-3 only) | FAIL (hover) | PASS | FAIL | FAIL | RE-DESCRIBES | **NOT VIABLE** |
| O2d1 Galilean field | FAIL (L-G) | PASS (c₁ ≥ 600 only) | PASS | PASS | FAIL | FAIL | not computed | **NOT VIABLE** |
| O2d2 dispersion dust | FAIL (no selection) | PASS | PASS | PASS | PASS | FAIL | RE-DESCRIBES | **NOT VIABLE** |

**Overall: NO-GO (theorem T-O2).** The nearest miss is O2d2. It fails only (a), because nothing selects the law, and (f). It is
"cold energy is the phantom, held by dispersion", i.e. not option 2. With a non-local supply rule it becomes option 3.

## 6. Plain statements

1. **Particle in disguise.** Option 2's cold energy is pressureless, universally coupled, self-gravitating dust. In every
   gravitational respect that is a cold collisionless matter species: CFG723's "particle in disguise", now without the tether
   that made S3 different. Option 2 adds no species beyond cold energy itself, but it makes cold energy indistinguishable from
   one. O2d2 is literally a cold-dust halo whose profile is the law's phantom.
2. **What option 2 would need.** At least one of the following:
   - a field sector with an EFE, costing satellites (2.7–3.7σ, conditional) and tidal dwarfs (3.5–3.8σ), plus failed growth,
     FRW well-posedness and lensing unless gated and disformally completed;
   - a tether that cancels the dust's self-gravity (CFG941);
   - a non-local supply (option 3).
3. **What is not claimed.**
   - That option 3 or any non-local construction fails.
   - That κ, a₀, Ω_c/Ω_b or L* are derived.
   - Any data verdict beyond the framework-native statements above.
   - Not "theory closed".

## 7. Controls and disclosures

**K: all pass.**
- K1: 2.2e-16 / 2.2e-16.
- K2: n = 0.694330 (CFG941) and dust n = 1 to 1e-12.
- K3: CL-AR Theorem 1 for three bodies with arbitrary pair potentials, plus the passive-charge corollary.
- K4: ℓ_min = 494.7 / 513.9 kpc (CL-AR 495 / 514); f_gen = 2.94 / 24.87 / 54.48%.
- K5: Gauss-flux boost 4.24850 = the analytic value (CFG925 K7: 4.249).
- K6: O2c(c₂ = 0) = 1.6445 / 1.8844 (CFG938 M3).

**MUTATE: all bite (exit 1 by design).**
- M1, sector off:
  - NGC 3198 deviation 0.8270 / 0.8413 = CFG938 M1;
  - BTFR limit 0;
  - n = 1;
  - EFE factor 1 to 2e-16.
- M2, double counting:
  - D-A dust with baryon-sourced X: 0.827 / 0.841. This equals the Newton deviation identically, since |g_law + u − g_law| = u.
  - D-A dust with universal X: 1.743 / 1.856 (= CFG941 M2b).
  - Multiplicity 2: 6.401 / 7.163 (= CFG941 M2a).
- M3, linearised X (ν̃ = 1): EFE factor 1 to 2e-16, deep BTFR limit 0.
- M4, external field → 0: EFE factor 1 to 2e-16.

**A1 (23e0a5765).**
- Items 1–5 are pre-result code fixes. Among them: K3's simplify replaced by expansion, after a first K attempt produced no output
  for 10 min and was stopped.
- Item 6 is post-result. In the first main run, numpy booleans made the class listing count two printed PASSes (O2a-G (b), O2c (b))
  as fails. No class and not the overall result changed. Kept: `cfg946_firstrun_npbool.*`.
- Item 7 adds O2d1's exponent at its fitted coupling to the printed text.
- K, MUTATE and main were then rerun from the final script (sha256 723f316e…). The diff to the first main run is only the
  amendment tag, timings, O2d1's text and the two corrected fail lists.

**Implementation choices (declared, not derived).**
- The D-A, D-F and D-U dust contents.
- Satellites' internal source is their baryons only; their own dust is ignored.
- The EFE factor is evaluated at the Plummer scale radius.
- Host D-F dust enters only O2a-3. O2b uses slaved settled dust for both satellite and host.
- The constant-ε EdS mapping is indicative, since ε depends on amplitude. The decisive statement is the required field y ≥ y_min
  against the upper bound y_max (δ = 1).
- O2a-2 uses a constant-ν̃ two-fluid matrix.
- Galileon example: cubic only.
- O2d2's second equilibrium is hydrostatic (Jeans); positivity of its distribution function is not checked.
- Slip estimators as CFG938. The minimal light coupling is conformal; the disformal best case is reported separately.

**Compute.** One process, ~5 s, peak RSS 0.15 GB, OMP_NUM_THREADS=1 and nice 10, beside NC2x. Nothing downloaded. No other lane's
file edited.
