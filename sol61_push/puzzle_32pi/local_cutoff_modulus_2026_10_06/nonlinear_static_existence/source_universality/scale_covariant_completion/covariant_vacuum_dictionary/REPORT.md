# Auxiliary cutoff in a concrete BIMOND vacuum/source dictionary

## Primary action and scope
Milgrom's Bimetric MOND gravity, arXiv:0912.0790v2, equations (1)–(3), (13), (15), (24), (84)–(87), is read from the authenticated project-local PDF/text (hashes in sources.json). Its curvature/Einstein-tensor signs are those of that paper. Vacuum Λ below is the positive coefficient of the physical Einstein vacuum equation in conventional notation; restore units as Λc⁴/a0². The proposed T and potential are our diagnostic addition, not a result attributed to Milgrom.

In c=1 units write the covariant action in the paper's conventions

S=−K∫[β√g R+α√ĝ Rhat−2(gĝ)^(1/4) f(k) χ_n a0² M(z,T)]d^(n+1)x+S_m[g]+S_hat[ĝ],
K=1/(16πG_EH), k=(g/ĝ)^(1/4), f(1)=1,
z=−Υ/(2χ_n a0²), χ_n=(n−1)/(2(n−2)), n≥3,
Define U_(μν)=C^α_(μλ)C^λ_(να)−C^α_(μν)C^λ_(αλ), C=Γ−Γhat. The direct opposite-sign lift uses the primary Υ_g=g^(μν)U_(μν). The exchange-symmetric repair uses a different explicitly specified invariant Υ_sym=(g^(μν)+ĝ^(μν))U_(μν)/2 in z. U_(μν) is even under C→−C, so Υ_sym is invariant under exchanging the two metrics; Υ_g alone is not. This action change is essential, not merely a volume-factor convention.

In n=3, χ_n=1 and the direct lift uses the primary action's chosen invariant. The symmetric lift is our explicit averaged-contraction variant, within the paper's allowance for different scalar contractions; it is not attributed as the exact primary example. The general-n extension and normalization here are explicitly derived, not asserted to have been studied in that paper. T is an auxiliary dimensionless scalar with no kinetic term and λ>0. Matter couples minimally to g; there is no direct T source or imposed force law. The chosen scalar gives the standard NR scalar branch locally, subject to its spatial-metric equations; a global relativistic existence/health theorem is not supplied.

The Newton normalization is ΔΦN=Ω Gnρ, with
Gn=8π(n−2)G_EH/[(n−1)Ω].

For the weak static scalar metrics g00=−1−2φ and gij=(1−2φ/(n−2))δij, and their hatted partners, the difference connections have C^0_(0i)=∂iφ*, C^i_(00)=∂iφ*, C^i_(jk)=−(δik∂jφ*+δij∂kφ*−δjk∂iφ*)/(n−2). Their contraction yields Υ=−(n−1)|∇φ*|²/(n−2), so z=|∇φ*|²/a0². The primary paper proves the four-dimensional spatial-metric reduction also for general α,β in equations (70)–(77). For the general-n extension one can check branch compatibility directly: adding an independent spatial perturbation H_ij gives δCbar_i=∂jH_ij−(1/2)∂iH_jj and background Ctrace_i=−2∂iφ*/(n−2). The cross term from g^(μν)C^α_(μλ)C^λ_(να) equals −2∂iφ*∂jH_ij/(n−2)+∂iφ*∂iH_jj/(n−2), exactly canceled by the −Cbar_i Ctrace_i term. Thus Υ has no φ*–H bilinear, and H_ij=0 solves the interaction spatial equations on this NR scalar branch, including spatially varying M_z(T). This establishes branch compatibility, not uniqueness or full constraint health. The EH scalar coefficient is 1/(2ΩGn); the interaction coefficient 2Kχ_n a0² equals κ=a0²/(2ΩGn). Hence the actual NR action is

L_NR=−[β|∇φ|²+α|∇φhat|²−a0²M(|∇φ*|²/a0²,T)]/(2ΩGn)−ρφ.

These equations are the required source-to-invariant dictionary, not an identification of a momentum spectral variable with acceleration.

## Direct same-source lift: an actual vacuum obstruction
For β=1, α=−1, φ*=φ−φhat is exactly Newtonian and ν=1+M_z. Set

M(z,T)=q(√z,T)−λT²/2−A,
q=2∫_0^y t b(t)/(1+(t/T)²)dt, b=√(1+1/t)−1.

The NR transformation gives exactly the frozen auxiliary action, apart from the constant A: −[2∇φ·∇φ*−|∇φ*|²−a0²M]/(2ΩGn). Its T equation is q_T=λT, and its source branch is unchanged by A.

However, coincident empty cosmological metrics cannot support nonzero A in this class. At C=0, the T equation gives T=0, and M(0,0)=−A. Let qv=(1+f'(1))/2 and qhat_v=(1−f'(1))/2, so qv+qhat_v=1. The two metric equations (the general-n extension of primary equation84) require, up to the common curvature sign convention,

βG_(μν)+χ_n a0² qv M0 g_(μν)=0,
αG_(μν)+χ_n a0² qhat_v M0 g_(μν)=0.

For β=1, α=−1 their sum requires χ_n a0²M0=0. No choice of f'(1) removes this condition. Therefore A=0 and Λ=0 for an empty coincident-metric solution in this exact direct lift. An added twin vacuum stress or unequal cosmological metrics would change the premise and require a new solution; they are not silently included. The action's opposite-sign sector also precludes borrowing full-action positivity from the reduced NR test.

The same-source UV normalization is not compatible with that vacuum branch: the frozen auxiliary envelope qeff=q−λT(y)²/2 satisfies qeff(0)=0, qeff_y=2y(ν−1), qeff(∞)=2Cresp. Setting M_eff(∞)=0 chooses A=2Cresp>0, contradicting A=0. Thus importing the finite moment into Λ fails at a specific second metric equation, rather than merely because an offset is generally free.

## Exchange-symmetric repair: exact local NR reconstruction
For the repair choose α=β=1, the invariant Υ_sym just defined, and f(k)=f(1/k). This makes the gravitational action exchange invariant: the EH terms exchange, the mixed volume is invariant, k→1/k, and U is even in C. Identical matter-sector functionals can also be exchanged, although an ordinary source in only one sector breaks the solution symmetry. At leading weak NR order both inverse metrics in Υ_sym equal η, so its NR scalar action and spatial-variation cancellations coincide with the primary Υ_g reduction. At coincident metrics its first variation likewise coincides, since U=0 and δU=0 there. These agreements do not equate the two full actions away those limits. For zero twin matter the full NR equations are div[(1−2m)∇φ*]=ΩGnρ and Δφ=ΩGnρ+div[m∇φ*]. They do not identify (1−2m)∇φ* with the Newtonian gradient for a general nonspherical source: their divergences agree, but the weighted star field need not be curl-free. In spherical symmetry, regular-center flux integration yields the aligned scalar relations

y=(1−2m)x, g/a0=(1−m)x, m=M_z, x=|∇φ*|/a0.

The linear map M_z=ν−1 is now wrong. To recover precisely the same spherical auxiliary constitutive law, let e(y,T)=b(y)/(1+(y/T)²), d=y e, and define parametrically

x=y+2d=y(1+2e),
M(x²,T)=q(y,T)+2d²−λT²/2−A.

At fixed T, M_y=2d x_y, so M_z=d/x=e/(1+2e). These are exactly the symmetric spherical source flux equations, giving g/a0=y(1+e). Here the parametric y equals the actual Newton acceleration only on this radial branch; for a generic source it is an interaction-coordinate parameter. Crucially, at fixed invariant x the T derivative is

M_T|x=q_T+4d d_T−(M_y/x_y)x_T−λT=q_T−λT.

Thus T variation preserves the auxiliary stationarity at the parametric y; on the radial branch this is the actual Newton y. No missing T_y chain term is discarded. The construction does not recover the original QUMOND equations for arbitrary source shapes. The reconstruction is valid where x_y at fixed T is nonzero. On the stationary source branch a sufficient globally admitted interval is 0<λ<5/192. The frozen ellipticity proof improves to D_fixed>1/2 there: for y≤1/8,z≤1/3 it gives D_fixed>1; for y≥1/8,z≤1/3 the negative term is ≤9/25, giving D_fixed≥16/25; for z≥1/3 it gives D_fixed≥1−96λ/5>1/2. Hence x_y=2D_fixed−1>0 everywhere along the source branch. This supplies a local-in-field-space inverse around every finite nonzero source point. It is not a claim that the entire off-shell (z,T) plane has a global invertible parametrization; fixed-T branches can fold outside this admitted neighborhood.

After auxiliary elimination the endpoint identity remains exact. The additional 2y²e² vanishes at both endpoints: it is O(y) in deep MOND and O(y^(−4)) in the UV. Thus

M_eff(0)=−A, M_eff(∞)=2Cresp−A.

The auxiliary vacuum solution is T=0; its positive potential curvature is not an absent vacuum potential curvature. On the source branch m→1/2 at the origin. Since z is quadratic in the connection difference, a bounded limiting m gives zero first interaction-derivative stress at C=0; only the value M0 contributes. This does not make second variations regular or prove full principal health. A chosen extension including (z,T)=(0,0) must retain that first variation; off-shell and negative-z/timelike extensions remain separate obligations.

For this actually exchange-invariant gravitational action, exchange symmetry imposes f(k)=f(1/k), hence f'(1)=0, qv=qhat_v=1/2. Both empty coincident-metric equations then agree and give

Λc⁴/a0²=χ_n A/2.

If, additionally, the strong-field normalization M_eff(∞)=0 is imposed, A=2Cresp and the conditional same-action dictionary is

Λc⁴/a0²=χ_n Cresp(λ), χ_n=(n−1)/(2(n−2)).

It reproduces Cresp in n=3. In an exact de Sitter physical metric, H²=2Λc²/[n(n−1)]. These factors use calibrated Gn versus G_EH; no raw equality of the two force constants is assumed away n=3.

## What is closed and what remains free
This closes a radial vacuum/source normalization leaf conditional on an admissible covariant extension of the symmetric parametric interaction. It does not close the global action leaf: the source reconstruction is only locally single-valued around its admissible static branch, the vacuum is non-C2, negative invariant arguments need a specified continuation, and full metric/auxiliary constraints and health remain unproved. The direct QUMOND lift's coincident-vacuum obstruction is exact without these symmetric-extension assumptions.

Neither vacuum stationarity nor exchange symmetry fixes λ. At C=0 the T equation is simply −λT=0 for every λ>0; symmetry acts on metrics and leaves the scalar potential coefficient invariant. Offsets A change vacuum curvature while leaving the entire NR source/T branch unchanged. Strong-field normalization removes A only by tying it to the free response moment. In the admitted interval the frozen proof establishes a continuous strictly decreasing Cresp(λ), unbounded as λ↓0. Thus even the conditional dictionary leaves a continuum of Λ/a0², without target insertion. Fixing A to zero instead gives a flat coincident vacuum and a nonzero strong-field interaction value; neither convention is a dynamical selector.

The spherical source physical a0 normalization, covariance, vacuum endpoint and exchange symmetry have now been kept in one explicit candidate. The original QUMOND external-field, quadrupole and higher-multipole calculations cannot be transferred to this symmetric action without deriving its distinct nonspherical response. The first unresolved full-theory implication is whether the local parametric reconstruction has an admissible covariant off-shell extension containing the intended vacuum and dynamical source solutions. A healthy extension and an independently fixed λ would be needed before a numerical coefficient could be claimed. No 32π selection is established.

## Evidence and references
sources.json records exact primary URL/version and cached PDF/text hashes. These pre-existing authorized source copies are read only; no new full-paper redistribution is introduced. Restoring https://arxiv.org/pdf/0912.0790v2 and checking the recorded hashes is required to rerun a source audit if the local cache is absent. checks.py explicitly checks evenness in C and exchange invariance of the averaged contraction, and independently contracts raw NR connections for n=3..6, checks normalization for symbolic n, symmetric source and T chain rules, endpoint values and empty-vacuum compatibility. Three controls test transplanting the α=−1 source map, discarding the vacuum offset, and claiming empty coincident vacuum with nonzero opposite-sector interaction. Algebraic checks are not a full covariant solution or a PDE existence test. Frozen hashes and current runs are separate provenance/RUNS artifacts.
