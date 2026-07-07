# Non-Local Modified-Inertia Eccentricity Signal in Wide Binaries — Honest Standing (2026-07)

Framework: Carl Zimmerman's de Sitter–Unruh **modified-inertia** MOND.
a₀ = cH_Λ/Z = 9.36e-11 m/s², Z = √(32π/3). Own RAR ν(y)=√(1+1/y), y=g_bar/a₀;
inertia ratio μ_fw(x)=(√(1+4x²)−1)/2x, x=a/a₀; EOM μ_fw(|a|/a₀)·a = g_N.

**Bottom line (reconciled against 3 adversarial verifiers, all confirmed): the kernel is
legitimate and reduces correctly, but the headline "+1..9% positive eccentricity signal" is a
mislabeled-eccentricity ARTIFACT, not a physical result. The genuine MG-impossible observable in
this framework is NOT the wide-binary orbit-mean acceleration — it is the dwarf orbital-history
σ-dispersion (paper §6.3). The wide-binary orbit-mean channel, as built, has no isolable non-local
signal.** This is a null-with-a-lesson, reported both-ways.

---

## 1. Does the framework fix the kernel? PARTIAL — forced core + bounded residual (correct as stated)

From `real_research/papers/DSUNRUH_MI_THEORY_2026.md` §4 (read firsthand, lines 100–110):

- **FORCED by the bath:** DC weight θ(0)=√2 (amplitude/−3 dB branch, two independent routes converge);
  Lorentzian form-class (dS Wightman ~ −1/sinh² → exponential envelope → 1/(1+(ω/ω_c)²)); existence
  of the corner; θ(1)=1. Kernel form: **θ(y)=θ₀/(1+(θ₀−1)y²)**, θ₀=√2.
- **NOT forced (paper's own honesty marker, §4 line 110 + §7 item 4):** the corner LOCATION (y=1
  rides on the "internal orbit = averaging bandwidth" postulate, Milgrom-1994-licensed only in the
  quasi-static limit; the general multi-frequency case is **obstructed, not closed**) and the MEMORY
  ORDER (single-pole θ₀=√2, y⁻¹ tail vs two-pole θ₀=2, y⁻² tail; KMS does not fix the pole count).

So the framework fixes the RAR exactly + kernel DC/form-class/existence, leaving a bounded
corner-location + memory-order residual. **This provenance statement is accurate.** The kernel
functions `th_fw(y)=√2/(1+(√2−1)y²)` and `th_2pole(y)=2/(1+y²)` match paper §4 line 108 exactly and
are NOT invented.

**Crucially, the kernel enters as** `A = a_internal + θ(y)·a_external`, `y = ω_external/ω_internal`
(paper §4 line 102). It re-weights how a body's **INTERNAL** dynamics respond to a time-varying
**EXTERNAL** field — i.e. an external-field-effect / orbital-history quantity. It is not a re-weighting
of a two-body orbit's own acceleration harmonics. The wide-binary sweep mapped the kernel onto the
wrong observable (see §3).

---

## 2. The four validations

| # | Validation | Result | Notes |
|---|-----------|--------|-------|
| V1 | Circular-orbit reduction → ν(y)=√(1+1/y) | **PASS** (max rel.err 3.6e-12) | Kernel genuinely reduces to the framework RAR for a circle; θ(1)=1 drops out. Not invented. |
| V2 | Newtonian limit boost→1 at a≫a₀ | **PASS** | Modification vanishes, all e. |
| V3 | MG baseline = 0 | **PASS but TRIVIAL** | Evaluates g=ν(g_N/a₀)·g_N at fixed r across e-*labels*; e never enters the expression, so 0 spread is guaranteed by inspection. It is NOT the null the signal is measured against. |
| V4 | No artifact / resolution stability | **PASS mechanically, but the wrong quantity is stable** | The reported signal is deterministic (an e-mismatch), so it reproduces stably under N. Stability does not rescue it. |

V1–V3 confirmed by direct re-run: `max rel.err = 3.61e-12`, `boost→1`, `MG e-spread = 0.0e+00`.
The kernel is this framework's MI. The failure is downstream of the kernel, in the observable.

---

## 3. THE ARTIFACT (reconciled — all three verifiers correct)

The sweep reports `signal = (orbit-mean a_eff of kernel orbit) − (orbit-mean a_eff of θ≡1 orbit)`,
divided by the reference, in %. Two independent facts kill the "+1..9%" headline:

**(a) The observable is DC-preserving → θ cannot touch it on a fixed orbit.**
`build_aeff_time` re-weights harmonics k≥2 but leaves W[0]=1 (the DC bin). The time-MEAN of a series
equals its DC bin. So on ANY *fixed* acceleration series, θ-reweighting changes the mean by exactly 0.
Verified: mean(θ-reweighted) − mean(original) = −2.6e-26 (machine zero). **The kernel is invisible to
the reported orbit-mean on a fixed orbit.**

**(b) The nonzero number comes entirely from an eccentricity mismatch between two orbits.**
The θ≡1 reference and the θ-kernel run are each self-consistently converged, and the kernel
partially circularizes, so they land at DIFFERENT measured e:

| e_target | e_ref (θ≡1) | e_kernel (θ_fw) | Δe | apo_ref | apo_kernel | reported "signal" |
|---|---|---|---|---|---|---|
| 0.2 | 0.1351 | 0.1243 | +0.011 | 8866 AU | 8673 AU | +1.06% |
| 0.4 | 0.2459 | 0.2181 | +0.028 | 11161 | 10524 | +3.89% |
| 0.6 | 0.3350 | 0.2952 | +0.040 | 13561 | 12412 | +6.20% |
| 0.8 | 0.4064 | 0.3600 | +0.046 | 16003 | 14355 | +7.39% |

Orbit-mean |a| is a steep function of e at fixed pericenter (pure kinematics, zero kernel content).
The x-axis is labeled with the reference e (0.335), not the differenced kernel orbit's e (0.295).
Differencing two orbits at different e manufactures the signal.

**(c) Controlling for e collapses the headline and flips its sign.**
Comparing the kernel orbit against a pure-MG orbit at the SAME measured e (via a θ≡1 mean(e)
calibration) gives the matched-e residual — resolution-stable, sub-1%, **sign-changing**:

| e_kernel | matched-e signal | (mislabeled was) |
|---|---|---|
| 0.124 | **−0.71%** | +1.06% |
| 0.218 | **−0.56%** | +3.89% |
| 0.295 | **+0.03%** | +6.20% |
| 0.360 | **+0.54%** | +7.39% |

The +6.2% at e≈0.30 collapses to +0.03% (99.5% of it was the e-mismatch confound). The residual
changes sign (−0.71% → +0.54%), directly contradicting the claimed "definite POSITIVE, few-to-several
percent" headline. Resolution-stable (N=2048/4096/8192 agree to ±0.002%), so it is a real orbit-shape
residual — but sub-1%, sign-ambiguous, and plausibly just the θ-kernel producing a slightly different
a(r) map, NOT a clean MG-impossible prediction.

**(d) Scaling-slope overclaim.** The COMPUTE input claimed small-e slope "2.6–2.7 / ~e²". The sweep
script's OWN printed output is **slope = 1.38**. The ~e² claim is unsupported by the script.

**(e) The "MG %" column is self-minus-self.** It compares the θ≡1 orbit to itself → 0 by construction.
It is not an independent MG null and does not demonstrate MG-impossibility of the reported signal.

---

## 4. Model-independent statement — CORRECTED

What survives, honestly:

- **The kernel is decreasing** (θ down-weights higher harmonics) — this is model-independent across the
  whole KMS-permitted window (√2↔2, y⁻¹↔y⁻²). TRUE and forced.
- **A genuine MG-impossible observable EXISTS** in this framework, because inertia is a functional of
  acceleration history: the **external-field / orbital-history** channel. Paper §6.3 quantifies the
  RIGHT one — the **dwarf σ-dispersion**: a diffuse dwarf on a radial-plunge orbit runs hotter (larger
  internal σ) than a circular-orbit dwarf of the same mass and pericenter, +12–14% at θ₀=√2 (+12–30%
  over the memory-order residual), exactly 0 in any instantaneous-EFE MOND/ΛCDM. That is the framework's
  real MG-impossible door (already published, DOI 10.5281/zenodo.20947913, currently an underpowered null).
- **What does NOT survive:** a definite-positive, few-to-several-percent eccentricity signal in the
  wide-binary orbit-mean acceleration. The correct model-independent statement for THIS observable is:
  **the isolable non-local signal is ≲1% and sign-ambiguous at the eccentricities the solver can reach
  (e≲0.36); the orbit-mean channel is DC-protected and largely blind to the kernel.** Sign and "few-%"
  are NOT model-independent here — they were an artifact of the e-mismatch.

---

## 5. Is MG exactly 0 — is the signal genuinely MG-impossible?

- MG's intrinsic force law g(r)=ν(g_N/a₀)·g_N is a function of r only → exactly 0 eccentricity
  dependence in the v(r) law. TRUE (V3), but trivial and not the operative null.
- The operative question — can a modified-GRAVITY orbit at the kernel orbit's *measured* e match its
  orbit-mean acceleration — is **never tested by these scripts**. The matched-e comparison in §3(c)
  (kernel orbit vs MG orbit at same e) is the closest proxy, and it yields a sub-1% sign-changing
  residual. **MG-impossibility of the wide-binary orbit-mean signal is UNPROVEN and, given the
  DC-protection, most likely absent for this observable.** MG-impossibility genuinely holds for the
  *dwarf orbital-history* observable (§4 above), by a different (history-dependent internal-σ) mechanism.

---

## 6. Single biggest caveat

**The observable was mis-chosen.** The kernel's physical action is on a body's INTERNAL dynamics under
a time-varying EXTERNAL field (A = a_int + θ(y)·a_ext), which is why the framework's own MG-impossible
prediction is the dwarf internal-σ dispersion, not a two-body orbit property. Applying θ to the binary's
own orbital-acceleration harmonics targets a DC-protected orbit-mean, so the kernel leaves it unchanged;
the entire reported signal is the eccentricity mismatch between two self-consistently-converged orbits.

---

## 7. Real testable door, or model-dependent one needing the kernel pinned first?

**For wide binaries (this workflow's target): NOT a clean door as formulated.** The orbit-mean channel
is DC-protected and the isolable residual is ≲1% and sign-ambiguous — below any plausible Gaia
wide-binary sensitivity and not cleanly MG-impossible. The eccentricity-resolved Gaia wide-binary test
(r>5000 AU) is **not** powered to see the honest residual, and the +6–9% target it was pitched against
does not exist.

**The framework's genuine MG-impossible door is elsewhere and already published:** the dwarf
orbital-history σ-dispersion (paper §6.3, DOI 10.5281/zenodo.20947913), +12–30% over the memory band,
tested via Gaia DR4 (Dec 2026) + diffuse-carrier spectroscopy of Crater II / Antlia II vs Fornax /
Sculptor. That door is real, MG-impossible, and model-dependent in magnitude (memory-order residual),
but currently an underpowered null (partial Spearman ρ=−0.196, p=0.395).

**Recommendation:** do not publish the wide-binary eccentricity signal. If the wide-binary channel is
to be pursued, the observable must be redefined to something the kernel actually touches (a per-harmonic
/ phase quantity such as apsidal-precession rate or the *shape* of a_r(t), not the DC-protected
orbit-mean) AND compared against a modified-GRAVITY orbit at MATCHED measured e — neither of which the
current solver does.

---

## Reproduction commands

```bash
cd /Users/carlzimmerman/new_physics/zimmerman-formula

# Committed solver (V1 3.6e-12, V2, V3, V4 all pass; kernel legitimate):
python3 real_research/reviews/mi_nonlocal_kernel.py

# Sweep (prints its own slope=1.38, not 2.6-2.7; headline is the artifact):
python3 real_research/reviews/mi_ecc_curve_sweep.py

# DC-preservation proof (theta invisible to orbit-mean on a fixed series):
python3 - <<'PY'
import numpy as np
from numpy.fft import rfft, irfft
au = 2e-10 + 3e-11*np.cos(np.linspace(0,2*np.pi,1024,endpoint=False)) \
          + 1e-11*np.cos(2*np.linspace(0,2*np.pi,1024,endpoint=False))
A=rfft(au); W=np.ones_like(A,float)
for k in range(len(A)):
    if k>=2: W[k]=0.5
print("mean shift from theta:", np.mean(irfft(A*W,n=len(au)))-np.mean(au))  # ~1e-26
PY

# Matched-e collapse (import solver, calibrate theta==1 mean(e), difference at same e):
# reproduces -0.71%..+0.54% sign-changing sub-1% residual (see section 3c).
```

Paper: `real_research/papers/DSUNRUH_MI_THEORY_2026.md` §4 (kernel), §6.3 (the real MG-impossible door).
