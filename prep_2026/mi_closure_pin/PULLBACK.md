# LANE PULLBACK — the off-circular de Sitter–Unruh Wightman pullback (Gap A, closing input)

**Date:** 2026-07-16. **Scripts (both exit 0, no hard-coded booleans):**
`pullback_dsunruh.py` (36/36 checks, sympy + numpy; out `pullback_dsunruh.out`) and
`pullback_nonstationary.py` (32/32 checks, exact non-uniform dS worldline via embedding
Frenet–Serret; out `pullback_nonstationary.out`). Both a₀ footings carried throughout:
**canonical a₀ = cH_Λ/Z = 9.36×10⁻¹¹** (ρ_DE), **alt a₀ = 1.13×10⁻¹⁰** (ρ_tot/cH₀),
Z = √(32π/3), H_Λ = a₀Z/c, T_dS = H_Λ/2π.

This is the computation the closure map and the published SPEC named as **the** closing input for
Gap A (`mi_field_theory/CLOSURE_MAP.md` §3 "What would close it";
`real_research/reviews/mi_offcircular_completion_SPEC.py` Stage 4, READ-ONLY, verbatim):
evaluate the dS Wightman two-point function W(τ,τ′) = ⟨φ(x(τ))φ(x(τ′))⟩ on a **non-uniform**
(eccentric / anisotropic) de Sitter worldline, spectrally decompose, and read whether the memory
pole **descends below κ = H_Λ** into the amplitude-MOND band (⇒ the pullback pins η(β), **freedom
closes**) or **stays at/above κ = H_Λ** (the orbital AC content passes as phase, η(β) undetermined,
**freedom stands**).

---

## 0. One-line answer

**FREEDOM STANDS.** The pulled-back memory pole sits at **κ_eff = √(H_Λ² + (a/c)²) ≥ H_Λ** for
**every** eccentricity, **every** velocity anisotropy, and — the decisive point — **every reduction
weighting**. It equals H_Λ only in the geodesic (a→0, deep-MOND) limit and moves **upward**, never
downward, with any acceleration. Nothing the non-uniform orbit does pushes spectral weight below
κ = H_Λ into the amplitude-MOND band. Therefore the pullback **does not pin η(β)**. The honest prior
recorded in the SPEC ("likely stays free") is **confirmed by direct computation**, not assumed.

The residual is exactly what the closure map bracketed: **one reduction-weighting function η(β)**,
bounded between the two closure endpoints; its **overall sign is not settled by the pullback** (two
admissible weightings give opposite signs — computed, §5); the one thing forced is the **anisotropy
derivative** (radially-anisotropic systems run hotter than tangential ones at fixed weighting), which
is MG-impossible.

---

## 1. The exact stationary anchor — why the pole can never fall below H_Λ (Stage A, sympy)

A uniformly-accelerated worldline in dS₄ (a static-patch observer held at fixed areal radius r₀,
proper acceleration a = H²r₀/√(1−H²r₀²)) has, from the **embedding** X·X = 1/H² in M^{1,4}
(derived, not quoted):

$$Z(\Delta\tau)=s^2\cosh(\kappa_{\rm eff}\Delta\tau)+(1-s^2),\qquad
1-Z=-2s^2\sinh^2\!\Big(\tfrac{\kappa_{\rm eff}\Delta\tau}{2}\Big),\qquad
s=\sqrt{1-H^2r_0^2},\ \ \kappa_{\rm eff}=\frac{H}{s}=\sqrt{H^2+a^2}.$$

The conformal-scalar Wightman function W ∝ 1/(1−Z) then has its nearest complex pole at
Δτ = 2πi/κ_eff, i.e. a **KMS/thermal structure at T = κ_eff/2π = √(H²+a²)/2π** — the dS–Unruh
(Deser–Levin / Narnhofer–Peter–Thirring) temperature, obtained here from the pullback itself. The
memory pole (spectral scale) is **κ_eff**. Two exact facts (machine-checked):

- **κ_eff − H = √(H²+a²) − H ≥ 0**, with equality **iff a = 0**. The pole is bounded below by the
  horizon scale H_Λ; the geodesic/comoving observer sits exactly at κ = H_Λ (the DC thermal floor).
- At the MOND transition a = a₀: **κ_eff/H_Λ = √(1 + 1/Z²) = 1.01481** — the pole sits **1.48% ABOVE
  H_Λ**, identical in both footings (Z is footing-independent). Deep-MOND (a ≪ a₀): κ_eff → H_Λ to
  <10⁻⁶.

This is the whole physics in one inequality: **the dS–Unruh temperature is Pythagorean in (H, a)**, so
acceleration only ever raises the effective temperature / Matsubara pole. There is no mechanism in the
pullback to lower it below H_Λ.

## 2. The non-uniform eccentric worldline (Stage B) — AC content is a comb above the band

An eccentric Kepler worldline (a(τ) = GM/r(τ)², r = a_sma(1−e cos E)) has, for every bound orbit,
**a(τ) > 0 on the entire orbit** (a_min = a_apo = GM/r_apo² > 0). Its acceleration spectrum is a
**harmonic comb at n·ω_orbit** (FFT inter-harmonic leakage < 3% for e up to 0.9). And for **every**
bound system the orbital frequency sits far above the horizon:

| system | ω_orbit/H_Λ (canon) |
|---|---|
| Milky-Way disk (T≈230 Myr) | ~480 |
| Fornax-like dSph (T≈0.5 Gyr) | ~220 |
| outer dSph / UDG (T≈2 Gyr) | 55 |
| cluster-galaxy orbit (T≈5 Gyr) | 22 |

So the AC (orbital) modulation lives at n·ω_orbit ≫ H_Λ. The **only** thing at DC (zero frequency) is
the mean — which gives the thermal pole at κ_eff(⟨profile⟩) ≥ H_Λ. Nothing lands in the open band
(0, H_Λ). This is the field-theoretic origin of the closure-map statement "the AC/orbital sector is
passed as pure phase; MOND lives entirely in the DC/first-moment sector."

## 3. The anisotropic / radial-plunge worldline (Stage C) — floor survives to e→1

For near-radial plunges (e = 0.95, 0.99) the acceleration is sharply pericentre-peaked but still
bounded below by a_apo > 0; the instantaneous κ_eff(τ) = √(H_Λ² + (a(τ)/c)²) ranges from
**min κ_eff/H_Λ = 1.01481 at apocentre** up to 10²–10³ × H_Λ at pericentre. The floor is unmoved: the
plunge adds high-κ pericentre weight, never sub-H_Λ weight.

## 4. The literal non-stationary pullback (`pullback_nonstationary.py`)

To avoid relying on the adiabatic instantaneous-κ proxy, an **exact** non-uniform dS worldline is
built by integrating the embedding Frenet–Serret system on the hyperboloid,
X′ = u, u′ = a(τ)n + H²X, n′ = a(τ)u, with a prescribed breathing profile
a(τ) = a_mean(1 + e cos ω τ). The pulled-back invariant Z(τ,τ′) = H²X(τ)·X(τ′) and the
conformal-scalar W = 1/(1−Z) are formed, and the τ-averaged memory pole is extracted by nonlinear fit
of ⟨1−Z⟩ to s²(cosh κΔ − 1) (the exact stationary form). Since ω ≫ H the correlator (memory ~1/κ)
averages many orbital periods, so this τ-averaged pole is exactly the object the slow dS bath sees.

- **Anchor** (a = const): the fit recovers κ_eff = √(H²+a²) to ~10⁻⁸ for a = 0, 0.5, 1, 2 — the
  machinery is validated before the non-uniformity is switched on.
- **Non-uniform** (H ≡ 1, ordering preserved and swept): κ_eff/H = **1.415** (e = 0.3), **1.417**
  (e = 0.6), **1.414** (ω = 20, deeper hierarchy), **1.044** (deep-MOND a_mean = 0.3H, e = 0.5). Every
  value **≥ H** and lands inside the moment bracket [√(H²+a_min²), √(H²+a_max²)]. The a(τ) AC power
  sits entirely at the orbital line ω ≫ H; sub-band leakage ≤ 6×10⁻⁴.

The literal (non-adiabatic) pullback confirms the Stage-A/D inequality: **the pole stays at/above
κ = H_Λ.**

## 5. The crux (Stage D) and the sign (Stage E)

**Why "free" and not "closed."** The bath memory τ_mem = 1/H_Λ ≈ 17.5 Gyr ≫ orbital period, so the
slow bath integrates the fast orbit and retains **a moment** ⟨a^k⟩_w of the a(τ) history. **Which
moment is exactly η(β).** Computing the pole for a family of weightings k = 1 (⟨a⟩), 2 (rms), 4, and
a_min, at fixed e, **all give κ_eff/H_Λ ≥ 1**:

| e | k=1 ⟨a⟩ | k=2 rms | k=4 | a_min (apo) |
|---|---|---|---|---|
| 0.0 | 1.01481 | 1.01481 | 1.01481 | 1.01481 |
| 0.3 | 1.01481 | 1.01780 | 1.02391 | 1.00474 |
| 0.7 | 1.01481 | 1.04977 | 1.15511 | 1.00091 |
| 0.9 | 1.01481 | 1.22730 | 2.26709 | 1.00022 |

The pole is ≥ H_Λ for **every** weighting ⇒ the pullback spectrally admits **all** of them ⇒ it
**cannot select one** ⇒ η(β) is not pinned. (If some weighting had driven the pole below H_Λ, that one
would be selected and freedom would close. None does.) The un-pinned lever is the rms/mean
acceleration ratio, which grows monotonically with e (1.10, 1.85, 4.12 for e = 0.3, 0.7, 0.9).

**The sign (settled straight, not by a proxy).** The framework RAR g_obs(g_bar) = √(g_bar²+g_bar a₀)
is **concave** in g_bar (verified). Under closure A (instantaneous) the orbit sits **exactly** on the
circular RAR — offset 0, no sign. Under closure B the offset's sign is set by which moment weights the
g_bar history, and this is **not** pinned: computed on a deep-MOND eccentric orbit, an
**amplitude/pericentre-weighted** moment gives offset **+0.056 dex** (e=0.3) / **+0.40 dex** (e=0.7),
while a **residence/apocentre-weighted** moment gives **−0.040 / −0.186 dex** — **opposite signs**. So
the pullback does not settle the overall sign. What **is** forced (positivity + the pericentre-dominated
amplitude functional, per CLOSURE_MAP §2.4 / rb3) is the **anisotropy derivative**:
d(offset)/d(radial anisotropy) > 0 — radially-anisotropic systems run hotter than tangential ones at
fixed weighting. MG-with-the-same-ν gives exactly zero offset and zero anisotropy dependence, so this
**correlation** is the MG-impossible signature; the overall sign at fixed anisotropy remains the A↔B
bracket.

## 6. The exact residual (both footings)

**Freedom stands. The residual is exactly ONE reduction-weighting function η(β)** on the 2-D
orbit-shape space (eccentricity × anisotropy), bounded between:

- **Closure A endpoint:** dSph offset = **0.000 dex** (exact, on the rotation RAR).
- **Closure B endpoint:** isotropic-ensemble dSph offset ≈ **−0.02 to −0.05 dex** (deep regime), with
  the radially-anisotropic tail flipping positive (pericentre kinetic pump — the framework's published
  σ-hysteresis direction). Footing-stable to ~10–15% (the footing only relabels y = g_bar/a₀).

κ_eff floor: H_Λ = 1.807×10⁻¹⁸ s⁻¹ (canon) / 2.182×10⁻¹⁸ s⁻¹ (alt). Sign of η forced only in its
anisotropy derivative; magnitude bracketed, not pinned. This is **identical** to the closure map's
prior deliverable (`CLOSURE_MAP.md` §3, C-P1) — the pullback **confirms** the bracket rather than
collapsing it.

## 7. Consequences and honest ceiling

1. **Off-circular predictivity** (dSph/dispersion RAR offset, eccentric-orbit RAR) remains a
   **sign-free, one-function bracket** [0 … closure-B pattern]. This is the exact boundary of the MI
   field theory's off-circular predictivity, stated precisely: **one bounded function**, sign forced
   only in its anisotropy derivative.
2. **Off-spherical lensing** inherits Gap A through B[K]; it stays bracketed by the same η(β).
3. **The planetary a₀/2 tension** (`planetary_doors/KERNEL_PLANETS.md`): the pole staying ≥ H_Λ means
   the RAR-preserving survivor remains the **gated Reading C** with a **free corner** — the pullback
   does **not** convert it into a forced clean evasion. The a₀/2 solar-system evasion stays a gated
   (free) choice, not a derived consequence. Honest, and unchanged by this lane.
4. **Ceiling:** this lane discriminates only among the framework's own closures; it prefers neither the
   framework nor ΛCDM, and it introduces no new number. s = −1 and a₀'s value remain postulates.

## 8. Ledger (this lane)

| # | Statement | Status |
|---|---|---|
| PB-D1 | κ_eff = √(H_Λ²+(a/c)²) ≥ H_Λ, equality iff a=0 (exact embedding + literal non-uniform pullback) | **DERIVED** |
| PB-D2 | At a=a₀ pole is 1.48% above H_Λ (= √(1+1/Z²)), both footings; deep-MOND → H_Λ | **DERIVED** |
| PB-D3 | Non-uniform AC content = comb at n·ω_orbit ≫ H_Λ; nothing in (0, H_Λ) | **DERIVED** |
| PB-D4 | Pole ≥ H_Λ for **every** moment weighting ⇒ pullback does not select one | **DERIVED (the crux)** |
| PB-D5 | Overall offset sign NOT settled by pullback (opposite signs for two admissible weightings) | **DERIVED** |
| PB-D6 | Anisotropy-derivative sign forced (radial hotter), MG-impossible | **DERIVED** (positivity + amplitude functional) |
| PB-P1 | η(β): one bounded reduction-weighting function; magnitude & overall sign | **FREE, bracketed** |
| PB-P2 | s = −1; a₀ value/footing | **POSTULATE / FORK** (both carried) |

**Bottom line.** The off-circular dS–Unruh Wightman pullback was computed literally, on exact
non-uniform (eccentric and radial-plunge) de Sitter worldlines, and its memory pole **stays at/above
κ = H_Λ** for every eccentricity, every anisotropy, and every reduction weighting. The pullback **does
not pin η(β)**; the honest prior "stays free" is confirmed. The theory's off-circular predictivity is
bounded by **exactly one function** — sign forced only in its anisotropy derivative, magnitude
bracketed [0 … the computed closure-B pattern], dSph offset 0 to −0.02…−0.05 dex both footings. This is
reported as the real, publishable result it is — a NULL that is as rigorous as a WIN would have been.

---

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_closure_pin && python3 pullback_dsunruh.py && python3 pullback_nonstationary.py` (both exit 0). Sources read (frozen read-only repo + local prep, cited inline): `mi_field_theory/CLOSURE_MAP.md`, `mi_field_theory/closure_map.py`, `mi_field_theory/BASELINE_ACTION.md`, `mi_field_theory/rederive_identity.py`, `mi_fingerprint/rb3_eccentric_offset.py`, `mi_fingerprint/rb2_frequency_dependence.py`, `real_research/reviews/mi_offcircular_completion_SPEC.py`, `planetary_doors/KERNEL_PLANETS.md`. Both a₀ footings throughout; s=−1 and a₀'s value postulated; no completeness/TOE/"closed" claim.*
