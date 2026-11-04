# CC10 physical memory kernel and changing-distribution stage

The memory work now goes beyond a prescribed multiplier table. Preferred API
is `response_api_v4.py`: it supplies an occupation-independent physical cell-pair
kernel, parent density/coherence, channel exits, massive-energy moments and
the actual signed scalar Floquet work. Prior APIs and source files remain
immutable evidence inputs.

The new stage `run_stage001` evolves every charged-scalar momentum cell using
that kernel. On the recorded slow orbit it reaches **Ycharged=1.72351e-13**,
compared with **6.27471e-13** from an independently evolved stationary kernel.
It retains the actual massive neutral cascade with terminal momentum cohorts.
The original full cosmological target remains open: this stage starts from
the prior conditional NWA endpoint, retains its slow orbit, uses dilute vacuum
daughters and omits matched nonlocal/dispersive charged selfenergies and new
2-to-2 reactions.

The physical API conventions are:

- `band_kernel(xmid,amplitude,omega,Tc,edges,radial=2,angular=12,channels=...)`
  returns Kij=<sigma v>, full positive rho_ij, exact boost-weighted exit rho_ij,
  positive coarse-grained source, channel_K, neutral/charged energy moments,
  signed scalar power and separate residual moments. Use radial>=2 for the
  default volume quadrature.
- `contract_band(kernel,Tc,edges,f_number)` applies arbitrary current fS with
  n_i±=12 Tc³ Wi fS_i/(2pi²), returning dfS/dtau, pair event rate, two-carrier
  loss, parent density/source and energy/work moments. No old-shape multiplier
  is needed. `parent_decay_step` retains coherent delayed neutral evolution.
- The complete 80-orbit Kij and stationary matrices are in
  `run_stage001/kernels.json`; actual evolving-shape channel sources versus N
  are in `run_stage001/result.json`.

Physical K contractions agree with the separately implemented occupied-v2
continuum response below 7.4e-14. Daughter-channel sums agree below 1.5e-15,
and carrier loss is exactly twice pair production in the three checked
packets. The stage's finer quadrature changes its endpoint-weighted rates by
at most .289%; three refined points were tested, not all possible shapes.

Stationary BW is still quantitatively wrong in parts of the late window:
fine endpoint dynamic/static ratios are .9148 and 7.0381, and a dense prescribed
table ranges .09093–9.31691. Actual continuum dephasing, parent occupation and
four-state ODE controls are recorded in the prior v2 checkpoint.

The omitted **explicit local charged absorptive width** is now bounded and
computed, rather than assessed only through its static correction. A passive
Floquet-space energy estimate uses
epsilon=sup||Gammaout^-1/2 GammaC(t) Gammaout^-1/2||. Its three rate intervals
are [.8172,1.2013], [.9214,1.0818] and [.9661,1.03445]; the actual full-matrix
continuum FFT corrections are .9595, .9918 and .9873. The sharp final bound
cannot erase the factor-seven enhancement. This bounds that local positive
absorptive operator; it does not bound an unspecified nonlocal/dispersive
charged kernel. See `run_v3checks001` and `run_bounds001`.

The actual neutral transfer has a tested maximum terminal-delay times H of
6.51e-7, allowing cosmological elimination while retaining many orbital
periods of delay. Its terminal map is positive and conserves the full parent
energy. Redshifted terminal cohorts retain massive energy, pressure and force.
The new S3_0 and S8_0 yields are 1.76223e-12 and 2.41092e-13. Their retained
rest energy/s is **3.68907e-8 GeV, 83.84 times the DM reference**. This is a
new conditional neutral pair-loss/relic obligation, not a global exclusion:
the stage omits their annihilation and occupied inverse reactions. Their
final force shifts the well center by 8.86e-14, only 2.65e-8 of the saved
orbit amplitude. Primary parent energy is at most 4.45e-10 of the recorded
field oscillation energy.

The signed action input is now derived and independently checked. A sideband
with positive neutral rate r_n transfers scalar power n omega r_n. Thus
Pscalar=sum n omega r_n, and sum |n omega| r_n is its absolute bound. The ODE
phase current gives the same work to 8.3e-7–1.35e-4 relative in three tested
pair modes (`run_work002`). A finite-width on-shell parent-energy residual
sum(delta0+n omega)r_n is exposed separately for common-ledger matching.
The 6.74e-6 quantity in the first stage is a positive phase-energy assignment
diagnostic; **it is not a rigorous signed action-covariance bound**. Use the
actual sideband work and valid absolute bound from v4/work-stage instead.

`run_workstage002` applies the signed work and separate finite-width/cell
projection energy residuals to the newly evolving fS stage. It computes a
controlled first action response on the recorded orbit: the actual relative
action correction is 5.95214e-8 and its valid absolute sideband bound is
1.00672e-7. Separate integrated finite-width parent-energy and cell projection
residual bounds are 3.64351e-8 and 1.77738e-9 on the same action scale.
The maximum instantaneous absolute dlogJ/dN bound is 4.09678e-7. These support
retaining the late recorded orbit at this controlled stage, while supplying
the actual moments for root's common field/cascade integration. They do not
silently declare that common quantum energy ledger complete.

First remaining bridge: common coupled force/action evolution with the new
kernel and actual occupied statistical/cascade state, together with dynamic
charged/dispersive matching and finite-width daughter energy matching. The
massive neutral population adds an explicit 2-to-2/relic obligation. No new
initial thermal history or fully matched cold photino abundance follows from
this stage alone.

`DERIVATION_V4.md` gives formulas and proof scopes. `PROVENANCE_V4.json` pins
all new contracts, inputs, source bytes, output hashes and fresh manifest
validations. There are seven completed and three valid failed records. The
new stages took 110.55s (464.76MB measured peak RSS) and 72.47s (216.69MB),
each with one numerical thread and the required wall/CPU caps. Original
failed sources are retained unchanged; corrections use new filenames and
fresh run directories. No Git mutation or prior-scope edit was made by this
work package.
