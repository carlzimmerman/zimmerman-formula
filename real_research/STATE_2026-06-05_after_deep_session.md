# Current state after the 2026-06-05 verification + door-pushing session

*C. Zimmerman. A single coherent picture tying together one long autonomous session (≈17 commits). Everything below was
computed on real on-disk data or grounded in primary 2024–2026 literature, and load-bearing numbers were independently
re-verified. The honest net: the framework's **standing did not improve — it sharpened, and in two places got less
favorable** (that's what honest checking does), while its **theoretical frontier became precisely defined** (a clean
trilemma) for the first time.*

## Bottom line (one paragraph)

`a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ)` is a **viable, internally-consistent re-derivation of MOND's z=0 phenomenology from
Λ**. The scale and the `Y^{3/2}` form are forced; the coefficient is a data-selected convention that, on consistent
footing, puts a₀ at the **low edge** of the data (not "favored"). It is **not refuted**, it **carries MOND's shared
cluster/Bullet tensions**, and its **one distinctive claim — declining a₀(z) — is undecided-leaning-unfavorable and
hostage to DESI**. Its deepest theoretical issue is now precisely stated: a **{Cassini-safe, CMB-safe, a₀(z)-natural}
trilemma** that no known realization satisfies in full. The verdict belongs to **DESI DR3 + a clean z~3 deep-MOND
curve (~2027)**.

## What this session changed (honestly)

1. **Coefficient — *less* favorable.** A cross-footing error (using `cH₀` where the pure-Λ `cH_Λ` was meant, a 1.208×
   inflation) had made the data look like they "land on Z = 5.79." On consistent footing the data give κ ≈ 0.59–0.64,
   so the framework's κ=½ (a₀ = 9.36e-11) sits at the **low edge**, ~20% under observed. Fixed across the corpus.
   → `reviews/COEFFICIENT_FOOTING_AUDIT_2026-06.md`.
2. **Empirical standing — comprehensive, mixed, not refuted.** 27-agent stress-test on 13 observables: 0 refuted, 2
   serious-tension (clusters η≈2.1, Bullet — both SHARED with all MOND). → `FRAMEWORK_EMPIRICAL_STANDING.md`.
3. **Corrected my own earlier read (*more* favorable).** The intermediate-z BTFR *differential* z-trend (cancels the
   zero-point) is **−0.029±0.012 dex/z — it leans the framework's *declining* way**, not rising. My earlier "leans
   against" had read the absolute-offset systematic.
4. **Universality holds (the strongest argument).** a₀-vs-environment slope = +0.052±0.037: 1.4σ from uniform, 12σ
   below a local-density source. The SB-residual is not significant. → `reviews/universality_selects_rho_lambda.py`.
5. **A *second* framework-relevant exposure surfaced and sharpened — *less* favorable.** The Cassini Solar-System
   quadrupole excludes RAR-fitting modified-gravity MOND at **3–15σ** (Desmond+2024 → 2026 update). It is **generic to
   all covariant relativistic MOND** (AeST/RMOND/BIMOND/Khronon) and **inherited via AeST**; the "modified-inertia
   evades it" escape is not freely available. → `CASSINI_QUADRUPOLE_CONSTRAINT.md`.
6. **The cluster liability gained an intrinsic candidate — *more* favorable, caveated.** AeST's mass term `μ²Φ`
   (`1/μ~1 Mpc`) switches on *at the cluster scale*, giving an oscillatory RAR that matches reported cluster-RAR
   features — but the regime is flagged *expected-unstable* and only isothermal toys exist. → `AEST_MASS_SCALE_two_doors.md`.

## The theoretical frontier, now precisely defined: a trilemma

The framework's concept — `a₀` = the **free-fall clock** (`a₀ ~ where t_dyn = t_cosmic`) — is **modified inertia**, not
a fifth force. That reframes both exposures and yields a clean trilemma (`MODIFIED_INERTIA_the_natural_home.md`):

| realization | Cassini-safe | a₀(z) natural | CMB-safe |
|---|---|---|---|
| **Modified inertia** (the concept) | ✓ (COM acceleration) | ✓ (time-nonlocal) | ✗ (acoustic mod + no DM-mimic) |
| **AeST** (modified gravity, the stopgap) | ✗ (3–15σ Cassini) | ~ (K(𝒬) parameterized) | ✓ (Ȳ=0 + dust mode) |
| **Mod. inertia + 11 eV sterile-ν** | ✓ | ✓ | ✓ (νHDM fits CMB) — **but** gives up the "one number" unification, only partially fixes clusters (Tremaine–Gunn), and is underexplored |

- **Cassini** dissolves in modified inertia (internal planetary `g≫a₀` stay Newtonian; only the COM galactic orbit
  feels MOND → no internal EFE quadrupole).
- **a₀(z)** is automatic in modified inertia (time-nonlocality → cosmic-history dependence → `√ρ_DE` tracking is the
  natural expectation, not a posit).
- **CMB** is the hard corner: a direct inertia modification has no field to play the `Ȳ=0`/dust trick, and the CMB
  perturbation accelerations **straddle a₀** (g ~ a₀ at low-ℓ, ~10–40 a₀ at the peaks), so it modifies the acoustic
  physics. The concrete fix (add an 11 eV sterile neutrino) works for the CMB but at the three costs above.

**The genuine open problem is to satisfy all three corners at once** — a covariant, CMB-safe modified-inertia
realization of the free-fall clock (or modified-inertia + a clean dark sector). That is hard and field-wide, but it is
the *correct* problem, and it is the one the framework's own concept points at. It is **not** the coefficient (proven a
data-selected convention, search exhausted) and **not** a TOE (no unified path).

## What decides it, and when

- **Distinctive claim (declining a₀(z)):** DESI DR3 + clean z~3 deep-MOND kinematics, ~2027. Currently
  undecided-leaning-unfavorable (MUSE-DARK III rises ~2σ against once de-systematized; the intermediate-z differential
  trend leans for; both weak).
- **Near-term pressure (no telescope needed):** the Cassini quadrupole vs the AeST realization — a real, strengthening
  3–15σ tension whose only escape (β₀ threading RAR+Cassini, or covariant modified inertia) is uncomputed.
- **Shared MOND tensions (clusters, Bullet):** real, serious, contested (Hernandez 2026 vs Famaey 2026 on the Bullet;
  the AeST μ²Φ candidate vs its instability on clusters).

## Session document index

- Empirical: `FRAMEWORK_EMPIRICAL_STANDING.md`, `reviews/COEFFICIENT_FOOTING_AUDIT_2026-06.md`,
  `A0Z_MUSE_DARK_III_CONFRONTATION.md`, `reviews/universality_selects_rho_lambda.py`,
  `reviews/cassini_quadrupole_framework.py`.
- Theory frontier: `CASSINI_QUADRUPOLE_CONSTRAINT.md`, `AEST_MASS_SCALE_two_doors.md`,
  `MODIFIED_INERTIA_the_natural_home.md`, `THE_NEXT_CALCULATION_aest_quasistatic.md`.
- Prior capstones (unchanged, still valid): `COEFFICIENT_DEFINITIVE_VERDICT.md`, `DOORS_FINAL_DISPOSITION.md`,
  `QG_PROGRAMS_TOE_GRADING.md`.

**Honest closing.** This was a session of *verification*, not vindication. The framework came through **not refuted**
and with its frontier **sharpened into a single well-posed problem** — but two of its softer comforts (the coefficient
"landing" on Z, and an easy modified-inertia escape from Cassini) were removed, and the distinctive claim remains
hostage to data ~2027. That is exactly what a real, falsifiable proposal looks like mid-life: standing, exposed, and
pointed at the right next problem.
