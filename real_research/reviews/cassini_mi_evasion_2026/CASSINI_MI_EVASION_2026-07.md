# The modified-INERTIA realization evades the Cassini-Q2 wall — 2026-07-07

**Verdict: EVADES (0/3 refuted; hand-reruns confirm).** The framework's modified-INERTIA realization produces an inner-solar-system quadrupole far below the Cassini bound, *derived* (not assumed), and the suppression is *forced* by the framework's own ν. This converts the Cassini standing from "the realization inherits a large quadrupole wall" to "the MI limb evades; the written MG limb does not."

## The result (both footings, hand-verified)

Cassini bound: Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻² (Park+ 2026, arXiv:2602.17884); 2σ upper ≈ 5.2×10⁻²⁷.

The anisotropic galactic external field (a_ext = 2.29 a₀, fixed direction) acting through the framework's non-local MI kernel at Saturn (deep-Newton, y = 7.0×10⁵) induces, by explicit Legendre decomposition (`verify_order.py`, a_ext-scaling confirmed):

| multipole | order in a_ext | magnitude (as accel/a) | vs Cassini 2σ ceiling |
|---|---|---|---|
| **l=1 dipole** | first (power 1.000) | 1.5×10⁻²⁸ s⁻² (canon) / 3.3×10⁻²⁹ secular | 0.03× (~0.015σ) |
| **l=2 quadrupole** (what Cassini constrains) | second (power 2.22) | **7.4×10⁻³⁴ s⁻²** | ~10⁻⁷× |

Both below the ceiling; the true l=2 quadrupole by ~7 orders. Robust across e = 0–0.5, all EFE directions φ_gc, a_ext = 2.0–2.48×10⁻¹⁰, both footings. Worst corner (inflating the O(1) prefactor, steeper true gradient): 3.9×10⁻²⁸ s⁻² = 0.076× ceiling — still ~13× to breach.

**Correction to the compute headline:** the compute script's "~2.7×10⁻²⁹ Q2" is the l=1 **dipole** scale; a uniform dipole force does not secularly precess the orbit the way a quadrupole does. The genuine l=2 quadrupole is the 7.4×10⁻³⁴ number. Reported as separate quantities here — the relabel makes EVADES *more* secure, not less.

## Why it's derived and forced, not manufactured

- **Derived:** the anisotropic response was obtained by Legendre-decomposing δA(ψ) = g_N·[1/μ_fw(|A_eff|/a₀) − iso] and confirmed by a_ext-scaling (l=1 first-order, l=2 second-order). The residual quadrupole the skeptics demanded was computed, not set to zero.
- **Forced:** the load-bearing suppression is the deep-Newtonian ν−1 = a₀/(2 a_int) = 7.1×10⁻⁷ at Saturn — a consequence of the framework's RAR ν=√(1+1/y), not a tunable kernel choice. In MI the Sun's field stays exactly Newtonian (no phantom-density quadrupole); the EFE enters only Saturn's inertial response. This is the derived realization of Milgrom 2009's (MNRAS 399.474) "no inner-SS Q2 anomaly in modified inertia."
- **DC-protection holds but is not needed:** the θ (k≥2) kernel residual is ~10⁻⁴⁰ s⁻²; the evasion comes from the ν−1 suppression, so the DC-protection/k=2 objection does not overturn it.

## The honest limit (do NOT overclaim)

**This is not a general "the framework passes Cassini" clearance.** The evasion holds *only* at the modified-INERTIA premise. The framework's *written*, CMB-safe covariant realization is AeST / Blanchet–Skordis khronon — which is modified **gravity** and **still inherits the wall**: D4 (own-ν) = +6 to +14σ, A2 (khronon) ~6–9σ. The MI escape requires the still-**unwritten covariant MI completion**.

So the durable standing is: the MI *core* is Cassini-safe (and this suppression is exactly what any covariant MI completion must reproduce), while the MG *limb* the framework currently has written is not. The Cassini wall is now a wall *against the MG realization*, evaded by the MI realization — and the MI completion that evades it is the same object the sign wall (no passive-nonlocal MOND-signed kernel) makes hard to write.

*Both footings carried throughout. The win was derived and survives the dipole-vs-quadrupole relabel; the caveat is stated so it is not read as a general clearance.*
