# Protected-gravity checkpoint PG06

The proposed epsilon=1e-4,b=c=1e8 quartic almost-no-scale model survives
the tested local scalar action. It does not remove the uneaten neutral
fermion: m_zeta~81.18 eV with matter-current amplitude~.99998333. The
leading photino partial lifetime remains about 1.325e20 s. This is a useful
conditional Einstein-frame window, not a complete quantum gravity/current
embedding or a derived dark-energy link.

Base checkpoint: a5617b4742892d38b77382fd67540fba365b2993. Owner writes
only this directory. TP01–TP05 and all previous outputs remain unchanged.
No Git mutation, queue change, installation or production simulation.

Preferred scalar point: [120-digit packet](run_export_002/result.json),
with normalized fields,W0 and every execution constant sufficient to
reconstruct net V=2.52e-47 GeV^4 to 6.32e-46 relative target error.
Full derivation and limits: [DERIVATION.md](DERIVATION.md).

| Quantity | Preferred value |
|---|---:|
| e,mu |.003,1.81706621115e7 GeV|
| X / old X_min |1.02656394539939|
| Phase,radial masses |.07586885724,.44320877744 GeV|
| Two modulus scalar masses |168.7261214 GeV|
| Gravitino |2.435351790 MeV|
| Photino |.9743577944 MeV|
| Leading uneaten neutral fermion |81.18110 eV|
| Leading matter-current partial lifetime |1.32488779e20 s|
| Sigma->phase pairs |Open|
| Raw F_hidden^2/rho_DE |about 1.396e74|
| Required relative W0 precision |about 3.58e-75|

The eight positive scalar eigenvalues cover the four-chiral commuting
singlet block. Neutral heavy fermions in the initial Ward-completed solve
are about 1.40749e6 GeV. All charged/nonflat rigid fields are much heavier,
but a rigid gap is not a transverse quantum Hessian theorem. The Goldstino
rotation/current calculation uses the K-normalized fields and retains the
rigid Ward self-energy required by CW stationarity. A tree-off-shell
matrix is not silently treated as a physical pole.

Runs and evidence:

* run_exact_001: symbolic complex inverse potential, exact rational 2–4-field
  controls,n=3 limit, leading Goldstino null/orthogonal identities.
* run_local_001: exact neutral tree plus full finite rigid CW; all complex
  stationarity/metric/scalar checks; leading Ward current/partial width.
* run_checks_001: independent leading profile and 60/100-digit repeat;
  classical transverse gap; full local anomaly combination;17-point
  profile discriminator for continued opening of the uneaten channel.
* run_finite_001: linear CW heavy-normal sources and unreduced U2diag,
  with 21/29-node convergence and no relaxation double count. Tiny residual
  explicitly tuned. Finite loop kinetic terms remain omitted.
* run_compare_001: independent leading-CW check of the canonical finite row;
  relative differences below .00181, phase closure and light-gravitino
  ordering independently reproduced. This is a consistency check, not a
  full independent finite-canonical reproduction.
* run_export_001: preserved failed strict target-accuracy assertion
  (7.06e-24 relative residual versus 1e-25 contract), not a physical failure.
* run_export_002: refreshed 120-digit constants, final W0 refinement,
  complete serialized packet and successful tiny-V reconstruction.

All seven v2 histories retain exact sources, inputs and output hashes;
six completed and one failed assertion. Individual computation times are
under 7 s; peak RSS under 110 MB; one thread, bounded wall/CPU. Manifest
validation checks current bytes and run status separately. Reproduction
commands are stored in the manifest argv; choose new output directories
for a rerun. [SOURCES.md](SOURCES.md) authenticates load-bearing primary
formulas; [SELF_REVIEW.md](SELF_REVIEW.md) states the audit scope and gaps.

Open continuation: compute a common finite SUGRA 1PI action for full
neutral/transverse two-point functions and the physical transition and
scalar cubic currents at the same loop-stationary background, with finite
Higgs/anomaly threshold matching. The leading 81 eV estimate and dipole
projection do not themselves certify scalar->two-Goldstino widths.
Production has been told this and given the actual finite protected row.
No arbitrary scalar scan or further precision increase closes this 1PI
obligation. The construction is not exhausted; the missing matching is
deferred at this checkpoint, with exact fields and sources now available.

Even a completed 1PI match would leave W0 residual selection, the V3
khronon/P multiplet/operator map and kappa derivation as distinct open
problems. Tuning a net residual is not the obstructed raw-F-energy link.
