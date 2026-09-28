# CFG23 — the ΛCDM control in the same machinery

Scripts:
- `CFG23_lcdm_control.py`, about 15 s. The lane.
- `CFG23_diagnostics.py`, about 10 s. Post-hoc diagnostics, written after the main run and labelled as such.

Each has `.out` / `_results.json` outputs and a MUTATE run:
- The lane's MUTATE caps halos at 10¹¹ M☉, and H1 and H1p fail.
- The diagnostics' MUTATE halves c on the analytic side, and V1 fails.

## Question

CFG21/22 found that KiDS's isolated lenses and the Local Group's zero-velocity radius exclude a universal phantom edge at 5–7σ. Is that conflict specific to the framework's phantom? Or does it also hit standard halos scored the same way?

## Method

- **The model:** NFW halos, with Duffy+08's c(M200m) and Tinker+10's bias as the 2-halo cap.
- **The same machinery:**
  - KiDS: FP1/L355 with FP20's exact projector and CFG16's fitting algebra.
  - LG: FP1's integrator, run as Newton + Λ.
- **Revisions (disclosed in the docstring):** made after the first (MUTATE) run and before the main run, to give the control what the framework was given:
  - a 2-halo amplitude in [0, bias];
  - an edge x_t R200m, scanned;
  - MW in bin 3 and M31 in bin 4;
  - a tested fitter;
  - a reading that requires a KiDS fit.
- **A declared range that was wrong:** the first-written C2 range (2–5 × 10¹² M☉) was the timing-argument mass. This integrator returns the zero-velocity-surface mass, 1.57 × 10¹² M☉ at R₀ = 0.93. It stays scored as a failure.

## Results

**Controls pass.**
- The fitter reproduces the committed numbers to 1e-9: BASE 139.800159, and CFG21's 104.685832.
- FP1's LG control reproduces 1.9290 / 2.0214 Mpc.
- The NFW projection matches the analytic ΔΣ (Wright & Brainerd 2000) to 2.7 × 10⁻⁴ (diagnostic V1).

**KiDS.** Duffy-c NFW with a linear 2-halo misses KiDS: best χ² 173.7 against the framework's 104.7, so H1p fails. The first-written H1 also fails, at 178.2.
- **Where it misses:** the misfit sits at R ≥ 0.6 Mpc, where the data lie 1–3σ per point above the model (V2). That is the vanilla halo model's transition region.
- **Concentration:** with c × 0.7 and an extended 1-halo, the same model reaches **χ² 99.3**, better than the framework's 104.7 (V3).
- **So KiDS does not prefer the framework** over standard halos in this machinery.

**The KiDS–LG tension for standard halos** (CFG21's statistic; shared: the edge and the two halo masses):

| variant | T_min | ≈ σ | R₀ (Mpc) |
|---|---|---|---|
| baseline (Duffy c, Tinker cap, LG M_b 1.145e11) | 55.4 | 7.4 | 1.80 |
| c × 0.7 (the KiDS-competitive variant) | 72.5 | 8.5 | 1.89 |
| c × 1.4 | 38.2 | 6.2 | 1.66 |
| x_t = 1 only (the halo-model convention) | 24.5 | 4.9 | 1.52 |
| MW in bin 4 | 65.2 | 8.1 | 1.80 |
| the framework, for comparison (CFG21, canonical) | 26.2–27.8 | 5.1–5.3 | — |

- KiDS gives the bins holding the MW and M31 halo masses of log M200m ≈ 12.45 and 12.60.
- Those put a standard-halo Local Group at R₀ = 1.5–1.9 Mpc against 0.93 ± 0.12.
- **The conflict is at least as large for ΛCDM halos as for the framework's phantom.**

The pre-declared reading (f) is void because the baseline control fails KiDS. The numbers above are reported, not scored.

**The cold budget against KiDS's own best (V4, framework-specific).** CFG12/16/17 judged the budget window with CFG4's tolerance: +9 against the untruncated law. KiDS itself beats that reference by 35–38. Against KiDS's own best edge, the budget's edge costs:

| case | budget edge x_e | KiDS cost | ≈ σ |
|---|---|---|---|
| canonical P2 | 0.348 | 40.9 | 6.4 |
| canonical ν_mono | 0.346 | 47.8 | 6.9 |
| alt P2 | 0.300 | 55.4 | 7.4 |
| alt ν_mono | 0.298 | 62.0 | 7.9 |

## Standing

**1. CFG21/22's 5–7σ is not a framework-specific failure.** Standard halos fitted to the same lenses hit the same Local Group wall, harder. The weak link is the Local Group's spherical R₀. Either the spherical, isolated timing model is too tight, or the MW and M31 are light for their stellar masses.

**2. KiDS does not discriminate between the framework and standard halos here.** A reasonable concentration fits it slightly better than the framework.

**3. The budget window is open only under the lenient tolerance.** Against KiDS's own best edge it is closed at 6.4–7.9σ.
- **Caveat:** the same linear 2-halo template that makes Duffy-c halos miss R ≥ 0.6 Mpc may be understating the lens's surroundings here too.
- Whether the framework's own surroundings can supply that signal inside its cold budget is the open question the next lane has to face.

Nothing here says the theory is closed.
