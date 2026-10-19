# CFG842 — can a satellite capture enough of its host's cold energy? (Liouville ceiling)

Criteria: `FROZEN_CRITERIA.md` (127c29c26, before the script). Run: `python3 cfg842.py` (MUTATE `CFG842_MUTATE=1`). Seconds.

## Result — frozen CLASS: **MARGINAL**, solely because of Sagittarius (a rule-design flaw, disclosed); physically: capture fails by 10⁵–10⁸
- The frozen rule compares the Liouville ceiling ρ_max = ρ_c(D)(σ_s/σ_h)³ with the needed extra inner density. Its maximum
  ratio, 0.17, comes from **Sagittarius, which has no excess** (Δ = 0.00; "needed" density 7e3 M_⊙/kpc³, i.e. nothing to
  explain). The rule did not exempt zero-excess objects; that is a flaw in how the criteria were written, not a capture channel.
- **For the 11 satellites with a real excess, the ceiling is 1.5e-8 to 1.8e-5 of what is needed** (both MW masses, best of
  present distance and pericentre): Draco 5e-7, Ursa Minor 1e-6, CVn II 9e-8, Fornax 2e-5. The host's cold energy is too
  dilute (10⁴–10⁶ M_⊙/kpc³ at 20–260 kpc) and far too hot (σ_s/σ_h = 0.02–0.10) to be packed into a satellite core.
- **Reading:** capture of the host's cold energy cannot supply the satellite excess. With CFG822 (expelled gas: too far out),
  CFG823 (own supply: tight / fails), the framework's external field (wrong sign) and CFG838/839 (tides: no signal), every
  framework supply channel examined fails for the satellite dwarfs. Remaining: kinematic systematics or non-equilibrium in
  the dwarfs, or a genuine failure of the framework for satellites.

## Controls
- K1 PASS (profile integral 1.000000). MUTATE bites: with no phase-space dilution the ratio rises to 3.3e2.

κ = ½ fitted; cold energy mass required; not theory closed.
