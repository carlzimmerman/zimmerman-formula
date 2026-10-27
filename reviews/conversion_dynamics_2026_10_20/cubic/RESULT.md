# Existing cubic conversion: actual states, channel rates, and memory tests

20 October 2026. Assessment HEAD `b1bb9296dbd20de4d7dc97e4b5f27a7d9b4ad26b`.
Base checkpoint: `reviews/attraction_from_existing_2026_10_20/CHECKPOINT.json`.
Actual read-source bytes are pinned in `source_hashes.json`. This lane writes
only this new directory. No campaign, old packet, publication, owner job,
or Git state is changed.

**Normalized target and verdict: incomplete, with the physical occupation
dictionary and receiver state missing.** The existing scalar fields do
identify source/daughter states and, in a specified host, bound/scattering
states. Their existing cubic vertex fixes transition matrix elements and
conditional capture/release kernels; no new fitted rate is required. An
open source has the already short microscopic decay time. Closing the
two-unbound-daughter channel does not close the bound-plus-unbound channel.
A truly subcontinuum dressed bound object is stable against its vacuum
two-body channel, but the reverse direct capture from that continuum then
also closes. Spectator-assisted formation and ionization use existing
vertices and avoid that two-body kinematic obstruction. They require an
actual host and incoming state to compute rates and lifetimes. None of
these states is yet identified with the canonical S4 free/tether label.

The exact fixed-bath two-state calculation below also distinguishes long
occupied-state survival from long memory of two different preparations.
It does not exclude a driven writer or cooperative memory.

## 1. Actual fields, hypotheses, and inventories

Use the original charge-one daughter `Phi` and charge-two source `X`, with
NR fields `psi,b` and conserved `Q=N_psi+2N_b`. At a common finite
regulator the stated matched retained-source Hamiltonian is

    H=mQ+H_a+H_b+V3+V4,
    H_a=integral psi†[-grad²/(2m)+V_a]psi,
    H_b=integral b†[delta-grad²/(2M)+V_b]b,
    V3=c3 integral (b†psi²+psi†²b),
    V4=kR integral psi†²psi²,
    delta=M-2m>0,
    c3=g_c/(2m sqrt(2M)),
    kR-c3²/delta=lambda_rep/(4m²)>0.                 (1)

`V_a=m Phi_N`, `V_b=M Phi_N` is the stated weak-gravity external-host
approximation when the small detuning mass is retained in gravitational
mass. A finite moving host must be included in the same energy and momentum
ledger. A static potential exchanges momentum with the host approximation
but supplies no energy. Its spectrum and initial state are physical inputs,
not additional interaction constants.

Let `h_a=-grad²/(2m)+V_a`, `h_b,orb=-grad²/(2M)+V_b`,
`h_a u_i=epsilon_i u_i` and `h_b,orb v_A=epsilon_A v_A`, with orthonormal
discrete modes and delta-normalized continuum modes in the final large-box
limit. Daughter energies are `m+epsilon_i`; source energies are
`2m+d_A`, `d_A=delta+epsilon_A`. Thus a genuine elementary source is not a
one-for-one relabeling of a daughter. A localized source/pair carries two
units of the same protected charge.

In a host whose potential approaches zero, negative daughter eigenvalues
are gravitational bound states and its continuum starts at zero. These
are real spectral definitions from the fields. They do not define the
canonical tether label: S4's free population can itself remain bound by
ordinary gravity, and the inspected equations contain no equality between
the source/daughter projectors and the polarization displacement `P`.
The original scalar and force sectors were explicitly left unjoined.

Dependency graph: (1) and an actual host -> spectral modes -> charge-
conserving matrix elements -> continuum/coherent distinction -> conditional
rates and thresholds -> bath state/receiver -> lifetime. The first three
links are derived here. The host/bath and the S4 identification are not
selected by the supplied equations.

## 2. Exact mode vertex and bosonic normalization

Expand `psi=sum_i u_i a_i`, `b=sum_A v_A B_A`, and define

    I_Aij=integral v_A* u_i u_j,   I_Aij=I_Aji.
    V3=c3 sum_Aij I_Aij B_A† a_i a_j + h.c.          (2)

Use unordered normalized pair states
`|ij>=a_i†a_j†|0>` for `i<j`, and
`|ii>=(a_i†)²|0>/sqrt(2)`. The exact vacuum pair-source matrix elements
in this projection are

    g_A,ij=<A|V3|ij>=2c3 I_Aij/sqrt(1+delta_ij).     (3)

The factor 2 for distinct modes comes from both ordered terms in (2).
For a Fock occupation, the individual transition intensities are proportional
to the following squared amplitudes:

| Channel | Capture `ij -> A` | Release `A -> ij` |
|---|---|---|
| `i<j` | `|g_Aij|²(N_A+1)n_i n_j` | `|g_Aij|²N_A(n_i+1)(n_j+1)` |
| `i=j` | `|g_Aii|²(N_A+1)n_i(n_i-1)/2` | `|g_Aii|²N_A(n_i+1)(n_i+2)/2` |

These are exact operator matrix elements, not rates until the time and
continuum approximation is stated. In a thermal bosonic mode
`<n(n-1)>=2 f²` and `<(n+1)(n+2)>=2(1+f)²`; replacing the same-mode
factorial moment by the square of its mean would be incorrect.

## 3. Deriving the continuum rate and its limits

For a matrix element `V_fi`, first-order unitary evolution gives

    P_i->f(t)=4|V_fi|² sin²[(E_f-E_i)t/(2hbar)]/(E_f-E_i)².  (4)

Only after integrating against a sufficiently smooth continuum of final
states and taking the weak-coupling/long-time window does `P/t` approach
`(2pi/hbar)|V_fi|² delta(E_f-E_i)`. Therefore the spontaneous product-mode
source width in that approximation is

    gamma_A=(2pi/hbar) sum_(i<=j) |g_Aij|²
                               delta(d_A-epsilon_i-epsilon_j). (5)

The continuum measures and unordered counting are included in the sum.
For occupied modes, multiply each term by the Fock factors in the table.
The inverse rate uses the same `g`, same energy delta, and reversed
occupation factors. It is a flux/density-dependent association rate,
not the vacuum lifetime with its arrow reversed.

Equation (5) uses uncorrelated one-body final products as a Born channel
basis. When the original contact rescattering matters, replace them by
the actual two-daughter scattering eigenstates of `H_aa=H_a+V4`. In
operator notation the corresponding leading source self-energy is

    Sigma_A(z)=c3² <A| A_pair (z-H_aa+i0)^(-1) A_pair† |A>,
    gamma_A(z)=-(2/hbar) Im Sigma_A(z),                (6)

where `A_pair` includes the bosonic contact map of (2)-(3), and all energies
are relative to `2m`. The physical pole, residue and resummed line shape
must be used near a resonance. Keeping a real source and then adding its
already included resonance again as a separate `2->2` collision rate would
double count. The common contact regulator is retained; no continuum
renormalization theorem is assumed.

For a flat source at rest in volume `V`, `I_(k,-k)=1/sqrt(V)`. Counting
`k,-k` pairs only once gives the NR energy width

    Gamma_NR=c3² m sqrt(m delta)/pi.                 (7)

Indeed `integral d³k/(2pi)³ delta(delta-k²/m)=m sqrt(mdelta)/(4pi²)`.
This checks the pair normalization. It agrees to NR accuracy with the raw
relativistic tree width

    Gamma_rel=g_c²/(8pi M) sqrt(1-4m²/M²),
    tau_rel=hbar/Gamma_rel.                          (8)

At the frozen published rounded benchmark `m=1 MeV,u*=.02,g_c=2168 eV`,
the existing result is `tau_rel about 3.52096e-13 seconds`. This is the
conditional lifetime of a prepared open source, far from a long-lived
macroscopic stored occupation. It is not the lifetime of a dressed bound
state in a host. The old finite resonant-band calculation also explicitly
omitted the actual threshold, quartic rescattering and many-particle
channels, so it cannot certify a host capture or storage lifetime.

### 3.1 Inverse association cannot prolong the bare source's population memory

There is an explicit rate bound even without choosing the incoming density.
Hold a factorized continuum daughter bath fixed, with occupation means
`f_i>=0`, and let `n_X` be the mean occupation of one source mode. Let
`d gamma_ij` denote its nonnegative vacuum differential decay-rate measure
from (5), with positive-energy distinct outgoing modes. Gain minus loss
from the table gives

    d n_X/dt=integral d gamma_ij
       [(1+n_X)f_i f_j-n_X(1+f_i)(1+f_j)]
      =A-Lambda n_X,
    A=integral d gamma_ij f_i f_j,
    Lambda=integral d gamma_ij (1+f_i+f_j)
            >=gamma_vac.                            (8a)

Here `gamma_vac=Gamma_rel/hbar` when the tree relativistic width is used,
or its consistently NR approximation. The bath factorization, continuum
kinetic window and weak coupling are assumptions of this equation. Its
coefficient inequality is exact inside those assumptions and does not
require a Maxwell distribution or isotropic occupation.

Two initial source preparations in the same bath therefore differ by
`Delta n_X(t)=Delta n_X(0)exp(-Lambda t)`. The population memory time
satisfies `tau_mem<=1/gamma_vac`. For an isotropic source at rest,
`f_i=f_j=f_*` on shell, this specializes to

    d n_X/dt=gamma_vac[f_*²-(1+2f_*)n_X],
    n_X,eq=f_*²/(1+2f_*),
    tau_mem=[gamma_vac(1+2f_*)]^-1<=tau_vac.          (8b)

At the existing open-source benchmark that bound is approximately
`3.52096e-13 seconds`. Bose-stimulated inverse conversion can increase
the mean source stock, but it does not slow loss of the source's initial
population information in this fixed bath. This is a result for the
actual unconstrained bosonic source occupation, not an invented hard-core
site. It does not cover a closed coherent source-plus-pair system or a
different stable dressed bound object; those are analyzed next.

## 4. A host closes different channels at different thresholds

Let the lowest daughter one-body energy be `epsilon0<0`. Product final
states have three distinct classes:

| Pair sector | Lowest energy/interpretation |
|---|---|
| Two unbound daughters | Continuum threshold `0` |
| One bound and one unbound daughter | Continuum threshold `epsilon0` |
| Two bound daughters | Discrete levels; coherent mixing, not a continuum width by itself |

For repulsive retained daughter contact, cluster separation leaves the
lowest bound-plus-free threshold at `epsilon0`: the contact vanishes as
the escaping daughter separates. The full coupled two-body Hamiltonian
can also have dressed discrete bound levels; those are not extra outgoing
continuum channels. All statements here use an isolated host with a genuine
bound ground level and no hidden bath spectrum below that threshold.

Consequently `d_A<0` closes two-free release but does not close the mixed
channel if `epsilon0<d_A<0`. Only `d_A<epsilon0` puts the bare source below
every daughter-pair continuum in this static-host approximation. At exact
threshold phase space and matrix-element limits require their own analysis;
no positive rate is claimed solely from a nonstrict threshold equality.
Open kinematics is necessary, not sufficient: angular selection and overlap
zeros may remove a particular matrix element.

For the same conditional Coulomb host used in the preceding scalar packet,
put `alpha=G M_host m`, `q=M/m`. Its one-body ground energies give

    epsilon0=-m alpha²/2,
    d_A=delta-q³ m alpha²/2,
    Delta_h=d_A-2epsilon0=delta-(q³-2)m alpha²/2.      (9)

Thus the derived channel-closure boundaries are

    alpha_CC=sqrt[2delta/(m q³)],
    alpha_BC=sqrt[2delta/(m(q³-1))],
    alpha_BB0=sqrt[2delta/(m(q³-2))].                (10)

Their order is strict. The previous projected attraction interval
`alpha approximately .01010155 to .01154181` straddles `alpha_BC`, about
`.01069` at that same frozen benchmark. Throughout that interval the
two-unbound channel is already closed. In its shallower part a mixed
bound/unbound decay remains energetically open; in the deeper part it
closes too, while `Delta_h>0` still leaves lower discrete pair states.
No host was selected or scanned. Exact continuum Coulomb overlaps and
the finite-regulator full-field transfer remain separately qualified as in
the earlier scalar report.

## 5. Closed channels give coherent states, not a derived capture clock

For one bound pair and one source mode, the exact two-state Hamiltonian
has matrix `[[E_pair,g*],[g,E_source]]`. Set `Delta=E_source-E_pair`.
Starting in either unmixed state, the exact conversion probability is

    P(t)=4|g|²/(Delta²+4|g|²)
           sin²[sqrt(Delta²+4|g|²)t/(2hbar)].          (11)

This follows by subtracting the mean diagonal energy and squaring the
remaining traceless matrix. The forward and backward probabilities are
equal. Discrete resonant mixing produces oscillation and returns; it is
not a one-way capture or release rate. A fitted attempt frequency cannot
be obtained by calling this oscillation a Markov process.

The physically stable vacuum object, when present, is an eigenstate of
the *coupled* charge-two Hamiltonian,

    |B>=Z^(1/2)|X-mode> + sum_(i<=j) phi_ij |ij>,
    E_B<epsilon0,                                   (12)

with a normalizable state and a real pole below all pair continua. Its
two-body vacuum width is zero in the stated Hamiltonian. A projected Ritz
witness alone must meet the previous packet's regulator/full-field
conditions before it establishes the corresponding exact state. In the
attractive projected ground branch the lowest energy is below `2epsilon0`,
so it is also below `epsilon0`; it is not the bare source of (8).

The same energy conservation that closes release also gives

    Gamma_(pair-continuum -> B)=0                    (13)

for direct static-host association without another excited degree of
freedom: every incoming pair continuum energy is at least `epsilon0`,
whereas `E_B<epsilon0`. In particular two unbound incoming daughters have
nonnegative excess energy and cannot end as this isolated lower level.
This is a channel statement, not a no-go for formation with a receiver.
Capture into a bare level and its later coherent mixing do not evade it.

Adding a host's internal excitations supplies actual receiver states, if
they are already part of its equations. Then the cubic matrix element is
`<B;h'|V3|ij;h>` and the delta is
`E_B+E_h'-epsilon_i-epsilon_j-E_h`. The host spectrum and overlap, not a
new loss constant, decide the result. Root's `HOST_RECEIVER.md` develops
that separate existing-orbital continuation. Merely assigning an
independent recoil energy to a final bound binary's center of mass is
not an additional receiver: its total momentum fixes that common motion.

## 6. Spectator-assisted formation and ionization from existing vertices

The existing field theory also admits charge-conserving channels

    a+a+a -> B+a,       B+a -> a+a+a.                 (14)

The escaping spectator can carry formation energy. For three initially
unbound daughters, energy conservation requires its final excess energy
`epsilon_out=epsilon1+epsilon2+epsilon3-E_B>0`, so there is no two-body
kinematic obstruction. Nonzero amplitudes still require allowed modes and
the actual host overlap. This channel uses a spectator already present in
the scalar stock, not a newly coupled reservoir species.

An illustrative bare-source Born term is

    T_fi^(c3 kR)=<B_A,a_l| V3 (E-H0+i0)^(-1) V4 |a_i a_j a_k>. (15)

The other time ordering `V4 G0 V3` vanishes on these bare `Q=3` states,
because after one association only one daughter remains and the
normal-ordered `V4` cannot act. There are also `V3^3` exchange terms and
all rescattering/dressing corrections. If `B` is a strongly mixed bound
eigenstate, using only (15) is not controlled: the correct amplitude is
the full cluster-channel transition amplitude of the same `Q=3`
Hamiltonian, with the bound channel (12) and consistent regulator. It
introduces no new microscopic vertex, but has not been evaluated merely
by writing (15).

Given the actual channel states, the differential rate is fixed:

    dW_i->f=(2pi/hbar)|T_fi(E_i)|² delta(E_f-E_i) dmu_f. (16)

Average this over the incoming distribution, multiply the bosonic
occupation factors and unordered incident counting, and the volume-
normalized capture and ionization kernels follow. This is a derivation
of what must be computed, not a numerical value for a missing bath.
The reverse uses the same Hamiltonian and time-reversed joint states;
for an isotropic time-reversal-invariant equilibrium host/bath it gives
the usual detailed balance. A coherent finite stock or a driven rotating
host must be treated in its own state rather than assigned this ensemble.

For true ionization out of `B`, specify what counts as released. If one
daughter remaining bound and two escaping are allowed, the final `Q=3`
continuum starts at `epsilon0`; the incoming spectator must supply at
least `epsilon0-E_B`. If two daughters may remain in lower host bound
levels while the third escapes, that final continuum starts at the
lowest *actual two-daughter bound* energy, which can be much lower than
`epsilon0`. Such a process can destroy the bare-X identity without
releasing both charges from the host. If `B` itself is the lowest coupled
Q=2 bound state, it cannot be ionized into a lower Q=2 state; excitation
or dissociation thresholds must then be calculated relative to its actual
allowed residual cluster, not guessed from `d_A` or `Delta_h`.

Thus an incoming bath with energy support below a correctly calculated
ionization gap has zero rate for that particular ionizing channel, while
formation can be kinematically allowed. This gives a possible stable
occupied object. The assumptions that its kernel is nonzero, its bath
has that compact support, and all other channels are absent are not
established by the supplied halo equations. A thermal tail, host
excitation, or other allowed collision changes the retention problem.

## 7. Finite-bath writing and retention tests, with counting stated

For a *mobile bound-object density*, let the dilute, externally fixed
free density be `n`, and define `L3,Kion` by the actual rate convention

    dn_B/dt=L3 n³-Kion n n_B.                       (17)

Here `L3` has units `volume²/time`, `Kion` has units `volume/time`.
Formation consumes two net unbound charges and ionization restores two.
Holding `n` fixed is a large-reservoir approximation; in a closed stock
its evolution and the host density must be included. Equation (17) is
not the finite memory count `(1,4,2)`.

With `n_B(0)=0` and `Kion>0`,

    n_B(t)=L3 n²/Kion [1-exp(-Kion n t)].             (18)

A desired stored charge fraction `0<f<=1` relative to the reference free
density requires `n_B(t_w)>=f n/2`. Retaining an individual bound object
with probability at least `0<R<1` for time `T` requires

    (2L3 n/(f Kion))[1-exp(-Kion n t_w)]>=1,
    Kion n T<=-ln R.                                (19)

Because destruction only reduces writing, a necessary feasibility bound is

    n >=sqrt[f/(2L3 t_w)],
    n <=-ln R/(Kion T),
    f Kion² T² <=2L3 t_w (-ln R)².                  (20)

For `Kion=0`, (18) is replaced by `n_B=L3n³t`, and individual survival
has no loss through this channel. This does not prove that a fixed empty
memory state survives, or that the finite reservoir can be ignored.
No `L3`, `Kion`, `n`, target time or retention probability is fitted here.
Their complete kernels and physical state remain the named inputs.

For a *localized one-place host level*, probabilities have different
units and counting. If spectator formation and ionization are the only
two Markov channels, define per-site kernels `k3,kion` by

    dp/dt=a(1-p)-b p,
    a=k3 n³, b=kion n,
    lambda=a+b, p_eq=a/lambda.                      (21)

Then `k3` has units `volume³/time`, and the exact solution is

    p(t|p0)=p_eq+(p0-p_eq)exp(-lambda t),
    p(t|1)-p(t|0)=exp(-lambda t).                   (22)

The last expression is memory of the preparation. Let `0<q<1` and `0<r<1`.
Small `b` alone gives
long occupied survival but does not give long empty-versus-full memory
when capture `a` remains on. A write from empty with success at least
`q` is possible only for `q<p_eq`, and requires

    lambda t_w >=-ln(1-q/p_eq).                     (23)

Retaining contrast at least `r` over time `T` requires
`lambda T<=-ln r`. Together,

    T/t_w <=[-ln r]/[-ln(1-q/p_eq)]
           <=[-ln r]/[-ln(1-q)].                    (24)

This exact bound holds for a constant two-state rate generator, whatever
existing microscopic channel supplied `a,b`. It is not a universal
write/erase theorem. A changed host/bath during writing, extra occupations,
cooperative barriers, coherent readout, or a different observable requires
the corresponding actual equations. Those are precisely the features that
must be derived before replacing (21) by the earlier finite latch.

If this one-level system is actually in a dilute equilibrium bath, its
statistical ratio is `p/(1-p)=g_B exp[-(E_B-2mu_NR)/theta]`. For an
asymptotically Maxwell-Boltzmann free gas with one internal state,
`n=exp(mu_NR/theta)/lambda_T³`,
`lambda_T=sqrt(2pi hbar²/(m theta))`. Thus detailed balance would give

    k3/kion=g_B lambda_T^6 exp(-E_B/theta).           (25)

The host-bound level degeneracy `g_B`, thermal trace, continuum wave
distortion and rate-kernel definitions must be included consistently.
This formula cannot be transferred to mobile clusters, which have an
additional translational partition factor, or to a collisionless bath
without a thermal ensemble. It is a conditional normalization check,
not an independently fitted capture-to-release ratio.

## 8. Decision, overlap, and exact remaining obligations

| Obligation | Result |
|---|---|
| Original fields identify source and daughter states | Proved from the actual charge and mode expansion |
| Their cubic transition vertex is parameter-free once modes are specified | Proved, with boson factors and continuum hypotheses |
| Original source vacuum lifetime supplies macroscopic memory | Fails for the stated open source; bound object is a different state |
| Closing two-free release closes every host release channel | Refuted by the lower bound-plus-free threshold |
| A subcontinuum state can be loaded directly from its pair continuum without a receiver | Refuted for a static isolated host by energy conservation |
| Existing spectator vertices can supply a formation/ionization channel | Allowed with the displayed amplitude and energy ledger; nonzero evaluated kernel remains conditional |
| Long occupied survival establishes persistent preparation memory | Refuted for the fixed two-state rate model by (22)-(24) |
| Source/daughter or bound/unbound labels equal canonical free/tether labels | Not supplied by the inspected equations |
| Physical capture/release numbers and halo memory lifetime | Not derived without host, bath, receiver and occupation data |

Nearest prior: the source packet already supplied vacuum width, a finite
resonant-band unitary production calculation, and scalar host-dependent
energy signs. The occupied-landscape packet already stressed that internal
two-well equilibration is conditional on a captured particle. This note
adds the explicit spectral identification, same-vertex capture/release
normalization, mixed-channel threshold, spectator write/retention tests
and the preparation-contrast discriminator. No claim is made that the
general Golden Rule, recombination mechanism or two-state kinetics is new.

No new scientific simulation, fit, parameter search or symbolic run was
needed. All deductions above are elementary algebra, operator projection,
channel energy accounting and explicitly stated continuum/Markov limits.
This is author analytic self-review; a separate audit is needed before a
broader physical closure claim. The cheapest next physical input is one
actual host/bath and one field-to-occupation map, with its complete
transition channels. A guessed density, dephasing frequency or lifetime
would supply the missing input rather than derive it.
