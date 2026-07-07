# Does the de Sitter bath FORCE the memory time τ_mem? (both-ways)

**Date:** 2026-07-07
**Script:** `real_research/reviews/dsunruh_tau_mem.py` (exit 0), reusing the committed
validated kernel and the committed dwarf door `dwarf_sigma_mi_final.py`.
**Question:** The dwarf σ-hysteresis at fixed galactocentric radius is a genuine,
MG-impossible door (MG gives σ = f(r) single-valued; MI memory makes σ(r) double-valued
inbound-vs-outbound). Its *magnitude* is hostage to the memory time τ_mem. Does the dS
(Gibbons-Hawking) bath FORCE τ_mem — or does the door-sized value (τ_mem ≈ 1/ω_internal)
enter only through the Milgrom-1994 averaging-bandwidth postulate?

---

## VERDICT: NOT FORCED

**τ_mem is NOT bath-forced.** The dS bath forces the memory kernel's *form* (Lorentzian
single-pole) and its DC weight (√2), but it does **not** force the *corner location*
ω_c = 1/τ_mem. The door-sized value τ_mem ≈ 1/ω_internal ≈ 0.4 Gyr is delivered *only* by
the Milgrom-1994 "internal orbit = averaging bandwidth" postulate, which the paper's own
sec. 4 (line 110) already flags as not derivable from the correlator. This is a *derived*
negative, not an assumed one: the code sets `FORCED=False` by default and flips it True
only if a bath-native timescale matches 1/ω_internal within 3×. Neither does — the raw
dS correlator misses by **44×** (too slow) and the framework's own forced kernel pole (d1)
misses by **~220×** (too fast). The verdict is robust even if that match-window were
widened to ~40×.

---

## The argument (fluctuation-dissipation, done honestly)

θ(y) = √2 / (1 + (√2−1)y²) is a function of the *ratio* y = ω_ext/ω_int and is therefore
scale-free in y. A frequency response and a time-domain memory kernel K(t) are Fourier/
Laplace pairs, so τ_mem is pinned **iff** the *absolute* corner frequency ω_c is pinned.
The whole question reduces to: what physical input fixes ω_c?

**FDT construction.** Build K(t) from the dS worldline Wightman function
W(u) = −(κ²/16π²)/sinh²(κ(u−iε)/2), κ = 2πT_dS = H_Λ. By fluctuation-dissipation the
dissipation (memory) kernel is the retarded response built from the spectral density
ρ(ω) — the odd/commutator part of FT[W]. Its **decay rate is set by the poles of ρ**, i.e.
the large-|u| *envelope* of W (1/sinh² → 4e^{−κ|u|}), **not** by the amplitude prefactor.

- Numeric envelope fit: d ln|W|/dt = −1.8074e−18 s⁻¹, i.e. **rate/κ = 1.000047** — confirms
  K(t) ~ e^{−κ|t|} to 1e−4.
- This forces the Lorentzian *form* and the *existence* of a single corner, and places the
  **correlator-native corner at ω_c = κ = H_Λ** → τ_mem = 1/κ = **17.53 Gyr (Hubble scale)**.

**FD-soundness (the one real attack surface, closed).** The envelope is read from |W| (the
*noise* part). A referee could object that the *dissipation* kernel (the commutator part
Im W) is what the equation of motion contains, and that it might have an in-band spectral
feature near the orbital frequency that secretly rescues τ_mem ≈ 1/ω_orbital. Ran directly:
the commutator kernel Im W decays *independently* at rate/κ = 1.0001, and the FT of 1/sinh²
has its **nearest pole to the real axis at the lowest Matsubara frequency = κ** (poles
spaced by κ; none at any orbital frequency). ρ(ω) is smooth/Planckian at galactic orbital
frequencies, so evaluating it there yields a damping *coefficient*, not a new memory time.
Raw-correlation-time and dissipation-kernel-decay **coincide at 1/κ** precisely because the
bath is thermal with no in-band resonance — no conflation occurred. The ~17.5 Gyr is
genuinely the dissipation-kernel decay.

**The bath never hands over ω_c = ω_internal.** FDT correctly kills the naive "cosmological
Hubble memory" worry *as a matter of principle* (kernel decay is a spectral-density
property, not the raw correlation time) — but here the spectral density's pole simply *is*
at κ, so the bath-native answer is genuinely ~Hubble.

---

## Which timescale sets τ_mem? Three candidates, none bath-selected

| # | source | ω_c | τ_mem | door reading |
|---|--------|-----|-------|--------------|
| 1 | internal dynamical 1/ω_int (Crater II) | ω_internal | **0.398 Gyr** | door PEAKS (~15%) — but this is the **POSTULATE** |
| 1′| internal dynamical 1/ω_int (Antlia II) | ω_internal | 0.491 Gyr | door peaks |
| 2 | raw dS correlator 1/κ = 1/H_Λ (FDT decay) | κ = H_Λ | **17.53 Gyr** | τ ≫ P → fully mixed → **door dies** |
| 3 | framework's own d1-forced kernel pole v2 | 2.7× band-top | **1.79 Myr** | τ ≪ P → no retained memory → **door dies** |

ω_internal sits **between** the two bath-derived scales and coincides with **neither**:
1/κ is 44× too slow, v2 is ~220× too fast. Only the Milgrom-1994 averaging-bandwidth
postulate places ω_c at ω_internal.

**Honest wording on candidate 3 (per adversarial review):** what is shown is that the
framework's **one d1-forced pole** lands above the galactic band — NOT that the kernel can
have *no* pole near ω_internal. The d1 inverse problem itself flags the off-circular /
multi-pole completion as *underdetermined*; an untested dominant pole could in principle
sit lower. That untestedness is itself *why* τ_mem is not forced. The Myr figure is also
conditional on the honest galactic-band edges (44–3008 H₀) and the 0.079-dex universality
budget; a different budget shifts v2 within the above-band window but never down to
ω_internal.

---

## Door magnitude — the honest range (Crater II & Antlia II)

Because τ_mem is not bath-forced, no single door magnitude can be pinned. Reported at each
candidate timescale, **and bracketed over kernel memory-order** (framework √2 single-pole
vs. 2-pole θ₀=2, y⁻² tail — the Fourier pair whose DC weight differs but whose corner
*location* does not):

| dwarf | τ_mem source | τ (Gyr) | √2 peak | 2-pole peak |
|-------|--------------|---------|---------|-------------|
| Crater II | dS correlator 1/κ | 17.53 | 1.4% | ~0% |
| Crater II | d1 pole 1/v2 (above-band) | 0.002 | 0.2% | ~0% |
| **Crater II** | **internal 1/ω_int (POSTULATE)** | **0.398** | **17.7%** | **7.0%** |
| Antlia II | dS correlator 1/κ | 17.53 | 1.1% | ~0% |
| Antlia II | d1 pole 1/v2 (above-band) | 0.002 | 0.1% | ~0% |
| **Antlia II** | **internal 1/ω_int (POSTULATE)** | **0.491** | **13.1%** | **3.6%** |

**Honest door range:** ~0% (at either bath-derived timescale) up to **7–18% (Crater II)** /
**4–13% (Antlia II)** — and only at the postulate τ = 1/ω_int. Note the memory-order
bracket nearly *halves* the peak (√2 → 2-pole), so even conditional on the postulate the
magnitude carries a factor-~2.5 kernel-order uncertainty on top of the τ_mem uncertainty.

---

## What WOULD force it

An **off-circular / multi-frequency completion** of the induced-inertia kernel that shows
the response's *dominant* pole lands at ω_internal. The d1 inverse problem explicitly flags
this off-circular completion as underdetermined — that freedom is exactly where the corner
location (and the η(β) anisotropy) live. Absent that completion, τ_mem is free.

Alternatively — and this is the productive reading — the **door magnitude is a proxy
measurement of ω_c**. A positive fixed-radius σ-hysteresis detection in Crater II / Antlia II
would *empirically* place the corner at ω_internal, resolving the postulate the theory cannot
currently derive. The door is a measurement of the corner, not a prediction from it.

---

## Biggest caveat

The FDT decay is read from the *asymptotic* envelope of W (a single-pole reduction). A
two-pole memory shifts the *DC weight* (hence the magnitude, as the table's √2→2-pole column
shows) but **not** the corner *location* — so the NOT-FORCED verdict is robust to memory
order, while the door *magnitude* is not. The single load-bearing caveat is that "candidate 3
kills the door" rests on the *one* d1-forced pole; the multi-pole off-circular completion is
untested and is the sole place a bath-forced ω_c ≈ ω_internal could still hide.

---

## Does this close the dwarf door into a dated prediction?

**No — it leaves the door quantitatively OPEN.** The door's *existence, sign, and
MG-impossibility* (double-valued σ(r) for any nonzero memory) remain genuine and firm. But
its *magnitude* is not a pinned number: it ranges from ~0% (bath timescales) to a
postulate-and-kernel-order-dependent 4–18%. τ_mem is **not** bath-forced, so the framework
cannot presently emit a falsifiable dated σ-hysteresis amplitude. The door is real and
MG-impossible; it is a **proxy measurement of the corner frequency**, not a quantitative
prediction — until the off-circular kernel completion (or a σ-hysteresis detection) fixes ω_c.
