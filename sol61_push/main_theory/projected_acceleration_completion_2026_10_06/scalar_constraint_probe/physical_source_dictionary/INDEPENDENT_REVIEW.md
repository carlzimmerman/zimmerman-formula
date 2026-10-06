# Independent physical-source audit

Verdict: accepted as written for the stated coincident on-shell de-Sitter, finite-k linear branch. No blocking mathematical correction found. This audit reconstructs the varied interaction source and Bardeen curvature; a zero scalar restoring term alone would not establish the result.

## Pinned mathematical inputs

- REPORT.md: `1e00e37969773c17795ae8ca4035b9d4d8fbe3829118425689d21341ff83111e`
- checks.py: `2185f183a5e07f0ac95e5dd1dd841121e991b7ef812ba785ef726eff32749e6e`
- contract.json: `5dead6dabf8440befd0a2665701aecc16e39887d84d913b3c6b9a1039f354b9b`
- SOURCES.md: `668a7692e19aec208ef0dfd90aa56da00e69f6b918d1d80ce391f7d254aaadb3`

Only this review was written; author inputs and outputs were not changed. REPORT is excluded from execution artifacts. The parent scalar proof and same-action homogeneous reduction are separate dependencies, not substitutions from the older indefinite-invariant action.

## Raw reconstruction

With each Einstein coefficient M=2K, the constant interaction is −4KΛv. Covariant variation of the geometric-mean volume gives T_g=−MΛ(v/V_g)g, while v/V_g=1−D/2 at first order, D=ν+3z+e. Subtracting the matched individual vacuum gives density −MΛD/2 and pressure +MΛD/2. The quadratic positive projected interaction is K a(∂ν)^2. Its g-lapse Euler derivative is −2KaΔν; because δS/δN=−a³ρ, its density is MΔν/a²=−MPν. The hatted lapse derivative reverses the sign. At this order there is no shift derivative, spatial stress from the gradient term, or anisotropic stress. Thus the volume response must be retained before imposing D=0, and each-sector density must not be replaced by half its value. The relative density is twice the visible density.

The constrained shear and lapse equations give B_rel=β+edot/P=−(z+ν)/H and zdot=Hν. Hence Φ_rel=ν and Ψ_rel=−νdot/H; the reduced evolution νdot=−Hν makes them equal. The unsourced mean Einstein scalar vanishes under the specified empty-de-Sitter boundary conditions, so visible Φ=Ψ=ν/2. This construction uses the common coordinate freedom only; it does not discard the relative shear by a second unavailable gauge choice.

Independent fixed-M geometric equations then give Y=Φdot+HΨ=0, δρ=−2M(PΦ+3HY)=−MPν, and δR=−Pν=(δρ−3δp)/M. The action and curvature sources agree. Before imposing the equations the energy residual is −MΛDdot/2−MP(νdot+Hν), and the spatial residual is MΛ∂D/2. Their vanishing is an on-shell statement; diagonal covariance alone does not grant two separate off-shell interaction conservation identities.

Finally Π=2Ka³P zdot/H² is constant. Substitution gives exactly δρ_g=−HΠ/a³ and W_g=HΠ/(4Kk²a). The constant z mode has Π=0 and vanishing linear metric curvature, while the decaying mode supplies a pressureless signed integration source. These are linear amplitudes, distinct from the nonnegative quadratic coordinate Hamiltonian H²Π²/(4Kk²a). Its scaling alone does not determine second-order physical backreaction.

For the same-action homogeneous branch, r+nζ=2nζ∞ makes v/V_g constant even when the homogeneous canonical momentum is nonzero. Its full interaction stress is consequently vacuumlike, not dustlike. Finite-k density, k=0 abundance, and nonlinear source completion cannot be pooled.

## Evidence and limitations

Independently invoked validate_manifest.py with the repository root for main_a, control_frozen_a, control_volume_a and control_density_a: all four return exit zero and valid evidence records. Raw recorded results are main 32/32, frozen-curvature 29/32, erased-volume 31/32 and half-density 31/32; the failures match the declared mutations. The development 29-check preflight is historical, not the current authoritative evidence. The symbolic script corroborates identities; the action derivation above supplies their interpretation.

A periodic finite-k seed has zero mean and both density signs. This does not exclude noncompact boundary flux, but neither boundary admission nor a positive particle population has been established. The background has zero additional homogeneous density. Primordial preparation, transfer to an admitted positive abundance, nonlinear source matching, and health beyond this branch remain open. The result supplies a genuine operational pressureless source clue, not a microscopic cold-sector identity or a 32π selector.
