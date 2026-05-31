# The Radion–MOND Bridge: an honest attempt at Tier B

**v12 · Draft, 2026-05-31 · companion to `reviews/radion_mond_bridge.py`**

The two halves of the framework — the E₆ orbifold GUT (`v12_E6_GUT_CONSTRUCTION.md`)
and the evolving-a₀ cosmology (`EVOLVING_A0_PREDICTION_PAPER.md`) — share the *number*
Z² = 32π/3 but, as `a0_construction_connection.py` showed, not a *mechanism*. This document
attempts the bridge the connection audit named as "Tier B": make the compactification
**volume modulus (the radion)** do double duty — fix the vacuum energy **and** be the field
that produces an evolving MOND scale. It is written to the same honesty bar as every other
floor: build it far enough to test, then keep a brutal ledger of what does not close.

**One-line verdict:** buildable as a coherent *research program* with a genuine mechanism
(a Hubble-mass / horizon-coupled modulus makes a₀ ~ cH(z) natural, with the O(1) factor = 1/Z),
**not** a finished derivation — it imports the cosmological-constant problem, needs an imposed
MOND interpolation, and the *literal* "one radion does everything" version faces a
varying-constants bound. More than a shared symbol; less than a Theory of Everything.

---

## 1. The 4D effective action

Compactify the higher-D Einstein–Yang–Mills–Dirac theory on K = (T²)³/(Z₂×Z₂). The 4D
effective theory is GR + the canonically-normalised radion φ (the volume modulus) + the
E₆/SM matter:

```
S = ∫d⁴x √-g [ M_Pl²/2 R  −  ½(∂φ)²  −  V(φ)  −  (a₀²/8πG) F( (∂φ_MOND)²/a₀² )  +  L_matter ]
```

- **V(φ):** the radion stabilisation potential (plank i).
- **F(X):** the AQUAL (Bekenstein–Milgrom) kinetic function whose deep limit gives MOND
  (plank ii). The bridge's content is the claim that *the same field* φ appears in V and in F.

## 2. Plank (i) — stabilisation fixes the volume, and (tries to) fix Λ

A radion potential `V(φ) = A e^{−αφ} − B e^{−βφ}` (Goldberger–Wise form; or a Casimir +
flux + curvature sum, cf. `radion_casimir_attempt.py`) has a minimum at φ₀. Demand
`V'(φ₀)=0` fixes the compactification volume to **Z² = 32π/3**, and `V(φ₀) = Λ` is the 4D
vacuum energy, which sets the late-time Hubble rate via H² = (8πG/3)ρ.

**Honest status:** `V(φ₀)` is generically O(M_KK⁴), not O((meV)⁴). Landing it on the
*observed* Λ is the **cosmological-constant problem** — a tuning / landscape selection, not a
derivation. Plank (i) "fixes Λ" only in the sense every string vacuum does.

## 3. Plank (ii) — the radion as the MOND field, and why a₀ ∝ H(z)

The AQUAL piece reproduces MOND exactly (demonstrated numerically in
`radion_mond_bridge.py`, part 1): the field equation `μ(g/a₀) g = g_N` with
`μ(x)=x/√(1+x²)` gives Newton for g≫a₀ and `v⁴ = G M a₀` (flat rotation curves) for g≪a₀.
A 10¹¹ M_⊙ galaxy flattens to v_flat ≈ 200 km/s. This is real, standard MOND physics; the
only new claim is **φ = the radion**.

**The evolution mechanism (the genuine new content).** An ultralight modulus whose Compton
wavelength equals the Hubble radius, `m_φ c² ~ ℏ H(z)`, has a force range ~ c/H(z) and a
natural acceleration scale a₀ ~ cH(z) — the de Sitter / horizon acceleration. The O(1)
normalisation is the coupling 1/Z, so

> **a₀(z) = c H(z) / Z**, hence **a₀(z)/a₀(0) = E(z)** — automatic and Z-independent,

with a₀(0) = cH₀/Z = 1.20×10⁻¹⁰ m/s² *requiring* the coupling = Z = 2√(8π/3), and a modulus
mass m_φ ~ ℏH₀/c² ≈ 1.5×10⁻³³ eV. **This is a mechanism for *why* a₀ ~ cH and *why* it tracks
H(z)** — strictly more than "the two halves share 32π/3."

**Solar-system safety:** in the Solar System a/a₀ ~ 5×10⁷, so μ→1 and the fractional MOND
deviation ~ a₀/a ~ 2×10⁻⁸ ≪ the Cassini PPN bound (~2×10⁻⁵). The scalar is Newtonian where
it must be; MOND switches on only in the a < a₀ galactic outskirts.

## 4. The ledger — what does **not** close

| Item | Status | Why |
|---|---|---|
| Cosmological constant | **OPEN** | V(φ₀)=Λ_obs is tuned (CC problem); imported wholesale. |
| Heavy-vs-light (the crux) | **OPEN** | (i) wants a *heavy, frozen* stabilised modulus; (ii) wants an *ultralight, rolling* one (m~H). A single field generically can't be both. |
| Varying constants | **OPEN** | a rolling radion makes Z² (hence α, couplings) time-dependent; α̇/α < 10⁻¹⁷/yr forces coupling ξ < 10⁻⁷. Possibly evadable, real. |
| MOND interpolation F | **IMPOSED** | μ(x)→x deep limit is chosen to fit rotation curves, not derived — as in every MOND theory. |

## 5. Three architectures — and which survives

- **A — one ultralight radion** (quintessence + MOND). Most economical, *literally* "the
  radion does everything." Killed/strained by varying constants, and a rolling field can't
  also sit at the minimum that fixes Z².
- **B — two moduli** (one heavy/stabilised for Z²+Λ, one ultralight for MOND). Clean, no
  varying-constants problem — but you paid with a second field, so it isn't "double duty."
- **C — stabilised radion + horizon MOND.** The stabilised modulus fixes Z² + bare Λ and
  sets the O(1) coupling **Z**; the evolving scale a₀(z) ~ cH(z) emerges *holographically*
  from the de Sitter horizon (Verlinde-style). No varying constants; uses the modulus you
  already need. **Most defensible** — but here the radion sets the *coupling*, not the
  *dynamics*, so it is a notch weaker than "the radion *is* the MOND field."

## 6. Honest net

**Built (computable, in the script):** the AQUAL completion makes v⁴=GMa₀; a Hubble-mass
modulus makes a₀(z)=cH(z)/Z with the evolution automatic and the coupling fixed to Z; it is
solar-system safe. **A real mechanism, not a coincidence of numbers.**

**Not closed:** the CC problem; the heavy-vs-light tension; the varying-constants bound on
the literal single-field version; the imposed interpolation. The architecture that survives
(C) makes the radion set the geometric O(1) = 1/Z while the horizon supplies the evolving
a₀ ~ cH(z).

The strongest *honest* sentence the bridge supports: *"an ultralight / horizon-coupled
modulus makes a₀ ~ cH(z) natural, with the geometric factor 1/Z; deriving Λ and pinning the
field's mass remain open."* That is the real Tier B — a genuine upgrade over the shared
symbol, and an honest distance short of a derivation.

---

*Reproducibility: `reviews/radion_mond_bridge.py`, `reviews/a0_construction_connection.py`,
`reviews/a0_cH0_Z_check.py`, `reviews/radion_stabilization_test.py`,
`reviews/radion_casimir_attempt.py`.*
