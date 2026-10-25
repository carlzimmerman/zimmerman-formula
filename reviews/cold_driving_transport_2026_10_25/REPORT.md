# Repeated driving and spatial concentration

## Result

Repeated driving can transfer energy into the unchanged scalar candidate. An
explicit periodic source produces parametric instability, and integrating the
full nonlinear potential verifies growth from a small seed with an independently
tracked work budget. This is a positive mechanism result, **not** a predicted
cluster abundance: the source's timing, energy, initial seed and stopping phase
remain unspecified by the action and previous data.

Spatial redistribution within the measured annulus does not close the earlier
production deficit: the single-jump energy supplies only 1.93–4.79% of the
integrated requirement in all 28 complete positive profile alternatives.
Redistribution can increase a central density, but cannot supply the missing
annulus-integrated energy without boundary inflow or additional source work.
This does not exclude transport from the untested core or outside R500.

No new constants were fitted. The tests retain r=1, s=1/4 and eta=1500 pc km/s
from commit 0dbe9d1421. Those inputs themselves still lack microscopic selection.
The Palatini candidate still has no demonstrated derivation of the galaxy law.
We have not found the requested parameter-free, galaxy-safe cluster mechanism.

## 1. Local and global energy identities

Use the preceding report's canonical field and Einstein time and length units:

    V(q,d)=W(q)/D+d A(q),
    W/D=[1+(4 sin²(q/2)-1)²]/cos⁴(q/2), A=sec(q/2),
    q_tt - laplacian q + V_q=0.

On the physical branch |q|<pi define excitation relative to the restored state,

    epsilon = (q_t²+|grad q|²)/2 + W/D-2+d(A-1),
    S = -q_t grad q.

Direct multiplication by q_t gives

    partial_t epsilon + div S = (partial_t d)(A-1).

Thus spatial concentration changes a region's excitation through its boundary
flux. Repeated driving changes it by signed matter-source work. A fixed positive
vacuum term alone is not a continuing source. These equations are for a prescribed
source in a flat Einstein-frame local approximation. Matter backreaction and
gravitational energy are not evolved. With a live metric the corresponding
covariant balance, rather than this flat-space identity, must be used.

The excitation includes q-dependent matter interaction energy. Identifying its
entire value with cold rest energy is a favorable bookkeeping comparison, not a
stress-energy calculation or a Palatini gravitational refit to cluster data.
It can include kinetic, gradient and anharmonic components with pressure.

## 2. Spatial redistribution: integrate before concentrating

The earlier positive-shell table contains 70 name/model/footing combinations.
Only 28 have all five reconstructed shells positive. The others have 3 or 4
positive rows; they are excluded from this complete-profile test, not repaired
by clipping their missing negative shells. These are model alternatives, not
28 independent clusters.

For each complete profile, sum densities times (x_out³-x_in³), with x=r/R500
and boundaries .1,.2,.3,.5,.7,1. Common factors 4pi R500³/3 and D cancel in ratios.
The available density is either the earlier slow-transition yield or the exact
single-jump excitation -0.4+d[sqrt(6/5)-1] in each shell. The required density is
the previous CCT inverse-source benchmark. This preserves the earlier caveat:
that reconstruction has not been repeated in this scalar-tensor gravity.

| Available quantity / required excitation | Range over 28 complete profiles |
|---|---:|
| Single-jump excitation | 0.0193106–0.0479243 |
| Slow-crossing excitation | 9.3881e-14–1.9483e-13 |
| Gas kinetic energy proxy | 1.5471e-6–3.9003e-6 |

The kinetic proxy is sum[.5 rho_gas sigma²] divided by required mass times c²,
using the inherited sigma=vc entries. It is not a measured merger energy, does
not include an assembly tree or all gravitational work, and is not an absolute
bound. It illustrates the serious cost of converting ordinary nonrelativistic
mechanical energy into a new gravitating rest-mass component. A claimed production
run must identify the reservoir paying the source work rather than prescribing
an unlimited density modulation.

At the same mean single-jump excitation density, a hypothetical donor would
need 20.87–51.79 times the tested annulus volume, with perfect conversion and
retention. Extending a uniform donor from .1 R500 gives radii 2.752–3.726 R500.
This is a dimensional budget illustration, not evidence that such material,
density, phase-space flow or capture efficiency exists outside the data.

Internal redistribution alone is therefore insufficient for these profiles
under the flat-space budget and unchanged source. Spatial compression with
additional matter/gravitational work is a different mechanism and is not ruled
out by this arithmetic. No spatial PDE collapse simulation was performed.

## 3. Repeated forcing: a real amplification mechanism

For a small homogeneous perturbation in the restored phase,

    q''+omega²(t)q=0, omega²=(d-8)/4.

There is no additive source: q=0 stays exactly zero classically. A seed from
restoration, quantum fluctuations or another state must be specified. Quantum
production is not computed by setting a classical seed by hand.

At constant frequency the phase-space transfer matrix is

    M(omega,theta)=[[cos theta, sin theta/omega],
                    [-omega sin theta, cos theta]].

Choose density levels d_low=24, d_high=56 as an illustrative sensitivity control,
not a fit. They give omega_low=2, omega_high=sqrt(12). Starting at a displacement
maximum, jumping to high density, evolving a quarter period, jumping low and
evolving a quarter period multiplies the displacement by -sqrt(3). At the same
low-density endpoint the energy increases by 3 per cycle. Half-period evolution
at each level instead gives the identity and no gain. Direct matrix assertions
verify both results. The quarter protocol saturates the linear optimal growth
for its specified phase; it is not a generic merger sequence.

A smooth control d=40+16 sin(Omega tau) has a one-period monodromy matrix. Numerical
spectral radii (amplitude eigenvalue magnitudes) are:

| Omega/sqrt(8) | Spectral radius |
|---|---:|
| .1 | 1 within numerical error |
| .5 | 1 within numerical error |
| 1 | 1.1570402 |
| 2 | 1.4767920 |
| 3 | 1 within numerical error |

All determinants agree with one to better than 1.6e-11. The ratio-one instability
also matters: amplification is not limited to the principal resonance. The
finite scan does not exclude narrow instability bands at other frequencies.

## 4. Nonlinear evolution and energy return

The full potential was integrated for 80 sinusoidal cycles from q=1e-6, q'=0,
tracking the work integral integral[d'(A-1) dt]. The seed and frequency are
sensitivity inputs, not selected physical parameters. Tighter-tolerance results:

| Frequency ratio | Peak excitation / D | Final excitation / D |
|---|---:|---:|
| 1 | .0339484 | .0339484 |
| 2 | 5.95459 | .0252725 |
| 3 | 7.94365e-12 | 3.96218e-12 |

The initial excitation is approximately 4e-12 D. The resonant ratio-two run grows
strongly, reaches |q| about 1.05, and subsequently returns most of that peak energy
to the source. All sampled fields stay on the physical |q|<pi branch. This is
not a full stability proof for coupled matter/metric perturbations. The finite
80-cycle result is neither an infinite-time saturation theorem nor a prediction
of a retained particle population.

Base runs use relative tolerance 2e-10, repeated at 2e-12. Final energies agree
within the declared relative 1e-4 or absolute 1e-10 criterion. The largest base
energy-ledger error is 2.02e-9 D; the largest tight-run error is 1.63e-11 D.
Very small energies are near the algebraic cancellation floor (~1e-15 D) of the
potential evaluation. This does not affect the substantial resonant growth.
The zero-seed run remains exactly zero. Reversing the work-source sign fails
the ledger test as intended.

## 5. Nonlinear bound on work per excursion

A post-run analytic follow-up makes the phase dependence quantitative without
linearizing. Put x=A=sec(q/2)>=1. The full potential satisfies

    W/D-2+8(A-1)=2(x-1)²(5x²+10x+3)>=0.

Thus for d>8 the homogeneous nonnegative excitation E obeys

    E >= (d-8)(A-1), E'=d'(A-1),
    E(t_f) <= E(t_i) exp[integral max(d',0)/(d-8) dt].

On downward excursions E cannot increase. A rise from d_low to d_high can
amplify E by at most (d_high-8)/(d_low-8), regardless of speed. For the chosen
24–56 excursion the bound is 3 per rise; the ideal linear quarter-cycle protocol
approaches this maximal efficiency. This statement does not apply through d=8,
to flux into a subregion, or to a contracting live geometry with extra work.
It is an upper bound, not a claim that each real merger achieves the gain.

Applying the optimistic factor-three arithmetic to the old slow seed/requirement
ratios gives 22–28 maximally effective cycles. The old shell states have different
final densities from the oscillator control, so this is only a scale illustration,
not a matched trajectory or an observed minimum merger count. The exact bound
must use the actual density excursions and source history for each system.

## 6. Timing and the galaxy requirement

With the unchanged eta and frame dictionary, the principal sinusoidal example
requires period pi/[sqrt(8) omega_unit]=14.5048 days. The existing crossing proxies
are .148–1.085 Gyr. They supply no evidence for coherent density pumping on the
required short period. This mismatch does not prove that shocks, substructure,
critical crossings or microscopic modes lack the relevant spectrum. Such a
spectrum must be calculated from the coupled equations, not inserted as an
external sinusoid. Smooth slow driving away from d=8 approximately conserves
the oscillator action; that adiabatic argument alone is not a theorem excluding
all long sequences or high harmonics.

In the separate spherical selective-CCT force bookkeeping, adding a nonnegative
cold enclosed mass changes the galaxy acceleration by G M_c/r². With

    L=[B+sqrt(B²+4AB)]/2, B=M_b(<r), A=a0 r²/G,

preserving the law within fractional allowance delta requires M_c(<r)<=delta L.
No observational delta is chosen here. Exact preservation requires M_c=0 in
that spherical model. This bound cannot be directly imported as a proof for
the Palatini candidate: its baryonic and metric response also need solving.
It remains a clear obligation for any proposed mapping back to the framework.

The periodic source has no demonstrated galaxy exclusion. It will amplify
appropriately seeded modes wherever the same forcing conditions occur. Spatial
supply drawn from galaxy interiors must respect their force allowances; a diffuse
or exterior donor must have independently derived abundance and inflow. Neither
the prescribed sinusoid nor assuming perfect focusing meets these requirements.

## Evidence and next discriminating calculation

Normal and mutation manifests record bounded execution and input hashes; all
raw budgets and oscillator results are in run/result.json. Frozen criteria and
contract describe the finite scope. bounds.py verifies the exact polynomial
identity and computes the explicitly hypothetical cycle/donor arithmetic;
it is a post-run follow-up, outside the original runner manifest. Results are
self-reviewed, not independently certified. No new external source theorem is
used: these are direct identities and computations in the recorded candidate.

Reproduce from repository root:

    python reviews/cold_driving_transport_2026_10_25/check.py --output /tmp/cold-driving-check
    python reviews/cold_driving_transport_2026_10_25/bounds.py

The remaining live route is a self-consistent matter-field calculation that
predicts the source spectrum and tracks backreaction, boundary inflow, retained
pressure and galaxy forces. An arbitrary periodic drive demonstrates possibility
but cannot select abundance. A cosmological or microscopic state must supply
those inputs without fitting them to the cluster target. This checkpoint leaves
that route open; it does not label the original goal solved.
