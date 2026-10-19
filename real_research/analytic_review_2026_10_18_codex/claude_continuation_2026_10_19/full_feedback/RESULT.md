# Full linear feedback: exact obstruction and conditional resolvent bound

19 October 2026, America/New_York. Checkpoint **ZAR-2026-10-19-09-CL** (continuation by Claude). Parent: **ZAR-2026-10-19-08**. Repository HEAD when this work began: `cbe934afe538b047eb99d2ddc64aed1b46039ce8`. Scope: only the handoff's "Next step", namely a bound on the full coupled linear Vlasov–Poisson feedback on the entire occupied action set, extending the checkpoint-08 bound on the free first term. The work is analytic. The only computation is the symbolic identity check `identity_check.py` in this folder (four algebraic identities, all returning 0). No existing file was modified.

## 0. Verdict

**Outcome (b): the full-feedback bound is not proved unconditionally.** This checkpoint pins down the exact obstruction, gives the weakest closing hypothesis this route can use, and proves a conditional theorem. **All-time confinement remains open, and nothing here says the gravity model is closed.** Nonlinear actual-path and label-gradient control are untouched.

1. **The energy method cannot close the step (proved, B1).** The linearized generator L is skew-adjoint in the conserved coercive energy Q. Its essential spectrum is iΣ, where Σ is the set of all receiving frequencies kΩ_i(q). So the energy-space resolvent has norm 1/dist(λ, σ(L)), which is infinite on the whole receiving-frequency set. The field-work functional is also unbounded on the Q-unit ball at every receiver whose receiving functional has positive continuous spectral density at its own frequency. A uniform work bound therefore needs a regularity norm of the data, not the energy norm. Q-coercivity gives only the one-sided static condition sup σ(T) < 1. It does not control the spectral radius, so the field-feedback series has no small parameter and has to be replaced by Fredholm inversion.
2. **Penrose failure is the same thing as a real-frequency mode (B3; the gap case is proved, the case ν ∈ Σ is proved given Lemma T).** Take the boundary feedback operator I − 𝒦(ν+i0) at a real frequency ν. When ν is in a spectral gap, it fails to be injective exactly when L has a gap eigenvalue. When ν ∈ Σ and the frequency map is nondegenerate, an exact imaginary-part identity applies. Every resonant term in it has the same sign, because w = −F_E > 0 and Ω > 0. So a kernel element must have vanishing resonant traces, which makes it a genuine **embedded neutral eigenmode**. Q-coercivity does not exclude such modes: their energy is ν times a sign-indefinite action.
3. **Critical frequencies are a second exact obstruction (proved, B2).** Suppose the frequency map has a nondegenerate interior extremum q_c on the source support. Then admissible canonical data have a **first-response** work on the critical orbit equal to 2 Re(e^{inθ_0} a_c) log t + O(1), with a_c ≠ 0. The cause is the strictly definite diagonal shell kernel. So the checkpoint-08 bound cannot be extended across such a point.
4. **Weakest closing hypothesis.** It is (NM_Σ): I − 𝒦(ν+i0) is injective on C^γ for every ν ∈ Σ. Spectrally, this means no embedded neutral mode and no band-edge threshold kernel. It is needed together with the frequency nondegeneracy (ND). Gap modes are *allowed*, and (A5) shows they are harmless for the work on unperturbed orbits. Theorem C proves rigorously that the operator hypotheses (K) and first-response hypotheses (F) give a time-uniform bound on the full field work, and hence on the linear label displacement u. This holds for every receiving orbit of the closed occupied set, including the circular line and the flat energy cap. Prop D reduces (K) and (F) to (ND) + (NM_Σ) through Lemma T and Prop F, whose proofs are **outlined**, not fully audited. Within this route (NM_Σ) cannot be weakened, because it is exactly the existence of the boundary resolvent. It is **not** shown to be necessary for the work bound itself (A5(c)).
5. **New unconditional facts.** These are A1–A5: the spectral structure, compactness of the field term, no growing or zero modes, uniform C^{1,1/2} field bounds, an L²(w)-averaged work bound uniform in time, radial locality of the force feedback, and bounded work from any single gap mode. In addition, Prop N reduces (ND) for the exact smooth equilibrium to strict monotonicity of the epicyclic frequencies plus small δ. For the free species this is an explicit inequality on the inner taper, and it **fails** for steep enough tapers.

## 1. Setting and the quantity bounded

**1.1 Model.** The model, conventions and equilibrium are those of the handoff and [EXACT_SMOOTH_INVERSE.md](../../smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md): species i ∈ {t,f}, radial variables (r,v,L) with L the squared specific angular momentum, dΓ = C_Γ dr dv dL, C_Γ = 4π², c = G²/a_0. Potentials vanish at infinity. Each F_i(E_i^F, L) is smooth with compact support in the hollow shell r_0 < r < R. Put w_i := −F_{i,E}; then w_i > 0 on the open occupied set O_i = {F_i > 0} and w_i vanishes at ∂O_i. Every occupied orbit lies in the epicyclic tube t = (E − E_c(L))/σ(s) < δ² (see Prop N).

**1.2 Action-angle variables and frequencies.** On the equilibrium flow use q = (J,L) and θ ∈ 𝕋, with dr dv = dJ dθ and dm := 2πC_Γ dJ dL. Write D_i = Ω_i(q)∂_θ. Let Ā_i be the closed set of actions of orbits in the closure of O_i; it includes the circular line J = 0. On Ā_i, Ω_i is smooth up to J = 0, because each well has a smooth nondegenerate minimum. Ā_i is compact inside the region of nondegenerate wells: orbits stay in [r_0,R], energies are at most a negative cap, and L lies in a compact positive interval. Hence

\[
0<\Omega_-\le\Omega_i(q)\le\Omega_+<\infty\quad(q\in\bar{\mathcal A}_i),
\qquad
\Sigma:=\bigcup_i\bigcup_{k\ne0}k\,\Omega_i(\bar{\mathcal A}_i).
\tag{1.1}
\]

Each Ā_i is connected, so Σ is a locally finite union of closed intervals k[Ω_{i,−},Ω_{i,+}]. It is closed and symmetric, it does not contain 0, and it has finitely many bounded gaps. Every large |ν| belongs to Σ.

**1.3 Linear system, labels, energy.** Accessible perturbations h_i have zero average on almost every equilibrium orbit and obey

\[
\partial_t h_i+D_ih_i=F_{i,E}D_i\psi_i,\qquad \psi=\mathcal P h .
\tag{1.2}
\]

Writing h_i = F_{i,E}u_i = −w_iu_i on O_i gives the linearized label equation (∂_t + D_i)u_i = D_iψ_i, the linear form of the handoff's (19). Once ψ is given, this equation makes sense on every equilibrium orbit, so u is defined on all of Ā_i and beyond. Canonical data generated by g_0 have h(0) = F_E D g_0 and u(0) = D g_0. The energy space ℋ is the completion of smooth accessible perturbations in A[h] = Σ_i∫h_i²/w_i dΓ, equivalently h = −wu with u ∈ L²(w dΓ) of zero orbit average. The conserved quadratic form

\[
Q[h]=\mathcal A[h]+\int m^THm\,dr,\qquad c_Q\mathcal A\le Q\le C_Q\mathcal A ,
\tag{1.3}
\]

is ZAR-S2 ([CLASSICAL_RADIAL_STABILITY.md](../../smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md)), with coercivity on the accessible closure from ZAR-N1. Here m_j(r) = ∫_{r'<r} h_j dΓ and δa = Hm, with

\[
H=\begin{pmatrix}2cM_{F_t}/r^4&-G/r^2\\-G/r^2&-G/r^2\end{pmatrix},
\qquad \psi_i(r)=\int_r^\infty\delta a_i(s)\,ds .
\]

This is exactly the shell-kernel operator 𝒫 with P_ff = P_ft = P_tf = −G/max(r,r') and P_tt = 2c∫_{max(r,r')}^∞ M_{F_t}(s)s^{−4}ds. For accessible h, m vanishes for r ≤ r_0 and r ≥ R. Integrating by parts, Σ_i∫h_iψ_i dΓ = ∫m^THm dr.

**1.4 Receiving coefficients.** Let I = [r_0,R] and Y_γ := C^γ(I)², with norm ‖φ‖_∞ + [φ]_γ and 0 < γ < 1. For a radial φ and an equilibrium orbit (i,q), put φ_{i,k}(q) = (2π)^{−1}∫φ_i(r_i(θ,q))e^{−ikθ}dθ. Fix any compact family 𝒪 of equilibrium bound orbits with radial range in I, for example 𝒪 = Ā_t ∪ Ā_f. Let V_𝒪 = sup|v| and Ω_𝒪 = inf Ω over 𝒪. Since ∂_θ r = v/Ω, the shift f̂_k = −(2π)^{−1}∫f(θ+π/k)e^{−ikθ}dθ gives

\[
|\phi_{i,k}(q)|\le\tfrac12(\pi V_{\mathcal O}/\Omega_{\mathcal O})^\gamma[\phi]_\gamma|k|^{-\gamma}
\qquad(k\ne0,\ q\in\mathcal O).
\tag{1.4}
\]

**1.5 The field work.** For an equilibrium orbit (i,q) in 𝒪 with initial angle θ_0, define

\[
W_i(t;\theta_0,q)=\int_0^t(\partial_s\psi_i)\bigl(s,r_i(\theta_0+\Omega_i(q)s,q)\bigr)ds
=\sum_ke^{ik\theta_0}W_{i,k}(t;q),
\quad W_{i,k}=\int_0^te^{ik\Omega_is}\partial_s\psi_{i,k}(s,q)ds .
\]

Along the orbit, (∂_t + D_i)(ψ_i − u_i) = ∂_tψ_i. Hence

\[
W_i=(\psi_i-u_i)(t,\theta_0+\Omega_it,q)-(\psi_i-u_i)(0,\theta_0,q).
\tag{1.5}
\]

So a time-uniform bound on W over Ā_i is equivalent to a time-uniform L^∞(Ā_i) bound on u_i, given sup|ψ| (A3) and bounded u(0). This is the linear content of the handoff's endpoint identity (20).

**1.6 Volterra form and the feedback symbol.** ZAR-S2 gives a classical solution with Duhamel form h(t) = e^{−tD}h(0) + ∫_0^t e^{−(t−s)D}F_EDψ(s)ds. Applying 𝒫,

\[
\psi(t)=\psi^0(t)+\int_0^t\mathcal K(t-s)\psi(s)\,ds,\qquad
\psi^0(t)=\mathcal P e^{-tD}h(0),\quad
\mathcal K(\tau)\phi=\mathcal P[e^{-\tau D}F_ED\phi].
\tag{1.6}
\]

Here ψ^0 is the checkpoint-08 first response. For Im z > 0, Laplace transforms converge (A3), and ∫_0^∞e^{izτ}e^{−ikΩτ}dτ = i/(z − kΩ) gives the feedback symbol

\[
\mathcal K(z)\phi=\mathcal P\Bigl[-w\sum_{k\ne0}\frac{k\Omega\,\phi_k\,e^{ik\theta}}{k\Omega-z}\Bigr]
=\mathcal P[-w(\phi-\bar\phi)]-z\,\mathcal P\Bigl[w\sum_{k\ne0}\frac{\phi_ke^{ik\theta}}{k\Omega-z}\Bigr],
\tag{1.7}
\]

species by species, where φ̄ is the orbit average. The second form uses kΩ/(kΩ−z) = 1 + z/(kΩ−z) and needs no derivative of φ. With ψ̂(z) = ∫_0^∞e^{izt}ψ dt and Ψ̂_1(z) = ∫_0^∞e^{izt}∂_tψ dt = −izψ̂ − ψ(0), and ψ(0) = ψ^0(0):

\[
(I-\mathcal K(z))\hat\psi=\hat\psi^0,\qquad
\hat\Psi_1(z)=(I-\mathcal K(z))^{-1}\bigl[\hat\Psi_1^0(z)+\mathcal K(z)\psi^0(0)\bigr].
\tag{1.8}
\]

The coefficients of 𝒦 contain the fixed F_E, so 𝒦 is order one as the data amplitude tends to zero.

## 2. Unconditional structure (Theorem A)

**A1 (spectral structure) [PROVED].**
- (a) e^{tL} is a strongly continuous unitary group on (ℋ,Q). L is skew-adjoint and σ(L) ⊂ iℝ.
- (b) The field term B = L − L_0, with Bh = F_EDψ[h] = w v δa[h], is compact on ℋ.
- (c) σ_ess(L) = σ(L_0) = iΣ.
- (d) σ(L)∖iΣ consists of isolated, semisimple, finite-multiplicity eigenvalues (gap eigenvalues).
- (e) 0 ∈ ρ(L).

*Proof.*
- (a) ZAR-S2 gives the group and conservation of Q for smooth data. Density and (1.3) give a Q-isometric group, hence a unitary one, and Stone's theorem applies.
- (b) For h ∈ ℋ, Cauchy–Schwarz gives |m_j| ≤ W_*^{1/2}‖h‖_A and |m_j(r) − m_j(s)| ≤ ‖h‖_A(χ̄|r−s|)^{1/2}, with χ̄ = sup_r C_Γ∫w_j dv dL < ∞. By Arzelà–Ascoli the image of the unit ball under h ↦ m, and hence under h ↦ δa = Hm, is precompact in C(I). Finally ‖wvφ‖_A² = ∫wv²φ² ≤ C‖φ‖_∞².
- (c) On the k-th angular mode, L_0 = −D is multiplication by −ikΩ(q) in L²(w^{−1}dm). Its spectrum is the closure of the essential range, and every point of it is essential, because multiplication operators have no isolated finite-multiplicity eigenvalues. Weyl's theorem (the norms are equivalent) transfers this to L.
- (d) This holds for normal operators outside the essential spectrum.
- (e) 0 ∉ iΣ by (1.1). If Lh = 0, then Dh = D(F_Eψ), so h − F_Eψ is orbit-invariant. Zero orbit averages force h = −w(ψ − ψ̄), so h/w + ψ = ψ̄ and Q[h] = ∫h(h/w + ψ)dΓ = ∫hψ̄ dΓ = 0. Coercivity gives h = 0.

**A2 (no growing modes; invertibility off the axis) [PROVED].** For Im z > 0 and γ ∈ (0,1), 𝒦(z) maps C^0(I)² boundedly into C^{1,1/2}(I)², so it is compact on Y_γ, and I − 𝒦(z) is invertible on Y_γ. In particular ψ̂(z) is the unique Y_γ solution of (1.8).

*Proof.* Both densities in (1.7) are accessible elements of ℋ. Their A-norms are at most 2‖φ‖_∞W_*^{1/2} and ‖φ‖_∞W_*^{1/2}/Im z (Parseval). By A3, 𝒫: ℋ → C^{1,1/2} is bounded. For injectivity, suppose ψ = 𝒦(z)ψ. Set u_k = kΩψ_k/(kΩ−z) and h = −wu. Then |kΩ/(kΩ−z)| ≤ 1 + |z|/Im z, so u ∈ L²(w) and h ∈ ℋ, and 𝒫h = ψ. Mode by mode, (Lh)_k = −ikΩh_k − ikΩwψ_k = −izh_k. This eigenvalue has real part Im z ≠ 0, which contradicts A1(a). Hence h = 0 and ψ = 𝒫h = 0. Compactness and the Fredholm alternative give invertibility.

**A3 (uniform field bounds; averaged work) [PROVED].** With Q_0 = Q[h(0)], for all t ≥ 0:

\[
\|\psi(t)\|_{C^{1,1/2}(I)}+\|\partial_t\psi(t)\|_{C^0}\le C\sqrt{Q_0},\qquad
|\psi_{i,k}(t,q)|\le C(1+|k|)^{-3/2}\sqrt{Q_0}\ \ (q\in\bar{\mathcal A}_i),
\]

\[
|W_i(t)|\le C\sqrt{Q_0}\,t,\qquad
\sup_{t\ge0}\|W_i(t,\cdot)\|_{L^2(w_i\,d\Gamma)}\le C\sqrt{Q_0}.
\]

*Proof.* The C^{1,1/2} bound follows from the m-estimates in A1(b), ψ' = −Hm, and ψ = ∫_r^∞δa. For ∂_tψ, use ∂_tm = −j with j = C_Γ∫v h dv dL, ∫|j|dr ≤ ‖h‖_A(∫μ)^{1/2}, and ∂_tψ_i(r) = −∫_r^∞(Hj)_i ds. The coefficient decay comes from θ ↦ ψ(r(θ,q)) ∈ C^{1,1/2}(𝕋), uniformly in q. For the averaged work bound, apply (1.5) pointwise in z_0 = (θ_0,q). The free flow S^t preserves w dΓ, and ‖u(t)‖_{L²(w)} = A[h(t)]^{1/2} ≤ (Q_0/c_Q)^{1/2}.

The weight w vanishes at ∂O, so A3 gives no control of u at the support boundary, which is exactly where confinement is decided.

**A4 (radial locality of the force feedback) [PROVED].** For accessible h, m_j[h](r) depends only on h restricted to orbits whose radial range [r_−(q'), r_+(q')] contains r. Therefore the force-to-force feedback f ↦ H m[e^{−τD}(wvf)] at radius r depends only on f restricted to the union of radial ranges of orbits through r.

*Proof.* If r_+(q') < r, then 1_{r(θ',q')<r} ≡ 1 and the orbit integral of h is zero. If r_−(q') > r, the indicator is zero. The source wvf on an orbit samples f only along that orbit. For the exact equilibrium these ranges have width ≤ Cδh(s) (Prop N(b)).

**A5 (single modes) [PROVED].** Let Lh_ν = −iνh_ν with ν real, h_ν ∈ ℋ and ψ_ν = 𝒫h_ν ∈ C^{1,1/2}.
- (a) On O_i, u_{ν,k} = kΩψ_{ν,k}/(kΩ − ν) and u_{ν,0} = 0. The same formula defines the mode's label displacement on every non-resonant orbit.
- (b) *Gap modes.* If ν ∉ Σ, then ‖u_ν‖_{L^∞(Ā)} ≤ C(ν, dist(ν,Σ))‖h_ν‖_Q. By (1.5), the work of Re(c e^{−iνt}h_ν) on every receiving orbit of Ā is bounded for all time by 2|c|(‖ψ_ν‖_∞ + ‖u_ν‖_∞).
- (c) *Embedded modes.* If ν ∈ Σ, then ψ_{ν,k} = 0 on every resonant point q* with kΩ_i(q*) = ν, w_i(q*) > 0 and ∇Ω_i(q*) ≠ 0. Under (ND) of §6, u_ν ∈ L^∞(Ā) and the mode's work is bounded.

*Proof.*
- (a) Take the angle Fourier transform of the eigen-equation.
- (b) Use (A3) and |kΩ/(kΩ−ν)| ≤ 2 for |k| ≥ 2|ν|/Ω_−, and ≤ |k|Ω_+/dist(ν,Σ) otherwise. The sum Σ_k(1+|k|)^{−3/2} converges.
- (c) We have ∫w|u_{ν,k}|²dm < ∞. If ψ_{ν,k}(q*) ≠ 0, then near q* the integrand is at least c/dist(q, {kΩ = ν})², which is not integrable across a regular curve. For J > 0, ψ_{ν,k} is C¹ in q. Near J = 0 it is Lipschitz in L uniformly, since ∂_L r(θ,J,L) is bounded, and ∂_LΩ ≠ 0 by (ND). Hence |ψ_{ν,k}| ≤ C|kΩ − ν| near the resonant set and |u_{ν,k}| ≤ C|k|Ω_+. Only finitely many k resonate (|k| ≤ |ν|/Ω_−). The rest are handled as in (b).

So **point spectrum is harmless mode by mode** for the work on unperturbed orbits. It obstructs *decay* of ∂_tψ, not boundedness of W.

## 3. Exact obstructions (Theorem B)

**B1 (the energy route cannot close) [PROVED].**
- (a) For λ ∈ iΣ we have λ ∈ σ(L), and ‖(L − λ')^{−1}‖_Q = 1/dist(λ', σ(L)) → ∞ as λ' → λ. The energy-space resolvent has no bounded boundary values anywhere on the receiving-frequency set.
- (b) Let q* be an eccentric occupied receiving orbit, k ≥ 1, ω = kΩ_i(q*). Let ℓ ∈ ℋ be the Q-representer of h ↦ ψ_i[h]_k(q*), bounded by A3, and μ_ℓ its spectral measure for H = iL. If μ_ℓ is absolutely continuous near ω with density continuous at ω and m_ℓ(ω) > 0, then sup{|W_i(t;θ_0,q*;h)| : t ≥ 0, ‖h‖_Q ≤ 1} = ∞ for every θ_0.
- (c) Write T h := −w(ψ[h] − ψ̄[h]) for the static response. Then Q[h] = ⟨h,(I − T)h⟩_A, with T compact and A-self-adjoint. Thus Q-coercivity is exactly sup σ(T) < 1. It is not r(T) < 1, so even the static feedback series is not guaranteed to converge. There is no small parameter, and the route must use Fredholm invertibility.

*Proof of (b).* Let I_ε = [ω−ε, ω+ε], N_ε = μ_ℓ(I_ε)^{1/2}, h_ε = E(I_ε)ℓ/N_ε and t = 1/(2ε). Then ψ_k(s) = N_ε^{−1}∫_{I_ε}e^{−isν}dμ_ℓ. With T(ν) = ∫_0^te^{i(ω−ν)s}ds we have Re T ≥ t cos(1/2) and |Im T| ≤ t/4 on I_ε. So

\[
|\operatorname{Im}W_{i,k}|=N_\varepsilon^{-1}\Bigl|\int_{I_\varepsilon}\nu\,\operatorname{Re}T\,d\mu_\ell\Bigr|\ge0.87(\omega-\varepsilon)tN_\varepsilon
\ge0.43(\omega-\varepsilon)\sqrt{m_\ell(\omega)/\varepsilon}\to\infty .
\]

For k' ≠ k, the measure of ψ_{k'} has total variation ≤ ‖ℓ_{k'}‖_Q ≤ C(1+|k'|)^{−3/2} and is supported in I_ε. Since |k'Ω(q*) − ν| ≥ Ω(q*)/2 there, |W_{k'}| ≤ C(1+|k'|)^{−3/2}(ω+1)·4/Ω(q*), which is summable. Also |W_0| ≤ 2 sup|ψ|. Hence |W| ≥ |W_{i,k}| − C.

*Remark.* For the feedback-free generator, m_ℓ(ω) > 0 whenever ∇Ω_i(q*) ≠ 0. The reason is that the spectral density contains the diagonal term |𝒦_{ii,kk}(q*,q*)|²w(q*) > 0 on the resonant curve (B2, (3.1)). With feedback, positivity is generic but is not proved here.

*Proof of (c).* ⟨h,Th⟩_A = −∫h(ψ − ψ̄)dΓ = −∫hψ dΓ, by zero orbit averages.

**B2 (critical frequencies already break the first response) [PROVED].** The shell kernels are strictly definite on the diagonal. Write 1/max(r,r') = ∫1_{s>r}1_{s>r'}s^{−2}ds and A_n(s;q) = (2π)^{−1}∫1_{r(θ,q)<s}e^{−inθ}dθ. Then, for n ≠ 0 and J(q) > 0,

\[
\mathcal K_{ff,nn}(q,q)=-G\!\int_0^\infty\!|A_n(s;q)|^2s^{-2}ds<0,\qquad
\mathcal K_{tt,nn}(q,q)=2c\!\int_0^\infty\!|A_n(s;q)|^2M_{F_t}(s)s^{-4}ds>0 .
\tag{3.1}
\]

Here 𝒦_{ij,kn} are the double-angle kernels of checkpoint 08, (22). Suppose Ω_j has a nondegenerate local extremum at q_c with J(q_c) > 0 and w_j(q_c) > 0; say a maximum, the minimum case being symmetric. Fix n ≥ 1. Take a small neighborhood U of q_c on which Ω_j < Ω_j(q_c) off q_c and |kΩ_j(q_c) − nΩ_j(q')| ≥ Ω_j(q_c)/2 for k ≠ n and q' ∈ U. Take the generator g_0 = χ(q)Re(g e^{inθ}) with χ ∈ C_c^∞(U), χ(q_c) = 1, g ≠ 0. This is smooth in phase space because U avoids J = 0. Then the first-response work at the receiving orbit (j,q_c) obeys

\[
W^0_j(t;\theta_0,q_c)=2\operatorname{Re}\bigl(e^{in\theta_0}a_c\bigr)\log t+O(1),\qquad
a_c=\frac{4\pi^2C_\Gamma\,\nu_c\,\mathcal K_{jj,nn}(q_c,q_c)\,h_n(0,q_c)}{n\sqrt{\det(-D^2\Omega_j(q_c))}}\ne0,
\tag{3.2}
\]

with ν_c = nΩ_j(q_c) and h_n(0,q_c) = inΩ_jF_{j,E}g_n(q_c) ≠ 0.

*Proof.* Checkpoint-08 (23)–(24) writes W^0_{j,n} = −∫a(ν)(e^{i(ν_c−ν)t}−1)/(ν_c−ν)dν, with a(ν) the coarea density of 2πC_Γν𝒦_{jj,nn}(q_c,·)h_n(0,·) on {nΩ_j = ν}. Near the maximum, in Morse coordinates, ∫_{nΩ=ν}dσ/|∇(nΩ)| = 2π/(n√det(−D²Ω)). The integrand is Lipschitz in q' (checkpoint 08), so a(ν) = a_c + O((ν_c−ν)^{1/2}) for ν < ν_c, and a = 0 for ν > ν_c. The remainder b = a − a_c1_{(ν_c−η,ν_c)} has b(ν_c) = 0 and |b| ≤ C|ν−ν_c|^{1/2}. By Lemma W its contribution is bounded. The step contributes a_c∫_0^{ηt}(e^{iy}−1)/y dy = a_c(−log(ηt) − γ_E + Ci(ηt) + i Si(ηt)), whose real part is −log t + O(1). Receiving harmonics k ≠ ±n are non-resonant on U. Their exterior bounds are summable by the kernel decay (27) of checkpoint 08 at the eccentric receiver q_c, and W_0 is bounded. The harmonic −n gives the complex conjugate.

*Consequences.* (i) No estimate of the form (30) holds for sources whose support contains a nondegenerate interior frequency extremum. (ii) At ν_c the coarea densities feeding 𝒦(ν+i0) jump, so 𝒦 is log-singular there and not Hölder, and the limiting-absorption route fails. Whether the self-consistent feedback screens this log is **not decided here**. A heuristic rank-one Sherman–Morrison computation suggests the full response stays bounded but has only a 1/log modulus, which would allow log log t growth. This is **not** a claim. A saddle gives a log-divergent density and, by the same argument, growth of order log² t (not needed below).

**B3 (Penrose failure ⟺ real-frequency mode) [(a) PROVED; (b) PROVED given Lemma T(a,b) and (ND)].** Let ν ∈ ℝ.
- (a) If ν ∉ Σ, then 𝒦 is analytic near ν, and ker(I − 𝒦(ν)) ≠ {0} if and only if −iν is a gap eigenvalue of L.
- (b) Let ν ∈ Σ and φ ∈ Y_γ with φ = 𝒦_+(ν)φ := lim_{ε↓0}𝒦(ν+iε)φ. Then φ is Lipschitz, being in the range of 𝒦_+ by Lemma T(a). It satisfies the **imaginary-part identity**

\[
\sum_i\sum_{k\ne0}\int_{\{k\Omega_i=\nu\}}w_i\,|\nu|\,|\phi_{i,k}|^2\,\frac{d\sigma}{|\nabla(k\Omega_i)|}=0 ,
\tag{3.3}
\]

so φ_{i,k} = 0 on every resonant curve inside the occupied set. Consequently h := −wu with u_k = kΩφ_k/(kΩ−ν) lies in ℋ, satisfies 𝒫h = φ and Lh = −iνh, and is an **embedded neutral eigenmode**. Conversely, every embedded eigenmode gives such a kernel element (A5(c)).
- (c) Q[h_ν] = 2πC_Γ ν Σ_k∫w kΩ|ψ_k|²(kΩ−ν)^{−2}dJ dL (identity 4 of `identity_check.py`). For ν > 0 the k > 0 and k < 0 terms have opposite signs. Positivity of Q is consistent with such modes and does not exclude them. The homogeneous Penrose argument also does not transfer. There the vanishing trace forces F' = 0 at the resonant velocity. Here it constrains the field coefficients φ_k, while w > 0.

*Proof of (b).* Let n_ε = −wΣkΩφ_ke^{ikθ}/(kΩ−ν−iε) ∈ ℋ; this holds because φ Lipschitz gives Σk²|φ_k|² < ∞. Put φ_ε = 𝒫n_ε = 𝒦(ν+iε)φ. The quantity J(ε) = ∫n̄_ε𝒫n_ε dΓ = ∫m̄_ε^THm_ε dr is real. Split J = J_1 + J_2, where J_1 = −2πC_ΓΣ∫wkΩ|φ_k|²/(kΩ−ν+iε)dJ dL. The Poisson-kernel limit gives Im J_1 → 2π²C_Γ × (left side of (3.3), signed by ν). By Lemma T(b), ‖φ_ε − φ‖ ≤ Cε^α, and ∫dm/|kΩ−ν+iε| = O(log(1/ε)). Hence |J_2| ≤ Cε^α log(1/ε) → 0. All terms of (3.3) have the sign of ν, because kΩ = ν forces sign k = sign ν. So each term vanishes, and by continuity φ_{i,k} vanishes on the resonant curves where w > 0. Lipschitz φ and (ND) bound u, as in A5(c). We have |n_ε| ≤ w|u| and n_ε → −wu, so dominated convergence gives 𝒫h = φ. Mode by mode, Lh = −iνh.

## 4. Frequency-to-work lemma and the first response

**Lemma W [PROVED].** Let a be bounded on [ω−ρ, ω+ρ] with modulus of continuity ω_a there, and suppose E_ρ := ∫_{|ν−ω|≥ρ}|a(ν)|/|ν−ω|dν < ∞. Then for all t ≥ 0,

\[
\Bigl|\int a(\nu)\frac{e^{i(\omega-\nu)t}-1}{\omega-\nu}d\nu\Bigr|\le4|a(\omega)|+4\int_0^\rho\frac{\omega_a(s)}sds+2E_\rho .
\tag{4.1}
\]

*Proof.* On the symmetric interior, the constant a(ω) multiplies 2i Si(ρt), with |Si| ≤ Si(π) < 2; the odd real part cancels. The rest of the interior is at most ∫_{|x|<ρ}ω_a(|x|)·2/|x|dx. The exterior is at most 2E_ρ. This is checkpoint-08 (21) in weighted form, with no frequency gap.

**Prop F (first response on the whole occupied set) [OUTLINED].** Let g_0 ∈ C_c^∞(O_j) be a fixed-L canonical generator. Assume ∇Ω_j ≠ 0 on its action support, and ∂_LΩ_j ≠ 0 where that support meets J = 0. Then for each γ ∈ (0,1) there is α > 0 such that Ψ̂_1^0 ∈ C^α(S̄;Y_γ) and sup_S(1+|z|)‖Ψ̂_1^0(z)‖_{Y_γ} < ∞, where S = {0 < Im z ≤ 1}. Also ψ^0(0) ∈ C^∞(I).

*Outline.* Write ν = nΩ(q'), let P^{(n)}(r,q') = (2π)^{−1}∫P(r,r(θ',q'))e^{inθ'}dθ', and let b_n(r,ν) be the coarea density of P^{(n)}(r,·)h_n(0,·) on {nΩ = ν}. Then

\[
\hat\Psi_1^0(z)=\sum_n\int\nu\,b_n(\cdot,\nu)\,(z-\nu)^{-1}d\nu .
\]

The needed properties are as follows.
- P^{(n)} = O(1/n) and is Lipschitz in r and q', because P(r,·) is Lipschitz and θ' ↦ r(θ',q') is C¹.
- ∂_rP^{(n)} = (G/r²)A_{−n} for Newtonian kernels and −2cM_{F_t}r^{−4}A_{−n} for P_tt, with A_n = sin(nθ_*)/(πn) jointly C^{1/2} in (r,q') uniformly in n.
- Near J = 0, use (a,L) coordinates with a = (2J/κ)^{1/2}. There h_n(0) = O(a^{|n|}) compensates the a^{−1/2} Hölder constants.
- (ND) makes level sets move smoothly. Vector-valued Plemelj–Privalov then gives C^α boundary values, and h_n decays rapidly in n.

Decay O(1/|z|) holds because each b_n has compact ν-support. The steps still to audit in full are the circular-line endpoint terms and the Privalov constants as functions of the support length (logarithmic).

**Corollary 4.1 (sharp first-response dichotomy).** Under Prop F, Lemma W and the summation of §5 (with 𝒦 replaced by 0) give sup_{t,θ_0}|W^0| < ∞ on *every* receiving orbit of 𝒪, including the circular line and the flat cap. Checkpoint 08 needed compact eccentric receiving bands and finitely many source harmonics; this result needs neither. Conversely, by B2, a nondegenerate interior frequency extremum in the source support produces log t growth. So (ND) is sharp for the first response.

## 5. Conditional full-feedback theorem

**Hypotheses.** Fix γ, α ∈ (0,1) and S̄ = {0 ≤ Im z ≤ 1}, with boundary values understood as limits.
- **(K)** 𝒦 extends to a uniformly α-Hölder map S̄ → B(Y_γ), with ‖𝒦(z)‖ → 0 as |z| → ∞. There is a finite set E ⊂ ℝ∖Σ such that I − 𝒦(z) is invertible for z ∈ S̄∖E.
- **(F)** For the given g_0: Ψ̂_1^0 ∈ C^α(S̄;Y_γ), sup_S(1+|z|)‖Ψ̂_1^0‖_{Y_γ} < ∞, and sup_S(1+|z|)‖𝒦(z)ψ^0(0)‖_{Y_γ} < ∞.

**Theorem C [PROVED: (K)+(F) ⇒ conclusion].** Under (K) and (F), every ν ∈ E corresponds to a gap eigenvalue −iν of L (B3(a)). The full linear solution satisfies

\[
\boxed{\sup_{t\ge0}\ \sup_{\theta_0}\ \sup_{(i,q)\in\mathcal O}|W_i(t;\theta_0,q)|\le C_W<\infty,}
\qquad
\sup_{t\ge0}\|u_i(t)\|_{L^\infty(\bar{\mathcal A}_i)}\le\|Dg_0\|_\infty+2\sup_t\|\psi\|_\infty+C_W ,
\]

where C_W depends linearly on the norms in (F) and on the constants in (K) and (1.4). This holds for every receiving orbit of the closed occupied set, including circular orbits and orbits at the flat energy cap.

*Proof.*

*Step 1 (Laplace identity).* For Im z > 0, (1.8) holds by A2.

*Step 2 (gap modes).* Let P_E be the Q-orthogonal projection onto ⊕_{ν∈E}ker(H−ν), with H = iL; it is finite-dimensional. Write h(0) = P_Eh(0) + h'. The gap part has bounded work by A5(b). For h', for Im z > 0,

\[
\hat\Psi_1[h'](z)=\hat\Psi_1[h](z)-\sum_{\nu_j\in E}\nu_j\,\psi[P_jh(0)]\,(z-\nu_j)^{-1}.
\]

Away from small discs D_j around the ν_j, the right side is Hölder and decays by (1.8), (K) and (F). Here ‖(I−𝒦)^{−1}‖ ≤ 2 where ‖𝒦‖ ≤ 1/2, the inverse is continuous on the compact rest, and the resolvent identity gives the Hölder modulus. Inside D_j we have ψ̂[h'](z) = ψ[−i(H−z)^{−1}h']. This is analytic, because h' ⊥ ker(H−ν_j) and ν_j is isolated, and ψ: ℋ → C^{1,1/2} is bounded. Hence B := sup_S(1+|z|)‖Ψ̂_1[h']‖_{Y_γ} and H_α := [Ψ̂_1[h']]_{C^α(S;Y_γ)} are finite.

*Step 3 (damped Parseval).* For ε ∈ (0,1], f_ε(s) = e^{−εs}∂_sψ_{i,k}(s,q)1_{s>0} lies in L¹ ∩ L², and f̂_ε(ν) = Ψ̂_{1,k}(ν+iε;q). Pair it with e^{iωs}1_{[0,t]}, where ω = kΩ_i(q):

\[
\int_0^te^{i\omega s}e^{-\varepsilon s}\partial_s\psi_{i,k}ds=\frac1{2\pi i}\int\hat\Psi_{1,k}(\nu+i\varepsilon;q)\frac{e^{i(\omega-\nu)t}-1}{\omega-\nu}d\nu .
\]

*Step 4 (each harmonic).* Apply (4.1) with ρ = 1 to a_k = Ψ̂_{1,k}(·+iε;q)/(2π). By (1.4) and Step 2, |a_k(ν)| ≤ C|k|^{−γ}B(1+|ν|)^{−1} and ω_{a_k}(s) ≤ C|k|^{−γ}H_αs^α. Since |ω| ≥ |k|Ω_𝒪, three bounds follow. First, sup_{|ν−ω|≤1}|a_k| ≤ C|k|^{−1−γ}B. Second, the Dini term is at most C|k|^{−1−γ}B[1 + α^{−1}log(1 + |k|H_α/B)]. Third, E_1 ≤ C|k|^{−γ}B∫_{|ν−ω|≥1}dν/((1+|ν|)|ν−ω|) ≤ C|k|^{−1−γ}log(2+|k|)B. These are summable over k ≠ 0. The k = 0 term is ∫_0^te^{−εs}∂_sψ_0 ds, at most 3 sup|ψ| after integrating by parts.

*Step 5.* The bound is uniform in ε and t. Since ∂_sψ is bounded on [0,t], letting ε → 0 gives the bound on W. The u-bound follows from (1.5).

## 6. Reduction to spectral hypotheses

**(ND)** For each species, ∇Ω_i ≠ 0 on Ā_i, and ∂_LΩ_i(0,L) ≠ 0 on the occupied L-range.

**(NM_Σ)** For every ν ∈ Σ, including band edges, I − 𝒦_+(ν) is injective on Y_γ. Under (ND), B3(b) shows this is equivalent to two conditions: L has no eigenvalue −iν with ν ∈ Σ, and there is no threshold kernel at the band edges of Σ, where resonant sets lie on ∂Ā and (3.3) is empty.

**Lemma T [OUTLINED].** Assume (ND) and let γ ∈ (0,1).
- (a) For Im z ≥ 0, 𝒦(z) maps Y_γ boundedly into Lip(I)², hence compactly into Y_γ.
- (b) z ↦ 𝒦(z) is uniformly α-Hölder on S̄ in B(Y_γ), for some α = α(γ) > 0.
- (c) ‖𝒦(z)‖_{B(Y_γ)} ≤ C(1+|z|)^{−γ}log(2+|z|).
- (d) ‖𝒦(z)φ‖_{Y_γ} ≤ C(1+|z|)^{−2}‖φ‖_{C³}.

*Outline.* By (1.7),

\[
\mathcal K(z)\phi=\sum_n\int\nu\,c_n(\cdot,\nu)(\nu-z)^{-1}d\nu,
\qquad c_n(r,\nu)=\int_{n\Omega=\nu}P^{(n)}(r,q')(-w)\phi_n(q')\frac{d\sigma}{|\nabla n\Omega|}.
\]

The bounds |P^{(n)}| + |∂_rP^{(n)}| ≤ C/n and |φ_n| ≤ Cn^{−γ}‖φ‖ hold, the coarea factor is ≤ C/n, and φ_n is Hölder in q' with min(n^{−γ}, |Δq'|^γ). With λ = ν/n these give

\[
|c_n|\le Cn^{-2-\gamma},\qquad |c_n(\nu)-c_n(\nu')|\le Cn^{-2-\gamma}\min(1,|\nu-\nu'|^\gamma),
\]

and Lipschitz dependence on r with the same size. Interpolation makes ν ↦ c_n(·,ν) ∈ C^{γ(1−γ)}(ℝ; C^γ_r). Vector-valued Privalov then bounds each term of νc_n by Cn^{−1−γ}log n in sup norm and Hölder norm, which is summable. This gives (a) and (b).

For (c), split n into three groups: resonant (n ≈ |z|/Ω, about |z| terms, each Cn^{−1−γ}log n), small non-resonant (distance ≥ |z|/2), and large non-resonant (distance ≥ nΩ_−/2). Each group sums to O(|z|^{−γ}log|z|).

For (d), expand 1/(ν − z) = −1/z − ν/z² + ν²/(z²(ν−z)). The 1/z term is 𝒫[iwDφ]. Its shell density ∫wvφ'dvdL vanishes, because w is even in v.

At the boundaries: the integrand vanishes like a^{1+γ} at J = 0 (in (a,L) coordinates, transverse by (ND)); w is flat at the energy cap and at the L-ends; and tangencies with the cap curve are therefore harmless. The steps still to audit in full are these boundary cases, the logarithmic growth of the Privalov constants with support length, and the finite species coupling.

**Prop D [PROVED given Lemma T and Prop F].** (ND) + (NM_Σ) imply (K), with E equal to the set of gap eigenfrequencies, which is finite. They also imply (F) for every g_0 ∈ C_c^∞(O). Hence the conclusion of Theorem C holds for every smooth compactly supported canonical generator.

*Proof.*
- (i) For Im z > 0, invertibility is A2.
- (ii) In a gap, 𝒦 is analytic on a complex neighborhood. By B3(a) its kernels are exactly gap eigenmodes, and these are isolated by the analytic Fredholm theorem.
- (iii) On Σ, injectivity is (NM_Σ). Lemma T(a) and the Fredholm alternative upgrade it to invertibility.
- (iv) Gap zeros cannot accumulate at a band edge ν_e ∈ Σ, because I − 𝒦_+(ν_e) is invertible and 𝒦 is continuous on S̄. The gaps are finitely many and bounded, so E is finite.
- (v) Lemma T(c) gives ‖𝒦‖ → 0. Continuity gives uniform bounds on S̄ away from E. Lemma T(b) gives the Hölder modulus. (F) follows from Prop F and Lemma T(d).

## 7. The exact smooth equilibrium

**Prop N [PROVED; the algebra is checked symbolically in `identity_check.py`].**
- (a) ∂_LΩ_i(0,L) = κ_i'(s)/L_{c,i}'(s), with s = s_i(L) and κ_i² = L_{c,i}'/s³ the epicyclic frequency. This is because Ω_i(0,L) = κ_i(s_i(L)) and ds/dL = 1/L_c'.
- (b) The target potentials are fixed independently of δ. Occupied orbits have E − E_c < δ²σ(s), so sup_{Ā_i}J ≤ C_iδ². Radial widths satisfy |r − s| ≤ C_iδh(s), by U − E_c ≥ (m/2R³)(r−s)² from the "no remote pieces" bound.
- (c) If κ_i is strictly monotone on [r_0,R] for both species, then (ND) holds for all sufficiently small δ. The reason is that Ω_i is a fixed smooth function and ∂_LΩ_i(J,L) = κ_i'/L_c' + O(J) uniformly. Decreasing δ is allowed by the existence construction.
- (d) For the free species, κ_f² = G(M_b + M + rM')/r³ and (κ_f²)' = G(r²M'' − rM' − 3M − 3M_b)/r⁴. This is strictly negative on the law annulus (M'' = 0) and on the outer taper (M'' = −AS'/(R−r_2) ≤ 0). On the inner taper M = ArS(z), with z = (r−r_0)/Δ and Δ = r_1 − r_0, it is negative **if and only if**

\[
r^2S'(z)/\Delta+r^3S''(z)/\Delta^2<3r_M+4rS(z),\qquad r_M=M_b/A .
\tag{7.1}
\]

Since S'' > 0 somewhere in (0,1/2), the left side is at least r_0³S''(z_*)/Δ². This exceeds the bounded right side for small Δ, so steep inner tapers make κ_f non-monotone. Monotonicity is a genuine profile condition and has not been evaluated for any parameter set here. If κ_f' vanishes, (ND) can still hold where ∂_JΩ(0,L) ≠ 0 (a boundary extremum, which is harmless because the harmonics vanish at J = 0). But Lemma T as outlined then needs an additional tangency argument.
- (e) For the tethered species, κ_t² = L_{c,t}'/r³ with L_{c,t} = Gr(M_b + M_f) − cM_t²/r. On the law annulus, κ_t² = [GM_b(1−f²) + 2G(1−f)Ar]/r³, which is strictly decreasing. It is also strictly decreasing at the flat edges r_0 and R. Its monotonicity on the tapers is a separate explicit condition, not evaluated here.

**Heuristic location of the remaining obstruction [HEURISTIC, not used].** Take the formal cold limit δ → 0. This is outside the fixed-δ theorems, and the cold limit of the equilibrium is singular. By A4 the force feedback becomes local. Ring displacements obey ξ'' + 𝕂(s)ξ = 0, with 𝕂_ij = κ_i²δ_ij + H_ijμ_j. For the free species with a common displacement this gives the Lagrangian frequency GM_tot/s³, which lies strictly below κ_f(s)² inside the support and meets it at the flat edges. Where M_tot/s³ decreases, these collective frequencies lie *inside* Σ. Their free resonances sit at radial distance O(1), while the coupling range is O(δ) by A4. (NM_Σ) asks whether the warm problem turns this collective band into embedded eigenvalues, or only into resonances absorbed at the free-resonance radius. That is not decided here. The repulsive tether term raises the tethered collective branch above κ_t, so it may also produce discrete gap modes; by A5(b) these are harmless for the work.

## 8. Ledger, remaining gap, and limits

| Item | Status |
|---|---|
| A1–A5 (spectral structure, compact field term, no growing or zero modes, uniform C^{1,1/2} field bounds, L²(w) work bound, radial locality, single-mode work) | Proved |
| B1 (energy-norm route cannot give a uniform work bound; static Q-coercivity is one-sided) | Proved |
| B2 (log t first-response growth at a nondegenerate interior frequency extremum) | Proved |
| B3 (kernel of I − 𝒦(ν+i0) ⟺ real-frequency eigenmode; imaginary-part identity) | (a) gaps: proved; (b) on Σ: proved given Lemma T(a,b) and (ND) |
| Lemma W; Theorem C ((K)+(F) ⇒ uniform full work and label bound on the closed occupied set) | Proved |
| Prop D (reduction to (ND)+(NM_Σ)) | Proved given Lemma T and Prop F |
| Lemma T; Prop F; Corollary 4.1 | Outlined; boundary and Privalov-constant audit outstanding |
| Prop N ((ND) ⟸ monotone κ_i + small δ; explicit free-species taper inequality) | Proved; parameters not evaluated |
| (NM_Σ): no embedded neutral mode or band-edge threshold kernel | **Assumed: the exact open obstruction** |
| Cold-limit location of the obstruction | Heuristic only |

**Remaining gap at this step.** Three things remain.
1. Prove or refute (NM_Σ) for the actual two-species equilibrium. Neither energy positivity nor the homogeneous Penrose argument decides it (B1(c), B3(c)).
2. Complete the audit of Lemma T and Prop F at the circular line and the flat cap.
3. Verify the monotonicity conditions (7.1) and (e) for the chosen profile, or handle boundary extrema of Ω.

If an embedded mode exists, the resolvent route breaks at its frequency. The mode itself has bounded work (A5(c)), but the continuous part near it would need a projected limiting-absorption analysis.

**Beyond the linear step (unchanged obligations).** Theorem C bounds work along *equilibrium* orbits for the *linear* field. The nonlinear problem still needs control of the actual paths and of the label-gradient term δa∂_vu in (19). Phase mixing makes ∂_vu grow linearly in t. A route through L¹ in time of sup_r|∂_tψ| would bound energy changes along arbitrary paths, but it needs no gap modes at all (they do not decay) and a stronger limiting absorption, one ν-derivative more. Neither is established.

**Not claimed.** This checkpoint does not claim:
- all-time confinement;
- a full-feedback bound without (NM_Σ) and (ND);
- decay of the self-consistent field;
- exclusion or existence of neutral modes;
- any statement about the circular or flat edges beyond the receiving-orbit bounds above;
- any change to the model's observational status.

The class is unchanged and respects every pitfall in the handoff: strictly radial canonical data, exact initial support, masses and Casimirs, a fixed negative initial gap, and no angular-current data, exterior population, shrinking gap or stationary substitute. No future work bound is assumed. The hypotheses concern only the fixed linear operator and the free first response.

## 9. Inputs read (sha256 at time of reading)

- `CLAUDE_HANDOFF_KINETIC_CONFINEMENT_2026-10-19.md`: 2af7be5626d3c90b7fe646f1cab4ff60fdb3bab15eefcbd644250f809823de71
- `canonical_confinement_2026_10_19/README.md`: 0b11424ddc82e9dcceff74b606ac75c760174b9fe084e5cc399ebad9ea1c7f9d
- `canonical_confinement_2026_10_19/AUDIT_AND_HANDOFF.md`: b93da5f8e8f564b5994d5c067cc441e8953710677f795635752d158d15df4324
- `canonical_confinement_2026_10_19/RESONANT_WORK_PROGRESS.md`: e74737fe9f1f5bda5635560e76f86f4978549d403d2a516235afd401ac797c5d
- `canonical_confinement_2026_10_19/CANONICAL_RIGIDITY_AND_SUPPORT.md`: 87962d02facb0db1a884423331203c0e78ba5a3b214ab3f35f3bcc03d1ebe466
- `canonical_confinement_2026_10_19/FINITE_TIME_CONFINEMENT.md`: 576b75161c5383ad09510b88875173bffd86e64333bf398589df788b39755644
- `nonlinear_radial_2026_10_19/NONLINEAR_COERCIVITY.md`: ec85b126c078e00f9cd5f364c08f78e9022c83f55228d06a7db1b3279bfe4c92
- `smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`: 490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b
- `smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md`: ff33f52fb33a7166a10ae5ba0c99b873ae581916286c6eefca2f70f86b880cb4

These are the derivations above, written by one author. They are not an external review or a formal proof certificate. Check the raw arguments before extending them.
