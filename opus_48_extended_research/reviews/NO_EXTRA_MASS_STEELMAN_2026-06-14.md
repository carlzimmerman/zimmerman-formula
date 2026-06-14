# Steelman: do galaxy clusters need a SECOND mass component? — the best honest case, on real eRASS1

*Opus-48 extended research, 2026-06-14. Carl's hypothesis: the cluster η≈2 deficit is a methodology/footing
artifact, not evidence for a second (dark) mass component. Tested on its OWN terms, both ways, on the real
eRASS1 (Bulbul+2024, N=9830) with the framework's own a0=9.36e-11 and its own dS-Unruh interpolation. Scripts:
`no_extra_mass_steelman.py`. Quarantine held: a0/Z never asserted derived.*

## Headline
The best defensible combination of honest reducers pulls η from the banked **2.33** (framework interp) /
**2.15** (simple interp) down to **~1.8–2.0**, and the absolute physical floor (every baryon = the full cosmic
fraction, capped) is **~1.7**. It does **not** reach 1. A residual **~65–75% of M_dyn** survives the best honest
case at R500. **Grade: η stays ~2 (mild-reducible at best, ~1.8); the deficit is real at R500, not a footing
artifact — but its *magnitude* is soft (interp + WL-systematic + aperture).**

## The forensic on M500's provenance (the load-bearing fact)
eRASS1 `M500` is a **weak-lensing-calibrated** mass (count-rate ↔ mass ↔ shear scaling; Ghirardini+2024,
Kleinebreil+2024, Chiu+2023), **not hydrostatic**. Consequences:
- M_dyn here is already the *true* (lensing) mass ⇒ **the hydrostatic-bias reducer does NOT apply** to this
  catalog. Non-thermal pressure (X-COP: ~6% at R500) makes *hydrostatic* masses too low; it cannot lower a WL
  mass. A steelman that claims "+10–30% hydrostatic bias cuts η" is **wrong on eRASS1** — that reducer is only
  available to hydrostatic-based analyses (Zhang+2026, Brownstein-Moffat).
- Likewise merger/non-equilibrium boosts don't help: WL doesn't assume equilibrium.

## Both-ways ladder (framework a0=9.36e-11, framework interp g_obs=√(g_bar²+g_bar·a0))
| configuration | η_med | implied 2nd-component (1−1/η²) |
|---|---|---|
| A. banked baseline (gas + 0.2·gas stars) | **2.33** | 82% |
| B. + IGIMF stars/remnants (Zhang+2026, 1.69× ICM) | 1.95 | 74% |
| C. + IGIMF + 15% gas clumping | 1.81 | 69% |
| D. C capped at cosmic f_b (physical ceiling) | 1.90 | 72% |
| E. baryons = FULL cosmic f_b (absolute floor) | 1.69 | 65% |
| F. E but McGaugh a0=1.2e-10 (regular-MOND footing) | 1.51 | 56% |

Interp spread of the capped steelman (D): simple 1.81 / standard 2.03 / deep-MOND 2.06 / framework 1.99.

## Reducers (honest, with sizes) — and inflaters
**REDUCERS (lower η):**
- **IGIMF top-heavy stellar remnants** (Zhang, Zonoozi & Kroupa 2026, PRD, arXiv:2602.06082). Strongest real
  pro-MOND result. On their 46 nearby (z<0.1) clusters with *hydrostatic* M_dyn: ICM-only baryons = **52%** of
  M_dyn (η=1.92); +canonical stars **67%** (η=1.49); +IGIMF stars/remnants/ICL **88%** (η=1.14), called an
  underestimate. Mechanism: super-solar metallicities ⇒ top-heavy gwIMF ⇒ large mass in neutron-star/BH
  remnants currently uncounted. On eRASS1 the same 88/52=1.69× multiplier on ICM cuts η 2.33→**1.95**, NOT to
  1.14 — because (i) eRASS1 M_dyn is the *higher* WL mass, not Zhang's hydrostatic mass; (ii) eRASS1 is
  gas-dominated (median f_gas=0.066) so the stellar boost is proportionally smaller. *Real, big, but
  catalog-limited here.* Size: **−0.39 in η_med (−0.08 dex).**
- **Full cosmic baryon budget within R500.** eRASS1 median f_gas=0.066 = only **42% of cosmic f_b=0.157**; even
  the most massive clusters reach f_gas~0.105 (67% of cosmic). Assuming the *full* cosmic fraction (upper bound)
  gives η→**1.69**. Size: **−0.64 in η_med.** But this is an over-claim: the gas isn't seen in X-ray and only
  16% of clusters even reach the cosmic cap under IGIMF — the missing 33–58% of cosmic baryons within R500 is
  itself the "warm-hot/undetected baryon" hypothesis, not a free reducer.
- **Gas clumping** (+10–20% on M_gas at R500; X-COP <5% corrected). Size: **−0.13 in η_med.**
- **Aperture/outskirts** (Famaey-Pizzuti-Saltas 2024 arXiv:2410.02612; Zhao-type relaxed-cluster profiles).
  The MOND residual is a **cored central excess** with a sharp r⁻⁴⁻⁶ cutoff near ~1 Mpc; residual/ICM ~1–5 at
  0.2–0.3 Mpc → 0.4–1.1 at 2–3 Mpc. Integrated to 2–3 Mpc (~3–4 R500) the residual approaches the ICM mass
  (η→~1.3–1.5). **At R500 (=0.77 Mpc median, where eRASS1 measures) it is still ~2** — the deficit is a
  central/aperture effect, smaller in the outskirts. *Genuine, but doesn't erase η at R500.*

**INFLATERS (raise η) — reported equally:**
- **The framework's a0=9.36e-11 is itself an INFLATER** vs McGaugh 1.2e-10. Lower a0 ⇒ higher η by
  √(1.2/0.936)=**1.13**. So adopting the framework's own footing makes the cluster problem *worse* by +13% than
  regular MOND (2.33 vs 2.07 at baseline). This is the opposite of a footing-artifact rescue: the framework's a0
  cannot be the thing that erases η — it inflates it.
- **The framework's own interp** (√(g_bar²+g_bar·a0)) sits at the HIGH end (2.33) vs simple (2.15); +0.18 in η.
- **AeST oscillatory "negative-mass" contribution:** in the framework's covariant realization (Durakovic-Skordis
  2024) this is a candidate *extra cluster gravity*, i.e. it would *raise* the predicted MOND mass and *reduce*
  η — but it is uncomputed for real clusters, lives in a possibly-unstable regime, and would itself BE the
  second component (a new field). It cannot be banked as "no extra mass."

## a0 used
Framework a0 = c²√(Λ/32π)/... = **9.36e-11** (pure dark-energy footing, ρ_DE/cH_Λ) throughout the ladder; McGaugh
1.2e-10 shown as the rival in rows F and the a0-inflater line. **No analysis used a local/density-enhanced a0**
(the `cluster_a0_from_density_HIS_FORMULA.py` branch, which *would* slash η via a0~√ρ inside overdensities, is a
SEPARATE unforced "Mpc-ambient density" reading — quarantined here, not credited, because it requires an
underived smoothing scale and conflicts with RAR universality). No interpolation onto a non-physical regime: the
sample is 96% deep-MOND (median g_bar/a0=0.037), so all interp functions converge.

## Is there a published analysis where MOND clusters need NO extra mass?
Closest: **Zhang+2026 (PRD)** — η→1.14 (88% baryon/dyn) with IGIMF remnants, "significantly alleviates," and
they argue 88% is a conservative underestimate (faint galaxies + ICL uncertainty could push toward ~1). That is
the genuine pro-MOND steelman and it is real and published. **But** it (a) uses hydrostatic, not WL, M_dyn;
(b) is z<0.1 relaxed clusters with rich galaxy censuses; (c) still leaves ~12% on average. On the WL-massed,
gas-dominated eRASS1 the same physics lands at η~1.9, not 1.1.

## Grade (honest, both ways)
**η stays ~1.8–2.0 under the best defensible combination at R500 — does NOT reach ~1.** The mild-reducible
target (~1.5) is reached only by (F) simultaneously (i) abandoning the framework's a0 for McGaugh AND (ii)
assuming the *full* cosmic baryon fraction is present within R500 — i.e. by giving up the framework's own footing
AND positing the undetected-baryon hypothesis. On the framework's OWN terms (a0=9.36e-11), the floor is η~1.7
even with every baryon at cosmic f_b. **Carl's intuition is partly vindicated and partly not:** the *magnitude*
is softer and more uncertain than "needs 2× more mass" (interp 1.8–2.3; the IGIMF reducer is real and the η
is an aperture-dependent central effect that shrinks in the outskirts), **but a real ~1.8–2× residual survives
the best honest case at R500.** It is NOT purely a footing artifact — and the framework's own a0 *inflates*,
not deflates, it. The honest verdict matches the banked standing (§3a): the cluster deficit is the framework's
heaviest real liability; the only clean route to η≈1 is a genuine second component (the framework already needs
one: the AeST Q-field as dust, or eV-scale sterile neutrinos, or the full undetected-baryon census).

**Sources:** Bulbul+2024 A&A 685 A106 (eRASS1); Ghirardini+2024, Kleinebreil+2024, Chiu+2023 (WL mass calib);
Zhang, Zonoozi & Kroupa 2026 PRD (arXiv:2602.06082, IGIMF remnants); Famaey, Pizzuti & Saltas 2024
(arXiv:2410.02612, lensing residual profiles); Eckert+2019 (X-COP non-thermal pressure ~6% at R500);
Durakovic & Skordis 2024 JCAP 04 040 (AeST oscillatory regime).
