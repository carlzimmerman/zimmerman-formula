# The Full Non-Uniform dS-Unruh Pullback: is the memory corner ω_c FORCED at ω_int?

**Verdict: FREE (bounded).** The corner ω_c is NOT forced to ω_int by the non-uniform
pullback. `tau_mem = 1/ω_int` is not derived; the dwarf σ-hysteresis magnitude stays a
**proxy measurement** of ω_c, not a dated bath-derived prediction. This confirms the prior
verdict at a strictly deeper level, and does NOT manufacture a forcing.

Script: `real_research/reviews/mi_nonuniform_pullback.py` (exit 0, all asserts pass).

---

## 1. Computation level actually reached (labeled exactly)

The **leading-order adiabatic/WKB envelope** pullback of the Bunch-Davies Wightman on a
genuinely non-uniform (eccentric-orbit) worldline. This is **beyond both prior reductions**:

- beyond the **uniform** constant-a stationary pullback (`dsunruh_tau_mem.py`, single kappa pole);
- beyond the **O(a_ext) fixed-bath-pole-at-kappa** reduction (`mi_offcircular_completion.py`).

The pole is **allowed to migrate**: the two-time separation is the phase integral
`Phi(tau,tau') = ∫ kappa_eff(s) ds`, with `kappa_eff(tau) = sqrt(a(tau)^2 + (cH_L)^2)/c`
(Deser-Levin local surface gravity), and `W ~ 1/sinh^2(Phi/2)`. This is genuinely two-time
(Phi at fixed lag varies with center-time).

**It is NOT** the fully-exact off-geodesic 5D-embedding BD pullback. That non-adiabatic
correction is the named residual (§5). Adiabaticity parameter
`max|d kappa_eff/dtau|/kappa_eff^2 = 0.76` at e=0.7 — controlled, not tiny; it rises toward 1
as e→1 (where dwarves tidally disrupt).

## 2. Uniform-limit validation (correctness check)

- **Sympy (Stage 0):** asymptotic decay rate `d(-lnW)/dlag → sqrt(a^2 + H^2) = kappa_eff`. The
  uniform pullback's single stationary pole is exactly the DL surface gravity. ✓
- **Numeric (Stage 2):** e→0 gives a FLAT pole (spread < 1e-6) equal to the constant
  `kappa_eff = sqrt(a^2 + (cH)^2)/c`. Uniform limit recovered. ✓

## 3. Non-uniform pole structure (the new content)

On e=0.7: the pole is a **time-varying ridge** `kappa_eff(a(T))` running from the apocentre
floor (`a→0`, `kappa_eff → H_Lambda = 1/17.5 Gyr`) to the pericentre Unruh rate (`a_peri/c`).
It varies by **31.85×** across the orbit and correlates with `kappa_eff(a(T))` at **1.0000**:
the pole **IS** the local DL surface gravity. This is a genuinely new intrinsic feature the
uniform/O(a_ext) correlators lacked — but it sits at `kappa_eff(a)`, an **acceleration-set**
absolute frequency, **not** at the bare kappa and **not** at ω_int.

## 4. The rescale tell-tale — and its HONEST correction (post-adversarial)

**Correction (Stage 4b, from two adversarial passes, both reproduced the numbers):** the
Stage-4 "rescale-ω_int tell-tale" is **structurally incapable of ever returning FORCED** and is
therefore a **consistency check of the premise, not a two-sided empirical test**. Reason:
`kappa_eff(tau) = sqrt(a(tau)^2 + (cH)^2)/c` is a function of `a(tau)` **alone**, and the pole
read by `two_time_pole_ridge` is `d/dlag` of `Phi = ∫ kappa_eff`, which **equals kappa_eff by
construction**. Holding `a(tau)` fixed while relabeling time trivially holds the pole fixed. The
verdict does **NOT** lean on Stage 4.

**The load-bearing, non-circular evidence for FREE** (three independent grounds, verifier-confirmed):

- **(A) Structural decoupling.** For any Newtonian bound orbit
  `kappa_eff_peri / ω_int ~ (a_peri/c)/ω_int ~ v_peri/c`. In the **physical dwarf band**
  (GM=1e30, e=0.7) this is `2.14e-2` (v/c=4.6e-3) — kappa_eff sits **~1.7 dex below** ω_int. The
  only regimes where `kappa_eff ≥ ω_int` demand a **relativistic peri** (deep potential,
  v/c≈0.84, GM=1e34 — outside the dwarf regime) or **e→0.99** (where WKB adiabaticity itself
  fails). Neither is the dwarf door; coincidence is geometric fine-tuning, not a bath property.
- **(B) Branch-point structure.** The dS BD correlator's only singularity is the
  `sinh^2(Phi/2)` pole whose argument `Phi = ∫ kappa_eff` carries **no ω_int**. An ω_int pole
  cannot arise from the correlator. FREE is the null; the burden is on FORCED to exhibit an ω_int
  pole, and nothing does.
- **(C) Z-floor lock.** `Z = sqrt(32π/3) > 1` floor-locks `kappa_eff(a~a0) = H·sqrt(1+1/Z²) ≈ H`
  (ratio 1.0148) — decades below ω_int. The floor is the bath constant cH_Lambda, not the drive.

## 5. Consequence for τ_mem and the dwarf door

`kappa_eff/ω_int = 2.70e-3` (mean), i.e. the bath's own memory pole is **-2.57 dex** from ω_int
(deep orbit) / -1.6 dex (dwarf band). The bath forces the memory pole to be `kappa_eff(a)` in
`[H_Lambda .. a_peri/c]` — an absolute, acceleration-set frequency. Therefore:

- **`tau_mem = 1/ω_int` is NOT derived.** The bath's own memory decay is Hubble-floored
  (τ ~ 1/H = 17.5 Gyr at apocentre) down to `1/(a_peri/c)` at pericentre — never `1/ω_int`.
- Landing ω_c = ω_int still requires the **Milgrom-1994 "internal orbit = averaging bandwidth"
  postulate** — an INPUT, not a derivation.
- **Dwarf door:** the σ-hysteresis **existence + sign + MG-impossibility remain firm** (from the
  memory functional + amplitude-average, unchanged). The **magnitude** (~7–18% Crater II) is set
  by `tau_mem = 1/ω_c`, which the pullback does NOT date. The magnitude stays a **PROXY
  MEASUREMENT** of ω_c — a positive dwarf-σ detection would place the corner empirically — NOT a
  dated, bath-derived prediction.

## 6. Biggest caveat

The "full pullback" is the **leading-order adiabatic/WKB envelope** (Phi = ∫ kappa_eff), NOT the
fully-exact off-geodesic 5D-embedding BD pullback; and the DL surface gravity is strictly derived
for **constant a**, so its use as the instantaneous local rate along a(tau) IS the adiabatic
approximation (adiabaticity 0.76 at e=0.7, degrading to ~1 as e→1 where dwarves live).

## 7. The irreducible residual (what keeps the door open, precisely)

The one closed-form object still open: the **non-adiabatic correction to Phi = ∫ kappa_eff** —
the fully-exact off-geodesic 5D-embedding pullback of the BD Wightman on the exact eccentric
worldline when adiabaticity is not small. This is **BOUNDED**: it can only inject bath harmonics
`n·kappa_eff` (the sinh² Matsubara ladder) and drive harmonics `m·ω_int`. It **cannot manufacture
a new absolute pole at ω_int** unless ω_int coincides with a kappa_eff — which the ridge and the
(A) decoupling show it does not (ω_int set by orbit geometry; kappa_eff by a & cH). So the residual
**cannot flip FREE→FORCED**. The exact object still open can shift spectral WEIGHT among
`{n·kappa_eff, m·ω_int}` but cannot create a pole at ω_int itself.

## 8. Does this close the last theory door?

**No — and it names the residual that keeps it open precisely.** The pullback does NOT force the
corner; it establishes, at a deeper level than the O(a_ext) reduction, that the only absolute
frequencies the dS correlator carries are the DL surface gravities `kappa_eff(a) ∈
[H_Lambda .. a_peri/c]`, and ω_int is not among them. The corner ω_c — hence `tau_mem` and the
dwarf-door magnitude — stays **FREE (bounded)**: a proxy measurement, gated on the Milgrom-1994
averaging-bandwidth postulate. The last theory door does not close; the irreducible residual is
the bounded non-adiabatic BD pullback of §7, which cannot flip the verdict.
