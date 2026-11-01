# TP04 radial dynamics and coherent cold-state test

The microscopic model has a stable, very light radial oscillator around the quantum vacuum. It is a different state from the previously tested rotating charge fluid. The actual finite radial coefficient has now been calculated, rather than identified with the angular coefficient. The rotating branch's negative-compressibility region remains a rapid spatial instability. The uncharged oscillator is cold at sufficiently small amplitude/momentum, but an actual phase-production channel imposes a density-dependent survival condition in addition to its perturbative width. No physical scale, abundance, cosmology or halo has been selected here.

## Matched radial action and evidence

All calculations use the retained original-X chart s=lnX, fixed couplings f=1,h=lambda=e,g=sqrt(29/200)e, and the TP03 fixed Q²=e/31+(e X_treeCWmin)². The raw canonical SU5 action, full 98-real-scalar matrices, 73-Weyl matrices and 24-vector matrices are immutable TP01--03 inputs. `radial_metric.py` differentiates the actual full matrices and includes scalar, scalar-Majorana, Landau scalar-vector and transverse vector-vector bubbles. The scalar-Majorana chirality-flip sign differs from the angular graph. There is no small-F Kahler substitution.

The one-loop heavy geometric pullback is **deltaA_h=(deltaF_h)_s-deltaF_h**, not deltaF_h. The reported A contains this pullback once and the new direct radial graph once. The angular F and the complete finite two-loop reduced V are TP03 inputs. The first local vacuum pole is m²=V_ss/(2A), with canonical sigma=sqrt(2A)delta s and phase pi=sqrt(2F)theta. The derivative coupling is g_sigma=Fs/(2F sqrt(2A)). Values at the matched quantum minimum, with the finer log-field stencil, are:

| e | A | F | m/sqrt(f) | g_sigma sqrt(f) | Gamma_phase/sqrt(f) |
|---|---:|---:|---:|---:|---:|
| .01 | 5418.5375122 | 5418.5373710 | 1.6765750e-7 | .0096060306 | 4.3257064e-27 |
| .03 | 1783.1598931 | 1783.1594706 | 8.9579274e-7 | .0167451834 | 2.0049455e-24 |

Here sqrt(f) is the unselected common mass unit. The finite direct radial graphs are -.0086162321 and -.0254249091; the radial heavy pullbacks are +.0054459789 and +.0160368868. Their differences from the angular coefficient are small compared with the tree metric, but are measured rather than assumed zero.

`run_metric/result.json` passes full-matrix derivative controls (maximum absolute error9.27e-11), full-Weyl vertex norm (3.56e-15), group UV identity (4.17e-16), finite scale derivative, exact equal-e scaling and null-sector handling. The unambiguous ungauged SUSY limit A_graph=F_graph agrees within3.5e-18, and SV/VV vanish with g. The gauged f=0 slice has an additional light modulus: its off-shell A-F difference is recorded, not forced to vanish and not promoted to a physical anisotropy. Independent algebra review confirmed the scalar/fermion signs and VV projector coefficient, without independently auditing all model vertices.

The isolated component coefficient depends on gauge, subtraction and field chart. X is a gauge singlet and the heavy invariant normals are eliminated, but one fixed-gauge matching calculation is not a proof of a gauge-independent all-order pole. The mass is a controlled local fixed-order result. The smallest massive-loop m² exceeds the radial pole by factors9.2e8 and9.8e7 respectively; expansion in external momentum is justified on the sampled vacuum. Gauge variation, higher loops and full interacting IR self-energies have not been certified.

## Circular-state dispersion and known tree completion

Use Omega=V-Fq-Jq²/2, q=omega², C=2F+6Jq, N=Omega_ss, D=N+4q(Fs+Jsq)²/C and vtheta²=n/(omega C). The leading local determinant is

    (Omega_freq²-k²-N/(2A))(Omega_freq²-vtheta² k²)
           -[(D-N)/(2A)]Omega_freq²=0.

The k=0 gap is D/(2A), not N/(2A); the gapless sound speed is vtheta² N/D and agrees with the independently recorded thermodynamics. The X/Xmin=1.2 states are stable on the declared finite momentum grid. At1.3 the results are:

| e | k_cut/sqrt(f) | k_peak/sqrt(f) | Gamma_max/sqrt(f) | Gamma_max/omega |
|---|---:|---:|---:|---:|
| .01 | 5.2979875e-8 | 3.3932649e-8 | 1.5874788e-8 | .35913192 |
| .03 | 2.7460925e-7 | 1.7740084e-7 | 7.8956074e-8 | .33067455 |

This is a finite-band spatial instability of those actual states, not simply a negative formal EOS derivative. Its momenta and background frequency remain far below the massive-loop thresholds. The stable interior rotating fluid remains warm: this task does not reopen it as a cold component.

The first dynamics run explicitly omitted q-activated radial higher-derivative terms. The subsequent `COVARIANT_HEAVY_COMPLETION.md` closes the known tree part, including the CP-odd relative heavy phase that vanishes in the homogeneous grand potential. Integrating both raw b normals gives

    L4=J/2 {[(partial theta)²-Box s-(partial s)²]²
                  +[Box theta+2partial s dot partial theta]²}.

The equality of the two raw b Hessians follows directly from the restricted tree potential term30|a|²|hX-lambda b|² at b0=hX/lambda: both Re(delta b) and Im(delta b) have Hbb=60lambda²a0², with no linear mixed a-b Hessian there. This is a heavy relative phase at fixed X, not the retained massless common phase.

The second square contributes to finite-frequency radial/phase mixing. Its quadratic entries and order reduction are recorded explicitly; extra high-derivative polynomial roots are not new particles. Independent direct expansion of the microscopic kinetic term confirmed both sources and the mixed coefficient2Jp², with the review restricted to this algebra rather than a complete pole/IR theorem. `run_heavy_completion/result.json` gives vacuum delta m²/m²=-4.22e-11,-4.01e-10 and charged k_cut² relative shifts -1.65e-12,-1.93e-11. The correction to the maximum growth is below1e-12 relative in the finite computation; no precision claim at that small level is needed for the instability conclusion. The IR sound slope is unchanged. This supplement supersedes the initial run's named tree omission, while preserving the original evidence. It does not complete higher p6, one-loop higher-derivative or nonlocal terms.

## Uncharged coherent radial state

A small, slowly varying sigma(t)=Sigma cos(mt) has average pressure zero at harmonic order and nonrelativistic gradient pressure at k<<m. It carries no stipulated conserved phase charge. This is an accessible coherent field state of the model, rather than an added particle species or abundance. Its weak-coupling leading constants, independently reproduced at both couplings, are

    m/sqrt(f) = .00016705339391 e^(3/2),
    v/sqrt(f) = 7.36714372128 e^(-1/2),
    g_sigma sqrt(f) = .095981130264 e^(1/2),
    Gamma_phase/sqrt(f) = 4.27206427928e-16 e^(11/2).

The quoted finite values in the table include TP03 two-loop vacuum/finite metric corrections. These analytic leading scaling laws can be taken to smaller e; they are not fresh full finite-spectrum runs at an arbitrary smaller e. The recorded canonical cubic ratio is V_sigma_sigma_sigma Sigma/m²=-8.72793 eta, eta=g_sigma Sigma. Its contribution to the force at the oscillation amplitude includes the Taylor factor1/2: -4.36396 eta relative to the harmonic force. Precision harmonic evolution therefore requires eta much less than .01. There is no claim that finite-amplitude native trajectories were solved.

The local interaction g_sigma sigma(partial pi)² gives Gamma(sigma->pi pi)=g_sigma²m³/(32pi), reducing to m³/(64pi v²) at tree normalization. Its massless phase loop is a nonlocal p4 log(-p²) self-energy, not a missing local p² metric. Its absorptive magnitude at the pole is |Im Sigma(m²)|=g_sigma²m4/(32pi)=m Gamma. It is tiny relative to the dimensionless pole here (Gamma/m=2.58e-20,2.24e-18), but an absolute lifetime still depends on sqrt(f). Other widths/current/anomaly effects belong to the companion cold-state and gapless-sector work. A perturbative phase mass below m/2 is assumed for this channel; a nonperturbative gap must be assessed separately.

## Parametric phase production: measured bound, not only a width

The same radial state pumps phase waves. At leading small amplitude y=R theta has the exact stipulated harmonic-pump equation

    y''+[kappa²+eta cos(tau)/(1+eta cos(tau))]y=0,
    tau=mt, kappa=k/m.

`run_floquet/result.json` computes the monodromy, including its exact zero-k constant-phase solution. The first band centers at k=m/2, has fractional half-width eta and maximum amplitude exponent mu_F=eta m/2. At eta=1e-5,1e-4,.001,.01 the declared interior points agree with the narrow-band formula within.433%; outside-band growth is below7.1e-17m. Wronskians and tighter-tolerance repeats pass.

Expansion redshifts a comoving mode through the narrow band. When m>>H and eta<<1, the integrated amplitude gain is

    I_cross=pi eta² m/(4H)=pi g_sigma² rho/(2mH),
    rho=m²Sigma²/2,
    I_cross/(Gamma_phase/H)=16pi² rho/m4.

Thus mu_F/H alone is not the relevant crossing test. The pump must remain coherent, and the mode spends a limited time in the band. For fixed density, making e small enough to lengthen the perturbative lifetime does not by itself remove stimulated phase production. The displayed density/scale-dependent inequality must also be checked.

The expanding harmonic-pump ODE was actually integrated. The first run included finite examples chi=eta²m/H=.1,1,3; their integrated band gains matched pi chi/4 within2.6e-5, and larger chi produced substantial amplification. Its chi=.1 in/out endpoints were only2.53 Fresnel formation lengths from the crossing, so that finite occupation is not an asymptotic weak-crossing result. This was identified and preserved, then tested in the fresh endpoint follow-up.

`run_floquet_endpoints/result.json` extends eta=.001 examples to +-64/sqrt(H/m), varies endpoint formation length8,16,32,64 and changes pump phase. At chi=.02,.1 it gives N=.03125985,.16736713 against the asymptotic narrow prediction exp(pi chi/2)-1=.03191462,.17008879:1.6--2.1% differences. Pump-phase changes are below.70%, and maximum Wronskian error8.24e-8. This is a quantitative weak-crossing check; it does not claim asymptotic occupation for every earlier finite strong-crossing example, nor solve nonlinear backreaction or depletion.

For a putative virialized coherent domain, conditional estimates tau_coh~1/(m v²),ell_coh~1/(mv) give mu_F tau_coh~eta/(2v²) and mu_F ell_coh~eta/(2v). Phase escape and incoherent domains can limit gain. Conversely an infinitely homogeneous Minkowski pump has a genuine narrow resonance for every nonzero amplitude. No velocity dispersion, domain geometry, random-phase transport or halo boundary has been chosen here; these estimates are not a universal halo decay law.

## Earned implication and remaining discriminator

The microscopic action supplies a real small-amplitude cold coherent candidate and its couplings, with bounded finite radial matching and measured phase production. It has not supplied a density or a cosmological preparation mechanism. Survival requires both acceptable perturbative widths and acceptable collective production/transport for the same scale, density and state. Tying sqrt(f) to a prescribed vacuum energy is a separate physical restriction; allowing an independent scale is another scenario, and this calculation does not exchange them silently.

The smallest next physical discriminator is to insert a specified common scale and radial energy density into eta=g_sigma sqrt(2rho)/m and chi=2g_sigma²rho/(mH), then use the same perturbative and crossing bounds. Writing m=mu mhat and g_sigma=ghat/mu, the bound chi<chi_max is mu>[2ghat²rho/(mhat H chi_max)]^(1/3). Its leading e dependence is e^(-1/6), weaker than the small-amplitude density lower bound e^(-1/2); collective production therefore does not automatically close every free-scale weak-e interval. A halo claim additionally needs coherent-domain escape/dephasing or a solved transport model. This is more discriminating than repeating the warm circular-fluid EOS or merely noting a tiny width in f=1 units.

Five v2 manifests have been checked by the supplied manifest validator against current on-disk hashes: `run_metric`, `run_dynamics`, `run_floquet`, `run_heavy_completion`, `run_floquet_endpoints`. All declared controls pass. The largest measured RSS was249.4MB and each experiment took under13seconds; one numerical thread and supported wall/CPU limits were used. No memory/affinity cap unavailable on this platform is claimed. Manifests freeze the actual active revision and dirty inputs rather than pretending the initial shared base remained unchanged. No TP01--03 input was changed by this task.
