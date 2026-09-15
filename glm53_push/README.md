# glm53_push — GLM-5.3 track (started 2026-09-13; README refreshed 2026-09-14 night)

Mission: closure on a complete theory of gravity on the Zimmerman framework,
backed by Lean certificates. Read anywhere in the repo; write only here.
Committed and pushed to origin/main as chunks land (user directive).

## START HERE (the track at a glance)

| document | what it is |
|---|---|
| `STATE.md` | **THE FINAL BOARD** — the theory in one document: the central chain rung-by-rung with lanes and commits, the completion, the cluster resolution, the honest record (kills/anomalies), the registered tests with dates, the artifacts, the Lean inventory, the open items. |
| `REFEREE_ATTACKS.md` | **THE DEFENSE** — the paper's complete attack surface: every objection (solar system, lensing, wide binaries, clusters, the sag, CMB, growth, a0(z), n=2), the response status (ANSWERED / ARMED / OPEN-HONEST), the lane that owns it, and the response matrix (what observation kills what). |
| `THE_EQUILIBRIUM_THEORY.md` | the capstone narrative. |
| `G051_master_table.*` | **the numbers**: every registered number recomputed from certified constants on both footings — 19 PASS / 4 CITED / 0 FAIL at the 2% drift gate (worst +0.48%); replayable in one command. |
| `lean/` | 12 certificates, 104 theorems, zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}. Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean` |

## THE HEADLINE (what this track now claims)

One scalar with zero free parameters beyond a0: rho_Lambda = 4a0^2/(Gc^2)
-> sigma^2 = sqrt(G M_b a0)/2 (rung 4, DERIVED — three independent routes,
G046/G056/Q001, c_deep = 1 exactly) -> rho_ph = sqrt(G M_b a0)/(4 pi G r^2)
(coefficient 1, Lean) -> v^4 = G M_b a0 (BTFR) -> g^2 = a0 g_N (deep RAR).
The relativistic completion (frozen scalar, hy4 H011): Lorentz invariant,
PPN-clean by structure (alpha1 = alpha2 = 0), phi_dot = 0 attractor
(14/14), LCDM-exact background (w = -1), c_s^2 in [1/2, 1) stable through
the transition, parameter count zero. Cosmology: Omega_Lambda =
32 pi a0^2/(3 H0^2 c^2) = 0.6857 at +0.07% — a Lean theorem (G058), not a
fit. Clusters: two-regime resolution (H012) — cold dust in the Newtonian
core, equilibrated phantom in the MOND outskirts, shape zero-parameter,
falsifier = core slope (-1 NFW vs ~-1.5). The RAR's outer sag resolved to
an observational channel (asymmetric drift, G057) with the sigma_z
calibration test named. The one open derivation: the cluster amplitude
partition (G059 tested, honest negative — the certified mu2 kernel
delivers 0.571/0.615, a parameter-free lower bound; the residual is the
free dust's astrophysical normalization, as in LCDM).

## LANES (G001–G059, each `.py` + `.out` + `_results.json` where applicable)

Every lane is committed with its pre-registered verdicts; FAILs are
findings. Highlights by phase:

- **G001–G003** (2026-09-13): the Clockmaker's Dilemma closed (Lean 9);
  the OneFunction (kappa = 1/2 derived, Lean 4); THE HALO IS THE PHANTOM
  (coefficient exactly 1; r_break ~ 6.1 kpc) — see EARLY HISTORY below.
- **G004–G018**: the pincer (Cassini G005, wide binaries G006, bimetric
  G007 CLOSED, clusters G008/G012/G016/G017, photocount G009 KILLED,
  a0(z) G011, RAR floor G013, DR4 bands G018).
- **G019–G033**: Z theorem; growth gates (G020 OPEN-UNCONFIRMED); CMB
  phase (G021, 40x Planck precision kill surface); Lyman-alpha (G022/G023
  +0.98%/+1.60% at z=3); DESI pointwise (G024); the GR fluid action
  (G031, 9/9 sympy-exact — the scaling closes at the action level); Horn A
  (G032: alpha1 = 0 by architecture); the website bundle (G033).
- **G034–G044**: the local k^4 operators all dead (G030/G034); the
  attractor KILL (G035 — the kill that became the discovery); the radial
  scatter function (G036, white-noise floor 0.045); the mass plane (G040);
  the literature sweep (G041); the Wang+2026 answer (G042, 14/14); the
  mimetic routes closed (G043/G048); the EFE split NOT ESTABLISHED (G044,
  p = 0.114 after the pre-committed audit).
- **G045–G059** (2026-09-14 night, the big swing): the completion's
  cosmology (G038, 6/6); rung 4 DERIVED (G046/G056); the cluster
  hydrostatic split (G050, 2/7 honest) + the 12-cluster table (G057b);
  the frozen-scalar cosmology (G054, 14/14 attractor) + Lean (G055);
  the sag parameter-space exhaustion (G057: asymmetric drift closes it);
  the one-constant closure (G058 Lean); the partition function (G059
  corrective: honest negative); the master table (G051); the salvaged
  EFE-cap certificate (G047).

## Conventions

- Checks state measurement and threshold separately; no hard-coded verdicts.
- Lean files carry only fully-proven theorems; anything not proven is named
  as verified-in-Python-lane instead (never `sorry`); trimmed theorems name
  their exact Mathlib blocker.
- Pre-registration before computation for every gate with a threshold.
- hermes_push/harness.py-style commit guard (paths=("glm53_push",)).
- Additive record: nothing deleted, history never rewritten.

---

## EARLY HISTORY (2026-09-13 morning, preserved)

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
equilibrium twice.