# Units correction to the frozen stage19 derivation

The frozen proof incorrectly labels pressure coefficients as keV/cm³ and uses r/R500. Those metadata claims are withdrawn. The original FGF019 normalization, checked after the author's correction, is x=r/Rt with Rt=1252 kpc for ZW1215, p(x)=C_SZ Rt Pe(Rt x), C_SZ=sigma_T/(m_e c²). Thus saved coefficients p and the target dp/dx are dimensionless. The target's physical electron-pressure derivative is (dp/dx)/(C_SZ Rt²). No equality of Rt with R500 is established by this audit.

The saved response maps dimensionless p to dimensionless y. FGF029 keeps that normalization while changing the endpoint to6. The current baseline, common step, coefficient perturbation radii and target separation all use this inherited normalized coordinate system. They are not physical pressure errors or pressure-gradient tolerances in keV/cm³ units.

Preserve the frozen derivation, code, contract and completed run bytes. The executed code contains no physical-unit conversion, and the contract has no keV/cm³ or R500 label; the exact Fraction arithmetic, inequalities and outputs are unchanged. Its manifest historically pins the mistaken frozen prose, so this correction is part of the final interpretation. No numerical rerun is required. This was a reviewer metadata error found through the author/coordinator's source check, not an independent instrument-unit validation before computation.

Source pins:
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/DERIVATION.md`: `1df5bae016cc214764dbaf26ddbca7ebec3df2af7a052cf6aa182c599cb47e30`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/project.py`: `5ecada23fa8ca823d02425655f33f37288e868d5e51d7172764576643147fb2c`
