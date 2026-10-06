# Independent mean-geometry audit and local-clock discrimination

Verdict: the frozen report's **formal homogeneous necessary-row calculation** is correct as scoped. No blocking error in its Bianchi-I response or geometric averaging was found. An additional independent local-clock calculation below shows that the specified nonzero decaying plane seed cannot be completed into a regular order-by-order solution of the retained local action. Thus its mean result must remain conditional; it is not an admitted nonlinear cold background.

## Frozen pins and bounded records

- REPORT.md: `bb60a2bb28979e755778ed5704f504294bd0e5dfb94ff4cef17a17250b5c0eef`
- checks.py: `410321ecaf4bf8e27e873e30e1aa40f162aedeb0436a66b098ca26ab4717d6d8`
- contract.json: `d26db675e706d9b96a153c8e214ce6ce3dd431acc92efba358655224e2d34759`

Independently validated main_a and all three current controls with validate_manifest.py and the repository root: four valid evidence records/exit zero. Main is 21/21, coordinate/omitted-response controls 20/21 and dust control 21/22 with their intended failed candidate. REPORT is excluded from run inputs. Only this review was written; author inputs and outputs were not changed. The new local proof is independent analytic review evidence, not an assertion that the 21-check script tested it.

## Raw homogeneous response and observable

The two plane ADM kinetic terms have cross expansion X[hy A_x+(hx+hy)Zdot], quadratic background coefficient X²(hxhy/2+hy²/4), and shift product −Pβ[hy U+(hx+hy)Z]. These follow directly from −4κxκy−2κy² with the symmetric exponential measure. The spatial/interaction terms give the same Q=(Z+ν)²/2 as the isotropic raw calculation. Directional common length variation must retain hx,hy independently until after Euler differentiation, including time derivatives of their momentum coefficients. It yields exactly ρ=−KH²ν²/2, px=3KH²ν²/2 and py=−KH²ν²/2 on the decay seed.

For mean log lengths Ht+A+2S/3 and Ht+A−S/3, the actual summed Einstein coefficient is 4K. The lapse and shear rows therefore are 24KH Adot=ρ and 4K(Sddot+3HSdot)=px−py. They give Adot=−Hν²/48 and Sdot=H B²a^(−2)/2+(J−HB²/2)a^(−3). The trace row is consistent: −8K Addot−24KH Adot=KH²ν²/6. These reproduce the report's explicit A,S and initial data without replacing the source by the canonical energy.

Independently normalize the preferred normal observable using the actual proper volume. On the decay seed, T=3Z+E=−ν, X=T−ν=−2ν, A_x=Zdot=Hν and Pβ=2Hν. Expanding the weighted Θ numerator gives Hν²/4 at order two, while the proper-volume denominator correction is ν²/16. Thus the expansion correction is (Hν²/4−3Hν²/16)/3=Hν²/48, precisely canceled by Adot. The weighted normal shear correction is −Hν²/2, leaving (J−HB²/2)a^(−3). J=HB²/2 sets it to zero. The initial Ai=−B²/48 normalizes the proper volume, and the coordinate proper-volume rate instead has correction −Hν²/16. This distinction is geometric lapse weighting, not an inconsistency in the mean equations.

## Fresh local clock reconstruction from temporal covariance

This calculation uses a different raw route from a direct acceleration/projector expansion: temporal covariance of the actual unitary ADM interaction, with the full lapse and spatial-metric transformation. It therefore also checks the missing time-projector effects rather than dropping them. Let the first relative lapse be r=εν(t,x) and the first relative contravariant shift be ΔS=εs(t,x), around the coincident flat-slicing de-Sitter pair. A metric Lie deformation with ξ0=T(t,x), keeping the unitary clock fixed for the metric variation, gives

δr=ε[Tνdot−s·grad T]+O(ε²),
δ(v h^{ij})=a(Tdot+HT)δij+O(ε).

The first relation follows from δ ln N=Tdot+T d ln N/dt−S·grad T, with its hatted counterpart: Tdot cancels in the relative lapse. The second includes both the density transformation of v and the inverse-spatial-metric transformation. The quadratic gradient interaction is K a(grad ν)². Its metric variation is consequently

δS_metric,2=K∫a[(Tdot+HT)(gradν)²+2gradν·grad(Tνdot−s·gradT)].

The Tdot, HT and T gradν·gradνdot terms cancel after the time boundary integration. Spatial integration of the shift-gradient term leaves

δS_metric,2=2K∫a[νdot gradν+(Δν)s]·gradT.

Diagonal temporal covariance says this metric variation plus Eθ T vanishes, hence

Eθ,2=2Ka div[νdot gradν+(Δν)s].

For ν=ν_amp(t) cos(kx) and s_x=−kβ(t)sin(kx)/a² this is 2Ka k²ν_amp(Pβ−ν_amp_dot)cos(2kx). The specified decaying mode has β=2Hν_amp/P and ν_amp_dot=−Hν_amp, so

Eθ,2=6Ka Hk²ν_amp² cos(2kx),

nonzero for the nonzero seed, H>0 and k>0. Its torus integral vanishes, exactly as required by the homogeneous clock-relabel identity; that identity cannot erase the nonzero local harmonic.

At coincident background the entire linear clock Euler row vanishes, including its metric-clock mixing, because the quadratic interaction contains no common clock perturbation. Therefore second-order field corrections cannot cancel this fixed order-two compatibility residual. The geometric-mean constant and Einstein pieces have no direct clock variation. The norm-cube remainder contributes only at higher order to this clock row: its M_I correction is O(|ε|), while the common-clock variation of I already starts at ε². Thus the obstruction is unchanged by that retained cubic term despite its lack of a general C3 Taylor expansion.

The conclusion is restricted to a regular perturbative family with bounded field/Euler jets and this first-order plane seed. It is not a theorem excluding every scalar superposition, a nonperturbative sourced branch, extra operators, different backgrounds, or singular/nonuniform expansions. The report explicitly allows the local clock condition to exclude its seed, so this result does not invalidate the correctly derived necessary mean rows. It does prevent treating their solved zero harmonic as a full local admission certificate.

## Physical implication

The mean normal expansion cancellation supplies no positive cold component even before the local test. The latter closes the precise retained-action compatibility arrow for this seed negatively: the signed linear dustlike mode is not by itself regularly assemblable into the tested second-order plane solution. This is a nonlinear admission restriction, not a physical ghost or a universal dark-sector no-go. Cold abundance, primordial/growth transfer, matter-source branches and the 32π selector remain separate obligations.
