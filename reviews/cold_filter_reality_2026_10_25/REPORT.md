# Smooth-boundary and cluster-data test of the cold filter

**The illustrative filter does not pass the intended cluster-entry gate.** At the unchanged r=1,s=1/4 point and reference H_J=1.8e-18 s^-1, all 35 gas-shell averages from the seven established X-COP clusters exceed the candidate's ideal slow-wave entry threshold. Gas alone is sufficient for this diagnostic. Smoothing the field boundary also shows that the preceding high reflection is not a universal property: it depends strongly on the source-gradient scale and incoming momentum.

This is a conditional failure of passive entry from a cold vacuum reservoir into locally restored regions. It is not a full statistical exclusion of the model, a pointwise statement about every location in each shell, or a proof against earlier in-situ production. No coefficient is retuned to rescue the example. Reservoir abundance, the microscopic coefficient selection and the MOND normalization remain open.

## 1. Replace the density step with a smooth profile

Keep the same Palatini candidate, canonical field q, dimensionless distance z and potential Wbar as a40c03c62e. Hold conserved Einstein rest density fixed, with

    d(z)=10[1-tanh(z/w)],
    V(q,z)=Wbar(q)+d(z)A(q),
    q0''=V_q(q0,z).

The interior density is 20D and the exterior is vacuum. The source is mechanically prescribed and the Einstein metric remains fixed. Solve q0(-L)=0, q0(L)=q_vac with L=max(20,16w), for w=.1,1,10,100. These widths are sensitivities, not galaxy-profile fits. The scalar background is solved by a boundary-value method instead of importing the sharp-wall solution.

Then integrate the linear fluctuation equation through the resulting V_qq, with outgoing interior and incident/reflected exterior waves. Reflection fractions are:

| Source width w | p/m=.001 | p/m=.003 | p/m=.01 |
|---:|---:|---:|---:|
| .1 | .989011 | .967396 | .895421 |
| 1 | .984677 | .954732 | .856914 |
| 10 | .860023 | .636106 | .221360 |
| 100 | .221360 | .010847 | 2.83e-7 |

At these momenta, v is approximately .001c, .003c and .01c, or 300,900 and 3000 km/s. They are sensitivity probes, not a predicted distribution. The physical length corresponding to w still depends on the candidate's normalization; an astronomical source cannot be assigned w merely because that value reflects efficiently.

The sharp boundary's 98.96% reflection was correct for that setup, but does not establish exclusion in a smooth galaxy. For w=100, the .003c and .01c probes transmit almost completely. This is the expected distinction between an energetic barrier and nonadiabatic reflection at an energetically allowed boundary. Here the d=20 interior is accessible at every tested energy.

Maximum BVP residual is below 1e-6. Maximum flux defect |R+T-1| is 5.62e-8. Repeating the slowest wave with tighter ODE tolerance changes reflection by less than 1e-5 in every width case. The BVP itself was not subjected to a second tolerance sequence, so this is bounded numerical evidence at the stated background tolerance, not an exhaustive error certificate. Full gravity, live matter and a stability analysis of these smooth profiles were not computed.

## 2. Calibrate the vacuum energy consistently before comparing data

The previous example treated D=DeltaV as a scale in the action. It is not automatically the observed vacuum density. At the unchanged vacuum,

    f=F/M²=5/6, u=U/D=10/9.

Use an explicit calibration assumption: the bare M is related to Newton G measured in a restored region, where F=M² and the scalar's linear matter coupling vanishes. Let H_J denote the external Jordan-frame vacuum Hubble reference. The vacuum trace gives

    3 M² f H_J² = D u,
    D/c² = [3 H_J²/(8 pi G)] f/u
         = (3/4)[3 H_J²/(8 pi G)].

This uses the Jordan Hubble rate; substituting the Einstein rate without the conformal factor would change the normalization. It remains a candidate calibration assumption, not a full cosmological or local-gravity fit. Three external H_J sensitivities, 1,1.8,3 times 10^-18 s^-1, are reported separately.

In the restored interior A=1, so rho_star=rho_J. For pressureless external matter, the prior constant-Einstein-lapse entry threshold for a zero-momentum vacuum excitation is

    d_barrier = rho_J/D = 31.04.

The restoration threshold itself is only d=8; restoration and blocking entry are not the same condition. Finite incoming momentum raises the entry threshold to

    d_barrier(p)=31.04+23.04(p/m_out)².

For p/m=.01 the change is .002304, negligible relative to the density ratios found below. The gas trace is approximated by rest density, appropriate to nonrelativistic cluster gas for this scale comparison; no temperature-based pressure correction or covariance is fitted.

## 3. Use measured gas supply, not inferred cold density, as the source

Read the released gas cumulative-mass FITS profiles for A1795, A2029, A2142, A2319, A644, A85 and ZW1215. At .1,.2,.3,.5,.7 and 1 R500, interpolate cumulative gas mass logarithmically and compute

    rho_gas,shell = [M_gas(r_out)-M_gas(r_in)]
                   / [(4pi/3)(r_out³-r_in³)].

These are volume averages over five shells per cluster, not local pointwise densities. Hydrostatic mass reconstructions and the previous MOND a0 footings do not enter this gas-density calculation. Stars are omitted. The scalar's inferred cold density is not added as another external source, avoiding double counting.

For a conservative sensitivity to the released marginal widths, also calculate

    Delta M_lower = M_out - sigma_out,lo - M_in - sigma_in,hi.

This is an endpoint box corner at one marginal width, not a confidence bound, posterior probability or correlated-error result. Unknown covariance remains unknown. Interpolated error columns follow the preceding repository convention; raw FITS files are hashed in the manifest.

| H_J (s^-1) | Range of central rho_gas/D | Central averages above 31.04 | One-width box lower averages above 31.04 |
|---:|---:|---:|---:|
| 1.0e-18 | 200.72–5641.93 | 35/35 | 35/35 |
| 1.8e-18 | 61.95–1741.34 | 35/35 | 35/35 |
| 3.0e-18 | 22.30–626.88 | 31/35 | 31/35 |

At the reference scale, the smallest ratio occurs in the .7–1 R500 shell of ZW1215. Even that average is approximately twice the threshold. The largest is A2029 at .1–.2 R500. Averaging cannot establish that every point in a shell is forbidden; clumping, cavities and nonspherical paths require spatial information. Nevertheless, a smooth local approximation using these shell densities does not yield cluster access for this example. Adding an arbitrary transparent channel is not a demonstrated remedy.

## 4. Required entry energies are not cold

Under the same restored-region and constant-Einstein-lapse approximation,

    m_in,E²/m_out,E²=(d-8)/23.04,
    (p/m_out)_required=sqrt[(d-31.04)/23.04],
    v_required/c=sqrt[1-23.04/(d-8)].

Inserting the smallest and largest reference gas-shell averages gives required exterior speeds about .757c and .993c. These follow algebraically from the recorded density ratios. They are not predicted velocities and cannot be supplied by simply relabeling a nonrelativistic reservoir. The actual metric may modify the energy condition; no strong-field geometry has been solved. A proposal relying on that change must reproduce observed weak-field cluster dynamics rather than introduce an unmeasured relativistic potential.

This tests passive entry from outside. Material already produced within a region, evolution through a phase transition, live changes in matter density, and scalar energy exchange are distinct possibilities. They require their own conserving dynamics; this report does not exclude them.

## 5. Consequence for the intended galaxy–cluster split

The preceding interface was an existence demonstration of a filter. It was not evidence that the filter's density scale lies between galaxies and clusters. The actual cluster gas check now goes the wrong way at the tested point: the mechanism suppresses entry into the systems where extra cold gravity is required.

It is therefore premature to claim a galaxy-law success. No SPARC volume-density comparison is fabricated from rotation curves: disk geometry, scale height and baryonic profiles would be needed. A necessary cluster gate already fails under the tested local capture approximation, so such a comparison cannot turn this unchanged example into a successful common model.

Changing s or r could shift the threshold. The general dependence is explicit:

    y=[1-s(1+r)]/(1-s), f=1-sy, u=r+(1-y)²,
    rho_barrier/D = 4(1-s)y/s + 8y(1-s)/(s f²),
    rho_barrier / [3 M² H_J²] = (f/u)(rho_barrier/D).

This is a useful constraint on any microscopic selection of those coefficients. Selecting them after this data comparison solely to put the barrier between systems would be fitting, not deriving them. It is not done here.

A viable successor needs a derived environment-dependent response beyond this illustrative density threshold, or a production/transport history that demonstrably bypasses the passive-entry obstruction. It must also preserve the galaxy force law, select the reservoir and fix the response normalization. None of those obligations is resolved by the stable wall.

## 6. Verification and provenance

Current results: `run_fixed/result.json` and `run_fixed/manifest.json`. They retain every shell/reference-scale row and all twelve smooth-wave probes. The independent astronomical-unit versus SI density calculation agrees; the deliberate R500-unit mutation fails it. Both current normal and mutation records validate against the input hashes.

The first BVP run failed because concatenating two floating-point meshes produced nearly duplicate nodes (minimum spacing 3.55e-15 at w=10). This was a numerical mesh construction error, not a physical instability. Rounding coordinates before deduplication removes those intervals; an explicit minimum-spacing check now guards the mesh. The original failed run and script are preserved under `run/`, whose old script hash is superseded. No acceptance tolerance, density, momentum or model coefficient was adjusted to obtain the successful run.

The calculation is self-reviewed, single-threaded and bounded to 120 seconds. It is a local candidate diagnostic with central observational inputs and specified sensitivities, not a fully correlated exclusion or a formation simulation. The original parameter-free mechanism goal remains OPEN. The prior ideal-interface positive result remains valid in its limited setting; its promotion to a working cluster/galaxy filter is not supported.
