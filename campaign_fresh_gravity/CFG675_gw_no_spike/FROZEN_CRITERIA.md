# CFG675 FROZEN CRITERIA: no cold-energy "spike" around black holes — sealed LISA IMRI dephasing prediction

Date: 2026-10-12. Block CFG670–679 (owner-assigned). Committed ALONE before any CFG675 code or number. κ = ½ FITTED; footings
separate; cold energy mass required; no particle species; not "theory closed"; nothing says the data favour the framework.

## 0. Idea and what is seen
Particle dark matter can form a dense spike around an intermediate-mass black hole (IMBH); a compact object inspiralling through it
loses energy to dynamical friction, which dephases the gravitational waveform measurably for LISA (Eda+2013/2015; Kavanagh+2020).
In the framework, cold energy's density is the law's profile, ρ_c = (1/4πG) ∇·[(ν(g_N/a0) − 1) g_N]: it depends only on a0 and the
enclosed baryons+BH, with no free amplitude. Author's hand estimate (disclosed): with ν_mono around a point mass at g ≫ a0,
(ν−1)g → a0, so ρ_c → a0/(2πG r) (~1e2 M☉/pc³ at 1 pc, universal); M_c(<r) = a0 r²/G. This ν_mono tail is the Solar-System-
excluded behaviour (a constant ~a0 anomaly); the framework's Solar-System-passing kernels (FRIED_CHICKEN rows 4–5, selector S5)
are exponentially silent, so ν_mono is used here only as a **ceiling**.

## 1. Computation
- Systems: m1 = 1e3 M☉ with m2 = 1.4 M☉, and m1 = 1e4 M☉ with m2 = 10 M☉; quasi-circular Newtonian inspiral with GW
  (quadrupole) + dynamical-friction losses, last 5 years before r_ISCO = 6 G m1/c², GW frequency f = Ω/π.
- Dynamical friction: P_DF = 4π G² m2² ρ(r) lnΛ / v, v = √(G m1/r), lnΛ = ln √(m1/m2) (the standard choice in this literature).
- ΔN = N_cycles(vacuum) − N_cycles(with medium), both over the same GW-frequency band (the vacuum 5-year band).
- **Framework ceiling F0:** ρ_c from ν_mono around the point mass (exact formula, both footings).
- **Particle-DM context (no verdict weight):** static Gondolo–Silk spike ρ = ρ_sp (r_sp/r)^{7/3} with the benchmark normalisation
  used by Eda+2015/Kavanagh+2020 for m1 = 1e3 M☉ (ρ_sp, r_sp read from the paper text before use; if not verifiable, labelled
  "recalled") and γ = 3/2, 9/4 variants; no halo feedback (feedback lowers DM dephasing, stated).

## 2. Sealed prediction and kill line
- **PREDICTION:** if ΔN_F0 < 1 on both footings for both systems, the framework predicts a **vacuum-GR IMRI waveform** (no
  environmental dephasing ≥ 1 cycle from cold energy) for any IMBH whose surroundings are not baryon-dense.
- **KILL:** a LISA (or deci-Hz) IMRI whose waveform requires an environmental density profile ≥ 10 × ρ_F0 at r ≤ 1e-3 pc, with the
  baryonic environment (gas, stars) measured or bounded below that, excludes the framework's "cold energy = the law's profile" reading.
- If ΔN_F0 ≥ 1: the framework itself predicts a universal, a0-set dephasing (report it; the Solar-System exclusion of ν_mono then
  decides whether it is physical).
- Seal: `cfg675_predictions.json`, sha256 in `cfg675_PREDICTIONS_HASH.txt`. MUTATE (`CFG675_MUTATE=1`): ρ → 0 must give ΔN = 0
  exactly; ρ × 1e6 must change ΔN by > 1 cycle (exit 1 iff both bite).
