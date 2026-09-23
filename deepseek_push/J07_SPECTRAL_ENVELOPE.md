# J07 — THE SHARPENED SPECTRAL ENVELOPE OF THE DELAY KERNEL
**2026-09-23 · moment channel, J05 follow-on · 20/20 checks, exit 0**
Files: `J07_spectral_envelope.py` · `.out` · `J07_results.json` (same dir)

**Scope (kept):** inside the Thomson-sphere model; a sharpening of the frozen
lane's Theorem 3, machine-verified on the independent engine. Not an
observational claim — the *envelopes* are what a measured |H(ω)| must respect.

---

## The three envelopes (ω in units of 1/E[D])

| | envelope | where from |
|---|---|---|
| T3 (frozen) | \|H(ω)\| ≥ max(0, 1 − ω·E[D]) | Theorem 3, linear |
| **T3′ (new)** | **\|H(ω)\| ≥ max(0, 1 − ½ω²·E[D²])** | second moment; asymptotically exact at ω→0 |
| **T3″ (new)** | **\|H(ω)\| ≥ max(0, 1 − ½ω²·L),  L = 3·E[Dv²]²/E[v⁴]** | J05 bound substituted; **line-moment-only, density-free** |

Why this is a real gain: cos x = 1 − x²/2 + O(x⁴), so the linear envelope is
asymptotically *weak* at small ω while the quadratic one is *tight there* —
verified: the log–log slope of |1 − ReH − ½ω²E[D²]| vs ω is **3.99** (i.e.
O(ω⁴), the predicted order). T3′ beats T3 for all ω < ω\* = 2E[D]/E[D²]
(measured ω\* = 1.31 for the uniform cloud; at ω·E[D] = 0.5 the quadratic
envelope 0.905 vs linear 0.750 — a 21% tighter floor).

Measured (uniform, central; independent engine, n = 4×10⁵):

| ω | \|H\|_meas | T3 linear | T3′ quadratic | T3″ line-moment |
|---|---|---|---|---|
| 0.25 | 0.9843 | 0.8750 | 0.9761 | 0.9809 |
| 0.50 | 0.9413 | 0.7501 | 0.9045 | 0.9235 |
| 1.00 | 0.8133 | 0.5001 | 0.6179 | 0.6939 |
| 2.00 | 0.5926 | 0.0002 | 0 (clips) | 0 (clips) |

Verified on all four clouds (uniform/q=3/q=10 central, uniform volume):
**20/20 checks** — measured |H| ≥ both envelopes at every ω; T3′ strictly
beats T3 on the finite interval; L ≤ E[D²] holds (J05 re-verified); the
asymptotic slope is ≈ 4 everywhere.

## What the line-moment envelope buys an observer

T3″ is the first of the three to be evaluable **without any assumption about
κ, n_e, or the geometry**: just the measured mixed moments of the
velocity-resolved transfer function (E[Dv²] from joint lag–width data and
E[v⁴] from the line profile) bound the coherence |H(ω)| at every frequency.
The frozen T3 needed E[D] (fair), but its *shape* was linear; the new one
matches the true asymptote. A monster pair: at ω·E[D] = 0.5 the scattering
interpretation keeps ≥ 90% coherence; any instrumental variation suppressing
|H| below 0.90 at that frequency is killing coherent signal — quantifia,ble
before the observation.

## Honest edges

- The envelopes are model-internal (the D used is the model's excess delay);
  the transfer from model observer-delay to real LRD monitoring requires the
  lane's own applicability caveats (THEOREM.md §What cannot be inferred).
- Not claimed: novelty of cos x ≤ 1−x²/2 (elementary); the new content is the
  *moment-chain substitution* L into the Fourier bound and its verification.
- The ω ≥ 2 clipping means the useful regime is ω·E[D] ≲ 1.5 — where T3′/T3″
  are the binding, testable ones.

**Status: J07 LANDED 20/20 — the frozen linear coherence bound is upgraded to
a quadratic, asymptotically exact, line-moment-only envelope.**