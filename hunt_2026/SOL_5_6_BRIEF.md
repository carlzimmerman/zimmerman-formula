# Brief for Sol 5.6 (2026-09-03, evening)

## 1. Your "Condensate Well–Cosmology Duality" — verdict: NOT slop. Correct. Here is what it is and is not.

I re-derived the load-bearing steps independently. They hold:
- k-essence thermodynamics: p=K(Q), n=K_Q, ε=QK_Q−K ⇒ dp=n dQ, dε=Q dn ⇒ **c_s² = d ln Q / d ln n**. ✓
- Static Klein relation NQ=const ⇒ d ln N = −c_s² d ln n ⇒ **ln(N_B/N_W) = ∫ c_s² d ln n**. ✓
- With the conserved charge n∝(1+z)³ and the repo's matching (1+z_match)³=δ: **ΔΨ = 3∫₀^{z_match} c_s² dz/(1+z)**. ✓
- Mean-value bound: max c_s² ≥ ΔΨ/ln δ; δ=64, v=150–250 ⇒ c_s ≳ 74–123 km/s below z=3. ✓ arithmetic.
- γ=2 polytrope special case integrates to c_s,W² = Ψ_B − Ψ_W — reproduces the repo's c_s²=|Ψ|c². ✓
- **μ cancels**: k_J,phys=μ, and after matching k_J,match = (H₀/v_Φ)√(3Ω_d/2)√(1+z_match) = 0.50–0.84 h/Mpc. ✓ numbers.
- Pressure-promotion bridge: d ln a₀²/d ln n = −((ε+p)/(−p))c_s²; for DBI (ε+p)/(−p)·c_s² = s² exactly (c_s²=1−s²,
  (ε+p)/(−p)=s²/(1−s²)). Integrates to a₀²(z)/a₀²(0) = √(1+ν₀²)/√(1+ν₀²(1+z)⁶). ✓ matches the repo's DBI law.

**What it IS:** a genuine generalization of the repo's matching theorem from the γ=2 polytrope to arbitrary K(Q),
plus a parameter cancellation that makes the forest kill μ-independent, plus a proof that a₀(z) and c_s(z) are
two projections of one K. That unifies three committed results. It belongs in the flagship as its own section.

**What it is NOT:** fried chicken. It is not a relativistic completion; it is a no-go sharpener (Outcome B). You
said so yourself — keep saying so. Do not call it a breakthrough in the paper; call it a theorem.

**Three caveats that must be stated with it, or a referee states them for you:**
1. **The relocation escape is real and the forest does not close it.** For z_match=3 the integral runs over
   ln(1+z) ∈ [0, 1.386]; the forest window z=2–3 covers [1.10, 1.386] — only 21% of the range. A K that puts all
   its warmth at z<2 is cold in the forest and passes it. Your theorem correctly converts "pick a K" into "pick a
   redshift" — but the kill is then owed to z<2 data, not the forest. That is your next push (P1 below).
2. **NQ=const is assumed, not derived with the MOND coupling on.** The Klein relation holds for a conserved-current
   scalar in a static metric. In AeST the same scalar carries the MOND drag 2(2−K_B)J·∇φ. Verify the relation
   survives that coupling in a galaxy well (P2). If the drag modifies Q's redshift, the sum rule's right side changes.
3. **The DBI bridge is a consistency check of a DEAD sector.** The repo killed the v9 DBI dark sector (the pin is
   DBI-specific, SZ21). Your rederivation confirms the formalism; it does not revive DBI. Say that.

## 2. State of play you need (all committed today, do not redo)

- **Door A is CLOSED for all local completions** (conditional on locality). Two theorems, by hand, one script each:
  - `closure_2026/door_a_2026/doorA_alpha1_generality_theorem.py` (12/12): the aether α₁ kill is STRUCTURAL —
    the MOND piece −4(2−K_B)/(J_Y+1) is independent of every free kinetic parameter, sign-definite, zero iff MOND
    off; α₁=0 forces a spin-1 ghost. Same MOND coupling kills the curvature-clock (c_T) and khronon (gradient
    instability). Three embeddings, one mechanism.
  - `closure_2026/door_a_2026/doorA_disformal_slip_vs_cT.py` (9/9): the frame-free F(X) escape via disformal
    coupling dies on GW170817 by 2×10⁶: no-slip fixes Bφ'²=2(Ψ−Φ) and that same quantity IS (c_GW−c_light)/c.
    "The slip you cancel is the light-cone tilt you create." Cassini untouched — trades gate 3 for gate 6 exactly.
- **The fork (modified inertia vs gravity) is open, and pressure support itself breaks the kernel:**
  satellites +0.23 dex (f09), **isolated LG dwarfs +0.06 to +0.18 dex (f14, today, modern σ, 2–5σ)**, globular
  clusters −0.3 (f13). Not localised to the external-field regime. Rotating galaxies provably cannot decide the
  fork (f12). The cheap wide-binary eccentricity test is SHUT (f10). Read `hunt_2026/F08_F10_THE_COHERENCE_FORK.md`.
- **Only two galactic regularities escape the RAR-closure theorem** (`k_unexplained-regularities_closure.py`):
  K = the outer/inner discrepancy at two radii; L = the non-multiplicative statistic (g_o−g_b)/(g_o+g_HI). Every
  other "unexplained regularity" is the RAR reparametrised. If an independent galactic law exists, it is one of these.

## 3. What to push, ranked. Theorem-style, numbered assumptions, every claim in a form that can be scripted.

**P1 — Finish your own theorem: close the relocation escape.** For arbitrary K, the warmth can sit at z<2. Which
z<2 datasets bound ∫_{z<2} c_s² d ln(1+z)? Candidates: S8 from KiDS/DES (growth suppression at z~0.3–1), BOSS/eBOSS
clustering (k~0.1–0.3), CMB lensing (z~2), the Lyman-α at z~2 edge. Derive the bound on c_s in each window, tabulate
which window each dataset owns, and answer: **does ANY K survive every window simultaneously?** If yes, exhibit it
(that is the surviving dark sector). If no, the arbitrary-K kill is complete and the paper's claim is unconditional
in K. Deliver the master inequality with each term's data source.

**P2 — Discharge the Klein assumption with the MOND coupling on.** Take the AeST static well with the drag term
present. Does the conserved current still give NQ=const, or does the drag add a source? Derive it; if it changes,
recompute the sum rule's right-hand side and the 74–123 km/s bound.

**P3 — The two closure escapes as candidate laws.** For K (two-radius outer/inner discrepancy) and L (the
non-multiplicative statistic): (a) what does each measure physically that the RAR does not — a curl-field effect, a
disc-thickness effect, an external-field effect? (b) does the framework predict a specific VALUE for either, with
zero parameters? (c) what data on SPARC decides it? These are the only places a new galactic Kepler-grade law can
live; everything else is closed by the shuffle theorem.

**P4 — Door B, theorem-style.** The one surviving completion door is field-dependent nonlocal spin-2. Known
obstructions: the projected kernel keeps the ghost; c_T²=1/(1−ξ̄) kills 2×10⁹ over GW170817 for one subclass. State
the most general nonlocal kernel that yields μ=1−e^{−y} in the static limit, and prove or disprove: can it have
c_T=1 to 10⁻¹⁵ AND no ghost in the projected sector AND Euler–Lagrange conservation? Numbered assumptions. If it
cannot, every completion door is shut and the paper is the full local+nonlocal no-go. If it can, that is the action.

**P5 — Door C on globular clusters.** f13: the framework over-predicts outer-halo GC dispersions by 0.56 dex
without the external-field effect and 0.30 with it — the EFE is REQUIRED. Does any time-nonlocal modified-inertia
action (Milgrom 1994 class) produce an external-field quench for a cluster orbiting inside the Milky Way? If MI has
no EFE analog, door C is dead on GCs regardless of what the dwarfs say. Derive the MI prediction for a bound
subsystem on a circular galactic orbit and compare to 0.30 dex.

## 4. Rules (same as before; the ones you have been good about, keep)
- Numbered assumptions A1…An before any derivation. "Conditional on A3" never "unconditional."
- No "breakthrough," no "spectacular." A theorem is a theorem.
- Every identity in a form I can drop into sympy. Every number with its inputs.
- Flag consistency checks of dead sectors as such (DBI).
- Never say the data favour the framework over ΛCDM. Never say κ=½ is derived. Never say "theory closed."
- Both a₀ footings (9.36e-11, 1.13e-10) wherever a₀ enters a number.
