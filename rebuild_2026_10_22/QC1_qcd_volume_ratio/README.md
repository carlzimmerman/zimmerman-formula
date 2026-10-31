# QC1_qcd_volume_ratio: is Ω_c/Ω_b the pion-to-proton volume ratio, with a QCD condensate as the cold fluid?

**Verdict: MECHANISM FAILS by the frozen word rule (T5, T6, T7 all fail). X1 is not closed. The number match is CHANCE-LEVEL (T3).**
G11, G12 and G14 do not move. κ = ½ is FITTED. Not "theory closed". No dark matter particle added. Particle values are PROVISIONAL,
from memory, not fetched; no verdict turns on their exact values. Criteria: `FROZEN_CRITERIA.md` (hand checks disclosed there).
Script: `qc1_check.py`; output: `qc1_check.out`, `qc1_results.json`.

| test | result | rule |
|---|---|---|
| T1 arithmetic | (λ_π0/0.8409 fm)³ = **5.2547, not 5.274** (the headline number). Other arithmetic holds, apart from rounding on 2.63e-2. Proposal's Ω_b 0.047466 is not the record's: ω_b/h² gives 0.047453, R 5.2715 | WRONG |
| T2 precision | CODATA 2022 radius: 5.2575 ± 0.012. Record: R = 5.272 ± 0.218 (4.1 %). True gap 0.27 %, −0.07σ. "0.07 %" compares against a number known to 4 % and conditional on flat a0: 6.12 ± 0.32 with SH0ES (−2.7σ), 2.9–8.1 with free dark energy | "0.07 %" FALSE |
| T3 look-elsewhere | Target against null targets: full pool 411 hits (null median 401.5), 25 in ±0.28 % (27). Bare: 8 (7), 2 (0), P 0.085 | CHANCE-LEVEL |
| T4 energy | Proposal's own E_bag = m_p/4 gives **R = 1.31**. MIT bag 0.80. Shell only 4.26. Needs 378 MeV/fm³, which is the proton's own mean density (377), i.e. the identity restated | FAIL |
| T5 baryon number | Thermal nucleons + antinucleons at 155 MeV are 8e6–3e7 × the net. A bag volume cannot see the sign of B | FAIL |
| T6 lifetime | Γ/H = **1.6e19–5.2e19** at zero temperature (X1: 22.6). A gap stops thermal absorption, not decay; lifetime ~1e-24 s. Even the thermal factor is 0.04 at 500 MeV, not 0 | FAIL |
| T7 delocalisation | Spheres fill 4e-9–1.5e-8 of space, with baryons 960–1470 fm apart | FAIL |
| T8 Λ scales | (H₀Λ³)^¼ = 1.1e-2 eV, 4.9 × ρ_Λ^¼ (claimed 2.3e-3). √(f m²/M) is 11.6 ×. "ρ_Λ ~ f²m²/M²" is eV², not eV⁴. a_QCD is 5e-57 of a0 | NO MATCH |
| T9 κ | Σ = c√(Gρ_Λ)/4πG equals a0/2πG at κ = ½, 106.85 M☉/pc² on the record's canonical footing (110.12 on this script's native-background ρ_Λ; the proposal's value is not wrong). Restatement: nothing selects 4π, and the a0 law still needs κ | κ FITTED |
| T10 core, response | (1+x⁴)^(−3/4) also has ρ′(0) = 0 and r⁻³, so "uniquely" is false. The form is X70's, already chosen by hand. "S fixed" has no equation: G12 asks for a calculation | NOT CLOSED |

**Two exits, both shut.** If the cloud stays on its baryon, it is 1e-8 of space, moves with the baryons through the acoustic era, and
is not a separate cold component. If it detaches, it is an excited vacuum state with no named conserved charge, and decays in ~1e-24 s.

**Credit.** (1) A post-inflation birth from the adiabatic plasma does give zero isocurvature. That holds for any such production and
is the proposal's useful point: it is a design requirement for any carrier replacing X1's spectator. (2) The trace-anomaly vacuum,
⟨αG²/π⟩ 0.005–0.02 GeV⁴, gives 183–732 MeV/fm³, bracketing the 378 needed: R 2.6–10. Same order, but this reading has no r_p in it,
so it drops the identity and has a factor-4 spread. It does not repair T5–T7. (3) 5.2575 lies 0.27 % from R: real as arithmetic.

**What this is not.** Not a test of X1, whose carrier and numbers stand as recorded. No grader ran: no new profile or number enters one.
Ω ratios were found FDR-exhausted earlier (framework-pool hits at chance); T3 agrees for a hadronic pool.
