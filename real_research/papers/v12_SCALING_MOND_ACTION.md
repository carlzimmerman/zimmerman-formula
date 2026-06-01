# The Scaling-MOND Unified Action

**v12 · Draft, 2026-05-31 · companion to `reviews/scaling_mond_action.py`**

*"What unified action works with scaling MOND?"* — the honest, literature-grounded answer.
The point is **not** to invent a Lagrangian, but to take the one relativistic-MOND action
that already fits cosmology, make its acceleration scale evolve as a₀(z) = cH(z)/Z, and bolt
it onto the orbifold gravity + E₆ + matter core. Every term is standard; the framework's
content is one identification (a₀'s scale = the radion energy density) and one conjecture
(the coupling = √volume-modulus).

---

## 1. The action

$$
S=\int d^4x\,\sqrt{-g}\;\Big[\underbrace{\tfrac{c^4}{16\pi G}R}_{\text{(a) gravity}}
\;+\;\underbrace{\mathcal L_{\text{gauge}+\text{matter}}(A,\psi;g)}_{\text{(b) E}_6\to\text{SM, orbifold}}
\;\underbrace{-\tfrac12(\partial\chi)^2-V(\chi)}_{\text{(c) radion modulus}}
\;+\;\underbrace{\mathcal L_{\text{MOND}}\big(\phi,A^\mu;\,g,\,a_0[\chi]\big)}_{\text{(d) RelMOND sector}}\Big]
$$

with matter coupling **conformally** to the MOND scalar, $\tilde g_{\mu\nu}=A^2(\phi)\,g_{\mu\nu}$,
and the **scaling relation** that defines "scaling MOND":

$$
a_0(t)^2 \;\propto\; \rho_\chi(t)\quad\Longrightarrow\quad \boxed{\,a_0(t)=\frac{c\,H(t)}{Z}\,}\qquad
\big(\text{since } H^2=\tfrac{8\pi G}{3}\rho\big),\quad Z=2\sqrt{8\pi/3}.
$$

### Term by term (each grounded, with its honest status)

- **(a) Gravity** — Einstein–Hilbert. The tensor (graviton) sector is *only* this, which is
  why **c_GW = c** exactly (§4). Standard.
- **(b) Gauge + matter** — the E₆→SM Yang–Mills–Dirac content from K=(T²)³/(Z₂×Z₂)
  (`v12_E6_GUT_CONSTRUCTION.md`). Real construction, inherited predictions.
- **(c) Radion modulus χ** — the compactification volume modulus, with a stabilising
  potential V(χ) whose minimum fixes ⟨χ⟩=Z² **and** supplies the late-time vacuum energy.
  It does double duty: it sets the geometry *and*, through ρ_χ, the MOND scale a₀(t).
- **(d) RelMOND sector** — a **Skordis–Złośnik-type** scalar (+unit-timelike vector A^μ)
  relativistic MOND Lagrangian (PRL 127, 161302, 2021): the one MOND theory that reproduces
  the CMB and linear matter power spectra *and* keeps c_GW=c. Its acceleration scale is the
  **a₀[χ]** above, making it *scaling* MOND.

## 2. The non-relativistic / galaxy limit

In a galaxy the scalar obeys the Bekenstein–Milgrom equation
$\nabla\!\cdot\!\big[\mu(|\nabla\phi|/a_0)\nabla\phi\big]=4\pi G\rho$, with
$\mu(x)\to1$ for $x\gg1$ (Newton) and $\mu(x)\to x$ for $x\ll1$ (deep MOND). The deep limit
gives $g=\sqrt{g_N\,a_0}$, i.e. **v⁴ = G M a₀** — flat rotation curves and the baryonic
Tully–Fisher relation (verified, `scaling_mond_action.py` part 1: a 6×10¹⁰ M_⊙ galaxy
flattens to ≈176 km/s).

## 3. The scaling — and why it is the *derived* part

$a_0(t)=cH(t)/Z$ gives **a₀(z)/a₀(0)=E(z)** (Z cancels). This is the falsifiable,
distinctive, z>10 prediction, and it is **derived** from horizon thermodynamics:
a₀ tied to the instantaneous de Sitter horizon forces a₀ ∝ H(z) regardless of the O(1)
(`horizon_a0_derivation.py`). The mechanism for a₀ tracking ρ_χ ∝ H² is architecture C of
`v12_RADION_MOND_BRIDGE.md` (the radion stays frozen; the *background* expansion supplies
the evolution — which is why this dodges both the heavy-vs-light and varying-constants
tensions).

## 4. The filter that shapes the action: GW170817

GW170817 + GRB170817A measured **|c_GW/c − 1| < ~10⁻¹⁵**. This is the single most important
modern constraint on modified-gravity actions, and it is a *design filter* here:

- The tensor sector is pure (c⁴/16πG)R, and the MOND scalar is **conformally** coupled —
  conformal factors don't move null cones — so **c_GW = c exactly. Passes by construction.**
- It **killed** the alternatives: TeVeS and disformal/vector MOND theories generically gave
  c_GW≠c and were excluded in 2017. That is *why* the surviving sector is the Skordis–Złośnik
  form — and why this action is built on it rather than on TeVeS.

## 5. The honest ledger

| Piece | Status |
|---|---|
| gravity + E₆ + matter (orbifold core) | **works** (inherited) |
| deep-MOND v⁴=GMa₀ | **works** (standard B–M / SZ) |
| c_GW = c (GW170817) | **works** (conformal coupling, by construction) |
| a₀(z) ∝ E(z) (the test) | **derived** (horizon, route-independent) |
| interpolation function 𝓕 | **chosen** (fit to galaxies — as in all MOND) |
| O(1) coupling Z = 2√(8π/3) | **fit** (the horizon alone gives ~2π; `desitter_factor_audit.py`) |
| V(χ) → observed Λ | **open** (the cosmological-constant problem) |
| Z = √(volume modulus 32π/3) | **conjecture** (the interlocking-web posit) |
| **CMB fit with *scaling* a₀(z)** | **OPEN — the key check** |

**The one calculation I will not fake (§4 of the script):** Skordis–Złośnik fit the CMB with
**constant** a₀. Here a₀ is ~2×10⁴ × larger at recombination. The ratio a₀/cH = 1/Z stays
constant (so the MOND effect is a fixed fraction of horizon dynamics at every epoch — arguably
*more* natural than constant-a₀), but whether the SZ CMB fit **survives** the scaling a₀(z)
must be recomputed. It is not done here, and scaling MOND does **not** automatically inherit
SZ's CMB success.

## 6. Answer

> **The unified action that works with scaling MOND is a Skordis–Złośnik-type relativistic
> MOND sector (CMB-viable, c_GW=c) whose acceleration scale a₀ is promoted to a₀(z)=cH(z)/Z by
> tying it to the radion energy density, added to the orbifold gravity + E₆ + matter core.**

The scaling a₀∝H(z) is the *derived, falsifiable* heart; the interpolation function and the
coupling Z are *fits*; landing Λ and re-fitting the CMB with the scaling a₀ are *open*. That
is a real, buildable, honestly-bounded action — not a Theory of Everything, but a legitimate
modified-gravity model with one clean near-term test.

---

*Reproducibility: `reviews/scaling_mond_action.py`, `reviews/horizon_a0_derivation.py`,
`reviews/radion_mond_bridge.py`, `reviews/desitter_factor_audit.py`. Key references:
Bekenstein–Milgrom 1984 (AQUAL); Skordis–Złośnik, PRL 127, 161302 (2021) (RelMOND);
Abbott et al. 2017 (GW170817, c_GW=c); Milgrom 1983 (a₀≈cH₀/2π).*
