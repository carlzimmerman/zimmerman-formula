# IC27 bridge: action obstruction, explicit expanding branch, and a local matter repair

Initial checkpoint CD26-2: `c8bb508131a7cc72d0cfbb0313c5b79db7189ed2`.
This calculation follows IC20/26/27/28 in
`qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026`.
It changes no existing action file or coefficient table. Full theory **OPEN**.

During this work the shared repository advanced to `9092fc0fd02b904e87c708971335cd63adb18151`, including a changed constitutive target and causality criterion. The calculations below retain their explicitly specified IC action and exponential static primitive. An instantaneous physical response fails the former metric-cone criterion A; it is not automatically a failure under the updated preferred-foliation criterion B. Under B, well-posed evolution, boundary data, stability and constraint control still need proof. No new result below is silently attributed to the changed constitutive target.

The constructive result is a **new fixed analytic IC28 coefficient family** with an exact expanding vacuum solution, positive scalar kinetic coefficient and positive time-dependent restoring coefficient at every wavelength under explicit inequalities. Its generic physical response retains an elliptic tail. A separate, more substantial action deformation that makes the active-pin potential constant admits a local physical linear system with ordinary matter and diagonal wave principal part. Its nonlinear lapse symmetry and pin-off interface remain unresolved.

## 1. Fields and the obstruction in the original IC27 action

The physical clock gives `N=(-g^{-1}(dT,dT))^(-1/2)`, `xi=ln N`, `w=(u-1)xi`, and `S=xi-w`. On the active pin `w=wc`, `S` is the clock lapse coordinate, not an independent matter density. The canonical trace momentum is `q=pi/sqrt(hbar)`. The field `z` is an independently varied nondynamical auxiliary, not a prescribed curvature function or the old exponential coordinate used in earlier IC versions.

IC20/26 has

    v = exp(S+2wc)/2 + z²,
    h = -exp(2S)q²/(6v) - A(S)qz - V(S) - D(S)z² - E4(S)z⁴ - vR,
    V(S) = exp(S)P0(S),
    C_z = exp(2S)q²z/(3v²) - A q - 2(D+R)z - 4E4 z³.

The raw variation gives `partial_R C_z=-2z`. At fixed `S,q,z`, the difference of `C_z` for two curvatures is `-2z(R1-R2)`. Thus `z²exp(-S)=constant>0` cannot solve this auxiliary equation identically for independently varying curvature through choices of **S-only** `A,D,E4`. On a regular implicit branch, `z_R=2z/h_zz` is nonzero for `z!=0`. This addresses action identities, not one selected background trajectory. Matter does not rescue a universal linear combination of the auxiliary equations: the lapse equation contains an independently variable minimally coupled density with unit coefficient, while `C_z` does not. Eliminating that independent density forces its multiplier to vanish; the remaining curvature coefficient remains `-2z`.

A singular auxiliary Hessian does not remove this polynomial obstruction. It invalidates regular elimination and requires a fresh constraint analysis. The result does not exclude changing the curvature coupling or adding an action constraint.

For example, adding a multiplier `lambda[z-Z(S)]` is an actual different action. Its auxiliary Hessian in `(S,z,lambda)` has determinant `-d²h(S,Z(S))/dS²` on `lambda=-h_z`. A regular such holonomic elimination need not add a propagating pair. But for `Z=c exp(S/2)` the resulting trace Hamiltonian is quadratic in `q` with `h_qq=-t/3`: the earlier scalar coefficient `a=t/6+H_qq/2` vanishes. Consequently the regular IC27/28 scalar health results cannot be inherited. This is not a proof that every remaining scalar mode disappears.

## 2. Preserve the stronger IC28 construction

IC28 already makes a genuinely different full-action choice `v=v0=exp(S+2w)/2`, retaining the independent `z` field. On the active pin its raw auxiliary elimination gives

    M_T²=1, c_T²=1,
    H_qR=H_RR=0, H_SR=-v0,
    a = A²/(4D+24E4 z²)>0   when A!=0,D>0,E4>=0.

The IC27 independent physical-potential reconstruction then gives `Phi=Psi` for arbitrary constrained nonzero Fourier data on the homogeneous active pin. There is no assignment of one potential to the other. Setting `v=v0` removes the tensor-normalization fluctuation while retaining the auxiliary response that contributes the scalar kinetic term. This local metric statement does not certify PPN, the pin transition, nonlinear constraints or measured coupling.

## 3. A new explicit fixed-function expanding solution

Use this IC28 full phase action, but set `E4=0`, choose constant `A>0`, and write `v=exp(S+2wc)/2`, `t=exp(2S)/v`. For fixed design parameters `S0,q0<0,m0>0`, define the following ONE function before variation:

    L(S) = -V(S)/q0² + m0(S-S0)²/(2q0²),
    D(S) = A²/[4(t(S)/6-L(S))].

Here `m0` is a lapse-Schur design parameter, not the bare gravitational normalization. On any open interval with `0<L<t/6`, this is a smooth positive coefficient. Varying `z` gives `z=-Aq/(2D)` and the exactly reduced Hamiltonian

    h_red = -L(S)q² - V(S) - v(S)R.

At `S=S0,q=q0,R=0`:

    h_red=0, (h_red)_S=0, (h_red)_SS=-m0,
    Qdot=H=-L0 q0>0, qdot=0, Sdot=0, zdot=0.

Thus `Q=Q_initial+HT` is an exact vacuum expanding solution, with physical proper-time expansion `H/exp(S0+wc)`. The coefficient function is not reconstructed along the solution and is not refitted when sources change. The auxiliary block is regular: `h_zz=-2D<0` and its lapse Schur is `-m0`. A local implicit-function argument permits small source changes where this block stays invertible; the bounded calculation also solves the actual fixed-function constraints for three source amplitudes.

For the inherited IC19 constants, take `wc=-1/40`, `S0=5`, `A=.1` and choose `a=t/6-L` so physical UV speed squared is `.1`. Then set `q0=-sqrt(-V/L)`, `C=-2L' q0=2V'/q0`, and `m0=C(2H-C)/(4a)`. The numerical witness is

    q0 = -3.15114905034856,
    H_coordinate = 163.385476648967,
    H_proper = 1.12875165986120,
    C/H = 1.99928787553455,
    a = .157996424857409,
    D(S0) = .0158231428480501,
    m0 = 60.1382638849416.

The actual activation with `h0=.5` is on its active plateau. These are engineering parameters, not observed values or a new cosmological prediction. Positivity of a finite interval of `D(S)` is not interval-certified; continuity supplies an unspecified neighborhood analytically and the run retains three sample values.

### All-wavelength scalar calculation

Let `p=k²`, with `pdot=-2Hp`, and `M=-m0-2Bp`, `B=2v(1-u²)>0`. The exact quadratic coefficients are

    K=a-C²/(2M), Lmix=2Cvp/M, W=-2vp-8v²p²/M.

Retain the time derivative of mixing when deriving the Euler equation. The result is

    omega² = p v (n0+n1 p+n2 p²)/[(m0+2Bp)(C²+2am0+4aBp)],
    n0=(C²+2am0)[C(2H-C)-2am0],
    n1=8a[BC(3H-C)+C²v+2am0(v-B)],
    n2=16Ba²(2v-B).

The sufficient conditions `a,B,H,m0>0`, `B<v`, `0<C<2H`, and `2am0<C(2H-C)` make all three numerator coefficients positive. `K>0`, and the damping `3H-Kdot/K` is strictly greater than `H`. Its exact difference from `H`, times the positive denominator above, is

    2H[2a(m0+2Bp)²+m0 C²]>0.

The UV physical speed is `2av(2v-B)/(B exp(2S0))=.1`. These are exact conditional statements plus a finite-precision parameter witness, not a nonlinear stability theorem. The homogeneous `p=0` mode is treated through its own regular auxiliary block.

### Static first variations, not merely a Hamiltonian value

On the open pin-off plateau with zero shift and static metric, the varied trace and auxiliary equations are `tq/3+Az=0`, `Aq+2Dz=0`. If `2D>3A²/t`, they force `q=z=0`. The identity

    2D-3A²/t = (12D/t)(t/6-A²/(4D))

links this to `L>0`. On that locus every first variation of the added trace/auxiliary terms vanishes. The independent static action variations in IC30 therefore apply conditionally in any pin-off chart region where the inequality holds: their regular constitutive equation is `u²=1-exp(-|a|/a0)`, and the leading weak-field metric and lapse equations give the stated exponential MOND law with no leading slip under the stated boundary/source approximations. This does **not** show that the local `D` interval reaches a galactic solution, solve the transition, or establish the later changed constitutive target. Off the pin the inequality uses the actual `w`-dependent `t`; its value on the pin alone is not a global bound.

## 4. Physical support: the regular branch has an elliptic tail

Use the actual physical-potential row, not a scalar frequency as a proxy for causality. In vacuum,

    deltaS=(C deltaq-4vp zeta)/(m0+2Bp),
    Psi=-zeta+H deltaq/(2vp), Phi=Psi,
    Psidot=H zeta-(a+H²/(2vp))deltaq+(H-C/2)deltaS.

The background `S` is a physical scalar and is constant, so its perturbation is gauge invariant. The actual evolution in `(zeta,deltaS)` gives

    deltaSdot = Q(p) zeta + R(p) deltaS,
    Q(p)=[2v(C-2H)p-16av²p²/C]/(m0+2Bp),
    R(p)=-H-4avp/C-2Hm0/(m0+2Bp).

The first numerator can be tuned to cancel its Yukawa pole by setting `m0=B C(2H-C)/(4av)`; for the witness this is about `1.20577211`, inside the restoring-sign window. The **second channel remains**, with pole residue `-2Hm0!=0` for every regular expanding `H,m0>0`.

Choose a smooth compactly supported nonnegative bump `f`, and at one time set `zeta=0`, `deltaS=p f`, `deltaq=(m0+2Bp)p f/C`. Here `p=-Delta` in initial barred spatial coordinates. The metric potentials, physical clock shear, shift and canonical data are compact: every inverse `p` in their reconstruction cancels. Outside the support of `f`, polynomial differential terms vanish, whereas

    deltaSdot = (H m0²/B)(m0-2B Delta)^(-1)f,
    Psiddot = (H-C/2)deltaSdot.

The Yukawa Green function is strictly positive away from the source, so this is a genuine nonzero tail. The traceless spatial Hessian of `Phi+Psi` is a physical linear tidal observable; its second time derivative inherits a nonzero tail for generic such data. This is a continuum support argument using the derived operator, not a Lean PDE theorem. It rejects metric-cone support under criterion A. Under updated criterion B it instead identifies the physical elliptic channel whose boundary prescription and well-posed dynamics need explicit treatment.

## 5. Exceptional vacuum branch and its ordinary-matter control

Do not divide away `m0=0`. In that distinct fixed-function candidate `L=-V/q0²`, so

    h_red=V(S)(q²/q0²-1).

Its vacuum homogeneous `q=q0` branch has an exactly degenerate lapse constraint, for every `S`. At the minimum of the inherited `P0`, `P0'(S*)=0`, giving `C=2H`. At every nonzero Fourier mode,

    deltaS=(2v/B)Psi,
    Psidot=-H Psi-a deltaq,
    deltaqdot=-2H deltaq+2v(2v/B-1)p Psi,
    Psiddot+3H Psidot+[2H²+2av(2v/B-1)p]Psi=0.

This is a genuine local vacuum linear metric equation. The `p=0` constraint is degenerate and was not inverted. The homogeneous lapse freedom of this truncation is not a nonlinear field-theory mode count.

For the same fixed function, add positive homogeneous minimally coupled density `rho_H`. On its actual lapse constraint the Schur becomes

    M0 = rho_H (1-V''/V').

At the original potential minimum, `V'=V` and `P0''>0`, so `M0=-rho_H P0''/P0>0`. The run finds `S*=3.93789172117758`, `P0''=.00348433167598589`. For `rho_H=1e-6`, `M0=1.00413004231e-9`, producing an auxiliary pole at `p=M0/(2B)=8.07583569225e-10` and negative low-wave scalar `K≈-6.35e12`. The positive-matter control therefore fails this particular vacuum repair. This is not a universal no-go for changing higher coefficient jets or the action.

A more general jet calculation makes the scope exact. For `h_g=-L(S)q²-V(S)` and `rho_H=e^S rho0(Q)`,

    C_S=-L' q²-V'+rho_H,
    C-2H=-2q(L'-L),
    M0|C_S=0=(L'-L'')q²+V'-V''.

Having `C=2H,M0=0` on an open set of `q`/matter at fixed `S` requires `L'=L`, `L''=L'`, `V''=V'`. A vacuum de Sitter point also requires `V'=V`, hence `P0'=P0''=0`. The original isolated minimum does not satisfy this. On an open `S` interval these conditions integrate to `L=ell exp(S)`, `V=vA exp(S)+vB`; the vacuum de Sitter condition forces `vB=0`.

## 6. A further action deformation: flatten the active-pin potential

This is a new input action, not a result transferred from the original potential. On the active pin choose constant `P0=P_Lambda<0`,

    L(S)=ell exp(S),
    D(S)=A²/[4exp(S)(exp(-2wc)/3-ell)],
    0<ell<exp(-2wc)/3, E4=0.

The reduced bulk Hamiltonian is `exp(S)[-ell q²-P_Lambda-exp(2wc)R/2]`. Homogeneous minimally coupled matter retains the same overall `exp(S)`. Thus `C=2H,M0=0` holds on the actual homogeneous constraint for varying matter. At homogeneous level the primary lapse constraint and Hamiltonian constraint form the reparametrization pair; `k=0` is not assigned a nonzero-mode inverse. With constant background `S=S0`, write `L=ell exp(S0)`, `a=t/6-L`, and `rhoP=rho_H+P_H`. The background obeys `Hdot=-(3/2)L rhoP`.

For one minimally coupled irrotational fluid define the physical variables

    R_p=deltaq-(3/2)j delta_sigma,
    T_B=-R_p/(2vp),
    J_B=j delta_sigma_B,
    Delta=delta_rho_B+3H J_B,
    D_c=Delta/p=2B deltaS-4v Psi.

`D_c` is a local combination of the physical lapse and metric, not an added canonical pair. Using the independently varied matter equations and retaining both `Hdot` and `pdot=-2Hp` gives the following exact local system for nonzero Fourier modes:

    Psidot = -H Psi + 2av p T_B + (3L/2)J_B,
    T_Bdot = -(2v/B-1)Psi - D_c/(2B),
    D_cdot = -H D_c + 6av rhoP T_B - exp(2S0)J_B,
    J_Bdot = -3H J_B + deltaP_B + rhoP Psi,
    delta_rho_B = p D_c - 3H J_B.

For `deltaP_B=w_f delta_rho_B` with `0<w_f<=1`, eliminating `Psi,J_B` (using `2v/B-1>0` and `exp(2S0)>0`) gives diagonal second-order principal terms in `(T_B,D_c)`: coordinate speed squares `2av(2v/B-1)` and `exp(2S0)w_f`. Their physical speed squares are therefore `2av(2v/B-1)/exp(2S0)` and `w_f`. This repairs the linear physical matter pole of the previous candidate; it is stronger than inspecting only the vacuum `Psi` equation. All transformations and principal entries are checked exactly. On a smooth homogeneous interval, positive bounded speeds and bounded lower-order coefficients permit the usual local exterior-energy/Gronwall finite-support argument for this linear system. That analytic PDE argument is not formalized in Lean here. The pressureless limit, nonlinear characteristic problem and arbitrary matter sectors need their own analysis. The existing raw IC23 quadratic Hamiltonian also gives the nonzero-mode momentum form `a deltaq²+[w_f u_f/(2j)]s²+(C deltaq+u_f s)²/(4Bp)`. Hence `a,B>0`, positive fluid enthalpy `u_f j>0` and `w_f>0` make the coupled kinetic matrix positive. This separate sign argument uses the actual lapse elimination `M=-2Bp`; it does not apply the nonzero-mode inverse at `p=0`.

### Why this still is not a nonlinear completion

The actual spatial coefficient remains

    B(S)=exp(S+2wc)(1-u²), u=(S+2wc)/(S+wc),
    B'-B=2wc exp(S+2wc)u/(S+wc)² < 0

on `wc<0,0<u<1`. For periodic or decaying spatial data, the full Hamiltonian `H_total=integral[exp(S)F-B(S)|grad S|²]` and its varied lapse constraint satisfy

    integral C_S - H_total = -integral (B'-B)|grad S|².

Thus the homogeneous lapse-scaling argument does not extend unchanged to the inhomogeneous action. The defect begins at quadratic gradient order. It could alter the zero-mode constraint, fix a formerly arbitrary multiplier, or expose strong coupling; no such verdict follows from this identity alone. A full functional constraint-preservation calculation is the next obligation. Flattening the active-pin potential while restoring the original pin-off primitive would also require a specified transition action, including variations of its switch. No solved interface, global coefficient extension or new empirical prediction is claimed.

### Repair the nonlinear gradient scaling explicitly

One further candidate adds the active-pin Hamiltonian counterterm

    [B_old(S)-b exp(S)]|DS|²,   b>0.

It replaces the gradient coefficient by `B_new=b exp(S)`. It changes the action and its spatial scalar response; none of the old coefficient's nonlinear claims is transferred. After the same auxiliary elimination, write the remaining S-independent Hamiltonian density as `A_field`. Then

    H_total=integral exp(S)[A_field-b|DS|²],
    C_S=exp(S)[A_field+b(|DS|²+2 Delta S)].

For `y=exp(S/2)>0`, the exact identity `|DS|²+2 Delta S=4 Delta y/y` gives

    H_total=integral [A_field y²-4b|Dy|²],
    C_S=y[A_field y+4b Delta y],
    (-4b Delta-A_field)y=0.

Under the same periodic/decaying boundary conditions, `integral C_S=H_total`. This repairs the displayed nonlinear scaling defect. It makes existence of a positive lapse a **spectral constraint on canonical data**, not an automatically invertible auxiliary problem. On a connected compact leaf, an actual positive solution is a zero ground state. Conditional on such a solution, the exact integration-by-parts identity is

    integral [4b|D(yf)|²-A_field(yf)²]
       =4b integral y²|Df|² >= 0.

Consequently the operator kernel is the constant multiples of `y` under the stated connectedness and regularity conditions. Fixing the normalization removes this particular scale freedom. This identity does not produce a positive eigenfunction for arbitrary canonical data; the zero lowest eigenvalue is an additional constraint to preserve. One must still evaluate its Poisson brackets with momentum and Hamiltonian constraints, count local versus global modes, and test the resulting evolution. A minisuperspace count or the isolated eigenvalue identity cannot do that work.

The repaired linear system above remains local after replacing `B` by `b exp(S0)`. Let `beta=exp(2wc)/2` and `a0=1/(6beta)-ell`. Its physical clock speed squared is `2a0 beta(2beta/b-1)`. The explicit choice `ell=a0=1/(12beta)`, `b=beta` gives speed squared `1/6`; `0<w_f<=1` supplies the ordinary-fluid cone. Thus the new gradient repair has a nonempty positive subluminal linear parameter domain. The active-pin potential and gradient modifications both still need a specified variation-consistent interface to the desired static action.

## 7. Reproducibility and certification

`check.py` performs 55 exact symbolic identity checks and deterministic 50/80-digit parameter calculations. The maximum reported relative precision change for the main witness is below `3.3e-48`; this is precision comparison, not interval certification. `contract.json` declares the exact inputs, bounds, exclusions and 110-second wall cap. The accepted bounded run is `run_002/manifest.json` (the earlier `run_001` predates the gradient repair and is development evidence only); all input notes and scripts are hashed and the old research scripts are not executed. The runner uses a cooperative one-thread numerical-library cap, not hard affinity or a memory limit.

`PushSlip20260926.lean` contains 15 scoped curvature, positivity, residue, matter-pole, exceptional local-ODE and positive-lapse jet bridges. `lean_record.json` records the accepted source hash, actual compiler/toolchain, command, output hash, exit code and theorem axiom reports. Failed development logs are retained separately and are not evidence for an accepted certificate. The derivative certificate derives the exceptional second-order local equation from its two first-order equations; it does not assume the second-order conclusion. No Lean statement certifies the action variation, nonlinear Dirac closure or finite PDE support.

For the companion clock agent, `covariant_clock/PushClock20260926.lean` supplies three conditional scalar positivity statements only; its compilation metadata is `clock_lean_record.json` in this directory. These do not certify that agent's field derivation.
