# CFG743: the collapsed cold medium settles fast in galaxies, too slowly in the outskirts of the most massive systems

**Label: T1 FAIL as frozen**, failing only at M_b = 10¹² M☉, y = 0.1 (r ≈ 110–120 kpc): periods 2.1–2.4 Gyr against the 1.38-Gyr
bar. Every M_b ≤ 10¹¹ M☉ at y = 0.1 and 1, and 10¹² M☉ at y = 1, passes (0.05–1.36 Gyr).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first.
- **Script:** `python3 cfg743.py` → `cfg743.out`, `cfg743_results.json`. `CFG743_MUTATE=1` exits 1: with the cosmic-mean density it
  reproduces CFG699 exactly (60.38 Gyr).
- **Settings:** κ = ½ FITTED; simple μ (CFG695); the cold energy's mass is required; no particle species; not "theory closed".

| M_b [M☉] | y = 1: r, period (can / alt) | y = 0.1: r, period (can / alt) |
|---|---|---|
| 10⁹ | 1.2 kpc, 0.055 / 0.048 Gyr | 3.9 kpc, 0.43 / 0.37 Gyr |
| 10¹⁰ | 3.9 kpc, 0.098 / 0.085 Gyr | 12 kpc, 0.76 / 0.66 Gyr |
| 10¹¹ | 12 kpc, 0.18 / 0.15 Gyr | 39 kpc, 1.36 / 1.18 Gyr |
| 10¹² | 39 kpc, 0.31 / 0.27 Gyr | **122 / 111 kpc, 2.41 / 2.09 Gyr** |

The local cold density is 10³·⁶–10⁶ × the cosmic mean. The period scales as T ∝ M_b^{1/4} at fixed y, and grows outward.

## Reading
1. **The nonlinear identification fixes CFG699's problem for galaxies.** With 4πG P = −g_c, the tether cancels the cold matter's
   self-gravity and leaves the law. Cold matter at its own halo density settles on local dynamical times, so CFG698's candidate
   B with a mechanism is not excluded on settle time for galaxies.
2. **It does not settle everywhere.** The outer halos of the most massive systems (≳10¹¹–10¹² M☉ beyond ~40–100 kpc) get only a
   few periods in a Hubble time. There the cold mass should **not** yet sit on the law's profile.
3. **POST-HOC observation (not tested; no verdict weight).** That unsettled zone matches the record's hardest galaxy failure:
   massive early types at 50–100 kpc (C3, CFG529; the excess persists on Ks masses, CFG669 Z 3.37). The sign depends on the
   pre-settling state:
   - if the cold medium fell in like ordinary cold matter before the tether acted, the unsettled zone holds **more** mass than
     the law. That is C3's sign.
   - starting from zero polarization (CFG696 state (i)), it holds **less**.

   A test needs a framework-native infall initial state and CFG696's relaxation curve, with no fitted settling rate. That is a
   new lane, frozen before any comparison with C3. The same unsettled outer halos would also move the shear one-halo term,
   which is relevant to D2.
4. **Not claimed:** collisionless relaxation to the profile (phase mixing; CFG461/CFG665 remain); the initial state; any C3 or
   D2 improvement.
