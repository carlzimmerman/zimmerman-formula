# MEDIUM-R2 raw derivation

Base checkpoint: 8aa3f7046a7ae14a99f3515fd42df5bf061fb1db. Target conventions: K=4πG, u=K|P|, gbar=u²/(a0−nu), b=a0/n. These are imported target definitions, not conclusions of the models below.

## A. A finite microscopic stochastic model

Define a continuous-time chain j=0,...,N. An empty slot is activated at rate κh; any activated slot deactivates at rate κj/N, a global density-dependent interaction. Thus B_j=κh(N−j), D_j=κj²/N, with B_N=D_0=0. κ>0 has units inverse time and h≥0 is dimensionless pump intensity. This is an explicitly defined many-body Markov model, not a Hamiltonian asserted to describe gravity. The j² rate contains a self contribution j/N in addition to j(j−1)/N. Removing that contribution makes j=1 absorbing when h=0 and changes the finite-N limit; the defined model retains it.

For h>0 the unique stationary distribution follows by zero current on every edge:

π_j/π_(j−1)=Nh(N−j+1)/j²,
π_j=Z_N(h)^−1 (Nh)^j N! / [(N−j)!(j!)²].

Detailed balance holds for this coarse chain: π_j B_j=π_(j+1)D_(j+1). A physical pump may nevertheless dissipate energy in hidden reservoir channels. Neither their entropy production nor thermal equilibrium follows from the chain alone. It would be incorrect to assert positive steady probability current in this one-dimensional chain.

The forward/backward edge affinity including a distribution p is A_j=log[p_j B_j/(p_(j+1)D_(j+1))]. It vanishes at stationarity. The bare rate affinity is log[Nh(N−j)/(j+1)²]. Its source-dependent part is log h. Equivalently H_eff(j;h)=−kBT log w_j(h) has source −kBT j log h plus a combinatorial term. This effective scalar energy is singular at h=0 and its conjugate observable is count j. It is not −g·P.

At h=0 the unique stationary law is δ_(j,0), and starting from j=N the mean absorption time is ∑_(j=1)^N 1/D_j=(N/κ)∑_(j=1)^N j^−2. The chain therefore has a genuine zero-source absorbing state; it is not a finite-gap equilibrium trace with a regular linear field source.

For x=j/N the drift is κ[h(1−x)−x²]. At fixed h>0 the macroscopic stable root is x_*=(sqrt(h²+4h)−h)/2. The distribution's ratio test or its large-N logarithm yields concentration at this root. Substituting u=bx and h=n gbar/b yields exactly gbar=u²/[n(b−u)] and dot u=(κ/b)[gbar(a0−nu)−u²]. Both the pump-to-acceleration map and b=a0/n are extra dictionary assumptions. The model derives the root from transition rules, not that dictionary.

At finite N the exact moment equation is h(1−E x)=E x². Consequently E x≤x_* by Var(x)≥0 and monotonicity. For fixed N and h→0, w_1/w_0=N²h, E x=Nh+O(h²); the square-root response only appears after taking a large-N regime N sqrt(h)≫1. These limits do not commute. The low-source crossover is h~N^−2, or gbar~b/(nN²). Large-N expansion at fixed h gives Var(j)/E j→(1−x_*)/(2−x_*). This follows from drift derivative −κ(h+2x_*) and jump variance rate 2κN x_*², giving Var(j)≈N x_*²/(h+2x_*)=N x_*(1−x_*)/(2−x_*). It is an asymptotic discriminator, not an exact finite-N identity.

## B. Gapless vector-mass spectrum

Set ℏ=kB=1 in this model. Let σ_i be Pauli matrices. Define Γ1=σ1⊗I, Γ2=σ2⊗I, Γ3=σ3⊗σ1, Γ4=σ3⊗σ2, Γ5=σ3⊗σ3. Their anticommutators are 2δ_ab I. For a spatially constant three-component order parameter u define

H(k,u)=v k_x Γ1+v k_y Γ2+λ∑_(a=1)^3 u_a Γ_(a+2), |vk|≤Λ.

The spectrum is ±E_k=±sqrt(v²k²+λ²u²), each twice. At zero chemical potential and T=0, fill the two negative states. Subtract the u=0 sea energy per sheet area:

ΔF_f=−2∫d²k/(2π)² [sqrt(v²k²+λ²u²)−v|k|]
=−[(Λ²+λ²u²)^(3/2)−Λ³−λ³|u|³]/(3πv²).

Let η be sheet area per volume if converting to a bulk density. Its value is an additional medium parameter. With η=1 in normalized checks,
ΔF_f=−Λλ²u²/(2πv²)+λ³|u|³/(3πv²)−λ⁴u⁴/(8πv²Λ)+λ⁶u⁶/(48πv²Λ³)+... .

Adding a bare quadratic F_bare=[1/(2K)+ηΛλ²/(2πv²)]u² leaves the specified full susceptibility and a positive cubic remainder. This is explicit tuning. Cubic coefficient matching requires ηλ³/(πv²)=1/(Ka0). This does not predict a0. The quadratic-subtracted fermion remainder is globally nonnegative and increasing: its derivative is ηλ²u[Λ+λu−sqrt(Λ²+λ²u²)]/(πv²)>0 for u>0. It has no finite capacity.

The microscopic operator conjugate to u_a is λ ψ†Γ_(a+2)ψ. To obtain a gravitational response one must separately couple −g·u/K and identify this internal O(3) mass order parameter with a spatial polarization. The spectrum's internal rotations allow an isotropic function of u, but do not derive that physical identification. Ordinary three-dimensional linear dispersion changes the integral's nonanalytic term to order u⁴ log u. Therefore bulk three-dimensional Dirac particles do not supply this cubic without a different density of states or lower-dimensional modes.

At finite temperature the exact derivative of the subtracted fermion free energy (before the zero-temperature quadratic correction) is

∂_u ΔF_(f,T)=−λ²u/(πv²)∫_(λu)^(sqrt(Λ²+λ²u²)) tanh(E/(2T)) dE
=−2Tλ²u/(πv²)[log cosh(sqrt(Λ²+λ²u²)/(2T))−log cosh(λu/(2T))].

For fixed T>0 its local expansion contains u and u³ but no u². If its actual thermal quadratic term is subtracted, the remainder force is O(u³). The desired u² term exists only in the zero-temperature limit or intermediate window T≪λu≪Λ. This infrared crossover is an additional discriminator.

## C. Capacity attempted and rejected in a common equilibrium ensemble

An independent bounded orientational degree of freedom at T>0 gives a logarithmically divergent Legendre energy near full polarization and a simple-pole conjugate force. Adding its free energy to the zero-temperature sea formula would combine incompatible strict thermal limits if both are asserted to be one equilibrium system. At their common T>0, the gapless determinant is rounded and the exact cubic is lost; at T=0, the classical orientational entropy coefficient vanishes. Two reservoirs could maintain the two sectors at different temperatures but would require an explicit nonequilibrium reduction; that was not constructed.

Even as a formal hybrid, a cubic plus an otherwise even analytic function lacks the target |u|^5/(5K n b^3) coefficient: target W_rem has every power u^k, k≥3. Matching the cubic, one quartic and a capacity residue cannot establish the exact law. No capacity term is invented here to hide that mismatch.

## D. Units, sign comparison, and finite-temperature derivation

In the Hamiltonian, k is inverse length, v has units energy×length (ℏ=1), Λ is energy, and λ has units energy/acceleration when u retains the target acceleration units. The fermionic integral is energy/area. η has units inverse length, so ηF_f is energy/volume and can be compared with u²/K. K=4πG has units length³/(mass×time²). No actual sheet geometry, area density, or constitutive coupling has been selected.

The target has positive quartic n u⁴/(4K a0²); the quadratic-corrected determinant has negative quartic −ηλ⁴u⁴/(8πv²Λ). Therefore this particular microscopic Hamiltonian plus quadratic counterterm cannot equal the target for any n>0 even locally beyond cubic order. A positive analytic quartic interaction could change this conclusion only by adding a new microscopic input; it is not generated by the displayed sea integral.

For clarity the finite-temperature derivative follows without importing a theorem: each ±E pair contributes −T[log(1+exp(−E/T))+log(1+exp(E/T))]; differentiate to get −tanh(E/(2T))dE/du, multiply by the two identical pairs, and perform the radial integral. At each T>0 the lower-end log cosh is even analytic in u. This establishes the stated rounding directly.

For the three-dimensional comparison, differentiate the radial sea integral twice with respect to s=m²: d²/ds²∫_0^Λ k² sqrt(k²+s)dk=−(1/4)∫_0^Λ k²(k²+s)^−3/2 dk. Its logarithmic small-s behavior integrates twice to s² log s (up to analytic terms), rather than s^(3/2). This comparison refers only to linear dispersion and a regular three-dimensional momentum measure.
