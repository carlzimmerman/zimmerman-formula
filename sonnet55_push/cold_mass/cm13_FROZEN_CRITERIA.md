# cm13 FROZEN CRITERIA: can feedback, coupled only through gravity, unbind 87% of the cold share below the step but not above?
(owner 2026-10-06: "yeah run b"; committed before any script exists)

**Question.** cm08–cm10 found that galaxy-scale hosts keep about 0.13 of their cosmic cold share and groups keep about 0.6. Does the energy released by stars and black holes suffice to remove 0.87 of the cold fluid from galaxies, but not from groups?

The cold fluid feels only gravity, so feedback can reach it only through potential fluctuations (Pontzen & Governato 2012). That keeps G9 safe. I treat the energy budget only; this is an energetic necessary condition, not a mechanism.

**Host (framework-native).**
- Baryonic mass M_b on a grid from 1e9 to 1e14 Msun. V = (G M_b a₀)^{1/4}. Both footings.
- Cold share M_c = (Ω_c/Ω_b) M_b = 5.36 M_b. Mass to remove: 0.87 M_c.

**Binding energy per unit mass at radius R.**
- e_MOND = V² [ln(r_e/R) + 1]. This is the logarithmic deep-MOND potential cut off by the external field g_e, with r_e = r_M · a₀/g_e and r_M = √(G M_b/a₀).
- B's T5 bookkeeping (dark = max) is applied to the potential: e = max(e_MOND, G (1 + 5.36) M_b / R).
- E_bind = 0.87 M_c · e.
- R ∈ {r_M, 10 r_M}. g_e ∈ {0.01, 0.05} a₀.

**Feedback energy.**
- Stellar mass M* = 0.7 M_b.
- SN: E_SN = 1e51 erg × M*/(100 Msun).
- AGN: E_AGN = 0.1 × 0.05 × M_BH c², with M_BH = 3.09e8 (σ/200 km/s)^4.38 Msun (Kormendy & Ho 2013) and σ = V/√2.
- Feedback sets: SN alone, and SN + AGN.

**Coupling to the cold fluid.** ε_grav ∈ {0.01, 0.1, 1}. ε_grav = 1 is the absolute energy ceiling. ε_grav = 0.1 is the frozen "physically generous" value.

**Critical mass.** M_crit is where ε (E_fb) = E_bind. Hosts below M_crit can be emptied energetically, and hosts above it cannot.

**Cells.** 2 footings × 2 R × 2 g_e × 2 feedback sets = 16 cells per ε.

**Bracket.** [6e10, 2.2e12] Msun baryons, as in cm12.

**Verdict, at ε = 0.1.**
- ALLOWED-AND-PLACED: M_crit falls inside the bracket in ≥ 12 of 16 cells.
- PARTIAL: M_crit falls inside the bracket in 1 to 11 of 16 cells.
- NEEDS-CEILING: M_crit falls inside the bracket in no ε = 0.1 cell, but in at least one ε = 1 cell.
- FORBIDDEN: M_crit < 6e10 in every cell, even at ε = 1. Feedback could not empty even the Milky Way.

**Also reported.**
- ε_need, the coupling needed to empty the Milky Way (M_b = 6e10).
- Whether E_fb/E_bind falls with mass, which a step requires.
- Whether AGN energy (rising steeply with σ) spoils the step.

**MUTATE.** The cold share is set to 0.536 M_b (×0.1). M_crit must move up by > 0.5 dex in the canonical, R = r_M, g_e = 0.01, SN cell. MUTATE writes separate outputs.

**Scope.** No mechanism is claimed, and the universality of 0.13 is not explained. The cold fluid is still required. κ = ½ is fitted.
