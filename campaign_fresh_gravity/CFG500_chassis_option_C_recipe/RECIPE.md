# Candidate B as a recipe (chassis option C), specification v1, 2026-10-08

This is candidate B stated without the relativistic khronon chassis, as CFG469's option C proposes and the owner asked
to pursue on 2026-10-08 ("try both A and C"; CFG499 does A). It is an **effective recipe**, not an action. Nothing in it
is derived from a Lagrangian. Its relativistic sector is **untested, not passed**.

- κ = ½ is **FITTED**.
- The cold energy's **mass is required**. No dark-matter particle species is added.
- The supply postulate is an **input**.
- This is not "theory closed".

Scoring and consistency checks: `cfg500_recipe_scoring.py` (outputs `cfg500_recipe_scoring.out`,
`cfg500_results.json`). Frozen rules: `FROZEN_CRITERIA.md` (21b1db999).

Status words used below:
- FITTED: set by a fit to data.
- DATA: a measured quantity.
- DECLARED: chosen, not derived. This covers functions, constants, rules and discrete choices.
- DERIVED: follows from listed items with no further choice.
- NUISANCE: refitted per data set.
- HYPOTHESIS: the law's form itself (not counted, as in CFG469).

---

## 1. Ingredients

**Matter content.** Baryons, and the **cold energy**, a cold clumping component with the cosmic amount Ω_c h² = 0.12
(FITTED, as in ΛCDM). The cold energy is not a particle species added to the Standard Model by this recipe. Its
microphysics is unspecified. The fluid/order-parameter reading (CFG288 road W, FL1) is one interpretation; the recipe
does not depend on it.

**Gravity.** Ordinary Newtonian gravity sourced by all real mass, ∇²Φ = 4πG(ρ_b + ρ_c), inside bound systems. On the
background, ordinary GR with ρ_b, ρ_c and dark energy (rule B1).

## 2. The rules

### LAW (HYPOTHESIS). The acceleration scale and the target law
- a₀(t) = κ c √(G ρ_DE(t)).
  - a₀ tracks the dark-energy density. It is **flat only if w = −1**.
  - On the canonical footing ρ_DE is ρ_Λ: a₀ = 9.3603e-11 m s⁻². On the alt footing ρ is ρ_crit: a₀ = 1.1312e-10 m s⁻².
- In a bound, owned system the total field obeys g = ν(|g_b|/a₀) g_b.
  - g_b is the Newtonian field of the system's own baryons, gas pressure included.
  - The "phantom" density is ρ_ph = (1/4πG) ∇·[(ν − 1) g_b]. It is a **target that the cold energy fills**, not a new
    force (working model 10-06, eq. 2).
- Tested by: SPARC (GATES 1.01), MeerKAT (CFG301/309), a₀(z) (CFG6, PAPER38: calibration wall), Gaia DR4 (pre-registered).

### F1 (FITTED). κ = ½
- Fitted on SPARC.
- CFG493 measures κ = 0.417 ± 0.095 (canonical) and 0.345 ± 0.078 (alt). That is consistent with ½ but does not
  discriminate.
- **The kernel moves κ.** Switching ν_mono to the quadrature form moves every route by +0.06 to +0.09 dex (κ_Λ 0.417 →
  0.489, CFG493). That shift is larger than the ½ vs 1/√π gap. κ must therefore be refitted whenever the kernel changes.

### FT (DECLARED DISCRETE CHOICE). Footing
- ρ in the law is ρ_Λ (canonical) or ρ_crit (alt).
- The recipe is run as two parallel recipes, never pooled.

### D1 (DATA). ρ_DE(t)
- From the background (ΛCDM, or a DESI branch).
- Growth passes with DE-tracking a₀ (CFG439, 512³, 0.033).

### K1 (DECLARED FUNCTION) + K1a (DECLARED CONSTANT). The kernel ν_mono
- ν_RAR(y) = 1/(1 − e^{−√y}) up to y* = 2.3374, then a monotone logarithmic splice with δ = 0.05. y* follows from δ by
  tangency, so only δ is a constant (`CFG5_common.py`).
- Tested by:
  - GATES 1.01 (0.1003 dex) and 1.05 (P2 disfavoured at about 2σ);
  - CFG468 (the kernel family): frozen criteria b0d7274a0, **no committed result**.
- Bare ν_mono is **not** Solar-System safe (CFG185). It needs S2.

### S1 (DECLARED RULE). The bound-only switch
- The law acts only in bound regions. It is exactly off on the FRW background and in linear parcels (CFG487).
- Tested by: CMB lensing 1.000 (−0.39σ) and forest deviation 0.00 (GATES 3.02 / 3.12).
- **Gap 1** (a legal, derived switch) stays open. CFG487's settled-fraction switch fails with the 5.85 r_M edge.

### S2 (DECLARED RULE). Ownership
- Each system carries the phantom of its own baryons. The host's external field does not enter (no EFE).
- The Sun carries no phantom.
- Globulars are class E, formed embedded without cold energy, so they are Newtonian.
- Tested by:
  - Cassini Q2 PASS, margin 2.0e4–3.3e4 (GATES 4.01);
  - globulars COND, tile FRAGILE (CFG465);
  - Chae EFE FAIL in 3 of 4 cells (GATES 1.15);
  - SPARC EFE slope, a +1.8σ lean against no-EFE (CFG491);
  - Gaia DR4 Arm C, γ̂ = 1.000 pre-registered.
- Not derived. Under option C the question "ownership from an action" is retired: ownership is declared.

### E1 (DECLARED CONSTANT). The lensing edge x_e = 0.4
- The phantom support for isolated-lens lensing ends at x_e = 0.4 (GATES 3.05 / 3.09).
- KiDS passes with it: Δχ² −12.4 / −11.3 for ν_mono.
- Not derived. The derived splashback edge fails (GATES 3.09).

### F2 (FITTED). The cold energy's amount
- Ω_c h² = 0.12, so S = Ω_c/Ω_b = 5.364.
- Not derived (CFG288, CFG360). CFG496 finds no cold-energy–dark-energy link (0 of 15 candidates).

### E2 (DECLARED RULE). The supply postulate
- Each galaxy settles S × M_b of cold energy inside its edge, where M_b is its original baryons.
- **Not derivable on six attacks** (STANDING 10-08):
  - CFG461, temperature: no class passes;
  - CFG462, khronon lapse: exhaustion only;
  - CFG488, co-settling: restatement;
  - CFG490, direct couplings: no Lagrangian coupling delivers;
  - CFG494, adiabatic initial conditions: relabel;
  - CFG497, binding-energy threshold: 0 of 10 candidates.
- It stands as an input.

### E3 (DERIVED given E2, the law, κ, f_b). The growth edge
- r_edge = r_M / ln(1/(1 − f_b)) = 5.85 r_M. This is where the phantom has used exactly S × M_b (CFG423/424).

### E4 (DECLARED RULE). Per-catchment mass conservation
- The phantom excess inside each halo's edge is drawn from the cold energy of the same halo's turnaround catchment, in
  proportion to the local cold density.
- The catchment uses the ΛCDM spherical-collapse Δ_ta(z).
- The added source sums to zero on every catchment.
- Tested by:
  - CFG424 (256³: 0.027 / 0.029);
  - MUTATE with no compensation: TENSION, max|P−1| 0.154;
  - CFG425, CFG426, CFG427, CFG439, CFG460: 16/16 runs including 512³ in two realisations (0.033, 0.040), on both
    footings, with DE-tracking a₀.

### E5 (DECLARED RULE). Max rule (T5)
- In clusters the dark mass is max(phantom, cosmic share).
- Tested by: X-COP identity 0.946 ± 0.080 (GATES 2.01); Bullet 4.6× / 4.9× (GATES 2.02).
- The supply limit does **not** set the cluster or group level:
  - CFG379 FAILS;
  - CFG497 bonus: FAIL by 0.007 / 0.008 at b = 0.

### R1 (DECLARED RULE). Relaxation
- The cold energy relaxes toward ρ_ph at a rate Γ. This is bookkeeping: no settling force is derived.
- Tested by:
  - CFG464: the λ = 1 t_dyn rate is NOT EXCLUDED;
  - CFG431: one clock is not universal (FRAGILE);
  - CFG461: no class sets σ⁴ = G M_b a₀/4 with G9 intact.

### R1c (OPTIONAL RULE, counted only if used). The settling clock (CFG487)
- Dm/Dt = Γ L (1 − m), with Γ = √(4πG ρ_X) (λ = 1) and a latch L at turnaround. The clock never resets.
- **V1** reads the cold energy. That is an **MS1 exception**: not admissible under the original MS1.
- **V2** reads the baryons (strict MS1).
- Tested by CFG487:
  - with the 5.85 r_M edge, both versions FAIL on SPARC (alt) and KiDS;
  - V1 alone, with no edge, passes KiDS (+2.05 / +0.71) and SPARC, but in growth it overdraws the cold supply (TENSION).
- CFG498 (clock taper + capped conservation) is **PENDING**.

### L1 (DECLARED RULE). Lensing
- Light is bent by GR lensing of the effective dark density.
- Tested by: KiDS (GATES 3.05) and SLACS (GATES 1.19, marginal).
- CFG495's drawdown cannot be tested by KiDS.

### B1 (DECLARED RULE). Background
- GR + cold energy + dark energy at all times.
- CMB, BBN and BAO are therefore standard **by declaration**, not predicted (GATES 3.01 / 3.04 / 3.13).

### G1 (DECLARED RULE). Gas pressure
- g_b includes gas pressure.
- Growth is insensitive to the gas filter (CFG427).

### N1 (NUISANCE). Stellar M/L
- Per data set (GATES 1.01: one global Υ_disk of 0.5–0.8 on SPARC).

### Inherited engine settings (reported, not counted)
- The T1 switch ε = 0.077 and the MIX-A filter in the growth engine. CFG427 shows the pass is insensitive to both.

### Retired by option C
- "G = measured G (no α_c/2 correction)" (CFG469). Without a khronon there is no correction to declare away, and Newton's
  G enters as in any theory.

## 3. Constant count

| class | n | items |
|---|---|---|
| FITTED | 2 | κ; Ω_c h² |
| DATA | 2 | ρ_DE(t); f_b |
| DECLARED FUNCTION | 1 | ν_mono |
| DECLARED CONSTANT | 2 | δ = 0.05; x_e = 0.4 |
| DECLARED RULE | 9 | switch S1; ownership S2; supply E2; catchment conservation E4; max rule E5; relaxation R1; lensing L1; background B1; gas pressure G1 |
| DECLARED DISCRETE CHOICE | 1 | footing |
| NUISANCE | 1 | M/L |
| **total** | **18** | +1 if the settling clock R1c is used; 2 inherited engine settings not counted |

**Reconciliation with CFG469's 15** (2 fitted, 2 data, 1 declared function, 9 rules or constants, 1 nuisance): 15 + 3 = 18.
- **+1** δ is split out of the ν_mono row.
- **+1** CFG469's growth-edge row is split into the supply postulate E2 and catchment conservation E4. The edge E3 itself
  is derived from them.
- **+1** the max rule T5 is added. It is in CFG7's B ledger ("declared 5") and carries X-COP, but CFG469's table omits it.
- **+1** the footing choice is added.
- **−1** "G = measured G" is retired (above).

## 4. Where each item is tested, and where it fails

See `cfg500_recipe_scoring.out` §2 for the 29 status-board tiles. In short:

**PASS under C (5):**
- SPARC;
- MeerKAT a₀;
- KiDS;
- clusters + Bullet;
- M31 and Local Volume dwarfs.

**COND (3):**
- globulars;
- Milky Way ultra-faints (CFG344);
- growth (B).

**UNDEC (4):**
- a₀(z);
- halo-free high z;
- CRISTAL/ALESS;
- SLUGGS (four centrals: ROBUST FAIL, CFG466).

**OPEN (3):**
- DR4;
- why κ = ½;
- the cold-energy amount.

**DECLARED (1):** ownership.

**PARTIAL (1):** Solar System. Cassini Q2 passes via ownership; PPN is untested.

**UNTESTED (10):**
- GW speed;
- the two well-posedness tiles;
- the lapse;
- pulsars;
- strong coupling;
- G9;
- G0;
- black holes;
- G12.

**MOOT (2), not passed:** the ungated zero-field FAIL, and the chassis-alone growth FAIL.

**Relativistic predictions that become unavailable:**
- the GW speed and polarisations;
- the full PPN set;
- binary pulsars and neutron-star sensitivities;
- BBN and the CMB (assumed, not predicted);
- black holes (shadows, ringdown, moving holes);
- strong field and collapse;
- Φ = Ψ as a derivation;
- preferred-frame effects;
- the Cauchy problem, DOF and ghost count, strong coupling and radiative stability.

**Results lost with the chassis.** None of these is a pass of B.
- **CFG373:** the zero-constant lapse carrier of the target.
- **CFG381:** the sink needs +1 constant.
- **CFG462:** a FAIL, so nothing is lost.
- **CFG483:** the khronon-boundary class gives σ⁴ = G M_b a₀/4 exactly, given the cosmic budget. Its edge is 4.02 r_M, its
  falsifier is UNDECIDED at 256³, and it is not on STANDING.
- **The khronon tie** κ = 2√(8π)/(3β), with β = 6.684 not derived.

## 5. Internal consistency

- **C1, CONFLICT: the lensing-edge clash.** Growth needs E2 → E3 + E4. Applied to real lenses, the 5.85 r_M edge fails:
  - KiDS (+60.5 / +70.6, CFG487);
  - SPARC alt dwarfs (A3 0.864, CFG487);
  - early-type levels (χ² 30.5 / 38.1 vs ≤ 12.59; CFG485, CFG494, CFG497).

  KiDS passes only with E1 (x_e = 0.4). Possible resolutions:
  - **Hand-set (on record).** One support x = 0.4 r_ta for both.
    - It passes KiDS (+0.79 / +2.16, CFG413), growth at 512³ (0.080 / 0.0996, CFG414, alt knife-edge by 0.0004), SPARC
      and early types.
    - But it is hand-set, which the owner's 10-07 rule forbids. CFG414 also uses the hand-set R_c = 3 Mpc/h and no
      per-catchment conservation.
  - **Zero-knob clock taper (CFG487 V1).** It passes lensing and SPARC, and fails growth (TENSION).
  - **CFG498:** PENDING.
- **C2, CONDITIONAL CONFLICT.** The settling clock used as the support (no edge) overdraws the cold supply in growth:
  CFG487 V1-CATCH, max|P−1| 0.174 / 0.202, TENSION.
- **C3, rule conflict if V1 is adopted.** The V1 clock reads the cold energy, which violates MS1. V2 (strict MS1) fails
  KiDS (+6.2 / +11.1).
- **C4, TENSION.** The supply limit cannot set the cluster, group or Milky Way levels (CFG379; CFG497 bonus). The X-COP
  tile still passes through E5.
- **C5, CONSISTENT.** The switch is exactly off on FRW, matching the background rule.
- **C6, DEPENDENCY.** The kernel fixes κ (CFG493).
- **C7, UNTESTED.** Relaxation has no force. Mass is conserved per catchment, but energy and momentum are not tracked,
  and G9 is untested under C.

**Verdict (frozen rule): C VIABLE WITH CONFLICTS (C1, C2).** No tile fails beyond the board's known fails. C1 is resolved
on the record only by a hand-set support, and otherwise waits on CFG498.

---

## 6. Candidate B as a recipe, in plain language (one page, for the foundation programme)

**What it is.** Candidate B is a set of instructions for computing how things move under gravity. It is not yet a
complete physical theory: no single equation of motion (an "action") produces it. That is the honest status.

**The one idea.** Galaxies stop following Newton below a tiny acceleration a₀. The recipe ties a₀ to the density of
dark energy: a₀ = κ · c · √(G ρ_DE). The number κ = ½ is measured from galaxy rotation curves, not derived. If dark
energy changes over cosmic time, a₀ changes with it. If it does not, a₀ is constant.

**What else it needs.** Like standard cosmology, the recipe needs a cold, clumping component with about five times the
mass of ordinary matter. Here we call it "cold energy". The recipe does **not** add a new particle, but it **does**
need that mass, and it does not explain how much there is.

**The rules, in words.**
1. Inside bound systems such as galaxies, the cold energy settles into the shape that makes the galaxy follow the a₀
   law exactly. Its shape is fixed by the visible matter alone. This is why rotation curves are so tight.
2. Outside bound systems the law is switched off, so the universe as a whole expands as in standard cosmology.
3. Each system carries its own extra pull. The Sun carries none, which is why the Solar System looks exactly Newtonian.
4. Each galaxy settles only its own cosmic share of cold energy, drawn from its own neighbourhood. This keeps structure
   in the universe from growing too fast. It is assumed: six attempts to derive it have failed.
5. In clusters, the dark mass is whichever is larger, the law's target or the cosmic share.
6. Light is bent by all of this mass exactly as in Einstein's gravity.

**How many choices it makes.** Eighteen: two numbers fitted to data (κ and the cold-energy amount), two measured inputs,
one chosen curve shape with one shape constant, one chosen lensing edge, nine stated rules, one choice of which density
sets a₀, and the usual star mass-to-light ratio.

**What it gets right** (committed tests):
- galaxy rotation curves (0.10 dex scatter);
- a₀ measured locally with MeerKAT;
- weak lensing around isolated galaxies;
- galaxy clusters and the Bullet Cluster;
- Andromeda's and nearby dwarfs;
- solar-system orbits (by rule 3);
- the growth of cosmic structure (by rule 4, in 16 of 16 simulations).

**What it does not yet get right, or cannot decide:**
- the Milky Way's faintest dwarfs (only conditionally);
- four giant galaxies at group centres;
- whether a₀ changes with time (today's data cannot tell);
- a ready-made clash: the edge that makes structure growth work is too small for the lensing data. One hand-chosen edge
  satisfies both. A rule-based fix is being tested now (CFG498).

**What it gives up by being a recipe.** It cannot predict anything that needs a full relativistic theory:
- the speed of gravitational waves;
- binary pulsars;
- the fine details of solar-system relativity;
- black holes;
- the early universe beyond "same as standard".

These are **untested, not passed**. The relativistic version (option A, CFG499) is the route to them.

**The two tests that can change the picture:** Gaia DR4 wide binaries (2 December 2026; the recipe predicts exactly
Newtonian), and a₀ at redshift about 2.5.

**What it is not.** It is not a closed theory, not a derivation of κ, and not evidence that the data favour this
framework over standard cosmology or MOND (CFG491 finds no on-disk test that singles it out).
