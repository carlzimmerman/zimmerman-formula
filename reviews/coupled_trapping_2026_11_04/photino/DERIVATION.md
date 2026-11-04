# CT09 photino source and charged companion, 4 November 2026

This package determines a leading microscopic source and necessary constraints.
It does **not** establish simultaneous vacuum survival, charged-pair removal,
and the photino dark-matter abundance. The protected point remains compatible
with a 1 kpc coldness comparison at the level of the Pauli floor; its actual
distribution and yield require the coupled collision problem.

## Inputs and accuracy

The contract is `../CONTRACT.md`; the requested base revision is
`285353a57bc1c21662c5565830bbc97ac5b0f7f9`. The component representation and
mass code date from 1 November 2026, the gravity packets from 3 November, and
the fixed-occupation stationary packet from 4 November. Exact hashes, rather
than the moving shared branch, determine the ancestry. `BASE_INPUTS.json`
lists every source004 execution input and before/after hash. In particular:

| Input | SHA-256 |
|---|---|
| `source.py` | `b24e0dd37176b838cbe790d71978a37567737a98c87430c01187b8aade2b3973` |
| TP04 `gaugino_threshold.py` | `c04f440eec7aafb669d517e1490fd37a79410415a3c340ddd5a14877feab4ba4` |
| TP03 `two_loop/model.py` | `d273fa59914fb4a3d7f07675100f8bfecff6b03cfae809c75e4e4b424dbc26dd` |
| TP03 `spectrum_pressure/spectrum.py` | `3c35638eb2bf55dcf1b66142e6a5cf826deccfa2cbf4f29344b4d93e996f5ae6` |
| TK08 `run_stationary_002/result.json` | `bdf4d18b436b01deaf66ba2eec299554cdc411919a6140a1b8bcb4e5d37bb373` |

We use e=h=lambda=.003, g=sqrt(29/200)e, mu=sqrt(f), x=X/mu.
The charged masses and mixing matrices are the complete rigid physical tree
bases. The finite-splitting leading one-loop unbroken-gaugino mass is inserted
in final-state kinematics. The external photino is the raw unbroken U1
gaugino at this order. No transverse SUGRA neutral 1PI pole, wavefunction or
transition-current matching is supplied by this calculation. In particular,
no TT-only neutral mass is substituted for a physical SUGRA eigenstate.

The frozen FD occupation with gspin=24 and xi=Tc/T_SM=.02 is an initial
condition. It is not a result about reheating or chemical equilibration.
The reference rho_DM/s=.44e-9 GeV and ten-percent charged allowance are those
of the shared contract. Calculations with fixed x and Tc are source
diagnostics, not a trajectory.

## Microscopic projection and two directions

For real physical scalar S_a, write

    L_int = -1/2 y_ij,a S_a psi_i psi_j + h.c.

The leading external-gaugino vertex follows directly from
`-sqrt(2) g phi* T^A psi lambda^A` in Martin, *A Supersymmetry Primer*,
[v7, Eq. (3.4.9)](https://arxiv.org/pdf/hep-ph/9709356v7), authenticated
4 November 2026. With psi_old=U psi_mass and delta phi=E O S, the actual
projection used here is

    y_e,u,a = sqrt(2) g sum_Aki ext_Ae (EO)*_ka R_Aki U_iu.

Only the parent chiral component enters this vertex. The charged gaugino
admixture of the parent must not be treated as an additional chiral field.
The tree unbroken external gaugino has no chiral component, so no
superpotential-Y term enters this particular raw-gaugino vertex.

The 98-real-scalar and 73-Weyl bases are adapted within degenerate mass blocks
to residual U1 charge squared. Twelve charged gauge Goldstone zero modes
are removed. There are 36 physical charged scalar reals and twelve Weyls in
the lightest charged fermion block. At x=0 the lowest charged scalar block
contains 24 real modes because two twelve-real branches coincide; at x>0
in the table it contains twelve. Reverse widths at x=0 average over the
whole 24-dimensional block.

A useful independent completeness identity, before Goldstone removal, is

    (1/12) sum_u,a |y_U1,u,a|^2
       = 2 g^2 (5/12) P_chiral.

It holds to the stated numerical tolerance over the complete tested grid.
The light mass and P_chiral are independently checked against the exact
broken-sector 3x3 matrix given in TK08. The adapted Takagi residual, charge
normalization and scalar count are also checked.

For a fermion parent of mass M, daughter photino mass m and real scalar mass
s, the parent-spin-averaged trace is

    |A|^2_bar = |y|^2 (M^2+m^2-s^2) + 2 Re(y^2) M m.

Consequently

    Gamma(F -> S+chi)
      = sqrt(lambda(M^2,m^2,s^2))/(16 pi M^3) |A|^2_bar.

For the reverse scalar decay, with the same y and distinct final fermions,

    Gamma(S -> F+chi)
      = sqrt(lambda(s^2,M^2,m^2))/(8 pi s^3)
        [|y|^2(s^2-M^2-m^2)-2 Re(y^2) M m].

Here lambda is the Kallen polynomial. The code evaluates its factored
two-body form. Charged Dirac widths result by averaging the twelve Takagi
parents and summing physical real scalar daughters. A separate chiral
Dirac benchmark reproduces h^2 M(1-s^2/M^2)^2/(32 pi).

The forward U1 channel opens at

    x = 3.8374251348747075

in the finite [1,10] threshold bracket. Exact finite final gaugino masses
are retained; the reverse threshold lies on the scalar-heavier side. The
following numbers are widths divided by mu:

| x | F -> S+all 12 unbroken gauginos | lowest S -> light F+all 12 unbroken gauginos |
|---:|---:|---:|
| 0 | 0 | 8.44717998e-10 |
| 1 | 0 | 6.26636138e-10 |
| 2 | 0 | 2.44895072e-10 |
| 3 | 0 | 3.60027068e-11 |
| 5 | 9.57332709e-12 | 0 |
| 7.5 | 2.06269148e-11 | 0 |
| 10 | 1.70852665e-11 | 0 |
| 20 | 4.33815011e-12 | 0 |
| 30 | 1.48244233e-12 | 0 |

These are only raw unbroken-gaugino final states. The microphysics worker's
slightly larger all-neutral-zero-fermion sum also contains the rigid
Goldstino direction; it must not be relabelled photino. That difference is
about .09 to 1.06 percent at the compared displaced points.

In the massless-final-gaugino limit the widths satisfy

    U1 : SU2 : SU3 = (5/12) : (3/4) : (4/3) = 1 : 1.8 : 3.2.

This follows from the (3,2) representation Casimirs and is independently
verified by projection. Thus direct photinos are one sixth of these gauge
decays. Additional open channels decrease the immediate branching fraction.
Finite gaugino-mass changes to this ratio are tiny in these examples.

The maximal tabulated forward all-gaugino width is about 1.13e-5 times the
origin-roll rate 1.825e-6 mu. The origin reverse rate is about 4.63e-4 of
that rate. Conversion is slow during an individual fast roll but need not
be slow over a Hubble interval. On the conditional frozen stationary
examples, the photino partial width alone has Gamma/H=152--1084 canonical
and 4.56--33.46 protected at Tc/mu=.003--.00064. This is a width comparison,
not an actual integrated decay fraction.

## Charge, one pass, and repeated emission

A single decay retains one unit of charged-carrier number before pair
annihilation. At the admitted outer points the lightest carrier is a charged
scalar. Exact charge conservation stabilizes the lightest charged state
against purely neutral decays; it does not conserve particle-plus-antiparticle
number. Pair annihilation and charge-preserving conversions must be evolved.

The assumed initial FD yield is Y0=3.74543843e-7. With no regeneration, one
pass through the light charged fermions would supply at most 2.2019 percent
of canonical dark matter or 82.9408 percent of protected dark matter even
if every decay made a photino. The direct gauge branching lowers those
figures to .36698 percent and 13.8235 percent. These one-pass comparisons
are **not** bounds on a history that regenerates the heavier carrier.

| quantity | canonical | protected |
|---|---:|---:|
| final m_chi | 25.8667 keV | .974358 MeV |
| stable charged scalar mass | 23.2059 TeV | 687.652 TeV |
| full-DM Y_chi | 1.70103e-5 | 4.51579e-7 |
| charged Y gate | 1.89607e-15 | 6.39858e-17 |
| N_charged/N_chi gate | 1.11466e-10 | 1.41693e-10 |
| remaining fraction of initial charged yield | 5.06235e-9 | 1.70837e-10 |

Oscillating x can change which carrier is heavier. An F can emit a gaugino
on the outer side and the resulting S can emit another on the inner side.
The field then supplies mass work. Ignoring this possibility would create
an invalid one-photino-per-initial-carrier argument. With a direct photino
branching of one sixth, the full-DM number target requires 272.496 gauge
emissions per initial canonical carrier, or 7.23407 protected. If every
half-cycle achieved a conversion, these are respectively 136.248 and
3.617 full two-conversion cycles per initial carrier. These are required
event counts, not a demonstration of enough available cycles or conversion
probability. Photinos from additional later neutral cascades are separate.

For the fixed frozen-branch birth examples Tc/mu=.003--.00064, the required
gauge radiation energy is .209--.326 mu per initial canonical carrier and
.00559--.00865 mu per initial protected carrier. It is computed as

    (Y_chi/(Y0 B_chi)) <E_gaugino>/mu.

The nearly massless gauge daughters share the same boost at this order.
This is the emitted energy that a repeated-emission mechanism must account
for, not a universal bound on available field work. Expansion, changed
occupations and subsequent massive/neutral cascades can change the energy
budget. The charged-pair removal obligation remains after repeated emission.

## Rest momentum, rate source, and a hypothetical prompt burst

The exact rest momentum is

    k = sqrt(lambda(M^2,m_chi^2,s^2))/(2M).

For the finite outer vacua it is hundreds of GeV canonical and many TeV
protected, despite a light photino. Early production can still be cold
because of redshift. Rest momentum alone is not a coldness prediction.

For an unpolarized parent, the massless-daughter lab momentum is uniform
between k(E-P)/M and k(E+P)/M. Define u=p_chi/Tc, z=P/Tc,
m=M/Tc and kappa=k/Tc. For a **hypothetical burst in which every initial
parent at one fixed x,Tc eventually decays**, with branching B, the unblocked
photino occupation is

    f_chi(u) = (gF B/gchi) m/(2 kappa u^2)
               integral_zmin^infinity dz z/(exp(z)+1),
    zmin = m |u^2-kappa^2|/(2 kappa u),
    gF=24, gchi=2.

This uses the initial parent number distribution. It is not the actual
instantaneous rate source and not a distribution integrated over a Hubble
interval with varying masses, populations or blocking. The instantaneous
rate instead contains M/E time dilation:

    df_chi(u)/dt = (gF/gchi) Gamma_chi m^2/(2 kappa u^2)
                  integral_zmin^infinity dz
                    z/[sqrt(z^2+m^2)(exp(z)+1)].

Correspondingly, the number-weighted hypothetical prompt burst has
<p_chi>=k <E/M>, whereas the normalized instantaneous rate has
<p_chi>=k/<M/E>. `source004` reports both first moments.
`phase001` computes the prompt-burst distribution itself, not a kinetic
solution. The massless boost is accurate here because m_chi/k is below
7e-8 at the examined nonzero-source stationary points; the rest-frame
phase space already retains the finite gaugino mass.

For B approximately one sixth, the unblocked burst has f_max=22.49--186.63
canonical and 21.65--187.01 protected. Thus this particular burst
normalization is Pauli inconsistent even at its one-pass yield. It cannot
be used as an actual abundance or actual cold distribution. A source-only
fixed-parent exposure f=1-exp(-A), and clipping min(1,A), are serialized
diagnostics; neither follows the disappearing parent, inverse process,
bosonic scalar occupation, field or replenishment. They do not replace a
coupled collision operator.

The collision statistical factors must include, for example,

    F -> S+chi: fF(1+fS)(1-fchi) - fS fchi(1-fF),
    S -> F+chi: fS(1-fF)(1-fchi) - fF fchi(1+fS).

An actual production history distributed over changing momenta need not
have the large f_max of a fixed-background all-parent burst.

## Independent Pauli and coldness control

For any isotropic spin-balanced fermion occupation 0<=f<=1 with number
density n_chi and gchi=2, a filled Fermi sphere has

    pF = (6 pi^2 n_chi/gchi)^(1/3),  <p>_min = 3 pF/4.

Filling the lowest momenta minimizes the expectation of every increasing
function of momentum: shifting occupied phase-space volume from a higher
momentum to an unfilled lower one decreases that expectation. This gives a
uniform Pauli constraint at fixed final density and mass, without assuming
the prompt-burst shape or a fermion FD distribution for the photinos.

At birth g*s=106.75, the full-DM target requires pF/T_SM approximately .287
canonical or .0856 protected. The corresponding present pF values are
2.23661303e-14 GeV and 6.67213941e-15 GeV. They are fixed by final density,
not by xi. The naive prompt-burst mean p/T_SM=.0075--.024 is too small to
accommodate the target number in unfilled low-momentum states.

Travel is a further **conditional** control. We use constant final photino
mass throughout propagation, no subsequent photino scattering or cooling,
early production at the stated Tc/mu values, and the explicitly declared
background H0=67.4 km/s/Mpc, Omega_m=.315, Omega_r=9.2e-5. Then

    L(p0) = (c/H0) integral_ab^1 da
             [p0/sqrt(p0^2+(a m_chi)^2)]
             /sqrt(Omega_r+Omega_m a+Omega_Lambda a^4).

This is increasing in p0. The phase-space rearrangement therefore gives a
minimum mean comoving travel by averaging L over the filled sphere:

| conditional propagation quantity | canonical | protected |
|---|---:|---:|
| naive overoccupied prompt burst, mean travel | .192--.578 kpc | 6.10--18.72 pc |
| filled sphere at full-DM number, minimum early-birth mean travel | 4.51718 kpc | 47.2971 pc |
| filled sphere, post-recombination travel alone | .311833 kpc | 2.46955 pc |

The first row is not a physical distribution because of its overoccupation.
The second row exceeds 1 kpc for the canonical point but permits the
protected point. At 90 percent of the full-DM number, scaling momenta by
.9^(1/3) gives a travel at least .9^(1/3) times the full-density value, so
the canonical lower comparison remains above 4.36 kpc under these same
assumptions. The post-recombination-only canonical bound does not exceed
1 kpc. Arbitrary late production, substantial mass evolution during
propagation, entropy changes, interactions or a different expansion history
are not excluded by the early constant-mass result. Coldness by itself
does not establish the protected yield or charged-particle annihilation.

`audit001` independently normalizes pF from present number density and
interchanges the filled-sphere and time integrations. Its two travel values
agree with `phase001` to 2.6e-12 relative or better. This is an orthogonal
numerical check of the conditional calculation, not independent full model
matching.

## Repeated conversions on a fixed reference orbit

`run_orbit003` performs a further discriminating calculation. It consumes
the completed `../kinetics/run_canonical_zero2_001/result.json` and protected
analogue, reconstructing each stored orbit from its energy, turning points,
original frozen occupation and pinned TK08 potential. It averages both
conversion directions over the orbit, including M/E time dilation, and
evolves normalized F and S fractions. Both carrier species are assigned the
same conserved comoving momentum shape. The continuous two-state equation
is integrated exactly within piecewise-constant small time intervals.
Gauge emission and emitted energy are counted at each birth.

This holds the original F-only, zero-loss orbit fixed even when conversion
would change its force or energy. It neglects Pauli/Bose factors, inverse
scatterings, non-gauge channels, neutral cascades and momentum changes
inherited at each conversion. It is a counterfactual optical-depth and work
control, not a consistent history and not an upper bound on every full
network. In particular, the emitted physical energies summed over births
are not a comoving radiation-energy ledger.

| fixed-orbit result through Tc/mu=.0005 | canonical | protected |
|---|---:|---:|
| gauge emissions per initial charged carrier | 10.0229 | 1.08229 |
| direct photinos per initial carrier | 1.67048 | .180381 |
| direct photino fraction of full DM | .0363297 | .147771 |
| emitted gauge energy per initial carrier, in mu | .0101411 | .00106172 |
| emitted energy / initial physical hidden energy per carrier | .525721 | .0550545 |
| emitted energy / initial origin-subtracted reference energy per carrier | .685687 | .0718136 |

The physical initial energy restores the pinned `T0_origin_reference_mu4`
to the origin-subtracted energy serialized by kinetics. An earlier source
version in `run_orbit002` labelled the reference-energy ratio as hidden
energy; its event counts and emitted energy are unchanged, but that label
is corrected in preferred `run_orbit003`. Both ratios are now explicit.
Neither comparison is a universal work bound over an expanding history.

The momentum-bin initial yield is 3.6994e-7 here, rather than the exact-FD
3.74544e-7, because the consumed reference orbit uses 32 bulk momentum bins.
The table uses that actual serialized normalization. Repeated emission is
therefore material in the canonical reference orbit, but the reference
calculation neither reaches the target direct yield nor retains a valid
unchanged energy/action history. The canonical emitted-energy cost alone
makes its feedback important. In the protected reference orbit there is
only a small enhancement over one conversion per carrier.

The 12/24 orbit-node comparison changes event count by .113 percent
canonical and .019 percent protected. Rate grids dx=.1/.05 differ by at
most .0051 percent; 16/32 temporal substeps differ by at most .0281 percent.
Six numerical and invariant checks pass. These are discretization controls
of the specified counterfactual, not error bars on the omitted plasma
physics. Its 41.73 s physics runtime and 125730816-byte peak RSS satisfy
the shared per-job caps.

## Necessary parameter overlap on the resonance branch

At the coordinator's request, `run_parameter001` maps three necessary gates
at fixed t=sqrt(60)/Z0, using the root's uniform pole ceiling and the
microphysics bosonic-width floor. It varies equal weak couplings e and the
independent scale mu by tree homogeneity. This is not a collection of
retuned stationary gravity packets. A background at the resonance radius
must still be established by an actual stable gravity/vacuum calculation.

At e0=.003, mu0=18170662.1115 GeV, the actual resonance radius is
x=25.4000254000. Its leading photino mass is 951.513531 keV, rather than
the outer-vacuum 974.357794 keV. The leading hidden-current massless-final
width gives partial lifetime at least 1.49175181e20 s here, with fixed
n=2.9999 and F_hidden=mu^2/sqrt(31). This bounds the specified partial
operator; unknown additional operators or current corrections are outside
the guarantee.

The homogeneities are

    m_charged proportional to mu sqrt(e),
    m_chi proportional to mu e^(5/2),
    sigma_pole,max proportional to mu^(-2) e^(-1),
    T_SM,start proportional to mu sqrt(e),
    L_pole proportional to mu^(-1) e^(-1/2),
    tau_partial,lower proportional to mu^(-1) e^(-25/2).

Two actual finite one-loop evaluations at e=.0015 and .006 independently
check the photino mass homogeneity. Let u=mu/mu0, v=e/e0 and w=u sqrt(v).
If L0 and gate0 denote the root's reference pole loss integral and charged
yield gate, then for an initial yield Y0 the exact necessary pole gate is

    [1/Y0+K L0/w]^(-1) <= gate0/w,
    w^2 <= gate0 (w/Y0+K L0).

Thus w is bounded above by the positive root of this quadratic. K=1 uses
the vacuum absorptive matrix. K=6.18474095 uses the looser cross-section
ceiling with every neutral FFS width blocked but the positive SSS floor
retained. The asymptotic lower-relic/gate ratio scales as mu^2 e, or as
m_chi^2 e^(-4) at fixed photino mass. Allowing a lower bound below the gate
merely avoids that obstruction; it does not establish actual annihilation.

Using the same early constant-mass collisionless Pauli travel control, the
full-DM 1 kpc gate requires m_chi>=86.5069554 keV. The 99 percent leading
partial-survival gate is tau_partial,lower>=age/[-log(.99)], with
age=4.3549488e17 s. The three necessary conditions have these intersections
in equal coupling e; the admissible mu interval is serialized at 151
couplings and given by the analytic lower/upper curves in the result:

| pole absorptive model | reference start Tc/mu at e=.003 | e interval with 1 kpc and 99% partial survival |
|---|---:|---:|
| vacuum widths | .00466 | [.00133578, .00431466] |
| vacuum widths | .0005 | [.00233393, .00431466] |
| all FFS blocked, SSS floor | .00466 | [.000847039, .00431466] |
| all FFS blocked, SSS floor | .0005 | [.00147998, .00431466] |

The weaker requirement tau_partial,lower>=age raises the common upper
endpoint to e=.00683485; it guarantees only exp(-1) survival in this
partial channel at its boundary, not 99 percent.

One concrete necessary-gate example is

    e=.003, mu=2e6 GeV,
    m_chi=104.730750 keV, m_charged(on pole)=77.459667 TeV,
    partial survival >= .999678726,
    Pauli minimum early-birth mean travel = .786880 kpc.

Its ideal-pole lower-relic/gate ratio is .0576097 for the earliest start
or .536922 for the .0005 start using vacuum widths; the SSS-floor ceilings
give .00931481 or .0868140. These satisfy the three necessary gates. They
do not supply the photino abundance, the pole velocity/occupation history,
actual charged depletion, a stable retuned SUGRA packet, total photino
survival, or the dark-energy scale. Scalar annihilation into photinos and
neutral cascades remain distinct source leaves. The parameter map leaves
a concrete candidate region for those calculations instead of extending a
benchmark obstruction into a universal exclusion.

## Leading inclusive current after the gravitino channel opens

The coordinator's finite lighter candidate has epsilon=.0249201741 and
n=2.97507983. Its physical gravitino channel is open. Keeping only the
uneaten n/3 current would omit a real leading loss channel. `run_current001`
therefore reconstructs m_3/2 from the candidate's serialized Kähler data,
evaluates the leading photino mass at its actual x=25.3990254000, and
includes both the eaten and uneaten directions.

For a pure photino, the physical massive-gravitino width is

    Gamma(chi -> photon+gravitino)
      = m_chi^5/(48 pi M_P^2 m_3/2^2) P(r),
    P(r)=(1-r)^3(1+3r), r=m_3/2^2/m_chi^2.

This is the standard full-spin result of Ellis, Olive, Santoso and Spanos,
[*Gravitino Dark Matter in the CMSSM*, v4, Eq. (4)](https://arxiv.org/pdf/hep-ph/0312262v4),
authenticated 4 November 2026, with their photino overlap C_chi,gamma=1.
Since P'(r)=-12r(1-r)^2, 0<=P<=1 on the open interval. Thus including
the physical transverse gravitino states does not evade the massless
fixed-current upper-width envelope.

At the leading small-field current level, the eaten and uneaten squared
weights are epsilon/3 and n/3 and sum to one. Any complete orthonormal
redistribution among uneaten poles preserves the remaining norm. Arbitrary
accessible spin-one-half pole masses multiply their widths by
(1-m_j^2/m_chi^2)^3<=1, and closed channels contribute zero. Therefore,
for this specified leading photon-current operator,

    Gamma_eaten + sum_j Gamma_uneaten,j
       <= Gamma0 = m_chi^5/(16 pi F_hidden^2).

The finite candidate gives m_chi=104.734840 keV, m_3/2=1.86898000 keV,
F_hidden=7.18421208e11 GeV^2. The eaten weight inferred from the physical
gravitino mass is .008306724269, versus geometric epsilon/3=.008306724717;
their small difference is below the declared leading current accuracy.
The geometric uneaten plus that exact eaten normalization is
.999999999553. Its actual gravitino kinematic factor is .999999392.

The resulting full-unit-current inclusive bound is

    Gamma_inclusive <= 4.85766680e-46 GeV,
    tau_inclusive,current >= 1.35499610e21 s,
    survival_current >= .999678652.

No uneaten pole mass has been assigned. At fixed mu=2e6 GeV, the same
full-current norm guarantees 99 percent survival for m_chi<=208.505870 keV.
The small old-map factor n_ref/3 with n_ref=2.9999 can be removed by
rescaling the map's upper coupling endpoints by (n_ref/3)^(1/10);
it changes none of the displayed interval conclusions.

If the only correction were a common multiplicative current amplitude,
the candidate could tolerate a factor up to 5.592 before the 99 percent
gate failed. This is a conditional sensitivity number, **not** a derived
bound on quantum corrections. Unitary mixing cannot increase a fixed
current norm, but uncomputed transverse 1PI residues/current coefficients,
new transition operators or other loss channels can change that premise.
The statement is inclusive within the specified leading current, not a
matched physical total photino lifetime. Eight checks pass in .082 s with
measured peak RSS 80986112 bytes.

## Run records, failed histories, and continuation

Preferred records are `run_source004`, `run_phase001`, `run_audit001`, and
`run_orbit003`, `run_parameter001`, and `run_current001`.
They complete with respectively 11, 5, and 4 checks true. Measured peak RSS
is 118325248, 56705024 and 56164352 bytes. Physics runtimes are 3.47 s,
.248 s and .0073 s. Each fresh v2 job has a 240 s wall cap, 235 s CPU cap
and one numerical-library thread; no macOS address-space or affinity cap.

`run_source001` and `run_source002` fail because the origin's lowest charged
scalar block is 24-dimensional rather than the initially assumed twelve.
The second run adds the diagnostic that exposes that degeneracy.
`run_source003` reaches serialization and fails on a NumPy bool. Their
original source bytes and hashes are preserved under `inputs_historical/`
with `archive_map.json`; no failed run is promoted to physical evidence.
Peak RSS was not emitted before those exceptions and is explicitly
unavailable, rather than reconstructed. `run_orbit001` also fails at NumPy
bool serialization and has an exact archived source; its RSS likewise was
not emitted. The corrected orbit script now emits RSS in a `finally` block
even if a subsequent assertion fails. No prior TP03--TK08 file was edited.
The successful but superseded orbit002 source is also preserved, together
with its label-correction mapping to preferred orbit003.
The necessary parameter map completes five checks in .223 s with measured
RSS 106102784 bytes. Its exact root/microphysics input hashes are added to
`BASE_INPUTS.json` and recorded before and after in its v2 manifest.

Open obligations are the momentum-dependent blocked forward/inverse source,
two charged carrier populations and their mass work, actual annihilation
exits, nonabelian/neutral cascades and the field/action history. A useful
next diagnostic is the two-state conversion optical depth on the
carrier-conserved zero-loss orbit; it must remain labelled an unperturbed
orbit control until source energy and the changed carrier force are fed
back; `run_orbit003` now supplies that unperturbed control. Charged scalar
pair annihilation into photino pairs via charged-fermion exchange is a
distinct possible source, with daughter momentum of order the heavy scalar
mass, not the small conversion splitting. The direct-conversion one-pass
and event-count comparisons do not bound that process. The protected early
cold source remains a plausible leaf, not a completed DE/cold-DM history.
