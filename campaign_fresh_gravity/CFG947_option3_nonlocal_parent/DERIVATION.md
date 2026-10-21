# CFG947 DERIVATION: option 3, a non-local causal parent of the class-A engine

Criteria `FROZEN_CRITERIA.md` (9c683a634, committed alone first). Amendment `AMENDMENT_A1_pre_result.md` (fad3a6b86,
pre-result, committed alone). Every load-bearing statement below has a sympy or numeric check in `cfg947.py`; check names are
in brackets. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle species. Not
"theory closed". Nothing here says the data favour the framework. K = 4πG.

**Overall class (frozen rule): NO-GO for exact parenthood.** No candidate is viable. Three structural statements, each passing
its check, show that the failure is generic to *every* parent whose non-relativistic (NR) limit is exactly the class-A engine:
- **T-M.** The engine's relocation rule E8 cannot be the NR limit of any covariantly conserved theory.
- **T-R.** The engine's resolution scale RMIN turns the law off for most isolated galaxies.
- **T-X.** The engine's phantom E4 carries the host external-field effect (EFE) that CFG478 excludes for satellites.

The engine-verbatim candidate N2-E is the only one to which the T1x / T2x / NC1x shear passes would transfer, and it fails (a),
(d), (f) and (h). Candidates that fix (f) are not the engine, so the shear results do not transfer to them. Approximate
parenthood is not excluded; it is not established either (§8).

---

## 1. The target (read from the code; criteria §0)

The class-A engine (CFG650 engine with M1 + M2 + M3 = T1x / T2x; CFG654 = native inputs, NC1x) has eleven NR equations, E1–E11.
They are listed in the criteria. In words:
- every particle feels −∇Φ;
- Φ is sourced by the particles plus a source S;
- S is
  - nonzero only on catchments (balls of r_ON around resolved peaks, r_ON ≥ RMIN = 0.78125 Mpc/h);
  - built from a phantom s_ph;
  - realised inside an edge (E7) as the deficit max(s_ph − s_c, 0);
  - paid for by a draw q·s_c on the rest of the catchment (zero-sum, q ≤ 1).

**Disclosed before any number.** E4, the phantom, is the pointwise QUMOND phantom of the *global* retained-baryon field (the PM
field of tab[code](1 + δ) or of the condensed deposit, over the whole box). It is *not* a per-structure own-baryon rule. It
therefore contains the baryonic EFE of every neighbour. The record's "own-baryon, no-EFE" wording (CFG941 §4; CFG888 Q1;
CFG478's material reading) is a galaxy-scale rule, not the engine's formula.

## 2. The chassis common to every candidate

  G_μν = (8πG/c⁴)(T^b + T^c + 𝒮)_μν.

**Geodesic matter.** Baryons and cold dust are geodesic (E1). The cold dust is CFG938's matter sector (comoving labels,
F = −mc²n) with *no* tether (no W, no χ, no λ, no τ-stiffness). Then the Bianchi identity forces ∇_μ𝒮^{μν} = 0 separately.

**NR content.** 𝒮 has a density ρ_s, a momentum density j_s and a stress Π_s, with:
- ∂ₜρ_s + ∇·j_s = 0;
- ∂ₜj_s + ∇·Π_s = −ρ_s∇Φ.

**Conservation by construction [T-Z].** Take J_s^μ = ∂_ν𝒬^{μν} with 𝒬 antisymmetric. Then ∂_μJ_s^μ ≡ 0; sympy confirms this
for six generic component functions. In the NR limit:
- ρ_s = −∇·𝒫 and j_s = ∂ₜ𝒫 + ∇×M satisfy continuity identically;
- a compact 𝒫 gives ∫ρ_s dV = 0 (sympy on a compact radial 𝒫).

**Causality.** Every inverse operator is □_ret⁻¹. The response to a source switched on at t₀ is H(t − t₀ − r/c)/(4πr), which is
zero before the light cone [d1].

**No action principle (declared cost).** For a non-local action ∫φKφ, the variation gives (K + Kᵀ)φ. With K = G_ret this is
G_ret + G_adv, which is time-symmetric. So retarded non-local equations are not Euler–Lagrange equations of any action (the
Deser–Woodard / Jordan point). The parents here are causal effective equations, with conservation imposed by the 2-form
construction.

MUTATE Mu2 shows the cost of the alternative. With ½(G_ret + G_adv), the response at t = t₀ − r/(2c), before the source
exists, is 1/(8πr): half the static value [Mu2]. The action version is acausal.

**Consequence for CFG678's contract.** CFG678's rule is "an action, not a recipe": a gate counts only if the behaviour follows
from varying one action. A retarded non-local parent therefore cannot score PASS on any CFG678 gate that needs an action. The
action form fails causality. Option 3 cannot meet the one-action rule and causality together.

## 3. Structural results (each with its check)

### 3.1 T-Z: zero-sum is forced by conservation [T-Z: PASS]

d/dt ∫ρ_s dV = −∮ j_s·dA. Two inputs:
- 𝒮 ≡ 0 on FRW, since no domain exists at δ = 0 (§5 (b));
- j_s has no flux through the boundary.

Hence ∫ρ_s = 0 for all time. Per-domain zero-sum holds exactly when no 𝒮 current crosses a domain boundary.

So class A's zero-sum is not an extra prescription. It is what covariant conservation demands of a source that relocates the
cold matter's active mass and has no mass of its own. A QUMOND phantom is not zero-sum because it is not a separately conserved,
matter-like sector.

- A growing class-A domain keeps \|∫ρ_s\|/M_ph = 0 exactly at every growth stage.
- Removing the draw (Mu3) creates 53.65 M_b of 𝒮 at switch-on (= 1/x for f_r = 0.1), for which continuity has no solution.

### 3.2 T-M: the engine's relocation rule is not conservable [T-M: PASS] (A1.1)

**Total momentum.** P_m + ∫j_s. Integrating continuity gives ∫j_s = Ḋ_s, with D_s = ∫xρ_s, the 𝒮 dipole (compact support).
Matter changes momentum at the rate F_ms = −∫ρ_m∇Φ_s, the force of 𝒮 on matter. The integrated 𝒮 momentum equation gives
d/dt ∫j_s = −∫ρ_s∇Φ_m = −F_ms (Newton's third law; the self-force of 𝒮 vanishes). Hence a prescribed source is conservable
only if

  D̈_s = −F_ms.

**Carried weights.** Let 𝒮 weights s_j be carried by matter elements at x_j. The identity

  D̈_s = Σ s_j ẍ_j + R,  R = Σ (s̈_j x_j + 2ṡ_j ẋ_j)

holds (sympy). With free-falling carriers, Σ s_j ẍ_j = Σ s_j g_m(x_j) + Σ s_j g_𝒮(x_j) = −F_ms + 0.

**Two consequences.**
1. **Constant weights conserve automatically,** even when F_ms ≠ 0. The matter's momentum change is carried by 𝒮's momentum Ḋ_s.
   Plummer toy: F_ms = −7.8e-4, −7.8e-3, −2.3e-2 (in units G = M = 1, X = 5) for ε = 0.01, 0.1, 0.3, and
   \|Σ s g_tot + F_ms\| ≤ 6.9e-18. The engine itself, which has no 𝒮 momentum, does not conserve matter momentum for
   asymmetric catchments (rate F_ms). This is the class-A form of CFG48's momentum obstruction.
2. **Relocation is the obstruction.** When the weights change (the phantom grows, the draw moves) in a non-concentric domain,
   R ≠ 0 and no solution exists.
   - E8's draw (q uniform over the shell's cold, two blobs with dipole fraction ε) gives exactly R = −ε(M̈_e X + 2Ṁ_e Ẋ).
   - N3's switch-on gives R = −(M_c ε/3)(X s̈ + 2Ẋṡ). The 1/3 is checked by a surface-integral quadrature, to 1e-12.
   - For the declared smooth histories (growth time = dynamical time; M_e/M_dom = M_c/M_dom = ½),
     max\|R\|/(M_dom g_ref) = π²ε/4 for E8 (0.025 / 0.247 / 0.740 at ε = 0.01 / 0.1 / 0.3) and π²ε/12 for N3.

**Reading.** No covariantly conserved parent reproduces E8 exactly in an asymmetric catchment.

A conservable class-A rule needs one of two things:
- **(i) a dipole-free relocation:** the draw's centroid tied to the phantom's at all times;
- **(ii) an independent 𝒮 dipole degree of freedom:** new initial data, which would reopen d2.

Neither is the engine.

### 3.3 T-E: the edge is forced [T-E: PASS]

**Argument.**
- Zero-sum means the enclosed gravitating mass at the domain boundary equals the particle mass M_ta.
- Positivity (ρ_tot ≥ 0) means the enclosed gravitating mass is non-decreasing.
- Hence M_law(< r) ≤ M_ta wherever the law holds.

The check then shows that the law's enclosed mass at turnaround exceeds the turnaround mass for every M_b:

| M_b (M⊙) | 1e7 | 1e8 | 1e9 | 1e10 | 1e11 | 1e12 | 1e13 | 1e14 | 1e15 |
|---|---|---|---|---|---|---|---|---|---|
| f_r (census) | 0.10 | 0.10 | 0.10 | 0.10 | 0.122 | 0.36 | 0.647 | 0.90 | 0.90 |
| M_law(< r_ON)/M_ta, canonical | 8.85 | 6.03 | 4.11 | 2.80 | 2.18 | 3.07 | 3.12 | 2.68 | 1.85 |
| same, alt | 9.72 | 6.63 | 4.52 | 3.08 | 2.39 | 3.38 | 3.42 | 2.94 | 2.02 |
| r_e / r_M (E7) | 54.1 | 54.1 | 54.1 | 54.1 | 44.6 | 15.4 | 8.8 | 6.4 | 6.4 |
| supply N = M_c/M_b | 53.6 | 53.6 | 53.6 | 53.6 | 44.1 | 14.9 | 8.3 | 6.0 | 6.0 |
| r_ON (Mpc, physical) | 0.07 | 0.15 | 0.32 | 0.69 | 1.39 | 2.08 | 3.68 | 7.11 | 15.3 |

The minimum ratio is 1.85, so the law must end at some r_e < r_ON in every option-3 parent. This holds on both footings and
for both kernels (the ν_mono rows equal the simple-kernel rows to the digits shown).

**E7 is the supply root of the RAR kernel.**
- For ν_RAR (= ν_mono at y < 2.54), M_ph(< r)/M_b = 1/(e^{r_M/r} − 1). Setting M_ph(< r_e) = M_c = M_b/x gives
  r_e = r_M/ln(1 + x), which is exactly E7's x_supply.
- Measured: q = M_ph(< r_e)/M_c = 1 + 4.8e-9 for ν_mono, the residue of its interpolation table.
- For the S2 simple kernel, q = 1 + x²/24 + … (1.0000143 at f_r = 0.1; up to 1.0011 for clusters). The cap then trims the
  phantom by ≈ 1.2e-5 inside the edge. This is why (a) fails on the simple kernel (§5).

**Supply against CFG803 (reported, no class weight).** CFG803's minimum supply is 3 (canonical) / 4 (alt) in its primary range
and 16 / 24 at all radii.
- Class A's census gives N = 53.6 (M_b ≲ 3e10) and 44.1 (1e11): both lines are met.
- At M_b ~ 1e12, N = 14.9: only the primary line is met.

### 3.4 T-R: RMIN switches the law off [T-R: PASS]

**Threshold.** Resolved means r_ON ≥ 0.78125 Mpc/h, i.e. M_ta ≥ 2.066e12 M⊙/h. With f_r = 0.10 this means M_b ≥ 4.815e10 M⊙,
on either footing.
- NGC 3198 (M_b = 4.720e10 at Υ = 0.61) has r_ON = 0.776 Mpc/h and is *not* resolved. This is marginal: 2% below in M_b, 0.7%
  in r_ON.
- 128 of 175 SPARC galaxies lie below the threshold (Υ = 0.61). This is robust.

**Consequence.** An isolated sub-threshold system has no catchment, hence no source. Its law is off: Newtonian baryons plus a
cold-particle halo that the engine does not tie to the law.

**The two ways out.**
- RMIN taken as physics fails (a) and (h) (§5).
- RMIN → 0 leaves no continuum limit for the engine's catchment rule. Every point mass is then a peak whose r_ON is its host's,
  so:
  - under M1 each star becomes its own host, and supply is shared out by a nearest-peak tessellation;
  - under connected components, all overlapping balls merge into one pool.

Either way the source depends on resolution. The T1x / T2x / NC1x runs fixed RMIN; a parent must adopt it to inherit them.

### 3.5 T-X: the EFE fork [T-X: PASS]

**Global QUMOND (E4).** For CFG882's dwarfs in a 6e10 M⊙ host, the static on-axis factor [g(g_bh + g_bs) − g(g_bh)]/g(g_bs) is
−0.102 to −0.730 dex over H1–H3 × 50 / 100 / 250 kpc, both footings and kernels. Canonical, simple kernel:

| | 50 kpc | 100 kpc | 250 kpc |
|---|---|---|---|
| H1 | −0.644 | −0.421 | −0.197 |
| H2 | −0.722 | −0.489 | −0.237 |
| H3 | −0.407 | −0.238 | −0.102 |

This equals CFG941's static EFE factor (K5) and CFG925's E2 form.

**Own-domain rule.** The factor is 0 by construction.

**Reading.** The two differ by far more than 1%. A parent reproducing E4 has the host EFE, which CFG478 excludes for cluster
satellites (force-with-EFE χ² 61–107/5, against the isolated phantom's 0.7/5) and which CFG925 R3 records as worsening the
dwarf excess. A parent without the EFE is not E4.

### 3.6 T-L: own-label phantoms are non-additive [T-L: PASS]

**Deep limit.** For co-spatial labels with fractions f and 1 − f, Σ√(a₀ g_i) gives a factor √f + √(1 − f). This is checked at
four f values; the run-1 sympy simplification defect is noted in §10.

**On NGC 3198** (canonical; the ν_mono numbers agree to 1e-3), max \|g/g_law − 1\| is:

| case | f = 0.01 | f = 0.1 | f = 0.3 | f = 0.5 | N = 2 | N = 10 | N = 100 equal labels |
|---|---|---|---|---|---|---|---|
| max \|g/g_law − 1\| | 0.086 | 0.240 | 0.349 | 0.375 | 0.375 | 1.96 | 8.18 |

**Reading.** First-turnaround labels are assigned in small progenitors (hierarchical collapse), so N1 without a merge rule gives
order-unity errors. With a 0.9 / 0.1 label split on SPARC, the rms is 0.1017 / 0.1061 at Υ 0.49 / 0.44 (TENSION). N1 needs
the merge rule M-R.

### 3.7 T-N3: domains are forced [T-N3: PASS]

**Setup.** A domain-free gate placed where Δ_enc falls from Δ_ta to Δ_lo puts the compensating charge −Q = −(M_ph − M_c) in a
transition shell between r_ON and r_out.

**Result.** The minimum total density there is negative in units of ρ̄_m:

| gate | NGC 3198 | dwarf | MW | group | cluster |
|---|---|---|---|---|---|
| Δ_lo = 2 (graded; r_out = 2.21 r_ON) | −8.4 | −69 | −7.6 | −16 | −10 |
| Δ_lo = 1.1 (broad; r_out = 4.77 r_ON) | −6.9 | −60 | −6.3 | −14 | −8.4 |

The broad gate fails even where the cold inside it would cover Q in total (Q/available = 0.16–1.04). The gate's shape is set
by Δ_enc, not by where the supply lies.

**Reading.** Positivity therefore needs the edge at the supply root: a per-domain integral, i.e. a domain.

### 3.8 T-F: no hover [T-F: PASS]

**Monopole order.**
- Stars and cold dust are geodesic.
- 𝒮 is conserved and carried by free-falling matter, so it obeys the weak equivalence principle at monopole order.

So a satellite's stars, cold matter and own phantom fall together: Δa/g_host = 0.

**Retardation.** For Lorentz-covariant □_ret⁻¹, a uniformly moving source's field is the boosted static field, centred on its
present position, so there is no O(v/c) lag. The residue is bounded by (g_ph(a)/g_host)·max(v²/c², g_host a/c²) ≤ 1.2e-6 on
H1–H3 × 3 radii × 2 footings.

**Why theorem D-T does not apply.** D-T concerns an always-on *tether*: a force on the medium that depends on the total
tethered field, i.e. a modified passive response. Class-A-type parents leave the passive response universal and modify only the
active source. MUTATE Mu1 puts the local tether back and recovers D-T in full:
- growth n = 0.69433;
- Δa/g_host = 1.017–1.107;
- linear-regime C₁C₂ coefficient (1 − c₂) = 0, against K/(2k²) with 𝒮 = 0.

**Found, not sought.** Inside an edge where ρ_c < ρ_ph, the deficit rule pins the source at ρ_ph. Cold perturbations there
therefore source no gravity (they still feel all of it). Where ρ_c > ρ_ph the clip leaves them Newtonian, as CFG888 states for
class-A clumps. This is a feature of the class-A rule, not a free-fall violation.

## 4. Candidates (criteria §2)

| id | domains | phantom | zero-sum / edge | non-variational parts |
|---|---|---|---|---|
| N1 | first-turnaround labels (rule β, latched, fractional; peaks at L*), optional merge rule M-R | own retained baryons of the label set | E6–E8 on labelled cold | latch, M-R |
| N2-E | balls of r_ON about minima of retarded ψ, r_ON ≥ RMIN, M1 partition | global retained field (E4) | E6–E10 verbatim | domain rule (instantaneous) |
| N2-B | watershed basins of ψ smoothed at L* (24 pc), no RMIN | own retained baryons of the basin | E6–E8 | basin rule |
| N3 | none (smooth gate of retarded scalars) | global retained field, mean removed | divergence form, gate transition | none beyond retardation |

**Kernels and auxiliaries.** All auxiliary potentials (ψ, χ_D, Φ_D) obey □_ret X = source with zero homogeneous part. Written
in localized form, with auxiliary fields in a local action, they would carry homogeneous solutions. Granting those as
independent data would require checking their kinetic signs, as in the RR / RT experience. This lane does not grant them; d2
counts zero independent data.

## 5. Tests (a)–(h)

### (a) Static law (NGC 3198, 43 radii, Υ = 0.61; deep points y = 1e-2, 1e-3)

Max \|g/g_law − 1\| under three cold profiles:

| candidate | P-S simple | P-S ν_mono | P-I | P-X | deep (simple / ν_mono) | grade |
|---|---|---|---|---|---|---|
| N1, N2-B | 1.19e-5 (can) / 1.21e-5 (alt) | 3.96e-9 / 4.03e-9 | 2.2e-16 | 0.83 / 0.84 | 1.3e-5 / 4.3e-9 | **FAIL** (simple kernel) |
| N2-E | 0.83 / 0.84 (no source: not resolved) | 0.83 / 0.84 | 2.2e-16 (accidental) | 0.83 / 0.84 | 0.90–0.97 | **FAIL** |
| N3 | 2.2e-16 | 2.2e-16 | 2.2e-16 | 2.2e-16 | 0 | **PASS** |

The edge is r_e = 454 kpc (canonical) / 413 kpc (alt), and every point lies inside it.

**What each failure means.**
- **N1, N2-B: the S2 simple kernel only.** E7 is the RAR kernel's supply root (§3.3). For the simple kernel q = 1 + 1.4e-5, so
  the cap trims the phantom uniformly by that fraction. With E7 replaced by each kernel's own supply root, P-S is exact to
  2.2e-16 (diagnostic, not a grade). With the engine's own kernel (ν_mono) the line passes.
- **N2-E: RMIN** (§3.4). NGC 3198 is marginally unresolved, so it gets no source. P-I passes only because the cold particles
  happen to sit where the law needs them; nothing in the parent produces that.
- **N1 also needs M-R** (§3.6).
- **P-X** (ρ_c = 2ρ_ph) shows that condition C-ρ (ρ_c ≤ ρ_ph) bites: class A exceeds the law wherever the cold particles
  outnumber the phantom.
- **N3** passes because inside its gate it replaces the cold's active mass by the phantom whatever ρ_c is. It pays for this in
  (d3).

**What (a) does and does not show.** As the criteria warned, inside the edge with ρ_c ≤ ρ_ph a class-A source *is* the law's
deficit. So (a) tests the edge, the cap, the kernel, RMIN and the labels, not physics beyond that.

**Asymptotics.** At y = 1e-2 and 1e-3 the law gives V⁴/(G M_b a₀) = 1.105 and 1.032. Beyond r_e the curve falls, because zero-sum
forces it (§3.3).

### (b) FRW: PASS for all
- Dust: ρ = m/a³, p = 0, isotropic (sympy).
- 𝒮 ≡ 0 because:
  - Δ_ta(z) ≥ 5.57 > 1 + 3ε, so no domain exists at δ = 0 and λ₂ = 0 < τ − ε;
  - labels are unset;
  - per-domain fields are unsourced;
  - N3's mean-removed field vanishes.

### (c) Growth: PASS for all
- 𝒮 ≡ 0 in the linear regime, so the dust exponent is n = 1.000000000000.
- The top-hat mean density rises monotonically to 9π²/16 = 5.5517 at turnaround (δ_lin = 1.0624). The gate opens only at
  turnaround.
- By construction; compare Mu1's 0.69433 for the local tether.

### (d) Causality and well-posedness: FAIL for all

| item | N1 | N2-E | N2-B | N3 |
|---|---|---|---|---|
| d1 retarded support | PASS | PASS | PASS | PASS |
| d2 no ghost (0 independent data; real roots) | PASS | PASS | PASS | PASS |
| d3 total-source positivity | PASS (cap) | PASS | PASS (cap) | **FAIL** (−7.6 … −69 ρ̄_m) |
| d4 Hadamard toy | PASS (0) | **FAIL** (r_ON jumps 20.6%) | **FAIL** (edge jumps 41%) | PASS (0) |
| d5 identities | PASS | PASS | PASS | PASS |
| d5 relocation (T-M) | **FAIL** | **FAIL** | **FAIL** | **FAIL** |

**d2.** The two-component Jeans determinant with the class-A linear response has positive kinetic coefficients:
- inside an edge, a_c = 0 (cold does not source), giving roots c_c²k² and c_b²k² − K a_b ρ_b;
- in shells, a_c = 1 − q.

Roots are real and ≥ −K(a_bρ_b + a_cρ_c) at k = 0, 1, 10, 1e3, with no large-k instability.

**d3.** Positivity holds for N1, N2-B and N2-E by the cap: (1 − q_eff) ≥ 0. It is by construction, and Mu5 shows what happens
without it.

**d4.**
- N2-E: the largest-R rule makes r_ON jump by 1 − 2^{−1/3} when the second peak enters at d = R₁₂.
- N2-B: the minima of ψ for two L*-smoothed masses merge at d = 2.7375 L*; the merged domain's edge jumps by √2 − 1.
- N1: latched labels (rule β) do not change.
- N3: the gate's outer radius is continuous.

### (e) Slip: PASS for all

| | worst value |
|---|---|
| overall | 1.63e-5 (alt cluster) — the cold's own isothermal pressure in P-I, the same for every candidate |
| 𝒮's own isotropic stress, P-S | 1.30e-5 (N1, N2) / 1.42e-5 (N3) |

All are within the 1.9e-5 line. MW disc 2.5e-7, group 8.3e-7 (s_847, canonical).

### (f) Satellites
- **f1.** Δa/g_host = 0 (+ ≤ 1.2e-6) for every candidate: PASS.
- **f2.**
  - N1 and N2-B: 0 dex, PASS.
  - N2-E and N3: −0.10 to −0.73 dex, FAIL.
- **(f): N1 PASS, N2-B PASS, N2-E FAIL, N3 FAIL.**
- **Reported, no class weight: N2-B's basin cap.** A satellite basin is truncated near its Jacobi radius. With the P-S profile
  (supply beyond r_e) it retains only 0–16% of its phantom (H3 at 50 / 100 kpc: r_J 5.3 / 8.6 kpc < r_e 9.3 kpc, so supply is
  0). Under P-I no supply is needed. N2-B's no-EFE pass therefore depends on the cold profile.

### (g) Class-A limit (criteria E1–E11)

| | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 | E9 | E10 | E11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N1 | R | R | **D** labels, no RMIN | **D** own-domain | R | R | R | R | R (M2 = latch) | R | disc. |
| N2-E | R | R | R | R | R | R | R | R | R | R | disc. |
| N2-B | R | R | **D** basins, no RMIN | **D** own-domain | R | R | R | R | R | R | disc. |
| N3 | R | **D** | **D** no domains | R | R (in s) | **D** no clip | **D** no edge | **D** ∇s compensation | **D** | R | disc. |

(R = reproduced; D = differs; disc. = discretisation.)

- N2-E: PASS, by construction.
- N1, N2-B, N3: FAIL. The differences are unquantified, so transfer is not established.
- N2-E is the engine written as a field theory. T-M shows that it is not conservable (d5).

### (h) CFG653's constraints

| | h1 SPARC rms (can / alt) | h2 binaries | h3 satellites (CFG478) | (h) |
|---|---|---|---|---|
| N1 | 0.10033 / 0.09910 (0 points beyond any edge) | PASS / TENSION | PASS | CONDITIONAL (M-R) |
| N2-B | 0.10033 / 0.09910 | PASS / TENSION | PASS | PASS |
| N3 | 0.10033 / 0.09910 | PASS / TENSION | FAIL | FAIL |
| N2-E | 0.2566 @ Υ 0.82 / 0.2619 @ 0.77 (1811 / 1820 of 3389 points in unresolved galaxies) | PASS / TENSION | FAIL | FAIL |

**h2.** Binaries form in situ inside their host's domain, so every candidate gives them the host's QUMOND EFE. CFG653's
local-EFE recovery (1.179, +1.3σ / 1.244, +2.3σ) applies. This differs from the sealed DR4 prediction of exactly Newtonian
(context, as CFG653 noted). A Newtonian binary would score z = −1.36 / −1.51.

**h4.** Domain supports are ≤ r_ON ≪ l_dS; PASS for all.

## 6. How this differs from CFG653, and where it fails the same way

**CFG653's filter** is a high-pass in *scale* on the total field. Its window is empty because a non-harmonic host leaks as
(L/D)², while the satellite's own field must pass out to r_bg.

**Option 3's domains separate by membership** (labels or basins), not by scale. An own-domain phantom has exactly zero host EFE.
That is how N1 and N2-B escape CFG653's satellite failure (f2 0 dex; CFG478 0.7/5).

| CFG653 issue | option 3 |
|---|---|
| SPARC | the zero-sum compensation sits at r_e = 6–54 r_M, far beyond SPARC radii, so the rms equals the local law (CFG653's C1 put its scale at r_M and failed) |
| zero monopole, curve overshoots below Newton (finding 2) | the cap q ≤ 1 keeps the enclosed gravitating mass ≥ M_b; Mu5 removes the cap and finds ρ_tot = −ρ_c |
| binaries | the same as CFG653's L ≥ 30 kpc candidates (QUMOND EFE): not escaped |
| merger discontinuity (c3) | N2's domain rules jump (20.6%, 41%), the same problem; N1's latched labels avoid it |
| static causality (c4) | supports ≤ r_ON: PASS |

**Where option 3 fails exactly as CFG653 and CFG478 do.** N2-E and N3 use the global (scale-free) QUMOND field, so they carry the
EFE: −0.10 to −0.73 dex.

## 7. Classes (frozen rule, criteria §6)

| | a | b | c | d | e | f | g | h | class |
|---|---|---|---|---|---|---|---|---|---|
| N1 | FAIL | PASS | PASS | FAIL | PASS | PASS | FAIL | CONDITIONAL | **NOT VIABLE** |
| N2-E | FAIL | PASS | PASS | FAIL | PASS | FAIL | PASS | FAIL | **NOT VIABLE** |
| N2-B | FAIL | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | **NOT VIABLE** |
| N3 | PASS | PASS | PASS | FAIL | PASS | FAIL | FAIL | FAIL | **NOT VIABLE** |

**Overall: NO-GO.** Every candidate is NOT VIABLE, and T-M, T-R and T-X pass their checks. Each concerns the engine's own
equations, so each binds every parent whose NR limit is exactly the engine:

| statement | engine equation | what it does to an exact parent |
|---|---|---|
| T-M | E8 | an exact parent is not covariantly conserved |
| T-R | E3 | an exact parent has the law off for isolated systems below 4.8e10 M⊙ of baryons (128 / 175 SPARC galaxies), failing (a) and (h1) |
| T-X | E4 | an exact parent carries the satellite EFE that CFG478 excludes, failing (f2) |

The T1x / T2x / NC1x shear passes therefore transfer to no parent tested here. They remain results of the class-A engine.

## 8. What is not excluded, what is open, and what is not claimed

**Approximate parenthood is not excluded; it is not established.** The nearest candidate is N1. Its failures are of three kinds:
- **(a)** the S2 simple kernel through E7 (it passes with ν_mono, the engine's kernel);
- **(d)** d5, through E8's relocation;
- **(g)** by design.

A version with the merge rule M-R, a dipole-free draw (§3.2 (i)) and the kernel's own supply root would be "a non-local theory,
not class A's parent", at three costs:
- a non-variational latch;
- M-R;
- no action principle.

This lane has not built or tested that version. Building it would be post-hoc design. Its shear performance is unknown and would
need its own PM engine (label domains, own-domain phantoms, dipole-free draw) and a 1024³ run.

**Not claimed:**
- that any candidate is viable;
- that κ, a₀, Ω_c/Ω_b, L* or RMIN is derived;
- any data verdict beyond the framework-native statements above;
- "theory closed".

## 9. Controls and MUTATE

**K (all PASS; exit 0).**

| id | result | target |
|---|---|---|
| K1 | CFG938's reduced EL on NGC 3198: 2.22e-16 / 2.22e-16 | 2.2e-16 |
| K2 | CFG941 exponents 0.609545 / 0.694330 / 1.000000000000 | 0.60954 / 0.69433 / 1 |
| K3 | SPARC local law 0.10033 @ 0.61 / 0.09910 @ 0.57; Newton 0.27548 | 0.1003 / 0.0991; 0.2755 |
| K4 | CFG938 worst s_847 1.5398e-5 | 1.5398e-5 |
| K5 | CFG941 tethered hover 1.0167–1.1067; EFE −0.728 to −0.102 dex | 1.017–1.107; −0.73 to −0.10 |

**MUTATE (all bite; exit 1 by design).**

| tooth | result |
|---|---|
| Mu1 | local tether gives n = 0.69433, hover ≥ 1.0167, linear C₁C₂ coefficient 0 |
| Mu2 | time-symmetric kernel gives a precursor of ½ |
| Mu3 | no zero-sum creates 53.65 M_b of 𝒮 |
| Mu4 | global field gives an EFE up to 0.730 dex |
| Mu5 | uncapped starved catchment gives q = 2.0000 and ρ_tot/ρ_c = −1 |

## 10. Disclosures

- **A1 (pre-result, fad3a6b86).** It corrected T-M's falsifier: F_ms ≠ 0 is consistent with conservation for constant weights,
  and the obstruction is the relocation term R. It also fixed implementation details: Mu5's starved catchment, N3's gate, the
  d4 metrics, the P-S shell profile, units, and the f1 bound.
- **Implementation choices made in code before the first run** (not frozen):
  - T-M's smooth histories, M_e ∝ (1 − cos πt/t_g) and s ∝ (1 − cos πt/t_s);
  - N2-B's toy domain mass, 1e9 M⊙;
  - N2-E's toy peaks, 2 × M_ta,thr each;
  - non-retained baryons left out of the static profiles;
  - the N2-B cap model (satellite cold in a P-S shell truncated at r_J).
- **Run 1.** The first main run printed T-L as FAIL. The cause was that sympy returned √f − f√(1/(1 − f)) + √(1/(1 − f)) and
  could not reduce it to √f + √(1 − f) without knowing 0 < f < 1. The check now evaluates the identity at f = 0.01, 0.1, 0.3,
  0.5. No number or class changed (`cfg947_firstrun_TLcheck.out` is kept; its diff with `cfg947.out` is that one line).
- **Final edit.** The d5 relocation flag, previously typed in by hand, is now derived from the computed T-M values. K, MUTATE and
  main were rerun from the final script (sha256 48fa85c8…). Outputs are identical apart from runtimes.
- **Marginality.** NGC 3198 sits 2% below the RMIN threshold in M_b. N2-E's (a) on NGC 3198 alone is therefore fragile. Its (h1)
  failure (128 of 175 galaxies unresolved; rms 0.257 / 0.262) is not.
- **Inherited and approximate inputs.**
  - The engine's M_ta uses an inherited 0.315 × 2.775e11, which places r_ON and the census; the law inside r_e does not depend
    on it.
  - The census f_ret is the engine's empirical table.
  - CFG847's systems are point masses.
- **Compute.** One process; peak RSS 0.18 GB; about 5 s per stage; nice 10, OMP_NUM_THREADS = 1. Run beside NC2x. Nothing
  downloaded. No other lane's file touched.
