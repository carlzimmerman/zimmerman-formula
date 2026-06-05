# The AeST mass scale 1/μ ~ 1 Mpc settles both framework-relevant doors — in opposite directions

*C. Zimmerman, 2026-06-05. "Keep pushing open doors." Pursuing the two framework-relevant exposures into the actual
2024 AeST literature (which had more computed than my earlier "uncomputed" scoping assumed) turned up a single
number — the AeST mass scale `1/μ ~ 1 Mpc` — that **answers both at once, oppositely**. This is a real finding, with
real caveats, reported straight. Companion grounding: the scale hierarchy in `reviews/cassini_quadrupole_framework.py`
neighborhood (computed inline below).*

## The one number

AeST (Skordis–Złošnik 2021) is **not** plain QUMOND. Its quasi-static weak-field limit (Verwayen, Skordis, Złošnik
2024, MNRAS **531**, 272, arXiv:2304.05134) is a **coupled two-potential** system `(Φ, χ)` carrying a **mass term
`μ²Φ`** absent in MOND/TeVeS ("tends to TeVeS as μ → 0") and an interpolation/screening parameter `β₀`. The mass
scale is pinned by the theory's own requirements:

> `μ ≲ 1 Mpc⁻¹` (so the low-momentum instability lives only on cosmological scales); Skordis–Złošnik require
> `m²/f_G ≲ 1 Mpc⁻²`. **⟹ `1/μ ≳ 1 Mpc`.**

The `μ²Φ` term matters where `(μr)² = (r / μ⁻¹)² ≳ O(1)`. With `1/μ ≈ 1 Mpc`:

| system | r | (μr)² | μ²Φ term |
|---|---|---|---|
| Solar System (~50 AU) | 2.4×10⁻¹⁰ Mpc | **6×10⁻²⁰** | OFF (~40 orders down) |
| galaxy (~10 kpc) | 0.01 Mpc | 10⁻⁴ | OFF |
| **galaxy cluster (~1 Mpc)** | 1 Mpc | **~1** | **ON** |
| cluster outskirt (~3 Mpc) | 3 Mpc | ~9 | ON |

**`1/μ ~ 1 Mpc` sits exactly at the cluster scale.** That single fact routes the two doors oppositely.

## Door B (clusters — the framework's heaviest liability): a real AeST mechanism, with a real caveat

**Opened, partway.** At cluster scales the `μ²Φ` term switches on and AeST develops an **oscillatory regime** beyond
Newton/MOND in which the radial-acceleration relation "**displays a peak, then drops below the MOND expectation, as
if there were a negative mass density**" (Durakovic & Skordis 2024, JCAP 04 040, arXiv:2312.00889 — *"isothermal
spheres and curiosities"*). The authors note **"similar features of the galaxy-cluster RAR have been reported… this
illustrates the potential of AeST to address the shortcomings of MOND in galaxy clusters."**

So the framework's heaviest liability has a **genuine, AeST-intrinsic candidate** that ordinary MOND lacks — extra
cluster gravity from the `μ²Φ` structure, switched on at the right scale, leaving galaxies as pure MOND. **But it is
not a clean win:**

- **Stability caveat (serious).** The oscillatory regime involves **negative-energy-density condensates**, and the
  AeST literature itself flags the model as **"expected to be unstable in this oscillatory regime"** (the weak-lensing
  confrontation, Mistele et al. 2023, A&A 676 A100). Whether this is a slow (cosmological) or fast instability for
  *cluster* configurations is unsettled — but the mechanism lives in a regime the theory's own authors mark as
  problematic. That is the honest status: a candidate, not a cure.
- **Quantitative caveat.** Only isothermal toy spheres so far; "a full quantitative comparison with observations will
  require going beyond the isothermal case." The eRASS1 `η ≈ 2` deficit is **not yet shown** to be closed.

**Net for Door B:** the cluster problem moves from "MOND simply fails, needs an *ad hoc* second component" to "AeST
has an *intrinsic* mechanism that qualitatively matches observed cluster-RAR structure, but sits in a possibly-
unstable regime and is not yet quantitative." Better than before; not resolved.

## Door A/C (the Cassini quadrupole — the near-term exposure): the tension stands, firmed up

**Closes unfavorably for the easy escape.** My earlier `CASSINI_QUADRUPOLE_CONSTRAINT.md` left the escape as "AeST
`K(𝒬)`/`μ` screening, uncomputed — could go either way." The μ-scale kills the optimism: at 50 AU, `(μr)² ~ 6×10⁻²⁰`,
so the `μ²Φ` term — AeST's *only* natural screening structure — is **utterly negligible in the Solar System**. AeST
there reduces to pure QUMOND, and **inherits the Desmond+2024 → 2026 quadrupole tension (3–15σ) in full**. The
remaining escape narrows to the interpolation/screening parameter `β₀` or the `χ`-field doing something special in the
external-field configuration — but `β₀` is **pinned by the SPARC RAR fit** (it sets the transition sharpness), which
is exactly the quantity Desmond shows is too gradual for Cassini. **The Desmond tension transplants into `β₀` intact.**

**Net for Door A/C:** the Solar-System quadrupole exposure is **firmer**, not softer — the natural AeST screening
scale is ~10 orders too large to help, and the surviving knob is the one the RAR already constrains. This is the
framework's most pressing near-term problem and it is **not** evaded by AeST's extra structure.

## The unifying picture (and why it's honest, not convenient)

One scale, `1/μ ~ 1 Mpc`, set by the CMB/cosmology fit — **not** chosen for either of these tests — lands so that:

```
   Solar System (AU)   <<   galaxies (kpc)   <<   clusters (Mpc)
   pure QUMOND              pure MOND              μ²Φ switches on
   → Cassini EXPOSED        → MOND works           → cluster mechanism (but unstable?)
```

The structure that could fix the framework's heaviest liability (clusters) is the *same* structure, at the *same*
scale, that is **constitutionally unable** to relieve its most pressing exposure (Cassini). That is not a result one
would design — it falls out of the one mass scale — which is why it is worth recording as found:

- **Cluster liability:** downgraded from "fails" to "has an intrinsic candidate mechanism, caveated by a possible
  instability and no quantitative fit yet." *Genuinely better.*
- **Cassini exposure:** upgraded from "uncomputed, maybe evadable" to "AeST inherits it in full at the Solar System;
  escape narrows to the RAR-pinned `β₀`." *Genuinely worse.*

**Updates owed:** `CASSINI_QUADRUPOLE_CONSTRAINT.md` (escape narrowed to β₀, μ-screening excluded by scale);
`FRAMEWORK_EMPIRICAL_STANDING.md` §3a (cluster row — add the AeST μ²Φ candidate + instability caveat);
`THE_NEXT_CALCULATION_aest_quasistatic.md` (the μ²Φ screening sub-question is now *answered* — it doesn't screen the
SS — so step 2 reduces to "can β₀/χ alone thread RAR+Cassini?", a sharper and more pessimistic question).

**Sources:** Skordis & Złošnik 2021, PRL 127 161302 · Verwayen, Skordis & Złošnik 2024, MNRAS 531 272
([arXiv:2304.05134](https://arxiv.org/abs/2304.05134)) · Durakovic & Skordis 2024, JCAP 04 040
([arXiv:2312.00889](https://arxiv.org/abs/2312.00889)) · Mistele, McGaugh, Schombert 2023, A&A 676 A100
([arXiv:2301.03499](https://arxiv.org/abs/2301.03499)) · Desmond, Hees, Famaey 2024, MNRAS 530 1781 · arXiv:2602.17884.
