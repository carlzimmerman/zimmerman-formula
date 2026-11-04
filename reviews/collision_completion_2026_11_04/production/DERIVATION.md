# CC10 conditional cosmological neutral decay and photino production

The terminal neutral scalars have radiative exits, so their apparent stable
rest density of 83.8424 times today's dark-matter density is an intermediate
storage diagnostic. In the specified fixed-pole, radiation-dominated decay
benchmark that rest energy becomes redshifted radiation, plus a conditional
small and very hot photino population. This does not establish the abundance
of a complete cosmological history or exclude a separate cold source.

Only this `production/` directory was written for this continuation.
`neutral_loop/` was read as a frozen input.

## Defined benchmark and calculation

Parents S8_0 and S3_0 are assumed nonrelativistic well before decay, with the
fixed pole masses and rates at e=.003, mu=2e6 GeV and x=25.4000254000381.
The parent survival probability is exp(-Gamma t). Every conditional mixed
gaugino decay emits one chi with p*=M/2; daughter masses introduce negligible
kinematic corrections here. The particles subsequently free stream without
scattering, cooling, entropy injection or a changing mass.

The background uses the numerical SM equation of state published with
[Saikawa–Shirai, arXiv:1803.01038v2, Appendix A](https://arxiv.org/pdf/1803.01038v2).
Its exact-version [ancillary table](https://arxiv.org/src/1803.01038v2/anc/standardmodel2018.dat)
is retained as `standardmodel2018.dat`; authentication and its SHA256 are in
`SOURCE_RECORD.json`. The table includes the QCD crossover and changes in SM
entropy degrees of freedom. It is not replaced by a constant 106.75.

For conserved SM entropy,

    a(T) = T_gamma0/T [g_s0/g_s(T)]^(1/3),
    H_RD(T) = sqrt(pi^2 g_rho(T)/90) T^2/M_Pl,
    t(T) = integral d ln(a)/H_RD.

The table's low-temperature limits g_s0=3.9309363 and g_rho0=3.3830836 are
used consistently. With T_gamma0=2.3486541805581e-13 GeV and H0=67.4 km/s/Mpc,
they imply Omega_r=9.210815829e-5. Late propagation includes Omega_m=.315
and Omega_Lambda=.6849078918. SM thermodynamic quantities and the cosmic clock
are interpolated with PCHIP in logarithmic coordinates.

For a birth scale factor a_b,

    alpha = p0/m_chi = [M/(2m_chi)] a_b,
    v(a) = alpha/sqrt(alpha^2+a^2),
    lambda_FS = c integral_(a_b)^1 v(a) da/[a^2 H(a)].

The full SM radiation background is used at early times, followed by matter
and Lambda. Exponential averages use u=Gamma t=r^2 and 96 Gauss-Legendre
nodes over 0<=u<=35. This removes the early-RD square-root endpoint cusp.
The omitted probability is below 6.4e-16. Propagation uses 16385 log-a nodes;
halving both quadrature and propagation resolutions changes the mean distances
by at most 2.51e-8 relatively. As an independent implementation comparison,
the CT09 `photino/phase_space.py.free_stream` gives distances within .031%.
Its constant late-LCDM radiation prescription explains this small difference.

## Lifetimes and source shape

The gauge-pair widths are complete leading vacuum calculations. The additional
gaugino widths are soft threshold derivatives whose exact on-shell matching
is unfinished. In particular the triplet soft amplitude changes by 15.3%
between two gauge choices; that uncertainty is not removed by this cosmological
calculation.

| Parent | Exact gauge-only lifetime | Conditional gauge + soft-chi lifetime | Conditional one-chi branch |
|---|---:|---:|---:|
| S8_0 | 7.10557 ms | 4.39263 ms | .381806 |
| S3_0 | 10.9650 microseconds | 9.18242 microseconds | .162570 |

The computed one-loop chi mass is 104.73075 keV. The parent-rest-frame
p*/m_chi ratios are 2.5264e7 and 9.6486e7. The following are number averages
over the full exponential decay distribution for the conditional mixed source:

| Quantity | S8_0 source | S3_0 source |
|---|---:|---:|
| Median SM temperature at decay | 15.5946 MeV | 240.891 MeV |
| Mean free-streaming distance today | 302.731 Mpc | 80.7778 Mpc |
| Mean present speed | 86.4548 km/s | 13.6235 km/s |
| Median redshift at p/m=1 | 3691.59 | 23752.0 |
| Median cosmic age at p/m=1 | 43913 years | 1280.06 years |

These daughters are very hot compared with a 1-kpc coldness target. The
gauge-only rows in the JSON carry hypothetical source-shape distances of
355.417 and 86.6668 Mpc at the longer gauge-only lifetime; their chi branch
is zero and they are not an additional predicted chi population.

## Explicit width sensitivity, not an all-channel rate bound

Two scans use factors (.1,.3,1,3,10,30,100). The first multiplies the total
conditional width while holding the branch fixed. The second multiplies only
the uncertified soft chi partial width, retaining the exact gauge-width floor.

| Width assumption | S8_0 mean distance | S3_0 mean distance |
|---|---:|---:|
| Common total rate x .1 | 633.454 Mpc | 195.171 Mpc |
| Common total rate x 100 | 54.2982 Mpc | 12.2359 Mpc |
| Soft chi partial rate x .1, exact gauge floor | 348.448 Mpc | 86.0094 Mpc |
| Soft chi partial rate x 100, exact gauge floor | 79.4235 Mpc | 25.5888 Mpc |

Every tested source remains much hotter than 1 kpc. This is a bounded
sensitivity calculation, not an upper bound on uncomputed decay channels or
a proof that any alternative production history fails. The common x .1 case
is deliberately a generic timing sensitivity and need not respect the known
gauge-width floor.

As a timing discriminator in this same early-NR benchmark, reducing the mean
distance to 1 kpc would require common rate multipliers about 3.49e12 and
1.06e11. These are not newly derived microscopic rates. The fraction of the
baseline exponential source born early enough individually to travel less
than 1 kpc is 2.21e-13 and 7.24e-12. Changes to production time, mother motion,
interactions or later entropy are outside this calculation.

## Yield and dark-radiation sensitivity

Two distinct finite-stage number normalizations are read, without joining
them into one physical history:

| Normalization | Y(S8_0) | Y(S3_0) |
|---|---:|---:|
| Late `memory/run_stage001` terminal output | 2.410915699e-13 | 1.762229892e-12 |
| Early `integration/run_warm001` checkpoint | 1.385343577e-8 | 7.408332456e-10 |

The warm numbers follow directly from its group comoving counts and
Y=n/s_SM, with xi=.02 and g_s=106.75 at that early checkpoint. Transplanting
them into the fixed pole masses and lifetimes is a sensitivity test; the
actual warm orbit has different masses and later cascade/population evolution.

For parent yield Y_i, mass M_i and conditional chi branch B_i, the gauge
dark-radiation energy per current SM entropy is

    (rho_DR/s)_0 = sum_i Y_i M_i (1-B_i) <a_decay>_i.

The energy-equivalent Delta N_eff is obtained by dividing by
(rho_gamma/s)_0 [7/8 (4/11)^(4/3)], where
(rho_gamma/s)_0=3T_gamma0/(2g_s0). This counts freely redshifting model gauge
radiation. It does not assert equilibration with the SM or a visible portal.
Conditional chi rest density is m_chi sum_i Y_i B_i; it is reported separately
from gauge radiation.

| Normalization and exits | Gauge energy-equivalent Delta N_eff | Conditional chi rest-density fraction of DM |
|---|---:|---:|
| Late stage, exact gauge only | 1.81646e-6 | 0 |
| Late stage, conditional soft chi included | 1.13246e-6 | 9.01007e-8 |
| Warm checkpoint transplanted, exact gauge only | .0527725 | 0 |
| Warm checkpoint transplanted, conditional soft chi | .0257063 | .00128765 |

For common rate factors .1 through 100 the late conditional gauge contribution
ranges from 3.71793e-6 to 1.07049e-7; the warm transplanted value ranges from
.0817707 to .00241793. The undepleted parent energy divided by SM radiation
at median decay stays below .021 for these normalizations, making the chosen
RD background a useful perturbative benchmark. A large hypothetical rescaling
of the source to supply all DM would require a new backreaction check.

The late stable-density number 83.8424 is therefore not a final overclosure
prediction once the established neutral radiative exits are included. The
conditional late hard-chi fraction is tiny, despite its large propagation
length. Neither this tiny warm component nor the larger warm-checkpoint
sensitivity excludes an independent source of the required cold photinos.
The remaining implications include an actual common abundance history,
on-shell gauge-complete mixed-gaugino matching, and any subsequent daughter
interactions or decays.

## Evidence and checks

`run001/manifest.json` is a fresh v2 record, status `completed`, with exact
before/after hashes for the script, EOS table, CT09 reference implementation,
and all four frozen result inputs. Its declared CPU and wall caps are 235 s
and 240 s; one numerical thread was used. The numerical script reports
.131 s and peak RSS 108920832 bytes. No Git mutation, installation or edit
outside `production/` occurred. The installed manifest validator accepts the
record against the current project inputs.

Checks cover exponential probability and mean time, resolution refinement,
the parent/daughter hierarchy used in subtracting the pre-birth light cone,
reproduction of the intermediate stable-density diagnostic, and subdominant
parent energy for the stated two normalizations. The tested width range,
constant-pole/NR assumptions, conditional branches and all non-claims are
declared before execution in `contract001.json`.

Self-review covered the new definitions, equations, units, numerical
transcriptions and conditional wording; no frozen source was changed.
