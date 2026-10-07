# CFG394: black-hole spins near 1e9 Msun vs the light end of the wave-field window: STAYS OPEN (and wider than CFG367 said)

Criteria 5aff6a7ba (committed before any table was read). Script `cfg394_light_end.py`, 10/10 checks, MUTATE passes. It runs CFG367's `cfg367_superradiance.py` from its committed bytes (sha256 d78a3812..., checked), and writes each run under `runs/`.

**Verdict.**
- **STAYS OPEN.** 2.01-4.35e-20 eV is not excluded at all.
- **No measurement passes the robust rule.** Six holes with 3e8-3e9 Msun have reflection spins. The only two with reverberation masses fail on spin once the most conservative published fit is taken:
  - PG 0804+761 (6.0e8 Msun): the 2019 fit gives a > 0.97. Mallick et al. 2026, using XMM+NuSTAR broadband data, give only upper limits (a <= 0.931 hard band, a <= 0.706 broadband).
  - PG 1426+015 (1.0e9 Msun, the largest reverberation mass): Walton et al. 2025 get a = 0.77-0.99 from broadband fits, but only if the soft excess is reflection. Their hard band alone gives a > -0.17. Mallick et al. 2026 give 0.44 (+0.49/-0.12). The authors themselves flag the result as model dependent.
- **TIER B (indicative) also excludes nothing.** These are Q2237+305 (a >= 0.71), PG 2112+059 (a >= 0.83) and 1H0419-577 (a >= 0.98). With their virial or "other" masses at 0.4 dex, the CFG367 code excludes nothing in the light end.

**Owner item: CFG367's own light-end edge moves (RUN_COMB, indicative).**
- CFG367's exclusion of 4.5-7.5e-20 came from PG 0804+761 alone. Its 1.5-1.95e-19 exclusion came from Ark 120 alone.
- Seven of CFG367's spins have been re-measured in 2019-2026: PG 0804+761, Ark 120, Mrk 79, PG 1229+204, Mrk 110, RBS 1124 and MCG-6-30-15. Replacing each with the lowest published lower edge removes both exclusions.
- With CFG367's code and masses unchanged, the surviving low piece becomes **2.0-9.7e-20 eV**, with a second survivor at 1.09-2.03e-19.
- CFG367's README headline intervals are therefore optimistic under this lane's conservative R2 rule. I did not edit CFG367; the owner decides whether its README gets a forward note.

**What would decide it** (decider grid: a hypothetical hole run through CFG367's own `mass_range`/`excluded`):
- **No single hole closes the light end.** Even M = 1.0-1.2e9 Msun known to ±10% (1σ) with a >= 0.98 excludes only about 70% of it, e.g. 2.6-4.35e-20.
- **Two holes would.** Both need a robust a >= 0.98 and a mass known to about ±10%: one at about 1.0e9 Msun and one at about 1.5e9 Msun.
- **Mass precision is the binding wall.** At ±20%, every case drops to ≤ 20% excluded. Reverberation masses carry about 0.3-0.4 dex systematics from the f factor, so only GRAVITY-type dynamical masses reach ±10%.
- **Concrete target.** The decisive measurement is a broadband XMM+NuSTAR reflection spin whose lower edge stays >= 0.9 under every soft-excess treatment, for a hole of 0.8-1.5e9 Msun with a dynamical (VLTI/GRAVITY) mass.

**Departures from the frozen file (disclosed).**
1. **Outputs are named per run, not by suffix.** The unchanged CFG367 code writes `cfg367_superradiance[_MUTATE].out`/`_results.json` into each run directory.
2. **Some spins come from SR26, not the primary papers.** For Ark 120 (Porquet+19), RBS 1124, MCG-6-30-15, J19 and Schartel10, the 2019-2026 spins are taken as listed in the SR26 compilation table. W25, SR22 and M26 were read directly.
3. **PG 0804+761 uses M26's mass.** That is the reverberation mass from the AGN BH mass database (log 8.78 ± 0.05), not the empirical 5.5e8 that SR26 and R21 quote. With a spin floor of 0 this changes nothing.
4. **The decider grid was not named in the frozen file.** It uses only CFG367's functions and is descriptive.

**Scope.**
- A gravity-only test. It bounds where the field's mass can be and detects nothing.
- The cold-fluid amount stays free. κ = ½ is fitted.
- No dark-matter particle species is claimed.
