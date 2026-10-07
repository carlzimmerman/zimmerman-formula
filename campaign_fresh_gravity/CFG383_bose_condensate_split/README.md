# CFG383: the cold fluid as a Bose field. VIABLE by the frozen rule, but it needs a relaxation mechanism the free field lacks

Criteria in FROZEN_CRITERIA.md. Script `cfg383_bec_split.py`: 2/2 checks; MUTATE (σ_cluster = σ_MW) gives clusters condensed at the real m_half, as required.

**Result (ideal Bose gas, k T = m σ²).**
- Setting clusters at R500 to half-unsettled fixes **m ≈ 0.81 eV** (range 0.62–1.04 eV over u = 0.3–0.7 and σ = 800–1200 km/s; 0.96 eV for particle + antiparticle).
- That is inside the record's fluid window (2e-20 to 2.78 eV) and in the range black-hole spins leave open (CFG367).
- With nothing left to fit:
  - groups (σ 400 km/s) are 3% unsettled;
  - the Milky Way is 3e-5;
  - UFDs are 5e-12;
  - clusters are 50%.
- So the frozen verdict is VIABLE: galaxies and dwarfs are fully condensed (settled into the law), and clusters near 1000 km/s straddle T_c.

**What limits it (read before citing).**
1. **Relaxation time (decisive caveat).** A free field relaxes toward these equilibrium fractions only through gravity. The gravitational condensation time (Levkov et al. 2018) at 0.8 eV is 1e55–1e77 Gyr in every system, far longer than the age.
   - So the equilibrium split cannot be reached with the free field of CFG288 road W.
   - A cosmic field that starts as a condensate would be scrambled by violent relaxation in halos and could not re-condense.
   - The mechanism needs a relaxation channel. A self-interaction λ|Φ|⁴ (as in Berezhiani–Khoury superfluid models) is one, at the cost of one constant, and it changes CFG288's free-field gates.
2. **One parameter fitted.** m is set from clusters. Landing inside a 20-decade window is not impressive by itself.
   - The galaxy and UFD predictions (fully condensed) hold for any m below about 1 eV.
   - The informative content is the ordering and the threshold: the condensation edge falls at cluster velocities.
3. **The cluster "half unsettled" target is bias-dominated** (CFG382 target audit, f982f4a34). The bracket u = 0.3–0.7 covers part of that.
4. **Ideal uniform gas.** No trapping potential, no interactions. The local R500 density is a declared ρ ∝ r⁻² estimate.

**Reading.**
- The condensate/normal split is a natural, nearly parameter-free way to get settled galaxies and partly unsettled clusters, if the cold fluid is a ~eV Bose field with a relaxation channel.
- The next step is a lane with an explicit self-interaction. It must re-check CFG288's gates and Bullet-cluster-type limits on self-interaction, and keep the coupling inside the dark sector (G9).
- The cold fluid is still required, and its amount is not derived. κ = ½ is fitted.
