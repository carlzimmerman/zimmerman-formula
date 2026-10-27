# A populated, restoring interface with mobile density

**The depleted transition and boundary restoration now work together in a finite spherical calculation. Exact preservation of the galaxy law through the transition remains unresolved.** The successful branch needs no interface charge. It uses the existing pressure closure, a lower conversion barrier and response stiffness, with both material density and phase varied. The outer phase is never pinned and the target law is never an optimization penalty.

The decisive result is MI-14/15/16: beta=.5, K=15, ell=10kpc, k=tau=0, total dark mass 5.364 Mb, prescribed Plummer baryons Mb=6e10 solar masses and b=3kpc. These are stipulated constitutive parameters, not a microscopic derivation. The action is LD-17/18's corrected common-quadrature gravity/response action. No extra carrier energy is present in this final branch.

## What the tests establish

| Quantity | Final n192 result |
|---|---:|
| Boundary q=.5 |58.9289139kpc|
| Empty material cells between15kpc and boundary |0|
| Smallest cell mass in that interval |.04294 Mb|
| Direct material KKT residual |1.26e-7|
| Maximum reported projected gradient |3.52e-8|
| Distance from saturation cap |.18215|
| Total free-phase mass |1.22586 Mb|
| Exterior mass at r>1.2R (70.715kpc) |.77524 Mb|
| Free fraction of that exterior mass |99.1304%|
| Maximum law error1.5–15kpc |.003012dex / .696%|
| Maximum law error1.5–30kpc |.008212dex /1.909%|
| Maximum law error1.5–50kpc |.050086dex /10.893%|

Law errors include interpolated values at the actual window endpoints. The grid-centre-only50kpc error is.048374dex; **do not use that number to claim a strict<.05dex endpoint-aware pass**. The old fixed exterior diagnostic starts near44kpc and reports28.27% T because it includes the newly populated transition. That historical gate is not passed; the explicitly defined exterior fractions above must not be substituted silently. They show that the outer reservoir beyond the actual boundary remains predominantly free.

MI-14 displaces phase and material together by±1kpc. Both signs return to the same equilibrium on n144 and n192 meshes; the largest final radius difference is1.3e-6kpc. Grid refinement changes the equilibrium radius by .01581kpc. MI-16 extends the outer domain fromabout 664 to1180kpc with the same interior mesh; radius changes 2.2e-9kpc, the radial law profile is unchanged to numerical precision, and the box-edge mass fraction isabout 2e-12. The total energy shiftsabout 9.8e-7Eunit under the changed exterior quadrature, so energies are not asserted identical.

## The actual restoring force

With Eunit=Mb a0 rM=3.2572e51J and radius measured in kpc, the fully relaxed local relation is

    F_R ≈ −[2.16872e-4 Eunit/kpc²] (R−R*),  R*=58.9289139kpc.

The stiffness is about 7.42e8N/m in this specified galaxy model. No oscillation period follows without a boundary inertia law.

This is a coupled result: density and other phase degrees of freedom relax. The fixed-density value is4.03042e-4Eunit/kpc², so freezing material would overestimate stiffness byabout 86%, or equivalently density relaxation reduces it46.2%. The constrained active-tangent Hessian is positive; changing the phase cutoff from 1e-4 to 1e-8 leaves the inferred stiffness unchanged toabout 4e-8 relative.

An independent constrained minimization holds the boundary atR*±.2kpc while releasing the remaining material and phase variables. Forces are+4.45277e-5 and−4.19884e-5Eunit/kpc, respectively: both restore the boundary. The energy curvature is2.16582e-4 and force-slope stiffness2.16290e-4Eunit/kpc², agreeing with the Hessian within .3%. Constraint residuals are near floating precision; force-balance residuals areat most 2.9e-6.

All additional carrier forces and the complete charge-free material/conversion forces are derived in [DERIVATION.md](DERIVATION.md). The cold pure-T equation still gives g²/(a0+g)=gb+gF. Finite mixing and response gradients in the actual transition are why the full target law is approximate there.

## What keeps the matter there

The carrier hypothesis was tested first: local-density-dependent interface capacity attracts material and supplies local density stiffness. It filled the old gap, but could store charge in weak core phase variations, pile up mixed shells or leave a new remote cavity. Requiring a genuinely mixed carrier suppressed part of that failure without delivering a complete solution.

The matched charge-free control retained a populated restoring transition. The useful regime is the existing positive F pressure, reduced mixing barrier and finite response stiffness solved **together with material transport equilibrium**. A large barrier excludes material from the transition; too small a stiffness can reintroduce an empty interval and detached shell. Increasing pressure alone can move the cavity outward. The evidence supports a finite tested parameter window, not a universal parameter choice or a claim that any pressure-supported wall works.

Two independent small conversion seeds, with different initial Plummer density scales, approach the same outer boundary and galaxy-scale profile in MI-16. They retain different central structures below .53kpc; one material residual remains1.43e-4. This supports accessibility of the outer branch under energy relaxation, not unique global convergence or physical formation dynamics. The earlier beta2,K10 branch reaches the same full outer equilibrium from both seeds in MI-13 and independently passes two-grid restoration in MI-10.

## Limits and next unresolved question

This is one prescribed spherical baryon model, not a new real-data fit or an ensemble of galaxies. The force balance, material support and radial restoration have numerical evidence. Exact galaxy-law preservation across the transition, universal microscopic values of K/beta/ell, nonspherical stability, and physical transport/conversion dynamics remain open. Do not restart the old fixed-density, bulk-binding, charge-only or vacuum-wall routes. Continue from this populated charge-free branch and address the measured transition-force correction.

[Result figure](run_artifacts/result.png) · [Machine-readable assessment](run_artifacts/assessment.json) · [Continuation state](HANDOFF.md) · [Evidence validation](validation.json)

Seventeen bounded records are retained: 16 completed and one failed derivative screen before optimization. All 17 manifests validate against current input hashes. Validation certifies provenance, not a physical theory. No previous research inputs were overwritten, and no commit was requested or made by this work.
