# Independent narrow review of the rational completion

Reviewed source:
`sol61_push/gravity_restoring_2026_10_19/rational_completion/RATIONAL_COMPLETION.md`,
23,087 bytes, SHA-256
`d6f6b0c01ffa2b74575ea003a291173150cba9b1bcac89865220d283e9d84e3f`.
Review scope: Sections 1, 3-5, and the physical source restrictions in Section
2. Sections 6-8 and the author's numerical implementation were not audited
here. This is a separate agent's analytic reconstruction with shared project
context, not an externally independent referee report. No source file was
edited by this review.

**Claim card.** For independent zero-temperature two-level dipoles with
`H_Delta=d(Delta sigma_x-E sigma_z)`, the specified positive occupied
dipole-weighted continuum yields `p=p_sat E/(a+E)` and the target Legendre
energy after the additional normalization `p_sat=a/K`. A positive isotropic
fixed-axis spectrum yields the same radial law. Finite-gap cutoffs are
claimed to give a controlled feature approximation in an intermediate field
window. **Primary verdict: correct only after a stated restriction** to the
low-field cutoff window below. The infinite-continuum construction and
isotropic inversion are proved as written under their stated assumptions.

## Independent reconstruction

For one site the two eigenvalues are `+-d sqrt(Delta²+E²)`. Its positive
ground-energy lowering is `d(sqrt(Delta²+E²)-Delta)`, with derivative
`d E/sqrt(Delta²+E²)`. For

\[
 w(s)=p_{\rm sat}{as\over(a^2+s^2)^{3/2}},
\]

the primitive

\[
 {d\over ds}\sqrt{{s^2+E^2\over s^2+a^2}}
 ={(a^2-E^2)s\over(s^2+a^2)^{3/2}\sqrt{s^2+E^2}}
\]

gives `integral w(s)/sqrt(s²+E²) ds=p_sat/(a+E)`, including the removable
`E=a` case by direct integration. Therefore `p=p_sat E/(a+E)` and
`F=p_sat[E-a log(1+E/a)]`. The inverse source is
`E=a p/(p_sat-p)`. Its Legendre transform is

\[
 W=-ap-ap_{\rm sat}\log(1-p/p_{\rm sat}).
\]

Setting `p_sat=a/K` gives the target and is an additional calibration.
Before this calibration the susceptibility is `p_sat/a`, so nothing in
this spectral integral predicts `K`.

For isotropic fixed axes, the absolute direction cosine `c` is uniform on
`[0,1]`. The response component is `d c² E/sqrt(Delta²+c²E²)`. Changing
`Delta=cs` in the nonnegative double integral gives

\[
 w_{\rm eff}(s)=\int_0^1c^2w_0(cs)dc
 ={1\over s^3}\int_0^s t^2w_0(t)dt.
\]

Hence `w0=3w_eff+s w_eff'`. Applying that derivative to the stated `w`
gives exactly

\[
 w_0(s)=p_{\rm sat}{as(4a^2+s^2)\over(a^2+s^2)^{5/2}}>0.
\]

Its unprojected inventory is `integral w0=2 p_sat`. As a separate
normalization check, `integral w0(s)/s ds=3 p_sat/a`, and multiplication
by the orientational factor `<c²>=1/3` recovers `p_sat/a`. Its saturation
also gives `2 p_sat<c>=p_sat` with `<c>=1/2`. These are consistent
independent checks of both ends of the radial response.

The Abel uniqueness argument is valid in the stated nonnegative
locally-integrable finite-weight density class, with boundary values and
inversion interpreted almost everywhere. It is uniqueness for the chosen
two-level kernel, not for all microscopic models.

## Finite-cutoff restriction

The exact finite-cutoff primitive, `E=a` removable case, susceptibility,
saturation and second-gap-moment formulas were rederived and agree.
The proposed uniform absolute-error bound also holds. The remaining issue
is using that absolute error to control the **quadratic low-field feature**
when the cutoff spectrum is kept without rescaling.

The missing UV tail changes the linear susceptibility by

\[
 \delta\chi_{\rm UV}
 ={p_{\rm sat}\over a}
   \left(1-{L\over\sqrt{L^2+a^2}}\right)
 ={p_{\rm sat}a\over2L^2}+O(L^{-4}).
\]

For `E<<a<<L`, the UV response error is consequently
`delta p_UV~p_sat a E/(2 L²)`. Relative to the target quadratic correction
`p_sat E²/a²`, its size is

\[
 {\delta p_{\rm UV}\over p_{\rm sat}E^2/a^2}
 \sim {a^3\over2L^2E}.
\]

Thus resolving that feature without retuning the susceptibility also
requires `E>>a³/L²`, in addition to `ell<<E<<a`. The relations
`ell<<a<<L` and `ell<<E<<L` alone are insufficient for arbitrarily small
fields within that range. For example `a=1`, `L=10^3`, `ell=10^-12`,
`E=10^-9` obey the latter hierarchies, but this UV linear error is about
500 times the target quadratic term. This example uses asymptotics whose
omitted relative corrections are controlled by `a²/L²=10^-6` and
`E²/L²=10^-24`.

The cheapest repair is to add `E>>a³/L²` when claiming low-field feature
accuracy, or explicitly introduce and analyze a susceptibility retuning.
The infinite-continuum identity and the stronger-field endpoint control
are unaffected. The finding was sent to the author and coordinator.

## Physical qualification

Section 2 correctly retains the source stock in the leading fixed-charge
gravity operator and redshifts the complete matrix under a constant lapse.
Its separated spatial-mode probe is explicitly conditional on actual mode
profiles and support; it is not an isolated uniform-field internal dipole.
Sections 3-4 explicitly add supported two-state degrees and an occupied
reduced-gap distribution. This is the necessary qualification: an exact
conditional spectral completion has been constructed, while the original
particle-to-dipole source map remains open.

| Obligation | Assessment |
|---|---|
| One-site sign and energy lowering | Passed by direct diagonalization |
| Infinite-continuum rational integral | Passed by independent primitive |
| Legendre transform and normalization | Passed; `p_sat=a/K` remains input |
| Isotropic kernel and inverse spectrum | Passed by variable change/differentiation |
| Isotropic inventory and susceptibility | Passed by separate endpoint integrals |
| Cutoff primitives and absolute error | Passed analytically |
| Low-field feature window | Requires `E>>a³/L²` absent retuning |
| Original-action physical source restriction | Passed within the declared NR/lapse scope |
| Author's quadrature/code provenance | Not audited or rerun here |

No external theorem or load-bearing computation was needed for this
review. Its dependence on standard integration and differentiation is
spelled out above. Any later source edit has a new hash and is not silently
covered by this reviewed byte pin.

## Reconciliation of the revised cutoff window

The revised source reviewed in Sections 3 and 5 is 25,988 bytes, SHA-256
`5ac62246b8f3716899b69ab579f19173e1d6103c0428b2020774612d88792724`.
It now states `max(ell,a³/L²)<<E<<a` for low-field feature control without
susceptibility retuning, and records the stronger-field IR inventory
condition `ell² E/a³<<1` when comparing to the full target inventory.
Both conditions follow from the displayed error bound divided by the
specific target feature being measured. They resolve the cutoff finding.

The revised local Hamiltonian also includes the identity term
`d Delta 1`, giving zero ground energy at zero field separately for each
site before forming the continuum. This avoids defining the continuum as
the difference of two divergent absolute zero-field energies, since
`integral w Delta` diverges. The energy lowering and response integrals
audited above are unchanged. The note additionally distinguishes a
thermodynamic/disorder-averaged continuous spectrum from a finite realized
sample of two-state sites. These qualifications are appropriate.

For the revised sections within this audit's scope, the primary verdict
is now **proved as written** under the explicit independent-site,
zero-temperature, occupied-spectrum and physical-source assumptions.
No source map from the original particles, universal normalization or
bound-state existence has thereby been established. Other revised sections
and the numerical implementation remain outside this audit.

## Final-byte reconciliation

The author's final note is 26,106 bytes, SHA-256
`4c055419d663114a2831feebab02f704da35c2724bf728db80b8b475595e8367`.
Its only changes from the 25,988-byte version above are in Section 6:
clarifying the permanent-site number density as `n_site`, and making the
thermal cell volume `V_c` explicit in the partition function, total-dipole
support and gamma-shift formulas. Reversing exactly those text changes
reproduces `5ac62246b8f3716899b69ab579f19173e1d6103c0428b2020774612d88792724`
byte for byte by SHA-256; no source file was mutated during this check.
Thus the reviewed Sections 1-5 were unchanged in that final edit.

I also freshly reread the complete final Sections 1-5 and checked the final
hash remained stable. The scoped verdict remains **proved as written**.
The new Section 6 volume normalization is sensible but its full thermal
argument remains outside this narrow review, as do Sections 7-9 and the
author's numerical implementation. There is no hidden extension of the
review to an unexamined source version.
