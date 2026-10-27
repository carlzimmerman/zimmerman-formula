# A counted cooperative latch and its mechanical price

20 October 2026. Assessment base: `8c450e4d106cc70b458d10ff4826d06fb7925dd3`.
Bounded analytic attempt; no numerical scientific run, existing experiment,
frozen criterion, job, or Git state was changed. Outputs are confined to
this directory. The result is a declared effective model, not a microscopic
derivation from canonical S2.

**Result.** A cooperative finite-state binding latch is possible with finite,
positive transition rates and a complete energy/entropy ledger. The smallest
count-exact example below has three occupancy states and an exact mean
switching time. The canonical conversion field energy raises its required
cooperativity. A related continuous occupancy model has an exact, unique
spinodal threshold after this field energy is included. These constructions
do not preserve the baryon-only cold rest profile of an actual tethered/free
mixture. A separate internal latch can preserve that profile when it changes
only kinetic coefficients; that counterexample supplies no ordinary-gravity
free population and therefore does not close O4.

## 1. Target contract and closest prior

The target is a physical internal state that can keep a memory of capture,
with closed positive inventories, bounded internal energy, reciprocal source
work, and the actual canonical mechanical response varied. Exact permanent
absorption is not the target. Long residence is distinguished from multiple
stationary Gibbs distributions. Material sites are a fixed historical stock,
not the instantaneous phantom target.

The closest inspected prior results are:

| Prior source | Already established | Additional implication here |
|---|---|---|
| `capture_dynamics/RESULT.md`, Section 3 | Closed independent sites, reversible reaction, unique equilibrium, falling-capacity domain obstruction | Cooperative interaction plus actual field conversion cost; exact finite-state barrier and switch time |
| CFG49 `README.md:23-24` | Latching double-well chi is explicitly OPEN; action and couplings are postulated | A chosen double well alone is not counted as progress; derive finite occupancy weights and their coupling cost |
| CFG349 `README.md:16-30` | Ordinary multiplier ratchet has unbounded multiplier energy; doubled-field version omits backreaction | No multiplier; bounded three-state energy and explicit heat/source ledger |
| CFG350 `README.md:67-85` | A state-function switch admits an ordinary action; cooling erases its proposed thermodynamic record | An independent material occupancy state, with its own finite barrier, is required; its energy is counted |
| `occupied_landscape/LANDSCAPE.md:45-54,301-378` | Collective many-particle double well remains separate; actual two-orbital trace and interaction-dependent loading window are already present | This latch is a different added effective interaction; no claim it follows from that scalar/contact model |
| `micro_response/DERIVATION.md:279-291` | Attractive residual quartic already gives a first-order density phase and spinodal | Finite binding inventory, full canonical conversion cost, and its mechanical variation are different objects |
| `reciprocity/SOURCE_RESPONSE.md`, Sections 1-3 | Full remainder energy; free mass changes cold rest; smooth elimination preserves reciprocity | Add the conversion coordinate to this same energy, rather than use a binding-only free energy |

Paths in this table are expanded in `source_hashes.json`. This is a bounded
local comparison, not a claim of literature novelty or a complete repository
search. O1 requires actual species variations and work; O4 requires a derived
transition and one common candidate's predictions. Neither obligation is
completed by the example.

## 2. The actual canonical conversion cost

Use the reciprocal spherical energy already declared in the source:

    U_can = -G/2 integral [(M_b+T+F)^2-T^2]/r^2 dr
            + integral 4 pi r^2 W_rem(GT/r^2) dr,
    R(u)=4 pi G W_rem'(u)=u^2/(a0-u),    0<=u<a0.

Here T,F are enclosed tethered/free masses. Converting a co-located particle
of mass m from free to tethered leaves T+F and the ordinary gravitational
pair energy unchanged. It increases the critical counterterm and remainder.
The derivative per converted particle is

    mu_can(t) = m integral_r^infinity [u(s)+R(u(s))] ds.

For the declared control of a thin shell at fixed radius r, with t converted
occupation units of mass m and no other tether stock, set

    b(t)^2=G m t/a0,     0<=t<t_sat=a0 r^2/(Gm),
    H(0;r)=0,           H_t=mu_can=m a0 b artanh(b/r).

Fixed baryons and the fixed total cold shell mass are counted in U_can;
their unchanged pair energy cancels only from this conversion difference.
The shell is an instantaneous chemical control at fixed positions, not a
mechanical equilibrium or a halo formation model. For the finite-state
construction below, H(n;r) is the declared diagonal energy of extended
collective occupancy modes, imported from this spherical effective field
functional. It is not automatically the Hamiltonian expectation for one or
two point particles. Their self-pair conventions, charge shape and nonlinear
quantum field expectation would require a new microscopic calculation.
A physical site host has its own positive mass/support, counted once in
the unchanged source energy.

An explicit primitive is

    H(t;r)=2 a0^2/G [ b^3/3 artanh(b/r) + r b^2/6
                     + r^3/6 ln(1-b^2/r^2) ].                 (1)

For t>0,

    H_tt=Gm^2/(2b) [artanh(b/r)+br/(r^2-b^2)] > Gm^2/r,
    H_tt(0)=Gm^2/r.

The integral representation independently gives

    H_tt = Gm^2 integral_r^infinity [1+R'(Gmt/s^2)]/s^2 ds,
    R'(u)=a0^2/(a0-u)^2-1,
    R''(u)=2a0^2/(a0-u)^3,   R'''(u)=6a0^2/(a0-u)^4.

Thus H is strictly convex. H_tt is increasing and strictly convex in t;
H_tt tends to infinity at t_sat. This term cannot be dropped from a passive
binding equilibrium. Its derivative, unlike the total Newtonian potential,
does not contain an additional baryon attraction for a co-located label
conversion at fixed total mass.

## 3. A count-exact three-state latch

Take N=C=2 distinguishable particles/sites. Each site holds at most one
particle. A free particle has one co-located internal free state in this
effective control; no orbital continuum or capture cross section is claimed.
The number of injective binding assignments with n bound particles is

    Omega_n=binomial(C,n) N!/(N-n)!,
    (Omega_0,Omega_1,Omega_2)=(1,4,2).

This fixes the free single-particle reference partition to one and gives
every bound assignment the same internal reference weight. A constant free
reference partition z_f would multiply weights by z_f^(N-n); its effect is
absorbed into B_d as B_d-theta ln z_f. An orbital continuum is extra physical
state information, not part of the reference choice proved here.

Assume t_sat>2 and add the finite effective internal energy

    E_n=H(n;r)-B_d n-J n(n-1)/(2C),    J>0, theta=k_B T_bath>0.

The pair interaction is new input. All three states have finite energy;
adding one fixed constant makes their internal energy nonnegative without
changing any result. Work in the Newtonian internal-energy approximation,
with all gaps small relative to mc_light^2. Their mass-equivalent relativistic
correction and a local covariant action are not derived.

The canonical occupancy weights are exactly

    w_n=Omega_n exp(-E_n/theta).

Choose the explicitly counted coexistence bias

    B_d=H(2)/2-J/4-(theta/2)ln 2.

Then

    (w_0,w_1,w_2)=(1,epsilon,1),
    epsilon=2 sqrt(2) exp[-D/theta],
    D=J/4+H(1)-H(2)/2.

The two endpoints are strict occupancy-probability maxima precisely when

    J > 2H(2)-4H(1)+6 theta ln 2.                         (2)

Convexity gives H(2)-2H(1)>Gm^2/r, so (2) requires, in particular,

    J > 2Gm^2/r + 6 theta ln 2.

The combination 2H(2)-4H(1) is invariant under subtracting any term linear
in n from H, with the corresponding shift of B_d. In particular removing
nH(1) as a one-parcel energy convention leaves the barrier criterion
unchanged. Thus the cooperative penalty is not an uncounted linear
self-energy claim. Positive B_d is possible: choose B_d=H(1)/2 and
J=2H(2)-2H(1)-2theta ln2. Then epsilon=4exp[-H(1)/(2theta)]<1 when
theta<H(1)/(4ln2), and J>0.

This is an exact finite-state bimodality criterion for the declared model,
not a thermodynamic phase transition. Its Gibbs distribution is unique.
The nonempty parameter region proves that the convex canonical conversion
cost does not by itself rule out a cooperative finite latch. It also shows
exactly which extra interaction must pay that cost.

For an explicit positive finite-rate dynamics, allow only neighboring n and
set k_(i,j)=kappa min(1,w_j/w_i), kappa>0. At coexistence with epsilon<1,

    k_01=k_21=kappa epsilon,    k_10=k_12=kappa.

Here kappa is a new attempt rate, distinct from the canonical cosmological
normalization denoted by the same Greek letter in other project files.

The mean time tau_i to first reach 2 from i satisfies

    tau_0=1/(kappa epsilon)+tau_1,
    tau_1=1/(2kappa)+tau_0/2,
    tau_0=(1+2/epsilon)/kappa.                            (3)

The reverse mean time is identical. For epsilon much smaller than one, the
two branches are metastable occupancy modes with a finite lifetime that
can grow exponentially in J/theta. Neither kappa nor J is derived from S2.
This constructive result adds more than a statement that a bath is needed.

For general N,C, the exact finite-state ratio is

    w_(n+1)/w_n = [(N-n)(C-n)/(n+1)]
      exp[(B_d+Jn/C-(H(n+1)-H(n)))/theta].                (4)

Equation (4), rather than a continuous spinodal, is the exact test at small
site count. Distinguishable internal states, integer C,N and the co-located
effective interaction are explicit assumptions; none is obtained by merely
renaming the existing medium's density.

## 4. Exact continuous spinodal threshold with the same cost

For a separate mesoscopic continuous-occupancy model set y=t/C, nu=N/C and
declare

    F(t)=H(t)+C theta L(y)-Bt-Jt^2/(2C),
    L(y)=(nu-y)[ln(nu-y)-1]+y(ln y-1)
          +(1-y)[ln(1-y)-1].

Its domain is 0<t<min(N,C,t_sat), with x ln x continued at zero. This is a
chosen mixing free energy, not an exact finite-integer combinatorial trace.
The reference normalization and omission of the pair self term shift B:
with the Stirling continuous approximation to Section 3,
B=B_d-J/(2C)+theta ln C. No finite-C equivalence is asserted.

Direct differentiation gives

    F_t=mu_can+theta ln[y/((nu-y)(1-y))]-B-Jy,
    F_tt=[K(y)-J]/C,
    K(y)=theta Q_nu(y)+C H_tt(Cy),
    Q_nu(y)=1/y+1/(nu-y)+1/(1-y).                       (5)

Q_nu is strictly convex: Q_nu'' is twice the sum of the three positive
inverse cubes. Section 2 proves convexity of H_tt. Therefore K is strictly
convex and diverges at both ends of the physical interval; if saturation is
the first upper boundary, H_tt supplies that divergence. It has exactly one
minimum and

    Jcrit=min K(y).                                     (6)

If J<=Jcrit, F_t is strictly increasing (at equality its derivative vanishes
only at one point), so exactly one equilibrium exists for every finite B.
If J>Jcrit, K(y)=J has exactly two roots y_-<y_+. Define

    h(y)=mu_can(Cy)+theta ln[y/((nu-y)(1-y))]-Jy,
    B_low=h(y_+),    B_high=h(y_-).

Then B_low<B_high. For B strictly between them, there are exactly three
stationary occupancies: two strict local minima separated by one local
maximum. At each endpoint one minimum and the maximum merge. Outside the
closed interval there is one minimum. This proof uses h' = K-J and its
endpoint limits, not a finite scan.

Without H, at nu=1 the unique curvature minimum is y=sqrt(2)-1 and
min Q_1=3+2sqrt(2). With the actual canonical field cost,

    Jcrit > (3+2sqrt(2))theta + C Gm^2/r      (N=C).      (7)

The exact threshold remains (6); (7) is a strict necessary lower bound,
not a sufficient criterion. The temperature term exceeds 4theta, the minimum
of 1/y+1/(1-y), because both free stock and vacant sites deplete. The
continuous result is distinct from the exact small-C
criterion (2).

## 5. Actual energy, entropy and source variations

For the discrete model let p_n be occupancy probabilities. Use

    U=sum_n p_n E_n,
    S=-k_B sum_n p_n ln(p_n/Omega_n),
    F=U-T_bath S.

For each oriented neighbor edge i<j, define the net flux
I_ij=p_i k_ij-p_j k_ji. The rates above obey
k_ij/k_ji=w_j/w_i. At fixed source parameters,

    dot E_bath=-sum_(i<j) (E_j-E_i) I_ij,
    dot U+dot E_bath=0,
    dot S_total=k_B sum_(i<j) I_ij
             ln[p_i k_ij/(p_j k_ji)] >=0.                (8)

The entropy statement follows edge by edge from (a-b)ln(a/b)>=0. It counts
the field energy H, the cooperative binding energy and multiplicities. The
canonical fixed-temperature trace is an ideal-reservoir contract; a finite
receiver's temperature must also evolve. A physical receiver, its capacity
and heat-exchange rate are additional inputs.

For a host/field coordinate q, with fixed material inventories, the actual
generalized source force in state n is

    -partial_q E_n=-H_q(n)+n partial_q B_d
                         +n(n-1)/(2C) partial_q J.       (9)

The source supplies work partial_q E_n dot q and loses that same energy.
Adding (9) is mandatory when a binding bias is prescribed from a baryonic
or tidal environment. Tuning B_d(r) to enforce coexistence for all r is such
a coupling. For constant J,theta it has B_d'(r)=H_r(2)/2, and at n=2 its
new binding force 2B_d' cancels the original H_r(2) force. A coexistence
calibration across hosts therefore changes their mechanical interaction.
Choosing B_d once at a fixed host is different and supplies no universal
host-selection law.

In the continuous model, let q be an actual canonical mechanical coordinate,
keep N,C,theta and the occupation reference fixed, and write
F_total=U_can(q,t)+Ctheta L(y)-B(q)t-J(q)t^2/(2C).
Vary q before eliminating t. The force added to the canonical force at the
given occupancy is

    t B_q + t^2 J_q/(2C).                               (10)

If two distinct positive occupancies t_1,t_2 are each to retain their own
canonical force at the same q without any added binding force or further
counterterm, both expressions in (10) must vanish. Their difference proves
B_q=J_q=0 there. Across a coordinate interval, B and J must be constant on
that interval. This is a
restriction for the declared linear/quadratic interaction; it is not a
universal theorem about every internal energy. A zero-occupancy endpoint
removes one of the two equations, and an additional chosen counterterm is
another interaction which must itself be varied.

On a smooth stable branch, local elimination yields the exact Schur formula

    (F_eff)_qq = (F_total)_qq
                       -[(F_total)_qt]^2/(F_total)_tt.   (11)

The branch relaxes the mechanical stiffness. A nonzero mixed coupling makes
this correction singular as a spinodal is approached. Branch switching or
fixed-history evolution cannot be replaced by smooth elimination there.
Equation (11) is conditional on a smooth branch and positive occupancy
curvature; it is not a theorem of full dynamical stability.

Even with B,J independent of q, converting actual free to tethered mass
changes T,F in U_can. In particular the source note's occupied cold rest is
R(GT/r^2)=G(M_b+F)/r^2. Thus an actual free mass stock changes the relaxed
profile. The H in Sections 2-4 is precisely the chemical consequence of
using this actual mechanical energy; cooperativity does not erase it.

## 6. A kinetic-only counterexample, with a different physical meaning

To delimit the obstruction, attach the three-state latch to a carrier whose
entire density continues to have canonical mechanics in every latch state.
Let z be this internal state and e_z its fixed energies, independent of the
canonical coordinate q. It counts internal bonds rather than tethered/free
mass. Take a positive carrier inertia M and finite friction gamma_z>0.
At positive temperature, include the matching thermal noise, rather than
use noiseless damping as a purported exact equilibrium bath:

    dq=(p/M)dt,
    dp=[-partial_q U_can(q)-gamma_z p/M]dt
                                     +sqrt(2gamma_z theta)dW.

Let z follow the counted reversible chain of Section 3 with independent
fixed state energies e_z. On a regular confining mechanical domain, the
exact stationary density is

    pi_z(q,p) proportional to Omega_z
            exp[-(p^2/(2M)+U_can(q)+e_z)/theta].

Its mechanical marginal and static potential are independent of gamma_z.
For a smooth probability density P_z with zero boundary flux, put
A_z=p/M+theta partial_p ln P_z. Integration by parts gives the mechanical
contribution to the derivative of the relative free energy
theta sum_z integral P_z ln(P_z/pi_z) as

    -sum_z gamma_z integral P_z A_z^2 dq dp <=0.

The jump contribution is -theta sum_(i<j) integral I_ij
ln[P_i k_ij/(P_j k_ji)] dq dp. Hamiltonian transport contributes zero.
The receiver's Stratonovich heat increment is
[gamma_z(p/M)dt-sqrt(2gamma_ztheta)dW] circle (p/M), minus the change of e_z
at each internal jump. This is exactly the negative carrier/latch energy increment;
recoil belongs in the receiver if momentum is tracked. The entropy
production is the relative-free-energy dissipation divided by T_bath.

Both long-lived internal branches have the identical mechanical potential
and drift rest equation partial_q U_can=0. Different gamma changes the
relaxation clock; it introduces no static source term. Positive-temperature
mechanical fluctuations are present, so this example is not a claim of an
exactly cold occupied state at finite T. It is a counted effective
counterexample to the overbroad assertion that any physical memory must
change the canonical static potential. It is not an S4 completion: no
latch state becomes an ordinary-gravity-only free population. The bath,
gamma and internal transition operator still need a microscopic realization.

## 7. Exact result, nonclaim, and next decision

| Obligation | Verdict |
|---|---|
| Full canonical energy appears in actual conversion affinity | Passed analytically in the declared fixed-position shell control |
| Cooperative finite latch with bounded energies and finite switch time exists | Passed by the exact three-state construction, (2)-(3) |
| Continuous model has a unique sharp curvature threshold | Passed for the declared free energy and domain, (5)-(7) |
| Energy, entropy and source work are counted | Passed within the Newtonian effective/isothermal contract, (8)-(10) |
| Two internally distinct branches can preserve a canonical rest law | Passed for the kinetic-only counterexample, with the stated different dictionary |
| Actual tethered/free partition retains baryon-only cold rest | Failed for the inherited reciprocal mechanical energy when F>0 |
| J, sites, capture kernel, bath and lifetimes come from canonical S2 | Not established; these are additional effective inputs |
| Retention survives a falling current phantom target | Not addressed; material C is deliberately independent of that target |
| One candidate satisfies galaxy/dwarf/merger/cluster data | Not addressed; no prior empirical pass is transferred |

The useful decision is now concrete. If memory means an internal slow
relaxation clock, a kinetically coupled latch is compatible with canonical
rest, and the next physical target is a derived gamma(z) and transition
operator. If memory means a true free/tethered conversion, retain H and the
changed shared-gravity rest equation, specify the source of J and material
site inventory, and test whether that same candidate reaches the required
finite release time. Choosing a double-well shape or tuning B to a desired
retained fraction does not make that physical join.

## Provenance and review

All mathematical results here are explicit analytic derivations. No external
theorem, numerical fit, stochastic simulation, symbolic package or finite
sampling is load bearing. The two backward-time equations independently
check the exact switching mean; differentiating (1) checks H_t; the integral
for H_tt establishes its strict inequalities and higher derivative signs.
This is author self-review, not an independent audit or a formal certificate.
The final proofreading scope is this new note only; no old packet was edited.
`source_hashes.json` pins exact read inputs and their base comparison. Several
provided working-tree prior notes are absent from the assessment commit;
their exact byte hashes authenticate those dependencies. The observed HEAD
changed externally during the task; this lane made no Git mutation.
