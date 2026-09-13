# kimik3_push — track state (read at session start, rewrite at each milestone)

**Mission:** get closure on a complete theory of gravity on the Zimmerman framework, backed by Lean
certificates (zero sorry, Mathlib available), with Kepler-grade testable predictions recorded.

**Constraint (user directive):** READ anywhere in the repo, but WRITE ONLY into `kimik3_push/`.
Keep all changes UNCOMMITTED until the user commits them later. The commit guard is
`hermes_push/harness.py`; it also flags `__pycache__/*.pyc` — clean before running it.

**Build note (NEW, this session):** Mathlib IS installed for Lean 4.34.0-rc2. Build location:
`/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026/.lake/packages/`.
To compile a single file with Mathlib:
```
cd fable_independent_2026/lean_2026
LP=$(for d in .lake/packages/*/.lake/build/lib/lean; do [ -d "$d" ] && printf '%s:' "$(cd "$d" && pwd)"; done)
env LEAN_PATH="${LP%:}" lean /path/to/file.lean
```
`Real.pi` is available via Mathlib (the old no-Mathlib note in CONTEXT_DIGEST is stale). Bare-core
`lean` only works for Bool/finite; real analysis needs the LEAN_PATH above. Zero-sorry check:
`grep -cE '(^|[^`])\bsorry\b([^`]|$)' file.lean` (exclude comments).

---

## The frontier this track attacks (as of 2026-09-13)

The programme's standing blocks (README rev. 20) and FRIED_CHICKEN.md agree: the ONE open
requirement for a complete theory is **Requirement 10 — the amplitude law**,
`rho = sqrt(G M_b a0)/(4 pi G r^2)` as a *dynamical consequence*, not initial data. It has been
PROVEN a formation/virialisation question, not an equation-of-state question:
- `collapse_2026.py`: no barotropic EOS `c_s^2(rho)` gives both flat curves AND the BTFR.
- `local_selection_2026.py`: no LOCAL covariant selection rule on realistic baryons works
  (the invariant `g_b^3/|grad g_b|^2 = G M_b/4` is exact for point/Hernquist but varies 1.41x
  across an exponential disk, 1.19x Plummer).
- Conclusion (FRIED_CHICKEN.md): the sector must have thermalised in the region `g_b > a0` and
  KEPT that virial temperature — i.e. **collapse history: multi-streaming, caustics, violent
  relaxation**. "It is the one route this programme flagged twice as unrun and never ran."

**The one remaining question (verbatim):** *Does the dark sector virialise at the MOND radius?*
Given `sigma^2 = G M_b/(2 r_M)`, `r_M = sqrt(G M_b/a0)`, the profile, its coefficient, and the
BTFR all follow with no freedom. `virialisation_2026.py` proved the confinement radius is FORCED
to be ∝ r_M (dimensional theorem, unique solution — the sector has no galactic length of its own,
`c^2/a0 = 31112 Mpc`). What is NOT proved is that it *settles* there.

## Certified necessity (L166, Lean) — what any completion must contain
(i) a real clustering cold component with retained fraction f rising with host mass;
(ii) a non-barotropic effective fluid; (iii) a locally screened preferred-frame source.
Ledger anchors: SPARC spiral f<=0.105 strict; MW 0.14; X-COP cluster 0.576; CMB >=0.988.

## FABLE 5.1 parallel track (running elsewhere — do not duplicate, build off if applicable)
- FABLE is at L240 (HEAD commit a9f9a2340). Its frontier: the photocount/EFE ambiguity, n=2 empirical.
- The two tracks are a PROVEN fork (L236): cuscuton-clock track and parameter-free-curve track
  assign U differing by 6.9e13 to the same coefficient; merge is arithmetically impossible.
- FABLE's dSph result (L240): both surviving EFE laws OVER-SUPPRESS classical dwarfs (a
  pre-existing MOND dwarf problem, not the new physics). Wide-binary prediction gamma_v(20 kAU)
  = 1.095–1.111, BELOW the registered Arm-A band — falsifiable.

## K-track lanes (this folder)
| Lane | Goal | Script | Status |
|---|---|---|---|
| K001 | 3D collisionless cold-collapse N-body: does the sector settle at r_M isothermal? | scripts/K001_*.py | RUNNING (subagent) |
| K002 | Lean-certify the collapse/BTFR algebra (Mathlib) | lean/AmplitudeLaw.lean | RUNNING (subagent) |
| K004 | Testable-predictions ledger (Kepler-grade) | predictions/PREDICTIONS.md | RUNNING (subagent) |
| K005 | Analytical spine of the formation route | scripts/K005_formation_spherical_infall.py | DONE 16/16 PASS, pushed |
| K006 | Controlled spherical self-gravitating collapse (shell code) | scripts/K006_spherical_collapse.py | RUNNING |

## Milestones (newest first)
- **2026-09-13 physics note (collapse modelling):** the framework's dark sector is a
  cuscuton-like condensate whose perturbations are NON-PROPAGATING (c_s^2 = 0 exactly on the
  critical surface, isotropic stress = clustering cold component; L192/L193), carried by the
  Noether charge of the shift symmetry (L217). => it clusters and self-gravitates as
  COLLISIONLESS DUST. Therefore a collisionless N-body (K001) is the CORRECT instrument for the
  formation question; a hydrodynamic treatment is not.
- **2026-09-13 numerics note:** a spherical SHELL code cannot do this problem. At top-hat collapse
  every shell reaches r~0 simultaneously, the potential diverges, and r=|r| reflection injects
  uncontrolled energy (measured dE/E ~ 1e6, r_half runaway). K006/K007 shell runs are SUPERSEDED;
  the formation test is K001's 3D numba N-body (validated to machine precision, adaptive dt).
- **2026-09-13 Lean certificate (pushed f931b4f89):** kimik3_push/lean/AmplitudeLaw.lean -- 10 theorems
  (a0_pos, rM_pos, rM_sq, btfr_virial, btfr_exponent, profile_slope, monomial_dim_length,
  mond_length_unique, mond_length_form, vc_flat), exit 0, ZERO sorry, axioms subset of
  {propext, Classical.choice, Quot.sound}; independently recompiled and re-grepped. Certifies the
  ALGEBRA of the amplitude law / BTFR / dimensional-uniqueness of r_M. Mathlib now available
  (8557 oleans) -- the old bare-Bool fallback is obsolete.
- **2026-09-13 predictions ledger (pushed f931b4f89):** kimik3_push/predictions/PREDICTIONS.md -- the
  numbered falsifiable ledger (Gaia DR4 Arm A/B; a0(z) flat vs evolving + z~2.5 BTFR zero-point;
  w_dm > 0 and the w <= 5.7e-7 window; Saturn 5.84e-16 m/s^2 power-law tail NEW both footings; etc.)
  with values, kill conditions, LCDM contrast, deciding instrument, pre-registered vs NEW flagged.
- **2026-09-13 K005 (16/16, pushed f3a2b229c):** the amplitude-law algebra is self-consistent and the
  BTFR emerges. (a) The local invariant g_b^3/|grad g_b|^2 = G M_b/4 is EXACT for point + Hernquist
  (the right temperature is available locally). (b) Cold-shell infall at r_M gives a virial
  temperature within the orbit-averaging factor (~2) of the target G M_b/(2 r_M). (c) r_M and sigma^2
  both scale as M_b^0.5 exactly (BTFR). (d) rho=A/r^2 gives an exactly flat curve with v_c^4 = G M_b a0
  coefficient 1. (e) HONESTY CONTROL: the invariant is NOT constant for an exponential disk (spread
  12.1x across 0.5-3 r_M) -- reproduces the documented no-go: no LOCAL covariant rule selects the
  temperature on realistic baryons; it must be set by collapse HISTORY. This is why K001/K006 exist.

## Testable predictions collected (see predictions/PREDICTIONS.md)
- (pending K004)


---
*Log format: append dated milestone entries below this line, newest first.*
