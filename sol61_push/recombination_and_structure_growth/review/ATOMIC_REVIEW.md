# Coordinator audit of the hydrogen-rate laboratory

Primary verdict: **correct only with the stated effective hydrogen-model
restrictions**. This is coordinator self-review, not a fresh independent
recombination-code endorsement. Root inspected the raw script, report and
HyRec's cached section II A rather than relying on the count of checks.
Reviewed revisions are pinned in the fourth-lane reconciliation record.

## Reconstructed critical implications

1. Substitution of n_H=eta_H[2zeta(3)/pi^2](kT/hbar c)^3 into Saha gives
   A=sqrt(pi)/[2^(5/2)zeta(3)] and the displayed entropy equation.
   x=.5 implies x^2/(1-x)=.5, not one. Differentiation gives
   (theta-3/2)dlnT=dlneta_H-(3/2)dlnm_e+theta dlnchi. The signs and
   leading Coulomb mass/alpha translation are correct at fixed eta_H.
2. Expanding 1/(exp(t)-1) as sum exp(-j t) and integrating t^2 gives the
   exact photon-tail series, including its polynomial. The inventory criterion
   and Saha criterion are different statements; no one-photon-per-ion premise
   is justified. The report correctly removes that earlier shortcut.
3. HyRec equations (1)-(11) use a shell photoionization coefficient beta_B and
   n=2 sublevel statistical weights. Multiplying its C numerator/denominator
   by four gives beta_rec=4beta_B and R_escape=3R_Lya. These yield the
   implemented effective equation; source n=2 energies and positive binding
   energies require the stated sign translation. The steady-state n=2
   reduction is part of the approximate model, not a general multilevel proof.
4. At fixed temperature/state, beta_rec scales with alpha_B and R_escape
   scales with H. Direct differentiation of
   alpha_B(Lambda+R)/[H(Lambda+R+beta)] gives alpha sensitivity C and H
   sensitivity -1+R beta/[(Lambda+R)(Lambda+R+beta)]. Thus changing H affects
   line escape as well as elapsed time. Both decay/escape channel controls
   have the correct direction within this system.
5. Common rescaling of H, capture/reverse rates, Lambda and sigma_T preserves
   C, all rate/H ratios, the matter-temperature equation and optical/drag
   integrals. It scales the conformal visibility normalization uniformly
   while leaving its shape and peak redshift invariant. This is a formal
   rate-system degeneracy, not a demonstrated physical transformation of
   fundamental constants or a conserved action.
6. dt/dz=-1/[H(1+z)] explains the positive recombination term in dx/dz.
   Opacity integrates n_e sigma_T c/[H(1+z)]; drag adds 1/R_b. Conformal
   visibility and probability per redshift have different Jacobians. Epoch
   separation cannot be substituted for the FWHM of either measure.

## Limits controlling the verdict

Hydrogen-only helium-electron omission, the approximate neutrino background,
the z=50 optical-depth cutoff without reionization, Case-B fit, excited-state
steady-state reduction, finite grid and solver tolerances remain explicit.
Similar numerical z_star to a Planck derived parameter is not calibration.
F=1.14 does not turn this laboratory into HyRec/CosmoRec. No atomic or
gravitational action selecting the common-rate rescaling was constructed.

The smallest missing implication for this research program is the retained
action's physical H, atomic currents, opacity and energy-deposition sources,
followed by a multilevel solve and the same-action perturbation calculation.
The laboratory's chemistry does not establish the cold potential source,
the microscopic vacuum, abundance selection or 32pi.
