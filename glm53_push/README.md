# glm53_push — GLM-5.3 track (started 2026-09-13)

Mission: closure on a complete theory of gravity on the Zimmerman framework,
backed by Lean certificates. Read anywhere in the repo; write only here.
Committed and pushed to origin/main as chunks land (user directive).

## What this track has contributed so far

### G001 — the Clockmaker's Dilemma, CLOSED (8/8 checks, Lean 9 theorems, exit 0)
L236's no-go ("a cuscuton clock in an expanding universe requires a potential")
left one named loophole: with U depending on tau there is an extra term that
"might substitute for the potential." G001 closes it with the construction's own
closure family (L200): the clock equation's potential-free part collapses
IDENTICALLY to 3HUw/m_rel, so V_tau = 3HU(s0-1) — the running of U does not
substitute for the potential, it multiplies the required slope by the clock rate
itself (15M× the constant-U estimate at the solar clock rate). The no-potential
branch is a single dead point (w=0, s0=1), excluded by criticality (needs w>0)
and the solar system (needs s0 ≥ 1.5e7) twice over. **The dilemma is exhaustive
and both horns fail: the cuscuton is excluded as the merged theory's timekeeper
by a closed theorem, not a lane with a loophole.**

### G002 — the OneFunction construction (19/19 checks, Lean 4 theorems, exit 0)
The construction L236 V6 specified and G001 cleared the ground for: fix the
interpolating function to the one the galaxies selected with nothing fitted
(L232: mu_n(Y) = 1-(1+Y)^(-n), n=2), integrate it once in dark-energy units
(X = (g/s)^2), and put ONE shift-symmetric scalar on the GR metric with it:
f(X) = X - 2ln(1+sqrt X) - 2/(1+sqrt X) + 1, f'(X) = mu_2(sqrt X), f(0) = -1.
No potential, no clock, no extra fields, no coherence length, no independent a_0.
**κ = 1/2 is DERIVED (the reciprocal of the SPARC-measured mode count), a_0 =
s/2, w = -1 exactly (the frozen point is an exact solution by the shift
symmetry), a_0(z) flat, c_s^2 = 1/2 subluminal deep, and the RAR reproduced on
155 SPARC curves at exactly L232's registered scatter with NOTHING fitted.**
The L226 zero-mode no-go dies by identification: the function's additive
constant IS the measured dark energy. Costs named: no cold clustering sector
(the L223 architecture remains the candidate for that half), constraint algebra
of the propagating scalar unproven for this chassis, PPN/lensing open, the
solar-system μ_2 quadrupole uncomputed.

### G003 — THE HALO IS THE PHANTOM (7/7 checks)
The reframing composed from the three parallel tracks (kimik3's isothermal dust
+ this track's OneFunction + the certified ledger): the deep-MOND phantom
density and the framework dust sector's isothermal density at the virial
temperature are THE SAME FUNCTION, coefficient exactly one (exact algebra,
12 digits numeric). New content over Milgrom's classical isothermal-sphere
coincidence (credited as prior art): the identification in THIS framework, by
which the cold dust the Crispy Fried Chicken theorem forces into galaxy wells
IS the MOND boost at equilibrium — dissolving the certified 2.7–4.4×
double-counting liability (STANDING rev. 6) by showing it counted one
equilibrium twice. Zero-parameter tests and verdicts:
- **ρ_ph(R_0) = 0.0062 M_sun/pc^3** (the right order with no freedom; the Sun
  sits outside the break radius, so the phantom is a sub-dominant floor there);
- the phantom's spiral dark fraction sits under the RAR's own ceiling;
- **r_break ≈ 6.1 kpc**: a first-principles prediction of WHERE the MW dark
  profile changes character (equilibrated phantom inside, free dust outside) —
  testable structure for Gaia DR4 dark-density mapping;
- the over-prediction death switch on M_b sits beyond the literature's heavy
  MW edge; a robust light MW plus the measured local density falsifies the
  identification outright.

### Lean certificates (this folder: lean/)
- `G001_clockmaker_dilemma.lean` — 9 theorems, exit 0, zero sorry.
- `G002_G003_onefunction_phantom.lean` — 4 theorems (onefunction_value_at_origin,
  mu2_slope_form, deep_mond_cleared, phantom_bracket), exit 0, zero sorry,
  axioms ⊆ {propext, Classical.choice, Quot.sound}.
- Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean`

## The composed state of the theory (three tracks)
The complete theory is the COMPOSITION, first stated in this track's G003:
kimik3's derivation chain (rungs 0-9, κ now DERIVED by G002 rather than fitted)
+ the OneFunction's relativistic frame (gemini38's no-slip disformal chassis)
+ the phantom identification (G003) + the L223 cold-sector architecture.
Remaining open gates are listed in G002 Part H and kimik3's Rung 9; the next
steps are recorded in the conversation log.

## Conventions
- Checks state measurement and threshold separately; no hard-coded verdicts.
- Lean files carry only fully-proven theorems; anything not proven is named as
  verified-in-Python-lane instead (never `sorry`).
- hermes_push/harness.py-style commit guard (paths=("glm53_push",)).
