# cm14 FROZEN CRITERIA: the "cooling window" pattern. Does the cold fluid sit only where a host's gas cannot cool?
(owner 2026-10-06: "do both", option 1; committed before any script exists)

**Hypothesis (from the record, not derived).**
- Hosts whose gas cannot cool keep the cold fluid at the HIGH level. That means T_vir below 1e4 K (no atomic cooling: ultra-faints, CFG344), or T_vir above the cooling step (groups and clusters, cm08/cm12).
- Hosts in between, where the gas cools, are at the LOW level: classical dSphs, spirals, the Milky Way, non-central early types.
- T_vir is framework-native: V = (G M_b a₀)^{1/4} and T = μ m_p V²/2k with μ = 0.6.

**Decisive test (scored): within discs, on SPARC.** All 175 galaxies with Q ≤ 2. Same morphology, so only T_vir changes.
- M_b(<R_last) = V_bar² R_last / G, with Υ_disk 0.5 and Υ_bul 0.7 (the cm01 convention).
- Outer residual Δ = median over the last 3 points of log10(g_obs / (g_bar ν_mono(g_bar/a₀))).
- HOT: M_b > 10^11.36 Msun, the lower edge of cm12's R1 step range (generous to the hypothesis). Also reported with the upper edge, 10^11.62.
- MID: everything else (T between 1e4 K and the step). No SPARC galaxy is below 1e4 K.
- D = median Δ(HOT) − median Δ(MID). The 1σ error is from a 4000-draw bootstrap over galaxies.

**Verdict (both footings, never pooled).**
- SUPPORTED: D > 0 at ≥ 2σ on both footings.
- CONTRADICTED: the 2σ upper bound of D is below +0.05 dex on both footings. The data would then exclude even a modest jump at the step. If HOT discs kept 0.6 of the share instead of 0.13, that would be about 2.5 M_b of extra cold mass.
- INCONCLUSIVE: anything else, including N_HOT < 5.

**Reported, not scored.** The population table from the record, with each population's native T_vir:
- UFDs need extra (+0.325 dex, 3.8σ);
- classical dSphs pass B;
- spirals f ≤ 0.105;
- Milky Way 0.14;
- massive HI discs pass (−0.028 ± 0.066);
- super spirals +0.164 dex (2.34σ);
- non-central ETGs 0.13;
- groups 0.60, group centrals 0.64, X-COP 0.576.

**MUTATE (injection).** Add +0.10 dex to Δ for HOT galaxies. The verdict must become SUPPORTED. MUTATE writes separate outputs.

**Scope.** A pattern test only, with no mechanism. The cold fluid is still required. κ = ½ is fitted.
