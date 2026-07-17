# SYNTHESIS — the MI lensing-completion swing (C1 / C2 / C3 + NO-GO)

**Date:** 2026-07-17 · **Status:** verified (all 5 scripts exit 0; adversarial verify UPHELD).
Frozen repo READ-ONLY throughout. Outputs only in `prep_2026/mi_lensing_completion/`.
Both a₀ footings carried (9.36×10⁻¹¹ canonical `cH_Λ/Z` · 1.13×10⁻¹⁰ alt).
Credit: Deffayet–Woodard 2011 (1106.4984), Skordis–Zlosnik AeST 2021, Milgrom (AQUAL / MOND-as-inertia).

---

## 1. Headline

**The ν² MI lensing wedge does NOT close as modified inertia. It closes only as modified GRAVITY, at the
price of a₀ becoming a free coupling.** A₀-DERIVED and single-metric MOND-lensing are mutually exclusive —
a sharpened, exact no-go. The theory can be completed for lensing (C2/C3b: single-metric, ghost-free,
GW170817-safe, correct √(a₀ g_bar) slope), but that completion forfeits the vacuum-derived a₀ = cH_Λ/Z —
the deepest possible cost to the program.

## 2. Outcome

**SHARPENED-NO-GO (as modified inertia) + COMPLETED-AS-MG (a₀ free) as the constructive partial.**
Footing-independent (the wedge, the shortfall 1/y, and the mass-blindness ratio √(M₂/M₁) are all a₀-free).

**The exact obstruction.** Within mandatory single-metric **S** (`¬S` = a second disformal photon cone =
GW170817-dead by ~7 orders — not reopened), the minimal mutually-exclusive subset is **{D, S, L}**, and the
binding collision is the **pair**:

> **a₀-DERIVED (passive 0-dof frame u, bounded Herglotz kernel ‖K‖≤1)  ⊕  single-metric MOND-lensing
> phantom (ν−1)ρ u_μu_ν  —  mutually exclusive.**

- Sourcing the phantom is **nonlocal in the baryons** (point-mass halo `M_ph(r)/r → √(a₀M/G)`, enclosed
  mass grows outside the source) ⇒ forces a propagating carrier whose acceleration scale is a **free
  Lagrangian coupling** ⇒ **¬D** (this is C2 / C3b).
- Keeping a₀ derived confines the modification to the passive frame's **bounded** kernel (‖K‖≤1, delivers
  the SUPPRESSION 1/ν, off-source `T_00=0`), short of the needed ν by **ν²−1 = 1/y → ∞** deep-MOND ⇒ **¬L**
  (this is pure MI / C1 / C3a). A *local* universal `F(y)` is additionally **mass-blind** (`F'_req ∝ √M`;
  fix on a 6×10¹⁰ galaxy → a 10¹⁴ cluster gets fraction 0.024, ~24× under-lensed).
- **Ghost-freedom G is NOT the lever:** C1's local a₀-derived term still fails L by mass-blindness
  regardless of its Ostrogradsky ghost. G and S are jointly satisfiable *on the L side* (C2/C3b hold both).

**The crux (independently re-derived, verify §2[B]): a passivity/amplification dichotomy.** a₀ = cH_Λ/Z is
derived *only because* the MI modification is a passive, causal, completely-monotone (Herglotz/Stieltjes)
vacuum-response kernel with a normalized measure ⇒ |K| ≤ K(0) = 1 ⇒ it can only **suppress**. MOND-lensing
needs **enhancement to ν > 1**, strictly **outside** the passive cone. The very property that derives a₀ is
the property that forbids the phantom. This is a structural sup-argument, not a failed search — conditional
on the (independently banked, frozen-repo v4/v11) kernel-passivity result, which is itself the source of the
a₀ derivation, so D and boundedness are locked together, not independently assumed.

### Lane scorecard (5 checks each)

| lane | candidate ΔS | lensing L | c_γ=c_GW | ghost | Cassini | cosmology | a₀ | verdict |
|---|---|---|---|---|---|---|---|---|
| **C1** | `∫√-g F(K(□_u/a₀²))·{R, uuR_μν}` | **FAIL** (mass-blind √M) | OK (scalar-R) / risk (uuR_μν) | **FAIL** (honest-var Ostrogradsky Φ‴) | OK* | plausible | kept-derived | **FAILS-LENSING** |
| **C2** | `∫√-g R[1+f(□⁻¹R)]`, retarded | **PASS** (F→1, √ slope) | PASS (purely metric) | cost (±½ ghost, tamed by *contested* retarded Rx) | PASS* (inherits AeST Q₂) | TUNE (separate fit) | **FREE** | **CLOSES-BUT-a₀-FREE (=MG)** |
| **C3a** | passive `−½ρh(X)(u·u)` | **FAIL** (delivers 1/ν, shortfall 1/y) | PASS | PASS | PASS | PASS | kept-derived | passive path can't source phantom |
| **C3b** | freed nonlocal carrier (AQUAL a₀/\|a\|) | **PASS** (F→1, √ slope) | PASS (own T_μν) | PASS (f′>0 Herglotz) | PASS | **FORFEITED** | **FREE** (+1 scalar dof) | **CLOSES-BUT-a₀-FREE (=MG)** |

Finite logical exhaustion (`nogo.py §5`): over all 16 assignments of {D,S,G,L}, the target **D=S=G=L=1 is
UNSAT**, and its ghost-relaxed sibling D=S=1,G=0,L=1 is also absent. The completion the lane sought does not
exist as modified inertia.

## 3. Completion statement — the honest final field-theory map

The MI field-theory program now stands as follows, sector by sector:

- **DYNAMICS — complete & a₀-derived.** The worldline moves as `g_obs = √(g_bar² + a₀ g_bar)`
  (ν = √(1+1/y), deep-MOND √(a₀ g_bar)), fits SPARC (0.108 dex @ Υ=0.70), from the passive-frame kernel
  `K(□_u/a₀²)` with **a₀ = cH_Λ/Z derived** (value + sign s=−1 remain postulates; the ν-kernel itself is
  Milgrom 1999 PLA 253:273 Eq 9 — the framework's distinctive content is the cH_Λ/Z coefficient + the MI
  completion). This sector is genuinely a completed modified-inertia field theory.
- **COSMOLOGY — viable, derived-degenerate.** The covariant PT result (ν_cosmo ∈ [1, 1.09], σ₈ +2–3%)
  survives; the growing mode sees the horizon-floored argument. Left ~intact by every candidate on the
  a₀-derived side.
- **LENSING — THIS RESULT: no completion as MI; completes only as MG (a₀ free).** Pure MI sources the
  SUPPRESSED ρ/ν and under-lenses (F < 1/ν, Brouwer 2021 ~27σ). The phantom (ν−1)ρ that would fix it cannot
  be sourced on a single metric while keeping a₀ derived (the no-go above). C2/C3b close it as
  Deffayet–Woodard / AeST-class modified gravity — single-metric, ghost-free (C3b) / ghost-cost-contested
  (C2), c_γ=c_GW safe, correct deep slope — **but a₀ is then a free coupling** (footing-non-diagnostic: both
  9.36e-11 and 1.13e-10 fit equally = the signature of a fitted parameter), plus a separate cosmology fit
  and (C3b) one new propagating scalar dof.

**Does a full field theory of gravity now exist, and at what cost?**
A single-metric, ghost-free, GW170817-safe field theory that reproduces MOND dynamics **and** MOND lensing
**does** exist (C2/C3b — this is the honest constructive content of the swing). **But it is modified
GRAVITY, not modified inertia:** it forfeits the vacuum-derived a₀ = cH_Λ/Z, which becomes a free
Lagrangian coupling. There is **no** field theory that closes all five checks while keeping a₀ derived — that
combination is provably obstructed (sharpened no-go, minimal mutually-exclusive subset {D,S,L}). So:

> **A complete field theory of gravity is available only at the cost of the program's single most
> distinctive claim — the derivation of a₀.** The MI-distinctive theory (a₀ derived) is complete for
> dynamics and cosmology but **incomplete for lensing, and provably so on a single metric.** No overclaim:
> no candidate passed all five a₀-derived, so "complete field theory of gravity" is NOT asserted for the MI
> reading. The program's true, defensible position remains the **a₀ reframing** (a₀ = cH_Λ/Z as the horizon
> scale of the passive vacuum) — and this result shows that reframing and single-metric MOND-lensing cannot
> coexist. a₀'s numerical value (9.36e-11) and the sign s=−1 remain postulates regardless of footing.

## 4. Next

1. **The relational σ-spread stays the live MI-distinctive front.** Lensing is now a shared-MG observable
   (C2/C3b degenerate with AeST); the clean modified-GRAVITY-impossible discriminator remains the
   non-adiabatic relational velocity-dispersion spread (MI 6–13%, MG exactly 0) — underpowered but the one
   place MI ≠ MG. Prioritize powering it over any further lensing route.
2. **Attack the banked premise, not the wedge.** The no-go is conditional on MI-kernel passivity
   (Herglotz, ‖K‖≤1, ∫dμ/|t|=1). The *only* MI escape is a kernel that enhances (ν>1) while staying causal
   and keeping a₀ tied to cH_Λ — i.e. a pumped/anti-dissipative frame response with a *derived* (not free)
   amplitude. The banked v4/v11 sign walls say this is closed pump-free; re-examine only if a NEW forced
   pump mechanism appears. Absent that, treat the no-go as final.
3. **Do NOT reopen** the disformal photon cone (GW170817-dead ~7 orders) or claim C2/C3b as an MI
   completion. If the MG completion is written up, label it Deffayet–Woodard/AeST-class with a₀ free,
   explicitly, and inherit the AeST Q₂-quadrupole caveat (Desmond–Hees–Famaey 2024) honestly.
4. **Optional formal hardening:** promote the C2 would-be-ghost analysis past the contested retarded
   prescription (is the ±½ kinetic block genuinely non-propagating, or is it a real ghost?) — decides
   whether the MG partial is clean ghost-free (C3b-like) or ghost-cost (C2).

---

*Reproduce:* `python3 {c1_frame_curvature,c2_nonlocal,c3_carrier,nogo,verify_adversarial}.py` — all exit 0
(C1 11/11, C2 18/0, nogo 16/16, verify independent). No "proves / solved / complete field theory" language:
no candidate passed all five a₀-derived, so none is claimed. The result is the sharpened no-go + the honest
MG partial. No manufactured completion; no manufactured no-go. Both footings; a₀ footing-non-diagnostic on
the lensing side.
