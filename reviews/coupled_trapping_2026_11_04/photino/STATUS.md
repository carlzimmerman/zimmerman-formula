# CT09 photino status, 4 November 2026

**The combined production goal is unresolved.** Leading microscopic widths,
both directions of charged-carrier conversion, conditional photino source
shapes, a Pauli check, stable companion obligations and repeated-emission
event/energy costs are computed. See `DERIVATION.md` for assumptions.

- Preferred source: `run_source004/result.json`; eleven controls pass.
  `source.py:atx(x)` is the cached API for kinetics. Physical tree charged
  scalars, charged Takagi parents, and raw unbroken gauginos are projected
  explicitly. F -> S+chi opens at x=3.8374251348747075. Reverse S -> F+chi
  operates on the inner side; oscillations can permit repeated emission.
- Massless unbroken-gaugino branching is U1:SU2:SU3=1:1.8:3.2, hence one
  direct photino per six gauge decays on average. One-pass initial-yield
  comparisons are not all-history abundance bounds. Full-DM direct source
  requires 272.496 or 7.234 gauge emissions per initial canonical/protected
  carrier, before additional neutral cascades or quantum/statistical changes.
- `run_phase001/result.json`: all five controls pass. A hypothetical
  fixed-background all-parent prompt burst has f_chi,max=22--187 and is
  Pauli inconsistent. This is not the integrated Hubble source. Its raw
  cold momentum spectrum cannot be assigned its naive abundance.
- For a phase-space-respecting full-DM population, the early constant-mass,
  collisionless comparison has minimum mean travel 4.51718 kpc canonical
  and 47.2971 pc protected. The protected floor permits a 1 kpc comparison;
  it does not demonstrate an actual cold yield. Late production, changing
  mass and interactions lie outside this transport control.
- `run_audit001/result.json`: four orthogonal controls pass; Pauli-floor
  travel agrees to 2.6e-12 relative after exchanging integration order and
  independently fixing present number density.
- `run_orbit003/result.json`: six controls pass for an unbackreacted
  two-state conversion diagnostic on the fresh carrier-conserved zero-loss
  orbits. Gauge emissions per initial carrier are 10.0229 canonical and
  1.08229 protected, giving 3.633 and 14.777 percent of full DM as direct
  photinos. Birth-energy cost is 52.57 and 5.51 percent of initial physical
  hidden energy per carrier, after restoring the potential origin reference.
  Pauli/Bose/inverse reactions, changed carrier force,
  inherited momentum and action feedback are omitted: this is a useful
  work/optical-depth control, not a physical history or universal bound.
- `run_parameter001/result.json`: five controls pass for a necessary-gate
  map at the actual resonance branch t=sqrt(60)/Z0. The early 1 kpc Pauli
  mass floor is 86.5070 keV. A concrete e=.003, mu=2e6 GeV point has
  m_chi=104.731 keV, partial survival at least .999679, Pauli minimum travel
  .786880 kpc and ideal vacuum-pole lower-relic/gate ratio .536922 even
  starting at Tc/mu=.0005. Thus the necessary gates overlap. This is not an
  actual depletion/source history or retuned stable gravity packet.
- `run_current001/result.json`: eight controls pass for the coordinator's
  actual lighter scalar candidate. The gravitino channel is open:
  m_chi=104.734840 keV and m_3/2=1.868980 keV. Summing eaten and arbitrary
  uneaten photon-current channels gives leading inclusive lifetime at
  least 1.35499610e21 s, survival at least .999678652, and a fixed-mu
  99-percent mass ceiling 208.505870 keV. This uses the full fixed leading
  hidden-current norm. Quantum current matching, other operators and other
  loss channels are not bounded; it is not the physical total lifetime.
- Charged-scalar yield must fall below 1.89607e-15 canonical or 6.39858e-17
  protected for the stated ten-percent rest-density gate. Exact charge
  conservation does not prevent pair annihilation; no annihilation history
  is inferred here.

Leading rigid projection and finite one-loop mass insertion are explicit
approximations. The transverse neutral SUGRA 1PI current/pole problem remains
uncomputed. Scalar/fermion conversion energy, inverse decays, Pauli/Bose
factors, charged annihilation and cascade feedback still require one
energy-consistent kinetic history.

Base ancestry: requested Git `285353a57bc1c21662c5565830bbc97ac5b0f7f9`;
actual before/after input hashes and runner-observed moving revision are in
`BASE_INPUTS.json` and the manifests. Successful records measure RSS; failed
source001--003 retain exact original sources and diagnostic logs, with
missing failed-run RSS explicitly recorded in `inputs_historical/archive_map.json`.
The first orbit-control run also fails only at NumPy-bool serialization and
is archived there; preferred orbit003 records RSS successfully. The successful
orbit002 source is preserved because its reference-energy ratio had been
labelled hidden energy; orbit003 distinguishes both quantities explicitly.

Self-review: mathematical prose and displays in `DERIVATION.md` were reviewed
for notation, units and statistical-source distinctions. No mathematical
claims are inferred from a run-completed flag alone. Reproduction commands
are in `REPRODUCE.md`.
