# Exact flowing-clock spherical ADM system and a formal MOND branch

## Result and status

The exact stationary spherical equations do not reproduce the aligned zero-flow obstruction: the clock flow supplies a real additional term in the momentum constraint. A formal weak-field deep-MOND profile with nonzero clock flow can satisfy that constraint exactly and approximate the other equations on a bounded radial interval. Its physical circular speed is approximately constant. The result is constructive at the level of an asymptotic candidate, not a matched solution.

This report supplies the full unfixed-radius reduced action, exact lapse/radial/shift equations, the lost-angular Noether identity, the stationary scalar-current identity and an executable first-order exterior system. Bounded outward numerical attempts did not reach their target: all explicit cases and a guarded implicit representative hit evaluation/resource limits. Cosmological boundary matching and source-interior matching remain unresolved. No coefficient is selected and no finite-gradient health is established.

## Same action and radial reduction before gauge fixing

Use signature (−+++), physical matter metric g, Einstein coefficient K_E>0 and φ=qt, q>0. Let c>0, H*>0, b=2c/(3H*), η=c/(3K_EH*²)=−z∈(0,1). With X=−∂φ²/2>0,

K(X)=−c ln(X/Xref), G(X)=−√2 c/(3H*) X^{−1/2},
Lresp=U(g)=−2K_E[W(g;A)−g²/2], A>0 fixed,
W(g;A)=½[g√(g²+A²/4)+(A²/4)asinh(2g/A)]−Ag/2.

Keep an independent areal function R(r) in

ds²=−N²dt²+B²(dr+Vdt)²+R²dΩ².

The unit normal clock has acceleration g=|N′|/(NB) and expansion θ=−[V′+(B′/B)V+2(R′/R)V]/N. Its radial and angular extrinsic eigenvalues are −D/N, −E/N, where D=V′+(B′/B)V and E=VR′/R. Hence KijKij−θ²=−(4DE+2E²)/N². The three-curvature is 2[1−R′²/B²−2RR″/B²+2RR′B′/B³]/R².

Before imposing R=r or eliminating any field, integrate the spatial-curvature and braid divergences with fixed boundary data/compactly supported variations. The action per 4π and coordinate time is ∫dr L, with

L=K_E[NB+NR′²/B+2N′RR′/B−(B/N)(2RR′VD+R′²V²)]
+NBR²[2c ln N−Veff+U(g)]−bBR²VN′/N,
Veff=ρv+c ln[q²/(2Xref)].

The omitted spatial boundary pieces are −2K_E NRR′/B and bBR²V ln N (the time/surface divergences from the original braid are also held fixed). Variations at a horizon or freely varying boundary require an explicit boundary action, not an automatic reuse of this reduced variational prescription. On the normalized flat-slicing vacuum branch Veff=3K_EH*², N=B=1, V=−H*r.

Dimensions in c_light=ℏ=1 are [K_E]=mass², [c,Veff]=mass^4, [b]=mass³, [H*,A,g]=mass. N,B,V are dimensionless, r,R lengths, [q]=mass² when [φ]=mass. A/H* is left free. The fixed-A response is independent of the ADM shift; this is a statement about the exact covariant normal acceleration, not an approximation identifying it with the physical Killing force.

## Exact variations and angular consistency

Write E_N=δL/δN etc, with the Euler convention ∂L/∂f−d(∂L/∂f′)/dr. First vary R as well as N,B,V. The general momentum equation is

E_V=(2K_E BRR′V/N)[R″/R′−B′/B−N′/N]−bBR²N′/N=0.

The undivided Euler expression extends across R′=0; formulas below use an areal region R′≠0. After these variations set R=r. Up to the further boundary −K_E BrV²/N, an equivalent first-order areal action is

L_areal=K_E[N(B+1/B)+2rN′/B−rV²(B′/N+BN′/N²)]
+NBr²S−bBr²VN′/N,
S=2c ln N−Veff+U(g).

On a local N′>0 branch let g=N′/(NB), U_g=dU/dg. For negative N′, replace U_g in a lapse derivative by the signed derivative of U(|N′|/(NB)); U−gU_g retains its positive-g meaning. The exact areal equations are

E_V=−(Br/N)[2K_E V(B′/B+N′/N)+brN′]=0,

E_B=K_E[N−(N+2rN′)/B²+(V²+2rVV′)/N−2rV²N′/N²]
+Nr²(S−gU_g)−br²VN′/N=0,

E_N=K_E[B−1/B+2rB′/B²+(2BrVV′+2rB′V²+BV²)/N²]
+Br²(S+2c−gU_g)+(b/N)(Br²V)′−(r²U_g)′=0.

The exact radial diffeomorphism identity of the unfixed action is

N′E_N+R′E_R+2V′E_V+VE_V′−BE_B′=0.

Thus the lost angular equation is recovered as E_R=[BE_B′−N′E_N−2V′E_V−VE_V′]/R′. It is not an independent omitted condition once all three exact areal equations hold and the sources obey their conservation equations. This identity was checked before gauge fixing with arbitrary N,B,V,R and a generic response function U, rather than only on an ansatz. Singular areal patches need a different coordinate chart.

## Physical Killing potential and exact necessary relation

For stationary test bodies the relevant norm is F=N²−B²V², not N². In a static patch F>0, a time-coordinate change diagonalizes the metric to

ds²=−F dT²+(N²B²/F)dr²+r²dΩ².

The local circular speed measured relative to static observers is v_c²=rF′/(2F); the proper static acceleration is |F′|/(2NB√F). In weak fields a potential Ψ=(F−1)/2 has metric force Ψ′. These formulas require an actual static patch and circular orbit existence; they do not identify the clock acceleration with the test force.

Combining the exact radial equation with momentum gives, in the vacuum exterior,

NB² E_B−NBV E_V
=K_E[(NB)²−(rF)′]+(NB)²r²(S−gU_g),

so every exact solution obeys

(rF)′=(NB)²[1+(r²/K_E)(2c ln N−Veff+U−gU_g)].

The braid derivative terms cancel in this combination. For the stated P2 response,

U−gU_g=2K_E[gW_g−W−g²/2],
−K_Eg²≤U−gU_g≤0.

The bound follows from gW_g−W=∫₀^g tW_gg(t)dt and 0≤W_gg≤1. This is a exact physical-metric radial constraint. It still contains the lapse/clock profile and therefore does not on its own determine the baryon force.

## Conserved sources and zero stationary scalar charge

The executable integration uses the vacuum exterior. For a static perfect fluid whose four-velocity is the Killing direction ∂t/√F, the matter Euler sources per 4π are

E_N,m=−Br²[N²(ρ+p)/F−p],
E_B,m=Nr²[p+B²V²(ρ+p)/F],
E_V,m=NB³r²V(ρ+p)/F,
E_R,m=2NBRp.

The total equations set E_f+E_f,m=0. Conservation supplies p′=−(ρ+p)F′/(2F), together with an equation of state/interior model. The fluid has nonzero ADM momentum when V≠0, even though it is physically static along the Killing field. Setting that momentum to zero inside such a star would change the source. Static dust with nonconstant F is not a conserved pressureless interior. None of the numerical exterior attempts supplies an interior solution.

For a stationary scalar perturbation δφ=ψ(r) at fixed metric, δg=[NVψ′]′/(qNB). Direct variation, before imposing equations, yields

q j^r=b[N′/B²−3H*V−(V/N)(V′+(B′/B+2/r)V)]
+[V/(Br²)](r²U_g)′.

The first term is the logarithmic KGB current and the second is the exact response current. Independently reconstructing the metric stress gives the identity

qNBr²j^r=−NVE_N+BVE_B−(N²/B²+V²)E_V.

It is checked symbolically for generic U. Therefore full stationary vacuum equations force pointwise j^r=0; there is no independently assignable scalar charge on this ansatz. For conserved static Killing-fluid sources their contribution to this energy-flux combination vanishes, with the same conclusion. This is stronger than merely choosing an integration constant by regularity at the center. An accretion flux, time dependence or counterflow matter changes these premises.

## Formal flowing MOND candidate and quantified residuals

In a near-zone weak-field expansion put N=1+n, B=1+h, V=−H*r+v, and S_v=V²−H*²r². The physical metric force is g_phys≈n′−S_v′/2, while the clock acceleration is approximately n′. The leading momentum equation is h′=[ηH*r/(−V)−1]n′. The leading radial metric equation is 2h−2rn′+(rS_v)′≈0. Keeping the response flux and the rolling braid in the lapse equation gives the formal flux relation r²[g_phys−n′+W_g(n′)+ηH*v]≈m. This relation is asymptotic; the exact equations above remain authoritative when leading terms cancel.

A candidate weak deep-MOND region is

N=(r/r0)^L, B=1+L, V=−ηH*rN,
L²=mA, L>0.

It satisfies the exact momentum equation, not just its leading approximation. The physical circular speed is exactly

v_c²=L−[(1+L)²η²H*²r²]/[1−(1+L)²η²H*²r²].

For H*r small its leading plateau is L, with g_phys≈L/r. The clock acceleration is g=L/[(1+L)r]. The shift flow differs from cosmological V=−H*r by an order-H*r fraction, even though the physical metric remains weak. This is not a perturbative continuation of the same homogeneous clock expansion at fixed radial position.

The profile is not an exact solution. Full lapse/radial residuals and the exact current must be corrected. The angular residual follows from the exact Noether identity: on this exact-momentum candidate E_R=B E_B′−N′E_N. Therefore satisfying momentum alone never supplies the missing angular equation.

Exact symbolic variation and 70-digit residual controls evaluate this profile at K_E=H*=A=1, η=.5, m∈{10^-12,10^-18}, on r∈[10√(m/A),20√(m/A)]. These are only two finite annuli. At m=10^-12, L=10^-6, the integrated lapse residual divided by the proposed source flux 2K_E m is 0.006443; the maximum radial residual divided by K_E N L is 0.000900. At m=10^-18 the corresponding values are 0.007316 and 8.999×10^-7. In both annuli the proposed r²W_g/m differs from one by less than .00981. The persistent approximately one-percent flux defect is expected from using the deep approximation rather than the exact P2 radial profile. Small raw residuals are not an existence theorem or an error bound for a corrected solution; the static system has sensitive fast modes and leading cancellations.

The parameter m is a proposed source integration scale. Defining m=G_N,bare M with G_N,bare=1/(8πK_E) does not prove the full interior supplies that charge. Nor does it prove the operational high-acceleration Newton constant equals that bare coefficient on this branch. If a physical matched force had g²=A G_N,bare M/r², its measured MOND scale would be a0=A G_N,bare/G_N,measured. This normalization must be measured from the same completed solution, not silently replaced by A.

## Executable exact exterior system and bounded continuation attempts

The exact equations can be integrated as four first-order fields N,B,V,P=N′ on a nonzero-flow patch. Momentum gives

B′=B[−P/N−brP/(2K_E V)].

The radial equation gives

V′=N/(2K_ErV){−K_E[N−(N+2rP)/B²+V²/N−2rV²P/N²]
−Nr²(S−gU_g)+br²VP/N}.

Define T=2BrVV′+2rB′V²+BV² and

C_N=K_E[B−1/B+2rB′/B²+T/N²]
+Br²(S+2c−gU_g)+(bBr²/N)[V′+(B′/B)V+2V/r].

Then the lapse equation gives

P′=(NB)/(r²U_gg){C_N−2rU_g+r²U_gg g[P/N+B′/B]}.

For the signed extension used by the code, g=P/(NB) and U_g is the signed derivative; U_gg=2K_E[1−|g|/√(g²+A²/4)]>0 at every finite g. The inverse becomes poorly conditioned at large |g|/A. V=0 is also singular in this chosen elimination and requires a different patch, not a claim of physical singularity. The system uses log radius and y=(ln N,ln B,w=−V/(H*rN),k=rP/N) for numerical scaling. ode.py is an importable copy of the frozen integration formulas.

The first nine-case DOP853 attempt (η=.25,.5,.75, A/H*=.3,1,3, m=10^-12, target H*r=.03) hit the declared CPU cap before completing a scientific output. The guarded rerun preserved all cases: each hit its 3000-RHS evaluation cap after only 0.03–12.7 percent radius advance from its formal initial point. The recorded last values are solver **trial stages**, not certified accepted endpoints or boundary solutions.

A guarded Radau representative at η=.5,A/H*=1 hit 12000 RHS evaluations. Its last trial radius was 1.57837×10^-5 from r0=10^-5, with w=.50355, k=9.95414×10^-7, positive F≈1.000000910, g/A≈.0631 and U_gg≈1.7497K_E. Its independently evaluated qj^r was −7.4×10^-12, small compared with individual current terms but not an exact zero. No complete accepted solution history or cosmological-boundary match is claimed from that stopped solve.

A two-step finite-difference Jacobian of the exact log-radius ODE at the formal initial point gave an agreeing pair −4.34535±98.7057i, an approximately −.04070 eigenvalue and a numerically sensitive near-zero eigenvalue. This diagnoses rapid damped **radial** modes locally and helps explain the costly IVP. It neither proves a global growing shooting mode nor supplies temporal stability. A tuned slow-manifold start, higher-precision/stiff formulation or a genuine boundary solver is a next numerical obligation, rather than extending these capped scans and declaring convergence.

The cosmological boundary requires N=B=1,V=−H*r in a normalized flat-slicing vacuum patch and the corresponding q/ρv relation Veff=3K_EH*². The trial N(r0)=1 with fixed Veff does not satisfy that outer condition automatically. Post-hoc lapse normalization cannot be imposed independently of the clock normalization/vacuum relation. A/H* remains free throughout the attempted scans.

## Provenance and exact next implication

Requested and initially observed HEAD is 07fa64b44891fc87697f53f86812287946481586; provenance.json and each run pin actual inputs. Primary authorized local copies are Bernardo [2101.00965v2](https://arxiv.org/pdf/2101.00965v2) and Kobayashi–Yamaguchi–Yokoyama [1105.5723v2](https://arxiv.org/pdf/1105.5723v2), already authenticated in the prior phase. The reduction/current calculation here is independently derived; no global novelty assertion is made.

Fresh main_b verifies the exact unfixed action identities, Killing relation, de Sitter benchmark, formal-flow momentum and residual controls. Fresh control_momentum_b rejects an omitted braid momentum term; control_metric_b rejects identifying the lapse with the physical Killing potential. Their manifests validate. Historical main_a had a missing N factor in the implemented equation-combination check, which was corrected before main_b; its failed record is retained. The broad integration_a resource failure, guarded integration_b and implicit_a failures are preserved, with their scientific bounds and failure reasons rather than treated as passing solutions. Manifest validity authenticates a record, not successful matching.

The remaining arrow is an exact conserved interior and cosmological exterior joined to a healthy flowing-clock radial solution, with physical G_N and a0 calibrated from that same metric. The formal candidate shows that nonzero flow can evade the simplest static obstruction and produce the right radial scaling. The exact constraints and bounded attempts do not yet establish existence, source normalization, finite-gradient health or selection of A/H*. Those are the present open obligations.
