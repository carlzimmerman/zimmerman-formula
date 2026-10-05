# CFG343 FROZEN CRITERIA: is the UFD cold mass set by the atomic-cooling collapse threshold?

**Lane:** orchestrator. The owner said "you missed something… we must resolve this".

**The missed assumption.** CFG317's leaky-box R measures only gas that was processed into stars and then lost. It is blind to gas that NEVER accreted. A galaxy that formed stars before reionisation must have collapsed into a structure whose virial temperature reached the atomic-hydrogen cooling threshold, T_vir ≥ 10⁴ K. That fixes a minimum collapse mass M_cool(z_f) from atomic physics plus the shared GR + Λ background, with no tuning. Under B's own rule (reading S, CFG35 / CFG313 / CFG317), the cold share is the collapse mass's cosmic share.

**Formula.** Barkana & Loeb 2001, eq. 26:

M_cool = 1.0e8 h⁻¹ M☉ · (μ/0.6)^(−3/2) · (Ω_m/Ω_m^z · Δ_c/18π²)^(−1/2) · (T_vir / 1.98e4 K)^(3/2) · ((1+z)/10)^(−3/2)

- Inputs: T_vir = 1e4 K; μ = 1.22 (neutral); h = 0.674; Ω_m = 0.315.
- At these redshifts Ω_m^z ≈ 1 and Δ_c ≈ 18π².
- z_f = 8 is primary; z_f = 6 and 10 are the bracket (CFG336's UFD class).

**Per UFD.** R_cool = max(1, f_b · M_cool / M_b), with f_b = 0.157126 and M_b = 2 L_V (AUDIT_UFD). This is a LOWER bound: the collapse could have been larger.

## Scoring (pre-registered approximation)
- Take the median log R_cool over CFG317's 40 MW UFDs.
- Read CFG317's committed UFD statistic s(log R) and z(log R) (numbers.NEED[profile|footing|P1], uniform-R grid) at that median, for both profiles and both footings.
- Disclosed limitation: this approximates per-object R by the population median.

## Decision
- **RESOLVES:** |z| < 2 on both footings and both profiles at the primary z_f = 8.
- **PARTIAL:** |z| < 2 only within the z_f bracket, or only for one profile.
- **NOT:** otherwise. Also report the factor short, R_need / R_cool.

## Controls
- **C1:** the formula reproduces Barkana & Loeb's quoted ~1e8 h⁻¹ M☉ normalisation at T_vir = 1.98e4 K, μ = 0.6, z = 9.
- **C2:** classical dwarfs have R_cool = 1 (their baryons already exceed f_b M_cool), so nothing changes for them.
- **MUTATE** (CFG343_MUTATE=1): T_vir = 1e3 K (H₂ minihalos instead of atomic cooling). The result must change.
