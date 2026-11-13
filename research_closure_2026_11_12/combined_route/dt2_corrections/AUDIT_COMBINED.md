# Independent audit of the combined-route reduction

Audit date: 2026-11-12. Reviewer: HY4 correction agent. Scope: `../DERIVATION.md` sections 1, 4, 5 and 6, and `../combined_constraints.py`. The sources were read and executed without modification by this reviewer.

**Verdict: conditional on named inputs.** The accounting, transport identity, two endpoint growth calculations, positive cold-component equilibrium, and uniform-acceleration cancellation are mathematically sound under the stated assumptions. They do not derive the effective-mass/rest-mass bridge, environment history, radius proxy, formation, stability, or an EFE coupling. One output-label issue identified below was corrected by the author during review; the follow-up hashes are recorded at the end.

## Provenance and computational check

Audited source snapshots (SHA-256):

- `DERIVATION.md`: `0457bdbe19c37e98def4bd698e92880e67dc74ac9cdfe630935f6c1315a58d85`.
- `combined_constraints.py`: `cec93e07ce6ebf7fe721735e47de1726bb8ce90db40517ec874b27f2feb5553a`.
- Repository HEAD at review: `2ffc012fa56dcdcbb4b3d5f169ba757fe482bcb8` (sources include uncommitted work).

Executed from the repository root:

```sh
python3 research_closure_2026_11_12/combined_route/combined_constraints.py /tmp/hy4_combined_audit_result.json
python3 research_closure_2026_11_12/combined_route/dt2_corrections/audit_combined_numeric.py /tmp/hy4_combined_audit_result.json research_closure_2026_11_12/combined_route/dt2_corrections/audit_combined_numeric.json
```

Exit status 0; Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4. The source's finite-difference slope check had maximum absolute error `2.7732e-11`; its Jeans check had maximum relative residual `4.0067e-8`; total cold mass quadrature had relative error zero at displayed precision. The 2,001-point convexity grid had minimum margin `1.72634`. These numerical checks support the implementation on its tested range; the all-radius claim rests on the analytic argument below. The pressure quadrature truncates its logarithmic integration variable at 35 (source lines 68–70); it is a numerical approximation to the infinite integral, not an exact evaluation.

An independent arithmetic check used the equivalent expression `F(x)=atan((1+x)^(-1/2))*(1+x)^(3/2)/x`, the stable positive quadratic root `x=2y/(sqrt(y*y+4y)-y)`, and a direct ratio of the two fold coefficients. It agreed with the exact-history values below to relative error less than `1e-13`. A central finite difference for the exact logarithmic environment rate differed from its analytic value by `6.54e-13`. A separate 1,001-point check of the convexity rational identity differed by at most `8.89e-16`. The numerical evidence is preserved in `audit_combined_numeric.json`; the analytic audit does not rely on the sampled identity as a proof.

## Independent derivations and dependency boundary

### 1. Retention accounting (derivation lines 5–9)

From `B=Fb*Bi` and `C=Fc*R*Bi`, division gives `X=C/B=R*Fc/Fb`. Thus `Fb/Fc=5.41/59.5=0.09092436974789916`. If `Fc<=1`, then `Fb<=0.09092437` and `Bi>=59.5*B/5.41=10.99815157*B`. At least `1-Fb>=0.90907563` of the *specified initial patch's baryons* are outside the chosen final inventory. The same-reservoir/no-external-exchange qualification in the text is essential and correctly stated. The argument does not locate those baryons or predict retention.

### 4. Continuity and environmental response (lines 39–50)

For `C(t)=integral_A(t) rho dV`, Reynolds transport gives `Cdot=integral_A partial_t rho dV + integral_boundary rho*vA.n dA`. Local conservation `partial_t rho+div j=0` and the divergence theorem yield equation (5), including its sign. For positive differentiable `B` and `X(x)=F(x)-1`, imposing `C=B*X` yields `dlnC=dlnB+(dlnX/dlnx)dlnx`. A material boundary has `j=rho*vA` in its normal component and zero flux; fixed mass then requires the asserted compensation. Signed contrast requires its own background-subtracted continuity convention, as the text says.

Writing `w=(1+x)^(-1/2)` gives `F=atan(w)*(1+x)^(3/2)/x`. Its logarithmic derivative reproduces source lines 29–33 and `s(x_late)=-1.001188962853027`. No current or energy equation follows from this derivative. Likewise `rho_pol=-div P`, `j_pol=partial_t P` is a kinematic identity, not a carrier dynamics.

### 5. Endpoint growth and the exact simple-kernel refinement (lines 54–66)

At fixed redshift, `RE=sqrt(G*B/a0)/x` scales as `B^(1/2)/x`, whereas the imported fold radius scales as `B^(1/3)`. Consequently the early/late ratio of `RE/Rfold` scales as `g^(-1/6)`, where `g=B_late/B_early`. If the fixed-mass ratio is `q`, the stipulated upper bound `.56` gives `g>=(q/.56)^6`. Independently, matching cold mass gives `C_late/C_early=g*X_late/X_early`. For fractions referred to one initial reservoir, `Fc_late<=1` then gives `Fc_early<=X_early/(g*X_late)`. The inequality directions are correct.

| Imposed environmental history | Early x | Early X | Fixed-mass proxy ratio | Minimum g | Minimum cold growth | Maximum early Fc |
|---|---:|---:|---:|---:|---:|---:|
| G242 deep scaling | .05824245752 | 13.41557448 | .60870478743 | 1.64934741 | 7.31509270 | .136703668 |
| Exact simple-kernel scalar relation | .05956050557 | 13.11721236 | .59523441551 | 1.44211548 | 6.54147152 | .152870802 |

For the second row, `y=x^2/(1+x)` implies `dlny/dlnx=(2+x)/(1+x)`. With the imposed `y proportional to a^-3`, this gives `dlnx/dlna=-3(1+x)/(2+x)`. Combining with `s` gives the stated fixed-B rate `1.5116184917384519`. Thus the one-kernel comparison is internally consistent and different from the deep approximation. Both numbers are conditional endpoint requirements, not universal accretion bounds. The scalar environment mapping, common progenitor mapping, asymptotic mass bridge, and `Rsettled=RE` remain independent physical assumptions; the imported `.56` proxy is not a computed forest likelihood.

### 6. Positive equilibrium and uniform acceleration (lines 70–92)

Direct differentiation of `C=(2XB/pi)*atan(r/t)` gives `rho=C'/(4*pi*r^2)` exactly as equation (8), and `C(infinity)=XB`. Near zero, `C~(B/rM)*r` and `rho~constant/r^2`; at infinity, `rho~constant/r^4`. The extended baryons have bounded central potential. These asymptotics make cold self-binding energy, cold–baryon interaction energy and total kinetic energy finite; point baryons instead introduce the stated logarithmic interaction divergence. The cold potential itself behaves logarithmically at zero, so the construction is an ideal singular model on `r>0`.

Let `M=B(r)+C(r)`. Since `Psi'=-GM/r^2` and `rho'=-gamma*rho/r`, `d rho/d Psi=gamma*rho*r/(GM)`. Differentiating once more gives

```text
d²rho/dPsi² = gamma*rho*r²/(G²*M²) * (gamma - 1 + pM - eta),
pM = r*M'/M >= 0,  eta = dln(gamma)/dln(r).
```

For `w=(r/t)^2`, `gamma=2(1+2w)/(1+w)` and `eta=2w/[(1+w)(1+2w)]`. Therefore

```text
gamma - 1 - eta = (1+3w+6w²)/[(1+w)(1+2w)] > 0.
```

At infinity the finite total gravitating mass gives `Psi~G*Mtotal/r`; hence `rho~constant*Psi^4` and the Eddington boundary derivative vanishes. The positive second derivative makes the Eddington distribution strictly positive for each finite binding energy `E>0`; the integral converges at both endpoints for every such E. This is a cold-component isotropic equilibrium in its own Newtonian gravity plus the specified extended baryonic potential. It does not itself construct a baryonic distribution function, establish stability, or form the profile dynamically. Its support is infinite; `t` is a finite scale, not an outer boundary. The source already distinguishes a transition radius from a mass boundary and excludes AQUAL equivalence.

The spherical/isotropic inversion formula and relative-potential convention were checked against the [official galpy Eddington documentation](https://docs.galpy.org/en/latest/reference/dfeddington.html), accessed 2026-11-12, displayed version `v1.12.2.dev0`. That page supplies the formula and assumptions, not a proof of this model's convexity. No galpy code was executed; the derivative and endpoint arguments above are independent.

For the uniform-field claim write `f(x,v,t)=F(x-q,v-qdot,t)`. The chain rule gives `partial_t f=partial_t F-qdot.grad_X F-qddot.grad_V F`. The streaming term cancels the first shift, leaving force `-(grad_X Phi_int+g_ext+qddot).grad_V F`. Choosing `qddot=-g_ext(t)` cancels the external field, including its time dependence. Poisson is translation invariant when *all internal gravitating sources and applicable boundaries co-transform*. A pinned baryonic source or fixed external boundary would be an additional force/constraint and is outside this cancellation. The stated ordinary universally gravitating matter comparison is therefore sound; it does not apply unchanged to a theory with an independently specified clock or field coupling.

## Required minimal correction and optional scope clarifications

**Required output-label qualification:** source lines 112, 116 and 120 compute `r=(3C/(4*pi*rho_cold,0))^(1/3)` and call it `minimum_comoving_catchment_Mpc` under only `Fc<=1`. This is a mean-density equivalent radius. A spherical initial patch at overdensity `delta_i` has radius smaller by `(1+delta_i)^(-1/3)` for the same mass; `Fc<=1` alone does not prohibit that. Rename the field to `mean_density_equivalent_comoving_catchment_Mpc`, or explicitly condition the geometric lower bound on a spherical reservoir at the stated mean density. This does not alter the mass-accounting or growth results.

For maximum clarity, the equilibrium statement could explicitly say “cold-component equilibrium in its self-gravity plus the prescribed baryonic profile” and “finite scale with infinite support”; the uniform-field statement could explicitly say that all internal sources/boundaries co-transform. These are scope clarifications, not failures of the displayed calculations.

Dependency chain: same-patch accounting -> imposed effective-excess/rest-mass bridge -> chosen environmental history and radius proxy -> endpoint accretion requirement. Independently, the explicit Newtonian density -> positive Eddington DF proves a limited equilibrium-existence comparison; universal Newtonian coupling -> accelerated-frame cancellation prevents that comparison from supplying a uniform EFE. Neither branch supplies the missing coupling or transport/selection law.

## Follow-up resolution

The author renamed the catchment field to `mean_density_equivalent_comoving_catchment_Mpc` at code line 120 and added the co-transformed-source, prescribed-baryon and infinite-support qualifications at derivation line 96. These resolve the specific label and scope comments above. Follow-up source hashes: derivation `1263b59b110bd3cee5d56e041898abb50f6d9ef8064923cf9b51eea8303652db`; code `532f2ce1f7e181dfaa9c83054dd61738a3aaa2d0cf3ea4c7b87c1e28f8688ba4`. Both commands above were rerun successfully on that revision; the saved JSON corresponds to the follow-up. Line references in the main audit refer to the first pinned snapshots. No audited source file was edited by this reviewer.
