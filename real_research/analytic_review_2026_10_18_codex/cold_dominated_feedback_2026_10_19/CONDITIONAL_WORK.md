# Conditional full linear work on the closed cold-dominated occupied set

19 October 2026. Author `/root/boundary_pairing`. Analytic derivation only.
This is the only file written for this task. No scientific scripts, numerical
integration, discretized scientific arrays, or process operations were used.
The repository sources were read without modification. Self-review only.

## 1. Exact conditional theorem

Fix one of the actual, strictly positive-warmth cold-dominated equilibria in
`GEOMETRY_AND_CAP.md`. Retain its exact two-species distribution, forces,
kernels, support, and the coercive energy `Q`. Assume the proved operator
inputs in `BOUNDARY_PAIRING.md`, `HIGH_FREQUENCY_INVERSE.md`, and
`REGULAR_INVERSE.md`, and the mode regularity and geometry in
`THRESHOLD_MODES.md` and `GEOMETRY_AND_CAP.md`. In particular:

* the full action-frequency gradient is nonzero on the closed occupied sets;
* circular stationary epicyclic points are finite and nondegenerate;
* the exact flat susceptibility extensions and cap resonance geometry hold;
* every boundary kernel is an actual finite-energy mode, the exceptional
  frequencies are locally finite, and high-frequency decay makes their full
  set `E` finite;
* at every such frequency the actual kernel fields have the `C^(1,1)`
  bootstrap specified in the mode and reduced-inverse inputs.

Make exactly the additional force-cancellation assumption

    (CF) phi_j'(s_c)=0 for every actual mode field phi whenever
         nu=Omega_j(0,L_c(s_c))=kappa_j(s_c),
         kappa_j'(s_c)=0, kappa_j''(s_c)!=0,

with the negative-frequency version obtained by conjugation. Thus this is an
assumption on every field of a possibly multidimensional kernel, at every
resonant fundamental circular threshold. No mode-absence condition is made.
Take as an operator input the conditional conclusion of `REDUCED_INVERSE.md`:
under (CF), for some `alpha_0>0`,

    (I-K(z))^-1=R_nu/(z-nu)+H_nu(z),

where `H_nu` is bounded and Holder on the whole `Y_gamma=C^gamma(I)^2`,
`0<gamma<1/2`, near each `nu in E`, and

    R_nu=nu sum_(a,b) phi_a (Q_Gram^-1)_ab ell_b,
    ell_b(f)=integral conjugate(h_b)*f dGamma,
    Q_Gram,ab=Q[h_a,h_b].

Here `h_a` is a basis of the actual `nu` energy eigenspace and `phi_a=P h_a`.
This input does not assume a work estimate or differentiability of the full
forcing on `Y_gamma`.

**Theorem.** For every smooth, compactly supported radial fixed-`L` canonical
generator `g_0`, the full actual linear solution with

    h_0=-w D g_0,   u_0=D g_0,

has

    sup_(t>=0) sup_i sup_(q in Abar_i) sup_(theta_0)
         |W_i(t;theta_0,q)| < infinity,

where `Abar_i` is the entire closed occupied action set, including its circular
line, upper flat cap, and physical endpoints. Consequently

    sup_(t>=0) ||u_i(t)||_(L^infinity(Abar_i x T)) < infinity.

The bound is linear in finitely many smooth-source seminorms of the datum and
its energy norm. It is not an energy-norm-only estimate. Constants may depend
on the selected halo and its fixed positive warmth.
On the support boundary, `u` is defined by the linear label transport equation
with initial value `Dg_0`, rather than by division by the vanishing `w`.

The new source-side step below proves the necessary pole cancellation from
the mode left coupling. It does not assume that the full vector-valued forcing
is `C^1`, or divide an arbitrary `C^alpha` field increment by `z-nu`.
The theorem is conditional on (CF) and the named reduced-inverse result. It
makes no nonlinear, actual-path, or all-time confinement assertion.

## 2. Conventions and the forcing in a useful exact form

Use the actual conventions

    dGamma=C_Gamma dr dv dL,  dm=2*pi*C_Gamma dJ dL,
    C_Gamma=4*pi^2,  w_i=-F_(i,E),
    omega_ik=k Omega_i,  D_i=Omega_i partial_theta,
    psi_in=P h_0.

The shell map `P` is the actual symmetric matrix with Newtonian cross/free
entries and the tethered entry stated in the sources. The Laplace convention
is `fhat(z)=integral_0^infinity exp(i z t) f(t) dt`, `Im z>0`. Then

    (I-K(z)) Psihat_1(z)=B(z),
    Psihat_1=hat(partial_t psi),
    B(z)=Psihat_1^0(z)+K(z)psi_in.

For `k!=0` put

    A_ik(q)=(h_0/w)_ik(q)+(psi_in)_ik(q)
           =-(D g_0)_ik(q)+(psi_in)_ik(q).

The exact free transport and kernel formulas give

    B(z)=-P[sum_(k!=0) w_i*omega_ik*A_ik(q)
                                  *exp(i k theta)/(omega_ik-z)].       (2.1)

Indeed `Psihat_1^0=-P[omega h_0/(omega-z)]` and
`K(z)psi_in=-P[w omega psi_in,k/(omega-z)]`.
There is no derivative of an arbitrary Holder radial field in (2.1).

The initial physical source `h_0` is smooth and compact. Its radial density,
cumulative masses, and the actual shell field equation make `psi_in` smooth
on the closed radial interval. Therefore, in the smooth circular variables
`(a,L)`, `a=sqrt(J)`, each `A_ik` is smooth and vanishes at `a=0` for `k!=0`.
All its needed derivatives decay rapidly in `|k|`: for each fixed finite
orders `m,M`,

    ||A_ik||C^m_(a,L) <= C_(m,M) (1+|k|)^(-M),
    |A_ik(a,L)| <= C_M (1+|k|)^(-M) a.                (2.2)

To justify this directly, pull the smooth physical functions back through the
smooth oscillator map and integrate by parts in `theta`. Their values at
`a=0` are independent of `theta`; the zero harmonic is excluded. The factor
`k` in `Dg_0` is absorbed by choosing one more integration by parts. For the
`psi_in` term, no support cutoff is needed: multiplication by the exact flat
`w` in (2.1) supplies the cap and angular-momentum zero extensions.

## 3. Global smooth-source transform bounds, including the circular boundary

For clarity this supplies the smooth-source transform leaf rather than
reusing the old stronger boundary transversality assumption.
Let `P_k(r,q)` be an actual shell harmonic and set `d=|r-r'|`. The exact
indicator-harmonic identity in `HIGH_FREQUENCY_INVERSE.md` gives

    |P_k(r,q)-P_k(r',q)|<=C d/|k|,                    (3.1)

and `P_k(R,q)=0`. As a function of `(a,L)`, each kernel section is uniformly
Lipschitz; its nonzero harmonic vanishes at `a=0`. This follows from joint
Lipschitz regularity of `P` and the smooth oscillator map and needs no action
derivative of a turning-angle indicator.

Consider the product

    [P_k(r,q)-P_k(r',q)] A_ik(q).

The first factor and the second factor are Lipschitz in `a`, vanish at `a=0`,
and the second has the rapid bounds (2.2). At fixed `L`, its difference
between `a,b>=0` is bounded by

    C_M (1+|k|)^(-M) (a+b)|a-b|
       =C_M (1+|k|)^(-M)|a^2-b^2|.

Changes in `L` are Lipschitz as well. Thus the product is Lipschitz in ordinary
actions `(J,L)`, with norm `C_M(1+|k|)^(-M)`, and its zero extension across
`J=0` remains Lipschitz. Its sup norm has the stronger bound, from (3.1),

    C_M d (1+|k|)^(-M-1).

Multiplication by `w_i Omega_i` and by a fixed smooth partition preserves
these estimates; the exact flat extensions cover all support boundaries.
For any fixed `0<beta<1`, elementary interpolation gives

    ||amplitude_k||C^beta_(J,L)
       <= C_M d^(1-beta) (1+|k|)^(-M-1+beta).         (3.2)

Use the fixed finite frequency submersion charts `y=Omega_i(q)`, independent
of `k`. The product extensions just justified remove all moving-domain terms.
The corresponding compactly supported `C^beta` coarea density `b_k(y)` has
the same norm (3.2), and the contribution to `B(r)-B(r')` is exactly

    -integral b_k(y)/(y-z/k) dy.                     (3.3)

The Cauchy-transform subtraction proof in `HIGH_FREQUENCY_INVERSE.md` bounds
this uniformly on either closed half-plane. Its frequency Holder norm is
bounded for every exponent strictly below `beta`, with the extra scale
`|k|^(-alpha)` in the frequency variable `z`. Summing (3.2) with `M` large
proves a global Holder bound into `C^(1-beta)` in output radius. Choose
`beta<1-gamma` so this output space embeds into `Y_gamma`.

The same estimates also give the exact needed decay. If
`|k|<=|z|/(2 Omega_+)`, use the distance from `z/k` to the fixed positive
`y` support in (3.3); it gains `C |k|/|z|`. Sum these low harmonics using
`M>1+beta`. The remaining rapidly decaying harmonic tail is `O(1/|z|)` or
better. Bounded `z` is already covered. Consequently, on
`Sbar={0<=Im z<=1}`, for some `alpha_s>0`,

    B in C^alpha_s(Sbar;Y_gamma),
    sup_Sbar (1+|z|)||B(z)||Y_gamma < infinity.        (3.4)

All constants use finitely many smooth-source seminorms in (2.2). This proves
the source transform statement at simple circular tangencies and flat caps
under the full-gradient geometry; it does not infer it from the old raw
Lemma T or Prop F outline. The logarithmic Cauchy estimate is taken on one
fixed `Omega` support interval, so no changing harmonic support-length
constant is concealed.

## 4. The modal left-coupling difference quotient

Fix one actual exceptional frequency `nu` and one of its energy modes `h_a`,
with field `phi_a=P h_a`. Reciprocity and (2.1) give the scalar identity

    ell_a B(z)
      =-sum_i sum_(k!=0) integral
          w_i*omega_ik*conjugate(phi_a,ik)*A_ik
                              /(omega_ik-z) dm.       (4.1)

This is the extra information not contained in the whole-field Holder
regularity (3.4). On a local resonance chart put `t=omega_ik-nu` and denote
the coarea density in (4.1), before the denominator, by `q_a(t)`.
We prove that `q_a(t)/t` has a compactly supported positive-Holder extension
at zero. Smooth factors and partitions are implicit below.

On an eccentric regular resonance the reduced-inverse input supplies

    sqrt(w_i)*phi_a,ik = t V_a,

with `V_a` Lipschitz in the chart, including the flat support collars. The
other weighted factor `sqrt(w_i)*A_ik` is smooth there. Hence the divided
coarea density is Holder. At a regular circular crossing solve for `L`,
keeping `a>=0`. The same weighted quotient is Lipschitz in `(a,L)` and
vanishes at `a=0`; the smooth-source factor also vanishes there. Their
product is Lipschitz in ordinary actions by the same product calculation
as Section 3. Alternatively one can keep fixed `a` when taking the coarea
integral. In either case the divided density has a positive Holder bound.
This uses the exact weighted division at the cap from `REDUCED_INVERSE.md`,
not an inference that unweighted traces vanish merely because `w` is flat.

At a simple circular threshold use its exact half-plane Morse chart

    t=epsilon*(b^2+x^2),  dJ dL=b c(b^2,x) db dx,
    rho=sqrt(b^2+x^2),  epsilon in {+1,-1}.

By the mode bootstrap and (CF), the mode weighted coefficient `g` obeys

    g in C^(1,1),   g=O(rho^2),   grad g=O(rho).

The smooth weighted source coefficient `f=sqrt(w_i)*A_ik` is smooth and
`O(b)`, hence `O(rho)`. Writing `s=rho^2>=0`, the coarea density has the form

    q_a(epsilon s)=rho integral_0^pi
        sin(theta) conjugate(g(rho sin(theta),rho cos(theta)))
                   f(rho sin(theta),rho cos(theta)) c(...) dtheta,

up to fixed smooth factors. It is `O(rho^4)=O(s^2)`. More precisely, the
angular integral before the prefactor is `O(rho^3)` and its `rho` derivative
is `O(rho^2)`. Therefore `q_a(epsilon s)/s` is `O(s)` with bounded derivative
in `s`. Its zero extension across the unoccupied side is Lipschitz. In
particular no threshold `sqrt(s)` term survives in this left coupling.
For higher resonant circular harmonics the bootstrap already supplies the
same zero first jet; only the fundamental uses (CF).

Finitely many such charts cover the resonant harmonics. All remaining charts
are nonresonant and analytic in `z`. The infinite nonresonant harmonic tail
has locally bounded analytic derivatives by (2.2), or by Parseval together
with the differentiated scalar multiplier `O(1/|k|)`.
Thus the elementary exact Cauchy identity

    [Cq(delta)-Cq(0)]/delta = C(q(t)/t)(delta),
    delta=z-nu,

applied with the overall minus sign of (4.1), proves that, for some
`alpha_l>0`,

    D_a(z):=[ell_a B(z)-ell_a B(nu)]/(z-nu)

extends as a bounded `C^alpha_l` scalar function through `z=nu`, on the
closed upper half-plane. This establishes precisely the needed finite-rank
regularity. No claim that `[B(z)-B(nu)]/(z-nu)` is bounded in the whole
`Y_gamma` space has been used or proved.

## 5. The residue is the actual energy projection

At `z=nu`, the canceled singularity in (4.1) allows the mode formula

    h_a,ik=-w_i*omega_ik*phi_a,ik/(omega_ik-nu)

to be inserted directly. It gives

    ell_a B(nu)
       =sum_i sum_(k!=0) integral conjugate(h_a,ik)*A_ik dm
       =integral conjugate(h_a)*h_0/w dGamma
             +integral conjugate(h_a)*psi_in dGamma
       =Q[h_a,h_0].                                (5.1)

The last equality is the polarized actual kinetic-plus-field energy;
reciprocity identifies its field term. These integrals converge also from
energy Cauchy-Schwarz. Let `P_nu` be the actual `Q`-orthogonal energy
projection and put `Phi_nu=P[P_nu h_0]`. Then

    P_nu h_0=sum_(a,b) h_a (Q_Gram^-1)_ab Q[h_b,h_0],
    R_nu B(nu)=nu Phi_nu.                           (5.2)

The pole residue has therefore been authenticated against the actual spectral
projection. Subtracting this residue removes exactly the actual mode part of
the solution rather than a formal pencil pole with unspecified data coupling.

## 6. The continuous derivative transform is Holder with the right decay

Let `P_E=sum_(nu in E) P_nu` and `h'=h_0-P_E h_0`. Define

    F_reg(z)=(I-K(z))^-1 B(z)
                    -sum_(nu in E) nu Phi_nu/(z-nu).  (6.1)

Linearity of the actual energy evolution and the Laplace transform gives

    F_reg(z)=hat(partial_t psi[h'])(z),  Im z>0,

because the derivative field of `exp(-i nu t)P_nu h_0` has Laplace transform
`nu Phi_nu/(z-nu)` under the stated convention.
Write `psi^c(t)=psi[h'](t)` for this continuous-component field.

Near a fixed `nu`, insert the whole-field reduced inverse:

    (I-K(z))^-1 B(z)-R_nu B(nu)/(z-nu)
       =R_nu [B(z)-B(nu)]/(z-nu)+H_nu(z)B(z).

The first term is Holder by Section 4 and the finite-rank residue formula;
the second is Holder by (3.4) and the reduced-inverse input. The other mode
terms in (6.1) are analytic near this frequency. Away from the finitely many
mode neighborhoods, the inverse is uniformly bounded and Holder by the
ordinary resolvent identity, compactness, the high-frequency bound, and
operator Holder continuity of `K`. Thus there is one `alpha>0` for which

    F_reg in C^alpha(Sbar;Y_gamma),
    M:=sup_Sbar (1+|z|)||F_reg(z)||Y_gamma < infinity,
    H:=[F_reg]_(C^alpha(Sbar;Y_gamma)) < infinity.     (6.2)

At large `|z|`, the inverse has norm at most two, `B=O(1/|z|)`, and every
subtracted mode term is `O(1/|z|)`, proving the weighted bound. A finite
cover handles the remaining compact part of the strip. The same estimates
are linear in the smooth-source norms and in `||h_0||Q`.

This is the place where a plain Holder estimate on the full `B` would have
been insufficient: only the residue-coupled difference quotient in Section 4
justifies the pole subtraction. The actual spectral projection alone would
not have supplied a Holder boundary transform without that calculation.

## 7. Uniform work for the continuous component

Fix a receiver `(i,q)` in the complete closed occupied set and put
`omega=k Omega_i(q)`. The orbital map is uniformly Lipschitz in angle and
`Omega_i>=Omega_->0`. For `k!=0`, orbital Fourier extraction on `Y_gamma`
gives uniformly

    |f_ik(q)|<=C |k|^(-gamma)||f||Y_gamma.             (7.1)

For `epsilon>0`, the damped derivative field of `h'` is in time `L^1 cap L^2`
by the uniform actual energy-to-field bound. Its harmonic transform is
`F_reg,ik(nu+i epsilon;q)`. Set

    a_k(nu)=F_reg,ik(nu+i epsilon;q)/(2*pi).

The elementary frequency-to-work lemma in the raw full-feedback source,
proved by subtracting the value at `nu=omega` and using the bounded sine
integral, says for `rho=1`

    |integral a_k(nu)*(exp(i*(omega-nu)*t)-1)/(omega-nu) dnu|
       <=4|a_k(omega)|
         +4 integral_0^1 modulus(a_k;s)/s ds
         +2 integral_(|nu-omega|>=1) |a_k(nu)|/|nu-omega| dnu.  (7.2)

Its left-hand side is, up to a fixed unit complex factor from Fourier
conventions, the damped receiving work harmonic. Equations (6.2) and (7.1)
give

    |a_k(nu)|<=C |k|^(-gamma) M/(1+|nu|),
    modulus(a_k;s)<=C |k|^(-gamma) H s^alpha.

For all sufficiently large `|k|`, `|omega|>=Omega_- |k|` and the entire unit
frequency neighborhood of `omega` has `1+|nu|>=c|k|`. Thus on that interval

    |a_k|<=C M |k|^(-1-gamma),
    modulus(a_k;s)<=C min(M |k|^(-1-gamma),
                          H |k|^(-gamma) s^alpha).

The Dini integral of the minimum is at most

    C_alpha M |k|^(-1-gamma)
                    [1+log(1+|k| H/M)],             (7.3)

with the zero-`M` case interpreted by continuity. The far integral in (7.2)
is bounded by

    C M |k|^(-gamma) integral_(|nu-omega|>=1)
                  dnu/[(1+|nu|)|nu-omega|]
       <=C M |k|^(-1-gamma) log(2+|k|).              (7.4)

For example split at `|nu|=|omega|/2`, at a comparable neighborhood of
`omega`, and at infinity. The finitely many small harmonics use (7.2)
directly. The series in (7.3)--(7.4) is summable because `gamma>0`.
Also `M log(1+H/M)<=H`, so its sum is bounded linearly by `C(M+H)`.
All constants are uniform in the receiver and in `0<epsilon<=1`.

The zero receiving harmonic is controlled without an inverse Fourier
estimate: integration by parts gives

    |integral_0^t exp(-epsilon s) partial_s psi^c_i,0(s,q) ds|
       <=3 sup_s ||psi^c(s)||infinity
       <=C ||h'||Q.

Hence the entire damped work is uniformly bounded. To justify identification
with the actual work, first compare Fourier coefficients in `theta_0`.
The summable work bounds give a uniformly convergent Fourier series; its
coefficients are exactly those of the continuous-in-`theta_0` actual damped
work integral. Uniqueness of Fourier coefficients identifies the two.
Finally let `epsilon` decrease to zero at fixed `t`; the actual derivative
field is continuous and bounded on the finite time interval, so dominated
convergence applies. The bound remains independent of `t`, giving

    sup_(t,i,q,theta_0) |W_i[h'](t;theta_0,q)|
       <=C (M+H+||h'||Q).                           (7.5)

No receiving-frequency gap is used, and the estimate includes `J=0`, the
flat cap, and physical endpoint limits.

## 8. Modal work and the label estimate

For a single mode field `exp(-i nu t)Phi`, each nonzero harmonic satisfies

    W_k(t,q)=-i nu Phi_k(q)
                       integral_0^t exp(i*(k Omega(q)-nu)s) ds.

Off exact resonance its time supremum is
`2 |nu| |Phi_k(q)|/|k Omega(q)-nu|`. The sources prove the required bounded
quotient over the full closed occupied set:

* regular eccentric and regular circular crossings use trace division;
* eccentric cap points are approached by occupied regular resonance curves,
  so their trace and division estimates follow from the actual cap geometry;
* physical endpoint accumulation is absorbed by flat mode forces and the
  nonzero endpoint epicyclic derivatives;
* at simple circular thresholds, the `C^(1,1)` mode bootstrap makes all
  higher resonant harmonics quadratic; the fundamental is quadratic by (CF).

Exactly resonant nonzero harmonics have zero coefficient and give zero work.
Only finitely many harmonics can resonate at a fixed mode frequency. For the
remaining tail, `|k Omega-nu|>=c|k|` and the uniform `C^(1,1/2)` angular bound
already gives an absolutely summable estimate; the stronger bootstrap is
available as well. The zero harmonic is an endpoint difference of the mode
potential and is bounded. Therefore every `P_nu h_0` has uniformly bounded
closed-set work. There are finitely many `nu`, and all constants on their
finite-dimensional mode spaces are finite, so their summed contribution is
bounded linearly in `||P_E h_0||Q<=||h_0||Q`.

Adding this to (7.5) proves the theorem's full work bound. The exact orbit
endpoint identity from the raw full-feedback source gives

    W=(psi-u)(t,theta_0+Omega t,q)-(psi-u)(0,theta_0,q),

and the uniform energy field bound gives

    sup_t ||u_i(t)||infinity
       <=||Dg_0||infinity+2 C ||h_0||Q+C_W.

This is a full linear estimate along equilibrium orbits. Neither a bound
along perturbed nonlinear paths nor control of nonlinear label gradients
has been inferred.

## 9. Exact remaining gap and provenance

Subject to the stated input theorems, there is no additional source-pole
regularity gap: Sections 4--5 prove the extra left-coupling regularity and
identify its residue with the actual energy projection. The resulting
conditional full closed-set linear work theorem does not require absence
of modes and does not assume its desired work conclusion as an input.

The unresolved model-specific implication is (CF), or the construction of an
actual mode violating it. The conditional reduced-inverse proof is also a
named mathematical dependency; this note does not independently audit all
of its weighted-square-root and Schur block arguments. If that dependency
fails, this theorem remains conditional on the exact pole-plus-Holder
statement in Section 1. No claim that (CF) follows from energy alone is made.

Mathematical proofreading self-review covered the entire new artifact,
including signs, projections, Laplace convention, source/receiver indices,
and the distinction between whole-field and finite-rank difference quotients.
This is not an independent correctness certificate. No scientific verification
command was applicable or run.

## 10. Sources and hashes at reading

All paths below are relative to
`real_research/analytic_review_2026_10_18_codex/`.

- `cold_dominated_feedback_2026_10_19/HIGH_FREQUENCY_INVERSE.md`:
  `6111b7f0f2e2ea0ef1ea80b81c1a1227374bedc270614c50698db830ade8d49c`
- `cold_dominated_feedback_2026_10_19/REGULAR_INVERSE.md`:
  `4830712683b98b46a53b796b4bde109c618a4fd26fa910cd47176ebe9f3ddf80`
- `cold_dominated_feedback_2026_10_19/THRESHOLD_MODES.md`:
  `40304ae8d1c0495cdd7482202aa9dcdfa494f12287754b7e648dd2adf26a77b5`
- `cold_dominated_feedback_2026_10_19/GEOMETRY_AND_CAP.md`:
  `c40c5f63e533fe19e41b996e292d21892160bf2b4aa31ffb499313b64f54fc0d`
- `cold_dominated_feedback_2026_10_19/REDUCED_INVERSE.md`:
  `ebc588cbd3fef36295dc355542f5b5344327c6ed1d76af12e777ee36786e93d1`
- `claude_continuation_2026_10_19/full_feedback/RESULT.md`:
  `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`

The complete boundary-pairing source is the earlier artifact
`/private/tmp/boundary_pairing_20261019.md`, SHA-256
`5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d`,
now durably copied by the coordinator as `BOUNDARY_PAIRING.md`. No external
literature claim is used.
