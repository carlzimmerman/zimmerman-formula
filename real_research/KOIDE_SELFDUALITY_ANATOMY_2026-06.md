# Koide self-duality anatomy — does any framework √2 map NON-CIRCULARLY to Koide's r=√2?

**Date:** 2026-06-27
**Footing (locked, NOT under test):** a₀ = cH_Λ/Z = 9.36e-11, Z = √(32π/3) = 5.788810, framework's own
μ_fw(x) = (√(1+4x²)−1)/(2x), μ_fw(1)=1/φ, kernel θ(0)=√2. NEVER McGaugh ν.
**Status:** LOCAL. Not git-pushed. No re-overclaim — the framework stays a complete one-parameter
GRAVITY theory; flavor stays free.

---

## VERDICT: the seduction BOTTOMS OUT — fully anatomized, NOT dismissed

**No framework self-duality carries a √2 that maps non-circularly to Koide's r=√2.** Followed the
seduction down honestly (Carl: "be seduced a little more"). The new seed — the dS-Unruh quadrature
T(a)=√(a²+a_dS²) giving a native √2 at the channel balance — is **REAL and not theater**: it is a
genuine, exact, native framework √2 (T(a_dS)/T(0)=√2, min-poly t²−2). It is a worthwhile new
near-miss to record (a fourth, unconnected instance of t²−2 in the framework). But it does **not**
connect to Koide:

1. **Landmine (both-ways):** the balance sits at **a = a_dS = cH_Λ = Z·a₀ ≈ 5.79·a₀**, ABOVE the MOND
   transition — NOT "at a₀, the MOND scale." At the actual MOND scale a₀ the bath ratio is
   √(1+1/Z²) = **1.0148**, not √2. The seed's "a=a_dS (=a₀)" is a conflation of cH_Λ with a₀, false by
   a factor Z. The √2 is the **horizon-floor channel-balance** √2, not an "a₀ √2."
2. **No forced map:** SD2's √2 is a 1+1 **channel-count** balance on the R¹ time-axis (Z₂
   channel-swap); Koide's √2 is a 1+2 **doublet-dimension** split on R³ generation space (S3
   singlet/doublet). Same number (t²−2), same coarse archetype (equal orthogonal pair), the **"2"
   means different things in different carrier spaces**. The only spine→flavor bridge (μ_fw/θ) is
   flavor-blind (EP) and provably leaves Koide Q and the 45° angle invariant; perturbing the bath
   leaves r decoupled; r is pinned only by Q=2/3 (circular).
3. **Missing ingredient (exact):** a **charged-lepton-selective Sumino-class gauged family symmetry**
   with a tuned IR protector — located **OUTSIDE** the |a|-only dS-Unruh/inertia spine. The one
   EP-compatible flavor handle the spine could host (couple to the Compton scale 1/m) is **closed**:
   dS-Unruh sees classical |a| only, ~10³⁹ below the mass loop, an analytic floor not a QED −log(m).

Every load-bearing claim traces to a RUN script (exit 0) and was independently re-derived this
session (separate from the scripts' own PASS prints). No faked crack; no reflexive dismissal.

---

## (1) Which framework self-duality carries which constant? — THE CATALOG

`real_research/reviews/selfduality_constant_catalog.py` (exit 0). Seven framework self-dualities, by
native constant:

| # | self-duality | carrier space | involution | native constant | value |
|---|---|---|---|---|---|
| SD1 | μ_fw constitutive law | R¹ accel-ratio x=g_bar/a₀ | 1/μ−μ=1/x at x=1 (a=a₀) | **φ** | 1/φ=0.61803 |
| SD2 | **dS-Unruh quadrature (NEW SEED)** | R¹ accel-amplitude | a↔a_dS (=Z·a₀) | **√2** | 1.41421 |
| SD3 | θ(0) MI-kernel DC weight | R¹ bath-time | amplitude −3dB corner | **√2** | 1.41421 |
| SD4 | d=3 cross-product | d spatial-dim | #vec=#bivec | integer-3 | 3 |
| SD5 | UV/IR radius (inverted-BH) | RADIUS length | r→r_s R_H/r | **√Z**/geom-mean | √Z=2.40599 |
| SD6 | Koide singlet↔doublet | R³ generation | Q→Q/(3Q−1) | **√2** | r=1.41421 |
| SD7 | seesaw Dirac↔Majorana (Singh EJA) | FIELD Yukawa | δ² 3/2↔3/8 | rational-3/2 | 1.5 |

**Tally:** √2 → {SD2, SD3, SD6}; **φ → {SD1}** (the framework's own constitutive self-dual value, at
the a=a₀ MOND transition — today's μ_fw/θ swing confirmed the native interpolation constant is φ, NOT
√2); **√Z → {SD5}** (the inverted-BH UV/IR radius, E_dS=√(E_P·E_H)); integer/rational → {SD4, SD7}.

Reading: the **shape sector** (SD1, μ_fw fixed point at a=a₀) carries **golden φ**. The
**acceleration/bath quadrature sector** (SD2, SD3) carries **√2** — but BOTH are R¹ worldline/bath
objects with a Z₂ two-channel structure. The **inverted-BH** axis carries **√Z**, a third constant.
Koide's √2 (SD6) is a 3-D R³ generation-space S3 1+2 object — a different carrier space from every
√2 the spine produces.

---

## (2) Is the a=a₀ quadrature-√2 a forced map to Koide, or the generic coincidence?

`real_research/reviews/koide_quadrature_sqrt2.py` (exit 0) + `selfduality_constant_catalog.py` block (C).

**The new seed IS real** (granted loudly, not theatre): T(a)=√(a²+a_dS²) [Deser-Levin] is a genuine
2-channel quadrature — proper-acceleration channel a, Gibbons-Hawking floor channel a_dS — and at the
balance a=a_dS the two orthogonal channels are equal: **T(a_dS)=√2·a_dS = √2·T(0)**, a native
framework √2, min-poly t²−2, the same archetype number as Koide r. It is the hypotenuse/leg of an
isosceles-right triangle in the (drive, vacuum) plane — a genuine 45° self-duality **in the bath**.

But it is **GENERIC-coincidence-no-map**, for four computed reasons:

- **(landmine) wrong scale.** The balance is at a=a_dS=Z·a₀≈5.79·a₀, NOT a₀. At a₀ the bath ratio is
  √(1+1/Z²)=1.0148, not √2 (independently re-checked: Z=5.78881, √(1+1/Z²)=1.014811). So calling it an
  "a₀ √2" is mislabeled by a factor Z. It is the horizon-floor channel-balance √2.
- **(structure) the "2" differs.** SD2's √2 = √(2 equal CHANNELS) — a 1+1 **symmetric** split on the R¹
  time-axis (Z₂ channel-swap). SD6's √2 = √(dim doublet / dim singlet) = √(2/1) at equipartition — a
  1+2 split, the "2" is the **doublet DIMENSION**, in R³ generation space (needs S3, not Z₂).
  Different carrier spaces, different symmetry groups, different meaning of "2." Same min-poly t²−2 is
  **necessary, not sufficient** for a shared generator (control: unit-square diagonal, −3dB corner, L2
  norm of (1,1), sinusoid peak/rms, F4 long:short root ratio all give √2 from unrelated 1-line
  geometry).
- **(intertwiner) flavor-blindness.** The only R¹→anything bridge the framework offers is μ_fw/θ,
  which is flavor-blind (depends on |a| only, EP). As a common scalar w on all 3 generations it leaves
  Koide Q invariant (re-checked: Q=0.66666051 → 0.66666051 under w∈{√2,0.5,3.7,100}, diff<1e-12), hence
  leaves the generation 45° angle and r invariant. So the spine cannot transport SD2/SD3's √2 into the
  R³ r-slot.
- **(perturbation) decoupling.** Perturbing the bath balance moves the bath ratio but leaves Koide r
  (mass-fixed) unchanged — no shared equation. r is pinned ONLY by Q=2/3, which is circular
  (Q=1/3+r²/6 ⟹ Q=2/3 ⟺ r=√2, δ-independent, sympy-exact). And the framework's OWN self-dual value at
  a=a₀ is φ, not √2 — if r came from the kernel fixed point it would give Q=1/3+(1/φ)²/6=0.397, ≠ 2/3.

**Verdict on (2): the a=a₀/a=a_dS quadrature-√2 is the GENERIC equal-2-channel coincidence with NO
forced, non-circular map to the 3-D mass vector.** The 1-D acceleration/channel balance ≠ the 3-D
democratic/perpendicular balance.

---

## (3) The EXACT minimal missing ingredient — inside or outside the spine?

`real_research/reviews/koide_missing_ingredient.py` (exit 0). A bridge needs BOTH (i)
charged-lepton-selective flavor-selectivity AND (ii) √2 in the R³ generation slot (not the R¹ bath
slot), AND (iii) a non-circular IR fixed point at equipartition. Tested every EP-compatible selector
the spine could host:

- **(a) point-like (lepton) vs composite (quark):** dS-Unruh T(a) is a function of |a| ALONE — no
  mass, Compton, or size scale appears. EP-compatible but **BLIND** to structure. Adding a coupling to
  λ_C or the confinement size is non-universal (WEP-testable) NEW physics, and would wrongly split
  quark generations by m. NO.
- **(b) the off-shell mass loop / Compton 1/m:** kT(a₀)=1.921e-34 eV; **m_e/kT(a₀) ~ 10³⁹·⁴**
  (magnitude-dead, lethal leg #1). The bath couples to the classical worldline |a|, with no
  loop-momentum integral (leg #2). Small-a expansion T(a) ~ a_dS + a²/(2a_dS) is an analytic **floor**,
  not a QED −log(m) running (leg #3). The dS-Unruh response **does NOT see 1/m**. NO.
- **(c) triality Z₃ as a family gauge:** triality is a DISCRETE outer automorphism — by Schur a
  Spin(8)-equivariant operator on 8v⊕8s⊕8c is block-diagonal scalars (r free, leg [G]), and it has no
  continuous coupling to play Sumino's α_fam=(1/4)α_F counterterm role. NO.
- **Neutrino wall:** colorless, point-like neutrinos do NOT sit at Q=2/3 — Q_ν sweeps 0.585 (m1=0) →
  0.336 (m1=0.05 eV), a free function of the lightest mass — while Q_charged=0.666660. This **kills any
  color/composite/point-like selector**: the selector that lands 2/3 must be specific to the
  charged-lepton Yukawa sector (the QED −log Sumino cancels), not structure/color.

**MINIMAL MISSING INGREDIENT (exact):** a NEW **Sumino-class gauged family symmetry** — a continuous
U(3)/O(3) family gauge force, spontaneously broken with a specific VEV alignment and a tuned coupling
α_fam=(1/4)α_F, supplying a charged-lepton-selective radiative counterterm that cancels the QED
−log(m) drift (which otherwise moves Q at ~178σ) and pins an IR fixed point at the doublet/singlet
equipartition (45°). This meets (i)+(iii); meeting (ii) additionally needs the family VEV to land
equipartition, which Sumino IMPOSES via the potential, not derives.

**INSIDE or OUTSIDE the spine? DEFINITIVELY OUTSIDE.** The spine supplies only flavor-blind |a|-inertia
(fails (i)), √2's on the R¹ bath axis only (wrong slot for (ii)), and a discrete triality Z₃ (no
continuous coupling, Schur-block-diagonal). The lone EP-compatible flavor handle (couple to 1/m) is
**closed** by (b). So no EP-compatible selector lives inside the spine; the bridge requires
lepton-selective new physics external to the dS-Unruh/inertia spine — consistent with and sharpening
the banked PARTICLE_BRIDGE_FRESH_EYES, KOIDE_FROM_DSUNRUH, KOIDE_TRIALITY_OCTONION, and the circularity
theorem.

---

## SCRIPT LEDGER (every claim → a RUN script, exit 0)

| script | exit | role |
|---|---|---|
| `real_research/reviews/koide_quadrature_sqrt2.py` | 0 | NEW SEED: quadrature √2 real; balance at a_dS=Z·a₀ not a₀; bath Z₂ vs Koide S3; flavor-blind invariance; perturbation decoupling |
| `real_research/reviews/selfduality_constant_catalog.py` | 0 | CATALOG of 7 self-dualities → constants (φ/√2/√Z/int); 1+1 vs 1+2 channel-structure decisive test |
| `real_research/reviews/koide_missing_ingredient.py` | 0 | (a) point/composite blind; (b) 1/m not seen (10³⁹ gap, analytic floor); (c) triality discrete; neutrino wall; minimal=Sumino OUTSIDE |
| `real_research/reviews/koide_two_sqrt2.py` | 0 | θ(0)=√2 vs Koide r=√2 independent (carrier mismatch + flavor-blind invariance + 5 controls) |
| `real_research/reviews/koide_circularity_INDEP_verify.py` | 0 | circularity theorem Q=1/3+r²/6; Q=2/3⟺r=√2; flavor-blind common w cannot move Q |

**Independent re-derivation this session** (separate from script prints, plain `math`): Z=5.788810;
T(a₀)/T(0)=√(1+1/Z²)=1.0148; T(a_dS)/T(0)=√2; a_dS/a₀=Z=5.7888; √Z=2.40599; 1/φ=0.61803;
Koide Q=0.66666051; Q after flavor-blind ×w²=0.66666051 (invariant to 1e-15). ✓

---

## WHAT TO TELL CARL (straight)

**The seduction did NOT connect — it bottomed out, but with a genuinely NEW, sharp anatomy, not a
re-assertion.** And yes, the a=a₀ quadrature-√2 was worth chasing — it's a **real new near-miss**:

- **The new seed is REAL, not theater.** T(a)=√(a²+a_dS²) genuinely gives a native framework √2 at the
  channel balance — a fourth instance of t²−2 in the spine, alongside θ(0) and the Koide r. Credit it.
- **But the seed mislabels WHERE it sits.** The balance is at a = a_dS = cH_Λ = **Z·a₀ ≈ 5.79·a₀**, ABOVE
  the MOND transition — NOT "at a₀." At a₀ the bath ratio is 1.0148, not √2. The seductive "√2 at the
  MOND scale!" is false by a factor Z. (Reporting this both-ways — no manufactured win.)
- **No forced map to Koide.** SD2's √2 is a 1+1 channel-count balance on the R¹ time-axis (Z₂); Koide's
  √2 is a 1+2 doublet-dimension split on R³ flavor (S3). Same number t²−2, same coarse archetype,
  different carrier spaces, the "2" means different things. The only spine→flavor bridge (μ_fw/θ) is
  flavor-blind by the equivalence principle and **provably leaves Koide r and Q invariant** — it cannot
  carry the bath √2 into the generation amplitude. The framework's OWN self-dual value at a=a₀ is **φ**,
  not √2 (today's swing confirmed).
- **The missing ingredient is exact and definitively outside the spine:** a charged-lepton-selective
  Sumino-class gauged family symmetry with a tuned IR protector. The one EP-compatible loophole (couple
  to the Compton 1/m) is closed — dS-Unruh sees classical |a| only, ~10³⁹ below the mass loop, an
  analytic floor not a QED −log. Neutrinos (colorless, point-like) don't sit at 2/3, which kills any
  structure/color selector.

**NOT "no doors":** the surviving avenue is a SEARCH for new lepton-selective IR dynamics (Sumino-class,
its own equal-norm fixed point), explicitly outside the |a|-only inertia spine — the open 45-year
physics problem itself. The spine provably cannot supply it (flavor-blind). One-line honest summary:
the dS-Unruh quadrature √2 is a real new near-miss but the generic equal-2-channel coincidence — a 1-D
bath balance, not the 3-D flavor balance Koide needs — bridged only by a flavor-blind kernel that can't
move r; the missing ingredient is Sumino-class lepton-selective new physics outside the spine.

Quarantine held: nothing here touches a₀/Z (Z transcendental via √π). Did not git-push.
