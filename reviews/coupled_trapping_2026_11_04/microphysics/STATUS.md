# CT09 microphysics status

The requested microscopic bottleneck was pursued beyond the initial charged
decay check. Leading-tree carrier conversion, actual displaced neutral sinks,
daughter rest energies/forces, full unbroken gauge annihilation normalization,
massless-scalar Coulomb strength, a previously F-closed charged-scalar resonance,
and its coherent four-mode absorptive matrix have been computed.

Completed finite records (all v2, one numerical thread, wall<=240s,
CPU<=235s, measured macOS RSS, no RLIMIT_AS or affinity cap):

- `run_network001`: thirteen x points, full charge-adapted SSS/FFS mass-DAG
  cascade. All checks pass. Vector and loop exits remain omitted.
- `run_endpoint002`: terminal masses, mass slopes, charged/neutral rest-energy
  and NR-force sums, FD inverse-relative-speed coefficient, and massless
  neutral scalar-exchange norm bounds. All checks pass.
- `run_scalar002`: charged-scalar-pair widths and frozen-shape inverse rates
  across x=20--30 plus the pole threshold. All checks pass. Per-basis net-loss
  factors at the fourfold degenerate pole are diagnostic; use the next record
  for coherent pole cross sections.
- `run_pole002`: exact four-mode tree absorptive matrix and coherent production
  Gram at x=25.4000254000381. All checks pass. The physical pair peak is
  15741.99983725 mu^-2; this pole's Cauchy upper value is 30151.28622873 mu^-2.
- `run_controls001`: exact rational gauge factor13/16, pole basis covariance,
  and e=.001,.003,.01 tree scaling. All checks pass.
- `run_medium001`: separate SSS/FFS absorptive matrices. The SSS width is
  positive definite; blocking every FFS decay gives a uniform fixed-pole
  positive-width bound97360.19095551 mu^-2. This covers ordinary Pauli
  suppression, not a general nonequilibrium gain/self-energy theorem.
- `run_tchannel002`: exact vertex completeness5g^2 and spacelike propagator
  norm controls. Direct t/u production of all twelve raw massless gauginos
  satisfies the bare physical-pair bound50g^4/(pi m_C^2), or492.3077 times
  the scalar gauge-boson baseline. Exact rates/momenta and all-partial-wave
  Coulomb resummation remain distinct leaves.

Failed attempts are preserved under their exact original script filenames:
`run_endpoint001` failed on NumPy's read-only diagonal view;
`run_scalar001`, `run_pole001` and `run_tchannel001` failed while serializing numpy.bool_.
Their manifests, stderr and exact source hashes remain. Successor scripts
have `_v2` suffixes rather than overwriting failed execution inputs.

Structural findings: the fermion-to-scalar conversion leaves one carrier;
the x=3 octet cascade removes about7.13% of a charged pair per inverse event
while depositing a massive neutral with negative mass slope; late gauge
annihilation must retain Coulomb1/v growth; massless scalar exchange is only
about1.1% of the maximal gauge attraction at the outer packet; the charged
scalar has a genuine singlet resonance at a radius above the fixed protected
vacuum. The resonance has a finite neutral width and cannot be represented
by an infinite zero-width cross section.

Open routes: coupled neutral daughter occupation/momentum forces; remaining
scalar finite-range channels, exact photino/gaugino-pair rates and momenta
beyond the direct-exchange bound; nonabelian radiative capture; neutral-adjoint loop
radiation; vector exits of heavier broad-network parents; loop pole-mass
retuning and any compatible gravity family. The coordinator owns the
cosmological loss integration and common live README. This package does not
claim a combined production history, final abundance, global annihilation
bound, or weak-regime no-go.

Regenerate any run using the exact argv in its manifest after confirming the
declared input hashes. Validate with the installed computation-audit
`validate_manifest.py MANIFEST --root PROJECT`. `DERIVATION.md` describes the
mathematical domain and limitations; `SOURCE_PINS.json` fixes actual inputs.
