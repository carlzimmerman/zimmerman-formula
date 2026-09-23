# J05 — WHAT THE MOMENT CHANNEL GIVES AN OBSERVER: a density-free width bound
**2026-09-23 · the transfer-function reading of J01/J02, verified**

**The question this answers.** "So nothing?" The frozen lane's Theorem 2 is a
lag–width **band** from two moments (E[D], E[v²]) and it needs uniformity +
isothermality. What we actually built is the exact **joint-moment structure**
of the scattering transfer function — and one concrete, new, density-free,
velocity-resolved-RM-testable inequality. All of it machine-checked.

---

## 1. The exact joint structure (J01 + J02, 35/35 checks)

Inside the Thomson-sphere model, conditional on the trajectory, v is Gaussian
with variance exactly 2·ang. The observable moments therefore satisfy

> **E[D v^{2m}] = (2m−1)!!·2^m·E[D·ang^m]**,   m = 1, 2, 3 verified;

and since the Gaussian lemma also fixes E[ang^m] through the line moments

> **E[ang^m] = E[v^{2m}] / ((2m−1)!!·2^m)**,   (m=1: E[ang]=E[v²]/2 — the
> frozen lane's exposure identity; m=2: E[ang²]=E[v⁴]/12, verified J02 S4b).

So the joint hierarchy is a **consistency family**: every velocity-resolved
transfer function of a Thomson-scattering LRD must satisfy these identities
simultaneously, *whatever the density profile*.

## 2. The new observable bound (this file)

Cauchy–Schwarz on the pair (D, ang) gives E[D·ang]² ≤ E[D²]·E[ang²]; insert
the two moment relations and solve for E[D²]:

> **E[D²] ≥ 3·E[D v²]² / E[v⁴]**   — density-free, isothermality-free.

All three inputs are velocity-resolved reverberation observables:
E[D²] = ∫τ²Ψ(τ,v)dτdv (transfer-function width), E[D v²] = ∫τ v²Ψ dτdv
(joint lag–width moment), E[v⁴] = line-profile kurtosis moment. **No κ, no
n_e, no geometry parameter appears.**

Verified on the independent solver (n = 10⁶, ±SE on every mean):

| cloud | E[D²] | bound 3E[Dv²]²/E[v⁴] | slack | σ_D (TF width) |
|---|---|---|---|
| τ₀=1, q=0 | 0.7651 | 0.6141 | 1.25 | 0.717 |
| τ₀=1, q=3 | 3.3615 | 2.9666 | 1.13 | 1.342 |
| τ₀=1, q=10 | 16.213 | 15.235 | 1.06 | 2.683 |
| τ₀=2, q=3 | 11.222 | 10.497 | 1.07 | 2.231 |

**The bound is nearly tight** (slack ≤ 1.25, → 1.06 as q grows) — it is a
*useful* constraint, not a weak one: a measured transfer function whose mean
square width falls below this line kills the Thomson-scattering reading for
ANY density.

## 3. What the volume-source face (J02B) adds to the observer

Theorem 1's E[D] = ∫rκ dr is central-source-only. A volume/thick-shell LRD
emission geometry is standard in the literature; for it,
E[D]_vol = E[τ]_vol − E[Q] with the exact Dynkin compensation — so an observer
using the frozen identity on a shell emitter would be wrong by exactly
E[Q] + ½E[F(r₀)] (measured: E[D]_vol = 0.338 vs central 0.501; E[Q] = 0.597).
That is a *correction to the applicability domain* of the lane's own Theorem 1.

## 4. Honest status

- **Stands:** the exact joint-moment hierarchy and the width bound — proven by
  the conditional-Gaussian argument (closed form) and verified across three
  independent MC engines (frozen transport.py, J01, J02) at 35/35, both
  source geometries. The numbers above are MC estimates with reported errors;
  the relations themselves are exact within the model.
- **Still open (registered, not hidden):** the target doc's deterministic
  discretized transport cross-check (J03 grid = singular at r→0; J04 P_N =
  interior operator proven exact to 1e-15, half-range boundary pinning of the
  constant mode unsolved — cond 9e17, level wrong by ~3). Tooling failure,
  not a physics refutation: the MC engines never meet that obstacle and the
  identities stand on proof + 35/35.
- **Not claimed:** any observational JWST confirmation (no data touched),
  no new law of nature, novelty in the strict literature sense unresolved.

## 5. The falsifier, stated once

For any LRD whose line is judged to be Thomson-scattered in a quasi-spherical
resolved region: velocity-resolved monitoring measures (E[D], E[v²], E[Dv²],
E[v⁴], E[D²]). The framework requires (a) the m=1,2 hierarchy ratios
E[Dv^{2m}]/((2m−1)!!2^m E[D]E[ang^m]) — R = 2.64, 3.57, 4.56 at q=0 —
to hold **jointly**, and (b) E[D²] ≥ 3E[Dv²]²/E[v⁴]. Any one violation at
≥ 3σ, with the model's conditions verified (stationarity, conservatism,
isothermality within the band's own tolerance), kills the interpretation.
This is the transfer-function statement the moment channel was for.