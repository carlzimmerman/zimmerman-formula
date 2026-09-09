# L37 — which density is in `a0 = κ c √(G ρ)`? The fork, decided at recombination and BBN

*Independent lane, 2026-09-08. Script: `L37_recombination_footing.py`; transcript
`L37_recombination_footing.out`. 35 checks, 10 FAIL — every FAIL is a designed fork outcome and
is labelled below. Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²) and both kernels (ν_RAR and
Milgrom's simple ν) carried through every number. Not committed.*

---

## The one-paragraph answer

**The canonical footing (ρ = ρ_Λ, a₀ constant) survives; the rival footing (ρ = ρ_tot,
a₀ ∝ cH(z)) does not.** But the brief's premise — that the CMB "sits right AT the MOND
transition" with g/a₀ ≈ 2.3 — **does not survive contact with a proper gradient**. Computed as
|∇Φ| = (k/a)Φ with a transfer-function potential, g/a₀ at recombination is **4.0–9.0 per mode
across the entire subhorizon Planck range and 15.6 for the point rms**, on the canonical footing.
The value 2.3 requires λ in place of k (a factor 2π) *and* a mode at l ≈ 20–40, which is 2–3×
**outside the horizon at last scattering**, where the quasi-static MOND limit is not defined at
all. This is numerically the same claim the repository already made and retracted on 2026-06-06
(`real_research/A0Z_OPEN_DOORS_AND_LENSING_FORECAST_2026-06-06.md` §1). This lane reproduces the
retraction independently and adds the reason: the missing 2π and a hand-set Φ.

---

## 1. Controls (all PASS)

| control | computed | reference | line |
|---|---|---|---|
| matter–radiation equality z_eq | 3402 | Planck 3387 ± 21 | C0a |
| sound horizon at drag | 147.10 Mpc | Planck 147.09 ± 0.26 | C0b |
| acoustic angular scale 100θ\* | 1.03959 | Planck 1.04109 ± 0.00031 | C0c |
| the brief's H(z)/H₀ table | 3.762 / 2.354e4 / 1.536e15 | brief 3.769 / 2.358e4 / 1.538e15 | C0d |
| ν → 1 at g/a₀ = 1e8 (both kernels) | 1.00000000 | Newtonian | C1a |
| ν√y → 1 at g/a₀ = 1e-8 (both kernels) | 1.000050 | deep MOND | C1b |
| kernel reproduces BTFR v⁴ = GMa₀ | 1.0041 / 1.0037 | 1 | C1c |
| Sachs–Wolfe normalisation Φ/3 at l = 10 | 9.79e-6 | observed ΔT/T ≈ 1.1e-5 | S2l |

The brief's own estimator is also reproduced exactly as a control on the premise: g = 2.138e-10,
g/a₀ = 2.284 (S2c). The a₀ table is reproduced to 3% on both footings and both readings (S1a).

**Incidental finding (S1b):** the repository's two mandated a₀ footings differ by
1.2048 ≈ 1/√Ω_Λ. The "both footings" pair *is* the ρ_Λ-vs-ρ_tot fork, evaluated today.

---

## 2. The estimator fork — three answers, six decades apart (S2)

The argument of the interpolating function is not a matter of taste; it is fixed by which arm of
the MI/MG fork the theory is on.

| reading | estimator | value at z = 1100 | g/a₀ (canonical) |
|---|---|---|---|
| **modified gravity** (operative arm since 2026-08-08) | \|∇Φ\| = (k/a)Φ, transfer-function Φ | 3.9e-10 … 8.4e-10 per mode; rms 1.46e-9 | **4.0–9.0 per mode; 15.6 rms** |
| **modified inertia** (closed arm, 21σ) | a_ac = c_s²/r_s(phys) — the fluid's own acceleration, pressure-dominated | 7.40e-6 | **7.9e4** |
| the brief's | Φ c²/λ_phys, Φ hand-set to 1e-5 | 2.14e-10 | 2.28 |

The MI row is what `real_research/reviews/mi_cmb_a0_horizon_2026.py` already uses. It is the right
estimator for that arm and the wrong one for the operative arm; this lane computes both rather
than choosing. The brief's estimator is not a third physical reading — it is the MG estimator with
the 2π of |∇| dropped and a hand-set Φ (the factor between them is 3.9× = 2π × 0.63).

Comoving Hubble radius at z = 1100 is 208 Mpc → **l_H = 67**. Every multipole below that is
superhorizon at last scattering. g/a₀ falls below 2.4 only at l ≲ 40.

Against the literature: Sanders (astro-ph/0509532) quotes g/a₀ ≈ 20; the point rms here is 13–16,
agreement to a factor 1.3. Stated as agreement in order and conclusion, **not** as reproduction —
the 40% gap is quoted, not hidden. Stated systematic on Φ at z = 1100: the (3/5) matter-era factor
is used while ρ_r/ρ_m = 0.33 still, so treat Δ_Φ as ±30%, moving the per-mode range to 3–12. That
reaches neither 2.3 nor 20.

---

## 3. Fractional shifts vs Planck's precision — the table the brief asked for

Method: in AQUAL the same source yields g = ν(g_N/a₀)g_N, so Φ → ν(k)Φ and C_l → ν(k_l)²C_l. A
scale-*independent* boost is exactly degenerate with A_s; only the scale dependence bites. Honest
error on every entry: **factor ~3** (linear response applied to a driven oscillator).

| observable | Planck precision | **canonical** (canon / alt a₀) | **rival** (canon / alt a₀) |
|---|---|---|---|
| sound horizon r_drag | 0.18% | 0.00% / 0.00% ✔ | 0.00% / 0.00% ✔ |
| acoustic scale 100θ\* | 0.030% | 0.00% / 0.00% ✔ | 0.00% / 0.00% ✔ |
| peak-1 amplitude (absorbed by A_s) | 1.4% | +12.8% / +17.0% (n/a) | +297 650% / +358 035% (n/a) |
| odd/even peak ratio → Ω_b h² | 0.67% | **+1.84% / +2.22%** ✘ | **+11.4% / +11.5%** ✘ |
| 3rd/1st peak ratio → Ω_c h² | 1.0% | **−1.33% / −1.59%** ✘ | **−7.52% / −7.52%** ✘ |
| damping tail l≈2200 rel. peak 1 | 1.5% per band | **+4.46% / +5.28%** ✘ | **+24.6% / +24.6%** ✘ |
| effective Δn_s, l ≥ 220 (ν_RAR) | σ(n_s) = 0.0042 | 0.0215 / 0.0256 = **5.1σ / 6.1σ** | 0.1148 / 0.1149 = **27σ** |
| effective Δn_s, l ≥ l_H (ν_RAR) | σ(n_s) = 0.0042 | −0.0226 / −0.0262 = 5.4σ / 6.2σ | −0.0983 = 23σ |

Kernel dependence is negligible: ν_simple gives 5.2σ/6.0σ (canonical) and 27σ (rival). In the
rival case the two kernels agree to 5 digits, because both reduce to ν → 1/√y in deep MOND.

**r_s and θ\* are untouched on both footings**, because a₀ does not appear in the Friedmann
equation in any relativistic MOND completion (see §5). That is the single most important structural
fact in this lane: the background is a₀-blind, so this whole question lives entirely in the
perturbation sector.

### How to read the canonical row — it is *not* an exclusion

S3a FAILs (5.1–6.1σ) and the script prints the caveat inline. Three things shrink it, all stated
because the lane must not manufacture a kill:

1. only A_s and n_s are marginalised. A real fit also moves Ω_b h², Ω_c h² and H₀, which absorb a
   smooth few-percent scale-dependent boost far better than a two-parameter fit;
2. factor ~3 estimator error either way;
3. **§5**: the relativistic completion that actually fits Planck does not implement AQUAL at
   cosmological scales, so this boost is not what the theory does.

What S3a *does* establish, and this is the useful part: **"g ≫ a₀ at recombination" is not by
itself a sufficient defence.** A residual boost of a few percent that *varies across the peaks* is
at the edge of Planck's reach. The canonical footing's safety comes from the completion's
structure, not from the size of g/a₀. That is a sharpening of the June-2026 retraction, not a
reversal of it.

---

## 4. BBN (S5) — and the result most against this lane's interest

| epoch | z | canonical g/a₀ | rival g/a₀ | rival boost ν |
|---|---|---|---|---|
| n/p freeze-out, T = 0.8 MeV | 3.41e9 | 1.19e13 | 1.07e-4 | 97 |
| D bottleneck, T = 0.094 MeV | 4.00e8 | 1.64e11 | 1.07e-4 | 97 |
| the brief's z = 4e8 | 4e8 | 1.64e11 | 1.07e-4 | 97 |

g is maximal at the horizon scale (superhorizon g ∝ k → 0; subhorizon Φ decays as k⁻²), so the row
bounds *every* mode.

**Structural finding (S5a2).** On the rival footing the ratio at horizon crossing is
**epoch-independent to machine precision**: g_hc/a₀ = c H₀ Φ_hc / a₀(0) = 1.068e-4, identical at
all three epochs, because g_hc = cHΦ and a₀ = a₀(0)E(z) both scale as H. The rival footing is deep
MOND by ~10⁴ at the horizon scale at *every* time in radiation domination. Its failure is not a
coincidence of one epoch.

**The BBN verdict, stated plainly: helium does NOT decide this fork.**

`a₀` is a constant of the free function in the *action* in every relativistic MOND completion
(RAQUAL, TeVeS, BIMOND, AeST). The Friedmann equation is sourced by the fields' energy densities,
not by a₀. Homogeneity forbids a background MOND effect independently: the Newtonian-analogue
shell acceleration r̈ = −(4πG/3)ρr has deep-MOND form r̈ = −√((4πG/3)ρ a₀ r), which scales as √r
rather than r and is therefore incompatible with homogeneous expansion. **Y_p is a₀-blind on both
footings, and the rival footing SURVIVES BBN (S5d PASSES).** Do not cite BBN as its kill.

The conditional row, for completeness only: *if* the deep-MOND boost reached the background
(the Felten/Sanders Newtonian-analogue reading), then λ = 97, T_f rises from 0.8 to 3.7 MeV,
X_n = 0.41, and Y_p = 0.824 against the standard-baseline 0.270 — 163σ against Aver et al.'s
0.2453 ± 0.0034. That is S5f, a FAIL that is explicitly **conditional and not a kill**. For
reference, what BBN does bound: ΔN_eff ≲ 0.25 → ΔH/H ≤ 1.7% → G_eff/G − 1 ≤ 3.4%.

---

## 5. Does a relativistic MOND theory already pass the CMB? Yes (S7)

Skordis & Złośnik 2021 (PRL **127** 161302) show AeST reproduces the Planck TT/TE/EE spectra and
the linear matter power spectrum at ΛCDM quality — **not** by making a₀ small at recombination
(a₀ in AeST is a constant of 𝒦(𝒬), the same one that does galaxies), but by:

1. **𝒦 has a quadratic minimum**, so on FRW the shift-symmetric charge redshifts as a⁻³ and the
   scalar sector behaves as **pressureless dust** with vanishing sound speed. At recombination the
   gravitational source is dust + baryons + radiation, i.e. numerically ΛCDM, and the peaks —
   including the third-peak forcing — come out standard.
2. **The MOND limit is quasi-static and gradient-dominated**: it needs |∇𝒬|² to dominate over 𝒬̇².
   At cosmological scales at recombination the time derivatives dominate, so the AQUAL boost of §3
   is *not* what the theory does there. §3 is an upper bound the completion evades by construction.

So `g/a₀ ~ a few` at recombination is **not by itself fatal** to a constant-a₀ MOND theory
(S7a PASSES). This lane does not claim otherwise.

**What the rescue does not cover, and this asymmetry is what decides the fork (S7b FAILS):**

- the rescue exists *because a₀ is a constant of the action*. The rival footing demands the free
  function depend on the background density. That is exactly the density promotion the programme's
  own `nbody_2026/stage17_a0z_from_the_action_2026.py` proves fatal from the action's side —
  unsuppressed backreaction (Q𝒦″ = O(μ²) rather than charge-suppressed), and verbatim: *"ρ_Q =
  M⁴ + dust GROWS into the past ⇒ a₀ RISES toward recombination ⇒ MOND ON at the CMB ⇒ fatal."*
  There is no AeST-shaped theory with a₀ ∝ H;
- the dust component that saves the CMB is the same cold component the programme's matching
  theorem shows falls into galaxies and double-counts with the boost by 2.7–4.4×. **The CMB rescue
  is real and it is not free.**

---

## 6. Does the record contradict itself? Yes — in shorthand, not in the derivation (S6)

`README.md` line 54 and the memory index both state the derived law is *"constant to <1%
everywhere MOND is tested (z ≤ 5), off at recombination as an output (a₀ falls to 0.002–0.006 of
today's value)."* The canonical footing ρ = ρ_Λ with w = −1 gives a₀(z) = a₀(0) **exactly**, at
every redshift. These cannot both be the same law.

- I reproduce the banked 0.002–0.006 from the stage17 / README **pressure** law,
  a₀²(z)/a₀²(0) = √(1+ν₀²)/√(1+ν₀²(1+z)⁶) over its committed window ν₀ ∈ [2.1e-5, 1.8e-4]:
  **0.0020–0.0060** (S6b PASSES). The two laws differ by **167×–490×** at recombination and agree
  only at z = 0 (S6c FAILS).
- **Resolution, and it is a labelling finding, not a physics error.** The README is internally
  explicit: the promotion is a₀² = κ²G(−𝒦(𝒬)) = κ²G(−p_Q), the dark sector's *pressure*, and
  −𝒦 = ρ_Λ **today**. So `a₀ = κ c √(G ρ_Λ)` is the law's boundary condition at z = 0, not the law.
  stage17 explicitly rejects the density promotion.
- **What is inconsistent is the shorthand** — "the headline equation is a₀ = κ c √(Gρ), canonical
  reading ρ = ρ_Λ" — which, at face value, forces a₀ constant and cannot produce the off-switch the
  same documents advertise as a prediction. **Three distinct a₀(z) laws circulate under one
  headline:** constant (ρ_Λ), rising as E(z) (ρ_tot), and the stage17 pressure law that declines as
  (1+z)^(−3/2) above z_t ≈ 17–35.
- **It changes no verdict here (S6d PASSES).** The off-switch drives a₀ *down*, so g/a₀ at the
  first peak goes from 8.1 to **1348–3948** — further into the Newtonian regime. It is safe and it
  buys nothing, because constant a₀ was already Newtonian there. That is the June-2026 "no CMB win"
  retraction, confirmed independently from a different direction.

---

## 7. Verbatim PASS/FAIL lines

See §8 of the transcript for the full 35. The load-bearing ones:

```
[PASS] S2i  the brief's premise g/a0 ~ 2.3 is NOT reproduced by any defensible subhorizon
            estimator (PASS = the premise does not survive)
[FAIL] S3a  CANONICAL footing, naive AQUAL applied literally to linear perturbations: is the
            induced tilt BELOW Planck's sigma(n_s)?   (5.1-6.1 sigma)
[FAIL] S4c  RIVAL footing: is the induced tilt below Planck's sigma(n_s)?   (27 sigma)
[PASS] S5d  RIVAL footing: is the observed helium abundance a decisive test of it?
            (PASS = the rival survives Y_p)
[FAIL] S6c  is the record's 'off at recombination' the SAME law as the headline
            a0 = kappa c sqrt(G rho_Lambda)?   (NO)
[PASS] S7a  is 'g/a0 of order a few at recombination' by itself fatal to a constant-a0 MOND
            theory?   (NO -- AeST fits Planck)
[FAIL] S7b  is the same rescue available to the rival footing a0 propto c H(z)?   (NO)
[PASS] S8a  VERDICT: does the CANONICAL footing survive recombination and BBN?   (YES)
[FAIL] S8b  VERDICT: does the RIVAL footing survive?   (NO)
[FAIL] S8c  VERDICT: is the record's 'off at recombination' consistent with the canonical
            rho_Lambda footing?   (NO)
```

---

## 8. What this lane changes, and what it does not

**Changes.**
1. The brief's premise is withdrawn: the CMB does **not** sit at the MOND transition on the
   canonical footing. The g/a₀ ≈ 2 number needs a missing 2π and a superhorizon mode.
2. The rival footing's failure is **epoch-independent** (g/a₀ = 1.07e-4 at horizon crossing at
   every radiation-era time), which is stronger than "it fails at recombination".
3. **BBN is not the discriminator.** The brief expected helium to be "the cleaner and possibly
   decisive test"; it is a₀-blind. The decisive evidence is the acoustic peaks and, independently,
   the programme's own stage17 action theorem.
4. The record carries three a₀(z) laws under one headline. The derivation is consistent; the
   index-level shorthand is not.
5. "g ≫ a₀" is not by itself a sufficient CMB defence at Planck precision (S3a). The defence is
   structural (AeST's dust-like cosmological sector), and that dust is the programme's known cost.

**Does not change.** κ = ½ remains fitted. a₀ ∝ H(z) was already recorded closed in `STANDING.md`
("recombination is deep-MOND, growth on an attractor tilted ×300") and by stage17; this lane
reproduces that independently rather than discovering it. Nothing here is a kill of ΛCDM or of the
canonical footing, and nothing here is a referee-proof result about the CMB — a Boltzmann-code
calculation in the actual completion would supersede every §3 number.

---

## Three-sentence verdict

The canonical footing ρ = ρ_Λ survives recombination and BBN: computed properly, g/a₀ is 4–16 at
last scattering rather than the brief's 2.3, nothing at BBN is within eleven orders of a₀, and a
relativistic completion carrying exactly this constant a₀ (AeST) already fits Planck — though the
defence is structural rather than a consequence of g/a₀ being large, since a literal AQUAL
implementation would already tilt the spectrum at 5–6σ. The rival footing ρ = ρ_tot does not
survive: it boosts the potentials 55–85× at recombination, tilts n_s by 27σ, shrinks the Jeans
length 7× so the acoustic oscillations become collapse, and sits at g/a₀ ≈ 1e-4 at horizon crossing
at every radiation-era epoch — but it is *not* killed by the helium abundance, which is a₀-blind,
and BBN must not be cited against it. The record's "off at recombination" belongs to a third law
(the stage17 pressure promotion, a₀ → 0.002–0.006 a₀(0)) that is 167–490× away from the constant
ρ_Λ reading at z = 1100 and coincides with it only today, which is a real labelling contradiction
in the shorthand and no contradiction at all in the derivation.
