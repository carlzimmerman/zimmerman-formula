# Independent audit: logarithmic braiding plus same-foliation acceleration response

**Primary verdict: proved as written**, for the formal classical vacuum map, the explicitly four-dimensional quadratic de Sitter constraint calculation, and the first-order conserved comoving-dust control. This verdict does not promote any of these statements to a bound-galaxy solution, nonlinear constraint-health proof, or selector for 32π.

Reviewed final current ../cuscuton/log_braiding_extension/REPORT.md SHA256 `234ef41a096b92467f4ba6d4f758ba2e9f4e51fd02de11004dd3bd603622221a` and checks.py SHA256 `a5fd69d3b6384e42826024f8df5dec087f6a192307889408d6cc81dbc48a8e70`. The current execution is `runs/main_b`, not a folder named final_b. Earlier a evidence is historical. Main_b authenticates the current script and exact external inputs; its own report is not a declared execution input, so this independent report hash is the prose-revision locator. This audit reconstructs the equations rather than accepting the author's verdict or number of tests.

## Claim card and dependencies

Objects: X>0, positive scalar rescaling s, minimally coupled matter, logarithmic K and inverse-root G with chosen H*, normalized future-directed clock u; added response −2K_E[W(g_a;A)−g_a²/2], A fixed positive or βθ on θ>0. Cosmological calculation: n=3, positive K_E and H*, q>0 constant, exact de Sitter, −1<z<0, unitary gauge, nonzero invertible Fourier/Laplacian modes. Source: smooth O(ε) dust stress about matter-free de Sitter, δρ=a^-3ρ0, no momentum/pressure at this order, isolated boundary conditions and no homogeneous free scalar waves. Exact homogeneous and zero-mode constraints are not being inferred from the nonzero-mode inversion.

Dependencies are: covariant definitions ⇒ rescaling invariance ⇒ same background; raw Einstein/KGB scalar quadratic action plus acceleration lapse-gradient ⇒ unchanged momentum constraint ⇒ reduced positive coefficients; the specified conserved source and constraint ⇒ boundary source term ⇒ ζ=ν=0 particular branch ⇒ shift potential ⇒ gauge transformation ⇒ physical force. External leaf is the raw Horndeski quadratic action in authorized Kobayashi–Yamaguchi–Yokoyama arXiv:1105.5723v2 eqs. (55)–(64), previously source-verified here. Bernardo2101.00965v2 independently supplies the original KGB branch/stability dictionary. The added response and dust control are internal derivations, not an external theorem being assumed.

## Reconstructed obligations

| Obligation | Result | Reason |
|---|---|---|
| Exact vacuum map | Passed | K(s²X)=K(X)+Δρ and G(s²X)s=G(X); positive s preserves u, hence a,θ and A |
| Full variation of A=βθ | Passed at stated order | W=|a|³/(3A)+higher terms; its A variation starts above quadratic order about a=0 |
| Acceleration operator | Passed | In unitary ADM gauge a_i=∂i ln N, so added quadratic term is +K_E a^-2(∇ν)² |
| Original shift constraint | Passed | No B in that quadratic addition; δS/δB enforces Θν=K_E ζdot on nonzero modes |
| Reduced coefficients | Passed | Elimination and integration by parts give G_S, F_S and positive k² temporal coefficient as stated |
| Source conservation | Passed at first order only | Background divergence of δT vanishes for a^-3ρ0; force-induced velocity/connection terms multiply O(ε) density |
| Gauge/source force | Passed | Ψ=ν+Bdot and Φ=−ζ−HB yield identical potentials and G_N,b/(1+z) |
| Clock acceleration versus metric force | Passed | ν=0 gives a_i=0 although Bdot and −HB are nonzero |
| UV damping and roots | Passed as UV asymptotics | Physical p redshifts; friction tends H, roots Hz and −H(1+z) |
| Bound galaxy, finite-gradient health, selector | Out of scope | Neither quadratic source control nor positive vacuum coefficients closes these implications |

### 1. Vacuum map and response expansion

Under φ→sφ, ∂φ and □φ scale by s while X→s²X. The normalized clock uμ=−∂μφ/√(2X) is unchanged because s>0. Its acceleration and expansion therefore remain identical pointwise. Fixed A and βθ are unchanged, so the response does not break the original vacuum map. This is a map between constant-ρ_v theories and their solutions, not a dynamical phase-transition theorem.

Differentiate W with respect to g: W_g=√(g²+A²/4)−A/2=g²/A+O(g⁴/A³). Hence W=g³/(3A)+O(g⁵/A³), and Lresp=K_Eg²−2K_Eg³/(3A)+… . The exact acceleration-norm response is C² at a=0, sufficient for the claimed quadratic expansion; higher differentiability/finite-gradient principal structure is not thereby established. When A=βθ, a perturbation of A multiplies the cubic-leading W and first contributes beyond quadratic order. Since the background has a=0, the added first variation vanishes, preserving its background equations.

### 2. ADM reduction, with signs retained

Using the stated raw quadratic action and t=ΔB/a², its t-dependent part is −2Θνt+2K_Eζdot t. The added +K_E(∇ν)²/a² has no t, so ν=K_Eζdot/Θ=ζdot/[H(1+z)]. Substitution gives the original cosmological kinetic coefficient G_S=3K_Ez²/(1+z)² and extra K_Ep²/[H²(1+z)²]. The cross term −2K_EνΔζ/a² becomes +2K_E²p²ζζdot/Θ in a Fourier mode. Because a³p²∝a, its time integration changes the gradient coefficient to F_S=K_E²H/Θ−K_E=−K_Ez/(1+z). The response changes the temporal k² coefficient, not this F_S.

Thus A_k=G_S+D p² is positive and F_S>0 throughout −1<z<0. The nonzero Θ hypothesis is indispensable; endpoints cannot be included by continuity. No quadratic νdot is introduced, and the displayed reduction has one scalar degree of freedom. A statement about nonlinear degree-of-freedom counting or finite-gradient characteristics would require more than this quadratic reduction; the report keeps that boundary explicit.

### 3. Conserved source and physical gauge

The first-order dust action is −∫dt d³x a³δρ ν. After the shift constraint it is −∫ρ0 ζdot/[H(1+z)], a time boundary term since H,z and ρ0 are constant in time. This permits ζ=ν=0 after free modes have been set to zero. Varying ν before elimination gives −ΘΔB/a²=δρ/2 at that solution. For Δ=-k²,
B_k=δρ_k/(2Θp²)>0 for positive density. With δρ∝a^-3 and p²∝a^-2, Bdot=−HB.

For ADM g0i=∂iB and spatial metric a²(1+2ζ)δij, the time change T=−B removes the shift (zero spatial shear). Lapse transforms as ν_new=ν−Tdot=ν+Bdot, and curvature as ζ_new=ζ−HT=ζ+HB. With Newtonian spatial potential convention 1−2Φ, this gives Ψ=ν+Bdot and Φ=−ζ−HB. Thus Ψ=Φ=−δρ/[2K_E(1+z)p²], so Δphysical Ψ=δρ/[2K_E(1+z)]. A compact spherical smooth source has the usual inverse-square force with G_N=1/[8πK_E(1+z)]. Meanwhile a_i=∂iν=0 in the original unitary foliation; proper acceleration is covariant, so its vanishing is not erased by changing gauge.

Conservation is strictly perturbative: δρ is O(ε) about vacuum, background dust velocities vanish, and δT momentum or the product of δρ with the first-order metric-force/worldline perturbation is O(ε²). This is not an exact dust configuration pinned to coordinate worldlines: exact fixed-coordinate worldlines with nonzero Ψ would accelerate. Nor is the source a stationary object of fixed physical size. The final report explicitly includes this restriction, resolving the principal conservation concern raised during review. This is a legitimate restricted countercontrol to automatic MOND inheritance, not a universal nonlinear branch theorem.

### 4. Cosmic-time UV dynamics

Since p_dot=−Hp, A_dot=−2HDp². Euler–Lagrange variation gives friction 3H+A_dot/A=H(3G_S+Dp²)/(G_S+Dp²), as stated. For p/H≫1 its limiting equation is ζddot+Hζdot−z(1+z)H²ζ=0. The polynomial factors as (r−Hz)[r+H(1+z)]. Both roots are negative in the open healthy interval. At z=−1/2 a repeated root permits (C1+C2t)e^-Ht/2. The limiting restoring coefficient is −z(1+z)H²≤H²/4. Thus the large physical wave number does not justify treating the mode as a rapidly oscillating static adjustment. Since p redshifts, these roots describe the UV regime over its duration, not the entire future evolution at fixed k. The report makes that distinction.

## Computation and verdict boundary

I read the actual checks, the positive main_b result, and three current b controls. The implemented quadratic polynomial has the raw action's Fourier signs, and its source/gauge check tests the restricted branch above. The source boundary step and gauge transformation require the prose derivation; test agreement alone does not prove them. All four current manifests independently validate against the repository, including input hashes. No peer files or run outputs were edited.

Strongest safe conclusion: the exact vacuum map survives this response operator, and the constrained quadratic vacuum is healthy on the stated interval, but an admissible first-order conserved source still produces a regular metric force with a geodesic clock. The smallest unproved bridge remains the report's stated one: a nonlinear timelike sourced bound-galaxy solution of the same varied action whose clock acceleration gives the physical MOND flux under acceptable boundary/history and finite-gradient constraints. Even that would leave β (or A*/H*) free and would not select 32π.
