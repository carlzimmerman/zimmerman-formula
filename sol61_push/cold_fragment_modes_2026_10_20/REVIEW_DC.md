# Independent review of the order-K fixed-charge DC response

20 October 2026. Bounded computation audit of `dc_backreaction.py`, its predeclared contract and completed `dc_run_001`. Exact reviewed bytes are pinned in `sources_review_dc.json`. The reviewer previously derived the raw mode-charge formula and the nonlinear harmonic source; the bordered/angular derivation was visible, so this is a reconstruction audit, not a blind review. No stationary relaxation, linear solve or simulation was rerun.

**Assessment: accepted within the stated finite perturbative scope.** The canonical charge signs, angular projections, bordered frequency response and direct real-field charge integration are consistent. The v2 manifest independently validates and the record contains 75/75 passed checks. This supplies the previously missing finite order-K static charge dressing. It does not give exactly fixed-charge finite-amplitude initial data, a full nonlinear periodic solution, the nonlinear mode-frequency shift, a quantum master equation or a later fixed-Q radiating remnant.

## 1. Raw mode charge and sidebands

For the canonical no-half unit-K mode, reduced components are ordered `(u,s,xi,v,t)`. The bare quadratic Noether charge per K is

    q_raw=integral dr {2omega(|u|^2+|v|^2)-4Omega Im(u* v)
                      +8omega(|s|^2+|t|^2)-8Omega Im(s* t)}.

The signs in the code are correct. In particular, with `cp=(u+i v)/sqrt(2)` and `cm=(u-i v)/sqrt(2)`, the Psi contribution is independently

    2(omega+Omega)|cp|^2+2(omega-Omega)|cm|^2.

The X contribution similarly has the charge-two factor `4(2omega+Omega)|xp|^2+4(2omega-Omega)|xm|^2`. Expanding these expressions gives the displayed negative imaginary cross terms. The agreement check therefore tests a meaningful normalization/sign identity. Linear global charge vanishes for ell=2; that does not remove this nonzero quadratic charge.

## 2. DC angular source, phase assumption and border

The source polynomial is the correct canonical quadratic force in the same field order. Its cross combination `N(z+z*)-N(z)-N(z*)` is precisely the time-independent coefficient multiplying `|Y22|^2`; it contains both mixed products, without an extra factor of two or half. The normalized real harmonic expansion is

    |Y22|^2=c0 Y00+c2 Y20+c4 Y40,
    c0=1/sqrt(4pi), c2=-sqrt(5)/(7sqrt(pi)),
    c4=1/(14sqrt(pi)).

Both analytic coefficient values and the numerical angular expansion are correct. The reduced field equation has source `-c_ell r cross`, with the expected minus sign.

For the selected simple imaginary-frequency modes, the amplitude components can be chosen real and the phase components imaginary. This makes the mixed time-independent phase forcing vanish. The code checks the actual cache rather than silently assuming it. Arbitrary degenerate or multimode superpositions need not have that quadrature property; their phase source and the phase zero/gauge solvability conditions would have to be treated explicitly.

Let d0 be the reduced canonical ell=0 static correction per K, a the radial linear-charge amplitude vector and p the phase vector. A uniform carrier-frequency correction omega->omega+K delta_omega produces the normalized-Y00 field equation and total charge condition

    Hplus_0 d0-sqrt(4pi) a delta_omega=source0,
    sqrt(4pi) dr a^T d0+I delta_omega=-q_raw,
    I=4pi dr p^T p.

These are exactly the code's bordered signs, factors and charge row. The negative upper-right entry is the frequency derivative of the stationary Euler-Lagrange force; the positive lower-right entry is the explicit frequency derivative of background charge at fixed fields. The field response to the frequency shift is already included in d0, so it must not be added again as a separate family deformation. Ell=2 and4 sources have no uniform frequency forcing or linear integrated charge and are correctly solved without that border.

## 3. Primary numerical values and order of cancellation

At L=60, dr=.05 the completed rows are:

| Q | Bare mode charge/K | Static-field charge/K | Explicit-frequency charge/K | delta_omega/K |
|---|---:|---:|---:|---:|
| 80000 | 14.284012469691696 | -13.897018509586623 | -0.3869939601050653 | -4.459077581770212e-6 |
| 160000 | 20.3053504594976 | -19.786446685118456 | -0.5189037743791588 | -2.949696827432439e-6 |

The order-K sums are `7.83e-15` and `-1.50e-14`. All recorded static solve residuals are below `2.4e-15`. The declared box/grid coefficient controls pass, and measured peak RSS is about197MB. These small residuals and finite consistency checks are not interval error bounds or a proof of continuum invertibility.

The direct angular check is a separate evaluation of the full Noether expression on the declared *truncated initializer*: background plus sqrt(K) mode plus K static field correction, with physical carrier frequency omega+K delta_omega. Canonical mode velocities and both charged carriers are included with the correct factors. The angular Gauss/Fourier quadrature resolves the polynomial harmonic products in this charge expression.

Its predicted charge is exactly of the form

    DeltaQ=K(q_raw+q_static+q_frequency)+K^2 c2+K^3 c3.

The code includes the K^2 terms from squared DC fields, shifted-frequency/static cross terms and the shifted carrier acting on the mode variance, plus the K^3 shifted-frequency/DC-square term. Odd half-integer powers vanish after azimuthal integration. This reconstruction has the correct coefficients, including the easily missed `delta_omega*q_static/omega` term.

Consequently the nonzero residual charge at K=1, about `.00152245` and `.00213039`, is expected. It scales primarily as K^2 as K is reduced. The initializer is charge-correct through order K, not exactly charge-preserving for finite K. A second-harmonic radiative field, not included in this initializer, has zero linear integrated charge but contributes at order K^2; the displayed higher-order remainder is therefore specific to the truncated initializer, not the charge error of a completed second-order dynamical solution.

## 4. Scope and interpretation

The solved delta_omega is the order-K adjustment of the charged background's common carrier frequency. It is not the nonlinear shift of the shape-mode frequency Omega. Fundamental-frequency solvability, frequency shifts, secular terms, higher-order gauge/collective-coordinate treatment and long-time error control remain uncomputed.

Subsequent Psi+ radiation exports positive charge, so the radiating remnant's Q changes. This fixed-total-bound-Q construction describes a perturbatively dressed initial excitation; it must not be reused to hold the remnant Q constant during emission. It also does not by itself canonically quantize the charge collective coordinate or justify the previously discussed conditional Lindblad reduction.

No failed record, established source, frozen criterion, publication or unrelated file was modified in this review. The approved claim is finite static charge dressing through order K in the specified alternative matter action. Mode excitation by real mergers, nonlinear capture and orbital transport, dwarf inventories, gravity/physical-unit normalization and four-dwarf selectivity remain separate obligations.
