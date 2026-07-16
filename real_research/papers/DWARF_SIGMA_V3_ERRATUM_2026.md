# Correction (v2) to the dwarf-spheroidal velocity-dispersion prediction

**Status:** DRAFT erratum for author review — not yet issued. Confirm the exact record/DOI before versioning.
**Supersedes:** the v1 headline claim that first-infall dwarf spheroidals show a velocity dispersion "**+12–30% hotter at fixed pericenter than modified gravity allows — an MG-impossible signature**."
**Basis:** the adversarially-verified non-local modified-inertia kernel chain, committed (local) `7a8c2b16` → `b0bafcf6`; scripts `real_research/reviews/{mi_nonlocal_kernel, dwarf_sigma_mi_final, dsunruh_tau_mem, mi_offcircular_completion, mi_nonuniform_pullback}.py`, all exit 0.

---

## 1. What is being corrected

The v1 headline observable and its "MG-impossible" claim are **withdrawn**. The underlying effect is real, but the observable was mis-specified and the claim was inflated by a non-fair modified-gravity (MG) baseline. The *existence*, *sign*, and *MG-impossibility* of the true effect survive; the *headline framing* and the *magnitude-as-prediction* do not.

## 2. Why the v1 headline is wrong

The v1 claim compared the framework's dispersion to an MG baseline that omitted the external-field effect's own dependence on the (time-varying) external field. A **fair** instantaneous-external-field-effect MG dwarf — dispersion set by the current galactocentric external field `a_ext(r)` with no memory — reproduces a **large** phase-to-phase dispersion spread on its own (~74% across Crater II's measured orbit), purely because `a_ext` swings ~8× between apocentre and pericentre. **A large phase-spread, or a dwarf being "hotter" near pericentre, is therefore NOT MG-impossible** — it is ordinary orbital kinematics that modified gravity produces too. (Control check: the adiabatic dwarf Fornax shows a ~21% raw spread with essentially zero kernel content.)

## 3. The corrected observable (genuinely MG-impossible)

The M/L-immune, MG-impossible content is **σ hysteresis at fixed galactocentric radius**:

- **Modified gravity:** σ = single-valued function of the current radius, `σ = f(r)`. A dwarf inbound to pericentre and the same dwarf outbound at the *same* r have the *same* σ.
- **Modified inertia (this framework):** the inertia is a functional of the `a_ext` **history**, so σ(r) is **double-valued** — a dwarf caught outbound (recently post-pericentre) stays "hot" from its recent high loading, while inbound at the same r it is "cold."

This inbound-vs-outbound doubling of σ at fixed r cannot be produced by any modified-gravity theory and cannot be mimicked by mass-to-light ratio, anisotropy, or the EFE amplitude. **That is the corrected prediction.**

## 4. The corrected magnitude framing: a proxy measurement, not a dated number

The magnitude of the hysteresis is set by the kernel's corner frequency ω_c (equivalently the memory time τ_mem). We establish, through the de Sitter bath physics (fluctuation-dissipation from the dS Wightman function; the full non-uniform worldline pullback), that:

- The dS bath **forces** the kernel's Lorentzian form, the √2 DC weight, and the corner's *existence*; the memory pole is the Deser-Levin local surface gravity `κ_eff(a) = √(a² + (cH_Λ)²)/c`, time-varying along the orbit.
- The bath **does not force** the corner *location* ω_c. κ_eff(a) **decouples** from the internal orbital frequency ω_int (κ_eff/ω_int ~ v/c ~ 2×10⁻² in the dwarf band), and no intrinsic feature develops at ω_int. Setting ω_c = ω_int (hence τ_mem ≈ the internal dynamical time ~0.4 Gyr, the door-sized value) requires the Milgrom-1994 "internal orbit = averaging bandwidth" **postulate** — an input, not a derivation.

Consequently the hysteresis amplitude is **a proxy measurement of ω_c**, not a dated prediction:

| τ_mem (= 1/ω_c) | Crater II hysteresis | Antlia II | interpretation |
|---|---|---|---|
| 1/H_Λ ≈ 17.5 Gyr (bath correlator) | ~1.4% | ~1.1% | fully mixed, door ~vanishes |
| **1/ω_int ≈ 0.4 Gyr (averaging-bandwidth postulate)** | **7–18%** | **4–13%** | door-sized (postulate, not forced) |
| ~1.8 Myr (above-band pole) | ~0.2% | ~0.1% | no retained memory |

A positive detection would **place ω_c empirically**, resolving the corner frequency the theory currently cannot derive.

## 5. The clean model-independent fingerprint

Because the raw hysteresis amplitude is dominated by the (kinematic) `a_ext` swing, its magnitude alone is not a clean kernel diagnostic. The θ-kernel–specific signature is the **model-dependence spread** `|θ₀=√2 single-pole − θ₀=2 two-pole|`:

- **Deep-pericentre carriers** (Crater II y_max=3.4, Antlia II y_max=2.5): ~10 percentage-point spread.
- **Adiabatic controls** (Fornax, Sculptor, y_max≪1): ~0.6 pp.

A detection in which carriers show the ~10 pp kernel sensitivity while controls do not is the model-independent confirmation.

## 6. The data test (unchanged, still valid)

- **Gaia DR4 proper motions** (≈ Dec 2026) to resolve each dwarf's **inbound vs outbound** orbital branch.
- Deep spectroscopy of **N ≳ 200 members at ≲ 0.3 km/s** per-star precision (σ to ≲ 0.2–0.3 km/s ≈ 4–5%) on **~15–20 post-pericentre diffuse carriers** (Crater II, Antlia II already in hand).
- Test: **is σ double-valued at fixed r** (MG → exactly 0), and do carriers show the ~10 pp θ-model sensitivity while controls do not?
- The v1 pilot (Crater II ~60–120 stars; ρ = −0.196, p = 0.40) is both underpowered and mis-specified (predicting σ from y embeds σ) — a wrong-signed null, not evidence against.

## 7. What survives from v1

The **existence**, **sign** (outbound hotter than inbound), and **MG-impossibility** of the σ-hysteresis are unchanged and firm. Only (i) the headline observable ("hotter at fixed pericenter") and (ii) the presentation of the magnitude as a dated prediction are corrected. Both footings (a₀ = 9.36×10⁻¹¹ and 1.13×10⁻¹⁰) carried throughout; verdict footing-stable.
