# CFG368 FROZEN CRITERIA: the open door. Does DESI's evolving dark energy prefer an energy flow between the cold fluid and the vacuum, and which way?
(owner 2026-10-06: "okay do the open door"; committed before any script)

**Framing (owner's correction, 10-06).** a₀(z) = κ c √(G ρ_vac(z)) tracks the vacuum (dark-energy) density.
- A flow is NOT capped by "flat a₀". It moves a₀ along with ρ_vac. CFG360-DE's flat-a₀ bound (0.023 H₀) assumed w = −1 and is not used here.

**Models.** True vacuum with w = −1; the cold fluid is dust. Q is the energy rate INTO the vacuum FROM the cold fluid; Q > 0 means the cold fluid decays into dark energy.
- **F1:** Q = Γ H₀ ρ_vac (tied to the dark-energy density).
- **F2:** Q = Γ H₀ ρ_c.
- **F3:** Q = ξ H ρ_vac (tied to the expansion rate, i.e. to the critical density via H²).
- **F4:** Q = ξ H ρ_c.
- Each parameter on a 41-point grid over [−0.5, 0.5], both signs.
- ω_c = 0.1200 is fixed early (comoving at a = 1e-4, what the CMB sees). ρ_vac is shot so that the universe is flat today.
- Baryons, radiation and h = 0.674 as in CFG360.

**Scoring.**
- CFG360's DECLARED, PROVISIONAL CPL projection: a w0wa fit to ln E(z) over 0 ≤ z ≤ 2.5 at the observer's Ω_m.
- χ² against the four DESI DR2 chains: CMB-only, +Pantheon+, +Union3, +DESY5. Gaussian (w0, wa) posteriors, Ω_m shift ignored, as in CFG360.
- Best fit per form; Δχ² relative to ΛCDM (zero flow).

**Verdict per form.**
- DESI-PREFERRED: the best fit improves on ΛCDM by Δχ² ≥ 4 on all three SN chains. The direction is reported as cold→vacuum or vacuum→cold.
- NOT PREFERRED: anything else.

**Lane verdict.**
- OPEN DOOR CONFIRMED: at least one form is DESI-PREFERRED. The direction is reported.
- OPEN DOOR NOT SUPPORTED: no form is DESI-PREFERRED.

**Also reported.**
- For each best fit:
  - the implied a₀(z)/a₀(0) = √(ρ_vac(z)/ρ_vac(0)) at z = 1, 2 and 2.5, compared with the record's M-DEC curve (≈ 0.87 at z = 2);
  - the fractional change of the comoving cold density between a = 1e-4 and today;
  - (w0, wa)_eff;
  - whether ρ_vac or the observer's effective ρ_DE goes negative anywhere.
- Whether the dark-energy-tied forms (F1, F3) or the cold-tied forms (F2, F4) fit better, i.e. the owner's question of what the flow is tied to.

**Controls.**
- K1: zero flow returns (w0, wa) = (−1, 0) to 1e-6 and ω_c unchanged.
- **MUTATE** (CFG368_MUTATE=1): Q := 0 for every grid point. Every Δχ² must be 0 and the verdict NOT SUPPORTED. MUTATE writes separate outputs.

**Scope.**
- A background-expansion test only. Perturbations, growth and the CMB beyond ω_c are not run.
- No new particle. The cold fluid is still required; the flow does not set its amount. κ = ½ is fitted.
