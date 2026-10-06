# Physical source dictionary of the projected relative scalar

The finite-wavenumber decaying relative scalar produces an actual pressureless, conserved **signed interaction stress** on coincident de Sitter. Its visible Weyl potential is nonzero. The constant relative scalar produces neither this stress nor Weyl curvature. Neither result supplies a positive homogeneous cold abundance: the exact homogeneous branch instead rescales vacuum stress.

This is a linear source dictionary for the inherited action, not an identification of particles, an early-universe transfer calculation, or a proof of nonlinear health. Base inspected: d2496439d7926ec44c7b2e8b29830a20a9890f61. Input hashes are in provenance.json.

## Action and finite-k constraints

Use signature −+++, K>0, measured tensor coefficient M=2K, three spatial dimensions, coincident empty de Sitter H>0, and Λ=3H². The parent action is

S=K∫(V_g R_g+V_hat R_hat)+2K a0²∫v M_eff(I),
v=√(V_g V_hat), M_eff=−A+I/2−I^(3/2)/12+…, Λ=a0²A/2.

The common clock defines the spatial projector in I. In its unitary ADM chart, I=(γ^{ij}+hatγ^{ij})∂i r∂j r/(2a0²), r=ln(N/L). Hence the interaction is shift independent. The quadratic I term at coincidence is K a(∂ν)², where ν is the relative lapse. Spatial/projector and clock variations of this term start beyond linear stress.

Write γij=a²[(1+2ζ)δij+2∂i∂j E], g0i=∂iβ, lapse 1+ν_g. Relative quantities are z=ζ_g−ζ_hat, ν=ν_g−ν_hat, β=β_g−β_hat, e=−k²(E_g−E_hat), P=k²/a²>0. Set c=Ka³, f=zdot−Hν and D=ν+3z+e. The boundary-corrected parent relative quadratic action is

L/c=−3f²−2f(edot+Pβ)+Pz²+2Pνz+(3/2)H²D²+Pν².

Varying the shift gives f=0. The remaining shear and lapse constraints give

ν=zdot/H, D=0, e=−3z−ν,
β=−edot/P−(z+ν)/H.

The reduced action is L=cP zdot²/H², so zddot+Hzdot=0 and z=z0+z1 exp(−Ht). These constraints use k>0; they do not describe the homogeneous mode.

## Actual metric potentials

For each metric define B=β−a²Edot, Ψ=ν_g+Bdot, Φ=−(ζ_g+HB). These are the Bardeen combinations for the stated spatial-sign convention: a common time shift T sends B→B+T, ζ→ζ−HT and ν_g→ν_g−Tdot. There is only one coordinate freedom; we do not simultaneously put both metrics in Newtonian gauge.

The relative B is β+edot/P=−(z+ν)/H. Therefore Φ_rel=ν and Ψ_rel=−νdot/H. The actual evolution equation νdot=−Hν yields Ψ_rel=Φ_rel=ν. The unsourced common Einstein scalar has vanishing Bardeen potentials at k>0 with the usual empty de-Sitter boundary conditions. Consequently the visible metric has

Φ_g=Ψ_g=W_g=ν/2,

and the hatted metric has their negatives. Here W=(Φ+Ψ)/2 is the lensing potential; its tracefree spatial Hessian divided by a² determines the scalar Weyl curvature. The frozen z0 mode has ν=W=0. This is invisibility of its linear metric curvature, not a declaration that relative clock/foliation data are a gauge symmetry of the nonlinear theory. The decaying mode has W_g∝a^(−1).

## Full interaction stress and its normalization

Define δS_int=(1/2)∫V_g T_g^{μν}δgμν+(hat term)+∫E_θδθ. In particular δS_int/δN=−√γ ρ_g. The constant interaction is −4KΛv. Its **full** stress is T_g,vac=−MΛ(v/V_g)gμν. With q_g=ν_g+3ζ_g+e_g, q_hat similarly, D=q_g−q_hat, the volume ratio is v/V_g=1−D/2+O(perturbation²). Subtracting the matched individual reference vacuum −MΛgμν gives

δρ_g,vol=−MΛD/2, δp_g,vol=+MΛD/2.

The projected gradient action gives δS_I/δN_g=−2Ka Δν, so δρ_g,I=MΔν/a²=−MPν. Its linear momentum, pressure and anisotropic stress vanish. Thus the actual extra stress in each sector is

δρ_g=−M(ΛD/2+Pν), δp_g=MΛD/2,
δq_g=0, δπ_g=0; hatted extra stress is opposite.

Relative density is twice the visible density; losing this factor changes the metric source. On D=0, δρ_g=−MPν and δp_g=0. Independent geometric checks give Y=Φdot+HΨ=0, δρ_Einstein=−2M(PΦ+3HY)=−MPν, and δR_geo=−Pν=(δρ_g−3δp_g)/M. These agree with the varied action rather than defining a dust stress by analogy.

Diagonal covariance supplies V_g∇T_g+V_hat hat∇T_hat=E_θ∂θ (indices suppressed). Individual off-shell interaction conservation is not a symmetry. The linear visible energy residual is

δρdot+3H(δρ+δp)=−MΛ Ddot/2−MP(νdot+Hν),

and the spatial residual is ∂iδp=(MΛ/2)∂iD. The actual constraints and evolution make both zero, consistently with each on-shell Einstein Bianchi identity.

The canonical momentum Π=2cP zdot/H² is conserved. It provides the particularly direct dictionary

δρ_g=−HΠ/a³, W_g=HΠ/(4Kk²a).

This is a signed pressureless integration stress on **zero additional homogeneous density**. Its initial amplitude is free. A nonzero Fourier mode on a periodic box has positive and negative regions and zero spatial mean. More generally the integrated source is a lapse-Laplacian boundary flux; noncompact boundary charges are not ruled out by the periodic example. No positive particle population or homogeneous cold mass has been derived.

## Homogeneous distinction and remaining implication

The separately audited exact homogeneous solution obeys ζ=ζ∞−2 asinh(q)/n and r=nζ∞+2 asinh(q), hence r+nζ=2nζ∞. Its I vanishes, v/V_g=exp(−nζ∞), and the full interaction stress remains pure vacuum, with Λ_g=Λ exp(−nζ∞), Λ_hat=Λ exp(+nζ∞). Its nonzero homogeneous canonical momentum does not turn this vacuum stress into dust.

The reduced quadratic canonical Hamiltonian H_mode=H²Π²/(4Kk²a) scales as a^(−1) and is nonnegative. Identifying H_mode/a³ with physical gravitational backreaction requires second-order metric/background variation; no radiation or matter backreaction law follows from that coordinate Hamiltonian alone. Linear signed density and quadratic canonical energy are different orders in amplitude.

The concrete new implication is a finite-k pressureless gravitational source with conserved mode momentum. Missing arrows are a positive admitted background/abundance, primordial preparation and cosmological transfer, a nonlinear boundary/source completion, and physical health beyond this quadratic branch. Neither a0 nor 32π is selected by this result.

## Evidence scope

checks.py independently reconstructs 32 exact identities, including geometric density/Ricci checks, mode conservation and the homogeneous distinction. Controls substitute raw relative curvature for the actual Bardeen potential, erase the volume response, or halve the source density. The durable derivations above carry the claim; the check count is a bounded algebra audit, not a universal proof. Authoritative run records and input reconciliation are in RUNS.md.
