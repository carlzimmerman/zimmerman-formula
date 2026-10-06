# cm15 FROZEN CRITERIA: the cold edge of the cooling window. Does native T_vir < 1e4 K decide which dwarfs need extra mass?
(owner 2026-10-06: "what else can we run", option 1; committed before any script)

**Data and law.**
- Data: LVD dwarfs (MW, M31, field) with a resolved σ (no upper limits). The law's σ is computed as in CFG341 and CFG335: ν_mono, r = 4/3 r_h, M_b = 2 L_V + 1.33 M_HI.
- Offset Δ = log10(σ_obs/σ_law).
- Native T = μ m_p V²/2k with V = (G M_b a₀)^{1/4} and μ = 0.6.
- Bins: COLD is T < 1e4 K, MID is T ≥ 1e4 K.
- Classes: classical is M_V ≤ −7.7, UFD is M_V > −7.7.

**Hypothesis (cm14).** Native T decides: COLD dwarfs need extra mass whatever their class.

**Scored (both footings, never pooled; 4000-draw bootstrap errors).**
- (a) D1 = median Δ(COLD) − median Δ(MID).
- (b) The median Δ of COLD classicals, and the median Δ of COLD UFDs.

**Verdict.**
- SUPPORTED: D1 > 0 at ≥ 2σ AND COLD classicals have median Δ > 0 at ≥ 2σ, on both footings.
- CONTRADICTED: COLD UFDs have Δ > 0 at ≥ 2σ, while COLD classicals have |Δ| < 2σ AND sit below the UFDs by ≥ 2σ, on both footings. The split would then follow class or formation history, not native T.
- INCONCLUSIVE: anything else.

**MUTATE.** σ_obs is shuffled across systems. The COLD-classical median must move by > 0.05 dex. MUTATE writes separate outputs.

**Scope.** A pattern test, with no mechanism. The cold fluid is still required. κ = ½ is fitted.
