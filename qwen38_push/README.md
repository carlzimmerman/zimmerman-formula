# qwen38_push — the closure track (Qwen 3.8 watcher + direct work)

Two lanes, both committed with Python verdicts AND Lean certificates (exit 0,
zero sorry, axioms {propext, Classical.choice, Quot.sound}).

## Q001 — THE SOUND-SPEED IDENTITY (the missing piece)

**σ_Z² ≡ c_s² ≡ P/ρ_ph = √(G·M_b·a₀)/2 — exactly, Lean-certified.**

The Zimmerman temperature — rung 4, the theory's one POSTULATED input, the
quantity G035's certified N-body **KILLED** as a relaxation product — is the
**adiabatic sound speed of the L247 self-acceleration medium** evaluated on the
G003 Lean-certified phantom solution:

- P = g²/8πG — L247's matched law (derived for *arbitrary* kernel ν from the
  theory's own sourced field equation; hydrostatic residual ≡ 0, Lean-verified)
- ρ_ph = √(G·M_b·a₀)/4πGr² — G003 (Lean)
- P/ρ_ph = √(G·M_b·a₀)/2 = G·M_b/(2r_M) = σ_Z² — **IDENTICAL: True** (sympy),
  d/dr = 0 (exact isothermality), EOS **linear** (P = σ_Z²·ρ — one constant,
  and it IS the temperature)

Derived consequences (zero free parameters):
- **w_eff = σ_Z²/c² = 1.55–1.74×10⁻⁷**, inside the G028 cold window (5.7×10⁻⁷)
  with margin 3.3–3.7× — the medium is cold BY CONSTRUCTION; the cold-sector
  requirement and the temperature are the same fact
- Numeric anchors reproduce registered values to 0.007%: G031 MW proxy
  119.2/124.9 km/s; G035 NGC3198 σ_target 118.05 km/s
- **G035's kill RESOLVED as a category error in the test**: Newtonian N-body
  asked whether σ_Z is a *relaxation product*; it is a *constitutive* EOS
  property. The C2 control evaporated because Newtonian-held isothermal dust
  at σ_Z is unbound — the medium is pressure-held (L247 V1), and Newtonian
  N-body has no pressure term. G035's own escape hatch ("L247 constitutive law
  or new dynamics") is now filled.
- **G056's V2b 43% deviation EXPLAINED**: profile matching across the
  transition regime, where the deep law is invalid; the ratio identity is
  pointwise-exact where the deep law is exact (G056 V1: c_deep = 1).

**Rung 4: POSTULATED → DERIVED-CONSTITUTIVE.** The first-principles chain is
now complete at the equation-of-state level:

a₀ = s/2 (G002) → P = g²/8πG (L247) → ρ_ph (G003, Lean) → **c_s² = σ_Z²
(Q001, Lean)** → g² = a₀·g_N, the RAR (G031, Lean)

Honest scope: derives the temperature's VALUE and thermodynamic IDENTITY; does
NOT derive the medium's EXISTENCE from a deeper principle (why the scalar
freezes at X=0 remains G001/L192 criticality), and rung 5's amplitude law
(PAPER29 Requirement 10) stays OPEN. Note G046 (committed 00217c30e) derived
the same temperature by a third route (scalar-mediated 1/r force + hydrostatic
matching) — three independent derivations now agree.

Files: `Q001_sound_speed_identity.py/.out`, `Q001_results.json`,
`lean/Q001_sound_speed_identity.lean` (7 theorems + capstone conjunction).

## Q002 — THE DARK-ENERGY COINCIDENCE AS A FOOTING SELECTOR

**Ω_Λ = 32π·a₀²/(3H₀²c²)** — G cancels exactly (Lean `omega_identity`). One
measured number plus H₀ fixes the dark-energy fraction:

| Footing | a₀ (m/s²) | Ω_Λ | Verdict |
|---|---|---|---|
| Canonical (theory's own, κ=½) | 9.3619e-11 | **0.685744** | +0.15% of Planck 0.6847; Lean window (0.6857, 0.6858); inside 1σ by 6× |
| Alt (empirical RAR family) | 1.1279e-10 | **0.9953** | matter-free flat universe, 44σ — **COSMOLOGICALLY DEAD** (Lean `alt_excluded`) |

**The selection rule (the finding):** the two a₀ footings carried as equal
options through every galaxy-scale lane are NOT cosmologically equal. Only
κ = ½ survives Planck; 1.1279e-10 is viable only as a fit value inside ~20%
systematics, never as the fundamental scale. G052's honest alt-footing FAIL is
promoted to a derived two-way exclusion.

**The pincer:** Planck (H₀, Ω_Λ) fixes a₀ = 9.362e-11 ±0.51% (1σ) — 40×
sharper than galactic systematics — and the RAR spread contains it. Registered
kill: a future <1%-systematics RAR fit outside [9.31, 9.41]e-11 falsifies
κ = ½. **H₀ sensitivity (honest):** with SH0ES H₀ = 73 the a₀ window slides to
1.01e-10, still RAR-consistent — the theory absorbs the Hubble tension and
cannot arbitrate it (stated, not hidden).

Honest scope: a₀'s canonical value was derived FROM ρ_Λ (G002/G031), so the
Ω-window checks are consistency checks of the whole chain, not independent
galactic predictions of Ω. The independent direction is the pincer kill.

Supersedes G058's uncommitted design script (same K to 1e-15; G058's
cross-check line carried a c²-placement bug — noted, main computation
confirmed).

Files: `Q002_omega_lambda_selector.py/.out`, `Q002_results.json`,
`lean/Q002_omega_lambda.lean` (7 theorems + `the_selector` capstone).

## Commits

- `ec8a02c12` — Q001 (8/8 PASS + Lean 7 theorems)
- `3e2ef826d` — Q002 (6/6 PASS + Lean 7 theorems)
