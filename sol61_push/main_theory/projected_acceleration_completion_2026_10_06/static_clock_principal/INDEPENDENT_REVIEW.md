# Independent static-clock principal audit

Verdict: accepted under the stated fixed-metric, stationary zero-shift hypotheses. No blocking mathematical error found. The all-spatial-dimension index derivation establishes the temporal cancellation; the finite matrix computation is corroboration, not its generalization. The leading NR examples establish a local spatial-row discriminator, not a constrained physical instability or a complete covariant source solution.

## Frozen inputs and evidence

- REPORT.md: `53ac413d6dc608648fa3aea7beb3170d398b7f4023b50dbb818087909ea2f1f7`
- checks.py: `eabc2936d9bd32dcff0bb8b1b51c1ae6e846bdbaa454e747ff4190660a3e73f4`
- contract.json: `862b3b76820fd16b25ff9cc17a3dccde09f2c2d5862ca1886c26073b36c7e47d`
- SOURCES.md: `3d9cf4223d3c0c1cb1f69420b3dae28cdae02b93d82df750a8299b732a9dfd64`

Independently validated main_a, control_projector_a, control_wave_a and control_offset_a with validate_manifest.py and the repository root: all four exit zero. Main records 40/40; each mutation 40/41 with its intended additional false assertion. Only this review was written; frozen author inputs and outputs were preserved.

## Covariant reconstruction

For θ=t+επ on g=−N²dt²+γ, set G=γ inverse and n=d ln N. Direct normalization of u=−dθ/sqrt(−g inverse(dθ,dθ)) gives u_0=−N[1+ε²N²G(∂π,∂π)/2] and u_i=−εNπ_i+ε²Nπ_tπ_i. The clock-normal lapse is Nθ=N[1−επ_t+ε²(π_t²+N²G(∂π,∂π)/2)]. Using a=P d ln Nθ reproduces the displayed acceleration components, including universal spatial terms −επ_it and ε²(π_tπ_it+π_iπ_tt). These cancel between the two metrics even when their lapses and spatial metrics differ.

With d=n−h, D=N²G−L²F and B=N²Gn−L²Fh, the remaining relative spatial second coefficient is ∂_i[D(∂π,∂π)]/2+π_i B·∂π, and the relative temporal first coefficient is B·∂π. The time-projector first coefficient is −H∂π. Therefore the invariant contributions 2(Hd·∂π)(B·∂π) and −2(Hd·∂π)(B·∂π) cancel. The temporal-temporal projector cannot contribute at this order because both its background and first coefficient vanish. The surviving spatial projector second coefficient gives half the sum N²(Gd·∂π)²+L²(Fd·∂π)². Together these yield exactly the report's a0² I_2. No π_t, π_tt or π_it remains pointwise, before integration by parts.

Since I_1=0 and the measure is held fixed, only m I_2 enters the quadratic interaction; an M_eff,II term cannot be added. Spatial integration by parts for compact variations gives C=−D div(v m H d)+(v m/2)[N²(Gd)⊗(Gd)+L²(Fd)⊗(Fd)]. In particular div differentiates m, the measure and H; a constant-m replacement is not legitimate on the sourced branch. The resulting pure-clock Euler row is spatial div(C grad π). No temporal boundary assumption was used to erase a kinetic term.

## Actual leading NR source and sign classification

The weak metric dictionary gives N²G−L²F=4χ_n φ* identity at leading order. Thus the fixed-metric pure-clock canonical energy is proportional to 4χ_n φ* div(m grad φ*)|grad π|²−m(grad φ*·grad π)². This is the negative of the stationary pure-clock Lagrangian, not the fully reduced gravitational Hamiltonian.

For the declared n=3 cubic constitutive action, m=1/2−x/8 and y=(1−2m)x=x²/4. The radial solution d=2a0 rM/r has constant star flux r²(1−2m)d=a0rM²=G_N M. Direct differentiation including m'(r) gives J=div(m grad φ*)=d/(2r). The individual gradients φ'=(1−m)d and hatφ'=−md sum to G_N M/r², so the example obeys the declared leading radial source equations rather than merely prescribing a force.

With φ*=2a0rM ln(r/r_ref), the energy eigenvalues are d² times 2l tangentially and 2l−m radially. At x=1/2, m=7/16, the l=−1, 1/8 and 1 examples are respectively negative definite, mixed-sign and positive definite. Either definite sign gives an elliptic spatial row. Degenerate boundaries require separate analysis. A relative potential offset changes these eigenvalues while leaving the leading source gradients unchanged; the NR force equations therefore do not select the clock-row classification.

## Exact scope

The cancellation is a fixed-metric coefficient identity valid for arbitrary admitted clock jets and stationary zero-shift metrics, including off-shell metrics. The local source sign witnesses are only leading weak-field radial solutions on bounded annuli; a global logarithmic geometry or a full covariant source/background admission has not been proved. Strict signs persist only conditional on a sufficiently weak full background with this limit and away from degeneracies.

There is no inference of a physical ghost from a negative pure-clock energy coefficient, no inference of an eliminated degree from missing pure-clock time derivatives, and no import of single-metric khronometric sufficient conditions. Mixed metric-clock terms and lapse/shift/matter constraints can be load-bearing. The remaining physical arrow is the coupled sourced constraint reduction with relative clock normalization and boundary matching; neither cold abundance nor 32π selection follows from this calculation.
