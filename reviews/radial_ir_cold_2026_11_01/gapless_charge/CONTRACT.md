# TP04 residual gauge spectrum and anomalous charge: bounded contract

Frozen before the first scientific execution, 1 November 2026. Parent contract
and base revision are `../CONTRACT.md` and
`27a0d27db1c343e1752698da36aa300398214689`; dirty imported inputs are hashed by
the v2 runner. Only this directory is written.

Compute the complete one-loop chirality-flipping self-energy of the twelve
tree-massless unbroken gauginos at zero external momentum. Include scalar/Weyl
and massive-vector/Weyl loops, retaining exact tree SUSY splittings. Source:
Martin, hep-ph/0509115v2, §III Eqs. (3.2), (3.4), (3.6), in supersymmetric
subtraction (`delta_MS=0`). These equations allow massive vectors at one loop.
This is a leading radiative pole mass because the external tree mass is zero;
tree-flat radial and Goldstino modes are kept separate.

Declared points: h=lambda=e, g=sqrt(29/200)e, f=1, e=.01,.03; z=hX/sqrt(c)
equals z0 and 1.21 z0, z0=7.367143721278508, c=fh lambda²/(30h²+lambda²).
Additional scaling point e=.0001 at z0. Controls: known finite-F U(1) ordinary
messenger formula at F/M²=.1,.5; f=0 SU5 limit; external subgroup degeneracy;
Q-independence; R_xi gauge independence between xi=0 and1 with Goldstone mass
shift; homogeneous e^(5/2) and sqrt(f) scaling. Failures are retained.

Then derive piecewise one-loop IR running and anomaly matching, with actual
conditional strong scales. No nonperturbative prefactor, thermal state,
cosmological abundance, physical mu=sqrt(f), exact lifetime, or universal
mass-gap claim is inferred. One-loop thresholds are not complete two-loop
pole masses. Integrating out a particle requires frequencies below its mass;
massless gauge/Goldstino response may remain nonlocal. Weak-coupling analytic
continuation is distinguished from a selected cold state.

Runs use one numerical thread, wall/CPU minute caps, expected RSS below1GB.
macOS affinity/address-space enforcement is unavailable; observed RSS is
recorded. No installs, external-source downloads, Git changes or earlier
checkpoint edits.
