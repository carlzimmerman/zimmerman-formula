# HOSTILE REGRADE — route [dsunruh_potential] (Route A): does a local potential/curvature shift the dS-Unruh (cH)² floor → a0_local? (2026-06-14)

**REGRADE VERDICT: CONFIRMED NULL (CLOSED-FALSIFIER). The original grade stands — independently re-derived and
re-computed. This is a clean, derived, sign-right, magnitude-fatal null; the sixth banked null on the local-a0 front.**

Skeptic's checklist (a)-(e), all independently re-run (`/tmp/tolman_regrade.py`, `tolman_derivation.py`,
`missed_route_probe.py`, `nested_potential.py`, `curvature_route_check.py`, `highdensity_limit.py`):

## (a) Is the derivation REAL? — YES, and the c² scale is FORCED, not smuggled.
Re-derived the load-bearing step two independent ways (sympy):
- **a0 ∝ T_floor LINEARLY.** a0_framework = c²√(Λ/32π); T_floor = ħH/2πkB with H=c√(Λ/3). The ratio
  a0/T_floor = √6·c·kB·√π/(4ħ) is **Λ-independent** → a0 = const·T_floor exactly. No hidden power that could amplify a
  small Tolman factor.
- **Tolman law a0_local = a0/√(1+2Φ/c²)** follows from Tolman's theorem T√(−g00)=const (zero tuned input) applied to the
  floor temperature. Cross-checked via the BREAK definition (a0=cH_floor, Tolman on the bath RATE H→H/√(−g00)): gives
  the **identical** law and the **identical c² scale**. The relativistic c² scale is FORCED by the theorem — not a knob.
  Derivation is real.

## (b) Is the a0_local arithmetic right? — YES, recomputed exactly.
- galaxy disk (Φ=−(200 km/s)²): 2Φ/c² = −8.90e-7 → a0_local/a0 = **1.0000004** (+0.000045%)
- cluster core (Φ=−(1500 km/s)²): 2Φ/c² = −5.01e-5 → a0_local/a0 = **1.0000250** (+0.0025%)
- 2× boost needs 2Φ/c²=−0.75, |Φ|=0.375c², escape velocity ~0.61c (BH-horizon scale). Cluster shortfall factor in
  |Φ|: **1.50e4** (matches the doc's ~1.5e4 exactly).

## (c) Does it THREAD? — NO, on both sub-routes.
- **TOLMAN (i):** cluster boost 1.000025× vs the needed 2-25×; differential cluster-vs-galaxy is ~36 ppm — physically
  zero. Does not boost clusters.
- **CURVATURE/DENSITY (ii):** re-derived algebraically. The steelman's "**algebraically identical to the density law**"
  is **loose at O(1)** — exact symbolic forms differ: a0_curv = (c√G/4)√(ρ+4ρ_DE) vs a0_dens = (c√G/2)√(ρ+ρ_DE), a
  nonzero difference. BUT the **load-bearing conclusion is correct**: in every bound system (ρ≫ρ_DE) both scale as
  **√ρ** → cluster(~1e3 ρ_DE) ~14-32×, disk(~1e6 ρ_DE) ~450-1000× → **breaks the 0.13-dex SPARC RAR**. So sub-route (ii)
  IS the banked density null in its operative behavior, just not literally the same O(1) prefactor. **No reading threads
  both.**

## (d) Is the SIGN right? — YES (verified). Φ<0 ⇒ √(1+2Φ/c²)<1 ⇒ a0_local>a0. Deep wells BOOST a0 — the direction
clusters need. The sign is genuinely favorable (contrast the banked EFE +0.218 sign-flip artifact); it is the
**magnitude** (Φ/c²~1e-5 in bound systems), not the sign, that kills it.

## (e) Null-steelman: is the closed-falsifier AIRTIGHT, or a route missed? — AIRTIGHT. Three escape attempts tested
and all collapse to banked nulls or to zero:
1. **Local expansion rate** (floor uses local Friedmann H_local²=(8πG/3)ρ_local): = the density law a0=(c/2)√(Gρ),
   boosts disks 1000× → banked DENSITY null. Not new.
2. **Local apparent-horizon size** (Unruh-wavelength-reaches-horizon, horizon shrunk by local matter): r_AH=c/H_local
   = **191 Mpc at the R500 mean**, ~5350 Mpc cosmic; only ~1 Mpc at ρ/ρ_crit~5e4 (no cluster reaches). → banked
   ELL_DESITTER null (Gpc). Not new.
3. **Nested/cumulative potential amplification** (galaxy-in-cluster-in-supercluster, potentials add): stacking EVERY
   structure scale in the observable universe gives |2Φ/c²| = 1.0e-4, boost +0.005%, still **7000× short**;
   cluster-vs-galaxy differential ~36 ppm. The most aggressive amplification attempt still gives physically zero.
   Closed-falsifier HOLDS.

Literature (web, 2026-06-14) confirms the foundation: the dS-Unruh floor T=√(a²+c²H²/3) tracks the **cosmological**
H/Λ (Milgrom astro-ph/9805346; EUP-de Sitter modified-inertia link, EPJC 2020); and "the local process of ionization of
the accelerating atom has NO relation to the [Rindler/horizon]" — local matter does not reset the horizon-temperature
floor. Sources: Milgrom astro-ph/9805346; EPJC 80 (2020) 08636-x; arXiv:2509.03470 (modified Unruh thermodynamics 2025).

## NET REGRADE
**CONFIRMED NULL — a genuine DERIVED falsifier, not a partial, not a cure.** The dS-Unruh foundation DOES license a
local-potential dependence of a0 (Tolman redshift of the floor — real, zero new input, right-signed), so "does the
foundation license ANY dependence?" = YES honestly. But the foundation DERIVES the scale as c² (relativistic), making
the effect ~1e-5 in every bound system — 4-5 dex short. The only large boost reads the floor off local
curvature/density (√ρ), which breaks SPARC = the banked density null. Three independent escape routes (local-H,
horizon-size, nested-potential) all collapse to banked nulls or to zero differential. **No SPARC-safe in-window derived
scale exists on this route.** The original verdict's two corrections to make precise: (i) the Tolman galaxy boost is
+0.000045% (I get this; the doc's "1.0000005" was for a slightly different Φ convention — same physics, ~1e-6); (ii)
the curvature route is the density null in BEHAVIOR (√ρ, SPARC-breaking) but is O(1)-distinct symbolically, not literally
"algebraically identical." Neither correction changes the grade.

Quarantine held: a0/Z never asserted derived; the c² Tolman scale flagged DERIVED-but-wrong-magnitude; the curvature/√ρ
reading flagged = banked tuned-scale density null. Both ways: the right-sign Tolman effect credited at full weight, then
shown fatally small with explicit numbers (no manufactured cure); full hearing given to three amplification escapes (no
high-priest dismissal). **Bank as closed — the sixth and cleanest local-a0 null.**
