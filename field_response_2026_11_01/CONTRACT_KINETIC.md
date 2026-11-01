# FR01 follow-up: canonical kinetic shear, frozen before execution

The six tested reduced-fluid equilibria have negative radial energy directions
in radial_run_003. That result is scoped to an isotropic closure. The actual
canonical kinetic parent preserves its occupied phase-space level and does
not re-isotropize after an arbitrary radial displacement.

This necessary interpretation check uses the same six equilibria and the same
fixed coefficients, with no new physical parameter. A radial cotangent lift
x=q+t xi(q), p=J^-T p0 preserves phase-space volume and angular momentum. With
A=xi' and D=xi/r, its relative kinetic factor is
[(1+tA)^-2+2(1+tD)^-2]/3. The isotropic density closure instead uses
[(1+tA)(1+tD)^2]^-2/3. Their Hessian difference is

    delta Q = (8/9) integral E_rel (xi'-xi/r)^2 dV
            = (4/3) integral n psi (xi'-xi/r)^2 r^2 dr

in the inherited dimensionless units. Scalar mixed terms, density and gravity
are unchanged. The positive shear cost must be retained before a fluid energy
direction can be called an accessible kinetic energy direction.

## Frozen computation

- Reconstruct six baselines and 12 scalar-minimized displacement basis vectors
  exactly as in radial_run_003, using the refined 3e-7 scalar BVP tolerance.
- Evaluate Q_kin=Q_fluid+delta Q at 256 and 512 Gauss nodes per region; nested
  sizes 4,8,12. Use the same positive finite metric only to normalize Rayleigh
  quotients; these are not solved Vlasov normal-mode frequencies.
- Report the shear cost on each old fluid-negative vector and the new minimum.
- Validate the coefficient by finite differences of the exact two kinetic
  stretch factors at five prescribed pairs (A,D): (0,0),(1,1),(2,-1),(-.4,.8),
  (.25,0), at h=.001,.0005,.00025. Homology must have zero shear correction.
- Negative margin below -1e-5 of summed absolute energy terms, with sign/value
  stable to 3e-4 under doubled quadrature, is an accessible energy saddle in
  the tested kinetic family. It is not by itself a growing-mode theorem.
- Positive finite-basis minima mean no negative direction found here, not
  kinetic stability. Preserve failed controls and do not select a new family
  to manufacture a desired outcome.

Same resources as CONTRACT.md. This amendment is justified by a specific
closure gap, not a rerun of an unchanged passing calculation.
