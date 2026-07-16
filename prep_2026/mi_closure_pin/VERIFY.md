# VERIFY.md — Adversarial verification of the MI closure-pin lane

Framework: de Sitter–Unruh MODIFIED-INERTIA (Carl Zimmerman). a0 = cH_Λ/Z, both footings
(canonical 9.36e-11 / alt 1.13e-10). Judged on the framework's OWN terms (own kernel
K(□_u/a0²), own ν(y)=√(1+1/y), own dS-Unruh temperature), never through the standard-MOND lens.

Verifier: independent re-run + hand re-derivation + adversarial attack on every load-bearing
claim. Verdict per claim below. **Overall: UPHELD** (with one hygiene fix applied).

---

## 0. Re-run + tautology scan

All six scripts re-run to **exit 0**:
`pullback_dsunruh.py`, `pullback_nonstationary.py`, `ostro_nonlocal_verify.py`,
`rider_a_offcircular.py`, `rider_b_lensing.py`, `rider_c_planetary.py`.

The `check(name, cond)` machinery in every script is a legitimate global accumulator
(`if not ok: PASS = False`), not a verdict switch.

**FINDING (fixed):** the initial run contained exactly ONE hard-coded/tautological check —
`pullback_dsunruh.py:305`, `check("both footings carried ...", True)`. This is decorative
narration (it manufactured no physics result; every substantive claim in that file is backed
by a real computed check), but it is a literal `True` and repeats the field-theory build's
prior sin, violating the "this run must have 0" rule. **Replaced** with a genuine computed
condition (`HL_DE>0 and HL_TOT>0 and |HL_TOT/HL_DE − a0_tot/a0_de| < 1e-12`). Script still
exits 0. Post-fix scan: `grep -nE "check\([^,]+,\s*(True|False)\s*\)" *.py` → **0 matches**.
No other tautological or `x is x`/`.has(...)` self-referential checks anywhere.

---

## 1. Pole location — does the pullback pin η(β)? (freedom-stands NULL)

**Independently re-derived by hand** on the static-patch dS worldline
X⁰=(s/H)sinh(Ht), X⁴=(s/H)cosh(Ht), X¹=r₀, s=√(1−H²r₀²), η=diag(−1,1,1,1,1):

- Z = H²X_A·X_B = s²cosh(κΔ) + (1−s²), κ=H/s.
- 1−Z = −2s²sinh²(κΔ/2). Poles of W=1/(1−Z) at Δ=2πin/κ ⇒ KMS T=κ/2π.
- κ_eff = √(H²+a²) since (H/s)² = H² + (H²r₀/s)² = H²+a². **≥ H, equality iff a=0.**

This is the standard Deser–Levin / dS-Unruh result, and `pullback_dsunruh.py:95,103` verify
it symbolically (squared identity + 1−Z form) — genuine sympy, reproduced by me.
At a=a0: κ_eff/H_L = √(1+1/Z²) = 1.01481 (footing-independent, Z carries it). Confirmed.

`pullback_nonstationary.py` does a genuine LITERAL two-time pullback: integrates the embedding
Frenet–Serret ODE (X′=u, u′=a·n+H²X, n′=a·u) with DOP853, checks X·X=1/H² and u·u=−1 to 1e-6,
forms Z(τ,τ′)=H²X·X′, and recovers κ_eff by a real `curve_fit` of g(D)=s²(cosh(kD)−1) — not
hard-coded. Recovered κ_eff ≥ H and inside the moment bracket [√(H²+a_min²),√(H²+a_max²)].

**Attack on the NULL (tried to make freedom CLOSE):** the claim is that because
κ_eff=√(H²+⟨a⟩_w²) ≥ H for *every* moment/weighting w, the pole singularity selects none of
them ⇒ η free. I tried to construct a pullback that forces a unique weighting: the only
privileged candidate is the first moment (u·□_u u = −|a|² is exact there), but for a
NON-uniform worldline the FFT shows a full harmonic comb (not just DC), so higher moments
enter at the same order and the first moment is an *endpoint* (closure A), not forced. The
freedom claim rests additionally on the moment-tower not collapsing, which the lane honestly
flags as *inherited from CLOSURE_MAP/rb, not re-proven here* (honest ceiling ii, general-mass
residues not computed — but the pole LOCATION is mass-independent). **I could not force a
unique weighting from the pullback. The NULL is honestly supported, not manufactured.**

**Verdict: UPHELD.** η(β) is genuinely left free (one bounded sign-free-magnitude reduction
weighting on the 2-D eccentricity×anisotropy shape space).

---

## 2. The SIGN — forced or bracket?

**Overall offset sign — correctly reported as NOT forced.** `pullback_dsunruh.py:277-286`
computes two admissible weightings of the same |a| history: amplitude ⟨g²⟩/⟨g⟩ and
residence/harmonic ⟨1/g⟩⁻¹. They straddle zero: e=0.3 → **+0.0562 / −0.0399 dex**; e=0.7 →
**+0.4017 / −0.1859 dex**. Real computed Jensen flip (RAR concave, d²g_obs/dg_bar²<0 verified).
I reproduced the straddle. The lane does NOT claim a forced overall sign. **Not a manufactured
win.**

**The anisotropy DERIVATIVE — claimed FORCED and MG-impossible.** This is the one place a
manufactured WIN could hide, since `rider_a`'s `orbit_offset` uses ONE specific closure (the
⟨g_N²⟩ rms fixed point, radius-weighted average, line 69-72). I attacked it directly:
recomputed the eccentricity sweep on the same Plummer orbits under

- rms fixed point (rider_a's own): Spearman(e,offset) = **+0.857**
- residence/harmonic ⟨1/g_N²⟩⁻¹, time-weighted: **+0.964**
- aggressive apocentre residence r²·harm(−2): **+1.000**
- r⁴·harm(−4): **+1.000**
- extreme r⁶·mom(−6): **+0.900**

The offset *magnitude* shrinks toward zero for apocentre-heavy weightings, but **the SLOPE sign
stays positive across every admissible weighting I could construct — I could not flip it.**
(The negative residence slope in the Kepler-at-fixed-mean panel is a different construction —
it drives the *overall sign*, which the lane already brackets — not the deepening-orbit
anisotropy slope.) The MG-with-same-ν comparison is legitimate: for an isolated spherical
system MG gives g_obs=ν·g_bar pointwise ⇒ offset≡0 and zero shape-dependence, whereas MI's
orbit-history boost produces the shape-dependence. So d(offset)/d(radial-anisotropy)>0 is a
genuine MI-vs-MG differential discriminator.

**Verdict: UPHELD.** Overall sign correctly bracketed (unpinned); anisotropy derivative
genuinely forced and MG-impossible, survived an aggressive weighting-flip attack.

---

## 3. Planetary a0/2 — evasion forced or free corner still needed?

**Independently recomputed** the per-planet a0/2 residual vs the cited INPOP/EPM δg bounds:

| planet  | a0/2·excl (canon) | (alt) |
|---------|------|------|
| Mercury | 1017× | 1228× |
| Venus   | 585×  | 706×  |
| Earth   | 5379× | 6494× |
| Mars    | 33429×| 40357×|
| Jupiter | 84×   | 101×  |
| Saturn  | 6686× | 8071× |

Matches `rider_c` exactly. The ν−1 → a0/(2g_bar) → constant a0/2 sunward tail confirmed
(y=1e4 gives δg/a0=0.4999). The action-forced corner ω_c=a0/2c=1.56e-19 rad/s (τ_mem=203 Gyr)
sits ~4-5 orders BELOW the Reading-C planetary window (~Myr), and at it the galactic boost
L_c(ω_gal/ω_c)=2.9e-8 ⇒ **RAR-dead at galaxies** (I reproduced ω_gal=9.2e-16, retained 2.87e-8).
`evasion_forced = (gal_retained_action > 0.9)` is a genuine computed condition → False.

**Verdict: UPHELD.** The clean solar-system evasion is NOT forced; the only survivor is the
gated Reading C with a FREE ~Myr corner (unpinned by both action and pullback). The a0/2
tension SURVIVES — reported straight as a NULL, not spun as a pass.

---

## 4. Ostrogradsky verify — genuine Hessian or hard-coded pass?

`ostro_nonlocal_verify.py` **genuinely computes** the momenta, reproduced independently:

- **T1 photon:** det g̃ = **B−1** (sympy), electric Hessian H_ij = −√(−g̃)·g̃⁰⁰·g̃ⁱʲ; the causal
  bound B<1 EMERGES where the Hessian loses positivity (not imposed).
- **T2 nonlocal frame:** spectral density ρ(t)=(1/π)Im K(−t+i0) computed via mpmath on both
  branch-cut regions; ρ≥0 on a 600-point grid; sum rule ∫dμ/|t| = **0.99999998** (I reproduced
  1.0000), region-B share 2/π. Ostrogradsky Hessian d²L/dχ̈² = **0** (χ̈ enters linearly —
  reproduced), kinetic Hessian = 2dμ>0, mass²=t·a0²>0 ⇒ healthy Herglotz tower.
- **T3 anti-tautology controls (load-bearing):** the SAME machinery flags L=½q̈² (Hessian=**1**≠0,
  reproduced), a negative-measure kernel (kinetic<0), and passes a healthy KG field. This proves
  the T2 positivity check discriminates and is not decorative.

**Verdict: UPHELD.** Real momentum Hessians; verdict "ghost-free" is correct; the old
tautology (`True is a_proxy.has(Derivative)`) is genuinely replaced by a discriminating test.

---

## 5. Manufactured-WIN / manufactured-NULL hunt (equal scrutiny)

- **Manufactured WIN sought:** the "FORCED anisotropy derivative / MG-impossible" claim
  (§2). Attacked with 5 weightings incl. extreme apocentre — **did not flip**; the claim is
  real. The lane did NOT over-claim the overall sign (kept it a bracket) or the planetary
  evasion (kept it conditional). No manufactured win found.
- **Manufactured NULL sought:** the "freedom stands / η free" claim (§1) and the "planetary
  evasion not forced" claim (§3). The freedom NULL rests on an inherited (flagged) moment-tower
  non-collapse but is airtight at the pole-location level, and I could not force a unique
  weighting. The planetary NULL is a straight computation. Neither is manufactured.

---

## VERDICT SUMMARY

| Claim | Verdict |
|-------|---------|
| Scripts exit 0, 0 tautological checks | **UPHELD** (1 decorative `True` found & fixed → 0) |
| Pole κ_eff=√(H²+a²)≥H, freedom η(β) STANDS | **UPHELD** (hand-derived + attack failed) |
| Overall off-circular sign NOT forced (bracket) | **UPHELD** (Jensen flip real) |
| Anisotropy derivative >0, MG-impossible, FORCED | **UPHELD** (survived 5-weighting flip attack) |
| Planetary a0/2 evasion NOT forced, tension survives | **UPHELD** (per-planet recomputed exactly) |
| Nonlocal disformal sector ghost-free (Ostrogradsky) | **UPHELD** (real Hessians + controls) |

Both a0 footings carried throughout. s=−1 and a0's value remain postulates (untouched by this
lane). No "theory complete/closed/proved" language. c_T=1 and Cassini respected. Framework
judged on its own terms. The lane prefers neither the framework nor ΛCDM and introduces no new
number — an honest ceiling on off-circular predictivity: exactly ONE bounded sign-free
reduction weighting η(β) remains free.

Frozen repo `zimmerman-formula` untouched; all edits confined to `mi_closure_pin/`.
