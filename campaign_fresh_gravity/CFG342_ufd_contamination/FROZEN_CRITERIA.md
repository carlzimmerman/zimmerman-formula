# CFG342 FROZEN CRITERIA: could foreground interlopers fake the UFD excess?

**Lane:** orchestrator. The owner said "run the contamination check".

**Model (favourable to the escape).** A fraction c of a UFD's velocity sample are Milky Way foreground stars that passed the membership cuts. Interlopers passing a velocity window ±W about the systemic velocity are spread uniformly across that window, so their dispersion is W/√3. The members carry the law's σ_law. A second-moment mix gives

σ_obs² = (1 − c) σ_law² + c W²/3,

so

c_need = (σ_obs² − σ_law²) / (W²/3 − σ_law²).

This is the most favourable estimator for the escape: real ML fits with outlier clipping suppress interlopers.

**Window.** W = max(3 σ_obs, 10 km/s) is primary, the typical membership window. W = 5 σ_obs is also reported (wider, which makes contamination more effective).

**Sample.** The same 31 resolved UFDs as AUDIT_UFD / CFG341, on both footings.

## Decision (primary window, both footings)
Compare against typical post-Gaia residual contamination rates of a few percent (literature, PROVISIONAL).
- **EXPLAINS:** median c_need ≤ 5%.
- **PLAUSIBLE:** 5% < median c_need ≤ 15%.
- **NOT:** median c_need > 15%.

Also reported: the fraction of UFDs with c_need ≤ 5%.

## Controls
- **C1:** if σ_obs = σ_law, then c_need = 0.
- **C2:** a synthetic mix with c = 0.10 and W = 30 km/s is recovered exactly by the formula.
- **MUTATE** (CFG342_MUTATE=1): σ_obs is shuffled; the c_need distribution must change.
