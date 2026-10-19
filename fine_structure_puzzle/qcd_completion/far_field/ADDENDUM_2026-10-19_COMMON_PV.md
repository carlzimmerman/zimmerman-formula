# Dated correction: the four-dimensional regulator leaves a finite electric term

2026-10-19 UTC. This addendum supersedes the interpretation of the equal
full-KK electric/magnetic coefficient and the common-PV total Coulomb-tail
formula in REPORT.md, sections 2--4. The frozen raw derivations, contracts,
code and executed runs are preserved unchanged. Their finite assertions
were correctly checked, but those assertions did not include the common
four-dimensional regulator limit. The original REPORT's claim of complete
electric matching to that limit was too strong.

The independent reviewer first derived the correction without the target
reports. Its evidence is
`../reviews/far_field/INDEPENDENT_RAW.md`, `check_regulator.py`, and
`runs/pv-001`. Those files and the completed, validated v2 manifest have
now been read and audited here. The finite symbolic code checks the
stated algebra; the KK limiting argument is separately analytic. This
addendum independently rederives that argument and records the consequence.

## 1. What remains valid

For a strictly three-dimensional unregulated frequency, the charged-pair
coefficient is exactly

`K_E,k=K_B,k=-11/(24pi |p_k|)`, `p_k=2pi k/L+h`.

The static calculation, its shell integral, the charged/ghost counts and
the bubble/constant-field checks remain valid. So do the full-KK magnetic
digamma function, beta divergence, finite magnetic coupling match, GPY
potential and corrected microscopic magnetic/dual normalization. The new
term changes the electric coefficient after a common 4D UV subtraction.

## 2. Direct common Pauli--Villars derivation

Use precisely the physical-minus-PV prescription

`Gamma_reg = [1/2 Tr log H-Tr log M_ghost]`
`            -[1/2 Tr log(H+M_PV^2)-Tr log(M_ghost+M_PV^2)]`.

For each charged frequency define
`m_PV=sqrt(p_k^2+M_PV^2)`. The two orbital scalar traces give

`K_B,orb,PV=1/(24pi m_PV)`,
`K_E,orb,PV=p_k^2/(24pi m_PV^3)`.

The second equation follows by differentiating the shifted squared mass,
`U=p_k^2+M_PV^2`: `grad U=2p_k grad h`. Replacing it by
`grad U=2m_PV grad h` would be incorrect. The spin coefficient is
`-1/(2pi m_PV)` for both E and B. Consequently the physical-minus-PV
coefficients obey

`K_B(M_PV)=-11/(24pi) sum_k[1/|p_k|-1/m_PV]`,
`K_E(M_PV)-K_B(M_PV)=1/(24pi) sum_k M_PV^2/m_PV^3`.

The last sum is a convergent Riemann sum. With
`f(t)=(1+t^2)^(-3/2)`, its spacing in `t=p/M_PV` tends to zero and
`integral_R f(t)dt=2`. Therefore

`lim_(M_PV L -> infinity) sum_k M_PV^2/(p_k^2+M_PV^2)^(3/2)=L/pi`.

The finite all-IBP bulk coefficients in this common regulator thus satisfy

`K_E(h)=K_B(h)+c`, `c=L/(24pi^2)`.

This is a genuine finite term in the declared all-IBP representative.
Changing the common four-dimensional strong coupling shifts E and B equally
and cannot absorb their difference. A different surface/EOM representative
must keep its compensating term explicitly.

There is an independent dimensional-regulator check. In d spatial dimensions
put

`C_d=(4pi)^(-d/2) Gamma(2-d/2)|p_k|^(d-4)`.

The one-frequency coefficients are

`K_B,k=[(d-1)/6-4]C_d`,
`K_E,k=[(d-1)(4-d)/6-4]C_d`.

Their difference is `(d-1)(3-d)C_d/6`. At `d=3-2epsilon`, the
Matsubara sum has pole `sum_k C_d=L/(16pi^2 epsilon)+O(1)`; the
two Hurwitz-zeta poles at `1+2epsilon` give this residue directly. The
evanescent factor times that pole is `+L/(24pi^2)`, agreeing with PV.
Taking d=3 before the KK sum loses this term. The finite checks in
`runs/bulk-002` did exactly that earlier specialization and therefore could
not detect the missing four-dimensional term.

## 3. Corrected Coulomb-background bulk tail

Keep the original magnetic harmonic scheme:

`K_B^ren(h;mu)=-11L/(24pi^2)log(mu L/(2pi))`
`               -11L/(48pi^2)F(Lh/(2pi))`,
`F(x)=-psi(x)-psi(1-x)-2gamma_E`.

The tree coefficient `L/(2g_H^2(mu))` is common to E and B. At the
natural magnetic harmonic scale `mu=2pi/L`, the extra `c E^2` on
`h=v-1/r` changes the Gamma inverse-radius coefficient by

`delta a_Gamma=-4pi c=-L/(6pi)`,

and changes the logweight coefficient by `+L/(6pi)`. The GPY contribution
`+L/(3pi)` to the logweight coefficient remains unchanged. Thus the corrected
common-PV, all-IBP local one-loop bulk coefficient is

`a_bulk,loop^PV = L/(2pi)-11L(1+n_mag^2)F(Lv/(2pi))/(12pi)`.

The classical coefficient adds
`2pi L(1+n_mag^2)/g_H^2(2pi/L)`. At center holonomy and unit magnetic tail,

`a_bulk,class+loop^PV = 4pi L/g_H^2(2pi/L)`
`                       +L/(2pi)-22L log(2)/(3pi)`.

This replaces the common-PV interpretation of the corresponding formula
in the original report. The original expression remains the result of the
explicit strict-d3 harmonic-first prescription; it must not be called the
all-IBP limit of this common 4D PV determinant.

## 4. Diagonal, IBP and source representatives must not be mixed

The scalar local diagonal heat kernel differs from the integrated bubble
representative by `Delta m/(24pi)` for one scalar trace. For the two orbital
traces and the common regulator, the full difference is

`Gamma_diagonal-Gamma_IBP = integral Delta F0(h)/(12pi)`,
`F0(h)=sum_k[|p_k|-sqrt(p_k^2+M_PV^2)]`,

up to field-independent terms. In the regulator limit within the chamber,

`F0'(h)=1-Lh/pi`, `F0''(h)=-L/pi`.

Writing `a(h)=(1-Lh/pi)/(12pi)` and `c=L/(24pi^2)`, this gives

`Delta F0/(12pi)=a(h) Delta h-2c E^2`.

The following are distinct representatives, with the same K_B symbol fixing
the magnetic scheme:

| Representative in Gamma | B^2 coefficient | E^2 coefficient | explicit EOM term |
|---|---:|---:|---:|
| Strict d3 harmonic-first bulk | `K_B` | `K_B` | none |
| Common-PV all-IBP bulk | `K_B` | `K_B+c` | none |
| Common-PV local diagonal | `K_B` | `K_B-c` | `a(h) Delta h` |
| Literal source f3=h3 with its (82) | `K_B` | `K_B` | `a(h) Delta h` |

The second and third rows differ by the displayed divergence and require
the corresponding boundary functional on an annulus. In particular
`Delta h=0` does not make that divergence zero: it leaves `-2c E^2`.
Its outer-boundary inverse-radius coefficient in Gamma is `+L/(3pi)`.
Accordingly, if the local diagonal density rather than the all-IBP density
is integrated as a bulk-only quantity, its loop logweight coefficient is
`L/(6pi)-11L(1+n_mag^2)F(Lv/(2pi))/(12pi)`. Its difference from the
all-IBP number is exactly the retained surface coefficient with logweight
sign reversed. Neither number is a boundary-domain determinant.

For the last row, integrating its EOM term by parts adds `+2c E^2` to
its bulk and leaves the surface `integral_boundary a(h) partial_n h`.
Thus literal source EOM82=0 on the Coulomb profile does not establish the
all-IBP coefficient used in the earlier report. The source's printed (83)
also has the separately documented sign inconsistency. No checked source
term currently reconciles the remaining finite `c E^2` mismatch between
the literal source formulas and the direct common-PV calculation.

Accordingly, the magnetic/digamma/beta source correspondence remains
verified, while the earlier claimed exact electric all-IBP correspondence
is withdrawn and marked unresolved. This is a bounded comparison of the
specified formulas and regulator, not a blanket claim about that paper.
The independent review's ADJUDICATION.md reaches the same separated result.

## 5. Physical scope and audit status

The screened magnetic stiffness and
`kappa_dual=1/(16pi^2 kappa_B)` remain unchanged. If the actual stable
holonomy saddle screens E, the new electric term has no algebraic large-R
tail. A full finite-wall determinant must still combine local bulk and
boundary/domain terms in one convention. Neither old nor corrected bulk
numbers determine vacuum stress, a QCD-to-electromagnetic bridge, or alpha.

Audit outcome: the reviewer's finite-regulator correction is confirmed by
an independent PV calculation and dimensional-regulator residue argument.
The review's `pv-001` manifest validates with `run.status=completed`; its
exact symbolic assertions were inspected rather than blindly equating
successful execution with the full analytic claim. No new experiment was
required for this adjudication. The original completed run remains valid
evidence only for its narrower strict-three-dimensional finite assertions.
No executed input, output or previous raw definition was modified.
