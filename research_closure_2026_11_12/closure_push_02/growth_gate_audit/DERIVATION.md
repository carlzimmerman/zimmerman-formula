# Corrected polarization growth and unchanged-clock background

This is a new, bounded audit. Historical QX3, KD1, MK1 and PIK1 sources and their frozen criteria are unchanged. Exact input snapshots and their SHA256 values are in `sources/index.json`. The experiment is a leading cold, subhorizon, post-recombination reference, not a Boltzmann calculation or a replacement data likelihood. The BBN calculation below is instead an exact homogeneous-clock identity evaluated against the already-declared KD1 criterion.

## 1. Where the imported number comes from

PIK1 `FROZEN_CRITERIA.md:58–59` imports two different lines: background coldness gives mu>=198.25/Mpc; the purported linear-growth consequence imports mu>=25120/Mpc from MK1/KD1/QX3. MK1 `mk1_rows.py:50–68` reads that growth number from `kd1.json`; it does not rerun it. KD1 `kd1.py:45–50,157–161` calls QX3's growth ratio and Limber rescaling before grading the PR4 lensing shape difference. These are not separate RSD or forest likelihoods.

The load-bearing QX3 code is `iter2.py:68–75`: its dark self-source is `(3/2)Omega_d(a)[1-(k/(a mu))²]`. QX3's frozen criteria state the same isolated n=1-polytrope Jeans equation and explicitly assume the polarization law is off on the linear web. The acoustic model can be studied under that assumption. It is not the full action's polarization-constrained linear equation derived below. Consequently 25118.864315095823/Mpc is not a validated growth threshold for the corrected model. Its historical likelihood statistic is not recalibrated by changing a printed label.

The original code's `zw=np.gradient(zgrid)` is unused, but this is not the decisive issue: its z grid is uniform, so a constant quadrature spacing cancels in its numerator/denominator ratio. The decisive change is the physical perturbation equation. No claim about all other aspects of the PR4 machinery is made here. `classy` is not installed in the current Python environment, and no new PR4 likelihood is executed.

## 2. Scale factors and actual charge perturbations

Set c=1, K=4piG, F(Q)=mu²(Q-1)²/(2K), x=Q-1, and use comoving coordinates r=a(t)X. Write the clock as tau=t+sigma. The physical peculiar velocity is v=-grad_X(sigma)/a and

```text
x = sigma_dot - Phi - |grad_X sigma|²/(2a²),
Pi = div_X P/a,
n = F_Q + Pi = (mu²/K)x + Pi.
```

Here P denotes components in the physical spatial orthonormal frame. Near P=0 the QX17 polarization energy is W=K|P|²/2+O(|P|³). Take the smooth gamma=0 reference and a flat gate endpoint with H(Q,0)=F(Q), H_Pi=H_QPi=H_PiPi=0. The linear polarization constraint and the conserved-charge/Euler equations are

```text
grad_X delta x/a + K delta P = 0,
delta Pi = -Delta_X delta x/(K a²),
n_dot + 3Hn + div_X(n v)/a = 0,
v_dot + Hv + (v.grad_X)v/a = -grad_X(Phi+x)/a,
Delta_X Phi/a² = K(rho_b delta_b + nbar delta_d).
```

The homogeneous mode is removed from the perturbation Poisson equation because it already determines H. For a nonzero comoving Fourier mode k,

```text
k_phys=k/a,
delta n = (mu²+k_phys²) delta x/K,
delta x = K nbar delta_d/(mu²+k_phys²).                    (1)
```

The density being transported and sourcing the leading Poisson equation is n=F_Q+Pi, not F_Q alone. Replacing it with F_Q before eliminating P loses the k_phys² term. Linear continuity gives delta_d_dot=-div_X(v_d)/a. Differentiating it, using the Hubble drag in Euler, gives

```text
delta_d_ddot + 2H delta_d_dot
  = K rho_b delta_b + K nbar [mu²/(mu²+k²/a²)] delta_d,      (2)

delta_b_ddot + 2H delta_b_dot
  = K rho_b delta_b + K nbar delta_d.                       (3)
```

Baryons feel the full gravitational source; they do not feel the clock's extra x force. Dark acceleration retains the full baryon term. Multiplying the entire matter source by the suppression factor would therefore be another error. The dark self-source stays positive and tends to zero at large k_phys; it does not become a negative acoustic term.

For derivatives with respect to eta=ln(a), (2) becomes

```text
delta_d'' + [2+dlnH/dlna]delta_d'
  = (3/2)[Omega_b(a)delta_b + Omega_d(a)f_mu(a,k)delta_d],
f_mu = 1/[1+(k/(a mu))²],
```

and (3) has f_mu replaced by 1. In the calculation Omega_d means the leading conserved cold density nbar, proportional to a^-3. The common background is `H²/H0²=Omega_r0 a^-4+(Omega_b0+Omega_d0)a^-3+Omega_L0`.

For nonnegative initial densities and eta derivatives, this four-state system has nonnegative off-diagonal coefficients. The usual comparison argument for cooperative linear ODEs therefore orders the densities as mu increases, below the infinite-mu reference with the same initial state. It does not compare arbitrarily changed primordial spectra or initial velocities.

## 3. Limits and the numerical contract

With no baryons and k_phys/mu tending to infinity in matter domination, the dark mode obeys delta''+delta'/2=0. With delta=delta'=1 initially it tends to 3, rather than oscillating. Baryons feed dark growth even when direct dark self-growth vanishes. At a fixed high-k limit in matter domination, the density coupling matrix is

```text
M = [[f_b,f_d],[f_b,0]],
lambda_+ = [f_b+sqrt(f_b²+4f_b f_d)]/2,
p_+ = [-1/2+sqrt(1/4+6lambda_+)]/2,
delta proportional to a^p_+.
```

For the benchmark f_b=.16, p_+=.6133364878069335. The infinite-mu EdS mode is delta proportional to a. In matter plus smooth radiation, neglecting Lambda, the exact growing reference is the Meszaros solution delta proportional to `1+3a/(2a_eq)`; this supplies the stated initial logarithmic derivative. These three separate limits check the solver's factors and signs.

The executed contract uses the recorded KD1 canonical and alt parameters. It starts at z=1090 or z=100, after the historical switch-on epoch for pressureless baryons. At each start it compares either equal baryon/dark growing initial data or baryon-zero catchup initial data to the identical infinite-mu initial state. These are controlled transfer comparisons, not calculated recombination transfer functions. Starting at z=100 deliberately resets any earlier suppression; that late-start result cannot be used as the full primordial transfer.

For mu=198.254232363749/Mpc, the canonical maximum homogeneous x from z=1090 onward is .00066688225. The smallest sampled k satisfies k/(aH)>=28.1545 at the start. The omitted stiff density is .00088457 of radiation there and an even smaller fraction of the total. These numbers make a leading cold/subhorizon diagnostic useful; they do not give a bound on all omitted radiation perturbations, recombination physics or relativistic transfer errors. The displayed numerical precision is solver precision within the model.

The original one-sided stiffness gamma Pi_+²/2 has no unique Frechet Hessian at Pi=0. The gamma=0 run is a separately specified smooth reference, not a rigorous nonlinear upper bound for that switch. For an everywhere-quadratic nonnegative stiffness Gamma, or a background with a defined nonnegative Hessian, the local elimination gives

```text
delta x/delta n = (K+Gamma k_phys²)
                 /[(mu²/K)(K+Gamma k_phys²)+k_phys²].
```

Increasing Gamma increases this response and the pressure cancellation term k_phys² delta x, reducing direct dark self-growth at fixed background. The flat additions in the two proposed repairs do not alter the smooth endpoint's quadratic coefficients. A proposed repair with different linear endpoint coefficients needs its own calculation.

## 4. Exact homogeneous inventory and the BBN test

For either proposed repair H(Q,0)=F(Q) exactly. Homogeneity and isotropy give P=Pi=0. The exact conserved clock current then gives, without a cold or subhorizon approximation,

```text
a³ n = constant,      n=F_Q=mu²(Q-1)/K,
rho=QF_Q-F = n + K n²/(2mu²),
p=F = K n²/(2mu²).                                    (4)
```

Thus the same positive inventory produces an a^-3 cold term and an a^-6 stiff term. This statement holds even when Q-1 is huge at early times. Failure of a Newtonian approximation at BBN does not remove (4).

Use KD1's notation `I0=2Kn0=3(H0/c)²Omega_d0` and `w0=I0/(4mu²)`. Then

```text
rho(a)=rho_d0 a^-3[1+w0 a^-3],
w(a)=w0/[a³+w0],
rho_stiff/rho_r = Omega_d0 I0/[4mu² Omega_r0 a²].         (5)
```

The historical B1a condition w(z3400)<=.01 is only a coldness condition. The separate KD1 B1b condition, explicitly frozen at `FROZEN_CRITERIA.md:65`, is

```text
T=0.1 MeV, Tcmb=2.7255 K,
a_BBN = 1/[1+10^5 eV/(k_B Tcmb)] = 2.3486541750419234e-9,
Omega_r h² = 2.47e-5[1+.2271*3.046],
rho_stiff/rho_r <= .067,
mu >= sqrt[Omega_d I0/(4*.067*Omega_r*a_BBN²)].            (6)
```

The .067 budget is a declared project criterion, approximately the post-annihilation radiation fraction for Delta N_eff=.5; it is not asserted here to be a newly verified or current observational likelihood bound. An a^-6 stiff component also does not represent a constant Delta N_eff across BBN: its ratio to radiation changes as a^-2. The frozen temperature-scale-factor conversion approximates the thermal history by the stated photon/neutrino convention and does not solve finite electron-positron annihilation. Its trailing digits are a reproduction of that convention, not an exact thermodynamic calculation at .1 MeV. No external observational result is needed to reproduce or interpret this explicit conditional criterion.

Equation (6) exactly reproduces the recorded canonical mu>=8.89011353538235e6/Mpc and alt mu>=8.889273437013572e6/Mpc. At the low canonical mu_B1a, (5) is 1.347238491702006e8, about 2.01e9 times the budget. Even the historical growth value mu=25118.864315095823 gives 8392.4626559, about 1.25e5 times the budget. Order-one changes in the specified radiation budget or thermal convention cannot bridge these gaps.

If the early homogeneous charge were a fraction f of the inventory used today, the stiff contribution scales as f². At mu=198.254, satisfying the same budget would require f<=2.2300528736e-5. The same homogeneous source-free clock has no mechanism to increase a³n by the required factor later. Spatial redistribution also does not create global conserved charge. A different early-time action/branch, additional source or stress sector, or a nonstandard cosmological history could change this conclusion, but is outside these unchanged-FRW repairs. This is a scoped obstruction, not a theorem against every possible later extension.

## 5. Claim dispositions

- The transferred mu>=25120 claim for the full polarization-constrained linear model is **inapplicable without a new likelihood calculation**: the old bound uses a different growth equation.
- Equations (1)–(3) are **correct after the stated cold, subhorizon, smooth-endpoint restriction**, and their finite numerical comparison is verified in the recorded range.
- The unchanged-FRW identity (4) is **exact on the homogeneous source-free branch**. Under that branch/history assumption, the low-mu repair **fails the existing specified BBN criterion**, independently of the disputed growth bound.
- No new CMB, lensing, forest, primordial-transfer, nonlinear-formation or full cosmological viability verdict is produced by the post-recombination table alone.
