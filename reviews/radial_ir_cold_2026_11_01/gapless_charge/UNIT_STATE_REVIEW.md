# Independent unit and conditional FD-state audit

1 November 2026. This is a new review addendum; no earlier frozen contract,
code, result, verification record or ARTIFACTS.sha256 is changed. The prior
gapless/charge inventory remains frozen. This review independently derives
the formulas below and inspects the author's code/results; it does not rerun
the scientific scripts or introduce a test grid. Both v2 manifests validate,
and their current input/output hashes independently match the recorded hashes.

## Scoped verdict

For the explicit unpolarized, decoupled, two-spin Majorana distribution with
m_chi=1MeV and e=.003, the density normalization, Pauli condition, small
velocity and sub-kpc free-streaming travel benchmark pass in the specified
Einstein expansion history. The supplied Goldstino width is a partial width:
it establishes a necessary survival condition, not a total-lifetime bound.
The separate cold-state decay audit must supply the remaining implication.

Subsequent bounded work in decay_bound/ now bounds the leading hard one-loop
two-vector class, in addition to the Ward channel: its inclusive loss is at
most1.070% of that partial width. Their retained-channel survival is at
least.996224 for this benchmark. This closes the leading hard coefficient
budget at that order; higher-loop and higher-body soft/Ward losses remain
outside that bound. It is still not an all-orders total-lifetime theorem.

The state is a stipulated initial distribution, not a derived production or
freezeout history. Its use also requires an independent vacuum normalization:
it does not survive the alternative requirement that raw V0 equal the stated
dark-energy budget. A zero-charge photino gas and a rotating phase are distinct
states of the same microscopic action.

## Units and vacuum normalization

Since f has dimension mass², restore mu=sqrt(f): m=mu mhat,
Gamma=mu Gammahat and rho=mu⁴ rhohat. Thus tau_s=hbar_GeV_s/(mu Gammahat).
For a density quoted in GeV/cm³, rho_GeV4=rho_GeV_per_cm3(hbar c)_GeV_cm³.
The unit script's conversions are dimensionally correct. Its reduced Planck
energy is sqrt(hbar_SI c⁵/(8pi G)), converted from joules to GeV; H0_GeV is
hbar_GeV_s H0_s. The resulting rho_DE=.685×3Mbar²H0²=2.51927e−47GeV⁴ and
mu_DE=(31rho_DE)^(1/4)=5.28639e−12GeV agree with these definitions.

The radial normalization sigma=sqrt(2)delta R, pi=sqrt(2)v theta gives
L_int=sigma(partial pi)²/(sqrt(2)v), hence the identical phase-pair width
Gamma_aa=m³/(64pi v²). For delta R=alpha v cos(mt), harmonic energy is
rho=m²v²alpha²; no factor2 is missing. With mhat proportional to e^(3/2)
and vhat proportional to e^(−1/2), the density floor scales e^(−1/2), while
the width-limited upper mu scales e^(−11/2). Passing this interval is only
the stated necessary test, as UNIT_CONDITIONS.md says.

For the photino, the independently computed finite one-loop coefficient is
c_chi=1.1164161506e−4, so m_chi=c_chi mu e^(5/2). The selected point gives

    mu=1.8170662e7GeV, v=2.4440454e9GeV,
    F_eff²=mu⁴/31,
    Gamma_chi->gamma G=m_chi⁵/(16pi F_eff²)=5.65730e−45GeV,
    tau_partial=1.1634747e20s.

Replacing F_eff² by the net gravitational vacuum energy after an independent
offset would be incorrect. The auxiliary order parameter remains mu⁴/31.
For this selected point raw V0/rho_DE=1.39587e74. Conversely, tying raw V0
to rho_DE fixes mu=mu_DE and does not give a1MeV photino at e=.003. The
free-mu particle example and the raw-vacuum identification must not be
presented as a common successful construction. In the rigid theory absolute
gravitating vacuum normalization has not been supplied by a gravitational
completion.

The constants were independently source-checked in
[NIST SP961,CODATA2022](https://physics.nist.gov/cuu/pdf/wall_2022.pdf): the
table gives h,c,GeV conversion and exact k_B=1.380649e−23J/K; G carries
experimental uncertainty. [Planck1807.06209v4](https://arxiv.org/html/1807.06209v4),
dated9August2021, footnote14 sets T_CMB=2.7255K. Its §3.2 supports the rounded
base-LambdaCDM H0/dark-energy benchmark. Omega_c=.265,Omega_m=.315 and
z_eq=3400 are the explicitly chosen comparison inputs, not a new fit or the
project's derived gravitational law.

## FD normalization, Pauli exclusion and moments

Let q=a p, a0=1, and put f_s(q)=1/[exp(q/T_chi0)+1] for each of g=2 spin
states. Then 0<=f_s<=1/2<1, which directly satisfies Pauli exclusion. No
compact-support assumption is needed. The separate halo compact-support
bound in UNIT_CONDITIONS.md is correctly conditional on that support; it
cannot be applied literally to an FD distribution with an infinite tail.

Define I_n=integral_0^infinity dx x^n/(exp x+1). Expanding the denominator
as an alternating exponential series gives

    I_n=(1−2^(−n))Gamma(n+1)zeta(n+1), n>0,
    n_chi0=g T_chi0³ I_2/(2pi²), I_2=3zeta(3)/2,
    T_chi0³=4pi²rho_cold/(3g zeta(3)m_chi),
    <q>=7pi⁴ T_chi0/[180zeta(3)],
    <q²>=15zeta(5)T_chi0²/zeta(3).

These reproduce the author's temperature and velocity integrands. In
Gauss–Laguerre quadrature the weights contain exp(−x); dividing them by
1+exp(−x) therefore produces exactly the desired FD measure. The numerators
x³/sqrt(x²+r²) and x⁴/(x²+r²), r=ma/T_chi0, are respectively the mean speed
and mean squared speed with the x² number measure. No extra degeneracy
factor belongs in either normalized moment.

For the selected state the supplied density is rho_cold=.265rho_crit,
n0=9.7460957e−45GeV³, T_chi0=3.7644775e−15GeV and T_chi0/T_nu0=.0224559.
The nonrelativistic analytic moments give

    v_rms,0=1.3541354e−11,
    v_rms,eq=(1+3400)v_rms,0=4.6054143e−8.

The exact relativistic quadrature agrees. The rest-density approximation
rho=mn has a present kinetic correction below 1e−21 relative and is harmless
for the quoted benchmark. The leading equality equation of state is
w≈v_rms,eq²/3≈7.1e−16. This supports finite coldness of this distribution;
it is not the pressure of the distinct rotating phase.

## Free-streaming travel

For a collisionless distribution present at a_i, the comoving travel is

    lambda_FS=c integral_ai^1 da <v(a)>/[a² H(a)],
    H(a)=H0 sqrt(Omega_r/a⁴+Omega_m/a³+Omega_Lambda).

Setting t=ln a gives the code's integrand <v>/(a E). The distance before
a_min is bounded by a_min c/(H0 sqrt(Omega_r)); the reported added bound
4.62e−10Mpc is negligible here. Integrating from zero also conservatively
overestimates travel if the stipulated relic is produced later; it does not
establish that its EFT or production mechanism exists arbitrarily early.

There is an independent elementary upper bound. Since
<v(a)><=min[1,A/a], A=<q>/m=1.1863278e−11, use the radiation lower bound
on H before a_eq and the matter lower bound after it to obtain

    lambda_FS <= c/H0 {
      A/sqrt(Omega_r)[1+log(a_eq/A)]
      +2A/sqrt(Omega_m)[a_eq^(−1/2)−1] } <.12kpc.

This bound assumes A<a_eq, which is satisfied. It independently passes the
stated1kpc travel benchmark. The author's quadrature gives 103.751 pc, with
64/128-order relative difference2.34e−10 for this mass. Neither an integrated
travel length nor the analytic bound is a Boltzmann transfer function or an
observational structure-formation exclusion/fit.

The optional bath count g_eff=24 gauge polarizations+1 phase+7/8×2 Goldstino
=26.75 is consistent with the assumed massless bath. It gives
Delta N_eff=(4/7)g_eff(T_bath/T_nu)^4. Its small value at the stipulated
temperature is a conditional radiation budget; neither the equal bath/relic
temperature nor its subsequent entropy history is derived here.

## Survival and rolling-current distinction

The displayed exp(−t_age/tau_partial)=.99626394 is the isolated partial-width
survival estimate over 13.8 Gyr. Unknown additional channels can lower total
survival; tau_partial>t_age alone is not a sufficient total-survival test.
Relativistic time dilation is negligible for most of this benchmark's age
but is another reason the displayed rest-width exponential is a scoped
estimate. A total-width claim needs the companion channel audit.

The R-anomaly source is correctly normalized: original R charges give
Tr(q_R T²)=5, theta shifts by2alpha, and the heavy residual-U1 WZ term is
−5g1²theta F Ftilde/(32pi²). Therefore constant rolling theta=omega t gives

    A_ddot,±+[k²±k c_theta omega]A_±=0,
    c_theta=5g1²/(8pi²), gamma_max=|c_theta omega|/2.

The unit script restores the corresponding inverse amplitude growth in
seconds correctly and calls it an amplitude e-fold time. A half-wave patch
size pi hbar c/kmax presumes an admitted half-wave boundary mode; a periodic
box uses2pi instead. A different patch/plasma/coherence/seed changes the
depletion implication. The code uses leading g1²=(29/200)e²; including our
one-loop gauge matching changes these leading growth estimates only at the
next relative loop order (about1.6e−5 at e=.03). Inverse gamma is not a
fractional-charge lifetime.

An unpolarized Majorana gas has no coherent phase rotation; opposite spin/
helicity contributions do not create a macroscopic R-axial charge. Thus the
rolling U(1) helicity instability cannot simply be assigned as this gas's
decay width. Gauge neutrality and zero mean theta-dot also do not prove the
gas is stable: its allowed particle decays/collisions must still be bounded.

## Pinned author inputs for this review

SHA256 values refer to the exact bytes inspected, not a claim about future
edits. Paths below are relative to reviews/radial_ir_cold_2026_11_01/.

| Input | SHA256 |
|---|---|
| UNIT_CONDITIONS.md | e2129cb6fea79c388433810d160737aeed264c1f954f41f631e5f0995d61ae4e |
| unit_conditions.py | 7b62dbb7bfd9e361e68cac781513b455bc53a8058b762d7f593ba3b760fb8dc6 |
| run_units/result.json | 65f3d7fa49a1b38c13434d86e330e07d09484c403c35a6baa6b3630adb89f599 |
| run_units/manifest.json | 5b93b587f3365684d0f6fb65e2dfaab6274e032067e3e48b2406a26eab93cee0 |
| thermal_state.py | 097713bc920a18c8ae755668afba1e7d7e710c7c5a1f8020c452f4a25eb0f1dc |
| run_thermal/result.json | 5f946d0d5d8bbeab7481444836980a4cd32f5fc3a0b18d3807f26ef5f04f04cd |
| run_thermal/manifest.json | 63e85cde7882e637fc18db4f74a0385b4e81733b6fa7801453a8dcbca62fe78f |
| SOURCE_CHECKS.md | 2f62171c6352be4e18973fa04f26d169209398f39570f37d7be9668772c70f88 |

New external reads are pinned by exact source URL/version/date and locators
in the units section above. No external full text was saved in this review.

## Companion decay review and later leading hard-channel bound

The frozen cold_states/check_decays_v2.py and DERIVATION.md pass the following
independent restricted checks. Since psi_old=U psi_mass, the Goldstino
coefficient cG=U†G enters the internal Yukawa contraction without an extra
conjugation. Projecting onto its unit vector and subtracting that norm from
the full null-space sum correctly identifies the unbroken-gaugino complement.
The real/imaginary flat scalar tangents have canonical unit norm.

For Majorana parent mass M, the real-scalar/massless-fermion spin trace is
|y|²(M²−ms²); phase space gives M|y|²(1−ms²/M²)²/(16pi). The ordered
real-scalar widths m sum|yij|²/(16pi) and sum lambdaij²/(32pi m) correctly
handle identical and distinct final states. No factor2 error was found.

The perturbative transpose signs are also consistent: chiral A/B and their
fermions transpose, while V and its gaugino minus-transpose. Canonical K,
TrA²B and the diagonal vacuum are invariant. The checked tensor/Hessian
identities support the C-forbidden two-body transitions and the closed
three-gaugino threshold3m3/m1=1.24484636. This is not an independent
classification of nonperturbative discrete anomalies or UV/gravity effects.

The Goldstino-photon local partial width was independently source-read in
[Brignole–Feruglio–Zwirner9703286v2](https://arxiv.org/pdf/hep-ph/9703286v2),
dated 5 February 1999, §2 Eqs2.26–2.27. Its use here requires a neutral Goldstino,
unbroken U1, rigid SUSY and soft external momenta relative to integrated
states. It is a low-energy current matching statement, not a new exact
finite-momentum three-point calculation. The finite one-loop gaugino mass
and F_eff normalization satisfy those hypotheses to the retained order.

The actual source slope dln mchi/ds=−.99037918 gives the radial Yukawa
−2.86535e−13. Integrating the positive-mass radial response produces the
attractive energy−n²y²/(2mrad²), with the displayed negative compressibility
correction. Its quoted7.6071e−55 ratio at the explicitly chosen halo density
and velocity is consistent with that formula. This number concerns that
local halo example, not an evolved FD halo or the rotating-phase EOS.

The cold author's verdict is correctly conditional: its c7 budget is not an
actual Wilson bound. The separate new decay_bound/ proof supplies a loose
operator-norm upper bound for the leading heavy one-loop boxes and seagull
triangles, including charged scalar/vector mixing and an inclusive spin/
color/phase-space overcount. Read its executed DERIVATION.md with the pinned
SCOPE_ADDENDUM.md: the C-forbidden one-field-strength statement is restricted
to final unbroken gauginos; the Goldstino-photon Ward dipole remains allowed.

At the selected point that result is |c7_eff|<=6.606061e6 and
Gamma_hard<=6.052437e−47GeV, versus Gamma_Ward=5.657295e−45GeV. The inclusive
coefficient is below the actual 99%-retained-survival budget8.290675e7. The
leading Ward plus hard-class survival lower estimate is.996224. The separate
radial reviewer reconstructs this bound independently. It does not turn the
uncomputed higher-loop exchange and higher-body loss into zero; no full
total-lifetime assertion is inferred solely from the two completed classes.

Additional exact input pins (relative to the TP04 root):

| Input | SHA256 |
|---|---|
| cold_states/check_decays_v2.py | 5b86ce5fc084e904ed3f51fefdb56d0d660649a267ccb70ddba3052578ea6972 |
| cold_states/DERIVATION.md | a8238fa2f13832c8b6822b3814b0f86a682f4005f76f63ceb8b4b8e10af968af |
| cold_states/REPORT.md | dc41080557fcd233b7ce926373affd3ef7d03e0f326441479dafc6e27cdaac9f |
| cold_states/run_002/result.json | 36866bb0b638fe36df46d03970091822168c27a0901f61b3bdb7dadbafe3ba53 |
| cold_states/run_widths_v2/result.json | 8c17321d04bd8de4c6e8a0c75ba9b8a4e2283fcb336156e098d6b349bc6571f6 |
| gapless_charge/decay_bound/DERIVATION.md | ad372550be7b9b120bdfc672d648c2963d4920ece008433d90de0fbd3a45148c |

All pinned completed cold-state input/output hashes independently agree.
Its new hard-bound record likewise validates and retains unchanged inputs.
No original numerical experiment was rerun for this review. The new bound's
single-point evaluation is separately contracted and recorded in decay_bound/.
