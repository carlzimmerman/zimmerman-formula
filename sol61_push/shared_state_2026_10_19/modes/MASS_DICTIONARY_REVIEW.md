# Independent focused audit of the shared-mode mass dictionary

**Normalized claim.** In the common-profile n=1 TF family, fix the EOS
coefficients, hence R; fix the odd probe
`D_k=int rho sin(kz)/k` with the COM removed; and fix one positive-frequency
total-density mode with nonzero physical source overlap. If objects of
different mass in that self-similar family are each counted once through
that mode, and a proposed saturating-site comparison identifies
`w(Delta)=n(Delta)d(Delta)`, then the displayed joint mass/dipole/reduced-gap
map and population moments follow. The infinite target weight has finite
object count but infinite object mass, with the stated quadratic
reduced-gap-cutoff cost.

**Primary verdict: proved as written.** This is a verdict on the conditional
dictionary and mass-budget test, not a derivation of saturation, occupation,
object formation or a medium from the original action. The raw file retains
those qualifications. Its mass-family scaling relies on the specified TF
state and source; it is not a universal relation for arbitrary scalar states.

Raw artifact audited:
`sol61_push/shared_state_2026_10_19/finite_wavelength/MODE_MASS_DICTIONARY.md`,
SHA-256 `19e3be56697bd24ba2a8412a7bf7ef802baf6804234e3ca3f6fb3cf533c88312`.
This final version includes the source-scope clarification requested during
the review. The preceding version had hash
`74a4e33679f82f5db4fd1d1599a8e0b1eb2bed3a50e087f48cda03ba74648ba2`.
Review date: 19 October 2026. This is a direct algebra/source audit by a
different subagent from the author in the same session. No scientific
computation was rerun, and no author file was edited by the reviewer.

## Claim card and dependencies

The mathematical domain is `hbar,G,R,M,c_nu>0`, fixed probe `q=kR`, and fixed
mode `nu` with `A_nu(q)>0`. The single-mode susceptibility is therefore a
positive constant across the chosen mass family,
`chi=chi_nu(q)=A_nu(q)R^3/G`. The target parameters `p_sat,a` are positive;
here `a` is the reduced-field scale in the target weight, rather than the
dark mass fraction used in the common-profile equilibrium notation.

| Implication | Dependency | Outcome |
|---|---|---|
| Common-profile family → `omega^2=c GM/R^3` and mass-independent chi at fixed q,nu | stated TF mode/source scaling in `modes/SHARED_MODES.md` | passed within that family |
| Actual source-conjugate oscillator → `d^2=hbar chi omega/2` | canonical oscillator normalization | passed |
| Reduced gap definition → `d=chi Delta` and `M=B Delta^4` | direct algebra | passed |
| One object counted once with `w=n d` → number/mass moments | change of variables / counting convention | passed |
| Target w → exact antiderivative and quadratic ultraviolet mass cost | elementary integral | passed |
| Target density pushed to M → soft and hard exponents | positive monotone mass map | passed |
| Long-wavelength packing claim → stated odd probe and independent separated objects | explicit source/population restriction | passed within that restriction |
| Harmonic oscillator → independently saturating two-level site | not established; explicitly hypothetical | conditional identification, not claimed proved |
| This mass-budget failure → exclusion of every original-model phase | no such implication asserted | out of scope |

The fixed-mode family must exclude the common translation (`c=0`) and the
compensated composition modes (`A=0`). It also excludes probe nodes with
zero overlap for the selected mode. These are excluded by the stated
positive c and A hypotheses, before division by chi is used.

## Restored hbar and the mass–gap map

For one canonical harmonic mode with linear source
`D=c_src q_mode`,

\[
 d^2={\hbar c_{\rm src}^2\over2\omega},\qquad
 \chi={c_{\rm src}^2\over\omega^2}
      ={2d^2\over\hbar\omega}.
\]

Thus the raw file's `d^2=(hbar/2)chi omega` is correct. With its reduced gap
`Delta=hbar omega/(2d)`, positivity gives

\[
 d=\chi\Delta,\qquad
 \omega={2\chi\Delta^2\over\hbar},\qquad
 M=\mathcal B\Delta^4,\quad
 \mathcal B={4\chi^2R^3\over\hbar^2 c_\nu G}>0.                 \tag{R1}
\]

There is no missing hbar in (R1). The powers `d~M^(1/4)`,
`Delta~M^(1/4)` and `d/M~M^(-3/4)` follow. The last ratio is a
source-weighted zero-point displacement scale; it is not a claim that an
object's geometric radius changes by this amount in every mode. The raw
note correctly distinguishes it from fixed R.

## Object count, exact mass integral and the mass-distribution pushforward

Counting the chosen mode once per object gives `n=w/(chi Delta)`. Therefore

\[
 N=\chi^{-1}\int_0^\infty{w\over\Delta}\,d\Delta,
 \qquad
 \rho_{\rm obj}={\mathcal B\over\chi}
                     \int_0^\infty\Delta^3w\,d\Delta.           \tag{R2}
\]

For `w=p_sat a Delta/(a^2+Delta^2)^(3/2)`,
`n=p_sat a/[chi(a^2+Delta^2)^(3/2)]`; its integral is exactly
`N=p_sat/(chi a)`. The number is finite at both endpoints.

Let

\[
 F(L)={L\sqrt{L^2+a^2}\over2}
       +{a^2L\over\sqrt{L^2+a^2}}
       -{3a^2\over2}\operatorname{asinh}(L/a).
\]

Direct differentiation gives `F'(L)=L^4/(L^2+a^2)^(3/2)` and `F(0)=0`.
This proves the exact formula (4) in the raw note. In particular,

\[
 \int_0^L\Delta^3w\,d\Delta
 ={p_{\rm sat}a\over2}L^2
   -{3p_{\rm sat}a^3\over2}\log(2L/a)
   +{5p_{\rm sat}a^3\over4}+O(L^{-2}).                        \tag{R3}
\]

The leading mass cost is therefore
`rho_obj(L)~[2 chi R^3 p_sat a/(hbar^2 c_nu G)] L^2`. This is quadratic
in the *reduced-gap cutoff*. Since `M_max=B L^4`, the same divergence is
proportional to `sqrt(M_max)` when expressed through a mass cutoff; the two
descriptions agree.

The full mass-distribution change of variables is

\[
 n_M(M)=n(\Delta(M)){d\Delta\over dM}
 ={p_{\rm sat}a\over
  4\chi\mathcal B^{1/4}M^{3/4}
        [a^2+(M/\mathcal B)^{1/2}]^{3/2}},\qquad M>0.             \tag{R4}
\]

Consequently,

\[
 n_M(M)\sim{p_{\rm sat}\over4\chi a^2\mathcal B^{1/4}}M^{-3/4}
 \quad(M\downarrow0),
\]
\[
 n_M(M)\sim{p_{\rm sat}a\mathcal B^{1/2}\over4\chi}M^{-3/2}
 \quad(M\to\infty).                                           \tag{R5}
\]

Both number tails are integrable, while `int M n_M dM` diverges at the
hard end. The formal soft and hard asymptotic labels are necessary: the
underlying TF/NR/source-elimination assumptions do not remain physically
valid as M tends to either endpoint. The raw note explicitly retains finite
physical cutoffs rather than asserting a physical all-mass family.

## Source, packing and interpretation

The final raw file now identifies the actual odd probe beside (1). After
COM removal its leading nonzero internal piece is proportional to
`k^2 z^3`. Thus its source matrix elements are `O((kR)^2)` relative to the
geometric scale, and each contributing positive mode's susceptibility is
`O((kR)^4)` or smaller. This statement is valid for that source. Even
plane-wave or tidal channels may have a different leading power; the final
wording explicitly preserves that distinction.

For an independent population of identical objects in the chosen mode,
`chi_eff=nu_objects chi`. Hence the target requires
`nu_objects R^3=1/(4 pi A_nu)`, exactly as in (5). A separated population
has geometric filling `f=(4 pi/3)nu_objects R^3<=1`. The complete odd-source
mode sum gives `4 pi G chi_eff=3 C f(kR)^4+...`; in its controlled small-kR
regime it cannot equal unity. This is a conditional packing conclusion for
separate objects. It does not replicate a shared baryon reservoir for each
mode or make a claim about a dense correlated phase.

The main source/state distinction is also respected. A harmonic oscillator
has a full ladder and an occupation-independent linear commutator response.
Its first matrix element and gap do not make it a saturating two-level
object. Equations (R1)–(R5) test a proposed one-mode-per-object identification
with the target inventory; they do not establish that identification. Counting
many transitions of one object as independent full-mass hosts would invalidate
the population premise, rather than remove its mass cost. Multiple modes
require their shared source Hamiltonian and actual state weights.

## Remaining obligations and review provenance

No algebraic, endpoint or normalization gap remains in the final conditional
dictionary. The remaining physical obligations are exactly the ones stated
in the raw note: formation-selected inventories, EFT-valid objects and probe,
actual occupations, control of nonlinear mode mixing/deformation or escape,
and a mechanism for genuine saturation. The finite-mass conclusion does not
exclude multimode, dense, non-TF or correlated states.

I read the raw dictionary, its referenced finite-wavelength source definition
and the relevant mode/occupation conventions, then reconstructed the
oscillator normalization, positive mass-map Jacobian, endpoint powers and
cutoff antiderivative directly. No scientific script, eigenproblem or
parameter scan was run. No external theorem or new literature citation is
needed for these algebraic implications. The pre-existing `ARTIFACTS.json`
was preserved; the new review and final raw-source hash are pinned separately.
