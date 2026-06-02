# Complete parameter-space review of the evolving-a₀ framework

**Date:** 2026-06-02 · *honest map of both axes — what is free/derived (theory) and where (if
anywhere) the framework is distinguishable from ΛCDM (observation). Backed by the literature and
by `reviews/parameter_space_map.py`.*

This closes out the five options on the table (① coherence/distinguishability, ② the z≳4 frontier,
③ deriving Z, ④ the second-order CMB, ⑤ the red-team as a methods contribution). The bottom line:
**the framework occupies one narrow, untested corner of parameter space; everything else is
degenerate with ΛCDM, fitted, or already leaning the other way.**

---

## Part I — Observational parameter space: distinguishable from ΛCDM? (① + ②)

The capstone (`NOVELTY_AND_DEGENERACY.md`) showed the *amplitude* of apparent-a₀ evolution is
degenerate. The full map of every observable:

| observable | framework | ΛCDM | current data | discriminates? |
|---|---|---|---|---|
| RAR amplitude / apparent a₀(z) | rises ∝ E(z) | rises (halo+baryon evol.) | both ≈×3 to z=2.3 | **NO — degenerate** (Magneticum, NIHAO) |
| RAR **intrinsic scatter** | ≈0 (a₀ universal) | grows with z | grows 0.13→0.19 dex | **YES → currently favors ΛCDM** |
| a₀ universality at fixed z | universal | galaxy-dependent | **contested** (Rodrigues+18) | YES → against / contested |
| EFE (host dependence) | yes* | none | seen locally (MOND) | YES — *but framework's EFE withdrawn (category error)* |
| z≳4 multi-channel coherence | one E(z) | uncertain | **no data yet** | **the only open window** |
| compact high-z galaxies | Newtonian (boost≈0) | dark matter | de Graaff M_dyn/M⋆≈40 | predictions don't apply (regime) |

**① The discriminators currently lean ΛCDM.** ΛCDM hydro simulations (Magneticum, Tian et al. 2022;
NIHAO, Dutton et al. 2019) reproduce the RAR *and* its amplitude evolution, so the one observable
that exists is degenerate. The observable that *does* discriminate — the **intrinsic scatter** —
goes the wrong way: MOND with a universal a₀(z) wants ≈0 intrinsic scatter, but the measured scatter
**grows with redshift** (0.13→0.19 dex), exactly as ΛCDM predicts. And the *universality* of a₀
itself is contested locally (Rodrigues et al. 2018 found individual-galaxy a₀ values mutually
incompatible; McGaugh/Kroupa dispute the analysis). The framework's own would-be discriminator, the
EFE, was withdrawn in round 2 as a category error.

**② The z≳4 frontier is genuinely unexplored — and it is the only open window.** High-z kinematic
RAR/a₀ measurements exist only to z≈2.4 (six galaxies; Genzel/Übler-type samples). Beyond that there
is **no data**. So the one region where evolving-a₀ could still be distinguished — z≳4, where E(z)'s
steep rise might outrun ΛCDM's apparent-a₀ drift — is untested in either direction (I previously
asserted they "diverge" there; honestly, it is simply *unmapped*).

**The regime caveat narrows even that window.** The a₀(z) boosts are deep-MOND (g_bar < a₀). At
z=6, only extended/low-mass galaxies (R≳1 kpc, M⋆≲10⁹) are deep-MOND; compact, massive ones — the
headline JWST targets — are Newtonian, where a₀(z) barely matters. So the test applies to
**extended high-z galaxies only**.

## Part II — Theoretical parameter space: what is free? (③ — can Z be derived?)

**③ The coefficient Z cannot be derived — it is one free O(1) number among several.**
With a₀ = k·c√(Gρ_c) = cH/Z and Z = √(8π/3)/k, the √(8π/3) = 2.894 is exact Friedmann physics; **k
is free**:

| reading | k | Z | status |
|---|:--:|:--:|---|
| Schwarzschild (literal) | 1.45 | 2.00 | wrong (a₀ ~2.9× too big) |
| Milgrom a₀≈cH₀/2π | 0.461 | 6.283 | posited (1983) |
| Verlinde a₀≈cH₀/6 | 0.482 | 6.000 | posited (2017) |
| **framework, k=½** | 0.500 | 5.789 | posited |
| 29/5 | 0.499 | 5.800 | fits data better, ~0 bits |

Every route that was tried to *pin* k — Bekenstein–Milgrom thermodynamics (Bridge 2),
horizon-entropy counting, the literal Schwarzschild identification — **fails**. The framework's k=½
is a clean choice but not unique and not the data's best. **Verdict: free.**

**The exponent p is fitted, not derived.** a₀(z)=a₀(0)E(z)^p with p the choice of which density a₀
tracks: p=0 (√Λ, constant), p=1 (√ρ_total ∝ H, the premise), p=1.5 (√ρ_matter). The data prefer
p≈0.80±0.17 — a **~2σ, single-point-driven** preference for p≈1 over the alternatives (Piece 3).
**Verdict: fitted.**

So the theory axis has **two free O(1) parameters** (k and p), neither derived, plus the choice of
coupling form (a₀ ∝ θ rather than ∝ √Λ).

## Part III — The open technical frontier (④)

**④ The second-order CMB is the one un-run quantitative check.** Linear CMB-safety is exact (a₀ is
O(δφ³); δq⁰⁰=0 — Piece 7). At second order a₀ acts, and at recombination it is ~2×10⁴ larger and the
acoustic scales sit in the deep-MOND (𝒴→0) corner where the 𝒴^{3/2} non-analyticity makes the
estimate (~0.01–0.1%) **soft**. A full second-order Boltzmann run (a CLASS/hi_class patch) is
required to confirm safety or bound the running from Planck — `nonlinear_cmb_scoping.py` specifies
it; it has not been run. The galaxy-scale aether back-reaction (Piece 5, leading-order only) is the
other open technical piece.

## Part IV — The complete ledger, the viable region, and the methods contribution (⑤)

**The viable region — the entire testable content — is one corner:** *z≳4, extended (deep-MOND)
galaxies, the cross-channel coherence and tightness of the RAR.* If, there, M_dyn/M⋆∝√E **and**
σ∝E^{1/4} **and** the BTFR zero-point∝−log E move together off a single E(z), *and* the intrinsic
scatter stays small (universal a₀), that is the signature ΛCDM halo evolution does not coherently
forge. Everywhere else the framework is degenerate, fitted, or disfavored. That corner has **no data
yet**, and the regime caveat means it requires *extended*, not compact, targets.

**Honest final verdict.** On the theory axis: two free O(1) numbers, none derived, atop a known
coincidence and a tuned host (AeST). On the observation axis: degenerate with ΛCDM on the only
existing observable, leaning ΛCDM on the discriminators that exist, and testable only in one
unobserved corner. The framework is a **coherent, CMB-safe, falsifiable variant of relativistic
MOND with no current distinguishing evidence** — a clean hypothesis parked at the edge of testability.

**⑤ The genuine transferable contribution is the method, not the model.** The most reusable output
of this whole effort is the *falsification workflow* applied to a numerology-driven "theory of
everything": (i) compute the **false-discovery rate** of the formula search (`false_discovery_rate.py`)
— it hit ~20% of arbitrary O(100) targets to the quoted precision, ⇒ ~0 bits; (ii) restate every
"match" in **units of the measurement's σ**, turning "0.004%" into a 10⁵σ miss; (iii) **jackknife and
add the inter-method systematic** to a small data fit (5σ→2σ); (iv) check **novelty and ΛCDM
degeneracy** against the literature before claiming a result. This is a clean, worked template for
self-falsification — and it is the part of this repository most worth writing up for others.

---

## References

- Milgrom 1983 (ApJ 270, 365); 2014 (PRD, arXiv:1412.4344, evolving a₀∝cH).
- Skordis & Złošnik 2021 (PRL 127, 161302, AeST).
- Tian et al. 2022 (MNRAS, arXiv:2206.04333, Magneticum: apparent a₀ ×3 to z=2.3).
- Dutton et al. 2019 (MNRAS, NIHAO XVIII: RAR in ΛCDM).
- Rodrigues et al. 2018 (Nat. Astron., arXiv:1806.06875, non-universal a₀; contested by McGaugh+).
- McGaugh, Lelli & Schombert 2016 (PRL 117, 201101, SPARC RAR; intrinsic scatter).
- MUSE-DARK III 2026 (A&A, RAR evolution + scatter to z≈0.9).

*Reproduce:* `python reviews/parameter_space_map.py`. Cross-refs: `NOVELTY_AND_DEGENERACY.md`,
`redteam_the_puzzle.py`, `redteam_round2.py`, `stresstest_piece3_evolution.py`,
`nonlinear_cmb_scoping.py`, `false_discovery_rate.py`.
