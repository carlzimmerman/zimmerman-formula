# Independent raw-action review: radiation-density completion

Raw derivation completed before the author's REPORT was available. This note will pin and assess the final report/script once the author freezes them. I did not execute or edit author inputs or radiation_schur_bound inputs. The following is an independent mathematical reconstruction, not a verdict inferred from a test count.

## Covariant square and actual fluid coordinate

Take bare radiation P(Y)=C Y², Y=−∂χ·∂χ/2, hence ρ_r=2Y P_Y−P=3C Y². With v_r=δχ/χdot, actual χdot∝a^−1 gives s_r=v_rdot−Hv_r. On homogeneous background δY=2Y(s_r−ν), so δρ_r=4ρ_r(s_r−ν), not 2ρ_r(s_r−ν). Define a fixed covariant function B(ρ_r) matching X=q²/2 along the selected monotone-density history, and ΔK=Z(ρ_r)[X−B(ρ_r)]²/2. On that history ΔK and both first derivatives vanish; derivatives of those first derivatives along the trajectory also vanish. Clock, radiation and metric background equations remain unchanged. Off trajectory this couples the clock to the ideal radiation scalar; separately conserved *bare* radiation stress is not a generic property of the changed theory.

Set b_r=4ρ_r B_ρ/q² and ΔΣ=Zq⁴/2. Unitary clock gauge gives

δ[X−B]=−q²[(1−b_r)ν+b_r s_r],
ΔL₂/a³=ΔΣ[(1−b_r)ν+b_r s_r]².

Since ρ_r∝a^−4 and q/q*=a³(h−1)/j,

b_r=−d ln q/d ln a=−[3+h_(ln a)/(h−1)].

This is a history-derived profile, rather than an independently selected coupling. A density-dependent Z has no extra quadratic contribution from its own first variation because the square vanishes on the background. Neither this ideal P(Y) fluid nor its derivative coupling automatically supplies real photon/Maxwell behavior.

## Constraints and kinetic capacity

The added square has no linear shift variable on the homogeneous background. Differentiating the unreduced action with respect to scalar shift therefore leaves

ν=d ζdot+e_d v_d+e_r v_r,
d=M/Θ, e_d=ρ_d/(2Θ), e_r=R_r/(2Θ), R_r=4ρ_r/3.

The lapse equation still determines shift through −2Θ provided Θ≠0. Dust remains π(v_d dot−ν); its canonical pair is not silently removed. Write u=s_r−ν. Ignoring lower-derivative terms *only to compute the velocity Hessian*, the two regular-fluid velocities give

L_vel=A_old ζdot²+C_r u²+ΔΣ(d ζdot+b_r u)²,
C_r=3R_r/2>0.

Thus

K_clock=A_old+ΔΣ d² C_r/(C_r+ΔΣ b_r²),
det K=C_r A_old+ΔΣ(A_old b_r²+C_r d²).

Where A_old<0 and b_r≠0, a finite positive lift exists iff C_r d²+A_old b_r²>0; the gain saturates at C_r d²/b_r². Equality gives only a zero asymptotic limit, not a positive finite lift. At b_r=0 the gain is unsaturated and the division-by-b_r formula is not applicable. A conditional designer construction is accepted only if the required strict capacity margin holds at every epoch concerned. This does not contradict root's independent radiation capacity obstruction for other histories. A homogeneous chosen-history square does not establish vacuum self-adjustment or a MOND-source branch.

## Principal characteristic reconstructed without a frozen-IR inference

For a finite background epoch, κ>0 and k/a=p→∞, use point coordinates w_d=v_d−dζ and w_r=v_r−dζ. Their time derivatives acquire only lower-order background derivatives. The acceleration term gives κM d²p² ζdot²; the radiation diagonal velocity coefficient is C_r+ΔΣ b_r². The dust pair supplies the canonical ω² factor. Direct leading-block elimination gives the p⁸ coefficient of the four-coordinate Euler determinant (ω=px):

−2κM³ x⁴[2(C_r+ΔΣ b_r²)x²−R_r]/Θ².

Consequently the nonzero principal acoustic pair has

c_r²=R_r/[2(C_r+ΔΣ b_r²)]>0.

For ΔΣ>0 it is at most the bare 1/3. The four x=0 roots cannot be classified from this determinant coefficient: they describe branches with ω/p→0. A frozen calculation of those roots at ω=O(H) is not controlled, because omitted coefficient evolution and cosmic friction are of the same order. κ=0, degenerate Θ, or a coefficient diverging in a joint epoch/momentum limit require a different principal analysis.

## Evolving high-p slow sector and ordered late limit

Rescale π=p² P. Since (a³p²)dot=H a³p² for a fixed comoving k, the leading slow action has volume a³p², not a³. With ν=dζdot+e_dv_d+e_rv_r its Lagrangian divided by that volume is

L_s=Mκν²+Mζ²+2Mνζ−ρ_d v_d²/2−R_r v_r²/2+P(v_d dot−ν).

Define ℛ=2Mκν+2Mζ−P. Direct Euler variation yields

ζdot=(ν−e_dv_d−e_rv_r)/d,
v_d dot=ν,
Pdot+HP=e_dℛ−ρ_dv_d,
ℛdot+(H+d_dot/d)ℛ=2M(ζ+ν)/d,
v_r=ℛ/(2Θ).

The last equation is the leading algebraic radiation constraint, taken at positive finite R_r before the late-background limit. It is not obtained by declaring zero radiation first. In the late background H→H*, d→1/[H*(1−η)], ρ_d,R_r→0 and

ν=(ℛ−2Mζ+P)/(2κM).

The state (ζ,v_d,P,ℛ) has characteristic

λ(λ+H*)[λ²+H*λ+η(1−η)H*²/κ].

I independently computed this matrix determinant. For κ=1 the rates are 0, −H*, −ηH*, −(1−η)H*. For κ>0, 0<η<1 both clock roots have negative real part even when they are complex. This calculation retains expansion and is distinct from a frozen-frequency test. It is an **ordered high-p slow-sector followed by late-background limit**, not the t→∞ evolution of any fixed finite comoving mode: p redshifts to zero, and such a mode eventually leaves the high-p approximation. Finite-p/full-IR growth and clock/fluid transfer remain unresolved.

## Provisional mathematical assessment

The raw square, fluid normalization, unchanged shift constraint, finite kinetic capacity, p⁸ principal coefficient and evolving slow-limit equations agree with the current script. No mathematical defect was found in these restricted identities. A final acceptance and evidence freshness assessment awaits the durable author report and frozen script. Positive acoustic characteristics and a conditional clock lift are not full same-action cosmological/source health, real-photon completion, or a 32π selector.

## Final mathematical acceptance

The final author report and script were inspected after the ordered-limit clarification and the general-κ characteristic were added. Their restricted claims agree with the independent derivation above. Accepted under the stated finite-epoch, nonzero-Θ, positive-radiation and conditional-capacity assumptions; no blocking mathematical correction remains. Exact source pins:

- `REPORT.md` SHA256 `f423e49bc32465a4f6db0432038f8a1959239873eadc22d9b1f4fbe3cca35d66`.
- `checks.py` SHA256 `c5e282b8d40d58af7795bf08ad046932c392478045c66ec528488b2b93deb68b`.

The author reports a-runs archived as superseded by changed inputs and is producing fresh b-runs. This note does not treat old manifests as current or substitute validation for the derivation. The mathematical acceptance does not depend on the illustrative frozen numerical roots.

Final evidence audit: independently validated main_b and all three current b-controls with --root repository. Current main passes all 27 assertions; controls fail their intended wrong-square/profile/dust-instability assertions. All four manifests have current input/output hashes. Historical a-runs remain superseded.
