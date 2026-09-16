# G151 — THE TEMPERATURE LADDER: the framework's three temperatures, stated

**Status:** 2026-09-16. Stated-statement lane — no new physics, every number
reproduced from its registered lane (`G151_temperature_ladder.py`, all checks
reproduce the registered values). The framework's thermodynamics in one place:
ONE velocity scale (the triad's σ), THREE temperatures (phase / free-dust /
baryonic gas), and an honest account of which of them any instrument can reach.

---

## 1. THE THREE TEMPERATURES

**(a) The equilibrium phase** (the phantom, ~1% of Ω_dm, inside the EFE line)

    T = m σ²/k_B        at m = 5 keV, σ = 119.2 km/s (the triad virial,
                        σ² = (1/2)√(G M_b a₀), mass-free: G091/G03G)
    T_a = 9.17 K        (direct recompute 9.1744 K; registered band
                        9.17–10.07 K across the two a₀ footings, G084)

Mass-free in T/m: T/m = σ²/k_B = **1.83–2.01 mK/eV** (registered constant,
G084/G116) — the dynamics (the DE-anchored virial σ) sets the temperature;
the particle mass enters only as a linear factor.

**(b) The free dust's kinetic temperature** (~99% of Ω_dm, outside the EFE line)

    T = m v_th²/k_B     the unequilibrated phase; no relaxation to σ
    T_b(z=3) = 2.04e-5 K    (m = 5 keV, v_th = 0.178 km/s; registered
                            2.0436e-5 K at 3.3 keV / 1.187e-5 K at 5.7 keV,
                            G116 A2, G093 A1)
    T_b(z=0) = 1.28e-6 K     (v_th = 0.0548 km/s at 3.3 keV, G093)
    T_b ∝ (1+z)²        v_th ∝ a⁻¹ — the expansion redshifts the
                        free-streaming momentum; T(z=3)/T(z=0) = 16 exactly

**(c) The baryonic gas temperature** (the ICM / ISM — the *same* velocity
scale, the standard-model coupling)

    T = μ m_p σ²/k_B    μ = 0.6 (G075/G109 registered)
    at the SAME σ as (a):   T_c = 89.0 eV = 1.03e6 K
    at the cluster's triad σ (the "3.6 keV-class" rung):
        σ_pred = (G M_b a₀)^(1/4)/√2, M_b(R500; A85) = 1.109e14 M☉
              → σ = 766.1 km/s → T = 3.68 keV
        G008/STATE.md registered σ = 809 km/s ("T = 809 km/s from zero
              parameters") → T = 4.10 keV        (3.6 keV ↔ σ = 758 km/s)
    observed (X-COP kTvir median, 12 clusters, Eckert+17): 6.17 keV
        ↔ σ_gas,1D = √(kT/μ m_p) = 992 km/s (G109's cross-instrument
        equipartition: σ_gal/σ_gas,1D = 0.998 median, rms 0.062 dex)

**THE LADDER — the same dynamical σ, three temperatures set by the sector's
mass and coupling:**

| rung | formula | value | set by | velocity scale |
|---|---|---|---|---|
| (a) phase | m σ²/k_B | **9.17 K** (5 keV; T/m = 1.835 mK/eV) | sector mass m (linear; T/m mass-free) | σ = 119.2 km/s (triad, mass-free) |
| (b) free dust | m v_th²/k_B | **2.04e-5 K** (z=3), ∝ (1+z)² | expansion (v_th ∝ a⁻¹) | v_th = 0.178 km/s (5 keV) — never σ |
| (c) baryonic gas | μ m_p σ²/k_B | **89 eV** at galaxy σ; **3.6–4.1 keV** cluster triad σ; **6.17 keV** observed | coupling μ m_p (SM baryons) + dynamics σ | σ = 766–809 km/s triad (A85-class); σ_1D = 992 km/s observed |

**The ratios (computed on the committed numbers):**

    a/b = T_a / T_b(z=3)     = 4.49e5        the registered decoupling ratio
                                             (G116 A2: "4.5e+05x": the
                                             equilibrium equilibrates at the
                                             virial T; the dust never does)
    c/a = T_c / T_a          = 1.126e5       = μ m_p / m — an EXACT identity
                                             at any equal σ (5.63e8 eV / 5 keV);
                                             the coupling-to-mass ratio in one
                                             number
    c/b = T_c / T_b(z=3)     = 5.06e10       at equal σ (galaxy footing)
    c/cluster over a:        4.65e6;   c/cluster over b(z=3): 2.09e12

*Registry correction, stated honestly:* the order-of-magnitude glosses in the
lane brief (c/b ~ 1e9, c/a ~ 1e5, a/b ~ 1e4) reproduce on the committed
numbers only partially — **c/a ~ 1e5 is right** (it is the exact mass ratio
μ m_p/m), but **a/b = 4.49e5** (the registered 4.5e5 decoupling ratio, not
1e4) and **c/b = 5.06e10** (equal-σ footing; 2.09e12 at the cluster rung, not
1e9). The ladder below uses the computed values.

## 2. THE STATEMENT — the theory's temperature bookkeeping in one table

**ONE velocity scale:** the triad's σ. The same dynamical dispersion appears
in every rung: the equilibrium's isotherm σ = 119.2 km/s (galaxy) /
766–809 km/s (cluster triad), the gas's σ at equipartition = the galaxies'
σ (G109: σ_gal/σ_gas = 0.998), and the dust's *non*-equilibrium v_th, which is
the one exception by construction (it never reaches σ — that is what makes it
dust).

**THREE temperatures** — which physical switch sets each:

| rung | temperature | set by | why | status on the record |
|---|---|---|---|---|
| (a) phase | T = m σ²/k_B | **the mass** | mass enters linearly, T/m mass-free: the dynamics picks σ, the mass converts it to K | 9.17 K @ 5 keV; T/m = 1.835 mK/eV registered constant (G084/G116) |
| (b) dust kinetic | T = m v_th²/k_B | **the expansion** | v_th ∝ a⁻¹ → T ∝ (1+z)²; no relaxation channel above the EFE line (G093 E1) | 2.04e-5 K (z=3) → 1.28e-6 K (z=0); c_s² = 5.3e-13 (z=3, G093 C3) |
| (c) baryonic gas | T = μ m_p σ²/k_B | **the coupling** | the gas is the standard sector in the same well: μ m_p/m = 1.13e5 = c/a exactly | 3.6–4.1 keV triad rung; 6.17 keV observed median (G075/G109/G095) |

Bookkeeping, complete: **one velocity scale, three temperatures — the mass
sets the phase temperature, the coupling sets the gas temperature, the
expansion sets the dust's kinetic temperature.** No fourth temperature exists
in the framework; every T in the theory is one of these three.

## 3. THE CONSEQUENCE — observationally inert, and the honest rung census

**Why (a) 9.17 K is observationally inert:** the equilibrium phase has no
radiation channel (no EM coupling — direct-detection class nulls by
construction, THEORY.md 8, G093 V4) and no collision channel (collisionless
by construction; it relaxes only through the scalar-mediated force inside the
EFE line). A 9.17 K object that neither radiates nor collides is invisible to
every instrument that exists. It is phase-space-safe (TG floor 23.25 eV vs
m > 3.3 keV: 141.9× margin, G084/G116) — but "safe" is not "visible". Same
for (b): the 2.04e-5 K dust is sensed *only* through its suppressed
structure-formation footprint (c_s² = 5.3e-13 at z=3, 61–1872× under the
registered residual budget, L194/L224) — coldness inferred, temperature never
read.

**Which rungs any instrument can reach — the honest census:**

| ratio or rung | measurable? | why |
|---|---|---|
| (c) alone: T_gas = μ m_p σ²/k_B | **YES** | X-ray/SZ kTvir (Eckert+17), galaxy σ (Tian+21/Sohn+20, G109), lensing M ↔ T (G095's closed form) |
| c/c′ (gas at two scales) | YES | the virial-T-of-total-mass relation: T_obs/T_pred = 2 f (r_M/r): closed form 3.51 vs 3.57 median, 0.05-dex scatter = HSE (G095) |
| σ_gal ↔ kT (equipartition) | YES | σ_gal/σ_gas,1D = 0.998 median, rms 0.062 dex (G109, 11 clusters) |
| a (= 9.17 K) | **NO** | no radiation, no collision — inert by construction |
| b (= 2.04e-5 K; (1+z)²) | **NO** | no channel; only its c_s² footprint at 1e-13, 61× under the tightest register |
| c/a, a/b, c/b | **NO** — none | every rung containing (a) or (b) has an inert denominator/numerator: the ladder's pair-ratios are identities between bookkeeping temperatures, not observables. In particular the c/a "cross-check via the cluster T and the phase T" does **not** exist: the phase T is not measurable, so c/a is never a measurable ratio — it is the exact mass-ratio identity μ m_p/m carved in stone, and only the mass ratio's *inputs* (m from the forest; μ m_p known) are empirical |

The one ratio with empirical content is not a ladder ratio at all — it is
**rung (c) read against itself**: the gas temperature IS the observable; the
ladder's other two rungs are its unobservable anchors.

## 4. VERDICTS

**V1 — the ladder, complete with the numbers. PASS.** (a) T = m σ²/k_B =
9.17 K at 5 keV (σ = 119.2 km/s triad; T/m = 1.835 mK/eV mass-free); (b) T =
m v_th²/k_B = 2.04e-5 K at z = 3 (1.28e-6 K at z = 0, ∝ (1+z)²); (c) T =
μ m_p σ²/k_B = 89.0 eV at the same σ, 3.68 keV at the cluster triad σ (A85
M_b(R500); 4.10 keV at G008's registered 809 km/s), observed median 6.17 keV
(X-COP kTvir, Eckert+17). Ratios on the committed numbers: a/b = 4.49e5
(registered 4.5e5 decoupling ratio, G116), c/a = 1.126e5 = μ m_p/m exact,
c/b = 5.06e10 (equal σ); cluster rung vs a: 4.65e6, vs b: 2.09e12. The
brief's glosses corrected: c/a ~ 1e5 ✓; a/b = 4.5e5 (not 1e4); c/b ~ 5e10
(not 1e9).

**V2 — the observable rungs. PASS (exactly one).** (c) is fully observable —
kTvir ↔ σ_1D = √(kT/μ m_p) (G109: 992 km/s ↔ 6.17 keV at the median; median
equipartition ratio 0.998); the T-of-total-mass reading (G095: closed form
2 f (r_M/r), median within 1.8%, 0.05-dex scatter = HSE 0.053 dex; G075:
3.6× hotter than the /2-convention baryon floor, median T_pred/T_obs =
0.28). (a) and (b) are unobservable — no radiation, no
collision, no coupling channel (G093 V4, THEORY.md 8); hence c/a, a/b, c/b
are unobservable ratios by construction, whatever the instruments' precision:
there is no instrument for 9.17 K or 2.04e-5 K.

**V3 — the honest statement. PASS.** The temperature ladder is a bookkeeping
statement — one velocity scale (the triad's σ; T/m = σ²/k_B registered
constant; the gas in equipartition with the same σ), three temperatures set
by (mass, coupling, expansion) — and it is *not* a new observable. Two of its
three rungs (the phase at 9.17 K, the dust at 2e-5 K) are observationally
inert by the theory's own construction: the ladder organizes the framework's
thermodynamic ledger but adds no measurable quantity to it. The one rung with
empirical content is the baryonic gas temperature T = μ m_p σ²/k_B — which is
the ordinary ICM virial relation — and on the committed record it is already
confirmed: G109's cross-instrument equipartition (σ_gal/σ_gas = 0.998 median,
rms 0.062 dex = 6% at 1σ), G095's closed-form T-ratio reproduction (1.8% at
the median; log10 scatter 0.051–0.053 dex = the registered 0.05-dex HSE
scatter), i.e. **T = μ m_p σ² confirmed at the 0.06–0.10 dex level** — and the
zero-parameter cluster rung (M_b → σ_pred → T: 3.68–4.10 keV vs the observed
6.17 keV median, a factor 1.5–1.7, the G075-registered 3.6× standing as the
floor-to-observed gap). Nothing more is claimed for the ladder; the ratios
c/a and a/b decorate the theory's bookkeeping; they are not observables.

---

**References:** G116 (T/m = σ²/k_B mass-free; T_phase(5 keV) = 9.17 K; dust
T(z=3) = 2.04e-5 K; decoupling ratio 4.5e5 — A2), G093 (the free-dust coldness:
v_th, λ_fs, c_s² footprint, V4 non-claims), G095 (the cluster T as the virial T
of the total mass; closed form 2 f (r_M/r); HSE scatter 0.053 dex), G109
(cross-instrument σ: equipartition 0.998; kTvir table), G008 (cluster σ_pred =
809 km/s registered, STATE.md line 91; the isothermal phantom at cluster scale),
G075 (clusters under the triad; T_pred/T_obs = 0.28; kTvir median 6.17 keV;
mu = 0.6; /2-convention), G091/G03G (the triad: σ² = (1/2)√(G M_b a₀), kappa =
1/2, k_B T = m σ²).