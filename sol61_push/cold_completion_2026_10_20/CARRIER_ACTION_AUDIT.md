# Carrier-action audit: protected production and ARGON binding are different theories

20 October 2026. Independent focused algebra audit for the current completion packet. Task base HEAD: `dce2a2e3d`; exact working-source hashes and current revisions are recorded in `sources_carrier.json`. In particular, the master equation document is dirty working material, not identical to its committed version. No live experiment, frozen criterion, publication or shared CURRENT pointer was changed.

**Normalized claim and verdict.** Claim: the original positive-square charged carrier action also supplies ARGON's below-free-particle stationary fragments and their measured merger gap by a change of notation. **Refuted.** The classical energy/charge bound, charged field content and fixed-frequency potentials differ. ARGON's attractive neutral-mediator sector is an additional physical model. This does not refute cold matter, gravitational binding, extraction of pre-existing excess energy, or the separately specified alternative common action below.

## 1. Original protected carrier: exact action, charge and energy

Use signature (+---), natural units and two complex fields with U(1) charges 1 and 2:

    L_p = |partial Phi|^2 + |partial X|^2 - V_p,
    V_p = m^2 |Phi|^2 + 4m^2 |X|^2
          + |sqrt(Delta) X + (g/sqrt(Delta)) Phi^2|^2
          + lambda_rep |Phi|^4,
    Delta > 0, m > 0, lambda_rep >= 0,
    M_X^2 = 4m^2 + Delta,
    lambda_tot = g^2/Delta + lambda_rep.

`CHARGED_ACTION.md` has lambda_rep=0; the current master inventory adds a positive repulsive remainder. Both obey the following argument. The equations are

    (Box + m^2) Phi + 2g X Phi* + 2 lambda_tot |Phi|^2 Phi = 0,
    (Box + M_X^2) X + g Phi^2 = 0.

The original document's positive-charge convention is

    Q_p = integral [ i(Phi* Phi_t - Phi_t* Phi)
                    + 2i(X* X_t - X_t* X) ] d^3x.

Thus Phi proportional to exp(-i omega t) has positive charge when omega>0. Let E_p be the ordinary material Hamiltonian, excluding any constant vacuum term. Direct square completion gives

    E_p - m Q_p = integral [ |Phi_t + im Phi|^2
                         + |X_t + 2im X|^2
                         + |grad Phi|^2 + |grad X|^2
                         + |sqrt(Delta)X + g Phi^2/sqrt(Delta)|^2
                         + lambda_rep |Phi|^4 ] d^3x >= 0.

Opposite time-derivative signs give E_p + m Q_p >= 0, hence E_p >= m|Q_p|. For smooth isolated Minkowski evolution with decaying fields, or in a fixed periodic box, both E_p and Q_p are conserved. No expansion, gravity, quantum renormalization or external work is included in this statement.

If Q_p>0 and the initial excess is D_p=E_p-mQ_p, then every final contribution to this positive functional is bounded by D_p. One cannot extract most of the protected charged rest energy while retaining its charge and claim that the original inequality remains intact. A source X=A exp(-i M_X t) has

    E_p/V = 2 M_X^2 |A|^2,
    Q_p/V = 4 M_X |A|^2,
    D_p/E_p = 1 - 2m/M_X = 1 - 1/sqrt(1+u_*^2).

For u_*=0.001 this is approximately 5e-7; for the separate u_*=0.02 benchmark it is approximately 1.9994e-4. Seeds and every other prepared excitation must be included in the actual initial E and Q. These distinct benchmark budgets must not be interchanged.

**Restriction:** E>=m|Q| alone does not imply E(Q) is additive, nor forbid positive merger release between excited configurations above that floor. It also does not bound the complete system after adding negative gravitational potential energy or another interacting sector. Such a sector needs its own conserved total ledger. The obstruction concerns importing ARGON's below-mass branch into this protected, nongravitating action.

## 2. A stronger stationary obstruction under stated localization hypotheses

For synchronized stationary fields

    Phi = exp(-i omega t) f(x),
    X   = exp(-2i omega t) b(x),

the fixed-frequency functional is

    F_omega = E_p - omega Q_p
            = T_grad + integral V_omega d^3x,
    T_grad = integral (|grad f|^2 + |grad b|^2) d^3x,
    V_omega = (m^2-omega^2)(|f|^2+4|b|^2)
              + |sqrt(Delta)b + g f^2/sqrt(Delta)|^2
              + lambda_rep |f|^4.

For |omega|<=m, V_omega>=0 pointwise. Any sufficiently regular, finite-energy localized stationary critical point permits the spatial scaling f(x)->f(x/lambda), b(x)->b(x/lambda), yielding

    T_grad + 3 integral V_omega d^3x = 0.

Both terms are nonnegative. Decay at infinity then forces f=b=0. This rules out nontrivial ordinary isolated synchronized subthreshold Q-balls for this action, including spatial phases whose gradients remain in T_grad. It is not a claim about arbitrary time-dependent breathers, external traps, gravitating stars or every possible above-threshold/embedded configuration. A nonzero daughter with the usual vacuum exponential tail requires |omega|<m, precisely the range ruled out here.

The finite periodic box is an important exception to the spatial-scaling/localization argument. With lambda_rep=0, homogeneous fields f=constant, b=-g f^2/Delta and the rest rotations above can saturate E=mQ. They are not localized isolated fragments. The audit does not exclude that condensate.

An independent coefficient check reaches the same sign. Minimizing the *static* potential over X gives

    X_min = -g Phi^2/M_X^2,
    V_eff,static = m^2 I + [lambda_rep
                     + 4m^2 g^2/(Delta M_X^2)] I^2, I=|Phi|^2.

The quartic is nonnegative. At fixed frequency, local minimization of V_omega over b instead gives

    V_eff,omega = (m^2-omega^2) I
       + [lambda_rep + 4g^2(m^2-omega^2)
                           /(Delta(M_X^2-4omega^2))] I^2.

It is nonnegative for |omega|<=m. This last local expression ignores b's gradient and is a lower bound on the corresponding gradient-inclusive functional, not a dynamical integration of a near-threshold source.

## 3. ARGON's actual neutral-mediator action changes this inequality

ARGON11 `frag3d.c` at `07546091c3` uses one complex charged field Psi and one **real neutral** field chi, in m_h=1 units:

    L_A = |partial Psi|^2 + (partial chi)^2/2 - V_A,
    V_A = I + Lq I^2 + a chi I + U(chi), I=|Psi|^2,
    U(chi) = M^2 chi^2/2 - M chi^3/8 + chi^4/4,
    M=100, Lq=1.99, a=200.

This (+---) notation reproduces the source's equations and positive Hamiltonian; its source comment uses the opposite metric convention. Explicitly,

    Psi_tt = lap Psi - (1 + 2Lq I + a chi) Psi,
    chi_tt = lap chi - M^2 chi + 3M chi^2/8 - chi^3 - a I,
    E_A = integral [ |Psi_t|^2 + |grad Psi|^2
                      + (chi_t^2+|grad chi|^2)/2 + V_A ] d^3x,
    Q_A = integral 2 Im(Psi* Psi_t) d^3x.

Q_A has the opposite sign orientation to Q_p under a direct daughter-field identification. A sign flip cannot change a bound on |Q|. Original field content is four real degrees of freedom with a charged source; ARGON has three real degrees of freedom with a neutral mediator. Identifying X with chi is not an invertible symmetry-preserving field redefinition.

For small I, eliminating the neutral mediator locally gives

    chi = -a I/M^2 + O(I^2),
    V_A,eff = I + [Lq-a^2/(2M^2)] I^2
                + a^3 I^3/(8M^5) + O(I^4)
            = I - I^2/M + I^3/M^2 + O(I^4).

The **negative quartic** is the missing attraction. This small-amplitude expansion diagnoses the sign; it is not a quantitative approximation for the dense solved profiles.

There is also an exact, elementary counterexample to transferring the original unit-mass floor. At I=1 and chi=-0.02,

    V_A = 0.99010004 < I.

In a periodic homogeneous initial state with Psi=1, Psi_t=i, chi=-0.02 and chi_t=0, the source conventions give Q_A/V=2 and E_A/V=1.99010004<2. These are admissible smooth initial data; they need not be stationary to refute a universal Hamiltonian inequality. The protected model cannot produce this violation by merely renaming fields.

The new isolated ARGON profile calculation separately finds candidate E/Q=0.9519747920 and 0.9333633691 at Q=80000 and 160000. Its stationary branch increment is 2977.827663, or 1.955033% of the initial pair energy. That finite numerical result is evidence *in the ARGON action*. It proves neither stability nor the escaped channel, and does not apply to the original protected carrier.

## 4. Explicit alternative common matter action: a consistent candidate, not an equivalence

The root's `common_action.py` specifies a new action with both a charge-2 source and neutral mediator. This audit independently checks its exact classical floor; it does not rerun or adopt the root's stationary computation.

    L_C = |partial Psi|^2 + |partial X|^2 + (partial chi)^2/2 - V_C,
    V_C = m^2 I + M_X^2 |X|^2 + g(X* Psi^2 + X Psi*^2)
            + lambda I^2 + a chi I + U(chi),
    m=1, M_X^2=4.0016, g=0.002168,
    lambda=1.99+g^2/M_X^2, M=100, a=200.

The same charge-1/charge-2 U(1) is preserved; chi is neutral. With the ARGON charge orientation,

    Q_C = integral [2 Im(Psi* Psi_t)+4 Im(X* X_t)] d^3x.

The exact field equations are

    (Box+m^2)Psi + 2g X Psi* + 2lambda I Psi + a chi Psi = 0,
    (Box+M_X^2)X + g Psi^2 = 0,
    Box chi + M^2 chi - 3M chi^2/8 + chi^3 + a I = 0.

At g=0, with lambda following the stated parameter relation and X initially zero, ARGON is a consistent subsystem plus a decoupled free X. At chi=0 the **potential restricted algebraically** is a member of the protected family because lambda-g^2/(M_X^2-4)>0. However, chi=0 is **not a consistent truncation** for a nonzero daughter: its equation contains a|Psi|^2. Removing the mediator requires a=0/decoupling or a separately justified approximation, not holding chi at zero against its equation.

Furthermore lambda_rep in that protected restriction is approximately 1.9870635, unlike the historical revised scattering benchmark's approximately 0.00587528. Therefore old elastic cross sections, pressure bounds, saturation and yield do not transfer. The narrow linear production band may be rederived about a chosen source background, but its nonlinear fate requires this extended action. Parameters are exploratory choices, not derived from the cold-energy normalization or observations.

### An independent exact lower floor for this changed action

Set mu=17/20, alpha=m^2-mu^2=111/400, A=M_X^2-4mu^2=2779/2500>0 and

    ell = lambda-g^2/A = 13831033985551/6950279000000 > 0.

Completing the X square gives

    V_C-mu^2(I+4|X|^2)
      = A |X+g Psi^2/A|^2 + ell I^2 +(alpha+a chi)I + U(chi).

U(chi)>=0 because

    U(chi)=chi^2[(chi-M/4)^2/4+31M^2/64].

For chi>=-alpha/a, every remaining term is nonnegative. For chi=-t<-alpha/a, minimizing the quadratic over I>=0 reduces positivity to

    F(t) = 4ell U(-t) - (alpha-a t)^2 >= 0,
    t >= t0=111/80000,
    F(t) = ell t^4 + 50ell t^3 + (20000ell-40000)t^2
                         + 111t - 12321/160000.

An independent exact-rational SymPy Sturm calculation gives F(t0)=0.07662136695771095...>0, no endpoint zero, and **zero real roots on [t0,infinity)**. Signs of the Sturm sequence at t0 are (+,+,+,-,-), at positive infinity (+,+,+,+,-); both have one sign variation. Hence F remains positive throughout that interval. Exact coefficients and the endpoint rational are preserved in `sources_carrier.json`; this is a polynomial certificate, not a sample of field amplitudes.

Consequently V_C>=mu^2(I+4|X|^2) for all classical field values. Completing time-derivative squares, including the neutral field's positive kinetic/gradient terms, proves

    E_C - mu Q_C = integral [ |Psi_t-i mu Psi|^2
                         + |X_t-2i mu X|^2
                         + |grad Psi|^2+|grad X|^2
                         + (chi_t^2+|grad chi|^2)/2
                         + V_C-mu^2(I+4|X|^2) ] d^3x >= 0,
    E_C >= 0.85 |Q_C|.

The opposite charge sign follows by conjugation/opposite time-square signs. This is a uniform flat classical bound for finite-energy configurations (or a periodic box), not a renormalized quantum inequality. It deliberately replaces the old E>=|Q| floor with a weaker one, permitting sub-unit E/Q while retaining a positive Hamiltonian floor. It does not prove soliton stability, a low-pressure state, production abundance or a usable merger luminosity. Any new stationary branch and its energy gap must be calculated afresh in these three fields; the old two-field 1.955% is not a certified value for this action.

## 5. Dependency and completion audit

| Obligation | Status | Decisive reason |
|---|---|---|
| Original classical E>=m|Q| | Passed under isolated/periodic flat classical hypotheses | Exact square identity |
| Original localized synchronized subthreshold fragment | Refuted within the stated stationary class | Nonnegative fixed-frequency potential and scaling identity force zero |
| ARGON is a notation change of protected carrier | Refuted | Charged/neutral field mismatch and exact E<Q counterexample |
| ARGON stationary gap | Finite numerical evidence in its own action | Existing box/tolerance/charge/virial/chemical-potential checks; no new run here |
| New common-action E>=0.85|Q| | Passed under the explicit changed coefficients/classical hypotheses | Square completion plus independent exact polynomial certificate |
| New-action stationary gap equals old ARGON gap | Not established; must not be transferred | Different equations and charged source backreaction |
| Merger gap becomes escaping E/Q/vector J | Open | Needs matched pair evolution and mode-resolved flux |
| Production remains cold with the neutral mediator active | Open | Original positive D_p and pressure protection no longer apply |
| Galactic gravity/normalization, finite stock and four dwarf likelihoods | Open | No action/source dictionary or observational selection follows from a microscopic floor |

A minimally covariant matter extension can be written as integral sqrt(-g)[M_Pl^2 R/2 + L_C] plus a baryonic action. It supplies ordinary stress-energy sourcing if adopted; it does not derive the separate polarization/RAR sector, kappa, cosmological charge origin or source abundance. Adding that sector requires one reciprocal interaction/stress ledger and an explicit account of whether its inferred gravity already counts this material mass. The master inventory itself identifies this S_bridge as open.

**Strongest safe conclusion:** an explicit changed matter action can retain a classical positive energy/charge floor while allowing an ARGON-like attractive phase. The original protected action does not already contain that phase. A phase-transition interpretation must derive its extra mediator/order parameter, coefficients, matching and charge/energy bookkeeping; a historical mobility gate cannot supply them.

**Cheapest next discriminating checks:** test the complete new fixed-charge profiles and linear/nonradial stability; rederive production/scattering in this same action; then measure phase/impact-averaged matched pair E,Q,linear momentum and vector-J flux. No abundance, galactic normalization or dwarf fit may be inferred before the source/unit/action bridge and stellar-selection/stock constraints are supplied.

Review provenance: independent sibling derivation of the energy identities, counterexample, stationary restriction, mediator sign and proposed polynomial floor; source stationary computations were read, not rerun. No external theorem or paper is load-bearing: the scale variation and polynomial-root certificate are displayed explicitly. Global smooth existence, quantization and every uncomputed transport/empirical implication remain outside this audit.
