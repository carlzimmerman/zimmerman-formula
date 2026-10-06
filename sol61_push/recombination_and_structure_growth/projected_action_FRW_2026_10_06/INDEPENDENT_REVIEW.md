# Independent projected-action homogeneous matter audit

Verdict: accepted as written on its homogeneous flat, common-timelike-clock, own-metric minimally conserved matter domain. No blocking mathematical correction found. This is actual same-action homogeneous admission, not a substitution from the nonminimal curvature carrier or a perturbation/atomic transfer result.

## Frozen pins

- REPORT.md: `0cff571d65b153894d7b27688feff25d3e1aaef230ebc0236d2bc3c4cf5afd37`
- checks.py: `fc70b6725a55ddafde360367c8a15f4c2217672b1b457e946c6c96eaf605b6cb`
- contract.json: `54824fdec0eea6f9d6adac4835df3355581a2d2f7ee7cfcd7d2be28e172b1d01`

Only this independent review was written in the author's folder; inputs and run outputs were preserved.

## Raw action and Bianchi reconstruction

For homogeneous lapses, r=ln(N/L) has no spatial gradient, so I=0 and δI=0 even under an arbitrary first metric/clock variation. In the exact unitary ADM invariant this follows directly from its quadratic gradient dependence. Thus the first metric variation of the interaction is entirely that of −4KΛ0 sqrt(Vg Vhat). With M=2K it gives T_g=−MΛ0 Q g and T_hat=−MΛ0/Q hatg, Q=sqrt(Lb^n/(Na^n)). In particular the separately varied pressure equals minus the density; imposing equal metrics before variation would lose the reciprocal factors.

Minimal matter conservation and each metric Einstein Bianchi identity require the own-metric divergence of these full vacuum-shaped interaction tensors to vanish on solutions. For Λ0 nonzero this sets Qdot=0. The two rows are compatible reciprocals, not two independent off-shell interaction conservation symmetries. The homogeneous clock Euler row is zero because δI=0 and the volume has no clock dependence; the diagonal Noether identity supplies the same on-shell dependency. This reasoning does not give a pressureless homogeneous component. Λ0=0 is exceptional: Bianchi does not force constant Q there.

## Uniform-n reconstruction

Take visible proper time N=1 and ordinary densities ρr/M=R a^(−n−1), ρd/M=D a^(−n), with n>=3 and nonnegative R,D. The visible Friedmann equation is n(n−1)H_g²/2=Λ0 Q+R a^(−n−1)+D a^(−n). Differentiation using the respective continuity equations yields exactly the stated Hdot_g. For positive Λ0,Q define h²=2Λ0/[Qn(n−1)].

Independently setting X=b^n gives Xdot=nhQ²a^n and L=Q²a^n/X. These imply Q²=Lb^n/a^n and bdot/(Lb)=Xdot/(nXL)=h. Therefore the hatted Einstein equations with no ordinary matter are exactly de Sitter in hatted proper time, including its acceleration row. This reconstructs both metrics with their lapses left distinct, and preserves each matter conservation equation. No relative lapse was fixed before the action variation.

The radiation-only solution a=C sinh[(n+1)h_g t/2]^(2/(n+1)), R=Λ0 Q C^(n+1), and its dust analogue follow from coth²=1+csch². These verify Friedmann and acceleration for arbitrary n>=3. The mixed positive ODE supplies a local smooth history for a>0. For any compact interior interval one may choose X initial data sufficiently large to maintain X>0; continuing backwards globally requires the stated positivity domain, not an unconditional arbitrary-B0 guarantee.

As t approaches the prescribed radiation big-bang boundary, a^n~t^(2n/(n+1)). A positive limiting X gives L with that power; the zero-limit construction gives X~t^((3n+1)/(n+1)) and L~t^(−1). Both retain admitted timelike clocks and finite positive lapses at every interior t>0, but no smooth endpoint metric/clock continuation is established. These are different integration-data branches, not a forced equality of metric proper times.

## Evidence and physical scope

Independently validated main_a, control_varying_a, control_cold_a and control_lapse_a with validate_manifest.py and the repository root; all four return valid evidence with exit zero. Current main is 27/27 and each control 27/28 with its declared false proposition. The earlier positivity-inference preflight issue is separately preserved and is not authoritative evidence. The general-n claim rests on the action and formulas above, not on finite test counts.

In n=3, conserved thermal photons and hydrogen admit constant η when T=Tref/a, but that assumes the chosen photon distribution and physical number currents. It does not derive ionization kinetics, Thomson visibility, perturbation transfer, relative-sector health or a positive extra cold abundance. The interaction remains pure vacuum for this whole homogeneous branch. The previously found finite-k signed dustlike stress is not a k=0 abundance formula. Λ0, Q, R and D are free inputs/integration data; no 32π selector follows. For positive Λ0 this supplies a concrete full-action ordinary radiation/dust/vacuum history on which those subsequent physical questions can be asked.

## Additional independently reconstructed perturbative identity

This identity is a new review observation, not a frozen-run claim. On homogeneous zero-shift g=−N(t)²dt²+a(t)²δ, normalize θ=t+π. To first order u_i=−N∂iπ and u^0=1/N, so P_i^0=−∂iπ. The clock-normal lapse has δ ln Nθ=ν_g−πdot. Hence a_i=P_i^μ∂μ ln Nθ gives

δa_g,i=∂iν_g−∂iπdot−(Ndot/N)∂iπ,

with the corresponding hatted expression. Equivalently one can derive it from u·∇u; scale-factor connection terms cancel. Their difference is δA_i=∂i[δr−rdot π], where δr=ν_g−ν_hat and rdot=d ln(N/L)/dt. The background A vanishes. Therefore the quadratic invariant is h^{ij}∂i(δr−rdot π)∂j(δr−rdot π)/a0². The interaction coefficient at this order is the background measure times M_I(0); it supplies no additional pure-clock time-derivative term before metric constraints are varied.

Under the common infinitesimal time shift T, δr→δr−rdot T and π→π−T, so this combination is invariant. For the reconstructed constant-Q matter history with N=1, rdot=−n(H_g−bdot/b), generally nonzero even though Q is constant. Coincident de-Sitter rdot=0 is thus a special coefficient background; its flat-clock quadratic statement cannot by itself establish scalar health on these matter histories. Full coupled lapse/shift/shear/matter constraint elimination remains required.
