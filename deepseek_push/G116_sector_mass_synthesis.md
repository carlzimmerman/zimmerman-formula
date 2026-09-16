# G116 — THE SECTOR MASS SYNTHESIS: one species, one mass

**Status:** 2026-09-15. Synthesis lane over the committed record — no new
physics, every number quoted from its registered lane and the arithmetic
reproduced in-script (`G116_sector_mass_synthesis.py`, all checks PASS).
The question: the framework's dark sector is ONE Noether charge in TWO
phases (the equilibrium phantom ~1% of Ω_dm inside the EFE line; the free
dust ~99% outside — G028/G093/G079). The two phases carry the same mass.
**What is the ONE mass window?**

---

## 1. THE TWO BOUNDS ON THE RECORD

| Bound | Value | Lane |
|---|---|---|
| Equilibrium phase — Tremaine–Gunn floor | m > 23.25 eV (ρ = 0.008 M☉/pc³, σ = 119.2 km/s; alt footing 22.45 eV at σ = 124.9) | G084 |
| Free-dust phase — Lyman-α forest bound | m > 3.3–5.7 keV (Viel+13 2σ 3.3 keV; Iršič+17 5.3 keV; Villaseñor+24 95% CL 5.7 keV) | G093 |
| The killed window (relic reading) | 93–148 eV empty by 1.6×; 11 eV relic dead at 103–190 Mpc streaming | f04 / f06 |

**The consistency (one species):** if the two phases are the same charge,
the binding bound is the forest's — m > 3.3–5.7 keV — and the
equilibrium's TG floor is then satisfied *automatically*:

    m_TG / m_forest = 23.25 eV / 3300 eV = 7.047e-3 ≈ 0.007
      (canonical, 2σ mass: 7.047e-3 ≤ 0.0071; alt footing 6.804e-3;
       95% CL mass 4.080e-3)

The 3.3 keV species clears the equilibrium's phase-space cap by a factor
**141.9×** (245.1× at the 95% CL mass) — the equilibrium TG bound never
binds. The same floor sits **4.01× below** the killed window's floor
(93.3 eV, f04/f06): the equilibrium sector is phase-space safe on *both*
sides of the killed window, exactly as G084 committed ("below the killed
window by 4×").

## 2. THE THERMAL CONSISTENCY — the phase temperature is set by the DYNAMICS

At m = 5 keV, σ = 119.2 km/s (the equilibrium's registered virial):

    T_phase = m σ²/k_B = 9.17 K
    (direct m σ²/k_B = 9.17 K; registered linear law 1.835 mK/eV → 9.17 K;
     band 9.17–10.07 K across the two footings, G084 thermo block)

The virial is **mass-free**: σ² = (1/2)√(G M_b a₀) = 1.4211e10 (m/s)²
→ σ = 119.21 km/s (registered 119.2 km/s, G084; M_b = 6.5e10 M☉, G003) —
no particle mass enters the well. Hence T_phase/m ≡ σ²/k_B is the
mass-*independent* registered constant **1.83–2.01 mK/eV**; at keV masses
the equilibrium phase sits at ~10 K, i.e. dynamically cold in absolute
terms.

**The decoupling, stated:** *the mass sets the free-streaming/phase-space
side of the species* (λ_fs = 0.50–0.82 Mpc at 5.7–3.3 keV against the
0.6 Mpc register; TG caps ρ_max ~ m⁴σ³); *the dynamics sets σ* (the
DE-anchored virial of the fixed baryon well). The two never feed back:
σ does not depend on m, and T is σ-determined up to the linear mass
factor.

**Registry note (honest):** the brief's "T ~ 4e-5 K" does **not**
reproduce on the committed formula at (m = 5 keV, σ = 119.2 km/s). It is
the *free dust's own kinetic temperature* T = m v_th²/k_B at z ≈ 3:
2.04e-5 K (3.3 keV, v_th = 0.219 km/s; 1.19e-5 K at 5.7 keV; 1.28e-6 K
at z = 0) — i.e. the two phases' velocity scales transposed (119.2 km/s
virial vs ~0.18–0.22 km/s thermal; T ~ v², (0.22/119.2)² = 3.4e-6).
The equilibrium phase's honest value is ~9.2–10.1 K, and the decoupling
in one number is

    T_equil / T_kin,dust(z=3) = 4.5e5

— the equilibrium is a Maxwell–Boltzmann state *at* the virial
temperature; the free dust never equilibrates.

## 3. THE WINDOW — upper-bound candidates, audited

**(a) Production (the shift-charge relic abundance): NOT DERIVED.** G093
V4's registered non-claim is the authoritative register: the framework
does not predict the mass ab initio, does not claim the thermal-relic
production mechanism; the window is the astrophysical constraint *on* the
species. Quantified: the thermal 1-dof closure Ωh² = m/(94 eV) (f04)
*overcloses* at keV masses — 292.6× Ω_dm at 3.3 keV, 505× at 5.7 keV,
8866× at 100 keV — so the observed Ω_dm requires a dilution of
3.4e-3–1.1e-4 (a non-thermal or diluted channel the framework does not
claim). The one production motif on file is the dark-dimension
KK-graviton corridor (1–100 keV, freeze-in at T ≈ 4 GeV,
FORWARD_PROGRESS_2026-06-06): alive, squeezed, a sketch — **not a
derivation**. This corridor is the origin of the 100 keV upper end.

**(b) The stellar-warming floor: NOT BINDING HERE.** Published
stellar-warming/cooling floors bind *SM-coupled* keV-DM classes. The
framework's species is SM-decoupled by construction (no direct-detection
coupling — THEORY.md 8; G093 V4), so no stellar probe channel exists.
Listed and dismissed.

**(c) TG in the densest systems (cluster cores): m > 11.8 eV only** (G093)
— a *lower* bound, satisfied with 279× margin at the 2σ mass. Non-binding
in either direction.

**The honest window:**

    m ∈ [3.3, 100] keV     — ONE cold species, lower bound BINDING

- lower end: the forest, 3.3 keV (2σ, Viel+13); the 95% CL reading
  5.7 keV (Villaseñor+24) puts λ_fs = 0.50 Mpc *inside* the 0.6 Mpc
  register — the preferred binding statement;
- upper end: 100 keV is the top of the KK-graviton freeze-in corridor
  sketch, **NOT an astrophysical constraint** — no committed gate binds
  the species from above; m > 100 keV is unconstrained on the record.

## 4. VERDICTS

**V1 — the two bounds are ONE-SPECIES COMPATIBLE. PASS.**
The binding bound is the forest's (m > 3.3–5.7 keV, G093); the
equilibrium's TG floor (m > 23.25 eV, G084) is satisfied automatically:
m_TG/m_forest = 7.047e-3 ≤ 0.007 (canonical, 2σ mass), margin 141.9×
(245.1× at 95% CL). The equilibrium floor also clears the killed
93–148 eV relic window by 4.0× below its floor (f04/f06) — safe on both
sides. One species, two phases, one mass: no conflict on the record.

**V2 — the honest mass window: m ∈ [3.3, 100] keV. PASS.**
Lower bound binding (forest); upper end a placeholder — the production
corridor's top, not a constraint. The two bounds of §1 collapse into one
statement because the equilibrium's floor is 142× below the forest's:
the phase-space cap never binds the equilibrium once the forest bound is
met.

**V3 — the decoupling: mass vs dynamics. PASS.**
σ² = (1/2)√(G M_b a₀) = (119.21 km/s)² contains no particle mass; the
mass sets λ_fs (0.50–0.82 Mpc vs the 0.6 Mpc register) and the TG caps;
T_phase/m = σ²/k_B = 1.83–2.01 mK/eV is the mass-independent registered
constant; T_phase(5 keV) = 9.17 K vs the free dust's own kinetic
T(z=3) ≈ 2e-5 K. The equilibrium's temperature is a *dynamical*
statement; the particle mass is a *kinematic/phase-space* statement.

**V4 — production-mechanism status: NOT DERIVED — listed. PASS as stated.**
No production mechanism is derived or claimed on the record (G093 V4);
a thermal-ish keV yield would overclose by 3e2–9e3× (Ωh² = m/94 eV,
f04), so the observed Ω_dm needs dilution 3e-3–1e-4 through a channel
the framework does not specify; the one registered motif — the
KK-graviton freeze-in corridor, 1–100 keV (FORWARD_PROGRESS_2026-06-06)
— is a squeezed sketch, and the window's upper end waits on it. The mass
window is an astrophysical constraint on the species, not a prediction
of its origin.

---

## 5. SOURCES (all committed)

- G084 (the equilibrium TG floor m > 23.25 eV at ρ = 0.008, σ = 119.2;
  T_per_eV = 1.83–2.01 mK/eV; the 4× offset below the killed window),
- G093 (the free dust: m > 3.3–5.7 keV cold; λ_fs 0.50–0.82 Mpc vs the
  0.6 Mpc register; TG minima incl. clusters 11.8 eV; V4's production
  non-claim; one-species-two-phases E1/V2),
- f04 (thermal 1-dof closure Ωh² = m/94 eV; the 14.7–93 eV conditional
  and its three costs), f06 (the 93–148 eV killed window, empty by 1.6×;
  the 11 eV relic dead at 103–190 Mpc; the Newtonian-linear-regime
  escape closed),
- G079/G022 (dust share 98.7–99.2% of Ω_dm; no double counting),
  G028 (the conserved Noether charge), G003/G03E (M_b, the EFE line),
- G089 (the classification rules applied to the window's claims:
  DERIVED / EMPIRICAL / CIRCULAR / OPEN),
- FORWARD_PROGRESS_2026-06-06 (the KK-graviton DM corridor 1–100 keV,
  freeze-in at T ≈ 4 GeV — sketch, listed as such).
