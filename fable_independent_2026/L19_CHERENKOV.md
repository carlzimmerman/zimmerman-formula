# L19 — does the gravitational-Cherenkov bound apply to IC10's k-essence clock?

2026-09-08. Lane L19 of [CHARTER.md](CHARTER.md). Script:
[L19_cherenkov_applicability.py](L19_cherenkov_applicability.py) → [.out](L19_cherenkov_applicability.out).
Exit 2 by design: 12 checks, 6 PASS (every control), 6 FAIL — and **four of those FAILs are this lane's
own L10 being corrected.**

Nothing under `closure_2026/integrable_clock_construction_2026/` was imported, executed or copied. The
IC10 plateau action was transcribed by hand from `IC10_LOCAL_CLOCK.md`.

## The three-sentence answer

The gravitational-Cherenkov bound is a bound on the **coupling of the subluminal mode to the emitting
particle's stress tensor**, not on its speed as such: for a gravitational-sector mode with a preferred
frame the vertex picks out `T^00 ~ E²` and the bound is `1 − c_s ≤ 2e-15`, but on IC10's η = 1 plateau
the metric sector is exactly Einstein and the clock reaches matter **only** through the conformal factor
`e^{2w}`, so the vertex is `T^μ_μ` and the applicable bound is `1 − c_s ≤ 1.4e-9` — **L10's number was
too tight by 7.2e5×**. That correction alone does *not* save `c_s² = 1/3`, which still fails the corrected
bound by 2.9e8×; what does save it is that L10 evaluated the framework's exponential wall in the wrong
place — along the ambient 10 kpc Galactic path, where `|a| ~ a₀` — when the radiation is generated in the
cosmic ray's **own** near field, where `|a|/a₀ = 8.8e38`, and applying it there (Milgrom 2011, re-derived
here independently) gives `D_loss = 4.5 ℓ_M`, 1.4e7× the Galactic path and 33× the Hubble distance, for
**any** subluminal speed and even at full gravitational-strength coupling. So the verdict is conditional:
**the lead's construction is alive with a subluminal clock, and σ = 1 is not forced by Cherenkov** —
provided its clock–matter coupling switches off at high acceleration, which its own static branch says it
does but which no IC file has yet computed.

## The PASS/FAIL lines, verbatim

```
[PASS] C1 [CONTROL] the Cherenkov kinematics derive symbolically: cos(theta), k_max = 2(p - Ev)/(1-v^2),
       the threshold E > M/sqrt(1-v^2), and the on-shell identity 2 p.k = k^2 = -(1-v^2)|k|^2
[PASS] C2 [CONTROL] Tr[(p'+M)(p+M)] = 4(p.p' + M^2) with explicit gamma matrices, and Maxwell's stress
       tensor is traceless identically
[PASS] C3 [CONTROL] the tensor-coupled energy-loss rate derived here reproduces BOTH Moore & Nelson's
       coefficient (as transcribed by Milgrom 2011 eq. 2) and the published Galactic bound 1 - c <= 2e-15
[PASS] C4 [coupling] IC10's clock couples to ordinary matter ONLY through the conformal factor -- the
       vertex is to T^mu_mu and to nothing else -- and the test detects a direct coupling when one is
       present (disformal positive control)
[FAIL] C5 [vertex] the trace vertex is (M/E)^2-suppressed relative to the tensor vertex at Cherenkov
       kinematics, as the standard conformal-decoupling argument would have it
[FAIL] C6 [bound] 1 - c_s <= 2e-15, the number L10 imposed, is the bound that applies to IC10's clock
[PASS] C7 [CONTROL] the derived rate, cut off at the primary's MOND radius, reproduces Milgrom 2011
       eq. (4) D_loss = q l_M with the cosmic-ray energy cancelling exactly, q = 2/(1-v^2)^2 -- on both
       a_0 footings
[FAIL] C8a [verdict] c_s^2 = 1/3 survives gravitational Cherenkov on the CORRECTED coupling alone, with
       no screening applied
[PASS] C8b [verdict] c_s^2 = 1/3 survives gravitational Cherenkov once the high-acceleration GR limit is
       applied where the radiation is generated (Milgrom 2011), on BOTH a_0 footings and BOTH couplings
[PASS] C9 [causality] the subluminal clock cone is causal -- it lies inside the metric null cone, so no
       closed causal curve can be formed
[FAIL] C10 [channels] photons, neutrinos or gravitons impose a Cherenkov bound on this clock that is
       stronger than the hadronic one
[FAIL] C11 [pulsar/CMB] binary pulsars or the CMB impose a bound on the clock's SOUND SPEED that is
       binding at c_s^2 = 1/3
[FAIL] C12 [VERDICT] L10's exclusion of c_s^2 = 1/3 by gravitational Cherenkov is correct AS STATED
       (bound 2e-15, exclusion 2.1e14x, exp wall cannot rescue)
```

Read the FAILs in the direction each cuts: **C5** cuts *against* the clock (this lane's own first-pass
reasoning was wrong and the trace coupling is far less protective than "conformal scalars don't couple to
radiation" suggests); **C8a** cuts against it too (the coupling correction alone is not enough);
**C10/C11** mean "no additional constraint found"; **C6/C12** are L10 being corrected.

## 1. What the bound is a bound on

Derived from scratch, not taken on authority (section A of the script). A primary `(E, M)` emitting one
quantum of a mode with `ω = v|k|`:

    cos θ = (E v + k(1-v²)/2)/p,   k_max = 2(p - E v)/(1-v²),   threshold E > M/√(1-v²),
    on shell 2 p·k = k² = -(1-v²)|k|²   (the emitted quantum is SPACELIKE),
    Γ = (1/16π E p v) ∫ dk |M|²,   dE/dx = (1/16π E p) ∫ dk k |M|²,   D_loss⁻¹ = (1/E) dE/dx.

Everything about the strength of the bound sits in `|M|²`, i.e. in **how the mode contracts with the
primary's stress tensor**. Two structures matter:

| mode | vertex | `|M|²` | rate scaling |
|---|---|---|---|
| gravitational-sector (tensor, or an aether spin-0 whose polarisation carries `u_μ u_ν`) | `e_{μν} T^{μν}` with `e ⊃ u_μu_ν` ⇒ `~E²` | `2 p⁴ sin⁴θ / M_Pl²` | `D_loss⁻¹ = (1/3) G δ² E³` |
| conformally coupled scalar | `φ T^μ_μ` | `β² M²[4M² + (1-v²)k²] / M_Pl²` (Dirac primary) | `D_loss⁻¹ = (1/4) β² G M² δ E` |

**Control (C3).** The tensor line reproduces the literature twice over. Its coefficient matches Milgrom
2011's transcription of Moore & Nelson (`D_loss⁻¹ = G p³ Q`, `Q ≈ δ²` once their partonic 1e-3 is
stripped) to a factor 3, and with that partonic factor restored it gives `1 − v ≤ 3.25e-15` at
`E = 3e20 eV` over 10 kpc against the published `2e-15` — **a factor 1.63.** The machinery is calibrated
against exactly the literature it is then used to overturn.

## 2. What IC10's clock couples to

From `IC10_LOCAL_CLOCK.md` on the η = 1 plateau, and frozen ingredient I2:

    S10|η=1 = ∫ √(-g̃) [ m* R̃/2 + P(X̃, w) ] + S_m[e^{2w} g̃, ψ],    g = e^{2w} g̃ the single physical metric.

**The clock field `T` does not appear in `S_m` at all.** Matter sees only `g`. The clock reaches matter
solely because `w` is slaved to `X̃` by the algebraic equation `P_w = 0`. Varying `w` (verified
symbolically, C4):

    ∂S_m/∂w = -√(-g) T^μ_μ      ⇒   the w equation with matter is   P_w + e^{4w} T^μ_μ = 0.

So the entire clock–matter vertex is `T^μ_μ` and nothing else. A **disformal positive control** —
`g_{μν} = e^{2w} g̃_{μν} + B T_μ T_ν` — makes `∂/∂T_0 ≠ 0` and shows the test is not vacuous.

**What had to be assumed, stated precisely:** (i) that `S_m[e^{2w}g̃, ψ]` is the complete matter action —
IC10 itself flags that "matter-coupled clock kinetic mixing must still be varied"; (ii) that `w` stays
auxiliary (`P_ww ≠ 0`), which L8-P6/P7/P8 verified on the sampled window. Nothing else.

**Why the character change matters.** In Einstein-aether/khronometric theory — IC5/IC6/IC7, and what
Elliott, Moore & Stoica actually bound — the spin-0 mode lives inside the gravitational sector, the aether
supplies `u_μ`, the mode's effective polarisation carries `u_μ u_ν`, and `e_{μν}T^{μν}` picks out
`T^00 ~ E²`. On IC10's plateau L8 verified DeWitt `λ = 1` identically and `m* > 0`: the graviton kinetic
operator is Einstein's, with no preferred-frame structure to inherit, and the clock's polarisation
contracts with `g_{μν}`. That is the whole difference.

## 3. The bound that actually applies (the computed answer)

`β = 1` is the gravitational-strength benchmark (`L_int = (β/M_Pl) φ T^μ_μ`; Brans-Dicke has
`β = 1/√(2ω+3)`, f(R) has `β = 1/√6 = 0.408`). No partonic factor is applied, deliberately: the trace
charge of a proton is its **mass** (`⟨p|T^μ_μ|p⟩ = 2M_p²` exactly for the hadron state), so the coherent
treatment is the correct one, and the trace form factor at `|q²| ~ (3e11 GeV)²` would suppress it further
— omitting it is conservative, i.e. generous to the exclusion.

| primary / energy | bound on `1 − c_s` (β = 1) | vs L10's 2e-15 |
|---|---|---|
| proton (Dirac), `E = 1e20 eV` | **4.33e-9** | 2.2e6× looser |
| proton (Dirac), `E = 3e20 eV` | **1.44e-9** | 7.2e5× looser |
| spin-0 primary (not physical) | 1.03e-16 | 5.1e-2× |

**A result worth naming correctly (C5, and it corrects this lane).** The familiar argument that a
conformal scalar decouples from ultra-relativistic matter because `T^μ_μ = -M²/E` is **false at Cherenkov
kinematics**: the emitted quantum is spacelike, `2p·k = k²`, so `p·p' = M² + (1-v²)k²/2` grows with `k`
and the trace does not vanish. The naive `(M/E)⁴` underestimates `|M_trace|²/|M_tensor|²` by 1.0e23×. And
the third table row is not a coincidence — for a **spin-0** primary the trace coupling reproduces the
coherent tensor bound to four digits (both integrals reduce to `(2/3)δ²E⁶`). The suppression found here is
therefore **entirely the Dirac structure** `⟨T^μ_μ⟩ = M ū(p')u(p)`, which carries one power of `M²` the
spin-0 trace does not. "Conformal coupling" is not the mechanism; the proton's spin-½ nature is.

At the measured `c_s² = 1/3` (`1 − c_s = 0.4226`), `E = 3e20 eV`, 10 kpc:

| coupling | `D_loss` | `D/D_loss` |
|---|---|---|
| trace, β = 1 | 5.17e11 m | **5.97e8** — excluded |
| tensor (L10's assumption) | 1.49e-11 m | 2.07e31 — excluded |

So **on the coupling correction alone, L10's conclusion survives and its number does not.** The applicable
exclusion factor is 2.9e8, not 2.1e14. Tolerating `c_s² = 1/3` on this arm would need `β ≤ 4.1e-5`.

## 4. Where the exponential wall is actually evaluated — L10's second, larger error

L10's escape analysis (K8) asked whether the construction's own screening `u² = 1 − e^{-|a|/a₀}` could
suppress the coupling **along the 10 kpc Galactic path**, found `|a| ~ a₀` there, and concluded "the exp
wall cannot rescue this gate… the wall is a function of `|a|/a₀` and the Cherenkov gate is read exactly
where `|a| ~ a₀`."

That is the wrong place to evaluate it, and the correction is published: **Milgrom, "Gravitational
Cherenkov losses in MOND theories", arXiv:1102.1818 (2011).** The cosmic ray is not a test particle
probing the ambient field — it is the **source**. Radiation of wavenumber `k` is generated coherently at
distance `~1/k` from it, and there the field is the primary's own. A hadron of momentum `p` carries a
bubble of radius `r_M = (G p / c a₀)^{1/2}` inside which `|a| ≫ a₀`; a theory that coincides with GR at
high acceleration simply does not produce waves with `k > 1/r_M`.

| footing | `E` | `r_M` | `k_dB⁻¹` | `(r_M k_dB)²` = `|a|/a₀` at `k_dB⁻¹` | `ℓ_M = c²/a₀` |
|---|---|---|---|---|---|
| canonical | 3e20 eV | 1.953e-8 m | 6.578e-28 m | **8.81e38** | 9.600e26 m |
| alt | 3e20 eV | 1.779e-8 m | 6.578e-28 m | 7.31e38 | 7.968e26 m |

(Milgrom quotes `r_M ≈ 1.64e-8 m` and `(r_M k_dB)² ~ 1e39` at `cp = 3e11 GeV` using `a₀ = 1.2e-10`;
rescaled to the canonical footing that is 1.87e-8 m, 4% from this lane's value.)

**Control C7 — Milgrom's result re-derived from this lane's own rate formula.** Feeding `k_cut = 1/r_M`
into the same integral, with `k_cut² = a₀/(G E)`:

    D_loss⁻¹ = (1/2) G E (1-v²)² k_cut² = (1/2)(1-v²)² a₀    ⇒    D_loss = q ℓ_M,  q = 2/(1-v²)²,

**and `E` cancels exactly.** That is Milgrom's eq. (4), obtained independently. Predicted `q = 4.500` at
`c_s² = 1/3`; measured from the full numerical integral `4.4998`, on both footings and both energies.

| footing | coupling | `D_loss` | `/ 10 kpc` | `/ D_H` |
|---|---|---|---|---|
| canonical | tensor (full gravitational strength) | 4.32e27 m | 1.40e7 | 33.2 |
| alt | tensor | 3.59e27 m | 1.16e7 | 27.6 |
| canonical | trace, β = 1 | 1.00e73 m | 3.25e52 | — |

Even with the **full** gravitational-strength tensor coupling — L10's own assumption — the loss distance
exceeds the Hubble distance, so the extragalactic `2e-19` version of the bound is neutralised too.

**And the framework's wall is stronger than Milgrom's sharp cutoff.** IC5/IC10 define `w = (u−1)ξ`, and
the static regular branch (IC-4, retained at η = 0: *"the old exponential constitutive equation therefore
survives"*) has `u² = 1 − e^{-|a|/a₀}`, so `1 − u ≈ ½ e^{-|a|/a₀}` and `w → 0` exponentially. Since the
*entire* clock–matter vertex is carried by `w` (section 2), the coupling in the cosmic ray's near field is
`~ exp(-8.8e38)` (canonical) / `exp(-7.3e38)` (alt). Not a factor of 1e-39 — zero.

## 5. The other constraints

- **Causality (C9, PASS).** Subluminal is the easy direction: the clock cone lies strictly inside the
  metric null cone, so no closed causal curve can be built. The preferred foliation is a *spare* argument
  here — it is what would be needed for L8-D7's superluminal band at `S < 0.0377`, in this solution's past.
- **Photons (C10).** `T^μ_μ = 0` identically for Maxwell in 4D (verified numerically): a photon **cannot**
  emit a conformally coupled clock quantum at tree level, at any speed. LHAASO's PeV photons give nothing.
- **Neutrinos.** Vertex `∝ m_ν²`; rate down by `(m_ν/M_p)⁴ = 1.3e-40`. IceCube gives nothing.
- **Gravitons.** The tensor mode is exactly luminal here (`c_T = 1`, an exact action identity, L8-A2/A3),
  so the channel Elliott, Moore & Stoica actually bound is closed at zero. A graviton could emit a clock
  quantum only via the background gradient `T̄_μ`, and no ultra-high-energy graviton flux exists to
  constrain it. Vacuous, not passed.
- **Binary pulsars (C11) — the constraint that actually deserves the next calculation.** A conformally
  coupled scalar generically radiates dipole energy from an asymmetric binary. Two things are both true:
  (i) this is a *high-acceleration* system, so the same wall applies and applies here at the right place —
  Milgrom makes exactly this point, and L10's own K6 (Cassini at 5.8e5 a₀, PPN passing by 3.7e4×) is the
  same statement; (ii) the dipole coefficient is **not** computed here and cannot be, because IC10's
  matter-coupled clock sector is one of its own stated open items. It is live, not passed. Note it
  constrains exactly the `β` on which the Cherenkov verdict now hangs.
- **CMB (C11).** `c_s² = 1/3` *is* the radiation sound speed; such a component does not cluster below its
  sound horizon and is perturbatively CMB-degenerate with a smooth relativistic fluid. The CMB constrains
  the clock's **density** (`N_eff`), which is L10's K5b arm, unchanged and still open. No bound on `c_s`.

## 6. Verdict, as a conditional, with the deciding input named

> **The bound applies at strength X if the clock couples in way Y:**
>
> - **Y1 — gravitational-sector mode with preferred-frame mixing** (DeWitt `λ ≠ 1`, no first-class
>   Hamiltonian constraint, `u_μ u_ν` in the polarisation): vertex `~E²`, **X = `1 − c_s ≤ 2e-15`**.
>   This is IC5/IC6/IC7, it is what Elliott, Moore & Stoica bound, and it is what L10 assumed. It is
>   **also** what IC10 becomes off the η = 1 plateau — L8-P9/P10 found IC9's `λ = 1/3 + 2/(3J9) ≠ 1` and a
>   residual `e^{2w}` once `η ≠ 1`.
> - **Y2 — shift-symmetric k-essence clock in an exactly Einstein metric sector, conformal coupling only**
>   (IC10 at η = 1 as published, plus I2): vertex `T^μ_μ`, **X = `1 − c_s ≤ 1.4e-9`** at β = 1 —
>   7.2e5× weaker than L10's number, but still violated by `c_s² = 1/3` by 2.9e8×.
> - **Y3 — the same, plus the theory's high-acceleration GR limit holding in the cosmic ray's own near
>   field**: **no bound at all**, `D_loss = 4.5 ℓ_M > 2π D_H`, for any `0 < c_s ≤ 1`, on both footings,
>   even at full gravitational-strength coupling.

**The deciding input, stated so the lead can settle it from its own action and nothing else:**

> Does the clock–matter conformal coupling switch off in the high-acceleration limit? Concretely: expand
> IC10's `w` equation with matter present, `P_w + e^{4w} T^μ_μ = 0`, on the **static** branch, and evaluate
> `∂w/∂X̃` as `|a|/a₀ → ∞`. If it vanishes at least as fast as `(a₀/|a|)^{1/2}` — and IC-4's
> `u² = 1 − e^{-|a|/a₀}` with `w = (u−1)ξ` says it goes as `e^{-|a|/a₀}`, vastly faster — then **Y3 holds,
> there is no Cherenkov bound, and σ = 1/3 survives.** If instead the coupling stays O(1) at high
> acceleration, **Y2 holds and σ = 1 is forced.** One calculation decides it, and it is the same one IC10
> already lists as its open item 3 (the sourced galactic branch, `Φ`, `Ψ`, measured `G`, all PPN).

## 7. What L10 got wrong, quantified — it is this lane's own result

1. **It used the wrong bound.** It applied the gravitational-sector number to a mode L8 later showed is
   not one. The applicable bound is `1.4e-9`, not `2e-15`: **too tight by 7.2e5×** in speed, 3.5e22× in
   the loss rate at `c_s² = 1/3`. Its "excluded by 2.1e14×" should read **2.9e8×**.
2. **Its escape analysis (K8) evaluated the exponential wall in the wrong place** — along the ambient
   Galactic path, where `|a| ~ a₀`, rather than in the cosmic ray's own near field, where
   `|a|/a₀ = 8.8e38`. K8's conclusion *"the exp wall cannot rescue this gate"* is **WITHDRAWN**; the wall
   does rescue it, by a published mechanism (Milgrom 2011) whose consequence this lane re-derived
   independently in C7.
3. **What L10 got right and this lane confirms.** The mode's speed is the invariant that matters; the
   tensor sector is not the issue; the PPN arm (K6) is untouched; and if the coupling does *not* screen
   then `c_s² = 1/3` is still excluded — by 2.9e8×.

**Handoff consequence.** `HANDOFF_CONTRACT.md` entry **A5** ("Gravitational Cherenkov excludes c_s² = 1/3
by 2.1e14×… the exp wall cannot rescue it") must be rewritten as the conditional above. **A6** ("Lower
edge is always Cherenkov ⇒ the khronon must be marginally superluminal") is correct only for a
gravitational-sector khronon (Y1) and must be scoped to that. **B1** (σ = 1 re-verification) is
**demoted**: σ = 1 is not forced by Cherenkov as things stand, so L15's re-derivation at σ = 1 is
contingency work, not the critical path. The critical path is the deciding input in section 6.

## Caveats, stated in the direction each cuts

- **Against the clock.** C5: the naive conformal-decoupling argument is false at Cherenkov kinematics.
  Without screening the trace coupling still excludes `c_s² = 1/3` by 2.9e8×. Do not quote the trace
  coupling alone as a rescue.
- **Against the clock.** Everything here is the η = 1 plateau. L8-P10 showed the Einstein form is a
  statement about that plateau, not the theory; off it, `λ ≠ 1` and Y1 applies again at the full `2e-15`.
  A transition spending time off the plateau at low acceleration reopens this.
- **Against the clock.** The dipole/pulsar arm is genuinely live and uncomputed, and it constrains exactly
  the `β` the verdict hangs on.
- **For the clock.** The proton trace form factor at `|q²| ~ (3e11 GeV)²` is omitted entirely — many
  orders of magnitude conservative in the direction of exclusion.
- **For the clock.** The TT polarisation sum used in the tensor control is the Lorentz-invariant one; a
  Lorentz-violating basis changes O(1) factors, and C3 shows those are within a factor 1.63.
- **The Milgrom cutoff is imported, not derived from IC10.** C7 re-derives its *consequence*
  (`D_loss = q ℓ_M`) from this lane's own rate formula, but the *premise* — that the coupling is switched
  off inside `r_M` — is the deciding input of section 6 and is **not** established for IC10's clock.

## Sources

- [Moore & Nelson, *Lower bound on the propagation speed of gravity from gravitational Cherenkov
  radiation*, JHEP 0109:023 (2001), hep-ph/0106220](https://arxiv.org/abs/hep-ph/0106220)
- Elliott, Moore & Stoica, *Constraining the new aether: gravitational Cherenkov radiation*,
  JHEP 0508:066 (2005), hep-ph/0505211
- [Milgrom, *Gravitational Cherenkov losses in MOND theories*, arXiv:1102.1818
  (2011)](https://arxiv.org/abs/1102.1818)
