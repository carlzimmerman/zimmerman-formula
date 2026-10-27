# What the current forest calculations can decide

Read-only assessment, 2026-10-27. The byte hashes and observation time are in
`snapshot_record.json`; the P1D2 primary stdout is copied here so later live-job
updates cannot silently alter this evidence. No fit was rerun or interrupted.

**No calibrated physical upper limit on the M6 population is available from
these calculations.** This is a limitation of the current evidence, not a
claim that the observed forest permits arbitrary M6 populations.

| Calculation | Adequacy and sensitivity | Permitted inference |
|---|---|---|
| Completed P1D1 primary | Null chi-square 137.63/39, p about 6e-13; Asimov separation 5.58, below the frozen threshold 9 | Its linear flux proxy is inadequate; fitted excess and limits do not decide M6 |
| Completed P1D1 k <= 0.1 s/km variant | Null chi-square 17.1/30, p about 0.97; Asimov 8.14; fitted mu about 0.48, delta-chi-square at mu=1 about 1.83 | This chosen template is not excluded. The nominal mu95=1.26 is not a calibrated population limit |
| P1D2 primary output at the saved snapshot | Null chi-square 95.32/36, p=2.91e-7; Asimov 0.44 canonical and 0.16 alternative | Primary run reports NOT DIAGNOSTIC on both footings; robustness runs/final verdict and current execution status are not certified here |
| Late completed P1D3 DESI output, independently checked | Primary null chi-square 7017.365/719; Asimov 24.687; both footings and all seven variants NOT DIAGNOSTIC | Greater template sensitivity cannot rescue the failed adequacy gate. Nominal mu95=0.3355 is not a physical population limit |

P1D3 was produced by the concurrent research work after the original snapshot.
Its checked result hash and exact values are recorded in
[`../population/p1d3_late_output_check.json`](../population/p1d3_late_output_check.json).
This inspection is not an independent rerun or data-release audit. Its
`BLINDING=desi_y1` metadata remains unresolved in the lane's own record. The
model's adequacy failure already prevents the physical-limit inference.

P1D2 improves the physical bookkeeping by putting rare patches in real space,
using an exponential flux map, and applying separate pressure and thermal
smoothing operations. Those improvements do not validate its response. It
uses a one-dimensional lognormal field and FGPA with fitted mean flux and
thermal parameters, omits peculiar velocities, and has no independent
hydrodynamic or controlled response calibration for the specified compensated
mode. Numerical field-power and chord-coverage checks establish construction
identities. They do not establish that real spectra respond to M6 this way.

The original two-phase field also differs from the final skewer prescription:
the patch factor multiplies a spatially varying lognormal density. Setting the
unweighted mean patch factor to one does not make the weighted mean density
identical in each finite realization. The existing stochastic conservation
check is useful within that model; it is not an evolved mass-conserving
galaxy-formation map.

The X57 budget inherited by P1D1/P1D2 constrains a prescribed gas-density
variance. Our exact two-phase correction uses that same numerical budget only
as a benchmark. Point variance, smoothed three-dimensional gas power and
observed one-dimensional flux power are different quantities. Replacing the
dilute variance expression with exact mass accounting does not supply the
missing physical map between them.

The decisive test remains:

1. Define the galaxies that require M6 using their law/dynamical evidence and
   a volume-complete selection, independently of the proposed M6 capacity.
2. Specify their disjoint Lagrangian ancestry, mass/radius distribution,
   retained gas and stars, and any transfer of baryons and cold component.
3. Evolve that same population into forest-epoch gas and spectra on the
   declared background. Validate the physical response against a controlled
   calculation with pressure, thermal broadening, velocities and flux
   saturation, and use independent realizations to assess numerical uncertainty.
   Additional random seeds alone do not calibrate the physical response. A
   successful null fit alone is insufficient.
4. Infer an allowed population and compare it with the required population,
   including the same nuisance and selection assumptions. A positive result
   additionally needs formation dynamics and present-day profiles.

The existing files do not specify all of item 2, and neither forest model
supplies item 3. Another fitted mu on their existing templates cannot close
those gaps. No new native simulation or observational selection has been
invented here to bypass them. This is the exact point where a physical
population-versus-forest verdict remains unresolved.

For the pressure/thermal distinction, see
[Boera et al., arXiv:1809.06980v2, Introduction and Figure 3](https://arxiv.org/html/1809.06980v2).
It supports the distinction between the two processes, not the native M6
response. P1D1's corrected independent sign test is documented in
[`../technical_fixes/README.md`](../technical_fixes/README.md).
