# PN28: pressure selection and conservative transport

User authorization: continue attempting the pressure-to-acceleration derivation.
Base checkpoint: `66c45c5082f651dd54e171f98c11acd9cb3d9086`; actual source bytes are pinned in INPUTS.json because concurrent work changes the shared repository.

## Exact target

Derive, from one specified conserving parent and a physically selected state, an inner finite-halo coefficient A>0 in p=A ln(rho/rho_ref), and an independent relation to the gravitating vacuum V=rho_Lambda c^2. Under the separately adopted core identification Sigma=a0/(2piG), the MC27 quarter-density convention gives a0^2=pi xi^2 G A, xi=5.84477267596. The desired kappa=1/2 corresponds to A/V=1/(4pi xi^2). This target value may be compared with a calculation, never inserted as input to claim selection.

A full success requires deriving the stress closure, energy exchange and state selection, preserving a finite physical halo, and testing allowed fixed-vacuum deformations. An exact obstruction or a conserving mechanism that leaves A free is useful partial progress. It is not theory closure, a new empirical fit or a claim of worldwide novelty.

## Portfolio frozen before route results

- DISP: /root/mechanism_closure; dispersion_coupling/. Change the total-current-only interaction hypothesis, derive an explicit positive-energy mediator coupling to relative stream motion, and test real random-energy exchange and residual amplitude freedom. First discriminator: exact energy/moment balance.
- REL: /root/theory_audit; relativistic_mixing/. Complete the previously nonrelativistic phase-level mixture in momentum space. First discriminator: exact pressure-energy normalization and its relativistic limits, without equating phase density with mass density or kinetic with vacuum energy.
- TRANS: /root/empirical_audit; transport/. Test Fourier heat flow against the exact inner pressure and compression requirement. First discriminator: central flux sign. If incompatible, derive necessary cooling/transport power.
- RES: /root; reservoir/. Integrate the reciprocal energy equation for a local comoving reservoir with constant equation-of-state w, then include its pressure in the total response. First discriminator: does conservation select A and is the coupled pressure response positive?

All files are new and confined to this directory. No old scientific claims or active Claude files are edited. Finite checks are bounded and recorded separately from analytic arguments. No manuscript integration, commits, long simulations or fitted coefficient search is part of this checkpoint.
